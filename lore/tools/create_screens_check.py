#!/usr/bin/env python3
"""Validates tables/create-screens-reskins.json (schema create-screens-reskins/0.1.0) and tables/create-flow-lines.proposed.json.
COVERAGE (fails on any missing id/key):
  chargen-5e.json: the 6 abilities, the 3 ability methods, every package id (A/B/C), every class choice group, every option of the
  non-weapon choices (fighting style, invocation), the divine/primal order options (must exist in species-class-reskins.json), the S11 spell
  select labels for every caster shape, and an audit row for skills/tools/languages/spell names.
  create-flow-lines.json: every key is either rewritten (and listed as flavored) or listed as left vanilla; rewritten keys keep the same
  {placeholders}, every number, <= 3 variants; unchanged keys are byte-identical; survey is identical.
With no argument it also verifies sha256s against tables/create-screens-reskins.version.json.
Usage: python3 tools/create_screens_check.py [--stage main.json lines.json]    Exit 0 = no errors."""
import json, os, re, sys, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import create_screens_data as D
T = os.path.join(HERE, "..", "tables")
STAGE = "--stage" in sys.argv
if STAGE: MAIN, LINES = sys.argv[sys.argv.index("--stage") + 1], sys.argv[sys.argv.index("--stage") + 2]
else: MAIN, LINES = os.path.join(T, "create-screens-reskins.json"), os.path.join(T, "create-flow-lines.proposed.json")
VER = os.path.join(T, "create-screens-reskins.version.json"); AUDIT = os.path.join(T, "create-screens-reskins.audit.md")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parent))
from paths import CHARGEN as _CH, CREATE_FLOW_LINES as _ORIG
CHARGEN = str(_CH) if _CH else ""
ORIG = str(_ORIG) if _ORIG else ""
SC = os.path.join(T, "species-class-reskins.json")
errs, warns, infos = [], [], []; E = errs.append; W = warns.append; I = infos.append
PH = re.compile(r"\{[a-z_]+\}")
def kid(s): return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "")).strip("-")
def nums(s): return set(re.findall(r"\d+", PH.sub("", s)))
d = json.load(open(MAIN, encoding="utf-8"))
if d.get("schema") != "create-screens-reskins/0.1.0": E("schema should be create-screens-reskins/0.1.0")
ents = d.get("entries", []); by = {e.get("id"): e for e in ents}
for k, n in collections.Counter(e.get("id") for e in ents).items():
    if n > 1: E("duplicate id %s x%d" % (k, n))
labels = [e for e in ents if e.get("state") == "label"]
for k, n in collections.Counter(e["combined_label"].lower() for e in labels).items():
    if n > 1: E("duplicate combined_label %r x%d" % (k, n))
for k, n in collections.Counter(e["display_name"].lower() for e in labels).items():
    if n > 1: E("duplicate display_name %r x%d" % (k, n))
