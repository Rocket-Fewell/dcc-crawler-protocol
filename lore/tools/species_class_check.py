#!/usr/bin/env python3
"""Validates tables/species-class-reskins.json (schema species-class-reskins/0.1.0).
Checks structure, uniqueness, tone rules, and COVERAGE against the campaign's chargen-5e.json and rules/30-species-supplement-5e.md (read only).
With no argument it also verifies the file's sha256 against tables/species-class-reskins.version.json.
Usage: python3 tools/species_class_check.py [path]     Exit 0 = no errors."""
import json, os, re, sys, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "..", "tables")
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(T, "species-class-reskins.json")
VER = os.path.join(T, "species-class-reskins.version.json")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parent))
from paths import CHARGEN as _CH, SPECIES_SUPP as _SUP
CHARGEN = str(_CH) if _CH else ""
SUPP = str(_SUP) if _SUP else ""
REQ = ["id", "kind", "parent_id", "srd_name", "display_name", "combined_label", "nation", "flavor", "spoken"]
KINDS = ["species", "species_variant", "species_lineage", "class", "class_option"]
errs, warns, infos = [], [], []
E = errs.append; W = warns.append; I = infos.append
def kid(s): return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "")).strip("-")

d = json.load(open(P, encoding="utf-8"))
if d.get("schema") != "species-class-reskins/0.1.0": E("schema should be species-class-reskins/0.1.0")
ents = d.get("entries", []); by = {e.get("id"): e for e in ents}
for k, n in collections.Counter(e.get("id") for e in ents).items():
    if n > 1: E("duplicate id %s x%d" % (k, n))
for k, n in collections.Counter(e.get("combined_label", "").lower() for e in ents).items():
    if n > 1: E("duplicate combined_label %r x%d" % (k, n))
for k, n in collections.Counter(e.get("display_name", "").lower() for e in ents if e.get("kind") in ("class", "class_option")).items():
    if n > 1: E("duplicate class display_name %r x%d" % (k, n))
nat = collections.Counter(e["nation"] for e in ents if e.get("kind") in ("species", "species_lineage", "species_variant"))
for k, n in nat.items():
    if n > 1: E("nationality %s used by %d entries (species, lineage and variant nations must be unique)" % (k, n))
