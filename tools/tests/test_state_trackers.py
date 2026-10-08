"""Oct 7 2026 (s1 post-session) state gaps: death saves, pet HP, class resources, healer's kit uses, skill proficiencies,
enemy stat blocks; and the card shows the crawler-facing ones but never the enemy blocks. Temp campaign dir only."""
import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("state_trackers_under_test", os.path.join(TOOLS, "state.py"))
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)
sys.path.insert(0, TOOLS)
import publisher as pub  # noqa: E402


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
        self.run_cmd("add-crawler", "Shirayuki", "--player", "Grimm", "--class", "Fighter", "--species", "Elf", "--hp-max", "12", "--abilities", "str=16,dex=14,con=12,int=10,wis=13,cha=8")
        self.run_cmd("add-crawler", "Eisenhorn", "--player", "Hornn", "--class", "Rogue", "--species", "Human", "--hp-max", "10", "--abilities", "int=7,dex=16,wis=12")

    def run_cmd(self, *argv, expect=0):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = state.main(list(argv))
            except SystemExit as e:
                code = e.code
        self.assertEqual(code, expect, f"{argv}: stdout={out.getvalue()!r} stderr={err.getvalue()!r}")
        return out.getvalue().strip(), err.getvalue().strip()

    def load(self):
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def crawler(self, name):
        return next(c for c in self.load()["crawlers"] if c["name"] == name)

    def card(self, name):
        return "\n".join(pub.render_card(self.crawler(name), {}))


class DeathSaveTests(Base):
    def test_successes_to_stable_and_reset(self):
        self.run_cmd("death-save", "success", "Shirayuki", expect=1)   # not at 0 HP
        self.run_cmd("hp", "damage", "Shirayuki", "12")
        self.run_cmd("death-save", "success", "Shirayuki")
        self.run_cmd("death-save", "fail", "Shirayuki")
        self.assertEqual(self.crawler("Shirayuki")["death_saves"], {"successes": 1, "fails": 1})
        out, _ = self.run_cmd("death-save", "success", "Shirayuki", "--n", "2")
        self.assertIn("STABLE", out)
        c = self.crawler("Shirayuki")
        self.assertEqual(c["death_saves"], {"successes": 0, "fails": 0})
        self.assertIn("Stable", c["conditions"])
        self.run_cmd("death-save", "success", "Shirayuki", expect=1)   # already stable
        out, _ = self.run_cmd("death-save", "fail", "Shirayuki")      # damage while stable
        self.assertIn("no longer Stable", out)
        self.assertNotIn("Stable", self.crawler("Shirayuki")["conditions"])

    def test_three_fails_reports_death_but_gm_confirms(self):
        self.run_cmd("hp", "set", "Eisenhorn", "0")
        out, _ = self.run_cmd("death-save", "fail", "Eisenhorn", "--n", "3")
        self.assertIn("3 FAILS", out)
        self.assertEqual(self.crawler("Eisenhorn")["death_saves"]["fails"], 3)
        self.assertNotIn("Dead", self.crawler("Eisenhorn")["conditions"])

    def test_heal_resets_counters(self):
        self.run_cmd("hp", "set", "Shirayuki", "0")
        self.run_cmd("death-save", "fail", "Shirayuki", "--n", "2")
        out, _ = self.run_cmd("hp", "heal", "Shirayuki", "3")
        self.assertIn("death saves reset", out)
        self.assertEqual(self.crawler("Shirayuki")["death_saves"], {"successes": 0, "fails": 0})

    def test_nat20_back_to_one_hp(self):
        self.run_cmd("hp", "set", "Shirayuki", "0")
        self.run_cmd("condition", "add", "Shirayuki", "Unconscious")
        self.run_cmd("death-save", "fail", "Shirayuki")
        self.run_cmd("death-save", "nat20", "Shirayuki")
        c = self.crawler("Shirayuki")
        self.assertEqual(c["hp"]["current"], 1)
        self.assertEqual(c["death_saves"], {"successes": 0, "fails": 0})
        self.assertNotIn("Unconscious", c["conditions"])

    def test_stabilize_with_healers_kit_spends_a_use(self):
        out, _ = self.run_cmd("inventory", "add", "Eisenhorn", "Healer's Kit", "--uses", "10")
        kit = self.crawler("Eisenhorn")["inventory"][0]
        self.assertEqual((kit["uses"], kit["uses_max"], kit["uses_reset"]), (10, 10, "never"))
        self.run_cmd("hp", "set", "Shirayuki", "0")
        self.run_cmd("death-save", "fail", "Shirayuki")
        out, _ = self.run_cmd("death-save", "stabilize", "Shirayuki", "--kit", "Eisenhorn")
        self.assertIn("9/10 uses left", out)
        self.assertEqual(self.crawler("Eisenhorn")["inventory"][0]["uses"], 9)
        self.assertIn("Stable", self.crawler("Shirayuki")["conditions"])
        self.run_cmd("death-save", "stabilize", "Shirayuki", "--kit", "Shirayuki", expect=1)   # no kit
        self.run_cmd("inventory", "add", "Eisenhorn", "Rope", "--uses", "0", expect=1)
        self.run_cmd("inventory", "add", "Eisenhorn", "Rope", "--uses", "2", "--uses-reset", "fortnight", expect=1)

    def test_death_saves_on_card_and_card_change(self):
        self.run_cmd("hp", "set", "Shirayuki", "0")
        self.assertIn("Death saves: 0 successes / 0 fails", self.card("Shirayuki"))   # dying: always shown
        self.run_cmd("death-save", "fail", "Shirayuki")
        self.assertIn("Death saves: 0 successes / 1 fails", self.card("Shirayuki"))


