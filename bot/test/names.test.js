// Species / lineage / class / class-option display names ("Our Name (5e Name)") from Lore's species-class-reskins.json. Placeholder names exist ONLY in these fixtures.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, readFileSync, readdirSync, rmSync, utimesSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { REAL_LORE } from './helpers/roots.js';
import test from 'node:test';
import { baseIdOf, buildNameIndex, checkNamesHash, classLabel, classOptionId, classOptionLabel, kid, lineageId, lineageLabel, nameLabel, speciesLabel, variantLabel } from '../src/create/names.js';
import { tablesFor } from '../src/create/data.js';
import { loadTables } from '../src/create/data.js';
import { Player, REAL_CAMPAIGN, drive, makeCtx, makeSandbox } from './helpers/create-harness.js';

const LORE = join(REAL_LORE, 'tables');
const ent = (id, kind, srd, display, parent = null, short = srd, extra = {}) => ({ id, kind, parent_id: parent, srd_name: srd, display_name: display, combined_label: `${display} (${short})`, nation: kind.startsWith('class') ? null : 'Testland', flavor: 'x', spoken: 'x', ...extra });
const FIXTURE = {
  schema: 'species-class-reskins/0.1.0',
  meta: { version: '9.9.9', title: 'TEST FIXTURE, PLACEHOLDER NAMES ONLY' },
  entries: [
    ent('human', 'species', 'Human', 'PLACEHOLDER Meatsack'),
    ent('elf', 'species', 'Elf', 'PLACEHOLDER Pointy'),
    ent('elf-high', 'species_lineage', 'High Elf', 'PLACEHOLDER Ivy League', 'elf', 'High Elf', { base_id: 'elf', chargen_value: 'High Elf', rules_entry: true }),
    ent('felid', 'species', 'Felid', 'PLACEHOLDER Whiskers'),
    ent('felid-cat', 'species_variant', 'Cat', 'PLACEHOLDER Tabby', 'felid', 'Cat', { base_id: 'felid', chargen_value: null, rules_entry: false }),
    ent('wizard', 'class', 'Wizard', 'PLACEHOLDER Grad Student'),
    ent('cleric', 'class', 'Cleric', 'PLACEHOLDER Chaplain'),
    ent('cleric-protector', 'class_option', 'Protector (Divine Order)', 'PLACEHOLDER Bodyguard', 'cleric', 'Protector'),
  ],
};
const idx = (j, o) => ({ names: buildNameIndex(j, o) });
const bump = (p) => { const t = new Date(Date.now() + Math.floor(Math.random() * 1e6) + 5000); utimesSync(p, t, t); };
const namesFile = (dir) => join(dir, 'tables', 'species-class-reskins.json');
const putNames = (dir, data, version = true, flag = true) => {
  if (flag) setFlag(dir, true);
  const p = namesFile(dir);
  writeFileSync(p, typeof data === 'string' ? data : JSON.stringify(data));
  bump(p);
  if (version) writeFileSync(join(dir, 'tables', 'species-class-reskins.version.json'), JSON.stringify({ version: '9.9.9', sha256: createHash('sha256').update(readFileSync(p)).digest('hex') }));
  return p;
};
const setFlag = (dir, v) => {
  const sj = join(dir, 'sessions-data', 'beta', 'session.json');
  const prof = JSON.parse(readFileSync(sj, 'utf8'));
  prof.create = { ...(prof.create ?? {}) };
  if (v === undefined) delete prof.create.species_class_reskin; else prof.create.species_class_reskin = v;
  writeFileSync(sj, JSON.stringify(prof)); bump(sj);
};
const toS5 = async (p, name) => {
  await p.command(); await p.click('ACCEPT'); await p.click('Skip');
  await p.form('S3:name', { name }); await p.click('Next');
  await p.form('S4:edit', { look: 'a', hook: 'b' }); await p.click('Next');
};

