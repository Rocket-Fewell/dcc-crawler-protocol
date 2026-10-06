/**
 * Real campaign/lore roots for the tests: the same roots the bridge itself resolves at startup.
 *
 * The bridge loads this package's .env (dotenv) before resolving paths, so on a layout where the package does not sit inside
 * the campaign (DCC_CAMPAIGN_ROOT set in .env) the tests must honour that too. Order, like dotenv: DCC_REAL_CAMPAIGN / DCC_REAL_LORE
 * (test overrides) > process env > the DCC_CAMPAIGN_* / DCC_LORE_* keys of .env (read only; nothing is injected into process.env,
 * so sandboxes never inherit them) > src/paths.js defaults (fresh checkout: the package's parent).
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { parse } from 'dotenv';
import { BRIDGE_PACKAGE_ROOT, resolveCampaignRoot, resolveLoreRoot } from '../../src/paths.js';

const ROOT_KEYS = ['DCC_CAMPAIGN_ROOT', 'DCC_CAMPAIGN_DIR', 'DCC_LORE_ROOT', 'DCC_LORE_DIR'];

function dotEnvRoots() {
  try {
    const all = parse(readFileSync(join(BRIDGE_PACKAGE_ROOT, '.env')));
    return Object.fromEntries(ROOT_KEYS.filter((k) => all[k]).map((k) => [k, all[k]]));
  } catch {
    return {};   // no .env (fresh checkout / CI)
  }
}

const ENV = { ...dotEnvRoots(), ...process.env };
export const REAL_CAMPAIGN = process.env.DCC_REAL_CAMPAIGN || resolveCampaignRoot(ENV);
export const REAL_LORE = process.env.DCC_REAL_LORE || resolveLoreRoot({ ...ENV, DCC_CAMPAIGN_ROOT: REAL_CAMPAIGN });
