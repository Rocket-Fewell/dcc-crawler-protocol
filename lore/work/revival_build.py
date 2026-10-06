import os as _os
_LORE = _os.environ.get('DCC_LORE_ROOT') or _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
import sys,re
sys.path.insert(0,_os.path.join(_LORE, 'work'))
import revival_rows as R
D='2026-10-03'
def c(s): return str(s).replace('|','\\|').replace('\n',' ').strip()
def q(s): return '"'+c(s)+'"'
def strip_web(tag):
    parts=[t.strip() for t in tag.split(';')]
    return '; '.join(t for t in parts if not t.startswith('WEB:'))
XC=[ # conflicts: id, topic, A, srcA, B, srcB, status
('X-RV1','Cockroach: chapter cite for the Desperado Club save (Ji-Hoon)',
 q("Donut's Cockroach skill absorbed a killing blow during a night out at the Desperado Club"),'W:Health (cite B3 ch2)',
 q("Donut uses this skill to survive Ji-Hoon's attack at the Desperado Club."),'W:Cockroach Skill (cite B3 ch8)',
 'PREFERRED B (B3 ch8): Health page cite looks off; B3 summary puts the Desperado fight at ch8. Health page also gives B2 ch1 for the class pick where the Cockroach page gives B2 ch2.'),
('X-RV2','Potion of Half Splat: scope (any fatal blow, or falling damage only)',
 q("cancelling what would otherwise be a fatal impact and leaving the drinker at five percent"),'W:Health (cite B5 ch46)',
 q("a potion that prevents you from dying from falling damage but leaves you at 5% health"),'W:Potion of Half Splat (no cite)',
 'PREFERRED B: falling damage only. Health page wording ("fatal impact") is loose. Earlier lore notes saying half-splat "cancels a fatal impact" were corrected; it is NOT a general death cancel. A Reddit OP recalled Mordecai saying it keeps full health: UNVERIFIED, thread unreadable (403).'),
('X-RV3','Hellspawn Familiar route (death + soul protection, or a biscuit)',
 q("The soul becomes hellbound and tainted and then shoved back into the resurrected body of the pet"),'W:Hellspawn Familiar (cite B2 ch14)',
 q("she consumed an Enhanced Pet Biscuit and was transformed into a horse-sized Hellspawn Familiar."),'W:Bianca (no cite)',
 'OPEN: the death-and-rebirth route is described for the race; Bianca is described as transformed by a biscuit with no death. Treat the rebirth as a possible race route only.'),
('X-RV4','Second Chance: "resurrected" or temporary undead minion (Olga)',
 q("Olga's corpse is now driving, having been resurrected by Donut's Second Chance spell."),'W:Book 8 Chapter Summaries (B8 ch48)',
 q("will fight on the caster's side for a number of minutes equal to the spell's level."),'W:Second Chance Spell (cite B1 ch30-32)',
 'PREFERRED B: a timed undead minion, not a revival. Wiki "resurrected" is loose wording.'),
('X-RV5','Second Chance duration',
 q("the duration increases to two minutes per spell level, with a max of approximately 10 minutes."),'W:Second Chance Spell (Level 5 text)',
 q("At Spell Level 10, the spell resurrects creatures up to 10 levels higher than the caster for a maximum of 15 minutes."),'W:Second Chance Spell (Level 10 text)',
 'OPEN: L1 = minutes equal to spell level; L5 = 2 min/level (max ~10); L7 = 14 min; L10 = max 15 min. The L5 and L10 caps are not obviously consistent (L7 already hits 14). Do not state one cap as fact.'),
]
def tabrow(cells): return '| '+' | '.join(cells)+' |'

