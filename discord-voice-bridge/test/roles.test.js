/** New-player roles (src/roles.js) against mocked discord.js objects and a temp campaign dir (never the live campaign). */
import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { ChannelType, OverwriteType, PermissionFlagsBits as P, PermissionsBitField } from 'discord.js';
import {
  CRAWLER_ROLE_NAME, PlayerRoles, createVoiceGuard, detectMembersIntent, formatReport, loadStore, membersIntentFromFlags, sheetOwners, uniqueRoleName,
} from '../src/roles.js';

const G = '900000000000000001';
const IDS = { caleb: '376517850724040714', grimm: '1177041830337056828', moses: '783884998230278164', gmBot: '1556179135783505930', newbie: '555000000000000001' };
const CH = { agents: '11', gmVoice: '12', general: '13', transcript: '14', create: '15', voice: '16', hiddenVoice: '17', gmSecret: '18', sheetCaleb: '21', sheetGrimm: '22', sheetMoses: '23', other: '19', alphaHornn: '24', alphaMoses: '25', alphaNobody: '26', catText: '41', catSheets: '42', catSecret: '43', catAlpha: '44' };
const ROLE = { admin: '31', external: '32', gmBotRole: '33' };

const bits = (n = 0n) => new PermissionsBitField(n);
let seq = 1000;

class FakeOverwrites {
  constructor(list = []) { this.cache = new Map(list.map((o) => [o.id, { ...o, allow: bits(o.allow), deny: bits(o.deny) }])); this.edits = []; }
  async edit(id, spec, opts = {}) {
    this.edits.push({ id, spec, opts });
    const cur = this.cache.get(id) ?? { id, type: opts.type ?? OverwriteType.Role, allow: bits(), deny: bits() };
    let a = cur.allow.bitfield, d = cur.deny.bitfield;
    for (const [k, v] of Object.entries(spec)) {
      const b = P[k];
      if (v === true) { a |= b; d &= ~b; } else if (v === false) { d |= b; a &= ~b; } else { a &= ~b; d &= ~b; }
    }
    this.cache.set(id, { ...cur, allow: bits(a), deny: bits(d) });
  }
  async delete() { throw new Error('overwrites must never be deleted'); }
  async set() { throw new Error('overwrites must never be replaced'); }
}

