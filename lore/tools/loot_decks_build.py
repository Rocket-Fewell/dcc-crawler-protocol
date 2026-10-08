#!/usr/bin/env python3
"""Builds the Floor 1 loot-box decks (schema loot-deck/0.1.1) into tables/loot-decks/.
Run from anywhere: python3 tools/loot_decks_build.py   Then: python3 tools/deck_check.py
Rules: dcc-campaign/rules/40-loot-deck-spec-5e.md v0.1.1. Mechanics checked 2026-10-04 against SRD 5.2.1
(ilmatar.net/~wiki/srd52, fantasygrounds SRD 5.2.1 mirror) and DMG 2024 text (aidedd.org 5.5 mirror); mirrors, not the books."""
import re
import json, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tables", "loot-decks")
SRDCHK = "Mechanics checked vs SRD 5.2.1 text (web mirror) 2026-10-04."
DMGCHK = "Mechanics checked vs DMG 2024 text (aidedd 5.5 mirror) 2026-10-04."
DR = "HOUSE DRAFT (status draft; Syndicate owns final mechanics text, Accountant checks value). "
SP = "Mechanics and value taken verbatim from Syndicate's rules/40-loot-deck-spec-5e.md section 3.1 row and rules/loot-deck-srd-check-f01.md (v0.1.2). "

def _act(a):
    if a.startswith("Attack action"): return "Action"
    if a.startswith("Bonus Action"): return "Bonus Action"
    if a.startswith("Utilize action"): return "Utilize action"
    if a.startswith("None (light)"): return "Magic action"
    return a
def M(text, action, rng=None, dmg=None, save=None, dur=None, uses=None, limits="", wt=0):
    return {"text": text, "action_cost": _act(action), "range": rng, "damage": dmg, "save_dc": save,
            "duration": dur, "uses": uses, "limits": limits, "weight_lb": wt}

class Deck:
    def __init__(self, zone, slug, zone_name, version="0.1.0", updated="2026-10-04"):
        self.zone, self.slug, self.zone_name, self.version, self.updated = zone, slug, zone_name, version, updated
        self.cards, self.n = [], 0
    def add(self, tier, pull, kind, reskin, real, src, rarity, cat, mech, spoken, snark, status, value, weight,
            box, deed, notes, attune=None, tags=None, unique=False, excl=None, grant=None, boxtypes=None, num=None, ledger_ids="", story=None, bound=None, ledger_text=None, sale=None):
        self.n = num if num else self.n + 1
        cid = "f01-%s-%04d" % (self.zone, self.n)
        ltype = {"credits": "credits", "key": "key", "pet": "pet", "clue": "clue"}.get(kind, "item")
        ltxt = ("credits +(%s) %s box" % (grant["roll"], tier)) if kind == "credits" else "item +1 %s box: %s%s" % (tier, reskin, "" if reskin == real else " (%s)" % real)
        if ledger_ids:
            notes = "LEDGER: %s. %s" % (ledger_ids, notes)
        self.cards.append({
            "id": cid, "floor": 1, "zone": self.zone, "tier": tier, "box_types": boxtypes or ["any"],
            "pull_type": ("weird" if pull == "key" else pull), "kind": kind, "reskin_name": reskin, "real_5e_name": real, "source_5e": src,
            "rarity": rarity, "attunement": attune, "category": cat, "plain_mechanics": mech,
            "spoken_line": spoken, "snark_line": snark, "reward": spoken, "canon_status": status,
            "credit_value": value, "draw_weight": weight, "unique": unique, "tailor_tags": tags or [],
            "exclusive_to": excl, "grant": grant,
            "ledger": {"type": ltype, "text": ledger_text or ltxt}, "box_name": box, "deed": deed, "notes": notes})
        if story is not None:
            self.cards[-1]["story_value"] = story
            self.cards[-1]["bound"] = bool(bound)
            if sale is not None: self.cards[-1]["sale_value"] = sale
    def dump(self, extra=None):
        sch = "loot-deck/0.1.2" if any("story_value" in c for c in self.cards) else "loot-deck/0.1.1"
        d = {"schema": sch, "deck_id": "f01-%s-%s" % (self.zone, self.slug), "version": self.version,
             "floor": 1, "zone": self.zone, "zone_name": self.zone_name, "owner": "DCC Lore", "updated": self.updated,
             "cards": self.cards}
        if extra: d.update(extra)
        p = os.path.join(OUT, "f01-%s-%s.json" % (self.zone, self.slug))
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False); f.write("\n")
        return p

CA, CI, H = "CANON", "CANON-INSPIRED", "HOUSE"
U1 = {"max": 1, "recharge": "none"}
def credits_grant(roll): return {"credits": None, "roll": roll}

# ------------------------------------------------------------------ ANY (floor-wide) deck
A = Deck("any", "orientation-pit", "Floor 1: The Orientation Pit (floor-wide pool)", version="0.1.1")

# ---- Bronze consumables
A.add("Bronze","consumable","consumable","Sports Drink, Mystery Flavor","Potion of Healing","SRD 5.2","Common","Consumables",
 M("Bonus Action: drink it, or give it to a creature within 5 ft; the drinker regains 2d4+2 HP. One use.","Bonus Action","5 ft (to give)",None,None,"instant",U1,"Consumed on use.",0.5),
 "Sports Drink, Mystery Flavor, Potion of Healing. Bonus Action: regain two d four plus two hit points.",
 "Tastes like a lawsuit and heals like a fairly priced one.",CA,50,30,"Bled on the Carpet Box","Took damage and kept going",
 SRDCHK+" Alpha used Red/Blue/Green flavors as placed potions; this is the box-draw version.",ledger_ids="I-009 (healing potion, B1), L-B02; flavor only, mechanics are 5e")
A.add("Bronze","consumable","consumable","Rope-Swing Energy Drink","Potion of Climbing","SRD 5.2","Common","Consumables",
 M("Bonus Action: drink; for 1 hour you gain a Climb Speed equal to your Speed and have Advantage on Strength (Athletics) checks to climb. One use.","Bonus Action",None,None,None,"1 hour",U1,"Consumed on use.",0.5),
 "Rope-Swing Energy Drink, Potion of Climbing. One hour: climb speed equals your speed, advantage on climbing checks.",
 "Side effects include confidence and a sudden interest in ceilings.",CI,60,18,"Climbed Something You Weren't Supposed To Box","Climbed a wall, rail or ceiling",SRDCHK)
A.add("Bronze","consumable","consumable","Cease-and-Desist Letter (Addressed To Your Enemies)","Spell Scroll (Magic Missile, level 1)","SRD 5.2","Common","Consumables",
 M("Magic action: if Magic Missile is on your class's spell list (Sorcerer, Wizard), read the scroll to cast it at level 1: three darts, each 1d4+1 Force, auto-hit, up to 120 ft. The scroll then disintegrates.","Magic action","120 ft","1d4+1 Force per dart (3 darts)",None,"instant",U1,"Only a class with Magic Missile on its list can read it. No Material components needed.",0),
 "Cease-and-Desist Letter, Spell Scroll of Magic Missile. Wizards and Sorcerers only: three darts, one d four plus one force each.",
 "Legally binding, magically binding, and neither is ever enforced.",CI,75,12,"Read the Fine Print Out Loud Box","Read something out loud that you shouldn't have",SRDCHK+" Scroll DC 13 / +5 irrelevant (Magic Missile needs no roll).",tags=["magic missile","wizard"])
A.add("Bronze","consumable","consumable","Get-Well-Soon Card (Singing, Unsolicited)","Spell Scroll (Cure Wounds, level 1)","SRD 5.2","Common","Consumables",
 M("Magic action: if Cure Wounds is on your class's spell list (Bard, Cleric, Druid, Paladin, Ranger), read the scroll to cast it at level 1: touch a creature, it regains 2d8 + your spellcasting ability modifier HP. The scroll then disintegrates.","Magic action","Touch","2d8 + spellcasting modifier HP restored",None,"instant",U1,"Only classes with Cure Wounds on their list can read it.",0),
 "Get-Well-Soon Card, Spell Scroll of Cure Wounds. Healers, Bards, Druids, Paladins, Rangers: touch heals two d eight plus your modifier.",
 "It plays a tinny song while you bleed. That part is not a setting.",CI,75,8,"Patched Up a Friend Box","Healed or stabilized a teammate",SRDCHK+" Only half the table can use it; low weight on purpose.")
A.add("Bronze","consumable","consumable","Birthday Candle (Lit, Somehow)","Spell Scroll (Fire Bolt, cantrip)","SRD 5.2","Common","Consumables",
 M("Magic action: if Fire Bolt is on your class's spell list (Sorcerer, Wizard), read the scroll to cast it: ranged spell attack (+5), up to 120 ft, 1d10 Fire. A flammable object not worn or carried ignites. The scroll then disintegrates.","Magic action","120 ft","1d10 Fire","Ranged spell attack +5 (scroll)","instant",U1,"Only a class with Fire Bolt on its list can read it.",0),
 "Birthday Candle, Spell Scroll of Fire Bolt. Wizards and Sorcerers only: ranged attack, one d ten fire, one hundred twenty feet.",
 "Make a wish. The wish is arson.",CI,50,10,"Set Something on Fire on Purpose Box","Used fire on purpose",SRDCHK+" Fire Bolt ignition rider per spell text; verify wording when announced.",tags=["fire","wizard"])
A.add("Bronze","consumable","consumable","Battery-Acid Slushie","Acid","PHB 2024","Mundane","Consumables",
 M("Attack action (replace one attack): throw at a creature or object you can see within 20 ft. It makes a Dex save (DC 8 + thrower's Dex modifier + proficiency bonus) or takes 2d6 Acid damage. One use.","Attack action (replaces one attack)","20 ft","2d6 Acid","Dex DC 8 + Dex mod + prof","instant",U1,"Consumed on throw.",1),
 "Battery-Acid Slushie, Acid. Throw twenty feet; failed dex save means two d six acid damage.",
 "Brain freeze is the least of their problems.",CI,25,16,"Threw Something Gross at Something Worse Box","Threw a dangerous liquid at an enemy",SRDCHK+" Spec §3 listed this as a ranged attack with no save; 2024 uses a Dex save.",tags=["explosives","acid"])
A.add("Bronze","consumable","consumable","Communion Cup, Chilled","Holy Water","PHB 2024","Mundane","Consumables",
 M("Attack action (replace one attack): throw at a creature you can see within 20 ft. A Fiend or Undead must make a Dex save (DC 8 + thrower's Dex modifier + proficiency bonus) or take 2d8 Radiant damage. No effect on other creature types. One use.","Attack action (replaces one attack)","20 ft","2d8 Radiant (Fiends and Undead only)","Dex DC 8 + Dex mod + prof","instant",U1,"Does nothing to creatures that are not Fiends or Undead. Skeleton-type Mannequin Staff on Floor 1 count as Undead.",1),
 "Communion Cup, Holy Water. Throw twenty feet at a fiend or undead: failed dex save means two d eight radiant.",
 "Blessed by someone who has seen things. Mostly the bottom of cups.",CI,25,14,"Splashed the Dead for Fun Box","Damaged an undead creature",SRDCHK)
A.add("Bronze","consumable","consumable","Gas-Station Pepto, Chewable","Antitoxin","PHB 2024","Mundane","Consumables",
 M("Bonus Action: drink; for 1 hour you have Advantage on saving throws to avoid or end the Poisoned condition. One use.","Bonus Action",None,None,None,"1 hour",U1,"Consumed on use. Does not cure the condition by itself.",0),
 "Gas-Station Pepto, Antitoxin. Bonus Action: one hour of advantage on saves against poison.",
 "Do not read the ingredients. They are in a language called regret.",CI,50,14,"Licked the Wrong Needle Box","Got poisoned and walked it off",SRDCHK+" Spec said Drink with no action type; 2024 text is Bonus Action.")
A.add("Bronze","consumable","consumable","Cooking Spray, Industrial Drum Size","Oil (flask)","PHB 2024","Mundane","Consumables",
 M("Attack action (replace one attack): throw at a creature or object within 20 ft; Dex save (DC 8 + Dex mod + proficiency bonus) or it is covered in oil for 1 minute; if it takes Fire damage in that time, +5 Fire damage. OR Utilize action: pour on level ground in a 5-ft square within 5 ft; if lit it burns until the end of the turn 2 rounds later, 5 Fire damage to any creature entering or ending its turn there (once per turn). Also fuels a Lamp or Lantern for 6 hours.","Attack action or Utilize action","20 ft (thrown) / 5 ft (poured)","5 Fire (burning oil)","Dex DC 8 + Dex mod + prof","1 minute (coating) / 2 rounds (burning pool)",U1,"Consumed. Fire damage is only added if something ignites it.",1),
 "Cooking Spray, Oil flask. Coat a target or pour a five foot pool; fire adds five damage.",
 "Fry something, anything, preferably the bad thing.",CI,0.1,16,"Fried Something Unwise Box","Combined grease and fire",SRDCHK+" Floor doc names oil as junk weapon oil (First Blood reward). Tagged fire.",tags=["fire","cooking"])
A.add("Bronze","consumable","consumable","Bag of Lost Marbles (Not Yours)","Ball Bearings","PHB 2024","Mundane","Consumables",
 M("Utilize action: spill the pouch over a level 10-ft square within 10 ft. A creature entering the area for the first time on a turn makes a DC 10 Dex save or falls Prone. Takes 10 minutes to pick up again.","Utilize action","10 ft (centre within)",None,"Dex DC 10","until picked up (10 min)",None,"Reusable once recovered (10 minutes).",2),
 "Bag of Lost Marbles, Ball Bearings. Spill a ten foot square; first entry each turn, dex save ten or prone.",
 "Your opponents lose their marbles. You are the one who found them.",CI,1,14,"Made the Floor Dangerous Box","Used terrain against enemies",SRDCHK+" Spec VERIFY about movement exception: 2024 text is 'first time on a turn', no half-speed exception.")
A.add("Bronze","consumable","consumable","Bag of LEGO, Barefoot Edition","Caltrops","PHB 2024","Mundane","Consumables",
 M("Utilize action: spread over a 5-ft square within 5 ft. A creature entering for the first time on a turn makes a DC 15 Dex save or takes 1 Piercing damage and its Speed drops to 0 until the start of its next turn. Takes 10 minutes to recover.","Utilize action","5 ft (centre within)","1 Piercing","Dex DC 15","until picked up (10 min)",None,"Reusable once recovered (10 minutes).",2),
 "Bag of LEGO, Caltrops. Spread a five foot square; failed dex save fifteen means one damage and speed zero.",
 "Every parent knows this weapon. No parent has ever beaten it.",CI,1,14,"Left a Mess on Purpose Box","Set a trap with junk",SRDCHK+" Spec said 'Speed -10 until it regains 1 HP'; 2024 text differs (Speed 0 until start of next turn).",tags=["traps"])
A.add("Bronze","consumable","consumable","Break-Room First-Aid Kit, Lightly Bitten","Healer's Kit","PHB 2024","Mundane","Consumables",
 M("Utilize action: expend 1 of 10 uses to stabilize an Unconscious creature at 0 HP without a Wisdom (Medicine) check.","Utilize action","Touch",None,None,"instant",{"max":10,"recharge":"none"},"Stabilizes only; does not restore HP. 10 uses total.",3),
 "Break-Room First-Aid Kit, Healer's Kit. Ten uses: Utilize to stabilize a creature at zero hit points, no check.",
 "Stabilize them. Do not ask what bit the kit.",CI,5,12,"Dragged Someone Out of the Fire Box","Stabilized a dying teammate",SRDCHK+" Alpha: Bone stabilized Horn with a similar kit (Buddy System).")
A.add("Bronze","consumable","consumable","Tiki Torch, Unlicensed","Torch","PHB 2024","Mundane","Consumables",
 M("Burns for 1 hour: bright light 20 ft, dim light another 20 ft. Attack action: use as a Simple melee weapon; on a hit, 1 Fire damage.","Attack action (as weapon)","20 ft light","1 Fire","None","1 hour",{"max":1,"recharge":"none"},"Needs a flame source (Tinderbox is a Bonus Action).",1),
 "Tiki Torch, Torch. One hour of light, twenty feet bright. As a weapon: one fire damage.",
 "Mood lighting for a crime scene.",CI,0.01,10,"Lit the Way Badly Box","Carried a light into the dark",SRDCHK)

# ---- Bronze gear
A.add("Bronze","gear","item","Paint-Can Pry Bar","Crowbar","PHB 2024","Mundane","Misc",
 M("Passive: Advantage on Strength checks where the crowbar's leverage can be applied.","None (passive)",None,None,None,"while held",None,"Not a weapon stat (improvised weapon).",5),
 "Paint-Can Pry Bar, Crowbar. Advantage on strength checks where leverage helps.",
 "Solves every problem that has a lid.",CI,2,14,"Opened the Door Marked Do Not Box","Forced something open",SRDCHK,tags=["tools"])
