"""One-off: Day 1 cold start (Caleb lock 2026-10-05; Lore cold-open beats M-539/541/545/546/547/548/554).
Edits floors/f01/day-01.spec.json only."""
import json, copy, os, sys
# Portable paths (fresh-checkout safe): campaign root via tools/dcc_paths.py, never a box-only absolute path.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # tools/
import dcc_paths  # noqa: E402
SPEC_DIR = os.path.join(dcc_paths.CAMPAIGN_ROOT, "floors", "f01")
P = os.path.join(SPEC_DIR, "day-01.spec.json")
s = json.load(open(P))
FH = None
for e in s["encounters"]:
    for g in e["carry_on"]["gm_tracks"]:
        if g.startswith("Floor hour"):
            FH = g
assert FH
NONCOMBAT_CR = {"b70": {"kind": "cite", "paths": ["floors.1.fixed_encounters"], "note": "none (non-combat)"}}
NONCOMBAT_BUDGET = {"b70": {"kind": "cite", "paths": ["floors.1.xp.by_party_size"], "note": "Non-combat: no combat budget (daily XP guidance applies)"}}
PF = "[PLAYER-FACING]"
def vl(a, b, c):
    return {"system_intro": {"text": a, "tag": PF}, "midpoint_twist": {"text": b, "tag": PF}, "win": {"text": c, "tag": PF}}
def qr(setup, decision, ok, bad, minutes, cut):
    return {"setup": setup, "decision": decision, "on_success": ok, "on_failure": bad, "minutes": minutes, "tag": "pacing guide", "cut_short": cut}
def enemy(slot, sid, sname, our, sec, z):
    return {"slot": slot, "srd_id": sid, "srd_name": sname, "our_name": "%s (%s)" % (our, sname), "name_source": "00-overview.md section %s nameplate" % sec,
            "count_slot": {"b70": {"kind": "count", "path": "floors.1.fixed_encounters.%s.counts_by_party_size" % z, "key": sid}},
            "cr_slot": {"b70": {"kind": "cr", "path": "floors.1.fixed_encounters.%s.creatures" % z, "key": sid}}}
CREDIT_CITE = lambda note: {"b70": {"kind": "cite", "paths": ["floors.1.credits.cash_per_crawler_per_encounter_f1_scale"], "note": note}}

# ---------------- meta
m = s["meta"]
m["version"] = "0.5"
m["updated"] = "2026-10-05"
m["title"] = "Day {day} of {days}: The Glowing Stairwell, the Tutorial Zones, and the First Saferooms"
m["summary"] = ("Floor 1 timed playthrough, Day {day} of {days}, cold start: the party walks down a glowing surface stairwell inside the one-hour entrance window, "
                "becomes Crawlers on the first step onto Floor 1, and plays the tutorial line (Z0 to Z5) to the Z6 Break Room, then on toward the Z9 Green Room. "
                "Nothing collapses (tutorial pace). Three routes to the stairwell (dash, loot, clever) are laid out with eleven encounters, a Stairwell key findable three ways, "
                "loot and achievement hooks from existing decks and tables, and a stall fallback. CR, budget, credit and loot figures are cited from "
                "rules/70-encounter-budget-5e.json by field path (GM-adaptable guideline). A shared template: no live party is assumed.")
m["sources"] = [x for x in m["sources"] if not x.startswith("sessions/session-01-recap")]
m["sources"] += [
    "lore/CANON-LEDGER.md rows M-546, M-539, M-541, M-545, M-547, M-548 and M-554 (Lore's cold-open beats: horn and light-beam stairwells, one-hour entrance window, Natives, Crawler on the first step onto Floor 1, stairwell opening under someone, animals registered)",
    "Caleb cold-start lock (2026-10-05): new campaigns open at the surface stairwell; one live table at a time, many saved campaigns; day pages are shared templates and never hardcode a party",
    "floors/f01/00-overview.md sections 5.0 to 5.5 (Intake Hall, Atrium, Vent Row, Vending Gore Arcade, Hall of Fair Warnings, Shooting Gallery)",
]

# ---------------- day
d = s["day"]
d["start_zone"] = "z00"
d["start_zone_name"] = "The glowing surface stairwell, down into Zone 0: Intake Hall"
d["short_rest_slots"] = [
    "Slot 1 (suggested): after Vent Row (the first fight), only if someone is hurt.",
    "Slot 2 (suggested): after the Shooting Gallery, taken in the Break Room.",
    "Slot 3 (suggested): after the Locker Room.",
    "Slot 4 (suggested): reserve; a wandering Ceiling Tick fight or a bad trap. Do not push the party to spend them.",
]
d["last_chance_hooks"]["note"] = ("Outer zones (Z0 to Z4 plus 3b) close on Day 2 (confirmed grouping, inspired). On a cold start the party walks through all of them today, "
    "so anything not claimed in Z0 to Z4 and 3b by the Day 2 morning is gone; the Z5 hooks last until the mid zones close on Day 3. "
    "The GM checks the sheets for what is already claimed; Encounter Bot does not read state.")
