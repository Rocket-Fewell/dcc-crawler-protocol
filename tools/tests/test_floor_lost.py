"""Decision 028: `floor-lost` (write-off of a dead Crawler's credits and items) and `loot-body` (survivor loot before the collapse), on temp copies only.
Every check runs against a throw-away DCC_CAMPAIGN_DIR; nothing here can touch the live state.json or credit-ledger.jsonl."""
import json
import os
import unittest

from test_state import StateTestCase


class FloorLostBase(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Bone", "--player", "Ann", "--class", "Barbarian", "--species", "Goliath", "--credits", "127", "--reason", "intake")
        self.run_cmd("add-crawler", "Horn", "--player", "Bo", "--class", "Fighter", "--species", "Human", "--credits", "75", "--reason", "intake")
        self.run_cmd("add-crawler", "Pip", "--player", "Cy", "--class", "Rogue", "--species", "Human", "--credits", "10", "--reason", "intake")
        for n, q in (("Rope", 2), ("Healer's Kit", 1)):
            self.run_cmd("inventory", "add", "Bone", n, "--qty", str(q))
        self.run_cmd("condition", "add", "Bone", "Dead")

    def rows(self):
        with open(os.path.join(self.sessions, "credit-ledger.jsonl"), encoding="utf-8") as f:
            return [json.loads(l) for l in f]

    def total(self, name):
        return sum(r["delta"] for r in self.rows() if r["crawler"] == name)

    def verify(self, expect=0):
        return self.run_cmd("ledger", "verify", expect=expect)[0]


class FloorLostCase(FloorLostBase):
    pass

    # ---- floor-lost
    def test_floor_lost_zeroes_balance_records_exact_coins_and_items_and_verify_passes(self):
        before = len(self.rows())
        old_rows = self.rows()
        self.run_cmd("floor-lost", "Bone", "--reason", "missed the F1 collapse", "--floor", "1")
        rows = self.rows()
        self.assertEqual(rows[:before], old_rows, "existing entries are never altered")
        self.assertEqual(len(rows), before + 1, "one append-only entry")
        e = rows[-1]
        self.assertEqual((e["crawler"], e["delta"], e["balance"], e["event"], e["source"], e["floor"]), ("Bone", -127, 0, "floor_lost", "floor_lost", 1))
        self.assertEqual(e["destroyed"]["coins"], 127)
        self.assertEqual(sorted((i["name"], i["qty"]) for i in e["destroyed"]["items"]), [("Healer's Kit", 1), ("Rope", 2)])
        self.assertEqual(e["destroyed"]["item_count"], 3)
        c = self.crawler("Bone")
        self.assertEqual((c["credits"], c["inventory"]), (0, []))
        self.assertEqual(self.total("Bone"), 0, "ledger totals reconcile to zero with no special case")
        self.assertIn("ledger OK", self.verify())
        self.assertIn("FLOOR LOST", self.verify())
        self.assertEqual(self.crawler("Horn")["credits"], 75, "other Crawlers untouched")

    def test_second_write_off_is_refused_and_adds_nothing(self):
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        n = len(self.rows())
        out, err = self.run_cmd("floor-lost", "Bone", "--reason", "r")      # exits 0 with a clear message (Accountant fix 5)
        self.assertIn("nothing left to destroy", out + err)
        self.assertEqual(len(self.rows()), n, "no ledger entry added")

    def test_validation(self):
        _, err = self.run_cmd("floor-lost", "Bone", expect=1)           # no reason
        _, err = self.run_cmd("floor-lost", "Horn", "--reason", "r", expect=1)
        self.assertIn("not DEAD", err)
        self.assertEqual(self.crawler("Horn")["credits"], 75)
        self.run_cmd("floor-lost", "Horn", "--reason", "r", "--dry-run", "--mark-dead")
        self.assertEqual(self.crawler("Horn")["credits"], 75)           # dry run changes nothing
        self.run_cmd("floor-lost", "Nobody", "--reason", "r", expect=1)

    def test_mark_dead_does_it_in_one_step(self):
        self.run_cmd("floor-lost", "Horn", "--reason", "missed the collapse", "--mark-dead")
        c = self.crawler("Horn")
        self.assertIn("Dead", c["conditions"])
        self.assertEqual((c["credits"], self.total("Horn")), (0, 0))
        self.verify()

    def test_zero_balance_with_items_still_writes_a_row(self):
        self.run_cmd("credits", "Bone", "=0", "--reason", "spent", "--benched-ok", "dead")
        n = len(self.rows())
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        e = self.rows()[-1]
        self.assertEqual((len(self.rows()), e["delta"], e["destroyed"]["coins"], e["destroyed"]["item_count"]), (n + 1, 0, 0, 3))
        self.verify()

    def test_npcs_and_the_ai_lose_nothing(self):
        self.run_cmd("set", "crawlers.pip.kind", '"companion"')
        _, err = self.run_cmd("floor-lost", "Pip", "--reason", "r", "--mark-dead", expect=1)
        self.assertIn("stasis", err)
        self.assertEqual(self.crawler("Pip")["credits"], 10)

    def test_verify_catches_a_tampered_write_off(self):
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        p = os.path.join(self.sessions, "credit-ledger.jsonl")
        lines = open(p, encoding="utf-8").read().splitlines()
        e = json.loads(lines[-1]); e["destroyed"]["coins"] = 100
        lines[-1] = json.dumps(e)
        open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        out = self.verify(expect=1)
        self.assertIn("destroyed", out)

    # ---- loot-body
    def test_loot_body_debits_the_body_and_credits_the_survivor_once_with_the_items(self):
        before = len(self.rows())
        out, _ = self.run_cmd("loot-body", "Bone", "Horn", "--coins", "100", "--item", "Rope=1", "--reason", "looted before the collapse", "--floor", "1")
        rows = self.rows()
        self.assertEqual(len(rows), before + 2)
        f, t = rows[-2], rows[-1]
        self.assertEqual((f["crawler"], f["delta"], f["role"], f["event"], f["source"]), ("Bone", -100, "from", "body_loot", "loot_body"))
        self.assertEqual((t["crawler"], t["delta"], t["role"]), ("Horn", 100, "to"))
        self.assertEqual(f["transfer_id"], t["transfer_id"])
        self.assertEqual(f["delta"] + t["delta"], 0, "no credit counted twice or lost")
        self.assertEqual(f["items"], t["items"])
        self.assertEqual([(i["name"], i["qty"]) for i in f["items"]], [("Rope", 1)])
        bone, horn = self.crawler("Bone"), self.crawler("Horn")
        self.assertEqual((bone["credits"], horn["credits"]), (27, 175))
        self.assertEqual({i["name"]: i["qty"] for i in bone["inventory"]}, {"Rope": 1, "Healer's Kit": 1})
        self.assertEqual({i["name"]: i["qty"] for i in horn["inventory"]}, {"Rope": 1})
        self.assertIn("ledger OK", self.verify())

    def test_loot_then_floor_lost_reconciles_everything_and_total_credits_are_conserved(self):
        total_before = sum(c["credits"] for c in self.load()["crawlers"])
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "all", "--all-items", "--reason", "grabbed it all")
        self.assertEqual(sum(c["credits"] for c in self.load()["crawlers"]), total_before, "looting moves credits, it never creates or destroys them")
        self.run_cmd("loot-body", "Bone", "Pip", "--item", "Rope", "--reason", "nothing there", expect=1)   # Rope already taken
        # nothing left on the body: the write-off exits 0 with "nothing left to destroy" and adds no entry, so no double counting
        n_rows = len(self.rows())
        out, err = self.run_cmd("floor-lost", "Bone", "--reason", "r")
        self.assertIn("nothing left to destroy", out + err)
        self.assertEqual(len(self.rows()), n_rows)
        self.assertEqual(self.total("Bone"), 0)
        self.assertEqual(self.total("Horn"), 75 + 127)
        self.verify()

    def test_partial_loot_then_floor_lost_destroys_exactly_the_rest(self):
        self.run_cmd("loot-body", "Bone", "Pip", "--coins", "27", "--item", "Healer's Kit", "--reason", "pre-collapse loot")
        self.run_cmd("floor-lost", "Bone", "--reason", "collapse", "--floor", "1")
        e = self.rows()[-1]
        self.assertEqual((e["delta"], e["balance"], e["destroyed"]["coins"]), (-100, 0, 100))
        self.assertEqual([(i["name"], i["qty"]) for i in e["destroyed"]["items"]], [("Rope", 2)])
        self.assertEqual(self.total("Bone"), 0)
        self.assertEqual(self.crawler("Pip")["credits"], 37)
        self.verify()

    def test_loot_body_validation(self):
        r = ("--reason", "x")
        self.run_cmd("loot-body", "Horn", "Pip", "--coins", "5", *r, expect=1)                 # a living Crawler is not a body (use transfer)
        self.run_cmd("loot-body", "Bone", "Horn", *r, expect=1)                                # nothing to take
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "500", *r, expect=1)              # more than the body has
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "-5", *r, expect=1)
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Rope=9", *r, expect=1)
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Sword", *r, expect=1)
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "5", expect=1)                    # no reason
        self.run_cmd("loot-body", "Bone", "Bone", "--coins", "5", *r, expect=1)
        self.run_cmd("condition", "add", "Horn", "Dead")
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "5", *r, expect=1)                # a dead survivor cannot loot
        self.run_cmd("condition", "remove", "Horn", "Dead")
        self.run_cmd("add-crawler", "Bone Two", "--player", "Ann", "--class", "Rogue", "--species", "Human")
        self.run_cmd("loot-body", "Bone", "Bone Two", "--coins", "5", *r, expect=1)            # same player
        self.assertEqual((self.crawler("Bone")["credits"], self.crawler("Horn")["credits"]), (127, 75), "every refusal left the balances alone")
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "5", "--dry-run", *r)
        self.assertEqual(self.crawler("Horn")["credits"], 75)

    def test_story_box_item_keeps_provenance_when_looted(self):
        self.run_cmd("set", "crawlers.bone.inventory.-", '{"name": "Story Thing", "qty": 1, "story_box_id": "SB1", "story_value": 5, "card_id": "c1"}')
        self.run_cmd("loot-body", "Bone", "Horn", "--item", "Story Thing", "--reason", "x")
        it = next(i for i in self.crawler("Horn")["inventory"] if i["name"] == "Story Thing")
        self.assertEqual((it["story_box_id"], it["story_value"]), ("SB1", 5))
        self.verify()

    def test_verify_catches_unpaired_or_unbalanced_body_loot(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "10", "--reason", "x")
        p = os.path.join(self.sessions, "credit-ledger.jsonl")
        lines = open(p, encoding="utf-8").read().splitlines()
        e = json.loads(lines[-1]); e["coins"] = 11     # the 'to' row now claims a different coin count than its delta
        lines[-1] = json.dumps(e)
        open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        self.assertIn("do not match", self.verify(expect=1))
        # drop the 'to' row altogether: the credit would be counted once only
        open(p, "w", encoding="utf-8").write("\n".join(lines[:-1]) + "\n")
        self.assertIn("missing", self.verify(expect=1))

    def test_run_state_does_not_leak_between_commands(self):
        self.run_cmd("loot-body", "Bone", "Horn", "--coins", "1", "--reason", "x")
        self.run_cmd("credits", "Horn", "+3", "--reason", "plain")
        e = self.rows()[-1]
        self.assertNotIn("event", e)
        self.assertNotIn("transfer_id", e)


