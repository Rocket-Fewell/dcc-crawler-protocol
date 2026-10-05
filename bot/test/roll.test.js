// The Roll ability method for /create (decision 024, spec v0.1.10 section 3.6). Discord is faked; roll.py is either scripted (deterministic dice) or the real tool.
import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import test from 'node:test';
import { handleInteraction } from '../src/commands/index.js';
import { archiveIdle } from '../src/create/store.js';
import { lockedUsers, makeEnv } from '../src/create/flow.js';
import { defaultRun } from '../src/create/commit.js';
import { loadTables } from '../src/create/data.js';
import * as R from '../src/create/rules.js';
import { createSettings } from '../src/create/settings.js';
import { REAL_CAMPAIGN, Player, drive, finish, makeCtx, makeSandbox } from './helpers/create-harness.js';

const t = loadTables(REAL_CAMPAIGN);

/** four d6 whose best three add up to `s` (3-18); the fourth die is a 1 and is dropped */
const diceFor = (s) => {
  let rem = s;
  const out = [];
  for (let k = 3; k >= 1; k--) { const v = Math.min(6, rem - (k - 1)); out.push(v); rem -= v; }
  return [...out, 1];
};
const ARR = {
  A: [15, 14, 13, 12, 12, 12],   // 78: keepable
  B: [10, 10, 10, 10, 10, 10],   // 60
  C: [14, 14, 14, 13, 13, 12],   // 80: keepable
};
const LOW = { A: Array(6).fill(10), B: Array(6).fill(10), C: [12, 12, 12, 12, 12, 11] };   // 60 / 60 / 71: nothing above 72

/** A scripted `run`: roll.py answers from plan(round, id) -> six scores; everything else goes to the real tools. */
function scripted(plan, delayMs = 0) {
  const calls = [];
  const run = async (cmd, args, opts) => {
    if (!String(args[0]).endsWith('roll.py')) return defaultRun(cmd, args, opts);
    const label = args[args.indexOf('--label') + 1];
    const who = args[args.indexOf('--who') + 1];
    const m = /^S8 roll r(\d+) ([ABC])([1-6])$/.exec(label);
    calls.push({ label, who, expr: args.at(-1), session: opts?.env?.DCC_SESSION });
    if (delayMs) await new Promise((r) => setTimeout(r, delayMs));
    const sc = plan(Number(m[1]), m[2])[Number(m[3]) - 1];
    return { ok: true, stdout: JSON.stringify({ terms: [{ rolls: diceFor(sc) }], total: sc }), stderr: '' };
  };
  return { run, calls };
}

const draftOf = (dir, uid) => JSON.parse(readFileSync(join(dir, 'sessions-data', 'beta', 'create-drafts', `${uid}.json`), 'utf8'));
const setup = (plan, args = ['--review', 'off'], delayMs = 0) => {
  const dir = makeSandbox('beta', args);
  const s = scripted(plan, delayMs);
  const ctx = makeCtx(dir, 'beta', { create: { run: s.run } });
  return { dir, ctx, ...s };
};

/** S1-S7 for a Human Fighter / Soldier, stopping on S8 (the screen with the method buttons). */
async function toS8(p, name = 'Ann') {
  await p.command();
  if (/Resume your intake/.test(p.lastText)) { await p.click('Resume'); if (p.screen() !== 'S1') return; }
  await p.click('ACCEPT'); await p.click('Skip');
  await p.form('S3:name', { name }); await p.click('Next');
  await p.form('S4:edit', { look: 'Sweatpants and regret', hook: 'Hits things very hard' }); await p.click('Next');
  await p.choose('S5:species', 'Human'); await p.click('Next');
  await p.choose('S6:class', 'Fighter'); if (p.components().some((c) => c.custom_id?.includes('S6:choice'))) await p.click('Pick for me'); await p.click('Next');
  await p.choose('S7:bg', 'Soldier'); await p.choose('S7:asi', p.byKey('S7:asi').options[0].value);
  if (p.byKey('S7:feat')) await p.choose('S7:feat', p.byKey('S7:feat').options[0].value);
  await p.click('Next');
}

