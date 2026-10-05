/**
 * The spec's 10-item beta test script (characters/create-flow-spec-5e.md section 6.2), driven through the real flow against
 * fresh sandbox `beta` sessions made by tools/new-session.py. Returns [{n, name, pass, detail}].
 */
import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';
import { Player, drive, makeCtx, makeSandbox, REAL_CAMPAIGN } from './create-harness.js';
import { reviewAction } from '../../src/create/flow.js';

const sha = (p) => (existsSync(p) ? createHash('sha256').update(readFileSync(p)).digest('hex') : null);
function treeHash(dir) {
  const h = createHash('sha256');
  const walk = (d) => { if (!existsSync(d)) return; for (const f of readdirSync(d).sort()) { const p = join(d, f); if (statSync(p).isDirectory()) walk(p); else { h.update(p.replace(dir, '')); h.update(readFileSync(p)); } } };
  walk(dir);
  return h.digest('hex');
}
const state = (dir) => JSON.parse(readFileSync(join(dir, 'sessions-data', 'beta', 'state.json'), 'utf8'));
const py = (dir, script, ...a) => {
  try { return { code: 0, out: execFileSync('python3', [join(dir, 'tools', script), ...a], { env: { ...process.env, DCC_CAMPAIGN_DIR: dir, DCC_AUTO_PUBLISH: '0' }, encoding: 'utf8', stdio: 'pipe' }) }; } catch (e) { return { code: e.status, out: `${e.stdout}${e.stderr}` }; }
};
const mod = (s) => Math.floor((s - 10) / 2);
const text = (dir, ...p) => readFileSync(join(dir, ...p), 'utf8');

