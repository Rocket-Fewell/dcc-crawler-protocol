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
    "lie", "tie", "try", "duck", "pour", "punch", "slash",
))
_NEGATION = frozenset((
    "don't", "dont", "won't", "wont", "not", "never", "no", "can't", "cant",
    "cannot", "wouldn't", "wouldnt", "shouldn't", "shouldnt",
))
_CHATTER_PHRASES = (
    "wish i had", "wish we had", "look at that", "look at this",
    "check this out", "check it out", "pick a favorite", "is it open",
    "we should probably", "i think we should",
)
_ATTACK_VERBS = frozenset((
    "attack", "swing", "shoot", "stab", "hit", "strike", "punch", "slash",
))
_PRONOUNS = frozenset(("it", "him", "her", "them", "he", "she"))
_WEAPONS = frozenset((
    "crowbar", "sword", "dagger", "knife", "axe", "bow", "club", "mace",
    "spear", "hammer", "crossbow", "sling", "weapon", "blade", "bat", "pipe", "gun",
))
_NAME_STOP = frozenset(("staff", "the", "with", "from", "that", "this"))


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


def _creature_tokens(creatures):
    """Names a line can hit. With no room, tests still know the mannequin."""
    if creatures is None:
        creatures = ("mannequin",)
    tokens = []
    for item in creatures:
        if isinstance(item, str):
            text = item
        elif isinstance(item, dict):
            text = " ".join(str(item.get(key) or "") for key in ("name", "our_name", "id"))
        else:
            continue
        for part in _words(text):
            if len(part) >= 4 and part not in _NAME_STOP:
                tokens.append(part)
    return tokens


def attack_lands(text, creatures=None):
    """True when an attack line names a creature, or a weapon is used on one."""
    words = _words(text)
    raw = set(words)
    if any(token in raw for token in _creature_tokens(creatures)):
        return True
    return any(word in _PRONOUNS for word in words) and any(word in _WEAPONS for word in words)


def _state_creatures(state):
    names = []
    for key, body in (state.get("combatants") or {}).items():
        if key == "crawler":
            continue
        names.append(key.replace("-", " "))
        if isinstance(body, dict) and body.get("name"):
            names.append(body["name"])
    return names


def _target_id(text, state):
    raw = set(_words(text))
    joined = " ".join(_words(text))
    for key, body in (state.get("combatants") or {}).items():
        if key == "crawler":
            continue
        if key in raw or key.replace("-", " ") in joined:
            return key
        name = str((body or {}).get("name") or "")
        for part in _words(name):
            if len(part) >= 4 and part not in _NAME_STOP and part in raw:
                return key
    return state.get("target_id") or "mannequin"


def classify_line(text, creatures=None):
    """Word fallback when the fast model is offline. Negation is not an action.

    An attack verb rolls damage only when the line names a creature (or a weapon
    is used on one). Anything else with a verb is a ruling.
    """
    raw = " ".join(_words(text))
    if not raw:
        return "chatter"
    if any(phrase in raw for phrase in _CHATTER_PHRASES):
        return "chatter"
    if raw in ("hello", "slightly", "broadcast"):
        return "chatter"
    words = _words(text)
    request = bool(re.search(r"\b(can|may|could|should)\s+(i|we)\b", raw))
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
        if attack_lands(text, creatures):
            return "engine"
        return "ruling"
    if positive:
        return "ruling"
    if (text or "").strip().endswith("?") and not request:
        return "chatter"
    return "chatter"


def needs_ruling(text):
    """True when the line is an action the engine did not already resolve."""
    return classify_line(text) == "ruling"


def line_class(text, model, creatures=None):
    """Fast model first. The word list runs only when that call does not answer."""
    label = None
    classify = getattr(model, "classify", None)
    if classify is not None:
        label = classify(text)
    if label not in ("chatter", "engine", "ruling"):
        label = classify_line(text, creatures)
    return label


def handle(msg, state, model, store):
    kind = msg.get("type")
    if kind == "line":
        text = msg.get("text") or ""
        creatures = _state_creatures(state)
        label = line_class(text, model, creatures)
        words = _words(text)
        if label == "engine" and "cunning" in words:
            return handle({"type": "cunning_action", "crawler": state["crawler"], "kind": "dash"}, state, model, store)
        if label == "engine" and not attack_lands(text, creatures):
            label = "ruling"
        if label == "engine":
            return handle({
                "type": "attack",
                "attacker": "crawler",
                "target": _target_id(text, state),
            }, state, model, store)
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
