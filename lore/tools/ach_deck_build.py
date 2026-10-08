#!/usr/bin/env python3
"""Builds tables/loot-decks/ach-f01-orientation-pit.json (schema achievement-deck/0.1).
Project Floor 1 = The Orientation Pit (dcc-campaign/floors/f01/00-overview.md), NOT the book Over City.
Alpha entries come from characters/*.md, gm-notes/10-open-threads.md and the credit ledger; wording is the project's own
(floor doc §10 toast lines, audit R1 samples) because spoken banner text was never archived (audit O1/R3)."""
import json, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tables", "loot-decks", "ach-f01-orientation-pit.json")
L = []
def add(title, zone, trigger, desc, kind, tier=None, box=None, credits=0, title_aw=None, cat="", src="HOUSE", ledger=(),
        alpha=None, status="proposed", hidden=False, trail=False, reward_line=None, notes="", inspiration=False):
    n = len(L) + 1
    if reward_line is None:
        if kind == "box":
            reward_line = "Reward: You've received a %s %s!" % (tier, box)
        else:
            raise SystemExit("reward_line needed: " + title)
    L.append({"id": "ach-f01-%04d" % n, "title": title, "floor": 1, "zone": zone, "trigger": trigger,
      "description": desc, "reward_line": reward_line, "reward_kind": kind, "reward_tier": tier, "box_name": box,
      "credits": credits, "title_awarded": title_aw, "heroic_inspiration": inspiration, "catalog_id": cat,
      "source_tag": src, "ledger_ids": list(ledger), "alpha_earned": bool(alpha), "alpha_crawler": alpha,
      "text_status": status, "hidden": hidden, "trailblazing": trail, "notes": notes})

CI, H, CA = "CANON-INSPIRED", "HOUSE", "CANON"
TC = "title_credits"
def tc(t, quip): return 'Reward: Title "%s" and 25 credits. %s' % (t, quip)

# ================= ALPHA-EARNED (in project files, 2026-10-04) =================
LOG = "alpha: earned per characters/*.md; description proposed (spoken text unlogged)"
add("Don't Skip Intro","z01","Sat through Proctor Bell's whole spiel",
 "You listened to the whole tutorial. Like a nerd. A live nerd, for now.","snark",
 reward_line="Reward: Nothing. Listening was the reward.",cat="ACH-0079",src=CI,ledger=["A-007","A-025"],alpha="Bone Wifebeater + Horn",status="floor doc §10.1 line; reward line proposed",notes="R0. Canon snark-only reward pattern. Alpha: given to both crawlers 14:59 CT.")
add("Grease Tube Disposal","z02","Killed a Vent Rat with Magic Missile",
 "You sent a rat down the grease tube with a spell. Its cousins are already filing paperwork.","box","Bronze","Pest Control, Magical Edition Box",
 cat="NEW",src=CI,ledger=["L-001","L-B02"],alpha="Horn",status="alpha: name and Bronze box logged; description + box name proposed",notes="Alpha Bronze for Horn (opened later: 50 credits + Driftglobe). Name 'Grease Tube Disposal' is in OT:117.")
add("You Better Fucking Listen","z02","First Rage + signature maul kill of a Vent Rat",
 "You hit a rat until it understood. The rat was listening. It just couldn't help itself.","box","Bronze","Talked to the Rat With a Hammer Box",
 cat="NEW",src=CI,ledger=["L-001"],alpha="Bone Wifebeater",status="alpha: name and Bronze logged; description + box name proposed",notes="Signature attack name chosen by the player at intake.")
add("Penalty Kick","z02","Punted a burning rat into a wall (unarmed Rage kill)",
 "You punted a burning rat into a wall. The rat did not see it coming. The rat saw nothing.","box","Bronze","Field Goal Box",
 cat="NEW",src=CI,ledger=["L-001"],alpha="Bone Wifebeater",status="audit R1 sample wording",notes="Audit R1 sample. Alpha Bronze.")
add("Buddy System","z02","Stabilized an ally at 0 HP with a first-aid kit",
 "You saved a teammate. They owe you. Collect before they die.",TC,credits=25,title_aw="Buddy System",
 reward_line=tc("Buddy System","Spend them on someone you like."),cat="ACH-0018",src=H,ledger=["A-148"],alpha="Bone Wifebeater",status="floor doc §10.1 line; reward line audit R2",notes="R1. Credits-for-Titles is HOUSE. +25 logged in credit-ledger seq 4.")
