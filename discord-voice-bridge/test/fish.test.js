import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { EventEmitter } from 'node:events';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import http from 'node:http';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { Readable } from 'node:stream';
import { test } from 'node:test';
import { loadConfig } from '../src/config.js';
import { SpeechQueue } from '../src/queue.js';
import { prepareSpeech } from '../src/text.js';
import { FishTts, createTtsProvider } from '../src/tts.js';
import { UsageLogger, meteredSynthesize, parseJsonl, summarize } from '../src/usage.js';

const SECRET = 'fish-SECRET-key-should-never-appear';
const env = {
  DISCORD_TOKEN: 't',
  CLIENT_ID: '111111111111111111',
  GUILD_ID: '222222222222222222',
  TRANSCRIPT_CHANNEL_ID: '444444444444444444',
  GM_OUTPUT_CHANNEL_ID: '555555555555555555',
  OPENAI_API_KEY: 'sk-test',
  TTS_PROVIDER: 'fish',
  FISH_API_KEY: SECRET,
  FISH_VOICE_ID_NARRATOR: 'narrator00112233445566778899aabb',
  FISH_VOICE_ID_SYSTEM: 'system0011223344556677889900cc',
};
const logger = { debug() {}, info() {}, warn() {}, error() {} };

/** Mock Fish Audio server. `handler(req, body, res)` can override the default reply. */
async function mockFish(handler) {
  const seen = [];
  const srv = http.createServer((req, res) => {
    let b = '';
    req.on('data', (d) => (b += d));
    req.on('end', () => {
      const entry = { method: req.method, url: req.url, headers: req.headers, body: b ? JSON.parse(b) : null };
      seen.push(entry);
      if (handler) return handler(entry, res, seen.length);
      res.setHeader('content-type', 'audio/mpeg');
      res.end(Buffer.alloc(16000, 1)); // 1 second of 128 kbps mp3
    });
  });
  await new Promise((r) => srv.listen(0, '127.0.0.1', r));
  return { seen, base: `http://127.0.0.1:${srv.address().port}`, close: () => new Promise((r) => srv.close(r)) };
}

const cfgFor = (base, extra = {}) => loadConfig({ ...env, FISH_BASE_URL: base, ...extra });
const drain = async (stream) => {
  const chunks = [];
  for await (const c of stream) chunks.push(c);
  return Buffer.concat(chunks);
};

test('config: fish provider selected, defaults and validation', () => {
  const c = loadConfig(env);
  assert.equal(c.tts.provider, 'fish');
  assert.equal(c.tts.fish.model, 's2.1-pro');
  assert.equal(c.tts.fish.latency, 'balanced');
  assert.equal(c.tts.fish.format, 'mp3');
  assert.equal(c.tts.fish.voices.gm.voiceId, env.FISH_VOICE_ID_NARRATOR);
  assert.equal(c.tts.fish.voices.system.voiceId, env.FISH_VOICE_ID_SYSTEM);
  assert.equal(c.tts.fish.voiceFallback, false);
  assert.equal(loadConfig({ ...env, FISH_MODEL: 's2.1-pro-free' }).tts.fish.model, 's2.1-pro-free');

  assert.throws(() => loadConfig({ ...env, FISH_API_KEY: '' }), /FISH_API_KEY/);
  assert.throws(() => loadConfig({ ...env, FISH_VOICE_ID_NARRATOR: '', FISH_VOICE_ID_SYSTEM: '' }), /FISH_VOICE_ID/);
  assert.throws(() => loadConfig({ ...env, FISH_LATENCY: 'warp' }), /FISH_LATENCY/);
  assert.throws(() => loadConfig({ ...env, FISH_FORMAT: 'flac' }), /FISH_FORMAT/);
  assert.throws(() => loadConfig({ ...env, FISH_MP3_BITRATE: '100' }), /FISH_MP3_BITRATE/);
  // openai/elevenlabs unaffected, no fish settings needed
  const { FISH_API_KEY, FISH_VOICE_ID_NARRATOR, FISH_VOICE_ID_SYSTEM, TTS_PROVIDER, ...rest } = env;
  assert.equal(loadConfig(rest).tts.provider, 'openai');
});

