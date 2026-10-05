import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import http from 'node:http';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import * as gmCmd from '../src/commands/gm.js';
import { loadConfig, loadWakeConfig } from '../src/config.js';
import { WakeUsageLogger, summarizeWakes } from '../src/usage.js';
import { GmWakeNotifier, buildPayload, postWake } from '../src/wake.js';
import { WakeBudget, formatClock, loadWakeHistory, postsUsed } from '../src/wakebudget.js';

const KEY = 'budget-SECRET-key-123';
const BODY_SECRET = 'Automation run rate limit exceeded: grok bot user limit 100 per hour';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const tmp = () => mkdtempSync(path.join(tmpdir(), 'wb-'));
const timing = { retryDelayMs: 10, pollMs: 10, timeoutMs: 2000 };
async function until(fn, ms = 4000) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    if (fn()) return true;
    await sleep(10);
  }
  return false;
}

async function mockHook(handler) {
  const reqs = [];
  const srv = http.createServer((req, res) => {
    let b = '';
    req.on('data', (d) => (b += d));
    req.on('end', () => {
      reqs.push({ t: Date.now(), body: b ? JSON.parse(b) : null });
      if (handler) return handler(reqs.length, res);
      res.end('ok');
    });
  });
  await new Promise((r) => srv.listen(0, '127.0.0.1', r));
  const port = srv.address().port;
  return { reqs, port, url: `http://127.0.0.1:${port}/hooks/PATH-SECRET`, close: () => { srv.closeAllConnections?.(); return new Promise((r) => srv.close(r)); } };
}
const cfg = (url, extra = {}) => ({
  ...loadWakeConfig({ GM_WEBHOOK_URL: url, GM_WEBHOOK_KEY: KEY }),
  debounceMs: 40, maxWaitMs: 150, minIntervalMs: 0, idleMaxWaitMs: 100, rateLimitBackoffMs: 400, ...extra,
});
function capture() {
  const lines = [];
  const mk = (l) => (...a) => lines.push(`${l} ${a.join(' ')}`);
  return { lines, logger: { debug: mk('debug'), info: mk('info'), warn: mk('warn'), error: mk('error') } };
}
const rowsOf = (file) => {
  try {
    return readFileSync(file, 'utf8').trim().split('\n').filter(Boolean).map(JSON.parse);
  } catch {
    return [];
  }
};

// ------------------------------------------------------------------ budget math

test('WakeBudget: rolling window, exhaustion and the time the oldest POST falls out', () => {
  const t0 = 10_000_000;
  let t = t0;
  const b = new WakeBudget({ max: 3, windowMs: 3_600_000, now: () => t });
  b.record(1, t0 - 3_000_000);
  b.record(1, t0 - 2_000_000);
  b.record(1, t0 - 1_000_000);
  assert.equal(b.used(), 3);
  assert.equal(b.isExhausted(), true);
  assert.equal(b.nextSlotAt(), t0 - 3_000_000 + 3_600_000, 'oldest counted wake + 60 min');
  t += 700_000; // oldest now 3.7M old => out of the window
  assert.equal(b.used(), 2);
  assert.equal(b.isExhausted(), false);
  assert.equal(b.nextSlotAt(), t);
  b.record(2); // two more at once (a retried POST) => over by one
  assert.equal(b.used(), 4);
  assert.equal(b.nextSlotAt(), t0 - 1_000_000 + 3_600_000, 'the second-oldest POST must expire before there is room again');
  assert.ok(b.status().exhausted && b.status().resumeAt > t);
  const off = new WakeBudget({ max: 0 });
  off.record(100);
  assert.equal(off.isExhausted(), false);
  assert.equal(off.nextSlotAt(5), 5);
});

test('postsUsed: skipped / rate-limited / legacy 400 use nothing; attempts count', () => {
  assert.equal(postsUsed({ ok: true, status: 200 }), 1);
  assert.equal(postsUsed({ ok: false, status: 502, attempts: 2 }), 2);
  assert.equal(postsUsed({ ok: false, status: null, attempts: 2 }), 2, 'failed POSTs count too');
  assert.equal(postsUsed({ skipped: true, lines: 1 }), 0);
  assert.equal(postsUsed({ ok: false, status: 400, attempts: 1, rate_limited: true }), 0);
  assert.equal(postsUsed({ ok: false, status: 400 }), 0, 'legacy 400 (pre-budget log) was a rate-limit rejection');
  assert.equal(postsUsed({ ok: false, status: 400, attempts: 1 }), 1, 'a new-format plain 400 did reach the server');
});

