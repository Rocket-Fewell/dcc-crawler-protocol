#!/usr/bin/env python3
"""One-shot dev patch: budget-file references, death-on-miss rule, quick runs, carry-on, zone color, GM warnings.
Run from anywhere (spec paths come from tools/dcc_paths.py). Pure local, no model calls. Not a deliverable of the generator."""
import json, copy, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from content_quick_carry import QUICK, CARRY
# Portable paths (fresh-checkout safe): campaign root via tools/dcc_paths.py, never a box-only absolute path.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # tools/
import dcc_paths  # noqa: E402
SPEC_DIR = os.path.join(dcc_paths.CAMPAIGN_ROOT, "floors", "f01")

PF = "[PLAYER-FACING]"
P = "floors.1."
def party(path, note=None):
    r = {"kind": "party", "path": path}
    if note: r["note"] = note
    return {"b70": r}
def cnt(zone, key): return {"b70": {"kind": "count", "path": P + "fixed_encounters.%s.counts_by_party_size" % zone, "key": key}}
def crr(zone, key): return {"b70": {"kind": "cr", "path": P + "fixed_encounters.%s.creatures" % zone, "key": key}}
def fit(zone): return {"b70": {"kind": "fit", "path": P + "fixed_encounters.%s.fit" % zone}}
def cite(paths, note=None):
    r = {"kind": "cite", "paths": paths if isinstance(paths, list) else [paths]}
    if note: r["note"] = note
    return {"b70": r}
def scalar(path, note=None, kind="scalar"):
    r = {"kind": kind, "path": path}
    if note: r["note"] = note
    return {"b70": r}
NONCOMBAT_CR = cite(P + "fixed_encounters", "none (non-combat)")
NONCOMBAT_BUDGET = cite(P + "xp.by_party_size", "Non-combat: no combat budget (daily XP guidance applies)")
BOXES = {"b70": [{"kind": "cite", "paths": ["economy_audit.floor_1"], "note": "Box openings"}, {"kind": "cite", "paths": [P + "boxes"]}]}
VENDOR = scalar(P + "prices.potion_of_healing_vendor.price", "Potion of Healing vendor price")
def reward(name): return scalar(P + "achievement_rewards.proposed.%s.reward" % name, kind="text")

