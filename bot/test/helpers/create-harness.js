/** Fake Discord interactions for driving the /create flow end to end against a real (temp) campaign dir. */
import { cpSync, existsSync, mkdirSync, mkdtempSync, symlinkSync, readFileSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { resolveCampaignRoot } from '../../src/paths.js';
import { handleInteraction } from '../../src/commands/index.js';

export const REAL_CAMPAIGN = process.env.DCC_REAL_CAMPAIGN || resolveCampaignRoot();

const SANDBOXES = [];
process.on('exit', () => {
  if (process.env.KEEP_SANDBOX) return;
  for (const d of SANDBOXES) { try { rmSync(d, { recursive: true, force: true }); } catch { /* best effort */ } }
});

/** A sandbox campaign: real tools (symlink) + real tables (copy) + a fresh `beta` session made by tools/new-session.py. */
export function makeSandbox(sessionId = 'beta', extraArgs = []) {
  const dir = mkdtempSync(join(tmpdir(), 'dcc-create-'));
  SANDBOXES.push(dir);
  symlinkSync(join(REAL_CAMPAIGN, 'tools'), join(dir, 'tools'));
  cpSync(join(REAL_CAMPAIGN, 'tables'), join(dir, 'tables'), { recursive: true });
  mkdirSync(join(dir, 'gm-notes'), { recursive: true });
  mkdirSync(join(dir, 'sessions'), { recursive: true });
  const env = { ...process.env, DCC_CAMPAIGN_DIR: dir, DCC_AUTO_PUBLISH: '0' };
  delete env.DCC_SESSION;
  execFileSync('python3', [join(dir, 'tools', 'new-session.py'), sessionId, '--label', 'Test', ...extraArgs], { env, stdio: 'pipe' });
  return dir;
}

export function makeCtx(dir, sessionId = 'beta', over = {}) {
  const dataDir = join(dir, 'sessions-data', sessionId);
  const sent = [];
  return {
    config: {
      discord: { guildId: 'G1' },
      campaign: { sessionId, dir, dataDir, charactersDir: join(dataDir, 'characters') },
      create: { enabled: true, python: 'python3', publish: false },
    },
    logger: { info() {}, warn() {}, error(...a) { console.error(...a); } },
    client: { channels: { fetch: async () => ({ send: async (m) => sent.push(m) }) }, users: { fetch: async (id) => ({ send: async (m) => sent.push({ dm: id, ...m }) }) } },
    staffSent: sent,
    ...over,
  };
}

const flat = (msg) => (msg?.components ?? []).flatMap((r) => (r.toJSON ? r.toJSON() : r).components);

export class Player {
  constructor(ctx, id, name) {
    this.ctx = ctx;
    this.user = { id, username: name.toLowerCase(), globalName: name };
    this.msg = null; // last rendered payload {embeds, components}
    this.pendingModal = null;
    this.lastText = '';
  }

  fake(extra) {
    const self = this;
    return {
      user: this.user, guildId: 'G1', inGuild: () => true, memberPermissions: { has: () => !!self.perms },
      isAutocomplete: () => false, isChatInputCommand: () => false, isButton: () => false, isStringSelectMenu: () => false, isModalSubmit: () => false,
      isMessageComponent: () => false, isFromMessage: () => true, deferred: false, replied: false,
      async reply(p) { self.capture(p); this.replied = true; },
      async update(p) { self.capture(p); },
      async deferUpdate() { this.deferred = true; },
      async editReply(p) { self.capture(p); },
      async followUp(p) { self.followups.push(p); },
      async showModal(m) { self.pendingModal = m; },
      ...extra,
    };
  }

  followups = [];

  capture(p) {
    if (p.embeds || p.components) this.msg = p;
    this.lastText = [p.content, ...(p.embeds ?? []).map((e) => { const j = e.toJSON ? e.toJSON() : e; return `${j.title ?? ''}\n${j.description ?? ''}`; })].filter(Boolean).join('\n');
  }

  options(map = {}) {
    return { getString: (k) => map[k] ?? null, getUser: (k) => map[k] ?? null };
  }

  async command(map = {}) {
    const i = this.fake({ isChatInputCommand: () => true, commandName: 'create', options: this.options(map) });
    this.lastText = '';
    await handleInteraction(i, this.ctx);
    return this.lastText;
  }

  components() { return flat(this.msg); }
  find(pred) { return this.components().find(pred); }
  byKey(screenKey) { return this.components().find((c) => c.custom_id?.includes(`:${screenKey}`) && (c.custom_id.endsWith(`:${screenKey}`) || c.custom_id.includes(`:${screenKey}:`))); }

  async click(label) {
    const c = this.find((x) => x.label === label || x.label?.startsWith(label) || x.label?.endsWith(` ${label}`) || x.custom_id?.endsWith(`:${label}`));
    if (!c) throw new Error(`no button "${label}". Have: ${this.components().map((x) => x.label ?? x.custom_id).join(' | ')}\n${this.lastText}`);
    if (c.disabled) throw new Error(`button "${label}" is disabled\n${this.lastText}`);
    await handleInteraction(this.fake({ isButton: () => true, isMessageComponent: () => true, customId: c.custom_id }), this.ctx);
  }

  async choose(key, values) {
    const c = this.byKey(key);
    if (!c) throw new Error(`no menu "${key}". Have: ${this.components().map((x) => x.custom_id).join(' | ')}\n${this.lastText}`);
    await handleInteraction(this.fake({ isStringSelectMenu: () => true, isMessageComponent: () => true, customId: c.custom_id, values: [].concat(values) }), this.ctx);
  }

  async chooseId(customId, values) {
    await handleInteraction(this.fake({ isStringSelectMenu: () => true, isMessageComponent: () => true, customId, values: [].concat(values) }), this.ctx);
  }

  /** Click a button that opens a modal, then submit it with `fields` {id: text}. Returns the modal's field ids. */
  async form(buttonKey, fields) {
    this.pendingModal = null;
    const c = this.byKey(buttonKey);
    if (!c) throw new Error(`no button "${buttonKey}". Have: ${this.components().map((x) => x.custom_id).join(' | ')}\n${this.lastText}`);
    await handleInteraction(this.fake({ isButton: () => true, isMessageComponent: () => true, customId: c.custom_id }), this.ctx);
    if (!this.pendingModal) throw new Error(`"${buttonKey}" did not open a modal\n${this.lastText}`);
    const m = this.pendingModal.toJSON();
    const ids = m.components.map((r) => r.components[0].custom_id);
    await handleInteraction(this.fake({ isModalSubmit: () => true, customId: m.custom_id, fields: { getTextInputValue: (id) => { if (!ids.includes(id)) throw new Error('nf'); return fields[id] ?? ''; } } }), this.ctx);
    return ids;
  }

  async nav(what) { await this.click(what); }
  disabled(label) { return !!this.find((x) => x.label?.startsWith(label))?.disabled; }
  screen() { return /^(S\d+) ·/.exec(this.lastText)?.[1] ?? null; }
}

export const read = (p) => JSON.parse(readFileSync(p, 'utf8'));
export const exists = existsSync;

/** Walk one player through S1-S16 (stops on the review screen; call p.click('Confirm') then p.click('Confirm and lock')). */
export async function drive(p, o = {}) {
  const O = { name: 'Ann', species: 'Human', cls: 'Fighter', bg: 'Soldier', ...o };
  if (!/S2/.test(p.lastText)) { await p.click('ACCEPT'); }
  if (O.optouts) await p.form('S2:edit', O.optouts);
  await p.click(O.optouts ? 'Next' : 'Skip');
  await p.form('S3:name', { name: O.name });
  if (p.find((x) => x.custom_id?.endsWith(':anyway'))) await p.click('Use it anyway');
  await p.click('Next');
  await p.form('S4:edit', { look: 'Sweatpants and regret', hook: 'Hits things very hard' });
  await p.click('Next');
  await p.choose('S5:species', O.species);
  if (p.byKey('S5:sub')) await p.choose('S5:sub', O.speciesSub ?? R_FIRST_SUB[O.species]);
  await p.click('Next');
  await p.choose('S6:class', O.cls);
  if (O.classChoice) for (const [k, v] of Object.entries(O.classChoice)) await p.choose(`S6:choice:${k}`, v);
  else if (p.components().some((c) => c.custom_id?.includes('S6:choice'))) await p.click('Pick for me');
  await p.click('Next');
  await p.choose('S7:bg', O.bg);
  await p.choose('S7:asi', O.asi ?? firstOption(p, 'S7:asi'));
  if (p.byKey('S7:feat')) await p.choose('S7:feat', O.extraFeat ?? firstOption(p, 'S7:feat'));
  await p.click('Next');
  if (O.onS8) await O.onS8(p);   // e.g. the Roll method (test/roll.test.js)
  else {
    await p.click(O.method === 'pointbuy' ? 'Point buy' : 'Standard array');
    if (O.scores) await p.form('S8:enter', { scores: O.scores }); else await p.click('Pick for me');
  }
  await p.click('Next');
  await p.click('Pick for me'); if (O.onS9) await O.onS9(p); await p.click('Next'); // S9
  if (O.kit) {
    await p.choose('S10:kc', O.kit.kc); await p.choose('S10:kb', O.kit.kb);
    for (const c of p.components().filter((x) => x.custom_id?.includes(':S10:var:'))) await p.chooseId(c.custom_id, O.kit.variants?.[c.custom_id.split(':').pop().split('~')[0]] ?? c.options[0].value);
    if (O.kit.shop) await p.form('S10:shop', { list: O.kit.shop });
  } else { await p.click('Pick for me'); if (O.noShop) await p.click('Clear shopping'); }
  await p.click('Next'); // S10
  if (p.screen() === 'S11') { if (O.onS11) await O.onS11(p); else { await p.click('Pick for me'); await p.click('Next'); } }
  // S12 (fan tags) is retired and skipped by the flow
  if (O.survey) { await p.form('S13:a', O.survey); await p.click('Next'); } else await p.click('Skip'); // S13
  await p.form('S14:edit', { story: 'Used to run a mid-size laundromat.', handle: O.handle ?? '' });
  await p.click('Next');
  await p.form('S15:edit', { orders: 'Make for the nearest saferoom and stay out of fights.', react: '', sig: '' });
  await p.click('Next');
}

export async function finish(p) {
  await p.click('Confirm ▸');
  await p.click('Confirm and lock the file');
  return p.lastText;
}

const R_FIRST_SUB = { Dragonborn: 'Red', Elf: 'High Elf', Gnome: 'Rock Gnome', Goliath: 'Hill', Tiefling: 'Infernal' };
function firstOption(p, key) {
  const c = p.byKey(key);
  const opts = c.options ?? [];
  return opts[0]?.value;
}
