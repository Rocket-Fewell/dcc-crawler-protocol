// Real-key smoke test for the Fish provider (costs a few characters of credit).
//   TTS_PROVIDER=fish node scripts/fish-smoke.js ["text to speak"]
// Needs FISH_API_KEY + FISH_VOICE_ID_* in .env. Writes fish-smoke-gm.mp3 / fish-smoke-system.mp3 to the
// current directory and prints time-to-first-byte and size. The key is never printed.
import 'dotenv/config';
import { createWriteStream } from 'node:fs';
import { pipeline } from 'node:stream/promises';
import { ConfigError, loadConfig } from '../src/config.js';
import { createTtsProvider } from '../src/tts.js';

process.env.TTS_PROVIDER = 'fish';
let config;
try {
  config = loadConfig();
} catch (err) {
  console.error(err instanceof ConfigError ? err.message : err.message);
  process.exit(1);
}
const provider = createTtsProvider(config);
const text = process.argv[2] ?? 'The System welcomes you, crawler. Please do not die immediately.';
console.log(`Provider: ${provider.name.replace(config.tts.fish.apiKey, '[redacted]')}`);
for (const voice of ['gm', 'system']) {
  const started = Date.now();
  try {
    const stream = await provider.synthesize(text, voice);
    let ttfb = null;
    stream.once('data', () => (ttfb = Date.now() - started));
    await pipeline(stream, createWriteStream(`fish-smoke-${voice}.mp3`));
    const u = await stream.usage;
    console.log(`${voice}: first audio ${ttfb} ms, total ${Date.now() - started} ms, ${u.bytes} bytes, ~${u.audioSeconds?.toFixed(1)} s -> fish-smoke-${voice}.mp3`);
  } catch (err) {
    console.error(`${voice}: FAILED - ${err.message}`);
    process.exitCode = 1;
  }
}