function makeGuild() {
  const g = { id: G, ownerId: IDS.caleb, calls: [] };
  const role = (id, name, perms = 0n, extra = {}) => ({ id, name, permissions: bits(perms), managed: false, editable: true, position: 1,
    async setPermissions(p) { g.calls.push(['setPermissions', id]); this.permissions = bits(BigInt(p)); },
    async setName(n) { g.calls.push(['setName', id, n]); this.name = n; }, async delete() { throw new Error('roles must never be deleted'); }, ...extra });
  g.roles = {
    cache: new Map([
      [G, role(G, '@everyone', P.ViewChannel | P.SendMessages | P.ReadMessageHistory | P.Connect | P.Speak)],
      [ROLE.admin, role(ROLE.admin, 'Admin', P.Administrator)],
      [ROLE.external, role(ROLE.external, 'External Agent', P.ChangeNickname)],
      [ROLE.gmBotRole, role(ROLE.gmBotRole, 'DCC AI GM', P.SendMessages, { managed: true })],
    ]),
    get everyone() { return g.roles.cache.get(G); },
    async create(opts) {
      g.calls.push(['createRole', opts.name]);
      const perms = (opts.permissions ?? []).reduce((a, b) => a | BigInt(b), 0n);
      const r = role(String(++seq), opts.name, perms);
      g.roles.cache.set(r.id, r);
      return r;
    },
  };
  const ch = (id, name, type, overwrites = [], parent = null) => ({ id, name, type, parentId: parent, permissionOverwrites: new FakeOverwrites(overwrites), guild: g });
  const ext = { id: ROLE.external, type: OverwriteType.Role, allow: 0n, deny: P.ViewChannel };
  const sheetEveryone = { id: G, type: OverwriteType.Role, allow: P.ViewChannel | P.ReadMessageHistory, deny: P.SendMessages | P.AddReactions };
  const gmBotOw = { id: IDS.gmBot, type: OverwriteType.Member, allow: P.ViewChannel | P.SendMessages | P.ReadMessageHistory | P.EmbedLinks, deny: 0n };
  g.channels = {
    cache: new Map([
      ch(CH.agents, 'agents', ChannelType.GuildText, [{ id: G, type: 0, allow: 0n, deny: P.ViewChannel }, { id: ROLE.external, type: 0, allow: P.ViewChannel | P.SendMessages, deny: P.MentionEveryone }, { id: IDS.caleb, type: 1, allow: P.ViewChannel, deny: 0n }]),
      ch(CH.gmVoice, 'gm-voice', ChannelType.GuildText, [ext]),
      ch(CH.catText, 'Text Channels', ChannelType.GuildCategory, [ext]),
      ch(CH.catSheets, 'Crawler Sheets (s1)', ChannelType.GuildCategory, []),
      ch(CH.catSecret, 'GM Secret', ChannelType.GuildCategory, [{ id: G, type: 0, allow: 0n, deny: P.ViewChannel }]),
      ch(CH.catAlpha, 'Crawler Sheets', ChannelType.GuildCategory, [ext]),
      ch(CH.general, 'general', ChannelType.GuildText, [{ id: ROLE.external, type: 0, allow: P.ViewChannel, deny: 0n }], CH.catText),
      ch(CH.transcript, 'table-transcript', ChannelType.GuildText, [ext]),
      ch(CH.create, 'create', ChannelType.GuildText, [{ id: G, type: 0, allow: P.ViewChannel | P.SendMessages, deny: 0n }, ext]),
      ch(CH.voice, 'General', ChannelType.GuildVoice, [{ id: ROLE.external, type: 0, allow: P.ViewChannel, deny: 0n }]),
      ch(CH.hiddenVoice, 'gm-only-voice', ChannelType.GuildVoice, [{ id: G, type: 0, allow: 0n, deny: P.ViewChannel }]),
      ch(CH.gmSecret, 'gm-secret', ChannelType.GuildText, [{ id: G, type: 0, allow: 0n, deny: P.ViewChannel }], CH.catSecret),
      ch(CH.alphaHornn, 'hornn-sheet', ChannelType.GuildText, [sheetEveryone, ext, gmBotOw], CH.catAlpha),
      ch(CH.alphaMoses, 'moses-sheet', ChannelType.GuildText, [sheetEveryone, ext, gmBotOw], CH.catAlpha),
      ch(CH.alphaNobody, 'nobody-sheet', ChannelType.GuildText, [sheetEveryone], CH.catAlpha),
      ch(CH.other, 'random', ChannelType.GuildText, []),
      ch(CH.sheetCaleb, 's1-hornn-eisenhorn', ChannelType.GuildText, [sheetEveryone, gmBotOw], CH.catSheets),
      ch(CH.sheetGrimm, 's1-grimmtrouble-shirayuki', ChannelType.GuildText, [sheetEveryone, gmBotOw], CH.catSheets),
      ch(CH.sheetMoses, 's1-trailer-park-moses-mr-white', ChannelType.GuildText, [{ id: G, type: 0, allow: P.ReadMessageHistory, deny: P.SendMessages | P.ViewChannel | P.AddReactions }, { id: IDS.moses, type: 1, allow: P.ViewChannel, deny: 0n }, gmBotOw], CH.catSheets),
    ].map((c) => [c.id, c])),
  };
  const member = (id, username, roleIds = [], bot = false) => {
    const m = {
      id, user: { id, username, bot }, guild: g, added: [],
      roles: {
        cache: new Map(roleIds.map((r) => [r, g.roles.cache.get(r)])),
        async add(r) { const rid = r.id ?? r; g.calls.push(['addRole', id, rid]); m.added.push(rid); m.roles.cache.set(rid, g.roles.cache.get(rid)); },
        async remove() { throw new Error('roles must never be removed'); },
        async set() { throw new Error('roles must never be replaced'); },
      },
      get permissions() { return bits([...m.roles.cache.values()].reduce((a, r) => a | (r?.permissions?.bitfield ?? 0n), g.roles.everyone.permissions.bitfield)); },
    };
    return m;
  };
  g.members = {
    cache: new Map([
      [IDS.caleb, member(IDS.caleb, 'hornn428', [ROLE.admin])],
      [IDS.grimm, member(IDS.grimm, 'troublegrimm', [])],
      [IDS.moses, member(IDS.moses, 'trailerparkmoses', [ROLE.admin, ROLE.external])],
      [IDS.gmBot, member(IDS.gmBot, 'DCC AI GM', [ROLE.gmBotRole, ROLE.admin], true)],
    ]),
    async fetch(arg) {
      if (arg === undefined) { g.calls.push(['listMembers']); return new Map(g.members.cache); }
      const id = typeof arg === 'object' ? arg.user : arg;
      const m = g.members.cache.get(id);
      if (!m) throw new Error('Unknown Member');
      return m;
    },
  };
  g.voiceStates = { cache: new Map() };
  g.member = member;
  return g;
}

