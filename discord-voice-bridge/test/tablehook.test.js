import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import http from 'node:http';
import path from 'node:path';
import { test } from 'node:test';
import { loadConfig } from '../src/config.js';
import { prepareSpeechDetailed } from '../src/text.js';
import { loadTableConfig, postLine, routeTranscript, speakable, TableHook } from '../src/tablehook.js';

const SECRET_LINE = 'I shoot the mannequin and the secret phrase xylophone-table';

function capture() {
  const lines = [];
  const mk = (level) => (...args) => lines.push(`${level} ${args.join(' ')}`);
  return { lines, logger: { debug: mk('debug'), info: mk('info'), warn: mk('warn'), error: mk('error') } };
}

const base = {
  DISCORD_TOKEN: 'x.y.z',
  CLIENT_ID: '111111111111111111',
  GUILD_ID: '222222222222222222',
  VOICE_CHANNEL_ID: '333333333333333333',
  TRANSCRIPT_CHANNEL_ID: '444444444444444444',
  GM_OUTPUT_CHANNEL_ID: '555555555555555555',
  OPENAI_API_KEY: 'sk-test',
};

test('table hook is off unless DCC_TABLE_URL is set', () => {
  assert.deepEqual(loadTableConfig({}), { enabled: false, url: '', problems: [] });
  assert.deepEqual(loadTableConfig({ DCC_TABLE_URL: '   ' }), { enabled: false, url: '', problems: [] });
  const c = loadConfig(base);
  assert.equal(c.table.enabled, false);
  assert.equal(c.table.url, '');
});

test('DCC_TABLE_URL accepts only a localhost http(s) origin', () => {
  assert.deepEqual(loadTableConfig({ DCC_TABLE_URL: 'http://127.0.0.1:8765/player?x=1' }), {
    enabled: true, url: 'http://127.0.0.1:8765', problems: [],
  });
  assert.equal(loadTableConfig({ DCC_TABLE_URL: 'https://localhost:9' }).url, 'https://localhost:9');
  assert.equal(loadTableConfig({ DCC_TABLE_URL: 'http://[::1]:8765' }).enabled, true);
  for (const url of [
    'https://example.com/api/line',
    'http://user:pass@127.0.0.1:8765',
    'ftp://127.0.0.1:8765',
    'http://127.0.0.1.evil.test',
    'not a url',
  ]) {
    const t = loadTableConfig({ DCC_TABLE_URL: url });
    assert.equal(t.enabled, false, url);
    assert.equal(t.url, '', url);
    assert.ok(t.problems.length === 1, url);
    assert.throws(() => loadConfig({ ...base, DCC_TABLE_URL: url }), /DCC_TABLE_URL/);
  }
});

test('speakable keeps SYSTEM and GM and drops rolls', () => {
  const say = [
    { voice: 'SYSTEM', speak: true, text: '[SYSTEM] Action spent.' },
    { voice: 'ROLL', speak: false, text: '[ROLL] to hit: 1d20+6 -> 18' },
    { voice: 'ROLL', speak: true, text: '[ROLL] this must stay unspoken' },
    { voice: 'GM', speak: true, text: '[GM] Your shot hits.' },
    { voice: 'GM', speak: false, text: '[GM] hidden' },
    { voice: 'NPC', speak: true, text: '[NPC: Proctor Bell] The shutter is the way out.' },
    { voice: 'SYSTEM', speak: true, text: '   ' },
  ];
  const kept = speakable(say);
  assert.deepEqual(kept.map((l) => l.voice), ['SYSTEM', 'GM', 'NPC']);
  const { chunks } = prepareSpeechDetailed(kept.map((l) => l.text).join('\n'));
  assert.ok(chunks.some((c) => c.voice === 'system'));
  assert.ok(chunks.some((c) => c.voice === 'gm'));
  assert.equal(chunks.some((c) => c.text.includes('unspoken') || c.text.includes('1d20')), false);
});

test('a transcript goes to the table, and the wake webhook is not called', async () => {
  const seen = [];
  let inflight = 0;
  let max = 0;
  let release;
  const gate = new Promise((r) => { release = r; });
  const fetchImpl = async (_url, opts) => {
    inflight += 1;
    max = Math.max(max, inflight);
    seen.push(JSON.parse(opts.body));
    await gate;
    inflight -= 1;
    return {
      status: 200,
      async json() {
        return {
          say: [
            { voice: 'SYSTEM', speak: true, text: '[SYSTEM] Action spent.' },
            { voice: 'ROLL', speak: false, text: '[ROLL] to hit: 1d20+6 -> 18' },
            { voice: 'GM', speak: true, text: '[GM] Your shot hits.' },
          ],
        };
      },
    };
  };
  const said = [];
  const { logger, lines } = capture();
  const tableHook = new TableHook({
    table: loadTableConfig({ DCC_TABLE_URL: 'http://127.0.0.1:8765' }),
    logger,
    fetchImpl,
    onSay: (spoken) => said.push(spoken),
  });
  const wake = { notify() { throw new Error('wake must not run'); } };
  const first = routeTranscript({ speaker: 'Raithen', text: SECRET_LINE }, { tableHook, wake });
  const second = tableHook.notify('I end my turn');
  assert.equal(max, 1);
  release();
  await first;
  await second;
  assert.equal(seen.length, 2);
  assert.deepEqual(seen[0], { text: SECRET_LINE });
  assert.equal(said.length, 2);
  assert.deepEqual(said[0].map((l) => l.voice), ['SYSTEM', 'GM']);
  assert.equal(lines.join('\n').includes(SECRET_LINE), false);
  assert.equal(lines.join('\n').includes('xylophone'), false);
  assert.match(lines.join('\n'), /HTTP 200 \(2 spoken\)/);
});

