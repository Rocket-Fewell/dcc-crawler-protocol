import assert from 'node:assert/strict';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { PermissionFlagsBits } from 'discord.js';
import * as enc from '../src/commands/encounter.js';
import { commandData, commands, handleInteraction } from '../src/commands/index.js';
import { MAX_MESSAGE, buildPreview, hintFor, hintText, listEntries, loadPage, resolvePointer, splitText, toMessages } from '../src/encounter/extract.js';

const REAL = process.env.DCC_REAL_CAMPAIGN || '/workspace/dcc-campaign';
const haveReal = [1, 2, 3, 4, 5].every((n) => existsSync(join(REAL, 'floors', 'f01', `day-0${n}.json`)));
const tmps = [];
process.on('exit', () => { for (const d of tmps) { try { rmSync(d, { recursive: true, force: true }); } catch { /* best effort */ } } });

// ---------------------------------------------------------------- fixtures
const GM_SECRET = 'GMONLY-SECRET-STRING-do-not-leak';
function fixtureDoc(over = {}) {
  return {
    meta: { title: `${GM_SECRET} meta title` },
    gm_stuff: { quick_run: `${GM_SECRET} quick run`, loot_hooks: [`${GM_SECRET} loot hook`] },
    day: {
      gm_warning: `${GM_SECRET} day gm warning`,
      tomorrow_notice: { text: 'Tomorrow the middle closes. Take what you need.', tag: '[PLAYER-FACING]', gm_note: `${GM_SECRET} tomorrow gm note`, hours_note: `${GM_SECRET} hours note` },
      collapse_notice: { text: 'The floor collapses in {hours} hours. Crawlers, move.', hours_note: `${GM_SECRET} collapse hours note`, status: `${GM_SECRET} status` },
      floor_exit: { system_line: { text: 'The floor has closed.' }, gm_warning: { text: 'Reach a stairwell or you do not leave.' } },
    },
    routes: [{ id: 'route-dash', title: `${GM_SECRET} route title`, voice_lines: { system_intro: { text: 'Dash route intro.', source: `${GM_SECRET} src` } } }],
    encounters: [
      { id: 'enc-t-01', title: `${GM_SECRET} enc title`, scaling: `${GM_SECRET} scaling`, stall_fallback: `${GM_SECRET} stall`, if_they_do_something_dumb: `${GM_SECRET} dumb`,
        voice_lines: { system_intro: { text: 'Welcome to the test room.', canon_tag: GM_SECRET }, win: { text: 'You won. Here are some credits.' } },
        zone_color: { lines: [{ text: 'It smells of old popcorn.' }, { text: 'Something drips.' }] },
        set_piece_intro: { title: `${GM_SECRET} sp title`, text: 'Para one. Para two. Para three.', paragraphs: [{ n: 1, text: 'Para one.' }, { n: 2, text: 'Para two.' }, { n: 3, text: 'Para three.', optional: true }], gm_note: `${GM_SECRET} sp note` },
        proposed_achievements: [{ name: `${GM_SECRET} ach name`, trigger: `${GM_SECRET} trig`, reward_slot: `${GM_SECRET} reward`, narration: 'Achievement unlocked: Test Pilot.' }],
        carry_on: `${GM_SECRET} carry`, quick_run: `${GM_SECRET} qr`, map_in_the_mind: `${GM_SECRET} map` },
    ],
    audience_manifest: {
      schema: 'audience/1', default: 'gm',
      player_blocks: [
        { path: '/routes/0/voice_lines/system_intro', kind: 'route_voice_line', field: 'text' },
        { path: '/encounters/0/voice_lines/system_intro', kind: 'voice_line', field: 'text', encounter: 'enc-t-01' },
        { path: '/encounters/0/voice_lines/win', kind: 'voice_line', field: 'text', encounter: 'enc-t-01' },
        { path: '/encounters/0/zone_color/lines/0', kind: 'zone_color', field: 'text', encounter: 'enc-t-01', optional: true },
        { path: '/encounters/0/zone_color/lines/1', kind: 'zone_color', field: 'text', encounter: 'enc-t-01', optional: true },
        { path: '/encounters/0/set_piece_intro', kind: 'set_piece', field: 'paragraphs', encounter: 'enc-t-01', set_piece: true, paragraphs_optional: [false, false, true], text_field_joined: 'text' },
        { path: '/encounters/0/proposed_achievements/0', kind: 'achievement_narration', field: 'narration', encounter: 'enc-t-01', show_only_when: 'the achievement is awarded' },
        { path: '/day/tomorrow_notice', kind: 'system_notice', field: 'text' },
        { path: '/day/collapse_notice', kind: 'system_notice', field: 'text', needs_fill: ['hours'] },
        { path: '/day/floor_exit/system_line', kind: 'system_notice', field: 'text' },
        { path: '/day/floor_exit/gm_warning', kind: 'exit_warning_read_aloud', field: 'text' },
      ],
    },
    ...over,
  };
}
function campaignWith(docs) {
  const dir = mkdtempSync(join(tmpdir(), 'dcc-enc-'));
  tmps.push(dir);
  mkdirSync(join(dir, 'floors', 'f01'), { recursive: true });
  for (const [n, d] of Object.entries(docs)) writeFileSync(join(dir, 'floors', 'f01', `day-0${n}.json`), typeof d === 'string' ? d : JSON.stringify(d));
  return dir;
}

