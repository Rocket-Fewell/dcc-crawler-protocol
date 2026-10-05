#!/usr/bin/env node
// Sums TTS usage (logs/tts-usage.jsonl) per day, month and bot session, and checks the monthly minutes cap.
//
//   node scripts/tts-usage-summary.js [--file PATH] [--month YYYY-MM] [--provider fish|openai|elevenlabs]
//                                     [--session ID]   (only this campaign session: alpha, beta, ...; default = all, with a per-session table)
//                                     [--no-balance]   (skip the live Fish balance request)
//                                     [--wake-file PATH] [--events-file PATH] [--cap MINUTES] [--cap-provider fish|all] [--json] [--csv] [--fail-on-warn]
//
// Fish bills prepaid credit at $15 per 1M UTF-8 bytes: the "bytes USD" columns are utf8_bytes x $15/1M per day and per bot session (bytes are logged per synthesized
// message, never the text). The live balance comes from GET https://api.fish.audio/wallet/self/api-credit (needs FISH_API_KEY, never printed).
// Also reports GM wake-ups per day and per bot session from logs/wake-usage.jsonl ($WAKE_USAGE_LOG).
// Cap defaults to $FISH_MONTHLY_CAP_MINUTES (else 200). Warns at >= 80%. Exit codes: 0 ok, 1 error,
// 3 when --fail-on-warn and usage >= 80% of the cap.
import 'dotenv/config';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { postsUsed } from '../src/wakebudget.js';
import { fetchFishBalance } from '../src/fishbalance.js';
import { listSessions, readProfile } from '../src/session.js';
import { parseArgs } from 'node:util';
import {
  DEFAULT_CHARS_PER_MINUTE,
  DEFAULT_MONTHLY_CAP_MINUTES,
  WARN_PERCENT,
  parseJsonl,
  parseEventsJsonl,
  parseWakeJsonl,
  summarize,
  summarizeVoiceEvents,
  summarizeWakes,
  dccSessionOf,
} from '../src/usage.js';

const ROOT = fileURLToPath(new URL('..', import.meta.url));

function fmt(n, d = 2) {
  return Number(n).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
}
function int(n) {
  return Number(n).toLocaleString('en-US');
}

function table(title, headers, rows) {
  if (!rows.length) return `${title}\n  (none)\n`;
  const widths = headers.map((h, i) => Math.max(h.length, ...rows.map((r) => String(r[i]).length)));
  const line = (cells) => '  ' + cells.map((c, i) => (i < 2 ? String(c).padEnd(widths[i]) : String(c).padStart(widths[i]))).join('  ');
  return [title, line(headers), line(widths.map((w) => '-'.repeat(w))), ...rows.map(line), ''].join('\n');
}

function render(s) {
  const out = [];
  const cols = ['calls', 'chars', 'utf8 bytes', 'minutes', 'bytes USD'];
  const tail = (r) => [int(r.records), int(r.chars), int(r.utf8_bytes), fmt(r.minutes), fmt(r.est_cost_usd, 4)];
  out.push(table('By day', ['date', 'provider', ...cols], s.by_day.map((r) => [r.date, r.provider, ...tail(r)])));
  out.push(table('By month', ['month', 'provider', ...cols], s.by_month.map((r) => [r.month, r.provider, ...tail(r)])));
  out.push(table('By bot session (grouped by date)', ['session', 'date', 'provider', ...cols],
    s.by_session.map((r) => [r.session, r.date, r.provider, ...tail(r)])));
  out.push(table('By campaign session (this month, Fish minutes vs share of the shared cap)', ['session', 'used min', 'share', 'left', '%'],
    (s.by_campaign ?? []).map((r) => [r.dcc_session, fmt(r.used_minutes), r.share_minutes > 0 ? fmt(r.share_minutes, 0) : 'none', r.remaining_minutes === null ? '-' : fmt(r.remaining_minutes), r.percent === null ? '-' : fmt(r.percent, 1) + (r.over ? ' OVER' : '')])));
  out.push(table('By voice', ['provider', 'voice', ...cols], s.by_voice.map((r) => [r.provider, r.voice, ...tail(r)])));
  const t = s.total;
  out.push(`Total: ${int(t.records)} calls, ${int(t.chars)} chars, ${int(t.utf8_bytes)} UTF-8 bytes, ${fmt(t.minutes)} min, est. $${fmt(t.est_cost_usd, 4)}`
    + (s.failed_excluded ? `  (${s.failed_excluded} failed call(s) excluded)` : ''));
  const c = s.cap;
  out.push('');
  out.push(`Monthly cap (${c.month}, ${c.provider === 'all' ? 'all providers' : c.provider}): ${fmt(c.used_minutes)} / ${fmt(c.cap_minutes, 0)} min`
    + ` = ${c.percent === null ? 'n/a' : fmt(c.percent, 1) + '%'} used, ${fmt(c.remaining_minutes)} min remaining`);
  if (c.over) out.push(`!! OVER CAP: usage is at or above 100% of the monthly cap.`);
  else if (c.warn) out.push(`WARNING: usage is at or above ${WARN_PERCENT}% of the monthly cap.`);
  return out.join('\n');
}

