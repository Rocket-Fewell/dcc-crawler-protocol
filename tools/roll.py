#!/usr/bin/env python3
"""roll.py - dice roller for the DCC 5e campaign (stdlib only).

Usage:
  python3 tools/roll.py "2d20kh1+5" --label "Grimsby Stealth" --who Grimsby
  python3 tools/roll.py adv+5 --label "Attack" --who Donut
  python3 tools/roll.py 4d6dl1 --json

Output (one line, also appended to <campaign>/sessions/rolls-YYYY-MM-DD.log for alpha, <campaign>/sessions-data/<id>/rolls-YYYY-MM-DD.log for other sessions):
  [ROLL] Grimsby Stealth (Grimsby): 2d20kh1+5 -> [17, 4] keep 17 +5 = 22

Campaign dir: $DCC_CAMPAIGN_ROOT or legacy $DCC_CAMPAIGN_DIR; default = tools/ parent.
Exit codes: 0 ok, 2 invalid input.
"""
import argparse
import datetime as dt
import json
import os
import re
import secrets
import sys

import dcc_paths as _paths  # noqa: E402
DEFAULT_CAMPAIGN_DIR = _paths.CAMPAIGN_ROOT

# Sane limits
MAX_EXPR_LEN = 200
MAX_TERMS = 20
MAX_DICE_PER_TERM = 100
MAX_TOTAL_DICE = 200
MAX_SIDES = 1000
MAX_CONSTANT = 100_000
MAX_LABEL_LEN = 80


class RollError(ValueError):
    """Invalid roll expression or arguments."""


def campaign_dir():
    return str(_paths.campaign_root())


# --------------------------------------------------------------------------- parsing

_TOKEN_RE = re.compile(
    r"""
    (?P<dice>(?P<count>\d*)d(?P<sides>\d+)(?P<mod>(?:kh|kl|dh|dl|k)\d*)?)
  | (?P<const>\d+)
  | (?P<adv>adv|dis)
  | (?P<sign>[+-])
    """,
    re.VERBOSE,
)


def _tokenize(expr):
    if re.search(r"\d\s+\d", expr):
        raise RollError(f"numbers separated by a space in {expr!r} (missing + or -?)")
    s = re.sub(r"\s+", "", expr.lower())
    if not s:
        raise RollError("empty expression")
    pos, tokens = 0, []
    while pos < len(s):
        m = _TOKEN_RE.match(s, pos)
        if not m:
            raise RollError(f"cannot parse {s[pos:pos + 12]!r} in {expr!r}")
        tokens.append(m)
        pos = m.end()
    return tokens


def _parse_dice(count, sides, mod):
    n = int(count) if count else 1
    d = int(sides)
    if not 1 <= n <= MAX_DICE_PER_TERM:
        raise RollError(f"dice count must be 1-{MAX_DICE_PER_TERM} (got {n})")
    if not 2 <= d <= MAX_SIDES:
        raise RollError(f"die sides must be 2-{MAX_SIDES} (got {d})")
    term = {"type": "dice", "count": n, "sides": d, "mode": None, "n": None}
    if mod:
        m = re.fullmatch(r"(kh|kl|dh|dl|k)(\d*)", mod)
        mode = "kh" if m.group(1) == "k" else m.group(1)
        amount = int(m.group(2)) if m.group(2) else 1
        if mode in ("kh", "kl") and not 1 <= amount <= n:
            raise RollError(f"{mode}{amount}: must keep between 1 and {n} dice")
        if mode in ("dh", "dl") and not 0 <= amount <= n - 1:
            raise RollError(f"{mode}{amount}: must drop between 0 and {n - 1} dice (at least one die must remain)")
        term["mode"], term["n"] = mode, amount
    return term


