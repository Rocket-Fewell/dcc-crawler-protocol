#!/usr/bin/env python3
"""Assemble chapters/02-crawler-creation.md from drafts/02-crawler-creation.src.md.
Replaces <<TABLE:name>> placeholders with markdown tables generated LIVE from the filed source tables
(read-only): chargen-5e.json (v0.1.5), species-class-reskins.json, background-reskins.json,
create-screens-reskins.json. Re-run whenever a source version moves.
"""
import json, os, re, sys, hashlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_PARENT = os.path.abspath(os.path.join(ROOT, ".."))


def _dir_or_none(path):
    return path if path and os.path.isdir(path) else None


def _campaign_root():
    env = os.environ.get("DCC_CAMPAIGN_ROOT")
    if env:
        return os.path.abspath(env)
    for cand in (
        os.path.join(_PARENT, "dcc-campaign"),
        os.path.join(_PARENT, "dcc-crawler-protocol"),
        _PARENT if os.path.isdir(os.path.join(_PARENT, "tables")) else None,
    ):
        hit = _dir_or_none(cand)
        if hit and os.path.isdir(os.path.join(hit, "tables")):
            return hit
    raise SystemExit(
        "Cannot find campaign root. Set DCC_CAMPAIGN_ROOT to the repo root "
        "(the folder that contains tables/)."
    )


def _lore_root(campaign_root):
    env = os.environ.get("DCC_LORE_ROOT")
    if env:
        return os.path.abspath(env)
    for cand in (
        os.path.join(campaign_root, "lore"),
        os.path.join(_PARENT, "dcc-lore"),
        os.path.join(campaign_root, "..", "dcc-lore"),
    ):
        hit = _dir_or_none(os.path.abspath(cand))
        if hit and os.path.isdir(os.path.join(hit, "tables")):
            return hit
    raise SystemExit(
        "Cannot find lore root. Set DCC_LORE_ROOT to the lore folder "
        "(the folder that contains tables/)."
    )


CAMP_ROOT = _campaign_root()
LORE_ROOT = _lore_root(CAMP_ROOT)
CAMP = os.path.join(CAMP_ROOT, "tables")
LORE = os.path.join(LORE_ROOT, "tables")

cg = json.load(open(os.path.join(CAMP, "chargen-5e.json")))
sc = json.load(open(os.path.join(LORE, "species-class-reskins.json")))
bg = json.load(open(os.path.join(CAMP, "background-reskins.json")))
cs = json.load(open(os.path.join(CAMP, "create-screens-reskins.json")))

assert cg["meta"]["version"] == "0.1.6", "chargen-5e.json moved off v0.1.6: re-read the spec and update the draft"

SC = {e["id"]: e for e in sc["entries"]}
BG = {e["id"]: e for e in bg["entries"]}
CS = {e["id"]: e for e in cs["entries"]}


def lab(e):
    return e["combined_label"]


def esc(s):
    return str(s).replace("|", "\\|")


def table(headers, rows, caption=None, cls=None):
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join("---" for _ in headers) + "|")
    for r in rows:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    s = "\n".join(out)
    if caption:
        s += "\n\n*" + caption + "*"
    return s


SPECIES = ["dragonborn", "dwarf", "elf", "gnome", "goliath", "halfling", "human", "orc", "tiefling"]
CLASSES = ["barbarian", "bard", "cleric", "druid", "fighter", "monk", "paladin", "ranger", "rogue", "sorcerer", "warlock", "wizard"]

def t_species():
    rows = []
    for sid in SPECIES:
        e = SC[sid]; d = cg["species"][e["srd_name"]]
        traits = "; ".join(t.replace(" (", " (") for t in d["traits"])
        rows.append([lab(e), f'{d["size"]}, {d["speed"]} ft', traits, d["quirk"]])
    return table(["Our Name (5e Name)", "Size, Speed", "Traits (SRD 5.2)", "Floors 1-2 quirk"], rows,
                 "Source: chargen-5e.json v0.1.6 and species-class-reskins v0.1.5. Dwarf, Elf and Orc darkvision as filed in the chargen table. Traits are named, not reprinted; use the SRD text.")

