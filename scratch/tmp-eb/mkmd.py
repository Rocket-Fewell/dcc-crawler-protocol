import json
R="/workspace/dcc-campaign/"
d=json.load(open(R+"rules/70-encounter-budget-5e.json"))
F=d["floors"]; E=d["economy_audit"]; sm=d["day01_slot_map"]["slots"]
o=[]
w=o.append
w("# Encounter Budget, Credits and Loot (5e 2024), companion to 70-encounter-budget-5e.json")
w("Owner: Syndicate | Status: draft | Version: 0.1.11 | Updated: 2026-10-04")
w("Summary: Human companion to `rules/70-encounter-budget-5e.json` v0.1.11, the only source the Encounter Bot cites for difficulty, XP budgets, CR caps, credits, loot-box odds and clock prices. 2024 XP-budget method for 2, 3 and 4 Crawlers on Floors 1-6, a formula for Floors 7-18, the per-floor credit arithmetic for Floors 1-2 against the Accountant's 1,500-per-Crawler-per-floor line, a proposed flag-line curve for Floors 3-18, rest/key/Detour Tax prices, safe-room adjacency fields, the Day 1 slot map (32 slots after the v0.1.2 refresh) and the Day 2-4 slot map (9 slots).")
w("")
w("> **Authority.** Budgets are guidelines, not enforced. The GM has authority to adapt as play goes (Caleb, 2026-10-04). Players are always **Crawlers**. Nothing here changes Story Box rules (one named deed per Floor 1-2, GM-handed, opened only in a saferoom; 0% in every odds table below) or the Floor 1 Reprieve (Floor 1 only). Filed by Caleb's go-ahead (\"Go ahead and write the budget file\").")
w("> **Tags.** AUTH = follows a filed source. ASSUMED = my proposal, GM/Caleb may change it (ids A1-A14 in section 10). The JSON repeats the split: `authoritative` vs `assumed`.")
w("")
w("**Changelog.** 0.1.11: wording only, no values changed: the Legendary cap of 2 is per Crawler (core v0.2.17 §4.5), not campaign-wide; Story Boxes noted as a separate track outside the cap and this budget. 0.1.10: provenance re-sync after Floor 1 achievement-ref swap to ACH-1824..1826; no values changed (sans-pin hashes re-synced; the method now also skips the achievements catalog version and sha). 0.1.9: provenance-only: slot maps now match on sans-pin spec hash so budget bumps no longer break provenance; no values changed (`spec_sha256_sans_pin_when_mapped` replaces `spec_sha256_when_mapped`; Day 5 hash recorded in `day05_slot_map`, no slots). 0.1.8 (no value changed): rules/20 version cites replaced by 'current section 9.1a'; slot-map provenance hashes (`spec_sha256_when_mapped`) re-synced to the current specs (provenance only; the v0.1.7 'every other value unchanged' did not cover them; all slot paths re-checked and still resolve); ratio-check averages now unrounded, 3.01 / 6.03 / 9.89. 0.1.7: Accountant YES on Q-004 (6 of 7; Encounter Bot pending) with three accepted price fixes (F8 held at F7, F13 raised to 180,000 / 360,000 / 600,000, F18 held at F17); ratio check added (section 13); stale cumulative_check / reading_the_table text fixed; flag lines and all other values unchanged. 0.1.6 (no value changed): the crafting-price schedule (section 13) is ADOPTED via room vote Q-004 and applied in rules/20 v0.3.4; Floors 1-2 keep 5,000 / 12,000 / 30,000. 0.1.5 (after the Accountant's re-audit of v0.1.4; no number changed): F15 income dip stated as intended; ONE F3+ flag rule (2.165 x expected counted income, nearest 500, not a fixed multiple of 1,500, this file is the loot tool's source of truth); new `flag_line_by_floor` map; tool-change wording fixed (it now exists); 'cash' became 'credits' in player-facing text; DRAFT-ONLY crafting-price schedule (section 13, Q-004). 0.1.4: Q2 re-resolved by room vote (Q-001 as revised, 6 of 6): F4/F5/F6 = 20/25/30 days, house rule; canon timers 10/15/17 (M-603..M-608) reference only; F7+ held at 30 days (ASSUMED); F4-F6 per-day figures and the Floors 3-18 growth curve recomputed; Floors 1-2 unchanged. 0.1.3: Q2 resolved as placeholders, F4/F5/F6 = 10/15/17 days (tagged inspired, Lore canon timers M-603..M-608; Caleb can adjust); per-day figures and the Floors 3-18 growth curve recomputed (F7+ held at 17 days). 0.1.2: Day 2-4 encounter fields (section 3), slot map refreshed with stale slots 3 and 4 removed (section 9), Floors 3-18 flag-line proposal (section 8). 0.1.1: audit line restated per Crawler per floor, box means re-derived from the live decks, governor demoted, simulations rerun from the live decks, death-on-missed-collapse applied, Floor 3 = 20 days. 0.1.0: first filing. No field path has been renamed or removed since 0.1.0.")
w("")
w("## 1. Method (2024 encounter building)")
w("1. Per-Crawler XP budget by level (SRD 5.2.1 table, same one the Floor 1 overview uses): Low / Moderate / High. Multiply by party size P. No group multiplier in 2024. AUTH")
w("2. Four tiers map onto the bands. **Floor 1** (matches overview 9.2): trivial = half of Low, standard = Low, hard = Moderate, boss = High. **Floors 2+**: trivial = Low, standard = Moderate, hard = High (an elite, avoidable or telegraphed), boss = High with support (core 8.3: mostly Moderate, some Low, 1-3 High per floor). ASSUMED for F2+ (A1)")
w("3. Monsters carry XP by CR (SRD table, in the JSON). Spend the budget without going over; pick any SRD 5.2.1 creature at or under the tier's **CR cap**, reskin it (core 8.1), fill the rest with lower-CR support. No stat blocks here. More than two creatures per Crawler: include fragile ones (SRD, matters at levels 1-2).")
w("4. **CR cap** = min(core 8.3 upper bound for the tier, highest CR whose XP fits the tier budget). Bosses use 90% of the High total for the lead so support has room (A2).")
w("5. Levels follow the standard track (core 2.2): arrive on Floor N at level N. Floor 1 is the exception: level 1 until the Green Room (Z9), level 2 after (core 2.3, overview rule 3), so the Z10 boss budgets at level 2. AUTH.")
w("")
w("## 2. Clock, rests and encounters per floor")
w("Days are a field (`floors.N.clock.days`); everything below recomputes from it. Each day: 1 Long Rest (honest saferoom only) and a **cap** of 4 short-rest slots (decision 026). Encounters are a ceiling envelope, not a quota.")
w("")
w("| Floor | Level (arrive-leave) | Days | Short-rest slots (cap, total) | Long Rests | Planned encounters (trivial/standard/hard/boss) | Per day |")
w("|---|---|---|---|---|---|---|")
for f in "123456":
    x=F[f]; c=x["clock"]; m=x["encounters"]["mix_planned"]
    lv = "1-2 (level 2 at Z9)" if f=="1" else "%d-%d"%(int(f),int(f)+1)
    days = str(c["days"]) + (" (Caleb)" if f=="3" else " (placeholder)" if int(f)>=4 else "")
    w("| %s | %s | %s | %d | %d | %d (%d/%d/%d/%d) | %s |"%(f,lv,days,c["short_rest_slots_total_cap"],c["long_rests_total"],x["encounters"]["total_planned"],m["trivial"],m["standard"],m["hard"],m["boss"],x["encounters"]["per_day_typical"]))
