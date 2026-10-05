import { MessageFlags, SlashCommandBuilder } from 'discord.js';
import { prepareSpeechDetailed } from '../text.js';

export const data = new SlashCommandBuilder()
  .setName('say')
  .setDescription('Speak text in the voice channel')
  .addStringOption((o) => o.setName('text').setDescription('What to say').setRequired(true).setMaxLength(2000))
  .addStringOption((o) =>
    o
      .setName('voice')
      .setDescription('Which voice to use (default: gm). [SYSTEM]/[GM]/[ROLL] tags inside the text still apply.')
      .addChoices({ name: 'GM (narrator)', value: 'gm' }, { name: 'System (dry/corporate)', value: 'system' })
      .setRequired(false)
  );

export async function execute(interaction, ctx) {
  const { config, session, queue } = ctx;
  if (!config.tts.enabled) {
    return interaction.reply({ content: 'TTS is disabled (TTS_ENABLED=false).', flags: MessageFlags.Ephemeral });
  }
  if (!session.isConnected) {
    return interaction.reply({ content: "I'm not in a voice channel. Use /join first.", flags: MessageFlags.Ephemeral });
  }
  if (ctx.sessionCap?.isReached()) {
    ctx.sessionCap.block();
    return interaction.reply({ content: 'The session voice cap is reached, so nothing was spoken. Use `/voicecap` to see or reset it.', flags: MessageFlags.Ephemeral });
  }
  const voice = interaction.options.getString('voice') ?? 'gm';
  const { chunks } = prepareSpeechDetailed(interaction.options.getString('text', true), {
    defaultVoice: voice,
    chunkMaxChars: config.tts.chunkMaxChars,
    maxMessageChars: config.tts.maxMessageChars,
  });
  if (!chunks.length) {
    return interaction.reply({ content: 'Nothing speakable in that text (note: [ROLL] lines are never spoken).', flags: MessageFlags.Ephemeral });
  }
  queue.enqueue(chunks, { label: `say:${interaction.user.id}` });
  return interaction.reply({ content: `Speaking (${chunks.length} chunk${chunks.length === 1 ? '' : 's'}, ${voice} voice default).`, flags: MessageFlags.Ephemeral });
}
