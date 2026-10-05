"""loot draw / totals, Legendary cap + bound + story_value, box ledger, banner archive, achievement --reward."""
import json
import os
import unittest

from test_state import StateTestCase


def card(i, tier="Bronze", weight=10, **kw):
    c = {"id": f"f01-z06-{i:04d}", "floor": 1, "zone": "z06", "tier": tier, "box_types": ["any"], "pull_type": "weird", "kind": "item",
         "reskin_name": f"Thing {i}", "real_5e_name": f"Real {i}", "source_5e": "HOUSE", "rarity": "Common", "attunement": None, "category": "Misc",
         "plain_mechanics": {"text": f"Does thing {i}.", "uses": None}, "credit_value": 25, "draw_weight": weight, "unique": False,
         "tailor_tags": [], "exclusive_to": None, "grant": None, "ledger": {"type": "item", "text": f"item +1 {tier} box: Thing {i}"}, "box_name": "X Box", "deed": "Did X", "notes": ""}
    c.update(kw)
    return c


class LootTests(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Ann", "--player", "P", "--class", "Fighter", "--species", "Human")
        self.run_cmd("add-crawler", "Bo", "--player", "Q", "--class", "Wizard", "--species", "Human")
        self.run_cmd("scene", "safe-room", "on")
        d = os.path.join(self.tmp.name, "tables", "loot-decks")
        os.makedirs(d)
        self.cards = [
            card(1), card(2, weight=0), card(3, kind="credits", grant={"credits": 40, "roll": None}, credit_value=40, category="Credits"),
            card(4, unique=True), card(5, exclusive_to="Bo"), card(6, ledger={"type": "item", "text": "stub"}, real_5e_name="NEEDS-VERIFY thing"),
            card(7, tier="Legendary", weight=0, credit_value=50000, rarity="Legendary"), card(8, tier="Legendary", weight=0, credit_value=70000),
            card(9, tier="Legendary", weight=0, kind="credits", grant={"credits": 5}, credit_value=1),
        ]
        with open(os.path.join(d, "f01-z06-test.json"), "w") as f:
            json.dump({"schema": "loot-deck/0.1.1", "deck_id": "t", "version": "0.1.0", "floor": 1, "zone": "z06", "cards": self.cards}, f)
        with open(os.path.join(d, "ach-f01-x.json"), "w") as f:  # achievements file: must be ignored
            json.dump({"schema": "achievements/0.1", "floor": 1, "zone": "z06", "cards": [card(99)]}, f)
        with open(os.path.join(d, "broken.json"), "w") as f:
            f.write("{nope")

    def ledger(self):
        with open(os.path.join(self.tmp.name, "sessions", "loot-ledger.jsonl")) as f:
            return [json.loads(l) for l in f]

    def test_pick_item_adds_inventory_card_data_and_ledger(self):
        out, _ = self.run_cmd("loot", "draw", "1", "6-break-room", "--crawler", "Ann", "--pick", "f01-z06-0001")
        self.assertIn("LOOT | Ann | F01/z06 | f01-z06-0001 | Bronze | item | value 25", out)
        inv = self.load()["crawlers"][0]["inventory"][0]
        self.assertEqual((inv["name"], inv["mechanics"], inv["notes"]), ("Thing 1", "Does thing 1.", "Real 1"))
        e = self.ledger()[0]
        self.assertEqual((e["economy_value"], e["story_value"], e["pick"]), (25, 0, True))
        with open(os.path.join(self.tmp.name, "exports", "card-data.json")) as f:
            self.assertIn("thing 1", json.load(f)["items"])
        with open(os.path.join(self.tmp.name, "sessions", "loot.log")) as f:
            self.assertTrue(f.read().startswith("LOOT |"))

    def test_random_draw_skips_weight0_stubs_legendary_wrong_exclusive_and_other_files(self):
        seen = set()
        for _ in range(30):
            out, _ = self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann")
            seen.add(json.loads(json.dumps(self.ledger()[-1]))["card_id"])
            if "f01-z06-0004" in seen:
                break
        self.assertTrue(seen <= {"f01-z06-0001", "f01-z06-0003", "f01-z06-0004"}, seen)
        _, err = self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0099", expect=1)
        self.assertIn("not in", err)
        _, err = self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0006", expect=1)
        self.assertIn("needs-verify", err)

    def test_weight0_only_by_pick_and_unique_once(self):
        self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0002")
        self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0004")
        _, err = self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Bo", "--pick", "f01-z06-0004", expect=1)
        self.assertIn("unique", err)
        _, err = self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0005", expect=1)
        self.assertIn("exclusive to Bo", err)

    def test_credits_card_writes_credit_ledger_with_reason(self):
        self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0003")
        self.assertEqual(self.load()["crawlers"][0]["credits"], 40)
        with open(os.path.join(self.tmp.name, "sessions", "credit-ledger.jsonl")) as f:
            r = [json.loads(l) for l in f][-1]
        self.assertEqual((r["delta"], r["reason"], r["source"]), (40, "Bronze box pull f01-z06-0003", "box"))
        self.assertEqual(self.ledger()[0]["economy_value"], 40)

    def test_totals_economy_only_without_story_boxes(self):
        self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0001")
        self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Bo", "--pick", "f01-z06-0003")
        out, _ = self.run_cmd("loot", "totals")
        self.assertIn("Ann F1: economy 25 | 1 draw(s)", out)
        self.assertIn("TOTAL economy 65 ", out)
        one, _ = self.run_cmd("loot", "totals", "--crawler", "Ann", "--floor", "1", "--json")
        self.assertEqual(json.loads(one)["totals"]["Ann"]["1"]["economy_value"], 25)
        none, _ = self.run_cmd("loot", "totals", "--floor", "2")
        self.assertIn("no loot draws", none)

    def test_box_ledger_banner_archive_and_achievement_reward(self):
        self.run_cmd("box", "earn", "Ann", "bronze", "--deed", "Rescued the tent-pole", "--box-name", "Tent-Pole Rescue Box")
        self.run_cmd("box", "add", "Ann", "bronze")  # alias still works and is logged
        self.run_cmd("box", "open", "Ann", "bronze", "--contents", "Thing 1")
        out, _ = self.run_cmd("box", "show", "Ann")
        self.assertIn("Tent-Pole Rescue Box", out)
        self.assertIn("-> Thing 1", out)
        self.assertEqual(self.load()["crawlers"][0]["boxes"]["bronze"], 1)
        self.run_cmd("box", "use", "Ann", "bronze")
        self.run_cmd("banner", "log", "Achievement! Buddy System", "--crawler", "Ann")
        out, _ = self.run_cmd("banner", "show")
        self.assertIn("Buddy System", out)
        self.run_cmd("achievement", "add", "Ann", "Buddy System", "--reward", "A free hug, redeemable never.")
        self.assertEqual(self.load()["crawlers"][0]["achievements"][0]["reward"], "A free hug, redeemable never.")
        import publisher
        text = "\n".join(publisher.render_card(self.load()["crawlers"][0], {}))
        self.assertIn("Buddy System: A free hug, redeemable never.", text)


if __name__ == "__main__":
    unittest.main()
