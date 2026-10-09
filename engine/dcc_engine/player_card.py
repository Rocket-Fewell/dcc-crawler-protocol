"""The channel card, computed the same way tools/card_rules.py already computes it.

The Gallery seats a copy. It does not read or write the live sheet while a fight is running.
"""

import json
import re
import sys

from dcc_engine.paths import FIXTURES_DIR, REPO_ROOT

_ATK = re.compile(
    r"^- \*\*(?P<name>.+?)\*\*(?: \([^)]*\))?: (?P<hit>[+-]?\d+) to hit, (?P<rest>.+)$"
)
_DMG = re.compile(
    r"^(?P<dice>\d*d\d+(?:[+-]\d+)?|\d+) (?P<type>[A-Za-z]+)"
    r"(?: \((?P<vers>\d*d\d+(?:[+-]\d+)?|\d+) two-handed\))?"
)
_WITCH = re.compile(
    r"([+-]?\d+) to hit, (\d*d\d+(?:[+-]\d+)?) ([A-Za-z]+)"
)
_TEMP = re.compile(r"(\d+) temp HP")
_SHIELD_AC = re.compile(r"\+(\d+) AC")


def _rules():
    tools = str(REPO_ROOT / "tools")
    if tools not in sys.path:
        sys.path.insert(0, tools)
    import card_rules
    import species_class_reskins

    return card_rules, species_class_reskins


def load_raithen_sheet():
    return json.loads((FIXTURES_DIR / "raithen-copy.json").read_text(encoding="utf-8"))["card"]


def _aliases(name):
    low = name.lower()
    names = {low}
    if "eldritch" in low:
        names.update({"eldritch blast", "blast", "eldritch"})
    if "chill" in low:
        names.update({"chill touch", "chill"})
    if "shocking" in low:
        names.update({"shocking grasp", "shocking", "grasp"})
    if "quarterstaff" in low or "mop" in low:
        names.update({"mop", "quarterstaff", "staff"})
    if "unarmed" in low:
        names.update({"unarmed", "punch"})
    return names


def parse_attack_lines(block):
    """Turn the Attacks block into rolls. The numbers stay the ones card_rules printed."""
    attacks = []
    for line in (block or "").splitlines():
        match = _ATK.match(line.strip())
        if not match:
            continue
        rest = match.group("rest")
        damage_text, _, tail = rest.partition(", ")
        parsed = _DMG.match(damage_text.strip())
        if not parsed:
            continue
        kind = "melee" if tail.lower().startswith(("melee", "touch")) else "ranged"
        attacks.append({
            "name": match.group("name"),
            "to_hit": int(match.group("hit")),
            "damage": parsed.group("dice"),
            "versatile": parsed.group("vers"),
            "type": parsed.group("type").lower(),
            "kind": kind,
            "aliases": sorted(_aliases(match.group("name"))),
        })
    return attacks


def parse_spells(block):
    spells = {}
    for line in (block or "").splitlines():
        if line.startswith("- Witch Bolt"):
            found = _WITCH.search(line)
            if found:
                spells["witch bolt"] = {
                    "name": "Witch Bolt",
                    "to_hit": int(found.group(1)),
                    "damage": found.group(2),
                    "type": found.group(3).lower(),
                    "cost": "action",
                    "slot": True,
                }
        elif line.startswith("- Armor of Agathys"):
            found = _TEMP.search(line)
            if found:
                spells["agathys"] = {
                    "name": "Armor of Agathys",
                    "temp": int(found.group(1)),
                    "cost": "bonus",
                    "slot": True,
                }
        elif line.startswith("- Shield"):
            found = _SHIELD_AC.search(line)
            if found:
                spells["shield"] = {
                    "name": "Shield",
                    "ac": int(found.group(1)),
                    "cost": "reaction",
                }
    return spells


def _section_title(text):
    first = text.splitlines()[0]
    if first.startswith("**"):
        end = first.find("**", 2)
        if end > 2:
            return first[2:end]
    if ":" in first and not first.startswith("-"):
        return first.split(":", 1)[0].strip()
    return "Card"


def card_sections(sheet, conditions, party_short_used=0):
    """Same pieces as the channel card, split so the page can show every block."""
    rules, labels = _rules()
    species = labels.species_label(sheet.get("species") or "")
    klass = labels.class_label(sheet.get("class") or "")
    hp = sheet.get("hp") or {}
    temp = f" (+{hp.get('temp')} temp)" if hp.get("temp") else ""
    abilities = sheet.get("abilities") or {}
    scores = "  ".join(f"{key.upper()} {abilities[key]}" for key in ("str", "dex", "con", "int", "wis", "cha") if key in abilities)
    dice = sheet.get("hit_dice") or {}
    header = [
        f"Credits: {sheet.get('credits', 0)}",
        f"**{sheet.get('name', '').upper()}** - {species} {klass} {sheet.get('level')} ({sheet.get('player', '')})",
        f"HP {hp.get('current')}/{hp.get('max')}{temp}  AC {sheet.get('ac')}  XP {sheet.get('xp', 0)}  Hit Dice {dice.get('current')}/{dice.get('max')}",
        scores,
        "Conditions: " + (", ".join(conditions) or "none"),
    ]
    sections = [{"title": "Crawler", "text": "\n".join(header)}]
    for block in rules.combat_blocks(sheet, {"short_used": party_short_used, "short_max": 4}):
        sections.append({"title": _section_title(block), "text": block})
    cats = (
        ("weapons", "Weapons & focus"),
        ("armor", "Armor & clothing"),
        ("magic", "Magic & special"),
        ("gear", "Gear"),
    )
    for key, title in cats:
        rows = []
        for item in sheet.get("inventory") or []:
            if item.get("category") != key:
                continue
            mechanics = rules.item_mechanics_text(sheet, item, item.get("mechanics") or "")
            qty = f" x{item['qty']}" if (item.get("qty") or 1) > 1 else ""
            rows.append(f"- **{item.get('name')}**{qty}: {mechanics}")
        if rows:
            sections.append({"title": title, "text": f"**{title}**\n" + "\n".join(rows)})
    for label, field in (
        ("Standing Orders", "standing_orders"),
        ("Signature attack", "signature"),
        ("Standing Reaction", "standing_reaction"),
    ):
        if sheet.get(field):
            sections.append({"title": label, "text": f"{label}: {sheet[field]}"})
    names = [a.get("name") for a in sheet.get("achievements") or [] if isinstance(a, dict) and a.get("name")]
    if names:
        sections.append({"title": "Achievements", "text": "**Achievements**\n" + "\n".join("- " + name for name in names)})
    return sections


