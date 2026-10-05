import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { handleInteraction } from '../src/commands/index.js';
import { headerRows } from '../src/create/commit.js';
import { loadTables } from '../src/create/data.js';
import * as K from '../src/create/reskin.js';
import * as R from '../src/create/rules.js';
import { findPurchase, surveyQuestions } from '../src/create/screens.js';
import { toSpec } from '../src/create/files.js';
import { REAL_CAMPAIGN, Player, drive, finish, makeCtx, makeSandbox } from './helpers/create-harness.js';

const stateOf = (dir) => JSON.parse(readFileSync(join(dir, 'sessions-data', 'beta', 'state.json'), 'utf8'));
const py = (dir, ...a) => {
  try { return { code: 0, out: execFileSync('python3', [join(dir, 'tools', 'state.py'), '--session', 'beta', ...a], { env: { ...process.env, DCC_CAMPAIGN_DIR: dir, DCC_AUTO_PUBLISH: '0' }, encoding: 'utf8', stdio: 'pipe' }) }; } catch (e) { return { code: e.status, out: `${e.stdout}${e.stderr}` }; }
};
const t = loadTables(REAL_CAMPAIGN);

/** Two registered Crawlers for one player (first active, second benched) and a second player, in a fresh beta sandbox. */
async function setup() {
  const dir = makeSandbox('beta', ['--review', 'off']);
  const ctx = makeCtx(dir);
  const ann = new Player(ctx, '1001', 'Ann');
  await ann.command();
  await drive(ann, { name: 'Annie', noShop: true });
  await finish(ann);
  const bea = new Player(ctx, '1002', 'Bea');
  await bea.command();
  await drive(bea, { name: 'Beatrix', noShop: true });
  await finish(bea);
  return { dir, ctx, ann, bea };
}

const slash = (p, name, opts = {}, extra = {}) => p.fake({ isChatInputCommand: () => true, commandName: name, options: { getString: (k) => opts[k] ?? null, getUser: () => null, getFocused: () => opts.focused ?? '' }, ...extra });

// ---------------------------------------------------------------- multi-Crawler create
test('a player\'s 2nd /create makes a BENCHED Crawler filed under the same player; the 1st stays active; the party shows one slot', async () => {
  const { dir, ctx, ann } = await setup();
  assert.equal(stateOf(dir).crawlers[0].status, 'active');
  const txt = await ann.command();
  assert.doesNotMatch(txt, /already (have|has|made|registered)? ?a crawler|can only/i);   // the old "already" refusal is gone
  assert.match(txt, /S1/);
  assert.match(ann.lastText, /starts \*\*BENCHED\*\*/);
  await drive(ann, { name: 'Annie Two', noShop: true, cls: 'Wizard', bg: 'Sage' });
  const out = await finish(ann);
  assert.match(out, /BENCHED/);
  const st = stateOf(dir);
  const [a1, a2] = st.crawlers.filter((c) => c.build.discord_user_id === '1001');
  assert.equal(a1.status, 'active');
  assert.equal(a2.status, 'benched');
  assert.equal(a2.player, a1.player);
  const party = JSON.parse(py(dir, 'party', '--json').out);
  assert.equal(party.encounter_count, 2);          // Annie + Beatrix; the benched one takes no slot
  assert.equal(py(dir, 'validate').code, 0);
  assert.equal(py(dir, 'ledger', 'verify').code, 0);
  void ctx;
});

test('a duplicate name is still refused (also across players); a different name for the same player passes', async () => {
  const { ann, bea } = await setup();
  await ann.command();
  await drive(ann, { name: 'Annie', noShop: true }).catch(() => {});
  assert.notEqual(ann.screen(), 'S16');            // stopped at S3: taken
  await bea.command();
  await drive(bea, { name: 'annie', noShop: true }).catch(() => {});
  assert.notEqual(bea.screen(), 'S16');
});