test('restart keeps the count: history is rebuilt from the wake log', () => {
  const dir = tmp();
  try {
    const now = Date.parse('2026-10-04T20:00:00Z');
    const iso = (minAgo) => new Date(now - minAgo * 60_000).toISOString();
    const file = path.join(dir, 'w.jsonl');
    writeFileSync(file, [
      { ts: iso(90), lines: 1, ok: true, status: 200 }, // outside the window
      { ts: iso(50), lines: 1, ok: true, status: 200 },
      { ts: iso(40), lines: 2, ok: false, status: 502, attempts: 2 },
      { ts: iso(30), skipped: true, reason: 'spotlight', lines: 1 },
      { ts: iso(20), lines: 1, ok: false, status: 400 }, // legacy rate-limit rejection
      { ts: iso(2), lines: 3, ok: false, status: 400, attempts: 1, rate_limited: true },
      { ts: iso(1), lines: 1, ok: true, status: 200, attempts: 1 },
    ].map((r) => JSON.stringify(r)).join('\n') + '\nnot json\n');
    const h = loadWakeHistory(file, { now, backoffMs: 5 * 60_000 });
    assert.equal(h.stamps.length, 1 + 2 + 1);
    assert.equal(h.rateLimitedUntil, now - 2 * 60_000 + 5 * 60_000, 'a recent rate limit keeps backing off after a restart');
    const b = new WakeBudget({ max: 4, now: () => now });
    b.stamps = h.stamps;
    assert.equal(b.isExhausted(), true);
    assert.equal(b.nextSlotAt(), now - 50 * 60_000 + 3_600_000);
    assert.deepEqual(loadWakeHistory(path.join(dir, 'nope.jsonl'), { now }), { stamps: [], rateLimitedUntil: 0 });
    assert.match(formatClock(now), /^\d\d:\d\d$/);
  } finally {
    rmSync(dir, { recursive: true });
  }
});

// ------------------------------------------------------------------ rate-limit detection

test('postWake: 400 with "rate limit" in the body is a rate limit (no retry); other 400s are not; 429 is', async () => {
  const cases = [
    [400, BODY_SECRET, true],
    [400, 'RATE-LIMIT hit', true],
    [400, 'rate_limit', true],
    [400, 'bad payload', false],
    [429, '', true],
    [403, 'rate limit', false], // only 400/429 are inspected
  ];
  for (const [status, body, expected] of cases) {
    const m = await mockHook((_n, res) => ((res.statusCode = status), res.end(body)));
    try {
      const r = await postWake(cfg(m.url), buildPayload([]), timing);
      assert.equal(r.rateLimited, expected, `${status} ${body}`);
      assert.equal(r.ok, false);
      assert.equal(r.attempts, 1);
      assert.equal(m.reqs.length, 1, 'never retried');
    } finally {
      await m.close();
    }
  }
  const flaky = await mockHook((n, res) => ((res.statusCode = n === 1 ? 503 : 200), res.end('x')));
  try {
    const r = await postWake(cfg(flaky.url), buildPayload([]), timing);
    assert.deepEqual([r.ok, r.attempts, r.rateLimited], [true, 2, false]);
  } finally {
    await flaky.close();
  }
});

