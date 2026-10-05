import { ActionRowBuilder, MessageFlags, SlashCommandBuilder, StringSelectMenuBuilder } from 'discord.js';
import { channelLink, crawlersText, listOwned, requestSwap } from '../create/manage.js';
import { readSessionState } from '../create/store.js';

export const data = new SlashCommandBuilder().setName('crawlers').setDescription('List your Crawlers (active or benched) and ask the GM for a swap');

const cut = (s, n) => (String(s).length > n ? `${String(s).slice(0, n - 1)}…` : String(s));

export function view(ctx, user) {
  const rows = listOwned(ctx.config, user);
  const floor = readSessionState(ctx.config)?.campaign?.current_floor;
  const benched = rows.filter((c) => !c.active && c.kind === 'player');
  const components = benched.length
    ? [new ActionRowBuilder().addComponents(new StringSelectMenuBuilder().setCustomId(`crawlers:${user.id}:swap`).setPlaceholder('Request a swap to…').addOptions(benched.slice(0, 25).map((c) => ({ label: cut(c.name, 100), value: cut(c.name, 100), description: cut(`${c.species ?? ''} ${c.class ?? ''} L${c.level} ${channelLink(c).startsWith('<') ? '' : ''}`.trim(), 100) }))))]
    : [];
  return { content: crawlersText(rows, floor), components, allowedMentions: { parse: [] } };
}

export async function execute(interaction, ctx) {
  return interaction.reply({ ...view(ctx, interaction.user), flags: MessageFlags.Ephemeral });
}

/** Select-menu: customId "crawlers:<userId>:swap". Sends a REQUEST only; never changes a Crawler. */
export async function handleComponent(interaction, ctx) {
  const [, uid, action] = interaction.customId.split(':');
  if (uid !== interaction.user.id) return interaction.reply({ content: 'This is not your list.', flags: MessageFlags.Ephemeral });
  if (action !== 'swap') return;
  const res = await requestSwap(ctx, interaction.user, interaction.values[0]);
  return interaction.reply({ content: res.message, flags: MessageFlags.Ephemeral, allowedMentions: { parse: [] } });
}