test('a fifth player\'s first /create still gets Party full; an existing player is never blocked by it', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  const ctx = makeCtx(dir);
  for (const [id, nm] of [['1', 'Aa'], ['2', 'Bb'], ['3', 'Cc'], ['4', 'Dd']]) { const p = new Player(ctx, id, nm); await p.command(); await drive(p, { name: `${nm}x`, noShop: true }); await finish(p); }
  const e = new Player(ctx, '5', 'Ee');
  assert.match(await e.command(), /full/i);
  const a = new Player(ctx, '1', 'Aa');
  await a.command();
  assert.match(a.screen() ?? '', /S1/);            // existing player may start another (benched) Crawler
});

// ---------------------------------------------------------------- /crawlers
test('/crawlers lists only the caller\'s Crawlers with active/benched and requests a swap without changing state', async () => {
  const { dir, ctx, ann, bea } = await setup();
  await ann.command(); await drive(ann, { name: 'Annie Two', noShop: true }); await finish(ann);
  await handleInteraction(slash(ann, 'crawlers'), ctx);
  assert.match(ann.lastText, /ACTIVE\*\* · \*\*Annie\*\*/);
  assert.match(ann.lastText, /benched · \*\*Annie Two\*\*/);
  assert.doesNotMatch(ann.lastText, /Beatrix/);
  const before = readFileSync(join(dir, 'sessions-data', 'beta', 'state.json'), 'utf8');
  const sel = ann.msg.components[0].toJSON().components[0];
  assert.match(sel.custom_id, /^crawlers:1001:swap$/);
  await handleInteraction(ann.fake({ isStringSelectMenu: () => true, isMessageComponent: () => true, customId: sel.custom_id, values: ['Annie Two'] }), ctx);
  assert.match(ann.lastText + JSON.stringify(ann.msg ?? ''), /./);
  assert.equal(readFileSync(join(dir, 'sessions-data', 'beta', 'state.json'), 'utf8'), before);   // a request never changes a Crawler
  assert.ok(existsSync(join(dir, 'sessions-data', 'beta', 'swap-requests.jsonl')));
  // another player cannot use ann's menu
  const stolen = bea.fake({ isStringSelectMenu: () => true, isMessageComponent: () => true, customId: sel.custom_id, values: ['Annie Two'] });
  let replied;
  stolen.reply = async (p) => { replied = p; };
  await handleInteraction(stolen, ctx);
  assert.match(replied.content, /not your list/);
});

test('/crawlers swap request is refused with a plain message while a session is open (even for a benched Crawler)', async () => {
  const { dir, ctx, ann } = await setup();
  await ann.command(); await drive(ann, { name: 'Annie Two', noShop: true }); await finish(ann);
  assert.equal(py(dir, 'session-status', 'open').code, 0);
  let replied;
  const i = ann.fake({ isStringSelectMenu: () => true, isMessageComponent: () => true, customId: 'crawlers:1001:swap', values: ['Annie Two'] });
  i.reply = async (p) => { replied = p; };
  await handleInteraction(i, ctx);
  assert.match(replied.content, /No swap while a session is open/);
  assert.equal(py(dir, 'crawler', 'activate', 'Annie Two', '--reason', 'x').code, 1);   // the GM command is refused too
  assert.equal(stateOf(dir).crawlers.find((c) => c.name === 'Annie').status, 'active');
});

// ---------------------------------------------------------------- /delete
test('/delete: autocomplete shows only the caller\'s Crawlers; another player\'s Crawler is refused; cancel is the default', async () => {
  const { dir, ctx, ann, bea } = await setup();
  let choices;
  await handleInteraction(slash(ann, 'delete', { focused: '' }, { isChatInputCommand: () => false, isAutocomplete: () => true, respond: async (c) => { choices = c; } }), ctx);
  assert.deepEqual(choices.map((c) => c.value), ['Annie']);
  let replied;
  const i = slash(ann, 'delete', { name: 'Beatrix' });
  i.reply = async (p) => { replied = p; };
  await handleInteraction(i, ctx);
  assert.match(replied.content, /not one of your Crawlers/);
  assert.equal(stateOf(dir).crawlers.length, 2);
  void bea;
});

