"""Busted-guess checker (gm-quirks guess) and the sealed repair log. Everything runs in a temp campaign dir with a temp sealed-roll
FIXTURE built here; the real gm-notes/secret is never read or written. (The quirk table is Lore's public file, not a sealed roll.)"""
import json
import os
import stat
import subprocess
import sys
import unittest
from unittest import mock

import busted
from test_gm_quirks import Base, TABLE, TOOLS, gq, slurp


def fixture_roll(fx, tic, pi=None, quirks=None):
    pi = pi or TABLE["prior_installation"][0]["id"]
    quirks = quirks or [e["id"] for e in TABLE["quirks"][:2]]
    f = next(e for e in TABLE["fixations"] if e["id"] == fx)
    variant = str(f["variants"][0]["values"][0]) if f.get("variants") else None
    rolls = {"prior_installation": pi, "fixation": fx, "fixation_variant": variant, "quirks": quirks, "tic": tic}
    nonce = "ab" * 32
    return {"schema_version": "1.0", "campaign_id": "test", "rolled_at": "2026-10-04T00:00:00-05:00", "rng": "fixture", "nonce": nonce,
            "rolls": rolls, "commitment_sha256": gq.commitment_for(rolls, nonce), "revealed": False}


def entry(table, eid):
    return next(e for t in table.values() if isinstance(t, list) for e in t if isinstance(e, dict) and e.get("id") == eid)


def pick_pair():
    """A fixation and a tic where the fixation's first keyword does NOT grade as the tic (so a wrong kind is a clean miss)."""
    for fx in TABLE["fixations"]:
        kws = fx["affinity"]["trigger_keywords"]
        if not kws:
            continue
        for tic in TABLE["tics"]:
            if not busted.grade("tic", kws[0], [tic]) and not busted.grade("quirk", kws[0], TABLE["quirks"][:2]):
                return fx, tic, kws[0]
    raise unittest.SkipTest("no clean fixation/tic pair in the table")


class PureGrading(unittest.TestCase):
    FX = {"name": "Obsession with Bees", "description": "The unit keeps stopping to admire pollinators.",
          "affinity": {"trigger_keywords": ["bee", "honey", "beehive", "hive mind"], "trigger_themes": ["insects that make honey"]}}

    def test_lenient_on_wording(self):
        for text in ("It is obsessed with bees", "the thing about BEE keeping!", "Honey!", "Bees, always the bees", "a hive mind thing"):
            self.assertTrue(busted.grade("fixation", text, [self.FX]), text)

    def test_strict_on_meaning(self):
        for text in ("It loves the colour yellow", "the unit is fixated on cats", "obsession", "the", "a bee"[0:0] or "zebras"):
            self.assertFalse(busted.grade("fixation", text, [self.FX]), text)

    def test_kind_must_match(self):
        self.assertFalse(busted.grade("tic", "bees", [{"name": "Says Please", "description": "Adds please to orders.", "tells_by_level": {}}]))
        self.assertFalse(busted.grade("nonsense", "bees", [self.FX]))

    def test_derived_keywords_when_no_explicit_list(self):
        e = {"name": "Counts Everything Aloud", "description": "The unit counts steps, doors, ceiling tiles and crawler heads out loud."}
        self.assertTrue(busted.grade("quirk", "it counts things aloud", [e]))
        self.assertTrue(busted.grade("quirk", "counting the ceiling tiles", [e]))
        self.assertFalse(busted.grade("quirk", "it sings", [e]))

    def test_text_checks_and_call_key(self):
        self.assertIsNotNone(busted.check_text("the of and"))
        self.assertIsNotNone(busted.check_text("word " * 40))
        self.assertIsNone(busted.check_text("bees"))
        self.assertEqual(busted.call_key("fixation", "The BEES!"), busted.call_key("fix", "bee, the bees"))
        self.assertNotEqual(busted.call_key("fixation", "bees"), busted.call_key("tic", "bees"))


