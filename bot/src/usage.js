import { appendFileSync, mkdirSync } from 'node:fs';
import { randomBytes } from 'node:crypto';
import { dirname } from 'node:path';

/**
 * TTS usage accounting: one JSON line per synthesized chunk (JSONL), plus a pure summarizer used by
 * scripts/tts-usage-summary.js. No secrets are ever written here - only counts.
 *
 * Record fields:
 *   ts           ISO-8601 UTC timestamp
 *   date, month  local calendar date (YYYY-MM-DD) / month (YYYY-MM) of the record
 *   session      id of the bot process run that produced it
 *   provider     openai | elevenlabs | fish
 *   voice        gm | system   (the tag contract's voice)
 *   model        provider model name
 *   chars        characters sent to the TTS provider (JS string length)
 *   utf8_bytes   UTF-8 bytes sent (Fish Audio bills per UTF-8 byte)
 *   minutes      audio minutes used: actual audio duration when known, else chars / charsPerMinute
 *   minutes_source  "audio" | "estimate"
 *   audio_seconds   measured/derived audio duration, or null
 *   ok           false when synthesis failed (excluded from totals)
 */

export const DEFAULT_CHARS_PER_MINUTE = 900;
export const DEFAULT_MONTHLY_CAP_MINUTES = 200;
export const WARN_PERCENT = 80;
// `session` in these logs is the bot-process run id; `dcc_session` is the CAMPAIGN session ("alpha", "beta"). Old records have no
// dcc_session and count as alpha.
export const DEFAULT_DCC_SESSION = 'alpha';
export const dccSessionOf = (r) => r?.dcc_session ?? DEFAULT_DCC_SESSION;

function pad(n) {
  return String(n).padStart(2, '0');
}
export function localDate(d = new Date()) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

export function newSessionId(now = new Date()) {
  return `${now.toISOString().replace(/[-:]/g, '').slice(0, 15)}-${randomBytes(2).toString('hex')}`;
}

export function estimateMinutes(chars, charsPerMinute = DEFAULT_CHARS_PER_MINUTE) {
  return chars / charsPerMinute;
}

export class UsageLogger {
  /**
   * @param {{ path: string, enabled?: boolean, session?: string, charsPerMinute?: number, logger?: any }} o
   */
  constructor({ path, enabled = true, session = newSessionId(), charsPerMinute = DEFAULT_CHARS_PER_MINUTE, dccSession = DEFAULT_DCC_SESSION, logger }) {
    Object.assign(this, { path, enabled, session, charsPerMinute, dccSession });
    this.log = logger;
    this.warned = false;
  }

  /** Append one usage record. Never throws (accounting must not break speech). */
  record({ provider, voice, model = '', text, audioSeconds = null, ok = true, now = new Date() }) {
    if (!this.enabled) return null;
    const chars = [...text].length;
    const entry = {
      ts: now.toISOString(),
      date: localDate(now),
      month: localDate(now).slice(0, 7),
      session: this.session,
      dcc_session: this.dccSession,
      provider,
      voice,
      model,
      chars,
      utf8_bytes: Buffer.byteLength(text, 'utf8'),
      minutes: round(audioSeconds != null ? audioSeconds / 60 : estimateMinutes(chars, this.charsPerMinute)),
      minutes_source: audioSeconds != null ? 'audio' : 'estimate',
      audio_seconds: audioSeconds != null ? round(audioSeconds, 2) : null,
      ok,
    };
    try {
      mkdirSync(dirname(this.path), { recursive: true });
      appendFileSync(this.path, `${JSON.stringify(entry)}\n`, 'utf8');
    } catch (err) {
      if (!this.warned) {
        this.warned = true;
        this.log?.warn(`Could not write TTS usage log ${this.path}: ${err.message}`);
      }
    }
    return entry;
  }
}

function round(n, places = 4) {
  const f = 10 ** places;
  return Math.round(n * f) / f;
}

/**
 * Wrap a TTS provider's synthesize() so every call is metered. The provider may return a Buffer, or a
 * stream with a `usage` promise ({ ok, audioSeconds }) that settles when the stream finishes.
 */
