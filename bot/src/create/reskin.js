/**
 * Item names, ids and prices for /create (spec S10, Caleb 2026-10-04).
 *
 * Source of truth for names: tables/item-reskins.json (Lore; a symlink into dcc-lore, never a copy), looked up by the stable SRD id.
 * Each chargen item (tables/chargen-5e.json) carries `srd_id`. The sheet stores the srd_id; dice, AC, weight and PRICES key off the id, never
 * the display name. The old chargen `junk` name is never read. Header ids (holy-symbol, gaming-set, musical-instrument, artisans-tools,
 * arcane-focus, druidic-focus; `resolve_to_variant: true` / `needs_variant_choice: true`) are NOT purchasable: a variant id must be picked first,
 * and a header is never shown priced, stored on a sheet or committed.
 */
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const low = (s) => String(s ?? '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

/** Index the item-reskins table (null/missing table = empty index; every lookup then falls back to the plain 5e name). */
export function buildReskinIndex(json) {
  const entries = Array.isArray(json?.entries) ? json.entries : [];
  const byId = new Map();
  const byKey = new Map();
  const byName = new Map();
  const offMenu = new Set();
  for (const e of entries) {
    if (!e?.srd_id) continue;
    byId.set(e.srd_id, e);
    // non_srd entries (Heal Critter potion, Pet Carrier) are OFF-MENU (decision 022): sold only by the GM-run pet shop, never typed, listed or priced in /create or on a vending wall.
    if (e.non_srd) { offMenu.add(e.srd_id); continue; }
    for (const k of e.chargen_keys ?? []) byKey.set(k, e);
    for (const n of [e.srd_name, e.display_name, e.combined_label, ...(e.legacy_names ?? [])]) if (n && !byName.has(low(n))) byName.set(low(n), e);
  }
  return { entries, byId, byKey, byName, offMenu, version: json?.meta?.version ?? null, loaded: entries.length > 0 };
}

/** True for a non_srd (off-menu) item: never listed, typed, priced or sold by /create or the vending wall. */
export const isOffMenu = (t, srdId) => !!srdId && (t.reskins?.offMenu.has(srdId) ?? false);

/** Drop every off-menu item from a chargen item map (defence in depth: a chargen item that points at a non_srd id is not purchasable). */
export function playerItems(t) {
  return Object.fromEntries(Object.entries(t.chargen.items).filter(([, it]) => !isOffMenu(t, it.srd_id)));
}

export const entryFor = (t, srdId) => t.reskins?.byId.get(srdId) ?? null;

/** The id that identifies a chargen item. For a header this is the header id until a variant is chosen. */
export const itemSrdId = (t, key) => t.chargen.items[key]?.srd_id ?? t.reskins?.byKey.get(key)?.srd_id ?? null;

/** True when a chargen key or srd id is a header placeholder (never purchasable, never stored). */
export function isHeaderKey(t, key) {
  const it = t.chargen.items[key];
  if (!it) return false;
  return !!(it.needs_variant_choice || it.srd_id_kind === 'header' || entryFor(t, it.srd_id)?.resolve_to_variant);
}
export const isHeaderId = (t, srdId) => !!entryFor(t, srdId)?.resolve_to_variant || [...Object.values(t.chargen.items)].some((it) => it.srd_id === srdId && (it.needs_variant_choice || it.srd_id_kind === 'header'));

/** Variant srd_ids of a header chargen key (chargen srd_variant_ids first, then the reskin table's `variants`). */
export function variantIds(t, key) {
  const it = t.chargen.items[key];
  const ids = it?.srd_variant_ids?.length ? it.srd_variant_ids : entryFor(t, it?.srd_id)?.variants ?? [];
  return ids.filter((id) => !!entryFor(t, id) || true);
}

/** Display label, never blank: combined_label, then the first legacy name, then the plain 5e name. */
export function labelFor(t, srdId, fallbackName = '') {
  const e = entryFor(t, srdId);
  const label = e?.combined_label || (e?.legacy_names ?? [])[0] || e?.srd_name || fallbackName || String(srdId ?? '').replace(/-/g, ' ');
  return String(label).trim() || 'Unnamed item';
}

/** The plain 5e name for an srd id (what the mechanics line is about). */
export const plainName = (t, srdId, fallbackName = '') => entryFor(t, srdId)?.srd_name || fallbackName || String(srdId ?? '').replace(/-/g, ' ');

/**
 * Price in copper for a resolved srd id: the variant's own base_price_cp. Header ids and unknown ids return null (not purchasable).
 * Chargen's cost_cp is used only as a fallback for a NON-header item whose reskin entry carries no price; a header's placeholder cost_cp is ignored.
 */
export function priceCp(t, srdId, key = null) {
  if (!srdId || isHeaderId(t, srdId) || isOffMenu(t, srdId)) return null;
  const e = entryFor(t, srdId);
  if (Number.isInteger(e?.base_price_cp)) return e.base_price_cp;
  const it = key ? t.chargen.items[key] : Object.values(t.chargen.items).find((x) => x.srd_id === srdId);
  if (it && !it.needs_variant_choice && it.srd_id_kind !== 'header' && Number.isInteger(it.cost_cp)) return it.cost_cp;
  return null;
}

/** Credit multiplier by floor (rules/10 section 3.9, same as tools/loot.py floor_multiplier): x1 F1-4, x5 F5-9, x20 F10-14, x50 F15+. */
export const floorMultiplier = (floor) => (floor >= 15 ? 50 : floor >= 10 ? 20 : floor >= 5 ? 5 : 1);

/** Resolve typed text to a variant srd id of the given header key ("lute", "Ukulele With Pretensions"). */
export function findVariant(t, key, text) {
  const n = low(text);
  if (!n) return null;
  const ids = variantIds(t, key);
  const names = (id) => [entryFor(t, id)?.srd_name, entryFor(t, id)?.display_name, entryFor(t, id)?.combined_label, ...(entryFor(t, id)?.legacy_names ?? []), id].map(low);
  const exact = ids.filter((id) => names(id).includes(n));
  if (exact.length === 1) return exact[0];
  const part = ids.filter((id) => names(id).some((x) => x.includes(n)));
  return part.length === 1 ? part[0] : null;
}

/** Find a chargen key by typed text via the reskin table: srd name, display name, combined label or legacy name. */
export function findKeyByReskinName(t, text) {
  const e = t.reskins?.byName.get(low(text));
  if (!e) return null;
  for (const k of e.chargen_keys ?? []) if (t.chargen.items[k]) return k;
  return Object.entries(t.chargen.items).find(([, it]) => it.srd_id === e.srd_id)?.[0] ?? null;
}

// ----------------------------------------------------------------- loading + hash check
export function reskinPath(campaignDir, env = process.env) {
  return env.ITEM_RESKINS_PATH || join(campaignDir, 'tables', 'item-reskins.json');
}

/** sha256 of item-reskins.json must equal the sha256 in Lore's item-reskins.version.json. Missing version file = warning only; mismatch = fail. */
export function checkReskinHash(campaignDir, env = process.env) {
  const table = reskinPath(campaignDir, env);
  const versionFile = env.ITEM_RESKINS_VERSION_PATH || join(table, '..', 'item-reskins.version.json');
  if (!existsSync(table)) return { status: 'missing', message: `item-reskins.json not found at ${table}; item names fall back to the plain 5e names` };
  if (!existsSync(versionFile)) return { status: 'warn', message: 'item-reskins.version.json not found; cannot verify the item-reskins hash' };
  let want;
  try {
    want = JSON.parse(readFileSync(versionFile, 'utf8')).sha256;
  } catch (err) {
    return { status: 'fail', message: `cannot read sha256 from item-reskins.version.json: ${err.message}` };
  }
  const got = createHash('sha256').update(readFileSync(table)).digest('hex');
  return got === want
    ? { status: 'ok', message: `item-reskins.json matches the version file (${want.slice(0, 12)})` }
    : { status: 'fail', message: `item-reskins.json sha256 ${got.slice(0, 12)} does not match the version file ${String(want).slice(0, 12)}: a divergent copy? Link it to Lore's file` };
}
