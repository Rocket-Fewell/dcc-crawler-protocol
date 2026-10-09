#!/usr/bin/env python3
"""Build Floor 1 room stubs for the local engine.

Reads floors/f01/day-0N.json and writes reference copies under
local/rooms/f01/. Does not edit floors/. The Day page wins if they disagree.
Spoken names stay the live names (Dean Thudd, Ceiling Tick, Usher).
Stat math points at a picture card in monsters/catalog.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "rooms" / "f01"

# Same SRD body. The room's spoken_name is what the table hears.
STAT_CARD = {
    "giant-rat": "f01-m-01",
    "stirge": "f01-m-02",
    "goblin-minion": "f01-m-03",
    "goblin-warrior": "f01-m-10",
    "skeleton": "f01-m-09",
    "animated-flying-sword": "f01-u-02",
    "animated-armor": "f01-e-01",
    "bugbear-warrior": "f01-e-02",
    "ogre": "f01-b-02",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def first_sentence(text: str, limit: int = 220) -> str:
    text = " ".join(text.split())
    parts = re.split(r"(?<=[.!])\s+", text)
    line = parts[0] if parts else text
    if len(line) < 24 and len(parts) > 1:
        line = f"{parts[0]} {parts[1]}"
    if len(line) > limit:
        line = line[: limit - 1].rstrip() + "…"
    return line


def zone_code(zone: str | None) -> str | None:
    match = re.fullmatch(r"z(\d+)", (zone or "").lower())
    if not match:
        return None
    return f"Z{int(match.group(1))}"


def spoken(our_name: str) -> str:
    # "Dean Thudd, Head of Orientation (Ogre)" -> keep the live name, drop the SRD tail.
    match = re.match(r"^(.*)\s+\([^()]+\)$", our_name.strip())
    return match.group(1) if match else our_name


def counts(enemy: dict) -> dict:
    resolved = ((enemy.get("count_slot") or {}).get("resolved") or {}).get("parts") or []
    for part in resolved:
        values = part.get("values")
        if isinstance(values, dict):
            return {str(key): value for key, value in values.items()}
    return {}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    encounters = []
    for day in range(1, 6):
        data = load(ROOT / "floors" / "f01" / f"day-0{day}.json")
        for enc in data["encounters"]:
            enc = dict(enc)
            enc["_day"] = day
            encounters.append(enc)
    by_day_code = {}
    for enc in encounters:
        code = zone_code(enc.get("zone"))
        if code:
            by_day_code[(enc["_day"], code)] = enc["id"]

    index = []
    for enc in encounters:
        mind = enc.get("map_in_the_mind") or {}
        intro = ((enc.get("voice_lines") or {}).get("system_intro") or {}).get("text") or ""
        exits = []
        for line in mind.get("exits") or []:
            target = None
            codes = re.findall(r"\bZ\s*(\d+)\b", line, flags=re.I)
            if codes:
                target = by_day_code.get((enc["_day"], f"Z{int(codes[0])}"))
                if target == enc["id"]:
                    target = None
            exits.append({"name": line, "to": target, "locked": False, "hidden": False})
        features = []
        for kind, visible in (("cover", True), ("hazard", True)):
            for text in mind.get({"cover": "cover", "hazard": "hazards"}[kind]) or []:
                features.append({"name": text, "kind": kind, "visible": visible})
        enemies = []
        for enemy in enc.get("enemies") or []:
            srd = enemy.get("srd_id")
            enemies.append(
                {
                    "slot": enemy.get("slot"),
                    "srd_id": srd,
                    "spoken_name": spoken(enemy.get("our_name") or ""),
                    "live_name": enemy.get("our_name"),
                    "stat_card": STAT_CARD.get(srd),
                    "counts_by_party_size": counts(enemy),
                    "note": "spoken_name is the live Day-page name. stat_card is the SRD body in this pack. Dean Thudd is not renamed.",
                }
            )
        room = {
            "id": enc["id"],
            "schema": "cursor-dcc-cards/room/0.3.0",
            "status": "R&D",
            "authoritative": False,
            "live_day_page_wins": True,
            "floor": 1,
            "day": enc["_day"],
            "zone": enc.get("zone"),
            "zone_name": enc.get("zone_name"),
            "name": enc.get("name"),
            "kind": enc.get("kind"),
            "source": f"floors/f01/day-0{enc['_day']}.json#{enc['id']}",
            "routes": enc.get("route") or [],
            "read_aloud": intro,
            "narrator_line": first_sentence(intro) if intro else enc.get("name"),
            "layout": mind.get("layout"),
            "exits": exits,
            "features": features,
            "encounter": {
                "id": enc["id"],
                "enemies": enemies,
                "quick_run": enc.get("quick_run"),
            },
            "loot": [
                {"text": hook.get("text"), "when": "see the Day page"}
                for hook in (enc.get("loot_hooks") or [])
                if hook.get("text")
            ],
            "achievement_ids": [
                hook.get("id") for hook in (enc.get("achievement_hooks") or []) if hook.get("id")
            ],
            "narrator_sees": ["name", "narrator_line", "read_aloud", "features"],
            "code_sees": ["layout", "exits", "encounter", "loot", "achievement_ids"],
            "gm_notes": "Strong-model notes stay on the Day page. This stub does not copy if_they_do_something_dumb.",
        }
        path = OUT / f"{enc['id']}.json"
        path.write_text(json.dumps(room, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        index.append(
            {
                "id": enc["id"],
                "day": enc["_day"],
                "zone": enc.get("zone"),
                "name": enc.get("name"),
                "kind": enc.get("kind"),
                "file": f"local/rooms/f01/{enc['id']}.json",
                "stat_cards": [e["stat_card"] for e in enemies if e["stat_card"]],
            }
        )
    summary = {
        "schema": "cursor-dcc-cards/room-index/0.3.0",
        "status": "R&D",
        "authoritative": False,
        "floor": 1,
        "count": len(index),
        "note": "Plugs for a future local engine. floors/f01 day pages win. Nothing here writes sessions or credits.",
        "rooms": index,
    }
    (OUT / "index.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(index)} floor 1 room stubs")


if __name__ == "__main__":
    main()
