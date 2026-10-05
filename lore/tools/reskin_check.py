#!/usr/bin/env python3
"""Validates tables/item-reskins.json (schema item-reskins/0.1.0).
Also checks /create coverage against the campaign's chargen-5e.json (read only) and deck reskin-name reuse.
Usage: python3 tools/reskin_check.py   Exit 0 = no errors."""
import json, os, re, sys, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__))
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "tables", "item-reskins.json")
DECKS = os.path.join(HERE, "..", "tables", "loot-decks", "*.json")
CHARGEN = "/workspace/dcc-campaign/tables/chargen-5e.json"
REQ = ["srd_id","srd_name","category","subcategory","display_name","combined_label","snark","source_tag","ledger_ref","name_origin",
       "legacy_names","chargen_keys","floor_variants","base_price","base_price_cp","price_flag","price_note","resolve_to_variant","variants","non_srd","price_credits_proposed","mechanic_note"]
CATS = {"weapon","armor","shield","ammunition","focus","gear","pack","tool"}
errs, warns, infos = [], [], []
E = errs.append; W = warns.append; I = infos.append

d = json.load(open(P, encoding="utf-8"))
if d.get("schema") != "item-reskins/0.1.0": E("schema should be item-reskins/0.1.0")
meta = d.get("meta", {})
ids = meta.get("id_scheme", {})
for k in ("id", "stored_on_sheet", "lookup", "fallback", "prices"):
    if k not in ids: E("meta.id_scheme.%s missing" % k)
if "srd_name" not in ids.get("fallback", ""): E("meta.id_scheme.fallback must mention srd_name")
if "srd_id" not in ids.get("lookup", ""): E("meta.id_scheme.lookup must mention srd_id")
ents = d.get("entries", [])
cnt = collections.Counter(e.get("srd_id") for e in ents)
for k, n in cnt.items():
    if n > 1: E("duplicate srd_id %s x%d" % (k, n))
disp = collections.Counter(e.get("display_name", "").lower() for e in ents)
for k, n in disp.items():
    if n > 1: E("duplicate display_name %r x%d" % (k, n))
names = collections.Counter(e.get("srd_name", "").lower() for e in ents)
for k, n in names.items():
    if n > 1: E("duplicate srd_name %r x%d" % (k, n))
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
deck = {}
for f in glob.glob(DECKS):
    try:
        for c in json.load(open(f, encoding="utf-8")).get("cards", []): deck[c["id"]] = c
    except Exception: pass