# ---------------- catalog ----------------
out=[]
w=out.append
w('# Revival, Resurrection and Death-Cheat Canon (Books 1-8)')
w(f'Owner: DCC Lore | Status: review | Version: 1.0 | Updated: {D}')
w('Summary: Every way in the local sources that a dead character or creature came back, regenerated, was reborn, or had death cancelled or cheated (Books 1-8, Book 9 hints), plus lookalikes and no-revival rules. Each row has an exact short quote, source tag and confidence. Spoilers through Book 8.')
w('')
w('## 0. How to read this file')
w('- **Nothing here was checked against the novels\' text.** Sources are the Fandom wiki mirror (`raw/pages/`), the fan-wiki-2 mirror, and YouTube recap transcripts (`sources/youtube/`) kept in this folder. VERIFIED is a bookkeeping label, not proof from the books.')
w('- **Confidence**: VERIFIED = the wiki row carries a book-chapter cite (or two independent source families agree); WIKI-ONLY = one wiki source with no cite; UNVERIFIED = anything else (single recap, speculation, a claim never shown to be true). Rules: `ledger-rules.md`.')
w('- Quotes are exact substrings of the cited local source (<=25 words). Source tags: `W:<wiki page>`, `FW2:<file>`, `YT:<video id>`; `WEB:` tags point to excerpts saved in `sources/web/revival-web-snippets.txt` (web-only facts, not ledger-quotable).')
w('- "ch" cites are the wiki\'s `[book|chapter]` cites. Where pages disagree the conflict is listed in section 7.')
w('')
w('## 1. Key findings')
w('- **True death reversal in the crawl is rare and always tied to a mechanism**: pet-race regeneration (Tummy Acher: Garret/Rend), nodling split-rebirth (Popov twins), contract regeneration for hired mercenaries and team-wide regeneration (Team Retribution), NPC key-holder immortality (Growler Gary), Grimaldi\'s vine, Mrs. Ghazi\'s sand, and divine resurrections via the Celestial Thorn Room (Yemaya, Eileithyia\'s retainers; Nekhebit is called "resurrected" with no mechanism given).')
w('- **Ordinary crawlers do not come back.** Carl notes the Cookbook has no case of the Dungeon reviving dead crawlers (B6 ch47). Dead crawlers become cards; dead gods leave memorial crystals; the Dungeon sells no "resurrection" product found in the mirror.')
w('- **Donut\'s Cockroach skill is a death-cheat, not a revival.** L5: one guaranteed free lethal hit per fight, leaving her near death; L10: the first fatal strike costs no health. It trains by use only (Mordecai). Costs: no XP/loot for that fight. Five on-page triggers are listed (RV-21..26). No potion that trains Cockroach or cancels death was found in the mirror.')
w('- **Potion of Half Splat prevents death from FALLING damage only** (Half Splat page), leaves the drinker at 5% health. It is not a general "cancel any fatal blow" (an earlier note implying that was wrong and has been corrected in `mechanics.md` / `parts/m1.md`). Carl, Donut and Katia got three each from a Silver Skydiver\'s Box in B4 ch13 (web chapter summaries; `Carl_Inventory`). The Health page cites B5 ch46 for the effect but words it loosely.')
w('- **Dolores Doesn\'t Splat (B4 ch12)** works only when falling at 200 km/h or more: five bounces, brief invulnerability, pain remains. Mordecai brewed the potions for the gnome-dreadnaught assault (wiki cite B4 ch10); naming the batch "Dolores" is chapter-summaries.com only.')
w('- **Mordecai\'s Special Brew** is ~30 seconds of de facto Immortality (Gold Standard healing + Troll\'s Second Wind), ~10 h potion sickness; fails against instant kills; never revives. Used on Carl vs Grull (B3 ch33), Louis (B7 ch84).')
w('- **Mordecai-brewed potions found**: Special Brew and Superb CON buff (B3 ch7), Rapid Detox (B4 ch5), the B4 assault potions, Revitalize Pet (B7 ch2); Heal Critter (B2 ch12) was Carl brewing under Mordecai\'s guidance. **None cancels death after the fact; none trains Cockroach.** See RV-29..37 and section 6.')
w('- **Reanimation is not revival.** Donut\'s Second Chance makes a temporary undead minion (1/3 level, minutes = spell level). Remex, Boned, Legionnaires, Zerzura, Raise Bootlicker, Resurrect totems and zombie/ghoul mechanics are all in section 4.')
w('- **Desperado Club/Pass**: no revival or cheat feature. Donut\'s Cockroach save there is incidental (RV-23).')
w('- **Book 9**: the prologue and ch1-2 are on Patreon with no release date; no revival content verified. Open B8 threads: Ysalte via Britney, Juice Box dumped in Sheol, the Scolopendra Club guests, the Apito crystal anomaly, Taranis holding Samantha.')
w('')
H='| ID | Name | Type | What it does | Cost / limits | Who / book-chapter | Quote (<=25 words) | Source tag | Confidence |'
S='|---|---|---|---|---|---|---|---|---|'
def sect(title,rows,intro=None):
    w(f'## {title}')
    if intro: w(intro); w('')
    w(H); w(S)
    for r in rows:
        w(tabrow([c(r[0]),c(r[1]),c(r[2]),c(r[3]),c(r[4]),c(r[5]),q(r[6]),c(r[7]),c(r[8])]))
    w('')