function renderWakes(w, wakeRecords = [], maxPerHour = 0) {
  const hourAgo = Date.now() - 3_600_000;
  const lastHour = wakeRecords.filter((r) => Date.parse(r.ts) > hourAgo).reduce((n, r) => n + postsUsed(r), 0);
  const budgetLine = `Last 60 min: ${int(lastHour)} wake POST(s) ${maxPerHour > 0 ? `of a budget of ${int(maxPerHour)} (WAKE_MAX_PER_HOUR; ${int(Math.max(0, maxPerHour - lastHour))} left)` : '(no hourly budget: WAKE_MAX_PER_HOUR=0)'}. ${int(w.total.rate_limited)} rate-limited rejection(s) in the report period; ${int(w.total.budget_held)} line(s) were held by the budget.`;
  const cols = ['wakes', 'failed', 'rate-lim', 'lines', 'skipped', 'paused', 'held', 'AI-word', 'saved<='];
  const tail = (r) => [int(r.wakes), int(r.failed), int(r.rate_limited), int(r.lines), int(r.skipped), int(r.paused), int(r.budget_held), int(r.overrides), int(r.saved_upper_bound)];
  const t = w.total;
  return [
    table('GM wake-ups by day', ['date', ...cols], w.by_day.map((r) => [r.date, ...tail(r)])),
    table('GM wake-ups by bot session (grouped by date)', ['session', 'date', ...cols], w.by_session.map((r) => [r.session, r.date, ...tail(r)])),
    `Total: ${int(t.wakes)} wake(s) fired (${int(t.failed)} failed) for ${int(t.lines)} transcript line(s); ` +
      `${int(t.skipped)} line(s) skipped by the spotlight filter; ${int(t.paused)} line(s) dropped while /gm pause was on; ${int(t.overrides)} wake-word ("AI") override line(s).`,
    `Estimated wake-ups saved: <= ${int(t.saved_upper_bound)} (UPPER BOUND: each skipped/paused line could have cost up to one wake, ` +
      `but batching would have merged some of them).`,
    budgetLine,
    '  Columns: skipped = lines the spotlight filter kept from waking the GM; paused = lines dropped by /gm pause; rate-lim = wakes the server rejected as rate-limited (lines kept and retried); held = lines held by the rolling-hour budget (sent later, NOT savings); AI-word = lines that woke the GM by saying "AI" while',
    '  someone else was in the spotlight; saved<= = skipped + paused lines (upper bound).',
  ].join('\n');
}

function renderEvents(e) {
  const cols = ['dupes', 'backlog drops', 'msgs dropped', 'chunks dropped', 'flushes'];
  const tail = (r) => [int(r.duplicates), int(r.backlog_events), int(r.backlog_messages), int(r.backlog_chunks), int(r.flushes)];
  const t = e.total;
  return [
    table('Voice protections by day', ['date', ...cols], e.by_day.map((r) => [r.date, ...tail(r)])),
    table('Voice protections by bot session (grouped by date)', ['session', 'date', ...cols], e.by_session.map((r) => [r.session, r.date, ...tail(r)])),
    `Total: ${int(t.duplicates)} duplicate GM message(s) dropped (never synthesized); ${int(t.backlog_events)} backlog trim(s) dropping ${int(t.backlog_messages)} message(s) / ${int(t.backlog_chunks)} chunk(s); ${int(t.flushes)} flush(es) (/shush or the stop kill switch).`,
  ].join('\n');
}

