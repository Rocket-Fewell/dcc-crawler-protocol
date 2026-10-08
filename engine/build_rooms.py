#!/usr/bin/env python3
"""Build Floor 1 room cards from the day specs and the overview zone graph.

Hand edits belong in the specs. Run this script again after a spec change.
Day-specific fights go on day layers. The base card keeps an encounter only
when that fight is on the room's first open day.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_DIR = ROOT / "floors" / "f01"
OUT_ROOMS = ROOT / "engine" / "data" / "rooms" / "f01"
OUT_STATS = ROOT / "engine" / "data" / "stat-blocks"
OUT_LAYERS = ROOT / "engine" / "data" / "layers" / "f01"

# Overview section 4.2. kind is door, vent, or stairs.
EDGES = [
    ("z00", "z01", "door", None, None),
    ("z01", "z02", "door", None, None),
    ("z02", "z03", "vent", None, None),
    ("z03", "z03b", "door", None, "back-cage"),
    ("z03", "z04", "door", None, None),
    ("z04", "z05", "door", None, None),
    ("z05", "z06", "door", None, None),
    ("z06", "z07", "door", None, None),
    ("z06", "z08", "door", None, None),
    ("z08", "z09", "door", None, None),
    ("z09", "z10", "door", None, None),
    ("z10", "z11", "stairs", None, None),
    ("z10", "zS", "door", None, None),
    ("zS", "z11", "stairs", "service-key", None),
]

# Days the room can still be entered. Hooks may close earlier; that is a layer.
DAYS = {
    "z00": [1], "z01": [1], "z02": [1], "z03": [1], "z03b": [1], "z04": [1],
    "z05": [1, 2], "z07": [1, 2],
    "z06": [1, 2, 3, 4, 5], "z08": [1, 2, 3, 4, 5], "z09": [1, 2, 3, 4, 5],
    "z10": [1, 2, 3, 4, 5], "z11": [1, 2, 3, 4, 5], "zS": [1, 2, 3, 4, 5],
}

NAMES = {
    "z00": "Intake Hall",
    "z01": "The Atrium",
    "z02": "Vent Row",
    "z03": "Vending Gore Arcade",
    "z03b": "Lost & Found, back cage",
    "z04": "Hall of Fair Warnings",
    "z05": "Shooting Gallery",
    "z06": "The Break Room",
    "z07": "The Big Green EXIT",
    "z08": "Mascot Locker Room",
    "z09": "The Green Room",
    "z10": "Graduation Stage",
    "z11": "The Stairwell",
    "zS": "Service Corridor",
    "wandering": "Wandering",
}

NPCS = {
    "z04": ("Dale Pruitt", "Dale Pruitt"),
    "z05": ("Proctor Bell", "Proctor Bell"),
    "z06": ("Proctor Bell", "Proctor Bell"),
    "z07": ("Exit Greeter", "Exit Greeter"),
    "z08": ("Bruiser the Mascot", "Bruiser the Mascot"),
    "z09": ("Proctor Bell", "Proctor Bell"),
    "z10": ("Dean Thudd", "Dean Thudd"),
}

# One attack, one to-hit. 2024 numbers are the ones the C1 review named.
# Floor specs do not print AC, HP, or to-hit, so unnamed fields stay put.
# Encounter owns the final block.
STATS = {
    "skeleton": {"ac": 14, "hp": 13, "to_hit": 5, "damage": "1d6+3", "attack": "Shortbow", "type": "piercing", "vulnerable": ["bludgeoning"]},
    "animated-armor": {"ac": 18, "hp": 33, "to_hit": 4, "damage": "1d6+2", "attack": "Slam", "type": "bludgeoning", "vulnerable": []},
    "animated-flying-sword": {"ac": 17, "hp": 14, "to_hit": 4, "damage": "1d8+2", "attack": "Slash", "type": "slashing", "vulnerable": []},
    "giant-rat": {"ac": 13, "hp": 7, "to_hit": 5, "damage": "1d4+3", "attack": "Bite", "type": "piercing", "vulnerable": []},
    "stirge": {"ac": 13, "hp": 5, "to_hit": 5, "damage": "1d6+3", "attack": "Proboscis", "type": "piercing", "vulnerable": []},
    "goblin-warrior": {"ac": 15, "hp": 10, "to_hit": 4, "damage": "1d6+2", "attack": "Scimitar", "type": "slashing", "vulnerable": []},
    "goblin-minion": {"ac": 12, "hp": 7, "to_hit": 4, "damage": "1d4+2", "attack": "Dagger", "type": "piercing", "vulnerable": []},
    "bugbear-warrior": {"ac": 14, "hp": 33, "to_hit": 4, "damage": "2d6+2", "attack": "Grab", "type": "bludgeoning", "vulnerable": []},
    "ogre": {"ac": 11, "hp": 68, "to_hit": 6, "damage": "2d8+4", "attack": "Greatclub", "type": "bludgeoning", "vulnerable": []},
}


def complete_sentences(text):
    """Split on sentence ends. A fragment with no ending is dropped."""
    flat = " ".join((text or "").replace("\n", " ").split())
    sentences = []
    buf = []
    i = 0
    while i < len(flat):
        ch = flat[i]
        buf.append(ch)
        if ch in ".!?":
            nxt = flat[i + 1] if i + 1 < len(flat) else ""
            prev = flat[i - 1] if i else ""
            if nxt == "" or nxt.isspace():
                if prev not in ".!?":
                    sentences.append("".join(buf).strip())
                    buf = []
        i += 1
    return [s for s in sentences if s]


def clip_sentences(text, words=28, fallback=""):
    """Keep whole sentences until the next one would pass the word budget."""
    sentences = complete_sentences(text)
    if not sentences:
        return fallback
    kept = []
    count = 0
    for sentence in sentences:
        n = len(sentence.split())
        if kept and count + n > words:
            break
        kept.append(sentence)
        count += n
    return " ".join(kept) if kept else fallback


def load_specs():
    found = []
    for path in sorted(SPEC_DIR.glob("day-0*.spec.json")):
        spec = json.loads(path.read_text(encoding="utf-8"))
        day = int(spec["day"]["number"])
        found.append((day, path, spec))
    return found


def b70(node):
    if isinstance(node, dict):
        return node.get("b70") or {}
    return {}


def trigger_for(kind):
    """Fights start on entry. 'non-combat' is not a fight."""
    text = (kind or "").lower().replace("non-combat", " ")
    if "boss" in text or "fight" in text or "combat" in text:
        return "on_enter"
    return "on_search"


def encounter_rows(enc):
    trigger = trigger_for(enc.get("kind"))
    enemies = enc.get("enemies") or []
    if not enemies:
        return [{
            "enc_id": enc["id"],
            "srd_id": None,
            "our_name": enc.get("name"),
            "count_ref": None,
            "cr_ref": None,
            "trigger": trigger,
        }]
    rows = []
    for enemy in enemies:
        count = b70(enemy.get("count_slot"))
        cr = b70(enemy.get("cr_slot"))
        rows.append({
            "enc_id": enc["id"],
            "srd_id": enemy.get("srd_id"),
            "our_name": enemy.get("our_name") or enemy.get("srd_name"),
            "count_ref": {"path": count["path"], "key": count.get("key")} if count.get("path") else None,
            "cr_ref": {"path": cr["path"], "key": cr.get("key")} if cr.get("path") else None,
            "trigger": trigger,
        })
    return rows


def loot_rows(enc):
    rows = []
    for hook in enc.get("loot_hooks") or []:
        amount = b70(hook.get("amount"))
        if isinstance(amount, dict) and amount.get("path"):
            rows.append({"dice_ref": amount["path"]})
        elif hook.get("card_id"):
            rows.append({"deck": hook["card_id"]})
    seen = []
    out = []
    for row in rows:
        key = json.dumps(row, sort_keys=True)
        if key not in seen:
            seen.append(key)
            out.append(row)
    return out[:6]


def fill_clock(text, clock):
    """Fill spec placeholders from the day spec. {days} is clock.days, never a guess."""
    clock = clock or {}
    out = text or ""
    if clock.get("days") is not None:
        out = out.replace("{days}", str(clock["days"]))
    if clock.get("day") is not None:
        out = out.replace("{day}", str(clock["day"]))
    return out


def voice_text(enc, key, clock=None):
    lines = enc.get("voice_lines") or {}
    node = lines.get(key) or {}
    if isinstance(node, dict):
        raw = node.get("text") or ""
    else:
        raw = str(node or "")
    return fill_clock(raw, clock)


def voice_of(enc, fallback_name, clock=None):
    intro = clip_sentences(voice_text(enc, "system_intro", clock), 28, fallback_name + " is ahead.")
    twist = clip_sentences(voice_text(enc, "midpoint_twist", clock), 24, "Something in the room changes.")
    win = clip_sentences(voice_text(enc, "win", clock), 24, "The room is clear.")
    return {"intro": intro, "twist": twist, "win": win}


def read_aloud_of(enc, fallback, clock=None):
    sentences = complete_sentences(voice_text(enc, "system_intro", clock))
    if sentences:
        return " ".join(sentences)
    return fallback


def map_of(enc, zone):
    mind = enc.get("map_in_the_mind") or {}
    layout = mind.get("layout") or NAMES.get(zone, zone)
    cover = mind.get("cover") or []
    hazards = mind.get("hazards") or []
    if isinstance(cover, list):
        cover = " ".join(str(x) for x in cover)
    if isinstance(hazards, list):
        hazards = " ".join(str(x) for x in hazards)
    name = NAMES.get(zone, zone)
    return {
        "layout": clip_sentences(layout, 22, name + "."),
        "cover": clip_sentences(cover, 18, "No listed cover."),
        "hazards": clip_sentences(hazards, 18, "No listed hazard."),
    }


def position_name(line):
    """Keep a whole sentence. Never stop on a word count."""
    sentences = complete_sentences(line)
    if sentences:
        return sentences[0]
    return " ".join(str(line).split()) or "Cover"


def positions_of(enc):
    mind = enc.get("map_in_the_mind") or {}
    rows = [{"id": "entry", "name": "Entry"}]
    cover = mind.get("cover") or []
    if isinstance(cover, str):
        cover = [cover]
    for i, line in enumerate(list(cover)[:3]):
        rows.append({"id": "cover-%d" % (i + 1), "name": position_name(line)})
    return rows


def gm_notes_of(enc):
    notes = enc.get("gm_notes")
    if isinstance(notes, (dict, str)) and notes:
        return notes
    return {"tag": "[GM-FACING]", "flavor": []}


def rest_of(zone, enc):
    """Day 1 offers a Long Rest at both saferooms. The Green Room also opens boxes."""
    kind = (enc.get("kind") or "").lower() if enc else ""
    if zone == "z09" or "rest" in kind:
        return {"kind": "long", "saferoom": True, "fee": None, "boxes": "open"}
    if zone == "z06" and "hazard" not in kind:
        return {"kind": "long", "also": ["short"], "saferoom": True, "fee": None}
    return None


def exits_for(zone):
    outs = []
    for a, b, kind, locked, hidden in EDGES:
        other = b if a == zone else a if b == zone else None
        if other is None:
            continue
        row = {"to": "f01-%s" % other, "kind": kind}
        if locked and a == zone:
            row["locked_by"] = locked
        if hidden and a == zone:
            row["hidden_by_secret"] = hidden
        outs.append(row)
    return outs


def blank_room(zone):
    name = NAMES.get(zone, zone)
    line = name + " is ahead."
    return {
        "id": "f01-%s" % zone,
        "floor": 1,
        "zone": zone,
        "name": name,
        "days_open": DAYS.get(zone) or [1],
        "narrator_line": line,
        "read_aloud": line,
        "positions": [{"id": "entry", "name": "Entry"}],
        "map": {
            "layout": name + ".",
            "cover": "No listed cover.",
            "hazards": "No listed hazard.",
        },
        "exits": exits_for(zone),
        "encounters": [],
        "secrets": [],
        "loot": [],
        "npcs": [],
        "voice_lines": {
            "intro": line,
            "twist": "The room does not stay still.",
            "win": "You can leave when you are ready.",
        },
        "item_hooks": [],
        "rest": rest_of(zone, None),
        "gm_notes": {"tag": "[GM-FACING]", "flavor": []},
        "flags": {"cleared": False, "looted": False, "rested": False},
        "source": {"spec": "floors/f01/00-overview.md", "enc_id": "overview-4.2"},
    }


def apply_prose(room, enc, spec_path, clock=None):
    zone = room["zone"]
    fallback = NAMES.get(zone, zone) + " is ahead."
    room["name"] = enc.get("zone_name") or enc.get("name") or room["name"]
    voices = voice_of(enc, NAMES.get(zone, zone), clock)
    room["narrator_line"] = voices["intro"]
    room["read_aloud"] = read_aloud_of(enc, fallback, clock)
    room["map"] = map_of(enc, zone)
    room["positions"] = positions_of(enc)
    room["voice_lines"] = voices
    flavors = ((enc.get("gm_notes") or {}).get("flavor")) or []
    hooks = []
    for line in flavors[:4]:
        kept = clip_sentences(str(line), 40, fallback="")
        if kept:
            hooks.append(kept)
    room["item_hooks"] = hooks
    room["gm_notes"] = gm_notes_of(enc)
    room["rest"] = rest_of(zone, enc)
    room["source"] = {"spec": str(spec_path.relative_to(ROOT)), "enc_id": enc["id"]}
    return room


def from_encounter(zone, enc, spec_path, clock=None):
    room = blank_room(zone)
    apply_prose(room, enc, spec_path, clock)
    room["encounters"] = encounter_rows(enc)
    room["loot"] = loot_rows(enc)
    if zone in NPCS:
        name, voice = NPCS[zone]
        room["npcs"] = [{"name": name, "voice": voice}]
    return room


def back_cage():
    """Shell only. Lore's lines live in engine/overrides/f01.json."""
    room = blank_room("z03b")
    room["source"] = {"spec": "floors/f01/00-overview.md", "enc_id": "overview-5.3"}
    return room


