"""Accountant round 3 (all on temp DCC_CAMPAIGN_DIR copies): body_loot item fingerprint, transfers are never income, --credit-sources validation,
strict ASCII-digit --coins, and the 'FNone' label. Nothing here can touch the live state.json or credit-ledger.jsonl."""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import ledgers  # noqa: E402
import loot  # noqa: E402
from test_floor_lost import FloorLostBase  # noqa: E402


class Job7(FloorLostBase):
    def lpath(self):
        return os.path.join(self.sessions, "credit-ledger.jsonl")

    def edit_rows(self, fn):
        lines = open(self.lpath(), encoding="utf-8").read().splitlines()
        rows = [json.loads(l) for l in lines]
        fn(rows)
        open(self.lpath(), "w", encoding="utf-8").write("\n".join(json.dumps(r) for r in rows) + "\n")

    def body_rows(self, rows, n=-1):
        tids = []
        for r in rows:
            if r.get("event") == "body_loot" and r["transfer_id"] not in tids:
                tids.append(r["transfer_id"])
        return [r for r in rows if r.get("transfer_id") == tids[n]] if tids else []

    # ---------------------------------------------------------------- (1) body_loot fingerprint
    def test_new_body_loot_rows_carry_item_count_and_digest_and_verify_clean(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=2", "--item", "Healer's Kit", "--coins", "10", "--reason", "x")
        a, b = [r for r in self.rows() if r.get("event") == "body_loot"]
        for r in (a, b):
            self.assertEqual(r["item_count"], 3)
            self.assertRegex(r["items_digest"], r"^[0-9a-f]{16}$")
        self.assertEqual(a["items_digest"], b["items_digest"])
        self.assertIn("ledger OK", self.verify())

    def test_editing_one_half_2_to_99_fails(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=2", "--reason", "x")
        def tamper(rows):
            next(r for r in rows if r.get("event") == "body_loot" and r["role"] == "to")["items"][0]["qty"] = 99
        self.edit_rows(tamper)
        out = self.verify(expect=1)
        self.assertIn("body_loot", out)
        self.assertTrue("item lists of the two rows differ" in out or "item_count" in out)

    def test_editing_both_halves_alike_fails_on_count_and_fingerprint(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=2", "--reason", "x")
        def both(rows):
            for r in rows:
                if r.get("event") == "body_loot":
                    r["items"][0]["qty"] = 99
        self.edit_rows(both)
        self.assertIn("item_count 2 but the looted items add up to 99", self.verify(expect=1))
        def both_counts(rows):
            for r in rows:
                if r.get("event") == "body_loot":
                    r["item_count"] = 99
        self.edit_rows(both_counts)                      # count now matches the edited items; the fingerprint still does not
        self.assertIn("does not match its recorded fingerprint", self.verify(expect=1))

    def test_emptying_the_items_of_one_or_both_halves_fails(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=2", "--reason", "x")
        self.edit_rows(lambda rows: [r.__setitem__("items", []) for r in rows if r.get("event") == "body_loot"])
        out = self.verify(expect=1)
        self.assertIn("looted items add up to 0", out)

    def test_tampering_with_only_the_fingerprint_or_the_count_fails(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=2", "--reason", "x")
        self.edit_rows(lambda rows: [r.__setitem__("items_digest", "0" * 16) for r in rows if r.get("event") == "body_loot" and r["role"] == "from"])
        self.assertIn("fingerprint", self.verify(expect=1))

    def test_old_rows_without_a_digest_still_verify(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=1", "--reason", "x")
        def legacy(rows):
            for r in rows:
                if r.get("event") == "body_loot":
                    r.pop("item_count"); r.pop("items_digest")
        self.edit_rows(legacy)
        self.assertIn("ledger OK", self.verify())

    def test_a_new_row_that_loses_its_digest_is_flagged_but_older_legacy_rows_are_not(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=1", "--reason", "first")
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "5", "--reason", "second")
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "6", "--reason", "third")
        def strip(rows):
            first, third = self.body_rows(rows, 0), self.body_rows(rows, 2)
            for r in first + third:
                r.pop("item_count"); r.pop("items_digest")
        self.edit_rows(strip)
        out = self.verify(expect=1)
        self.assertEqual(out.count("has no items fingerprint (required for entries after #"), 2, out)   # only the third loot's two rows
        self.assertNotIn("first", out)

    def test_floor_lost_fingerprint_is_required_once_one_exists(self):
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        self.assertIn("ledger OK", self.verify())
        self.run_cmd("add-crawler", "Zed", "--player", "Dee", "--class", "Rogue", "--species", "Human", "--credits", "5", "--reason", "intake")
        self.run_cmd("condition", "add", "Zed", "Dead")
        self.run_cmd("floor-lost", "Zed", "--reason", "r")
        self.edit_rows(lambda rows: rows[-1]["destroyed"].pop("items_digest"))
        self.assertIn("has no items fingerprint", self.verify(expect=1))

    # ---------------------------------------------------------------- (2) transfers are never income
    def story_transfer(self):
        self.run_cmd("set", "crawlers.horn.inventory.-", '{"name": "Grudge Ring", "qty": 1, "story_box_id": "SB9", "story_value": 5, "card_id": "c9"}')
        self.run_cmd("credits", "Pip", "+300", "--reason", "seed")
        self.run_cmd("transfer", "Horn", "Pip", "Grudge Ring", "--price", "200", "--reason", "traded")

    def test_priced_transfer_is_not_sale_proceeds_in_totals_or_all_in(self):
        self.story_transfer()
        ledgers.append("loot", {"crawler": "Horn", "floor": 1, "zone": "z", "card_id": "x", "tier": "Bronze", "kind": "item", "economy_value": 1400, "story_value": 0, "text": "t"})
        out, _ = self.run_cmd("loot", "totals")
        self.assertNotIn("sale proceeds", out)
        self.assertNotIn("is over 1,500", out, "1,400 of boxes + a 200-credit TRANSFER must not tip a Crawler over the line")
        self.assertIn("FLAG: Horn transferred (for 200 credits) to Pip Story Box item Grudge Ring on F1: 200 credits changed hands between Crawlers, NOT counted as income", out)
        out, _ = self.run_cmd("loot", "totals", "--include-credits")
        self.assertIn("Horn F1: boxes 1400 + sale proceeds 0 + earned credits 0 = all-in 1400", out)
        j, _ = self.run_cmd("loot", "totals", "--include-credits", "--json")
        self.assertEqual(json.loads(j)["all_in"]["Horn"]["1"]["sale_proceeds"], 0)

    def test_a_real_sale_still_counts(self):
        self.assertEqual(loot.sale_proceeds([{"event": "sold", "crawler": "A", "floor": 1, "price": 500}, {"event": "transferred", "crawler": "A", "floor": 1, "price": 900, "to": "B"}]), {("A", 1): 500})
        t = {"A": {1: {"economy_value": 1200, "story_value": 0, "draws": 1, "legendary": 0}}}
        out = loot.totals_text(t, [{"event": "sold", "crawler": "A", "floor": 1, "price": 500, "item": "X", "story_value": 1, "reason": "r"}])
        self.assertIn("1200 + 500 Story Box sale proceeds is over 1,500", out)
        out = loot.totals_text(t, [{"event": "transferred", "crawler": "A", "floor": 1, "price": 500, "to": "B", "item": "X", "story_value": 1, "reason": "r"}])
        self.assertNotIn("is over 1,500", out)

    # ---------------------------------------------------------------- (3) --credit-sources
    def test_unknown_credit_sources_are_refused_with_the_valid_names(self):
        for bad in ("loot_body", "transfer", "box", "bogus", "encounter,transfer", "encounter,,r1"):
            _, err = self.run_cmd("loot", "totals", "--include-credits", "--credit-sources", bad, expect=1)
            self.assertIn("--credit-sources: unknown source name(s): ", err, bad)
            self.assertIn("Valid names: achievement, encounter, r1, toast.", err, bad)
        _, err = self.run_cmd("loot", "totals", "--include-credits", "--credit-sources", "loot_body,transfer", expect=1)
        self.assertEqual(err, "ERROR: --credit-sources: unknown source name(s): loot_body, transfer. Valid names: achievement, encounter, r1, toast. (Box pulls, sales, transfers and body loot are never counted as earned credits.)")
        _, err = self.run_cmd("loot", "totals", "--include-credits", "--credit-sources", " , ", expect=1)
        self.assertIn("needs at least one source name", err)

    def test_valid_credit_sources_work_in_any_case_and_order(self):
        self.run_cmd("credits", "Horn", "+40", "--reason", "x", "--source", "encounter", "--floor", "1")
        out, _ = self.run_cmd("loot", "totals", "--include-credits", "--credit-sources", "R1, Encounter,encounter")
        self.assertIn("sources: r1, encounter)", out)
        self.assertIn("earned credits 40", out)

    # ---------------------------------------------------------------- (4) strict digits, FNone
    def test_coins_with_whitespace_or_non_ascii_digits_are_refused(self):
        for bad in (" 5", "5 ", "5\n", "\t5", "\u0665", "\uff15", "5\u0665", "+5", "-5", "5.0", "1_0", " all", "all ", "al l", ""):
            _, err = self.run_cmd("loot-body", "Bone", "Horn", "--coins", bad, "--reason", "x", expect=1)
            self.assertIn("--coins must be a whole number of credits written with the digits 0-9 only", err, repr(bad))
        self.assertEqual((self.crawler("Bone")["credits"], self.crawler("Horn")["credits"]), (127, 75))
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "5", "--reason", "x")
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "ALL", "--reason", "x")
        self.assertEqual(self.crawler("Bone")["credits"], 0)

    def test_item_quantity_and_floor_whitespace_are_refused_too(self):
        _, err = self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope= 1", "--reason", "x", expect=1)
        self.assertIn("--item", err)
        _, err = self.run_cmd("loot-body", "Bone", "Horn", "--coins", "1", "--floor", " 3", "--reason", "x", expect=1)
        self.assertIn("1 to 18", err)

    def test_no_floor_set_wording_replaces_fnone(self):
        t = {"Ann": {None: {"economy_value": 2000, "story_value": 0, "draws": 1, "legendary": 0}}}
        out = loot.totals_text(t, [{"event": "sold", "crawler": "Ann", "floor": None, "price": 10, "item": "X", "story_value": 1, "reason": "r"}])
        self.assertNotIn("FNone", out)
        self.assertIn("- Ann (no floor set): economy 2000", out)
        self.assertIn("FLAG: Ann (no floor set) economy value 2000 + 10 Story Box sale proceeds is over 1,500", out)
        self.assertIn("on (no floor set):", out)
        ai = loot.all_in(t, [], {"Ann": {None: 1}})
        ai_out = loot.all_in_text(ai, ["encounter"])
        self.assertNotIn("FNone", ai_out)
        self.assertIn("FLAG: Ann (no floor set) all-in 2001 is over 1,500 credits for the floor", ai_out)

    def test_floors_1_and_2_default_output_is_unchanged(self):
        t = {"Ann": {1: {"economy_value": 1400, "story_value": 0, "draws": 3, "legendary": 0}, 2: {"economy_value": 1600, "story_value": 0, "draws": 4, "legendary": 0}}}
        sales = [{"event": "sold", "crawler": "Ann", "floor": 1, "price": 200, "item": "Thing", "story_value": 5, "reason": "r"}]
        self.assertEqual(loot.totals_text(t, sales), (
            "crawler / floor: economy value | draws\n- Ann F1: economy 1400 | 3 draw(s)\n- Ann F2: economy 1600 | 4 draw(s)\n"
            "FLAG: Ann F1 economy value 1400 + 200 Story Box sale proceeds is over 1,500 (the award's story value is excluded; sale proceeds count)\n"
            "FLAG: Ann F2 economy value 1600 is over 1,500 (the award's story value is excluded; sale proceeds count)\n"
            "FLAG: Ann sold Story Box item Thing on F1: 200 credits received, story value 5 is provenance only and was NOT credited (r)\n"
            "TOTAL economy 3000 (what the Accountant audits)"))


if __name__ == "__main__":
    unittest.main()
