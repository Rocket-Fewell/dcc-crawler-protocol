"""Oct 7 2026 (Caleb): every player card shows what a player needs on their turn, computed from the build:
Attacks (to-hit, damage, type, range), Spellcasting (DC, attack, slots left and when they return, known spells),
Features & traits (uses left and recharge), Rests (Hit Dice, party Short Rests today). Plus the /create fixes
(Intake Bag = decision 038, spellbook flag on non-Wizards, Lessons of the First Ones feat flag). Temp campaign dir only."""
import contextlib
import importlib.util
import io
import json
import os
import re
import sys
import tempfile
import unittest
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMPAIGN = os.path.dirname(TOOLS)
spec = importlib.util.spec_from_file_location("state_cards_under_test", os.path.join(TOOLS, "state.py"))
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)
sys.path.insert(0, TOOLS)
import card_rules as cr  # noqa: E402
import publisher as pub  # noqa: E402

with open(os.path.join(CAMPAIGN, "tables", "chargen-5e.json"), encoding="utf-8") as _f:
    CG = json.load(_f)


def raithen_spec(**over):
    """A Dwarf Warlock 1 like the one Hornn made on Oct 7 (Lessons of the First Ones, quarterstaff, a mistaken spellbook)."""
    s = {
        "name": "Raithen", "player": "Hornn", "class": "Warlock", "species": "Dwarf", "level": 1, "hp_max": 12, "ac": 15,
        "abilities": {"str": 7, "dex": 18, "con": 17, "int": 17, "wis": 12, "cha": 19}, "credits": 50,
        "inventory": [
            {"name": "Duct-Taped Mop (Quarterstaff)", "qty": 1, "mechanics": "1d6 bludgeoning, Versatile (1d8). Mastery: Topple.", "category": "weapons", "srd_id": "quarterstaff", "chargen_key": "quarterstaff"},
            {"name": "Glitter-Glued Mop Handle (Arcane Focus (Staff))", "qty": 1, "mechanics": "Quarterstaff that is also your spellcasting focus.", "category": "magic", "srd_id": "arcane-focus-staff", "chargen_key": "arcane_focus_staff"},
            {"name": "Cracked Phone App (Spellbook)", "qty": 1, "mechanics": "Holds your wizard spells; ritual-cast from it.", "category": "magic", "srd_id": "spellbook", "chargen_key": "spellbook"},
            {"name": "Motorcycle Jacket (Leather Armor)", "qty": 1, "mechanics": "AC 11 + Dex. Light armor.", "category": "armor", "srd_id": "leather-armor", "chargen_key": "leather"},
            {"name": "Intake Bag", "qty": 1, "notes": "cosmetic, zero value", "mechanics": "Cosmetic. Holds nothing special.", "category": "gear"}],
        "build": {"hit_die": "d8", "class_choices": {"invocation": "Lessons of the First Ones"}, "origin_feat": "Skilled", "extra_origin_feat": None,
                  "saves": ["wis", "cha"], "passives": {"perception": 13}, "weapon_masteries": [],
                  "spells": {"cantrips": ["Eldritch Blast", "Chill Touch"], "prepared": ["Armor of Agathys", "Witch Bolt"], "spellbook": None},
                  "spell_slots": {"1": 1}, "spellcasting_ability": "cha"},
    }
    s.update(over)
    return s


def _row(key, qty=1):
    it = CG["items"][key]
    return {"name": f"Junk ({it['name']})", "qty": qty, "mechanics": it.get("mechanics", ""), "category": it.get("category", "gear"), "srd_id": it.get("srd_id", key), "chargen_key": key}


def class_spec(cls, level=1, **over):
    """A plain level-N test Crawler for any class: Package A kit, standard array by the class priority, first legal spells."""
    c = CG["classes"][cls]
    arr = sorted(CG["standard_array"], reverse=True)
    ab = {a: arr[i] for i, a in enumerate(c["priority"])}
    inv = [_row(k, q) for k, q in c["packages"][0]["items"] if k in CG["items"] and not CG["items"][k].get("variants")]
    build = {"hit_die": f"d{c['hit_die']}", "class_choices": {ch["key"]: ch["options"][0] for ch in c["choices"] if ch.get("options") and ch["key"] != "weapon_masteries"},
             "origin_feat": "Alert", "saves": c["saves"], "weapon_masteries": []}
    sp = c.get("spells")
    if sp:
        l1 = sp["level1_list"][: (sp.get("spellbook") or sp.get("level1_known") or sp.get("prepared") or 0)]
        build["spells"] = {"cantrips": sp["cantrip_list"][: sp["cantrips"]], "prepared": l1[: sp["prepared"]] if sp.get("spellbook") else l1, "spellbook": l1 if sp.get("spellbook") else None}
        build["spellcasting_ability"] = sp["ability"]
    s = {"name": f"Test {cls}", "player": f"P-{cls}", "class": cls, "species": "Human", "level": level, "hp_max": c["hit_die"] + 2, "ac": 12,
         "abilities": ab, "credits": 0, "inventory": inv, "build": build}
    s.update(over)
    return s


