/** Loads the shared /create tables from <campaign>/tables (chargen-5e.json, create-flow-lines.json, prebuilt-crawlers.json). */
import { readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { buildReskinIndex, checkReskinHash, reskinPath } from './reskin.js';
import './names.js';      // each of these registers its display layer (layers.js)
import './bgnames.js';
import { mergeProposedLines } from './screenstext.js';
import { money } from './money.js';
import { loadLayers } from './layers.js';
import { createSettings } from './settings.js';

const cache = new Map();

function loadJson(path, optional = false) {
  let mtime;
  try {
    mtime = statSync(path).mtimeMs;
  } catch (err) {
    if (optional) return null;
    throw new Error(`/create table missing: ${path}`);
  }
  const hit = cache.get(path);
  if (hit && hit.mtime === mtime) return hit.data;
  const data = JSON.parse(readFileSync(path, 'utf8'));
  cache.set(path, { mtime, data });
  return data;
}

/** Tables for one request, honouring the session's create.species_class_reskin switch (default OFF = plain 5e names; true shows Lore's names from tables/species-class-reskins.json). */
export function tablesFor(config) {
  let layers = {};
  try { layers = createSettings(config).layers; } catch { /* every layer defaults OFF */ }
  return loadTables(config.campaign.dir, { layers });
}

/** layers: { [layerId]: boolean } (see layers.js); legacy options: reskin = species_class (default true here), bgReskin = background (default false). Every other layer defaults OFF. */
export function loadTables(campaignDir, { reskin = true, bgReskin = false, layers = {} } = {}) {
  const dir = join(campaignDir, 'tables');
  const chargen = loadJson(join(dir, 'chargen-5e.json'));
  const lines = loadJson(join(dir, 'create-flow-lines.json'));
  const prebuilt = loadJson(join(dir, 'prebuilt-crawlers.json'), true) ?? { crawlers: [] };
  const reskins = buildReskinIndex(loadJson(reskinPath(campaignDir), true));
  for (const [k, it] of Object.entries(chargen.items ?? {})) if (reskins.offMenu.has(it.srd_id)) delete chargen.items[k];   // off-menu (non_srd pet items) never enter /create
  // display layers (species/class names, background names, later screens): each behind its own session flag, read by mtime, a broken file is ignored (plain text), never a crash
  const display = loadLayers(campaignDir, { species_class: reskin, background: bgReskin, ...layers }, loadJson);
  return { chargen, lines: mergeProposedLines(lines, display.proposedLines), prebuilt, reskins, ...display, version: chargen.meta?.version ?? '0' };
}

/** Stable "random" pick: the same user always sees the same variant of a line. */
export function line(tables, key, uid = '', vars = {}) {
  const arr = tables.lines.lines[key];
  if (!arr?.length) return '';
  const h = createHash('sha1').update(`${uid}:${key}`).digest()[0];
  const text = arr[h % arr.length];
  const out = text.replace(/\{(\w+)\}/g, (_, k) => (vars[k] ?? `{${k}}`));
  return key === 'S10' ? money(out) : out;   // the equipment intro line says cash/gold in the table: shown as credits (money.js), the table is not edited
}

export const ABILITIES = ['str', 'dex', 'con', 'int', 'wis', 'cha'];
export const ABILITY_NAMES = { str: 'Strength', dex: 'Dexterity', con: 'Constitution', int: 'Intelligence', wis: 'Wisdom', cha: 'Charisma' };

export function backgroundNames(tables, contentSource = 'phb') {
  const all = Object.keys(tables.chargen.backgrounds);
  return contentSource === 'srd' ? all.filter((b) => tables.chargen.srd_backgrounds.includes(b)) : all;
}
