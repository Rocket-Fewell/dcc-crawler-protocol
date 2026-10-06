/**
 * GM-output tag contract (decision 032 / Caleb Oct 5 2026).
 *
 *   [SYSTEM] ...  -> spoken in the "system" voice (dry, informative, corporate: clock, fees,
 *                    registration, collapse warnings, floor notices, welcome/registration). No jokes.
 *   [GM] ...      -> spoken in the narrator ("gm") voice (snarky: achievements banner+description,
 *                    loot-box callouts/openings, jokes and color)
 *   [ROLL] ...    -> never spoken
 *   [NPC: Name] ... -> spoken in that NPC's own Fish voice from <campaign>/tables/npc-voices.json (src/npcvoices.js):
 *                    name matched case-insensitively, punctuation and extra spaces ignored, aliases allowed. No voice
 *                    id, or not in the map: narrator voice. (Caleb Oct 6 2026.)
 *   (no tag)      -> narrator voice (or the caller's default voice) — same as [GM]
 *
 * Tags are matched per line, case-insensitively, at the start of a line (optionally preceded by
 * whitespace and markdown such as `**[SYSTEM]**` or `> [GM]`). A tag applies to its own line and to
 * every following line until the next tag. Tags inside ``` code fences are ignored. The tag text itself is never
 * spoken (it is stripped before TTS, so Fish bills only the words).
 * Mixed messages: after a [SYSTEM] line, re-tag [GM] before any snark so carry-over stays correct.
 *
 * Safety net (Caleb Oct 6 2026): rules notes and corrections to a Crawler's requested action are
 * always System voice. An untagged line that opens with "Rules note", "Rule note", "Rules check",
 * "Rules correction" or "System note" is spoken in the system voice for that line only, then the
 * previous voice resumes. The GM should still tag these [SYSTEM].
 */

export const VOICE_GM = 'gm';
export const VOICE_SYSTEM = 'system';
export const VOICES = [VOICE_GM, VOICE_SYSTEM];
/** NPC voices are 'npc:<normalized name>' (see npcKey); TTS providers resolve them, unknown ones fall back to the narrator. */
export const NPC_PREFIX = 'npc:';

/**
 * Normalized NPC name for the voice key and the voice-map lookup: case-insensitive, punctuation (hyphens, dots, brackets,
 * quotes) and extra spaces ignored, so "Snakk-Matic", "snakk matic" and "SNAKK  MATIC" are one NPC, as are
 * "Dean Thudd (JV)" and "Dean Thudd JV".
 */
export const npcKey = (name) => String(name ?? '').normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
export const isNpcVoice = (voice) => typeof voice === 'string' && voice.startsWith(NPC_PREFIX);
export const npcNameOf = (voice) => (isNpcVoice(voice) ? voice.slice(NPC_PREFIX.length) : null);

const TAG_LINE = /^[\s>*_~`|]*\[\s*(SYSTEM|GM|ROLL|NPC\s*:([^\]\n]*))\s*\][*_~`|]*[ \t]*:?[ \t]*(.*)$/i;
/** A stray [NPC: Name] left mid-line is never read aloud (mid-line [SYSTEM]/[GM]/[ROLL] keep their old handling). */
const STRAY_TAG = /\[\s*NPC\s*:[^\]\n]*\]/gi;
const HAS_STRAY_TAG = /\[\s*NPC\s*:[^\]\n]*\]/i;
export const stripStrayTags = (text) => {
  const t = String(text ?? '');
  return HAS_STRAY_TAG.test(t) ? t.replace(STRAY_TAG, ' ').replace(/[ \t]{2,}/g, ' ') : t;
};
const SKIP = null; // marker for [ROLL]
const RULES_NOTE_LINE = /^[\s>*_~`|]*(?:rules?\s+(?:note|check|correction)|system\s+note)\b/i;

/**
 * Split raw message text into voiced segments. Consecutive lines with the same voice are merged.
 * [ROLL] content is dropped.
 * @param {string} raw
 * @param {{ defaultVoice?: 'gm' | 'system' }} [opts]
 * @returns {{ voice: string, text: string }[]}  voice: 'gm' | 'system' | 'npc:<name>'
 */
export function parseTaggedLines(raw, { defaultVoice = VOICE_GM } = {}) {
  const segments = [];
  let voice = defaultVoice; // VOICE_* or SKIP
  let inFence = false;

  const push = (line) => {
    if (voice === SKIP) return;
    const last = segments[segments.length - 1];
    if (last && last.voice === voice) last.text += `\n${line}`;
    else segments.push({ voice, text: line });
  };

  for (const line of String(raw ?? '').replace(/\r\n?/g, '\n').split('\n')) {
    if (/^\s*```/.test(line)) {
      // A fence line toggles state (unless it opens and closes on one line); it stays with the
      // current voice and cleaning strips the code later.
      if (!/^\s*```.*```\s*$/.test(line)) inFence = !inFence;
      push(line);
      continue;
    }
    const m = inFence ? null : TAG_LINE.exec(line);
    if (m) {
      const tag = m[1].toUpperCase();
      if (tag.startsWith('NPC')) {
        const key = npcKey(m[2]);
        voice = key ? `${NPC_PREFIX}${key}` : VOICE_GM;   // "[NPC:]" with no name = narrator
      } else {
        voice = tag === 'ROLL' ? SKIP : tag === 'SYSTEM' ? VOICE_SYSTEM : VOICE_GM;
      }
      if (m[3]) push(m[3]);
    } else if (!inFence && voice !== VOICE_SYSTEM && RULES_NOTE_LINE.test(line)) {
      const prev = voice;
      voice = VOICE_SYSTEM;
      push(line);
      voice = prev;
    } else {
      push(line);
    }
  }
  return segments.map((s) => ({ ...s, text: stripStrayTags(s.text) })).filter((s) => s.text.trim().length > 0);
}
