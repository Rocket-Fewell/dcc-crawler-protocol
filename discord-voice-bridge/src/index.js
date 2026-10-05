import { markSession } from './create/manage.js';
import { FishBalanceMonitor, fetchFishBalance, lowBalanceThreshold } from './fishbalance.js';
import { createSettings } from './create/settings.js';
import { Client, Events, GatewayIntentBits } from 'discord.js';
import { handleInteraction } from './commands/index.js';
import { ConfigError, loadConfig } from './config.js';
import { MonthlyShare } from './monthlycap.js';
import { replaceInPlace, resolveActiveId, sessionEnv, sessionExists, writeActive } from './session.js';
import { createLogger } from './logger.js';
import { checkReskinHash } from './create/reskin.js';
import { LAYERS, checkLayerHash } from './create/layers.js';
import './create/names.js';      // register the display layers
import './create/bgnames.js';
import './create/screenstext.js';
import { SpeechQueue } from './queue.js';
import { SessionVoiceCap, fmt } from './sessioncap.js';
import { DuplicateGuard } from './dedupe.js';
import { GmWakeState } from './gmpause.js';
import { createSpotlightFilter } from './spotlight.js';
import { VoiceControlWatcher } from './voicecontrol.js';
import { WakeBudget, formatClock, loadWakeHistory } from './wakebudget.js';
import { UsageLogger, VoiceEventLogger, WakeUsageLogger, meteredSynthesize } from './usage.js';
import { SttBridge } from './stt.js';
import { GmOutputBridge, createTtsProvider } from './tts.js';
import { GmWakeNotifier } from './wake.js';
import { VoiceSession } from './voice.js';

let config;
try {
  // One bot, one ACTIVE campaign session ("alpha" unless DCC_SESSION or `/session use` says otherwise); see src/session.js.
  config = loadConfig(sessionEnv(process.env, resolveActiveId(process.env)));
} catch (err) {
  if (err instanceof ConfigError) {
    console.error(err.message);
    console.error('\nCopy .env.example to .env and fill it in.');
    process.exit(1);
  }
  throw err;
}

const log = createLogger(config.logLevel);
log.info(`Campaign session: ${config.campaign.sessionId} (data ${config.campaign.dataDir})`);
{ // item-reskins.json must be Lore's single file: its sha256 has to match item-reskins.version.json (warn only; the bridge still starts)
  const rs = checkReskinHash(config.campaign.dir);
  if (rs.status === 'ok') log.info(`item-reskins: ${rs.message}`);
  else log.warn(`item-reskins: ${rs.message}`);
  for (const spec of LAYERS.values()) {   // display layers (species/class, background, ...): absent = plain 5e text (not delivered/approved yet), hash mismatch = warning only
    const h = checkLayerHash(spec, config.campaign.dir);
    if (h.status === 'ok' || h.status === 'absent') log.info(`${spec.file.replace(/\.json$/, '')}: ${h.message}`);
    else log.warn(`${spec.file.replace(/\.json$/, '')}: ${h.message}`);
  }
}

{
  const [major, minor] = process.versions.node.split('.').map(Number);
  if (major < 22 || (major === 22 && minor < 12)) {
    log.warn(`Node ${process.versions.node} detected: @discordjs/voice 0.19 (needed for Discord's DAVE E2EE) requires Node >= 22.12.0`);
  }
}

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildVoiceStates,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent, // privileged: enable in the Developer Portal
  ],
});

