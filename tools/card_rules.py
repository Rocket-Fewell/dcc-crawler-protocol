#!/usr/bin/env python3
"""card_rules.py - the "on your turn" part of every player-channel card, computed from the Crawler's build (stdlib only).

Reads tables/chargen-5e.json (classes, weapons, spells, species) and tables/card-rules-5e.json (weapon proficiencies,
slot tables, class features with uses and recharge, species traits, origin feats, invocations, one-line spell mechanics).
Nothing here is typed per character: class, level, ability scores, build (choices, feats, spells, masteries) and the
inventory decide every number. Current values come from the state's tracked fields (crawler.resources, hit_dice,
party rest counter), so a spent slot or Rage shows on the next card.

Used by tools/publisher.py (render_card) and tools/state.py (default resources for new Crawlers, `resource sync`, `rest`).
Paths: <campaign root>/tables (DCC_CAMPAIGN_ROOT honored), falling back to the tables beside this checkout.
"""
import json
import math
import os
import re

import dcc_paths as _paths

ABILITIES = ["str", "dex", "con", "int", "wis", "cha"]
ORDINAL = {1: "1st", 2: "2nd", 3: "3rd"}
RESET_TEXT = {"short_rest": "Short Rest", "long_rest": "Long Rest", "session": "session", "day": "day", "floor": "floor", "never": "never"}
STAFF_FOCUS_KEYS = ("arcane_focus_staff", "druidic_focus_staff")
_CACHE = {}


# --------------------------------------------------------------------------- data

def _tables_dirs():
    out = [os.path.join(str(_paths.campaign_root()), "tables")]
    here = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tables")
    if here not in out:
        out.append(here)
    return out


def _load(name):
    for d in _tables_dirs():
        p = os.path.join(d, name)
        try:
            mt = os.stat(p).st_mtime
        except OSError:
            continue
        hit = _CACHE.get(p)
        if hit and hit[0] == mt:
            return hit[1]
        try:
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError):
            continue
        _CACHE[p] = (mt, data)
        return data
    return {}


def rules():
    return _load("card-rules-5e.json")


def chargen():
    return _load("chargen-5e.json")


# --------------------------------------------------------------------------- small helpers

def mod(score):
    try:
        return (int(score) - 10) // 2
    except (TypeError, ValueError):
        return 0


def pb(level):
    return 2 + (max(1, int(level or 1)) - 1) // 4


def signed(n):
    return f"+{n}" if n >= 0 else str(n)


def _dmg(dice, bonus):
    return dice if not bonus else f"{dice}{signed(bonus)}"


def _level(c):
    try:
        return max(1, min(20, int(c.get("level") or 1)))
    except (TypeError, ValueError):
        return 1


def _build(c):
    return c.get("build") if isinstance(c.get("build"), dict) else {}


def _abil(c):
    ab = c.get("abilities") or {}
    return {a: ab.get(a, 10) for a in ABILITIES}


def _by_level(table, level):
    best = None
    for k, v in sorted(((int(k), v) for k, v in (table or {}).items()), key=lambda x: x[0]):
        if k <= level:
            best = v
    return best


def _listify(v):
    if v is None or v == "":
        return []
    return [x for x in (v if isinstance(v, list) else [v]) if x]


def class_choices(c):
    cc = _build(c).get("class_choices")
    return cc if isinstance(cc, dict) else {}


def invocations(c):
    return [str(x) for x in _listify(class_choices(c).get("invocation")) + _listify(class_choices(c).get("invocations"))]


LESSONS = "Lessons of the First Ones"


def lessons_feats(c):
    return [str(x) for x in _listify(_build(c).get("lessons_feat"))]


def lessons_pending(c):
    """How many Lessons of the First Ones origin feats are still unchosen (0 when the invocation is not taken)."""
    return max(0, sum(1 for i in invocations(c) if i == LESSONS) - len(lessons_feats(c)))


def origin_feats(c):
    b = _build(c)
    return [str(f) for f in _listify(b.get("origin_feat")) + _listify(b.get("extra_origin_feat")) + lessons_feats(c)]


def spell_ability(c):
    cls_spells = (((chargen().get("classes") or {}).get(c.get("class")) or {}).get("spells") or {})
    a = _build(c).get("spellcasting_ability") or cls_spells.get("ability")
    return a if a in ABILITIES else None


def is_caster(c):
    return (c.get("class") in (rules().get("spellcasting") or {})) and bool(spell_ability(c))


def spell_numbers(c, ability=None):
    """(ability, save DC, attack bonus) for the class (or a given ability)."""
    a = ability or spell_ability(c)
    if not a:
        return None, None, None
    m = mod(_abil(c)[a])
    p = pb(_level(c))
    return a, 8 + p + m, p + m


def _species_choice(c):
    return _build(c).get("species_choice")


def _species_cantrips(c):
    """Cantrips the species gives (lineage/legacy choice plus fixed traits such as Tiefling Thaumaturgy). Extra: they never count
    against the class's cantrips known."""
    ch = ((rules().get("species_choices") or {}).get(c.get("species")) or {}).get(_species_choice(c))
    out = list(ch.get("cantrips") or []) if isinstance(ch, dict) else []
    for t in (rules().get("species_traits") or {}).get(c.get("species"), []):
        if t.get("min_level", 1) <= _level(c):
            out += [x for x in t.get("cantrips") or [] if x not in out]
    return out


def _class_spells(c):
    return (((chargen().get("classes") or {}).get(c.get("class")) or {}).get("spells")) or {}


