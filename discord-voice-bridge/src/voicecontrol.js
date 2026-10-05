import { readFileSync, statSync } from 'node:fs';

/**
 * File-based kill switch for the GM tool: `python3 tools/discord_gm.py stop` atomically writes
 *   {"action":"flush","id":"<unique>","ts":"ISO"}
 * to VOICE_CONTROL_FILE. When the `id` changes to a value the bridge has not seen, it flushes the speech queue
 * and playback. The id present at startup is only recorded (a stale file never flushes on boot). Polling is
 * used instead of fs.watch because atomic replace-writes confuse watchers. Never throws.
 */
export function readControl(file) {
  try {
    if (statSync(file).size > 16 * 1024) return null;
    const d = JSON.parse(readFileSync(file, 'utf8'));
    if (!d || typeof d !== 'object' || typeof d.id !== 'string' || !d.id.trim()) return null;
    return { action: typeof d.action === 'string' ? d.action : '', id: d.id, ts: d.ts };
  } catch {
    return null;
  }
}

export class VoiceControlWatcher {
  /**
   * @param {{ file: string, onFlush: (info:{id:string, ts?:string}) => void, logger?: any, pollMs?: number }} o
   */
  constructor({ file, onFlush, logger, pollMs = 500 }) {
    Object.assign(this, { file, onFlush, pollMs });
    this.log = logger;
    this.lastId = null;
    this.timer = null;
  }

  start() {
    this.lastId = readControl(this.file)?.id ?? null; // baseline: ignore whatever is already there
    this.timer = setInterval(() => this.poll(), this.pollMs);
    this.timer.unref?.();
    return this;
  }

  stop() {
    clearInterval(this.timer);
    this.timer = null;
  }

  /** One check (exposed for tests). Returns true when a flush was triggered. */
  poll() {
    const c = readControl(this.file);
    if (!c || c.id === this.lastId) return false;
    this.lastId = c.id;
    if (c.action !== 'flush') {
      this.log?.warn(`Voice control: ignoring unknown action "${String(c.action).slice(0, 20)}"`);
      return false;
    }
    try {
      this.onFlush({ id: c.id, ts: c.ts });
    } catch (err) {
      this.log?.warn(`Voice control flush failed: ${err?.message ?? err}`);
    }
    return true;
  }
}
