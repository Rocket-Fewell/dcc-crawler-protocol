import { MessageFlags } from 'discord.js';
import * as create from './create.js';
import * as crawlers from './crawlers.js';
import * as del from './delete.js';
import * as encounter from './encounter.js';
import * as gm from './gm.js';
import { handleComponent } from '../create/flow.js';
import * as join from './join.js';
import * as leave from './leave.js';
import * as say from './say.js';
import * as sessionCmd from './session.js';
import * as shush from './shush.js';
import * as skip from './skip.js';
import * as voicecap from './voicecap.js';

const all = [join, leave, skip, say, voicecap, shush, gm, sessionCmd, create, crawlers, del, encounter];
const componentHandlers = { crawlers: crawlers.handleComponent, delete: del.handleComponent, encounter: encounter.handleComponent };

export const commands = new Map(all.map((c) => [c.data.name, c]));
export const commandData = all.map((c) => c.data.toJSON());

/** Route a chat-input interaction to its command, with guild checks and error handling. */
export async function handleInteraction(interaction, ctx) {
  if (interaction.isAutocomplete?.()) {
    const command = commands.get(interaction.commandName);
    if (!command?.autocomplete || !interaction.inGuild() || interaction.guildId !== ctx.config.discord.guildId) return interaction.respond([]).catch(() => {});
    try { await command.autocomplete(interaction, ctx); } catch (err) { ctx.logger.warn(`autocomplete /${interaction.commandName} failed: ${err.message}`); await interaction.respond([]).catch(() => {}); }
    return;
  }
  if (!interaction.isChatInputCommand()) {
    // /crawlers swap menu, /delete confirm buttons + modal and /encounter Post/Cancel buttons (customId "crawlers:<userId>:..." / "delete:<userId>:..." / "encounter:<userId>:...")
    const prefix = interaction.customId?.split(':')[0];
    if (componentHandlers[prefix] && (interaction.isButton() || interaction.isStringSelectMenu() || interaction.isModalSubmit())) {
      if (!interaction.inGuild() || interaction.guildId !== ctx.config.discord.guildId) return;
      try {
        await componentHandlers[prefix](interaction, ctx);
      } catch (err) {
        ctx.logger.error(`/${prefix} component failed:`, err);
        const msg = { content: `Something went wrong: ${err.message}`, flags: MessageFlags.Ephemeral };
        if (interaction.deferred || interaction.replied) await interaction.followUp(msg).catch(() => {});
        else await interaction.reply(msg).catch(() => {});
      }
      return;
    }
    // /create buttons, select menus and modals (customId "create:<userId>:<screen>:<key>")
    if ((interaction.isButton() || interaction.isStringSelectMenu() || interaction.isModalSubmit()) && interaction.customId?.startsWith('create:')) {
      if (!interaction.inGuild() || interaction.guildId !== ctx.config.discord.guildId) return;
      try {
        await handleComponent(interaction, ctx);
      } catch (err) {
        ctx.logger.error('/create component failed:', err);
        const msg = { content: `Something went wrong: ${err.message}`, flags: MessageFlags.Ephemeral };
        if (interaction.deferred || interaction.replied) await interaction.followUp(msg).catch(() => {});
        else await interaction.reply(msg).catch(() => {});
      }
    }
    return;
  }
  const command = commands.get(interaction.commandName);
  if (!command) return;
  if (!interaction.inGuild() || interaction.guildId !== ctx.config.discord.guildId) {
    return interaction.reply({ content: 'This bot only works in its configured server.', flags: MessageFlags.Ephemeral });
  }
  try {
    await command.execute(interaction, ctx);
  } catch (err) {
    ctx.logger.error(`/${interaction.commandName} failed:`, err);
    const msg = `Something went wrong: ${err.message}`;
    if (interaction.deferred || interaction.replied) await interaction.editReply(msg).catch(() => {});
    else await interaction.reply({ content: msg, flags: MessageFlags.Ephemeral }).catch(() => {});
  }
}
