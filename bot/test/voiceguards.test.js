import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import { spawnSync } from 'node:child_process';
import http from 'node:http';
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { AudioPlayerStatus } from '@discordjs/voice';
import * as gmCmd from '../src/commands/gm.js';
import { commandData } from '../src/commands/index.js';
import * as shushCmd from '../src/commands/shush.js';
import * as skipCmd from '../src/commands/skip.js';
import { loadConfig, loadWakeConfig } from '../src/config.js';
import { DuplicateGuard, compareTexts, normalizeForDedupe } from '../src/dedupe.js';
import { GmWakeState } from '../src/gmpause.js';
import { SpeechQueue } from '../src/queue.js';
import { GmOutputBridge } from '../src/tts.js';
import { VoiceEventLogger, WakeUsageLogger, parseEventsJsonl, summarizeVoiceEvents, summarizeWakes } from '../src/usage.js';
import { VoiceControlWatcher, readControl } from '../src/voicecontrol.js';
import { GmWakeNotifier } from '../src/wake.js';

const quiet = { debug() {}, info() {}, warn() {}, error() {} };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const tmp = () => mkdtempSync(path.join(tmpdir(), 'vg-'));
const env = {
  DISCORD_TOKEN: 'x.y.z', CLIENT_ID: '111111111111111111', GUILD_ID: '222222222222222222',
  TRANSCRIPT_CHANNEL_ID: '444444444444444444', GM_OUTPUT_CHANNEL_ID: '555555555555555555', OPENAI_API_KEY: 'sk-test',
};

// ------------------------------------------------------------------ config

test('config: voice protections defaults and overrides', () => {
  const v = loadConfig(env).voice;
  assert.equal(v.duplicateWindowSeconds, 120);
  assert.equal(v.maxQueuedChunks, 12);
  assert.equal(v.maxQueuedSeconds, 90);
  assert.equal(v.controlEnabled, true);
  assert.equal(v.controlFile, '/workspace/dcc-campaign/sessions/voice-control.json');
  const o = loadConfig({ ...env, DUPLICATE_WINDOW_SECONDS: '0', MAX_QUEUED_CHUNKS: '5', MAX_QUEUED_SECONDS: '30', VOICE_CONTROL_FILE: '/tmp/vc.json', VOICE_CONTROL_ENABLED: 'false' }).voice;
  assert.deepEqual([o.duplicateWindowSeconds, o.maxQueuedChunks, o.maxQueuedSeconds, o.controlFile, o.controlEnabled], [0, 5, 30, '/tmp/vc.json', false]);
  assert.ok(loadConfig(env).gmWakeStateFile.endsWith(path.join('logs', 'gm-wake-state.json')));
});

// ------------------------------------------------------------------ duplicate suppression

test('dedupe: normalization and near-identical rule (containment + >90%)', () => {
  assert.equal(normalizeForDedupe('  The   DOOR\nopens '), 'the door opens');
  assert.equal(compareTexts('abc def', 'abc def'), 'exact');
  const base = 'the goblin lunges at you with a rusty knife and you feel the wind of the blade pass your ear';
  assert.equal(compareTexts(base, `${base} now`), 'near'); // prefix, 96% similar
  assert.equal(compareTexts(`well, ${base}`, base), 'near'); // contained
  assert.equal(compareTexts(base.slice(0, 60), base), null, 'a short prefix (<90%) is not a duplicate');
  assert.equal(compareTexts('hello there', 'goodbye now'), null);
  assert.equal(compareTexts('', 'x'), null);
});

test('DuplicateGuard: same author within the window only; expires; clear(); disabled at 0', () => {
  let t = 1_000_000;
  const g = new DuplicateGuard({ windowSeconds: 120, now: () => t });
  assert.equal(g.check('gm', 'Hello world').duplicate, false);
  g.remember('gm', 'Hello world');
  const d = g.check('gm', '  hello   WORLD ');
  assert.deepEqual([d.duplicate, d.kind], [true, 'exact']);
  assert.equal(g.check('someone-else', 'Hello world').duplicate, false, 'different author is never a duplicate');
  t += 119_000;
  assert.equal(g.check('gm', 'hello world').duplicate, true);
  t += 2_000;
  assert.equal(g.check('gm', 'hello world').duplicate, false, 'outside the window');
  g.remember('gm', 'again');
  g.clear();
  assert.equal(g.check('gm', 'again').duplicate, false);
  const off = new DuplicateGuard({ windowSeconds: 0 });
  off.remember('gm', 'x');
  assert.equal(off.check('gm', 'x').duplicate, false);
});