add("Down But Not Out","z02","Stabilized at 0 HP after an Opportunity Attack dropped you",
 "Stabilized! You're alive, technically, which is our favorite kind of alive.",TC,credits=25,title_aw="Down But Not Out",
 reward_line=tc("Down But Not Out","Technically alive pays technically well."),cat="ACH-0015",src=H,ledger=["L-011"],alpha="Horn",status="floor doc §10.1 line; reward line proposed",notes="R1. Canon cousin: Survivor's Box (L-011) for barely surviving. +25 logged seq 9.")
add("Personal Luggage","z02","Hauled an unconscious ally to the nearest saferoom",
 "You carried your friend like a carry-on. The carry-on has feelings, mostly about airlines.",TC,credits=25,title_aw="Personal Luggage",
 reward_line=tc("Personal Luggage","Excess baggage fee waived. This time."),cat="NEW",src=H,alpha="Bone Wifebeater",status="alpha: Title+25 logged; description proposed",notes="R1. +25 logged seq 5.")
add("Warranty Void If Removed","z01","Investigated Proctor Bell's mount: ceiling rails, not floor-bolted",
 "You noticed the ceiling rails. Nobody noticed you noticing.","box","Bronze","Maintenance Closet Box",
 cat="NEW",src=CI,ledger=["L-001"],alpha="Bone Wifebeater",status="audit R1 sample wording",notes="Alpha Bronze for Bone.")
add("Tow Package","z02","Tied self and an unconscious ally to Proctor Bell's booth and got towed Zone 2 to Zone 3",
 "You tied an unconscious friend to a booth and let it drag you both through the building.","box","Bronze","Dead Weight Box",
 cat="NEW",src=CI,ledger=["L-001"],alpha="Bone Wifebeater",status="audit R1 sample wording",notes="Alpha Bronze for Bone (Ath 23 check).")
add("Corpse Lesson","z03","Looted Tanya Ruiz's body",
 "You went through a dead woman's pockets before learning her name. Efficient. Ghoulish. On-brand.","snark",
 reward_line="Reward: A lesson. You may find it in your conscience. Please check.",cat="ACH-0083",src=CI,ledger=["A-007","A-025"],alpha="Bone Wifebeater",status="floor doc §10.1 line; reward line proposed",notes="R0 snark only.")
add("Find a Lore Scrap","z03","Found Tanya's handwritten note",
 "You found a dead woman's diary. Reading it is free. Living with it costs extra.",TC,credits=25,title_aw="Find a Lore Scrap",
 reward_line=tc("Find a Lore Scrap","Some of that is hazard pay."),cat="ACH-0871",src=H,alpha="Bone Wifebeater",status="floor doc §10.1 line; reward line proposed",notes="R1. +25 logged seq 7. Reading it aloud is a separate achievement below.")
add("Vending Gore","z03","Robbed a Snakk-Matic machine that bites (Nat 20 smash)",
 "You robbed a machine that bites. The machine respects you. Nobody else does.",TC,credits=25,title_aw="Vending Gore",
 reward_line=tc("Vending Gore","Try not to spend it all at the machine."),cat="ACH-0077",src=H,alpha="Bone Wifebeater",status="floor doc §10.1 line; reward line proposed",notes="R1. +25 logged seq 8. Fan tobacco pull also fired at this beat (house shortcut).")
add("Tick Sandwich","z03","Peeled two Ceiling Ticks off your body and clapped them together",
 "You peeled two parasites off your own body and clapped them together. Disgusting. Ratings up.","box","Bronze","That-Was-Disgusting Box",
 cat="NEW",src=CI,ledger=["L-B66","L-001"],alpha="Bone Wifebeater",status="audit R1 sample wording",notes="Box name is a canon type (L-B66, WIKI-ONLY). Alpha Bronze; with this Bone logged 5 achievement Bronze, over the 2-4 band that includes the Welcome Box (core §4.5).")
