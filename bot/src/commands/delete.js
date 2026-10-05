import { ActionRowBuilder, ButtonBuilder, ButtonStyle, MessageFlags, ModalBuilder, SlashCommandBuilder, TextInputBuilder, TextInputStyle } from 'discord.js';
import { deleteOwned, deleteWarning, listOwned } from '../create/manage.js';

export const data = new SlashCommandBuilder()
  .setName('delete')
  .setDescription('Delete one of your own Crawlers (permanent, nothing is refunded)')
  .addStringOption((o) => o.setName('name').setDescription('Which of your Crawlers').setRequired(true).setAutocomplete(true));

const enc = (s) => Buffer.from(s, 'utf8').toString('base64url');
const dec = (s) => Buffer.from(s, 'base64url').toString('utf8');
const user = (i) => ({ id: i.user.id, username: i.user.username, globalName: i.user.globalName });

/** Autocomplete shows ONLY the caller's own Crawlers. */
export async function autocomplete(interaction, ctx) {
  const q = String(interaction.options.getFocused() ?? '').toLowerCase();
  const rows = listOwned(ctx.config, user(interaction)).filter((c) => c.name.toLowerCase().includes(q));
  return interaction.respond(rows.slice(0, 25).map((c) => ({ name: `${c.name} (${c.active ? 'active' : 'benched'})`.slice(0, 100), value: c.name.slice(0, 100) })));
}

export async function execute(interaction, ctx) {
  const name = interaction.options.getString('name');
  const c = listOwned(ctx.config, user(interaction)).find((x) => x.name.toLowerCase() === String(name).toLowerCase());
  if (!c) return interaction.reply({ content: 'That is not one of your Crawlers, so it cannot be deleted.', flags: MessageFlags.Ephemeral });
  if (enc(c.name).length > 60) return interaction.reply({ content: 'That name is too long for the confirm button; ask the GM to delete it.', flags: MessageFlags.Ephemeral });
  const row = new ActionRowBuilder().addComponents(
    new ButtonBuilder().setCustomId(`delete:${interaction.user.id}:cancel:${enc(c.name)}`).setLabel('Cancel').setStyle(ButtonStyle.Secondary),
    new ButtonBuilder().setCustomId(`delete:${interaction.user.id}:ask:${enc(c.name)}`).setLabel('I want to delete it…').setStyle(ButtonStyle.Danger),
  );
  return interaction.reply({ content: deleteWarning(c), components: [row], flags: MessageFlags.Ephemeral, allowedMentions: { parse: [] } });
}

/** Buttons and the modal: customId "delete:<userId>:<cancel|ask|confirm>:<base64url name>". The typed name is the real confirm. */
export async function handleComponent(interaction, ctx) {
  const [, uid, action, packed] = interaction.customId.split(':');
  if (uid !== interaction.user.id) return interaction.reply({ content: 'This is not your confirmation.', flags: MessageFlags.Ephemeral });
  const name = dec(packed ?? '');
  if (action === 'cancel') return interaction.update({ content: `Cancelled. ${name} was not deleted.`, components: [] });
  if (action === 'ask') {
    const m = new ModalBuilder().setCustomId(`delete:${uid}:confirm:${packed}`).setTitle('Type the exact name to delete');
    m.addComponents(new ActionRowBuilder().addComponents(new TextInputBuilder().setCustomId('typed').setLabel(`Type: ${name}`.slice(0, 45)).setStyle(TextInputStyle.Short).setRequired(true).setMaxLength(100)));
    return interaction.showModal(m);
  }
  if (action === 'confirm') {
    await interaction.deferReply({ flags: MessageFlags.Ephemeral });
    const typed = interaction.fields.getTextInputValue('typed');
    const res = await deleteOwned(ctx, user(interaction), name, typed);
    return interaction.editReply({ content: res.message, allowedMentions: { parse: [] } });
  }
}
