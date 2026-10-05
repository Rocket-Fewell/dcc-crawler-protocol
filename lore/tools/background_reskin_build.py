#!/usr/bin/env python3
"""Builds tables/background-reskins.json (+ .version.json and a CHANGELOG line) from background_reskin_data.py.
Display-name layer for the /create S7 'Prior Employment' screen. Same discipline as species_class_build.py:
stage, check the stage, then write JSON, version file (version, sha256, diff) and changelog.
Usage: python3 tools/background_reskin_build.py [--note "text"]   (patch version bumps on every build)"""
import json, os, sys, hashlib, datetime, subprocess, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import background_reskin_data as D
OUT = os.path.join(HERE, "..", "tables")
JSON_PATH = os.path.join(OUT, "background-reskins.json")
VER_PATH = os.path.join(OUT, "background-reskins.version.json")
LOG_PATH = os.path.join(OUT, "background-reskins.CHANGELOG.md")
CHARGEN = "/workspace/dcc-campaign/tables/chargen-5e.json"
NOTE = sys.argv[sys.argv.index("--note") + 1] if "--note" in sys.argv else None
jobs = {}
if os.path.exists(CHARGEN):
    jobs = {k: v.get("job") for k, v in json.load(open(CHARGEN, encoding="utf-8"))["backgrounds"].items()}
entries = []
for r in D.ROWS:
    i, kind, parent, srd, cval, disp, flavor = r[:7]
    label = r[7] if len(r) > 7 else srd
    e = {"id": i, "kind": kind, "parent_id": parent, "srd_name": srd, "display_name": disp,
         "combined_label": "%s (%s)" % (disp, label), "chargen_value": cval, "flavor": flavor}
    if label != srd: e["label_name"] = label
    if kind == "background": e["chargen_job"] = jobs.get(cval)
    entries.append(e)
order = ["background", "choice"]
entries.sort(key=lambda e: order.index(e["kind"]))
counts = collections.Counter(e["kind"] for e in entries)
def snap(es): return {e["id"]: e["display_name"] for e in es}
prev_ver, prev_snap = None, {}
if os.path.exists(VER_PATH):
    pv = json.load(open(VER_PATH, encoding="utf-8")); prev_ver, prev_snap = pv["version"], pv.get("snapshot", {})
def bump(v):
    a, b, c = (int(x) for x in v.split(".")); return "%d.%d.%d" % (a, b, c + 1)
NEW_VER = bump(prev_ver) if prev_ver else "0.1.0"
cur = snap(entries)
diff = {"since_version": prev_ver, "added": sorted(set(cur) - set(prev_snap)), "removed": sorted(set(prev_snap) - set(cur)),
        "renamed": sorted(k for k in set(cur) & set(prev_snap) if prev_snap[k] != cur[k])}
