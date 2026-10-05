/** Pure 5e (2024) level-1 rules for /create. Everything is computed from the tables; nothing is typed in by the player. */
import { ABILITIES } from './data.js';
import { tx } from './screenstext.js';
import { money } from './money.js';
import * as K from './reskin.js';

export const mod = (score) => Math.floor((score - 10) / 2);
export const signed = (n) => (n >= 0 ? `+${n}` : `${n}`);
export const PB = 2;
export const SCREENS = Array.from({ length: 17 }, (_, i) => `S${i + 1}`);

export const isCaster = (d, t) => !!t.chargen.classes[d.class]?.spells;
export const speciesInfo = (d, t) => t.chargen.species[d.species];
export const classInfo = (d, t) => t.chargen.classes[d.class];
export const bgInfo = (d, t) => t.chargen.backgrounds[d.background];

// ---------------------------------------------------------------- ability scores
export function pointBuyCost(base, t) {
  const { cost, min, max } = t.chargen.point_buy;
  let total = 0;
  for (const a of ABILITIES) {
    const v = base[a];
    if (!Number.isInteger(v) || v < min || v > max) return null;
    total += cost[String(v)];
  }
  return total;
}

/** Background bonus per ability from the S7 choice. */
export function asiBonus(d, t) {
  const bg = bgInfo(d, t);
  const out = Object.fromEntries(ABILITIES.map((a) => [a, 0]));
  if (!bg || !d.asi) return out;
  if (d.asi.type === '1-1-1') for (const a of bg.asi) out[a] += 1;
  else if (d.asi.type === '2-1' && bg.asi.includes(d.asi.plus2) && bg.asi.includes(d.asi.plus1) && d.asi.plus2 !== d.asi.plus1) {
    out[d.asi.plus2] += 2;
    out[d.asi.plus1] += 1;
  }
  return out;
}

export function finalAbilities(d, t) {
  if (!d.base) return null;
  const b = asiBonus(d, t);
  return Object.fromEntries(ABILITIES.map((a) => [a, d.base[a] + b[a]]));
}

/** Parse "15 8 14 10 12 13" (STR DEX CON INT WIS CHA order) -> {str..} or {error}. */
export function parseScores(text, t) {
  const nums = String(text).match(/-?\d+/g)?.map(Number) ?? [];
  if (nums.length !== 6) return { error: tx(t, 'error-s8-six-numbers', 'Give exactly six numbers in the order STR DEX CON INT WIS CHA.') };
  return { base: Object.fromEntries(ABILITIES.map((a, i) => [a, nums[i]])) };
}

export function validateBase(d, t, allowed = null) {
  if (!d.base) return tx(t, 'error-s8-not-set', 'Ability scores are not set.');
  if (d.method === 'array') {
    const want = [...t.chargen.standard_array].sort((a, b) => b - a).join(',');
    const got = ABILITIES.map((a) => d.base[a]).sort((a, b) => b - a).join(',');
    if (want !== got) return tx(t, 'error-s8-array-once', `Standard array means each of ${t.chargen.standard_array.join(', ')} exactly once.`, { array: t.chargen.standard_array.join(', ') });
  } else if (d.method === 'pointbuy') {
    const c = pointBuyCost(d.base, t);
    if (c === null) return tx(t, 'error-s8-pointbuy-range', `Point buy scores must be ${t.chargen.point_buy.min}-${t.chargen.point_buy.max} before bonuses.`, { min: t.chargen.point_buy.min, max: t.chargen.point_buy.max });
    if (c > t.chargen.point_buy.budget) return tx(t, 'error-s8-pointbuy-cost', `That costs ${c} points; you have ${t.chargen.point_buy.budget}.`, { cost: c, budget: t.chargen.point_buy.budget });
  } else if (d.method === 'roll') {
    const c = checkRolls(d.scoreRolls, t);   // S17 re-check: everything is recomputed from the stored dice
    if (c.error) return c.error;
    const got = ABILITIES.map((a) => d.base[a]).sort((a, b) => b - a).join(',');
    if (got !== [...c.scores].sort((a, b) => b - a).join(',')) return tx(t, 'error-s8-kept-array', 'Use the six scores of the array you kept, each exactly once.');
  } else return tx(t, 'notice-s8-pick-method', 'Pick a method first.');
  for (const a of ABILITIES) if (!Number.isInteger(d.base[a]) || d.base[a] < 1 || d.base[a] > 30) return tx(t, 'error-s8-whole-numbers', 'Scores must be whole numbers.');
  void allowed;
  return null;
}

