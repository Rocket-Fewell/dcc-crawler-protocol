#!/usr/bin/env python3
"""Builds tables/species-class-reskins.json (+ .version.json and a CHANGELOG line) from species_class_data.py.
Display-name layer only: ids, stats and rules stay the 5e ones. Same discipline as reskin_build.py:
stage the JSON, run species_class_check.py on the stage, then write the JSON, the version file (version, sha256, diff) and the changelog.
Usage: python3 tools/species_class_build.py [--note "text"]      (the patch version bumps on every build)"""
import json, os, sys, hashlib, datetime, subprocess, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import species_class_data as D
OUT = os.path.join(HERE, "..", "tables")
JSON_PATH = os.path.join(OUT, "species-class-reskins.json")
VER_PATH = os.path.join(OUT, "species-class-reskins.version.json")
LOG_PATH = os.path.join(OUT, "species-class-reskins.CHANGELOG.md")
NOTE = sys.argv[sys.argv.index("--note") + 1] if "--note" in sys.argv else None

VARIANT_NOTES = {
 "felid-cat": "Same rules as Felid (rules/30 4.2 has one stat block). Cosmetic variant; no separate rules entry (rules/30 open question 14).",
 "felid-cat-girl": "Same rules as Felid (one stat block). Cosmetic variant; no separate rules entry (open question 14).",
 "felid-tigran": "DIFFERS IN CANON, NOT IN RULES: canon Tigran is a big cat (ledger R-053), but rules/30 4.2 gives no separate stat block, so it plays as base Felid (size Medium or Small per the Felid table). Syndicate to confirm whether Tigran needs its own rules entry (open question 14).",
 "caprid-small": "Same rules as Caprid. Canon sub-type 'smallest breed, about four feet' (Caprid wiki page, Subraces, Book 8 spoiler). rules/30 4.8 allows Small size 'if you pick a small breed; DM approves', but names no breed entry. Names come from the wiki/ledger (R-004), not the supplement.",
 "caprid-large-dark": "Same rules as Caprid (Medium default). Canon sub-type 'large, dark, satanic-looking breed' (Caprid wiki page, Subraces, Book 8 spoiler). rules/30 4.8 'Not ported' lists it as a later subrace idea. Name from the wiki/ledger, not the supplement.",
 "lajabless-radiant": "A PHASE, not a pick: every Lajabless alternates Radiant and Skull every 12 hours (rules/30 4.7 names Radiant Phase; ledger R-049: beautiful form, spells cost half, Strength halved). Rules are already in the base Lajabless entry. Syndicate to confirm whether the starting phase is selectable.",
 "lajabless-skull": "A PHASE, not a pick: every Lajabless alternates Radiant and Skull every 12 hours (rules/30 4.7 names Skull Phase; ledger R-049: skull-faced form, Strength doubled, spells cost more). Rules are already in the base Lajabless entry. Syndicate to confirm whether the starting phase is selectable.",
 "nodling-two-headed": "This is the version rules/30 4.10 ports (two heads; 'this is the two-head version'). Canon allows two to six heads (ledger R-050, Nodling wiki page). Base Nodling rules apply; no separate rules entry.",
 "nodling-three-headed": "Canon head count (ledger R-050: two to six heads). rules/30 4.10 lists the 2-6 head variants as NOT ported, so the rules are those of base Nodling (two heads); Syndicate to decide whether more heads need their own entry. Name from the ledger, not the supplement.",
 "nodling-four-headed": "Canon head count (ledger R-050). Not ported in rules/30 4.10; base Nodling rules apply. Syndicate to decide. Name from the ledger.",
 "nodling-five-headed": "Canon head count (ledger R-050). Not ported in rules/30 4.10; base Nodling rules apply. Syndicate to decide. Name from the ledger.",
 "nodling-six-headed": "Canon head count (ledger R-050). Not ported in rules/30 4.10; base Nodling rules apply. Syndicate to decide. Name from the ledger.",
 "felid-were-cat": "Same rules as Felid (one stat block). Cosmetic variant; no separate rules entry (open question 14). Canon Were-Cat is a shifter form; no shifting rules are ported.",
}
entries = []
for r in D.ROWS:
    i, kind, parent, srd, disp, nation, flavor = r[:7]
    label = r[8] if len(r) > 8 else srd
    long_name = long_spoken = None
    if kind in ("species", "species_lineage", "species_variant"):
        # Caleb, 2026-10-04: species and lineage display names are just the nationality; the joke name is kept as long_name.
        long_name, long_spoken = disp, (r[7] if len(r) > 7 and r[7] else None)
        disp = nation
    spoken = r[7] if (kind not in ("species", "species_lineage") and len(r) > 7 and r[7]) else "%s. %s." % (disp, srd)
    e = {"id": i, "kind": kind, "parent_id": parent, "srd_name": srd, "display_name": disp,
         "combined_label": "%s (%s)" % (disp, label), "nation": nation, "flavor": flavor, "spoken": spoken}
    if label != srd: e["label_name"] = label
    if kind in ("species_lineage", "species_variant"):
        e["base_id"] = parent
    if kind == "species_lineage":
        e["chargen_value"] = srd.replace(" Dragonborn", "").replace(" Goliath", "").replace(" Tiefling", "")
        e["rules_entry"] = True
    if kind == "species_variant":
        e["chargen_value"] = None
        e["rules_entry"] = False
        e["rules_note"] = VARIANT_NOTES[i]
    if long_name:
        e["long_name"] = long_name
        e["long_label"] = "%s (%s)" % (long_name, srd)
        if long_spoken: e["long_spoken"] = long_spoken
    entries.append(e)