def load_overrides():
    path = ROOT / "engine" / "overrides" / "f01.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def apply_override(room, overrides):
    patch = ((overrides or {}).get("rooms") or {}).get(room["id"])
    if not isinstance(patch, dict):
        return room
    for key, val in patch.items():
        if key == "voice_lines" and isinstance(val, dict):
            merged = dict(room.get("voice_lines") or {})
            merged.update(val)
            room["voice_lines"] = merged
        elif key == "loot_add" and isinstance(val, list):
            room["loot"] = list(room.get("loot") or []) + val
        elif key == "npc_lines" and isinstance(val, dict):
            for npc in room.get("npcs") or []:
                line = val.get(npc.get("name"))
                if line:
                    npc["line"] = line
        else:
            room[key] = val
    return room


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def merge_layer(layer, room_id, patch):
    """Add a patch onto a day's room entry. Lists of encounters append."""
    cur = layer.get(room_id)
    if not isinstance(cur, dict):
        layer[room_id] = json.loads(json.dumps(patch))
        return
    for key, val in patch.items():
        if key == "day_encounters" and isinstance(val, list):
            cur[key] = list(cur.get(key) or []) + val
        elif isinstance(val, dict) and isinstance(cur.get(key), dict):
            merged = dict(cur[key])
            merged.update(val)
            cur[key] = merged
        else:
            cur[key] = val


