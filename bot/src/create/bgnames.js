/**
 * Background (S7 "Prior Employment") display names for /create ("Our Name (5e Name)"): the sibling of names.js (species/classes) and reskin.js (items).
 *
 * Source: tables/background-reskins.json (DCC Lore; entries[] as in the header below) plus
 * background-reskins.version.json. DISPLAY ONLY: the ids, the values behind every select, state.json, the ledger, dice and rules keep the plain 5e names.
 * OFF unless the session says create.background_reskin === true (default false until Caleb approves). Read by file mtime, so an edit or a drop-in shows without a
 * restart (the bridge CODE needs one restart once). A missing file, entry or text shows the plain 5e name/text; nothing throws; nothing is blank.
 *
 * Lore's format (background-reskins/0.1.0, entries[]: id, kind, parent_id, srd_name, display_name, combined_label, chargen_value, flavor, optional label_name/chargen_job):
 *   kind 'background'  id = the lower-cased chargen background key ('acolyte'); chargen_value = the key
 *   kind 'choice'      parent_id 'origin-feat'     id 'feat-<kebab origin feat>' ('feat-magic-initiate-cleric'); chargen_value = the exact origin_feats string
 *                      parent_id 'background-asi'  id 'asi-2-1' / 'asi-1-1-1' (the "+2 / +1" and "+1 / +1 / +1" bonus picks)
 *                      parent_id 'background-kit'  id 'package-a' / 'package-b' (shared by all backgrounds); chargen_value = the package id 'A' / 'B'
 * Lookup is by id, else by (kind, parent_id, chargen_value). Lore's combined_label already avoids nested parentheses (label_name); flatParens() is a safety net so a label never nests.
 */
import { kid, MAX_LABEL } from './names.js';
import { buildLayerIndex, checkLayerHash, layerEntry, layerPath, registerLayer } from './layers.js';

export const BG_KINDS = ['background', 'choice'];
export const CHOICE_PARENTS = ['origin-feat', 'background-asi', 'background-kit'];
// what to look a thing up by: { id, kind, parent, value } (value = the entry's chargen_value)
export const bgRef = (name) => ({ id: kid(name), kind: 'background', parent: null, value: String(name) });
export const featRef = (name) => ({ id: `feat-${kid(name)}`, kind: 'choice', parent: 'origin-feat', value: String(name) });
export const asiRef = (type) => (type === '1-1-1' ? { id: 'asi-1-1-1', kind: 'choice', parent: 'background-asi', value: '+1 / +1 / +1' } : { id: 'asi-2-1', kind: 'choice', parent: 'background-asi', value: '+2 / +1' });
export const packageRef = (pkg) => ({ id: `package-${kid(pkg)}`, kind: 'choice', parent: 'background-kit', value: String(pkg) });

/** Never nest parentheses: an inner "(x)" becomes " - x". Balanced or not, the result has at most one level. */
export function flatParens(text) {
  let depth = 0;
  let out = '';
  for (const ch of String(text ?? '')) {
    if (ch === '(') { depth += 1; out += depth === 1 ? '(' : ' - '; continue; }
    if (ch === ')') { if (depth === 0) continue; depth -= 1; out += depth === 0 ? ')' : ''; continue; }
    out += ch;
  }
  return out.replace(/\s+-\s+/g, ' - ').replace(/\s+/g, ' ').trim();
}

/** Index the table (the generic layer index): null/odd table, or enabled=false -> empty index: everything falls back to the plain text. */
export const buildBgIndex = buildLayerIndex;

const clean = (s) => (typeof s === 'string' ? s.replace(/\s+/g, ' ').trim() : '');

/** "Our Name (5e Name)" of an entry (combined_label as written, parentheses flattened), or null with no usable text. Over 100 characters it cuts the display name. */
function entryLabel(e) {
  const display = clean(e?.display_name);
  const srd = flatParens(clean(e?.label_name) || clean(e?.srd_name));
  const text = flatParens(clean(e?.combined_label)) || (display && srd ? `${display} (${srd})` : display);
  if (!text) return null;
  if (text.length <= MAX_LABEL) return text;
  return display && srd ? `${display.slice(0, Math.max(10, MAX_LABEL - srd.length - 5))}… (${srd})`.slice(0, MAX_LABEL) : `${text.slice(0, MAX_LABEL - 1)}…`;
}

/** The entry for a ref: by id (kind and parent must match: a wrong-kind entry is ignored), else by (kind, parent, chargen_value). */
/** The entry for a ref: by id (kind and parent must match: a wrong-kind entry is ignored), else by (kind, parent, chargen_value). */
const find = (t, ref) => layerEntry(t, 'bgnames', ref);

/** The label for a ref, else the plain text. Never throws. */
function lab(t, ref, plain) {
  try { return entryLabel(find(t, ref)) ?? String(plain ?? ''); } catch { return String(plain ?? ''); }
}

export const backgroundLabel = (t, name) => lab(t, bgRef(name), name);
export const featLabel = (t, name) => lab(t, featRef(name), name);
/** The bonus-choice label: "Our Name (+2 / +1): +2 INT / +1 WIS"; plain = the rules text ("+2 INT / +1 WIS"), always kept. */
export function asiLabel(t, type, plain) {
  try {
    const l = entryLabel(find(t, asiRef(type)));
    return l ? `${l}: ${plain}`.slice(0, MAX_LABEL) : plain;
  } catch { return plain; }
}
/** A starting-gear package (Package A / B are shared by all backgrounds): "Our Name (Package A) - 8 GP left over"; plain = the existing label. */
export function packageLabel(t, pkg, gpText, plain) {
  try {
    const l = entryLabel(find(t, packageRef(pkg)));
    return l ? `${l} - ${gpText}`.slice(0, MAX_LABEL) : plain;
  } catch { return plain; }
}

/** The flavor line of a ref (or '' when there is none/the table is off). Cut to max (a select description) when given. */
export function flavorOf(t, ref, max = 0) {
  try {
    const f = clean(find(t, ref)?.flavor);
    return max && f.length > max ? `${f.slice(0, max - 1)}…` : f;
  } catch { return ''; }
}
export const backgroundFlavor = (t, name, max = 0) => flavorOf(t, bgRef(name), max);
export const featFlavor = (t, name, max = 0) => flavorOf(t, featRef(name), max);
export const asiFlavor = (t, type, max = 0) => flavorOf(t, asiRef(type), max);
export const packageFlavor = (t, pkg, max = 0) => flavorOf(t, packageRef(pkg), max);

// ----------------------------------------------------------------- loading + hash check (the generic layer mechanism, layers.js)
export const BG_LAYER = registerLayer({ id: 'background', file: 'background-reskins.json', flag: 'background_reskin', env: 'BACKGROUND_RESKINS_PATH', tkey: 'bgnames', build: buildBgIndex });
export const bgNamesPath = (campaignDir, env = process.env) => layerPath(BG_LAYER, campaignDir, env);
export const checkBgNamesHash = (campaignDir, env = process.env) => checkLayerHash(BG_LAYER, campaignDir, env);
