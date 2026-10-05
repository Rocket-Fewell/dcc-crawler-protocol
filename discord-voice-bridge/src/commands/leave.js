import { markSession } from '../create/manage.js';
import { MessageFlags, SlashCommandBuilder } from 'discord.js';

export const data = new SlashCommandBuilder().setName('leave').setDescription('Leave the voice channel and stop the bridge');

export async function execute(interaction, ctx) {
  const left = ctx.session.leave();
  ctx.queue.clear();
  if (left) await markSession(ctx, 'close');
  return interaction.reply({
    content: left ? 'Left the voice channel.' : "I'm not in a voice channel.",
    flags: MessageFlags.Ephemeral,
  });
}
