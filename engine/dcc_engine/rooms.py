"""Load room cards, apply a day layer, and resolve budget refs for a party size."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "engine" / "data"
BUDGET = ROOT / "rules" / "70-encounter-budget-5e.json"


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def walk(node, path):
    cur = node
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list) and part.isdigit():
            cur = cur[int(part)]
        else:
            raise KeyError(path)
    return cur


def load_budget(path=None):
    return load_json(path or BUDGET)


# The budget file publishes counts for 2, 3, and 4 Crawlers only.
SUPPORTED_PARTY_SIZES = ("2", "3", "4")


def party_key_for(node, party_size):
    """Pick a budget party-size key. Sizes outside 2, 3, and 4 use the nearest one."""
    key = str(party_size)
    if isinstance(node, dict) and key in node:
        return key, None
    if not isinstance(node, dict):
        raise ValueError("Party size %s is not in the budget." % party_size)
    choices = [k for k in SUPPORTED_PARTY_SIZES if k in node]
    if not choices:
        raise ValueError(
            "Party size %s is not in the budget. Supported sizes are 2, 3, and 4 Crawlers."
            % party_size
        )
    try:
        wanted = int(party_size)
    except (TypeError, ValueError):
        raise ValueError(
            "Party size %s is not in the budget. Supported sizes are 2, 3, and 4 Crawlers."
            % party_size
        )
    nearest = min(choices, key=lambda k: (abs(int(k) - wanted), int(k)))
    note = "Party size %s is not in the budget. Using the %s-Crawler count." % (party_size, nearest)
    return nearest, note


def resolve_count(budget, ref, party_size):
    """Return (count, note). note is set when the party size is not in the budget."""
    if not ref:
        return None, None
    node = walk(budget, ref["path"])
    key, note = party_key_for(node, party_size)
    party = node[key]
    field = ref.get("key")
    if field is None:
        return party, note
    if isinstance(party, dict):
        if field not in party:
            raise ValueError(
                "Party size %s has no %s count in the budget." % (key, field)
            )
        return party[field], note
    return party, note


def resolve_cr(budget, ref):
    if not ref:
        return None
    node = walk(budget, ref["path"])
    key = ref.get("key")
    if isinstance(node, list):
        for row in node:
            if row.get("srd_id") == key:
                return row.get("cr")
        raise KeyError(ref["path"] + " key " + str(key))
    if key and isinstance(node, dict):
        return node[key]
    return node


def room_path(room_id, root=None):
    root = Path(root or DATA)
    return root / "rooms" / "f01" / ("%s.json" % room_id)


def load_room(room_id, day=None, root=None, budget=None):
    root = Path(root or DATA)
    room = load_json(room_path(room_id, root))
    if day is not None:
        layer_path = root / "layers" / "f01" / ("day-%02d.json" % int(day))
        if layer_path.is_file():
            layer = load_json(layer_path)
            patch = layer.get(room_id)
            if patch:
                room = apply_patch(room, patch)
    return room


def apply_patch(room, patch):
    out = json.loads(json.dumps(room))
    for key, val in patch.items():
        if isinstance(val, dict) and isinstance(out.get(key), dict):
            merged = dict(out[key])
            merged.update(val)
            out[key] = merged
        else:
            out[key] = val
    return out


def active_encounters(room):
    """A day layer's day_encounters replace the base list, even when the list is empty."""
    if "day_encounters" in room:
        return list(room.get("day_encounters") or [])
    return list(room.get("encounters") or [])


def resolve_room(room, party_size, budget=None):
    budget = budget if budget is not None else load_budget()
    out = json.loads(json.dumps(room))
    resolved = []
    for enc in active_encounters(out):
        row = dict(enc)
        if enc.get("count_ref"):
            count, note = resolve_count(budget, enc["count_ref"], party_size)
            row["count"] = count
            if note:
                row["party_size_note"] = note
                out["party_size_note"] = note
        if enc.get("cr_ref"):
            row["cr"] = resolve_cr(budget, enc["cr_ref"])
        resolved.append(row)
    out["encounters"] = resolved
    return out
