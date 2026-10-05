import { mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { dirname } from 'node:path';

/**
 * Runtime on/off switch for the GM wake webhook (`/gm pause|resume|status`). Kept in memory and persisted to a
 * small JSON file so it survives a restart. Default (no / unreadable file) = running (not paused).
 */
export class GmWakeState {
  constructor({ file, logger } = {}) {
    this.file = file;
    this.log = logger;
    this.paused = false;
    this.since = null;
    this.by = null;
    this.load();
  }

  load() {
    try {
      if (!this.file) return;
      const d = JSON.parse(readFileSync(this.file, 'utf8'));
      if (d && typeof d === 'object') {
        this.paused = d.paused === true;
        this.since = typeof d.updated === 'string' ? d.updated : null;
        this.by = typeof d.by === 'string' ? d.by : null;
      }
    } catch {
      /* missing or malformed => running */
    }
  }

  set(paused, by = null) {
    this.paused = Boolean(paused);
    this.since = new Date().toISOString();
    this.by = by;
    this._save();
  }

  _save() {
    if (!this.file) return;
    try {
      mkdirSync(dirname(this.file), { recursive: true });
      const tmp = `${this.file}.${process.pid}.tmp`;
      writeFileSync(tmp, `${JSON.stringify({ paused: this.paused, updated: this.since, by: this.by })}\n`);
      renameSync(tmp, this.file);
    } catch (err) {
      this.log?.warn(`Could not persist GM wake state (${err?.code ?? err?.name}); it will reset on restart`);
    }
  }
}
