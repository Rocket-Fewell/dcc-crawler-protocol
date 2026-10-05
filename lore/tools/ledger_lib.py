"""Helpers for building/checking CANON-LEDGER.md.  All quotes are pulled programmatically from local source
files so they are exact substrings (see ledger_check.py).  Written 2026-10-03 (Pass 4)."""
import re, os, json
ROOT='/workspace/dcc-lore'
PAGES=ROOT+'/raw/pages'
_cache={}
def fname(title): return re.sub(r'[^\w\-\.\' ()]','_',title)+'.txt'
def unspoil(t):
    """replace {{Spoiler|book=N|spoiler=TEXT}} wrappers by TEXT (brace-depth aware)"""
    out=[];i=0;n=len(t)
    pat=re.compile(r'\{\{\s*[Ss]poiler\s*\|\s*book\s*=\s*\d+\s*\|\s*spoiler\s*=\s*')
    while i<n:
        m=pat.search(t,i)
        if not m: out.append(t[i:]);break
        out.append(t[i:m.start()])
        j=m.end();depth=0
        while j<n:
            if t.startswith('{{',j): depth+=1;j+=2
            elif t.startswith('}}',j):
                if depth==0: break
                depth-=1;j+=2
            else: j+=1
        out.append(unspoil(t[m.end():j]));i=j+2
    return ''.join(out)
def page(title):
    title=resolve(title) if title!='' else title
    if title not in _cache:
        p=os.path.join(PAGES,fname(title))
        _cache[title]=unspoil(open(p,errors='ignore').read().replace('{{PAGENAME}}',title)) if os.path.exists(p) else None
    return _cache[title]
def resolve(title):
    for _ in range(3):
        p=os.path.join(PAGES,fname(title))
        if not os.path.exists(p): return title
        raw=open(p,errors='ignore').read().strip()
        m=re.match(r'#redirect\s*:?\s*(?:\[\[)?([^#\n\]\|]+)',raw,flags=re.I)
        if not m: return title
        title=m.group(1).strip()
    return title
def exists(title): return page(resolve(title)) is not None
CITE=re.compile(r'\[(\d+)\|([^\]|]+)\]')
def norm_ws(s): return re.sub(r'\s+',' ',s).strip()
def strip_cites(s): return norm_ws(CITE.sub('',s))
def cites_in(s):
    out=[]
    for b,c in CITE.findall(s):
        out.append(f'B{b}:{c.strip()}')
    return out
def fmt_cite(c):  # 'B1:5' -> 'B1 ch5'
    b,ch=c.split(':',1)
    return f'{b} ch{ch}' if ch.isdigit() else f'{b} {ch}'
def sections(t):
    parts=re.split(r'^(==[^=\n]+==)\s*$',t,flags=re.M)
    d={'_lead':parts[0]}
    for i in range(1,len(parts),2): d[parts[i].strip('= ').strip()]=parts[i+1]
    return d
def split_sentences(s):
    """sentences keep trailing cite markers"""
    s=re.sub(r'\s*\n\s*',' ',s)
    out=re.split(r'(?<=[\.\!\?\u201d"])(?:(?:\[\d+\|[^\]]+\])*)\s+(?=[A-Z0-9\u201c"\(\*])',s)
    # re-attach: the split dropped trailing cites, so use finditer approach instead
    res=[];pos=0
    for m in re.finditer(r'(?<=[\.\!\?\u201d"])((?:\[\d+\|[^\]]+\])*)\s+(?=[A-Z0-9\u201c"\(\*])',s):
        res.append(s[pos:m.end(1)]);pos=m.end()
    res.append(s[pos:])
    return [x.strip() for x in res if x.strip()]
def trim_words(q,maxw=25):
    w=q.split(' ')
    if len(w)<=maxw: return q
    return ' '.join(w[:maxw])+' …'
def esc(s): return s.replace('|','\\|').replace('\n',' ')
def unesc(s): return s.replace('\\|','|')

def ai_quote(title,maxw=25,prefer=None):
    """Quote from the page's AI Description (System text). Returns (quote, cites) or (None,[])"""
    t=page(title)
    if not t: return None,[]
    sec=sections(t)
    body=None
    for h in ('AI Description','AI Notification','Introductory Announcement'):
        if h in sec: body=sec[h];break
    if body is None: return None,[]
    return pick_from_body(body,maxw,prefer)
