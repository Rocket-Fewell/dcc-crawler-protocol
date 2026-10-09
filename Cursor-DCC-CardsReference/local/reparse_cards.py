#!/usr/bin/env python3
"""Reparse the R&D card pack into local-engine cards.

Reads monster-names.json and item-name-punches.json. Writes picture lines,
structured attacks, and item mechanics onto the catalogs. Rebuilds the
floor splits and the readable books' names. Does not touch floors/, rules/,
sessions/, characters/, or lore/.

Run from the repo root:
  python3 Cursor-DCC-CardsReference/local/reparse_cards.py
  python3 Cursor-DCC-CardsReference/local/reparse_cards.py --check
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "Cursor-DCC-CardsReference"
LOCAL = PACK / "local"
CHARGEN = ROOT / "tables" / "chargen-5e.json"
SRD_TXT = ROOT / "srd" / "srd.txt"

# Weapon rows copied from srd/srd.txt "Weapons" table (SRD 5.2.1).
# check_srd_weapons() confirms each damage die still sits on that name's line.
SRD_WEAPONS = {
    "club": {"damage": "1d4", "damage_type": "bludgeoning", "properties": ["light"], "mastery": "Slow"},
    "dagger": {"damage": "1d4", "damage_type": "piercing", "properties": ["finesse", "light", "thrown"], "thrown_ft": [20, 60], "mastery": "Nick"},
    "greatclub": {"damage": "1d8", "damage_type": "bludgeoning", "properties": ["two_handed"], "mastery": "Push"},
    "handaxe": {"damage": "1d6", "damage_type": "slashing", "properties": ["light", "thrown"], "thrown_ft": [20, 60], "mastery": "Vex"},
    "javelin": {"damage": "1d6", "damage_type": "piercing", "properties": ["thrown"], "thrown_ft": [30, 120], "mastery": "Slow"},
    "light-hammer": {"damage": "1d4", "damage_type": "bludgeoning", "properties": ["light", "thrown"], "thrown_ft": [20, 60], "mastery": "Nick"},
    "mace": {"damage": "1d6", "damage_type": "bludgeoning", "properties": [], "mastery": "Sap"},
    "quarterstaff": {"damage": "1d6", "damage_type": "bludgeoning", "properties": ["versatile"], "versatile": "1d8", "mastery": "Topple"},
    "sickle": {"damage": "1d4", "damage_type": "slashing", "properties": ["light"], "mastery": "Nick"},
    "spear": {"damage": "1d6", "damage_type": "piercing", "properties": ["thrown", "versatile"], "thrown_ft": [20, 60], "versatile": "1d8", "mastery": "Sap"},
    "dart": {"damage": "1d4", "damage_type": "piercing", "properties": ["finesse", "thrown"], "thrown_ft": [20, 60], "mastery": "Vex"},
    "light-crossbow": {"damage": "1d8", "damage_type": "piercing", "properties": ["ammunition", "loading", "two_handed"], "range_ft": [80, 320], "mastery": "Slow"},
    "shortbow": {"damage": "1d6", "damage_type": "piercing", "properties": ["ammunition", "two_handed"], "range_ft": [80, 320], "mastery": "Vex"},
    "sling": {"damage": "1d4", "damage_type": "bludgeoning", "properties": ["ammunition"], "range_ft": [30, 120], "mastery": "Slow"},
    "battleaxe": {"damage": "1d8", "damage_type": "slashing", "properties": ["versatile"], "versatile": "1d10", "mastery": "Topple"},
    "flail": {"damage": "1d8", "damage_type": "bludgeoning", "properties": [], "mastery": "Sap"},
    "glaive": {"damage": "1d10", "damage_type": "slashing", "properties": ["heavy", "reach", "two_handed"], "mastery": "Graze"},
    "greataxe": {"damage": "1d12", "damage_type": "slashing", "properties": ["heavy", "two_handed"], "mastery": "Cleave"},
    "greatsword": {"damage": "2d6", "damage_type": "slashing", "properties": ["heavy", "two_handed"], "mastery": "Graze"},
    "halberd": {"damage": "1d10", "damage_type": "slashing", "properties": ["heavy", "reach", "two_handed"], "mastery": "Cleave"},
    "lance": {"damage": "1d10", "damage_type": "piercing", "properties": ["heavy", "reach", "two_handed"], "mastery": "Topple"},
    "longsword": {"damage": "1d8", "damage_type": "slashing", "properties": ["versatile"], "versatile": "1d10", "mastery": "Sap"},
    "maul": {"damage": "2d6", "damage_type": "bludgeoning", "properties": ["heavy", "two_handed"], "mastery": "Topple"},
    "morningstar": {"damage": "1d8", "damage_type": "piercing", "properties": [], "mastery": "Sap"},
    "pike": {"damage": "1d10", "damage_type": "piercing", "properties": ["heavy", "reach", "two_handed"], "mastery": "Push"},
    "rapier": {"damage": "1d8", "damage_type": "piercing", "properties": ["finesse"], "mastery": "Vex"},
    "scimitar": {"damage": "1d6", "damage_type": "slashing", "properties": ["finesse", "light"], "mastery": "Nick"},
    "shortsword": {"damage": "1d6", "damage_type": "piercing", "properties": ["finesse", "light"], "mastery": "Vex"},
    "trident": {"damage": "1d8", "damage_type": "piercing", "properties": ["thrown", "versatile"], "thrown_ft": [20, 60], "versatile": "1d10", "mastery": "Topple"},
    "warhammer": {"damage": "1d8", "damage_type": "bludgeoning", "properties": ["versatile"], "versatile": "1d10", "mastery": "Push"},
    "war-pick": {"damage": "1d8", "damage_type": "piercing", "properties": ["versatile"], "versatile": "1d10", "mastery": "Sap"},
    "whip": {"damage": "1d4", "damage_type": "slashing", "properties": ["finesse", "reach"], "mastery": "Slow"},
    "blowgun": {"damage": "1", "damage_type": "piercing", "properties": ["ammunition", "loading"], "range_ft": [25, 100], "mastery": "Vex"},
    "hand-crossbow": {"damage": "1d6", "damage_type": "piercing", "properties": ["ammunition", "light", "loading"], "range_ft": [30, 120], "mastery": "Vex"},
    "heavy-crossbow": {"damage": "1d10", "damage_type": "piercing", "properties": ["ammunition", "heavy", "loading", "two_handed"], "range_ft": [100, 400], "mastery": "Push"},
    "longbow": {"damage": "1d8", "damage_type": "piercing", "properties": ["ammunition", "heavy", "two_handed"], "range_ft": [150, 600], "mastery": "Slow"},
    "musket": {"damage": "1d12", "damage_type": "piercing", "properties": ["ammunition", "loading", "two_handed"], "range_ft": [40, 120], "mastery": "Slow"},
    "pistol": {"damage": "1d10", "damage_type": "piercing", "properties": ["ammunition", "loading"], "range_ft": [30, 90], "mastery": "Vex"},
}

BANNED_IN_DISPLAY = (
    "stirge",
    "skeleton",
    "ankheg",
    "ettercap",
    "dretch",
    "quasit",
    "grimlock",
    "sahuagin",
    "mephit",
    "ettin",
    "manticore",
    "cockatrice",
    "pseudodragon",
    "hippogriff",
    "worg",
    "gnoll",
    "bugbear",
    "hobgoblin",
    "dryad",
    "satyr",
    "magmin",
    "gelatinous",
    "owlbear",
    "rust monster",
    "black pudding",
    "axe beak",
    "blink dog",
    "death dog",
    "phase spider",
    "gray ooze",
)

ATTACK_ROLL = re.compile(
    r"(Melee or Ranged|Melee|Ranged) Attack Roll:\s*\+"
    r"(\d+)"
    r"(?:\s*\(([^)]*)\))?"
    r"\s*,\s*"
    r"(?:reach\s+(\d+)\s*(?:feet|ft\.?))?"
    r"(?:\s*or\s*)?"
    r"(?:range\s+(\d+)(?:\s*/\s*(\d+))?\s*(?:feet|ft\.?))?",
    re.I,
)
HIT_DAMAGE = re.compile(
    r"Hit:\s*(?:(\d+)\s*)?\(([^)]+)\)\s+([A-Za-z]+)\s+damage",
    re.I,
)
PLUS_DAMAGE = re.compile(
    r"plus\s+(?:(\d+)\s*)?\(([^)]+)\)\s+([A-Za-z]+)\s+damage",
    re.I,
)
SAVE = re.compile(
    r"(Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma)"
    r" Saving Throw:\s*DC\s+(\d+)",
    re.I,
)
FAIL_DAMAGE = re.compile(
    r"Failure:\s*(?:(\d+)\s*)?\(([^)]+)\)\s+([A-Za-z]+)\s+damage",
    re.I,
)
RECHARGE = re.compile(r"\(Recharge\s+([^)]+)\)", re.I)
PER_DAY = re.compile(r"\((\d+)/Day\)", re.I)
NUMBER_WORD = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, data) -> None:
    path.write_text(
        json.dumps(data, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def dice_of(raw: str) -> str:
    return re.sub(r"\s+", "", raw)


def damage_obj(dice: str, dtype: str, avg: str | None) -> dict:
    return {
        "dice": dice_of(dice),
        "type": dtype.lower(),
        "average": int(avg) if avg else None,
    }


def parse_action(name: str, text: str, slot: str) -> dict:
    entry: dict = {
        "name": name,
        "slot": slot,
        "kind": "special",
        "parsed": False,
        "raw": text,
    }
    roll = ATTACK_ROLL.search(text)
    if roll:
        label = roll.group(1).lower()
        entry["kind"] = "melee_or_ranged" if "or" in label else ("melee" if label == "melee" else "ranged")
        entry["to_hit"] = int(roll.group(2))
        if roll.group(3):
            entry["attack_note"] = roll.group(3)
        if roll.group(4):
            entry["reach_ft"] = int(roll.group(4))
        if roll.group(5):
            far = int(roll.group(6) or roll.group(5))
            entry["range_ft"] = [int(roll.group(5)), far]
        entry["parsed"] = True
    hits = [damage_obj(m.group(2), m.group(3), m.group(1)) for m in HIT_DAMAGE.finditer(text)]
    pluses = [damage_obj(m.group(2), m.group(3), m.group(1)) for m in PLUS_DAMAGE.finditer(text)]
    if hits:
        entry["damage"] = hits[0]
        extra = hits[1:] + pluses
        if extra:
            entry["extra_damage"] = extra
    elif pluses:
        entry["extra_damage"] = pluses
    save = SAVE.search(text)
    if save:
        save_obj = {"ability": save.group(1).title(), "dc": int(save.group(2))}
        if "half damage" in text.lower():
            save_obj["success"] = "half"
        if roll:
            entry["on_hit_save"] = save_obj
        else:
            entry["kind"] = "save"
            entry["save"] = save_obj
            entry["parsed"] = True
            fail = FAIL_DAMAGE.search(text)
            if fail and "damage" not in entry:
                entry["damage"] = damage_obj(fail.group(2), fail.group(3), fail.group(1))
    if name.lower().startswith("multiattack"):
        entry["kind"] = "multiattack"
        entry["parsed"] = True
        counted = re.search(r"makes (\w+) (.+?) attacks", text, re.I)
        if counted:
            word = counted.group(1).lower()
            entry["count"] = NUMBER_WORD.get(word)
            entry["uses"] = [counted.group(2).strip()]
        else:
            using = re.search(r"using ([^.]+)", text, re.I)
            if using:
                parts = re.split(r",| and ", using.group(1))
                entry["uses"] = [
                    p.strip()
                    for p in parts
                    if p.strip() and "combination" not in p.lower()
                ]
    if "spellcasting" in name.lower() or name.lower().startswith("divine aid"):
        entry["kind"] = "spellcasting"
        entry["parsed"] = True
        at_will = re.search(r"At Will:\s*([^.\n]+)", text)
        if at_will:
            entry["at_will"] = [s.strip() for s in at_will.group(1).split(",") if s.strip()]
        leveled = re.findall(r"(\d)/Day[^:]*:\s*([^.\n]+)", text)
        if leveled:
            entry["per_day_spells"] = [
                {"uses": int(n), "spells": [s.strip() for s in spells.split(",") if s.strip()]}
                for n, spells in leveled
            ]
    recharge = RECHARGE.search(name)
    if recharge:
        entry["recharge"] = recharge.group(1).replace("–", "-")
    per_day = PER_DAY.search(name)
    if per_day:
        entry["per_day"] = int(per_day.group(1))
    if not entry["parsed"]:
        classify_special(entry)
    if not entry["parsed"]:
        entry["needs_review"] = True
    return entry


def classify_special(entry: dict) -> None:
    """Tag a non-attack line so local code can switch on it. The raw sentence stays."""
    text = entry["raw"]
    low = text.lower()
    name = entry["name"].lower()
    if low.startswith("trigger:"):
        entry["kind"] = "reaction"
        entry["parsed"] = True
        parts = re.split(r"Response:\s*", text, maxsplit=1, flags=re.I)
        entry["trigger"] = parts[0].replace("Trigger:", "").strip(" .")
        if len(parts) > 1:
            entry["response"] = parts[1].strip()
        if "adds 2 to its ac" in low:
            entry["ac_bonus"] = 2
        return
    if "casts " in low:
        entry["kind"] = "spell"
        entry["parsed"] = True
        spell = re.search(r"casts (?:the )?([A-Za-z][A-Za-z' -]+?)(?: spell|,)", text)
        if spell:
            entry["spell"] = spell.group(1).strip()
        dc = re.search(r"DC\s+(\d+)", text)
        if dc:
            entry["save_dc"] = int(dc.group(1))
        ability = re.search(r"using ([A-Za-z]+) as the spellcasting", text)
        if ability:
            entry["ability"] = ability.group(1).lower()
        return
    if "disengage or hide" in low:
        entry["kind"] = "bonus"
        entry["options"] = ["disengage", "hide"]
        entry["parsed"] = True
        return
    if "takes the hide action" in low:
        entry["kind"] = "bonus"
        entry["options"] = ["hide"]
        entry["parsed"] = True
        if "dim light" in low:
            entry["requires"] = "dim light or darkness"
        return
    if "teleports" in low:
        entry["kind"] = "teleport"
        entry["parsed"] = True
        distance = re.search(r"(\d+) feet", low)
        if distance:
            entry["distance_ft"] = int(distance.group(1))
        return
    if "advantage on saving throws against spells" in low:
        entry["kind"] = "trait"
        entry["effect"] = "advantage_on_spell_saves"
        entry["parsed"] = True
        return
    if "0 hit points" in low and "saving throw" in low:
        entry["kind"] = "trait"
        entry["effect"] = "drop_to_1_on_save"
        entry["parsed"] = True
        return
    if "swallows" in low or name == "swallow":
        entry["kind"] = "swallow"
        entry["parsed"] = True
        acid = re.search(r"(\d+)\s*\(([^)]+)\)\s+Acid", text)
        if acid:
            entry["damage"] = damage_obj(acid.group(2), "acid", acid.group(1))
        return
    if "bloodied" in low and "half its speed" in low:
        entry["kind"] = "bonus"
        entry["effect"] = "rampage"
        entry["parsed"] = True
        return
    if "pull" in low and "restrained" in low:
        entry["kind"] = "bonus"
        entry["effect"] = "pull_restrained"
        entry["parsed"] = True
        return
    if "sets itself ablaze" in low or "sheds bright light" in low:
        entry["kind"] = "bonus"
        entry["effect"] = "light_toggle"
        entry["parsed"] = True
        return
    if "shape-shifts" in low or "shape-shift" in name:
        entry["kind"] = "shapechange"
        entry["parsed"] = True
        return
    if "destroys a 1-foot" in low or name.startswith("destroy metal"):
        entry["kind"] = "object"
        entry["effect"] = "destroy_metal_cube"
        entry["parsed"] = True
        return
    if "swims up to" in low:
        entry["kind"] = "bonus"
        entry["effect"] = "swim_toward_enemy"
        entry["parsed"] = True
        return
    if "fills its entire space" in low:
        entry["kind"] = "trait"
        entry["effect"] = "fills_space"
        entry["parsed"] = True
        return
    if "emits a shriek" in low or name == "shriek":
        entry["kind"] = "reaction"
        entry["effect"] = "shriek"
        entry["parsed"] = True
        return


def quoted_tagline(nameplate: str) -> str:
    match = re.search(r'"([^"]+)"', nameplate)
    if match:
        return match.group(1)
    match = re.search(r"“([^”]+)”", nameplate)
    return match.group(1) if match else ""


def engine_line(attack: dict) -> str:
    if attack["kind"] == "multiattack":
        uses = ", ".join(attack.get("uses") or [])
        count = attack.get("count")
        if count and uses:
            return f"Multiattack: {count} x {uses}"
        return "Multiattack: " + (uses or attack["raw"])
    if attack["kind"] == "spellcasting":
        return "Spellcasting: spend tracked_uses. At-will does not spend."
    bits = [attack["name"]]
    if attack["kind"] in ("melee", "ranged"):
        bits.append(attack["kind"])
        if "to_hit" in attack:
            bits.append(f"+{attack['to_hit']}")
        if "reach_ft" in attack:
            bits.append(f"reach {attack['reach_ft']} ft")
        if "range_ft" in attack:
            near, far = attack["range_ft"]
            bits.append(f"range {near}/{far} ft")
    if attack["kind"] == "save" and "save" in attack:
        bits.append(f"{attack['save']['ability']} DC {attack['save']['dc']}")
    if "damage" in attack:
        dmg = attack["damage"]
        bits.append(f"{dmg['dice']} {dmg['type']}")
    for extra in attack.get("extra_damage") or []:
        bits.append(f"plus {extra['dice']} {extra['type']}")
    if "recharge" in attack:
        bits.append(f"recharge {attack['recharge']}")
    return ", ".join(bits)


def apply_monsters() -> list[str]:
    names = load(LOCAL / "monster-names.json")["names"]
    catalog = load(PACK / "monsters" / "catalog.json")
    problems = []
    by_id = {card["id"]: card for card in catalog["cards"]}
    if set(names) != set(by_id):
        missing = sorted(set(by_id) - set(names))
        extra = sorted(set(names) - set(by_id))
        raise SystemExit(f"name map mismatch missing={missing} extra={extra}")
    old_to_new = []
    for card in catalog["cards"]:
        spec = names[card["id"]]
        old = card["display_name"]
        new = spec["display_name"]
        previous = card.get("previous_display_name") or old
        if old != new:
            old_to_new.append((old, new, card["id"], spec["picture"]))
        tagline = spec.get("tagline") or quoted_tagline(card["nameplate"])
        level = card["nameplate_level"]
        if card["role"] == "boss":
            nameplate = f'{new}. Level {level}. Boss. "{tagline}"'
        else:
            nameplate = f'{new}. Level {level}. "{tagline}"'
        attacks = []
        for slot in ("actions", "bonus_actions", "reactions"):
            for action in card["stat_block"].get(slot) or []:
                attacks.append(parse_action(action["name"], action["text"], slot))
        riders = []
        for trait in card["stat_block"].get("traits") or []:
            if "Saving Throw" in trait["text"] or "saving throw" in trait["text"]:
                riders.append(parse_action(trait["name"], trait["text"], "trait"))
        unparsed = [a["name"] for a in attacks + riders if a.get("needs_review")]
        if unparsed:
            problems.append(f"{card['id']} unparsed: {', '.join(unparsed)}")
        card["previous_display_name"] = previous
        card["display_name"] = new
        card["nameplate"] = nameplate
        card["picture"] = spec["picture"]
        if spec.get("lore_floor_name"):
            card["lore_floor_name"] = spec["lore_floor_name"]
            card["lore_floor_note"] = (
                "Lore's Floor 1 draft name for this body. The live Day page wins if it uses that name."
            )
        card["schema"] = "cursor-dcc-cards/monster/0.3.0"
        card["system_line"] = card["system_line"].replace(old, new)
        card["gm_line"] = card["gm_line"].replace(old, new)
        card["state_hooks"]["display"] = new
        card["local"] = {
            "schema": "cursor-dcc-cards/local-monster/0.3.0",
            "resolves_in": "code",
            "picture": spec["picture"],
            "attacks": attacks,
            "riders": riders,
            "tracked_uses": card.get("tracked_uses") or [],
            "note": "Numbers are the SRD block already on this card. The engine rolls these fields. It does not ask a model what the dice were.",
        }
        low = new.lower()
        for banned in BANNED_IN_DISPLAY:
            if banned in low:
                problems.append(f"{card['id']} display still says {banned}")
    catalog["schema"] = "cursor-dcc-cards/0.3.0"
    catalog["updated"] = "2026-10-09"
    catalog["naming"] = "Picture names. srd_name stays the mechanical key. See local/monster-names.json."
    dump(PACK / "monsters" / "catalog.json", catalog)
    for floor, filename in ((1, "f01.json"), (2, "f02.json"), (3, "f03.json")):
        subset = [c for c in catalog["cards"] if c["floor"] == floor]
        dump(
            PACK / "monsters" / filename,
            {
                "floor": floor,
                "count": len(subset),
                "schema": "cursor-dcc-cards/0.3.0",
                "cards": subset,
            },
        )
    rewrite_monster_book(old_to_new, by_id)
    return problems


def rewrite_monster_book(old_to_new, by_id) -> None:
    book = (PACK / "monsters" / "monster-book.md").read_text(encoding="utf-8")
    book = book.replace(
        "Owner: Cursor (R&D) | Status: draft | Version: 0.2.0 | Updated: 2026-10-09",
        "Owner: Cursor (R&D) | Status: draft | Version: 0.3.0 | Updated: 2026-10-09",
    )
    if "Names are pictures." not in book:
        book = book.replace(
            "Nameplate level is CR rounded up, minimum 1 (core §8.4).",
            "Names are pictures. A Crawler should know what they are looking at without a Monster Manual. The SRD name stays in the table for the math.\n\nNameplate level is CR rounded up, minimum 1 (core §8.4).",
        )
    for old, new, _card_id, _picture in sorted(old_to_new, key=lambda row: len(row[0]), reverse=True):
        book = book.replace(old, new)
    for card_id, card in by_id.items():
        attacks = card["local"]["attacks"]
        summary = "; ".join(engine_line(a) for a in attacks) or "No attack line. It does not swing."
        picture = card["picture"]
        needle = f"`{card_id}`"
        lines = book.splitlines()
        for index, line in enumerate(lines):
            if not line.startswith(needle):
                continue
            following = lines[index + 1 : index + 8]
            if any(item.startswith("**Picture.**") for item in following):
                pic_at = next(i for i, item in enumerate(following) if item.startswith("**Picture.**"))
                eng_at = next(i for i, item in enumerate(following) if item.startswith("**Engine.**"))
                lines[index + 1 + pic_at] = f"**Picture.** {picture}"
                lines[index + 1 + eng_at] = f"**Engine.** {summary}"
            else:
                lines.insert(index + 1, "")
                lines.insert(index + 2, f"**Picture.** {picture}")
                lines.insert(index + 3, "")
                lines.insert(index + 4, f"**Engine.** {summary}")
            break
        book = "\n".join(lines) + ("\n" if book.endswith("\n") else "")
    (PACK / "monsters" / "monster-book.md").write_text(book, encoding="utf-8")


def chargen_by_srd() -> dict:
    data = load(CHARGEN)
    found = {}

    def walk(node) -> None:
        if isinstance(node, dict):
            if "srd_id" in node and "mechanics" in node:
                found[node["srd_id"]] = node
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(data.get("items", {}))
    return found


def parse_item_mechanics(text: str) -> dict | None:
    if not text or text.lower().startswith("use the srd"):
        return None
    weapon = re.match(
        r"(\d+d\d+(?:\s*\+\s*\d+)?)\s+([A-Za-z]+)(.*)",
        text.strip(),
        re.I,
    )
    if weapon:
        rest = weapon.group(3)
        thrown = re.search(r"Thrown \((\d+)/(\d+)\)", rest, re.I)
        ammo = re.search(r"Ammunition \((\d+)/(\d+)\)", rest, re.I)
        versatile = re.search(r"Versatile \(([^)]+)\)", rest, re.I)
        mastery = re.search(r"Mastery:\s*([A-Za-z]+)", text)
        props = []
        for prop in (
            "Finesse",
            "Light",
            "Heavy",
            "Two-Handed",
            "Loading",
            "Reach",
            "Thrown",
            "Ammunition",
            "Versatile",
        ):
            if re.search(rf"\b{prop}\b", rest, re.I):
                props.append(prop.lower().replace("-", "_").replace(" ", "_"))
        local = {
            "playable": True,
            "kind": "weapon",
            "damage": dice_of(weapon.group(1)),
            "damage_type": weapon.group(2).lower(),
            "properties": props,
            "mastery": mastery.group(1) if mastery else None,
            "source": "tables/chargen-5e.json",
        }
        if thrown:
            local["thrown_ft"] = [int(thrown.group(1)), int(thrown.group(2))]
        if ammo:
            local["range_ft"] = [int(ammo.group(1)), int(ammo.group(2))]
        if versatile:
            local["versatile"] = dice_of(versatile.group(1))
        return local
    plus_ac = re.search(r"\+\s*(\d+)\s*AC", text, re.I)
    if plus_ac:
        return {
            "playable": True,
            "kind": "shield",
            "ac_bonus": int(plus_ac.group(1)),
            "text": text,
            "source": "tables/chargen-5e.json",
        }
    if re.search(r"no AC", text, re.I):
        return {
            "playable": True,
            "kind": "clothing",
            "ac_bonus": 0,
            "text": text,
            "source": "tables/chargen-5e.json",
        }
    armor = re.search(
        r"AC\s+(\d+|[\+\-]\d+)(?:\s*\+\s*Dex(?:\s*\(max\s*(\d+)\))?)?",
        text,
        re.I,
    )
    if armor or "armor" in text.lower() or text.strip().upper().startswith("AC"):
        local = {
            "playable": True,
            "kind": "armor",
            "source": "tables/chargen-5e.json",
            "text": text,
        }
        if armor:
            token = armor.group(1)
            if token.startswith("+") or token.startswith("-"):
                local["ac_bonus"] = int(token)
            else:
                local["ac_base"] = int(token)
            if "Dex" in text:
                local["dex"] = f"max {armor.group(2)}" if armor.group(2) else "full"
        if re.search(r"stealth disadvantage", text, re.I):
            local["stealth"] = "disadvantage"
        for weight in ("Light", "Medium", "Heavy"):
            if re.search(rf"\b{weight}\b", text):
                local["weight_class"] = weight.lower()
        if re.search(r"shield", text, re.I) and "ac_base" not in local:
            local["kind"] = "shield"
        return local
    return {
        "playable": False,
        "kind": "gear",
        "text": text,
        "source": "tables/chargen-5e.json",
        "note": "Filed text has no attack or AC line. The engine does not invent one.",
    }


def local_sentence(local: dict) -> str:
    source = local.get("source") or "the filed table"
    if not local or not local.get("playable"):
        if local and local.get("text"):
            return f"Local. {local['text']} Source: {source}. Not a confirmed roll, so the engine will not invent a number."
        return "Local. No attack or AC line is filed for this srd_id. The engine will not invent damage, AC, or weight."
    if local["kind"] == "weapon":
        props = ", ".join(local.get("properties") or [])
        extra = []
        if local.get("thrown_ft"):
            extra.append(f"thrown {local['thrown_ft'][0]}/{local['thrown_ft'][1]}")
        if local.get("range_ft"):
            extra.append(f"ammo {local['range_ft'][0]}/{local['range_ft'][1]}")
        if local.get("versatile"):
            extra.append(f"versatile {local['versatile']}")
        if local.get("mastery"):
            extra.append(f"mastery {local['mastery']}")
        tail = ", ".join(bit for bit in [props, *extra] if bit)
        return (
            f"Local. {local['damage']} {local['damage_type']}"
            + (f". {tail}." if tail else ".")
            + f" Source: {source}. Not a new number."
        )
    if local["kind"] in ("armor", "shield", "clothing"):
        return f"Local. {local.get('text', '')} Source: {source}. Not a new number."
    return f"Local. {local.get('text', '')}"


def apply_items() -> None:
    punches = load(LOCAL / "item-name-punches.json")["by_old_display_name"]
    catalog = load(PACK / "items" / "catalog.json")
    filed = chargen_by_srd()
    renamed = []
    for card in catalog["cards"]:
        lore = card.get("lore_display_name") or card["display_name"]
        new = punches.get(lore, lore)
        card["lore_display_name"] = lore
        old = lore
        card["display_name"] = new
        card["combined_label"] = f"{new} ({card['srd_name']})"
        card["schema"] = "cursor-dcc-cards/item/0.3.0"
        card["picture"] = f"In your hand: {new}. {card.get('snark', '').strip()}"
        filed_row = filed.get(card["srd_id"])
        mechanics_text = filed_row.get("mechanics") if filed_row else None
        if card["srd_id"] in SRD_WEAPONS:
            local = {
                "playable": True,
                "kind": "weapon",
                "source": "srd/srd.txt#Weapons",
                **SRD_WEAPONS[card["srd_id"]],
            }
        else:
            local = parse_item_mechanics(mechanics_text) if mechanics_text else None
        own = card.get("mechanics") or ""
        if own and not own.lower().startswith("use the srd"):
            local = {
                "playable": False,
                "kind": card.get("category") or "gear",
                "text": own,
                "note": "The card already has rules text. It does not include a confirmed damage or heal number, so the engine will not invent one.",
                "source": "card.mechanics",
            }
        elif local is None:
            local = {
                "playable": False,
                "kind": card.get("category") or "gear",
                "note": "No mechanic string is filed in tables/chargen-5e.json for this srd_id. The engine will not invent damage, AC, or weight.",
                "source": "tables/chargen-5e.json",
            }
        local["lore_display_name"] = old
        local["display_name"] = new
        card["local"] = local
        card["state_hooks"]["display"] = card["combined_label"]
        card["state_hooks"]["live_reskin_name"] = old
        if old != new:
            renamed.append((old, new, card["id"]))
    catalog["schema"] = "cursor-dcc-cards/items/0.3.0"
    catalog["updated"] = "2026-10-09"
    catalog["naming"] = (
        "Lore's reskin is lore_display_name. display_name is the local-engine name. "
        "Flat names were punched up in local/item-name-punches.json. Prices are still the filed list prices."
    )
    dump(PACK / "items" / "catalog.json", catalog)
    rewrite_gear_book(renamed, {c["id"]: c for c in catalog["cards"]})
    write_item_audit(renamed, catalog)


def rewrite_gear_book(renamed, by_id) -> None:
    book = (PACK / "items" / "gear-book.md").read_text(encoding="utf-8")
    book = book.replace(
        "Owner: Cursor (R&D) | Status: draft | Version: 0.2.0 | Updated: 2026-10-09",
        "Owner: Cursor (R&D) | Status: draft | Version: 0.3.0 | Updated: 2026-10-09",
    )
    for old, new, _card_id in sorted(renamed, key=lambda row: len(row[0]), reverse=True):
        book = book.replace(old, new)
    parts = book.split("\n### ")
    rebuilt = [parts[0]]
    for part in parts[1:]:
        match = re.search(r"`(cdr-gear-[^`]+)`", part)
        if not match:
            rebuilt.append(part)
            continue
        card = by_id.get(match.group(1))
        sentence = local_sentence(card["local"]) if card else ""
        old_sentence = "Use the SRD 5.2 entry. This card does not restate damage, AC, or weight."
        if sentence and old_sentence in part:
            part = part.replace(old_sentence, sentence, 1)
        elif sentence and "Local. " in part:
            part = re.sub(r"Local\. .*", sentence, part, count=1)
        elif sentence and "\nSnark. " in part:
            snark_at = part.find("\nSnark. ")
            end = part.find("\n\n", snark_at)
            if end != -1:
                part = part[:end] + "\n\n" + sentence + part[end:]
        rebuilt.append(part)
    (PACK / "items" / "gear-book.md").write_text("\n### ".join(rebuilt), encoding="utf-8")


def write_item_audit(renamed, catalog) -> None:
    lines = [
        "# Item name audit",
        "Owner: Cursor (R&D) | Status: draft | Version: 0.3.0 | Updated: 2026-10-09",
        "Summary: Which gear names changed, and which Lore names were already a picture.",
        "",
        "Lore's filed name stays on `lore_display_name`. The live reskin table was not edited.",
        "A future local engine shows `display_name`. Prices were not changed.",
        "",
        "## Punched up",
        "",
        "| Card | Was | Now |",
        "|---|---|---|",
    ]
    for old, new, card_id in renamed:
        lines.append(f"| `{card_id}` | {old} | {new} |")
    kept = [c for c in catalog["cards"] if c["lore_display_name"] == c["display_name"]]
    playable = sum(1 for c in catalog["cards"] if c["local"].get("playable"))
    lines += [
        "",
        f"Kept Lore's name on {len(kept)} cards. Those names already show the object.",
        f"Attack or AC lines are on {playable} cards. Weapons cite `srd/srd.txt`. Armor and shields cite `tables/chargen-5e.json`.",
        "Gear with no filed attack or AC line is marked `local.playable` false. The engine must not invent a number for those.",
        "",
    ]
    (LOCAL / "item-name-audit.md").write_text("\n".join(lines), encoding="utf-8")


def write_monster_audit() -> None:
    catalog = load(PACK / "monsters" / "catalog.json")
    lines = [
        "# Monster name audit",
        "Owner: Cursor (R&D) | Status: draft | Version: 0.3.0 | Updated: 2026-10-09",
        "Summary: Every Floor 1–3 monster card, old name to picture name.",
        "",
        "The SRD name is still on the card. The name a Crawler hears is the picture.",
        "Lore's Floor 1 draft name is listed when this body is the same one the Day pages use.",
        "Dean Thudd is not in this table. Adjunct Smash is a different giant.",
        "",
        "| ID | Was | Now | You are looking at | SRD |",
        "|---|---|---|---|---|",
    ]
    for card in catalog["cards"]:
        picture = card["picture"].replace("|", "/")
        lines.append(
            f"| `{card['id']}` | {card['previous_display_name']} | {card['display_name']} | {picture} | {card['srd_name']} |"
        )
    lines.append("")
    (LOCAL / "monster-name-audit.md").write_text("\n".join(lines), encoding="utf-8")


def stamp_loot_boxes() -> None:
    path = PACK / "items" / "loot-boxes.json"
    data = load(path)
    for key in ("deck_cards", "rules_40"):
        for card in data.get(key) or []:
            uses = card.get("tracked_uses") or card.get("uses")
            card["local"] = {
                "schema": "cursor-dcc-cards/local-loot/0.3.0",
                "playable": bool(card.get("mechanics")),
                "display_name": card.get("display_name"),
                "action_cost": card.get("action_cost"),
                "effect": card.get("mechanics"),
                "uses": uses,
                "note": "Copied from the filed deck or the rules/40 row already on this card. Not a new credit, not a new effect.",
            }
    data["schema"] = "cursor-dcc-cards/loot-boxes/0.3.0"
    data["updated"] = "2026-10-09"
    dump(path, data)


def check_srd_weapons() -> list[str]:
    if not SRD_TXT.exists():
        return ["srd/srd.txt missing; weapon numbers were not rechecked"]
    text = SRD_TXT.read_text(encoding="utf-8", errors="replace")
    start = text.find("Simple Melee Weapons")
    end = text.find("The Armor table", start)
    region = text[start:end if end > start else start + 8000]
    problems = []
    catalog = load(PACK / "items" / "catalog.json")
    by_id = {c["srd_id"]: c["srd_name"] for c in catalog["cards"]}
    for srd_id, row in SRD_WEAPONS.items():
        name = by_id.get(srd_id, srd_id)
        hit = None
        for line in region.splitlines():
            if name in line:
                hit = line
                break
        if hit is None:
            problems.append(f"srd table missing {name}")
            continue
        if row["damage"] not in hit:
            problems.append(f"{name} damage {row['damage']} not on {hit.strip()}")
    return problems


def check() -> int:
    catalog = load(PACK / "monsters" / "catalog.json")
    items = load(PACK / "items" / "catalog.json")
    problems = []
    ids = [c["id"] for c in catalog["cards"]]
    if len(ids) != 72 or len(set(ids)) != 72:
        problems.append(f"monster count {len(ids)}")
    if len(items["cards"]) != 191:
        problems.append(f"item count {len(items['cards'])}")
    for card in catalog["cards"]:
        if "picture" not in card or "local" not in card:
            problems.append(f"{card['id']} missing picture or local")
        if card["display_name"] == card["srd_name"]:
            problems.append(f"{card['id']} display equals srd name")
        low = card["display_name"].lower()
        for banned in BANNED_IN_DISPLAY:
            if banned in low:
                problems.append(f"{card['id']} banned word {banned}")
        for attack in card["local"]["attacks"]:
            if attack.get("needs_review"):
                problems.append(f"{card['id']} unparsed {attack['name']}")
    for card in items["cards"]:
        if "local" not in card or "picture" not in card or "lore_display_name" not in card:
            problems.append(f"{card['id']} missing local parse")
    for floor, filename in ((1, "f01.json"), (2, "f02.json"), (3, "f03.json")):
        subset = load(PACK / "monsters" / filename)
        if subset["count"] != len(subset["cards"]):
            problems.append(f"{filename} count mismatch")
        if any(c["floor"] != floor for c in subset["cards"]):
            problems.append(f"{filename} floor mismatch")
    problems.extend(check_srd_weapons())
    if problems:
        print("\n".join(problems))
        return 1
    playable = sum(1 for c in items["cards"] if c["local"].get("playable"))
    print(f"ok monsters=72 items=191 playable_gear={playable}")
    return 0


def main() -> int:
    if "--check" in sys.argv:
        return check()
    problems = apply_monsters()
    apply_items()
    write_monster_audit()
    stamp_loot_boxes()
    code = check()
    if problems:
        print("REVIEW")
        print("\n".join(problems))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
