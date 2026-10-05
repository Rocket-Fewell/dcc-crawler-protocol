#!/usr/bin/env python3
"""Verify every quoted string in CANON-LEDGER.md is an exact substring (cites/whitespace normalised) of a source
named in the same table row.  Usage: python3 tools/ledger_check.py [path]   (default: CANON-LEDGER.md)
Exit code 1 if any quote fails or exceeds 25 words."""
import re,sys
sys.path.insert(0,'/workspace/dcc-lore/tools')
from ledger_lib import *
path=sys.argv[1] if len(sys.argv)>1 else ROOT+'/CANON-LEDGER.md'
TAG=re.compile(r'\b(W|FW2|NL|YT):([^;|]+)')
def src_norm(tag):
    kind,_,name=tag.partition(':'); name=name.strip()
    cands=[name]
    m=re.match(r'^(.*?)\s*\([^()]*\)$',name)
    if m: cands.append(m.group(1))
    for c in cands:
        t=src_text(f'{kind}:{c}')
        if t: return norm_ws(strip_cites(t)).replace('\u200b','')
    return None
cache={}
bad=[];n=0;rows=0
for ln,line in enumerate(open(path),1):
    if not line.startswith('|') or line.startswith('|---'): continue
    cells=[c.strip() for c in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
    quotes=[unesc(c)[1:-1] for c in cells if len(c)>2 and c.startswith('"') and c.endswith('"')]
    if not quotes: continue
    rows+=1
    tags=[(k,v.strip()) for k,v in TAG.findall(line)]
    texts=[]
    for k,v in tags:
        t=src_norm(f'{k}:{v}')
        if t: texts.append(t)
    for qt in quotes:
        n+=1
        core=norm_ws(qt).strip('… ').strip()
        if len(core.split())>25: bad.append((ln,'>25 words',qt[:80]));continue
        if not any(core in t for t in texts): bad.append((ln,'not found in cited sources',qt[:100]))
print(f'checked {n} quotes in {rows} rows; failures: {len(bad)}')
for b in bad[:60]: print(b)
sys.exit(1 if bad else 0)
