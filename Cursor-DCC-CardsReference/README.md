# Cursor DCC cards reference
Owner: Cursor (R&D) | Status: draft | Version: 0.2.0 | Updated: 2026-10-09
Summary: House encounter cards for grok bots. SRD 5.2.1 numbers, Dungeon Crawler Carl tone, tracked spell uses, full gear and loot-box cards. Not a live floor.

This folder is an R&D draw pile. Caleb asked for it without a room vote. It does not change `rules/`, `floors/`, `lore/CANON-LEDGER.md`, sessions, or credit ledgers.

Live Day pages and `rules/70-encounter-budget-5e.json` win if a card disagrees with them. Lore and Encounter Bot can hang stories on these cards later. Until they do, nothing here is filed for the table.

## What is in here

| Path | What |
|---|---|
| `monsters/monster-book.md` | Readable book. 72 cards, Floors 1–3. |
| `monsters/catalog.json` | The same 72 cards for a bot to load. |
| `monsters/f01.json` `f02.json` `f03.json` | The same cards split by floor. |
| `encounters/sample-recipes.json` | Eleven example lineups. Each one fits a rules/70 XP budget for 4 Crawlers. |
| `items/catalog.json` | 191 gear cards. One per filed reskin. List prices are copied. |
| `items/gear-book.md` | The same 191 cards, readable. |
| `items/loot-boxes.json` | 112 filed loot-deck cards, plus 46 rules/40 crosswalk rows. Charges are counters. |
| `items/loot-box-book.md` | The same loot cards, readable. |
| `achievements/catalog.json` | 24 house toasts. Snark or Heroic Inspiration. No new credit amounts and no boxes. |
| `00-how-bots-draw.md` | How a grok bot builds a random encounter from this pile. |
| `ATTRIBUTION.md` | CC BY 4.0 credit for the SRD text. |

## Counts

| Floor | Mobs | Units | Elites | Bosses |
|---:|---:|---:|---:|---:|
| 1 | 12 | 6 | 4 | 2 |
| 2 | 10 | 6 | 5 | 3 |
| 3 | 10 | 6 | 5 | 3 |

72 monsters. 191 gear cards. 112 loot-deck cards. 46 rules/40 crosswalk rows. 24 achievements.

## Rules these cards already obey

- Players are Crawlers. The rest room is a saferoom. Money is credits.
- Monster math is an SRD 5.2.1 stat block with a house name, a nameplate, and tactics. The numbers are not house-ruled.
- Nameplate level is CR rounded up, minimum 1 (core §8.4). Boss cards say Boss.
- XP is `authoritative.xp_by_cr.table` in `rules/70-encounter-budget-5e.json`. Each card was checked against that table.
- A card's `fits_rules_70_cr_cap` says which party size and tier can legally include it. Floor 1's ogre boss (`f01-b-02`) fits the Level 2 boss day only. It does not fit a Level 1 boss cap.
- Achievement cards do not open boxes and do not invent a credit payout.
- Gear cards do not set a new price. List prices and the two Accountant proposals (`heal-critter-potion` 50, `pet-carrier` 100) are copied from `lore/tables/item-reskins.json`. Buying still follows core §5.10.
- Loot-box `credit_value`, `story_value`, and `sale_value` are copied from the filed decks or from `rules/40-loot-deck-spec-5e.md` §3.1. `story_value` is provenance, not a sale price. A row with `draw_weight` 0 is a hand-pick. Eight rules/40 rows are not in a deck yet (superior healing, hill giant strength, animal friendship, handy haversack, portable hole, +1 weapon, +1 shield, ring of protection). They do not draw until Lore files them.
- Floors 1–2 random boxes stay Bronze, or Silver on a boss box. Gold starts at Floor 3. No Platinum on Floors 1–8.
- A leveled spell, a 1/Day trick, a recharge breath, and an item charge all spend a counter. At-will cantrips do not. At 0, that spell or charge is done. Daily uses come back on a Long Rest in a saferoom. Do not add slots the stat block does not print.
- House flavor was checked against the live Floor 1 module and core rules. The Floor 2 reserve canon table was not copied. Dean Thudd on the Day pages stays the live Floor 1 boss. Book-proper mob names were not added.

## Voice

`system_line` is dry. `gm_line` is the snark and starts a [GM] beat. Do not read GM snark in the System voice.
