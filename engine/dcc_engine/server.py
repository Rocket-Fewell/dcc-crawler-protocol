"""Stdio JSON-lines server. One JSON object per line in, one or more out."""

from __future__ import annotations

import json
import re
import sys

from dcc_engine.model import ModelClient
from dcc_engine.rules import ScriptedRng, attack, cunning_action
from dcc_engine.ruling import apply_ruling, resolve_effect
from dcc_engine.store import Store

# Offline fallback. The fast model classifies when it is live.
# engine: attack or Cunning Action. ruling: any other attempt. chatter: the rest.
_ACTION_VERBS = frozenset((
    "throw", "light", "open", "push", "pull", "cast", "hide", "search", "smash",
    "climb", "jump", "shove", "grapple", "improvise", "use", "check", "look",
    "drink", "pick", "unlock", "sneak", "read", "wish", "lock", "run", "kick",
    "steal", "give", "bribe", "eat", "talk", "attack", "swing", "shoot",
    "stab", "hit", "strike", "grab", "pry", "hack", "break", "barricade", "lean", "sprint",
))
_NEGATION = frozenset((
    "don't", "dont", "won't", "wont", "not", "never", "no", "can't", "cant",
    "cannot", "wouldn't", "wouldnt", "shouldn't", "shouldnt",
))
_CHATTER_PHRASES = (
    "wish i had", "wish we had", "look at that", "check this out",
    "pick a favorite", "is it open",
)
_ATTACK_VERBS = frozenset(("attack", "swing", "shoot", "stab", "hit", "strike"))


def _words(text):
    return re.findall(r"[a-z']+", (text or "").lower())


def _stem(word):
    if word in _ACTION_VERBS:
        return word
    for suf in ("ing", "ed", "es", "s"):
        if word.endswith(suf) and len(word) - len(suf) >= 3:
            base = word[: -len(suf)]
            if base in _ACTION_VERBS:
                return base
            if suf in ("ing", "ed") and (base + "e") in _ACTION_VERBS:
                return base + "e"
    return word


def classify_line(text):
    """Word fallback when the fast model is offline. Negation is not an action."""
    raw = " ".join(_words(text))
    if not raw:
        return "chatter"
    if any(phrase in raw for phrase in _CHATTER_PHRASES):
        return "chatter"
    if raw in ("hello", "slightly", "broadcast"):
        return "chatter"
    words = _words(text)
    request = bool(re.search(r"\b(can|may|could|should)\s+(i|we)\b", raw))
    if (text or "").strip().endswith("?") and not request:
        return "chatter"
    negated = False
    positive = []
    cunning_open = False
    for word in words:
        if word in _NEGATION or word.endswith("n't"):
            negated = True
            continue
        if word == "cunning" and not negated:
            cunning_open = True
        stem = _stem(word)
        if stem in _ACTION_VERBS:
            if not negated:
                positive.append(stem)
            negated = False
    if cunning_open:
        return "engine"
    if any(verb in _ATTACK_VERBS for verb in positive):
        return "engine"
    if positive:
        return "ruling"
    return "chatter"


def needs_ruling(text):
    """True when the line is an action the engine did not already resolve."""
    return classify_line(text) == "ruling"


def line_class(text, model):
    """Fast model first. The word list runs only when that call does not answer."""
    label = None
    classify = getattr(model, "classify", None)
    if classify is not None:
        label = classify(text)
    if label not in ("chatter", "engine", "ruling"):
        label = classify_line(text)
    return label


def handle(msg, state, model, store):
    kind = msg.get("type")
    if kind == "line":
        text = msg.get("text") or ""
        label = line_class(text, model)
        words = _words(text)
        if label == "engine" and "cunning" in words:
            return handle({"type": "cunning_action", "crawler": state["crawler"], "kind": "dash"}, state, model, store)
        if label == "engine":
            return handle({"type": "attack", "attacker": "crawler", "target": state.get("target_id", "mannequin")}, state, model, store)
        snap = {"line": text, "narrator_line": state.get("narrator_line"), "result": {}}
        if label != "ruling":
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
