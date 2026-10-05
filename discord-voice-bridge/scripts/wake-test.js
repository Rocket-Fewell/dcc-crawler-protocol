// Sends one test wake payload to GM_WEBHOOK_URL using the same code path/auth as the bot.
//   npm run wake-test
// Reads GM_WEBHOOK_URL / GM_WEBHOOK_KEY / GM_WEBHOOK_AUTH_* from the environment (.env). Prints ONLY the HTTP
// status (or a short error code) - never the URL, the key or the response body.
// Exit codes: 0 = 2xx, 1 = failed / not configured.
import 'dotenv/config';
import { loadWakeConfig } from '../src/config.js';
import { buildPayload, postWake } from '../src/wake.js';

const wake = loadWakeConfig(process.env);
for (const p of wake.problems) console.error(`Config problem: ${p}`);
if (!wake.enabled) {
  console.error('GM_WEBHOOK_URL is not set (or invalid): the wake feature is OFF. Nothing sent.');
  process.exit(1);
}
const payload = buildPayload(
  [{ speaker: 'Wake Test', text: 'This is a test wake from `npm run wake-test`. No player said this.', ts: new Date().toISOString() }],
  { hint: wake.hint, extra: { test: true } }
);
const auth = wake.key ? (wake.keyInQuery ? `key in query param "${wake.keyInQuery}"` : `header ${wake.authHeader} (${wake.authScheme ? 'scheme ' + wake.authScheme : 'raw key'})`) : 'no key';
console.log(`Sending test wake (auth: ${auth}) ...`);
const r = await postWake(wake, payload);
if (r.status) console.log(`HTTP ${r.status}`);
else console.log(`Network error: ${r.error}`);
process.exit(r.ok ? 0 : 1);
