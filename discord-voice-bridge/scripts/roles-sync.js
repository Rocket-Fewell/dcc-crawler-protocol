/**
 * Manual admin trigger for the new-player role backfill (same code the bridge runs on every start; additive + idempotent).
 *   npm run roles:sync              # apply
 *   npm run roles:sync -- --dry-run # show what would change, change nothing
 * Uses the bridge's own config (.env + the active campaign session); logs in briefly with DISCORD_TOKEN, then exits.
 */
import { Client, Events, GatewayIntentBits } from 'discord.js';
import { ConfigError, loadConfig } from '../src/config.js';
import { resolveActiveId, sessionEnv } from '../src/session.js';
import { PlayerRoles, detectMembersIntent, formatReport, rolesFile } from '../src/roles.js';

const dryRun = process.argv.includes('--dry-run');
let config;
try {
  config = loadConfig(sessionEnv(process.env, resolveActiveId(process.env)), { mode: 'register' });
} catch (err) {
  console.error(err instanceof ConfigError ? err.message : err);
  process.exit(1);
}
const mi = await detectMembersIntent(config.discord.token);
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildVoiceStates, ...(mi.enabled ? [GatewayIntentBits.GuildMembers] : [])] });
const timer = setTimeout(() => { console.error('roles:sync timed out after 120s'); process.exit(1); }, 120_000);
client.once(Events.ClientReady, async (c) => {
  let code = 0;
  try {
    console.log(`Logged in as ${c.user.tag}; campaign session ${config.campaign.sessionId}; store ${rolesFile(config)}; GuildMembers intent ${mi.enabled ? 'ON' : `OFF (${mi.source})`}`);
    const guild = await c.guilds.fetch(config.discord.guildId);
    await guild.roles.fetch();
    await guild.channels.fetch();
    const report = await new PlayerRoles({ config, membersIntent: mi.enabled, dryRun, logger: console }).sync(guild);
    console.log(formatReport(report));
    if (report.problems.length) code = 2;
  } catch (err) {
    console.error(`roles:sync failed: ${err.message}`);
    code = 1;
  }
  clearTimeout(timer);
  await client.destroy();
  process.exit(code);
});
await client.login(config.discord.token);
