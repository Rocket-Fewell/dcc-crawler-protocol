import json,urllib.request,urllib.parse,concurrent.futures as cf,re
H={"User-Agent":"Mozilla/5.0"}
titles=open("titles.txt").read().split("\n")
def fetch(batch):
    for attempt in range(3):
        try:
            u="https://dungeon-crawler-carl.fandom.com/api.php?action=query&prop=revisions&rvprop=content&rvslots=main&format=json&titles="+urllib.parse.quote("|".join(batch))
            d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=90))
            return list(d["query"]["pages"].values())
        except Exception as e: err=e
    print("fail",err); return []
batches=[titles[i:i+25] for i in range(0,len(titles),25)]
out={}
with cf.ThreadPoolExecutor(6) as ex:
    for res in ex.map(fetch,batches):
        for p in res:
            if "revisions" in p: out[p["title"]]=p["revisions"][0]["slots"]["main"]["*"]
json.dump(out,open("all.json","w"))
print(len(out), sum(len(v) for v in out.values()))
