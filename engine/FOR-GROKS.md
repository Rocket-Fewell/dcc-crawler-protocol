# For the Grok bots: what Cursor built, where it sits, what it is for
Owner: Cursor | Status: handoff | Version: 0.1.0 | Updated: 2026-10-09
Summary: Read this when you come online. The local table lives in `engine/`. It does not replace the live Discord game. The plan it is measured against is the 2026-10-07 Grok conversation in `engine-design/00-source-grok-conversation.md`, plus `engine-design/01-rules-engine-scope.md` and `engine-design/02-architecture.md`.

Players are Crawlers. Money is credits. Dean Thudd stays the Floor 1 boss. This folder does not write `sessions/`, `sessions-data/`, `characters/`, `floors/`, or a credit ledger.

## Purpose

The conversation's split, in the words that still govern this folder:

- Code decides every number. The model does not do arithmetic and does not set hit points.
- A fast voice narrates after the result is final. The funny GM stays the funny GM. `[SYSTEM]` stays dry. `[NPC: Name]` is that NPC.
- A strong model is only for a line no rule covers. It returns a ruling. Code still rolls.
- Agents build between sessions. No agent sits in the live turn.

Caleb's later direction (2026-10-09) kept that split and added a table he can look at: a process on his machine, a player page, a GM page for a rare correction, Discord still the ears and the mouth. `engine-design/02-architecture.md` still says "no HTTP, stdin/stdout only." The pages exist because he asked for them. Do not delete them to match the older sentence.

The live bridge keeps running the real game until he says to switch. Leaving `DCC_TABLE_URL` unset is that switch, still off.

## Where it is saved

| Path | What it is |
|---|---|
| `engine/` | The whole local table. Start here. |
| `engine/README.md` | How to run it. |
| `engine/serve.py` | `python3 engine/serve.py` binds localhost. Default port 8765. |
| `engine/dcc_engine/table.py` | The Shooting Gallery fight. Dice come off the cards. Code sets hit points. |
| `engine/dcc_engine/playthrough.py` | The Floor 1–3 walk. One seat, in memory, scene by scene. |
| `engine/dcc_engine/script.py` | Reads Floor 1 and Floor 2 day pages. Does not rewrite them. |
| `engine/campaign/floor3.json` | Floor 3 only. There are no Floor 3 day pages. This file is not a live floor. |
| `engine/dcc_engine/pages.py` | `/` is the walk. `/player` is the Gallery. `/gm` is the correction page. |
| `engine/dcc_engine/narrate.py` | Short lines after a roll. A mannequin can still be smiling. A rat is not. |
| `engine/fixtures/raithen-copy.json` | The seated copy. The live sheet is not this file. |
| `discord-voice-bridge/src/tablehook.js` | Opt-in hook. Posts a transcript to `/api/line`. Speaks `[SYSTEM]`, `[GM]`, and `[NPC: Name]`. Never speaks `[ROLL]`. |
| `Cursor-DCC-CardsReference/` | The R&D cards the table reads. Already on main. Not a live floor. |
| `engine-design/` | The conversation and the v1 plan. The scoreboard below is measured against it. |

`/` walks 85 scenes: every Floor 1 and Floor 2 encounter from the day pages, then 15 Floor 3 scenes (Millroad through the county stair). Say `next` to move. In a fight, type or use Listen, then Send.

## Progress, against the conversation

The build order in `engine-design/02-architecture.md` is C1, C2, C3. This is how far each one got.

### C1 engine core — started, not the replay yet

Done in this folder:

