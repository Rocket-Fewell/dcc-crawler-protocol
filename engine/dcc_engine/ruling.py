"""Strong-model ruling JSON. Code checks the shape, then resolves it.

A ruling is logged on the engine action store, tagged POST-SESSION REVIEW.
This module does not write gm-notes/.
"""

from __future__ import annotations

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