function bridgeFor({ dedupe, events, enqueue }) {
  return new GmOutputBridge({
    client: { user: { id: 'bot' } }, config: loadConfig(env), session: { isConnected: true },
    queue: { enqueue }, logger: quiet, dedupe, events,
  });
}
const gmMsg = (content, id = '1', author = 'gm1') => ({ guildId: env.GUILD_ID, channelId: env.GM_OUTPUT_CHANNEL_ID, id, author: { id: author, tag: 'GM#1' }, cleanContent: content, content, embeds: [] });

test('GmOutputBridge drops duplicates (logged + counted), keeps different/other-author messages', async () => {
  const dir = tmp();
  try {
    const enq = [];
    const events = new VoiceEventLogger({ path: path.join(dir, 'ev.jsonl'), session: 'S1' });
    let gid = 0;
    const b = bridgeFor({ dedupe: new DuplicateGuard({ windowSeconds: 120 }), events, enqueue: (c) => (enq.push(c), ++gid) });
    await b.handle(gmMsg('The door creaks open.', '1'));
    await b.handle(gmMsg('the  DOOR creaks open.', '2')); // duplicate
    await b.handle(gmMsg('[GM] The door creaks open.', '3')); // same speakable text, different tag syntax => duplicate
    await b.handle(gmMsg('A new thing happens.', '4'));
    await b.handle(gmMsg('The door creaks open.', '5', 'other-gm')); // other author => spoken
    assert.equal(enq.length, 3);
    const rows = readFileSync(path.join(dir, 'ev.jsonl'), 'utf8').trim().split('\n').map(JSON.parse);
    assert.deepEqual(rows.map((r) => [r.type, r.kind]), [['duplicate_dropped', 'exact'], ['duplicate_dropped', 'exact']]);
    assert.ok(!JSON.stringify(rows).includes('creaks'), 'no message text in the events log');
    const s = summarizeVoiceEvents(parseEventsJsonl(readFileSync(path.join(dir, 'ev.jsonl'), 'utf8')).records);
    assert.equal(s.total.duplicates, 2);
  } finally {
    rmSync(dir, { recursive: true });
  }
});

test('GmOutputBridge: a message that was never queued is not remembered (cap/disabled queue)', async () => {
  const enq = [];
  const b = bridgeFor({ dedupe: new DuplicateGuard({ windowSeconds: 120 }), enqueue: (c) => (enq.push(c), 0) });
  await b.handle(gmMsg('Same text.', '1'));
  await b.handle(gmMsg('Same text.', '2'));
  assert.equal(enq.length, 2);
});

// ------------------------------------------------------------------ backlog safeguard

function fakePlayer() {
  const p = new EventEmitter();
  p.state = { status: AudioPlayerStatus.Idle };
  p.stops = 0;
  p.play = () => {};
  p.stop = () => { p.stops++; return true; };
  return p;
}
function blockedQueue(opts) {
  // synth never resolves: nothing starts playing, so everything stays pending (head is "synthesizing")
  const drops = [];
  const q = new SpeechQueue({ player: fakePlayer(), logger: quiet, synthesize: () => new Promise(() => {}), onBacklogDrop: (d) => drops.push(d), ...opts });
  return { q, drops };
}

test('backlog: more than MAX chunks drops the oldest pending messages and keeps the newest', () => {
  const { q, drops } = blockedQueue({ maxChunks: 5, maxSeconds: 0 });
  q.enqueue(['playing']); // becomes the current chunk (its synth never finishes)
  q.enqueue(['m1a', 'm1b']);
  q.enqueue(['m2a', 'm2b']);
  assert.equal(drops.length, 0);
  assert.equal(q.items.length, 4);
  q.enqueue(['m3a', 'm3b']); // 6 pending > 5 => drop the oldest pending message (m1)
  const texts = () => q.items.map((i) => i.text);
  assert.deepEqual(drops, [{ messages: 1, chunks: 2 }]);
  assert.deepEqual(texts(), ['m2a', 'm2b', 'm3a', 'm3b']);
  q.enqueue(['m4a', 'm4b', 'm4c', 'm4d']); // 8 pending > 5 => drops m2 (4 pending... still 8-2=6>5) then m3
  assert.deepEqual(texts(), ['m4a', 'm4b', 'm4c', 'm4d']);
  assert.deepEqual(drops.at(-1), { messages: 2, chunks: 4 });
  assert.equal(q.current.text, 'playing', 'the chunk being played is never dropped');
});

