import sys,re
sys.path.insert(0,'/workspace/dcc-lore/tools'); sys.path.insert(0,'/workspace/dcc-lore/work')
from ledger_lib import *
import revival_rows as R
TAG=re.compile(r'\b(W|FW2|NL|YT):([^;|]+)')
def srcnorm(tag):
    k,_,n=tag.partition(':'); n=n.strip()
    for c in [n, re.sub(r'\s*\([^()]*\)$','',n)]:
        t=src_text(f'{k}:{c}')
        if t: return norm_ws(strip_cites(t)).replace('\u200b','')
bad=0
def chk(id,quote,tags):
    global bad
    q=norm_ws(quote)
    if len(q.split())>25: print('LONG',id,len(q.split())); bad+=1
    texts=[srcnorm(f'{k}:{v}') for k,v in TAG.findall(tags)]
    texts=[t for t in texts if t]
    if not texts: print('NOSRC',id,tags); bad+=1; return
    ok=any(q in t or q.replace('\u2019',"'") in t.replace('\u2019',"'") for t in texts)
    if not ok:
        # try loose
        tl=[t.replace('\u2019',"'").replace('\u201c','"').replace('\u201d','"') for t in texts]
        ql=q.replace('\u2019',"'")
        if any(ql in t for t in tl): print('CURLY',id); return
        print('MISS',id,'|',q[:90]); bad+=1
for grp in (R.A,R.B,R.C,R.D):
    for r in grp: chk(r[0],r[6],r[7])
for r in R.LOOK: chk(r[0],r[4],r[5])
for r in R.NOREV: chk(r[0],r[2],r[3])
print('bad',bad)
