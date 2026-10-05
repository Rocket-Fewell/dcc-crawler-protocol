import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { FishBalanceMonitor, fetchFishBalance, lowBalanceThreshold } from '../src/fishbalance.js';
import { balanceLine } from '../scripts/tts-usage-summary.js';

const KEY = 'sk-secret-key-123';
const reply = (body, status = 200) => async (url, init) => {
  reply.last = { url, init };
  return { ok: status < 300, status, json: async () => body, text: async () => JSON.stringify(body) };
};

test('fetchFishBalance: GET /wallet/self/api-credit with a Bearer key, `credit` is a dollar STRING', async () => {
  const f = reply({ credit: '12.34' });
  assert.equal(await fetchFishBalance({ apiKey: KEY, fetchImpl: f }), 12.34);
  assert.equal(reply.last.url, 'https://api.fish.audio/wallet/self/api-credit');
  assert.equal(reply.last.init.headers.Authorization, `Bearer ${KEY}`);
  await assert.rejects(fetchFishBalance({ apiKey: KEY, fetchImpl: reply({ nope: 1 }) }), /numeric `credit`/);
  await assert.rejects(fetchFishBalance({ apiKey: '', fetchImpl: f }), /FISH_API_KEY/);
});

test('errors never contain the key', async () => {
  const bad = async () => { throw new Error(`connect failed for ${KEY}`); };
  await assert.rejects(fetchFishBalance({ apiKey: KEY, fetchImpl: bad }), (e) => !e.message.includes(KEY) && e.message.includes('***'));
  const http = reply(`oops ${KEY}`, 401);
  await assert.rejects(fetchFishBalance({ apiKey: KEY, fetchImpl: http }), (e) => !e.message.includes(KEY) && /HTTP 401/.test(e.message));
});

const logs = () => { const l = { info: [], warn: [] }; return { l, logger: { info: (m) => l.info.push(m), warn: (m) => l.warn.push(m) } }; };

test('monitor: under $3 warns ONCE (log + staff note), again only after recovering; at or above $3 stays quiet; never throws', async () => {
  const { l, logger } = logs();
  const sent = [];
  let credit = 2.5;
  const m = new FishBalanceMonitor({ getBalance: async () => credit, logger, notify: async (t) => sent.push(t) });
  assert.equal(await m.check('startup'), 2.5);
  await m.check('interval');
  await m.check('session closed');
  assert.equal(sent.length, 1);
  assert.match(sent[0], /\$2\.50 left/);
  assert.doesNotMatch(sent[0], /\[SYSTEM\]/);                     // never in the GM-voice tag format, and never spoken
  assert.equal(l.warn.filter((x) => /credit is low/.test(x)).length, 1);
  credit = 3;                                                      // exactly $3 is fine
  await m.check();
  credit = 1;
  await m.check();
  assert.equal(sent.length, 2);                                    // re-armed after it recovered
});

test('monitor: no staff channel = log only; a failing balance request or notify is logged, never thrown', async () => {
  const { l, logger } = logs();
  const m = new FishBalanceMonitor({ getBalance: async () => 0.5, logger, notify: null });
  assert.equal(await m.check(), 0.5);
  assert.equal(l.warn.length, 1);
  const { l: l2, logger: lg2 } = logs();
  const m2 = new FishBalanceMonitor({ getBalance: async () => { throw new Error('HTTP 500'); }, logger: lg2 });
  assert.equal(await m2.check('startup'), null);
  assert.match(l2.warn[0], /failed: HTTP 500/);
  const { l: l3, logger: lg3 } = logs();
  const m3 = new FishBalanceMonitor({ getBalance: async () => 1, logger: lg3, notify: async () => { throw new Error('no perms'); } });
  assert.equal(await m3.check(), 1);
  assert.ok(l3.warn.some((x) => /staff note failed: no perms/.test(x)));
});

test('monitor: start() checks at once and every interval; stop() clears the timer', async () => {
  const { logger } = logs();
  let calls = 0;
  let tick;
  const m = new FishBalanceMonitor({ getBalance: async () => { calls++; return 10; }, logger, intervalMs: 1800000, setIntervalImpl: (fn, ms) => { tick = { fn, ms }; return { unref() {} }; }, clearIntervalImpl: () => { tick = null; } });
  m.start();
  await new Promise((r) => setImmediate(r));
  assert.equal(calls, 1);
  assert.equal(tick.ms, 30 * 60_000);
  tick.fn();
  await new Promise((r) => setImmediate(r));
  assert.equal(calls, 2);
  m.stop();
  assert.equal(tick, null);
});

test('npm run usage: balanceLine prints the live balance without the key; --no-balance skips the request; bytes cost is per day and session', async () => {
  const r = await balanceLine({ FISH_API_KEY: KEY }, reply({ credit: '7.5' }));
  assert.equal(r.line, 'Fish balance (live): $7.50 prepaid credit');
  assert.ok(!r.line.includes(KEY));
  assert.match((await balanceLine({}, reply({ credit: '1' }))).line, /not set/);
  const bad = await balanceLine({ FISH_API_KEY: KEY }, reply({}, 403));
  assert.ok(!bad.ok && !bad.line.includes(KEY));
  const d = mkdtempSync(join(tmpdir(), 'usage-'));
  try {
    const f = join(d, 'u.jsonl');
    writeFileSync(f, [{ ts: '2026-10-04T12:00:00Z', date: '2026-10-04', month: '2026-10', session: 's1', dcc_session: 'alpha', provider: 'fish', voice: 'gm', model: 's2.1-pro', chars: 1000000, utf8_bytes: 1000000, minutes: 5, ok: true }].map((x) => JSON.stringify(x)).join('\n'));
    const out = execFileSync('node', ['scripts/tts-usage-summary.js', '--file', f, '--wake-file', join(d, 'w'), '--events-file', join(d, 'e'), '--no-balance', '--json'], { env: { ...process.env, FISH_API_KEY: KEY }, encoding: 'utf8' });
    const j = JSON.parse(out);
    assert.equal(j.by_day[0].est_cost_usd, 15);                  // 1,000,000 bytes x $15 / 1M
    assert.equal(j.by_session[0].est_cost_usd, 15);
    assert.equal(j.fish_balance_usd, null);
    assert.ok(!out.includes(KEY));
    const txt = execFileSync('node', ['scripts/tts-usage-summary.js', '--file', f, '--wake-file', join(d, 'w'), '--events-file', join(d, 'e'), '--no-balance'], { env: { ...process.env, FISH_API_KEY: KEY }, encoding: 'utf8' });
    assert.match(txt, /\$15 per 1M UTF-8 bytes: Fish calls in this report cost \$15\.0000/);
    assert.match(txt, /bytes USD/);
  } finally { rmSync(d, { recursive: true, force: true }); }
});

test('FISH_LOW_BALANCE_USD: numbers are used, anything else falls back to 3', () => {
  assert.equal(lowBalanceThreshold('5'), 5);
  assert.equal(lowBalanceThreshold('0.5'), 0.5);
  for (const bad of [undefined, '', '  ', 'abc', 'NaN', 'Infinity', '-2', null]) assert.equal(lowBalanceThreshold(bad), 3, String(bad));
});