w("")
w("- Floor 1 is the module's fixed list (Z2, Z5, Z7 standard; Z8 hard; wandering Ceiling Ticks trivial, max 2 on the floor; Z10 boss), 4-8 total per core 10.3. AUTH. F1 days 5 / F2 10 / F3 20 are decision 026 (F3 = 20 by Caleb's later ruling); F4-F6 days (20/25/30) are a HOUSE RULE by room vote (Q-001 as revised; Caleb can veto or change; GM-adaptable; A4); Lore's canon timers 10/15/17 (M-603..M-608) are reference only.")
w("- F2+ formula (A3): total = round(days x 1.5); boss 1, hard = 15% of the rest (min 1), trivial = 25%, standard = remainder. Floor 3 at 20 days gives 30 encounters (7/18/4/1).")
w("")
w("## 3. XP budgets and CR caps (Floors 1-6)")
w("Tier budget in XP for the party (per-Crawler band x P). CR caps in brackets. Full tables for 2, 3, 4 and for F1 level 1 vs 2 are in the JSON (`floors.N.tiers`).")
w("")
def row(f,L,P):
    t=F[f]["tiers"]["L%d"%L]; b=t["xp_budget_total"][str(P)]; c=t["cr_caps"][str(P)]
    return "| %s | L%d | %d | %s | %s | %s | %s |"%(f,L,P,*["%d (CR %s)"%(b[k],c[k]) for k in ("trivial","standard","hard","boss")])
w("| Floor | Lvl | Crawlers | Trivial | Standard | Hard | Boss |")
w("|---|---|---|---|---|---|---|")
for f,L in (("1",1),("1",2),("2",2),("3",3),("4",4),("5",5),("6",6)):
    for P in (4,3,2):
        w(row(f,L,P))
w("")
w("Rows are party sizes 4, 3, 2 for each floor and level. F1 L1 is everything before the Green Room; F1 L2 is the Z10 boss. Boss lead CR below core 8.3's minimum (e.g. 2 Crawlers on F5) is deliberate: the core row assumes four.")
w("")
w("### Daily XP budget (the party's XP envelope per day)")
w("Daily budget = sum of planned tier budgets / days. Caps (A3): a normal day holds at most 1 hard + 2 standard + 1 trivial; a boss day, the boss + 1 standard. The 2024 SRD has no adventuring-day XP table, so these are house guidelines.")
w("")
w("| Floor | 4 Crawlers: daily budget (per Crawler) | normal-day cap | boss-day cap | 3 Crawlers daily | 2 Crawlers daily |")
w("|---|---|---|---|---|---|")
for f in "123456":
    x=F[f]["xp"]["by_party_size"]
    w("| %s | %g (%g) | %d | %d | %g | %g |"%(f,x["4"]["daily_xp_budget_typical"],x["4"]["daily_xp_budget_per_crawler"],x["4"]["daily_xp_cap_normal_day"],x["4"]["daily_xp_cap_boss_day"],x["3"]["daily_xp_budget_typical"],x["2"]["daily_xp_budget_typical"]))