test('config: falls back to the other voice id when only one is set', () => {
  const onlyNarr = loadConfig({ ...env, FISH_VOICE_ID_SYSTEM: '' });
  assert.equal(onlyNarr.tts.fish.voices.system.voiceId, env.FISH_VOICE_ID_NARRATOR);
  assert.equal(onlyNarr.tts.fish.voiceFallback, true);
  const onlySys = loadConfig({ ...env, FISH_VOICE_ID_NARRATOR: '' });
  assert.equal(onlySys.tts.fish.voices.gm.voiceId, env.FISH_VOICE_ID_SYSTEM);
  assert.equal(onlySys.tts.fish.voiceFallback, true);
});

test('fish request: endpoint, auth + model headers, body, voice routing', async () => {
  const m = await mockFish();
  try {
    const p = createTtsProvider(cfgFor(m.base, { FISH_MODEL: 's2.1-pro-free', FISH_SPEED: '1.25', FISH_LATENCY: 'low' }));
    assert.ok(p instanceof FishTts);
    assert.equal(p.id, 'fish');
    assert.ok(!p.name.includes(SECRET));
    await drain(await p.synthesize('Welcome, crawler.', 'system'));
    await drain(await p.synthesize('The door creaks.', 'gm'));
    await drain(await p.synthesize('Untagged default.'));
    const [sys, gm, def] = m.seen;
    assert.equal(sys.method, 'POST');
    assert.equal(sys.url, '/v1/tts');
    assert.equal(sys.headers.authorization, `Bearer ${SECRET}`);
    assert.equal(sys.headers.model, 's2.1-pro-free');
    assert.equal(sys.headers['content-type'], 'application/json');
    assert.equal(sys.body.text, 'Welcome, crawler.');
    assert.equal(sys.body.reference_id, env.FISH_VOICE_ID_SYSTEM);
    assert.equal(sys.body.format, 'mp3');
    assert.equal(sys.body.mp3_bitrate, 128);
    assert.equal(sys.body.latency, 'low');
    assert.equal(sys.body.prosody.speed, 1.25);
    assert.equal(gm.body.reference_id, env.FISH_VOICE_ID_NARRATOR);
    assert.equal(def.body.reference_id, env.FISH_VOICE_ID_NARRATOR);
    assert.equal(p.modelFor('gm'), 's2.1-pro-free');
  } finally {
    await m.close();
  }
});

test('fish: single voice id is used for both voices', async () => {
  const m = await mockFish();
  try {
    const p = createTtsProvider(cfgFor(m.base, { FISH_VOICE_ID_SYSTEM: '' }));
    await drain(await p.synthesize('a', 'system'));
    await drain(await p.synthesize('b', 'gm'));
    assert.deepEqual(m.seen.map((s) => s.body.reference_id), [env.FISH_VOICE_ID_NARRATOR, env.FISH_VOICE_ID_NARRATOR]);
  } finally {
    await m.close();
  }
});

test('tag contract end to end: [SYSTEM] -> system id, [GM]/untagged -> narrator id, [ROLL] never sent', async () => {
  const m = await mockFish();
  try {
    const p = createTtsProvider(cfgFor(m.base));
    const chunks = prepareSpeech('Untagged intro.\n[SYSTEM] The floor collapses in 6 hours.\n[ROLL] d20 = 17\nsilent continuation\n[GM] The goblin snarls.');
    for (const c of chunks) await drain(await p.synthesize(c.text, c.voice));
    assert.deepEqual(
      m.seen.map((s) => [s.body.text, s.body.reference_id]),
      [
        ['Untagged intro.', env.FISH_VOICE_ID_NARRATOR],
        ['The floor collapses in 6 hours.', env.FISH_VOICE_ID_SYSTEM],
        ['The goblin snarls.', env.FISH_VOICE_ID_NARRATOR],
      ]
    );
    assert.ok(!m.seen.some((s) => /ROLL|d20|silent continuation/.test(s.body.text)));
  } finally {
    await m.close();
  }
});