add("Mostly Dead Intern","z02","Floor 1 Reprieve used: ejected to the Break Room at 1 HP",
 "You are not dead. You are an intern. Both are temporary.","title",title_aw="Mostly Dead Intern",
 reward_line='Reward: Title "Mostly Dead Intern". It comes with a lanyard.',cat="NEW",src=H,alpha="Bone Wifebeater",status="alpha: Title logged; description proposed",notes="Mocks the Reprieve, not the death (audit O24). No credits.")
add("Participation Corpse","z03","Floor 1 Reprieve used: ejected to the Break Room at 1 HP",
 "You died on time and attended regardless. The certificate is in the mail.","title",title_aw="Participation Corpse",
 reward_line='Reward: Title "Participation Corpse". Nobody else gets a ribbon.',cat="NEW",src=H,alpha="Horn",status="alpha: Title logged; description proposed",notes="Title only. Reprieve Titles listed in floor doc §1.3.")

# ================= DESIGNED FLOOR 1 (Orientation Pit) =================
add("Coin Slot","z01","Pay Proctor Bell before it finishes its intro",
 "You paid the robot to stop talking. Relatable. Didn't work.","snark",reward_line="Reward: One credit's worth of silence, redeemable never.",cat="NEW",src=H,notes="R0.")
add("Assault on Faculty","z01","Attack Proctor Bell",
 "You punched the teacher. The teacher is glass. The glass is fine. Your hand isn't.","snark",reward_line="Reward: A tutorial on pain.",cat="NEW",src=H,notes="R0. Proctor Bell is an object, 40 HP, not a combatant.")
add("First Blood","z02","First kill of the floor",
 "First kill! It was a rat. Your parents would be so... it was a rat.","item",title_aw="Blooded",
 reward_line='Reward: Title "Blooded" and one flask of oil. Do not drink it.',cat="ACH-0001",src=CI,ledger=["A-149","M-001"],notes="R1. Canon first-kill achievement (A-149, M-001) is the base; reward here is HOUSE.")
add("Land a Critical Hit","any","Roll a natural 20 on an attack",
 "Natural 20. Don't let it go to your head. Your head has enough going on.","snark",reward_line="Reward: Nothing. The crit was the reward. Think about that.",cat="ACH-0894",src=H,notes="R0.")
add("Scenic Panic","any","Panic loudly in chat, then win",
 "You typed 'WE'RE GONNA DIE' in all caps and then won. We heard you scream. In text.","snark",reward_line="Reward: Your screams, preserved for a bloopers reel.",cat="ACH-0205",src=H,notes="R0.")
add("Fed the Machine","z03","Bitten by a Hungry Vendor",
 "You put your hand in a hole with teeth. Your mother would be proud. Of the machine.","snark",reward_line="Reward: A bandage. Pay for it.",cat="NEW",src=H,notes="R0.")
add("Hidden Cache","z03","Find the DC 15 back cage (3b)",
 "You looked behind the machine. Nobody looks behind the machine.",TC,credits=25,title_aw="Hidden Cache",
 reward_line=tc("Hidden Cache","Nobody ever looks. Good for you."),cat="ACH-0177",src=H,notes="R1.")
add("Side Path","zS","Reveal the Service Corridor (Zone S) via the 3b map",
 "You found the staff-only route. Staff are required to hate you.",TC,credits=25,title_aw="Side Path",
 reward_line=tc("Side Path","Keep taking the side paths. We love watching."),cat="ACH-0179",src=H,notes="R1.")
add("Read a Lore Scrap Aloud","z03","Read Tanya's note out loud to the party",
 "You read a dead woman's last words to a room full of cameras. Beautiful. Or content. It's content.","inspiration",
 reward_line="Reward: Heroic Inspiration, if you meant it. A shrug, if you didn't.",cat="ACH-0872",src=H,inspiration=True,notes="R2 if heartfelt; R0 if mocking. Heroic Inspiration max 1 per session (core §3.7). Catalog rarity outlier stepped down.")
add("Odd Coin Pocketed","z03","Open the UNCLAIMED crate in the Lost & Found",
 "Oddity logged.","hidden",hidden=True,reward_line="Reward: (none)",cat="ACH-0081",src=H,notes="HIDDEN, no reward. Spine plant SEED-ODDCOIN. Never explain. GM (2026-10-07): an identify/appraise request to any terminal, vendor or the System gets ITEM NOT RECOGNIZED (or the cancelled 500-credit offer); never name a floor, fee, clearance level or future appraisal.")
