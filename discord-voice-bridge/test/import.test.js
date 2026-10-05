import assert from 'node:assert/strict';
import { test } from 'node:test';

// Dry import of every module with dummy env (no network, no Discord login).
test('all modules import with dummy env', async () => {
  Object.assign(process.env, {
    DISCORD_TOKEN: 'dummy',
    CLIENT_ID: '111111111111111111',
    GUILD_ID: '222222222222222222',
    TRANSCRIPT_CHANNEL_ID: '444444444444444444',
    GM_OUTPUT_CHANNEL_ID: '555555555555555555',
    OPENAI_API_KEY: 'sk-dummy',
  });
  for (const m of ['config', 'logger', 'http', 'audio', 'text', 'queue', 'stt', 'tts', 'voice', 'commands/index']) {
    await import(`../src/${m}.js`);
  }
  const { commandData } = await import('../src/commands/index.js');
  assert.deepEqual(commandData.map((c) => c.name).sort(), ['crawlers', 'create', 'delete', 'encounter', 'gm', 'join', 'leave', 'say', 'session', 'shush', 'skip', 'voicecap']);
  const { createTtsProvider } = await import('../src/tts.js');
  const { loadConfig } = await import('../src/config.js');
  assert.match(createTtsProvider(loadConfig({ ...process.env, TTS_PROVIDER: 'openai' })).name, /^openai:/); // explicit: a developer's .env may select another provider
  const el = loadConfig({ ...process.env, TTS_PROVIDER: 'elevenlabs', ELEVENLABS_API_KEY: 'k', ELEVENLABS_VOICE_ID: 'v' });
  assert.match(createTtsProvider(el).name, /^elevenlabs:/);
});
