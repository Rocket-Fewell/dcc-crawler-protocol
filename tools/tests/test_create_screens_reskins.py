"""tables/create-screens-reskins.json (the /create screens display layer): hash + companion, content rules, flag switch, source map. Fixture text is placeholder only."""
import contextlib
import hashlib
import io
import json
import os
import shutil
import tempfile
import unittest

from test_state import TOOLS
import sys
sys.path.insert(0, TOOLS)
import create_screens_reskins as cs  # noqa: E402

LIVE_TABLES = os.path.join(os.path.dirname(TOOLS), "tables")


def row(i, old, new, state="text", **kw):
    ph = lambda s: ["{" + x + "}" for x in cs.PH.findall(s)]
    r = {"id": i, "screen": "S3", "kind": "notice", "state": state, "old": old, "new": new, "placeholders": ph(new), "old_placeholders": ph(old),
         "chargen_ref": None, "code_ref": None, "source_match": "found", "needs_code": False}
    r.update(kw)
    return r


def write(dirp, rows, version=True, name="create-screens-reskins.json"):
    p = os.path.join(dirp, name)
    with open(p, "w") as f:
        json.dump({"schema": cs.SCHEMA, "meta": {"version": "9.9.9"}, "entries": rows}, f)
    if version:
        with open(os.path.join(dirp, "create-screens-reskins.version.json"), "w") as f:
            json.dump({"version": "9.9.9", "sha256": hashlib.sha256(open(p, "rb").read()).hexdigest()}, f)
    return p


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.t = self.tmp.name
        shutil.copy(os.path.join(LIVE_TABLES, "chargen-5e.json"), self.t)
        self._env = os.environ.pop("CREATE_SCREENS_RESKINS_PATH", None)

    def tearDown(self):
        if self._env is not None:
            os.environ["CREATE_SCREENS_RESKINS_PATH"] = self._env
        self.tmp.cleanup()

    def errs(self, rows):
        return cs.check(path=write(self.t, rows), tables=self.t)["errors"]


class Content(Fixture):
    def test_clean_rows_pass(self):
        rep = cs.check(path=write(self.t, [row("a", "Pick {n} skills", "PLACEHOLDER pick {n}"), row("b", "Roll 3d6", "PLACEHOLDER roll 3d6")]), tables=self.t)
        self.assertEqual(rep["hash"]["status"], "ok")
        self.assertEqual(rep["errors"], [])

    def test_lost_placeholder_number_champs_crawler(self):
        e = self.errs([row("a", "Pick {n} skills", "PLACEHOLDER pick skills"), row("b", "Roll 3d6", "PLACEHOLDER roll dice"), row("c", "Hi", "PLACEHOLDER champs"), row("d", "Hi", "PLACEHOLDER crawler")])
        self.assertTrue(any(x.startswith("a:") and "placeholders" in x for x in e), e)
        self.assertTrue(any(x.startswith("b:") and "numbers" in x for x in e), e)
        self.assertTrue(any(x.startswith("c:") and "champs" in x for x in e), e)
        self.assertTrue(any(x.startswith("d:") and "capitalised" in x for x in e), e)

    def test_documented_renames_are_allowed_others_are_not(self):
        ok = row("hint-s8-method-line", "{method} is here", "PLACEHOLDER {method_label} is here")
        self.assertEqual(self.errs([ok]), [])
        bad = row("other", "{method} is here", "PLACEHOLDER {method_label} is here")
        self.assertTrue(self.errs([bad]))

    def test_label_rule(self):
        good = row("l", "Edit", "Rewrite It (Edit)", state="label", kind="button", display_name="Rewrite It", srd_name="Edit", combined_label="Rewrite It (Edit)")
        self.assertEqual(self.errs([good]), [])
        bad = dict(good, id="m", combined_label="Rewrite It [Edit]")
        self.assertTrue(self.errs([bad]))

    def test_length_warning_and_strict(self):
        r = row("t", "Hi", "x" * 60, kind="modal_title")
        rep = cs.check(path=write(self.t, [r]), tables=self.t)
        self.assertEqual(rep["errors"], [])
        self.assertEqual(len(rep["warnings"]), 1)
        self.assertEqual(cs.main(["--path", write(self.t, [r]), "--strict"]), 1)

    def test_plain_on_must_be_a_list_of_the_known_views_and_a_backticked_command_is_not_prose(self):
        self.assertEqual(self.errs([row("a", "Hi", "PLACEHOLDER hi", plain_on=["S1", "S13", "comfort_only"])]), [])
        self.assertTrue(self.errs([row("b", "Hi", "PLACEHOLDER hi", plain_on=["S99"])]))
        self.assertEqual(self.errs([row("c", "Run /crawlers", "PLACEHOLDER run `/crawlers`")]), [])
        self.assertEqual(self.errs([row("hint-money-cp", "{n} cp", "{amount} credits")]), [])

    def test_duplicate_id_and_bad_schema(self):
        self.assertTrue(self.errs([row("a", "x", "y"), row("a", "x", "z")]))
        p = write(self.t, [row("a", "x", "y")])
        d = json.load(open(p)); d["schema"] = "nope"
        json.dump(d, open(p, "w"))
        self.assertTrue(any("schema" in e for e in cs.check(path=p, tables=self.t)["errors"]))


