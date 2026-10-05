/**
 * Fish Audio prepaid credit: live balance and the low-balance staff warning.
 *
 * Fish bills prepaid API credit at $15 per 1M UTF-8 bytes of text (see usage.js, `utf8_bytes` per synthesized message; bytes only, never the text).
 * GET {base}/wallet/self/api-credit with `Authorization: Bearer $FISH_API_KEY` answers { credit: "12.34", ... } (dollars as a STRING).
 * The key is never logged or printed; error text is scrubbed of it.
 */
export const DEFAULT_LOW_BALANCE_USD = 3;
/** FISH_LOW_BALANCE_USD -> dollars; unset, empty, non-numeric or negative falls back to the default 3. */
export function lowBalanceThreshold(raw) {
  if (raw === undefined || raw === null || String(raw).trim() === '') return DEFAULT_LOW_BALANCE_USD;
  const n = Number(raw);
  return Number.isFinite(n) && n >= 0 ? n : DEFAULT_LOW_BALANCE_USD;
}
export const DEFAULT_CHECK_INTERVAL_MS = 30 * 60_000;

const scrub = (text, key) => (key ? String(text).split(key).join('***') : String(text));

/** -> number of dollars. Throws a scrubbed Error on HTTP/parse problems. */
export async function fetchFishBalance({ apiKey, baseUrl = 'https://api.fish.audio', fetchImpl = fetch, timeoutMs = 15_000 } = {}) {
  if (!apiKey) throw new Error('FISH_API_KEY is not set');
  let res;
  try {
    res = await fetchImpl(`${String(baseUrl).replace(/\/+$/, '')}/wallet/self/api-credit`, {
      headers: { Authorization: `Bearer ${apiKey}` },
      signal: AbortSignal.timeout(timeoutMs),
    });
  } catch (err) {
    throw new Error(scrub(`balance request failed: ${err.message}`, apiKey));
  }
  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(scrub(`balance request failed: HTTP ${res.status} ${body.slice(0, 200)}`, apiKey));
  }
  const data = await res.json().catch(() => null);
  const n = Number(data?.credit);
  if (data?.credit === undefined || data?.credit === null || data?.credit === '' || !Number.isFinite(n)) throw new Error('balance response had no numeric `credit` field');
  return n;
}

/**
 * Checks the balance at start, every ~30 min and on demand (after a session closes). Under the threshold it warns ONCE (to the log and, if a
 * staff channel is configured, there); it warns again only after the balance has recovered above the threshold. Never speaks.
 */
export class FishBalanceMonitor {
  constructor({ getBalance, threshold = DEFAULT_LOW_BALANCE_USD, intervalMs = DEFAULT_CHECK_INTERVAL_MS, logger = console, notify = null, setIntervalImpl = setInterval, clearIntervalImpl = clearInterval } = {}) {
    Object.assign(this, { getBalance, threshold, intervalMs, logger, notify, setIntervalImpl, clearIntervalImpl });
    this.warned = false;
    this.last = null;
    this.timer = null;
    this.checking = null;
  }

  start() {
    this.check('startup').catch(() => {});
    this.timer = this.setIntervalImpl(() => this.check('interval').catch(() => {}), this.intervalMs);
    this.timer?.unref?.();
  }

  stop() {
    if (this.timer) this.clearIntervalImpl(this.timer);
    this.timer = null;
  }

  /** -> balance in dollars, or null when it could not be read (logged at warn level; never throws). */
  async check(reason = 'manual') {
    if (this.checking) return this.checking;   // one request at a time
    this.checking = this.#run(reason).finally(() => { this.checking = null; });
    return this.checking;
  }

  async #run(reason) {
    let credit;
    try {
      credit = await this.getBalance();
    } catch (err) {
      this.logger.warn?.(`Fish balance check (${reason}) failed: ${err.message}`);
      return null;
    }
    this.last = credit;
    if (credit >= this.threshold) {
      this.warned = false;
      this.logger.info?.(`Fish balance: $${credit.toFixed(2)} (${reason})`);
      return credit;
    }
    if (!this.warned) {
      this.warned = true;
      const msg = `Fish Audio credit is low: $${credit.toFixed(2)} left (warning under $${this.threshold.toFixed(2)}). Top up at fish.audio or the GM voice will stop.`;
      this.logger.warn?.(msg);
      try {
        await this.notify?.(msg);
      } catch (err) {
        this.logger.warn?.(`Fish balance staff note failed: ${err.message}`);
      }
    }
    return credit;
  }
}
