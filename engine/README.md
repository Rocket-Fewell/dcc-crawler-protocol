# Table (Shooting Gallery slice, and a local Floors 1–3 walk)

Owner: Cursor | Status: draft | Version: 0.1.0 | Updated: 2026-10-09

Grok bots: read `engine/FOR-GROKS.md` before changing this folder. The plan for the Discord Floor 1 rebuild is `engine/NEXT.md`. The hook stays on the Gallery until that floor can be played.

The fight runs in this process. Caleb can play while it sits in the background. Discord stays the voice channel: the bridge already turns speech into text and speaks `[GM]` and `[SYSTEM]` back. This slice does not join voice and it does not need a new bot token or a new server token.

`engine-design/02-architecture.md` still says the Node bridge is the only front end and that there is no HTTP server. Caleb's later direction (2026-10-09) is the one this folder follows: a table process on his Windows PC, a player client for cards and the resolution text, and a GM page for the rare correction. The bridge remains the ears and the mouth. The live game stays on the current bridge until he says to switch. This folder does not write `sessions/`, `sessions-data/`, `characters/`, or a credit ledger.

## What this slice does

One room: the Shooting Gallery (`enc-d01-11`). Two Smiling Polo Mannequins, the filed count for a party of 2. Their shortbow is +5 and `1d6+3` piercing, copied off `local.attacks` on `f01-m-09`. Half cover from the counter is +2 AC until a Crawler closes.

On the player page, Listen is on only during that Crawler's turn. The browser transcribes speech into the line. They can still type. Nothing is sent until Send. No new token. The line is split on "and" / "then" and walked left to right. Movement, one free object interaction, one action, one bonus action. A second action stops the chain, and the System names what did not happen. Those leftovers are not saved for later. Cunning Action is refused at Rogue 1. "Pick up the body and swing it" is a ruling, then code rolls an improvised bludgeoning attack. The mannequins are vulnerable to bludgeoning, so that damage is doubled. The model stand-in never sets hit points.

`[ROLL]` lines are on the page and marked `speak: false`. `[GM]` and `[SYSTEM]` are marked `speak: true`. The bridge can say those when `DCC_TABLE_URL` points at this process. That hook is off until the variable is set, so the live game keeps waking the agent GM.

The GM page can undo the last resolution or set one combatant's hit points. The player page does not show the room's GM note.

## Floors 1–3

`http://127.0.0.1:8765/` is a separate walk from the live game. It reads the Floor 1 and Floor 2 day pages and speaks those `[PLAYER-FACING]` and `[GM-FACING]` lines: dry lines as `[SYSTEM]`, the snark and the set pieces as `[GM]`. It does not rewrite `floors/`. Dean Thudd stays Dean Thudd. A party of 2 meets Dean Thudd (JV), which is the filed count. Floor 3 has no day pages, so `engine/campaign/floor3.json` is only this table's rural script, using NPC names already in `tables/npc-voices.json`. Say `next` to move on. In a fight, the dice still come off the card. `[NPC: Name]` is spoken when the bridge hook is on. `[ROLL]` stays on the page.

The Shooting Gallery player page is still `/player`. The hook `DCC_TABLE_URL` still posts to `/api/line` on that slice.

## Run

From the repo root:

```
python3 engine/serve.py
```

Player: `http://127.0.0.1:8765/player`
Table: `http://127.0.0.1:8765/gm`

It binds to localhost. `--host` or `DCC_TABLE_HOST` changes that. `--port` or `DCC_TABLE_PORT` changes the port. `--party-size` is 2, 3, or 4, matching the counts already on the room card.

The seat is a copy of Raithen (Hornn's Warlock) in `engine/fixtures/raithen-copy.json`. The player page shows the whole channel card: attacks, spellcasting, features, rests, gear, standing orders, signature, achievements. Attacks are the numbers `tools/card_rules.py` already prints. The live sheet in `sessions-data/` is not written, and the copy leaves out the fan profile, the survey, and the quirk. A Crawler sees the System nameplate, the picture, and hit points. The printed stat block (`f01-m-09`), including armor class, the shortbow and shortsword lines, and the bludgeoning vulnerability, stays on the table page with the chair-leg note. The shortbow roll is still +5. The long card and the log scroll inside the window.

## Check

```
PYTHONPATH=tools:engine python3 -m unittest discover -s engine/tests -p 'test_*.py'
```

## Voice hook

The bridge already has its bot token. Nothing new is pasted into the repo or into `#agents`.

With `python3 engine/serve.py` running, set `DCC_TABLE_URL=http://127.0.0.1:8765` on the bridge and restart it. A transcript line is posted to `/api/line`. `[GM]` and `[SYSTEM]` are spoken and copied into the GM output channel. `[ROLL]` stays on the page. While that variable is set, new lines do not wake the agent. Leave it unset and the live game is unchanged. The URL has to be localhost. A public address is refused.

## Not in this slice

Character creation beyond seating a card. A map. Fog of war. A live narrator model. The rest of Floor 1.