test('/delete needs the typed name: a button alone does nothing, a wrong name deletes nothing, the exact name deletes and the ledger still verifies', async () => {
  const { dir, ctx, ann } = await setup();
  await ann.command(); await drive(ann, { name: 'Annie Two', noShop: true }); await finish(ann);
  let replied;
  const i = slash(ann, 'delete', { name: 'Annie Two' });
  i.reply = async (p) => { replied = p; };
  await handleInteraction(i, ctx);
  assert.match(replied.content, /Nothing is refunded/);
  const [cancel, ask] = replied.components[0].toJSON().components;
  assert.match(cancel.label, /Cancel/);
  // cancel button
  let updated;
  const c = ann.fake({ isButton: () => true, customId: cancel.custom_id });
  c.update = async (p) => { updated = p; };
  await handleInteraction(c, ctx);
  assert.match(updated.content, /not deleted/);
  assert.equal(stateOf(dir).crawlers.length, 3);
  // ask opens a modal; wrong name
  let modal;
  const a = ann.fake({ isButton: () => true, customId: ask.custom_id });
  a.showModal = async (m) => { modal = m; };
  await handleInteraction(a, ctx);
  const confirmId = modal.toJSON().custom_id;
  const submit = (typed) => {
    let out;
    const m = ann.fake({ isModalSubmit: () => true, customId: confirmId, fields: { getTextInputValue: () => typed } });
    m.deferReply = async () => {};
    m.editReply = async (p) => { out = p; };
    return handleInteraction(m, ctx).then(() => out);
  };
  assert.match((await submit('annie two')).content, /did not match/);
  assert.equal(stateOf(dir).crawlers.length, 3);
  assert.match((await submit('Annie Two')).content, /Deleted \*\*Annie Two\*\*/);
  assert.deepEqual(stateOf(dir).crawlers.map((x) => x.name), ['Annie', 'Beatrix']);
  assert.equal(py(dir, 'ledger', 'verify').code, 0);
  assert.equal(py(dir, 'validate').code, 0);
  const log = readFileSync(join(dir, 'sessions-data', 'beta', 'delete-log.jsonl'), 'utf8');
  assert.match(log, /"crawler":"Annie Two"/);
  assert.match(log, /"by":"1001"/);
});

test('/delete refuses the ACTIVE Crawler while a session is open (state.py enforces it); a benched one is fine', async () => {
  const { dir, ctx, ann } = await setup();
  await ann.command(); await drive(ann, { name: 'Annie Two', noShop: true }); await finish(ann);
  py(dir, 'session-status', 'open');
  const confirm = async (name) => {
    let out;
    const m = ann.fake({ isModalSubmit: () => true, customId: `delete:1001:confirm:${Buffer.from(name).toString('base64url')}`, fields: { getTextInputValue: () => name } });
    m.deferReply = async () => {}; m.editReply = async (p) => { out = p; };
    await handleInteraction(m, ctx);
    return out.content;
  };
  assert.match(await confirm('Annie'), /ACTIVE Crawler/);
  assert.equal(stateOf(dir).crawlers.length, 3);
  assert.match(await confirm('Annie Two'), /Deleted/);
});

test('/join and /leave record the session status (best effort); a failing tool never breaks them', async () => {
  const calls = [];
  const ctx = { config: { discord: { guildId: 'G1' }, campaign: { dir: '/x', sessionId: 'beta', dataDir: '/x/d' }, create: { python: 'python3' } }, logger: { warn() {}, error() {}, info() {} }, create: { run: async (cmd, args) => { calls.push(args.slice(3)); return { ok: false, stderr: 'boom' }; } }, session: { leave: () => true }, queue: { clear() {} } };
  const { markSession } = await import('../src/create/manage.js');
  await markSession(ctx, 'open');
  await markSession(ctx, 'close');
  assert.deepEqual(calls.map((c) => c.slice(0, 2)), [['session-status', 'open'], ['session-status', 'close']]);
});