function toCsv(s, w, e) {
  // wake_* rows reuse the columns: calls=wakes, chars=lines, utf8_bytes=skipped, minutes=wake-word overrides, est_cost_usd=saved upper bound
  const rows = [['scope', 'key', 'provider', 'calls', 'chars', 'utf8_bytes', 'minutes', 'est_cost_usd']];
  for (const r of s.by_day) rows.push(['day', r.date, r.provider, r.records, r.chars, r.utf8_bytes, r.minutes, r.est_cost_usd]);
  for (const r of s.by_month) rows.push(['month', r.month, r.provider, r.records, r.chars, r.utf8_bytes, r.minutes, r.est_cost_usd]);
  for (const r of s.by_session) rows.push(['session', `${r.session} (${r.date})`, r.provider, r.records, r.chars, r.utf8_bytes, r.minutes, r.est_cost_usd]);
  for (const r of w.by_day) rows.push(['wake_day', r.date, 'wake', r.wakes, r.lines, r.skipped, r.overrides, r.saved_upper_bound]);
  for (const r of w.by_session) rows.push(['wake_session', `${r.session} (${r.date})`, 'wake', r.wakes, r.lines, r.skipped, r.overrides, r.saved_upper_bound]);
  // voice_* rows: calls=duplicates dropped, chars=backlog messages dropped, utf8_bytes=backlog chunks dropped, minutes=flushes
  for (const r of e.by_day) rows.push(['voice_day', r.date, 'voice', r.duplicates, r.backlog_messages, r.backlog_chunks, r.flushes, '']);
  return rows.map((r) => r.join(',')).join('\n');
}

export async function balanceLine(env = process.env, fetchImpl = fetch) {
  if (!env.FISH_API_KEY) return { ok: false, line: 'Fish balance: n/a (FISH_API_KEY not set)' };
  try {
    const credit = await fetchFishBalance({ apiKey: env.FISH_API_KEY, baseUrl: env.FISH_BASE_URL || 'https://api.fish.audio', fetchImpl });
    return { ok: true, credit, line: `Fish balance (live): $${fmt(credit, 2)} prepaid credit` };
  } catch (err) {
    return { ok: false, line: `Fish balance: unavailable (${err.message})` };
  }
}

