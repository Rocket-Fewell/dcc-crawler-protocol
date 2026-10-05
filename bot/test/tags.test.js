import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import http from 'node:http';
import { test } from 'node:test';
import { loadConfig } from '../src/config.js';
import { parseTaggedLines } from '../src/tags.js';
import { prepareSpeech, prepareSpeechDetailed } from '../src/text.js';
import { SpeechQueue } from '../src/queue.js';
import { ElevenLabsTts, GmOutputBridge, OpenAiTts, createTtsProvider } from '../src/tts.js';

const env = {
  DISCORD_TOKEN: 't',
  CLIENT_ID: '111111111111111111',
  GUILD_ID: '222222222222222222',
  TRANSCRIPT_CHANNEL_ID: '444444444444444444',
  GM_OUTPUT_CHANNEL_ID: '555555555555555555',
  OPENAI_API_KEY: 'sk-test',
};
const logger = { debug() {}, info() {}, warn() {}, error() {} };

test('untagged text uses the narrator voice', () => {
  assert.deepEqual(parseTaggedLines('You enter the room.\nIt is dark.'), [{ voice: 'gm', text: 'You enter the room.\nIt is dark.' }]);
});

test('[GM], [SYSTEM], [ROLL] per line; tag applies until the next tag; tags are stripped', () => {
  const raw = [
    'Untagged intro.',
    '[SYSTEM] Achievement unlocked!',
    'Still the system talking.',
    '[ROLL] d20 + 5 = 17',
    'this continuation of the roll is silent too',
    '[GM] The goblin snarls.',
    '[system]: lowercase and colon work',
  ].join('\n');
  assert.deepEqual(parseTaggedLines(raw), [
    { voice: 'gm', text: 'Untagged intro.' },
    { voice: 'system', text: 'Achievement unlocked!\nStill the system talking.' },
    { voice: 'gm', text: 'The goblin snarls.' },
    { voice: 'system', text: 'lowercase and colon work' },
  ]);
});

test('tag on its own line, markdown-wrapped tags, and tags inside code fences', () => {
  assert.deepEqual(parseTaggedLines('[SYSTEM]\nWelcome, crawler.'), [{ voice: 'system', text: 'Welcome, crawler.' }]);
  assert.deepEqual(parseTaggedLines('**[SYSTEM]** Bold tag\n> [GM] quoted tag'), [
    { voice: 'system', text: 'Bold tag' },
    { voice: 'gm', text: 'quoted tag' },
  ]);
  const fenced = parseTaggedLines('[GM] Look:\n```\n[ROLL] not a tag\n```\nAfter.');
  assert.equal(fenced.length, 1);
  assert.equal(fenced[0].voice, 'gm');
  assert.match(fenced[0].text, /After\./);
  // a mid-line tag is not a tag
  assert.deepEqual(parseTaggedLines('He said [SYSTEM] out loud.'), [{ voice: 'gm', text: 'He said [SYSTEM] out loud.' }]);
});

test('[ROLL]-only messages produce nothing; defaultVoice applies to untagged lines', () => {
  assert.deepEqual(prepareSpeech('[ROLL] 1d20 = 4'), []);
  assert.deepEqual(prepareSpeech('[ROLL] a\n[ROLL] b'), []);
  assert.deepEqual(prepareSpeech('Hello there.', { defaultVoice: 'system' }), [{ voice: 'system', text: 'Hello there.' }]);
  assert.deepEqual(prepareSpeech('[GM] Hello there.', { defaultVoice: 'system' }), [{ voice: 'gm', text: 'Hello there.' }]);
});

