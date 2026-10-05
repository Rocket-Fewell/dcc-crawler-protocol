// S7 background display names ("Our Name (5e Name)") from Lore's background-reskins.json, behind create.background_reskin (default OFF),
// plus the generic display-layer mechanism (layers.js). Placeholder names exist ONLY in these fixtures; the real-file test reads Lore's copy.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, readFileSync, rmSync, utimesSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { resolveLoreRoot } from '../src/paths.js';
import test from 'node:test';
import { asiLabel, backgroundFlavor, backgroundLabel, bgNamesPath, buildBgIndex, checkBgNamesHash, featLabel, flatParens, packageLabel } from '../src/create/bgnames.js';
import { LAYERS, buildLayerIndex, checkLayerHash, layerEntry, layerFlags, layerText, loadLayers, registerLayer } from '../src/create/layers.js';
import { loadTables, tablesFor } from '../src/create/data.js';
import { Player, makeCtx, makeSandbox } from './helpers/create-harness.js';

const LORE = join(resolveLoreRoot(), 'tables');
const E = (id, kind, parent, srd, display, value, extra = {}) => ({ id, kind, parent_id: parent, srd_name: srd, display_name: display, combined_label: `${display} (${extra.label_name ?? srd})`, chargen_value: value, flavor: `PLACEHOLDER flavor of ${id}.`, ...extra });
const FIXTURE = {
  schema: 'background-reskins/0.1.0',
  meta: { version: '9.9.9', title: 'TEST FIXTURE, PLACEHOLDER NAMES ONLY' },
  entries: [
    E('soldier', 'background', null, 'Soldier', 'PLACEHOLDER Reservist', 'Soldier'),
    E('acolyte', 'background', null, 'Acolyte', 'PLACEHOLDER Youth Pastor', 'Acolyte'),
    E('feat-tough', 'choice', 'origin-feat', 'Tough', 'PLACEHOLDER Gym Rat', 'Tough'),
    E('feat-magic-initiate-cleric', 'choice', 'origin-feat', 'Magic Initiate (Cleric)', 'PLACEHOLDER Prayer Chain', 'Magic Initiate (Cleric)', { label_name: 'Magic Initiate, Cleric' }),
    E('asi-2-1', 'choice', 'background-asi', '+2 / +1', 'PLACEHOLDER Raise', '+2 / +1'),
    E('asi-1-1-1', 'choice', 'background-asi', '+1 / +1 / +1', 'PLACEHOLDER Trophy', '+1 / +1 / +1'),
    E('package-a', 'choice', 'background-kit', 'Package A', 'PLACEHOLDER Desk Box', 'A'),
    E('package-b', 'choice', 'background-kit', 'Package B', 'PLACEHOLDER Envelope', 'B'),
  ],
};
const bump = (p) => { const t = new Date(Date.now() + Math.floor(Math.random() * 1e6) + 5000); utimesSync(p, t, t); };
const bgFile = (dir) => join(dir, 'tables', 'background-reskins.json');
const setFlag = (dir, v) => {
  const sj = join(dir, 'sessions-data', 'beta', 'session.json');
  const prof = JSON.parse(readFileSync(sj, 'utf8'));
  prof.create = { ...(prof.create ?? {}) };
  if (v === undefined) delete prof.create.background_reskin; else prof.create.background_reskin = v;
  writeFileSync(sj, JSON.stringify(prof)); bump(sj);
};
const putBg = (dir, data, { flag = true, version = true } = {}) => {
  if (flag !== null) setFlag(dir, flag);
  const p = bgFile(dir);
  writeFileSync(p, typeof data === 'string' ? data : JSON.stringify(data)); bump(p);
  if (version) writeFileSync(join(dir, 'tables', 'background-reskins.version.json'), JSON.stringify({ version: '9.9.9', sha256: createHash('sha256').update(readFileSync(p)).digest('hex') }));
};
const idx = (j, o) => ({ bgnames: buildBgIndex(j, o) });
const toS7 = async (p, name) => {
  await p.command(); await p.click('ACCEPT'); await p.click('Skip');
  await p.form('S3:name', { name }); await p.click('Next');
  await p.form('S4:edit', { look: 'a', hook: 'b' }); await p.click('Next');
  await p.choose('S5:species', 'Human'); await p.click('Next');
  await p.choose('S6:class', 'Fighter'); if (p.components().some((c) => c.custom_id?.includes('S6:choice'))) await p.click('Pick for me'); await p.click('Next');
};
const labels = (p, key) => p.byKey(key).options.map((o) => o.label);