def card(c, data=None):
    return pub.render_card(c, data or {}, [])


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        env = {"DCC_CAMPAIGN_DIR": self.tmp.name, "DCC_CAMPAIGN_ROOT": self.tmp.name, "DCC_AUTO_PUBLISH": "0", "DCC_SESSION": "alpha"}
        p = mock.patch.dict(os.environ, env)
        p.start()
        self.addCleanup(p.stop)
        os.environ.pop("GM_DISCORD_TOKEN", None)
        self.path = os.path.join(self.tmp.name, "sessions", "state.json")
        self.run_cmd("init")

    def run_cmd(self, *argv, expect=0):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = state.main(list(argv))
            except SystemExit as e:
                code = e.code
        self.assertEqual(code, expect, f"{argv}: stdout={out.getvalue()!r} stderr={err.getvalue()!r}")
        return out.getvalue().strip(), err.getvalue().strip()

    def create(self, spec_):
        p = os.path.join(self.tmp.name, f"{spec_['name']}.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(spec_, f)
        self.run_cmd("create-crawler", "--file", p)

    def load(self):
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def crawler(self, name):
        return next(c for c in self.load()["crawlers"] if c["name"] == name)

    def text(self, name, data=None):
        msgs = pub.render_card(self.crawler(name), data or {"party_rests": pub.party_rests_of(self.load())}, [])
        for m in msgs:
            self.assertLess(len(m), 2000)
        return "\n".join(msgs)


class WarlockCardTests(Base):
    def test_raithen_attacks_spellcasting_features_rests(self):
        self.create(raithen_spec())
        t = self.text("Raithen")
        self.assertIn("**Eldritch Blast**: +6 to hit, 1d10 force, 120 ft", t)
        self.assertIn("**Chill Touch**: +6 to hit, 1d10 necrotic, touch (target can't regain HP until the end of your next turn)", t)
        self.assertIn("**Duct-Taped Mop (Quarterstaff)**: +0 to hit, 1d6-2 bludgeoning (1d8-2 two-handed), melee 5 ft", t)
        self.assertEqual(t.count("to hit, 1d6-2 bludgeoning"), 1)   # the staff focus does not add a second quarterstaff line
        self.assertIn("**Spellcasting** (CHA): Save DC 14 | Spell attack +6", t)
        self.assertIn("Pact Magic slots: 1/1 left (level 1), back on a Short Rest", t)
        self.assertIn("- Armor of Agathys (1st):", t)
        self.assertIn("- Witch Bolt (1st): Action, 60 ft, Concentration 1 min: +6 to hit, 2d12 lightning", t)
        self.assertIn("**Darkvision**: 120 ft.", t)
        self.assertIn("Resistance to Poison damage; Advantage on saves to avoid or end Poisoned", t)
        self.assertIn("+1 HP per level (already in your HP)", t)
        self.assertIn("Hit Dice: 1/1 left (d8). Short Rest: spend any, roll each d8+3 (CON)", t)
        self.assertIn("Party Short Rests today: 0/4 used", t)
        # Lessons of the First Ones: the extra Origin feat is flagged, never picked for the player
        self.assertIn("Origin feat: not chosen yet, pick one", t)
        self.assertIn("Origin feat (Lessons of the First Ones): not chosen yet, pick one", t)
        # /create fixes: Intake Bag = decision 038; a spellbook on a non-Wizard is flagged
        self.assertIn("store or retrieve one item in your System Inventory", t)
        self.assertNotIn("Cosmetic. Holds nothing special", t)
        self.assertIn("only Wizards use a spellbook", t)

    def test_new_crawler_gets_resources_and_card_tracks_spending(self):
        self.create(raithen_spec())
        res = {r["name"]: (r["uses"], r["uses_max"], r["uses_reset"]) for r in self.crawler("Raithen")["resources"]}
        self.assertEqual(res["Pact Magic slots"], (1, 1, "short_rest"))
        self.assertEqual(res["Stonecunning"], (2, 2, "long_rest"))
        self.run_cmd("resource", "spend", "Raithen", "Pact Magic slots")
        self.assertIn("Pact Magic slots: 0/1 left (level 1), back on a Short Rest", self.text("Raithen"))
        out, _ = self.run_cmd("rest", "short")
        self.assertIn("Short Rest 1/4 today", out)
        t = self.text("Raithen")
        self.assertIn("Pact Magic slots: 1/1 left", t)
        self.assertIn("Party Short Rests today: 1/4 used", t)
        self.assertNotIn("Resources: Pact Magic", t)   # shown once, in Spellcasting

    def test_lessons_feat_chosen_is_shown(self):
        s = raithen_spec()
        s["build"]["lessons_feat"] = "Alert"
        self.create(s)
        t = self.text("Raithen")
        self.assertNotIn("not chosen yet", t)
        self.assertIn("Origin feat: Alert", t)
        self.assertIn("Initiative +6", t)   # Alert adds the Proficiency Bonus

    def test_card_view_has_rests_and_old_snapshots_do_not_repost(self):
        self.create(raithen_spec())
        st = self.load()
        c = self.crawler("Raithen")
        data = {"party_rests": pub.party_rests_of(st)}
        new = pub.make_view(c, data)
        self.assertEqual(new["party_rests"], {"short_used": 0, "short_max": 4})
        old = {k: v for k, v in new.items() if k != "party_rests"}
        self.assertFalse(pub.views_differ(old, new))
        later = pub.make_view(c, {"party_rests": {"short_used": 2, "short_max": 4}})
        self.assertIn("Party Short Rests 2/4", pub.diff_views(new, later))


class MartialCardTests(Base):
    def test_fighter_second_wind_attacks_no_spellcasting(self):
        self.create(class_spec("Fighter"))
        t = self.text("Test Fighter")
        self.assertIn("**Second Wind**: 2/2 left (regain 1 on a Short Rest, all on a Long Rest)", t)
        self.assertIn("**Junk (Greatsword)**: +4 to hit, 2d6+2 slashing, melee 5 ft; Heavy", t)
        self.assertIn("**Junk (Javelin)** x8: +4 to hit, 1d6+2 piercing, melee 5 ft or thrown 30/120 ft", t)
        self.assertIn("Fighting Style**: Archery: +2 to attack rolls with Ranged weapons", t)
        self.assertNotIn("**Spellcasting**", t)
        self.assertNotIn("Action Surge", t)   # level 2
        self.assertIn("Hit Dice: 1/1 left (d10)", t)

    def test_fighter_archery_adds_to_ranged(self):
        s = class_spec("Fighter")
        s["inventory"] = [_row("longbow")]
        self.create(s)
        self.assertIn("**Junk (Longbow)**: +5 to hit, 1d8+1 piercing, range 150/600 ft", self.text("Test Fighter"))   # DEX 13 +1, PB +2, Archery +2

    def test_barbarian_rage_and_short_rest_regains_one(self):
        self.create(class_spec("Barbarian"))
        t = self.text("Test Barbarian")
        self.assertIn("**Rage**: 2/2 left (regain 1 on a Short Rest, all on a Long Rest)", t)
        self.assertIn("**Junk (Greataxe)**: +4 to hit, 1d12+2 slashing, melee 5 ft; Heavy (+2 while raging)", t)
        self.assertIn("Unarmored Defense", t)
        self.assertNotIn("**Spellcasting**", t)
        self.run_cmd("resource", "spend", "Test Barbarian", "Rage", "--n", "2")
        self.run_cmd("rest", "short")
        self.assertEqual(next(r for r in self.crawler("Test Barbarian")["resources"] if r["name"] == "Rage")["uses"], 1)
        self.run_cmd("rest", "long")
        self.assertEqual(next(r for r in self.crawler("Test Barbarian")["resources"] if r["name"] == "Rage")["uses"], 2)

    def test_rogue_non_caster_and_cunning_action_from_level_2(self):
        self.create(class_spec("Rogue"))
        t = self.text("Test Rogue")
        self.assertNotIn("**Spellcasting**", t)
        self.assertIn("Sneak Attack", t)
        self.assertIn("(Sneak Attack +1d6)", t)
        self.assertNotIn("Cunning Action", t)
        c2 = state.crawler_from_spec(class_spec("Rogue", level=2))
        self.assertIn("Cunning Action", "\n".join(card(c2)))


class RestAndHitDiceTests(Base):
    def test_short_rest_cap_force_long_rest_resets(self):
        self.create(class_spec("Fighter"))
        for i in range(4):
            self.run_cmd("rest", "short")
        _, err = self.run_cmd("rest", "short", expect=1)
        self.assertIn("4/4", err)
        self.run_cmd("rest", "short", "--force", "GM ruling: ritual nap")
        self.run_cmd("hp", "damage", "Test Fighter", "5")
        out, _ = self.run_cmd("rest", "long")
        self.assertIn("Short Rests reset to 0/4", out)
        self.assertEqual(self.crawler("Test Fighter")["hp"]["current"], self.crawler("Test Fighter")["hp"]["max"])
        out, _ = self.run_cmd("rest", "show")
        self.assertIn("0/4", out)

    def test_hit_dice_spend_heal_and_restore(self):
        self.create(class_spec("Fighter"))
        self.run_cmd("hp", "damage", "Test Fighter", "8")
        out, _ = self.run_cmd("hit-dice", "spend", "Test Fighter", "--heal", "6")
        self.assertIn("healed 6", out)
        c = self.crawler("Test Fighter")
        self.assertEqual(c["hit_dice"]["current"], 0)
        self.run_cmd("hit-dice", "spend", "Test Fighter", expect=1)
        self.assertIn("Hit Dice: 0/1 left (d10)", self.text("Test Fighter"))
        self.run_cmd("hit-dice", "restore", "Test Fighter", "--all")
        self.assertEqual(self.crawler("Test Fighter")["hit_dice"]["current"], 1)

    def test_resource_sync_for_an_older_crawler(self):
        self.run_cmd("add-crawler", "Old Lock", "--player", "X", "--class", "Warlock", "--species", "Orc", "--hp-max", "9", "--abilities", "cha=16,dex=14")
        self.assertNotIn("resources", self.crawler("Old Lock"))
        self.run_cmd("resource", "sync", expect=1)   # one Crawler at a time
        out, _ = self.run_cmd("resource", "sync", "Old Lock")
        self.assertIn("+ Pact Magic slots 1/1", out)
        names = [r["name"] for r in self.crawler("Old Lock")["resources"]]
        self.assertIn("Adrenaline Rush", names)
        self.assertIn("Relentless Endurance", names)
        out, _ = self.run_cmd("resource", "sync", "Old Lock")
        self.assertIn("nothing changed", out)


class AllClassesTests(unittest.TestCase):
    """A level-1 card builds for each of the 12 classes, every message under Discord's 2000 characters."""
    CLASSES = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]

    def test_every_class_card(self):
        self.assertEqual(sorted(CG["classes"]), sorted(self.CLASSES))
        for cls in self.CLASSES:
            for level in (1, 2):
                with self.subTest(cls=cls, level=level):
                    c = state.crawler_from_spec(class_spec(cls, level=level))
                    msgs = card(c, {"party_rests": {"short_used": 1, "short_max": 4}})
                    t = "\n".join(msgs)
                    for m in msgs:
                        self.assertLess(len(m), 2000)
                    self.assertIn("**Attacks**", t)
                    self.assertIn("**Unarmed Strike**", t)
                    self.assertIn("**Features & traits**", t)
                    self.assertIn(f"Hit Dice: {level}/{level} left (d{CG['classes'][cls]['hit_die']})", t)
                    self.assertNotIn("could not be computed", t)
                    self.assertNotRegex(t, r"\{[a-z_]+\}")   # no unfilled template field
                    caster = bool(CG["classes"][cls].get("spells"))
                    self.assertEqual("**Spellcasting**" in t, caster)
                    if cls == "Warlock":
                        self.assertIn("back on a Short Rest", t)
                    elif caster:
                        self.assertIn("back on a Long Rest", t)
        expect = {"Barbarian": "Rage", "Bard": "Bardic Inspiration", "Fighter": "Second Wind", "Paladin": "Lay on Hands", "Ranger": "Favored Enemy",
                  "Sorcerer": "Innate Sorcery", "Wizard": "Arcane Recovery", "Warlock": "Pact Magic slots"}
        for cls, name in expect.items():
            names = [r["name"] for r in cr.default_resources(state.crawler_from_spec(class_spec(cls)))]
            self.assertIn(name, names, cls)

    def test_spell_lines_cover_every_chargen_spell(self):
        rules = cr.rules()
        self.assertEqual(sorted(n for n in CG["spells"] if n not in rules["spells"]), [])
        for n, s in rules["spells"].items():
            self.assertTrue(s["line"].strip(), n)
            self.assertIsNone(re.search(r"\{(?!dc\}|atk\}|mod\}|cd\}|beams\})[a-z_]+\}", s["line"]), n)