NOTICE = {
 2: "Attention, Crawlers: the outer zones are now closed for renovation, and by \"renovation\" we mean \"gone.\" Anything you left in them is now a lesson. The way forward remains open. You're welcome.",
 3: "Update: the middle of the floor is joining the outer parts in the afterlife. Loot and services there have ended. Your route is untouched, because we want you to see what's next. Sadly.",
 4: "Notice: the Break Room is now off duty. The vending terminal has gone to lunch and will not return. Resting there is no longer recommended. The Green Room remains open, for reasons of mercy and liability.",
 5: "This is your final-morning reminder: in {hours} hours this floor collapses with you or without you. Only the corridor is left. The stairwell is down the hall. Please do not make us say it twice.",
}
SIX = "Six hours remain. Anyone going down the stairs from this point descends freely. Anyone who went earlier is still napping in the stairwell. Hurry up."
MISS = "The floor has closed. Your attendance has been noted and your tenure has been terminated. We will not be sending flowers."
LORE_WARN = "Reach a stairwell before the collapse or you do not leave. This is not a toll. This is not a detour. This is the end."
GM_WARN = {
 "start": "Say it plainly at Floor 1 start: reach a stairwell before the collapse or you do not leave. A Crawler who is not at a stairwell when the floor collapses is dead, on Floor 1 as on every floor, and the Reprieve does not apply. Early-descent stasis counts as reaching a stairwell.",
 "pen": "Day 4 reminder, say it plainly: the floor collapses at the end of Day 5. A Crawler who is not at a stairwell then is dead, with no Reprieve. Remind the table of the free descent in the last six hours and that stasis counts as reaching a stairwell.",
 "last": "Day 5 reminder, say it plainly: the floor collapses at 24 in-game hours of today, whatever the party is doing. A Crawler who is not at a stairwell then is dead, and the Reprieve does not apply. Stasis from an early descent counts as reaching a stairwell.",
}
ZONE = {
 "src": "lore/drafts/floor1-zone-color.draft.md (Lore draft v0.1, own words, optional read-aloud)",
 2: ["A section of ceiling lets go behind you, and the noise rolls down the corridor like applause. The speakers crackle: \"Zone closing. Please enjoy your last look.\"",
     "The floor tiles ahead are bright and clean. The ones behind are gray rubble. Someone has painted a thin white line where the two meet, and it is moving toward you.",
     "A vending alcove sits half-buried under fallen concrete, its light still blinking. The sign reads \"Temporarily closed. Permanently, actually.\"",
     "Dust hangs in the air and every footstep leaves a print. Somewhere a mob is following the prints, and it is patient."],
 3: ["The walls start shedding old posters and warning signs. Under them is raw stone with tally marks scratched by earlier Crawlers. Some tallies stop mid-row.",
     "A hallway you crossed this morning is now a gap with a clean edge. You can still see the doorway on the far side, which is its own kind of insult.",
     "Emergency lights flip from white to a tired orange. The recorded voice announces the closing zone at the same cheerful volume as everything else.",
     "A crowd of mobs has stopped to watch the floor fall. They look as unhappy about it as you do."],
 4: ["The lights go out in sections, one hall at a time, until only your own lantern is left. The dark makes a sound, a slow settling, like a building thinking.",
     "You find a dead-end alcove and sit with your backs to the wall. Every few minutes the far end of the hall clicks, ticks, and goes quiet again.",
     "Someone has left a half-eaten ration and a note on the floor: \"Slept here. Do not recommend.\" No signature.",
     "Rest is possible, but it is not comfortable. Whoever takes watch hears the System's announcement chime from three zones away, muffled, like a door closing on a party you were not invited to."],
}
FIELD_REST = ("A field rest can only be a Short Rest (Core section 5.6: Long Rests only in saferooms). The rest-without-a-saferoom price ({{b70:floors.1.prices.rest_without_saferoom}}) "
              "buys a quiet Short Rest and grants no Long Rest; unpaid or noisy, Ceiling Ticks interrupt it (00-overview.md section 2 rule 7). %s")
FIELD_REST_TAIL = {"early": "A saferoom is where the day's Long Rest happens (the Break Room through Day 3, the Green Room always).",
                   "late": "The Green Room is where the day's Long Rest happens."}
BR_SAFE = "Honest saferoom through Day 3; it stops being a saferoom when it loses service on Day 4 (decision 026)."

PENDING = [
 {"owner": "Syndicate", "item": "rules/70-encounter-budget-5e.json v0.1.0 (filed): slots with no matching field",
  "waiting_for": "Most slots on this page now cite the budget file by field path. Any slot still bracketed has no matching field there (for example counts and budgets for the house-built Day 2 to 4 Usher and displaced-vermin encounters); Syndicate was told which.",
  "status": "partly filled; remaining slots listed in the report"},
 {"owner": "Caleb", "item": "Veto window on one Syndicate default (decision 026, ~9:45 PM CT)",
  "waiting_for": "The final collapse is fixed at 24 in-game hours into the last day and a Long Rest never ends or skips the floor. (The missed-collapse rule is no longer open: Caleb ruled at ~10:02 PM CT that it is death on every floor, no Reprieve.)",
  "status": "open (default applies)"},
 {"owner": "Day-count field", "item": "clock.days",
  "waiting_for": "Floor 1 is 5 (field set), Floor 2 is 10, Floor 3 is 20 (Caleb, decision 026). Page text takes the day count from the field; nothing is hard-coded.",
  "status": "settled"},
 {"owner": "Lore", "item": "Canon table, collapse notices, missed-floor line and zone color",
  "waiting_for": "Received and used: canon-floor-1.json (rebuilt; sha256 and ledger version in the page meta), floor1-collapse-notices.draft.md (Day 2 to 5 notices, six-hours warning, death-version missed-floor line, GM warning line, achievement frames) and floor1-zone-color.draft.md (read-aloud color). If Lore edits any of them, re-run the script.",
  "status": "received"},
 {"owner": "Syndicate", "item": "ACH rows for canon A-044, A-151 and A-139",
  "waiting_for": "Canon-ledger rows that are not in tables/achievements.csv; the pages cite them as canon references only. A-044 is not attainable on Floor 1; A-151 only in the stasis form. The six proposed achievements take their rewards from the budget file by field path.",
  "status": "waiting (backlog)"},
 {"owner": "Syndicate", "item": "Budget file wording that predates Caleb's ~10:02 PM CT ruling",
  "waiting_for": "In rules/70-encounter-budget-5e.json the detour_tax.what text still lists a missed collapse as a Detour Tax case, open question Q1b asks about a larger missed-collapse toll, and Q2 still lists Floor 3 as 15 or 20 days. The pages cite only the party_toll_by_size field. Encounter Bot may not edit rules/.",
  "status": "flagged"},
 {"owner": "Encounter Bot", "item": "Days 1 to 5 pages",
  "waiting_for": "Built with budget citations, the death-on-miss rule, quick runs, carry-on and zone color. Next: a Floor 2 (10-day) spec using the same script (use --allow-other-floors).",
  "status": "done"},
]

