import { EndBehaviorType } from '@discordjs/voice';
import { escapeMarkdown } from 'discord.js';
import prism from 'prism-media';
import { DECODE_CHANNELS, DECODE_RATE, STT_RATE, downsample, pcmDurationMs, pcmRms, pcmToWav } from './audio.js';
import { fetchWithRetry } from './http.js';
import { isHallucination } from './text.js';

/** Transcribe a WAV buffer with the OpenAI audio transcriptions API. Returns trimmed text ('' if none). */
export async function transcribeWav(wav, { openai, stt }) {
  const res = await fetchWithRetry(
    `${openai.baseUrl}/audio/transcriptions`,
    () => {
      const form = new FormData();
      form.append('file', new Blob([wav], { type: 'audio/wav' }), 'speech.wav');
      form.append('model', stt.model);
      form.append('response_format', 'json'); // the only format gpt-4o-transcribe supports besides text
      form.append('temperature', '0');
      if (stt.language) form.append('language', stt.language);
      if (stt.prompt) form.append('prompt', stt.prompt);
      return { method: 'POST', headers: { Authorization: `Bearer ${openai.apiKey}` }, body: form };
    },
    { label: 'OpenAI transcription' }
  );
  const json = await res.json();
  return (json.text ?? '').trim();
}

/** Tiny async semaphore. */
class Limiter {
  constructor(max) {
    this.max = max;
    this.active = 0;
    this.waiters = [];
  }
  async run(fn) {
    if (this.active >= this.max) await new Promise((r) => this.waiters.push(r));
    this.active++;
    try {
      return await fn();
    } finally {
      this.active--;
      this.waiters.shift()?.();
    }
  }
}

const IDENTITY_TTL_MS = 5 * 60_000;

/**
 * Speech-to-text bridge: per-user Opus receive streams -> PCM -> WAV -> Whisper -> transcript channel.
 */
export class SttBridge {
  constructor({ client, config, logger, transcribe = transcribeWav, onTranscript = null }) {
    this.client = client;
    this.config = config;
    this.log = logger;
    this.transcribe = transcribe;
    this.onTranscript = onTranscript; // called after each transcript line is posted ({ speaker, text, ts, channel })
    this.limiter = new Limiter(config.stt.concurrency);
    this.active = new Map(); // userId -> { opus, decoder }
    this.identities = new Map(); // userId -> { name, bot, at }
    this.chain = Promise.resolve(); // keeps transcript posts in utterance order
    this.connection = null;
    this.onSpeakingStart = null;
  }

  attach(connection) {
    this.detach();
    if (!this.config.stt.enabled) return;
    this.connection = connection;
    this.onSpeakingStart = (userId) => this._onSpeakingStart(userId);
    connection.receiver.speaking.on('start', this.onSpeakingStart);
    this.log.info('STT listening for speakers');
  }

  detach() {
    if (this.connection && this.onSpeakingStart) {
      this.connection.receiver.speaking.off('start', this.onSpeakingStart);
    }
    for (const { opus, decoder } of this.active.values()) {
      opus.destroy();
      decoder.destroy();
    }
    this.active.clear();
    this.connection = null;
    this.onSpeakingStart = null;
  }

  async _identity(userId) {
    const cached = this.identities.get(userId);
    if (cached && Date.now() - cached.at < IDENTITY_TTL_MS) return cached;
    const guild = this.client.guilds.cache.get(this.config.discord.guildId);
    let result = null;
    try {
      const member = guild?.members.cache.get(userId) ?? (await guild?.members.fetch(userId));
      if (member) result = { name: member.displayName, username: member.user.username, bot: member.user.bot, at: Date.now() };
    } catch {
      /* not in guild any more; fall through */
    }
    if (!result) {
      try {
        const user = await this.client.users.fetch(userId);
        result = { name: user.displayName ?? user.username, username: user.username, bot: user.bot, at: Date.now() };
      } catch {
        result = { name: `User ${userId}`, bot: false, at: Date.now() };
      }
    }
    this.identities.set(userId, result);
    return result;
  }

  _onSpeakingStart(userId) {
    if (userId === this.client.user?.id) return; // never transcribe ourselves
    if (this.active.has(userId)) return;
    const cached = this.identities.get(userId);
    if (cached?.bot) return; // never transcribe other bots
    const knownBot = this.client.users.cache.get(userId)?.bot;
    if (knownBot) return;
    this._capture(userId);
  }

