/** Which Crawlers belong to a Discord user (spec section 8: a player may own many; exactly one is active). */
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { readSessionState } from './store.js';

export const normName = (s) => String(s ?? '').toLowerCase().replace(/[^a-z0-9]+/g, '');
export const kindOf = (c) => c.kind ?? 'player';
export const isActive = (c) => c.status !== 'benched';

/** Crawler name -> player aliases from the sheet map (player-channels.json), so alpha Crawlers made before /create (no discord_user_id) still match their player. */
function aliasMap(config) {
  const p = process.env.PLAYER_CHANNELS_FILE || join(config.campaign.dataDir, 'player-channels.json');
  try {
    if (!existsSync(p)) return {};
    const cfg = JSON.parse(readFileSync(p, 'utf8'));
    return Object.fromEntries(Object.entries(cfg.crawlers ?? {}).map(([k, v]) => [k, (v.players ?? []).map(normName)]));
  } catch {
    return {};
  }
}

/**
 * The user's Crawlers (player + pet-Crawlers). Match: build.discord_user_id, else (for Crawlers with no recorded id) the player name or a sheet-map alias
 * equals the user's Discord username or display name. A Crawler with a recorded id never matches by name.
 */
export function ownedCrawlers(config, user, state = readSessionState(config)) {
  if (!state) return [];
  const names = new Set([user.username, user.globalName, user.uname].map(normName).filter(Boolean));
  const aliases = aliasMap(config);
  return state.crawlers.filter((c) => {
    if (!['player', 'pet-crawler'].includes(kindOf(c))) return false;
    const uid = c.build?.discord_user_id;
    if (uid) return String(uid) === String(user.id);
    return names.has(normName(c.player)) || (aliases[c.name] ?? []).some((a) => names.has(a));
  });
}

/** The exact player string tools use for this human (so state.py groups a 2nd Crawler with the 1st), or null for a brand-new player. */
export const playerStringOf = (owned) => owned.find((c) => kindOf(c) === 'player')?.player ?? owned[0]?.player ?? null;