def spell_counts(c):
    """What the class allows at this level (2024 tables): cantrips known (incl. Magician/Thaumaturge +1), prepared spells, spellbook size."""
    sc = (rules().get("spellcasting") or {}).get(c.get("class")) or {}
    cs = _class_spells(c)
    lv = _level(c)
    cantrips = _by_level(sc.get("cantrips_by_level") or {}, lv)
    if cantrips is None:
        cantrips = cs.get("cantrips") or 0
    cc = class_choices(c)
    bonus = sum(n for key, n in (cs.get("bonus_cantrips") or {}).items() if cc.get(key.split(":", 1)[0]) == key.split(":", 1)[1])
    prepared = _by_level(sc.get("prepared_by_level") or {}, lv)
    if prepared is None:
        prepared = cs.get("prepared") or cs.get("level1_known") or 0
    book = None
    if sc.get("spellbook_base"):
        book = sc["spellbook_base"] + sc.get("spellbook_per_level", 2) * (lv - 1)
    return {"cantrips": cantrips + bonus, "cantrip_bonus": bonus, "prepared": prepared, "spellbook": book}


def always_prepared(c):
    """[(spell, from feature)] always prepared at this level; they never count against the prepared number."""
    sc = (rules().get("spellcasting") or {}).get(c.get("class")) or {}
    return [(a["spell"], a.get("from", "")) for a in sc.get("always_prepared") or [] if a.get("level", 1) <= _level(c)]


def invocation_count(c):
    sc = (rules().get("spellcasting") or {}).get(c.get("class")) or {}
    return _by_level(sc.get("invocations_by_level") or {}, _level(c)) or 0


def magic_initiate(c):
    """{feat name: {ability, cantrips, level1}} for each Magic Initiate the Crawler has (picks may be empty: not chosen yet)."""
    got = _build(c).get("magic_initiate")
    got = got if isinstance(got, dict) else {}
    out = {}
    for f in origin_feats(c):
        if f.startswith("Magic Initiate") and f not in out:
            g = got.get(f) if isinstance(got.get(f), dict) else {}
            out[f] = {"ability": g.get("ability") if g.get("ability") in ("int", "wis", "cha") else None,
                      "cantrips": [str(x) for x in _listify(g.get("cantrips"))], "level1": [str(x) for x in _listify(g.get("level1"))]}
    return out


def _evaluate_uses(spec, c):
    lv, ab = _level(c), _abil(c)
    if spec is None:
        return None
    if isinstance(spec, bool):
        return None
    if isinstance(spec, int):
        return spec
    if isinstance(spec, dict) and "by_level" in spec:
        return _by_level(spec["by_level"], lv)
    if isinstance(spec, str):
        if spec == "pb":
            return pb(lv)
        if spec == "level":
            return lv
        m = re.fullmatch(r"level\*(\d+)", spec)
        if m:
            return lv * int(m.group(1))
        m = re.fullmatch(r"mod:(\w{3})", spec)
        if m:
            return max(1, mod(ab.get(m.group(1), 10)))
    return None


# --------------------------------------------------------------------------- spell slots

def slot_rows(c):
    """[(resource name, slot level, max, reset)] for the class at its level (pact: one row)."""
    sc = (rules().get("spellcasting") or {}).get(c.get("class"))
    if not sc or not spell_ability(c):
        return []
    table = ((rules().get("slot_tables") or {}).get(sc.get("progression")) or {})
    row = table.get(str(_level(c)))
    if not row:
        return []
    if sc.get("progression") == "pact":
        n, lvl = row
        return [("Pact Magic slots", lvl, n, "short_rest")]
    return [(f"Spell slots L{i}", i, n, "long_rest") for i, n in enumerate(row, 1) if n]


# --------------------------------------------------------------------------- features, traits, feats

def _fill(text, c):
    lv, ab, p = _level(c), _abil(c), pb(_level(c))
    b = _build(c)
    ch = _species_choice(c)
    sc = (rules().get("species_choices") or {}).get(c.get("species")) or {}
    choice = sc.get(ch) if ch else None
    rage = 2 if lv < 9 else 3 if lv < 16 else 4
    ma = "d6" if lv < 5 else "d8" if lv < 11 else "d10" if lv < 17 else "d12"
    bard = "d6" if lv < 5 else "d8" if lv < 10 else "d10" if lv < 15 else "d12"
    masteries = b.get("weapon_masteries") or []
    vals = {
        "level": lv, "pb": p, "half_pb": p // 2, "rage": rage, "ma_die": ma, "bardic_die": bard,
        "sneak": f"{math.ceil(lv / 2)}d6", "cd_dice": f"{1 if lv < 7 else 2 if lv < 13 else 3 if lv < 18 else 4}d8",
        "ki_dc": 8 + p + mod(ab["wis"]), "arcane_recovery": f"{math.ceil(lv / 2)} (half your level, rounded up)",
        "masteries": ", ".join(masteries) if masteries else "your chosen weapons",
        "ancestry_type": (choice if isinstance(choice, str) else "your ancestry's") if c.get("species") == "Dragonborn" else "",
        "elf_darkvision": (choice or {}).get("darkvision", "60 ft") if isinstance(choice, dict) else "60 ft",
        "elf_lineage": (choice or {}).get("text", "Lineage not on file.") if isinstance(choice, dict) else "Lineage not on file.",
        "gnome_lineage": (choice or {}).get("text", "Lineage not on file.") if isinstance(choice, dict) else "Lineage not on file.",
        "tiefling_legacy": (choice or {}).get("text", "Legacy not on file.") if isinstance(choice, dict) else "Legacy not on file.",
        "giant_ancestry": choice if isinstance(choice, str) and c.get("species") == "Goliath" else "Ancestry not on file.",
    }

    class D(dict):
        def __missing__(self, k):
            return "{" + k + "}"
    try:
        return text.format_map(D(vals)).replace("{pb}", str(p))
    except (ValueError, IndexError):
        return text


