#!/usr/bin/env python3
"""Coverage + hash + content check for Lore's /create "screens" display layer (create-screens-reskins), modeled on background_reskins.py.
Owner: Architect (tool) / DCC Lore (the table) | Status: LIVE (approved by Caleb) | Version: 0.1.0 | Updated: 2026-10-04
Summary: tables/create-screens-reskins.json (Lore's format create-screens-reskins/0.1.0; entries[] with id, screen, kind, state label|text, old, new, placeholders, old_placeholders, chargen_ref, source_match) is DISPLAY ONLY: the bridge swaps `old` for `new` on the later /create screens (S3-S17: buttons, labels, hints, help, dialogs, notices, errors) only while create.screens_reskin is true in session.json. A row is applied only if its `old` still matches the bridge's current text (drift guard), every {placeholder} of `new` is supplied, and the rule numbers survive; otherwise the plain text shows. "credits" for GP is display-only. ids, state.json, the ledger, package values, amounts and the rules keep the plain 5e names and numbers. The 11 changed create-flow lines (v0.1.2) are a plain swap of tables/create-flow-lines.json (version file next to it) and are NOT behind this flag.

Usage:
  python3 tools/create_screens_reskins.py [--path FILE] [--strict] [--json]   hash + structure + content report
      --path     check another copy (e.g. lore/tables/create-screens-reskins.json); its version file is read from the same folder
      --strict   also exit 1 on a content WARN (length limits, chargen_ref not found)
  python3 tools/create_screens_reskins.py --source-map [--json]   which row ids the bridge code wires (grep of src/create) and which source_match=not_found rows are still unresolved
  python3 tools/create_screens_reskins.py --money-words [--json]   Lore text (backgrounds, items, screens, flow lines) that still says GP/cp/gold/cash: report only, the bridge shows credits (src/create/money.js)
  python3 tools/create_screens_reskins.py --ids [--json]          every row id with its screen, kind and source_match
  python3 tools/create_screens_reskins.py --enable | --disable [--session ID]   set create.screens_reskin true/false in that session's session.json
  ROLLBACK (instant, no restart for the tables): python3 tools/create_screens_reskins.py --disable
      the bridge reads the flag when each /create screen is drawn; plain screens return immediately. The v0.1.2 flow lines are separate: cp tables/create-flow-lines.v0.1.1.bak.json tables/create-flow-lines.json && rm tables/create-flow-lines.version.json
  No table in tables/ = "absent", exit 0.
Exit 1 on a hash mismatch, a structure error or a content ERROR (a lost placeholder or rule number, a bad label, 'champs')."""
import argparse
import hashlib
import json
import os
import re
import sys

import dcc_paths as _paths  # noqa: E402
HERE = os.path.dirname(os.path.abspath(__file__))
CAMPAIGN = os.path.dirname(HERE)
TABLES = os.path.join(CAMPAIGN, "tables")
BRIDGE = os.environ.get("DCC_BRIDGE_DIR") or str(_paths.bridge_root())
SCHEMA = "create-screens-reskins/0.1.0"
KINDS_STATE = ("label", "text")
RENAMED = {"hint-s8-method-line": ({"method"}, {"method_label"}), "select-s8-assign": ({"ab"}, {"ability_label"}),
           "hint-money-cp": ({"n"}, {"amount"})}
MAX_MODAL, MAX_BUTTON, MAX_SELECT = 45, 80, 100
PH = re.compile(r"\{(\w+)\}")
FAMILIES = ("opt-fighting-style-", "opt-invocation-")


def default_path(tables=TABLES):
    return os.environ.get("CREATE_SCREENS_RESKINS_PATH") or os.path.join(tables, "create-screens-reskins.json")


def version_path(path):
    return os.path.join(os.path.dirname(path), "create-screens-reskins.version.json")


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha256_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def check_hash(path):
    """-> (status, message): ok | warn | fail | absent. Also checks the companion (proposed flow lines) sha."""
    if not os.path.exists(path):
        return "absent", f"{path} is not in place: later /create screens keep the plain 5e text"
    v = version_path(path)
    if not os.path.exists(v):
        return "warn", "create-screens-reskins.version.json not found next to the table; cannot verify the hash"
    try:
        vd = _load(v)
        want = vd["sha256"]
    except (OSError, ValueError, KeyError) as e:
        return "fail", f"cannot read sha256 from the version file: {e}"
    got = sha256_of(path)
    if got != want:
        return "fail", f"create-screens-reskins.json sha256 {got[:12]} does not match the version file {str(want)[:12]}: a stale or edited copy? Re-copy Lore's file and version file together"
    msg = f"create-screens-reskins.json matches the version file ({want[:12]}, v{vd.get('version', '?')})"
    comp = (vd.get("companions") or {}).get("tables/create-flow-lines.proposed.json")
    cp = os.path.join(os.path.dirname(path), "create-flow-lines.proposed.json")
    if comp and os.path.exists(cp) and sha256_of(cp) != comp.get("sha256"):
        return "fail", "create-flow-lines.proposed.json does not match the sha in the version file's companions entry"
    return "ok", msg


