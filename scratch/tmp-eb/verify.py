import json,re
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
R = os.environ.get("DCC_CAMPAIGN_ROOT") or os.environ.get("DCC_CAMPAIGN_DIR") or os.path.abspath(os.path.join(_HERE, "..", ".."))
if not R.endswith(os.sep):
    R += os.sep
d=json.load(open(R+"rules/70-encounter-budget-5e.json"))
day=json.load(open(R+"floors/f01/day-01.json"))
spec=json.load(open(R+"floors/f01/day-01.spec.json"))
sl=d["day01_slot_map"]["slots"]
assert len(sl)==34==len(day["slots"])
for a,b in zip(sl,day["slots"]):
    assert a["spec_path"]==b["path"],(a,b["path"])
    assert ("value" in a) != ("value_by_party_size" in a)
print("34 slots path-aligned, each has value")
def resolve(path):
    p=re.sub(r"\s*\(.*\)","",path)
    p=re.sub(r"\[[^\]]*\]","",p)
    cur=d
    for k in p.split("."):
        if k=="*": break
        assert isinstance(cur,dict) and k in cur,(path,k)
        cur=cur[k]
    return True
for a in sl: resolve(a["fills_from"])
print("fills_from paths resolve")
e=d["economy_audit"]
for P,v in e["by_party_size"].items(): assert v["per_crawler_f1_f2"]==e["expected_total_f1_f2_per_crawler"]<1500
print("per-crawler flat",e["expected_total_f1_f2_per_crawler"])
# day-01 spec counts cross-check vs fixed encounters
fe=d["floors"]["1"]["fixed_encounters"]
for z,v in fe.items():
    if z.startswith("_"): continue
    for P in "234":
        print(z,P,v["counts_by_party_size"][P],v["xp_by_party_size"][P],v["fit"][P]["tier_budget"],"OVER %d"%v["fit"][P]["over_by"] if v["fit"][P]["over_by"] else "")