class GuessBase(Base):
    def setUp(self):
        super().setUp()
        self.assertTrue(os.path.realpath(gq.secret_dir()).startswith(os.path.realpath(self.root)))  # never the real secret dir
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Ann", "--player", "Pat", "--class", "Fighter", "--species", "Human")
        self.run_cmd("add-crawler", "Bo", "--player", "Quin", "--class", "Wizard", "--species", "Human")
        self.fx, self.tic, self.kw = pick_pair()
        os.makedirs(self.secret, mode=0o700, exist_ok=True)
        data = fixture_roll(self.fx["id"], self.tic["id"])
        with open(self.roll_file, "w") as f:
            json.dump(data, f)
        os.chmod(self.roll_file, 0o600)
        self.sealed_words = {self.fx["id"], self.tic["id"], self.fx["name"], self.tic["name"], data["nonce"], data["commitment_sha256"],
                             *self.fx["affinity"]["trigger_keywords"]} - {self.kw}
        self.log = os.path.join(self.secret, "repair-log.jsonl")

    def guess(self, crawler, scene, kind, text, expect=0, floor=8, tell=True):
        if tell:
            self.run_cmd("repair-log", "tell", "--scene", scene, "--floor", str(floor))  # the GM logs that a tell was shown
        return self.run_cmd("gm-quirks", "guess", "--crawler", crawler, "--floor", str(floor), "--scene", scene, "--kind", kind, "--trigger", text, expect=expect)

    def log_rows(self):
        return [json.loads(l) for l in slurp(self.log).splitlines() if l.strip()]

    def call_rows(self):
        return [r for r in self.log_rows() if r["type"] == "busted_call"]


class GuessTests(GuessBase):
    def test_busted_prints_only_busted_and_records_therapy(self):
        out, err = self.guess("Ann", "s1", "fixation", f"it keeps going on about {self.kw}")
        self.assertEqual((out, err), ("Busted", ""))
        row = self.call_rows()[0]
        self.assertEqual((row["type"], row["crawler"], row["result"], row["therapy_unlocked"], row["therapy_min_floor"], row["kind"]),
                         ("busted_call", "Ann", "Busted", True, 8, "fixation"))
        self.assertEqual(row["text"], f"it keeps going on about {self.kw}")

    def test_not_busted_prints_only_not_busted_with_no_other_consequence(self):
        snap = slurp(os.path.join(self.root, "sessions", "state.json"))
        out, err = self.guess("Ann", "s1", "fixation", "zzyzx banana unrelated")
        self.assertEqual((out, err), ("Not busted", ""))
        self.assertEqual(slurp(os.path.join(self.root, "sessions", "state.json")), snap)  # no Stress, no credits, nothing
        row = self.call_rows()[0]
        self.assertEqual((row["result"], row["therapy_unlocked"]), ("Not busted", False))
        self.assertNotIn("stress", json.dumps(row).lower())

    def test_kind_must_be_equal(self):
        out, _ = self.guess("Ann", "s1", "tic", self.kw)
        self.assertEqual(out, "Not busted")
        out, _ = self.guess("Ann", "s2", "fixation", self.kw)
        self.assertEqual(out, "Busted")

    def test_one_call_per_crawler_per_scene(self):
        self.guess("Ann", "s1", "fixation", "zzyzx banana")
        _, err = self.guess("Ann", "s1", "fixation", "plumbus quartz", expect=1)
        self.assertIn("one call per crawler per scene", err)
        out, _ = self.guess("Bo", "s1", "fixation", "plumbus quartz")  # another crawler, same scene: fine
        self.assertEqual(out, "Not busted")
        out, _ = self.guess("Ann", "s2", "fixation", "plumbus quartz")  # next scene: fine, no per-floor limit
        self.assertEqual(out, "Not busted")
        self.assertEqual(len(self.call_rows()), 3)

    def test_repeated_call_is_rejected_even_reworded_and_in_a_new_scene(self):
        self.guess("Ann", "s1", "fixation", "plumbus quartz")
        _, err = self.guess("Ann", "s2", "fixation", "Quartz, the plumbus!", expect=1)
        self.assertIn("cannot be repeated", err)
        self.assertEqual(len(self.call_rows()), 1)
        out, _ = self.guess("Ann", "s3", "tic", "quartz plumbus")  # same words as a different kind is a different call
        self.assertEqual(out, "Not busted")
        out, _ = self.guess("Bo", "s2", "fixation", "plumbus quartz")  # a different crawler may make it
        self.assertEqual(out, "Not busted")

    def test_after_busted_no_more_calls_and_calls_listing(self):
        self.guess("Ann", "s1", "fixation", self.kw)
        _, err = self.guess("Ann", "s2", "fixation", "another thing", expect=1)
        self.assertIn("already Busted", err)
        out, _ = self.run_cmd("repair-log", "calls", "--crawler", "Ann")
        self.assertIn("-> Busted | Therapy unlocked (Floor 8+, 250 x multiplier)", out)
        self.assertIn(self.kw, out)  # the player's own words only

    def test_nothing_sealed_in_output_or_log(self):
        outs = []
        for i, (kind, text) in enumerate([("fixation", "zzyzx"), ("quirk", "plumbus"), ("tic", "quartz"), ("tell", "banana split"), ("fixation", self.kw)]):
            o, e = self.guess("Ann", f"s{i}", kind, text)
            outs += [o, e]
        blob = "\n".join(outs) + slurp(self.log)
        for word in self.sealed_words:
            self.assertNotIn(word.lower(), blob.lower(), word)
        self.assertEqual(set(outs) - {""}, {"Not busted", "Busted"})
        self.assertEqual(stat.S_IMODE(os.stat(self.log).st_mode), 0o600)

    def test_error_paths_do_not_leak_or_touch_the_log(self):
        for args, frag in ((("Ann", "s1", "nonsense", "bees"), "unknown kind"), (("Ann", "s1", "fixation", "the of and"), "needs some words"),
                           (("Zed", "s1", "fixation", "bees"), "unknown crawler")):
            _, err = self.guess(*args, expect=1)
            self.assertIn(frag, err)
            for word in self.sealed_words:
                self.assertNotIn(word.lower(), err.lower())
        self.assertEqual(self.call_rows() if os.path.exists(self.log) else [], [])

    def test_missing_roll_gives_a_generic_error(self):
        os.remove(self.roll_file)
        _, err = self.guess("Ann", "s1", "fixation", "bees", expect=1)
        self.assertEqual(err, "ERROR: could not grade this call")
        self.assertEqual(self.call_rows() if os.path.exists(self.log) else [], [])

    def test_json_mode_is_still_only_the_result(self):
        self.run_cmd("repair-log", "tell", "--scene", "s1", "--floor", "8")
        out, _ = self.run_cmd("gm-quirks", "guess", "--crawler", "Ann", "--floor", "8", "--scene", "s1", "--kind", "fixation", "--trigger", "zzyzx", "--json")
        self.assertEqual(json.loads(out), {"result": "Not busted"})

    def test_standalone_script_entry_point(self):
        self.run_cmd("repair-log", "tell", "--scene", "s1", "--floor", "8")
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "gm_quirks.py"), "guess", "--crawler", "Ann", "--floor", "8", "--scene", "s1", "--kind", "fixation", "--trigger", self.kw],
                           capture_output=True, text=True, env={**os.environ, "DCC_CAMPAIGN_DIR": self.root})
        self.assertEqual((r.returncode, r.stdout.strip(), r.stderr.strip()), (0, "Busted", ""))


