import sys,re,os,collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parent))
from paths import LORE_ROOT
from wk import *
OUT=str(LORE_ROOT/'catalog'); os.makedirs(OUT,exist_ok=True)
def isredir(v): return v.lstrip().lower().startswith('#redirect')
def pg(cat,exclude=()):
    r=[]
    for k,v in sorted(D.items()):
        if isredir(v): continue
        cs=cats(v)
        if cat in cs and not any(e in cs for e in exclude): r.append(k)
    return r
def esc(s): return s.replace('|','/').replace('\n',' ')
def short(s,n=160):
    s=clean(s) if s else ''
    s=re.sub(r'\[B\d+ ch[^\]]*\]','',s); s=re.sub(r'\[\d+\]','',s).strip()
    if len(s)>n:
        cut=s[:n];k=max(cut.rfind('; '),cut.rfind(', '),cut.rfind(' '));s=cut[:k]+'…'
    return s
def sp(v):
    s=spoil(v);return f'B{s}' if s else '-'
def name(k):
    return re.sub(r'\s*(Achievement|Skill|Spell|Class|Benefit|Box|Potion)$','',k) if False else k
def refs(v):
    c=cites(v)
    if not c:return '?'
    bs=books(v); return ','.join('B%d'%b for b in bs)
def uns(f,flags):
    return ' **[UNVERIFIED: '+', '.join(flags)+']**' if flags else ''
USED=set()
HDR="> Source: Fandom wiki mirror (raw/all.json) condensed by script + hand-checked structure; paraphrased/condensed, not book text. `Bk` = books whose chapter citations appear on the wiki page. `Spoil` = wiki spoiler-gate book. Wiki-only claims are **unverified against the books** unless noted.\n\n"
w=lambda fn,s: open(f'{OUT}/{fn}','w').write(s)


# master list from Achievement page
def norm(n): return re.sub(r"[^a-z0-9]","",n.lower().replace('’',"'").replace(' achievement',''))
MASTER={}
_cur=None;_floor=''
for line in D['Achievement'].split('\n'):
    m=re.match(r'^=== (Floor \d+) ===',line)
    if m: _floor=m.group(1);continue
    m=re.match(r'^==== (.+?) ====',line)
    if m: _cur=clean(m.group(1)).strip();MASTER[_cur]={'floor':_floor,'reward':'','n':norm(_cur)};continue
    if _cur and line.startswith('Reward:') and not MASTER[_cur]['reward']:
        r=clean(line[7:]);r=re.sub(r"^You[’']?ve (received|earned|been (given|awarded))( an?| the)? ",'',r).strip(' !.')
        MASTER[_cur]['reward']=short(r,110) if re.search(r'\b(Box|box|Patch|Coupon|Potion|Nothing|None|none)\b',r) else '(narration reward) '+short(r,60)
MBY={v['n']:(k,v) for k,v in MASTER.items()}

# ---------- achievements
ach_all=pg('Achievements'); NOTE_PAGES=[k for k in ach_all if re.match(r'^Floor \d+ Achievements$',k) or k in ('Achievement','Good Shit Box')]
ach=[k for k in ach_all if k not in NOTE_PAGES]
rows=[];flags=0
for k in ach:
    v=D[k];nm,f=info(v,{'achievement'})
    if not f: nm,f=info(v,{'item'})
    fl=clean(f.get('floor','')); tr=short(f.get('for',''),150); rw=short(f.get('reward',''),130)
    ld=short(lead(v,260),200) if not tr else ''
    if not tr: tr=ld
    tr=re.sub(r'^(The )?.{0,60}? (Achievement )?(is|are) (an? )?(achievement )?(that is )?(awarded|given|earned)( to| for| by)?( \w+)?( for)? ','',tr) if tr==ld else tr
    if not rw:
        mm=re.search(r"(?:received|receive|awarded) (?:a|an|the)? ?((?:Bronze|Silver|Gold|Platinum|Legendary|Celestial)[^!.<\n]{0,60}?)(?:!|\.|\n|<)",clean(v))
        if mm: rw=short(mm.group(1),90)+' (from page text)'
    nt=''
    mk=MBY.get(norm(k))
    if mk:
        if (not fl) and mk[1]['floor']: fl=mk[1]['floor']+' (master list)'
        if (not rw or rw.endswith('(from page text)')) and mk[1]['reward']: rw=mk[1]['reward']+' (master list)'
    if not f.get('for') or not f.get('reward'): nt='infobox incomplete [UNVERIFIED]';flags+=1
    rows.append(f"| {esc(k.replace(' Achievement',''))} | {esc(fl) or '?'} | {esc(tr)} | {esc(rw) or '?'} | {refs(v)} | {sp(v)} | {nt} |")
    USED.add(k)