for a in d["last_chance_hooks"]["achievements"]:
    a["note"] = a["note"].replace("; outer-zone hook, unclaimed, vanishes with the zone.", "; outer-zone hook, vanishes with the zone.").replace("; outer-zone hook, unclaimed.", "; outer-zone hook.")
d["stall_fallback"] = ("At the top of the stairs the one-hour entrance window does the work: the System counts it down, and anyone still on the surface when it closes is a Native, "
    "not a Crawler (canon M-539, M-541, M-545); that player rolls a fresh Crawler who joins at the next saferoom (Core Book Ch1, Death and Revival, Replacement Crawler). "
    "Once inside, Day 1 has no collapse, so stalling only costs clock. If the party loiters in the Atrium, Proctor Bell sells hints until they try the shutter (enc-d01-07). "
    "If they loiter in the Break Room, the System posts Short Rest and Long Rest reminders, the corkboard rumors repeat, and the Lights-Out hour arrives on schedule (enc-d01-04). "
    "If they refuse to pick a route, the vending terminal offers the bribe in enc-d01-01 and the speaker announces what the clock will do tomorrow. "
    "If the day rolls over at the 24-hour mark without a Long Rest, the System still posts the Day 2 notice; the party simply rests later at an honest saferoom. "
    "The Floor 1 Reprieve does not cover a missed collapse: that is death on every floor (decision 026), so say so at the start.")
d["start_note"] = ("Cold start (Caleb, 2026-10-05): the table begins on the surface at a glowing stairwell with the one-hour entrance window running, and each character becomes a Crawler "
    "on the first step onto Floor 1, in the Intake Hall (Z0; canon M-547). Intake runs in the booths: Death Mode first, then character creation (00-overview.md sections 1 and 5.0). "
    "Day 1 then runs the tutorial line, Z1 to Z5, to the Break Room (Z6, the first saferoom and the Welcome Boxes), and on through Z8 (Z7 optional) to the Green Room (Z9), "
    "where the default Long Rest closes the day. A Long Rest taken in the Break Room also closes Day 1, and Day 2 then starts there. "
    "Play order is the order on this page; encounter ids keep their earlier numbers so later pages still point at them. "
    "Floor hours count from the moment the entrances open (default reading; Syndicate may adjust). "
    "This page is a shared template: a saved campaign resuming mid-floor starts from its own session files, not from this cold open.")
for r in d["rest_options"]:
    if r["option"].startswith("Break Room"):
        r["note"] = "The first saferoom on the floor, where the Welcome Boxes are opened. Honest saferoom through Day 3; it stops being a saferoom when it loses service on Day 4 (decision 026). A Long Rest here ends Day 1 early."
d["gm_warning"]["text"] = ("Say it plainly at Floor 1 start, at the top of the stairwell or in the Intake Hall before the first fight: reach a stairwell before the collapse or you do not leave. "
    "Missing the collapse is death on Floor 1 as on every floor, and the Reprieve does not apply. Early-descent stasis counts as reaching a stairwell.")

# ---------------- routes
R = {r["id"]: r for r in s["routes"]}
R["route-dash"]["path"] = "Z0 to Z5 down the tutorial line (no bypass on Day 1), Z6, then Z8 (skip Z7) to Z9 to Z10 to the real stairwell at Z11 (behind the stage)."
R["route-dash"]["summary"] = ("Straight down the tutorial line, through the Locker Room and the Green Room, then the boss stage (full encounter on the Day 5 page, usable from Day 2). "
    "On Day 1 the party can reach the stage but the stairwells have not opened, so there is no descent yet. Reaching Z9 and resting there is when level 2 lands "
    "(00-overview.md section 5.9); a party that skips the rest meets the boss at level 1 and the GM uses Variant B (section 6.6).")
R["route-loot"]["path"] = ("Z0 to Z5 slowly (the Z3 machines and the 3b cache, Dale in Z4, the Z5 register), Z6, then Z7 (bait stairs and the Back Office), Z8, Z9 (rest, level 2), "
    "then the Z S service corridor and the service stairwell (skips the boss).")
R["route-loot"]["summary"] = ("Spend the day collecting: every tutorial zone is full today and the outer ones (Z0 to Z4 and 3b) close tomorrow morning, then the Greeters' Back Office, "
    "the Locker Room and the Green Room boxes. Ends at the service door in Zone S rather than the boss. Slow means the clock bites: each day the floor closes more of what you came to collect.")
R["route-clever"]["path"] = ("Z1 (listen to Proctor Bell, read the wall directory), Z3b (the scrawled map shows Zone S), Z4 by reading the signs, Z6 (corkboard, terminal, Complaint Card) "
    "to Z8 (use the room, not the weapons) to Z9 to the Z S service door with a bought or found key.")
for a in R["route-dash"]["achievements"]:
    if a["id"] == "ACH-1824":
        a["gm_note"] = ("Not earnable on Floor 1; listed for continuity. The surface entrance stairwell does not count: it leads onto Floor 1, not down from it. "
                        "Reward: see the catalog row (tables/achievements.csv, ACH-1824).")

