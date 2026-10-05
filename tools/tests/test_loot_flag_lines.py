"""Per-floor inflation flag lines for `loot totals` (and the --include-credits ALL-IN view), read from rules/70-encounter-budget-5e.json.
Fixtures only: every budget file here is written into a temp DCC_CAMPAIGN_DIR; the real rules file and live ledgers are never touched."""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import ledgers  # noqa: E402
import loot  # noqa: E402
from test_state import StateTestCase  # noqa: E402

# Golden output of the code before per-floor flags existed (Floors 1-2 must stay byte-identical).
GOLD_TOTALS = ("crawler / floor: economy value | draws\n- Ann F1: economy 1400 | 3 draw(s)\n- Ann F2: economy 1600 | 4 draw(s)\n"
               "FLAG: Ann F1 economy value 1400 + 200 Story Box sale proceeds is over 1,500 (the award's story value is excluded; sale proceeds count)\n"
               "FLAG: Ann F2 economy value 1600 is over 1,500 (the award's story value is excluded; sale proceeds count)\n"
               "FLAG: Ann sold Story Box item Thing on F1: 200 credits received, story value 5 is provenance only and was NOT credited (r)\n"
               "TOTAL economy 3000 (what the Accountant audits)")
GOLD_ALLIN = ("ALL-IN credits per Crawler per floor (boxes + Story Box sale proceeds + earned credits from sources: encounter):\n"
              "- Ann F1: boxes 1400 + sale proceeds 200 + earned credits 10 = all-in 1610\nFLAG: Ann F1 all-in 1610 is over 1,500 credits for the floor\n"
              "- Ann F2: boxes 1600 + sale proceeds 0 + earned credits 0 = all-in 1600\nFLAG: Ann F2 all-in 1600 is over 1,500 credits for the floor\n"
              "VALVE (optional, A12): Ann F2 all-in 1600 has reached 900: the GM may hand-pick the Boss Box from cards worth 175 or less")
T12 = {"Ann": {1: {"economy_value": 1400, "story_value": 0, "draws": 3, "legendary": 0}, 2: {"economy_value": 1600, "story_value": 0, "draws": 4, "legendary": 0}}}
SALES = [{"event": "sold", "crawler": "Ann", "floor": 1, "price": 200, "item": "Thing", "story_value": 5, "reason": "r"}]
AI12 = {"Ann": {1: {"boxes": 1400, "sale_proceeds": 200, "earned_credits": 10, "all_in": 1610}, 2: {"boxes": 1600, "sale_proceeds": 0, "earned_credits": 0, "all_in": 1600}}}

TABLE = [(1, 1500), (2, 1500), (3, 6500), (4, 6500), (5, 9000), (15, 263500)]


def budget_v014():
    return {"version": "0.1.4", "economy_audit": {"line": {"value": 1500}, "governor": {"hard_flag": 1500}},
            "proposed_floor_growth_curve": {"table": [{"floor": f, "flag_line": v, "expected_counted": 1} for f, v in TABLE]}}


def tot(floor, value, who="Ann"):
    return {who: {floor: {"economy_value": value, "story_value": 0, "draws": 1, "legendary": 0}}}