class TellGuardTests(GuessBase):
    def test_no_tell_no_call_and_the_sealed_roll_is_not_consulted(self):
        with mock.patch.object(gq, "load_roll", side_effect=AssertionError("sealed roll consulted")), \
                mock.patch.object(gq, "load_table", side_effect=AssertionError("table consulted")):
            for text in ("zzyzx", self.kw):
                _, err = self.guess("Ann", "s1", "fixation", text, expect=1, tell=False)
                self.assertEqual(err, "ERROR: no tell was shown this scene")
        self.assertFalse(os.path.exists(self.log))

    def test_tell_is_per_scene_and_per_floor(self):
        self.run_cmd("repair-log", "tell", "--scene", "s1", "--floor", "8")
        _, err = self.guess("Ann", "s2", "fixation", self.kw, expect=1, tell=False)
        self.assertIn("no tell was shown this scene", err)
        _, err = self.guess("Ann", "s1", "fixation", self.kw, expect=1, floor=9, tell=False)
        self.assertIn("no tell was shown this scene", err)
        out, _ = self.guess("Ann", "s1", "fixation", self.kw, tell=False)
        self.assertEqual(out, "Busted")

    def test_refused_call_does_not_use_up_the_scene(self):
        self.guess("Ann", "s1", "fixation", "plumbus", expect=1, tell=False)
        out, _ = self.guess("Ann", "s1", "fixation", "plumbus")  # GM logs the tell, then the same call is fine
        self.assertEqual(out, "Not busted")

    def test_tell_entry_stores_no_quirk_details_and_is_idempotent(self):
        out, _ = self.run_cmd("repair-log", "tell", "--scene", "s1", "--floor", "8")
        self.assertIn("tell logged for scene s1", out)
        out, _ = self.run_cmd("repair-log", "tell", "--scene", "s1", "--floor", "8")
        self.assertIn("already logged", out)
        rows = self.log_rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(set(rows[0]), {"seq", "ts", "type", "scene", "floor", "prev", "hash"})
        for word in self.sealed_words:
            self.assertNotIn(word.lower(), slurp(self.log).lower())
        self.run_cmd("repair-log", "verify")
        self.run_cmd("repair-log", "tell", "--scene", "", "--floor", "8", expect=1)

    def test_reveal_lists_tells(self):
        self.run_cmd("repair-log", "tell", "--scene", "s1", "--floor", "8")
        out, _ = self.run_cmd("repair-log", "reveal", "--finale")
        self.assertIn("F8 s1: tell shown", out)


