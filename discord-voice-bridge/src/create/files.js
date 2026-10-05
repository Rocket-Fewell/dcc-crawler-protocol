/** Turns a finished draft into the state.py spec JSON and the crawler sheet file (BUILD block + card). */
import { ABILITIES } from './data.js';
import { BRANCH_CHOICES, classLabel, classOptionLabel, lineageLabel, speciesLabel } from './names.js';
import * as R from './rules.js';

export const slug = (s) => String(s).toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'crawler';

export function playerName(d) {
  if (d.playerOverride) return String(d.playerOverride).slice(0, 30);   // a 2nd+ Crawler is filed under the player's existing name so the tools group them
  return String(d.uname || 'player').replace(/[^\w .'-]/g, '').trim().slice(0, 30) || 'player';
}

export const sheetFileName = (d) => `${slug(playerName(d))}-${slug(d.name)}.md`;

export function newIntakeTag(taken, rand = Math.random) {
  const used = new Set([...taken].map((x) => String(x).toLowerCase()));
  for (let i = 0; i < 500; i++) {
    const n = String(Math.floor(rand() * 10000)).padStart(4, '0');
    const l = String.fromCharCode(65 + Math.floor(rand() * 26));
    const tag = `CRAWLER #${n}-${l}`;
    if (!used.has(tag.toLowerCase())) return tag;
  }
  throw new Error('could not find a free intake tag');
}

function surveyNotes(d) {
  return (d.survey ?? []).map((x, i) => `${x.bonus ? `Bonus${x.bonus}` : `Q${i + 1}`}: ${x.a || 'PASS'}`).join(' | ');
}

export function buildObject(d, t, tag) {
  const c = R.classInfo(d, t);
  const sp = R.spellInfo(d, t);
  const dv = R.derived(d, t);
  const cc = { ...(d.classChoices ?? {}) };
  const bonus = R.asiBonus(d, t);
  const b = {
    pronouns: d.pronouns || null,
    look: d.look,
    hook: d.hook,
    backstory: d.backstory,
    species_choice: d.speciesSub || null,
    quirk: R.speciesInfo(d, t)?.quirk ?? null,
    hit_die: `d${c.hit_die}`,
    class_choices: cc,
    background_asi: d.asi?.type === '2-1' ? { mode: '+2/+1', plus2: d.asi.plus2, plus1: d.asi.plus1, applied: bonus } : { mode: '+1/+1/+1', applied: bonus },
    origin_feat: R.bgInfo(d, t).feat,
    extra_origin_feat: R.extraFeatNeeded(d, t) ? d.extraFeat : null,
    score_method: d.method,
    score_base: d.base,
    score_rolls: d.method === 'roll' ? d.scoreRolls : undefined,
    initiative: dv.initiative,
    passives: dv.passives,
    proficiency_bonus: R.PB,
    skills: R.profSkills(d, t),
    expertise: d.expertise?.length ? d.expertise : [],
    tools: R.toolsList(d, t),
    saves: c.saves,
    weapon_masteries: (d.masteries ?? []).map((id) => R.itemLabel(id, t)),
    languages: [t.chargen.languages.common, ...(d.languages ?? [])],
    kit: { class_option: `${d.kitClass}`, background_option: `${d.kitBg}` },
    handle_request: d.handle || null,
    broadcast_name: 'PENDING',
    survey: Object.fromEntries((d.survey ?? []).map((x, i) => [x.bonus ? `bonus${x.bonus}` : `q${i + 1}`, x.a || null])),
    discord_user_id: d.uid,
    created_via: d.prebuilt ? 'create-flow-prebuilt' : 'create-flow',
    flow_version: d.flow_version,
    chargen_table_version: t.version,
    todo: ['Origin feat sub-picks (Magic Initiate spells, Musician instruments, Crafter tools) are not asked by the flow v0.1'],
  };
  if (sp) {
    b.spells = { cantrips: d.spells.cantrips, prepared: sp.spellbook ? d.spells.prepared : d.spells.level1, spellbook: sp.spellbook ? d.spells.level1 : null };
    b.spell_slots = { 1: sp.slots_l1 };
    b.spellcasting_ability = sp.ability;
  }
  void tag;
  return b;
}

export function toSpec(d, t, tag) {
  const dv = R.derived(d, t);
  const fa = R.finalAbilities(d, t);
  const breakdown = R.creditBreakdown(d, t);
  return {
    name: d.name,
    player: playerName(d),
    class: d.class,
    species: d.species,
    level: 1,
    hp_max: dv.hp,
    ac: dv.ac,
    abilities: fa,
    background: d.background,
    intake_tag: tag,
    credits: breakdown.reduce((s, r) => s + r.delta, 0),
    credit_breakdown: breakdown,
    inventory: R.inventoryRows(d, t),
    standing_orders: d.orders,
    standing_reaction: d.reactions || 'Opportunity Attacks: on',
    signature: d.signature || undefined,
    fan_profile: {
      quirks: [],
      notes: surveyNotes(d),
      opt_outs: (d.optouts ?? []).map((o) => ({ kind: o.kind, topic: o.topic, shared: !!o.shared })),
    },
    notes: '',
    build: buildObject(d, t, tag),
  };
}

/** BUILD block (player-visible facts only: never survey answers or opt-outs). */
export function buildBlock(d, t) {
  const c = R.classInfo(d, t);
  const fa = R.finalAbilities(d, t);
  const dv = R.derived(d, t);
  const sp = R.spellInfo(d, t);
  const L = [];
  const sub = d.speciesSub ? ` (${lineageLabel(t, d.species, d.speciesSub)})` : '';   // display names only; buildObject/toSpec (state) keep the 5e names
  L.push(`Species (Latent Biology): ${speciesLabel(t, d.species)}${sub}`);
  const picks = Object.entries(d.classChoices ?? {}).map(([k, v]) => (BRANCH_CHOICES.has(k) ? classOptionLabel(t, d.class, v) : `${v}`)).join(', ');
  L.push(`Class (Provisional): ${classLabel(t, d.class)} 1 (d${c.hit_die})${picks ? ` - ${picks}` : ''}`);
  const asi = d.asi?.type === '2-1' ? `+2 ${d.asi.plus2.toUpperCase()}, +1 ${d.asi.plus1.toUpperCase()}` : '+1 to each of ' + R.bgInfo(d, t).asi.map((a) => a.toUpperCase()).join('/');
  L.push(`Background (Prior Employment): ${d.background} (${asi}); Origin feat ${R.originFeats(d, t).join(' + ')}`);
  L.push(`Scores (${d.method}): ` + ABILITIES.map((a) => `${a.toUpperCase()} ${fa[a]}`).join(' '));
  L.push(`HP ${dv.hp}, AC ${dv.ac}, Proficiency Bonus +${R.PB}, Initiative ${R.signed(dv.initiative)}, Passive Perception ${dv.passives.perception}`);
  L.push(`Saves: ${c.saves.map((s) => s.toUpperCase()).join(', ')}`);
  L.push(`Skills: ${R.profSkills(d, t).join(', ')}${d.expertise?.length ? ` (Expertise: ${d.expertise.join(', ')})` : ''}`);
  L.push(`Tools: ${R.toolsList(d, t).join(', ') || 'none'}; Languages: Common, ${(d.languages ?? []).join(', ')}`);
  if (d.masteries?.length) L.push(`Weapon Mastery: ${d.masteries.map((m) => R.itemLabel(m, t)).join(', ')}`);
  if (sp) {
    L.push(`Spells (${sp.ability.toUpperCase()}): cantrips ${d.spells.cantrips.join(', ')}; ${sp.spellbook ? `spellbook ${d.spells.level1.join(', ')}; prepared ${d.spells.prepared.join(', ')}` : `level 1 ${d.spells.level1.join(', ')}`}; ${sp.slots_l1} slot(s)`);
  }
  L.push(`Backstory: ${d.backstory}`);
  L.push(`Requested Handle: ${d.handle || '(none)'}; Broadcast Name: PENDING`);
  L.push(`Standing Orders: ${d.orders}`);
  L.push(`Standing Reactions: ${d.reactions || 'Opportunity Attacks: on'}`);
  if (d.signature) L.push(`Signature attack: ${d.signature}`);
  return L.join('\n');
}

export function sheetMarkdown(d, t, tag, cardText, today) {
  const L = [
    `# ${d.name} (${classLabel(t, d.class)}) - played by ${playerName(d)}`,
    `Owner: AI GM | Status: registered (created via /create) | Version: 0.1 | Updated: ${today}`,
    `Summary: ${playerName(d)}'s Crawler. ${classLabel(t, d.class)}, ${speciesLabel(t, d.species)} (${d.background} background). Intake Tag ${tag}. Created by the Discord /create flow; the state file is the source of truth for HP, credits and inventory.`,
    '',
    '## Identity',
    `- Player: ${playerName(d)} (Discord)`,
    `- Crawler name: ${d.name}${d.pronouns ? ` (${d.pronouns})` : ''}`,
    `- Intake Tag: ${tag}`,
    `- Look: ${d.look}`,
    `- Hook: ${d.hook}`,
    '',
    '## Build',
    buildBlock(d, t),
    '',
    '## Card (as first posted to the sheet channel)',
    cardText || '(card not rendered)',
    '',
  ];
  return L.join('\n');
}