/** Keep an array and assign its scores to STR..CHA in the given order of indexes (by score value). Walks the pages of selects. */
async function assign(p, scores) {
  const ab = ['str', 'dex', 'con', 'int', 'wis', 'cha'];
  const used = new Set();
  for (let k = 0; k < 6; k++) {
    for (let guard = 0; guard < 4 && !p.byKey(`S8:assign:${ab[k]}`); guard++) await p.click('More');
    const menu = p.byKey(`S8:assign:${ab[k]}`);
    const opt = menu.options.find((o) => Number(o.label) === scores[k] && !used.has(o.value));
    assert.ok(opt, `no option ${scores[k]} for ${ab[k]}: ${menu.options.map((o) => o.label)}`);
    used.add(opt.value);
    await p.choose(`S8:assign:${ab[k]}`, opt.value);
  }
}

test('Roll: three arrays, 18 logged calls, non-keepable array disabled with its reason, keep one, assign, confirm', async () => {
  const { dir, ctx, calls } = setup((r, id) => ARR[id]);
  const p = new Player(ctx, '1001', 'Ann');
  await toS8(p);
  assert.ok(p.find((c) => c.label === 'Roll'), 'Roll button is offered by default');
  assert.match(p.lastText, /rolls three arrays of six scores/);
  await p.click('Roll');
  assert.equal(calls.length, 18);
  assert.deepEqual(calls.map((c) => c.label), ['A', 'B', 'C'].flatMap((id) => [1, 2, 3, 4, 5, 6].map((n) => `S8 roll r1 ${id}${n}`)));
  assert.ok(calls.every((c) => c.who === 'Ann' && c.expr === '4d6dl1'));
  assert.match(p.lastText, /A:\*\* 15 14 13 12 12 12 = \*\*78\*\*  Keepable \(total 78\)/);
  assert.match(p.lastText, /B:\*\* .* = \*\*60\*\*  Not keepable \(total 60, needs 73 or more\)/);
  assert.match(p.lastText, /~~1~~/);                                      // the dropped die is shown struck through
  assert.ok(p.disabled('Keep B') && !p.disabled('Keep A') && !p.disabled('Keep C'));
  assert.ok(p.disabled('Next'));
  await assert.rejects(p.click('Keep B'), /disabled/);
  await p.click('Keep C');
  assert.match(p.lastText, /Assign your scores/);
  assert.match(p.lastText, /No score goes above 20/);
  await assign(p, [14, 14, 14, 13, 13, 12]);
  assert.deepEqual(draftOf(dir, '1001').base, { str: 14, dex: 14, con: 14, int: 13, wis: 13, cha: 12 });
  // each score once: a used score is not offered to the other abilities
  while (!p.byKey('S8:assign:str')) await p.click('More');
  assert.equal(p.byKey('S8:assign:str').options.length, 6 - 5);
  assert.ok(!p.disabled('Next'));
});

test('Roll end to end: build.score_method / score_base / score_rolls are stored, abilities = base + background, dice re-checked', async () => {
  const { dir, ctx } = setup((r, id) => ARR[id]);
  const p = new Player(ctx, '1002', 'Bea');
  await p.command();
  await drive(p, { name: 'Bea', noShop: true, onS8: async (q) => { await q.click('Roll'); await q.click('Keep A'); await assign(q, [15, 14, 13, 12, 12, 12]); } });
  const d = draftOf(dir, '1002');
  assert.equal(d.method, 'roll');
  assert.equal(R.validateBase(d, t), null);
  await finish(p);
  const st = JSON.parse(readFileSync(join(dir, 'sessions-data', 'beta', 'state.json'), 'utf8'));
  const c = st.crawlers.find((x) => x.name === 'Bea');
  assert.equal(c.build.score_method, 'roll');
  assert.deepEqual(Object.values(c.build.score_base).sort((a, b) => b - a), [15, 14, 13, 12, 12, 12]);
  assert.equal(c.build.score_rolls.rounds.length, 1);
  assert.equal(c.build.score_rolls.rounds[0].arrays.length, 3);
  assert.deepEqual(c.build.score_rolls.kept, { round: 1, array: 'A' });
  const applied = c.build.background_asi.applied;
  for (const k of Object.keys(c.build.score_base)) assert.equal(c.abilities[k], c.build.score_base[k] + applied[k]);
  assert.ok(Object.values(c.abilities).every((v) => v <= 20));
});