w('achievements.md',f"# Achievements catalog ({len(ach)} entries)\n\n"+HDR+"Achievements: System-AI notifications that reward (usually with loot boxes), mock, or warn crawlers for specific actions; a few give specific items, temporary classes, or nothing at all. Tutorial floors (1-3) hand them out densely and generically; they become much rarer from Floor 4 [B1 ch12, per wiki]. Box tiers: Bronze < Silver < Gold < Platinum < Legendary < Celestial (see `loot-boxes.md`). Reaching base 100 in a stat also triggers an achievement + a choice of permanent upgrade (see `benefits-and-status-effects.md`). The wiki's own count is ~160 (161 category members: {len(ach)} true achievement pages here + {len(NOTE_PAGES)} index/hub pages listed in the footer); pages with incomplete infoboxes are flagged.\n\n| Achievement | Floor | Trigger (condensed) | Reward | Bk | Spoil | Notes |\n|---|---|---|---|---|---|---|\n"+'\n'.join(rows)+'\n\n## Non-entry pages in the Achievements category\n'+'\n'.join(f'- {k}' for k in NOTE_PAGES)+'\n')
pagenames={norm(k) for k in ach}
missing=[(k,v) for k,v in MASTER.items() if v['n'] not in pagenames]
mrows=[f"| {esc(k)} | {v['floor']} | {esc(v['reward']) or '?'} |" for k,v in missing]
open(f'{OUT}/achievements.md','a').write(f"\n## Master-list entries with no own wiki page ({len(missing)}) - from the wiki 'Achievement' page (title + floor + reward only)\nThe master list has {len(MASTER)} headed entries in total. Triggers for these are not captured here (the wiki text is AI narration, not summarized in this pass).\n\n| Achievement | Floor | Reward (condensed) |\n|---|---|---|\n"+'\n'.join(mrows)+'\n')
print('ach',len(ach),flags,'master',len(MASTER),'missing',len(missing))

# ---------- spells
def spellrow(k):
    v=D[k];nm,f=info(v,{'spells'})
    if not f: nm,f=info(v,{'item'})
    eff=short(f.get('effect') or f.get('effects') or lead(v,260),170)
    return f"| {esc(k)} | {esc(short(f.get('cost',''),50)) or '?'} | {esc(short(f.get('casting',''),40)) or '-'} | {esc(short(f.get('cooldown',''),40)) or '-'} | {esc(short(f.get('target',''),40)) or '-'} | {esc(short(f.get('duration',''),40)) or '-'} | {esc(eff)} | {esc(short(f.get('users',''),60)) or '-'} | {refs(v)} | {sp(v)} |"