# ---------------- existing encounters
E = {e["id"]: e for e in s["encounters"]}
e1 = E["enc-d01-01"]
e1["name"] = "The Break Room: First Saferoom and Briefing"
e1["map_in_the_mind"]["exits"][0] = "Back door to the Shooting Gallery (Z5, a mid zone, closes Day 3), with Z4 beyond it (outer, closes Day 2)."
for h in e1["loot_hooks"]:
    if h.get("check_text") == "Bronze Welcome Box":
        h["text"] = "Welcome Box ceremony: every Crawler receives a Bronze Welcome Box here and opens it during the rest (one tailored pull per overview)."
e1["quick_run"]["setup"] = "The Crawlers reach the first saferoom: a Welcome Box each, the clock briefing, and a terminal that sells a spare key."
e1["quick_run"]["on_success"] = "They open their Welcome Boxes, pick a route and leave with a plan, or take the Long Rest here and end Day 1 early."
e1["carry_on"]["gm_tracks"] = [g if not g.startswith("Welcome Box held") else "Welcome Boxes opened, and for which Crawlers" for g in e1["carry_on"]["gm_tracks"]]
e5 = E["enc-d01-05"]
for c in e5["carry_on"]["changes"]:
    if c["choice"] == "What they leave in the outer zones":
        c["effect"] = "Anything uncollected in Z0 to Z4 and 3b is gone when those zones close on Day 2; the notice names the loss. Z5 is a mid zone and stays open one more day."

# ---------------- new encounters (play order: 06..11, then 01..05)
new = []
new.append({
  "id": "enc-d01-06", "name": "Cold Open: The Glowing Stairwell", "zone": "z00",
  "zone_name": "Surface stairwell, down into Zone 0: Intake Hall", "route": ["dash", "loot", "clever"], "route_primary": "dash",
  "kind": "non-combat (cold open and intake)",
  "map_in_the_mind": {
    "layout": "Street level: a stairwell has opened in the pavement with a beam of light shooting straight up out of it, and concrete steps lead down into the light. At the bottom is the Intake Hall, a long hallway of identical booths.",
    "exits": ["Down the stairs onto Floor 1; the first step onto the floor makes a Crawler (canon M-547).",
              "Back up to the surface, until the one-hour window closes (canon M-539).",
              "The booth doors open onto the Atrium (Z1) once intake is done."],
    "hazards": ["The one-hour entrance window: the System counts it down (canon M-539, M-545).",
                "Standing on the stairs is not entering (canon M-547).",
                "A stairwell can open under a bystander and swallow them (canon M-548)."],
    "cover": ["None that matters."]},
  "enemies": [], "enemies_note": "No enemies. Intake runs here: Death Mode first (00-overview.md section 1), then character creation in the booths (section 5.0).",
  "cr_slot": copy.deepcopy(NONCOMBAT_CR), "budget_slot": copy.deepcopy(NONCOMBAT_BUDGET),
  "voice_lines": vl(
    "A horn like a stadium trumpet rolls over the city, and stairwells open in the pavement, each one firing a beam of light straight into the sky. The entrances stay open for one hour. Anyone still up here when they close stays up here as a Native, and the System wishes them luck with that. Walk down, and keep walking: you become a Crawler the moment your foot touches Floor 1, not one stair sooner.",
    "Your foot touches the floor and a chime goes off inside your skull: CRAWLER REGISTERED. Anything alive over the weight limit gets registered too, so somebody's dog now has a nameplate. A booth door clunks open and waits.",
    "Paperwork filed, Death Mode chosen, nameplates printed with at least one name spelled wrong. Welcome to the Orientation Pit. The booths open onto an atrium, and something in there is clacking its jaw."),
  "loot_hooks": [{"kind": "placed", "text": "Nothing to loot on the stairs. Start the audience-nickname plant: the hallway screen misspells one Crawler's name (00-overview.md section 8.5).",
                  "overview_ref": "00-overview.md sections 5.0 and 8.5", "check_text": "audience-nickname plant"}],
  "achievement_hooks": [{"id": "ACH-0079", "note": "Don't Skip Intro starts here: whoever reads the full intake popup and then sits through Proctor Bell's spiel in the Atrium (enc-d01-07)."}],
  "scaling": {"2": "Issue the Assigned Companion at intake: Pudding, the Mastiff in a tiny mortarboard (00-overview.md section 9.3).",
              "3": "As written.",
              "4": "As written; give each player one beat stepping out of a booth (00-overview.md section 5.0)."},
  "if_they_do_something_dumb": ("If a character stays on the stairs or goes back up, they are not a Crawler yet (canon M-547). When the one-hour window closes, anyone still on the surface is a Native and out of the game as that character (canon M-539, M-541, M-545); "
    "the player rolls a fresh Crawler who joins at the next saferoom (Core Book Ch1, Death and Revival, Replacement Crawler). Pets over the weight limit that go through are registered as well (canon M-554); "
    "the GM decides whose animal followed whom. If someone stands at the edge of open pavement to gawk, the System can open a stairwell under them and drop them in (canon M-548): "
    "house call, tagged inspired, they land in the Intake Hall winded and embarrassed, never hurt. Never a wipe."),
  "canon_zone": "z00",
  "quick_run": qr("Stairwells with light beams open in the pavement; the one-hour entrance window is running and the characters stand at the top.",
                  "Go down now, or linger on the surface while the window runs?",
                  "Everyone steps onto Floor 1, becomes a Crawler and finishes intake in the booths.",
                  "Someone lingers; the System counts down and the window closes on anyone still up top.",
                  10, "Read the System intro, have everyone step down together, and run intake from the booths."),
  "carry_on": {"changes": [
      {"choice": "Who steps onto Floor 1 before the window closes",
       "effect": "Only those who set foot on Floor 1 are Crawlers; anyone left up top is a Native and the player needs a new Crawler. A two-Crawler table gets its Assigned Companion here.",
       "reacts_in": ["enc-d01-07", "enc-d01-01"]},
      {"choice": "Death Mode and the misspelled nameplate",
       "effect": "Death Mode is logged before the first fight; the misspelled name starts the audience nickname that the floor summary records.",
       "reacts_in": ["enc-d01-08", "enc-d05-04"]}],
    "gm_tracks": [FH, "Who entered before the one-hour window closed, and any Natives left on the surface",
                  "Death Mode logged for each Crawler", "Animals registered (canon M-554) and the Assigned Companion for a two-Crawler table",
                  "Misspelled nameplate (audience-nickname plant)"]}})