def t_species_flavor():
    out = []
    for sid in SPECIES:
        e = SC[sid]; d = cg["species"][e["srd_name"]]
        sub = ""
        if "sub" in d:
            sub = f' Choose a **{d["sub"]["label"].lower()}**: ' + ", ".join(
                lab(SC[x["id"]]) for x in sc["entries"] if x.get("parent_id") == sid and x["kind"] == "species_lineage") + "."
        out.append(f'**{lab(e)}.** {e["flavor"]}{sub}')
    return "\n\n".join(out)

LINEAGE_FX = {
    "dragonborn-black": "Acid", "dragonborn-blue": "Lightning", "dragonborn-brass": "Fire", "dragonborn-bronze": "Lightning",
    "dragonborn-copper": "Acid", "dragonborn-gold": "Fire", "dragonborn-green": "Poison", "dragonborn-red": "Fire",
    "dragonborn-silver": "Cold", "dragonborn-white": "Cold",
    "elf-drow": "Darkvision 120 ft; Dancing Lights cantrip", "elf-high": "Prestidigitation cantrip (swappable)", "elf-wood": "Speed 35 ft; Druidcraft cantrip",
    "gnome-forest": "Minor Illusion cantrip; Speak with Animals", "gnome-rock": "Mending and Prestidigitation cantrips; clockwork devices",
    "goliath-cloud": "Cloud's Jaunt: teleport as a Bonus Action", "goliath-fire": "Fire's Burn: extra fire damage on a hit",
    "goliath-frost": "Frost's Chill: extra cold damage and a speed penalty", "goliath-hill": "Hill's Tumble: knock a target prone",
    "goliath-stone": "Stone's Endurance: Reaction to reduce damage", "goliath-storm": "Storm's Thunder: Reaction thunder damage",
    "tiefling-abyssal": "Poison resistance; Poison Spray cantrip", "tiefling-chthonic": "Necrotic resistance; Chill Touch cantrip",
    "tiefling-infernal": "Fire resistance; Fire Bolt cantrip",
}

def t_lineages():
    rows = []
    for e in sc["entries"]:
        if e["kind"] != "species_lineage":
            continue
        fx = LINEAGE_FX[e["id"]]
        parent = SC[e["parent_id"]]["srd_name"]
        if e["parent_id"] == "dragonborn":
            fx = f"Breath Weapon and resistance: {fx}"
        rows.append([lab(e), parent, fx])
    return table(["Our Name (5e Name)", "Species", "Lineage effect (summary)"], rows,
                 "24 lineages. Effect column summarized by the author from SRD 5.2 [VERIFY: the chargen table lists lineage names only; check each effect against the SRD before printing].")

def t_classes():
    rows = []
    for cid in CLASSES:
        e = SC[cid]; c = cg["classes"][e["srd_name"]]
        armor = ", ".join(c["armor"]) if c["armor"] else "none"
        if c.get("unarmored"): armor += " (Unarmored Defense)" if armor == "none" else ""
        saves = "/".join(s.upper() for s in c["saves"])
        rows.append([lab(e), f'd{c["hit_die"]}', saves, armor, str(c["skill_count"])])
    return table(["Our Name (5e Name)", "Hit Die", "Saves", "Armor", "Skills"], rows,
                 "Source: chargen-5e.json v0.1.6. Weapon proficiencies are in the SRD class entries.")

def t_class_flavor():
    out = []
    for cid in CLASSES:
        e = SC[cid]; c = cg["classes"][e["srd_name"]]
        feats = "; ".join(c["features"])
        out.append(f'**{lab(e)}.** {e["flavor"]} *Level 1:* {feats}.')
    return "\n\n".join(out)

def t_class_options():
    rows = []
    for e in sc["entries"]:
        if e["kind"] == "class_option":
            rows.append([lab(e), SC[e["parent_id"]]["srd_name"], e["flavor"]])
    return table(["Our Name (5e Name)", "Class", "What it does"], rows)