sps=pg('Spells'); skl=[k for k in pg('Skills') if k not in sps]
w('spells.md',f"# Spells catalog ({len(sps)} pages)\n\n"+HDR+"Spells come from spellbooks, scrolls, classes and floor/level rewards; mana pool is roughly equal to Intelligence, and Int also sets regen and spell/scroll effectiveness. Leveling a spell scales it (see mechanics.md §Magic). Blank `?` = infobox field missing on wiki (**[UNVERIFIED]**).\n\n| Spell | Cost | Cast | CD | Target | Duration | Effect (condensed) | Users | Bk | Spoil |\n|---|---|---|---|---|---|---|---|---|---|\n"+'\n'.join(spellrow(k) for k in sps)+'\n')
w('skills.md',f"# Skills catalog ({len(skl)} pages)\n\n"+HDR+"Skills are non-magical talents that level up through use (levels roughly 1-10 easy, then slow). Each Earth-hobby/profession can generate a skill. Skills differ from Benefits (not levelable) and Stats. Some skills have cost/cooldown (active); others passive.\n\n| Skill | Cost | Cast | CD | Target | Duration | Effect (condensed) | Users | Bk | Spoil |\n|---|---|---|---|---|---|---|---|---|---|\n"+'\n'.join(spellrow(k) for k in skl)+'\n')
USED.update(sps);USED.update(skl);print('sp',len(sps),len(skl))

# ---------- loot boxes
lb=pg('Loot Boxes')
rows=[]
for k in lb:
    v=D[k];nm,f=info(v,{'item'})
    ld=short(lead(v,300),210)
    m=re.search(r'==\s*Loot\s*==\s*(.*?)(?=\n==|\Z)',v,flags=re.S)
    loot=''
    if m:
        items=[clean(x) for x in re.findall(r'^\*+\s*(.+)$',m.group(1),flags=re.M)]
        items=[re.sub(r'\[B\d+ ch[^\]]*\]','',x).strip() for x in items]
        loot='; '.join(items)[:260]
    rows.append(f"| {esc(k)} | {esc(short(f.get('source',''),70)) or '?'} | {esc(short(f.get('effects',''),100)) or '-'} | {esc(ld)} | {esc(loot) or '-'} | {refs(v)} | {sp(v)} |")
    USED.add(k)
w('loot-boxes.md',f"# Loot boxes catalog ({len(lb)} pages)\n\n"+HDR+"""## Tiers & general rules (condensed from wiki; **[UNVERIFIED]** where noted)
- Dozens of box types, each in six tiers: Bronze, Silver, Gold, Platinum, Legendary, Celestial. Higher tier = rarer and stronger contents (Bronze mostly junk; most patrons can only afford Silver/Gold).
- Sources: achievements, boss kills (Boss Boxes scale with boss rank: Bronze for Neighborhood Boss, Silver for Borough Boss, and so on up the ladder; see mechanics.md), quests (Quest Boxes), and gifts from viewers/patrons (Fan Boxes, Benefactor Boxes). Benefactor Boxes are the exception to "theme-appropriate loot": they may hold off-world tech; even a Bronze Benefactor Box outclasses a Gold Adventurer Box [per wiki, B1 ch4].
- Loot is "semi-random": may be truly random or hand-picked by the System AI to help/hurt ratings. Drops key off the crawler's *race*, not class (wiki, B1 ch7).
- Operation: boxes sit locked in the inventory "Awards and Boxes" tab until the crawler is in a Safe Room / guildhall; opening is all-or-nothing, in tier order. Boxes never drop outright cursed gear but can drop unstable/dangerous items, so read item descriptions first.
- The host company reportedly owes the Syndicate a tax on the tier of non-sponsored boxes, explaining Celestial rarity [wiki, B2 epilogue] **[UNVERIFIED against text]**.
- Contents below are only observed drops recorded by the wiki, not a drop table. Drop-rate math is not established in canon.

| Box | Source | Effect field | Description (condensed) | Observed loot (sample) | Bk | Spoil |
|---|---|---|---|---|---|---|
"""+'\n'.join(rows)+'\n')
print('lb',len(lb))

# ---------- classes
cl=pg('Classes')
rows=[];seen=set()
for k in cl:
    v=D[k];nm,f=info(v,{'class'})
    ld=short(lead(v,300),200)
    rows.append(f"| {esc(k.replace(' Class',''))} | {esc(short(f.get('type',''),40)) or '?'} | {esc(short(f.get('subclass_of',''),40)) or '-'} | {esc(short(f.get('crawlers',''),70)) or '-'} | {esc(short(f.get('stats',''),80)) or '-'} | {esc(short(f.get('skills',''),90)) or '-'} | {esc(short(f.get('effects',''),90)) or '-'} | {esc(short(f.get('prerequisites',''),50)) or '-'} | {esc(ld)} | {refs(v)} | {sp(v)} |")
    seen.add(k.replace(' Class','').lower()); USED.add(k)