new.append({
  "id": "enc-d01-07", "name": "The Atrium: Proctor Bell's Meet-and-Greet", "zone": "z01", "zone_name": "The Atrium",
  "route": ["clever", "dash", "loot"], "route_primary": "clever", "kind": "non-combat (d20 tests)",
  "map_in_the_mind": {
    "layout": "A three-story concrete atrium around a dead fountain, smooth jazz from the ceiling speakers, and a glass booth on ceiling rails holding Proctor Bell, a painted wooden fortune-teller.",
    "exits": ["The jammed security shutter, onward to Vent Row (Z2).", "Back to the Intake Hall booths (Z0)."],
    "hazards": ["The jammed shutter (Strength (Athletics); check value in 00-overview.md section 5.1).", "Sharp-edged fountain coins (Dexterity (Sleight of Hand); section 5.1)."],
    "cover": ["The fountain rim (half cover if it ever matters)."]},
  "enemies": [], "enemies_note": "No enemies. Proctor Bell is a guide, not a target (00-overview.md section 11.2).",
  "cr_slot": copy.deepcopy(NONCOMBAT_CR), "budget_slot": copy.deepcopy(NONCOMBAT_BUDGET),
  "voice_lines": vl(
    "A glass booth squeals along its ceiling rail and stops in front of you. The wooden fortune-teller inside clacks its jaw and introduces itself as your teacher. It points at a security shutter jammed halfway up, which is apparently the way out.",
    "Under the graffiti, the wall directory still mostly reads. Somebody lettered GREEN ROOM, STAFF ONLY far too neatly for it to be a joke. Proctor Bell pretends not to notice you reading it.",
    "The shutter screams up into the ceiling. Proctor Bell rings once, which is either applause or a warning. Beyond the shutter, something skitters."),
  "loot_hooks": [{"kind": "placed", "text": "Fountain coins (corroded, a sharp edge) and Proctor Bell's one-credit hint (00-overview.md section 5.1).",
                  "overview_ref": "00-overview.md section 5.1", "check_text": "Fountain coins",
                  "amount": CREDIT_CITE("Fountain coins: amount as in 00-overview.md section 5.1, inside the floor credit scale")}],
  "achievement_hooks": [{"id": "ACH-0079", "note": "Don't Skip Intro: sit through Proctor Bell's whole spiel (00-overview.md section 5.1)."}],
  "scaling": {"2": "The shutter check stays; the Assigned Companion can Help.", "3": "As written.", "4": "As written; teach Help with two Crawlers on the shutter."},
  "if_they_do_something_dumb": "If someone attacks Proctor Bell, it self-heals and withholds its hints for the floor (00-overview.md section 11.2). If nobody can lift the shutter, Proctor Bell sells a hint for a credit and the Help action does the rest; failure costs time, never the route. Never a wipe.",
  "canon_zone": "z01",
  "quick_run": qr("A dead fountain, smooth jazz, and a fortune-teller booth that glides in to teach d20 tests.",
                  "Lift the stuck shutter together, read the directory, or pay Proctor Bell for a hint?",
                  "The shutter goes up, the System Map shows Z1 to Z6, and the Crawlers move on.",
                  "They fumble the shutter; Proctor Bell sells a hint and the Help action gets them through.",
                  8, "One Athletics check with Help for the shutter; skip the fountain and the directory."),
  "carry_on": {"changes": [
      {"choice": "Read the wall directory", "effect": "Z1 to Z6 show on the System Map and the Green Room is named, which points every route at Z9.", "reacts_in": ["enc-d01-01", "enc-d01-05"]},
      {"choice": "Treat Proctor Bell well, or not", "effect": "A friendly Bell keeps selling cheap hints through the Hall of Fair Warnings and the Locker Room; a hostile Bell withholds them for the floor.", "reacts_in": ["enc-d01-10", "enc-d01-03"]}],
    "gm_tracks": [FH, "Directory read (map shows Z1 to Z6)", "Proctor Bell's mood: friendly or hostile", "Who sat through the whole spiel (ACH-0079)"]}})