def feature_entries(c):
    """Every class feature, species trait and origin feat that applies at this level:
    [{group, name, text, resource?: {name, uses_max, reset, short_rest_regain?, unit?}}]."""
    R, lv = rules(), _level(c)
    out = []

    def res(spec, name, reset, regain=None, unit=None):
        mx = _evaluate_uses(spec, c)
        if not mx:
            return None
        r = {"name": name, "uses_max": mx, "reset": reset}
        if regain:
            r["short_rest_regain"] = regain
        if unit:
            r["unit"] = unit
        return r

    cc = class_choices(c)
    for f in (R.get("class_features") or {}).get(c.get("class"), []):
        if f.get("level", 1) > lv:
            continue
        if f.get("invocations"):
            want, have = invocation_count(c), len(invocations(c))
            if want:
                more = max(0, want - have)
                out.append({"group": "class", "name": "Eldritch Invocations", "text": f"{min(have, want)}/{want} chosen" + (f"; **{more} not chosen yet, pick {'it' if more == 1 else 'them'}.**" if more else ".")})
            for inv in invocations(c):
                text = (R.get("invocations") or {}).get(inv, "")
                if inv == LESSONS:
                    got = lessons_feats(c)
                    text += f" Origin feat: {', '.join(got)}." if got else ""
                    if lessons_pending(c):
                        text += " **Origin feat: not chosen yet, pick one.**"
                out.append({"group": "class", "name": f"Invocation: {inv}", "text": text.strip()})
            continue
        if f.get("choice"):
            pick = cc.get(f["choice"])
            text = (f.get("options") or {}).get(pick) if pick else None
            out.append({"group": "class", "name": f["name"], "text": text or "not chosen yet (ask the GM)."})
            continue
        reset = f.get("reset")
        for k, v in sorted(((int(k), v) for k, v in (f.get("reset_by_level") or {}).items())):
            if k <= lv:
                reset = v
        e = {"group": "class", "name": f["name"], "text": _fill(f.get("text", ""), c)}
        if f.get("uses") is not None:
            e["resource"] = res(f["uses"], f.get("resource_name") or f["name"], reset, f.get("short_rest_regain"), f.get("unit"))
        out.append(e)
    for t in (R.get("species_traits") or {}).get(c.get("species"), []):
        if t.get("min_level", 1) > lv:
            continue
        e = {"group": "species", "name": t["name"], "text": _fill(t.get("text", ""), c)}
        spec = t if t.get("uses") is not None else ((t.get("uses_by_choice") or {}).get(_species_choice(c)) or {})
        if spec.get("uses") is not None:
            e["resource"] = res(spec["uses"], spec.get("resource_name") or t.get("resource_name") or t["name"], spec.get("reset"))
        out.append(e)
    seen = set()
    for feat in origin_feats(c):
        meta = (R.get("origin_feats") or {}).get(feat) or {}
        key = feat if feat != "Skilled" else f"Skilled#{len([x for x in seen if x.startswith('Skilled')])}"
        seen.add(key)
        text = meta.get("text", "")
        if feat.startswith("Magic Initiate"):
            mi = magic_initiate(c).get(feat) or {"ability": None, "cantrips": [], "level1": []}
            parts = []
            if mi["cantrips"]:
                parts.append(f"cantrips {', '.join(mi['cantrips'])}" + ("" if len(mi["cantrips"]) >= 2 else f" ({2 - len(mi['cantrips'])} not chosen yet)"))
            if mi["level1"]:
                parts.append(f"level 1 {mi['level1'][0]} (free once per Long Rest)")
            missing = []
            if not mi["cantrips"]:
                missing.append("2 cantrips")
            if not mi["level1"]:
                missing.append("one level 1 spell")
            spells = ("Spells: " + "; ".join(parts) + "." if parts else "") + (f" **Not chosen yet: {' and '.join(missing)}, pick them.**" if missing else "")
            text = text.replace("{mi_spells}", spells.strip()).replace("{mi_ability}", mi["ability"].upper() if mi["ability"] else "Int, Wis or Cha (not chosen yet)")
        e = {"group": "feat", "name": f"Origin feat: {feat}", "text": _fill(text, c)}
        rname = meta.get("resource_name") or feat
        if feat.startswith("Magic Initiate") and (magic_initiate(c).get(feat) or {}).get("level1"):
            rname = f"{magic_initiate(c)[feat]['level1'][0]} free cast"   # e.g. "Shield free cast" (1/Long Rest)
        if meta.get("uses") is not None and rname not in {x.get("resource", {}).get("name") for x in out if x.get("resource")}:
            e["resource"] = res(meta["uses"], rname, meta.get("reset"))
        out.append(e)
    if lessons_pending(c) and not any(e["name"] == f"Invocation: {LESSONS}" for e in out):
        out.append({"group": "feat", "name": "Origin feat", "text": "**not chosen yet, pick one.**"})
    return out


