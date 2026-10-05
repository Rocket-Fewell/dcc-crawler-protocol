import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { PassThrough } from 'node:stream';
import { test } from 'node:test';
import { AudioPlayerStatus } from '@discordjs/voice';
import { PermissionFlagsBits } from 'discord.js';
import { commandData } from '../src/commands/index.js';
import * as voicecap from '../src/commands/voicecap.js';
import * as sayCmd from '../src/commands/say.js';
import { loadConfig } from '../src/config.js';
import { SpeechQueue } from '../src/queue.js';
import { SessionVoiceCap } from '../src/sessioncap.js';
import { GmOutputBridge } from '../src/tts.js';
import { SessionCapError, UsageLogger, WakeUsageLogger, meteredSynthesize, parseWakeJsonl, summarizeWakes } from '../src/usage.js';

const quiet = { debug() {}, info() {}, warn() {}, error() {} };
const env = {
  DISCORD_TOKEN: 'x.y.z', CLIENT_ID: '111111111111111111', GUILD_ID: '222222222222222222',
  TRANSCRIPT_CHANNEL_ID: '444444444444444444', GM_OUTPUT_CHANNEL_ID: '555555555555555555', OPENAI_API_KEY: 'sk-test',
};
const tmp = () => mkdtempSync(path.join(tmpdir(), 'cap-'));

/** Fake provider: 900 chars = 1 minute (the default estimate). Counts real synth calls ("spend"). */
function fakeProvider({ stream = false, fail = false } = {}) {
  const p = {
    id: 'fish', calls: 0,
    modelFor: () => 'm',
    async synthesize(text) {
      p.calls++;
      if (fail) throw new Error('boom');
      if (!stream) return Buffer.from(text);
      const s = new PassThrough();
      s.usage = new Promise((resolve) => s.on('end', () => resolve({ ok: true, audioSeconds: null })));
      s.end(text);
      s.resume();
      return s;
    },
  };
  return p;
}
const mins = (n) => 'x'.repeat(n * 900); // text worth n estimated minutes

// ------------------------------------------------------------------ config

test('config: FISH_SESSION_CAP_MINUTES defaults to 50, 0 disables, override works', () => {
  assert.equal(loadConfig(env).usage.sessionCapMinutes, 50);
  assert.equal(loadConfig({ ...env, FISH_SESSION_CAP_MINUTES: '0' }).usage.sessionCapMinutes, 0);
  assert.equal(loadConfig({ ...env, FISH_SESSION_CAP_MINUTES: '12.5' }).usage.sessionCapMinutes, 12.5);
  assert.equal(loadConfig({ ...env, FISH_SESSION_CAP_MINUTES: '-3' }).usage.sessionCapMinutes, 0);
  assert.throws(() => loadConfig({ ...env, FISH_SESSION_CAP_MINUTES: 'lots' }), /FISH_SESSION_CAP_MINUTES/);
  const u = loadConfig(env).usage;
  assert.ok(u.wakeLogPath.endsWith(path.join('logs', 'wake-usage.jsonl')) && u.wakeLogEnabled === true);
});

// ------------------------------------------------------------------ counter

test('SessionVoiceCap: warns once at 80%, blocks at 100%, notice only once, reset re-arms', () => {
  const events = [];
  const cap = new SessionVoiceCap({ capMinutes: 10, logger: quiet, onWarn: (s) => events.push(['warn', Math.round(s.percent)]), onReached: () => events.push(['reached']) });
  cap.settle(0, 7.9);
  assert.equal(events.length, 0);
  cap.settle(0, 0.1); // 8.0 => 80%
  cap.settle(0, 0.5);
  assert.deepEqual(events, [['warn', 80]], 'warn fires once');
  assert.equal(cap.isReached(), false);
  cap.settle(0, 1.5);
  assert.equal(cap.isReached(), true);
  cap.block();
  cap.block();
  cap.block();
  assert.deepEqual(events.filter((e) => e[0] === 'reached').length, 1, 'notice only once per session');
  cap.reset();
  assert.equal(cap.used, 0);
  assert.equal(cap.isReached(), false);
  cap.settle(0, 10);
  cap.block();
  assert.deepEqual(events.map((e) => e[0]), ['warn', 'reached', 'warn', 'reached'], 're-armed after reset');
});