  _capture(userId) {
    if (!this.connection) return;
    const { stt } = this.config;
    // Start identity lookup right away (in parallel with capture) so we don't delay subscribing.
    const identityPromise = this._identity(userId);

    const opus = this.connection.receiver.subscribe(userId, {
      end: { behavior: EndBehaviorType.AfterSilence, duration: stt.silenceMs },
    });
    const decoder = new prism.opus.Decoder({ rate: DECODE_RATE, channels: DECODE_CHANNELS, frameSize: 960 });
    this.active.set(userId, { opus, decoder });

    const chunks = [];
    let bytes = 0;
    let finished = false;
    const finish = (reason, { resume = false } = {}) => {
      if (finished) return;
      finished = true;
      if (this.active.get(userId)?.opus === opus) this.active.delete(userId);
      opus.destroy();
      decoder.destroy();
      const pcm = Buffer.concat(chunks);
      this._process(userId, pcm, identityPromise, reason);
      if (resume) this._capture(userId);
    };

    decoder.on('data', (chunk) => {
      chunks.push(chunk);
      bytes += chunk.length;
      if ((bytes / 2 / DECODE_RATE) * 1000 >= stt.maxDurationMs) finish('max-duration', { resume: true });
    });
    decoder.on('end', () => finish('silence'));
    // Corrupt/undecryptable packets happen (esp. around DAVE transitions); keep what we have.
    opus.on('error', (err) => {
      this.log.debug(`Opus stream error for ${userId}: ${err.message}`);
      finish('stream-error');
    });
    decoder.on('error', (err) => {
      this.log.debug(`Opus decode error for ${userId}: ${err.message}`);
      finish('decode-error');
    });
    opus.pipe(decoder);
  }

  _process(userId, pcm, identityPromise, reason) {
    const { stt } = this.config;
    const durationMs = pcmDurationMs(pcm);
    if (durationMs < stt.minDurationMs) {
      this.log.debug(`Skip ${userId}: too short (${Math.round(durationMs)}ms, ${reason})`);
      return;
    }
    const rms = pcmRms(pcm);
    if (rms < stt.minRms) {
      this.log.debug(`Skip ${userId}: too quiet (rms ${Math.round(rms)})`);
      return;
    }
    const wav = pcmToWav(downsample(pcm, DECODE_RATE / STT_RATE), STT_RATE, 1);
    this.log.debug(`Transcribing ${userId}: ${Math.round(durationMs)}ms, rms ${Math.round(rms)}, ${wav.length} bytes`);

    const started = this.limiter
      .run(() => this.transcribe(wav, this.config))
      .catch((err) => {
        this.log.error(`Transcription failed for ${userId}: ${err.message}`);
        return '';
      });

    // Post strictly in utterance order even though requests run in parallel.
    this.chain = this.chain
      .then(async () => {
        const [raw, identity] = await Promise.all([started, identityPromise]);
        const text = (raw ?? '').replace(/\s+/g, ' ').trim();
        if (identity.bot) return; // bots are never transcribed
        if (isHallucination(text)) {
          if (text) this.log.debug(`Filtered likely hallucination: "${text}"`);
          return;
        }
        await this._post(identity.name, text, { username: identity.username });
      })
      .catch((err) => this.log.error(`Transcript pipeline error: ${err.message}`));
  }

  async _post(name, text, extra = {}) {
    const channel = await this.client.channels.fetch(this.config.discord.transcriptChannelId);
    if (!channel?.isTextBased()) throw new Error('TRANSCRIPT_CHANNEL_ID is not a text channel');
    const body = text.length > 1800 ? `${text.slice(0, 1797)}...` : text;
    const content = `**${escapeMarkdown(name)}**: "${body}"`;
    await channel.send({ content, allowedMentions: { parse: [] } });
    this.log.info(`Transcript: ${content}`);
    try {
      this.onTranscript?.({ speaker: name, names: extra.username ? [extra.username] : [], text: body, ts: new Date().toISOString(), channel: channel.name });
    } catch (err) {
      this.log.warn(`Transcript hook failed: ${err?.name ?? 'error'}`);
    }
  }
}
