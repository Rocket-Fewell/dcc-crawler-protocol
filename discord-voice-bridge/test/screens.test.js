// The /create "screens" display layer (Lore's create-screens-reskins.json) behind create.screens_reskin (default OFF): tx/txd rules, the merged flow lines,
// a flag-on walk over S3-S17 in a sandbox with Lore's real file, flag-off = vanilla, and a drop-in (new file, no restart). Fixture strings are placeholders.
import assert from 'node:assert/strict';
import { copyFileSync, existsSync, readFileSync, utimesSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import test from 'node:test';
import { TRACE, buildScreensIndex, mergeProposedLines, tx, txd } from '../src/create/screenstext.js';
import { LAYERS, layerFlags } from '../src/create/layers.js';
import { loadTables, tablesFor } from '../src/create/data.js';
import { Player, REAL_CAMPAIGN, drive, makeCtx, makeSandbox } from './helpers/create-harness.js';

const R = (id, old, nw, extra = {}) => ({ id, kind: 'notice', state: 'text', old, new: nw, placeholders: [...nw.matchAll(/\{(\w+)\}/g)].map((m) => m[0]), old_placeholders: [...old.matchAll(/\{(\w+)\}/g)].map((m) => m[0]), ...extra });
const mk = (...rows) => ({ screens: buildScreensIndex({ entries: rows }) });

test('tx: applies new only when the row exists, old still matches, and every placeholder is supplied; else the current text', () => {
  const t = mk(R('a', 'Pick {n} skills', 'PLACEHOLDER pick {n}'), R('b', 'Roll 3d6', 'PLACEHOLDER roll 3d6'));
  assert.equal(tx(t, 'a', 'Pick 2 skills', { n: 2 }), 'PLACEHOLDER pick 2');
  assert.equal(tx(t, 'a', 'Pick 2 skills'), 'Pick 2 skills');                    // placeholder not supplied
  assert.equal(tx(t, 'a', 'Choose 2 skills', { n: 2 }), 'Choose 2 skills');      // drift: the bridge text changed
  assert.equal(tx(t, 'zzz', 'Plain'), 'Plain');                                  // no row
  assert.equal(tx({}, 'a', 'Plain'), 'Plain');                                   // layer off (no index)
  assert.equal(tx(undefined, 'a', 'Plain'), 'Plain');
});

test('txd: chargen-data strings change only when the row old is exactly the data value', () => {
  const t = mk(R('c', 'Archery', 'PLACEHOLDER Bow Guy (Archery)'));
  assert.equal(txd(t, 'c', 'Archery'), 'PLACEHOLDER Bow Guy (Archery)');
  assert.equal(txd(t, 'c', 'Dueling'), 'Dueling');
});

test('buildScreensIndex drops rows with no new text or a lost rule number (never shown)', () => {
  const idx = buildScreensIndex({ entries: [R('ok', 'Standard array 15', 'PLACEHOLDER 15'), R('lost', 'Roll 4d6, drop 1', 'PLACEHOLDER roll them'), R('empty', 'x', ' ')] });
  assert.ok(idx.byId.has('ok'));
  assert.ok(!idx.byId.has('lost') && !idx.byId.has('empty'));
});

test('mergeProposedLines: keeps placeholders and numbers, skips a violating key, same object when nothing applies', () => {
  const base = { meta: {}, lines: { A: ['Hello {name}, 72'], B: ['Plain'], C: ['Keep {x}'] } };
  const prop = { loaded: true, lines: { A: ['PLACEHOLDER {name} 72', 'PLACEHOLDER2 {name} 72'], B: ['PLACEHOLDER plain'], C: ['PLACEHOLDER no placeholder'], D: ['not in base'] } };
  const m = mergeProposedLines(base, prop);
  assert.deepEqual(m.lines.A, prop.lines.A);
  assert.deepEqual(m.lines.B, prop.lines.B);
  assert.deepEqual(m.lines.C, base.lines.C);          // lost {x}: current stays
  assert.equal(m.lines.D, undefined);
  assert.equal(mergeProposedLines(base, { loaded: false, lines: {} }), base);
  assert.equal(mergeProposedLines(base, undefined), base);
  assert.deepEqual(base.lines.A, ['Hello {name}, 72']);   // not mutated
});

test('layers: the screens layers read create.screens_reskin (exactly true)', () => {
  assert.ok(LAYERS.has('screens') && LAYERS.has('screens_lines'));
  assert.equal(layerFlags({ screens_reskin: true }).screens, true);
  assert.equal(layerFlags({ screens_reskin: true }).screens_lines, true);
  assert.equal(layerFlags({ screens_reskin: 'true' }).screens, false);
  assert.equal(layerFlags({}).screens, false);
});

const setFlag = (dir, on) => {
  const sj = join(dir, 'sessions-data', 'beta', 'session.json');
  const prof = JSON.parse(readFileSync(sj, 'utf8'));
  prof.create = { ...(prof.create ?? {}), screens_reskin: on };
  writeFileSync(sj, JSON.stringify(prof));
  const t = new Date(Date.now() + 5000 + Math.floor(Math.random() * 1e6)); utimesSync(sj, t, t);
};
const labels = (p) => p.components().map((c) => c.label ?? c.placeholder ?? '');
const hasReal = existsSync(join(REAL_CAMPAIGN, 'tables', 'create-screens-reskins.json'));

test('flag off: later screens keep the plain text, buttons and flow lines; flag on: Lore labels and lines appear; both from the real table', { skip: !hasReal }, async () => {
  const dir = makeSandbox('beta');
  const ctx = makeCtx(dir);
  const p = new Player(ctx, '2001', 'Ann');
  await p.command();
  await drive(p, { cls: 'Warlock', bg: 'Acolyte' });                // flag OFF walk to S16
  const off = {};
  for (let i = 0; i < 16 && p.screen() !== 'S3'; i++) { off[p.screen()] = { text: p.lastText, labels: labels(p) }; await p.click('Back'); }
  assert.ok(labels(p).includes('Next ▸') && !labels(p).some((l) => /Onward/.test(l)));
  assert.ok(off.S8.labels.includes('Standard array') && off.S8.labels.includes('Roll'), off.S8.labels.join('|'));
  assert.ok(off.S14.labels.includes('Edit'));
  assert.ok(!/Factory Preset/.test(off.S8.text));
  assert.equal(tablesFor(ctx.config).lines.appliedProposed, undefined);
  // flag ON, same draft, walk back from S3 forward through every screen
  setFlag(dir, true);
  TRACE.on = true; TRACE.hit.clear(); TRACE.drift.clear();
  const on = {};
  await p.click('next'); await p.click('back');          // re-render S3 under the flag
  for (let i = 0; i < 16; i++) {
    on[p.screen()] = { text: p.lastText, labels: labels(p) };
    if (p.screen() === 'S16') break;
    await p.click('next');
  }
  for (const s of ['S3', 'S4', 'S6', 'S8', 'S9', 'S10', 'S11', 'S13', 'S14', 'S15', 'S16']) assert.ok(on[s], `reached ${s}`);
  const L = (s) => on[s].labels.join(' | ');
  assert.match(L('S3'), /Reprint the Name Tag \(Change name\)/);
  assert.match(L('S8'), /Factory Preset \(Standard array\)/);
  assert.match(L('S8'), /Layaway Plan \(Point buy\)/);
  assert.match(L('S8'), /Dice Gamble \(Roll\)/);
  assert.match(on.S8.text, /Factory Preset \(Standard array\) with 15, 14, 13, 12, 10, 8/);   // numbers kept
  assert.match(on.S8.text, /27 points/);
  assert.match(L('S9'), /Rehearsed Talents \(Class skills\): pick 2/);
  assert.match(L('S10'), /Intake Vending Wall/);
  assert.match(L('S14'), /Rewrite It \(Edit\)/);
  assert.match(L('S13'), /Pass on all/);   // S13 is a plain_on view: its buttons keep the old text
  assert.ok(!/Decline to Comment/.test(L('S13')));
  assert.match(on.S10.text, /\*\*Credits:\*\* \d+ from options, \d+ spent/);   // credits wording stays; amounts untouched
  assert.ok(!/champ/i.test(Object.values(on).map((x) => x.text + x.labels.join(' ')).join('\n')));
  // the only wired id allowed to fall back is the known title-s16 old/current mismatch
  assert.deepEqual([...TRACE.drift.keys()].filter((k) => k !== 'title-s16'), [], JSON.stringify([...TRACE.drift]));
  assert.ok(TRACE.hit.size >= 40, `hits ${TRACE.hit.size}`);
  // flow lines: the merged v0.1.2 lines apply only with the flag on, and the table file is untouched
  const t = tablesFor(ctx.config);
  assert.ok(t.lines.appliedProposed?.includes('S8_roll_closed'));
  assert.match(t.lines.lines.S8_roll_closed[0], /Dice Gamble \(Roll\)/);
  setFlag(dir, false);
  assert.equal(tablesFor(ctx.config).lines.appliedProposed, undefined);
  assert.match(tablesFor(ctx.config).lines.lines.S8_roll_closed[0], /^That method is closed today/);
  TRACE.on = false;
});

test('errors, notices and the help dialog read from the layer with the flag on, and the rules still reject bad input', { skip: !hasReal }, async () => {
  const dir = makeSandbox('beta');
  const ctx = makeCtx(dir);
  const p = new Player(ctx, '2002', 'Bea');
  await p.command();
  await drive(p, { cls: 'Fighter', bg: 'Soldier' });
  setFlag(dir, true);
  for (let i = 0; i < 16 && p.screen() !== 'S8'; i++) await p.click('back');
  await p.click('array');
  await p.form('S8:enter', { scores: '15 15 15 15 15 15' });
  const bad = p.lastText;
  assert.match(bad, /Factory Preset|each of 15, 14, 13, 12, 10, 8 exactly once/);
  assert.match(bad, /15, 14, 13, 12, 10, 8/);
  await p.click('help');
  assert.match(p.lastText, /\S/);
});

test('a new screens table version drops in without a restart (mtime reload), and a broken or drifted file falls back to the plain text', { skip: !hasReal }, async () => {
  const dir = makeSandbox('beta');
  setFlag(dir, true);
  const f = join(dir, 'tables', 'create-screens-reskins.json');
  const v = JSON.parse(readFileSync(f, 'utf8'));
  const row = v.entries.find((e) => e.id === 'button-edit');
  row.new = 'PLACEHOLDER Rewrite (Edit)'; row.combined_label = 'PLACEHOLDER Rewrite (Edit)';
  writeFileSync(f, JSON.stringify(v)); const t = new Date(Date.now() + 9e6); utimesSync(f, t, t);
  const ON = { layers: { screens: true, screens_lines: true } };
  assert.equal(tx(loadTables(dir, ON), 'button-edit', 'Edit'), 'PLACEHOLDER Rewrite (Edit)');
  writeFileSync(f, '{ not json'); const t2 = new Date(Date.now() + 19e6); utimesSync(f, t2, t2);
  assert.equal(tx(loadTables(dir, ON), 'button-edit', 'Edit'), 'Edit');
});