A.add("Bronze","gear","item","Big Honking Flashlight","Lantern, Hooded","PHB 2024","Mundane","Misc",
 M("Burns Oil: bright light 30 ft, dim light another 30 ft; one oil flask lasts 6 hours. Bonus Action: lower the hood (dim light 5 ft radius only) or raise it again.","Bonus Action (hood)","30 ft bright + 30 ft dim","None","None","6 hours per Oil flask",None,"Needs a flask of Oil and a flame to light.",2),
 "Big Honking Flashlight, Hooded Lantern. Thirty feet bright, thirty dim; Bonus Action to lower the hood.",
 "It lights your path and everyone else's attention.",CI,5,12,"Saw Something in the Dark Box","Explored a dark area",SRDCHK+" Spec VERIFY radius resolved: 30/30 plus hood.")
A.add("Bronze","gear","item","Hardware-Store Harness (Pitons Included, Regrettably)","Climber's Kit","PHB 2024","Mundane","Misc",
 M("Utilize action: anchor yourself; you can't fall more than 25 ft from the anchor point and can't move more than 25 ft from it without undoing the anchor as a Bonus Action.","Utilize action","25 ft from anchor",None,None,"until undone",None,"Needs a place to set the anchor.",12),
 "Hardware-Store Harness, Climber's Kit. Utilize to anchor: no falling more than twenty-five feet from the anchor.",
 "Safety first. Second and third are also yours.",CI,25,10,"Went the Wrong Way Up Box","Climbed or dropped somewhere risky",SRDCHK+" Spec VERIFY resolved with 25 ft numbers.")
A.add("Bronze","gear","item","Volleyball Net, Reclaimed","Net","PHB 2024","Mundane","Misc",
 M("Attack action (replace one attack): throw at a creature you can see within 15 ft; Dex save (DC 8 + Dex mod + proficiency bonus) or it is Restrained until it escapes. Huge or larger succeed automatically. Escape: the target or a creature within 5 ft uses an action for a DC 10 Strength (Athletics) check, or the net is destroyed (AC 10, 5 HP, immune to Bludgeoning, Poison, Psychic).","Attack action (replaces one attack)","15 ft",None,"Dex DC 8 + Dex mod + prof","until escape",None,"Huge or larger creatures auto-succeed on the save.",3),
 "Volleyball Net, Net. Throw fifteen feet; failed dex save means restrained until freed.",
 "Nothing but net, and nothing but regret.",CI,1,12,"Caught Something in a Net Box","Restrained an enemy",SRDCHK+" Spec VERIFY range resolved: 15 ft, Dex save, Huge+ immune.")
A.add("Bronze","gear","item","Raccoon Trap, Industrial","Hunting Trap","PHB 2024","Mundane","Misc",
 M("Utilize action: set it. A creature stepping on the plate makes a DC 13 Dex save or takes 1d4 Piercing damage and its Speed drops to 0 until the start of its next turn; thereafter movement is limited by the chain (about 3 ft) until it breaks free. Freeing: a creature uses its action for a DC 13 Strength (Athletics) check. Each failed check deals 1 Piercing.","Utilize action (set)","Touch (set); trap triggers underfoot","1d4 Piercing (+1 per failed escape)","Dex DC 13","until freed",None,"Must be chained to an immobile object.",25),
 "Raccoon Trap, Hunting Trap. Set it down: failed dex save thirteen means one d four piercing and no movement.",
 "Guaranteed to catch something. Statistically, you.",CI,5,10,"Forgot Where You Put the Trap Box","Set or sprang a trap",SRDCHK+" Spec VERIFY free-DC resolved: DC 13 Strength (Athletics).",tags=["traps"])
A.add("Bronze","gear","item","Padlock for a Locker Nobody Owns","Lock","PHB 2024","Mundane","Misc",
 M("Comes with a key. Without the key, Thieves' Tools pick it with a successful DC 15 Dexterity (Sleight of Hand) check.","none",None,None,"Dex (Sleight of Hand) DC 15 to pick","permanent",None,"Needs Thieves' Tools to pick.",1),
 "Padlock for a Locker Nobody Owns, Lock. Comes with a key; picking it takes thieves' tools and a dex check fifteen.",
 "Somebody lost the key and everybody regrets it.",CI,10,8,"Locked Something Up Box","Secured or picked a lock",SRDCHK)
A.add("Bronze","gear","item","Extension Cord, Fifty Feet, Unplugged","Rope (hempen, 50 ft)","PHB 2024","Mundane","Misc",
 M("Utilize action: tie a knot (DC 10 Dex (Sleight of Hand)). Bursts on a DC 20 Strength (Athletics) check. Binds an unwilling creature only if it is Grappled, Incapacitated or Restrained; escape: DC 15 Dex (Acrobatics) as an action.","Utilize action","50 ft length",None,"Burst Str DC 20; escape Dex DC 15","permanent",None,"2024 numbers: burst DC 20 (starter kit card-data says DC 17, 2014).",5),
 "Extension Cord, Rope. Fifty feet; knots with a dex check ten, bursts at strength twenty.",
 "Someone will tie a booth to something. We just know.",CI,1,12,"Tied It to Something Terrible Box","Used rope to haul, tow or climb",SRDCHK+" Weight 5 lb per 2024 equipment table (spec VERIFY resolved). Alpha: Bone towed a booth with rope (Tow Package).")
A.add("Bronze","gear","item","Staff-Lounge Hand Bell","Bell","PHB 2024","Mundane","Misc",
 M("Utilize action: ring it; the sound can be heard up to 60 ft away.","Utilize action","60 ft",None,None,"instant",None,"No other effect.",0),
 "Staff-Lounge Hand Bell, Bell. Utilize: heard sixty feet away.",
 "Cue the proctor. Cue the regret.",CI,1,6,"Rang It Anyway Box","Made noise on purpose",SRDCHK,tags=["pranks"])
A.add("Bronze","gear","item","Mascot Head, Sweaty (Not That One)","Costume","PHB 2024","Mundane","Armor",
 M("While worn, Advantage on any ability check to impersonate the type of person the costume represents. 4 lb.","None (passive)",None,None,None,"while worn",None,"No AC. Floor 1 mascots are not impressed.",4),
 "Mascot Head, Costume. Advantage on checks to impersonate what it represents.",
 "Smells like a warm yes.",CI,5,10,"Dressed for the Wrong Occasion Box","Wore or fought in a costume",SRDCHK,tags=["hats","costumes"])
A.add("Bronze","tailored","item","Dean's List Magnifying Glass","Magnifying Glass","PHB 2024","Mundane","Misc",
 M("Advantage on any ability check made to appraise or inspect a highly detailed item. Lighting a fire with it needs sunlight-bright light, tinder and about 5 minutes.","None (passive)",None,None,None,"while held",None,"Fire use needs sunlight-level light.",0),
 "Dean's List Magnifying Glass. Advantage on checks to inspect highly detailed items.",
 "Look closer. Nothing will improve.",CI,100,6,"Read the Tiny Print Box","Investigated something carefully",SRDCHK,tags=["reading","investigation"])
A.add("Bronze","tailored","item","Gas-Station Jerky Cubes (Mystery Meat, Sealed Since 2019)","Rations (1 day)","PHB 2024","Mundane","Consumables",
 M("Travel food for one day. 2 lb.","none",None,None,None,"1 day",{"max":1,"recharge":"none"},"Counts as a day's food; a dog will also eat it.",2),
 "Gas-Station Jerky Cubes, Rations. One day of travel food.",
 "Chewy, salty, and nobody asks what animal.",CI,0.5,12,"Shared a Snack Box","Shared food or fed an animal",SRDCHK+" Tailor tag: dogs (hidden tailoring only, no public tag).",tags=["dogs","food"])
A.add("Bronze","tailored","item","Hotel Desk Bell, Ding Ding","Signal Whistle","PHB 2024","Mundane","Misc",
 M("Utilize action: blow it; the sound can be heard up to 600 ft away.","Utilize action","600 ft",None,None,"instant",None,"No other effect.",0),
 "Hotel Desk Bell, Signal Whistle. Utilize: heard six hundred feet away.",
 "Calls the staff. The staff will not come.",CI,0.05,6,"Called for Help Loudly Box","Called out for help or attention",SRDCHK+" Tailored slot: dog-whistle gag for Horn is in exclusive card below.",tags=["noise"])
# exclusive gag (Horn) - dog hook is public from sheet
A.add("Bronze","tailored","item","Dog Whistle, Silent Except To Pebbles","Signal Whistle (house: gag skin)","PHB 2024","Mundane","Misc",
 M("Utilize action: blow it; the sound can be heard up to 600 ft away. No special effect on any creature.","Utilize action","600 ft",None,None,"instant",None,"No bonus on dogs; jokes are on the item, not the dog.",0),
 "Dog Whistle, Signal Whistle. Utilize: heard six hundred feet away.",
 "It works on dogs. This is the part about dogs we are not discussing.",CI,0.05,0,"Followed a Hunch Box","Looked for a missing friend",SRDCHK+" Horn running gag (public dog hook). Hand-pick only (weight 0) so the gag lands once.",tags=["dogs"],excl="Horn",unique=True)
# magic-ish Bronze: Driftglobe hand-pick, Cloak, Pole (alpha-issued)
A.add("Bronze","gear","item","Pebbles Snow Globe","Driftglobe","DMG 2024","Uncommon","Misc",
 M("Within 60 ft, a command word makes it shed light as the Light spell (20 ft bright + 20 ft dim) or the Daylight spell (60 ft bright + 60 ft dim); Daylight once, then not again until next dawn. A second command word (Magic action) floats it up to 5 ft in the air; if you move more than 60 ft away it follows you; if blocked it sinks and goes dark. 1 lb.","None (light); Magic action (float)","60 ft","None",None,"until commanded off / until next dawn (Daylight)",{"max":1,"recharge":"dawn"},"Daylight once per dawn only.",1),
 "Pebbles Snow Globe, Driftglobe. Command word for light or daylight; Magic action to float it.",
 "Hand-picked. Do not read into it.",CI,100,0,"Left Something Behind Box","Looked for a lost dog",DMGCHK+" UNCOMMON, hand-picked into a Bronze box (Horn, alpha). Audit O15: not Common; float command is Magic action (2024). Already issued to Horn; weight 0 so it cannot be redrawn.",
 tags=["dogs","light"],unique=True,excl="Horn")
A.add("Bronze","gear","item",'Eternally Stained Wifebeater',"Cloak of Many Fashions (house)","HOUSE","Common","Misc",
 M('Worn as your outer garment (no attunement). Bonus Action: change its style, color and apparent quality to any cloak, hoodie, cape or vest you have seen. Looks only: no AC, no powers, no bonus to any check. Weight does not change.',"Bonus Action",None,None,None,"until you change it",None,'Cosmetic only. Copies the look of other garments, never their properties or magic. You can wear only one outer-garment magic item at a time (house). It always stays a garment of about its own size. Touching it reveals nothing odd.',1),
 'Eternally Stained Wifebeater, Cloak of Many Fashions. Bonus Action: change its style and color. Looks only.',
 'It is stained. That part is not a setting.',CI,50,0,'Showed Up in That Shirt Box','Wore the same shirt through everything',
 'HOUSE design (rules/42-house-items-f01.md §2). Follows the general shape of the DMG cloak from memory; not copied, not checked against the book. Already issued to Bone Wifebeater (alpha). weight 0 / hand-pick, exclusive. Same text as f01-z09-0015: only id, zone, weight, unique, exclusive_to, reskin and box fields differ.',tags=["clothing"],unique=True,excl="Bone Wifebeater")
A.add("Bronze","gear","item","Collapsible Tent-Pole","Pole of Collapsing (house)","HOUSE","Common","Misc",
 M('Works as a 10 ft Pole. Magic action while holding it: collapse it to a 1 ft rod (weight unchanged) or extend it back to 10 ft; it stops growing where something blocks it. As a Pole you can touch something up to 10 ft away, and you have Advantage on a Strength (Athletics) check to vault in a High or Long Jump. Not a weapon: extending it pushes and damages nothing.',"Magic action",None,None,None,"until you change it",None,'No attack or damage use; one change per action. Collapsed it is a plain 1 ft rod. Extending into a creature or object stops it at that point.',7),
 "Collapsible Tent-Pole, Pole of Collapsing. Magic action: collapse to one foot or extend to ten.",
 "Easy to carry. Hard to explain.",CI,50,6,"Poked Something Gently Box","Prodded a trap or hazard from afar",
 "HOUSE design (rules/42-house-items-f01.md §3). DMG shape from memory, not copied. Action cost is Magic action (2024 term). The Pole part follows the SRD 5.2 Pole. Alpha item, kept low weight for redraw by other Crawlers.",tags=["tools"])

# ---- Bronze weird / junk / key / clue
A.add("Bronze","weird","junk","Kevin the Sentient Rubber Duck","Rubber Duck (house: joke item, no effect)","HOUSE","n/a","Misc",
 M("Joke item. No mechanical effect. Kevin gives terrible advice; the GM treats it as flavor only.","none",None,None,None,"permanent",None,"No effect on dice, DCs, damage or saves. Never gives a real hint.",0),
 "Kevin the Sentient Rubber Duck. Weird pull, joke item, no mechanical effect.",
 "Kevin is not licensed.",H,0,8,"Took Bad Advice Seriously Box","Followed terrible advice",
 "Alpha item. Weird pull. Kevin may speak up; never a hint. Weight 8.",tags=[])
A.add("Bronze","weird","junk","Raffle Ticket No. 0000","Raffle Ticket (house: joke item, no effect)","HOUSE","n/a","Misc",
 M("Joke item. No mechanical effect. The System never explains the raffle ticket.","none",None,None,None,"permanent",None,"Does nothing. Probably.",0),
 "Raffle Ticket Zero Zero Zero Zero. Joke item. No mechanical effect.",
 "Drawing is at some point. We will not say when.",H,0,6,"Won a Contest Nobody Entered Box","Cracked a register or searched a gallery",
 "Matches the Shooting Gallery register's raffle ticket in the floor doc §5.5. Keep it a joke; never pay out.")
A.add("Bronze","weird","junk","Apology Voucher, Valid Nowhere","Apology Box voucher (house: joke item, no effect)","HOUSE","n/a","Misc",
 M("Joke item. No mechanical effect. Compensates for System error in sentiment only.","none",None,None,None,"permanent",None,"No cash value. The System is not sorry.",0),
 "Apology Voucher, Valid Nowhere. Joke item. No mechanical effect.",
 "We are sorry you were disappointed. This is the apology.",CI,1,5,"Filed a Grievance Box","Complained loudly",
 "Dud by design (core §4.3: never two duds in a row). Apology Box idea in core §4.7.",ledger_ids="none (HOUSE joke variant, core §4.7); canon joke-contents rows L-B61/L-B09 are WIKI-ONLY")
A.add("Bronze","weird","clue","Maintenance Note, Greasy","Lore scrap (house: one-use hint)","HOUSE","n/a","Misc",
 M("Utilize action, once: read it; the GM gives you one true, useful sentence about the next zone (like one Proctor Bell hint). The note is then spent.","Utilize action",None,None,None,"instant",U1,"One hint per card. Does not stack with Proctor Bell's per-zone limit.",0),
 "Maintenance Note, Greasy. One use: the GM gives one true hint about the next zone.",
 "Written by a man named Dale. Dale means well.",H,10,10,"Read a Dead Man's Mail Box","Read someone else's notes",
 "Clue card. Do not duplicate Tanya's lore scroll (placed). Hint must be true.",tags=["reading"])
A.add("Bronze","weird","clue","Staff Map, Coffee-Stained","Map (house: marks one hidden spot)","PHB 2024","Mundane","Misc",
 M("While consulting this accurate Map of Floor 1, +5 bonus to Wisdom (Survival) checks to find your way in the place it shows. House: it marks one hidden room (GM-only note).","None (passive)",None,None,None,"while held",None,"Only helps on Floor 1.",0),
 "Staff Map, Coffee-Stained. Plus five to survival checks to find your way on this floor.",
 "The coffee stain is where the exit is not.",CI,25,6,"Followed a Map Into a Wall Box","Found a hidden room or path",SRDCHK+" House rider: GM marks Zone S (service corridor) or 3b.",tags=["maps"])
A.add("Bronze","key","key","Gas-Station Bathroom Key on a Hubcap","Mystery Key (house, single lock)","HOUSE","Common","Keys",
 M('Utilize action: opens one specific lock on this floor, picked by the GM when the key is drawn (the GM does not say which). On that lock it unlocks it and the key is spent. On any other lock nothing happens and it is not spent. If you leave the floor with it unused, it becomes a plain hubcap key.',"Utilize action",None,None,None,"until used or you leave the floor",U1,'One use, one lock. Cannot open a lock sealed by a boss, spine object or magic barrier. Never the only way through a required door.',1),
 'Gas-Station Bathroom Key on a Hubcap. House Mystery Key: opens one GM-chosen lock on this floor; spent on use.',
 "It opens something, and the System is not telling.",H,25,5,"Found the Right Key Eventually Box","Hunted for a way through a locked door",
 'HOUSE design (rules/42-house-items-f01.md §4). GM only: pick the lock now and write it into session state, not this deck. Optional rooms are best (Break Room supply cabinet, a locker bank, the 3b Lost & Found cage). Zone S door works but skips the boss and the Boss Box, so decide on purpose. The real 5e Mystery Key is a chance-based key; this is a different item. Same text for f01-z06-0004 (weight 6).')

