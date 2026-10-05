/**
 * fetch with timeout and a small retry on 429 / 5xx / network errors.
 * `makeInit` is a function so FormData bodies are rebuilt for each attempt.
 */
export async function fetchWithRetry(url, makeInit, { retries = 2, timeoutMs = 45000, label = 'request' } = {}) {
  let lastErr;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const res = await fetch(url, { ...makeInit(), signal: AbortSignal.timeout(timeoutMs) });
      if (res.ok) return res;
      const body = await res.text().catch(() => '');
      const err = new Error(`${label} failed: HTTP ${res.status} ${body.slice(0, 300)}`);
      err.status = res.status;
      if (res.status !== 429 && res.status < 500) throw err; // not retryable
      lastErr = err;
    } catch (err) {
      if (err.status && err.status !== 429 && err.status < 500) throw err;
      lastErr = err;
    }
    if (attempt < retries) await new Promise((r) => setTimeout(r, 500 * 2 ** attempt));
  }
  throw lastErr;
}
