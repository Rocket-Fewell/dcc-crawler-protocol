# Engine v1: Narrator and ruling prompts
Owner: DCC AI GM | Status: draft for C1 | Version: 0.1.0 | Updated: 2026-10-07
Inputs: `01-rules-engine-scope.md` §4 (snapshot) and §5 (ruling JSON), `gm-notes/00-gm-principles.md`, `gm-notes/20-gm-persona.md`, `gm-notes/45-gm-quick-calls.md`. The engine loads the persona and length rule from those files at session start; it does not copy them here, so one edit updates both.

## 1. Fast narrator: system prompt (engine fills `{persona}` from 20-gm-persona.md "Copy-paste description")
```
You are the GM narrator of a Dungeon Crawler Carl-style 5e game, on live voice.
{persona}
Every number in the snapshot is final. Code already rolled and applied it. Never change, add or invent a roll, HP, damage, DC, credit, item or rule. Never reveal anything not in the snapshot.
Write 2-4 short spoken sentences. Second person to the acting Crawler. Players are always "Crawlers".
Say each roll that matters out loud, plainly, once: "Shirayuki rolls a 19 to hit, that's 9 damage."
Output tagged lines only:
[GM] narration, jokes, achievements, loot callouts (default)
[SYSTEM] dry rules notes, refusals, timers, fees. No jokes. Re-tag [GM] after it.
[NPC: Name] an NPC speaking (name exactly as given in the snapshot)
End by naming whose turn is next, exactly as the snapshot says.
Hints in the snapshot marked `hint` are subtle: at most one per reply, never stated outright.
```

## 2. Fast narrator: user message (engine-built, under ~600 tokens)
```
ROOM: {room.read_aloud_short} | visible: {room.visible}
ACTOR: {crawler} ({player}) HP {hp}/{max} {conditions}
ACTION: {player_line}
RESULT: {resolved: rolls with totals vs target, hit/miss, damage, effects}
OTHERS: {changes to other combatants}
EVENTS: {achievements/loot/secret reveals already granted, with Reward lines}
HINT: {optional hint text or none}
NEXT: {next player} ({crawler})
```
`[ROLL]` lines are added by code from RESULT, never by the model, and are never spoken.

## 3. Strong model: ruling prompt (only when the parser finds no rule)
```
You are the rules judge for a 5e (2024) + Dungeon Crawler Carl homebrew game. A Crawler tried something no coded rule covers.
Rule fast and fair, in favor of fun, within 5e. Never set HP, credits or items directly.
Reply with JSON only: {"ruling": "one sentence", "resolve_as": "attack|save|check|damage|heal|condition|move|item|none", "params": {...}, "log": "why"}
```
Input: player line, snapshot, the full room card (secrets included), rule excerpts the code picks by tag, and `45-gm-quick-calls.md`. Code validates `params`; on failure it says `[SYSTEM] The System doesn't support that. Try something else.` and logs it.

## 4. Things the engine must enforce (lessons from s1, 2026-10-07)
- One turn at a time: a line is consumed only by the turn that resolves it (lost-line bug).
- Spotlight: only the active player's lines act; anyone saying "AI" can ask a question that does not spend their turn. Questions are answered without ending the turn.
- Split speech: wait about 4 s for a sentence to finish before resolving; join fragments from the same player.
- Players roll their own death saves unless they say "go"; code may auto-roll when every Crawler is down (stated aloud).
- Enemies skip downed Crawlers unless the encounter card says otherwise.
- Death, wipe and "end the campaign": only Caleb ends a campaign. A player saying "we're dead" is not an end command.
- Private reveals (Benefactor Signal, Proctor hints) go as `whisper` to the Crawler's sheet channel, never voice.
- Message length: chunk speech so nothing is cut off.

## 5. Replay test (C1 done-check, GM owns the script)
Script: `engine/tests/replay/s1-2026-10-07-shooting-gallery.jsonl`, one player line per step with the forced dice from `sessions-data/s1/rolls-2026-10-07.log`, and the expected HP/conditions after each step. GM writes it after C1 lands its replay format; source lines are in `sessions-data/s1/transcripts/2026-10-07-table.md`. Known corrections the engine must make vs. what happened live: Cunning Action refused at Rogue 1; one mannequin to-hit value; no disadvantage on a save from being hidden.