w("")
w("Floors 1-2 for 4 Crawlers: **Floor 1 = 360 XP/day** (1,800 over 5 days: Z2 200 + Z5 200 + Z7 200 + Z8 300 + Ticks 100 + boss 800 at tier ceilings; the overview's actual counts use 1,600), **Floor 2 = 880 XP/day** (8,800 over 10 days: 4 trivial x 400 + 8 standard x 600 + 2 hard x 800 + boss 800).")
w("")
w("### Floor 1 fixed encounters (mirror overview 9.2/9.3, AUTH)")
w("| Zone | Tier | 2 Crawlers | 3 Crawlers | 4 Crawlers |")
w("|---|---|---|---|---|")
names={"z02":"Z2 Vent Rats","z05":"Z5 Mannequin Staff","z07":"Z7 Exit Greeters","z08":"Z8 Elite","wandering":"W Ceiling Ticks","z10":"Z10 Dean Thudd"}
for z,n in names.items():
    v=F["1"]["fixed_encounters"][z]
    cells=[]
    for P in "234":
        cn=", ".join("%dx %s"%(c,s) for s,c in v["counts_by_party_size"][P].items() if c)
        fit=v["fit"][P]
        cells.append("%s = %d XP / %d%s"%(cn,fit["xp_used"],fit["tier_budget"]," **over by %d**"%fit["over_by"] if fit["over_by"] else ""))
    w("| %s | %s | %s | %s | %s |"%(n,v["tier"],*cells))
w("")
w("The overview runs the Z8 elite above the Moderate budget for 2 Crawlers (Animated Armor alone, 200 vs 150, called \"High for 2\" in overview 9.3) and for 3 (250 vs 225). I kept the overview's counts and flagged the overage (`fit.over_by`); the GM may tighten. Z10 for 2 Crawlers is overview Variant B (Bugbear Warrior + 4 Skeletons); Skeleton counts are totals across both phases.")
w("")
w("### Floor 1 Days 2-4 house-built encounters (v0.1.2, ASSUMED)")
w("Added for the Encounter Bot (new keys `floors.1.fixed_encounters.d02_02`, `d03_02`, `d03_03`, `d04_03`; index in `floors.1.fixed_encounters._day_encounter_index`). All are conditional or avoidable and budgeted at level 1 from the same F1 tier budgets (trivial = half of Low, standard = Low); if the table already has level 2, counts stay inside the level-2 budget in `tier_budget_if_level_2` and the GM may add creatures up to it.")
w("")
w("| Spec encounter | Key | Tier | 2 Crawlers | 3 Crawlers | 4 Crawlers | Why |")
w("|---|---|---|---|---|---|---|")
for z in ("d02_02","d03_02","d03_03","d04_03"):
    v=F["1"]["fixed_encounters"][z]; cells=[]
    for P in "234":
        cn=", ".join("%dx %s"%(c,s_) for s_,c in v["counts_by_party_size"][P].items() if c)
        fit=v["fit"][P]; cells.append("%s = %d / %d XP"%(cn,fit["xp_used"],fit["tier_budget"]))
    w("| %s %s | `%s` | %s | %s | %s | %s | %s |"%(v["spec_encounter_id"],v["name"].split(" (")[0],z,v["tier"],*cells,v["reasoning"]))
