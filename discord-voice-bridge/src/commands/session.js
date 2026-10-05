import { MessageFlags, SlashCommandBuilder } from 'discord.js';
import { canManage } from './voicecap.js';
import { listSessions, readProfile, validSessionId } from '../session.js';
import { fmt } from '../sessioncap.js';

export const data = new SlashCommandBuilder()
  .setName('session')
  .setDescription('Which campaign session (alpha, beta, ...) the bridge serves right now')
  .addSubcommand((s) => s.setName('status').setDescription('Show the active session, its channels and its Fish minutes'))
  .addSubcommand((s) => s.setName('list').setDescription('List the known campaign sessions'))
  .addSubcommand((s) =>
    s
      .setName('use')
      .setDescription('Switch the bridge to another campaign session (admin; leave voice first)')
      .addStringOption((o) => o.setName('id').setDescription('Session id, e.g. alpha or beta').setRequired(true))
  );

const ref = (id) => (id ? `<#${id}>` : '-');

export function describe(ctx) {
  const c = ctx.config;
  const m = ctx.monthly?.status?.();
  const lines = [
    `Active session: **${c.campaign.sessionId}**${readProfile(c.campaign.sessionId).label ? ` (${readProfile(c.campaign.sessionId).label})` : ''}`,
    `Ears ${ref(c.discord.transcriptChannelId)} | Mouth ${ref(c.discord.gmOutputChannelId)} | Voice ${ref(c.discord.voiceChannelId)}`,
    `GM wake: ${c.wake.enabled ? 'webhook configured' : 'NO webhook for this session (nothing will wake a GM)'}`,
  ];
  if (m && c.tts.provider === 'fish') {
    lines.push(
      `Fish minutes this month: this session ${fmt(m.usedSession)}${m.share > 0 ? ` / ${m.share}` : ''}, all sessions ${fmt(m.usedTotal)}${m.totalCap > 0 ? ` / ${m.totalCap}` : ''}${m.reached ? ` - **${m.reason === 'share' ? 'this session\'s share is used up' : 'shared total reached'}**` : ''}`
    );
  }
  return lines.join('\n');
}

export async function execute(interaction, ctx) {
  const reply = (content) => interaction.reply({ content, flags: MessageFlags.Ephemeral });
  const sub = interaction.options.getSubcommand();
  if (sub === 'status') return reply(describe(ctx));
  if (sub === 'list') {
    const active = ctx.config.campaign.sessionId;
    const rows = listSessions().map((id) => `${id === active ? '▶' : '•'} **${id}**${readProfile(id).label ? ` - ${readProfile(id).label}` : ''}${id === 'alpha' ? ' (live table files under sessions/)' : ''}`);
    rows.push('_Create a new empty campaign:_ `python3 tools/new-session.py <id>` (does not switch). Switch with `/session use <id>` after `/leave`.');
    return reply(rows.join('\n'));
  }
  if (!canManage(interaction)) return reply('You need the **Manage Server** permission to switch campaign sessions.');
  const id = interaction.options.getString('id', true).trim().toLowerCase();
  if (id !== 'alpha' && !validSessionId(id)) return reply('Session ids use a-z, 0-9, _ and - (e.g. `beta`).');
  if (!ctx.sessionExists(id)) return reply(`No session "${id}" yet. Create it first: \`python3 tools/new-session.py ${id}\`.`);
  if (id === ctx.config.campaign.sessionId) return reply(`Already on **${id}**.\n${describe(ctx)}`);
  if (ctx.session.isConnected || ctx.session.connection) return reply('The bot is in a voice channel. Use `/leave` first, then switch (alpha and beta never share a voice session).');
  const out = ctx.applySession(id, interaction.user.id);
  ctx.logger.info(`Campaign session switched to "${id}" by ${interaction.user.id}`);
  return reply(`Switched to **${id}**.\n${describe(ctx)}${out.guildId && out.guildId !== interaction.guildId ? '\nThis session lives in another server: continue there (register commands for it with `DCC_SESSION=' + id + ' npm run register`).' : ''}`);
}