export function meteredSynthesize(provider, usage, sessionCap = null) {
  return async (text, voice) => {
    // Hard session cap: refuse BEFORE calling the provider so nothing is spent once the cap is reached.
    if (sessionCap?.isReached()) {
      sessionCap.block();
      throw new SessionCapError();
    }
    const model = provider.modelFor?.(voice) ?? '';
    // Reserve the estimated minutes now so prefetched chunks count before their audio finishes streaming.
    const est = estimateMinutes([...text].length, usage.charsPerMinute);
    sessionCap?.reserve(est);
    // Same minutes figure the usage log writes (measured audio when known, else the chars estimate).
    const rec = (args) => {
      const entry = usage.record(args);
      sessionCap?.settle(est, args.ok === false ? 0 : (entry?.minutes ?? est));
      return entry;
    };
    let audio;
    try {
      audio = await provider.synthesize(text, voice);
    } catch (err) {
      rec({ provider: provider.id, voice, model, text, ok: false });
      throw err;
    }
    const base = { provider: provider.id, voice, model, text };
    if (audio && typeof audio.pipe === 'function' && audio.usage) {
      audio.usage.then(
        (u) => rec({ ...base, audioSeconds: u.audioSeconds ?? null, ok: u.ok !== false }),
        () => rec({ ...base, ok: false })
      );
    } else {
      rec({ ...base, audioSeconds: provider.audioSeconds?.(audio) ?? null });
    }
    return audio;
  };
}

/** Thrown by the metered synthesizer when the per-session voice cap is reached (nothing was synthesized). */
export class SessionCapError extends Error {
  constructor() {
    super('session voice cap reached');
    this.name = 'SessionCapError';
    this.code = 'SESSION_CAP';
  }
}

// ---------------------------------------------------------------------------- wake-up log

/**
 * One JSONL line per GM wake webhook (logs/wake-usage.jsonl): { ts, date, session, lines, ok, status }.
 * Never contains the URL, key or transcript text.
 */
export class WakeUsageLogger {
  constructor({ path, enabled = true, session = newSessionId(), dccSession = DEFAULT_DCC_SESSION, logger }) {
    Object.assign(this, { path, enabled, session, dccSession });
    this.log = logger;
    this.warned = false;
  }

  record({ lines, ok = true, status = null, overrides = 0, attempts = 1, rateLimited = false, now = new Date() }) {
    if (!this.enabled) return null;
    const entry = { ts: now.toISOString(), date: localDate(now), session: this.session, dcc_session: this.dccSession, lines, ok, status, overrides, attempts };
    if (rateLimited) entry.rate_limited = true; // a rate-limit rejection: lines are kept and retried, not counted against the budget
    return this._append(entry);
  }

  /** A transcript line that did NOT trigger a wake because of the spotlight filter (no names/text are stored). */
  recordSkipped({ reason = 'spotlight', now = new Date() } = {}) {
    if (!this.enabled) return null;
    const entry = { ts: now.toISOString(), date: localDate(now), session: this.session, dcc_session: this.dccSession, skipped: true, speaker_matched: false, reason, lines: 1 };
    return this._append(entry);
  }

  _append(entry) {
    try {
      mkdirSync(dirname(this.path), { recursive: true });
      appendFileSync(this.path, `${JSON.stringify(entry)}\n`, 'utf8');
    } catch (err) {
      if (!this.warned) {
        this.warned = true;
        this.log?.warn(`Could not write wake usage log: ${err.code ?? err.name}`);
      }
    }
    return entry;
  }
}

export function parseWakeJsonl(text) {
  const records = [];
  let bad = 0;
  for (const line of text.split('\n')) {
    if (!line.trim()) continue;
    try {
      const r = JSON.parse(line);
      if (r && typeof r === 'object' && typeof r.ts === 'string' && typeof r.lines === 'number') records.push(r);
      else bad++;
    } catch {
      bad++;
    }
  }
  return { records, bad };
}