// ---------------------------------------------------------------- fake interactions
function fakeSlash(opts = {}, { manage = true, owner = false, uid = '111' } = {}) {
  const log = { replies: [], followUps: [] };
  const o = { day: 1, ...opts };
  return {
    log,
    commandName: 'encounter',
    user: { id: uid },
    guild: { ownerId: owner ? uid : 'someone-else' },
    memberPermissions: { has: (f) => manage && f === PermissionFlagsBits.ManageGuild },
    options: {
      getInteger: (k) => o[k] ?? null, getString: (k) => o[k] ?? null, getBoolean: (k) => o[k] ?? null, getNumber: (k) => o[k] ?? null,
      getFocused: (full) => (full ? { name: o.focusedName, value: o.focusedValue ?? '' } : o.focusedValue ?? ''),
    },
    reply: async (m) => { log.replies.push(m); },
    followUp: async (m) => { log.followUps.push(m); },
    respond: async (c) => { log.choices = c; },
  };
}
const ctxFor = (dir) => ({ config: { campaign: { dir } }, logger: { info() {}, warn() {}, error() {} } });
const allText = (log) => [...log.replies, ...log.followUps].map((m) => m.content).join('\n---\n');
const isEph = (m) => (m.flags & 64) === 64;

function fakeButton(customId, { uid = '111', manage = true } = {}) {
  const sent = [];
  const log = { updates: [], replies: [], sent };
  return {
    log, customId, user: { id: uid }, guild: { ownerId: 'x' },
    memberPermissions: { has: (f) => manage && f === PermissionFlagsBits.ManageGuild },
    channel: { send: async (m) => { sent.push(m); } },
    update: async (m) => { log.updates.push(m); }, reply: async (m) => { log.replies.push(m); },
  };
}
const tokenOf = (log) => log.followUps.at(-1).components[0].components[0].data.custom_id.split(':')[3];

// ---------------------------------------------------------------- registration
test('/encounter is in the command list (register payload) and routes its buttons; nothing is registered by tests', () => {
  assert.ok(commands.has('encounter'));
  const d = commandData.find((c) => c.name === 'encounter');
  assert.ok(d);
  assert.equal(d.default_member_permissions, String(PermissionFlagsBits.ManageGuild));
  assert.deepEqual(d.options.map((o) => o.name), ['day', 'encounter', 'block', 'include_optional', 'hours', 'confirm', 'floor']);
  assert.equal(d.options[0].required, true);
});

test('the command source never says cash or champs', () => {
  for (const f of ['../src/commands/encounter.js', '../src/encounter/extract.js']) {
    const src = readFileSync(new URL(f, import.meta.url), 'utf8');
    assert.doesNotMatch(src, /\bcash\b|\bchamps?\b/i, f);
  }
});

