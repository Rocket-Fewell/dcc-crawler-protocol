import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import test from 'node:test';
import { loadTables } from '../src/create/data.js';
import * as R from '../src/create/rules.js';
import { findItem, revalidate, SCREENS } from '../src/create/screens.js';
import { buildBlock, newIntakeTag, slug, toSpec } from '../src/create/files.js';
import { nearDuplicate } from '../src/create/commit.js';
import { REAL_CAMPAIGN, Player, drive, finish, makeCtx, makeSandbox } from './helpers/create-harness.js';
import { runScript } from './helpers/create-script.js';

const t = loadTables(REAL_CAMPAIGN);
const base = (o = {}) => ({ uid: '1', uname: 'Ann', class: 'Fighter', species: 'Human', background: 'Soldier', asi: { type: '2-1', plus2: 'str', plus1: 'dex' }, method: 'array', base: { str: 15, dex: 14, con: 13, int: 12, wis: 10, cha: 8 }, ...o });

test('modifiers, standard array and point buy validation', () => {
  assert.equal(R.mod(8), -1);
  assert.equal(R.mod(15), 2);
  assert.equal(R.validateBase(base(), t), null);
  assert.match(R.validateBase(base({ base: { str: 15, dex: 15, con: 13, int: 12, wis: 10, cha: 8 } }), t), /exactly once/);
  const pb = base({ method: 'pointbuy', base: { str: 15, dex: 15, con: 15, int: 8, wis: 8, cha: 8 } });
  assert.equal(R.pointBuyCost(pb.base, t), 27);
  assert.equal(R.validateBase(pb, t), null);
  assert.match(R.validateBase({ ...pb, base: { ...pb.base, int: 15 } }, t), /costs 36/);
  assert.match(R.validateBase({ ...pb, base: { ...pb.base, int: 7 } }, t), /8-15/);
});

test('background bonus applies and no score may end above 20', () => {
  const d = base();
  assert.equal(R.finalAbilities(d, t).str, 17);
  const arr = R.buildArray('A', [[6, 6, 6, 1], [6, 6, 3, 1], [5, 5, 4, 1], [5, 4, 4, 1], [4, 4, 4, 1], [3, 3, 2, 1]]);   // 18 15 14 13 12 8 = 80
  assert.deepEqual(arr.scores, [18, 15, 14, 13, 12, 8]);
  const big = { ...d, method: 'roll', scoreRolls: { rounds: [{ round: 1, qualified: true, arrays: [arr, R.buildArray('B', Array(6).fill([1, 1, 1, 1])), R.buildArray('C', Array(6).fill([1, 1, 1, 1]))] }], kept: { round: 1, array: 'A' } }, base: { str: 18, dex: 15, con: 14, int: 13, wis: 12, cha: 8 }, asi: { type: '2-1', plus2: 'str', plus1: 'dex' } };
  assert.equal(R.validateBase(big, t), null);
  assert.equal(R.finalAbilities(big, t).str, 20);
  const over = { ...big, base: { ...big.base, str: 19 } };
  assert.ok(R.validateDraft(over, t).some((e) => e.screen === 'S8'));
});

test('HP, AC (armor, unarmored) and Dwarven Toughness', () => {
  const f = base({ kitClass: 'A', kitBg: 'A', cart: [] });
  assert.equal(R.hpMax(f, t), 10 + R.mod(R.finalAbilities(f, t).con));
  assert.equal(R.armorClass(f, t), 16);
  const w = base({ class: 'Wizard', background: 'Sage', asi: { type: '2-1', plus2: 'int', plus1: 'con' }, kitClass: 'A', kitBg: 'A', base: { str: 8, dex: 14, con: 13, int: 15, wis: 10, cha: 12 } });
  assert.equal(R.armorClass(w, t), 12);
  assert.equal(R.hpMax(w, t), 6 + R.mod(14));
  const dw = base({ species: 'Dwarf', class: 'Barbarian', kitClass: 'B', kitBg: 'B', base: { str: 15, dex: 13, con: 14, int: 8, wis: 10, cha: 12 }, asi: { type: '1-1-1' } });
  const fa = R.finalAbilities(dw, t);
  assert.equal(R.armorClass(dw, t), 10 + R.mod(fa.dex) + R.mod(fa.con));
  assert.equal(R.hpMax(dw, t), 12 + R.mod(fa.con) + 1);
});

