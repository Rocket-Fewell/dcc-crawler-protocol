# How local play uses these cards
Owner: Cursor (R&D) | Status: draft | Version: 0.3.0 | Updated: 2026-10-09
Summary: The card pile a future engine loads so a turn does not wake an agent.

Source: `engine-design/00-source-grok-conversation.md` and `engine-design/01-rules-engine-scope.md`. This folder does not start that engine. It is the content the engine will read.

## The split
Code owns the numbers. It loads these cards at session start and keeps them in memory. A player line maps to an action card. Code rolls, spends uses, and writes the new numbers onto the crawler card and the combat-state card. Then a fast model gets the snapshot card and speaks two to four sentences. A strong model is called only when no action card matched, and it returns the ruling card for code to validate.

Git is not in the turn. This pack does not write `sessions/`, `sessions-data/`, `characters/`, or a credit ledger.

## What a GUI will load
| File | What it is |
|---|---|
| `../monsters/catalog.json` | 72 picture-named stat cards. `local.attacks` is what code rolls. `srd_name` stays the math key. |
| `../items/catalog.json` | 191 gear cards. `display_name` is the local name. `lore_display_name` is Lore's filed reskin. `local` is damage or AC when a table filed it. |
| `../items/loot-boxes.json` | Filed loot cards. `local.effect` is the text already on the card. |
| `../achievements/catalog.json` | 24 house toasts. No new credits. |
| `actions.json` | The lines code can resolve without a model. |
| `conditions.json` | Flags code applies. Prone is not a narrator opinion. |
| `crawler-card.template.json` | Blank player state. Copy it into memory. Do not fill it with a live crawler in git. |
| `combat-state.template.json` | Whose turn, which round. |
| `clock.template.json` | Floor 1 day clock, copied from the decision already on the day pages. |
| `secret-card.template.json` | Trigger plus reveal. Hidden from the narrator until code flips `revealed`. |
| `npc-card.template.json` | Blank talker. |
| `snapshot.template.json` | What the fast voice model is allowed to see. |
| `ruling.template.json` | What the strong model must return when no action card matched. |
| `rooms/f01/` | 25 Floor 1 room stubs pointed at the day pages. The day page wins. |
| `monster-name-audit.md` | Old name, new picture name, what you are looking at. |
| `item-name-audit.md` | Which gear names were too flat to keep. |

## Names
A card name has to be a picture. "Latch-On Ceiling Mosquito" is a stirge. "Smiling Polo Mannequin" is a skeleton. Krakaren Clone is the style of name that works: you can see it, and it is funny. A bare "Skeleton" is not. D&D dictionary words stay on `srd_name`.

Lore's Floor 1 draft names are on `lore_floor_name` when this body is the one the day pages use (Vent Rat, Ceiling Tick, Mannequin Staff). The room stubs keep the live spoken name. Dean Thudd is still Dean Thudd. Adjunct Smash is only the random-draw giant.

Gear keeps Lore's joke when the joke already shows the object. Ten flat names were punched up. The filed reskin name is still `lore_display_name`, and `lore/tables/item-reskins.json` was not edited.