test('rate limited: lines are held (not dropped), backoff, then ONE batched retry; log shows only a short marker', async () => {
  const dir = tmp();
  const m = await mockHook((n, res) => (n === 1 ? ((res.statusCode = 400), res.end(BODY_SECRET)) : res.end('ok')));
  try {
    const file = path.join(dir, 'w.jsonl');
    const { logger, lines } = capture();
    const blocked = [];
    const budget = new WakeBudget({ max: 60 });
    const n = new GmWakeNotifier({ wake: cfg(m.url), logger, timing, budget, onBlocked: (b) => blocked.push(b), usageLog: new WakeUsageLogger({ path: file, session: 'S1' }) });
    n.notify({ speaker: 'A', text: 'first line' });
    n.notify({ speaker: 'B', text: 'second line' });
    assert.ok(await until(() => m.reqs.length === 1));
    await sleep(120);
    n.notify({ speaker: 'C', text: 'third line, during the backoff' });
    await sleep(150);
    assert.equal(m.reqs.length, 1, 'nothing sent during the 400 ms backoff');
    assert.equal(budget.used(), 0, 'a rate-limited rejection does not use budget');
    assert.ok(await until(() => m.reqs.length === 2, 3000));
    assert.ok(m.reqs[1].t - m.reqs[0].t >= 380, `retry after ${m.reqs[1].t - m.reqs[0].t}ms`);
    assert.deepEqual(m.reqs[1].body.lines.map((l) => l.text), ['first line', 'second line', 'third line, during the backoff'], 'all lines kept, in order');
    await sleep(60);
    assert.equal(budget.used(), 1);
    const rows = rowsOf(file);
    assert.deepEqual(rows.map((r) => [r.status, r.ok, r.rate_limited ?? false, r.lines]), [[400, false, true, 2], [200, true, false, 3]]);
    assert.equal(blocked.length, 1);
    assert.equal(blocked[0].reason, 'rate_limit');
    assert.ok(blocked[0].resumeAt > Date.now() - 100);
    const all = lines.join('\n');
    assert.match(all, /rate limited \(HTTP 400\)/);
    for (const secret of [BODY_SECRET, 'grok bot user', 'Automation', KEY, 'PATH-SECRET', '127.0.0.1', String(m.port), 'first line']) {
      assert.ok(!all.includes(secret), `log leaked ${secret}`);
    }
    assert.ok(!JSON.stringify(rows).includes('Automation'));
    n.stop();
  } finally {
    await m.close();
    rmSync(dir, { recursive: true });
  }
});

test('a plain 400 (not a rate limit) still drops the batch as before', async () => {
  const m = await mockHook((_n, res) => ((res.statusCode = 400), res.end('invalid')));
  try {
    const { logger, lines } = capture();
    const n = new GmWakeNotifier({ wake: cfg(m.url), logger, timing, budget: new WakeBudget({ max: 60 }) });
    n.notify({ speaker: 'A', text: 'x' });
    assert.ok(await until(() => m.reqs.length === 1));
    await sleep(200);
    assert.equal(m.reqs.length, 1);
    assert.equal(n.pending.length, 0);
    assert.match(lines.join('\n'), /GM wake failed: HTTP 400/);
    n.stop();
  } finally {
    await m.close();
  }
});

// ------------------------------------------------------------------ budget exhausted

test('budget exhausted: lines are HELD, logged as skipped/budget, notice once; ONE batched wake when the oldest falls out', async () => {
  const dir = tmp();
  const m = await mockHook();
  try {
    const file = path.join(dir, 'w.jsonl');
    const { logger, lines } = capture();
    const blocked = [];
    const budget = new WakeBudget({ max: 2, windowMs: 600 });
    budget.record(1, Date.now() - 100); // oldest counted wake: leaves the window ~500 ms from now
    budget.record(1, Date.now() - 50);
    const t0 = Date.now();
    const n = new GmWakeNotifier({ wake: cfg(m.url), logger, timing, budget, onBlocked: (b) => blocked.push(b), usageLog: new WakeUsageLogger({ path: file, session: 'S1' }) });
    n.notify({ speaker: 'A', text: 'one' });
    await sleep(80);
    n.notify({ speaker: 'B', text: 'two' });
    n.notify({ speaker: 'C', text: 'three' });
    await sleep(200);
    assert.equal(m.reqs.length, 0, 'held while the budget is exhausted');
    assert.equal(n.pending.length, 3, 'nothing dropped');
    assert.ok(await until(() => m.reqs.length === 1, 3000));
    assert.ok(m.reqs[0].t - t0 >= 450, `sent at +${m.reqs[0].t - t0}ms`);
    assert.deepEqual(m.reqs[0].body.lines.map((l) => l.text), ['one', 'two', 'three'], 'one batched wake with every held line');
    await sleep(100);
    assert.equal(m.reqs.length, 1);
    assert.equal(blocked.length, 1, 'notice only when the budget first blocks');
    assert.equal(blocked[0].reason, 'budget');
    assert.ok(Math.abs(blocked[0].resumeAt - (t0 - 100 + 600)) < 80, 'resume time = oldest counted wake + window');
    const rows = rowsOf(file);
    assert.deepEqual(rows.filter((r) => r.skipped).map((r) => [r.reason, r.lines]), [['budget', 1], ['budget', 1], ['budget', 1]], 'each held line logged once');
    const wakeRow = rows.find((r) => !r.skipped);
    assert.deepEqual([wakeRow.lines, wakeRow.ok], [3, true]);
    const sum = summarizeWakes(rows);
    assert.deepEqual([sum.total.wakes, sum.total.budget_held, sum.total.saved_upper_bound, sum.total.skipped], [1, 3, 0, 0], 'held lines are not counted as savings');
    const all = lines.join('\n');
    assert.match(all, /GM wake budget reached \(2\/2 in the last hour\): holding 1 line\(s\) until \d\d:\d\d/);
    for (const secret of [KEY, 'PATH-SECRET', '127.0.0.1', 'three']) assert.ok(!all.includes(secret));
    n.stop();
  } finally {
    await m.close();
    rmSync(dir, { recursive: true });
  }
});