test('credits: packages, vending math, breakdown rows sum to credits', () => {
  const d = base({ kitClass: 'A', kitBg: 'B', cart: [{ id: 'rations', qty: 12 }, { id: 'rope', qty: 1 }] });
  assert.equal(R.creditsFromPackages(d, t), 54);
  assert.equal(R.cartTotal(d, t), 7);
  const rows = R.creditBreakdown(d, t);
  assert.equal(rows.reduce((s, r) => s + r.delta, 0), 47);
  assert.ok(rows.every((r) => r.reason && r.source === 'intake'));
  assert.ok(R.creditsLeft({ ...d, cart: [{ id: 'plate', qty: 1 }] }, t) < 0);
});

test('findItem resolves typed names (5e or reskin names); the old junk field is never read', () => {
  assert.equal(findItem('rope', t), 'rope');
  assert.equal(findItem("healer's kit", t), 'healers_kit');
  assert.equal(findItem('nonsense item', t), null);
  assert.equal(findItem('Extension Cord, Fifty Feet, Unplugged', t), 'rope');   // a reskin display name
  assert.equal(findItem('Box Cutter', t), 'dagger');
  const d = base({ class: 'Wizard', background: 'Sage', kitClass: 'A', kitBg: 'A', cart: [], junk: { dagger: 'Letter Opener' } });
  const rows = R.inventoryRows(d, t);
  assert.ok(rows.some((r) => r.name === 'Box Cutter (Dagger)'), 'combined_label from item-reskins, not d.junk');
  assert.ok(!rows.some((r) => /Letter Opener/.test(r.name)));
  assert.ok(rows.some((r) => r.name === 'Intake Bag' && r.qty === 1));
});

test('revalidate drops picks that stopped being legal after a change', () => {
  const d = base({ classSkills: ['Athletics', 'Survival'], speciesSub: 'Red', kitClass: 'Z' });
  const dropped = revalidate(d, t);
  assert.ok(dropped.includes('species sub-choice'));
  assert.equal(d.speciesSub, null);
  assert.ok(dropped.includes('class skills')); // Athletics belongs to the Soldier background
  assert.ok(dropped.includes('class equipment'));
});

test('names: slug, near-duplicates, intake tag uniqueness', () => {
  assert.equal(slug('Trailer Park Moses!'), 'trailer-park-moses');
  assert.equal(nearDuplicate('Horn', ['Hornet', 'Ann']), 'Hornet');
  assert.equal(nearDuplicate('Hornet', ['hornet']), null);
  const used = new Set();
  for (let i = 0; i < 50; i++) {
    const tag = newIntakeTag(used);
    assert.match(tag, /^CRAWLER #\d{4}-[A-Z]$/);
    assert.ok(!used.has(tag));
    used.add(tag);
  }
});

test('every pre-built is legal and yields a balanced create-crawler spec', () => {
  assert.equal(t.prebuilt.crawlers.length, 12);
  for (const p of t.prebuilt.crawlers) {
    const d = { ...p, name: 'X', look: 'x', hook: 'x', backstory: 'x', uid: '9', uname: 'P', optouts: [], flow_version: '0.1', survey: [] };
    R.fillVariants(d, t);   // the flow does this when a pre-built is loaded
    assert.deepEqual(R.validateDraft(d, t), [], p.id);
    const spec = toSpec(d, t, 'CRAWLER #0001-A');
    assert.equal(spec.credits, spec.credit_breakdown.reduce((s, r) => s + r.delta, 0), p.id);
    assert.ok(spec.credits >= 0 && spec.hp_max > 0 && spec.ac >= 10, p.id);
  }
});

test('screens cover S1..S17 and Discord limits hold on the review screen', async () => {
  assert.deepEqual(Object.keys(SCREENS), R.SCREENS);
  const dir = makeSandbox('beta', ['--review', 'off']);
  const p = new Player(makeCtx(dir), '77', 'Lim');
  await p.command();
  await drive(p, { name: 'Lim', species: 'Human', cls: 'Wizard', bg: 'Sage' });
  assert.equal(p.screen(), 'S16');
  for (const c of p.components().filter((x) => x.options)) assert.ok(c.options.length <= 25);
  assert.ok(p.msg.components.length <= 5);
});

test('Back keeps answers; Restart keeps only the comfort answers', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  const p = new Player(makeCtx(dir), '88', 'Bo');
  await p.command();
  await p.click('ACCEPT');
  await p.form('S2:edit', { lines: 'zzsecretxx', veils: '' });
  await p.click('Next');
  await p.form('S3:name', { name: 'Bo' });
  await p.click('Next');
  await p.click('◂ Back');
  assert.match(p.lastText, /S3/);
  assert.match(p.lastText, /Bo/);
  await p.click('Restart');
  await p.click('Yes, wipe my answers');
  const dr = JSON.parse(readFileSync(join(dir, 'sessions-data', 'beta', 'create-drafts', '88.json'), 'utf8'));
  assert.equal(dr.name, undefined);
  assert.equal(dr.optouts[0].topic, 'zzsecretxx');
  assert.equal(dr.screen, 'S1');
});

