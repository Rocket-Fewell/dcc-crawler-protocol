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


if __name__ == "__main__":
    unittest.main()
