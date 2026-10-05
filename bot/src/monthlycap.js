/**
 * Monthly Fish minutes, shared by all campaign sessions: each session has its own SHARE (default 100 min) and everything counts
 * against one TOTAL (FISH_MONTHLY_CAP_MINUTES, default 200). Usage comes from the same tts-usage.jsonl the reports read
 * (records without dcc_session count as "alpha"), so a restart or a session switch loses nothing.
 */
import { readFileSync } from 'node:fs';
import { DEFAULT_CHARS_PER_MINUTE, localDate, monthMinutesBySession, parseJsonl } from './usage.js';

export class MonthlyShare {
  /**
   * @param {object} o
   * @param {string} o.logPath
   * @param {() => string} o.getSession      active campaign session id
   * @param {() => number} o.getShare        this session's share of the month (0 = no per-session share)
   * @param {() => number} o.getTotalCap     shared monthly total (0 = no total cap)
   */
  constructor({ logPath, getSession, getShare, getTotalCap, provider = 'fish', charsPerMinute = DEFAULT_CHARS_PER_MINUTE, ttlMs = 5000, now = () => new Date(), logger }) {
    Object.assign(this, { logPath, getSession, getShare, getTotalCap, provider, charsPerMinute, ttlMs, now });
    this.log = logger;
    this.cache = null;
  }

  _usage() {
    const t = Date.now();
    const month = localDate(this.now()).slice(0, 7);
    if (this.cache && this.cache.month === month && t - this.cache.at < this.ttlMs) return this.cache.by;
    let by = new Map();
    try {
      by = monthMinutesBySession(parseJsonl(readFileSync(this.logPath, 'utf8')).records, { month, provider: this.provider, charsPerMinute: this.charsPerMinute });
    } catch {
      /* no log yet */
    }
    this.cache = { at: t, month, by };
    return by;
  }

  /** Forget the cached figures (after a session switch). */
  invalidate() {
    this.cache = null;
  }

  status() {
    const by = this._usage();
    const session = this.getSession();
    const share = this.getShare();
    const totalCap = this.getTotalCap();
    const usedSession = by.get(session) ?? 0;
    const usedTotal = [...by.values()].reduce((a, b) => a + b, 0);
    let reason = null;
    if (share > 0 && usedSession >= share) reason = 'share';
    else if (totalCap > 0 && usedTotal >= totalCap) reason = 'total';
    return { month: this.cache.month, session, usedSession, share, usedTotal, totalCap, reached: reason !== null, reason };
  }

  isReached() {
    return this.status().reached;
  }
}