test('Roll: when no array totals above 72 the System rerolls all three (logged), shows the failed round, and stops after 10 rounds', async () => {
  const two = setup((r, id) => (r === 1 ? LOW[id] : ARR[id]));
  const p = new Player(two.ctx, '1003', 'Cy');
  await toS8(p, 'Cy');
  await p.click('Roll');
  assert.equal(two.calls.length, 36);
  assert.ok(two.calls.some((c) => c.label === 'S8 roll r2 C6'));
  assert.match(p.lastText, /Round 1: A 60, B 60, C 71 \(none above 72\)/);
  assert.match(p.lastText, /The System has filed your luck and is rolling all three again/);
  assert.match(p.lastText, /Round 2\./);
  assert.equal(draftOf(two.dir, '1003').scoreRolls.rounds.length, 2);

  const never = setup((r, id) => LOW[id]);
  const q = new Player(never.ctx, '1004', 'Dee');
  await toS8(q, 'Dee');
  await q.click('Roll');
  assert.equal(never.calls.length, 180);                                  // 10 rounds x 18, then it stops
  assert.match(q.lastText, /10 rounds and no array above 72\. That should not happen\. Pick the standard array or point buy\./);
  assert.ok(q.find((c) => c.label === 'Standard array'));
  assert.equal(draftOf(never.dir, '1004').method, null);
  assert.equal(draftOf(never.dir, '1004').scoreRolls.rounds.length, 10);
  const log = readFileSync(join(never.dir, 'sessions-data', 'beta', 'create-log.jsonl'), 'utf8');
  assert.match(log, /"event":"roll_giveup"/);
  await q.click('Roll');                                                  // pressing it again never rolls more
  assert.equal(never.calls.length, 180);
  assert.match(q.lastText, /10 rounds and no array above 72/);
  await q.click('Standard array'); await q.click('Pick for me');          // the other two methods still work
  assert.ok(!q.disabled('Next'));
});

test('Roll: no free reroll on Back, Edit, changing method, or Restart', async () => {
  const { dir, ctx, calls } = setup((r, id) => ARR[id]);
  const p = new Player(ctx, '1005', 'Eli');
  await toS8(p, 'Eli');
  await p.click('Roll');
  const first = JSON.stringify(draftOf(dir, '1005').scoreRolls.rounds);
  assert.equal(calls.length, 18);
  await p.click('Keep A');
  await p.click('◂ Back');                                                // S7
  assert.equal(p.screen(), 'S7');
  await p.click('Next');                                                  // back on S8
  await p.click('Roll');
  assert.equal(calls.length, 18);                                         // the same saved round, no new dice
  assert.equal(JSON.stringify(draftOf(dir, '1005').scoreRolls.rounds), first);
  await p.click('Standard array'); await p.click('Roll');                 // change method and come back
  assert.equal(calls.length, 18);
  assert.match(p.lastText, /Round 1\./);
  // resume from a new client
  const later = new Player(ctx, '1005', 'Eli');
  await later.command(); await later.click('Resume');
  assert.equal(JSON.stringify(draftOf(dir, '1005').scoreRolls.rounds), first);
  // Restart wipes the answers but not the rolled rounds
  await later.click('Restart'); await later.click('Yes, wipe my answers');
  const wiped = draftOf(dir, '1005');
  assert.equal(wiped.name, undefined);
  assert.equal(JSON.stringify(wiped.scoreRolls.rounds), first);
  assert.equal(wiped.scoreRolls.kept, null);
  await toS8(later, 'Eli');
  await later.click('Roll');
  assert.equal(calls.length, 18);                                         // still no new dice
  assert.match(later.lastText, /Round 1\./);
  await later.click('Keep C');                                            // the player can still keep one of the same arrays
  assert.equal(draftOf(dir, '1005').scoreRolls.kept.array, 'C');
});