test('SessionVoiceCap: cap 0 never blocks; setCap raises the limit; callbacks that throw are contained', async () => {
  const off = new SessionVoiceCap({ capMinutes: 0, logger: quiet });
  off.settle(0, 9999);
  assert.equal(off.isReached(), false);
  assert.equal(off.status().percent, null);
  const cap = new SessionVoiceCap({ capMinutes: 1, logger: quiet, onWarn: () => { throw new Error('x'); }, onReached: async () => { throw new Error('y'); } });
  cap.settle(0, 2);
  cap.block();
  await new Promise((r) => setTimeout(r, 10)); // no unhandled rejection
  assert.equal(cap.isReached(), true);
  cap.setCap(5);
  assert.equal(cap.isReached(), false);
  assert.equal(cap.status().cap, 5);
});

// ------------------------------------------------------------------ metered synthesizer

test('meteredSynthesize: counts logged minutes; once the cap is reached the provider is NOT called', async () => {
  const dir = tmp();
  try {
    const usage = new UsageLogger({ path: path.join(dir, 'u.jsonl'), logger: quiet });
    const provider = fakeProvider();
    let notices = 0;
    const cap = new SessionVoiceCap({ capMinutes: 2, logger: quiet, onReached: () => notices++ });
    const synth = meteredSynthesize(provider, usage, cap);
    await synth(mins(1), 'gm');
    assert.equal(cap.used, 1);
    await synth(mins(1), 'gm');
    assert.equal(cap.used, 2);
    assert.equal(provider.calls, 2);
    await assert.rejects(synth('more', 'gm'), (e) => e instanceof SessionCapError && e.code === 'SESSION_CAP');
    await assert.rejects(synth('more', 'gm'), SessionCapError);
    assert.equal(provider.calls, 2, 'no further provider spend');
    assert.equal(notices, 1);
    const rows = readFileSync(path.join(dir, 'u.jsonl'), 'utf8').trim().split('\n').map(JSON.parse);
    assert.equal(rows.length, 2, 'blocked attempts are not logged as usage');
    assert.equal(rows.reduce((a, r) => a + r.minutes, 0), cap.used, 'cap counter == sum of logged minutes');
  } finally {
    rmSync(dir, { recursive: true });
  }
});

test('meteredSynthesize: reservation makes prefetched chunks count immediately; failures release it', async () => {
  const usage = new UsageLogger({ path: '/dev/null', enabled: false, logger: quiet });
  const slow = fakeProvider();
  const cap = new SessionVoiceCap({ capMinutes: 3, logger: quiet });
  let release;
  slow.synthesize = () => new Promise((r) => (release = () => r(Buffer.from('x'))));
  const synth = meteredSynthesize(slow, usage, cap);
  const first = synth(mins(3), 'gm'); // still synthesizing
  assert.equal(cap.used, 3, 'estimate reserved up front');
  assert.equal(cap.isReached(), true);
  await assert.rejects(synth('x', 'gm'), SessionCapError);
  release();
  await first;
  assert.equal(cap.used, 3, 'reservation replaced by the logged estimate (no double count)');

  const bad = new SessionVoiceCap({ capMinutes: 3, logger: quiet });
  await assert.rejects(meteredSynthesize(fakeProvider({ fail: true }), usage, bad)(mins(2), 'gm'), /boom/);
  assert.equal(bad.used, 0, 'failed synthesis costs nothing');
});

test('meteredSynthesize: streaming provider settles when the stream finishes', async () => {
  const usage = new UsageLogger({ path: '/dev/null', enabled: false, logger: quiet });
  const cap = new SessionVoiceCap({ capMinutes: 10, logger: quiet });
  const stream = await meteredSynthesize(fakeProvider({ stream: true }), usage, cap)(mins(2), 'gm');
  await stream.usage;
  await new Promise((r) => setImmediate(r));
  assert.equal(cap.used, 2);
  assert.equal(cap.reserved, 0);
});

test('queue: a SESSION_CAP refusal drops the chunk quietly (no error log) and does not wedge', async () => {
  const errors = [];
  const player = Object.assign(new EventEmitter(), { state: { status: AudioPlayerStatus.Idle }, stop() {}, play() {} });
  const q = new SpeechQueue({
    player, prefetch: 2, logger: { ...quiet, error: (m) => errors.push(m) },
    synthesize: async () => { throw new SessionCapError(); },
  });
  q.enqueue(['a', 'b']);
  await new Promise((r) => setTimeout(r, 30));
  assert.equal(q.size, 0);
  assert.deepEqual(errors, []);
});

