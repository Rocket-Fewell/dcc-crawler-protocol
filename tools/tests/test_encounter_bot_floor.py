"""Floor-aware day-page generator. Floor 1 output stays the same; other floors use their own canon table."""
import copy
import hashlib
import importlib.util
import json
import os
import unittest


TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMPAIGN = os.path.dirname(TOOLS)
EB_PATH = os.path.join(TOOLS, "encounter_bot", "encounter_bot.py")
_spec = importlib.util.spec_from_file_location("encounter_bot_floor_under_test", EB_PATH)
eb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eb)


def render_like_main(spec_path):
    """Same assemble-and-render path as encounter_bot.main, without writing day pages."""
    raw = eb.read_text(spec_path)
    spec = json.loads(raw)
    rep = eb.Report()
    meta = spec.get("meta") if isinstance(spec, dict) else None
    data = eb.Data(eb.floor_number(meta.get("floor", 1)) if isinstance(meta, dict) else 1)
    doc = eb.build(spec, data, rep)
    sans_pin = eb.spec_sha256_sans_pin(json.loads(raw))
    eb.check_slot_map_provenance(spec, sans_pin, data.budget, rep)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    doc["meta"]["spec_sha256_sans_pin"] = sans_pin
    doc["meta"]["spec_sha256_sans_pin_method"] = eb.SANS_PIN_METHOD
    doc["validation"] = {"result": "?", "pass": 0, "warn": 0, "fail": 0, "spec_sha256": digest, "checks": []}
    eb.check_md_audience(eb.render_md(doc), doc, rep)
    checks = [{"status": s, "check": c, "detail": d} for s, c, d in rep.items]
    doc["validation"] = {
        "result": "PASS" if rep.passed else "FAIL",
        "pass": rep.count("PASS"), "warn": rep.count("WARN"), "fail": rep.count("FAIL"),
        "spec_sha256": digest, "checks": checks}
    doc["meta"]["spec_sha256_sans_pin"] = sans_pin
    doc["meta"]["spec_sha256_sans_pin_method"] = eb.SANS_PIN_METHOD
    md = eb.render_md(doc)
    if not md.endswith("\n"):
        md += "\n"
    return md, doc, data


def scrub_md(text):
    """Drop lines that move when the budget file or achievements catalog hash changes."""
    kept = []
    for line in text.splitlines(keepends=True):
        if line.startswith("Budget file:") or line.startswith("### Budget at a glance") or line.startswith("*Build note:"):
            continue
        kept.append(line)
    return "".join(kept)


def scrub_doc(doc):
    doc = copy.deepcopy(doc)
    meta = doc.get("meta") or {}
    for key in ("achievements_csv_sha256", "budget_file_version", "budget_file_sha256"):
        meta.pop(key, None)
    doc.pop("validation", None)
    return doc


