#!/usr/bin/env python3
"""One-shot dev patch (kept for the record): applies decision 026 final rulings + Lore's collapse-notice draft
to floors/f01/day-0N.spec.json. Run from floors/f01/. Pure local, no model calls.
Current ruling (Caleb, decision 026 ~10:02 PM CT; decisions/028): missing the floor collapse = the Crawler is dead, game over, on EVERY floor including Floor 1,
no Reprieve; NPCs and the AI go into stasis and lose nothing. The Detour Tax covers only a missed Stairwell key. This script no longer writes any
soft-penalty missed-collapse default."""
import json, copy

PT = "proposed by Encounter Bot, framed by Lore, reward = slot for Syndicate"
REW = "[REWARD: slot for Syndicate; snark-only allowed]"
PF = "[PLAYER-FACING]"
def pa(name, trigger, narration=None, canon_ref=None):
    d = {"name": name, "trigger": trigger, "tag": PT, "reward_slot": REW}
    if narration:
        d["narration"] = narration; d["narration_tag"] = PF
    if canon_ref:
        d["canon_ref"] = canon_ref
    return d
HP = pa("Hold Please", "Talk Dean Thudd down without a fight.", "You waited on hold and won. The System is baffled.")
LOO = pa("Last One Out", "Hold a closing zone until the party is clear, then reach the Green Room.", "Someone had to be the last one out, and it turned out to be you.")
DT = pa("Detour Tax", "Pay the missed-key toll and still descend.", "You paid the fee and got there anyway. Efficient.")
EW = pa("Early Withdrawal", "Choose early-descent stasis.", "You left early. The floor is still here. So are you, in a closet.",
        {"ledger_id": "A-151", "use": "Parallel canon: 'The Early Bird Gets To Squirm'."})
RFP = pa("Read the Fine Print", "Use the Break Room terminal bribe route.")
SL = pa("Slow Learner", "Clear every Day 1 to 3 encounter before descending.")

NOTICE = {
 2: "ATTENTION, CRAWLERS. The outer zones are now closed for renovation. By \"renovation\" we mean \"gone.\" Anything you left in them is now a lesson. The way forward remains open. You're welcome.",
 3: "UPDATE. The middle of the floor is joining the outer parts in the afterlife. Loot and services there have ended. Your route is untouched, because we want you to see what's next. Sadly.",
 4: "NOTICE. The Break Room is now off duty. The vending terminal has gone to lunch and will not return. Resting there is no longer recommended. The Green Room remains open, for reasons of mercy and liability.",
 5: "FINAL-MORNING REMINDER. In {hours} hours this floor collapses, with you or without you. Only the corridor is left. The stairwell is down the hall. Please do not make us say it twice.",
}
SIX = "SIX HOURS REMAIN. Anyone taking the stairs from this point descends freely. Anyone who went earlier is still napping in the stairwell. Hurry up."
MISS = "The floor has closed. Your attendance has been noted and your tenure has been terminated. We will not be sending flowers."
TOLL = "[DETOUR TAX (missed Stairwell key only): toll amount; cite rules/70-encounter-budget-5e.json when filed]"
SIDELINE = ("A Crawler in stasis is out of the floor, not out of the game. Their player gets short sideline System scenes until the party arrives on Floor 2: "
            "waiting-room gags, and a vote on the party's next move. The GM decides how much weight the vote carries, keeps each scene brief, and cuts back to the main table. "
            "(Syndicate ruling, decision 026.)")

