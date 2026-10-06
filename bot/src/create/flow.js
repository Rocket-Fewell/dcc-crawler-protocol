/** /create flow engine: draft lifecycle, rendering, navigation and interaction routing. Silent: no TTS, no #ears/#mouth post, no GM wake. */
import { EmbedBuilder, ButtonStyle, MessageFlags } from 'discord.js';
import { join } from 'node:path';
import { line, tablesFor } from './data.js';
import { cardText, commitDraft, partyInfo, defaultRun } from './commit.js';
import { sheetFileName, toSpec, buildBlock } from './files.js';
import { isActive, kindOf, ownedCrawlers, playerStringOf } from './owner.js';
import * as R from './rules.js';
import { SCREENS, revalidate, screenTitle } from './screens.js';
import { createSettings } from './settings.js';
import { appendLog, deleteDraft, draftsDir, listDrafts, readDraft, writeDraft, ensureDir, archiveIdle } from './store.js';
import { addButton, button, cid, row, cut } from './ui.js';
import { classLabel, speciesLabel } from './names.js';
import { tx, viewT } from './screenstext.js';
import { money } from './money.js';
import { writeFileSync } from 'node:fs';

export const FLOW_VERSION = '0.1.2'; // create-flow-spec-5e.md version this implements
const EPHEMERAL = MessageFlags.Ephemeral;
const HELP = {
  S1: 'This is a private intake booth: nothing here is spoken or posted. Accept or decline, both continue.\nA pre-built fills the mechanical screens with a legal concept you can still edit.\nNothing is saved to the game until you Confirm at the end.',
  S2: 'A line never appears. A veil is faded to black. You never have to explain.\nThe GM obeys every entry; the reviewer only sees entries you mark with *.\nSkip if you have none; you can reopen this with /create comfort.',
  S3: 'The name goes on the paperwork. Your Broadcast Name (what the audience calls you) comes later.\nIt must be unique in this session.\nPronouns are optional.',
  S4: 'Two short lines: what you look like now, and why you are funny or dangerous.\nEveryone reads as baseline human on Floors 1-2.\nNo links.',
  S5: 'Latent Biology is your species. Its traits work now but look like quirks until Floor 3.\nSome species ask a sub-choice (ancestry, lineage).\nPick for me chooses a legal default.',
  S6: 'Your Provisional Class is a level 1 class.\nSome classes ask one extra choice (fighting style, order, invocation).\nWeapon masteries and Expertise are picked on screen 9.',
  S7: 'Prior Employment is your 2024 background: it gives skills, a tool and an Origin feat.\nChoose +2/+1 or +1/+1/+1 to the three listed scores. No score above 20.\nHumans pick one extra Origin feat.',
  S8: 'Standard array: 15 14 13 12 10 8, each once. Point buy: 27 points, scores 8-15.\nEnter six numbers in the order STR DEX CON INT WIS CHA; the background bonus is added after.\nHP, AC and the rest are computed for you.',
  S9: 'Fixed proficiencies came with your background and species.\nPick the rest; skills you already own are hidden.\nClasses with masteries or expertise ask for those here.',
  S10: 'Each of class and background gives a package or a gold amount (1 gold = 1 credit).\nSpend leftover credits at the Vending Wall by typing names; everything is a real 5e item.\nEvery item shows the System\'s own name with the real 5e name in brackets (from the item-reskins table); stats never change. Holy symbols, gaming sets, instruments and tools ask you to pick a type.',
  S11: 'Casters pick cantrips and level 1 spells; Wizards also prepare a subset.\nEach menu entry says what the spell does in one line.\nOther classes skip this screen.',
  S13: 'Private notes the System uses to tailor your story. Never read aloud.\nBlank = pass, and that is fine.\nSkip the whole screen if you like.',
  S14: 'Backstory is public: the System reads it at your introduction.\nRequested Handle is what you would like the audience to call you.\nBroadcast Name stays PENDING until Floor 3.',
  S15: 'Orders tell your body what to do when you are away; reactions say how to use your reaction.\nA signature attack name is optional.\nNo orders means Dodge on timeout.',
  S16: 'This is the finished sheet and the card exactly as it will be posted.\nUse Edit to jump back to any screen; you return here.\nConfirm enables when everything is legal.',
  S17: 'Confirm locks the file and registers your Crawler.\nCorrections after this go through the GM.',
};

