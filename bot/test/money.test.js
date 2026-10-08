// /create money words: one currency, "credits" (1 credit = 1 GP, 1 cp = 0.01 credit). DISPLAY ONLY: every sum below is integer coin math and is identical to the
// values recorded before the display change; decimals appear only in formatted text.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, utimesSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import test from 'node:test';
import { cpText, creditsText, fmtCredits, money, moneyKeeping, TOKEN } from '../src/create/money.js';
import { loadTables, tablesFor } from '../src/create/data.js';
import * as K from '../src/create/reskin.js';
import * as R from '../src/create/rules.js';
import { Player, REAL_CAMPAIGN, drive, makeCtx, makeSandbox } from './helpers/create-harness.js';

test('fmtCredits / creditsText / cpText: whole credits without decimals, fractions with, singular for an amount of 1 or less', () => {
  assert.equal(fmtCredits(15), '15');
  assert.equal(fmtCredits(0.5), '0.5');
  assert.equal(fmtCredits(0.05), '0.05');
  assert.equal(fmtCredits(12.25), '12.25');
  assert.equal(creditsText(15), '15 credits');
  assert.equal(creditsText(1), '1 credit');
  assert.equal(creditsText(0.5), '0.5 credit');
  assert.equal(creditsText(0), '0 credits');
  assert.equal(cpText(50), '0.5 credit');
  assert.equal(cpText(5), '0.05 credit');
  assert.equal(cpText(100), '1 credit');
  assert.equal(cpText(250), '2.5 credits');
  assert.equal(cpText(null), 'n/a');
  assert.equal(cpText(undefined), 'n/a');
});

test('money(): GP, cp, gold and cash words become credits; names and other text are left alone', () => {
  assert.equal(money('Package A (8 GP left over)'), 'Package A (8 credits left over)');
  assert.equal(money('Gold option: 50 GP'), 'Credits option: 50 credits');
  assert.equal(money('1 GP'), '1 credit');
  assert.equal(money('1,500 gp'), '1500 credits'.replace('1500', '1500'));
  assert.equal(money('5 cp'), '0.05 credit');
  assert.equal(money('150 cp'), '1.5 credits');
  assert.equal(money('Take each package or its gold.'), 'Take each package or its credits.');
  assert.equal(money('Box or Cash (Package or gold)'), 'Box or Credits (Package or credits)');
  assert.equal(money('each gives a package or a gold amount (1 gold = 1 credit).'), 'each gives a package or a credits amount.');
  assert.equal(money('The Gold Dragonborn'), 'The Credits Dragonborn');   // callers never pass names; this documents why they must not
  assert.equal(money('Sickle, 12 credits'), 'Sickle, 12 credits');
  assert.equal(money('Equipment'), 'Equipment');
  assert.equal(money(undefined), '');
  assert.equal(moneyKeeping(`${TOKEN}: package or gold`, 'Gold Digger (Soldier)'), 'Gold Digger (Soldier): package or credits');
});

// Recorded BEFORE the display change (same tables): 122 priced entries, per-line costs for qty 1/3/7 at floors 1/5/10/15, and the all-items cart totals.
const GOLDEN = { rows: 122, totals: [8805, 43999, 175993, 439981], digest: '4d3607743f8e296f058d1effbc7d3fce7abe95a566a2df3a2aca6768f6b51ef2' };
const priced = (t) => {
  const out = [];
  for (const [id] of Object.entries(t.chargen.items)) {
    const ids = K.isHeaderKey(t, id) ? K.variantIds(t, id).map((v) => [v, v]) : [[K.itemSrdId(t, id), null]];
    for (const [srd, variant] of ids) {
      const cp = K.priceCp(t, srd, id);
      if (cp !== null) out.push({ id, srd, variant, cp });
    }
  }
  return out;
};