/** Discord's channel permission calculation (admins bypass). */
function effective(g, ch, m) {
  let base = m.permissions.bitfield;
  if (base & P.Administrator) return (1n << 53n) - 1n;
  const ow = ch.permissionOverwrites.cache;
  const e = ow.get(G);
  if (e) base = (base & ~e.deny.bitfield) | e.allow.bitfield;
  let a = 0n, d = 0n;
  for (const rid of m.roles.cache.keys()) { const o = ow.get(rid); if (o && rid !== G) { a |= o.allow.bitfield; d |= o.deny.bitfield; } }
  base = (base & ~d) | a;
  const mo = ow.get(m.id);
  if (mo) base = (base & ~mo.deny.bitfield) | mo.allow.bitfield;
  return base;
}
const can = (g, chId, m, flag) => (effective(g, g.channels.cache.get(chId), m) & P[flag]) === P[flag];

function makeCampaign() {
  const dir = mkdtempSync(join(tmpdir(), 'dcc-roles-'));
  const dataDir = join(dir, 'sessions-data', 's1');
  mkdirSync(dataDir, { recursive: true });
  mkdirSync(join(dir, 'sessions'), { recursive: true });
  writeFileSync(join(dataDir, 'state.json'), JSON.stringify({ crawlers: [
    { name: 'Eisenhorn', player: 'Hornn', build: { discord_user_id: IDS.caleb } },
    { name: 'Shirayuki', player: 'Grimmtrouble', build: { discord_user_id: IDS.grimm } },
    { name: 'Mr. White', player: 'Trailer Park Moses', build: { discord_user_id: IDS.moses } },
  ] }));
  writeFileSync(join(dataDir, 'player-channels.json'), JSON.stringify({ crawlers: {
    Eisenhorn: { channel_id: CH.sheetCaleb, channel_name: 's1-hornn-eisenhorn' },
    Shirayuki: { channel_id: CH.sheetGrimm, channel_name: 's1-grimmtrouble-shirayuki' },
    'Mr. White': { channel_id: CH.sheetMoses, channel_name: 's1-trailer-park-moses-mr-white' },
  } }));
  writeFileSync(join(dir, 'sessions', 'state.json'), JSON.stringify({ crawlers: [
    { name: 'Horn', player: 'Hornn', build: { discord_user_id: IDS.caleb } }, { name: 'Bone Wifebeater', player: 'Trailer Park Moses', build: { discord_user_id: IDS.moses } }, { name: 'Ghost', player: '?' },
  ] }));
  writeFileSync(join(dir, 'sessions', 'player-channels.json'), JSON.stringify({ crawlers: {
    Horn: { channel_id: CH.alphaHornn, channel_name: 'hornn-sheet' }, 'Bone Wifebeater': { channel_id: CH.alphaMoses, channel_name: 'moses-sheet' }, Ghost: { channel_id: CH.alphaNobody, channel_name: 'nobody-sheet' },
  } }));
  const config = { campaign: { sessionId: 's1', dir, dataDir }, discord: { guildId: G, gmOutputChannelId: CH.gmVoice, transcriptChannelId: CH.transcript, voiceChannelId: CH.voice } };
  return { dir, dataDir, config, file: join(dir, 'sessions', 'player-roles.json') };
}