last = -1
for e in ents:
    i = e.get("id", "?")
    for k in REQ:
        if k not in e: E("%s: missing field %s" % (i, k))
    for bad in ("tone_risk", "alt_display_name"):
        if bad in e: E("%s: field %s was dropped (Caleb, 2026-10-04)" % (i, bad))
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", i): E("%s: id not kebab-case" % i)
    if e.get("kind") not in KINDS: E("%s: bad kind" % i); continue
    k = KINDS.index(e["kind"])
    if k < last: E("%s: entries not sorted by kind" % i)
    last = max(last, k)
    dn, sn = e.get("display_name", ""), e.get("srd_name", "")
    if e.get("combined_label") != "%s (%s)" % (dn, e.get("label_name", sn)): E("%s: combined_label should be 'Display (5e Name)'" % i)
    if e.get("combined_label", "").count("(") != 1: E("%s: combined_label must have exactly one pair of parentheses" % i)
    if not dn or len(dn) > 60: E("%s: display_name empty or > 60 chars" % i)
    if sn.lower() in dn.lower() and e["kind"] in ("species", "class") and False: pass
    if len(e.get("flavor", "").split()) > 30 or not e.get("flavor"): E("%s: flavor empty or > 30 words" % i)
    if not e.get("spoken"): E("%s: spoken empty" % i)
    blob = json.dumps(e, ensure_ascii=False)
    if re.search(r"champ", blob, re.I): E("%s: contains the banned word" % i)
    if re.search(r"\bHOLD\b", blob): E("%s: contains capitalised HOLD" % i)
    if re.search(r"slur|lazy|dirty|savage|primitive", e.get("flavor", ""), re.I): E("%s: flavor trips the stereotype word list" % i)
    if e["kind"] in ("species", "species_lineage", "species_variant") and not e.get("nation"): E("%s: nation required" % i)
    if e["kind"] in ("species", "species_lineage", "species_variant"):
        if dn != e.get("nation"): E("%s: display_name must be just the nationality (%r)" % (i, e.get("nation")))
        if not e.get("long_name") or len(e["long_name"]) > 60: E("%s: long_name required (<= 60 chars)" % i)
        if e.get("long_label") != "%s (%s)" % (e.get("long_name"), sn): E("%s: long_label should be 'long_name (5e Name)'" % i)
        if re.search(r"champ", json.dumps(e.get("long_name", "")) , re.I): E("%s: long_name contains the banned word" % i)
    if e["kind"] in ("class", "class_option") and e.get("nation") is not None: E("%s: classes have nation null" % i)
    if e["kind"] in ("species_lineage", "species_variant"):
        b = e.get("base_id")
        if not b: E("%s: base_id missing" % i)
        elif b not in by or by[b].get("kind") != "species": E("%s: base_id %r is not a known species id" % (i, b))
        elif b != e.get("parent_id"): E("%s: base_id %r != parent_id %r" % (i, b, e.get("parent_id")))
        if e["kind"] == "species_variant":
            if e.get("rules_entry") is not False or not e.get("rules_note"): E("%s: variant needs rules_entry false and a rules_note" % i)
        elif e.get("rules_entry") is not True or not e.get("chargen_value"): E("%s: lineage needs rules_entry true and chargen_value" % i)
    elif "base_id" in e: E("%s: base_id only on lineages and variants" % i)
    if e["kind"] in ("species_lineage", "species_variant", "class_option"):
        p = by.get(e.get("parent_id"))
        if not p: E("%s: parent_id %r not found" % (i, e.get("parent_id")))
        elif e["kind"] in ("species_lineage", "species_variant") and p["kind"] != "species": E("%s: parent must be a species" % i)
        elif e["kind"] == "class_option" and p["kind"] != "class": E("%s: class_option parent must be a class" % i)
        if not i.startswith(e.get("parent_id", "?") + "-"): E("%s: id should start with '<parent>-'" % i)
    elif e.get("parent_id") is not None: E("%s: parent_id only on lineages, variants and options" % i)

# canon sub-types not named in a rules/30 heading (ledger R-004 Caprid, R-049/rules 4.7 Lajabless phases, R-050 Nodling heads)
CANON_VARIANTS = {"caprid": ["Small Caprid", "Large Dark Caprid"], "lajabless": ["Radiant Phase", "Skull Phase"],
                  "nodling": ["Two-Headed Nodling", "Three-Headed Nodling", "Four-Headed Nodling", "Five-Headed Nodling", "Six-Headed Nodling"]}
# ---- coverage against chargen-5e.json (species, lineages, classes, class options)
need = []   # (id, label)
if os.path.exists(CHARGEN):
    c = json.load(open(CHARGEN, encoding="utf-8"))
    for sp, v in c["species"].items():
        need.append((kid(sp), "chargen species " + sp))
        for o in (v.get("sub") or {}).get("options", []):
            base = {"Dragonborn": o + " Dragonborn", "Elf": o, "Gnome": o if "Gnome" in o else o + " Gnome", "Goliath": o + " Goliath", "Tiefling": o + " Tiefling"}[sp]
            need.append((kid(sp + "-" + o.replace(" Elf", "").replace(" Gnome", "")), "chargen %s lineage %s" % (sp, o), base))
    for cl, v in c["classes"].items():
        need.append((kid(cl), "chargen class " + cl))
        for ch in v.get("choices", []):
            if ch["key"] in ("divine_order", "primal_order"):
                for o in ch["options"]: need.append((kid(cl + "-" + o), "chargen %s %s" % (cl, o), "%s (%s)" % (o, ch["label"])))