test('bgnames: label = combined_label as written; plain text for any missing id, off flag, wrong kind or odd table; never nests parentheses', () => {
  const t = idx(FIXTURE);
  assert.equal(backgroundLabel(t, 'Soldier'), 'PLACEHOLDER Reservist (Soldier)');
  assert.equal(backgroundLabel(t, 'Guard'), 'Guard');                                          // no entry
  assert.equal(featLabel(t, 'Tough'), 'PLACEHOLDER Gym Rat (Tough)');
  assert.equal(featLabel(t, 'Magic Initiate (Cleric)'), 'PLACEHOLDER Prayer Chain (Magic Initiate, Cleric)');   // label_name: no nested parentheses
  assert.equal(featLabel(t, 'Alert'), 'Alert');
  assert.equal(asiLabel(t, '2-1', '+2 INT / +1 WIS'), 'PLACEHOLDER Raise (+2 / +1): +2 INT / +1 WIS');          // the rules text stays in the label
  assert.equal(asiLabel(t, '1-1-1', '+1 INT / +1 WIS / +1 CHA'), 'PLACEHOLDER Trophy (+1 / +1 / +1): +1 INT / +1 WIS / +1 CHA');
  assert.equal(packageLabel(t, 'A', '8 GP left over', 'Package A (8 GP left over)'), 'PLACEHOLDER Desk Box (Package A) - 8 GP left over');
  assert.equal(packageLabel(t, 'B', '50 GP', 'Gold option: 50 GP'), 'PLACEHOLDER Envelope (Package B) - 50 GP');
  assert.equal(packageLabel(t, 'C', '1 GP', 'Gold option: 1 GP'), 'Gold option: 1 GP');
  assert.equal(backgroundFlavor(t, 'Soldier'), 'PLACEHOLDER flavor of soldier.');
  assert.equal(backgroundFlavor(t, 'Soldier', 12), 'PLACEHOLDER…');
  assert.equal(backgroundFlavor(t, 'Guard'), '');
  // off / absent / odd
  assert.equal(backgroundLabel(idx(FIXTURE, { enabled: false }), 'Soldier'), 'Soldier');
  assert.equal(backgroundLabel(idx(null), 'Soldier'), 'Soldier');
  assert.equal(backgroundLabel({}, 'Soldier'), 'Soldier');
  assert.equal(backgroundLabel(idx({ entries: 'oops' }), 'Soldier'), 'Soldier');
  assert.equal(backgroundLabel(idx({ entries: [null, 3, { id: 9 }, { id: 'soldier', kind: 'background', display_name: 7, combined_label: 9 }] }), 'Soldier'), 'Soldier');
  // a wrong-kind entry never answers (a feat id used as a background)
  assert.equal(backgroundLabel(idx({ entries: [E('tough', 'choice', 'origin-feat', 'Tough', 'X', 'Tough')] }), 'Tough'), 'Tough');
  // a different id but the exact chargen_value still resolves (Lore lookup rule)
  assert.equal(backgroundLabel(idx({ entries: [E('job-soldier', 'background', null, 'Soldier', 'PLACEHOLDER Odd', 'Soldier')] }), 'Soldier'), 'PLACEHOLDER Odd (Soldier)');
  // safety net: a nested label is flattened, a long one keeps its parenthesis
  assert.equal(flatParens('Name (Magic Initiate (Cleric))'), 'Name (Magic Initiate - Cleric)');
  assert.equal(featLabel(idx({ entries: [E('feat-x', 'choice', 'origin-feat', 'X', 'D', 'X', { combined_label: 'D (Magic Initiate (Cleric))' })] }), 'X'), 'D (Magic Initiate - Cleric)');
  const long = backgroundLabel(idx({ entries: [E('soldier', 'background', null, 'Soldier', 'Z'.repeat(150), 'Soldier', { combined_label: `${'Z'.repeat(150)} (Soldier)` })] }), 'Soldier');
  assert.ok(long.length <= 100 && long.endsWith('(Soldier)'), long);
});

