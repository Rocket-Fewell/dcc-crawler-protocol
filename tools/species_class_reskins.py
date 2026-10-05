#!/usr/bin/env python3
"""Coverage + hash check and label lookup for Lore's species/class display names ("Our Name (5e Name)"), the sibling of reskin_check.py.
Owner: Architect (tool) / DCC Lore (the table) | Status: draft | Version: 0.3.0 | Updated: 2026-10-04
Summary: tables/species-class-reskins.json (schema species-class-reskins/0.1.0, entries[] with id, kind, parent_id, srd_name, display_name, combined_label, nation, flavor, spoken) is Lore's file; the campaign copy in tables/ is put in place only after Caleb approves the names. This tool lists every id /create needs (--ids), checks that the copy covers chargen-5e.json and matches its version-file sha256, and gives the publisher a label() that falls back to the plain 5e name (never blank, never an error). Names only: state.json and the ledger keep the plain 5e names.

Usage:
  python3 tools/species_class_reskins.py --enable | --disable [--session ID]   set create.species_class_reskin true/false in that session's session.json (the switch is OFF by default)
  python3 tools/species_class_reskins.py --ids [--json]      every id the table must cover (species, lineages, classes, class options; kind and expected srd_name)
  python3 tools/species_class_reskins.py [--path FILE] [--strict] [--house] [--json]   hash + structure + coverage report
      --path     check another copy (e.g. Lore's lore/tables/species-class-reskins.json); its version file is read from the same folder
      --strict   also exit 1 when any /create id (species, lineage, class, class option) has no entry
      --house    also require the 12 Floor 3 oddities from rules/30 section 4 (21 species in all)
  No table in tables/ = "absent", exit 0. The bridge and publisher show the names only while create.species_class_reskin is true in session.json (default false).
  Variants (kind species_variant, e.g. Felid: Cat, Cat Girl, Tigran, Were-Cat) are display-only; /create offers none. The check fails when a variant/lineage has no base_id, a base_id that is not a
  known species (chargen-5e.json or rules/30), a chargen_value that is not the exact chargen option, a variant that carries a chargen_value or rules_entry true, or when two entries would
  map to the same (base_id, chargen_value) / the same (base_id, srd_name) - anything that could break the S17 recompute, which only ever sees the 5e ids.
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
SCHEMA = "species-class-reskins/0.1.0"
KINDS = ("species", "species_variant", "species_lineage", "class", "class_option")
LORE_COPY = str(_paths.lore_root() / "tables" / "species-class-reskins.json")
MAX_LABEL = 100


def default_path(tables=TABLES):
    return os.environ.get("SPECIES_CLASS_RESKINS_PATH") or os.path.join(tables, "species-class-reskins.json")


def version_path(path):
    return os.path.join(os.path.dirname(path), "species-class-reskins.version.json")


def kid(s):
    """Lore's id rule (dcc-lore tools/species_class_check.py): lower case, apostrophes dropped, runs of non-alphanumerics -> '-'."""
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower().replace("'", "")).strip("-")


def lineage_id(species, option):
    return kid(f"{species}-{str(option).replace(' Elf', '').replace(' Gnome', '')}")


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def house_species(campaign=CAMPAIGN):
    """The Floor 3 oddities: '### 4.N Name' headings of rules/30-species-supplement-5e.md (same rule as Lore's checker)."""
    try:
        text = open(os.path.join(campaign, "rules", "30-species-supplement-5e.md"), encoding="utf-8").read()
    except OSError:
        return []
    return [s for s in re.findall(r"^### 4\.\d+ ([A-Za-z]+)", text, re.M) if s != "Common"]


