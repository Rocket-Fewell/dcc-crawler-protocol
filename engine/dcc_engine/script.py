"""Read the filed voice lines. This module does not rewrite a day page."""

import json
import re
from pathlib import Path

from dcc_engine.cards import load_room, monster_catalog
from dcc_engine.paths import REPO_ROOT

FLOORS = REPO_ROOT / "floors"
VOICES = REPO_ROOT / "tables" / "npc-voices.json"
FLOOR3 = Path(__file__).resolve().parents[1] / "campaign" / "floor3.json"

_QUOTE = re.compile(r"[\"“]([^\"”]+)[\"”]")
_SLOT = re.compile(r"\*([^*]+)\*")
_ENC = re.compile(r"^### (enc-[\w-]+): (.+)$")
_SRD_ROW = re.compile(r"^\| [^|]+ \| `([^`]+)` \| ([^|]+) \| ([^|]*) \|")
_COUNT2 = re.compile(r"2 Crawlers:\s*(\d+)")
_BLOCK = re.compile(r"^>\s*(?:\*\(optional\)\*\s*)?(.*)$")


def npc_names():
    data = json.loads(VOICES.read_text(encoding="utf-8"))
    names = []
    for npc in data.get("npcs") or []:
        if npc.get("name"):
            names.append(npc["name"])
    return names


def _voice(audience, slot):
    slot = (slot or "").lower()
    if audience == "GM-FACING" or "gm color" in slot:
        return "GM"
    if slot.startswith("system") or "floor notice" in slot:
        return "SYSTEM"
    return "GM"


def _line_from_markdown(raw):
    if "GM-ONLY" in raw or "PLAYER-FACING" not in raw and "GM-FACING" not in raw:
        return None
    audience = "GM-FACING" if "GM-FACING" in raw and "PLAYER-FACING" not in raw else "PLAYER-FACING"
    if "[GM-FACING]" in raw and "[PLAYER-FACING]" not in raw:
        audience = "GM-FACING"
    quoted = _QUOTE.search(raw)
    if not quoted:
        return None
    slot = ""
    found = _SLOT.search(raw)
    if found:
        slot = found.group(1).strip()
    when = "open"
    low = slot.lower()
    if "midpoint" in low:
        when = "mid"
    elif "win" in low:
        when = "win"
    return {"when": when, "voice": _voice(audience, slot), "text": quoted.group(1).strip(), "slot": slot}


def _enemies_from_section(body):
    enemies = []
    for raw in body.splitlines():
        found = _SRD_ROW.match(raw.strip())
        if not found:
            continue
        srd, display, count_cell = found.group(1), found.group(2).strip(), found.group(3)
        spoken = display.rsplit(" (", 1)[0].strip() if " (" in display else display
        count = 1
        counted = _COUNT2.search(count_cell)
        if counted:
            count = int(counted.group(1))
        elif "count: 0" in count_cell.lower():
            count = 0
        enemies.append({"srd_id": srd, "spoken_name": spoken, "count": count})
    return enemies


def _set_pieces(body):
    lines = []
    grabbing = False
    for raw in body.splitlines():
        if "Set piece" in raw and "PLAYER-FACING" in raw:
            grabbing = True
            continue
        if not grabbing:
            continue
        if raw.startswith(">"):
            found = _BLOCK.match(raw.strip())
            text = (found.group(1) if found else "").strip()
            if text and not text.startswith("*(optional)*"):
                text = text.removeprefix("*(optional)*").strip()
            if text.startswith("*") and text.endswith("*"):
                continue
            if text:
                lines.append({"when": "open", "voice": "GM", "text": text, "slot": "set piece"})
            continue
        if raw.strip() == "":
            continue
        grabbing = False
    return lines


def _encounters(path, floor):
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?=^### enc-)", text, flags=re.M)
    scenes = []
    preamble = parts[0]
    notices = []
    for raw in preamble.splitlines():
        parsed = _line_from_markdown(raw)
        if not parsed:
            continue
        if "FLOOR NOTICE" in parsed["text"]:
            parsed["voice"] = "SYSTEM"
        notices.append(parsed)
    day = int(path.stem.split("-")[1])
    if notices:
        scenes.append({
            "key": f"f{floor:02d}-d{day:02d}-notice",
            "id": f"d{day:02d}-notice",
            "floor": floor,
            "day": day,
            "title": f"Floor {floor} day {day} notice",
            "kind": "notice",
            "lines": notices,
            "enemies": [],
        })
    for part in parts[1:]:
        first = part.splitlines()[0]
        found = _ENC.match(first.strip())
        if not found:
            continue
        enc_id, title = found.group(1), found.group(2).strip()
        lines = []
        for raw in part.splitlines():
            parsed = _line_from_markdown(raw)
            if parsed:
                lines.append(parsed)
        lines.extend(_set_pieces(part))
        kind = "scene"
        typed = re.search(r"\*\*Type:\*\*\s*([^|\n]+)", part)
        if typed:
            kind = typed.group(1).strip()
        scenes.append({
            "key": f"f{floor}:{enc_id}",
            "id": enc_id,
            "floor": floor,
            "day": day,
            "title": title,
            "kind": kind,
            "lines": lines,
            "enemies": _enemies_from_section(part),
        })
    return scenes


def _srd_cards():
    found = {}
    for card in monster_catalog().values():
        srd = card.get("srd_id")
        if srd and srd not in found:
            found[srd] = card["id"]
    return found


def _attach_cards(scene, srd_cards):
    """Floor 1 room stubs win. Elsewhere, an SRD id on a card is the body."""
    if scene["floor"] == 1 and scene["id"].startswith("enc-"):
        try:
            room = load_room(scene["id"])
        except OSError:
            room = None
        if room:
            scene["room"] = room
            scene["enemies"] = []
            for slot in (room.get("encounter") or {}).get("enemies") or []:
                scene["enemies"].append({
                    "srd_id": slot.get("srd_id") or "",
                    "spoken_name": slot.get("spoken_name") or "",
                    "stat_card": slot.get("stat_card") or "",
                    "counts_by_party_size": slot.get("counts_by_party_size") or {},
                })
            return
    for enemy in scene["enemies"]:
        card = srd_cards.get(enemy.get("srd_id") or "")
        if not card:
            continue
        count = int(enemy.get("count") or 0)
        enemy["stat_card"] = card
        enemy["counts_by_party_size"] = {"2": count, "3": count, "4": count}


def load_floor3():
    data = json.loads(FLOOR3.read_text(encoding="utf-8"))
    scenes = []
    for scene in data["scenes"]:
        scenes.append({
            "key": scene["id"],
            "id": scene["id"],
            "floor": 3,
            "day": scene.get("day") or 1,
            "title": scene["title"],
            "kind": scene.get("kind") or "scene",
            "lines": scene.get("lines") or [],
            "enemies": scene.get("enemies") or [],
            "floor_name": data.get("floor_name") or "Kingdom Continuum",
        })
    return scenes


def load_script():
    """Floor 1 and 2 from the day pages, then the local Floor 3 script."""
    scenes = []
    for floor, folder in ((1, "f01"), (2, "f02")):
        for path in sorted((FLOORS / folder).glob("day-*.md")):
            scenes.extend(_encounters(path, floor))
    srd_cards = _srd_cards()
    for scene in scenes:
        _attach_cards(scene, srd_cards)
    scenes.extend(load_floor3())
    return scenes
