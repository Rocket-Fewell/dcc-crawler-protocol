"""Dice through tools/roll.py. This module never writes a session log."""

import re

_DICE = re.compile(r"^(\d*)d(\d+)([+-]\d+)?$")


def roll_expr(expr, rng, label, who):
    """Return roll()'s dict. Callers must not pass the result to append_log."""
    import roll

    return roll.roll(str(expr), label=label, who=who, rng=rng)


def double_dice(expr):
    """Crits double the dice, not the modifier. '1d6+3' becomes '2d6+3'."""
    text = str(expr).replace(" ", "")
    match = _DICE.fullmatch(text)
    if not match:
        raise ValueError(f"not a damage expression: {expr}")
    count = int(match.group(1) or "1") * 2
    tail = match.group(3) or ""
    return f"{count}d{match.group(2)}{tail}"


def ability_mod(score):
    return (int(score) - 10) // 2