new.append({
  "id": "enc-d01-08", "name": "Vent Row: Combat 101", "zone": "z02", "zone_name": "Vent Row",
  "route": ["dash", "loot", "clever"], "route_primary": "dash", "kind": "combat",
  "map_in_the_mind": {
    "layout": "A service hallway lined with floor vents, every grate bent outward, with red UI brackets over the openings.",
    "exits": ["Back through the shutter to the Atrium (Z1).", "On to the Vending Gore Arcade (Z3)."],
    "hazards": ["Two vents 20 ft apart spill the rats in two groups (00-overview.md section 5.2).", "Backing away from a rat triggers the first Opportunity Attack popup."],
    "cover": ["Bent grates and wall pipes (half cover)."]},
  "enemies": [enemy("vent-rat", "giant-rat", "Giant Rat", "Vent Rat", "5.2", "z02")],
  "enemies_note": "First combat of the floor: roll initiative for everyone in one post and print the order (00-overview.md section 5.2). Pack Tactics makes the rats ugly in groups.",
  "budget_slot": {"b70": {"kind": "fit", "path": "floors.1.fixed_encounters.z02.fit"}},
  "voice_lines": vl(
    "The vents start skittering the second the shutter is up. Red brackets pop up over every grate, which is the System's way of saying these are the bad guys. This is Combat 101, and attendance is mandatory.",
    "The second wave climbs out of a vent twenty feet down the hall, right where nobody was looking. Somebody just learned about flanking the hard way. The audience felt that one.",
    "Rats down. You are now qualified to work the night shift at a children's pizza arcade. The vents rattle with dropped change, if you're the kind of Crawler who checks vents."),
  "loot_hooks": [{"kind": "placed", "text": "Dropped change in the vents; the rats carry nothing (00-overview.md section 5.2).", "overview_ref": "00-overview.md section 5.2",
                  "check_text": "Rats carry nothing", "amount": {"b70": {"kind": "text", "path": "floors.1.fixed_encounters.z02.cash_dice_per_crawler", "note": "Vent change per Crawler"}}}],
  "achievement_hooks": [{"id": "ACH-0001", "note": "First Blood: the killing blow on the floor's first enemy."},
                        {"id": "ACH-0860", "note": "Win Initiative on the floor's first roll (the overview downgrades it to a snark-only reward here)."},
                        {"id": "ACH-0894", "note": "Land a critical hit."},
                        {"id": "ACH-0205", "note": "Scenic Panic: whoever panics out loud before the fight and then wins it."}],
  "scaling": {"2": "Two-Crawler count from the budget file; the Assigned Companion draws a rat's attention.",
              "3": "Three-Crawler count from the budget file.",
              "4": "Four-Crawler count in two groups from vents 20 ft apart (00-overview.md sections 5.2 and 9.3)."},
  "if_they_do_something_dumb": "If someone sticks an arm into a vent, a rat bites it (a normal attack) and the System posts a toast. If the party runs back through the shutter, the rats follow into the Atrium and the fight goes on there. If a Crawler drops, run the death-save popup; a death here is real unless that Crawler's Floor 1 Reprieve is unused (Core Book Ch1, Reprieve). It is a Low fight by design, never a wipe.",
  "canon_zone": "z02",
  "quick_run": qr("A vent-lined hall and two waves of giant rats: the floor's first fight.",
                  "Hold the line together, or chase rats down the hall?",
                  "The rats fall and the Crawlers learn initiative, flanking and Opportunity Attacks.",
                  "A Crawler drops and the party spends its first short-rest slot early.",
                  12, "Run one wave only and resolve the second with a single group check."),
  "carry_on": {"changes": [
      {"choice": "How the first fight goes", "effect": "Damage taken here decides whether the first short-rest slot goes before the Arcade; a clean fight saves it for the Hall of Fair Warnings.", "reacts_in": ["enc-d01-09", "enc-d01-10"]},
      {"choice": "Check the vents for change", "effect": "Credits found here go toward the Break Room terminal (the spare key or potions).", "reacts_in": ["enc-d01-01"]}],
    "gm_tracks": [FH, "First Blood (who)", "HP and short-rest slots after the first fight", "Initiative and Opportunity Attack popups shown"]}})
