/**
 * npm run npc-voices:import -- <file.xlsx|file.csv> [--dry-run] [--check] [--out FILE]
 * Reads Caleb's filled casting sheet and writes <campaign>/tables/npc-voices.json (campaign root from .env / src/paths.js;
 * NPC_VOICES_FILE or --out overrides). The running bridge re-reads the file by itself (no restart).
 * --check asks Fish (GET /model/<id>) whether each id exists, with FISH_API_KEY from the environment (never printed).
 */
import 'dotenv/config';
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { basename, dirname, resolve } from 'node:path';
import { buildEntries, checkIds, formatImportReport, readTable } from '../src/npcimport.js';
import { npcVoicesFile } from '../src/npcvoices.js';
import { resolveCampaignRoot } from '../src/paths.js';

const args = process.argv.slice(2);
const flag = (f) => args.includes(f);
const outIdx = args.indexOf('--out');
const out = resolve(outIdx >= 0 ? args[outIdx + 1] ?? '' : npcVoicesFile(resolveCampaignRoot()));
const file = args.find((a, i) => !a.startsWith('--') && !(outIdx >= 0 && i === outIdx + 1));
if (!file) {
  console.error('usage: npm run npc-voices:import -- <file.xlsx|file.csv> [--dry-run] [--check] [--out FILE]');
  process.exit(1);
}
let code = 0;
try {
  const { sheet, rows } = await readTable(resolve(file));
  const { entries, report } = buildEntries(rows);
  console.log(formatImportReport(report, { file, sheet, out, dryRun: flag('--dry-run') }));
  if (report.invalidId.length || report.duplicates.length) code = 2;
  if (flag('--check')) {
    const apiKey = process.env.FISH_API_KEY;
    if (!apiKey) {
      console.error('  --check: FISH_API_KEY is not set; ids not checked');
      code = 2;
    } else {
      const res = await checkIds(entries, { apiKey });
      if (!res.length) console.log('  --check: no ids to check');
      for (const r of res) console.log(`  --check ${r.status === 'ok' ? 'ok  ' : 'FAIL'} ${r.name}: ${r.id} ${r.status}${r.detail ? ` (${r.detail})` : ''}`);
      if (res.some((r) => r.status !== 'ok')) code = 2;
    }
  }
  if (!flag('--dry-run')) {
    let prev = {};
    try { prev = existsSync(out) ? JSON.parse(readFileSync(out, 'utf8')) : {}; } catch { prev = {}; }
    const doc = {
      schema: prev.schema ?? 'npc-voices/0.1',
      owner: prev.owner ?? 'Caleb (casting) / bridge (format)',
      version: prev.version ?? '0.1.0',
      updated: new Date().toISOString().slice(0, 10),
      imported_from: basename(file),
      note: prev.note ?? 'One Fish Audio library voice per NPC for the [NPC: Name] tag. fish_voice_id null = narrator voice. Written by npm run npc-voices:import; the bridge reloads it on change.',
      npcs: entries,
    };
    mkdirSync(dirname(out), { recursive: true });
    const tmp = `${out}.${process.pid}.tmp`;
    writeFileSync(tmp, JSON.stringify(doc, null, 1) + '\n');
    renameSync(tmp, out);
    console.log(`  wrote ${entries.length} NPCs to ${out}`);
  }
} catch (err) {
  console.error(`npc-voices import failed: ${err.message}`);
  code = 1;
}
process.exit(code);