def default_resources(c):
    """Tracked resources a Crawler of this class/level/build starts with (all full): spell slots, then features."""
    out = [{"name": n, "uses": mx, "uses_max": mx, "uses_reset": reset} for n, _lvl, mx, reset in slot_rows(c)]
    for e in feature_entries(c):
        r = e.get("resource")
        if r and not any(x["name"].lower() == r["name"].lower() for x in out):
            row = {"name": r["name"], "uses": r["uses_max"], "uses_max": r["uses_max"], "uses_reset": r["reset"]}
            if r.get("short_rest_regain"):
                row["short_rest_regain"] = r["short_rest_regain"]
            out.append(row)
    return out


def sync_resources(c):
    """Add every missing default resource (full) and bring the max/reset of default-named ones up to date (level-up).
    Never removes a resource and never refills one. Returns a list of change lines."""
    changes = []
    have = c.setdefault("resources", [])
    for d in default_resources(c):
        cur = next((r for r in have if str(r.get("name", "")).lower() == d["name"].lower()), None)
        if cur is None:
            have.append(dict(d))
            changes.append(f"+ {d['name']} {d['uses']}/{d['uses_max']} ({d['uses_reset'].replace('_', ' ')})")
            continue
        if cur.get("uses_max") != d["uses_max"]:
            gain = d["uses_max"] - (cur.get("uses_max") or 0)
            cur["uses_max"] = d["uses_max"]
            cur["uses"] = max(0, min(d["uses_max"], (cur.get("uses") or 0) + max(0, gain)))
            changes.append(f"{d['name']} max -> {d['uses_max']}")
        if cur.get("uses_reset") != d["uses_reset"]:
            cur["uses_reset"] = d["uses_reset"]
            changes.append(f"{d['name']} now resets per {d['uses_reset'].replace('_', ' ')}")
        if d.get("short_rest_regain") and cur.get("short_rest_regain") != d["short_rest_regain"]:
            cur["short_rest_regain"] = d["short_rest_regain"]
    return changes


# --------------------------------------------------------------------------- attacks

def _weapon_profs(c):
    R = rules()
    profs = set((R.get("weapon_proficiency") or {}).get(c.get("class"), ["simple"]))
    for key, extra in (R.get("choice_weapon_proficiency") or {}).items():
        k, v = key.split(":", 1)
        if class_choices(c).get(k) == v:
            profs.update(extra)
    return profs


def _proficient(c, kind, props):
    profs = _weapon_profs(c)
    if kind in profs or kind is None:
        return True
    if kind == "martial":
        if "martial:finesse" in profs and "Finesse" in props:
            return True
        if "martial:light" in profs and "Light" in props:
            return True
    return False


def _parse_weapon(text):
    m = re.search(r"(\d+d\d+|\b\d+\b)\s+(acid|bludgeoning|cold|fire|force|lightning|necrotic|piercing|poison|psychic|radiant|slashing|thunder)", text or "", re.I)
    if not m:
        return None
    props = []
    for p in ("Finesse", "Light", "Heavy", "Two-Handed", "Loading", "Reach"):
        if re.search(rf"\b{p}\b", text, re.I):
            props.append(p)
    vers = re.search(r"Versatile\s*\(?\s*(\d+d\d+)", text, re.I)
    thrown = re.search(r"Thrown\s*\((\d+)/(\d+)\)", text, re.I)
    ammo = re.search(r"Ammunition\s*\((\d+)/(\d+)\)", text, re.I)
    mastery = re.search(r"Mastery:\s*([A-Za-z]+)", text)
    magic = re.search(r"\+(\d)\s+(?:bonus\s+)?to\s+attack\s+and\s+damage", text, re.I)
    return {"dice": m.group(1), "type": m.group(2).lower(), "props": props, "versatile": vers.group(1) if vers else None,
            "thrown": thrown.groups() if thrown else None, "ammo": ammo.groups() if ammo else None,
            "mastery": mastery.group(1) if mastery else None, "magic": int(magic.group(1)) if magic else 0}


def _weapon_base(it):
    """(chargen weapon item or None, base key) for an inventory row: by chargen key, srd id, or '(Base Name)' in the name."""
    items = chargen().get("items") or {}
    key = it.get("chargen_key")
    if key in STAFF_FOCUS_KEYS:
        return items.get("quarterstaff"), "quarterstaff"
    if key in items and items[key].get("weapon"):
        return items[key], key
    sid = it.get("srd_id")
    for k, v in items.items():
        if v.get("weapon") and sid and v.get("srd_id") == sid:
            return v, k
    if sid in ("arcane-focus-staff", "druidic-focus-wooden-staff"):
        return items.get("quarterstaff"), "quarterstaff"
    for inner in reversed(re.findall(r"\(([^()]+)\)", it.get("name", ""))):
        for k, v in items.items():
            if v.get("weapon") and v.get("name", "").lower() == inner.strip().lower():
                return v, k
    return None, None


def _has_mastery(c, base_key, base_name):
    for m in _build(c).get("weapon_masteries") or []:
        low = str(m).lower()
        inner = re.findall(r"\(([^()]+)\)", low)
        cand = inner[-1].strip() if inner else low.strip()
        if cand in (str(base_key).replace("_", " "), str(base_name).lower()) or low == str(base_key):
            return True
    return False