// ------------------------------------------------------------------ GM bridge + commands

test('GM output: at the cap nothing is enqueued, notice fires once; [ROLL]-only messages never trigger it', async () => {
  const enqueued = [];
  let notices = 0;
  const cap = new SessionVoiceCap({ capMinutes: 1, logger: quiet, onReached: () => notices++ });
  const bridge = new GmOutputBridge({
    client: { user: { id: 'bot' } }, config: loadConfig(env), session: { isConnected: true },
    queue: { enqueue: (c) => enqueued.push(c) }, logger: quiet, sessionCap: cap,
  });
  const msg = (content) => ({ guildId: env.GUILD_ID, channelId: env.GM_OUTPUT_CHANNEL_ID, id: '1', author: { id: 'gm' }, cleanContent: content, content, embeds: [] });
  await bridge.handle(msg('Before the cap.'));
  assert.equal(enqueued.length, 1);
  cap.settle(0, 1);
  await bridge.handle(msg('[ROLL] 1d20 = 4'));
  assert.equal(notices, 0);
  await bridge.handle(msg('After the cap.'));
  await bridge.handle(msg('And again.'));
  assert.equal(enqueued.length, 1);
  assert.equal(notices, 1);
  cap.reset(); // new /join
  await bridge.handle(msg('Fresh session.'));
  assert.equal(enqueued.length, 2);
});

function fakeInteraction({ options = {}, manage = false, owner = false } = {}) {
  const replies = [];
  return {
    replies,
    user: { id: 'u1' },
    guild: { ownerId: owner ? 'u1' : 'someone' },
    memberPermissions: { has: (bit) => manage && bit === PermissionFlagsBits.ManageGuild },
    options: { getString: (k) => options[k] ?? null, getNumber: (k) => options[k] ?? null },
    reply: async (r) => replies.push(r.content),
  };
}

test('/voicecap: registered, shows used/cap, reset + set need Manage Server (or owner)', async () => {
  assert.ok(commandData.some((c) => c.name === 'voicecap'));
  const cap = new SessionVoiceCap({ capMinutes: 50, logger: quiet });
  cap.settle(0, 12.34);
  const ctx = { sessionCap: cap, logger: quiet };

  let i = fakeInteraction();
  await voicecap.execute(i, ctx);
  assert.match(i.replies[0], /12\.3 \/ 50\.0 min used \(25%\), 37\.7 min left/);

  i = fakeInteraction({ options: { action: 'reset' } });
  await voicecap.execute(i, ctx);
  assert.match(i.replies[0], /Manage Server/);
  assert.equal(cap.used > 12, true, 'unauthorised reset ignored');

  i = fakeInteraction({ options: { action: 'reset' }, manage: true });
  await voicecap.execute(i, ctx);
  assert.equal(cap.used, 0);
  assert.match(i.replies[0], /Reset/);

  cap.settle(0, 49);
  i = fakeInteraction({ options: { action: 'set', minutes: 90 }, owner: true });
  await voicecap.execute(i, ctx);
  assert.equal(cap.status().cap, 90);
  assert.match(i.replies[0], /49\.0 \/ 90\.0/);

  i = fakeInteraction({ options: { action: 'set' }, manage: true });
  await voicecap.execute(i, ctx);
  assert.match(i.replies[0], /minutes/);
  assert.equal(cap.status().cap, 90);

  i = fakeInteraction({ options: { action: 'set', minutes: 0 }, manage: true });
  await voicecap.execute(i, ctx);
  assert.equal(cap.enabled, false);
  i = fakeInteraction();
  await voicecap.execute(i, ctx);
  assert.match(i.replies[0], /no cap/);
});

test('/say is refused (and the notice fires once) at the cap', async () => {
  const cap = new SessionVoiceCap({ capMinutes: 1, logger: quiet });
  cap.settle(0, 1);
  const enqueued = [];
  const i = fakeInteraction({ options: { text: 'hello' } });
  await sayCmd.execute(i, {
    config: loadConfig(env), session: { isConnected: true }, queue: { enqueue: (c) => enqueued.push(c) }, sessionCap: cap,
  });
  assert.equal(enqueued.length, 0);
  assert.match(i.replies[0], /cap is reached/);
});

