import { randomBytes } from 'node:crypto';
import { ActionRowBuilder, ButtonBuilder, ButtonStyle, MessageFlags, PermissionFlagsBits, SlashCommandBuilder } from 'discord.js';
import { EncounterError, MAX_MESSAGES, buildPreview, hintFor, hintText, loadPage } from '../encounter/extract.js';
import { canManage } from './voicecap.js';

export const data = new SlashCommandBuilder()
  .setName('encounter')
  .setDescription('GM only: preview, then post, the player-facing text of a Floor day page')
  .setDefaultMemberPermissions(PermissionFlagsBits.ManageGuild)
  .setDMPermission(false)
  .addIntegerOption((o) => o.setName('day').setDescription('Day of the floor (1-5)').setMinValue(1).setMaxValue(5).setRequired(true))
  .addStringOption((o) => o.setName('encounter').setDescription('Encounter or route id, or "all". Leave empty for the day-level notices.').setAutocomplete(true))
  .addStringOption((o) => o.setName('block').setDescription('Block kind or slot, e.g. system_intro, win, zone_color, collapse_notice').setAutocomplete(true))
  .addBooleanOption((o) => o.setName('include_optional').setDescription('Also show optional lines (zone colour, optional set-piece paragraphs)'))
  .addNumberOption((o) => o.setName('hours').setDescription('In-game hours left; fills {hours} in the collapse notice (required for it)').setMinValue(0).setMaxValue(24))
  .addBooleanOption((o) => o.setName('confirm').setDescription('Confirm the "shown only when" condition is true (e.g. the achievement was awarded)'))
  .addIntegerOption((o) => o.setName('floor').setDescription('Floor number (default 1; only Floor 1 pages exist so far)').setMinValue(1).setMaxValue(18));

export const PREVIEW_TTL_MS = 30 * 60 * 1000;
/** token -> { userId, messages, floor, day, expires }. In memory only: a restart (or 30 minutes) expires a preview; run /encounter again. */
export const previews = new Map();

const prune = (now = Date.now()) => { for (const [k, v] of previews) if (v.expires <= now) previews.delete(k); };
const eph = (content, extra = {}) => ({ content: String(content).slice(0, 2000), flags: MessageFlags.Ephemeral, allowedMentions: { parse: [] }, ...extra });
const NOT_ALLOWED = 'You need the **Manage Server** permission to use `/encounter` (it is a GM command).';

function options(interaction) {
  const o = interaction.options;
  return {
    day: o.getInteger('day', true),
    floor: o.getInteger('floor') ?? 1,
    encounter: o.getString('encounter') ?? undefined,
    block: o.getString('block') ?? undefined,
    includeOptional: o.getBoolean('include_optional') ?? false,
    hours: o.getNumber('hours') ?? undefined,
    confirm: o.getBoolean('confirm') ?? false,
  };
}

/** Autocomplete: names of groups and block kinds/slots only (no text). GM-only like the command; empty for everyone else. */
export async function autocomplete(interaction, ctx) {
  if (!canManage(interaction)) return interaction.respond([]);
  const focused = interaction.options.getFocused(true);
  const day = interaction.options.getInteger('day');
  const floor = interaction.options.getInteger('floor') ?? 1;
  if (!day) return interaction.respond([]);
  let names = [];
  try {
    const hint = hintFor(loadPage(ctx.config.campaign.dir, floor, day));
    names = focused.name === 'encounter' ? ['all', ...hint.map((g) => g.id)] : [...new Set(hint.flatMap((g) => [...g.kinds, ...g.slots]))];
  } catch { names = []; }
  const q = String(focused.value ?? '').toLowerCase();
  return interaction.respond(names.filter((n) => n.toLowerCase().includes(q)).slice(0, 25).map((n) => ({ name: n.slice(0, 100), value: n.slice(0, 100) })));
}

