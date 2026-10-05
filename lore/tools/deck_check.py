#!/usr/bin/env python3
"""Validates tables/loot-decks/*.json (loot decks schema loot-deck/0.1.1 or 0.1.2 and achievement deck achievement-deck/0.1).
Usage: python3 tools/deck_check.py [dir]   Exit 0 = no errors (warnings allowed)."""
import json, os, re, sys, glob, collections
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tables", "loot-decks")
TIERS = ["Bronze", "Silver", "Gold", "Platinum", "Legendary", "Celestial"]
ITEM_RANGE = {"Bronze": (0, 100), "Silver": (100, 500), "Gold": (500, 5000), "Platinum": (5000, 50000), "Legendary": (20000, 250000)}
CREDIT_RANGE = {"Bronze": (15, 90), "Silver": (50, 300), "Gold": (500, 3000), "Platinum": (5000, 30000), "Legendary": (20000, 120000)}
CARD_REQ = ["id","floor","zone","tier","box_types","pull_type","kind","reskin_name","real_5e_name","source_5e","rarity","attunement",
 "category","plain_mechanics","spoken_line","snark_line","reward","canon_status","credit_value","draw_weight","unique","tailor_tags",
 "exclusive_to","grant","ledger","box_name","deed","notes"]
MECH_REQ = ["text","action_cost","range","damage","save_dc","duration","uses","limits","weight_lb"]
ENUM = {"pull_type": {"consumable","gear","credits","tailored","weird"}, "kind": {"item","consumable","credits","key","pet","stat_bump","junk","clue"},
 "source_5e": {"SRD 5.2","DMG 2024","PHB 2024","Other 5e (VERIFY)","HOUSE"},
 "rarity": {"Mundane","Common","Uncommon","Rare","Very Rare","Legendary","Artifact","n/a"},
 "category": {"Weapons","Armor","Consumables","Keys","Misc","Credits","Stats"}, "canon_status": {"CANON","CANON-INSPIRED","HOUSE"}}
RECHARGE = {"none", "dawn", "short rest", "long rest", "1d6+1 at dawn", "floor"}  # "floor" added 2026-10-04 (once per floor); Syndicate to add to rules/40 section 1.1
ACTIONS = {"Action","Bonus Action","Magic action","Utilize action","Reaction","None (passive)","none"}
errs, warns = [], []
def E(m): errs.append(m)
def W(m): warns.append(m)
def words(s): return len(s.split())

files = sorted(glob.glob(os.path.join(D, "*.json")))
if not files: E("no json files in %s" % D)
ids = collections.Counter(); stats = collections.defaultdict(lambda: collections.Counter()); vals = collections.defaultdict(list)
wsum = collections.defaultdict(float); wval = collections.defaultdict(float); zero = []
ach_stats = collections.Counter(); ach_ids = collections.Counter(); ach_titles = collections.Counter()

