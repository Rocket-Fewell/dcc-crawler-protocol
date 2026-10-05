import { readFileSync, statSync, openSync, readSync, closeSync } from 'node:fs';

/**
 * Rolling-window wake budget (default 60 wake POSTs per hour; 0 disables). Each HTTP attempt of a wake counts
 * (successful or failed), but a rate-limited rejection does not. The history is seeded at startup from
 * logs/wake-usage.jsonl so a restart keeps the count.
 */
export const HOUR_MS = 3_600_000;

export class WakeBudget {
  constructor({ max = 60, windowMs = HOUR_MS, now = () => Date.now() } = {}) {
    this.max = Math.max(0, Number(max) || 0);
    this.windowMs = windowMs;
    this.now = now;
    this.stamps = []; // ascending timestamps (ms), one per counted POST
  }

  get enabled() {
    return this.max > 0;
  }

  _prune(t = this.now()) {
    const cutoff = t - this.windowMs;
    let i = 0;
    while (i < this.stamps.length && this.stamps[i] <= cutoff) i++;
    if (i) this.stamps.splice(0, i);
  }

  /** Count `n` POSTs made at `at`. */
  record(n = 1, at = this.now()) {
    for (let i = 0; i < Math.min(n, 1000); i++) this.stamps.push(at);
    this.stamps.sort((a, b) => a - b);
    this._prune();
  }

  used(t = this.now()) {
    this._prune(t);
    return this.stamps.length;
  }

  isExhausted(t = this.now()) {
    return this.enabled && this.used(t) >= this.max;
  }

  /** Earliest time (ms) a wake may be sent: `t` when there is room, else when enough old POSTs leave the window. */
  nextSlotAt(t = this.now()) {
    if (!this.enabled) return t;
    const used = this.used(t);
    if (used < this.max) return t;
    return this.stamps[used - this.max] + this.windowMs; // the (used-max+1)-th oldest must expire
  }

  status(t = this.now()) {
    const used = this.used(t);
    return { enabled: this.enabled, used, max: this.max, exhausted: this.isExhausted(t), resumeAt: this.isExhausted(t) ? this.nextSlotAt(t) : null };
  }
}

/**
 * POSTs a wake-log record used up. Skipped records and rate-limited rejections use none. Records written before
 * the budget existed have no `attempts`; their 400/429 responses were the platform's rate-limit rejections
 * (which did not start a run), so they are not counted either.
 */
export function postsUsed(r) {
  if (!r || r.skipped === true || r.rate_limited === true) return 0;
  if (typeof r.attempts === 'number') return Math.max(0, Math.floor(r.attempts));
  if (r.ok === false && (r.status === 400 || r.status === 429)) return 0;
  return 1;
}

/** Read the tail of a JSONL file (bounded) as text; '' when missing/unreadable. */
function readTail(file, maxBytes = 2 * 1024 * 1024) {
  try {
    const size = statSync(file).size;
    if (size <= maxBytes) return readFileSync(file, 'utf8');
    const fd = openSync(file, 'r');
    try {
      const buf = Buffer.alloc(maxBytes);
      readSync(fd, buf, 0, maxBytes, size - maxBytes);
      const text = buf.toString('utf8');
      return text.slice(text.indexOf('\n') + 1); // drop the partial first line
    } finally {
      closeSync(fd);
    }
  } catch {
    return '';
  }
}

/**
 * Recover the in-window wake count (and any still-running rate-limit backoff) from the wake usage log.
 * Skipped records are not wakes. Rate-limited rejections are not counted but start a backoff.
 * @returns {{ stamps: number[], rateLimitedUntil: number }}
 */
export function loadWakeHistory(file, { now = Date.now(), windowMs = HOUR_MS, backoffMs = 300_000, dccSession = 'alpha' } = {}) {
  const stamps = [];
  let rateLimitedUntil = 0;
  for (const line of readTail(file).split('\n')) {
    if (!line.trim()) continue;
    let r;
    try {
      r = JSON.parse(line);
    } catch {
      continue;
    }
    if (!r || typeof r !== 'object' || r.skipped === true) continue;
    if ((r.dcc_session ?? 'alpha') !== dccSession) continue; // each campaign session has its own hourly budget
    const t = Date.parse(r.ts);
    if (Number.isNaN(t)) continue;
    if (r.rate_limited === true) {
      rateLimitedUntil = Math.max(rateLimitedUntil, t + backoffMs);
      continue;
    }
    if (t > now - windowMs && t <= now + 60_000) {
      for (let i = 0; i < Math.min(postsUsed(r), 1000); i++) stamps.push(t);
    }
  }
  stamps.sort((a, b) => a - b);
  return { stamps, rateLimitedUntil: rateLimitedUntil > now ? rateLimitedUntil : 0 };
}

export function formatClock(ms) {
  return new Date(ms).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', hour12: false });
}