test('names: ids follow Lore\'s scheme; label = combined_label as written, else the plain 5e name; never blank, never throws', () => {
  assert.equal(kid('High Elf'), 'high-elf');
  assert.equal(lineageId('Elf', 'High Elf'), 'elf-high');
  assert.equal(lineageId('Gnome', 'Rock Gnome'), 'gnome-rock');
  assert.equal(lineageId('Dragonborn', 'Black'), 'dragonborn-black');
  assert.equal(classOptionId('Cleric', 'Protector'), 'cleric-protector');
  const t = idx(FIXTURE);
  assert.equal(speciesLabel(t, 'Human'), 'PLACEHOLDER Meatsack (Human)');
  assert.equal(classLabel(t, 'Wizard'), 'PLACEHOLDER Grad Student (Wizard)');
  assert.equal(lineageLabel(t, 'Elf', 'High Elf'), 'PLACEHOLDER Ivy League (High Elf)');
  assert.equal(classOptionLabel(t, 'Cleric', 'Protector'), 'PLACEHOLDER Bodyguard (Protector)');   // no nested parentheses, and not hard-coded
  assert.equal(classLabel(t, 'Fighter'), 'Fighter');                                             // no entry
  assert.equal(lineageLabel(t, 'Elf', 'Drow'), 'Drow');
  assert.equal(classOptionLabel(t, 'Druid', 'Warden'), 'Warden');
  assert.equal(speciesLabel({}, 'Human'), 'Human');                                              // no tables
  assert.equal(speciesLabel(idx(null), 'Human'), 'Human');                                       // no file
  assert.equal(speciesLabel(idx(FIXTURE, { enabled: false }), 'Human'), 'Human');                // switched off
  assert.equal(nameLabel(idx({ entries: [{ id: 'human', display_name: 7, combined_label: 9 }] }), 'human', 'Human'), 'Human');
  assert.equal(nameLabel(idx({ entries: [null, 3, { id: 9 }, { id: 'human' }] }), 'human', 'Human'), 'Human');
  assert.equal(nameLabel(idx({ entries: 'oops' }), 'human', 'Human'), 'Human');
  assert.equal(nameLabel(idx(null), 'x', ''), 'x');
  // srd_name fallback for species/classes whose id differs
  assert.equal(speciesLabel(idx({ entries: [ent('wild-elf', 'species', 'Wild Elf', 'PLACEHOLDER W')] }), 'Wild Elf'), 'PLACEHOLDER W (Wild Elf)');
  const long = nameLabel(idx({ entries: [ent('human', 'species', 'Human', 'Z'.repeat(150))] }), 'human', 'Human');
  assert.ok(long.length <= 100 && long.endsWith('(Human)'), 'a long label is cut but keeps the 5e name');
});

test('names: hash check absent / ok / warn / fail; the live tables dir is absent until approved, ok after', () => {
  // the approved copy goes into tables/ only after Caleb says so; until then the live status is 'absent', afterwards it must be 'ok'
  assert.equal(checkNamesHash(REAL_CAMPAIGN).status, existsSync(join(REAL_CAMPAIGN, 'tables', 'species-class-reskins.json')) ? 'ok' : 'absent');
  const dir = makeSandbox('beta');
  rmSync(namesFile(dir), { force: true }); rmSync(join(dir, 'tables', 'species-class-reskins.version.json'), { force: true });   // the sandbox copies tables/; start without the file
  assert.equal(checkNamesHash(dir).status, 'absent');
  putNames(dir, FIXTURE, false);
  assert.equal(checkNamesHash(dir).status, 'warn');
  putNames(dir, FIXTURE);
  assert.equal(checkNamesHash(dir).status, 'ok');
  writeFileSync(namesFile(dir), JSON.stringify({ ...FIXTURE, entries: FIXTURE.entries.slice(1) }));
  assert.equal(checkNamesHash(dir).status, 'fail');
  writeFileSync(join(dir, 'tables', 'species-class-reskins.version.json'), '{bad');
  assert.equal(checkNamesHash(dir).status, 'fail');
});

test('/create shows plain 5e names by default (switch off), whether or not the copy is in tables/', async () => {
  const dir = makeSandbox('beta');
  const p = new Player(makeCtx(dir), '3001', 'Ann');
  await toS5(p, 'Ann');
  assert.deepEqual(p.byKey('S5:species').options.map((o) => o.label), ['Dragonborn', 'Dwarf', 'Elf', 'Gnome', 'Goliath', 'Halfling', 'Human', 'Orc', 'Tiefling']);
  await p.choose('S5:species', 'Elf');
  assert.deepEqual(p.byKey('S5:sub').options.map((o) => o.label), ['Drow', 'High Elf', 'Wood Elf']);
});

