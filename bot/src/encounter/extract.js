/**
 * /encounter extraction: turns a Floor day page (floors/fNN/day-NN.json) into the text players may see.
 *
 * SAFETY CONTRACT (Encounter Bot, audience/1): everything is GM-only unless it is named in
 * audience_manifest.player_blocks[]. For each manifest entry we read ONLY block[entry.field] (for set pieces, each
 * paragraph's `text`). Whole blocks are never printed: they carry GM metadata (hours_note, gm_note, source, status,
 * timing, canon_tag, title ...). Nothing else in the file is ever read for output. Files are loaded fresh on every call.
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

export const MAX_MESSAGE = 1900;      // Discord's limit is 2000; keep a margin
export const MAX_MESSAGES = 12;       // refuse to preview more than this at once (narrow the request instead)
export const SYSTEM_TAG = '**[SYSTEM]** ';
export const GM_TAG = '**[GM]** ';

/** Voice by manifest kind (decision 032 / Caleb Oct 5 2026): dry System lines get **[SYSTEM]**; everything else is narrator/GM.
 * SYSTEM_KINDS is an allow-list only. Unknown or new kinds (e.g. optional [GM] color beats Encounter Bot may add) are narration — never System.
 * Achievements and loot-box color are GM. Collapse/exit warnings stay System. */
const SYSTEM_KINDS = new Set(['voice_line', 'route_voice_line', 'system_notice', 'exit_warning_read_aloud']);
export { SYSTEM_KINDS };

export class EncounterError extends Error {}

const safeId = (s) => String(s).replace(/[^A-Za-z0-9_:.-]/g, '').slice(0, 60);
const own = (o, k) => o !== null && typeof o === 'object' && Object.prototype.hasOwnProperty.call(o, k);

export const pagePath = (campaignDir, floor, day) => join(campaignDir, 'floors', `f${String(floor).padStart(2, '0')}`, `day-${String(day).padStart(2, '0')}.json`);

