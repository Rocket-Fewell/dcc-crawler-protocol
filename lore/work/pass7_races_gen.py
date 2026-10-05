import sys,re,datetime
sys.path.insert(0,'/workspace/dcc-lore/tools'); sys.path.insert(0,'/workspace/dcc-lore/work')
from ledger_lib import *
import pass7_races_spec as S
DATE=datetime.date.today().isoformat()
TAG=re.compile(r'\b(W|FW2|NL|YT):([^;|]+)')
def src_norm(tag):
    kind,_,name=tag.partition(':'); t=src_text(f'{kind}:{name.strip()}')
    return norm_ws(strip_cites(t)).replace('\u200b','') if t else None
bad=[]
def chk(q,tag,label):
    if not q: return
    core=norm_ws(q).strip('… ').strip()
    t=src_norm(tag)
    if t is None: bad.append((label,'no source',tag));return
    if len(core.split())>25: bad.append((label,'>25',q[:60]))
    if core not in t: bad.append((label,'not found',q[:80]))
def cell(q): return '"'+esc(q)+'"' if q else '—'
n=25
rows=[]
def mk(items,prefix):
    global n
    out=[]
    for (sub,facts,named,cite,q1,s1,conf,q2,s2) in items:
        i=f'R-{n:03d}'; n+=1
        chk(q1,s1,i+' '+sub); chk(q2,s2,i+' q2 '+sub)
        out.append(f'| {i} | {esc(sub)} | {esc(facts)} | {esc(named)} | {esc(cite)} | {cell(q1)} | {s1} | {conf} | {cell(q2)} | {s2 or "—"} | {DATE} |')
    return out
proc=mk(S.PROCESS,'P'); first=25; mid=n; races=mk(S.RACES,'R'); last=n-1
x=31; xr=[]
for (topic,a,sa,b,sb,status) in S.CONFLICTS:
    i=f'X-{x:03d}'; x+=1
    chk(a,sa,i+' A'); 
    if sb: chk(b,sb,i+' B')
    qa=f'"{esc(a)}"'
    qb=(f'"{esc(b)}"' if sb else f'— {esc(b)}')
    xr.append(f'| {i} | {esc(topic)} | {qa} | {sa} | {qb} | {sb or "WEB (snippet, not quotable)"} | {esc(status)} | {DATE} |')
print('failures',len(bad)); [print(b) for b in bad]
open('/workspace/dcc-lore/work/pass7_block.md','w').write('\n'.join(proc)+'\n@@RACES@@\n'+'\n'.join(races)+'\n@@X@@\n'+'\n'.join(xr)+'\n')
print('R-025..R-%03d'%last, len(proc),len(races),len(xr),'X-031..X-%03d'%(x-1), 'process ends', mid-1)
