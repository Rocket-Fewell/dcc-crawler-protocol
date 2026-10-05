# GM principles audit (Lore)
Owner: DCC Lore | Status: review | Version: 0.2 | Updated: 2026-10-04
Summary: Read-only audit of the GM's principles (gm-notes/00, 10, 20, 30, 31, INDEX) against the Lore ledger, audits, Story Box rulings, Lore's pricing rulings, Busted, Costly Revives, multi-Crawler rules and the item reskin table. Lists contradictions with file, line and quote, canon-accuracy concerns, the three GM open questions, and decisions for Caleb.

Read at about 6:37-6:42 PM CT. `gm-notes/00-gm-principles.md` and `10-open-threads.md` were being edited while I read; Caleb's 6:38 / 6:39 / 6:40 PM CT answers are included below. Line numbers are as of 6:42 PM CT and may move. I did not open `gm-notes/secret/` or anything sealed. Nothing outside `audits/` was changed.

Files compared: dcc-campaign `gm-notes/*` (non-secret), `rules/10, 20, 40, 42, 45, 50`, `decisions/005, 015, 017, 019, 020`, `characters/create-flow-spec-5e.md`, `floors/f01/00-overview.md`, `exports/sheet-*.md`, `sessions/session-01-recap-2026-10-04.md`; dcc-lore `CANON-LEDGER.md`, `mechanics.md`, `catalog/mechanics-clarifications.md`, `raw/pages/Loot Boxes.txt`, `audits/*.md`, `status-and-todo.md`, `tables/item-reskins.json` (v0.1.1, sha256 e271cb366b51; the campaign copy matches).

## Resolutions (Caleb's rulings of 2026-10-04, applied by Lore in Pass 17)
These overrule the "Recommended" lines below where they differ. Marked in place as RESOLVED.

| Item | Ruling | Effect |
|---|---|---|
| D-1 / question (c) | RESOLVED. Crafting Studio is about 12,000 and Enhanced Studio about 30,000, each at Floor-1 scale times the floor multiplier. The basic table stays 5,000. | Overrules my 20,000 / 50,000 recommendation. rules/20 (lines 135, 814-815, 888 and the 0.3.2 flag) is now stale: Syndicate must change it to 12,000 / 30,000. The GM note was right. The Enhanced Studio at Floor 6+ (x5) is now 150,000, still above the 25,000 coupon cap, so the 0.3.2 flag stays open for the Accountant. |
| D-2 / G-5 | RESOLVED. Floor 1 Reprieve is ON for Floor 1 only. | Matches session 1 (both Reprieves spent). Syndicate: record it in the Floor 1 module (line 954, remove the open question) and say in core §6.2 that it expires on Floor 2. |
| D-3 / G-3 | RESOLVED. An unopened Story Box is reclaimed if its Crawler dies before a safe room, and the slot is freed. | Overrules rules/45 §6.3 ("deed stays closed, cap stays used") and my option 1. Lore changed the notes on all Story Box cards (f01-any-0055 to 0065) and the deck notes in `tools/loot_decks_build.py`; decks regenerated. Syndicate: update rules/45 §6.3 (line 363) and gm-notes/31. |
| D-5 | RESOLVED. Old item names stay as stored on live sheets; lookup is by `srd_id`. | Option 1. Lore added the missing `legacy_names` (reskin table v0.1.2); no `srd_id` or chargen key changed. Names with no SRD item are listed below. |
| D-7 | RESOLVED. GM persona unchanged. | Overrules my "carnival barker" recommendation. C-8 is closed as "no change": leave "game show host" in both persona prompts. The foot bit stays where it is. |

Still open: D-4 (slot cycling) and D-6 (two-player deed wording).

