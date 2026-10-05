"""Sealed repair log: gm-notes/secret/repair-log.jsonl (per session: gm-notes/secret/sessions/<id>/), mode 600, append-only,
every line hash-chained (rules/50 sections 9-10: the GM's judgments are committed BEFORE the dice and revealed at the finale).

Two kinds of line:
  commit      the GM's call (fit tier, busted grade, rapport word) with a random nonce, so the value cannot be guessed from the hash.
              Never printed except by `repair-log reveal --finale`.
  tell        the GM logged that a tell was shown in a scene (scene + floor only, no quirk details). Busted calls are valid only then.
  busted_call a player's Busted call: ONLY the player's own call text and Busted / Not busted (no sealed data), plus the Therapy flag.
Each line: seq, ts, type, ..., prev (hash of the previous line, 64 zeros for the first), hash = sha256(prev + "|" + canonical json of the
line without `hash`). `verify` recomputes the chain and prints no content."""
import argparse
import hashlib
import json
import os
import re
import secrets
import time

ZERO = "0" * 64
COMMIT_KINDS = {"fit": "Tribute Fit tier", "busted": "Busted grade", "rapport": "Rapport word"}
RAPPORT_WORDS = ["frosty", "cool", "warm", "cozy"]


class RepairLogError(Exception):
    pass



def _cli_int(raw, signed=False):
    """argparse type for integer CLI options (same rule as state.py): ASCII digits 0-9 only, no spaces, decimals or leading zeros; a lone 0 is fine.
    signed=True also accepts a leading '+' (for deltas such as +2); '-' is accepted either way and range checks stay with each command."""
    pat = r"0|[+-]?[1-9][0-9]*" if signed else r"0|-?[1-9][0-9]*"
    if not re.fullmatch(pat, str(raw)):
        raise argparse.ArgumentTypeError(f"must be a whole number written with the digits 0-9 only (no spaces, {'' if signed else chr(39) + '+' + chr(39) + ' signs, '}decimals or leading zeros; a lone 0 is fine), got {str(raw)!r}")
    return int(raw)


def _cli_signed(raw):
    return _cli_int(raw, signed=True)

def _gq():
    import gm_quirks
    return gm_quirks


def path():
    return os.path.join(_gq().secret_dir(), "repair-log.jsonl")


def _canon(entry):
    return json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def entry_hash(prev, entry):
    body = {k: v for k, v in entry.items() if k != "hash"}
    return hashlib.sha256((prev + "|" + _canon(body)).encode("utf-8")).hexdigest()


