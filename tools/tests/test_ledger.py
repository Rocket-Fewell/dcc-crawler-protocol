"""Credit ledger tests for tools/state.py."""
import json
import os
import unittest

from test_state import StateTestCase


class LedgerTests(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Bone", "--player", "P", "--class", "Barbarian", "--species", "Goliath", "--credits", "13", "--reason", "intake")

    def rows(self):
        with open(os.path.join(self.sessions, "credit-ledger.jsonl"), encoding="utf-8") as f:
            return [json.loads(l) for l in f]

    def test_every_change_is_recorded_with_balance_and_reason(self):
        self.run_cmd("credits", "Bone", "+25", "--reason", "Buddy System", "--source", "achievement")
        _, err = self.run_cmd("credits", "Bone", "-1")
        self.assertIn("unspecified", err)
        r = self.rows()
        self.assertEqual([(x["delta"], x["balance"]) for x in r], [(13, 13), (25, 38), (-1, 37)])
        self.assertEqual(r[1]["reason"], "Buddy System")
        self.assertEqual(r[1]["source"], "achievement")
        self.assertEqual(r[2]["reason"], "unspecified")

    def test_unsigned_amount_means_plus(self):
        self.run_cmd("credits", "Bone", "25", "--reason", "x")
        self.assertEqual(self.load()["crawlers"][0]["credits"], 38)

    def test_non_credit_change_adds_no_row(self):
        n = len(self.rows())
        self.run_cmd("hp", "damage", "Bone", "2")
        self.assertEqual(len(self.rows()), n)

    def test_verify_ok_then_detects_hand_edit(self):
        self.run_cmd("credits", "Bone", "+5", "--reason", "r")
        out, _ = self.run_cmd("ledger", "verify")
        self.assertIn("ledger OK", out)
        s = self.load()
        s["crawlers"][0]["credits"] = 999
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(s, f)
        self.run_cmd("ledger", "verify", expect=1)

    def test_show_filters_by_crawler(self):
        self.run_cmd("credits", "Bone", "+5", "--reason", "loot roll")
        out, _ = self.run_cmd("ledger", "show", "--crawler", "Bone")
        self.assertIn("loot roll", out)

    def test_import_backfills_empty_ledger_only(self):
        os.remove(os.path.join(self.sessions, "credit-ledger.jsonl"))
        f = os.path.join(self.tmp.name, "bf.json")
        with open(f, "w") as fh:
            json.dump([{"crawler": "Bone", "delta": 10, "reason": "open"}, {"crawler": "Bone", "delta": 3, "reason": "vent"}], fh)
        out, _ = self.run_cmd("ledger", "import", f)
        self.assertIn("imported 2", out)
        self.run_cmd("ledger", "import", f, expect=1)  # already has entries
        self.run_cmd("ledger", "verify")


if __name__ == "__main__":
    unittest.main()
