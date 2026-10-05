import assert from 'node:assert/strict';
import http from 'node:http';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { loadConfig, loadWakeConfig } from '../src/config.js';
import { resolveCampaignRoot } from '../src/paths.js';
import { SttBridge } from '../src/stt.js';
import { createSpotlightFilter, decide, hasWakeWord, nameMatches, normalizeName, readSpotlight } from '../src/spotlight.js';
import { WakeUsageLogger, parseWakeJsonl, summarizeWakes } from '../src/usage.js';
import { GmWakeNotifier } from '../src/wake.js';

const quiet = { debug() {}, info() {}, warn() {}, error() {} };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const NOW = Date.parse('2026-10-04T18:00:00Z');
const minsAgo = (m) => new Date(NOW - m * 60_000).toISOString();

function tmpFile(content) {
  const dir = mkdtempSync(path.join(tmpdir(), 'spot-'));
  const file = path.join(dir, 'spotlight.json');
  if (content !== undefined) writeFileSync(file, typeof content === 'string' ? content : JSON.stringify(content));
  return { dir, file, done: () => rmSync(dir, { recursive: true }) };
}
const read = (f, o = {}) => readSpotlight({ file: f, maxAgeMinutes: 20, now: NOW, ...o });

// ---------------------------------------------------------------- wake word

test('wake word: AI / A.I. / A I / hey AI match (any case, punctuation)', () => {
  for (const t of ['AI', 'ai', 'Ai?', 'Hey AI, what now', 'hey ai', 'A.I.', 'a.i', 'A. I.', 'A I', 'okay, AI! help', 'so... AI.', '"AI" please', 'the AI said no', "AI's turn"]) {
    assert.equal(hasWakeWord(t), true, t);
  }
});

test('wake word: said / again / main / mail / aim / available / paid / rain do NOT match', () => {
  for (const t of ['he said no', 'again', 'main quest', 'mail', 'aim high', 'available', 'I paid', 'rain', 'raising', 'Aidan', 'chair it', 'AIM', 'maid', 'wait, I', 'a it', 'I am', 'Thai food', 'hair', 'aisle', 'said again, the main thing', '']) {
    assert.equal(hasWakeWord(t), false, JSON.stringify(t));
  }
});

// ---------------------------------------------------------------- name matching

test('name matching: case/accent-insensitive, substring either way, short names exact only', () => {
  assert.equal(normalizeName('  JOSÉ-Ñandú!! '), 'jose nandu');
  assert.ok(nameMatches('Trailer Park Moses', 'moses'));
  assert.ok(nameMatches('Moses', 'Trailer Park Moses'));
  assert.ok(nameMatches('José', 'jose'));
  assert.ok(nameMatches('MOSES the 2nd', 'Moses'));
  assert.ok(nameMatches('X', 'x'));
  assert.ok(!nameMatches('Xavier', 'X'), 'a single character never substring-matches');
  assert.ok(!nameMatches('Hornn', 'Moses'));
  assert.ok(!nameMatches('', 'Moses'));
  assert.ok(!nameMatches('Moses', ''));
});

// ---------------------------------------------------------------- state file (fail open)

test('readSpotlight: active file', () => {
  const t = tmpFile({ player: 'Moses', aliases: ['TPM', 7, ''], updated: minsAgo(5), note: 'x' });
  try {
    const s = read(t.file);
    assert.deepEqual([s.active, s.player, s.aliases, s.note], [true, 'Moses', ['TPM'], 'x']);
  } finally {
    t.done();
  }
});