// ---------------------------------------------------------------- Roll method (decision 024)
export const ROLL_IDS = ['A', 'B', 'C'];
export const ROLL_MIN_TOTAL = 73;   // above 72; no upper limit
export const ROLL_MAX_ROUNDS = 10;  // safety stop for the System's automatic rerolls

/** One score from four d6: the three highest dice. null when the dice are not four whole numbers 1-6. */
export function scoreFromDice(dice) {
  if (!Array.isArray(dice) || dice.length !== 4 || dice.some((x) => !Number.isInteger(x) || x < 1 || x > 6)) return null;
  return dice.reduce((s, x) => s + x, 0) - Math.min(...dice);
}

/** An array of six scores built from its six dice sets (computed here, never typed). */
export function buildArray(id, diceSets) {
  const scores = diceSets.map(scoreFromDice);
  const total = scores.reduce((s, x) => s + x, 0);
  return { id, dice: diceSets, scores, total, keepable: total >= ROLL_MIN_TOTAL };
}

export function buildRound(round, byId) {
  const arrays = ROLL_IDS.map((id) => buildArray(id, byId[id]));
  return { round, qualified: arrays.some((a) => a.keepable), arrays };
}

/** Validate saved rolls from the dice up: -> {scores, array, round} for the kept array, else {error}. Also used at S17. */
export function checkRolls(sr, t) {
  const bad = (m) => ({ error: m });
  const rounds = sr?.rounds;
  if (!Array.isArray(rounds) || !rounds.length || rounds.length > ROLL_MAX_ROUNDS) return bad(tx(t, 'notice-s8-roll-three', 'Roll your three arrays first.'));
  for (let i = 0; i < rounds.length; i++) {
    const r = rounds[i];
    if (r?.round !== i + 1 || !Array.isArray(r.arrays) || r.arrays.length !== 3) return bad(tx(t, 'error-s8-roll-sum', 'Your rolled numbers do not add up. Roll again from the method screen.'));
    for (let k = 0; k < 3; k++) {
      const a = r.arrays[k];
      if (a?.id !== ROLL_IDS[k] || !Array.isArray(a.dice) || a.dice.length !== 6 || a.dice.some((x) => scoreFromDice(x) === null)) return bad(tx(t, 'error-s8-roll-sum', 'Your rolled numbers do not add up. Roll again from the method screen.'));
      const fresh = buildArray(a.id, a.dice);
      if (fresh.total !== a.total || fresh.keepable !== a.keepable || fresh.scores.join() !== (a.scores ?? []).join()) return bad(tx(t, 'error-s8-roll-dice', 'Your rolled numbers do not match the dice.'));
    }
    const q = r.arrays.some((a) => a.keepable);
    if (q !== !!r.qualified) return bad(tx(t, 'error-s8-roll-dice', 'Your rolled numbers do not match the dice.'));
    if (i < rounds.length - 1 && q) return bad(tx(t, 'error-s8-roll-past-keeper', 'A round that had a keepable array cannot be rolled past.'));
  }
  const k = sr.kept;
  const last = rounds[rounds.length - 1];
  if (!k) return bad(tx(t, 'error-s8-roll-keep-one', 'Keep one of your rolled arrays first.'));
  if (k.round !== last.round) return bad(tx(t, 'error-s8-roll-final-round', 'Keep an array from your final round.'));
  const arr = last.arrays.find((a) => a.id === k.array);
  if (!arr) return bad(tx(t, 'error-s8-roll-keep-one', 'Keep one of your rolled arrays first.'));
  if (!arr.keepable) return bad(tx(t, 'error-s8-roll-total', `That array totals ${arr.total}; it needs ${ROLL_MIN_TOTAL} or more.`, { total: arr.total, min_total: ROLL_MIN_TOTAL }));
  return { scores: arr.scores, array: arr, round: last };
}

/** Standard array assigned to suit the class (class.priority is highest-first). */
export function pickArray(d, t) {
  const pr = classInfo(d, t)?.priority ?? ABILITIES;
  const arr = [...t.chargen.standard_array].sort((a, b) => b - a);
  return Object.fromEntries(pr.map((a, i) => [a, arr[i]]));
}

