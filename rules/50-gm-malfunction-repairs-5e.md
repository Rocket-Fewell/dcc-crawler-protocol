# GM Malfunction Repairs (5e Overlay)
Owner: Syndicate | Status: draft | Version: 0.1.4 | Updated: 2026-10-04
Summary: Proposed rulings for the eight undefined items in section 6 of DCC Lore's GM Malfunction player guide: credit costs, DCs, quest and retrieval specifics, failure penalties, how a Tribute is judged, what counts as a "Busted" callout, stacking, and whether the Patch Ticket uses Stress. Quirk-agnostic: every ruling works against any sealed roll. One-page table of the five repairs in section 2.
Depends on: dcc-lore/guides/gm-malfunction-player-guide.md v0.1 (ladder, Stress, five repairs; wins on anything it already defines), rules/10-core-rules-5e.md v0.2.16 (§3.9 credit multiplier x1/x5/x20/x50, §5.10 vendors, §6.4 revive fees for scale), rules/40-loot-deck-spec-5e.md v0.1.7 (§3.2 credit ranges and audit hint), gm-notes/00-gm-principles.md (fair play, opt-outs, address rule), gm-notes/20-gm-persona.md (voice split). Consumers: AI GM (runs the repairs), DCC Lore (updates the player guide after approval), Borent (any state fields: Repair Offset, Rapport), the Accountant (credit audit).

> **Status:** DRAFT v0.1.4. Nothing here is LOCKED. **Every number is HOUSE and tunable** unless it is quoted from the Lore guide or another file (those are marked "(guide)" or "(core)"). **Project:** *Crawler Protocol: Season Zero*, private fan RPG inspired by *Dungeon Crawler Carl*.
> **Changelog:** v0.1.1: Patch base 300 to 500 per Accountant review; Floor 4 300 was only about a low Gold box.
> **Changelog v0.1.2 (2026-10-04):** Busted is a spontaneous callout, with no prompts and no fees, per Lore + Caleb.
> **Changelog v0.1.3 (2026-10-04):** Busted guard added (a call is valid only in a scene where the GM logged a tell; a refusal never consults the sealed roll); §1.2 states that box credit pulls get no floor multiplier while repair prices (System fees) do; party size corrected to four; dependency pointers refreshed.
> **Changelog v0.1.4 (2026-10-04):** tell-shown rule written out in §6.2 (the GM logs the tell with `state.py repair-log tell` when it is shown, before any call is graded; matches `tools/repair_log.py` and gm-notes/00-gm-principles.md); two-Crawler line added under §10 Q2; dependency pointers refreshed (core v0.2.16, rules/40 v0.1.7). No price, DC or lockout changed.
> **Sealed-roll hygiene:** written without opening `gm-notes/secret/` or anything in `sessions/`. It names no quirk, fixation, tic, tell or table entry, and it needs none. If a ruling below only works against some quirks, that is a bug in this file; tell Syndicate.
> **Stress note:** the Stress mechanic (-1..+1, effective level = ladder + Stress, clamped 0-5) exists only in the Lore guide; core rules v0.2.16 has no Stress section. §1 below treats the guide as the definition and adds one track beside it (the Repair Offset, see §1.1). Core should get a short pointer when Caleb approves.
> **Address rule:** players are Crawlers (Caleb, 2026-10-04).
> **Voice:** rulings are plain; the flavor lines are the System ([SYSTEM]: smooth, smug, bureaucratic, bored). The GM ([GM]) reacts in his own wet, delighted voice. Both stay in fair play: the unit never touches dice, DCs, damage, HP, saves, initiative or rules text (guide §3).

## Contents
1. Shared machinery (money scale, DC bands, the Repair Offset, Rapport)
2. One-page summary table
3. Tribute (question 1)
4. Patch Ticket (questions 3 and 4)
5. Lobotomizer (question 5)
6. Therapy Session and the "Busted" callout (question 6)
7. Sabotage (question 7)
8. Stacking, repeats, lockouts (questions 2, 4 and 8)
9. Fair-play checklist, tuning notes, change list for Lore
10. Open questions for Caleb

---

## 1. Shared machinery

### 1.1 Effective level with a Repair Offset (answers guide Q2 and Q4)
The guide says effective level = ladder level + Stress, clamped 0-5, Stress capped at -1..+1. To keep Tribute useful beside the permanent fixes, this file adds one more term:

**Effective level = clamp( ladder level + Stress + Repair Offset, 0, 5 )**. **HOUSE**

- **Stress** (guide): one track, -1..+1, set by Tribute, refused or mocked Spite Moves, management overrules, and Sabotage. Two Stress sources never add past the cap, and a +1 and a -1 cancel to 0 (a Tribute and a Sabotage on one floor = 0; the System calls it "a wash, like your marriage").
- **Repair Offset** (new): the sum of active Patch Ticket (-1), Lobotomizer (-2), Therapy Session (-1). **Capped at -3 in total.** **HOUSE**
- So the best case is -4 (Offset -3, Stress -1). On Floor 12+ (ladder 5) that is still Level 1: the unit never goes fully Stable down there, which the table should regard as a feature.
- Repairs never re-roll or rewrite the sealed roll (guide). The Offset only changes which level the unit behaves at.

### 1.2 Money scale
Prices are written at Floor-1 scale and multiplied by **M**, the core §3.9 credits multiplier **(core)**:

| Floors | M |
|---|---:|
| 1-4 | x1 |
| 5-9 | x5 |
| 10-14 | x20 |
| 15-18 | x50 |

**Fees versus box pulls (Lore, with Caleb's delegation, 2026-10-04).** Repair prices are System fees, so they multiply by M. Box credit pulls do **not** get the floor multiplier on top of their tier ranges (rules/40 §3.2). Achievement rewards and System fees (repairs, Story Box buyback, crafting prices) keep it.

Cost lines below are **per party** (one shared pot, any split) unless stated. Benchmarks for sanity: loot spec §3.2 audit hint puts box credit value at roughly 300-1,000 per Crawler per floor on F1-2 (flag above 1,500), Gold box credit pulls are 500-3,000, Platinum 5,000-30,000; core §6.4 revive Licensing Fees are flat 5,000 / 15,000 / 40,000 / 100,000. Repair prices aim at: Tribute is pocket change, Patch is a real bite, Lobotomizer sits near a first-tier revive, Therapy is the cheap permanent fix the guide promises.

**Party size:** the table plays four Crawlers (decision 013). Credit prices do not scale with party size. Encounters and challenges scale through the normal 5e encounter budget for the party's level and headcount.

### 1.3 DC bands (all HOUSE)
Fixed per floor band, never adjusted by the unit's mood.

| Band | Floors | Tribute effort DC | Patch quest DC | Lobotomizer DC |
|---|---|---:|---:|---:|
| A | 3-6 (Lobotomizer starts F6) | 12 | 13 | 15 |
| B | 7-11 | 14 | 15 | 17 |
| C | 12+ | 16 | 17 | 19 |

### 1.4 Rapport (new, small, HOUSE)
A hidden GM-side counter, 0-10, starting at 3, that answers the guide's "kept the unit on good terms overall" for Therapy. Published as four words only, shown on request: **Frosty 0-2 | Cool 3-5 | Warm 6-8 | Cozy 9-10**.

| Event | Rapport |
|---|---:|
| Tribute that lands (Standing Ovation) | +1 |
| Accept a Spite Move with good grace (laugh, do the bit; once per floor) | +1 |
| Finish a Patch Ticket | +1 |
| Spite Move refused or mocked (also Stress +1, guide) | -1 |
| Tribute Boo with a natural 1 | -1 |
| Sabotage | -2 |

Rapport is capped 0-10, changes no dice, and is logged in the open [ROLL]-style log with the word band so Crawlers can check the GM is not fudging it. Opt-outs always win: a Crawler who opted out of a joke can never lose Rapport by refusing it.

---

## 2. One-page summary table

Costs are per party at Floor-1 scale, multiplied by M (§1.2). "Check" are Crawler rolls at the band DC (§1.3). All numbers HOUSE.

| Repair | Unlocked | Cost (x M) | Check | Failure | Effect on the ladder L0-L5 |
|---|---|---|---|---|---|
| **Tribute** | Any floor; useful F3+ (F1-2 refunded, nothing to fix) | 50 credits, or an item of that credit_value, or a free performance at DC +2. Once per floor. | Presenter Cha (Performance/Persuasion/Deception), DC 12/14/16. Judged by a hidden Fit tier set before the roll (§3). | Offering is spent. Boo = Stress +1 unless you beat DC by 5. Applause or a miss = nothing. | Stress -1 for the floor. L0..L5 -> L0, L0, L1, L2, L3, L4. |
| **Patch Ticket** | Floor 4+; needs a sponsor or Syndicate contact | 500 + 25% per earlier Patch (max +100%) | Three parts at DC 13/15/17: Fetch a Core (3 successes before 3 failures), Defense scene (5 rounds), Reboot (2 of 3). | Part 1: Core cracks, 25% re-fee. Part 2: tech down, 50% refund, retry next floor. Part 3: Stress +1 this floor, fee kept, redo from Part 1. | Repair Offset -1 for 2 floors, then reverts. L0..L5 -> L0, L0, L1, L2, L3, L4. Unit sulks one scene. |
| **Lobotomizer** | Floor 6+; technician and a risky retrieval | 1,000, paid at install | Three stages at DC 15/17/19: Find (group check), Get (4 successes before 3 failures, then a High encounter), Install (one volunteer, others Help). | Find: finder's fee retry. Get: Net lost, 20% reclaim fee, retry next floor. Install: Misfire: Net lost, 25% disposal fee, Stress +1 for the floor, one Spite Move at the thrower. | Repair Offset -2, permanent. L0..L5 -> L0, L0, L0, L1, L2, L3. Spite budget -1 per floor (min 0). |
| **Therapy Session** | Floor 8+ | 250 credits x M per party | Route A: Rapport Warm or Cozy. Route B: a spontaneous "Busted" callout (§6). No DC; it is a purchase. | Wrong callout: no penalty; one callout per Crawler per scene and wrong text cannot repeat. Right callout opens Route B for the party. | Repair Offset -1, permanent. L0..L5 -> L0, L0, L1, L2, L3, L4. No new mechanical tells; obsession may be narrated openly. |
| **Sabotage** | Any floor; table consensus | 0 credits. Pays 50 (Hazard Pay) plus a Crowd Pop. | None to start; the Spite Move that follows is an ordinary scene. | Rapport -2, saboteur's personal blowback (§7). | Stress +1 for the floor (not +2). L0..L5 -> L1, L2, L3, L4, L5, L5. |

Combined worst-case line: Lobotomizer + Therapy + Patch is -4, capped at -3 on the Offset; add a Tribute and you are at -4 from ladder. Sabotage and Tribute cancel on the same floor.

---

## 3. Tribute (RP-01)

> **[SYSTEM]** "A Tribute is a gift offered in the hope of affection. Management reminds you that affection is not guaranteed and has been itemized."

### 3.1 Cost (guide Q1)
- **Price:** 50 credits x M per party. **HOUSE**
- **Pay in kind:** an item worth at least that much by its loot-card `credit_value` (the System values it at full price, not the usual half). **HOUSE**
- **Free performance:** no price, but the effort DC is +2 and the performer must give an actual in-character bit at the table.
- **Once per floor.** The offering is spent whatever happens.
- **Floors 1-2:** no malfunction to fix. The System takes the offering, laughs, and refunds it ("Management is touched and confused").

### 3.2 How a Tribute is judged (guide Q1)
Two ingredients. The Crawlers control the first; the sealed profile (via observable behavior only) decides the second.

1. **Effort roll (open):** one Crawler presents; others may Help (Advantage). Charisma (Performance, Persuasion or Deception), DC 12 / 14 / 16 by band. A natural 20 counts as beating the DC by 5; a natural 1 counts as missing by 5. **HOUSE**
2. **Fit tier (committed first):** before any dice, the GM writes the Fit tier into the sealed Fit Log (§10, Q6): **Standing Ovation, Polite Applause or Boo**. It is chosen like this, which works for any quirk because it uses only what the table has seen:
   - **Standing Ovation:** the offering clearly speaks to what the unit has *visibly* fixated on in the last two floors (the thing the trend lines in the guide would point at).
   - **Boo:** only if the offering runs against something the unit has visibly flinched at on screen at least once, with that flinch logged. No on-screen flinch, no Boo. This keeps the guide's "you are not told in advance" without making it a trap.
   - **Polite Applause:** everything else.
   The Fit tier never changes the DC. It changes what the roll buys.

| Fit tier | Roll beats DC by 5+ | Roll meets DC | Roll misses DC |
|---|---|---|---|
| **Standing Ovation** | Stress -1 for the floor, Rapport +1, half the credits come back (Encore Rebate) | Stress -1 for the floor, Rapport +1 | Nothing. "Wonderful idea. Disgraceful execution." |
| **Polite Applause** | Stress -1 for the floor | Nothing, but a hint line: a reaction the Crawlers can watch | Nothing |
| **Boo** | Nothing ("Nice recovery") | Stress +1 for the floor | Stress +1 for the floor; on a natural 1, Rapport -1 |

Guide check: "success = Stress -1", "offensive = Stress +1 instead", once per floor, no advance warning. The only additions are the roll and the hint line.

### 3.3 Feral meltdown ("Calm Down")
At Level 5, a Tribute can end a meltdown (guide). Ruling: it costs no credits, does not use up the floor's once-per-floor Tribute, and needs an effort roll at the band DC +2 (a sincere apology instead of a gift also works at the same DC). Success ends the meltdown; failure lets it run one more round. No Stress or Rapport change either way. **HOUSE**

---

## 4. Patch Ticket (RP-02)

> **[SYSTEM]** "Your Maintenance Window is confirmed. Please take a number. The number is a quest. Please do not take the technician's number."

### 4.1 Unlock, price, duration (guide Q3)
- **Floor 4+**, needs a sponsor or Syndicate contact (guide): any active sponsor deal, a Syndicate Voucher, or a sponsor-granted favor counts. **HOUSE**
- **Price:** 500 credits x M per party, paid when Part 1 is accepted, plus 25% per Patch the party has bought before (max +100%). F4: 500; F5-9: 2,500; F10-14: 10,000; F15+: 25,000. **HOUSE**
- **Duration:** covers the floor on which Part 3 finishes and the next floor, then reverts when the party descends past it (guide: 2 floors). One active Patch at a time.
- **Where the technician is:** a Syndicate Technician NPC shows up at the first saferoom terminal on any floor 4+ once the party meets the sponsor/contact condition, listed on the terminal as "Maintenance Window (1)". The System refuses to say where he was before. **HOUSE**

### 4.2 The three-part quest (guide Q3)
All checks use the Patch DC for the floor band (13 / 15 / 17). All scales by party level.

1. **Fetch a Stabilizer Core.** The Core sits in a back-of-house location the GM places on that floor (a hazard room, not a boss). Skill challenge: **3 successes before 3 failures**, each Crawler using a different skill or tool. *Failure (3 misses):* the Core cracks. A replacement costs a 25% re-fee, and the party tries again after a long rest.
2. **Defense scene.** Hold the technician for **5 rounds** while the reboot spins up. Threat: a Moderate encounter for the party (2024 DMG budget), Hard from the second Patch onward. The technician is AC 13, HP 5 x the floor number. At most half of the enemies' attacks may be aimed at him (the GM rolls openly). *Failure (technician drops to 0 HP):* he goes offline. 50% of the fee comes back; the Core is kept; the defense scene is rerun for free on the next floor.
3. **Reboot the unit.** A three-step bench job: **2 of 3 successes**, Crawlers pick any three different skill or tool checks (examples: Sleight of Hand, Arcana, Investigation, Thieves' or Tinker's tools). *Failure:* the unit restarts in Safe Mode and sulks. **Stress +1 for the floor**, the fee is kept, and the quest restarts from Part 1 on a new Core.

**Reward:** the achievement "Have You Tried Turning It Off And On Again?" = Bronze box (core §4). Rapport +1. **HOUSE**

### 4.3 After a successful Patch
The unit sulks for one scene (guide): prose only, rules text intact.

### 4.4 Stress or separate? (guide Q4)
**Ruling: the Patch does not use the Stress mechanic.** It is a Repair Offset of -1 (§1.1). Reasons: (1) it would be eaten by the Stress cap and make a Tribute pointless on the same floor; (2) it lasts two floors, and Stress resets per floor; (3) the guide already says Stress is for mood, repairs are for the machine. A Tribute and a Patch therefore stack to -2 on the same floor.

---

## 5. Lobotomizer (RP-03)

> **[SYSTEM]** "This product is an error-replacement net. It was not designed for you. It was not designed for anyone. Return it, if you can find the receipt."

### 5.1 Unlock and price (guide Q5)
- **Floor 6+**, needs a Syndicate technician (placed like the Patch technician; he is visibly nervous) and the retrieval below.
- **Price:** 1,000 credits x M per party, paid at the moment of install. F6-9: 5,000; F10-14: 20,000; F15+: 50,000. Same tier as a first revive Licensing Fee (core §6.4). **HOUSE**
- **Table vote:** unanimous among living Crawlers before the Install stage. Any Crawler may veto. **HOUSE**

### 5.2 The risky retrieval (guide Q5)
Three stages, Lobotomizer DC (15 / 17 / 19):
1. **Find the Net.** The technician only gives a rumor. Group check (Investigation, Persuasion or Insight): at least half the party must succeed. *Failure:* the Net moved; try again after a long rest for a 100 credits x M finder's fee.
2. **Get the Net.** It is held in a guarded Syndicate stockroom the GM places on that floor (not on the main path). Skill challenge: **4 successes before 3 failures**, then a **High** encounter (2024 DMG budget) with the Net as the prize. The Net is not a weapon and cannot be used against Crawlers. *Failure at the challenge:* the Net is lost; a 20% reclaim fee x price, retry on the next floor. Combat risk is ordinary 5e: Death Mode and revive rules still apply and nothing is softened (the guide calls this "risky").
3. **Install.** One volunteer throws the Net; the others Help (Advantage). One check at the band DC (Athletics, Acrobatics or Sleight of Hand). *Failure (Misfire):* the Net is spent, a 25% disposal fee is charged, **Stress +1 for the floor**, and the unit gets one Spite Move aimed at the thrower (counts against the one-per-Crawler-per-floor cap).

### 5.3 What it does, and to what (guide Q5)
- **Offset:** -2, **permanent**, applied at every future floor, floor of Level 0 (so "permanent" means a fixed -2 offset, subject to the -3 cap). **HOUSE**
- **Personality loss (guide):** one quirk and signature flourishes lost (which: sealed), snark capped at 2/5, obsession dormant, no new tells. Nothing is re-rolled; the sealed roll still hashes the same at the finale.
- **Rewards:** base rewards stay exactly as they are (fair play). Reward flavor goes beige: shorter banners, fewer jokes. Mechanics never change. **HOUSE**
- **Spite Moves:** the per-floor Spite budget (guide: L2 1, L3 2, L4 3, L5 3) is reduced by 1, minimum 0. **HOUSE**
- **Undo:** none. Once per campaign.

---

## 6. Therapy Session and the "Busted" callout (RP-04)

> **[SYSTEM]** "The unit will now articulate its feelings. This is not a betrayal of the brand. Please do not clap."

### 6.1 Unlock and price (guide Q6)
- **Floor 8+.** Two doors (guide): Route A (good terms) or Route B (a correct spontaneous "Busted" callout).
- **No DC:** Therapy is a purchase, not a check.
- **Price:** 250 credits x M per party at the session. F8-9: 1,250; F10-14: 5,000; F15+: 12,500. **HOUSE**
- **Route A, good terms:** Rapport Warm or Cozy when the party asks. No callout needed. The session is a saferoom scene. **(Unchanged.)**
- **Route B, "Busted" callout:** a spontaneous callout opens Therapy for the party even without good terms. Any Crawler's correct call counts. Route B has no additional payment. **HOUSE**

### 6.2 What counts as "Busted" (guide Q6)
"Busted" is a spontaneous callout, never invited. When the unit's quirk comes up naturally, the GM shows a subtle, noticeable but never announced tell: a pause, a changed tone, or an odd phrasing, always the same tell for the same trigger. A Crawler who spots it says **"Busted"** in character and names what they noticed—the trigger and the reaction—for example: **"Busted. It goes quiet and changes the subject whenever someone mentions the Syndicate."**

The Architect's command first applies the Busted guard below and only then, if the guard passes, checks the callout against the sealed roll. The GM answers with one fixed line only: **"Busted."** or **"Not busted."** There are no hints and no Warm/Cold grade. A right call opens Route B for the party; Therapy needs no good terms. A wrong call has no penalty and adds no Stress. As a spam guard, each Crawler gets one callout per scene, and a wrong callout text cannot be repeated.

> **Busted guard (v0.1.3).** A Busted call is **valid only in a scene where the GM has logged a tell** (the tell log, `tools/repair_log.py`; the GM logs each tell as it is shown). If no tell is logged for the scene, the call is refused with the same fixed line as a wrong call, **"Not busted."**, so a refusal and a wrong call read the same and leak nothing. A refused call uses up that Crawler's one callout for the scene but does not enter the list of wrong texts. **The refusal never consults the sealed roll** (no read, no hash check, no keyword match against it); only a call made in a scene with a logged tell is graded, under the rules above. This stops blind guessing in tell-less scenes from probing the sealed roll.

> **Tell-shown rule (v0.1.4).** When the GM shows the tell, the GM logs it **at that moment, before any call is graded**: `state.py repair-log tell --scene <SCENE_ID> --floor <N>` (scene and floor only; no quirk, trigger or text is written). A call counts only if its scene ID **and** floor match a logged tell. One log per scene is enough (a second log for the same scene and floor is ignored), and a tell logged later never revives a call that was already refused. The tell log is part of the sealed, hash-chained repair log and shows at the finale as "tell shown". Source: `tools/repair_log.py` (`tell`, `tell_shown`), `tools/gm_quirks.py` (`guess`), gm-notes/00-gm-principles.md (Quirk tell).

> **GM guidance: The tell**
>
> The tell is noticeable, never announced; use the same tell each time the trigger appears. Show it at least twice per floor when the trigger naturally arises. Never narrate it as "it twitched" or "you may have noticed." Never invite or hint at callouts, never say "Busted" first, and keep tells readable in plain text chat.

> **Player version**
>
> Some units have a quirk, and when it comes up the unit reacts a little differently: a pause, a change in tone, an odd choice of words. The GM will never point it out. If you notice it, say "Busted" in character and tell the table what you noticed and what set it off. The GM answers only "Busted" or "Not busted." If you're right, the party can book a Therapy Session even if the unit doesn't like you. If you're wrong, nothing bad happens, but you can't make the same call again, and each Crawler gets one call per scene.

The callout text and binary result are logged in the sealed log (§10, Q6) so the finale can audit the ruling; the log records the callout text and result only, not hints or a grade.

### 6.3 What it does (guide)
- **Offset:** -1, permanent. **HOUSE**
- The obsession can now be narrated openly by the unit; Therapy adds no new mechanical tells.
- Nothing is rewritten or re-rolled. The sealed hash still matches.
- No side-effect penalty (guide); the cost is money and attention.


## 7. Sabotage (RP-05)

> **[SYSTEM]** "You have chosen to antagonize a secondhand, vengeful AI. Your funeral is scheduled. The audience has requested popcorn."

### 7.1 Procedure (guide Q7)
- **Consensus:** every living Crawler says yes in the channel.
- **The trick:** the table describes a specific, spiteful bit and runs it in the fiction. No roll is needed to start it. The GM may ask for ordinary checks for any physical or social part (normal DCs).
- **Frequency:** once per floor.
- **Opt-outs:** the saboteur is a volunteer. No Crawler is made the saboteur by consensus alone; the volunteer picks it.

### 7.2 Effects
- **Stress +1** for the floor (guide). The guide also lists "raises effective level by 1": ruling is that these are **the same +1**, delivered through Stress, so it never becomes +2.
- **Spite Move follows** within a floor, aimed at the saboteur. It sits outside the free Spite budget at L0 and L1 but obeys "one per Crawler per floor" and the Warning line.
- **Rapport -2.** **HOUSE**

### 7.3 Personal blowback (guide Q7)
The saboteur takes one of these (GM picks, openly, never touching dice, DCs, damage, HP or saves): **HOUSE**
- **Blacklisted:** vendors that floor charge the saboteur +10%.
- **Wrong Name:** the next Reward line for the saboteur is addressed to the wrong Crawler (cosmetic).
- **Title:** a visible Title ("Known Vandal") the audience reacts to.
Plus the Spite Move itself. Nothing is reduced below the base reward floor, and the discretionary gap rule (one Bronze item per floor) still holds.

### 7.4 Pay-out (guide Q7)
Sabotage pays a modest **Hazard Pay of 50 credits x M** to the saboteur and **one Crowd Pop** (counts toward the Heroic Inspiration cap of 1 per session, core §3.7). It only pays out if the saboteur actually takes the Spite Move and the floor's Stress was not already +1, so repeating it cannot be farmed. **HOUSE**

---

## 8. Stacking, repeats, lockouts (guide Q2, Q4, Q8)

| Rule | Ruling (HOUSE) |
|---|---|
| Stress + Offset | Different tracks. Stack as in §1.1. |
| Stress sources | Never past -1..+1. +1 and -1 cancel. |
| Two Patches | No. One at a time; a new one is bought only after the old one reverts. Each later Patch costs +25% (max +100%). |
| Offset cap | -3 in total across Patch, Lobotomizer, Therapy. |
| Tribute | Once per floor. |
| Lobotomizer | Once per campaign. |
| Therapy | Once per campaign. |
| Busted callout | One per Crawler per scene; a wrong callout text cannot be repeated. |
| Sabotage | Once per floor. |
| Therapy after Lobotomizer | **Locked out.** The obsession is dormant; there is nothing to say. |
| Lobotomizer after Therapy | Allowed. Total Offset still capped at -3. |
| Patch with any other repair | Allowed. |
| Sabotage with any other repair | Allowed; effects stack by the rules above. |
| Level floor | Effective level never below 0 or above 5. |

---

## 9. Fair-play checklist, tuning notes, change list for Lore

**Fair-play checklist** (against guide §3):
- Dice, DCs, damage, HP, saves, initiative, rules text: untouched. DCs are band-fixed (§1.3) and Fit never changes them.
- Base rewards: untouched. The Lobotomizer only changes reward flavor.
- Death: no fiat kills. The Lobotomizer retrieval uses ordinary Death Mode.
- Spite: one per Crawler per floor, with a Warning line, honored in every failure above.
- Opt-outs: always win, including over Rapport, Boo and any spontaneous callout scene.
- Busted tells: noticeable but never announced, shown consistently when the trigger naturally arises; the GM never invites, hints at or says the callout first.
- Everything the GM judges (Fit tier, binary Busted/Not busted result, Rapport) is written down before or at the time and revealed at the finale; the Busted ruling gives no hints or intermediate grade.

**Tuning notes:**
- If Tribute becomes a no-brainer: raise the Boo share (never above "visibly flinched"), or raise the price to 75 x M.
- If the Patch Ticket is skipped: drop its 500-credit base fee, or drop the Fetch to "3 successes before 4 failures".
- If the Lobotomizer is too lethal: swap the High encounter for Moderate. Do not remove the risk entirely.
- Re-run `tools/sim_floors.py` (planning-only Monte Carlo) with the Offset term before locking, if Borent wants a feel for how often the unit sits at Level 0.

**Change list for DCC Lore (do not edit; after Caleb approves):**
1. Guide §2 "Effective level": add the Repair Offset term and the -3 cap.
2. Guide §4.2-4.4: Patch / Lobotomizer / Therapy are Repair Offset, not Stress.
3. Guide §4: replace each TBD with the §3-§7 numbers and failure penalties.
4. Guide §6: delete the eight rows once this file is approved; point to rules/50.
5. Guide §1: mention the Fit Log, Busted callout log and Rapport words are revealed at the finale.

---

## 10. Open questions for Caleb (max 6)

1. **Repair Offset as a separate track?** Recommended default: **yes.** Stress stays the mood track (-1..+1); Patch, Lobotomizer and Therapy sit in an Offset capped at -3. The alternative (everything inside Stress) makes Tribute and Patch fight over the same -1.
2. **Prices per party and the x1/x5/x20/x50 multiplier?** Recommended default: **yes.** Tribute 50, Patch 500, Lobotomizer 1,000, Therapy 250, Sabotage pays 50, all multiplied by M. Lobotomizer is the big spend; check it against your gut for F6. **Two-Crawler tables** (the current alpha table has two Crawlers): prices are per party and do not scale with party size, so two Crawlers split the full listed price (Tribute on F3-4 is 50 between them, 25 each if split evenly); per-Crawler limits (one Busted call per Crawler per scene, Spite once per Crawler per floor) are unchanged.
3. **Rapport counter as the "good terms" test for Therapy Route A?** Recommended default: **yes**, with Route A unchanged at Warm or Cozy and four published words (Frosty/Cool/Warm/Cozy) in the open log. Route B is the spontaneous Busted-callout path even without good terms.
4. **Does Sabotage pay out?** Recommended default: **yes, modest**: 50 x M credits plus one Crowd Pop, once per floor and only if Stress was not already +1. Alternative: nothing but the bit and the Title.
5. **Lockouts:** Lobotomizer and Therapy once per campaign; Therapy locked out after a Lobotomizer. Recommended default: **as drafted.** Alternative: allow both in either order.
6. **Commit-and-reveal logs for the GM's judgments?** The Tribute Fit tier, each Busted callout text and its binary Busted/Not busted result, and Rapport words would be written to the sealed log and published at the finale next to the hash. The Busted record contains callout text and result only. Recommended default: **yes.** Owner for the file location: Borent; I did not pick one.
