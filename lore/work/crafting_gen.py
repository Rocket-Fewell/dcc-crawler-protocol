import os as _os
_LORE = _os.environ.get('DCC_LORE_ROOT') or _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
import sys,re; sys.path.insert(0,_os.path.join(_LORE, 'work'))
from crafting_lib import *
import crafting_rows as cr
DATE='2026-10-03'
def conf(c):
    if c.startswith('V '):
        r=c[2:]
        return 'VERIFIED ('+r+')' if not r.startswith('(') else 'VERIFIED '+r
    if c.startswith('UNRESOLVED') or c.startswith('GAP'): return 'UNVERIFIED ('+c.lower()+')'
    if c.startswith('RESOLVED'): return 'VERIFIED ('+c.lower()+')'
    return c
def qcell(q): return '"'+q.replace('|','\\|')+'"'
def esc(s): return s.replace('|','\\|')
secs={'T':'Tables / Workstations','S':'Skills & classes','I':'Ingredients','R':'Recipes','L':'Rules / limits / failure','X':'Conflicts and gaps'}
rows={k:[] for k in secs}
n=0;xn=0;ids={}
for r in cr.ROWS:
    sec,subj,find,bc,c,qs=parse(r)
    if sec=='X':
        xn+=1; rid=f'X-C{xn:02d}'; subj=re.sub(r'^X-C\d+\s*','',subj)
    else:
        n+=1; rid=f'K-{n:03d}'
    ids[subj]=rid
    q1=Q(*qs[0]); t1=qs[0][0]
    q2=Q(*qs[1]) if len(qs)>1 else None; t2=qs[1][0] if len(qs)>1 else None
    cc=conf(c)
    row=f"| {rid} | {esc(subj)} | {esc(find)} | {bc} | {qcell(q1)} | {t1} | {cc} | "+(f"{qcell(q2)} | {t2}" if q2 else "— | —")+f" | {DATE} |"
    rows[sec].append((rid,subj,cc,row))
HDR="| ID | Subject | Finding | Book/ch | Quote (<=25 words) | Source | Confidence | Quote 2 (second source) | Source 2 | Date |\n|---|---|---|---|---|---|---|---|---|---|"
def cat(c):
    return c.split(' ')[0].rstrip('(')
def counts(secs_):
    tot=v=w=u=0
    for k in secs_:
        for rid,subj,cc,row in rows[k]:
            tot+=1
            if cc.startswith('VERIFIED'): v+=1
            elif cc.startswith('WIKI-ONLY'): w+=1
            else: u+=1
    return tot,v,w,u
main=['T','S','I','R','L']
tot=counts(main); xt=counts(['X'])
def I(s): return ids[s]
def tables(level):
    out=[]
    for k in secs:
        out.append(f"{level} {list(secs).index(k)+1}. {secs[k]}\n")
        out.append(HDR)
        out+= [r[3] for r in rows[k]]
        out.append('')
    return '\n'.join(out)