class RepairLogTests(GuessBase):
    def add(self, kind="fit", value="B", **kw):
        return self.run_cmd("repair-log", "add", "--kind", kind, "--value", value, "--crawler", "Ann", "--floor", "8", "--scene", "s1", *kw.get("extra", []))

    def test_add_commits_sealed_and_prints_no_value(self):
        out, _ = self.add("fit", "Perfectly Silly")
        self.assertIn("committed #1 (sealed)", out)
        self.assertNotIn("Silly", out.title())
        self.assertEqual(stat.S_IMODE(os.stat(self.log).st_mode), 0o600)
        row = self.log_rows()[0]
        self.assertEqual((row["type"], row["kind"], row["value"], row["prev"]), ("commit", "fit", "Perfectly Silly", "0" * 64))
        self.assertEqual(len(row["nonce"]), 32)

    def test_chain_verifies_and_detects_tampering_and_is_append_only(self):
        self.add("fit", "B")
        self.add("busted", "Warm")
        self.add("rapport", "Cozy")
        self.guess("Ann", "s1", "fixation", "zzyzx")
        first_two = slurp(self.log).splitlines()[:2]
        out, _ = self.run_cmd("repair-log", "verify")
        self.assertIn("chain OK: 5 line(s)", out)
        self.add("fit", "A")
        self.assertEqual(slurp(self.log).splitlines()[:2], first_two)  # earlier lines never rewritten
        rows = self.log_rows()
        self.assertEqual([r["seq"] for r in rows], [1, 2, 3, 4, 5, 6])
        self.assertTrue(all(rows[i]["prev"] == rows[i - 1]["hash"] for i in range(1, 6)))
        text = slurp(self.log).replace('"value":"Warm"', '"value":"Cold"')
        with open(self.log, "w") as f:
            f.write(text)
        _, err = self.run_cmd("repair-log", "verify", expect=1)
        self.assertIn("chain is broken at line 2", err)

    def test_reveal_needs_the_finale_flag(self):
        self.add("fit", "B")
        self.add("rapport", "warm")
        out, err = self.run_cmd("repair-log", "reveal", expect=1)
        self.assertEqual(out, "")
        self.assertIn("sealed until the finale", err)
        self.assertNotIn("Warm", err)
        out, _ = self.run_cmd("repair-log", "reveal", "--finale")
        self.assertIn("Tribute Fit tier = B", out)
        self.assertIn("Rapport word = warm", out)
        self.assertIn("chain head:", out)

    def test_validation(self):
        _, err = self.run_cmd("repair-log", "add", "--kind", "rapport", "--value", "lukewarm", "--crawler", "Ann", "--floor", "8", expect=1)
        self.assertIn("Frosty, Cool, Warm, Cozy", err)
        self.run_cmd("repair-log", "add", "--kind", "bogus", "--value", "x", "--crawler", "Ann", "--floor", "8", expect=2)
        self.assertFalse(os.path.exists(self.log))

    def test_normal_commands_never_print_the_log(self):
        self.add("fit", "SecretTierXyz")
        for argv in (("repair-log", "verify"), ("repair-log", "calls"), ("show",), ("gm-quirks", "status"), ("validate",)):
            out, err = self.run_cmd(*argv)
            self.assertNotIn("SecretTierXyz", out + err)

    def test_log_lives_in_the_secret_dir_and_state_commands_refuse_to_read_it(self):
        self.add("fit", "B")
        self.assertTrue(gq.is_secret_path(self.log))


if __name__ == "__main__":
    unittest.main()
