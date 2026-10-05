/**
 * Hard per-session cap on spoken TTS minutes (a "session" = from /join until /leave or restart).
 *
 * Minutes are the same figures src/usage.js logs (measured audio when known, else chars / charsPerMinute).
 * Estimates are *reserved* when a chunk starts synthesizing and replaced by the real figure when it is
 * recorded, so prefetched chunks count immediately. Once `used >= cap`, `isReached()` is true and the
 * metered synthesizer refuses to call the TTS provider (no spend). cap <= 0 disables the cap (still counts).
 */
export const SESSION_WARN_PERCENT = 80;

export class SessionVoiceCap {
  /**
   * @param {object} o
   * @param {number} o.capMinutes
   * @param {{info:Function,warn:Function}} [o.logger]
   * @param {(status: object) => void} [o.onWarn]     called once per session when usage first reaches 80%
   * @param {(status: object) => void} [o.onReached]  called once per session on the first refused synthesis
   */
  constructor({ capMinutes = 50, logger, onWarn, onReached } = {}) {
    this.capMinutes = Math.max(0, Number(capMinutes) || 0);
    this.log = logger;
    this.onWarn = onWarn;
    this.onReached = onReached;
    this.external = null; // optional monthly-share check: () => { reached, reason, ... } (src/monthlycap.js)
    this.reset();
  }

  /** Also refuse synthesis while an outside limit (the monthly Fish share / shared total) is reached. */
  setExternalLimit(fn) {
    this.external = typeof fn === 'function' ? fn : null;
  }

  /** Start a fresh session: zero the counter and re-arm the one-shot warning and notice. */
  reset() {
    this.settled = 0;
    this.reserved = 0;
    this.warned = false;
    this.notified = false;
    this.startedAt = new Date();
  }

  /** Change the cap mid-session (0 = disabled). Re-arms the one-shot warning and notice. */
  setCap(minutes) {
    this.capMinutes = Math.max(0, Number(minutes) || 0);
    this.warned = false;
    this.notified = false;
  }

  get enabled() {
    return this.capMinutes > 0;
  }

  get used() {
    return this.settled + this.reserved;
  }

  /** Why synthesis is refused: 'session' (this /join's cap), 'share' / 'total' (monthly Fish minutes), or null. */
  reason() {
    if (this.enabled && this.used >= this.capMinutes) return 'session';
    try {
      return this.external?.()?.reason ?? null;
    } catch {
      return null; // a broken monthly check must never silence the bot
    }
  }

  isReached() {
    return this.reason() !== null;
  }

  reserve(minutes) {
    this.reserved += minutes;
    this._checkWarn();
  }

  /** Replace a reservation with the real figure (0 when the synthesis failed). */
  settle(reservedMinutes, actualMinutes) {
    this.reserved = Math.max(0, this.reserved - reservedMinutes);
    this.settled += actualMinutes;
    this._checkWarn();
  }

  /** A synthesis/speech attempt was refused because the cap is reached; fires `onReached` once per session. */
  block() {
    if (this.notified) return;
    this.notified = true;
    const st = { ...this.status(), reason: this.reason() ?? 'session' };
    this.log?.warn(
      st.reason === 'session'
        ? `Voice session cap reached (${fmt(st.used)}/${fmt(st.cap)} min): TTS disabled until /leave + /join or /voicecap`
        : `Monthly Fish minutes reached (${st.reason}): TTS disabled until next month, a bigger share, or /session use`
    );
    this._fire(this.onReached, st);
  }

  status() {
    const used = this.used;
    const cap = this.capMinutes;
    return {
      used,
      cap,
      enabled: this.enabled,
      percent: this.enabled ? (used / cap) * 100 : null,
      remaining: this.enabled ? Math.max(0, cap - used) : null,
      reached: this.isReached(),
      reason: this.reason(),
      warned: this.warned,
      since: this.startedAt,
    };
  }

  _checkWarn() {
    if (this.warned || !this.enabled || this.used < (this.capMinutes * SESSION_WARN_PERCENT) / 100) return;
    this.warned = true;
    const st = this.status();
    this.log?.warn(`Voice session usage at ${Math.round(st.percent)}% of cap (${fmt(st.used)}/${fmt(st.cap)} min)`);
    this._fire(this.onWarn, st);
  }

  _fire(fn, st) {
    try {
      Promise.resolve(fn?.(st)).catch((err) => this.log?.warn(`Voice cap notice failed: ${err?.message ?? err}`));
    } catch (err) {
      this.log?.warn(`Voice cap notice failed: ${err?.message ?? err}`);
    }
  }
}

export function fmt(n) {
  return (Math.round(n * 10) / 10).toFixed(1);
}