def required_ids(tables=TABLES, campaign=CAMPAIGN):
    """-> list of dicts {id, kind, srd_name, shown_in_create}. srd_name is what the entry's srd_name must equal (Lore's rule)."""
    cg = _load(os.path.join(tables, "chargen-5e.json"))
    out = []
    for sp, v in cg["species"].items():
        out.append({"id": kid(sp), "kind": "species", "srd_name": sp, "shown_in_create": True})
        for o in (v.get("sub") or {}).get("options", []):
            base = {"Dragonborn": f"{o} Dragonborn", "Elf": o, "Gnome": o if "Gnome" in o else f"{o} Gnome", "Goliath": f"{o} Goliath", "Tiefling": f"{o} Tiefling"}.get(sp, o)
            out.append({"id": lineage_id(sp, o), "kind": "species_lineage", "srd_name": base, "shown_in_create": True, "base_id": kid(sp), "chargen_value": o})
    for cl, v in cg["classes"].items():
        out.append({"id": kid(cl), "kind": "class", "srd_name": cl, "shown_in_create": True})
        for ch in v.get("choices", []):
            if ch["key"] in ("divine_order", "primal_order"):
                for o in ch["options"]:
                    out.append({"id": kid(f"{cl}-{o}"), "kind": "class_option", "srd_name": f"{o} ({ch['label']})", "shown_in_create": True})
    have = {r["id"] for r in out}
    for s in house_species(campaign):
        if kid(s) not in have:
            out.append({"id": kid(s), "kind": "species", "srd_name": s, "shown_in_create": False})
    return out


def entries_by_id(data):
    out = {}
    if isinstance(data, dict) and isinstance(data.get("entries"), list):
        for e in data["entries"]:
            if isinstance(e, dict) and isinstance(e.get("id"), str) and e["id"]:
                out.setdefault(e["id"], e)
    return out


def entry_label(e):
    """combined_label of an entry, or display_name (srd_name), else None. Over 100 characters it cuts the display name, keeping '(5e Name)'."""
    if not isinstance(e, dict):
        return None
    def txt(k):
        return " ".join(e[k].split()) if isinstance(e.get(k), str) else ""
    combined, display, srd = txt("combined_label"), txt("display_name"), txt("srd_name")
    text = combined or (f"{display} ({srd})" if display and srd else display)
    if not text:
        return None
    if len(text) <= MAX_LABEL:
        return text
    return (f"{display[:max(10, MAX_LABEL - len(srd) - 5)]}… ({srd})" if display and srd else text[:MAX_LABEL - 1] + "…")[:MAX_LABEL]


def label(ident, plain_name, data=None, kind=None):
    """'Our Name (5e Name)' from the entry's combined_label, else the plain 5e name. No table in tables/ = plain names. Never blank, never raises."""
    try:
        if data is None:
            p = default_path()
            data = _load(p) if os.path.exists(p) else None
        e = entries_by_id(data).get(ident)
        if e is not None and kind and e.get("kind") != kind:
            e = None   # a wrong-kind entry (e.g. a variant id) is ignored
        return entry_label(e) or str(plain_name)
    except Exception:
        return str(plain_name)


def species_label(name, data=None):
    return label(kid(name), name, data, "species")


def class_label(name, data=None):
    return label(kid(name), name, data, "class")


def sha256_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def check_hash(path):
    """-> (status, message): ok | warn (no version file) | fail | absent."""
    if not os.path.exists(path):
        return "absent", f"{path} is not in place (not approved yet): species and class names show the plain 5e names"
    v = version_path(path)
    if not os.path.exists(v):
        return "warn", "species-class-reskins.version.json not found next to the table; cannot verify the hash"
    try:
        vd = _load(v)
        want = vd["sha256"]
    except (OSError, ValueError, KeyError) as e:
        return "fail", f"cannot read sha256 from the version file: {e}"
    got = sha256_of(path)
    if got != want:
        return "fail", f"species-class-reskins.json sha256 {got[:12]} does not match the version file {str(want)[:12]}: a stale or edited copy? Re-copy Lore's file and version file together"
    return "ok", f"species-class-reskins.json matches the version file ({want[:12]}, v{vd.get('version', '?')})"


