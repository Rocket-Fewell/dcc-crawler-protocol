/**
 * New-player roles (Caleb, Oct 6 2026).
 *
 * - Every human gets a personal role named after their Discord handle (username), tracked BY USER ID in
 *   <campaign>/sessions/player-roles.json (handles change and collide; a taken name gets "-2", "-3", ...).
 * - One shared "Crawler" base role carries the common access: read + send in #agents, #gm-voice, #general,
 *   #table-transcript and #create, Connect/Speak/Voice Activity (+ the built-in text chat) in the GM voice channel
 *   ("General", VOICE_CHANNEL_ID), and the role-level Deafen Members permission. Never Mute Members.
 * - Players SEE only those channels plus their own sheet (Caleb, Oct 6 2026, 9:39 AM): the Crawler role has ViewChannel
 *   DENIED on every other channel and category, including every sheet channel; each sheet's owner's personal role has
 *   View + Read History + Send ALLOWED there (a role allow beats a role deny). @everyone is never changed.
 *   Sheets = every campaign session's player-channels.json (alpha sessions/ + sessions-data/<id>/), owners from that
 *   session's state.json build.discord_user_id. A channel created later is hidden from Crawler at once (ChannelCreate).
 * - Additive only: roles are only ever added to members, overwrites only edited for the Crawler/personal roles.
 *   Nothing is removed from anyone; bots, managed roles and other overwrites are never touched.
 * Idempotent: safe on every start (ClientReady), on guildMemberAdd, and from `npm run roles:sync`.
 */