test('new hold episode after a wake goes out: notice fires again', async () => {
  const m = await mockHook();
  try {
    const blocked = [];
    const budget = new WakeBudget({ max: 1, windowMs: 300 });
    budget.record(1, Date.now());
    const n = new GmWakeNotifier({ wake: cfg(m.url), logger: capture().logger, timing, budget, onBlocked: (b) => blocked.push(b.reason) });
    n.notify({ speaker: 'A', text: 'a' });
    assert.ok(await until(() => m.reqs.length === 1));
    n.notify({ speaker: 'A', text: 'b' }); // budget used again by the wake just sent
    assert.ok(await until(() => m.reqs.length === 2, 3000));
    assert.deepEqual(blocked, ['budget', 'budget']);
    n.stop();
  } finally {
    await m.close();
  }
});

test('warns once at 80% of the budget (logs only), re-armed when the count falls', async () => {
  const m = await mockHook();
  try {
    const { logger, lines } = capture();
    const budget = new WakeBudget({ max: 5, windowMs: 3_600_000 });
    budget.record(2, Date.now() - 1000);
    const n = new GmWakeNotifier({ wake: cfg(m.url), logger, timing, budget });
    const warns = () => lines.filter((l) => /budget at \d+%/.test(l));
    n.notify({ speaker: 'A', text: '1' });
    assert.ok(await until(() => m.reqs.length === 1));
    await sleep(60);
    assert.equal(warns().length, 0, '3/5 = 60%');
    n.notify({ speaker: 'A', text: '2' });
    assert.ok(await until(() => m.reqs.length === 2));
    await sleep(60);
    assert.equal(warns().length, 1, '4/5 = 80%');
    assert.match(warns()[0], /warn .*80% \(4\/5 wakes in the last hour\)/);
    n.notify({ speaker: 'A', text: '3' });
    assert.ok(await until(() => m.reqs.length === 3));
    await sleep(60);
    assert.equal(warns().length, 1, 'only once');
    n.stop();
  } finally {
    await m.close();
  }
});

test('budget disabled (0) never holds; no budget object behaves as before', async () => {
  const m = await mockHook();
  try {
    const budget = new WakeBudget({ max: 0 });
    const n = new GmWakeNotifier({ wake: cfg(m.url), logger: capture().logger, timing, budget });
    for (let i = 0; i < 3; i++) {
      n.notify({ speaker: 'A', text: `l${i}` });
      assert.ok(await until(() => m.reqs.length === i + 1));
      await sleep(30);
    }
    n.stop();
    assert.equal(loadWakeConfig({}).maxPerHour, 60);
    assert.equal(loadWakeConfig({ WAKE_MAX_PER_HOUR: '0' }).maxPerHour, 0);
    assert.equal(loadWakeConfig({ WAKE_MAX_PER_HOUR: '25' }).maxPerHour, 25);
    assert.equal(loadWakeConfig({}).rateLimitBackoffMs, 300_000);
    assert.equal(loadConfig({ DISCORD_TOKEN: 't', CLIENT_ID: '111111111111111111', GUILD_ID: '222222222222222222', TRANSCRIPT_CHANNEL_ID: '444444444444444444', GM_OUTPUT_CHANNEL_ID: '555555555555555555', OPENAI_API_KEY: 'x' }).wake.maxPerHour, 60);
  } finally {
    await m.close();
  }
});

