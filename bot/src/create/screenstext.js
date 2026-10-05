/**
 * Display text for the later /create screens (S3/S4, S6 choices, S8 onward, nav, dialogs, errors, notices, help): Lore's tables/create-screens-reskins.json
 * (schema create-screens-reskins/0.1.0, entries[] = one UI string each: id, screen, kind, state label|text, old, new, placeholders, old_placeholders, chargen_ref, code_ref)
 * plus the proposed create-flow-lines (tables/create-flow-lines.proposed.json). A layer of the display mechanism (layers.js), behind its OWN flag
 * session.json create.screens_reskin (exactly true; default OFF until Caleb approves). DISPLAY ONLY: ids, select values, custom ids, numbers, state, the ledger and the
 * rules never change; with the flag off, or any id/placeholder missing, every string is the current text, byte for byte.
 *
 * tx(t, id, fallback, vars): `fallback` is the CURRENT literal at the call site. The row's `new` is used only when
 *   - the layer is on and the row exists and has a usable `new`;
 *   - the row's `old` still matches the call site's current text (drift guard: if the code changed after Lore wrote the row, the code wins);
 *   - every {placeholder} in `new` is supplied in vars (otherwise the current text, so a table typo can never show "{x}");
 *   - every rule number that the old text had (73, 4d6, 20, 27, 8-15, ...) is still in `new` (checked once when the layer loads; a violating row is dropped).
 * txd(t, id, plain): for strings that come from chargen data (choice groups, fighting styles, invocations, abilities, methods): same, `plain` is the data value.
 */
import { buildLayerIndex, registerLayer } from './layers.js';

const PH = /\{(\w+)\}/g;
const nums = (s) => {
  const m = new Map();
  for (const n of String(s).replace(PH, '').match(/\d+/g) ?? []) m.set(n, (m.get(n) ?? 0) + 1);
  return m;
};
const keepsNumbers = (oldText, newText) => {
  const a = nums(oldText);
  const b = nums(newText);
  for (const [n, c] of a) if ((b.get(n) ?? 0) < c) return false;
  return true;
};
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const oldRe = new WeakMap();
/** Does the call site's current text still have the shape of the row's `old` (placeholders match anything)? */
function matchesOld(e, text) {
  let re = oldRe.get(e);
  if (!re) {
    re = new RegExp(`^${String(e.old).split(PH).map((part, i) => (i % 2 ? '[\\s\\S]*?' : esc(part))).join('')}$`);
    oldRe.set(e, re);
  }
  return re.test(text);
}

/** Debug/test trace: which ids were used and which fell back because the call site no longer matches `old`. */
export const TRACE = { on: false, hit: new Set(), drift: new Map() };

export function buildScreensIndex(json, { enabled = true } = {}) {
  const base = buildLayerIndex(json, { enabled });
  const byId = new Map();
  const dropped = [];
  for (const [id, e] of base.byId) {
    if (typeof e.new !== 'string' || !e.new.trim() || typeof e.old !== 'string') { dropped.push(id); continue; }
    if (!keepsNumbers(e.old, e.new)) { dropped.push(id); continue; }   // a rule number was lost: never shown
    byId.set(id, e);
  }
  return { ...base, byId, loaded: byId.size > 0, dropped };
}

export function tx(t, id, fallback, vars = {}) {
  try {
    const e = t?.screens?.byId?.get(id);
    if (!e) return fallback;
    if (t.plainView && e.plain_on?.includes(t.plainView)) return fallback;   // Lore's plain_on: S1, S2, S13 and the comfort-only view keep the old text
    const fb = String(fallback);
    if (!matchesOld(e, fb)) { if (TRACE.on) TRACE.drift.set(id, fb.slice(0, 80)); return fallback; }
    let bad = false;
    const out = e.new.replace(PH, (_, k) => { if (vars[k] === undefined || vars[k] === null) { bad = true; return ''; } return String(vars[k]); });
    if (bad) { if (TRACE.on) TRACE.drift.set(id, `placeholder missing in ${e.new.slice(0, 60)}`); return fallback; }
    if (TRACE.on) TRACE.hit.add(id);
    return out;
  } catch { return fallback; }
}

/** A string from chargen data: the row applies only when its `old` is exactly that data value. */
export function txd(t, id, plain) {
  try {
    const e = t?.screens?.byId?.get(id);
    if (e && t.plainView && e.plain_on?.includes(t.plainView)) return plain;
    if (!e || e.old !== plain) { if (e && TRACE.on) TRACE.drift.set(id, String(plain)); return plain; }
    if (TRACE.on) TRACE.hit.add(id);
    return e.new;
  } catch { return plain; }
}

/** The tables as seen from one view (a screen id or 'comfort_only'): rows whose plain_on lists that view show their old text. A shallow copy, the tables object itself is never changed. */
export const viewT = (t, screen, comfortOnly = false) => (t?.screens?.byId?.size ? { ...t, plainView: comfortOnly ? 'comfort_only' : screen } : t);

export const SCREENS_LAYER = registerLayer({ id: 'screens', file: 'create-screens-reskins.json', flag: 'screens_reskin', env: 'CREATE_SCREENS_RESKINS_PATH', tkey: 'screens', build: buildScreensIndex });

// ------------------------------------------------------------------ the proposed create-flow-lines (same keys, same placeholders, same numbers)
function vars(s) { return new Set([...String(s).matchAll(PH)].map((m) => m[1])); }
const sameSet = (a, b) => a.size === b.size && [...a].every((x) => b.has(x));

/** Index of the proposed lines file: { lines: {key: [variants]}, loaded }. Disabled / odd file -> empty. */
export function buildLinesIndex(json, { enabled = true } = {}) {
  const lines = enabled && json?.lines && typeof json.lines === 'object' ? json.lines : {};
  return { lines, loaded: Object.keys(lines).length > 0, version: json?.meta?.version ?? null };
}
export const LINES_LAYER = registerLayer({
  id: 'screens_lines', file: 'create-flow-lines.proposed.json', flag: 'screens_reskin', env: 'CREATE_FLOW_LINES_PROPOSED_PATH', tkey: 'proposedLines', build: buildLinesIndex,
  versionFile: 'create-screens-reskins.version.json', wantSha: (v) => v?.companions?.['tables/create-flow-lines.proposed.json']?.sha256,
});

/**
 * Merge the proposed lines over the current create-flow-lines object ({meta, lines, survey}) without mutating it. A key is taken only when the current table has it, the
 * proposed value is a non-empty array of non-empty strings, and every variant keeps the current key's placeholders and rule numbers (otherwise the current lines stay).
 * Returns the same object when nothing applies (flag off = identical).
 */
export function mergeProposedLines(lines, proposed) {
  if (!proposed?.loaded) return lines;
  const next = {};
  for (const [k, cur] of Object.entries(lines.lines ?? {})) {
    const p = proposed.lines[k];
    if (!Array.isArray(cur) || !Array.isArray(p) || !p.length || p.some((x) => typeof x !== 'string' || !x.trim())) continue;
    const want = new Set(cur.flatMap((x) => [...vars(x)]));
    if (p.some((x) => !sameSet(vars(x), want)) || p.some((x) => !cur.some((c) => keepsNumbers(c, x)))) continue;
    next[k] = p;
  }
  return Object.keys(next).length ? { ...lines, lines: { ...lines.lines, ...next }, appliedProposed: Object.keys(next) } : lines;
}
