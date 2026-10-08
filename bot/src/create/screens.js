/**
 * The 17 /create screens (spec: characters/create-flow-spec-5e.md). Each screen is data + small handlers:
 *   rows(d, env)        -> content component rows (nav row is added by the flow)
 *   describe(d, env)    -> plain-rule text under the System's prompt
 *   ready(d, env)       -> null when Next is allowed, else the reason
 *   onSelect / onButton / onModal(key, ..., d, env) mutate the draft and return {notice?, modal?, followup?}
 *   followup is one ephemeral string, or an array of them (S10 price list: Weapons, Armor, Other gear)
 */
import { ButtonStyle } from 'discord.js';
import { ABILITIES, ABILITY_NAMES, backgroundNames, line } from './data.js';
import * as R from './rules.js';
import * as K from './reskin.js';
import { tx, txd } from './screenstext.js';
import { TOKEN, creditsText, fmtCredits, money, moneyKeeping } from './money.js';
import { BRANCH_CHOICES, classLabel, classOptionLabel, lineageLabel, speciesLabel } from './names.js';
import { asiFlavor, asiLabel, backgroundFlavor, backgroundLabel, featFlavor, featLabel, packageFlavor, packageLabel } from './bgnames.js';
import { isActive } from './owner.js';
import { button, cid, cleanText, cut, modal, row, select } from './ui.js';
import { nearDuplicate, takenNames } from './commit.js';
import { buildBlock } from './files.js';