const session = new VoiceSession({ logger: log.child('voice') });
const provider = config.tts.enabled ? createTtsProvider(config) : null;
if (provider) log.info(`TTS provider: ${provider.name}`);
if (config.tts.enabled && config.tts.provider === 'elevenlabs' && config.tts.elevenlabs.systemVoiceFallback) {
  log.warn('ELEVENLABS_SYSTEM_VOICE_ID not set: [SYSTEM] lines will use the narrator voice');
}
const usage = new UsageLogger({
  dccSession: config.campaign.sessionId,
  path: config.usage.path,
  enabled: config.usage.enabled,
  charsPerMinute: config.usage.charsPerMinute,
  logger: log.child('usage'),
});
if (provider && usage.enabled) log.info(`TTS usage log: ${usage.path} (session ${usage.session})`);
if (config.tts.enabled && config.tts.provider === 'fish' && config.tts.fish.voiceFallback) {
  log.warn('Only one of FISH_VOICE_ID_NARRATOR / FISH_VOICE_ID_SYSTEM is set: it is used for both voices');
}
// Hard per-session cap on spoken minutes (reset on every /join). Notices go to the transcript channel.
async function postStatus(text) {
  const id = config.discord.transcriptChannelId;
  if (!id) return;
  const ch = await client.channels.fetch(id).catch(() => null);
  if (ch?.isTextBased()) await ch.send({ content: text, allowedMentions: { parse: [] } });
}
const gmChannelRef = config.discord.gmOutputChannelId ? `<#${config.discord.gmOutputChannelId}>` : 'the GM text channel';
const sessionCap = new SessionVoiceCap({
  capMinutes: config.usage.sessionCapMinutes,
  logger: log.child('voicecap'),
  onWarn: (st) => postStatus(`⚠️ Voice session at ${Math.round(st.percent)}% of its cap (${fmt(st.used)}/${fmt(st.cap)} min). Spoken GM narration will stop at the cap; text continues in ${gmChannelRef}.`),
  onReached: (st) =>
    postStatus(
      st.reason === 'share' || st.reason === 'total'
        ? `🔇 ${st.reason === 'share' ? "This table's share of the month's Fish voice minutes" : 'The shared monthly Fish voice minutes'} ran out. The GM is no longer spoken aloud; the story continues as text in ${gmChannelRef}.`
        : `🔇 Session voice cap reached (${fmt(st.cap)} min). The GM is no longer spoken aloud; the story continues as text in ${gmChannelRef}.`
    ),
});
// Monthly Fish minutes: this campaign session's share + the shared total (usage log is the source, so restarts keep the count).
const monthly = new MonthlyShare({
  logPath: config.usage.path,
  getSession: () => config.campaign.sessionId,
  getShare: () => config.usage.sessionMonthlyMinutes,
  getTotalCap: () => config.usage.fishMonthlyCapMinutes,
  logger: log.child('monthly'),
});
if (provider && config.tts.provider === 'fish') sessionCap.setExternalLimit(() => monthly.status());
if (provider) log.info(`Voice session cap: ${sessionCap.enabled ? `${sessionCap.capMinutes} min per /join session` : 'disabled'}`);
const metered = provider ? meteredSynthesize(provider, usage, sessionCap) : null;
const queue = new SpeechQueue({
  player: session.player,
  synthesize: (text, voice) => {
    if (!metered) throw new Error('TTS disabled');
    return metered(text, voice);
  },
  prefetch: config.tts.prefetch,
  logger: log.child('queue'),
  maxChunks: config.voice.maxQueuedChunks,
  maxSeconds: config.voice.maxQueuedSeconds,
  charsPerMinute: config.usage.charsPerMinute,
  onBacklogDrop: (d) => onBacklogDrop(d),
});
queue.enabled = false; // until we're in a voice channel

// Voice-side protections: event log, duplicate suppression, backlog notice, flush (/shush + file kill switch).
const events = new VoiceEventLogger({ dccSession: config.campaign.sessionId, path: config.voice.eventsLogPath, enabled: config.voice.eventsLogEnabled, session: usage.session, logger: log.child('events') });
const dedupe = new DuplicateGuard({ windowSeconds: config.voice.duplicateWindowSeconds });
let lastBacklogNotice = 0;
function onBacklogDrop({ messages, chunks }) {
  log.warn(`Speech backlog over limit (${config.voice.maxQueuedChunks} chunks / ${config.voice.maxQueuedSeconds}s): dropped the ${messages} oldest pending message(s) (${chunks} chunk(s)); kept the newest`);
  events.record('backlog_dropped', { messages, chunks });
  const now = Date.now();
  if (now - lastBacklogNotice > 60_000) {
    // One notice per overflow event, but at most one a minute so a storm cannot spam the channel.
    lastBacklogNotice = now;
    postStatus(`⏩ Speech backlog: skipped ${messages} older GM message(s) to catch up with the newest. The full text is in ${gmChannelRef}.`).catch((err) => log.warn(`Backlog notice failed: ${err?.message ?? err}`));
  }
}
function flushVoice(source) {
  const dropped = queue.clear();
  session.player.stop(true);
  dedupe.clear();
  events.record('flush', { source, chunks: dropped });
  log.info(`Voice flushed (${source}): stopped playback, cleared ${dropped} queued chunk(s)`);
  return dropped;
}
const gmState = new GmWakeState({ file: config.gmWakeStateFile, logger: log.child('gm') });
if (gmState.paused) log.warn('GM wake is PAUSED (saved state from /gm pause); use /gm resume to wake the GM again');
let voiceControl = null;
if (config.voice.controlEnabled) {
  voiceControl = new VoiceControlWatcher({
    file: config.voice.controlFile,
    pollMs: config.voice.controlPollMs,
    logger: log.child('control'),
    onFlush: ({ id }) => flushVoice(`file:${String(id).slice(0, 8)}`),
  }).start();
  log.info(`Voice kill switch: watching ${config.voice.controlFile}`);
}

