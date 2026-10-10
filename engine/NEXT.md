# Floor 1, days 1–5, on the lean table
Owner: Cursor | Status: done for this slice | Version: 0.2.0 | Updated: 2026-10-10
Summary: Rebuild the Floor 1 the Discord game already runs (the five day pages) onto `engine/`. Use the room cards and the stat cards that already exist. Do not rewrite `floors/`. Do not point Discord at this walk yet. The code in this change is that rebuild.

This file is the plan. The code in this same change is the execution of it.

## What "the Discord floor" is

`floors/f01/day-01.md` through `day-05.md` are the live Floor 1. Twenty-five encounters, plus the day notice at the top of each page. The card pack already has one room file per encounter in `Cursor-DCC-CardsReference/local/rooms/f01/`. Those stubs say the day page wins on names and on voice. The lean table reads the day page for the spoken line and the room file for who is in the fight.

A party of 2, which is the seat this process uses:

| Day | Fight | Who shows up | Card | Roll the table uses |
|---|---|---|---|---|
| 1 | Vent Row | 3 Vent Rats | `f01-m-01` | Bite, melee |
| 1 | Shooting Gallery | 2 mannequins, spoken as the room names them | `f01-m-09` | Shortbow +5, `1d6+3` piercing. Shortsword in melee |
| 1 | Big Green EXIT | 1 Exit Greeter, 2 Trainees | `f01-m-10`, `f01-m-03` | Scimitar +4 `1d6+2` and Shortbow +4 `1d6+2`. Trainee dagger +4 `1d4+2`, melee or thrown |
| 1 | Mascot Locker | 1 Bruiser. Lanyard Blade count is 0 | `f01-e-01` | Slam +4 `1d6+2`. The card's Multiattack is two Slams |
| 1 | Lights-Out | 2 Ceiling Ticks | `f01-m-02` | the printed melee bite |
| 2 | Service Door | the filed mannequin count | `f01-m-09` | same shortbow / shortsword |
| 3 | Collapsing Hall | rats and ticks at the filed counts | `f01-m-01`, `f01-m-02` | their printed bites |
| 3 | Stage Wings | the filed mannequin count | `f01-m-09` | same |
| 4 | Dark halls | ticks at the filed count | `f01-m-02` | same |
| 4 | Stage door | Ushers | `f01-m-09` | same, spoken name Usher |
| 5 | Graduation | Dean Thudd (JV) and 4 Ushers. The ogre body `f01-b-02` count is 0 | `f01-e-02`, `f01-m-09` | Grab +4 `2d6+2` in melee. Light Hammer +4 `3d4+2` when they are not in melee |

Talk scenes stay talk scenes. Cold open, Proctor Bell, vending, warnings, break room, green room, the day notices, the stair choice, last call, the outage, the night shift, the toll, and the last six hours have no enemy count. Hear the filed line. Say next.

Dean Thudd stays Dean Thudd. The picture name on `f01-b-02` (Adjunct Smash) is not his name. At a party of 2 he is the bugbear card with the spoken name Dean Thudd (JV).

## What was actually broken

The cards were already there. Two Day 1 fights never reached the table: the Big Green EXIT and the Mascot Locker. `attack_record` demanded `to_hit` on every line in `local.attacks`. Nimble Escape is a bonus (Disengage or Hide) and has no to-hit. Bruiser's Multiattack line says "two Slam attacks" and has no to-hit. The Slam under it does. `melee_or_ranged` is a real attack (the trainee dagger, Dean's hammer) and the spawner was only looking for `melee` and `ranged`, so a dagger-only body had no attack after the bonus line crashed it.

No new stat card. Nothing on Floor 1's twenty-five rooms points at a missing id.

## What this build does

1. A line is a roll only when it has `to_hit`, damage dice, and kind `melee`, `ranged`, or `melee_or_ranged`. Bonus, trait, reaction, save, and the Multiattack header are skipped. Their numbers are not invented.
2. `melee_or_ranged` can fill the ranged slot and the melee slot. A real `melee` line stays the melee attack when one is printed (Grab stays Grab; the hammer is the ranged one).
3. When a Multiattack header names that melee attack and prints a count, the enemy turn uses that count. Bruiser swings Slam twice. Everyone else swings once. The Gallery mannequins are unchanged: one Shortbow.
4. Days 1 through 5 play in the order the day pages already have, on the same seated copy. Hit points carry. A fight accepts the same line the Gallery accepts. Code sets the hit points. The filed `[SYSTEM]` and `[GM]` lines stay the voice.
5. The walk still continues into Floor 2 after the stairwell. This change does not rebuild Floor 2 or Floor 3.

## What this build does not do

- Retarget `DCC_TABLE_URL`. It still posts to the Gallery.
- Call a model. Narration stays the filed line plus the short sentence after a roll.
- Spend credits, open boxes, take a rest, or level anyone. The day pages may say those words. Code does not apply them.
- Rewrite `floors/` or `rules/`.
- Add a Krakaren card. That body is Floor 2.
- Store the session. It still dies when the process stops.

## Done means

`python3 engine/serve.py`, the Raithen copy, party of 2. Every Floor 1 fight in the table above spawns from its card and a shot changes hit points. EXIT is the greeter and the trainees. The locker is Bruiser, and his two Slams are the card's count. Graduation names Dean Thudd (JV), not Adjunct Smash. Talk scenes speak the filed lines. A test walks those five days with scripted dice and does not write `sessions/`. The Gallery page still calls the dummies Smiling Polo Mannequin.

## Party size

The same floor converts from the counts already on the room cards. There is no separate 1-Crawler floor and no invented count.

| Who sits down | Column used |
|---|---|
| 1 Crawler | the filed 2-Crawler counts |
| 2 Crawlers | 2 |
| 3 Crawlers | 3. Graduation is Dean Thudd, Head of Orientation (`f01-b-02`, Greatclub and Javelin), plus 2 Ushers. Not the JV bugbear. Not Adjunct Smash. |
| 4 Crawlers | 4. Same Dean, 4 Ushers. The locker adds 2 Lanyard Blades. The Gallery is 4 mannequins. Vent Row is 6 rats. |

`--party-size` or `DCC_PARTY_SIZE` sets it at startup. The Party buttons on the walk restart that walk on the chosen column. The Gallery uses the same number.

## After this floor fights

1. Point the hook at the Floor 1 scene you are standing in.
2. Floor 2 bodies that have no attack card, starting with Krakaren. Do not rename Dean.
3. Fast narrator, then the strong-model ruling, as in `engine-design/04-narrator-prompt.md`.
4. The 2026-10-07 Gallery replay. Then a dry run. The live game switches when Caleb says so.
