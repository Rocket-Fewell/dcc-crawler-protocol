# Full Audit of /workspace/dcc-lore (2026-10-04)
Owner: DCC Lore (audit run for Caleb) | Status: review | Version: 1.0 | Updated: 2026-10-04
Summary: Checklist and results of the all-files audit: schema and ID integrity, "champ" hits, stale statements after today's decisions, credit/tier consistency, canon-accuracy flags, leftover drafts, copyright, lore vs campaign copies, sealed-roll leakage; plus the rules/45 power-ladder conflicts on Story Box cards 0056-0059 (report only, no edits). Lists what was fixed and what needs another agent or Caleb.
Depends on: rules/40 v0.1.3, rules/42 v0.2, rules/45 v0.1, rules/50 v0.1.2 (all read-only in dcc-campaign).

Scope: decks, tables, tools, ledger, guides, drafts, audits, sources (by name/size/grep), catalog, status files, INDEX files. `gm-notes/secret/` was never opened. `ledger_build.py` was not run. `raw/pages` (2,017 wiki mirror files) and `sources/*` transcripts were checked by grep only, not read.

## 1. Checklist (what was run)
| # | Check | Method | Result |
|--|---|---|---|
| a1 | Duplicate card ids | script over all 6 f01 decks | 94 cards, 0 duplicates, numbering gap-free per zone (any 1-60, z03 1-8, z06 1-7, z09 1-15, z10 1-4) |
| a2 | Ids referenced but missing | regex `f01-<zone>-NNNN` over every .md/.py/.json | none missing |
| a3 | deck_check / ledger_check | run | deck_check 0 errors 0 warnings; ledger_check 1,268 quotes, 0 failures |
| a4 | Ledger id uniqueness, next-free table | regex over CANON-LEDGER.md | 1,154 row ids, 0 duplicates; max A-190, M-239, X-056, L-022 match ledger-rules.md (one stale row fixed, F2) |
| a5 | Version numbers | read headers | ledger 1.8 = INDEX 1.8; tables/INDEX 0.7; ledger-rules 1.6 (separate file, own number); guides 0.2 |
| a6 | Broken links / paths in INDEX and status docs | script | 4 real breaks fixed (F4-F6); the rest are historical (_archive, Pass 1-3 tables) or default output paths |
| b | "champ"/"champs" | grep -w and -i | 3 hits, all in tables/gm-quirks.json (section 3). "Champion" appears only as canon text in catalog/ledger/sources, not as address |
| c | Stale statements | grep + read | see section 5 |
| d | Credit/tier ranges | script vs Bronze 0-100, Silver 150-400, Legendary story_value 20k-250k | all pass; see section 6 for 0-weight cards |
| e | Canon-accuracy flags | ledger scan | section 7 |
| f | Leftover drafts | read headers | section 8 |
| g | Copyright (quotes <=25 words) | ledger_check + regex over guides/drafts/audits/status | no quote over 25 words; sources/ holds third-party transcripts and wiki mirrors (not book text) |
| h | Lore vs campaign copies | cmp | 6 loot decks in campaign/tables/loot-decks are symlinks to the lore files (identical). `ach-f01-orientation-pit.json` is intentionally not linked. `dcc-campaign/lore` is a symlink to dcc-lore. No divergent copies found |
| i | Sealed-roll leakage | filename + grep of shared lore files | none found (section 9) |

