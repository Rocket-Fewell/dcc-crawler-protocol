// "Cancel build": an exit on every /create screen. Asks once, hard-deletes the uncommitted draft (rolled rounds too), works on stale messages, takes the per-user lock.
import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import test from 'node:test';
import { defaultRun } from '../src/create/commit.js';
import { CANCELLED_TEXT, CLEARED_TEXT } from '../src/create/flow.js';
import { Player, drive, makeCtx, makeSandbox } from './helpers/create-harness.js';

const draftFile = (dir, uid) => join(dir, 'sessions-data', 'beta', 'create-drafts', `${uid}.json`);
const stateFile = (dir) => join(dir, 'sessions-data', 'beta', 'state.json');
const logLines = (dir) => { try { return readFileSync(join(dir, 'sessions-data', 'beta', 'create-log.jsonl'), 'utf8').trim().split('\n').map((l) => JSON.parse(l)); } catch { return []; } };

/** roll.py answers a keepable 15 every time (6+6+3, drop the 1); everything else is real */
const fakeRoll = async (cmd, args, opts) => {
  if (!String(args[0]).endsWith('roll.py')) return defaultRun(cmd, args, opts);
  return { ok: true, stdout: JSON.stringify({ terms: [{ rolls: [6, 6, 3, 1] }], total: 15 }), stderr: '' };
};

/** a Player that records, for every message shown, whether it has a Cancel build exit and respects Discord's 5x5 limit */
class Watcher extends Player {
  seen = new Map();   // screen -> {cancel, rows, maxRow}
  capture(p) {
    super.capture(p);
    if (!p.components?.length) return;
    const rows = p.components.map((r) => (r.toJSON ? r.toJSON() : r).components);
    const labels = rows.flat().map((c) => c.label);
    const scr = this.screen() ?? (/Trash everything/.test(this.lastText) ? 'confirm-cancel' : 'other');
    const exit = labels.includes('Cancel build') || labels.includes('Got it') || labels.includes('Yes, trash it') || labels.includes('Cancel');
    assert.ok(rows.length <= 5 && rows.every((r) => r.length <= 5), `Discord limit on ${scr}`);
    const prev = this.seen.get(scr) ?? { cancel: true };
    this.seen.set(scr, { cancel: prev.cancel && exit, direct: labels.includes('Cancel build') });
  }
}

test('Cancel build is on the Roll screen (before and after rolling) and on the assign screens', async () => {
  const dir = makeSandbox('beta');
  const p = new Watcher(makeCtx(dir, 'beta', { create: { run: fakeRoll } }), '2001', 'Ann');
  await p.command();
  await drive(p, { name: 'Ann', onS8: async (q) => {
    assert.ok(q.find((c) => c.label === 'Cancel build'), 'S8 method picker');
    await q.click('Roll');
    assert.ok(q.find((c) => c.label === 'Cancel build'), 'after rolling');
    await q.click('Keep A');
    assert.ok(q.find((c) => c.label === 'Cancel build'), 'assign');
    for (const k of ['str', 'dex', 'con', 'int', 'wis', 'cha']) {
      for (let g = 0; g < 4 && !q.byKey(`S8:assign:${k}`); g++) { assert.ok(q.find((c) => c.label === 'Cancel build'), 'assign page'); await q.click('More'); }
      const m = q.byKey(`S8:assign:${k}`); await q.choose(`S8:assign:${k}`, m.options[0].value);
    }
  } });
  for (const [scr, v] of p.seen) assert.ok(v.cancel, `${scr} has an exit`);
});

test('Cancel build is on every screen of a full walk-through, including the review screens', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  const p = new Watcher(makeCtx(dir), '2002', 'Bea');
  await p.command();
  await drive(p, { name: 'Bea', noShop: true });
  for (const s of ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S13', 'S14', 'S15', 'S16']) assert.ok(p.seen.get(s)?.direct, `${s} has Cancel build`);
  assert.equal(p.screen(), 'S16');
  assert.ok(p.find((c) => c.label === 'Cancel build'), 'the review screen has it');
  // pickers: S8 point buy / standard array, S10 shopping, paged screens
  assert.ok([...p.seen.values()].every((v) => v.cancel));
});