/**
 * Wake-up counts per day and per bot session (grouped by date). `month` limits to YYYY-MM.
 * Spotlight records ({skipped:true}) are counted separately: skipped lines, and wake-word overrides carried by
 * wake records; wakes the server rejected as rate-limited (`rate_limited`) and lines held by the rolling-hour budget (`budget_held`) are separate; lines dropped while `/gm pause` was active are counted as `paused`. `saved_upper_bound` = skipped + paused lines: each could have cost up to one wake, but batching would have
 * merged some of them, so this is an UPPER bound on wake-ups saved.
 */
export function summarizeWakes(records, { month, dccSession } = {}) {
  const days = new Map();
  const campaigns = new Map();
  const sessions = new Map();
  const fresh = () => ({ wakes: 0, failed: 0, lines: 0, skipped: 0, paused: 0, budget_held: 0, rate_limited: 0, attempts: 0, overrides: 0, saved_upper_bound: 0 });
  const total = fresh();
  const apply = (b, r) => {
    if (r.skipped === true) {
      if (r.reason === 'budget') {
        b.budget_held += r.lines; // held until the rolling-hour budget frees up, then sent: NOT a saving
        return;
      }
      if (r.reason === 'paused') b.paused += r.lines; // /gm pause
      else b.skipped += r.lines; // spotlight filter
      b.saved_upper_bound += r.lines;
      return;
    }
    b.attempts += typeof r.attempts === 'number' ? r.attempts : 1;
    if (r.rate_limited === true) {
      // The server refused the run (rate limit): lines were kept and retried. Not a wake that ran.
      b.rate_limited += 1;
      return;
    }
    b.wakes += 1;
    b.lines += r.lines;
    b.overrides += typeof r.overrides === 'number' ? r.overrides : 0;
    if (r.ok === false) b.failed += 1;
  };
  const bucketFor = (map, k) => map.get(k) ?? map.set(k, fresh()).get(k);
  for (const r of records) {
    const d = r.date ?? localDate(new Date(r.ts));
    if (month && d.slice(0, 7) !== month) continue;
    if (dccSession && dccSessionOf(r) !== dccSession) continue;
    apply(bucketFor(days, d), r);
    apply(bucketFor(sessions, `${r.session ?? 'unknown'}|${d}`), r);
    apply(bucketFor(campaigns, dccSessionOf(r)), r);
    apply(total, r);
  }
  const sorted = (m) => [...m.entries()].sort(([a], [b]) => a.localeCompare(b));
  return {
    total,
    by_day: sorted(days).map(([date, b]) => ({ date, ...b })),
    by_session: sorted(sessions).map(([k, b]) => {
      const [session, date] = k.split('|');
      return { session, date, ...b };
    }),
    by_campaign: sorted(campaigns).map(([dcc_session, b]) => ({ dcc_session, ...b })),
  };
}
// ---------------------------------------------------------------------------- voice events log

/**
 * One JSONL line per voice-side protective action (logs/voice-events.jsonl):
 *   duplicate_dropped {kind, age_s, chars} | backlog_dropped {messages, chunks} | flush {source, chunks}
 * Never stores message text.
 */
export class VoiceEventLogger {
  constructor({ path, enabled = true, session = newSessionId(), dccSession = DEFAULT_DCC_SESSION, logger }) {
    Object.assign(this, { path, enabled, session, dccSession });
    this.log = logger;
    this.warned = false;
  }

  record(type, fields = {}, now = new Date()) {
    if (!this.enabled) return null;
    const entry = { ts: now.toISOString(), date: localDate(now), session: this.session, dcc_session: this.dccSession, type, ...fields };
    try {
      mkdirSync(dirname(this.path), { recursive: true });
      appendFileSync(this.path, `${JSON.stringify(entry)}\n`, 'utf8');
    } catch (err) {
      if (!this.warned) {
        this.warned = true;
        this.log?.warn(`Could not write voice events log: ${err.code ?? err.name}`);
      }
    }
    return entry;
  }
}

export function parseEventsJsonl(text) {
  const records = [];
  let bad = 0;
  for (const line of text.split('\n')) {
    if (!line.trim()) continue;
    try {
      const r = JSON.parse(line);
      if (r && typeof r === 'object' && typeof r.ts === 'string' && typeof r.type === 'string') records.push(r);
      else bad++;
    } catch {
      bad++;
    }
  }
  return { records, bad };
}

