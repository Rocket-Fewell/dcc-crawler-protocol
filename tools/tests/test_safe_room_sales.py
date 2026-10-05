"""Safe-room rule for every loot box, two-step Story Box, sell/transfer with provenance flags, floor multiplier, pet-crawler (Caleb 2026-10-04)."""
import json
import os
import unittest

from test_state import StateTestCase, TOOLS
from test_story_box import card


class SafeRoomSalesTests(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Ann", "--player", "P", "--class", "Fighter", "--species", "Human")
        self.run_cmd("add-crawler", "Bo", "--player", "Q", "--class", "Wizard", "--species", "Human")
        self.decks = os.path.join(self.tmp.name, "tables", "loot-decks")
        os.makedirs(self.decks)
        bronze = card(20, tier="Bronze", rarity="Common", draw_weight=10, unique=False, credit_value=25, box_name="X Box")
        bronze.pop("story_value"), bronze.pop("bound"), bronze.pop("sale_value")
        cards = [card(1), card(2, sale_value=250), card(3, sale_value=None), bronze]
        with open(os.path.join(self.decks, "d.json"), "w") as f:
            json.dump({"schema": "loot-deck/0.1.2", "deck_id": "d", "version": "0.1.0", "floor": 1, "zone": "z06", "cards": cards}, f)

    def rows(self, name):
        p = os.path.join(self.tmp.name, "sessions", name)
        if not os.path.exists(p):
            return []
        with open(p) as f:
            return [json.loads(l) for l in f if l.strip()]

    def award(self, cid="f01-z06-0001", who="Ann", *extra):
        return self.run_cmd("loot", "story-box", "1", "z06", "--crawler", who, "--pick", cid, "--deed", "Did a notable thing here", "--deed-id", "d-" + cid[-4:],
                            "--witness", "GM", "--override-cap", "test", *extra)

    # --- safe room
    def test_loot_draw_and_box_open_refuse_outside_a_safe_room(self):
        _, err = self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", expect=1)
        self.assertIn("only be opened in a safe room", err)
        self.assertEqual(self.rows("loot-ledger.jsonl"), [])
        self.run_cmd("box", "earn", "Ann", "gold")
        _, err = self.run_cmd("box", "open", "Ann", "gold", expect=1)
        self.assertIn("safe room", err)
        self.assertEqual(self.load()["crawlers"][0]["boxes"]["gold"], 1)
        self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", "--dry-run")  # a dry run is fine anywhere
        self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", "--safe-room")
        self.assertEqual(self.rows("loot-ledger.jsonl")[0]["safe_room"], "flag")
        self.run_cmd("box", "open", "Ann", "gold", "--safe-room")
        self.assertEqual(self.rows("box-ledger.jsonl")[-1]["safe_room"], "flag")

    def test_scene_flag_on_off_show(self):
        out, _ = self.run_cmd("scene", "show")
        self.assertIn("off", out)
        self.run_cmd("scene", "safe-room", "on", "--note", "Floor 1 stairwell")
        self.assertIn("ON", self.run_cmd("scene", "show")[0])
        self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann")
        self.assertEqual(self.rows("loot-ledger.jsonl")[0]["safe_room"], "scene")
        self.run_cmd("scene", "safe-room", "off")
        self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Bo", expect=1)

    def test_story_box_award_then_open_two_steps(self):
        out, _ = self.award()
        self.assertIn("STORY BOX EARNED (unopened)", out)
        st = self.load()["crawlers"][0]
        self.assertEqual((st["inventory"], st["boxes"]["legendary"]), ([], 1))
        self.assertEqual(self.rows("loot-ledger.jsonl"), [])
        self.assertEqual([(r["event"], r["tier"]) for r in self.rows("box-ledger.jsonl")], [("earned", "legendary")])
        dry, _ = self.run_cmd("loot", "story-box", "--open", "--crawler", "Ann", "--dry-run")
        self.assertIn("NO: a real open would be refused", dry)
        _, err = self.run_cmd("loot", "story-box", "--open", "--crawler", "Ann", expect=1)
        self.assertIn("safe room", err)
        self.assertEqual(self.load()["crawlers"][0]["inventory"], [])
        _, err = self.run_cmd("box", "open", "Ann", "legendary", "--safe-room", expect=1)
        self.assertIn("Story Box", err)
        out, _ = self.run_cmd("loot", "story-box", "--open", "--crawler", "Ann", "--safe-room")
        self.assertIn("opened Legendary", out)
        st = self.load()["crawlers"][0]
        self.assertEqual((st["inventory"][0]["name"], st["boxes"]["legendary"], st["inventory"][0]["sale_value"]), ("Story Thing 1", 0, 500))
        self.assertEqual(self.rows("loot-ledger.jsonl")[0]["safe_room"], "flag")
        self.assertEqual([r["event"] for r in self.rows("box-ledger.jsonl")], ["earned", "opened"])
        _, err = self.run_cmd("loot", "story-box", "--open", "--crawler", "Ann", "--safe-room", expect=1)
        self.assertIn("no unopened", err)

    def test_open_refused_for_a_dead_crawler_and_unknown_box_id(self):
        self.award()
        out, _ = self.run_cmd("condition", "add", "Ann", "Dead")
        self.assertIn("STORY BOX RECLAIMED", out)   # Caleb 2026-10-04: dying with an unopened box reclaims it
        _, err = self.run_cmd("loot", "story-box", "--open", "--crawler", "Ann", "--safe-room", expect=1)
        self.assertIn("no unopened", err)
        self.run_cmd("condition", "remove", "Ann", "Dead")
        _, err = self.run_cmd("loot", "story-box", "--open", "--crawler", "Ann", "--safe-room", "--box-id", "nope", expect=1)
        self.assertIn("no unopened", err)

    def test_cap_is_per_floor_and_counts_unopened_boxes(self):
        self.run_cmd("loot", "story-box", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0001", "--deed", "Did a notable thing here", "--deed-id", "a")
        _, err = self.run_cmd("loot", "story-box", "1", "z06", "--crawler", "Bo", "--pick", "f01-z06-0002", "--deed", "Did another thing", "--deed-id", "b", expect=1)
        self.assertIn("floor 1", err)
        self.assertNotIn("session", err)
        self.assertNotIn("bound", err.lower())

    # --- sell
    def opened(self, cid="f01-z06-0001", who="Ann"):
        self.award(cid, who)
        self.run_cmd("loot", "story-box", "--open", "--crawler", who, "--safe-room")

    def test_system_buyback_pays_sale_value_times_floor_multiplier(self):
        self.opened("f01-z06-0002")  # sale_value 250
        self.run_cmd("sell", "Ann", "Story Thing 2", "--reason", "sold to the System", "--floor", "5")
        c = self.load()["crawlers"][0]
        self.assertEqual((c["credits"], c["inventory"]), (250 * 5, []))
        e = self.rows("credit-ledger.jsonl")[-1]
        self.assertEqual((e["delta"], e["source"]), (1250, "sale"))
        self.assertIn("sale_value 250 x5", e["reason"])
        self.assertEqual(e["provenance"]["story_value"], 40000)
        self.assertNotEqual(e["delta"], 40000)

    def test_default_sale_value_500_and_each_floor_band(self):
        import loot
        self.assertEqual([loot.floor_multiplier(f) for f in (1, 4, 5, 9, 10, 14, 15, 18)], [1, 1, 5, 5, 20, 20, 50, 50])
        self.opened("f01-z06-0003")  # card has no sale_value
        self.assertEqual(self.load()["crawlers"][0]["inventory"][0]["sale_value"], 500)  # the System default
        self.run_cmd("sell", "Ann", "Story Thing 3", "--reason", "sold", "--floor", "10")
        self.assertEqual(self.load()["crawlers"][0]["credits"], 500 * 20)

    def test_sell_uses_current_floor_and_dry_run_and_reason_required(self):
        self.opened()
        self.run_cmd("sell", "Ann", "Story Thing 1", "--dry-run", "--reason", "x")
        self.assertEqual(len(self.load()["crawlers"][0]["inventory"]), 1)
        self.run_cmd("sell", "Ann", "Story Thing 1", expect=1)
        self.run_cmd("sell", "Ann", "Story Thing 1", "--reason", "System buyback")
        self.assertEqual(self.load()["crawlers"][0]["credits"], 500)  # floor 1: x1

    def test_sale_is_flagged_in_totals_and_ledger_verify_not_blocked(self):
        self.opened()
        self.run_cmd("sell", "Ann", "Story Thing 1", "--reason", "sold to the System")
        out, _ = self.run_cmd("loot", "totals")
        self.assertIn("FLAG: Ann sold Story Box item Story Thing 1", out)
        self.assertIn("story value 40000 is provenance only", out)
        out, _ = self.run_cmd("ledger", "verify")
        self.assertIn("FLAG:", out)
        self.assertIn("ledger OK", out)
        t, _ = self.run_cmd("loot", "totals", "--json")
        self.assertEqual(len(json.loads(t)["story_box_sales"]), 1)

    def test_sale_proceeds_count_toward_the_per_floor_flag(self):
        self.opened()
        self.run_cmd("sell", "Ann", "Story Thing 1", "--reason", "x", "--floor", "1")
        import loot
        t = {"Ann": {1: {"economy_value": 1200, "story_value": 0, "draws": 1, "legendary": 0}}}
        out = loot.totals_text(t, [{"event": "sold", "crawler": "Ann", "floor": 1, "price": 500, "item": "X", "story_value": 1, "reason": "r"}])
        self.assertIn("1200 + 500 Story Box sale proceeds is over 1,500", out)

    def test_non_story_item_needs_a_price(self):
        self.run_cmd("inventory", "add", "Ann", "Rope")
        self.run_cmd("sell", "Ann", "Rope", "--reason", "fence", expect=1)
        self.run_cmd("sell", "Ann", "Rope", "--reason", "fence", "--price", "40")
        self.assertEqual(self.load()["crawlers"][0]["credits"], 40)
        out, _ = self.run_cmd("ledger", "verify")
        self.assertNotIn("FLAG", out)

    # --- transfer
    def test_transfer_is_free_for_loot_or_gifts_and_keeps_provenance(self):
        self.opened()
        self.run_cmd("condition", "add", "Ann", "Dead")
        self.run_cmd("transfer", "Ann", "Bo", "Story Thing 1", "--reason", "looted from the corpse")
        st = self.load()
        self.assertEqual(st["crawlers"][0]["inventory"], [])
        self.assertEqual(st["crawlers"][1]["inventory"][0]["story_value"], 40000)
        self.assertEqual(self.rows("credit-ledger.jsonl"), [])
        out, _ = self.run_cmd("loot", "totals")
        self.assertNotIn("FLAG: Ann transferred", out)

    def test_priced_transfer_moves_credits_is_flagged_and_free_form(self):
        self.opened()
        self.run_cmd("credits", "Bo", "+300", "--reason", "seed")
        self.run_cmd("transfer", "Ann", "Bo", "Story Thing 1", "--price", "120", "--reason", "traded for coin")
        st = self.load()
        self.assertEqual((st["crawlers"][0]["credits"], st["crawlers"][1]["credits"]), (120, 180))
        self.assertEqual(st["crawlers"][1]["inventory"][0]["name"], "Story Thing 1")
        out, _ = self.run_cmd("loot", "totals")
        self.assertIn("FLAG: Ann transferred (for 120 credits) to Bo Story Box item Story Thing 1", out)
        out, _ = self.run_cmd("ledger", "verify")
        self.assertIn("FLAG:", out)
        self.assertIn("ledger OK", out)
        self.run_cmd("transfer", "Bo", "Ann", "Story Thing 1", "--price", "9999", "--reason", "x", expect=1)  # Ann cannot pay
        self.assertEqual(len(self.load()["crawlers"][0]["inventory"]), 0)

    def test_transfer_validation(self):
        self.run_cmd("transfer", "Ann", "Ann", "Rope", "--reason", "x", expect=1)
        self.run_cmd("transfer", "Ann", "Bo", "Rope", "--reason", "x", expect=1)
        self.run_cmd("transfer", "Ann", "Bo", "Rope", expect=1)

    # --- no more bound / repossess
    def test_no_bound_field_is_written_and_repossess_is_gone(self):
        self.opened()
        self.assertNotIn("bound", self.load()["crawlers"][0]["inventory"][0])
        self.run_cmd("loot", "story-box", "--repossess", "--crawler", "Ann", expect=2)

    # --- pet-crawler
    def pet_spec(self, name="Biscuit", **kw):
        s = {"name": name, "player": "P", "class": "Fighter", "species": "Dog", "abilities": {"str": 10, "dex": 10, "con": 10, "int": 10, "wis": 10, "cha": 10},
             "hp_max": 8, "ac": 12, "kind": "pet-crawler", "owner": "Ann", "pet": "Biscuit"}
        s.update(kw)
        p = os.path.join(self.tmp.name, name + ".json")
        with open(p, "w") as f:
            json.dump(s, f)
        return p

    def test_pet_crawler_needs_biscuit_takes_no_slot_and_converts_once(self):
        for n in ("Cy", "Di"):
            self.run_cmd("add-crawler", n, "--player", n, "--class", "Rogue", "--species", "Human")
        self.run_cmd("limits", "set", "max_crawlers", "4")
        self.run_cmd("create-crawler", "--file", self.pet_spec(), expect=1)  # no biscuit
        self.run_cmd("inventory", "add", "Ann", "Enhanced Pet Biscuit", "--qty", "2")
        out, _ = self.run_cmd("create-crawler", "--file", self.pet_spec())
        self.assertIn("pet-crawler of Ann", out)
        self.assertIn("takes no extra slot", out)
        st = self.load()
        ann = st["crawlers"][0]
        self.assertEqual(ann["inventory"][0]["qty"], 1)  # one biscuit consumed
        pet = st["crawlers"][-1]
        self.assertEqual((pet["kind"], pet["owner"], pet["player"], pet["pet_name"]), ("pet-crawler", "Ann", "P", "Biscuit"))
        import state as sm
        self.assertEqual(sm.player_crawler_count(st), 4)
        self.assertEqual(pet["owner_player"], "P")
        out, _ = self.run_cmd("party", "--json")
        party = json.loads(out)
        self.assertEqual((party["encounter_count"], party["party_slots"]), (5, "4/4"))  # the pet-crawler counts in encounters, takes no slot
        self.assertTrue([m for m in party["members"] if m["name"] == "Biscuit"][0]["counts_in_encounters"])
        self.run_cmd("create-crawler", "--file", self.pet_spec("Biscuit2", pet="biscuit"), expect=1)  # one conversion per pet
        self.run_cmd("create-crawler", "--file", self.pet_spec("Rex", pet="Rex"))  # a different pet is fine
        self.run_cmd("create-crawler", "--file", self.pet_spec("Zed", pet="Zed", player="Q"), expect=1)  # not the owner's player

    def test_biscuit_rule_is_one_conversion_per_living_pet_crawler(self):
        """Caleb 2026-10-04: no tombstone. A deleted pet-Crawler frees its conversion, but a new conversion still needs a new biscuit."""
        self.run_cmd("inventory", "add", "Ann", "Enhanced Pet Biscuit", "--qty", "1")
        self.run_cmd("create-crawler", "--file", self.pet_spec())
        self.run_cmd("inventory", "add", "Ann", "Enhanced Pet Biscuit", "--qty", "1")
        _, err = self.run_cmd("create-crawler", "--file", self.pet_spec("Biscuit2", pet="Biscuit"), expect=1)
        self.assertIn("already a living pet-Crawler", err)
        self.run_cmd("crawler", "delete", "Biscuit", "--reason", "test", "--confirm", "Biscuit")
        self.assertEqual(self.crawler("Ann")["inventory"][0]["qty"], 1)  # the biscuit is not restored
        self.run_cmd("create-crawler", "--file", self.pet_spec("Biscuit2", pet="Biscuit"))  # new conversion with the new biscuit
        self.assertEqual(self.crawler("Ann").get("inventory"), [])
        self.run_cmd("crawler", "delete", "Biscuit2", "--reason", "test", "--confirm", "Biscuit2")
        _, err = self.run_cmd("create-crawler", "--file", self.pet_spec("Biscuit3", pet="Biscuit"), expect=1)  # no biscuit left
        self.assertIn("Enhanced Pet Biscuit", err)

    def test_pet_crawler_needs_a_player_owner_and_a_pet_name(self):
        self.run_cmd("inventory", "add", "Ann", "Enhanced Pet Biscuit")
        self.run_cmd("create-crawler", "--file", self.pet_spec(owner="Nobody"), expect=1)
        self.run_cmd("create-crawler", "--file", self.pet_spec(pet=""), expect=1)
        self.run_cmd("create-crawler", "--file", self.pet_spec(biscuit_waiver=None))
        self.assertEqual(self.load()["crawlers"][0]["inventory"], [])

    def test_pet_crawler_waiver_and_own_channel_name(self):
        self.run_cmd("create-crawler", "--file", self.pet_spec(biscuit_waiver="GM ruled: story reward"))
        import publisher
        st = self.load()
        ann, pet = st["crawlers"][0], st["crawlers"][-1]
        self.assertNotEqual(publisher.default_channel_name(ann, None), publisher.default_channel_name(pet, None))
        self.assertEqual(publisher.default_channel_name(pet, None), "p-biscuit-sheet")

    def test_unused_biscuit_is_an_ordinary_sellable_tradable_item(self):
        self.run_cmd("inventory", "add", "Ann", "Enhanced Pet Biscuit")
        self.run_cmd("transfer", "Ann", "Bo", "Enhanced Pet Biscuit", "--reason", "looted")
        self.run_cmd("sell", "Bo", "Enhanced Pet Biscuit", "--price", "100", "--reason", "fence")
        self.assertEqual(self.load()["crawlers"][1]["credits"], 100)

    def test_real_story_box_deck_carries_sale_value(self):
        real = os.path.join(os.path.dirname(TOOLS), "tables", "loot-decks", "f01-any-story-boxes.json")
        if not os.path.exists(real):
            self.skipTest("deck not present")
        with open(real) as f:
            d = json.load(f)
        import loot
        vals = {c["id"]: loot.sale_value_of(c) for c in d["cards"]}
        self.assertEqual(vals.get("f01-any-0056"), 500)
        self.assertEqual(vals.get("f01-any-0060"), 100)
        decks, skipped = loot.load_decks(1, "z06", os.path.dirname(real))
        self.assertTrue(any(x["deck_id"] == "f01-any-story-boxes" for x in decks))


if __name__ == "__main__":
    unittest.main()