# list table
lt=D['List of Classes']
rows2=[]
for row in lt.split('\n|-'):
    cells=[c.strip() for c in re.split(r'\n\s*\|',row.strip().lstrip('|').strip())]
    cells=[c for c in cells]
    if not cells or 'Class' not in cells[0]: continue
    m=re.search(r'\{\{[Cc]ite\|(\d+)\|([^}]*)\}\}',cells[0])
    c0=re.sub(r'\{\{[Cc]ite[^}]*\}\}','',cells[0])
    c0=clean(c0); n=re.sub(r'\s*Class\s*$','',c0).strip()
    if not n or n.lower() in seen or n=='Class' or 'Wiki note' in n: continue
    rest=[clean(c.lstrip('| ')) for c in cells[1:]]
    rest=(rest+['','',''])[:3]
    fs=(f"B{m.group(1)} ch{m.group(2)}" if m.group(2).isdigit() else f"B{m.group(1)} {m.group(2)}") if m else '?'
    rows2.append(f"| {esc(n)} | {esc(rest[0]) or '?'} | {esc(rest[1]) or '-'} | {esc(rest[2][:140]) or '-'} | {fs} |")
w('classes.md',f"# Classes catalog\n\n"+HDR+f"""## How classes work (condensed, wiki-based)
- Primary class is chosen on the Third Floor (after race, before stat spending). The System AI prepares 30+ options per crawler from stats, race, Desperado Club membership, certain gear and tutorial choices, and recommends three based only on skills [wiki, B1 ch47, B2 ch1].
- Perks: new skills/spells, ability to train skills/spells past level 15, XP or mana buffs/debuffs, status immunities, stat bonuses/penalties, club membership, benefits. Earth Classes (inspired by Earth culture) come with a Silver Earth Box containing an Earth Hobby Potion (random level-3 hobby skill).
- Specialization: flagged classes choose a subclass on Floor 6 (ten-minute timer, no chat); some re-specialize on Floors 9 and 12. Classes that cannot specialize pick one of three 'endorsements' instead (name unchanged). Nobody has done more than three specializations ('four seasons' build). [wiki, B5 ch1, ch8]
- Examples: Carl = Compensated Anarchist (Monk/Rogue hybrid) → Agent Provocateur on F6; Donut = Former Child Actor (rotating specialty classes: Artist Alley Mogul, Football Hooligan, Glass Cannon, Legendary Diva, Viper Queen, Master Telephone Psychic...) and later The Oak Fell (B7). Temporary classes can come from wearing certain corpses (e.g. Fursuiter, B8).
- ~40,000 distinct classes were reported chosen in the current season [Cascadia quote, B2 ch7].

## Part A: classes with their own wiki page / infobox ({len(rows)})
| Class | Type | Subclass of | Crawlers | Stats | Skills | Effects | Prereq | Description (condensed) | Bk | Spoil |
|---|---|---|---|---|---|---|---|---|---|---|
"""+'\n'.join(rows)+f"""

## Part B: classes only listed in the wiki's "List of Classes" table ({len(rows2)}, through Book 7 per wiki note)
| Class | Type | Crawlers | Notes | First seen |
|---|---|---|---|---|
"""+'\n'.join(rows2)+'\n')
print('cl',len(rows),len(rows2))
USED.add('List of Classes')