add("Rescue a Civilian","z04","Get Dale Pruitt out of the net",
 "You saved Dale. Dale will now talk to you about ductwork. Forever. You did this.",TC,credits=25,title_aw="Lifeguard",
 reward_line=tc("Lifeguard","Dale says thanks. Dale says it again."),cat="ACH-0869",src=H,notes="R1.")
add("Fail to Rescue a Civilian","z04","Dale dies",
 "Dale's dead. The audience is sad. Sad audiences buy merch. So... thanks?","snark",reward_line="Reward: Merch sales are up. You receive none of it.",cat="ACH-0870",src=H,notes="R0 (tasteless to pay 25). Run the permanence popup.")
add("Poison Tolerant","z04","Poisoned, then cured",
 "You got stuck by a dirty needle and lived. Very public-restroom of you.",TC,credits=25,title_aw="Poison Tolerant",
 reward_line=tc("Poison Tolerant","Wash your hands."),cat="ACH-0198",src=H,notes="R1.")
add("Disarm a Trap with Junk","z04","Disarm a trap using gum, shoes or similar junk",
 "You beat a trap with chewing gum. MacGyver's crying. So is the trap.",TC,credits=25,title_aw="Gum Disarmer",
 reward_line=tc("Gum Disarmer","Chew on that."),cat="ACH-0877",src=H,notes="R1.")
add("Literacy Optional","z04","Trigger a trap the signs warned about",
 "Three signs. You read zero. Who raised you? Don't answer. We'll find her.","snark",reward_line="Reward: A fourth sign. Read it.",cat="NEW",src=H,notes="R0. If box-worthy: Bronze Maybe Read the Sign Next Time Box (core §4.8 #5), but only inside the 2-4 Bronze band.")
add("Block a Hit with a Shield","z05","Block an attack with a Shield",
 "You held up a stop sign and it worked. Traffic law remains undefeated.",TC,credits=25,title_aw="Crossing Guard",
 reward_line=tc("Crossing Guard","Please do not run red lights."),cat="ACH-0867",src=H,notes="R1.")
add("Lose Initiative and Still Win","z05","Win a fight after going last",
 "You went last and still won. The audience calls this a comeback. We call it luck with confidence.",TC,credits=25,title_aw="Last Pick",
 reward_line=tc("Last Pick","Last place pays surprisingly well."),cat="ACH-0861",src=H,notes="R1.")
add("Hit the Cutout","z05","Attack a plywood crawler in the Shooting Gallery",
 "That one was plywood. To be fair, it looked smarter than you.","snark",reward_line="Reward: Splinters.",cat="NEW",src=H,notes="R0.")
add("Saferoom Skeptic","z06","Search a certified saferoom for traps",
 "You searched a certified saferoom for traps. Clean. You're paranoid. Stay that way.","item",
 reward_line="Reward: A refilled Thieves' Tools kit or Healer's Kit, your pick. Paranoia pays.",cat="ACH-0025",src=H,notes="R1 tool refill (no credits).")
add("Share Food with the Party","z06","Split a meal with the party",
 "You split a sandwich. With feelings. Gross. Wholesome. Gross.",TC,credits=25,title_aw="Meal Buddy",
 reward_line=tc("Meal Buddy","Do not mention the sandwich."),cat="ACH-0899",src=H,notes="R1.")
add("Rumor Mill","z06","Read the Break Room corkboard three times",
 "You read a corkboard. Three times. Somebody get this crawler a library card.",TC,credits=25,title_aw="Rumor Mill",
 reward_line=tc("Rumor Mill","Gossip is a skill."),cat="ACH-0188",src=H,notes="R1.")
add("Lunch Thief","z06","Eat Dale's labeled sandwich in front of Dale",
 "Dale saw. Dale will always have seen.","snark",reward_line="Reward: Indigestion. Dale's.",cat="NEW",src=H,notes="R0.")