test('S12 (fan tags) is retired: skipped in both directions, no tags stored, none on the sheet or the review screen', async () => {
  const d = { ...t.prebuilt.crawlers[0], name: 'X', look: 'x', hook: 'x', backstory: 'x', uid: '9', uname: 'P', optouts: [], flow_version: '0.1', survey: [], screen: 'S10' };
  R.fillVariants(d, t);
  assert.deepEqual(R.validateDraft(d, t), []);  // no tags needed to be legal
  const spec = toSpec(d, t, 'CRAWLER #0001-A');
  assert.equal(spec.fan_profile.public_tags, undefined);
  assert.equal(spec.build.fear_tag, undefined);
  assert.doesNotMatch(buildBlock(d, t), /Fan tags/);
  assert.equal(SCREENS.S12.title, 'Retired');
  const dir = makeSandbox('beta', ['--review', 'off']);
  const p = new Player(makeCtx(dir), '98', 'Di');
  await p.command();
  await drive(p, { name: 'Dina' });
  assert.equal(p.screen(), 'S16');  // S11-S15 filled, S12 never shown
  await finish(p);
  const sheets = readFileSync(join(dir, 'sessions-data', 'beta', 'characters', 'INDEX.md'), 'utf8');
  assert.match(sheets, /Dina/);
  const st = JSON.parse(readFileSync(join(dir, 'sessions-data', 'beta', 'state.json'), 'utf8'));
  assert.deepEqual(st.crawlers[0].fan_profile.public_tags ?? [], []);
});

test('a draft saved at the retired S12 resumes at S13', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  const p = new Player(makeCtx(dir), '97', 'Ed');
  await p.command();
  await p.click('ACCEPT');
  const f = join(dir, 'sessions-data', 'beta', 'create-drafts', '97.json');
  const d = JSON.parse(readFileSync(f, 'utf8'));
  d.screen = 'S12';
  writeFileSync(f, JSON.stringify(d));
  await p.command();
  assert.match(p.lastText, /S13/);
  assert.doesNotMatch(p.lastText, /S12/);
});

test('S3 rejects reserved names', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  const p = new Player(makeCtx(dir), '99', 'Cy');
  await p.command();
  await p.click('ACCEPT');
  await p.click('Skip');
  await p.form('S3:name', { name: 'GM' });
  assert.match(p.lastText, /will not work/);
  await p.form('S3:name', { name: 'Cyrus' });
  const d = JSON.parse(readFileSync(join(dir, 'sessions-data', 'beta', 'create-drafts', '99.json'), 'utf8'));
  assert.equal(d.name, 'Cyrus');
});

test('the spec 10-item test script passes against fresh beta sandboxes', { timeout: 120_000 }, async () => {
  const { results, realAlphaUnchanged } = await runScript();
  for (const r of results) assert.ok(r.pass, `#${r.n} ${r.name}: ${r.detail}`);
  assert.equal(results.length, 10);
  assert.ok(realAlphaUnchanged);
});