test('backlog: a single huge newest message is kept whole; the playing message is protected', () => {
  const { q, drops } = blockedQueue({ maxChunks: 3, maxSeconds: 0 });
  q.enqueue(['p']);
  q.enqueue(['a1', 'a2']);
  q.enqueue(['b1', 'b2', 'b3', 'b4', 'b5']);
  assert.deepEqual(drops, [{ messages: 1, chunks: 2 }]);
  assert.deepEqual(q.items.map((i) => i.text), ['b1', 'b2', 'b3', 'b4', 'b5'], 'newest kept even though it alone exceeds the limit');
  // remaining chunks of the message currently being spoken are protected
  const { q: q2, drops: d2 } = blockedQueue({ maxChunks: 2 });
  q2.enqueue(['c1', 'c2', 'c3']); // c1 current, c2/c3 pending (same group)
  q2.enqueue(['d1', 'd2']);
  assert.equal(d2.length, 0, 'nothing droppable except the playing message and the newest');
  assert.deepEqual(q2.items.map((i) => i.text), ['c2', 'c3', 'd1', 'd2']);
});

test('backlog: audio-seconds limit (chars / charsPerMinute) trims oldest pending; dropped prefetched synth results are discarded', async () => {
  const discarded = [];
  const q = new SpeechQueue({
    player: fakePlayer(), logger: quiet, maxChunks: 0, maxSeconds: 90, charsPerMinute: 900, prefetch: 3,
    synthesize: async (text) => (text === 'playing' ? new Promise(() => {}) : { destroy: () => discarded.push(text) }),
    onBacklogDrop: () => {},
  });
  q.enqueue(['playing']);
  q.enqueue(['x'.repeat(600)]); // 40 s pending
  q.enqueue(['y'.repeat(600)]); // 80 s pending
  await sleep(10); // prefetch finished for x and y
  assert.equal(q.items.length, 2);
  q.enqueue(['z'.repeat(300)]); // 100 s pending => drop the oldest (x)
  assert.deepEqual(q.items.map((i) => i.text[0]), ['y', 'z']);
  assert.ok(q.pendingSeconds <= 90);
  await sleep(10);
  assert.deepEqual(discarded.map((t) => t[0]), ['x'], 'cancelled prefetch result released');
});

test('backlog off (0/0): nothing is ever dropped', () => {
  const { q, drops } = blockedQueue({ maxChunks: 0, maxSeconds: 0 });
  for (let i = 0; i < 30; i++) q.enqueue([`m${i}`]);
  assert.equal(drops.length, 0);
});

test('backlog callback errors never break enqueue', () => {
  const q = new SpeechQueue({ player: fakePlayer(), logger: quiet, maxChunks: 1, synthesize: () => new Promise(() => {}), onBacklogDrop: () => { throw new Error('x'); } });
  q.enqueue(['a']);
  q.enqueue(['b']);
  assert.doesNotThrow(() => q.enqueue(['c']));
});

// ------------------------------------------------------------------ kill switch file

test('voice control file: new id flushes; baseline id at startup does not; bad files are ignored', () => {
  const dir = tmp();
  try {
    const file = path.join(dir, 'voice-control.json');
    writeFileSync(file, JSON.stringify({ action: 'flush', id: 'old', ts: 'x' }));
    const flushes = [];
    const w = new VoiceControlWatcher({ file, logger: quiet, onFlush: (i) => flushes.push(i.id) });
    w.start();
    w.stop();
    assert.equal(w.poll(), false, 'stale id present at startup is not acted on');
    writeFileSync(file, JSON.stringify({ action: 'flush', id: 'new-1', ts: 'x' }));
    assert.equal(w.poll(), true);
    assert.equal(w.poll(), false, 'same id only once');
    writeFileSync(file, '{broken');
    assert.equal(w.poll(), false);
    writeFileSync(file, JSON.stringify({ action: 'explode', id: 'new-2' }));
    assert.equal(w.poll(), false, 'unknown action ignored');
    writeFileSync(file, JSON.stringify({ action: 'flush', id: 'new-3' }));
    assert.equal(w.poll(), true);
    assert.deepEqual(flushes, ['new-1', 'new-3']);
    assert.equal(readControl(path.join(dir, 'missing.json')), null);
    // throwing handler is contained
    const w2 = new VoiceControlWatcher({ file, logger: quiet, onFlush: () => { throw new Error('x'); } });
    w2.lastId = 'zzz';
    assert.doesNotThrow(() => w2.poll());
  } finally {
    rmSync(dir, { recursive: true });
  }
});