// ---------------------------------------------------------------- equipment
const pkg = (list, id) => list.packages.find((p) => p.id === id);

export function chosenPackages(d, t) {
  const c = classInfo(d, t);
  const b = bgInfo(d, t);
  return [c && d.kitClass ? { src: 'class', info: c, pkg: pkg(c, d.kitClass) } : null, b && d.kitBg ? { src: 'background', info: b, pkg: pkg(b, d.kitBg) } : null].filter((x) => x?.pkg);
}

export const creditsFromPackages = (d, t) => chosenPackages(d, t).reduce((s, p) => s + p.pkg.gp, 0);

/** The variant the player chose for a header in a package (null until chosen: a header is never resolved silently). */
export const pickedVariant = (d, t, src, id) => d.variants?.[`${src}:${id}`] ?? null;

/** srd id of a kit entry {id (chargen key), variant}: a header's chosen variant, else the item's own srd_id; null = an unresolved header. */
export const lineSrdId = (line, t) => (K.isHeaderKey(t, line.id) ? (K.variantIds(t, line.id).includes(line.variant) ? line.variant : null) : K.itemSrdId(t, line.id));   // a variant that does not belong to the header counts as unresolved

/** Credits for one cart line: the chosen variant's own base_price_cp x qty x the floor multiplier (vending only), rounded up to whole credits. Throws on a header or unknown item. */
export function cartLineCost(line, t, floor = 1) {
  const cp = K.priceCp(t, lineSrdId(line, t), line.id);
  if (cp === null) throw new Error(`cannot price ${line.id}: pick a variant first (a header is never priced)`);
  return Math.ceil((cp * line.qty * K.floorMultiplier(floor)) / 100);
}
export const cartTotal = (d, t) => (d.cart ?? []).reduce((s, l) => s + cartLineCost(l, t, d.floor ?? 1), 0);
export const creditsLeft = (d, t) => creditsFromPackages(d, t) - cartTotal(d, t);

/** Merge package items + cart into [{id, qty, variant, src}] (stable order). A header in a package gets the variant picked for it (d.variants["class:holy_symbol"]); null until picked. */
export function kitItems(d, t) {
  const map = new Map();
  const add = (id, q, variant, src) => {
    const k = `${id}|${variant ?? ''}`;
    const cur = map.get(k);
    if (cur) cur.qty += q; else map.set(k, { id, qty: q, variant, src });
  };
  for (const p of chosenPackages(d, t)) for (const [id, q] of p.pkg.items) add(id, q, K.isHeaderKey(t, id) ? pickedVariant(d, t, p.src, id) : null, p.src);
  for (const l of d.cart ?? []) add(l.id, l.qty, K.isHeaderKey(t, l.id) ? l.variant ?? null : null, 'cart');
  return [...map.values()];
}

/** Fill every unresolved package header with its first listed variant (Pick for me, and pre-built Crawlers, which have no screen to pick on). Returns the picks made. */
export function fillVariants(d, t) {
  const made = [];
  d.variants ??= {};
  for (const v of pendingVariants(d, t)) {
    if (!v.chosen || !v.options.includes(v.chosen)) { d.variants[`${v.src}:${v.id}`] = v.options[0]; made.push(v.options[0]); }
  }
  return made;
}

/** Headers the player still has to resolve in the chosen packages: [{src, id, options:[srd ids]}] (valid picks are removed from the list). */
export function pendingVariants(d, t) {
  const out = [];
  for (const p of chosenPackages(d, t)) {
    for (const [id] of p.pkg.items) {
      if (!K.isHeaderKey(t, id) || out.some((o) => o.src === p.src && o.id === id)) continue;
      out.push({ src: p.src, id, options: K.variantIds(t, id), chosen: pickedVariant(d, t, p.src, id) });
    }
  }
  return out;
}

/** Display label for a kit entry: combined_label by srd id (variant id for a header), legacy name, then the plain 5e name. Never blank, never the junk field. */
export function itemLabel(entryOrKey, t) {
  const line = typeof entryOrKey === 'string' ? { id: entryOrKey, variant: null } : entryOrKey;
  const it = t.chargen.items[line.id];
  const srd = lineSrdId(line, t) ?? (K.isHeaderKey(t, line.id) ? null : K.itemSrdId(t, line.id));
  return srd ? K.labelFor(t, srd, it?.name ?? line.id) : it?.name ?? String(line.id);
}

