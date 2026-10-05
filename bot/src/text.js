import { VOICE_GM, parseTaggedLines } from './tags.js';

/** Text helpers: STT hallucination filtering, markdown/emoji stripping for TTS, sentence chunking. */

// ---------- STT output filtering ----------

// Typical Whisper hallucinations on silence/noise (matched after normalisation, whole-string).
const HALLUCINATION_EXACT = new Set([
  'thanks for watching',
  'thank you for watching',
  'thanks for watching!',
  'thank you',
  'thank you.',
  'thanks',
  'you',
  'bye',
  'uh',
  'um',
  'hmm',
  'mm',
  'mhm',
  'oh',
  'ah',
  '.',
  'subtitles by the amara.org community',
  'please subscribe',
  'like and subscribe',
  'see you next time',
  'see you in the next video',
  'thank you very much',
  'thank you so much',
  'thanks for listening',
  'transcribed by',
]);

const HALLUCINATION_PATTERNS = [
  /thanks? for (watching|listening|viewing)/i,
  /(please )?(like,? )?(and )?subscribe( to (my|the) channel)?/i,
  /subtitles? (by|from) .*(amara|community|team)/i,
  /amara\.org/i,
  /transcri(bed|ption) by/i,
  /^\s*\[(music|applause|laughter|silence|blank_audio|noise|inaudible)\]\s*$/i,
  /^\s*\((music|applause|laughter|silence|noise|inaudible|coughs?|sighs?)\)\s*$/i,
  /^\s*♪.*♪?\s*$/,
  /www\.\w+\.\w+/i,
];

function normalize(s) {
  return s
    .toLowerCase()
    .replace(/[\p{P}\p{S}]+/gu, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/** True if a transcription result is empty, filler, or a known Whisper hallucination. */
export function isHallucination(text) {
  if (!text) return true;
  const trimmed = text.trim();
  if (trimmed.length === 0) return true;
  const norm = normalize(trimmed);
  if (norm.length === 0) return true; // only punctuation
  if (HALLUCINATION_EXACT.has(norm)) return true;
  if (HALLUCINATION_PATTERNS.some((re) => re.test(trimmed))) return true;
  // Same word/phrase repeated many times ("you you you you ...")
  const words = norm.split(' ');
  if (words.length >= 5) {
    const unique = new Set(words);
    if (unique.size <= 2) return true;
  }
  // A long single token repeated (e.g. "aaaaaaaa")
  if (/^(.)\1{7,}$/.test(norm.replace(/\s/g, ''))) return true;
  return false;
}

// ---------- TTS text preparation ----------

const EMOJI_RE = /[\p{Extended_Pictographic}\p{Regional_Indicator}\u{FE0E}\u{FE0F}\u{200D}\u{20E3}\u{1F3FB}-\u{1F3FF}\u{E0020}-\u{E007F}]/gu;

/** Strip markdown, code blocks, links, emoji, mentions-markup, etc. so the text reads well aloud. */
export function cleanForSpeech(input) {
  if (!input) return '';
  let t = String(input).replace(/\r\n?/g, '\n');

  // Fenced and inline code
  t = t.replace(/```[\s\S]*?(```|$)/g, ' ');
  t = t.replace(/`([^`\n]+)`/g, '$1');
  // Discord markup: custom emoji, timestamps, raw mentions that weren't resolved
  t = t.replace(/<a?:\w+:\d+>/g, ' ');
  t = t.replace(/<t:\d+(?::[a-zA-Z])?>/g, ' ');
  t = t.replace(/<(@[!&]?|#)\d+>/g, ' ');
  t = t.replace(/:[a-z0-9_+-]{2,}:/gi, ' '); // :shortcode: emoji
  // Images, markdown links, autolinks, bare URLs
  t = t.replace(/!\[[^\]]*\]\([^)]*\)/g, ' ');
  t = t.replace(/\[([^\]]+)\]\([^)]*\)/g, '$1');
  t = t.replace(/<(https?:\/\/[^>\s]+)>/g, ' ');
  t = t.replace(/https?:\/\/\S+/gi, ' ');
  // Spoilers, bold/italic/underline/strikethrough
  t = t.replace(/\|\|([\s\S]*?)\|\|/g, '$1');
  t = t.replace(/(\*\*\*|\*\*|\*|__|~~)(?=\S)([\s\S]*?\S)\1/g, '$2');
  t = t.replace(/(^|[\s(])_(?=\S)([^_\n]*?\S)_(?=[\s).,!?;:]|$)/g, '$1$2');
  // Block-level markup, line by line
  t = t
    .split('\n')
    .map((line) =>
      line
        .replace(/^\s{0,3}#{1,6}\s+/, '') // headings
        .replace(/^\s*>{1,3}\s?/, '') // blockquotes
        .replace(/^\s*([-*+•]|\d+[.)])\s+/, '') // bullets / numbered lists
        .replace(/^\s*([-*_=]\s*){3,}$/, '') // horizontal rules
        .replace(/^\s*-#\s+/, '') // subtext
        .replace(/^\s*\|?[\s:|-]+\|[\s:|-]*$/, '') // table separator rows
        .replace(/\s*\|\s*/g, ', ') // table cells
    )
    .join('\n');
  // Any leftover stray markers
  t = t.replace(/[*_~`|]+/g, '');
  // Emoji
  t = t.replace(EMOJI_RE, ' ');
  // Whitespace: keep paragraph breaks as newlines
  t = t
    .split('\n')
    .map((l) => l.replace(/[ \t]+/g, ' ').trim())
    .join('\n')
    .replace(/\n{2,}/g, '\n')
    .trim();
  return t;
}