// ---------------------------------------------------------------- item reskins, variants, headers
test('every chargen item has an srd_id that resolves in item-reskins; no price mismatch; names are never blank', () => {
  const unmapped = [];
  for (const [key, it] of Object.entries(t.chargen.items)) {
    const srd = K.itemSrdId(t, key);
    if (!srd || !K.entryFor(t, srd)) unmapped.push(key);
    assert.ok(K.labelFor(t, srd, it.name).trim().length > 0, key);
    if (!K.isHeaderKey(t, key)) assert.equal(K.priceCp(t, srd, key), it.cost_cp, `${key} price must equal the reskin base_price_cp`);
  }
  assert.deepEqual(unmapped, []);
  for (const key of Object.keys(t.chargen.items).filter((k) => K.isHeaderKey(t, k))) {
    const ids = K.variantIds(t, key);
    assert.ok(ids.length > 0, key);
    for (const v of ids) { assert.ok(K.entryFor(t, v), v); assert.ok(Number.isInteger(K.priceCp(t, v)), `${v} priced from its own base_price_cp`); assert.ok(!K.isHeaderId(t, v)); }
    assert.equal(K.priceCp(t, K.itemSrdId(t, key), key), null, 'a header is never priced');   // the placeholder cost_cp is ignored
  }
});

test('the fallback is never blank: unknown id, missing table, entry without names', () => {
  assert.equal(K.labelFor(t, 'no-such-id', 'Plain Name'), 'Plain Name');
  assert.equal(K.labelFor(t, 'no-such-id'), 'no such id');
  assert.equal(K.labelFor(t, undefined, ''), 'Unnamed item');
  const noTable = { ...t, reskins: K.buildReskinIndex(null) };
  assert.equal(R.itemLabel('rope', noTable), t.chargen.items.rope.name);
  for (const key of Object.keys(t.chargen.items)) assert.ok(R.itemLabel(key, noTable).trim() && R.itemLabel(key, t).trim(), key);
  const legacyOnly = { ...t, reskins: K.buildReskinIndex({ entries: [{ srd_id: 'rope', srd_name: '', combined_label: '', legacy_names: ['Old Cord'] }] }) };
  assert.equal(K.labelFor(legacyOnly, 'rope', 'Rope'), 'Old Cord');
  // the old junk field is never read
  const poisoned = { ...t, chargen: JSON.parse(JSON.stringify(t.chargen)) };
  poisoned.chargen.items.rope.junk = 'JUNK-NAME';
  assert.doesNotMatch(R.itemLabel('rope', poisoned), /JUNK-NAME/);
});

