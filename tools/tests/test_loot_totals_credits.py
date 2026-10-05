"""Q-003 / budget A12 + Q5: `loot totals --include-credits` (optional all-in view and Floor 2 valve check). Default `loot totals` must not change.
Temp campaign only (DCC_CAMPAIGN_DIR); nothing here touches the live state or ledgers."""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import ledgers  # noqa: E402
import loot  # noqa: E402
from test_state import StateTestCase  # noqa: E402


class TotalsCreditsCase(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Ann", "--player", "P", "--class", "Fighter", "--species", "Human")
        self.run_cmd("add-crawler", "Bo", "--player", "Q", "--class", "Wizard", "--species", "Human")

    def box(self, who, floor, value):
        ledgers.append("loot", {"crawler": who, "floor": floor, "zone": "z06", "card_id": "x", "tier": "Bronze", "kind": "item", "economy_value": value, "story_value": 0, "text": "t"})

    def earn(self, who, amount, source, floor=None):
        extra = ("--floor", str(floor)) if floor is not None else ()
        self.run_cmd("credits", who, f"+{amount}", "--reason", f"{source} credits", "--source", source, *extra)

    def test_default_output_is_unchanged_and_has_no_all_in_section(self):
        self.box("Ann", 1, 25)
        self.earn("Ann", 40, "encounter", 1)
        base, _ = self.run_cmd("loot", "totals")
        self.assertNotIn("ALL-IN", base)
        self.assertEqual(base, loot.totals_text(loot.totals(ledgers.read("loot"))))
        j, _ = self.run_cmd("loot", "totals", "--json")
        self.assertNotIn("all_in", json.loads(j))

    def test_include_credits_adds_earned_credits_to_boxes(self):
        self.box("Ann", 1, 25)
        self.earn("Ann", 40, "encounter", 1)
        self.earn("Ann", 25, "achievement", 1)          # an R1 toast
        out, _ = self.run_cmd("loot", "totals", "--include-credits")
        self.assertIn("boxes 25 + sale proceeds 0 + earned credits 65 = all-in 90", out)
        self.assertNotIn("cash", out.lower())
        j, _ = self.run_cmd("loot", "totals", "--include-credits", "--json")
        self.assertEqual(json.loads(j)["all_in"]["Ann"]["1"], {"boxes": 25, "sale_proceeds": 0, "earned_credits": 65, "all_in": 90})
        self.assertIn("TOTAL economy 25 ", out, "the normal box-only total line is still there")

    def test_only_earning_sources_count_and_never_spending_or_box_pulls(self):
        self.earn("Ann", 40, "encounter", 1)
        self.earn("Ann", 100, "box", 1)                  # box credit pulls are already in box value
        self.run_cmd("credits", "Ann", "-10", "--reason", "bought rope", "--source", "vendor", "--floor", "1")
        self.run_cmd("credits", "Ann", "+7", "--reason", "gift", "--source", "transfer", "--floor", "1")
        j, _ = self.run_cmd("loot", "totals", "--include-credits", "--json")
        self.assertEqual(json.loads(j)["all_in"]["Ann"]["1"]["earned_credits"], 40)
        j, _ = self.run_cmd("loot", "totals", "--include-credits", "--credit-sources", "transfer,encounter", "--json")
        self.assertEqual(json.loads(j)["all_in"]["Ann"]["1"]["earned_credits"], 47)

    def test_floors_and_crawlers_are_kept_apart_and_filters_work(self):
        self.earn("Ann", 10, "encounter", 1)
        self.earn("Ann", 20, "encounter", 2)
        self.earn("Bo", 30, "encounter", 2)
        j, _ = self.run_cmd("loot", "totals", "--include-credits", "--floor", "2", "--crawler", "Ann", "--json")
        d = json.loads(j)["all_in"]
        self.assertEqual(list(d), ["Ann"])
        self.assertEqual(list(d["Ann"]), ["2"])
        self.assertEqual(d["Ann"]["2"]["earned_credits"], 20)

    def test_unrecorded_floor_is_flagged_and_assume_floor_places_it(self):
        self.earn("Ann", 40, "encounter")                # no --floor on this entry
        out, _ = self.run_cmd("loot", "totals", "--include-credits")
        self.assertIn("floor not recorded", out)
        self.assertIn("--assume-floor", out)
        out, _ = self.run_cmd("loot", "totals", "--include-credits", "--assume-floor", "1")
        self.assertIn("Ann F1: boxes 0 + sale proceeds 0 + earned credits 40 = all-in 40", out)
        self.assertNotIn("floor not recorded", out)
        self.run_cmd("loot", "totals", "--include-credits", "--assume-floor", "19", expect=1)
        self.run_cmd("loot", "totals", "--include-credits", "--assume-floor", "x", expect=1)

    def test_valve_check_on_floor_2_at_900(self):
        self.box("Ann", 2, 600)
        self.earn("Ann", 299, "encounter", 2)
        out, _ = self.run_cmd("loot", "totals", "--include-credits")
        self.assertIn("all-in 899 is below 900: no valve", out)
        self.earn("Ann", 1, "encounter", 2)
        out, _ = self.run_cmd("loot", "totals", "--include-credits")
        self.assertIn("has reached 900", out)
        self.assertIn("175 or less", out)
        self.assertNotIn("VALVE", self.run_cmd("loot", "totals")[0], "default output never mentions the valve")

    def test_valve_only_on_floor_2(self):
        self.earn("Ann", 950, "encounter", 1)
        out, _ = self.run_cmd("loot", "totals", "--include-credits")
        self.assertNotIn("VALVE", out)

    def test_all_in_over_1500_is_flagged(self):
        self.box("Ann", 1, 1400)
        self.earn("Ann", 200, "encounter", 1)
        out, _ = self.run_cmd("loot", "totals", "--include-credits")
        self.assertIn("FLAG: Ann F1 all-in 1600", out)

    def test_story_box_sale_proceeds_count_once(self):
        ledgers.append("story-box", {"event": "sold", "crawler": "Ann", "floor": 1, "price": 100, "item": "Thing", "story_value": 5, "reason": "r"})
        self.earn("Ann", 10, "encounter", 1)
        j, _ = self.run_cmd("loot", "totals", "--include-credits", "--json")
        self.assertEqual(json.loads(j)["all_in"]["Ann"]["1"]["all_in"], 110)

    def test_credits_floor_argument_is_validated_and_default_row_unchanged(self):
        self.run_cmd("credits", "Ann", "+5", "--reason", "x", "--floor", "19", expect=1)
        self.run_cmd("credits", "Ann", "+5", "--reason", "x", "--floor", "\u0663", expect=1)
        self.assertEqual(self.crawler("Ann")["credits"], 0)
        self.run_cmd("credits", "Ann", "+5", "--reason", "plain")
        with open(os.path.join(self.sessions, "credit-ledger.jsonl"), encoding="utf-8") as f:
            last = json.loads(f.read().splitlines()[-1])
        self.assertNotIn("floor", last, "without --floor the ledger row has exactly the old shape")

    def test_pure_functions(self):
        entries = [{"crawler": "A", "delta": 5, "source": "encounter", "floor": 1}, {"crawler": "A", "delta": -5, "source": "encounter", "floor": 1},
                   {"crawler": "A", "delta": 9, "source": "box", "floor": 1}, {"crawler": "A", "delta": 3, "source": "r1"}]
        self.assertEqual(loot.credit_income(entries), {"A": {1: 5, None: 3}})
        self.assertEqual(loot.credit_income(entries, assume_floor=1), {"A": {1: 8}})
        self.assertEqual(loot.credit_income(entries, floor=1, assume_floor=1), {"A": {1: 8}})
        self.assertEqual(loot.credit_income(entries, floor=2), {})


if __name__ == "__main__":
    unittest.main()
