"""Strong-model ruling JSON. Code checks the shape, then resolves it.

A ruling is logged on the engine action store, tagged POST-SESSION REVIEW.
This module does not write gm-notes/.
"""

from __future__ import annotations

from dcc_engine.rules import add_condition, apply_damage, apply_healing, clear_condition, rolltool

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


def _actor(state, key):
    who = _combatant(state, key) if key else None
    if who is not None:
        return who
    who = _combatant(state, "crawler")
    if who is not None:
        return who
    crawler = (state or {}).get("crawler")
    return crawler if isinstance(crawler, dict) else None


def _spend_item(who, item):
    """Remove one matching inventory entry. Returns whether one was spent."""
    if not isinstance(who, dict):
        return False
    inventory = who.get("inventory")
    if not isinstance(inventory, list):
        return False
    for i, row in enumerate(inventory):
        name = row if isinstance(row, str) else (row.get("name") or row.get("item"))
        if name != item:
            continue
        if isinstance(row, dict) and int(row.get("uses") or 0) > 1:
            row["uses"] = int(row["uses"]) - 1
        else:
            del inventory[i]
        return True
    return False


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
        if rng is None:
            return {"ok": False, "reason": "That check has no dice roller."}
        if "dc" not in params:
            return {"ok": False, "reason": "That check needs a DC the card does not have."}
        mod = int(params.get("mod") or 0)
        d20 = int(rolltool.evaluate(rolltool.parse_expression("1d20"), rng)["total"])
        total = d20 + mod
        dc = int(params["dc"])
        success = total >= dc
        who = _actor(state, params.get("target"))
        roll = {"kind": kind, "d20": d20, "total": total, "dc": dc, "success": success}
        if who is not None:
            who["last_roll"] = roll
        condition = params.get("condition")
        if who is not None and condition:
            if success:
                clear_condition(who, condition)
            else:
                add_condition(who, condition)
        return {
            "ok": True,
            "resolve_as": kind,
            "d20": d20,
            "total": total,
            "dc": dc,
            "success": success,
            "target": None if who is None else who.get("name"),
            "condition": condition,
            "ruling": applied.get("ruling"),
            "tag": "POST-SESSION REVIEW",
        }
    if kind in ("damage", "heal"):
        who = _combatant(state, params.get("target"))
        if who is None or "amount" not in params:
            return {"ok": False, "reason": "That ruling names no target."}
        before = int(who.get("hp") or 0)
        amount = int(params["amount"])
        if kind == "damage":
            apply_damage(
                who, amount, params.get("type") or params.get("damage_type"), crit=bool(params.get("crit"))
            )
        else:
            apply_healing(who, amount)
        return {
            "ok": True,
            "resolve_as": kind,
            "target": who.get("name"),
            "target_hp": who["hp"],
            "amount": amount,
            "hp_changed": who["hp"] != before,
            "ruling": applied.get("ruling"),
            "tag": "POST-SESSION REVIEW",
        }
    if kind == "condition":
        who = _combatant(state, params.get("target"))
        name = params.get("condition")
        if who is None or not name:
            return {"ok": False, "reason": "That ruling names no condition."}
        canon = add_condition(who, name)
        if not canon:
            return {"ok": False, "reason": "That is not a condition."}
        return {
            "ok": True,
            "resolve_as": kind,
            "condition": canon,
            "target": who.get("name"),
            "ruling": applied.get("ruling"),
            "tag": "POST-SESSION REVIEW",
        }
    if kind == "move":
        dest = params.get("to")
        if not dest and params.get("distance_ft") is None:
            return {"ok": False, "reason": "That move names no destination."}
        who = _actor(state, params.get("target"))
        if isinstance(who, dict) and dest:
            who["position"] = dest
        if dest:
            state["position"] = dest
        if params.get("distance_ft") is not None:
            state["distance_ft"] = params.get("distance_ft")
        return {
            "ok": True,
            "resolve_as": kind,
            "to": dest,
            "position": state.get("position"),
            "distance_ft": params.get("distance_ft"),
            "hp_changed": False,
            "applied": True,
            "ruling": applied.get("ruling"),
            "tag": "POST-SESSION REVIEW",
        }
    if kind == "item":
        item = params.get("item")
        action = params.get("action") or "use"
        if not item:
            return {"ok": False, "reason": "That item ruling names no item."}
        who = _actor(state, params.get("target"))
        spent = _spend_item(who, item)
        if not spent:
            return {
                "ok": False,
                "reason": "That item is not in hand.",
                "resolve_as": kind,
                "item": item,
                "spent": False,
                "hp_changed": False,
            }
        state["last_item"] = {"item": item, "action": action, "spent": spent}
        before = int(who.get("hp") or 0) if isinstance(who, dict) else None
        if isinstance(who, dict) and "amount" in params and action in ("use", "drink"):
            apply_healing(who, int(params["amount"]))
        return {
            "ok": True,
            "resolve_as": kind,
            "item": item,
            "action": action,
            "spent": spent,
            "hp_changed": isinstance(who, dict) and who.get("hp") != before,
            "applied": True,
            "ruling": applied.get("ruling"),
            "tag": "POST-SESSION REVIEW",
        }
    return {"ok": False, "reason": "resolve_as is not an action code can run"}