test('readSpotlight fails OPEN for null / missing / empty / unreadable / malformed / stale / bad timestamps', () => {
  const cases = {
    cleared: { player: null, updated: minsAgo(1) },
    cleared2: { player: '', updated: minsAgo(1) },
    wrongtype: { player: 42, updated: minsAgo(1) },
    stale: { player: 'Moses', updated: minsAgo(21) },
    no_timestamp: { player: 'Moses' },
    bad_ts: { player: 'Moses', updated: 'yesterday-ish' },
    future: { player: 'Moses', updated: new Date(NOW + 3_600_000).toISOString() },
    array: ['Moses'],
  };
  for (const [name, content] of Object.entries(cases)) {
    const t = tmpFile(content);
    try {
      assert.equal(read(t.file).active, false, name);
    } finally {
      t.done();
    }
  }
  for (const [name, raw] of [['empty', ''], ['whitespace', '  \n'], ['malformed', '{"player": "Mo'], ['garbage', 'not json at all'], ['null', 'null'], ['number', '5']]) {
    const t = tmpFile(raw);
    try {
      assert.equal(read(t.file).active, false, name);
    } finally {
      t.done();
    }
  }
  assert.equal(read('/nonexistent/dir/spotlight.json').reason, 'missing');
  assert.equal(read(undefined).active, false);
  const t = tmpFile();
  try {
    assert.equal(read(t.dir).active, false, 'a directory is unreadable, not fatal');
    assert.equal(read(t.dir).reason, 'unreadable');
  } finally {
    t.done();
  }
  // exactly at the age limit is still fresh; 20 min + 1s is stale
  const e = tmpFile({ player: 'Moses', updated: minsAgo(20) });
  try {
    assert.equal(read(e.file).active, true);
    assert.equal(read(e.file, { now: NOW + 1000 }).active, false);
    assert.equal(read(e.file, { now: NOW + 1000, maxAgeMinutes: 30 }).active, true);
  } finally {
    e.done();
  }
});

// ---------------------------------------------------------------- decide()

test('decide: open floor wakes for everyone', () => {
  const open = { active: false, reason: 'missing' };
  assert.deepEqual(decide({ speaker: 'Hornn', text: 'hi' }, open), { wake: true, reason: 'open_floor', override: false });
});

test('decide: spotlight player wakes; others skipped; wake word overrides; aliases + username match', () => {
  const spot = { active: true, player: 'Trailer Park Moses', aliases: ['TPM'] };
  assert.equal(decide({ speaker: 'moses', text: 'I buy the thing' }, spot).wake, true);
  assert.equal(decide({ speaker: 'Mösés', text: 'accent check' }, spot).wake, true);
  assert.equal(decide({ speaker: 'tpm_gaming', text: 'alias' }, spot).wake, true);
  assert.equal(decide({ speaker: 'Nickname', names: ['trailerparkmoses'], text: 'username only' }, { ...spot, player: 'Trailer Park Moses' }).wake, false, 'no separator => no match (documented)');
  assert.equal(decide({ speaker: 'Nick', names: ['trailer_park_moses'], text: 'username' }, spot).wake, true);
  assert.deepEqual(decide({ speaker: 'Hornn', text: 'I swing my axe' }, spot), { wake: false, reason: 'spotlight', override: false });
  assert.deepEqual(decide({ speaker: 'Hornn', text: 'Hey AI, wait' }, spot), { wake: true, reason: 'wake_word', override: true });
  assert.deepEqual(decide({ speaker: 'Hornn', text: 'he said again' }, spot), { wake: false, reason: 'spotlight', override: false });
  // wake word from the spotlight player is a normal match, not an override
  assert.deepEqual(decide({ speaker: 'Moses', text: 'AI?' }, spot), { wake: true, reason: 'spotlight_player', override: false });
});

// ---------------------------------------------------------------- filter factory