w("")
ee=F["1"]["fixed_encounters"]["_day_encounter_economy"]
w("Effect on the budget: if every one fires, Floor 1 has 10 encounters (core 10.3 says 4-8, so the GM may drop any), and the added XP per day for 4 Crawlers is Day 2 %d, Day 3 %d, Day 4 %d, each inside the typical daily budget of 360. Only `d03_02` pays cash (standard tier, 5 credits per Crawler expected); none carries a box, so `economy_audit` is unchanged. Ushers are Skeletons (CR 1/4, 50 XP); the Ticks of `d03_02` count toward the floor's wandering cap of two if the GM uses them."%(ee["xp_added_per_day_if_all_fire_4_crawlers"]["day_2"],ee["xp_added_per_day_if_all_fire_4_crawlers"]["day_3"],ee["xp_added_per_day_if_all_fire_4_crawlers"]["day_4"]))
w("")
w("## 4. Credits and loot, with the arithmetic")
w("**Line (corrected in v0.1.1): about 1,500 credits per Crawler per FLOOR**, not Floors 1 and 2 combined. Verified in `rules/40-loot-deck-spec-5e.md` 3.2 (audit hint: per crawler per floor on F1-2, box `credit_value` should land around 300-1,000; above about 1,500 is inflation to flag), `rules/45-story-boxes-5e.md` 6.3 item 4 and change row C2 (\"1,500-per-floor inflation flag\", sale proceeds count, flag not block) and `tools/loot.py` `INFLATION_FLAG = 1500` (tested per crawler per floor). Each floor is audited on its own; no combined total is audited or claimed.")
w("")
w("**What counts.** By default `tools/loot.py` counts only box value (`economy_value` of drawn cards, credit pulls as rolled) plus Story Box sale proceeds; it does not see encounter credits or R1 toast credits. `state.py loot totals --include-credits` (optional `--credit-sources`, `--assume-floor N`; record the floor with `state.py credits ... --floor N`) adds the credits earned outside boxes, so each floor is shown two ways: **box-only** (comparable to the default `loot totals`) and **all-in** (encounter credits + R1 + boxes, the stricter reading, comparable to `--include-credits`). Not counted: Story Box `story_value`, vendor spending (sinks), resale at half (already counted at `credit_value`), placed goods.")
w("")
w("**Box means, re-derived in v0.1.1 from the live decks** (`tables/loot-decks/f01-*.json`, Story Box deck excluded; cards filtered like `tools/loot.py`: `draw_weight` above 0, no stubs, no Legendary/Celestial, `box_types` any or the box's type). v0.1.0 selected cards by `kind` instead of `pull_type`, which gave a Silver box of 429.5; the live decks give about 481. Pull type by core 4.2 d100 (30/25/15/18/10, 99-00 re-rolls Silver). Credit cards use their grant roll (Bronze 3d6 x 5 = 52.5, Silver 2d6 x 25 = 175). Script: `tools-notes/encounter_budget_econ.py` (read-only).")
pe=E["pull_expectations"]; mb=pe["pull_type_means_bronze_pooled"]; ms=pe["pull_type_means_silver_boss"]; u=pe["used_in_budget"]
w("")
w("| Mean (credits) | Consumable | Gear | Credits | Tailored | Weird |")
w("|---|---|---|---|---|---|")
w("| Bronze pull type, all F1 decks pooled | %.2f | %.2f | %.2f | %.2f | %.2f |"%(mb["consumable"],mb["gear"],mb["credits"],mb["tailored"],mb["weird"]))
w("| Silver pull type, Boss Box (z10 Boss + any) | %.2f | %.2f | %.2f | %.2f | %.2f |"%(ms["consumable"],ms["gear"],ms["credits"],ms["tailored"],ms["weird"]))
w("")
w("- Silver pull = (.30 x %.2f + .25 x %.2f + .15 x %.0f + .18 x %.2f + .10 x %.2f) / .98 = **%.2f**. Silver Boss Box (2 pulls) = **%.1f**."%(ms["consumable"],ms["gear"],ms["credits"],ms["tailored"],ms["weird"],u["silver_pull_mean"],u["silver_box_mean_2_pulls"]))
w("- Bronze pull (pooled) = .30 x %.2f + .25 x %.2f + .15 x %.1f + .18 x %.2f + .10 x %.2f + .02 x %.2f (upgrade to a Silver pull) = **%.3f**. Bronze box (1-2 pulls, average 1.5) = **%.2f**."%(mb["consumable"],mb["gear"],mb["credits"],mb["tailored"],mb["weird"],pe["scopes"]["pooled_floor"]["silver_pull"],u["bronze_pull_mean"],u["bronze_box_mean_1_5_pulls"]))
w("- Welcome Box (Break Room, decks z06 + any; pull 1 tailored, pull 2 d100) = %.2f + %.2f = **%.2f**."%(pe["scopes"]["any+z06"]["bronze_pull_type_means"]["tailored"],pe["scopes"]["any+z06"]["bronze_pull"],u["welcome_box_mean"]))
w("- Other deck scopes (any only, any+z03, any+z09, all pooled) move the Bronze box between %.1f and %.1f and the Silver box between %.0f and %.0f; the full list is in `economy_audit.pull_expectations.scopes`."%(min(pe["scopes"][k]["bronze_box_1_5_pulls"] for k in ("any_only","any+z03","any+z06","any+z09","pooled_floor")),max(pe["scopes"][k]["bronze_box_1_5_pulls"] for k in ("any_only","any+z03","any+z06","any+z09","pooled_floor")),min(pe["scopes"][k]["silver_box_2_pulls"] for k in ("any_only","any+z09","z10_boss","pooled_floor")),max(pe["scopes"][k]["silver_box_2_pulls"] for k in ("any_only","any+z09","z10_boss","pooled_floor"))))
w("- Analytic means are with replacement; Floor 2 reuses the Floor 1 decks (no F2 decks yet, A8); \"two consumables at one tier lower\" is ignored.")
w("")
w("**Encounter cash per Crawler** (F1 scale, ASSUMED A5; the pool is this x P, split evenly): trivial 0-2 (average 1; F1 Ticks and F1 trivial 0), standard 1d4 x 2 (5), hard 1d6 x 2 (7), boss 1d6 x 5 (17.5). **R1 toast credits** 10-40 (average 25), 2 on F1 and 3 on F2 per Crawler (A6).")
w("")
for fl,key in (("Floor 1","floor_1"),("Floor 2","floor_2")):
    w("**%s, expected per Crawler**"%fl)
    w("")
    for r in E[key]["rows"]:
        w("- %s: **%.1f** (%s)%s"%(r["item"],r["expected_credits"],r["arithmetic"]," [box]" if r["counts_in_loot_totals"] else " [cash]"))
    w("- **%s all-in: %.1f** (%.1f%% of 1,500). **Box-only: %.1f** (%.1f%% of 1,500)."%(fl,E[key]["expected_total_per_crawler"],E[key]["share_of_line_all_in"]*100,E[key]["expected_box_only_per_crawler"],E[key]["share_of_line_box_only"]*100))
    w("")
w("Box odds per encounter are the fight share of core 4.5's targets: F1 standard 6%, hard 23% (Bronze), boss Silver 100% **only if the boss is fought or talked down**; F2 standard 7%, hard 28%, boss Silver 100%. Non-fight deed Bronze adds 0.5 (F1) and 0.9 (F2). Soft cap 2-3 achievement boxes per Crawler per floor. No Gold, no second Silver, no Story Box from these odds.")
w("")
w("| Crawlers | F1 all-in per Crawler | F2 all-in per Crawler | F1 / F2 box-only | Cash pool F1 / F2 (x P) | Table total F1 / F2 (all-in) |")
w("|---|---|---|---|---|---|")
for P in "234":
    b=E["by_party_size"][P]
    w("| %s | %.1f | %.1f | %.1f / %.1f | %.1f / %.1f | %.1f / %.1f |"%(P,b["per_crawler_f1_all_in"],b["per_crawler_f2_all_in"],b["per_crawler_f1_box_only"],b["per_crawler_f2_box_only"],b["cash_pool_f1"],b["cash_pool_f2"],b["table_total_f1_all_in"],b["table_total_f2_all_in"]))
