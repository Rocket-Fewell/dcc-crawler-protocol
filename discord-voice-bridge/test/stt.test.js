import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import { Readable } from 'node:stream';
import { test } from 'node:test';
import OpusScript from 'opusscript';
import { loadConfig } from '../src/config.js';
import { SttBridge } from '../src/stt.js';

const logger = { debug() {}, info() {}, warn() {}, error() {} };
const BOT_ID = '999999999999999999';
const env = {
  DISCORD_TOKEN: 't',
  CLIENT_ID: '111111111111111111',
  GUILD_ID: '222222222222222222',
  TRANSCRIPT_CHANNEL_ID: '444444444444444444',
  GM_OUTPUT_CHANNEL_ID: '555555555555555555',
  OPENAI_API_KEY: 'sk-test',
  STT_MIN_DURATION_MS: '500',
};

/** Encode `ms` of a stereo 440Hz tone (amplitude `amp`) into Discord-style 20ms Opus packets. */
function tonePackets(ms, amp = 8000) {
  const enc = new OpusScript(48000, 2, OpusScript.Application.VOIP);
  const packets = [];
  for (let f = 0; f < ms / 20; f++) {
    const pcm = Buffer.alloc(960 * 2 * 2);
    for (let i = 0; i < 960; i++) {
      const v = Math.round(amp * Math.sin((2 * Math.PI * 440 * (f * 960 + i)) / 48000));
      pcm.writeInt16LE(v, i * 4);
      pcm.writeInt16LE(v, i * 4 + 2);
    }
    packets.push(Buffer.from(enc.encode(pcm, 960)));
  }
  enc.delete?.();
  return packets;
}

function setup({ members = {} } = {}) {
  const posted = [];
  const speaking = new EventEmitter();
  const subscriptions = [];
  const connection = {
    receiver: {
      speaking,
      subscribe: (userId, opts) => {
        const spec = subscriptions.shift();
        assert.equal(opts.end.duration, 1000);
        return Readable.from(spec ?? []);
      },
    },
  };
  const guild = {
    members: {
      cache: new Map(),
      fetch: async (id) => {
        if (!members[id]) throw new Error('unknown member');
        return members[id];
      },
    },
  };
  const client = {
    user: { id: BOT_ID },
    guilds: { cache: new Map([[env.GUILD_ID, guild]]) },
    users: { cache: new Map(), fetch: async () => { throw new Error('nope'); } },
    channels: { fetch: async () => ({ isTextBased: () => true, send: async (m) => posted.push(m) }) },
  };
  return { client, connection, speaking, subscriptions, posted };
}

const flush = () => new Promise((r) => setTimeout(r, 150));

test('captures a user utterance, transcribes, posts with display name', async () => {
  const members = { u1: { displayName: 'Carl *the* Crawler', user: { bot: false } } };
  const { client, connection, speaking, subscriptions, posted } = setup({ members });
  let wavSeen;
  const stt = new SttBridge({
    client,
    config: loadConfig(env),
    logger,
    transcribe: async (wav) => {
      wavSeen = wav;
      return ' I attack the goblin. ';
    },
  });
  stt.attach(connection);
  subscriptions.push(tonePackets(1500));
  speaking.emit('start', 'u1');
  await flush();
  assert.equal(posted.length, 1);
  assert.equal(posted[0].content, '**Carl \\*the\\* Crawler**: "I attack the goblin."');
  assert.deepEqual(posted[0].allowedMentions, { parse: [] });
  // 16kHz mono WAV of ~1.5s
  assert.equal(wavSeen.toString('ascii', 0, 4), 'RIFF');
  assert.equal(wavSeen.readUInt32LE(24), 16000);
  const seconds = (wavSeen.length - 44) / 2 / 16000;
  assert.ok(seconds > 1.2 && seconds < 1.8, `duration ${seconds}`);
});

test('skips short, quiet, hallucinated, bot and self audio', async () => {
  const members = {
    u1: { displayName: 'Dee', user: { bot: false } },
    b1: { displayName: 'MusicBot', user: { bot: true } },
  };
  const { client, connection, speaking, subscriptions, posted } = setup({ members });
  const calls = [];
  const stt = new SttBridge({
    client,
    config: loadConfig(env),
    logger,
    transcribe: async () => {
      calls.push(1);
      return calls.length === 1 ? 'Thanks for watching!' : 'real speech';
    },
  });
  stt.attach(connection);

  subscriptions.push(tonePackets(200)); // too short
  speaking.emit('start', 'u1');
  await flush();
  subscriptions.push(tonePackets(1500, 20)); // too quiet
  speaking.emit('start', 'u1');
  await flush();
  assert.equal(calls.length, 0);

  subscriptions.push(tonePackets(1000)); // hallucination
  speaking.emit('start', 'u1');
  await flush();
  assert.equal(calls.length, 1);
  assert.equal(posted.length, 0);

  subscriptions.push(tonePackets(1000)); // bot (identity resolved after subscribe) -> dropped before post
  speaking.emit('start', 'b1');
  await flush();
  assert.equal(posted.length, 0);
  // second time the bot is cached and never subscribed
  const before = subscriptions.length;
  subscriptions.push(tonePackets(1000));
  speaking.emit('start', 'b1');
  await flush();
  assert.equal(subscriptions.length, before + 1);

  subscriptions.length = 0;
  subscriptions.push(tonePackets(1000));
  speaking.emit('start', BOT_ID); // self
  await flush();
  assert.equal(subscriptions.length, 1);
  assert.equal(posted.length, 0);

  subscriptions.length = 0;
  subscriptions.push(tonePackets(1000)); // legit
  speaking.emit('start', 'u1');
  await flush();
  assert.equal(posted.length, 1);
  assert.equal(posted[0].content, '**Dee**: "real speech"');
});
