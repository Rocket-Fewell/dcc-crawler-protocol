#!/usr/bin/env python3
import os as _os
_LORE = _os.environ.get('DCC_LORE_ROOT') or _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
"""Pass 20 (2026-10-04): premise verification rows (M-525.. and X-066..). APPENDS section 9.3 to CANON-LEDGER.md just before
'### Pass log'. Quotes are located programmatically (exact substrings). Idempotent: refuses to run if M-525 exists.
Writes work/pass20-row-map.json (key -> ledger id). Usage: python3 work/pass20_rows.py [--dry]"""
import re, sys, json
sys.path.insert(0, _os.path.join(_LORE, 'tools'))
from ledger_lib import *
LEDGER = ROOT + '/CANON-LEDGER.md'
START = 525
XSTART = 66
DATE = '2026-10-04'
TR='W:Transformation'; DG='W:Dungeon'; ST='W:Stairwells'; CR='W:Crawler'; SF='W:Second Floor'
YT1='YT:j6jRXuCgsAA'
# key, summary (paraphrase), source tag, exact find-text, optional extra
R = [
 # ---- Claim 1: the Introduction event
 ('tr_time','[Claim 1] The Transformation hit at about 2:23 AM Pacific time on Tuesday, January 3.',TR,'which occurred at approximately 2:23 AM Pacific Standard Time on Tuesday, January 3'),
 ('tr_flatten','[Claim 1] It flattened every roofed or closed-top structure on Earth (buildings, cars, airplanes, tents, even boxes).',TR,'the instantaneous flattening of every roofed or closed-top structure on Earth'),
 ('tr_death','[Claim 1] Any living being inside or underneath such a structure was killed instantly (no survival or stasis is described).',TR,'Any living being inside or underneath such a structure was killed instantly.'),
 ('tr_carl','[Claim 1] Carl\'s own account: anyone indoors at that moment died instantly.',TR,'anyone who was indoors when it happened died instantly'),
 ('tr_yt','[Claim 1] The B1 recap transcript agrees: everything with a roof collapses and everyone inside is killed.',YT1,'everything in the world with a roof suddenly collapses'),
 ('tr_yt_kill','[Claim 1] Same recap: anything counting as indoors is crushed and everyone inside is immediately killed.',YT1,'Cars, houses, anything that counts as indoors instantly gets crushed, and everyone inside is immediately killed.'),
 ('tr_collection','[Claim 1] The event was a "collection": Borant mined every interior for rare primal elements.',TR,'Every interior was processed and mined for rare primal elements'),
 ('tr_matter','[Claim 1] The announcement says nearly all the remaining matter is being repurposed for the subterranean World Dungeon.',TR,'is currently being repurposed for the subterranean World Dungeon'),
 ('tr_dirt','[Claim 1] Visible aftermath: closed structures vanished, leaving churned dirt and shallow dents (a collection looks different on other worlds, e.g. Aryl).',TR,'every closed structure on Earth vanished, leaving only churned dirt and shallow indentations behind'),
 ('tr_aryl','[Claim 1] On the planet Aryl the buildings instead rolled aside and were swept away (so "collapse" is not universal).',TR,'the buildings instead rolled to the side and were swept away'),
 ('tr_appeal','[Claim 1] Why Earth was seized: humanity filed no proper appeal within 50 Solars of first contact; the Syndicate observer announces the planet seized.',TR,'failed to file a proper appeal for mineral and elemental rights within 50 Solars of first contact'),
 ('tr_seized','[Claim 1] The observer AI announcement says the planet is seized and being mined by the assigned planetary regent.',TR,'your planet has been successfully seized and is currently being mined of all requested elemental deposits'),
 ('tr_reclaim','[Claim 1] Survivors are offered a legal chance to reclaim their lost matter.',TR,'any surviving humans will be given the opportunity to reclaim their lost matter'),
 ('tr_option3','[Claim 1] Borant picked "option 3", the 18-Level World Dungeon, as the manner of reclamation.',TR,'they have chosen option 3, also known as the 18-Level World Dungeon'),
 ('tr_hour','[Claim 1] The first-level entrances stay open exactly one human hour.',TR,'The first-level entrances will be open for exactly one human hour and one hour only.'),
 ('tr_nolate','[Claim 1] Once the entrances close nobody can enter.',TR,'Once the entrances are closed, you may no longer enter.'),
 ('tr_optional','[Claim 1] Entering is a choice: those who do not enter must sustain themselves on the surface.',TR,'If you choose not to enter the World Dungeon, you will have to sustain yourself upon the surface of your planet'),
 ('tr_forfeit','[Claim 1] Those who do not enter forfeit all previously processed matter and elements.',TR,'All previously-processed matter and elements are forfeit.'),
 ('tr_noleave','[Claim 1] Once inside you cannot leave until all 18 levels are done (or "certain other requirements" are met; see the Exit Deal row).',TR,'If you enter, you may not leave until you have either completed all 18 levels of the World Dungeon'),
 ('tr_exitdeal','[Claim 1] The "other requirement" route: Exit Deals let surviving Crawlers leave in exchange for years of indenture, available after the Tenth Floor.','W:Exit Deal','Although crawlers can accept Exit Deals after entering the Tenth Floor'),
 ('tr_entrance_choice','[Claim 1] Survivors may choose to enter by descending a stairwell; those who stay on the surface are "Natives".','W:Dungeon Entrance','Survivors may choose to enter the Dungeon and become crawlers by descending a stairwell from the Earth\'s surface.'),
 ('tr_horn','[Claim 1] After the announcement a horn sounds and 150,000 stairwells appear in high-population areas, each marked by an upward light.','W:Dungeon Entrance','a trumpet-like horn sounds and 150,000 stairwells are randomly distributed in high population areas across Earth'),
 ('tr_setfoot','[Claim 1] Entering the stairwell is not enough: you must set foot on the First Floor to count as a Crawler.','W:Dungeon Entrance','You must physically set foot on the First Floor.'),
 ('tr_fall','[Claim 1] A stairwell that opens under someone drops them in; whether they land safely or are "collected" is unclear on the wiki.','W:Dungeon Entrance','that person falls into the stairwell and disappears'),
 ('tr_crawler_def','[Claim 1] Crawler = anyone who chose to enter the World Dungeon after surviving the Transformation.',CR,'Crawler describes anyone who chose to enter the World Dungeon after surviving the Transformation'),
 ('tr_three_groups','[Claim 1] After a collection the population sorts into the Collected (caught in the collapse, usually the largest share), Crawlers (chose to enter) and Natives (everyone else who survived on the surface). (Book 4 spoiler.)',TR,'the Collected (those caught in the collapse, typically the largest share of the population)'),
 ('tr_collected_def','[Claim 1] Wiki glossary: the Collected are all citizens and sustainable fauna "mined" in a planetwide collection, on Earth the largest share.','W:Collected','The Collected are all citizens and sustainable fauna'),
 ('tr_natives_lock','[Claim 1] Natives: aliens may not approach or interact with them until after the crawl, and the planet is locked down for generations.','W:Natives','Aliens cannot approach or interact with Natives until after the crawl.'),
 ('tr_children','[Claim 1] Eligibility: Syndicate law bars pregnant women and children under the age of maturity from the crawl.',CR,'Syndicate law bars pregnant women and children under the age of maturity from the crawl.'),
 ('tr_weight','[Claim 1] Any biological creature above a certain weight that goes through the entrance gets registered, so pets can enter too.',CR,'Any biological creature above a certain weight that passes through the Dungeon Entrance and onto the First Floor'),
 ('tr_nostasis_only_descent','[Claim 1/5] The only stasis rule in the opening is the early-descent rule: stairs taken with more than six hours left put the Crawler in stasis until the next countdown.',DG,'the crawler will be placed in stasis until the countdown begins on the next floor'),
 # ---- start counts (claim 4)
 ('cnt_13m','[Claim 4] Just under 13 million humans entered as Crawlers in the first hour.',TR,'Just under 13 million humans made it through the gates as crawlers'),
 ('cnt_10m','[Claim 4] By the time the first floor sealed the count had fallen below 10 million (about 3 million lost in minutes).',TR,'that number had already fallen below 10 million'),
 ('cnt_yt','[Claim 4] The recap transcript gives the same opening figures: 13 million entered, under 10 million at the seal.',YT1,'only 13 million crawlers made it inside, and that number is already down to under 10 million'),
 ('cnt_yt4','[Claim 4] The recap shows the global count dropping from 10 million to just over four million on Floor 1.',YT1,'The number of survivors has plummeted from 10 million down to just over four.'),
 ('cnt_f2','[Claim 4] The Floor 2 announcement reports just under 1.3 million Crawlers still alive (see M-335 for the toll at the Floor 1 collapse).',SF,'We have just under 1.3 million crawlers still in the game.'),
 ('cnt_f3','[Claim 4] At the Floor 3 race/class announcement about 700,000 Crawlers had chosen.','W:Class','Of the just under 700,000 crawlers who\'ve made a decision'),
 ('cnt_f4','[Claim 4] The recap says the Floor 4 collapse killed tens of thousands.','YT:edNtE1movic','Floor four\'s collapse killed off tens of thousands'),
 ('cnt_f5','[Claim 4] A fan overview gives 178,887 Crawlers at the start of Floor 5.','FW2:book4-overview','Remaining Crawlers | 178,887'),
 ('cnt_f6','[Claim 4] A fan overview gives 85,223 Crawlers at the start of Floor 6.','FW2:book5-overview','Remaining Crawlers | 85,223'),
 ('cnt_f8','[Claim 4] A fan overview gives 38,532 Crawlers at the start of Floor 8.','FW2:book6-overview','Crawlers Remaining | 38,532'),
 ('cnt_f9','[Claim 4] A fan overview gives 32,429 Crawlers beginning Floor 9 (Faction Wars).','FW2:book7-overview','32,429 crawlers begin the floor.'),
 ('cnt_f10','[Claim 4] A fan overview gives about 989 Crawlers beginning Floor 10: Floor 9 is where the field collapses from tens of thousands to about a thousand.','FW2:book8-overview','Approximately 989 crawlers begin Floor 10.'),
 ('cnt_f12','[Claim 4] By the end of Floor 11 only 19 Crawlers remain (plus two special cases).','FW2:book8-overview','By the end of Floor 11, only 19 crawlers remain'),
 ('cnt_numbers','[Claim 4] Crawler numbers are issued in order of arrival; a late-awakened Crawler (the transformed Scolopendra) carries a number near 13 million, consistent with ~13 million entrants.','FW2:book8-overview','Sexy Scolopendra (Level 1 crawler, Crawler #12,953,456) joined the party'),
 # ---- Claim 2: shape / floors / win
 ('sh_18','[Claim 2] The World Dungeon is an eighteen-level subterranean maze built under Earth\'s surface from the planet\'s repurposed matter.',DG,'The World Dungeon is an eighteen-level subterranean maze created beneath the Earth\'s surface'),
 ('sh_triangle','[Claim 2] Seen from the side the Dungeon is an "inverted triangle" (wiki wording; nothing in the pack says "pyramid").',DG,'the subterranean Dungeon looks like an inverted triangle'),
 ('sh_smaller','[Claim 2/4] Each level is progressively more difficult and (except the Ninth Floor) smaller as Crawlers descend.',DG,'each level grows progressively more difficult and (with the notable exception of the Ninth Floor) smaller as crawlers descend'),
 ('sh_f1_largest','[Claim 2] The First Floor is the largest, roughly Earth-surface sized and directly beneath it.',DG,'The First Floor is the largest level'),
 ('sh_f18_smallest','[Claim 2] The Eighteenth Floor is the smallest, closest to the core.',DG,'the Eighteenth Floor is the smallest and closest to the Earth\'s core'),
 ('sh_outlined','[Claim 2] All eighteen floors were outlined in advance by Borant and approved by the Crawl Council.',DG,'All eighteen floors were outlined in advance by the Borant Corporation and approved by the Crawl Council.'),
 ('sh_tutorial','[Claim 2/4] The first two floors are tutorial levels; the Third and every third floor after join a multi-season storyline.',DG,'the Third Floor and every third floor after it are part of an over-arching, multi-season storyline'),
 ('sh_scolo','[Claim 2] Floors 3, 6, 9, 12, 15 and 18 form one interconnected storyline (the six-layer volcano of Scolopendra).',DG,'The Third Floor, Sixth Floor, Ninth Floor, Twelfth Floor, Fifteenth Floor, and Eighteenth Floor are part of an interconnected storyline'),
 ('sh_oneway','[Claim 2] Descent is strictly one-way; no returning to a previous floor.',DG,'descent is strictly one-way, and crawlers cannot return to a previous floor'),
 ('sh_closes','[Claim 2/4] The Dungeon closes after the later of full Crawler extinction or the end of the Twelfth Floor, yet a plan must exist for every level.',DG,'The Dungeon will close after the later of (a) full crawler extinction or, more commonly, (b) the conclusion of the Twelfth Floor.'),
 ('win_regency','[Claim 2] Win condition as presented: complete all eighteen levels and exit the final stairwell to win regency of the Earth.',DG,'if a survivor successfully completes all eighteen levels and exits the final stairwell, they will win regency of the Earth'),
 ('win_announce','[Claim 2] The announcement words the prize as regency of the planet reverting to "the successor" on completing level 18.',TR,'Upon successful completion of level 18 of the World Dungeon, regency of this planet will revert to the successor.'),
 ('win_final_door','[Claim 2] To win Dungeon Crawler World, Crawlers must reach Floor 18 and pass through the final door.','W:Eighteenth Floor','To win Dungeon Crawler World, crawlers must reach this floor and pass through the final door.'),
 ('win_not_past13','[Claim 2] No Crawler has made it past the Thirteenth Floor, but the production company must plan all levels.',DG,'no crawler has made it past the Thirteenth Floor'),
 ('win_one13','[Claim 2] Only one participant in the show\'s whole history has reached the Thirteenth Floor.',DG,'only one participant in the show\'s history has made it as far as the Thirteenth Floor'),
 ('win_b8door','[Claim 2] Book 8 spoiler (wiki): Scolopendra was summoned to the 11th-floor arena, Carl defeated it, and the AI opened the final door on Floor 18.','W:Eighteenth Floor','After Carl defeated this boss, the AI officially opened the final door on the Eighteenth Floor.'),
 ('win_b8_crawler','[Claim 2] Book 8 fan overview: the Dungeon Boss was turned into a Level-1 Crawler by a pet biscuit (not killed) during Floor 11.','FW2:book8-overview','Transformed to Level 1 crawler by enriched pet biscuit'),
 ('win_b8_f11','[Claim 2] Book 8 covers Floors 10-11 and ends with the first-ever summoning of the Dungeon Boss.','FW2:book8-overview','culminating in the first-ever summoning of Scolopendra, the Dungeon Boss'),
 ('win_dying','[Claim 2/5] A Crawler who dies inside the Dungeon is permanently dead (there is no respawning).',DG,'A crawler who dies inside the dungeon is permanently dead.'),
 ('win_norespawn','[Claim 2/5] There is no respawning for Crawlers.',CR,'There is no respawning.'),
 ('win_citizen','[Claim 2/4] Crawlers have no legal standing until the Tenth Floor, where they earn Syndicate citizenship.',CR,'hold no legal standing of their own until they reach the Tenth Floor and earn Syndicate citizenship'),
 # ---- Claim 3: stairwells
 ('st_rule','[Claim 3] Rule: each floor has half (rounded up) the stairwells of the previous level.',DG,'Each floor has 1/2 (rounded up) the number of stairwells as the previous level.'),
 ('st_pg','[Claim 3] Stairwells page: 150,000 entrances to Floor 1, 75,000 to Floor 2, halving (rounding up) to two entrances and one exit on Floor 18.',ST,'there were 150,000 entrances from Earth down to the First Floor, 75,000 down to the Second Floor'),
 ('st_ann','[Claim 3] The announcement itself gives 150,000 level-one entrances, 75,000 for level two and 37,500 for level three.',TR,'There will be 75,000 entrances to level two. There will be 37,500 entrances to level three.'),
 ('st_ann18','[Claim 3] The announcement: the count keeps halving, rounding up, until level 18 has two entrances and a single exit.',TR,'will continue to decrease by half, rounding up until the 18th level, which will only have two entrances and a single exit'),
 ('st_18','[Claim 3] Floor 18 page: only two entrances and a single exit.','W:Eighteenth Floor','containing only two entrances and a single exit'),
 ('st_unlock3','[Claim 3] From the Third Floor stairwells must be unlocked by quests, boss kills or gambles.',DG,'Beginning on the Third Floor, stairwells must be unlocked by completing quests'),
 ('st_guard4','[Claim 3] Stairwells page: from the Fourth Floor on they stop populating randomly and become guarded (see X-073 for the Third/Fourth mismatch).',ST,'from the Fourth Floor onward they stop populating randomly and become guarded'),
 ('st_f1_late','[Claim 3] On Floor 1 the stairwells down do not populate until after the first episode, roughly 30 hours in.',ST,'do not populate or open until after the first episode of Dungeon Crawler World: Earth, roughly 30 hours in'),
 ('st_f4_late','[Claim 3] On Floor 4 Crawlers may not descend early; stairwells open only six hours before collapse (Book 3 spoiler).',ST,'Crawlers may not descend early; the stairwells open only six hours before collapse.'),
 ('st_f4_rooms','[Claim 3] On Floor 4 stairwells sit in hidden underground rooms, five to a chamber, ringed in a circle (Book 3 spoiler).',ST,'stairwells were clustered in hidden underground rooms, five to a chamber, ringed in a circle'),
 ('st_f7_portal','[Claim 3] On Floor 7 the stairwells are round glowing portals in a vertical corkscrew, not stairs (Book 5 spoiler).',ST,'the stairwells had no stairs or doors at all'),
 ('st_door','[Claim 3] The Floor 1 stairwell ends at a double-wide door engraved with a Kua-Tin.',ST,'a massive, double-wide door engraved with a stylized, oversized Kua-Tin'),
 # ---- Claim 4: progression
 ('pg_timers','[Claim 4] Each level is open a set number of 24-hour days; the countdown for a floor starts when the previous floor collapses.',DG,'each level is open to crawlers for a predetermined number of 24-hour days'),
 ('pg_urban','[Claim 4] The Third, Sixth and Ninth Floors are Urban levels with Elites who star in their own programs.',DG,'The Third, Sixth, and Ninth Floors are Urban levels'),
 ('pg_elites','[Claim 4] Thousands of Elites are spread over Floors 3, 6 and 9 each season.','W:Elite','thousands of Elites are spread across the third, sixth, and ninth floors'),
 ('pg_blood','[Claim 4] Around Floors 8-9 safe-room access becomes timed (a "blood bar"; Book 5 spoiler).',DG,'Safe Room access becomes timed and regulated by a'),
 ('pg_exit_better','[Claim 4] Exit Deal terms improve the lower a Crawler gets.','W:Exit Deal','the options and terms become more favorable as crawlers reach lower levels'),
 ('pg_sexy','[Claim 4] The wealthy battle on the Twelfth Floor or party in the Eighteenth Floor Scolopendra Club (Book 8 spoiler).',DG,'The galaxy\'s wealthy elite battle one another in the Twelfth Floor'),
 # ---- Claim 5: collapse fate
 ('co_crawler','[Claim 5] A Crawler who cannot reach a stairwell before the timer hits zero is killed and "collected" when the level collapses.',DG,'the crawler is killed and collected when the level collapses'),
 ('co_stair','[Claim 5] Stairwells page: a Crawler who misses a stairwell dies in the collapse "along with everything else left behind".',ST,'they will die in the level collapse along with everything else left behind'),
 ('co_f1','[Claim 5] More than 700,000 died when Floor 1 collapsed (existing row M-335 quotes the Second Floor page).',SF,'died the instant the First Floor collapsed'),
 ('co_asher','[Claim 5] Book 6 spoiler: the Dungeon reused the consciousnesses of people who died in the collapse to form the heads of a hydra boss.','W:Asher','the dungeon uses the collected consciousnesses and memories of the people who died in the collapse'),
 ('co_printed','[Claim 5] Book 6 spoiler: the Dungeon prints its mobs and NPCs from recycled biological remains of Earth\'s previous inhabitants.',DG,'The Dungeon relies on recycling the biological remains of Earth\'s previous inhabitants'),
 ('co_npc_own','[Claim 5] NPCs are living creatures printed and owned by the production company; most know only the Dungeon.','W:NPCs','Most are printed by the production company running the current season'),
 ('co_npc_rewrite','[Claim 5] NPC minds are rewritten at every regeneration, erasing earlier crawls.','W:NPCs','NPC minds are rewritten at every regeneration, erasing memories of previous crawls'),
 ('co_npc_recycle','[Claim 5] Book 7 spoiler: NPCs auto-recycle on death and are meant to be recycled after about twenty lives.','W:NPCs','Class A and Class B NPCs auto-recycle whenever they are killed'),
 ('co_goblin_sleep','[Claim 5] Floor 1 mobs Rory and Lorelai are aware they are mobs in a construct and say that at floor collapse they "go to sleep" until the next Dungeon opens (wiki page has no chapter cite).','W:Lorelai','go to sleep until the next Dungeon opens'),
 ('co_goblin_aware','[Claim 5] Same page: the shamankas know they are mobs inside a construct.','W:Lorelai','keenly aware that they are mobs inside a construct'),
 ('co_stair_mobs','[Claim 5] A mob that wanders onto a stairwell is destroyed outright, keeping each floor\'s monster ecology on that floor.',ST,'Mobs that wander onto a stairwell are not teleported away but destroyed outright'),
 ('co_patch','[Claim 5] After the Rage Elemental recap aired the rule changed: non-sapient mobs reaching a stairwell are no longer disintegrated.',ST,'non-sapient mobs reaching a stairwell would no longer be disintegrated'),
 ('co_cabaret','[Claim 5] Book 8 recap: the Pineapple Cabaret is a pocket dimension where NPCs and mobs can survive a floor collapse (implying they normally do not).','YT:kk6nspvVf_M','It occupies a separate pocket dimension where NPCs and mobs can survive the collapse of a dungeon floor'),
 ('co_guild_room','[Claim 5] Tutorial guild rooms (guide NPC homes) relocate intact when the Third Floor collapses.','W:Tutorial Guild Hall','the room relocates intact when the third floor collapses'),
 ('co_guides_kill','[Claim 5] Game Guides get no system protection and can be permanently killed (a guide killed by administrative action is noted on the page).','W:Game Guide','receive no system protection, so they can be permanently killed'),
 ('co_elite_travel','[Claim 5] Elites who survive their Floor 3 storylines travel on to Floor 6.','W:Elite','important Elites who survive their third-floor storylines automatically travel down to the sixth floor'),
 ('co_stasis_early','[Claim 5] Stairwells page: descending prematurely holds a Crawler in stasis until the floor above collapses; the last six hours are stasis-free.',ST,'Descending prematurely holds a crawler in stasis until the floor above collapses'),
]
# per-floor stairwell counts (table, no quotable sentence). floor -> (name, days or None, stairwells)
TABLE = [(1,'First Floor',5,75000),(2,'Second Floor',6,37500),(3,'The Over City',8,18750),(4,'The Iron Tangle',10,9375),(5,'The Bubbles',15,4688),
 (6,'The Hunting Grounds',17,2344),(7,'The Great Race',20,1172),(8,'The Ghosts of Earth',21,586),(9,'Faction Wars',None,293),(10,'Don\'t Come In Last',None,147),
 (11,'A Parade of Horribles',None,74),(12,'Halls of Ascendancy',None,37),(13,'Thirteenth Floor',None,19),(14,'Fourteenth Floor',None,10),(15,'Sheol',None,5),
 (16,'Agony of Mirrors',None,3),(17,'The Backstage Death Maze',None,2),(18,'Scolopendra\'s Lair',None,1)]
