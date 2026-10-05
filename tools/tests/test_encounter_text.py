"""Tests for tools/encounter_text.py (read-only player/GM text of Floor day pages). Uses the real floors/f01 pages."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import tempfile
import unittest


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMPAIGN = os.path.dirname(TOOLS)
spec = importlib.util.spec_from_file_location("encounter_text", os.path.join(TOOLS, "encounter_text.py"))
et = importlib.util.module_from_spec(spec)
spec.loader.exec_module(et)
DAYS = [d for d in range(1, 6) if os.path.exists(et.page_path(CAMPAIGN, 1, d))]


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = et.main(list(args))
    return code, out.getvalue(), err.getvalue()


def gm_only_strings(doc):
    """Every string on the page that is not the named field of a manifest player block (the GM block fields)."""
    player = {(e["path"], e["field"]) for e in et.entries(doc)}
    found = []

    def walk(o, ptr):
        if isinstance(o, dict):
            for k, v in o.items():
                if (ptr, k) not in player:
                    walk(v, f"{ptr}/{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{ptr}/{i}")
        elif isinstance(o, str) and len(o) >= 40:
            found.append(o)
    walk({k: v for k, v in doc.items() if k != "audience_manifest"}, "")
    return found


@unittest.skipUnless(DAYS, "no floors/f01 day pages")
class EncounterText(unittest.TestCase):
    def test_default_has_no_gm_only_text(self):
        for d in DAYS:
            doc = et.load_page(CAMPAIGN, 1, d)
            # widest player output: every optional / confirm / {hours} block switched on
            allp, _ = et.player_items(doc, lambda e: True, 6, True, True)
            ptexts = {t for _, t in allp}
            gm = [s for s in gm_only_strings(doc) if s.strip() not in ptexts and s.replace("{hours}", "6").strip() not in ptexts]
            self.assertGreater(len(gm), 50)
            for args in ([], ["--include-optional", "--confirm", "--hours", "6"]):
                code, out, _ = run("--day", str(d), *args)
                self.assertEqual(code, 0)
                self.assertTrue(out.strip())
                self.assertNotIn(et.GM_HEADER, out)
                self.assertNotIn("{", out.replace("{hours}", ""))   # no JSON
                leaks = [s[:60] for s in gm if s in out]
                self.assertEqual(leaks, [], f"day {d}: GM-only text in player output")

    def test_gm_header_and_content(self):
        doc = et.load_page(CAMPAIGN, 1, DAYS[0])
        eid = doc["encounters"][0]["id"]
        code, out, _ = run("--day", str(DAYS[0]), "--encounter", eid, "--gm")
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines()[0], et.GM_HEADER)
        self.assertIn("map_in_the_mind", out)
        self.assertIn(doc["encounters"][0]["map_in_the_mind"]["layout"], out)

    def test_list(self):
        doc = et.load_page(CAMPAIGN, 1, DAYS[0])
        code, out, _ = run("--day", str(DAYS[0]), "--list")
        self.assertEqual(code, 0)
        ids = [l.split("\t")[0] for l in out.splitlines()]
        for enc in doc["encounters"]:
            self.assertIn(enc["id"], ids)

    def test_missing_day_and_id(self):
        code, out, err = run("--day", "9")
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("Day", err)
        with tempfile.TemporaryDirectory() as tmp:
            code, _, err = run("--day", "1", "--campaign-dir", tmp)
            self.assertNotEqual(code, 0)
            self.assertIn("missing", err)
        code, out, err = run("--day", str(DAYS[0]), "--encounter", "enc-nope-99")
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("enc-nope-99", err)

    def test_zone_and_hours_flags(self):
        code, out, err = run("--day", str(DAYS[0]), "--hours", "5")   # Day 1 has no {hours} data
        if DAYS[0] == 1:
            self.assertEqual(code, 0)
            self.assertIn("--hours ignored", err)
        code, _, err = run("--day", str(DAYS[0]), "--zone", "z99")
        self.assertNotEqual(code, 0)

    def test_read_only(self):
        paths = [et.page_path(CAMPAIGN, 1, d) for d in DAYS]
        before = [sha(p) for p in paths]
        for d in DAYS:
            run("--day", str(d)); run("--day", str(d), "--gm"); run("--day", str(d), "--list")
        self.assertEqual(before, [sha(p) for p in paths])


if __name__ == "__main__":
    unittest.main()
