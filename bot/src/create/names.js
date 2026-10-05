/**
 * Species / lineage / class / class-option display names for /create ("Our Name (5e Name)"), the sibling of the item reskin layer (reskin.js).
 *
 * Source: tables/species-class-reskins.json (DCC Lore, schema species-class-reskins/0.1.0; entries[] with id, kind, parent_id, srd_name, display_name,
 * combined_label, nation, flavor, spoken) plus species-class-reskins.version.json. The campaign copy is NOT put in place until Caleb approves the names;
 * with no file everything shows the plain 5e name. Read by file mtime like the other tables, so an edit shows without a restart. The kill switch is
 * session.json create.species_class_reskin = false.
 *
 * Ids follow Lore's scheme (lower-cased kebab-case): species 'elf', class 'wizard', lineage '<species>-<option without " Elf"/" Gnome">' ('elf-high',
 * 'dragonborn-black'), class option '<class>-<option>' ('cleric-protector'). The label is the entry's combined_label (never rebuilt or hard-coded here);
 * a missing entry, or one without usable text, shows the plain 5e name. Nothing throws and nothing is blank. state.json, the ledger, dice, stats and
 * rules keep the plain 5e names.
 */
import { checkLayerHash, layerPath, registerLayer } from './layers.js';

export const MAX_LABEL = 100;   // Discord select option label limit

/** Lore's id scheme (tools/species_class_check.py kid()): lower case, apostrophes dropped, runs of non-alphanumerics become one '-'. */
export const kid = (s) => String(s ?? '').toLowerCase().replace(/'/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
export const lineageId = (species, option) => kid(`${species}-${String(option ?? '').replace(/ Elf/g, '').replace(/ Gnome/g, '')}`);
export const classOptionId = (cls, option) => kid(`${cls}-${option}`);

/** Index the table: { byId, byName, lineages, version, loaded }. A null/odd table (or enabled=false) gives an empty index: every lookup falls back to the plain name.
 *  Entry kinds: species, species_lineage (base_id = its species, chargen_value = the exact chargen option), species_variant (base_id = the species it is
 *  display-only for; /create never offers variants), class, class_option. */
export function buildNameIndex(json, { enabled = true } = {}) {
  const byId = new Map();
  const byName = new Map();
  const lineages = new Map();   // `${base_id}|${chargen_value}` -> entry
  const list = enabled && Array.isArray(json?.entries) ? json.entries : [];
  for (const e of list) {
    if (!e || typeof e.id !== 'string' || !e.id) continue;
    if (!byId.has(e.id)) byId.set(e.id, e);
    if (typeof e.srd_name === 'string' && (e.kind === 'species' || e.kind === 'class') && !byName.has(e.srd_name.toLowerCase())) byName.set(e.srd_name.toLowerCase(), e);
    if (e.kind === 'species_lineage' && typeof e.base_id === 'string' && typeof e.chargen_value === 'string') {
      const k = `${e.base_id}|${e.chargen_value}`;
      if (!lineages.has(k)) lineages.set(k, e);
    }
  }
  return { byId, byName, lineages, version: json?.meta?.version ?? null, loaded: byId.size > 0 };
}

/** combined_label ("Our Name (5e Name)") of an entry, or null when it has no usable text. A label over 100 characters keeps its parenthesis by cutting the display name. */
function entryLabel(e) {
  const combined = typeof e?.combined_label === 'string' ? e.combined_label.replace(/\s+/g, ' ').trim() : '';
  const display = typeof e?.display_name === 'string' ? e.display_name.replace(/\s+/g, ' ').trim() : '';
  const srd = typeof e?.srd_name === 'string' ? e.srd_name.trim() : '';
  const text = combined || (display && srd ? `${display} (${srd})` : display);
  if (!text) return null;
  if (text.length <= MAX_LABEL) return text;
  return display && srd ? `${display.slice(0, Math.max(10, MAX_LABEL - srd.length - 5))}… (${srd})`.slice(0, MAX_LABEL) : `${text.slice(0, MAX_LABEL - 1)}…`;
}

/** The label for an id of the wanted kind, else (species/class only) for the 5e name, else the plain 5e name. A wrong-kind entry (e.g. a variant id) is ignored. */
export function nameLabel(t, id, plainName, { byName = false, kind = null, entry = null } = {}) {
  const plain = String(plainName ?? '').trim() || String(id ?? '').replace(/-/g, ' ') || 'Unknown';
  try {
    const idx = t?.names;
    let e = entry ?? idx?.byId?.get(id) ?? (byName ? idx?.byName?.get(plain.toLowerCase()) : null);
    if (e && kind && e.kind !== kind) e = null;
    return entryLabel(e) ?? plain;
  } catch {
    return plain;
  }
}

export const speciesLabel = (t, name) => nameLabel(t, kid(name), name, { byName: true, kind: 'species' });
export const classLabel = (t, name) => nameLabel(t, kid(name), name, { byName: true, kind: 'class' });
/** Lineage by its exact chargen option string under its species (Lore's base_id + chargen_value), else by the computed id. */
export const lineageLabel = (t, species, option) => nameLabel(t, lineageId(species, option), option, { kind: 'species_lineage', entry: t?.names?.lineages?.get(`${kid(species)}|${option}`) ?? null });
export const classOptionLabel = (t, cls, option) => nameLabel(t, classOptionId(cls, option), option, { kind: 'class_option' });

/** Variants (rules/30: Felid = Cat, Cat Girl, Tigran, Were-Cat) are DISPLAY-ONLY: /create does not offer them (Floor 3 Offer, decision 009). For cards/sheets that
 *  later keep a variant_id: its label, and the base id every rule, state.json and the ledger must use instead. */
export const variantLabel = (t, variantId, plainName) => nameLabel(t, variantId, plainName, { kind: 'species_variant' });
export const baseIdOf = (t, id) => {
  const e = t?.names?.byId?.get(id);
  return e && (e.kind === 'species_variant' || e.kind === 'species_lineage') && typeof e.base_id === 'string' ? e.base_id : id;
};
/** Class choices that rename a branch of the class (Cleric Divine Order, Druid Primal Order); every other choice (fighting style, masteries...) stays plain. */
export const BRANCH_CHOICES = new Set(['divine_order', 'primal_order']);

// ----------------------------------------------------------------- loading + hash check (the generic layer mechanism, layers.js)
export const NAMES_LAYER = registerLayer({ id: 'species_class', file: 'species-class-reskins.json', flag: 'species_class_reskin', env: 'SPECIES_CLASS_RESKINS_PATH', tkey: 'names', build: buildNameIndex });
export const namesPath = (campaignDir, env = process.env) => layerPath(NAMES_LAYER, campaignDir, env);
/** sha256 of species-class-reskins.json must equal the sha256 in species-class-reskins.version.json (Lore's build). No file = 'absent' (the feature is simply off). */
export const checkNamesHash = (campaignDir, env = process.env) => checkLayerHash(NAMES_LAYER, campaignDir, env);