def set_flag(on, session=None, campaign=CAMPAIGN):
    """Write create.screens_reskin into the session's session.json (alpha: sessions/session.json). Config only; no state or ledger. Atomic."""
    sid = session or os.environ.get("DCC_SESSION") or "alpha"
    d = os.path.join(campaign, "sessions") if sid == "alpha" else os.path.join(campaign, "sessions-data", sid)
    p = os.path.join(d, "session.json")
    data = _load(p) if os.path.exists(p) else {}
    data.setdefault("create", {})["screens_reskin"] = bool(on)
    os.makedirs(d, exist_ok=True)
    with open(p + ".tmp", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
    os.replace(p + ".tmp", p)
    return p


def _nums(s):
    return sorted(re.findall(r"\d+", PH.sub("", s)))


def _chargen_ref_ok(ref, cg):
    m = re.match(r"^(\w+)\.choices\[(\w+)\](\.options)?$", ref or "")
    if not m:
        return True   # not a shape we can resolve: skip
    cls = cg.get("classes", {}).get(m.group(1))
    return bool(cls) and any(c.get("key") == m.group(2) for c in cls.get("choices", []))


def check(path=None, tables=TABLES):
    path = path or default_path(tables)
    st, msg = check_hash(path)
    rep = {"path": path, "hash": {"status": st, "message": msg}, "errors": [], "warnings": [], "entry_count": 0, "counts": {}}
    if st == "absent":
        return rep
    err, warn = rep["errors"].append, rep["warnings"].append
    try:
        d = _load(path)
    except (OSError, ValueError) as e:
        err(f"cannot read the table: {e}")
        return rep
    pv = {"S1", "S2", "S13", "comfort_only"}
    if d.get("schema") != SCHEMA:
        err(f"schema should be {SCHEMA}, got {d.get('schema')}")
    rows = d.get("entries")
    if not isinstance(rows, list):
        err("entries[] missing")
        return rep
    rep["entry_count"] = len(rows)
    try:
        cg = _load(os.path.join(tables, "chargen-5e.json"))
    except (OSError, ValueError):
        cg = {}
    seen = set()
    for r in rows:
        i = r.get("id")
        if not i or i in seen:
            err(f"duplicate or missing id: {i}")
            continue
        seen.add(i)
        if not isinstance(r.get("old"), str) or not isinstance(r.get("new"), str) or not r["new"].strip():
            err(f"{i}: old/new must be non-empty strings")
            continue
        if r.get("state") not in KINDS_STATE:
            err(f"{i}: state should be label or text")
        po, pn = set(PH.findall(r["old"])), set(PH.findall(r["new"]))
        if {x.strip("{}") for x in r.get("old_placeholders", [])} != po or {x.strip("{}") for x in r.get("placeholders", [])} != pn:
            err(f"{i}: placeholders/old_placeholders do not match the strings")
        want = RENAMED.get(i)
        if want and (po, pn) == want:
            pass
        elif po != pn:
            err(f"{i}: placeholders changed {sorted(po)} -> {sorted(pn)}")
        if _nums(r["old"]) != _nums(r["new"]) and not set(_nums(r["old"])) <= set(_nums(r["new"])):
            err(f"{i}: rule numbers {_nums(r['old'])} not all kept in new ({_nums(r['new'])})")
        if r.get("plain_on") is not None and (not isinstance(r["plain_on"], list) or not set(r["plain_on"]) <= pv):
            err(f"{i}: plain_on must be a list of S1, S2, S13, comfort_only")
        if re.search(r"champ", r["new"], re.I):
            err(f"{i}: 'champs' in new text (say Crawlers)")
        if re.search(r"\bcrawlers?\b", re.sub(r"`[^`]*`", "", r["new"])):   # a `/crawlers` command in backticks is not player-facing prose
            err(f"{i}: 'Crawler' must be capitalised")
        if r.get("state") == "label" and r.get("combined_label") is not None:
            dn, sn = r.get("display_name"), r.get("srd_name")
            if r["combined_label"] not in r["new"] or r["combined_label"] != f"{dn} ({sn})" or r["combined_label"].count("(") != 1 or r["combined_label"].count(")") != 1:
                err(f"{i}: label should be 'Our Name (5e Name)' with one pair of parentheses")
        kind, n = r.get("kind", ""), len(r["new"])
        lim = MAX_MODAL if kind in ("modal_title", "field_label") else MAX_BUTTON if kind == "button" else MAX_SELECT if kind in ("select_label", "choice_option", "choice_group", "method", "package", "ability") else None
        if lim and n > lim:
            warn(f"{i}: new is {n} characters, over the {lim} limit for a {kind}")
        if r.get("chargen_ref") and cg and not _chargen_ref_ok(r["chargen_ref"], cg):
            warn(f"{i}: chargen_ref {r['chargen_ref']} not found in chargen-5e.json")
    sm = {}
    for r in rows:
        sm[r.get("source_match")] = sm.get(r.get("source_match"), 0) + 1
    rep["counts"] = sm
    return rep


MONEY = re.compile(r"\b(\d+(\.\d+)?\s*(gp|cp)|gp|cp|cash|gold|copper)\b", re.I)


def money_words(tables=TABLES):
    """-> list of (file, id, field, text): player-facing Lore text that still says GP/cp/gold/cash (report only; the bridge shows credits via money.js, the tables are not edited).
    Item prices (base_price*, price_flag) and meta are skipped; `old` fields are the bridge's old text and are listed with field 'old'."""
    out = []
    for f in ("background-reskins.json", "item-reskins.json", "create-screens-reskins.json"):
        p = os.path.join(tables, f)
        if not os.path.exists(p):
            continue
        for e in _load(p).get("entries", []):
            for k, v in e.items():
                if k in ("id", "base_price", "price_flag", "placeholders", "old_placeholders", "chargen_value") or not isinstance(v, str):
                    continue
                if MONEY.search(v):
                    out.append((f, e.get("id"), k, v))
    for f in ("create-flow-lines.json", "create-flow-lines.proposed.json"):
        p = os.path.join(tables, f)
        if os.path.exists(p):
            for key, arr in _load(p).get("lines", {}).items():
                for v in arr:
                    if MONEY.search(v):
                        out.append((f, key, "line", v))
    return out


def _bridge_src():
    out = ""
    base = os.path.join(BRIDGE, "src", "create")
    if not os.path.isdir(base):
        return None
    for f in sorted(os.listdir(base)):
        if f.endswith(".js") and f != "screenstext.js":
            out += open(os.path.join(base, f), encoding="utf-8").read() + "\n"
    return out


def source_map(path=None, tables=TABLES):
    """Which row ids appear as a literal in the bridge's src/create (the wiring), and which not_found rows are still unwired."""
    path = path or default_path(tables)
    rows = _load(path)["entries"] if os.path.exists(path) else []
    src = _bridge_src()
    if src is None:
        return {"error": f"bridge source not found at {BRIDGE}"}
    wired, unwired = [], []
    for r in rows:
        i = r["id"]
        ok = f"'{i}'" in src or f'"{i}"' in src or (i.startswith(FAMILIES) and any(f"'{p}'" in src for p in FAMILIES if i.startswith(p)))
        (wired if ok else unwired).append(i)
    nf = [r["id"] for r in rows if r.get("source_match") == "not_found"]
    return {"rows": len(rows), "wired": len(wired), "unwired": unwired, "not_found": len(nf), "not_found_still_unwired": [i for i in nf if i in unwired]}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Create screens reskins: hash, content, wiring")
    ap.add_argument("--ids", action="store_true")
    ap.add_argument("--source-map", action="store_true")
    ap.add_argument("--money-words", action="store_true", help="list Lore text that still says GP/cp/gold/cash (report only)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--path")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--enable", action="store_true", help="set create.screens_reskin true in the session's session.json")
    ap.add_argument("--disable", action="store_true", help="set it false (the rollback)")
    ap.add_argument("--session")
    a = ap.parse_args(argv)
    if a.enable or a.disable:
        print("wrote", set_flag(a.enable, a.session), "create.screens_reskin =", str(a.enable).lower())
        return 0
    if a.money_words:
        rows = money_words()
        if a.json:
            print(json.dumps([dict(zip(("file", "id", "field", "text"), r)) for r in rows], indent=1))
        else:
            for f, i, k, v in rows:
                print(f"{f}\t{i}.{k}\t{v[:140]!r}")
            print(f"total {len(rows)}")
        return 0
    if a.ids or a.source_map:
        p = a.path or default_path()
        if not os.path.exists(p):
            print("ABSENT:", p)
            return 0
        if a.ids:
            rows = _load(p)["entries"]
            if a.json:
                print(json.dumps([{k: r.get(k) for k in ("id", "screen", "kind", "state", "source_match")} for r in rows], indent=1))
            else:
                for r in rows:
                    print(f"{r['id']}\t{r['screen']}\t{r['kind']}\t{r['state']}\t{r['source_match']}")
                print(f"total {len(rows)}")
            return 0
        sm = source_map(a.path)
        if a.json:
            print(json.dumps(sm, indent=1))
        elif "error" in sm:
            print("ERROR:", sm["error"])
        else:
            print(f"wired {sm['wired']}/{sm['rows']} rows; source_match=not_found rows: {sm['not_found']}, still unwired: {len(sm['not_found_still_unwired'])}")
            for i in sm["unwired"]:
                print("  unwired:", i)
        return 1 if "error" in sm else 0
    rep = check(path=a.path)
    if a.json:
        print(json.dumps(rep, indent=1))
    else:
        print(f"{rep['hash']['status'].upper()}: {rep['hash']['message']}")
        if rep["hash"]["status"] != "absent":
            print(f"{rep['entry_count']} rows; source_match {rep['counts']}")
        for e in rep["errors"]:
            print("ERROR:", e)
        for w in rep["warnings"]:
            print("WARN:", w)
    bad = rep["hash"]["status"] == "fail" or bool(rep["errors"]) or (a.strict and bool(rep["warnings"]))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