chargen = json.load(open(CHARGEN, encoding="utf-8")) if os.path.exists(CHARGEN) else None
last_cat = -1; order = ["weapon","armor","shield","ammunition","focus","gear","pack","tool"]
for e in ents:
    sid = e.get("srd_id", "?")
    for k in REQ:
        if k not in e: E("%s: missing field %s" % (sid, k))
    if not ID_RE.match(sid): E("%s: srd_id not kebab-case" % sid)
    if e.get("category") not in CATS: E("%s: bad category" % sid)
    else:
        i = order.index(e["category"])
        if i < last_cat: E("%s: entries not sorted by category" % sid)
        last_cat = max(last_cat, i)
    dn, sn, cl, sk = e.get("display_name", ""), e.get("srd_name", ""), e.get("combined_label", ""), e.get("snark", "")
    if not dn or not sn: E("%s: empty name" % sid)
    if cl != "%s (%s)" % (dn, sn): E("%s: combined_label should be 'Display (SRD Name)'" % sid)
    if len(dn) > 60: E("%s: display_name > 60 chars" % sid)
    if not sk or len(sk.split()) > 25: E("%s: snark empty or > 25 words" % sid)
    blob = json.dumps(e)
    if re.search(r"champ", blob, re.I): E("%s: contains 'champ'" % sid)
    if re.search(r"\bHOLD\b", blob): E("%s: contains capitalised HOLD" % sid)
    if e.get("source_tag") not in ("HOUSE", "CANON"): E("%s: bad source_tag" % sid)
    if e.get("source_tag") == "CANON" and not e.get("ledger_ref"): E("%s: CANON needs ledger_ref" % sid)
    if e.get("floor_variants") != []: W("%s: floor_variants not empty (reserved)" % sid)
    bp, cpv = e.get("base_price"), e.get("base_price_cp")
    if e.get("resolve_to_variant"):
        vs = [x for x in ents if x.get("subcategory") == e.get("subcategory") and not x.get("resolve_to_variant")]
        if not vs: W("%s: resolve_to_variant but no variant entries" % sid)
        if sorted(e.get("variants", [])) != sorted(x["srd_id"] for x in vs): E("%s: variants list does not match entries in subcategory" % sid)
        for x in vs:
            if x.get("base_price") is None: W("%s: variant %s is unpriced (%s)" % (sid, x["srd_id"], x.get("price_flag")))
        if bp is not None or cpv is not None: E("%s: generic header must have null price" % sid)
        if not e.get("price_flag"): E("%s: generic header needs a price_flag" % sid)
    else:
        if e.get("variants"): E("%s: variants set but resolve_to_variant false" % sid)
        if bp is None and e.get("non_srd"):
            if cpv is not None: E("%s: non_srd with null base_price must have null base_price_cp" % sid)
            if not e.get("price_flag") or not e.get("price_note"): E("%s: non_srd null price needs price_flag and price_note" % sid)
            if not isinstance(e.get("price_credits_proposed"), int) or e["price_credits_proposed"] <= 0: E("%s: non_srd needs price_credits_proposed (positive int)" % sid)
            if e.get("source_tag") != "CANON" or not e.get("ledger_ref"): E("%s: non_srd items must be CANON with a ledger_ref" % sid)
            if "no SRD entry" not in e.get("srd_name", ""): E("%s: non_srd srd_name should say '(canon item, no SRD entry)'" % sid)
        elif bp is None: E("%s: null price on a non-generic entry (only resolve_to_variant headers and non_srd items may be unpriced)" % sid)
        else:
            m = re.fullmatch(r"([\d,]+) (gp|sp|cp)", bp)
            if not m: E("%s: base_price format" % sid)
            elif int(m[1].replace(",", "")) * {"gp":100,"sp":10,"cp":1}[m[2]] != cpv: E("%s: base_price_cp != base_price" % sid)
        if e.get("price_flag") and bp is not None: E("%s: price_flag set but price not null" % sid)
        if not e.get("non_srd") and (e.get("price_credits_proposed") is not None or e.get("mechanic_note")): E("%s: price_credits_proposed / mechanic_note only allowed on non_srd items" % sid)
    o = e.get("name_origin", "")
    if o.startswith("deck:"):
        c = deck.get(o[5:])
        if not c: E("%s: deck card %s not found" % (sid, o[5:]))
        elif c["reskin_name"] != dn: E("%s: display_name differs from deck %s reskin_name %r" % (sid, o[5:], c["reskin_name"]))
    elif o not in ("new", "chargen"): E("%s: bad name_origin" % sid)
    if chargen:
        for k in e.get("chargen_keys", []):
            it = chargen["items"].get(k)
            if not it: E("%s: chargen key %s not in chargen-5e.json" % (sid, k)); continue
            if it["junk"] != dn and it["junk"] not in e.get("legacy_names", []):
                E("%s: chargen junk %r is neither display_name nor in legacy_names" % (sid, it["junk"]))
            if o == "chargen" and it["junk"] != dn and not any(it["junk"] == l for l in e["legacy_names"]):
                E("%s: name_origin chargen but display differs" % sid)
            if bp is not None and it["cost_cp"] != cpv:
                I("price differs: %s chargen-5e.json %s=%d cp vs SRD %s (%d cp). Use SRD." % (sid, k, it["cost_cp"], bp, cpv))

# /create coverage
by_id = {e["srd_id"]: e for e in ents}; by_name = {e["srd_name"].lower(): e for e in ents}
missing, used = [], set()
if chargen:
    for grp in ("classes", "backgrounds"):
        for nm, v in chargen[grp].items():
            for pk in v.get("packages", []):
                for key, _q in pk["items"]:
                    used.add((key, "%s %s pkg %s" % (grp[:-2] if grp == "classes" else "background", nm, pk["id"])))
    keys = sorted({k for k, _ in used})
    for k in keys:
        if not any(k in e["chargen_keys"] for e in ents): missing.append(k)
    tools = set()
    for nm, v in chargen["backgrounds"].items():
        t = v.get("tool")
        if t: tools.add(re.sub(r"^One ", "", t))
    for t in sorted(tools):
        if t.lower() not in by_name and not any(t.lower() == l.lower() for l in by_name): missing.append("background tool: " + t)
    for k, it in chargen["items"].items():
        if not any(k in e["chargen_keys"] for e in ents) and k not in keys: I("chargen item %s (%s) has no reskin entry and is unused by starting packages" % (k, it["name"]))
    I("/create coverage: %d starting-equipment keys used, %d unmapped" % (len(keys), len([m for m in missing if not m.startswith("background")])))
for m in missing: E("/create item has no reskin entry: " + m)

print("item-reskins: %d entries (%s)" % (len(ents), ", ".join("%s %d" % (c, sum(1 for e in ents if e["category"] == c)) for c in order)))
print("generic headers (resolve_to_variant): %s" % ", ".join(e["srd_id"] for e in ents if e["resolve_to_variant"]))
for x in infos: print("INFO:", x)
for x in warns: print("WARN:", x)
for x in errs: print("ERROR:", x)
print("%d errors, %d warnings" % (len(errs), len(warns)))
sys.exit(1 if errs else 0)