def _check_bases(rep, by, tables, campaign):
    """Lineage/variant integrity: everything rules-related resolves through base_id to a 5e species; nothing display-only can reach state or the S17 recompute."""
    err = rep["errors"].append
    cg = _load(os.path.join(tables, "chargen-5e.json"))
    species_ids = {kid(n): n for n in cg["species"]} | {kid(n): n for n in house_species(campaign)}
    seen_cv, seen_name = {}, {}
    for i, e in by.items():
        k = e.get("kind")
        if k not in ("species_lineage", "species_variant"):
            if "base_id" in e and k != "class_option":
                err(f"{i}: base_id is only for lineages and variants")
            continue
        b = e.get("base_id")
        if not isinstance(b, str) or not b:
            err(f"{i}: base_id missing")
            continue
        if b not in species_ids:
            err(f"{i}: base_id {b!r} is not a known species (chargen-5e.json or rules/30)")
        elif by.get(b, {}).get("kind") not in (None, "species"):
            err(f"{i}: base_id {b!r} must be a species entry")
        if e.get("parent_id") not in (None, b):
            err(f"{i}: base_id {b!r} != parent_id {e.get('parent_id')!r}")
        if i == b:
            err(f"{i}: an entry cannot be its own base")
        if k == "species_variant":
            if e.get("chargen_value") is not None:
                err(f"{i}: a variant must not carry a chargen_value (it never reaches /create or state)")
            if e.get("rules_entry") is not False:
                err(f"{i}: a variant must have rules_entry false (display-only, decision 025)")
        else:
            cv = e.get("chargen_value")
            opts = ((cg["species"].get(species_ids.get(b, ""), {}) or {}).get("sub") or {}).get("options", [])
            if cv not in opts:
                err(f"{i}: chargen_value {cv!r} is not an exact chargen-5e.json option for {b} ({opts})")
            key = (b, cv)
            if key in seen_cv:
                err(f"{i}: same (base_id, chargen_value) as {seen_cv[key]}: the S17 recompute could not tell them apart")
            seen_cv[key] = i
        sk = (b, str(e.get("srd_name", "")).lower())
        if sk in seen_name:
            err(f"{i}: same (base_id, srd_name) as {seen_name[sk]}")
        seen_name[sk] = i
    # a variant/lineage id must never collide with a species or class id
    for i, e in by.items():
        if e.get("kind") in ("species_lineage", "species_variant") and (i in species_ids or i in {kid(c) for c in cg["classes"]}):
            err(f"{i}: id collides with a species/class id")