/** Sheet rows. An unresolved header is NEVER emitted (validateDraft refuses to confirm until it is picked). Each row stores the srd_id and the chargen key. */
export function inventoryRows(d, t) {
  const rows = [];
  for (const line of kitItems(d, t)) {
    const srd = lineSrdId(line, t);
    if (!srd || K.isHeaderId(t, srd)) continue; // header placeholder: never stored
    const it = t.chargen.items[line.id];
    rows.push({ name: itemLabel(line, t), qty: line.qty, notes: '', mechanics: it.mechanics || `${K.plainName(t, srd, it.name)}: standard 5e item.`, category: it.category, srd_id: srd, chargen_key: line.id });
  }
  rows.push({ name: 'Intake Bag', qty: 1, notes: 'cosmetic, zero value', mechanics: 'Cosmetic. Holds nothing special.', category: 'gear' });
  return rows;
}

export function creditBreakdown(d, t) {
  const rows = [];
  for (const p of chosenPackages(d, t)) {
    if (p.pkg.gp) rows.push({ delta: p.pkg.gp, reason: `Starting credits: ${p.info.name} ${p.pkg.items.length ? `package ${p.pkg.id}` : 'gold option'}`, source: 'intake' });
  }
  for (const l of d.cart ?? []) rows.push({ delta: -cartLineCost(l, t, d.floor ?? 1), reason: `Vending Wall: ${itemLabel(l, t)}${l.qty > 1 ? ` x${l.qty}` : ''}`, source: 'intake' });
  return rows;
}

// ---------------------------------------------------------------- derived numbers
export function hpMax(d, t) {
  const c = classInfo(d, t);
  const ab = finalAbilities(d, t);
  if (!c || !ab) return null;
  return Math.max(1, c.hit_die + mod(ab.con) + (speciesInfo(d, t)?.hp_per_level ?? 0) + (originFeats(d, t).includes('Tough') ? 2 : 0));
}

export function armorClass(d, t) {
  const ab = finalAbilities(d, t);
  if (!ab) return null;
  const items = kitItems(d, t).map((k) => t.chargen.items[k.id]);
  const dex = mod(ab.dex);
  let best = null;
  for (const it of items) {
    if (!it.armor) continue;
    const v = it.armor.base + (it.armor.dex === 'full' ? dex : it.armor.dex === 'max2' ? Math.min(2, dex) : 0);
    if (best === null || v > best) best = v;
  }
  const shield = items.some((it) => it.shield);
  let ac;
  if (best !== null) ac = best;
  else if (d.class === 'Barbarian') ac = 10 + dex + mod(ab.con);
  else if (d.class === 'Monk' && !shield) ac = 10 + dex + mod(ab.wis);
  else ac = 10 + dex;
  if (shield) ac += 2;
  if (best !== null && d.classChoices?.fighting_style === 'Defense') ac += 1;
  return ac;
}

export function skillMod(d, t, skill) {
  const ab = finalAbilities(d, t);
  const base = mod(ab[t.chargen.skills[skill]]);
  const prof = profSkills(d, t).includes(skill);
  const exp = (d.expertise ?? []).includes(skill);
  return base + (prof ? PB : 0) + (exp ? PB : 0);
}

export function derived(d, t) {
  const ab = finalAbilities(d, t);
  if (!ab) return null;
  return { hp: hpMax(d, t), ac: armorClass(d, t), initiative: mod(ab.dex), passives: { perception: 10 + (profSkills(d, t).includes('Perception') ? PB : 0) + mod(ab.wis) } };
}

// ---------------------------------------------------------------- proficiencies
export const fixedSkills = (d, t) => [...(bgInfo(d, t)?.skills ?? [])];
export function profSkills(d, t) {
  return [...new Set([...fixedSkills(d, t), ...(d.classSkills ?? []), ...(d.speciesSkill ? [d.speciesSkill] : []), ...(d.featSkills ?? [])])];
}

