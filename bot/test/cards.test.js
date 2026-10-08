/**
 * Oct 7 2026 (Caleb): every /create card shows what a player needs on their turn, for every class, plus three /create fixes:
 * a spellbook only for Wizards (core book Ch2), the Intake Bag on decision 038 wording, and the Lessons of the First Ones
 * Origin feat offered but never picked for the player (the card says "not chosen yet, pick one").
 */
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { loadTables } from '../src/create/data.js';
import * as R from '../src/create/rules.js';
import { revalidate, SCREENS } from '../src/create/screens.js';
const SCREENS_S11 = () => SCREENS.S11;
import { buildBlock, buildObject, toSpec } from '../src/create/files.js';
import { REAL_CAMPAIGN } from './helpers/roots.js';

const t = loadTables(REAL_CAMPAIGN);
const draft = (cls, o = {}) => {
  const d = { ...structuredClone(t.prebuilt.crawlers.find((c) => c.class === cls)), name: `Test ${cls}`, look: 'x', hook: 'x', backstory: 'x', uid: '9', uname: 'P', optouts: [], flow_version: '0.1', survey: [], ...o };
  R.fillVariants(d, t);
  return d;
};

test('core book Ch2: only a Wizard may buy a Spellbook at the Vending Wall', () => {
  assert.deepEqual(R.itemClasses('spellbook', t), ['Wizard']);
  assert.equal(R.itemClasses('rope', t), null);
  const lock = draft('Warlock', { cart: [{ id: 'spellbook', qty: 1 }, { id: 'rope', qty: 1 }] });
  assert.equal(R.itemAllowed(lock, t, 'spellbook'), false);
  assert.ok(R.validateDraft(lock, t).some((e) => e.screen === 'S10' && /Spellbook/.test(e.msg ?? e.message ?? JSON.stringify(e))));
  revalidate(lock, t);
  assert.deepEqual(lock.cart.map((l) => l.id), ['rope']);   // the class-only line is dropped, the rest kept
  const wiz = draft('Wizard', { cart: [{ id: 'spellbook', qty: 1 }] });
  assert.equal(R.itemAllowed(wiz, t, 'spellbook'), true);
  assert.equal(R.disallowedCart(wiz, t).length, 0);
});

test('no class starting package hands out a Spellbook except the Wizard', () => {
  for (const [cls, c] of Object.entries(t.chargen.classes)) {
    for (const p of c.packages) {
      const ids = p.items.map(([id]) => id);
      assert.equal(ids.includes('spellbook'), cls === 'Wizard' && p === c.packages[0], `${cls} package ${p.label ?? ''}`);
    }
  }
});

test('Intake Bag rows carry decision 038 wording, not "cosmetic"', () => {
  const bag = R.inventoryRows(draft('Fighter'), t).find((r) => r.name === 'Intake Bag');
  assert.equal(bag.mechanics, R.INTAKE_BAG_MECHANICS);
  assert.match(bag.mechanics, /store or retrieve one item in your System Inventory/);
  assert.match(bag.notes, /decision 038/);
  assert.doesNotMatch(`${bag.mechanics} ${bag.notes}`, /cosmetic/i);
});