def item_mechanics_text(c, row, text):
    """An inventory line's mechanics with the weapon's Mastery tag kept only when the Crawler chose that weapon's mastery
    (build.weapon_masteries). Text only: the stored item is never changed."""
    if not text or not isinstance(row, dict):
        return text
    base, key = _weapon_base(row)
    if base is None or _has_mastery(c, key, base.get("name", "")):
        return text
    names = sorted({str((v.get("weapon") or {}).get("mastery")) for v in (chargen().get("items") or {}).values() if (v.get("weapon") or {}).get("mastery")})
    out = re.sub(r"\s*Mastery:\s*[A-Za-z]+\.?", "", text)
    if names:
        out = re.sub(r",\s*(?:" + "|".join(map(re.escape, names)) + r")(?=\))", "", out)
    return out.strip()


def weapon_attacks(c):
    ab, lv = _abil(c), _level(c)
    p = pb(lv)
    cls = c.get("class")
    style = class_choices(c).get("fighting_style")
    blade = cls == "Warlock" and "Pact of the Blade" in invocations(c)
    rows, seen_bases = [], set()
    inv = [i for i in c.get("inventory") or [] if isinstance(i, dict)]
    has_real_staff = any(_weapon_base(i)[1] == "quarterstaff" and i.get("chargen_key") not in STAFF_FOCUS_KEYS for i in inv)
    for it in inv:
        base, key = _weapon_base(it)
        if it.get("chargen_key") in STAFF_FOCUS_KEYS or it.get("srd_id") in ("arcane-focus-staff", "druidic-focus-wooden-staff"):
            if has_real_staff:
                continue   # one Quarterstaff line is enough
        own = _parse_weapon(it.get("mechanics") or "")
        if base is None and not (own and (it.get("category") == "weapons")):
            continue
        info = own if (own and base is None) else (_parse_weapon(base.get("mechanics", "")) if base else own)
        if own and base is not None and own.get("magic"):
            info = dict(info, magic=own["magic"])
        if not info:
            continue
        w = (base or {}).get("weapon") or {}
        kind = w.get("kind")
        ranged = w.get("range") == "ranged" or bool(info["ammo"])
        props = info["props"]
        if ranged:
            a = "dex"
        elif "Finesse" in props:
            a = "dex" if ab["dex"] > ab["str"] else "str"
        else:
            a = "str"
        monk_weapon = cls == "Monk" and not ranged and (kind == "simple" or (kind == "martial" and "Light" in props))
        if monk_weapon and ab["dex"] > ab[a]:
            a = "dex"
        if blade and not ranged and ab["cha"] > ab[a]:
            a = "cha"
        m = mod(ab[a])
        prof = _proficient(c, kind, props) or blade
        hit = m + (p if prof else 0) + info["magic"] + (2 if style == "Archery" and ranged else 0)
        dice = info["dice"]
        if monk_weapon:
            ma = "1d6" if lv < 5 else "1d8" if lv < 11 else "1d10" if lv < 17 else "1d12"
            if int(ma.split("d")[1]) > int(dice.split("d")[-1]) and dice.startswith("1d"):
                dice = ma
        dbonus = m + info["magic"]
        notes = []
        if style == "Dueling" and not ranged and "Two-Handed" not in props:
            dbonus += 2
            notes.append("Dueling +2 incl.")
        if style == "Thrown Weapon Fighting" and info["thrown"]:
            notes.append("+2 damage when thrown")
        dmg = f"{_dmg(dice, dbonus)} {info['type']}"
        if info["versatile"] and not monk_weapon:
            dmg += f" ({_dmg(info['versatile'], dbonus - (2 if style == 'Dueling' else 0))} two-handed)"
        if ranged:
            rng = f"range {info['ammo'][0]}/{info['ammo'][1]} ft" if info["ammo"] else "ranged"
        else:
            rng = "melee 10 ft" if "Reach" in props else "melee 5 ft"
            if info["thrown"]:
                rng += f" or thrown {info['thrown'][0]}/{info['thrown'][1]} ft"
        extra = [x for x in props if x in ("Light", "Heavy", "Loading", "Finesse")]
        if info["mastery"] and _has_mastery(c, key, (base or {}).get("name", "")):
            extra.append(f"Mastery: {info['mastery']}")
        if cls == "Barbarian" and a == "str" and not ranged:
            notes.append(f"+{2 if lv < 9 else 3 if lv < 16 else 4} while raging")
        if cls == "Rogue" and (ranged or "Finesse" in props):
            notes.append(f"Sneak Attack +{math.ceil(lv / 2)}d6")
        if blade and a == "cha":
            notes.append("Pact of the Blade (Cha)")
        if not prof:
            notes.append("not proficient")
        qty = f" x{it['qty']}" if (it.get("qty") or 1) > 1 else ""
        label = it.get("name", "?")
        rows.append(f"- **{label}**{qty}: {signed(hit)} to hit, {dmg}, {rng}" + (f"; {', '.join(extra)}" if extra else "") + (f" ({'; '.join(notes)})" if notes else ""))
        seen_bases.add(key)
    # unarmed strike: every Crawler has one
    feats = origin_feats(c)
    sm = mod(ab["str"])
    if cls == "Monk":
        a = "dex" if ab["dex"] > ab["str"] else "str"
        ma = "1d6" if lv < 5 else "1d8" if lv < 11 else "1d10" if lv < 17 else "1d12"
        dmg = f"{_dmg(ma, mod(ab[a]))} bludgeoning"
        hit = mod(ab[a]) + p
        tail = "; one Unarmed Strike as a Bonus Action each turn (Martial Arts)"
    elif style == "Unarmed Fighting":
        hit, dmg, tail = sm + p, f"{_dmg('1d6', sm)} bludgeoning (1d8 with both hands free)", ""
    elif "Tavern Brawler" in feats:
        hit, dmg, tail = sm + p, f"{_dmg('1d4', sm)} bludgeoning", ""
    else:
        hit, dmg, tail = sm + p, f"{max(0, 1 + sm)} bludgeoning", ""
    dc = 8 + p + (max(sm, mod(ab["dex"])) if cls == "Monk" else sm)   # Martial Arts: Grapple/Shove DC may use Dex
    rows.append(f"- **Unarmed Strike**: {signed(hit)} to hit, {dmg}, melee 5 ft; or Grapple/Shove (DC {dc} Str or Dex save){tail}")
    return rows


