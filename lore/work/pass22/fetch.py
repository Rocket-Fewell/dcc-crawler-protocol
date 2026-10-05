import json,urllib.request,urllib.parse,re,sys
sys.path.insert(0,'/workspace/dcc-lore/raw')
H={"User-Agent":"Mozilla/5.0"}
titles=[t for t in open('titles.txt').read().split('\n') if t.strip()]
out={};missing=[]
for i in range(0,len(titles),20):
    b=titles[i:i+20]
    u="https://dungeon-crawler-carl.fandom.com/api.php?action=query&redirects=1&prop=revisions&rvprop=content|ids|timestamp&rvslots=main&format=json&titles="+urllib.parse.quote("|".join(b))
    d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=90))
    for p in d["query"]["pages"].values():
        if "revisions" in p:
            r=p["revisions"][0]; out[p["title"]]={"rev":r["revid"],"ts":r["timestamp"],"text":r["slots"]["main"]["*"]}
        else: missing.append(p.get("title"))
    for rd in d["query"].get("redirects",[]): print("redirect",rd)
json.dump(out,open('live.json','w'))
print(len(out),"missing",missing)
