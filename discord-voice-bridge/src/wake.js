/**
 * GM wake notifier: when new player speech lands in the transcript channel, POST a small JSON webhook
 * so the (sleeping) AI GM agent can wake up and reply.
 *
 * Behaviour
 *  - OFF unless GM_WEBHOOK_URL is set (see loadWakeConfig in config.js).
 *  - Debounce: wait `debounceMs` after the LAST line (batching lines), but never longer than `maxWaitMs`
 *    after the FIRST pending line.
 *  - One POST in flight at a time; at most one wake per `minIntervalMs` (lines arriving meanwhile are
 *    carried into the next wake).
 *  - Don't wake while the GM's TTS is speaking: when a wake is due and `isBusy()` is true, wait until the
 *    speech queue is idle, for at most `idleMaxWaitMs` extra.
 *  - Failures never throw: one retry on network error / HTTP 5xx, then the batch is dropped (the GM re-reads
 *    the channel anyway). Logs contain status codes only - never the URL, the key or the transcript.
 */

import { formatClock } from './wakebudget.js';

const MAX_HELD_LINES = 1000;

export const DEFAULT_HINT = 'Run: python3 tools/discord_gm.py new  then reply with: python3 tools/discord_gm.py say ...';

/** Build the webhook request (url + headers) from config without ever logging it. */
export function buildRequest(wake) {
  const headers = { 'Content-Type': 'application/json', 'User-Agent': 'discord-voice-bridge-wake/1' };
  let url = wake.url;
  if (wake.key) {
    if (wake.keyInQuery) {
      const u = new URL(url);
      u.searchParams.set(wake.keyInQuery, wake.key);
      url = u.toString();
    } else {
      headers[wake.authHeader] = wake.authScheme ? `${wake.authScheme} ${wake.key}` : wake.key;
    }
  }
  return { url, headers };
}

export function buildPayload(lines, { channel = 'dcc_ears', hint = DEFAULT_HINT, extra = {} } = {}) {
  return { event: 'player_speech', channel, lines, hint, ...extra };
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/**
 * POST one payload, retrying once on network error / 5xx.
 * Never throws. Resolves { ok, status, error, attempts, rateLimited } where `error` is a short code (never a message that could
 * contain the URL).
 */
export async function postWake(wake, payload, { timeoutMs = 10_000, retryDelayMs = 500, retries = 1 } = {}) {
  let last = { ok: false, status: null, error: 'unknown', attempts: 0, rateLimited: false };
  for (let attempt = 0; attempt <= retries; attempt++) {
    last.attempts = attempt + 1;
    try {
      const { url, headers } = buildRequest(wake);
      const res = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload),
        redirect: 'manual', // never follow a redirect with credentials attached
        signal: AbortSignal.timeout(timeoutMs),
      });
      const ok = res.status >= 200 && res.status < 300;
      // A 400/429 whose body says "rate limit" is a rate limit, not a bad request: the caller backs off and keeps the lines.
      // The body is only inspected for that phrase; it is never stored or logged.
      let rateLimited = res.status === 429;
      if (res.status === 400 || res.status === 429) {
        try {
          rateLimited = rateLimited || /rate[\s_-]?limit/i.test((await res.text()).slice(0, 4096));
        } catch {
          /* unreadable body: treat as a plain 400 */
        }
      } else {
        res.body?.cancel().catch(() => {});
      }
      last = { ok, status: res.status, error: null, attempts: attempt + 1, rateLimited };
      if (ok || res.status < 500) return last; // success, or a 3xx/4xx that retrying won't fix
    } catch (err) {
      const code = err?.cause?.code ?? err?.code ?? err?.name ?? 'error';
      last = { ok: false, status: null, error: String(code).slice(0, 40), attempts: attempt + 1, rateLimited: false };
    }
    if (attempt < retries) await sleep(retryDelayMs);
  }
  return last;
}