def t_fighting_styles():
    rows = []
    for st in cg["classes"]["Fighter"]["choices"][0]["options"]:
        key = "opt-fighting-style-" + re.sub(r"[^a-z]+", "-", st.lower()).strip("-")
        e = CS.get(key)
        rows.append([lab(e) if e else st, e["flavor"] if e else ""])
    return table(["Our Name (5e Name)", "Kiosk line"], rows,
                 "Fighters pick one at level 1. Paladins and Rangers pick theirs at level 2.")

def t_invocations():
    rows = []
    for st in cg["classes"]["Warlock"]["choices"][0]["options"]:
        key = "opt-invocation-" + re.sub(r"[^a-z]+", "-", st.lower().replace("'", "")).strip("-")
        e = CS.get(key)
        rows.append([lab(e) if e else st, e["flavor"] if e else ""])
    return table(["Our Name (5e Name)", "Kiosk line"], rows, "Warlocks pick one invocation at level 1.")

def t_skill_picks():
    rows = []
    for cid in CLASSES:
        e = SC[cid]; c = cg["classes"][e["srd_name"]]
        sk = c["skills"]
        lst = "Any skill" if len(sk) >= 18 else ", ".join(sk)
        rows.append([lab(e), str(c["skill_count"]), lst])
    return table(["Our Name (5e Name)", "Pick", "From"], rows, "Skill names stay plain: rules key on them.")

SRD_BG = ["acolyte", "criminal", "sage", "soldier"]
ABIL = {"str": "Str", "dex": "Dex", "con": "Con", "int": "Int", "wis": "Wis", "cha": "Cha"}
def t_backgrounds():
    rows = []
    for bid in SRD_BG:
        e = BG[bid]; b = cg["backgrounds"][e["srd_name"]]
        feat = BG["feat-" + re.sub(r"[^a-z]+", "-", b["feat"].lower().replace(" (", "-").replace(")", "")).strip("-")]
        pa = [p for p in b["packages"] if p["id"] == "A"][0]["gp"]
        pb = [p for p in b["packages"] if p["id"] == "B"][0]["gp"]
        rows.append([lab(e), "/".join(ABIL[a] for a in b["asi"]), lab(feat), ", ".join(b["skills"]), b["tool"], f"{pa} / {pb}"])
    return table(["Our Name (5e Name)", "Raise", "Origin feat", "Skills", "Tool", "Credits (A kit / B)"], rows,
                 "The four SRD 5.2 backgrounds. Credits: Package A is the kit and its leftover credits; Package B is the credit option.")

def t_bg_flavor():
    out = []
    for bid in SRD_BG:
        e = BG[bid]
        out.append(f'**{lab(e)}.** {e["flavor"]}')
    return "\n\n".join(out)

SRD_FEATS = ["feat-alert", "feat-magic-initiate-cleric", "feat-magic-initiate-druid", "feat-magic-initiate-wizard", "feat-savage-attacker", "feat-skilled"]
def t_feats():
    rows = []
    for fid in SRD_FEATS:
        e = BG[fid]
        rows.append([lab(e), e["flavor"]])
    return table(["Our Name (5e Name)", "Kiosk line"], rows, "The four SRD 5.2 Origin feats (Magic Initiate has three spell-list versions). Human Versatile picks from these four only.")

def t_pointbuy():
    cost = cg["point_buy"]["cost"]
    rows = [[k for k in cost], [v for v in cost.values()]]
    out = "| Score | " + " | ".join(cost.keys()) + " |\n|---|" + "---|" * len(cost) + "\n| Cost | " + " | ".join(str(v) for v in cost.values()) + " |"
    return out + "\n\n*Point buy: " + str(cg["point_buy"]["budget"]) + " points; scores 8 to 15 before bonuses.*"

def t_abilities():
    rows = []
    for k in ["str", "dex", "con", "int", "wis", "cha"]:
        e = CS["ability-" + k]
        rows.append([lab(e), e["flavor"]])
    return table(["Our Name (5e Name)", "What it is"], rows)

