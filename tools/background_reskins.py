#!/usr/bin/env python3
"""Coverage + hash check for Lore's S7 background display names ("Our Name (5e Name)"), modeled on species_class_reskins.py.
Owner: Architect (tool) / DCC Lore (the table) | Status: draft | Version: 0.1.0 | Updated: 2026-10-04
Summary: tables/background-reskins.json (Lore's format background-reskins/0.1.0; entries[] with id, kind, parent_id, srd_name, display_name, combined_label, chargen_value, flavor) is DISPLAY ONLY; the bridge shows it on /create S7 (and the S10 background package) only while create.background_reskin is true in session.json (default false, until Caleb approves). This tool lists every id the table must cover vs tables/chargen-5e.json (--ids), checks the file's structure and sha256, and with --strict fails on any missing id or a chargen_value that is not the exact chargen string. ids, state.json, the ledger and the rules keep the plain 5e names. Lore's own checker (dcc-lore tools/background_reskin_check.py) is the stricter content check.

Usage:
  python3 tools/background_reskins.py --ids [--json]        every id the table must cover (16 backgrounds, 2 bonus choices, 12 Origin feats, 32 gear packages)
  python3 tools/background_reskins.py [--path FILE] [--strict] [--json]   hash + structure + coverage report
      --path     check another copy (e.g. Lore's lore/tables/background-reskins.json); its version file is read from the same folder
      --strict   also exit 1 when any required id has no entry
  python3 tools/background_reskins.py --enable | --disable [--session ID]   set create.background_reskin true/false in that session's session.json
  No table in tables/ = "absent", exit 0 (with --strict, absent is also exit 0: nothing is live; use --path to check Lore's file before the drop-in).
Ids (Lore's scheme): kind background, id = the lower-cased chargen background key ('acolyte'); kind choice with parent_id origin-feat 'feat-<kebab origin feat>' ('feat-magic-initiate-cleric'), background-asi 'asi-2-1' / 'asi-1-1-1', background-kit 'package-a' / 'package-b' (shared by all backgrounds). chargen_value is the exact chargen string ('Magic Initiate (Cleric)', '+2 / +1', 'A').
Exit 1 on a hash mismatch, a structure error, or (with --strict) missing coverage."""
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
KINDS = ("background", "choice")
PARENTS = ("origin-feat", "background-asi", "background-kit")
ASI = (("asi-2-1", "+2 / +1"), ("asi-1-1-1", "+1 / +1 / +1"))
LORE_COPY = str(_paths.lore_root() / "tables" / "background-reskins.json")
MAX_LABEL = 100


def default_path(tables=TABLES):
    return os.environ.get("BACKGROUND_RESKINS_PATH") or os.path.join(tables, "background-reskins.json")


def version_path(path):
    return os.path.join(os.path.dirname(path), "background-reskins.version.json")


def kid(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower().replace("'", "")).strip("-")


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def required_ids(tables=TABLES):
    """-> list of dicts {id, kind, parent_id, srd_name, chargen_value}. Everything comes from tables/chargen-5e.json."""
    cg = _load(os.path.join(tables, "chargen-5e.json"))
    out = [{"id": kid(n), "kind": "background", "parent_id": None, "srd_name": n, "chargen_value": n} for n in cg["backgrounds"]]
    out += [{"id": f"feat-{kid(f)}", "kind": "choice", "parent_id": "origin-feat", "srd_name": f, "chargen_value": f} for f in cg["origin_feats"]]
    out += [{"id": i, "kind": "choice", "parent_id": "background-asi", "srd_name": v, "chargen_value": v} for i, v in ASI]
    pk = sorted({p["id"] for b in cg["backgrounds"].values() for p in b.get("packages", [])})
    out += [{"id": f"package-{kid(p)}", "kind": "choice", "parent_id": "background-kit", "srd_name": f"Package {p}", "chargen_value": p} for p in pk]
    return out


def sha256_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def check_hash(path):
    """-> (status, message): ok | warn (no version file) | fail | absent."""
    if not os.path.exists(path):
        return "absent", f"{path} is not in place (not delivered/approved yet): backgrounds show the plain 5e names"
    v = version_path(path)
    if not os.path.exists(v):
        return "warn", "background-reskins.version.json not found next to the table; cannot verify the hash"
    try:
        vd = _load(v)
        want = vd["sha256"]
    except (OSError, ValueError, KeyError) as e:
        return "fail", f"cannot read sha256 from the version file: {e}"
    got = sha256_of(path)
    if got != want:
        return "fail", f"background-reskins.json sha256 {got[:12]} does not match the version file {str(want)[:12]}: a stale or edited copy? Re-copy Lore's file and version file together"
    return "ok", f"background-reskins.json matches the version file ({want[:12]}, v{vd.get('version', '?')})"


