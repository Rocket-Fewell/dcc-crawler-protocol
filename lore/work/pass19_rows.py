#!/usr/bin/env python3
"""Pass 19 (2026-10-04): builds the Floor 2 canon ledger rows (M-327.. and X-059..) from local sources and APPENDS them
to CANON-LEDGER.md as section 9.2 (just before '### Pass log'). Quotes are located programmatically (exact substrings).
Idempotent: refuses to run if the first new ID already exists. Writes work/pass19-row-map.json (key -> ledger id).
Usage: python3 work/pass19_rows.py [--dry]"""
import re, sys, json
sys.path.insert(0, '/workspace/dcc-lore/tools')
from ledger_lib import *
LEDGER = ROOT + '/CANON-LEDGER.md'
START = 327
XSTART = 59
DATE = '2026-10-04'
SF = 'W:Second Floor'; YT = 'YT:j6jRXuCgsAA'; CS = 'W:Book 1 Chapter Summaries'
# key, summary (paraphrase), source tag, exact find-text, optional extra tag / 'UNVERIFIED' / 'CS:<ch>'
R = [
 # ---- floor-wide
 ('f2_final_tutorial','The Second Floor is the last Tutorial floor and, like Floor 1, a grid maze of cinderblock halls.',SF,'The Second Floor is the final Tutorial level of the Dungeon and, like the First Floor above it, consists of a sprawling, grid-like maze'),
 ('f2_regions','The grid is cut into unconnected regional sections, so Crawlers from far-apart places cannot meet on this floor.',SF,'unconnected regional sections \u2014 meaning a crawler originating in, say, China cannot reach a crawler from the USA'),
 ('f2_walls','Floor 2 walls are magical cinderblock that cracks under impact but never fully breaks (a boss can still wreck them).',SF,'built from magical cinderblock that cracks on impact but never fully breaks'),
 ('f2_ground','Floor 2 ground is cracked, uneven white concrete with sharp little rocks and pavement splinters.',SF,'The ground is cracked, uneven white concrete strewn with sharp little rocks and splinters of pavement'),
 ('f2_arteries','The main halls on Floor 2 are narrower than on Floor 1.',SF,'though the main arteries here are narrower'),
 ('f2_timer_short','Floor 2 is remembered for an unusually short six-day timer cut to the legal minimum by Borant.',SF,'It is best remembered for its unusually short, six-day timer, slashed to the legal minimum by the Borant Corporation.'),
 ('f2_timer_why','The six-day timer replaced the ten days that guides such as Mordecai expected, because far fewer Crawlers survived Floor 1 than projected. (House note: Floor 2 is 10 days in the house game, see X-062.)',SF,'the collapse timer was cut to the Syndicate legal minimum of six days, rather than the ten that guides like Mordecai had anticipated.'),
 ('f2_count_start','1,292,526 Crawlers were left when the Floor 2 countdown started.',SF,'Remaining Crawlers: 1,292,526.'),
 ('f2_collapse_toll','More than 700,000 people died the instant Floor 1 collapsed, about a third of the survivors.',SF,'more than 700,000 people \u2014 about a third of the survivors \u2014 died the instant the First Floor collapsed.'),
 ('f2_count_mid','Remaining-Crawler counts logged on Floor 2: 1,033,992 at 4 d 20 h left and 990,303 at 3 d 11 h left (under one million).',SF,'Remaining Crawlers: 990,303.'),
 ('f2_ann_timing','Cascadia\'s Floor 2 opening announcement follows the fourth Dungeon Crawler World: Earth episode, about seven hours after the floor opens.',SF,'Cascadia\'s announcement follows the episode, meaning it takes place approximately seven hours after the Second Floor opened to crawlers.'),
 ('f2_ann_tone','The opening announcement is mostly a cash-grab for Sponsors with one stern bathroom warning.',SF,'The announcement mostly details Borant Corporation\'s desperate cash-grab for Sponsors'),
 ('f2_ann_count','Announcement: the crawler count is under projection, so the timer drops to the legal minimum.',SF,'That number is slightly lower than our projections, so we are speeding up the second floor timer to the minimum legally allowed by the rules.'),
 ('f2_ann_six','Announcement: six days to find a staircase down.',SF,'You have six days to find a staircase down.'),
 ('f2_ann_wait','Announcement: Crawlers are urged to wait until the last possible moment to descend.',SF,'Once again, we urge you all to wait until the last possible moment to descend.'),
 ('f2_ann_follows','Announcement: viewer follows and favorites switch on when it ends; numbers fill in slowly.',SF,'follows and favorites will be turned on for our viewers'),
 ('f2_ann_patrons','Announcement: patronage is revised to a three-patron cap, with auctions on the later floors (the amounts are not recorded here).',SF,'All crawlers are now limited to three patrons'),
 ('f2_ann_boxes','Announcement: a patron who pays more for a Crawler gets more and better Benefactor Boxes for them.',SF,'the more your patron pays for you, the more and higher-quality Benefactor Boxes you may receive'),
 ('f2_ann_disappointed','Announcement: Cascadia scolds Crawlers for disrespecting the bathrooms.',SF,'we are disappointed in the disrespect we are being shown regarding the bathrooms'),
 ('f2_ann_penalty','Announcement: relieving yourself outside a designated bathroom brings a Rage Elemental from the thirteenth floor.',SF,'they will be immediately and swiftly penalized in the form of a Rage Elemental plucked from the thirteenth floor','YT'),
 ('f2_ann_penalty_kill','Announcement: the elemental kills the offender and the whole party.',SF,'This elemental will kill them and everyone in their party before they can get their pants back up.'),
 ('f2_ann_signoff','Announcement sign-off: cheerful kill-kill-kill send-off.',SF,'Have fun out there, and remember to kill, kill, kill!'),
 ('f2_penalty_humans','The bathroom penalty hits human-born Crawlers only; pets such as Mongo are exempt, and the rule ends at floor collapse.',SF,'The penalty applies only to humans; non-human pets such as Mongo can relieve themselves without consequence.'),
 ('f2_penalty_admin','The bathroom penalty applies to every human in the Dungeon, not only Crawlers (a human admin was splattered).','W:Rage Elemental','The bathroom penalty applied to every human in the Dungeon, not only to crawlers'),
 ('f2_restroom_portals','Floor 2 restroom doors are portals to the Crawler\'s own single stall, one toilet-paper roll per floor.',SF,'The mismatched doors are actually portals that always open onto the same single stall assigned to each crawler'),
 ('f2_restroom_spacing','Restroom doors appear about every quarter mile.',SF,'appear roughly every 0.25 mile (0.4 km)'),
 ('f2_restroom_privacy','Now that Syndicate citizens can watch, the stall is the only place shielded from cameras.',SF,'the stalls are the only place a crawler is shielded from watching eyes'),
 ('f2_sr_spacing','Safe rooms sit every few miles and show on the minimap from afar.',SF,'Safe Rooms appear every few miles and are visible from afar on the minimap.'),
 ('f2_sr_staffing','Some Floor 2 safe rooms are full-service and staffed by a Bopca Protector; others are unstaffed with no food.',SF,'Some are full-service dining areas staffed by a Bopca Protector, while others are unstaffed and offer no food at all.'),
 ('f2_sr_beds','Every safe room has cots or private rooms, free or for rent on this floor.',SF,'Every safe room provides either limited-capacity public sleeping space (usually dusty cots) or private rooms, free to use or rent on this floor.'),
 ('f2_sr_look','Safe rooms are lifted from Earth, for example a French storm shelter or a converted industrial kitchen.',SF,'taking forms such as a French storm shelter or a converted industrial kitchen'),
 ('f2_sr_mailbox','New on Floor 2: safe rooms include a mailbox.',SF,'Beginning on this floor, safe rooms also include a mailbox.'),
 ('f2_sr_mail_error','A Crawler without a Floor Club (or similar) subscription who opens the mailbox gets a System error line.',SF,'Why would someone send you mail?'),
 ('f2_sr_close','Safe-room closure: anyone still inside one hour before collapse is teleported just outside (patch made at the 4 d 17 h mark).',SF,'any crawler still inside a safe room one hour before level collapse is teleported just outside it','YT'),
 ('f2_sr_close_why','The closure rule was a response to Crawlers who stayed, partied and died in Floor 1 safe rooms.',SF,'a measure prompted by the many crawlers who chose to remain, party, and die in First Floor safe rooms'),
 ('f2_sr_close_clock','A second countdown, Time to Safe Room Closure, appears inside safe rooms.',SF,'A second countdown, Time to Safe Room Closure, now appears inside.'),
 ('f2_sr_ch39','Chapter 39 summary: the rules change so Crawlers cannot sit in a safe room until the collapse.',CS,'The rules change to prevent crawlers staying in a safe room until the collapse.','CS:39'),
 ('f2_stair_all','Unlike Floor 1, all 37,500 Floor 2 stairwells exist the moment the floor opens.',SF,'all 37,500 stairwells were in place the moment the Second Floor opened'),
 ('f2_stair_bosses','Every Borough Boss and City Boss chamber holds a stairwell; the rest are scattered at random.',SF,'Stairwells sit inside every Borough Boss and City Boss chamber'),
 ('f2_stair_stasis','Descending with more than six hours left holds the Crawler in stasis until collapse.',SF,'A crawler who descends with more than six hours left on the timer is held in stasis until collapse'),
 ('f2_stair_headstart','Descending with six hours or less left gives a head start on Floor 3 and its race/class selection.',SF,'descending with six hours or less grants a head start on the Third Floor'),
 ('f2_stair_free','The timeline marks the last six hours (about Fri 8:30 PM PST) as when descending costs no time.',SF,'Crawlers can begin descending to the Third Floor without losing time.'),
 ('f2_stair_nonsapient','Patch (3 d 11 h left): non-sapient mobs that enter a stairwell no longer disintegrate.',SF,'Non-sapient mobs that enter a stairwell will no longer disintegrate.'),
 ('f2_guild_halls','Tutorial Guild Halls are all over the first three floors.',SF,'Tutorial Guild Halls liberally populate the dungeon\'s first three floors.'),
 ('f2_guides_f3','Patch (3 d 11 h left): Game Guides may start explaining Floor 3 race/class selection.',SF,'Game Guides can now begin explaining Third Floor race/class selection.'),
 ('f2_ratings_on','Floor 2 is where ratings switch on: follows and favorites activate and rating numbers start to fill in.',SF,'viewer follows and favorites activate and crawlers\' rating numbers begin to populate'),
 ('f2_guides_hidden','Viewers cannot see Game Guides; only press-credentialed viewers can.',SF,'viewers still cannot see Game Guides, who are visible only to those with press credentials'),
 ('f2_bosses_leave','From Floor 2, bosses can leave their chambers (Floor 1 bosses could not).',SF,'On the Second Floor, bosses gain the ability to leave their chambers.'),
 ('f2_stories','Several Floor 2 mobs belong to overarching set-ups; the big one is the Rev-Up pyramid-scheme storyline.',SF,'a parody of multi-level-marketing moonshine sales run by the floor\'s Krakaren clones'),
 ('f2_no_quests','No formal quests yet; Floor 2 stories play out shallowly or on their own.',SF,'With no formal quests yet (those begin deeper in the dungeon), these stories play out shallowly or unfold on their own.'),
 ('f2_behind','Behind the scenes Borant is accelerating the crawl at the Bloom\'s insistence (shorter timers, bugs, overpowered mobs).',SF,'is actively accelerating the crawl by shortening timers'),
 ('f2_council','By Floor 2 the Crawl Council has put Borant on notice about violations.',SF,'the Crawl Council has put Borant on notice'),
 ('f2_morning','First Floor 2 morning staff update: twelve Site Prep workers were swallowed whole.',SF,'reports twelve Site Prep workers swallowed whole'),
 ('f2_timeline_open','Timeline: Crawlers can begin exploring the Second Floor about 6 d 6 h before collapse; the countdown starts six hours later.',SF,'Crawlers can begin exploring the Second Floor.'),
 ('f2_timeline_ep5','Timeline (about 4 d 18 h left): episode 5 shows Carl, Donut and the Meadow Lark party in a safe room with a Rage Elemental outside.',SF,'Dungeon Crawler World: Earth (episode 5) features Carl, Donut, and the Meadow Lark party camped in a safe room while a Rage Elemental lurks outside.'),
 ('f2_patch_hedgehog','Patch notes (4 d 17 h left): Satan\'s Lil\' Hedgehogs are moved to a deeper floor.',SF,'The Satan\'s Lil\' Hedgehogs mob is relocated to a deeper floor.'),
 ('f2_patch_hedgehog_why','The Hedgehogs were pulled because their armor-piercing quills were judged too strong.',SF,'its armor-piercing quills deemed too strong'),
 # ---- grubs
 ('grub_spawn','Brindle Grubs are the Floor 2 janitor mob: 1 to 15 spawn per corpse, capped at 5,000 per quadrant.','W:Brindle Grub','One to fifteen Brindle Grubs are spawned every time a corpse is created until their numbers cap out at 5,000 per quadrant.','YT'),
 ('grub_corpses','Destroying corpses stops grubs growing but not spawning; hordes then drive Crawlers out of secured neighborhoods.','W:Brindle Grub','Destroying corpses prevents Brindle Grubs from leveling up but not from spawning'),
 ('grub_swarm','A swarm of grubs chases Crawlers out of otherwise secured neighborhoods.','W:Brindle Grub','chasing crawlers out of otherwise secured neighborhoods'),
 ('grub_basic','Basic grubs are fuzzy, fat, cat-sized worms with black-and-brown tortoiseshell coloring.','W:Brindle Grub','fuzzy, fat, cat-sized worms with tortoiseshell-like black and brown coloring'),
 ('grub_goo','Grubs are slow and squeaky and burst into white goo on impact, with no special attacks.','W:Brindle Grub','They move slowly, make pitiful squeaking noises, and their squishy innards explode into white goo on impact.'),
 ('grub_hemolymph','Grub corpses drop hemolymph, an alchemy material.','W:Brindle Grub','Their corpses drop Brindle Grub Hemolymph, a type of alchemy material.'),
 ('grub_cowtail','Late-stage Cow-Tailed grubs are bigger and have ineffective whip tails.','W:Brindle Grub','long, pointed tails that they whipped ineffectively'),
 ('grub_pupa','The pupa stage is a wet, pulsating sac about the size of a standing human with red and yellow lights flashing inside.','W:Brindle Grub','The grub pupae are wet, pulsating sacs and roughly the size of a human standing up'),
 ('grub_pupa_timer','A pupa carries a visible countdown of at least ten hours.','W:Brindle Grub','A countdown timer (of at least 10 hours) appears above the mob and in the mobs\' icon.'),
 ('grub_vespa_emerge','When the pupa countdown ends, a Brindled Vespa emerges.','W:Brindle Grub','When the countdown reaches zero, the Brindle Grub emerges as a Brindled Vespa.'),
 ('grub_pupa_burst','Bursting a pupa early releases convulsing "uncooked" human-sized creatures.','W:Brindle Grub','If the sac is destroyed before the timer expires, then "uncooked" human-sized creatures "vomit" from the sac and begin convulsing.'),
 ('grub_vespa_look','Brindled Vespas look like hornets that spit acid globs of white goo.','W:Brindle Grub','looks like a hornet that spit acid globs of white goo'),
 ('grub_patch_pupa','Patch (3 d 11 h left): grubs still spawn on every corpse but have only a 50% chance to reach the pupa stage.',SF,'Brindle Grubs continue to generate on every corpse, but now have only a 50% chance of advancing to the pupa stage.'),
 ('grub_patch_vespa','Patch: the Vespa population is halved and their acid spit is lowered slightly.',SF,'The Brindled Vespa population is reduced by 50%, and their acid-spit damage is lowered slightly.'),
 ('grub_story','Carl and Donut\'s Krakaren fight and kills trigger a janitor-grub infestation that swarms the neighborhood and traps Meadow Lark.',SF,'their kills trigger a massive janitor-grub infestation that swarms the neighborhood and traps the group'),
 ('grub_ch37','Chapter 37 summary: grubs hit the spawn limit near the group; Carl and Donut rejoin Meadow Lark and head to the stairs.',CS,'Brindle Grubs start to become an issue as the immediate area hits the spawn limit.','CS:37'),
 ('grub_vs_elemental','The Rage Elemental tears through thousands of grubs without disappearing (grubs may have no souls).','W:Brindle Grub','It tears through thousands of the grubs but does not disappear'),
 # ---- mind horror / dingo / kobold / ralph
 ('mh_look','Mind Horrors are jellyfish-like floating brains with dangling tentacles.','W:Mind Horror','Mind Horrors are jellyfish-like floating brains with dangling tentacles.'),
 ('mh_body','Mind Horror bodies feel like a jam-filled kickball and may bounce or splatter.','W:Mind Horror','consistency of a jam-filled kickball'),
 ('mh_psionic','The psionic attack seems not to bother high-Intelligence Crawlers but gives others a near-debilitating headache.','W:Mind Horror','causes a nearly debilitating health-sapping headache in other creatures'),
 ('mh_slow','Mind Horrors are physically weak and slow.','W:Mind Horror','They are physically weak and move slowly'),
 ('mh_first','Carl and Donut meet Mind Horrors soon after arriving, on the way to a safe room.','W:Mind Horror','Carl and Donut encounter a group of Mind Horrors shortly after entering the Second Floor as they try to find a Safe Room.'),
 ('mh_guide','Frank Q and Maggie My\'s Game Guide is a Mind Horror with a deep, rumbly voice.','W:Mind Horror','Frank Q and Maggie My have a Mind Horror as their game guide'),
 ('dingo_look','Danger Dingoes are mastiff-sized with huge fangs and fur that looks like heavy-metal corpse paint.','W:Danger Dingo','The fur on their faces looks like heavy metal corpse paint.'),
 ('dingo_masters','Dingoes come with Kobold riders and slave masters nearby.','W:Danger Dingo','Where there are dingoes, their Kobold riders and slave masters usually aren\'t far behind.'),
 ('dingo_control','A fan site says Kobolds hold the dingoes with a control spell that breaks in the Ralph fight.','FW2:book1-bestiary','Danger Dingoes are enslaved by Kobolds via a control spell.','UNVERIFIED'),
 ('dingo_biscuit_dot','Feeding a caged dingo a Pet Biscuit turns its map dot from red to white (hostile to neutral).','W:Ralph','The dot on the Map goes from red to white.','FW2:book1-bestiary'),
 ('dingo_fed_all','Carl feeds every caged dingo, turning them all white before the boss fight starts.','W:Ralph','Carl feeds all the dingos in the pet cages, turning them all white.'),
 ('kobold_chi','Kobolds are small, fearless, yappy chihuahua-like brawlers who bite first.','W:Kobold','The DNA of a kobold and the DNA of a chihuahua are almost identical.'),
 ('kobold_lance','Kobold Riders charge on Danger Dingoes with long feathered spears used like lances.','W:Kobold','wield long, feathered spears like lances'),
 ('ralph_pound','The Kobold boss chamber is a Portuguese municipal dog pound with three hallways of cages, loud distorted-barking music.','W:Ralph','The chamber itself is from a Portuguese municipal dog pound, with three hallways flanked by cages.'),
 ('ralph_kobolds','About forty Kobolds escort Ralph, who comes out of a small metal cage.','W:Ralph','There are about 40 Kobolds, with one opening a small metal cage with Ralph in it.'),
 ('ralph_look','Ralph looks like an absurdly cute gerbil until his mouth opens wider than physically possible.','W:Ralph','opens wider than physically possible'),
 ('ralph_ai','Ralph is the champion pit fighter of the kobold training grounds, perpetually enraged; the AI intro is a gerbil/Black Death history lesson.','W:Ralph','champion pit fighter of the kobold training grounds, lives his life in a perpetual state of rage'),
 ('ralph_regular','Ordinary Frenzied Gerbils are normal mobs on later floors; Ralph is the special case.','W:Frenzied Gerbil','Frenzied Gerbils are regular mobs one might encounter on the fifth or seventh floors.'),
 ('ralph_fight','The first dingo Carl fed eats Ralph whole while the others attack the Kobolds.','W:Ralph','The first dingo Carl fed eats Ralph whole, while the others tear into the remaining Kobolds.'),
 ('ralph_phase2','Ralph is not dead: the dingo\'s head explodes and he emerges; a punch stuns him and Carl ends it with a bare foot.','W:Ralph','Just then, the dingo\'s head explodes, with Ralph emerging from the corpse.'),
 ('ralph_ch45','Chapter 45 summary: the fed dingoes are kept from joining the boss\'s side; Carl must "pay the daddy tax".',CS,'Carl and Donut find the Kobold boss chamber and feed some caged dingoes','CS:45'),
 ('reward_room','Chapter 46 summary: after Ralph, Carl and Donut find the reward room and Mongo joins the Royal Court.',CS,'Carl and Donut discover the reward room, Mongo joins the Royal Court','CS:46'),
 ('reward_key','The Kobold corpse\'s key is the selection mechanism of the pet reward room.','W:Reward Room','The key that Carl obtains from the Kobold corpse on the Second Floor is an example of a selection mechanism for the room.'),
 ('reward_cages','The Master Pen Key opens the fighters\' and bait animals\' cages in the kobold fighting pits.','W:Reward Room','Opens the individual cages of both the fighters and the bait animals within the kobold fighting pits.'),
 ('mongo_pet','Mongo is a Dungeon-generated pet-class Mongoliensis (tamed on Floor 2 into Donut\'s Royal Steed).','W:Mongo','Mongo is a Dungeon-generated, pet-class Mongoliensis mob'),
 ('mongo_tame','Mongo bonds with Donut after she teaches him to eviscerate Brindle Grubs.','W:Mongo','he bonded with Donut after she taught him how to properly eviscerate Brindle Grubs'),
 # ---- Rev-Up / Krakaren clone
 ('revup_intro','Rev-Up is an MLM-style pyramid scheme run by the "Krakaren cooperative"; first seen on Floor 2.','W:Rev-Up','Rev-Up is introduced on the Second Floor as an MLM-type pyramid scheme'),
 ('revup_chain','Clurichauns make the moonshine, Laminak Elites oversee them, and a Krakaren Clone tops the pyramid.','W:Rev-Up','who genuinely believe that their work for Rev-Up will allow them to move to the Third Floor'),
 ('revup_pamphlet','Rev-Up pamphlets pitch making money and moving to the next floor down.','W:Rev-Up','Make Money. Be Your Own Boss. Move to the next floor down.'),
 ('revup_damien','Damien is at least partly involved in creating or maintaining the Rev-Up story.','W:Rev-Up','A dungeon administrator named Damien is at least partly involved in creating or maintaining this story.'),
 ('revup_satire','Rev-Up is political satire of the Apothecary and the Plenty (a later-book reveal).','W:Rev-Up','created as a political satire of the Apothecary and the Plenty'),
 ('clur_look','Clurichauns are small, troll-like fairies with big heads, black curls and few teeth.','W:Clurichaun','Small and troll-like with humanoid bodies and oversized heads'),
 ('clur_attack','Clurichauns use slingshots and rock bags, may grapple, and move impossibly fast.','W:Clurichaun','They are armed with Slingshots and little bags of rocks, but may opt to grapple instead; they can move impossibly fast.'),
 ('clur_taint','Touching an unvaccinated clurichaun leaves oily lime-green residue and the Taint for five minutes.','W:Clurichaun','their skin will be covered in an oily, lime green residue, and they will be infected with the Taint for five minutes'),
 ('clur_corpse','Clurichaun corpses ooze a toxic liquid.','W:Clurichaun','Unvaccinated clurichaun corpses ooze a clear toxic liquid.'),
 ('clur_banjo','The AI nameplate jokes: if you hear banjo music, run.','W:Clurichaun','If you hear banjo music, run.'),
 ('clur_opening','Carl and Donut meet three Unvaccinated Clurichaun Rev-Up Consultants at the start of Floor 2; Donut kills them from range.','W:Clurichaun','Carl and Donut come across a group of three Unvaccinated Clurichaun Rev-Up Consultants at the start of the Second Floor.'),
 ('lam_look','Laminaks are fat, crow-sized fairies with hummingbird wings.','W:Laminak','They are fat, human-like, crow-sized fairies with buzzing hummingbird wings.'),
 ('lam_elite','Laminak Elites look like miniature winged soccer moms in leaf pantsuits and can cast Magic Missile.','W:Laminak','with their hair cut in inverted bobs and their pantsuits and dresses made of leaves'),
 ('lam_immune','Laminak Elites resist most health-seeping attacks; their corpses are alchemy material.','W:Laminak','These mobs do not have any special abilities other than immunity to most health-seeping attacks.'),
 ('lam_scream','A dying Laminak Elite screams that they were meant to move to the next floor and calls for Damien.','W:Laminak','The other fairy screams that they were supposed to move to the next floor, and keeps screaming for someone named Damien to help.'),
 ('krak_boss','The Krakaren Clone is a Neighborhood Boss of the running Rev-Up storyline.','W:Krakaren Clone (Second Floor)','The Krakaren Clone is a Neighborhood Boss on the Second Floor, and part of the running Rev-Up storyline.',YT),
 ('krak_instances','There are at least three separate Krakaren Clone instances on the level.','W:Krakaren Clone (Second Floor)','There are at least three separate instances of the Krakaren Clone on the level.'),
 ('krak_ai','AI text: for every Krakaren killed, Krakaren Prime births two more.','W:Krakaren Clone (Second Floor)','For every one that is killed, Krakaren Prime births two more.'),
 ('krak_look','The clone is a 20-ft-tall immobile octopus with a beaked mouth and groups of eyes.','W:Krakaren Clone (Second Floor)','is a 20 ft tall, immobile, octopus monster with a beaked mouth and groups of eyes'),
 ('krak_snot','Its tentacles bear screeching human-style mouths that drip Taint-causing snot.','W:Krakaren Clone (Second Floor)','drip with gooey snot that inflicts the Taint debuff'),
 ('krak_mist','A thinner tentacle sprays a green mist that causes Vigorous Measles.','W:Krakaren Clone (Second Floor)','A longer, thinner tentacle is covered in orifices that spray a fine green mist that causes Vigorous Measles.'),
 ('krak_chamber','The boss door is under cut-out wood letters and is reached through the room where Rev-Up moonshine is distilled.','W:Krakaren Clone (Second Floor)','which is accessed from the large room where Rev-Up Toilet-Grade Moonshine is distilled'),
 ('krak_distillery','The distillery has a bolted-down moonshine tub, an Alchemy Table and two bicycle-powered blenders.','W:Krakaren Clone (Second Floor)','an Alchemy Table, two bicycle-powered blenders, and the recipe for a Rev-Up Immunity Smoothie'),
 ('krak_first','The clone is the first Floor 2 boss fought; it blasts its door open and sends tentacles into the room (the Wait, Bosses Can Leave achievement).','W:Krakaren Clone (Second Floor)','The Krakaren Clone is the first boss that Carl and Donut fight on the Second Floor.'),
 ('krak_walls','The clone\'s tentacles destroy the otherwise unbreakable cinderblock walls.','W:Krakaren Clone (Second Floor)','the Krakaren Clone\'s tentacles destroy them'),
 ('krak_kill','Carl and Donut kill it by sending a Second-Chance-raised clurichaun in with a Jug O\'Boom and goblin dynamite.','W:Krakaren Clone (Second Floor)','sends a resurrected clurichaun into the Krakaren Clone\'s chamber with a Carl\'s Jug O\'Boom and a stick of Goblin Dynamite'),
 ('taint_def','The Taint is a five-minute debuff that blocks all healing.','W:Taint','The Taint is a five-minute debuff that prevents the target from healing.'),
 ('measles_def','Vigorous Measles is a communicable disease spread by aerosol attacks.','W:Vigorous Measles','Vigorous Measles is a communicable disease that can be transmitted by aerosol-based attacks.'),
 ('smoothie_effect','Rev-Up Immunity Smoothie gives immunity to the Taint and Vigorous Measles (prevents, does not cure).','W:Vigorous Measles','Both conditions could be prevented but not cured by consuming a Rev-Up Immunity Smoothie.',YT),
 ('smoothie_buzz','The smoothie also inflicts the Buzzed debuff.','W:Rev-Up Immunity Smoothie','Inflicts the Buzzed Debuff.'),
 ('damien_loc','Damien oversaw the Rev-Up and Krakaren Clone areas as Location Manager.','W:Damien','Damien was responsible for overseeing the Rev-Up and Krakaren Clone (Second Floor) areas on the Second Floor.'),
 ('locmgr_hidden','Location Managers are hidden Borant staff; Game Guides only speak of them if asked directly.','W:Location Manager','Crawlers are not supposed to know about or see them'),
 ('locmgr_three','Only three Location Managers work Floor 2.','W:Location Manager','There are only three (3) Location Managers on the Second Floor.'),
 ('krak_ch34','Chapter 34 summary: Carl and Donut drink a blended corpse and get the Buzzed debuff in the Krakaren fight.',CS,'Carl and Donut drink a blended corpse and get the Buzzed Debuff.','CS:34'),
 # ---- Rage Elemental
 ('re_origin','Rage Elementals come from the thirteenth floor and are deployed as a penalty, not an encounter.','W:Rage Elemental','Rage Elementals are mobs drawn from the Thirteenth Floor of the Dungeon and deployed on lower floors as a penalty rather than as an encounter.'),
 ('re_dissipate','The almost-indestructible elemental is said to dissipate only after claiming 666 souls.','W:Rage Elemental','The almost-indestructible Rage Elemental is said to only dissipate after it has claimed 666 souls.','YT'),
 ('re_smoke','It is mostly smoke: arrows shatter on it and Magic Missile barely registers before it heals.','W:Rage Elemental','arrows shatter against the smoke without generating a health bar at all'),
 ('re_burning','Its self-healing slows against burning damage.','W:Rage Elemental','That self-healing slows noticeably against burning damage.'),
 ('re_gravity','It casts a limited-range Reverse Gravity Spell.','W:Rage Elemental','Beyond their claws they cast a Reverse Gravity Spell of limited range'),
 ('re_look','Six legs with obsidian rake-sized claws, a horned badger-like skull and burning red eyes in black and purple smoke.','W:Rage Elemental','Six legs end in gleaming obsidian claws the size of rakes'),
 ('re_door','It hammers on a safe room door for hours without tiring.','W:Rage Elemental','An elemental never tires, hammering on a safe room door for hours without pause.'),
 ('re_eject','Opening a safe room door ejects it to the main hallway; it takes 75 to 120 seconds to return.','W:Rage Elemental','it is ejected when a safe room door is opened, teleporting out to the main hallway and taking 75 to 120 seconds to return'),
 ('re_pupae','It ignores grubs in the pupa stage.','W:Rage Elemental','while ignoring those already in the pupa stage'),
 ('re_stair_kill','The elemental is killed by sliding it on an oil slick into a stairwell hole, where descent rules destroy it.','W:Rage Elemental','The elemental hit the oil, slid into the stairwell, and was destroyed.'),
 ('re_summon','Jack relieving himself on a wall summons the Rage Elemental that kills Yolanda and Randall.','W:Bathrooms','Jack pees on the wall on the Second Floor, summoning the Rage Elemental that Carl and Donut fight.'),
 ('re_ch38','Chapter 38 summary: Yolanda kills Jack, then dies protecting Randall as gravity reverses.',CS,'Yolanda kills Jack and then dies trying to protect Randall from the Rage Elemental.','CS:38'),
 ('re_ch40','Chapter 40 summary: the Bomb Chicken drive ends with the elemental destroyed via an exploit.',CS,'Several bombs, obstacles, and a significant exploit later, the rage elemental is no more.','CS:40'),
 ('re_ch31','Chapter 31 summary: the announcement warns of Rage Elementals.',CS,'An announcement warns of Rage Elementals','CS:31'),
 # ---- other mobs / gaps
 ('impaler','Shambling Acid Impalers: hairy green four-legged acid-dart spitters; the wiki places them in previous seasons.','W:Shambling Acid Impaler','Shambling Acid Impalers were a common Second Floor mob in previous Borant Corporation-hosted seasons of Dungeon Crawler World.'),
 ('impaler_warn','Mordecai warned the Shambling Acid Impalers would be everywhere on Floor 2.',SF,'the Shambling Acid Impalers Mordecai warned would be everywhere'),
 ('blimp_boss','A "Giant Blimp" neighbourhood boss was killed by Yolanda\'s bow with Brandon and Chris; only one wiki page, no mob page.','W:Yolanda Martinez','neighbourhood boss thanks largely to Yolanda and her bow'),
 ('blimp_float','Wood salvaged from a blimp-shaped boss became the frame of the ten-car parade float.','W:Brandon Andrews','salvaged wood from a blimp-shaped boss became the frame of a ten-car parade float built to move the residents toward the stairwell'),
 ('ml_descend','Chapter 41 summary: 36 Meadow Lark residents and 3 staff descend to Floor 3.',CS,'36 Meadow Lark residents and 3 members of staff descend to the 3rd floor.','CS:41'),
 ('ml_ten_car','Meadow Lark staff move the frail residents in a ten-car float through a hallway choked with grubs.','W:Chris Andrews','To move the frail residents through a hallway choked with janitor grubs'),
 ('tiatha_stairs','Mistress Tiatha told Brandon every borough and city boss on the first four or five floors would have a stairwell.','W:Mistress Tiatha','all borough and city bosses on the first four or five levels would have Stairwells'),
 ('tiatha_drink','Mistress Tiatha, Meadow Lark\'s manager, drinks and smokes blitz sticks.','W:Mistress Tiatha','She has a drinking problem and smokes blitz sticks.'),
 # ---- NPCs / media
 ('zev_role','Zev is a low-ranked Borant liaison between the company and privately produced shows.','W:Zev','low-ranked liaison between her company and the privately-produced shows that want to feature crawlers'),
 ('zev_suit','For the first three floors, where staff have no protection, Zev wears a full water-filled suit.','W:Zev','For her first three floors, where staff receive no protections'),
 ('zev_ch35','Chapter 35 summary: Zev appears; Mordecai is now a Bugaboo in the guild hall.',CS,'They visit Mordecai, now a Bugaboo','CS:35'),
 ('zev_suspended','The System AI suspends Zev for warning Carl about the Rage Elemental, and Mukta takes over PR.','W:Mukta','after the System AI suspends Zev for warning Carl about the Rage Elemental'),
 ('mukta_role','Mukta is a Kua-Tin Bloom member in Borant\'s Communications Department.','W:Mukta','Mukta is a Kua-Tin member of the Bloom, and an employee in Borant Corporation\'s Communications Department.'),
 ('mukta_remote','Unlike Zev, Mukta never enters the Dungeon and closes his chats.','W:Mukta','he never enters the Dungeon to talk in person, and he closes his chats to prevent crawlers from messaging him'),
 ('mukta_booking','Mukta cancels the Dungeon Crawl Tactics booking and rents the pair to Death Watch because it pays a higher fee.','W:Mukta','Mukta cancels the booking and rents them to Death Watch Extreme Dungeon Mayhem because it is paying a higher fee.'),
 ('mukta_free','Mukta tells Carl the show paid for his appearance and nothing else.','W:Mukta','They have paid for your appearance.  Nothing else.'),
 ('dw_format','Death Watch Extreme Dungeon Mayhem is a tunneled round-table game show hosted by Prince Maestro.','W:Death Watch Extreme Dungeon Mayhem','a tunneled, round-table game show hosted by Prince Maestro of the Skull Empire'),
 ('dw_segment','The Death Watch segment pulls Crawlers from the brink of death into a guessing game for a chance to live.','W:Death Watch Extreme Dungeon Mayhem','Its signature Death Watch segment plucks crawlers from the brink of death and makes them play guessing games for a chance to live.'),
 ('dw_freeze','Death Watch guests are held in a Time Freeze spell until the episode ends.','W:Death Watch Extreme Dungeon Mayhem','held there by a Time Freeze spell that lasts until the episode ends'),
 ('dw_points','Each correct guess earns a teleport point.','W:Death Watch Extreme Dungeon Mayhem','each correct guess earns a teleport point'),
 ('dw_audience','The studio audience is mostly pre-teen and early-teen boys, Maestro\'s "piglets".','W:Death Watch Extreme Dungeon Mayhem','The studio audience is loud and made up almost entirely of pre-teen and early-teen boys'),
 ('dw_not_live','Episodes are not normally broadcast live.','W:Death Watch Extreme Dungeon Mayhem','Episodes are not normally broadcast live.'),
 ('dw_trailer','The episode is tunneled from a rented trailer, with a robot greeter named Mexx-55.','W:Death Watch Extreme Dungeon Mayhem','a black, metallic, frisbee-shaped greeter robot named Mexx-55'),
 ('dw_syndicate','The Skull Empire is a Syndicate member, so Borant cannot discriminate against its production companies in scheduling.','W:Death Watch Extreme Dungeon Mayhem','Borant cannot discriminate against its production companies when scheduling crawler appearances.'),
 ('dw_frozen_scene','Li Jun and Zhang play for companions frozen mid-ambush between Troglodytes and a nest of Brindled Vespas.','W:Death Watch Extreme Dungeon Mayhem','between a pack of Troglodytes and a nest of Brindled Vespas'),
 ('dw_carl_gamble','Carl demands the two points be spent moving him and Donut into the frozen scene, betting Maestro cannot risk his guest stars.','W:Death Watch Extreme Dungeon Mayhem','Carl demanded that the two points instead be spent transferring him and Donut into the frozen scene'),
 ('dw_hiatus','Death Watch Extreme Dungeon Mayhem announces a hiatus for restructuring after the fallout.','W:Maestro','Death Watch Extreme Dungeon Mayhem announces a hiatus for restructuring'),
 ('maestro_look','Maestro is a huge, muscular boar-like orc with a gold tusk, about six and a half feet tall.','W:Maestro','a huge, muscular orc about six and a half feet tall'),
 ('maestro_temper','Maestro is cruel, condescending and egotistical.','W:Maestro','Maestro is cruel, condescending, and egotistical'),
 ('maestro_ch42','Chapter 42 summary: Carl gambles on his importance to save Li Jun, Li Na, Zhang and their boss from the Vespas.',CS,'Carl gambles on his importance to help them, their boss, and Li Jun\'s sister Li Na escape the Brindled Vespas they\'re facing.','CS:42'),
 ('snick','The "Pork Boy Snick" fan video spreads; the hiatus and the nickname outlast the show.','W:Maestro','become the subjects of a fan fiction video'),
 ('qwist','Qwist, a Bopca Protector, staffs the Big Shot Chicken safe room.','W:Qwist','Qwist is a Bopca Protector who staffs the Big Shot Chicken safe room where Carl and Donut shelter early in their crawl.'),
 ('qwist_job','Bopca Protectors manage, clean and cook for their safe room.','W:Qwist','Qwist manages, cleans, and cooks for the safe room'),
 ('manatoast_def','Mana Toast is a burned triangle of toast that restores mana.','W:Mana Toast','Mana Toast is a burned triangle of toast that restores mana.'),
 ('manatoast_where','An unmanned Floor 2 safe room has a toaster oven handing out one Mana Toast per Crawler.','W:Mana Toast','Carl and Donut each receive one piece of toast from a metallic toaster oven in an unmanned safe room on the Second Floor.'),
 ('club_def','The Dungeon Book of the Floor Club mails members one new Tome each floor.','W:Dungeon Book of the Floor Club','The Dungeon Book of the Floor Club is a Dungeon Benefit which delivers one new Tome to members on each floor.'),
 ('club_mailbox','Only subscribers can open the safe-room mailboxes, which look like suburban mailboxes with the flag up.','W:Dungeon Book of the Floor Club','only crawlers who participate in the Dungeon Book of the Floor Club or similar subscription services can open the boxes'),
 ('club_lost','A tome not collected before the floor collapses is destroyed in the collapse (later-book rule).','W:Dungeon Book of the Floor Club','the book is destroyed in the collapse'),
 ('club_f2','Donut gets her first Floor Club tome (Second Chance) on Floor 2.','W:Dungeon Book of the Floor Club','They receive their first tomes on the Second Floor.'),
 ('agatha_cart','Agatha pushes her cart into the stairwell where Carl and Donut are camped; the cart held illegal Valtay items.','W:Agatha','Minutes later Agatha pushes her cart into the stairwell where he and Donut are camped.'),
 ('agatha_valtay','Carl later finds three Valtay items in his inventory history that could only have come from her cart.','W:Agatha','Carl later finds three Valtay items in his inventory history that could only have come from her cart'),
 ('agatha_arrival','Agatha is edited out of the recap footage of Dungeon Crawler World: Earth (first noted on Floor 2).','W:Agatha','She is edited out of the recap footage on Dungeon Crawler World: Earth'),
 ('epilogue','Epilogue (end of Floor 2): Odette\'s show covers Pork Boy, Mongo, race selection and Valtay.',CS,'Carl and Donut appear on Odette\'s show and talk Pork Boy, Mongo, race selection, and Valtay.','CS:Epilogue'),
 ('ch44_under_million','Chapter 44 summary: another recap, a Le Mouvement wipe, and the crawler count falls under one million.',CS,'Another recap, Le Mouvement wipe, and the number of crawlers goes under 1 million.','CS:44'),
 ('ch30_summary','Chapter 30 summary: Carl and Donut battle Grubs, Dingoes and Mind Horrors; a safe room gives Donut the Floor Club\'s Second Chance.',CS,'Carl and Donut battle Brindle Grubs, Danger Dingoes, and Mind Horrors.','CS:30'),
 ('ch33_summary','Chapter 33 summary: the pair skip the boss chamber but the boss has other ideas.',CS,'They decide to skip the boss chamber but the boss has other ideas.','CS:33'),
]