def t_stats():
    rows = []
    for k in ["stat-hp", "stat-ac", "stat-initiative", "stat-passive-perception", "stat-proficiency-bonus"]:
        e = CS[k]
        rows.append([lab(e), e["flavor"]])
    return table(["Our Name (5e Name)", "What it is"], rows)

def t_methods():
    rows = []
    for k in ["method-standard-array", "method-point-buy", "method-roll"]:
        e = CS[k]
        rows.append([lab(e), e["flavor"]])
    return table(["Our Name (5e Name)", "What it is"], rows)

ITEM_NAME = {
 "chain_mail": "chain mail", "greatsword": "greatsword", "flail": "flail", "javelin": "javelin", "dungeoneers_pack": "Dungeoneer's Pack",
 "studded": "studded leather armor", "scimitar": "scimitar", "shortsword": "shortsword", "longbow": "longbow", "arrows": "arrows", "quiver": "quiver",
 "greataxe": "greataxe", "handaxe": "handaxe", "explorers_pack": "Explorer's Pack", "leather": "leather armor", "dagger": "dagger",
 "musical_instrument": "musical instrument", "entertainers_pack": "Entertainer's Pack", "chain_shirt": "chain shirt", "shield": "shield", "mace": "mace",
 "holy_symbol": "holy symbol", "priests_pack": "Priest's Pack", "sickle": "sickle", "druidic_focus_staff": "druidic focus (staff)", "herbalism_kit": "herbalism kit",
 "spear": "spear", "artisans_tools": "artisan's tools", "longsword": "longsword", "druidic_focus_sprig": "druidic focus (sprig)", "shortbow": "shortbow",
 "thieves_tools": "thieves' tools", "burglars_pack": "Burglar's Pack", "arcane_focus_crystal": "arcane focus (crystal)", "arcane_focus_orb": "arcane focus (orb)",
 "book": "book", "scholars_pack": "Scholar's Pack", "arcane_focus_staff": "arcane focus (staff)", "robe": "robe", "spellbook": "spellbook",
}
def items_str(items):
    parts = []
    for k, q in items:
        n = ITEM_NAME.get(k, k.replace("_", " "))
        parts.append(f"{q} {n}s" if q > 1 and not n.endswith("s") and k != "javelin" else (f"{q} javelins" if k == "javelin" else (f"{q} {n}" if q > 1 else n)))
    return ", ".join(parts)

def t_packages():
    rows = []
    for cid in CLASSES:
        e = SC[cid]; c = cg["classes"][e["srd_name"]]
        pk = {p["id"]: p for p in c["packages"]}
        a = pk["A"]
        others = []
        for pid in ("B", "C"):
            if pid in pk:
                p = pk[pid]
                others.append(f'{p["gp"]} credits' if not p["items"] else f'kit B: {items_str(p["items"])} + {p["gp"]} credits')
        rows.append([lab(e), items_str(a["items"]) + f' + {a["gp"]} credits', "; ".join(others)])
    return table(["Our Name (5e Name)", "Package A (kit)", "Credit option"], rows,
                 "Source: chargen-5e.json v0.1.6 [VERIFY: package contents and credit amounts were written from memory of SRD 5.2; chargen verify list still open]. Fighters have a second kit (B) and a credit option (C); every other class has Package B as credits only.")

