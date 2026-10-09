"""Load the card pack. Numbers come off the cards. This file does not invent them."""

import json
import re

from dcc_engine.paths import CARDS_DIR, FIXTURES_DIR

_PASSIVE = re.compile(r"Passive Perception\s+(\d+)")


def _read(path):
    return json.loads(path.read_text(encoding="utf-8"))


_MONSTERS = None


def monster_catalog():
    """One read of the R&D catalog. The live day pages still win on names."""
    global _MONSTERS
    if _MONSTERS is None:
        cards = _read(CARDS_DIR / "monsters" / "catalog.json")["cards"]
        _MONSTERS = {card["id"]: card for card in cards}
    return _MONSTERS


def load_monster(card_id):
    try:
        return monster_catalog()[card_id]
    except KeyError as exc:
        raise KeyError(card_id) from exc


def load_room(room_id):
    return _read(CARDS_DIR / "local" / "rooms" / "f01" / f"{room_id}.json")


def load_pilot():
    return _read(FIXTURES_DIR / "gallery-pilot.json")["card"]


def _words(label):
    if not label:
        return []
    return [part.strip().lower() for part in re.split(r"[;,]", label) if part.strip()]


def attack_record(raw):
    return {
        "name": raw["name"],
        "to_hit": int(raw["to_hit"]),
        "damage": raw["damage"]["dice"],
        "type": raw["damage"]["type"].lower(),
        "kind": raw["kind"],
    }


def _named(items):
    return [
        {"name": item.get("name") or "", "text": item.get("text") or ""}
        for item in items or []
        if item.get("name") or item.get("text")
    ]


def public_block(monster):
    """Printed stat block. GM lines and cheese notes stay off this object."""
    block = monster.get("stat_block") or {}
    abilities = []
    for key in ("str", "dex", "con", "int", "wis", "cha"):
        row = (block.get("abilities") or {}).get(key) or {}
        abilities.append({
            "key": key,
            "score": row.get("score"),
            "mod": row.get("mod"),
            "save": row.get("save"),
        })
    labels = [
        {"name": name, "text": text}
        for name, text in (block.get("labels") or {}).items()
    ]
    return {
        "nameplate": monster.get("nameplate") or "",
        "picture": monster.get("picture") or "",
        "system_line": monster.get("system_line") or "",
        "tactics": monster.get("tactics") or "",
        "type_line": block.get("type_line") or "",
        "ac": block.get("ac"),
        "initiative": block.get("initiative"),
        "hp_formula": block.get("hp_formula") or "",
        "speed": block.get("speed") or "",
        "cr": block.get("cr"),
        "xp": block.get("xp"),
        "pb": block.get("pb"),
        "abilities": abilities,
        "labels": labels,
        "traits": _named(block.get("traits")),
        "actions": _named(block.get("actions")),
        "bonus_actions": _named(block.get("bonus_actions")),
        "reactions": _named(block.get("reactions")),
    }


def monster_combatant(monster, number):
    """One enemy in memory. to-hit and damage are copied off local.attacks."""
    labels = monster["stat_block"].get("labels") or {}
    senses = labels.get("Senses", "")
    found = _PASSIVE.search(senses)
    if not found:
        raise ValueError(f"{monster['id']} has no Passive Perception on the stat card")
    attacks = [attack_record(raw) for raw in monster["local"]["attacks"]]
    ranged = next((item for item in attacks if item["kind"] == "ranged"), None)
    melee = next((item for item in attacks if item["kind"] == "melee"), None)
    if ranged is None and melee is None:
        raise ValueError(f"{monster['id']} has no local attack")
    if ranged is None:
        ranged = melee
    if melee is None:
        melee = ranged
    return {
        "id": f"ms-{number}",
        "name": f"{monster['display_name']} {number}",
        "picture": monster.get("picture") or "",
        "spoken_name": monster.get("lore_floor_name") or monster["display_name"],
        "hp": int(monster["stat_block"]["hp_max"]),
        "hp_max": int(monster["stat_block"]["hp_max"]),
        "ac": int(monster["stat_block"]["ac"]),
        "vulnerabilities": _words(labels.get("Vulnerabilities")),
        "resistances": _words(labels.get("Resistances")),
        "immunities": _words(labels.get("Immunities")),
        "passive_perception": int(found.group(1)),
        "ranged": ranged,
        "melee": melee,
        "system_line": monster.get("system_line") or "",
        "gm_line": monster.get("gm_line") or "",
        "how_to_cheese": monster.get("how_to_cheese") or "",
        "what_it_wants": monster.get("what_it_wants") or "",
        "card": public_block(monster),
        "conditions": [],
    }


def gallery_count(room, party_size):
    """Filed counts only. A solo seat uses the smallest filed party, which is 2."""
    slot = room["encounter"]["enemies"][0]
    counts = slot["counts_by_party_size"]
    key = str(party_size)
    if key not in counts:
        key = "2"
    return int(counts[key]), slot["stat_card"]


def crawler_from_card(card):
    abilities = card.get("abilities") or {}
    hp = card["hp"]
    attacks = []
    for raw in card.get("attacks") or []:
        attacks.append({
            "name": raw["name"],
            "to_hit": int(raw["to_hit"]),
            "damage": raw["damage"],
            "type": str(raw.get("type") or "piercing").lower(),
        })
    return {
        "id": card.get("id") or "crawler",
        "name": card.get("name") or "Crawler",
        "class_name": card.get("class") or card.get("class_name") or "",
        "level": int(card.get("level") or 1),
        "hp": int(hp["current"]),
        "hp_max": int(hp["max"]),
        "ac": int(card.get("ac") or 10),
        "speed_ft": int(card.get("speed_ft") or 30),
        "str_mod": int(abilities.get("str_mod", _mod(abilities.get("str", 10)))),
        "dex_mod": int(abilities.get("dex_mod", _mod(abilities.get("dex", 10)))),
        "pb": int(card.get("proficiency_bonus") or card.get("pb") or 2),
        "skills": [str(item).lower() for item in card.get("skills") or []],
        "attacks": attacks,
        "movement_left": int(card.get("speed_ft") or 30),
        "action": True,
        "bonus": True,
        "reaction": True,
        "object": True,
        "cover": None,
        "hidden": False,
        "dodging": False,
        "disengaged": False,
        "conditions": [],
        "death_success": 0,
        "death_fail": 0,
        "spent_action": "",
    }


def _mod(score):
    return (int(score) - 10) // 2


def has_cunning(crawler):
    """Cunning Action is a Rogue feature at level 2. Level 1 does not have it."""
    return crawler["class_name"].lower() == "rogue" and int(crawler["level"]) >= 2