test('Cancel build: asks "Trash everything?" once; No returns to the same screen; Yes hard-deletes the draft and says so', async () => {
  const dir = makeSandbox('beta');
  const p = new Watcher(makeCtx(dir, 'beta', { create: { run: fakeRoll } }), '2003', 'Cy');
  await p.command();
  await p.click('ACCEPT'); await p.click('Skip');
  assert.equal(p.screen(), 'S3');
  await p.click('Cancel build');
  assert.match(p.lastText, /Trash everything\?/);
  assert.deepEqual(p.components().map((c) => c.label), ['Yes, trash it', 'No, keep going']);
  assert.ok(existsSync(draftFile(dir, '2003')), 'nothing deleted before the yes');
  await p.click('No, keep going');
  assert.equal(p.screen(), 'S3');
  assert.ok(!/Trash everything/.test(p.lastText));
  assert.equal(JSON.parse(readFileSync(draftFile(dir, '2003'), 'utf8')).confirmCancel, false);
  await p.click('Cancel build');
  await p.click('Yes, trash it');
  assert.equal(p.lastText, CANCELLED_TEXT);
  assert.equal(CANCELLED_TEXT, 'Build cancelled. Run /create to start fresh.');
  assert.deepEqual(p.components(), []);
  assert.ok(!existsSync(draftFile(dir, '2003')));
  assert.ok(!readdirSync(join(dir, 'sessions-data', 'beta', 'create-drafts')).some((f) => f.startsWith('2003')));
  const ev = logLines(dir).find((e) => e.event === 'build_cancelled');
  assert.ok(ev && ev.uid === '2003' && ev.screen === 'S3', 'staff log has the event');
  assert.ok(!JSON.stringify(ev).includes('Cy'), 'the log holds no content');
});

test('Cancel build deletes rolled rounds too; a fresh /create starts at S1 with a fresh roll (no kept rolls)', async () => {
  const dir = makeSandbox('beta');
  const ctx = makeCtx(dir, 'beta', { create: { run: fakeRoll } });
  const p = new Player(ctx, '2004', 'Di');
  await p.command(); await p.click('ACCEPT'); await p.click('Skip');
  await p.form('S3:name', { name: 'Di' }); await p.click('Next');
  await p.form('S4:edit', { look: 'a', hook: 'b' }); await p.click('Next');
  await p.choose('S5:species', 'Human'); await p.click('Next');
  await p.choose('S6:class', 'Fighter'); if (p.components().some((c) => c.custom_id?.includes('S6:choice'))) await p.click('Pick for me'); await p.click('Next');
  await p.choose('S7:bg', 'Soldier'); await p.choose('S7:asi', p.byKey('S7:asi').options[0].value);
  if (p.byKey('S7:feat')) await p.choose('S7:feat', p.byKey('S7:feat').options[0].value);
  await p.click('Next');
  await p.click('Roll');
  assert.ok(JSON.parse(readFileSync(draftFile(dir, '2004'), 'utf8')).scoreRolls.rounds.length >= 1, 'rolls were saved');
  await p.click('Cancel build'); await p.click('Yes, trash it');
  assert.ok(!existsSync(draftFile(dir, '2004')));
  await p.command();
  assert.equal(p.screen(), 'S1');
  assert.ok(!JSON.parse(readFileSync(draftFile(dir, '2004'), 'utf8')).scoreRolls);
});

test('Cancel build works from a stale message, and a missing draft just says it is cleared', async () => {
  const dir = makeSandbox('beta');
  const p = new Watcher(makeCtx(dir), '2005', 'Eve');
  await p.command(); await p.click('ACCEPT');                      // now on S2
  const staleCancel = p.find((c) => c.label === 'Cancel build').custom_id;
  await p.click('Skip');                                            // S3; the old message is now stale
  const press = async (id) => { const { handleInteraction } = await import('../src/commands/index.js'); await handleInteraction(p.fake({ isButton: () => true, isMessageComponent: () => true, customId: id }), p.ctx); };
  await press(staleCancel);
  assert.match(p.lastText, /Trash everything\?/);
  const yes = p.find((c) => c.label === 'Yes, trash it').custom_id;
  const no = p.find((c) => c.label === 'No, keep going').custom_id;
  await press(yes);
  assert.equal(p.lastText, CANCELLED_TEXT);
  assert.ok(!existsSync(draftFile(dir, '2005')));
  // the same buttons again, on a draft that no longer exists
  await press(staleCancel);
  assert.equal(p.lastText, CLEARED_TEXT);
  await press(yes);
  assert.equal(p.lastText, CLEARED_TEXT);
  await press(no);
  assert.equal(p.lastText, CLEARED_TEXT);
});

test('Cancel build is not blocked by an open session', async () => {
  const dir = makeSandbox('beta');
  const p = new Player(makeCtx(dir), '2006', 'Flo');
  await p.command(); await p.click('ACCEPT');
  writeFileSync(join(dir, 'sessions-data', 'beta', 'session-status.json'), JSON.stringify({ status: 'open' }));
  await p.click('Cancel build'); await p.click('Yes, trash it');
  assert.equal(p.lastText, CANCELLED_TEXT);
  assert.ok(!existsSync(draftFile(dir, '2006')));
});

