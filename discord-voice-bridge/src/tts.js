import { PassThrough, Readable } from 'node:stream';
import { fetchWithRetry } from './http.js';
import { VOICE_GM, isNpcVoice, npcNameOf } from './tags.js';
import { prepareSpeechDetailed } from './text.js';

/** OpenAI Text-to-Speech (/v1/audio/speech). Returns MP3 bytes. `voices` maps 'gm' / 'system' to settings. */
export class OpenAiTts {
  constructor({ apiKey, baseUrl, voices }) {
    Object.assign(this, { apiKey, baseUrl, voices });
    this.id = 'openai';
    this.name = `openai:gm=${voices.gm.model}/${voices.gm.voice},system=${voices.system.model}/${voices.system.voice}`;
  }

  modelFor(voice) {
    return (this.voices[voice] ?? this.voices[VOICE_GM]).model;
  }

  async synthesize(text, voice = VOICE_GM) {
    const v = this.voices[voice] ?? this.voices[VOICE_GM];
    const body = { model: v.model, voice: v.voice, input: text, response_format: 'mp3' };
    // `instructions` is only supported by the gpt-4o-mini-tts family.
    if (v.instructions && v.model.startsWith('gpt-4o')) body.instructions = v.instructions;
    if (v.speed && v.speed !== 1) body.speed = v.speed;
    const res = await fetchWithRetry(
      `${this.baseUrl}/audio/speech`,
      () => ({
        method: 'POST',
        headers: { Authorization: `Bearer ${this.apiKey}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      }),
      { label: 'OpenAI TTS' }
    );
    return Buffer.from(await res.arrayBuffer());
  }
}

/** ElevenLabs Text-to-Speech. Returns MP3 bytes. `voices` maps 'gm' / 'system' to voice settings. */
export class ElevenLabsTts {
  constructor({ apiKey, voices }) {
    Object.assign(this, { apiKey, voices });
    this.id = 'elevenlabs';
    this.name = `elevenlabs:gm=${voices.gm.voiceId},system=${voices.system.voiceId}`;
  }

  modelFor(voice) {
    return (this.voices[voice] ?? this.voices[VOICE_GM]).modelId;
  }

  async synthesize(text, voice = VOICE_GM) {
    const v = this.voices[voice] ?? this.voices[VOICE_GM];
    const url = `https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(v.voiceId)}?output_format=mp3_44100_128`;
    const res = await fetchWithRetry(
      url,
      () => ({
        method: 'POST',
        headers: { 'xi-api-key': this.apiKey, 'Content-Type': 'application/json', Accept: 'audio/mpeg' },
        body: JSON.stringify({
          text,
          model_id: v.modelId,
          voice_settings: { stability: v.stability, similarity_boost: v.similarity },
        }),
      }),
      { label: 'ElevenLabs TTS' }
    );
    return Buffer.from(await res.arrayBuffer());
  }
}

/**
 * Fish Audio TTS (POST {baseUrl}/v1/tts, Bearer auth, `model` header, JSON body, chunked audio response).
 * `synthesize()` resolves as soon as the response headers arrive and returns a *stream* that keeps filling
 * in the background, so ffmpeg/Discord can start playing the first audio while the rest is still arriving.
 * The stream carries `.usage`, a promise of { ok, bytes, audioSeconds } for the usage log.
 *
 * `voices` maps 'gm' (narrator) / 'system' to { voiceId } - Fish "reference_id" model ids.
 * NPC voices ('npc:<name>', from the [NPC: Name] tag) resolve through `npcVoices` (src/npcvoices.js): no entry or no id ->
 * narrator; a Fish error on the NPC's id (deleted/private voice) -> that line is spoken by the narrator, a warning is logged
 * (nothing is posted to Discord) and the id is skipped for BAD_NPC_TTL_MS so later lines go straight to the narrator.
 */
const BAD_NPC_TTL_MS = 30 * 60_000;
export class FishTts {
  constructor({ apiKey, baseUrl = 'https://api.fish.audio', model = 's2.1-pro', voices, latency = 'balanced', format = 'mp3', mp3Bitrate = 128, speed = 1, npcVoices = null, logger = null }) {
    Object.assign(this, { apiKey, baseUrl: baseUrl.replace(/\/+$/, ''), model, voices, latency, format, mp3Bitrate, speed, npcVoices });
    this.log = logger ?? { warn() {}, debug() {} };
    this.badNpcIds = new Map();   // voice id -> failed at (ms)
    this.id = 'fish';
    this.name = `fish:${model}/gm=${voices.gm.voiceId},system=${voices.system.voiceId}`;
  }

  modelFor() {
    return this.model;
  }

  /** Never let the API key leak through error text. */
  _redact(message) {
    return this.apiKey ? String(message).split(this.apiKey).join('[redacted]') : String(message);
  }

  /** NPC voice id for 'npc:<name>' or null (narrator). Skips ids that just failed. */
  npcVoiceId(voice) {
    if (!isNpcVoice(voice) || !this.npcVoices) return null;
    const id = this.npcVoices.voiceIdFor(npcNameOf(voice));
    if (!id) {
      this.unknownNpcs ??= new Set();
      const name = npcNameOf(voice);
      if (!this.unknownNpcs.has(name)) {
        this.unknownNpcs.add(name);
        this.log.info?.(`NPC "${name}" has no Fish voice in tables/npc-voices.json${this.npcVoices.find(name) ? ' (entry without an id)' : ''}; using the narrator voice`);
      }
      return null;
    }
    const bad = this.badNpcIds.get(id);
    if (bad && Date.now() - bad < BAD_NPC_TTL_MS) return null;
    return id;
  }

  async synthesize(text, voice = VOICE_GM) {
    if (isNpcVoice(voice)) {
      const id = this.npcVoiceId(voice);
      if (!id) return this._synthesize(text, this.voices[VOICE_GM].voiceId);
      try {
        const out = await this._synthesize(text, id);
        this.badNpcIds.delete(id);
        return out;
      } catch (err) {
        if (err.status === 401 || err.status === 402) throw err;   // key/credit problem: the narrator would fail the same way
        this.badNpcIds.set(id, Date.now());
        this.log.warn(`Fish voice for NPC "${this.npcVoices.find(npcNameOf(voice))?.name ?? npcNameOf(voice)}" (${id}) failed (${err.status ? `HTTP ${err.status}` : err.message.slice(0, 120)}); this line uses the narrator. Fix or replace the id in tables/npc-voices.json.`);
        return this._synthesize(text, this.voices[VOICE_GM].voiceId);
      }
    }
    const v = this.voices[voice] ?? this.voices[VOICE_GM];
    return this._synthesize(text, v.voiceId);
  }

  async _synthesize(text, referenceId) {
    const body = {
      text,
      reference_id: referenceId,
      format: this.format,
      latency: this.latency,
      normalize: true,
    };
    if (this.format === 'mp3') body.mp3_bitrate = this.mp3Bitrate;
    if (this.speed && this.speed !== 1) body.prosody = { speed: this.speed, volume: 0, normalize_loudness: true };

    let res;
    try {
      res = await fetchWithRetry(
        `${this.baseUrl}/v1/tts`,
        () => ({
          method: 'POST',
          headers: { Authorization: `Bearer ${this.apiKey}`, 'Content-Type': 'application/json', model: this.model },
          body: JSON.stringify(body),
        }),
        { label: 'Fish Audio TTS', retries: 3, timeoutMs: 60_000 }
      );
    } catch (err) {
      err.message = this._redact(err.message);
      throw err;
    }

    // Pump the chunked response into a roomy PassThrough: playback can begin on the first bytes while the
    // download continues independently of how fast ffmpeg consumes it (so prefetched chunks never stall).
    const out = new PassThrough({ highWaterMark: 16 * 1024 * 1024 });
    const src = Readable.fromWeb(res.body);
    let bytes = 0;
    out.usage = new Promise((resolve) => {
      src.on('data', (c) => (bytes += c.length));
      src.on('end', () => resolve({ ok: true, bytes, audioSeconds: this._seconds(bytes) }));
      // Consumer stopped early (skip/leave): the request itself succeeded, so it still counts - by estimate.
      src.on('close', () => resolve({ ok: true, bytes, audioSeconds: null }));
      src.on('error', (err) => {
        out.destroy(new Error(this._redact(`Fish Audio stream error: ${err.message}`)));
        resolve({ ok: false, bytes, audioSeconds: null });
      });
    });
    src.pipe(out);
    out.once('close', () => src.destroy()); // consumer gave up (skip/leave): stop downloading
    return out;
  }

  /** Audio seconds derived from byte count when the format has a fixed, known bitrate. */
  _seconds(bytes) {
    if (this.format === 'mp3' && this.mp3Bitrate) return (bytes * 8) / (this.mp3Bitrate * 1000);
    if (this.format === 'wav') return Math.max(0, bytes - 44) / (44100 * 2);
    return null;
  }
}

/** Pluggable provider factory selected by TTS_PROVIDER. */
/** `extra` (Fish only): { npcVoices, logger } for the [NPC: Name] voices. */
export function createTtsProvider(config, extra = {}) {
  switch (config.tts.provider) {
    case 'openai':
      return new OpenAiTts({ apiKey: config.openai.apiKey, baseUrl: config.openai.baseUrl, voices: config.tts.openai.voices });
    case 'fish':
      return new FishTts({ ...config.tts.fish, ...extra });
    case 'elevenlabs':
      return new ElevenLabsTts({ apiKey: config.tts.elevenlabs.apiKey, voices: config.tts.elevenlabs.voices });
    default:
      throw new Error(`Unknown TTS provider "${config.tts.provider}"`);
  }
}

/** Watches the GM output channel and feeds new messages to the speech queue. */
export class GmOutputBridge {
  constructor({ client, config, session, queue, logger, sessionCap = null, dedupe = null, events = null }) {
    this.dedupe = dedupe;
    this.events = events;
    this.sessionCap = sessionCap;
    this.client = client;
    this.config = config;
    this.session = session;
    this.queue = queue;
    this.log = logger;
  }

  /**
   * Independent text sources for a message: its content, plus (optionally) each embed.
   * Tags are parsed per source, so an embed never inherits a tag (e.g. [ROLL]) from the message body.
   */
  extractSources(message) {
    const sources = [message.cleanContent ?? message.content ?? ''];
    if (this.config.tts.readEmbeds) {
      for (const e of message.embeds ?? []) {
        const text = [e.title, e.description].filter(Boolean).join('\n');
        if (text) sources.push(text);
      }
    }
    return sources.filter(Boolean);
  }

  /** @param {import('discord.js').Message} message */
  async handle(message) {
    const { discord, tts } = this.config;
    if (!tts.enabled) return;
    if (message.guildId !== discord.guildId || message.channelId !== discord.gmOutputChannelId) return;
    if (message.author?.id === this.client.user?.id) return; // never speak our own messages
    if (message.system) return;
    if (discord.gmAllowedAuthorIds.length && !discord.gmAllowedAuthorIds.includes(message.author.id)) {
      this.log.debug(`Ignoring GM output from non-allowed author ${message.author.id}`);
      return;
    }
    if (!this.session.isConnected) {
      this.log.debug('GM message received but bot is not in a voice channel; not speaking it');
      return;
    }
    const { chunks, truncated, split, parts, totalChars, droppedChars } = prepareSpeechDetailed(this.extractSources(message), {
      chunkMaxChars: tts.chunkMaxChars,
      maxMessageChars: tts.maxMessageChars,
      maxTotalChars: tts.maxTotalChars,
    });
    if (!chunks.length) return;
    if (this.sessionCap?.isReached()) {
      this.sessionCap.block(); // posts the one-time notice; no synthesis, no spend
      this.log.debug(`Voice session cap reached; not speaking GM message ${message.id}`);
      return;
    }
    const authorKey = message.author?.id ?? 'unknown';
    const speakable = chunks.map((c) => c.text).join(' ');
    const dup = this.dedupe?.check(authorKey, speakable);
    if (dup?.duplicate) {
      this.log.info(`Dropped duplicate GM message ${message.id} (${dup.kind}, same author ${dup.ageSeconds}s after the first; not spoken)`);
      this.events?.record('duplicate_dropped', { kind: dup.kind, age_s: dup.ageSeconds, chars: speakable.length });
      return;
    }
    if (split) this.log.info(`GM message ${message.id} is ${totalChars} chars (over TTS_MAX_MESSAGE_CHARS ${tts.maxMessageChars}): split into ${parts} parts, speaking all in order`);
    if (truncated) this.log.warn(`GM message ${message.id} exceeded TTS_MAX_TOTAL_CHARS (${tts.maxTotalChars}); truncated (${droppedChars} chars not spoken)`);
    const voices = [...new Set(chunks.map((c) => c.voice))].join('+');
    this.log.info(`Speaking GM message from ${message.author.tag ?? message.author.id} (${chunks.length} chunk(s), voice: ${voices})`);
    const groupId = this.queue.enqueue(chunks, { label: `msg:${message.id}` });
    if (groupId) this.dedupe?.remember(authorKey, speakable);
  }
}
