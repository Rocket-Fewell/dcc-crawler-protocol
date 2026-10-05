/**
 * Display layers for /create: ONE mechanism to load a Lore display table (or string overrides) from the campaign tables/ dir behind its own session flag.
 *
 * A layer = { id, file, flag, env, tkey, build }:
 *   id    short name ('species_class', 'background', later 'abilities', 'skills', 'equipment', 'spells', 'messages', ...)
 *   file  tables/<file>.json, with <file>.version.json beside it (sha256 of the table, written by Lore's build)
 *   flag  session.json -> create.<flag>; the layer is ON only when that is exactly true (default OFF until Caleb approves)
 *   env   optional env var that overrides the file path (tests, trials)
 *   tkey  the key under which the loaded index sits on the tables object (t.names, t.bgnames, t.<tkey>)
 *   wantSha optional (versionJson) -> the sha256 this table must have (default versionJson.sha256; a companion file uses its entry in a shared version file)
 *   build (json, {enabled}) -> index; default buildLayerIndex. A flag-off layer gets an EMPTY index, so every lookup falls back to the current plain text.
 * Adding a layer is one registerLayer() call; data.js loads every registered layer on each request (read by file mtime, no restart), settings.js reads every flag,
 * src/index.js logs every layer's hash check at startup. DISPLAY ONLY: ids, select values, state.json, the ledger and the rules never change.
 *
 * Generic entry shape (Lore's tables): { id, kind, parent_id, srd_name, display_name, combined_label, chargen_value, flavor, label_name, ... } for names, and for string
 * overrides { screen: 'S8', id: 'roll_button', text: '...' } (optional {var} placeholders). Lookups: layerEntry (id, else kind+parent+chargen_value) and layerText (screen+id).
 * Nothing here throws; a missing layer, entry, field or placeholder gives the caller's fallback.
 */
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

export const LAYERS = new Map();

export function registerLayer(spec) {
  const s = { versionFile: spec.file.replace(/\.json$/, '.version.json'), build: buildLayerIndex, ...spec };
  LAYERS.set(s.id, s);
  return s;
}

const strOr = (v, d = '') => (typeof v === 'string' ? v : d);

/** Generic index: byId, byValue (`kind|parent_id|chargen_value`), byScreen (`screen|id`). null/odd table or enabled=false -> empty. */
export function buildLayerIndex(json, { enabled = true } = {}) {
  const byId = new Map();
  const byValue = new Map();
  const byScreen = new Map();
  const list = enabled && Array.isArray(json?.entries) ? json.entries : [];
  for (const e of list) {
    if (!e || typeof e !== 'object') continue;
    if (typeof e.id === 'string' && e.id) {
      if (!byId.has(e.id)) byId.set(e.id, e);
      if (typeof e.screen === 'string' && e.screen && !byScreen.has(`${e.screen}|${e.id}`)) byScreen.set(`${e.screen}|${e.id}`, e);
    }
    if (typeof e.chargen_value === 'string') { const k = `${e.kind}|${e.parent_id ?? ''}|${e.chargen_value}`; if (!byValue.has(k)) byValue.set(k, e); }
  }
  return { byId, byValue, byScreen, loaded: byId.size > 0, version: json?.meta?.version ?? null };
}

export const layerPath = (spec, campaignDir, env = process.env) => (spec.env && env[spec.env]) || join(campaignDir, 'tables', spec.file);

/** The flags of every registered layer for a session's create settings object: { id: true|false } (true only when exactly true). */
export const layerFlags = (create) => Object.fromEntries([...LAYERS.values()].map((s) => [s.id, create?.[s.flag] === true]));

/** Load every registered layer: { [tkey]: index }. loadJson(path, optional) is data.js's mtime cache; on: { [layerId]: boolean }. A broken file is ignored (empty index). */
export function loadLayers(campaignDir, on, loadJson, env = process.env) {
  const out = {};
  for (const s of LAYERS.values()) {
    try { out[s.tkey] = s.build(loadJson(layerPath(s, campaignDir, env), true), { enabled: on?.[s.id] === true }); } catch { out[s.tkey] = s.build(null, { enabled: false }); }
  }
  return out;
}

/** sha256 of the table must equal the sha256 in its version file. No file = 'absent' (the layer is simply off); mismatch = 'fail' (a warning in the log, never a crash). */
export function checkLayerHash(spec, campaignDir, env = process.env) {
  const table = layerPath(spec, campaignDir, env);
  const versionFile = join(table, '..', spec.versionFile);
  const nm = spec.file;
  const wantOf = spec.wantSha ?? ((v) => v?.sha256);
  if (!existsSync(table)) return { status: 'absent', message: `${nm} is not in place (not delivered/approved yet); the plain 5e text shows` };
  if (!existsSync(versionFile)) return { status: 'warn', message: `${spec.versionFile} not found; cannot verify the hash` };
  let want;
  try {
    want = wantOf(JSON.parse(readFileSync(versionFile, 'utf8')));
  } catch (err) {
    return { status: 'fail', message: `cannot read sha256 from ${spec.versionFile}: ${err.message}` };
  }
  if (typeof want !== 'string') return { status: 'warn', message: `${spec.versionFile} has no sha256 for ${nm}; cannot verify the hash` };
  const got = createHash('sha256').update(readFileSync(table)).digest('hex');
  return got === want
    ? { status: 'ok', message: `${nm} matches the version file (${want.slice(0, 12)})` }
    : { status: 'fail', message: `${nm} sha256 ${got.slice(0, 12)} does not match the version file ${String(want).slice(0, 12)}: a stale or edited copy? Re-copy Lore's file and version file together` };
}

/** Entry for a ref { id, kind, parent, value } in t[tkey]: by id (kind and parent must match), else by (kind, parent, chargen_value). */
export function layerEntry(t, tkey, ref) {
  try {
    const idx = t?.[tkey];
    const e = idx?.byId?.get(ref.id);
    if (e && (ref.kind == null || e.kind === ref.kind) && (ref.parent === undefined || (e.parent_id ?? null) === ref.parent)) return e;
    return ref.value != null ? idx?.byValue?.get(`${ref.kind}|${ref.parent ?? ''}|${ref.value}`) ?? null : null;
  } catch { return null; }
}

/**
 * String override by screen and id: the entry's `text` (or `label`) with {var} placeholders filled from vars. Any unfilled placeholder, a missing entry,
 * a layer that is off or a non-string gives `fallback` (the current text), so a typo in a table can never show "{x}" to a player.
 */
export function layerText(t, tkey, screen, id, fallback, vars = {}) {
  try {
    const e = t?.[tkey]?.byScreen?.get(`${screen}|${id}`);
    const raw = strOr(e?.text) || strOr(e?.label);
    if (!raw.trim()) return fallback;
    let bad = false;
    const out = raw.replace(/\{(\w+)\}/g, (_, k) => { if (vars[k] === undefined || vars[k] === null) { bad = true; return ''; } return String(vars[k]); });
    return bad ? fallback : out;
  } catch { return fallback; }
}