CASTERS = [
 ("bard", "2", "4 prepared", "2"), ("cleric", "3", "4 prepared", "2"), ("druid", "2", "4 prepared", "2"), ("sorcerer", "4", "2 prepared", "2"),
 ("warlock", "2", "2 prepared", "1 (Pact Magic)"), ("wizard", "3", "6 in spellbook, 4 prepared", "2"), ("paladin", "0", "2 prepared", "2"), ("ranger", "0", "2 prepared", "2"),
]
def t_spells():
    rows = []
    for cid, can, l1, slots in CASTERS:
        c = cg["classes"][SC[cid]["srd_name"]]["spells"] if "spells" in cg["classes"][SC[cid]["srd_name"]] else None
        rows.append([lab(SC[cid]), can, l1, slots, {"bard": "Cha", "cleric": "Wis", "druid": "Wis", "sorcerer": "Cha", "warlock": "Cha", "wizard": "Int", "paladin": "Cha", "ranger": "Wis"}[cid]])
    return table(["Our Name (5e Name)", "Cantrips", "Level 1 spells", "Level 1 slots", "Ability"], rows,
                 "Counts per characters/create-flow-spec-5e.md v0.1.13 S11 (SRD 5.2 checked by the rules team). Barbarian, Fighter, Monk and Rogue skip the spells screen.")

def t_screens():
    rows = [
     ["S1", "Welcome and table settings", "Read the table's settings; accept the Terms (declining also continues). Optionally pick a pre-built Crawler.", "Table Settings"],
     ["S2", "Comfort: lines and veils", "Set private lines and veils.", "Table Settings"],
     ["S3", lab(CS["title-s3"]), "Name and pronouns.", "Name, Look and Hook"],
     ["S4", lab(CS["title-s4"]), "Look and hook.", "Name, Look and Hook"],
     ["S5", "Species (Latent Biology)", "Pick one of nine species, then a lineage if it has one.", "Species"],
     ["S6", "Class (Provisional Class)", "Pick one of twelve classes, then its level-1 choices.", "Class"],
     ["S7", "Background (Prior Employment) and Origin feat", "Pick a background and its ability increases.", "Background"],
     ["S8", lab(CS["title-s8"]), "Pick a method and assign six scores.", "Ability Scores"],
     ["S9", lab(CS["title-s9"]), "Fixed proficiencies, then your class picks.", "Skills"],
     ["S10", lab(CS["title-s10"]), "Take each package or its credits; shop the Vending Wall.", "Equipment"],
     ["S11", lab(CS["title-s11"]), "Casters pick cantrips and spells. Others skip.", "Spells"],
     ["S12", "Retired", "Skipped on purpose; the numbers stay stable.", "none"],
     ["S13", "Customer survey (private notes)", "A short private survey. Pass on any question.", "Survey"],
     ["S14", lab(CS["title-s14"]), "Backstory and requested handle.", "Backstory and Handle"],
     ["S15", lab(CS["modal-s15"]), "Standing Orders, Standing Reactions, signature attack.", "Standing Orders"],
     ["S16", lab(CS["title-s16"]), "Review the whole sheet. Edit anything.", "Review and Confirm"],
     ["S17", lab(CS["title-s17"]), "Confirm. The only screen that writes anything.", "Review and Confirm"],
    ]
    return table(["Screen", "Name", "You decide", "Section"], rows, "Sixteen active screens. S12 is retired and never shown.")

def t_gear_examples():
    ir = json.load(open(f"{CAMP}/item-reskins.json"))
    ids = ["longsword", "chain-mail", "quarterstaff", "greataxe", "shortbow", "shield", "dagger", "leather-armor", "spellbook", "robe", "thieves-tools", "explorers-pack"]
    m = {e["srd_id"]: e for e in ir["entries"]}
    rows = []
    for i in ids:
        e = m[i]
        if "Box" in e["combined_label"].split(" (")[0]:
            continue
        rows.append([e["combined_label"]])
    return "\n".join("- " + r[0] for r in rows)