/** Ids of Lore's help rows (create-screens-reskins.json): the help dialog shows the row's text when the layer is on and the current text still matches. */
const HELP_IDS = { S3: 'help-s3', S4: 'help-s4', S8: 'help-s8', S9: 'help-s9', S10: 'help-s10', S11: 'help-s11', S13: 'help-s13', S14: 'help-s14', S15: 'help-s15', S16: 'help-s16', S17: 'help-s17' };

export function makeEnv(ctx, d) {
  const config = ctx.config;
  const t = tablesFor(config);
  const run = ctx.create?.run ?? defaultRun;
  const party = partyInfo(config, { id: d.uid, username: d.uname, globalName: d.uname });
  if (party.campaign?.current_floor) d.floor = party.campaign.current_floor;   // vending prices use the floor multiplier
  return {
    ctx, config, t: viewT(t, d.screen, d.comfortOnly),
    settings: createSettings(config),
    party,
    uid: d.uid,
    save: (dr) => writeDraft(config, dr),
    log: (e) => appendLog(config, e),
    /** One S8 Roll round: three arrays x six scores = 18 `roll.py 4d6dl1` calls, each logged as `S8 roll r<round> <A|B|C><1-6>` for the Crawler. Scores and totals are computed here from the dice. */
    async rollRound(dr, round) {
      const who = String(dr.name || dr.scoreRolls?.who || dr.uname || 'crawler');   // after a Restart the name is wiped: fall back to the Crawler name the rounds were rolled under
      const jobs = R.ROLL_IDS.flatMap((id) => [1, 2, 3, 4, 5, 6].map((n) => ({ id, n })));
      const out = await Promise.all(jobs.map(({ id, n }) => run(config.create.python, [join(config.campaign.dir, 'tools', 'roll.py'), '--json', '--who', who, '--label', `S8 roll r${round} ${id}${n}`, '4d6dl1'], { env: { ...process.env, DCC_CAMPAIGN_DIR: config.campaign.dir, DCC_SESSION: config.campaign.sessionId }, cwd: config.campaign.dir })));   // roll.py logs into THIS session's data dir
      const byId = { A: [], B: [], C: [] };
      out.forEach((r, k) => {
        let dice = null;
        try { dice = JSON.parse(r.stdout).terms[0].rolls; } catch { /* handled below */ }
        if (R.scoreFromDice(dice) === null) throw new Error(`roll.py gave no usable dice for ${jobs[k].id}${jobs[k].n}`);
        byId[jobs[k].id].push(dice);
      });
      return R.buildRound(round, byId);
    },
  };
}

export const newDraft = (config, user, keep = null) => ({
  flow_version: FLOW_VERSION, session: config.campaign.sessionId, uid: user.id, uname: user.globalName || user.username || 'player',
  started_at: new Date().toISOString(), screen: 'S1', status: 'draft', restarts: (keep?.restarts ?? -1) + 1,
  optouts: keep?.optouts ?? [], terms: keep?.terms ?? null, readTerms: keep?.readTerms ?? false,
  ...(keep?.scoreRolls?.rounds?.length ? { scoreRolls: { rounds: keep.scoreRolls.rounds, kept: null, ...(keep.scoreRolls.who ? { who: keep.scoreRolls.who } : {}) } } : {}),   // Restart wipes answers but not rolled rounds: no free rerolls (decision 024)
  ...(keep?.playerOverride ? { playerOverride: keep.playerOverride } : {}), ...(keep?.floor ? { floor: keep.floor } : {}),
});

// ------------------------------------------------------------------ navigation
const MECH = new Set(['S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S15']);
function skip(screen, d, t) {
  if (screen === 'S12') return true; // retired: tags come from the survey only
  if (screen === 'S11' && !R.isCaster(d, t)) return true;
  if (d.prebuilt && !d.editing && MECH.has(screen)) return true;
  return false;
}
export function nextScreen(d, t) {
  if (d.returnTo) { const s = d.returnTo; d.returnTo = null; d.editing = false; return s; }
  let i = R.SCREENS.indexOf(d.screen) + 1;
  while (i < 16 && skip(R.SCREENS[i], d, t)) i++;
  return R.SCREENS[Math.min(i, 16)];
}
export function prevScreen(d, t) {
  if (d.returnTo) { const s = d.returnTo; d.returnTo = null; d.editing = false; return s; }
  let i = R.SCREENS.indexOf(d.screen) - 1;
  while (i > 0 && skip(R.SCREENS[i], d, t)) i--;
  return R.SCREENS[Math.max(i, 0)];
}

