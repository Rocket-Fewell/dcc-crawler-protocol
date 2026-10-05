import { MessageFlags, SlashCommandBuilder } from 'discord.js';

export const data = new SlashCommandBuilder()
  .setName('skip')
  .setDescription('Skip the GM message currently being spoken')
  .addBooleanOption((o) => o.setName('all').setDescription('Clear the whole speech queue').setRequired(false));

export async function execute(interaction, ctx) {
  const all = interaction.options.getBoolean('all') ?? false;
  const dropped = ctx.queue.skip({ all });
  if (dropped) ctx.dedupe?.clear(); // what was skipped was not heard; a re-post may be spoken
  return interaction.reply({
    content: dropped ? `Skipped${all ? ' everything in the queue' : ''} (${dropped} chunk${dropped === 1 ? '' : 's'}).` : 'Nothing is being spoken.',
    flags: MessageFlags.Ephemeral,
  });
}
