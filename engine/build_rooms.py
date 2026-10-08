#!/usr/bin/env python3
"""Build Floor 1 room cards from the day specs and the overview zone graph.

Hand edits belong in the specs. Run this script again after a spec change.
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

# One attack, one to-hit. Shape for the engine until Encounter files the real block.
STATS = {
    "skeleton": {"ac": 13, "hp": 13, "to_hit": 4, "damage": "1d6+2", "attack": "Shortbow", "type": "piercing", "vulnerable": ["bludgeoning"]},
    "animated-armor": {"ac": 18, "hp": 33, "to_hit": 4, "damage": "1d6+2", "attack": "Slam", "type": "bludgeoning", "vulnerable": []},
    "animated-flying-sword": {"ac": 17, "hp": 17, "to_hit": 5, "damage": "1d8+3", "attack": "Slash", "type": "slashing", "vulnerable": []},
    "giant-rat": {"ac": 13, "hp": 7, "to_hit": 5, "damage": "1d4+3", "attack": "Bite", "type": "piercing", "vulnerable": []},
    "stirge": {"ac": 13, "hp": 5, "to_hit": 5, "damage": "1d4+3", "attack": "Blood Drain", "type": "piercing", "vulnerable": []},
    "goblin-warrior": {"ac": 15, "hp": 10, "to_hit": 4, "damage": "1d6+2", "attack": "Scimitar", "type": "slashing", "vulnerable": []},
    "goblin-minion": {"ac": 12, "hp": 3, "to_hit": 4, "damage": "1d4+2", "attack": "Dagger", "type": "piercing", "vulnerable": []},
    "bugbear-warrior": {"ac": 14, "hp": 27, "to_hit": 4, "damage": "1d8+2", "attack": "Morningstar", "type": "piercing", "vulnerable": []},
    "ogre": {"ac": 11, "hp": 68, "to_hit": 6, "damage": "2d8+4", "attack": "Greatclub", "type": "bludgeoning", "vulnerable": []},
}


def clip(text, words=28):
    parts = (text or "").replace("\n", " ").split()
    if len(parts) <= words:
        return " ".join(parts)
    return " ".join(parts[:words])


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


def encounter_rows(enc):
    trigger = "on_enter" if enc.get("kind") == "combat" else "on_search"
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
    # unique, stable
    seen = []
    out = []
    for row in rows:
        key = json.dumps(row, sort_keys=True)
        if key not in seen:
            seen.append(key)
            out.append(row)
    return out[:6]


def voice_of(enc):
    lines = enc.get("voice_lines") or {}
    def text(key):
        node = lines.get(key) or {}
        if isinstance(node, dict):
            return clip(node.get("text") or "", 24)
        return clip(str(node), 24)
    intro = text("system_intro") or "The room is open."
    twist = text("midpoint_twist") or "Something in the room changes."
    win = text("win") or "The room is clear."
    return {"intro": intro, "twist": twist, "win": win}


def map_of(enc, zone):
    mind = enc.get("map_in_the_mind") or {}
    layout = clip(mind.get("layout") or NAMES[zone], 22)
    cover = mind.get("cover") or []
    hazards = mind.get("hazards") or []
    if isinstance(cover, list):
        cover = "; ".join(cover)
    if isinstance(hazards, list):
        hazards = "; ".join(hazards)
    return {
        "layout": layout,
        "cover": clip(cover or "No listed cover.", 18),
        "hazards": clip(hazards or "No listed hazard.", 18),
    }


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
    return {
        "id": "f01-%s" % zone,
        "floor": 1,
        "zone": zone,
        "name": NAMES[zone],
        "days_open": DAYS[zone],
        "narrator_line": clip(NAMES[zone] + ". The floor keeps its own clock.", 16),
        "map": {
            "layout": NAMES[zone] + ".",
            "cover": "No listed cover.",
            "hazards": "No listed hazard.",
        },
        "exits": exits_for(zone),
        "encounters": [],
        "secrets": [],
        "loot": [],
        "npcs": [],
        "voice_lines": {
            "intro": NAMES[zone] + " is ahead.",
            "twist": "The room does not stay still.",
            "win": "You can leave when you are ready.",
        },
        "item_hooks": [],
        "flags": {"cleared": False, "looted": False, "rested": False},
        "source": {"spec": "floors/f01/00-overview.md", "enc_id": "overview-4.2"},
    }


def from_encounter(zone, enc, spec_path):
    room = blank_room(zone)
    room["name"] = enc.get("zone_name") or enc.get("name") or NAMES[zone]
    room["narrator_line"] = voice_of(enc)["intro"]
    room["map"] = map_of(enc, zone)
    room["encounters"] = encounter_rows(enc)
    room["loot"] = loot_rows(enc)
    room["voice_lines"] = voice_of(enc)
    flavors = ((enc.get("gm_notes") or {}).get("flavor")) or []
    room["item_hooks"] = [clip(line, 20) for line in flavors[:4]]
    room["source"] = {"spec": str(spec_path.relative_to(ROOT)), "enc_id": enc["id"]}
    if zone in NPCS:
        name, voice = NPCS[zone]
        room["npcs"] = [{"name": name, "voice": voice}]
    if zone == "z03":
        room["secrets"] = z03_secrets()
    return room


VENDOR_ODDITY_BOX = (
    "╔══ ITEM ════════════════════════════════════════════╗\n"
    "  Vendor Oddity (Unappraised)\n"
    "  A coin. Probably. Value: ???\n"
    "  This item cannot be sold. Please don't try. It's\n"
    "  embarrassing for everyone.\n"
    "╚════════════════════════════════════════════════════╝"
)


def z03_secrets():
    return [
        {
            "id": "unclaimed-crate",
            "trigger": {"type": "action", "verb": "open", "target": "UNCLAIMED crate"},
            "reveal_text": "Oddity logged.",
            "gm_only": False,
            "grants": {
                "item": "Vendor Oddity (Unappraised)",
                "box_text": VENDOR_ODDITY_BOX,
            },
            "sets_flag": "SEED-ODDCOIN",
            "flag_holder": "opener",
            "achievement": {"id": "ACH-0081", "name": "Odd Coin Pocketed", "hidden": True, "toast": "Oddity logged.", "reward": None},
            "gm_note": "No check. If the crate is never opened, the coin comes as a Weird pull in the first Green Room box (lore card f01-z09-0001), or from Dale's pocket if he dies. Must be planted on Floor 1.",
        },
        {
            "id": "odd-coin-identify",
            "trigger": {
                "type": "item",
                "item": "Vendor Oddity (Unappraised)",
                "actions": ["sell", "identify", "appraise"],
            },
            "reveal_text": "ITEM NOT RECOGNIZED.",
            "gm_only": False,
            "gm_note": "Same reply for sell, identify or appraise (Snakk-Matic, spell, check, or asking an NPC). Selling can instead get a 500-credit offer that cancels mid-animation. Never name a floor, fee or time. Never explain it.",
        },
        {
            "id": "back-cage",
            "triggers": [
                {"type": "check", "skill": "Perception", "dc": 15, "passive": True},
                {"type": "check", "skill": "Investigation", "dc": 13, "when": "someone says they are checking behind the machines"},
            ],
            "reveal_text": "A false panel behind the change machine opens the back cage.",
            "opens_exit": "f01-z03b",
            "gm_only": False,
        },
    ]


def back_cage():
    room = blank_room("z03b")
    room["narrator_line"] = "Behind the panel, a wire cage nobody was meant to find, and a stash somebody meant to come back for."
    room["voice_lines"] = {
        "intro": "Behind the panel, a wire cage nobody was meant to find, and a stash somebody meant to come back for.",
        "twist": "Something in here is stenciled PROPERTY OF ORIENTATION. Orientation is not coming back for it.",
        "win": "The map is scrawled in a hurry, and it shows a door that isn't on yours.",
    }
    room["loot"] = [
        {"item": "Potion of Healing", "label": "Sports Drink, Blue Flavor, Do Not Ask"},
        {"item": "Shield", "label": "riot shield stenciled PROPERTY OF ORIENTATION"},
        {"roll": "3d6 x 5", "unit": "credits"},
        {"item": "scrawled map", "reveals": "f01-zS"},
    ]
    room["achievements"] = [
        {"id": "ACH-0177", "name": "Hidden Cache", "when": "on_loot"},
        {"id": "ACH-0179", "name": "Side Path", "when": "zone_s_revealed"},
    ]
    room["source"] = {"spec": "floors/f01/00-overview.md", "enc_id": "overview-5.3"}
    return room


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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
        "source": "engine/build_rooms.py one to-hit; Encounter owns the final block",
    }


def main():
    specs = load_specs()
    by_zone = {}
    later = {2: {}, 3: {}, 4: {}, 5: {}}
    srd_ids = set()
    for day, path, spec in specs:
        for enc in spec.get("encounters") or []:
            zone = enc.get("zone")
            if zone not in DAYS:
                continue
            if zone not in by_zone:
                by_zone[zone] = from_encounter(zone, enc, path)
            else:
                patch = {"day_encounters": encounter_rows(enc)}
                later[day][by_zone[zone]["id"]] = patch
            for row in encounter_rows(enc):
                if row.get("srd_id"):
                    srd_ids.add(row["srd_id"])
    by_zone["z03b"] = back_cage()
    for zone in DAYS:
        by_zone.setdefault(zone, blank_room(zone))
        if zone in NPCS and not by_zone[zone]["npcs"]:
            name, voice = NPCS[zone]
            by_zone[zone]["npcs"] = [{"name": name, "voice": voice}]
    for zone, room in by_zone.items():
        write(OUT_ROOMS / ("%s.json" % room["id"]), room)
    for srd_id in sorted(srd_ids):
        write(OUT_STATS / ("%s.json" % srd_id), stat_block(srd_id))
    # Day overlays from the clock, not new rooms.
    later[2].setdefault("f01-z00", {"closed": True})
    for zone in ("z00", "z01", "z02", "z03", "z03b", "z04"):
        later[2]["f01-%s" % zone] = {"closed": True, "hooks": "gone"}
    for zone in ("z05", "z07", "z08"):
        later[3]["f01-%s" % zone] = {"hooks": "gone"}
    later[4]["f01-z06"] = {"saferoom": False, "vendors": "closed"}
    later[5]["f01-z09"] = {"open": True}
    for day, patch in later.items():
        if patch:
            write(OUT_LAYERS / ("day-%02d.json" % day), patch)
    print("rooms %d, stat blocks %d" % (len(by_zone), len(srd_ids)))


if __name__ == "__main__":
    main()