test('/create shows "Our Name (5e Name)" for species, lineage, class and class option; values/state/rules keep the 5e names; live reload; kill switch', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  const p = new Player(makeCtx(dir), '3002', 'Bea');
  putNames(dir, FIXTURE);
  await toS5(p, 'Bea');
  const sp = p.byKey('S5:species').options;
  assert.equal(sp.find((o) => o.value === 'Human').label, 'PLACEHOLDER Meatsack (Human)');
  assert.equal(sp.find((o) => o.value === 'Dwarf').label, 'Dwarf');
  await p.choose('S5:species', 'Elf');
  assert.match(p.lastText, /\*\*PLACEHOLDER Pointy \(Elf\)\*\*/);
  assert.deepEqual(p.byKey('S5:sub').options.map((o) => [o.label, o.value]), [['Drow', 'Drow'], ['PLACEHOLDER Ivy League (High Elf)', 'High Elf'], ['Wood Elf', 'Wood Elf']]);
  await p.choose('S5:sub', 'High Elf');
  assert.match(p.lastText, /Elven lineage:\*\* PLACEHOLDER Ivy League \(High Elf\)/);
  await p.click('Next');
  assert.equal(p.byKey('S6:class').options.find((o) => o.value === 'Wizard').label, 'PLACEHOLDER Grad Student (Wizard)');
  await p.choose('S6:class', 'Cleric');
  assert.match(p.lastText, /\*\*PLACEHOLDER Chaplain \(Cleric\)\*\*/);
  const order = p.components().find((c) => c.custom_id?.includes('S6:choice:divine_order'));
  assert.deepEqual(order.options.map((o) => [o.label, o.value]), [['PLACEHOLDER Bodyguard (Protector)', 'Protector'], ['Thaumaturge', 'Thaumaturge']]);
  // live reload: the table changes mid-draft, no restart
  putNames(dir, { ...FIXTURE, entries: FIXTURE.entries.map((e) => (e.id === 'cleric' ? ent('cleric', 'class', 'Cleric', 'PLACEHOLDER Second Edition') : e)) });
  await p.click('◂ Back'); await p.click('Next');
  assert.equal(p.byKey('S6:class').options.find((o) => o.value === 'Cleric').label, 'PLACEHOLDER Second Edition (Cleric)');
  // switch: session.json create.species_class_reskin false (or missing) -> plain names, file untouched
  setFlag(dir, false);
  await p.click('◂ Back'); await p.click('Next');
  assert.equal(p.byKey('S6:class').options.find((o) => o.value === 'Cleric').label, 'Cleric');
  setFlag(dir, undefined);
  await p.click('◂ Back'); await p.click('Next');
  assert.equal(p.byKey('S6:class').options.find((o) => o.value === 'Cleric').label, 'Cleric', 'default is OFF');
  assert.ok(existsSync(namesFile(dir)));
});

test('the copy can sit in tables/ with the switch off: plain names until create.species_class_reskin is true', async () => {
  const dir = makeSandbox('beta');
  putNames(dir, FIXTURE, true, false);
  const cfg = (on) => ({ campaign: { dir, sessionId: 'beta', dataDir: join(dir, 'sessions-data', 'beta') }, on });
  assert.equal(speciesLabel(tablesFor(cfg()), 'Human'), 'Human');
  setFlag(dir, true);
  assert.equal(speciesLabel(tablesFor(cfg()), 'Human'), 'PLACEHOLDER Meatsack (Human)');
  setFlag(dir, 'yes');
  assert.equal(speciesLabel(tablesFor(cfg()), 'Human'), 'Human', 'only a real true turns it on');
});

test('variants are display-only: the loader keeps base_id, never lets a variant answer a species/lineage lookup, and /create offers no variant', async () => {
  const t = idx(FIXTURE);
  assert.equal(variantLabel(t, 'felid-cat', 'Cat'), 'PLACEHOLDER Tabby (Cat)');
  assert.equal(baseIdOf(t, 'felid-cat'), 'felid');
  assert.equal(baseIdOf(t, 'elf-high'), 'elf');
  assert.equal(baseIdOf(t, 'wizard'), 'wizard');
  assert.equal(baseIdOf(t, 'unknown'), 'unknown');
  assert.equal(speciesLabel(t, 'Felid'), 'PLACEHOLDER Whiskers (Felid)');
  assert.equal(speciesLabel(t, 'Felid Cat'), 'Felid Cat', 'a variant is not a species');
  assert.equal(nameLabel(t, 'felid-cat', 'Cat', { kind: 'species' }), 'Cat');
  assert.equal(variantLabel(t, 'felid', 'Felid'), 'Felid', 'a species id is not a variant');
  // lineage lookup uses base_id + the exact chargen option, even if the id differs
  const odd = idx({ entries: [ent('weird-id', 'species_lineage', 'High Elf', 'PLACEHOLDER Odd', 'elf', 'High Elf', { base_id: 'elf', chargen_value: 'High Elf' })] });
  assert.equal(lineageLabel(odd, 'Elf', 'High Elf'), 'PLACEHOLDER Odd (High Elf)');
  assert.equal(lineageLabel(odd, 'Elf', 'Drow'), 'Drow');
  // /create: the S5 picker lists exactly the nine SRD species; no variant value or house species appears
  const dir = makeSandbox('beta');
  putNames(dir, FIXTURE);
  const p = new Player(makeCtx(dir), '3006', 'Fay');
  await toS5(p, 'Fay');
  assert.deepEqual(p.byKey('S5:species').options.map((o) => o.value), ['Dragonborn', 'Dwarf', 'Elf', 'Gnome', 'Goliath', 'Halfling', 'Human', 'Orc', 'Tiefling']);
});

