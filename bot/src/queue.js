import { Readable } from 'node:stream';
import { AudioPlayerStatus, StreamType, createAudioResource } from '@discordjs/voice';

/** Release an unused audio result (a stream is destroyed so its download stops). */
function discard(audio) {
  if (audio && typeof audio.destroy === 'function') audio.destroy();
}

const MAX_PLAY_MS = 180_000; // safety net: never let one chunk wedge the queue

/**
 * Ordered speech queue. Text chunks are synthesized ahead of playback (bounded by `prefetch`)
 * and played one at a time, in order, through a single AudioPlayer.
 */
export class SpeechQueue {
  /**
   * @param {object} o
   * @param {import('@discordjs/voice').AudioPlayer} o.player
   * @param {(text: string, voice: string) => Promise<Buffer | import('node:stream').Readable>} o.synthesize  encoded audio (mp3 etc.), whole or streaming
   * @param {number} [o.prefetch]
   * @param {ReturnType<import('./logger.js').createLogger>} o.logger
   */
  constructor({ player, synthesize, prefetch = 2, logger, maxChunks = 0, maxSeconds = 0, charsPerMinute = 900, onBacklogDrop = null }) {
    this.maxChunks = maxChunks; // backlog safeguard: 0 = off
    this.maxSeconds = maxSeconds; // estimated seconds of pending (not yet playing) audio; 0 = off
    this.charsPerMinute = charsPerMinute;
    this.onBacklogDrop = onBacklogDrop;
    this.player = player;
    this.synthesize = synthesize;
    this.prefetch = prefetch;
    this.log = logger;
    this.items = [];
    this.current = null;
    this.running = false;
    this.nextGroup = 1;
    this.enabled = true; // when false (not in voice) enqueue is refused
  }

  get size() {
    return this.items.length + (this.current ? 1 : 0);
  }

  /**
   * Queue text chunks as one group (one GM message). Returns the group id, or 0 if nothing was queued.
   * @param {(string | { text: string, voice?: string })[]} chunks  plain strings use the 'gm' voice
   * @param {{ label?: string }} [meta]
   */
  enqueue(chunks, meta = {}) {
    if (!this.enabled || chunks.length === 0) return 0;
    const groupId = this.nextGroup++;
    for (const chunk of chunks) {
      const { text, voice = 'gm' } = typeof chunk === 'string' ? { text: chunk } : chunk;
      this.items.push({ groupId, label: meta.label ?? '', text, voice, cancelled: false, ready: null });
    }
    this._trimBacklog(groupId);
    this._kick();
    void this._pump();
    return groupId;
  }

  /** Estimated seconds of speech in the pending (not yet started) items. */
  get pendingSeconds() {
    return this.items.reduce((sum, i) => sum + ([...i.text].length / this.charsPerMinute) * 60, 0);
  }

  /**
   * Backlog safeguard: if too many chunks / too much audio are pending, drop the OLDEST pending messages and
   * keep the newest. The message being played and the newest message are never dropped.
   */
  _trimBacklog(newestGroup) {
    if (!this.maxChunks && !this.maxSeconds) return;
    const over = () => (this.maxChunks > 0 && this.items.length > this.maxChunks) || (this.maxSeconds > 0 && this.pendingSeconds > this.maxSeconds);
    let messages = 0;
    let chunks = 0;
    while (over()) {
      const victim = this.items.find((i) => i.groupId !== newestGroup && i.groupId !== this.current?.groupId);
      if (!victim) break;
      for (const item of this.items) {
        if (item.groupId === victim.groupId) {
          item.cancelled = true; // a synthesis still in flight is discarded when it arrives (see _start)
          this._release(item); // ...and one that already finished is released now (stops a streaming download)
          chunks++;
        }
      }
      this.items = this.items.filter((i) => !i.cancelled);
      messages++;
    }
    if (messages) {
      try {
        this.onBacklogDrop?.({ messages, chunks });
      } catch (err) {
        this.log.warn(`Backlog callback failed: ${err?.message ?? err}`);
      }
    }
  }