def _cantrip_dice(dice, lv):
    n = 1 if lv < 5 else 2 if lv < 11 else 3 if lv < 17 else 4
    cnt, size = dice.split("d")
    return f"{int(cnt) * n}d{size}"


def spell_attacks(c):
    """Attack cantrips the Crawler knows (class cantrips, lineage cantrips), with numbers filled in."""
    lv = _level(c)
    sdata = rules().get("spells") or {}
    known = list(((_build(c).get("spells") or {}).get("cantrips")) or [])
    rows = []
    sp_ab = spell_ability(c)
    lineage = [x for x in _species_cantrips(c) if x not in known]
    mi_src = {}
    for feat, mi in magic_initiate(c).items():
        for n in mi["cantrips"]:
            if n not in known and n not in lineage and n not in mi_src:
                mi_src[n] = mi["ability"]
    for name in known + lineage + list(mi_src):
        att = (sdata.get(name) or {}).get("attack")
        if not att:
            continue
        ab_ = sp_ab
        tag = ""
        if name in lineage:
            if not ab_:
                ab_ = max(("int", "wis", "cha"), key=lambda a: _abil(c)[a])
            tag = f" ({c.get('species')} trait, {ab_.upper()})"
        elif name in mi_src:
            ab_ = mi_src[name] or ab_ or max(("int", "wis", "cha"), key=lambda a: _abil(c)[a])
            tag = f" (Magic Initiate, {ab_.upper()}{'' if mi_src[name] else '; ability not chosen yet'})"
        _a, dc, atk = spell_numbers(c, ab_)
        if att.get("scale") == "beams":
            beams = 1 if lv < 5 else 2 if lv < 11 else 3 if lv < 17 else 4
            dmg = f"{att['dice']} {att['type']}" + (f" x{beams} beams" if beams > 1 else "")
        else:
            dmg = f"{_cantrip_dice(att['dice'], lv)} {att['type']}"
        roll = f"{signed(atk)} to hit" if att.get("roll") == "attack" else f"DC {dc} {att.get('save', '').capitalize()} save"
        rider = f" ({att['rider']})" if att.get("rider") else ""
        rows.append(f"- **{name}**{tag}: {roll}, {dmg}, {att['range']}{rider}")
    if c.get("species") == "Dragonborn":
        dtype = ((rules().get("species_choices") or {}).get("Dragonborn") or {}).get(_species_choice(c)) or "ancestry"
        n = 1 if lv < 5 else 2 if lv < 11 else 3 if lv < 17 else 4
        dc = 8 + mod(_abil(c)["con"]) + pb(lv)
        rows.append(f"- **Breath Weapon** (replaces one attack): DC {dc} Dex save, {n}d10 {dtype} (half on a success), 15-ft cone or 30-ft line")
    return rows


# --------------------------------------------------------------------------- card blocks

def _find_res(c, name):
    for r in c.get("resources") or []:
        if isinstance(r, dict) and str(r.get("name", "")).lower() == name.lower():
            return r
    return None


def _recharge_text(reset, regain=None):
    if regain:
        return f"regain {regain} on a Short Rest, all on a Long Rest"
    if reset == "short_rest":
        return "back on a Short or Long Rest"
    if reset == "long_rest":
        return "back on a Long Rest"
    return f"resets per {RESET_TEXT.get(reset, str(reset).replace('_', ' '))}"


def _uses_text(c, r):
    """'2/2 left (regain 1 on a Short Rest, all on a Long Rest)' from the tracked resource when there is one, else the computed max."""
    cur = _find_res(c, r["name"])
    mx = r["uses_max"]
    left = cur.get("uses") if isinstance(cur, dict) and isinstance(cur.get("uses"), int) else mx
    mx = cur.get("uses_max") if isinstance(cur, dict) and isinstance(cur.get("uses_max"), int) else mx
    unit = f" {r['unit']}" if r.get("unit") else ""
    if isinstance(cur, dict) and cur.get("uses_reset"):   # the tracked record wins (a GM may have set another reset)
        reset = re.sub(r"[\s-]+", "_", str(cur["uses_reset"]).strip().lower())
        return f"{left}/{mx}{unit} left ({_recharge_text(reset, cur.get('short_rest_regain'))})"
    return f"{left}/{mx}{unit} left ({_recharge_text(r.get('reset'), r.get('short_rest_regain'))})"


def tracked_names(c):
    """Lower-case names of resources the combat blocks already show (the publisher's generic Resources line skips them)."""
    names = {n.lower() for n, *_ in slot_rows(c)}
    names |= {e["resource"]["name"].lower() for e in feature_entries(c) if e.get("resource")}
    return names


