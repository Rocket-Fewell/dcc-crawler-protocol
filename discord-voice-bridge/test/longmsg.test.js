import assert from 'node:assert/strict';
import { test } from 'node:test';
import { loadConfig } from '../src/config.js';
import { groupIntoParts, prepareSpeechDetailed } from '../src/text.js';
import { GmOutputBridge } from '../src/tts.js';

// Oct 7 2026: GM posts longer than TTS_MAX_MESSAGE_CHARS are split and spoken in full (up to TTS_MAX_TOTAL_CHARS), not truncated.
const env = {
  DISCORD_TOKEN: 't',
  CLIENT_ID: '111111111111111111',
  GUILD_ID: '222222222222222222',
  TRANSCRIPT_CHANNEL_ID: '444444444444444444',
  GM_OUTPUT_CHANNEL_ID: '555555555555555555',
  OPENAI_API_KEY: 'sk-test',
};
const opts = { chunkMaxChars: 600, maxMessageChars: 1500, maxTotalChars: 6000 };
const spoken = (chunks) => chunks.map((c) => c.text).join(' ');

test('a 1900-char GM post is spoken in full, in order, as several parts (no truncation)', () => {
  const sentences = Array.from({ length: 34 }, (_, i) => `Sentence number ${i} drips down the corridor wall.`);
  const raw = sentences.join(' ');
  assert.ok(raw.length > 1500 && raw.length < 2000, String(raw.length));
  const r = prepareSpeechDetailed(raw, opts);
  assert.equal(r.truncated, false);
  assert.equal(r.split, true);
  assert.ok(r.parts >= 2);
  assert.equal(r.droppedChars, 0);
  const text = spoken(r.chunks);
  for (const s of sentences) assert.ok(text.includes(s), s);
  assert.ok(text.indexOf('Sentence number 0 ') < text.indexOf('Sentence number 33 '));
  for (const c of r.chunks) assert.match(c.text, /[.!?]$/); // sentence boundaries
});

test('voice tags survive the split: every chunk keeps its [GM]/[SYSTEM]/[NPC: Name] voice, in order', () => {
  const gm = 'The narrator sneers at your life choices. '.repeat(20);
  const sys = 'Floor collapse notice: forty minutes remain. '.repeat(15);
  const npc = 'Snakk-Matic hums a jingle about potions. '.repeat(15);
  const raw = `[GM] ${gm}\n[SYSTEM] ${sys}\n[NPC: Snakk-Matic] ${npc}\n[ROLL] 1d20 = 4\n[GM] Back to me. Lovely.`;
  const r = prepareSpeechDetailed(raw, opts);
  assert.equal(r.truncated, false);
  assert.ok(r.totalChars > 1500);
  const voices = r.chunks.map((c) => c.voice);
  const order = voices.filter((v, i) => i === 0 || voices[i - 1] !== v);
  assert.deepEqual(order, ['gm', 'system', 'npc:snakk matic', 'gm']);
  for (const c of r.chunks) {
    if (c.voice === 'system') assert.match(c.text, /Floor collapse/);
    if (c.voice === 'npc:snakk matic') assert.match(c.text, /Snakk-Matic hums/);
    assert.ok(!/\[ROLL\]|1d20 = 4/.test(c.text));
  }
  assert.match(r.chunks.at(-1).text, /Back to me\. Lovely\./);
});

test('the safety ceiling still truncates (at a sentence) and reports what was dropped', () => {
  const raw = 'The corridor stretches on and on into the dripping dark. '.repeat(150); // ~8550 chars
  const r = prepareSpeechDetailed(raw, opts);
  assert.equal(r.truncated, true);
  assert.ok(r.totalChars <= 6000 && r.totalChars > 5800, String(r.totalChars));
  assert.ok(r.droppedChars > 2000);
  const small = prepareSpeechDetailed(raw, { ...opts, maxTotalChars: 1000 }); // ceiling below the part size: part size wins
  assert.ok(small.totalChars > 1000 && small.totalChars <= 1500);
});

test('legacy callers without maxTotalChars keep the old 1500 hard cap', () => {
  const raw = 'The corridor stretches on and on into the dripping dark. '.repeat(40);
  const r = prepareSpeechDetailed(raw, { chunkMaxChars: 600, maxMessageChars: 1500 });
  assert.equal(r.truncated, true);
  assert.ok(r.totalChars <= 1500);
});

test('groupIntoParts packs chunks in order without splitting one', () => {
  const chunks = [{ voice: 'gm', text: 'a'.repeat(700) }, { voice: 'system', text: 'b'.repeat(700) }, { voice: 'gm', text: 'c'.repeat(200) }];
  const parts = groupIntoParts(chunks, 1500);
  assert.equal(parts.length, 2);
  assert.deepEqual(parts.flat(), chunks);
  assert.deepEqual(groupIntoParts([], 1500), []);
});

test('config: TTS_MAX_TOTAL_CHARS default 6000, configurable, never below TTS_MAX_MESSAGE_CHARS', () => {
  assert.equal(loadConfig(env).tts.maxTotalChars, 6000);
  assert.equal(loadConfig({ ...env, TTS_MAX_TOTAL_CHARS: '9000' }).tts.maxTotalChars, 9000);
  assert.equal(loadConfig({ ...env, TTS_MAX_TOTAL_CHARS: '800', TTS_MAX_MESSAGE_CHARS: '1500' }).tts.maxTotalChars, 1500);
});

test('GmOutputBridge enqueues the whole long message once and logs the split, not a truncation', async () => {
  const enqueued = [];
  const logs = { info: [], warn: [] };
  const logger = { debug() {}, info: (m) => logs.info.push(m), warn: (m) => logs.warn.push(m), error() {} };
  const bridge = new GmOutputBridge({
    client: { user: { id: 'bot' } },
    config: loadConfig(env),
    session: { isConnected: true },
    queue: { enqueue: (chunks) => (enqueued.push(chunks), 1) },
    logger,
  });
  const body = `[GM] ${'Your mop finds the Bruiser in a deeply personal place. '.repeat(25)}\n[SYSTEM] ${'Damage logged. '.repeat(20)}`;
  await bridge.handle({ guildId: env.GUILD_ID, channelId: env.GM_OUTPUT_CHANNEL_ID, id: '9', author: { id: 'gm1', tag: 'GM#0001' }, cleanContent: body, content: body, embeds: [] });
  assert.equal(enqueued.length, 1);
  const text = spoken(enqueued[0]);
  assert.ok(text.length > 1500, String(text.length));
  assert.match(enqueued[0].at(-1).text, /Damage logged\.$/);
  assert.equal(enqueued[0].at(-1).voice, 'system');
  assert.ok(logs.info.some((m) => /split into \d+ parts/.test(m)));
  assert.ok(!logs.warn.some((m) => /truncated/.test(m)));
});
