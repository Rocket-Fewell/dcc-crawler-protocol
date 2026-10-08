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


def resolve_count(budget, ref, party_size):
    if not ref:
        return None
    node = walk(budget, ref["path"])
    party = node[str(party_size)]
    key = ref.get("key")
    if key is None:
        return party
    if isinstance(party, dict):
        return party[key]
    return party


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


def resolve_room(room, party_size, budget=None):
    budget = budget if budget is not None else load_budget()
    out = json.loads(json.dumps(room))
    resolved = []
    for enc in out.get("encounters") or []:
        row = dict(enc)
        if enc.get("count_ref"):
            row["count"] = resolve_count(budget, enc["count_ref"], party_size)
        if enc.get("cr_ref"):
            row["cr"] = resolve_cr(budget, enc["cr_ref"])
        resolved.append(row)
    out["encounters"] = resolved
    return out