meta = {
 "title": "Background (Prior Employment) reskins: 5e background and S7 choices -> modern-Earth display name (names and flavor only)",
 "owner": "DCC Lore", "updated": datetime.date.today().isoformat(), "version": NEW_VER,
 "version_file": "tables/background-reskins.version.json (sha256, built_at, entry_count, diff); history in tables/background-reskins.CHANGELOG.md",
 "id_scheme": {
   "id": "background ids are the lower-cased chargen-5e.json background keys (acolyte ... wayfarer). Choice ids: feat-<origin feat>, asi-2-1, asi-1-1-1, package-a, package-b. Never change once published.",
   "stored_on_sheet": "Sheets keep storing the 5e background key, origin feat and package id as today; this table only changes what /create and announcements show.",
   "lookup": "Look up by id, or by (kind, chargen_value): chargen_value is the exact string used in chargen-5e.json (background key, origin_feats entry, package id) or the spec string for the ability bonus picks.",
   "fallback": "If an id is missing, fall back to srd_name (exact, case-insensitive)."},
 "display_rule": "Show combined_label = 'Display Name (5e Name)'. Names and flavor only: ability score bonuses, feats, skills, tools, equipment and gold are untouched. Skill and tool names stay plain. label_name, when present, is the short 5e name used in the label because srd_name itself has parentheses (Magic Initiate): labels never nest parentheses.",
 "kinds": {"background": "the 16 backgrounds on S7 (chargen-5e.json backgrounds); chargen_job keeps the earlier placeholder job line from that file",
           "choice": "other labels on S7: parent_id origin-feat (the 12 origin feats in chargen-5e.json origin_feats), background-asi (the +2 / +1 and +1 / +1 / +1 picks), background-kit (starting-gear Package A and Package B, shared by all backgrounds)"},
 "tone": "DCC dungeon-crawl gallows humor, prior jobs that went badly, modern Earth, petty and funny. Adults-only table, cursing cleared. Crawlers, never the other word. One industry and one punchline per entry.",
 "counts": dict(counts), "total": len(entries),
 "needs_code": {
   "owner": "Architect",
   "what": "bgnames.js packageLabel(t, pkg, gpText, plain) is called from screens.js with gpText built from GP ('{gp} GP left over' for a package with items, '{gp} GP' for the gold option). Switch the S10 background menu to credits so it matches the class menu (package-class-a, package-class-b, package-gold in create-screens-reskins).",
   "templates": {"package_with_items": "<combined_label> - {gp} credits left over", "gold_option": "<combined_label> - {gp} credits"},
   "examples": ["Cardboard Carton From Your Desk (Package A) - 8 credits left over", "Severance Envelope, Unmarked (Package B) - 50 credits"],
   "units": "1 credit = 1 GP (Core 5.10). The amounts are the chargen-5e.json gp numbers, unchanged. Whole credits print without decimals (15 credits); a fraction prints with decimals (0.5 credit); 1 cp = 0.01 credit. Singular 'credit' for an amount of 1 or less. Starting-package amounts are whole numbers.",
   "not_changed_here": "The table stores names and flavor only; no amount is stored in this file."},
 "consumers": ["/create S7 (Prior Employment) and S10 package screens", "sheet cards", "System announcements"],
}
doc = {"schema": "background-reskins/0.1.0", "meta": meta, "entries": entries}
STAGE = JSON_PATH + ".tmp"
json.dump(doc, open(STAGE, "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(STAGE, "a").write("\n")
r = subprocess.run([sys.executable, os.path.join(HERE, "background_reskin_check.py"), STAGE], capture_output=True, text=True)
if r.returncode:
    sys.stdout.write(r.stdout); os.remove(STAGE); sys.exit("background_reskin_check failed on the staged build; nothing written")
os.replace(STAGE, JSON_PATH)
sha = hashlib.sha256(open(JSON_PATH, "rb").read()).hexdigest()
now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
json.dump({"version": NEW_VER, "sha256": sha, "built_at": now, "entry_count": len(entries), "note": NOTE, "diff": diff, "snapshot": cur},
          open(VER_PATH, "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(VER_PATH, "a").write("\n")
new_log = not os.path.exists(LOG_PATH)
with open(LOG_PATH, "a", encoding="utf-8") as f:
    if new_log: f.write("# background-reskins CHANGELOG\nOwner: DCC Lore | Status: draft | Version: 0.1 | Updated: %s\nSummary: One line per build of tables/background-reskins.json (version, short sha256, entry count, diff).\n\n" % datetime.date.today().isoformat())
    f.write("- %s | v%s | sha256 %s | %d entries | %s; +%d added, -%d removed, %d renamed\n" % (datetime.date.today().isoformat(), NEW_VER, sha[:12], len(entries), NOTE or "build", len(diff["added"]), len(diff["removed"]), len(diff["renamed"])))
print("wrote %d entries (%s)" % (len(entries), dict(counts)))
print("version %s sha256 %s" % (NEW_VER, sha))