class FloorAwareGeneratorTests(unittest.TestCase):
    def test_floor_paths(self):
        self.assertEqual(eb.floor_number(None), 1)
        self.assertEqual(eb.floor_number("nope"), 1)
        self.assertEqual(eb.canon_table_display(1), "lore/tables/canon-floor-1.json")
        self.assertEqual(eb.canon_table_display(2), "lore/tables/canon-floor-2.json")
        self.assertTrue(eb.canon_table_path(1).endswith(os.path.join("tables", "canon-floor-1.json")))
        self.assertTrue(eb.canon_table_path(2).endswith(os.path.join("tables", "canon-floor-2.json")))
        self.assertTrue(eb.floor_pages_dir(2).endswith(os.path.join("floors", "f02")))

    def test_loaded_tables_follow_floor(self):
        one = eb.Data(1)
        two = eb.Data(2)
        self.assertEqual(one.canon_display, "lore/tables/canon-floor-1.json")
        self.assertEqual(two.canon_display, "lore/tables/canon-floor-2.json")
        self.assertNotEqual(one.canon_sha256, two.canon_sha256)
        self.assertTrue(one.overview_path.endswith(os.path.join("floors", "f01", "00-overview.md")))
        self.assertTrue(two.overview_path.endswith(os.path.join("floors", "f02", "00-overview.md")))
        self.assertEqual(two.canon.get("floor"), 2)
        with open(eb.canon_table_path(2), "rb") as fh:
            self.assertEqual(two.canon_sha256, hashlib.sha256(fh.read()).hexdigest())

    def test_write_guard_follows_spec_floor(self):
        f01 = os.path.join(eb.ROOT, "floors", "f01", "day-01.md")
        f02 = os.path.join(eb.ROOT, "floors", "f02", "day-01.md")
        self.assertTrue(eb.check_write_allowed(f01, floor=1, days=5).endswith("day-01.md"))
        self.assertTrue(eb.check_write_allowed(f02, floor=2, days=10).endswith("day-01.md"))
        with self.assertRaises(PermissionError):
            eb.check_write_allowed(f02, floor=1, days=5)
        with self.assertRaises(PermissionError):
            eb.check_write_allowed(f01, floor=2, days=10)
        with self.assertRaises(PermissionError):
            eb.check_write_allowed(os.path.join(eb.ROOT, "floors", "f02", "00-overview.md"), floor=2, days=10)

    def test_floor1_output_matches_committed_pages(self):
        for n in range(1, 6):
            spec = os.path.join(CAMPAIGN, "floors", "f01", "day-%02d.spec.json" % n)
            md, doc, _data = render_like_main(spec)
            with open(os.path.join(CAMPAIGN, "floors", "f01", "day-%02d.md" % n), encoding="utf-8") as fh:
                disk_md = fh.read()
            with open(os.path.join(CAMPAIGN, "floors", "f01", "day-%02d.json" % n), encoding="utf-8") as fh:
                disk_doc = json.load(fh)
            self.assertEqual(scrub_md(md), scrub_md(disk_md), "day %d markdown drifted" % n)
            self.assertEqual(scrub_doc(doc), scrub_doc(disk_doc), "day %d json drifted" % n)
            self.assertIn("from `floors/f01/day-%02d.spec.json`" % n, md)
            self.assertIn("*Canon table: `lore/tables/canon-floor-1.json`", md)
            self.assertIn("(Floor 1 seed list, GM discretion)", md)

    def test_floor2_render_uses_its_own_table_and_dir(self):
        spec = os.path.join(CAMPAIGN, "floors", "f02", "day-01.spec.json")
        md, doc, data = render_like_main(spec)
        self.assertEqual(data.floor, 2)
        self.assertEqual(data.canon_display, "lore/tables/canon-floor-2.json")
        self.assertIn("from `floors/f02/day-01.spec.json`", md)
        self.assertIn("*Canon table: `lore/tables/canon-floor-2.json`", md)
        self.assertIn(data.canon_sha256, md)
        self.assertNotIn("lore/tables/canon-floor-1.json`, ledger", md)
        self.assertNotIn("from `floors/f01/day-01.spec.json`", md)
        self.assertIn("(Floor 2 seed list, GM discretion)", md)
        self.assertEqual(doc["meta"]["canon_table_sha256"], data.canon_sha256)
        self.assertEqual(doc["canon_table"]["sha256"], data.canon_sha256)


def build_checks(spec):
    """Run build() on an in-memory spec; return the (status, check, detail) report items."""
    rep = eb.Report()
    data = eb.Data(eb.floor_number(spec.get("meta", {}).get("floor", 1)))
    eb.build(spec, data, rep)
    return rep.items


def load_spec(floor, day):
    with open(os.path.join(CAMPAIGN, "floors", "f%02d" % floor, "day-%02d.spec.json" % day), encoding="utf-8") as fh:
        return json.load(fh)


def with_check(items, name):
    return [(s, c, d) for s, c, d in items if c == name]