sect('2. True revival, regeneration and rebirth',R.A,'Dead character comes back (or is guaranteed to) by a stated mechanism.')
sect('3. Death cheats and prevention (no return from death)',R.B,'Death is prevented, delayed or cancelled before it lands. Includes the Cockroach, Special Brew, Dolores and Half Splat rows requested in the steering note.')
sect('4. Reanimation and undead (not revival)',R.C,'The body or spirit is made to act again; the person is not restored.')
sect('5. Soul and body mechanics',R.D,'Context mechanics that touch death; none restores a dead crawler.')
w('## 6. Potion cross-check: what Mordecai made, and whether any cancels death or trains Cockroach')
w('| Potion | Made by / book-chapter | Effect | Cancels death? | Trains Cockroach? | Row | Confidence |')
w('|---|---|---|---|---|---|---|')
for r in [
 ('Heal Critter Potion','Carl under Mordecai\'s guidance, B2 ch12','heals pets (Mongo); pet-class only','No (healing, patient was alive)','No','LK-01','VERIFIED (cite B2 ch12)'),
 ('Superb Constitution Buff','Mordecai, B3 ch7','temporary CON boost','No','No','RV-29 (same table session)','VERIFIED (cite B3 ch7)'),
 ('Special Brew','Mordecai, B3 ch7','~30 s de facto Immortality, ~10 h sickness, 2 doses','Only prevents lethal damage while active; not instant kills; not after death','No','RV-29..33','VERIFIED (cite B3 ch7, 33; B7 ch84)'),
 ('Rapid Detox','Mordecai, B4 ch5','purges toxins','No','No','(see Mordecai page)','VERIFIED (cite B4 ch5)'),
 ('B4 assault jump potions (Dolores Doesn\'t Splat)','Mordecai brewed (cite B4 ch10); potion named in ch12','survive a fall at >=200 km/h, 5 bounces','Prevents splat death only, pain remains','No','RV-34/35','VERIFIED (cite B4 ch10/12); batch naming WEB-ONLY'),
 ('Potion of Half Splat','Loot (Silver Skydiver\'s Box, B4 ch13); not shown as Mordecai-made','prevents death from falling damage, leaves 5%','Falling damage only','No','RV-36/37','VERIFIED (cite B5 ch46, Health page); acquisition WEB/inventory'),
 ('Revitalize Pet','Mordecai, B7 ch2','pet-class heal','No','No','LK-02','VERIFIED (cite B7 ch2)'),
]: w(tabrow([c(x) for x in r]))
w('')
w('No Cockroach-training potion exists in the mirror: Mordecai says the only way to train the skill is by using it (RV-20), and the Cockroach and Skill-potion pages list no such potion. (Pawna\'s Tears and general skill-training potions exist, but no on-page use on Cockroach was found.)')
w('')
w('## 7. Open conflicts and unverified points')
w('| ID | Topic | Reading A | Source A | Reading B | Source B | Status |')
w('|---|---|---|---|---|---|---|')
for x in XC: w(tabrow([c(x[0]),c(x[1]),x[2],c(x[3]),x[4],c(x[5]),c(x[6])]))
w('')
w('Other unverified points: Ysalte\'s return via crystal/plinth is only Samantha\'s claim (RV-14); how Nekhebit was resurrected is not stated (RV-13); Orthrus\' Special Brew slingshot rests on one recap (RV-32); the memorial-crystal "phylactery" idea is wiki speculation (RV-75); a generated fan wiki says Cockroach later reached L15 on Donut (WEB-only; the card form is L15, RV-27); Bubble Beluga raised by Second Chance (B4 ch23) is WEB-only.')
w('')
w('## 8. Things that look like revival but are not')
w('| ID | Name | Looks like | What it really is | Quote (<=25 words) | Source tag | Confidence |')
w('|---|---|---|---|---|---|---|')
for r in R.LOOK: w(tabrow([c(r[0]),c(r[1]),c(r[2]),c(r[3]),q(r[4]),c(r[5]),c(r[6])]))
w('')
w('## 9. No-revival rules in canon (permadeath rules)')
w('| ID | Rule | Quote (<=25 words) | Source tag | Confidence |')
w('|---|---|---|---|---|')
for r in R.NOREV: w(tabrow([c(r[0]),c(r[1]),q(r[2]),c(r[3]),c(r[4])]))
w('')
w('## 10. Searched and not found (local mirror)')
w('- Zero hits for "Neuron(s)", "Soul Stone", phoenix, ankh, "raise dead". "Phylactery" appears only as wiki speculation (RV-75).')
w('- No product, spell or loot box that revives an ordinary dead crawler. No potion that trains Cockroach. No revival feature in the Desperado Club or Pass.')
w('- Yarilo, Geyrun and Khnum: no resurrection shown (fan-wiki, WEB-only; see `sources/web/revival-web-snippets.txt`).')
w('- Book 9: nothing verified (Patreon text was not read).')
w('')
w('## 11. Sources and method')
w('- Full-text search of `raw/pages/*.txt`, `sources/fan-wiki-2/`, and the transcripts in `sources/youtube/` for revival terms (resurrect, revive, regenerate, reborn, undead, raise, zombie, immortal, invulnerable, splat, Cockroach, Second Chance, memorial/soul crystal and similar).')
w('- Web: chapter-summaries.com (B4), Storiluna (B4 ch13), Mana Toast B2 recap, a generated fan wiki (Yarilo/Geyrun/Donut), Book 9 pages; excerpts saved in `sources/web/revival-web-snippets.txt`. Reddit returned 403 and counts as snippets only.')
w('- Quotes checked by `work/revival_check.py` and `tools/ledger_check.py`.')
w('- Ledger-ready block: `catalog/revival-ledger-block.md` (NOT yet appended to `CANON-LEDGER.md`).')
open(_os.path.join(_LORE, 'catalog/revival-canon.md'),'w').write('\n'.join(out)+'\n')