// ------------------------------------------------------------------ Cancel build
/** A draft in these statuses already made a Crawler in the state file: it is not an uncommitted build and cannot be cancelled here. */
export const COMMITTED = new Set(['state_written', 'sheet_written', 'channel_done']);
const cancelButton = (d, t) => button(cid(d.uid, 'nav', 'cancel'), d.status === 'comfort' ? tx(t, 'nav-close-nosave', 'Close without saving') : tx(t, 'nav-cancel-build', 'Cancel build'), { style: ButtonStyle.Danger });
export const CANCELLED_TEXT = 'Build cancelled. Run /create to start fresh.';
export const REGISTERED_TEXT = 'This Crawler is already registered. Nothing to cancel.';
export const CLEARED_TEXT = 'Your build is already cleared. Run /create to start fresh.';

// ------------------------------------------------------------------ one request at a time per player
const userChains = new Map();
/** Serialize everything that reads, changes and writes one player's draft (3 quick Roll presses = one roll). The chain entry is removed when the queue drains. */
export async function withUserLock(uid, fn) {
  const prev = userChains.get(uid) ?? Promise.resolve();
  let release;
  const gate = new Promise((r) => { release = r; });
  const tail = prev.then(() => gate);
  userChains.set(uid, tail);
  await prev;
  try { return await fn(); } finally {
    release();
    if (userChains.get(uid) === tail) userChains.delete(uid);
  }
}
export const lockedUsers = () => userChains.size;

// ------------------------------------------------------------------ rendering
function pageRows(allRows, d, t) {
  if (allRows.length <= 4) return allRows;
  const pages = Math.ceil(allRows.length / 3);
  const p = (d.page ?? 0) % pages;
  return [...allRows.slice(p * 3, p * 3 + 3), row(button(cid(d.uid, d.screen, 'page'), tx(t, 'nav-more', `More ▸ (page ${p + 1}/${pages})`, { p: p + 1, pages })))];
}