class FloorAwareSaferoomTests(unittest.TestCase):
    """Saferoom names come from floors/fNN/00-overview.md, not a hardcoded 'Green Room'."""

    def test_saferooms_resolved_from_each_floor_overview(self):
        one, two = eb.Data(1), eb.Data(2)
        self.assertEqual(one.saferooms, [("z06", "The Break Room"), ("z09", "The Green Room")])
        self.assertEqual(one.saferoom_anchor, ("z09", "The Green Room"))
        self.assertEqual(two.saferooms, [("z24", "Storm Shelter A"), ("z27", "Big Shot Chicken B")])
        self.assertEqual(two.saferoom_anchor, ("z27", "Big Shot Chicken B"))
        self.assertEqual(two.saferoom_source, os.path.join("floors", "f02", "00-overview.md"))

    def test_floor_without_overview_does_not_borrow_floor1_saferooms(self):
        self.assertFalse(os.path.isfile(os.path.join(CAMPAIGN, "floors", "f17", "00-overview.md")))
        d = eb.Data(17)
        self.assertEqual(d.saferooms, [])
        self.assertEqual(d.saferoom_anchor, (None, None))

    def test_parse_overview_row_shapes(self):
        bold = "| **Saferooms** | 2: **The Break Room** (Zone 6) and **The Green Room** (Zone 9) |\n"
        self.assertEqual(eb.parse_floor_saferooms(bold), [("z06", "The Break Room"), ("z09", "The Green Room")])
        plain = ("| Regions | Lobby z20, Cold Cellar A z31, Diner B z32 |\n"
                 "| Saferooms | Cold Cellar A (mailbox); Diner B (staffed). May lie elsewhere (Core Ch1) |\n")
        self.assertEqual(eb.parse_floor_saferooms(plain), [("z31", "Cold Cellar A"), ("z32", "Diner B")])
        table = "| Saferooms | **Back Office** |\n| 4 | **Back Office** | Rest | Saferoom | Yes |\n"
        self.assertEqual(eb.parse_floor_saferooms(table), [("z04", "Back Office")])
        self.assertEqual(eb.parse_floor_saferooms("| Regions | nothing here |\n"), [])

    def test_names_saferoom_matching(self):
        self.assertTrue(eb.names_saferoom("From then on the Z9 Green Room is the only saferoom", "The Green Room"))
        self.assertTrue(eb.names_saferoom("Chicken B: big shot chicken b is the anchor", "Big Shot Chicken B"))
        self.assertFalse(eb.names_saferoom("Storm Shelter A only", "Big Shot Chicken B"))
        self.assertFalse(eb.names_saferoom("anything", None))

    def test_floor1_still_requires_the_green_room(self):
        spec = load_spec(1, 4)
        self.assertEqual([s for s, _, _ in with_check(build_checks(spec), "saferoom rule")], ["PASS"])
        self.assertEqual([s for s, _, _ in with_check(build_checks(spec), "rest options")], ["PASS"])
        bad = copy.deepcopy(spec)
        bad["clock"]["saferoom_rule"]["text"] = bad["clock"]["saferoom_rule"]["text"].replace("Green Room", "Lounge")
        got = with_check(build_checks(bad), "saferoom rule")
        self.assertEqual([s for s, _, _ in got], ["FAIL"])
        self.assertIn("The Green Room", got[0][2])
        bad = copy.deepcopy(spec)
        bad["clock"]["saferoom_rule"]["only_saferoom"] = "z06"
        self.assertEqual([s for s, _, _ in with_check(build_checks(bad), "saferoom rule")], ["FAIL"])

    def test_floor2_uses_its_own_saferoom_names(self):
        for day in range(1, 11):
            items = build_checks(load_spec(2, day))
            sr = with_check(items, "saferoom rule")
            self.assertEqual([s for s, _, _ in sr], ["PASS"], "day %d: %s" % (day, sr))
            self.assertIn("Big Shot Chicken B", sr[0][2])
            self.assertEqual([s for s, _, _ in with_check(items, "rest options")], ["PASS"], "day %d" % day)
        spec = load_spec(2, 1)
        bad = copy.deepcopy(spec)
        bad["clock"]["saferoom_rule"]["only_saferoom"] = "z09"  # Floor 1's Green Room zone is not a Floor 2 saferoom
        self.assertEqual([s for s, _, _ in with_check(build_checks(bad), "saferoom rule")], ["FAIL"])
        bad = copy.deepcopy(spec)
        bad["clock"]["saferoom_rule"]["text"] = "Storm Shelter A is honest until T-1h eject; nothing else is named here."
        self.assertEqual([s for s, _, _ in with_check(build_checks(bad), "saferoom rule")], ["FAIL"])


class ReadAloudLengthIsSoftTests(unittest.TestCase):
    """Caleb 2026-10-05: the four-sentence read-aloud limit is a WARN, never a FAIL."""

    def _long_spec(self, n_sentences):
        spec = copy.deepcopy(load_spec(2, 1))
        r = spec["routes"][0]
        key = next(k for k, v in r["voice_lines"].items() if isinstance(v, dict) and v.get("text"))
        r["voice_lines"][key]["text"] = " ".join("Line %s is short." % w for w in
                                                 ("one", "two", "three", "four", "five", "six", "seven", "eight",
                                                  "nine", "ten", "eleven", "twelve")[:n_sentences])
        return spec, "route %s %s" % (r["id"], key)

    def test_over_guideline_warns(self):
        for n in (5, 12):  # just over the guideline, and over the old hard limit
            spec, where = self._long_spec(n)
            items = build_checks(spec)
            self.assertEqual([x for x in items if x[0] == "FAIL" and x[1].startswith("read-aloud")], [], "n=%d" % n)
            warns = [x for x in items if x[0] == "WARN" and x[1] == "read-aloud length (soft)" and x[2].startswith(where + " (%d sentences)" % n)]
            self.assertEqual(len(warns), 1, "n=%d" % n)

    def test_report_with_only_warns_passes(self):
        rep = eb.Report()
        rep.warn("read-aloud length (soft)", "x (12 sentences)")
        self.assertTrue(rep.passed)


if __name__ == "__main__":
    unittest.main()