order = ["species", "species_variant", "species_lineage", "class", "class_option"]
entries.sort(key=lambda e: order.index(e["kind"]))   # stable
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
 "title": "Species and class reskins: 5e species/class -> modern-Earth display name (names and flavor only)",
 "owner": "DCC Lore", "updated": datetime.date.today().isoformat(), "version": NEW_VER,
 "version_file": "tables/species-class-reskins.version.json (sha256, built_at, entry_count, diff); history in tables/species-class-reskins.CHANGELOG.md",
 "id_scheme": {
   "id": "id = stable kebab-case 5e id: the lower-cased species or class name from tables/chargen-5e.json / rules/30-species-supplement-5e.md, or '<parent>-<option>' for a lineage, ancestry or class option. Never changes once published.",
   "stored_on_sheet": "Sheets keep storing the 5e species and class (and lineage/option) as they do today; this table only changes what /create and announcements show.",
   "lookup": "Look up by id. For a lineage or class option, parent_id names its species or class.",
   "fallback": "If an id is missing, fall back to srd_name (exact, case-insensitive)."},
 "display_rule": "Species and lineages: display_name is just the nationality (Caleb, 2026-10-04), e.g. 'Welsh (Dragonborn)', 'Icelandic (High Elf)'; the earlier joke name is kept as long_name (and long_label, long_spoken). Show combined_label = 'Display Name (5e Name)' (label_name, when present, is the short 5e name used in the label instead of srd_name; class options only). Names and flavor only: ability scores, traits, hit dice, proficiencies, spells and every other 5e rule are untouched.",
 "kinds": {"species": "9 SRD species (chargen-5e.json species) + 12 supplement species (rules/30 section 4) = 21",
           "species_variant": "variants of a species: rules/30 4.2 Felid = Cat, Cat Girl, Tigran, Were-Cat; Lajabless phases Radiant and Skull (rules/30 4.7); Caprid Small and Large Dark breeds and Nodling Two to Six heads (ledger R-004 / R-050 and the wiki pages, since rules/30 names no entries for them). They have base_id = the species id, rules_entry false (no separate stat block), and a rules_note. Added at Caleb's request, 2026-10-04.",
           "species_lineage": "base_id = the species id; chargen_value = the exact option string in chargen-5e.json. The sub-choices /create shows: Dragonborn ancestry (10), Elf lineage (3), Gnome lineage (2), Goliath ancestry (6), Tiefling legacy (3)",
           "class": "the 12 classes in chargen-5e.json",
           "class_option": "the level-1 class choices that rename a branch: Cleric Divine Order (2), Druid Primal Order (2). No level-3 subclasses are chosen in /create."},
 "nation": "Real-world nationality the name plays on (null for classes). Caleb, 2026-10-04: every species, lineage and variant entry has its OWN unique nationality (no two share one), so a label never repeats a nationality; the check enforces it.",
 "tone": "DCC dungeon-crawl gallows humor, affectionate, adults-only table. Real nationalities played for comedy on food, weather, folklore, sports, quirks and absurdity. No slurs, no 'lazy/dirty/violent' stereotypes. Crawlers, never the other word. Caleb, 2026-10-04: real nationalities for ALL species including Orc; no archetype swaps; no tone_risk or alt_display_name fields.",
 "source": "Caleb's request of 2026-10-04 (Azerbaijani/Romanian Orc, Norwegian/Icelandic Elf, Vietnamese Dwarf named by him; rest made up by Lore).",
 "counts": dict(counts), "total": len(entries),
 "consumers": ["/create (species, lineage, class, class option prompts)", "sheet cards", "System announcements"],
}
doc = {"schema": "species-class-reskins/0.1.0", "meta": meta, "entries": entries}
STAGE = JSON_PATH + ".tmp"
json.dump(doc, open(STAGE, "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(STAGE, "a").write("\n")
r = subprocess.run([sys.executable, os.path.join(HERE, "species_class_check.py"), STAGE], capture_output=True, text=True)
if r.returncode:
    sys.stdout.write(r.stdout); os.remove(STAGE); sys.exit("species_class_check failed on the staged build; nothing written")
os.replace(STAGE, JSON_PATH)
sha = hashlib.sha256(open(JSON_PATH, "rb").read()).hexdigest()
now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
json.dump({"version": NEW_VER, "sha256": sha, "built_at": now, "entry_count": len(entries), "note": NOTE, "diff": diff, "snapshot": cur},
          open(VER_PATH, "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(VER_PATH, "a").write("\n")
new_log = not os.path.exists(LOG_PATH)
with open(LOG_PATH, "a", encoding="utf-8") as f:
    if new_log: f.write("# species-class-reskins CHANGELOG\nOwner: DCC Lore | Status: draft | Version: 0.1 | Updated: %s\nSummary: One line per build of tables/species-class-reskins.json (version, short sha256, entry count, diff).\n\n" % datetime.date.today().isoformat())
    f.write("- %s | v%s | sha256 %s | %d entries | %s; +%d added, -%d removed, %d renamed\n" % (datetime.date.today().isoformat(), NEW_VER, sha[:12], len(entries), NOTE or "build", len(diff["added"]), len(diff["removed"]), len(diff["renamed"])))
print("wrote %d entries (%s)" % (len(entries), dict(counts)))
print("version %s sha256 %s" % (NEW_VER, sha))
