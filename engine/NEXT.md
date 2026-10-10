# Next slice: Floor 1, Day 1, as one session
Owner: Cursor | Status: plan | Version: 0.1.0 | Updated: 2026-10-10
Summary: Do not wire Discord to the 85-scene walk yet. The next build is Day 1 of Floor 1, played in order, with every combat room using the same rules as the Gallery.

Read `engine/FOR-GROKS.md` for what already exists. This file is the decision about what to build next. It does not change `floors/`, `rules/`, or the live game.

## Where we actually are

One fight is real. The Shooting Gallery (`enc-d01-11`) rolls from the card, spends the action, and sets hit points. The player page, the Listen button, and the GM correction page all sit on that fight.

The Floor 1–3 walk is a reader with a few fights attached. Say `next` and it speaks the filed lines. Discord does not drive it. `DCC_TABLE_URL` still posts to the Gallery only.

Floor 1, Day 1 is 12 scenes. At a party of 2, this is what the process can do with them today:

| Scene | What happens now |
|---|---|
| Day notice, Cold Open, Proctor Bell | Spoken. No fight. |
| Vent Row (`enc-d01-08`) | Fight. Three Vent Rats. A shot lands. |
| Vending Gore, Hall of Fair Warnings | Spoken. No fight. |
| Shooting Gallery (`enc-d01-11`) | Fight. Two mannequins. This is the proven one. |
| Break Room | Spoken. No fight. |
| Big Green EXIT (`enc-d01-02`) | Does not start. The card is there. `local.attacks` has no `to_hit`, so the spawn dies. |
| Mascot Locker (`enc-d01-03`) | Same failure. Bruiser and the lanyard blade never reach the table. |
| Lights-Out (`enc-d01-04`) | Fight. Two Ceiling Ticks. |
| Green Room | Spoken. Day 1 ends. |

So "the whole campaign" is a script you can click through. "A game" is three fights, and one of them is the one we trust.

## The decision

The next build is Floor 1, Day 1, from the opening notice through the Green Room. Same seat (the Raithen copy). Same dice rules as the Gallery. Filed lines stay the voice. No new day pages.

Discord stays on the Gallery until that day can be played in the browser without a missing fight. Pointing the hook at the long walk first would let people talk at a tour.

## What that slice includes

1. Fix the two spawns that already have cards and no `to_hit` (Exit Greeter, Exit Greeter trainee, Bruiser, Lanyard Blade). Read the bonus off the card if it is stored under another field. Do not invent a to-hit.
2. Walk Day 1 in order. Talk scenes stay talk scenes: hear the line, say next.
3. Every Day 1 fight accepts the same kind of line the Gallery accepts: move, one action, one bonus, one reaction, one object. A second action stops. Code sets the hit points.
4. Hit points carry from Vent Row to the Gallery to the EXIT to the locker to Lights-Out.
5. Stop at the Green Room. Do not auto-continue into Day 2.

## What that slice does not include

- Retargeting `DCC_TABLE_URL`. The live bridge stays as it is.
- A model call. Narration stays the filed line plus the short sentence after a roll.
- Krakaren, the rest of Floor 2, and Floor 3 fights.
- Credits, rests, boxes, level-up math, or a second Crawler.
- Rewriting `floors/` or adding a Floor 3 day page.
- SQLite. The session can still die when the process stops.

## Done means

One person can open `python3 engine/serve.py`, sit the Raithen copy, and play Day 1 to the Green Room. Vent Row, the Gallery, the Big Green EXIT, the Mascot Locker, and Lights-Out each take a shot and change hit points from the card. The other scenes speak the filed `[SYSTEM]` and `[GM]` lines. A test walks that day with scripted dice and does not write `sessions/`.

## After that day works

1. Point the hook at the scene you are in, for Day 1 only.
2. Day 2 through Dean Thudd, same rule: a fight starts only when the card can supply the roll.
3. Then Floor 2 bodies that have no attack card, starting with Krakaren. Dean Thudd is not renamed.
4. Fast narrator and the strong-model ruling, as in `engine-design/04-narrator-prompt.md`, only after the Day 1 numbers are already final.
5. The 2026-10-07 Gallery replay. Then a dry run. The live game switches when Caleb says so.