LIM = {"button": 80, "select_label": 100, "modal_title": 45, "field_label": 45, "title": 100}
REQ = ["id", "screen", "kind", "old", "new", "placeholders", "old_placeholders", "code_ref", "source_match", "needs_code", "state"]
for e in ents:
    i = e.get("id", "?")
    for k in REQ:
        if k not in e: E("%s: missing field %s" % (i, k))
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", i): E("%s: id not kebab-case" % i)
    if e.get("screen") not in D.SCREENS: E("%s: bad screen %r" % (i, e.get("screen")))
    if e.get("source_match") not in ("found", "not_found", "no_source"): E("%s: bad source_match" % i)
    blob = json.dumps(e, ensure_ascii=False)
    if re.search(r"champ", blob, re.I): E("%s: contains the banned word" % i)
    if re.search(r"\bHOLD\b", blob): E("%s: contains capitalised HOLD" % i)
    old, new = e.get("old", ""), e.get("new", "")
    if not new or new == old: E("%s: new text empty or unchanged" % i)
    if set(PH.findall(new)) != set(e.get("placeholders", [])): E("%s: placeholders in new %s != declared %s" % (i, sorted(set(PH.findall(new))), e.get("placeholders")))
    if set(PH.findall(old)) != set(e.get("old_placeholders", [])): E("%s: placeholders in old %s != declared %s" % (i, sorted(set(PH.findall(old))), e.get("old_placeholders")))
    if nums(old) != nums(new): E("%s: numbers changed: old %s new %s" % (i, sorted(nums(old)), sorted(nums(new))))
    if e.get("state") == "label":
        if e.get("kind") not in D.LABEL_KINDS: E("%s: bad label kind" % i); continue
        cl, dn, sn = e.get("combined_label", ""), e.get("display_name", ""), e.get("srd_name", "")
        if cl != "%s (%s)" % (dn, sn): E("%s: combined_label should be 'Display (5e Name)'" % i)
        if cl.count("(") != 1 or cl.count(")") != 1: E("%s: combined_label must have exactly one pair of parentheses" % i)
        if not new.startswith(cl): E("%s: new text must start with the combined label" % i) if i != "select-s10-kit" else None
        if i == "select-s10-kit" and cl not in new: E("%s: new must contain the combined label" % i)
        if sn.lower() not in old.lower(): E("%s: old text should contain the 5e name" % i)
        if not e.get("flavor") or len(e["flavor"].split()) > 35: E("%s: flavor missing or > 35 words" % i)
        lim = LIM.get(e["kind"]) 
        if lim and len(new) > lim: E("%s: new text %d chars > Discord limit %d" % (i, len(new), lim))
        if e["kind"] == "choice_option" and len(new) > 100: E("%s: option label > 100" % i)
    else:
        if e.get("kind") not in D.TEXT_KINDS: E("%s: bad text kind" % i)
# ---- v0.1.2 audit rules (Syndicate F1-F12)
BARE = {"Factory Preset": "Standard array", "Layaway Plan": "Point buy", "Dice Gamble": "Roll"}
GAP_IDS = ["button-help", "button-resume", "dialog-restart-no", "dialog-cancel-body", "notice-fix-screen", "notice-benched", "notice-party-full",
           "hint-embed-footer", "hint-s8-kept", "hint-s10-describe", "notice-s10-need-class-bg", "hint-money-gp", "hint-money-cp"]
for g in GAP_IDS:
    if g not in by: E("coverage gap row missing: %s" % g)
def bare_check(i, txt):
    for nm, five in BARE.items():
        for m in re.finditer(re.escape(nm), txt):
            if not txt[m.end():].startswith(" (" + five + ")"): E("%s: bare method name %r without ' (%s)' (F9)" % (i, nm, five)); break
for e in ents:
    i, new = e["id"], e["new"]
    if e["state"] == "text": bare_check(i, new)
    if re.search(r"\bcash\b", new + e.get("flavor", ""), re.I): E("%s: use credits, never cash" % i)
    if re.search(r"\b(GP|cp)\b", new): E("%s: money unit GP/cp in new text; use credits" % i)
    if re.search(r"burn", new + e.get("flavor", ""), re.I): E("%s: 'burn' is banned (Restart and Cancel build must differ, F10)" % i)
    if re.search(r"binder", new + e.get("flavor", ""), re.I): E("%s: spellbook is the Cracked Phone App everywhere (F8)" % i)
    if e["screen"] == "S10" and re.search(r"\bboxe?s?\b", new + e.get("flavor", ""), re.I): E("%s: no 'box' on S10 (collides with loot boxes, F3)" % i)
    if e["screen"] == "ALL" and e.get("plain_on") != D.PLAIN_VIEWS: E("%s: ALL rows must carry plain_on %s (F2)" % (i, D.PLAIN_VIEWS))
    if e["screen"] != "ALL" and "plain_on" in e: E("%s: plain_on only on ALL rows" % i)
    if e["screen"] in ("S2", "S13"): E("%s: S2 and S13 stay plain (F2)" % i)
for must in ("hint-s8-method-line", "select-s8-assign"):
    if must in by and "needs_code_detail" not in by[must]: E("%s: renamed placeholder needs needs_code_detail (F5)" % must)
