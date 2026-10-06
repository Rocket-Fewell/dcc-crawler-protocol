#!/usr/bin/env python3
"""Ledger Pass 33 (2026-10-05): clubs (Desperado Club, Club Vanquisher) and Personal Spaces / Bopca pricing.
Builds rows, verifies every quote with the same normalisation as tools/ledger_check.py, writes work/pass33/block.md.
Do not re-run after the block is appended."""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parents[2] / 'tools'))
from ledger_lib import *
DC='W:Desperado Club'; CV='W:Club Vanquisher'; PS='W:Personal Space'; BO='W:Bopca'
DP='W:Desperado Pass Tattoo'; DD='W:Destruction of the Desperado Club'; Y3='YT:FHLzs9fjyU8'
D='2026-10-05'
rows=[
# (topic, fact, quote, source, confidence)
('Desperado/Vanquisher exclusivity','Holding a Desperado Pass blocks a Vanquisher pass (the two clubs never share members under normal rules).',"obtaining a Desperado Pass automatically negates a crawler's ability to earn a Vanquisher pass",DC,'VERIFIED (cite B1 ch19)'),
('Desperado Pass sources','The pass tattoo comes from an Asshole\'s Box (usually for horrific deeds) or a first Player-Killer Skull.',"may be received in an Asshole's Box and/or after a crawler earns their first Player-Killer Skull",DP,'VERIFIED (cite B1 ch19, B3 ch25)'),
('Desperado front room','The first room is a town pub any local can enter without a pass.',"…public pub open to any local of the specific town; no Desperado Pass is required to enter it",DC,'VERIFIED (cite B2 ch15)'),
('Desperado front-room quests','Pass-less crawlers can take quests in the front pub to earn the tattoo.',"crawlers without access can pick up quests here to win themselves the tattoo",DC,'VERIFIED (cite B2 ch15)'),
('Desperado pocket dimension','Every club door on a floor opens into the same shared room, like a guild hall.',"the moment a crawler enters, they are in the same room as everyone in every club location across the entire floor",DC,'VERIFIED (cite B2 ch15)'),
('Desperado no fast travel','You always leave by the door you came in, so the club is not a teleport network.',"exiting always returns a crawler to the door they came in through, so the club cannot be used for fast travel",DC,'VERIFIED (cite B2 ch15)'),
('Desperado main room not safe','The dance floor is not a safe room; crawlers can be hurt there (Ji-Hoon backstab, T-058).',"The main room is not a safe room, and crawlers can be injured within it.",DC,'VERIFIED (cite B2 ch15)'),
('Desperado bot crowd','The club always looks like ~200 people; generated bots fill gaps and vanish as real patrons arrive.',"the club maintains the appearance of roughly 200 people at all times, backfilling with bots",DC,'VERIFIED (cite B2 ch15)'),
('Desperado pets','Pets are banned inside; familiars go to a playroom with no safety guarantee.',"for familiars whose safety is not guaranteed",DC,'VERIFIED (cite B2 ch14, B8 ch85)'),
('Desperado level unlocks','Three internal levels: top from Floor 3, Hunting Grounds from Floor 6, Larracos from Floor 9; entry is always on top.',"Crawlers always enter on the top level.",DC,'VERIFIED (cite B3 ch9)'),
('Desperado Jobs room','Jobs room hands out rogue gigs: NPC assassination and theft quests.',"a room offering rogue-themed gigs such as NPC assassination and theft quests",DC,'VERIFIED (cite B2 ch15)'),
('Desperado Silk Road','The Silk Road market sells supplies, magic gear and potions (Pustule shop K-099).',"a marketplace selling supplies, magical gear, and potions",DC,'VERIFIED (cite B2 ch15)'),
('Desperado Guild-O-Rama','Rogue guild hallway; specialised guilds (Dodge, Lockpicking, Sleight of Hand) unlock deeper.',"more specialized guilds (such as Dodge, Lockpicking, and Sleight of Hand) open as crawlers descend the floors",DC,'VERIFIED (cite B2 ch15, B3 ch9)'),
('Desperado Pharmacist','A dealer sells addictive substances such as blitz sticks.',"a drug dealer, originally Quint, offering addictive substances such as blitz sticks",DC,'VERIFIED (cite B2 ch15)'),
('Desperado casino unlock','The casino opens on Floor 4, not Floor 3.',"The Casino — opens on the Fourth Floor.",DC,'VERIFIED (cite B2 ch15, B3 ch9)'),
('Desperado Wheel of Fortune','The vertical wheel mixes big prizes with brutal punishments (stabbing, vomiting blood). Nothing! trapdoor is M-182.',"The wheel mixes lucrative prizes with brutal punishments, such as being stabbed by the croupier",DC,'VERIFIED (cite B3 ch9)'),
('Desperado privacy bubble','A hand-circle gesture makes a privacy bubble that dims the music so a group can talk.',"wave their hand in a circle to form a basic privacy bubble that dims the pounding music to background level",DC,'VERIFIED (cite B2 ch15)'),
('Desperado privacy bubble pop','Poking the bubble pops it and the volume returns.',"Poking the bubble pops it, restoring the full volume.",DC,'VERIFIED (cite B2 ch15)'),
('Desperado private security price','From Floor 4: two bodyguards, 300 gold per crawler or 500 for a pair, per visit (recap: level-35 rock-monster guards Bomo and The Sledge).',"offers private security for 300 gold per crawler or 500 gold for a pair, per visit",DC+'; '+Y3,'VERIFIED (cite B3 ch8; 2 sources)'),
('Desperado security comp','Spend more than the fee at the tables and the next visit\'s security is free.',"if a crawler spends more than that at the tables, the next visit's security is free",DC,'VERIFIED (cite B3 ch8)'),
('Desperado security failure refund','Recap: after an assassin breach, Astrid refunded Carl and granted free security from then on.',"Astrid arrives, apologizes for the security failure, refunds Carl's money and grants them free security from now on",Y3,'WIKI-ONLY (recap transcript, auto-captions)'),
('Desperado exterior varies','Outside look matches the local floor; inside layout stays the same everywhere.',"adapting its exterior architecture to match the local environment while maintaining a consistent internal layout",DC,'VERIFIED (cite B2 ch15, B5 ch5)'),
('Iron Tangle club doors','Floor 4: Desperado doors at transfer stations ending in 1, Vanquisher at stations ending in 9.',"on the Iron Tangle it can be found at any transfer station whose number ends in a 1",DC,'VERIFIED (cite B3 ch6, ch8)'),
('Club blood bar','Floor 6+ blood bar: a full bar is needed to enter a club, but it does not drain inside.',"A crawler needs a full blood bar to enter, but the bar does not drain while inside, the same as the Desperado Club.",CV,'VERIFIED (cite B7 ch46)'),
('Club evacuation','After catastrophic damage the System ran a 15-minute evacuation timer and shut the club for remodeling.',"the system initiated a 15-minute evacuation timer, temporarily closing the club for remodeling",DD,'VERIFIED (cite B6 ch34)'),
('Vanquisher shared portal','Every Vanquisher entrance on a floor leads into one shared members-only club.',"every entrance on a floor is a portal into the same shared, members-only club",CV,'VERIFIED (cite B2 ch15)'),
('Vanquisher entrances','Doors hide in ordinary-looking temples, each watched by a ram-headed cleric.',"Entrances to the club are concealed within seemingly ordinary local temples and church-like buildings, each guarded by a ram-headed cleric.",CV,'VERIFIED (cite B3 ch6, ch10)'),
('Vanquisher ring','Membership is shown by a Club Vanquisher ring (Desperado uses a tattoo).',"Membership is marked by a Club Vanquisher ring.",CV,'VERIFIED (cite B4 ch2)'),
('Vanquisher Holy Crusade Bounty','Defiling or disrupting the club puts a Holy Crusade Bounty on you.',"draws a \"Holy Crusade Bounty\" on the offender's head",CV,'VERIFIED (cite B4 ch25)'),
('Vanquisher Emberus exception','Emberus adherents get free entry regardless of club affiliation, overriding the Desperado lockout.',"an adherent of the fire god Emberus is granted free access to Club Vanquisher regardless of any previous or current club affiliation",CV,'VERIFIED (cite B4 ch32)'),
('Vanquisher single-entrance bubble','Floor 5 bubbles each have one entrance; destroy it and that bubble loses the club.',"if that entrance is destroyed, the bubble loses access to Club Vanquisher entirely",CV,'VERIFIED (cite B4 ch33)'),
('Vanquisher healers','Members can hire healers through the club (Floor 6).',"Crawlers with access can hire healers through the club.",CV,'VERIFIED (cite B5 ch6)'),
('Vanquisher bard dual access','Some bard classes reportedly get into both clubs (hedged; see X-085).',"A few bard classes are said to grant dual access to both clubs.",CV,'UNVERIFIED (source hedges: "said to")'),
('Vanquisher deity day pass','Deity-granted visitors get a one-location day pass declared in advance, no refreshments, cleric or paid-guard escort.',"issued a single day pass covering one location inside per day, which must be stated in advance on a request form",CV,'VERIFIED (cite B6 ch18, ch56)'),
('Vanquisher church loan','Big enchanting jobs (~1M gold) can be fronted by your church as an interest-free loan; you cannot renounce until repaid.',"a worshipper's own church may cover the balance as an interest-free loan",CV,'VERIFIED (cite B6 ch56)'),
('Vanquisher demon lockdown','Detected demonic activity triggers an alarm, dead temple portals and guard aura protections.',"When demonic activity is detected, the club enters a lockdown: an alarm sounds, the temple portals stop functioning",CV,'VERIFIED (cite B7 ch51, ch52)'),
('Personal Space start floor','Personal Spaces can be bought or acquired from Floor 4 on.',"a crawler can purchase or acquire starting on the fourth floor of the World Dungeon",PS,'VERIFIED (cite B3 ch2)'),
('Personal Space price','List price is usually ~40,000 gold; this season it starts at 50,000.',"the price usually starts around 40,000 gold, though for the current dungeon it had risen to a 50,000-gold starting price",PS,'VERIFIED (cite B3 ch2)'),
('Bopca haggle floor','About 25% haggle room (37,500 on a 50,000 space); the System blocks any lower sale.',"about 25% of wiggle room (down to 37,500 gold on a 50,000-gold space), and the system will not allow a sale below that floor",PS,'VERIFIED (cite B3 ch2)'),
('Bopca covers shortfall','A Bopca talked below the floor pays the difference personally.',"A proprietor talked below the floor must personally cover the difference.",PS,'VERIFIED (cite B3 ch2)'),
('Bopca incentives','Bopcas are rewarded for selling (next-floor location pick, food budget), not by the price.',"rewards such as earlier location selection on the next floor or a larger food budget",PS,'VERIFIED (cite B3 ch2)'),
('Negotiation XP from Bopca','Talking a Bopca down grants extra Negotiation skill experience.',"Crawlers receive extra skill experience if they can talk a Bopca down.",BO,'VERIFIED (cite B3 ch2)'),
('Bopca info limits','Bopcas cannot discuss the dungeon\'s finer points but can explain Safe Rooms and Personal Spaces.',"they can share information about Safe Rooms and Personal Spaces",BO,'VERIFIED (cite B1 ch10)'),
('Bopca newsletter','Bopcas have no newsfeed; they get a physical newsletter after each episode.',"They do not have access to the newsfeed, and instead receive a physical newsletter after each episode",BO,'VERIFIED (cite B2 ch8)'),
('Personal Space safe rules','Safe-room rules apply inside: attacking mobs are teleported away; crawler violence and theft are forbidden.',"any mob that attacks is instantly teleported away, and violence or theft between crawlers is strictly forbidden",PS,'VERIFIED (cite B1 ch20)'),
('Personal Space joining fee','Merging spaces into a communal one costs 5,000 gold per union.',"carries a joining fee of 5,000 gold per union",PS,'VERIFIED (cite B3 ch2)'),
('Personal Space merge levels','Same party required, one space must be level 3; two level-3s make level 4, three make level 5.',"two level-three spaces make a level 4, and three make a level 5",PS,'VERIFIED (cite B3 ch2, ch3)'),
('Personal Space level 1','Level 1 is one open room about a quarter the size of level 5, with a five-table crafting studio; too small for a Training Room.',"Roughly a fourth the size of a level-five space",PS,'VERIFIED (cite B3 ch3)'),
('Personal Space level 2','Level 2 is a larger room that unlocks kitchen upgrades.',"A larger room that unlocks kitchen upgrades.",PS,'VERIFIED (cite B3 ch3)'),
('Personal Space level 5 manager','Level 5 adds a manager\'s room; level 4 differs only by lacking it.',"The only known difference from a level 5 is the absence of a dedicated manager's room.",PS,'VERIFIED (cite B3 ch3)'),
('Personal Space whitelist','Spaces are private; others enter only if an owner whitelists them.',"other crawlers cannot enter unless a space owner whitelists them",PS,'VERIFIED (cite B3 ch21)'),
('Personal Space whitelist level','A level-4 communal hall cannot whitelist outside visitors; level 5 can.',"a level-four communal space cannot whitelist outside visitors",PS,'VERIFIED (cite B3 ch21)'),
('Personal Space vestibule','With access to several spaces, the exit opens into a generated vestibule with one door per space.',"lined with a separate door for each space that crawler is allowed to enter",PS,'VERIFIED (cite B3 ch21)'),
('Quest upgrade prices','Quest category: Quest Screen 90,000; Adventurer\'s, Inc. 100,000; invite-only Naughty Boys Employment Agency 500,000.',"a Quest Screen (90,000 gold), the Adventurer's, Inc. Employment Agency (100,000 gold), and the invite-only Naughty Boys Employment Agency (500,000 gold)",PS,'VERIFIED (cite B3 ch2)'),
('Social Screen price','Social Screen upgrade costs 50,000 gold.',"Social -- a Social Screen (50,000 gold)",PS,'VERIFIED (cite B3 ch2)'),
('Cleaner Bot price','Cleaner Bot (flying scrubber) is one of the cheapest upgrades at 25,000 gold.',"at 25,000 gold it is one of the cheapest upgrades available",PS,'VERIFIED (cite B3 ch30)'),
('Ultra-Stabilized Sleep Apparatus','Top tier-one bed: full rest after two hours of sleep.',"the Ultra-Stabilized Sleep Apparatus, which grants full rest after only two hours of sleep",PS,'VERIFIED (cite B3 ch2)'),
('Instacot 60','Tier-two bed: full refresh after 60 seconds; upgrades Good Rest to Great Rest (+15% stats).',"upgrades the Good Rest buff to Great Rest for a 15% stat bonus",PS,'VERIFIED (cite B5 ch21)'),
('Shrine in Personal Space','A religious shrine a crawler takes on also appears in their space (Carl\'s Emberus sun shrine).',"Any religious shrine a crawler takes on also appears inside their personal space.",PS,'VERIFIED (cite B4 ch32)'),
('Guild upgrade sharing','From Floor 6 the guild system shares Personal Space upgrades without a shared party.',"the guild system lets crawlers share personal-space upgrades without having to join the same party",PS,'VERIFIED (cite B4 ch33)'),
]
def clean(t): return norm_ws(strip_cites(t)).replace('\u200b','')
bad=0; out=[]
n=766
for topic,fact,q,src,conf in rows:
    core=norm_ws(q).strip('… ').strip()
    words=len(core.split())
    texts=[clean(src_text(s.strip())) for s in src.split(';') if src_text(s.strip())]
    ok=any(core in t for t in texts)
    if words>25 or not ok:
        bad+=1; print('BAD',n,words,ok,q[:80])
    qq=q.replace('|','\\|')
    out.append(f'| M-{n:03d} | {topic} | {fact} | "{qq}" | {src} | {conf} | {D} |'); n+=1
print('rows',len(rows),'bad',bad,'last',f'M-{n-1}')
open(Path(__file__).parent/'block.md','w').write('\n'.join(out)+'\n')