export function classSkillOptions(d, t) {
  const c = classInfo(d, t);
  if (!c) return [];
  const owned = new Set([...fixedSkills(d, t), ...(d.speciesSkill ? [d.speciesSkill] : []), ...(d.featSkills ?? [])]);
  return c.skills.filter((s) => !owned.has(s));
}

export function speciesSkillOptions(d, t) {
  const sp = speciesInfo(d, t)?.extra_skill;
  if (!sp) return null;
  const owned = new Set([...fixedSkills(d, t), ...(d.classSkills ?? []), ...(d.featSkills ?? [])]);
  const from = sp.from === 'any' ? Object.keys(t.chargen.skills) : sp.from;
  return { label: sp.label, options: from.filter((s) => !owned.has(s)) };
}

export function featSkillOptions(d, t) {
  const owned = new Set([...fixedSkills(d, t), ...(d.classSkills ?? []), ...(d.speciesSkill ? [d.speciesSkill] : [])]);
  return Object.keys(t.chargen.skills).filter((s) => !owned.has(s));
}

export function toolsList(d, t) {
  const tools = [];
  const bt = bgInfo(d, t)?.tool;
  if (bt) tools.push(bt);
  if (d.class === 'Rogue') tools.push("Thieves' Tools");
  return [...new Set(tools)];
}

export function expertiseOptions(d, t) {
  return [...profSkills(d, t), ...(d.class === 'Rogue' ? ["Thieves' Tools"] : [])];
}

export function masteryChoice(d, t) {
  return classInfo(d, t)?.choices?.find((c) => c.key === 'weapon_masteries') ?? null;
}

export function languageOptions(d, t) {
  return t.chargen.languages.standard.filter((l) => l !== 'Common');
}

export function spellInfo(d, t) {
  const c = classInfo(d, t);
  return c?.spells ?? null;
}

export const originFeats = (d, t) => [bgInfo(d, t)?.feat, extraFeatNeeded(d, t) ? d.extraFeat : null].filter(Boolean);
export const featSkillCount = (d, t) => (originFeats(d, t).includes('Skilled') ? 3 : 0);

export const extraFeatNeeded = (d, t) => !!speciesInfo(d, t)?.extra_feat;

