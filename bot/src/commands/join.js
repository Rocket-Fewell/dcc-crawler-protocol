import { markSession } from '../create/manage.js';
import { ChannelType, MessageFlags, PermissionFlagsBits, SlashCommandBuilder } from 'discord.js';

export const data = new SlashCommandBuilder()
  .setName('join')
  .setDescription('Join a voice channel (default: yours, else the configured one) and start the bridge')
  .addChannelOption((o) =>
    o
      .setName('channel')
      .setDescription('Voice channel to join')
      .addChannelTypes(ChannelType.GuildVoice, ChannelType.GuildStageVoice)
      .setRequired(false)
  );

export async function execute(interaction, ctx) {
  await interaction.deferReply({ flags: MessageFlags.Ephemeral });
  const { config, session } = ctx;

  let channel = interaction.options.getChannel('channel');
  if (!channel) channel = interaction.member?.voice?.channel ?? null;
  if (!channel && config.discord.voiceChannelId) {
    channel = await interaction.guild.channels.fetch(config.discord.voiceChannelId).catch(() => null);
  }
  if (!channel?.isVoiceBased()) {
    return interaction.editReply('Join a voice channel first, pass a `channel`, or set VOICE_CHANNEL_ID.');
  }
  // Re-resolve through the guild so permissions/guild adapter are available.
  channel = await interaction.guild.channels.fetch(channel.id);

  const me = interaction.guild.members.me ?? (await interaction.guild.members.fetchMe());
  const perms = channel.permissionsFor(me);
  const missing = [
    ['View Channel', PermissionFlagsBits.ViewChannel],
    ['Connect', PermissionFlagsBits.Connect],
    ['Speak', PermissionFlagsBits.Speak],
  ].filter(([, bit]) => !perms?.has(bit));
  if (missing.length) {
    return interaction.editReply(`I'm missing permissions in ${channel}: ${missing.map(([n]) => n).join(', ')}.`);
  }

  try {
    await session.join(channel);
  } catch (err) {
    ctx.logger.error(`/join failed: ${err.message}`);
    return interaction.editReply(`Couldn't join ${channel}: ${err.message}`);
  }
  await markSession(ctx, 'open');   // best effort: Crawler swaps are locked while a session is open (tools/state.py session-status)
  return interaction.editReply(`Joined ${channel}. Listening for players and speaking GM output.`);
}