/** Load a day page fresh from disk. Friendly EncounterError for anything wrong; never throws anything else. */
export function loadPage(campaignDir, floor, day) {
  if (!Number.isInteger(floor) || floor < 1 || floor > 18) throw new EncounterError('Floor must be a whole number from 1 to 18.');
  if (!Number.isInteger(day) || day < 1 || day > 5) throw new EncounterError('Day must be a whole number from 1 to 5.');
  const file = pagePath(campaignDir, floor, day);
  let raw;
  try {
    raw = readFileSync(file, 'utf8');
  } catch (err) {
    if (err.code === 'ENOENT') {
      throw new EncounterError(floor === 1
        ? `There is no page for Floor 1 Day ${day} yet (floors/f01/day-${String(day).padStart(2, '0')}.json is missing). The Encounter Bot may still be building it.`
        : `Only Floor 1 pages exist so far: there is no page for Floor ${floor} Day ${day}.`);
    }
    throw new EncounterError(`I could not read the Floor ${floor} Day ${day} page (${err.code || 'read error'}).`);
  }
  let doc;
  try { doc = JSON.parse(raw); } catch { throw new EncounterError(`The Floor ${floor} Day ${day} page is not valid JSON right now (it may be mid-rebuild). Try again in a moment.`); }
  const m = doc?.audience_manifest;
  if (!m || !Array.isArray(m.player_blocks)) throw new EncounterError(`The Floor ${floor} Day ${day} page has no audience manifest, so nothing on it can be shown to players safely.`);
  if (m.schema !== undefined && !/^audience\//.test(String(m.schema))) throw new EncounterError(`The Floor ${floor} Day ${day} page has an audience manifest I do not recognise (${safeId(m.schema)}).`);
  return doc;
}

/** Follow a JSON pointer through own properties only. Returns undefined when anything is missing. */
export function resolvePointer(doc, ptr) {
  if (typeof ptr !== 'string' || !ptr.startsWith('/')) return undefined;
  let o = doc;
  for (const seg of ptr.slice(1).split('/').map((s) => s.replace(/~1/g, '/').replace(/~0/g, '~'))) {
    if (Array.isArray(o)) {
      if (!/^\d+$/.test(seg) || Number(seg) >= o.length) return undefined;
      o = o[Number(seg)];
    } else if (own(o, seg)) o = o[seg];
    else return undefined;
  }
  return o;
}

const groupOf = (doc, e) => {
  if (typeof e.encounter === 'string' && e.encounter) return safeId(e.encounter);
  const m = /^\/routes\/(\d+)(\/|$)/.exec(e.path || '');
  if (m) {
    const id = doc.routes?.[Number(m[1])]?.id;
    return typeof id === 'string' && id ? safeId(id) : `route-${m[1]}`;
  }
  return 'day';
};

const slotOf = (e) => {
  const parts = String(e.path || '').split('/').filter(Boolean);
  if (e.kind === 'exit_warning_read_aloud') return 'floor_exit_warning';   // the key is called gm_warning but the text is read to the players
  if (e.kind === 'zone_color') return 'zone_color';
  if (e.kind === 'set_piece') return 'set_piece';
  if (e.kind === 'achievement_narration') return 'achievement';
  if (parts[0] === 'day') return parts.slice(1).join('_') || 'day';
  return parts[parts.length - 1] || e.kind;
};

/** Manifest entries with their group (encounter id, route id or 'day'), slot name and voice. Reads no block content. */
export function listEntries(doc) {
  return doc.audience_manifest.player_blocks
    .filter((e) => e && typeof e.path === 'string' && typeof e.kind === 'string' && typeof e.field === 'string')
    .map((e) => ({ ...e, group: groupOf(doc, e), slot: slotOf(e), voice: SYSTEM_KINDS.has(e.kind) ? 'system' : 'gm' }));
}

/** GM-side hint: which groups exist and which kind/slot NAMES each offers. No GM text, no player text. */
export function hintFor(doc) {
  const groups = new Map();
  for (const e of listEntries(doc)) {
    const g = groups.get(e.group) ?? { id: e.group, kinds: new Set(), slots: new Set() };
    g.kinds.add(e.kind);
    g.slots.add(e.slot);
    groups.set(e.group, g);
  }
  return [...groups.values()].map((g) => ({ id: g.id, kinds: [...g.kinds], slots: [...g.slots] }));
}

export function hintText(doc) {
  const rows = hintFor(doc).map((g) => `- \`${g.id}\`: ${g.kinds.join(', ')}`);
  return `Groups and block kinds on this page (\`encounter:\` takes the id, \`all\`, or nothing for the day-level notices; \`block:\` takes a kind or a slot name):\n${rows.join('\n')}`;
}

const fmtHours = (h) => String(Number(h));

/** Split one text into pieces of at most `max` characters, at sentence ends, then spaces, then hard. */
export function splitText(text, max) {
  if (text.length <= max) return [text];
  const out = [];
  let cur = '';
  const push = (s) => { if (s) out.push(s); };
  const words = text.split(/(?<=[.!?])\s+|\s+/).filter(Boolean);
  for (const w0 of words) {
    let w = w0;
    while (w.length > max) { push(cur); cur = ''; push(w.slice(0, max)); w = w.slice(max); }
    if (cur && cur.length + 1 + w.length > max) { push(cur); cur = w; } else cur = cur ? `${cur} ${w}` : w;
  }
  push(cur);
  return out;
}

/** Group items into Discord messages <= MAX_MESSAGE. In a message with any System line, narration lines carry [GM] so the voice tag stays right. */
export function toMessages(items, max = MAX_MESSAGE) {
  const reserve = Math.max(SYSTEM_TAG.length, GM_TAG.length);
  const pieces = [];
  for (const it of items) for (const p of splitText(it.text, max - reserve)) pieces.push({ voice: it.voice, text: p });
  const messages = [];
  let cur = [];
  let len = 0;
  const flush = () => {
    if (!cur.length) return;
    const mixed = cur.some((p) => p.voice === 'system');
    messages.push(cur.map((p) => (p.voice === 'system' ? SYSTEM_TAG : mixed ? GM_TAG : '') + p.text).join('\n\n'));
    cur = []; len = 0;
  };
  for (const p of pieces) {
    const cost = p.text.length + reserve;
    if (cur.length && len + 2 + cost > max) flush();
    len = cur.length ? len + 2 + cost : cost;
    cur.push(p);
  }
  flush();
  return messages;
}

/**
 * Build what players would see.
 * opts: { encounter?: string|'all', block?: string, includeOptional?: bool, hours?: number, confirm?: bool }
 * Returns { items, messages, notes[], error? }. error = a refusal the GM must fix (nothing is returned to post).
 */
export function buildPreview(doc, opts = {}) {
  const notes = [];
  const entries = listEntries(doc);
  const groups = [...new Set(entries.map((e) => e.group))];
  let scope;
  if (!opts.encounter) scope = (e) => e.group === 'day';
  else if (String(opts.encounter).toLowerCase() === 'all') scope = () => true;
  else {
    const want = groups.find((g) => g.toLowerCase() === String(opts.encounter).trim().toLowerCase());
    if (!want) return { items: [], messages: [], notes, error: `No encounter or route "${safeId(opts.encounter)}" on this page. Available: ${groups.map((g) => `\`${g}\``).join(', ')}.` };
    scope = (e) => e.group === want;
  }
  const blk = opts.block ? String(opts.block).trim().toLowerCase() : '';
  const picked = entries.filter((e) => scope(e) && (!blk || blk === 'all' || e.kind.toLowerCase() === blk || e.slot.toLowerCase() === blk));
  if (!picked.length) {
    return { items: [], messages: [], notes, error: blk && !['all'].includes(blk) && entries.some((e) => scope(e))
      ? `No "${safeId(blk)}" block in that scope.` : 'Nothing player-facing in that scope.' };
  }

  const hasHours = opts.hours !== undefined && opts.hours !== null && Number.isFinite(Number(opts.hours));
  const items = [];
  let skippedOptional = 0;
  const waiting = new Map();
  const unfilled = [];
  for (const e of picked) {
    const need = Array.isArray(e.needs_fill) ? e.needs_fill : [];
    if (need.includes('hours') && !hasHours) {
      return { items: [], messages: [], notes, error: `The ${e.slot.replace(/_/g, ' ')} has an {hours} placeholder the GM fills. Re-run with \`hours:<number>\` (in-game hours left before the collapse). Nothing was shown.` };
    }
    const other = need.filter((n) => n !== 'hours');
    if (other.length) { unfilled.push(`${e.slot} (needs ${other.map(safeId).join(', ')})`); continue; }
    if (e.show_only_when && !opts.confirm) {
      const k = String(e.show_only_when).slice(0, 140);
      waiting.set(k, (waiting.get(k) ?? 0) + 1);
      continue;
    }
    if (e.optional === true && !opts.includeOptional) { skippedOptional += 1; continue; }
    const block = resolvePointer(doc, e.path);
    const value = own(block, e.field) ? block[e.field] : undefined;     // ONLY the named field of the block
    const texts = [];
    if (typeof value === 'string') texts.push(value);
    else if (Array.isArray(value)) {
      value.forEach((p, i) => {
        const text = typeof p === 'string' ? p : own(p, 'text') && typeof p.text === 'string' ? p.text : null;
        if (text === null) return;
        const optionalPara = (Array.isArray(e.paragraphs_optional) && e.paragraphs_optional[i] === true) || (p !== null && typeof p === 'object' && p.optional === true);
        if (optionalPara && !opts.includeOptional) { skippedOptional += 1; return; }
        texts.push(text);
      });
    }
    for (let t of texts) {
      t = t.trim();
      if (!t) continue;
      if (hasHours) t = t.replace(/\{hours\}/g, fmtHours(opts.hours));
      const left = t.match(/\{[A-Za-z_]+\}/);
      if (left) { unfilled.push(`${e.slot} (still has ${left[0]})`); continue; }
      items.push({ voice: e.voice, kind: e.kind, slot: e.slot, group: e.group, text: t });
    }
  }
  if (skippedOptional) notes.push(`${skippedOptional} optional line${skippedOptional === 1 ? '' : 's'} skipped. Add \`include_optional:true\` to show ${skippedOptional === 1 ? 'it' : 'them'}.`);
  for (const [cond, n] of waiting) notes.push(`${n} block${n === 1 ? '' : 's'} held back: shown only when ${cond}. Add \`confirm:true\` once that is true.`);
  if (unfilled.length) notes.push(`Skipped (not filled): ${unfilled.join('; ')}.`);
  return { items, messages: toMessages(items), notes };
}