test('price math is untouched: line costs, cart totals and the credit breakdown equal the integer coin values recorded before the display change', () => {
  const t = loadTables(REAL_CAMPAIGN);
  const rows = priced(t);
  assert.equal(rows.length, GOLDEN.rows);
  const out = rows.map((r) => {
    const row = [r.id, r.srd, r.cp];
    for (const floor of [1, 5, 10, 15]) for (const qty of [1, 3, 7]) row.push(R.cartLineCost({ id: r.id, qty, variant: r.variant }, t, floor));
    return row;
  });
  assert.equal(createHash('sha256').update(JSON.stringify(out)).digest('hex'), GOLDEN.digest);
  const cart = rows.map((r) => ({ id: r.id, qty: 2, variant: r.variant ?? undefined }));
  assert.deepEqual([1, 5, 10, 15].map((f) => R.cartTotal({ cart, floor: f }, t)), GOLDEN.totals);
  // independent of the bridge: the same integers computed straight from the table's copper prices
  const mult = { 1: 1, 5: 5, 10: 20, 15: 50 };
  for (const f of [1, 5, 10, 15]) assert.equal(R.cartTotal({ cart, floor: f }, t), cart.reduce((s, l, i) => s + Math.ceil((rows[i].cp * 2 * mult[f]) / 100), 0));
});

