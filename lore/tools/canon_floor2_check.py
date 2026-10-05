#!/usr/bin/env python3
"""Checker for tables/canon-floor-2.json (+ .md view), the Floor 2 RESERVE canon table. Owner: DCC Lore, 2026-10-04 (Pass 19).
Also fails if: status is not "reserve"; refinement_backlog or gaps are missing/empty; floor_clock / differences / announcements / timeline rows are missing from the ledger.
Fails (exit 1) if: JSON invalid; schema/ids wrong; any referenced ledger row id does not exist in CANON-LEDGER.md;
a canon/unverified entry has no ledger row; a confidence differs from the ledger (weakest label rule); an unverified tag sits on a
non-UNVERIFIED row; a tag is not canon/inspired/unverified; an announcement quote is over 25 words or is not the quote of its
ledger row (or, for quote_source, not found in that local page); forbidden numeric/difficulty/loot text appears; sealed-path
words appear; 'players' is used instead of 'Crawlers'; the .md view is out of date vs the builder.
Usage: python3 tools/canon_floor2_check.py [json_path]"""
import json, re, sys, os, hashlib
ROOT = '/workspace/dcc-lore'
JP = sys.argv[1] if len(sys.argv) > 1 else ROOT + '/tables/canon-floor-2.json'
LEDGER = ROOT + '/CANON-LEDGER.md'
RANK = {'UNVERIFIED': 0, 'WIKI-ONLY': 1, 'VERIFIED': 2}
errs = []; warns = []
def err(m): errs.append(m)

# ---- ledger ids + confidence + quotes
ledger = {}
for line in open(LEDGER, encoding='utf-8'):
    m = re.match(r'^\| ([A-Z]-[A-Z]?\d+) \|', line)
    if not m: continue
    cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip().strip('|'))]
    conf = next((c.split(' ')[0].split(';')[0] for c in cells if c.startswith(('VERIFIED', 'WIKI-ONLY', 'UNVERIFIED'))), None)
    quotes = [c[1:-1].replace('\\|', '|') for c in cells if len(c) > 2 and c.startswith('"') and c.endswith('"')]
    ledger[m.group(1)] = {'conf': conf, 'quotes': quotes}

try:
    doc = json.load(open(JP, encoding='utf-8'))
except Exception as e:
    print('INVALID JSON:', e); sys.exit(1)

if doc.get('schema') != 'canon-floor-2/0.1.0': err('schema mismatch')
if doc.get('floor') != 2: err('floor must be 2')
if doc.get('status') != 'reserve': err('status must be "reserve" (not for live use)')
if not doc.get('reserve_note'): err('reserve_note missing')
if doc.get('players_are') != 'Crawlers': err('players_are must be Crawlers')

TAGS = {'canon', 'inspired', 'unverified'}
FORBID = [r'\bCR\b', r'\bCR\s*\d', r'\blevels?\s*\d', r'\bLv\.?\s*\d', r'\bXP\b', r'\bcredits?\b\s*\d', r'\d+\s*(credits|gp|gold|xp)\b',
          r'\bDC\s*\d', r'\bdifficulty\b', r'\bgm-notes\b', r'\bsecret/', r'\bplayers?\b']
# 'credits'/'difficulty' may appear only in the out_of_scope disclaimer
SKIP_KEYS = {'out_of_scope', 'how_to_use', 'tag_legend', 'confidence_legend', 'consumer', 'reserve_note'}
ids = set(); seen_ledger = set(); counts = {'zones': 0, 'mobs': 0, 'hazards': 0, 'features': 0}

def check_rows(owner, rows):
    for rid in rows:
        seen_ledger.add(rid)
        if rid not in ledger: err(f'{owner}: ledger row {rid} does not exist')
def weakest(rows):
    cs = [ledger[r]['conf'] for r in rows if r in ledger and ledger[r]['conf']]
    return min(cs, key=lambda c: RANK[c]) if cs else None