// ---------------------------------------------------------------- extraction basics
test('only the named field of each manifest entry is read; System lines are bold-tagged, narration is plain', () => {
  const doc = fixtureDoc();
  const r = buildPreview(doc, { encounter: 'enc-t-01', includeOptional: true, confirm: true });
  const out = r.messages.join('\n');
  assert.match(out, /\*\*\[SYSTEM\]\*\* Welcome to the test room\./);
  assert.match(out, /\*\*\[GM\]\*\* It smells of old popcorn\./, 'narration in a message that also has a System line carries [GM]');
  assert.doesNotMatch(out, /GMONLY/);
  const only = buildPreview(doc, { encounter: 'enc-t-01', block: 'zone_color', includeOptional: true });
  assert.ok(!only.messages[0].includes('**['), 'a pure narration message has no tags');
});

test('encounter scope: none = day-level notices only, id = that encounter, route id works, all = everything, unknown id lists the options', () => {
  const doc = fixtureDoc();
  const day = buildPreview(doc, { hours: 6 }).messages.join('\n');
  assert.match(day, /Tomorrow the middle closes/);
  assert.doesNotMatch(day, /test room|Dash route/);
  assert.match(buildPreview(doc, { encounter: 'route-dash' }).messages.join('\n'), /Dash route intro\./);
  assert.match(buildPreview(doc, { encounter: 'ALL', hours: 3, includeOptional: true, confirm: true }).messages.join('\n'), /Dash route intro[\s\S]*test room[\s\S]*Tomorrow/);
  const bad = buildPreview(doc, { encounter: 'enc-nope' });
  assert.match(bad.error, /No encounter or route "enc-nope"[\s\S]*`enc-t-01`/);
});

test('block filter matches a kind or a slot name', () => {
  const doc = fixtureDoc();
  assert.match(buildPreview(doc, { encounter: 'enc-t-01', block: 'win' }).messages[0], /You won/);
  const kind = buildPreview(doc, { encounter: 'enc-t-01', block: 'voice_line' }).messages.join('\n');
  assert.match(kind, /test room[\s\S]*You won/);
  assert.match(buildPreview(doc, { block: 'floor_exit_warning' }).messages[0], /Reach a stairwell/);   // the key is called gm_warning, the text is for players
  assert.match(buildPreview(doc, { encounter: 'enc-t-01', block: 'nonsense' }).error, /No "nonsense" block/);
});

test('day.floor_exit.gm_warning is shown (player-facing); day.gm_warning (GM-only) never is', () => {
  const out = buildPreview(fixtureDoc(), { block: 'all', hours: 6 }).messages.join('\n');
  assert.match(out, /Reach a stairwell or you do not leave/);
  assert.doesNotMatch(out, /day gm warning/);
});

// ---------------------------------------------------------------- optional / show_only_when / needs_fill
test('optional zone-colour lines and optional set-piece paragraphs are skipped unless asked', () => {
  const doc = fixtureDoc();
  const base = buildPreview(doc, { encounter: 'enc-t-01', block: 'set_piece' });
  assert.equal(base.messages.join(''), 'Para one.\n\nPara two.');
  assert.match(base.notes.join(' '), /1 optional line skipped\. Add `include_optional:true`/);
  assert.match(buildPreview(doc, { encounter: 'enc-t-01', block: 'set_piece', includeOptional: true }).messages.join(''), /Para three\./);
  const zc = buildPreview(doc, { encounter: 'enc-t-01', block: 'zone_color' });
  assert.equal(zc.messages.length, 0);
  assert.match(zc.notes.join(' '), /2 optional lines skipped/);
  assert.match(buildPreview(doc, { encounter: 'enc-t-01', block: 'zone_color', includeOptional: true }).messages[0], /popcorn[\s\S]*drips/);
});

test('show_only_when blocks are held back with an ephemeral note until confirm:true', () => {
  const doc = fixtureDoc();
  const r = buildPreview(doc, { encounter: 'enc-t-01', block: 'achievement_narration' });
  assert.equal(r.messages.length, 0);
  assert.match(r.notes.join(' '), /1 block held back: shown only when the achievement is awarded\. Add `confirm:true`/);
  const conf = buildPreview(doc, { encounter: 'enc-t-01', block: 'achievement_narration', confirm: true }).messages[0];
  assert.match(conf, /Achievement unlocked: Test Pilot\./);
  assert.doesNotMatch(conf, /\[SYSTEM\]/);
});