export async function execute(interaction, ctx) {
  if (!canManage(interaction)) return interaction.reply(eph(NOT_ALLOWED));
  const opt = options(interaction);
  let doc;
  try {
    doc = loadPage(ctx.config.campaign.dir, opt.floor, opt.day);          // fresh from disk every call
  } catch (err) {
    if (err instanceof EncounterError) return interaction.reply(eph(err.message));
    throw err;
  }
  const res = buildPreview(doc, opt);
  const hint = hintText(doc);
  if (res.error) return interaction.reply(eph(`${res.error}\n\n${hint}`));
  if (!res.messages.length) return interaction.reply(eph(`Nothing to post with those options.${res.notes.length ? `\n${res.notes.join('\n')}` : ''}\n\n${hint}`));
  if (res.messages.length > MAX_MESSAGES) {
    return interaction.reply(eph(`That would be ${res.messages.length} messages (the limit is ${MAX_MESSAGES} at once). Narrow it with \`encounter:\` or \`block:\`.\n\n${hint}`));
  }
  prune();
  const token = randomBytes(6).toString('hex');
  previews.set(token, { userId: interaction.user.id, messages: res.messages, floor: opt.floor, day: opt.day, expires: Date.now() + PREVIEW_TTL_MS });
  const n = res.messages.length;
  await interaction.reply(eph(`**Preview (only you can see this)** - Floor ${opt.floor} Day ${opt.day}: ${n} message${n === 1 ? '' : 's'} follow${n === 1 ? 's' : ''}, exactly as players would see them.${res.notes.length ? `\n${res.notes.join('\n')}` : ''}\n\n${hint}`.slice(0, 1990)));
  for (const m of res.messages) await interaction.followUp(eph(m));
  const row = new ActionRowBuilder().addComponents(
    new ButtonBuilder().setCustomId(`encounter:${interaction.user.id}:post:${token}`).setLabel(`Post ${n} message${n === 1 ? '' : 's'} here`).setStyle(ButtonStyle.Success),
    new ButtonBuilder().setCustomId(`encounter:${interaction.user.id}:cancel:${token}`).setLabel('Cancel').setStyle(ButtonStyle.Secondary),
  );
  return interaction.followUp(eph('Post the text above publicly in this channel?', { components: [row] }));
}

/** Buttons: customId "encounter:<userId>:<post|cancel>:<token>". */
export async function handleComponent(interaction, ctx) {
  const [, uid, action, token] = interaction.customId.split(':');
  if (uid !== interaction.user.id) return interaction.reply(eph('This is not your preview.'));
  if (!canManage(interaction)) return interaction.reply(eph(NOT_ALLOWED));
  prune();
  const p = previews.get(token);
  if (action === 'cancel') {
    previews.delete(token);
    return interaction.update({ content: 'Cancelled. Nothing was posted.', components: [] });
  }
  if (action !== 'post') return undefined;
  if (!p || p.userId !== interaction.user.id) return interaction.update({ content: 'This preview has expired (30 minutes, or the bot restarted). Run `/encounter` again.', components: [] });
  previews.delete(token);                                                  // one click, one post
  let sent = 0;
  try {
    for (const m of p.messages) {
      await interaction.channel.send({ content: m, allowedMentions: { parse: [] } });
      sent += 1;
    }
  } catch (err) {
    ctx.logger.warn(`/encounter post failed after ${sent}/${p.messages.length}: ${err.message}`);
    return interaction.update({ content: `Posted ${sent} of ${p.messages.length} message${p.messages.length === 1 ? '' : 's'} before an error (${err.message}). Run \`/encounter\` again for the rest.`, components: [] });
  }
  ctx.logger.info(`/encounter Floor ${p.floor} Day ${p.day}: ${sent} message(s) posted by ${interaction.user.id}`);
  return interaction.update({ content: `Posted ${sent} message${sent === 1 ? '' : 's'}.`, components: [] });
}