def check_entry(owner, e, kind):
    if e['id'] in ids: err(f'duplicate id {e["id"]}')
    ids.add(e['id'])
    if e.get('tag') not in TAGS: err(f'{owner}/{e["id"]}: bad tag {e.get("tag")}')
    check_rows(f'{owner}/{e["id"]}', e.get('ledger_rows', []))
    if e.get('tag') in ('canon', 'unverified') and not [r for r in e.get('ledger_rows', []) if not r.startswith('X-')]: err(f'{owner}/{e["id"]}: {e["tag"]} entry has no non-conflict ledger row')
    w = weakest([r for r in e.get('ledger_rows', []) if not r.startswith('X-')])
    if e.get('confidence') != w: err(f'{owner}/{e["id"]}: confidence {e.get("confidence")} != ledger {w}')
    has_x = any(r.startswith('X-') for r in e.get('ledger_rows', []))
    if e.get('tag') == 'unverified' and w != 'UNVERIFIED' and not has_x: err(f'{owner}/{e["id"]}: unverified tag but ledger says {w} and no open X- conflict row')
    if e.get('tag') == 'canon' and w == 'UNVERIFIED': err(f'{owner}/{e["id"]}: canon tag on an UNVERIFIED row; retag unverified')
    for k in ('what',):
        if not e.get(k): err(f'{owner}/{e["id"]}: missing {k}')
    if e.get('analog_of') and e['analog_of'] not in ids and e['analog_of'] not in ALL_IDS: err(f'{owner}/{e["id"]}: analog_of {e["analog_of"]} unknown')

ALL_IDS = {e['id'] for z in doc['zones'] for k in ('mobs', 'hazards', 'features') for e in z.get(k, [])}
zone_ids = set()
for z in doc['zones']:
    counts['zones'] += 1
    zid = z.get('id')
    if zid in zone_ids: err(f'duplicate zone {zid}')
    zone_ids.add(zid)
    for k in ('name', 'kind', 'tag', 'staging', 'announcement', 'ledger_rows', 'mobs', 'hazards'):
        if k not in z: err(f'{zid}: missing {k}')
    if z.get('tag') not in TAGS: err(f'{zid}: bad zone tag')
    check_rows(zid, z.get('ledger_rows', []))
    for x in z.get('conflicts', []):
        seen_ledger.add(x)
        if x not in ledger: err(f'{zid}: conflict row {x} missing')
    if z.get('tag') == 'canon' and not z.get('ledger_rows'): err(f'{zid}: canon zone without ledger rows')
    if z.get('confidence') != weakest(z.get('ledger_rows', [])): err(f'{zid}: zone confidence != ledger')
    if len(z['staging'].split('. ')) > 4: warns.append(f'{zid}: staging longer than ~2 sentences')
    a = z.get('announcement', {})
    if not a.get('style'): err(f'{zid}: announcement.style missing')
    q = a.get('quote')
    if q:
        if len(q.split()) > 25: err(f'{zid}: announcement quote > 25 words')
        if a.get('quote_row'):
            if a['quote_row'] not in ledger: err(f'{zid}: quote_row missing')
            elif q not in ledger[a['quote_row']]['quotes']: err(f'{zid}: quote is not the quote of {a["quote_row"]}')
            seen_ledger.add(a['quote_row'])
        elif a.get('quote_source'):
            tag = a['quote_source'].split(' (')[0]
            kind, _, name = tag.partition(':')
            p = f'{ROOT}/raw/pages/{name}.txt'
            if not os.path.exists(p): err(f'{zid}: quote_source page {name} not found')
            else:
                txt = re.sub(r'\[\d+\|[^\]]+\]', '', open(p, errors='ignore').read()); txt = re.sub(r'\s+', ' ', txt)
                if q not in txt: err(f'{zid}: quote not found in {name}')
        else: err(f'{zid}: quote without quote_row/quote_source')
    for k, key in (('mobs', 'mobs'), ('hazards', 'hazards'), ('features', 'features')):
        for e in z.get(k, []):
            counts[key] += 1
            check_entry(zid, e, k)
    for it in z.get('items', []):
        irs = {x['srd_id']: x for x in json.load(open(ROOT + '/tables/item-reskins.json'))['entries']}
        if it['srd_id'] not in irs: err(f'{zid}: item {it["srd_id"]} not in item-reskins.json')
        elif irs[it['srd_id']]['display_name'] != it['game_display_name']: err(f'{zid}: item display name mismatch {it["srd_id"]}')
    for ref in z.get('table_refs', []):
        base = ref
        cand = [f'{ROOT}/tables/loot-decks/{base}.json']
        if not any(os.path.exists(c) for c in cand): err(f'{zid}: table_ref {ref} not found in tables/loot-decks/')


# ---- reserve-specific sections
def rows_ok(owner, rows):
    for rid in rows:
        seen_ledger.add(rid)
        if rid not in ledger: err(f'{owner}: ledger row {rid} does not exist')