PENDING = [
 {"owner": "Syndicate", "item": "rules/70-encounter-budget-5e.json (not yet filed)",
  "waiting_for": "Every CR, XP/encounter budget, enemy count and credit amount on these pages, including the Detour Tax toll, the key price, vendor prices, the Zone S toll and the rest-without-saferoom price. All appear as bracketed slots.",
  "status": "waiting"},
 {"owner": "Caleb", "item": "Veto window on Syndicate's Floor 1 defaults (decision 026, ~9:45 PM CT)",
  "waiting_for": "The final collapse is fixed at 24 in-game hours into the last day and a Long Rest never ends or skips the floor (Syndicate default, Caleb may veto). The missed-collapse rule is not open: Caleb ruled (decision 026, ~10:02 PM CT; decisions/028) that missing the floor collapse is death on every floor, Floor 1 included, with no Reprieve; NPCs and the AI go into stasis.",
  "status": "open (fixed-collapse default applies)"},
 {"owner": "Day-count field", "item": "clock.days",
  "waiting_for": "Floor 1 is 5 (field set), Floor 2 is 10, Floor 3 is 15 or 20 (Caleb to pick). Page text takes the day count from the field; nothing is hard-coded.",
  "status": "Floor 1 set; Floor 3 open (Caleb)"},
 {"owner": "Lore", "item": "Canon table and collapse-notice draft",
  "waiting_for": "Received and used: /workspace/dcc-lore/tables/canon-floor-1.json (rebuilt; sha256 and ledger version recorded in the page meta) and /workspace/dcc-lore/drafts/floor1-collapse-notices.draft.md (draft v0.1: Day 2 to 5 notices, six-hours warning, missed-floor line, achievement frames). If Lore edits either, re-run the script.",
  "status": "received"},
 {"owner": "Syndicate", "item": "Rewards for the six proposed achievements; ACH rows for canon A-044, A-151 and A-139",
  "waiting_for": "Each proposed achievement (Hold Please, Last One Out, Early Withdrawal, Detour Tax, Read the Fine Print, Slow Learner) has a reward slot; snark-only is allowed and the floor caps apply. A-044/A-151/A-139 stay canon references only until ACH rows are added (A-044 is not attainable on Floor 1; A-151 only in the stasis form).",
  "status": "waiting (backlog)"},
 {"owner": "Syndicate", "item": "00-overview.md section 2 rule 6 wording",
  "waiting_for": "Decision 026 (~10:02 PM CT) governs: fixed collapse, a missed collapse is death with no Reprieve, and the Detour Tax covers only a missed Stairwell key. Encounter Bot may not edit the overview.",
  "status": "settled"},
 {"owner": "Encounter Bot", "item": "Days 1 to 5 pages",
  "waiting_for": "Built and updated with the final rulings. Next: a Floor 2 (10-day) spec using the same script (use --allow-other-floors).",
  "status": "done"},
]

def enc(s, eid):
    return next(e for e in s["encounters"] if e["id"] == eid)
def add(e, *items):
    e.setdefault("proposed_achievements", []).extend(copy.deepcopy(i) for i in items)

