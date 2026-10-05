import assert from 'node:assert/strict';
import { test } from 'node:test';
import { ConfigError, loadConfig } from '../src/config.js';

const base = {
  DISCORD_TOKEN: 'x.y.z',
  CLIENT_ID: '111111111111111111',
  GUILD_ID: '222222222222222222',
  VOICE_CHANNEL_ID: '333333333333333333',
  TRANSCRIPT_CHANNEL_ID: '444444444444444444',
  GM_OUTPUT_CHANNEL_ID: '555555555555555555',
  OPENAI_API_KEY: 'sk-test',
};

test('loads defaults', () => {
  const c = loadConfig(base);
  assert.equal(c.stt.model, 'gpt-4o-transcribe');
  assert.equal(c.tts.provider, 'openai');
  assert.equal(c.stt.silenceMs, 1000);
  assert.deepEqual(c.discord.gmAllowedAuthorIds, []);
});

test('parses lists and booleans', () => {
  const c = loadConfig({ ...base, GM_ALLOWED_AUTHOR_IDS: '1, 2 3', AUTO_JOIN: 'true' });
  assert.deepEqual(c.discord.gmAllowedAuthorIds, ['1', '2', '3']);
  assert.equal(c.discord.autoJoin, true);
});

test('reports all problems', () => {
  assert.throws(() => loadConfig({}), (e) => e instanceof ConfigError && e.problems.length >= 3);
  assert.throws(() => loadConfig({ ...base, TTS_PROVIDER: 'elevenlabs' }), /ELEVENLABS_API_KEY/);
  assert.throws(() => loadConfig({ ...base, TTS_PROVIDER: 'nope' }), /TTS_PROVIDER/);
  assert.throws(() => loadConfig({ ...base, GUILD_ID: 'abc' }), /GUILD_ID/);
});

test('register mode only needs app credentials', () => {
  const c = loadConfig({ DISCORD_TOKEN: 't', CLIENT_ID: '111111111111111111', GUILD_ID: '222222222222222222' }, { mode: 'register' });
  assert.equal(c.discord.guildId, '222222222222222222');
});