new.append({
  "id": "enc-d01-09", "name": "Vending Gore Arcade: The Loot Lesson", "zone": "z03", "zone_name": "Vending Gore Arcade",
  "route": ["loot", "clever", "dash"], "route_primary": "loot", "kind": "non-combat (hazard and loot)",
  "map_in_the_mind": {
    "layout": "A long hall of vending machines, half smashed and half glowing and faintly breathing, with a body in scrubs face-down in the middle of the floor.",
    "exits": ["Back to Vent Row (Z2).", "On to the Hall of Fair Warnings (Z4).", "A false panel behind the change machine opens the back cage (3b; hidden, check values in 00-overview.md section 5.3)."],
    "hazards": ["Hungry vendors bite a reaching arm (a Dexterity save, then Strength (Athletics) to pull free; section 5.3).", "Prying a machine open is loud: one Ceiling Ticks roll (section 5.11)."],
    "cover": ["Machines (half cover; the breathing ones are a bad idea)."]},
  "enemies": [], "enemies_note": "No enemies unless a loud pry brings a Ceiling Ticks roll (enc-d01-04).",
  "cr_slot": copy.deepcopy(NONCOMBAT_CR), "budget_slot": copy.deepcopy(NONCOMBAT_BUDGET),
  "voice_lines": vl(
    "Rows of vending machines hum in a dozen colors, and some of them are breathing. One screen promises that you deserve this. A woman in scrubs lies face-down in the wrappers, one arm still reaching for it. This is the loot lesson, and she is the first page.",
    "A machine closes on someone's arm with a satisfied little click. The screen thanks you for your patronage. Pull, or wait for the next customer.",
    "Pockets full, one arm slightly chewed, and a stamped coin that feels heavier than it should. The machines go dark one by one and read SOLD OUT FOREVER, the most honest thing in the building."),
  "loot_hooks": [
    {"kind": "placed", "text": "Tanya Ruiz's corpse cache: a Mop-Handle Staff, a lore scrap, a Potion of Healing reskinned as Sports Drink, Red Flavor, and some credits (00-overview.md sections 5.3 and 8.3, potion #1).",
     "overview_ref": "00-overview.md section 5.3", "check_text": "Tanya Ruiz's body",
     "amount": CREDIT_CITE("Corpse-cache credits as in 00-overview.md section 5.3, inside the floor credit scale")},
    {"kind": "card", "card_id": "f01-z03-0004", "note": "A vending pull: the Common consumable row."},
    {"kind": "card", "card_id": "f01-z03-0005", "note": "A vending pull: a mundane item."},
    {"kind": "card", "card_id": "f01-z03-0008", "note": "A vending pull: the credits row."},
    {"kind": "placed", "text": "Lost & Found crate: junk and the Odd Coin (spine plant; log the holder; never explain it). 00-overview.md sections 5.3 and 8.4.",
     "overview_ref": "00-overview.md section 5.3", "check_text": "Lost & Found Bin"},
    {"kind": "placed", "text": "Back cage (3b) hidden cache: a Potion of Healing (potion #2), a riot shield, credits, and the scrawled map that reveals Zone S (00-overview.md section 5.3).",
     "overview_ref": "00-overview.md section 5.3", "check_text": "hidden cache",
     "amount": CREDIT_CITE("Back-cage credits as in 00-overview.md section 5.3, inside the floor credit scale")}],
  "achievement_hooks": [{"id": "ACH-0083", "note": "Corpse Lesson: loot Tanya's body."},
                        {"id": "ACH-0871", "note": "Find a journal or lore scrap: Tanya's note."},
                        {"id": "ACH-0872", "note": "Read a lore scrap aloud: Tanya's note, done with feeling."},
                        {"id": "ACH-0077", "note": "Vending Gore: loot the hungry machines."},
                        {"id": "ACH-0081", "note": "Hidden toast only when the coin is pocketed (00-overview.md section 5.3)."},
                        {"id": "ACH-0177", "note": "Hidden Cache: the back cage (3b)."},
                        {"id": "ACH-0179", "note": "Side Path: Zone S revealed by the 3b map."}],
  "scaling": {"2": "Same machines; the per-Crawler vending cap (section 5.3) keeps a small party from emptying the hall.", "3": "As written.", "4": "As written."},
  "if_they_do_something_dumb": "If someone tries to sell the Odd Coin to a machine, it refuses (ITEM NOT RECOGNIZED) or offers a suspicious sum and cancels mid-animation (00-overview.md section 5.3). If someone keeps reaching after SOLD OUT FOREVER, the machine bites anyway and the System posts a toast. Each loud pry is a Ceiling Ticks roll (enc-d01-04). Never a wipe.",
  "spine_plant_gm_only": "[GM-ONLY] The Odd Coin must be planted on Floor 1 (00-overview.md section 8.4): the Lost & Found crate here; fallbacks are a Green Room box Weird pull or Dale's pocket. Never explain it.",
  "canon_zone": "z03",
  "quick_run": qr("A hall of hungry vending machines, a fallen Crawler's cache, and a crate with a strange stamped coin.",
                  "Reach into the machines, pry them open loudly, or search the body and the crate first?",
                  "They loot the hall, read Tanya's note and pocket the stamped coin.",
                  "Arms get bitten, a loud pry draws a Ceiling Ticks roll, and the cache behind the change machine stays hidden.",
                  12, "One roll per Crawler on the vending table; hand over Tanya's cache and the coin without checks."),
  "carry_on": {"changes": [
      {"choice": "Find the back cage (3b)", "effect": "The scrawled map reveals Zone S, which opens the clever and loot routes to the service door; a missed cache is gone when the outer zones close on Day 2.", "reacts_in": ["enc-d02-02", "enc-d05-02"]},
      {"choice": "Read Tanya's note", "effect": "Her note warns that the green EXIT is a trick and that the big man on the stage counts before he swings; it pays off at the bait stairs and in the boss fight.", "reacts_in": ["enc-d01-02", "enc-d05-03"]},
      {"choice": "Who pockets the stamped coin", "effect": "The holder is logged; the coin follows them all floor with no mechanics and no explanation.", "reacts_in": ["enc-d01-01"]}],
    "gm_tracks": [FH, "Stamped coin holder (or which fallback was used)", "Back cage found, and Zone S revealed", "Vending cap reached, per Crawler", "Potions #1 and #2 taken"]}})