add("First Box","z06","Open the Welcome Box",
 "Your pupils went full slot machine. It's going in the promo.","snark",reward_line="Reward: The box. You're welcome.",cat="NEW",src=H,notes="R0. Welcome Box is the one fixed box name on the floor (floor doc §8.1).")
add("Stair Bait Resisted","z07","Walk away from the EXIT without going down",
 "You smelled freedom and said 'nah.' The birds are devastated.","box","Bronze","Didn't Fall for the Birdsong Box",
 cat="ACH-0084",src=CI,ledger=["L-001"],notes="Floor doc §10.1 Bronze box; the floor's best smart-play reward.")
add("Freedom Smelled Like a Fan","z07","Go down the Big Green EXIT",
 "You heard birds and ran at them like a horny golden retriever. The pit has your name on it now. We engraved it.","snark",reward_line="Reward: A pit with your name. Also, a bruise.",cat="NEW",src=H,notes="R0. Alternate Bronze if the fight goes well: Bronze You Opened the Door Marked 'Do Not' Box (core §4.8 #3).")
add("First Down","z08","First time you hit 0 HP",
 "You hit the floor. The floor hit back. Floor: 1. You: also on the floor.","snark",reward_line="Reward: A tutorial popup, and zero dignity.",cat="ACH-0085",src=H,notes="R0.")
add("Close Call","z08","Survive at exactly 1 HP",
 "One hit point. One. We could have framed it, but you asked to keep it.",TC,credits=25,title_aw="Close Call",
 reward_line=tc("Close Call","Go buy a potion."),cat="ACH-0016",src=H,ledger=["L-011"],notes="R1. Canon cousin: Survivor's Box (L-011).")
add("Sacrifice Play","any","Take a hit meant for someone else",
 "You took the hit for someone else. Heroic. Stupid. The good kind of stupid.","box","Bronze","Took One for the Team Box",
 cat="ACH-0020",src=CI,ledger=["L-001"],notes="Floor doc §10.1 Bronze box.")
add("Tutorial Elite","z08","Defeat Bruiser the Mascot (Unoccupied)",
 "You beat up an empty costume. Nobody was inside. Think about that. Then don't.",TC,credits=25,title_aw="Mascot Hunter",
 reward_line=tc("Mascot Hunter","The costume's bleeding stuffing."),cat="ACH-0078",src=H,notes="R1.")
add("Static in the Ear","z08","First death save on Floor 1 (Benefactor Signal)",
 "Signal logged.","hidden",hidden=True,reward_line="Reward: (none)",cat="ACH-0082",src=H,notes="HIDDEN, no reward. Spine plant SEED-BENEFACTOR. If asked: 'No such broadcast exists.'")
add("Level-Up, Baby!","z09","Reach level 2 at the Green Room",
 "Level two. The audience noticed you are slightly less bad.","snark",
 reward_line="Reward: More hit points. And your own self-respect, we hear it's back in stock.",cat="NEW",src=CA,ledger=["A-070"],notes="Canon achievement A-070 (reaching level 2, reward None, VERIFIED B1 ch5); wording here is original, reward is snark-only like canon.")
add("Stair Seeker","zS","Find the service stairwell before beating the boss",
 "You found the back stairs before the boss. Smart. Cowardly. Smart.","box","Bronze","Went Around the Bouncer Box",
 cat="ACH-0180",src=CI,ledger=["L-001"],notes="Floor doc §10.1 Bronze box.")
add("Dodge a Telegraphed AoE","z10","Avoid a telegraphed area attack from Dean Thudd",
 "He counted to three. You can count to three. Congratulations on counting to three.",TC,credits=25,title_aw="Counted to Three",
 reward_line=tc("Counted to Three","Count higher next time."),cat="ACH-0868",src=H,notes="R1.")
add("Boss Babe","z10","Deal damage to Dean Thudd",
 "You hit the dean. The dean noticed. The dean has a club.","snark",
 reward_line="Reward: Nothing. Punching a boss is its own reward, apparently.",cat="NEW",src=CA,ledger=["A-011"],notes="Canon achievement A-011 (dealing damage to a boss, reward None, VERIFIED B1 ch11); wording original.")