# ---- Bronze credits
for i,(nm,box,deed,sn) in enumerate([
 ("Loose Change From Under the Couch Cushion","Looked Under the Cushion Box","Searched furniture","Found it. Do not ask where it was."),
 ("Employee-of-the-Month Bonus (Withheld, Then Un-Withheld)","Employee of the Month by Accident Box","Survived and impressed nobody","HR has reconsidered. Briefly."),
 ("Credits, Slightly Damp","Participation Trophy Box","Showed up, technically","Please spend it before it ferments.")],1):
    A.add("Bronze","credits","credits",nm,"Credits (Bronze pull, 3d6 x 5)","HOUSE","n/a","Credits",
     M("Adds 3d6 x 5 credits (15-90) to your balance when the box is opened. Roll at draw time with tools/roll.py. No weight.","none",None,None,None,"instant",None,"Added when the box is opened.",0),
     "%s. Bronze credits: three d six times five, added to your balance." % nm.split(" (")[0],
     sn,CI,52.5,10,box,deed,"Credit boxes are canon-shaped (tiered boxes, L-001); amount math is HOUSE core §4.2. credit_value = expected value (10.5 x 5). Roll at draw.",
     grant=credits_grant("3d6x5"),ledger_ids="L-001")

# ------------------------------------------------------------------ SILVER (any)
A.add("Silver","consumable","consumable","Sports Drink, Extra Strength Flavor","Potion of Healing (greater)","SRD 5.2","Uncommon","Consumables",
 M("Bonus Action: drink it, or give it to a creature within 5 ft; the drinker regains 4d4+4 HP. One use.","Bonus Action","5 ft (to give)",None,None,"instant",U1,"Consumed on use.",0.5),
 "Sports Drink, Extra Strength, Potion of Greater Healing. Bonus Action: regain four d four plus four hit points.",
 "Tastes like two lawsuits.",CA,150,24,"Almost Died Impressively Box","Survived a fight at very low HP",SRDCHK+" Price HOUSE (spec price VERIFY retained as HOUSE estimate).",ledger_ids="I-009 (healing potion, B1); L-B02; Survivor's Box L-011")
A.add("Silver","consumable","consumable","Hazmat Slushie, Color of the Day","Potion of Resistance","SRD 5.2","Uncommon","Consumables",
 M("Drink (Bonus Action): you have Resistance to one damage type for 1 hour. The GM chooses the type or rolls 1d10: Acid, Cold, Fire, Force, Lightning, Necrotic, Poison, Psychic, Radiant, Thunder.","Bonus Action",None,"Resistance (half damage) to one type",None,"1 hour",U1,"Type chosen or rolled at drink time by the GM. Consumed.",0.5),
 "Hazmat Slushie, Potion of Resistance. One hour of resistance to one damage type the GM picks.",
 "The color tells you nothing. The color is a rumor.",CI,200,12,"Stood in the Wrong Puddle Box","Resisted a hazard or trap",SRDCHK+" Spec VERIFY resolved: GM chooses or rolls 1d10, 1 hour.")
A.add("Silver","consumable","consumable","Pocket Dragon Breath Mints (Extra Strong)","Potion of Fire Breath (house)","HOUSE","Uncommon","Consumables",
 M('Drink (Bonus Action). For 1 hour, as a Bonus Action you can exhale fire at one creature you can see within 30 ft: Dex save DC 13, 4d6 Fire on a failure, half on a success. Ends after three exhalations or after 1 hour, whichever comes first.',"Bonus Action","30 ft","4d6 Fire (half on save)","Dex DC 13","1 hour or 3 uses",{"max":3,"recharge":"none"},'One exhalation per Bonus Action. Single target, no area. Spent after the third exhalation or the hour. As with any fire effect, flammable unattended objects it hits may ignite (GM).',0.5),
 "Pocket Dragon Breath Mints, Potion of Fire Breath. Three bonus action blasts, thirty feet, four d six fire, dex save thirteen.",
 "Your breath finally has a purpose.",CI,200,10,"Burned the Whole Hallway Box","Used fire in a closed space",
 "HOUSE design (rules/42-house-items-f01.md §5). Numbers follow Lore's draft, which matches secondary listings of the DMG potion; not checked against the book. Uncommon, so inside the Floors 1-2 peak. Open: 4d6 at level 1 is strong (rules/42 §5.4).",tags=["fire","explosives"])
A.add("Silver","gear","item","Pre-Owned Laser Pointer (Cat Not Included)","Wand of Magic Missiles","SRD 5.2","Uncommon","Weapons",
 M("7 charges. Magic action while holding it: expend 1-3 charges to cast Magic Missile (1 charge = level 1: three darts, 1d4+1 Force each, auto-hit, 120 ft; each extra charge raises the spell level by 1, adding a dart). Regains 1d6+1 charges at dawn. If you expend the last charge, roll d20: on a 1 the wand crumbles to ash. 1 lb.","Magic action","120 ft","1d4+1 Force per dart","None (auto-hit)","instant",{"max":7,"recharge":"1d6+1 at dawn"},"Destroyed on a 1 (d20) after the last charge is spent.",1),
 "Pre-Owned Laser Pointer, Wand of Magic Missiles. Seven charges; one charge fires three darts, one d four plus one force each.",
 "Previous owner: a man named Gary. Gary is not available for comment.",CI,300,5,"Brave, Loud, and Mostly Lucky Box","Charged first and won anyway",SRDCHK+" Spec VERIFY resolved: 'cast the level 1 version, +1 level per extra charge'.",tags=["magic missile","cats"])
A.add("Silver","gear","item","Bungee Cord of Questionable Intent","Rope of Climbing","DMG 2024","Uncommon","Misc",
 M("60-ft rope, holds up to 3,000 lb. Magic action: command the free end to move toward a destination within 60 ft (10 ft now, 10 ft at the start of each of your turns), or to fasten, unfasten, knot, unknot or coil. Knotted: shortens to 50 ft and grants Advantage on ability checks to climb it. AC 20, HP 20, immune to Poison and Psychic, regains 1 HP every 5 min; destroyed at 0 HP.","Magic action","60 ft",None,None,"permanent",None,"Destroyed at 0 HP.",3),
 "Bungee Cord of Questionable Intent, Rope of Climbing. Magic action: sixty foot rope moves, knots and fastens itself.",
 "It is very strong. It has opinions about knots.",CI,300,5,"Hauled the Whole Party Up Box","Climbed with allies",DMGCHK.replace("DMG 2024 text (aidedd 5.5 mirror)","SRD 5.2.1 text (web mirror)")+" Spec VERIFY resolved (3,000 lb, 60 ft).")
A.add("Silver","gear","item","Stuck Door Wedge, Industrial","Immovable Rod","SRD 5.2","Uncommon","Misc",
 M("Utilize action: press the button; the rod becomes fixed in place (even in midair) and holds up to 8,000 lb. Utilize again to release. A creature can Utilize to move a fixed rod up to 10 ft with a DC 30 Strength (Athletics) check. More weight deactivates it. 2 lb.","Utilize action",None,None,"Str (Athletics) DC 30 to move","until released",None,"Over 8,000 lb deactivates it.",2),
 "Stuck Door Wedge, Immovable Rod. Utilize to fix it in place; holds eight thousand pounds.",
 "Do not press the button near your own foot.",CI,300,7,"Held the Door Shut Box","Jammed or held a door",SRDCHK)
A.add("Silver","gear","item","Welding Goggles, Night Shift","Goggles of Night","SRD 5.2","Uncommon","Armor",
 M("While worn: Darkvision out to 60 ft; if you already have Darkvision, its range increases by 60 ft.","None (passive)",None,None,None,"while worn",None,"No attunement.",1),
 "Welding Goggles, Goggles of Night. Darkvision sixty feet; adds sixty if you already have it.",
 "You will see everything. Most of it is unflattering.",CI,250,8,"Walked Into the Dark Gladly Box","Navigated a dark area",SRDCHK)
A.add("Silver","gear","item","Library Sneakers (Silent Edition)","Boots of Elvenkind","SRD 5.2","Uncommon","Armor",
 M("While worn: your steps make no sound on any surface; Advantage on Dexterity (Stealth) checks.","None (passive)",None,None,None,"while worn",None,"No attunement.",1),
 "Library Sneakers, Boots of Elvenkind. Silent steps; advantage on stealth checks.",
 "Perfect for sneaking away from your friends.",CI,250,8,"Tiptoed Past Something Awful Box","Sneaked past a threat",SRDCHK+" Spec VERIFY resolved: Advantage on all Dex (Stealth) checks, silent steps.")
A.add("Silver","gear","item","Oven Mitts, Sticky-Fingered","Gloves of Thievery","SRD 5.2","Uncommon","Armor",
 M("While worn, the gloves are imperceptible and you gain a +5 bonus to Dexterity (Sleight of Hand) checks. No attunement.","None (passive)",None,None,"+5 Dex (Sleight of Hand)","while worn",None,"Spec said lock-picking also; 2024 text is Sleight of Hand only.",1),
 "Oven Mitts, Gloves of Thievery. Imperceptible; plus five on sleight of hand checks.",
 "Do not touch the dessert. The dessert is evidence.",CI,250,6,"Pickpocketed a Pickpocket Box","Stole or picked something",SRDCHK+" Spec VERIFY attunement resolved: none.",tags=["thieving"])
A.add("Silver","tailored","item","Hi-Vis Safety Vest, Reflective","Cloak of Protection","SRD 5.2","Uncommon","Armor",
 M("Requires attunement. While worn: +1 bonus to Armor Class and +1 bonus to all saving throws.","None (passive)",None,None,None,"while worn and attuned",None,"Counts toward the 3-item attunement limit.",1),
 "Hi-Vis Safety Vest, Cloak of Protection. Attune it for plus one Armor Class and plus one on all saving throws.",
 "Visible from orbit. So are you.",CI,400,5,"Survived the Obvious Hazard Box","Avoided damage by luck or skill",SRDCHK+" Build-aware tailored pull for armor-light fighters. Counts as the crawler's permanent Uncommon on F1.",attune="yes",tags=["armor"])
A.add("Silver","tailored","item","Pearl From a Very Expensive Necklace (Allegedly)","Pearl of Power","SRD 5.2","Uncommon","Misc",
 M("Requires attunement by a spellcaster. While on your person, Magic action: regain one expended spell slot of level 3 or lower. Once used, not again until next dawn.","Magic action",None,None,None,"instant",{"max":1,"recharge":"dawn"},"Spellcasters only; counts toward attunement limit.",0),
 "Pearl From a Very Expensive Necklace, Pearl of Power. Spellcasters: once per dawn, regain one spell slot, third level or lower.",
 "The necklace is fine. The pearl wanted out.",CI,400,4,"Bet on the Wizard Box","Out-of-slots wizard won anyway",SRDCHK,attune="yes: spellcaster",tags=["wizard","spellcasting"])
A.add("Silver","gear","item","Mop Handle of Mild Menace","+1 Quarterstaff","SRD 5.2","Uncommon","Weapons",
 M("A magic quarterstaff: +1 bonus to attack and damage rolls made with it. Quarterstaff: 1d6 Bludgeoning, Versatile (1d8), Topple mastery (if you have it). 4 lb.","Attack action","Melee",
   "1d6+1 Bludgeoning (1d8+1 two-handed)",None,"permanent",None,"No attunement. Needs proficiency to add your proficiency bonus.",4),
 "Mop Handle of Mild Menace, plus one quarterstaff. Plus one to attack and damage; one d six bludgeoning.",
 "It has seen things. It has mopped them.",CI,400,4,"Hit It With a Stick Box","Won a fight with improvised weapons",SRDCHK+" Reskin of a mundane quarterstaff; Weapon +1 is Uncommon (2024). Also counts as the crawler's permanent Uncommon.",tags=["staff","quarterstaff"])
A.add("Silver","weird","consumable","Aquarium Cocktail, Do Not Swallow Fish","Potion of Water Breathing","SRD 5.2","Uncommon","Consumables",
 M("Drink (Bonus Action): you can breathe underwater for 24 hours. One use.","Bonus Action",None,None,None,"24 hours",U1,"Floor 1 has no water. Keep it for later floors.",0.5),
 "Aquarium Cocktail, Potion of Water Breathing. Twenty-four hours of breathing underwater.",
 "Floor One has no water. We are not sorry.",CI,150,5,"Packed for the Wrong Floor Box","Prepared for a danger that wasn't there",SRDCHK+" Joke-ish weird pull on F1, genuinely useful from later floors.")
A.add("Silver","gear","item","Duffel Bag, Roomier Inside","Bag of Holding","SRD 5.2","Uncommon","Misc",
 M("Holds up to 500 lb, not exceeding 64 cubic feet; the bag weighs 5 lb regardless of contents. Utilize action to retrieve an item. Overloading, piercing or tearing destroys it and scatters the contents in the Astral Plane. Never place it inside another extradimensional space.","Utilize action (retrieve)",None,None,None,"permanent",None,"Spec weight (15 lb) was wrong; 2024 is 5 lb. Redundant with System Inventory (core §5.9).",5),
 "Duffel Bag, Bag of Holding. Holds five hundred pounds; Utilize to retrieve an item.",
 "Bottomless, like your shame.",CI,400,0,"Packed Everything You Own Box","Carried too much",SRDCHK+" draw_weight 0 pending spec §5 Q5 (ban vs physical stash job). Hand-pick only.")
A.add("Silver","tailored","item","Rolled-Up Gym Socks (Lucky)","Boots of Elvenkind","SRD 5.2","Uncommon","Armor",
 M("(Duplicate shell: see Library Sneakers.)","none"),
 "x","x",CI,250,0,"x","x","placeholder")  # removed below
A.cards.pop(); A.n -= 1
for i,(nm,box,deed,sn) in enumerate([
 ("Sponsor-Adjacent Gift Envelope","Impressed the Wrong People Box","Won on style",   "Sent by a mystery donor who is, suspiciously, the System."),
 ("Severance Package (Partial)","Survived the Layoff Box","Survived against the odds","Not nearly enough. Enjoy the enough.")],1):
    A.add("Silver","credits","credits",nm,"Credits (Silver pull, 2d6 x 25)","HOUSE","n/a","Credits",
     M("Adds 2d6 x 25 credits (50-300) to your balance when the box is opened. Roll at draw time with tools/roll.py. No weight.","none",None,None,None,"instant",None,"Added when the box is opened.",0),
     "%s. Silver credits: two d six times twenty-five, added to your balance." % nm,
     sn,CI,175,12,box,deed,"credit_value = expected value (7 x 25). Roll at draw.",grant=credits_grant("2d6x25"),ledger_ids="L-001")

# Story Box item (HOUSE, Legendary, hand-pick only; spec 2.8; Caleb approved the Story Box exception for Floors 1-2 on 2026-10-04). Text: rules/42-house-items-f01.md section 6.
A.add("Legendary","weird","consumable","Enhanced Pet Biscuit","Enhanced Pet Biscuit (house: pet-to-Crawler consumable)","HOUSE","Legendary","Consumables",
 M('Utilize action: feed it to your willing pet (a Beast, CR 1/4 or lower). The pet becomes a Crawler: it gets the System interface (inventory, map, achievements, boxes), speech, Int/Wis/Cha of at least 10, and a class at the next saferoom (level = party level). One conversion per living pet-Crawler: a deleted pet-Crawler frees its conversion, but a new conversion needs a new Enhanced Pet Biscuit (which uses a Story Box slot). No effect on a creature that is already a Crawler.',"Utilize action","5 ft",None,None,"permanent",U1,"Pet only: the GM decides what counts as yours. Irreversible. Roll d4 for one Biscuit Quirk (rules/42 §6.2). Boxes and loot of the new Crawler follow core §4.4 like any Crawler's.",0.1),
 'Enhanced Pet Biscuit. Feed it to your pet: the pet becomes a Crawler, with a System interface and a class at the next saferoom.',
 'Good boy. Good, billable, ratings-eligible boy.',CI,0,0,"Pet Box","Brought a pet into the Crawl",
 'Story Box card (spec §2.8): GM-triggered only, hand-pick, never drawn. trigger_deed: first Crawler at the table to bring a pet into the Crawl, judged by the GM (canon trigger not captured in the ledger). Banner adds the tier: Legendary Pet Box. Item canon I-007 and M-037; mechanics are HOUSE. power_note: Story keystone (pattern C), consumed once, rung 0 numbers: the new Crawler is a CR 1/4 Beast stat block plus a class at party level, so it adds a Crawler to encounter budgets and uses the owner\'s one consumable for the floor. Once fed it\'s consumed; the pet-Crawler can\'t be traded; one conversion per living pet-Crawler (a deleted pet-Crawler frees its conversion; a new conversion still needs a new Enhanced Pet Biscuit, which uses a Story Box slot). An unused biscuit is a normal tradable, sellable, lootable item. The pet-Crawler is a separate player-controlled Crawler played by the owner, takes no extra slot. Hook: the pet now has opinions, and the audience adores it. (rules/45 section 4.5) Not bound (bound is false): lootable, tradeable, sellable like any item; story_value is provenance only and never the buyback base; sale_value 100 (System buyback at Floor-1 scale, times the multiplier of the sale floor at runtime). Opens only in a saferoom: the deed is recorded and announced at award and the box waits unopened until the next saferoom.',
 tags=["pets"],unique=True,num=55,story=40000,bound=False,sale=100,ledger_text="item +1 Legendary Story Box: Enhanced Pet Biscuit (story value 40000, not bound)")