async function main() {
  let values;
  try {
    ({ values } = parseArgs({
      options: {
        file: { type: 'string' },
        'wake-file': { type: 'string' },
        'events-file': { type: 'string' },
        month: { type: 'string' },
        session: { type: 'string' },
        provider: { type: 'string' },
        cap: { type: 'string' },
        'cap-provider': { type: 'string' },
        'chars-per-minute': { type: 'string' },
        'no-balance': { type: 'boolean', default: false },
        json: { type: 'boolean', default: false },
        csv: { type: 'boolean', default: false },
        'fail-on-warn': { type: 'boolean', default: false },
        help: { type: 'boolean', short: 'h', default: false },
      },
    }));
  } catch (err) {
    console.error(`${err.message}\nTry --help`);
    return 1;
  }
  if (values.help) {
    console.log(readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n').filter((l) => l.startsWith('//')).map((l) => l.slice(3)).join('\n'));
    return 0;
  }
  if (values.month && !/^\d{4}-\d{2}$/.test(values.month)) {
    console.error('--month must look like 2026-10');
    return 1;
  }
  const cap = Number(values.cap ?? process.env.FISH_MONTHLY_CAP_MINUTES ?? DEFAULT_MONTHLY_CAP_MINUTES);
  if (!Number.isFinite(cap) || cap < 0) {
    console.error('cap must be a non-negative number of minutes');
    return 1;
  }
  const file = values.file ?? process.env.TTS_USAGE_LOG ?? `${ROOT}logs/tts-usage.jsonl`;
  let text;
  try {
    text = readFileSync(file, 'utf8');
  } catch (err) {
    if (err.code === 'ENOENT') text = ''; // no usage yet
    else {
      console.error(`Cannot read ${file}: ${err.message}`);
      return 1;
    }
  }
  const parsed = parseJsonl(text);
  const bad = parsed.bad;
  const dccSession = values.session ? values.session.trim().toLowerCase() : undefined;
  const records = parsed.records;
  const wakeFile = values['wake-file'] ?? process.env.WAKE_USAGE_LOG ?? `${ROOT}logs/wake-usage.jsonl`;
  let wakeText = '';
  try {
    wakeText = readFileSync(wakeFile, 'utf8');
  } catch (err) {
    if (err.code !== 'ENOENT') {
      console.error(`Cannot read ${wakeFile}: ${err.message}`);
      return 1;
    }
  }
  const { records: wakeRecords, bad: wakeBad } = parseWakeJsonl(wakeText);
  const w = summarizeWakes(wakeRecords, { month: values.month, dccSession });
  const eventsFile = values['events-file'] ?? process.env.VOICE_EVENTS_LOG ?? `${ROOT}logs/voice-events.jsonl`;
  let eventsText = '';
  try {
    eventsText = readFileSync(eventsFile, 'utf8');
  } catch (err) {
    if (err.code !== 'ENOENT') {
      console.error(`Cannot read ${eventsFile}: ${err.message}`);
      return 1;
    }
  }
  const { records: eventRecords, bad: eventsBad } = parseEventsJsonl(eventsText);
  const e = summarizeVoiceEvents(dccSession ? eventRecords.filter((r) => dccSessionOf(r) === dccSession) : eventRecords, { month: values.month });
  // Each campaign session's share of the monthly cap: env default 100 min, overridden by <data>/session.json fish_monthly_minutes.
  const defaultShare = Number(process.env.FISH_SESSION_MONTHLY_MINUTES ?? 100);
  const shares = Object.fromEntries(listSessions().map((id) => [id, Number(readProfile(id).fish_monthly_minutes ?? defaultShare)]));
  const s = summarize(records, {
    dccSession,
    shares,
    defaultShare,
    month: values.month,
    provider: values.provider,
    cap,
    capProvider: values['cap-provider'] ?? 'fish',
    charsPerMinute: Number(values['chars-per-minute'] ?? process.env.TTS_USAGE_CHARS_PER_MINUTE ?? DEFAULT_CHARS_PER_MINUTE),
  });
  const bal = values['no-balance'] ? null : await balanceLine();
  if (values.json) console.log(JSON.stringify({ file, malformed_lines: bad, ...s, fish_balance_usd: bal?.ok ? bal.credit : null, wakes: { file: wakeFile, malformed_lines: wakeBad, ...w }, voice_events: { file: eventsFile, malformed_lines: eventsBad, ...e } }, null, 2));
  else if (values.csv) console.log(toCsv(s, w, e));
  else {
    console.log(`TTS usage from ${file}: ${records.length} record(s)${bad ? `, ${bad} malformed line(s) skipped` : ''}\n`);
    console.log(render(s));
    console.log(`Fish bills $15 per 1M UTF-8 bytes: Fish calls in this report cost $${fmt(s.total.est_cost_usd, 4)} (the bytes USD columns above, per day and per bot session; other providers and free-model calls count 0).`);
    if (bal) console.log(bal.line);
    console.log(`\nGM wake log ${wakeFile}: ${wakeRecords.length} record(s) (wakes + skipped lines)${wakeBad ? `, ${wakeBad} malformed line(s) skipped` : ''}\n`);
    console.log(renderWakes(w, dccSession ? wakeRecords.filter((r) => dccSessionOf(r) === dccSession) : wakeRecords, Number(process.env.WAKE_MAX_PER_HOUR ?? 60)));
    console.log(`\nVoice events log ${eventsFile}: ${eventRecords.length} record(s)${eventsBad ? `, ${eventsBad} malformed line(s) skipped` : ''}\n`);
    console.log(renderEvents(e));
  }
  return values['fail-on-warn'] && s.cap.warn ? 3 : 0;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) process.exitCode = await main();