if "title-s16" in by and by["title-s16"]["old"] != "Review (the full sheet)": E("title-s16: old must be 'Review (the full sheet)' (drift guard, F4)")
if "help-s16" in by and "Sign ▸ (Confirm ▸)" not in by["help-s16"]["new"]: E("help-s16: must point at the Sign ▸ (Confirm ▸) button (F4)")
if "package-gold" in by and "packages[B]" not in str(by["package-gold"].get("chargen_ref")): E("package-gold: chargen_ref must name packages[B] (F3)")
for must in ("plain-views", "titles-s13-s15", "modal-and-field-labels", "money-cp-rule", "embed-header-and-round-header", "rule-statement-messages"):
    if must not in {a["id"] for a in d.get("vanilla_on_purpose", [])}: E("audit: missing row %s" % must)
# ---- coverage vs chargen-5e.json
if os.path.exists(CHARGEN):
    c = json.load(open(CHARGEN, encoding="utf-8")); miss = 0; need = 0
    def req(i, why):
        global miss, need
        need += 1
        if i not in by: E("coverage: no entry %s (%s)" % (i, why)); miss += 1
    for ab, nm in (("str", "Strength"), ("dex", "Dexterity"), ("con", "Constitution"), ("int", "Intelligence"), ("wis", "Wisdom"), ("cha", "Charisma")):
        req("ability-" + ab, "ability " + ab)
        if "ability-" + ab in by and by["ability-" + ab]["srd_name"] != nm: E("ability-%s: srd_name should be %s" % (ab, nm))
    for m in c["ability_methods"]["methods"]: req("method-" + kid(m.replace("_", " ")), "ability method " + m)
    for pid, has_items in sorted({(p["id"], bool(p["items"])) for cl in c["classes"].values() for p in cl["packages"]}):
        req("package-class-" + pid.lower() if has_items else "package-gold", "package %s (%s)" % (pid, "with items" if has_items else "gold option"))
    sc = {x["id"] for x in json.load(open(SC, encoding="utf-8"))["entries"]} if os.path.exists(SC) else set()
    for cn, cl in c["classes"].items():
        for ch in cl.get("choices", []):
            req("choice-" + kid(ch["key"].replace("_", " ")), "%s choice group %s" % (cn, ch["key"]))
            if ch["key"] in ("divine_order", "primal_order"):
                for o in ch["options"]:
                    need += 1
                    if kid(cn + " " + o) not in sc: E("coverage: %s %s option missing from species-class-reskins (%s)" % (cn, ch["key"], kid(cn + " " + o))); miss += 1
            elif ch["key"] not in ("weapon_masteries", "expertise"):
                for o in ch.get("options", []): req("opt-%s-%s" % (kid(ch["key"].replace("_", " ")), kid(o)), "%s option %s" % (ch["key"], o))
    caster = [cl.get("spellcasting") for cl in c["classes"].values() if cl.get("spellcasting")]
    sp = c.get("spells", {})
    shapes = set()
    for v in (sp.values() if isinstance(sp, dict) else []):
        if isinstance(v, dict):
            if v.get("cantrips"): shapes.add("select-s11-cantrips")
            if v.get("spellbook"): shapes.update(["select-s11-spellbook", "select-s11-prepare"])
            if v.get("level1_known"): shapes.add("select-s11-level1")
    if not shapes: shapes = {"select-s11-cantrips", "select-s11-level1", "select-s11-spellbook", "select-s11-prepare"}
    for s in sorted(shapes): req(s, "S11 spell select shape")
    I("coverage vs chargen-5e.json: %d required ids/options, %d missing" % (need, miss))
else: W("chargen-5e.json not found: coverage skipped")
# ---- audit rows for the intentionally plain families
aud = {a["id"] for a in d.get("vanilla_on_purpose", [])}
for must in ("skill-names", "tool-language-names", "spell-names", "weapon-mastery-properties", "ability-abbreviations", "rule-numbers", "roll-log-wording", "item-names"):
    if must not in aud: E("audit: missing vanilla_on_purpose row %s" % must)