def header_line(c):
    ab, lv = _abil(c), _level(c)
    p = pb(lv)
    init = mod(ab["dex"]) + (p if "Alert" in origin_feats(c) else 0)
    sp = (chargen().get("species") or {}).get(c.get("species"), {}).get("speed", 30)
    ch = ((rules().get("species_choices") or {}).get(c.get("species")) or {}).get(_species_choice(c))
    if isinstance(ch, dict) and ch.get("speed"):
        sp = ch["speed"]
    if c.get("class") == "Monk" and lv >= 2:
        sp += 10 if lv < 6 else 15 if lv < 10 else 20 if lv < 14 else 25 if lv < 18 else 30
    if c.get("class") == "Barbarian" and lv >= 5:
        sp += 10
    saves = [s for s in (_build(c).get("saves") or ((chargen().get("classes") or {}).get(c.get("class")) or {}).get("saves") or [])]
    sv = " ".join(f"{a.upper()} {signed(mod(ab[a]) + (p if a in saves else 0))}" for a in ABILITIES)
    pp = (_build(c).get("passives") or {}).get("perception")
    head = f"Initiative {signed(init)} | Speed {sp} ft | Proficiency +{p}" + (f" | Passive Perception {pp}" if pp else "")
    return head + f"\nSaves: {sv}" + (f" (proficient: {', '.join(s.upper() for s in saves)})" if saves else "")


def attacks_block(c):
    rows = spell_attacks(c) + weapon_attacks(c)
    return "**Attacks**\n" + header_line(c) + "\n" + "\n".join(rows)


def _spell_line(c, n, label, ability):
    lv = _level(c)
    _a, dc, atk = spell_numbers(c, ability)
    vals = {"dc": dc, "atk": signed(atk), "mod": mod(_abil(c)[ability]), "cd": 1 if lv < 5 else 2 if lv < 11 else 3 if lv < 17 else 4,
            "beams": "1 beam" if lv < 5 else f"{1 if lv < 5 else 2 if lv < 11 else 3 if lv < 17 else 4} beams"}
    text = ((rules().get("spells") or {}).get(n) or {}).get("line") or ((chargen().get("spells") or {}).get(n) or {}).get("effect") or "see the SRD."
    try:
        text = text.format(**vals)
    except (KeyError, IndexError, ValueError):
        pass
    return f"- {n} ({label}): {text}"


def magic_initiate_lines(c):
    """Lines for each Magic Initiate with picks: its ability, DC/attack, cantrips and the level 1 spell (free once per Long Rest, or with slots)."""
    out = []
    sdata = rules().get("spells") or {}
    pact = ((rules().get("spellcasting") or {}).get(c.get("class")) or {}).get("progression") == "pact"
    for feat, mi in magic_initiate(c).items():
        if not (mi["cantrips"] or mi["level1"]):
            continue
        ab = mi["ability"] or spell_ability(c) or max(("int", "wis", "cha"), key=lambda a: _abil(c)[a])
        _a, dc, atk = spell_numbers(c, ab)
        out.append(f"{feat} ({ab.upper()}{'' if mi['ability'] else ', ability not chosen yet'}): Save DC {dc} | Spell attack {signed(atk)}")
        att = [n for n in mi["cantrips"] if (sdata.get(n) or {}).get("attack")]
        if att:
            out.append(f"Cantrips with numbers in Attacks: {', '.join(att)}")
        out += [_spell_line(c, n, "cantrip", ab) for n in mi["cantrips"] if n not in att]
        for n in mi["level1"][:1]:
            r = _find_res(c, f"{n} free cast")
            left = f" {r.get('uses')}/{r.get('uses_max')} left," if isinstance(r, dict) and isinstance(r.get("uses"), int) else ""
            slots = "or with your Pact Magic slot" if pact else ("or with a spell slot" if slot_rows(c) else "")
            out.append(_spell_line(c, n, f"1st, free once per Long Rest,{left} {slots}".rstrip(", ").replace(",,", ","), ab))
    return out


