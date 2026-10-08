# Room card format v1
Owner: Architect (format), Encounter (rooms, fights), Lore (secrets, loot, NPCs, achievements), Accountant (counts) | Version: 0.1.1 | Updated: 2026-10-08

One JSON file per room: `engine/data/rooms/f01/<room-id>.json` (id style `f01-z05`). Stat blocks are shared: `engine/data/stat-blocks/<stat-id>.json`. Day overlays: `engine/data/layers/f01/day-NN.json`. There is no second schema file. The check is `PYTHONPATH=engine python -m dcc_engine.validate engine/data`.

The fast narrator only ever sees `name`, `narrator_line`, the map lines, revealed secrets and live combat state. That snapshot stays at or under 150 tokens. Everything else is for code and the strong model.

Counts are never copied into the card. `count_ref` and `cr_ref` are field paths in `rules/70-encounter-budget-5e.json`. The loader fills the number for the party size.

## Room
```json
{
  "id": "f01-z05",
  "floor": 1,
  "zone": "z05",
  "name": "Shooting Gallery",
  "days_open": [1, 2],
  "narrator_line": "Mannequins in staff polos raise pink bows from behind the counter.",
  "map": {
    "layout": "Carnival gallery, counters, sandbags, mannequins at the far counter.",
    "cover": "Counters and sandbags are half cover. The prize booth is three-quarters.",
    "hazards": "A conveyor carries a standing Crawler 10 ft at the end of each round."
  },
  "exits": [
    {"to": "f01-z04", "kind": "door"},
    {"to": "f01-z06", "kind": "door"}
  ],
  "encounters": [
    {
      "enc_id": "enc-d01-11",
      "srd_id": "skeleton",
      "our_name": "Mannequin Staff (Skeleton)",
      "count_ref": {"path": "floors.1.fixed_encounters.z05.counts_by_party_size", "key": "skeleton"},
      "cr_ref": {"path": "floors.1.fixed_encounters.z05.creatures", "key": "skeleton"},
      "trigger": "on_enter"
    }
  ],
  "secrets": [],
  "loot": [
    {"dice_ref": "floors.1.fixed_encounters.z05.cash_dice_per_crawler"}
  ],
  "npcs": [{"name": "Proctor Bell", "voice": "Proctor Bell"}],
  "voice_lines": {"intro": "...", "twist": "...", "win": "..."},
  "item_hooks": [],
  "flags": {"cleared": false, "looted": false, "rested": false},
  "source": {"spec": "floors/f01/day-01.spec.json", "enc_id": "enc-d01-11"}
}
```

`map` is at most four lines (layout, cover, hazards, and one optional extra). Exit `kind` is `door`, `vent`, or `stairs`. Optional exit fields: `locked_by`, `hidden_by_secret`. Encounter `trigger` is `on_enter`, `on_search`, `clock`, or `noise`. Secret `trigger.type` is `check`, `item`, `action`, or `clock`. `voice` on an NPC is a name in `tables/npc-voices.json`. Lore owns `reveal_text`.

## Stat block
```json
{"id": "mannequin-staff", "name": "Mannequin Staff", "ac": 12, "hp": 13, "speed_ft": 30,
 "abilities": {"str": 12, "dex": 12, "con": 12, "int": 3, "wis": 8, "cha": 3},
 "saves": {}, "resist": [], "immune": ["poisoned"], "vulnerable": [],
 "attacks": [{"name": "Pricing gun", "kind": "ranged", "to_hit": 4, "range_ft": [30, 120], "damage": "1d6+2", "type": "piercing"}],
 "traits": [], "xp": 50, "source": "rules/70-encounter-budget-5e.json"}
```
Numbers above are examples of shape only. The real values come from Encounter's pages and Accountant's budget, and each stat block has exactly one to-hit per attack.

## Secret (also used for achievements, with "kind": "achievement")
```json
{"id": "odd-coin-identify", "kind": "secret",
 "trigger": {"type": "item_use", "item": "Odd Coin", "action": ["identify", "appraise"]},
 "reveal": "ITEM NOT RECOGNIZED.", "voice": "SYSTEM",
 "private": false, "once": false, "requires": [], "sets_flags": []}
```
`private: true` sends the reveal only to the triggering Crawler's sheet channel (bridge whisper), never to voice.

## Trigger types (code checks these; anything else is a strong-model call)
- `enter`, `leave`: party or a Crawler enters or leaves the room. Optional `first_time`.
- `clear`: every hostile in the encounter is down.
- `check`: a check of `skill` or `ability` at or above `dc`, optional `target` feature.
- `action`: a parsed action `verb` (search, open, talk, push, break) on `target`.
- `item_use`: `item` used with `action`.
- `say`: a spoken keyword or phrase list (`any_of`), optional `to_npc`.
- `hp`: a Crawler drops to 0 (`at_zero`), or below a fraction.
- `death_save`: first death save of the session, optional `result`.
- `round`: combat round number reached.
- `clock`: floor day or tick reached.
- `flag`: another secret's flag is set (chains).
Each trigger can carry `who: "any|first|each"` and `requires: [flags]`.

## NPC
```json
{"name": "Proctor Bell", "voice": "NPC: Proctor Bell", "position": "booth",
 "disposition": "faux-cheerful", "knows": ["hint-vent-row"], "sells": [{"item": "Hint", "credits": 1}],
 "lines": {"greet": "Little lambs!", "refuse": "Rules are rules, lambs."}}
```
`voice` must match a name in `tables/npc-voices.json`.

## Day layers and generation (Encounter's additions)
- `engine/build_rooms.py` reads `floors/f01/day-0*.spec.json` and the zone graph in `floors/f01/00-overview.md` section 4.2. Hand edits go in the spec, then the script is run again.
- Counts stay as `count_ref` / `cr_ref`. The loader resolves them for the party size.
- Day changes are layers: `engine/data/layers/f01/day-NN.json` holds `{"room_id": {patch}}` overrides (collapses, Lights-Out, vendors closed on Day 4), applied on top of the base room. A collapse is not a new room.
- Tests (`engine/tests/`): every exit target exists; every room is reachable from the Intake Hall (`f01-z00`); the stairwell (`f01-z11`) is reachable; every budget ref resolves; every NPC voice key exists; each room's narration snapshot is 150 tokens or less.

## Validation
`PYTHONPATH=engine python -m dcc_engine.validate engine/data` must report 0 errors before a content PR goes to the vote. The schema lives in `engine/dcc_engine/schema.py` and matches this file. Pilot fight: Shooting Gallery, replayed from `engine/tests/fixtures` with a hand-written dice script until the session roll log is on main.