for a in d.get("vanilla_on_purpose", []):
    if not a.get("what") or not a.get("why"): E("audit %s: needs what and why" % a.get("id"))
# ---- create-flow-lines coverage
pl = json.load(open(LINES, encoding="utf-8"))
if os.path.exists(ORIG):
    o = json.load(open(ORIG, encoding="utf-8"))
    ok, pk = set(o["lines"]), set(pl["lines"])
    for k in sorted(ok - pk): E("lines: key %s missing from the proposed file" % k)
    for k in sorted(pk - ok): E("lines: extra key %s not in create-flow-lines.json" % k)
    fl = set(d["line_keys"]["flavored"]); left = set(d["line_keys"]["left_vanilla_or_already_flavored"])
    if fl & left: E("lines: keys both flavored and left: %s" % sorted(fl & left))
    for k in sorted(ok - fl - left): E("lines: key %s is neither flavored nor listed as left vanilla" % k)
    for k in sorted((fl | left) - ok): E("lines: %s listed in the audit but not in create-flow-lines.json" % k)
    if sorted(fl) != sorted(pl["meta"].get("changed_keys", [])): E("lines: meta.changed_keys != line_keys.flavored")
    for k in sorted(ok & pk):
        a, b = o["lines"][k], pl["lines"][k]
        if k in fl:
            if a == b: E("lines: %s is listed as flavored but unchanged" % k)
            if not b or len(b) > 3: E("lines: %s must have 1 to 3 variants" % k)
            for v in b:
                if not isinstance(v, str) or not v.strip(): E("lines: %s has an empty variant" % k)
                elif re.search(r"champ", v, re.I) or re.search(r"\bHOLD\b", v): E("lines: %s has a banned word" % k)
                else:
                    pa = set().union(*[set(PH.findall(x)) for x in a]); pb = set(PH.findall(v))
                    if pb != pa: E("lines: %s variant placeholders %s != %s" % (k, sorted(pb), sorted(pa)))
                    bare_check("lines:" + k, v)
                    if re.search(r"burn|\bcash\b|one body per customer", v, re.I) and k != "S10": E("lines: %s has a banned phrase" % k)
                    na = set().union(*[nums(x) for x in a])
                    if not na <= nums(v) or not nums(v) <= na: E("lines: %s variant numbers %s != original %s (rule facts must stay)" % (k, sorted(nums(v)), sorted(na)))
        elif a != b: E("lines: %s should be unchanged" % k)
    if o["survey"] != pl["survey"]: E("lines: survey section must be identical")
    I("create-flow-lines: %d keys, %d rewritten, %d left" % (len(ok), len(fl), len(left)))
else: W("create-flow-lines.json not found: line coverage skipped")
if len(sys.argv) == 1:
    if not os.path.exists(VER): E("create-screens-reskins.version.json missing")
    else:
        v = json.load(open(VER, encoding="utf-8"))
        h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
        if h(MAIN) != v["sha256"]: E("sha256 mismatch for create-screens-reskins.json; run tools/create_screens_build.py")
        if v["version"] != d["meta"]["version"]: E("meta.version %s != version file %s" % (d["meta"]["version"], v["version"]))
        if v["entry_count"] != len(ents): E("entry_count mismatch")
        cp = v.get("companions", {})
        if cp.get("tables/create-flow-lines.proposed.json", {}).get("sha256") != h(LINES): E("sha256 mismatch for create-flow-lines.proposed.json")
        if cp.get("tables/create-screens-reskins.audit.md", {}).get("sha256") != h(AUDIT): E("sha256 mismatch for the audit md")
print("create-screens-reskins: %d entries (%d label rows, %d text rows)" % (len(ents), len(labels), len(ents) - len(labels)))
for x in infos: print("INFO:", x)
for x in warns: print("WARN:", x)
for x in errs: print("ERROR:", x)
print("%d errors, %d warnings" % (len(errs), len(warns)))
sys.exit(1 if errs else 0)