test('combined_label is shown, with the variant\'s own label for a header', () => {
  const d = { class: 'Cleric', background: 'Acolyte', kitClass: 'A', kitBg: 'A', cart: [], variants: { 'class:holy_symbol': 'holy-symbol-amulet', 'background:holy_symbol': 'holy-symbol-reliquary' } };
  const rows = R.inventoryRows(d, t);
  const syms = rows.filter((r) => r.chargen_key === 'holy_symbol');
  assert.deepEqual(syms.map((r) => r.srd_id).sort(), ['holy-symbol-amulet', 'holy-symbol-reliquary']);
  assert.match(syms.find((r) => r.srd_id === 'holy-symbol-amulet').name, /Gas-Station Saint Medal \(/);
  assert.ok(rows.every((r) => r.name === 'Intake Bag' || r.srd_id));
  assert.equal(headerRows(rows, t).length, 0);
});

test('a header never reaches the sheet: unresolved headers are skipped, validation blocks, the commit guard catches a stray header row', () => {
  const d = { class: 'Cleric', background: 'Acolyte', kitClass: 'A', kitBg: 'A', cart: [], uid: '1', uname: 'X' };
  const rows = R.inventoryRows(d, t);
  assert.ok(!rows.some((r) => /holy/i.test(r.chargen_key ?? '')));
  assert.ok(rows.every((r) => !K.isHeaderId(t, r.srd_id ?? 'x')));
  const full = { ...d, species: 'Human', asi: { type: '2-1', plus2: 'int', plus1: 'wis' }, method: 'array', base: { str: 8, dex: 12, con: 14, int: 10, wis: 15, cha: 13 } };
  assert.ok(R.validateDraft(full, t).some((e) => e.screen === 'S10' && /Pick which one/.test(e.msg)));
  assert.deepEqual(headerRows([{ name: 'Holy Symbol', srd_id: 'holy-symbol' }, { name: 'Mystery' }, { name: 'Intake Bag' }], t), ['Holy Symbol', 'Mystery']);
  assert.throws(() => R.cartLineCost({ id: 'holy_symbol', qty: 1 }, t), /pick a variant/);
  assert.throws(() => R.cartLineCost({ id: 'gaming_set', qty: 1, variant: null }, t), /pick a variant/);
  assert.throws(() => R.cartLineCost({ id: 'gaming_set', qty: 1, variant: 'holy-symbol-amulet' }, t), /pick a variant|cannot price/);   // a variant of another header is not a gaming set
});

test('Vending Wall: typing a variant buys it at the variant\'s own price; typing only the generic buys nothing; floor multiplier applies to vending only', () => {
  assert.deepEqual(findPurchase('lute', t), { id: 'musical_instrument', variant: 'lute' });
  assert.deepEqual(findPurchase('Ukulele With Pretensions', t), { id: 'musical_instrument', variant: 'lute' });
  assert.deepEqual(findPurchase('rope', t), { id: 'rope' });
  assert.equal(findPurchase('musical instrument', t).header, 'musical_instrument');
  const d = { class: 'Fighter', background: 'Soldier', kitClass: 'A', kitBg: 'A', cart: [{ id: 'musical_instrument', qty: 1, variant: 'lute' }] };
  assert.equal(R.cartTotal(d, t), 35);                                // lute 35 gp, not the 25 gp placeholder
  assert.equal(R.cartTotal({ ...d, floor: 5 }, t), 175);              // x5 on floor 5-9
  assert.equal(R.cartTotal({ ...d, cart: [{ id: 'gaming_set', qty: 1, variant: 'dice' }] }, t), 1);
  assert.equal(R.creditsFromPackages(d, t), R.creditsFromPackages({ ...d, floor: 15 }, t));   // package gold does not scale
});

test('S10 variant pick: the gear screen shows a menu per header, the pick is stored as the variant srd_id and lands on the sheet', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  const ctx = makeCtx(dir);
  const p = new Player(ctx, '1', 'Cleo');
  await p.command();
  await drive(p, { name: 'Cleo', cls: 'Cleric', bg: 'Acolyte', kit: { kc: 'A', kb: 'A', variants: { class: 'holy-symbol-emblem', background: 'holy-symbol-reliquary' } } });
  const spec = JSON.stringify(toSpec(JSON.parse(readFileSync(join(dir, 'sessions-data', 'beta', 'create-drafts', '1.json'), 'utf8')), t, 'CRAWLER #0001-A'));
  assert.match(spec, /"srd_id":"holy-symbol-emblem"/);
  await finish(p);
  const inv = stateOf(dir).crawlers[0].inventory;
  assert.deepEqual(inv.filter((r) => r.chargen_key === 'holy_symbol').map((r) => r.srd_id).sort(), ['holy-symbol-emblem', 'holy-symbol-reliquary']);
  assert.ok(inv.every((r) => r.name === 'Intake Bag' || (r.srd_id && !K.isHeaderId(t, r.srd_id))));
  assert.ok(inv.every((r) => r.mechanics && r.mechanics.trim()));
});