# ---------------- ledger block ----------------
L=[];a=L.append
a('# Revival Ledger Block (ready to append)')
a(f'Owner: DCC Lore | Status: review | Version: 1.0 | Updated: {D}')
a('Summary: Ready-to-append rows for CANON-LEDGER.md covering revival, death-cheat and no-revival findings (from catalog/revival-canon.md). Not appended; CANON-LEDGER.md is untouched.')
a('')
a('## How to use')
a('- Append each table body to the matching ledger section (2 mechanics, 7 plot beats, 8 conflicts) and the Pass-log line to section 9. **Re-check the tail of each section first**: the IDs below start at M-046, T-050, X-026 (as of the Pass 4 rules file) and may need renumbering if another worker has appended since. Internal "RV-/LK-/NR-" references point to `catalog/revival-canon.md`.')
a('- Every quote was checked against its local source tag. Web-only facts (Dolores batch naming, Half Splat acquisition, Bubble Beluga, fan-wiki Cockroach L15) are intentionally left out of the ledger rows.')
a('')
mech=[];plot=[]
ids=[]
for grp in (R.A,R.B,R.C,R.D):
    for r in grp: ids.append(('RV',r))
for r in R.LOOK: ids.append(('LK',r))
for r in R.NOREV: ids.append(('NR',r))
mn=46; tn=50
def conf_clean(s): return c(s)
for kind,r in ids:
    if kind=='RV':
        rid,name,typ,what,lim,who,quote,tag,conf=r
        tag=strip_web(tag)
        if not tag: continue
        if typ.startswith('event'):
            plot.append((rid,who,f'{name}: {what}',quote,tag,conf))
        else:
            mech.append((rid,f'[{rid}] {name}: {what} Limits: {lim}',quote,tag,conf))
    elif kind=='LK':
        rid,name,looks,real,limit,quote_,tag_ = (r[0],r[1],r[2],r[3],None,r[4],r[5]); conf=r[6]
        mech.append((rid,f'[{rid}] NOT a revival: {name} ("{looks}"): {real}',quote_,tag_,conf))
    else:
        rid,rule,quote,tag,conf=r
        mech.append((rid,f'[{rid}] No-revival rule: {rule}',quote,tag,conf))
a('## For section 2 (Mechanics rulings)')
a('| ID | Ruling | Source quote | Source | Confidence | Date |')
a('|---|---|---|---|---|---|')
for i,(rid,txt,quote,tag,conf) in enumerate(mech):
    a(tabrow([f'M-{mn+i:03d}',c(txt),q(quote),c(tag),c(conf),D]))
mlast=mn+len(mech)-1
a('')
a('## For section 7 (Plot beats)')
a('| ID | Book / chapter | Beat | quote | Source | Confidence | Date |')
a('|---|---|---|---|---|---|---|')
for i,(rid,who,beat,quote,tag,conf) in enumerate(plot):
    a(tabrow([f'T-{tn+i:03d}',c(who),c(f'[{rid}] '+beat),q(quote),c(tag),c(conf),D]))
a('')
a('## For section 8 (Conflicts / Unverified)')
a('| ID | Topic | Reading A | Source A | Reading B | Source B | Status | Date |')
a('|---|---|---|---|---|---|---|---|')
for i,x in enumerate(XC):
    a(tabrow([f'X-{26+i:03d}',c(x[1]),x[2],c(x[3]),x[4],c(x[5]),c(x[6]),D]))
a('')
a('## For section 9 (Pass log)')
a('| Date | Pass | Who | Summary |')
a('|---|---|---|---|')
a(f'| {D} | 5 | DCC Lore | Revival/death-cheat research: M-046..M-{mlast:03d}, T-050..T-{tn+len(plot)-1:03d}, X-026..X-030 appended from catalog/revival-canon.md. Corrects Half Splat scope (falling damage only). |')
a('')
a(f'Also update the ledger header (Updated/Version) and the "next free ID" table in `ledger-rules.md`: M next M-{mlast+1:03d}, T next T-{tn+len(plot):03d}, X next X-031.')
open(_os.path.join(_LORE, 'catalog/revival-ledger-block.md'),'w').write('\n'.join(L)+'\n')
print(len(mech),len(plot),len(XC))