class Hash(Fixture):
    def test_absent_is_exit_zero(self):
        self.assertEqual(cs.check(path=os.path.join(self.t, "none.json"), tables=self.t)["hash"]["status"], "absent")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cs.main(["--path", os.path.join(self.t, "none.json"), "--strict"]), 0)

    def test_edited_copy_fails_and_missing_version_warns(self):
        p = write(self.t, [row("a", "x", "y")])
        with open(p, "a") as f:
            f.write(" ")
        self.assertEqual(cs.check_hash(p)[0], "fail")
        os.remove(cs.version_path(p))
        p2 = write(self.t, [row("a", "x", "y")], version=False)
        self.assertEqual(cs.check_hash(p2)[0], "warn")

    def test_companion_sha_is_checked(self):
        p = write(self.t, [row("a", "x", "y")])
        open(os.path.join(self.t, "create-flow-lines.proposed.json"), "w").write("{}")
        vp = cs.version_path(p)
        v = json.load(open(vp)); v["companions"] = {"tables/create-flow-lines.proposed.json": {"sha256": "0" * 64}}
        json.dump(v, open(vp, "w"))
        st, msg = cs.check_hash(p)
        self.assertEqual(st, "fail")
        v["companions"]["tables/create-flow-lines.proposed.json"]["sha256"] = hashlib.sha256(b"{}").hexdigest()
        json.dump(v, open(vp, "w"))
        self.assertEqual(cs.check_hash(p)[0], "ok")


class Switch(unittest.TestCase):
    def test_enable_disable_keeps_other_flags(self):
        with tempfile.TemporaryDirectory() as camp:
            os.makedirs(os.path.join(camp, "sessions"))
            sj = os.path.join(camp, "sessions", "session.json")
            json.dump({"create": {"background_reskin": True, "species_class_reskin": True}, "x": 1}, open(sj, "w"))
            cs.set_flag(True, campaign=camp)
            d = json.load(open(sj))
            self.assertEqual(d["create"], {"background_reskin": True, "species_class_reskin": True, "screens_reskin": True})
            self.assertEqual(d["x"], 1)
            cs.set_flag(False, campaign=camp)
            self.assertIs(json.load(open(sj))["create"]["screens_reskin"], False)
            self.assertEqual(json.load(open(sj))["create"]["background_reskin"], True)
            self.assertFalse(os.path.exists(sj + ".tmp"))


class RealFile(unittest.TestCase):
    """Lore's actual file (skipped if it is not installed): clean under --strict; the documented placeholder renames only."""
    def setUp(self):
        self.p = os.path.join(LIVE_TABLES, "create-screens-reskins.json")
        if not os.path.exists(self.p):
            self.skipTest("create-screens-reskins.json not installed")

    def test_real_file_is_clean(self):
        rep = cs.check(path=self.p)
        self.assertEqual(rep["hash"]["status"], "ok", rep["hash"])
        self.assertEqual(rep["errors"], [])
        self.assertEqual(rep["warnings"], [])
        self.assertGreaterEqual(rep["entry_count"], 192)

    def test_source_map_leaves_only_the_composed_stat_rows(self):
        if not os.path.isdir(os.path.join(cs.BRIDGE, "src", "create")):
            self.skipTest("bridge source not present")
        sm = cs.source_map(self.p)
        self.assertEqual(set(sm["unwired"]) - {"stat-ac", "stat-hp", "stat-initiative", "stat-passive-perception", "stat-proficiency-bonus"}, set())


class MoneyWords(Fixture):
    def test_report_lists_money_words_and_skips_prices(self):
        os.makedirs(self.t, exist_ok=True)
        json.dump({"entries": [{"id": "a", "flavor": "no petty cash", "base_price": "5 gp", "combined_label": "Fine (Fine)"}, {"id": "b", "old": "{n} GP"}]}, open(os.path.join(self.t, "item-reskins.json"), "w"))
        json.dump({"lines": {"S10": ["take the cash"], "S1": ["hello"]}}, open(os.path.join(self.t, "create-flow-lines.json"), "w"))
        rows = cs.money_words(self.t)
        self.assertEqual(sorted((r[1], r[2]) for r in rows), [("S10", "line"), ("a", "flavor"), ("b", "old")])


if __name__ == "__main__":
    unittest.main()
