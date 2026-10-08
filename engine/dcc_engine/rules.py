"""Importable rules. Dice come from tools/roll.py. Loot helpers come from tools/loot.py.

This module does not write sessions/, sessions-data/, or credit ledgers.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import roll as rolltool  # noqa: E402
import loot as loottool  # noqa: E402

__all__ = ["rolltool", "loottool", "ScriptedRng", "attack", "cunning_action", "apply_damage"]


class ScriptedRng:
    """Pops integers from a hand-written dice script. Does not read session logs."""

    def __init__(self, rolls):
        self.rolls = [int(n) for n in rolls]

    def randint(self, a, b):
        if not self.rolls:
            raise RuntimeError("dice script ran out")
        n = self.rolls.pop(0)
        if n < a or n > b:
            raise RuntimeError("scripted roll %s is outside %s-%s" % (n, a, b))
        return n


def _roll_expr(expr, rng):
    terms = rolltool.parse_expression(expr)
    return rolltool.evaluate(terms, rng)


def _crit_expr(expr):
    def repl(m):
        return "%dd%s" % (int(m.group(1)) * 2, m.group(2))

    return re.sub(r"(\d+)d(\d+)", repl, expr, count=1)


def attack(attacker, target, rng, attack_name=None):
    """Resolve one attack. `to_hit` is taken only from the chosen attack on the attacker.

    A natural 20 hits and doubles the damage dice. A natural 1 misses.
    """
    attacks = list(attacker.get("attacks") or [])
    if not attacks:
        raise ValueError("%s has no attacks" % attacker.get("name"))
    chosen = None
    if attack_name:
        for atk in attacks:
            if atk.get("name") == attack_name:
                chosen = atk
                break
        if chosen is None:
            raise ValueError("no attack named %s" % attack_name)
    else:
        chosen = attacks[0]
    to_hits = {int(a["to_hit"]) for a in attacks}
    if len(to_hits) != 1:
        raise ValueError("%s attacks do not share one to-hit" % attacker.get("name"))
    d20 = _roll_expr("1d20", rng)["total"]
    bonus = int(chosen["to_hit"])
    total = d20 + bonus
    nat20 = d20 == 20
    nat1 = d20 == 1
    ac = int(target["ac"])
    hit = nat20 or (not nat1 and total >= ac)
    damage = 0
    damage_total = None
    if hit:
        expr = chosen["damage"]
        if nat20:
            expr = _crit_expr(expr)
        rolled = _roll_expr(expr, rng)
        damage = max(0, int(rolled["total"]))
        damage_total = rolled["total"]
        apply_damage(target, damage)
    return {
        "attacker": attacker.get("name"),
        "target": target.get("name"),
        "attack": chosen.get("name"),
        "to_hit": bonus,
        "d20": d20,
        "total": total,
        "ac": ac,
        "hit": hit,
        "nat20": nat20,
        "nat1": nat1,
        "damage": damage,
        "damage_total": damage_total,
        "target_hp": int(target["hp"]),
    }


def apply_damage(combatant, amount):
    combatant["hp"] = max(0, int(combatant.get("hp", 0)) - int(amount))
    return combatant["hp"]


def cunning_action(crawler, kind="dash"):
    """Cunning Action is a Rogue feature at level 2 or higher. Rogue 1 is refused."""
    cls = str(crawler.get("class") or crawler.get("cls") or "").lower()
    level = int(crawler.get("level") or 1)
    if cls == "rogue" and level < 2:
        return {
            "ok": False,
            "reason": "Cunning Action is refused at Rogue 1. It is a Rogue feature at level 2 or higher.",
            "kind": kind,
        }
    if cls != "rogue":
        return {"ok": False, "reason": "Cunning Action is a Rogue feature.", "kind": kind}
    return {"ok": True, "reason": "Cunning Action (%s) spent as the bonus action." % kind, "kind": kind}


def credit_dice(expr, rng):
    """Roll a credit expression with tools/roll.py. Does not write a ledger."""
    return _roll_expr(expr, rng)["total"]