const setup = (opts = {}) => {
  const c = makeCampaign();
  const g = makeGuild();
  const roles = new PlayerRoles({ config: c.config, file: c.file, membersIntent: true, ...opts });
  return { ...c, g, roles };
};
const roleNamed = (g, name) => [...g.roles.cache.values()].find((r) => r.name === name);

test('roles: guildMemberAdd creates a role named after the handle, tracks it by user id and assigns it + Crawler', async () => {
  const { g, roles, file } = setup();
  const m = g.member(IDS.newbie, 'newcrawler');
  g.members.cache.set(m.id, m);
  const r = await roles.onMemberAdd(m);
  const personal = roleNamed(g, 'newcrawler');
  const crawler = roleNamed(g, CRAWLER_ROLE_NAME);
  assert.ok(personal && crawler, 'personal + Crawler roles exist');
  assert.equal(personal.permissions.bitfield, 0n, 'personal role carries no server permissions');
  assert.ok(m.roles.cache.has(personal.id) && m.roles.cache.has(crawler.id));
  const store = loadStore(file);
  assert.equal(store.players[IDS.newbie].role_id, personal.id, 'tracked by user id');
  assert.equal(store.crawler_role_id, crawler.id);
  assert.equal(r.players[0].created, true);
});

test('roles: Crawler role grants Deafen Members (role level) and never Mute Members; no overwrite grants Mute/Deafen', async () => {
  const { g, roles } = setup();
  await roles.sync(g);
  const crawler = roleNamed(g, CRAWLER_ROLE_NAME);
  assert.ok(crawler.permissions.has(P.DeafenMembers));
  assert.ok(!crawler.permissions.has(P.MuteMembers));
  assert.ok(!crawler.permissions.has(P.Administrator));
  for (const ch of g.channels.cache.values()) for (const ow of ch.permissionOverwrites.cache.values()) {
    if (ow.id === crawler.id) assert.equal(ow.allow.bitfield & (P.MuteMembers | P.DeafenMembers), 0n, `#${ch.name}: no channel Mute/Deafen grant`);
  }
  for (const r of g.roles.cache.values()) if (r.id !== ROLE.admin) assert.ok(!r.permissions.has(P.MuteMembers, false), `${r.name} has no Mute Members`);
});

test('roles: idempotent - a second sync / join makes no new roles, adds or overwrite edits', async () => {
  const { g, roles, config, file } = setup();
  await roles.sync(g);
  const before = g.calls.length;
  const editsBefore = [...g.channels.cache.values()].reduce((n, c) => n + c.permissionOverwrites.edits.length, 0);
  const r2 = await roles.sync(g);
  await roles.onMemberAdd(g.members.cache.get(IDS.grimm));
  assert.deepEqual(g.calls.slice(before).filter((c) => c[0] !== 'listMembers'), [], 'no role creates/adds the second time');
  assert.equal([...g.channels.cache.values()].reduce((n, c) => n + c.permissionOverwrites.edits.length, 0), editsBefore, 'no overwrite edits the second time');
  assert.equal(r2.actions.length, 0);
  // a fresh process (new manager, same store file) is idempotent too
  const again = new PlayerRoles({ config, file, membersIntent: true });
  const n = g.calls.length;
  await again.sync(g);
  assert.deepEqual(g.calls.slice(n).filter((c) => c[0] !== 'listMembers'), []);
  assert.equal([...g.roles.cache.values()].filter((r) => r.name === 'troublegrimm').length, 1);
});

test('roles: backfill gives every human a personal role, skips bots, never removes a role (admin roles stay)', async () => {
  const { g, roles } = setup();
  const r = await roles.sync(g);
  assert.deepEqual(r.players.map((p) => p.username).sort(), ['hornn428', 'trailerparkmoses', 'troublegrimm']);
  assert.ok(!roleNamed(g, 'DCC AI GM-2') && !r.players.some((p) => p.userId === IDS.gmBot), 'bots get nothing');
  const caleb = g.members.cache.get(IDS.caleb);
  assert.ok(caleb.roles.cache.has(ROLE.admin), 'Caleb keeps Admin');
  assert.ok(g.members.cache.get(IDS.moses).roles.cache.has(ROLE.admin) && g.members.cache.get(IDS.moses).roles.cache.has(ROLE.external));
  assert.deepEqual(g.members.cache.get(IDS.gmBot).added, [], 'bot roles untouched');
  assert.ok(g.calls.every((c) => ['createRole', 'addRole', 'listMembers'].includes(c[0])), `only additive calls: ${JSON.stringify(g.calls)}`);
  assert.ok(roleNamed(g, 'Admin').permissions.has(P.Administrator), 'Admin role permissions unchanged');
});