SRC_ADD = ["rules/70-encounter-budget-5e.json v0.1.0 and decisions/027-encounter-budget-v0-1-0.md (every figure cited by field path; guideline)",
           "decisions/026 Caleb rulings of ~10:00 PM and ~10:02 PM CT (Floor 3 = 20 days; a missed collapse is death)",
           "lore/drafts/floor1-zone-color.draft.md (Lore draft v0.1: optional read-aloud zone color)"]

def enc(s, eid): return next(e for e in s["encounters"] if e["id"] == eid)

def fill_encounters(n, s):
    E = lambda i: enc(s, "enc-d%02d-%02d" % (n, i))
    def en_fill(e, idx, zone, key, with_count=True):
        x = e["enemies"][idx]
        x["cr_slot"] = crr(zone, key)
        if with_count: x["count_slot"] = cnt(zone, key)
    def nc(e):
        e["cr_slot"] = copy.deepcopy(NONCOMBAT_CR); e["budget_slot"] = copy.deepcopy(NONCOMBAT_BUDGET)
    if n == 1:
        e = E(1); nc(e)
        e["loot_hooks"][0]["amount"] = cite("economy_audit.pull_expectations", "Welcome Box pulls")
        e["loot_hooks"][4]["amount"] = copy.deepcopy(VENDOR)
        e["proposed_achievements"][0]["reward_slot"] = reward("read_the_fine_print")
        e = E(2)
        en_fill(e, 0, "z07", "goblin-warrior"); en_fill(e, 1, "z07", "goblin-minion"); e["budget_slot"] = fit("z07")
        e["loot_hooks"][0]["amount"] = scalar(P + "fixed_encounters.z07.cash_dice_per_crawler", "Back Office cache is placed items; Greeter pocket change per Crawler", kind="text")
        e = E(3)
        en_fill(e, 0, "z08", "animated-armor"); en_fill(e, 1, "z08", "animated-flying-sword"); e["budget_slot"] = fit("z08")
        e["loot_hooks"][0]["amount"] = cite([P + "prices.zone_s_door_forcing", P + "prices.detour_tax"], "Quest item, not a credit source; missing it is priced at the paths")
        e["loot_hooks"][1]["amount"] = scalar(P + "prices.potion_of_healing_vendor.price", "Placed consumable: vendor value only")
        e = E(4)
        en_fill(e, 0, "wandering", "stirge"); e["budget_slot"] = fit("wandering")
        e["loot_note"] = scalar(P + "fixed_encounters.wandering.cash_dice_per_crawler", "Wandering Ticks carry no loot", kind="text")
        e["if_they_do_something_dumb"] = ("If the party insists on a Long Rest outside a saferoom, remind them a field rest can only be a Short Rest and the Ticks interrupt it (00-overview.md section 2 rule 7); "
            "the price is cited at {{b70:floors.1.prices.rest_without_saferoom}}. If they ignore the Lights-Out hour entirely, the Ticks show up anyway. Never a wipe.")
        e = E(5); nc(e)
        e["loot_hooks"][3]["amount"] = copy.deepcopy(BOXES)
        e["if_they_do_something_dumb"] = e["if_they_do_something_dumb"].replace("the cost is the rest-without-saferoom slot", "being unrested is the cost (a field rest is only a Short Rest; price at {{b70:floors.1.prices.rest_without_saferoom}})")
        s["day"]["proposed_achievements"][0]["reward_slot"] = reward("slow_learner")
    if n == 2:
        e = E(1); nc(e); e["loot_hooks"][3]["amount"] = copy.deepcopy(BOXES)
        e["proposed_achievements"][0]["reward_slot"] = reward("last_one_out")
        e["zone_color"] = {"tag": "inspired", "source": ZONE["src"], "lines": [{"text": t, "tag": PF} for t in ZONE[2]]}
        e = E(2)
        e["enemies"][0]["cr_slot"] = crr("z10", "skeleton")
        e["loot_hooks"][0]["amount"] = cite([P + "prices.zone_s_door_forcing", P + "prices.detour_tax"], "Quest item, not a credit source; missing it is priced at the paths")
        e["proposed_achievements"][0]["reward_slot"] = reward("detour_tax")
        e = E(3); nc(e)
        e["loot_hooks"][0]["amount"] = cite(P + "boxes", "n/a: a placed procedure, not a loot source")
        e["proposed_achievements"][0]["reward_slot"] = reward("early_withdrawal")
    if n == 3:
        e = E(1); nc(e)
        e["loot_hooks"][0]["note"] = "Vendor stock is shared floor-wide; price cited at {{b70:floors.1.prices.potion_of_healing_vendor.price}}."
        e["proposed_achievements"][0]["reward_slot"] = reward("read_the_fine_print")
        e = E(2)
        e["enemies"][0]["cr_slot"] = crr("z02", "giant-rat"); e["enemies"][1]["cr_slot"] = crr("wandering", "stirge")
        e["proposed_achievements"][0]["reward_slot"] = reward("last_one_out")
        e["zone_color"] = {"tag": "inspired", "source": ZONE["src"], "lines": [{"text": t, "tag": PF} for t in ZONE[3]]}
        e = E(3)
        e["enemies"][0]["cr_slot"] = crr("z10", "skeleton")
        s["day"]["proposed_achievements"][0]["reward_slot"] = reward("early_withdrawal")
        s["day"]["proposed_achievements"][1]["reward_slot"] = reward("slow_learner")
    if n == 4:
        e = E(1); nc(e)
        e["loot_hooks"][1]["amount"] = cite(P + "boxes", "n/a: services have ended, no ceremony")
        e["if_they_do_something_dumb"] = ("If someone tries to use the dead terminal, the screen shows OUT OF ORDER and a snarky line. If they try to rest here as if it were still a saferoom, "
            "it is a field rest: only a Short Rest, with the price cited at {{b70:floors.1.prices.rest_without_saferoom}} and no Long Rest. Never a wipe.")
        e["map_in_the_mind"]["hazards"][0] = "No services: no terminal, no vendors, no corkboard. It is no longer a saferoom (decision 026); the Green Room is the only saferoom."
        e = E(2)
        en_fill(e, 0, "wandering", "stirge"); e["budget_slot"] = fit("wandering")
        e["map_in_the_mind"]["hazards"][0] = "Red dim light; Ceiling Ticks interrupt a field rest per 00-overview.md section 2 rule 7. A field rest can only be a Short Rest."
        e["if_they_do_something_dumb"] = ("Resting outside the Green Room is allowed, but it is only a Short Rest: the price ({{b70:floors.1.prices.rest_without_saferoom}}) buys a quiet one and grants no Long Rest. "
            "If the party tries to Long Rest in the open anyway, the System refuses and the Ticks interrupt. Never a wipe.")
        zc = {"tag": "inspired", "source": ZONE["src"], "lines": [{"text": t, "tag": PF} for t in ZONE[4]],
              "gm_note": "GM note (from Lore's hook): a rest here can be interrupted by a dumb, loud, wrong-footed mob, which keeps the cost real without being cruel."}
        e["zone_color"] = zc
        e = E(3)
        e["enemies"][0]["cr_slot"] = crr("z10", "skeleton")
        e = E(4); nc(e); e["loot_hooks"][3]["amount"] = copy.deepcopy(BOXES)
        e["if_they_do_something_dumb"] = ("If they skip the rest and push on, the day rolls over at 24 in-game hours anyway; they start Day 5 unrested (a field rest is only a Short Rest, price cited at "
            "{{b70:floors.1.prices.rest_without_saferoom}}). If someone attacks another Crawler in the saferoom, the canon three-strikes freeze applies. Never a wipe.")
        s["day"]["proposed_achievements"][0]["reward_slot"] = reward("early_withdrawal")
        s["day"]["proposed_achievements"][1]["reward_slot"] = reward("detour_tax")
    if n == 5:
        e = E(1); nc(e)
        e = E(2); nc(e)
        e["loot_hooks"][0]["text"] = "Toll at the door: cited at {{b70:floors.1.prices.detour_tax}} (the Detour Tax, a missed Stairwell key only). House idea (inspired); a missed key costs, never wipes."
        e["loot_hooks"][0]["amount"] = party(P + "prices.detour_tax.party_toll_by_size", "Detour Tax party toll")
        e["proposed_achievements"][0]["reward_slot"] = reward("detour_tax")
        e = E(3)
        en_fill(e, 0, "z10", "ogre"); en_fill(e, 1, "z10", "skeleton"); en_fill(e, 2, "z10", "bugbear-warrior")
        e["budget_slot"] = fit("z10")
        e["budget_variant_b"] = party(P + "boss_variant_b_level1.xp_budget_total", "Variant B XP budget total at level 1")
        e["loot_hooks"][4]["amount"] = {"b70": [{"kind": "text", "path": P + "fixed_encounters.z10.cash_dice_per_crawler", "note": "Boss cash per Crawler"},
                                                {"kind": "cite", "paths": ["economy_audit.pull_expectations"], "note": "Silver Boss Box"}]}
        e["proposed_achievements"][0]["reward_slot"] = reward("hold_please")
        e = E(4); nc(e)
        e["loot_hooks"][0]["amount"] = cite(P + "boxes", "n/a: a placed procedure, not a loot source")
        e["proposed_achievements"][0]["reward_slot"] = reward("early_withdrawal")