# Needs-verify (kept OUT of cards[]; not drawable until a 2024 text check passes).
NEEDS_VERIFY = [
 {"candidate_reskin": "Beastmaster Treat Bag", "real_5e_name": "Potion of Animal Friendship", "tier": "Silver", "suggested_credit_value": 150,
  "spec_ref": "rules/40 §3.1 B (flag: VERIFY save DC and duration)",
  "reason": "SRD 5.2 page only says 'you can cast the level 3 version of Animal Friendship (save DC 13)'; casting time, duration and beast count were not confirmed from the printed book. Not drawable."},
 {"candidate_reskin": "Gym-Bro Protein Shake, Hill Flavor", "real_5e_name": "Potion of Giant Strength (Hill)", "tier": "Silver", "suggested_credit_value": 200,
  "spec_ref": "rules/40 §3.1 B (no flag in spec)",
  "reason": "Could not find the item text in either SRD 5.2.1 mirror used (ilmatar has no page; aidedd 5.5 has no 'potion-of-giant-strength-hill' page). Strength 21 for 1 hour is from the spec only. Not drawable."},
 {"candidate_reskin": "Riot Shield, Sharpie'd PROPERTY OF ORIENTATION (+1)", "real_5e_name": "+1 Shield", "tier": "Silver", "suggested_credit_value": 400,
  "spec_ref": "rules/40 §3.1 D (flag: VERIFY rarity, Uncommon in 2014)",
  "reason": "SRD 5.2 lists '+1 Shield' under Armor but the rarity and exact AC text were not confirmed (2024 Shield is +2 AC base). Not drawable."},
 {"candidate_reskin": "Heward's Handy Haversack (Sponsor Edition)", "real_5e_name": "Heward's Handy Haversack", "tier": "Gold", "suggested_credit_value": 1500,
  "spec_ref": "rules/40 §3.1 C (flag: VERIFY 2024 stats and SRD inclusion)",
  "reason": "Gold/Rare is above the Floor 1 ceiling (Uncommon peak); Benefactor-only and Benefactors do not exist on Floor 1. Parked, not built."},
 {"candidate_reskin": "Portable Hole in a Hoodie", "real_5e_name": "Portable Hole", "tier": "Gold", "suggested_credit_value": 1500,
  "spec_ref": "rules/40 §3.1 C (flag: VERIFY rarity and rules)",
  "reason": "Gold/Rare is above the Floor 1 ceiling and Benefactor-only. Parked, not built."},
]

# ------------------------------------------------------------------ Z03 Vending Gore Arcade
Z3 = Deck("z03", "vending-gore-arcade", "Zone 3: Vending Gore Arcade")
Z3.add("Bronze","consumable","consumable","Snack Cake, Expiration Date: Yes","Rations (1 day)","PHB 2024","Mundane","Consumables",
 M("Travel food for one day. 2 lb.","none",None,None,None,"1 day",{"max":1,"recharge":"none"},"One day's food.",2),
 "Snack Cake, Expiration Date: Yes, Rations. One day of food.",
 "It is technically food. It is also technically old.",CI,0.5,25,"Robbed a Machine That Bites Box","Looted a hungry vendor",
 SRDCHK+" Vending Gore d6=3 result.",ledger_ids="L-B04 (Apparel Box on F1 is WIKI-ONLY; vending flavor is HOUSE)",tags=["food"])
Z3.add("Bronze","gear","item","Big Honking Flashlight (Vending Edition)","Lantern, Hooded","PHB 2024","Mundane","Misc",
 M("Burns Oil: bright light 30 ft, dim light another 30 ft; one oil flask lasts 6 hours. Bonus Action: lower the hood (dim 5 ft) or raise it again.","Bonus Action (hood)","30 ft + 30 ft","None","None","6 hours per Oil flask",None,"Needs Oil and a flame.",2),
 "Big Honking Flashlight, Hooded Lantern. Thirty feet bright, thirty dim; Bonus Action to lower the hood.",
 "Batteries not included, but oil is, and we are not discussing it.",CI,5,15,"Raided the Hardware Aisle Box","Opened a vendor",SRDCHK+" Vending d6=4 mundane item.")
Z3.add("Bronze","gear","item","Extension Cord, Fifty Feet (Vending Edition)","Rope (hempen, 50 ft)","PHB 2024","Mundane","Misc",
 M("Utilize action: tie a knot (DC 10 Dex (Sleight of Hand)). Bursts on a DC 20 Strength (Athletics) check. Binds an unwilling creature only if it is Grappled, Incapacitated or Restrained; escape DC 15 Dex (Acrobatics). 5 lb.","Utilize action","50 ft",None,"Burst Str DC 20; escape Dex DC 15","permanent",None,"2024 numbers.",5),
 "Extension Cord, Rope. Fifty feet; knots with a dex check ten, bursts at strength twenty.",
 "The vending machine never plugged it in. Neither will you.",CI,1,15,"Grabbed the Rope from the Display Box","Reached into the vending machine",SRDCHK)
Z3.add("Bronze","consumable","consumable","Flaming Hot Nacho Cheese Pouch","Alchemist's Fire","PHB 2024","Mundane","Consumables",
 M("Attack action (replace one attack): throw at a creature or object you can see within 20 ft. Dex save (DC 8 + thrower's Dex modifier + proficiency bonus) or it takes 1d4 Fire damage and starts burning (1d4 Fire at the start of each of its turns until the flames are put out; see Burning in the Rules Glossary). One use. 1 lb.","Attack action (replaces one attack)","20 ft","1d4 Fire, then 1d4 per turn while burning","Dex DC 8 + Dex mod + prof","until extinguished",U1,"Consumed on throw.",1),
 "Flaming Hot Nacho Cheese Pouch, Alchemist's Fire. Thrown twenty feet; failed dex save means one d four fire, burning each turn.",
 "Do not lick the nozzle. We already tried.",CI,50,25,"Stabbed the Vending Machine Box","Fought a vending machine",SRDCHK+" Spec sample id kept (f01-z03-0004). Spec VERIFY first-hit timing resolved: Dex save, burning per Rules Glossary.",tags=["explosives","fire"],num=4,ledger_ids="L-018, I-013 (explosives, goblin dynamite) flavor only")
Z3.add("Bronze","consumable","consumable","Bag of LEGO (Vending Edition)","Caltrops","PHB 2024","Mundane","Consumables",
 M("Utilize action: spread over a 5-ft square within 5 ft. A creature entering for the first time on a turn makes a DC 15 Dex save or takes 1 Piercing and its Speed drops to 0 until the start of its next turn. 10 minutes to recover.","Utilize action","5 ft","1 Piercing","Dex DC 15","until picked up",None,"Reusable once recovered.",2),
 "Bag of LEGO, Caltrops. Spread a five foot square; failed dex save means one damage and speed zero.",
 "Every parent's nightmare, now with receipts.",CI,1,15,"Stepped on It Box","Used a vending machine item as a trap",SRDCHK)
Z3.add("Bronze","consumable","consumable","Fryer Grease, Reclaimed","Oil (flask)","PHB 2024","Mundane","Consumables",
 M("Attack action (replace one attack): throw at a creature or object within 20 ft; Dex save (DC 8 + Dex mod + proficiency bonus) or it is coated for 1 minute; Fire damage in that time adds 5 Fire. OR Utilize: pour on a 5-ft square within 5 ft; if lit, 5 Fire to any creature entering or ending its turn there (once per turn) for 2 rounds. Fuel for a lantern, 6 hours.","Attack action or Utilize action","20 ft / 5 ft","5 Fire (burning oil)","Dex DC 8 + Dex mod + prof","1 minute / 2 rounds",U1,"Consumed.",1),
 "Fryer Grease, Oil flask. Coat a target or pour a pool; fire adds five damage.",
 "Season it, light it, then cry.",CI,0.1,15,"Lit the Grease Fire Box","Burned something greasy",SRDCHK,tags=["fire","cooking"])
Z3.add("Bronze","weird","junk","SOLD OUT FOREVER Sticker","Joke item (house: no effect)","HOUSE","n/a","Misc",
 M("Joke item. No mechanical effect. A sticker the vending machine peels off and hands you.","none",None,None,None,"permanent",None,"Does nothing. It does look official.",0),
 "SOLD OUT FOREVER Sticker. Joke item. No mechanical effect.",
 "Finally, a promise the System keeps.",H,0,6,"Overstayed at the Machine Box","Kept raiding vending machines after the cap",
 "Matches 'SOLD OUT FOREVER' cap in floor doc §5.3. Use as the dud when a crawler farms vending.")
Z3.add("Bronze","credits","credits","Snack-Machine Change Slot, Jammed Open","Credits (Bronze pull, 3d6 x 5)","HOUSE","n/a","Credits",
 M("Adds 3d6 x 5 credits (15-90) to your balance when the box is opened. Roll at draw time. No weight.","none",None,None,None,"instant",None,"Added when the box is opened.",0),
 "Snack-Machine Change Slot. Bronze credits: three d six times five, added to your balance.",
 "The machine coughed it up. Do not thank the machine.",CI,52.5,12,"Broke the Change Machine Box","Smashed a change machine",
 "credit_value = expected value. Roll at draw.",grant=credits_grant("3d6x5"),ledger_ids="L-001")

# ------------------------------------------------------------------ Z06 Break Room
Z6 = Deck("z06", "break-room", "Zone 6: The Break Room (Saferoom A)", version="0.1.1", updated="2026-10-07")
Z6.add("Bronze","weird","consumable","Laminated Complaint Card","Laminated Complaint Card (house: single-use oracle)","HOUSE","Common","Consumables",
 M("Utilize action, once: ask the System one yes/no question about the current floor; it answers truthfully, yes or no. The card is then spent.","Utilize action",None,None,None,"instant",U1,"Must be a yes/no question about the floor you are on. A question that is not yes/no is refused and the card is not spent. Never reveals spine secrets or GM-only information: a question about them gets bureaucratic runaround (a form number, 'your complaint has been escalated', 'please allow 6-8 floors for processing') and the card is spent.",0),
 "Laminated Complaint Card. One use: ask the System one yes-or-no question about this floor. It must answer truthfully.",
 "The System has never lost a complaint; it files them under Funny.",H,25,10,"Filed a Formal Complaint Box","Filed a formal complaint with the System",
 "Alpha-test item (2026-10-04, Bone). Lore ruling 2026-10-07 (resolves spec §5 Q3 on the Lore side; Syndicate/Caleb may still overrule in rules/40): the card never reveals spine secrets (Odd Coin, Benefactor, Black Box, etc.) or GM-only information; such questions get bureaucratic runaround instead of yes/no, the card is still spent, and it never confirms or denies that a secret exists.")
Z6.add("Bronze","consumable","consumable","Sports Drink, Blue Flavor","Potion of Healing","SRD 5.2","Common","Consumables",
 M("Bonus Action: drink it, or give it to a creature within 5 ft; the drinker regains 2d4+2 HP. One use.","Bonus Action","5 ft (to give)",None,None,"instant",U1,"Consumed on use.",0.5),
 "Sports Drink, Blue Flavor, Potion of Healing. Bonus Action: regain two d four plus two hit points.",
 "Tastes like a lawsuit.",CA,50,25,"Bled on the Break Room Carpet Box","Took damage and reached the saferoom",
 SRDCHK+" Alpha draw (Bone). Break Room vendor stock is 2 for the floor; box potions are extra and cost vendor-stock nothing.",ledger_ids="I-009; L-B02")
Z6.add("Bronze","weird","junk","Kevin the Sentient Rubber Duck","Rubber Duck (house: joke item, no effect)","HOUSE","n/a","Misc",
 M("Joke item. No mechanical effect. Kevin gives terrible advice; the GM treats it as flavor only.","none",None,None,None,"permanent",None,"No effect on dice, DCs, damage or saves.",0),
 "Kevin the Sentient Rubber Duck. Weird pull, joke item, no mechanical effect.",
 "Kevin is not licensed.",H,0,10,"Took Bad Advice Seriously Box","Followed terrible advice","Alpha item (Bone). Duplicate of the any-deck Kevin; keep one in play per crawler.")
Z6.add("Bronze","key","key","Gas-Station Bathroom Key on a Hubcap","Mystery Key (house, single lock)","HOUSE","Common","Keys",
 M('Utilize action: opens one specific lock on this floor, picked by the GM when the key is drawn (the GM does not say which). On that lock it unlocks it and the key is spent. On any other lock nothing happens and it is not spent. If you leave the floor with it unused, it becomes a plain hubcap key.',"Utilize action",None,None,None,"until used or you leave the floor",U1,'One use, one lock. Cannot open a lock sealed by a boss, spine object or magic barrier. Never the only way through a required door.',1),
 'Gas-Station Bathroom Key on a Hubcap. House Mystery Key: opens one GM-chosen lock on this floor; spent on use.',
 "It opens something, and the System is not telling.",H,25,6,"Found the Right Key Eventually Box","Hunted for a way through a locked door",
 'HOUSE design (rules/42-house-items-f01.md §4). Break Room copy, same text as f01-any-0035. GM only: pick the lock at draw and write it into session state (suggest the Break Room supply cabinet or the 3b cage).')
Z6.add("Bronze","credits","credits","Credits, Slightly Damp","Credits (Bronze pull, 3d6 x 5)","HOUSE","n/a","Credits",
 M("Adds 3d6 x 5 credits (15-90) to your balance when the box is opened. Roll at draw time with tools/roll.py. No weight.","none",None,None,None,"instant",None,"Added when the box is opened.",0),
 "Credits, Slightly Damp. Bronze credits: three d six times five. They are damp. Do not ask what from.",
 "Please spend it before it ferments.",CI,52.5,25,"Participation Trophy Box","Showed up, technically",
 "Spec sample 5 id (f01-z06-0005) but credits:null and roll at draw per spec preference.",grant=credits_grant("3d6x5"),num=5,ledger_ids="L-001")
Z6.add("Bronze","consumable","consumable","Break-Room First-Aid Kit, Lightly Bitten","Healer's Kit","PHB 2024","Mundane","Consumables",
 M("Utilize action: expend 1 of 10 uses to stabilize an Unconscious creature at 0 HP without a Wisdom (Medicine) check.","Utilize action","Touch",None,None,"instant",{"max":10,"recharge":"none"},"Stabilizes only.",3),
 "Break-Room First-Aid Kit, Healer's Kit. Ten uses: Utilize to stabilize a creature at zero hit points.",
 "Stabilize them. Do not ask what bit the kit.",CI,5,12,"Dragged Someone Out of the Fire Box","Stabilized a dying teammate",SRDCHK)
Z6.add("Bronze","weird","junk","Fridge Sandwich Labeled DALE'S. DO NOT.","Joke item (house: no effect)","HOUSE","n/a","Misc",
 M("Joke item. Eating it counts as food for one day (rations) but the label says no. Eating it in front of Dale triggers Lunch Thief.","none",None,None,None,"1 day",{"max":1,"recharge":"none"},"Dale has seen what you did.",1),
 "Fridge Sandwich Labeled Dale's. Joke item; counts as one day of food.",
 "Dale saw. Dale will always have seen.",H,1,6,"Ate Dale's Lunch Box","Ate a labeled sandwich",
 "Pairs with NEW achievement Lunch Thief. Mechanically a ration.")

# ------------------------------------------------------------------ Z09 Green Room (spine fallback + drawable set, v0.1.1)
Z9 = Deck("z09", "green-room", "Zone 9: The Green Room (Saferoom B)", version="0.1.3", updated="2026-10-07")
Z9.add("Bronze","weird","clue","Vendor Oddity (Unappraised)","Spine object: Odd Coin (house; no mechanics on Floor 1)","HOUSE","n/a","Misc",
 M("A coin, probably. Value: ???. This item cannot be sold. It has no mechanical effect on Floor 1.","none",None,None,None,"permanent",None,"Cannot be sold; do not explain it. Sell attempt: terminal says ITEM NOT RECOGNIZED or offers 500 credits and cancels. Identify/appraise attempt (any terminal, vendor or the System, any fee): same response as a sell attempt, ITEM NOT RECOGNIZED (or the 500-credit offer that cancels mid-animation); any fee is not taken. Never name a floor, a fee, a clearance level or a future appraisal.",0),
 "Vendor Oddity, Unappraised. A coin, probably. It cannot be sold.",
 "Value unknown, and trying to sell it is embarrassing for everyone.",H,0,0,"Opened Something Nobody Opens Box","Opened a box in the Green Room",
 "SEED-ODDCOIN FALLBACK ONLY (draw_weight 0, hand-pick only): if the Lost & Found crate (Zone 3) was never opened, the coin shows up here as a Weird pull in the first Green Room box. Must be planted on F1; never explain it. credit_value 0 because it cannot be sold. Identify rule added 2026-10-07 (Lore, after s1 review): the GM improvised a floor-gated appraisal reply in s1; use only ITEM NOT RECOGNIZED or the cancelled 500-credit offer.",unique=True)