test('fish streams: first audio is available before the response finishes', async () => {
  let release;
  const gate = new Promise((r) => (release = r));
  const m = await mockFish(async (_e, res) => {
    res.setHeader('content-type', 'audio/mpeg');
    res.write(Buffer.alloc(1000, 7)); // first chunk immediately
    await gate; // ...rest only when the test says so
    res.end(Buffer.alloc(1000, 8));
  });
  try {
    const p = createTtsProvider(cfgFor(m.base));
    const stream = await p.synthesize('Streaming test.', 'gm'); // resolves on headers, not on completion
    const first = await new Promise((resolve) => stream.once('data', resolve));
    assert.equal(first[0], 7);
    let done = false;
    stream.usage.then(() => (done = true));
    await new Promise((r) => setTimeout(r, 30));
    assert.equal(done, false, 'usage must settle only after the stream completes');
    release();
    const rest = await drain(stream);
    assert.ok(rest.length > 0);
    const u = await stream.usage;
    assert.equal(u.ok, true);
    assert.equal(u.bytes, 2000);
    assert.equal(u.audioSeconds, (2000 * 8) / 128000); // mp3 @128kbps => exact duration
  } finally {
    await m.close();
  }
});

test('fish errors: 401/402 are not retried, 429 and 503 are retried; key never leaks', async () => {
  for (const status of [401, 402]) {
    const m = await mockFish((_e, res) => {
      res.statusCode = status;
      res.setHeader('content-type', 'application/json');
      res.end(JSON.stringify({ status, message: `bad auth Bearer ${SECRET}` })); // even if the server echoed the key
    });
    try {
      const p = createTtsProvider(cfgFor(m.base));
      await assert.rejects(p.synthesize('x', 'gm'), (err) => {
        assert.match(err.message, new RegExp(`HTTP ${status}`));
        assert.ok(!err.message.includes(SECRET), 'API key leaked into error message');
        return true;
      });
      assert.equal(m.seen.length, 1);
    } finally {
      await m.close();
    }
  }
  const flaky = await mockFish((_e, res, n) => {
    if (n <= 2) {
      res.statusCode = n === 1 ? 429 : 503;
      return res.end('{"message":"busy"}');
    }
    res.end(Buffer.alloc(100, 1));
  });
  try {
    const p = createTtsProvider(cfgFor(flaky.base));
    const audio = await drain(await p.synthesize('x', 'gm'));
    assert.equal(audio.length, 100);
    assert.equal(flaky.seen.length, 3);
  } finally {
    await flaky.close();
  }
});

test('queue plays a streaming result and destroys a cancelled stream', async () => {
  const played = [];
  const player = Object.assign(new EventEmitter(), {
    state: { status: 'idle' },
    play(resource) {
      played.push(resource);
      setTimeout(() => this.emit('stateChange', { status: 'playing' }, { status: 'idle' }), 5);
    },
    stop() {
      this.emit('stateChange', { status: 'playing' }, { status: 'idle' });
    },
  });
  const streams = [];
  const q = new SpeechQueue({
    player,
    logger,
    prefetch: 2,
    synthesize: async (t) => {
      const s = Readable.from([Buffer.from(t)]);
      streams.push(s);
      return s;
    },
  });
  q.enqueue([{ text: 'one', voice: 'system' }]);
  await new Promise((r) => setTimeout(r, 50));
  assert.equal(played.length, 1);
  q.enqueue([{ text: 'two' }, { text: 'three' }]);
  q.skip({ all: true });
  await new Promise((r) => setTimeout(r, 50));
  assert.ok(streams.slice(1).every((s) => s.destroyed), 'cancelled streams must be destroyed');
});