export async function render(d, env0) {
  const env = { ...env0, t: viewT(env0.t, d.screen, d.comfortOnly) };   // plain_on views (S1, S2, S13, comfort-only) keep the old text
  const { t, ctx } = env;
  if (d.confirmCancel) {
    return { embeds: [new EmbedBuilder().setColor(0xb00020).setTitle(tx(t, 'dialog-trash-title', 'Trash everything?')).setDescription(tx(t, 'dialog-cancel-body', 'This deletes your whole build, including any rolled ability scores. Nothing has been registered. You can start fresh with /create.'))], components: [row(button(cid(d.uid, 'nav', 'cancel_yes'), tx(t, 'dialog-trash-yes', 'Yes, trash it'), { style: ButtonStyle.Danger }), button(cid(d.uid, 'nav', 'cancel_no'), tx(t, 'dialog-trash-no', 'No, keep going'), { style: ButtonStyle.Success }))] };
  }
  if (d.confirmRestart) {
    return { embeds: [new EmbedBuilder().setColor(0xb00020).setTitle(tx(t, 'dialog-restart-title', 'Restart?')).setDescription(line(t, 'restart_confirm', d.uid))], components: [row(button(cid(d.uid, 'nav', 'restart_yes'), tx(t, 'dialog-restart-yes', 'Yes, wipe my answers'), { style: ButtonStyle.Danger }), button(cid(d.uid, 'nav', 'restart_no'), tx(t, 'dialog-restart-no', 'Cancel')))] };
  }
  if (d.helpOpen) {
    return { embeds: [new EmbedBuilder().setColor(0x5865f2).setTitle(tx(t, 'dialog-help-title', `Help: ${d.screen}`, { screen: d.screen })).setDescription(money(tx(t, HELP_IDS[d.screen], HELP[d.screen] ?? '')))], components: [row(button(cid(d.uid, 'nav', 'help_close'), tx(t, 'dialog-help-ok', 'Got it')))] };
  }
  const S = SCREENS[d.screen];
  const desc = [];
  if (d.notice) desc.push(`> ${d.notice}`);
  const prompt = line(t, d.screen, d.uid);
  if (prompt) desc.push(`*${prompt}*`);
  desc.push(S.describe(d, env));
  const embeds = [new EmbedBuilder().setColor(0x2b2d31).setTitle(cut(`${d.screen} · ${screenTitle(t, d.screen)}`, 250)).setDescription(cut(desc.join('\n\n'), 4000)).setFooter({ text: tx(t, 'hint-embed-footer', `Private intake · session ${d.session} · only you can see this`, { session: d.session }) })];
  if (S.review) {
    const spec = toSpec({ ...d, intakeTag: d.intakeTag }, t, d.intakeTag ?? 'CRAWLER #PENDING');
    const specPath = join(draftsDir(env.config), `${d.uid}.preview.json`);
    const errs = R.validateDraft(d, t, { partyCount: env.party.count, partyMax: env.party.max, benched: env.party.benched });
    if (!errs.length) {
      ensureDir(draftsDir(env.config));
      writeFileSync(specPath, JSON.stringify(spec), { mode: 0o600 });
      const run = ctx.create?.run ?? defaultRun;
      const card = await cardText((script, ...a) => run(env.config.create.python, [join(env.config.campaign.dir, 'tools', script), '--session', env.config.campaign.sessionId, ...a], { env: { ...process.env, DCC_CAMPAIGN_DIR: env.config.campaign.dir }, cwd: env.config.campaign.dir }), specPath);
      embeds[0].setDescription(cut(`${d.notice ? `> ${d.notice}\n\n` : ''}*${prompt}*\n\n**BUILD**\n${buildBlock(d, t)}`, 4000));
      embeds.push(new EmbedBuilder().setColor(0x57f287).setTitle(tx(t, 'hint-s16-card', 'Player-channel card (as it will be posted)')).setDescription(cut(card ?? tx(t, 'hint-s16-card-missing', '(card preview unavailable)'), 3000)));
      try { (await import('node:fs')).unlinkSync(specPath); } catch { /* ignore */ }
    } else {
      embeds[0].setDescription(cut(`${d.notice ? `> ${d.notice}\n\n` : ''}**${tx(t, 'hint-s16-not-ready', 'Not ready to confirm:')}**\n${errs.map((e) => `• ${e.screen}: ${e.msg}`).join('\n')}\n\n**BUILD (so far)**\n${safeBuild(d, t)}`, 4000));
    }
  }
  const content = S.paged ? pageRows(S.allRows(d, env), d, t) : S.rows(d, env);
  const components = [...content].slice(0, 4);   // Discord caps a message at 5 rows; the nav row always takes one
  if (S.nav !== false) {
    const reason = S.ready(d, env);
    const empty = (d.screen === 'S2' && !(d.optouts ?? []).length) || (d.screen === 'S13' && !(d.survey ?? []).length);
    const nxt = d.comfortOnly ? tx(t, 'nav-save-close', 'Save and close') : d.screen === 'S16' ? tx(t, 'nav-confirm', 'Confirm ▸') : S.skippable && empty ? tx(t, 'nav-skip', 'Skip ▸') : tx(t, 'nav-next', 'Next ▸');
    const nav = [];
    if (!d.comfortOnly) nav.push(button(cid(d.uid, 'nav', 'back'), tx(t, 'nav-back', '◂ Back'), { disabled: d.screen === 'S2' && false }));
    nav.push(button(cid(d.uid, 'nav', 'next'), nxt, { style: ButtonStyle.Primary, disabled: !!reason && !(S.skippable && empty) }));
    if (S.pick && !d.comfortOnly) nav.push(button(cid(d.uid, 'nav', 'pick'), tx(t, 'nav-pick-for-me', 'Pick for me')));
    nav.push(button(cid(d.uid, 'nav', 'help'), tx(t, 'button-help', 'Help')));
    if (!d.comfortOnly && d.screen !== 'S16') nav.push(button(cid(d.uid, 'nav', 'restart'), tx(t, 'button-restart', 'Restart')));
    components.push(row(...nav));
  } else components.push(row(button(cid(d.uid, 'nav', 'help'), tx(t, 'button-help', 'Help'))));
  if (!COMMITTED.has(d.status) && !addButton(components, cancelButton(d, t))) {
    // a full screen (five rows, nav row full): Cancel build takes Restart's seat so the screen always has its exit
    const nav = components.find((r) => r.components.some((c) => c.data?.custom_id?.endsWith(':nav:restart')));
    const at = nav ? nav.components.findIndex((c) => c.data?.custom_id?.endsWith(':nav:restart')) : -1;
    if (at >= 0) nav.components.splice(at, 1, cancelButton(d, t));
    else components.at(-1).components.splice(-1, 1, cancelButton(d, t));
  }
  return { embeds, components };
}