class FlagLineCase(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.rules = os.path.join(self.tmp.name, "rules")
        os.makedirs(self.rules)

    def write_budget(self, d, raw=None):
        with open(os.path.join(self.rules, "70-encounter-budget-5e.json"), "w", encoding="utf-8") as f:
            f.write(raw if raw is not None else json.dumps(d))

    # ---- floors 1 and 2: byte-identical to the old behaviour, with and without a budget file
    def test_floors_1_and_2_are_byte_identical_without_a_budget_file(self):
        self.assertEqual(loot.totals_text(T12, SALES), GOLD_TOTALS)
        self.assertEqual(loot.all_in_text(AI12, ["encounter"]), GOLD_ALLIN)

    def test_floors_1_and_2_are_byte_identical_with_the_v014_budget_file(self):
        self.write_budget(budget_v014())
        self.assertEqual(loot.totals_text(T12, SALES), GOLD_TOTALS)
        self.assertEqual(loot.all_in_text(AI12, ["encounter"]), GOLD_ALLIN)

    def test_floors_1_and_2_are_byte_identical_with_a_corrupt_budget_file(self):
        self.write_budget(None, raw="{not json")
        self.assertEqual(loot.totals_text(T12, SALES), GOLD_TOTALS)
        self.assertEqual(loot.all_in_text(AI12, ["encounter"]), GOLD_ALLIN)

    def test_flag_lines_for_floor_1_and_2_from_the_file(self):
        self.write_budget(budget_v014())
        f = loot.FlagLines()
        self.assertEqual((f.line(1)[0], f.line(2)[0]), (1500, 1500))
        self.assertEqual(f.source, "proposed_floor_growth_curve.table[].flag_line (v0.1.4)")

    # ---- floor 3 and floor 15 scale
    def test_floor_3_uses_its_own_line(self):
        self.write_budget(budget_v014())
        self.assertNotIn("FLAG: Ann F3", loot.totals_text(tot(3, 3000)))          # normal Crawler: no flag from F3 on
        out = loot.totals_text(tot(3, 7000))
        self.assertIn("FLAG: Ann F3 economy value 7000 is over 6,500 (", out)
        self.assertIn("FLAG LINES in use (credits per Crawler for the floor, source proposed_floor_growth_curve.table[].flag_line (v0.1.4)): F3 6,500", out)
        self.assertIn("F3 6,500", out)
        self.assertNotIn("cash", out.lower())

    def test_floor_15_uses_its_own_line(self):
        self.write_budget(budget_v014())
        self.assertNotIn("FLAG: Ann F15", loot.totals_text(tot(15, 100000)))
        self.assertIn("is over 263,500 (", loot.totals_text(tot(15, 270000)))
        self.assertIn("F15 263,500", loot.totals_text(tot(15, 1)))

    def test_all_in_view_uses_the_floor_line_and_names_it(self):
        self.write_budget(budget_v014())
        ai = {"Ann": {3: {"boxes": 3000, "sale_proceeds": 0, "earned_credits": 4000, "all_in": 7000}}}
        out = loot.all_in_text(ai, ["encounter"])
        self.assertIn("FLAG: Ann F3 all-in 7000 is over 6,500 credits for the floor", out)
        self.assertIn("F3 6,500", out)
        ai["Ann"][3]["all_in"] = 6000
        self.assertNotIn("FLAG:", loot.all_in_text(ai, ["encounter"]))

    # ---- fallback: never crash, note for floor 3+
    def test_missing_file_falls_back_to_1500_with_a_note_for_floor_3_plus(self):
        out = loot.totals_text(tot(3, 2000))
        self.assertIn("FLAG: Ann F3 economy value 2000 is over 1,500 (", out)
        self.assertIn("NOTE: F3: no flag line in the budget file (budget file rules/70-encounter-budget-5e.json not found); using the default 1,500 credits, which is not floor-scaled", out)

    def test_corrupt_or_keyless_file_falls_back_with_a_note(self):
        for raw in ("{nope", "[]", json.dumps({"version": "0.1.9"}), json.dumps({"proposed_floor_growth_curve": {"table": "x"}})):
            self.write_budget(None, raw=raw)
            out = loot.totals_text(tot(15, 2000))
            self.assertIn("is over 1,500 (", out, raw)
            self.assertIn("NOTE: F15:", out, raw)

    def test_floor_missing_from_the_file_gets_a_note_only_for_floor_3_plus(self):
        self.write_budget(budget_v014())
        self.assertIn("NOTE: F9:", loot.totals_text(tot(9, 2000)))
        self.assertNotIn("NOTE", loot.totals_text(tot(2, 1000)))

    # ---- v0.1.5+ per-floor map (key name not known yet): common shapes are picked up, and it wins over the v0.1.4 table
    def test_v015_flag_map_in_common_shapes_wins_over_the_table(self):
        shapes = [
            ({"economy_audit": {"flag_lines": {"1": 1500, "2": 1500, "3": 7000}}}, "economy_audit.flag_lines"),
            ({"flag_line_by_floor": {"F1": 1500, "F2": 1500, "F3": {"flag_line": 7000}}}, "flag_line_by_floor"),
            ({"proposed_floor_growth_curve": {"flag_lines_by_floor": [{"floor": 1, "flag_line": 1500}, {"floor": 2, "flag_line": 1500}, {"floor": 3, "flag_line": 7000}]}}, "proposed_floor_growth_curve.flag_lines_by_floor"),
            ({"economy_audit": {"some_new_flag_map": {"floor_1": 1500, "floor_2": 1500, "floor_3": 7000}}}, "economy_audit.some_new_flag_map"),   # unknown name: found by 'flag' in the key
        ]
        for extra, key in shapes:
            d = budget_v014()
            d["version"] = "0.1.5"
            for k, v in extra.items():
                if isinstance(v, dict) and isinstance(d.get(k), dict):
                    d[k].update(v)
                else:
                    d[k] = v
            self.write_budget(d)
            f = loot.FlagLines()
            self.assertEqual(f.line(3)[0], 7000, key)
            self.assertIn(key, f.source)
            self.assertIn("(v0.1.5)", f.source)

    def test_v015_map_with_a_floor_missing_falls_back_for_that_floor_only(self):
        d = budget_v014()
        d["version"] = "0.1.5"
        d["flag_lines"] = {"1": 1500, "2": 1500, "3": 7000}
        self.write_budget(d)
        f = loot.FlagLines()
        self.assertEqual(f.line(3), (7000, None))
        self.assertEqual(f.line(5)[0], 1500)
        self.assertIn("NOTE: F5:", "\n".join(f.footer({3, 5})))

    # ---- CLI end to end on a temp campaign
    def test_cli_totals_and_all_in_use_the_floor_line(self):
        self.write_budget(budget_v014())
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Ann", "--player", "P", "--class", "Fighter", "--species", "Human")
        ledgers.append("loot", {"crawler": "Ann", "floor": 3, "zone": "z1", "card_id": "x", "tier": "Gold", "kind": "item", "economy_value": 5000, "story_value": 0, "text": "t"})
        self.run_cmd("credits", "Ann", "+3000", "--reason", "encounter pay", "--source", "encounter", "--floor", "3")
        out, _ = self.run_cmd("loot", "totals")
        self.assertNotIn("FLAG: Ann F3", out)                                  # 5,000 is under the F3 line of 6,500
        out, _ = self.run_cmd("loot", "totals", "--include-credits")
        self.assertIn("= all-in 8000", out)
        self.assertIn("FLAG: Ann F3 all-in 8000 is over 6,500 credits for the floor", out)
        self.assertEqual(out.count("FLAG LINES in use"), 1)
        j, _ = self.run_cmd("loot", "totals", "--include-credits", "--json")
        self.assertEqual(json.loads(j)["all_in"]["Ann"]["3"]["all_in"], 8000)

    def test_cli_missing_budget_file_does_not_crash(self):
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Ann", "--player", "P", "--class", "Fighter", "--species", "Human")
        ledgers.append("loot", {"crawler": "Ann", "floor": 3, "zone": "z1", "card_id": "x", "tier": "Gold", "kind": "item", "economy_value": 5000, "story_value": 0, "text": "t"})
        out, _ = self.run_cmd("loot", "totals")
        self.assertIn("is over 1,500 (", out)
        self.assertIn("NOTE: F3:", out)


if __name__ == "__main__":
    unittest.main()