// ---------------------------------------------------------------- validation
/** Whole-draft legality check -> [{screen, msg}] (empty = ready to Confirm). */
export function validateDraft(d, t, env = {}) {
  const e = [];
  const add = (screen, msg) => e.push({ screen, msg });
  if (!d.name) add('S3', 'Crawler name missing.');
  if (!d.look || !d.hook) add('S4', 'Look and hook are both required.');
  if (!d.species || !t.chargen.species[d.species]) add('S5', 'Pick a species.');
  else {
    const sub = speciesInfo(d, t).sub;
    if (sub && !sub.options.includes(d.speciesSub)) add('S5', `Pick your ${sub.label.toLowerCase()}.`);
  }
  if (!d.class || !classInfo(d, t)) add('S6', 'Pick a class.');
  else for (const c of classInfo(d, t).choices.filter((x) => x.options && x.key !== 'weapon_masteries')) {
    if (!c.options.includes(d.classChoices?.[c.key])) add('S6', `Pick your ${c.label}.`);
  }
  if (!d.background || !bgInfo(d, t)) add('S7', 'Pick a background.');
  else {
    if (!d.asi) add('S7', 'Choose how the background raises your scores.');
    if (extraFeatNeeded(d, t) && !t.chargen.origin_feats.includes(d.extraFeat)) add('S7', 'Humans pick one extra Origin feat.');
    if (extraFeatNeeded(d, t) && d.extraFeat === bgInfo(d, t).feat) add('S7', 'Pick an Origin feat different from your background\'s.');
  }
  const be = validateBase(d, t);
  if (be) add('S8', be);
  else if (d.background && d.asi) {
    const fa = finalAbilities(d, t);
    if (ABILITIES.some((a) => fa[a] > 20)) add('S8', tx(t, 'error-s8-cap-20', 'No score may end above 20.'));
  }
  if (d.class && d.background) {
    const c = classInfo(d, t);
    const opts = classSkillOptions(d, t);
    const picks = d.classSkills ?? [];
    if (picks.length !== c.skill_count) add('S9', tx(t, 'error-s9-class-skills', `Pick exactly ${c.skill_count} class skills.`, { n: c.skill_count }));
    if (new Set(picks).size !== picks.length || picks.some((s) => !opts.includes(s))) add('S9', tx(t, 'error-s9-class-skills-legal', 'Class skill picks must be legal and not duplicate.'));
    if (featSkillCount(d, t) && ((d.featSkills ?? []).length !== featSkillCount(d, t) || (d.featSkills ?? []).some((x) => !featSkillOptions(d, t).includes(x)))) add('S9', tx(t, 'error-s9-skilled', `Skilled: pick ${featSkillCount(d, t)} more skills.`, { n: featSkillCount(d, t) }));
    const sp = d.species ? speciesSkillOptions(d, t) : null;
    if (sp && !sp.options.includes(d.speciesSkill)) add('S9', `Pick your ${sp.label}.`);
    if ((d.languages ?? []).length !== t.chargen.languages.pick || new Set(d.languages).size !== (d.languages ?? []).length) add('S9', tx(t, 'error-s9-languages', `Pick ${t.chargen.languages.pick} languages.`, { n: t.chargen.languages.pick }));
    const ex = c.choices.find((x) => x.key === 'expertise');
    if (ex && (d.expertise ?? []).length !== ex.count) add('S9', tx(t, 'error-s9-expertise-count', `Pick ${ex.count} Expertise.`, { n: ex.count }));
    if (ex && (d.expertise ?? []).some((s) => !expertiseOptions(d, t).includes(s))) add('S9', tx(t, 'error-s9-expertise-legal', 'Expertise needs a skill you are proficient in.'));
    const mc = masteryChoice(d, t);
    if (mc && ((d.masteries ?? []).length !== mc.count || (d.masteries ?? []).some((m) => !mc.options.includes(m)))) add('S9', tx(t, 'error-s9-masteries', `Pick ${mc.count} weapon masteries.`, { n: mc.count }));
  }
  if (d.class && d.background) {
    if (!d.kitClass || !d.kitBg) add('S10', money(tx(t, 'error-s10-need-both', 'Pick equipment (package or gold) for both class and background.')));
    else {
      const open = pendingVariants(d, t).filter((v) => !v.chosen || !v.options.includes(v.chosen));
      if (open.length) add('S10', tx(t, 'error-s10-which-one', `Pick which one you get: ${open.map((v) => t.chargen.items[v.id].name.replace(/ \(your choice\)/, '')).join(', ')}.`, { list: open.map((v) => t.chargen.items[v.id].name.replace(/ \(your choice\)/, '')).join(', ') }));
      else if ((d.cart ?? []).some((l) => K.isHeaderKey(t, l.id) && !K.variantIds(t, l.id).includes(l.variant))) add('S10', tx(t, 'error-s10-wall-no-type', 'A Vending Wall line is missing its type.'));
      else if (creditsLeft(d, t) < 0) add('S10', tx(t, 'error-s10-overspent', 'You spent more credits than you have.'));
    }
  }
  const sp = d.class ? spellInfo(d, t) : null;
  if (sp) {
    const s = d.spells ?? {};
    const inList = (arr, list) => (arr ?? []).every((n) => list.includes(n)) && new Set(arr).size === (arr ?? []).length;
    if ((s.cantrips ?? []).length !== sp.cantrips || !inList(s.cantrips, sp.cantrip_list)) add('S11', tx(t, 'error-s11-cantrips', `Pick ${sp.cantrips} cantrips from the class list.`, { n: sp.cantrips }));
    if (sp.spellbook) {
      if ((s.level1 ?? []).length !== sp.spellbook || !inList(s.level1, sp.level1_list)) add('S11', tx(t, 'error-s11-spellbook', `Pick ${sp.spellbook} spellbook spells.`, { n: sp.spellbook }));
      if ((s.prepared ?? []).length !== sp.prepared || !(s.prepared ?? []).every((n) => (s.level1 ?? []).includes(n))) add('S11', tx(t, 'error-s11-prepare', `Prepare ${sp.prepared} spells from your spellbook.`, { n: sp.prepared }));
    } else if ((s.level1 ?? []).length !== sp.level1_known || !inList(s.level1, sp.level1_list)) add('S11', tx(t, 'error-s11-level1', `Pick ${sp.level1_known} level 1 spells.`, { n: sp.level1_known }));
  }
  if (!d.backstory) add('S14', tx(t, 'error-s14-required', 'Backstory is required.'));
  if (!d.orders) add('S15', tx(t, 'error-s15-required', 'Standing Orders are required.'));
  if (!env.benched && env.partyCount !== undefined && env.partyMax !== undefined && env.partyCount >= env.partyMax) add('S1', tx(t, 'notice-party-full', 'Party full.'));   // a player's 2nd+ Crawler starts benched and needs no slot
  return e;
}