test('roles: External Agent holders get their personal role but not the Crawler base role', async () => {
  const { g, roles } = setup();
  const r = await roles.sync(g);
  const moses = r.players.find((p) => p.userId === IDS.moses);
  assert.ok(moses.roleName === 'trailerparkmoses' && !moses.crawlerAssigned && /External Agent/.test(moses.crawlerSkipped));
  const crawler = roleNamed(g, CRAWLER_ROLE_NAME);
  assert.ok(!g.members.cache.get(IDS.moses).roles.cache.has(crawler.id));
  assert.ok(g.members.cache.get(IDS.grimm).roles.cache.has(crawler.id));
});

const visible = (g, m) => [...g.channels.cache.values()].filter((c) => can(g, c.id, m, 'ViewChannel')).map((c) => c.name).sort();
const everyoneEdits = (g) => [...g.channels.cache.values()].flatMap((c) => c.permissionOverwrites.edits.filter((e) => e.id === G).map(() => c.name));

test('roles: players see only their channels + their own sheet; other sheets are hidden; @everyone never changed', async () => {
  const { g, roles } = setup();
  const r = await roles.sync(g);
  const grimm = g.members.cache.get(IDS.grimm);
  const moses = g.members.cache.get(IDS.moses);
  moses.roles.cache.delete(ROLE.admin);   // look at Moses as a plain player too
  moses.roles.cache.delete(ROLE.external);
  moses.roles.cache.set(roleNamed(g, CRAWLER_ROLE_NAME).id, roleNamed(g, CRAWLER_ROLE_NAME));
  const base = ['General', 'Text Channels', 'agents', 'create', 'general', 'gm-voice', 'table-transcript'];
  assert.deepEqual(visible(g, grimm), [...base, 's1-grimmtrouble-shirayuki'].sort());
  assert.deepEqual(visible(g, moses), [...base, 'moses-sheet', 's1-trailer-park-moses-mr-white'].sort());
  assert.ok(can(g, CH.sheetGrimm, grimm, 'ReadMessageHistory') && can(g, CH.sheetGrimm, grimm, 'SendMessages'), 'owner reads + sends own sheet');
  assert.ok(can(g, CH.alphaMoses, moses, 'ReadMessageHistory') && can(g, CH.alphaMoses, moses, 'SendMessages'), 'alpha sheet to its clear owner');
  assert.deepEqual(everyoneEdits(g), [], '@everyone overwrites are never edited');
  const gmOw = g.channels.cache.get(CH.sheetGrimm).permissionOverwrites.cache.get(IDS.gmBot);
  assert.equal(gmOw.allow.bitfield, P.ViewChannel | P.SendMessages | P.ReadMessageHistory | P.EmbedLinks, 'GM bot overwrite untouched');
  assert.ok(!g.channels.cache.get(CH.sheetCaleb).permissionOverwrites.cache.has(roleNamed(g, 'troublegrimm').id), 'no grant on another player\'s sheet');
  const nobody = r.sheets.find((x) => x.channelId === CH.alphaNobody);
  assert.match(nobody.status, /owner unclear: hidden from Crawler only/);
  assert.deepEqual(r.sheets.filter((x) => x.ownerRole).map((x) => [x.channelName, x.ownerRole]).sort(),
    [['hornn-sheet', 'hornn428'], ['moses-sheet', 'trailerparkmoses'], ['s1-grimmtrouble-shirayuki', 'troublegrimm'], ['s1-hornn-eisenhorn', 'hornn428'], ['s1-trailer-park-moses-mr-white', 'trailerparkmoses']]);
  // the owner overwrite is written before the Crawler hide on a sheet (owner never locked out mid-sync)
  const order = g.channels.cache.get(CH.sheetGrimm).permissionOverwrites.edits.map((e) => e.id);
  assert.deepEqual(order, [roleNamed(g, 'troublegrimm').id, roleNamed(g, CRAWLER_ROLE_NAME).id]);
  // an admin still sees everything
  assert.equal(visible(g, g.members.cache.get(IDS.caleb)).length, g.channels.cache.size);
});