const RESERVED = new Set(['gm', 'ai', 'system', 'party', 'all', 'everyone']);
const NAME_RE = /^[\p{L}\p{N} '.-]+$/u;
const A = (a) => a.toUpperCase();
const list = (x) => (x?.length ? x.join(', ') : '-');
const pick = (values, d, key) => (d[key] = values);

/** Drop picks that stopped being legal after an earlier choice changed; returns the notices. */
export function revalidate(d, t) {
  const dropped = [];
  const sp = R.speciesInfo(d, t);
  if (d.speciesSub && !(sp?.sub?.options ?? []).includes(d.speciesSub)) { d.speciesSub = null; dropped.push('species sub-choice'); }
  const cl = R.classInfo(d, t);
  for (const k of Object.keys(d.classChoices ?? {})) if (!cl?.choices?.some((c) => c.key === k && (c.options ?? []).includes(d.classChoices[k]))) { delete d.classChoices[k]; dropped.push(k.replace(/_/g, ' ')); }
  const bg = R.bgInfo(d, t);
  if (d.asi && (!bg || (d.asi.type === '2-1' && !(bg.asi.includes(d.asi.plus2) && bg.asi.includes(d.asi.plus1))))) { d.asi = null; dropped.push('background score bonus'); }
  if (d.extraFeat && (!R.extraFeatNeeded(d, t) || d.extraFeat === bg?.feat)) { d.extraFeat = null; dropped.push('extra Origin feat'); }
  if (d.base && d.method !== 'roll' && !R.validateBase(d, t) === false) { /* base stays; ASI is re-applied automatically */ }
  if (d.classSkills?.length && (d.classSkills.length !== cl?.skill_count || d.classSkills.some((s) => !R.classSkillOptions(d, t).includes(s)))) { d.classSkills = []; dropped.push('class skills'); }
  const so = R.speciesSkillOptions(d, t);
  if (d.speciesSkill && (!so || !so.options.includes(d.speciesSkill))) { d.speciesSkill = null; dropped.push('species skill'); }
  if (d.featSkills?.length && (R.featSkillCount(d, t) !== d.featSkills.length || d.featSkills.some((s) => !R.featSkillOptions(d, t).includes(s)))) { d.featSkills = []; dropped.push('feat skills'); }
  if (d.expertise?.length && d.expertise.some((s) => !R.expertiseOptions(d, t).includes(s))) { d.expertise = []; dropped.push('expertise'); }
  const mc = R.masteryChoice(d, t);
  if (d.masteries?.length && (!mc || d.masteries.length !== mc.count || d.masteries.some((m) => !mc.options.includes(m)))) { d.masteries = []; if (!d.masteriesAuto) dropped.push('weapon masteries'); }
  if (d.masteriesAuto) R.fillDefaultMasteries(d, t);   // defaults follow the carried weapons; the player's own picks are kept
  if (d.kitClass && !cl?.packages?.some((p) => p.id === d.kitClass)) { d.kitClass = null; dropped.push('class equipment'); }
  if (d.kitBg && !bg?.packages?.some((p) => p.id === d.kitBg)) { d.kitBg = null; dropped.push('background equipment'); }
  if (d.spells && (!cl?.spells || (d.spells.cantrips ?? []).some((n) => !cl.spells.cantrip_list.includes(n)) || (d.spells.level1 ?? []).some((n) => !cl.spells.level1_list.includes(n)))) { d.spells = null; dropped.push('spells'); }
  if (d.variants) {
    const want = new Map(R.pendingVariants(d, t).map((v) => [`${v.src}:${v.id}`, v.options]));
    let lost = false;
    for (const [k, v] of Object.entries(d.variants)) if (!want.get(k)?.includes(v)) { delete d.variants[k]; lost = true; }
    if (lost) dropped.push('equipment type picks');
  }
  if (d.cart?.some((l) => !t.chargen.items[l.id] || (K.isHeaderKey(t, l.id) && !K.variantIds(t, l.id).includes(l.variant)))) { d.cart = d.cart.filter((l) => t.chargen.items[l.id] && (!K.isHeaderKey(t, l.id) || K.variantIds(t, l.id).includes(l.variant))); dropped.push('Vending Wall lines that could not be priced'); }
  if (R.disallowedCart(d, t).length) { d.cart = d.cart.filter((l) => R.itemAllowed(d, t, l.id)); dropped.push('class-only Vending Wall items (Spellbook: Wizards only)'); }
  if (d.mi) {
    const keep = R.miFeats(d, t);
    for (const f of Object.keys(d.mi)) if (!keep.includes(f) || R.miProblem(f, d.mi[f], t)) { delete d.mi[f]; dropped.push(`${f} spell picks`); }
  }
  if (d.lessonsFeat && (!R.lessonsFeatOffered(d, t) || !R.lessonsFeatOptions(d, t).includes(d.lessonsFeat))) { d.lessonsFeat = null; dropped.push('Lessons of the First Ones feat'); }
  if (R.creditsLeft(d, t) < 0 && d.cart?.length) { d.cart = []; dropped.push('Vending Wall purchases'); }
  return dropped;
}

/** Ids of Lore's screens-layer rows (create-screens-reskins.json) for the things that come from tables (titles, abilities, class choices, methods). */
const TITLE_IDS = { S3: 'title-s3', S4: 'title-s4', S8: 'title-s8', S9: 'title-s9', S10: 'title-s10', S11: 'title-s11', S14: 'title-s14', S16: 'title-s16', S17: 'title-s17' };
const ABILITY_IDS = { str: 'ability-str', dex: 'ability-dex', con: 'ability-con', int: 'ability-int', wis: 'ability-wis', cha: 'ability-cha' };
const CHOICE_IDS = { divine_order: 'choice-divine-order', fighting_style: 'choice-fighting-style', invocation: 'choice-invocation', primal_order: 'choice-primal-order' };
const OPTION_PREFIX = { fighting_style: 'opt-fighting-style-', invocation: 'opt-invocation-' };
const METHOD_IDS = { array: 'method-standard-array', pointbuy: 'method-point-buy', roll: 'method-roll' };
const METHOD_PLAIN = { array: 'Standard array', pointbuy: 'Point buy', roll: 'Roll' };
/** The screen title with its number: the layer's title row when on and the current title still matches, else the current title. */
export const screenTitle = (t, screen) => tx(t, TITLE_IDS[screen], SCREENS[screen]?.title ?? '');
const abilityLabel = (t, ab) => { const l = txd(t, ABILITY_IDS[ab], ABILITY_NAMES[ab]); return l === ABILITY_NAMES[ab] ? A(ab) : l; };
const optionLabel = (t, ch, o) => (OPTION_PREFIX[ch.key] ? txd(t, `${OPTION_PREFIX[ch.key]}${kebab(o)}`, o) : o);
const kebab = (x) => String(x).toLowerCase().replace(/'/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');

/** The current package label (class packages and the plain fallback of background packages): Lore's package-class-a/b and package-gold rows when the screens layer is on. */
const pkgPlain = (t, p) => money(p.items.length   // money words show as credits (money.js); the row's `old` is still compared against the old GP wording
  ? tx(t, p.id === 'A' ? 'package-class-a' : p.id === 'B' ? 'package-class-b' : 'package-class-x', `Package ${p.id} (${p.gp} GP left over)`, { gp: p.gp })
  : tx(t, 'package-gold', `Gold option: ${p.gp} GP`, { gp: p.gp }));
/** The S10 package-or-gold menu placeholder: the owner's name is kept as is, the money words show as credits. */
const ownerKit = (t, owner) => moneyKeeping(tx(t, 'select-s10-kit', `${TOKEN}: package or gold`, { owner: TOKEN }), owner);

function optionsFromPackages(list_, t, d, src) {
  return list_.packages.map((p) => ({
    // S10 background package: the display name (Lore's background-reskins.json, only while create.background_reskin is true) replaces the label text, never the value
    label: (src === 'background' ? money(packageLabel(t, p.id, p.items.length ? `${creditsText(p.gp)} left over` : creditsText(p.gp), pkgPlain(t, p))) : pkgPlain(t, p)).slice(0, 100),
    value: p.id,
    // the package screen lists real 5e names (spec S10); a header shows as "pick the type" (never as a priced item)
    description: p.items.length ? p.items.map(([id, q]) => `${q > 1 ? `${q} ` : ''}${K.isHeaderKey(t, id) ? (d.variants?.[`${src}:${id}`] ? K.plainName(t, d.variants[`${src}:${id}`]) : `${t.chargen.items[id].name.replace(/ \(your choice\)/, '')} (pick type)`) : t.chargen.items[id].name}`).join(', ') : `${money(tx(t, 'hint-s10-skip-package', 'Skip the package, take the credits'))}${src === 'background' && packageFlavor(t, p.id) ? `. ${packageFlavor(t, p.id)}` : ''}`,
  }));
}

const normText = (s) => String(s ?? '').toLowerCase().replace(/[^a-z0-9 ]/g, '').trim();

/** Names a player may type for a chargen item: its 5e name, the reskin display/combined/legacy names, never the old `junk` field. */
function namesOf(id, it, t) {
  const e = K.entryFor(t, it.srd_id);
  return [it.name, e?.srd_name, e?.display_name, e?.combined_label, ...(e?.legacy_names ?? [])].filter(Boolean).map(normText);
}

/** Resolve a typed item name ("rope", "healer's kit", "Extension Cord") to a chargen key. May return a header key (use findPurchase to resolve it). */
export function findItem(text, t) {
  const n = normText(text);
  if (!n) return null;
  const items = Object.entries(t.chargen.items);
  const exact = items.filter(([id, it]) => id === n.replace(/ /g, '_') || namesOf(id, it, t).includes(n));
  if (exact.length === 1) return exact[0][0];
  const part = items.filter(([id, it]) => namesOf(id, it, t).some((x) => x.startsWith(n) || x.includes(n)));
  return part.length === 1 ? part[0][0] : part.length > 1 ? part.find(([id, it]) => namesOf(id, it, t).some((x) => x.startsWith(n)))?.[0] ?? null : null;
}

/** Vending Wall lookup: {id} for a plain item, {id, variant} when a variant name was typed ("lute"), {header: id} when only the generic was typed (not purchasable), else null. */
export function findPurchase(text, t) {
  const id = findItem(text, t);
  if (id && !K.isHeaderKey(t, id)) return { id };
  for (const [key] of Object.entries(t.chargen.items).filter(([k]) => K.isHeaderKey(t, k))) {
    const v = K.findVariant(t, key, text);
    if (v) return { id: key, variant: v };
  }
  return id ? { header: id } : null;
}

function previewTable(d, t) {
  const fa = R.finalAbilities(d, t);
  if (!fa) return '';
  const bonus = R.asiBonus(d, t);
  const dv = R.derived(d, t);
  const rows = ABILITIES.map((a) => `${A(a)}  base ${String(d.base[a]).padStart(2)} ${bonus[a] ? `+${bonus[a]}` : '  '} = ${String(fa[a]).padStart(2)}  (${R.signed(R.mod(fa[a]))})`);
  const acNote = d.kitClass && d.kitBg ? '' : ` ${tx(t, 'hint-s8-ac-provisional', '(10 + Dex for now)')}`;
  rows.push('', tx(t, 'hint-s8-preview-line', `HP ${dv.hp}   AC ${dv.ac}${acNote}   Prof +${R.PB}   Init ${R.signed(dv.initiative)}   Passive Perception ${dv.passives.perception}`, { hp: dv.hp, ac: dv.ac, ac_note: acNote, pb: R.PB, init: R.signed(dv.initiative), pp: dv.passives.perception }));
  return '```\n' + rows.join('\n') + '\n```';
}

/** A price held as integer copper, shown as credits (Lore's hint-money-gp / hint-money-cp rows, else money.js). Formatting only: the integer is never changed. */
const priceText = (t, cp) => {
  if (cp === null || cp === undefined) return 'n/a';
  const credits = cp / 100, amount = fmtCredits(credits);
  return money(cp >= 100 ? tx(t, 'hint-money-gp', `${credits} GP`, { n: amount }) : tx(t, 'hint-money-cp', `${cp} cp`, { amount }));
};

const DISCORD_CONTENT_MAX = 2000;
const priceBucket = (cat) => {
  const c = String(cat ?? '').toLowerCase();
  if (c === 'weapons') return 'Weapons';
  if (c === 'armor') return 'Armor';
  return 'Other gear';   // gear, magic, and anything else that is not a weapon or armor
};

/** One Gouge Sheet section as Discord messages of at most 2000 characters. Later parts repeat the header with (cont.). */
function chunkPriceList(header, lines) {
  const out = [];
  if (!lines.length) return out;
  const title = (cont) => (cont ? `**${header}** (cont.)` : `**${header}**`);
  let cont = false;
  let buf = title(false);
  for (let line of lines) {
    if (!line) continue;
    const fits = () => buf.length + 1 + line.length <= DISCORD_CONTENT_MAX;
    if (!fits()) {
      if (buf !== title(cont)) { out.push(buf); cont = true; buf = title(true); }
      if (!fits()) line = line.slice(0, Math.max(0, DISCORD_CONTENT_MAX - buf.length - 1));
    }
    if (line) buf += `\n${line}`;
  }
  if (buf.includes('\n')) out.push(buf);
  return out;
}

const kitText = (d, t) => [
  ...R.inventoryRows(d, t).map((r) => `• ${r.name}${r.qty > 1 ? ` ×${r.qty}` : ''}`),
  ...R.pendingVariants(d, t).filter((v) => !v.chosen || !v.options.includes(v.chosen)).map((v) => `• *${t.chargen.items[v.id].name.replace(/ \(your choice\)/, '')}: pick the type in the menu below*`),
].join('\n');

// ---------------------------------------------------------------- S8 Roll method (decision 024)
const effMethod = (d, env) => (d.method === 'roll' && !env.settings.allowRoll ? null : d.method ?? null);   // switch off: Roll disappears, the saved rounds are held
const rollRounds = (d) => d.scoreRolls?.rounds ?? [];
const diceText = (dice) => {
  const sorted = [...dice].sort((a, b) => b - a);
  return `(${sorted.slice(0, 3).join(' ')} ~~${sorted[3]}~~)`;
};
const arrayText = (a, t, uid) => {
  const order = a.scores.map((sc, i) => ({ sc, i })).sort((x, y) => y.sc - x.sc);
  return `**${a.id}:** ${order.map((o) => o.sc).join(' ')} = **${a.total}**  ${line(t, a.keepable ? 'S8_roll_keep_ok' : 'S8_roll_keep_no', uid, { total: a.total })}\n${order.map((o) => `${o.sc} ${diceText(a.dice[o.i])}`).join(' · ')}`;
};
function rollText(d, env) {
  const rounds = rollRounds(d);
  if (!rounds.length) return tx(env.t, 'notice-s8-press-roll', 'Press Roll for your three arrays.');
  const last = rounds.at(-1);
  const out = [];
  if (rounds.length > 1) out.push(rounds.slice(0, -1).map((r) => `Round ${r.round}: ${r.arrays.map((a) => `${a.id} ${a.total}`).join(', ')} (none above 72)`).join('\n'), line(env.t, 'S8_roll_none', d.uid));
  if (!last.qualified) { out.push(line(env.t, 'S8_roll_giveup', d.uid, { rounds: rounds.length })); return out.join('\n'); }
  out.push(`**Round ${last.round}.** ${line(env.t, 'S8_roll_result', d.uid)}`, ...last.arrays.map((a) => arrayText(a, env.t, d.uid)));
  const kept = d.scoreRolls?.kept;
  if (kept?.round === last.round) {
    const arr = last.arrays.find((a) => a.id === kept.array);
    out.push(`${tx(env.t, 'hint-s8-kept', `**Kept: ${kept.array}.**`, { array: kept.array })} ${line(env.t, 'S8_roll_assign', d.uid)} ${line(env.t, 'S8_roll_cap', d.uid)}`);
    out.push(ABILITIES.map((a) => `${A(a)} ${Number.isInteger(d.rollAssign?.[a]) && arr ? arr.scores[d.rollAssign[a]] : '-'}`).join('  '));
  } else out.push(tx(env.t, 'notice-s8-tap-keep', 'Tap Keep A, B or C (a greyed-out array is not keepable).'));
  return out.join('\n');
}
function assignRows(d, arr, t) {
  const as = d.rollAssign ?? {};
  return ABILITIES.map((ab) => {
    const used = new Set(ABILITIES.filter((x) => x !== ab).map((x) => as[x]).filter(Number.isInteger));
    const opts = arr.scores.map((sc, i) => ({ sc, i })).filter((o) => !used.has(o.i)).sort((x, y) => y.sc - x.sc || x.i - y.i)
      .map((o) => ({ label: String(o.sc), value: String(o.i), description: `rolled as ${arr.id}${o.i + 1}` }));
    return select(cid(d.uid, 'S8', 'assign', ab), tx(t, 'select-s8-assign', `${A(ab)}: pick a score`, { ab: A(ab), ability_label: abilityLabel(t, ab) }), opts, { selected: Number.isInteger(as[ab]) ? [String(as[ab])] : [] });
  });
}
/** [Roll]: roll rounds of three arrays until one is keepable (max 10), saving each round in the draft; saved rounds are shown again, never rolled again. */
async function rollMethod(d, env) {
  const was = d.method;
  d.method = 'roll';
  const sr = (d.scoreRolls ??= { rounds: [], kept: null });
  if (!sr.who && d.name) sr.who = d.name;   // the log name of these rounds (a Restart wipes the draft's own name)
  const giveUp = () => {
    d.method = null;
    d.base = null;
    return { notice: line(env.t, 'S8_roll_giveup', d.uid, { rounds: sr.rounds.length }) };
  };
  if (sr.rounds.length >= R.ROLL_MAX_ROUNDS && !sr.rounds.at(-1).qualified) return giveUp();
  if (was !== 'roll') d.base = null;   // coming from another method: the old base is not a Roll base
  try {
    while (!sr.rounds.at(-1)?.qualified && sr.rounds.length < R.ROLL_MAX_ROUNDS) {
      sr.rounds.push(await env.rollRound(d, sr.rounds.length + 1));
      env.save?.(d);
    }
  } catch (err) {
    env.log?.({ event: 'roll_error', uid: d.uid, message: String(err.message).slice(0, 200) });
    return { notice: tx(env.t, 'notice-s8-dice-jam', 'The dice would not roll. Tap Roll to try again.') };
  }
  if (!sr.rounds.at(-1).qualified) { env.log?.({ event: 'roll_giveup', uid: d.uid, rounds: sr.rounds.length }); return giveUp(); }
  const c = R.checkRolls(sr);   // a complete saved assignment for the kept array brings its base back (coming back to Roll from another method)
  if (!d.base && !c.error && ABILITIES.every((a) => Number.isInteger(d.rollAssign?.[a]))) d.base = Object.fromEntries(ABILITIES.map((a) => [a, c.scores[d.rollAssign[a]]]));
  return {};
}

export const SCREENS = {
  // ------------------------------------------------------------------ S1
  S1: {
    title: 'Welcome and table settings',
    nav: false,
    describe(d, env) {
      const c = env.party.campaign ?? {};
      return `**Session:** ${d.session}  |  **Death Mode:** ${c.death_mode ?? '-'}  |  **Comfort:** ${c.comfort ?? '-'}  |  **Floor 1 Reprieve:** ${c.f1_reprieve ? 'on' : 'off'}\n**Party:** ${env.party.count} of ${env.party.max} active Crawlers${env.party.benched ? `\n**You already have ${env.party.owned.length} Crawler${env.party.owned.length > 1 ? 's' : ''}** (${env.party.owned.map((c) => `${c.name}${isActive(c) ? ' - active' : ' - benched'}`).join(', ')}). This new Crawler starts **BENCHED**: it takes no party slot and stays inert until you swap to it between sessions (/crawlers).` : ''}\n*Table settings are changed only by the table owner.*`;
    },
    rows(d, env) {
      const rows = [row(
        button(cid(d.uid, 'S1', 'accept'), 'ACCEPT', { style: ButtonStyle.Success }),
        button(cid(d.uid, 'S1', 'decline'), 'DECLINE', { style: ButtonStyle.Danger }),
        button(cid(d.uid, 'S1', 'terms'), 'Read the Terms'),
        button(cid(d.uid, 'S1', 'prebuilt'), 'Use a pre-built', { disabled: !env.t.prebuilt.crawlers.length }),
      )];
      if (d.showPrebuilt) {
        rows.push(select(cid(d.uid, 'S1', 'pick'), 'Pick a pre-built concept', env.t.prebuilt.crawlers.slice(0, 25).map((p) => ({ label: `${p.label} - ${classLabel(env.t, p.class)}`.slice(0, 100), value: p.id, description: `${speciesLabel(env.t, p.species)} ${p.background}: ${p.blurb ?? ''}` }))));
      }
      return rows;
    },
    ready: () => 'Tap ACCEPT, DECLINE, Read the Terms or a pre-built to go on.',
    onButton(key, d, env) {
      if (key === 'accept' || key === 'decline') { d.terms = key; return { go: 'S2' }; }
      if (key === 'terms') { d.terms = 'accept'; d.readTerms = true; return { go: 'S2', notice: 'The Terms are not shown. Reading them is noted. *Don\'t Skip Intro* arrives at Confirm.' }; }
      if (key === 'prebuilt') { d.showPrebuilt = !d.showPrebuilt; return {}; }
      return {};
    },
    onSelect(key, values, d, env) {
      const p = env.t.prebuilt.crawlers.find((x) => x.id === values[0]);
      if (!p) return { notice: 'Unknown pre-built.' };
      for (const k of ['species', 'speciesSub', 'class', 'classChoices', 'background', 'asi', 'extraFeat', 'method', 'base', 'classSkills', 'speciesSkill', 'featSkills', 'languages', 'expertise', 'masteries', 'kitClass', 'kitBg', 'cart', 'spells', 'orders', 'reactions', 'signature']) {
        if (p[k] !== undefined) d[k] = JSON.parse(JSON.stringify(p[k]));
      }
      d.prebuilt = p.id;
      d.variants = p.variants ? JSON.parse(JSON.stringify(p.variants)) : {};
      R.fillVariants(d, env.t);   // a pre-built has no gear screen: unresolved headers take their first listed variant (editable on S10)
      d.terms = 'accept';
      d.showPrebuilt = false;
      return { go: 'S2', notice: `Pre-built **${p.label}** loaded. You still do comfort, name, look, backstory and review. Everything can be edited.` };
    },
  },

  // ------------------------------------------------------------------ S2
  S2: {
    title: 'Comfort: lines and veils (private)',
    skippable: true,
    describe(d) {
      const o = d.optouts ?? [];
      return `A **line** never appears anywhere. A **veil** may exist off-screen but is never shown (fade to black). The word **cut** works any time in play with no setup.\nNo explanation is asked or stored. Only topics you mark with \`*\` can be seen by the reviewer; the GM obeys all of them regardless.\n\n**Your list (only you see this):** ${o.length ? o.map((x) => `${x.kind}: ${x.topic}${x.shared ? ' (shared)' : ''}`).join('; ') : 'none'}`;
    },
    rows: (d) => [row(button(cid(d.uid, 'S2', 'edit'), 'Add or edit lines and veils'), button(cid(d.uid, 'S2', 'clear'), 'Clear all', { disabled: !(d.optouts ?? []).length }))],
    ready: () => null,
    onButton(key, d, env) {
      if (key === 'clear') { d.optouts = []; return { notice: 'Cleared.' }; }
      const val = (kind) => (d.optouts ?? []).filter((o) => o.kind === kind).map((o) => o.topic + (o.shared ? ' *' : '')).join('\n');
      return { modal: modal(cid(d.uid, 'S2', 'm', 'edit'), 'Lines and veils (private)', [
        { id: 'lines', label: 'Lines (never appear). One per line', style: 'paragraph', required: false, max: 400, value: val('line'), placeholder: 'spiders\nending a topic with * shares it with the GM reviewer' },
        { id: 'veils', label: 'Veils (never shown). One per line', style: 'paragraph', required: false, max: 400, value: val('veil') },
      ]) };
    },
    onModal(key, f, d) {
      const out = [];
      for (const [kind, id] of [['line', 'lines'], ['veil', 'veils']]) {
        for (const raw of String(f.get(id) ?? '').split('\n')) {
          const shared = /\*\s*$/.test(raw.trim());
          const topic = raw.replace(/\*\s*$/, '').replace(/\s+/g, ' ').trim().slice(0, 60);
          if (topic) out.push({ kind, topic, shared });
        }
      }
      if (out.length > 6) return { notice: 'Six topics at most. Nothing was changed.' };
      d.optouts = out;
      return { notice: 'Saved privately.' };
    },
  },

  // ------------------------------------------------------------------ S3
  S3: {
    title: 'Crawler name and pronouns',
    skippable: false,
    describe(d) {
      const near = d.nearDup ? `\n⚠ ${line({ lines: { lines: { x: ['That name sits inside another Crawler\'s name (\'{other}\'). Tools match partial names, so this could cause mix-ups. Tap Use it anyway, or pick another.'] } } }, 'x', d.uid, { other: d.nearDup.other })}` : '';
      return `**Name:** ${d.name ?? '(not set)'}  |  **Pronouns:** ${d.pronouns ?? 'unspecified'}\n2-30 characters: letters, digits, space, apostrophe, hyphen, period. Unique in this session.${near}`;
    },
    rows(d, env) {
      const t = env?.t;
      const r = [row(button(cid(d.uid, 'S3', 'name'), d.name ? tx(t, 'button-s3-change', 'Change name') : tx(t, 'button-s3-set', 'Set name'), { style: ButtonStyle.Primary }), ...(d.nearDup ? [button(cid(d.uid, 'S3', 'anyway'), tx(t, 'button-s3-anyway', 'Use it anyway'), { style: ButtonStyle.Danger })] : []))];
      r.push(select(cid(d.uid, 'S3', 'pron'), tx(t, 'select-s3-pronouns', 'Pronouns (optional)'), ['he/him', 'she/her', 'they/them', 'unspecified'].map((p) => ({ label: p, value: p })), { selected: [d.pronouns ?? 'unspecified'] }));
      return r;
    },
    ready: (d, env) => (d.name && !d.nearDup ? null : d.nearDup ? tx(env?.t, 'error-s3-near-dup', 'Confirm the similar name or pick another.') : tx(env?.t, 'error-s3-no-name', 'Set a name first.')),
    onSelect(key, v, d) { d.pronouns = v[0] === 'unspecified' ? null : v[0]; return {}; },
    onButton(key, d, env) {
      if (key === 'anyway') { d.name = d.nearDup.name; d.nearDup = null; return {}; }
      return { modal: modal(cid(d.uid, 'S3', 'm', 'name'), tx(env?.t, 'modal-s3-name', 'Crawler name'), [{ id: 'name', label: tx(env?.t, 'field-s3-name', 'Name (2-30 characters)'), max: 30, min: 2, value: d.name }]) };
    },
    onModal(key, f, d, env) {
      const raw = String(f.get('name') ?? '').replace(/\s+/g, ' ').trim();
      if (raw.length < 2 || raw.length > 30 || !NAME_RE.test(raw) || RESERVED.has(raw.toLowerCase())) return { notice: tx(env.t, 'error-s3-bad-name', 'That name will not work. Use 2-30 letters, digits, spaces, apostrophes, hyphens or periods, and not a reserved word.') };
      const taken = takenNames(env.config, d.uid);
      if (taken.some((n) => n.toLowerCase() === raw.toLowerCase())) return { notice: line(env.t, 'taken', d.uid) };
      const other = nearDuplicate(raw, taken);
      d.nearDup = other ? { name: raw, other } : null;
      if (!other) d.name = raw;
      return {};
    },
  },

  // ------------------------------------------------------------------ S4
  S4: {
    title: 'Look and hook',
    describe: (d) => `**Look:** ${d.look ?? '-'}\n**Hook:** ${d.hook ?? '-'}\nBoth required, 160 characters each, no links. Everyone reads as baseline human on Floors 1-2, so keep species features out of the look (or call it a costume).`,
    rows: (d, env) => [row(button(cid(d.uid, 'S4', 'edit'), d.look ? tx(env?.t, 'button-s4-edit', 'Edit look and hook') : tx(env?.t, 'button-s4-write', 'Write look and hook'), { style: ButtonStyle.Primary }))],
    ready: (d, env) => (d.look && d.hook ? null : tx(env?.t, 'error-s4-both', 'Both lines are required.')),
    onButton: (key, d, env) => ({ modal: modal(cid(d.uid, 'S4', 'm', 'edit'), tx(env?.t, 'title-s4', 'Look and hook'), [
      { id: 'look', label: 'What you look like right now', max: 160, value: d.look },
      { id: 'hook', label: 'Why you are still funny or dangerous', max: 160, value: d.hook },
    ]) }),
    onModal(key, f, d) {
      const l = cleanText(f.get('look'), 160), h = cleanText(f.get('hook'), 160);
      if (l.error || h.error) return { notice: `Look/hook: ${l.error ?? h.error}.` };
      d.look = l.value; d.hook = h.value;
      return /\b(horns?|tail|scales?|wings?)\b/i.test(d.look) ? { notice: 'Saved. Note: species features stay hidden on Floors 1-2; keep that as a costume if you like.' } : {};
    },
  },

  // ------------------------------------------------------------------ S5
  S5: {
    title: 'Species (Latent Biology)',
    pick: true,
    describe(d, env) {
      const sp = R.speciesInfo(d, env.t);
      const base = 'You look human on Floors 1-2; the traits get filed as quirks.\n*Floor 3: the System will offer you a rebuild. Optional. It\'s in the Terms.*';
      return sp ? `${base}\n\n**${speciesLabel(env.t, d.species)}** (${sp.size}, speed ${sp.speed} ft): ${sp.traits.join('; ')}.\n*${sp.quirk}*${sp.sub ? `\n**${sp.sub.label}:** ${d.speciesSub ? lineageLabel(env.t, d.species, d.speciesSub) : '(pick below)'}` : ''}` : base;
    },
    rows(d, env) {
      const r = [select(cid(d.uid, 'S5', 'species'), 'Pick your Latent Biology', Object.entries(env.t.chargen.species).map(([n, s]) => ({ label: speciesLabel(env.t, n), value: n, description: s.traits.slice(0, 3).join(', ') })), { selected: [d.species] })];
      const sub = R.speciesInfo(d, env.t)?.sub;
      if (sub) r.push(select(cid(d.uid, 'S5', 'sub'), sub.label, sub.options.map((o) => ({ label: lineageLabel(env.t, d.species, o), value: o })), { selected: [d.speciesSub] }));
      return r;
    },
    ready(d, env) {
      const sub = R.speciesInfo(d, env.t)?.sub;
      return d.species && (!sub || sub.options.includes(d.speciesSub)) ? null : 'Pick a species (and its sub-choice).';
    },
    onSelect(key, v, d, env) {
      if (key === 'species') { d.species = v[0]; d.speciesSub = null; return { notice: revalNotice(d, env.t) }; }
      d.speciesSub = v[0];
      return {};
    },
  },

  // ------------------------------------------------------------------ S6
  S6: {
    title: 'Class (Provisional Class)',
    pick: true,
    describe(d, env) {
      const c = R.classInfo(d, env.t);
      return c ? `**${classLabel(env.t, d.class)}** (d${c.hit_die}; saves ${c.saves.map(A).join('/')}): ${c.features.join('; ')}.\n*${c.kiosk}*` : 'Level 1 only. No multiclassing; we don\'t have the forms.';
    },
    rows(d, env) {
      const r = [select(cid(d.uid, 'S6', 'class'), 'Pick your Provisional Class', Object.values(env.t.chargen.classes).map((c) => ({ label: classLabel(env.t, c.name), value: c.name, description: `d${c.hit_die} · ${c.features[0]}` })), { selected: [d.class] })];
      for (const ch of R.classInfo(d, env.t)?.choices?.filter((x) => x.options && x.key !== 'weapon_masteries') ?? []) {
        r.push(select(cid(d.uid, 'S6', 'choice', ch.key), `${txd(env.t, CHOICE_IDS[ch.key], ch.label)}: ${ch.help}`, ch.options.map((o) => ({ label: BRANCH_CHOICES.has(ch.key) ? classOptionLabel(env.t, d.class, o) : optionLabel(env.t, ch, o), value: o })), { selected: [d.classChoices?.[ch.key]] }));
      }
      return r;
    },
    ready(d, env) {
      const c = R.classInfo(d, env.t);
      if (!c) return 'Pick a class.';
      return c.choices.filter((x) => x.options && x.key !== 'weapon_masteries').every((x) => x.options.includes(d.classChoices?.[x.key])) ? null : 'Make your class choice.';
    },
    onSelect(key, v, d, env, arg) {
      if (key === 'class') { d.class = v[0]; return { notice: revalNotice(d, env.t) }; }
      d.classChoices = { ...(d.classChoices ?? {}), [arg]: v[0] };
      return {};
    },
  },

  // ------------------------------------------------------------------ S7
  S7: {
    title: 'Background (Prior Employment) and Origin feat',
    pick: true,
    describe(d, env) {
      const bg = R.bgInfo(d, env.t);
      if (!bg) return `${env.settings.contentSource === 'srd' ? 'SRD backgrounds only.' : '2024 PHB backgrounds.'} Reskin the *reason* you have the skills, never the skills.`;
      const b = R.asiBonus(d, env.t);
      const asi = d.asi ? ABILITIES.filter((a) => b[a]).map((a) => `${A(a)} +${b[a]}`).join(', ') : '(choose below)';
      const fl = backgroundFlavor(env.t, d.background);
      return `**${backgroundLabel(env.t, d.background)}** - ${fl ? `${fl}\n` : ''}scores ${bg.asi.map(A).join('/')}; Origin feat **${featLabel(env.t, bg.feat)}**; skills ${bg.skills.join(', ')}; tool ${bg.tool}.\n**Bonus:** ${asi}  |  no score above 20${R.extraFeatNeeded(d, env.t) ? `\n**Human Versatile feat:** ${d.extraFeat ? featLabel(env.t, d.extraFeat) : '(pick below)'}` : ''}${R.lessonsFeatOffered(d, env.t) ? `\n**Lessons of the First Ones feat:** ${d.lessonsFeat ? featLabel(env.t, d.lessonsFeat) : 'not chosen yet (pick below, or leave it and the card will say pick one)'}` : ''}`;
    },
    rows(d, env) {
      const r = [select(cid(d.uid, 'S7', 'bg'), 'Pick your Prior Employment', backgroundNames(env.t, env.settings.contentSource).map((n) => { const b = env.t.chargen.backgrounds[n]; return { label: backgroundLabel(env.t, n), value: n, description: `${b.asi.map(A).join('/')} · ${b.feat} · ${b.skills.join(', ')}` }; }), { selected: [d.background] })];
      const bg = R.bgInfo(d, env.t);
      if (bg) {
        const o = [];
        for (const p2 of bg.asi) for (const p1 of bg.asi) if (p1 !== p2) o.push({ label: asiLabel(env.t, '2-1', `+2 ${A(p2)} / +1 ${A(p1)}`), value: `2-1:${p2}:${p1}`, description: asiFlavor(env.t, '2-1', 100) });
        o.push({ label: asiLabel(env.t, '1-1-1', `+1 ${bg.asi.map(A).join(' / +1 ')}`), value: '1-1-1', description: asiFlavor(env.t, '1-1-1', 100) });
        const cur = d.asi ? (d.asi.type === '1-1-1' ? '1-1-1' : `2-1:${d.asi.plus2}:${d.asi.plus1}`) : null;
        r.push(select(cid(d.uid, 'S7', 'asi'), 'How the background raises your scores', o, { selected: [cur] }));
        if (R.extraFeatNeeded(d, env.t)) r.push(select(cid(d.uid, 'S7', 'feat'), 'Human Versatile: pick an extra Origin feat', env.t.chargen.origin_feats.filter((f) => f !== bg.feat).map((f) => ({ label: featLabel(env.t, f), value: f, description: featFlavor(env.t, f, 100) })), { selected: [d.extraFeat] }));
        if (R.lessonsFeatOffered(d, env.t)) r.push(select(cid(d.uid, 'S7', 'lessons'), 'Lessons of the First Ones: pick an Origin feat (optional)', R.lessonsFeatOptions(d, env.t).map((f) => ({ label: featLabel(env.t, f), value: f, description: featFlavor(env.t, f, 100) })), { selected: [d.lessonsFeat] }));
      }
      return r;
    },
    ready(d, env) {
      return d.background && d.asi && (!R.extraFeatNeeded(d, env.t) || d.extraFeat) ? null : 'Pick a background, the score bonus' + (R.extraFeatNeeded(d, env.t) ? ' and your extra feat.' : '.');
    },
    onSelect(key, v, d, env) {
      if (key === 'bg') { d.background = v[0]; return { notice: revalNotice(d, env.t) }; }
      if (key === 'asi') { const [t_, p2, p1] = v[0].split(':'); d.asi = t_ === '1-1-1' ? { type: '1-1-1' } : { type: '2-1', plus2: p2, plus1: p1 }; return {}; }
      if (key === 'lessons') { d.lessonsFeat = v[0] ?? null; return { notice: revalNotice(d, env.t) }; }
      d.extraFeat = v[0];
      return {};
    },
  },

  // ------------------------------------------------------------------ S8
  S8: {
    title: 'Ability scores',
    pick: true,
    paged: true,
    describe(d, env) {
      const s = env.settings;
      const m = effMethod(d, env);
      const head = `${tx(env.t, 'hint-s8-methods-head', `Methods: standard array (${env.t.chargen.standard_array.join(', ')}) or point buy (${env.t.chargen.point_buy.budget} points; scores 8-15 before bonuses). The background bonus is added after.`, { array: env.t.chargen.standard_array.join(', '), budget: env.t.chargen.point_buy.budget })}${s.allowRoll ? `\n${line(env.t, 'S8_roll_offer', d.uid)}` : ''}`;
      if (!m) return head;
      let out = tx(env.t, 'hint-s8-method-line', `**Method:** ${m === 'roll' ? 'Roll' : m}.`, { method: m === 'roll' ? 'Roll' : m, method_label: txd(env.t, METHOD_IDS[m], METHOD_PLAIN[m]) });
      if (m !== 'roll') {
        out += ` ${tx(env.t, 'hint-s8-enter-order', 'Enter six numbers in the order STR DEX CON INT WIS CHA.')}`;
        if (m === 'pointbuy' && d.base) out += `  ${tx(env.t, 'hint-s8-points-used', `Points used: ${R.pointBuyCost(d.base, env.t) ?? '?'} of ${env.t.chargen.point_buy.budget}.`, { used: R.pointBuyCost(d.base, env.t) ?? '?', budget: env.t.chargen.point_buy.budget })}`;
      } else out += `\n${rollText(d, env)}`;
      return `${head}\n${out}${d.base ? '\n' + (R.bgInfo(d, env.t) && d.asi ? previewTable(d, env.t) : tx(env.t, 'hint-s8-base-line', `Base: ${ABILITIES.map((a) => `${A(a)} ${d.base[a]}`).join(' ')} (choose your background bonus on S7 to see finals)`, { scores: ABILITIES.map((a) => `${A(a)} ${d.base[a]}`).join(' ') })) : ''}`;
    },
    allRows(d, env) {
      const m = effMethod(d, env);
      const methods = [button(cid(d.uid, 'S8', 'array'), txd(env.t, METHOD_IDS.array, 'Standard array'), { style: m === 'array' ? ButtonStyle.Primary : ButtonStyle.Secondary }), button(cid(d.uid, 'S8', 'pointbuy'), txd(env.t, METHOD_IDS.pointbuy, 'Point buy'), { style: m === 'pointbuy' ? ButtonStyle.Primary : ButtonStyle.Secondary })];
      if (env.settings.allowRoll) methods.push(button(cid(d.uid, 'S8', 'roll'), txd(env.t, METHOD_IDS.roll, 'Roll'), { style: m === 'roll' ? ButtonStyle.Primary : ButtonStyle.Secondary }));
      const r = [row(...methods)];
      if (m === 'roll') {
        const last = rollRounds(d).at(-1);
        if (last?.qualified) {
          const kept = d.scoreRolls?.kept;
          r.push(row(...last.arrays.map((a) => button(cid(d.uid, 'S8', `keep${a.id}`), tx(env.t, 'button-s8-keep', `Keep ${a.id}`, { id: a.id }), { disabled: !a.keepable, style: kept?.array === a.id && kept?.round === last.round ? ButtonStyle.Success : ButtonStyle.Secondary }))));
          // after a keep: one select per ability, each of the six scores used once (paged, three rows per page; the method and keep buttons are on the first page)
          if (kept?.array === undefined) return r;
          const arr = last.arrays.find((a) => a.id === kept.array);
          if (arr?.keepable) return [...r, ...assignRows(d, arr, env.t)];
        }
      } else if (m) r.push(row(button(cid(d.uid, 'S8', 'enter'), tx(env.t, 'button-s8-enter-scores', 'Enter scores'), { style: ButtonStyle.Primary })));
      return r;
    },
    ready(d, env) {
      if (d.method === 'roll' && !env.settings.allowRoll) return tx(env.t, 'notice-s8-pick-method', 'Pick a method first.');
      return d.base && !R.validateBase(d, env.t) ? null : tx(env.t, 'notice-s8-set-scores', 'Set legal ability scores first.');
    },
    async onButton(key, d, env) {
      if (['array', 'pointbuy'].includes(key)) { d.method = key; d.base = null; return {}; }
      if (key === 'roll' || /^keep[ABC]$/.test(key)) {
        if (!env.settings.allowRoll) { if (d.method === 'roll') { d.method = null; d.base = null; } return { notice: line(env.t, 'S8_roll_closed', d.uid) }; }
        if (key === 'roll') return rollMethod(d, env);
        const last = rollRounds(d).at(-1);
        const arr = last?.arrays.find((a) => a.id === key.slice(4));
        if (!arr) return { notice: tx(env.t, 'notice-s8-roll-three', 'Roll your three arrays first.') };
        if (!arr.keepable) return { notice: line(env.t, 'S8_roll_keep_no', d.uid, { total: arr.total }) };
        if (d.scoreRolls.kept?.array !== arr.id || d.scoreRolls.kept?.round !== last.round) { d.scoreRolls.kept = { round: last.round, array: arr.id }; d.rollAssign = {}; d.base = null; }
        d.method = 'roll';
        return { notice: line(env.t, 'S8_roll_assign', d.uid) };
      }
      const cur = d.base ? ABILITIES.map((a) => d.base[a]).join(' ') : d.method === 'array' ? ABILITIES.map((a) => R.pickArray(d, env.t)[a]).join(' ') : '';
      return { modal: modal(cid(d.uid, 'S8', 'm', 'scores'), tx(env.t, 'title-s8', 'Ability scores'), [{ id: 'scores', label: 'STR DEX CON INT WIS CHA', max: 40, value: cur, placeholder: 'e.g. 15 8 14 10 12 13' }]) };
    },
    onSelect(key, v, d, env, ability) {
      if (key !== 'assign' || !ABILITIES.includes(ability)) return {};
      if (!env.settings.allowRoll) return { notice: line(env.t, 'S8_roll_closed', d.uid) };
      const c = R.checkRolls(d.scoreRolls, env.t);
      if (c.error || d.method !== 'roll') return { notice: c.error ?? tx(env.t, 'notice-s8-pick-roll', 'Pick Roll first.') };
      const idx = Number(v[0]);
      const as = (d.rollAssign ??= {});
      if (!Number.isInteger(idx) || idx < 0 || idx > 5 || ABILITIES.some((a) => a !== ability && as[a] === idx)) return { notice: tx(env.t, 'notice-s8-once-each', 'Each score goes to one ability, once.') };
      as[ability] = idx;
      d.base = ABILITIES.every((a) => Number.isInteger(as[a])) ? Object.fromEntries(ABILITIES.map((a) => [a, c.scores[as[a]]])) : null;
      return {};
    },
    onModal(key, f, d, env) {
      if (effMethod(d, env) === 'roll') return { notice: tx(env.t, 'notice-s8-menus-only', 'Roll scores are assigned with the menus, not typed.') };
      const p = R.parseScores(f.get('scores'), env.t);
      if (p.error) return { notice: p.error };
      const keep = d.base;
      d.base = p.base;
      const e = R.validateBase(d, env.t);
      if (e) { d.base = keep; return { notice: e }; }
      return {};
    },
  },

  // ------------------------------------------------------------------ S9
  S9: {
    title: 'Skills and proficiencies',
    pick: true,
    paged: true,
    describe(d, env) {
      const c = R.classInfo(d, env.t);
      if (!c || !d.background) return tx(env.t, 'notice-s9-need-class-bg', 'Pick a class and background first (screens 6 and 7).');
      return `**Fixed:** skills ${R.fixedSkills(d, env.t).join(', ')}; tool ${R.toolsList(d, env.t).join(', ')}; saves ${c.saves.map(A).join('/')}; armor ${c.armor.join(', ') || 'none'}; Proficiency Bonus +${R.PB}.\n**Picks so far:** class skills ${list(d.classSkills)}${d.speciesSkill ? `; species skill ${d.speciesSkill}` : ''}${d.featSkills?.length ? `; Skilled ${list(d.featSkills)}` : ''}; languages Common + ${list(d.languages)}${d.expertise?.length ? `; Expertise ${list(d.expertise)}` : ''}${d.masteries?.length ? `; masteries ${d.masteries.map((m) => R.itemLabel(m, env.t)).join(', ')}` : ''}`;
    },
    allRows(d, env) {
      const c = R.classInfo(d, env.t);
      if (!c || !d.background) return [];
      const r = [];
      const ms = (k, ph, opts, n, sel) => r.push(select(cid(d.uid, 'S9', k), ph, opts.map((o) => (typeof o === 'string' ? { label: o, value: o } : o)), { min: n, max: n, selected: sel ?? [] }));
      ms('cskills', tx(env.t, 'select-s9-class-skills', `Class skills: pick ${c.skill_count}`, { n: c.skill_count }), R.classSkillOptions(d, env.t), c.skill_count, d.classSkills);
      const so = R.speciesSkillOptions(d, env.t);
      if (so) ms('sskill', `${so.label}: pick 1`, so.options, 1, [d.speciesSkill]);
      if (R.featSkillCount(d, env.t)) ms('fskills', tx(env.t, 'select-s9-skilled', `Skilled feat: pick ${R.featSkillCount(d, env.t)} skills`, { n: R.featSkillCount(d, env.t) }), R.featSkillOptions(d, env.t), R.featSkillCount(d, env.t), d.featSkills);
      ms('langs', tx(env.t, 'select-s9-languages', `Languages: pick ${env.t.chargen.languages.pick} (plus Common)`, { n: env.t.chargen.languages.pick }), R.languageOptions(d, env.t), env.t.chargen.languages.pick, d.languages);
      const ex = c.choices.find((x) => x.key === 'expertise');
      if (ex) ms('exp', `${tx(env.t, 'choice-expertise', 'Expertise')}: pick ${ex.count}`, R.expertiseOptions(d, env.t), ex.count, d.expertise);
      const mc = R.masteryChoice(d, env.t);
      if (mc) ms('mast', `${tx(env.t, 'choice-weapon-masteries', 'Weapon Mastery')}: pick ${mc.count}${d.masteriesAuto ? ' (preset: weapons you carry)' : ''}`, mc.options.map((id) => ({ label: R.itemLabel(id, env.t), value: id, description: env.t.chargen.items[id].weapon.mastery ? `Mastery: ${env.t.chargen.items[id].weapon.mastery}` : '' })), mc.count, d.masteries);
      return r;
    },
    ready(d, env) {
      const e = R.validateDraft({ ...d, name: 'x', look: 'x', hook: 'x', backstory: 'x', orders: 'x' }, env.t).filter((x) => x.screen === 'S9');
      return e.length ? e[0].msg : null;
    },
    onSelect(key, v, d, env) {
      const map = { cskills: 'classSkills', sskill: null, fskills: 'featSkills', langs: 'languages', exp: 'expertise', mast: 'masteries' };
      if (key === 'sskill') d.speciesSkill = v[0];
      else d[map[key]] = v;
      if (key === 'mast') d.masteriesAuto = false;   // the player's own picks: never re-defaulted
      if (['cskills', 'sskill', 'fskills'].includes(key)) {
        const dr = revalidate(d, env.t).filter((x) => x !== 'class skills' || key !== 'cskills');
        return { notice: dr.length ? `${tx(env.t, 'notice-s9-dropped', `Dropped picks that stopped being legal: ${dr.join(', ')}`, { list: dr.join(', ') })}.` : '' };
      }
      return {};
    },
  },

  // ------------------------------------------------------------------ S10
  S10: {
    title: 'Starting equipment',
    pick: true,
    describe(d, env) {
      if (!d.class || !d.background) return tx(env.t, 'notice-s10-need-class-bg', 'Pick a class and background first.');
      const left = R.creditsLeft(d, env.t);
      const dv = d.base && d.asi ? R.derived(d, env.t) : null;
      return `${money(tx(env.t, 'hint-s10-describe', `Take each package or its gold. Everything is junk; everything works. **Credits:** ${R.creditsFromPackages(d, env.t)} from options, ${R.cartTotal(d, env.t)} spent at the Intake Vending Wall, **${left} left**.`, { from_options: R.creditsFromPackages(d, env.t), spent: R.cartTotal(d, env.t), left }))}${dv ? `  **AC ${dv.ac}**` : ''}\n${d.kitClass && d.kitBg ? kitText(d, env.t) : ''}`;
    },
    rows(d, env) {
      const c = R.classInfo(d, env.t), b = R.bgInfo(d, env.t);
      if (!c || !b) return [];
      return [
        select(cid(d.uid, 'S10', 'kc'), ownerKit(env.t, classLabel(env.t, d.class)), optionsFromPackages(c, env.t, d, 'class'), { selected: [d.kitClass] }),
        select(cid(d.uid, 'S10', 'kb'), ownerKit(env.t, backgroundLabel(env.t, d.background)), optionsFromPackages(b, env.t, d, 'background'), { selected: [d.kitBg] }),
        row(button(cid(d.uid, 'S10', 'shop'), tx(env.t, 'button-s10-shop', 'Vending Wall (buy)'), { style: ButtonStyle.Primary, disabled: !(d.kitClass && d.kitBg) }), button(cid(d.uid, 'S10', 'prices'), tx(env.t, 'button-s10-prices', 'Price list')), button(cid(d.uid, 'S10', 'clear'), tx(env.t, 'button-s10-clear', 'Clear shopping'), { disabled: !(d.cart ?? []).length })),
        // one variant pick at a time (Discord allows 5 rows: 2 package menus + buttons + this + nav); unpicked types show first, so a second one appears after the first is chosen
        ...[...R.pendingVariants(d, env.t)].sort((a, b) => (a.chosen && a.options.includes(a.chosen) ? 1 : 0) - (b.chosen && b.options.includes(b.chosen) ? 1 : 0)).slice(0, 1).map((v) => select(cid(d.uid, 'S10', 'var', `${v.src}~${v.id}`), tx(env.t, 'hint-s10-variant', `Pick your ${env.t.chargen.items[v.id].name.replace(/ \(your choice\)/, '')} (${v.src} package)`, { item: env.t.chargen.items[v.id].name.replace(/ \(your choice\)/, ''), src: v.src }),
          v.options.map((o) => ({ label: K.labelFor(env.t, o), value: o, description: `${K.plainName(env.t, o)} - ${priceText(env.t, K.priceCp(env.t, o, v.id))}` })), { selected: v.chosen ? [v.chosen] : [] })),
      ];
    },
    ready(d, env) {
      if (!(d.kitClass && d.kitBg)) return money(tx(env.t, 'error-s10-pick-both', 'Pick both equipment options (and do not overspend).'));
      if (R.pendingVariants(d, env.t).some((v) => !v.chosen || !v.options.includes(v.chosen))) return tx(env.t, 'error-s10-pick-type', 'Pick the type of each item that says "pick type" (holy symbol, gaming set, instrument, tools).');
      return R.creditsLeft(d, env.t) >= 0 ? null : money(tx(env.t, 'error-s10-pick-both', 'Pick both equipment options (and do not overspend).'));
    },
    onSelect(key, v, d, env, arg) {
      if (key === 'var') {
        const [src, id] = String(arg).split('~');
        const want = R.pendingVariants(d, env.t).find((x) => x.src === src && x.id === id);
        if (!want || !want.options.includes(v[0])) return { notice: tx(env.t, 'notice-s10-type-na', 'That type is not available for this item.') };
        (d.variants ??= {})[`${src}:${id}`] = v[0];
        return {};
      }
      if (key === 'kc') d.kitClass = v[0]; else d.kitBg = v[0];
      revalidate(d, env.t);
      if (R.creditsLeft(d, env.t) < 0) { d.cart = []; return { notice: tx(env.t, 'notice-s10-cart-cleared', 'Your shopping list was cleared (it no longer fit).') }; }
      return {};
    },
    onButton(key, d, env) {
      if (key === 'clear') { d.cart = []; return {}; }
      if (key === 'prices') {
        const groups = { Weapons: [], Armor: [], 'Other gear': [] };
        // every price comes from the item's own srd_id (the variant's base_price_cp); a header is not listed - its variants are
        const mult = K.floorMultiplier(d.floor ?? 1);
        const shown = (id, srd) => `${K.labelFor(env.t, srd, env.t.chargen.items[id]?.name)} ${priceText(env.t, (K.priceCp(env.t, srd, id) ?? 0) * mult)}`;
        for (const [id, it] of Object.entries(env.t.chargen.items)) {
          const bucket = groups[priceBucket(it.category)];
          if (K.isHeaderKey(env.t, id)) { for (const v of K.variantIds(env.t, id)) if (K.priceCp(env.t, v, id) !== null) bucket.push(shown(id, v)); continue; }
          if (K.priceCp(env.t, K.itemSrdId(env.t, id), id) !== null) bucket.push(shown(id, K.itemSrdId(env.t, id)));
        }
        return { followup: ['Weapons', 'Armor', 'Other gear'].flatMap((header) => chunkPriceList(header, groups[header])) };
      }
      if (key === 'shop') {
        const cur = (d.cart ?? []).map((l) => `${K.plainName(env.t, R.lineSrdId(l, env.t), env.t.chargen.items[l.id].name)} ${l.qty}`).join('\n');
        return { modal: modal(cid(d.uid, 'S10', 'm', 'shop'), 'Intake Vending Wall', [{ id: 'list', label: `One per line: name, then quantity (${R.creditsLeft({ ...d, cart: [] }, env.t)} credits)`, style: 'paragraph', required: false, max: 1000, value: cur, placeholder: 'Rations 12\nRope\nHealer\'s Kit' }]) };
      }
      const cur = R.kitItems(d, env.t).map((k) => `${env.t.chargen.items[k.id].name} = ${d.junk?.[k.id] ?? env.t.chargen.items[k.id].junk}`).join('\n');
      return { modal: modal(cid(d.uid, 'S10', 'm', 'rename'), 'Rename your junk', [{ id: 'list', label: 'Real item = junk name (60 chars max)', style: 'paragraph', required: false, max: 3000, value: cur.slice(0, 3000) }]) };
    },
    onModal(key, f, d, env) {
      const text = String(f.get('list') ?? '');
      const errs = [];
      const heads = [];
      const classOnly = [];
      const cart = new Map();
      for (const raw of text.split('\n').map((x) => x.trim()).filter(Boolean)) {
        const m = raw.match(/^(.*?)(?:\s*[x×]?\s*(\d+))?$/i);
        const hit = findPurchase(m[1] || raw, env.t);
        const q = m[2] ? Number(m[2]) : 1;
        if (hit?.header) { heads.push(env.t.chargen.items[hit.header].name.replace(/ \(your choice\)/, '')); continue; }
        if (!hit || q < 1 || q > 99) { errs.push(`"${cut(raw, 30)}"`); continue; }
        if (!R.itemAllowed(d, env.t, hit.id)) { classOnly.push(`${env.t.chargen.items[hit.id].name} (${R.itemClasses(hit.id, env.t).join('/')} only)`); continue; }
        const k = `${hit.id}|${hit.variant ?? ''}`;
        cart.set(k, { id: hit.id, qty: (cart.get(k)?.qty ?? 0) + q, ...(hit.variant ? { variant: hit.variant } : {}) });
      }
      const next = { ...d, cart: [...cart.values()] };
      if (R.creditsLeft(next, env.t) < 0) return { notice: tx(env.t, 'notice-s10-overspend', `That costs ${R.cartTotal(next, env.t)} credits but you have ${R.creditsFromPackages(d, env.t)}. Nothing was bought.`, { cost: R.cartTotal(next, env.t), have: R.creditsFromPackages(d, env.t) }) };
      d.cart = next.cart;
      const bits = [];
      if (errs.length) bits.push(`${tx(env.t, 'notice-s10-not-on-wall', `Not on the Wall: ${errs.join(', ')}`, { names: errs.join(', ') })}.`);
      if (classOnly.length) bits.push(`Not for your class: ${classOnly.join(', ')}. Nothing of that was bought.`);
      if (heads.length) bits.push(tx(env.t, 'notice-s10-say-type', `Say which type: ${heads.map((h) => `${h} (see the price list)`).join(', ')}. A generic is never sold.`, { names: heads.map((h) => `${h} (see the price list)`).join(', ') }));
      return { notice: bits.join(' ') };
    },
  },

  // ------------------------------------------------------------------ S11
  S11: {
    title: 'Spells',
    pick: true,
    paged: true,
    describe(d, env) {
      const sp = R.spellInfo(d, env.t);
      const mi = miText(d, env.t);
      if (!sp) return mi || tx(env.t, 'notice-s11-none', 'No spells for this class.');
      const s = d.spells ?? {};
      return `**${classLabel(env.t, d.class)}** (${A(sp.ability)}): ${R.cantripCount(d, env.t)} cantrips${sp.spellbook ? `, ${sp.spellbook} spellbook spells, prepare ${sp.prepared}` : sp.level1_known ? `, ${sp.level1_known} level 1 spells` : ''}; ${sp.slots_l1} level 1 slot(s).\n**Cantrips:** ${list(s.cantrips)}\n**Level 1:** ${list(s.level1)}${sp.spellbook ? `\n**Prepared:** ${list(s.prepared)}` : ''}\n*Pick (effect lines are in the menus).*${mi ? `\n${mi}` : ''}`;
    },
    allRows(d, env) {
      const sp = R.spellInfo(d, env.t);
      const opt = (n) => ({ label: n, value: n, description: `${env.t.chargen.spells[n].school}: ${env.t.chargen.spells[n].effect}` });
      const miRows = R.miFeats(d, env.t).flatMap((f, i) => {
        const L = R.miLists(f, env.t);
        if (!L) return [];
        const m = d.mi?.[f] ?? {};
        const cls = R.miClass(f);
        return [
          select(cid(d.uid, 'S11', 'mic', i), `${f}: pick 2 ${cls} cantrips (optional)`, L.cantrips.slice(0, 25).map(opt), { min: 0, max: Math.min(2, L.cantrips.length), selected: m.cantrips ?? [] }),
          ...[L.level1.slice(0, 25), L.level1.slice(25)].filter((c) => c.length).map((c, j, all) => select(cid(d.uid, 'S11', 'mil', `${i}~${j}`), `${f}: pick 1 level 1 ${cls} spell (optional)${all.length > 1 ? ` (list ${j + 1}/${all.length})` : ''}`, c.map(opt), { min: 0, max: 1, selected: (m.level1 ?? []).filter((x) => c.includes(x)) })),
          select(cid(d.uid, 'S11', 'mia', i), `${f}: spellcasting ability (optional)`, R.MI_ABILITIES.map((a) => ({ label: A(a), value: a })), { min: 0, max: 1, selected: m.ability ? [m.ability] : [] }),
        ];
      });
      if (!sp) return miRows;
      const s = d.spells ?? {};
      const r = [];
      const nc = R.cantripCount(d, env.t);
      if (nc) r.push(select(cid(d.uid, 'S11', 'can'), tx(env.t, 'select-s11-cantrips', `Cantrips: pick ${nc}`, { n: nc }), sp.cantrip_list.map(opt), { min: nc, max: nc, selected: s.cantrips ?? [] }));
      const n1 = sp.spellbook ?? sp.level1_known;
      const chunks = [sp.level1_list.slice(0, 25), sp.level1_list.slice(25)].filter((c) => c.length);
      const picked = s.level1 ?? [];
      chunks.forEach((c, i) => r.push(select(cid(d.uid, 'S11', 'l1', i), `${tx(env.t, sp.spellbook ? 'select-s11-spellbook' : 'select-s11-level1', `Level 1 ${sp.spellbook ? 'spellbook' : 'spells'}: pick ${n1} in total`, { n: n1 })}${chunks.length > 1 ? ` (list ${i + 1}/${chunks.length})` : ''}`, c.map(opt), { min: 0, max: Math.min(n1, c.length), selected: picked.filter((x) => c.includes(x)) })));
      if (sp.spellbook) r.push(select(cid(d.uid, 'S11', 'prep'), tx(env.t, 'select-s11-prepare', `Prepare ${sp.prepared} from your spellbook`, { n: sp.prepared }), (s.level1 ?? []).length ? s.level1.map(opt) : [{ label: tx(env.t, 'hint-s11-pick-book-first', 'Pick spellbook spells first'), value: '-' }], { min: (s.level1 ?? []).length ? sp.prepared : 1, max: (s.level1 ?? []).length ? sp.prepared : 1, selected: s.prepared ?? [] }));
      return [...r, ...miRows];   // Magic Initiate picks last (paged)
    },
    ready(d, env) {
      const e = R.validateDraft({ ...d, name: 'x', look: 'x', hook: 'x', backstory: 'x', orders: 'x' }, env.t).filter((x) => x.screen === 'S11');
      return e.length ? e[0].msg : null;
    },
    onSelect(key, v, d, env, arg) {
      if (['mic', 'mil', 'mia'].includes(key)) {   // Magic Initiate picks (optional; never auto-picked)
        const [fi, chunk] = String(arg).split('~').map(Number);
        const f = R.miFeats(d, env.t)[fi];
        const L = f ? R.miLists(f, env.t) : null;
        if (!L) return {};
        const m = ((d.mi ??= {})[f] ??= { ability: null, cantrips: [], level1: [] });
        if (key === 'mic') m.cantrips = v.filter((x) => L.cantrips.includes(x)).slice(0, 2);
        else if (key === 'mia') m.ability = R.MI_ABILITIES.includes(v[0]) ? v[0] : null;
        else {
          const part = (chunk || 0) === 0 ? L.level1.slice(0, 25) : L.level1.slice(25);
          m.level1 = [...(m.level1 ?? []).filter((x) => !part.includes(x)), ...v.filter((x) => part.includes(x))].slice(-1);
        }
        return {};
      }
      d.spells = d.spells ?? { cantrips: [], level1: [], prepared: [] };
      if (key === 'can') d.spells.cantrips = v;
      else if (key === 'prep') d.spells.prepared = v.filter((x) => x !== '-');
      else {
        const sp = R.spellInfo(d, env.t);
        const chunk = Number(arg) === 0 ? sp.level1_list.slice(0, 25) : sp.level1_list.slice(25);
        d.spells.level1 = [...d.spells.level1.filter((x) => !chunk.includes(x)), ...v];
        d.spells.prepared = d.spells.prepared.filter((x) => d.spells.level1.includes(x));
        if (d.spells.level1.length > (sp.spellbook ?? sp.level1_known)) return { notice: tx(env.t, 'notice-s11-too-many', `Too many level 1 spells (${d.spells.level1.length}). Trim the other list.`, { n: d.spells.level1.length }) };
      }
      return {};
    },
  },

  // ------------------------------------------------------------------ S12 (retired: numbering kept, screen skipped)
  // Fan tags are no longer asked for. The GM reads the survey (S13); any tags live only in the GM-only fan profile and never on a card.
  S12: {
    title: 'Retired',
    describe: (d, env) => tx(env?.t, 'notice-s12-retired', 'This step is retired. Press Next.'),
    rows: () => [],
    ready: () => null,
  },

  // ------------------------------------------------------------------ S13
  S13: {
    title: 'Customer survey (private notes)',
    skippable: true,
    describe(d, env) {
      const qs = surveyQuestions(d, env.t);
      return `Your answers are private and will not be read aloud. Pass on any (blank = pass), one line each, 140 characters.\n${qs.map((q, i) => `${i + 1}. ${q.q}${d.survey?.[i]?.a ? ' ✔' : ''}`).join('\n')}`;
    },
    rows: (d, env) => [row(button(cid(d.uid, 'S13', 'a'), tx(env?.t, 'button-s13-first', 'Answer 1-5'), { style: ButtonStyle.Primary }), button(cid(d.uid, 'S13', 'b'), tx(env?.t, 'button-s13-second', 'Answer 6 and bonus')), button(cid(d.uid, 'S13', 'pass'), tx(env?.t, 'button-s13-pass', 'Pass on all')))],
    ready: () => null,
    onButton(key, d, env) {
      const qs = surveyQuestions(d, env.t);
      if (key === 'pass') { d.survey = qs.map((q) => ({ ...q, a: '' })); return { notice: 'Passed. A pass is data too.' }; }
      const slice = key === 'a' ? qs.slice(0, 5) : qs.slice(5);
      const off = key === 'a' ? 0 : 5;
      return { modal: modal(cid(d.uid, 'S13', 'm', key), 'Customer survey', slice.map((q, i) => ({ id: `q${off + i}`, label: cut(q.q, 45), required: false, max: 140, value: d.survey?.[off + i]?.a, placeholder: cut(q.q, 100) }))) };
    },
    onModal(key, f, d, env) {
      const qs = surveyQuestions(d, env.t);
      d.survey = d.survey?.length === qs.length ? d.survey : qs.map((q) => ({ ...q, a: '' }));
      const off = key === 'a' ? 0 : 5;
      const n = key === 'a' ? 5 : qs.length - 5;
      for (let i = 0; i < n; i++) {
        const raw = String(f.get(`q${off + i}`) ?? '').trim();
        const c = raw ? cleanText(raw, 140) : { value: '' };
        d.survey[off + i] = { ...qs[off + i], a: c.error ? '' : c.value };
      }
      return {};
    },
  },

  // ------------------------------------------------------------------ S14
  S14: {
    title: 'Backstory and requested handle',
    describe: (d) => `Two sentences, max 300 characters. **This is public**: the System reads it at your introduction.\nThen a Requested Handle (max 30, optional): a request, not a promise. Your Broadcast Name stays PENDING until Floor 3.\n**Backstory:** ${d.backstory ?? '-'}\n**Requested Handle:** ${d.handle ?? '(none)'}`,
    rows: (d, env) => [row(button(cid(d.uid, 'S14', 'edit'), d.backstory ? tx(env?.t, 'button-edit', 'Edit') : tx(env?.t, 'button-s14-write', 'Write backstory and handle'), { style: ButtonStyle.Primary }))],
    ready: (d, env) => (d.backstory ? null : tx(env?.t, 'error-s14-required', 'Backstory is required.')),
    onButton: (key, d, env) => ({ modal: modal(cid(d.uid, 'S14', 'm', 'edit'), tx(env?.t, 'modal-s14', 'Backstory and handle'), [
      { id: 'story', label: 'What you did before the crawl (public)', style: 'paragraph', max: 300, value: d.backstory },
      { id: 'handle', label: 'Requested Handle (optional)', required: false, max: 30, value: d.handle },
    ]) }),
    onModal(key, f, d, env) {
      const s = cleanText(f.get('story'), 300);
      if (s.error) return { notice: `Backstory: ${s.error}.` };
      const raw = String(f.get('handle') ?? '').trim();
      const h = raw ? cleanText(raw, 30) : { value: null };
      if (h.error) return { notice: `Handle: ${h.error}.` };
      if ((d.optouts ?? []).some((o) => o.topic.length > 1 && s.value.toLowerCase().includes(o.topic.toLowerCase()))) return { notice: tx(env.t, 'error-s14-words', 'Pick different words for the backstory.') };
      d.backstory = s.value; d.handle = h.value;
      return {};
    },
  },

  // ------------------------------------------------------------------ S15
  S15: {
    title: 'Standing Orders, Reactions, signature attack',
    describe(d, env) {
      const opts = [...(d.spells?.cantrips ?? []), ...(d.spells?.prepared ?? []), ...(d.masteries ?? []).map((m) => R.itemLabel(m, env.t))];
      return `**Orders** (required, max 200): what your body does while you are away; no orders = Dodge on timeout.\n**Reactions** (max 200): default "Opportunity Attacks: on".\n**Signature attack** (optional, max 40): names an attack or spell you actually have${opts.length ? ` (${list(opts.slice(0, 8))})` : ''}.\n**Orders:** ${d.orders ?? '-'}\n**Reactions:** ${d.reactions ?? 'Opportunity Attacks: on'}\n**Signature:** ${d.signature ?? '-'}`;
    },
    rows: (d, env) => [row(button(cid(d.uid, 'S15', 'edit'), d.orders ? tx(env?.t, 'button-edit', 'Edit') : tx(env?.t, 'button-s15-write', 'Write orders'), { style: ButtonStyle.Primary }))],
    ready: (d, env) => (d.orders ? null : tx(env?.t, 'error-s15-required', 'Standing Orders are required.')),
    onButton: (key, d, env) => ({ modal: modal(cid(d.uid, 'S15', 'm', 'edit'), tx(env?.t, 'modal-s15', 'Orders and reactions'), [
      { id: 'orders', label: 'Standing Orders', style: 'paragraph', max: 200, value: d.orders },
      { id: 'react', label: 'Standing Reactions', required: false, max: 200, value: d.reactions ?? 'Opportunity Attacks: on' },
      { id: 'sig', label: 'Signature attack name (optional)', required: false, max: 40, value: d.signature },
    ]) }),
    onModal(key, f, d) {
      const o = cleanText(f.get('orders'), 200);
      if (o.error) return { notice: `Orders: ${o.error}.` };
      const rRaw = String(f.get('react') ?? '').trim(), sRaw = String(f.get('sig') ?? '').trim();
      const r = rRaw ? cleanText(rRaw, 200) : { value: null }, s = sRaw ? cleanText(sRaw, 40) : { value: null };
      if (r.error || s.error) return { notice: `Reactions/signature: ${r.error ?? s.error}.` };
      d.orders = o.value; d.reactions = r.value; d.signature = s.value;
      return {};
    },
  },

  // ------------------------------------------------------------------ S16 (rendered by the flow: needs the card)
  S16: {
    title: 'Review (the full sheet)',
    review: true,
    describe: (d, env) => buildBlock(d, env.t),
    rows(d, env) {
      const errs = R.validateDraft(d, env.t, { partyCount: env.party.count, partyMax: env.party.max, benched: env.party.benched });
      const targets = ['S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', ...(R.isCaster(d, env.t) ? ['S11'] : []), 'S13', 'S14', 'S15'];
      return [
        select(cid(d.uid, 'S16', 'edit'), tx(env.t, 'select-s16-edit', 'Edit a screen…'), targets.map((s) => ({ label: `${s}: ${screenTitle(env.t, s)}`, value: s }))),
        row(button(cid(d.uid, 'S16', 'private'), tx(env.t, 'button-s16-private', 'Private notes (only you)')), button(cid(d.uid, 'S16', 'restart'), tx(env.t, 'button-restart', 'Restart'), { style: ButtonStyle.Danger })),
        ...(errs.length ? [] : []),
      ];
    },
    ready: (d, env) => { const e = R.validateDraft(d, env.t, { partyCount: env.party.count, partyMax: env.party.max, benched: env.party.benched }); return e.length ? tx(env.t, 'notice-fix-screen', `Fix ${e[0].screen}: ${e[0].msg}`, { screen: e[0].screen, msg: e[0].msg }) : null; },
    onSelect: (key, v) => ({ go: v[0], edit: true }),
    onButton(key, d, env) {
      if (key === 'restart') return { restart: true };
      const o = (d.optouts ?? []).map((x) => `${x.kind}: ${x.topic}${x.shared ? ' (shared with reviewer)' : ' (private)'}`);
      const sv = (d.survey ?? []).filter((x) => x.a).map((x) => `• ${x.q}\n  ${x.a}`);
      return { followup: `**Private (only you see this)**\n**Comfort:** ${o.join('; ') || 'none'}\n**Survey:**\n${sv.join('\n') || 'none'}` };
    },
  },

  // ------------------------------------------------------------------ S17
  S17: {
    title: 'Confirm',
    describe: (d, env) => `${line(env.t, 'S17', d.uid)}\n\n**${d.name}** - ${speciesLabel(env.t, d.species)} ${classLabel(env.t, d.class)} 1, ${d.background}.`,
    rows: (d, env) => [row(button(cid(d.uid, 'S17', 'confirm'), tx(env?.t, 'button-s17-confirm', 'Confirm and lock the file'), { style: ButtonStyle.Success }))],
    ready: () => null,
    onButton: (key) => ({ commit: true }),
  },
};

export function surveyQuestions(d, t) {
  const core = t.lines.survey.core.map((q) => ({ q }));
  const hasOpt = (d.optouts ?? []).length > 0;
  const pool = t.lines.survey.bonus_pool.filter((b) => !b.drop && !(b.drop_if_optouts && hasOpt));
  const h = [...String(d.uid)].reduce((s, ch) => (s * 31 + ch.charCodeAt(0)) >>> 0, 7);
  const picks = pool.length ? [pool[h % pool.length], pool[(h + 3) % pool.length]].filter((x, i, a) => a.indexOf(x) === i) : [];
  return [...core, ...picks.map((p, i) => ({ q: p.q, bonus: i + 1 }))];
}

/** S11 summary of each Magic Initiate's picks ("not chosen yet" until the player picks; nothing is ever picked for them). */
function miText(d, t) {
  return R.miFeats(d, t).map((f) => {
    const m = d.mi?.[f] ?? {};
    return `**${f}:** cantrips ${list(m.cantrips)}; level 1 ${list(m.level1)}; ability ${m.ability ? A(m.ability) : 'not chosen yet'} (optional here; the card says "not chosen yet" until picked)`;
  }).join('\n');
}

const revalNotice = (d, t) => {
  const dr = revalidate(d, t);
  return dr.length ? `Changed your mind? These picks no longer apply and were cleared: ${dr.join(', ')}.` : '';
};

export { ABILITY_NAMES };