# ---------- races
rc=pg('Races')
def flat(x,n=120): return esc(short(x,n)) or '-'
rows=[]
for k in rc:
    v=D[k];nm,f=info(v,{'race infobox'})
    cs=cats(v)
    grp=[g for g in ['Crawler Races','Syndicate Races','Aliens','Mob Types'] if g in cs]
    rows.append(f"| {esc(k)} | {'/'.join(grp) or '-'} | {flat(f.get('type'),50)} | {flat(f.get('floors'),50)} | {flat(f.get('bonuses'),90)} | {flat(f.get('penalties'),90)} | {flat(f.get('deities'),40)} | {esc(short(lead(v,260),180))} | {refs(v)} | {sp(v)} |")
    USED.add(k)
w('races.md',f"# Races catalog ({len(rc)} pages)\n\n"+HDR+"""## Notes
- Race selection happens on the Third Floor, in the Tutorial Guild Hall, before class and stat allocation. The System AI recommends three races out of potentially hundreds; options are roughly balanced (bonuses/penalties net about ten points, or the race carries a skill bonus, racial spell or a benefit like night vision). About 80% keep their original race; a big change means being dissolved into goo and rebuilt over minutes/hours [wiki, B2 ch1-2, ch7]. Ledger rows: CANON-LEDGER.md section 11 (R-025..R-081); summary in `race-selection-canon.md`. Per-race rows: Grulke R-045/046, Crocodilian R-047, Lajabless R-049, Nodling R-050, Vampire R-051, Tigran R-053, Cat Girl R-054, Changeling R-056, Doppelgänger R-058, Hobgoblin R-059, Half-Djinn R-060, Frost Maiden R-061, Caprid R-062, Dog Soldier R-063, Curupira R-064, Amazonian R-065, Igneous R-066, Cretin R-067, Cat R-068, Naga R-069, Human R-070, Elf R-071, Dwarf R-072, Half Elf R-073, Fairy R-074, Primal R-075, Sasquatch R-076.
- Many pages here are not playable: they are Syndicate/alien species or mob types ('Group' column).
- `-` means field blank on wiki (not necessarily absent in canon).

| Race | Group | Type | Floors | Bonuses | Penalties | Deities | Description (condensed) | Bk | Spoil |
|---|---|---|---|---|---|---|---|---|---|
"""+'\n'.join(rows)+'\n')
print('rc',len(rc))

# ---------- benefits / status effects / potions / quests
bn=[k for k in pg('Benefits') if k not in ('Benefit','Benefits')]; se=pg('Status Effects')
def simple(k,keys):
    v=D[k];nm,f=info(v,keys)
    eff=short(f.get('effect') or f.get('effects') or lead(v,260),170)
    return f,eff
rows=[]
for k in bn:
    v=D[k];f,eff=simple(k,{'spells','item'});rows.append(f"| {esc(k)} | {esc(eff)} | {flat(f.get('users'),70)} | {flat(f.get('associated equipment'),60)} | {refs(v)} | {sp(v)} |");USED.add(k)
rows_se=[]
for k in se:
    v=D[k];nm,f=info(v,{'status effects','item'})
    eff=short(f.get('effect') or f.get('effects') or lead(v,260),170)
    rows_se.append(f"| {esc(k)} | {flat(f.get('type'),30)} | {esc(eff)} | {flat(f.get('causes'),90)} | {flat(f.get('duration'),40)} | {refs(v)} | {sp(v)} |");USED.add(k)
w('benefits-and-status-effects.md',f"# Benefits ({len(bn)}) and Status Effects ({len(se)})\n\n"+HDR+"Benefits: static traits that cannot be leveled (unlike skills/spells), attached to a class or enchanted item. Status effects: buffs/debuffs; stacking rules not formally established **[UNVERIFIED]**. At base 100 in a stat, the crawler gets an achievement and 3 minutes to pick one of three permanent upgrades (one always doubles future gains in that stat; e.g. Swole for Strength) [wiki, B5 ch36].\n\n## Benefits\n| Benefit | Effect | Users | Equipment | Bk | Spoil |\n|---|---|---|---|---|---|\n"+'\n'.join(rows)+"\n\n## Status effects (buffs, debuffs, conditions)\n| Effect | Type | Effect (condensed) | Causes | Duration | Bk | Spoil |\n|---|---|---|---|---|---|---|\n"+'\n'.join(rows_se)+'\n')
print('bn',len(bn),len(se))

