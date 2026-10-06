import os as _os
_LORE = _os.environ.get('DCC_LORE_ROOT') or _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
import re,sys
sys.path.insert(0,_os.path.join(_LORE, 'tools'))
from ledger_lib import *
_n={}
def srcnorm(tag):
    if tag not in _n:
        t=src_text(tag)
        _n[tag]=norm_ws(strip_cites(t)).replace('\u200b','') if t else None
    return _n[tag]
def rx(s): return re.escape(s).replace("\\'","['’]").replace("'", "['’]").replace('\\ ',' ')
def Q(tag,start,end=None):
    t=srcnorm(tag)
    if t is None: raise Exception('no source '+tag)
    end=end or start
    m=re.search(rx(start),t)
    if not m: raise Exception(f'start not found {tag}: {start}')
    m2=re.compile(rx(end)).search(t,m.start())
    if not m2: raise Exception(f'end not found {tag}: {end}')
    q=t[m.start():m2.end()]
    if len(q.split())>25: raise Exception(f'>25 words ({len(q.split())}) {tag}: {q}')
    return q

import re as _re
def isTag(x): return bool(_re.match(r'^(W|YT|FW2|NL):',x))
def parse(r):
    sec,subj,find,bc,conf=r[:5]
    rest=list(r[5:]); quotes=[]  # list of (tag,quote)
    while rest:
        tag=rest.pop(0); items=[]
        while rest and not isTag(rest[0]): items.append(rest.pop(0))
        start=items[0]; end=items[1] if len(items)>1 else start
        quotes.append((tag,start,end))
    return sec,subj,find,bc,conf,quotes
