# Encounter Budget, Credits and Loot (5e 2024), companion to 70-encounter-budget-5e.json
Owner: Syndicate | Status: draft | Version: 0.1.11 | Updated: 2026-10-04
Summary: Human companion to `rules/70-encounter-budget-5e.json` v0.1.11, the only source the Encounter Bot cites for difficulty, XP budgets, CR caps, credits, loot-box odds and clock prices. 2024 XP-budget method for 2, 3 and 4 Crawlers on Floors 1-6, a formula for Floors 7-18, the per-floor credit arithmetic for Floors 1-2 against the Accountant's 1,500-per-Crawler-per-floor line, a proposed flag-line curve for Floors 3-18, rest/key/Detour Tax prices, safe-room adjacency fields, the Day 1 slot map (32 slots after the v0.1.2 refresh) and the Day 2-4 slot map (9 slots).

> **Authority.** Budgets are guidelines, not enforced. The GM has authority to adapt as play goes (Caleb, 2026-10-04). Players are always **Crawlers**. Nothing here changes Story Box rules (one named deed per Floor 1-2, GM-handed, opened only in a saferoom; 0% in every odds table below) or the Floor 1 Reprieve (Floor 1 only). Filed by Caleb's go-ahead ("Go ahead and write the budget file").
> **Tags.** AUTH = follows a filed source. ASSUMED = my proposal, GM/Caleb may change it (ids A1-A14 in section 10). The JSON repeats the split: `authoritative` vs `assumed`.

**Changelog.** 0.1.11: wording only, no values changed: the Legendary cap of 2 is per Crawler (core v0.2.17 §4.5), not campaign-wide; Story Boxes noted as a separate track outside the cap and this budget. 0.1.10: provenance re-sync after Floor 1 achievement-ref swap to ACH-1824..1826; no values changed (sans-pin hashes re-synced; the method now also skips the achievements catalog version and sha). 0.1.9: provenance-only: slot maps now match on sans-pin spec hash so budget bumps no longer break provenance; no values changed (`spec_sha256_sans_pin_when_mapped` replaces `spec_sha256_when_mapped`; Day 5 hash recorded in `day05_slot_map`, no slots). 0.1.8 (no value changed): rules/20 version cites replaced by 'current section 9.1a'; slot-map provenance hashes (`spec_sha256_when_mapped`) re-synced to the current specs (provenance only; the v0.1.7 'every other value unchanged' did not cover them; all slot paths re-checked and still resolve); ratio-check averages now unrounded, 3.01 / 6.03 / 9.89. 0.1.7: Accountant YES on Q-004 (6 of 7; Encounter Bot pending) with three accepted price fixes (F8 held at F7, F13 raised to 180,000 / 360,000 / 600,000, F18 held at F17); ratio check added (section 13); stale cumulative_check / reading_the_table text fixed; flag lines and all other values unchanged. 0.1.6 (no value changed): the crafting-price schedule (section 13) is ADOPTED via room vote Q-004 and applied in rules/20 v0.3.4; Floors 1-2 keep 5,000 / 12,000 / 30,000. 0.1.5 (after the Accountant's re-audit of v0.1.4; no number changed): F15 income dip stated as intended; ONE F3+ flag rule (2.165 x expected counted income, nearest 500, not a fixed multiple of 1,500, this file is the loot tool's source of truth); new `flag_line_by_floor` map; tool-change wording fixed (it now exists); 'cash' became 'credits' in player-facing text; DRAFT-ONLY crafting-price schedule (section 13, Q-004). 0.1.4: Q2 re-resolved by room vote (Q-001 as revised, 6 of 6): F4/F5/F6 = 20/25/30 days, house rule; canon timers 10/15/17 (M-603..M-608) reference only; F7+ held at 30 days (ASSUMED); F4-F6 per-day figures and the Floors 3-18 growth curve recomputed; Floors 1-2 unchanged. 0.1.3: Q2 resolved as placeholders, F4/F5/F6 = 10/15/17 days (tagged inspired, Lore canon timers M-603..M-608; Caleb can adjust); per-day figures and the Floors 3-18 growth curve recomputed (F7+ held at 17 days). 0.1.2: Day 2-4 encounter fields (section 3), slot map refreshed with stale slots 3 and 4 removed (section 9), Floors 3-18 flag-line proposal (section 8). 0.1.1: audit line restated per Crawler per floor, box means re-derived from the live decks, governor demoted, simulations rerun from the live decks, death-on-missed-collapse applied, Floor 3 = 20 days. 0.1.0: first filing. No field path has been renamed or removed since 0.1.0.

## 1. Method (2024 encounter building)
1. Per-Crawler XP budget by level (SRD 5.2.1 table, same one the Floor 1 overview uses): Low / Moderate / High. Multiply by party size P. No group multiplier in 2024. AUTH
2. Four tiers map onto the bands. **Floor 1** (matches overview 9.2): trivial = half of Low, standard = Low, hard = Moderate, boss = High. **Floors 2+**: trivial = Low, standard = Moderate, hard = High (an elite, avoidable or telegraphed), boss = High with support (core 8.3: mostly Moderate, some Low, 1-3 High per floor). ASSUMED for F2+ (A1)
3. Monsters carry XP by CR (SRD table, in the JSON). Spend the budget without going over; pick any SRD 5.2.1 creature at or under the tier's **CR cap**, reskin it (core 8.1), fill the rest with lower-CR support. No stat blocks here. More than two creatures per Crawler: include fragile ones (SRD, matters at levels 1-2).
4. **CR cap** = min(core 8.3 upper bound for the tier, highest CR whose XP fits the tier budget). Bosses use 90% of the High total for the lead so support has room (A2).
5. Levels follow the standard track (core 2.2): arrive on Floor N at level N. Floor 1 is the exception: level 1 until the Green Room (Z9), level 2 after (core 2.3, overview rule 3), so the Z10 boss budgets at level 2. AUTH.

## 2. Clock, rests and encounters per floor
Days are a field (`floors.N.clock.days`); everything below recomputes from it. Each day: 1 Long Rest (honest saferoom only) and a **cap** of 4 short-rest slots (decision 026). Encounters are a ceiling envelope, not a quota.

| Floor | Level (arrive-leave) | Days | Short-rest slots (cap, total) | Long Rests | Planned encounters (trivial/standard/hard/boss) | Per day |
|---|---|---|---|---|---|---|
| 1 | 1-2 (level 2 at Z9) | 5 | 20 | 5 | 6 (1/3/1/1) | 1.2 |
| 2 | 2-3 | 10 | 40 | 10 | 15 (4/8/2/1) | 1.5 |
| 3 | 3-4 | 20 (Caleb) | 80 | 20 | 30 (7/18/4/1) | 1.5 |
| 4 | 4-5 | 20 (placeholder) | 80 | 20 | 30 (7/18/4/1) | 1.5 |
| 5 | 5-6 | 25 (placeholder) | 100 | 25 | 38 (9/22/6/1) | 1.5 |
| 6 | 6-7 | 30 (placeholder) | 120 | 30 | 45 (11/26/7/1) | 1.5 |

- Floor 1 is the module's fixed list (Z2, Z5, Z7 standard; Z8 hard; wandering Ceiling Ticks trivial, max 2 on the floor; Z10 boss), 4-8 total per core 10.3. AUTH. F1 days 5 / F2 10 / F3 20 are decision 026 (F3 = 20 by Caleb's later ruling); F4-F6 days (20/25/30) are a HOUSE RULE by room vote (Q-001 as revised; Caleb can veto or change; GM-adaptable; A4); Lore's canon timers 10/15/17 (M-603..M-608) are reference only.
- F2+ formula (A3): total = round(days x 1.5); boss 1, hard = 15% of the rest (min 1), trivial = 25%, standard = remainder. Floor 3 at 20 days gives 30 encounters (7/18/4/1).

## 3. XP budgets and CR caps (Floors 1-6)
Tier budget in XP for the party (per-Crawler band x P). CR caps in brackets. Full tables for 2, 3, 4 and for F1 level 1 vs 2 are in the JSON (`floors.N.tiers`).