# ---------- items
it=[k for k in pg('Items') if k not in USED]
pot=[k for k in it if 'Potions' in cats(D[k])]
it2=[k for k in it if k not in pot]
def itemrow(k):
    v=D[k];nm,f=info(v,{'item','spells'})
    eff=short(f.get('effects') or f.get('effect') or lead(v,260),170)
    return f"| {esc(k)} | {flat(f.get('type'),40)} | {esc(eff)} | {flat(f.get('source'),60)} | {flat(f.get('buy'),20)} | {refs(v)} | {sp(v)} |"
hdr="| Item | Type | Effect (condensed) | Source | Buy | Bk | Spoil |\n|---|---|---|---|---|---|---|\n"
w('items.md',f"# Items catalog ({len(it2)} items) and potions ({len(pot)})\n\n"+HDR+"Items = gear, consumables, artifacts, crafting mats, vehicles... Named enchanted gear typically carries Benefits and stat bonuses; Craftable via Crafting/Midnight Market; see `loot-boxes.md` for boxes and `benefits-and-status-effects.md`.\n\n## Potions\n"+hdr+'\n'.join(itemrow(k) for k in pot)+"\n\n## Other items\n"+hdr+'\n'.join(itemrow(k) for k in it2)+'\n')
USED.update(it)
print('items',len(it2),len(pot))

# quests
qs=pg('Quests'); rows=[]
for k in qs:
    v=D[k];nm,f=info(v,{'quest'})
    rows.append(f"| {esc(k)} | {esc(short(lead(v,300),220))} | {refs(v)} | {sp(v)} |")
w('quests.md',f"# Quests catalog ({len(qs)})\n\n"+HDR+"| Quest | Description (condensed) | Bk | Spoil |\n|---|---|---|---|\n"+'\n'.join(rows)+'\n')
print('qs',len(qs))

# ---------- floors data & bosses
order=['First','Second','Third','Fourth','Fifth','Sixth','Seventh','Eighth','Ninth','Tenth','Eleventh','Twelfth','Thirteenth','Fourteenth','Fifteenth','Sixteenth','Seventeenth','Eighteenth']
def lst(x,n=260):
    items=[clean(i) for i in re.findall(r'^\*+\s*(.+)$',x or '',flags=re.M)]
    items=[re.sub(r'\[B\d+ ch[^\]]*\]','',i).strip() for i in items]
    s='; '.join(i for i in items if i)
    return s[:n]+('…' if len(s)>n else '')
rows=[]
for o in order:
    k=f'{o} Floor'
    if k not in D: continue
    v=D[k];nm,f=info(v,{'dungeon floor'})
    t=re.search(r'DISPLAYTITLE:([^}]*)',v)
    rows.append(f"### {k}: {esc(clean(f.get('title1','')) or (t.group(1) if t else ''))}\n- Spoil gate: {sp(v)}; books cited: {refs(v)}\n- Theme: {esc(short(f.get('theme',''),100)) or '?'}; duration: {esc(short(f.get('duration',''),40)) or '?'}; start date: {esc(short(f.get('start_date',''),30)) or '?'}\n- Crawlers: {esc(short(f.get('crawlers',''),40)) or '?'}; crawler levels: {esc(short(f.get('crawler_levels',''),40)) or '?'}; mob levels: {esc(short(f.get('mob_levels',''),40)) or '?'}; exits/survivors-through: {esc(short(f.get('exits',''),40)) or '?'}\n- Bosses: {lst(f.get('bosses')) or '?'}\n- Quests: {lst(f.get('quests')) or '?'}\n- Locations: {lst(f.get('locations'),300) or '?'}\n- Notable mobs: {lst(f.get('mobs'),300) or '?'}\n")