Z9.add("Bronze","weird","junk","Fruit Plate That Has Become Something Else","Joke item (house: no effect)","HOUSE","n/a","Misc",
 M("Joke item. No mechanical effect. It is looking at you.","none",None,None,None,"permanent",None,"Do not eat.",1),
 "Fruit Plate That Has Become Something Else. Joke item. No mechanical effect.",
 "Enjoy the fruit.",H,0,8,"Ate Backstage Food Box","Searched the Green Room",
 "Floor doc §5.9 flavor. Pure dud.")

# ---- v0.1.1: drawable Green Room set (Accountant found the deck had nothing with weight > 0).
# Flavor from floor doc 5.9: backstage green room, bulb-ringed mirror (half dead), folding chairs, fruit plate,
# STAFF ONLY, Midterm / level 2, Proctor Bell parked. Real items are 2024 SRD 5.2.1 gear not already in the
# other F1 decks (except the Silver Greater Healing: consumables may repeat, spec 2.3). Text: 5e24srd.com / ilmatar SRD 5.2.
ZCHK = "Mechanics checked vs SRD 5.2.1 text (5e24srd.com / ilmatar mirrors) 2026-10-04."
Z9.add("Bronze","consumable","consumable","Dead Mirror Bulb, Briefly Alive","Spell Scroll (Light, cantrip)","SRD 5.2","Common","Consumables",
 M("Magic action: if Light is on your class's spell list (Bard, Cleric, Sorcerer, Wizard), read the scroll to cast it: touch one Large or smaller object not worn or carried by someone else; it sheds bright light in a 20-ft radius and dim light 20 ft more for 1 hour. Covering it with something opaque blocks the light. The scroll then disintegrates.","Magic action","Touch",None,None,"1 hour",U1,"Only a class with Light on its list can read it. No Material component needed. Consumed.",0),
 "Dead Mirror Bulb, Spell Scroll of Light. Bards, Clerics, Sorcerers, Wizards: touch an object; twenty feet of bright light for one hour.",
 "It was dead, then it got better. Tell no other bulbs.",CI,50,8,"Relit the Dressing-Room Mirror Box","Brought light to a dark corner of the Green Room",
 ZCHK+" Cantrip scroll: no save or attack, so DC 13 / +5 is irrelevant. Green Room flavor: half the mirror bulbs are dead (floor doc 5.9).",tags=["light","wizard"])
Z9.add("Bronze","consumable","consumable","Stage Whisper Cue Card","Spell Scroll (Healing Word, level 1)","SRD 5.2","Common","Consumables",
 M("Bonus Action: if Healing Word is on your class's spell list (Bard, Cleric, Druid), read the scroll to cast it at level 1: one creature you can see within 60 ft regains 2d4 + your spellcasting ability modifier HP. The scroll then disintegrates.","Bonus Action","60 ft","2d4 + spellcasting modifier HP restored",None,"instant",U1,"Only a class with Healing Word on its list can read it. Verbal component only. Consumed.",0),
 "Stage Whisper Cue Card, Spell Scroll of Healing Word. Bards, Clerics, Druids: Bonus Action, sixty feet, heal two d four plus modifier.",
 "Whispered from the wings. The audience hears everything anyway.",CI,75,8,"Whispered a Line From the Wings Box","Talked a downed teammate back on their feet",
 ZCHK+" Level 1 scroll; no save or attack. Healing Word casting time is a Bonus Action, so the scroll is too. Pairs with the pre-boss rest.")
Z9.add("Bronze","consumable","consumable","Dressing-Room Body Spray, Industrial Lilac","Perfume","PHB 2024","Mundane","Consumables",
 M("Utilize action: apply it to yourself. For 1 hour you have Advantage on Charisma (Persuasion) checks made to influence an Indifferent Humanoid within 5 ft of you. One 4-oz vial, one application.","Utilize action","5 ft (target of the check)",None,None,"1 hour",U1,"Only works on Indifferent Humanoids. Consumed on application. Floor 1 mascots and Ushers are not impressed.",0),
 "Dressing-Room Body Spray, Perfume. Utilize to apply; one hour of advantage on Persuasion against an indifferent humanoid within five feet.",
 "Smells like three decades of opening nights.",CI,5,10,"Smelled Like Victory, Mostly Lilac Box","Rested in the Green Room",
 ZCHK+" Utilize action is the house reading (2024 text says only 'after applying'). Useful for the Thudd talk-down route (floor doc 6.6) only if Thudd is Indifferent; GM call.")
Z9.add("Bronze","consumable","consumable","Dressing-Room Candle, Scented Like a Funeral","Candle","PHB 2024","Mundane","Consumables",
 M("Once lit, it sheds bright light in a 5-ft radius and dim light for 5 ft more for 1 hour. Lighting it takes a Bonus Action with a Tinderbox or any open flame.","none","5 ft bright + 5 ft dim",None,None,"1 hour",U1,"Burns out after 1 hour; needs a flame source.",0),
 "Dressing-Room Candle, Candle. One hour of light: five feet bright, five more dim.",
 "The replacement for the dead bulbs, dying on the same schedule.",CI,0.01,8,"Made Do With Half the Lights Box","Worked in a badly lit room",
 ZCHK+" Value 0.01 (1 cp). Burglar's Pack item, not a duplicate of the Torch or Birthday Candle scroll in the any-deck.")
Z9.add("Bronze","tailored","item","Stage Makeup Kit, Half-Dried","Disguise Kit","PHB 2024","Mundane","Misc",
 M("Utilize action: apply makeup to create a visual disguise; Charisma check, DC 10, using the kit (add your proficiency bonus if proficient). It can also be used to craft a Costume. 3 lb.","Utilize action","Self or touch",None,"Cha check DC 10","until washed off",None,"Visual disguise only: no voice, mannerism or height change.",3),
 "Stage Makeup Kit, Disguise Kit. Utilize to apply makeup; Charisma check ten makes a visual disguise.",
 "Contour like nobody is watching. Four million people are watching.",CI,25,10,"Put On a Face for the Audience Box","Disguised yourself or impersonated someone",
 ZCHK+" Disguise Kit tool entry (Ability Charisma, Utilize: Apply makeup DC 10). The 'visual only' limit is the 2014/2024 flavor text; GM call on edge cases.",tags=["costumes","makeup"])
Z9.add("Bronze","gear","item","Vanity Mirror, Half the Bulbs Dead","Mirror","PHB 2024","Mundane","Misc",
 M("A handheld steel mirror: use it to peek around corners without exposing yourself, to signal by reflecting light, or for cosmetics. No other effect. 1/2 lb.","none",None,None,None,"permanent",None,"No mechanical bonus; the GM rules what a peek reveals.",0.5),
 "Vanity Mirror, Mirror. Peek around corners without stepping out, or flash a signal with reflected light.",
 "Reflects well on no one.",CI,5,10,"Checked Your Reflection Mid-Crisis Box","Looked around a corner before charging in",
 ZCHK+" Weight 1/2 lb. Pairs with the bulb-ringed mirror in the zone description.")
Z9.add("Bronze","gear","item","Curtain Rigging Pulley, Stage Left","Block and Tackle","PHB 2024","Mundane","Misc",
 M("Passive while rigged: you can hoist up to four times the weight you can normally lift. 5 lb.","None (passive)",None,None,None,"while rigged",None,"Needs something to anchor it to; a lift, not a throw.",5),
 "Curtain Rigging Pulley, Block and Tackle. Hoist up to four times the weight you can normally lift.",
 "Built for lifting curtains. Works on anything heavy and uninterested.",CI,1,8,"Hauled the Stage Props Box","Lifted or moved something heavy",ZCHK+" Mason's Tools craft item; 1 gp.")
Z9.add("Bronze","gear","item","Midterm Blazer, Embroidered STAFF","Clothes, Fine","PHB 2024","Mundane","Misc",
 M("Expensive-looking clothes: some events and locations admit only people wearing Fine Clothes (GM decides which). No AC, no other effect. 6 lb.","none",None,None,None,"while worn",None,"Cosmetic and access only; no AC.",6),
 "Midterm Blazer, Fine Clothes. Some events and places admit only people wearing these.",
 "Dress for the job you will not survive to keep.",CI,15,8,"Dressed for the Funeral Early Box","Dressed up for a high-stakes room",
 ZCHK+" Fine Clothes, 15 gp. Staff-only door flavor (floor doc 5.9); no mechanical gate is written on F1, so purely a roleplay key.",tags=["clothing"])
Z9.add("Bronze","gear","item","Prop Arrows, Foam Tips Removed","Arrows (20)","PHB 2024","Mundane","Misc",
 M("Twenty arrows: ammunition for a Shortbow or Longbow; each shot uses one arrow. After a fight you can spend 1 minute to recover half the arrows you used (rounded down); the rest are lost. A Quiver (1 gp) holds them; this bundle does not include one. 1 lb.","none",None,None,None,"until spent",{"max":20,"recharge":"none"},"Useless without a Shortbow or Longbow. Damage comes from the bow. Recover half the arrows used (rounded down) with 1 minute after a fight; the rest are lost.",1),
 "Prop Arrows, Arrows. Twenty pieces of ammunition for a shortbow or longbow.",
 "Someone removed the foam. That someone is a problem for later.",CI,1,8,"Shot Something Across the Room Box","Hit an enemy from range",
 ZCHK+" Arrows 20 / 1 lb / 1 gp. Ammunition-recovery rule added 2026-10-04 per Syndicate's SRD check.",tags=["archery"])
Z9.add("Bronze","credits","credits","Backstage Per Diem Envelope, Water-Stained","Credits (Bronze pull, 3d6 x 5)","HOUSE","n/a","Credits",
 M("Adds 3d6 x 5 credits (15-90) to your balance when the box is opened. Roll at draw time with tools/roll.py. No weight.","none",None,None,None,"instant",None,"Added when the box is opened.",0),
 "Backstage Per Diem Envelope. Bronze credits: three d six times five, added to your balance.",
 "Meant for catering. Catering was cancelled in your honor.",CI,52.5,20,"Took the Per Diem and Ran Box","Searched a dressing-room drawer",
 "credit_value = expected value (10.5 x 5). Roll at draw.",grant=credits_grant("3d6x5"),ledger_ids="L-001")

# Silver: Green Room is the opening spot for the replacement-crawler Silver late-entry compensation box
# (floor doc 5.9). The Boss Box (z10) is the only other Silver on F1, so these stay low weight / hand-pick.
Z9.add("Silver","consumable","consumable","Green-Room Smoothie, Pre-Show Strength","Potion of Healing (greater)","SRD 5.2","Uncommon","Consumables",
 M("Bonus Action: drink it, or give it to a creature within 5 ft; the drinker regains 4d4+4 HP. One use.","Bonus Action","5 ft (to give)",None,None,"instant",U1,"Consumed on use.",0.5),
 "Green-Room Smoothie, Potion of Greater Healing. Bonus Action: regain four d four plus four hit points.",
 "Gluten-free, sugar-free, and somehow still against the rules.",CI,150,5,"Arrived Late, Apologized Early Box","Joined the crawl late as a replacement crawler",
 ZCHK+" Same real item as the any-deck and z10 Greater Healing on purpose: consumables may repeat (spec 2.3), and it is the pre-boss heal. Low weight: Silver only opens here as the replacement-crawler late-entry box (floor doc 5.9); GM may hand-pick instead. Spec price HOUSE (VERIFY retained).")
Z9.add("Silver","gear","item","Stage-Crew Gaffer Wristbands, Pointing Hand","Bracers of Archery","SRD 5.2","Uncommon","Armor",
 M("Requires attunement. While worn: proficiency with the Longbow and Shortbow, and +2 bonus to damage rolls made with them.","None (passive)",None,"+2 damage with Longbow/Shortbow",None,"while worn and attuned",None,"Counts toward the 3-item attunement limit and is the crawler's permanent Uncommon on F1 (floor doc 8: 0-1 per crawler).",1),
 "Stage-Crew Gaffer Wristbands, Bracers of Archery. Attune: shortbow and longbow proficiency, plus two damage with them.",
 "Points at the exit. The exit is not impressed.",CI,400,0,"Arrived Dressed for the Part Box","Joined the crawl late with a bow in hand",
 ZCHK+" HAND-PICK ONLY (weight 0): permanent Uncommon item, so GM gives it deliberately (replacement archer; do not stack with another permanent Uncommon on the same crawler). Value 400 from spec 3.1 D.",attune="yes",tags=["archery"])

Z9.add("Bronze","gear","item",'Wardrobe-Rack Hoodie, Many Moods',"Cloak of Many Fashions (house)","HOUSE","Common","Misc",
 M('Worn as your outer garment (no attunement). Bonus Action: change its style, color and apparent quality to any cloak, hoodie, cape or vest you have seen. Looks only: no AC, no powers, no bonus to any check. Weight does not change.',"Bonus Action",None,None,None,"until you change it",None,'Cosmetic only. Copies the look of other garments, never their properties or magic. You can wear only one outer-garment magic item at a time (house). It always stays a garment of about its own size. Touching it reveals nothing odd.',1),
 'Wardrobe-Rack Hoodie, Cloak of Many Fashions. Bonus Action: change its style and color. Looks only.',
 'Looks great on every Crawler. Looks do not stop knives.',CI,50,6,'Changed Outfits Mid-Fight Box','Switched costumes backstage',
 'HOUSE design (rules/42-house-items-f01.md §2). Follows the general shape of the DMG cloak from memory; not copied, not checked against the book. Same text for f01-any-0028 (unique, weight 0, exclusive card for the alpha holder): only id, zone, weight, unique, exclusive_to, reskin and box fields differ.',tags=["clothing"])

# ------------------------------------------------------------------ Z10 Graduation Stage (Boss Box, Silver)
Z10 = Deck("z10", "graduation-stage", "Zone 10: Graduation Stage (Dean Thudd Boss Box)")
Z10.add("Silver","gear","item","Dean Thudd's Valedictorian Cord (Gold)","Rope of Climbing","DMG 2024","Uncommon","Misc",
 M("60-ft rope, holds up to 3,000 lb. Magic action: command the free end to move toward a destination within 60 ft (10 ft now, 10 ft at the start of each of your turns), or to fasten, unfasten, knot, unknot or coil. Knotted: shortens to 50 ft, Advantage on climb checks. AC 20, HP 20, immune to Poison and Psychic, regains 1 HP per 5 min.","Magic action","60 ft",None,None,"permanent",None,"Destroyed at 0 HP.",3),
 "Dean Thudd's Valedictorian Cord, Rope of Climbing. Magic action: sixty foot rope moves, knots and fastens itself.",
 "He earned it and you took it, which is the same thing.",CI,300,12,"Pushed the Dean Into the Orchestra Pit and Called It Extra Credit Box","Pushed Dean Thudd into the orchestra pit",
 "Floor doc §6.7 trophy suggestion (Cord of Upward Mobility). Floor doc suggested Potion of Climbing; Uncommon Rope of Climbing keeps Silver value. Unique false: each boss-fighting crawler gets a Boss Box. DMG/SRD 2024 text per mirror 2026-10-04.",boxtypes=["Boss"])
Z10.add("Silver","gear","item","Podium Leg, Bolted Once, Now Stuck Forever","Immovable Rod","SRD 5.2","Uncommon","Misc",
 M("Utilize action: press the button; the rod becomes fixed in place and holds up to 8,000 lb. Utilize again to release. Moving a fixed rod up to 10 ft needs a DC 30 Strength (Athletics) check. 2 lb.","Utilize action",None,None,"Str (Athletics) DC 30 to move","until released",None,"Over 8,000 lb deactivates it.",2),
 "Podium Leg, Immovable Rod. Utilize to fix it in place; holds eight thousand pounds.",
 "A sturdy piece of the dean's authority.",CI,300,12,"Accepted a Diploma and Got Hugged So Hard Your Spine Filed for Divorce Box","Survived Dean Thudd's hug",
 "Boss trophy. Floor doc §6.7 box-name example.",boxtypes=["Boss"])
Z10.add("Silver","consumable","consumable","Dean's Emergency Flask (Courtesy of the Faculty)","Potion of Healing (greater)","SRD 5.2","Uncommon","Consumables",
 M("Bonus Action: drink it, or give it to a creature within 5 ft; the drinker regains 4d4+4 HP. One use.","Bonus Action","5 ft (to give)",None,None,"instant",U1,"Consumed.",0.5),
 "Dean's Emergency Flask, Potion of Greater Healing. Bonus Action: regain four d four plus four hit points.",
 "He was saving it. Not any more.",CI,150,16,"Dodged the Group Photo and Ruined the Yearbook Box","Avoided the Dean's final attack",
 "Boss Box consumable pull.",boxtypes=["Boss"],ledger_ids="I-009; L-005 (Boss Box scales with boss)")
