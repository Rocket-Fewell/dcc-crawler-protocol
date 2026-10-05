"""state.py create-crawler: build{}, public tags, object opt-outs, death saves, unique intake tag, party cap."""
import json
import os
import unittest

from test_state import StateTestCase, state as state_mod


class CreateCrawlerTests(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.run_cmd("init")

    def spec(self, name, tag="CRAWLER #0001-A", **kw):
        s = {"name": name, "player": name.lower(), "class": "Fighter", "species": "Human", "abilities": {"str": 15, "dex": 12, "con": 14, "int": 8, "wis": 10, "cha": 13},
             "hp_max": 12, "ac": 16, "credits": 3, "intake_tag": tag,
             "credit_breakdown": [{"delta": 10, "reason": "Starting credits: Fighter package A", "source": "intake"},
                                  {"delta": -7, "reason": "Vending Wall: Rope", "source": "intake"}],
             "fan_profile": {"quirks": [], "notes": "Q1: x", "opt_outs": [{"kind": "line", "topic": "spiders", "shared": False}]},
             "build": {"hit_die": "d10", "skills": ["Athletics"], "created_via": "create-flow"}}
        s.update(kw)
        p = os.path.join(self.tmp.name, name + ".json")
        with open(p, "w") as f:
            json.dump(s, f)
        return p

    def test_fields_are_copied(self):
        out, err = self.run_cmd("create-crawler", "--file", self.spec("Ann"))
        c = self.load()["crawlers"][0]
        self.assertEqual(c["build"]["hit_die"], "d10")
        self.assertNotIn("public_tags", c["fan_profile"])  # S12 retired: fan_profile is GM-only
        self.assertEqual(c["fan_profile"]["opt_outs"][0]["topic"], "spiders")
        self.assertEqual(c["death_saves"], {"successes": 0, "fails": 0})
        self.assertEqual(c["credits"], 3)
        _, err = self.run_cmd("ledger", "verify")
        self.assertNotIn("PROBLEM", err.upper())

    def test_duplicate_intake_tag_refused(self):
        self.run_cmd("create-crawler", "--file", self.spec("Ann"))
        _, err = self.run_cmd("create-crawler", "--file", self.spec("Bea"), expect=1)
        self.assertIn("intake tag", err)
        self.assertEqual(len(self.load()["crawlers"]), 1)

    def test_party_cap(self):
        for i, n in enumerate(["Ann", "Bea", "Cy", "Di"]):
            self.run_cmd("create-crawler", "--file", self.spec(n, tag=f"CRAWLER #000{i}-A"))
        _, err = self.run_cmd("create-crawler", "--file", self.spec("Ed", tag="CRAWLER #0009-A"), expect=1)
        self.assertIn("party full", err)
        self.assertEqual(len(self.load()["crawlers"]), 4)

    def test_validator_rejects_bad_opt_out_and_tags(self):
        self.run_cmd("create-crawler", "--file", self.spec("Ann"))
        st = self.load()
        st["crawlers"][0]["fan_profile"]["opt_outs"] = [5]
        errs, _ = state_mod.validate_state(st)
        self.assertTrue(any("opt_outs" in e for e in errs))

    def test_card_shows_build_but_never_fan_tags_or_private(self):
        import publisher  # noqa
        self.run_cmd("create-crawler", "--file", self.spec("Ann"))
        c = self.load()["crawlers"][0]
        text = "\n".join(publisher.render_card(c, {}))
        self.assertNotIn("Fan tags", text)  # S12 retired: the stored profile is GM-only
        self.assertIn("Skills: Athletics", text)
        self.assertNotIn("spiders", text)
        self.assertNotIn("Q1: x", text)


if __name__ == "__main__":
    unittest.main()


class PetKindTests(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.run_cmd("init")

    def test_pets_do_not_count_toward_the_party_cap(self):
        def mk(name, kind=None, tag=None):
            s = {"name": name, "player": name, "class": "Fighter", "species": "Dog", "abilities": {k: 10 for k in ("str", "dex", "con", "int", "wis", "cha")}, "hp_max": 5, "ac": 12}
            if kind:
                s["kind"] = kind
                s["owner"] = "Ann"
            p = os.path.join(self.tmp.name, name + ".json")
            with open(p, "w") as f:
                json.dump(s, f)
            return p
        for n in ("A", "B", "C", "D"):
            self.run_cmd("create-crawler", "--file", mk(n))
        self.run_cmd("create-crawler", "--file", mk("Biscuit", kind="pet"))  # 5th crawler, but a pet
        self.run_cmd("create-crawler", "--file", mk("E"), expect=1)           # a 5th PLAYER is still refused
        st = self.load()
        self.assertEqual(len(st["crawlers"]), 5)
        self.assertEqual(st["crawlers"][4]["kind"], "pet")
        self.assertNotIn("kind", st["crawlers"][0])
        self.run_cmd("create-crawler", "--file", mk("F", kind="dragon"), expect=1)


class ObjectOptOutTests(unittest.TestCase):
    def test_gm_filter_reads_object_form_opt_outs(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("gmq", os.path.join(os.path.dirname(__file__), "..", "gm_quirks.py"))
        gmq = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gmq)
        crawlers = [{"fan_profile": {"opt_outs": [{"kind": "line", "topic": "spiders", "shared": False}, "clowns"]}}]
        self.assertTrue(gmq._opt_out_hit(crawlers, ["a joke about spiders"], []))
        self.assertTrue(gmq._opt_out_hit(crawlers, ["clowns"], []))
        self.assertFalse(gmq._opt_out_hit(crawlers, ["a joke about cats"], []))