NONSRD_BG = ["artisan", "charlatan", "entertainer", "farmer", "guard", "guide", "hermit", "merchant", "noble", "sailor", "scribe", "wayfarer"]
NONSRD_FEAT = ["feat-crafter", "feat-healer", "feat-lucky", "feat-musician", "feat-tavern-brawler", "feat-tough"]
# Short mechanics summaries in our own words (decision 029: no copied book text, no parenthetical 5e name).
NONSRD_BG_MECH = {
    "artisan": "Ability raises among Str/Dex/Int; tool-and-craft Origin feat; two skills and artisan's tools.",
    "charlatan": "Ability raises among Dex/Con/Cha; deception-leaning Origin feat; two skills and a forgery kit.",
    "entertainer": "Ability raises among Str/Dex/Cha; performance Origin feat; two skills and a musical instrument.",
    "farmer": "Ability raises among Str/Con/Wis; toughing-it-out Origin feat; two skills and a farming tool.",
    "guard": "Ability raises among Str/Wis/Cha; alertness Origin feat; two skills and a gaming set.",
    "guide": "Ability raises among Dex/Con/Wis; magic-initiate-style Origin feat; two skills and a navigator's tools-style kit.",
    "hermit": "Ability raises among Con/Wis/Cha; healer Origin feat; two skills and an herbalism kit.",
    "merchant": "Ability raises among Con/Int/Cha; lucky Origin feat; two skills and navigator's tools.",
    "noble": "Ability raises among Str/Int/Cha; skilled Origin feat; two skills and a gaming set.",
    "sailor": "Ability raises among Str/Dex/Wis; tavern-brawler Origin feat; two skills and navigator's tools.",
    "scribe": "Ability raises among Dex/Int/Wis; skilled Origin feat; two skills and calligrapher's supplies.",
    "wayfarer": "Ability raises among Dex/Wis/Cha; lucky Origin feat; two skills and thieves' tools.",
}
NONSRD_FEAT_MECH = {
    "feat-crafter": "Faster, cheaper crafting of nonmagical items; start with artisan's tools and discounts.",
    "feat-healer": "Stabilize with a kit as a Bonus Action; heal dice when you Treat; kit uses refresh on a Short Rest.",
    "feat-lucky": "A small pool of luck points to reroll your d20 or force an attacker to reroll.",
    "feat-musician": "Encourage allies after a Short or Long Rest; grant temporary Hit Points or Heroic Inspiration.",
    "feat-tavern-brawler": "Improved unarmed strikes; grapple more easily; once per turn deal extra damage on an unarmed or improvised hit.",
    "feat-tough": "Extra hit points equal to twice your level (and +2 HP each time you gain a level).",
}

def t_nonsrd_backgrounds():
    rows = []
    for bid in NONSRD_BG:
        e = BG[bid]
        # reskin name ONLY — no parenthetical 5e name (decision 029)
        rows.append([e["display_name"], NONSRD_BG_MECH[bid]])
    return table(["Reskin name", "Mechanics summary (our words)"], rows,
                 "Appendix only. Sheet stores the underlying 5e background key. Open these only if the table owns the source books.")

def t_nonsrd_feats():
    rows = []
    for fid in NONSRD_FEAT:
        e = BG[fid]
        rows.append([e["display_name"], NONSRD_FEAT_MECH[fid]])
    return table(["Reskin name", "Mechanics summary (our words)"], rows,
                 "Appendix only. Human Versatile does not pick from this list in the printed book (SRD four only).")


TABLES = {k[2:]: v for k, v in globals().items() if k.startswith("t_")}

def main():
    src = open(os.path.join(ROOT, "drafts", "02-crawler-creation.src.md"), encoding="utf-8").read()
    def sub(m):
        name = m.group(1)
        if name not in TABLES:
            sys.exit("no table generator: " + name)
        return TABLES[name]()
    out = re.sub(r"<<TABLE:(\w+)>>", sub, src)
    stamp = {
        "chargen-5e.json": cg["meta"]["version"],
        "species-class-reskins.json": sc["meta"]["version"],
        "background-reskins.json": bg["meta"]["version"],
        "create-screens-reskins.json": cs["meta"]["version"],
    }
    out = out.replace("<<STAMP>>", ", ".join(f"{k} v{v}" for k, v in stamp.items()))
    out = out.replace("cash-only", "credits-only")  # money-word rule: no "cash"
    open(os.path.join(ROOT, "chapters", "02-crawler-creation.md"), "w", encoding="utf-8").write(out)
    print("wrote chapters/02-crawler-creation.md", stamp)

if __name__ == "__main__":
    main()