test('prepareSpeech yields voiced, tag-free, markdown-free chunks', () => {
  const chunks = prepareSpeech('[SYSTEM] **Level up!** 🎉 You are now level 2.\n[ROLL] 12\n[GM] Carl grins. `Ha`.');
  assert.deepEqual(chunks.map((c) => c.voice), ['system', 'gm']);
  const all = chunks.map((c) => c.text).join(' ');
  assert.ok(!/SYSTEM|ROLL|\[|\*|🎉/.test(all), all);
  assert.match(chunks[0].text, /Level up! You are now level 2\./);
});

test('chunk max splits long text at sentence boundaries; hard cap truncates', () => {
  const sentence = 'The corridor stretches on and on into the dripping dark. ';
  const raw = sentence.repeat(40); // ~2280 chars
  const { chunks, truncated } = prepareSpeechDetailed(raw, { chunkMaxChars: 600, maxMessageChars: 1500 });
  assert.equal(truncated, true);
  const total = chunks.reduce((n, c) => n + c.text.length, 0);
  assert.ok(total <= 1500, `total ${total}`);
  assert.ok(total > 1300, `total ${total}`);
  for (const c of chunks) {
    assert.ok(c.text.length <= 600);
    assert.match(c.text, /[.!?]$/); // cut at sentence boundaries
  }
  assert.ok(chunks.length > 5); // sentence-size, not one big blob

  const small = prepareSpeechDetailed('Short one. Another.', { chunkMaxChars: 600, maxMessageChars: 1500 });
  assert.equal(small.truncated, false);
});

test('hard cap spans voices and long single sentences respect chunk max', () => {
  const longSentence = Array.from({ length: 130 }, (_, i) => `word${i}`).join(' ') + '.'; // ~900 chars
  const { chunks } = prepareSpeechDetailed(`[SYSTEM] ${longSentence}\n[GM] ${'Short sentence here. '.repeat(40)}`, { chunkMaxChars: 600, maxMessageChars: 1500 });
  assert.ok(chunks.every((c) => c.text.length <= 600));
  assert.ok(chunks.reduce((n, c) => n + c.text.length, 0) <= 1500);
  assert.deepEqual([...new Set(chunks.map((c) => c.voice))], ['system', 'gm']);
});

test('multiple sources: tag state does not leak from message body into embeds', () => {
  const chunks = prepareSpeech(['[ROLL] 15', 'Embed text speaks.']);
  assert.deepEqual(chunks, [{ voice: 'gm', text: 'Embed text speaks.' }]);
});

test('config: system voice settings, defaults and fallbacks', () => {
  const c = loadConfig(env);
  assert.equal(c.tts.chunkMaxChars, 600);
  assert.equal(c.tts.maxMessageChars, 1500);
  assert.equal(c.tts.openai.voices.gm.voice, 'onyx');
  assert.equal(c.tts.openai.voices.system.voice, 'coral');
  assert.match(c.tts.openai.voices.system.instructions, /game-show host/);
  assert.match(c.tts.openai.voices.system.instructions, /smug/);

  const c2 = loadConfig({
    ...env,
    OPENAI_TTS_SYSTEM_VOICE: 'shimmer',
    OPENAI_TTS_SYSTEM_MODEL: 'tts-1',
    OPENAI_TTS_SYSTEM_INSTRUCTIONS: 'custom',
    TTS_CHUNK_MAX_CHARS: '400',
    TTS_MAX_MESSAGE_CHARS: '900',
  });
  assert.equal(c2.tts.openai.voices.system.voice, 'shimmer');
  assert.equal(c2.tts.openai.voices.system.model, 'tts-1');
  assert.equal(c2.tts.openai.voices.system.instructions, 'custom');
  assert.equal(c2.tts.chunkMaxChars, 400);
  assert.equal(c2.tts.maxMessageChars, 900);

  const el = loadConfig({ ...env, TTS_PROVIDER: 'elevenlabs', ELEVENLABS_API_KEY: 'k', ELEVENLABS_VOICE_ID: 'narr' });
  assert.equal(el.tts.elevenlabs.voices.system.voiceId, 'narr'); // fallback
  assert.equal(el.tts.elevenlabs.systemVoiceFallback, true);
  const el2 = loadConfig({ ...env, TTS_PROVIDER: 'elevenlabs', ELEVENLABS_API_KEY: 'k', ELEVENLABS_VOICE_ID: 'narr', ELEVENLABS_SYSTEM_VOICE_ID: 'sys' });
  assert.equal(el2.tts.elevenlabs.voices.system.voiceId, 'sys');
  assert.equal(el2.tts.elevenlabs.systemVoiceFallback, false);
});

test('providers send the right voice settings per voice (mock HTTP server)', async () => {
  const seen = [];
  const srv = http.createServer((req, res) => {
    let b = '';
    req.on('data', (d) => (b += d));
    req.on('end', () => {
      seen.push({ url: req.url, body: JSON.parse(b) });
      res.setHeader('content-type', 'audio/mpeg');
      res.end(Buffer.from('mp3'));
    });
  });
  await new Promise((r) => srv.listen(0, r));
  const port = srv.address().port;
  try {
    const cfg = loadConfig({ ...env, OPENAI_BASE_URL: `http://127.0.0.1:${port}/v1`, OPENAI_TTS_INSTRUCTIONS: 'gravelly dungeon announcer' });
    const oa = createTtsProvider(cfg);
    assert.ok(oa instanceof OpenAiTts);
    await oa.synthesize('narrate', 'gm');
    await oa.synthesize('announce', 'system');
    await oa.synthesize('default');
    assert.equal(seen[0].body.voice, 'onyx');
    assert.match(seen[0].body.instructions, /dungeon announcer/);
    assert.equal(seen[1].body.voice, 'coral');
    assert.match(seen[1].body.instructions, /game-show host/);
    assert.equal(seen[2].body.voice, 'onyx');

    // ElevenLabs: patch fetch to hit the mock server
    const el = createTtsProvider(
      loadConfig({ ...env, TTS_PROVIDER: 'elevenlabs', ELEVENLABS_API_KEY: 'k', ELEVENLABS_VOICE_ID: 'narr', ELEVENLABS_SYSTEM_VOICE_ID: 'sys' })
    );
    assert.ok(el instanceof ElevenLabsTts);
    const realFetch = globalThis.fetch;
    globalThis.fetch = (url, init) => realFetch(String(url).replace('https://api.elevenlabs.io', `http://127.0.0.1:${port}`), init);
    try {
      seen.length = 0;
      await el.synthesize('narrate', 'gm');
      await el.synthesize('announce', 'system');
    } finally {
      globalThis.fetch = realFetch;
    }
    assert.match(seen[0].url, /\/v1\/text-to-speech\/narr\?/);
    assert.match(seen[1].url, /\/v1\/text-to-speech\/sys\?/);
    assert.equal(seen[1].body.voice_settings.stability, 0.35);
  } finally {
    srv.close();
  }
});

test('queue passes the voice to synthesize', async () => {
  const calls = [];
  const player = Object.assign(new EventEmitter(), {
    state: { status: 'idle' },
    play() {},
    stop() {
      // like a real AudioPlayer: stopping goes Idle, which releases the queue
      player.emit('stateChange', { status: 'playing' }, { status: 'idle' });
    },
  });
  const q = new SpeechQueue({ player, logger, prefetch: 3, synthesize: async (t, v) => (calls.push([t, v]), Buffer.from(t)) });
  q.enqueue([{ voice: 'system', text: 'a' }, { voice: 'gm', text: 'b' }, 'c']);
  await new Promise((r) => setTimeout(r, 30));
  q.clear();
  assert.deepEqual(calls.slice(0, 3), [['a', 'system'], ['b', 'gm'], ['c', 'gm']]);
});

test('GmOutputBridge: tags drive voices, [ROLL] never spoken, bot/self ignored', async () => {
  const enqueued = [];
  const bridge = new GmOutputBridge({
    client: { user: { id: 'bot' } },
    config: loadConfig(env),
    session: { isConnected: true },
    queue: { enqueue: (chunks) => enqueued.push(chunks) },
    logger,
  });
  const msg = (content, extra = {}) => ({
    guildId: env.GUILD_ID,
    channelId: env.GM_OUTPUT_CHANNEL_ID,
    id: '1',
    author: { id: 'gm1', tag: 'GM#0001' },
    cleanContent: content,
    content,
    embeds: [],
    ...extra,
  });
  await bridge.handle(msg('[SYSTEM] Ding!\n[ROLL] 3\n[GM] The door creaks.'));
  assert.deepEqual(enqueued[0], [
    { voice: 'system', text: 'Ding!' },
    { voice: 'gm', text: 'The door creaks.' },
  ]);
  await bridge.handle(msg('[ROLL] 1d20 = 7'));
  await bridge.handle(msg('Hello', { author: { id: 'bot' } }));
  await bridge.handle(msg('[ROLL] hidden', { embeds: [{ title: 'Embed', description: 'Visible embed text.' }] }));
  assert.equal(enqueued.length, 2);
  assert.deepEqual(enqueued[1], [{ voice: 'gm', text: 'Embed' }, { voice: 'gm', text: 'Visible embed text.' }]);
});
