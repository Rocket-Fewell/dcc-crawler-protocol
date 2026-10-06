/**
 * NPC voice casting sheet -> <campaign>/tables/npc-voices.json (used by `npm run npc-voices:import`).
 *
 * Input: .xlsx (first sheet whose header row has a name column and a Fish voice id column) or .csv. Headers are matched
 * loosely (case, spaces and punctuation ignored); expected, roughly:
 *   Name (required; the canonical [NPC: Name] tag)  | Floor(s) | Who/what (note) | Fish Voice ID (required column)
 *   optional: Aliases | Voice notes / cue | Type | NPC ID | Fish Voice Name | anything else is ignored
 * Rows for the narrator and the System voice (Type "...already assigned", or named GM Narrator / The System) are skipped:
 * those voices stay on FISH_VOICE_ID_NARRATOR / FISH_VOICE_ID_SYSTEM. A Fish id may be pasted as the 32-hex id or as a
 * fish.audio URL containing it. A blank id keeps the NPC on the narrator voice.
 */
import { readFileSync } from 'node:fs';
import { extname } from 'node:path';
import { npcKey } from './tags.js';

export const FISH_ID = /^[0-9a-f]{32}$/;
const HEX32 = /[0-9a-f]{32}/i;
const norm = (h) => String(h ?? '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

/** Column roles, tried in order; the first header that matches a role wins it (a header serves one role). */
const ROLES = [
  ['fish_voice_id', (h) => /\bfish\b.*\bid\b|\b(voice|model|reference) id\b|^fish voice$/.test(h) && !/\bname\b/.test(h)],
  ['fish_voice_name', (h) => /\bfish\b.*\bname\b|\bvoice name\b/.test(h)],
  ['aliases', (h) => /\balias(es)?\b|\baka\b|\balso known\b/.test(h)],
  ['voice_cue', (h) => /\bvoice (notes?|cue|description|style)\b|\bcue\b|\btone\b/.test(h)],
  ['floors', (h) => /^floors?\b|^floor s$|\bfloor\(?s\)?$/.test(h) && !/\bsame\b/.test(h)],
  ['npc_id', (h) => /^npc id$|^id$|^npc no$|^npc number$/.test(h)],
  ['type', (h) => /^(type|kind|category|role type)$/.test(h)],
  ['note', (h) => /\bwho\b|\bwhat\b|\bdescription\b|^notes?$|^role$|^who what$/.test(h)],
  ['name', (h) => /^(npc )?name$|^character( name)?$|^npc$/.test(h)],
];

export function mapHeaders(headers) {
  const map = {};
  const used = new Set();
  for (const [role, test] of ROLES) {
    const i = headers.findIndex((h, n) => !used.has(n) && test(norm(h)));
    if (i >= 0) { map[role] = i; used.add(i); }
  }
  return map;
}

/** RFC 4180-ish CSV (quotes, doubled quotes, CRLF, a BOM). Returns string[][]. */
export function parseCsv(text) {
  const rows = [];
  let row = [], cell = '', q = false;
  const s = String(text).replace(/^\uFEFF/, '');
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (q) {
      if (c === '"' && s[i + 1] === '"') { cell += '"'; i++; } else if (c === '"') q = false; else cell += c;
    } else if (c === '"') q = true;
    else if (c === ',') { row.push(cell); cell = ''; }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && s[i + 1] === '\n') i++;
      row.push(cell); rows.push(row); row = []; cell = '';
    } else cell += c;
  }
  if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
  return rows;
}

/** Rows (string[][]) of the first usable sheet of an .xlsx/.csv file, with the sheet name. */
export async function readTable(file) {
  const ext = extname(file).toLowerCase();
  if (ext === '.csv') return { sheet: null, rows: parseCsv(readFileSync(file, 'utf8')) };
  if (ext !== '.xlsx') throw new Error(`unsupported file type "${ext}" (use .xlsx or .csv)`);
  const { default: ExcelJS } = await import('exceljs');
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.readFile(file);   // read-only: the workbook is never written back
  let first = null;
  for (const ws of wb.worksheets) {
    const rows = [];
    ws.eachRow({ includeEmpty: true }, (r, n) => {
      const out = [];
      for (let c = 1; c <= ws.columnCount; c++) out.push(String(r.getCell(c).text ?? '').trim());
      rows[n - 1] = out;
    });
    const dense = Array.from(rows, (r) => r ?? []);
    const t = { sheet: ws.name, rows: dense };
    first ??= t;
    if (findHeader(dense) >= 0) return t;
  }
  return first ?? { sheet: null, rows: [] };
}