w("")
w("**Credits per Crawler do not rise with party size.** Encounter cash is a per-Crawler figure, so the pool **scales** with P and then **splits** evenly among living Crawlers; boxes belong to each Crawler and are never split or traded (core 4.4).")
w("")
sc=E["simulation"]["scenarios"]
w("**Simulation from the live decks** (`tools-notes/encounter_budget_econ.py`, %s Crawlers per scenario, seed %s, real cards drawn, non-consumables not repeated per Crawler per floor; rerun it to reproduce). Share of Crawler-floors above 1,500:"%(sc["base"]["n"],sc["base"]["seed"]))
w("")
w("| Scenario | Floor | Mean | p90 | p99 | Max | Over 1,500 |")
w("|---|---|---|---|---|---|---|")
for nm,lab in (("base","Plan (this file)"),("pacing_ceiling","Core 4.5 ceiling: 4 Bronze + Silver, 5 R1 toasts"),("base_with_valve_900","Plan with optional valve at 900"),("pacing_ceiling_with_valve_900","Ceiling with optional valve at 900")):
    for fl_,k in (("F1 all-in","f1_all"),("F2 all-in","f2_all"),("F1 box-only","f1_box"),("F2 box-only","f2_box")):
        x=sc[nm]["result"][k]
        w("| %s | %s | %.1f | %d | %d | %d | %.2f%% |"%(lab,fl_,x["mean"],x["p90"],x["p99"],x["max"],x["pct_over_1500"]))