if __name__ == "__main__":
    unittest.main()


class SyndicateReviewTests(unittest.TestCase):
    """Oct 7 2026 Syndicate review of the 12 sample cards: masteries, level-2 spell counts, Monk 2024 wording and DC, Druid Magician,
    Sorcerer cantrips, Warlock invocations, Ranger Hunter's Mark, Explorer's Pack, Magic Initiate picks."""

    def text(self, spec_):
        msgs = card(state.crawler_from_spec(spec_), {"party_rests": {"short_used": 0, "short_max": 4}})
        for m in msgs:
            self.assertLess(len(m), 2000)
        return "\n".join(msgs)

    def test_mastery_tag_only_on_chosen_weapons(self):
        s = class_spec("Fighter")
        s["build"]["weapon_masteries"] = ["Junk (Greatsword)", "Junk (Javelin)"]
        t = self.text(s)
        self.assertIn("**Junk (Greatsword)**: +4 to hit, 2d6+2 slashing, melee 5 ft; Heavy, Mastery: Graze", t)
        self.assertIn("- **Junk (Greatsword)**: 2d6 slashing, Heavy, Two-Handed. Mastery: Graze.", t)
        self.assertIn("- **Junk (Flail)**: 1d8 bludgeoning.", t)
        self.assertNotIn("Mastery: Sap", t)   # flail not chosen
        self.assertIn("Mastery: Slow", t)
        r = self.text(raithen_spec())   # a Warlock has no Weapon Mastery: no tag anywhere
        self.assertNotIn("Mastery:", r)
        self.assertNotIn("Topple", r)

    def test_level_2_spell_counts_carry_over_level_1(self):
        want = {"Bard": 5, "Cleric": 5, "Druid": 5, "Paladin": 3, "Ranger": 3, "Sorcerer": 4, "Wizard": 5, "Warlock": 3}
        for cls, n in want.items():
            with self.subTest(cls=cls):
                s1, s2 = class_spec(cls), class_spec(cls, level=2)
                self.assertEqual(cr.spell_counts(state.crawler_from_spec(s2))["prepared"], n)
                t = self.text(s2)
                sp = s1["build"]["spells"]
                for name in sp["cantrips"] + sp["prepared"]:
                    self.assertIn(name, t)   # nothing known at level 1 is dropped
                have = len([x for x in sp["prepared"] if not (cls == "Ranger" and x == "Hunter's Mark")])
                self.assertIn(f"Prepared spells {have}/{n}", t)
                if have < n:
                    self.assertIn(f"{n - have} not chosen yet", t)
        w = self.text(class_spec("Wizard", level=2))
        self.assertIn("Spellbook 6/8; **2 not chosen yet", w)

    def test_monk_martial_arts_2024(self):
        s = class_spec("Monk", abilities={"str": 12, "dex": 17, "con": 13, "int": 8, "wis": 15, "cha": 10})
        t = self.text(s)
        self.assertIn("one Unarmed Strike as a Bonus Action each turn (Martial Arts)", t)
        self.assertIn("Grapple/Shove (DC 13 Str or Dex save)", t)   # 8 + Dex 3 + PB 2
        self.assertNotIn("after the Attack action", t)
        self.assertIn("no Attack action needed", t)

    def test_druid_magician_and_cleric_thaumaturge_extra_cantrip(self):
        d = class_spec("Druid")
        d["build"]["class_choices"] = {"primal_order": "Magician"}
        self.assertIn("Cantrips known 2/3 (incl. +1 from Magician)", self.text(d))
        d["build"]["class_choices"] = {"primal_order": "Warden"}
        self.assertIn("Cantrips known 2/2:", self.text(d))
        c = class_spec("Cleric")
        c["build"]["class_choices"] = {"divine_order": "Thaumaturge"}
        self.assertIn("Cantrips known 3/4 (incl. +1 from Thaumaturge)", self.text(c))

    def test_sorcerer_four_class_cantrips_species_extra(self):
        s = class_spec("Sorcerer", species="Tiefling")
        s["build"]["species_choice"] = "Abyssal"
        s["build"]["spells"]["cantrips"] = ["Acid Splash", "Chill Touch", "Fire Bolt", "Dancing Lights"]
        t = self.text(s)
        self.assertIn("Cantrips known 4/4: Acid Splash*, Chill Touch*, Fire Bolt*, Dancing Lights", t)
        self.assertIn("Species cantrips (extra, not counted): Poison Spray, Thaumaturgy", t)

    def test_warlock_invocation_count_by_level(self):
        self.assertIn("**Eldritch Invocations**: 1/1 chosen.", self.text(raithen_spec()))
        t2 = self.text(raithen_spec(level=2, hp_max=20))
        self.assertIn("**Eldritch Invocations**: 1/3 chosen; **2 not chosen yet, pick them.**", t2)
        self.assertIn("Pact Magic slots: 2/2 left (level 1), back on a Short Rest", t2)

    def test_ranger_hunters_mark_always_prepared(self):
        t = self.text(class_spec("Ranger"))
        self.assertIn("Hunter's Mark (1st, always prepared (Favored Enemy), doesn't count)", t)
        self.assertIn("Prepared spells 2/2 (+1 always prepared)", t)
        self.assertNotIn("Hunter's Mark", CG["classes"]["Ranger"]["spells"]["level1_list"])
        self.assertIn("Divine Smite (1st, always prepared (Paladin's Smite)", self.text(class_spec("Paladin", level=2)))

    def test_explorers_pack_2024_contents(self):
        mech = CG["items"]["explorers_pack"]["mechanics"]
        self.assertNotIn("mess kit", mech.lower())
        for x in ("Backpack", "bedroll", "2 oil flasks", "10 days rations", "rope", "tinderbox", "10 torches", "waterskin"):
            self.assertIn(x, mech)

    def test_magic_initiate_picks_on_raithen(self):
        s = raithen_spec()
        s["build"]["lessons_feat"] = "Magic Initiate (Wizard)"
        s["build"]["magic_initiate"] = {"Magic Initiate (Wizard)": {"ability": "cha", "cantrips": ["Shocking Grasp", "Mage Hand"], "level1": ["Shield"]}}
        c = state.crawler_from_spec(s)
        self.assertIn({"name": "Shield free cast", "uses": 1, "uses_max": 1, "uses_reset": "long_rest"}, c["resources"])
        t = "\n".join(card(c))
        self.assertIn("**Shocking Grasp** (Magic Initiate, CHA): +6 to hit, 1d8 lightning, touch (target can't make Opportunity Attacks until the start of its next turn)", t)
        self.assertIn("- Mage Hand (cantrip):", t)
        self.assertIn("- Shield (1st, free once per Long Rest, 1/1 left, or with your Pact Magic slot): Reaction", t)
        self.assertNotIn("not chosen yet", t)
        self.assertIn("Origin feat: Magic Initiate (Wizard)", t)

    def test_magic_initiate_unpicked_and_non_caster(self):
        s = class_spec("Fighter")
        s["build"]["origin_feat"] = "Magic Initiate (Cleric)"
        t = self.text(s)
        self.assertIn("**Not chosen yet: 2 cantrips and one level 1 spell, pick them.**", t)
        self.assertIn("Int, Wis or Cha (not chosen yet)", t)
        self.assertNotIn("**Magic Initiate spells**", t)
        s["build"]["magic_initiate"] = {"Magic Initiate (Cleric)": {"ability": "wis", "cantrips": ["Sacred Flame", "Guidance"], "level1": ["Bless"]}}
        t = self.text(s)
        self.assertIn("**Magic Initiate spells**", t)
        self.assertIn("**Sacred Flame** (Magic Initiate, WIS): DC 11 Dex save", t)   # 8 + PB 2 + Wis 12 (+1)
        self.assertIn("- Bless (1st, free once per Long Rest", t)
        self.assertNotIn("**Spellcasting**", t)

    def test_publish_note_goes_first_on_changed_line(self):
        c = state.crawler_from_spec(raithen_spec())
        msgs = pub.render_card(c, {}, [], {"credits": 50}, ["Refund: Spellbook removed, +50 credits (Vending Wall bug)", "- Cracked Phone App (Spellbook)"])
        self.assertIn("**Changed:** Refund: Spellbook removed, +50 credits (Vending Wall bug); - Cracked Phone App (Spellbook)", "\n".join(msgs))
