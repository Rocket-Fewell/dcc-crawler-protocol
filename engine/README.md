# Table (Shooting Gallery slice)

Owner: Cursor | Status: draft | Version: 0.1.0 | Updated: 2026-10-09

The fight runs in this process. Caleb can play while it sits in the background. Discord stays the voice channel: the bridge already turns speech into text and speaks `[GM]` and `[SYSTEM]` back. This slice does not join voice and it does not need a new bot token or a new server token.

`engine-design/02-architecture.md` still says the Node bridge is the only front end and that there is no HTTP server. Caleb's later direction (2026-10-09) is the one this folder follows: a table process on his Windows PC, a player client for cards and the resolution text, and a GM page for the rare correction. The bridge remains the ears and the mouth. The live game stays on the current bridge until he says to switch. This folder does not write `sessions/`, `sessions-data/`, `characters/`, or a credit ledger.

## What this slice does

One room: the Shooting Gallery (`enc-d01-11`). Two Smiling Polo Mannequins, the filed count for a party of 2. Their shortbow is +5 and `1d6+3` piercing, copied off `local.attacks` on `f01-m-09`. Half cover from the counter is +2 AC until a Crawler closes.

A typed line stands in for a transcript. The line is split on "and" / "then" and walked left to right. Movement, one free object interaction, one action, one bonus action. A second action stops the chain, and the System names what did not happen. Those leftovers are not saved for later. Cunning Action is refused at Rogue 1. "Pick up the body and swing it" is a ruling, then code rolls an improvised bludgeoning attack. The mannequins are vulnerable to bludgeoning, so that damage is doubled. The model stand-in never sets hit points.

`[ROLL]` lines are on the page and marked `speak: false`. `[GM]` and `[SYSTEM]` are marked `speak: true` so a later bridge hook can say them.

The GM page can undo the last resolution or set one combatant's hit points. The player page does not show the room's GM note.

## Run

From the repo root:

```
python3 engine/serve.py
```

Player: `http://127.0.0.1:8765/player`
Table: `http://127.0.0.1:8765/gm`

It binds to localhost. `--host` or `DCC_TABLE_HOST` changes that. `--port` or `DCC_TABLE_PORT` changes the port. `--party-size` is 2, 3, or 4, matching the counts already on the room card.

Seat a Crawler from the player page before the first swing, or leave the Gallery Pilot (Rogue 1) that loads with the room. The pilot is a fixture in `engine/fixtures/`. It is not a live crawler.

## Check

```
PYTHONPATH=tools:engine python3 -m unittest discover -s engine/tests -p 'test_*.py'
```

## Not in this slice

Character creation beyond seating a card. A map. Fog of war. The bridge posting transcripts into `/api/line` and speaking the `say` list. When that hook is added, it uses the bot tokens the bridge already has. Do not paste those into the repo or into `#agents`.