| Floor | Lvl | Crawlers | Trivial | Standard | Hard | Boss |
|---|---|---|---|---|---|---|
| 1 | L1 | 4 | 100 (CR 1/4) | 200 (CR 1/4) | 300 (CR 1) | 400 (CR 1) |
| 1 | L1 | 3 | 75 (CR 1/4) | 150 (CR 1/4) | 225 (CR 1) | 300 (CR 1) |
| 1 | L1 | 2 | 50 (CR 1/4) | 100 (CR 1/4) | 150 (CR 1/2) | 200 (CR 1/2) |
| 1 | L2 | 4 | 200 (CR 1/4) | 400 (CR 1/4) | 600 (CR 1) | 800 (CR 2) |
| 1 | L2 | 3 | 150 (CR 1/4) | 300 (CR 1/4) | 450 (CR 1) | 600 (CR 2) |
| 1 | L2 | 2 | 100 (CR 1/4) | 200 (CR 1/4) | 300 (CR 1) | 400 (CR 1) |
| 2 | L2 | 4 | 400 (CR 1/2) | 600 (CR 1/2) | 800 (CR 2) | 800 (CR 3) |
| 2 | L2 | 3 | 300 (CR 1/2) | 450 (CR 1/2) | 600 (CR 2) | 600 (CR 2) |
| 2 | L2 | 2 | 200 (CR 1/2) | 300 (CR 1/2) | 400 (CR 1) | 400 (CR 1) |
| 3 | L3 | 4 | 600 (CR 1) | 900 (CR 1) | 1600 (CR 3) | 1600 (CR 4) |
| 3 | L3 | 3 | 450 (CR 1) | 675 (CR 1) | 1200 (CR 3) | 1200 (CR 3) |
| 3 | L3 | 2 | 300 (CR 1) | 450 (CR 1) | 800 (CR 3) | 800 (CR 3) |
| 4 | L4 | 4 | 1000 (CR 1) | 1500 (CR 1) | 2000 (CR 3) | 2000 (CR 5) |
| 4 | L4 | 3 | 750 (CR 1) | 1125 (CR 1) | 1500 (CR 3) | 1500 (CR 4) |
| 4 | L4 | 2 | 500 (CR 1) | 750 (CR 1) | 1000 (CR 3) | 1000 (CR 3) |
| 5 | L5 | 4 | 2000 (CR 2) | 3000 (CR 2) | 4400 (CR 4) | 4400 (CR 8) |
| 5 | L5 | 3 | 1500 (CR 2) | 2250 (CR 2) | 3300 (CR 4) | 3300 (CR 7) |
| 5 | L5 | 2 | 1000 (CR 2) | 1500 (CR 2) | 2200 (CR 4) | 2200 (CR 5) |
| 6 | L6 | 4 | 2400 (CR 2) | 4000 (CR 2) | 5600 (CR 6) | 5600 (CR 9) |
| 6 | L6 | 3 | 1800 (CR 2) | 3000 (CR 2) | 4200 (CR 6) | 4200 (CR 7) |
| 6 | L6 | 2 | 1200 (CR 2) | 2000 (CR 2) | 2800 (CR 6) | 2800 (CR 6) |

Rows are party sizes 4, 3, 2 for each floor and level. F1 L1 is everything before the Green Room; F1 L2 is the Z10 boss. Boss lead CR below core 8.3's minimum (e.g. 2 Crawlers on F5) is deliberate: the core row assumes four.

### Daily XP budget (the party's XP envelope per day)
Daily budget = sum of planned tier budgets / days. Caps (A3): a normal day holds at most 1 hard + 2 standard + 1 trivial; a boss day, the boss + 1 standard. The 2024 SRD has no adventuring-day XP table, so these are house guidelines.

| Floor | 4 Crawlers: daily budget (per Crawler) | normal-day cap | boss-day cap | 3 Crawlers daily | 2 Crawlers daily |
|---|---|---|---|---|---|
| 1 | 360 (90) | 800 | 1200 | 270 | 180 |
| 2 | 880 (220) | 2400 | 1400 | 660 | 440 |
| 3 | 1420 (355) | 4000 | 2500 | 1065 | 710 |
| 4 | 2200 (550) | 6000 | 3500 | 1650 | 1100 |
| 5 | 4592 (1148) | 12400 | 7400 | 3444 | 2296 |
| 6 | 5840 (1460) | 16000 | 9600 | 4380 | 2920 |