// GM wake webhook (OFF unless GM_WEBHOOK_URL is set). Held back while the GM's own TTS is playing.
for (const p of config.wake.problems) log.error(`GM wake disabled/misconfigured: ${p}`);
// Rolling-hour budget of wake POSTs. History is recovered from logs/wake-usage.jsonl so a restart keeps the count.
const wakeBudget = new WakeBudget({ max: config.wake.maxPerHour });
const wakeHistory = () => loadWakeHistory(config.usage.wakeLogPath, { backoffMs: config.wake.rateLimitBackoffMs, dccSession: config.campaign.sessionId });
let restoredBackoff = 0;
if (config.wake.enabled && wakeBudget.enabled) {
  const h = wakeHistory();
  wakeBudget.stamps = h.stamps;
  restoredBackoff = h.rateLimitedUntil;
  log.info(`GM wake budget: ${wakeBudget.used()}/${wakeBudget.max} wakes in the last hour${config.usage.wakeLogEnabled ? '' : ' (WAKE_USAGE_LOG_ENABLED=false: count will not survive a restart)'}`);
}
const wake = new GmWakeNotifier({
  wake: config.wake,
  isBusy: () => queue.size > 0 || session.isPlaying,
  isPaused: () => gmState.paused,
  budget: wakeBudget,
  onBlocked: ({ reason, resumeAt }) =>
    postStatus(reason === 'budget'
      ? `⏳ GM wake budget reached, replies resume at ${formatClock(resumeAt)}. Lines are held, not lost.`
      : `⏳ The GM platform rate-limited wake-ups; replies resume at ${formatClock(resumeAt)}. Lines are held, not lost.`),
  logger: log.child('wake'),
  filter: config.spotlight.enabled ? createSpotlightFilter({ config: config.spotlight, logger: log.child('spotlight') }) : null,
  usageLog: new WakeUsageLogger({
    dccSession: config.campaign.sessionId,
    path: config.usage.wakeLogPath,
    enabled: config.usage.wakeLogEnabled,
    session: usage.session,
    logger: log.child('wake'),
  }),
});
if (wake.enabled) {
  wake.rateLimitedUntil = restoredBackoff;
  log.info(`Spotlight wake filter: ${config.spotlight.enabled ? `ON (file ${config.spotlight.file}, stale after ${config.spotlight.maxAgeMinutes} min; fails open)` : 'disabled'}`);
  log.info(
    `GM wake webhook: ON (debounce ${config.wake.debounceMs}ms, max wait ${config.wake.maxWaitMs}ms, min interval ${config.wake.minIntervalMs}ms)`
  );
}
const stt = new SttBridge({ client, config, logger: log.child('stt'), onTranscript: (line) => wake.notify(line) });
const gm = new GmOutputBridge({ client, config, session, queue, logger: log.child('tts'), sessionCap, dedupe, events });
const ctx = { config, client, session, queue, stt, sessionCap, dedupe, gmState, flushVoice, wake, logger: log };

/**
 * Activate another campaign session in place (admin `/session use <id>`; the caller has already checked we are not in voice).
 * Re-derives the config from the session's profile, swaps it into the live config object, and re-points everything that is
 * session-scoped: wake budget + pause switch + kill-switch file, usage-log tags, monthly share. Returns a summary.
 */