# web-only rows (no quote; see sources/web/premise-web-snippets.txt)
WEB = [
 ('web_nerdist','[Claim 4] Nerdist overview: ten million Crawlers enter and three million die in the first hour (differs from the wiki\'s 13 million entering and under 10 million at the seal). (WEB:nerdist-overview)','WEB:nerdist-overview'),
 ('web_wikipedia','[Claim 4] Wikipedia plot summary: only "a few million" escape the elimination of humanity (loose; no counts). (WEB:wikipedia-dcc)','WEB:wikipedia-dcc'),
 ('web_triangle','[Claim 2] A fan reference site also says "inverted triangle", each floor smaller than the last, with one exit on the last floor; it does not say "pyramid". (WEB:simulacra-world-dungeon)','WEB:simulacra-world-dungeon'),
 ('web_pyramid','[Claim 2] Search-engine synthesis wrote "inverted triangle/pyramid" but none of its cited pages said pyramid; "inverted pyramid" is unconfirmed as canon wording. (WEB:search-synthesis-inverted)','WEB:search-synthesis-inverted'),
 ('web_goblin_sleep','[Claim 5] Recap site: the Floor 1 goblins know the floor collapses but go to sleep and wake on the next floor down, hoping Crawlers stop coming. (WEB:manatoast-b1-recap-npc)','WEB:manatoast-b1-recap-npc'),
 ('web_collapse_dies','[Claim 5] Fan guide: when a floor timer reaches zero anyone still on the floor dies. (WEB:crawlerscookbook-floor1)','WEB:crawlerscookbook-floor1'),
]
CALEB='Caleb\'s overview (job brief 2026-10-04)'
X = [
  ('x_stasis','Transformation: instant death vs "stasis"',
   ('note','overview says the aliens collapsed every interior structure, killed every human and put them in stasis',CALEB),
   (TR,'anyone who was indoors when it happened died instantly'),
   'RESOLVED for canon. PREFERRED: instant death for anyone inside or under a roofed structure; no stasis for the dead appears in the pack. Stasis in canon is only the early-descent rule (M-277, tr_nostasis row). Keep "stasis" only as a house/inspired idea and label it so in the Core Book.'),
  ('x_everyone','Transformation: "every human" vs only those indoors',
   ('note','overview says the aliens killed every human (then separately that people outside survived)',CALEB),
   (TR,'Any living being inside or underneath such a structure was killed instantly.'),
   'RESOLVED for canon. PREFERRED: only those inside or under a roof died; survivors were outdoors and the Collected are the dead (Book 4 spoiler). The overview\'s own two statements disagree unless read as "every human indoors".'),
  ('x_pyramid','Dungeon shape: "inverted pyramid" vs "inverted triangle"',
   ('note','overview says giant inverted pyramid',CALEB),
   (DG,'the subterranean Dungeon looks like an inverted triangle'),
   'OPEN (wording only). PREFERRED: say "inverted triangle" (seen from the side) for canon; "pyramid" is not used by any local source or cited web page, so tag it inspired.'),
  ('x_return','Prize: "returns Earth" vs "win regency of the Earth"',
   ('note','overview says beating floor 18 wins and returns Earth',CALEB),
   (TR,'Upon successful completion of level 18 of the World Dungeon, regency of this planet will revert to the successor.'),
   'OPEN. PREFERRED: say the winner wins regency of Earth (the right to reclaim its matter, as presented to survivors). No source says Earth, the dead or the mined matter are restored; "returns Earth" is unverified. Note the announcement says "the successor", wording left unexplained on the wiki.'),
  ('x_nobody','Win status: "nobody has beaten it"',
   ('note','overview says nobody has beaten it',CALEB),
   (DG,'only one participant in the show\'s history has made it as far as the Thirteenth Floor'),
   'RESOLVED (with a spoiler caveat). PREFERRED: no one in the show\'s history has finished (best prior result: one Crawler reached Floor 13). Book 8 spoilers on the Floor 18 page say the final door was opened for the Earth crawl, so the claim is only safe for the opening premise, not the whole series.'),
  ('x_counts','Start counts: 13 million vs 10 million vs "previous two million"',
   (TR,'Just under 13 million humans made it through the gates as crawlers'),
   (SF,'roughly 1.3 million of the previous two million'),
   'OPEN. PREFERRED: say "about 13 million entered, under 10 million by the first-floor seal, about 1.3 million at the start of Floor 2". Nerdist says ten million entered (WEB:nerdist-overview) and the Second Floor page\'s "previous two million" fits no other figure (the recap shows 3.5-4 million mid-floor). Counts stay unverified against the novel.'),
  ('x_f4count','Floor 4 survivors: about 1,400 vs 178,887',
   ('FW2:book3-overview','Approximately 1,400 crawlers escaped Floor 4 alive.'),
   ('FW2:book4-overview','Remaining Crawlers | 178,887'),
   'OPEN. PREFERRED: use the 178,887 figure for the start of Floor 5 (matches the tens-of-thousands collapse toll). The 1,400 may be a subset or a slip in one fan overview; unverified.'),
  ('x_guard','Guarded stairwells: Third Floor vs Fourth Floor',
   (DG,'Beginning on the Third Floor, stairwells must be unlocked by completing quests'),
   (ST,'from the Fourth Floor onward they stop populating randomly and become guarded'),
   'OPEN. Both are wiki statements; the Stairwells table leaves Floor 3 blank. PREFERRED for the Core Book: say "from about the Third or Fourth Floor stairwells are guarded or unlocked", not an exact floor.'),
  ('x_leave','Leaving the Dungeon: "may not leave" vs Exit Deals',
   (TR,'If you enter, you may not leave until you have either completed all 18 levels of the World Dungeon'),
   ('W:Exit Deal','Although crawlers can accept Exit Deals after entering the Tenth Floor'),
   'RESOLVED. PREFERRED: the announcement\'s "or if you meet certain other requirements" is the Exit Deal route (indenture to the production company, from Floor 10). Do not tell players winning is the only way out.'),
  ('x_npc','NPC fate at floor collapse: sleep vs not surviving',
   ('W:Lorelai','go to sleep until the next Dungeon opens'),
   ('YT:kk6nspvVf_M','It occupies a separate pocket dimension where NPCs and mobs can survive the collapse of a dungeon floor'),
   'OPEN. Canon never states the NPC/AI fate at collapse in one authoritative line. Mob belief (Rory, Lorelai; wiki page uncited) is sleep until the next Dungeon; the Pineapple Cabaret recap implies NPCs and mobs normally do not survive; Stairwells says everything left behind dies. PREFERRED: tag unverified; for the RPG treat Crawlers left behind as dead (canon) and NPCs as reset or recycled (inspired).'),
]
OVERRIDE = {}
def stripped(tag): return norm_ws(strip_cites(src_text(tag)))
def find_snip(tag, find):
    cands = [find, find.replace("'", "\u2019"), find.replace('"', '\u201c')]
    raw = src_text(tag)
    for f in cands:
        words = norm_ws(f).split(' ')
        pat = r'(?:\s|\[\d+\|[^\]]+\])+'.join(re.escape(w) for w in words)
        m = re.search(pat, raw)
        if m: return f, raw, m
    return None, raw, None