test('a table error does not throw, does not speak, and does not log the line', async () => {
  const { logger, lines } = capture();
  const said = [];
  const hook = new TableHook({
    table: { enabled: true, url: 'http://127.0.0.1:9' },
    logger,
    onSay: (spoken) => said.push(spoken),
    fetchImpl: async () => ({ status: 500, body: { cancel: async () => {} } }),
  });
  await hook.notify({ text: SECRET_LINE });
  const refused = Object.assign(new Error(`down ${SECRET_LINE}`), { code: 'ECONNREFUSED' });
  hook.fetchImpl = async () => { throw refused; };
  await hook.notify(SECRET_LINE);
  assert.equal(said.length, 0);
  const log = lines.join('\n');
  assert.match(log, /HTTP 500/);
  assert.match(log, /ECONNREFUSED/);
  assert.equal(log.includes(SECRET_LINE), false);
  assert.equal(log.includes('xylophone'), false);
});

test('routeTranscript uses the wake webhook when the table hook is off', () => {
  const woke = [];
  routeTranscript({ text: 'hello' }, {
    tableHook: { enabled: false, notify() { throw new Error('table must not run'); } },
    wake: { notify: (line) => woke.push(line) },
  });
  assert.equal(woke.length, 1);
});

test('a real gallery line posts to /api/line and the roll is not spoken', async () => {
  const repo = path.resolve(import.meta.dirname, '../..');
  const child = spawn('python3', ['engine/serve.py', '--port', '0'], {
    cwd: repo,
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  const stop = () => new Promise((resolve) => {
    if (child.exitCode !== null) return resolve();
    const timer = setTimeout(() => {
      try { child.kill('SIGKILL'); } catch { /* already gone */ }
      resolve();
    }, 2000);
    child.once('exit', () => {
      clearTimeout(timer);
      resolve();
    });
    try { child.kill('SIGTERM'); } catch { /* already gone */ }
  });
  let out = '';
  let origin;
  try {
    origin = await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('table did not print a url')), 15000);
      const take = (buf) => {
        out += buf.toString();
        const m = out.match(/http:\/\/127\.0\.0\.1:(\d+)/);
        if (!m) return;
        clearTimeout(timer);
        resolve(`http://127.0.0.1:${m[1]}`);
      };
      child.stdout.on('data', take);
      child.stderr.on('data', take);
      child.once('exit', (code) => {
        clearTimeout(timer);
        reject(new Error(`table exited ${code} before a url`));
      });
    });
    const raw = await postLine(origin, 'I shoot the mannequin');
    assert.equal(raw.ok, true);
    assert.ok(raw.say.some((s) => s.voice === 'ROLL' && s.speak === false));
    assert.ok(raw.say.some((s) => s.voice === 'SYSTEM' && s.text.startsWith('[SYSTEM]')));
    const spoken = speakable(raw.say);
    assert.ok(spoken.length >= 1);
    assert.ok(spoken.every((s) => s.speak === true && (s.voice === 'SYSTEM' || s.voice === 'GM' || s.voice === 'NPC')));
    const { chunks } = prepareSpeechDetailed([...spoken.map((s) => s.text), '[ROLL] to hit stays on the page'].join('\n'));
    assert.equal(chunks.some((c) => c.text.includes('stays on the page')), false);
    const { logger, lines } = capture();
    const said = [];
    const hook = new TableHook({
      table: loadTableConfig({ DCC_TABLE_URL: origin }),
      logger,
      onSay: (linesOut) => said.push(linesOut),
    });
    await hook.notify({ speaker: 'Raithen', text: SECRET_LINE });
    assert.equal(said.length, 1);
    assert.ok(said[0].every((s) => s.voice === 'SYSTEM' || s.voice === 'GM' || s.voice === 'NPC'));
    assert.equal(lines.join('\n').includes('xylophone'), false);
  } finally {
    await stop();
  }
});

test('redirects are not followed', async () => {
  const srv = http.createServer((_req, res) => {
    res.writeHead(302, { Location: 'http://127.0.0.1:1/nope' });
    res.end();
  });
  await new Promise((r) => srv.listen(0, '127.0.0.1', r));
  try {
    const port = srv.address().port;
    const result = await postLine(`http://127.0.0.1:${port}`, 'hello');
    assert.equal(result.ok, false);
    assert.equal(result.status, 302);
    assert.deepEqual(result.say, []);
  } finally {
    srv.closeAllConnections?.();
    await new Promise((r) => srv.close(r));
  }
});