test('Roll: S17 re-check from the stored dice (tampered totals, kept array, assignment, skipped rounds)', () => {
  const mk = (sets) => R.buildArray('X', sets.map(diceFor));
  const round = (n, tot) => R.buildRound(n, { A: ARRAYS(tot), B: ARRAYS(60), C: ARRAYS(60) });
  const ARRAYS = (tot) => { const base = Math.floor(tot / 6); const extra = tot - base * 6; return Array.from({ length: 6 }, (_, i) => diceFor(base + (i < extra ? 1 : 0))); };
  void mk;
  const good = { rounds: [round(1, 73)], kept: { round: 1, array: 'A' } };
  const d = { method: 'roll', scoreRolls: good, base: { str: 13, dex: 12, con: 12, int: 12, wis: 12, cha: 12 } };
  assert.equal(R.validateBase(d, t), null);                                // 73 qualifies
  assert.match(R.validateBase({ ...d, base: { ...d.base, str: 14 } }, t), /each exactly once/);   // not the kept array's scores
  const copy = () => JSON.parse(JSON.stringify(good));
  const tamper = copy(); tamper.rounds[0].arrays[0].dice[0] = [6, 6, 6, 1];                    // the dice no longer add up to the stored total
  assert.match(R.validateBase({ ...d, scoreRolls: tamper }, t), /do not match the dice/);
  const forged = copy(); forged.rounds[0].arrays[0].total = 99; forged.rounds[0].arrays[0].keepable = true;
  assert.match(R.validateBase({ ...d, scoreRolls: forged }, t), /do not match the dice/);
  const noKeep = copy(); noKeep.kept = { round: 1, array: 'B' };                                  // B totals 60
  assert.match(R.validateBase({ ...d, scoreRolls: noKeep }, t), /needs 73 or more/);
  const edge = { rounds: [R.buildRound(1, { A: ARRAYS(72), B: ARRAYS(72), C: ARRAYS(72) })], kept: { round: 1, array: 'A' } };
  assert.match(R.validateBase({ ...d, scoreRolls: edge }, t), /Keep an array|needs 73 or more/);   // 72 is not enough
  assert.ok(!edge.rounds[0].qualified);
  const skipped = { rounds: [round(1, 80), round(2, 80)], kept: { round: 2, array: 'A' } };       // rerolled past a keepable round
  assert.match(R.validateBase({ ...d, scoreRolls: skipped }, t), /cannot be rolled past/);
  const early = copy(); early.kept = { round: 2, array: 'A' };
  assert.match(R.validateBase({ ...d, scoreRolls: early }, t), /final round/);
  assert.match(R.validateBase({ ...d, scoreRolls: { rounds: [], kept: null } }, t), /Roll your three arrays/);
  assert.match(R.validateBase({ ...d, scoreRolls: { rounds: Array.from({ length: 11 }, (_, i) => round(i + 1, 60)), kept: null } }, t), /Roll your three arrays/);
});

