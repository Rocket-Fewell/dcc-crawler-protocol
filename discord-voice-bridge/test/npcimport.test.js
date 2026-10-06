import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { copyFileSync, existsSync, mkdtempSync, readFileSync, rmSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { autoAliases, buildEntries, checkIds, mapHeaders, parseCsv, parseFloors, readTable } from '../src/npcimport.js';
import { NpcVoiceMap } from '../src/npcvoices.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const FIX = join(HERE, 'fixtures');
const PKG = join(HERE, '..');
const byName = (entries) => Object.fromEntries(entries.map((e) => [e.name, e]));

test('import: CSV parsing handles quotes, doubled quotes and blank rows', () => {
  assert.deepEqual(parseCsv('a,"b, c","d ""e"""\r\n1,2,3\n'), [['a', 'b, c', 'd "e"'], ['1', '2', '3']]);
});

test('import: headers matched loosely; "NPC ID" is not the name or the Fish id; "Same floor as" is not floors', () => {
  const m = mapHeaders(['NPC ID', 'Name', 'Floor(s)', 'Type', 'Who/what', 'Voice notes', 'Same floor as', 'Fish Voice ID', 'Fish Voice Name', 'Source']);
  assert.deepEqual(m, { fish_voice_id: 7, fish_voice_name: 8, voice_cue: 5, floors: 2, npc_id: 0, type: 3, note: 4, name: 1 });
  const c = mapHeaders(['NPC name', 'Floors', 'Who / what', 'Fish voice id', 'Voice cue', 'Aliases']);
  assert.deepEqual(c, { fish_voice_id: 3, aliases: 5, voice_cue: 4, floors: 1, note: 2, name: 0 });
});

test('import: floors and auto aliases', () => {
  assert.deepEqual(parseFloors('F1, F2, F9'), [1, 2, 9]);
  assert.deepEqual(parseFloors('F1-F3'), [1, 2, 3]);
  assert.deepEqual(parseFloors('All'), ['all']);
  assert.deepEqual(autoAliases('Laminak Rev-Up Consultant Elite'), ['Laminak Elite']);
  assert.deepEqual(autoAliases('Unvaccinated Clurichaun Rev-Up Consultant'), ['Clurichaun']);
  assert.deepEqual(autoAliases('Bruiser the Mascot'), ['Bruiser']);
  assert.deepEqual(autoAliases('The Owners'), ['Owners']);
  assert.deepEqual(autoAliases('Dale Pruitt'), []);
});

test('import: CSV fixture -> entries, ids validated (hex, URL, upper case), blank/invalid/duplicate/env rows reported', async () => {
  const { rows } = await readTable(join(FIX, 'npc-voices.csv'));
  const { entries, report } = buildEntries(rows);
  const e = byName(entries);
  assert.deepEqual(Object.keys(e), ['Mordecai', 'Proctor Bell', 'Snakk-Matic', 'Dale Pruitt', 'Laminak Rev-Up Consultant Elite']);
  assert.equal(e.Mordecai.fish_voice_id, '0123456789abcdef0123456789abcdef');
  assert.deepEqual(e.Mordecai.aliases, ['Mordy', 'The Guide']);
  assert.deepEqual(e.Mordecai.floors, [1, 2]);
  assert.equal(e.Mordecai.voice_cue, 'tired, "sarcastic"');
  assert.equal(e['Proctor Bell'].fish_voice_id, 'fedcba9876543210fedcba9876543210', 'id taken from a fish.audio URL');
  assert.equal(e['Snakk-Matic'].fish_voice_id, null);
  assert.equal(e['Dale Pruitt'].fish_voice_id, null);
  assert.deepEqual(e['Laminak Rev-Up Consultant Elite'].aliases, ['Laminak Elite']);
  assert.equal(report.withId, 2);
  assert.deepEqual(report.blankId, ['Dale Pruitt', 'Laminak Rev-Up Consultant Elite']);
  assert.equal(report.invalidId.length, 1);
  assert.match(report.invalidId[0], /Snakk-Matic/);
  assert.equal(report.duplicates.length, 1);
  assert.match(report.duplicates[0], /mordecai/);
  assert.equal(report.skippedEnv.length, 1);
  assert.equal(report.skippedBlank, 1);
});

test('import: XLSX fixture (casting-sheet layout, "How to fill" sheet first) -> right sheet, env rows skipped, aliases', async () => {
  const { sheet, rows } = await readTable(join(FIX, 'npc-voices.xlsx'));
  assert.equal(sheet, 'NPC Voices');
  const { entries, report } = buildEntries(rows);
  const e = byName(entries);
  assert.deepEqual(report.skippedEnv.map((s) => s.replace(/ \(row \d+\)/, '')), ['GM Narrator', 'The System']);
  assert.equal(entries.length, 6);
  assert.equal(e['Dean Thudd'].fish_voice_id, 'aabbccddeeff00112233445566778899');
  assert.equal(e['Dean Thudd'].fish_voice_name, 'Big Coach');
  assert.equal(e['Dean Thudd'].npc_id, 'NPC-007');
  assert.deepEqual(e['Dean Thudd'].floors, [1, 2]);
  assert.equal(e['Dean Thudd'].note, 'Ogre principal');
  assert.deepEqual(e['The Audience'].floors, ['all']);
  assert.deepEqual(e['The Audience'].aliases, ['Audience']);
  assert.deepEqual(e['Dean Thudd (JV)'].aliases, [], '"Dean Thudd" belongs to the other row');
  assert.deepEqual(e['Laminak Rev-Up Consultant Elite'].aliases, ['Laminak Elite']);
  assert.deepEqual(e['Unvaccinated Clurichaun Rev-Up Consultant'].aliases, ['Clurichaun']);
  assert.deepEqual(e['Ralph the Frenzied Gerbil'].aliases, ['Ralph']);
  assert.ok(report.aliasCollisions.some((c) => /Dean Thudd/.test(c)));
});

test('import: CLI --dry-run writes nothing and leaves the input untouched; a real run writes a map the bridge loads', () => {
  const dir = mkdtempSync(join(tmpdir(), 'npcimp-'));
  try {
    const xlsx = join(dir, 'casting.xlsx');
    copyFileSync(join(FIX, 'npc-voices.xlsx'), xlsx);
    const before = readFileSync(xlsx);
    const out = join(dir, 'tables', 'npc-voices.json');
    const env = { ...process.env, FISH_API_KEY: '' };
    delete env.DCC_CAMPAIGN_ROOT;
    const dry = spawnSync(process.execPath, ['scripts/npc-voices-import.js', xlsx, '--dry-run', '--out', out], { cwd: PKG, env, encoding: 'utf8' });
    assert.equal(dry.status, 0, dry.stderr);
    assert.match(dry.stdout, /DRY RUN/);
    assert.match(dry.stdout, /6 NPCs imported, 1 with a valid Fish voice id/);
    assert.ok(!existsSync(out));
    const run = spawnSync(process.execPath, ['scripts/npc-voices-import.js', xlsx, '--out', out], { cwd: PKG, env, encoding: 'utf8' });
    assert.equal(run.status, 0, run.stderr);
    assert.ok(readFileSync(xlsx).equals(before), 'input xlsx unchanged');
    const doc = JSON.parse(readFileSync(out, 'utf8'));
    assert.equal(doc.version, '0.1.0');
    assert.equal(doc.npcs.length, 6);
    const m = new NpcVoiceMap({ file: out }).load();
    assert.equal(m.voiceIdFor('clurichaun'), null);
    assert.equal(m.voiceIdFor('DEAN THUDD'), 'aabbccddeeff00112233445566778899');
    assert.ok(statSync(out).size > 0);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('import: --check asks GET /model/<id> per id and never leaks the key', async () => {
  const seen = [];
  const KEY = 'fish-SECRET-key';
  const fetchImpl = async (url, opts) => {
    seen.push({ url, auth: opts.headers.Authorization });
    if (url.endsWith('/model/' + 'a'.repeat(32))) return { ok: true, status: 200, json: async () => ({ title: 'Gravel', visibility: 'public' }) };
    if (url.endsWith('/model/' + 'b'.repeat(32))) return { ok: false, status: 404 };
    throw new Error(`socket hang up (key ${KEY})`);
  };
  const res = await checkIds([
    { name: 'A', fish_voice_id: 'a'.repeat(32) },
    { name: 'B', fish_voice_id: 'b'.repeat(32) },
    { name: 'C', fish_voice_id: 'c'.repeat(32) },
    { name: 'D', fish_voice_id: null },
  ], { apiKey: KEY, fetchImpl });
  assert.deepEqual(res.map((r) => r.status), ['ok', 'not found', 'error']);
  assert.equal(res[0].detail, 'Gravel, public');
  assert.equal(seen[0].url, `https://api.fish.audio/model/${'a'.repeat(32)}`);
  assert.equal(seen[0].auth, `Bearer ${KEY}`);
  assert.ok(!JSON.stringify(res).includes(KEY));
});
