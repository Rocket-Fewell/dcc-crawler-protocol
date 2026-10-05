import { readFileSync, statSync } from 'node:fs';

/**
 * Spotlight filter for the GM wake webhook.
 *
 * While the AI GM is running a "spotlight" exchange it listens only to one player (until it says it is done);
 * any player can break in by saying the wake word "AI". The GM writes the state file (see
 * dcc-campaign/tools/discord_gm.py `spotlight ...`):
 *   {"player":"<name or null>","aliases":["optional","other names"],"updated":"ISO ts","note":""}
 *
 * FAIL OPEN: a missing / empty / unreadable / malformed / stale file, or player null, means "open floor":
 * every line wakes the GM. This module never throws and never blocks on an error.
 *
 * Only the wake POST is filtered. Every line is still posted to the transcript channel by the STT bridge.
 */

const MAX_FILE_BYTES = 64 * 1024;
const FUTURE_SKEW_MS = 5 * 60_000; // an `updated` further in the future than this is treated as invalid (=> open)

/** Lowercase, strip accents/diacritics, turn punctuation into spaces, collapse whitespace. */
export function normalizeName(s) {
  return String(s ?? '')
    .normalize('NFKD')
    .replace(/\p{M}+/gu, '')
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, ' ')
    .trim();
}

/**
 * Does a speaker's name match the spotlight value? Case/accent-insensitive; matches when either string is a
 * substring of the other. A single-character name only matches by equality (so "a" can't match everybody).
 */
export function nameMatches(speakerName, wanted) {
  const a = normalizeName(speakerName);
  const b = normalizeName(wanted);
  if (!a || !b) return false;
  if (a === b) return true;
  if (a.length < 2 || b.length < 2) return false;
  return a.includes(b) || b.includes(a);
}

// Standalone "AI", "A.I.", "A. I.", "A I" (any case). Letters/digits on either side defeat the match, so
// "said", "main", "again", "available", "AIM", "mail" do not trigger. "hey AI" is covered by "AI".
const WAKE_WORD = /(?<![\p{L}\p{N}])a(?:\s?\.\s?|\s)?i(?:\.)?(?![\p{L}\p{N}])/iu;

export function hasWakeWord(text) {
  return WAKE_WORD.test(String(text ?? ''));
}

/**
 * Read the spotlight file. Always returns an object; `active` is true only for a fresh, well-formed file with a player.
 * @returns {{active:boolean, player?:string, aliases?:string[], note?:string, updated?:string, reason:string}}
 */
export function readSpotlight({ file, maxAgeMinutes = 20, now = Date.now() } = {}) {
  try {
    if (!file) return { active: false, reason: 'no_file_configured' };
    let raw;
    try {
      if (statSync(file).size > MAX_FILE_BYTES) return { active: false, reason: 'too_large' };
      raw = readFileSync(file, 'utf8');
    } catch (err) {
      return { active: false, reason: err?.code === 'ENOENT' ? 'missing' : 'unreadable' };
    }
    if (!raw.trim()) return { active: false, reason: 'empty' };
    let data;
    try {
      data = JSON.parse(raw);
    } catch {
      return { active: false, reason: 'malformed' };
    }
    if (!data || typeof data !== 'object' || Array.isArray(data)) return { active: false, reason: 'malformed' };
    const player = typeof data.player === 'string' ? data.player.trim() : '';
    if (!player) return { active: false, reason: data.player == null || data.player === '' ? 'cleared' : 'malformed' };
    const updatedMs = typeof data.updated === 'string' ? Date.parse(data.updated) : NaN;
    if (Number.isNaN(updatedMs)) return { active: false, reason: 'no_timestamp' };
    if (updatedMs - now > FUTURE_SKEW_MS) return { active: false, reason: 'bad_timestamp' };
    if (maxAgeMinutes > 0 && now - updatedMs > maxAgeMinutes * 60_000) return { active: false, reason: 'stale' };
    const aliases = Array.isArray(data.aliases) ? data.aliases.filter((x) => typeof x === 'string' && x.trim()).map((x) => x.trim()) : [];
    return { active: true, player, aliases, note: typeof data.note === 'string' ? data.note : '', updated: data.updated, reason: 'active' };
  } catch {
    return { active: false, reason: 'error' };
  }
}

/**
 * Decide whether a transcript line should count toward a wake.
 * @param {{speaker?:string, names?:string[], text?:string}} line   `names`: extra identities (e.g. Discord username)
 * @param {ReturnType<typeof readSpotlight>} spot
 * @returns {{wake:boolean, reason:'open_floor'|'spotlight_player'|'wake_word'|'spotlight', override:boolean}}
 */
export function decide(line, spot) {
  if (!spot?.active) return { wake: true, reason: 'open_floor', override: false };
  const wanted = [spot.player, ...(spot.aliases ?? [])];
  const names = [line.speaker, ...(line.names ?? [])];
  if (names.some((n) => wanted.some((w) => nameMatches(n, w)))) return { wake: true, reason: 'spotlight_player', override: false };
  if (hasWakeWord(line.text)) return { wake: true, reason: 'wake_word', override: true };
  return { wake: false, reason: 'spotlight', override: false };
}

/**
 * Build the filter used by GmWakeNotifier: `(line) => decision`. Reads the file on every line (tiny file) so
 * a change by the GM takes effect immediately. Logs state changes (and fail-open causes) once, never line text.
 */
export function createSpotlightFilter({ config, logger, now = () => Date.now() }) {
  let lastKey = null;
  const note = (spot) => {
    const key = spot.active ? `active:${spot.player}` : `open:${spot.reason}`;
    if (key === lastKey) return;
    lastKey = key;
    if (spot.active) logger?.info(`Spotlight ON: wake limited to the spotlight player (+ "AI" wake word)${spot.aliases?.length ? `, ${spot.aliases.length} alias(es)` : ''}`);
    else if (['malformed', 'unreadable', 'too_large', 'no_timestamp', 'bad_timestamp', 'error'].includes(spot.reason)) {
      logger?.warn(`Spotlight file problem (${spot.reason}): failing open, every line wakes the GM`);
    } else logger?.info(`Spotlight OFF (${spot.reason}): open floor, every line wakes the GM`);
  };
  return (line) => {
    try {
      if (!config?.enabled) return { wake: true, reason: 'open_floor', override: false };
      const spot = readSpotlight({ file: config.file, maxAgeMinutes: config.maxAgeMinutes, now: now() });
      note(spot);
      return decide(line, spot);
    } catch {
      return { wake: true, reason: 'open_floor', override: false }; // fail open, always
    }
  };
}