- A Python package that rolls from `tools/roll.py` and does not log to `sessions/`.
- Room and monster numbers come off `Cursor-DCC-CardsReference/`. The Gallery mannequin shortbow is +5 and `1d6+3`, from `f01-m-09`.
- Action economy for one Crawler: one action, one bonus action, one reaction, one free object interaction, movement. A second action stops. The System names what did not happen.
- Cunning Action is refused at Rogue 1. At Rogue 2, Hide can be the bonus.
- "Pick up the body and swing it" is a ruling, then an improvised bludgeoning attack. Mannequins are vulnerable to bludgeoning, so that damage is doubled. The model does not set the hit points.
- Cover in the Gallery is +2 AC until the Crawler closes.
- The player page shows the channel card, the System nameplate, the picture, and hit points. The printed stat block stays on `/gm`.
- Listen on the player page is on only during that Crawler's turn. The browser transcribes into the line. They can still type. Nothing is sent until Send.
- Floor 1 and Floor 2 voice lines are the filed `[PLAYER-FACING]` and `[GM-FACING]` lines. Dry notices are `[SYSTEM]`. Snark and set pieces are `[GM]`. Dean Thudd is still Dean Thudd. A party of 2 meets Dean Thudd (JV), which is the filed count.
- Floor 3 NPC lines use names already in `tables/npc-voices.json`: Village Elder, Hedge Appraiser, Low Chapel Bishop, Village Saint, Benefactor, Guide. No new species.

Not done from C1:

- No SQLite. State dies when the process stops. That is on purpose until a session is real.
- No import of `tools/state.py` or `tools/loot.py`. Credits, boxes, rests, and the clock are spoken when the day page says them. Code does not spend them.
- No JSON Schema check against `engine-design/03-room-card-format.md`.
- No replay of the 2026-10-07 Shooting Gallery log with those exact dice. Scope section 7 is still the "done" line for C1.
- No fast-model call and no strong-model call. Routine color is the filed line or a short sentence in `narrate.py`. A weird line in the Gallery becomes one improvised attack or a System refusal. It is not the ruling JSON in scope section 5.

### C2 bridge integration — a hook, not ENGINE_MODE

Done:

- `DCC_TABLE_URL` must be an http(s) localhost origin with no user or password. Anything else is refused.
- While it is set, a transcript is posted to the table and the agent GM is not woken.
- `[ROLL]` stays on the page. `[SYSTEM]`, `[GM]`, and `[NPC: Name]` can be spoken.
- Unset, the live game is unchanged. No new token.

Not done:

- The hook posts to `/api/line`, which is the Gallery only. The Floor 1–3 walk is `/api/play`. A sentence spoken in Discord does not yet land in the room the walk is standing in.
- The bridge does not spawn the engine. You start `python3 engine/serve.py` yourself. `ENGINE_MODE` from the architecture doc does not exist.
- Narration is not streamed from a model. The table returns the whole reply.

### C3 live dry run — not started

Caleb has not played this table on a test channel with the hook on. Accountant has no cost-per-turn, because no model is called. Do not flip the live game over to this.

### Content the conversation asked the bots for

Floor 1 room stubs and the picture-name card pack are in `Cursor-DCC-CardsReference/`. The day pages still win if a stub disagrees. Floor 2's named fights are only partly fightable: a body is used when the day page's SRD id matches a card. Krakaren Clone is a chuul. There is no chuul attack card, so that scene is spoken and not fought. Floor 3 is the local script above, not a day-page module.

## What still needs to be done

The order changed on 2026-10-10. Read `engine/NEXT.md`. Do not start at the hook.

1. Floor 1, Day 1, as one session. Five fights must take a shot: Vent Row, the Gallery, the Big Green EXIT, the Mascot Locker, and Lights-Out. The EXIT and the locker currently fail because `local.attacks` has no `to_hit`. Talk scenes stay talk scenes. Stop at the Green Room. Discord stays on the Gallery until that day plays.
2. Point the hook at the Day 1 scene you are standing in. Not at the 85-scene tour.
3. Day 2 through Dean Thudd, then the missing attack cards, starting with Krakaren Clone. Do not rename Dean Thudd to the picture on `f01-b-02`.
4. Wire the fast narrator the way `engine-design/04-narrator-prompt.md` says: code finishes the roll, then a short call writes 2–4 sentences from the snapshot. The strong model only when the parser has no rule, and only as ruling JSON that code then rolls. No tools on either call.
5. Pass C1's own finish line: replay the 2026-10-07 Gallery with the logged dice and match the numbers.
6. Keep session state in the process (SQLite after each resolved action, when Caleb wants a session that survives a restart). Git stays out of the turn.
7. Then C3: a dry run on a test channel. The live bridge stays the live bridge until that passes and Caleb says switch.

Leave `floors/`, `rules/`, live sheets, and credit ledgers to their owners. Propose in the handoff channel. Do not invent a species, a fee, or a Crawler into the live campaign.
