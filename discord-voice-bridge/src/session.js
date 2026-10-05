/**
 * Campaign sessions ("alpha" = the live game; others e.g. "beta"): one bot, ONE active session at a time.
 *
 * The active session selects the data root, the #ears/#mouth/voice channels (same or another guild), the GM webhook URL/key and
 * the Fish minute shares. The choice persists in <campaign>/sessions/active-session.json (shared with the Python tools, which
 * follow it too) and can be overridden at startup with DCC_SESSION. Default and fallback: "alpha" - with no file and no env var
 * nothing changes for the live game.
 *
 * Per-session settings: <data>/session.json (no secrets), e.g.
 *   { "label": "Beta", "guild_id": "...", "ears_channel_id": "...", "mouth_channel_id": "...", "voice_channel_id": "...",
 *     "fish_session_cap_minutes": 40, "fish_monthly_minutes": 100, "env_prefix": "BETA_" }
 * Secrets stay in .env under the prefix: BETA_GM_WEBHOOK_URL, BETA_GM_WEBHOOK_KEY, BETA_GM_ALLOWED_AUTHOR_IDS, BETA_GM_DISCORD_TOKEN ...
 * Any env var named <PREFIX><NAME> overrides <NAME> while that session is active.
 */
import { existsSync, mkdirSync, readFileSync, readdirSync, renameSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

export const DEFAULT_SESSION = 'alpha';
export const DEFAULT_CAMPAIGN_DIR = '/workspace/dcc-campaign';
const RESERVED = new Set(['backups', 'secret', 'archive', 'sessions', 'characters', 'tmp']);
const ID = /^[a-z0-9][a-z0-9_-]{0,30}$/;

export const validSessionId = (id) => typeof id === 'string' && ID.test(id) && !RESERVED.has(id);
export const campaignDir = (env = process.env) => env.DCC_CAMPAIGN_DIR || DEFAULT_CAMPAIGN_DIR;
export const dataDir = (id, env = process.env) =>
  id === DEFAULT_SESSION ? join(campaignDir(env), 'sessions') : join(campaignDir(env), 'sessions-data', id);
export const charactersDir = (id, env = process.env) =>
  id === DEFAULT_SESSION ? join(campaignDir(env), 'characters') : join(dataDir(id, env), 'characters');
export const sessionFile = (id, env = process.env) => join(dataDir(id, env), 'session.json');
export const activeFile = (env = process.env) => join(campaignDir(env), 'sessions', 'active-session.json');

export function readActive(env = process.env) {
  try {
    const id = String(JSON.parse(readFileSync(activeFile(env), 'utf8')).session ?? '').trim().toLowerCase();
    return validSessionId(id) ? id : null;
  } catch {
    return null;
  }
}

export function writeActive(id, by = null, env = process.env) {
  const file = activeFile(env);
  mkdirSync(dirname(file), { recursive: true });
  const tmp = `${file}.${process.pid}.tmp`;
  writeFileSync(tmp, `${JSON.stringify({ session: id, updated: new Date().toISOString(), by })}\n`);
  renameSync(tmp, file);
}

/** DCC_SESSION (startup override) > persisted choice > alpha. Invalid values are ignored. */
export function resolveActiveId(env = process.env) {
  const e = String(env.DCC_SESSION ?? '').trim().toLowerCase();
  if (e && (e === DEFAULT_SESSION || validSessionId(e))) return e;
  return readActive(env) ?? DEFAULT_SESSION;
}

export function readProfile(id, env = process.env) {
  try {
    const p = JSON.parse(readFileSync(sessionFile(id, env), 'utf8'));
    return p && typeof p === 'object' ? p : {};
  } catch {
    return {};
  }
}

export function listSessions(env = process.env) {
  const root = join(campaignDir(env), 'sessions-data');
  let more = [];
  try {
    more = readdirSync(root, { withFileTypes: true }).filter((d) => d.isDirectory() && validSessionId(d.name)).map((d) => d.name).sort();
  } catch {
    /* none */
  }
  return [DEFAULT_SESSION, ...more];
}

export const sessionExists = (id, env = process.env) => id === DEFAULT_SESSION || existsSync(join(dataDir(id, env), 'state.json')) || existsSync(sessionFile(id, env));

const PROFILE_TO_ENV = {
  guild_id: 'GUILD_ID',
  voice_channel_id: 'VOICE_CHANNEL_ID',
  ears_channel_id: 'TRANSCRIPT_CHANNEL_ID',
  mouth_channel_id: 'GM_OUTPUT_CHANNEL_ID',
  fish_session_cap_minutes: 'FISH_SESSION_CAP_MINUTES',
  fish_monthly_minutes: 'FISH_SESSION_MONTHLY_MINUTES',
};

/**
 * The environment the bridge runs with while session `id` is active. alpha = the process env untouched (plus DCC_SESSION_ID),
 * so the live game is configured exactly as before.
 */
export function sessionEnv(env, id) {
  const out = { ...env, DCC_SESSION_ID: id };
  if (id === DEFAULT_SESSION) return out;
  const profile = readProfile(id, env);
  for (const [k, name] of Object.entries(PROFILE_TO_ENV)) {
    if (profile[k] !== undefined && profile[k] !== null && String(profile[k]) !== '') out[name] = String(profile[k]);
  }
  const dir = dataDir(id, env);
  out.SPOTLIGHT_FILE = join(dir, 'spotlight.json');
  out.VOICE_CONTROL_FILE = join(dir, 'voice-control.json');
  out.GM_WAKE_STATE_FILE = join(dir, 'gm-wake-state.json');
  const prefix = typeof profile.env_prefix === 'string' ? profile.env_prefix : `${id.toUpperCase().replace(/[^A-Z0-9]/g, '_')}_`;
  if (prefix) {
    for (const [k, v] of Object.entries(env)) {
      if (k.startsWith(prefix) && k.length > prefix.length && v !== undefined && v !== '') out[k.slice(prefix.length)] = v;
    }
  }
  // A new table must never inherit another table's webhook / author allow-list by accident.
  for (const name of ['GM_WEBHOOK_URL', 'GM_WEBHOOK_KEY', 'GM_ALLOWED_AUTHOR_IDS']) {
    if (!(prefix && env[`${prefix}${name}`])) delete out[name];
  }
  return out;
}

/** Replace the contents of `target` with `src`, in place, recursively, so modules holding a reference to a nested config object see it. */
export function replaceInPlace(target, src) {
  const isObj = (v) => v && typeof v === 'object' && !Array.isArray(v);
  for (const k of Object.keys(target)) if (!(k in src)) delete target[k];
  for (const [k, v] of Object.entries(src)) {
    if (isObj(v) && isObj(target[k])) replaceInPlace(target[k], v);
    else target[k] = v;
  }
  return target;
}