def cites_after(raw, m):
    tail = raw[m.end():]
    s = re.match(r'([^.!?\[]*[.!?"\u201d]*)((?:\[\d+\|[^\]]+\])+)', tail)
    if s: return cites_in(s.group(2)), 'sentence'
    para_after = tail.split('\n\n')[0]
    g = re.search(r'((?:\[\d+\|[^\]]+\])+)', para_after)
    if g: return cites_in(g.group(1)), 'page'
    head = raw[:m.start()]
    para_before = head.split('\n\n')[-1]
    gs = re.findall(r'((?:\[\d+\|[^\]]+\])+)', para_before)
    if gs: return cites_in(gs[-1]), 'page'
    return [], 'none'
def fmt(cs):
    by = {}
    for c in cs:
        b, ch = c.split(':', 1)
        by.setdefault(b, [])
        if ch not in by[b]: by[b].append(ch)
    out = []
    for b, chs in by.items():
        out.append(f'{b} ch' + ','.join(chs) if all(x.isdigit() for x in chs) else f'{b} ' + ','.join(chs))
    return '; '.join(out)


# self-check of the table against the announced halving rule
_n = 150000
for fl, nm, days, st in TABLE:
    _n = (_n + 1) // 2
    assert _n == st, (fl, _n, st)

def main():
    dry = '--dry' in sys.argv
    led = open(LEDGER).read()
    if f'| M-{START} |' in led:
        print('already appended'); return 1
    rows = []; idmap = {}
    for i, r in enumerate(R):
        key, summ, tag, find = r[:4]
        extra = r[4] if len(r) > 4 else None
        rid = f'M-{START+i}'
        f, raw, m = find_snip(tag, find)
        if not m: print('NOT FOUND', key, '|', tag, '|', find); continue
        core = norm_ws(f)
        if len(core.split()) > 25: print('TOO LONG', key, len(core.split())); continue
        cs, kind = cites_after(raw, m)
        tags = tag
        if kind == 'sentence': conf = f'VERIFIED (cite {fmt(cs)})'
        elif kind == 'page': conf = f'VERIFIED (page cite {fmt(cs)})'
        else: conf = 'WIKI-ONLY'
        if tag.startswith('YT:') or tag.startswith('FW2:'):
            conf = 'UNVERIFIED (single transcript or fan-overview claim; not read against the novel)' if tag.startswith('FW2:') else 'WIKI-ONLY (recap transcript, auto-captions)'
        if key in ('tr_yt','tr_yt_kill'):
            tags = f'{tag}; {TR}'; conf = 'VERIFIED (2 sources: recap transcript + wiki cite B1 ch1)'
        if key in ('cnt_yt','cnt_yt4'): tags = f'{tag}; {TR}' if key=='cnt_yt' else tag; conf = 'VERIFIED (2 sources: transcript + wiki cite B1 ch4)' if key=='cnt_yt' else 'WIKI-ONLY (recap transcript, auto-captions)'
        if key == 'cnt_numbers': conf = 'UNVERIFIED (single fan-overview claim; not read against the novel)'
        if key in OVERRIDE: conf = OVERRIDE[key]
        quote = core.replace('|', '\\|')
        rows.append(f'| {rid} | {summ} | "{quote}" | {tags} | {conf} | {DATE} |')
        idmap[key] = rid
    if len(rows) != len(R): print('ABORT: some rows failed'); sys.exit(2)
    n = START + len(R)
    rid = f'M-{n}'; n += 1
    rows.append(f'| {rid} | [Claim 3] Earth surface: 150,000 entrances to Floor 1, open exactly one human hour. | \u2014 (Floor Breakdown table row; announcement quotes at the Introduction rows) | {DG} | WIKI-ONLY (table row; matches the announcement quotes) | {DATE} |')
    idmap['tb_surface'] = rid
    for fl, nm, days, st in TABLE:
        rid = f'M-{n}'; n += 1
        d = f'; timer {days} days' if days else '; timer not listed on the wiki table'
        extra = ' Last floor: one exit, entered from the 2 stairwells on Floor 17.' if fl == 18 else ''
        extra = ' (Floor 9 is the one floor that is not smaller than the one above.)' if fl == 9 else extra
        rows.append(f'| {rid} | [Claim 3] Floor {fl} ({nm}): {st:,} stairwells lead down from it{d}.{extra} | \u2014 (Floor Breakdown table cell; not a quotable sentence) | {DG} | WIKI-ONLY (table row; equals the halving rule rounded up, checked in script) | {DATE} |')
        idmap[f'tb_f{fl:02d}'] = rid
    for k, summ, slug in WEB:
        rid = f'M-{n}'; n += 1
        rows.append(f'| {rid} | {summ} | \u2014 (no quote; web search snippet, see sources/web/premise-web-snippets.txt) | {slug} | UNVERIFIED (web-only claim; no quote; not read against the novel) | {DATE} |')
        idmap[k] = rid
    last_m = n - 1
    xrows = []
    for j, (key, topic, A, B, status) in enumerate(X):
        xid = f'X-{XSTART+j:03d}'
        def cell(src):
            if src[0] == 'note': return f'{src[1]}', src[2]
            tag, find = src
            f, raw, m = find_snip(tag, find)
            if not m: print('X NOT FOUND', key, tag, find); sys.exit(2)
            c = norm_ws(f)
            if len(c.split()) > 25: print('X TOO LONG', key); sys.exit(2)
            return '"' + c.replace('|', '\\|') + '"', tag
        ta, sa = cell(A); tb, sb = cell(B)
        xrows.append(f'| {xid} | {topic} | {ta} | {sa} | {tb} | {sb} | {status} | {DATE} |')
        idmap[key] = xid
    block = ['', '### 9.3 Premise verification: Transformation, dungeon shape, stairwells, progression and collapse fate (Pass 20, 2026-10-04; prefix M- continues mechanics rulings; feeds drafts/premise-verification.md)',
             'Source: local Fandom mirror pages, one YouTube recap transcript set, fan-overview files (FW2) and web search snippets saved in `sources/web/premise-web-snippets.txt` (web-only rows have no quote and are labelled UNVERIFIED). Same caveat as section 0: nothing here was read against the novels. Quotes are wiki wording, not novel text. "[Claim n]" in a ruling refers to the five claims in `drafts/premise-verification.md`. "page cite" = a chapter cite sits elsewhere in the same paragraph of the wiki page. The per-floor stairwell rows come from the wiki\'s Floor Breakdown table, which has no quotable sentence, so they carry no quote; each was checked against the announced halving rule (150,000, halving and rounding up). Crawler counts, timers in days and stairwell counts are canon facts, not difficulty values; levels, credits and loot amounts are deliberately not captured. Existing anchors: T-001, T-002, R-024, R-042, M-016, M-039, M-277, M-335, M-366.',
             '', '| ID | Ruling (paraphrase) | Source quote (<=25 words) | Source | Confidence | Date |', '|---|---|---|---|---|---|'] + rows + ['',
             f'#### 9.3c Premise conflicts with the overview (X-{XSTART:03d}..X-{XSTART+len(X)-1:03d})', '',
             '| ID | Topic | Reading A (quote or note) | Source A | Reading B (quote or note) | Source B | Status | Date |', '|---|---|---|---|---|---|---|---|'] + xrows + ['']
    marker = '### Pass log'
    idx = led.index(marker)
    new = led[:idx] + '\n'.join(block).lstrip('\n') + '\n' + led[idx:]
    json.dump(idmap, open(ROOT + '/work/pass20-row-map.json', 'w'), indent=1)
    print('rows', len(rows), f'M-{START}..M-{last_m}', 'X', len(xrows), f'X-{XSTART}..X-{XSTART+len(X)-1}')
    if dry:
        print('\n'.join(block)[:2500]); return 0
    open(LEDGER, 'w').write(new)
    print('appended')
    return 0
sys.exit(main())
