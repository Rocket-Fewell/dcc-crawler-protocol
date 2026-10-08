"""python -m dcc_engine.validate engine/data"""

from __future__ import annotations

import json
import sys
from pathlib import Path

if __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dcc_engine.rooms import load_budget, resolve_cr, resolve_count, walk
from dcc_engine.schema import check_encounter, check_room, check_stat

ROOT = Path(__file__).resolve().parents[2]
VOICES = ROOT / "tables" / "npc-voices.json"


def voice_names():
    data = json.loads(VOICES.read_text(encoding="utf-8"))
    names = set()
    for row in data.get("npcs") or []:
        names.add(row.get("name"))
        for alias in row.get("aliases") or []:
            names.add(alias)
    return names


def budget_ok(ref, budget, party_size=3):
    if not ref:
        return True
    try:
        if ref.get("key") and "creatures" in ref.get("path", ""):
            resolve_cr(budget, ref)
        else:
            resolve_count(budget, ref, party_size)[0]
            if "creatures" not in ref.get("path", ""):
                walk(budget, ref["path"])
        return True
    except (KeyError, TypeError, ValueError):
        return False


def validate_tree(root: Path):
    errs = []
    budget = load_budget()
    names = voice_names()
    rooms_dir = root / "rooms" / "f01"
    if not rooms_dir.is_dir():
        return ["%s missing" % rooms_dir]
    rooms = {}
    for path in sorted(rooms_dir.glob("*.json")):
        room = json.loads(path.read_text(encoding="utf-8"))
        rooms[room.get("id")] = room
        errs.extend(check_room(room, str(path.relative_to(ROOT))))
        for enc in room.get("encounters") or []:
            for ref_name in ("count_ref", "cr_ref"):
                ref = enc.get(ref_name)
                if ref and not budget_ok(ref, budget):
                    errs.append("%s %s does not resolve: %s" % (room.get("id"), ref_name, ref.get("path")))
        for loot in room.get("loot") or []:
            ref = loot.get("dice_ref")
            if ref:
                try:
                    walk(budget, ref)
                except KeyError:
                    errs.append("%s loot dice_ref does not resolve: %s" % (room.get("id"), ref))
        for npc in room.get("npcs") or []:
            if npc.get("voice") not in names:
                errs.append("%s npc voice %r is not in tables/npc-voices.json" % (room.get("id"), npc.get("voice")))
    ids = set(rooms)
    for room in rooms.values():
        for ex in room.get("exits") or []:
            if ex.get("to") not in ids:
                errs.append("%s exit to missing room %s" % (room.get("id"), ex.get("to")))
    # reachability, including hidden exits
    start = "f01-z00"
    if start not in ids:
        errs.append("Intake Hall f01-z00 is missing")
    else:
        seen = set()
        stack = [start]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            for ex in rooms[cur].get("exits") or []:
                dest = ex.get("to")
                if dest in ids and dest not in seen:
                    stack.append(dest)
        for missing in sorted(ids - seen):
            if rooms[missing].get("zone") == "wandering":
                continue
            errs.append("%s is not reachable from the Intake Hall" % missing)
        if "f01-z11" not in seen:
            errs.append("the stairwell f01-z11 is not reachable from the Intake Hall")
    layers = root / "layers" / "f01"
    if layers.is_dir():
        for path in sorted(layers.glob("day-*.json")):
            layer = json.loads(path.read_text(encoding="utf-8"))
            rel = str(path.relative_to(ROOT))
            for room_id, patch in layer.items():
                if not isinstance(patch, dict):
                    errs.append("%s %s patch is not an object" % (rel, room_id))
                    continue
                for i, enc in enumerate(patch.get("day_encounters") or []):
                    errs.extend(check_encounter(enc, "%s %s day_encounter %d" % (rel, room_id, i)))
                    for ref_name in ("count_ref", "cr_ref"):
                        ref = enc.get(ref_name)
                        if ref and not budget_ok(ref, budget):
                            errs.append("%s %s %s does not resolve: %s" % (rel, room_id, ref_name, ref.get("path")))
    stats = root / "stat-blocks"
    if stats.is_dir():
        for path in sorted(stats.glob("*.json")):
            block = json.loads(path.read_text(encoding="utf-8"))
            errs.extend(check_stat(block, str(path.relative_to(ROOT))))
    return errs


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    target = Path(argv[0]) if argv else ROOT / "engine" / "data"
    if not target.is_absolute():
        target = ROOT / target
    errs = validate_tree(target)
    if errs:
        for err in errs:
            print("FAIL " + err)
        print("%d FAIL" % len(errs))
        return 1
    print("PASS 0 errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
