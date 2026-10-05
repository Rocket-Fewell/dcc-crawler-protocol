"""tables/background-reskins.json (S7 display names): ids come from chargen-5e.json, strict coverage, hash, structure, switch. Placeholder names live ONLY in fixtures here."""
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
import background_reskins as br  # noqa: E402

CAMPAIGN = os.path.dirname(TOOLS)
LIVE_TABLES = os.path.join(CAMPAIGN, "tables")


def full_fixture(tables=LIVE_TABLES):
    ents = []
    for r in br.required_ids(tables):
        disp = "PLACEHOLDER " + r["id"]
        e = {"id": r["id"], "kind": r["kind"], "parent_id": r["parent_id"], "srd_name": r["srd_name"], "display_name": disp, "combined_label": f"{disp} ({r['srd_name']})", "chargen_value": r["chargen_value"], "flavor": "PLACEHOLDER flavor line."}
        if r["srd_name"].count("(") and r["kind"] == "choice":   # Lore's rule: label_name carries a 5e name that has its own parentheses
            e["label_name"] = r["srd_name"].replace(" (", ", ").replace(")", "")
            e["combined_label"] = f"{disp} ({e['label_name']})"
        ents.append(e)
    return {"schema": "background-reskins/0.1.0", "meta": {"version": "9.9.9", "title": "TEST FIXTURE, PLACEHOLDER NAMES ONLY"}, "entries": ents}


