# Story Box how-to (GM, one page)
Owner: Borent Corp Systems Architect | Status: final | Version: 1.4 | Updated: 2026-10-04
Summary: How to award a Legendary Story Box (award, then open in a safe room), sell it, and what not to do.

**When.** A Crawler does a rare, first-of-its-kind deed that matches a Story Box card (0055-0060: Pet Box, Quadruped Box, That's the Spirit! Box, Pacifist's Box, Stopped the Porkchop Express Box; 0061-0065: Four Paws Over the Threshold, Family Reunion Now Streaming, Talked It Into Quitting, Let the Room Do It, Group Handshake; ids `f01-any-00NN`, list them with `loot show`). You judge it on the spot. It is never random and never a reward for ordinary play.

**1. Check first (nothing is written):**
`python3 tools/state.py loot story-box 1 any --crawler Donut --pick f01-any-0056 --deed "Brought a cat into the Crawl" --witness "Carl" --gm-note "first quadruped, S1" --dry-run`
Read the warnings. A HOLD note from Lore or a missing `power_note` is a warning, not a stop.

**2. Award it:** the same line without `--dry-run`. This records the deed and announces the box; **the box stays unopened** (the player's card shows an unopened Legendary box). Nothing is in their inventory yet. Add `--deed-id some-slug` so a reworded deed cannot pay twice.

**3. Open it in a safe room:** `python3 tools/state.py loot story-box --open --crawler Donut --safe-room` (or turn the scene on once: `python3 tools/state.py scene safe-room on`, and off when the party leaves). Every loot box works this way; outside a safe room the tool refuses. This adds the item, ledgers and card.

**Two cards, one box** (Pet Box = Enhanced Pet Biscuit + Pet Biscuit Crate): `--pick f01-any-0055,f01-any-0060`. It counts as one box.

**Pairs and duplicate themes (award only ONE of each duplicate-theme pair).** 0055 Enhanced Pet Biscuit and 0060 Pet Biscuit Crate are the two cards of ONE Pet Box: award them together (`--pick f01-any-0055,f01-any-0060`, one box under the cap). Duplicate-theme pairs, one card each: Quadruped Box (0056) / Four Paws Over the Threshold (0061), a four-legged companion; That's the Spirit! (0057) / Family Reunion, Now Streaming (0062), a fictional rival. Never give both cards of a pair for one table. Other new cards: 0063 Talked It Into Quitting (sale 250), 0064 Let the Room Do It (500), 0065 Group Handshake (100, every Crawler present did a distinct part). A pet itself never earns a box; the owner does, for a deed.

**If the holder dies before opening:** the box is reclaimed automatically (see below). To give that deed out again use `--reaward "why"` on the same `loot story-box` line: allowed only if EVERY earlier award of that deed was reclaimed and none was opened, sold or released by a /delete (a deed closed by /delete stays closed). The new box gets id `sb-F-deed-r2`; the ledger records `reaward_of` and your reason.

**Rules you will hit:**
- Floors 1-2 only. Only one Story Box per floor; the cap counts LIVING Crawlers only (a deleted Crawler frees the slot, a dead Crawler's UNOPENED Story Box is reclaimed and frees the slot; one already opened still counts). Only the ACTIVE Crawler receives one. A second needs `--override-cap "why"` (logged). It is your call: give a real reason in the logged "why" (Caleb 2026-10-04 ruling, decision 018 addendum). Caleb can veto.
- A deed pays once. `loot deeds` shows what was paid. A genuinely different deed gets its own `--deed-id`.
- `--deed` must say what happened, in a sentence. No deed text, no box.
- Quadruped Box: any four-legged companion counts, not only a cat. One per table.
- The item is **not bound**: it can be looted from a corpse, traded or sold. Story value is provenance only, never credits; do not quote it as money. Sell to the System with `python3 tools/state.py sell Donut "Tiara..." --reason "sold to the System"`: it pays the card's sale value (100/250/500 by rung) times the sale floor's multiplier. Crawler to Crawler: `transfer FROM TO ITEM --reason "..." [--price N]`. Sales are flagged in `loot totals` and `ledger verify`, never blocked.
- The spotlight rota ("every living Crawler gets a first Story Box before anyone gets a second") is guidance. The tool only warns.
- A second pet deed on the same floor pays Silver at most, plus a Title.
- Never improvise a strong item. If no card fits, say "Achievement under review by Production" and deliver it next session (rules/45 s3 step 1).
- **If a Crawler DIES holding an UNOPENED Story Box, the box is reclaimed** (Caleb 2026-10-04): `condition add X Dead` does it automatically, logs a `reclaimed` event in the Story Box ledger, removes the unopened box and frees the floor slot (the cap no longer counts it). The deed stays closed. A revived Crawler does not get it back. An opened box is not touched (its items are ordinary items).
- Unopened Story Boxes can't be traded or sold. When a safe room opens, all unopened boxes open at once, lowest tier first. Opened items are ordinary tradeable items.
- Pet Box: feeding an Enhanced Pet Biscuit to a pet can make it a Crawler (own sheet, played by the same player, no extra slot, one conversion per living pet-Crawler; the pet-Crawler can't be traded, sold or looted; channel `<player>-<pet>-sheet`; the biscuit works only on the pet named in the deed): `create-crawler` with `kind: pet-crawler`, see tools/README.md.
- Respect opt-outs: "That's the Spirit!" is opt-in per player at session zero (fictional rival, no killing, no PvP). Don't run it for a player who didn't opt in.

**After:** `loot totals` (economy and story separately), `loot deeds`, `loot show`.
