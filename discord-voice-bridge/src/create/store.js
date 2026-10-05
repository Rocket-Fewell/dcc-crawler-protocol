/** Draft + log storage for /create: one JSON file per Discord user per session, mode 600, written atomically. */
import { appendFileSync, chmodSync, existsSync, mkdirSync, readFileSync, readdirSync, renameSync, unlinkSync, writeFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

export const draftsDir = (config) => join(config.campaign.dataDir, 'create-drafts');
export const draftPath = (config, uid) => join(draftsDir(config), `${String(uid).replace(/\D/g, '')}.json`);
export const logPath = (config) => join(config.campaign.dataDir, 'create-log.jsonl');

export function ensureDir(dir) {
  mkdirSync(dir, { recursive: true, mode: 0o700 });
}

export function readDraft(config, uid) {
  try {
    return JSON.parse(readFileSync(draftPath(config, uid), 'utf8'));
  } catch {
    return null;
  }
}

export function writeDraft(config, d) {
  ensureDir(draftsDir(config));
  d.updated = new Date().toISOString();
  const p = draftPath(config, d.uid);
  const tmp = `${p}.${process.pid}.tmp`;
  writeFileSync(tmp, JSON.stringify(d, null, 1), { mode: 0o600 });
  chmodSync(tmp, 0o600);
  renameSync(tmp, p);
}

export function deleteDraft(config, uid) {
  try {
    unlinkSync(draftPath(config, uid));
  } catch {
    /* already gone */
  }
}

export function listDrafts(config) {
  try {
    return readdirSync(draftsDir(config))
      .filter((f) => /^\d+\.json$/.test(f))
      .map((f) => JSON.parse(readFileSync(join(draftsDir(config), f), 'utf8')));
  } catch {
    return [];
  }
}

/** Idle drafts (default 14 days) move to _archive; nothing is deleted. Drafts with rolled ability rounds stay where they are. */
export function archiveIdle(config, days = 14, now = Date.now()) {
  let n = 0;
  const dir = draftsDir(config);
  if (!existsSync(dir)) return 0;
  for (const f of readdirSync(dir)) {
    if (!/^\d+\.json$/.test(f)) continue;
    const p = join(dir, f);
    if (now - statSync(p).mtimeMs > days * 86_400_000) {
      // a draft that holds rolled ability rounds is never archived: archiving would hand the player a free reroll (decision 024)
      try { if (JSON.parse(readFileSync(p, 'utf8')).scoreRolls?.rounds?.length) continue; } catch { /* unreadable: archive as before */ }
      ensureDir(join(dir, '_archive'));
      renameSync(p, join(dir, '_archive', `${f.replace('.json', '')}-${new Date(now).toISOString().slice(0, 10)}.json`));
      n++;
    }
  }
  return n;
}

/** True while a play session is recorded open (tools/state.py session-status; the bridge writes it when it joins voice). */
export function sessionIsOpen(config) {
  try {
    return String(JSON.parse(readFileSync(join(config.campaign.dataDir, 'session-status.json'), 'utf8')).status).toLowerCase() === 'open';
  } catch { return false; }
}

export function readSessionState(config) {
  try {
    return JSON.parse(readFileSync(join(config.campaign.dataDir, 'state.json'), 'utf8'));
  } catch {
    return null;
  }
}

/** Staff log: what happened, never private content (no answers, no opt-outs). */
export function appendLog(config, entry) {
  ensureDir(config.campaign.dataDir);
  appendFileSync(logPath(config), JSON.stringify({ ts: new Date().toISOString(), ...entry }) + '\n', { mode: 0o600 });
}