def set_flag(on, session=None, campaign=CAMPAIGN):
    """Write create.background_reskin into the session's session.json (alpha: sessions/session.json). Config only; no state or ledger."""
    sid = session or os.environ.get("DCC_SESSION") or "alpha"
    d = os.path.join(campaign, "sessions") if sid == "alpha" else os.path.join(campaign, "sessions-data", sid)
    p = os.path.join(d, "session.json")
    data = _load(p) if os.path.exists(p) else {}
    data.setdefault("create", {})["background_reskin"] = bool(on)
    os.makedirs(d, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
    return p


def check(path=None, tables=TABLES):
    path = path or default_path(tables)
    st, msg = check_hash(path)
    rep = {"path": path, "hash": {"status": st, "message": msg}, "errors": [], "warnings": [], "missing": [], "extra": [], "required": 0, "covered": 0, "entry_count": 0}
    if st == "absent":
        return rep
    err, warn = rep["errors"].append, rep["warnings"].append
    try:
        data = _load(path)
    except ValueError as e:
        err(f"not valid JSON: {e}")
        return rep
    raw = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(raw, list):
        err("entries must be a list")
        return rep
    by, seen = {}, set()
    for e in raw:
        if not isinstance(e, dict) or not isinstance(e.get("id"), str) or not e["id"]:
            err(f"entry without an id: {str(e)[:60]}")
            continue
        i = e["id"]
        if i in seen:
            err(f"{i}: duplicate id")
        seen.add(i)
        by.setdefault(i, e)
        rep["entry_count"] += 1
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", i):
            err(f"{i}: id must be lower-case kebab-case")
        if e.get("kind") not in KINDS:
            err(f"{i}: kind must be one of {KINDS}")
        if e.get("kind") == "choice" and e.get("parent_id") not in PARENTS:
            err(f"{i}: a choice needs parent_id one of {PARENTS}")
        if e.get("kind") == "background" and e.get("parent_id") is not None:
            err(f"{i}: a background has parent_id null")
        for k in ("srd_name", "display_name", "combined_label", "flavor", "chargen_value"):
            if not isinstance(e.get(k), str) or not e[k].strip():
                err(f"{i}: {k} must be a non-empty string")
        cl, dn = e.get("combined_label"), e.get("display_name")
        if isinstance(dn, str) and ("(" in dn or ")" in dn):
            err(f"{i}: display_name must not contain parentheses (a label would nest them)")
        if isinstance(cl, str) and isinstance(dn, str) and not (cl.startswith(f"{dn} (") and cl.endswith(")")):
            err(f"{i}: combined_label should be 'display_name (5e Name)'")
        if isinstance(cl, str):
            if re.search(r"\(.*\(", cl):
                err(f"{i}: nested parentheses in combined_label ({cl}); use label_name for a 5e name that has its own parentheses")
            if len(cl) > MAX_LABEL:
                warn(f"{i}: combined_label is {len(cl)} characters; the bridge cuts it to {MAX_LABEL} (a Discord select label limit)")
        if isinstance(e.get("flavor"), str) and len(e["flavor"].split()) > 30:
            warn(f"{i}: flavor is over 30 words")
        if re.search(r"champ", json.dumps(e, ensure_ascii=False), re.I):
            err(f"{i}: players are Crawlers, never champs")
        for bad in ("value", "state", "ledger", "rules", "asi", "feat", "skills", "tool", "items", "gp", "packages"):
            if bad in e:
                err(f"{i}: field {bad!r} does not belong in a display-only table (ids and rules stay 5e)")
    need = required_ids(tables)
    rep["required"] = len(need)
    for r in need:
        got = by.get(r["id"])
        if got is None:
            rep["missing"].append(r["id"])
            continue
        rep["covered"] += 1
        if got.get("kind") != r["kind"] or (got.get("parent_id") or None) != r["parent_id"]:
            err(f"{r['id']}: should be kind {r['kind']!r} parent_id {r['parent_id']!r}, got {got.get('kind')!r} {got.get('parent_id')!r}")
        if got.get("chargen_value") != r["chargen_value"]:
            err(f"{r['id']}: chargen_value {got.get('chargen_value')!r} is not the exact chargen string {r['chargen_value']!r}")
        if str(got.get("srd_name", "")).lower() != r["srd_name"].lower():
            err(f"{r['id']}: srd_name {got.get('srd_name')!r} differs from the 5e name {r['srd_name']!r}")
        lab = got.get("label_name") or got.get("srd_name")
        if isinstance(got.get("display_name"), str) and got.get("combined_label") != f"{got['display_name']} ({lab})":
            err(f"{r['id']}: combined_label should be '{got['display_name']} ({lab})'")
    known = {r["id"] for r in need}
    rep["extra"] = sorted(i for i in by if i not in known)
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description="Background reskins: ids, coverage, hash")
    ap.add_argument("--ids", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--path")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--enable", action="store_true", help="set create.background_reskin true in the session's session.json")
    ap.add_argument("--disable", action="store_true", help="set it false")
    ap.add_argument("--session")
    a = ap.parse_args(argv)
    if a.enable or a.disable:
        print("wrote", set_flag(a.enable, a.session), "create.background_reskin =", str(a.enable).lower())
        return 0
    if a.ids:
        req = required_ids()
        if a.json:
            print(json.dumps(req, indent=1))
        else:
            for k in KINDS:
                rows = [r for r in req if r["kind"] == k]
                print(f"[{k}] {len(rows)}")
                for r in rows:
                    print(f"  {r['id']}\t{r['chargen_value']}")
            print(f"total {len(req)}")
        return 0
    rep = check(path=a.path)
    if a.json:
        print(json.dumps(rep, indent=1))
    else:
        print(f"{rep['hash']['status'].upper()}: {rep['hash']['message']}")
        if rep["hash"]["status"] != "absent":
            print(f"coverage: {rep['covered']}/{rep['required']} required ids have an entry ({rep['entry_count']} entries)")
        for e in rep["errors"]:
            print("ERROR:", e)
        for w in rep["warnings"]:
            print("WARN:", w)
        if rep["extra"]:
            print("INFO: entries not matching a chargen id (not shown) (kept, unused):", ", ".join(rep["extra"]))
        if a.strict:
            for m in rep["missing"]:
                print("MISSING:", m)
    bad = rep["hash"]["status"] == "fail" or bool(rep["errors"]) or (a.strict and rep["hash"]["status"] != "absent" and bool(rep["missing"]))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
