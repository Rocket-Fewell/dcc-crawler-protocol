"""Accountant round 3 (all on temp DCC_CAMPAIGN_DIR copies): body_loot item fingerprint, transfers are never income, --credit-sources validation,
strict ASCII-digit --coins, and the 'FNone' label. Nothing here can touch the live state.json or credit-ledger.jsonl."""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import ledgers  # noqa: E402
import loot  # noqa: E402
import state  # noqa: E402
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

    # Fixed cutoff (job 7 follow-up): the "old row" exemption comes from constants in state.py, never from the ledger, so stripping fingerprints cannot move it.
    def test_cutoff_is_a_fixed_constant(self):
        self.assertEqual((state.FINGERPRINT_CUTOFF_SEQ, state.FINGERPRINT_CUTOFF_TS), (11, "2026-10-04T15:58:00-05:00"))

    def test_t20_strip_every_body_loot_fingerprint_then_qty_99_fails(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "5", "--reason", "first")
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=2", "--reason", "second")
        def t20(rows):
            for r in rows:
                if r.get("event") == "body_loot":
                    r.pop("item_count", None); r.pop("items_digest", None)
            for r in self.body_rows(rows, 1):
                r["items"][0]["qty"] = 99
        self.edit_rows(t20)
        out = self.verify(expect=1)
        self.assertEqual(out.count("has no items fingerprint (required for entries from #11 or stamped after 2026-10-04T15:58:00-05:00)"), 4, out)
        self.assertIn("does not record item_count (required for entries from #11", out)

    def test_t21_strip_floor_lost_digest_then_edit_rope_fails(self):
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        def t21(rows):
            d = rows[-1]["destroyed"]
            d.pop("items_digest")
            rope = next(i for i in d["items"] if i["name"] == "Rope")
            d["item_count"] += 99 - rope["qty"]
            rope["qty"] = 99
        self.edit_rows(t21)
        self.assertIn("floor_lost entry #", self.verify(expect=1))
        self.assertIn("has no items fingerprint (required for entries from #11", self.verify(expect=1))

    def test_t24_strip_first_pair_then_claim_99_gem_fails(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=1", "--reason", "first")
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=1", "--reason", "second")
        def t24(rows):
            for r in self.body_rows(rows, 0):
                r.pop("item_count"); r.pop("items_digest"); r["items"] = [{"name": "Gem", "qty": 99, "notes": ""}]
        self.edit_rows(t24)
        out = self.verify(expect=1)
        self.assertEqual(out.count("has no items fingerprint (required for entries from #11"), 2, out)

    def test_exemption_needs_both_old_seq_and_old_timestamp(self):
        old = {"seq": 3, "ts": "2026-10-04T15:00:00-05:00"}
        self.assertFalse(state._fingerprint_required(old))
        self.assertFalse(state._fingerprint_required({"seq": 10, "ts": "2026-10-04T15:58:00-05:00"}))
        for e in ({"seq": 11, "ts": old["ts"]}, {"seq": 3, "ts": "2026-10-04T15:58:01-05:00"}, {"seq": 3, "ts": "2026-10-04T15:00:00"},
                  {"seq": 3}, {"seq": 3, "ts": "garbage"}, {"ts": old["ts"]}, {"seq": "3", "ts": old["ts"]}):
            self.assertTrue(state._fingerprint_required(e), e)

    def legacy_pair(self, seq_from, seq_to, items):
        base = {"ts": "2026-10-04T15:10:00-05:00", "event": "body_loot", "transfer_id": "legacy-1", "coins": 0, "items": items, "reason": "old", "source": "loot_body", "command": "loot-body"}
        return [dict(base, seq=seq_from, crawler="Bone", delta=0, balance=0, role="from"), dict(base, seq=seq_to, crawler="Horn", delta=0, balance=0, role="to")]

    def test_a_genuine_pre_cutoff_row_without_fingerprint_still_verifies(self):
        rows = self.legacy_pair(4, 5, [{"name": "Rope", "qty": 1}])
        self.assertEqual(state._verify_floor_events(rows, {}), [])

    def test_a_row_that_fakes_an_old_seq_is_caught(self):
        rows = [{"seq": 4, "ts": "2026-10-04T15:00:00-05:00", "crawler": "Bone", "delta": 0, "balance": 0}] + self.legacy_pair(4, 5, [{"name": "Gem", "qty": 99}])
        self.assertTrue(any("seq is reused or out of order" in p for p in state._verify_floor_events(rows, {})))
        rows = [{"seq": 12, "ts": "2026-10-04T23:00:00-05:00", "crawler": "Bone", "delta": 0, "balance": 0}] + self.legacy_pair(6, 7, [{"name": "Gem", "qty": 99}])
        self.assertTrue(any("seq is reused or out of order" in p for p in state._verify_floor_events(rows, {})))

    def test_floor_lost_fingerprint_is_required_after_the_cutoff(self):
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        self.assertIn("ledger OK", self.verify())
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

    def test_credit_sources_or_assume_floor_without_include_credits_is_an_error(self):
        _, err = self.run_cmd("loot", "totals", "--credit-sources", "encounter", expect=1)
        self.assertEqual(err, "ERROR: --credit-sources only apply to the ALL-IN view; add --include-credits (e.g. `loot totals --include-credits --credit-sources ...`)")
        _, err = self.run_cmd("loot", "totals", "--assume-floor", "1", expect=1)
        self.assertIn("--assume-floor only apply to the ALL-IN view; add --include-credits", err)
        _, err = self.run_cmd("loot", "totals", "--credit-sources", "encounter", "--assume-floor", "1", expect=1)
        self.assertIn("--credit-sources and --assume-floor only apply", err)

    def test_transfer_says_transferred_between_crawlers_not_sold(self):
        self.run_cmd("set", "crawlers.horn.inventory.-", '{"name": "Grudge Ring", "qty": 1, "story_box_id": "SB9", "story_value": 5, "card_id": "c9"}')
        self.run_cmd("credits", "Pip", "+300", "--reason", "seed")
        dry, _ = self.run_cmd("transfer", "Horn", "Pip", "Grudge Ring", "--price", "200", "--reason", "traded", "--dry-run")
        out, _ = self.run_cmd("transfer", "Horn", "Pip", "Grudge Ring", "--price", "200", "--reason", "traded")
        for text in (dry, out):
            self.assertNotIn("sold between", text.lower())
            self.assertIn("FLAG: Story Box item transferred between Crawlers for 200 credits (a transfer, not a sale: NOT counted as income)", text)

    # ---------------------------------------------------------------- (4) strict digits, FNone
    def test_coins_with_whitespace_or_non_ascii_digits_are_refused(self):
        for bad in (" 5", "5 ", "5\n", "\t5", "\u0665", "\uff15", "5\u0665", "+5", "-5", "5.0", "1_0", " all", "all ", "al l", "", "05", "00", "007"):
            _, err = self.run_cmd("loot-body", "Bone", "Horn", "--coins", bad, "--reason", "x", expect=1)
            self.assertIn("--coins must be a whole number of credits written with the digits 0-9 only", err, repr(bad))
        self.assertEqual((self.crawler("Bone")["credits"], self.crawler("Horn")["credits"]), (127, 75))
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "5", "--reason", "x")
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "0", "--item", "Rope=1", "--reason", "a lone 0 is fine")
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "ALL", "--reason", "x")
        self.assertEqual(self.crawler("Bone")["credits"], 0)

    def test_item_quantity_and_floor_whitespace_are_refused_too(self):
        _, err = self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope= 1", "--reason", "x", expect=1)
        self.assertIn("--item", err)
        _, err = self.run_cmd("loot-body", "Bone", "Horn", "--coins", "1", "--floor", " 3", "--reason", "x", expect=1)
        self.assertIn("--floor must be a whole number from 1 to 18 (got ' 3')", err)          # the raw value, space included
        _, err = self.run_cmd("loot-body", "Bone", "Horn", "--coins", "1", "--floor", "03", "--reason", "x", expect=1)
        self.assertIn("(got '03')", err)
        _, err = self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=02", "--reason", "x", expect=1)
        self.assertIn("no leading zeros", err)

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
