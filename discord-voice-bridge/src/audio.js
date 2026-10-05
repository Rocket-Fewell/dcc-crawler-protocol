/** Audio helpers: PCM analysis, downsampling, WAV encoding. All PCM is signed 16-bit little-endian. */

export const DECODE_RATE = 48000; // Discord Opus decode rate
export const STT_RATE = 16000; // what we upload to the STT API
export const DECODE_CHANNELS = 1;

/** Duration in ms of a mono 16-bit PCM buffer at `rate`. */
export function pcmDurationMs(pcm, rate = DECODE_RATE) {
  return (pcm.length / 2 / rate) * 1000;
}

/** Root-mean-square amplitude (0..32767) of a mono 16-bit PCM buffer. */
export function pcmRms(pcm) {
  const n = Math.floor(pcm.length / 2);
  if (n === 0) return 0;
  let sum = 0;
  for (let i = 0; i < n; i++) {
    const s = pcm.readInt16LE(i * 2);
    sum += s * s;
  }
  return Math.sqrt(sum / n);
}

/** Downsample mono 16-bit PCM by an integer factor, averaging each group (cheap low-pass). */
export function downsample(pcm, factor) {
  if (factor === 1) return pcm;
  const n = Math.floor(pcm.length / 2 / factor);
  const out = Buffer.alloc(n * 2);
  for (let i = 0; i < n; i++) {
    let acc = 0;
    for (let j = 0; j < factor; j++) acc += pcm.readInt16LE((i * factor + j) * 2);
    out.writeInt16LE(Math.round(acc / factor), i * 2);
  }
  return out;
}

/** Wrap raw PCM in a RIFF/WAVE header. */
export function pcmToWav(pcm, sampleRate = STT_RATE, channels = 1) {
  const bytesPerSample = 2;
  const header = Buffer.alloc(44);
  header.write('RIFF', 0, 'ascii');
  header.writeUInt32LE(36 + pcm.length, 4);
  header.write('WAVE', 8, 'ascii');
  header.write('fmt ', 12, 'ascii');
  header.writeUInt32LE(16, 16); // PCM fmt chunk size
  header.writeUInt16LE(1, 20); // PCM format
  header.writeUInt16LE(channels, 22);
  header.writeUInt32LE(sampleRate, 24);
  header.writeUInt32LE(sampleRate * channels * bytesPerSample, 28);
  header.writeUInt16LE(channels * bytesPerSample, 32);
  header.writeUInt16LE(bytesPerSample * 8, 34);
  header.write('data', 36, 'ascii');
  header.writeUInt32LE(pcm.length, 40);
  return Buffer.concat([header, pcm]);
}