Z10.add("Silver","credits","credits","Alumni Fund Check (Cleared, Unfortunately)","Credits (Silver pull, 2d6 x 25)","HOUSE","n/a","Credits",
 M("Adds 2d6 x 25 credits (50-300) to your balance when the box is opened. Roll at draw time. No weight.","none",None,None,None,"instant",None,"Added when the box is opened.",0),
 "Alumni Fund Check. Silver credits: two d six times twenty-five, added to your balance.",
 "Every graduate paid in. Not one got out.",CI,175,14,"Talked the Final Exam Into Early Retirement and He Took the Fruit Plate With Him Box","Talked Dean Thudd into early retirement",
 "Separate from Thudd's corpse cache (2d6x10).",grant=credits_grant("2d6x25"),boxtypes=["Boss"],ledger_ids="L-005")

# ------------------------------------------------------------------ STORY BOXES (Legendary one-offs, hand-pick only)
# Spec 2.8 (rules/40 v0.1.3) + Caleb's approval of the narrow Story Box exception (2026-10-04).
# Card text is Syndicate's final JSON from rules/42-house-items-f01.md v0.2 sections 6.5-6.9, copied verbatim (only f01-any-0057
# action_cost differs: "Action: 30 seconds of focus (outside combat)" per Caleb's/Syndicate's instruction to Lore).
# Rules: GM-triggered, draw_weight 0, bound false (Caleb's ruling 2026-10-04: lootable, transferable, sellable), credit_value 0, story_value 20,000-250,000, cap one per table per floor.
# The Enhanced Pet Biscuit stays as f01-any-0055 in the orientation-pit deck (not duplicated here).
S = Deck("any", "story-boxes", "Floor 1: Story Boxes (Legendary one-offs, GM hand-pick only)", version="0.1.1")
STORY_CARDS = [
{'id': 'f01-any-0056',
 'floor': 1,
 'zone': 'any',
 'tier': 'Legendary',
 'box_types': ['any'],
 'pull_type': 'weird',
 'kind': 'item',
 'reskin_name': 'Tiara of Bloody Succession (Fits Any Head, Fits Any Paws)',
 'real_5e_name': 'Circlet of Quick Wits (house: Fleeting +Int crown)',
 'source_5e': 'HOUSE',
 'rarity': 'Uncommon',
 'attunement': None,
 'category': 'Misc',
 'plain_mechanics': {'text': 'Worn on the head by one creature (no attunement); it resizes to fit any quadruped or biped. While worn: +2 '
                             'bonus to Intelligence checks, and Advantage on your first Charisma (Persuasion) check against each creature '
                             'that has not met you. Once per turn, right after you hit with an attack, roll a d20: on 18 or higher the '
                             'target makes a DC 12 Constitution save or has the Poisoned condition until the end of its next turn. '
                             "Fleeting: if it leaves the wearer's head for any reason it crumbles and the GM places it elsewhere on this "
                             'floor.',
                     'action_cost': 'None (passive)',
                     'range': 'Self',
                     'damage': 'Poisoned (Sepsis rider)',
                     'save_dc': 'Con DC 12 (Sepsis rider)',
                     'duration': 'while worn',
                     'uses': None,
                     'limits': 'The +2 applies to Intelligence checks only, not saves, attack rolls or spell DCs. The Poisoned rider is '
                               'once per turn and does nothing to creatures immune to Poisoned. One crown exists at a time. It gives a '
                               'non-sapient wearer no speech. Fleeting: the GM sets the new place within fair reach of the party, with a '
                               'clue; the owner puts it on again; if you go downstairs wearing it, it goes with you. Awarded to the Crawler '
                               'whose companion earned it; not bound (it can be traded, sold or looted from a corpse like any item); the owner decides who wears it. Story hook only: wearing it '
                               'enters the wearer in the Blood Sultanate line of succession (a Floor 9 thread; no effect on Floors 1-2).',
                     'weight_lb': 0.5},
 'spoken_line': 'Tiara of Bloody Succession, Circlet of Quick Wits. Plus two to Intelligence checks, fits any quadruped, and vanishes if '
                'removed.',
 'snark_line': 'Every four-legged Crawler deserves a crown, and this one comes with a grudge.',
 'reward': 'Tiara of Bloody Succession, Circlet of Quick Wits. Plus two to Intelligence checks, fits any quadruped, and vanishes if '
           'removed.',
 'canon_status': 'CANON-INSPIRED',
 'credit_value': 0,
 'draw_weight': 0,
 'unique': True,
 'tailor_tags': ['pets'],
 'exclusive_to': None,
 'grant': None,
 'ledger': {'type': 'item',
            'text': 'item +1 Legendary Story Box: Tiara of Bloody Succession (Circlet of Quick Wits (house)) (story value 60000, not bound)'},
 'box_name': 'Quadruped Box',
 'deed': 'First quadruped companion into the Crawl',
 'notes': 'HOUSE design (rules/42-house-items-f01.md §6.5). GM-triggered Story Box (spec 2.8): hand-pick only (weight 0), not bound (lootable, tradeable, sellable), never '
          'drawn at random. Cap one per table per floor (log an override to exceed). LEDGER: L-001, A-165, I-014, M-231, M-232. '
          'trigger_deed: the first quadruped companion (any four-legged creature, not only a cat) enters the Crawl with a Crawler at the '
          'table, judged by the GM. power_note: +2 on Intelligence checks only, no AC, attack, save or damage bonus, and a 15 percent '
          'Poisoned rider that lasts one turn, so armor, weapons and Silver loot stay the main upgrades. Canon: box and deed are canon '
          '(A-165, VERIFIED B1 ch7; any quadruped is a HOUSE table rule); canon contents were the Crown of the Sepsis Whore; numbers here '
          'are HOUSE.',
 'story_value': 60000,
 'bound': False},
{'id': 'f01-any-0057',
 'floor': 1,
 'zone': 'any',
 'tier': 'Legendary',
 'box_types': ['any'],
 'pull_type': 'weird',
 'kind': 'item',
 'reskin_name': 'Grudge Ring (Green Glass, Red Stone)',
 'real_5e_name': 'Ring of Divine Suffering (house: Marked for Death ring)',
 'source_5e': 'HOUSE',
 'rarity': 'Rare',
 'attunement': 'yes',
 'category': 'Misc',
 'plain_mechanics': {'text': "Requires attunement and the table's session-zero opt-in. Once per Long Rest, spend 30 seconds focusing (so "
                             'outside combat) to mark one hostile non-Crawler creature you can see within 60 ft that is at full hit points '
                             'and that the GM agrees is a real threat (no vermin, no noncombatants). One mark at a time. While the mark '
                             'lives you cannot regain hit points by any means (temporary hit points and stabilizing still work). When it '
                             'dies, from any cause, you regain all your hit points and gain Heroic Inspiration.',
                     'action_cost': 'Action: 30 seconds of focus (outside combat)',
                     'range': '60 ft',
                     'damage': 'Mark (no damage)',
                     'save_dc': 'None',
                     'duration': 'until the mark dies, you take the ring off, or you leave the floor',
                     'uses': {'max': 1, 'recharge': 'long rest'},
                     'limits': 'Session-zero opt-in required (the canon ring is tied to a family killing; offer the estranged-rival '
                               'reframe instead of kin). Never marks Crawlers unless every player opted into PvP at session zero. No '
                               'healing of any kind while a mark is active, including potions, spells, Hit Point Dice, rests and the '
                               'Stairwell Checkpoint. You may take the ring off at any time: the mark ends, you get no reward, and the use '
                               'is spent until your next Long Rest. The mark ends with no reward if you leave the floor. If you already '
                               'hold Heroic Inspiration, give the new one to another Crawler (core rule). Counts toward the three '
                               'attunement slots. Not bound: it can be traded, sold or looted from a corpse like any item. Hunters of Floor 6 will target the wearer (GM hook, no effect '
                               'on Floors 1-2). No permanent stat bonus.',
                     'weight_lb': 0},
 'spoken_line': 'Grudge Ring, Ring of Divine Suffering. Once per long rest, mark one foe: no healing for you until it dies, then full '
                'health and Inspiration. Opt-in only.',
 'snark_line': 'It sounds scary because it is, and it does not care who you were angry at.',
 'reward': 'Grudge Ring, Ring of Divine Suffering. Once per long rest, mark one foe: no healing for you until it dies, then full health '
           'and Inspiration. Opt-in only.',
 'canon_status': 'CANON-INSPIRED',
 'credit_value': 0,
 'draw_weight': 0,
 'unique': True,
 'tailor_tags': [],
 'exclusive_to': None,
 'grant': None,
 'ledger': {'type': 'item',
            'text': 'item +1 Legendary Story Box: Grudge Ring (Ring of Divine Suffering (house)) (story value 80000, not bound)'},
 'box_name': "That's the Spirit! Box",
 'deed': 'Entered the Crawl fighting kin',
 'notes': 'HOUSE design (rules/42-house-items-f01.md §6.6). GM-triggered Story Box (spec 2.8): hand-pick only (weight 0), not bound (lootable, tradeable, sellable), never '
          'drawn at random. Cap one per table per floor (log an override to exceed). LEDGER: L-001, A-167, I-025, S-011, M-233, X-054. '
          'trigger_deed: a Crawler enters the Crawl in a fight with a relative, or with an NPC they treat as kin (an estranged rival is '
          "fine), set up at session zero with everyone's opt-in. Do NOT run it without the opt-in: the canon ring is tied to a killing "
          'within a family. power_note: double-edged and Rare, so it is a risk trade (no healing until the mark dies, one full heal plus '
          'Inspiration per Long Rest at most), not a free upgrade. Canon: box and deed canon (A-167, VERIFIED B3 ch19; Legendary vs '
          'Platinum tier conflict X-054, Legendary preferred); canon ring is +5 percent all stats plus the Marked for Death skill (I-025, '
          'S-011); numbers here are HOUSE. Not the same item as the core 6.7 Marked for Death Band (revival curse).',
 'story_value': 80000,
 'bound': False},
{'id': 'f01-any-0058',
 'floor': 1,
 'zone': 'any',
 'tier': 'Legendary',
 'box_types': ['any'],
 'pull_type': 'weird',
 'kind': 'item',
 'reskin_name': 'Olive Branch Lanyard (Laminated, Nobody Got Hurt)',
 'real_5e_name': 'Olive Branch Lanyard (house: redirect charm)',
 'source_5e': 'HOUSE',
 'rarity': 'Uncommon',
 'attunement': None,
 'category': 'Misc',
 'plain_mechanics': {'text': 'Reaction, once per Long Rest: when a creature you can see, and have not damaged, is about to make an attack '
                             'roll against you, it makes a DC 13 Wisdom save. On a failure it must pick a different target within its '
                             'reach or range, or lose the attack.',
                     'action_cost': 'Reaction',
                     'range': 'Sight',
                     'damage': 'None',
                     'save_dc': 'Wis DC 13',
                     'duration': 'instant',
                     'uses': {'max': 1, 'recharge': 'long rest'},
                     'limits': 'Only works against a creature you have not damaged. One use per Long Rest. It does nothing to a creature '
                               'that is immune to the Charmed condition (GM call) and does not stop area effects. The attacker chooses the '
                               'new target, which may be one of your allies. Not bound: it can be traded, sold or looted from a corpse like any item.',
                     'weight_lb': 0},
 'spoken_line': 'Olive Branch Lanyard. Once per long rest, a creature you have not hurt that attacks you must pick another target or lose '
                'its attack.',
 'snark_line': 'Proof that you did it all without hurting anyone, laminated for your convenience.',
 'reward': 'Olive Branch Lanyard. Once per long rest, a creature you have not hurt that attacks you must pick another target or lose its '
           'attack.',
 'canon_status': 'CANON-INSPIRED',
 'credit_value': 0,
 'draw_weight': 0,
 'unique': True,
 'tailor_tags': ['pacifist'],
 'exclusive_to': None,
 'grant': None,
 'ledger': {'type': 'item', 'text': 'item +1 Legendary Story Box: Olive Branch Lanyard (story value 30000, not bound)'},
 'box_name': "Pacifist's Box",
 'deed': 'Left Floor 1 without a single kill',
 'notes': 'HOUSE design (rules/42-house-items-f01.md §6.7). GM-triggered Story Box (spec 2.8): hand-pick only (weight 0), not bound (lootable, tradeable, sellable), never '
          'drawn at random. Cap one per table per floor (log an override to exceed). LEDGER: L-001, L-B43, A-092. trigger_deed: the '
          'Crawler (or the whole party) reaches the Floor 1 stairwell without having killed anything; traps, allies and the environment '
          'killing do not count against them, the GM judges. If the whole party qualifies there is still one Lanyard: the party names its '
          'owner. power_note: one defensive redirect per Long Rest that only works on foes you have not hurt, with no damage, so armor, '
          "shields and healing stay the main defenses. Canon: Pacifist's Box is canon (L-B43, A-092) but the Legendary Pacifist's Boxes "
          'went to Meadow Lark on Floor 3 (B2 ch8), so this is a HOUSE Floor 1 version. Numbers HOUSE.',
 'story_value': 30000,
 'bound': False},
{'id': 'f01-any-0059',
 'floor': 1,
 'zone': 'any',
 'tier': 'Legendary',
 'box_types': ['any'],
 'pull_type': 'weird',
 'kind': 'item',
 'reskin_name': 'Porkchop Express Wheel-Hub Maul',
 'real_5e_name': '+1 Maul (house: Rolling Ruin)',
 'source_5e': 'HOUSE',
 'rarity': 'Uncommon',
 'attunement': None,
 'category': 'Weapons',
 'plain_mechanics': {'text': 'A +1 maul: +1 bonus to attack and damage rolls (Maul: 2d6 Bludgeoning, Heavy, Two-Handed, Topple, 10 lb). '
                             'Once per short rest, when you hit with it, the target makes a DC 12 Strength save or is pushed 10 ft and has '
                             'the Prone condition.',
                     'action_cost': 'Action',
                     'range': 'Melee',
                     'damage': '2d6+1 Bludgeoning',
                     'save_dc': 'Str DC 12 (push and Prone)',
                     'duration': 'instant',
                     'uses': {'max': 1, 'recharge': 'short rest'},
                     'limits': 'The push and Prone work only once per short rest. Heavy: Small creatures have Disadvantage on attack rolls '
                               'with it. Huge or larger creatures are unaffected by the push and Prone. It is a Martial weapon: without '
                               'proficiency you add no Proficiency Bonus. If you also have the Topple mastery, use one effect per hit, not '
                               'both. Awarded to the Crawler the party names; not bound (it can be traded, sold or looted from a corpse like any item).',
                     'weight_lb': 10},
 'spoken_line': 'Porkchop Express Wheel-Hub Maul, plus one maul. Once per short rest, a hit pushes ten feet and knocks the target prone.',
 'snark_line': 'Salvaged from something that rolled over a lot of people, and now it is your turn.',
 'reward': 'Porkchop Express Wheel-Hub Maul, plus one maul. Once per short rest, a hit pushes ten feet and knocks the target prone.',
 'canon_status': 'CANON-INSPIRED',
 'credit_value': 0,
 'draw_weight': 0,
 'unique': True,
 'tailor_tags': ['boss'],
 'exclusive_to': None,
 'grant': None,
 'ledger': {'type': 'item', 'text': 'item +1 Legendary Story Box: Porkchop Express Wheel-Hub Maul (story value 35000, not bound)'},
 'box_name': 'Stopped the Porkchop Express Box',
 'deed': 'First party to take down a Floor 1 Borough Boss',
 'notes': 'HOUSE design (rules/42-house-items-f01.md §6.8). GM-triggered Story Box (spec 2.8): hand-pick only (weight 0), not bound (lootable, tradeable, sellable), never '
          'drawn at random. Cap one per table per floor (log an override to exceed). LEDGER: L-001, A-168, A-173, B-003. trigger_deed: the '
          'first party at the table to defeat a Floor 1 Borough Boss (Ball of Swine or any other the GM names; in the F1 module this is '
          'Dean Thudd unless the GM names another), judged by the GM. power_note: a +1 weapon (Uncommon) with one short-rest shove, no new '
          'damage dice, so armor and Silver Boss Box loot stay relevant. Canon: the canon reward for the first Borough Boss is a Platinum '
          'Weapon Box (A-168, VERIFIED B1 ch14), not Legendary, so Legendary is an approved HOUSE upgrade for a table-first; Ball of Swine '
          'is B-003 (level 15 in the books). Numbers HOUSE.',
 'story_value': 35000,
 'bound': False},
{'id': 'f01-any-0060',
 'floor': 1,
 'zone': 'any',
 'tier': 'Legendary',
 'box_types': ['any'],
 'pull_type': 'weird',
 'kind': 'item',
 'reskin_name': 'Pet Biscuit Crate, Industrial (500)',
 'real_5e_name': 'Pet Biscuit, plain (house: x500 supply)',
 'source_5e': 'HOUSE',
 'rarity': 'Common',
 'attunement': None,
 'category': 'Consumables',
 'plain_mechanics': {'text': 'Utilize action, within 5 ft: feed one plain Pet Biscuit to a willing pet or companion Beast; it regains 1d4 '
                             'hit points and is calm for 1 minute (it does not flee in panic, and you succeed on any Wisdom (Animal '
                             'Handling) check to settle it). A pet gets this benefit from at most 3 biscuits per Long Rest. The crate '
                             'holds 500 biscuits.',
                     'action_cost': 'Utilize action',
                     'range': '5 ft',
                     'damage': 'Heals 1d4',
                     'save_dc': 'None',
                     'duration': 'instant (calm lasts 1 minute)',
                     'uses': {'max': 500, 'recharge': 'none'},
                     'limits': 'Plain biscuits only: not Enhanced, no transformation, no effect on a Crawler (including a pet already made '
                               "a Crawler). Beyond 3 biscuits per pet per Long Rest a biscuit is just a snack. It also covers the pet's "
                               'ordinary food. 25 lb. Not bound: it can be traded, sold or looted from a corpse like any item. Awarded together with f01-any-0055 as one Story Box.',
                     'weight_lb': 25},
 'spoken_line': 'Pet Biscuit Crate. Five hundred plain biscuits: feed one to a pet to heal one d four and calm it, up to three per pet per '
                'long rest.',
 'snark_line': 'Enough kibble to feed the entire Orientation Pit, if the Orientation Pit were a good boy.',
 'reward': 'Pet Biscuit Crate. Five hundred plain biscuits: feed one to a pet to heal one d four and calm it, up to three per pet per long '
           'rest.',
 'canon_status': 'CANON-INSPIRED',
 'credit_value': 0,
 'draw_weight': 0,
 'unique': True,
 'tailor_tags': ['pets'],
 'exclusive_to': None,
 'grant': None,
 'ledger': {'type': 'item', 'text': 'item +1 Legendary Story Box: Pet Biscuit Crate (story value 20000, not bound)'},
 'box_name': 'Pet Box',
 'deed': 'Brought a pet into the Crawl',
 'notes': 'HOUSE design (rules/42-house-items-f01.md §6.9). GM-triggered Story Box (spec 2.8): hand-pick only (weight 0), not bound (lootable, tradeable, sellable), never '
          'drawn at random. LEDGER: L-001, L-020, I-007, M-228. trigger_deed: same deed as f01-any-0055 (the Enhanced Pet Biscuit): the '
          'first Crawler at the table to bring a pet into the Crawl. It is the second pull of the same Legendary Pet Box, so it is awarded '
          "together with f01-any-0055 as ONE Story Box; log this card with the override reason 'same box' under the one-per-floor cap. "
          'power_note: Common-level pet supply, 1d4 healing capped at 3 per pet per Long Rest, no combat power. Canon: the Legendary Pet '
          'Box held Pet Biscuit x500 plus the Enhanced Pet Biscuit (M-228, VERIFIED B1 ch5); healing and calm numbers are HOUSE.',
 'story_value': 20000,
 'bound': False},
# Syndicate's rules/45 section 4.4 example cards 0061-0065 (Caleb approved them 2026-10-04: 'if Lore thinks they are good'); reviewed and adjusted in _retune() below.
{'id': 'f01-any-0061',
 'floor': 1,
 'zone': 'any',
 'tier': 'Legendary',
 'box_types': ['any'],
 'pull_type': 'weird',
 'kind': 'item',
 'reskin_name': 'Little Crown, Four-Paw Fit',
 'real_5e_name': 'Circlet of the Crowd (house: quadruped charm crown)',
 'source_5e': 'HOUSE',
 'rarity': 'Uncommon',
 'attunement': None,
 'category': 'Misc',
 'plain_mechanics': {'text': 'Worn by one quadruped companion (resizes to fit; no attunement). Once per long rest, when the wearer or its '
                             'owner meets a creature that has not met either of them, one of the two may make one Charisma (Persuasion or '
                             'Performance) check with Advantage; say so before rolling. Dormant part: at owner level 3 it gains a second '
                             'use per long rest. No effect on attacks, saves, AC or damage.',
                     'action_cost': 'none',
                     'range': '30 ft (wearer and owner within 30 ft of each other)',
                     'damage': None,
                     'save_dc': None,
                     'duration': 'one check',
                     'uses': {'max': 1, 'recharge': 'long rest'},
                     'limits': 'Quadruped wearer only. Second use stays locked until the owner is level 3. If the companion dies, the '
                               'crown is ordinary loot.',
                     'weight_lb': 0.5},
 'spoken_line': 'Little Crown, Circlet of the Crowd. Once per rest, the wearer or its owner rolls one Charisma check with Advantage.',
 'snark_line': 'Four legs, one crown, zero understanding of taxes. The audience has already voted.',
 'reward': 'Little Crown, Circlet of the Crowd. Once per rest, the wearer or its owner rolls one Charisma check with Advantage.',
 'canon_status': 'CANON-INSPIRED',
 'credit_value': 0,
 'story_value': 30000,
 'sale_value': 250,
 'bound': False,
 'draw_weight': 0,
 'unique': True,
 'tailor_tags': ['pets'],
 'exclusive_to': None,
 'grant': None,
 'ledger': {'type': 'item', 'text': 'item +1 Legendary Story Box: Little Crown, Four-Paw Fit (story value 30000)'},
 'box_name': 'Four Paws Over the Threshold Box',
 'deed': 'Brought a four-legged companion into the Crawl and got it through the first fight alive',
 'notes': 'Canon basis: ledger L-001, A-165 (Legendary Quadruped Box, first cat in; Donut), I-014. Pattern B (Seed). trigger_deed: first '
          'quadruped companion (any four-legged creature, not only a cat) that enters the Crawl with a Crawler at the table AND gets '
          'through a first fight alive because of a risk its owner or the animal took; GM judged. power_note: Utility, rung 1 now; rung 2 '
          'later by named step only (level 3: second use). One social Advantage per rest, no combat numbers. Hook: the audience adores the '
          'wearer, and anything hostile that likes crowns can notice it. Recipient: the owner Crawler is the ledger name; the item sits on '
          'the companion.'},
{'id': 'f01-any-0062',
 'floor': 1,
 'zone': 'any',
 'tier': 'Legendary',
 'box_types': ['any'],
 'pull_type': 'weird',
 'kind': 'item',
 'reskin_name': 'Grudge Pin, Enamel (Family Reunion 2019)',
 'real_5e_name': 'Pin of Settled Scores (house: grudge charm)',
 'source_5e': 'HOUSE',
 'rarity': 'Common',
 'attunement': None,
 'category': 'Misc',
 'plain_mechanics': {'text': 'Pin worn on clothing (no attunement). When you earn it, name one fictional rival from your backstory (never '
                             'a real person; the GM approves the name). While you can see that rival or anyone acting for them, you have '
                             'Advantage on saving throws against being Frightened. The first time the table plays out that rival being '
                             'beaten without being killed, spared or forgiven, you gain Heroic Inspiration, once ever; after that the pin '
                             'is a keepsake with no effect.',
                     'action_cost': 'none',
                     'range': 'self',
                     'damage': None,
                     'save_dc': None,
                     'duration': 'while the rival is in view',
                     'uses': {'max': 1, 'recharge': 'none'},
                     'limits': 'PvP never counts and the rival is never another Crawler. The GM may swap the rival for a different '
                               'fictional one at any time, without giving a reason. The Inspiration is a one-time payout, paid once ever '
                               'to the Crawler who earned the deed; if the pin changes hands, the new holder keeps only the fear-save edge '
                               'against that rival.',
                     'weight_lb': 0},
 'spoken_line': 'Grudge Pin, Pin of Settled Scores. Advantage on fear saves near your rival, and Inspiration when the score is settled.',
 'snark_line': 'Nothing says family like a signed waiver. The audience is eating this up with a spoon.',
 'reward': 'Grudge Pin, Pin of Settled Scores. Advantage on fear saves near your rival, and Inspiration when the score is settled.',
 'canon_status': 'CANON-INSPIRED',
 'credit_value': 0,
 'story_value': 25000,
 'sale_value': 250,
 'bound': False,
 'draw_weight': 0,
 'unique': True,
 'tailor_tags': ['rivals'],
 'exclusive_to': None,
 'grant': None,
 'ledger': {'type': 'item', 'text': 'item +1 Legendary Story Box: Grudge Pin, Enamel (story value 25000)'},
 'box_name': 'Family Reunion, Now Streaming Box',
 'deed': 'Faced a fictional rival in the first fight of the Crawl and settled the score on camera',
 'notes': "Canon basis: ledger A-167 (Legendary That's the Spirit! Box, entering while fighting a family member; Frank Q), I-025. Content: "
          'HOUSE reframe, opt-in at session zero, a fictional rival NPC, no killing, no PvP, nothing cursed. Pattern A (Echo). '
          'trigger_deed: the Crawler enters or begins Floor 1 in a live fight with an opted-in fictional rival from the backstory and '
          'resolves it without killing in a way the table remembers; never staged by the GM, never PvP. power_note: Story plus one small '
          'save edge (rung 1); the Inspiration is a single one-time payout and then the pin goes inert. Hook: the rival now knows the '
          'Crawler by name.'},
{'id': 'f01-any-0063',
 'floor': 1,
 'zone': 'any',
 'tier': 'Legendary',
 'box_types': ['any'],
 'pull_type': 'weird',
 'kind': 'consumable',
 'reskin_name': 'Laminated Truce Chit (Do Not Fold)',
 'real_5e_name': 'Truce Chit (house: one-shot parley)',
 'source_5e': 'HOUSE',
 'rarity': 'Uncommon',
 'attunement': None,
 'category': 'Consumables',
 'plain_mechanics': {'text': 'Utilize action, once: hold it up to one creature you can see within 30 ft that has Intelligence 6 or higher, '
                             'is hostile, and has not yet attacked this scene. It must hear you out: for 1 minute it will not attack you '
                             'or your allies and will talk if it can. This ends at once if you or an ally hurts or threatens it. The chit '
                             'is spent.',
                     'action_cost': 'Utilize action',
                     'range': '30 ft',
                     'damage': None,
                     'save_dc': None,
                     'duration': '1 minute',
                     'uses': {'max': 1, 'recharge': 'none'},
                     'limits': 'Not usable on a floor boss, on a creature already in a fight with you, or on anything with Intelligence 5 '
                               'or lower. It buys a conversation, not a win: the usual checks still apply to what is said.',
                     'weight_lb': 0},
 'spoken_line': 'Laminated Truce Chit, a house parley token. One use: one smart hostile creature must hear you out for one minute.',
 'snark_line': "Valid for one conversation. Void if you say 'but hear me out' twice.",
 'reward': 'Laminated Truce Chit, a house parley token. One use: one smart hostile creature must hear you out for one minute.',
 'canon_status': 'HOUSE',
 'credit_value': 0,
 'story_value': 20000,
 'sale_value': 250,
 'bound': False,
 'draw_weight': 0,
 'unique': True,
 'tailor_tags': [],
 'exclusive_to': None,
 'grant': None,
 'ledger': {'type': 'item', 'text': 'item +1 Legendary Story Box: Laminated Truce Chit (story value 20000)'},
 'box_name': 'Talked It Into Quitting Box',
 'deed': 'Talked a named hostile out of a fight, with the whole table watching, using its own rules against it',
 'notes': 'Pattern C (Keystone). trigger_deed: a named Floor 1 hostile (not a floor boss) that was about to fight stands down because of '
          "the Crawler's words and plan, first time at the table, risk real (low HP, no escape), witnessed. power_note: Story keystone, "
          'single use, no numbers beyond 1 minute; floor bosses excluded. Hook: the creature remembers who talked to it. Tradeable '
          'consumable; if unused it carries to the next floor.'},
{'id': 'f01-any-0064',
 'floor': 1,
 'zone': 'any',
 'tier': 'Legendary',
 'box_types': ['any'],
 'pull_type': 'weird',
 'kind': 'item',
 'reskin_name': 'Annotated Floor Plan (Coffee Ring Included)',
 'real_5e_name': 'Plan of Unfair Advantage (house: environment charm)',
 'source_5e': 'HOUSE',
 'rarity': 'Uncommon',
 'attunement': None,
 'category': 'Misc',
 'plain_mechanics': {'text': 'Folded plan carried in your System Inventory (no attunement). Once per long rest, when you use a Utilize '
                             'action on part of the room (a trap, door, shelf, light, vending machine) against a creature, that creature '
                             'has Disadvantage on the first saving throw it makes against that effect. The effect must be something the '
                             'room already offers; the plan adds no damage and no new effect.',
                     'action_cost': 'None (passive)',
                     'range': 'as the Utilize action',
                     'damage': None,
                     'save_dc': None,
                     'duration': 'one saving throw',
                     'uses': {'max': 1, 'recharge': 'long rest'},
                     'limits': 'One use per long rest, never on a floor boss. The GM decides what the room offers.',
                     'weight_lb': 0},
 'spoken_line': 'Annotated Floor Plan, Plan of Unfair Advantage. Once per rest, a room trick you use gives its target Disadvantage on its '
                'first save.',
 'snark_line': 'Every coffee ring marks a trap that worked. The cleaning staff has stopped asking.',
 'reward': 'Annotated Floor Plan, Plan of Unfair Advantage. Once per rest, a room trick you use gives its target Disadvantage on its first '
           'save.',
 'canon_status': 'HOUSE',
 'credit_value': 0,
 'story_value': 30000,
 'sale_value': 500,
 'bound': False,
 'draw_weight': 0,
 'unique': True,
 'tailor_tags': ['traps'],
 'exclusive_to': None,
 'grant': None,
 'ledger': {'type': 'item', 'text': 'item +1 Legendary Story Box: Annotated Floor Plan (story value 30000)'},
 'box_name': 'Let the Room Do It Box',
 'deed': 'Beat a named Floor 1 hostile using only the room, never raising a weapon',
 'notes': 'Pattern A (Echo). trigger_deed: first Crawler at the table to defeat or drive off a named hostile using only the environment, '
          'without a weapon attack or spell of their own, at real risk. power_note: Capped, rung 2: Disadvantage on one save per long '
          'rest, no damage dice, no DC, no new action. Hook: the room is now a suspect; the System starts moving the furniture.'},
{'id': 'f01-any-0065',
 'floor': 1,
 'zone': 'any',
 'tier': 'Legendary',
 'box_types': ['any'],
 'pull_type': 'weird',
 'kind': 'item',
 'reskin_name': 'Group Photo, Mid-Handshake (Framed)',
 'real_5e_name': 'Keepsake of the Four (house: table-deed trophy)',
 'source_5e': 'HOUSE',
 'rarity': 'Common',
 'attunement': None,
 'category': 'Misc',
 'plain_mechanics': {'text': 'Framed photo held by one Crawler (the table picks the holder; the GM default is a Crawler without a Story '
                             'Box yet). While all four pictured Crawlers are alive and within 1 mile of each other, each of them always '
                             'knows the compass direction to the others. Once per floor, the holder may ask the System to replay the '
                             'moment in the photo: a free recap of who stood where when the plan began. No combat effect.',
                     'action_cost': 'none',
                     'range': '1 mile',
                     'damage': None,
                     'save_dc': None,
                     'duration': 'while all four are alive',
                     'uses': {'max': 1, 'recharge': 'none'},
                     'limits': 'A dead pictured Crawler shows in grey and drops out of the direction sense. A replacement Crawler is not '
                               'in the photo. Story and navigation only.',
                     'weight_lb': 1},
 'spoken_line': 'Group Photo, Keepsake of the Four. While all four of you live, each always knows the direction to the others.',
 'snark_line': 'Everybody smile. Production wants this on the poster. Production has already chosen the poster.',
 'reward': 'Group Photo, Keepsake of the Four. While all four of you live, each always knows the direction to the others.',
 'canon_status': 'HOUSE',
 'credit_value': 0,
 'story_value': 20000,
 'sale_value': 100,
 'bound': False,
 'draw_weight': 0,
 'unique': True,
 'tailor_tags': [],
 'exclusive_to': None,
 'grant': None,
 'ledger': {'type': 'item', 'text': 'item +1 Legendary Story Box: Group Photo, Mid-Handshake (story value 20000)'},
 'box_name': 'Four-Way Handshake Box',
 'deed': 'All four Crawlers carried out one plan, each with a different job, and it worked',
 'notes': 'Table deed (rules/45 section 6.2): counts as the one Story Box deed of every Crawler named in the deed line; the GM names all '
          'four in --witness and logs the other three as sharing it. Pattern: Trophy (rung 0 plus a navigation perk). trigger_deed: all '
          'four Crawlers each did a distinct, necessary part of one improvised plan against something above their weight, unscripted, with '
          'real risk. power_note: Story and navigation only, no combat numbers. Hook: if one Crawler dies, the photo greys them out where '
          'everyone can see.'},
]
# Lore trims two spoken lines that were over the 25-word limit in rules/42 (spec 1.1); Syndicate to adopt.
_SPOKEN_FIX = {
    "f01-any-0057": "Grudge Ring, Ring of Divine Suffering. Once per long rest, mark a foe: no healing until it dies, then full health. Opt-in only.",
    "f01-any-0060": "Pet Biscuit Crate. Five hundred plain biscuits: one heals a pet one d four and calms it, three per pet per long rest.",
}
SALE_VALUE = {"f01-any-0056": 500, "f01-any-0057": 500, "f01-any-0058": 500, "f01-any-0059": 500, "f01-any-0060": 100, "f01-any-0061": 250, "f01-any-0062": 250, "f01-any-0063": 250, "f01-any-0064": 500, "f01-any-0065": 100}
def _swap_notes(c, trigger=None, power=None, canon_add=None):
    n = c["notes"]
    if trigger:
        n = re.sub(r"trigger_deed:.*?(?= power_note:)", "trigger_deed: " + trigger, n, count=1, flags=re.S)
    if power:
        n = re.sub(r"power_note:.*?(?= Canon:)", "power_note: " + power, n, count=1, flags=re.S)
    c["notes"] = n