def spellcasting_block(c):
    if not is_caster(c):
        mi = magic_initiate_lines(c)
        return "**Magic Initiate spells**\n" + "\n".join(mi) if mi else None
    lv = _level(c)
    a, dc, atk = spell_numbers(c)
    sc = (rules().get("spellcasting") or {}).get(c.get("class")) or {}
    lines = [f"**Spellcasting** ({a.upper()}): Save DC {dc} | Spell attack {signed(atk)}"]
    rows = slot_rows(c)
    if sc.get("progression") == "pact" and rows:
        name, slvl, mx, reset = rows[0]
        cur = _find_res(c, name)
        left = cur.get("uses") if cur and isinstance(cur.get("uses"), int) else mx
        lines.append(f"{sc.get('label', 'Pact Magic')} slots: {left}/{mx} left (level {slvl}), back on a Short Rest")
    elif rows:
        parts = []
        for name, slvl, mx, reset in rows:
            cur = _find_res(c, name)
            left = cur.get("uses") if cur and isinstance(cur.get("uses"), int) else mx
            parts.append(f"{ORDINAL.get(slvl, f'{slvl}th')} {left}/{mx}")
        lines.append(f"Spell slots left: {', '.join(parts)}; back on a Long Rest")
    sp = _build(c).get("spells") if isinstance(_build(c).get("spells"), dict) else {}
    sdata = rules().get("spells") or {}
    cg = chargen().get("spells") or {}
    vals = {"dc": dc, "atk": signed(atk), "mod": mod(_abil(c)[a]), "cd": 1 if lv < 5 else 2 if lv < 11 else 3 if lv < 17 else 4,
            "beams": "1 beam" if lv < 5 else f"{1 if lv < 5 else 2 if lv < 11 else 3 if lv < 17 else 4} beams"}

    def line_for(n, label):
        text = (sdata.get(n) or {}).get("line") or (cg.get(n) or {}).get("effect") or "see the SRD."
        try:
            text = text.format(**vals)
        except (KeyError, IndexError, ValueError):
            pass
        return f"- {n} ({label}): {text}"

    counts = spell_counts(c)
    prepared = [n for n in (sp.get("prepared") or []) if n]
    always = [(n, src) for n, src in always_prepared(c)]
    always_names = {n for n, _src in always}
    counted = [n for n in prepared if n not in always_names]
    cantrips = [n for n in (sp.get("cantrips") or []) if n]
    species = [n for n in _species_cantrips(c) if n not in cantrips]

    def pending(n):
        return f"; **{n} not chosen yet, pick {'one' if n == 1 else 'them'}**" if n > 0 else ""
    if counts["cantrips"] or cantrips:
        att = [n for n in cantrips if (sdata.get(n) or {}).get("attack")]
        names = [f"{n}*" if n in att else n for n in cantrips]
        extra = f" (incl. +{counts['cantrip_bonus']} from {class_choices(c).get('primal_order') or class_choices(c).get('divine_order')})" if counts["cantrip_bonus"] else ""
        lines.append(f"Cantrips known {len(cantrips)}/{counts['cantrips']}{extra}: {', '.join(names) or 'none'}{pending(counts['cantrips'] - len(cantrips))}" + (" (* numbers in Attacks)" if att else ""))
        for n in cantrips:
            if n not in att:
                lines.append(line_for(n, "cantrip"))
    if species:
        lines.append(f"Species cantrips (extra, not counted): {', '.join(species)}")
    book = [n for n in (sp.get("spellbook") or []) if n]
    if counts["spellbook"]:
        lines.append(f"Spellbook {len(book)}/{counts['spellbook']}{pending(counts['spellbook'] - len(book))}")
    lines.append(f"Prepared spells {len(counted)}/{counts['prepared']}{pending(counts['prepared'] - len(counted))}" + (f" (+{len(always)} always prepared)" if always else ""))
    for n in counted:
        lvl = (cg.get(n) or {}).get("level", 1)
        lines.append(line_for(n, ORDINAL.get(lvl, f"{lvl}th")))
    for n, src in always:
        lvl = (cg.get(n) or {}).get("level", 1)
        lines.append(line_for(n, f"{ORDINAL.get(lvl, f'{lvl}th')}, always prepared ({src}), doesn't count"))
    rest = [n for n in book if n not in prepared]
    if rest:
        lines.append(f"Also in your spellbook (prepare after a Long Rest): {', '.join(rest)}")
    lines += magic_initiate_lines(c)
    return "\n".join(lines)


def features_block(c):
    ents = feature_entries(c)
    if not ents:
        return None
    lines = ["**Features & traits**"]
    for e in ents:
        u = f" {_uses_text(c, e['resource'])}." if e.get("resource") else ""
        text = e.get("text") or ""
        lines.append(f"- **{e['name']}**:{u} {text}".rstrip())
    return "\n".join(lines)


def rests_block(c, party_rests=None):
    hd = c.get("hit_dice") or {}
    die = _build(c).get("hit_die") or (f"d{((chargen().get('classes') or {}).get(c.get('class')) or {}).get('hit_die')}" if ((chargen().get('classes') or {}).get(c.get('class')) or {}).get('hit_die') else "d?")
    cm = mod(_abil(c)["con"])
    pr = party_rests or {}
    used = pr.get("short_used", 0) or 0
    mx = pr.get("short_max") or (rules().get("rests") or {}).get("short_rests_per_day", 4)
    short = sorted({n for n, *_r, reset in [(n, l, m, r) for n, l, m, r in slot_rows(c)] if reset == "short_rest"} |
                   {e["resource"]["name"] for e in feature_entries(c) if e.get("resource") and (e["resource"].get("reset") == "short_rest" or e["resource"].get("short_rest_regain"))})
    lines = ["**Rests**",
             f"Hit Dice: {hd.get('current', '?')}/{hd.get('max', '?')} left ({die}). Short Rest: spend any, roll each {die}{signed(cm)} (CON) and regain that many HP.",
             f"Party Short Rests today: {used}/{mx} used. Long Rest (saferoom only): all HP, all Hit Dice and every use back."]
    if short:
        lines.append(f"Back on a Short Rest: {', '.join(short)}.")
    return "\n".join(lines)


def combat_blocks(c, party_rests=None):
    """The card's turn blocks in order: Attacks, Spellcasting (casters only), Features & traits, Rests. Never raises:
    a broken table or odd record gives a short notice instead, so the rest of the card still posts."""
    out = []
    for fn in (attacks_block, spellcasting_block, features_block):
        try:
            b = fn(c)
        except Exception as e:  # noqa: BLE001 - a card must still post
            b = f"({fn.__name__.replace('_block', '')} could not be computed: {type(e).__name__}; ask the GM)"
        if b:
            out.append(b)
    try:
        out.append(rests_block(c, party_rests))
    except Exception as e:  # noqa: BLE001
        out.append(f"(rests could not be computed: {type(e).__name__})")
    return out
