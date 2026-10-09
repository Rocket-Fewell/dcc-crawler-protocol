# Cursor DCC cards reference
Owner: Cursor (R&D) | Status: draft | Version: 0.1.0 | Updated: 2026-10-09
Summary: House encounter cards for grok bots. SRD 5.2.1 numbers, Dungeon Crawler Carl tone, not a live floor.

This folder is an R&D draw pile. Caleb asked for it without a room vote. It does not change `rules/`, `floors/`, `lore/CANON-LEDGER.md`, sessions, or credit ledgers.

Live Day pages and `rules/70-encounter-budget-5e.json` win if a card disagrees with them. Lore and Encounter Bot can hang stories on these cards later. Until they do, nothing here is filed for the table.

## What is in here

| Path | What |
|---|---|
| `monsters/monster-book.md` | Readable book. 72 cards, Floors 1–3. |
| `monsters/catalog.json` | The same 72 cards for a bot to load. |
| `monsters/f01.json` `f02.json` `f03.json` | The same cards split by floor. |
| `encounters/sample-recipes.json` | Eleven example lineups. Each one fits a rules/70 XP budget for 4 Crawlers. |
| `items/catalog.json` | 24 gear cards. Names and list prices come from `lore/tables/item-reskins.json`. Mechanics stay the SRD item. |
| `achievements/catalog.json` | 24 house toasts. Snark or Heroic Inspiration. No new credit amounts and no boxes. |
| `00-how-bots-draw.md` | How a grok bot builds a random encounter from this pile. |
| `ATTRIBUTION.md` | CC BY 4.0 credit for the SRD text. |

## Counts

| Floor | Mobs | Units | Elites | Bosses |
|---:|---:|---:|---:|---:|
| 1 | 12 | 6 | 4 | 2 |
| 2 | 10 | 6 | 5 | 3 |
| 3 | 10 | 6 | 5 | 3 |

72 monsters. 24 items. 24 achievements.

## Rules these cards already obey

- Players are Crawlers. The rest room is a saferoom. Money is credits.
- Monster math is an SRD 5.2.1 stat block with a house name, a nameplate, and tactics. The numbers are not house-ruled.
- Nameplate level is CR rounded up, minimum 1 (core §8.4). Boss cards say Boss.
- XP is `authoritative.xp_by_cr.table` in `rules/70-encounter-budget-5e.json`. Each card was checked against that table.
- A card's `fits_rules_70_cr_cap` says which party size and tier can legally include it. Floor 1's ogre boss (`f01-b-02`) fits the Level 2 boss day only. It does not fit a Level 1 boss cap.
- Achievement cards do not open boxes and do not invent a credit payout.
- Item cards do not set a new price. Buying still follows core §5.10.

## Voice

`system_line` is dry. `gm_line` is the snark and starts a [GM] beat. Do not read GM snark in the System voice.