test('bgnames: hash check absent / ok / warn / fail; the file is read by mtime and a broken file is ignored', () => {
  const dir = makeSandbox('beta');
  rmSync(bgFile(dir), { force: true }); rmSync(join(dir, 'tables', 'background-reskins.version.json'), { force: true });
  assert.equal(checkBgNamesHash(dir).status, 'absent');
  putBg(dir, FIXTURE);
  assert.equal(checkBgNamesHash(dir).status, 'ok');
  assert.equal(backgroundLabel(loadTables(dir, { bgReskin: true }), 'Soldier'), 'PLACEHOLDER Reservist (Soldier)');
  assert.equal(backgroundLabel(loadTables(dir), 'Soldier'), 'Soldier', 'bgReskin defaults OFF');
  writeFileSync(bgFile(dir), JSON.stringify({ ...FIXTURE, entries: [] })); bump(bgFile(dir));
  assert.equal(checkBgNamesHash(dir).status, 'fail');
  rmSync(join(dir, 'tables', 'background-reskins.version.json'));
  assert.equal(checkBgNamesHash(dir).status, 'warn');
  putBg(dir, '{ not json', { version: false });
  assert.equal(backgroundLabel(loadTables(dir, { bgReskin: true }), 'Soldier'), 'Soldier');
  assert.equal(bgNamesPath(dir, { BACKGROUND_RESKINS_PATH: '/x/y.json' }), '/x/y.json');
});

test('S7 shows the plain 5e text by default (flag off), with the file in tables/ or not', async () => {
  const dir = makeSandbox('beta');
  putBg(dir, FIXTURE, { flag: null });
  const p = new Player(makeCtx(dir), '4001', 'Ann');
  await toS7(p, 'Ann');
  assert.ok(labels(p, 'S7:bg').every((l) => !/PLACEHOLDER/.test(l)));
  await p.choose('S7:bg', 'Soldier');
  assert.deepEqual(labels(p, 'S7:asi').filter((l) => /PLACEHOLDER/.test(l)), []);
  assert.ok(labels(p, 'S7:asi').includes('+1 STR / +1 CON / +1 WIS') || labels(p, 'S7:asi').some((l) => /^\+1 /.test(l)));
  assert.ok(!/PLACEHOLDER/.test(p.lastText));
  assert.match(p.lastText, /\*\*Soldier\*\* - scores/);
  setFlag(dir, false);
  await p.click('◂ Back'); await p.click('Next');
  assert.ok(labels(p, 'S7:bg').every((l) => !/PLACEHOLDER/.test(l)));
});

