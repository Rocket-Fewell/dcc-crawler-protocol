"""Regenerates catalog/system-voice-index.md: page names that carry System-voice sections, no text excerpts."""
import os,re,json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parent))
from paths import LORE_ROOT
P=str(LORE_ROOT/'raw'/'pages'); D=json.load(open(LORE_ROOT/'raw'/'all.json'))
Dn={re.sub(r'[:?/"*<>|]','_',k):k for k in D}
heads={'AI Description':'AI Description','Introductory Announcement':'Floor announcement','AI Notification':'Notification','Quest Updates':'Quest update','Quest Status':'Quest status','Quest':'Quest text','Level Up':'Level-up note','Official Summary':'Official summary'}
rows=[]
for f in sorted(os.listdir(P)):
    k=f[:-4]; t=open(os.path.join(P,f),errors='ignore').read()
    secs=re.split(r'^(==\s*[^=\n]+?\s*==)\s*$',t,flags=re.M)
    src=D.get(Dn.get(k,k)) or ''
    cats=[c.strip() for c in re.findall(r'\[\[Category:([^\]|]*)',src)]
    for i in range(1,len(secs),2):
        h=secs[i].strip('= ').strip()
        if h in heads and h in('AI Description','Introductory Announcement','AI Notification'):
            body=secs[i+1].strip()
            rows.append((k,heads[h],len(body.split()),cats[0] if cats else '?', 'yes' if re.search(r'Reward\s*:',body) else ''))
out=['# System-voice index (generated; page names only, no quoted text)','',f'{len(rows)} sections. Source text lives in `raw/pages/<Page>.txt`. Regenerate: `python3 tools/voice_index.py`. `Words` = length of the wiki-transcribed section; `Reward line` = contains a "Reward:" line.','','| Page | Section | Words | First category | Reward line |','|---|---|---|---|---|']
for r in rows: out.append('| %s | %s | %d | %s | %s |'%r)
open(LORE_ROOT/'catalog'/'system-voice-index.md','w').write('\n'.join(out)+'\n')
print(len(rows))

import apply_headers; apply_headers.main()  # keep convention headers after regeneration