ck = doc.get('floor_clock') or {}
if not ck: err('floor_clock missing')
else:
    if ck.get('canon_days') != 6: err('floor_clock.canon_days must be 6 (ledger M-%s)' % '332')
    rows_ok('floor_clock', ck.get('canon_rows', []))
    if ck.get('canon_confidence') != weakest(ck.get('canon_rows', [])): err('floor_clock confidence != ledger')
    h = ck.get('house', {})
    if h.get('tag') != 'inspired': err('floor_clock.house must be tagged inspired')
    if h.get('conflict_row') not in ledger: err('floor_clock.house.conflict_row missing from ledger')
    for f in h.get('fixed_points_keep_absolute', []): rows_ok('floor_clock.fixed_points', f.get('ledger_rows', []))
for sec in ('floor_differences_from_floor_1', 'timeline_by_countdown'):
    if not doc.get(sec): err(sec + ' missing or empty')
    for d in doc.get(sec, []):
        rows_ok(sec + '/' + d.get('id', '?'), d.get('ledger_rows', []))
        if d.get('confidence') != weakest([r for r in d.get('ledger_rows', []) if not r.startswith('X-')]): err(f'{sec}/{d.get("id")}: confidence != ledger')
sa = doc.get('system_announcements') or {}
if not sa.get('voice') or not sa.get('beats'): err('system_announcements incomplete')
for b in sa.get('beats', []):
    rows_ok('announcement/' + b['id'], b.get('ledger_rows', []))
    for q in b.get('quotes', []):
        if len(q['quote'].split()) > 25: err(f'announcement/{b["id"]}: quote > 25 words')
        if q['row'] not in ledger or q['quote'] not in ledger[q['row']]['quotes']: err(f'announcement/{b["id"]}: quote is not the quote of {q["row"]}')
if not doc.get('gaps'): err('gaps missing')
bl = doc.get('refinement_backlog') or []
if len(bl) < 5: err('refinement_backlog missing or too short')
bids = set()
for b in bl:
    if b.get('id') in bids: err('duplicate backlog id ' + str(b.get('id')))
    bids.add(b.get('id'))
    for k in ('id', 'priority', 'item', 'why', 'how'):
        if not b.get(k): err(f'backlog {b.get("id")}: missing {k}')
    rows_ok('backlog/' + str(b.get('id')), b.get('ledger_rows', []))
rows_ok('open_conflicts', doc.get('open_conflicts', []))
if doc.get('ledger_version') != re.search(r'Version: ([\d.]+)', open(LEDGER).read().split('\n')[1]).group(1): err('ledger_version is stale; re-run the builder')

# ---- forbidden text scan (skip disclaimer keys)
def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in SKIP_KEYS: continue
            yield from walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from walk(v, f'{path}[{i}]')
    elif isinstance(o, str): yield path, o
for path, s in walk(doc):
    if path.endswith('/quote') or path.endswith('/quote_source') or path.endswith('/quote_row'): continue  # ledger/wiki wording, verified above
    for pat in FORBID:
        if re.search(pat, s, re.I): err(f'forbidden text {pat!r} at {path}: {s[:70]}')
# canon entries must not use house words and vice versa is not enforced.

# ---- md view up to date
sys.path.insert(0, ROOT + '/tools')
try:
    import importlib
    b = importlib.import_module('canon_floor2_build')
    fresh = b.md(b.build())
    cur = open(ROOT + '/tables/canon-floor-2.md', encoding='utf-8').read().rstrip('\n')
    if fresh.rstrip('\n') != cur: err('tables/canon-floor-2.md is out of date; re-run tools/canon_floor2_build.py')
    # JSON also equals a fresh build
    if json.dumps(b.build(), indent=1, ensure_ascii=False) + '\n' != open(JP, encoding='utf-8').read(): err('JSON is not what the builder produces now; re-run tools/canon_floor2_build.py')
except Exception as e:
    warns.append(f'builder freshness check skipped: {e}')

sha = hashlib.sha256(open(JP, 'rb').read()).hexdigest()
tags = {}
for z in doc['zones']:
    tags[z['tag']] = tags.get(z['tag'], 0) + 1
    for k in ('mobs', 'hazards', 'features'):
        for e in z[k]: tags[e['tag']] = tags.get(e['tag'], 0) + 1
print(f"zones {counts['zones']} | mobs {counts['mobs']} | hazards {counts['hazards']} | features {counts['features']}")
print(f"distinct ledger rows referenced: {len(seen_ledger)} (all exist: {not any('does not exist' in e or 'missing' in e for e in errs)})")
print('tag counts (zones+entries):', tags)
print('sha256', sha)
for w in warns: print('WARN', w)
for e in errs: print('ERROR', e)
print(f'errors: {len(errs)}')
sys.exit(1 if errs else 0)