test('filter: reads the file live; disabled / broken input never blocks', () => {
  const t = tmpFile({ player: 'Moses', updated: new Date().toISOString() });
  try {
    const logs = [];
    const logger = { ...quiet, info: (m) => logs.push(m), warn: (m) => logs.push(m) };
    const f = createSpotlightFilter({ config: { enabled: true, file: t.file, maxAgeMinutes: 20 }, logger });
    assert.equal(f({ speaker: 'Hornn', text: 'hello' }).wake, false);
    assert.equal(f({ speaker: 'Hornn', text: 'AI' }).override, true);
    writeFileSync(t.file, '{broken');
    assert.equal(f({ speaker: 'Hornn', text: 'hello' }).wake, true, 'malformed => open');
    assert.equal(f({ speaker: 'Hornn', text: 'hello again' }).wake, true);
    writeFileSync(t.file, JSON.stringify({ player: null, updated: new Date().toISOString() }));
    assert.equal(f({ speaker: 'Hornn', text: 'hello' }).wake, true);
    writeFileSync(t.file, JSON.stringify({ player: 'Hornn', updated: new Date().toISOString() }));
    assert.equal(f({ speaker: 'Hornn', text: 'x' }).wake, true);
    assert.equal(f({ speaker: 'Moses', text: 'x' }).wake, false);
    // state changes are logged once each, and never contain transcript text
    assert.equal(logs.filter((l) => /Spotlight file problem/.test(l)).length, 1);
    assert.ok(!logs.join('\n').includes('hello'));
    const off = createSpotlightFilter({ config: { enabled: false, file: t.file }, logger });
    assert.equal(off({ speaker: 'Moses', text: 'x' }).wake, true);
    const noCfg = createSpotlightFilter({ config: undefined, logger });
    assert.equal(noCfg({ speaker: 'x', text: 'y' }).wake, true);
  } finally {
    t.done();
  }
});

test('config: spotlight defaults and overrides', () => {
  const env = { DISCORD_TOKEN: 't', CLIENT_ID: '111111111111111111', GUILD_ID: '222222222222222222', TRANSCRIPT_CHANNEL_ID: '444444444444444444', GM_OUTPUT_CHANNEL_ID: '555555555555555555', OPENAI_API_KEY: 'x' };
  const c = loadConfig(env).spotlight;
  assert.deepEqual(c, { enabled: true, file: path.join(resolveCampaignRoot(env), 'sessions', 'spotlight.json'), maxAgeMinutes: 20 });
  const o = loadConfig({ ...env, SPOTLIGHT_FILTER_ENABLED: 'false', SPOTLIGHT_FILE: '/tmp/s.json', SPOTLIGHT_MAX_AGE_MINUTES: '45' }).spotlight;
  assert.deepEqual(o, { enabled: false, file: '/tmp/s.json', maxAgeMinutes: 45 });
});

// ---------------------------------------------------------------- notifier integration

async function mockHook() {
  const reqs = [];
  const srv = http.createServer((req, res) => {
    let b = '';
    req.on('data', (d) => (b += d));
    req.on('end', () => {
      reqs.push(JSON.parse(b));
      res.end('ok');
    });
  });
  await new Promise((r) => srv.listen(0, '127.0.0.1', r));
  return { reqs, url: `http://127.0.0.1:${srv.address().port}/h`, close: () => { srv.closeAllConnections?.(); return new Promise((r) => srv.close(r)); } };
}
const wakeCfg = (url) => ({ ...loadWakeConfig({ GM_WEBHOOK_URL: url, GM_WEBHOOK_KEY: 'k' }), debounceMs: 60, maxWaitMs: 300, minIntervalMs: 0 });
const timing = { retryDelayMs: 10, pollMs: 10, timeoutMs: 2000 };
async function until(fn, ms = 3000) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    if (fn()) return true;
    await sleep(10);
  }
  return false;
}
function setup(m, spotContent, wakeLogFile) {
  const t = tmpFile(spotContent);
  const usageLog = new WakeUsageLogger({ path: wakeLogFile ?? path.join(t.dir, 'wake-usage.jsonl'), session: 'S1' });
  const infos = [];
  const filter = createSpotlightFilter({ config: { enabled: true, file: t.file, maxAgeMinutes: 20 }, logger: quiet });
  const n = new GmWakeNotifier({ wake: wakeCfg(m.url), logger: { ...quiet, info: (x) => infos.push(x) }, timing, usageLog, filter });
  return { t, n, infos, usageLog, log: () => (readLog(path.join(t.dir, 'wake-usage.jsonl'))) };
}
function readLog(file) {
  try {
    return readFileSync(file, 'utf8').trim().split('\n').filter(Boolean).map(JSON.parse);
  } catch {
    return [];
  }
}