w("")
w("The with-replacement check (%d Crawlers) gives F1 %.1f and F2 %.1f all-in against the analytic %.1f and %.1f. The v0.1.0 claim (13.2%% to 3.1%%) came from a combined-line script that is not filed and is **withdrawn**."%(sc["with_replacement_check"]["n"],sc["with_replacement_check"]["result"]["f1_all"]["mean"],sc["with_replacement_check"]["result"]["f2_all"]["mean"],E["floor_1"]["expected_total_per_crawler"],E["floor_2"]["expected_total_per_crawler"]))
g=E["governor"]
w("")
w("**Governor: demoted to an OPTIONAL safety valve (A12).** With the line read per floor the plan sits at %.0f%% and %.0f%% of it all-in, and almost no Crawler-floor crosses it, so the valve is not needed to stay under the line. If a Floor 2 looks hot, the GM may hand-pick the Boss Box from cards worth 175 or less when that Crawler's running total on that floor reaches 900. Simulated effect: F2 all-in over 1,500 goes %s in the plan and %s at the pacing ceiling. **Tool:** the change now exists (Q-003 passed; built by the Architect): `state.py loot totals --include-credits` (optional `--credit-sources`, `--assume-floor N`; `state.py credits ... --floor N`) shows the all-in running total the valve needs, and the default output is unchanged. This file made no tool change."%(E["floor_1"]["share_of_line_all_in"]*100,E["floor_2"]["share_of_line_all_in"]*100,g["effect_simulated"]["base_f2_all_in_over_1500"],g["effect_simulated"]["pacing_ceiling_f2_all_in_over_1500"]))
w("A Story Box item *sale* (100 / 250 / 500 by rung, times the sale floor's multiplier) counts on the floor of the sale; the Accountant flags, never blocks.")
w("")
w("### Floors 3-6 (outside the audited line; ASSUMED)")
w("Same tier dice times a cash scale equal to the floor's credit multiplier (x1 F3-4, x5 F5-6; A9). Expected encounter cash per Crawler: " + ", ".join("F%s %g"%(f,F[f]["credits"]["cash_expected_per_crawler"]) for f in "3456") + ". Box odds per encounter (ASSUMED, core 4.5 pacing): "+"; ".join("F%s standard Bronze %s, hard Bronze %s / Silver %s, boss %s 100%%"%(f,F[f]["boxes"]["odds_per_encounter_by_tier"]["standard"].get("Bronze"),F[f]["boxes"]["odds_per_encounter_by_tier"]["hard"].get("Bronze"),F[f]["boxes"]["odds_per_encounter_by_tier"]["hard"].get("Silver"),F[f]["boxes"]["expected_fight_boxes_per_crawler"]["boss_box"]) for f in "3456")+". The per-floor flag line for Floors 3-18 is proposed in section 8.")
w("")
w("## 5. Prices and costs (Floor 1, all ASSUMED unless noted)")
w("System fees multiply by the floor credit multiplier (decision 019); all of these are x1 on Floor 1. Party prices are per-Crawler x P so small tables are not punished; any Crawler may pay, pooling allowed.")
w("")
w("| Item | Per Crawler | Party of 2 / 3 / 4 | Reasoning |")
w("|---|---|---|---|")
p=F["1"]["prices"]
w("| Potion of Healing at the Snakk-Matic (AUTH, overview 5.6/8.3) | 50 | 2 in stock floor-wide | Existing price, buys back at half |")
w("| Rest without a saferoom (no Long Rest is granted; Ticks interrupt after 1d4 hours) | 20, cap 60 per floor | 40 / 60 / 80 | 40% of a potion; three billings = 4% of a floor's line. A saferoom is free (Z9 stays open to the end), so it only has to sting |")
w("| Stairwell key, terminal bribe (Z6 Break Room, gone Day 4) | 50 | 100 / 150 / 200 | One potion each (3.3%% of a floor's 1,500 line); using the key to skip the Z10 fight also forfeits the Silver Boss Box (about %d expected), so cheap in credits, dear in opportunity |"%round(E["pull_expectations"]["used_in_budget"]["silver_box_mean_2_pulls"]))
w("| Detour Tax (**missed Stairwell key only**) | 75 | 150 / 225 / 300 | 1.5x the bribe: waiting costs more than buying early; 5% of a floor's line. Shortfall: pay what they have, GM logs the balance. **Not a collapse toll** |")
w("| Forcing the Zone S door (Thieves' Tools or Athletics DC 15, 10 min, loud; Thudd and Ushers arrive 1 minute later, overview 5.10) | 25 | 50 / 75 / 100 | Cheapest in credits because it already costs danger. Order: forcing 25 < bribe 50 < Detour Tax 75 |")
w("| Detour (back to Z8 or Z6 while they serve) | 0 | 2 in-game hours, 0 rest slots | 4 extra Ceiling Tick rolls (d6 per 30 minutes) |")
w("| Collapse steps (outer, mid, Break Room) | 0 | 0 | They cost hooks and services only; the Detour Tax (missed key) is the only credit toll on the clock |")
w("| **Missed floor collapse** | none | none | **Death on every floor. No Reprieve, no toll, no Exhaustion price** (decision 026, Caleb, ~10:02 PM CT). Credits and items are destroyed with the floor; survivors may loot only while it stands (decision 028). The GM warns clearly at Floor 1 start and on Days 4 and 5; stasis counts as reaching a stairwell |")
w("")
w("Worst case for one Crawler on Floor 1 (Detour Tax 75 + rest cap 60) = 135 = 9% of the floor's line. These are sinks, not income, so they do not count against the 1,500.")
w("")
w("## 6. Safe-room adjacency (fields in `floors.N.adjacency`, ASSUMED A11)")
w("- Boss arena within **1 zone (one door)** of an honest saferoom on F1-2 (Z10 is one door from the Z9 Green Room, overview 6.7); within 2 on F3+. Hard encounters within 1 zone on F1 (Z8 sits between Z6 and Z9), 2 on F2+.")
w("- **No more than 3 encounters between rests**, and at most **1 hard-or-boss** per rest segment. Offer, never force, a rest before the boss. A Crawler should never be more than two fights from an honest saferoom on F1-2.")
w("- Wandering: F1 max 2 on the floor (AUTH, overview 5.11); F2+ max 1 per day. At least 2 saferooms per floor. Saferooms can lie from F2 (core 5.6). Break Room is a saferoom through Day 3 only; Z9 is the only one after (decision 026).")
w("")
w("## 7. Pets, companions, class features, PvP (brief)")
w("Pets are GM-run, do not count toward P, and take no XP, loot or credits (rules/60); do not rebuild budgets for them, the GM may add one CR 1/4 (50 XP) to the enemy side if a fight is close. The 2-Crawler Assigned Companion does not count toward P. No adjustment for Second Wind or other class features (the 2024 budgets assume them). No PvP: nothing here pays for attacking a Crawler.")
w("")
w("## 8. Floors 7-18 and the proposed flag-line curve (PLACEHOLDER, GM/Caleb adaptable)")
w("`floors_7_18` gives, per floor, only what the sources already fix: level = floor number, per-Crawler Low/Moderate/High at that level, core 8.3 CR ranges and the credit multiplier. Days, mix and cash are placeholders. The table below (`proposed_floor_growth_curve`, added for the Accountant's per-floor audit table) proposes the **flag line per Crawler per floor** for Floors 3-18. Everything from Floor 3 is a proposal; the Floor 1-2 lines (1,500) are authoritative.")
G=d["proposed_floor_growth_curve"]
w("")
w("**How it is built.** (1) Cash and R1 credits take the core 3.9 multiplier (x1 F1-4, x5 F5-9, x20 F10-14, x50 F15-18). (2) Box counts are the midpoint of core 4.5's range per floor (Legendary 0.5 on F13-14, 0.25 on F15-18, so each Crawler's total stays at 2 (core §4.5 per-Crawler cap)). (3) Bronze and Silver box values come from the live decks; Gold, Platinum and Legendary pulls = .15 x credit-pull mean (2d6 x 250 / 2,500 / 10,000) + .85 x the geometric midpoint of the rules/40 3.2 item range (500-5,000, 5,000-50,000, 20,000-250,000). That method puts a Silver item pull within about 12% of the live decks (223 vs 251). No F3+ decks exist yet. (4) Days beyond Floor 3 are placeholders: +5 per floor to a cap of 60. (5) Flag line = the cushion Floors 1-2 carry (1,500 over the average of their expected totals, about @@Kx), rounded to the nearest 500.".replace("@@K","%.2f"%(1500/((E["floor_1"]["expected_total_per_crawler"]+E["floor_2"]["expected_total_per_crawler"])/2))))
w("")
w("**ONE rule for F3+ flag lines.** Flag line = **2.165 x expected counted income** for that floor, rounded to the nearest 500. 2.165 is the cushion the authoritative F1-F2 line carries over expected income (1,500 / mean of the F1 and F2 all-in totals, %.1f). It is **not a fixed multiple of 1,500** and not one number per band. Floors 1-2 stay at 1,500. **This file's flag lines are the source of truth for the loot tool**; the map is `flag_line_by_floor` (F1..F18), equal to the table's `flag_line` column, for the Architect to load in place of the fixed `INFLATION_FLAG = 1500`."%((E["per_floor_summary"]["1"]["all_in"]+E["per_floor_summary"]["2"]["all_in"])/2))
w("")
T14=[x for x in d["proposed_floor_growth_curve"]["table"] if x["floor"]==14][0]; T15=[x for x in d["proposed_floor_growth_curve"]["table"] if x["floor"]==15][0]
w("**The F15 dip is intended.** Expected income falls from %s (F14) to %s (F15), and the flag line from %s to %s, on purpose: Legendary boxes are 0.5 per Crawler on F13-14 and 0.25 on F15-18, which keeps each Crawler's Legendary total at 2 (core §4.5 per-Crawler cap), even though the multiplier steps up to x50. Flag lines are **not required to be monotonic** there."%(format(T14["expected_counted"],","),format(T15["expected_counted"],","),format(T14["flag_line"],","),format(T15["flag_line"],",")))
w("")
w("Story Boxes (F1-2) are a separate track outside the Legendary cap and outside this budget (core §4.1/4.5/4.7).")
w("")
w("`flag_line_by_floor`: "+", ".join("F%s %s"%(k,format(v,",")) for k,v in d["flag_line_by_floor"].items())+".")
w("")
w("**Growth rate (geometric mean per floor, expected counted income):** "+", ".join("%s %s"%(k,v) for k,v in G["growth_rate"]["per_band_geometric_mean"].items())+". The curve is steppy, not smooth: it jumps at F3 (first Gold box, 20-day floor), F9 (first Platinum), F13 (Legendary) and rises on F5, F10 and F15 mainly through the multiplier on cash and R1 credits.")
w("")
w("| Floor | Days | Mult | Cash + R1 | Boxes | Expected | Ceiling case | **Flag line** | Growth vs prior | Liquid (items sold at half) | Basic table 5,000 x mult: floors of liquid income | Studio 12,000 x mult | Enhanced 30,000 x mult (F6+) |")
w("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in G["table"]:
    if r["floor"]<3:
        w("| %d | %d | x1 | (see section 4) | | %.0f | | **1,500** | | | | | |"%(r["floor"],r["days"],r["expected_counted"])); continue
    w("| %d | %d | x%d | %s | %s | %s | %s | **%s** | %s | %s | %s | %s | %s |"%(r["floor"],r["days"],r["credit_multiplier"],format(r["cash_plus_r1"],","),format(r["boxes_counted"],","),format(r["expected_counted"],","),format(r["pacing_ceiling_counted"],","),format(r["flag_line"],","),r["growth_vs_previous"],format(r["liquid_if_items_sold_at_half"],","),r["floors_of_liquid_income_basic_table"],r["floors_of_liquid_income_studio"],r["floors_of_liquid_income_enhanced"] if r["floors_of_liquid_income_enhanced"] is not None else "-"))
w("")
for t in G["reading_the_table"]: w("- "+t)
w("- "+G["cumulative_check"])
w("- Reasoning for the shape: the line is tied to the same boxes the core already schedules (core 4.5), so it needs no new reward promise; it grows where the core grows (first Gold, Platinum, Legendary) and where fees grow (the multiplier). The mismatch with crafting prices is reported rather than hidden (Q6).")
w("")
w("## 9. Slot maps")
w("")
w("**Provenance (v0.1.10).** Each slot map records the Day spec's **sans-pin** hash (pins on this file, the canon table and the achievements catalog removed before hashing) (`spec_sha256_sans_pin_when_mapped`; method in `day01_slot_map.spec_hash_method`, helper `python3 tools/encounter_bot/spec_hash_sans_pin.py floors/f01/day-NN.spec.json`), which ignores the spec's pin on this file, so a budget bump no longer breaks provenance. Day 1 %s, Days 2-4 %s, Day 5 %s (`day05_slot_map`, provenance only, no slots mapped)."%(d["day01_slot_map"]["spec_sha256_sans_pin_when_mapped"][:12]+"...", " / ".join(v[:12]+"..." for v in d["day02_to_04_slot_map"]["spec_sha256_sans_pin_when_mapped"].values()), d["day05_slot_map"]["spec_sha256_sans_pin_when_mapped"][:12]+"..."))
sm=d["day01_slot_map"]; D24=d["day02_to_04_slot_map"]
w("### Day 1 (%d slots; v0.1.2 refresh)"%sm["count"])
w("The Encounter Bot regenerated the Day 1 spec at 10:08 PM CT and now cites this file by field path (`b70` cites). All 153 cites in the Day 1-5 specs resolve against this file (checked). **Removed in v0.1.2: stale slots 3 and 4** (`/clock/collapse_miss/effects[2]` and `/clock/collapse_miss/toll_slot`, the old missed-collapse toll): a missed collapse is death with no toll (decision 026, decision 028). Slot numbers of the others are unchanged, so existing references still resolve. Slot 1 keeps the Detour Tax for a missed Stairwell key only.")
w("")
w("Naming scheme: `slot_no` = position in the 22:08 Day 1 map; `spec_path` = JSON path in the spec; `fills_from` = dotted path in this file; `value` or `value_by_party_size` (keys \"2\",\"3\",\"4\") = ready-to-paste fill. Cite as `rules/70-encounter-budget-5e.json#<fills_from>`.")
w("")
w("| # | Spec path | Label | Fill (2 / 3 / 4 Crawlers where it varies) |")
w("|---|---|---|---|")
for s_ in sm["slots"]:
    if "value_by_party_size" in s_:
        vv=s_["value_by_party_size"]
        if all(isinstance(v,(int,float)) for v in vv.values()):
            val=" / ".join(str(vv[k]) for k in "234")
        else:
            val=vv["4"]; val=(val[:110]+"...") if len(val)>113 else val
            val="(4) "+val+" (2 and 3 in JSON)"
    else:
        val=str(s_["value"]); val=(val[:130]+"...") if len(val)>133 else val
    w("| %d | `%s` | %s | %s |"%(s_["slot_no"],s_["spec_path"],s_["label"],val.replace("|","/")))
w("")
w("### Days 2-4 (%d slots, v0.1.2)"%D24["count"])
w("| Spec file | Spec path | Label | Cites | 2 / 3 / 4 Crawlers |")
w("|---|---|---|---|---|")
for s_ in D24["slots"]:
    vv=s_["value_by_party_size"]
    val=" / ".join(str(vv[k]) for k in "234") if all(isinstance(v,int) for v in vv.values()) else "see `fit` (tier budget and XP used)"
    w("| %s | `%s` | %s | `%s`%s | %s |"%(s_["spec_file"].split("/")[-1],s_["spec_path"],s_["label"],s_["fills_from"]," key `%s`"%s_["cite"]["key"] if "key" in s_["cite"] else "",val))
w("")
w("## 10. Assumptions (all ASSUMED, GM may adapt)")
for a in sorted(d["assumed"]["list"],key=lambda a:int(a["id"][1:])):
    w("- **%s** %s *(adjust: %s)*"%(a["id"],a["what"],a["adapt"]))
w("")
w("**Authoritative (follows a source):** SRD XP budget and XP-by-CR tables (CR 11-13 missing from my SRD extraction; standard values used, verify); level track (core 2.2/2.3); core 8.3 CR targets; box credit dice (core 4.2, no multiplier on pulls); box pacing and ceilings (core 4.5, 3.6, 4.7); credit multiplier (core 3.9, decision 019); clock days F1-F3, 4 short-rest slots (cap), 1 Long Rest, collapse order, zone groups, 32-hour stairwell, 6-hour stasis threshold, key deadlines, the fixed final collapse at hour 120 (a Syndicate default in decision 026 that Caleb may veto); a missed floor collapse is death on every floor with no Reprieve and no toll (Caleb ruling ~10:02 PM CT, decisions 026 and 028); Story Box limits (decisions 015/018, rules/45); Floor 1 encounter counts (overview 9.2/9.3); Potion price 50.")
w("")
w("## 11. Open questions for Caleb")
for q in d["open_questions"]:
    w("- "+q)
w("")
w("## 12. Changes for the room")
w("- Encounter Bot: new Day 2-4 fields are in `floors.1.fixed_encounters.d02_02 / d03_02 / d03_03 / d04_03`; re-pin to the new sha256 (the file's sha is recorded in decisions/027 and the indexes). CR slots for these encounters already resolve.")
w("- Accountant: use `proposed_floor_growth_curve.table` for the per-floor audit table (PLACEHOLDER); the Floor 1-2 flag is 1,500 per Crawler per floor; re-audit the live-deck box means (`economy_audit.pull_expectations`) and the simulations (`tools-notes/encounter_budget_econ.py`).")
w("- Architect: the all-in tool change exists (Q5 resolved); next, load `flag_line_by_floor` in place of the fixed 1500 for `INFLATION_FLAG` (this file is the source of truth for the flag lines). Lore: F2 loot decks should keep the Bronze/Silver value ranges used here (A8).")
Q=d["q6_crafting_price_proposal"]
w("")
w("## 13. Q6 proposal: crafting price schedule (ADOPTED via Q-004, 6 of 7 yes; v0.1.7 price tweaks; applied in rules/20 current §9.1a)")
w("")
w("**Status.** "+Q["status"])
w("")
w("**What it replaces.** "+Q["what_it_replaces"])
w("")
w("**What the targets are measured against.** "+Q["target_basis"])
w("")
w("**Targets (floors of liquid income, half-credit box items):** basic table 3, Crafting Studio (F4+) 6, Enhanced Crafting Studio (F6+) 10.")
w("")
w("**Method.**")
for t in Q["method"]: w("- "+t)
w("")
names={"basic_table":"Basic crafting table (5,000 at Floor-1 scale)","crafting_studio":"Crafting Studio, F4+ (12,000)","enhanced_studio":"Enhanced Crafting Studio, F6+ (30,000)"}
for k,nm in names.items():
    s_=Q["summary"][k]
    w("### "+nm+": superseded vs adopted")
    w("")
    w("Floors of liquid income across F3-F18: superseded %s to %s, adopted %s to %s."%(s_["current_floors_range"][0],s_["current_floors_range"][1],s_["proposed_floors_range"][0],s_["proposed_floors_range"][1]))
    w("")
    w("| Floor | Liquid income / floor | Smoothed S | Superseded price (credit multiplier) | Superseded floors | **Adopted price** | **Adopted floors** | Deviation from target | Implied crafting multiplier |")
    w("|---|---|---|---|---|---|---|---|---|")
    for r in Q["table"]:
        x=r[k]
        if not x: continue
        w("| %d | %s | %s | %s (x%d) | %s | **%s** | **%s** | %+.1f%% | x%s |"%(r["floor"],format(r["liquid_income_per_floor"],","),format(r["smoothed_income"],","),format(x["current_price"],","),r["credit_multiplier"],x["current_floors_of_liquid_income"],format(x["proposed_price"],","),x["proposed_floors_of_liquid_income"],x["deviation_from_target_pct"],x["implied_crafting_multiplier"]))
    w("")
w("**Caveats.**")
for t in Q["caveats"]: w("- "+t)
import re as _re
def decash(t):
    for a_,b_ in [("cash credits","encounter credits"),("Cash credits","Encounter credits"),("encounter cash","encounter credits"),("Encounter cash","Encounter credits"),("[cash]","[credits]"),("Cash dice","Credit dice"),("cash dice","credit dice"),("cash:","credits:"),("pays cash","pays credits"),("Cash and R1","Encounter credits and R1"),("on cash and R1","on encounter credits and R1"),("(cash","(encounter credits"),("cash +","encounter credits +"),("table's cash","table's encounter credits"),("mixes, cash","mixes, encounter credits")]:
        t=t.replace(a_,b_)
    t=_re.sub(r"\bcash\b","encounter credits",t); t=_re.sub(r"\bCash\b","Encounter credits",t)
    return t.replace("encounter encounter","encounter").replace("Encounter encounter","Encounter")
o[:]=[decash(x) if not x.startswith("**Changelog.**") else x for x in o]
open(R+"rules/70-encounter-budget-5e.md","w").write("\n".join(o)+"\n")
print(len("\n".join(o)))
