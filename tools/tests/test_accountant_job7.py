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

    # No exemption (job 7, second follow-up): every floor_lost / body_loot row must carry item_count + items_digest, whatever its seq or timestamp.
    def test_no_cutoff_constants_or_exemption_remain(self):
        for name in ("FINGERPRINT_CUTOFF_SEQ", "FINGERPRINT_CUTOFF_TS", "_fingerprint_required"):
            self.assertFalse(hasattr(state, name), name)

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
        self.assertEqual(out.count("has no items fingerprint (required on every body_loot row)"), 4, out)
        self.assertIn("does not record item_count (required on every body_loot row)", out)

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
        self.assertIn("has no items fingerprint (required on every floor_lost row)", self.verify(expect=1))

    def test_t24_strip_first_pair_then_claim_99_gem_fails(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=1", "--reason", "first")
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=1", "--reason", "second")
        def t24(rows):
            for r in self.body_rows(rows, 0):
                r.pop("item_count"); r.pop("items_digest"); r["items"] = [{"name": "Gem", "qty": 99, "notes": ""}]
        self.edit_rows(t24)
        out = self.verify(expect=1)
        self.assertEqual(out.count("has no items fingerprint (required on every body_loot row)"), 2, out)

    OLD_TS = "2026-10-04T15:50:00-05:00"

    def strip_floor_lost(self, rows):
        d = rows[-1]["destroyed"]
        d.pop("items_digest")
        next(i for i in d["items"] if i["name"] == "Rope")["qty"] = 99
        d["item_count"] = sum(i["qty"] for i in d["items"])

    def test_c6_renumber_earlier_rows_and_give_forged_floor_lost_an_old_seq_fails(self):
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        def c6(rows):
            self.strip_floor_lost(rows)
            for r in rows[:-1]:
                r["seq"] = 9
            rows[-1].update(seq=10, ts=self.OLD_TS)
        self.edit_rows(c6)
        self.assertIn("floor_lost entry #10 has no items fingerprint (required on every floor_lost row)", self.verify(expect=1))

    def test_c7_body_loot_pair_renumbered_with_old_seq_and_ts_fails(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=2", "--reason", "x")
        def c7(rows):
            pair = self.body_rows(rows, 0)
            for r in rows:
                if r not in pair:
                    r["seq"] = 8
            for r, sq in zip(pair, (9, 10)):
                r.pop("item_count"); r.pop("items_digest"); r["items"][0]["qty"] = 99; r.update(seq=sq, ts=self.OLD_TS)
        self.edit_rows(c7)
        out = self.verify(expect=1)
        self.assertEqual(out.count("has no items fingerprint (required on every body_loot row)"), 2, out)
        self.assertEqual(out.count("does not record item_count (required on every body_loot row)"), 2, out)

    def test_c8_all_earlier_rows_seq_0_and_forged_row_seq_1_fails(self):
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        def c8(rows):
            self.strip_floor_lost(rows)
            for r in rows[:-1]:
                r["seq"] = 0
            rows[-1].update(seq=1, ts=self.OLD_TS)
        self.edit_rows(c8)
        self.assertIn("floor_lost entry #1 has no items fingerprint", self.verify(expect=1))

    def test_c9_a_row_that_looks_old_in_every_way_still_needs_its_fingerprint(self):
        # the strongest forgery: a unique low seq, an old ts, in file order, nothing else touched -> still refused, because there is no exemption at all
        base = {"ts": self.OLD_TS, "event": "body_loot", "transfer_id": "legacy-1", "coins": 0, "items": [{"name": "Gem", "qty": 99}], "reason": "old", "source": "loot_body", "command": "loot-body"}
        rows = [dict(base, seq=1, crawler="Bone", delta=0, balance=0, role="from"), dict(base, seq=2, crawler="Horn", delta=0, balance=0, role="to")]
        probs = state._verify_floor_events(rows, {})
        self.assertEqual(sum("has no items fingerprint (required on every body_loot row)" in p for p in probs), 2, probs)

    def test_floor_lost_fingerprint_is_always_required(self):
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        self.assertIn("ledger OK", self.verify())
        self.edit_rows(lambda rows: rows[-1]["destroyed"].pop("items_digest"))
        self.assertIn("has no items fingerprint", self.verify(expect=1))

    # ---------------------------------------------------------------- job 7d: tamper6 f1-f6, seq gaps, orphan halves, credits -0
    def two_loots(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "20", "--reason", "coins")       # pair 0 (coin pair)
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=2", "--reason", "items")    # pair 1 (item-only, delta 0)
        self.assertIn("ledger OK", self.verify())

    def test_f1_floor_lost_row_with_event_removed_is_still_checked(self):
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        def f1(rows):
            x = rows[-1]; x.pop("event"); x["source"] = "adjust"; x["destroyed"]["items"][0]["qty"] = 99; x["destroyed"].pop("items_digest")
        self.edit_rows(f1)
        out = self.verify(expect=1)
        self.assertIn("has floor_lost fields but its event is None (must be exactly 'floor_lost')", out)
        self.assertIn("has no items fingerprint (required on every floor_lost row)", out)

    def test_f2_body_loot_pair_with_event_removed_fails(self):
        self.two_loots()
        def f2(rows):
            for x in self.body_rows(rows, 1):
                x.pop("event"); x.pop("item_count"); x.pop("items_digest"); x["items"][0]["qty"] = 99
        self.edit_rows(f2)
        out = self.verify(expect=1)
        self.assertEqual(out.count("has body_loot fields but its event is None (must be exactly 'body_loot')"), 2, out)
        self.assertIn("has no items fingerprint (required on every body_loot row)", out)

    def test_f3_deleting_an_item_only_pair_leaves_a_seq_gap(self):
        self.two_loots()
        self.run_cmd("credits", "Pip", "+1", "--reason", "a later entry (as in tamper6, where rows follow the deleted pair)")
        gone = []
        def f3(rows):
            pair = self.body_rows(rows, 1); gone.extend(sorted(r["seq"] for r in pair))
            rows[:] = [r for r in rows if r not in pair]
        self.edit_rows(f3)
        self.assertIn(f"ledger seq has a gap: entry #{gone[0]}, #{gone[1]} is missing", self.verify(expect=1))

    def test_seq_duplicates_and_bad_seq_fail(self):
        self.two_loots()
        self.edit_rows(lambda rows: rows[-1].__setitem__("seq", rows[-2]["seq"]))
        out = self.verify(expect=1)
        self.assertIn("appears 2 times in the ledger", out)

    def test_f4_orphaned_item_pair_with_ghost_counterparty_fails(self):
        self.two_loots()
        def f4(rows):
            for x, t in zip(self.body_rows(rows, 1), ("body-x1", "body-x2")):
                x["transfer_id"] = t; x["counterparty"] = "Ghost"; x.pop("item_count"); x.pop("items_digest"); x["items"][0]["qty"] = 99
        self.edit_rows(f4)
        out = self.verify(expect=1)
        self.assertEqual(out.count("is missing (orphan"), 2, out)
        self.assertEqual(out.count("counterparty 'Ghost'"), 2, out)
        self.assertEqual(out.count("has no items fingerprint (required on every body_loot row)"), 2, out)

    def test_f5_orphaned_coin_pair_with_wrong_coins_fails(self):
        self.two_loots()
        def f5(rows):
            for x, t in zip(self.body_rows(rows, 0), ("body-y1", "body-y2")):
                x["transfer_id"] = t; x["counterparty"] = "Ghost"; x["coins"] = 5; x["items"] = [{"name": "Gem", "qty": 50, "notes": ""}]; x.pop("item_count"); x.pop("items_digest")
        self.edit_rows(f5)
        out = self.verify(expect=1)
        self.assertEqual(out.count("does not match the 5 coins looted"), 2, out)
        self.assertEqual(out.count("is missing (orphan"), 2, out)

    def test_f6_recapitalised_event_fails(self):
        self.two_loots()
        def f6(rows):
            for x in self.body_rows(rows, 1):
                x["event"] = "Body_Loot"; x.pop("item_count"); x.pop("items_digest"); x["items"][0]["qty"] = 99
        self.edit_rows(f6)
        self.assertEqual(self.verify(expect=1).count("its event is 'Body_Loot' (must be exactly 'body_loot')"), 2)

    def test_unknown_event_and_wrong_counterparty_in_a_pair_fail(self):
        self.two_loots()
        self.edit_rows(lambda rows: rows[0].__setitem__("event", "bonus"))
        self.assertIn("has an unknown event 'bonus'", self.verify(expect=1))
        self.edit_rows(lambda rows: rows[0].pop("event"))
        self.edit_rows(lambda rows: self.body_rows(rows, 0)[0].__setitem__("counterparty", "Pip"))
        self.assertIn("counterparty fields do not name the other row's Crawler", self.verify(expect=1))

    def test_partner_half_in_the_deleted_archive_still_verifies(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "20", "--item", "Rope=1", "--reason", "x")
        self.run_cmd("crawler", "delete", "Bone", "--reason", "gone", "--confirm", "Bone")
        self.assertIn("ledger OK", self.verify())

    def test_credits_zero_amount_is_a_refused_no_op(self):
        for amt in ("-0", "+0", "0"):
            _, err = self.run_cmd("credits", "Horn", amt, "--reason", "x", expect=1)
            self.assertIn(f"amount {amt!r} changes nothing (a no-op is not recorded)", err)
        self.run_cmd("credits", "Horn", "=0", "--reason", "set to zero is allowed")
        self.assertEqual(self.crawler("Horn")["credits"], 0)

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
        self.assertEqual(err, "ERROR: --credit-sources applies only to the ALL-IN view; add --include-credits (e.g. `loot totals --include-credits --credit-sources ...`)")
        _, err = self.run_cmd("loot", "totals", "--assume-floor", "1", expect=1)
        self.assertIn("--assume-floor applies only to the ALL-IN view; add --include-credits", err)
        _, err = self.run_cmd("loot", "totals", "--credit-sources", "encounter", "--assume-floor", "1", expect=1)
        self.assertIn("--credit-sources and --assume-floor apply only to the ALL-IN view", err)
        for bad in ("0", "19", " 3", "03"):
            _, err = self.run_cmd("loot", "totals", "--include-credits", "--assume-floor", bad, expect=1)
            self.assertIn(f"--assume-floor must be a whole number from 1 to 18 (got {bad!r})", err)

    def test_transfer_says_transferred_between_crawlers_not_sold(self):
        self.run_cmd("set", "crawlers.horn.inventory.-", '{"name": "Grudge Ring", "qty": 1, "story_box_id": "SB9", "story_value": 5, "card_id": "c9"}')
        self.run_cmd("credits", "Pip", "+300", "--reason", "seed")
        dry, _ = self.run_cmd("transfer", "Horn", "Pip", "Grudge Ring", "--price", "200", "--reason", "traded", "--dry-run")
        out, _ = self.run_cmd("transfer", "Horn", "Pip", "Grudge Ring", "--price", "200", "--reason", "traded")
        for text in (dry, out):
            self.assertNotIn("sold between", text.lower())
            self.assertIn("FLAG: Story Box item transferred between Crawlers for 200 credits (a transfer, not a sale: NOT counted as income)", text)

    def test_leading_zeros_and_loose_forms_refused_on_every_integer_option(self):
        self.run_cmd("set", "crawlers.horn.inventory.-", '{"name": "Spoon", "qty": 3}')
        self.run_cmd("credits", "Pip", "+300", "--reason", "seed")
        bad_cmds = [("transfer", "Horn", "Pip", "Spoon", "--price", "05", "--reason", "x"), ("transfer", "Horn", "Pip", "Spoon", "--qty", "01", "--reason", "x"),
                    ("transfer", "Horn", "Pip", "Spoon", "--price", "+5", "--reason", "x"), ("transfer", "Horn", "Pip", "Spoon", "--price", " 5", "--reason", "x"),
                    ("transfer", "Horn", "Pip", "Spoon", "--price", "\uff15", "--reason", "x"), ("transfer", "Horn", "Pip", "Spoon", "--price", "1_0", "--reason", "x"),
                    ("pet", "shop", "Horn", "Treat", "--qty", "01", "--reason", "x"), ("loot", "totals", "--floor", "01"), ("loot", "totals", "--floor", "-0")]
        for cmd in bad_cmds:
            _, err = self.run_cmd(*cmd, expect=2)
            self.assertIn("must be a whole number written with the digits 0-9 only (no spaces, '+' signs, decimals or leading zeros; a lone 0 is fine)", err, cmd)
        for amt in ("+05", "-05", "=05", "05", "+ 5", " +5", "+5 ", "+\u0665"):
            _, err = self.run_cmd("credits", "Horn", amt, "--reason", "x", expect=1)
            self.assertIn("amount must look like +500, -200 or =1000 (digits 0-9 only, no spaces or leading zeros", err, amt)
        self.assertEqual(self.crawler("Horn")["credits"], 75)
        self.run_cmd("credits", "Horn", "+5", "--reason", "ok"); self.run_cmd("credits", "Horn", "-5", "--reason", "ok")
        self.run_cmd("transfer", "Horn", "Pip", "Spoon", "--price", "0", "--reason", "a lone 0 is fine")
        self.run_cmd("loot", "totals", "--floor", "1")
        self.assertEqual(self.crawler("Horn")["credits"], 75)

    def test_gm_quirks_and_repair_log_integer_options_use_the_same_rule(self):
        import argparse
        import gm_quirks
        import repair_log
        self.assertEqual((gm_quirks._cli_signed("+2"), gm_quirks._cli_signed("-3"), gm_quirks._cli_signed("0"), gm_quirks._cli_int("5"), repair_log._cli_int("1")), (2, -3, 0, 5, 1))
        for fn, bad in ((gm_quirks._cli_signed, "+02"), (gm_quirks._cli_signed, " 2"), (gm_quirks._cli_int, "01"), (gm_quirks._cli_int, "+1"), (repair_log._cli_int, "01"), (repair_log._cli_int, "\uff11")):
            with self.assertRaises(argparse.ArgumentTypeError, msg=(fn, bad)):
                fn(bad)
        self.assertNotIn("type=int", open(os.path.join(os.path.dirname(state.__file__), "state.py"), encoding="utf-8").read().replace("replaces type=int", ""))
        for mod in (gm_quirks, repair_log):
            self.assertNotIn("type=int", open(mod.__file__, encoding="utf-8").read(), mod.__name__)

    def test_priced_transfer_ledger_reason_and_verify_flag_say_transfer(self):
        self.run_cmd("set", "crawlers.horn.inventory.-", '{"name": "Grudge Ring", "qty": 1, "story_box_id": "SB9", "story_value": 5, "card_id": "c9"}')
        self.run_cmd("credits", "Pip", "+300", "--reason", "seed")
        self.run_cmd("transfer", "Horn", "Pip", "Grudge Ring", "--price", "200", "--reason", "traded")
        rows = [r for r in self.rows() if r.get("source") == "transfer"]
        self.assertEqual({r["reason"] for r in rows}, {"Transferred 1x Grudge Ring Horn -> Pip for 200 credits: traded"})
        out = self.verify()
        self.assertNotIn("credits from a Story Box item", out)
        self.assertIn("FLAG: #", out)
        self.assertIn("Horn +200 credits: received for a Story Box item transferred between Crawlers (Grudge Ring; a transfer, not income; story value 5", out)
        self.assertIn("Pip -200 credits: paid for a Story Box item transferred between Crawlers (Grudge Ring; a transfer, not income;", out)
        # an old row whose reason still says "Sold ..." reads the same way: the logic keys on source / the story-box event, never on the word "Sold"
        self.edit_rows(lambda rr: [r.__setitem__("reason", r["reason"].replace("Transferred", "Sold").replace(" for 200 credits", "")) for r in rr if r.get("source") == "transfer"])
        self.assertIn("received for a Story Box item transferred between Crawlers", self.verify())
        tot, _ = self.run_cmd("loot", "totals", "--include-credits")
        self.assertIn("NOT counted as income (a transfer is not a sale)", tot)
        self.assertNotIn("sale proceeds 200", tot)

    def test_ledger_extra_does_not_leak_into_the_next_in_process_command(self):
        self.run_cmd("set", "crawlers.horn.inventory.-", '{"name": "Grudge Ring", "qty": 1, "story_box_id": "SB9", "story_value": 5, "card_id": "c9"}')
        self.run_cmd("credits", "Pip", "+300", "--reason", "seed")
        self.run_cmd("transfer", "Horn", "Pip", "Grudge Ring", "--price", "200", "--reason", "traded")
        self.run_cmd("credits", "Pip", "+1", "--reason", "next command")
        self.assertNotIn("provenance", self.rows()[-1])

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