test('S10: Next stays disabled until every header has a type; Pick for me resolves them', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  const p = new Player(makeCtx(dir), '2', 'Bard');
  await p.command();
  await drive(p, { name: 'Bardo', cls: 'Bard', bg: 'Entertainer', kit: { kc: 'A', kb: 'A' } }).catch(() => {});
  assert.equal(p.screen(), 'S16');   // drive picked the first variants and moved on
  const q = new Player(makeCtx(dir), '3', 'Moe');
  await q.command();
  await q.click('ACCEPT'); await q.click('Skip'); await q.form('S3:name', { name: 'Moe' }); await q.click('Next');
  await q.form('S4:edit', { look: 'a', hook: 'b' }); await q.click('Next');
  await q.choose('S5:species', 'Human'); await q.click('Next');
  await q.choose('S6:class', 'Cleric'); if (q.components().some((c) => c.custom_id?.includes('S6:choice'))) await q.click('Pick for me'); await q.click('Next');
  await q.choose('S7:bg', 'Acolyte'); await q.choose('S7:asi', q.byKey('S7:asi').options[0].value); if (q.byKey('S7:feat')) await q.choose('S7:feat', q.byKey('S7:feat').options[0].value); await q.click('Next');
  await q.click('Standard array'); await q.click('Pick for me'); await q.click('Next');
  await q.click('Pick for me'); await q.click('Next');
  await q.choose('S10:kc', 'A'); await q.choose('S10:kb', 'A');
  assert.equal(q.disabled('Next'), true);
  assert.match(q.lastText, /pick the type/);
  await q.click('Pick for me');
  assert.equal(q.disabled('Next'), false);
});

test('a synthetic generic header (arcane-focus) is handled like the six known ones: variant pick, own price, never stored', () => {
  const t2 = JSON.parse(JSON.stringify({ chargen: t.chargen }));
  t2.reskins = t.reskins;
  t2.chargen.items.arcane_focus = { name: 'Arcane Focus (your choice)', category: 'magic', cost_cp: 123, mechanics: 'Arcane focus.', srd_id: 'arcane-focus' };
  assert.equal(K.isHeaderKey(t2, 'arcane_focus'), true);                         // via the reskin entry's resolve_to_variant
  assert.deepEqual(K.variantIds(t2, 'arcane_focus'), ['arcane-focus-crystal', 'arcane-focus-orb', 'arcane-focus-rod', 'arcane-focus-staff', 'arcane-focus-wand']);
  assert.equal(K.priceCp(t2, 'arcane-focus', 'arcane_focus'), null);              // cost_cp 123 placeholder ignored
  assert.equal(K.isHeaderId(t, 'druidic-focus'), true);
  assert.ok(Number.isInteger(K.priceCp(t, 'druidic-focus-yew-wand')));
  const d = { class: 'Wizard', background: 'Sage', kitClass: 'A', kitBg: 'A', cart: [{ id: 'arcane_focus', qty: 1, variant: 'arcane-focus-orb' }] };
  assert.equal(R.cartTotal(d, t2), (K.priceCp(t, 'arcane-focus-orb') ?? 0) / 100);
  const rows = R.inventoryRows(d, t2);
  assert.ok(rows.some((r) => r.srd_id === 'arcane-focus-orb'));
  assert.ok(!rows.some((r) => r.srd_id === 'arcane-focus'));
});

test('item-reskins single source: ITEM_RESKINS_PATH override; sha256 must match Lore\'s version file (missing version file only warns)', () => {
  const r = K.checkReskinHash(REAL_CAMPAIGN);
  assert.equal(r.status, 'ok', r.message);
  const d = mkdtempSync(join(tmpdir(), 'reskin-'));
  try {
    writeFileSync(join(d, 'item-reskins.json'), '{"entries":[]}');
    assert.equal(K.checkReskinHash('/nonexistent', { ITEM_RESKINS_PATH: join(d, 'item-reskins.json') }).status, 'warn');
    writeFileSync(join(d, 'item-reskins.version.json'), JSON.stringify({ sha256: '0'.repeat(64) }));
    assert.equal(K.checkReskinHash('/nonexistent', { ITEM_RESKINS_PATH: join(d, 'item-reskins.json') }).status, 'fail');
    assert.equal(K.checkReskinHash('/nonexistent', { ITEM_RESKINS_PATH: join(d, 'nope.json') }).status, 'missing');
  } finally { rmSync(d, { recursive: true, force: true }); }
});