test('voice control file: missing at startup then created => flush; real interval polling works', async () => {
  const dir = tmp();
  try {
    const file = path.join(dir, 'vc.json');
    const flushes = [];
    const w = new VoiceControlWatcher({ file, logger: quiet, pollMs: 20, onFlush: (i) => flushes.push(i.id) }).start();
    await sleep(60);
    writeFileSync(file, JSON.stringify({ action: 'flush', id: 'abc', ts: new Date().toISOString() }));
    for (let i = 0; i < 50 && !flushes.length; i++) await sleep(20);
    w.stop();
    assert.deepEqual(flushes, ['abc']);
  } finally {
    rmSync(dir, { recursive: true });
  }
});

test('python `discord_gm.py stop` output is understood by the watcher (cross-tool contract)', () => {
  const py = '/workspace/dcc-campaign/tools/discord_gm.py';
  if (!existsSync(py)) return;
  const dir = tmp();
  try {
    const file = path.join(dir, 'vc.json');
    const flushes = [];
    const w = new VoiceControlWatcher({ file, logger: quiet, onFlush: (i) => flushes.push(i.id) });
    w.start();
    w.stop();
    const r = spawnSync('python3', [py, 'stop'], { env: { PATH: process.env.PATH, VOICE_CONTROL_FILE: file }, encoding: 'utf8' });
    assert.equal(r.status, 0, r.stderr);
    assert.equal(w.poll(), true);
    assert.equal(flushes.length, 1);
    spawnSync('python3', [py, 'stop'], { env: { PATH: process.env.PATH, VOICE_CONTROL_FILE: file } });
    assert.equal(w.poll(), true, 'each stop is a new event');
  } finally {
    rmSync(dir, { recursive: true });
  }
});

// ------------------------------------------------------------------ /shush, /skip

function interaction(options = {}) {
  const replies = [];
  return { replies, user: { id: 'u1' }, options: { getString: (k) => options[k] ?? null, getBoolean: (k) => options[k] ?? null }, reply: async (r) => replies.push(r) };
}

test('/shush: anyone; stops playback, clears the queue, forgets dedupe history, mentions /gm pause; ephemeral', async () => {
  const player = fakePlayer();
  const q = new SpeechQueue({ player, logger: quiet, synthesize: async () => { await sleep(20); return Buffer.alloc(0); } });
  q.enqueue(['a', 'b']);
  q.enqueue(['c']);
  const dedupe = new DuplicateGuard({ windowSeconds: 120 });
  dedupe.remember('gm', 'something');
  const events = [];
  const flushVoice = (source) => {
    const n = q.clear();
    player.stop(true);
    dedupe.clear();
    events.push(source);
    return n;
  };
  const i = interaction();
  await shushCmd.execute(i, { flushVoice, logger: quiet });
  assert.equal(q.items.length, 0);
  assert.equal(q.current?.cancelled ?? true, true, 'the playing chunk is cancelled');
  assert.ok(player.stops >= 1);
  assert.equal(dedupe.check('gm', 'something').duplicate, false);
  assert.deepEqual(events, ['shush']);
  assert.match(i.replies[0].content, /cleared \(\d+ chunks?\)/);
  assert.match(i.replies[0].content, /\/gm pause/);
  assert.ok(i.replies[0].flags, 'ephemeral');
  assert.equal(shushCmd.data.toJSON().default_member_permissions ?? null, null, 'no permission restriction');
  assert.ok(commandData.some((c) => c.name === 'shush') && commandData.some((c) => c.name === 'gm'));
});

test('/skip clears dedupe history only when something was skipped', async () => {
  const dedupe = new DuplicateGuard({ windowSeconds: 120 });
  dedupe.remember('gm', 'x');
  await skipCmd.execute(interaction({ all: false }), { queue: { skip: () => 0 }, dedupe });
  assert.equal(dedupe.check('gm', 'x').duplicate, true);
  await skipCmd.execute(interaction({ all: false }), { queue: { skip: () => 2 }, dedupe });
  assert.equal(dedupe.check('gm', 'x').duplicate, false);
});

// ------------------------------------------------------------------ /gm pause|resume|status