def _retune(c):
    """Lore retune (2026-10-04) of the Story Box cards to the rules/45 power ladder; Caleb deferred item strength to Lore.
    Rung 2 = one small combat effect once per long rest; no always-on numeric bonus, no repeatable rider, DC <= 12, no permanent
    weapon bonus; strong parts are dormant with a named unlock (level 3 or Floor 3). Ids, story_value, sale_value, canon flavor kept."""
    i = c["id"]; pm = c["plain_mechanics"]
    if i == "f01-any-0056":
        c["real_5e_name"] = "Circlet of Quick Wits (house: quadruped Int crown)"
        pm.update({
            "text": "Worn on the head by one creature (no attunement); it resizes to fit any quadruped or biped. Once per long rest, the wearer may make one Intelligence check, or one Charisma (Persuasion) check against a creature that has not met the wearer, with Advantage; say so before rolling. Dormant until the wearer reaches level 3: the Sepsis rider. Once per long rest, right after you hit with an attack, the target makes a DC 12 Constitution saving throw or has the Poisoned condition until the end of its next turn.",
            "action_cost": "None (passive)", "range": "Self", "damage": "Poisoned (dormant Sepsis rider, level 3)",
            "save_dc": "Con DC 12 (dormant Sepsis rider, level 3)", "duration": "one check",
            "uses": {"max": 1, "recharge": "long rest"},
            "limits": "One Advantage per long rest and no always-on bonus. The Sepsis rider does nothing until the wearer is level 3 (a named step; the GM re-checks the budget then), is once per long rest, and does nothing to creatures immune to Poisoned. It gives a non-sapient wearer no speech. Whoever wears it uses it; a quadruped companion can wear it. Not bound: it can be traded, sold or looted from a corpse like any item. Story hook only: wearing it enters the wearer in the Blood Sultanate line of succession (a Floor 9 thread; no effect on Floors 1-2). Fleeting was removed (an item that vanishes when it leaves the head cannot be traded or looted)."})
        c["spoken_line"] = c["reward"] = "Tiara of Bloody Succession, Circlet of Quick Wits. Once per rest, Advantage on one Intelligence check. Fits any quadruped."
        _swap_notes(c, power="Utility, rung 2 (one Advantage per long rest on an Intelligence or first-meeting Persuasion check; no always-on bonus); the Poisoned rider (DC 12, once per long rest) is dormant until level 3. Hook: the Blood Sultanate succession thread (Floor 9). Armor, weapons and Silver loot stay the main upgrades.")
        c["notes"] += " RETUNED (Lore, rules/45 ladder): the always-on +2 to Intelligence checks, the every-turn Poisoned rider and the repeatable Persuasion Advantage were removed or limited to once per long rest; Fleeting was dropped because the item is now tradeable and lootable. DUPLICATE THEME: f01-any-0061 is also an A-165 quadruped crown; award only one of 0056 / 0061 for the first-quadruped deed (one Story Box per table per floor)."
    elif i == "f01-any-0057":
        pm.update({
            "text": "Once per long rest, spend 30 seconds of focus (outside combat) to mark one hostile non-Crawler creature you can see within 60 ft that the GM agrees is a real threat (a fictional rival fits; no vermin, no noncombatants). The mark lasts up to 1 hour. You have Advantage on the first attack roll you make against the marked creature, and the mark ends when you make it. Marking never requires or rewards a kill.",
            "action_cost": "Action: 30 seconds of focus (outside combat)", "range": "60 ft", "damage": "None (mark)", "save_dc": "None",
            "duration": "up to 1 hour or until your first attack on the mark",
            "uses": {"max": 1, "recharge": "long rest"},
            "limits": "One mark at a time, one Advantage per long rest. It never marks a Crawler (no PvP). It runs only with the table's session-zero opt-in: the rival is fictional, never a real person and never a child, and a killing blow is not a deed. No healing is blocked and no hit points or Inspiration are restored. Hunters of Floor 6 will target the wearer (GM hook, no effect on Floors 1-2). No permanent stat bonus. No attunement. Not bound: it can be traded, sold or looted from a corpse like any item."})
        c["rarity"] = "Uncommon"; c["attunement"] = None
        c["spoken_line"] = c["reward"] = "Grudge Ring, Ring of Divine Suffering. Once per long rest, mark one threat: your first attack on it has Advantage. Opt-in only."
        c["deed"] = "Entered the Crawl fighting a fictional rival"
        _swap_notes(c, trigger="a Crawler enters the Crawl in a live fight or confrontation with an opted-in fictional rival from their backstory, set up at session zero (no killing, no PvP; rules/45 section 2.4). Without the opt-in, do not run it.",
            power="Utility, rung 2 (one Advantage per long rest on the first attack against a marked threat); no healing block, no full heal. Hook: Hunters of Floor 6 (no effect on Floors 1-2). Armor, weapons and Silver loot stay the main upgrades.")
        c["notes"] += " RETUNED (Lore, rules/45 ladder and Caleb's rival rule): the no-healing curse, the full heal and Heroic Inspiration on the mark's death, the Rare label and attunement were removed; it is now Uncommon with no attunement, never marks Crawlers, and needs no kill. The earlier hold on this card is resolved. DUPLICATE THEME: f01-any-0062 is also an A-167 rival item; award only one of 0057 / 0062 for the rival deed (one Story Box per table per floor). Canon ring: +5 percent all stats plus Marked for Death (I-025); the stat bonus is not used."
    elif i == "f01-any-0058":
        pm["text"] = pm["text"].replace("DC 13", "DC 12"); pm["save_dc"] = "Wis DC 12"
        _swap_notes(c, power="one defensive redirect per Long Rest that only works on foes you have not hurt, DC 12 (the rung 2 cap), no damage, uses the Reaction you already have. Armor, shields and healing stay the main defenses.")
        c["notes"] += " RETUNED (Lore, rules/45 ladder): save DC lowered from 13 to 12 (rung 2 cap); the redirect is judged borderline rung 2 (a single attack, once per long rest). Syndicate may still rule it rung 1 or 2."
    elif i == "f01-any-0059":
        c["real_5e_name"] = "Maul (house: Rolling Ruin, +1 dormant until Floor 3)"
        pm.update({
            "text": "A Maul (2d6 Bludgeoning, Heavy, Two-Handed, Topple, 10 lb). Once per long rest, when you hit with it, the target makes a DC 12 Strength saving throw or is pushed 10 ft and has the Prone condition. Dormant until the party reaches Floor 3: it becomes a +1 maul (+1 bonus to attack and damage rolls).",
            "action_cost": "Action", "range": "Melee", "damage": "2d6 Bludgeoning",
            "save_dc": "Str DC 12 (push and Prone)", "duration": "instant",
            "uses": {"max": 1, "recharge": "long rest"},
            "limits": "The push and Prone work only once per long rest. Heavy: Small creatures have Disadvantage on attack rolls with it. Huge or larger creatures are unaffected by the push and Prone. It is a Martial weapon: without proficiency you add no Proficiency Bonus. If you also have the Topple mastery, use one effect per hit, not both. The +1 is dormant on Floors 1-2 (named step: Floor 3; the GM re-checks the budget then). Not bound: it can be traded, sold or looted from a corpse like any item."})
        c["spoken_line"] = c["reward"] = "Porkchop Express Wheel-Hub Maul. Once per long rest, a hit pushes ten feet and knocks the target prone. Plus one at Floor three."
        _swap_notes(c, power="a Maul with one Strength-save shove per long rest (DC 12, the rung 2 cap) and no new damage dice; the +1 is dormant until Floor 3. Armor, spells and the Silver Boss Box stay relevant.")
        c["notes"] += " RETUNED (Lore, rules/45 ladder): the permanent +1 to attack and damage is dormant until Floor 3 and the shove is once per long rest (was short rest)."
    elif i == "f01-any-0061":
        pm["limits"] = pm["limits"].replace("Bound to the companion; if the companion dies the System takes the crown back.", "Needs a quadruped wearer (a companion item still needs its companion); if the companion dies the crown does nothing until another quadruped wears it. Not bound: it can be traded, sold or looted from a corpse like any item.")
        c["notes"] += " REVIEW (Lore): limits no longer say the System takes the crown back (no repossession, rules/45 section 6.3). DUPLICATE THEME: same canon box and deed as f01-any-0056 (Quadruped Box, A-165); award only one of 0056 / 0061 (one Story Box per table per floor). Canon contents were the Crown of the Sepsis Whore (I-014); numbers are HOUSE."
    elif i == "f01-any-0062":
        pm["text"] = "Pin worn on clothing (no attunement). When you earn it, name one fictional rival or estranged relative from your backstory (never a real person, never a child; the GM approves the name). Once per long rest, when you must make a saving throw against being Frightened by that rival or anyone acting for them, you have Advantage on that save. The first time the table plays out that rival being beaten, spared or forgiven (never killed), you gain Heroic Inspiration, once ever; after that the pin has no Inspiration left."
        pm["uses"] = {"max": 1, "recharge": "long rest"}
        pm["duration"] = "one saving throw"
        pm["limits"] = "PvP never counts and the rival is never another Crawler. A killing blow is not a deed. The GM may swap the rival for a different fictional one at any time, without giving a reason. The Inspiration is a one-time payout that stays with the Crawler who earned it. Not bound: it can be traded, sold or looted from a corpse like any item (the new holder gets the save edge only, never a second Inspiration)."
        c["spoken_line"] = c["reward"] = "Grudge Pin, Pin of Settled Scores. Once per rest, Advantage on a fear save against your rival. Inspiration when the score is settled."
        _swap_notes(c, power="Story plus one save edge (rung 2: one Advantage per long rest, conditional on the rival); the Inspiration is a single one-time payout. Hook: the rival now knows the Crawler by name.")
        c["notes"] += " REVIEW (Lore): the always-on Advantage on fear saves near the rival (a permanent save edge) is now once per long rest; 'no killing' and 'never a child' added to match rules/45 section 2.4. DUPLICATE THEME: same canon box (A-167) and deed as f01-any-0057; award only one of 0057 / 0062 (one Story Box per table per floor)."
    elif i == "f01-any-0063":
        pm.update({
            "text": "Utilize action, once: hold it up to one named hostile creature you can see within 30 ft that has Intelligence 6 or higher and has not yet attacked this scene. It makes a DC 12 Wisdom saving throw. On a failure it must hear you out: for 1 minute it will not attack you or your allies and will talk if it can. On a success nothing happens (no truce). This ends at once if you or an ally hurts or threatens it. The chit is spent either way.",
            "save_dc": "Wis DC 12", "duration": "1 minute on a failed save",
            "limits": "Named hostiles only. Not usable on a floor boss, on a creature already in a fight with you, or on anything with Intelligence 5 or lower. A success means no truce. It buys a conversation, not a win: the usual checks still apply to what is said."})
        c["spoken_line"] = c["reward"] = "Laminated Truce Chit, a house parley token. One use: one smart named hostile must pass a Wisdom save or hear you out."
        _swap_notes(c, power="Story keystone, single use, one Wisdom save at DC 12 (the rung cap) and a 1-minute truce on a failure; floor bosses excluded. Hook: the creature remembers who talked to it.")
        c["notes"] += " REVIEW (Lore): the forced truce was replaced by a Wisdom saving throw at DC 12 (success = no truce) at Caleb's request, so it reads like SRD Charm / Command style effects; ladder-compliant (consumable, one use, floor bosses excluded)."
    elif i == "f01-any-0064":
        c["notes"] += " REVIEW (Lore): ladder-compliant rung 2 (one Disadvantage on one save per long rest; no DC). 5e wording checked: Utilize action and Disadvantage on a saving throw are SRD 5.2 terms."
    elif i == "f01-any-0065":
        c["real_5e_name"] = "Keepsake of the Pictured (house: table-deed trophy)"
        c["box_name"] = "Group Handshake Box"
        c["deed"] = "Every Crawler present carried out a distinct part of one plan, and it worked"
        pm.update({
            "text": "Framed photo held by one Crawler (the table picks the holder; the GM default is a Crawler without a Story Box yet). The pictured Crawlers are the Crawlers present when the deed is recorded. While every Crawler pictured is alive and within 1 mile of the others, each of them always knows the compass direction to the others. Once per floor, the holder may ask the System to replay the moment in the photo: a free recap of who stood where when the plan began. No combat effect.",
            "duration": "while every Crawler pictured is alive",
            "uses": {"max": 1, "recharge": "floor"}})
        c["spoken_line"] = c["reward"] = "Group Photo, Keepsake of the Pictured. While every Crawler pictured lives, each always knows the direction to the others."
        c["snark_line"] = "Everybody smile; Production has already chosen the poster."
        c["notes"] = c["notes"].replace("the GM names all four in --witness and logs the other three as sharing it", "the GM names every pictured Crawler in --witness and logs the others as sharing it")
        _swap_notes(c, trigger="every Crawler present (the Crawlers pictured when the deed is recorded) each did a distinct, necessary part of one improvised plan against something above their weight, unscripted, with real risk.")
        c["notes"] += " REVIEW (Lore): snark line trimmed to one sentence for deck_check; 'all four Crawlers' became 'every Crawler pictured' (the Crawlers present when the deed is recorded), so it works for a two-Crawler table; the once-per-floor replay now uses uses.recharge 'floor' (new value, added to deck_check; Syndicate to add 'floor' to the recharge list in rules/40 section 1.1)."

