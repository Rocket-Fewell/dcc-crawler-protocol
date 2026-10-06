/**
 * NPC voice map (Caleb, Oct 6 2026): every NPC gets its own Fish Audio library voice.
 *
 * File: <campaign>/tables/npc-voices.json (campaign root from src/paths.js; NPC_VOICES_FILE overrides), written by
 * `npm run npc-voices:import`. Shape:
 *   { "schema": "npc-voices/0.1", "version": "0.1.0", ..., "npcs": [
 *       { "name": "Mordecai", "aliases": ["Mordy"], "floors": [1], "fish_voice_id": "<32 hex>", "note": "who/what" } ] }
 * Lookup: case-insensitive, extra spaces ignored, name or any alias. No entry or no valid id -> null (caller uses the
 * narrator). The file is re-read when it changes (polling, so an atomic rename by the importer is seen too).
 */
import { existsSync, readFileSync, unwatchFile, watchFile } from 'node:fs';
import { join } from 'node:path';
import { resolveCampaignRoot } from './paths.js';
import { npcKey } from './tags.js';

export const FISH_ID = /^[0-9a-f]{32}$/;
export const npcVoicesFile = (campaignDir = resolveCampaignRoot(), env = process.env) =>
  env.NPC_VOICES_FILE || join(campaignDir, 'tables', 'npc-voices.json');

export class NpcVoiceMap {
  constructor({ file, logger = null, pollMs = 2000 } = {}) {
    this.file = file;
    this.log = logger ?? { info() {}, warn() {}, debug() {} };
    this.pollMs = pollMs;
    this.byKey = new Map();   // npcKey(name or alias) -> entry
    this.entries = [];
    this.loadedAt = null;
    this.error = null;
  }

  get size() {
    return this.entries.length;
  }

  /** (Re)read the file. A missing file = empty map; a broken file keeps the last good map and logs a warning. */
  load() {
    if (!existsSync(this.file)) {
      this.entries = [];
      this.byKey = new Map();
      this.error = 'missing';
      return this;
    }
    let doc;
    try {
      doc = JSON.parse(readFileSync(this.file, 'utf8'));
    } catch (err) {
      this.error = err.message;
      this.log.warn(`npc-voices: ${this.file} is not valid JSON (${err.message}); keeping the previous map (${this.size} entries)`);
      return this;
    }
    const list = Array.isArray(doc) ? doc : Array.isArray(doc?.npcs) ? doc.npcs : [];
    const entries = [];
    const byKey = new Map();
    for (const raw of list) {
      const name = String(raw?.name ?? '').trim();
      if (!name) continue;
      let id = raw.fish_voice_id == null ? null : String(raw.fish_voice_id).trim().toLowerCase();
      if (id && !FISH_ID.test(id)) {
        this.log.warn(`npc-voices: ${name} has an invalid fish_voice_id (not 32 hex chars); using the narrator voice`);
        id = null;
      }
      const e = { name, aliases: (raw.aliases ?? []).map(String).filter(Boolean), floors: raw.floors ?? [], fish_voice_id: id || null, note: raw.note ?? '' };
      entries.push(e);
      for (const k of [name, ...e.aliases].map(npcKey)) {
        if (!k) continue;
        if (byKey.has(k) && byKey.get(k) !== e) this.log.warn(`npc-voices: "${k}" is used by both ${byKey.get(k).name} and ${name}; the first wins`);
        else byKey.set(k, e);
      }
    }
    this.entries = entries;
    this.byKey = byKey;
    this.loadedAt = Date.now();
    this.error = null;
    return this;
  }

  /** Entry for a tag name (or an npc key), or null. */
  find(name) {
    return this.byKey.get(npcKey(name)) ?? null;
  }

  /** The Fish voice id for an NPC name, or null (no entry / no id -> narrator). */
  voiceIdFor(name) {
    return this.find(name)?.fish_voice_id ?? null;
  }

  /** Re-read on change (no restart needed after an import). */
  watch() {
    this.unwatch();
    this._listener = (cur, prev) => {
      if (cur.mtimeMs === prev.mtimeMs && cur.size === prev.size) return;
      const before = this.size;
      this.load();
      this.log.info(`npc-voices: reloaded ${this.file} (${this.size} entr${this.size === 1 ? 'y' : 'ies'}${before !== this.size ? `, was ${before}` : ''})`);
    };
    watchFile(this.file, { interval: this.pollMs, persistent: false }, this._listener);
    return this;
  }

  unwatch() {
    if (this._listener) unwatchFile(this.file, this._listener);
    this._listener = null;
  }

  summary() {
    const withId = this.entries.filter((e) => e.fish_voice_id).length;
    return `${this.size} entr${this.size === 1 ? 'y' : 'ies'} (${withId} with a Fish voice id) from ${this.file}${this.error === 'missing' ? ' [file not found: everyone uses the narrator]' : ''}`;
  }
}
