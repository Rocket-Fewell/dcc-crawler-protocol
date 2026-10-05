/**
 * S17 Confirm: the ONLY step that writes game state. Resume-safe: draft.status moves
 * draft -> awaiting_review (hold mode) -> state_written -> sheet_written -> channel_done -> done,
 * and a retry continues from the first undone step. No GM wake, nothing in #table-transcript or #gm-voice.
 */
import { execFile } from 'node:child_process';
import { appendFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { promisify } from 'node:util';
import { line } from './data.js';
import { tx } from './screenstext.js';
import { createSettings } from './settings.js';
import { unlinkSync } from 'node:fs';
import { newIntakeTag, sheetFileName, sheetMarkdown, toSpec } from './files.js';
import * as R from './rules.js';
import { isHeaderId } from './reskin.js';
import { isActive, kindOf, ownedCrawlers } from './owner.js';
import { appendLog, deleteDraft, ensureDir, draftsDir, listDrafts, readSessionState, sessionIsOpen, writeDraft } from './store.js';

const execFileP = promisify(execFile);

export async function defaultRun(cmd, args, { env, cwd } = {}) {
  try {
    const { stdout, stderr } = await execFileP(cmd, args, { env, cwd, timeout: 60_000, maxBuffer: 4 * 1024 * 1024 });
    return { ok: true, stdout, stderr };
  } catch (err) {
    return { ok: false, stdout: err.stdout ?? '', stderr: String(err.stderr ?? err.message).slice(0, 500) };
  }
}

/** Party numbers. `count` = ACTIVE player Crawlers (benched Crawlers and pets take no slot). With `user`, also `owned` (that user's Crawlers) and `benched` (a new Crawler of theirs starts benched, so no slot is needed). */
export function partyInfo(config, user = null) {
  const st = readSessionState(config);
  if (!st) return { ready: false, count: 0, max: 4, names: [], tags: [], players: [], owned: [], benched: false };
  const owned = user ? ownedCrawlers(config, user, st) : [];
  return {
    ready: true,
    count: st.crawlers.filter((c) => kindOf(c) === 'player' && isActive(c)).length, // benched Crawlers, pets and companions do not count toward the cap
    max: st.limits?.max_crawlers ?? 4,
    names: st.crawlers.map((c) => c.name),
    tags: st.crawlers.map((c) => c.intake_tag).filter(Boolean),
    users: st.crawlers.map((c) => c.build?.discord_user_id).filter(Boolean),
    campaign: st.campaign,
    owned,
    benched: owned.some((c) => kindOf(c) === 'player') || sessionIsOpen(config),   // B2: any Crawler on file, or a session open, means the new one starts benched (no slot needed)
  };
}

/** Names that are taken (registered crawlers + other users' held drafts). */
export function takenNames(config, exceptUid) {
  const p = partyInfo(config);
  const held = listDrafts(config).filter((x) => x.uid !== exceptUid && ['awaiting_review', 'state_written', 'sheet_written', 'channel_done'].includes(x.status) && x.name).map((x) => x.name);
  return [...p.names, ...held];
}

/** Sort of near-duplicate: one name contains the other (case-insensitive), but they are not equal. */
export function nearDuplicate(name, others) {
  const n = name.toLowerCase();
  return others.find((o) => o.toLowerCase() !== n && (o.toLowerCase().includes(n) || n.includes(o.toLowerCase()))) ?? null;
}

const today = () => new Date().toISOString().slice(0, 10);

export async function commitDraft(d, ctx, tables, { run = ctx.create?.run ?? defaultRun, approved = false } = {}) {
  const config = ctx.config;
  const mode = createSettings(config).reviewMode;
  const out = { ok: false, held: false, messages: [], tag: d.intakeTag };
  const fail = (msg) => ({ ...out, error: msg });
  const party = partyInfo(config, { id: d.uid, username: d.uname, globalName: d.uname });
  if (!party.ready) return fail(line(tables, 'not_set_up', d.uid));

  // 1. validation + name check (resume-safe: skip the checks once the crawler exists)
  // resume-safe: a retry finds its own Crawler by intake tag (a user may own several, so the Discord id alone is not enough)
  const already = d.intakeTag ? readSessionState(config)?.crawlers.find((c) => c.intake_tag === d.intakeTag && c.build?.discord_user_id === d.uid) : null;
  if (!already) {
    const errs = R.validateDraft(d, tables, { partyCount: party.count, partyMax: party.max, benched: party.benched });
    if (errs.length) return fail(tx(tables, 'notice-fix-screen', `Fix ${errs[0].screen}: ${errs[0].msg}`, { screen: errs[0].screen, msg: errs[0].msg }));
    if (takenNames(config, d.uid).some((n) => n.toLowerCase() === d.name.toLowerCase())) {
      d.screen = 'S3';
      writeDraft(config, d);
      return { ...fail(line(tables, 'taken', d.uid)), backTo: 'S3' };
    }
  }
  // 2. intake tag
  if (!d.intakeTag) {
    const taken = [...party.tags, ...listDrafts(config).filter((x) => x.uid !== d.uid && x.intakeTag).map((x) => x.intakeTag)];
    d.intakeTag = newIntakeTag(taken);
    writeDraft(config, d);
  }
  const tag = d.intakeTag;
  out.tag = tag;
  // 3. review gate
  if (mode === 'hold' && !approved && d.status === 'draft') {
    d.status = 'awaiting_review';
    d.screen = 'S17';
    writeDraft(config, d);
    appendLog(config, { event: 'filed_for_review', crawler: d.name, uid: d.uid, tag });
    return { ...out, ok: true, held: true, messages: [line(tables, 'held', d.uid, { name: d.name })] };
  }
  if (d.status === 'awaiting_review' && !approved) return { ...out, ok: true, held: true, messages: [line(tables, 'held', d.uid, { name: d.name })] };

  const spec = toSpec(d, tables, tag);
  const bad = headerRows(spec.inventory, tables);
  if (bad.length) return fail(`Your gear still has an unresolved type (${bad.join(', ')}); go back to S10 and pick it.`);
  const specPath = join(draftsDir(config), `${d.uid}.spec.json`);
  ensureDir(draftsDir(config));
  writeFileSync(specPath, JSON.stringify(spec, null, 1), { mode: 0o600 });
  const py = config.create.python;
  const tools = join(config.campaign.dir, 'tools');
  const env = { ...process.env, DCC_CAMPAIGN_DIR: config.campaign.dir, DCC_SESSION: config.campaign.sessionId, DCC_AUTO_PUBLISH: '0' };
  const sid = config.campaign.sessionId;
  const py_ = (script, ...args) => run(py, [join(tools, script), '--session', sid, ...args], { env, cwd: config.campaign.dir });

  // 4. state
  if (['draft', 'awaiting_review'].includes(d.status)) {
    if (!already) {
      const r = await py_('state.py', 'create-crawler', '--file', specPath);
      if (!r.ok) return fail(`The registry refused the file: ${r.stderr.split('\n').filter(Boolean).pop() ?? 'unknown error'}`);
    }
    d.status = 'state_written';
    writeDraft(config, d);
    // 7. snark toasts (pay nothing)
    const toasts = ['Paperwork Survivor', ...(d.readTerms ? ["Don't Skip Intro"] : [])];
    for (const t of toasts) await py_('state.py', 'achievement', 'add', d.name, t, '--note', 'create-flow intake toast, pays nothing', '--benched-ok', 'intake toast (pays nothing)');
  }
  // 5. sheet file + index line
  if (d.status === 'state_written') {
    const cards = await cardText(py_, specPath);
    const dir = config.campaign.charactersDir;
    mkdirSync(dir, { recursive: true });
    const file = sheetFileName(d);
    writeFileSync(join(dir, file), sheetMarkdown(d, tables, tag, cards, today()));
    const idx = join(dir, 'INDEX.md');
    const entry = `- characters/${sessionPrefix(config)}${file}: ${d.name} (${d.class}, ${d.species}, ${d.background}), played by ${spec.player}. Owner: AI GM. Status: registered via /create.\n`;
    if (!existsSync(idx)) writeFileSync(idx, `# characters index (session ${sid})\nOwner: see NAMING-CONVENTIONS.md | Updated: ${today()}\n\n`);
    if (!readFileSync(idx, 'utf8').includes(`${file}:`)) appendFileSync(idx, entry);
    d.status = 'sheet_written';
    writeDraft(config, d);
  }
  // 6. sheet channel + first card (best effort; needs GM_DISCORD_TOKEN in the bridge env)
  if (d.status === 'sheet_written') {
    let posted = false;
    if (config.create.publish && process.env.GM_DISCORD_TOKEN) {
      const a = await py_('discord_gm.py', 'setup-channels');
      const b = a.ok ? await py_('discord_gm.py', 'publish', '--crawler', d.name, '--full') : a;
      posted = b.ok;
      if (!posted) ctx.logger?.warn?.(`/create: first-card publish failed for ${d.name}: ${b.stderr?.split('\n').pop()}`);
    }
    d.cardPosted = posted;
    d.status = 'channel_done';
    writeDraft(config, d);
  }
  // 8-9. staff log, finish, delete draft
  appendLog(config, { event: 'registered', crawler: d.name, uid: d.uid, tag, session: sid, card_posted: !!d.cardPosted, via: spec.build.created_via });
  deleteDraft(config, d.uid);
  try {
    unlinkSync(specPath);
  } catch {
    /* ignore */
  }
  const mine = readSessionState(config)?.crawlers.find((c) => c.intake_tag === tag);
  const msgs = [line(tables, 'registered', d.uid, { name: d.name, tag })];
  if (mine?.status === 'benched') { const sheetNote = d.cardPosted ? 'Your sheet channel is already posted.' : 'Your sheet channel and card are not up yet; the GM will post them.'; msgs.push(tx(tables, 'notice-benched', `**${d.name} starts BENCHED**: no party slot, no XP, credits or loot, until you make it your active Crawler between sessions (\`/crawlers\`). ${sheetNote}`, { name: d.name, sheet_note: sheetNote })); }
  return { ...out, ok: true, tag, cardPosted: !!d.cardPosted, benched: mine?.status === 'benched', messages: msgs };
}

export const sessionPrefix = (config) => (config.campaign.sessionId === 'alpha' ? '' : `../sessions-data/${config.campaign.sessionId}/characters/`);

/** The first-card text exactly as the publisher renders it. */
export async function cardText(py_, specPath) {
  const r = await py_('publisher.py', '--render-spec', specPath);
  if (!r.ok) return null;
  try {
    return JSON.parse(r.stdout).join('\n\n');
  } catch {
    return null;
  }
}

/** Names of inventory rows that are a header placeholder or carry no srd_id (nothing but the Intake Bag may lack one). A non-empty result blocks the commit. */
export function headerRows(rows, tables) {
  return (rows ?? []).filter((r) => (r.srd_id ? isHeaderId(tables, r.srd_id) : r.name !== 'Intake Bag')).map((r) => r.name);
}