for p in files:
    name = os.path.basename(p)
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as ex:
        E("%s: invalid JSON: %s" % (name, ex)); continue
    txt = open(p, encoding="utf-8").read()
    if re.search(r"desperado\s+box", txt, re.I) and "no_desperado_box" not in txt and "Never a" not in txt:
        W("%s: mentions 'Desperado Box' (ok only as a warning note)" % name)
    sch = d.get("schema", "")
    if sch.startswith("achievement-deck/"):
        for k in ["schema","deck_id","version","floor","owner","updated","achievements"]:
            if k not in d: E("%s: wrapper missing %s" % (name, k))
        for a in d.get("achievements", []):
            aid = a.get("id", "?"); ach_ids[aid] += 1; ach_titles[a.get("title","")] += 1
            for k in ["id","title","floor","zone","trigger","description","reward_line","reward_kind","reward_tier","box_name","credits","title_awarded","catalog_id","source_tag","ledger_ids","alpha_earned","text_status","hidden","notes"]:
                if k not in a: E("%s %s: missing %s" % (name, aid, k))
            if words(a.get("description","")) > 25: E("%s %s: description > 25 words" % (name, aid))
            if not str(a.get("reward_line","")).startswith("Reward:"): E("%s %s: reward_line must start 'Reward:'" % (name, aid))
            if a.get("source_tag") not in ("CANON","CANON-INSPIRED","HOUSE"): E("%s %s: bad source_tag" % (name, aid))
            if a.get("source_tag") in ("CANON",) and not a.get("ledger_ids"): E("%s %s: CANON needs ledger_ids" % (name, aid))
            if words(a.get("reward_line","")) > 28: W("%s %s: reward_line long for TTS (%d words)" % (name, aid, words(a["reward_line"])))
            if not isinstance(a.get("credits"), (int, float)) or a["credits"] < 0: E("%s %s: credits must be number >= 0" % (name, aid))
            rk = a.get("reward_kind"); ach_stats["kind:" + str(rk)] += 1
            if rk == "box":
                t = a.get("reward_tier"); ach_stats["box:" + str(t)] += 1
                if t not in ("Bronze", "Silver"): E("%s %s: Floor 1 achievement box must be Bronze or Silver (got %s)" % (name, aid, t))
                bn = a.get("box_name") or ""
                if not bn.endswith("Box") or bn.split(" ")[0] in TIERS: E("%s %s: box_name must end 'Box' and have no tier prefix: %r" % (name, aid, bn))
                if a.get("reward_line") != "Reward: You've received a %s %s!" % (t, bn): E("%s %s: reward_line must be 'Reward: You've received a <Tier> <box_name>!'" % (name, aid))
                if "desperado" in bn.lower(): E("%s %s: Desperado Box forbidden" % (name, aid))
            elif a.get("box_name"): E("%s %s: box_name set on non-box reward" % (name, aid))
            if rk == "title_credits" and a.get("credits") != 25: W("%s %s: title_credits without 25 credits" % (name, aid))
            if a.get("alpha_earned"): ach_stats["alpha"] += 1
            if a.get("hidden"): ach_stats["hidden"] += 1
        for k, c in ach_ids.items():
            if c > 1: E("%s: duplicate achievement id %s" % (name, k))
        for k, c in ach_titles.items():
            if c > 1: E("%s: duplicate achievement title %s" % (name, k))
        continue
    # ---- loot deck
    if sch not in ("loot-deck/0.1.1", "loot-deck/0.1.2"): E("%s: schema must be loot-deck/0.1.1 or loot-deck/0.1.2 (got %r)" % (name, sch))
    for k in ["schema","deck_id","version","floor","zone","cards"]:
        if k not in d: E("%s: wrapper missing %s" % (name, k))
    expect = os.path.splitext(name)[0]
    if d.get("deck_id") != expect: E("%s: deck_id %r != filename" % (name, d.get("deck_id")))
    if not re.match(r"^f\d\d-(z\d\d|zS|any)-[a-z0-9-]+\.json$", name): E("%s: filename not f<FF>-<zone>-<slug>.json" % name)
    cn = [c["reskin_name"] for c in d.get("cards", []) if "reskin_name" in c]
    for c in d.get("cards", []):
        cid = c.get("id", "?"); ids[cid] += 1
        miss = [k for k in CARD_REQ if k not in c]
        if miss: E("%s %s: missing %s" % (name, cid, miss)); continue
        story_ok = sch == "loot-deck/0.1.2"
        extra = [k for k in c if k not in CARD_REQ and not (story_ok and k in ("story_value", "bound", "sale_value"))]
        if extra: E("%s %s: unknown fields %s (schema bump needed)" % (name, cid, extra))
        m = re.match(r"^f(\d\d)-(z\d\d|zS|any)-(\d{4})$", cid)
        if not m: E("%s %s: bad id format" % (name, cid))
        else:
            if int(m.group(1)) != c["floor"] or m.group(2) != c["zone"]: E("%s %s: id does not match floor/zone" % (name, cid))
        if c["zone"] != d.get("zone") or c["floor"] != d.get("floor"): E("%s %s: card floor/zone != deck" % (name, cid))
        if c["tier"] not in TIERS: E("%s %s: bad tier" % (name, cid))
        for ek, ev in ENUM.items():
            if c[ek] not in ev: E("%s %s: bad %s %r" % (name, cid, ek, c[ek]))
        if not isinstance(c["box_types"], list) or not c["box_types"] or not set(c["box_types"]) <= {"any","Boss","Quest","Fan","Benefactor"}: E("%s %s: bad box_types" % (name, cid))
        pm = c["plain_mechanics"]
        mm = [k for k in MECH_REQ if k not in pm]
        if mm: E("%s %s: plain_mechanics missing %s" % (name, cid, mm))
        else:
            if not str(pm["text"]).strip(): E("%s %s: empty plain_mechanics.text" % (name, cid))
            if pm["action_cost"] not in ACTIONS and pm["action_cost"].split(":")[0] not in ACTIONS: E("%s %s: bad action_cost %r" % (name, cid, pm["action_cost"]))
            if not isinstance(pm["weight_lb"], (int, float)): E("%s %s: weight_lb must be number" % (name, cid))
            if pm["uses"] is not None and not (isinstance(pm["uses"], dict) and "max" in pm["uses"] and "recharge" in pm["uses"]): E("%s %s: bad uses" % (name, cid))
            elif pm["uses"] is not None and pm["uses"]["recharge"] not in RECHARGE: E("%s %s: bad uses.recharge %r (allowed: %s)" % (name, cid, pm["uses"]["recharge"], sorted(RECHARGE)))
        for k in ["reskin_name","real_5e_name","snark_line","reward","box_name","deed","spoken_line"]:
            if not str(c[k]).strip(): E("%s %s: blank %s" % (name, cid, k))
        if words(c["spoken_line"]) > 25: E("%s %s: spoken_line %d words (>25)" % (name, cid, words(c["spoken_line"])))
        if words(c["reward"]) > 25: E("%s %s: reward %d words (>25)" % (name, cid, words(c["reward"])))
        if words(c["snark_line"]) > 22 or c["snark_line"].count(". ") > 1: W("%s %s: snark_line long/multi-sentence" % (name, cid))
        if c["reward"] != c["spoken_line"]: W("%s %s: reward != spoken_line" % (name, cid))
        base = c["reskin_name"].split(" (")[0].split(",")[0].lower()
        if base[:10] not in c["spoken_line"].lower(): W("%s %s: spoken_line does not include reskin name" % (name, cid))
        bn = c["box_name"]
        if not bn.endswith("Box") or bn.split(" ")[0] in TIERS or re.search(r"loot box|desperado", bn, re.I): E("%s %s: bad box_name %r" % (name, cid, bn))
        if not isinstance(c["draw_weight"], int) or not (0 <= c["draw_weight"] <= 100): E("%s %s: draw_weight must be int 0-100" % (name, cid))
        elif c["draw_weight"] == 0:
            zero.append(cid)
            if not re.search(r"weight 0|hand-pick|fallback|already issued|ONLY", c["notes"], re.I): E("%s %s: draw_weight 0 needs a note saying why" % (name, cid))
        if "story_value" in c or "bound" in c or "sale_value" in c:
            sv = c.get("story_value")
            if c["tier"] != "Legendary" or c["draw_weight"] != 0: E("%s %s: story_value/bound only on Legendary Story Box cards with draw_weight 0" % (name, cid))
            if not isinstance(sv, (int, float)) or isinstance(sv, bool) or not (ITEM_RANGE["Legendary"][0] <= sv <= ITEM_RANGE["Legendary"][1]): E("%s %s: story_value %r outside Legendary range %s" % (name, cid, sv, ITEM_RANGE["Legendary"]))
            if "bound" in c and not isinstance(c["bound"], bool): E("%s %s: bound must be a boolean (false = lootable, tradeable, sellable; Caleb ruling 2026-10-04)" % (name, cid))
            if c["credit_value"] != 0: E("%s %s: Story Box credit_value must be 0" % (name, cid))
            if "sale_value" in c and (not isinstance(c["sale_value"], (int, float)) or isinstance(c["sale_value"], bool) or c["sale_value"] < 0): E("%s %s: sale_value must be a number >= 0 (System buyback, Floor-1 scale)" % (name, cid))
        if not isinstance(c["credit_value"], (int, float)) or isinstance(c["credit_value"], bool) or c["credit_value"] < 0: E("%s %s: credit_value must be number >= 0" % (name, cid))
        elif "story_value" in c: pass
        else:
            rng = CREDIT_RANGE.get(c["tier"]) if c["kind"] == "credits" else ITEM_RANGE.get(c["tier"])
            if rng and not (rng[0] <= c["credit_value"] <= rng[1]) and not (c["draw_weight"] == 0 and c["kind"] in ("junk","clue") ):
                if c["kind"] == "junk" and c["credit_value"] <= rng[1]: pass
                else: E("%s %s: credit_value %s outside %s range %s" % (name, cid, c["credit_value"], c["tier"], rng))
        if c["tier"] in ("Gold","Platinum","Legendary","Celestial") and c["draw_weight"] != 0: E("%s %s: %s card on Floor 1 must have draw_weight 0" % (name, cid, c["tier"]))
        if c["draw_weight"] > 0:
            ok = {"Bronze": {"Mundane","Common","n/a"}, "Silver": {"Mundane","Common","Uncommon","n/a"}}.get(c["tier"], set())
            if c["rarity"] not in ok: E("%s %s: rarity %s not drawable in %s box (Floor 1 ceiling)" % (name, cid, c["rarity"], c["tier"]))
        if c["kind"] == "credits":
            g = c["grant"]
            if not g or not re.match(r"^\d+d\d+x\d+$", str(g.get("roll", ""))): E("%s %s: credits card needs grant.roll like 3d6x5" % (name, cid))
            elif (c["tier"], g["roll"]) not in {("Bronze","3d6x5"),("Silver","2d6x25")}: E("%s %s: roll %s wrong for %s" % (name, cid, g["roll"], c["tier"]))
        elif c["grant"] is not None: E("%s %s: non-credits grant not expected on F1" % (name, cid))
        if c["attunement"] is not None and c["rarity"] in ("Mundane","Common"): W("%s %s: attunement on low rarity" % (name, cid))
        if c["canon_status"] == "CANON" and "LEDGER:" not in c["notes"]: E("%s %s: CANON needs 'LEDGER: <ids>' in notes" % (name, cid))
        if c["unique"] and c["exclusive_to"] is None and c["zone"] == "z10": W("%s %s: unique boss trophy would starve other crawlers" % (name, cid))
        if c["rarity"] == "Uncommon" and c["tier"] == "Bronze" and c["draw_weight"] != 0: E("%s %s: Uncommon in Bronze must be hand-pick (weight 0)" % (name, cid))
        s = stats[c["tier"]]; s["cards"] += 1; s["live" if c["draw_weight"] > 0 else "hand_pick_only"] += 1
        s["pull:" + c["pull_type"]] += 1; vals[c["tier"]].append(c["credit_value"])
        wsum[c["tier"]] += c["draw_weight"]; wval[c["tier"]] += c["draw_weight"] * c["credit_value"]
    nv = d.get("needs_verify", [])
    live = {c["real_5e_name"] for c in d.get("cards", [])}
    for n in nv:
        for k in ["candidate_reskin","real_5e_name","tier","reason","spec_ref"]:
            if k not in n: E("%s needs_verify entry missing %s" % (name, k))
        if n.get("real_5e_name") in live: E("%s: needs_verify item %r also appears in cards[]" % (name, n.get("real_5e_name")))
    stats["_needs_verify"]["count"] += len(nv)
