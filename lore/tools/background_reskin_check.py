#!/usr/bin/env python3
"""Validates tables/background-reskins.json (schema background-reskins/0.1.0).
COVERAGE (fails on any missing id): every background in chargen-5e.json, every origin feat, Package A/B, and both ability bonus picks.
With no argument it also verifies the sha256 against tables/background-reskins.version.json.
Usage: python3 tools/background_reskin_check.py [path]    Exit 0 = no errors."""
import json, os, re, sys, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "..", "tables")
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(T, "background-reskins.json")
VER = os.path.join(T, "background-reskins.version.json")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parent))
from paths import CHARGEN as _CH
CHARGEN = str(_CH) if _CH else ""
REQ = ["id", "kind", "parent_id", "srd_name", "display_name", "combined_label", "chargen_value", "flavor"]
GROUPS = {"origin-feat", "background-asi", "background-kit"}
ASI_VALUES = ["+2 / +1", "+1 / +1 / +1"]
errs, warns, infos = [], [], []
E = errs.append; W = warns.append; I = infos.append
def kid(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
d = json.load(open(P, encoding="utf-8"))
if d.get("schema") != "background-reskins/0.1.0": E("schema should be background-reskins/0.1.0")
ents = d.get("entries", []); by = {e.get("id"): e for e in ents}
for k, n in collections.Counter(e.get("id") for e in ents).items():
    if n > 1: E("duplicate id %s x%d" % (k, n))
for k, n in collections.Counter(e.get("combined_label", "").lower() for e in ents).items():
    if n > 1: E("duplicate combined_label %r x%d" % (k, n))
for k, n in collections.Counter(e.get("display_name", "").lower() for e in ents).items():
    if n > 1: E("duplicate display_name %r x%d" % (k, n))
for k, n in collections.Counter((e.get("kind"), e.get("chargen_value")) for e in ents).items():
    if n > 1: E("duplicate (kind, chargen_value) %r x%d" % (k, n))
last = -1
for e in ents:
    i = e.get("id", "?")
    for k in REQ:
        if k not in e: E("%s: missing field %s" % (i, k))
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", i): E("%s: id not kebab-case" % i)
    if e.get("kind") not in ("background", "choice"): E("%s: bad kind" % i); continue
    k = ["background", "choice"].index(e["kind"])
    if k < last: E("%s: not sorted by kind" % i)
    last = max(last, k)
    dn, sn, cl = e.get("display_name", ""), e.get("srd_name", ""), e.get("combined_label", "")
    if cl != "%s (%s)" % (dn, e.get("label_name", sn)): E("%s: combined_label should be 'Display (5e Name)'" % i)
    if cl.count("(") != 1 or cl.count(")") != 1: E("%s: combined_label must have exactly one pair of parentheses" % i)
    if not dn or len(dn) > 60: E("%s: display_name empty or > 60 chars" % i)
    fl = e.get("flavor", "")
    if not fl or len(fl.split()) > 35: E("%s: flavor empty or > 35 words" % i)
    blob = json.dumps(e, ensure_ascii=False)
    if re.search(r"champ", blob, re.I): E("%s: contains the banned word" % i)
    if re.search(r"\bHOLD\b", blob): E("%s: contains capitalised HOLD" % i)
    if re.search(r"\bcash\b|\bboxe?s?\b", dn + " " + cl + " " + fl, re.I): E("%s: never 'cash' or 'box' in names or flavor (Syndicate; credits, and boxes are loot)" % i)
    if e["kind"] == "background":
        if e.get("parent_id") is not None: E("%s: background parent_id must be null" % i)
        if i != kid(e.get("chargen_value", "")): E("%s: id should be the kebab-case chargen key" % i)
    else:
        if e.get("parent_id") not in GROUPS: E("%s: choice parent_id must be one of %s" % (i, sorted(GROUPS)))
# ---- coverage vs chargen-5e.json (fails on any missing id)
if os.path.exists(CHARGEN):
    c = json.load(open(CHARGEN, encoding="utf-8"))
    need = []
    for b in c["backgrounds"]: need.append(("background", b, kid(b)))
    for f in c["origin_feats"]: need.append(("choice", f, "feat-" + kid(f)))
    pk = sorted({p["id"] for b in c["backgrounds"].values() for p in b["packages"]})
    for p in pk: need.append(("choice", p, "package-" + p.lower()))
    for a in ASI_VALUES: need.append(("choice", a, "asi-" + a.replace("+", "").replace(" / ", "-")))
    miss = 0
    for kind, val, i in need:
        e = by.get(i)
        if not e: E("coverage: no entry for %s %r (expected id %s)" % (kind, val, i)); miss += 1
        elif e.get("kind") != kind or e.get("chargen_value") != val: E("coverage: %s should be kind %s chargen_value %r" % (i, kind, val))
        elif kind == "background" and e.get("srd_name") != val: E("%s: srd_name should be %r" % (i, val))
    known = {n[2] for n in need}
    for e in ents:
        if e["id"] not in known: W("%s is not in chargen-5e.json (extra)" % e["id"])
    nb = sum(1 for e in ents if e.get("kind") == "background")
    if nb != len(c["backgrounds"]): E("background count %d != chargen %d" % (nb, len(c["backgrounds"])))
    I("coverage: %d required ids, %d missing; backgrounds %d (expect 16), origin feats %d, packages %d, ASI picks %d" % (len(need), miss, nb, sum(e.get("parent_id") == "origin-feat" for e in ents), sum(e.get("parent_id") == "background-kit" for e in ents), sum(e.get("parent_id") == "background-asi" for e in ents)))
else: W("chargen-5e.json not found: coverage skipped")
if len(sys.argv) == 1:
    if not os.path.exists(VER): E("background-reskins.version.json missing")
    else:
        v = json.load(open(VER, encoding="utf-8"))
        if hashlib.sha256(open(P, "rb").read()).hexdigest() != v["sha256"]: E("sha256 mismatch: file changed since the last build; run tools/background_reskin_build.py")
        if v["version"] != d["meta"]["version"]: E("meta.version %s != version file %s" % (d["meta"]["version"], v["version"]))
        if v["entry_count"] != len(ents): E("entry_count mismatch")
print("background-reskins: %d entries" % len(ents))
for x in infos: print("INFO:", x)
for x in warns: print("WARN:", x)
for x in errs: print("ERROR:", x)
print("%d errors, %d warnings" % (len(errs), len(warns)))
sys.exit(1 if errs else 0)
