/**
 * GM-output tag contract (decision 032 / Caleb Oct 5 2026).
 *
 *   [SYSTEM] ...  -> spoken in the "system" voice (dry, informative, corporate: clock, fees,
 *                    registration, collapse warnings, floor notices, welcome/registration). No jokes.
 *   [GM] ...      -> spoken in the narrator ("gm") voice (snarky: achievements banner+description,
 *                    loot-box callouts/openings, jokes and color)
 *   [ROLL] ...    -> never spoken
 *   (no tag)      -> narrator voice (or the caller's default voice) — same as [GM]
 *
 * Tags are matched per line, case-insensitively, at the start of a line (optionally preceded by
 * whitespace and markdown such as `**[SYSTEM]**` or `> [GM]`). A tag applies to its own line and to
 * every following line until the next tag. Tags inside ``` code fences are ignored.
 * Mixed messages: after a [SYSTEM] line, re-tag [GM] before any snark so carry-over stays correct.
 */

export const VOICE_GM = 'gm';
export const VOICE_SYSTEM = 'system';
export const VOICES = [VOICE_GM, VOICE_SYSTEM];

const TAG_LINE = /^[\s>*_~`|]*\[(SYSTEM|GM|ROLL)\][*_~`|]*[ \t]*:?[ \t]*(.*)$/i;
const SKIP = null; // marker for [ROLL]

/**
 * Split raw message text into voiced segments. Consecutive lines with the same voice are merged.
 * [ROLL] content is dropped.
 * @param {string} raw
 * @param {{ defaultVoice?: 'gm' | 'system' }} [opts]
 * @returns {{ voice: 'gm' | 'system', text: string }[]}
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
      voice = tag === 'ROLL' ? SKIP : tag === 'SYSTEM' ? VOICE_SYSTEM : VOICE_GM;
      if (m[2]) push(m[2]);
    } else {
      push(line);
    }
  }
  return segments.filter((s) => s.text.trim().length > 0);
}