new.append({
  "id": "enc-d01-10", "name": "Hall of Fair Warnings: Read the Signs", "zone": "z04", "zone_name": "Hall of Fair Warnings",
  "route": ["clever", "loot", "dash"], "route_primary": "clever", "kind": "trap + rescue",
  "map_in_the_mind": {
    "layout": "A clean, well-lit corridor about 100 feet long, caution tape on both walls and a row of ever-louder TRAP signs; Dale Pruitt hangs upside down in a snare net halfway along.",
    "exits": ["Back to the Arcade (Z3).", "On to the Shooting Gallery (Z5)."],
    "hazards": ["Welcome Mat pressure plates and a swinging WET FLOOR sign (check values in 00-overview.md section 5.4).",
                "Ticket, Please turnstile with a hidden needle (poison; section 5.4).", "The snare net holding Dale, with a plate right under him."],
    "cover": ["None worth naming; the hazard is the floor."]},
  "enemies": [], "enemies_note": "No enemies. The traps are the lesson, and the signs are honest (00-overview.md section 5.4).",
  "cr_slot": copy.deepcopy(NONCOMBAT_CR), "budget_slot": copy.deepcopy(NONCOMBAT_BUDGET),
  "voice_lines": vl(
    "Three cheerful signs line the corridor, and each one says TRAP louder than the last. Halfway along, a man in a net turns slowly upside down and waves, which only makes him spin. He calls out that his name is Dale and that you should avoid the square tiles.",
    "A plate clicks under somebody's shoe and a WET FLOOR sign swings out of the wall like it has been waiting all day. Dale spins faster. The signs, for the record, said so.",
    "Dale is down, upright and very grateful, and he has already offered to carry things. The third sign was begging, and somebody still stepped on a plate. The System will be mentioning it."),
  "loot_hooks": [{"kind": "placed", "text": "Dale Pruitt, rescued: he tags along and gives Advantage on one check per zone involving vents, doors or machinery (00-overview.md section 5.4).",
                  "overview_ref": "00-overview.md section 5.4", "check_text": "Rescue Dale"}],
  "achievement_hooks": [{"id": "ACH-0869", "note": "Rescue a civilian NPC: Dale in the net."},
                        {"id": "ACH-0870", "note": "Fail to rescue: if Dale dies (run the permanence popup, 00-overview.md section 3.4)."},
                        {"id": "ACH-0877", "note": "Disarm an enemy trap with junk: wedge a Welcome Mat plate."},
                        {"id": "ACH-0198", "note": "Poison Tolerant: Poisoned by the turnstile needle, then cured."}],
  "scaling": {"2": "Same traps; a small party leans on the Assigned Companion or a rope to catch Dale.", "3": "As written.", "4": "As written; plenty of hands for the plate, the net and the catch."},
  "if_they_do_something_dumb": "If someone walks onto a signed plate anyway, the sign swings and the System reads the signs back to them; it costs HP, not the route. If Dale falls and dies, run the permanence popup (00-overview.md section 3.4) and play the laugh track cutting off a beat too late. Never a wipe.",
  "canon_zone": "z04",
  "quick_run": qr("An honest, signed trap hall with a man hanging in a net above a pressure plate.",
                  "Disarm the plates and get Dale down carefully, or rush through and hope?",
                  "Dale is rescued and joins as a helper, and the Crawlers learn saving throws.",
                  "A plate drops Dale or a Crawler; the cost is HP and, at worst, Dale.",
                  10, "One Perception check for the plates and one check to catch Dale; skip the turnstile."),
  "carry_on": {"changes": [
      {"choice": "Rescue Dale, or not", "effect": "A rescued Dale tags along with his one-check-per-zone help, and his labeled sandwich waits in the Break Room fridge; a dead Dale gets the permanence popup and can carry the coin fallback (00-overview.md section 8.4).", "reacts_in": ["enc-d01-01", "enc-d04-01"]},
      {"choice": "Get poisoned at the turnstile", "effect": "A Crawler Poisoned and then cured earns Poison Tolerant; the hook vanishes when the outer zones close on Day 2.", "reacts_in": ["enc-d02-01"]}],
    "gm_tracks": [FH, "Dale: rescued, dead or left hanging", "Traps sprung or disarmed, and with what", "Anyone Poisoned, and whether it was cured"]}})
