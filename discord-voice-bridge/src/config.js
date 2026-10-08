import 'dotenv/config';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { campaignDir, charactersDir, dataDir, DEFAULT_SESSION } from './session.js';

const PROJECT_ROOT = fileURLToPath(new URL('..', import.meta.url));

const DEFAULT_SYSTEM_INSTRUCTIONS =
  'Voice: dry, informative, corporate. Calm and even. Delivers timers, fees, registration, collapse warnings and floor notices with no jokes, no sarcasm, and no theatrical flair. Think a polite automated PA system reading policy.';

const SNOWFLAKE = /^\d{15,25}$/;

function str(env, key, def = '') {
  const v = env[key];
  return v === undefined || v === null || String(v).trim() === '' ? def : String(v).trim();
}

function bool(env, key, def) {
  const v = str(env, key, '');
  if (v === '') return def;
  return ['1', 'true', 'yes', 'on'].includes(v.toLowerCase());
}

function num(env, key, def, { min = -Infinity, max = Infinity } = {}) {
  const v = str(env, key, '');
  if (v === '') return def;
  const n = Number(v);
  if (!Number.isFinite(n)) throw new ConfigError([`${key} must be a number (got "${v}")`]);
  return Math.min(max, Math.max(min, n));
}

function list(env, key) {
  return str(env, key, '')
    .split(/[\s,]+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

/**
 * GM wake webhook settings. OFF unless GM_WEBHOOK_URL is set. Secrets (URL, key) are only ever held here
 * and used by src/wake.js - never log this object.
 */
export function loadWakeConfig(env = process.env) {
  const problems = [];
  let url = str(env, 'GM_WEBHOOK_URL');
  if (url) {
    try {
      const u = new URL(url);
      if (!['http:', 'https:'].includes(u.protocol)) throw new Error('protocol');
    } catch {
      problems.push('GM_WEBHOOK_URL is not a valid http(s) URL'); // never echo the value
      url = '';
    }
  }
  const headerName = str(env, 'GM_WEBHOOK_AUTH_HEADER', 'Authorization');
  // Scheme: unset -> "Bearer" for the Authorization header (raw key for any other header);
  // set but empty -> raw key; set -> "<scheme> <key>".
  const schemeSet = Object.hasOwn(env, 'GM_WEBHOOK_AUTH_SCHEME');
  const authScheme = schemeSet ? str(env, 'GM_WEBHOOK_AUTH_SCHEME') : headerName.toLowerCase() === 'authorization' ? 'Bearer' : '';
  const q = str(env, 'GM_WEBHOOK_KEY_IN_QUERY');
  const keyInQuery = ['', '0', 'false', 'no', 'off'].includes(q.toLowerCase()) ? '' : ['1', 'true', 'yes', 'on'].includes(q.toLowerCase()) ? 'key' : q;
  const debounceMs = num(env, 'GM_WAKE_DEBOUNCE_MS', 2500, { min: 0, max: 600_000 });
  const wake = {
    enabled: Boolean(url),
    url,
    key: str(env, 'GM_WEBHOOK_KEY'),
    authHeader: headerName,
    authScheme,
    keyInQuery,
    debounceMs,
    maxWaitMs: Math.max(debounceMs, num(env, 'GM_WAKE_MAX_WAIT_MS', 8000, { min: 0, max: 600_000 })),
    minIntervalMs: num(env, 'GM_WAKE_MIN_INTERVAL_MS', 4000, { min: 0, max: 600_000 }),
    idleMaxWaitMs: num(env, 'GM_WAKE_IDLE_MAX_WAIT_MS', 15_000, { min: 0, max: 600_000 }),
    // Rolling-hour budget of wake POSTs (the GM platform limits automation runs per hour). 0 = off.
    maxPerHour: Math.floor(num(env, 'WAKE_MAX_PER_HOUR', 60, { min: 0, max: 100_000 })),
    // After a "rate limit" response, hold lines and retry after this long.
    rateLimitBackoffMs: num(env, 'WAKE_RATE_LIMIT_BACKOFF_MS', 300_000, { min: 1000, max: 86_400_000 }),
    hint: str(env, 'GM_WEBHOOK_HINT', 'Run: python3 tools/discord_gm.py new  then reply with: python3 tools/discord_gm.py say ...'),
    problems,
  };
  if (wake.enabled && wake.keyInQuery && !wake.key) problems.push('GM_WEBHOOK_KEY_IN_QUERY is set but GM_WEBHOOK_KEY is empty');
  return wake;
}

export class ConfigError extends Error {
  constructor(problems) {
    super(`Invalid configuration:\n  - ${problems.join('\n  - ')}`);
    this.name = 'ConfigError';
    this.problems = problems;
  }
}

/**
 * Build and validate configuration from environment variables.
 * @param {NodeJS.ProcessEnv} env
 * @param {{ mode?: 'bot' | 'register' }} opts  `register` only needs the Discord app credentials.
 */
export function loadConfig(env = process.env, { mode = 'bot' } = {}) {
  const problems = [];
  const need = (key, { snowflake = false } = {}) => {
    const v = str(env, key);
    if (!v) problems.push(`${key} is required`);
    else if (snowflake && !SNOWFLAKE.test(v)) problems.push(`${key} must be a numeric Discord ID (got "${v}")`);
    return v;
  };

  const openaiGm = {
    model: str(env, 'OPENAI_TTS_MODEL', 'gpt-4o-mini-tts'),
    voice: str(env, 'OPENAI_TTS_VOICE', 'onyx'),
    instructions: str(env, 'OPENAI_TTS_INSTRUCTIONS', ''),
    speed: num(env, 'OPENAI_TTS_SPEED', 1.0, { min: 0.25, max: 4.0 }),
  };
  const elGm = {
    voiceId: str(env, 'ELEVENLABS_VOICE_ID'),
    modelId: str(env, 'ELEVENLABS_MODEL_ID', 'eleven_flash_v2_5'),
    stability: num(env, 'ELEVENLABS_STABILITY', 0.5, { min: 0, max: 1 }),
    similarity: num(env, 'ELEVENLABS_SIMILARITY', 0.75, { min: 0, max: 1 }),
  };

  const cfg = {
    discord: {
      token: mode === 'register' ? need('DISCORD_TOKEN') : need('DISCORD_TOKEN'),
      clientId: need('CLIENT_ID', { snowflake: true }),
      guildId: need('GUILD_ID', { snowflake: true }),
      voiceChannelId: str(env, 'VOICE_CHANNEL_ID'),
      transcriptChannelId: str(env, 'TRANSCRIPT_CHANNEL_ID'),
      gmOutputChannelId: str(env, 'GM_OUTPUT_CHANNEL_ID'),
      autoJoin: bool(env, 'AUTO_JOIN', false),
      gmAllowedAuthorIds: list(env, 'GM_ALLOWED_AUTHOR_IDS'),
    },
    openai: {
      apiKey: str(env, 'OPENAI_API_KEY'),
      baseUrl: str(env, 'OPENAI_BASE_URL', 'https://api.openai.com/v1').replace(/\/+$/, ''),
    },
    stt: {
      enabled: bool(env, 'STT_ENABLED', true),
      model: str(env, 'STT_MODEL', 'gpt-4o-transcribe'),
      language: str(env, 'STT_LANGUAGE', ''),
      prompt: str(env, 'STT_PROMPT', ''),
      silenceMs: num(env, 'STT_SILENCE_MS', 1000, { min: 200, max: 10000 }),
      minDurationMs: num(env, 'STT_MIN_DURATION_MS', 700, { min: 0 }),
      minRms: num(env, 'STT_MIN_RMS', 250, { min: 0 }),
      maxDurationMs: num(env, 'STT_MAX_DURATION_MS', 60000, { min: 2000 }),
      concurrency: num(env, 'STT_CONCURRENCY', 3, { min: 1, max: 10 }),
    },
    tts: {
      enabled: bool(env, 'TTS_ENABLED', true),
      provider: str(env, 'TTS_PROVIDER', 'openai').toLowerCase(),
      // Max characters per synthesized chunk (sentences are never merged beyond this).
      chunkMaxChars: num(env, 'TTS_CHUNK_MAX_CHARS', 600, { min: 40, max: 4000 }),
      // Part size: a GM message longer than this is split at sentence/paragraph boundaries and spoken as several parts
      // in order (Oct 7 2026; it used to be truncated here). Each chunk keeps its [GM]/[SYSTEM]/[NPC: Name] voice.
      maxMessageChars: num(env, 'TTS_MAX_MESSAGE_CHARS', 1500, { min: 100 }),
      // Safety ceiling on total spoken characters per GM message (runaway-cost guard); beyond it the rest is dropped and logged.
      // Never below TTS_MAX_MESSAGE_CHARS.
      maxTotalChars: Math.max(num(env, 'TTS_MAX_TOTAL_CHARS', 6000, { min: 100 }), num(env, 'TTS_MAX_MESSAGE_CHARS', 1500, { min: 100 })),
      readEmbeds: bool(env, 'TTS_READ_EMBEDS', true),
      prefetch: num(env, 'TTS_PREFETCH', 2, { min: 1, max: 6 }),
      fish: {
        apiKey: str(env, 'FISH_API_KEY'),
        baseUrl: str(env, 'FISH_BASE_URL', 'https://api.fish.audio').replace(/\/+$/, ''),
        model: str(env, 'FISH_MODEL', 's2.1-pro'),
        latency: str(env, 'FISH_LATENCY', 'balanced').toLowerCase(),
        format: str(env, 'FISH_FORMAT', 'mp3').toLowerCase(),
        mp3Bitrate: num(env, 'FISH_MP3_BITRATE', 128),
        speed: num(env, 'FISH_SPEED', 1.0, { min: 0.5, max: 2.0 }),
        // Voices are Fish "reference_id" model ids. If only one is set, it is used for both.
        voices: {
          gm: { voiceId: str(env, 'FISH_VOICE_ID_NARRATOR') || str(env, 'FISH_VOICE_ID_SYSTEM') },
          system: { voiceId: str(env, 'FISH_VOICE_ID_SYSTEM') || str(env, 'FISH_VOICE_ID_NARRATOR') },
        },
        voiceFallback: !(str(env, 'FISH_VOICE_ID_NARRATOR') && str(env, 'FISH_VOICE_ID_SYSTEM')),
      },
      openai: {
        // "gm" = narrator voice (untagged, [GM]); "system" = [SYSTEM] voice.
        voices: {
          gm: {
            model: openaiGm.model,
            voice: openaiGm.voice,
            instructions: openaiGm.instructions,
            speed: openaiGm.speed,
          },
          system: {
            model: str(env, 'OPENAI_TTS_SYSTEM_MODEL', openaiGm.model),
            voice: str(env, 'OPENAI_TTS_SYSTEM_VOICE', 'coral'),
            instructions: str(env, 'OPENAI_TTS_SYSTEM_INSTRUCTIONS', DEFAULT_SYSTEM_INSTRUCTIONS),
            speed: num(env, 'OPENAI_TTS_SYSTEM_SPEED', openaiGm.speed, { min: 0.25, max: 4.0 }),
          },
        },
      },
      elevenlabs: {
        apiKey: str(env, 'ELEVENLABS_API_KEY'),
        systemVoiceFallback: !str(env, 'ELEVENLABS_SYSTEM_VOICE_ID'),
        voices: {
          gm: elGm,
          system: {
            voiceId: str(env, 'ELEVENLABS_SYSTEM_VOICE_ID', elGm.voiceId), // falls back to the narrator voice
            modelId: str(env, 'ELEVENLABS_SYSTEM_MODEL_ID', elGm.modelId),
            stability: num(env, 'ELEVENLABS_SYSTEM_STABILITY', 0.35, { min: 0, max: 1 }),
            similarity: num(env, 'ELEVENLABS_SYSTEM_SIMILARITY', elGm.similarity, { min: 0, max: 1 }),
          },
        },
      },
    },
    usage: {
      enabled: bool(env, 'TTS_USAGE_LOG_ENABLED', true),
      path: str(env, 'TTS_USAGE_LOG', `${PROJECT_ROOT}logs/tts-usage.jsonl`),
      charsPerMinute: num(env, 'TTS_USAGE_CHARS_PER_MINUTE', 900, { min: 100, max: 5000 }),
      fishMonthlyCapMinutes: num(env, 'FISH_MONTHLY_CAP_MINUTES', 200, { min: 0 }), // shared by ALL campaign sessions
      // This campaign session's share of the monthly minutes (default 100 each; 0 = no per-session share, only the shared total).
      sessionMonthlyMinutes: num(env, 'FISH_SESSION_MONTHLY_MINUTES', 100, { min: 0 }),
      // Hard cap on spoken minutes per voice session (/join .. /leave or restart). 0 = disabled.
      sessionCapMinutes: num(env, 'FISH_SESSION_CAP_MINUTES', 50, { min: 0 }),
      // One JSONL line per GM wake webhook (only written when the wake feature is on).
      wakeLogEnabled: bool(env, 'WAKE_USAGE_LOG_ENABLED', true),
      wakeLogPath: str(env, 'WAKE_USAGE_LOG', `${PROJECT_ROOT}logs/wake-usage.jsonl`),
    },
    wake: loadWakeConfig(env),
    // /gm pause|resume: persisted runtime switch for the wake webhook.
    gmWakeStateFile: str(env, 'GM_WAKE_STATE_FILE', `${PROJECT_ROOT}logs/gm-wake-state.json`),
    // Voice-side protections.
    voice: {
      // Drop a GM message if the same author already had identical/near-identical text spoken or queued this recently (0 = off).
      duplicateWindowSeconds: num(env, 'DUPLICATE_WINDOW_SECONDS', 120, { min: 0, max: 86400 }),
      // Backlog safeguard: above either limit the OLDEST pending messages are dropped (0 = off).
      maxQueuedChunks: num(env, 'MAX_QUEUED_CHUNKS', 12, { min: 0, max: 1000 }),
      maxQueuedSeconds: num(env, 'MAX_QUEUED_SECONDS', 90, { min: 0, max: 36000 }),
      // File kill switch written by `discord_gm.py stop`.
      controlEnabled: bool(env, 'VOICE_CONTROL_ENABLED', true),
      controlFile: str(env, 'VOICE_CONTROL_FILE', join(campaignDir(env), 'sessions', 'voice-control.json')),
      controlPollMs: num(env, 'VOICE_CONTROL_POLL_MS', 500, { min: 100, max: 60000 }),
      eventsLogEnabled: bool(env, 'VOICE_EVENTS_LOG_ENABLED', true),
      eventsLogPath: str(env, 'VOICE_EVENTS_LOG', `${PROJECT_ROOT}logs/voice-events.jsonl`),
    },
    // Wake-up filter: while the GM runs a "spotlight" exchange only that player (or the wake word "AI") wakes it.
    spotlight: {
      enabled: bool(env, 'SPOTLIGHT_FILTER_ENABLED', true),
      file: str(env, 'SPOTLIGHT_FILE', join(campaignDir(env), 'sessions', 'spotlight.json')),
      maxAgeMinutes: num(env, 'SPOTLIGHT_MAX_AGE_MINUTES', 20, { min: 1, max: 1440 }),
    },
    // Which campaign session ("alpha" = the live game) this process is configured for; see src/session.js.
    campaign: {
      sessionId: str(env, 'DCC_SESSION_ID', DEFAULT_SESSION),
      dir: campaignDir(env),
      dataDir: dataDir(str(env, 'DCC_SESSION_ID', DEFAULT_SESSION), env),
      charactersDir: charactersDir(str(env, 'DCC_SESSION_ID', DEFAULT_SESSION), env),
    },
    // /create: silent Discord character creation (writes the character file, registers the crawler via tools/state.py).
    create: {
      enabled: bool(env, 'CREATE_ENABLED', true),
      python: str(env, 'PYTHON_BIN', 'python3'),
      publish: bool(env, 'CREATE_PUBLISH', true), // register the sheet channel + post the first card (needs GM_DISCORD_TOKEN in this process's env)
    },
    logLevel: str(env, 'LOG_LEVEL', 'info').toLowerCase(),
  };

  if (mode === 'bot') {
    for (const [key, val] of [
      ['VOICE_CHANNEL_ID', cfg.discord.voiceChannelId],
      ['TRANSCRIPT_CHANNEL_ID', cfg.discord.transcriptChannelId],
      ['GM_OUTPUT_CHANNEL_ID', cfg.discord.gmOutputChannelId],
    ]) {
      if (val && !SNOWFLAKE.test(val)) problems.push(`${key} must be a numeric Discord ID (got "${val}")`);
    }
    if (cfg.stt.enabled && !cfg.discord.transcriptChannelId) problems.push('TRANSCRIPT_CHANNEL_ID is required when STT_ENABLED=true');
    if (cfg.tts.enabled && !cfg.discord.gmOutputChannelId) problems.push('GM_OUTPUT_CHANNEL_ID is required when TTS_ENABLED=true');
    if (cfg.discord.autoJoin && !cfg.discord.voiceChannelId) problems.push('VOICE_CHANNEL_ID is required when AUTO_JOIN=true');
    if (cfg.stt.enabled && !cfg.openai.apiKey) problems.push('OPENAI_API_KEY is required when STT_ENABLED=true');

    if (cfg.tts.enabled) {
      if (!['openai', 'elevenlabs', 'fish'].includes(cfg.tts.provider)) {
        problems.push(`TTS_PROVIDER must be "openai", "elevenlabs" or "fish" (got "${cfg.tts.provider}")`);
      } else if (cfg.tts.provider === 'fish') {
        const f = cfg.tts.fish;
        if (!f.apiKey) problems.push('FISH_API_KEY is required when TTS_PROVIDER=fish');
        if (!f.voices.gm.voiceId) problems.push('FISH_VOICE_ID_NARRATOR and/or FISH_VOICE_ID_SYSTEM is required when TTS_PROVIDER=fish');
        for (const [k, id] of [['FISH_VOICE_ID_NARRATOR', f.voices.gm.voiceId], ['FISH_VOICE_ID_SYSTEM', f.voices.system.voiceId]]) {
          if (id && !/^[A-Za-z0-9_-]{6,128}$/.test(id)) problems.push(`${k} must be a Fish Audio model id (letters/digits, no spaces)`);
        }
        if (!['low', 'normal', 'balanced'].includes(f.latency)) problems.push('FISH_LATENCY must be low, balanced or normal');
        if (!['mp3', 'opus', 'wav'].includes(f.format)) problems.push('FISH_FORMAT must be mp3, opus or wav');
        if (![64, 128, 192].includes(f.mp3Bitrate)) problems.push('FISH_MP3_BITRATE must be 64, 128 or 192');
      } else if (cfg.tts.provider === 'openai' && !cfg.openai.apiKey) {
        problems.push('OPENAI_API_KEY is required when TTS_PROVIDER=openai');
      } else if (cfg.tts.provider === 'elevenlabs') {
        if (!cfg.tts.elevenlabs.apiKey) problems.push('ELEVENLABS_API_KEY is required when TTS_PROVIDER=elevenlabs');
        if (!cfg.tts.elevenlabs.voices.gm.voiceId) problems.push('ELEVENLABS_VOICE_ID is required when TTS_PROVIDER=elevenlabs');
      }
    }
  }

  if (problems.length) throw new ConfigError(problems);
  return cfg;
}