function safeBuild(d, t) { try { return buildBlock(d, t); } catch { return '(incomplete)'; } }

const respond = async (i, payload) => {
  if (i.deferred || i.replied) return i.editReply(payload);
  if (i.isMessageComponent() || (i.isModalSubmit() && i.isFromMessage())) return i.update(payload);
  return i.reply({ ...payload, flags: EPHEMERAL });
};

// ------------------------------------------------------------------ entry points
/** /create (start or resume). */
export async function startCreate(i, ctx) {
  return withUserLock(i.user.id, () => startCreateLocked(i, ctx));
}
async function startCreateLocked(i, ctx) {
  const config = ctx.config;
  const t0 = (() => { try { return tablesFor(config); } catch { return null; } })();
  if (!config.create.enabled || !t0) return i.reply({ content: tx(t0, 'notice-unavailable', 'Character creation is not available right now.'), flags: EPHEMERAL });
  archiveIdle(config);
  const party = partyInfo(config, i.user);
  if (!party.ready) return i.reply({ content: line(t0, 'not_set_up', i.user.id), flags: EPHEMERAL });
  let d = readDraft(config, i.user.id);
  // a player may create any number of Crawlers (spec 8.2): the 1st is active, later ones start benched and need no party slot
  if (!d && !party.benched && party.count >= party.max) return i.reply({ content: line(t0, 'party_full', i.user.id), flags: EPHEMERAL });
  if (d?.status === 'awaiting_review') return i.reply({ content: line(t0, 'held', i.user.id, { name: d.name }), components: [row(cancelButton(d, t0))], flags: EPHEMERAL });   // still an uncommitted draft: it can be trashed
  if (!d) {
    d = newDraft(config, i.user);
    d.table_version = t0.version;
    d.floor = party.campaign?.current_floor ?? 1;
    if (party.benched) d.playerOverride = playerStringOf(party.owned);   // file the new Crawler under the player's existing name
    writeDraft(config, d);
    return i.reply({ ...(await render(d, makeEnv(ctx, d))), flags: EPHEMERAL });
  }
  const env = makeEnv(ctx, d);
  if (d.table_version !== env.t.version) {
    const dropped = revalidate(d, env.t);
    d.table_version = env.t.version;
    d.notice = dropped.length ? `${tx(env.t, 'notice-rules-changed', `The rules table changed; these picks were cleared: ${dropped.join(', ')}`, { list: dropped.join(', ') })}.` : null;
    writeDraft(config, d);
  }
  if (d.screen === 'S12') { d.screen = 'S13'; writeDraft(config, d); } // S12 retired: a draft saved there resumes at S13
  // resume prompt: re-post the current screen (messages go stale), never edit the old one
  return i.reply({
    embeds: [new (EmbedBuilder)().setColor(0xfee75c).setTitle('Resume your intake?').setDescription(`You have a draft open at **${d.screen}: ${SCREENS[d.screen] ? screenTitle(env.t, d.screen) : ''}**${d.name ? ` (${d.name})` : ''}. Your answers are kept.`)],
    components: [row(button(cid(d.uid, 'nav', 'resume'), tx(env.t, 'button-resume', 'Resume'), { style: ButtonStyle.Success }), button(cid(d.uid, 'nav', 'restart'), 'Start over'), ...(COMMITTED.has(d.status) ? [] : [cancelButton(d, env.t)]))],
    flags: EPHEMERAL,
  });
}