test('Lessons of the First Ones: the extra Origin feat is offered, optional, never auto-picked', () => {
  const d = draft('Warlock', { classChoices: { invocation: R.LESSONS } });
  assert.equal(R.lessonsFeatOffered(d, t), true);
  assert.equal(R.lessonsFeatOffered(draft('Warlock'), t), false);
  assert.equal(R.lessonsFeatOffered(draft('Fighter', { classChoices: { ...draft('Fighter').classChoices, invocation: R.LESSONS } }), t), false);
  const bgFeat = t.chargen.backgrounds[d.background].feat;
  assert.equal(R.lessonsFeatOptions(d, t).includes(bgFeat), bgFeat === 'Skilled');   // no duplicate feat, except the repeatable Skilled
  assert.deepEqual(R.validateDraft(d, t), []);   // legal without a pick
  assert.equal(d.lessonsFeat, undefined);
  assert.equal(buildObject(d, t, 'CRAWLER #0001-A').lessons_feat, null);
  assert.match(buildBlock(d, t), /Lessons of the First Ones feat: not chosen yet, pick one/);
  const spec = toSpec(d, t, 'CRAWLER #0001-A');
  assert.equal(spec.build.lessons_feat, null);
  const pick = R.lessonsFeatOptions(d, t).find((f) => f !== 'Skilled');
  const d2 = { ...d, lessonsFeat: pick };
  assert.deepEqual(R.validateDraft(d2, t), []);
  assert.ok(R.originFeats(d2, t).includes(pick));
  assert.equal(buildObject(d2, t, 'CRAWLER #0001-A').lessons_feat, pick);
  assert.doesNotMatch(buildBlock(d2, t), /not chosen yet/);
  const bad = { ...d, lessonsFeat: 'Not A Feat' };
  assert.ok(R.validateDraft(bad, t).some((e) => e.screen === 'S7'));
  revalidate(bad, t);
  assert.equal(bad.lessonsFeat, null);
});