test('Roll: no upper limit on the total, and the 20 cap holds after the background bonus', () => {
  const six = (s) => Array.from({ length: 6 }, () => diceFor(s));
  const top = R.buildRound(1, { A: six(18), B: six(3), C: six(3) });
  assert.equal(top.arrays[0].total, 108);
  assert.ok(top.arrays[0].keepable);
  const d = { uid: '1', class: 'Fighter', species: 'Human', background: 'Soldier', asi: { type: '2-1', plus2: 'str', plus1: 'dex' }, method: 'roll', scoreRolls: { rounds: [top], kept: { round: 1, array: 'A' } }, base: { str: 18, dex: 18, con: 18, int: 18, wis: 18, cha: 18 } };
  assert.equal(R.validateBase(d, t), null);
  const fa = R.finalAbilities(d, t);
  assert.equal(fa.str, 20);                                                // 18 + 2
  assert.equal(fa.dex, 19);                                                // 18 + 1
  assert.ok(Object.values(fa).every((v) => v <= 20));
  assert.ok(!R.validateDraft(d, t).some((e) => e.screen === 'S8'));
  assert.ok(R.validateDraft({ ...d, base: { ...d.base, str: 19 } }, t).some((e) => e.screen === 'S8'));   // 19 was never rolled
});

test('allow_roll: default ON; off hides Roll and its text, an old Roll button gets the closed line, saved rounds come back when it is switched on again', async () => {
  assert.equal(createSettings({ campaign: { sessionId: 'nope', dir: REAL_CAMPAIGN } }).allowRoll, true);

  const off = setup((r, id) => ARR[id], ['--review', 'off', '--no-roll']);
  assert.equal(JSON.parse(readFileSync(join(off.dir, 'sessions-data', 'beta', 'session.json'), 'utf8')).create.allow_roll, false);
  const p = new Player(off.ctx, '1006', 'Fay');
  await toS8(p, 'Fay');
  assert.ok(!p.find((c) => c.label === 'Roll'));
  assert.ok(p.find((c) => c.label === 'Standard array') && p.find((c) => c.label === 'Point buy'));
  assert.doesNotMatch(p.lastText, /Roll:|three arrays|rolling/i);
  await handleInteraction(p.fake({ isButton: () => true, isMessageComponent: () => true, customId: 'create:1006:S8:roll' }), off.ctx);   // a stale Roll button
  assert.match(p.lastText, /That method is closed today\. Pick the standard array or point buy\./);
  assert.equal(off.calls.length, 0);
  await p.click('Standard array'); await p.click('Pick for me');
  assert.ok(!p.disabled('Next'));                                          // the other methods behave as before

  // on, roll, then the table switches it off mid-draft and back on
  const on = setup((r, id) => ARR[id]);
  const q = new Player(on.ctx, '1007', 'Gus');
  await toS8(q, 'Gus');
  await q.click('Roll');
  const sj = join(on.dir, 'sessions-data', 'beta', 'session.json');
  const prof = JSON.parse(readFileSync(sj, 'utf8'));
  prof.create.allow_roll = false;
  writeFileSync(sj, JSON.stringify(prof));
  const later = new Player(on.ctx, '1007', 'Gus');
  await later.command(); await later.click('Resume');
  assert.ok(!later.find((c) => c.label === 'Roll'));
  assert.ok(later.disabled('Next'));                                       // back on the method screen
  prof.create.allow_roll = true;
  writeFileSync(sj, JSON.stringify(prof));
  const again = new Player(on.ctx, '1007', 'Gus');
  await again.command(); await again.click('Resume');
  await again.click('Roll');
  assert.equal(on.calls.length, 18);                                       // the held rounds are shown, nothing is re-rolled
  assert.match(again.lastText, /Round 1\./);
});