add("Peaceful Path","z10","Talk Dean Thudd into early retirement",
 "You talked the Dean into retirement. HR is furious. We are HR.","box","Bronze","Talked the Final Exam Into Early Retirement Box",
 cat="ACH-0189",src=CI,ledger=["L-001"],notes="Floor doc §10.1 Bronze box (in addition to Silver Boss Box? fold per ACH-0170 notes).")
add("Environmentalist","z10","Kill Dean Thudd using the orchestra pit",
 "You killed him with an orchestra pit. The orchestra has filed a complaint.","box","Bronze","Pit Stop Box",
 cat="ACH-0173",src=CI,ledger=["L-001"],notes="Floor doc §10.1 Bronze box.")
add("Boss Claim","z10","Defeat or talk down Dean Thudd",
 "The Dean is down. The dean is unavailable for comment. The dean is on the floor.","box","Silver","Pushed the Dean Into the Orchestra Pit and Called It Extra Credit Box",
 cat="ACH-0170",src=CI,ledger=["L-005","L-001"],notes="FOLDED into the Silver Boss Box (floor doc §6.7). Boss Box capped to Silver by F1 ceiling (core §4.7). Counts as the crawler's single 0-1 Silver. Alt names in floor doc §6.7: Accepted a Diploma..., Talked the Final Exam..., Dodged the Group Photo....")
add("Most Dangerous Hug","z10","Accept Dean Thudd's diploma mid-fight",
 "You let an ogre hug you for ratings. Your spine and the audience both screamed.","inspiration",
 reward_line="Reward: Crowd Pop and a rib check. Both are free.",cat="NEW",src=H,inspiration=True,notes="R2 (Crowd Pop) per floor doc §10.2. Heroic Inspiration max 1 per session.")
add("Destroy a Camera or Drone","z10","Destroy a camera or the drone",
 "You broke a camera. We have eleven thousand more. That one was Kevin's favorite, though.","snark",reward_line="Reward: A very small fine, billed to Kevin.",cat="ACH-0873",src=H,notes="R0.")
add("Skipped Finals","zS","Bypass Dean Thudd via the service stairs",
 "You went around the final exam, through the janitor's door, like a raccoon. Four million viewers just watched.","snark",
 reward_line="Reward: A raccoon sticker. No Boss Box. No Boss Claim.",cat="NEW",src=H,notes="R0. Bypass loses the Boss Box (floor doc §7.2); Stair Seeker can still pay.")
add("Tutorial Complete","z11","Descend the Floor 1 stairwell",
 "You graduated. Your diploma is in the mail. The mail is on fire.","title",title_aw="Oriented",
 reward_line='Reward: Title "Oriented". It is not a compliment.',cat="ACH-0022",src=H,notes="R1 Title only (ACH-0076 retired duplicate). Fires once.")
add("Strategic Advance in the Other Direction","any","Flee a fight without taking damage",
 "REWARD! ... lol no. Bitches don't get rewards.","snark",reward_line="Reward: ...lol no.",cat="NEW",src=CI,ledger=["A-007"],notes="R0. Canon snark-only pattern; line adapted from floor doc §10.2.")
add("Toe Talent","any","Fight barefoot, kick something to death, or otherwise make it about feet",
 "Our foot demographic would like to thank you personally. Please don't let them.","snark",reward_line="Reward: Attention. Of a kind.",cat="NEW",src=CI,ledger=["M-210"],notes="R0 (R1 if the audience demands it). Foot bit: at most once per session (floor doc §3.2). Respect opt-outs.")
add("Again? Production Has Seen This Episode","any","Repeat a farmed stunt (e.g. vending after the cap)",
 "Reruns don't pay. Ask any actor.","snark",reward_line="Reward: A rerun.",cat="NEW",src=H,notes="R0.")
add("Bleed Tax","any","Use a third healing item on the tutorial floor",
 "Three healing items on the tutorial floor. You're not a crawler, you're a sponge with a debit card.","snark",reward_line="Reward: A receipt.",cat="ACH-0197",src=H,notes="R0.")
add("Deal Psychic Damage","any","Deal psychic damage",
 "You hurt its feelings. Literally. We're so proud. Of the feelings.","snark",reward_line="Reward: An apology to the feelings.",cat="ACH-0866",src=H,notes="R0.")