def stat_block(srd_id):
    row = STATS.get(srd_id) or {
        "ac": 10, "hp": 4, "to_hit": 2, "damage": "1d4", "attack": "Strike", "type": "bludgeoning", "vulnerable": [],
    }
    return {
        "id": srd_id,
        "name": srd_id,
        "ac": row["ac"],
        "hp": row["hp"],
        "attacks": [{
            "name": row["attack"],
            "to_hit": row["to_hit"],
            "damage": row["damage"],
            "type": row["type"],
        }],
        "vulnerable": row["vulnerable"],
        "source": "5e 2024 where the C1 review named a number; Encounter owns the final block. Floor specs do not print these figures.",
    }


def group_specs(specs):
    grouped = {}
    for day, path, spec in specs:
        for enc in spec.get("encounters") or []:
            zone = enc.get("zone")
            if not zone:
                continue
            grouped.setdefault(zone, {}).setdefault(day, []).append((enc, path))
    return grouped


def clock_for(path, day):
    spec = json.loads(Path(path).read_text(encoding="utf-8"))
    return {"days": (spec.get("clock") or {}).get("days"), "day": day}


def collapse_notice(specs, day):
    """The day's dry floor notice. A sentence with an unfilled blank is dropped."""
    for number, _path, spec in specs:
        if number != day:
            continue
        notice = ((spec.get("day") or {}).get("collapse_notice") or {})
        text = " ".join((notice.get("text") or "").split())
        kept = [sentence for sentence in complete_sentences(text) if "{" not in sentence]
        gm = " ".join((((notice.get("gm_color") or {}).get("text")) or "").split())
        return " ".join(kept), gm
    return "", ""