for k, c in ids.items():
    if c > 1: E("duplicate card id %s (%d)" % (k, c))
if not ach_ids: W("no achievement deck found")

print("FILES:", ", ".join(os.path.basename(p) for p in files))
for t in TIERS:
    if t in stats:
        s = stats[t]; v = vals[t]
        pulls = ", ".join("%s=%d" % (k[5:], n) for k, n in sorted(s.items()) if k.startswith("pull:"))
        wm = (wval[t] / wsum[t]) if wsum[t] else 0
        print("%-8s cards=%d live=%d hand-pick-only=%d | total credit_value=%.2f | weighted mean=%.2f | %s" % (t, s["cards"], s["live"], s["hand_pick_only"], sum(v), wm, pulls))
print("hand-pick-only (weight 0):", ", ".join(zero) or "none")
print("needs_verify entries:", stats["_needs_verify"]["count"])
if ach_ids:
    print("ACHIEVEMENTS: total=%d alpha=%d hidden=%d | " % (len(ach_ids), ach_stats["alpha"], ach_stats["hidden"]) +
          ", ".join("%s=%d" % (k[5:], n) for k, n in sorted(ach_stats.items()) if k.startswith("kind:")) + " | boxes: " +
          ", ".join("%s=%d" % (k[4:], n) for k, n in sorted(ach_stats.items()) if k.startswith("box:")))
for w in warns: print("WARN:", w)
for e in errs: print("ERROR:", e)
print("errors: %d  warnings: %d" % (len(errs), len(warns)))
sys.exit(1 if errs else 0)
