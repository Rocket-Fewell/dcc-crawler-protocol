import json,glob,random,statistics,sys
cards=[]
for f in glob.glob('tables/loot-decks/f01-*.json'):
    if 'story' in f: continue
    cards+=json.load(open(f))['cards']
def pool(tier,kinds,cap=None):
    p=[(c['credit_value'],c['draw_weight']) for c in cards if c['tier']==tier and c['kind'] in kinds and (c.get('draw_weight') or 0)>0 and (cap is None or c['credit_value']<=cap)]
    if not p: p=[(c['credit_value'],c['draw_weight']) for c in cards if c['tier']==tier and c['kind']=='consumable' and (c.get('draw_weight') or 0)>0 and (cap is None or c['credit_value']<=cap)]
    return p
def run(N=60000,seed=7,silver_cap=None,gov_thr=None,gov_cap=175,r1=(2,3),deed=(0.5,0.9),p1=((0.057,3),(0.23,1)),p2=((0.07,8),(0.28,2))):
    rng=random.Random(seed)
    def draw(p):
        tot=sum(w for v,w in p); r=rng.uniform(0,tot)
        for v,w in p:
            r-=w
            if r<=0: return v
        return p[-1][0]
    def pull(tier,cap=None,depth=0):
        c = cap if tier=='Silver' else None
        r=rng.randint(1,100)
        if r<=30: v=draw(pool(tier,['consumable'],c))
        elif r<=55: v=draw(pool(tier,['item'],c))
        elif r<=70: v=(sum(rng.randint(1,6) for _ in range(3))*5 if tier=='Bronze' else sum(rng.randint(1,6) for _ in range(2))*25)
        elif r<=88: v=draw(pool(tier,['consumable','item'],c))
        elif r<=98: v=draw((pool(tier,['junk','clue','key']) if tier=='Bronze' else pool(tier,['consumable'],c)))
        else: v=pull('Silver',cap,depth+1) if depth<2 else 0
        if tier=='Silver' and c is not None and v>c: v=c
        return v
    res=[]
    for _ in range(N):
        t=(rng.randint(1,4)*2)*3 + rng.randint(1,6)*2 + rng.randint(1,6)*5
        t+= pull('Bronze')+pull('Bronze')
        for p,n in p1:
            for _ in range(n):
                if rng.random()<p: t+=sum(pull('Bronze') for _ in range(rng.choice([1,2])))
        for _ in range(3):
            if rng.random()<deed[0]/3: t+=sum(pull('Bronze') for _ in range(rng.choice([1,2])))
        t+=sum(rng.randint(10,40) for _ in range(r1[0]))
        sc=silver_cap
        t+=sum(pull('Silver',sc) for _ in range(2))
        t+=sum(rng.randint(0,2) for _ in range(4))+sum(rng.randint(1,4)*2 for _ in range(8))+sum(rng.randint(1,6)*2 for _ in range(2))+rng.randint(1,6)*5
        for p,n in p2:
            for _ in range(n):
                if rng.random()<p: t+=sum(pull('Bronze') for _ in range(rng.choice([1,2])))
        for _ in range(3):
            if rng.random()<deed[1]/3: t+=sum(pull('Bronze') for _ in range(rng.choice([1,2])))
        t+=sum(rng.randint(10,40) for _ in range(r1[1]))
        cap = sc
        if gov_thr is not None and t>=gov_thr: cap = gov_cap if sc is None else min(sc,gov_cap)
        t+=sum(pull('Silver',cap) for _ in range(2))
        res.append(t)
    res.sort(); n=len(res)
    return round(statistics.mean(res)), round(res[n//2]), round(res[int(n*.9)]), round(res[int(n*.95)]), round(100*sum(1 for x in res if x>1500)/n,1)
if __name__=="__main__":
    print('base',run())
    for thr in (700,800,900):
        for gc in (175,250):
            print('gov',thr,gc,run(gov_thr=thr,gov_cap=gc))
    print('cap300',run(silver_cap=300))
    print('cap300+gov800/200',run(silver_cap=300,gov_thr=800,gov_cap=200))
