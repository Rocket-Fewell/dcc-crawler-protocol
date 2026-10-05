import sys,re
sys.path.insert(0,'/workspace/dcc-lore/tools')
from wk import D,cats,info,clean,spoil,find_templates,fields
from ledger_lib import *
ORD={'first':1,'second':2,'third':3,'fourth':4,'fifth':5,'sixth':6,'seventh':7,'eighth':8,'ninth':9,'tenth':10,'eleventh':11,'twelfth':12}
def floor_num(s):
    if not s: return None
    m=re.search(r'\b(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth)\b',s,flags=re.I)
    if m: return ORD[m.group(1).lower()]
    m=re.search(r'(?:floor\s*)?(\d+)',s,flags=re.I)
    return int(m.group(1)) if m else None
def isredir(v): return v.lstrip().lower().startswith('#redirect')
def norm(n): return re.sub(r"[^a-z0-9]","",n.lower().replace('’',"'").replace(' achievement',''))
def master():
    M={};cur=None;fl=''
    body=page('Achievement')
    sec=body
    for line in body.split('\n'):
        m=re.match(r'^=== (Floor \d+) ===',line)
        if m: fl=m.group(1);continue
        m=re.match(r'^==== (.+?) ====',line)
        if m: cur=m.group(1).strip();M[cur]={'floor':fl,'lines':[],'n':norm(cur)};continue
        if line.startswith('==') : cur=None; continue
        if cur: M[cur]['lines'].append(line)
    return M
def hubs():
    rows=[]
    for n in range(1,10):
        t=page(f'Floor {n} Achievements')
        if not t: continue
        for m in re.finditer(r'\|-\n\|([^\n]*)\n\|([^\n]*)\n\|([^\n]*)',t):
            nm,fo,rw=[x.strip() for x in m.groups()]
            rows.append((n,nm,fo,rw))
    return rows
def fw2_blocks():
    out={}
    for f in ('book3-achievements','book4-achievements'):
        t=src_text('FW2:'+f)
        if not t: continue
        lines=[l.rstrip() for l in t.split('\n')]
        i=0
        while i<len(lines):
            if i+1<len(lines) and lines[i+1].startswith('Earner:'):
                nm=lines[i].strip('\u200b ').strip()
                blk=[];j=i+1
                while j<len(lines) and not (j+1<len(lines) and lines[j+1].startswith('Earner:')) and not lines[j].startswith('Wiki content'):
                    blk.append(lines[j]);j+=1
                out[norm(nm)]=(f,nm,'\n'.join(blk));i=j
            else: i+=1
    return out