/** Per day and per bot session: duplicate GM messages dropped, backlog drops (messages/chunks), flushes. */
export function summarizeVoiceEvents(records, { month } = {}) {
  const fresh = () => ({ duplicates: 0, backlog_events: 0, backlog_messages: 0, backlog_chunks: 0, flushes: 0 });
  const days = new Map();
  const sessions = new Map();
  const total = fresh();
  const apply = (b, r) => {
    if (r.type === 'duplicate_dropped') b.duplicates += 1;
    else if (r.type === 'backlog_dropped') {
      b.backlog_events += 1;
      b.backlog_messages += r.messages ?? 0;
      b.backlog_chunks += r.chunks ?? 0;
    } else if (r.type === 'flush') b.flushes += 1;
  };
  const bucketFor = (map, k) => map.get(k) ?? map.set(k, fresh()).get(k);
  for (const r of records) {
    const d = r.date ?? localDate(new Date(r.ts));
    if (month && d.slice(0, 7) !== month) continue;
    apply(bucketFor(days, d), r);
    apply(bucketFor(sessions, `${r.session ?? 'unknown'}|${d}`), r);
    apply(total, r);
  }
  const sorted = (m) => [...m.entries()].sort(([a], [b]) => a.localeCompare(b));
  return {
    total,
    by_day: sorted(days).map(([date, b]) => ({ date, ...b })),
    by_session: sorted(sessions).map(([k, b]) => {
      const [session, date] = k.split('|');
      return { session, date, ...b };
    }),
  };
}

// ---------------------------------------------------------------------------- reading + summarizing

export function parseJsonl(text) {
  const records = [];
  let bad = 0;
  for (const line of text.split('\n')) {
    if (!line.trim()) continue;
    try {
      const r = JSON.parse(line);
      if (r && typeof r === 'object' && typeof r.chars === 'number') records.push(r);
      else bad++;
    } catch {
      bad++;
    }
  }
  return { records, bad };
}

function dateOf(r) {
  return r.date ?? (r.ts ? localDate(new Date(r.ts)) : 'unknown');
}

function minutesOf(r, charsPerMinute) {
  return typeof r.minutes === 'number' ? r.minutes : estimateMinutes(r.chars, charsPerMinute);
}

function costUsd(r, pricePerMillionBytes) {
  if (r.provider !== 'fish' || /free/i.test(r.model ?? '')) return 0;
  return ((r.utf8_bytes ?? Buffer.byteLength('x'.repeat(r.chars))) / 1e6) * pricePerMillionBytes;
}

function bucket() {
  return { records: 0, chars: 0, utf8_bytes: 0, minutes: 0, est_cost_usd: 0 };
}

function add(b, r, charsPerMinute, price) {
  b.records += 1;
  b.chars += r.chars;
  b.utf8_bytes += r.utf8_bytes ?? r.chars;
  b.minutes += minutesOf(r, charsPerMinute);
  b.est_cost_usd += costUsd(r, price);
}

function finish(b) {
  return { ...b, minutes: round(b.minutes, 2), est_cost_usd: round(b.est_cost_usd, 4) };
}

/**
 * Summarize usage records.
 * @param {object[]} records
 * @param {{ month?: string, provider?: string, cap?: number, capProvider?: string, charsPerMinute?: number,
 *           fishPricePerMillionBytes?: number, now?: Date }} [opts]
 *   month         limit the tables to YYYY-MM; also the month the cap is checked for (default: current month)
 *   capProvider   provider the cap applies to ("fish" by default, "all" for every provider)
 */