def scene_voice(specs, enc_id):
    for _number, _path, spec in specs:
        clock = {"days": (spec.get("clock") or {}).get("days"), "day": (spec.get("day") or {}).get("number")}
        for enc in spec.get("encounters") or []:
            if enc.get("id") == enc_id:
                return voice_of(enc, enc.get("name") or "The room", clock)
    return None


def stamp_closed_text(cur, specs, day):
    """Replace a closed zone's old read-aloud with that day's dry floor notice."""
    notice, gm = collapse_notice(specs, day)
    if not notice:
        return
    scene = None
    for row in cur.get("day_encounters") or []:
        if not row.get("srd_id") and row.get("enc_id"):
            scene = scene_voice(specs, row["enc_id"])
            break
    intro = (scene or {}).get("intro") or notice
    cur["narrator_line"] = notice
    cur["read_aloud"] = intro if scene else notice
    cur["voice_lines"] = {
        "intro": intro,
        "twist": (scene or {}).get("twist") or notice,
        "win": (scene or {}).get("win") or notice,
    }
    cur["map"] = {
        "layout": "This zone is closed.",
        "cover": "No listed cover.",
        "hazards": "No listed hazard.",
    }
    if gm:
        cur["gm_notes"] = {"tag": "[GM-FACING]", "flavor": [gm]}


