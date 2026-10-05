import { MessageFlags, SlashCommandBuilder } from 'discord.js';

export const data = new SlashCommandBuilder().setName('shush').setDescription('Instantly stop the GM voice and clear everything queued to be spoken');

export async function execute(interaction, ctx) {
  const dropped = ctx.flushVoice('shush');
  ctx.logger.info(`/shush used by ${interaction.user.id}`);
  return interaction.reply({
    content: `Shushed: playback stopped and the speech queue cleared (${dropped} chunk${dropped === 1 ? '' : 's'}). ` +
      'This does not stop the GM from running; `/gm pause` stops new GM runs.',
    flags: MessageFlags.Ephemeral,
  });
}