/** Fill a mechanical screen with a legal default; returns what it did, or null when nothing applies. */
export function autoPick(screen, d, t) {
  const c = classInfo(d, t);
  switch (screen) {
    case 'S5': {
      if (!d.species) d.species = 'Human';
      const sub = speciesInfo(d, t).sub;
      if (sub && !sub.options.includes(d.speciesSub)) d.speciesSub = sub.options[0];
      return `species ${d.species}${sub ? ` (${d.speciesSub})` : ''}`;
    }
    case 'S6': {
      if (!c) return null;
      d.classChoices = d.classChoices ?? {};
      for (const ch of c.choices.filter((x) => x.options && x.key !== 'weapon_masteries')) if (!ch.options.includes(d.classChoices[ch.key])) d.classChoices[ch.key] = ch.options[0];
      return `${d.class} choices`;
    }
    case 'S7': {
      const bg = bgInfo(d, t);
      if (!bg) return null;
      const pr = c?.priority ?? ABILITIES;
      const ranked = [...bg.asi].sort((a, b) => pr.indexOf(a) - pr.indexOf(b));
      d.asi = { type: '2-1', plus2: ranked[0], plus1: ranked[1] };
      if (extraFeatNeeded(d, t) && !d.extraFeat) d.extraFeat = t.chargen.origin_feats.find((f) => f !== bg.feat);
      return `+2 ${ranked[0].toUpperCase()} / +1 ${ranked[1].toUpperCase()}`;
    }
    case 'S8': {
      d.method = 'array';
      d.base = pickArray(d, t);
      return `standard array: ${ABILITIES.map((a) => `${a.toUpperCase()} ${d.base[a]}`).join(' ')}`;
    }
    case 'S9': {
      if (!c || !d.background) return null;
      const sp = speciesSkillOptions(d, t);
      if (sp && !sp.options.includes(d.speciesSkill)) d.speciesSkill = sp.options[0];
      if (featSkillCount(d, t)) d.featSkills = Object.keys(t.chargen.skills).filter((s) => !fixedSkills(d, t).includes(s) && s !== d.speciesSkill).slice(-featSkillCount(d, t));
      d.classSkills = classSkillOptions(d, t).slice(0, c.skill_count);
      d.languages = languageOptions(d, t).slice(0, t.chargen.languages.pick);
      const ex = c.choices.find((x) => x.key === 'expertise');
      if (ex) d.expertise = expertiseOptions(d, t).slice(0, ex.count);
      const mc = masteryChoice(d, t);
      if (mc) d.masteries = mc.options.slice(0, mc.count);
      return 'skills, languages and picks';
    }
    case 'S10': {
      if (!c || !d.background) return null;
      d.kitClass = 'A';
      d.kitBg = 'A';
      d.cart = [];
      d.variants = {};
      fillVariants(d, t);
      let left = creditsLeft(d, t);
      for (const [id, qty] of [['rations', 5], ['rope', 1], ['torch', 3], ['healers_kit', 1], ['waterskin', 1]]) {
        const cost = cartLineCost({ id, qty }, t, d.floor ?? 1);
        if (cost <= left && cost > 0) {
          d.cart.push({ id, qty });
          left -= cost;
        }
      }
      return `package A + package A, ${cartTotal(d, t)} credits of supplies`;
    }
    case 'S11': {
      const sp = spellInfo(d, t);
      if (!sp) return null;
      const pickN = (list, n, from = 0) => list.slice(from, from + n);
      d.spells = { cantrips: pickN(sp.cantrip_list, sp.cantrips), level1: pickN(sp.level1_list, sp.spellbook ?? sp.level1_known), prepared: [] };
      if (sp.spellbook) d.spells.prepared = d.spells.level1.slice(0, sp.prepared);
      return `${sp.cantrips} cantrips and level 1 spells`;
    }
    default:
      return null;
  }
}
