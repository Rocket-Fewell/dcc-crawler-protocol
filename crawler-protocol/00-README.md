# Crawler Protocol — DM Source Pack

Personal fan project inspired by *Dungeon Crawler Carl* (Matt Dinniman). Not affiliated with or endorsed by the author or publishers. For private play with friends only.

## Purpose

This pack is the **single source of truth** for an AI Dungeon Master. Humans play by typing moves. The AI runs the world, NPCs, adjudication, and floor progression using only these docs plus the live session state.

## How an AI DM should use this pack

1. Read `protocols/ai-dm-instructions.md` first every session.
2. Follow `01-game-brief.md` for tone, scope, and hard limits.
3. Adjudicate with **`02-core-rules-5e.md`** (v0.2.x, D&D 5e 2024 overlay; never invent a conflicting rule mid-session without noting it in the Session Log). The old `02-core-rules.md` (v0.1) is superseded.
4. Build / load characters with **`03-character-creation-5e.md`** (v0.2). The old `03-character-creation.md` (v0.1) is superseded.
5. Know the long game via `05-campaign-narrative.md` then `04-floor-bible.md` (seeds and payoffs). **⚠ `04-floor-bible.md` still needs a Continuum + 5e rewrite;** use it for seeds only until then.
5b. Award achievements from `reference/achievements.xlsx`.
6. Run the active floor from `floors/floor-XX-5e.md` (start with **`floors/floor-01-5e.md`**; the old `floors/floor-01.md` stub is superseded).
7. Log state in `reference/session-state.md` (or the live session equivalent).

## Build order (elephant bites)
| 0 | Campaign Narrative + 3-floor triads | Draft — awaiting input |

| Priority | Doc | Status |
|----------|-----|--------|
| 1 | Game Brief | Draft |
| 2 | AI DM Instructions + Session Protocol | Draft |
| 3 | Floor Bible (floors 1–18) | Draft; **needs Continuum + 5e rewrite** |
| 4 | Core Rules 5e overlay (`02-core-rules-5e.md`) | **v0.2.x draft (current)**; v0.1 superseded |
| 5 | Character Creation 5e (`03-character-creation-5e.md`) | **v0.2 draft (current)**; v0.1 superseded |
| 6 | Floor 01 playable module (`floors/floor-01-5e.md`) | **v0.2 draft (current)** |
| 7 | Floors 02–18 (expand using Bible) | Ongoing |
| 8 | Play UI (roller, fog-of-war map) | After Floor 01 runs |

## Design goals

- Simple enough for friends typing moves in chat
- Enough structure for fair rolls and D&D-like basics
- Floor-by-floor unlocks and callbacks (plant on 2, pay off on 6)
- AI-runnable without human GM prep each session