test('a missing item-reskins table degrades to plain 5e names, never a blank or a crash', () => {
  const prev = process.env.ITEM_RESKINS_PATH;
  process.env.ITEM_RESKINS_PATH = '/nonexistent/item-reskins.json';
  try {
    const t3 = loadTables(REAL_CAMPAIGN);
    assert.equal(t3.reskins.loaded, false);
    const d = { class: 'Wizard', background: 'Sage', kitClass: 'A', kitBg: 'A', cart: [] };
    const rows = R.inventoryRows(d, t3);
    assert.ok(rows.every((r) => r.name.trim() && r.mechanics.trim()));
    assert.ok(rows.some((r) => r.name === 'Dagger'));
  } finally { if (prev === undefined) delete process.env.ITEM_RESKINS_PATH; else process.env.ITEM_RESKINS_PATH = prev; }
});

test('legacy_names: a live sheet keeps its stored item name; lookup goes by srd_id, and old names still resolve to the item', () => {
  const stored = { name: 'Duct-Taped Mop Handle', srd_id: 'quarterstaff' };   // written before the reskin table renamed it (legacy_names)
  assert.equal(K.entryFor(t, stored.srd_id).srd_name, 'Quarterstaff');
  assert.equal(K.labelFor(t, stored.srd_id), 'Duct-Taped Mop (Quarterstaff)');       // new sheets use combined_label
  assert.equal(K.findKeyByReskinName(t, 'Duct-Taped Mop Handle'), 'quarterstaff');    // an old (legacy) name still finds the item
  assert.equal(K.priceCp(t, stored.srd_id, 'quarterstaff'), 20);                     // priced by srd_id, not by the stored name
  assert.equal(stored.name, 'Duct-Taped Mop Handle');                                // nothing rewrites a stored name; only /create writes names, at Confirm
});

test('lookup misses (Story Box / deed items with no srd_id or no reskin entry) fall back to the stored name: never an error, never blank', () => {
  for (const nm of ['Pencil & Paper', 'Light Crossbow + 20 Bolts', 'ORIENTATION PIT Banner', 'Kevin the Sentient Rubber Duck']) {
    assert.equal(K.labelFor(t, undefined, nm), nm);
    assert.equal(K.labelFor(t, 'not-in-the-table', nm), nm);
    assert.equal(K.plainName(t, null, nm), nm);
    assert.equal(K.entryFor(t, 'not-in-the-table'), null);
    assert.equal(K.priceCp(t, 'not-in-the-table'), null);
  }
  assert.ok(K.labelFor(t, undefined, '').length > 0);
});

