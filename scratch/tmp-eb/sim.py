import json,glob,random,statistics
cards=[]
for f in glob.glob('tables/loot-decks/f01-*.json'):
    if 'story' in f: continue
    cards+=json.load(open(f))['cards']
def pool(tier,kinds):
    return [(c['credit_value'],c['draw_weight']) for c in cards if c['tier']==tier and c['kind'] in kinds and (c.get('draw_weight') or 0)>0]
def wmean(p): return sum(v*w for v,w in p)/sum(w for v,w in p)
def draw(p,rng):
    tot=sum(w for v,w in p); r=rng.uniform(0,tot)
    for v,w in p:
        r-=w
        if r<=0: return v
    return p[-1][0]
def pull(tier,rng,depth=0):
    r=rng.randint(1,100)
    if r<=30: return draw(pool(tier,['consumable']),rng)
    if r<=55: return draw(pool(tier,['item']),rng)
    if r<=70:
        # credits: bronze 3d6x5, silver 2d6x25
        return sum(rng.randint(1,6) for _ in range(3))*5 if tier=='Bronze' else sum(rng.randint(1,6) for _ in range(2))*25
    if r<=88: return draw(pool(tier,['consumable','item']),rng)  # tailored
    if r<=98: return draw(pool(tier,['junk','clue','key']) or pool(tier,['consumable']),rng)
    return pull('Silver',rng,1) if tier=='Bronze' else pull('Silver',rng,1) if depth<1 else 0
def box(tier,rng,pulls=None):
    n=pulls or (rng.choice([1,2]) if tier=='Bronze' else 2)
    return sum(pull(tier,rng) for _ in range(n))
rng=random.Random(70)
N=200000
for t in ['Bronze','Silver']:
    xs=[box(t,rng) for _ in range(N)]
    xs.sort(); print(t,'mean',round(statistics.mean(xs),1),'p50',xs[N//2],'p90',xs[int(N*.9)],'p95',xs[int(N*.95)],'p99',xs[int(N*.99)],'max',xs[-1])