class PetHpTests(Base):
    def setUp(self):
        super().setUp()
        self.run_cmd("pet", "add", "Eisenhorn", "--name", "Rawlee", "--species", "Raccoon", "--override", "test", "--hp-max", "4")

    def test_damage_heal_set_and_card(self):
        out, _ = self.run_cmd("pet", "hp", "Eisenhorn", "--damage", "3")
        self.assertIn("HP 4 -> 1/4", out)
        self.run_cmd("pet", "hp", "Eisenhorn", "--heal", "10")
        self.assertEqual(self.crawler("Eisenhorn")["pet"]["hp_current"], 4)
        out, _ = self.run_cmd("pet", "hp", "Eisenhorn", "--to", "0")
        self.assertIn("AT 0 HP", out)
        self.assertIn("HP 0/4", self.card("Eisenhorn"))
        self.run_cmd("pet", "hp", "Eisenhorn", expect=1)
        self.run_cmd("pet", "hp", "Eisenhorn", "--damage", "1", "--heal", "1", expect=1)
        self.run_cmd("pet", "hp", "Shirayuki", "--damage", "1", expect=1)   # no pet


class ResourceTests(Base):
    def test_add_spend_reset_card(self):
        out, _ = self.run_cmd("resource", "add", "Shirayuki", "Second Wind", "--max", "2", "--per", "short rest")
        self.assertIn("Second Wind 2/2 (short rest)", out)
        self.run_cmd("resource", "add", "Shirayuki", "Second Wind", "--max", "2", expect=1)
        self.run_cmd("resource", "add", "Shirayuki", "Action Surge", "--max", "1", "--per", "long_rest")
        self.run_cmd("resource", "spend", "Shirayuki", "second")
        self.run_cmd("resource", "spend", "Shirayuki", "Action Surge")
        self.run_cmd("resource", "spend", "Shirayuki", "Action Surge", expect=1)   # none left
        # Oct 7 2026 card: a class feature's tracked uses show once, on its Features line (tracked reset wins); others stay on Resources
        card = self.card("Shirayuki")
        self.assertIn("**Second Wind**: 1/2 left (back on a Short or Long Rest)", card)
        self.assertIn("Resources: Action Surge 0/1 per long rest", card)
        self.assertNotIn("Resources: Second Wind", card)
        out, _ = self.run_cmd("uses", "reset", "--per", "short_rest")
        self.assertIn("1 class resource(s)", out)
        rs = {r["name"]: r["uses"] for r in self.crawler("Shirayuki")["resources"]}
        self.assertEqual(rs, {"Second Wind": 2, "Action Surge": 0})
        self.run_cmd("resource", "set", "Shirayuki", "Action Surge", "--to", "1")
        self.run_cmd("resource", "set", "Shirayuki", "Action Surge", "--to", "5", expect=1)
        self.run_cmd("resource", "remove", "Shirayuki", "Action Surge")
        out, _ = self.run_cmd("resource", "show")
        self.assertIn("Shirayuki: Second Wind 2/2", out)
        self.assertIn("Eisenhorn: none", out)
        self.run_cmd("resource", "add", "Shirayuki", "Rage", "--max", "2", "--per", "fortnight", expect=1)

    def test_item_reset_message_unchanged_without_resources(self):
        self.run_cmd("inventory", "add", "Eisenhorn", "Cap", "--uses", "1", "--uses-reset", "session")
        self.run_cmd("uses", "spend", "Eisenhorn", "Cap")
        out, _ = self.run_cmd("uses", "reset")
        self.assertTrue(out.startswith("refilled 1 item(s) that reset per session"), out)