def parse_expression(expr):
    """Parse an expression into a list of signed terms.

    Each term: {"sign": +1|-1, "type": "dice"|"const", ...}. Dice terms carry count, sides,
    mode (None|kh|kl|dh|dl) and n. `adv`/`dis` are shorthand for 2d20kh1 / 2d20kl1; written after
    a term (e.g. "d20+5 adv") they turn the first plain d20 into advantage/disadvantage.
    """
    if not isinstance(expr, str):
        raise RollError("expression must be a string")
    if len(expr) > MAX_EXPR_LEN:
        raise RollError(f"expression too long (max {MAX_EXPR_LEN} chars)")
    tokens = _tokenize(expr)

    terms, sign, expect_term, pending_adv = [], 1, True, []
    for m in tokens:
        if m.group("dice"):
            kind = "dice"
        elif m.group("const"):
            kind = "const"
        elif m.group("adv"):
            kind = "adv"
        else:
            kind = "sign"

        if kind == "sign":
            if expect_term and terms:
                raise RollError(f"unexpected operator in {expr!r}")
            if expect_term:  # leading sign: "-d4+10", "+d20"
                sign = -1 if m.group("sign") == "-" else 1
                continue
            sign = 1 if m.group("sign") == "+" else -1
            expect_term = True
        elif kind in ("dice", "const"):
            if not expect_term:
                raise RollError(f"missing + or - before {m.group(0)!r}")
            if kind == "dice":
                term = _parse_dice(m.group("count"), m.group("sides"), m.group("mod"))
            else:
                value = int(m.group("const"))
                if value > MAX_CONSTANT:
                    raise RollError(f"constant too large (max {MAX_CONSTANT})")
                term = {"type": "const", "value": value}
            term["sign"] = sign
            terms.append(term)
            sign, expect_term = 1, False
        else:  # adv / dis
            word = m.group("adv")
            if expect_term:  # standalone term: 2d20kh1 / 2d20kl1
                term = _parse_dice("2", "20", "kh1" if word == "adv" else "kl1")
                term["sign"] = sign
                terms.append(term)
                sign, expect_term = 1, False
            else:  # modifier on an earlier plain d20
                pending_adv.append(word)

    if expect_term:
        raise RollError(f"expression ends with an operator: {expr!r}")
    for word in pending_adv:
        for term in terms:
            if term["type"] == "dice" and term["sides"] == 20 and term["count"] == 1 and term["mode"] is None and term["sign"] == 1:
                term["count"] = 2
                term["mode"], term["n"] = ("kh", 1) if word == "adv" else ("kl", 1)
                break
        else:
            raise RollError(f"'{word}' needs a single d20 term to apply to (e.g. d20+5 {word})")

    if len(terms) > MAX_TERMS:
        raise RollError(f"too many terms (max {MAX_TERMS})")
    if sum(t["count"] for t in terms if t["type"] == "dice") > MAX_TOTAL_DICE:
        raise RollError(f"too many dice in total (max {MAX_TOTAL_DICE})")
    if not any(t["type"] == "dice" for t in terms):
        raise RollError("expression needs at least one die (e.g. d20, 2d6+3)")
    return terms


def term_text(term):
    if term["type"] == "const":
        return str(term["value"])
    s = f"{term['count']}d{term['sides']}"
    if term["mode"]:
        s += f"{term['mode']}{term['n']}"
    return s


def canonical_expression(terms):
    out = ""
    for i, t in enumerate(terms):
        out += ("-" if t["sign"] < 0 else ("+" if i else "")) + term_text(t)
    return out


# --------------------------------------------------------------------------- rolling

def _kept_indexes(rolls, mode, n):
    idx = range(len(rolls))
    if mode is None:
        return set(idx)
    if mode == "kh":
        order = sorted(idx, key=lambda i: (-rolls[i], i))
        return set(order[:n])
    if mode == "kl":
        order = sorted(idx, key=lambda i: (rolls[i], i))
        return set(order[:n])
    if mode == "dh":
        order = sorted(idx, key=lambda i: (-rolls[i], i))
        return set(idx) - set(order[:n])
    if mode == "dl":
        order = sorted(idx, key=lambda i: (rolls[i], i))
        return set(idx) - set(order[:n])
    raise RollError(f"unknown mode {mode}")


def evaluate(terms, rng=None):
    """Roll the parsed terms. `rng` needs .randint(a, b); default is secrets.SystemRandom."""
    rng = rng or secrets.SystemRandom()
    results, total = [], 0
    nat20 = nat1 = False
    for t in terms:
        if t["type"] == "const":
            results.append({"sign": t["sign"], "type": "const", "value": t["value"]})
            total += t["sign"] * t["value"]
            continue
        rolls = [rng.randint(1, t["sides"]) for _ in range(t["count"])]
        kept_idx = _kept_indexes(rolls, t["mode"], t["n"])
        kept = [r for i, r in enumerate(rolls) if i in kept_idx]
        subtotal = sum(kept)
        total += t["sign"] * subtotal
        if t["sides"] == 20 and t["sign"] > 0:
            nat20 = nat20 or 20 in kept
            nat1 = nat1 or 1 in kept
        results.append({
            "sign": t["sign"], "type": "dice", "expr": term_text(t), "sides": t["sides"],
            "rolls": rolls, "kept": kept, "dropped": [r for i, r in enumerate(rolls) if i not in kept_idx],
            "subtotal": subtotal,
        })
    return {"terms": results, "total": total, "nat20": nat20, "nat1": nat1}