body=tables('##')
quick=f"""## Quick reference (every line points to a row below)
| Station / topic | Key facts | Row IDs |
|---|---|---|
| Where tables live | Personal Space accessories; basic Crafting Studio holds 5 basic tables; Enhanced Crafting Studio is the upgrade; Safe Rooms sell tables only from Floor 4 (earlier tables looted/box-won) | {I('Workbenches in general')}, {I('Crafting Studio (basic)')}, {I('Enhanced Crafting Studio')} |
| How tables level | Auto +1 level per floor collapse (wiki); coupons (<=250,000 gold each) upgrade tables | {I('Workbenches: leveling')}, {I('Table upgrade coupons')}, {I('Table level counting')} |
| Engineer's Table | Catch-all fabrication with Goo-Inator 3000; ~25,000 gold; looted from a Floor-1 goblin workshop; L2 for multi-part builds | {I("Engineer's Table")}, {I("Engineer's Table: source (Carl)")}, {I("Engineer's Table: level 2")} |
| Sapper's Table | Gold Sapper's Box (Floor 2); L1 stability and modules; L3 infusion (Carl, Floor 4); skill/level 5 on Floor 6 with Agent Provocateur | {I("Sapper's Table: obtained")}, {I("Sapper's Table: level 1")}, {I("Sapper's Table: level 3")}, {I("Sapper's Table: level 5 (Book 5)")} |
| Alchemy Table | Looted Floor 2 (Rev-Up); Mordecai's table L3 on Floor 4 (Special Brew, potion balls); L5 halves brew time, L6 autoclave (100 units), L9 hoped-for fix; Floor 8 coupons for Liquid Therapy; Floor 9 recipe-learning | {I('Alchemy Table: source (Carl, Floor 2)')}, {I('Alchemy Table: level thresholds')}, {I('Alchemy Table: level 9 target')}, {I('Alchemy Table: Floor 8 coupons')}, {I('Alchemy Table: Floor 9 upgrade')} |
| Armorer's Workshop | Needed for equippable armor; L1 cannot enchant or work most metals | {I("Armorer's Workshop/Table")}, {I("Armorer's Workshop: level 1 limits")} |
| Other tables | Metal Working (L2 Floor 5, L3 reforge), Bolt-Thrower's, Makeup (L3/L5), Automaton (Floor 6), Advanced Bomber's Studio | {I('Metal Working Table')}, {I("Bolt-Thrower's Workshop")}, {I('Makeup Table')}, {I('Automaton Table')}, {I("Advanced Bomber's Studio")} |
| Carl's class path | Compensated Anarchist (Floor 3) then Agent Provocateur (Floor 6) | {I('Compensated Anarchist (class)')}, {I('Agent Provocateur (subclass)')} |
| Mordecai's Special Brew | 30 s near-immortality, 10 h potion sickness, only two work per drinker | {I("Mordecai's Special Brew")}, {I("Mordecai's Special Brew: limits")}, {I("Mordecai's Special Brew: potion sickness")} |
| Carl's inventions | Jug O' Boom (Dungeonpreneur), MOAB, Jelly Bomb, Disco Ball, Doomsday Scenario, Royal Chariot, Waffle Maker, poleaxes | {I("Carl's Jug O' Boom")}, {I('Mother of All Bombs (MOAB)')}, {I('Jelly Bomb / landmines')}, {I('Hobgoblin Disco Ball')}, {I('The Waffle Maker (Book 7)')} |
| Not found locally | Cooking, Smithing, Enchanting, Scribe and Tinker stations/skills as defined crafts | {I('No Cooking/Smithing/Scribe/Tinker/Enchanting table or skill pages')} |
"""
head=f"""# Crafting Canon (Books 1-8)
Owner: DCC Lore | Status: review | Version: 1.0 | Updated: {DATE}
Summary: Crafting tables/workstations, crafting skills and classes, ingredients, recipes, and failure/limit rules for Dungeon Crawler Carl Books 1-8; {tot[0]} rows plus {xt[0]} conflict/gap rows, each with a quote (<=25 words), source tag and confidence.

Spoilers through Book 8. Built {DATE} from `raw/pages/` (Fandom mirror), `sources/fanwiki/` and `sources/youtube/` only. **Nothing here was checked against the novels' text**; "VERIFIED" is the ledger's bookkeeping label (wiki sentence/page carries a book-chapter cite, or two independent source families agree), as defined in `ledger-rules.md`. All quotes are exact substrings of the cited local file (checked by `tools/ledger_check.py`). Mirrors section 10 (Crafting) of `CANON-LEDGER.md` (IDs `K-001...`, conflicts `X-C01...`).

Column notes: *Quote 2 / Source 2* appear only where a second source backs the row (a different source family makes the row VERIFIED even without a chapter cite). `B1 ch10` = Book 1, chapter 10 as cited by the wiki. Tag `W:` = Fandom wiki page, `FW2:` = generated fan wiki, `YT:` = YouTube recap auto-caption (names may be garbled).

Counts: {tot[0]} crafting rows = {tot[1]} VERIFIED, {tot[2]} WIKI-ONLY, {tot[3]} UNVERIFIED; {xt[0]} conflict/gap rows (flagged separately).

"""
tail="""## Coverage notes and gaps
- Tables with real data: Engineer's, Sapper's, Alchemy, Armorer's, Metal Working, Bolt-Thrower's, Makeup, Automaton, Advanced Bomber's Studio (a room). Writing Table, Printing Press, Repair Bench and Tinker's Table are only named (one line in the Crafting overview).
- No local page defines Cooking, Smithing, Enchanting or Scribe as stations or skills (see X-C10). Enchanted gear appears as loot; the only table-linked enchanting fact is that an Armorer's Workshop at level 1 cannot add enchantments.
- Donut and Bautista have no crafting skill pages locally. Donut's crafting role is coupons/potion use; Bautista's tea is treated as a potion (Book 8). Katia, Mordecai, Rosetta and Milk appear with crafting-related facts.
- Page-level wiki cites are not chapter-by-chapter confirmations; cross-check against the novels before using a figure at the table.
"""
doc=head+quick+'\n'+body+tail
open(_os.path.join(_LORE, 'catalog/crafting-canon.md'),'w').write(doc)
# ledger block
lead=f"""

## 10. Crafting (added {DATE}, Pass 5; prefix K-, conflicts X-C)

Source: `catalog/crafting-canon.md` (same rows). IDs `K-001`..`K-{n:03d}` (next free: K-{n+1:03d}); conflict/gap rows `X-C01`..`X-C{xn:02d}` (next free: X-C{xn+1:02d}); the `X-` series in section 8 is untouched. Counts: {tot[0]} crafting rows = {tot[1]} VERIFIED, {tot[2]} WIKI-ONLY, {tot[3]} UNVERIFIED; {xt[0]} conflict/gap rows. VERIFIED here = chapter cite on the wiki page/sentence or two source families; not checked against the novels.

"""
led=lead
for k in secs:
    led+=f"### 10.{list(secs).index(k)+1} {secs[k]}\n\n"+HDR+"\n"+'\n'.join(r[3] for r in rows[k])+"\n\n"
open(_os.path.join(_LORE, 'work/crafting-ledger-block.md'),'w').write(led)
print(tot,xt,n,xn)