/** Index of the header row (within the first 10 rows): it must have a name column and a Fish voice id column. */
export function findHeader(rows) {
  for (let i = 0; i < Math.min(rows.length, 10); i++) {
    const m = mapHeaders(rows[i] ?? []);
    if (m.name != null && m.fish_voice_id != null) return i;
  }
  return -1;
}

/** "F1, F2" / "1-3" / "All" -> [1, 2] / [1, 2, 3] / ["all"]. */
export function parseFloors(v) {
  const out = [];
  for (const part of String(v ?? '').split(/[,;/|]+|\band\b/i).map((x) => x.trim()).filter(Boolean)) {
    const r = /^f?(\d+)\s*[-–]\s*f?(\d+)$/i.exec(part);
    const one = /^(?:f|floor\s*)?(\d+)$/i.exec(part);
    if (r) { for (let n = +r[1]; n <= +r[2] && n - +r[1] < 30; n++) out.push(n); }
    else if (one) out.push(+one[1]);
    else out.push(part.toLowerCase());
  }
  return [...new Set(out)];
}

const splitList = (v) => String(v ?? '').split(/[,;|]+/).map((x) => x.trim()).filter(Boolean);
/** Job-title filler in long sheet names; dropping it gives the short alias ("Laminak Rev-Up Consultant Elite" -> "Laminak Elite"). */
export const ALIAS_FILLER = new Set(['rev', 'up', 'revup', 'consultant', 'unvaccinated']);

/** Candidate short aliases for a canonical name (collisions are removed later). */
export function autoAliases(name) {
  const out = [];
  const n = String(name).trim();
  const noParen = n.replace(/\s*\([^)]*\)\s*/g, ' ').trim();
  if (/^the\s+\S/i.test(noParen)) out.push(noParen.replace(/^the\s+/i, ''));                  // The Owners -> Owners
  const xthe = /^(\S+)\s+the\s+\S/i.exec(noParen);
  if (xthe) out.push(xthe[1]);                                                                 // Bruiser the Mascot -> Bruiser
  if (noParen !== n) out.push(noParen);                                                        // Exit Greeter (Trainee) -> Exit Greeter (dropped if taken)
  const words = noParen.split(/\s+/);
  if (words.length >= 3) {
    const kept = words.filter((w) => !w.toLowerCase().split(/[^a-z0-9]+/).filter(Boolean).every((p) => ALIAS_FILLER.has(p)));
    if (kept.length && kept.length < words.length) out.push(kept.join(' '));                   // Unvaccinated Clurichaun Rev-Up Consultant -> Clurichaun
  }
  return [...new Set(out)].filter((a) => npcKey(a) && npcKey(a) !== npcKey(n));
}

const SKIP_NAMES = new Set(['gm narrator', 'narrator', 'the narrator', 'gm', 'the system', 'system', 'system voice']);
const isEnvVoiceRow = (name, type) => SKIP_NAMES.has(npcKey(name)) || /already assigned/i.test(type ?? '');