def _clean(text, limit=MAX_LABEL_LEN):
    """Single-line, printable, length-limited text (keeps the [ROLL] line one line)."""
    text = re.sub(r"[\x00-\x1f\x7f]+", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()[:limit]


def format_line(expression, result, label=None, who=None, dc=None):
    parts = []
    for i, r in enumerate(result["terms"]):
        sign = "-" if r["sign"] < 0 else "+"
        if r["type"] == "const":
            parts.append(f"{sign}{r['value']}" if (i or sign == "-") else str(r["value"]))
            continue
        body = "[" + ", ".join(str(x) for x in r["rolls"]) + "]"
        if r["dropped"]:
            body += " keep " + ", ".join(str(x) for x in r["kept"]) if r["kept"] else ""
        prefix = "-" if r["sign"] < 0 else ("+" if i else "")
        parts.append(prefix + body)
    head = "[ROLL] " + (_clean(label) or "Roll")
    if _clean(who):
        head += f" ({_clean(who)})"
    line = f"{head}: {expression} -> {' '.join(parts)} = {result['total']}"
    flags = []
    if result["nat20"]:
        flags.append("NAT 20!")
    if result["nat1"]:
        flags.append("NAT 1!")
    if flags:
        line += f" ({' '.join(flags)})"
    if dc is not None:
        line += f" vs DC {dc} -> {'SUCCESS' if result['total'] >= dc else 'FAIL'}"
    return line


def roll(expr, label=None, who=None, dc=None, rng=None, now=None):
    """Parse + roll + format. Returns a dict (line, total, terms, nat20, nat1, ...)."""
    terms = parse_expression(expr)
    canonical = canonical_expression(terms)
    result = evaluate(terms, rng)
    now = now or dt.datetime.now().astimezone()
    return {
        "timestamp": now.isoformat(timespec="seconds"),
        "label": _clean(label) or "Roll",
        "who": _clean(who) or None,
        "expression": canonical,
        "terms": result["terms"],
        "total": result["total"],
        "nat20": result["nat20"],
        "nat1": result["nat1"],
        "dc": dc,
        "success": (result["total"] >= dc) if dc is not None else None,
        "line": format_line(canonical, result, label, who, dc),
    }


def log_path(now=None):
    now = now or dt.datetime.now().astimezone()
    import campaign_session
    return os.path.join(campaign_session.data_dir(), f"rolls-{now.date().isoformat()}.log")


def append_log(entry, now=None):
    path = log_path(now)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = f"{entry['timestamp']} {entry['line']}\n".encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, data)  # single O_APPEND write: safe against interleaving
    finally:
        os.close(fd)
    return path


# --------------------------------------------------------------------------- CLI

def build_parser():
    p = argparse.ArgumentParser(
        prog="roll.py",
        description="Roll dice, print a [ROLL] line, and log it to sessions/rolls-YYYY-MM-DD.log",
        epilog='Examples: roll.py "2d20kh1+5" --label "Stealth" --who Grimsby | roll.py adv+5 | roll.py 4d6dl1 --json',
    )
    p.add_argument("expression", nargs="+", help='e.g. "2d20kh1+5", "d20+5 adv", "adv", "dis", "4d6dl1", "2d6+1d4+3"')
    p.add_argument("--label", "-l", help="what is being rolled, e.g. 'Grimsby Stealth'")
    p.add_argument("--who", "-w", help="character or player name")
    p.add_argument("--dc", type=int, help="optionally compare the total against a DC")
    p.add_argument("--json", action="store_true", help="print JSON instead of the one-line text")
    p.add_argument("--no-log", action="store_true", help="do not append to the roll log")
    return p


def main(argv=None):
    import campaign_session
    try:
        argv = campaign_session.apply_cli_session(argv)
    except campaign_session.SessionError as e:
        print(f"[ROLL-ERROR] {e}", file=sys.stderr)
        return 2
    args = build_parser().parse_args(argv)
    try:
        entry = roll(" ".join(args.expression), args.label, args.who, args.dc)
    except RollError as e:
        print(f"[ROLL-ERROR] {e}", file=sys.stderr)
        return 2
    if not args.no_log:
        try:
            entry["log_file"] = append_log(entry)
        except OSError as e:
            print(f"[ROLL-WARN] could not write roll log: {e}", file=sys.stderr)
    print(json.dumps(entry, indent=2) if args.json else entry["line"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
