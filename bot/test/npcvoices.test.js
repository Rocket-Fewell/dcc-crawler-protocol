import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { NpcVoiceMap, npcVoicesFile } from '../src/npcvoices.js';
import { prepareSpeech } from '../src/text.js';
import { npcKey, parseTaggedLines, stripStrayTags } from '../src/tags.js';
import { FishTts } from '../src/tts.js';

const ID_M = '0123456789abcdef0123456789abcdef';
const ID_B = 'fedcba9876543210fedcba9876543210';
const NARR = 'aa'.repeat(16);
const SYS = 'bb'.repeat(16);
const quiet = { info() {}, warn() {}, debug() {} };

function mapFile(npcs) {
  const dir = mkdtempSync(join(tmpdir(), 'npcv-'));
  const file = join(dir, 'npc-voices.json');
  writeFileSync(file, JSON.stringify({ schema: 'npc-voices/0.1', version: '0.1.0', npcs }));
  return { dir, file };
}

test('tags: [NPC: Name] starts an NPC segment that carries over until the next tag; tag text is not spoken', () => {
  const segs = parseTaggedLines('[GM] The door creaks.\n[NPC: Mordecai] Kid, listen.\nDon\'t touch that.\n[GM] He sighs.\n[SYSTEM] Clock: 10 minutes.');
  assert.deepEqual(segs, [
    { voice: 'gm', text: 'The door creaks.' },
    { voice: 'npc:mordecai', text: "Kid, listen.\nDon't touch that." },
    { voice: 'gm', text: 'He sighs.' },
    { voice: 'system', text: 'Clock: 10 minutes.' },
  ]);
  assert.ok(!segs.some((s) => /\[|NPC/.test(s.text)), 'no tag text reaches TTS');
});

test('tags: NPC names match case-insensitively, ignoring extra spaces and punctuation; markdown-wrapped tags work', () => {
  const v = (raw) => parseTaggedLines(raw)[0].voice;
  assert.equal(v('[NPC:   proctor    BELL ] Welcome!'), 'npc:proctor bell');
  assert.equal(v('[npc:Proctor Bell] Welcome!'), 'npc:proctor bell');
  assert.equal(v('**[NPC: Proctor Bell]** Welcome!'), 'npc:proctor bell');
  assert.equal(v('> [NPC: Snakk-Matic]: Buy now!'), 'npc:snakk matic');
  assert.equal(npcKey('Dean Thudd (JV)'), npcKey('dean  thudd jv'));
  assert.equal(v('[NPC:] Hello'), 'gm', 'an empty NPC name is the narrator');
});

test('tags: the rules-note line fallback to System still applies inside an NPC segment, then the NPC resumes', () => {
  const segs = parseTaggedLines('[NPC: Mordecai] Try it.\nRules note: that needs a DC 12 check.\nGo on then.');
  assert.deepEqual(segs.map((s) => s.voice), ['npc:mordecai', 'system', 'npc:mordecai']);
});

test('tags: a stray [NPC: Name] mid-line is stripped, other brackets are not', () => {
  assert.equal(stripStrayTags('He says [NPC: Mordecai] hi'), 'He says hi');
  assert.equal(stripStrayTags('Roll [1d20] now'), 'Roll [1d20] now');
  assert.equal(stripStrayTags('He said [SYSTEM] out loud.'), 'He said [SYSTEM] out loud.');
  const chunks = prepareSpeech('[NPC: Qwist] Eat, dear! [NPC: Qwist] Eat!');
  assert.deepEqual(chunks.map((c) => c.voice), ['npc:qwist']);
  assert.ok(!/\[|NPC/.test(chunks[0].text), chunks[0].text);
});

test('npc map: name and aliases (case/space-insensitive); no id or bad id = null; missing file = empty', () => {
  const { dir, file } = mapFile([
    { name: 'Mordecai', aliases: ['Mordy'], floors: [1], fish_voice_id: ID_M.toUpperCase(), note: 'guide' },
    { name: 'Laminak Rev-Up Consultant Elite', aliases: ['Laminak Elite'], fish_voice_id: ID_B },
    { name: 'Dale Pruitt', aliases: [], fish_voice_id: null },
    { name: 'Broken', aliases: [], fish_voice_id: 'xyz' },
  ]);
  try {
    const m = new NpcVoiceMap({ file, logger: quiet }).load();
    assert.equal(m.size, 4);
    assert.equal(m.voiceIdFor('MORDY'), ID_M);
    assert.equal(m.voiceIdFor('  mordecai '), ID_M);
    assert.equal(m.voiceIdFor('laminak   elite'), ID_B);
    assert.equal(m.voiceIdFor('Laminak Rev Up Consultant Elite'), ID_B);
    assert.equal(m.voiceIdFor('Dale Pruitt'), null);
    assert.equal(m.voiceIdFor('Broken'), null);
    assert.equal(m.voiceIdFor('Nobody'), null);
    const none = new NpcVoiceMap({ file: join(dir, 'missing.json'), logger: quiet }).load();
    assert.equal(none.size, 0);
    assert.match(none.summary(), /file not found/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('npc map: path comes from the campaign root (or NPC_VOICES_FILE), never a box path', () => {
  assert.equal(npcVoicesFile('/c', {}), join('/c', 'tables', 'npc-voices.json'));
  assert.equal(npcVoicesFile('/c', { NPC_VOICES_FILE: '/x/v.json' }), '/x/v.json');
});

test('npc map: a broken file keeps the last good map; a change is picked up by watch() (no restart)', async () => {
  const { dir, file } = mapFile([{ name: 'Mordecai', fish_voice_id: ID_M }]);
  const m = new NpcVoiceMap({ file, logger: quiet, pollMs: 20 }).load().watch();
  try {
    writeFileSync(file, '{ not json');
    m.load();
    assert.equal(m.voiceIdFor('Mordecai'), ID_M, 'previous map kept');
    writeFileSync(file, JSON.stringify({ npcs: [{ name: 'Mordecai', fish_voice_id: ID_M }, { name: 'Zev', fish_voice_id: ID_B, padding: 'x'.repeat(50) }] }));
    const t0 = Date.now();
    while (m.voiceIdFor('Zev') !== ID_B && Date.now() - t0 < 3000) await new Promise((r) => setTimeout(r, 25));
    assert.equal(m.voiceIdFor('Zev'), ID_B, 'hot-reloaded');
  } finally {
    m.unwatch();
    rmSync(dir, { recursive: true, force: true });
  }
});

function fishWith(npcs, impl) {
  const { dir, file } = mapFile(npcs);
  const warns = [];
  const tts = new FishTts({ apiKey: 'k', voices: { gm: { voiceId: NARR }, system: { voiceId: SYS } }, npcVoices: new NpcVoiceMap({ file, logger: quiet }).load(), logger: { warn: (m) => warns.push(m), info() {}, debug() {} } });
  const calls = [];
  tts._synthesize = async (text, id) => { calls.push(id); return impl ? impl(id) : `audio:${id}`; };
  return { tts, calls, warns, done: () => rmSync(dir, { recursive: true, force: true }) };
}

test('fish: an NPC with a voice id speaks in it; GM/system unchanged', async () => {
  const f = fishWith([{ name: 'Mordecai', aliases: ['Mordy'], fish_voice_id: ID_M }]);
  try {
    assert.equal(await f.tts.synthesize('hi', 'npc:mordy'), `audio:${ID_M}`);
    assert.equal(await f.tts.synthesize('hi', 'gm'), `audio:${NARR}`);
    assert.equal(await f.tts.synthesize('hi', 'system'), `audio:${SYS}`);
  } finally { f.done(); }
});

test('fish: NPC missing from the map, or with no id, uses the narrator voice', async () => {
  const f = fishWith([{ name: 'Dale Pruitt', fish_voice_id: null }]);
  try {
    assert.equal(await f.tts.synthesize('hi', 'npc:dale pruitt'), `audio:${NARR}`);
    assert.equal(await f.tts.synthesize('hi', 'npc:nobody'), `audio:${NARR}`);
    assert.deepEqual(f.calls, [NARR, NARR]);
  } finally { f.done(); }
});

test('fish: a Fish error on an NPC id (deleted/private) falls back to the narrator for that line and logs a warning', async () => {
  const f = fishWith([{ name: 'Mordecai', fish_voice_id: ID_M }], (id) => {
    if (id === ID_M) throw Object.assign(new Error('Fish Audio TTS failed: HTTP 404'), { status: 404 });
    return `audio:${id}`;
  });
  try {
    assert.equal(await f.tts.synthesize('hi', 'npc:mordecai'), `audio:${NARR}`);
    assert.equal(f.warns.length, 1);
    assert.match(f.warns[0], /Mordecai.*404.*narrator/);
    assert.ok(!f.warns[0].includes('k '), 'no key in the warning');
    // the bad id is not retried on the next line for a while (no double billing / latency)
    assert.equal(await f.tts.synthesize('again', 'npc:mordecai'), `audio:${NARR}`);
    assert.deepEqual(f.calls, [ID_M, NARR, NARR]);
  } finally { f.done(); }
});

test('fish: key/credit errors (401/402) on an NPC voice are not hidden by the fallback', async () => {
  const f = fishWith([{ name: 'Mordecai', fish_voice_id: ID_M }], () => { throw Object.assign(new Error('HTTP 402'), { status: 402 }); });
  try {
    await assert.rejects(() => f.tts.synthesize('hi', 'npc:mordecai'), /402/);
  } finally { f.done(); }
});