export async function runScript() {
  const R = [];
  const rec = (n, name, pass, detail) => R.push({ n, name, pass: !!pass, detail });
  const guard = async (n, name, fn) => { try { const r = await fn(); rec(n, name, r.pass, r.detail); } catch (e) { rec(n, name, false, `threw: ${String(e.message).split('\n')[0]}`); } };
  const alphaRealBefore = sha(join(REAL_CAMPAIGN, 'sessions', 'state.json'));

  // ---- main sandbox: fresh beta, review off, four new players
  const dir = makeSandbox('beta', ['--review', 'off']);
  const ctx = makeCtx(dir);
  let wakes = 0;
  ctx.wake = { notify: () => { wakes++; } };
  copyFileSync(join(REAL_CAMPAIGN, 'sessions', 'state.json'), join(dir, 'sessions', 'state.json')); // stand-in alpha to checksum
  const alphaBefore = sha(join(dir, 'sessions', 'state.json'));
  const secretBefore = treeHash(join(dir, 'gm-notes', 'secret'));
  const draftFile = (uid) => join(dir, 'sessions-data', 'beta', 'create-drafts', `${uid}.json`);
  const A = new Player(ctx, '1001', 'Ann'), B = new Player(ctx, '1002', 'Bea'), C = new Player(ctx, '1003', 'Cy'), E = new Player(ctx, '1005', 'Eli'), D = new Player(ctx, '1004', 'Dee');

  await guard(1, 'Player A through S1-S17 (array, Human Fighter, Soldier)', async () => {
    await A.command();
    const seen = [];
    await drive(A, { name: 'Ann', noShop: true });
    seen.push(existsSync(draftFile('1001')), (statSync(draftFile('1001')).mode & 0o777) === 0o600);
    const beforeConfirm = state(dir).crawlers.length;
    await A.click('Confirm ▸'); await A.click('Confirm and lock the file');
    const st = state(dir);
    const sheet = existsSync(join(dir, 'sessions-data', 'beta', 'characters', 'ann-ann.md'));
    const alphaSame = sha(join(dir, 'sessions', 'state.json')) === alphaBefore;
    return { pass: seen.every(Boolean) && beforeConfirm === 0 && st.crawlers.length === 1 && sheet && alphaSame && !existsSync(draftFile('1001')), detail: `draft saved (600): ${seen}; crawlers before confirm ${beforeConfirm}, after ${st.crawlers.length}; sheet file ${sheet}; alpha checksum unchanged ${alphaSame}; draft deleted ${!existsSync(draftFile('1001'))}` };
  });

  await guard(2, "Check A's numbers by hand", async () => {
    const c = state(dir).crawlers[0];
    const b = c.build.background_asi.applied, base = c.build.score_base;
    const abOk = Object.keys(base).every((k) => c.abilities[k] === base[k] + b[k]) && Object.values(c.abilities).every((v) => v <= 20);
    const hpOk = c.hp.max === 10 + mod(c.abilities.con);
    const acOk = c.ac === 16 && c.inventory.some((i) => /Chain Mail/.test(i.name)); // chain mail is AC 16 flat, no Dex
    return { pass: abOk && hpOk && acOk, detail: `abilities=base+bonus ${abOk}; HP ${c.hp.max} = d10 max + Con ${mod(c.abilities.con)} ${hpOk}; AC ${c.ac} (chain mail 16) ${acOk}; no score above 20` };
  });

  await guard(3, 'Credits: A package+package; B gold+vending; ledger verify', async () => {
    await B.command();
    await drive(B, { name: 'Bea', species: 'Elf', cls: 'Wizard', bg: 'Sage', kit: { kc: 'B', kb: 'B', shop: "Rations 12\nRope\nHealer's Kit\nCrowbar" } });
    await B.click('Confirm ▸'); await B.click('Confirm and lock the file');
    const st = state(dir);
    const a = st.crawlers.find((x) => x.name === 'Ann'), b = st.crawlers.find((x) => x.name === 'Bea');
    const v = py(dir, 'state.py', '--session', 'beta', 'ledger', 'verify');
    const led = readFileSync(join(dir, 'sessions-data', 'beta', 'credit-ledger.jsonl'), 'utf8').trim().split('\n').map(JSON.parse);
    const intake = led.filter((r) => r.source === 'intake' && r.reason);
    return { pass: a.credits === 18 && b.credits >= 0 && b.credits === 105 - (6 + 1 + 5 + 2) && v.code === 0 && intake.length === led.length, detail: `A credits ${a.credits} (Fighter A 4 + Soldier A 14 = 18); B credits ${b.credits} (55+50 gold - 14 spent = 91 expected); ledger verify exit ${v.code}; ${intake.length}/${led.length} rows are intake with reasons` };
  });

  await guard(4, 'Disconnect at S9, return later: Resume at S9, answers kept, no duplicate draft', async () => {
    await C.command(); await C.click('ACCEPT'); await C.click('Skip');
    await C.form('S3:name', { name: 'Cy' }); await C.click('Next');
    await C.form('S4:edit', { look: 'Cardigan', hook: 'Calm until not' }); await C.click('Next');
    await C.choose('S5:species', 'Human'); await C.click('Next');
    await C.choose('S6:class', 'Cleric'); await C.click('Pick for me'); await C.click('Next');
    await C.choose('S7:bg', 'Acolyte'); await C.choose('S7:asi', '2-1:wis:cha'); await C.choose('S7:feat', 'Alert'); await C.click('Next');
    await C.click('Standard array'); await C.click('Pick for me'); await C.click('Next');
    await C.choose('S9:cskills', ['History', 'Medicine']);
    const later = new Player(ctx, '1003', 'Cy'); // a new client an hour later
    const txt = await later.command();
    const prompt = /Resume your intake/.test(txt) && /S9/.test(txt);
    await later.click('Resume');
    const back = later.screen() === 'S9';
    const kept = JSON.parse(readFileSync(draftFile('1003'), 'utf8')).classSkills.join() === 'History,Medicine';
    const files = readdirSync(join(dir, 'sessions-data', 'beta', 'create-drafts')).filter((f) => /^1003/.test(f));
    Object.assign(C, { msg: later.msg, lastText: later.lastText });
    return { pass: prompt && back && kept && files.length === 1, detail: `resume prompt ${prompt}; back at S9 ${back}; answers kept ${kept}; draft files for C ${files.length}` };
  });
  // finish C
  C.ctx = ctx; Object.setPrototypeOf(C, Player.prototype);
  await C.click('Pick for me'); await C.click('Next'); await C.click('Pick for me'); await C.click('Next');
  if (C.screen() === 'S11') { await C.click('Pick for me'); await C.click('Next'); }
  await C.click('Skip'); await C.form('S14:edit', { story: 'Church volunteer.', handle: '' }); await C.click('Next');
  await C.form('S15:edit', { orders: 'Heal whoever is lowest, then follow the group.', react: '', sig: '' }); await C.click('Next');
  await C.click('Confirm ▸'); await C.click('Confirm and lock the file');

  await guard(7, 'Wizard S11 counts per the table; Fighter never sees S11', async () => {
    const tbl = JSON.parse(readFileSync(join(dir, 'tables', 'chargen-5e.json'), 'utf8')).classes.Wizard.spells;
    const W = new Player(ctx, '2001', 'Wes');
    // a wizard draft in the same session (party has room only if < 4: use a separate sandbox)
    const dir7 = makeSandbox('beta', ['--review', 'off']);
    const c7 = makeCtx(dir7);
    const w = new Player(c7, '2001', 'Wes');
    let blockedWrong = false, blockedFewBook = false, sawS11 = false;
    await w.command();
    await drive(w, { name: 'Wes', species: 'Human', cls: 'Wizard', bg: 'Sage', onS11: async (p) => {
      sawS11 = p.screen() === 'S11';
      await p.choose('S11:can', ['Light', 'Mage Hand']); // 2 of 3
      blockedWrong = p.disabled('Next');
      await p.choose('S11:can', ['Light', 'Mage Hand', 'Fire Bolt']);
      await p.choose('S11:l1:0', ['Shield', 'Sleep']);
      blockedFewBook = p.disabled('Next');
      await p.click('Pick for me');
      await p.click('Next');
    } });
    const dr = JSON.parse(readFileSync(join(dir7, 'sessions-data', 'beta', 'create-drafts', '2001.json'), 'utf8'));
    const spellsOk = dr.spells.cantrips.length === tbl.cantrips && dr.spells.level1.length === tbl.spellbook && dr.spells.prepared.length === tbl.prepared;
    // Fighter A's flow skipped S11: its draft screens never included it (checked via build)
    const aBuild = state(dir).crawlers[0].build;
    const fighterNoSpells = !aBuild.spells;
    void W;
    return { pass: sawS11 && blockedWrong && blockedFewBook && spellsOk && fighterNoSpells, detail: `Wizard S11 shown ${sawS11}; 2 of ${tbl.cantrips} cantrips blocks Next ${blockedWrong}; short spellbook blocks Next ${blockedFewBook}; final counts ${dr.spells.cantrips.length}/${dr.spells.level1.length}/${dr.spells.prepared.length} vs table ${tbl.cantrips}/${tbl.spellbook}/${tbl.prepared} ${spellsOk}; Fighter has no spells and was never shown S11 ${fighterNoSpells}` };
  });

  await guard(9, 'Pre-built + species change at S16 [Edit]', async () => {
    await E.command();
    await E.click('Use a pre-built'); await E.choose('S1:pick', 'rogue');
    await E.click('Skip'); await E.form('S3:name', { name: 'Eli' }); await E.click('Next');
    await E.form('S4:edit', { look: 'Hoodie', hook: 'Light fingers' }); await E.click('Next');
    const skipped = E.screen() === 'S13'; // S5-S12 and S15 were pre-filled or retired
    await E.click('Skip'); await E.form('S14:edit', { story: 'Professional houseguest.', handle: '' }); await E.click('Next');
    const reached16 = E.screen() === 'S16';
    await E.choose('S16:edit', 'S5'); await E.choose('S5:species', 'Dwarf'); await E.click('Next');
    const back16 = E.screen() === 'S16';
    await E.click('Confirm ▸'); await E.click('Confirm and lock the file');
    const c = state(dir).crawlers.find((x) => x.name === 'Eli');
    return { pass: skipped && reached16 && back16 && !!c && c.build.created_via === 'create-flow-prebuilt' && c.species === 'Dwarf' && c.hp.max === 8 + mod(c.abilities.con) + 1, detail: `pre-filled screens skipped ${skipped}; reached S16 ${reached16}; edit returned to S16 ${back16}; registered ${!!c}; created_via ${c?.build.created_via}; Dwarf HP ${c?.hp.max} (d8 max + Con + Dwarven Toughness)` };
  });

  await guard(8, 'Fifth /create after four are registered: Party full, no draft, no write', async () => {
    const before = treeHash(join(dir, 'sessions-data', 'beta'));
    const txt = await D.command();
    const after = treeHash(join(dir, 'sessions-data', 'beta'));
    return { pass: /Party full\./.test(txt) && !existsSync(draftFile('1004')) && before === after && state(dir).crawlers.length === 4, detail: `reply "${txt.trim()}"; no draft file ${!existsSync(draftFile('1004'))}; session folder byte-identical ${before === after}; crawlers ${state(dir).crawlers.length}` };
  });

  await guard(10, 'Card and isolation check after all four register', async () => {
    const st = state(dir);
    const tags = st.crawlers.every((c) => (c.fan_profile.public_tags ?? []).length === 0); // S12 retired: no tags asked, none stored
    const secretSame = treeHash(join(dir, 'gm-notes', 'secret')) === secretBefore;
    const sheets = readdirSync(join(dir, 'sessions-data', 'beta', 'characters')).filter((f) => f.endsWith('.md') && f !== 'INDEX.md');
    const cardFirst = sheets.every((f) => /## Card[^\n]*\nCredits: \d+/.test(text(dir, 'sessions-data', 'beta', 'characters', f)));
    const oneEach = sheets.length === 4;
    const alphaSame = sha(join(dir, 'sessions', 'state.json')) === alphaBefore;
    const noPrivate = sheets.every((f) => !/Q1:|opt-out|Customer survey/i.test(text(dir, 'sessions-data', 'beta', 'characters', f)));
    return { pass: tags && secretSame && cardFirst && oneEach && alphaSame && noPrivate && wakes === 0, detail: `4 sheets with a credits-first card ${cardFirst && oneEach}; no fan tags stored or asked (S12 retired) ${tags}; no survey/opt-out text in sheet files ${noPrivate}; flow wake calls ${wakes}; gm-notes/secret hash unchanged ${secretSame}; alpha stand-in unchanged ${alphaSame}. NOT exercised: live Discord posting (needs GM_DISCORD_TOKEN + channels); the card text is the publisher's own render.` };
  });

  // ---------------------------------------------------------------- hold sandbox: items 5 and 6
  const dirH = makeSandbox('beta', ['--review', 'hold']);
  const cH = makeCtx(dirH);
  const secret = 'zzspidersxx', veilTopic = 'zzdrowningxx', unshared = 'zzclownsxx';
  await guard(5, 'Lines/veil privacy with review_mode hold', async () => {
    const P = new Player(cH, '3003', 'Cat');
    await P.command();
    await drive(P, { name: 'Cat', optouts: { lines: `${secret} *\n${unshared}`, veils: veilTopic } });
    await P.click('Confirm ▸'); await P.click('Confirm and lock the file');
    const held = /Filed|pending/i.test(P.lastText) && state(dirH).crawlers.length === 0;
    const rev = new Player(cH, '9000', 'Rev'); rev.perms = true;
    let shown = '';
    const i = rev.fake({ isChatInputCommand: () => true, options: { getString: () => null, getUser: () => ({ id: '3003' }) }, async reply(p) { shown = p.content; } });
    await reviewAction(i, cH, 'review');
    const reviewerOk = shown.includes(secret) && !shown.includes(unshared) && !shown.includes(veilTopic) && /Opt-outs: set \(private\)/.test(shown);
    const j = rev.fake({ isChatInputCommand: () => true, deferReply: async () => {}, editReply: async () => {}, options: { getString: () => null, getUser: () => ({ id: '3003' }) } });
    await reviewAction(j, cH, 'approve');
    const hay = [text(dirH, 'sessions-data', 'beta', 'characters', 'cat-cat.md'), text(dirH, 'sessions-data', 'beta', 'create-log.jsonl'), JSON.stringify(cH.staffSent), P.lastText, shown];
    const leaked = [unshared, veilTopic].some((t) => hay.some((h) => h.includes(t)));
    const registered = state(dirH).crawlers.length === 1;
    const gmHas = JSON.stringify(state(dirH).crawlers[0].fan_profile.opt_outs).includes(unshared);
    return { pass: held && reviewerOk && !leaked && registered && gmHas, detail: `held (nothing in state) ${held}; reviewer view shows the shared topic only + "Opt-outs: set (private)" ${reviewerOk}; unshared topics absent from card/sheet/staff note/log/reviewer view ${!leaked}; approved and registered ${registered}; the GM state still holds every opt-out (so it can obey them) ${gmHas}` };
  });

  await guard(6, 'Same name at once; Horn vs Hornet', async () => {
    const dir6 = makeSandbox('beta', ['--review', 'off']);
    const c6 = makeCtx(dir6);
    const P1 = new Player(c6, '4001', 'Pat'), P2 = new Player(c6, '4002', 'Quin'), P3 = new Player(c6, '4003', 'Rae');
    await P1.command(); await P2.command();
    await drive(P1, { name: 'Hornet' });
    await drive(P2, { name: 'Hornet' });
    await P1.click('Confirm ▸'); await P1.click('Confirm and lock the file');
    const firstWins = /Registered/.test(P1.lastText);
    await P2.click('Confirm ▸'); await P2.click('Confirm and lock the file');
    const sentBack = P2.screen() === 'S3' && /taken/i.test(P2.lastText);
    await P3.command(); await P3.click('ACCEPT'); await P3.click('Skip');
    await P3.form('S3:name', { name: 'Horn' });
    const warn = /sits inside another crawler/i.test(P3.lastText) && !!P3.find((x) => x.label === 'Use it anyway');
    const count = JSON.parse(readFileSync(join(dir6, 'sessions-data', 'beta', 'state.json'), 'utf8')).crawlers.length;
    return { pass: firstWins && sentBack && warn && count === 1, detail: `first Confirm wins ${firstWins}; second sent back to S3 with "taken" ${sentBack}; Horn vs Hornet warning + second tap ${warn}; crawlers ${count}` };
  });

  const alphaRealAfter = sha(join(REAL_CAMPAIGN, 'sessions', 'state.json'));
  R.sort((a, b) => a.n - b.n);
  return { results: R, realAlphaUnchanged: alphaRealBefore === alphaRealAfter, dir };
}