test('collapse_notice needs hours: refused with a clear message when missing, filled (and trimmed to a plain number) when given', () => {
  const doc = fixtureDoc();
  const miss = buildPreview(doc, { block: 'collapse_notice' });
  assert.match(miss.error, /placeholder the GM fills\. Re-run with `hours:<number>`/);
  assert.deepEqual(miss.messages, []);
  assert.equal(buildPreview(doc, {}).error?.slice(0, 20), 'The collapse notice ', 'a plain day-level run also refuses, nothing is half-shown');
  assert.match(buildPreview(doc, { block: 'collapse_notice', hours: 6 }).messages[0], /collapses in 6 hours\./);
  assert.match(buildPreview(doc, { block: 'collapse_notice', hours: 5.5 }).messages[0], /in 5\.5 hours/);
  assert.match(buildPreview(doc, { block: 'collapse_notice', hours: 0 }).messages[0], /in 0 hours/);
  assert.doesNotMatch(buildPreview(doc, { block: 'collapse_notice', hours: 6 }).messages[0], /\{hours\}/);
});

test('other fills and stray placeholders are skipped with a note, never shown raw', () => {
  const doc = fixtureDoc();
  doc.audience_manifest.player_blocks.push({ path: '/day/tomorrow_notice', kind: 'system_notice', field: 'text', needs_fill: ['zone'] });
  doc.day.floor_exit.system_line.text = 'Go to {zone} now.';
  const r = buildPreview(doc, { hours: 4 });
  assert.doesNotMatch(r.messages.join('\n'), /\{/);
  assert.match(r.notes.join(' '), /Skipped \(not filled\)[\s\S]*still has \{zone\}[\s\S]*needs zone/);
});

// ---------------------------------------------------------------- length splitting
test('long text is split under the Discord limit, short blocks are grouped, order is kept', () => {
  const sentence = 'The System would like a word with every Crawler in the room. ';
  const long = sentence.repeat(120).trim();              // ~7,000 characters
  const msgs = toMessages([{ voice: 'system', text: long }, { voice: 'gm', text: 'After the long one.' }]);
  assert.ok(msgs.length >= 4);
  assert.ok(msgs.every((m) => m.length <= MAX_MESSAGE && m.length <= 2000));
  assert.ok(msgs.slice(0, -1).every((m) => m.startsWith('**[SYSTEM]** ')), 'every piece of a System text keeps the tag');
  assert.match(msgs.at(-1), /After the long one\.$/);
  assert.equal(toMessages([{ voice: 'gm', text: 'a' }, { voice: 'gm', text: 'b' }, { voice: 'system', text: 'c' }]).length, 1);
  const w = splitText('x'.repeat(5000), 1900);
  assert.deepEqual(w.map((s) => s.length), [1900, 1900, 1200]);
  assert.deepEqual(toMessages([]), []);
});

test('many mid-size blocks are grouped greedily, each message within the limit', () => {
  const items = Array.from({ length: 30 }, (_, i) => ({ voice: i % 2 ? 'system' : 'gm', text: `Block ${i}. ` + 'word '.repeat(60).trim() }));
  const msgs = toMessages(items);
  assert.ok(msgs.length > 1 && msgs.length < 30);
  assert.ok(msgs.every((m) => m.length <= 2000));
});

// ---------------------------------------------------------------- loading
test('files are loaded fresh on every call and a missing, broken or manifest-less page is a friendly error, never a crash', async () => {
  const dir = campaignWith({ 1: fixtureDoc() });
  const ctx = ctxFor(dir);
  let i = fakeSlash({ day: 1, hours: 2 });
  await enc.execute(i, ctx);
  assert.match(allText(i.log), /Tomorrow the middle closes/);
  writeFileSync(join(dir, 'floors', 'f01', 'day-01.json'), JSON.stringify({ ...fixtureDoc(), day: { ...fixtureDoc().day, tomorrow_notice: { text: 'REBUILT notice.' } } }));
  i = fakeSlash({ day: 1, hours: 2 });
  await enc.execute(i, ctx);
  assert.match(allText(i.log), /REBUILT notice/, 'no restart needed for a rebuilt page');
  assert.doesNotMatch(allText(i.log), /Tomorrow the middle closes/);

  i = fakeSlash({ day: 3 });
  await enc.execute(i, ctx);
  assert.match(i.log.replies[0].content, /There is no page for Floor 1 Day 3 yet/);
  assert.ok(isEph(i.log.replies[0]));
  i = fakeSlash({ day: 1, floor: 2 });
  await enc.execute(i, ctx);
  assert.match(i.log.replies[0].content, /Only Floor 1 pages exist so far: there is no page for Floor 2 Day 1/);
  writeFileSync(join(dir, 'floors', 'f01', 'day-02.json'), '{"half":');
  i = fakeSlash({ day: 2 });
  await enc.execute(i, ctx);
  assert.match(i.log.replies[0].content, /not valid JSON right now/);
  writeFileSync(join(dir, 'floors', 'f01', 'day-04.json'), JSON.stringify({ day: { tomorrow_notice: { text: 'leak?' } } }));
  i = fakeSlash({ day: 4 });
  await enc.execute(i, ctx);
  assert.match(i.log.replies[0].content, /no audience manifest, so nothing on it can be shown/);
  assert.doesNotMatch(i.log.replies[0].content, /leak\?/);
  assert.throws(() => loadPage(dir, 1, 9), /Day must be/);
  assert.throws(() => loadPage(dir, 99, 1), /Floor must be/);
});

test('a manifest pointing at nothing, or at a non-string, is skipped quietly', () => {
  const doc = fixtureDoc();
  doc.audience_manifest.player_blocks.push({ path: '/day/does/not/exist', kind: 'system_notice', field: 'text' }, { path: '/day/tomorrow_notice', kind: 'system_notice', field: 'tag_missing' },
    { path: '/__proto__', kind: 'system_notice', field: 'constructor' }, { path: '/day/tomorrow_notice', kind: 'system_notice', field: '__proto__' });
  const r = buildPreview(doc, { hours: 1 });
  assert.ok(r.messages.length >= 1);
  assert.equal(resolvePointer(doc, '/__proto__'), undefined);
  assert.equal(resolvePointer(doc, 'nope'), undefined);
});

// ---------------------------------------------------------------- the command: preview, hint, permission, post
test('non-GMs are refused, ephemerally, before any file is read', async () => {
  const ctx = ctxFor('/nonexistent-dir-should-never-be-read');
  const i = fakeSlash({ day: 1 }, { manage: false });
  await enc.execute(i, ctx);
  assert.match(i.log.replies[0].content, /Manage Server/);
  assert.ok(isEph(i.log.replies[0]));
  assert.equal(i.log.followUps.length, 0);
  const owner = fakeSlash({ day: 1, hours: 2 }, { manage: false, owner: true });
  await enc.execute(owner, ctxFor(campaignWith({ 1: fixtureDoc() })));
  assert.match(allText(owner.log), /Preview/);
  const ac = fakeSlash({ day: 1, focusedName: 'encounter' }, { manage: false });
  await enc.autocomplete(ac, ctx);
  assert.deepEqual(ac.log.choices, []);
});

test('preview is ephemeral, shows the exact text, lists kinds (names only) and offers Post/Cancel; nothing is public until Post', async () => {
  const dir = campaignWith({ 1: fixtureDoc() });
  const i = fakeSlash({ day: 1, encounter: 'enc-t-01', block: 'voice_line' });
  await enc.execute(i, ctxFor(dir));
  const all = [...i.log.replies, ...i.log.followUps];
  assert.ok(all.every(isEph), 'every preview message is ephemeral');
  assert.ok(all.every((m) => m.allowedMentions?.parse?.length === 0));
  assert.match(i.log.replies[0].content, /Preview \(only you can see this\)[\s\S]*Groups and block kinds[\s\S]*`enc-t-01`: voice_line, zone_color, set_piece, achievement_narration/);
  assert.doesNotMatch(i.log.replies[0].content, /Welcome to the test room/, 'the hint carries kind names only, no text');
  assert.match(i.log.followUps[0].content, /^\*\*\[SYSTEM\]\*\* Welcome to the test room\./);
  const row = i.log.followUps.at(-1).components[0].components;
  assert.deepEqual(row.map((b) => b.data.label), ['Post 1 message here', 'Cancel']);
});

test('Post sends the messages publicly once; the same click cannot post twice; Cancel posts nothing', async () => {
  const dir = campaignWith({ 1: fixtureDoc() });
  const ctx = ctxFor(dir);
  const i = fakeSlash({ day: 1, hours: 6 });
  await enc.execute(i, ctx);
  const token = tokenOf(i.log);
  const b = fakeButton(`encounter:111:post:${token}`);
  await enc.handleComponent(b, ctx);
  assert.equal(b.log.sent.length, 1);
  assert.match(b.log.sent[0].content, /collapses in 6 hours/);
  assert.deepEqual(b.log.sent[0].allowedMentions, { parse: [] });
  assert.match(b.log.updates[0].content, /Posted 1 message\./);
  const again = fakeButton(`encounter:111:post:${token}`);
  await enc.handleComponent(again, ctx);
  assert.equal(again.log.sent.length, 0);
  assert.match(again.log.updates[0].content, /expired/);

  const j = fakeSlash({ day: 1, hours: 6 });
  await enc.execute(j, ctx);
  const c = fakeButton(`encounter:111:cancel:${tokenOf(j.log)}`);
  await enc.handleComponent(c, ctx);
  assert.equal(c.log.sent.length, 0);
  assert.match(c.log.updates[0].content, /Nothing was posted/);
});

test('another user, or someone who lost the permission, cannot press Post', async () => {
  const dir = campaignWith({ 1: fixtureDoc() });
  const ctx = ctxFor(dir);
  const i = fakeSlash({ day: 1, hours: 6 });
  await enc.execute(i, ctx);
  const token = tokenOf(i.log);
  const other = fakeButton(`encounter:111:post:${token}`, { uid: '222' });
  await enc.handleComponent(other, ctx);
  assert.equal(other.log.sent.length, 0);
  assert.match(other.log.replies[0].content, /not your preview/);
  const demoted = fakeButton(`encounter:111:post:${token}`, { manage: false });
  await enc.handleComponent(demoted, ctx);
  assert.equal(demoted.log.sent.length, 0);
  assert.match(demoted.log.replies[0].content, /Manage Server/);
  const ok = fakeButton(`encounter:111:post:${token}`);
  await enc.handleComponent(ok, ctx);
  assert.equal(ok.log.sent.length, 1, 'the real owner can still post');
});

test('an expired preview does not post; a failing channel reports how many went out', async () => {
  const dir = campaignWith({ 1: fixtureDoc() });
  const ctx = ctxFor(dir);
  const i = fakeSlash({ day: 1, hours: 6 });
  await enc.execute(i, ctx);
  const token = tokenOf(i.log);
  enc.previews.get(token).expires = Date.now() - 1;
  const b = fakeButton(`encounter:111:post:${token}`);
  await enc.handleComponent(b, ctx);
  assert.equal(b.log.sent.length, 0);
  assert.match(b.log.updates[0].content, /expired/);
  const j = fakeSlash({ day: 1, hours: 6 });
  await enc.execute(j, ctx);
  const f = fakeButton(`encounter:111:post:${tokenOf(j.log)}`);
  f.channel.send = async () => { throw new Error('Missing Permissions'); };
  await enc.handleComponent(f, ctx);
  assert.match(f.log.updates[0].content, /Posted 0 of 1 message before an error \(Missing Permissions\)/);
});

test('the collapse notice without hours is refused in the command with a clear ephemeral message and no Post button', async () => {
  const i = fakeSlash({ day: 1, block: 'collapse_notice' });
  await enc.execute(i, ctxFor(campaignWith({ 1: fixtureDoc() })));
  assert.equal(i.log.followUps.length, 0);
  assert.match(i.log.replies[0].content, /Re-run with `hours:<number>`/);
  assert.ok(isEph(i.log.replies[0]));
});

test('too many messages at once is refused with a hint to narrow it', async () => {
  const doc = fixtureDoc();
  doc.day.tomorrow_notice.text = Array.from({ length: 40 }, (_, i) => `Sentence number ${i}. ` + 'filler '.repeat(40)).join(' ');
  const i = fakeSlash({ day: 1, hours: 1, block: 'tomorrow_notice' });
  await enc.execute(i, ctxFor(campaignWith({ 1: doc })));
  const r = buildPreview(doc, { block: 'tomorrow_notice' }).messages.length;
  if (r > 12) assert.match(i.log.replies[0].content, /the limit is 12 at once\. Narrow it/);
  else assert.match(allText(i.log), /Preview/);
});

test('an empty result explains why and still lists the kinds', async () => {
  const i = fakeSlash({ day: 1, encounter: 'enc-t-01', block: 'zone_color' });
  await enc.execute(i, ctxFor(campaignWith({ 1: fixtureDoc() })));
  assert.match(i.log.replies[0].content, /Nothing to post with those options\.\n2 optional lines skipped[\s\S]*Groups and block kinds/);
});

test('autocomplete offers group ids and kind/slot names to the GM only', async () => {
  const ctx = ctxFor(campaignWith({ 1: fixtureDoc() }));
  const a = fakeSlash({ day: 1, focusedName: 'encounter', focusedValue: 'enc' });
  await enc.autocomplete(a, ctx);
  assert.deepEqual(a.log.choices.map((c) => c.value), ['enc-t-01']);
  const b = fakeSlash({ day: 1, focusedName: 'block', focusedValue: 'win' });
  await enc.autocomplete(b, ctx);
  assert.deepEqual(b.log.choices.map((c) => c.value), ['win']);
  const none = fakeSlash({ day: 4, focusedName: 'block' });
  await enc.autocomplete(none, ctx);
  assert.deepEqual(none.log.choices, []);
});

test('through handleInteraction: a button with the encounter: prefix is routed to the handler', async () => {
  const dir = campaignWith({ 1: fixtureDoc() });
  const ctx = { ...ctxFor(dir), config: { campaign: { dir }, discord: { guildId: 'g1' } } };
  const i = fakeSlash({ day: 1, hours: 6 });
  Object.assign(i, { inGuild: () => true, guildId: 'g1', isChatInputCommand: () => true, isAutocomplete: () => false });
  await handleInteraction(i, ctx);
  const b = fakeButton(`encounter:111:post:${tokenOf(i.log)}`);
  Object.assign(b, { inGuild: () => true, guildId: 'g1', isChatInputCommand: () => false, isAutocomplete: () => false, isButton: () => true, isStringSelectMenu: () => false, isModalSubmit: () => false });
  await handleInteraction(b, ctx);
  assert.equal(b.log.sent.length, 1);
});

// ---------------------------------------------------------------- the LEAK TEST
const walkStrings = (o, path, cb) => {
  if (typeof o === 'string') return cb(path, o);
  if (Array.isArray(o)) o.forEach((v, i) => walkStrings(v, `${path}/${i}`, cb));
  else if (o && typeof o === 'object') for (const [k, v] of Object.entries(o)) walkStrings(v, `${path}/${k}`, cb);
  return undefined;
};

/** Every string in the file that is NOT a manifest-named player field. */
function gmStrings(doc) {
  const playerPaths = new Set();
  const playerTexts = [];
  for (const e of listEntries(doc)) {
    const v = resolvePointer(doc, `${e.path}/${e.field}`);
    if (typeof v === 'string') { playerPaths.add(`${e.path}/${e.field}`); playerTexts.push(v); }
    else if (Array.isArray(v)) v.forEach((p, i) => { if (p && typeof p.text === 'string') { playerPaths.add(`${e.path}/${e.field}/${i}/text`); playerTexts.push(p.text); } });
    if (e.text_field_joined) playerPaths.add(`${e.path}/${e.text_field_joined}`);          // the joined copy of the paragraphs
  }
  const out = [];
  walkStrings(doc, '', (path, s) => {
    if (playerPaths.has(path)) return;
    const t = s.trim();
    if (t.length < 8) return;
    if (playerTexts.some((p) => p.includes(t))) return;                                    // equals (or sits inside) a player field
    out.push({ path, s: t });
  });
  return { gm: out, playerTexts };
}

/** All messages the command could produce for a page, over every group, block filter and flag combination. */
function everything(doc) {
  const groups = [undefined, 'all', ...hintFor(doc).map((g) => g.id)];
  const blocks = [undefined, 'all', ...new Set(listEntries(doc).flatMap((e) => [e.kind, e.slot]))];
  const outs = [];
  for (const encounter of groups) for (const block of blocks) {
    for (const flags of [{}, { includeOptional: true, confirm: true, hours: 6 }, { hours: 3.5 }]) {
      const r = buildPreview(doc, { encounter, block, ...flags });
      outs.push(r.messages.join('\n'));
    }
  }
  return outs.join('\n=====\n');
}

test('LEAK TEST: no text from any non-manifest field ever reaches the output (synthetic page with planted GM strings)', () => {
  const doc = fixtureDoc();
  const { gm } = gmStrings(doc);
  assert.ok(gm.length > 20, 'the fixture really has GM-only text to leak');
  const out = everything(doc);
  assert.ok(out.length > 500);
  for (const { path, s } of gm) assert.ok(!out.includes(s), `LEAK from ${path}`);
  assert.doesNotMatch(out, /GMONLY/);
});

test('LEAK TEST (harness check): the checker itself fails when a whole block is printed', () => {
  const doc = fixtureDoc();
  const { gm } = gmStrings(doc);
  const leaky = JSON.stringify(doc.day.tomorrow_notice);                                    // what a lazy "print the block" would do
  assert.ok(gm.some(({ s }) => leaky.includes(s)), 'the checker would catch a whole-block print');
});

for (const n of [1, 2, 3, 4, 5]) {
  test(`LEAK TEST: real floors/f01/day-0${n}.json (every encounter, route, block, flag combination)`, { skip: !haveReal && 'real floors/f01 pages not present' }, () => {
    const doc = loadPage(REAL, 1, n);
    const { gm, playerTexts } = gmStrings(doc);
    assert.ok(gm.length > 100, 'plenty of GM-only text to check against');
    assert.ok(playerTexts.length > 10);
    const out = everything(doc);
    assert.ok(out.length > 1000);
    const leaks = gm.filter(({ s }) => out.includes(s)).map(({ path }) => path);
    assert.deepEqual(leaks, [], `GM-only text reached the output from: ${leaks.slice(0, 5).join(', ')}`);
    // the never-show list in the manifest, by name, must not be present as labels either
    for (const bad of ['[GM-FACING]', '[GM-ONLY]', 'hours_note', 'gm_note', 'loot_hooks', 'carry_on', 'quick_run', 'stall_fallback']) assert.ok(!out.includes(bad), bad);
    assert.doesNotMatch(out, /\bchamps?\b|\bcash\b/i);
    assert.doesNotMatch(out, /\{[A-Za-z_]+\}/, 'no raw placeholder reaches players');
    for (const m of out.split('\n=====\n').flatMap((x) => x.split('\n\n'))) assert.ok(m.length <= 2000);
  });
}

test('real pages: every message is within the limit and hints list only kind names', { skip: !haveReal && 'real pages not present' }, () => {
  for (const n of [1, 2, 3, 4, 5]) {
    const doc = loadPage(REAL, 1, n);
    const t = hintText(doc);
    assert.ok(t.length < 1900, `hint for day ${n} fits a Discord message`);
    for (const g of hintFor(doc)) assert.ok(g.kinds.every((k) => /^[a-z_]+$/.test(k)));
    const r = buildPreview(doc, { encounter: 'all', hours: 6, includeOptional: true, confirm: true });
    assert.ok(r.messages.every((m) => m.length <= 2000));
  }
});