test('S7 with create.background_reskin true: backgrounds, bonus choices, Human extra feat and S10 packages show Our Name (5e Name); values, state and ledger keep the 5e text; live reload; kill switch', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  putBg(dir, FIXTURE);
  const p = new Player(makeCtx(dir), '4002', 'Bea');
  await toS7(p, 'Bea');
  const bg = p.byKey('S7:bg').options;
  assert.equal(bg.find((o) => o.value === 'Soldier').label, 'PLACEHOLDER Reservist (Soldier)');
  assert.equal(bg.find((o) => o.value === 'Guard').label, 'Guard');                         // no entry: plain
  assert.deepEqual(bg.map((o) => o.value), ['Acolyte', 'Artisan', 'Charlatan', 'Criminal', 'Entertainer', 'Farmer', 'Guard', 'Guide', 'Hermit', 'Merchant', 'Noble', 'Sage', 'Sailor', 'Scribe', 'Soldier', 'Wayfarer'].slice(0, bg.length));
  assert.ok(bg.find((o) => o.value === 'Soldier').description.includes('Savage Attacker') || bg.find((o) => o.value === 'Soldier').description.length > 0, 'rules facts stay in the description');
  await p.choose('S7:bg', 'Soldier');
  assert.match(p.lastText, /\*\*PLACEHOLDER Reservist \(Soldier\)\*\* - PLACEHOLDER flavor of soldier\./);
  const asi = p.byKey('S7:asi').options;
  assert.ok(asi.some((o) => /^PLACEHOLDER Raise \(\+2 \/ \+1\): \+2 [A-Z]{3} \/ \+1 [A-Z]{3}$/.test(o.label)), JSON.stringify(asi.map((o) => o.label)));
  assert.ok(asi.some((o) => /^PLACEHOLDER Trophy \(\+1 \/ \+1 \/ \+1\): \+1 /.test(o.label)));
  assert.ok(asi.every((o) => /^(2-1:[a-z]+:[a-z]+|1-1-1)$/.test(o.value)), 'values are the rules ids');
  assert.ok(asi.every((o) => (o.label.match(/\(/g) ?? []).length <= 1), 'no nested parentheses');
  await p.choose('S7:asi', asi[0].value);
  if (p.byKey('S7:feat')) {
    const f = p.byKey('S7:feat').options;
    assert.ok(f.every((o) => o.value && (o.label.match(/\(/g) ?? []).length <= 1), 'feat labels never nest parentheses');
    assert.ok(f.some((o) => o.label === 'PLACEHOLDER Prayer Chain (Magic Initiate, Cleric)' && o.value === 'Magic Initiate (Cleric)'));
    assert.equal(f.find((o) => o.value === 'Tough')?.label, 'PLACEHOLDER Gym Rat (Tough)');
    await p.choose('S7:feat', 'Tough');
    assert.match(p.lastText, /Human Versatile feat:\*\* PLACEHOLDER Gym Rat \(Tough\)/);
  }
  // live reload (no restart)
  putBg(dir, { ...FIXTURE, entries: FIXTURE.entries.map((e) => (e.id === 'soldier' ? E('soldier', 'background', null, 'Soldier', 'PLACEHOLDER Second Edition', 'Soldier') : e)) });
  await p.click('◂ Back'); await p.click('Next');
  assert.equal(p.byKey('S7:bg').options.find((o) => o.value === 'Soldier').label, 'PLACEHOLDER Second Edition (Soldier)');
  // switch off: plain again, file untouched
  setFlag(dir, false);
  await p.click('◂ Back'); await p.click('Next');
  assert.equal(p.byKey('S7:bg').options.find((o) => o.value === 'Soldier').label, 'Soldier');
  assert.ok(existsSync(bgFile(dir)));
  setFlag(dir, 'yes');
  await p.click('◂ Back'); await p.click('Next');
  assert.equal(p.byKey('S7:bg').options.find((o) => o.value === 'Soldier').label, 'Soldier', 'only a real true turns it on');
});

test('a full /create walk with the layer on: S10 package labels carry the names, the draft, state.json, the ledger and the sheet keep the 5e background', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  putBg(dir, FIXTURE);
  const { drive } = await import('./helpers/create-harness.js');
  const p = new Player(makeCtx(dir), '4003', 'Cy');
  await p.command();
  // S10 is inspected from a first walk that stops there (a sentinel thrown from the S9 hook)
  const q = new Player(makeCtx(dir), '4004', 'Di');
  await q.command();
  await assert.rejects(drive(q, { name: 'Di', bg: 'Soldier', species: 'Human', cls: 'Fighter', onS9: async (r) => {
    await r.click('Next');
    assert.equal(r.screen(), 'S10');
    const kb = r.byKey('S10:kb');
    assert.match(kb.placeholder ?? '', /PLACEHOLDER Reservist \(Soldier\): package or credits/);
    assert.ok(kb.options.some((o) => /^PLACEHOLDER Desk Box \(Package A\) - \d+ credits? left over$/.test(o.label) && o.value === 'A'), JSON.stringify(kb.options.map((o) => o.label)));
    assert.ok(kb.options.some((o) => /^PLACEHOLDER Envelope \(Package B\) - \d+ credits?$/.test(o.label) && o.value === 'B'));
    assert.ok(r.byKey('S10:kc').options.every((o) => !/PLACEHOLDER/.test(o.label)), 'class packages are not part of this layer');
    throw new Error('STOP-AT-S10');
  } }), /STOP-AT-S10/);
  await drive(p, { name: 'Cy', bg: 'Soldier', species: 'Human', cls: 'Fighter', noShop: true, kit: { kc: 'A', kb: 'A' }, onS11: async (r) => { await r.click('Pick for me'); await r.click('Next'); } });
  assert.equal(p.screen(), 'S16');
  await p.click('Confirm ▸');
  await p.click('Confirm and lock the file');
  const data = join(dir, 'sessions-data', 'beta');
  const st = JSON.parse(readFileSync(join(data, 'state.json'), 'utf8'));
  const c = st.crawlers.find((x) => x.name === 'Cy');
  assert.equal(c.background, 'Soldier');
  assert.ok(!JSON.stringify(st).includes('PLACEHOLDER'));
  const ledgerFile = join(data, 'credit-ledger.jsonl');
  if (existsSync(ledgerFile)) assert.ok(!readFileSync(ledgerFile, 'utf8').includes('PLACEHOLDER'));
});