def set_flag(on, session=None, campaign=CAMPAIGN):
    """Write create.species_class_reskin into the session's session.json (alpha: sessions/session.json). Config only; no state or ledger."""
    sid = session or os.environ.get("DCC_SESSION") or "alpha"
    d = os.path.join(campaign, "sessions") if sid == "alpha" else os.path.join(campaign, "sessions-data", sid)
    p = os.path.join(d, "session.json")
    data = _load(p) if os.path.exists(p) else {}
    data.setdefault("create", {})["species_class_reskin"] = bool(on)
    os.makedirs(d, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
    return p


def check(path=None, tables=TABLES, campaign=CAMPAIGN, include_house=False):
    path = path or default_path(tables)
    st, msg = check_hash(path)
    rep = {"path": path, "hash": {"status": st, "message": msg}, "errors": [], "warnings": [], "missing": [], "extra": [], "required": 0, "covered": 0, "entry_count": 0}
    if st == "absent":
        return rep
    try:
        data = _load(path)
    except ValueError as e:
        rep["errors"].append(f"not valid JSON: {e}")
        return rep
    if data.get("schema") != SCHEMA:
        rep["errors"].append(f"schema must be {SCHEMA!r}, got {data.get('schema')!r}")
    raw = data.get("entries")
    if not isinstance(raw, list):
        rep["errors"].append("entries must be a list")
        return rep
    seen = set()
    for e in raw:
        if not isinstance(e, dict) or not isinstance(e.get("id"), str) or not e["id"]:
            rep["errors"].append(f"entry without an id: {str(e)[:60]}")
            continue
        i = e["id"]
        if i in seen:
            rep["errors"].append(f"{i}: duplicate id")
        seen.add(i)
        rep["entry_count"] += 1
        if e.get("kind") not in KINDS:
            rep["errors"].append(f"{i}: kind must be one of {KINDS}")
        for k in ("srd_name", "display_name", "combined_label"):
            if not isinstance(e.get(k), str) or not e[k].strip():
                rep["errors"].append(f"{i}: {k} must be a non-empty string")
        cl, dn = e.get("combined_label"), e.get("display_name")
        if isinstance(cl, str) and isinstance(dn, str) and not (cl.startswith(f"{dn} (") and cl.endswith(")")):
            rep["errors"].append(f"{i}: combined_label should be 'display_name (5e Name)'")
        if isinstance(e.get("combined_label"), str) and len(e["combined_label"]) > MAX_LABEL:
            rep["warnings"].append(f"{i}: combined_label is {len(e['combined_label'])} characters; the bridge cuts it to {MAX_LABEL} (a Discord select label limit)")
        if re.search(r"champ", json.dumps(e, ensure_ascii=False), re.I):
            rep["errors"].append(f"{i}: players are Crawlers, never champs")
        if re.search(r"\(.*\(", str(e.get("combined_label", ""))):
            rep["warnings"].append(f"{i}: nested parentheses in combined_label: {e['combined_label']}")
    by = entries_by_id(data)
    _check_bases(rep, by, tables, campaign)
    need = [r for r in required_ids(tables, campaign) if r["shown_in_create"] or include_house]
    rep["required"] = len(need)
    for r in need:
        e = by.get(r["id"])
        if e is None:
            rep["missing"].append(r["id"])
            continue
        rep["covered"] += 1
        if str(e.get("srd_name", "")).lower() != r["srd_name"].lower():
            rep["warnings"].append(f"{r['id']}: srd_name {e.get('srd_name')!r} differs from the 5e name {r['srd_name']!r}")
    known = {r["id"] for r in required_ids(tables, campaign)}
    rep["extra"] = sorted(i for i in by if i not in known)
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description="Species/class reskins: ids, coverage, hash")
    ap.add_argument("--ids", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--path")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--house", action="store_true")
    ap.add_argument("--enable", action="store_true", help="set create.species_class_reskin true in the session's session.json")
    ap.add_argument("--disable", action="store_true", help="set it false")
    ap.add_argument("--session")
    a = ap.parse_args(argv)
    if a.enable or a.disable:
        print("wrote", set_flag(a.enable, a.session), "create.species_class_reskin =", str(a.enable).lower())
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
                    print(f"  {r['id']}\t{r['srd_name']}\t{'create' if r['shown_in_create'] else 'house (Floor 3, not in /create)'}")
            print(f"total {len(req)}: {sum(r['shown_in_create'] for r in req)} shown in /create + {sum(not r['shown_in_create'] for r in req)} house species")
        return 0
    rep = check(path=a.path, include_house=a.house)
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
            print("INFO: entries not in chargen/supplement (kept, unused):", ", ".join(rep["extra"]))
        if a.strict:
            for m in rep["missing"]:
                print("MISSING:", m)
        if rep["hash"]["status"] != "absent" and os.path.exists(LORE_COPY) and not a.path and os.path.exists(default_path()):
            if sha256_of(LORE_COPY) != sha256_of(default_path()):
                print("WARN: the tables/ copy differs from Lore's current file (re-copy the table and version file together once Caleb approves the change)")
    bad = rep["hash"]["status"] == "fail" or bool(rep["errors"]) or (a.strict and rep["hash"]["status"] != "absent" and bool(rep["missing"]))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