/** /create comfort: edit lines and veils any time (draft, or a registered crawler via state.py set). */
export async function startComfort(i, ctx) {
  return withUserLock(i.user.id, () => startComfortLocked(i, ctx));
}
async function startComfortLocked(i, ctx) {
  const config = ctx.config;
  const t = tablesFor(config);
  let d = readDraft(config, i.user.id);
  if (d) {
    d.screen = 'S2'; d.returnTo = d.status === 'draft' ? d.screen : null;
    d.comfortOnly = true;
    writeDraft(config, d);
  } else {
    const st = (await import('./store.js')).readSessionState(config);
    // lines and veils belong to the player: they are read from the active Crawler and saved to ALL of the player's Crawlers
    const owned = st ? ownedCrawlers(config, i.user, st) : [];
    const idxs = owned.map((c) => st.crawlers.indexOf(c));
    if (!idxs.length) return i.reply({ content: 'No Crawler or draft of yours in this session.', flags: EPHEMERAL });
    const idx = st.crawlers.indexOf(owned.find((c) => kindOf(c) === 'player' && isActive(c)) ?? owned[0]);
    const oo = (st.crawlers[idx].fan_profile?.opt_outs ?? []).map((o) => (typeof o === 'string' ? { kind: 'line', topic: o, shared: false } : o));
    d = { ...newDraft(config, i.user), status: 'comfort', screen: 'S2', comfortOnly: true, crawlerIndex: idx, crawlerIndexes: idxs, optouts: oo };
    writeDraft(config, d);
  }
  return i.reply({ ...(await render(d, makeEnv(ctx, d))), flags: EPHEMERAL });
}

const fieldsOf = (i) => ({ get: (id) => { try { return i.fields.getTextInputValue(id); } catch { return ''; } } });

/** Buttons, select menus and modal submits whose customId starts with "create:". */
export async function handleComponent(i, ctx) {
  const [, uid, screen, key] = i.customId.split(':');
  if (uid !== i.user.id) return i.reply({ content: 'This is not your intake booth.', flags: EPHEMERAL });
  // the first Roll rolls 18 dice through roll.py: answer Discord now (even if this press has to wait its turn), edit the message when the dice are done
  if (screen === 'S8' && key === 'roll' && i.isButton()) await i.deferUpdate();
  // one request at a time per player; the draft is read AFTER taking the turn, so every press acts on what the screen really shows
  return withUserLock(uid, () => handleComponentLocked(i, ctx));
}

const tablesSafe = (config) => { try { return tablesFor(config); } catch { return null; } };

async function handleComponentLocked(i, ctx) {
  const config = ctx.config;
  const [, uid, screen, key, arg] = i.customId.split(':');
  let d = readDraft(config, uid);
  if (!d) return respond(i, { content: screen === 'nav' && /^cancel/.test(key) ? CLEARED_TEXT : tx(tablesSafe(config), 'notice-draft-gone', 'That draft is gone. Run /create again.'), embeds: [], components: [] });
  const env = makeEnv(ctx, d);
  const S = SCREENS[d.screen];
  let res = {};
  if (screen === 'nav') res = await handleNav(i, key, d, env, ctx);
  else if (screen !== d.screen && !d.comfortOnly) { /* stale message: just redraw the current screen */ }
  else if (key === 'page') d.page = (d.page ?? 0) + 1 >= 99 ? 0 : (d.page ?? 0) + 1;
  else if (i.isModalSubmit()) res = (await SCREENS[screen].onModal?.(arg, fieldsOf(i), d, env)) ?? {};
  else if (i.isStringSelectMenu()) res = (await SCREENS[screen].onSelect?.(key, i.values, d, env, arg)) ?? {};
  else if (i.isButton()) res = (await SCREENS[screen].onButton?.(key, d, env)) ?? {};
  void S;
  if (res.modal) return i.showModal(res.modal);
  if (res.done) return res.done;
  if (res.go) { d.screen = res.go === 'S12' ? 'S13' : res.go; d.page = 0; if (res.edit) { d.returnTo = 'S16'; d.editing = true; } }
  if (res.restart) d.confirmRestart = true;
  d.notice = res.notice || null;
  if (res.commit) return doCommit(i, d, env, ctx);
  writeDraft(config, d);
  await respond(i, await render(d, env));
  if (res.followup) await i.followUp({ content: res.followup, flags: EPHEMERAL });
}

