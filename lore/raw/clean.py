import json,re,os
d=json.load(open("all.json"))
def clean(t):
    t=re.sub(r'<ref[^>]*/>','',t)
    t=re.sub(r'<ref[^>]*>.*?</ref>','',t,flags=re.S)
    t=re.sub(r'<!--.*?-->','',t,flags=re.S)
    t=re.sub(r'\{\{cite\|[^}]*\}\}',lambda m:'['+m.group(0)[7:-2]+']',t)
    t=re.sub(r'\[\[(?:File|Image|Category):[^\]]*\]\]','',t)
    t=re.sub(r'\[\[([^\]|]*)\|([^\]]*)\]\]',r'\2',t)
    t=re.sub(r"\[\[([^\]]*)\]\]",r'\1',t)
    t=re.sub(r"'''?","",t)
    t=re.sub(r'<[^>]+>','',t)
    t=re.sub(r'\n{3,}','\n\n',t)
    return t
os.makedirs("pages",exist_ok=True)
for k,v in d.items():
    open("pages/"+re.sub(r'[^\w\-\.\' ()]','_',k)+".txt","w").write(clean(v))