test('GmWakeState persists across restarts, defaults to running, survives a bad file', () => {
  const dir = tmp();
  try {
    const file = path.join(dir, 'sub', 'gm-wake-state.json');
    assert.equal(new GmWakeState({ file }).paused, false);
    const s = new GmWakeState({ file, logger: quiet });
    s.set(true, 'u1');
    assert.equal(new GmWakeState({ file }).paused, true, 'paused survives a restart');
    assert.equal(new GmWakeState({ file }).by, 'u1');
    s.set(false, 'u2');
    assert.equal(new GmWakeState({ file }).paused, false);
    writeFileSync(file, '{garbage');
    assert.equal(new GmWakeState({ file }).paused, false);
    assert.doesNotThrow(() => new GmWakeState({ file: path.join(file, 'nope', 'x.json'), logger: quiet }).set(true)); // unwritable
    assert.equal(new GmWakeState({}).paused, false);
  } finally {
    rmSync(dir, { recursive: true });
  }
});

test('/gm command: choices, pause / resume / status replies (ephemeral, anyone)', async () => {
  const opts = gmCmd.data.toJSON().options[0];
  assert.deepEqual(opts.choices.map((c) => c.value), ['pause', 'resume', 'status']);
  assert.equal(gmCmd.data.toJSON().default_member_permissions ?? null, null);
  const dir = tmp();
  try {
    const gmState = new GmWakeState({ file: path.join(dir, 's.json'), logger: quiet });
    const ctx = { gmState, logger: quiet, config: { wake: { enabled: true }, spotlight: { enabled: false } } };
    let i = interaction({ action: 'status' });
    await gmCmd.execute(i, ctx);
    assert.match(i.replies[0].content, /GM wake: \*\*ON\*\*/);
    assert.match(i.replies[0].content, /Webhook: configured/);
    i = interaction({ action: 'pause' });
    await gmCmd.execute(i, ctx);
    assert.equal(gmState.paused, true);
    assert.match(i.replies[0].content, /Paused\./);
    assert.match(i.replies[0].content, /PAUSED/);
    assert.ok(i.replies[0].flags);
    i = interaction({ action: 'status' });
    await gmCmd.execute(i, ctx);
    assert.match(i.replies[0].content, /PAUSED/);
    i = interaction({ action: 'resume' });
    await gmCmd.execute(i, { ...ctx, config: { wake: { enabled: false }, spotlight: { enabled: false } } });
    assert.equal(gmState.paused, false);
    assert.match(i.replies[0].content, /NOT configured/);
  } finally {
    rmSync(dir, { recursive: true });
  }
});

// ------------------------------------------------------------------ paused wake

async function mockHook() {
  const reqs = [];
  const srv = http.createServer((req, res) => {
    req.resume();
    req.on('end', () => {
      reqs.push(1);
      res.end('ok');
    });
  });
  await new Promise((r) => srv.listen(0, '127.0.0.1', r));
  return { reqs, url: `http://127.0.0.1:${srv.address().port}/h`, close: () => { srv.closeAllConnections?.(); return new Promise((r) => srv.close(r)); } };
}
const wakeCfg = (url) => ({ ...loadWakeConfig({ GM_WEBHOOK_URL: url, GM_WEBHOOK_KEY: 'k' }), debounceMs: 50, maxWaitMs: 200, minIntervalMs: 0 });
const timing = { retryDelayMs: 10, pollMs: 10, timeoutMs: 2000 };

test('paused: no wake POST, lines counted as skipped reason "paused"; resume wakes again; pending lines dropped on pause', async () => {
  const dir = tmp();
  const m = await mockHook();
  try {
    const file = path.join(dir, 'w.jsonl');
    const usageLog = new WakeUsageLogger({ path: file, session: 'S1' });
    let paused = true;
    const n = new GmWakeNotifier({ wake: wakeCfg(m.url), logger: quiet, timing, usageLog, isPaused: () => paused });
    n.notify({ speaker: 'A', text: 'secret table talk' });
    n.notify({ speaker: 'B', text: 'more' });
    await sleep(250);
    assert.equal(m.reqs.length, 0);
    const rows = () => readFileSync(file, 'utf8').trim().split('\n').map(JSON.parse);
    assert.deepEqual(rows().map((r) => [r.skipped, r.reason, r.speaker_matched, r.lines]), [[true, 'paused', false, 1], [true, 'paused', false, 1]]);
    assert.ok(!JSON.stringify(rows()).includes('secret'));
    // resume
    paused = false;
    n.notify({ speaker: 'A', text: 'now awake' });
    for (let i = 0; i < 100 && !m.reqs.length; i++) await sleep(20);
    assert.equal(m.reqs.length, 1);
    // pause while a batch is waiting: it is dropped, not sent
    n.notify({ speaker: 'A', text: 'queued then paused' });
    paused = true;
    await sleep(300);
    assert.equal(m.reqs.length, 1);
    const last = rows().at(-1);
    assert.deepEqual([last.skipped, last.reason], [true, 'paused']);
    n.stop();
    const sum = summarizeWakes(rows());
    assert.equal(sum.total.paused, 3);
    assert.equal(sum.total.wakes, 1);
    assert.equal(sum.total.saved_upper_bound, 3);
    assert.equal(sum.total.skipped, 0);
  } finally {
    await m.close();
    rmSync(dir, { recursive: true });
  }
});