  /** Skip the chunk being played plus the rest of its message; with `all`, drop everything. Returns #chunks dropped. */
  skip({ all = false } = {}) {
    let dropped = 0;
    if (all) {
      for (const item of this.items) {
        item.cancelled = true;
        this._release(item);
        dropped++;
      }
      this.items = [];
    } else if (this.current) {
      for (const item of this.items) {
        if (item.groupId === this.current.groupId) {
          item.cancelled = true;
          dropped++;
        }
      }
      this.items = this.items.filter((i) => !i.cancelled);
    } else if (this.items.length) {
      // Nothing playing yet (still synthesizing the head): skip the head message.
      const gid = this.items[0].groupId;
      for (const item of this.items) if (item.groupId === gid) { item.cancelled = true; dropped++; }
      this.items = this.items.filter((i) => !i.cancelled);
    }
    if (this.current) {
      this.current.cancelled = true;
      dropped++;
      this.player.stop(true);
    }
    return dropped;
  }

  /** Drop everything and stop audio (used on /leave and disconnect). */
  clear() {
    return this.skip({ all: true });
  }

  /** Release the audio of an already-synthesized item that will never be played. */
  _release(item) {
    item.ready?.then((r) => discard(r.audio)).catch(() => {});
  }

  _start(item) {
    if (item.ready) return;
    this.log.debug(`TTS synth [${item.voice}]: "${item.text.slice(0, 60)}${item.text.length > 60 ? '…' : ''}"`);
    item.ready = this.synthesize(item.text, item.voice).then(
      (audio) => {
        if (item.cancelled) discard(audio); // skipped while synthesizing: stop any in-flight stream
        return { audio };
      },
      (error) => ({ error })
    );
  }

  /** Start synthesis for the first `prefetch` queued items. */
  _kick() {
    for (const item of this.items.slice(0, this.prefetch)) {
      if (!item.cancelled) this._start(item);
    }
  }

  async _pump() {
    if (this.running) return;
    this.running = true;
    try {
      while (this.items.length) {
        const item = this.items.shift();
        this.current = item;
        this._kick();
        if (item.cancelled) continue;
        this._start(item);
        const result = await item.ready;
        if (item.cancelled) {
          discard(result.audio);
          continue;
        }
        if (result.error?.code === 'SESSION_CAP') {
          this.log.debug('Voice session cap reached: chunk not synthesized');
          continue;
        }
        if (result.error) {
          this.log.error(`TTS synthesis failed, dropping chunk: ${result.error.message}`);
          continue;
        }
        await this._play(result.audio);
      }
    } finally {
      this.current = null;
      this.running = false;
      // A chunk may have been enqueued between the loop check and here.
      if (this.items.length) void this._pump();
    }
  }

  _play(audio) {
    return new Promise((resolve) => {
      let timer;
      const done = () => {
        clearTimeout(timer);
        this.player.off('stateChange', onState);
        this.player.off('error', onError);
        resolve();
      };
      const onState = (_old, next) => {
        if (next.status === AudioPlayerStatus.Idle) done();
      };
      const onError = (err) => {
        this.log.warn(`Audio player error: ${err.message}`);
        this.player.stop(true);
        done();
      };
      this.player.on('stateChange', onState);
      this.player.on('error', onError);
      timer = setTimeout(() => {
        this.log.warn('Playback timed out; stopping player');
        this.player.stop(true);
        done();
      }, MAX_PLAY_MS);
      // Arbitrary => ffmpeg (via prism-media) transcodes mp3/etc to 48kHz Opus.
      // `audio` is a Buffer (OpenAI/ElevenLabs) or a Readable that is still filling (Fish streaming).
      const input = Buffer.isBuffer(audio) ? Readable.from([audio]) : audio;
      const resource = createAudioResource(input, { inputType: StreamType.Arbitrary });
      this.player.play(resource);
    });
  }
}