BR_SAFE = "Honest saferoom through Day 3; it stops being a saferoom when it loses service on Day 4 (decision 026)."
for n in range(1, 6):
    fn = "day-%02d.spec.json" % n
    s = json.load(open(fn))
    m, c, d = s["meta"], s["clock"], s["day"]
    m["version"] = "0.3" if n == 1 else "0.2"
    src = "/workspace/dcc-lore/drafts/floor1-collapse-notices.draft.md (Lore draft v0.1: collapse notices, six-hours warning, missed-floor line, achievement frames)"
    if src not in m["sources"]:
        m["sources"].append(src)
    if n > 1 and "Lore's draft notices" not in m["summary"]:
        m["summary"] += " Collapse notices use Lore's draft wording; the final collapse is fixed and a missed collapse is death on every floor, with no Reprieve."
    # --- clock
    c["day_ends"] = ("At the party's saferoom Long Rest, or at 24 in-game hours if they have not had one (the System rolls the day over anyway). "
                     "The last day is different: the floor collapses at 24 in-game hours into Day {days} no matter what.")
    c["authority"] = ("decisions/026-timed-floor-clock-override.md (Caleb; Syndicate confirmations of ~9:25 PM, ~9:35 PM and ~9:45 PM CT recorded there; the ~9:45 PM rulings are defaults Caleb may veto). "
                      "Overrides the old 'Floor clock: off' wording. A missed collapse is death on every floor with no Reprieve (Caleb, ~10:02 PM CT; decisions/028); decision 026 governs over any older wording.")
    for k in ("collapse_order_slot", "final_day_end_slot", "collapse_miss_slot", "break_room_status_slot", "stasis_table_slot"):
        c.pop(k, None)
    c["collapse_order_status"] = "confirmed per decision 026; the steps only remove hooks and services, and the Detour Tax is the only toll on the clock"
    c["collapse_cost_slot"] = TOLL
    c["collapse_order"][3]["event"] = "The Break Room (Z6) and vendors lose service; the Break Room is no longer a saferoom."
    c["collapse_order"][4]["event"] = "Only the Stairwell corridor stays; the floor collapses at 24 in-game hours of this day."
    c["closed_zone_rule"] = ("Closed zones lose their loot and achievement hooks and the System announces it with a snarky notice (Lore's wording on the day pages). "
                             "Zone 9 (The Green Room) saferoom stays open to the end (house exception, inspired).")
    c["final_collapse"] = {
        "hour_of_last_day": 24, "tag": "inspired", "status": "Syndicate default, decision 026; Caleb may veto",
        "text": "The final collapse comes at a FIXED moment: 24 in-game hours into Day {days} (hour {floor_hours} of the floor). A Long Rest never ends the floor and never skips it; the System cuts short any rest that would run past the collapse."}
    c["collapse_miss"] = {
        "scope": "every floor, Floor 1 included", "tag": "canon-aligned (canon: a missed collapse ends the run)", "death": True, "reprieve_applies": False,
        "status": "Caleb ruling, decision 026 (~10:02 PM CT); decisions/028",
        "text": "Any Crawler not at a stairwell when the floor collapses is dead, game over. There is no Reprieve, no toll and no detour for it. NPCs and the AI go into stasis and lose nothing.",
        "stasis_counts": "Early-descent stasis counts as reaching a stairwell.",
        "detour_tax_scope": "The Detour Tax covers only a missed Stairwell key, never a missed collapse."}
    c["saferoom_rule"] = {
        "only_saferoom": "z09", "break_room_not_saferoom_from_day": 4,
        "text": "The Break Room (Z6) is a saferoom through Day 3 and stops being one when it loses service on Day 4 (Syndicate ruling, decision 026). From then on the Z9 Green Room is the only saferoom, open to the end of the floor (tagged inspired)."}
    c["achievement_caps"] = ("Floor caps still apply: the soft cap is 2 to 3 achievement boxes per Crawler per floor (Caleb's ruling); on Floors 1 and 2 the Silver ceiling and one Story Box per floor hold. "
                             "Rewards are tailored by the GM and snark-only is allowed; the proposed achievements are a seed list at GM discretion.")
    # --- key
    mk = s["stairwell_key"]["missing_key_cost"]
    mk["text"] = ("Missing the key is a COST, not an instant wipe: a detour (back to Z8 or Z6 while those still serve), the Detour Tax toll, or the loud keyless forcing. "
                  "Missing the collapse is a different matter: it is death (see the missed-collapse rule). The Detour Tax covers only a missed Stairwell key.")
    mk["toll_slot"] = TOLL
    mk.pop("detour_slot", None)
    # --- pending
    s["pending_inputs"] = copy.deepcopy(PENDING)
    # --- rest options: Break Room wording
    for r in d["rest_options"]:
        if "Break Room" in r["option"]:
            if n <= 3:
                r["note"] = BR_SAFE
            else:
                r["note"] = ("Not a saferoom since it lost service on Day 4 (decision 026). The Green Room is the only saferoom to the end.")
        if "outside a saferoom" in r["option"] and n >= 4:
            r["note"] = ("Allowed outside the Green Room, but a Long Rest is interrupted by Ceiling Ticks (00-overview.md section 2 rule 7) and the Lights-Out roll applies. "
                         "Cost: [REST-WITHOUT-SAFEROOM COST: priced in rules/70-encounter-budget-5e.json when filed].")
    # --- collapse notice & early-descent
    if n >= 2:
        d["collapse_notice"] = {"text": NOTICE[n], "tag": PF, "canon_tag": "inspired",
                                "status": "Lore draft v0.1 (floor1-collapse-notices.draft.md), house wording; Lore may still edit"}
        if n == 5:
            d["collapse_notice"]["hours_note"] = "The GM fills {hours} with the in-game hours left until the fixed collapse when reading this aloud."
        ed = d["early_descent"]
        ed.pop("slots", None)
        ed["sideline_note"] = SIDELINE
    # --- stall suffixes
    miss_stall = " A Crawler still on the floor when it collapses is dead, with no Reprieve (decision 026); keep the warning in view."
    if n == 1:
        d["stall_fallback"] = d["stall_fallback"].split(" Do not rely on the Floor 1 Reprieve")[0] + (
            " A missed collapse is death on every floor and the Reprieve does not cover it (decision 026); say so at the start.")
    elif n in (2, 3, 4):
        d["stall_fallback"] += miss_stall
    # --- per-day specifics
    if n == 1:
        add(enc(s, "enc-d01-01"), RFP)
        d["proposed_achievements"] = [copy.deepcopy(SL)]
    if n == 2:
        add(enc(s, "enc-d02-01"), LOO); add(enc(s, "enc-d02-02"), DT); add(enc(s, "enc-d02-03"), EW)
    if n == 3:
        add(enc(s, "enc-d03-01"), RFP); add(enc(s, "enc-d03-02"), LOO)
        d["proposed_achievements"] = [copy.deepcopy(EW), copy.deepcopy(SL)]
        e = enc(s, "enc-d03-02")
        e["enemies_note"] = e["enemies_note"].replace("House idea (inspired):", "Confirmed by Syndicate (decision 026, ruling 5), tagged inspired:")
    if n == 4:
        d["proposed_achievements"] = [copy.deepcopy(EW), copy.deepcopy(DT)]
        e = enc(s, "enc-d04-01")
        e["map_in_the_mind"]["hazards"][0] = "No services: no terminal, no vendors, no corkboard. It is no longer a saferoom (decision 026); the Green Room is the only saferoom."
        e["if_they_do_something_dumb"] = ("If someone tries to use the dead terminal, the screen shows OUT OF ORDER and a snarky line. If they try to rest here as if it were still a saferoom, "
            "treat it as the rest-without-saferoom case: [REST-WITHOUT-SAFEROOM COST: priced in rules/70-encounter-budget-5e.json when filed]. Never a wipe.")
        e = enc(s, "enc-d04-04")
        e["if_they_do_something_dumb"] = e["if_they_do_something_dumb"]
    if n == 5:
        d["collapse_today"] = ("Only the Stairwell corridor stays: Z10, Z11 and Z S, plus the Z9 saferoom. The floor collapses at 24 in-game hours into Day {days} (fixed; hour {floor_hours} of the floor), "
                               "whatever the party is doing. Tagged inspired.")
        d["tomorrow_notice"] = {"text": "FINAL NOTICE. The floor collapses at the end of today's last hour, rested or not. A nap will not hold it, and the System will cut your rest short.", "tag": PF}
        ed = d["early_descent"]
        ed["free_window"] = {"text": SIX, "tag": PF}
        d["floor_exit"] = {
            "system_line": {"text": MISS, "tag": PF},
            "gm_warning": {"text": "Table warning before anyone goes down: reach a stairwell before the collapse or you do not leave. Missing the collapse is death on every floor, with no Reprieve. Stasis from an early descent still counts as reaching a stairwell.", "tag": PF}}
        for r in d["rest_options"]:
            if "Green Room" in r["option"]:
                r["note"] = ("The only saferoom, open to the end of the floor (inspired). Short Rests and the Long Rest are allowed, but the Long Rest never ends or skips the floor, "
                             "and the System cuts short any rest that would run past the collapse.")
        e = enc(s, "enc-d05-01")
        e["if_they_do_something_dumb"] = ("If the party delays, the countdown reminds them and the Lights-Out hour arrives. A Long Rest here is allowed, but it never ends or skips the floor, and the System cuts short any rest that would run past the collapse. "
            "If they miss the collapse, it is death for anyone not at a stairwell: no Reprieve, no toll, no detour. Say so before they settle in.")
        add(enc(s, "enc-d05-02"), DT); add(enc(s, "enc-d05-03"), HP); add(enc(s, "enc-d05-04"), EW)
        e = enc(s, "enc-d05-04")
        e["if_they_do_something_dumb"] = ("If a Crawler tries to descend earlier than the last six hours, run the early-descent block (stasis); the GM logs any override. "
            "Before anyone goes down, give the floor exit warning (floor_exit): missing the collapse is death on every floor, with no Reprieve. "
            "If a Crawler is still on the floor at the collapse, read the missed-floor line: they are dead.")
        d["stall_fallback"] = ("If the party stalls, the countdown ticks, the Lights-Out hour arrives, and the System posts the six-hours warning. In the last six hours the descent is free, so a patient party simply waits at the stairwell if they are not ready to fight. "
            "If they cannot or will not fight the boss, the Z S toll door and the boss cheese routes are open. The collapse is fixed: a Long Rest does not move it. "
            "A Crawler still on the floor when it collapses is dead, with no Reprieve (decision 026). "
            "Warn the players at the floor exit that missing the collapse is death on every floor.")
    json.dump(s, open(fn, "w"), indent=2, ensure_ascii=False); open(fn, "a").write("\n")
print("patched")