export function summarize(records, opts = {}) {
  const {
    month,
    provider,
    cap = DEFAULT_MONTHLY_CAP_MINUTES,
    capProvider = 'fish',
    charsPerMinute = DEFAULT_CHARS_PER_MINUTE,
    fishPricePerMillionBytes = 15,
    now = new Date(),
    dccSession,
    shares = {},
    defaultShare = 0,
  } = opts;
  const ok = records.filter((r) => r.ok !== false);
  const failed = records.length - ok.length;
  const scoped = ok.filter((r) => (!provider || r.provider === provider) && (!month || (r.month ?? dateOf(r).slice(0, 7)) === month) && (!dccSession || dccSessionOf(r) === dccSession));

  const days = new Map();
  const months = new Map();
  const sessions = new Map();
  const voices = new Map();
  const total = bucket();
  for (const r of scoped) {
    const d = dateOf(r);
    const key = (map, k) => map.get(k) ?? map.set(k, bucket()).get(k);
    const dayB = key(days, `${d}|${r.provider}`);
    const monthB = key(months, `${d.slice(0, 7)}|${r.provider}`);
    const sessB = key(sessions, `${r.session ?? 'unknown'}|${d}|${r.provider}`);
    const voiceB = key(voices, `${r.provider}|${r.voice ?? '?'}`);
    for (const b of [dayB, monthB, sessB, voiceB]) add(b, r, charsPerMinute, fishPricePerMillionBytes);
    add(total, r, charsPerMinute, fishPricePerMillionBytes);
  }
  const rows = (map, split) =>
    [...map.entries()]
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([k, b]) => ({ ...split(k.split('|')), ...finish(b) }));

  const capMonth = month ?? localDate(now).slice(0, 7);
  let used = 0;
  for (const r of ok) {
    if ((r.month ?? dateOf(r).slice(0, 7)) !== capMonth) continue;
    if (capProvider !== 'all' && r.provider !== capProvider) continue;
    used += minutesOf(r, charsPerMinute);
  }
  const percent = cap > 0 ? (used / cap) * 100 : Infinity;
  // Per campaign session: this month's minutes against that session's share of the shared monthly cap.
  const perCampaign = new Map();
  for (const r of ok) {
    if ((r.month ?? dateOf(r).slice(0, 7)) !== capMonth) continue;
    if (capProvider !== 'all' && r.provider !== capProvider) continue;
    perCampaign.set(dccSessionOf(r), (perCampaign.get(dccSessionOf(r)) ?? 0) + minutesOf(r, charsPerMinute));
  }
  for (const id of Object.keys(shares)) if (!perCampaign.has(id)) perCampaign.set(id, 0);
  const campaigns = [...perCampaign.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([id, m]) => {
      const share = shares[id] ?? defaultShare;
      return { dcc_session: id, used_minutes: round(m, 2), share_minutes: share, remaining_minutes: share > 0 ? round(Math.max(0, share - m), 2) : null, percent: share > 0 ? round((m / share) * 100, 1) : null, over: share > 0 && m >= share };
    });
  return {
    records: scoped.length,
    failed_excluded: failed,
    total: finish(total),
    by_day: rows(days, ([date, provider]) => ({ date, provider })),
    by_month: rows(months, ([month, provider]) => ({ month, provider })),
    by_session: rows(sessions, ([session, date, provider]) => ({ session, date, provider })),
    by_voice: rows(voices, ([provider, voice]) => ({ provider, voice })),
    by_campaign: campaigns,
    cap: {
      month: capMonth,
      provider: capProvider,
      cap_minutes: cap,
      used_minutes: round(used, 2),
      remaining_minutes: round(Math.max(0, cap - used), 2),
      percent: Number.isFinite(percent) ? round(percent, 1) : null,
      warn: percent >= WARN_PERCENT,
      over: percent >= 100,
    },
  };
}

/**
 * Minutes spoken in `month` (YYYY-MM) per campaign session, from usage records. Failed syntheses are excluded.
 * Used by the monthly share enforcement (src/monthlycap.js).
 */
export function monthMinutesBySession(records, { month, provider = 'fish', charsPerMinute = DEFAULT_CHARS_PER_MINUTE } = {}) {
  const out = new Map();
  for (const r of records) {
    if (r.ok === false) continue;
    if ((r.month ?? dateOf(r).slice(0, 7)) !== month) continue;
    if (provider !== 'all' && r.provider !== provider) continue;
    out.set(dccSessionOf(r), (out.get(dccSessionOf(r)) ?? 0) + minutesOf(r, charsPerMinute));
  }
  return out;
}