new.append({
  "id": "enc-d01-11", "name": "Shooting Gallery: Range and Cover", "zone": "z05", "zone_name": "Shooting Gallery",
  "route": ["dash", "loot", "clever"], "route_primary": "dash", "kind": "combat",
  "map_in_the_mind": {
    "layout": "A carnival shooting gallery scaled up to a big room: plywood cutouts on squeaking conveyors, overturned counters, sandbags, a cash register on a stool, and mannequins in staff polos behind the far counter.",
    "exits": ["Back to the Hall of Fair Warnings (Z4).", "A door with a cartoon coffee cup on it: the Break Room (Z6)."],
    "hazards": ["Conveyors carry a standing Crawler 10 ft at the end of each round (00-overview.md section 5.5).", "The mannequins shoot from behind the far counter and close to melee only if the Crawlers do."],
    "cover": ["Counters and sandbags (half cover); the brick prize booth (three-quarters cover)."]},
  "enemies": [enemy("mannequin", "skeleton", "Skeleton", "Mannequin Staff", "5.5", "z05")],
  "enemies_note": "Skeletons are vulnerable to bludgeoning as written; let the crowbars shine (00-overview.md section 5.5).",
  "budget_slot": {"b70": {"kind": "fit", "path": "floors.1.fixed_encounters.z05.fit"}},
  "voice_lines": vl(
    "Behind the far counter, mannequins in staff polos turn their heads all at once, with a sound like a dropped tray of silverware. Each one raises a pink plastic bow that is very clearly not a toy. Somewhere above, Proctor Bell suggests getting behind things.",
    "Someone steps onto a conveyor and glides ten feet sideways like a carnival prize. The mannequins keep smiling. It's in their contract.",
    "The last mannequin drops its bow and keeps smiling anyway. The register on the stool is still full, plus a raffle ticket the System refuses to explain. Through the far door: a cartoon coffee cup and a green light."),
  "loot_hooks": [{"kind": "placed", "text": "Cash register: credits and a raffle ticket that does nothing (00-overview.md section 5.5).", "overview_ref": "00-overview.md section 5.5",
                  "check_text": "raffle ticket", "amount": {"b70": {"kind": "text", "path": "floors.1.fixed_encounters.z05.cash_dice_per_crawler", "note": "Register change per Crawler"}}}],
  "achievement_hooks": [{"id": "ACH-0867", "note": "Block a hit with a shield or brace (the 3b riot shield earns its keep)."},
                        {"id": "ACH-0861", "note": "Lose initiative and still win."},
                        {"id": "ACH-0894", "note": "Land a critical hit."}],
  "scaling": {"2": "Two-Crawler count from the budget file; lean on the cover so the lesson lands without a wipe.",
              "3": "Three-Crawler count from the budget file.",
              "4": "Four-Crawler count (00-overview.md sections 9.2 and 9.3): top of the Low band, and the cover makes it bite."},
  "if_they_do_something_dumb": "If the Crawlers charge across open floor, the mannequins get every shot; the cost is HP. If someone rides a conveyor on purpose, let them (no save) and let the System narrate it like a prize. If a Crawler drops, a death here is real unless that Crawler's Floor 1 Reprieve is unused (Core Book Ch1, Reprieve). Never a wipe by design.",
  "canon_zone": "z05",
  "quick_run": qr("A carnival shooting gallery where smiling mannequins shoot from behind counters.",
                  "Use cover and close carefully, or rush the counter?",
                  "The mannequins fall, the cover lesson lands and the register pays out.",
                  "Crawlers caught in the open take the shots; someone needs a short-rest slot in the Break Room.",
                  12, "Run two rounds with cover, then resolve the rest as one group check."),
  "carry_on": {"changes": [
      {"choice": "How much damage they bring to the Break Room", "effect": "The next room is the first saferoom: a hurt party takes a Short Rest there or the Long Rest, which ends Day 1 early at Z6.", "reacts_in": ["enc-d01-01"]},
      {"choice": "Leave the gallery unfinished", "effect": "Z5 is a mid zone: its hooks stay until the mid zones close on Day 3.", "reacts_in": ["enc-d02-01", "enc-d03-02"]}],
    "gm_tracks": [FH, "HP and short-rest slots entering the Break Room", "Register looted", "Cover popup shown"]}})

ids = {e["id"] for e in s["encounters"]}
assert not ids & {e["id"] for e in new}
s["encounters"] = new + s["encounters"]
json.dump(s, open(P, "w"), indent=2, ensure_ascii=False)
open(P, "a").write("\n")
print("encounters:", [e["id"] for e in s["encounters"]])