Live-sheet names that do not map to an SRD item (they stay as stored; no `legacy_names` entry is possible): Pencil & Paper (writing kit); Light Crossbow + 20 Bolts (a bundle of `light-crossbow` and `bolts`); Dog leash clipped to nothing (Pebbles's); ORIENTATION PIT Banner (stolen hallway canvas); Tanya Ruiz Lore Scrap; Bone's Own Chewing Tobacco (Fan Pull); Laminated Complaint Card; Pebbles Snow Globe (Driftglobe); Eternally Stained Wifebeater (Cloak of Many Fashions reskin); Collapsible Tent-Pole (Pole of Collapsing); Kevin the Sentient Rubber Duck; Gas-Station Bathroom Key on a Hubcap (Mystery Key). These are house, magic or story items outside the 189-entry SRD equipment table.

Added to the table as legacy names: Box Cutters (dagger), Food Blocks / Discount Jerky Cubes / Discount Gas-Station Jerky Cubes (rations), Mop-Handle Staff (quarterstaff), Steel Mirror (mirror), Reinforced Absorbing Gloves (club), Sports Drink, Red / Blue Flavor (potion-of-healing), Ziplock Pouches (pouch), Torches (torch). "Expired Office First-Aid Kit" was already there. Ledger row L-023 (unopened boxes cannot be sold or transferred) is added.

## 1. Scorecard: what the principles already get right
| Check | Result |
|---|---|
| "Crawlers", never "champs" | OK. No player-facing text contains it. `tables/gm-quirks.json` has 0 hits now (it had 3 at the 5:19 PM audit; fixed since). Minor: see C-13. |
| Story Box: Floors 1-2 only, one per floor, hand-pick, named deed, not bound, announced at award, opens only in a safe room | OK in 00 (line 85, 91-92) and 31 (how-to). Matches core §4.1/§4.4, rules/45 §1.2 rows 5, 9, rules/40 §2.8. |
| Deleting a Crawler frees its Story Box slot | OK (00 line 103; decision 020; rules/45 §1.2 row 5). |
| Pet-biscuit = one conversion per living pet-Crawler | OK in 00 line 93, 31 line 24, decision 020, rules/42 §6.3 limits, create-flow §8.4 item 12. Stale copies: C-4. |
| Box credit pulls get NO floor multiplier; crafting prices and System fees DO | Rules agree (core §4.2 line 438, rules/20 §0 line 53, rules/40 §3.2, rules/45 §4.6, decision 019). **The principles file never states it** (gap G-1). |
| Buyback = fixed `sale_value` per rung x sale-floor multiplier, never `story_value` | OK in 31 line 22. 00 line 92 shows the `sell` command but not the price rule (G-1). |
| Busted: never prompted, same tell, only "Busted." / "Not busted.", one call per Crawler per scene, no penalty | 00 line 83 and 10 line 162 cover "never prompt", "tell logged first", "answer only its output". Missing: one call per Crawler per scene, same tell every time, no penalty (G-2). No contradiction with rules/50 §6.2 or decision 017. |
| Costly Revives, very costly and rare | OK in intent. One wrong detail: C-1. |
| Multi-Crawler / active Crawler / session lock / `/delete` | Mostly OK. Two wording conflicts: C-2, C-3. |
| Item names `Our Name (5e Name)` from the reskin table, prices by `srd_id` | OK (00 line 104). Live sheets still use old names: C-10. |

## 2. Contradictions found
Quotes are under 25 words. "Fix" is a suggestion; the owner of each file applies it.

| # | File and line | Quote | Conflicts with | Suggested fix |
|---|---|---|---|---|
| C-1 | gm-notes/00-gm-principles.md:31 | "every revive pays a fee plus a menu pick (see rules/ section 6)" | rules/10 §6.4.4 (line 776): "TWO picks from the Costly Revive Menu"; decision 005: "TWO different picks". | Say "a fee plus TWO different menu picks (at most one Celestial Tax)". |
| C-2 | 00-gm-principles.md:100 | "one is active per campaign" | decision 020 (line 14): "Exactly one active Crawler per player"; create-flow §8. | "one is active per player". |
| C-3 | 00-gm-principles.md:103 | "I log deletions for audit only; never flag or penalize players for them." | decision 020 (line 10): "the GM flags suspected Crawler-cycling to Caleb". Also 00 omits that the active Crawler cannot be deleted while a session is open (decision 020 line 9). | Reword: "never penalize; but flag suspected Crawler-cycling (delete, recreate, re-earn a Story Box) to Caleb". Add the open-session block. This is Decision D-4. |
| C-4 | rules/45-story-boxes-5e.md:88 | "One Enhanced Pet Biscuit per pet, ever; no crafting or duplicating a second one." | New ruling: one conversion per living pet-Crawler. | "One conversion per living pet-Crawler; a deleted pet-Crawler frees its conversion; a new conversion needs a new Enhanced Pet Biscuit (a Story Box slot)". |
| C-4b | rules/42-house-items-f01.md:350 (card JSON text) | "One biscuit per pet, once." | rules/42:323 (its own limits line) and the Lore deck (fixed 6:33 PM). | Replace with the deck wording on card f01-any-0055. |
| C-4c | decisions/015-story-boxes.md:17 | "no extra slot, once per pet, consumes the biscuit" | decision 020 (line 17). | "one conversion per living pet-Crawler". |
| C-5 | gm-notes/10-open-threads.md:18 | "table price and coupon cap stay 25,000" | rules/20 lines 135, 813, 888: basic table 5,000 (Caleb, 2026-10-04); coupon cap stays 25,000. 00 line 112 agrees with rules/20. | Mark the line superseded: table 5,000, coupon cap 25,000. |
| C-6 | 00-gm-principles.md:109 | "Crafting station prices (Studio ~12,000, Enhanced Studio ~30,000) still unanswered." | rules/20 lines 135, 814-815: Crafting Studio 20,000, Enhanced Studio 50,000 (HR, Floor-1 scale). | These numbers are not in the rules. See open question (c). |
| C-7 | 00-gm-principles.md:78 and rules/45:328, floors/f01/00-overview.md:47, 715 | "Open call for Caleb: Bone got 5 Bronze vs Floor 1 cap of 2"; "Cap: 2 per crawler on F1"; rules/45: "the Floor 1 cap of two achievement boxes per Crawler (GM principles)" | 00 line 74 and 111 now say a SOFT guideline of about 2-3 per Crawler per floor (Caleb 6:40 PM CT); 00 line 110: Caleb never set a hard 2 cap. | Update line 78 (answered: Bone's 5 stay as alpha-only). Floor doc §8.2 and line 47: "2-3, soft". rules/45:328: cite the soft guideline, not a cap. My own gm-achievement-loot-audit.md O9 and checklist lines say "cap of 2"; erratum added there (see section 7). |
| C-8 | gm-notes/20-gm-persona.md:6 and :9 | "washed-up, sleazy game show host" | 10-open-threads:23: "keep GM as bar-owner/carnival-barker (not game-show host, which is the System)"; 00 line 13 gives the System the "game-show host" voice; 20 line 21 itself separates the two. | Change both prompts to "washed-up carnival barker / bar owner". |
| C-9 | 00-gm-principles.md:77 | "Trailblazing <X>" ... "Silver max on Floor 1." | Ledger A-114 / M-230: canon's Trailblazing Crazy Cat Lady paid a **Legendary** Pet Box on Floor 1. Our Story Box exception (rules/45 row 5) now covers exactly this deed. | Add "except a Story Box deed (rules/45)". |
| C-10 | exports/sheet-horn.md:21-26 and sheet-bone-wifebeater.md:12, 27; gm-notes/30:18 | "Expired Office First-Aid Kit (Healer's Kit)"; "Food Blocks x30 (Rations)"; "Box Cutters x2 (Dagger)" | tables/item-reskins.json: Healer's Kit is "Break-Room First-Aid Kit, Lightly Bitten" (deck name reused); Rope, Ball Bearings, Mirror, Rations likewise. Sheet also writes "(Steel Mirror)", not an SRD name, and "Mop-Handle Staff (Quarterstaff)" vs "Duct-Taped Mop (Quarterstaff)". Card format puts the count before the parenthesis. | Lookup by `srd_id`; the old sheet names are in `legacy_names` except "Food Blocks", "Discount Jerky Cubes", "Mop-Handle Staff", "Steel Mirror" (Lore will add them on request). Decision D-5. Card format: "Box Cutter (Dagger) x2". |
| C-11 | rules/45-story-boxes-5e.md:283, 285 (example 5) and 251, 253 (example 3) | "Group Photo, Keepsake of the Four. While all four of you live..." ; "one smart hostile creature must hear you out for one minute." | Lore decks (JOB 1, 6:20 PM CT): 0065 says "every Crawler pictured", 0063 forces the truce with a Wisdom save, DC 12. Table is locked at 2 Crawlers (10-open-threads:26), so "all four" can never be met. | Syndicate to copy the deck text into examples 3 and 5; rules/45 §6.1-6.2 "all four" -> "every active Crawler". |
| C-12 | gm-notes/10-open-threads.md:143 | "Pebbles Snow Globe (Driftglobe, Common)" | Deck f01-any-0027 and sheet-horn: Uncommon (DMG 2024); 00 line 75: "Driftglobe is Uncommon". | Correct to Uncommon. |
| C-13 | 00-gm-principles.md:69, 84 vs characters/create-flow-spec-5e.md:573 | "Always say Crawlers, never 'champs'." | create-flow checklist: the address rule at line 3 "is the only mention allowed". | Reword lines 69 and 84 to "per the address rule" so a grep audit stays clean. Trivial. |
| C-14 | 10-open-threads.md:62 and 5, 11, 13 | "SPOTLIGHT RULE (Caleb): while in dialogue with one player, ignore all other players." Also "Needs a decisions/ file", "Canon ledger ... in progress" | 00 lines 38-46: spotlight rule superseded by the Exchange framework; decision 005 and the ledger exist. | Mark these stale or move to a history section. Also 00 line 85: "Exact commands pending from the Architect" is answered at lines 90-92. Header of 10 still says Version 0.1, Updated 2026-10-03. |
| C-15 | 00-gm-principles.md:27 | "Open only in a saferoom, not tradeable." | Reads as if it covers Story Box items (00 line 85: "traded, sold"). Caleb answered at 6:38 PM CT (line 107): unopened boxes cannot be traded; opened items can. | Reword line 27 to "Unopened boxes cannot be traded or sold; items inside can be, once opened in a safe room." |

## 3. Gaps in the principles (nothing contradicts, but the GM would act wrongly without them)
- **G-1 Pricing rulings.** Add: box credit pulls are never multiplied; achievement rewards, repairs, crafting prices and Story Box buyback are multiplied by the floor credit multiplier (x1 F1-4, x5 F5-9, x20 F10-14, x50 F15-18; decision 019). Revive Licensing Fees stay flat (core §6.4.3, decision 005), so "System fees multiply" has that one exception. The Celestial Tax pick does multiply (core §6.4.4 menu row 1). Buyback = fixed `sale_value` (100/250/500) x the multiplier of the floor where the sale happens; never `story_value`.
- **G-2 Busted.** Add: one call per Crawler per scene; a wrong call text cannot repeat; no penalty and no Stress; same tell for the same trigger; the call is valid only in a scene with a logged tell and a refusal reads "Not busted." (rules/50 §6.2, decision 017).
- **G-3 Death edge. RESOLVED (D-3).** A Story Box awarded but still unopened when its Crawler dies is reclaimed, the deed stays closed, and the floor slot stays used (rules/45 §6.3, line 363). The principles do not tell the GM this. See D-3.
- **G-4 Story Box how-to (31).** It lists five box names but not the five cards added later (0061-0065) or the rule "award only one of 0056 or 0061, and one of 0057 or 0062" (duplicate themes). It does not say how a table deed (0065) is recorded.
- **G-5 Floor 1 Reprieve. RESOLVED (D-2).** The live session used it twice (sessions/session-01-recap:8). Core §6.2 (line 689) says OFF by default and the Floor 1 module (line 954) still lists it as an open question. No file records that Caleb turned it on. See D-2.
- **G-6 Safe room wording.** Canon says a Safe Room or Guildhall (L-002, M-011). Our rule says safe room only; fine, but the Guildhall exists only in the tutorial.
- **G-7 "buff / boon" rewards.** 00 line 50 lists "buff / boon" as a reward; line 52 says rewards never change dice, DCs, damage, saves or revives. Clarify that a buff is narrative or capped by core §3 (otherwise the GM will hand out dice changes).

## 4. Canon-accuracy concerns
Ledger ids are in CANON-LEDGER.md. "HOUSE" is fine when labeled; these are the places where the labeling or the canon claim should be tightened.
1. **Box trading.** Canon: "Unopened boxes cannot be sold or transferred to other crawlers" (wiki Loot Boxes, cite B1 ch5; raw/pages/Loot Boxes.txt line 46; repeated in mechanics.md §8 and catalog/mechanics-clarifications 4.4). The **ledger has no row for it**: L-002 (locked until a safe room) and M-011 (open only in a Safe Room) cover the lock, not the trade ban. Lore should add a row (proposed id L-023, VERIFIED B1 ch5). Canon's default is the reverse for ordinary items: they transfer unless flagged non-transferable (C-020 Earth Hobby Potion) or change on transfer (M-129 Hunting Trophy); totems are freely traded (M-030, M-204). That supports Story Box items being tradeable once opened.
2. **Celestial cap.** Canon: no crawler has had more than four (L-008). One per Crawler is a HOUSE limit. Already labeled; keep. The "Syndicate tax" line is canon-grounded for hosts (mechanics-clarifications 4.2), so the System grumbling is right.
3. **Trailblazing.** Canon Trailblazing Crazy Cat Lady is unique, once per dungeon, and paid a Legendary Pet Box (A-114, M-229, M-230). C-9 above.
4. **Pet Box.** Canon gave Carl the Pet Box and the biscuit, and Donut the Quadruped Box (M-239, X-055); our pet-deed rule matches. Canon biscuit outcomes are random, "over 100 possible effects, half of which are good" (M-235), and the Enriched version resets the pet to level 1 (M-236, M-237). Ours (d4 Quirk, class at party level, always a Crawler) is a HOUSE softening; it should be labeled HOUSE, not "canon". Mordecai's advice to feed it only in a Safe Room (M-234, WIKI-ONLY) is not in the rules; consider adopting it as flavor.
5. **Achievement boxes on Floor 1.** Canon is much more generous: A-024 (Bronze Pet Box), A-035 (Silver Adventurer Box), A-037 and A-090 (Bronze), A-118 (Bronze) on the tutorial floor, and Gold or Platinum for rare deeds (A-094, A-110, A-124, A-133). mechanics.md §8: almost every achievement carries a box. A soft 2-3 per Crawler is a deliberate tightening; the floor rarity ceiling (core §3.6) still caps what is inside.
6. **Persona.** 20-gm-persona line 15 lists a "foot bit". In canon the foot jokes belong to the System AI (achievements A-094, A-110; mechanics.md §8, "the AI's foot fetish"). Keep the bit on the [SYSTEM] voice or tag it HOUSE for the GM. Also see C-8: "game show host" is the System's role.
7. **Crafting prices.** Canon prices are in gold (table about 25,000, K-011 and K-046; Enhanced Studio 255,000, K-007 and K-008, WIKI-ONLY; coupons up to 250,000, K-049). Ours are credits at a 1/5 scale. The ledger has no price for the basic Crafting Studio (K-005 gives capacity only), so any Studio number is HOUSE.
8. **Item-name format.** The reskin table is names only; magic-item names (Driftglobe, Cloak of Many Fashions, Story Box cards) come from the loot decks, not the table. Both use "Display Name (Real Name)". Consistent.

## 5. The three open questions the GM raised
Current rules text first, then the canon-grounded recommendation. Caleb has since answered (a) and (b); (c) is still open.

**(a) Can unopened loot boxes be traded?**
- Rules now: No. Core §4.4 (rules/10:453) "cannot be traded, gifted, or sold between crawlers, opened or not"; core §6.2 (line 702): reclaimed on death; rules/45 §6 item 6: "Unopened boxes cannot be traded or sold (core §4.4); only the opened item can." The GM's worry came from 00 line 27 versus Story Box items being tradeable (C-15).
- Canon: wiki Loot Boxes (B1 ch5), mechanics.md §8; no ledger row yet (section 4, item 1).
- Recommendation: No, all tiers including Story Boxes. **Caleb ruled this at 6:38 PM CT. Matches canon and the rules; nothing to change except the 00 line 27 wording (C-15) and adding the ledger row.**

**(b) Floor 1 achievement-box cap.**
- Rules now: floors/f01 §8.2 (line 715) "Cap: 2 per crawler on F1" (Bronze 0-2 plus the Welcome Box); core §4.5: Bronze 2-4, Silver 0-1 per floor; 00 line 74 now a soft 2-3 guideline.
- Canon: A-024, A-035, A-037, A-090, A-118 (all Floor 1) show boxes on most early achievements; ledger ids A-094, A-110, A-124 show Gold and Platinum for rare deeds.
- Recommendation: soft guideline of 2-3 ordinary achievement boxes per Crawler per floor, plus the Welcome Box, plus Story Boxes outside it. This is within the core §4.5 Bronze 2-4 range if the Welcome Box is counted. **Caleb ruled 2-3 soft at 6:40 PM CT; agree.** Cleanups: C-7 (floor doc, rules/45:328, 00 line 78, my older audit). Bone's 5 Bronze stay as an alpha-only freebie (10-open-threads:151).

**(c) Crafting station prices. RESOLVED 2026-10-04: Studio about 12,000, Enhanced about 30,000 (see Resolutions).** Was unanswered in 00 (line 109), but the rules already contain numbers.
- Rules now (rules/20 lines 135, 814-815, 888, all Floor-1 scale, multiplied by the floor of purchase): basic table 5,000 (LOCKED, Caleb); Crafting Studio 20,000 [HR]; Enhanced Crafting Studio 50,000, Floor 6+ [HR]; level upgrades 5,000 x target level; coupons up to 25,000. The "Studio ~12,000 / Enhanced ~30,000" in the GM's note appear in no rules file.
- Canon: table about 25,000 gold (K-011, K-046); Enhanced Studio 255,000 gold (K-007, K-008, wiki infobox only); coupon cap 250,000 gold (K-049); basic Studio price not in the ledger.
- The house table is canon / 5 (25,000 -> 5,000). Applying the same factor to the Enhanced Studio gives 51,000, so 50,000 follows canon. 20,000 for the basic Studio is a house number (4 tables).
- Recommendation: keep rules/20 (Studio 20,000, Enhanced 50,000) and tell the GM those are the answers; delete the 12,000 / 30,000 guess. Open flag from rules/20 0.3.2: at Floor 6+ with the x5 multiplier the Enhanced Studio costs 250,000, above the 25,000 coupon cap. See D-1.

## 6. Decisions Caleb should make
Each has plain options and Lore's recommendation (marked **Recommended**).

**D-1. Crafting station prices and the multiplier. RESOLVED 2026-10-04: Studio about 12,000, Enhanced about 30,000, times the floor multiplier; basic table 5,000 (see Resolutions).**
1. Keep Studio 20,000 and Enhanced Studio 50,000 at Floor-1 scale, times the floor multiplier. **Recommended.** Canon-ratio for the Enhanced Studio; simplest; nothing to change in the rules.
2. Use the GM's 12,000 / 30,000. Cheaper, but not tied to canon or to any rules file.
3. Keep the numbers but stop multiplying crafting prices past Floor 5. Avoids a 250,000-credit Studio, but undoes the pricing ruling of 2026-10-04.
Also ask the Accountant whether earnings that do scale (achievement rewards, mob credits) keep pace with prices that scale, because box credit pulls do not scale.

**D-2. Is the Floor 1 Reprieve ON for this table? RESOLVED 2026-10-04: ON for Floor 1 only.** It was used twice in session 1 but no file says it is on.
1. Record it as ON for Floor 1 only, as used (both spent). **Recommended.** Matches what happened; core already expects it for new-to-5e tables; it expires on Floor 2.
2. Record it as an alpha-only exception; OFF for the real run.
3. Say it was a GM error and ruling the deaths real (harsh, and not what the table was told).

**D-3. Unopened Story Box when its Crawler dies before a safe room. RESOLVED 2026-10-04: reclaimed and the slot is freed.** Today the box is reclaimed, the deed stays closed and the slot stays used (rules/45 line 363).
1. Keep it. **Recommended.** Same as every unopened box; fits "death is nearly game over"; the GM can avoid it by awarding when a safe room is close.
2. Return the box to the party's next safe room as a "reissue", keeping the same deed. Kinder, but it bends the unopened-boxes-vanish rule (core §6.2).
3. Announce the award only on arrival at the safe room. No limbo, but it contradicts "announced at award time".

**D-4. Delete, recreate, re-earn (Story Box slot cycling).** `/delete` frees the slot (decision 020), and 00 line 103 says never flag it.
1. GM never penalizes, but flags suspected cycling to Caleb (decision 020 wording). **Recommended.** Keeps the "no punishment" tone and keeps Caleb in the loop.
2. Never flag (00 as written). Then the one-per-floor cap is easy to farm.
3. Add a hard rule (for example a deleted Crawler's slot is freed only after the floor ends). Strong, but Caleb already declined "a hard anti-farm rule".

**D-5. Rename items already on live sheets? RESOLVED 2026-10-04: no; old names stay as stored, lookup by `srd_id`.** The reskin table changed some names (for example "Expired Office First-Aid Kit" -> "Break-Room First-Aid Kit, Lightly Bitten"). Sheets store old names.
1. Do not rename live items; the sheet keeps its stored name, and new items use the table. Lookup is by `srd_id`, with legacy names mapped. **Recommended.** No confusion mid-run.
2. Rename everything at the next publish (consistent, but players see their gear change).
3. Ask each player.

**D-6. Table deed wording for a 2-player table.** rules/45 §6.2 still says "all four, or three plus a witness". Party is locked at 2.
1. "Every active Crawler, or all but one plus a witness." **Recommended.** Works at any party size; matches deck card 0065.
2. Keep "four" and let the GM adapt.

**D-7 (small). GM persona. RESOLVED 2026-10-04: persona unchanged.** Fix both persona prompts to "carnival barker / bar owner" (C-8), and decide whether the foot bit stays with the GM or moves to the System. **Recommended:** barker for the GM, foot bit to the System (canon A-094 / A-110).

## 7. What Lore will do next, and what I did not change
- Not changed (not mine): everything under dcc-campaign, including the stale lines in sections 2 and 3.
- Added: an erratum at the end of `audits/gm-achievement-loot-audit.md` (the "cap of 2" came from the Floor 1 module §8.2; Caleb never ratified it; the policy is now a soft 2-3).
- Done in Pass 17: ledger row L-023 (WIKI-ONLY); legacy names in the reskin table (v0.1.2); reclaim-and-free-the-slot notes on the Story Box cards. Ready on request: deck-text patches for rules/42 and rules/45 (C-4, C-11).
- Already done earlier today and still valid: deck card 0055 wording, `floor` recharge, 0063 save, 0065 wording (tables/INDEX.md v0.13).