ctx.applySession = (id, by = null) => {
  const next = loadConfig(sessionEnv(process.env, id));
  replaceInPlace(config, next);
  writeActive(id, by);
  for (const l of [usage, events, wake.usageLog]) if (l) l.dccSession = id;
  wake.reset();
  const h = wakeHistory();
  wakeBudget.max = Math.max(0, Number(config.wake.maxPerHour) || 0);
  wakeBudget.stamps = h.stamps;
  wake.rateLimitedUntil = h.rateLimitedUntil;
  gmState.file = config.gmWakeStateFile;
  gmState.paused = false;
  gmState.since = gmState.by = null;
  gmState.load();
  voiceControl?.stop();
  if (config.voice.controlEnabled) {
    voiceControl = new VoiceControlWatcher({
      file: config.voice.controlFile,
      pollMs: config.voice.controlPollMs,
      logger: log.child('control'),
      onFlush: ({ id: fid }) => flushVoice(`file:${String(fid).slice(0, 8)}`),
    }).start();
  }
  sessionCap.setCap(config.usage.sessionCapMinutes);
  sessionCap.reset();
  monthly.invalidate();
  dedupe.clear();
  log.info(`Active campaign session is now "${id}" (data ${config.campaign.dataDir}, ears ${config.discord.transcriptChannelId || '-'}, mouth ${config.discord.gmOutputChannelId || '-'}, wake ${config.wake.enabled ? 'ON' : 'off'})`);
  return { id, guildId: config.discord.guildId, wake: config.wake.enabled, ears: config.discord.transcriptChannelId, mouth: config.discord.gmOutputChannelId };
};
ctx.monthly = monthly;
ctx.sessionExists = (id) => sessionExists(id);

session.on('joined', (connection) => {
  sessionCap.reset(); // a new voice session starts with a fresh counter
  queue.enabled = true;
  stt.attach(connection);
});
session.on('left', () => {
  queue.enabled = false;
  queue.clear();
  stt.detach();
  log.info('Left voice channel');
});

client.once(Events.ClientReady, async (c) => {
  log.info(`Logged in as ${c.user.tag}`);
  const guild = await c.guilds.fetch(config.discord.guildId).catch(() => null);
  if (!guild) {
    log.error('Bot is not in GUILD_ID. Invite it with the URL from the README.');
    return;
  }
  for (const [name, id] of [
    ['TRANSCRIPT_CHANNEL_ID', config.discord.transcriptChannelId],
    ['GM_OUTPUT_CHANNEL_ID', config.discord.gmOutputChannelId],
  ]) {
    if (!id) continue;
    const ch = await guild.channels.fetch(id).catch(() => null);
    if (!ch) log.warn(`${name} (${id}) not found or not visible to the bot`);
    else if (!ch.isTextBased()) log.warn(`${name} (${id}) is not a text channel`);
  }
  if (config.discord.autoJoin) {
    try {
      const vc = await guild.channels.fetch(config.discord.voiceChannelId);
      await session.join(vc);
    } catch (err) {
      log.error(`Auto-join failed: ${err.message}`);
    }
  }
});

client.on(Events.InteractionCreate, (i) => handleInteraction(i, ctx));
client.on(Events.MessageCreate, (m) => gm.handle(m).catch((err) => log.error('GM output handler error:', err)));
client.on(Events.Error, (err) => log.error('Discord client error:', err));
client.on(Events.Warn, (m) => log.warn(m));

process.on('unhandledRejection', (err) => log.error('Unhandled rejection:', err));
process.on('uncaughtException', (err) => log.error('Uncaught exception:', err));

// Fish prepaid credit: checked at start, every ~30 min and after each session close; one low-balance warning to the log and the staff channel (never spoken).
const fishBalance = config.tts.enabled && config.tts.provider === 'fish'
  ? new FishBalanceMonitor({
      getBalance: () => fetchFishBalance({ apiKey: config.tts.fish.apiKey, baseUrl: config.tts.fish.baseUrl }),
      threshold: lowBalanceThreshold(process.env.FISH_LOW_BALANCE_USD),
      logger: log.child('fish'),
      notify: async (text) => {
        const id = createSettings(config).staffChannelId;
        if (!id) return;
        const ch = await client.channels.fetch(id);
        await ch?.send({ content: text, allowedMentions: { parse: [] } });
      },
    })
  : null;
client.once(Events.ClientReady, () => fishBalance?.start());

// S3: the session marker follows the real voice connection: closed whenever the bridge leaves voice for ANY reason (/leave, a dropped connection, shutdown).
session.on('left', () => { markSession(ctx, 'close').catch(() => {}); fishBalance?.check('session closed').catch(() => {}); });

let stopping = false;
async function shutdown(signal) {
  if (stopping) return;
  stopping = true;
  log.info(`${signal} received, shutting down`);
  try {
    if (session.connection) await Promise.race([markSession(ctx, 'close'), new Promise((r) => setTimeout(r, 5000))]).catch(() => {});   // before the exit: the process may not live to see 'left'
    queue.clear();
    stt.detach();
    wake.stop();
    voiceControl?.stop();
    fishBalance?.stop();
    session.leave();
    await client.destroy();
  } finally {
    process.exit(0);
  }
}
process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));

await client.login(config.discord.token);
