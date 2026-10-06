#!/usr/bin/env python3
"""Ledger Pass 34 (2026-10-06): quest system rules, quest boxes and the Floor 3 quests (plus the two later quests named in TODO 55).
Builds rows, verifies every quote with the same normalisation as tools/ledger_check.py, writes work/pass34/block.md.
Do not re-run after the block is appended."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parents[2] / 'tools'))
from ledger_lib import *
Q='W:Quest'; QB='W:Quest Box'; SM='W:Show Must Go On Quest'; FB='W:Fools Who Broke the Glass Quest'
SW='W:Sex Workers Who Fell from the Heavens Quest'; VS='W:Vengeance of the Daughter'; VQ='W:Vengeance of the Daughter Quest'
WS='W:Where the Sidewalk Ends Quest'
D='2026-10-06'
rows=[
# --- 9.8a quest system basics
('Quest tab unlock','The Quests tab of the crawler interface first unlocks on Floor 3 (confirms M-718).',"tracked in a dedicated tab of the crawler interface that unlocks on the third floor",Q,'VERIFIED (cite B2 ch4)'),
('Quests pay XP and loot','Quests are a main source of experience and loot.',"They are a primary source of experience and loot.",Q,'VERIFIED (cite B2 ch7)'),
('Quest announcement staging','A new quest lands with a trumpet chime, illusion streamers and title-card text in midair.',"announced with a trumpet chime, illusionary streamers, and text that slams into place in midair like a title card",Q,'VERIFIED (cite B2 ch4)'),
('Quest text shape','Every quest reads the same way: AI-voice flavor paragraph, a plain objective, then a Reward line.',"a flavor paragraph in the AI's voice, a plainly worded objective, and a Reward line naming the payout",Q,'VERIFIED (cite B2 ch4)'),
('Quest triggers','Most quests fire from the crawler\'s own actions or location, such as walking into a district with a running storyline.',"Most quests trigger on a crawler's own actions or location, such as entering a district where a storyline is already running.",Q,'VERIFIED (cite B2 ch4)'),
('NPC-given quests','NPC quests come face to face, usually from desperate pub locals, and are usually low-value busywork.',"handed out face to face by NPCs, most often by desperate locals in pubs, and tend to be low-value busywork",Q,'VERIFIED (cite B2 ch14)'),
('Quest-giver star','Quest-givers sometimes show a star over their minimap dot, but not always.',"quest-givers sometimes carry a star over their minimap icon, though not every quest is flagged that way",Q,'VERIFIED (cite B2 ch14)'),
('Quest map markers','Objectives, targets and destinations are often marked on the map.',"Objectives, targets, and destinations are frequently marked on the crawler's map.",Q,'VERIFIED (cite B2 ch24)'),
('Quest Update','A Quest Update can rewrite an active quest in place, redirecting the goal and resetting its clock.',"A Quest Update can revise an active quest in place, redirecting the original objective and resetting its clock.",Q,'VERIFIED (cite B2 ch25)'),
('Event quest saferoom lockout','In a floor-wide event quest crawlers get a short window to reach a saferoom; then saferooms in the zone lock until it ends.',"crawlers are given a brief window to reach a saferoom, after which saferoom access inside the quest zone is shut off until the event concludes",Q,'VERIFIED (cite B2 ch24)'),
('Quest Chat','Event quests open a temporary Quest Chat listing every participant.',"a temporary Quest Chat channel opens listing every participant",Q,'VERIFIED (cite B2 ch24)'),
('Johnny Quest map perk','Completing a first quest alive (A-065) makes new quest locations sometimes appear on the map.',"new quest locations will sometimes appear on your map",Q,'VERIFIED (cite B2 ch13)'),
('Pass or fail quests','A pass-or-fail quest states its failure condition up front and stays live only while its trigger holds (e.g. staying aboard a train).',"A pass or fail quest names its failure condition in the quest text and stays active only while its trigger condition holds",Q,'VERIFIED (cite B3 ch12)'),
('Solving before issue','Solving a quest before the AI issues it gives Premature Questjaculation and forfeits the box (adds a chapter cite to WIKI-ONLY row A-095).',"A quest can be resolved before it is ever issued, which earns the Premature Questjaculation achievement and forfeits the box",Q,'VERIFIED (cite B5 ch28)'),
('Option-menu quests','Some quests offer a numbered menu of outcomes, each with its own reward line.',"Some quests are presented as a numbered menu of options, each with its own reward line",Q,'VERIFIED (cite B6 ch62)'),
# --- 9.8b quest types
('Individual quests','Individual quests go to one crawler only.',"Individual Quests are issued to a single crawler rather than to a party or a wider body of crawlers.",Q,'VERIFIED (page cite B4 ch32)'),
('Individual via god','A quest can be individual because it comes from a god only that crawler worships.',"A quest may be individual because it comes from a god only that crawler worships",Q,'VERIFIED (cite B4 ch32)'),
('Escort quests','Escort quests ask for safe delivery of a creature, not a kill.',"Escort quests are a recognized variant, tasking a crawler with delivering a creature safely to a destination rather than killing anything.",Q,'VERIFIED (cite B6 ch26)'),
('Party quests','Party quests go to every party member at once.',"Party Quests are issued to every member of a party at once.",Q,'VERIFIED (page cite B2 ch4)'),
('Pub quests are party quests','Pub NPC quests are usually party quests, often fetch or kill errands.',"Quests taken from NPCs in pubs are generally party quests",Q,'VERIFIED (cite B2 ch14)'),
('Group quests: host party','Group quests name a host party that cannot opt out and open a shared quest chat.',"They designate a host party that is explicitly barred from opting out, and open a shared quest chat listing every participant",Q,'VERIFIED (cite B2 ch24)'),
('Regional quests','Regional quests cover every crawler in a set area of the floor, between group and world scale, with a host squad that cannot withdraw.',"covering every crawler inside a defined geographic area of the floor rather than a blast radius or the entire level",Q,'VERIFIED (cite B6 ch62)'),
('World quests','World quests go to every crawler on the floor and affect the whole floor.',"World Quests are issued to every crawler on a floor and affect the floor as a whole.",Q,'VERIFIED (cite B4 ch30)'),
('World quests can be PvP','World quests are not always cooperative and may have no shared chat (Get Orthrus bounty).',"They are not always cooperative and do not always come with a communications channel",Q,'VERIFIED (cite B4 ch30)'),
('Mandatory quests','Mandatory quests cannot be declined, ignored or deferred (Floor 10 race tracks).',"Mandatory Quests cannot be declined, ignored, or deferred.",Q,'VERIFIED (cite B8 ch43)'),
('Church quests required','A god\'s worshippers must complete all its church quests.',"Adherents of a god are required to complete all church quests as a condition of worship",Q,'VERIFIED (cite B4 ch32)'),
('Deity quest voice','Deity quests speak in the god\'s voice, not the System\'s.',"deity quests arrive in the god's own voice rather than the system's",Q,'VERIFIED (cite B4 ch32)'),
('Non-patron deity quests','A god you do not worship can still quest you; it warns you may refuse but the god may resent it.',"These arrive with an explicit warning that the crawler is not required to complete them, but that the god may take the refusal poorly.",Q,'VERIFIED (cite B6 ch17)'),
# --- 9.8c rewards, boxes, failure
('Box tier = difficulty','Quest box tier follows the quest\'s difficulty, not the crawler\'s level.',"Tier tracks the difficulty of the quest rather than the crawler who completes it.",QB,'VERIFIED (cite B2 ch14)'),
('Silver quest tier','Silver boxes go to small local jobs (e.g. investigating NPC deaths).',"Silver: smaller local objectives, such as investigating a string of NPC deaths.",QB,'VERIFIED (cite B2 ch14)'),
('Gold quest tier','Gold boxes go to larger floor quests with elites and a city boss.',"Gold: larger floor quests involving elites and a city boss.",QB,'VERIFIED (cite B2 ch4)'),
('Platinum quest tier','Platinum boxes go to high-stakes and event quests (one held 5,000 gold plus two items).',"Platinum: high-stakes and event quests; one held 5,000 gold coins plus two further items.",QB,'VERIFIED (cite B2 ch13)'),
('Bronze quest tier','Bronze boxes exist for minor errands; the ladder runs bronze up through platinum.',"Boxes run from bronze on minor errands up through platinum on major ones",Q,'VERIFIED (cite B4 ch15)'),
('Legendary quest tier','A Legendary quest tier exists, first promised on Floor 8 (Hell Comes to Crawler Town).',"A Legendary tier also exists, first promised for the Hell Comes to Crawler Town Quest on the Eighth Floor.",QB,'VERIFIED (cite B6 ch54)'),
('XP often the bigger prize','XP often outweighs the box; Carl gained three levels from his first quest.',"Experience is frequently the larger prize, and Carl gained three levels on completing his first quest.",Q,'VERIFIED (cite B2 ch11)'),
('Group quest payout','Group quests give every qualifying participant a full box of the stated tier; no splitting.',"Group quests pay a box of the stated tier to every qualifying participant rather than splitting a single prize.",QB,'VERIFIED (cite B2 ch24)'),
('Showrunner veto','A promised box can be appealed in Syndicate court or voided by the host company\'s single seasonal veto, and then nothing arrives.',"a host company may spend its single seasonal veto to reverse one, in which case nothing is delivered at all",QB,'VERIFIED (cite B2 Epilogue)'),
('Hadji repeatable','Hadji (A-048) raises a quest box one tier and can be earned more than once.',"The Hadji achievement raises a box one tier and can be awarded more than once.",QB,'VERIFIED (cite B2 ch13)'),
('Hadji/Bandit patched out','Bandit (A-004) raised boxes two tiers; both upgrade achievements were patched out after the mass Celestial payout.',"Both were disabled by patch after they produced a mass Celestial payout.",QB,'VERIFIED (cite B2 Epilogue)'),
('CockBlock repeat penalty','CockBlock (A-020) works once; doing it again names you to the victim, who gets a quest to hunt you.',"a crawler who does it again is identified to the aggrieved party, who is then issued a quest to hunt them down",Q,'VERIFIED (cite B2 ch22)'),
('Failed by someone else','A quest can fail through no fault of its holder, e.g. another crawler kills the NPC you were freeing.',"Carl's quest to free a captive gnome failed the moment an unrelated crawler killed the gnome in front of him",Q,'VERIFIED (cite B4 ch6)'),
('Divine quest failure','Failing or abandoning a divine quest brings a smite (M-162).',"failing or abandoning one results in a smite",Q,'VERIFIED (cite B4 ch32)'),
('World quest failure','Failing a world quest can rewrite the floor\'s rules (Floor 6: blood-bar saferoom timing, Gehenna Bramble).',"Failing a world quest rewrote the rules of the entire sixth floor",Q,'VERIFIED (cite B5 ch52)'),
('Reward = next quest','A quest\'s only reward can be another quest.',"a quest's stated reward may be nothing more than another quest",QB,'VERIFIED (cite B4 ch30)'),
('Race-wide charisma reward','One quest added a permanent 50% charisma bonus toward a whole race on top of its box.',"One quest added a permanent fifty percent charisma bonus toward an entire race on top of its box.",Q,'VERIFIED (cite B4 ch10)'),
('Quest box opening','Quest boxes follow normal loot-box rules: open only in a safe area.',"a crawler may only open them inside a safe area",QB,'VERIFIED (cite B1 ch5)'),
# --- 9.8d dungeon lore (how quests are made)
('Elite quests are shows','Any quest with an Elite belongs to a produced show with writers.',"any quest involving an elite belongs to a show with its own writers and producers",Q,'VERIFIED (cite B2 ch7)'),
('Storyline runs anyway','A show storyline plays out whether or not a crawler joins.',"the storyline will play out whether or not a crawler participates",Q,'VERIFIED (cite B2 ch7)'),
('Mordecai on quests','Mordecai: only quest when comfortably ahead of the difficulty curve; otherwise grind.',"quests are worth doing only when a crawler is comfortably ahead of the difficulty curve",Q,'VERIFIED (cite B2 ch7)'),
('Dense quests from short timers','Mordecai read the elaborate Floor 3 quests as showrunners packing content into cut timers.',"He considered the increasingly elaborate quests of the third floor a symptom of compressed floor timers",Q,'VERIFIED (cite B2 ch21)'),
('Quests replay','Quest scenarios reset and replay for later crawlers (Levi the 7th).',"Quest scenarios reset and replay for successive crawlers",Q,'VERIFIED (cite B3 ch12)'),
('Reactive quest generation','An unstable AI makes quests from what crawlers say aloud (Herot\'s cookbook note).',"an unstable AI generates quests reactively from what crawlers say out loud",Q,'VERIFIED (cite B6 ch38)'),
('Quest as private channel','A goddess issued a trivial quest just to open a message thread the System could not monitor.',"the goddess Eileithyia issued a trivial spider-killing quest purely to open a message thread the system was not permitted to monitor",Q,'VERIFIED (cite B6 ch17)'),
('Box tier formula (speculation)','Wiki speculation only: box tier may come from a difficulty formula, so the reward previews the true scale.',"Box tier may be set by a difficulty formula rather than by a show's writers",Q,'UNVERIFIED (wiki Speculation section)'),
# --- 9.8e Floor 3 quests and the two later quests from TODO 55
('Show Must Go On objective','Floor 3 first quest: find out why the cursed circus still exists and end it; Gold box.',"Find out why this circus still exists and put an end to its reign of terror.",SM,'VERIFIED (cite B2 ch4)'),
('Show Must Go On upgrade','Carl and Donut solved it unusually, so Hadji upgraded both boxes to Platinum.',"Completing it in an unusual way triggered the Hadji Achievement for both of them, upgrading each box to Platinum.",QB,'VERIFIED (cite B2 ch13)'),
('Show Must Go On deal','Carl bargained with the show\'s production team, trading future cooperation for survival.',"Carl negotiated directly with the production team behind it and traded future cooperation for his own survival",Q,'VERIFIED (cite B2 ch11)'),
('Signet circus raids','Show backdrop: Signet raids the circus nightly to kill Grimaldi and free the transformed troupe.',"she assaults the circus every night in the hopes of reaching Ringmaster Grimaldi and killing him, which would free the monsters",VS,'VERIFIED (cite B2 ch8)'),
('Sex Workers quest','GumGum\'s Floor 3 village murder mystery: new bodies each morning; Silver box.',"Nobody knows who they are or where they come from. Find out why.",SW,'VERIFIED (cite B2 ch14)'),
('Fools Who Broke the Glass reach','Group quest to every crawler inside a 45 sq km blast radius; Princess Donut\'s party hosts.',"All Crawlers currently within the 45 square kilometer blast radius will receive this quest.",FB,'WIKI-ONLY'),
('Fools saferoom window','Opt-out is a 60-second dash to a saferoom; then zone saferooms lock (matches M-835).',"you will have sixty seconds from the end of this message to get yourselves into a saferoom",FB,'WIKI-ONLY'),
('Fools NPC and mob fate','NPCs who stay indoors, saferoom or not, are safe from the blast.',"All NPCs who remain indoors, saferoom or not, will remain safe.",FB,'WIKI-ONLY'),
('Fools mob wipe','Mobs and neighborhood-level bosses caught in the blast are killed.',"All mobs and neighborhood-level boss monsters within the blast radius subject to both physical and magical explosions will be killed.",FB,'WIKI-ONLY'),
('Fools precursor bursts','A Quest Update reveals four precursor bursts before the main blast; the first stripped magic from equipped gear.',"temporarily removed the magical properties of all your equipped gear",FB,'WIKI-ONLY'),
('Fools Celestial payout','Bandit double-upgraded the Platinum prize to Celestial for 83 survivors.',"double-upgrading the prize to Celestial for 83 crawlers",QB,'VERIFIED (cite B2 Epilogue)'),
('Quan Ch opened first','Quan Ch opened his Celestial box before Borant could act, so the veto missed his.',"Quan Ch opened his before the Borant Corporation could act",QB,'VERIFIED (cite B2 Epilogue)'),
('Floor 3 deal comes due','The Floor 3 production deal came due on Floor 6 as the two-part Vengeance of the Daughter quest.',"The deal Carl struck with the show's producers on the third floor came due on the sixth as a two-part quest line.",Q,'VERIFIED (cite B5 ch15)'),
('Vengeance part 1 reward','Part 1 (Fort Freedom): survivors are 20% more willing to follow your orders.',"every survivor of the assault against the Confederacy will be 20% more willing to follow your orders",VQ,'WIKI-ONLY'),
('Vengeance part 2 reward','Part 2 (kill Queen Imogen): the High Elf Castle becomes lootable.',"the contents of the High Elf Castle will become available to loot",VQ,'WIKI-ONLY'),
('Sidewalk Ends regional','Floor 8 regional quest: every crawler in the Cuba area is added; the receiving squad is named host.',"This is a regional quest. All crawlers within the area of Cuba have been added to this quest.",WS,'VERIFIED (page cite B6 ch62)'),
('Sidewalk Ends option 2','Freeing Amayon resets the timer and turns the regional quest into a world quest.',"The timer will reset, and this quest will reset into a World quest.",WS,'VERIFIED (page cite B6 ch62)'),
('Sidewalk Ends option 3','Killing the (invulnerable on this floor) Amayon pays a Celestial Hell Boon.',"Reward: You will receive a Celestial Hell Boon.",WS,'VERIFIED (cite B6 ch62)'),
]
def clean(t): return norm_ws(strip_cites(t)).replace('\u200b','')
bad=0; out=[]
n=826
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
