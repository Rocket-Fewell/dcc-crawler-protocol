# Session Protocol (Players + AI)

> **Current docs (v0.2.x, D&D 5e 2024 overlay):** rules are in `02-core-rules-5e.md`, character creation in `03-character-creation-5e.md`, and Floor 1 in `floors/floor-01-5e.md`. The v0.1 files (`02-core-rules.md`, `03-character-creation.md`, `floors/floor-01.md`) are superseded. Turn order, timeouts, Standing Orders and the dice roller are in `02-core-rules-5e.md` §2.5.

## Player moves (type these)

Examples of clear moves:

- `I move north to the door and listen.`
- `I attack the scavenger with my crowbar.`
- `I search the kiosk.`
- `I talk to the vendor — ask about the stairwell.`
- `I use a healing injector on Maya.`

If a move is vague, the AI asks one clarifying question, then proceeds.

## Rolls

- AI calls the roll and the target.
- Player (or UI later) rolls; result is public.
- Critical success / failure: as written in 5e 2024 (natural 20 / natural 1 rules; see `02-core-rules-5e.md` §1 and §2.5.6 for the DM-run roller).

## Shared table rules

- No looking at unrevealed map areas (honor fog of war).
- No secretly rewriting your inventory; the sheet is source of truth.
- Disputes: AI cites the rule doc; if silent, make a temporary ruling and log it.