test('Roll with the real roll.py: 18 [ROLL] lines per round land in THIS session\'s data dir (beta), labelled for the Crawler', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  const ctx = makeCtx(dir);
  const p = new Player(ctx, '1008', 'Hal');
  await toS8(p, 'Hal');
  await p.click('Roll');
  const rounds = draftOf(dir, '1008').scoreRolls.rounds;
  const logs = readdirSync(join(dir, 'sessions-data', 'beta')).filter((f) => /^rolls-.*\.log$/.test(f));
  assert.equal(logs.length, 1);
  assert.deepEqual(readdirSync(join(dir, 'sessions')).filter((f) => /^rolls-/.test(f)), [], 'nothing was logged into the alpha data dir');
  const lines = readFileSync(join(dir, 'sessions-data', 'beta', logs[0]), 'utf8').split('\n').filter((l) => l.includes('S8 roll r'));
  assert.equal(lines.length, 18 * rounds.length);
  for (let r = 1; r <= rounds.length; r++) for (const id of 'ABC') for (let n = 1; n <= 6; n++) assert.ok(lines.some((l) => l.includes(`[ROLL] S8 roll r${r} ${id}${n} (Hal): 4d6dl1 ->`)), `r${r} ${id}${n}`);
  for (const r of rounds) for (const a of r.arrays) { assert.equal(a.scores.length, 6); assert.ok(a.scores.every((s) => s >= 3 && s <= 18)); assert.equal(a.total, a.scores.reduce((x, y) => x + y, 0)); assert.equal(a.keepable, a.total > 72); }
});

test('Roll passes DCC_SESSION to roll.py', async () => {
  const { ctx, calls } = setup((r, id) => ARR[id]);
  const p = new Player(ctx, '1009', 'Ian');
  await toS8(p, 'Ian');
  await p.click('Roll');
  assert.equal(calls.length, 18);
  assert.ok(calls.every((c) => c.session === 'beta'));
});

test('Roll lines: nine keys exist with the spec wording, no pet hint, "Crawler" never lowercase', () => {
  const keys = ['S8_roll_offer', 'S8_roll_result', 'S8_roll_keep_ok', 'S8_roll_keep_no', 'S8_roll_none', 'S8_roll_assign', 'S8_roll_cap', 'S8_roll_giveup', 'S8_roll_closed'];
  for (const k of keys) {
    const v = t.lines.lines[k];
    assert.ok(Array.isArray(v) && v.length === 1 && v[0].length > 10, k);
    assert.doesNotMatch(v[0], /\bpets?\b|familiar|champ|crawler/i, k);
  }
  assert.equal(t.lines.lines.S8_roll_keep_ok[0], 'Keepable (total {total})');
  assert.equal(t.lines.lines.S8_roll_giveup[0], '{rounds} rounds and no array above 72. That should not happen. Pick the standard array or point buy.');
});

test('B1: an idle draft with rolled rounds is never archived; one without is; a Confirmed Crawler still deletes its draft', async () => {
  const { dir, ctx } = setup((r, id) => ARR[id]);
  const p = new Player(ctx, '1010', 'Jo');
  const q = new Player(ctx, '1011', 'Kai');
  await toS8(p, 'Jo'); await p.click('Roll');
  await q.command();                                                       // a fresh draft with no rolls
  const dd = join(dir, 'sessions-data', 'beta', 'create-drafts');
  const config = ctx.config;
  const later = Date.now() + 20 * 86_400_000;
  // archiveIdle looks at mtime: 20 days on is "idle" for both
  assert.equal(archiveIdle(config, 14, later), 1);
  assert.ok(existsSync(join(dd, '1010.json')), 'the rolled draft stays');
  assert.ok(!existsSync(join(dd, '1011.json')), 'the plain idle draft moves to _archive');
  assert.equal(readdirSync(join(dd, '_archive')).length, 1);
  assert.equal(archiveIdle(config, 14, later + 400 * 86_400_000), 0);      // however long it idles
  const again = new Player(ctx, '1010', 'Jo');
  await again.command(); await again.click('Resume');
  await again.click('Roll');                                               // the same saved round
  assert.equal(draftOf(dir, '1010').scoreRolls.rounds.length, 1);
  // Confirm deletes the draft (and with it the saved rounds)
  const r = new Player(ctx, '1012', 'Lee');
  await r.command();
  await drive(r, { name: 'Lee', noShop: true, onS8: async (x) => { await x.click('Roll'); await x.click('Keep A'); await assign(x, [15, 14, 13, 12, 12, 12]); } });
  assert.ok(existsSync(join(dd, '1012.json')));
  await finish(r);
  assert.ok(!existsSync(join(dd, '1012.json')), 'a registered Crawler deletes its draft');
});