else: W("chargen-5e.json not found: coverage vs /create skipped")
if os.path.exists(CHARGEN):
    for e in ents:
        if e.get("kind") == "species_lineage":
            opts = ((c["species"].get(e.get("base_id"), c["species"].get(str(e.get("base_id")).capitalize(), {})) or {}).get("sub") or {}).get("options", [])
            sp = {k.lower(): k for k in c["species"]}.get(e.get("base_id"))
            opts = ((c["species"].get(sp) or {}).get("sub") or {}).get("options", [])
            if e.get("chargen_value") not in opts: E("%s: chargen_value %r is not an option of %s in chargen-5e.json" % (e["id"], e.get("chargen_value"), sp))
for sp_, vs_ in CANON_VARIANTS.items():
    for v_ in vs_: need.append((kid(sp_ + "-" + v_.replace(" Caprid", "").replace(" Phase", "").replace(" Nodling", "")), "canon %s variant %s" % (sp_, v_), v_))
supp = []
if os.path.exists(SUPP):
    heads = re.findall(r"^### 4\.\d+ ([A-Za-z]+)(?: \(([^)]*)\))?", open(SUPP, encoding="utf-8").read(), re.M)
    supp = [h[0] for h in heads]
    for sp_, par in heads:
        if "/" in par:
            for v_ in [x.strip() for x in par.split("/")]:
                need.append((kid(sp_ + "-" + v_), "supplement %s variant %s" % (sp_, v_), v_))
    supp = [s for s in supp if s != "Common"]
    # decision 036 Offer options: rules/30 section 4A ("### 4A.N Name", names may have spaces)
    for nm in re.findall(r"^### 4A\.\d+ ([A-Za-z][A-Za-z ]*?)\s*(?:\(|$)", open(SUPP, encoding="utf-8").read(), re.M):
        supp.append(nm.strip())
    if "Fairy" in supp:
        for v_ in ("Sprite", "Wisteria Fairy"): need.append((kid("fairy-" + v_.replace(" Fairy", "")), "decision 036 Fairy subrace " + v_, v_))
    for s in supp: need.append((kid(s), "supplement species " + s))
else: W("species supplement not found: supplement coverage skipped")
missing = 0
for n in need:
    if n[0] not in by: E("coverage: no entry for id %s (%s)" % (n[0], n[1])); missing += 1
    elif len(n) > 2 and by[n[0]]["srd_name"].lower() != n[2].lower(): E("coverage: %s srd_name %r should be %r" % (n[0], by[n[0]]["srd_name"], n[2]))
nsp = sum(1 for e in ents if e.get("kind") == "species")
if os.path.exists(CHARGEN) and nsp != len(c["species"]) + len(supp): E("species count %d != chargen %d + supplement %d" % (nsp, len(c["species"]), len(supp)))
for e in ents:
    if (e["id"], ) and e["id"] not in {n[0] for n in need} and need: I("entry %s is not in chargen/supplement (extra)" % e["id"])
I("coverage: %d required ids, %d missing; species %d (expect 26), lineages %d, variants %d, classes %d, class options %d" % (len(need), missing, nsp, sum(e["kind"] == "species_lineage" for e in ents), sum(e["kind"] == "species_variant" for e in ents), sum(e["kind"] == "class" for e in ents), sum(e["kind"] == "class_option" for e in ents)))
# ---- hash discipline (only on the live file)
if len(sys.argv) == 1:
    if not os.path.exists(VER): E("species-class-reskins.version.json missing")
    else:
        v = json.load(open(VER, encoding="utf-8"))
        sha = hashlib.sha256(open(P, "rb").read()).hexdigest()
        if sha != v["sha256"]: E("sha256 mismatch: file changed since the last build; run tools/species_class_build.py")
        if v["version"] != d["meta"]["version"]: E("meta.version %s != version file %s" % (d["meta"]["version"], v["version"]))
        if v["entry_count"] != len(ents): E("entry_count mismatch")
print("species-class-reskins: %d entries" % len(ents))
for x in infos: print("INFO:", x)
for x in warns: print("WARN:", x)
for x in errs: print("ERROR:", x)
print("%d errors, %d warnings" % (len(errs), len(warns)))
sys.exit(1 if errs else 0)