## 2. Issues found and fixes
| # | Sev | Issue | Action |
|--|---|---|---|
| F1 | Med | Story Box cards 0056-0060 differed from Syndicate's rules/42 v0.2 text | **Fixed**: card JSON copied verbatim into `loot_decks_build.py`; ids, weights, story_values unchanged; deck_check 0 errors |
| F1a | Low | rules/42 spoken_line/reward for 0057 (27 words) and 0060 (28 words) broke the 25-word rule | **Fixed** by trimming in Lore's build (Syndicate to adopt) |
| F1b | Low | rules/42 gives 0057 action_cost "30 seconds of focus (outside combat)"; deck_check enum rejects it | **Fixed**: card uses "Action: 30 seconds of focus (outside combat)"; deck_check accepts "<enum>: qualifier" |
| F1c | Low | Enhanced Pet Biscuit 0055 lacked the rules/45 §4.5 power_note | **Fixed** (notes only, no mechanics change) |
| F2 | Low | ledger-rules.md "next free" row for section 15 said M-228 | **Fixed** (points to section 16; the M- row above is current) |
| F3 | Low | "TODO 34 / 35" used twice in status-and-todo.md | **Fixed**: second set is 34b / 35b |
| F4 | Low | status TODO 38 and the research draft named a deck file `f01-any-legendary-storybox.json` that does not exist | **Fixed** (real name f01-any-story-boxes.json) |
| F5 | Low | floors-and-plot-by-book.md linked `books-1-2-6-7-detail.md`, `books-5-8-detail.md` without `catalog/` | **Fixed** |
| F6 | Low | INDEX.md: orientation-pit row said schema 0.1.1 and 14/55 card counts were stale; no row for story-box deck, guides, drafts, this audit | **Fixed** |
| F7 | Low | Card note "Public Fan Profile hook: dogs." on the Snack Box card (public tags were dropped) | **Fixed**: "Tailor tag: dogs (hidden tailoring only, no public tag)" |
| F8 | Low | Build-script comment said spec 2.8 needs Caleb's approval | **Fixed** (approved 2026-10-04) |
| F9 | Low | Pass 13 status said canon_status CANON on 0056/0057/0060 | **Fixed** (all five CANON-INSPIRED) |
| F10 | Low | gm-achievement-loot-audit O9 (Bone's 5 Bronze boxes = DRIFT) had no decision note | **Fixed**: decision recorded (alpha freebie stays) |
| F11 | Med | GM malfunction guides (long and short) had TBD items | **Fixed**: both rewritten to rules/50 v0.1.2, 0 TBD |
| F12 | Info | `LEDGER-RULES.md` and `ledger-rules.md` both exist (case-only difference; fails on case-insensitive file systems) | Not changed (the upper-case file is a pointer stub made on request); Caleb/Borent may delete it |

## 3. "champ" hits
Only `tables/gm-quirks.json` (GM-side quirk text, not card text; left alone as instructed for VT-03):
- FX-14 line 1298: insults field ("Circling the drain, champ.")
- QK-01 line 1770: narration field ("I remember Floor 2, champ.")
- VT-03 line 2109: description ("rotating nickname: champ, sport, chief, Sunshine") - known
FX-14 and QK-01 are not on the known list. Decision for Caleb: leave as in-fiction GM insults, or change to "Crawler". No deck, achievement-deck, build-script or audit file contains "champ".

## 4. rules/45 power-ladder conflicts (as found at 5:19 PM; RESOLVED by the 6:10 PM retune, see section 11)
rules/45 §4.1 (v0.1): Floors 1-2 numbers must sit in the core §3.6 ceiling (Common default, Uncommon peak); rung 2 max = one small Advantage/Disadvantage, or damage up to 1d6, or DC up to 12, once per long rest; combat numbers mean Common or Uncommon; **never** a permanent bonus to AC, saves, attack, damage, spell DC, ability score, HP or speed; no extra action, attack or reaction; no healing or revival; no attunement; dormant strong parts unlock by level 3 or Floor 3. All depend on Caleb's rules/45 question 2.
| Card | Conflict with rules/45 |
|---|---|
| **0056** Tiara of Bloody Succession (Uncommon, no attunement) | (1) Passive +2 to Intelligence checks is a permanent numeric bonus, always on (rung 2 allows one Advantage per long rest). (2) The Poisoned rider triggers every turn on 18+ and uses DC 12 (at the cap) but is not once per long rest; it is an on-hit combat rider. (3) Advantage on the first Persuasion check against each new creature is repeatable, not once per rest. (4) No dormant/unlock structure. |
| **0057** Grudge Ring (Rare, attunement) | (1) Rare label with a combat-adjacent effect breaks rule 3 (Common or Uncommon). (2) Attunement is on the "never" list. (3) Full hit-point restore on mark death is a healing effect (the "never" list), and the no-healing curse changes how healing works. (4) Heroic Inspiration payout is reasonable but repeats once per Long Rest, not once. (5) Already flagged as rules/42 question 9 (core §3.6 Uncommon ceiling). |
| **0058** Olive Branch Lanyard (Uncommon) | Save DC 13 is above the DC 12 cap. Otherwise in the ladder: once per Long Rest, uses the Reaction (not an extra one), no damage. |
| **0059** Wheel-Hub Maul (Uncommon, +1 maul) | (1) +1 to attack and damage is a permanent attack/damage bonus (the "never" list). (2) The push/Prone is once per Short Rest, not Long Rest (rung 2 is per long rest). The DC 12 Strength save is at the cap. |
| 0060 Pet Biscuit Crate (not asked, noted) | 1d4 healing to pets, up to 3 per pet per Long Rest: "healing" is on the "never" list unless pets are excluded; 500 biscuits are a bulk consumable, not one "R3 consumable". |
| 0055 Enhanced Pet Biscuit | Consistent: pattern C keystone, power_note now added per §4.5. |
Also noted: rules/45 proposes 0061 Little Crown (Quadruped deed A-165) and 0062 Grudge Pin (A-167 family-fight deed). These are second cards for the same canon boxes already covered by 0056 and 0057; with a one-box-per-floor cap and "a deed kind pays once", one of each pair would be a duplicate unless Caleb picks. No edits were made to 0056-0059 beyond the rules/42 text.

**New cards f01-any-0061..0065:** not present in any lore deck (deck max id is 0060; no file mentions them except rules/45). They are proposals; add to `f01-any-story-boxes.json` only after Syndicate confirms. Their schema looks addable: `action_cost` "none" in 0061 is a lower-case enum value already accepted by deck_check; their `power_note:` lines are present in the notes.

## 5. Stale-statement checks (after today's decisions)
| Decision | Result |
|---|---|
| Story Boxes allowed on Floors 1-2 (hand-picked, one named deed, cap one per floor; items were "bound" until Caleb ruled them lootable and sellable later on 2026-10-04, so this audit's references to "bound" Story Boxes are superseded) | Lore files updated (build script, INDEX, status, draft HOLD marked superseded). Remaining: rules/45 §5.3/§8 (Syndicate) mention rules/40 wording still to fix; not a lore file |
| Fan Profile tags screen S12 dropped / no public tags | No "S12" or public-tag wording in lore. One card note fixed (F7). Syndicate's own note: rules/40 §1.1 `tailor_tags` ("Public Fan Profile hooks only") and §2.4 still say public; `tailor_tags` remain in the card schema as hidden tailoring tags. Campaign file, not edited |
| Busted is spontaneous only | Guides updated; no other lore file mentions prompts, fees or guess limits |
| Bone's 5 Bronze boxes stay (alpha freebie) | Recorded in audit O9 (F10) |
| Quirk roll stays sealed | No roll value, quirk name or tell in guides, drafts, audits, tables INDEX. `catalog/gm-quirk-framework.md` is a stub pointing to gm-notes/secret |
| "Quadruped" means any quadruped | 0056 and the research draft say so; mechanics.md "Quadrupeds (e.g. Donut)" is canon wording |
| "Cat-tier" reading | audits/gm-achievement-loot-audit.md reads it as Crazy Cat Lady (Bronze Pet Box) vs Trailblazing Crazy Cat Lady (Legendary Pet Box). Consistent with the Story Box deck |
| rules/45 | Added as a dependency in the check list; 0055 power_note applied; ladder conflicts listed in section 4 |

## 6. Credit/tier consistency
All Bronze cards are 0-100, Silver 150-400 (deck_check). Story Box cards have credit_value 0 and story_value 20,000-80,000 (inside 20k-250k). Cards with draw_weight 0 that are not Story Boxes are intentional hand-picks: f01-any-0026 and 0027 (Horn items), 0028 (Bone's Wifebeater), 0052 (Duffel, pending spec §5 Q5), z09-0001 (Odd Coin fallback), z09-0014 (Gaffer Wristbands). The Grudge Ring's Rare rarity is above the Floor 1-2 Uncommon ceiling (flagged on the card, open question 9). No card id, weight or value was changed in this audit.

## 7. Canon accuracy flags
- Of 891 ledger rows tagged VERIFIED, about 766 rest on a single W: (wiki) source family; the ledger's own section 0 defines VERIFIED as "wiki chapter cite or two source families, not a book check". No novel text was checked by any pass.
- Open conflicts: 56 X- rows (29 with OPEN/UNRESOLVED/UNVERIFIED text). New this pass series: X-054 (Spirit Box tier, Legendary preferred), X-055 (Pet Box recipient, Carl vs Donut), X-056 (biscuit chapter B1 ch5 vs ch6). The 0057 card notes cite X-054.
- Unchecked TODOs: 34 (Ascendency competitors), 35 (Orthrus wording), 36 (B5 ch53 / B6 ch46 cites), 34b/35b (Borent quirk tooling; Caleb +3 band), 39 (re-check X-054/X-055), 41-43 (Borent story_value fix, Syndicate card folding, Caleb values), 44-46 (this audit's hand-offs).

## 8. Leftover drafts
- `drafts/f01-legendary-oneoffs-research.md`: header now says prep, deck built, LEG-05..07 superseded; HOLD line already marked superseded. Keep as research record.
- `_archive/*` and `parts/_archive/*` are marked archive; `work/*` is scratch (INDEX says safe to overwrite). `work/CANON-LEDGER.pre-pass7.bak` is a backup of an older ledger (373 KB class file); safe to delete when Caleb agrees.
- All other files are Status draft/review; none needs a superseded marker.

## 9. Sealed-roll leakage
No quirk id, fixation name, tic, tell or roll value appears in guides, drafts, audits, status or INDEX files. `tables/gm-quirks.json` holds the full quirk tables (not the rolled values) in the lore folder; `catalog/gm-quirk-framework.md` was already moved to gm-notes/secret as a stub. Recommendation for Borent/Caleb: keep `tables/gm-quirks.json` out of player-visible exports and out of the commitment hash inputs list; also `dcc-campaign/sessions/rolls-2026-10-04.log` exists and should stay out of any shared export (filename only; not opened).

## 10. Needs another agent or Caleb
- **Caleb:** rules/45 question 2 (how strong 0056-0059 may be) and the four-card conflict list in section 4; open question 9 (Rare ring); whether to change "champ" in FX-14, QK-01, VT-03; whether to delete `LEDGER-RULES.md` and the pre-pass7 backup.
- **Syndicate:** adopt the trimmed spoken lines for 0057/0060 and the 0057 action_cost wording; confirm rules/45 cards 0061-0065 (and resolve the duplicate quadruped/kin deeds vs 0056/0057); update rules/40 §1.1/§2.4 public Fan Profile wording.
- **Borent:** `state.py` `_loot_draw` story_value fix (`card.get("story_value") or card.get("credit_value") or 0`); keep gm-quirks.json and the rolls log out of shared exports.
- **Accountant:** story_value line for the five cards (20,000-80,000).

## 11. Change log
| Time (CT) | Change |
|---|---|
| 5:19 PM | Audit written; rules/42 v0.2 cards applied; guides rewritten. |
| 5:30-5:40 PM | Story Box items made not bound (`bound: false`), `sale_value` added, deck-level safe-room note. Audit sections 4-5 text about "bound" is superseded. |
| 6:05 PM | 0055 power note reworded (consumed once, pet-Crawler not tradable, separate player-controlled Crawler with no extra slot); sale_value 0055 and 0060 = 100, 0056-0059 = 500; 0057 Grudge Ring on HOLD (needs retune to fictional rival / no kills / no PvP; weight 0). Cards 0061-0065 deliberately not added (Syndicate: drafts until Caleb answers rules/45 question 2); section 4 conflict list still applies. Channel label #dcc_mouth replaced with #gm-voice in this folder's audit file. Crafting table: no lore doc uses the old 25,000-credit house price. |
| 6:10 PM | Caleb approved rules/45 cards 0061-0065 and deferred strength to Lore. Added 0061-0065 (reviewed; fixes listed in tables/INDEX.md v0.10). Retuned 0056, 0057, 0058, 0059 to the ladder; 0057 HOLD removed; section 4 conflicts resolved. Deck now has 10 Story Box cards; deck_check 0 errors, 0 warnings. |
| 6:40 PM | JOB 1: 0063 truce is a Wis save DC 12; 0065 'every Crawler pictured', recharge 'floor' (deck_check RECHARGE enum added). JOB 2: tables/item-reskins.json/.md added (189 SRD 5.2 items, srd_id scheme, reference base_price). Details in tables/INDEX.md v0.11.