import { existsSync, mkdirSync, readFileSync, readdirSync, renameSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { ChannelType, OverwriteType, PermissionFlagsBits as P } from 'discord.js';

export const CRAWLER_ROLE_NAME = 'Crawler';
export const CRAWLER_ROLE_PERMS = P.DeafenMembers;          // role-level, server-wide (Caleb's final call); NOT MuteMembers
export const FORBIDDEN_PLAYER_PERMS = P.MuteMembers | P.Administrator;
export const ACCESS_CHANNEL_NAMES = ['agents', 'gm-voice', 'general', 'table-transcript', 'create'];
/** Members holding one of these roles keep that role's restricted setup: they get a personal role but NOT the Crawler base role. */
export const RESTRICTED_ROLE_NAMES = ['External Agent'];

export const TEXT_ALLOW = { ViewChannel: true, SendMessages: true, ReadMessageHistory: true };
export const VOICE_ALLOW = { ViewChannel: true, Connect: true, Speak: true, UseVAD: true, SendMessages: true, ReadMessageHistory: true };
export const CRAWLER_HIDDEN = { ViewChannel: false };
export const SHEET_OWNER = { ViewChannel: true, ReadMessageHistory: true, SendMessages: true };

const REASON = 'DCC new-player roles (additive sync)';
const TEXT_TYPES = new Set([ChannelType.GuildText, ChannelType.GuildAnnouncement]);
const VOICE_TYPES = new Set([ChannelType.GuildVoice, ChannelType.GuildStageVoice]);

// ------------------------------------------------------------------ store (by user id)

/** <campaign>/sessions/player-roles.json: guild-wide, shared by every campaign session. */
export const rolesFile = (config) => process.env.PLAYER_ROLES_FILE || join(config.campaign.dir, 'sessions', 'player-roles.json');

export function loadStore(file) {
  try {
    const s = JSON.parse(readFileSync(file, 'utf8'));
    return { version: 1, crawler_role_id: null, ...s, players: s.players ?? {} };
  } catch {
    return { version: 1, crawler_role_id: null, players: {} };
  }
}

export function saveStore(file, store) {
  mkdirSync(dirname(file), { recursive: true });
  const tmp = `${file}.${process.pid}.tmp`;
  writeFileSync(tmp, JSON.stringify(store, null, 1) + '\n');
  renameSync(tmp, file);
}

// ------------------------------------------------------------------ campaign data: sheet channel -> owner user id

/** Every campaign session's data dir: alpha (<campaign>/sessions) + <campaign>/sessions-data/<id>, the active one first. */
function sessionDataDirs(config) {
  const dirs = [config.campaign.dataDir, join(config.campaign.dir, 'sessions')];
  const root = join(config.campaign.dir, 'sessions-data');
  try { for (const d of readdirSync(root, { withFileTypes: true })) if (d.isDirectory()) dirs.push(join(root, d.name)); } catch { /* none */ }
  return [...new Set(dirs)];
}

/** Sheet channels of every campaign session with their owner's Discord user id (that session's state.json build.discord_user_id; null = unclear). */
export function sheetOwners(config) {
  const read = (p) => { try { return JSON.parse(readFileSync(p, 'utf8')); } catch { return null; } };
  const out = [];
  const seen = new Set();
  for (const dir of sessionDataDirs(config)) {
    const mapPath = dir === config.campaign.dataDir && process.env.PLAYER_CHANNELS_FILE ? process.env.PLAYER_CHANNELS_FILE : join(dir, 'player-channels.json');
    const map = existsSync(mapPath) ? read(mapPath) : null;
    if (!map) continue;
    const crawlers = read(join(dir, 'state.json'))?.crawlers ?? [];
    for (const [name, entry] of Object.entries(map.crawlers ?? {})) {
      if (!entry?.channel_id || seen.has(String(entry.channel_id))) continue;
      seen.add(String(entry.channel_id));
      const c = crawlers.find((x) => x.name === name);
      const uid = c?.build?.discord_user_id ? String(c.build.discord_user_id) : null;
      out.push({ crawler: name, channelId: String(entry.channel_id), channelName: entry.channel_name ?? null, ownerId: uid });
    }
  }
  return out;
}

// ------------------------------------------------------------------ helpers

const bitsOf = (x) => (x == null ? 0n : typeof x === 'bigint' ? x : BigInt(x.bitfield ?? x));

/** True when the channel's overwrite for `id` does not already match `spec` ({ Flag: true=allow | false=deny }). */
export function overwriteNeedsEdit(channel, id, spec) {
  const ow = channel.permissionOverwrites?.cache?.get(id);
  const allow = bitsOf(ow?.allow);
  const deny = bitsOf(ow?.deny);
  return Object.entries(spec).some(([k, v]) => (v ? (allow & P[k]) !== P[k] : (deny & P[k]) !== P[k]));
}

async function ensureOverwrite(channel, id, spec, { dryRun }) {
  if (!overwriteNeedsEdit(channel, id, spec)) return false;
  if (!dryRun) await channel.permissionOverwrites.edit(id, spec, { type: OverwriteType.Role, reason: REASON });   // edit() merges: other bits stay as they are
  return true;
}

export const sanitizeRoleName = (s) => String(s ?? '').replace(/[\r\n\t]/g, ' ').trim().slice(0, 100) || 'player';

/** Unique role name for a user: their handle, or handle-2, -3, ... when another role already has that name. */
export function uniqueRoleName(guild, base, exceptRoleId = null) {
  const taken = new Set([...guild.roles.cache.values()].filter((r) => r.id !== exceptRoleId).map((r) => r.name.toLowerCase()));
  taken.add('@everyone');
  taken.add(CRAWLER_ROLE_NAME.toLowerCase());
  const b = sanitizeRoleName(base);
  if (!taken.has(b.toLowerCase())) return b;
  for (let n = 2; ; n++) {
    const nm = `${b.slice(0, 96)}-${n}`;
    if (!taken.has(nm.toLowerCase())) return nm;
  }
}

const isAdminMember = (m) => Boolean(m.permissions?.has?.(P.Administrator));
const holdsRestricted = (guild, member) =>
  [...(member.roles?.cache?.keys?.() ?? [])].some((rid) => RESTRICTED_ROLE_NAMES.includes(guild.roles.cache.get(rid)?.name));

// ------------------------------------------------------------------ the manager

export class PlayerRoles {
  /**
   * @param {object} o
   * @param {object} o.config  bridge config (campaign.dir/dataDir, discord.* channel ids)
   * @param {string} [o.file]  store path (default rolesFile(config))
   * @param {boolean} [o.membersIntent] GuildMembers intent granted (guild.members.fetch() lists everyone)
   */
  constructor({ config, file = null, membersIntent = false, logger = null, dryRun = false }) {
    this.config = config;
    this.file = file ?? rolesFile(config);
    this.membersIntent = membersIntent;
    this.log = logger ?? { info() {}, warn() {}, error() {}, debug() {} };
    this.dryRun = dryRun;
    this.store = loadStore(this.file);
    this.known = new Set();   // user ids already checked this process (cheap lazy path)
    this.dryRoles = {};       // dry run: the roles that WOULD be created, by user id
    this.inflight = new Map(); // user id -> running onMemberAdd (a message + a voice join at once must not create two roles)
  }

  save() {
    if (!this.dryRun) saveStore(this.file, this.store);
  }

  /** The shared base role (created once, tracked by id). Only ever ADDS Deafen Members to it; never removes a bit. */
  async ensureCrawlerRole(guild, report = null) {
    let role = this.store.crawler_role_id ? guild.roles.cache.get(this.store.crawler_role_id) : null;
    if (!role) role = [...guild.roles.cache.values()].find((r) => r.name === CRAWLER_ROLE_NAME && !r.managed) ?? null;
    if (!role) {
      role = this.dryRun
        ? { id: 'dry-crawler', name: CRAWLER_ROLE_NAME, permissions: { bitfield: CRAWLER_ROLE_PERMS }, dry: true }
        : await guild.roles.create({ name: CRAWLER_ROLE_NAME, permissions: [CRAWLER_ROLE_PERMS], hoist: false, mentionable: false, reason: REASON });
      report?.actions.push(`created role ${CRAWLER_ROLE_NAME}`);
    } else if ((bitsOf(role.permissions) & CRAWLER_ROLE_PERMS) !== CRAWLER_ROLE_PERMS) {
      if (!this.dryRun) await role.setPermissions(bitsOf(role.permissions) | CRAWLER_ROLE_PERMS, REASON);
      report?.actions.push(`added Deafen Members to ${CRAWLER_ROLE_NAME}`);
    }
    if (this.store.crawler_role_id !== role.id && !role.dry) {
      this.store.crawler_role_id = role.id;
      this.save();
    }
    return role;
  }

  /** Personal role for one human: find it by user id (or adopt an exact-name role they already hold), else create it; then ADD it. */
  async ensurePlayer(guild, member, crawlerRole, report = null) {
    const user = member.user;
    if (!user || user.bot) return null;
    const uid = String(user.id);
    const entry = this.store.players[uid];
    let role = entry?.role_id ? guild.roles.cache.get(entry.role_id) : null;
    let created = false;
    if (!role) {
      // a role that is exactly their handle, that they already hold, unmanaged, no permissions, and nobody else's: adopt it (store lost)
      const owned = new Set(Object.values(this.store.players).map((p) => p.role_id));
      role = [...guild.roles.cache.values()].find((r) => r.name === sanitizeRoleName(user.username) && !r.managed && bitsOf(r.permissions) === 0n
        && member.roles.cache.has(r.id) && !owned.has(r.id)) ?? null;
    }
    if (!role) {
      const name = uniqueRoleName(guild, user.username);
      role = this.dryRun
        ? (this.dryRoles[uid] = { id: `dry-${uid}`, name, dry: true })
        : await guild.roles.create({ name, permissions: [], hoist: false, mentionable: false, reason: `${REASON}: personal role for ${user.username} (${uid})` });
      created = true;
      report?.actions.push(`created role ${name} for ${user.username}`);
    } else if (entry && role.name === entry.role_name && entry.username !== user.username) {
      // handle changed and nobody renamed the role by hand: follow the new handle
      const name = uniqueRoleName(guild, user.username, role.id);
      if (name !== role.name) {
        if (!this.dryRun) await role.setName(name, REASON);
        report?.actions.push(`renamed role ${role.name} -> ${name}`);
        role = this.dryRun ? { ...role, id: role.id, name } : role;
      }
    }
    if (role.editable === false) report?.problems.push(`role ${role.name} is above the bot's highest role: cannot assign it`);
    let assigned = false;
    if (!member.roles.cache.has(role.id)) {
      if (!this.dryRun) await member.roles.add(role, REASON);
      assigned = true;
      report?.actions.push(`gave ${user.username} role ${role.name}`);
    }
    let crawlerAssigned = false;
    let crawlerSkipped = null;
    if (crawlerRole && !member.roles.cache.has(crawlerRole.id)) {
      if (holdsRestricted(guild, member)) crawlerSkipped = `holds ${RESTRICTED_ROLE_NAMES.join('/')}`;
      else {
        if (!this.dryRun) await member.roles.add(crawlerRole, REASON);
        crawlerAssigned = true;
        report?.actions.push(`gave ${user.username} role ${CRAWLER_ROLE_NAME}`);
      }
    }
    if (!role.dry) {
      const next = { role_id: role.id, role_name: role.name, username: user.username, created_at: entry?.created_at ?? new Date().toISOString() };
      if (JSON.stringify(next) !== JSON.stringify(entry)) {
        this.store.players[uid] = next;
        this.save();
      }
    }
    this.known.add(uid);
    const r = { userId: uid, username: user.username, admin: isAdminMember(member), roleId: role.id, roleName: role.name, created, assigned, crawlerAssigned, crawlerSkipped };
    report?.players.push(r);
    return r;
  }

  /** 'text' | 'voice' when the channel is on the players' list (names/ids + PLAYER_ACCESS_CHANNELS), else null. */
  accessKind(ch) {
    const d = this.config.discord ?? {};
    const extra = String(process.env.PLAYER_ACCESS_CHANNELS ?? '').split(',').map((x) => x.trim()).filter(Boolean);
    const names = new Set([...ACCESS_CHANNEL_NAMES, ...extra.filter((x) => !/^\d+$/.test(x))]);
    const ids = new Set([d.gmOutputChannelId, d.transcriptChannelId, ...extra.filter((x) => /^\d+$/.test(x))].filter(Boolean).map(String));
    if (TEXT_TYPES.has(ch.type) && (ids.has(ch.id) || names.has(ch.name))) return 'text';
    if (VOICE_TYPES.has(ch.type) && (ch.id === String(d.voiceChannelId ?? '') || ids.has(ch.id))) return 'voice';
    return null;
  }

  /** Categories that hold a players' channel stay visible (no Crawler overwrite); every other category is hidden. */
  categoryHoldsAccess(guild, cat) {
    return [...guild.channels.cache.values()].some((c) => c.parentId === cat.id && this.accessKind(c));
  }

  /** One channel: allow the players' channels, hide everything else from the Crawler role (categories first, see visibility()). */
  async applyChannel(guild, ch, crawlerRole) {
    if (ch.isThread?.()) return null;   // threads follow their parent
    const kind = this.accessKind(ch);
    const dry = { dryRun: this.dryRun || crawlerRole.dry };
    if (kind) return { id: ch.id, name: ch.name, kind, changed: await ensureOverwrite(ch, crawlerRole.id, kind === 'text' ? TEXT_ALLOW : VOICE_ALLOW, dry) };
    if (ch.type === ChannelType.GuildCategory && this.categoryHoldsAccess(guild, ch)) return { id: ch.id, name: ch.name, kind: 'category (shown)', changed: false };
    return { id: ch.id, name: ch.name, kind: 'hidden', changed: await ensureOverwrite(ch, crawlerRole.id, CRAWLER_HIDDEN, dry) };
  }

  /** Crawler visibility for the whole guild. Returns [{ id, name, kind, changed }]. */
  async applyVisibility(guild, crawlerRole, report = null) {
    const out = [];
    const sheets = new Set(sheetOwners(this.config).map((x) => x.channelId));   // sheets: lockSheets (owner first, then the Crawler hide)
    const all = [...guild.channels.cache.values()].sort((x, y) => (y.type === ChannelType.GuildCategory) - (x.type === ChannelType.GuildCategory));
    for (const ch of all) {
      if (sheets.has(ch.id)) continue;
      const r = await this.applyChannel(guild, ch, crawlerRole);
      if (r) out.push(r);
    }
    if (report) report.channels = out;
    return out;
  }

  /** ChannelCreate: hide a new channel from Crawler at once (unless it is on the players' list); its sheet owner is added by lockSheets. */
  async onChannelCreate(ch) {
    if (!ch?.guild || String(ch.guild.id) !== String(this.config.discord.guildId)) return null;
    const crawler = this.store.crawler_role_id ? ch.guild.roles.cache.get(this.store.crawler_role_id) : null;
    if (!crawler) return null;
    return this.applyChannel(ch.guild, ch, crawler);
  }

  /** Every mapped sheet channel: hidden from Crawler, visible + readable + writable for its owner's personal role. @everyone untouched. */
  async lockSheets(guild, report = null) {
    const out = [];
    const crawler = this.store.crawler_role_id ? guild.roles.cache.get(this.store.crawler_role_id) : null;
    for (const s of sheetOwners(this.config)) {
      const ch = guild.channels.cache.get(s.channelId);
      if (!ch) { out.push({ ...s, status: 'channel not found' }); continue; }
      if (!TEXT_TYPES.has(ch.type)) { out.push({ ...s, status: 'not a text channel: skipped' }); continue; }
      const roleId = s.ownerId ? this.store.players[s.ownerId]?.role_id : null;
      const role = (roleId ? guild.roles.cache.get(roleId) : null) ?? (s.ownerId ? this.dryRoles[s.ownerId] : null) ?? null;
      // owner first, so the owner never loses the channel mid-sync
      const a = role ? (role.dry ? true : await ensureOverwrite(ch, role.id, SHEET_OWNER, { dryRun: this.dryRun })) : false;
      const b = crawler ? await ensureOverwrite(ch, crawler.id, CRAWLER_HIDDEN, { dryRun: this.dryRun }) : false;
      const status = role ? (a || b ? 'locked' : 'already locked') : `${s.ownerId ? 'owner has no personal role' : 'owner unclear'}: hidden from Crawler only${b ? ' (updated)' : ''}`;
      out.push({ ...s, name: ch.name, ownerRole: role?.name ?? null, status });
    }
    if (report) report.sheets = out;
    return out;
  }

  /** Every human to backfill. With the GuildMembers intent: the full list. Without it: every id the bot can know (store, sheet owners, member overwrites, voice, owner). */
  async humans(guild) {
    let members = [];
    if (this.membersIntent) {
      try { members = [...(await guild.members.fetch()).values()]; } catch (err) { this.log.warn(`roles: member list failed (${err.message}); using known ids`); }
    }
    if (!members.length) {
      const ids = new Set([...Object.keys(this.store.players), ...sheetOwners(this.config).map((s) => s.ownerId).filter(Boolean)]);
      if (guild.ownerId) ids.add(String(guild.ownerId));
      for (const ch of guild.channels.cache.values()) for (const ow of ch.permissionOverwrites?.cache?.values() ?? []) if (ow.type === OverwriteType.Member) ids.add(String(ow.id));
      for (const id of guild.voiceStates?.cache?.keys?.() ?? []) ids.add(String(id));
      for (const id of ids) {
        const m = await guild.members.fetch({ user: id, force: true }).catch(() => null);   // force: a cached member can be partial (no roles) without the intent
        if (m) members.push(m);
      }
    }
    return members.filter((m) => m.user && !m.user.bot);
  }

  /** Full idempotent backfill. Returns a report (also used by `npm run roles:sync`). */
  async sync(guild) {
    const report = { dryRun: this.dryRun, membersIntent: this.membersIntent, actions: [], problems: [], players: [], channels: [], sheets: [] };
    const crawler = await this.ensureCrawlerRole(guild, report);
    report.crawlerRole = { id: crawler.id, name: crawler.name };
    for (const m of await this.humans(guild)) {
      try { await this.ensurePlayer(guild, m, crawler, report); } catch (err) { report.problems.push(`${m.user.username}: ${err.message}`); }
    }
    await this.applyVisibility(guild, crawler, report);
    await this.lockSheets(guild, report);
    return report;
  }

  /** guildMemberAdd: personal role + Crawler for a new human; then their sheets (a returning player) lock to them. */
  async onMemberAdd(member) {
    if (!member?.user || member.user.bot) return null;
    if (String(member.guild.id) !== String(this.config.discord.guildId)) return null;
    const uid = String(member.user.id);
    if (this.inflight.has(uid)) return this.inflight.get(uid);
    const p = this._onMemberAdd(member).finally(() => this.inflight.delete(uid));
    this.inflight.set(uid, p);
    return p;
  }

  async _onMemberAdd(member) {
    const report = { dryRun: this.dryRun, actions: [], problems: [], players: [], channels: [], sheets: [] };
    const crawler = await this.ensureCrawlerRole(member.guild, report);
    await this.ensurePlayer(member.guild, member, crawler, report);
    await this.lockSheets(member.guild, report);
    for (const a of report.actions) this.log.info(`roles: ${a}`);
    for (const p of report.problems) this.log.warn(`roles: ${p}`);
    return report;
  }

  /** Lazy path when the GuildMembers intent is off: a human we have not seen yet speaks/uses a command/joins voice -> same as a join. */
  async ensureKnown(member) {
    if (!member?.user || member.user.bot || this.known.has(String(member.user.id))) return null;
    const entry = this.store.players[String(member.user.id)];
    if (entry && member.roles?.cache?.has(entry.role_id) && (!this.store.crawler_role_id || member.roles.cache.has(this.store.crawler_role_id) || holdsRestricted(member.guild, member))) {
      this.known.add(String(member.user.id));
      return null;
    }
    return this.onMemberAdd(member);
  }
}

// ------------------------------------------------------------------ voice self-guard

/**
 * VoiceStateUpdate guard for the bridge bot's own voice state: a server MUTE is undone at once (the GM voice cannot be killed
 * by accident). A server DEAFEN is intended (players hold Deafen Members): it is never undone and nothing is posted anywhere
 * (local log line only). While deafened the bridge hears nothing: no transcription, no GM wake from speech.
 */
export function createVoiceGuard({ getBotId, guildId, logger = null }) {
  const log = logger ?? { info() {}, warn() {} };
  let lastUnmute = 0;
  return async (oldState, newState) => {
    if (!newState || String(newState.id) !== String(getBotId()) || String(newState.guild?.id) !== String(guildId)) return { action: 'ignored' };
    if (!newState.channelId) return { action: 'ignored' };
    let action = 'none';
    if (newState.serverMute) {
      const now = Date.now();
      if (now - lastUnmute > 2000) {
        lastUnmute = now;
        try {
          await newState.setMute(false, 'GM voice guard: the bridge bot is never server-muted');
          log.warn('GM voice guard: someone server-muted the bridge bot; unmuted it');
          action = 'unmuted';
        } catch (err) {
          log.warn(`GM voice guard: could not unmute the bridge bot (${err.message})`);
          action = 'unmute-failed';
        }
      }
    }
    if (Boolean(oldState?.serverDeaf) !== Boolean(newState.serverDeaf) || (!oldState?.channelId && newState.serverDeaf)) {
      log.info(`GM voice guard: bridge bot ${newState.serverDeaf ? 'is server-deafened (hears nothing until undeafened)' : 'was undeafened'}; left as is`);
      if (action === 'none') action = newState.serverDeaf ? 'deafened' : 'undeafened';
    }
    return { action };
  };
}

// ------------------------------------------------------------------ GuildMembers intent preflight

/** Application flags: GATEWAY_GUILD_MEMBERS (1<<14) or GATEWAY_GUILD_MEMBERS_LIMITED (1<<15) means the privileged intent is enabled. */
export const membersIntentFromFlags = (flags) => (Number(flags) & ((1 << 14) | (1 << 15))) !== 0;

/** Decide whether to request the GuildMembers intent. DISCORD_MEMBERS_INTENT=true|false forces it; auto asks Discord (a refused intent would stop login). */
export async function detectMembersIntent(token, { env = process.env, fetchImpl = globalThis.fetch } = {}) {
  const v = String(env.DISCORD_MEMBERS_INTENT ?? 'auto').toLowerCase();
  if (['true', '1', 'on', 'yes'].includes(v)) return { enabled: true, source: 'env' };
  if (['false', '0', 'off', 'no'].includes(v)) return { enabled: false, source: 'env' };
  try {
    const r = await fetchImpl('https://discord.com/api/v10/applications/@me', { headers: { Authorization: `Bot ${token}` } });
    if (!r.ok) return { enabled: false, source: `api ${r.status}` };
    const app = await r.json();
    return { enabled: membersIntentFromFlags(app.flags), source: 'api' };
  } catch (err) {
    return { enabled: false, source: `api error ${err.message}` };
  }
}

/** One-line text summary of a sync report (logs + the CLI). */
export function formatReport(r) {
  const lines = [];
  lines.push(`roles sync${r.dryRun ? ' (DRY RUN)' : ''}: Crawler role ${r.crawlerRole?.name ?? '?'} (${r.crawlerRole?.id ?? '?'}); member list via ${r.membersIntent ? 'GuildMembers intent' : 'known ids (GuildMembers intent off)'}`);
  for (const p of r.players) lines.push(`  player ${p.username} (${p.userId})${p.admin ? ' [admin]' : ''}: role "${p.roleName}" ${p.roleId}${p.created ? ' CREATED' : ''}${p.assigned ? ' ASSIGNED' : ''}${p.crawlerAssigned ? ' +Crawler' : ''}${p.crawlerSkipped ? ` (no Crawler: ${p.crawlerSkipped})` : ''}`);
  for (const c of r.channels) lines.push(`  ${c.kind === 'hidden' ? 'hidden from Crawler' : c.kind.startsWith('category') ? 'category shown' : `players' ${c.kind}`} #${c.name}: ${c.changed ? 'UPDATED' : 'ok'}`);
  for (const s of r.sheets) lines.push(`  sheet #${s.name ?? s.channelName} -> ${s.ownerRole ?? s.ownerId ?? '?'}: ${s.status}`);
  for (const p of r.problems) lines.push(`  PROBLEM: ${p}`);
  if (!r.actions.length && !r.channels.some((c) => c.changed) && !r.sheets.some((x) => /^locked$|updated/.test(x.status))) lines.push('  no changes needed');
  return lines.join('\n');
}