test('no spotlight => every line wakes (batched as before), nothing skipped', async () => {
  const m = await mockHook();
  const s = setup(m, undefined);
  try {
    s.n.notify({ speaker: 'Hornn', text: 'one' });
    s.n.notify({ speaker: 'Moses', text: 'two' });
    assert.ok(await until(() => m.reqs.length === 1));
    assert.deepEqual(m.reqs[0].lines.map((l) => l.text), ['one', 'two']);
    await sleep(40);
    const rows = s.log();
    assert.equal(rows.length, 1);
    assert.equal(rows[0].skipped, undefined);
    assert.equal(rows[0].overrides, 0);
  } finally {
    s.n.stop();
    s.t.done();
    await m.close();
  }
});

test('spotlight set: other speaker is skipped (no POST), logged as skipped; payload shape unchanged', async () => {
  const m = await mockHook();
  const s = setup(m, { player: 'Moses', updated: new Date().toISOString() });
  try {
    s.n.notify({ speaker: 'Hornn', text: 'private chatter that must never be logged' });
    s.n.notify({ speaker: 'Hornn', text: 'more chatter' });
    await sleep(300);
    assert.equal(m.reqs.length, 0, 'no wake for non-spotlight speech');
    assert.equal(s.n.pending.length, 0);
    const rows = s.log();
    assert.equal(rows.length, 2);
    for (const r of rows) {
      assert.deepEqual(Object.keys(r), ['ts', 'date', 'session', 'dcc_session', 'skipped', 'speaker_matched', 'reason', 'lines']);
      assert.deepEqual([r.skipped, r.speaker_matched, r.reason, r.lines, r.session], [true, false, 'spotlight', 1, 'S1']);
    }
    assert.ok(!JSON.stringify(rows).includes('chatter'));
    // matching player wakes with the usual payload
    s.n.notify({ speaker: 'Trailer Park Moses', text: 'I do the thing', ts: '2026-10-04T18:00:00.000Z' });
    assert.ok(await until(() => m.reqs.length === 1));
    assert.deepEqual(Object.keys(m.reqs[0]), ['event', 'channel', 'lines', 'hint']);
    assert.deepEqual(m.reqs[0].lines, [{ speaker: 'Trailer Park Moses', text: 'I do the thing', ts: '2026-10-04T18:00:00.000Z' }]);
  } finally {
    s.n.stop();
    s.t.done();
    await m.close();
  }
});

test('wake word from a non-spotlight player wakes, is batched with the spotlight line, logged as an override', async () => {
  const m = await mockHook();
  const s = setup(m, { player: 'Moses', updated: new Date().toISOString() });
  try {
    s.n.notify({ speaker: 'Moses', text: 'I think so' });
    s.n.notify({ speaker: 'Hornn', text: 'side talk' }); // skipped
    s.n.notify({ speaker: 'Hornn', text: 'AI, hold on' }); // override
    assert.ok(await until(() => m.reqs.length === 1));
    assert.deepEqual(m.reqs[0].lines.map((l) => l.text), ['I think so', 'AI, hold on'], 'skipped line is not in the batch');
    assert.ok(s.infos.some((x) => /wake word from a non-spotlight player/.test(x)));
    await sleep(40);
    const rows = s.log();
    const wake = rows.find((r) => !r.skipped);
    assert.deepEqual([wake.lines, wake.overrides, wake.ok], [2, 1, true]);
    assert.equal(rows.filter((r) => r.skipped).length, 1);
    const sum = summarizeWakes(parseWakeJsonl(rows.map((r) => JSON.stringify(r)).join('\n')).records);
    assert.deepEqual(sum.total, { wakes: 1, failed: 0, lines: 2, skipped: 1, paused: 0, budget_held: 0, rate_limited: 0, attempts: 1, overrides: 1, saved_upper_bound: 1 });
  } finally {
    s.n.stop();
    s.t.done();
    await m.close();
  }
});

test('"said / again / main" from a non-spotlight player do not wake', async () => {
  const m = await mockHook();
  const s = setup(m, { player: 'Moses', updated: new Date().toISOString() });
  try {
    for (const text of ['He said it again', 'the main door', 'Maine and Spain']) s.n.notify({ speaker: 'Hornn', text });
    await sleep(300);
    assert.equal(m.reqs.length, 0);
    assert.equal(s.log().filter((r) => r.skipped).length, 3);
  } finally {
    s.n.stop();
    s.t.done();
    await m.close();
  }
});

