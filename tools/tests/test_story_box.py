"""Legendary Story Boxes (rules/40 section 2.8): deed registry, cap, bound, story_value, dry-run, warnings, no credit conversion."""
import copy
import json
import os
import shutil
import unittest

from test_state import StateTestCase, TOOLS

REAL_ANY = os.path.join(os.path.dirname(TOOLS), "tables", "loot-decks", "f01-any-orientation-pit.json")


def card(i, tier="Legendary", **kw):
    c = {"id": f"f01-z06-{i:04d}", "floor": 1, "zone": "z06", "tier": tier, "box_types": ["any"], "pull_type": "weird", "kind": "item",
         "reskin_name": f"Story Thing {i}", "real_5e_name": f"House thing {i}", "source_5e": "HOUSE", "rarity": "Legendary", "attunement": None,
         "category": "Misc", "plain_mechanics": {"text": f"Does story thing {i}.", "uses": None}, "credit_value": 0, "draw_weight": 0, "unique": True,
         "tailor_tags": [], "exclusive_to": None, "grant": None, "ledger": {"type": "item", "text": f"item +1 Legendary Story Box: Story Thing {i}"},
         "box_name": f"Deed {i} Box", "deed": f"Did deed number {i}", "notes": f"Story Box card. trigger_deed: deed {i}. power_note: Uncommon-level option.", "story_value": 40000, "bound": False, "sale_value": 500}
    c.update(kw)
    return c