export class GmWakeNotifier {
  /**
   * @param {object} o
   * @param {ReturnType<import('./config.js').loadWakeConfig>} o.wake
   * @param {() => boolean} [o.isBusy]   true while the GM's TTS is queued/speaking
   * @param {{debug:Function,info:Function,warn:Function,error:Function}} o.logger
   * @param {object} [o.budget]  rolling-hour WakeBudget: when exhausted lines are HELD, not dropped
   * @param {Function} [o.onBlocked]  notice hook for the first budget / rate-limit hold of an episode
   * @param {Function} [o.filter]  spotlight filter; lines it rejects never enter a batch (fail open on any error)
   * @param {{ record: Function }} [o.usageLog]  per-wake JSONL counter
   * @param {{ retryDelayMs?: number, pollMs?: number, timeoutMs?: number }} [o.timing]  (tests)
   */
  constructor({ wake, isBusy = () => false, logger, timing = {}, usageLog = null, filter = null, isPaused = () => false, budget = null, onBlocked = null }) {
    this.budget = budget; // optional WakeBudget (rolling hour)
    this.onBlocked = onBlocked; // ({ reason: 'budget'|'rate_limit', resumeAt }) once per hold episode
    this.rateLimitedUntil = 0;
    this.heldMarked = 0; // pending lines already logged as skipped/'budget'
    this.blockedNotified = false;
    this.budgetWarned = false;
    this.isPaused = isPaused; // /gm pause: lines are still posted to the channel, but no wake POST is made
    this.filter = filter; // optional (line) => { wake, reason, override } - the spotlight filter
    this.pendingOverrides = 0; // wake-word lines from non-spotlight players in the pending batch
    this.wake = wake;
    this.usageLog = usageLog; // optional WakeUsageLogger: one JSONL line per wake
    this.isBusy = isBusy;
    this.log = logger;
    this.timing = { retryDelayMs: 500, pollMs: 250, timeoutMs: 10_000, ...timing };
    this.pending = [];
    this.firstAt = 0; // when the oldest pending line arrived
    this.lastAt = 0; // when the newest pending line arrived
    this.lastSentAt = -Infinity;
    this.busySince = null;
    this.inFlight = false;
    this.timer = null;
    this.stopped = false;
    this.channel = 'dcc_ears';
  }

  get enabled() {
    return Boolean(this.wake?.enabled);
  }

  /** Call for every transcript line posted to the transcript channel. Never throws. */
  notify({ speaker, text, ts = new Date().toISOString(), channel, names }) {
    if (!this.enabled || this.stopped) return;
    try {
      if (this.isPaused()) {
        this._skipped('paused', 1);
        return;
      }
      let override = false;
      if (this.filter) {
        let d = null;
        try {
          d = this.filter({ speaker, text, names });
        } catch {
          d = null; // fail open
        }
        if (d && d.wake === false) {
          this.log.debug('GM wake: line skipped by spotlight filter');
          this._skipped(d.reason ?? 'spotlight', 1);
          return;
        }
        override = Boolean(d?.override);
        if (override) this.log.info('GM wake: wake word from a non-spotlight player; waking the GM');
      }
      if (override) this.pendingOverrides++;
      const now = Date.now();
      if (!this.pending.length) this.firstAt = now;
      this.lastAt = now;
      if (channel) this.channel = channel;
      this.pending.push({ speaker, text, ts });
      this._schedule();
    } catch (err) {
      this.log.warn(`GM wake: could not queue line (${err?.name ?? 'error'})`);
    }
  }

  _skipped(reason, count) {
    try {
      for (let i = 0; i < count; i++) this.usageLog?.recordSkipped?.({ reason });
    } catch {
      /* counting must never break the bot */
    }
  }

  /** Forget everything pending/held and any backoff (a different campaign session was activated). Does not stop the notifier. */
  reset() {
    clearTimeout(this.timer);
    this.timer = null;
    this.pending = [];
    this.pendingOverrides = 0;
    this.heldMarked = 0;
    this.blockedNotified = false;
    this.budgetWarned = false;
    this.rateLimitedUntil = 0;
    this.busySince = null;
  }

  stop() {
    this.stopped = true;
    clearTimeout(this.timer);
    this.timer = null;
    this.pending = [];
    this.pendingOverrides = 0;
  }

  _setTimer(ms) {
    clearTimeout(this.timer);
    this.timer = setTimeout(() => this._tick(), Math.max(1, Math.ceil(ms)));
    this.timer.unref?.();
  }

  _schedule() {
    if (this.inFlight || this.stopped || !this.pending.length) return; // finishing a POST re-schedules
    if (this.isPaused()) {
      // Paused while lines were waiting: drop them (they remain in the channel) and count them as skipped.
      this.log.info(`GM wake paused: dropping ${this.pending.length} pending line(s)`);
      this._skipped('paused', this.pending.length);
      this.pending = [];
      this.pendingOverrides = 0;
      clearTimeout(this.timer);
      this.timer = null;
      return;
    }
    const { debounceMs, maxWaitMs, minIntervalMs, idleMaxWaitMs } = this.wake;
    const now = Date.now();
    let dueAt = Math.max(Math.min(this.lastAt + debounceMs, this.firstAt + maxWaitMs), this.lastSentAt + minIntervalMs);
    // Rolling-hour budget / rate-limit backoff: HOLD the lines (never drop them) until sending is allowed again.
    const budgetAt = this.budget?.enabled ? this.budget.nextSlotAt(now) : now;
    const gateAt = Math.max(budgetAt, this.rateLimitedUntil);
    if (gateAt > now) {
      this._hold(budgetAt > now && budgetAt >= this.rateLimitedUntil ? 'budget' : 'rate_limit', gateAt);
      dueAt = Math.max(dueAt, gateAt);
    }
    if (now < dueAt) return this._setTimer(dueAt - now);
    // Due. Hold off while the GM is still talking, but only for idleMaxWaitMs.
    if (this.isBusy()) {
      this.busySince ??= now;
      const left = idleMaxWaitMs - (now - this.busySince);
      if (left > 0) return this._setTimer(Math.min(this.timing.pollMs, left));
      this.log.debug('GM wake: TTS still busy after max extra wait; waking anyway');
    }
    this._send();
  }