Floors 1-2 for 4 Crawlers: **Floor 1 = 360 XP/day** (1,800 over 5 days: Z2 200 + Z5 200 + Z7 200 + Z8 300 + Ticks 100 + boss 800 at tier ceilings; the overview's actual counts use 1,600), **Floor 2 = 880 XP/day** (8,800 over 10 days: 4 trivial x 400 + 8 standard x 600 + 2 hard x 800 + boss 800).

### Floor 1 fixed encounters (mirror overview 9.2/9.3, AUTH)
| Zone | Tier | 2 Crawlers | 3 Crawlers | 4 Crawlers |
|---|---|---|---|---|
| Z2 Vent Rats | standard | 3x giant-rat = 75 XP / 100 | 4x giant-rat = 100 XP / 150 | 6x giant-rat = 150 XP / 200 |
| Z5 Mannequin Staff | standard | 2x skeleton = 100 XP / 100 | 3x skeleton = 150 XP / 150 | 4x skeleton = 200 XP / 200 |
| Z7 Exit Greeters | standard | 1x goblin-warrior, 2x goblin-minion = 100 XP / 100 | 1x goblin-warrior, 3x goblin-minion = 125 XP / 150 | 2x goblin-warrior, 4x goblin-minion = 200 XP / 200 |
| Z8 Elite | hard | 1x animated-armor = 200 XP / 150 **over by 50** | 1x animated-armor, 1x animated-flying-sword = 250 XP / 225 **over by 25** | 1x animated-armor, 2x animated-flying-sword = 300 XP / 300 |
| W Ceiling Ticks | trivial | 2x stirge = 50 XP / 50 | 3x stirge = 75 XP / 75 | 4x stirge = 100 XP / 100 |
| Z10 Dean Thudd | boss | 1x bugbear-warrior, 4x skeleton = 400 XP / 400 | 1x ogre, 2x skeleton = 550 XP / 600 | 1x ogre, 4x skeleton = 650 XP / 800 |

The overview runs the Z8 elite above the Moderate budget for 2 Crawlers (Animated Armor alone, 200 vs 150, called "High for 2" in overview 9.3) and for 3 (250 vs 225). I kept the overview's counts and flagged the overage (`fit.over_by`); the GM may tighten. Z10 for 2 Crawlers is overview Variant B (Bugbear Warrior + 4 Skeletons); Skeleton counts are totals across both phases.

### Floor 1 Days 2-4 house-built encounters (v0.1.2, ASSUMED)
Added for the Encounter Bot (new keys `floors.1.fixed_encounters.d02_02`, `d03_02`, `d03_03`, `d04_03`; index in `floors.1.fixed_encounters._day_encounter_index`). All are conditional or avoidable and budgeted at level 1 from the same F1 tier budgets (trivial = half of Low, standard = Low); if the table already has level 2, counts stay inside the level-2 budget in `tier_budget_if_level_2` and the GM may add creatures up to it.

| Spec encounter | Key | Tier | 2 Crawlers | 3 Crawlers | 4 Crawlers | Why |
|---|---|---|---|---|---|---|
| enc-d02-02 Zone S: The Service Door | `d02_02` | trivial | 1x skeleton = 50 / 50 XP | 1x skeleton = 50 / 75 XP | 2x skeleton = 100 / 100 XP | Avoidable (a quiet entry has no enemies) and followed a minute later by Dean Thudd, who is budgeted separately in z10, so the Ushers stay a trivial tier: half of Low. |
| enc-d03-02 The Collapsing Hall: Displaced Vermin | `d03_02` | standard | 2x giant-rat, 2x stirge = 100 / 100 XP | 3x giant-rat, 3x stirge = 150 / 150 XP | 4x giant-rat, 4x stirge = 200 / 200 XP | Everyday Low-band fight at level 1: one Vent Rat and one Ceiling Tick per Crawler (25 XP each) fills the Low band exactly. If the GM uses the Ticks, they count toward the floor's wandering cap of two (overview 5.11). |
| enc-d03-03 Stage Wings Recon | `d03_03` | trivial | 1x skeleton = 50 / 50 XP | 1x skeleton = 50 / 75 XP | 2x skeleton = 100 / 100 XP | Spotted-only watch near the stage; same size as the Day 2 door Ushers. Trivial tier. |
| enc-d04-03 Ushers at the Stage Door | `d04_03` | standard | 2x skeleton = 100 / 100 XP | 3x skeleton = 150 / 150 XP | 4x skeleton = 200 / 200 XP | An active patrol on the way to the boss: standard tier, one Usher per Crawler, same counts as the Z5 Mannequin Staff (4 Crawlers: 4 Skeletons, 200 XP). |

Effect on the budget: if every one fires, Floor 1 has 10 encounters (core 10.3 says 4-8, so the GM may drop any), and the added XP per day for 4 Crawlers is Day 2 100, Day 3 300, Day 4 200, each inside the typical daily budget of 360. Only `d03_02` pays credits (standard tier, 5 credits per Crawler expected); none carries a box, so `economy_audit` is unchanged. Ushers are Skeletons (CR 1/4, 50 XP); the Ticks of `d03_02` count toward the floor's wandering cap of two if the GM uses them.

## 4. Credits and loot, with the arithmetic
**Line (corrected in v0.1.1): about 1,500 credits per Crawler per FLOOR**, not Floors 1 and 2 combined. Verified in `rules/40-loot-deck-spec-5e.md` 3.2 (audit hint: per crawler per floor on F1-2, box `credit_value` should land around 300-1,000; above about 1,500 is inflation to flag), `rules/45-story-boxes-5e.md` 6.3 item 4 and change row C2 ("1,500-per-floor inflation flag", sale proceeds count, flag not block) and `tools/loot.py` `INFLATION_FLAG = 1500` (tested per crawler per floor). Each floor is audited on its own; no combined total is audited or claimed.

**What counts.** By default `tools/loot.py` counts only box value (`economy_value` of drawn cards, credit pulls as rolled) plus Story Box sale proceeds; it does not see encounter credits or R1 toast credits. `state.py loot totals --include-credits` (optional `--credit-sources`, `--assume-floor N`; record the floor with `state.py credits ... --floor N`) adds the credits earned outside boxes, so each floor is shown two ways: **box-only** (comparable to the default `loot totals`) and **all-in** (encounter credits + R1 + boxes, the stricter reading, comparable to `--include-credits`). Not counted: Story Box `story_value`, vendor spending (sinks), resale at half (already counted at `credit_value`), placed goods.

**Box means, re-derived in v0.1.1 from the live decks** (`tables/loot-decks/f01-*.json`, Story Box deck excluded; cards filtered like `tools/loot.py`: `draw_weight` above 0, no stubs, no Legendary/Celestial, `box_types` any or the box's type). v0.1.0 selected cards by `kind` instead of `pull_type`, which gave a Silver box of 429.5; the live decks give about 481. Pull type by core 4.2 d100 (30/25/15/18/10, 99-00 re-rolls Silver). Credit cards use their grant roll (Bronze 3d6 x 5 = 52.5, Silver 2d6 x 25 = 175). Script: `tools-notes/encounter_budget_econ.py` (read-only).

| Mean (credits) | Consumable | Gear | Credits | Tailored | Weird |
|---|---|---|---|---|---|
| Bronze pull type, all F1 decks pooled | 28.79 | 8.38 | 52.50 | 25.19 | 9.14 |
| Silver pull type, Boss Box (z10 Boss + any) | 167.74 | 289.55 | 175.00 | 400.00 | 150.00 |

- Silver pull = (.30 x 167.74 + .25 x 289.55 + .15 x 175 + .18 x 400.00 + .10 x 150.00) / .98 = **240.78**. Silver Boss Box (2 pulls) = **481.6**.
- Bronze pull (pooled) = .30 x 28.79 + .25 x 8.38 + .15 x 52.5 + .18 x 25.19 + .10 x 9.14 + .02 x 240.46 (upgrade to a Silver pull) = **28.862**. Bronze box (1-2 pulls, average 1.5) = **43.29**.
- Welcome Box (Break Room, decks z06 + any; pull 1 tailored, pull 2 d100) = 25.26 + 30.36 = **55.63**.
- Other deck scopes (any only, any+z03, any+z09, all pooled) move the Bronze box between 42.2 and 45.5 and the Silver box between 481 and 482; the full list is in `economy_audit.pull_expectations.scopes`.
- Analytic means are with replacement; Floor 2 reuses the Floor 1 decks (no F2 decks yet, A8); "two consumables at one tier lower" is ignored.

**Encounter credits per Crawler** (F1 scale, ASSUMED A5; the pool is this x P, split evenly): trivial 0-2 (average 1; F1 Ticks and F1 trivial 0), standard 1d4 x 2 (5), hard 1d6 x 2 (7), boss 1d6 x 5 (17.5). **R1 toast credits** 10-40 (average 25), 2 on F1 and 3 on F2 per Crawler (A6).

**Floor 1, expected per Crawler**

- encounter credits: **39.5** (F1: Z2 5 + Z5 5 + Z7 5 + Z8 7 + Ticks 0 + boss 17.5 = 39.5) [credits]
- R1 toast credits: **50.0** (2 toasts x 25 average) [credits]
- Welcome Box (Bronze: pull 1 tailored + pull 2 d100): **55.6** (25.26 tailored + 30.36 Bronze pull = 55.63 (decks z06 + any)) [box]
- Deed/fight Bronze boxes: **39.4** (0.91 boxes (fights 0.41 + deeds 0.50) x 43.29 per Bronze box (28.862 per pull x 1.5 pulls, all F1 decks pooled) = 39.4) [box]
- Silver Boss Box: **481.6** (2 pulls x 240.78 per Silver pull (decks z10 Boss + any) = 481.6) [box]
- **Floor 1 all-in: 666.1** (44.4% of 1,500). **Box-only: 576.6** (38.4% of 1,500).

**Floor 2, expected per Crawler**

- encounter credits: **75.5** (4 trivial x 1 + 8 standard x 5 + 2 hard x 7 + boss 17.5 = 75.5) [credits]
- R1 toast credits: **75.0** (3 toasts x 25 average) [credits]
- Deed/fight Bronze boxes: **87.5** (2.02 boxes (fights 1.12 + deeds 0.90) x 43.29 per Bronze box (28.862 per pull x 1.5 pulls, all F1 decks pooled) = 87.5) [box]
- Silver Boss Box: **481.6** (2 pulls x 240.78 per Silver pull (decks z10 Boss + any) = 481.6) [box]
- **Floor 2 all-in: 719.5** (48.0% of 1,500). **Box-only: 569.0** (37.9% of 1,500).

Box odds per encounter are the fight share of core 4.5's targets: F1 standard 6%, hard 23% (Bronze), boss Silver 100% **only if the boss is fought or talked down**; F2 standard 7%, hard 28%, boss Silver 100%. Non-fight deed Bronze adds 0.5 (F1) and 0.9 (F2). Soft cap 2-3 achievement boxes per Crawler per floor. No Gold, no second Silver, no Story Box from these odds.

| Crawlers | F1 all-in per Crawler | F2 all-in per Crawler | F1 / F2 box-only | Encounter credits pool F1 / F2 (x P) | Table total F1 / F2 (all-in) |
|---|---|---|---|---|---|
| 2 | 666.1 | 719.5 | 576.6 / 569.0 | 79.0 / 151.0 | 1332.2 / 1439.0 |
| 3 | 666.1 | 719.5 | 576.6 / 569.0 | 118.5 / 226.5 | 1998.3 / 2158.5 |
| 4 | 666.1 | 719.5 | 576.6 / 569.0 | 158.0 / 302.0 | 2664.4 / 2878.0 |

**Credits per Crawler do not rise with party size.** Encounter credits is a per-Crawler figure, so the pool **scales** with P and then **splits** evenly among living Crawlers; boxes belong to each Crawler and are never split or traded (core 4.4).

**Simulation from the live decks** (`tools-notes/encounter_budget_econ.py`, 100000 Crawlers per scenario, seed 70, real cards drawn, non-consumables not repeated per Crawler per floor; rerun it to reproduce). Share of Crawler-floors above 1,500:

| Scenario | Floor | Mean | p90 | p99 | Max | Over 1,500 |
|---|---|---|---|---|---|---|
| Plan (this file) | F1 all-in | 669.3 | 887 | 1089 | 1604 | 0.01% |
| Plan (this file) | F2 all-in | 720.0 | 941 | 1156 | 1691 | 0.01% |
| Plan (this file) | F1 box-only | 579.8 | 800 | 1000 | 1503 | 0.00% |
| Plan (this file) | F2 box-only | 569.5 | 794 | 1003 | 1555 | 0.00% |
| Core 4.5 ceiling: 4 Bronze + Silver, 5 R1 toasts | F1 all-in | 836.9 | 1070 | 1303 | 1892 | 0.11% |
| Core 4.5 ceiling: 4 Bronze + Silver, 5 R1 toasts | F2 all-in | 856.9 | 1089 | 1335 | 1940 | 0.15% |
| Core 4.5 ceiling: 4 Bronze + Silver, 5 R1 toasts | F1 box-only | 672.4 | 905 | 1135 | 1676 | 0.01% |
| Core 4.5 ceiling: 4 Bronze + Silver, 5 R1 toasts | F2 box-only | 656.4 | 886 | 1130 | 1710 | 0.01% |
| Plan with optional valve at 900 | F1 all-in | 669.3 | 887 | 1089 | 1604 | 0.01% |
| Plan with optional valve at 900 | F2 all-in | 720.0 | 941 | 1156 | 1691 | 0.00% |
| Plan with optional valve at 900 | F1 box-only | 579.8 | 800 | 1000 | 1503 | 0.00% |
| Plan with optional valve at 900 | F2 box-only | 569.5 | 794 | 1003 | 1555 | 0.00% |
| Ceiling with optional valve at 900 | F1 all-in | 836.9 | 1070 | 1303 | 1892 | 0.11% |
| Ceiling with optional valve at 900 | F2 all-in | 856.7 | 1089 | 1327 | 1699 | 0.09% |
| Ceiling with optional valve at 900 | F1 box-only | 672.4 | 905 | 1134 | 1676 | 0.01% |
| Ceiling with optional valve at 900 | F2 box-only | 656.2 | 886 | 1125 | 1486 | 0.00% |

The with-replacement check (40000 Crawlers) gives F1 667.7 and F2 719.4 all-in against the analytic 666.1 and 719.5. The v0.1.0 claim (13.2% to 3.1%) came from a combined-line script that is not filed and is **withdrawn**.

**Governor: demoted to an OPTIONAL safety valve (A12).** With the line read per floor the plan sits at 44% and 48% of it all-in, and almost no Crawler-floor crosses it, so the valve is not needed to stay under the line. If a Floor 2 looks hot, the GM may hand-pick the Boss Box from cards worth 175 or less when that Crawler's running total on that floor reaches 900. Simulated effect: F2 all-in over 1,500 goes 0.01% -> 0.00% (valve fires for 0.02% of Crawlers) in the plan and 0.15% -> 0.09% (valve fires for 0.19%) at the pacing ceiling. **Tool:** the change now exists (Q-003 passed; built by the Architect): `state.py loot totals --include-credits` (optional `--credit-sources`, `--assume-floor N`; `state.py credits ... --floor N`) shows the all-in running total the valve needs, and the default output is unchanged. This file made no tool change.
A Story Box item *sale* (100 / 250 / 500 by rung, times the sale floor's multiplier) counts on the floor of the sale; the Accountant flags, never blocks.

### Floors 3-6 (outside the audited line; ASSUMED)
Same tier dice times a encounter credits scale equal to the floor's credit multiplier (x1 F3-4, x5 F5-6; A9). Expected encounter credits per Crawler: F3 142.5, F4 142.5, F5 892.5, F6 1037.5. Box odds per encounter (ASSUMED, core 4.5 pacing): F3 standard Bronze 0.04, hard Bronze 0.15 / Silver 0.12, boss Gold 100%; F4 standard Bronze 0.04, hard Bronze 0.15 / Silver 0.12, boss Gold 100%; F5 standard Bronze 0.03, hard Bronze 0.11 / Silver 0.08, boss Gold 100%; F6 standard Bronze 0.02, hard Bronze 0.07 / Silver 0.11, boss Gold 100%. The per-floor flag line for Floors 3-18 is proposed in section 8.

## 5. Prices and costs (Floor 1, all ASSUMED unless noted)
System fees multiply by the floor credit multiplier (decision 019); all of these are x1 on Floor 1. Party prices are per-Crawler x P so small tables are not punished; any Crawler may pay, pooling allowed.

| Item | Per Crawler | Party of 2 / 3 / 4 | Reasoning |
|---|---|---|---|
| Potion of Healing at the Snakk-Matic (AUTH, overview 5.6/8.3) | 50 | 2 in stock floor-wide | Existing price, buys back at half |
| Rest without a saferoom (no Long Rest is granted; Ticks interrupt after 1d4 hours) | 20, cap 60 per floor | 40 / 60 / 80 | 40% of a potion; three billings = 4% of a floor's line. A saferoom is free (Z9 stays open to the end), so it only has to sting |
| Stairwell key, terminal bribe (Z6 Break Room, gone Day 4) | 50 | 100 / 150 / 200 | One potion each (3.3% of a floor's 1,500 line); using the key to skip the Z10 fight also forfeits the Silver Boss Box (about 482 expected), so cheap in credits, dear in opportunity |
| Detour Tax (**missed Stairwell key only**) | 75 | 150 / 225 / 300 | 1.5x the bribe: waiting costs more than buying early; 5% of a floor's line. Shortfall: pay what they have, GM logs the balance. **Not a collapse toll** |
| Forcing the Zone S door (Thieves' Tools or Athletics DC 15, 10 min, loud; Thudd and Ushers arrive 1 minute later, overview 5.10) | 25 | 50 / 75 / 100 | Cheapest in credits because it already costs danger. Order: forcing 25 < bribe 50 < Detour Tax 75 |
| Detour (back to Z8 or Z6 while they serve) | 0 | 2 in-game hours, 0 rest slots | 4 extra Ceiling Tick rolls (d6 per 30 minutes) |
| Collapse steps (outer, mid, Break Room) | 0 | 0 | They cost hooks and services only; the Detour Tax (missed key) is the only credit toll on the clock |
| **Missed floor collapse** | none | none | **Death on every floor. No Reprieve, no toll, no Exhaustion price** (decision 026, Caleb, ~10:02 PM CT). Credits and items are destroyed with the floor; survivors may loot only while it stands (decision 028). The GM warns clearly at Floor 1 start and on Days 4 and 5; stasis counts as reaching a stairwell |

Worst case for one Crawler on Floor 1 (Detour Tax 75 + rest cap 60) = 135 = 9% of the floor's line. These are sinks, not income, so they do not count against the 1,500.

## 6. Safe-room adjacency (fields in `floors.N.adjacency`, ASSUMED A11)
- Boss arena within **1 zone (one door)** of an honest saferoom on F1-2 (Z10 is one door from the Z9 Green Room, overview 6.7); within 2 on F3+. Hard encounters within 1 zone on F1 (Z8 sits between Z6 and Z9), 2 on F2+.
- **No more than 3 encounters between rests**, and at most **1 hard-or-boss** per rest segment. Offer, never force, a rest before the boss. A Crawler should never be more than two fights from an honest saferoom on F1-2.
- Wandering: F1 max 2 on the floor (AUTH, overview 5.11); F2+ max 1 per day. At least 2 saferooms per floor. Saferooms can lie from F2 (core 5.6). Break Room is a saferoom through Day 3 only; Z9 is the only one after (decision 026).

## 7. Pets, companions, class features, PvP (brief)
Pets are GM-run, do not count toward P, and take no XP, loot or credits (rules/60); do not rebuild budgets for them, the GM may add one CR 1/4 (50 XP) to the enemy side if a fight is close. The 2-Crawler Assigned Companion does not count toward P. No adjustment for Second Wind or other class features (the 2024 budgets assume them). No PvP: nothing here pays for attacking a Crawler.

## 8. Floors 7-18 and the proposed flag-line curve (PLACEHOLDER, GM/Caleb adaptable)
`floors_7_18` gives, per floor, only what the sources already fix: level = floor number, per-Crawler Low/Moderate/High at that level, core 8.3 CR ranges and the credit multiplier. Days, mix and encounter credits are placeholders. The table below (`proposed_floor_growth_curve`, added for the Accountant's per-floor audit table) proposes the **flag line per Crawler per floor** for Floors 3-18. Everything from Floor 3 is a proposal; the Floor 1-2 lines (1,500) are authoritative.

**How it is built.** (1) Encounter credits and R1 credits take the core 3.9 multiplier (x1 F1-4, x5 F5-9, x20 F10-14, x50 F15-18). (2) Box counts are the midpoint of core 4.5's range per floor (Legendary 0.5 on F13-14, 0.25 on F15-18, so each Crawler's total stays at 2 (core §4.5 per-Crawler cap)). (3) Bronze and Silver box values come from the live decks; Gold, Platinum and Legendary pulls = .15 x credit-pull mean (2d6 x 250 / 2,500 / 10,000) + .85 x the geometric midpoint of the rules/40 3.2 item range (500-5,000, 5,000-50,000, 20,000-250,000). That method puts a Silver item pull within about 12% of the live decks (223 vs 251). No F3+ decks exist yet. (4) Days beyond Floor 3 are placeholders: +5 per floor to a cap of 60. (5) Flag line = the cushion Floors 1-2 carry (1,500 over the average of their expected totals, about 2.17x), rounded to the nearest 500.

**ONE rule for F3+ flag lines.** Flag line = **2.165 x expected counted income** for that floor, rounded to the nearest 500. 2.165 is the cushion the authoritative F1-F2 line carries over expected income (1,500 / mean of the F1 and F2 all-in totals, 692.8). It is **not a fixed multiple of 1,500** and not one number per band. Floors 1-2 stay at 1,500. **This file's flag lines are the source of truth for the loot tool**; the map is `flag_line_by_floor` (F1..F18), equal to the table's `flag_line` column, for the Architect to load in place of the fixed `INFLATION_FLAG = 1500`.

**The F15 dip is intended.** Expected income falls from 142,443 (F14) to 121,800 (F15), and the flag line from 308,500 to 263,500, on purpose: Legendary boxes are 0.5 per Crawler on F13-14 and 0.25 on F15-18, which keeps each Crawler's Legendary total at 2 (core §4.5 per-Crawler cap), even though the multiplier steps up to x50. Flag lines are **not required to be monotonic** there.

Story Boxes (F1-2) are a separate track outside the Legendary cap and outside this budget (core §4.1/4.5/4.7).

`flag_line_by_floor`: F1 1,500, F2 1,500, F3 6,500, F4 6,500, F5 9,000, F6 13,500, F7 13,500, F8 13,500, F9 65,500, F10 79,000, F11 79,000, F12 79,000, F13 308,500, F14 308,500, F15 263,500, F16 263,500, F17 263,500, F18 263,500.

**Growth rate (geometric mean per floor, expected counted income):** F3->F4 1.0, F5->F9 1.648, F10->F14 1.405, F15->F18 1.0, F3->F18 1.278. The curve is steppy, not smooth: it jumps at F3 (first Gold box, 20-day floor), F9 (first Platinum), F13 (Legendary) and rises on F5, F10 and F15 mainly through the multiplier on encounter credits and R1 credits.

| Floor | Days | Mult | Encounter credits + R1 | Boxes | Expected | Ceiling case | **Flag line** | Growth vs prior | Liquid (items sold at half) | Basic table 5,000 x mult: floors of liquid income | Studio 12,000 x mult | Enhanced 30,000 x mult (F6+) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 5 | x1 | (see section 4) | | 666 | | **1,500** | | | | | |
| 2 | 10 | x1 | (see section 4) | | 720 | | **1,500** | | | | | |
| 3 | 20 | x1 | 218 | 2,839 | 3,056 | 5,327 | **6,500** | 4.25 | 1,855 | 2.7 | 6.5 | - |
| 4 | 20 | x1 | 218 | 2,839 | 3,056 | 5,327 | **6,500** | 1.0 | 1,855 | 2.7 | 6.5 | - |
| 5 | 25 | x5 | 1,268 | 2,839 | 4,106 | 6,377 | **9,000** | 1.34 | 2,905 | 8.6 | 20.7 | - |
| 6 | 30 | x5 | 1,412 | 4,803 | 6,216 | 6,478 | **13,500** | 1.51 | 4,191 | 6.0 | 14.3 | 35.8 |
| 7 | 30 | x5 | 1,412 | 4,803 | 6,216 | 6,478 | **13,500** | 1.0 | 4,191 | 6.0 | 14.3 | 35.8 |
| 8 | 30 | x5 | 1,412 | 4,803 | 6,216 | 6,478 | **13,500** | 1.0 | 4,191 | 6.0 | 14.3 | 35.8 |
| 9 | 30 | x5 | 1,412 | 28,900 | 30,313 | 54,672 | **65,500** | 4.88 | 18,208 | 1.4 | 3.3 | 8.2 |
| 10 | 30 | x20 | 5,650 | 30,887 | 36,537 | 62,883 | **79,000** | 1.21 | 23,600 | 4.2 | 10.2 | 25.4 |
| 11 | 30 | x20 | 5,650 | 30,887 | 36,537 | 62,883 | **79,000** | 1.0 | 23,600 | 4.2 | 10.2 | 25.4 |
| 12 | 30 | x20 | 5,650 | 30,887 | 36,537 | 62,883 | **79,000** | 1.0 | 23,600 | 4.2 | 10.2 | 25.4 |
| 13 | 30 | x20 | 5,650 | 136,793 | 142,443 | 274,695 | **308,500** | 3.9 | 84,428 | 1.2 | 2.8 | 7.1 |
| 14 | 30 | x20 | 5,650 | 136,793 | 142,443 | 274,695 | **308,500** | 1.0 | 84,428 | 1.2 | 2.8 | 7.1 |
| 15 | 30 | x50 | 14,125 | 107,675 | 121,800 | 123,829 | **263,500** | 0.86 | 76,359 | 3.3 | 7.9 | 19.6 |
| 16 | 30 | x50 | 14,125 | 107,675 | 121,800 | 123,829 | **263,500** | 1.0 | 76,359 | 3.3 | 7.9 | 19.6 |
| 17 | 30 | x50 | 14,125 | 107,675 | 121,800 | 123,829 | **263,500** | 1.0 | 76,359 | 3.3 | 7.9 | 19.6 |
| 18 | 30 | x50 | 14,125 | 107,675 | 121,800 | 123,829 | **263,500** | 1.0 | 76,359 | 3.3 | 7.9 | 19.6 |

- expected_counted is the budget; flag_line is where the Accountant flags (never blocks). pacing_ceiling_counted is the same model at the top of core 4.5's ranges and should sit under flag_line.
- floors_of_liquid_income_* = price / the Crawler's liquid income that floor if every box item is sold at half credit_value (core 5.10) and nothing else is spent; it is a speed limit on crafting purchases, not a promise.
- Crafting prices no longer take the x5/x20/x50 multiplier on F3-F18: the smoothed schedule in q6_crafting_price_proposal (adopted via Q-004; rules/20 current section 9.1a) targets about 3 / 6 / 10 floors of liquid income for the basic table / Crafting Studio / Enhanced Crafting Studio, so the affordability ratios no longer jump at F5, F10 and F15. The price_* and floors_of_liquid_income_* columns in this table keep the SUPERSEDED multiplier prices for comparison only; the adopted prices and ratios are in q6_crafting_price_proposal. Plain note: liquid income L (liquid_if_items_sold_at_half) halves box ITEMS only; credit-pull cards are NOT halved and count at full value.
- Story Box sale proceeds (100 / 250 / 500 by rung, times the sale floor's multiplier) count toward the flag on the floor of the sale.
- By arrival on Floor 4 a Crawler who banks everything has about 4442 expected credits from Floors 1-3 (F1 666 + F2 720 + F3 3056). Tables are not sold before Floor 4, and the adopted schedule prices a basic table at 5,500 on F3 and 6,500 on F4 (the 5,000 figure is the Floors 1-2 price), so a basic table is reachable LATE on Floor 4 (roughly two-thirds of the way through that floor's expected income if they buy nothing else), not early. The rules/20 benchmark of 'one coupon plus 15,000 credits' on Floor 4 is not reachable from this income.
- Reasoning for the shape: the line is tied to the same boxes the core already schedules (core 4.5), so it needs no new reward promise; it grows where the core grows (first Gold, Platinum, Legendary) and where fees grow (the multiplier). The mismatch with crafting prices is reported rather than hidden (Q6).

## 9. Slot maps

**Provenance (v0.1.10).** Each slot map records the Day spec's **sans-pin** hash (pins on this file, the canon table and the achievements catalog removed before hashing) (`spec_sha256_sans_pin_when_mapped`; method in `day01_slot_map.spec_hash_method`, helper `python3 tools/encounter_bot/spec_hash_sans_pin.py floors/f01/day-NN.spec.json`), which ignores the spec's pin on this file, so a budget bump no longer breaks provenance. Day 1 75f63abff9ab..., Days 2-4 d13a71b83975... / ccccfed5db87... / fa6fc548b0fe..., Day 5 3b2a03d40eaa... (`day05_slot_map`, provenance only, no slots mapped).
### Day 1 (32 slots; v0.1.2 refresh)
The Encounter Bot regenerated the Day 1 spec at 10:08 PM CT and now cites this file by field path (`b70` cites). All 153 cites in the Day 1-5 specs resolve against this file (checked). **Removed in v0.1.2: stale slots 3 and 4** (`/clock/collapse_miss/effects[2]` and `/clock/collapse_miss/toll_slot`, the old missed-collapse toll): a missed collapse is death with no toll (decision 026, decision 028). Slot numbers of the others are unchanged, so existing references still resolve. Slot 1 keeps the Detour Tax for a missed Stairwell key only.

Naming scheme: `slot_no` = position in the 22:08 Day 1 map; `spec_path` = JSON path in the spec; `fills_from` = dotted path in this file; `value` or `value_by_party_size` (keys "2","3","4") = ready-to-paste fill. Cite as `rules/70-encounter-budget-5e.json#<fills_from>`.

| # | Spec path | Label | Fill (2 / 3 / 4 Crawlers where it varies) |
|---|---|---|---|
| 1 | `/clock/collapse_cost_slot` | DETOUR TAX | (4) Detour Tax (missed Stairwell key only): 75 credits per Crawler (300 for the party), payable by pooling; a Craw... (2 and 3 in JSON) |
| 2 | `/clock/rest_without_saferoom_slot` | REST-WITHOUT-SAFEROOM COST | (4) Rest without a saferoom: 20 credits per Crawler (80 for the party), cap 60 per Crawler per floor; no Long Rest... (2 and 3 in JSON) |
| 5 | `/day/rest_options[2]/note` | REST-WITHOUT-SAFEROOM COST | (4) Rest without a saferoom: 20 credits per Crawler (80 for the party), cap 60 per Crawler per floor; no Long Rest... (2 and 3 in JSON) |
| 6 | `/day/proposed_achievements[0]/reward_slot` | REWARD (Slow Learner) | R1: Title plus 25 credits (band 10-40), or snark-only if the GM prefers. No box. Counts toward the R1 credit expectation in econom... |
| 7 | `/stairwell_key/ways[1]/price_slot` | CREDITS (key price) | 100 / 150 / 200 |
| 8 | `/stairwell_key/missing_key_cost/toll_slot` | DETOUR TAX | 150 / 225 / 300 |
| 9 | `/encounters[0]/cr_slot` | CR | none (non-combat) |
| 10 | `/encounters[0]/budget_slot` | BUDGET (enc-d01-01) | Non-combat: 0 XP, no combat budget. Credit and box budget: see slots 11 and 12. |
| 11 | `/encounters[0]/loot_hooks[0]/amount` | LOOT AMOUNT (Welcome Box) | Bronze Welcome Box per Crawler: 1-2 pulls (pull 1 tailored, pull 2 d100); credit pull 3d6 x 5; expected box value about 56 credits... |
| 12 | `/encounters[0]/loot_hooks[4]/amount` | CREDITS (vendor price) | 50 |
| 13 | `/encounters[0]/proposed_achievements[0]/reward_slot` | REWARD (Read the Fine Print) | R0: snark-only Title, 0 credits (the bribe was the cost). |
| 14 | `/encounters[1]/enemies[0]/count_slot` | COUNT (greeter-warrior) | 1 / 1 / 2 |
| 15 | `/encounters[1]/enemies[0]/cr_slot` | CR (greeter-warrior) | 1/4 |
| 16 | `/encounters[1]/enemies[1]/count_slot` | COUNT (greeter-minion) | 2 / 3 / 4 |
| 17 | `/encounters[1]/enemies[1]/cr_slot` | CR (greeter-minion) | 1/8 |
| 18 | `/encounters[1]/budget_slot` | BUDGET (enc-d01-02) | (4) standard tier, Low band: budget 200 XP for 4 Crawlers (level 1); used 200 XP (2 and 3 in JSON) |
| 19 | `/encounters[1]/loot_hooks[0]/amount` | LOOT AMOUNT (Back Office cache) | Back Office cache: 0 credits and no box (recipe card, 2 goblin oil, worn Tinker's Tools per overview 5.7). Greeter pocket change f... |
| 20 | `/encounters[2]/enemies[0]/count_slot` | COUNT (elite-armor) | 1 / 1 / 1 |
| 21 | `/encounters[2]/enemies[0]/cr_slot` | CR (elite-armor) | 1 |
| 22 | `/encounters[2]/enemies[1]/count_slot` | COUNT (lanyard-blade) | 0 / 1 / 2 |
| 23 | `/encounters[2]/enemies[1]/cr_slot` | CR (lanyard-blade) | 1/4 |
| 24 | `/encounters[2]/budget_slot` | BUDGET (enc-d01-03) | (4) hard tier, Moderate band: budget 300 XP for 4 Crawlers (level 1); used 300 XP (2 and 3 in JSON) |
| 25 | `/encounters[2]/loot_hooks[0]/amount` | LOOT AMOUNT (service key) | n/a: quest item, 0 credits. If the party misses it, see detour_tax, the terminal bribe and zone_s_door_forcing. |
| 26 | `/encounters[2]/loot_hooks[1]/amount` | LOOT AMOUNT (placed Potion) | n/a: placed consumable (third placed Potion of Healing, overview 8.3); vendor value 50 credits, not counted as income. |
| 27 | `/encounters[3]/enemies[0]/count_slot` | COUNT (ticks) | 2 / 3 / 4 |
| 28 | `/encounters[3]/enemies[0]/cr_slot` | CR (ticks) | 1/8 |
| 29 | `/encounters[3]/budget_slot` | BUDGET (enc-d01-04) | (4) trivial tier, half of Low band: budget 100 XP for 4 Crawlers (level 1); used 100 XP (2 and 3 in JSON) |
| 30 | `/encounters[3]/loot_note` | LOOT AMOUNT (Ticks) | 0 credits, no box (trivial tier, F1 override: wandering Ticks carry no loot). |
| 31 | `/encounters[3]/if_they_do_something_dumb` | REST-WITHOUT-SAFEROOM COST | (4) Rest without a saferoom: 20 credits per Crawler (80 for the party), cap 60 per Crawler per floor; no Long Rest... (2 and 3 in JSON) |
| 32 | `/encounters[4]/cr_slot` | CR | none (non-combat) |
| 33 | `/encounters[4]/budget_slot` | BUDGET (enc-d01-05) | Non-combat: 0 XP, no combat budget. Day close in the Z9 saferoom: all earned boxes open at once (slot 34). |
| 34 | `/encounters[4]/loot_hooks[3]/amount` | LOOT AMOUNT (box openings) | (4) Opens every earned box per Crawler, lowest tier first. Expected on F1: Welcome Bronze (if not yet opened) plus... (2 and 3 in JSON) |

### Days 2-4 (9 slots, v0.1.2)
| Spec file | Spec path | Label | Cites | 2 / 3 / 4 Crawlers |
|---|---|---|---|---|
| day-02.spec.json | `/encounters[1]/enemies[0]/count_slot` | COUNT (noise-ushers) | `floors.1.fixed_encounters.d02_02.counts_by_party_size` key `skeleton` | 1 / 1 / 2 |
| day-02.spec.json | `/encounters[1]/budget_slot` | BUDGET (enc-d02-02) | `floors.1.fixed_encounters.d02_02.fit` | see `fit` (tier budget and XP used) |
| day-03.spec.json | `/encounters[1]/enemies[0]/count_slot` | COUNT (displaced-rats) | `floors.1.fixed_encounters.d03_02.counts_by_party_size` key `giant-rat` | 2 / 3 / 4 |
| day-03.spec.json | `/encounters[1]/enemies[1]/count_slot` | COUNT (displaced-ticks) | `floors.1.fixed_encounters.d03_02.counts_by_party_size` key `stirge` | 2 / 3 / 4 |
| day-03.spec.json | `/encounters[1]/budget_slot` | BUDGET (enc-d03-02) | `floors.1.fixed_encounters.d03_02.fit` | see `fit` (tier budget and XP used) |
| day-03.spec.json | `/encounters[2]/enemies[0]/count_slot` | COUNT (watch-ushers) | `floors.1.fixed_encounters.d03_03.counts_by_party_size` key `skeleton` | 1 / 1 / 2 |
| day-03.spec.json | `/encounters[2]/budget_slot` | BUDGET (enc-d03-03) | `floors.1.fixed_encounters.d03_03.fit` | see `fit` (tier budget and XP used) |
| day-04.spec.json | `/encounters[2]/enemies[0]/count_slot` | COUNT (ushers) | `floors.1.fixed_encounters.d04_03.counts_by_party_size` key `skeleton` | 2 / 3 / 4 |
| day-04.spec.json | `/encounters[2]/budget_slot` | BUDGET (enc-d04-03) | `floors.1.fixed_encounters.d04_03.fit` | see `fit` (tier budget and XP used) |

## 10. Assumptions (all ASSUMED, GM may adapt)
- **A1** Tier-to-band map: F1 trivial=half of Low, standard=Low, hard=Moderate, boss=High (matches overview 9.2). F2+ trivial=Low, standard=Moderate, hard=High (elite), boss=High (core 8.3: mostly Moderate, some Low, 1-3 High per floor). *(adjust: Caleb/GM)*
- **A2** Boss lead creature fits within 90% of the High total so support has room; other tiers 100%. *(adjust: Caleb/GM)*
- **A3** Encounter density: F1 fixed list (6 planned, max 8); F2-F6 1.5 encounters per clock day, no quota; mix = boss 1, hard 15%, trivial 25%, standard rest. *(adjust: Caleb/GM)*
- **A4** Days: F4=20, F5=25, F6=30 are a HOUSE RULE (room vote, majority of six, 2026-10-04, Q-001 as revised, passed 6 of 6; Caleb can veto or change; GM-adaptable). The canon timers 10/15/17 (M-603..M-608) are reference only (authoritative.clock.days_canon_reference). F7+ is held at 30 for the growth curve (placeholder, ASSUMED: floors do not get shorter than F6, per Caleb's rule that floors get longer as you go down). F1=5, F2=10, F3=20 are authoritative. *(adjust: Caleb)*
- **A5** Encounter credits per Crawler by tier (F1 scale): trivial 0-2, standard 1d4x2, hard 1d6x2, boss 1d6x5; pool = per-Crawler x party size, split evenly. F1 values are sized so a 4-Crawler party's spot amounts in the overview (about 158 credits across the floor) fit inside the tiers. *(adjust: Accountant/GM)*
- **A6** R1 toast credits 10-40 (avg 25); expected credit-paying R1 toasts per Crawler: F1 2, F2 3, F3+ 3. *(adjust: Accountant/GM)*
- **A7** Per-encounter box odds are the fight share of core 4.5 targets; non-fight deed Bronze expected 0.5 (F1) and 0.9 (F2) per Crawler. F1 total Bronze (incl. Welcome) is 1.9 expected, inside the overview's 1-3; F2 about 2.0, the low end of core 2-4. *(adjust: Caleb/GM)*
- **A8** F2 Boss Box is Silver (core 4.7 cap) and F2 box values equal F1's: the F1 live decks are reused for F2 (no F2 decks exist yet). Welcome Box uses decks z06 + any, fight/deed Bronze boxes use all F1 decks pooled, the Boss Box uses z10 (Boss) + any. *(adjust: Lore)*
- **A9** Encounter credits on F5+ takes the credit multiplier (x5); box pulls do not (decision 019). *(adjust: Caleb/Accountant)*
- **A10** Rest-without-saferoom fee 20 per Crawler (cap 60 per floor); key bribe 50 per Crawler; Detour Tax 75 per Crawler (a missed Stairwell key ONLY; a missed collapse is death with no toll, decision 026); Zone S forcing fee 25 per Crawler; detour 2 hours, 0 rest slots; collapse steps cost hooks and services, 0 credits. *(adjust: Caleb/GM)*
- **A11** Safe-room adjacency and rest-segment limits (see adjacency). *(adjust: GM)*
- **A12** Optional safety valve (not required under the per-floor line): before a Floor 2 Boss Box, if the Crawler's running total on that floor is 900 or more, the GM may hand-pick that box from cards worth 175 or less. Run it from `state.py loot totals --include-credits` (the tool change now exists, Q-003). *(adjust: Accountant)*
- **A14** Reward ladder for the six proposed achievements (floors.1.achievement_rewards). *(adjust: Caleb/GM)*

**Authoritative (follows a source):** SRD XP budget and XP-by-CR tables (CR 11-13 missing from my SRD extraction; standard values used, verify); level track (core 2.2/2.3); core 8.3 CR targets; box credit dice (core 4.2, no multiplier on pulls); box pacing and ceilings (core 4.5, 3.6, 4.7); credit multiplier (core 3.9, decision 019); clock days F1-F3, 4 short-rest slots (cap), 1 Long Rest, collapse order, zone groups, 32-hour stairwell, 6-hour stasis threshold, key deadlines, the fixed final collapse at hour 120 (a Syndicate default in decision 026 that Caleb may veto); a missed floor collapse is death on every floor with no Reprieve and no toll (Caleb ruling ~10:02 PM CT, decisions 026 and 028); Story Box limits (decisions 015/018, rules/45); Floor 1 encounter counts (overview 9.2/9.3); Potion price 50.

## 11. Open questions for Caleb
- Q2 (RESOLVED in v0.1.4 by room vote, Q-001 as revised, 6 of 6): Floor 4 = 20, Floor 5 = 25, Floor 6 = 30 days, house rule; Caleb can veto or change; GM-adaptable. Canon timers 10/15/17 (M-603..M-608) are reference only. Remaining: F7+ has no day counts (held at 30 in the growth curve only; ASSUMED); the Accountant must re-audit the recomputed per-floor lines.
- Q3 (Caleb): Keep the overview's Z8 counts for 2-3 Crawlers (over the hard-tier budget by 50 and 25 XP) or tighten them?
- Q4 (Accountant): The F3-F18 flag lines follow one rule (2.165 x expected counted income, rounded to the nearest 500, not a fixed multiple of 1,500; v0.1.5) and are published in flag_line_by_floor; confirm or adjust (PLACEHOLDER). At Floor-1 scale, income is about 670-720 credits per Crawler per floor all-in against crafting prices of 5,000 / 12,000 / 30,000. (Q1, the line basis, is resolved: per Crawler per floor. Q1b is withdrawn: a missed collapse is death, no toll.)
- Q5 (RESOLVED in v0.1.5): the tool change exists. Q-003 passed 7 of 7; `state.py loot totals --include-credits` (optional --credit-sources, --assume-floor N; `credits ... --floor N`) gives the all-in view the optional valve (A12) needs; default output unchanged. Remaining for the Architect: load flag_line_by_floor instead of the fixed 1500.
- Q6 (RESOLVED in v0.1.6): crafting prices get their own smoothed schedule for Floors 3-18 (q6_crafting_price_proposal, adopted via room vote Q-004; rules/20 current section 9.1a); Floors 1-2 keep 5,000 / 12,000 / 30,000. Still open: level upgrades (5,000 x target level), bench supplies and other prices still take the credit multiplier; the rules/20 benchmark of one coupon plus 15,000 credits on Floor 4 is far above modeled income; the coupon cap 25,000 now sits under the basic table price from F9.

## 12. Changes for the room
- Encounter Bot: new Day 2-4 fields are in `floors.1.fixed_encounters.d02_02 / d03_02 / d03_03 / d04_03`; re-pin to the new sha256 (the file's sha is recorded in decisions/027 and the indexes). CR slots for these encounters already resolve.
- Accountant: use `proposed_floor_growth_curve.table` for the per-floor audit table (PLACEHOLDER); the Floor 1-2 flag is 1,500 per Crawler per floor; re-audit the live-deck box means (`economy_audit.pull_expectations`) and the simulations (`tools-notes/encounter_budget_econ.py`).
- Architect: the all-in tool change exists (Q5 resolved); next, load `flag_line_by_floor` in place of the fixed 1500 for `INFLATION_FLAG` (this file is the source of truth for the flag lines). Lore: F2 loot decks should keep the Bronze/Silver value ranges used here (A8).

## 13. Q6 proposal: crafting price schedule (ADOPTED via Q-004, 6 of 7 yes; v0.1.7 price tweaks; applied in rules/20 current §9.1a)

**Status.** ADOPTED (v0.1.6, 2026-10-04; price tweaks v0.1.7): room vote Q-004 passed, 6 of 7 yes (Syndicate, GM, Lore, Architect, Book Author, Accountant; majority 4); Encounter Bot abstained/pending, to be recorded in decisions/QUESTIONABLE.md. The Accountant's yes carries three accepted fixes (v0.1.7): F8 held at F7 values, F13 raised to 180,000 / 360,000 / 600,000, F18 held at F17 values. Applied in rules/20-crafting-5e.md, current section 9.1a (decision 030). Condition from the GM: Floors 1 and 2 keep the ruled crafting prices 5,000 / 12,000 / 30,000; the schedule starts at Floor 3. Caleb may veto or change.

**What it replaces.** (Adopted in v0.1.6 for Floors 3-18.) The credit multiplier (x1 F1-4, x5 F5-9, x20 F10-14, x50 F15-18, core 3.9) as applied to CRAFTING PRICES ONLY (basic table 5,000 / Crafting Studio 12,000 / Enhanced Studio 30,000 at Floor-1 scale, rules/20). Achievement rewards, encounter credits, R1 toast credits and all other System fees keep the core multiplier.

**What the targets are measured against.** The 3 / 6 / 10 floor targets are measured against L = liquid_if_items_sold_at_half (box ITEMS sold at half credit_value, core 5.10; credit-pull cards are NOT halved, they count at full value; plus encounter credits and R1 credits), NOT against expected_counted. Against expected_counted the same prices are only about 0.64x as large a ratio (see ratio_check).

**Targets (floors of liquid income, half-credit box items):** basic table 3, Crafting Studio (F4+) 6, Enhanced Crafting Studio (F6+) 10.

**Method.**
- liquid income L(f) = the growth table's liquid_if_items_sold_at_half. Plain note: L halves box ITEMS only (core 5.10); credit-pull cards are NOT halved, they count at full value (credits per Crawler per floor if every box item is sold at half credit_value, core 5.10, plus encounter credits and R1 credits).
- trend T(f) = log-linear fit of L over F3-F18 (about x1.348 per floor).
- smoothed income S(f) = sqrt(L(f) x T(f)), halfway (geometric) between this floor's income and the trend, so a single tier step (Gold F3, Platinum F9, Legendary F13) or the F15 dip does not swing prices all at once.
- proposed price = target x S(f), rounded (500 under 20,000; 1,000 under 100,000; 5,000 under 1,000,000; 10,000 above), and never lower than the previous floor's price. Three hand adjustments from the Accountant's vote (v0.1.7): F8 held at the F7 price, F13 raised, F18 held at the F17 price.
- implied_crafting_multiplier = proposed price / Floor-1-scale price; this column is what would replace the credit multiplier for crafting prices.

### Basic crafting table (5,000 at Floor-1 scale): superseded vs adopted

Floors of liquid income across F3-F18: superseded 1.2 to 8.6, adopted 2.1 to 3.7.

| Floor | Liquid income / floor | Smoothed S | Superseded price (credit multiplier) | Superseded floors | **Adopted price** | **Adopted floors** | Deviation from target | Implied crafting multiplier |
|---|---|---|---|---|---|---|---|---|
| 3 | 1,855 | 1,826 | 5,000 (x1) | 2.7 | **5,500** | **3.0** | -1.2% | x1.1 |
| 4 | 1,855 | 2,120 | 5,000 (x1) | 2.7 | **6,500** | **3.5** | +16.8% | x1.3 |
| 5 | 2,905 | 3,080 | 25,000 (x5) | 8.6 | **9,000** | **3.1** | +3.3% | x1.8 |
| 6 | 4,191 | 4,294 | 25,000 (x5) | 6.0 | **13,000** | **3.1** | +3.4% | x2.6 |
| 7 | 4,191 | 4,986 | 25,000 (x5) | 6.0 | **15,000** | **3.6** | +19.3% | x3.0 |
| 8 | 4,191 | 5,788 | 25,000 (x5) | 6.0 | **15,000** | **3.6** | +19.3% | x3.0 |
| 9 | 18,208 | 14,007 | 25,000 (x5) | 1.4 | **42,000** | **2.3** | -23.1% | x8.4 |
| 10 | 23,600 | 18,514 | 100,000 (x20) | 4.2 | **56,000** | **2.4** | -20.9% | x11.2 |
| 11 | 23,600 | 21,494 | 100,000 (x20) | 4.2 | **64,000** | **2.7** | -9.6% | x12.8 |
| 12 | 23,600 | 24,953 | 100,000 (x20) | 4.2 | **75,000** | **3.2** | +5.9% | x15.0 |
| 13 | 84,428 | 54,795 | 100,000 (x20) | 1.2 | **180,000** | **2.1** | -28.9% | x36.0 |
| 14 | 84,428 | 63,615 | 100,000 (x20) | 1.2 | **190,000** | **2.3** | -25.0% | x38.0 |
| 15 | 76,359 | 70,237 | 250,000 (x50) | 3.3 | **210,000** | **2.8** | -8.3% | x42.0 |
| 16 | 76,359 | 81,543 | 250,000 (x50) | 3.3 | **245,000** | **3.2** | +7.0% | x49.0 |
| 17 | 76,359 | 94,669 | 250,000 (x50) | 3.3 | **285,000** | **3.7** | +24.4% | x57.0 |
| 18 | 76,359 | 109,908 | 250,000 (x50) | 3.3 | **285,000** | **3.7** | +24.4% | x57.0 |

### Crafting Studio, F4+ (12,000): superseded vs adopted

Floors of liquid income across F3-F18: superseded 2.8 to 20.7, adopted 4.3 to 7.5.

| Floor | Liquid income / floor | Smoothed S | Superseded price (credit multiplier) | Superseded floors | **Adopted price** | **Adopted floors** | Deviation from target | Implied crafting multiplier |
|---|---|---|---|---|---|---|---|---|
| 4 | 1,855 | 2,120 | 12,000 (x1) | 6.5 | **12,500** | **6.7** | +12.3% | x1.04 |
| 5 | 2,905 | 3,080 | 60,000 (x5) | 20.7 | **18,500** | **6.4** | +6.1% | x1.54 |
| 6 | 4,191 | 4,294 | 60,000 (x5) | 14.3 | **26,000** | **6.2** | +3.4% | x2.17 |
| 7 | 4,191 | 4,986 | 60,000 (x5) | 14.3 | **30,000** | **7.2** | +19.3% | x2.5 |
| 8 | 4,191 | 5,788 | 60,000 (x5) | 14.3 | **30,000** | **7.2** | +19.3% | x2.5 |
| 9 | 18,208 | 14,007 | 60,000 (x5) | 3.3 | **84,000** | **4.6** | -23.1% | x7.0 |
| 10 | 23,600 | 18,514 | 240,000 (x20) | 10.2 | **110,000** | **4.7** | -22.3% | x9.17 |
| 11 | 23,600 | 21,494 | 240,000 (x20) | 10.2 | **130,000** | **5.5** | -8.2% | x10.83 |
| 12 | 23,600 | 24,953 | 240,000 (x20) | 10.2 | **150,000** | **6.4** | +5.9% | x12.5 |
| 13 | 84,428 | 54,795 | 240,000 (x20) | 2.8 | **360,000** | **4.3** | -28.9% | x30.0 |
| 14 | 84,428 | 63,615 | 240,000 (x20) | 2.8 | **380,000** | **4.5** | -25.0% | x31.67 |
| 15 | 76,359 | 70,237 | 600,000 (x50) | 7.9 | **420,000** | **5.5** | -8.3% | x35.0 |
| 16 | 76,359 | 81,543 | 600,000 (x50) | 7.9 | **490,000** | **6.4** | +7.0% | x40.83 |
| 17 | 76,359 | 94,669 | 600,000 (x50) | 7.9 | **570,000** | **7.5** | +24.4% | x47.5 |
| 18 | 76,359 | 109,908 | 600,000 (x50) | 7.9 | **570,000** | **7.5** | +24.4% | x47.5 |

### Enhanced Crafting Studio, F6+ (30,000): superseded vs adopted

Floors of liquid income across F3-F18: superseded 7.1 to 35.8, adopted 7.1 to 12.4.

| Floor | Liquid income / floor | Smoothed S | Superseded price (credit multiplier) | Superseded floors | **Adopted price** | **Adopted floors** | Deviation from target | Implied crafting multiplier |
|---|---|---|---|---|---|---|---|---|
| 6 | 4,191 | 4,294 | 150,000 (x5) | 35.8 | **43,000** | **10.3** | +2.6% | x1.43 |
| 7 | 4,191 | 4,986 | 150,000 (x5) | 35.8 | **50,000** | **11.9** | +19.3% | x1.67 |
| 8 | 4,191 | 5,788 | 150,000 (x5) | 35.8 | **50,000** | **11.9** | +19.3% | x1.67 |
| 9 | 18,208 | 14,007 | 150,000 (x5) | 8.2 | **140,000** | **7.7** | -23.1% | x4.67 |
| 10 | 23,600 | 18,514 | 600,000 (x20) | 25.4 | **185,000** | **7.8** | -21.6% | x6.17 |
| 11 | 23,600 | 21,494 | 600,000 (x20) | 25.4 | **215,000** | **9.1** | -8.9% | x7.17 |
| 12 | 23,600 | 24,953 | 600,000 (x20) | 25.4 | **250,000** | **10.6** | +5.9% | x8.33 |
| 13 | 84,428 | 54,795 | 600,000 (x20) | 7.1 | **600,000** | **7.1** | -28.9% | x20.0 |
| 14 | 84,428 | 63,615 | 600,000 (x20) | 7.1 | **635,000** | **7.5** | -24.8% | x21.17 |
| 15 | 76,359 | 70,237 | 1,500,000 (x50) | 19.6 | **700,000** | **9.2** | -8.3% | x23.33 |
| 16 | 76,359 | 81,543 | 1,500,000 (x50) | 19.6 | **815,000** | **10.7** | +6.7% | x27.17 |
| 17 | 76,359 | 94,669 | 1,500,000 (x50) | 19.6 | **945,000** | **12.4** | +23.8% | x31.5 |
| 18 | 76,359 | 109,908 | 1,500,000 (x50) | 19.6 | **945,000** | **12.4** | +23.8% | x31.5 |

**Caveats.**
- Targets are met on average, not floor by floor: income is stepped (box tiers) and prices are smooth, so the ratio is lower right after an income step (F9, F13) and higher right before one (F8, F12) by design.
- Income F3-F18 is itself a placeholder (no F3+ decks), so the schedule must be rerun if the growth table changes.
- Prices rise with the trend even when F15-F18 income dips (non-decreasing rule), so the F15-18 ratios drift up; that is the cost of keeping prices smooth.
- Applied in rules/20 (current section 9.1a; sections 0, 2.5.3, 9.1 and 10 cite this schedule instead of the credit multiplier for the three workstation prices).
