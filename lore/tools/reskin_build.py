#!/usr/bin/env python3
"""Builds tables/item-reskins.json and tables/item-reskins.md from tools/reskin_data.py.
Usage: python3 tools/reskin_build.py [--note "what changed"]
After every successful build (staged JSON passes tools/reskin_check.py) it also writes tables/item-reskins.version.json
({version, sha256, built_at, entry_count, diff vs previous build, snapshot}) and appends one line to tables/item-reskins.CHANGELOG.md.
Version = patch counter, bumped on every build (starts from meta.version / the previous version.json).
Then run tools/reskin_publish.py for the ready-to-post summary."""
import json, os, re, sys, collections, hashlib, subprocess, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import reskin_data as D
OUT = os.path.join(HERE, "..", "tables")
CAT_ORDER = ["weapon", "armor", "shield", "ammunition", "focus", "gear", "pack", "tool"]
CAT_LABEL = {"weapon": "Weapons", "armor": "Armor", "shield": "Shields", "ammunition": "Ammunition", "focus": "Spellcasting foci",
             "gear": "Adventuring gear", "pack": "Starting equipment packs", "tool": "Tools, kits, gaming sets, instruments"}
MULT = {"gp": 100, "sp": 10, "cp": 1}

def slug(n):
    s = n.lower().replace("\u2019", "").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def cp(price):
    if price is None: return None
    m = re.fullmatch(r"([\d,]+) (gp|sp|cp)", price)
    assert m, price
    return int(m[1].replace(",", "")) * MULT[m[2]]

keys_by_id = collections.defaultdict(list)
for k, v in D.CHARGEN_KEYMAP.items(): keys_by_id[v].append(k)

entries = []
for row in D.ROWS:
    name, cat, sub, price, disp, snark, origin = row[:7]
    ex = row[7] if len(row) > 7 else {}
    sid = ex.get("id") or slug(name)
    e = {"srd_id": sid, "srd_name": name, "category": cat, "subcategory": sub, "display_name": disp,
         "combined_label": "%s (%s)" % (disp, name), "snark": snark, "source_tag": ex.get("source", "HOUSE"), "ledger_ref": ex.get("ledger"),
         "name_origin": origin, "legacy_names": ex.get("legacy", []), "chargen_keys": sorted(keys_by_id.get(sid, [])),
         "floor_variants": [], "base_price": price, "base_price_cp": cp(price),
         "price_flag": ex.get("flag") if price is None else None, "price_note": ex.get("note"),
         "resolve_to_variant": bool(ex.get("resolve")), "variants": [],
         "non_srd": bool(ex.get("non_srd")), "price_credits_proposed": ex.get("credits"), "mechanic_note": ex.get("mech")}
    entries.append(e)
for g in entries:
    if g["resolve_to_variant"]:
        g["variants"] = [v["srd_id"] for v in entries if v["subcategory"] == g["subcategory"] and not v["resolve_to_variant"]]
entries.sort(key=lambda e: CAT_ORDER.index(e["category"]))   # stable: keeps SRD order inside a category
nulls = [e["srd_id"] for e in entries if e["resolve_to_variant"]]
non_srd = [e["srd_id"] for e in entries if e["non_srd"]]
counts = collections.Counter(e["category"] for e in entries)
NOTE = None
if "--note" in sys.argv:
    NOTE = sys.argv[sys.argv.index("--note") + 1]
JSON_PATH = os.path.join(OUT, "item-reskins.json")
VER_PATH = os.path.join(OUT, "item-reskins.version.json")
LOG_PATH = os.path.join(OUT, "item-reskins.CHANGELOG.md")
def snap(ents):
    return {e["srd_id"]: {"cp": e["base_price_cp"], "display": e["display_name"]} for e in ents}
prev_ver, prev_snap = None, {}
if os.path.exists(VER_PATH):
    pv = json.load(open(VER_PATH, encoding="utf-8")); prev_ver, prev_snap = pv["version"], pv.get("snapshot", {})
elif os.path.exists(JSON_PATH):
    pj = json.load(open(JSON_PATH, encoding="utf-8")); prev_ver, prev_snap = pj["meta"]["version"], snap(pj["entries"])
def bump(v):
    a, b, c = (int(x) for x in v.split("."))
    return "%d.%d.%d" % (a, b, c + 1)
NEW_VER = bump(prev_ver) if prev_ver else "0.1.0"
cur_snap = snap(entries)
diff = {"since_version": prev_ver,
        "added": sorted(set(cur_snap) - set(prev_snap)), "removed": sorted(set(prev_snap) - set(cur_snap)),
        "price_changed": [{"srd_id": k, "from_cp": prev_snap[k]["cp"], "to_cp": cur_snap[k]["cp"]} for k in sorted(set(cur_snap) & set(prev_snap)) if prev_snap[k]["cp"] != cur_snap[k]["cp"]],
        "renamed": sorted(k for k in set(cur_snap) & set(prev_snap) if prev_snap[k]["display"] != cur_snap[k]["display"])}