class Sandbox(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.t = self.tmp.name
        shutil.copy(os.path.join(LIVE_TABLES, "chargen-5e.json"), self.t)
        self.path = os.path.join(self.t, "background-reskins.json")
        self._env = os.environ.pop("BACKGROUND_RESKINS_PATH", None)

    def tearDown(self):
        if self._env is not None:
            os.environ["BACKGROUND_RESKINS_PATH"] = self._env
        self.tmp.cleanup()

    def put(self, data, version=True):
        raw = json.dumps(data, indent=1).encode()
        open(self.path, "wb").write(raw)
        if version:
            json.dump({"version": "9.9.9", "sha256": hashlib.sha256(raw).hexdigest(), "entry_count": len(data["entries"])}, open(os.path.join(self.t, "background-reskins.version.json"), "w"))

    def run_main(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = br.main(list(args))
        return rc, buf.getvalue()


class Ids(unittest.TestCase):
    def test_ids_come_from_chargen(self):
        req = br.required_ids()
        kinds = {k: [r for r in req if r["kind"] == k] for k in br.KINDS}
        cg = json.load(open(os.path.join(LIVE_TABLES, "chargen-5e.json")))
        self.assertEqual(len(kinds["background"]), 16)
        ch = kinds["choice"]
        self.assertEqual(len([r for r in ch if r["parent_id"] == "background-asi"]), 2)
        self.assertEqual(len([r for r in ch if r["parent_id"] == "origin-feat"]), len(cg["origin_feats"]))
        self.assertEqual({r["id"] for r in ch if r["parent_id"] == "background-kit"}, {"package-a", "package-b"})   # shared by all backgrounds
        self.assertEqual(len(req), 32)
        ids = {r["id"] for r in req}
        self.assertIn("acolyte", ids)
        self.assertIn("feat-magic-initiate-cleric", ids)
        self.assertIn("asi-2-1", ids)
        self.assertEqual(len(ids), len(req), "ids are unique")

    def test_live_tables_dir_has_no_file_until_delivered(self):
        # not live until Lore delivers and Caleb approves: the check says ABSENT and exits 0, even with --strict
        if os.path.exists(os.path.join(LIVE_TABLES, "background-reskins.json")):
            self.skipTest("the real file has been dropped in; coverage is tested in Real")
        rep = br.check()
        self.assertEqual(rep["hash"]["status"], "absent")
        self.assertEqual(rep["errors"], [])


class Check(Sandbox):
    def test_full_fixture_is_strict_clean(self):
        self.put(full_fixture())
        rep = br.check(self.path, tables=self.t)
        self.assertEqual(rep["errors"], [])
        self.assertEqual(rep["missing"], [])
        self.assertEqual(rep["covered"], rep["required"])
        rc, out = self.run_main("--path", self.path, "--strict")
        self.assertEqual(rc, 0, out)
        self.assertIn(f"coverage: {rep['required']}/{rep['required']}", out)

    def test_strict_fails_on_any_missing_id(self):
        f = full_fixture()
        f["entries"] = [e for e in f["entries"] if e["id"] not in ("sage", "asi-1-1-1", "feat-tough", "package-b")]
        self.put(f)
        # report only: exit 0; strict: exit 1 listing every missing id
        self.assertEqual(self.run_main("--path", self.path)[0], 0)
        rc, out = self.run_main("--path", self.path, "--strict")
        self.assertEqual(rc, 1)
        for m in ("sage", "asi-1-1-1", "feat-tough", "package-b"):
            self.assertIn(f"MISSING: {m}", out)

    def test_structure_errors(self):
        f = full_fixture()
        e = f["entries"]
        e[0]["flavor"] = ""
        e[1]["display_name"] = "Has (parens)"
        e[1]["combined_label"] = "Has (parens) (Artisan)"
        e[2]["kind"] = "nonsense"
        e[3]["gp"] = 99
        e[4]["flavor"] = "the champs of the floor"
        e[5]["chargen_value"] = "Wrong"        # not the exact chargen string
        e.append(dict(e[6]))                   # duplicate id
        self.put(f)
        errs = " | ".join(br.check(self.path, tables=self.t)["errors"])
        for want in ("flavor must be a non-empty string", "must not contain parentheses", "kind must be one of", "does not belong in a display-only table", "never champs", "duplicate id", "not the exact chargen string"):
            self.assertIn(want, errs)
        self.assertEqual(self.run_main("--path", self.path)[0], 1)

    def test_nested_parentheses_are_an_error_and_label_name_is_the_fix(self):
        f = full_fixture()
        mi = next(e for e in f["entries"] if e["id"] == "feat-magic-initiate-cleric")
        self.assertIn("label_name", mi)                       # the fixture follows Lore's rule
        self.put(f)
        self.assertEqual(br.check(self.path, tables=self.t)["errors"], [])
        mi.pop("label_name")
        mi["combined_label"] = "PLACEHOLDER feat-magic-initiate-cleric (Magic Initiate (Cleric))"
        self.put(f)
        self.assertTrue(any("nested parentheses" in e for e in br.check(self.path, tables=self.t)["errors"]))

    def test_hash_mismatch_and_missing_version(self):
        self.put(full_fixture())
        open(self.path, "a").write("\n ")
        rc, out = self.run_main("--path", self.path)
        self.assertEqual(rc, 1)
        self.assertIn("FAIL", out)
        self.put(full_fixture(), version=False)
        os.remove(os.path.join(self.t, "background-reskins.version.json"))
        self.assertEqual(br.check_hash(self.path)[0], "warn")

    def test_absent_is_exit_zero(self):
        rc, out = self.run_main("--path", os.path.join(self.t, "nope.json"), "--strict")
        self.assertEqual(rc, 0)
        self.assertIn("ABSENT", out)


class Switch(unittest.TestCase):
    def test_enable_disable_writes_only_the_flag(self):
        with tempfile.TemporaryDirectory() as c:
            os.makedirs(os.path.join(c, "sessions"))
            sj = os.path.join(c, "sessions", "session.json")
            json.dump({"create": {"allow_roll": True}, "keep": 1}, open(sj, "w"))
            br.set_flag(True, campaign=c)
            d = json.load(open(sj))
            self.assertIs(d["create"]["background_reskin"], True)
            self.assertEqual((d["create"]["allow_roll"], d["keep"]), (True, 1))
            br.set_flag(False, campaign=c)
            self.assertIs(json.load(open(sj))["create"]["background_reskin"], False)


class Real(unittest.TestCase):
    def test_real_file_when_dropped_in(self):
        for p in (os.path.join(LIVE_TABLES, "background-reskins.json"), "/workspace/dcc-lore/tables/background-reskins.json"):
            if os.path.exists(p):
                rep = br.check(p)
                self.assertEqual(rep["errors"], [], p)
                self.assertEqual(rep["missing"], [], p)
                return
        self.skipTest("Lore's background-reskins.json does not exist yet")


if __name__ == "__main__":
    unittest.main()