def build_achievements():
    M=master(); H=hubs(); FW=fw2_blocks()
    MB={v['n']:(k,v) for k,v in M.items()}
    rows=[];stats={'VERIFIED':0,'WIKI-ONLY':0,'UNVERIFIED':0};conflicts=[];noquote=[];fw2hits=[]
    pages=sorted(k for k,v in D.items() if not isredir(v) and 'Achievements' in cats(v) and not re.match(r'^Floor \d+ Achievements$',k) and k not in ('Achievement','Good Shit Box'))
    used=set()
    for k in pages:
        v=D[k]; nm,f=info(v,{'achievement'})
        if not f: nm,f=info(v,{'item'})
        f=f or {}
        name=k.replace(' Achievement','')
        fl=clean(f.get('floor','')); tr=clean(f.get('for','')); rw=clean(f.get('reward',''))
        tr=re.sub(r'\s+',' ',tr).strip(); 
        fn=floor_num(fl)
        t=page(k) or ''
        cs=cites_in(t)
        mk=MB.get(norm(k))
        q,qc=ai_quote(k)
        qsrc=f'W:{k}'
        if q is None and mk:
            body='\n'.join(mk[1]['lines'])
            q,qc=pick_from_body(body); qsrc='W:Achievement'
        if q is None:
            noquote.append(k)
        if not rw:
            rq=reward_quote(k)
            rw=('(AI text) '+rq) if rq else ''
        if not rw and mk:
            m=re.search(r'^Reward\s*:\s*(.+)$','\n'.join(mk[1]['lines']),flags=re.M)
            if m: rw='(master list) '+trim_words(strip_cites(m.group(1)),18)
        mf=floor_num(mk[1]['floor']) if mk else None
        flags=[]
        if mk and fn and mf and fn!=mf: flags.append(f'floor conflict: page says F{fn}, master list says F{mf}')
        if not fn and mf: fn=mf; flags.append('floor from master list only')
        incomplete = (not tr) or (not rw)
        # second source
        tags=[qsrc if qsrc!='W:Achievement' else f'W:Achievement']
        second=None
        fb=FW.get(norm(k))
        if fb:
            fwrw=re.search(r'Reward:\s*(.*)',fb[2])
            box=re.search(r'((?:Bronze|Silver|Gold|Platinum|Legendary|Celestial)\s+[A-Z][\w\' \-’]+? Box)',rw or '')
            if box and fwrw and box.group(1).lower().replace('’',"'") in fwrw.group(1).lower().replace('’',"'"):
                second=fb[0]; tags.append('FW2:'+fb[0]); fw2hits.append((k,fb[0]))
        BF={1:{1,2},2:{3},3:{4},4:{5},5:{6,7},6:{8},7:{9},8:{10,11}}
        cb={int(c.split(':')[0][1:]) for c in cs}
        okf=set().union(*[BF.get(b,set()) for b in cb]) if cb else set()
        if any('floor conflict' in x for x in flags):
            cand={x for x in (fn,mf) if x}
            res=cand&okf
            flags=[x for x in flags if 'floor conflict' not in x]
            if len(res)==1:
                fn=res.pop(); flags.append(f'floor conflict (page F{floor_num(fl)} vs master list F{mf}) resolved to F{fn} by cited book(s)')
            else:
                flags.append(f'floor CONFLICT unresolved (page F{floor_num(fl)} vs master list F{mf})')
        if any('CONFLICT unresolved' in x for x in flags): conf='UNVERIFIED'
        elif incomplete and not q: conf='UNVERIFIED'
        elif cs or second: conf='VERIFIED'
        else: conf='WIKI-ONLY'
        basis=''
        if conf=='VERIFIED': basis=' (%s)'%('cite '+fmt_cite(cs[0]) if cs else '2 sources')
        if incomplete and conf!='UNVERIFIED': flags.append('infobox incomplete')
        books=sorted({int(c.split(':')[0][1:]) for c in cs})
        bk=','.join('B%d'%b for b in books) if books else 'B?'
        loc=(f'F{fn}' if fn else 'F?')+' / '+bk
        stats[conf]+=1
        rows.append(dict(name=name,loc=loc,trig=tr or '?',quote=q,reward=rw or '?',tags=tags,conf=conf+basis,flags=flags,src='page',key=k))
        used.add(norm(k))
        if flags: conflicts.append((name,flags))
    # master-only
    pagen={norm(k) for k in pages}
    mrows=[]
    for k,v in M.items():
        if v['n'] in pagen: continue
        body='\n'.join(v['lines'])
        q,qc=pick_from_body(body)
        m=re.search(r'^Reward\s*:\s*(.+)$',body,flags=re.M)
        rw=trim_words(strip_cites(m.group(1)),18) if m else '?'
        if m and not re.search(r'\b(Box|box|Patch|Coupon|Potion|Nothing|None)\b',rw): rw='(narration) '+rw
        mf=floor_num(v['floor'])
        cs=cites_in(body)
        conf='VERIFIED' if (cs and q) else ('WIKI-ONLY' if q else 'UNVERIFIED')
        basis=' (cite %s)'%fmt_cite(cs[0]) if conf=='VERIFIED' else ''
        stats[conf]+=1
        bk=','.join(sorted({'B'+c.split(':')[0][1:] for c in cs})) or 'B?'
        rows.append(dict(name=k,loc=f'F{mf} / {bk}',trig='(trigger not stated on master list; see quote)',quote=q,reward=rw,tags=['W:Achievement'],conf=conf+basis,flags=['master-list only; no own wiki page'],src='master',key=k))
        if q is None: noquote.append(k)
    # unnamed hub rows
    for n,nm,fo,rw in H:
        if nm!='N/A': continue
        cs=cites_in(rw+fo)
        rwc=strip_cites(rw).strip()
        conf='VERIFIED' if cs else 'WIKI-ONLY'
        basis=' (cite %s)'%fmt_cite(cs[0]) if cs else ''
        stats[conf]+=1
        bk=','.join(sorted({'B'+c.split(':')[0][1:] for c in cs})) or 'B?'
        rows.append(dict(name='(unnamed) F%d'%n,loc=f'F{n} / {bk}',trig=strip_cites(fo).strip(' .'),quote=None,reward=rwc or '?',tags=[f'W:Floor {n} Achievements'],conf=conf+basis,flags=['unnamed on hub page; no System text captured'],src='hub',key='hub%d'%n))
    return rows,stats,conflicts,noquote,fw2hits