class ProficiencyTests(Base):
    def test_add_list_mod_and_card(self):
        self.run_cmd("proficiency", "add", "Eisenhorn", "sleight-of-hand")
        self.run_cmd("proficiency", "add", "Eisenhorn", "Stealth", "--expertise")
        self.run_cmd("proficiency", "add", "Eisenhorn", "Juggling", expect=1)
        self.run_cmd("proficiency", "add", "Eisenhorn", "Thieves' Tools", "--other")
        c = self.crawler("Eisenhorn")
        self.assertEqual(c["proficiencies"], ["Sleight of Hand", "Stealth", "Thieves' Tools"])
        self.assertEqual(c["expertise"], ["Stealth"])
        out, _ = self.run_cmd("proficiency", "mod", "Eisenhorn", "investigation")
        self.assertIn("Investigation -2", out)
        self.assertIn("not proficient", out)
        out, _ = self.run_cmd("proficiency", "mod", "Eisenhorn", "stealth")
        self.assertIn("Stealth +7", out)   # DEX 16 (+3) + 2x prof 2
        out, _ = self.run_cmd("proficiency", "mod", "Eisenhorn", "Sleight of Hand")
        self.assertIn("+5", out)
        self.assertIn("Skill proficiencies: Sleight of Hand, Stealth, Thieves' Tools (expertise: Stealth)", self.card("Eisenhorn"))
        self.run_cmd("proficiency", "remove", "Eisenhorn", "Stealth")
        c = self.crawler("Eisenhorn")
        self.assertNotIn("Stealth", c["proficiencies"])
        self.assertNotIn("Stealth", c["expertise"])

    def test_build_skills_are_the_fallback_and_seed(self):
        def fn(s):
            next(c for c in s["crawlers"] if c["name"] == "Shirayuki")["build"] = {"skills": ["Athletics", "perception"]}
            return s, None
        state.mutate(fn)
        out, _ = self.run_cmd("proficiency", "list", "Shirayuki")
        self.assertIn("from the creation build", out)
        out, _ = self.run_cmd("proficiency", "mod", "Shirayuki", "Athletics")
        self.assertIn("+5", out)
        self.run_cmd("proficiency", "add", "Shirayuki", "Survival")
        self.assertEqual(self.crawler("Shirayuki")["proficiencies"], ["Athletics", "Perception", "Survival"])
        card = self.card("Shirayuki")
        self.assertIn("Skill proficiencies: Athletics, Perception, Survival", card)
        self.assertNotIn("Skills: Athletics", card)   # the build line is replaced, not duplicated


class EnemyTests(Base):
    def test_encounter_blocks_one_line_each_and_never_on_cards(self):
        self.run_cmd("enemy", "start", "Shooting Gallery")
        out, _ = self.run_cmd("enemy", "add", "Mannequin", "--ac", "14", "--hp", "13", "--to-hit", "5", "--damage", "shortbow 1d6+3", "--notes", "vuln bludgeoning", "--count", "3")
        self.assertIn("Mannequin 1: AC 14 | HP 13/13 | +5 to hit | shortbow 1d6+3 | vuln bludgeoning", out)
        out, _ = self.run_cmd("enemy", "damage", "Mannequin 2", "20")
        self.assertIn("HP 0/13 DOWN", out)
        self.run_cmd("enemy", "heal", "Mannequin 2", "4")
        self.run_cmd("enemy", "damage", "Mannequin", "3", expect=1)   # ambiguous
        self.run_cmd("enemy", "set", "Mannequin 3", "--ac", "16", "--notes", "half cover")
        self.run_cmd("enemy", "add", "Mannequin 1", "--hp", "5", expect=1)   # duplicate name
        self.run_cmd("enemy", "start", "Other", expect=1)   # one active encounter
        out, _ = self.run_cmd("enemy", "list")
        self.assertIn("Mannequin 2: AC 14 | HP 4/13", out)
        self.assertIn("Mannequin 3: AC 16", out)
        out, _ = self.run_cmd("show")
        self.assertIn("Encounter (GM only): Shooting Gallery", out)
        self.run_cmd("validate")
        for name in ("Shirayuki", "Eisenhorn"):
            card = self.card(name)
            self.assertNotIn("Mannequin", card)
            self.assertNotIn("encounter", json.dumps(pub.make_view(self.crawler(name), {})).lower())
        self.run_cmd("enemy", "remove", "Mannequin 1")
        out, _ = self.run_cmd("enemy", "clear")
        self.assertIn("2 enemy blocks removed", out)
        self.assertNotIn("encounter", self.load())
        self.run_cmd("enemy", "add", "Bruiser", "--ac", "18", expect=1)   # no --hp
        self.run_cmd("enemy", "add", "Bruiser", "--ac", "18", "--hp", "33")   # auto-creates the encounter
        self.assertEqual(self.load()["encounter"]["enemies"][0]["hp"], {"current": 33, "max": 33})

    def test_old_saves_without_new_fields_validate_and_bad_new_fields_are_refused(self):
        s = self.load()
        errs, _ = state.validate_state(s)
        self.assertEqual(errs, [])
        s["encounter"] = {"name": "x", "enemies": [{"name": "A", "hp": {"current": 5, "max": 3}}]}
        s["crawlers"][0]["resources"] = [{"name": "Rage", "uses": 3, "uses_max": 2, "uses_reset": "long_rest"}]
        s["crawlers"][0]["proficiencies"] = "Athletics"
        errs, _ = state.validate_state(s)
        self.assertTrue(any("enemy 'A'" in e for e in errs))
        self.assertTrue(any("resource 'Rage'" in e for e in errs))
        self.assertTrue(any("proficiencies must be an array" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
