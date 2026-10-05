import { REST, Routes } from 'discord.js';
import { commandData } from './commands/index.js';
import { ConfigError, loadConfig } from './config.js';
import { resolveActiveId, sessionEnv } from './session.js';

try {
  const { discord } = loadConfig(sessionEnv(process.env, resolveActiveId(process.env)), { mode: 'register' }) /* DCC_SESSION=beta npm run register -> that session's guild */;
  const rest = new REST({ version: '10' }).setToken(discord.token);
  const route = Routes.applicationGuildCommands(discord.clientId, discord.guildId);
  const result = await rest.put(route, { body: commandData });
  console.log(`Registered ${result.length} guild commands: ${result.map((c) => '/' + c.name).join(', ')}`);
} catch (err) {
  if (err instanceof ConfigError) console.error(err.message);
  else console.error('Command registration failed:', err);
  process.exit(1);
}