test('Lore\'s real background-reskins.json (a sandbox copy): every background, origin feat, bonus choice and package gets its combined_label; no label nests parentheses or passes 100 characters', {
  skip: !existsSync(join(LORE, 'background-reskins.json')) && 'Lore\'s file is not on this box',
}, async () => {
  const dir = makeSandbox('beta');
  copyFileSync(join(LORE, 'background-reskins.json'), bgFile(dir));
  copyFileSync(join(LORE, 'background-reskins.version.json'), join(dir, 'tables', 'background-reskins.version.json'));
  bump(bgFile(dir));
  setFlag(dir, true);
  assert.equal(checkBgNamesHash(dir).status, 'ok');
  const t = loadTables(dir, { bgReskin: true });
  const lore = JSON.parse(readFileSync(bgFile(dir), 'utf8'));
  const byId = new Map(lore.entries.map((e) => [e.id, e]));
  const nest = (s) => !/\(.*\(/.test(s);
  assert.equal(Object.keys(t.chargen.backgrounds).length, 16);
  for (const n of Object.keys(t.chargen.backgrounds)) {
    const l = backgroundLabel(t, n);
    assert.equal(l, byId.get(n.toLowerCase()).combined_label, n);
    assert.ok(l !== n && l.endsWith(`(${n})`) && nest(l) && l.length <= 100, l);
    assert.ok(backgroundFlavor(t, n).length > 10, `${n} flavor`);
  }
  for (const f of t.chargen.origin_feats) {
    const l = featLabel(t, f);
    assert.ok(l !== f && nest(l) && l.length <= 100, l);
  }
  assert.equal(featLabel(t, 'Magic Initiate (Cleric)'), byId.get('feat-magic-initiate-cleric').combined_label);
  for (const [ty, plain] of [['2-1', '+2 INT / +1 WIS'], ['1-1-1', '+1 INT / +1 WIS / +1 CHA']]) { const l = asiLabel(t, ty, plain); assert.ok(l.endsWith(plain) && l !== plain && nest(l.replace(plain, '')) && l.length <= 100, l); }
  for (const pk of ['A', 'B']) { const l = packageLabel(t, pk, '8 GP left over', 'plain'); assert.ok(l !== 'plain' && l.endsWith(' - 8 GP left over') && nest(l) && l.length <= 100, l); }
  // through the real screens
  const p = new Player(makeCtx(dir), '4005', 'Eve');
  await toS7(p, 'Eve');
  for (const o of p.byKey('S7:bg').options) assert.ok(o.label !== o.value && o.label.endsWith(`(${o.value})`) && nest(o.label), `S7 ${o.value}: ${o.label}`);
  await p.choose('S7:bg', 'Acolyte');
  assert.match(p.lastText, /\*\*Youth-Group Pizza Wrangler \(Acolyte\)\*\*/);
  for (const o of p.byKey('S7:asi').options) assert.ok(nest(o.label) && o.label.length <= 100 && !/^\+/.test(o.label), o.label);
});

// ------------------------------------------------------------------ the generic mechanism
test('layers: one registry gives every display layer a session flag (exactly true), a hash check and a tables object key; later Lore layers are one registerLayer() call', () => {
  assert.ok(LAYERS.has('species_class') && LAYERS.has('background'));
  assert.deepEqual(layerFlags({ background_reskin: true, species_class_reskin: 'true' }), { species_class: false, background: true, screens: false, screens_lines: false });
  assert.deepEqual(layerFlags(undefined), { species_class: false, background: false, screens: false, screens_lines: false });
  const spec = registerLayer({ id: 'test_strings', file: 'test-strings.json', flag: 'test_strings', env: 'TEST_STRINGS_PATH', tkey: 'teststrings' });
  try {
    assert.equal(layerFlags({ test_strings: true }).test_strings, true);
    const dir = makeSandbox('beta');
    const f = join(dir, 'tables', 'test-strings.json');
    const j = { meta: { version: '1' }, entries: [
      { screen: 'S8', id: 'roll_button', text: 'PLACEHOLDER Roll the dice' },
      { screen: 'S8', id: 'rolled', text: 'PLACEHOLDER {name} rolled {total}' },
      { screen: 'S9', id: 'blank', text: '   ' },
      { screen: 'S9', id: 'bad', text: 123 },
      { id: 'abilities-str', kind: 'ability', srd_name: 'Strength', display_name: 'PLACEHOLDER Brawn', combined_label: 'PLACEHOLDER Brawn (Strength)', chargen_value: 'str' },
    ] };
    writeFileSync(f, JSON.stringify(j)); bump(f);
    writeFileSync(join(dir, 'tables', 'test-strings.version.json'), JSON.stringify({ sha256: createHash('sha256').update(readFileSync(f)).digest('hex') }));
    assert.equal(checkLayerHash(spec, dir).status, 'ok');
    const load = (on) => loadTables(dir, { layers: { test_strings: on } });
    const on = load(true);
    assert.equal(layerText(on, 'teststrings', 'S8', 'roll_button', 'Roll'), 'PLACEHOLDER Roll the dice');
    assert.equal(layerText(on, 'teststrings', 'S8', 'rolled', 'fallback', { name: 'Bea', total: 14 }), 'PLACEHOLDER Bea rolled 14');
    assert.equal(layerText(on, 'teststrings', 'S8', 'rolled', 'fallback', { name: 'Bea' }), 'fallback', 'an unfilled placeholder never shows');
    for (const [s, i] of [['S9', 'blank'], ['S9', 'bad'], ['S9', 'nope'], ['S1', 'roll_button']]) assert.equal(layerText(on, 'teststrings', s, i, 'FB'), 'FB');
    assert.equal(layerEntry(on, 'teststrings', { id: 'abilities-str', kind: 'ability', parent: undefined })?.display_name, 'PLACEHOLDER Brawn');
    assert.equal(layerEntry(on, 'teststrings', { id: 'other', kind: 'ability', parent: null, value: 'str' })?.display_name, 'PLACEHOLDER Brawn');
    // off (the default): empty index, every lookup falls back to the current text
    for (const t of [load(false), loadTables(dir), {}, null]) assert.equal(layerText(t, 'teststrings', 'S8', 'roll_button', 'Roll'), 'Roll');
    // a broken file never crashes the load
    writeFileSync(f, '{ nope'); bump(f);
    assert.equal(layerText(load(true), 'teststrings', 'S8', 'roll_button', 'Roll'), 'Roll');
    assert.equal(loadLayers(dir, { test_strings: true }, () => { throw new Error('boom'); }).teststrings.loaded, false);
    // the species/class and background layers are untouched by the extra layer
    assert.equal(load(true).bgnames.loaded, false);
  } finally {
    LAYERS.delete('test_strings');
  }
  assert.ok(!LAYERS.has('test_strings'));
  assert.equal(buildLayerIndex({ entries: [{ id: 'a' }] }, { enabled: false }).loaded, false);
});

test('layers: tablesFor honours each layer flag from the session independently', () => {
  const dir = makeSandbox('beta');
  putBg(dir, FIXTURE, { flag: true });
  const cfg = { campaign: { dir, sessionId: 'beta', dataDir: join(dir, 'sessions-data', 'beta') } };
  assert.equal(backgroundLabel(tablesFor(cfg), 'Soldier'), 'PLACEHOLDER Reservist (Soldier)');
  setFlag(dir, false);
  assert.equal(backgroundLabel(tablesFor(cfg), 'Soldier'), 'Soldier');
});