RECLAIM_NOTE = " Death before a saferoom (Caleb's 2026-10-04 ruling): an unopened Story Box is reclaimed if the Crawler dies before a saferoom, and the slot is freed (the one-per-floor cap no longer counts it; the GM may award a Story Box again). This replaces the older rule where the box stayed closed and the cap stayed used."
for _c in A.cards:
    if _c["id"] == "f01-any-0055":
        _c["notes"] += RECLAIM_NOTE
for _c in STORY_CARDS:
    _retune(_c)
    _c["notes"] += RECLAIM_NOTE
    _c["sale_value"] = SALE_VALUE[_c["id"]]
    _c["notes"] += " sale_value %d (System buyback at Floor-1 scale, multiplied by the sale floor's credits multiplier at runtime; independent of story_value, which is provenance only and never the buyback base)." % _c["sale_value"]
    _c["notes"] += " story_value is provenance (what the deed was worth to the Accountant), not a sale price; bound is false: the item can be looted, traded or sold like any item (Caleb's ruling 2026-10-04)."
    if _c["id"] in _SPOKEN_FIX:
        _c["spoken_line"] = _c["reward"] = _SPOKEN_FIX[_c["id"]]
    S.cards.append(_c)
    S.n = int(_c["id"].split("-")[-1])

STORY_DECK_NOTES = ("Story Boxes are hand-pick only (draw_weight 0) and GM-triggered for one named, one-time deed. Like every loot box, a Story Box can only be opened in a saferoom. "
    "The deed is recorded and announced at award; the box then waits unopened until the next saferoom. If the Crawler dies before that saferoom, the unopened box is reclaimed and the slot is freed (Caleb's 2026-10-04 ruling; the one-per-floor cap no longer counts it). Story Box items are NOT bound (bound is false): they can be looted from a corpse, traded or sold, "
    "as in canon. story_value is provenance for the Accountant, not a sale price; sale_value is the System buyback at Floor-1 scale (times the sale floor's multiplier); credit_value stays 0. Cap one per table per floor (log an override to exceed).")
DECKS = [A, Z3, Z6, Z9, Z10, S]
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    extra_by_deck = {A: {"needs_verify": NEEDS_VERIFY, "pacing": {
        "core_4_5_floors_1_2": "2-4 Bronze and 0-1 Silver per crawler per floor (core §4.5)",
        "floor_doc_8_2_note": "floors/f01/00-overview.md §8.2 separately caps achievement boxes at 2 per crawler (plus the Welcome Box); core §4.5 is the rule that wins (spec v0.1.1 §2.6).",
        "no_gold_or_higher": "Floor 1 ceiling Common default / Uncommon peak (core §3.6). No Gold+ cards in F1 decks."},
        "needs_verify_note": "Cards whose 2024 text could not be confirmed are NOT in cards[]; each is listed here with its reason. Mechanics for every live card were checked against SRD 5.2.1 / DMG 2024 mirrors on 2026-10-04, not the printed books."}}
    extra_by_deck[S] = {"deck_notes": STORY_DECK_NOTES}
    for d in DECKS:
        print(d.dump(extra_by_deck.get(d)), len(d.cards))
