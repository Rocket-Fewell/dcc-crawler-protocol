import { MessageFlags, PermissionFlagsBits, SlashCommandBuilder } from 'discord.js';
import { fmt } from '../sessioncap.js';

export const data = new SlashCommandBuilder()
  .setName('voicecap')
  .setDescription('Show spoken-TTS minutes used this voice session vs the cap (Manage Server can reset or change it)')
  .addStringOption((o) =>
    o
      .setName('action')
      .setDescription('Leave empty to just show usage')
      .addChoices({ name: 'reset - zero the used minutes', value: 'reset' }, { name: 'set - change the cap (needs minutes)', value: 'set' })
      .setRequired(false)
  )
  .addNumberOption((o) => o.setName('minutes').setDescription('With action "set": new cap in minutes (0 = no cap)').setMinValue(0).setMaxValue(10000).setRequired(false));

export function describe(st) {
  if (!st.enabled) return `Voice session: ${fmt(st.used)} min used, no cap (FISH_SESSION_CAP_MINUTES=0).`;
  return `Voice session: ${fmt(st.used)} / ${fmt(st.cap)} min used (${Math.round(st.percent)}%), ${fmt(st.remaining)} min left.${st.reached ? ' **Cap reached: GM speech is paused.**' : ''}`;
}

/** Manage Server (or Administrator, or the server owner) may change things; anyone may view. */
export function canManage(interaction) {
  return Boolean(interaction.memberPermissions?.has(PermissionFlagsBits.ManageGuild) || interaction.guild?.ownerId === interaction.user?.id);
}

export async function execute(interaction, ctx) {
  const cap = ctx.sessionCap;
  const reply = (content) => interaction.reply({ content, flags: MessageFlags.Ephemeral });
  const action = interaction.options.getString('action');
  const minutes = interaction.options.getNumber('minutes');
  if (!action) return reply(describe(cap.status()));
  if (!canManage(interaction)) return reply('You need the **Manage Server** permission to change the voice cap.');
  if (action === 'reset') {
    cap.reset();
    ctx.logger.info(`Voice session counter reset by ${interaction.user.id}`);
    return reply(`Reset. ${describe(cap.status())}`);
  }
  if (minutes === null) return reply('Use `/voicecap action:set minutes:<n>` (0 = no cap).');
  cap.setCap(minutes);
  ctx.logger.info(`Voice session cap set to ${minutes} min by ${interaction.user.id}`);
  return reply(`Cap set to ${minutes > 0 ? fmt(minutes) + ' min' : 'none'} for this run (until the bot restarts). ${describe(cap.status())}`);
}
