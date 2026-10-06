/** Player-side Crawler management: /crawlers (list + swap REQUEST) and /delete. Every state change goes through tools/state.py; nothing here edits state.json. */
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { defaultRun } from './commit.js';
import { tablesFor } from './data.js';
import { classLabel, speciesLabel } from './names.js';
import { isActive, kindOf, ownedCrawlers } from './owner.js';
import { createSettings } from './settings.js';
import { readSessionState } from './store.js';

const channelMap = (config) => {
  const p = process.env.PLAYER_CHANNELS_FILE || join(config.campaign.dataDir, 'player-channels.json');
  try { return existsSync(p) ? JSON.parse(readFileSync(p, 'utf8')) : {}; } catch { return {}; }
};

const userOf = (i) => ({ id: i.user.id, username: i.user.username, globalName: i.user.globalName });

/** The caller's Crawlers with their sheet channel link, active one first. */
export function listOwned(config, user) {
  const st = readSessionState(config);
  const owned = ownedCrawlers(config, user, st);
  const map = channelMap(config).crawlers ?? {};
  let t = null;
  try { t = tablesFor(config); } catch { /* no tables: plain 5e names */ }
  return owned
    .map((c) => ({
      name: c.name, class: c.class, species: c.species, classDisplay: c.class ? classLabel(t, c.class) : c.class, speciesDisplay: c.species ? speciesLabel(t, c.species) : c.species, level: c.level ?? 1, kind: kindOf(c), active: kindOf(c) === 'pet-crawler' ? isActive(c) : isActive(c), owner: c.owner ?? null,
      player: c.player, discordId: c.build?.discord_user_id ?? null, dead: (c.conditions ?? []).some((x) => /^(dead|deceased)$/i.test(x)),
      channelId: map[c.name]?.channel_id ?? null, channelName: map[c.name]?.channel_name ?? null,
    }))
    .sort((a, b) => Number(b.active) - Number(a.active) || a.name.localeCompare(b.name));
}

export const channelLink = (c) => (c.channelId ? `<#${c.channelId}>` : '(no sheet channel yet)');

export function crawlersText(rows, floor) {
  if (!rows.length) return 'You have no Crawlers in this session yet. Use `/create`.';
  const lines = rows.map((c) => `${c.active ? '**ACTIVE**' : 'benched'} · **${c.name}** — ${c.speciesDisplay ?? c.species ?? ''} ${c.classDisplay ?? c.class ?? ''} L${c.level}${c.kind === 'pet-crawler' ? ` (pet-Crawler of ${c.owner})` : ''}${c.dead ? ' · DEAD' : ''} · ${channelLink(c)}`);
  return `${lines.join('\n')}\n\nOne Crawler is active and locked for the whole session${floor ? ` (floor ${floor})` : ''}. To change, **request a swap** below; the GM approves it between sessions. Nothing changes until then.`;
}

const pyRun = (ctx) => ctx.create?.run ?? defaultRun;
export function stateCmd(ctx, args, { publish = false } = {}) {
  const { config } = ctx;
  const env = { ...process.env, DCC_CAMPAIGN_ROOT: config.campaign.dir, DCC_CAMPAIGN_DIR: config.campaign.dir, DCC_SESSION: config.campaign.sessionId, DCC_AUTO_PUBLISH: publish ? '1' : '0' };
  return pyRun(ctx)(config.create.python, [join(config.campaign.dir, 'tools', 'state.py'), '--session', config.campaign.sessionId, ...args], { env, cwd: config.campaign.dir });
}

/** The error text of a refused state.py command, plain (no "ERROR:" prefix, no traceback). */
export const plainError = (r) => String(r.stderr || r.stdout || 'refused').split('\n').map((l) => l.trim()).filter(Boolean).map((l) => l.replace(/^ERROR:\s*/, '')).slice(0, 4).join(' ').slice(0, 600);

const ownerArgs = (c, user) => (c.discordId ? ['--as-user', String(user.id)] : ['--as-player', c.player]);

/** A swap REQUEST: never changes a Crawler. Refused with a plain message while a session is open. */
export async function requestSwap(ctx, user, name) {
  const rows = listOwned(ctx.config, user);
  const c = rows.find((x) => x.name === name);
  if (!c) return { ok: false, message: 'That is not one of your Crawlers.' };
  if (c.kind !== 'player') return { ok: false, message: `${c.name} is a pet-Crawler: it follows its owner, so ask for the owner instead.` };
  if (c.active) return { ok: false, message: `${c.name} is already your active Crawler.` };
  const r = await stateCmd(ctx, ['crawler', 'request', c.name, '--reason', 'player asked via /crawlers', ...ownerArgs(c, user), '--by', String(user.id)]);
  if (!r.ok) return { ok: false, message: plainError(r) };
  const settings = createSettings(ctx.config);
  if (settings.staffChannelId && ctx.client) {
    try {
      const ch = await ctx.client.channels.fetch(settings.staffChannelId);
      await ch?.send({ content: `Swap request: **${c.player}** asks to make **${c.name}** the active Crawler. Nothing changed. GM: \`state.py crawler activate "${c.name}" --reason ...\` between sessions.`, allowedMentions: { parse: [] } });
    } catch (err) { ctx.logger?.warn?.(`/crawlers: staff note failed (${err.message})`); }
  }
  return { ok: true, message: `Request sent: make **${c.name}** your active Crawler. The GM approves it between sessions; nothing has changed yet.` };
}

export const deleteWarning = (c) => [
  `**Delete ${c.name}?** This is permanent.`,
  `• Its sheet file, its published card and its text channel (${channelLink(c)}) are removed.`,
  `• Its credits, gear and boxes go with it. **Nothing is refunded**, and nothing moves to another Crawler.`,
  `• The ledger rows are archived (never destroyed) so the books still balance.`,
  c.active ? `• ${c.name} is your **active** Crawler: it can only be deleted between sessions, and you will need to name a new active one afterwards.` : `• ${c.name} is benched, so it can be deleted any time.`,
  `The default answer is **Cancel**. To go on, press the button and type the exact name.`,
].join('\n');

/** Delete with the typed name already checked by the caller. Own Crawlers only (checked here and again by state.py). */
export async function deleteOwned(ctx, user, name, typed) {
  const c = listOwned(ctx.config, user).find((x) => x.name === name);
  if (!c) return { ok: false, message: 'That is not one of your Crawlers, so it cannot be deleted.' };
  if (typed !== c.name) return { ok: false, message: 'The name you typed did not match exactly. Nothing was deleted.' };
  const r = await stateCmd(ctx, ['crawler', 'delete', c.name, '--reason', 'player /delete', '--confirm', typed, ...ownerArgs(c, user), '--by', String(user.id)], { publish: false });
  if (!r.ok) return { ok: false, message: plainError(r) };
  return { ok: true, message: `Deleted **${c.name}**. ${String(r.stdout).split('\n').filter((l) => /deleted Discord channel|channel NOT deleted|sheet file/.test(l)).join(' ')}`.trim() };
}

/** Best-effort: record that a play session opened/closed (the bridge joined/left voice). A restart is needed to load this. */
export async function markSession(ctx, action) {
  try {
    const r = await stateCmd(ctx, ['session-status', action, '--by', 'bridge', '--note', `bridge /${action === 'open' ? 'join' : 'leave'}`]);
    if (!r.ok) ctx.logger?.warn?.(`session-status ${action} failed: ${plainError(r)}`);
  } catch (err) {
    ctx.logger?.warn?.(`session-status ${action} failed: ${err.message}`);
  }
}