test('Cancel build takes the per-user lock: presses queue behind a slow Roll, and a double Yes is safe', async () => {
  const dir = makeSandbox('beta');
  let release;
  const gate = new Promise((r) => { release = r; });
  const slow = async (cmd, args, opts) => { if (String(args[0]).endsWith('roll.py')) await gate; return fakeRoll(cmd, args, opts); };
  const p = new Player(makeCtx(dir, 'beta', { create: { run: slow } }), '2007', 'Gus');
  await p.command(); await p.click('ACCEPT'); await p.click('Skip');
  await p.form('S3:name', { name: 'Gus' }); await p.click('Next');
  await p.form('S4:edit', { look: 'a', hook: 'b' }); await p.click('Next');
  await p.choose('S5:species', 'Human'); await p.click('Next');
  await p.choose('S6:class', 'Fighter'); if (p.components().some((c) => c.custom_id?.includes('S6:choice'))) await p.click('Pick for me'); await p.click('Next');
  await p.choose('S7:bg', 'Soldier'); await p.choose('S7:asi', p.byKey('S7:asi').options[0].value);
  if (p.byKey('S7:feat')) await p.choose('S7:feat', p.byKey('S7:feat').options[0].value);
  await p.click('Next');
  const { handleInteraction } = await import('../src/commands/index.js');
  const cancelId = p.find((c) => c.label === 'Cancel build').custom_id;
  const rolling = p.click('Roll');                                  // holds the lock while the dice are out
  await new Promise((r) => setTimeout(r, 30));
  const q = new Player(p.ctx, '2007', 'Gus');
  const waiting = handleInteraction(q.fake({ isButton: () => true, isMessageComponent: () => true, customId: cancelId }), q.ctx);
  await new Promise((r) => setTimeout(r, 30));
  assert.equal(q.lastText, '', 'cancel waits for the roll to finish');
  release(); await rolling; await waiting;
  assert.match(q.lastText, /Trash everything\?/, 'it saw the finished roll, then asked');
  const yes = q.find((c) => c.label === 'Yes, trash it').custom_id;
  await Promise.all([1, 2].map(() => handleInteraction(q.fake({ isButton: () => true, isMessageComponent: () => true, customId: yes }), q.ctx)));
  assert.ok(!existsSync(draftFile(dir, '2007')));
  assert.equal(logLines(dir).filter((e) => e.event === 'build_cancelled').length, 1, 'cancelled once, second press found nothing');
});

test('Cancel build is on the Resume prompt and on the held-for-review reply', async () => {
  const dir = makeSandbox('beta');
  const p = new Player(makeCtx(dir), '2008', 'Hal');
  await p.command(); await p.click('ACCEPT');
  await p.command();
  assert.match(p.lastText, /Resume your intake/);
  assert.ok(p.find((c) => c.label === 'Cancel build'), 'resume prompt has Cancel build');
  const f = draftFile(dir, '2008');
  writeFileSync(f, JSON.stringify({ ...JSON.parse(readFileSync(f, 'utf8')), status: 'awaiting_review' }));
  await p.command();
  assert.ok(p.find((c) => c.label === 'Cancel build'), 'held reply has Cancel build');
  await p.click('Cancel build'); await p.click('Yes, trash it');
  assert.ok(!existsSync(f));
});

test('a committed Crawler is untouched: state.json and its draft survive, and Cancel build is refused', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  const q = new Player(makeCtx(dir), '2009', 'Ivy');
  await q.command();
  await drive(q, { name: 'Ivy', noShop: true });
  await q.click('Confirm ▸'); await q.click('Confirm and lock the file');
  const st1 = readFileSync(stateFile(dir), 'utf8');
  assert.match(st1, /Ivy/);
  const f = draftFile(dir, '2009');
  // a leftover draft file marked as already written to state (as after a crash between steps)
  writeFileSync(f, JSON.stringify({ ...(existsSync(f) ? JSON.parse(readFileSync(f, 'utf8')) : { uid: '2009', screen: 'S16' }), uid: '2009', status: 'state_written' }));
  const { handleInteraction } = await import('../src/commands/index.js');
  const press = (id) => handleInteraction(q.fake({ isButton: () => true, isMessageComponent: () => true, customId: id }), q.ctx);
  await press('create:2009:nav:cancel');
  assert.match(q.lastText, /already registered/);
  assert.ok(!/Trash everything/.test(q.lastText));
  await press('create:2009:nav:cancel_yes');                       // even a forged Yes does nothing
  assert.match(q.lastText, /already registered/);
  assert.ok(existsSync(f), 'draft not deleted');
  assert.equal(readFileSync(stateFile(dir), 'utf8'), st1, 'state.json untouched');
  assert.equal(logLines(dir).filter((e) => e.event === 'build_cancelled').length, 0);
});
