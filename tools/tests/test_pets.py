"""GM-run plain pets (decision 022, rules/60, spec section 9). Discord is never touched."""
import json
import os
import sys
import unittest

from test_state import StateTestCase, TOOLS

sys.path.insert(0, TOOLS)
import publisher as pub  # noqa: E402
import state  # noqa: E402


class PetTests(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Ann", "--player", "P", "--class", "Fighter", "--species", "Human", "--credits", "1000")
        self.run_cmd("add-crawler", "Ann Two", "--player", "P", "--class", "Wizard", "--species", "Elf")
        self.run_cmd("add-crawler", "Bo", "--player", "Q", "--class", "Wizard", "--species", "Human", "--credits", "1000")

    def rows(self, name="pet-log.jsonl"):
        p = os.path.join(self.tmp.name, "sessions", name)
        return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []

    def add(self, owner="Ann", name="Pebbles", species="dog", *extra, expect=0):
        return self.run_cmd("pet", "add", owner, "--name", name, "--species", species, *extra, expect=expect)

    def test_add_show_and_card_line(self):
        out, _ = self.add("Ann", "Pebbles", "rottweiler", "--quote", "my dog Pebbles", "--description", "big, dumb, loyal")
        self.assertIn("Mastiff", self.crawler("Ann")["pet"]["species"])   # rottweiler is a reskinned mastiff
        pet = self.crawler("Ann")["pet"]
        self.assertEqual((pet["status"], pet["cr"], pet["quote"], pet["filed_by"]), ("alive", 0.125, "my dog Pebbles", "gm"))
        self.assertIn("Pebbles", self.run_cmd("pet", "show", "Ann")[0])
        self.run_cmd("validate")
        data = {"pets_enabled": True}
        card = "\n".join(pub.render_card(self.crawler("Ann"), data, []))
        self.assertIn("Pet (GM-run): Pebbles", card)
        self.assertNotIn("big, dumb", card)                                # the GM's notes never reach Discord
        self.assertNotIn("Pet", "\n".join(pub.render_card(self.crawler("Bo"), data, [])))   # no pet, no line
        self.assertNotIn("Pet", "\n".join(pub.render_card(self.crawler("Ann"), {"pets_enabled": False}, [])))

    def test_refusals_one_pet_cr_species_kind(self):
        self.add()
        _, err = self.add("Ann", "Rex", "wolf", expect=1)
        self.assertIn("one pet per Crawler", err)
        _, err = self.add("Bo", "Pebbles", "dog", expect=1)
        self.assertIn("already used", err)
        _, err = self.add("Bo", "Smaug", "Brown Bear", expect=1)
        self.assertIn("--override", err)
        _, err = self.add("Bo", "Big", "wolf", "--cr", "1", expect=1)
        self.assertIn("1/4", err)
        self.add("Bo", "Ursa", "Brown Bear", "--override", "GM: a small bear cub, ruled CR 1/4")     # a GM ruling is allowed and logged
        self.assertEqual(self.rows()[-1]["override"], "GM: a small bear cub, ruled CR 1/4")
        self.add("Ann Two", "Cat", "cat")                               # a benched Crawler may have a pet
        self.assertEqual(self.crawler("Ann Two")["pet"]["name"], "Cat")
        self.run_cmd("validate")

    def test_nit_convert_without_file_is_a_clean_error(self):
        self.add()
        _, err = self.run_cmd("pet", "convert", "Ann", expect=1)
        self.assertIn("pet convert needs --file SPEC.json", err)
        self.assertNotIn("Traceback", err)

    def test_nit_pet_items_move_only_to_or_from_a_living_pet_owner(self):
        KENNEL, GULP = state.PET_SHOP["pet-carrier"][0], state.PET_SHOP["heal-critter-potion"][0]
        self.add("Ann")
        self.run_cmd("pet", "shop", "Ann", "pet-carrier", "--reason", "kennel")
        self.run_cmd("pet", "shop", "Ann", "heal-critter-potion", "--reason", "gulp")
        for argv in (("transfer", "Ann", "Bo", KENNEL, "--reason", "gift"), ("transfer", "Ann", "Bo", GULP, "--reason", "gift")):
            _, err = self.run_cmd(*argv, expect=1)
            self.assertIn("living pet", err)
        _, err = self.run_cmd("transfer", "Ann", "Bo", KENNEL, "--reason", "gift", "--dry-run", expect=1)
        self.assertIn("living pet", err)
        self.add("Bo", "Rex", "wolf")
        self.run_cmd("transfer", "Ann", "Bo", KENNEL, "--reason", "gift")           # the receiver has a living pet
        self.assertTrue(any(i.get("srd_id") == "pet-carrier" for i in self.crawler("Bo")["inventory"]))
        # sell: the seller needs a living pet
        self.run_cmd("pet", "mark-dead", "Bo", "--reason", "x")
        _, err = self.run_cmd("sell", "Bo", KENNEL, "--price", "10", "--reason", "x", expect=1)
        self.assertIn("living pet", err)
        self.run_cmd("sell", "Ann", GULP, "--price", "10", "--reason", "back to the System")
        # ordinary items are untouched by the gate
        self.run_cmd("inventory", "add", "Ann", "Rope", "--qty", "2")
        self.run_cmd("transfer", "Ann", "Bo", "Rope", "--reason", "gift")

    def test_nit_leftover_pet_items_hidden_on_the_card_without_a_living_pet_or_with_pets_off(self):
        self.add("Ann")
        self.run_cmd("pet", "shop", "Ann", "heal-critter-potion", "--reason", "gulp")
        self.run_cmd("inventory", "add", "Ann", "Rope")
        card = lambda data: "\n".join(pub.render_card(self.crawler("Ann"), data, []))
        self.assertIn("Heal Critter Potion", card({"pets_enabled": True}))
        self.assertNotIn("Heal Critter Potion", card({"pets_enabled": False}))
        self.assertIn("Rope", card({"pets_enabled": False}))
        self.run_cmd("pet", "mark-dead", "Ann", "--reason", "x")
        self.assertNotIn("Heal Critter Potion", card({"pets_enabled": True}))
        self.assertIn("heal-critter-potion", json.dumps(self.crawler("Ann")["inventory"]))   # still on file

    def test_nit_shop_checks_pets_off_before_the_benched_owner(self):
        self.add("Ann Two", "Cat", "cat")
        self.run_cmd("limits", "set", "pets_enabled", "false")
        _, err = self.run_cmd("pet", "shop", "Ann Two", "pet-carrier", "--reason", "x", expect=1)
        self.assertIn("pets are off", err)
        self.assertNotIn("benched", err)

    def test_species_table_matches_srd_521_beasts_cr_quarter_or_lower(self):
        d = json.load(open(os.path.join(os.path.dirname(state.__file__), "..", "tables", "pet-species.json")))
        sp = {e["id"]: e for e in d["species"]}
        self.assertEqual(len(sp), 48)
        self.assertEqual(sorted(__import__("collections").Counter(e["cr"] for e in d["species"]).items()), [(0.0, 24), (0.125, 9), (0.25, 15)])
        self.assertEqual(sp["baboon"]["cr"], 0.0)
        for gone in ("axe-beak", "flying-snake", "stirge", "giant-owl", "quipper", "sea-horse", "poisonous-snake", "giant-poisonous-snake"):
            self.assertNotIn(gone, sp)
        for here in ("pteranodon", "piranha", "seahorse", "venomous-snake", "giant-venomous-snake"):
            self.assertIn(here, sp)
        self.assertEqual((sp["venomous-snake"]["cr"], sp["giant-venomous-snake"]["cr"], sp["pteranodon"]["cr"]), (0.125, 0.25, 0.25))
        for target in d["aliases"].values():
            self.assertIn(target, sp)                                   # no alias points at a removed species
        for k, v in (("snake", "venomous-snake"), ("viper", "venomous-snake"), ("quipper", "piranha"), ("sea horse", "seahorse"),
                     ("Poisonous Snake", "venomous-snake"), ("giant poisonous snake", "giant-venomous-snake")):
            self.assertEqual(state._species_lookup(k)[0], v, k)         # old names still resolve
        self.assertEqual(state._species_lookup("Pteranodon")[2], 0.25)

    def test_non_beast_and_swarm_species_need_override(self):
        for i, sp_ in enumerate(("Axe Beak", "Flying Snake", "Stirge", "Giant Owl", "Swarm of Rats", "Giant Fly")):
            _, err = self.add("Ann" if i % 2 == 0 else "Bo", "X%d" % i, sp_, expect=1)
            self.assertIn("--override", err, sp_)

    def test_pet_is_not_a_crawler_and_takes_no_credits_xp_loot_or_trades(self):
        self.add()
        for argv in (("credits", "Pebbles", "+5", "--reason", "x"), ("sell", "Pebbles", "Rope", "--reason", "x"), ("transfer", "Ann", "Pebbles", "Rope", "--reason", "x"),
                     ("loot", "story-box", "1", "any", "--crawler", "Pebbles", "--pick", "f01-any-0056", "--deed", "x")):
            _, err = self.run_cmd(*argv, expect=1)
            self.assertIn("not a Crawler", err) if argv[0] != "loot" else None
        out = json.loads(self.run_cmd("party", "--json")[0])
        self.assertEqual(out["encounter_count"], 2)                    # Ann + Bo: the pet is a GM-run companion, not counted
        self.assertEqual(out["party_slots"], "2/4")
        self.assertEqual([(c["name"], c["owner"], c["party_slot"]) for c in out["companions"]], [("Pebbles", "Ann", False)])
        self.assertNotIn("Pebbles", [m["name"] for m in out["members"]])

    def test_benched_owners_pet_is_not_a_companion_in_play(self):
        self.add("Ann Two", "Cat", "cat")
        self.assertEqual(json.loads(self.run_cmd("party", "--json")[0])["companions"], [])

    def test_mark_dead_is_final_and_a_dead_pet_is_hidden(self):
        self.add()
        _, err = self.run_cmd("pet", "mark-dead", "Ann", expect=1)
        self.assertIn("--reason", err)
        self.run_cmd("pet", "mark-dead", "Ann", "--reason", "fell off the stairs")
        self.assertEqual(self.crawler("Ann")["pet"]["status"], "dead")
        _, err = self.run_cmd("pet", "mark-dead", "Ann", "--reason", "again", expect=1)
        self.assertIn("no living pet", err)
        self.assertNotIn("Pet", "\n".join(pub.render_card(self.crawler("Ann"), {}, [])))
        self.assertEqual(json.loads(self.run_cmd("party", "--json")[0])["companions"], [])
        self.assertEqual([r["event"] for r in self.rows()], ["added", "died"])
        self.run_cmd("use-revive", "Ann", "--dry-run")                   # a Crawler revive has nothing to do with the pet
        self.assertEqual(self.crawler("Ann")["pet"]["status"], "dead")

    def test_remove_is_a_logged_correction(self):
        self.add()
        self.run_cmd("pet", "remove", "Ann", "--reason", "filed on the wrong Crawler")
        self.assertNotIn("pet", self.crawler("Ann"))
        self.assertEqual(self.rows()[-1]["event"], "removed")

    def test_off_switch(self):
        self.add()
        self.run_cmd("limits", "set", "pets_enabled", "false")
        _, err = self.add("Bo", "Rex", "wolf", expect=1)
        self.assertIn("pets are off", err)
        _, err = self.run_cmd("pet", "shop", "Ann", "heal-critter-potion", "--reason", "x", expect=1)
        self.assertIn("pets are off", err)
        _, err = self.run_cmd("pet", "shop", "Ann", expect=1)
        self.assertIn("pets are off", err)                              # the items are not listed anywhere
        self.assertEqual(json.loads(self.run_cmd("party", "--json")[0])["companions"], [])
        self.assertIn("Pebbles", self.run_cmd("pet", "show", "Ann")[0])  # the record stays on file, inert
        self.assertEqual(self.crawler("Ann")["pet"]["status"], "alive")
        self.run_cmd("limits", "set", "pets_enabled", "true")
        self.run_cmd("validate")
        self.assertIn("pets_enabled", self.run_cmd("limits", "show")[0])

    def test_shop_only_for_a_living_pet_owner_priced_by_floor_and_buyback_half(self):
        _, err = self.run_cmd("pet", "shop", "Ann", "heal-critter-potion", "--reason", "x", expect=1)
        self.assertIn("no living pet", err)
        _, err = self.run_cmd("pet", "shop", "Ann", expect=1)
        self.assertIn("not offered", err)
        self.add()
        out = json.loads(self.run_cmd("pet", "shop", "Ann", "--json")[0])
        self.assertEqual({i["id"]: (i["credits"], i["buyback"]) for i in out["items"]}, {"heal-critter-potion": (50, 25), "pet-carrier": (100, 50)})
        self.run_cmd("pet", "shop", "Ann", "heal-critter-potion", "--qty", "2", "--reason", "Good Boy Gulp from the System")
        self.assertEqual(self.crawler("Ann")["credits"], 900)
        inv = [i for i in self.crawler("Ann")["inventory"] if i.get("srd_id") == "heal-critter-potion"]
        self.assertEqual((inv[0]["qty"], inv[0]["off_menu"]), (2, True))
        self.run_cmd("pet", "shop", "Ann", "pet-carrier", "--reason", "kennel", "--floor", "5")   # x5 at floors 5-9
        self.assertEqual(self.crawler("Ann")["credits"], 400)
        self.run_cmd("pet", "shop", "Ann", "heal-critter-potion", "--sell", "--reason", "bought back", "--floor", "5")
        self.assertEqual(self.crawler("Ann")["credits"], 400 + 125)       # half of 250
        led = open(os.path.join(self.tmp.name, "sessions", "credit-ledger.jsonl")).read()
        self.assertIn("Good Boy Gulp", led)
        self.assertIn("ledger OK", self.run_cmd("ledger", "verify")[0])
        _, err = self.run_cmd("pet", "shop", "Ann Two", "pet-carrier", "--reason", "x", expect=1)    # benched: no purchases
        self.assertIn("benched", err)
        _, err = self.run_cmd("pet", "shop", "Bo", "pet-carrier", "--reason", "x", expect=1)         # no pet
        self.assertIn("no living pet", err)
        self.run_cmd("pet", "shop", "Bo", "pet-carrier", "--reason", "GM ruling", "--override", "pet arrives next session")   # GM override is logged
        self.assertEqual(self.rows()[-1]["override"], "pet arrives next session")
        _, err = self.run_cmd("pet", "shop", "Ann", "sword", "--reason", "x", expect=1)
        self.assertIn("pet shop sells only", err)

    def test_heal_uses_a_potion_only_on_a_plain_pet(self):
        self.add()
        _, err = self.run_cmd("pet", "heal", "Ann", "--reason", "x", expect=1)
        self.assertIn("no Good Boy Gulp", err)
        self.run_cmd("pet", "shop", "Ann", "heal-critter-potion", "--reason", "x")
        out, _ = self.run_cmd("pet", "heal", "Ann", "--reason", "after the rat swarm")
        self.assertRegex(out, r"2d4\+2 = \d\+\d\+2 = (\d|1\d) HP")
        self.assertFalse([i for i in self.crawler("Ann")["inventory"] if i.get("srd_id") == "heal-critter-potion"])
        self.assertEqual(self.rows()[-1]["event"], "healed")

    def test_validate_rejects_a_pet_on_a_non_player_or_with_a_bad_cr(self):
        self.add()
        s = self.load()
        s["crawlers"][0]["pet"]["cr"] = 3
        json.dump(s, open(self.path, "w"))
        out, err = self.run_cmd("validate", expect=1)
        self.assertIn("pet.cr", out + err)

    def test_delete_owner_removes_the_plain_pet_with_it_but_not_the_biscuit_pet_crawler(self):
        self.add("Bo", "Rex", "wolf")
        out, _ = self.run_cmd("crawler", "delete", "Bo", "--reason", "housekeeping", "--confirm", "Bo")
        self.assertIn("plain pet Rex", out)
        self.assertNotIn("Rex", json.dumps(self.load()))
        # the archived state copy keeps it
        arch = os.path.join(self.tmp.name, "sessions", "deleted-archive")
        self.assertTrue(any("Rex" in open(os.path.join(arch, f)).read() for f in os.listdir(arch) if f.startswith("bo-state")))
        self.assertEqual(self.rows("delete-log.jsonl")[-1]["plain_pet"]["name"], "Rex")

    def test_convert_makes_a_pet_crawler_and_retires_the_plain_pet(self):
        self.add("Ann", "Pebbles", "dog")
        self.run_cmd("add-crawler", "Zed", "--player", "Z", "--class", "Fighter", "--species", "Human")
        spec = {"name": "Pebbles", "class": "Fighter", "species": "Mastiff", "level": 1, "hp_max": 11, "ac": 12, "abilities": {a: 10 for a in ("str", "dex", "con", "int", "wis", "cha")},
                "player": "P", "biscuit_waiver": "GM: biscuit from the Pet Box (test)", "inventory": []}
        path = os.path.join(self.tmp.name, "spec.json")
        json.dump(spec, open(path, "w"))
        self.run_cmd("pet", "convert", "Ann", "--file", path)
        c = self.crawler("Pebbles")
        self.assertEqual((c["kind"], c["owner"]), ("pet-crawler", "Ann"))
        self.assertEqual(self.crawler("Ann")["pet"]["status"], "became-crawler")
        _, err = self.add("Ann", "Rex", "wolf", expect=1)
        self.assertIn("one pet per Crawler", err)
        _, err = self.run_cmd("pet", "heal", "Ann", "--reason", "x", expect=1)         # Good Boy Gulp no longer works on it
        self.assertIn("no living plain pet", err)
        _, err = self.run_cmd("pet", "convert", "Ann", "--file", path, expect=1)
        self.assertIn("no living plain pet", err)
        self.assertEqual(json.loads(self.run_cmd("party", "--json")[0])["companions"], [])
        self.run_cmd("validate")

    def test_deleted_pet_crawler_no_longer_blocks_a_new_pet_or_conversion(self):
        self.add("Ann", "Pebbles", "dog")
        spec = {"name": "Pebbles", "class": "Fighter", "species": "Mastiff", "level": 1, "hp_max": 11, "ac": 12, "abilities": {a: 10 for a in ("str", "dex", "con", "int", "wis", "cha")},
                "player": "P", "biscuit_waiver": "GM: biscuit from the Pet Box (test)", "inventory": []}
        path = os.path.join(self.tmp.name, "spec.json")
        json.dump(spec, open(path, "w"))
        self.run_cmd("pet", "convert", "Ann", "--file", path)
        _, err = self.add("Ann", "Rex", "wolf", expect=1)                                # alive pet-Crawler: still one pet per Crawler
        self.assertIn("one pet per Crawler", err)
        self.run_cmd("condition", "add", "Pebbles", "Dead")
        _, err = self.add("Ann", "Rex", "wolf", expect=1)                                # dead but on file: still blocks
        self.assertIn("one pet per Crawler", err)
        self.run_cmd("condition", "remove", "Pebbles", "Dead")
        self.run_cmd("crawler", "delete", "Pebbles", "--reason", "GM ruling", "--confirm", "Pebbles")
        _, err = self.run_cmd("pet", "convert", "Ann", "--file", path, expect=1)         # nothing to convert yet; the message says what to do
        self.assertIn("pet add", err)
        self.add("Ann", "Pebbles", "dog")                                              # the old name is free again
        pet = self.crawler("Ann")["pet"]
        self.assertEqual(pet["status"], "alive")
        hist = self.crawler("Ann")["pet_history"]
        self.assertEqual((len(hist), hist[0]["status"], hist[0].get("pet_crawler_deleted")), (1, "became-crawler", True))
        self.run_cmd("validate")
        self.run_cmd("pet", "convert", "Ann", "--file", path)                          # a new Enhanced Pet Biscuit, a new conversion
        self.assertEqual(self.crawler("Pebbles")["kind"], "pet-crawler")
        self.assertEqual(self.crawler("Ann")["pet"]["status"], "became-crawler")
        _, err = self.add("Ann", "Rex", "wolf", expect=1)
        self.assertIn("one pet per Crawler", err)
        self.assertIn("ledger OK", self.run_cmd("ledger", "verify")[0])

    def test_party_json_marks_benched_members_and_keeps_existing_keys(self):
        d = json.loads(self.run_cmd("party", "--json")[0])
        by = {m["name"]: m for m in d["members"]}
        self.assertEqual((by["Ann"]["status"], by["Ann"]["benched"]), ("active", False))
        self.assertEqual((by["Ann Two"]["status"], by["Ann Two"]["benched"], by["Ann Two"]["counts_in_encounters"]), ("benched", True, False))
        self.assertEqual(d["benched_count"], 1)
        for k in ("encounter_count", "encounter_count_living", "party_slots", "companions"):
            self.assertIn(k, d)
        for m in d["members"]:
            for k in ("name", "kind", "player", "owner", "owner_player", "status", "level", "hp", "alive", "counts_in_encounters"):
                self.assertIn(k, m)

    def test_assigned_companion_rule_and_credit_split_untouched(self):
        """Accountant: an Assigned Companion (kind companion) takes no share of credits or loot; a plain pet never touches either."""
        self.run_cmd("credits", "Ann", "+50", "--reason", "loot")
        before = self.crawler("Ann")["credits"]
        self.add()
        self.assertEqual(self.crawler("Ann")["credits"], before)
        self.assertIn("ledger OK", self.run_cmd("ledger", "verify")[0])
        self.assertFalse([r for r in open(os.path.join(self.tmp.name, "sessions", "credit-ledger.jsonl")) if "Pebbles" in r])


if __name__ == "__main__":
    unittest.main()
