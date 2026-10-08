"""Stdio JSON-lines server. One JSON object per line in, one or more out."""

from __future__ import annotations

import json
import re
import sys

from dcc_engine.model import ModelClient
from dcc_engine.rules import ScriptedRng, attack, cunning_action
from dcc_engine.ruling import apply_ruling, resolve_effect
from dcc_engine.store import Store

# Whole words only. The engine resolves cunning and attack first.
# Any other action-shaped line goes to the strong model. Chatter does not.
_ACTION_VERBS = frozenset((
    "throw", "light", "open", "push", "pull", "cast", "hide", "search", "smash",
    "climb", "jump", "shove", "grapple", "improvise", "use", "check", "look",
    "drink", "pick", "unlock", "sneak", "read", "wish", "lock",
))


def _words(text):
    return re.findall(r"[a-z']+", (text or "").lower())


def needs_ruling(text):
    """True when the line is an action the engine did not already resolve."""
    words = _words(text)
    if not words:
        return False
    if words[0] in ("i", "we") and any(word in _ACTION_VERBS for word in words[1:4]):
        return True
    return words[0] in _ACTION_VERBS


def handle(msg, state, model, store):
    kind = msg.get("type")
    if kind == "line":
        text = (msg.get("text") or "").lower()
        words = _words(text)
        if "cunning" in words:
            return handle({"type": "cunning_action", "crawler": state["crawler"], "kind": "dash"}, state, model, store)
        if "attack" in words or text.startswith("i swing") or text.startswith("i shoot"):
            return handle({"type": "attack", "attacker": "crawler", "target": state.get("target_id", "mannequin")}, state, model, store)
        snap = {"line": msg.get("text"), "narrator_line": state.get("narrator_line"), "result": {}}
        if not needs_ruling(text):
            outs = [{"type": "say", "voice": "GM", "text": sentence} for sentence in model.stream(snap)]
            store.save_action("line", {"in": msg, "out": outs})
            return outs
        ruling = model.rule(snap)
        applied = resolve_effect(apply_ruling(ruling, state), state)
        store.save_action("ruling", applied)
        if not applied.get("ok"):
            outs = [{"type": "say", "voice": "SYSTEM", "text": "The System says no, try something else."}]
            store.save_action("line", {"in": msg, "out": outs})
            return outs
        if applied.get("resolve_as") == "attack":
            params = applied.get("params") or {}
            outs = handle({
                "type": "attack",
                "attacker": params.get("attacker") or "crawler",
                "target": params.get("target") or state.get("target_id", "mannequin"),
            }, state, model, store)
            store.save_action("line", {"in": msg, "out": outs})
            return outs
        snap = {"line": applied.get("ruling") or msg.get("text"), "narrator_line": state.get("narrator_line"), "result": applied}
        outs = [{"type": "say", "voice": "GM", "text": sentence} for sentence in model.stream(snap)]
        store.save_action("line", {"in": msg, "out": outs})
        return outs
    if kind == "cunning_action":
        result = cunning_action(msg.get("crawler") or state["crawler"], msg.get("kind") or "dash")
        snap = {"result": result, "narrator_line": state.get("narrator_line")}
        outs = [{"type": "say", "voice": "SYSTEM", "text": sentence} for sentence in model.stream(snap)]
        store.save_action("cunning_action", result)
        return outs
    if kind == "attack":
        who = msg.get("attacker") or "crawler"
        attacker = state["combatants"][who]
        target_id = msg.get("target") or state.get("target_id")
        target = state["combatants"][target_id]
        result = attack(attacker, target, state["rng"])
        snap = {"result": result, "narrator_line": state.get("narrator_line")}
        voice = "GM" if who == "crawler" else "SYSTEM"
        outs = [{"type": "say", "voice": voice, "text": sentence} for sentence in model.stream(snap)]
        outs.append({"type": "card", "crawler": target.get("name"), "hp": target.get("hp")})
        store.save_action("attack", result)
        return outs
    return [{"type": "say", "voice": "SYSTEM", "text": "The System says no, try something else."}]


def serve(stdin=None, stdout=None, state=None):
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    model = ModelClient(fake=True)
    store = Store()
    state = state or {}
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        for out in handle(msg, state, model, store):
            stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
            stdout.flush()
    store.close()