for n in range(1, 6):
    fn = os.path.join(SPEC_DIR, "day-%02d.spec.json" % n)
    s = json.load(open(fn))
    m, c, d = s["meta"], s["clock"], s["day"]
    days = c["days"]
    s["budget_file"] = {"expected_sha256": "b794eeb7c7ce752768dc1b8a08a4833e1f35279aec87c12111f4610f8cedd736", "path": "rules/70-encounter-budget-5e.json", "version": "0.1.0"}
    m["version"] = "0.4" if n == 1 else "0.3"
    for x in SRC_ADD:
        if x not in m["sources"]: m["sources"].append(x)
    # summary: budget wording
    import re
    m["summary"] = re.sub(r"CR, budget, credits? and loot (?:amounts|figures)? ?(?:are|is) (?:empty )?slots? until rules/70-encounter-budget-5e\.json is filed\.",
        "CR, budget, credit and loot figures are cited from rules/70-encounter-budget-5e.json by field path (GM-adaptable guideline).", m["summary"])
    m["summary"] = m["summary"].replace("a missed collapse costs the Detour Tax, never a death.", "a missed collapse is death on every floor, with no Reprieve.")
    m["summary"] = re.sub(r" Collapse notices use Lore's draft wording; the final collapse is fixed and a missed collapse costs the Detour Tax, never a death\.",
        " Collapse notices use Lore's draft wording; the final collapse is fixed and a missed collapse is death on every floor, with no Reprieve.", m["summary"])
    if "empty slots until" in m["summary"] or "slots until" in m["summary"]:
        m["summary"] = re.sub(r"[^.]*slots until rules/70-encounter-budget-5e\.json is filed\.", " Figures are cited from rules/70-encounter-budget-5e.json by field path (GM-adaptable guideline).", m["summary"]).replace("  ", " ")
    # clock
    c["other_floors"]["3"] = 20
    c["authority"] = ("decisions/026-timed-floor-clock-override.md (Caleb; Syndicate confirmations of ~9:25, ~9:35 and ~9:45 PM CT; Caleb rulings of ~10:00 PM CT (Floor 3 = 20 days) and ~10:02 PM CT (a missed collapse is death on every floor)). "
                      "Overrides the old 'Floor clock: off' wording. The fixed final-collapse hour is a Syndicate default Caleb may veto. 00-overview.md section 2 rule 6 matches these rulings.")
    c["collapse_cost_slot"] = party(P + "prices.detour_tax.party_toll_by_size", "Detour Tax party toll (missed Stairwell key only)")
    c["rest_without_saferoom_slot"] = party(P + "prices.rest_without_saferoom.party_fee_by_size", "Rest-without-a-saferoom party fee (buys a quiet Short Rest, no Long Rest)")
    c["collapse_order_status"] = "confirmed per decision 026; the steps only remove hooks and services, and the Detour Tax is the only toll on the clock (a missed Stairwell key only)"
    c["collapse_miss"] = {
        "scope": "every floor, Floor 1 included", "tag": "canon-aligned (canon: a missed collapse ends the run)", "death": True, "reprieve_applies": False,
        "status": "Caleb ruling, decision 026 (~10:02 PM CT)",
        "text": "Any Crawler not at a stairwell when the floor collapses is dead. There is no Reprieve, no toll and no detour for it. Death rules follow Core section 6 (death is pretty much game over; loot stays lootable).",
        "stasis_counts": "Early-descent stasis (canon M-277) counts as reaching a stairwell.",
        "detour_tax_scope": "The Detour Tax now covers only a missed Stairwell key, never a missed collapse."}
    mk = s["stairwell_key"]["missing_key_cost"]
    mk["text"] = ("Missing the key is a COST, not an instant wipe: a detour (back to Z8 or Z6 while those still serve), the Detour Tax toll, or the loud keyless forcing. "
                  "Missing the collapse is a different matter: it is death (see the missed-collapse rule).")
    mk["toll_slot"] = party(P + "prices.detour_tax.party_toll_by_size", "Detour Tax party toll")
    s["stairwell_key"]["keyless_fee"] = party(P + "prices.zone_s_door_forcing.party_fee_by_size", "Zone S door forcing fee (party)")
    for w in s["stairwell_key"]["ways"]:
        if w["id"] == "key-terminal":
            w["price_slot"] = party(P + "prices.stairwell_key_terminal_bribe.party_price_by_size", "Terminal bribe (party price)")
            w["closes"] = "Lost on Day 4 when the Break Room and vendors lose service; the price is cited from the budget file."
    # rest options
    for r in d["rest_options"]:
        if "outside a saferoom" in r["option"].lower():
            r["note"] = FIELD_REST % FIELD_REST_TAIL["early" if n <= 3 else "late"]
        elif "Break Room" in r["option"]:
            r["note"] = BR_SAFE if n <= 3 else "Not a saferoom since it lost service on Day 4 (decision 026). The Green Room is the only saferoom to the end."
    if n == 5:
        for r in d["rest_options"]:
            if "Green Room" in r["option"]:
                r["note"] = ("The only saferoom, open to the end of the floor (inspired). Short Rests and the Long Rest are allowed, but the Long Rest never ends or skips the floor, "
                             "and the System cuts short any rest that would run past the collapse.")
    # notices
    if n >= 2:
        d["collapse_notice"]["text"] = NOTICE[n]
    if n == 5:
        d["early_descent"]["free_window"]["text"] = SIX
        d["floor_exit"] = {
            "system_line": {"text": MISS, "tag": PF},
            "gm_warning": {"text": "Table warning before anyone goes down: reach a stairwell before the collapse or you do not leave. Missing the collapse is death on every floor, with no Reprieve. Stasis from an early descent still counts as reaching a stairwell.", "tag": PF}}
        d["collapse_today"] = ("Only the Stairwell corridor stays: Z10, Z11 and Z S, plus the Z9 saferoom. The floor collapses at 24 in-game hours into Day {days} (fixed; hour {floor_hours} of the floor), "
                               "whatever the party is doing, and a Crawler not at a stairwell then is dead. Tagged inspired.")
    # gm warnings
    if n == 1: d["gm_warning"] = {"tag": "[GM-FACING]", "text": GM_WARN["start"], "lore_line": LORE_WARN}
    if n == 4: d["gm_warning"] = {"tag": "[GM-FACING]", "text": GM_WARN["pen"], "lore_line": LORE_WARN}
    if n == 5: d["gm_warning"] = {"tag": "[GM-FACING]", "text": GM_WARN["last"], "lore_line": LORE_WARN}
    # stall fallbacks
    dead = " A Crawler who is not at a stairwell when the floor collapses is dead, with no Reprieve (decision 026); keep the warning in view."
    if n == 1:
        d["stall_fallback"] = d["stall_fallback"].split(" A missed collapse is death on every floor and the Reprieve does not cover it")[0].split(" The Floor 1 Reprieve does not cover a missed collapse")[0] + " The Floor 1 Reprieve does not cover a missed collapse: that is death on every floor (decision 026), so say so at the start."
    elif n in (2, 3, 4):
        d["stall_fallback"] = d["stall_fallback"].split(" A Crawler still on the floor when it collapses")[0] + dead
    else:
        d["stall_fallback"] = ("If the party stalls, the countdown ticks, the Lights-Out hour arrives, and the System posts the six-hours warning. In the last six hours the descent is free, so a patient party simply waits at the stairwell if they are not ready to fight. "
            "If they cannot or will not fight the boss, the Z S toll door and the boss cheese routes are open; a missed key is only the detour or the Detour Tax (cited at {{b70:floors.1.prices.detour_tax}}). "
            "The collapse is fixed and a Long Rest does not move it. A Crawler not at a stairwell when it comes is dead, with no Reprieve; read the missed-floor line and warn the table before anyone dawdles.")
        e = enc(s, "enc-d05-01")
        e["if_they_do_something_dumb"] = ("If the party delays, the countdown reminds them and the Lights-Out hour arrives. A Long Rest here is allowed, but it never ends or skips the floor, and the System cuts short any rest that would run past the collapse. "
            "If they miss the collapse, it is death for anyone not at a stairwell: no Reprieve, no toll, no detour. Say so before they settle in.")
        e = enc(s, "enc-d05-04")
        e["if_they_do_something_dumb"] = ("If a Crawler tries to descend earlier than the last six hours, run the early-descent block (stasis); the GM logs any override. "
            "Before anyone goes down, give the floor exit warning: missing the collapse is death on every floor, with no Reprieve. "
            "If a Crawler is still on the floor at the collapse, read the missed-floor line: they are dead.")
    fill_encounters(n, s)
    for e in s["encounters"]:
        e["quick_run"] = copy.deepcopy(QUICK[e["id"]])
        cc = copy.deepcopy(CARRY[e["id"]])
        co = {"changes": cc["changes"], "gm_tracks": cc["gm_tracks"]}
        if cc.get("later"): co["changes"][-1]["later_note"] = cc["later"]
        e["carry_on"] = co
    # budget table
    rows = [("Detour Tax, party toll (missed Stairwell key only)", party(P + "prices.detour_tax.party_toll_by_size")),
            ("Stairwell key, terminal bribe (party price)", party(P + "prices.stairwell_key_terminal_bribe.party_price_by_size")),
            ("Zone S door forcing fee (party)", party(P + "prices.zone_s_door_forcing.party_fee_by_size")),
            ("Rest without a saferoom (party fee; buys a quiet Short Rest, no Long Rest)", party(P + "prices.rest_without_saferoom.party_fee_by_size")),
            ("Potion of Healing, vendor price (shared floor stock)", scalar(P + "prices.potion_of_healing_vendor.price")),
            ("Daily XP guidance and caps", cite(P + "xp.by_party_size"))]
    if n == 5:
        rows.append(("Boss Variant B XP budget total at level 1", party(P + "boss_variant_b_level1.xp_budget_total")))
    d["budget_table"] = [dict(label=l, **copy.deepcopy(r)) for l, r in rows]
    s["pending_inputs"] = copy.deepcopy(PENDING)
    json.dump(s, open(fn, "w"), indent=2, ensure_ascii=False); open(fn, "a").write("\n")
print("patched")