// ------------------------------------------------------------------ report

test('events summary + `npm run usage` reports duplicates, backlog drops, flushes and paused lines', () => {
  const dir = tmp();
  try {
    const ev = new VoiceEventLogger({ path: path.join(dir, 'ev.jsonl'), session: 'S1' });
    ev.record('duplicate_dropped', { kind: 'exact', age_s: 5, chars: 30 }, new Date(2026, 9, 4, 12));
    ev.record('duplicate_dropped', { kind: 'near', age_s: 9, chars: 30 }, new Date(2026, 9, 4, 12, 5));
    ev.record('backlog_dropped', { messages: 2, chunks: 5 }, new Date(2026, 9, 4, 13));
    ev.record('flush', { source: 'shush', chunks: 3 }, new Date(2026, 9, 5, 1));
    new VoiceEventLogger({ path: path.join(dir, 'ev.jsonl'), enabled: false }).record('flush');
    const { records, bad } = parseEventsJsonl(readFileSync(path.join(dir, 'ev.jsonl'), 'utf8') + 'junk\n');
    assert.deepEqual([records.length, bad], [4, 1]);
    const s = summarizeVoiceEvents(records);
    assert.deepEqual(s.total, { duplicates: 2, backlog_events: 1, backlog_messages: 2, backlog_chunks: 5, flushes: 1 });
    assert.deepEqual(s.by_day.map((d) => [d.date, d.duplicates, d.flushes]), [['2026-10-04', 2, 0], ['2026-10-05', 0, 1]]);

    const wakeFile = path.join(dir, 'w.jsonl');
    writeFileSync(wakeFile, [
      { ts: '2026-10-04T20:00:00Z', date: '2026-10-04', session: 'S1', lines: 2, ok: true, status: 200, overrides: 0 },
      { ts: '2026-10-04T20:01:00Z', date: '2026-10-04', session: 'S1', skipped: true, speaker_matched: false, reason: 'paused', lines: 1 },
      { ts: '2026-10-04T20:02:00Z', date: '2026-10-04', session: 'S1', skipped: true, speaker_matched: false, reason: 'spotlight', lines: 1 },
    ].map((r) => JSON.stringify(r)).join('\n') + '\n');
    const r = spawnSync(process.execPath, ['scripts/tts-usage-summary.js', '--file', path.join(dir, 'none'), '--wake-file', wakeFile, '--events-file', path.join(dir, 'ev.jsonl')], { encoding: 'utf8', cwd: path.join(import.meta.dirname, '..') });
    assert.equal(r.status, 0, r.stderr);
    assert.match(r.stdout, /2 duplicate GM message\(s\) dropped/);
    assert.match(r.stdout, /1 backlog trim\(s\) dropping 2 message\(s\) \/ 5 chunk\(s\); 1 flush/);
    assert.match(r.stdout, /1 line\(s\) skipped by the spotlight filter; 1 line\(s\) dropped while \/gm pause was on/);
    assert.match(r.stdout, /saved: <= 2|saved wake-ups: <= 2/i);
    const j = JSON.parse(spawnSync(process.execPath, ['scripts/tts-usage-summary.js', '--json', '--file', path.join(dir, 'none'), '--wake-file', wakeFile, '--events-file', path.join(dir, 'ev.jsonl')], { encoding: 'utf8', cwd: path.join(import.meta.dirname, '..') }).stdout);
    assert.equal(j.voice_events.total.duplicates, 2);
    assert.equal(j.wakes.total.paused, 1);
  } finally {
    rmSync(dir, { recursive: true });
  }
});