// ------------------------------------------------------------------ wake counting

test('WakeUsageLogger writes one JSONL line per wake; summarizeWakes groups by day and session', () => {
  const dir = tmp();
  try {
    const file = path.join(dir, 'logs', 'wake-usage.jsonl');
    const log = new WakeUsageLogger({ path: file, session: 'S1', logger: quiet });
    log.record({ lines: 3, ok: true, status: 200, now: new Date(2026, 9, 3, 20, 0, 0) });
    log.record({ lines: 1, ok: false, status: 500, now: new Date(2026, 9, 3, 21, 0, 0) });
    new WakeUsageLogger({ path: file, session: 'S2', logger: quiet }).record({ lines: 2, now: new Date(2026, 9, 4, 1, 0, 0) });
    new WakeUsageLogger({ path: file, enabled: false, logger: quiet }).record({ lines: 9 });
    const raw = readFileSync(file, 'utf8');
    assert.equal(raw.trim().split('\n').length, 3);
    const first = JSON.parse(raw.split('\n')[0]);
    assert.deepEqual(Object.keys(first), ['ts', 'date', 'session', 'dcc_session', 'lines', 'ok', 'status', 'overrides', 'attempts']);
    assert.equal(first.lines, 3);
    assert.ok(!Number.isNaN(Date.parse(first.ts)));
    const { records, bad } = parseWakeJsonl(`${raw}garbage\n{"x":1}\n`);
    assert.equal(records.length, 3);
    assert.equal(bad, 2);
    const s = summarizeWakes(records);
    assert.deepEqual(s.total, { wakes: 3, failed: 1, lines: 6, skipped: 0, paused: 0, budget_held: 0, rate_limited: 0, attempts: 3, overrides: 0, saved_upper_bound: 0 });
    assert.deepEqual(s.by_day.map((d) => [d.date, d.wakes, d.failed, d.lines]), [['2026-10-03', 2, 1, 4], ['2026-10-04', 1, 0, 2]]);
    assert.deepEqual(s.by_session.map((r) => [r.session, r.date, r.wakes]), [['S1', '2026-10-03', 2], ['S2', '2026-10-04', 1]]);
    assert.equal(summarizeWakes(records, { month: '2026-09' }).total.wakes, 0);
    // unwritable path (a file used as a directory) never throws
    assert.doesNotThrow(() => new WakeUsageLogger({ path: path.join(file, 'sub', 'x.jsonl'), logger: quiet }).record({ lines: 1 }));
  } finally {
    rmSync(dir, { recursive: true });
  }
});

test('npm run usage reports wake-ups per day and session', () => {
  const dir = tmp();
  try {
    const wakeFile = path.join(dir, 'w.jsonl');
    writeFileSync(
      wakeFile,
      [
        { ts: '2026-10-03T20:00:00.000Z', date: '2026-10-03', session: 'S1', lines: 3, ok: true, status: 200 },
        { ts: '2026-10-03T20:05:00.000Z', date: '2026-10-03', session: 'S1', lines: 1, ok: true, status: 200 },
      ].map((r) => JSON.stringify(r)).join('\n') + '\n'
    );
    const run = (...args) => spawnSync(process.execPath, ['scripts/tts-usage-summary.js', '--file', path.join(dir, 'none.jsonl'), '--wake-file', wakeFile, ...args], { encoding: 'utf8', cwd: path.join(import.meta.dirname, '..') });
    const r = run();
    assert.equal(r.status, 0, r.stderr);
    assert.match(r.stdout, /GM wake-ups by day/);
    assert.match(r.stdout, /2026-10-03\s+2\s+0\s+0\s+4\s+0\s+0\s+0\s+0\s+0/);
    assert.match(r.stdout, /S1\s+2026-10-03\s+2/);
    assert.match(r.stdout, /Total: 2 wake\(s\) fired \(0 failed\) for 4 transcript line/);
    assert.match(r.stdout, /UPPER BOUND/);
    const j = JSON.parse(run('--json').stdout);
    assert.equal(j.wakes.total.wakes, 2);
    assert.equal(j.wakes.by_day[0].date, '2026-10-03');
  } finally {
    rmSync(dir, { recursive: true });
  }
});