def close_room(layer, room_id, specs, day, extra=None):
    """Drop the day's fights. A non-combat scene stays. The room stays passable."""
    cur = layer.get(room_id)
    if not isinstance(cur, dict):
        cur = {}
    scenes = [row for row in (cur.get("day_encounters") or []) if not row.get("srd_id")]
    patch = {
        "closed": True,
        "passable": True,
        "day_encounters": scenes,
        "loot": [],
        "achievements": [],
        "item_hooks": [],
        "npcs": [],
        "key": None,
        "rest": None,
    }
    if extra:
        patch.update(extra)
    cur.update(patch)
    stamp_closed_text(cur, specs, day)
    layer[room_id] = cur


def main():
    specs = load_specs()
    overrides = load_overrides()
    grouped = group_specs(specs)
    by_zone = {}
    later = {2: {}, 3: {}, 4: {}, 5: {}}
    srd_ids = set()

    def take_rows(encounters):
        rows = []
        for enc, _path in encounters:
            rows.extend(encounter_rows(enc))
            for row in rows:
                if row.get("srd_id"):
                    srd_ids.add(row["srd_id"])
        return rows

    for zone, days in list(DAYS.items()):
        if zone == "z03b":
            continue
        found = grouped.get(zone) or {}
        first_open = min(days)
        if first_open in found:
            enc, path = found[first_open][0]
            room = from_encounter(zone, enc, path, clock_for(path, first_open))
            for extra, _path in found[first_open][1:]:
                room["encounters"].extend(encounter_rows(extra))
                room["loot"].extend(loot_rows(extra))
            for row in room["encounters"]:
                if row.get("srd_id"):
                    srd_ids.add(row["srd_id"])
        else:
            room = blank_room(zone)
            if found:
                earliest = min(found)
                enc, path = found[earliest][0]
                apply_prose(room, enc, path, clock_for(path, earliest))
                room["encounters"] = []
                room["loot"] = []
        by_zone[zone] = room
        for day, encounters in found.items():
            on_base = day == first_open and first_open in found
            if on_base:
                continue
            if day not in later:
                later[day] = {}
            merge_layer(later[day], room["id"], {"day_encounters": take_rows(encounters)})

    if "wandering" in grouped:
        found = grouped["wandering"]
        first = min(found)
        enc, path = found[first][0]
        room = from_encounter("wandering", enc, path, clock_for(path, first))
        room["days_open"] = sorted(found)
        room["exits"] = []
        for extra, _path in found[first][1:]:
            room["encounters"].extend(encounter_rows(extra))
        for row in room["encounters"]:
            if row.get("srd_id"):
                srd_ids.add(row["srd_id"])
        by_zone["wandering"] = room
        for day, encounters in found.items():
            if day == first:
                continue
            if day not in later:
                later[day] = {}
            merge_layer(later[day], room["id"], {"day_encounters": take_rows(encounters)})

    by_zone["z03b"] = back_cage()
    for zone in DAYS:
        by_zone.setdefault(zone, blank_room(zone))
        if zone in NPCS and not by_zone[zone]["npcs"]:
            name, voice = NPCS[zone]
            by_zone[zone]["npcs"] = [{"name": name, "voice": voice}]

    for zone in ("z00", "z01", "z02", "z03", "z03b", "z04"):
        room_id = "f01-%s" % zone
        merge_layer(later[2], room_id, {"closed": True, "hooks": "gone"})
        stamp_closed_text(later[2][room_id], specs, 2)
    for zone in ("z05", "z07"):
        close_room(later[3], "f01-%s" % zone, specs, 3, {"hooks": "gone"})
    merge_layer(later[3], "f01-z08", {"hooks": "gone", "npcs": [], "key": None, "loot": []})
    for day in (4, 5):
        for zone in ("z05", "z07", "z08"):
            close_room(later[day], "f01-%s" % zone, specs, day, {"hooks": "gone"})
        close_room(later[day], "f01-z06", specs, day, {"saferoom": False, "vendors": "closed", "hooks": "gone"})
    merge_layer(later[5], "f01-z09", {"open": True})

    for zone, room in by_zone.items():
        apply_override(room, overrides)
        write(OUT_ROOMS / ("%s.json" % room["id"]), room)
    for srd_id in sorted(srd_ids):
        write(OUT_STATS / ("%s.json" % srd_id), stat_block(srd_id))
    for day, patch in later.items():
        if patch:
            write(OUT_LAYERS / ("day-%02d.json" % day), patch)
    print("rooms %d, stat blocks %d" % (len(by_zone), len(srd_ids)))


if __name__ == "__main__":
    main()