class StoryBoxTests(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Ann", "--player", "P", "--class", "Fighter", "--species", "Human")
        self.run_cmd("add-crawler", "Bo", "--player", "Q", "--class", "Wizard", "--species", "Human")
        self.decks = os.path.join(self.tmp.name, "tables", "loot-decks")
        os.makedirs(self.decks)
        bronze = card(20, tier="Bronze", rarity="Common", draw_weight=10, unique=False, credit_value=25, story_value=None, bound=None, box_name="X Box")
        bronze.pop("story_value"), bronze.pop("bound")
        self.run_cmd("scene", "safe-room", "on")
        self.cards = [
            card(1), card(2), card(3),
            card(4, notes="Story Box card. trigger_deed: deed 4."),
            card(5, notes="Story Box card. power_note: fine. HOLD (Lore): not allowed on Floors 1-2 until Caleb approves."),
            card(8, plain_mechanics={"text": "", "uses": None}),
            card(10, box_name="Pet Box", deed="Brought a pet into the Crawl"),
            card(11, box_name="Pet Box", deed="Brought a pet into the Crawl", story_value=20000),
            card(12, story_value=None, credit_value=5000, box_name="Legacy Box"),
            card(6, kind="credits", grant={"credits": 500}, credit_value=0),
            card(7, kind="item", grant={"credits": 99}),
            bronze,
        ]
        self.write_deck("f01-z06-test.json", "loot-deck/0.1.2", self.cards)

    def write_deck(self, name, schema, cards, zone="z06"):
        with open(os.path.join(self.decks, name), "w") as f:
            json.dump({"schema": schema, "deck_id": name, "version": "0.1.0", "floor": 1, "zone": zone, "cards": cards}, f)

    def sb(self, cid, crawler="Ann", deed="Carried a goat through the tutorial", *extra, expect=0, open_it=True):
        """Award step; by default also the open step (the scene is a safe room in setUp) so older tests can look at the inventory."""
        extra = list(extra)
        if "--deed-id" not in extra:
            extra += ["--deed-id", "deed-" + cid.replace(",", "-")]
        out = self.run_cmd("loot", "story-box", "1", "z06", "--crawler", crawler, "--pick", cid, "--deed", deed, "--witness", "the GM", *extra, expect=expect)
        if open_it and expect == 0 and "--dry-run" not in extra:
            self.run_cmd("loot", "story-box", "--open", "--crawler", crawler)
        return out

    def rows(self, name):
        p = os.path.join(self.tmp.name, "sessions", name)
        if not os.path.exists(p):
            return []
        with open(p) as f:
            return [json.loads(l) for l in f if l.strip()]

    def open_lines(self):
        with open(os.path.join(self.tmp.name, "sessions", "loot.log")) as f:
            return f.read()

    def awards(self):
        return [r for r in self.rows("story-box-ledger.jsonl") if r.get("event") == "awarded"]

    # --- the basics
    def test_draw_refuses_legendary_and_points_to_story_box(self):
        _, err = self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0001", expect=1)
        self.assertIn("loot story-box", err)
        self.assertEqual(self.load()["crawlers"][0]["inventory"], [])
        self.assertEqual(self.rows("loot-ledger.jsonl"), [])

    def test_random_draws_never_return_legendary(self):
        self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann")
        self.assertEqual({r["tier"] for r in self.rows("loot-ledger.jsonl")}, {"Bronze"})
        _, err = self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Bo", "--box-type", "any", "--pull-type", "weird", "--tier", "Legendary", expect=1)
        self.assertIn("no eligible", err)
        for _ in range(3):  # the Bronze card is already owned by Ann, so nothing else is drawable for her
            _, err = self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", expect=1)
            self.assertIn("no eligible", err)

    def test_deed_text_is_required(self):
        for deed in (None, "", "   ", "pet"):
            args = ["loot", "story-box", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0001", "--deed-id", "goat-in"] + (["--deed", deed] if deed is not None else [])
            _, err = self.run_cmd(*args, expect=1)
            self.assertIn("needs the deed written down", err)
        self.assertEqual(self.load()["crawlers"][0]["inventory"], [])
        self.assertEqual(self.awards(), [])
        self.assertEqual(self.rows("loot-ledger.jsonl"), [])

    def test_award_records_everything(self):
        out, _ = self.sb("f01-z06-0001", "Ann", "Carried a goat through the tutorial", "--gm-note", "first pet in the Crawl", "--when", "S1 20:40")
        self.assertIn("STORY BOX EARNED (unopened)", out)
        self.assertNotIn("BOUND", out)
        c = self.load()["crawlers"][0]
        inv = c["inventory"][0]
        self.assertEqual((inv["name"], inv.get("bound"), inv["story_value"], inv["sale_value"], c["credits"]), ("Story Thing 1", None, 40000, 500, 0))
        reg = self.awards()
        self.assertEqual(len(reg), 1)
        r = reg[0]
        self.assertEqual((r["event"], r["crawler"], r["floor"], r["witness"], r["gm_note"], r["when"], r["story_value"], r["card_id"]),
                         ("awarded", "Ann", 1, "the GM", "first pet in the Crawl", "S1 20:40", 40000, "f01-z06-0001"))
        self.assertNotIn("bound", r)
        self.assertEqual((r["deed"], r["deed_key"]), ("Carried a goat through the tutorial", "deed-f01-z06-0001"))
        loot = self.rows("loot-ledger.jsonl")[0]
        self.assertEqual((loot["economy_value"], loot["story_value"], loot.get("bound"), loot["story_box"], loot["safe_room"]), (0, 40000, None, True, "scene"))
        self.assertEqual(loot["deed"], "Carried a goat through the tutorial")
        with open(os.path.join(self.tmp.name, "exports", "card-data.json")) as f:
            self.assertIn("story thing 1", json.load(f)["items"])
        deeds, _ = self.run_cmd("loot", "deeds")
        self.assertIn("Ann: Deed 1 Box", deeds)
        self.assertIn("witness: the GM", deeds)

    # --- deed registry
    def test_same_deed_cannot_be_awarded_twice(self):
        self.sb("f01-z06-0001")
        st = self.load()
        before = json.dumps(st["crawlers"])
        # same canonical deed on a different card: card 2 has its own deed, so force the same deed id
        _, err = self.sb("f01-z06-0002", "Bo", "Carried a goat again", "--deed-id", "Deed F01 z06 0001!", "--override-cap", "test", expect=1)
        self.assertIn("a deed pays once", err)
        self.assertEqual(json.dumps(self.load()["crawlers"]), before)
        self.assertEqual(len(self.awards()), 1)

    def test_same_card_twice_refused_unique_and_distinct_deed_id_allowed(self):
        self.sb("f01-z06-0001")
        _, err = self.sb("f01-z06-0001", "Bo", "Carried a second goat", "--deed-id", "second-goat", "--override-cap", "test", expect=1)
        self.assertIn("unique", err)
        self.sb("f01-z06-0002", "Bo", "Did the second thing", "--override-cap", "Caleb ruled: two deeds")
        self.assertEqual(len(self.awards()), 2)

    # --- cap
    def test_cap_one_per_floor_with_logged_override(self):
        self.sb("f01-z06-0001")
        _, err = self.sb("f01-z06-0002", "Bo", "Did the second thing", expect=1)
        self.assertIn("Story Box cap reached", err)
        self.assertIn("--override-cap", err)
        self.assertEqual(len(self.awards()), 1)
        self.sb("f01-z06-0002", "Bo", "Did the second thing", "--override-cap", "Caleb ruled: boss reward")
        r = self.awards()[1]
        self.assertEqual(r["override_cap"], "Caleb ruled: boss reward")
        self.assertEqual(self.rows("loot-ledger.jsonl")[1]["override_cap"], "Caleb ruled: boss reward")

    def test_cap_configurable_through_limits(self):
        self.run_cmd("limits", "set", "legendary_cap_per_floor", "2")
        self.sb("f01-z06-0001")
        self.sb("f01-z06-0002", "Bo", "Did the second thing")
        _, err = self.sb("f01-z06-0003", "Ann", "Did the third thing", expect=1)
        self.assertIn("cap reached", err)

    # --- dry run and warnings
    def test_dry_run_writes_nothing_and_shows_plan(self):
        before = self.digest()
        out, _ = self.sb("f01-z06-0001", "Ann", "Carried a goat through the tutorial", "--dry-run")
        self.assertIn("DRY RUN", out)
        self.assertIn("box 1/1 on floor 1", out)
        self.assertEqual(self.digest(), before)
        self.assertEqual(self.awards(), [])
        self.assertEqual(self.rows("loot-ledger.jsonl"), [])
        self.assertFalse(os.path.exists(os.path.join(self.tmp.name, "exports", "card-data.json")))

    def test_dry_run_still_enforces_refusals(self):
        self.sb("f01-z06-0001")
        _, err = self.sb("f01-z06-0002", "Bo", "Did the second thing", "--dry-run", expect=1)
        self.assertIn("cap reached", err)

    def test_missing_power_note_warns_but_awards(self):
        out, _ = self.sb("f01-z06-0004")
        self.assertIn("WARNING: card has no power note (no 'power_note:' in notes)", out)
        self.assertEqual(self.awards()[0]["card_id"], "f01-z06-0004")
        self.assertTrue(any("no power note" in w for w in self.awards()[0]["warnings"]))

    def test_blank_effect_text_warns(self):
        out, _ = self.sb("f01-z06-0008")
        self.assertIn("states no effect", out)

    # --- several cards, one box
    def test_two_cards_one_box_counts_once_against_the_cap(self):
        out, _ = self.sb("f01-z06-0010,f01-z06-0011", "Ann", "Brought a goat into the Crawl", "--deed-id", "goat-in")
        self.assertIn("2 cards, one box", out)
        inv = {i["name"] for i in self.load()["crawlers"][0]["inventory"]}
        self.assertEqual(inv, {"Story Thing 10", "Story Thing 11"})
        loot = self.rows("loot-ledger.jsonl")
        self.assertEqual([e["story_value"] for e in loot], [40000, 20000])
        self.assertEqual({e["box_id"] for e in loot}, {"sb-1-goat-in"})
        self.assertTrue(all("same box" in e["same_box"] for e in loot))
        reg = self.awards()
        self.assertEqual(len(reg), 1)
        self.assertEqual((reg[0]["card_ids"], reg[0]["story_value"]), (["f01-z06-0010", "f01-z06-0011"], 60000))
        self.assertNotIn("override_cap", {k for k, v in reg[0].items() if v})
        out, _ = self.run_cmd("loot", "totals")
        self.assertIn("story 60000", out)
        # the cap is used up by that ONE box
        _, err = self.sb("f01-z06-0001", "Bo", "Did the other thing", expect=1)
        self.assertIn("1 of 1 already awarded", err)

    def test_two_cards_one_box_dry_run_and_custom_reason(self):
        out, _ = self.sb("f01-z06-0010,f01-z06-0011", "Ann", "Brought a goat into the Crawl", "--dry-run", "--deed-id", "goat-in")
        self.assertIn("ONE box", out)
        self.assertEqual(self.awards(), [])
        self.sb("f01-z06-0010,f01-z06-0011", "Ann", "Brought a goat into the Crawl", "--same-box-reason", "second pull of the Pet Box", "--deed-id", "goat-in")
        self.assertEqual(self.rows("loot-ledger.jsonl")[1]["same_box"], "second pull of the Pet Box")

    def test_cards_from_different_deeds_are_separate_boxes(self):
        _, err = self.sb("f01-z06-0001,f01-z06-0002", expect=1)
        self.assertIn("separate Story Boxes", err)
        self.assertEqual(self.rows("loot-ledger.jsonl"), [])

    def test_draw_takes_only_one_pick(self):
        _, err = self.run_cmd("loot", "draw", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0020,f01-z06-0010", expect=1)
        self.assertIn("one card id", err)

    def test_story_value_falls_back_to_credit_value_but_never_spendable(self):
        self.sb("f01-z06-0012")
        e = self.rows("loot-ledger.jsonl")[0]
        self.assertEqual((e["story_value"], e["economy_value"]), (5000, 0))
        self.assertEqual(self.load()["crawlers"][0]["credits"], 0)

    def test_hold_note_is_a_warning_not_a_block(self):
        out, _ = self.sb("f01-z06-0005")
        self.assertIn("WARNING: deck note says: HOLD (Lore)", out)
        self.assertEqual(len(self.load()["crawlers"][0]["inventory"]), 1)

    def test_no_witness_warns(self):
        out, _ = self.run_cmd("loot", "story-box", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0001", "--deed", "Carried a goat through the tutorial", "--deed-id", "goat-in")
        self.assertIn("no --witness or --gm-note", out)

    # --- never convertible
    def test_story_value_never_becomes_credits(self):
        self.sb("f01-z06-0001")
        st = self.load()
        self.assertEqual(st["crawlers"][0]["credits"], 0)
        self.assertEqual(self.rows("credit-ledger.jsonl"), [])
        self.assertEqual(self.rows("loot-ledger.jsonl")[0]["economy_value"], 0)
        self.assertNotIn("credits_granted", self.rows("loot-ledger.jsonl")[0])
        t, _ = self.run_cmd("loot", "totals", "--json")
        slot = json.loads(t)["totals"]["Ann"]["1"]
        self.assertEqual((slot["economy_value"], slot["story_value"]), (0, 40000))

    def test_legendary_cards_that_grant_credits_are_refused(self):
        for cid in ("f01-z06-0006", "f01-z06-0007"):
            _, err = self.sb(cid, expect=1)
            self.assertIn("never convertible", err)
        self.assertEqual(self.load()["crawlers"][0]["credits"], 0)
        self.assertEqual(self.rows("credit-ledger.jsonl"), [])

    def test_story_value_is_never_a_price_in_the_code(self):
        with open(os.path.join(TOOLS, "state.py")) as f:
            src = f.read().lower()
        for word in ("story_value\"] *", "story_value * ", "prov[\"story_value\"] *"):
            self.assertNotIn(word, src)
        with open(os.path.join(TOOLS, "ledgers.py")) as f:
            self.assertNotIn("credit_value", f.read())

    # --- switch, defaults, tier checks
    def test_switch_off_refuses_and_default_is_on(self):
        self.assertTrue(self.load()["limits"]["legendary_enabled"])
        self.run_cmd("limits", "set", "legendary_enabled", "false")
        _, err = self.sb("f01-z06-0001", expect=1)
        self.assertIn("switched off", err)
        self.assertEqual(self.load()["crawlers"][0]["inventory"], [])
        self.run_cmd("limits", "set", "legendary_enabled", "true")
        self.sb("f01-z06-0001")
        _, err = self.run_cmd("limits", "set", "nonsense", "1", expect=1)
        self.assertIn("usage", err)

    def test_story_box_refuses_non_legendary_cards(self):
        _, err = self.sb("f01-z06-0020", expect=1)
        self.assertIn("only awards Legendary", err)

    # --- totals + inflation flag
    def test_totals_split_and_inflation_flag_excludes_story_value(self):
        self.sb("f01-z06-0001")
        out, _ = self.run_cmd("loot", "totals")
        self.assertIn("Ann F1: economy 0 | story 40000 | 1 draw(s) (1 Legendary)", out)
        self.assertIn("TOTAL economy 0", out)
        self.assertNotIn("FLAG", out)
        import loot
        t = loot.totals([{"crawler": "Ann", "floor": 1, "tier": "Silver", "economy_value": 1600, "story_value": 0}])
        self.assertIn("FLAG: Ann F1 economy value 1600", loot.totals_text(t))

    def test_new_session_defaults_story_boxes_on_and_has_deed_registry(self):
        import subprocess
        import sys
        os.makedirs(os.path.join(self.tmp.name, "gm-notes"))
        os.symlink(TOOLS, os.path.join(self.tmp.name, "tools"))
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "new-session.py"), "betatest"], capture_output=True, text=True,
                           env={**os.environ, "DCC_CAMPAIGN_DIR": self.tmp.name})
        self.assertEqual(r.returncode, 0, r.stderr)
        base = os.path.join(self.tmp.name, "sessions-data", "betatest")
        self.assertTrue(self.read_json(os.path.join(base, "state.json"))["limits"]["legendary_enabled"])
        self.assertTrue(os.path.exists(os.path.join(base, "story-box-ledger.jsonl")))

    # --- no BOUND marker any more (Caleb 2026-10-04)
    def test_no_bound_marker_on_card_or_show_and_old_field_not_enforced(self):
        self.sb("f01-z06-0001")
        import publisher
        c = self.load()["crawlers"][0]
        text = "\n".join(publisher.render_card(c, publisher.load_card_data()))
        self.assertNotIn("BOUND", text)
        out, _ = self.run_cmd("show", "Ann")
        self.assertNotIn("BOUND", out)
        # an old row with bound:true still reads, and is still sellable/transferable (the field is not enforced)
        self.set_state(lambda st: st["crawlers"][0]["inventory"][0].update(bound=True))
        self.run_cmd("show", "Ann")
        self.run_cmd("transfer", "Ann", "Bo", "Story Thing 1", "--reason", "looted")
        self.assertEqual([i["name"] for i in self.load()["crawlers"][1]["inventory"]], ["Story Thing 1"])

    # --- rules/45 section 8: deed id, box name, rota, shared deeds, repossess/restore
    def test_deed_id_is_required(self):
        _, err = self.run_cmd("loot", "story-box", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0001", "--deed", "Carried a goat through the tutorial", expect=1)
        self.assertIn("needs --deed-id", err)
        self.assertEqual(self.awards(), [])
        _, err = self.run_cmd("loot", "story-box", "1", "z06", "--crawler", "Ann", "--pick", "f01-z06-0001", "--deed", "Carried a goat through the tutorial", "--deed-id", "!!", expect=1)
        self.assertIn("needs --deed-id", err)

    def test_rewording_the_deed_id_cannot_dodge_the_registry(self):
        self.sb("f01-z06-0001", "Ann", "Carried a goat", "--deed-id", "First Quadruped In")
        _, err = self.sb("f01-z06-0002", "Bo", "Walked a dog in", "--deed-id", "first-quadruped-in!", "--override-cap", "x", expect=1)
        self.assertIn("a deed pays once", err)

    def test_box_name_override_is_recorded(self):
        out, _ = self.sb("f01-z06-0001", "Ann", "Carried a goat", "--box-name", "Four Paws Over the Threshold")
        self.assertIn("Legendary Four Paws Over the Threshold Box", out)
        self.assertEqual(self.awards()[0]["box_name"], "Four Paws Over the Threshold")
        self.assertEqual(self.rows("loot-ledger.jsonl")[0]["box_name"], "Four Paws Over the Threshold")

    def set_state(self, fn):
        st = self.load()
        fn(st)
        with open(self.path, "w") as f:
            json.dump(st, f)

    def test_rota_warns_by_default_and_names_who_waits(self):
        self.run_cmd("limits", "set", "legendary_cap_per_floor", "5")
        self.sb("f01-z06-0001", "Ann", "Carried a goat")
        out, _ = self.sb("f01-z06-0002", "Ann", "Did a second thing")  # warning only: open question 6 is unresolved
        self.assertIn("WARNING: rota: Ann already has a Story Box", out)
        self.assertIn("Bo", out.split("WARNING: rota:")[1].splitlines()[0])
        self.assertEqual(len(self.awards()), 2)
        self.assertEqual(self.awards()[0]["rota_remaining"], ["Bo"])

    def test_rota_stays_warn_only_there_is_no_hard_mode(self):
        self.assertEqual(self.load()["limits"]["story_box_rota"], "warn")
        self.run_cmd("limits", "set", "story_box_rota", "hard", expect=1)
        self.run_cmd("limits", "set", "story_box_rota", "maybe", expect=1)
        self.run_cmd("limits", "set", "legendary_cap_per_floor", "1")
        self.sb("f01-z06-0001", "Ann", "Carried a goat")
        out, _ = self.sb("f01-z06-0002", "Ann", "Did a second thing", "--override-cap", "Caleb: yes")  # the cap override works; the rota only warns
        self.assertIn("WARNING: rota:", out)
        self.assertEqual(len(self.awards()), 2)

    def test_rota_ignores_dead_crawlers_and_pets(self):
        self.run_cmd("limits", "set", "legendary_cap_per_floor", "5")
        self.set_state(lambda st: st["crawlers"][1]["conditions"].append("Dead"))
        self.sb("f01-z06-0001", "Ann", "Carried a goat")
        out, _ = self.sb("f01-z06-0002", "Ann", "Did a second thing")  # Bo is dead: nobody is waiting
        self.assertNotIn("rota:", out)

    def test_shared_deed_puts_every_contributor_on_the_rota(self):
        self.run_cmd("limits", "set", "legendary_cap_per_floor", "5")
        out, _ = self.sb("f01-z06-0001", "Ann", "The table took down the boss together", "--shared-with", "Bo")
        rec = self.awards()[0]
        self.assertEqual((rec["crawler"], rec["shared_with"], rec["rota_remaining"]), ("Ann", ["Bo"], []))
        out, _ = self.sb("f01-z06-0002", "Ann", "Did a second thing")  # everybody has had one: no rota problem
        self.assertNotIn("rota:", out)
        _, err = self.sb("f01-z06-0003", "Ann", "x deed text", "--shared-with", "Nobody", expect=1)
        self.assertIn("no crawler named Nobody", err)
        _, err = self.sb("f01-z06-0003", "Ann", "x deed text", "--shared-with", "Ann", expect=1)
        self.assertIn("holder is --crawler", err)

    def test_missing_trigger_deed_warns(self):
        out, _ = self.sb("f01-z06-0005")
        self.assertIn("no trigger_deed: line", out)

    # --- Lore's any-deck at schema loot-deck/0.1.2
    def any_card(self):
        return card(55, id="f01-any-0055", zone="any", reskin_name="Enhanced Pet Biscuit", box_name="Pet Box", deed="Brought a pet into the Crawl",
                    kind="consumable", category="Consumables", plain_mechanics={"text": "Utilize action: feed it to your willing pet.", "uses": {"max": 1, "recharge": "none"}},
                    tailor_tags=["pets"], notes="Story Box card (spec 2.8): GM-triggered only. trigger_deed: first pet. HOLD (Lore): not allowed on Floors 1-2 by core 4.1 until Caleb approves the narrow Story Box exception.")

    def test_any_deck_0_1_2_hand_pick_with_hold_warning(self):
        self.write_deck("f01-any-test.json", "loot-deck/0.1.2", [self.any_card()], zone="any")
        out, _ = self.run_cmd("loot", "story-box", "1", "z06", "--crawler", "Ann", "--pick", "f01-any-0055", "--deed", "Brought a goat into the Crawl", "--deed-id", "pet-in", "--gm-note", "tutorial")
        self.assertIn("WARNING: deck note says: HOLD (Lore)", out)
        out, _ = self.run_cmd("loot", "story-box", "--open", "--crawler", "Ann")
        self.assertIn("f01-any-0055 | Legendary | consumable | story 40000", self.open_lines())
        inv = self.load()["crawlers"][0]["inventory"][0]
        self.assertEqual((inv["name"], inv.get("bound"), inv["uses"]), ("Enhanced Pet Biscuit", None, 1))
        self.assertEqual(self.awards()[0]["deed_key"], "pet-in")

    def test_any_deck_loads_with_zone_any_too(self):
        self.write_deck("f01-any-test.json", "loot-deck/0.1.2", [self.any_card()], zone="any")
        self.run_cmd("loot", "story-box", "1", "any", "--crawler", "Bo", "--pick", "f01-any-0055", "--deed", "Brought a pet into the Crawl", "--deed-id", "pet-in", "--gm-note", "n", "--dry-run")

    @unittest.skipUnless(os.path.exists(REAL_ANY), "real any-deck not present")
    def test_real_lore_any_deck_pick_in_sandbox(self):
        with open(REAL_ANY) as f:
            deck = json.load(f)
        if not any(c["id"] == "f01-any-0055" for c in deck["cards"]):
            self.skipTest("f01-any-0055 not in deck")
        shutil.copy(REAL_ANY, os.path.join(self.decks, "f01-any-real.json"))
        os.remove(os.path.join(self.decks, "f01-z06-test.json"))
        out, _ = self.run_cmd("loot", "story-box", "1", "z06", "--crawler", "Ann", "--pick", "f01-any-0055", "--deed", "Brought a pet into the Crawl", "--deed-id", "pet-in", "--gm-note", "sandbox", "--witness", "GM")
        self.run_cmd("loot", "story-box", "--open", "--crawler", "Ann")
        self.assertIn("story 40000", self.open_lines())
        self.assertNotIn("BOUND", out)
        if "HOLD" in "".join(c.get("notes", "") for c in deck["cards"] if c["id"] == "f01-any-0055"):
            self.assertIn("WARNING: deck note says: HOLD", out)  # surfaced, not blocking (Lore will remove the line)
        self.assertEqual(self.load()["crawlers"][0]["credits"], 0)
        self.assertEqual(self.rows("loot-ledger.jsonl")[0]["story_value"], 40000)


if __name__ == "__main__":
    unittest.main()
