import { EventEmitter } from 'node:events';
import {
  AudioPlayerStatus,
  NoSubscriberBehavior,
  VoiceConnectionStatus,
  createAudioPlayer,
  entersState,
  joinVoiceChannel,
} from '@discordjs/voice';

/**
 * Owns the single voice connection + AudioPlayer for the configured guild.
 * Emits: 'joined' (connection), 'left'.
 */
export class VoiceSession extends EventEmitter {
  constructor({ logger }) {
    super();
    this.log = logger;
    this.connection = null;
    this.channelId = null;
    this.player = createAudioPlayer({ behaviors: { noSubscriber: NoSubscriberBehavior.Pause } });
    this.player.on('stateChange', (o, n) => {
      if (o.status !== n.status) this.log.debug(`Player: ${o.status} -> ${n.status}`);
    });
    this.player.on('error', (e) => this.log.warn(`Player error: ${e.message}`));
  }

  get isConnected() {
    return this.connection?.state.status === VoiceConnectionStatus.Ready;
  }

  get isPlaying() {
    return this.player.state.status === AudioPlayerStatus.Playing;
  }

  /** Join (or move to) a voice/stage channel. Resolves once the connection is Ready. */
  async join(channel) {
    if (this.connection && this.channelId === channel.id && this.isConnected) return this.connection;
    this.leave();

    const connection = joinVoiceChannel({
      channelId: channel.id,
      guildId: channel.guild.id,
      adapterCreator: channel.guild.voiceAdapterCreator,
      selfDeaf: false, // must be undeafened to receive player audio
      selfMute: false,
      daveEncryption: true, // Discord's E2EE (DAVE) is mandatory; requires @snazzah/davey
    });

    connection.on('error', (err) => this.log.error(`Voice connection error: ${err.message}`));
    connection.on('debug', (m) => this.log.debug(`[voice] ${m}`));
    connection.on('stateChange', (o, n) => {
      if (o.status !== n.status) this.log.info(`Voice: ${o.status} -> ${n.status}`);
    });

    // Standard reconnect pattern: if Discord moved/dropped us, give it a few seconds to re-signal.
    connection.on(VoiceConnectionStatus.Disconnected, async () => {
      try {
        await Promise.race([
          entersState(connection, VoiceConnectionStatus.Signalling, 5_000),
          entersState(connection, VoiceConnectionStatus.Connecting, 5_000),
        ]);
      } catch {
        if (connection.state.status !== VoiceConnectionStatus.Destroyed) connection.destroy();
      }
    });
    connection.on(VoiceConnectionStatus.Destroyed, () => {
      if (this.connection === connection) {
        this.connection = null;
        this.channelId = null;
        this.player.stop(true);
        this.emit('left');
      }
    });

    this.connection = connection;
    this.channelId = channel.id;
    try {
      await entersState(connection, VoiceConnectionStatus.Ready, 30_000);
    } catch (err) {
      if (connection.state.status !== VoiceConnectionStatus.Destroyed) connection.destroy();
      throw new Error(`Could not connect to voice channel within 30s (${err.message})`);
    }
    connection.subscribe(this.player);
    this.log.info(`Joined voice channel ${channel.name ?? channel.id}`);
    this.emit('joined', connection);
    return connection;
  }

  leave() {
    const connection = this.connection;
    if (!connection) return false;
    if (connection.state.status !== VoiceConnectionStatus.Destroyed) connection.destroy(); // triggers 'left'
    return true;
  }
}