async function handleNav(i, key, d, env, ctx) {
  const { t, config } = env;
  switch (key) {
    case 'resume': d.confirmRestart = false; if (['state_written', 'sheet_written', 'channel_done'].includes(d.status)) { d.screen = 'S17'; return { commit: true }; } return {};
    case 'cancel': {   // ask once; works from any screen and from a stale message (no session or screen check)
      if (COMMITTED.has(d.status)) return { done: respond(i, { content: tx(t, 'notice-cancel-registered', REGISTERED_TEXT), embeds: [], components: [] }) };
      d.confirmCancel = true; d.confirmRestart = false; d.helpOpen = false;
      return {};
    }
    case 'cancel_no': d.confirmCancel = false; return {};
    case 'cancel_yes': {
      if (COMMITTED.has(d.status)) return { done: respond(i, { content: tx(t, 'notice-cancel-registered', REGISTERED_TEXT), embeds: [], components: [] }) };
      deleteDraft(config, d.uid);   // hard delete: answers, survey, opt-outs and any rolled rounds
      appendLog(config, { event: 'build_cancelled', uid: d.uid, screen: d.screen, status: d.status, had_rolls: !!d.scoreRolls?.rounds?.length });
      return { done: respond(i, { content: tx(t, 'notice-cancel-done', CANCELLED_TEXT), embeds: [], components: [] }) };
    }
    case 'help': d.helpOpen = true; return {};
    case 'help_close': d.helpOpen = false; return {};
    case 'restart': d.confirmRestart = true; return {};
    case 'restart_no': d.confirmRestart = false; return {};
    case 'restart_yes': {
      const fresh = newDraft(config, { id: d.uid, globalName: d.uname }, d);
      fresh.table_version = t.version;
      for (const k of Object.keys(d)) delete d[k];
      Object.assign(d, fresh);
      return { notice: tx(t, 'notice-wiped', 'Wiped. Your comfort answers were kept.') };
    }
    case 'back': return { go: prevScreen(d, t) };
    case 'pick': {
      const what = R.autoPick(d.screen, d, t);
      if (!what) return { notice: tx(t, 'notice-nothing-to-pick', 'Nothing to pick yet; finish the earlier screens first.') };
      const dr = revalidate(d, t);
      void dr;
      return { notice: line(t, 'pick_for_me', d.uid, { what }) };
    }
    case 'next': {
      if (d.comfortOnly) return saveComfort(i, d, env);
      const reason = SCREENS[d.screen].ready(d, env);
      if (reason && !(SCREENS[d.screen].skippable)) return { notice: reason };
      if (d.screen === 'S16') return { go: 'S17' };
      return { go: nextScreen(d, t) };
    }
    default: return {};
  }
  void ctx;
}

async function saveComfort(i, d, env) {
  const { config } = env;
  if (d.status === 'comfort') {
    const run = env.ctx.create?.run ?? defaultRun;
    let r = { ok: true };
    for (const ix of d.crawlerIndexes ?? [d.crawlerIndex]) {
      const one = await run(config.create.python, [join(config.campaign.dir, 'tools', 'state.py'), '--session', config.campaign.sessionId, 'set', `crawlers.${ix}.fan_profile.opt_outs`, JSON.stringify(d.optouts)], { env: { ...process.env, DCC_CAMPAIGN_DIR: config.campaign.dir, DCC_AUTO_PUBLISH: '0' }, cwd: config.campaign.dir });
      if (!one.ok) r = one;
    }
    deleteDraft(config, d.uid);
    appendLog(config, { event: 'comfort_updated', uid: d.uid, ok: r.ok });
    return { done: i.update({ embeds: [new EmbedBuilder().setTitle('Saved').setDescription(r.ok ? 'Your lines and veils are updated. Nobody was notified.' : tx(env.t, 'notice-save-failed', 'Could not save; ask the GM.'))], components: [] }) };
  }
  d.comfortOnly = false;
  d.screen = d.returnTo ?? 'S3';
  d.returnTo = null;
  return { notice: 'Comfort answers saved.' };
}

async function doCommit(i, d, env, ctx) {
  const { config, t } = env;
  await i.deferUpdate();
  writeDraft(config, d);
  const r = await commitDraft(d, ctx, t);
  if (!r.ok) {
    if (r.backTo) d.screen = r.backTo;
    d.notice = r.error;
    writeDraft(config, d);
    return i.editReply(await render(d, makeEnv(ctx, d)));
  }
  if (r.held) await staffNote(ctx, env, `**${d.name}** (${classLabel(env.t, d.class)} ${speciesLabel(env.t, d.species)}) is filed and waiting for review. Use \`/create review\` to look at it.`);
  else if (env.settings.reviewMode === 'notify') await staffNote(ctx, env, `New Crawler registered: **${d.name}** (${classLabel(env.t, d.class)} ${speciesLabel(env.t, d.species)}), Intake Tag ${r.tag}.`);
  return i.editReply({ embeds: [new EmbedBuilder().setColor(0x57f287).setTitle(r.held ? 'Filed' : 'Registered').setDescription(r.messages.join('\n'))], components: [] });
}

