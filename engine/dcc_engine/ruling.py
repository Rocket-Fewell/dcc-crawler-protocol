"""Strong-model ruling JSON. Code checks the shape, then resolves it.

A ruling is logged on the engine action store, tagged POST-SESSION REVIEW.
This module does not write gm-notes/.
"""

from __future__ import annotations

from dcc_engine.rules import apply_damage, rolltool

RESOLVE_AS = ("attack", "save", "check", "damage", "heal", "condition", "move", "item", "none")


def apply_ruling(ruling, state=None):
    """Validate a ruling. Attack params are returned for the attack resolver."""
    if not isinstance(ruling, dict):
        return {"ok": False, "reason": "ruling was not a JSON object"}
    kind = ruling.get("resolve_as")
    if kind not in RESOLVE_AS:
        return {"ok": False, "reason": "resolve_as is not an action code can run"}
    text = ruling.get("ruling")
    if not isinstance(text, str) or not text.strip():
        return {"ok": False, "reason": "ruling text is missing"}
    params = ruling.get("params")
    if not isinstance(params, dict):
        return {"ok": False, "reason": "params must be an object"}
    log = ruling.get("log")
    if not isinstance(log, str):
        return {"ok": False, "reason": "log is missing"}
    return {
        "ok": True,
        "resolve_as": kind,
        "ruling": text.strip(),
        "params": params,
        "log": log,
        "tag": "POST-SESSION REVIEW",
        "state_present": state is not None,
    }


def _combatant(state, key):
    combatants = (state or {}).get("combatants") or {}
    if key not in combatants:
        return None
    return combatants[key]


def resolve_effect(applied, state):
    """Apply a non-attack ruling. Attack stays with the attack resolver."""
    if not applied.get("ok"):
        return applied
    kind = applied.get("resolve_as")
    if kind in ("attack", "none"):
        return applied
    params = applied.get("params") or {}
    state = state or {}
    if kind in ("save", "check"):
        rng = state.get("rng")
        if rng is None or "dc" not in params:
            return {"ok": False, "reason": "That check needs a DC the card does not have."}
        mod = int(params.get("mod") or 0)
        d20 = int(rolltool.evaluate(rolltool.parse_expression("1d20"), rng)["total"])
        total = d20 + mod
        dc = int(params["dc"])
        return {
            "ok": True,
            "resolve_as": kind,
            "d20": d20,
            "total": total,
            "dc": dc,
            "success": total >= dc,
            "ruling": applied.get("ruling"),
            "tag": "POST-SESSION REVIEW",
        }
    if kind in ("damage", "heal"):
        who = _combatant(state, params.get("target"))
        if who is None or "amount" not in params:
            return {"ok": False, "reason": "That ruling names no target."}
        amount = int(params["amount"])
        if kind == "damage":
            apply_damage(who, amount)
        else:
            who["hp"] = int(who.get("hp") or 0) + amount
            if who.get("max_hp") is not None:
                who["hp"] = min(int(who["max_hp"]), who["hp"])
        return {
            "ok": True,
            "resolve_as": kind,
            "target": who.get("name"),
            "target_hp": who["hp"],
            "amount": amount,
            "ruling": applied.get("ruling"),
            "tag": "POST-SESSION REVIEW",
        }
    if kind == "condition":
        who = _combatant(state, params.get("target"))
        name = params.get("condition")
        if who is None or not name:
            return {"ok": False, "reason": "That ruling names no condition."}
        who.setdefault("conditions", []).append(name)
        return {
            "ok": True,
            "resolve_as": kind,
            "condition": name,
            "target": who.get("name"),
            "ruling": applied.get("ruling"),
            "tag": "POST-SESSION REVIEW",
        }
    if kind == "move":
        return {
            "ok": True,
            "resolve_as": kind,
            "to": params.get("to"),
            "distance_ft": params.get("distance_ft"),
            "hp_changed": False,
            "ruling": applied.get("ruling"),
            "tag": "POST-SESSION REVIEW",
        }
    if kind == "item":
        return {
            "ok": True,
            "resolve_as": kind,
            "item": params.get("item"),
            "action": params.get("action"),
            "hp_changed": False,
            "ruling": applied.get("ruling"),
            "tag": "POST-SESSION REVIEW",
        }
    return {"ok": False, "reason": "resolve_as is not an action code can run"}
