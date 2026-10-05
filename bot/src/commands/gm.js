import { MessageFlags, SlashCommandBuilder } from 'discord.js';
import { readSpotlight } from '../spotlight.js';
import { formatClock } from '../wakebudget.js';

export const data = new SlashCommandBuilder()
  .setName('gm')
  .setDescription('Pause or resume waking the AI GM (transcripts keep being posted either way)')
  .addStringOption((o) =>
    o
      .setName('action')
      .setDescription('pause = no new GM runs, resume = wake the GM again, status = show')
      .setRequired(true)
      .addChoices({ name: 'pause', value: 'pause' }, { name: 'resume', value: 'resume' }, { name: 'status', value: 'status' })
  );

export function describe(ctx) {
  const st = ctx.gmState;
  const cfg = ctx.config;
  const lines = [];
  lines.push(st.paused ? `GM wake: **PAUSED**${st.since ? ` since ${st.since}` : ''}. Players are still transcribed to the transcript channel, but no new GM runs are started.` : 'GM wake: **ON**.');
  lines.push(cfg.wake.enabled ? 'Webhook: configured.' : 'Webhook: NOT configured (GM_WEBHOOK_URL is unset), so nothing is sent either way.');
  const ws = ctx.wake?.status?.();
  if (ws) {
    const b = ws.budget;
    let line = b.enabled ? `Wakes used in the last hour: **${b.used} / ${b.max}**` : `Wakes budget: unlimited (WAKE_MAX_PER_HOUR=0)`;
    if (b.exhausted) line += ` - budget reached, next wake at ${formatClock(b.resumeAt)}`;
    if (ws.rateLimitedUntil) line += ` - rate limited by the server, retrying at ${formatClock(ws.rateLimitedUntil)}`;
    if (ws.held) line += ` (${ws.held} line${ws.held === 1 ? '' : 's'} held for the next wake)`;
    lines.push(line + '.');
  }
  if (cfg.spotlight?.enabled) {
    const s = readSpotlight({ file: cfg.spotlight.file, maxAgeMinutes: cfg.spotlight.maxAgeMinutes });
    lines.push(s.active ? `Spotlight: ${s.player} (others only wake the GM by saying "AI").` : 'Spotlight: none (open floor).');
  }
  return lines.join('\n');
}

export async function execute(interaction, ctx) {
  const action = interaction.options.getString('action', true);
  const reply = (content) => interaction.reply({ content, flags: MessageFlags.Ephemeral });
  if (action === 'pause' || action === 'resume') {
    const was = ctx.gmState.paused;
    ctx.gmState.set(action === 'pause', interaction.user.id);
    ctx.logger.info(`GM wake ${action === 'pause' ? 'PAUSED' : 'resumed'} by ${interaction.user.id}${was === ctx.gmState.paused ? ' (no change)' : ''}`);
    return reply(`${action === 'pause' ? 'Paused.' : 'Resumed.'}\n${describe(ctx)}`);
  }
  return reply(describe(ctx));
}