# web-only rows (no quote; see sources/web/f02-web-snippets.txt): key, summary, WEB slug(s)
WEB = [
 ('web_pet_room_ten','Afterword chapter summaries: the Kobold arena after Ralph is a pet reward room with a line of ten cages; Mongo is in the last one. (WEB:afterword-b1-ch46)','WEB:afterword-b1-ch46'),
 ('web_fourteen_dingoes','Afterword chapter summaries count fourteen caged dingoes (ch45) but thirteen that flee (ch46); the counts are inconsistent. (WEB:afterword-b1-ch45)','WEB:afterword-b1-ch45; WEB:afterword-b1-ch46'),
 ('web_835','Afterword ch37 summary: the grub flood followed a boss battle in which 835 monsters died. (WEB:afterword-b1-ch37)','WEB:afterword-b1-ch37'),
 ('web_stair_minimap','Recap sites: on arrival the stairwell to Floor 3 is already visible on the minimap (northeast corner). (WEB:manatoastmedia-b1-recap)','WEB:manatoastmedia-b1-recap'),
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

# conflicts: key, topic, A (text or None -> quote find), srcA, B, srcB, status
X = [
 ('x_krak_tier','Tier of the Floor 2 Krakaren Clone boss',
  ('W:Krakaren Clone (Second Floor)','The Krakaren Clone is a Neighborhood Boss on the Second Floor'),
  ('FW2:book1-bestiary','Giant sac mobs. When damaged, release Brindled Vespas.') if False else ('note','a fan bestiary table lists Krakaren under Floor 2 bosses as a Borough Boss (chapter 35); the recap transcript says neighborhood boss','FW2:book1-bestiary'),
  'OPEN. PREFERRED: Neighborhood Boss (AI nameplate text on the wiki and the recap transcript agree). The Borough listing is a single fan-site table.'),
 ('x_pupa_burst','What a damaged grub pupa releases',
  ('W:Brindle Grub','If the sac is destroyed before the timer expires, then "uncooked" human-sized creatures "vomit" from the sac and begin convulsing.'),
  ('FW2:book1-bestiary','Giant sac mobs. When damaged, release Brindled Vespas.'),
  'OPEN. PREFERRED: wiki text (uncooked convulsing creatures from a burst sac; Vespas emerge only when the timer ends). Fan table is a simplification.'),
 ('x_patron_start','Which floor the patron auctions start on',
  (SF,'all three spots will be up for auction for one day immediately upon the induction of the fourth floor'),
  (YT,'Spots go to auction at the start of each floor starting with floor three'),
  'OPEN. PREFERRED: the wiki\'s transcription of the announcement (fourth floor). The transcript is auto-captioned; one recap site says "start of each floor".'),
 ('x_timer_house','Floor 2 timer: canon six days vs the house 10-day clock',
  (SF,'the collapse timer was cut to the Syndicate legal minimum of six days, rather than the ten that guides like Mordecai had anticipated.'),
  ('note','house decision 026 (Caleb, 2026-10-04) sets Floor 2 = 10 days; canon says ten was the normal length and six was a one-off cut. Read-only note; decision file lives in dcc-campaign/decisions/','house:decisions/026'),
  'HOUSE OVERRIDE (not a canon error). PREFERRED for the RPG: 10 days per decision 026, tagged inspired. Keep the canon fixed points regardless of day count: safe rooms close 1 h before collapse (M-012) and free descent in the last 6 h.'),
 ('x_impaler','Whether Shambling Acid Impalers appear on Floor 2 in the book',
  ('W:Shambling Acid Impaler','Shambling Acid Impalers were a common Second Floor mob in previous Borant Corporation-hosted seasons of Dungeon Crawler World.'),
  (SF,'the Shambling Acid Impalers Mordecai warned would be everywhere'),
  'OPEN. Both are wiki statements; no on-page Impaler encounter is recorded. Treat as a warning rumor, not a seen mob, until the novel is checked.'),
 ('x_grub_kill_count','How many grubs the Rage Elemental shreds',
  ('W:Rage Elemental','shredding thousands of Brindle Grubs in under a minute'),
  ('note','a chapter-summary site says it kills 666 grubs before returning to the door (WEB:afterword-b1-ch39)','WEB:afterword-b1-ch39'),
  'OPEN (minor). PREFERRED: wiki ("thousands"). The 666 figure may echo the soul count joke. Unverified against the novel.'),
 ('x_tuskling_f2','Tusklings listed under Floor 2 mobs',
  ('FW2:book1-bestiary','Overweight orc aristocrats. Weak individually; catastrophic in Ball of Swine formation.'),
  ('W:Ball of Swine','Once the sphere pops, the encounter drops into a standard skirmish against more than thirty dazed targets') if False else ('note','the Ball of Swine is the Floor 1 Borough Boss and its Tuskling Knights are Floor 1 (ledger M-263..M-326 section 9.1)','W:Ball of Swine'),
  'OPEN. PREFERRED: Tusklings belong to Floor 1; the Floor 2 bestiary table row is a placement glitch. Not used in the Floor 2 canon table.'),
]

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
        tags = tag; conf = None
        if extra == 'UNVERIFIED': conf = 'UNVERIFIED (single fan-site claim; not confirmed by a second source)'
        elif extra == 'YT': tags = f'{tag}; {YT}'
        elif extra and extra.startswith('CS:'):
            conf = f'VERIFIED (chapter-summary row B1 ch{extra[3:]})'
        elif extra: tags = f'{tag}; {extra}'
        if conf is None:
            if kind == 'sentence': conf = f'VERIFIED (cite {fmt(cs)})'
            elif kind == 'page': conf = f'VERIFIED (page cite {fmt(cs)})'
            else: conf = 'WIKI-ONLY'
            if extra and (extra.startswith('FW2') or extra == 'YT' or tag.startswith('FW2')):
                conf = (conf + '; 2 families') if conf.startswith('VERIFIED') else 'VERIFIED (2 sources)'
        quote = core.replace('|', '\\|')
        if key in OVERRIDE: conf = OVERRIDE[key]
        rows.append(f'| {rid} | {summ} | "{quote}" | {tags} | {conf} | {DATE} |')
        idmap[key] = rid
    if len(rows) != len(R): print('ABORT: some rows failed'); sys.exit(2)
    n = START + len(R)
    for k, summ, slug in WEB:
        rid = f'M-{n}'; n += 1
        rows.append(f'| {rid} | {summ} | \u2014 (no quote; web chapter summary, see sources/web/f02-web-snippets.txt) | {slug} | UNVERIFIED (web-only chapter-summary claim; no quote; not read against the novel) | {DATE} |')
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
    block = ['', '### 9.2 Floor 2 rules, creatures, hazards, NPCs and set-pieces (Pass 19, 2026-10-04; prefix M- continues mechanics rulings; feeds tables/canon-floor-2.json, status "reserve")',
             'Source: local Fandom mirror pages, one FW2 bestiary and one YouTube recap transcript (auto-captions), plus web chapter-summary snippets saved in `sources/web/f02-web-snippets.txt` (web-only rows have no quote and are labelled UNVERIFIED). Same caveat as section 0: nothing here was read against the novels. Quotes are wiki wording, not novel text. "page cite" = a chapter cite sits elsewhere in the same paragraph of the wiki page; "chapter-summary row" = the row comes from the wiki\'s Book 1 chapter table. Levels, difficulty, credits and loot amounts are deliberately not captured (Syndicate rules/10 and the loot decks own them). Existing Floor 2 anchors stay where they are: M-010..M-016 (safe rooms, stairwells), A-123/A-034/A-047/A-071/A-083/A-091/A-131/A-136 (achievements), B-004/B-005/B-029, H-004/H-021/H-028, T-007..T-009.',
             '', '| ID | Ruling (paraphrase) | Source quote (<=25 words) | Source | Confidence | Date |', '|---|---|---|---|---|---|'] + rows + ['',
             f'#### 9.2c Floor 2 conflicts (X-{XSTART:03d}..X-{XSTART+len(X)-1:03d})', '',
             '| ID | Topic | Reading A (quote or note) | Source A | Reading B (quote or note) | Source B | Status | Date |', '|---|---|---|---|---|---|---|---|'] + xrows + ['']
    marker = '### Pass log'
    idx = led.index(marker)
    new = led[:idx] + '\n'.join(block).lstrip('\n') + '\n' + led[idx:]
    json.dump(idmap, open(ROOT + '/work/pass19-row-map.json', 'w'), indent=1)
    print('rows', len(rows), f'M-{START}..M-{last_m}', 'X', len(xrows))
    if dry:
        print('\n'.join(block)[:3000]); return 0
    open(LEDGER, 'w').write(new)
    print('appended')
    return 0
sys.exit(main())