class AccountantFixesCase(FloorLostBase):
    """Job 3 (Accountant): strict quantities, companions, ASCII digits, tamper detection of destroyed.items, floor range, empty write-off."""

    def loot(self, *extra, expect=0):
        return self.run_cmd("loot-body", "Bone", "Horn", "--reason", "x", *extra, expect=expect)

    def assert_nothing_moved(self):
        self.assertEqual((self.crawler("Bone")["credits"], self.crawler("Horn")["credits"]), (127, 75))
        self.assertEqual(sorted((i["name"], i["qty"]) for i in self.crawler("Bone")["inventory"]), [("Healer's Kit", 1), ("Rope", 2)])
        self.assertFalse(any(i["name"] == "Rope" for i in self.crawler("Horn")["inventory"]))

    # (1) bad quantities are refused, never silently 1
    def test_bad_item_quantities_are_refused(self):
        for spec in ("Rope=-1", "Rope=abc", "Rope=2.5", "Rope=", "Rope=1e2", "Rope= ", "=3"):
            _, err = self.loot("--item", spec, expect=1)
            self.assertIn("--item", err, spec)
        self.assert_nothing_moved()

    def test_zero_quantity_has_its_own_clear_message(self):
        _, err = self.loot("--item", "Rope=0", expect=1)
        self.assertIn("quantity of 0 takes nothing", err)
        self.assert_nothing_moved()

    def test_good_quantities_still_work(self):
        self.loot("--item", "Rope=2")
        self.assertEqual(next(i for i in self.crawler("Horn")["inventory"] if i["name"] == "Rope")["qty"], 2)
        self.verify()

    def test_plain_item_name_means_one(self):
        self.loot("--item", "Rope")
        self.assertEqual(next(i for i in self.crawler("Horn")["inventory"] if i["name"] == "Rope")["qty"], 1)

    # (2) a companion is not a looter (nor a body)
    def test_companion_cannot_loot_and_is_not_a_body(self):
        self.run_cmd("set", "crawlers.pip.kind", '"companion"')
        _, err = self.run_cmd("loot-body", "Bone", "Pip", "--coins", "5", "--reason", "x", expect=1)
        self.assertIn("companion", err)
        self.assertIn("REFUSED", err)
        self.run_cmd("condition", "add", "Pip", "Dead")
        _, err = self.run_cmd("loot-body", "Pip", "Horn", "--coins", "1", "--reason", "x", expect=1)
        self.assertIn("companion", err)
        self.assertEqual((self.crawler("Bone")["credits"], self.crawler("Pip")["credits"]), (127, 10))

    # (3) ASCII digits only
    def test_non_ascii_digits_are_refused(self):
        for bad in ("\u0663", "\uff15", "\u0665\u0665"):          # Arabic-Indic 3, fullwidth 5, ...
            _, err = self.loot("--coins", bad, expect=1)
            self.assertIn("whole number", err)
            _, err = self.loot("--item", "Rope=" + bad, expect=1)
            self.assertIn("--item", err)
            _, err = self.run_cmd("floor-lost", "Bone", "--reason", "r", "--floor", bad, expect=1)
            self.assertIn("--floor", err)
        self.assert_nothing_moved()
        self.assertEqual(self.crawler("Bone")["credits"], 127)

    def test_credits_amount_is_ascii_only(self):
        self.run_cmd("credits", "Horn", "+\u0665", "--reason", "x", expect=1)
        self.assertEqual(self.crawler("Horn")["credits"], 75)
        self.run_cmd("credits", "Horn", "+5", "--reason", "x")
        self.assertEqual(self.crawler("Horn")["credits"], 80)

    # (4) verify catches tampering with destroyed.items
    def _tamper(self, fn):
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        p = os.path.join(self.sessions, "credit-ledger.jsonl")
        lines = open(p, encoding="utf-8").read().splitlines()
        e = json.loads(lines[-1]); fn(e["destroyed"])
        lines[-1] = json.dumps(e)
        open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        return self.verify(expect=1)

    def test_verify_catches_emptied_destroyed_items(self):
        out = self._tamper(lambda d: d.update(items=[]))
        self.assertIn("item_count", out)

    def test_verify_catches_changed_quantity(self):
        out = self._tamper(lambda d: d["items"][0].update(qty=d["items"][0]["qty"] + 5))
        self.assertIn("item_count", out)

    def test_verify_catches_items_and_count_edited_together_via_fingerprint(self):
        def both(d):
            d["items"] = [i for i in d["items"] if i["name"] != "Rope"]
            d["item_count"] = sum(i["qty"] for i in d["items"])
        self.assertIn("fingerprint", self._tamper(both))

    def test_verify_catches_malformed_or_duplicate_rows(self):
        self.assertIn("malformed", self._tamper(lambda d: d["items"][0].update(qty=0)))

    def test_verify_clean_write_off_passes(self):
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        self.assertIn("ledger OK", self.verify())

    # (5) --floor 1-18; empty write-off exits 0
    def test_floor_range(self):
        for bad in ("0", "19", "-1", "2.5", "abc", "1e1"):
            _, err = self.run_cmd("floor-lost", "Bone", "--reason", "r", "--floor", bad, expect=1)
            self.assertIn("1 to 18", err, bad)
            _, err = self.loot("--coins", "1", "--floor", bad, expect=1)
            self.assertIn("1 to 18", err, bad)
        self.assertEqual(self.crawler("Bone")["credits"], 127)
        self.loot("--coins", "1", "--floor", "18")
        self.run_cmd("floor-lost", "Bone", "--reason", "r", "--floor", "1")
        self.assertEqual(self.rows()[-1]["floor"], 1)

    def test_empty_write_off_exits_zero_with_a_clear_message_and_adds_nothing(self):
        self.run_cmd("floor-lost", "Bone", "--reason", "r")
        n = len(self.rows())
        out, err = self.run_cmd("floor-lost", "Bone", "--reason", "again")
        self.assertIn("nothing left to destroy", out + err)
        out, err = self.run_cmd("floor-lost", "Bone", "--reason", "again", "--dry-run")
        self.assertIn("nothing left to destroy", out + err)
        self.assertEqual(len(self.rows()), n)
        self.verify()


if __name__ == "__main__":
    unittest.main()