// ------------------------------------------------------------------ /gm status + report

test('/gm status shows wakes used in the last hour / budget, held lines and resume time', async () => {
  const replies = [];
  const i = { user: { id: 'u' }, options: { getString: () => 'status' }, reply: async (r) => replies.push(r.content) };
  const budget = new WakeBudget({ max: 10 });
  budget.record(4);
  const fakeWake = new GmWakeNotifier({ wake: loadWakeConfig({ GM_WEBHOOK_URL: 'http://127.0.0.1:9/x' }), logger: capture().logger, budget });
  const ctx = { gmState: { paused: false }, config: { wake: { enabled: true }, spotlight: { enabled: false } }, wake: fakeWake, logger: capture().logger };
  await gmCmd.execute(i, ctx);
  assert.match(replies[0], /Wakes used in the last hour: \*\*4 \/ 10\*\*\./);
  budget.record(6);
  fakeWake.pending = [{}, {}];
  await gmCmd.execute(i, ctx);
  assert.match(replies[1], /\*\*10 \/ 10\*\* - budget reached, next wake at \d\d:\d\d \(2 lines held for the next wake\)\./);
  fakeWake.rateLimitedUntil = Date.now() + 60_000;
  await gmCmd.execute(i, ctx);
  assert.match(replies[2], /rate limited by the server, retrying at \d\d:\d\d/);
  const off = new GmWakeNotifier({ wake: loadWakeConfig({}), logger: capture().logger, budget: new WakeBudget({ max: 0 }) });
  await gmCmd.execute(i, { ...ctx, wake: off });
  assert.match(replies[3], /unlimited/);
  await gmCmd.execute(i, { ...ctx, wake: undefined });
  assert.ok(replies[4].includes('GM wake: **ON**'), 'works without the notifier');
});

test('npm run usage: wakes in the last 60 min / budget, rate-limited and held columns', () => {
  const dir = tmp();
  try {
    const now = Date.now();
    const iso = (minAgo) => new Date(now - minAgo * 60_000).toISOString();
    const date = iso(0).slice(0, 10);
    const f = path.join(dir, 'w.jsonl');
    writeFileSync(f, [
      { ts: iso(5), date, session: 'S1', lines: 2, ok: true, status: 200, overrides: 0, attempts: 1 },
      { ts: iso(4), date, session: 'S1', lines: 1, ok: false, status: 502, overrides: 0, attempts: 2 },
      { ts: iso(3), date, session: 'S1', lines: 3, ok: false, status: 400, overrides: 0, attempts: 1, rate_limited: true },
      { ts: iso(2), date, session: 'S1', skipped: true, speaker_matched: false, reason: 'budget', lines: 1 },
      { ts: iso(1), date, session: 'S1', skipped: true, speaker_matched: false, reason: 'budget', lines: 1 },
    ].map((r) => JSON.stringify(r)).join('\n') + '\n');
    const run = (...a) => spawnSync(process.execPath, ['scripts/tts-usage-summary.js', '--file', path.join(dir, 'none'), '--wake-file', f, '--events-file', path.join(dir, 'none2'), ...a], { encoding: 'utf8', cwd: path.join(import.meta.dirname, '..'), env: { PATH: process.env.PATH, WAKE_MAX_PER_HOUR: '10' } });
    const r = run();
    assert.equal(r.status, 0, r.stderr);
    assert.match(r.stdout, /Last 60 min: 3 wake POST\(s\) of a budget of 10 \(WAKE_MAX_PER_HOUR; 7 left\)\. 1 rate-limited rejection\(s\) in the report period; 2 line\(s\) were held by the budget\./);
    assert.match(r.stdout, /rate-lim/);
    const j = JSON.parse(run('--json').stdout);
    assert.deepEqual([j.wakes.total.wakes, j.wakes.total.rate_limited, j.wakes.total.budget_held, j.wakes.total.attempts], [2, 1, 2, 4]);
    assert.equal(j.wakes.total.saved_upper_bound, 0);
  } finally {
    rmSync(dir, { recursive: true });
  }
});
