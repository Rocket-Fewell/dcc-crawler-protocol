/**
 * Local table hook. Spoken lines go to the table process instead of waking an agent GM.
 *
 * OFF unless DCC_TABLE_URL is set. Only http(s) to localhost, 127.0.0.1, or [::1], with no
 * username or password in the URL. POST {text} to {origin}/api/line. Lines with speak true and
 * voice SYSTEM, GM, or NPC are handed to onSay. [ROLL] stays on the page and is not spoken.
 * Failures never throw and never log the line text.
 */

const LOCAL_HOSTS = new Set(['localhost', '127.0.0.1', '::1']);

function str(env, key) {
  const v = env[key];
  return v === undefined || v === null ? '' : String(v).trim();
}

function localHost(hostname) {
  return LOCAL_HOSTS.has(String(hostname || '').replace(/^\[|\]$/g, '').toLowerCase());
}

/** Table URL. Enabled only for a localhost http(s) origin. A bad value is a problem, not a silent fallback. */
export function loadTableConfig(env = process.env) {
  const raw = str(env, 'DCC_TABLE_URL');
  if (!raw) return { enabled: false, url: '', problems: [] };
  try {
    const u = new URL(raw);
    if (!['http:', 'https:'].includes(u.protocol)) {
      return { enabled: false, url: '', problems: ['DCC_TABLE_URL must be http or https'] };
    }
    if (u.username || u.password) {
      return { enabled: false, url: '', problems: ['DCC_TABLE_URL must not include a username or password'] };
    }
    if (!localHost(u.hostname)) {
      return { enabled: false, url: '', problems: ['DCC_TABLE_URL must point at localhost'] };
    }
    return { enabled: true, url: u.origin, problems: [] };
  } catch {
    return { enabled: false, url: '', problems: ['DCC_TABLE_URL is not a valid http(s) URL'] };
  }
}

/** Keep lines the mouth is allowed to say. Rolls and anything not marked speak stay out. */
export function speakable(say) {
  if (!Array.isArray(say)) return [];
  return say.filter((item) => {
    if (!item || item.speak !== true) return false;
    if (item.voice !== 'SYSTEM' && item.voice !== 'GM' && item.voice !== 'NPC') return false;
    return typeof item.text === 'string' && item.text.trim() !== '';
  });
}

/**
 * POST one transcript line. Never throws. `error` is a short code, never the line and never the URL.
 * Redirects are not followed.
 */
export async function postLine(url, text, { timeoutMs = 8000, fetchImpl = fetch } = {}) {
  const endpoint = new URL('/api/line', url.endsWith('/') ? url : `${url}/`);
  let res;
  try {
    res = await fetchImpl(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'User-Agent': 'discord-voice-bridge-table/1' },
      body: JSON.stringify({ text: String(text).slice(0, 7000) }),
      redirect: 'manual',
      signal: AbortSignal.timeout(timeoutMs),
    });
  } catch (err) {
    const code = err?.cause?.code ?? err?.code ?? err?.name ?? 'error';
    return { ok: false, status: null, say: [], error: String(code).slice(0, 40) };
  }
  if (res.status < 200 || res.status >= 300) {
    res.body?.cancel?.().catch(() => {});
    return { ok: false, status: res.status, say: [], error: null };
  }
  try {
    const data = await res.json();
    return { ok: true, status: res.status, say: Array.isArray(data?.say) ? data.say : [], error: null };
  } catch {
    return { ok: false, status: res.status, say: [], error: 'bad-json' };
  }
}

/**
 * Send a transcript line to the table when the hook is on; otherwise leave it for the wake webhook.
 * @param {object} line
 * @param {{ tableHook: { enabled: boolean, notify: Function }, wake: { notify: Function } }} route
 */
export function routeTranscript(line, { tableHook, wake }) {
  if (tableHook.enabled) tableHook.notify(line);
  else wake.notify(line);
}

export class TableHook {
  /**
   * @param {object} o
   * @param {{ enabled: boolean, url: string }} o.table  live config object (session swaps update it in place)
   * @param {{ info: Function, error: Function }} o.logger
   * @param {(lines: { voice: string, speak: boolean, text: string }[]) => Promise<void> | void} [o.onSay]
   * @param {typeof fetch} [o.fetchImpl]
   * @param {number} [o.timeoutMs]
   */
  constructor({ table, logger, onSay = () => {}, fetchImpl = fetch, timeoutMs = 8000 }) {
    this.table = table;
    this.log = logger;
    this.onSay = onSay;
    this.fetchImpl = fetchImpl;
    this.timeoutMs = timeoutMs;
    this.queue = [];
    this.draining = false;
    this._idle = Promise.resolve();
  }

  get enabled() {
    return Boolean(this.table?.enabled && this.table?.url);
  }

  /** Queue one transcript line. Resolves when this line and anything already queued have been posted. Never rejects. */
  notify(line) {
    if (!this.enabled) return Promise.resolve();
    const text = typeof line === 'string' ? line : line?.text;
    if (text === undefined || text === null || String(text).trim() === '') return Promise.resolve();
    this.queue.push(String(text));
    return this._drain();
  }

  _drain() {
    if (this.draining) return this._idle;
    this.draining = true;
    this._idle = this._run()
      .catch((err) => {
        const code = err?.code ?? err?.name ?? 'error';
        this.log.error(`table hook drain failed: ${String(code).slice(0, 40)}`);
      })
      .finally(() => {
        this.draining = false;
        if (this.queue.length) return this._drain();
      });
    return this._idle;
  }

  async _run() {
    while (this.queue.length && this.enabled) {
      const text = this.queue.shift();
      const result = await postLine(this.table.url, text, { timeoutMs: this.timeoutMs, fetchImpl: this.fetchImpl });
      if (!result.ok) {
        const why = result.status ? `HTTP ${result.status}` : String(result.error || 'error');
        this.log.error(`table hook failed: ${why}`);
        continue;
      }
      const lines = speakable(result.say);
      this.log.info(`table hook ok: HTTP ${result.status} (${lines.length} spoken)`);
      if (!lines.length) continue;
      try {
        await this.onSay(lines);
      } catch (err) {
        const code = err?.code ?? err?.name ?? 'error';
        this.log.error(`table hook speak failed: ${String(code).slice(0, 40)}`);
      }
    }
  }
}