meta = {
 "title": "Item reskins: SRD 5.2 item -> flavored display name (names and flavor only)",
 "owner": "DCC Lore", "updated": datetime.date.today().isoformat(), "version": NEW_VER,
 "version_file": "tables/item-reskins.version.json (sha256, built_at, entry_count, diff); history in tables/item-reskins.CHANGELOG.md",
 "id_scheme": {
   "id": "srd_id = stable kebab-case SRD item id (examples: 'quarterstaff', 'chain-mail', 'explorers-pack'). Never changes once published.",
   "stored_on_sheet": "The sheet stores srd_id for every item (not the display name).",
   "lookup": "Look up by srd_id.",
   "fallback": "If srd_id is missing on a sheet entry, fall back to srd_name (exact, case-insensitive); then to legacy_names (older /create junk names).",
   "prices": "Prices always key off srd_id, never the display name (the Accountant must not price by display text)."},
 "display_rule": "Show combined_label = 'Display Name (SRD Name)'. Names and flavor only: damage, properties, mastery, AC, weight, price and every other 5e rule are untouched. One display_name + one snark line per 5e item.",
 "tone": "DCC dungeon-crawl gallows humor, mild snark, adult table okay. Crawlers, never 'champ'. snark <= 25 words.",
 "name_priority": "1) loot-deck reskin_name when the same 5e item is a deck card (name_origin 'deck:<card id>'); 2) chargen-5e.json junk name ('chargen', or kept in legacy_names when replaced); 3) new house name ('new').",
 "source_tag": "HOUSE for every SRD-equivalent entry; CANON for the non_srd canon items (heal-critter-potion: M-090, K-121; pet-carrier: I-012), whose ledger_ref lists the ledger ids. No DCC book item shares a name with an SRD mundane item in CANON-LEDGER.md (closest: I-009 'Healing Potion' ~ Potion of Healing, kept HOUSE). ledger_ref is null on HOUSE entries.",
 "non_srd_fields": {
   "non_srd": "true on canon/house items that have no SRD 5.2 entry (heal-critter-potion, pet-carrier). Their srd_name says '(canon item, no SRD entry)'. base_price is null on purpose (price_flag explains) and they ARE purchasable; they are not generic headers.",
   "price_credits_proposed": "Vending price in credits at Floor-1 scale (Accountant proposal; times the floor multiplier at runtime; buyback half). null for SRD items. Syndicate to confirm in the pets rule.",
   "mechanic_note": "Short rules note for non-SRD items (null for SRD items). Numbers inside it flagged 'Syndicate to set' are suggestions only."},
 "floor_variants": "Reserved: per-floor alternate display names/snark. Empty for now.",
 "price_fields": {
   "base_price": "SRD 5.2.1 cost as a string, e.g. '2 gp' (null if the SRD gives no single price).",
   "base_price_cp": "Same price as an integer in copper (1 gp = 100 cp, 1 sp = 10 cp). null when base_price is null.",
   "price_flag": "Reason a price is null.",
   "price_note": "Source note for a price that is not a plain SRD 5.2 table value (e.g. spellbook: 'SRD 5.1 gear table, Accountant ruling').",
   "resolve_to_variant": "true on generic 'Varies' category headers (arcane-focus, druidic-focus, holy-symbol, gaming-set, musical-instrument, artisans-tools). They are NOT purchasable and must be resolved to one of their `variants` srd_ids before /create or a vending wall shows or prices them.",
   "reference_only": True,
   "source": "SRD 5.2.1 'Equipment' tables (weapons, armor, adventuring gear, ammunition, foci) and tool/instrument/gaming-set entries, read 2026-10-04 from D&D Beyond free rules. Reference only; Vending Wall pricing stays with the Accountant."},
 "null_price_srd_ids": nulls + non_srd, "non_srd_ids": non_srd, "resolve_to_variant_ids": nulls,
 "counts": dict(counts), "total": len(entries),
 "scope_not_covered": "Mounts, vehicles, tack, services, lifestyle/food prices (not item reskins); magic items (see loot-decks); specific spell scrolls (deck cards name them).",
 "consumers": ["/create (starting equipment and Vending Wall)", "sheet cards", "loot announcements"],
}
doc = {"schema": "item-reskins/0.1.0", "meta": meta, "entries": entries}
STAGE = JSON_PATH + ".tmp"
with open(STAGE, "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=1, ensure_ascii=False); f.write("\n")
r = subprocess.run([sys.executable, os.path.join(HERE, "reskin_check.py"), STAGE], capture_output=True, text=True)
if r.returncode != 0:
    print(r.stdout + r.stderr); os.remove(STAGE)
    sys.exit("reskin_check failed: nothing written (item-reskins.json, version and changelog unchanged)")
os.replace(STAGE, JSON_PATH)

L = ["# Item reskins (SRD 5.2 to flavored names)",
     "Owner: DCC Lore | Status: draft | Version: %s | Updated: %s" % (NEW_VER, datetime.date.today().isoformat()),
     "Summary: Flavored display name and one snark line for every SRD 5.2 weapon, armor, shield, ammunition, focus, gear, pack and tool, with SRD reference prices for the Accountant. Names and flavor only.", "",
     "Table version %s (hash and history: `tables/item-reskins.version.json`, `tables/item-reskins.CHANGELOG.md`)." % NEW_VER, "",
     "Source of truth: `tables/item-reskins.json` (built by `tools/reskin_build.py` from `tools/reskin_data.py`; checked by `tools/reskin_check.py`).", "",
     "Display rule: show **Display Name (SRD Name)**. Names and flavor only; no 5e rule changes. Prices are SRD 5.2 reference values for the Accountant. **They always key off `srd_id`, never the display name.**", "",
     "**ID scheme:** stable kebab-case `srd_id` (e.g. `quarterstaff`, `chain-mail`, `explorers-pack`), stored on the sheet; lookup by `srd_id`; fallback to `srd_name` if missing (then `legacy_names`).", "",
     "Counts: " + ", ".join("%s %d" % (c, counts[c]) for c in CAT_ORDER) + " (total %d)." % len(entries), ""]
if nulls:
    L += ["**Generic ids are category headers, not purchasable** (`resolve_to_variant: true`): " + ", ".join("`%s`" % n for n in nulls) + ". Each lists its concrete `variants`, all priced; /create and the vending wall must resolve a generic to a variant srd_id before showing or pricing it. The only other null prices are the non_srd canon items ("+", ".join("`%s`"%n for n in non_srd)+"), which are purchasable and priced in credits (`price_credits_proposed`: Accountant proposal, Syndicate to confirm).", ""]
for c in CAT_ORDER:
    L += ["## " + CAT_LABEL[c], "", "| srd_id | SRD name | Display name | Snark | base_price |", "|---|---|---|---|---|"]
    for e in entries:
        if e["category"] != c: continue
        bp = e["base_price"] if e["base_price"] else ("%d credits proposed (non-SRD canon, Floor-1 scale; Syndicate to confirm)" % e["price_credits_proposed"] if e["non_srd"] else "header, not purchasable (resolve to variant)")
        L.append("| `%s` | %s | %s | %s | %s |" % (e["srd_id"], e["srd_name"], e["display_name"], e["snark"].replace("|", "/"), bp))
    L.append("")
open(os.path.join(OUT, "item-reskins.md"), "w", encoding="utf-8").write("\n".join(L))
print("wrote %d entries; nulls: %s" % (len(entries), nulls))

# version file + changelog (only reached when the check passed)
sha = hashlib.sha256(open(JSON_PATH, "rb").read()).hexdigest()
now = datetime.datetime.now().astimezone()
ver = {"version": NEW_VER, "sha256": sha, "built_at": now.isoformat(timespec="seconds"), "entry_count": len(entries),
       "note": NOTE, "diff": diff, "snapshot": cur_snap}
with open(VER_PATH, "w", encoding="utf-8") as f:
    json.dump(ver, f, indent=1, ensure_ascii=False); f.write("\n")
auto = "+%d added, -%d removed, %d price changes, %d renamed" % (len(diff["added"]), len(diff["removed"]), len(diff["price_changed"]), len(diff["renamed"]))
line = "- %s | v%s | sha256 %s | %d entries | %s%s" % (now.date().isoformat(), NEW_VER, sha[:12], len(entries), (NOTE + "; ") if NOTE else "", auto)
hdr = ["# Item reskins changelog", "Owner: DCC Lore | Status: draft | Version: %s | Updated: %s" % (NEW_VER, now.date().isoformat()),
       "Summary: One line per build of tables/item-reskins.json (written by tools/reskin_build.py; do not edit by hand).", ""]
body = []
if os.path.exists(LOG_PATH):
    body = [l for l in open(LOG_PATH, encoding="utf-8").read().splitlines()[4:] if l.strip()]
open(LOG_PATH, "w", encoding="utf-8").write("\n".join(hdr + body + [line]) + "\n")
print("version %s sha256 %s (%s)" % (NEW_VER, sha, auto))