w('floor-data.md',"# Per-floor data sheet (Floors 1-18)\n\n"+HDR+"Numbers (crawler counts, level ranges, exits) come straight from the wiki's floor infoboxes; blank = `?`. Floors 12+ are partly or fully speculative/stub **[UNVERIFIED]**. Narrative summaries live in `floors-and-plot-by-book.md`.\n\n"+'\n'.join(rows))
print('floors',len(rows))

# bosses
tier_re=re.compile(r"[Ll]evel (\d+) ((?:Elite )?(?:Neighborhood|Borough|City|Province|Country|Floor|Dungeon|Planetary|World|Region)?\s?Boss)")
bossnames=[k for k in pg('Bosses') if k not in ('Boss','Crawler Cards')]
rows=[]
for k in bossnames:
    v=D[k]; ct=clean(v)
    m=tier_re.search(ct)
    nm,f=info(v,{'character info','race infobox'})
    lv=f.get('level') and clean(f['level']) or (m.group(1) if m else '?')
    tr=m.group(2) if m else '?'
    flr=clean(f.get('floors') or f.get('first_appearance') or '') or '?'
    ab='; '.join(x for x in [clean(f.get('skills','')),clean(f.get('spells','')),clean(f.get('bonuses','')),clean(f.get('weapon',''))] if x)
    wk=clean(f.get('penalties','')) 
    rows.append(f"| {esc(k)} | {esc(lv)} | {esc(tr)} | {esc(flr[:50])} | {esc(short(f.get('species') or f.get('type') or '',40)) or '-'} | {esc(short(ab,200)) or '-'} | {esc(short(wk,160)) or '-'} | {esc(short(lead(v,300),200))} | {refs(v)} | {sp(v)} |")
w('bosses.md',"# Boss stat blocks (wiki-derived, 41 boss-category pages + tier legend)\n\n"+HDR+"""## Boss tier ladder (levels seen in wiki text)
Order (Fandom 'Boss' page, r/dungeoncrawlercarl threads, dungeoncrawlercarl.nl): Neighborhood < Borough < City < Province < Country < Floor < Dungeon (only Scolopendra, lvl 500, is a Dungeon Boss so far). Levels seen: Neighborhood ~7-19 early (65 later); Borough ~15-65; City ~80-140 (Asojano 130, Shi Maria 140); Country e.g. Imogen 145; Province e.g. Prison Pocket 170; Floor e.g. 235. **Level is not a reliable proxy for tier** (Province 170 vs Country 145 above; Reddit users note mechanics/immunities matter more). Boss Box tier climbs with boss tier (Bronze for Neighborhood, Silver for Borough, up to Celestial for Floor boss, per mechanics.md §Bosses). Exact full-stat blocks (STR/INT/etc.) are rarely given in canon; most bosses are given level, tier, name and a short AI blurb. Where a column says `?`, the wiki page had no data **[UNVERIFIED]**.

| Boss | Lvl | Tier | Floor | Species/type | Abilities/skills/spells/notes | Weaknesses/constraints | Description (condensed) | Bk | Spoil |
|---|---|---|---|---|---|---|---|---|---|
"""+'\n'.join(rows)+'\n')
print('bosses',len(rows))

# unnamed achievements from hub pages
un=[]
for k in sorted(D):
    if re.match(r'^Floor \d+ Achievements$',k):
        for row in D[k].split('|-')[1:]:
            cells=[c.strip() for c in re.split(r'\n\|',row.strip().lstrip('|'))]
            if len(cells)>=3 and cells[0].upper().startswith('N/A'):
                un.append(f"| {k.replace(' Achievements','')} | {esc(short(cells[1],120))} | {esc(short(cells[2],80))} |")
open(f'{OUT}/achievements.md','a').write(f"\n## Unnamed ('N/A') achievements listed on the per-floor hub pages ({len(un)})\n| Floor | For | Reward |\n|---|---|---|\n"+'\n'.join(un)+'\n')
print('unnamed',len(un))

import apply_headers; apply_headers.main()  # keep convention headers after regeneration