test('off-menu pet items (non_srd: heal-critter-potion, pet-carrier) never appear in /create, vending lists or player docs; /create has no pet question', () => {
  const PET = /heal[- ]critter|pet[- ]carrier|good boy gulp|impossible interior/i;
  assert.ok(K.isOffMenu(t, 'heal-critter-potion') && K.isOffMenu(t, 'pet-carrier'), 'Lore\'s table marks both as non_srd');
  for (const id of ['heal-critter-potion', 'pet-carrier']) {
    assert.equal(K.priceCp(t, id), null);                       // no price in cp, no purchase
    assert.equal(K.itemSrdId(t, id), null);
  }
  for (const nm of ['Good Boy Gulp, Shaken Until Brown', 'Fold-Flat Kennel With an Impossible Interior', 'Heal Critter Potion', 'Pet Carrier']) {
    assert.equal(K.findKeyByReskinName(t, nm), null, nm);       // typed into the shop modal: not found
    assert.equal(findPurchase(nm, t)?.id ?? null, null, nm);
  }
  const listed = K.playerItems(t);                                // what any list/vending wall is built from
  assert.ok(Object.keys(listed).length > 50);
  for (const [k, it] of Object.entries(listed)) assert.doesNotMatch(`${k} ${it.name} ${K.labelFor(t, it.srd_id, it.name)}`, PET, k);
  // defence in depth: a chargen item that points at a non_srd id is dropped from the player list and from loadTables
  const fake = { ...t, chargen: { ...t.chargen, items: { ...t.chargen.items, sneaky: { name: 'Sneaky', srd_id: 'pet-carrier', cost_cp: 100 } } } };
  assert.ok(!('sneaky' in K.playerItems(fake)));
  // no /create screen text, line table or player doc mentions pets
  const pool = JSON.parse(readFileSync(join(REAL_CAMPAIGN, 'tables', 'create-flow-lines.json'), 'utf8')).survey.bonus_pool;
  assert.ok(!pool.some((b) => b.id === 'pets' || /cats or dogs/i.test(b.q)), 'the pets bonus question is gone from the lines table');
  for (const uid of ['1', '1001', '1002', '77777', '424242', 'abc']) {   // the S13 survey (core + bonus pool, Lore's 'pets' question removed) has no pet question
    for (const q of surveyQuestions({ uid, optouts: [] }, t)) assert.doesNotMatch(q.q, /\b(pets?|cats?|dogs?|kittens?|puppy|puppies|animals?)\b/i, q.q);
  }
  for (const f of ['guides/create-how-to.md']) assert.doesNotMatch(readFileSync(join(REAL_CAMPAIGN, f), 'utf8'), PET, f);
  for (const f of ['screens.js', 'rules.js', 'flow.js', 'commit.js', 'files.js']) {
    assert.doesNotMatch(readFileSync(new URL(`../src/create/${f}`, import.meta.url), 'utf8'), /\bd\.pets?\b|['"]pets?['"]|pet_?(name|species|field)|pets?\s*:/i, `${f} has no pet field/screen/question`);
  }
});

test('B2/S7: a session open (or any Crawler on file) means a new /create starts BENCHED, needs no slot even when the party is full, and the first player is never active mid-session', async () => {
  const { dir, ctx } = await setup();
  // 3rd and 4th players fill the party (4 active), then a session opens
  for (const [id, nm] of [['1003', 'Cy'], ['1004', 'Di']]) {
    const p = new Player(ctx, id, nm);
    await p.command();
    await drive(p, { name: `${nm}Crawler`, noShop: true });
    await finish(p);
  }
  assert.equal(JSON.parse(py(dir, 'party', '--json').out).party_slots, '4/4');
  writeFileSync(join(dir, 'sessions-data', 'beta', 'session-status.json'), JSON.stringify({ status: 'open', since: new Date().toISOString(), opens: 1 }));
  const eve = new Player(ctx, '1005', 'Eve');                       // a brand-new 5th human, party full, session open
  const txt = await eve.command();
  assert.doesNotMatch(String(txt), /party is full|party_full|no room/i);
  await drive(eve, { name: 'EveCrawler', noShop: true });
  const out = await finish(eve);
  assert.match(out, /BENCHED/);
  const c = stateOf(dir).crawlers.find((x) => x.name === 'EveCrawler');
  assert.equal(c.status, 'benched');
  assert.equal(JSON.parse(py(dir, 'party', '--json').out).party_slots, '4/4');
  assert.equal(py(dir, 'validate').code, 0);
});

test('S3: the bridge closes the session marker whenever it leaves voice (any reason) and on shutdown; /join opens it idempotently', () => {
  const src = readFileSync(new URL('../src/index.js', import.meta.url), 'utf8');
  assert.match(src, /session\.on\('left',[\s\S]*?markSession\(ctx, 'close'\)/s);
  assert.match(src, /async function shutdown[\s\S]*markSession\(ctx, 'close'\)[\s\S]*session\.leave\(\)/);
  assert.match(readFileSync(new URL('../src/commands/join.js', import.meta.url), 'utf8'), /markSession\(ctx, 'open'\)/);
});
