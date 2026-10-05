import json,re,collections
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parent))
from paths import LORE_ROOT
D=json.load(open(LORE_ROOT/'raw'/'all.json'))
D={k:v.replace('{{PAGENAME}}',k) for k,v in D.items()}
def cats(t): return [c.strip() for c in re.findall(r'\[\[Category:([^\]|]*)',t,flags=re.I)]
def find_templates(t):
    """return list of (name, body) for top-level {{...}}"""
    out=[];i=0;n=len(t)
    while i<n-1:
        if t[i:i+2]=='{{':
            depth=0;j=i
            while j<n-1:
                if t[j:j+2]=='{{': depth+=1;j+=2
                elif t[j:j+2]=='}}':
                    depth-=1;j+=2
                    if depth==0:break
                else:j+=1
            body=t[i+2:j-2]
            nm=re.split(r'[|\n]',body,1)[0].strip()
            out.append((nm,body,i,j));i=j
        else:i+=1
    return out
def fields(body):
    # split top-level on | respecting {{ }} and [[ ]]
    parts=[];cur='';d1=d2=0;i=0
    while i<len(body):
        c=body[i:i+2]
        if c=='{{':d1+=1;cur+=c;i+=2;continue
        if c=='}}':d1-=1;cur+=c;i+=2;continue
        if c=='[[':d2+=1;cur+=c;i+=2;continue
        if c==']]':d2-=1;cur+=c;i+=2;continue
        if body[i]=='|' and d1==0 and d2==0: parts.append(cur);cur=''
        else: cur+=body[i]
        i+=1
    parts.append(cur)
    f={}
    for p in parts[1:]:
        if '=' in p:
            k,v=p.split('=',1);f[k.strip().lower()]=v.strip()
    return f
def cite(m):
    a=[x.strip() for x in m.group(1).split('|')]
    if len(a)>=2 and a[0].isdigit(): return f'[B{a[0]} ch{a[1]}]' if a[1].isdigit() else f'[B{a[0]} {a[1]}]'
    return ''
def clean(s):
    s=re.sub(r'<ref[^>]*/>','',s); s=re.sub(r'<ref[^>]*>.*?</ref>','',s,flags=re.S)
    s=re.sub(r'<!--.*?-->','',s,flags=re.S); s=re.sub(r'<!--.*','',s,flags=re.S)
    s=re.sub(r'\{\{[Cc]ite\|([^}]*)\}\}',cite,s)
    s=re.sub(r'\{\{ref\|([^}]*)\}\}','',s)
    s=re.sub(r'\[\[(?:File|Image|Category):[^\]]*\]\]','',s)
    s=re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]',r'\1',s)
    s=re.sub(r'\[\[([^\]]*)\]\]',r'\1',s)
    s=re.sub(r"'{2,}","",s)
    s=re.sub(r'<br\s*/?>','; ',s)
    s=re.sub(r'<[^>]+>','',s)
    s=re.sub(r'\{\{[^{}]*\}\}','',s)
    s=re.sub(r'\s*\n\s*\*\s*','; ',s)
    s=re.sub(r'\s+',' ',s).strip(' ;')
    return s
def lead(t,maxlen=300):
    """first prose paragraph starting with ''' after templates"""
    # remove templates top-level
    ts=find_templates(t); out='';last=0
    for nm,b,i,j in ts: out+=t[last:i];last=j
    out+=t[last:]
    for para in re.split(r'\n\s*\n',out):
        p=para.strip()
        if p.startswith("'''") or re.match(r"^(The |A |An )?'''",p):
            c=clean(p); c=re.split(r'\s*==',c)[0]
            c=re.sub(r'\[B\d+ ch[^\]]*\]','',c).strip()
            if len(c)>maxlen:
                cut=c[:maxlen]; k=max(cut.rfind('. '),cut.rfind('; '))
                c=(cut[:k+1] if k>80 else cut.rstrip()+'…')
            return c
    return ''
def spoil(t):
    m=re.search(r'\{\{\s*[Ss]poil[Hh]\s*\|\s*(\d+)',t)
    return int(m.group(1)) if m else None
def info(t,names):
    for nm,b,i,j in find_templates(t):
        if nm.lower() in names: return nm,fields(b)
    return None,{}
def cites(t):
    s=sorted({(int(a),int(b)) for a,b in re.findall(r'\{\{[Cc]ite\|(\d+)\|(\d+)',t)})
    return s
def books(t):
    return sorted({a for a,b in cites(t)})
def bk(t):
    b=books(t); return ','.join(map(str,b)) if b else '?'