  /** Lines are being held because the budget is exhausted / the server rate-limited us. */
  _hold(reason, resumeAt) {
    if (this.pending.length > MAX_HELD_LINES) {
      const extra = this.pending.length - MAX_HELD_LINES;
      this.pending.splice(0, extra); // memory guard only; the lines remain in the channel
      this.heldMarked = Math.max(0, this.heldMarked - extra);
      this.log.warn(`GM wake: holding more than ${MAX_HELD_LINES} lines; the oldest ${extra} were not kept for the batch`);
    }
    if (reason === 'budget' && this.pending.length > this.heldMarked) {
      this._skipped('budget', this.pending.length - this.heldMarked); // counted once per held line; they are sent later
      this.heldMarked = this.pending.length;
    }
    if (!this.blockedNotified) {
      this.blockedNotified = true;
      this.log.warn(
        reason === 'budget'
          ? `GM wake budget reached (${this.budget.used()}/${this.budget.max} in the last hour): holding ${this.pending.length} line(s) until ${formatClock(resumeAt)}`
          : `GM wake rate limited: holding ${this.pending.length} line(s) until ${formatClock(resumeAt)}`
      );
      try {
        Promise.resolve(this.onBlocked?.({ reason, resumeAt })).catch((err) => this.log.warn(`Wake notice failed: ${err?.message ?? err}`));
      } catch (err) {
        this.log.warn(`Wake notice failed: ${err?.message ?? err}`);
      }
    }
  }

  /** Warn once when the rolling count reaches 80% of the budget (re-armed when it falls below). */
  _checkBudgetWarn() {
    if (!this.budget?.enabled) return;
    const used = this.budget.used();
    const threshold = this.budget.max * 0.8;
    if (used < threshold) this.budgetWarned = false;
    else if (!this.budgetWarned) {
      this.budgetWarned = true;
      this.log.warn(`GM wake budget at ${Math.round((used / this.budget.max) * 100)}% (${used}/${this.budget.max} wakes in the last hour)`);
    }
  }

  /** For /gm status. */
  status() {
    const now = Date.now();
    const b = this.budget?.enabled ? this.budget.status(now) : { enabled: false, used: 0, max: 0, exhausted: false, resumeAt: null };
    return { budget: b, held: this.pending.length, rateLimitedUntil: this.rateLimitedUntil > now ? this.rateLimitedUntil : null, inFlight: this.inFlight };
  }

  _tick() {
    this.timer = null;
    this._schedule();
  }

  async _send() {
    const lines = this.pending;
    const overrides = this.pendingOverrides;
    const batchFirstAt = this.firstAt;
    this.pending = [];
    this.pendingOverrides = 0;
    this.heldMarked = 0;
    this.busySince = null;
    this.inFlight = true;
    this.lastSentAt = Date.now();
    try {
      const payload = buildPayload(lines, { channel: this.channel, hint: this.wake.hint });
      const r = await postWake(this.wake, payload, this.timing);
      try {
        this.usageLog?.record({ lines: lines.length, ok: r.ok, status: r.status, overrides, attempts: r.attempts, rateLimited: r.rateLimited });
      } catch {
        /* counting must never break the bot */
      }
      // A rate-limited rejection is not a run, so it does not use up the budget.
      this.budget?.record(r.rateLimited ? 0 : (r.attempts ?? 1));
      this._checkBudgetWarn();
      if (r.rateLimited) {
        // Keep the lines: put them back in front of anything that arrived meanwhile and retry after the backoff.
        this.pending = lines.concat(this.pending);
        this.pendingOverrides += overrides;
        this.firstAt = batchFirstAt;
        this.rateLimitedUntil = Date.now() + this.wake.rateLimitBackoffMs;
        this.log.warn(`GM wake rate limited (HTTP ${r.status}): backing off ${Math.round(this.wake.rateLimitBackoffMs / 60000)} min, holding ${this.pending.length} line(s)`);
      } else {
        this.blockedNotified = false; // a wake went out: the next hold is a new episode
        this.rateLimitedUntil = 0;
      }
      if (r.rateLimited) {
        /* logged above */
      } else if (r.ok) this.log.info(`GM wake sent: HTTP ${r.status} (${lines.length} line${lines.length === 1 ? '' : 's'})`);
      else if (r.status) this.log.warn(`GM wake failed: HTTP ${r.status} (${lines.length} line(s) dropped)`);
      else this.log.warn(`GM wake failed: network error ${r.error} (${lines.length} line(s) dropped)`);
    } catch (err) {
      this.log.warn(`GM wake failed: ${err?.name ?? 'error'}`); // never include err.message (could contain the URL)
    } finally {
      this.inFlight = false;
      this._schedule(); // carry forward anything that arrived while the POST was in flight
    }
  }
}