def render_card(sheet, conditions, party_short_used=0):
    """Plain text in the same order as the channel card. Secrets never get here."""
    return "\n".join(section["text"] for section in card_sections(sheet, conditions, party_short_used))


def sync_card(crawler):
    """Write the in-memory numbers back onto the copy, then rebuild the text."""
    sheet = crawler.get("sheet")
    if not sheet:
        crawler["card_text"] = ""
        crawler["card_sections"] = []
        return crawler
    sheet.setdefault("hp", {})
    sheet["hp"]["current"] = crawler["hp"]
    sheet["hp"]["max"] = crawler["hp_max"]
    sheet["hp"]["temp"] = crawler.get("temp_hp") or 0
    sheet["conditions"] = list(crawler.get("conditions") or [])
    sheet["death_saves"] = {
        "successes": crawler.get("death_success") or 0,
        "fails": crawler.get("death_fail") or 0,
    }
    sections = card_sections(sheet, crawler.get("conditions") or [])
    crawler["card_sections"] = sections
    crawler["card_text"] = "\n".join(section["text"] for section in sections)
    return crawler


def seat_raithen():
    """Memory crawler for the copy. Attacks come off the computed card, not a second table."""
    rules, _labels = _rules()
    sheet = load_raithen_sheet()
    attack_block = rules.attacks_block(sheet)
    spell_block = rules.spellcasting_block(sheet) or ""
    attacks = parse_attack_lines(attack_block)
    header = attack_block.splitlines()[1] if attack_block else ""
    speed = 30
    found = re.search(r"Speed (\d+) ft", header)
    if found:
        speed = int(found.group(1))
    abilities = sheet.get("abilities") or {}
    crawler = {
        "id": "raithen",
        "name": sheet.get("name") or "Raithen",
        "player": sheet.get("player") or "",
        "class_name": sheet.get("class") or "",
        "level": int(sheet.get("level") or 1),
        "hp": int(sheet["hp"]["current"]),
        "hp_max": int(sheet["hp"]["max"]),
        "temp_hp": int(sheet["hp"].get("temp") or 0),
        "ac": int(sheet.get("ac") or 10),
        "ac_bonus": 0,
        "speed_ft": speed,
        "str_mod": (int(abilities.get("str", 10)) - 10) // 2,
        "dex_mod": (int(abilities.get("dex", 10)) - 10) // 2,
        "pb": int((sheet.get("build") or {}).get("proficiency_bonus") or 2),
        "skills": [str(item).lower() for item in (sheet.get("build") or {}).get("skills") or []],
        "attacks": attacks,
        "spells": parse_spells(spell_block),
        "sheet": sheet,
        "movement_left": speed,
        "action": True,
        "bonus": True,
        "reaction": True,
        "object": True,
        "cover": None,
        "hidden": False,
        "dodging": False,
        "disengaged": False,
        "conditions": list(sheet.get("conditions") or []),
        "death_success": 0,
        "death_fail": 0,
        "spent_action": "",
        "card_text": "",
    }
    return sync_card(crawler)


def pick_attack(crawler, text):
    """Match a listed attack. A plain shot uses Eldritch Blast, the ranged cantrip on the card."""
    low = (text or "").lower()
    attacks = crawler.get("attacks") or []
    two_hands = bool(re.search(r"\b(?:two-handed|both hands)\b", low))
    for attack in attacks:
        if any(alias in low for alias in attack.get("aliases") or []):
            return _maybe_versatile(attack, two_hands)
    if re.search(r"\b(?:swing|mop|staff|quarterstaff)\b", low):
        for attack in attacks:
            if "mop" in attack["aliases"] or "quarterstaff" in attack["aliases"]:
                return _maybe_versatile(attack, two_hands)
    for attack in attacks:
        if "eldritch blast" in attack["aliases"]:
            return attack
    return dict(attacks[0]) if attacks else None


def _maybe_versatile(attack, two_hands):
    chosen = dict(attack)
    if two_hands and chosen.get("versatile"):
        chosen["damage"] = chosen["versatile"]
    return chosen


def spell_named(crawler, text):
    low = (text or "").lower()
    spells = crawler.get("spells") or {}
    if "witch bolt" in low and "witch bolt" in spells:
        return "witch bolt"
    if ("armor of agathys" in low or "agathys" in low) and "agathys" in spells:
        return "agathys"
    if re.search(r"\bshield\b", low) and "shield" in spells:
        return "shield"
    return None
