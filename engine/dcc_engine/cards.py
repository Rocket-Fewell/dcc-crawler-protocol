"""Load the card pack. Numbers come off the cards. This file does not invent them."""

import json
import re

from dcc_engine.paths import CARDS_DIR, FIXTURES_DIR

_PASSIVE = re.compile(r"Passive Perception\s+(\d+)")


def _read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_monster(card_id):
    catalog = _read(CARDS_DIR / "monsters" / "catalog.json")
    for card in catalog["cards"]:
        if card["id"] == card_id:
            return card
    raise KeyError(card_id)


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


def monster_combatant(monster, number):
    """One enemy in memory. to-hit and damage are copied off local.attacks."""
    labels = monster["stat_block"].get("labels") or {}
    senses = labels.get("Senses", "")
    found = _PASSIVE.search(senses)
    if not found:
        raise ValueError(f"{monster['id']} has no Passive Perception on the stat card")
    attacks = [attack_record(raw) for raw in monster["local"]["attacks"]]
    ranged = next(item for item in attacks if item["kind"] == "ranged")
    melee = next(item for item in attacks if item["kind"] == "melee")
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