test('roles: Crawler allow on the five text channels + GM voice only; every other channel and category hidden by a Crawler deny', async () => {
  const { g, roles } = setup();
  await roles.sync(g);
  const grimm = g.members.cache.get(IDS.grimm);
  const crawler = roleNamed(g, CRAWLER_ROLE_NAME);
  for (const id of [CH.agents, CH.gmVoice, CH.general, CH.transcript, CH.create]) {
    for (const f of ['ViewChannel', 'SendMessages', 'ReadMessageHistory']) assert.ok(can(g, id, grimm, f), `${id} ${f}`);
  }
  for (const f of ['ViewChannel', 'Connect', 'Speak', 'UseVAD', 'SendMessages', 'ReadMessageHistory']) assert.ok(can(g, CH.voice, grimm, f), `voice ${f}`);
  for (const id of [CH.hiddenVoice, CH.gmSecret, CH.other, CH.catSheets, CH.catSecret, CH.catAlpha, CH.sheetCaleb, CH.alphaNobody]) {
    assert.ok(g.channels.cache.get(id).permissionOverwrites.cache.get(crawler.id).deny.has(P.ViewChannel), `${id} denied to Crawler`);
  }
  assert.ok(!g.channels.cache.get(CH.catText).permissionOverwrites.cache.has(crawler.id), 'a category holding a players\' channel is left as is');
  // External Agent overwrites keep their exact bits
  const ext = g.channels.cache.get(CH.agents).permissionOverwrites.cache.get(ROLE.external);
  assert.equal(ext.allow.bitfield, P.ViewChannel | P.SendMessages);
  assert.equal(ext.deny.bitfield, P.MentionEveryone);
  assert.ok(g.channels.cache.get(CH.gmVoice).permissionOverwrites.cache.get(ROLE.external).deny.has(P.ViewChannel));
  for (const ch of g.channels.cache.values()) {
    const ow = ch.permissionOverwrites.cache.get(crawler.id);
    if (ow) assert.equal(ow.allow.bitfield & (P.MuteMembers | P.DeafenMembers), 0n, `#${ch.name}: no channel Mute/Deafen grant`);
  }
});

test('roles: a channel created later is hidden from Crawler at once; a players\'-list name is opened; a new sheet gets its owner', async () => {
  const { g, roles, dataDir } = setup();
  await roles.sync(g);
  const crawler = roleNamed(g, CRAWLER_ROLE_NAME);
  const mk = (id, name, type = ChannelType.GuildText) => {
    const c = { id, name, type, parentId: null, permissionOverwrites: new FakeOverwrites([]), guild: g };
    g.channels.cache.set(id, c);
    return c;
  };
  const secret = mk('51', 'gm-plans');
  assert.equal((await roles.onChannelCreate(secret)).kind, 'hidden');
  assert.ok(secret.permissionOverwrites.cache.get(crawler.id).deny.has(P.ViewChannel));
  const vc = mk('52', 'side-room', ChannelType.GuildVoice);
  await roles.onChannelCreate(vc);
  assert.ok(vc.permissionOverwrites.cache.get(crawler.id).deny.has(P.ViewChannel), 'other voice channels are hidden too');
  // /create made a sheet for Grimm's 2nd Crawler: hidden first, then lockSheets lets the owner in
  const sheet = mk('53', 's1-grimmtrouble-second');
  await roles.onChannelCreate(sheet);
  const map = JSON.parse(readFileSync(join(dataDir, 'player-channels.json'), 'utf8'));
  map.crawlers.Second = { channel_id: '53', channel_name: 's1-grimmtrouble-second' };
  writeFileSync(join(dataDir, 'player-channels.json'), JSON.stringify(map));
  const st = JSON.parse(readFileSync(join(dataDir, 'state.json'), 'utf8'));
  st.crawlers.push({ name: 'Second', player: 'Grimmtrouble', build: { discord_user_id: IDS.grimm } });
  writeFileSync(join(dataDir, 'state.json'), JSON.stringify(st));
  await roles.lockSheets(g);
  const grimm = g.members.cache.get(IDS.grimm);
  assert.ok(can(g, '53', grimm, 'ViewChannel') && can(g, '53', grimm, 'SendMessages'));
  const outsider = g.member(IDS.newbie, 'newcrawler');
  g.members.cache.set(outsider.id, outsider);
  await roles.onMemberAdd(outsider);
  assert.ok(!can(g, '53', outsider, 'ViewChannel') && !can(g, '51', outsider, 'ViewChannel'));
});