def pick_from_body(body,maxw=25,prefer=None):
    body=body.replace('\r','')
    lines=[l.strip() for l in body.split('\n') if l.strip()]
    cand=[]   # (line_idx, sentence)
    for i,l in enumerate(lines):
        if re.match(r'^(New )?[Aa]chievement!',l) or re.match(r'^New Achievement',l): continue
        if re.match(r'^Reward\s*:',l): continue
        if l.startswith('System Message') or l.startswith('Admin Note'): continue
        for s in split_sentences(l): cand.append((i,s))
    if prefer:
        for i,s in cand:
            if re.search(prefer,s): return fit(s,maxw)
    for k,(i,s) in enumerate(cand):
        st=strip_cites(s)
        if len(st.split())<3: continue
        out=[s]
        j=k+1
        while len(strip_cites(' '.join(out)).split())<8 and j<len(cand):
            ni,ns=cand[j]
            if ni-cand[j-1][0]>1: break
            if len(strip_cites(' '.join(out+[ns])).split())>maxw: break
            out.append(ns); j+=1
        return fit(' '.join(out),maxw)
    return None,[]
def fit(s,maxw=25):
    cs=cites_in(s); st=strip_cites(s)
    return trim_words(st,maxw),cs
def reward_quote(title,maxw=25):
    t=page(title)
    if not t: return None
    sec=sections(t)
    for h in ('AI Description',):
        if h in sec:
            m=re.search(r'^Reward\s*:\s*(.+)$',sec[h],flags=re.M)
            if m: return trim_words(strip_cites(m.group(1)),maxw)
    return None
def body_lines(t):
    t=re.sub(r'\{\{[^{}]*\}\}','',t)
    t=re.sub(r'\{\{[^{}]*\}\}','',t)
    t=re.sub(r'\{\|.*?\|\}','',t,flags=re.S)
    out=[]
    for l in t.split('\n'):
        l=l.strip()
        if not l or l.startswith(('==','|','{','}','!',':')): continue
        l=re.sub(r'^[\*#]+\s*','',l)
        out.append(l)
    return out
def find_sentence(title,pattern,maxw=25,section=None):
    """best sentence in page (or named section) matching regex -> (quote, cites). Prefers <=maxw words."""
    first=pattern.startswith('!')
    if first: pattern=pattern[1:]
    t=page(title)
    if not t: return None,[]
    if section:
        t=sections(t).get(section,'')
    cands=[]
    for l in body_lines(t):
        for s in split_sentences(l):
            st=strip_cites(s)
            if re.search(pattern,st,flags=re.I) and len(st.split())>=4:
                cands.append((s,st))
    if not cands: return None,[]
    if not first:
        for s,st in cands:
            if len(st.split())<=maxw: return st,cites_in(s)
    s,st=cands[0]
    if len(st.split())<=maxw: return st,cites_in(s)
    m=re.search(pattern,st,flags=re.I); w=st.split(' ')
    idx=len(st[:m.start()].split(' '))-1
    a=max(0,idx-8); b=min(len(w),a+maxw); a=max(0,b-maxw)
    q=' '.join(w[a:b])
    return ('… ' if a>0 else '')+q+(' …' if b<len(w) else ''),cites_in(s)
def lead_quote(title,maxw=25):
    t=page(title)
    if not t: return None,[]
    sec=sections(t)
    pre=sec['_lead']
    for l in body_lines(pre):
        if len(strip_cites(l).split())>=6:
            ss=split_sentences(l)
            for s in ss:
                if len(strip_cites(s).split())>=5: return fit(s,maxw)
    # fall back: first long body sentence anywhere before AI Description
    for l in body_lines(t):
        for s in split_sentences(l):
            if len(strip_cites(s).split())>=6: return fit(s,maxw)
    return None,[]
def src_text(tag):
    """resolve a source tag like W:Page, YT:id, FW2:file, NL:file to file text (for checks)"""
    kind,_,name=tag.partition(':')
    if kind=='W': return page(name)
    if kind=='YT':
        p=f'{ROOT}/sources/youtube/{name}.txt'
    elif kind=='FW2': p=f'{ROOT}/sources/fanwiki/{name}.txt'
    elif kind=='NL': p=f'{ROOT}/sources/nl/{name}.txt'
    else: return None
    return open(p,errors='ignore').read() if os.path.exists(p) else None