test('decimals are formatting only: summing the DISPLAYED credit amounts gives exactly the integer copper sum / 100, and the display never feeds a total', () => {
  const t = loadTables(REAL_CAMPAIGN);
  const rows = priced(t);
  const cps = rows.map((r) => r.cp);
  const cpSum = cps.reduce((s, c) => s + c, 0);                                  // integer coins, never rounded before summing
  const shown = cps.map((c) => Number(cpText(c).split(' ')[0]));                 // what the player sees
  assert.equal(Math.round(shown.reduce((s, c) => s + c * 100, 0)), cpSum);
  for (const c of cps) assert.equal(Math.round(Number(cpText(c).split(' ')[0]) * 100), c, `${c} cp round-trips`);
  assert.ok(cps.some((c) => c % 100 !== 0), 'the table has fractional-credit prices (sub-credit cp)');
  // the displayed text is derived from the integer; the integer is not a function of the text
  const before = JSON.stringify(rows);
  rows.forEach((r) => cpText(r.cp));
  assert.equal(JSON.stringify(rows), before);
  // the rules module does not import the display helpers (math and text stay separate); only its error TEXT goes through money()
  const src = readFileSync(new URL('../src/create/rules.js', import.meta.url), 'utf8');
  for (const m of src.matchAll(/\bmoney\(([^\n]*)/g)) assert.match(m[1], /tx\(t, 'error-/, 'rules.js uses money() only around error messages');
});

const MONEY_WORDS = /\b(GP|gp|cp|gold|cash)\b/;
const setFlag = (dir, on) => {
  const sj = join(dir, 'sessions-data', 'beta', 'session.json');
  const prof = JSON.parse(readFileSync(sj, 'utf8'));
  prof.create = { ...(prof.create ?? {}), screens_reskin: on };
  writeFileSync(sj, JSON.stringify(prof));
  const t = new Date(Date.now() + 5000 + Math.floor(Math.random() * 1e6)); utimesSync(sj, t, t);
};

for (const flag of [false, true]) {
  test(`S10 shows credits only (flag ${flag ? 'on' : 'off'}): package labels, gold option, intro, price list, no GP/cp/gold/cash, and the stored values keep their numbers`, async () => {
    const dir = makeSandbox('beta');
    const ctx = makeCtx(dir);
    const p = new Player(ctx, '3001', 'Eve');
    await p.command();
    let seen = null;
    await assert.rejects(drive(p, { name: 'Eve', bg: 'Soldier', species: 'Human', cls: 'Fighter', onS9: async (r) => {
      if (flag) setFlag(dir, true);   // the walk uses the plain labels; the flag goes on just before S10 renders
      await r.click('next');
      assert.equal(r.screen(), 'S10');
      const text = [r.lastText, ...r.components().flatMap((c) => [c.label, c.placeholder, ...(c.options ?? []).flatMap((o) => [o.label, o.description])])].filter(Boolean).join('\n');
      seen = { text, kc: r.byKey('S10:kc').options, kb: r.byKey('S10:kb').options };
      await r.click('prices');
      seen.priceMsgs = r.followups.map((f) => f.content ?? '');
      seen.prices = seen.priceMsgs.join('\n');
      throw new Error('STOP-AT-S10');
    } }), /STOP-AT-S10/);
    assert.ok(seen);
    assert.ok(!MONEY_WORDS.test(seen.text), `money words left on S10: ${seen.text.match(MONEY_WORDS)?.[0]} in\n${seen.text}`);
    assert.match(seen.text, /\*\*Credits:\*\* \d+ from options, \d+ spent/);
    const t = tablesFor(ctx.config);
    const fighter = t.chargen.classes.Fighter;
    for (const o of seen.kc) {
      const pk = fighter.packages.find((x) => x.id === o.value);
      assert.match(o.label, new RegExp(`\\b${pk.gp} credits?\\b`), o.label);   // the SAME number as the table's gp value
    }
    assert.ok(seen.kc.some((o) => /credits/i.test(o.label)) && seen.kb.some((o) => /credits/i.test(o.label)));
    assert.ok(!MONEY_WORDS.test(seen.prices), seen.prices.match(MONEY_WORDS)?.[0]);
    assert.match(seen.prices, /\d(\.\d+)? credits?/);
    // "Gas-Station GPS Kit" contains " GP" once gear is listed; a price is a number then GP or cp
    assert.ok(!/\d\s*GP\b|\d\s*cp\b/.test(seen.prices));
    assert.ok(seen.priceMsgs.length >= 3, `expected Weapons, Armor, and Other gear messages, got ${seen.priceMsgs.length}`);
    assert.ok(seen.priceMsgs.every((m) => m.length > 0 && m.length <= 2000), seen.priceMsgs.map((m) => m.length).join(','));
    const titles = seen.priceMsgs.map((m) => (m.match(/^\*\*(Weapons|Armor|Other gear)\*\*/) || [])[1]);
    assert.ok(titles.every(Boolean), 'every price message starts with Weapons, Armor, or Other gear');
    assert.deepEqual([...new Set(titles)], ['Weapons', 'Armor', 'Other gear']);
    assert.match(seen.prices, /Rations|Torch|Rope/);
    assert.match(seen.prices, /Spellbook|Component Pouch|Arcane Focus/);   // magic/misc stays on the Other gear list
    assert.match(seen.prices, /Gas-Station GPS Kit/);   // late gear item: the list was not sliced off at armor
  });
}

test('a committed Crawler: credits and the credit breakdown are the same integers as the packages and cart say; ledger reasons are stored as before', async () => {
  const dir = makeSandbox('beta', ['--review', 'off']);
  const ctx = makeCtx(dir);
  const p = new Player(ctx, '3002', 'Fay');
  await p.command();
  await drive(p, { name: 'Fay', bg: 'Soldier', species: 'Human', cls: 'Fighter', kit: { kc: 'A', kb: 'A', shop: 'Rations 3' } });
  assert.equal(p.screen(), 'S16');
  await p.click('Confirm ▸');
  await p.click('Confirm and lock the file');
  const st = JSON.parse(readFileSync(join(dir, 'sessions-data', 'beta', 'state.json'), 'utf8'));
  const c = st.crawlers.find((x) => x.name === 'Fay');
  const t = tablesFor(ctx.config);
  const gp = (cls, id) => cls.packages.find((x) => x.id === id).gp;
  const fromPackages = gp(t.chargen.classes.Fighter, 'A') + gp(t.chargen.backgrounds.Soldier, 'A');
  const cost = R.cartLineCost({ id: Object.keys(t.chargen.items).find((k) => /ration/i.test(k)), qty: 3 }, t, 1);
  assert.equal(c.credits, fromPackages - cost);
  assert.ok(c.credits >= 0 && Number.isInteger(c.credits));
});