test('roles: handle collisions get a suffix; a changed handle renames the tracked role; bots are ignored on join', async () => {
  const { g, roles } = setup();
  g.roles.cache.set('77', { id: '77', name: 'troublegrimm', permissions: bits(P.ManageMessages), managed: false });   // someone else's role with that name
  assert.equal(uniqueRoleName(g, 'troublegrimm'), 'troublegrimm-2');
  await roles.sync(g);
  const grimm = g.members.cache.get(IDS.grimm);
  assert.ok(grimm.roles.cache.has(roleNamed(g, 'troublegrimm-2').id) && !grimm.roles.cache.has('77'));
  grimm.user.username = 'grimm2026';
  await roles.onMemberAdd(grimm);
  assert.ok(roleNamed(g, 'grimm2026'), 'tracked role follows the new handle');
  const bot = g.member('600', 'somebot', [], true);
  assert.equal(await roles.onMemberAdd(bot), null);
});

test('roles: concurrent lazy sightings create exactly one role; a known member is a no-op', async () => {
  const { g, roles } = setup();
  const m = g.member(IDS.newbie, 'newcrawler');
  g.members.cache.set(m.id, m);
  await Promise.all([roles.ensureKnown(m), roles.ensureKnown(m), roles.onMemberAdd(m)]);
  assert.equal([...g.roles.cache.values()].filter((r) => r.name.startsWith('newcrawler')).length, 1);
  const n = g.calls.length;
  assert.equal(await roles.ensureKnown(m), null);
  assert.equal(g.calls.length, n);
});

test('roles: without the GuildMembers intent the backfill uses known ids (sheet owners, member overwrites, owner) and never lists members', async () => {
  const { g, roles } = setup({ membersIntent: false });
  const r = await roles.sync(g);
  assert.ok(!g.calls.some((c) => c[0] === 'listMembers'));
  assert.deepEqual(r.players.map((p) => p.userId).sort(), [IDS.caleb, IDS.grimm, IDS.moses].sort());
  assert.match(formatReport(r), /GuildMembers intent off/);
});

test('roles: dry run changes nothing and writes no store', async () => {
  const { g, roles, file } = setup({ dryRun: true });
  const r = await roles.sync(g);
  assert.deepEqual(g.calls.filter((c) => c[0] !== 'listMembers'), []);
  assert.equal([...g.channels.cache.values()].reduce((n, c) => n + c.permissionOverwrites.edits.length, 0), 0);
  assert.throws(() => readFileSync(file));
  assert.ok(r.actions.some((a) => /created role troublegrimm/.test(a)));
  assert.ok(r.sheets.filter((s) => s.ownerId).every((s) => s.status === 'locked'), 'dry run reports the sheet locks it would make');
});

test('roles: an existing Crawler role only gains Deafen Members, keeping its other bits', async () => {
  const { g, roles } = setup();
  g.roles.cache.set('88', { id: '88', name: CRAWLER_ROLE_NAME, managed: false, permissions: bits(P.ChangeNickname), async setPermissions(p) { this.permissions = bits(BigInt(p)); } });
  await roles.ensureCrawlerRole(g);
  const r = g.roles.cache.get('88');
  assert.ok(r.permissions.has(P.ChangeNickname) && r.permissions.has(P.DeafenMembers));
});

test('roles: sheetOwners maps every session\'s sheet channels (active first, then alpha) to state.json discord_user_id', () => {
  const { config } = makeCampaign();
  const s = sheetOwners(config);
  assert.deepEqual(s.map((x) => [x.channelId, x.ownerId]), [[CH.sheetCaleb, IDS.caleb], [CH.sheetGrimm, IDS.grimm], [CH.sheetMoses, IDS.moses], [CH.alphaHornn, IDS.caleb], [CH.alphaMoses, IDS.moses], [CH.alphaNobody, null]]);
});