/** Does the string contain anything pronounceable (a letter or digit)? */
export function hasSpeakableContent(s) {
  return /[\p{L}\p{N}]/u.test(s);
}

function splitLong(sentence, max) {
  if (sentence.length <= max) return [sentence];
  const out = [];
  let rest = sentence;
  while (rest.length > max) {
    let cut = -1;
    for (const re of [/[,;:—–]\s/g, /\s/g]) {
      let m;
      let last = -1;
      re.lastIndex = 0;
      while ((m = re.exec(rest)) !== null) {
        const end = m.index + m[0].length;
        if (end > max) break;
        last = end;
      }
      if (last > max * 0.4) {
        cut = last;
        break;
      }
    }
    if (cut <= 0) cut = max;
    out.push(rest.slice(0, cut).trim());
    rest = rest.slice(cut).trim();
  }
  if (rest) out.push(rest);
  return out.filter(Boolean);
}

let segmenter;
function sentencesOf(paragraph) {
  if (typeof Intl !== 'undefined' && Intl.Segmenter) {
    segmenter ??= new Intl.Segmenter('en', { granularity: 'sentence' });
    return [...segmenter.segment(paragraph)].map((s) => s.segment.trim()).filter(Boolean);
  }
  return paragraph.match(/[^.!?]+[.!?]+["')\]]*|[^.!?]+$/g)?.map((s) => s.trim()).filter(Boolean) ?? [paragraph];
}

/**
 * Split cleaned text into sentence-sized chunks. Sentences are split first, then very short ones are
 * merged with neighbours (within the same paragraph) up to `maxChars`; overlong ones are split at
 * commas/spaces.
 */
export function splitIntoChunks(text, maxChars = 300) {
  const chunks = [];
  for (const paragraph of text.split('\n').map((p) => p.trim()).filter(Boolean)) {
    let current = '';
    for (const sentence of sentencesOf(paragraph).flatMap((s) => splitLong(s, maxChars))) {
      if (!current) {
        current = sentence;
        continue;
      }
      // Merge tiny neighbours so we don't make a request for "Ha!" on its own.
      const fits = current.length + 1 + sentence.length <= maxChars;
      if (fits && (current.length < 40 || sentence.length < 25)) current += ` ${sentence}`;
      else {
        chunks.push(current);
        current = sentence;
      }
    }
    if (current) chunks.push(current);
  }
  return chunks.filter(hasSpeakableContent);
}

/**
 * Cut `text` to at most `max` chars at a sentence end. If it has no sentence end that fits, returns ''
 * when `allowWordCut` is false, otherwise cuts at a word boundary.
 */
function cutAtBoundary(text, max, allowWordCut) {
  if (text.length <= max) return text;
  const head = text.slice(0, max + 1);
  const end = Math.max(head.lastIndexOf('. '), head.lastIndexOf('! '), head.lastIndexOf('? '));
  if (end > 0) return head.slice(0, end + 1).trim();
  if (!allowWordCut) return '';
  const space = head.lastIndexOf(' ');
  return (space > max * 0.5 ? head.slice(0, space) : head.slice(0, max)).trim();
}

/**
 * Full pipeline: raw GM text -> voiced, speakable chunks.
 *   1. parse [SYSTEM]/[GM]/[ROLL] tags per line (tag stripped, [ROLL] dropped)
 *   2. strip markdown/emoji/code, split into sentence-size chunks (each <= chunkMaxChars)
 *   3. hard-cap the total spoken text at maxMessageChars (cutting at a sentence/word boundary)
 *
 * @param {string | string[]} raw  one text, or several independent sources (message body, embeds…);
 *                                 tag state resets for each source.
 * @returns {{ chunks: { voice: 'gm' | 'system', text: string }[], truncated: boolean }}
 */
export function prepareSpeechDetailed(raw, { chunkMaxChars = 600, maxMessageChars = 1500, defaultVoice = VOICE_GM } = {}) {
  const chunks = [];
  for (const source of Array.isArray(raw) ? raw : [raw]) {
    for (const seg of parseTaggedLines(source, { defaultVoice })) {
      const cleaned = cleanForSpeech(seg.text);
      if (!hasSpeakableContent(cleaned)) continue;
      for (const text of splitIntoChunks(cleaned, Math.min(chunkMaxChars, maxMessageChars))) {
        chunks.push({ voice: seg.voice, text });
      }
    }
  }
  const out = [];
  let used = 0;
  let truncated = false;
  for (const chunk of chunks) {
    const remaining = maxMessageChars - used;
    if (chunk.text.length <= remaining) {
      out.push(chunk);
      used += chunk.text.length;
      continue;
    }
    truncated = true;
    const cut = cutAtBoundary(chunk.text, remaining, out.length === 0);
    if (hasSpeakableContent(cut)) out.push({ voice: chunk.voice, text: cut });
    break;
  }
  return { chunks: out, truncated };
}

/** Convenience wrapper returning just the chunks. */
export function prepareSpeech(raw, opts) {
  return prepareSpeechDetailed(raw, opts).chunks;
}