test('usage logger writes JSONL with chars, bytes, minutes and session', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'usage-'));
  try {
    const file = path.join(dir, 'nested', 'tts-usage.jsonl');
    const u = new UsageLogger({ path: file, session: 'S-test', charsPerMinute: 900, logger });
    u.record({ provider: 'fish', voice: 'system', model: 's2.1-pro', text: 'x'.repeat(450) });
    u.record({ provider: 'fish', voice: 'gm', model: 's2.1-pro', text: 'héllo 🎲', audioSeconds: 30 });
    u.record({ provider: 'fish', voice: 'gm', model: 's2.1-pro', text: 'bad', ok: false });
    const lines = readFileSync(file, 'utf8').trim().split('\n').map((l) => JSON.parse(l));
    assert.equal(lines.length, 3);
    assert.deepEqual(
      { provider: lines[0].provider, voice: lines[0].voice, chars: lines[0].chars, minutes: lines[0].minutes, src: lines[0].minutes_source, session: lines[0].session },
      { provider: 'fish', voice: 'system', chars: 450, minutes: 0.5, src: 'estimate', session: 'S-test' }
    );
    assert.match(lines[0].ts, /^\d{4}-\d\d-\d\dT.*Z$/);
    assert.match(lines[0].date, /^\d{4}-\d\d-\d\d$/);
    assert.equal(lines[1].chars, 7); // code points, not UTF-16 units
    assert.equal(lines[1].utf8_bytes, Buffer.byteLength('héllo 🎲'));
    assert.equal(lines[1].minutes, 0.5);
    assert.equal(lines[1].minutes_source, 'audio');
    assert.equal(lines[2].ok, false);
    assert.ok(!readFileSync(file, 'utf8').includes('SECRET'));

    const off = new UsageLogger({ path: path.join(dir, 'off.jsonl'), enabled: false, logger });
    assert.equal(off.record({ provider: 'fish', voice: 'gm', text: 'x' }), null);
    // unwritable path must not throw
    const bad = new UsageLogger({ path: path.join(file, 'cannot', 'be-a-dir.jsonl'), logger }) // `file` is a regular file;
    assert.doesNotThrow(() => bad.record({ provider: 'fish', voice: 'gm', text: 'x' }));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('metered synth logs buffer providers by estimate and streams by measured audio', async () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'usage-'));
  const m = await mockFish();
  try {
    const file = path.join(dir, 'u.jsonl');
    const usage = new UsageLogger({ path: file, session: 'S1', logger });
    const fish = createTtsProvider(cfgFor(m.base));
    const synth = meteredSynthesize(fish, usage);
    const audio = await synth('Hello there.', 'system');
    await drain(audio);
    await audio.usage;
    await new Promise((r) => setImmediate(r));
    const bufferProvider = { id: 'openai', modelFor: () => 'gpt-4o-mini-tts', synthesize: async () => Buffer.from('mp3') };
    await meteredSynthesize(bufferProvider, usage)('Narration text here', 'gm');
    const failing = { id: 'openai', modelFor: () => 'm', synthesize: async () => { throw new Error('boom'); } };
    await assert.rejects(meteredSynthesize(failing, usage)('nope', 'gm'), /boom/);

    const rows = readFileSync(file, 'utf8').trim().split('\n').map((l) => JSON.parse(l));
    assert.equal(rows.length, 3);
    assert.deepEqual([rows[0].provider, rows[0].voice, rows[0].model, rows[0].minutes_source, rows[0].audio_seconds], ['fish', 'system', 's2.1-pro', 'audio', 1]);
    assert.equal(rows[0].minutes, 0.0167);
    assert.deepEqual([rows[1].provider, rows[1].minutes_source], ['openai', 'estimate']);
    assert.equal(rows[2].ok, false);
  } finally {
    rmSync(dir, { recursive: true, force: true });
    await m.close();
  }
});

const rec = (date, session, minutes, extra = {}) => ({
  ts: `${date}T12:00:00.000Z`, date, month: date.slice(0, 7), session, provider: 'fish', voice: 'gm', model: 's2.1-pro',
  chars: Math.round(minutes * 900), utf8_bytes: Math.round(minutes * 900), minutes, minutes_source: 'estimate', audio_seconds: null, ok: true, ...extra,
});