test('malformed or stale file: filter fails open and every line wakes', async () => {
  for (const content of ['{oops', { player: 'Moses', updated: new Date(Date.now() - 3_600_000).toISOString() }]) {
    const m = await mockHook();
    const s = setup(m, content);
    try {
      s.n.notify({ speaker: 'Hornn', text: 'anyone there' });
      assert.ok(await until(() => m.reqs.length === 1), 'wake fired');
      assert.equal(s.log().filter((r) => r.skipped).length, 0);
    } finally {
      s.n.stop();
      s.t.done();
      await m.close();
    }
  }
});

test('a throwing filter fails open; skip-logging errors never break the notifier', async () => {
  const m = await mockHook();
  try {
    const n = new GmWakeNotifier({ wake: wakeCfg(m.url), logger: quiet, timing, filter: () => { throw new Error('boom'); } });
    n.notify({ speaker: 'A', text: 'x' });
    assert.ok(await until(() => m.reqs.length === 1));
    n.stop();
    const n2 = new GmWakeNotifier({
      wake: wakeCfg(m.url), logger: quiet, timing,
      filter: () => ({ wake: false, reason: 'spotlight' }),
      usageLog: { recordSkipped: () => { throw new Error('disk'); } },
    });
    assert.doesNotThrow(() => n2.notify({ speaker: 'A', text: 'x' }));
    n2.stop();
  } finally {
    await m.close();
  }
});

test('STT bridge passes the Discord username as an extra identity to the wake hook', async () => {
  const channel = { name: 'dcc_ears', isTextBased: () => true, send: async () => {} };
  const calls = [];
  const stt = new SttBridge({
    client: { user: { id: 'bot' }, channels: { fetch: async () => channel } },
    config: { discord: { transcriptChannelId: '1' }, stt: { concurrency: 1 } },
    logger: quiet,
    onTranscript: (l) => calls.push(l),
  });
  await stt._post('Nick', 'hi', { username: 'moses_the_great' });
  await stt._post('Nick', 'hi');
  assert.deepEqual(calls[0].names, ['moses_the_great']);
  assert.deepEqual(calls[1].names, []);
});

// ---------------------------------------------------------------- usage report

test('wake summary: per day/session wakes, skipped, overrides, saved upper bound; old records still parse', () => {
  const recs = [
    { ts: '2026-10-03T20:00:00Z', date: '2026-10-03', session: 'S1', lines: 3, ok: true, status: 200 }, // pre-spotlight record
    { ts: '2026-10-04T20:00:00Z', date: '2026-10-04', session: 'S2', lines: 2, ok: true, status: 200, overrides: 1 },
    { ts: '2026-10-04T20:01:00Z', date: '2026-10-04', session: 'S2', skipped: true, speaker_matched: false, reason: 'spotlight', lines: 1 },
    { ts: '2026-10-04T20:02:00Z', date: '2026-10-04', session: 'S2', skipped: true, speaker_matched: false, reason: 'spotlight', lines: 1 },
    { ts: '2026-10-04T20:03:00Z', date: '2026-10-04', session: 'S3', skipped: true, speaker_matched: false, reason: 'spotlight', lines: 1 },
  ];
  const s = summarizeWakes(recs);
  assert.deepEqual(s.total, { wakes: 2, failed: 0, lines: 5, skipped: 3, paused: 0, budget_held: 0, rate_limited: 0, attempts: 2, overrides: 1, saved_upper_bound: 3 });
  assert.deepEqual(s.by_day.map((d) => [d.date, d.wakes, d.skipped, d.overrides, d.saved_upper_bound]), [['2026-10-03', 1, 0, 0, 0], ['2026-10-04', 1, 3, 1, 3]]);
  assert.deepEqual(s.by_session.map((d) => [d.session, d.wakes, d.skipped]), [['S1', 1, 0], ['S2', 1, 2], ['S3', 0, 1]]);
});
