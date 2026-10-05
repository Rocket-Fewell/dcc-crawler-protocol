import assert from 'node:assert/strict';
import { test } from 'node:test';
import { cleanForSpeech, isHallucination, prepareSpeech, splitIntoChunks } from '../src/text.js';

test('isHallucination filters known junk and keeps real speech', () => {
  for (const s of ['', '  ', '.', 'Thanks for watching!', 'Thank you.', 'you', 'Subtitles by the Amara.org community', '[BLANK_AUDIO]', '(music)', 'you you you you you you', '♪ la la ♪']) {
    assert.equal(isHallucination(s), true, `should filter: ${JSON.stringify(s)}`);
  }
  for (const s of ['I attack the goblin with my sword', 'Donut, get behind me!', 'Yes', 'Okay, I roll a nineteen.']) {
    assert.equal(isHallucination(s), false, `should keep: ${JSON.stringify(s)}`);
  }
});

test('cleanForSpeech strips markdown, code, links, emoji', () => {
  const raw = [
    '# The Crawl Begins 🎉',
    'You see **a very scary** goblin with __underlined__ ~~struck~~ _italic_ text.',
    '```js',
    'console.log("code");',
    '```',
    '- bullet one',
    '1. numbered one',
    '> quoted words',
    'Visit [the wiki](https://example.com/x) or https://example.com/raw now <:custom:123456789012345678> 😀👍🏽',
    '||spoiler|| and `inline code`.',
  ].join('\n');
  const out = cleanForSpeech(raw);
  assert.ok(!/[*_~`#>|]/.test(out), out);
  assert.ok(!/console|http|\p{Extended_Pictographic}/u.test(out), out);
  assert.match(out, /The Crawl Begins/);
  assert.match(out, /a very scary goblin/);
  assert.match(out, /the wiki/);
  assert.match(out, /bullet one/);
  assert.match(out, /spoiler and inline code/);
});

test('splitIntoChunks makes sentence-size chunks and respects max length', () => {
  const text = 'You enter the room. It is dark. A long corridor stretches ahead of you, and the walls drip with something unpleasant that you would rather not identify. "Welcome, crawler!" says the voice.';
  const chunks = splitIntoChunks(text, 120);
  assert.ok(chunks.length >= 2);
  for (const c of chunks) assert.ok(c.length <= 120, `too long: ${c.length}`);
  assert.equal(chunks.join(' ').replace(/\s+/g, ' '), text);
});

test('splitIntoChunks splits an overlong sentence without losing words', () => {
  const text = Array.from({ length: 80 }, (_, i) => `word${i}`).join(' ') + '.';
  const chunks = splitIntoChunks(text, 100);
  for (const c of chunks) assert.ok(c.length <= 100);
  assert.equal(chunks.join(' '), text);
});

test('prepareSpeech returns [] for non-speakable content', () => {
  assert.deepEqual(prepareSpeech('```only code```'), []);
  assert.deepEqual(prepareSpeech('🎲🎲🎲'), []);
  assert.deepEqual(prepareSpeech('  '), []);
  assert.equal(prepareSpeech('Hello there. General Kenobi.').length >= 1, true);
});
