import assert from 'node:assert/strict';
import { test } from 'node:test';
import { downsample, pcmDurationMs, pcmRms, pcmToWav } from '../src/audio.js';

function pcmOf(samples) {
  const b = Buffer.alloc(samples.length * 2);
  samples.forEach((s, i) => b.writeInt16LE(s, i * 2));
  return b;
}

test('pcmToWav writes a valid header', () => {
  const pcm = pcmOf([0, 1000, -1000, 2000]);
  const wav = pcmToWav(pcm, 16000, 1);
  assert.equal(wav.toString('ascii', 0, 4), 'RIFF');
  assert.equal(wav.toString('ascii', 8, 12), 'WAVE');
  assert.equal(wav.readUInt32LE(4), 36 + pcm.length);
  assert.equal(wav.readUInt16LE(22), 1);
  assert.equal(wav.readUInt32LE(24), 16000);
  assert.equal(wav.readUInt32LE(40), pcm.length);
  assert.equal(wav.length, 44 + pcm.length);
});

test('pcmRms / duration / downsample', () => {
  assert.equal(pcmRms(Buffer.alloc(0)), 0);
  assert.equal(Math.round(pcmRms(pcmOf([100, -100, 100, -100]))), 100);
  assert.equal(pcmDurationMs(Buffer.alloc(48000 * 2), 48000), 1000);
  const ds = downsample(pcmOf([3, 6, 9, 12, 15, 18]), 3);
  assert.equal(ds.length, 4);
  assert.equal(ds.readInt16LE(0), 6);
  assert.equal(ds.readInt16LE(2), 15);
});
