/**
 * Duplicate suppression for GM messages: drop a message if the same author already had identical (whitespace/
 * case-normalized) speakable text spoken or queued within the last `windowSeconds`, or near-identical text
 * (one contains the other, e.g. a prefix, and the shorter is > 90% of the longer's length).
 */
export function normalizeForDedupe(text) {
  return String(text ?? '').normalize('NFC').toLowerCase().replace(/\s+/g, ' ').trim();
}

/** @returns {'exact'|'near'|null} */
export function compareTexts(a, b) {
  if (!a || !b) return null;
  if (a === b) return 'exact';
  const [short, long] = a.length <= b.length ? [a, b] : [b, a];
  if (long.includes(short) && short.length / long.length > 0.9) return 'near';
  return null;
}

export class DuplicateGuard {
  constructor({ windowSeconds = 120, now = () => Date.now() } = {}) {
    this.windowMs = Math.max(0, windowSeconds) * 1000;
    this.now = now;
    this.history = []; // { author, norm, at }
  }

  get enabled() {
    return this.windowMs > 0;
  }

  _prune() {
    const cutoff = this.now() - this.windowMs;
    this.history = this.history.filter((h) => h.at >= cutoff);
  }

  /** @returns {{duplicate:boolean, kind?:'exact'|'near', ageSeconds?:number}} */
  check(author, text) {
    if (!this.enabled) return { duplicate: false };
    this._prune();
    const norm = normalizeForDedupe(text);
    for (const h of this.history) {
      if (h.author !== author) continue;
      const kind = compareTexts(norm, h.norm);
      if (kind) return { duplicate: true, kind, ageSeconds: Math.round((this.now() - h.at) / 1000) };
    }
    return { duplicate: false };
  }

  /** Call once a message was actually queued for speech. */
  remember(author, text) {
    if (!this.enabled) return;
    this._prune();
    this.history.push({ author, norm: normalizeForDedupe(text), at: this.now() });
  }

  /** Forget everything (after /shush, /skip or a flush: the content was not actually spoken). */
  clear() {
    this.history = [];
  }
}