export async function staffNote(ctx, env, text) {
  const id = env.settings.staffChannelId;
  if (!id || !ctx.client) return;
  try {
    const ch = await ctx.client.channels.fetch(id);
    await ch?.send({ content: text, allowedMentions: { parse: [] } });
  } catch (err) {
    ctx.logger?.warn?.(`/create: staff note failed (${err.message})`);
  }
}

// ------------------------------------------------------------------ reviewer actions
export const isReviewer = (i, settings) => settings.reviewerIds.includes(i.user.id) || i.memberPermissions?.has?.('ManageGuild');

export function reviewerView(d, t) {
  const shared = (d.optouts ?? []).filter((o) => o.shared);
  const n = (d.optouts ?? []).length - shared.length;
  return [
    `**${d.name}** (${classLabel(t, d.class)} ${speciesLabel(t, d.species)}, ${d.background}) by <@${d.uid}> - status ${d.status}, Intake Tag ${d.intakeTag ?? '-'}`,
    buildBlock(d, t),
    `Shared with GM: ${shared.map((o) => `${o.kind}: ${o.topic}`).join('; ') || 'none'}`,
    n > 0 || shared.length ? `Opt-outs: set (private)${n ? ` (${n} not shown)` : ''}` : 'Opt-outs: none',
    `Survey: ${(d.survey ?? []).some((x) => x.a) ? 'answered' : 'not answered'}`,
  ].join('\n');
}

export async function reviewAction(i, ctx, action) {
  const config = ctx.config;
  const settings = createSettings(config);
  if (!isReviewer(i, settings)) return i.reply({ content: 'Only the table owner or a listed reviewer can do that.', flags: EPHEMERAL });
  const user = i.options.getUser('player');
  const t = tablesFor(config);
  if (action === 'review' && !user) {
    const held = listDrafts(config).filter((x) => x.status === 'awaiting_review');
    return i.reply({ content: held.length ? held.map((x) => `• ${x.name} - <@${x.uid}>`).join('\n') : 'Nothing is waiting for review.', flags: EPHEMERAL });
  }
  if (!user) return i.reply({ content: 'Name the player.', flags: EPHEMERAL });
  return withUserLock(user.id, () => reviewLocked(i, ctx, action, user, t));
}

async function reviewLocked(i, ctx, action, user, t) {
  const config = ctx.config;
  const d = readDraft(config, user.id);
  if (!d || d.status !== 'awaiting_review') return i.reply({ content: 'No filed draft from that player.', flags: EPHEMERAL });
  if (action === 'review') return i.reply({ content: cut(reviewerView(d, t), 1990), flags: EPHEMERAL });
  if (action === 'return') {
    const screen = (i.options.getString('screen') ?? 'S3').toUpperCase();
    if (!R.SCREENS.includes(screen) || screen === 'S1' || screen === 'S17') return i.reply({ content: 'Pick a screen from S2 to S16.', flags: EPHEMERAL });
    const note = i.options.getString('note') ?? '';
    d.status = 'draft'; d.screen = screen; d.notice = line(t, 'returned', d.uid, { name: d.name, screen, note: cut(note.replace(/[@<>`]/g, ''), 200) });
    writeDraft(config, d);
    appendLog(config, { event: 'returned', crawler: d.name, uid: d.uid, screen });
    await dm(ctx, user.id, d.notice);
    return i.reply({ content: `Sent ${d.name} back to ${screen}.`, flags: EPHEMERAL });
  }
  await i.deferReply({ flags: EPHEMERAL });
  const r = await commitDraft(d, ctx, t, { approved: true });
  if (!r.ok) return i.editReply(`Could not register: ${r.error}`);
  await dm(ctx, user.id, r.messages.join('\n'));
  return i.editReply(`Approved ${d.name}. Registered with Intake Tag ${r.tag}${r.cardPosted ? ' and the first card was posted' : ' (card not posted: run `discord_gm.py publish`)'}.`);
}

async function dm(ctx, uid, text) {
  try { await (await ctx.client.users.fetch(uid)).send({ content: text, allowedMentions: { parse: [] } }); } catch { /* DMs closed: they see it on next /create */ }
}
void sheetFileName;