add("Trailblazing Vending Gore","z03","First crawler in the campaign to smash a Snakk-Matic machine open",
 "You are the first crawler to murder a snack machine this season. Management is thrilled.","box","Silver","Snakk-Matic Box",
 cat="NEW",src=CI,ledger=["A-024","A-114","A-165"],trail=True,
 notes="Trailblazing pattern (audit R8; canon Crazy Cat Lady -> Trailblazing Crazy Cat Lady A-024/A-114, WIKI-ONLY for A-114): same theme, one tier up, Silver max on F1. DESIGN ONLY: in the alpha Bone was first and was paid only base Vending Gore; do not backfill. Counts as the crawler's 0-1 Silver, so do not also pay a Boss Box Silver unless the table agrees.")

# ================= Added 2026-10-07 (Lore, s1 review): toasts used at the table, from the floor docs =================
add("Paperwork Survivor","z00","Complete intake",
 "You completed intake without dying, crying, or reading the Terms of Service. Two out of three ain't bad.","snark",
 reward_line="Reward: ...No. It's paperwork. Nobody gets a prize for paperwork.",cat="NEW",src=H,status="toast text from character creation guide §9; floor doc §10.2 NEW R0",
 notes="R0 snark-only, pays nothing. Intake toast (create flow step 7); fires once per Crawler at intake. Given to all three s1 Crawlers.")
add("Win Initiative","z02","Win initiative on the floor's first roll",
 "You went first. Enjoy it. It is the last time anything down here waits for you.","snark",
 reward_line="Reward: None. Bragging rights only.",cat="ACH-0860",src=H,status="trigger from floor doc day-01 Z2 hooks; description proposed; reward line as played in s1",
 notes="Catalog R1 downgraded to R0 on F1 (floor doc §5.2 seeds: too routine to pay). Catalog name 'Orientation Pit: Win initiative'. s1: Mr. White, Vent Row.")
add("Rescued by Paperwork","any","Floor 1 Reprieve used: ejected to the nearest saferoom at 1 HP",
 "You were, for legal reasons, not dead. Please do not take this as a precedent.","title",title_aw="Rescued by Paperwork",
 reward_line='Reward: Title "Rescued by Paperwork". No credits. No precedent.',cat="NEW",src=H,status="Title and toast from floor doc §1.3 (Reprieve)",
 notes="Title only, no credits (same as Mostly Dead Intern / Participation Corpse). Third suggested Reprieve Title in floor doc §1.3; pick one Reprieve Title per Reprieve. s1: Mr. White, 2026-10-07.")

# canon pacing check: how many Bronze box achievements per crawler
deck = {"schema": "achievement-deck/0.1", "deck_id": "ach-f01-orientation-pit", "version": "0.1.1", "floor": 1,
 "zone": "any", "floor_name": "The Orientation Pit", "owner": "DCC Lore", "updated": "2026-10-07",
 "banner_format": "[SYSTEM] New achievement! <title>.  /  <description>  /  <reward_line>",
 "reward_kinds": {"box": "named Bronze/Silver box (box_name has no tier prefix)", "title_credits": "Title + 25 credits (R1, x1 on F1)",
   "title": "Title only", "snark": "snark-only reward (R0, canon pattern A-007/A-025)", "item": "specific item or mixed reward",
   "inspiration": "Heroic Inspiration (R2), max 1 per session", "hidden": "spine plant toast, no reward, never explained"},
 "pacing": {"core_4_5_floors_1_2": "2-4 Bronze and 0-1 Silver per crawler per floor, Welcome Box included; Benefactor extra",
   "floor_doc_8_2": "Floor doc caps achievement boxes at 2 per crawler (plus Welcome Box). Core 4.5 is the winning rule (spec v0.1.1 2.6); box overage is logged in the box ledger with the deed.",
   "alpha_note": "Bone Wifebeater logged 5 achievement Bronze boxes in the alpha (You Better Fucking Listen, Penalty Kick, Warranty Void If Removed, Tow Package, Tick Sandwich); Horn logged 1 (Grease Tube Disposal).",
   "no_desperado_box": "Desperado Pass Tattoo comes in a first Asshole's Box (L-019); there is no Desperado Box."},
 "achievements": L}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(deck, f, indent=2, ensure_ascii=False); f.write("\n")
print(OUT, len(L))