def read_entries(verify=True):
    entries, prev = [], ZERO
    try:
        with open(path(), encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    e = json.loads(line)
                except ValueError:
                    raise RepairLogError("the repair log has an unreadable line; refusing to continue")
                if verify and (e.get("prev") != prev or e.get("hash") != entry_hash(prev, e) or e.get("seq") != len(entries) + 1):
                    raise RepairLogError(f"the repair log chain is broken at line {n}; refusing to continue (do not edit the file)")
                prev = e.get("hash", prev)
                entries.append(e)
    except FileNotFoundError:
        pass
    return entries


def append(entry):
    """Append one chained line (caller holds gm_quirks.lock()). Returns the stored entry."""
    gq = _gq()
    gq.ensure_secret_dir()
    existing = read_entries()
    prev = existing[-1]["hash"] if existing else ZERO
    e = {"seq": len(existing) + 1, "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), **entry, "prev": prev}
    e["hash"] = entry_hash(prev, e)
    fd = os.open(path(), os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try:
        os.write(fd, (json.dumps(e, ensure_ascii=True, separators=(",", ":")) + "\n").encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    os.chmod(path(), 0o600)
    return e


def _clean(text, limit):
    return re.sub(r"\s+", " ", str(text or "")).strip()[:limit]


# ----------------------------------------------------------------------- commands (called through state.py)

def cmd_add(a):
    gq = _gq()
    gq._need_core()
    kind = (a.kind or "").lower()
    value = _clean(a.value, 80)
    if kind not in COMMIT_KINDS or not value:
        raise gq.GMError("usage: repair-log add --kind fit|busted|rapport --value TEXT --crawler X --floor N [--scene S] [--note TEXT]")
    if kind == "rapport" and value.lower() not in RAPPORT_WORDS:
        raise gq.GMError("a rapport word is one of Frosty, Cool, Warm, Cozy")
    if not (a.crawler and a.floor is not None):
        raise gq.GMError("a committed call needs --crawler and --floor")
    with gq.lock():
        e = append({"type": "commit", "kind": kind, "value": value, "crawler": _clean(a.crawler, 60), "floor": a.floor,
                    "scene": _clean(a.scene, 60) or None, "note": _clean(a.note, 200) or None, "nonce": secrets.token_hex(16)})
    # the hash is a public commitment: it reveals nothing without the nonce
    return {"ok": True, "seq": e["seq"], "hash": e["hash"]}, f"committed #{e['seq']} (sealed). chain head {e['hash'][:16]}"


def cmd_tell(a):
    """The GM records that a tell was shown in this scene: scene and floor only, no quirk details. A Busted call is valid only in such a scene."""
    gq = _gq()
    gq._need_core()
    scene = _clean(a.scene, 60)
    if not scene or a.floor is None or a.floor < 1:
        raise gq.GMError("usage: repair-log tell --scene SCENE_ID --floor N")
    with gq.lock():
        try:
            rows = read_entries()
        except RepairLogError as e:
            raise gq.GMError(str(e))
        if any(e.get("type") == "tell" and e["scene"] == scene and e["floor"] == a.floor for e in rows):
            return {"ok": True, "logged": False}, f"a tell is already logged for scene {scene}"
        e = append({"type": "tell", "scene": scene, "floor": a.floor})
    return {"ok": True, "logged": True, "seq": e["seq"]}, f"tell logged for scene {scene} (#{e['seq']}); Busted calls are open in this scene"


def tell_shown(rows, scene, floor):
    return any(e.get("type") == "tell" and e["scene"] == scene and e["floor"] == floor for e in rows)


def cmd_verify(a):
    gq = _gq()
    gq._need_core()
    with gq.lock():
        try:
            n = len(read_entries())
        except RepairLogError as e:
            raise gq.GMError(str(e))
        head = read_entries()[-1]["hash"] if n else ZERO
    return {"ok": True, "lines": n, "head": head}, f"repair log chain OK: {n} line(s), head {head[:16]}"


def cmd_calls(a):
    """Players' own Busted calls and results (their text only): safe for the GM to read at any time."""
    gq = _gq()
    gq._need_core()
    with gq.lock():
        try:
            rows = [e for e in read_entries() if e.get("type") == "busted_call"]
        except RepairLogError as e:
            raise gq.GMError(str(e))
    if a.crawler:
        rows = [r for r in rows if r["crawler"].lower() == a.crawler.lower()]
    out = [{k: r[k] for k in ("seq", "ts", "crawler", "floor", "scene", "kind", "text", "result", "therapy_unlocked", "therapy_min_floor")} for r in rows]
    lines = [f"#{r['seq']} F{r['floor']} {r['scene']} {r['crawler']} [{r['kind']}] \"{r['text']}\" -> {r['result']}" + (" | Therapy unlocked (Floor 8+, 250 x multiplier)" if r["therapy_unlocked"] else "") for r in out]
    return {"ok": True, "calls": out}, "\n".join(lines) or "(no Busted calls yet)"


def cmd_reveal(a):
    gq = _gq()
    gq._need_core()
    if not a.finale:
        raise gq.GMError("REFUSED: the repair log is sealed until the finale (pass --finale at the finale reveal)")
    with gq.lock():
        try:
            rows = read_entries()
        except RepairLogError as e:
            raise gq.GMError(str(e))
    lines = ["*** FINALE REVEAL: publish this next to the chain head hash. ***", ""]
    for e in rows:
        if e["type"] == "commit":
            lines.append(f"#{e['seq']} F{e['floor']} {e.get('scene') or '-'} {e['crawler']}: {COMMIT_KINDS[e['kind']]} = {e['value']}" + (f" ({e['note']})" if e.get("note") else "") + f"  [hash {e['hash'][:12]}]")
        elif e["type"] == "tell":
            lines.append(f"#{e['seq']} F{e['floor']} {e['scene']}: tell shown  [hash {e['hash'][:12]}]")
        else:
            lines.append(f"#{e['seq']} F{e['floor']} {e['scene']} {e['crawler']}: Busted call [{e['kind']}] \"{e['text']}\" -> {e['result']}  [hash {e['hash'][:12]}]")
    head = rows[-1]["hash"] if rows else ZERO
    lines.append(f"\nchain head: {head}")
    return {"ok": True, "entries": rows, "head": head}, "\n".join(lines)


def add_parsers(sub, common):
    rl = sub.add_parser("repair-log", help="sealed repair log: add (commit the GM's call before dice) | verify | calls | reveal --finale")
    rsub = rl.add_subparsers(dest="rl_cmd", required=True, metavar="SUBCOMMAND")

    def leaf(name, fn, help_):
        sp = rsub.add_parser(name, help=help_, parents=[common])
        sp.set_defaults(fn=fn)
        return sp
    sp = leaf("add", cmd_add, "commit a GM call (sealed; prints only the sequence number and chain head)")
    sp.add_argument("--kind", required=True, choices=sorted(COMMIT_KINDS), help="fit (Tribute Fit tier) | busted (grade) | rapport (word)")
    sp.add_argument("--value", required=True)
    sp.add_argument("--crawler", required=True)
    sp.add_argument("--floor", type=_cli_int, required=True)
    sp.add_argument("--scene")
    sp.add_argument("--note")
    sp = leaf("tell", cmd_tell, "GM: a tell was shown in this scene (scene + floor only; opens Busted calls for that scene)")
    sp.add_argument("--scene", required=True)
    sp.add_argument("--floor", type=_cli_int, required=True)
    leaf("verify", cmd_verify, "recompute the hash chain (prints no content)")
    sp = leaf("calls", cmd_calls, "players' own Busted calls and results (their text only; no sealed data)")
    sp.add_argument("--crawler")
    sp = leaf("reveal", cmd_reveal, "FINALE ONLY: print every line; refuses without --finale")
    sp.add_argument("--finale", action="store_true")
