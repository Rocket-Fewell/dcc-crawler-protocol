/**
 * Portable campaign/lore roots (fresh-checkout safe).
 *
 * CAMPAIGN_ROOT = env DCC_CAMPAIGN_ROOT, else legacy DCC_CAMPAIGN_DIR, else
 *   parent of this package when it looks like the campaign repo (bot/ or
 *   discord-voice-bridge/ under the flattened repo), else /workspace/dcc-campaign
 *   when present (box layout).
 * LORE_ROOT = env DCC_LORE_ROOT, else <campaign>/lore, else sibling dcc-lore,
 *   else /workspace/dcc-lore.
 */
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const BRIDGE_ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const BOX_CAMPAIGN = '/workspace/dcc-campaign';
const BOX_LORE = '/workspace/dcc-lore';

export const looksLikeCampaign = (p) =>
  !!p && (existsSync(join(p, 'NAMING-CONVENTIONS.md')) || existsSync(join(p, 'tables', 'chargen-5e.json')));

export const looksLikeLore = (p) =>
  !!p && (existsSync(join(p, 'CANON-LEDGER.md')) || existsSync(join(p, 'tables')));

function envPath(env, ...names) {
  for (const n of names) {
    const v = env[n];
    if (v != null && String(v).trim() !== '') return String(v).trim();
  }
  return null;
}

/** Resolve campaign root. Pass env (default process.env) so tests can inject. */
export function resolveCampaignRoot(env = process.env) {
  const fromEnv = envPath(env, 'DCC_CAMPAIGN_ROOT', 'DCC_CAMPAIGN_DIR');
  if (fromEnv) return fromEnv;
  const parent = join(BRIDGE_ROOT, '..');
  if (looksLikeCampaign(parent)) return parent;
  if (looksLikeCampaign(BOX_CAMPAIGN)) return BOX_CAMPAIGN;
  return BOX_CAMPAIGN; // legacy default string (may not exist off-box; callers override via env)
}

export function resolveLoreRoot(env = process.env) {
  const fromEnv = envPath(env, 'DCC_LORE_ROOT', 'DCC_LORE_DIR');
  if (fromEnv) return fromEnv;
  const camp = resolveCampaignRoot(env);
  const viaCamp = join(camp, 'lore');
  if (looksLikeLore(viaCamp)) return viaCamp;
  const sibling = join(dirname(camp), 'dcc-lore');
  if (looksLikeLore(sibling)) return sibling;
  if (looksLikeLore(BOX_LORE)) return BOX_LORE;
  return viaCamp;
}

export const BRIDGE_PACKAGE_ROOT = BRIDGE_ROOT;
