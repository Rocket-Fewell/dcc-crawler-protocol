import { MessageFlags, SlashCommandBuilder } from 'discord.js';
import { reviewAction, startComfort, startCreate } from '../create/flow.js';

export const data = new SlashCommandBuilder()
  .setName('create')
  .setDescription('Create your Crawler in a private text flow (nothing is spoken or posted)')
  .addStringOption((o) =>
    o
      .setName('action')
      .setDescription('Default: start or resume your intake')
      .addChoices({ name: 'comfort (edit lines and veils)', value: 'comfort' }, { name: 'review (reviewer)', value: 'review' }, { name: 'approve (reviewer)', value: 'approve' }, { name: 'return (reviewer)', value: 'return' })
  )
  .addUserOption((o) => o.setName('player').setDescription('Reviewer actions: which player'))
  .addStringOption((o) => o.setName('screen').setDescription('return: screen to send them back to, e.g. S7'))
  .addStringOption((o) => o.setName('note').setDescription('return: a short note for the player').setMaxLength(200));

export async function execute(interaction, ctx) {
  const action = interaction.options.getString('action');
  if (!action) return startCreate(interaction, ctx);
  if (action === 'comfort') return startComfort(interaction, ctx);
  return reviewAction(interaction, ctx, action);
}
void MessageFlags;