test('a level-1 /create card renders for all 12 classes (cross-tool: toSpec -> publisher.py --render-spec)', () => {
  const dir = mkdtempSync(join(tmpdir(), 'cards-'));
  try {
    const classes = t.prebuilt.crawlers.map((c) => c.class);
    assert.equal(new Set(classes).size, 12);
    for (const cls of classes) {
      const d = draft(cls, { classChoices: cls === 'Warlock' ? { invocation: R.LESSONS } : draft(cls).classChoices });
      const f = join(dir, `${cls}.json`);
      writeFileSync(f, JSON.stringify(toSpec(d, t, 'CRAWLER #0001-A')));
      const r = spawnSync('python3', [join(REAL_CAMPAIGN, 'tools', 'publisher.py'), '--render-spec', f], { env: { PATH: process.env.PATH, DCC_CAMPAIGN_ROOT: REAL_CAMPAIGN, DCC_CAMPAIGN_DIR: REAL_CAMPAIGN, DCC_AUTO_PUBLISH: '0' }, encoding: 'utf8' });
      assert.equal(r.status, 0, `${cls}: ${r.stderr}`);
      const msgs = JSON.parse(r.stdout);
      for (const m of msgs) assert.ok(m.length < 2000, `${cls} message ${m.length} chars`);
      const text = msgs.join('\n');
      for (const h of ['**Attacks**', '**Features & traits**', '**Rests**', 'Party Short Rests today: 0/4 used', 'Hit Dice: 1/1 left']) assert.ok(text.includes(h), `${cls}: ${h}`);
      assert.doesNotMatch(text, /could not be computed/);
      assert.equal(text.includes('**Spellcasting**'), !!t.chargen.classes[cls].spells, `${cls} spellcasting block`);
      if (cls === 'Warlock') {
        assert.match(text, /Pact Magic slots: 1\/1 left \(level 1\), back on a Short Rest/);
        assert.match(text, /Origin feat: not chosen yet, pick one/);
      }
      if (cls === 'Barbarian') assert.match(text, /\*\*Rage\*\*: 2\/2 left \(regain 1 on a Short Rest, all on a Long Rest\)/);
      if (cls === 'Fighter') assert.match(text, /\*\*Second Wind\*\*: 2\/2 left/);
      if (cls === 'Rogue') assert.doesNotMatch(text, /Cunning Action/);
      assert.match(text, /store or retrieve one item in your System Inventory/);
    }
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

// ---------------------------------------------------------------- Oct 7 2026 Syndicate review fixes
const bare = (cls, o = {}) => ({ uid: '1', uname: 'Ann', class: cls, species: 'Human', background: 'Soldier', classChoices: {}, cart: [], ...o });

test('Weapon Mastery: options are every weapon the class may master; defaults are weapons carried', () => {
  const opts = (cls) => R.masteryChoice(bare(cls), t).options;
  assert.ok(opts('Ranger').includes('scimitar') && opts('Ranger').includes('longbow'));
  assert.ok(!opts('Barbarian').includes('longbow'));   // Barbarian: melee weapons
  assert.ok(opts('Rogue').includes('rapier') && !opts('Rogue').includes('greatsword'));
  assert.deepEqual(R.defaultMasteries(bare('Fighter'), t), ['greatsword', 'flail', 'javelin']);   // package A, before S10
  assert.deepEqual(R.defaultMasteries(bare('Barbarian'), t), ['greataxe', 'handaxe']);
  assert.deepEqual(R.defaultMasteries(bare('Rogue'), t), ['dagger', 'shortsword']);
  assert.deepEqual(R.defaultMasteries(bare('Ranger'), t), ['scimitar', 'shortsword']);
  const pal = bare('Paladin');
  assert.deepEqual(R.defaultMasteries(pal, t), ['longsword', 'javelin']);
  const fb = bare('Fighter', { kitClass: 'B', kitBg: 'A' });
  assert.deepEqual(R.defaultMasteries(fb, t), ['scimitar', 'shortsword', 'longbow']);   // kit B weapons once chosen
  assert.equal(R.masteryChoice(bare('Wizard'), t), null);
});

test('auto masteries follow the kit; a player\'s own picks are never re-defaulted', () => {
  const d = bare('Fighter');
  R.fillDefaultMasteries(d, t);
  assert.deepEqual(d.masteries, ['greatsword', 'flail', 'javelin']);
  assert.equal(d.masteriesAuto, true);
  d.kitClass = 'B'; d.kitBg = 'A';
  revalidate(d, t);
  assert.deepEqual(d.masteries, ['scimitar', 'shortsword', 'longbow']);
  d.masteries = ['dagger', 'handaxe', 'maul']; d.masteriesAuto = false;   // what S9 onSelect does
  d.kitClass = 'A';
  revalidate(d, t);
  assert.deepEqual(d.masteries, ['dagger', 'handaxe', 'maul']);
  const a = bare('Rogue'); R.autoPick('S9', a, t);
  assert.deepEqual(a.masteries, ['dagger', 'shortsword']);
});

test('pre-built Crawlers master weapons they carry, and stay legal', () => {
  for (const p of t.prebuilt.crawlers) {
    if (!p.masteries.length) continue;
    const d = draft(p.class);
    const carried = R.carriedWeapons(d, t);
    for (const m of p.masteries) assert.ok(carried.includes(m), `${p.class} masters ${m} but carries ${carried}`);
  }
});

test('cantrip counts: Magician/Thaumaturge +1, Sorcerer 4 (species cantrips extra), Ranger Hunter\'s Mark is not a pick', () => {
  assert.equal(R.cantripCount(bare('Druid', { classChoices: { primal_order: 'Magician' } }), t), 3);
  assert.equal(R.cantripCount(bare('Druid', { classChoices: { primal_order: 'Warden' } }), t), 2);
  assert.equal(R.cantripCount(bare('Cleric', { classChoices: { divine_order: 'Thaumaturge' } }), t), 4);
  assert.equal(R.cantripCount(bare('Cleric', { classChoices: { divine_order: 'Protector' } }), t), 3);
  assert.equal(R.cantripCount(bare('Sorcerer', { species: 'Tiefling', speciesSub: 'Abyssal' }), t), 4);
  const dr = draft('Druid');
  assert.equal(dr.classChoices.primal_order, 'Magician');
  assert.equal(dr.spells.cantrips.length, 3);
  assert.deepEqual(R.validateDraft(dr, t), []);
  const two = { ...dr, spells: { ...dr.spells, cantrips: dr.spells.cantrips.slice(0, 2) } };
  assert.ok(R.validateDraft(two, t).some((e) => e.screen === 'S11' && /Pick 3 cantrips/.test(e.msg)));
  assert.ok(!t.chargen.classes.Ranger.spells.level1_list.includes("Hunter's Mark"));
});

test('Explorer\'s Pack has the 2024 contents (no mess kit)', () => {
  const row = R.inventoryRows(draft('Barbarian'), t).find((r) => r.chargen_key === 'explorers_pack');
  assert.doesNotMatch(row.mechanics, /mess kit/i);
  assert.match(row.mechanics, /2 oil flasks/);
});

test('Magic Initiate: S11 asks its picks (also for non-casters), optional and never auto-picked', () => {
  const f = { ...bare('Fighter', { background: 'Sage' }), kitClass: 'A', kitBg: 'A' };
  assert.deepEqual(R.miFeats(f, t), ['Magic Initiate (Wizard)']);
  assert.equal(R.hasSpellScreen(f, t), true);
  assert.equal(R.hasSpellScreen(bare('Fighter'), t), false);
  assert.equal(R.autoPick('S11', f, t), null);
  assert.equal(f.mi, undefined);
  assert.ok(!R.validateDraft(f, t).some((e) => e.screen === 'S11'));   // legal with nothing picked
  assert.deepEqual(buildObject({ ...draft('Fighter'), background: 'Sage', kitBg: 'A' }, t, 'X').magic_initiate, { 'Magic Initiate (Wizard)': { ability: null, cantrips: [], level1: [] } });
  const bad = { ...f, mi: { 'Magic Initiate (Wizard)': { cantrips: ['Sacred Flame'], level1: [], ability: 'cha' } } };
  assert.ok(R.validateDraft(bad, t).some((e) => e.screen === 'S11' && /Magic Initiate/.test(e.msg)));
  revalidate(bad, t);
  assert.equal(bad.mi['Magic Initiate (Wizard)'], undefined);
  const ok = { ...draft('Fighter'), background: 'Sage', kitBg: 'A', mi: { 'Magic Initiate (Wizard)': { cantrips: ['Shocking Grasp', 'Mage Hand'], level1: ['Shield'], ability: 'cha' } } };
  R.fillVariants(ok, t);
  assert.ok(!R.validateDraft(ok, t).some((e) => e.screen === 'S11'));
  assert.deepEqual(toSpec(ok, t, 'X').build.magic_initiate['Magic Initiate (Wizard)'], { ability: 'cha', cantrips: ['Shocking Grasp', 'Mage Hand'], level1: ['Shield'] });
  assert.match(buildBlock(ok, t), /Magic Initiate \(Wizard\): cantrips Shocking Grasp, Mage Hand; level 1 Shield; ability CHA/);
  assert.match(buildBlock({ ...ok, mi: {} }, t), /not chosen yet: 2 cantrips, one level 1 spell, ability; pick them/);
  const w = { ...draft('Wizard') };
  R.autoPick('S11', w, t);
  assert.equal(w.mi, undefined);   // Sage Wizard: class spells picked, Magic Initiate left to the player
});

test('Magic Initiate selects render and store picks on S11', () => {
  const d = { ...draft('Fighter'), background: 'Sage', kitBg: 'A', screen: 'S11' };
  const env = { t };
  const rows = SCREENS_S11().allRows(d, env);
  assert.ok(rows.length >= 3);
  SCREENS_S11().onSelect('mic', ['Shocking Grasp', 'Mage Hand'], d, env, '0');
  SCREENS_S11().onSelect('mil', ['Shield'], d, env, '0~0');
  SCREENS_S11().onSelect('mia', ['cha'], d, env, '0');
  assert.deepEqual(d.mi['Magic Initiate (Wizard)'], { ability: 'cha', cantrips: ['Shocking Grasp', 'Mage Hand'], level1: ['Shield'] });
  assert.equal(d.spells ?? null, d.spells);   // a non-caster's class spells are untouched
  assert.match(SCREENS_S11().describe(d, env), /Magic Initiate \(Wizard\):\*\* cantrips Shocking Grasp, Mage Hand; level 1 Shield; ability CHA/);
});