test('full walk with the names in place: S11/S16/S17 and the sheet file are labelled; state.json and the ledger hold only the 5e names', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  putNames(dir, FIXTURE);
  const p = new Player(makeCtx(dir), '3003', 'Cy');
  await p.command();
  let sawSpells = false;
  await drive(p, { name: 'Cy', species: 'Human', cls: 'Wizard', noShop: true, onS11: async (q) => { sawSpells = /\*\*PLACEHOLDER Grad Student \(Wizard\)\*\* \(/.test(q.lastText); await q.click('Pick for me'); await q.click('Next'); } });
  assert.ok(sawSpells, 'the spell screen names the class with its flavor name');
  assert.match(p.lastText, /Species \(Latent Biology\): PLACEHOLDER Meatsack \(Human\)/);
  assert.match(p.lastText, /Class \(Provisional\): PLACEHOLDER Grad Student \(Wizard\) 1/);
  await p.click('Confirm ▸');
  assert.match(p.lastText, /\*\*Cy\*\* - PLACEHOLDER Meatsack \(Human\) PLACEHOLDER Grad Student \(Wizard\) 1/);
  await p.click('Confirm and lock the file');
  const data = join(dir, 'sessions-data', 'beta');
  const st = JSON.parse(readFileSync(join(data, 'state.json'), 'utf8'));
  const c = st.crawlers.find((x) => x.name === 'Cy');
  assert.equal(c.species, 'Human');
  assert.equal(c.class, 'Wizard');
  assert.ok(!JSON.stringify(st).includes('PLACEHOLDER'), 'state keeps the 5e names only');
  const ledgerFile = join(data, 'credit-ledger.jsonl');
  if (existsSync(ledgerFile)) assert.ok(!readFileSync(ledgerFile, 'utf8').includes('PLACEHOLDER'));
  const sheet = readdirSync(join(data, 'characters')).filter((f) => f.endsWith('.md')).map((f) => readFileSync(join(data, 'characters', f), 'utf8')).join('\n');
  assert.match(sheet, /PLACEHOLDER Grad Student \(Wizard\)/);
  assert.match(sheet, /Species \(Latent Biology\): PLACEHOLDER Meatsack \(Human\)/);
});

test('a broken species-class-reskins.json never crashes /create: plain 5e names show', async () => {
  const dir = makeSandbox('beta');
  putNames(dir, '{ this is not json', false);
  assert.equal(speciesLabel(loadTables(dir), 'Human'), 'Human');
  const p = new Player(makeCtx(dir), '3004', 'Di');
  await toS5(p, 'Di');
  assert.equal(p.byKey('S5:species').options.find((o) => o.value === 'Human').label, 'Human');
});

test('Lore\'s real table (a copy, in a sandbox only): every species, lineage, class and class option /create shows gets its combined_label, each fits a select label', {
  skip: !existsSync(join(LORE, 'species-class-reskins.json')) && 'Lore\'s file is not on this box',
}, async () => {
  const dir = makeSandbox('beta');
  copyFileSync(join(LORE, 'species-class-reskins.json'), namesFile(dir));
  copyFileSync(join(LORE, 'species-class-reskins.version.json'), join(dir, 'tables', 'species-class-reskins.version.json'));
  bump(namesFile(dir));
  setFlag(dir, true);
  assert.equal(checkNamesHash(dir).status, 'ok');
  const t = loadTables(dir);
  const lore = JSON.parse(readFileSync(namesFile(dir), 'utf8'));
  const byId = new Map(lore.entries.map((e) => [e.id, e]));
  for (const [sp, v] of Object.entries(t.chargen.species)) {
    assert.equal(speciesLabel(t, sp), byId.get(kid(sp)).combined_label, sp);
    for (const o of v.sub?.options ?? []) {
      const e = byId.get(lineageId(sp, o));
      assert.ok(e, `lineage ${sp}/${o}`);
      assert.equal(lineageLabel(t, sp, o), e.combined_label);
      assert.ok(lineageLabel(t, sp, o).length <= 100);
    }
  }
  for (const [cl, v] of Object.entries(t.chargen.classes)) {
    assert.equal(classLabel(t, cl), byId.get(kid(cl)).combined_label, cl);
    for (const ch of v.choices ?? []) if (ch.key === 'divine_order' || ch.key === 'primal_order') for (const o of ch.options) assert.equal(classOptionLabel(t, cl, o), byId.get(classOptionId(cl, o)).combined_label);
  }
  const p = new Player(makeCtx(dir), '3005', 'Eve');
  await toS5(p, 'Eve');
  for (const o of p.byKey('S5:species').options) assert.ok(o.label !== o.value && o.label.endsWith(`(${o.value})`), `S5 ${o.value}: ${o.label}`);
});