test('voice guard: bridge bot is unmuted when server-muted, never undeafened, nothing posted; other members ignored', async () => {
  const calls = [];
  const guard = createVoiceGuard({ getBotId: () => 'BOT', guildId: G });
  const state = (over) => ({ id: 'BOT', guild: { id: G }, channelId: CH.voice, serverMute: false, serverDeaf: false,
    channel: { send: async () => calls.push(['send']), isTextBased: () => true },
    async setMute(v) { calls.push(['mute', v]); }, async setDeaf(v) { calls.push(['deaf', v]); }, ...over });
  assert.equal((await guard(state(), state({ serverMute: true }))).action, 'unmuted');
  assert.deepEqual(calls, [['mute', false]]);
  calls.length = 0;
  assert.equal((await guard(state(), state({ serverDeaf: true }))).action, 'deafened');
  assert.equal((await guard(state({ serverDeaf: true }), state({ serverDeaf: false }))).action, 'undeafened');
  assert.equal((await guard(state({ channelId: null }), state({ serverDeaf: true }))).action, 'deafened');
  assert.deepEqual(calls, [], 'no undeafen and nothing posted anywhere');
  assert.equal((await guard(state({ id: 'P1' }), state({ id: 'P1', serverMute: true }))).action, 'ignored');
  assert.equal((await guard(state({ guild: { id: 'other' } }), state({ guild: { id: 'other' }, serverMute: true }))).action, 'ignored');
  assert.deepEqual(calls, []);
  assert.equal(createVoiceGuard.length, 1);
});

test('voice guard: index.js wires no note/post for deafen', () => {
  const src = readFileSync(fileURLToPath(new URL('../src/index.js', import.meta.url)), 'utf8');
  const i = src.indexOf('createVoiceGuard({');
  const call = src.slice(i, src.indexOf('});', i));
  assert.ok(i > 0 && !/note|send\(/.test(call));
  assert.ok(!/deafened/.test(readFileSync(fileURLToPath(new URL('../src/roles.js', import.meta.url)), 'utf8').match(/createVoiceGuard[\s\S]*?\n}\n/)[0].replace(/log\.info\([^\n]*\n/g, '').replace(/action = [^\n]*\n/g, '').replace(/\* [^\n]*\n/g, '')), 'no deafen message text outside the local log');
});

test('members intent: detected from application flags; env can force it; failures default to off', async () => {
  assert.equal(membersIntentFromFlags(1 << 14), true);
  assert.equal(membersIntentFromFlags(1 << 15), true);
  assert.equal(membersIntentFromFlags(2621440), false);   // the live app's flags on Oct 6 2026 (message content only)
  const fetchImpl = async () => ({ ok: true, json: async () => ({ flags: 1 << 15 }) });
  assert.deepEqual(await detectMembersIntent('t', { env: {}, fetchImpl }), { enabled: true, source: 'api' });
  assert.equal((await detectMembersIntent('t', { env: { DISCORD_MEMBERS_INTENT: 'false' }, fetchImpl })).enabled, false);
  assert.equal((await detectMembersIntent('t', { env: {}, fetchImpl: async () => { throw new Error('offline'); } })).enabled, false);
  assert.equal((await detectMembersIntent('t', { env: {}, fetchImpl: async () => ({ ok: false, status: 401 }) })).enabled, false);
});

test('roles: /create locks the new sheet channel after setup-channels and before the first card is published', () => {
  const src = readFileSync(fileURLToPath(new URL('../src/create/commit.js', import.meta.url)), 'utf8');
  const a = src.indexOf("'setup-channels'");
  const l = src.indexOf('ctx.lockSheetChannels()');
  const p = src.indexOf("'publish', '--crawler'");
  assert.ok(a > 0 && l > a && p > l, 'setup-channels -> lockSheetChannels -> publish');
});

test('roles: source has no hard-coded box paths', () => {
  for (const f of ['../src/roles.js', '../scripts/roles-sync.js']) {
    const src = readFileSync(fileURLToPath(new URL(f, import.meta.url)), 'utf8');
    assert.ok(!/\/workspace|\/home\/box/.test(src), f);
  }
});