test('B2: three simultaneous Roll presses roll once (18 calls, not 54); Keep acts on the draft the screen shows; the lock chain empties', async () => {
  const { dir, ctx, calls } = setup((r, id) => ARR[id], ['--review', 'off'], 15);
  const p = new Player(ctx, '1013', 'Mo');
  await toS8(p, 'Mo');
  const c = p.find((x) => x.label === 'Roll');
  const press = () => handleInteraction(p.fake({ isButton: () => true, isMessageComponent: () => true, customId: c.custom_id }), ctx);
  await Promise.all([press(), press(), press()]);
  assert.equal(calls.length, 18);
  assert.equal(draftOf(dir, '1013').scoreRolls.rounds.length, 1);
  assert.equal(lockedUsers(), 0);
  // two Keep presses at once: they run one after the other, the last one wins, and the draft is consistent
  const keep = (label) => { const b = p.find((x) => x.label === label); return handleInteraction(p.fake({ isButton: () => true, isMessageComponent: () => true, customId: b.custom_id }), ctx); };
  await Promise.all([keep('Keep A'), keep('Keep C')]);
  assert.deepEqual(draftOf(dir, '1013').scoreRolls.kept, { round: 1, array: 'C' });
  assert.equal(lockedUsers(), 0);
  // two /create entries at once make one draft
  const other = new Player(ctx, '1014', 'Ned');
  await Promise.all([other.command(), other.command()]);
  assert.equal(readdirSync(join(dir, 'sessions-data', 'beta', 'create-drafts')).filter((f) => f === '1014.json').length, 1);
  assert.equal(lockedUsers(), 0);
  // a different player is not held up by this one
  assert.equal(calls.length, 18);
});

test('nits: the page button wraps; Roll keeps the assignment when rounds exist and restores it after a method change; --who falls back to the saved Crawler name', async () => {
  const { dir, ctx, calls } = setup((r, id) => ARR[id]);
  const p = new Player(ctx, '1015', 'Oz');
  await toS8(p, 'Oz');
  await p.click('Roll'); await p.click('Keep A');
  assert.match(p.components().find((c) => c.label?.startsWith('More')).label, /page 1\/3/);
  for (let k = 0; k < 4; k++) await p.click('More');                       // 1 -> 2 -> 3 -> 1 -> 2
  assert.match(p.components().find((c) => c.label?.startsWith('More')).label, /page 2\/3/);
  await p.click('More'); await p.click('More');                            // back to page 1
  await assign(p, [15, 14, 13, 12, 12, 12]);
  const base = draftOf(dir, '1015').base;
  assert.ok(base);
  while (!p.find((c) => c.label === 'Roll')) await p.click('More');
  await p.click('Roll');                                                   // pressing Roll again keeps the finished assignment
  assert.deepEqual(draftOf(dir, '1015').base, base);
  await p.click('Standard array');
  assert.equal(draftOf(dir, '1015').base, null);
  await p.click('Roll');                                                   // coming back brings the saved assignment back
  assert.deepEqual(draftOf(dir, '1015').base, base);
  assert.equal(calls.length, 18);
  assert.equal(draftOf(dir, '1015').scoreRolls.who, 'Oz');
  // after Restart the draft has no name, but the rounds remember who rolled them
  await p.click('Restart'); await p.click('Yes, wipe my answers');
  const wiped = draftOf(dir, '1015');
  assert.equal(wiped.name, undefined);
  assert.equal(wiped.scoreRolls.who, 'Oz');
  const env = makeEnv(ctx, { ...wiped, uid: '1015', uname: 'oz-the-discord-name' });
  await env.rollRound({ uname: 'oz-the-discord-name', scoreRolls: wiped.scoreRolls }, 2);
  assert.equal(calls.at(-1).who, 'Oz');
});
