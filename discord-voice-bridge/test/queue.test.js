import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import { test } from 'node:test';
import { AudioPlayerStatus } from '@discordjs/voice';
import { SpeechQueue } from '../src/queue.js';

const logger = { debug() {}, info() {}, warn() {}, error() {} };

/** Fake AudioPlayer: "plays" each resource for a few ms then goes idle. */
function fakePlayer(playMs = 5) {
  const p = new EventEmitter();
  p.played = [];
  p.state = { status: AudioPlayerStatus.Idle };
  let timer;
  const setStatus = (status) => {
    const old = p.state;
    p.state = { status };
    p.emit('stateChange', old, p.state);
  };
  p.play = (resource) => {
    p.played.push(resource);
    setStatus(AudioPlayerStatus.Playing);
    timer = setTimeout(() => setStatus(AudioPlayerStatus.Idle), playMs);
    resource.playStream.on('error', () => {});
  };
  p.stop = () => {
    clearTimeout(timer);
    if (p.state.status !== AudioPlayerStatus.Idle) setStatus(AudioPlayerStatus.Idle);
    return true;
  };
  return p;
}

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

/** Poll until cond() is true (CPU-starved CI/parallel runs make fixed sleeps flaky); fail after timeoutMs. */
async function waitFor(cond, timeoutMs = 5000) {
  const end = Date.now() + timeoutMs;
  while (!cond()) {
    if (Date.now() > end) throw new Error('waitFor timed out');
    await wait(5);
  }
}

test('plays chunks in order even when later synths finish first', async () => {
  const player = fakePlayer();
  const order = [];
  const delays = { a: 40, b: 1, c: 1 };
  const q = new SpeechQueue({
    player,
    prefetch: 3,
    logger,
    synthesize: async (t) => {
      await wait(delays[t]);
      order.push(`synth:${t}`);
      return Buffer.from(t);
    },
  });
  const bufs = [];
  const origPlay = player.play;
  player.play = (r) => {
    bufs.push(r);
    origPlay(r);
  };
  q.enqueue(['a', 'b', 'c']);
  await waitFor(() => bufs.length === 3 && q.size === 0 && player.state.status === AudioPlayerStatus.Idle);
  assert.equal(bufs.length, 3);
  assert.deepEqual(order, ['synth:b', 'synth:c', 'synth:a']);
  assert.equal(q.size, 0);
});

test('skip drops rest of current message but keeps later messages', async () => {
  const player = fakePlayer(50);
  const q = new SpeechQueue({ player, logger, synthesize: async (t) => Buffer.from(t) });
  q.enqueue(['m1-a', 'm1-b']);
  q.enqueue(['m2-a']);
  await waitFor(() => player.played.length === 1); // m1-a is playing (50ms) when we skip
  const dropped = q.skip();
  assert.ok(dropped >= 2);
  await waitFor(() => player.played.length === 2 && q.size === 0 && player.state.status === AudioPlayerStatus.Idle);
  assert.equal(player.played.length, 2); // m1-a (skipped mid-play) + m2-a
  assert.equal(q.size, 0);
});

test('skip all clears queue; synth errors do not wedge it; disabled queue refuses', async () => {
  const player = fakePlayer();
  let n = 0;
  const q = new SpeechQueue({
    player,
    logger,
    synthesize: async () => {
      if (n++ === 0) throw new Error('boom');
      return Buffer.from('ok');
    },
  });
  q.enqueue(['bad', 'good']);
  await wait(100);
  assert.equal(player.played.length, 1);
  q.enqueue(['x', 'y', 'z']);
  q.skip({ all: true });
  await wait(50);
  assert.equal(q.size, 0);
  q.enabled = false;
  assert.equal(q.enqueue(['nope']), 0);
});