/** Build entries + a report from table rows. */
export function buildEntries(rows) {
  const h = findHeader(rows);
  const report = { headerRow: h + 1, columns: {}, rows: 0, imported: 0, withId: 0, blankId: [], invalidId: [], skippedEnv: [], skippedBlank: 0, duplicates: [], aliases: [], aliasCollisions: [] };
  if (h < 0) throw new Error('no header row with a Name column and a Fish Voice ID column in the first 10 rows');
  const headers = rows[h];
  const m = mapHeaders(headers);
  for (const [role, i] of Object.entries(m)) report.columns[role] = headers[i];
  const cell = (r, role) => (m[role] == null ? '' : String(r[m[role]] ?? '').trim());
  const entries = [];
  const seen = new Map();
  for (let i = h + 1; i < rows.length; i++) {
    const r = rows[i] ?? [];
    if (!r.some((c) => String(c ?? '').trim())) { report.skippedBlank++; continue; }
    report.rows++;
    const name = cell(r, 'name').replace(/\s+/g, ' ');
    if (!name) { report.skippedBlank++; report.rows--; report.blankName = (report.blankName ?? 0) + 1; continue; }
    const line = i + 1;
    if (isEnvVoiceRow(name, cell(r, 'type'))) { report.skippedEnv.push(`${name} (row ${line})`); continue; }
    if (seen.has(npcKey(name))) { report.duplicates.push(`${name} (row ${line}, first on row ${seen.get(npcKey(name))})`); continue; }
    seen.set(npcKey(name), line);
    const rawId = cell(r, 'fish_voice_id');
    let id = null;
    if (rawId) {
      const hex = HEX32.exec(rawId)?.[0]?.toLowerCase();
      if (hex && (FISH_ID.test(rawId.toLowerCase()) || /fish\.audio|^\s*[0-9a-f]{32}\s*$/i.test(rawId))) id = hex;
      else report.invalidId.push(`${name} (row ${line}): "${rawId.slice(0, 60)}"`);
    } else report.blankId.push(name);
    if (id) report.withId++;
    const e = { name, aliases: splitList(cell(r, 'aliases')), floors: parseFloors(cell(r, 'floors')), fish_voice_id: id, note: cell(r, 'note') };
    for (const k of ['npc_id', 'type', 'voice_cue', 'fish_voice_name']) if (cell(r, k)) e[k] = cell(r, k);
    e._auto = autoAliases(name);
    entries.push(e);
  }
  // aliases: explicit ones always kept (unless they collide); auto ones only when no other NPC already owns that key
  const owner = new Map(entries.map((e) => [npcKey(e.name), e]));
  for (const e of entries) for (const a of e.aliases) {
    const k = npcKey(a);
    if (owner.has(k) && owner.get(k) !== e) { report.aliasCollisions.push(`${a} (${e.name}; already ${owner.get(k).name})`); e.aliases = e.aliases.filter((x) => x !== a); } else owner.set(k, e);
  }
  for (const e of entries) {
    for (const a of e._auto) {
      const k = npcKey(a);
      if (owner.has(k)) { if (owner.get(k) !== e) report.aliasCollisions.push(`${a} (auto for ${e.name}; already ${owner.get(k).name})`); continue; }
      owner.set(k, e);
      e.aliases.push(a);
      report.aliases.push(`${e.name} -> ${a}`);
    }
    delete e._auto;
  }
  report.imported = entries.length;
  return { entries, report };
}

/** --check: GET {base}/model/<id> for every id. The key is only sent as a header, never printed. */
export async function checkIds(entries, { apiKey, fetchImpl = globalThis.fetch, baseUrl = 'https://api.fish.audio' } = {}) {
  const results = [];
  for (const e of entries.filter((x) => x.fish_voice_id)) {
    let status = 'error', detail = '';
    try {
      const r = await fetchImpl(`${baseUrl}/model/${e.fish_voice_id}`, { headers: { Authorization: `Bearer ${apiKey}` } });
      if (r.ok) {
        const j = await r.json().catch(() => ({}));
        status = 'ok';
        detail = [j.title, j.visibility].filter(Boolean).join(', ');
      } else {
        status = r.status === 404 ? 'not found' : r.status === 401 ? 'unauthorized (check FISH_API_KEY)' : r.status === 403 ? 'private / no access' : `HTTP ${r.status}`;
      }
    } catch (err) {
      detail = String(err.message ?? err).split(apiKey || '\u0000').join('[redacted]').slice(0, 120);
    }
    results.push({ name: e.name, id: e.fish_voice_id, status, detail });
  }
  return results;
}

export function formatImportReport(r, { file, sheet, out, dryRun }) {
  const L = [];
  L.push(`npc-voices import${dryRun ? ' (DRY RUN: nothing written)' : ''}: ${file}${sheet ? ` [sheet "${sheet}"]` : ''} -> ${out}`);
  L.push(`  header row ${r.headerRow}: ${Object.entries(r.columns).map(([k, v]) => `${k}="${v}"`).join(', ')}`);
  L.push(`  ${r.rows} data rows: ${r.imported} NPCs imported, ${r.withId} with a valid Fish voice id, ${r.blankId.length} blank id (narrator voice), ${r.invalidId.length} invalid id`);
  if (r.skippedEnv.length) L.push(`  skipped (voice comes from env FISH_VOICE_ID_*): ${r.skippedEnv.join('; ')}`);
  if (r.skippedBlank) L.push(`  skipped blank rows: ${r.skippedBlank}${r.blankName ? ` (${r.blankName} with other cells but no Name)` : ''}`);
  if (r.invalidId.length) L.push(`  INVALID ids (not 32 hex chars; imported without an id, narrator voice): ${r.invalidId.join('; ')}`);
  if (r.duplicates.length) L.push(`  DUPLICATE names (later rows ignored): ${r.duplicates.join('; ')}`);
  if (r.blankId.length) L.push(`  blank id: ${r.blankId.join(', ')}`);
  if (r.aliases.length) L.push(`  auto aliases: ${r.aliases.join('; ')}`);
  if (r.aliasCollisions.length) L.push(`  aliases dropped (another NPC owns that name): ${r.aliasCollisions.join('; ')}`);
  return L.join('\n');
}