test('summarize: per day / month / session, cap percent, 80% warning, over cap', () => {
  const records = [
    rec('2026-09-30', 'A', 50), rec('2026-10-01', 'B', 60), rec('2026-10-01', 'B', 40), rec('2026-10-03', 'C', 61),
    rec('2026-10-03', 'C', 5, { ok: false }),
    rec('2026-10-03', 'C', 10, { provider: 'openai' }),
  ];
  const s = summarize(records, { cap: 200, now: new Date('2026-10-10T12:00:00') });
  assert.equal(s.failed_excluded, 1);
  const day = (d, p = 'fish') => s.by_day.find((r) => r.date === d && r.provider === p);
  assert.equal(day('2026-10-01').minutes, 100);
  assert.equal(day('2026-10-01').records, 2);
  assert.equal(day('2026-10-03').minutes, 61);
  assert.equal(s.by_month.find((r) => r.month === '2026-10' && r.provider === 'fish').minutes, 161);
  assert.equal(s.by_session.find((r) => r.session === 'B').minutes, 100);
  assert.equal(s.cap.month, '2026-10');
  assert.equal(s.cap.used_minutes, 161); // fish only; openai and the failed record excluded
  assert.equal(s.cap.percent, 80.5);
  assert.equal(s.cap.warn, true);
  assert.equal(s.cap.over, false);
  assert.equal(s.cap.remaining_minutes, 39);

  assert.equal(summarize(records, { cap: 400, now: new Date('2026-10-10T12:00:00') }).cap.warn, false);
  const edge = summarize([rec('2026-10-01', 'B', 160)], { cap: 200, now: new Date('2026-10-10T12:00:00') });
  assert.equal(edge.cap.percent, 80);
  assert.equal(edge.cap.warn, true);
  const over = summarize([rec('2026-10-01', 'B', 210)], { cap: 200, now: new Date('2026-10-10T12:00:00') });
  assert.deepEqual([over.cap.over, over.cap.remaining_minutes], [true, 0]);
  assert.equal(summarize(records, { cap: 200, capProvider: 'all', now: new Date('2026-10-10T12:00:00') }).cap.used_minutes, 171);
  assert.equal(summarize(records, { month: '2026-09', cap: 200 }).cap.used_minutes, 50);
  assert.equal(summarize([], { cap: 200 }).cap.percent, 0);
});

test('summarize: estimates cost per UTF-8 byte, free model costs $0; minutes fall back to chars/900', () => {
  const paid = { ...rec('2026-10-01', 'A', 1), utf8_bytes: 1_000_000, chars: 900_000 };
  const free = { ...rec('2026-10-01', 'A', 1, { model: 's2.1-pro-free' }), utf8_bytes: 1_000_000 };
  const s = summarize([paid, free]);
  assert.equal(s.total.est_cost_usd, 15);
  const noMinutes = { ts: '2026-10-01T00:00:00Z', date: '2026-10-01', provider: 'fish', chars: 1800, ok: true };
  assert.equal(summarize([noMinutes]).total.minutes, 2);
  const parsed = parseJsonl('{"chars":3}\nnot json\n{"nochars":1}\n\n');
  assert.deepEqual([parsed.records.length, parsed.bad], [1, 2]);
});

test('usage summary script: report, cap warning, --json, --fail-on-warn, missing file', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'usage-'));
  try {
    const month = new Date();
    const ym = `${month.getFullYear()}-${String(month.getMonth() + 1).padStart(2, '0')}`;
    const file = path.join(dir, 'u.jsonl');
    writeFileSync(file, [rec(`${ym}-01`, 'S1', 90), rec(`${ym}-02`, 'S2', 80)].map((r) => JSON.stringify(r)).join('\n') + '\nbroken line\n');
    const run = (...args) => spawnSync(process.execPath, [path.join(import.meta.dirname, '..', 'scripts', 'tts-usage-summary.js'), '--file', file, ...args], { encoding: 'utf8', env: { PATH: process.env.PATH, FISH_MONTHLY_CAP_MINUTES: '200' } });
    let r = run();
    assert.equal(r.status, 0, r.stderr);
    assert.match(r.stdout, /By day/);
    assert.match(r.stdout, /By month/);
    assert.match(r.stdout, /By bot session/);
    assert.match(r.stdout, /170\.00 \/ 200 min = 85\.0% used/);
    assert.match(r.stdout, /WARNING: usage is at or above 80%/);
    assert.match(r.stdout, /1 malformed/);
    r = run('--cap', '1000');
    assert.doesNotMatch(r.stdout, /WARNING/);
    assert.equal(run('--fail-on-warn').status, 3);
    assert.equal(run('--cap', '1000', '--fail-on-warn').status, 0);
    const j = JSON.parse(run('--json').stdout);
    assert.equal(j.cap.percent, 85);
    assert.equal(j.by_day.length, 2);
    assert.equal(run('--month', 'bad').status, 1);
    const none = spawnSync(process.execPath, [path.join(import.meta.dirname, '..', 'scripts', 'tts-usage-summary.js'), '--file', path.join(dir, 'missing.jsonl')], { encoding: 'utf8' });
    assert.equal(none.status, 0);
    assert.match(none.stdout, /0\.0% used/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
