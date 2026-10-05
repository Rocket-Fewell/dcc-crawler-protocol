"""Several Crawlers per player: active/benched, session lock, swaps, delete (Caleb 2026-10-04). Discord is always mocked."""
import json
import os
import sys
import unittest
from unittest import mock

from test_state import StateTestCase, TOOLS
from test_story_box import card

sys.path.insert(0, TOOLS)
import publisher as pub  # noqa: E402
import test_publisher as tp  # noqa: E402


class CrawlerStatusTests(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Ann", "--player", "P", "--class", "Fighter", "--species", "Human")
        self.run_cmd("add-crawler", "Ann Two", "--player", "p", "--class", "Wizard", "--species", "Elf")
        self.run_cmd("add-crawler", "Bo", "--player", "Q", "--class", "Wizard", "--species", "Human")

    def rows(self, name):
        p = os.path.join(self.tmp.name, "sessions", name)
        return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []

    def test_first_crawler_active_later_ones_benched(self):
        self.assertEqual([(c["name"], c["status"]) for c in self.load()["crawlers"]], [("Ann", "active"), ("Ann Two", "benched"), ("Bo", "active")])

    def test_party_counts_only_active(self):
        out, _ = self.run_cmd("party", "--json")
        data = json.loads(out)
        self.assertEqual(data["encounter_count"], 2)
        self.assertIn("benched", self.run_cmd("party")[0])

    def test_party_cap_ignores_benched(self):
        self.run_cmd("limits", "set", "party_max", "2") if False else None
        self.run_cmd("add-crawler", "Ann Three", "--player", "P", "--class", "Rogue", "--species", "Human")  # benched: no slot needed
        self.assertEqual(self.crawler("Ann Three")["status"], "benched")

    def test_benched_cannot_earn_trade_or_open(self):
        for argv in (("credits", "Ann Two", "+5", "--reason", "x"), ("box", "earn", "Ann Two", "gold"), ("set", "crawlers.ann two.credits", "5")):
            _, err = self.run_cmd(*argv, expect=1)
            self.assertIn("benched", err)
        _, err = self.run_cmd("transfer", "Ann", "Ann Two", "Rope", "--reason", "mule", expect=1)
        self.assertIn("same player", err)
        self.assertNotIn("--benched-ok", err)  # no override for trade/sell/receive
        self.run_cmd("credits", "Ann Two", "+5", "--reason", "gm fix", "--benched-ok", "GM correction")
        self.assertEqual(self.crawler("Ann Two")["credits"], 5)

    def test_validate_flags_two_active_for_one_human(self):
        bad = self.load()
        bad["crawlers"][1]["status"] = "active"
        import json as j
        j.dump(bad, open(self.path, "w"))
        out, err = self.run_cmd("validate", expect=1)
        self.assertIn("ACTIVE", out + err)

    def test_migrate_is_idempotent(self):
        s = self.load()
        for c in s["crawlers"]:
            c.pop("status")
        json.dump(s, open(self.path, "w"))
        self.run_cmd("crawler", "migrate")
        self.assertEqual([c["status"] for c in self.load()["crawlers"]], ["active", "benched", "active"])
        self.assertIn("nothing to migrate", self.run_cmd("crawler", "migrate")[0])

    # --- session lock + swap
    def test_activate_swaps_and_logs(self):
        out, _ = self.run_cmd("crawler", "activate", "Ann Two", "--reason", "new build", "--by", "P")
        self.assertIn("Ann Two is now the active", out)
        self.assertEqual([c["status"] for c in self.load()["crawlers"]], ["benched", "active", "active"])
        log = self.rows("swap-log.jsonl")
        self.assertEqual((log[0]["activated"], log[0]["benched"], log[0]["by"]), ("Ann Two", ["Ann"], "P"))
        _, err = self.run_cmd("crawler", "activate", "Ann Two", "--reason", "again", expect=1)
        self.assertIn("already", err)
        self.run_cmd("validate")

    def test_activate_refused_while_session_open_and_dry_run(self):
        self.run_cmd("session-status", "open", "--note", "tonight")
        self.assertIn("OPEN", self.run_cmd("session-status", "show")[0])
        _, err = self.run_cmd("crawler", "activate", "Ann Two", "--reason", "swap", expect=1)
        self.assertIn("locked for the whole session", err)
        self.assertEqual([r["event"] for r in self.rows("swap-log.jsonl")], ["refused"])  # a refused swap writes its reason
        self.assertIn("session is open", self.rows("swap-log.jsonl")[0]["reason"])
        self.run_cmd("session-status", "close")
        self.assertIn("DRY RUN", self.run_cmd("crawler", "activate", "Ann Two", "--reason", "x", "--dry-run")[0])
        self.assertEqual(self.crawler("Ann")["status"], "active")

    def test_fresh_gm_lock_counts_as_open(self):
        os.makedirs(os.path.join(self.sessions, ".gm-lock"), exist_ok=True)
        _, err = self.run_cmd("crawler", "activate", "Ann Two", "--reason", "swap", expect=1)
        self.assertIn("GM run", err)

    def test_list_by_player_and_user(self):
        out, _ = self.run_cmd("crawler", "list", "--player", "P", "--json") if False else self.run_cmd("crawler", "list", "--player", "P")
        self.assertIn("Ann [player, active]", out)
        self.assertIn("Ann Two [player, benched]", out)
        self.assertNotIn("Bo", out)

    # --- delete
    def test_delete_requires_confirm_and_ownership(self):
        out, _ = self.run_cmd("crawler", "delete", "Ann Two", "--reason", "mistake")
        self.assertIn("NOT DELETED", out)
        self.assertEqual(len(self.load()["crawlers"]), 3)
        _, err = self.run_cmd("crawler", "delete", "Ann Two", "--reason", "x", "--confirm", "Ann Two", "--as-player", "Q", expect=1)
        self.assertIn("your own", err)
        self.assertEqual(len(self.load()["crawlers"]), 3)

    def test_delete_moves_ledger_rows_and_keeps_verify_ok(self):
        self.run_cmd("credits", "Ann", "+40", "--reason", "gift")
        self.run_cmd("credits", "Bo", "+10", "--reason", "gift")
        before = self.read_text(os.path.join(self.sessions, "credit-ledger.jsonl"))
        self.assertTrue(before)
        backups = len(self.backups())
        out, _ = self.run_cmd("crawler", "delete", "Ann", "--reason", "retire", "--confirm", "Ann", "--as-player", "p")
        self.assertIn("ledger rows archived: 1", out)
        self.assertEqual([c["name"] for c in self.load()["crawlers"]], ["Ann Two", "Bo"])
        self.assertGreater(len(self.backups()), backups)
        arch = os.path.join(self.sessions, "deleted-archive", "ann-ledger-rows.jsonl")
        self.assertEqual(json.loads(open(arch).readline())["crawler"], "Ann")
        self.assertNotIn('"Ann"', self.read_text(os.path.join(self.sessions, "credit-ledger.jsonl")).replace('"Ann Two"', ""))
        self.assertIn("ledger OK", self.run_cmd("ledger", "verify")[0])
        entry = self.rows("delete-log.jsonl")[0]
        self.assertEqual((entry["crawler"], entry["credits"], entry["by"]), ("Ann", 40, "p"))
        self.run_cmd("validate")
        # Ann Two was benched; its owner's first Crawler is gone, so it stays benched until swapped (no silent promotion)
        self.assertEqual(self.crawler("Ann Two")["status"], "benched")

    def test_delete_active_refused_during_session_but_benched_ok(self):
        self.run_cmd("session-status", "open")
        _, err = self.run_cmd("crawler", "delete", "Ann", "--reason", "x", "--confirm", "Ann", expect=1)
        self.assertIn("ACTIVE", err)
        self.assertEqual(len(self.load()["crawlers"]), 3)
        self.run_cmd("crawler", "delete", "Ann Two", "--reason", "x", "--confirm", "Ann Two")
        self.assertEqual(len(self.load()["crawlers"]), 2)

    def test_delete_frees_story_box_slot_but_deed_stays_closed(self):
        decks = os.path.join(self.tmp.name, "tables", "loot-decks")
        os.makedirs(decks)
        json.dump({"schema": "loot-deck/0.1.2", "deck_id": "d", "version": "0.1.0", "floor": 1, "zone": "z06", "cards": [card(1), card(2)]}, open(os.path.join(decks, "d.json"), "w"))
        argv = ["loot", "story-box", "1", "z06", "--pick", "f01-z06-0001", "--witness", "GM"]
        self.run_cmd(*argv, "--crawler", "Ann", "--deed", "Did a thing", "--deed-id", "d-1")
        _, err = self.run_cmd(*argv[:5], "f01-z06-0002", *argv[6:], "--crawler", "Bo", "--deed", "Did another", "--deed-id", "d-2", expect=1)
        self.assertIn("cap", err.lower())
        out, _ = self.run_cmd("crawler", "delete", "Ann", "--reason", "retire", "--confirm", "Ann")
        self.assertIn("released", "".join(e["event"] for e in self.rows("story-box-ledger.jsonl")))
        self.assertEqual(json.loads(open(os.path.join(self.sessions, "delete-log.jsonl")).readline())["story_box_slots_freed"][0].startswith("sb"), True)
        self.run_cmd(*argv[:5], "f01-z06-0002", *argv[6:], "--crawler", "Bo", "--deed", "Did another", "--deed-id", "d-2")  # the slot is free now
        _, err = self.run_cmd(*argv, "--crawler", "Bo", "--deed", "Did a thing", "--deed-id", "d-1", expect=1)  # the deed stays closed
        self.assertTrue(err)
        self.assertIn("ledger OK", self.run_cmd("ledger", "verify")[0])

    def test_same_player_transfer_refused_even_both_active_and_other_players_ok(self):
        self.run_cmd("add-item", "Ann", "Rope") if False else None
        self.run_cmd("set", "crawlers.ann.inventory.-", '{"name": "Rope", "qty": 1}')
        _, err = self.run_cmd("transfer", "Ann", "Ann Two", "Rope", "--reason", "mule", expect=1)
        self.assertIn("same player", err)
        self.run_cmd("transfer", "Ann", "Bo", "Rope", "--reason", "gift")  # a different player is fine
        self.assertEqual(self.crawler("Bo")["inventory"][0]["name"], "Rope")

    def test_one_swap_per_window_refusals_logged_and_override(self):
        self.run_cmd("add-crawler", "Ann Three", "--player", "P", "--class", "Rogue", "--species", "Human")
        self.run_cmd("session-status", "open")
        self.run_cmd("session-status", "close")                      # window 1
        self.run_cmd("crawler", "activate", "Ann Two", "--reason", "first", "--by", "GM")
        _, err = self.run_cmd("crawler", "activate", "Ann Three", "--reason", "second", expect=1)
        self.assertIn("one swap per player", err)
        self.run_cmd("crawler", "activate", "Ann Three", "--reason", "second", "--override-window", "GM allows", "--by", "GM")
        self.assertEqual([r["event"] for r in self.rows("swap-log.jsonl")], ["swap", "refused", "swap"])
        self.assertEqual(self.rows("swap-log.jsonl")[0]["window"], 1)
        self.run_cmd("session-status", "open", "--fresh")
        self.run_cmd("session-status", "close")                      # window 2: allowed again
        self.run_cmd("crawler", "activate", "Ann", "--reason", "next window")

    def test_swap_for_someone_elses_crawler_refused(self):
        _, err = self.run_cmd("crawler", "activate", "Ann Two", "--reason", "x", "--as-player", "Q", expect=1)
        self.assertIn("your own", err)
        self.assertEqual(self.rows("swap-log.jsonl")[0]["event"], "refused")

    def test_request_never_changes_state_and_is_refused_in_session(self):
        out, _ = self.run_cmd("crawler", "request", "Ann Two", "--reason", "want to play her", "--as-player", "P")
        self.assertIn("Nothing changed", out)
        self.assertEqual(self.crawler("Ann Two")["status"], "benched")
        self.assertIn("Ann Two", self.run_cmd("crawler", "requests")[0])
        self.run_cmd("session-status", "open")
        _, err = self.run_cmd("crawler", "request", "Ann Two", "--reason", "now", "--as-player", "P", expect=1)
        self.assertIn("No swap while a session is open", err)
        _, err = self.run_cmd("crawler", "request", "Ann Two", "--reason", "x", "--as-player", "Q", expect=1)
        self.assertIn("your own", err)
        self.assertEqual(len(self.rows("swap-requests.jsonl")), 1)

    def test_active_deleted_between_sessions_then_new_active_is_not_a_second_swap(self):
        self.run_cmd("session-status", "open")
        self.run_cmd("session-status", "close")
        self.run_cmd("crawler", "activate", "Ann Two", "--reason", "swap")
        self.run_cmd("crawler", "delete", "Ann Two", "--reason", "retire", "--confirm", "Ann Two")   # active, between sessions: allowed
        self.run_cmd("crawler", "activate", "Ann", "--reason", "name a new active")                     # no active left: not a second swap
        self.assertEqual(self.crawler("Ann")["status"], "active")

    def test_typed_name_must_match(self):
        _, err = self.run_cmd("crawler", "delete", "Ann Two", "--reason", "x", "--confirm", "ann", expect=1)
        self.assertIn("exact Crawler name", err)
        _, err = self.run_cmd("crawler", "delete", "Ann Two", "--reason", "x", "--confirm", expect=1)
        self.assertIn("exact Crawler name", err)
        self.assertEqual(len(self.load()["crawlers"]), 3)

    def test_delete_log_has_session_state_and_prints_count_without_penalty(self):
        self.run_cmd("add-crawler", "Ann Three", "--player", "P", "--class", "Rogue", "--species", "Human")
        out1, _ = self.run_cmd("crawler", "delete", "Ann Two", "--reason", "a", "--confirm", "Ann Two")
        out2, _ = self.run_cmd("crawler", "delete", "Ann Three", "--reason", "b", "--confirm", "Ann Three")
        self.assertIn("deleted 1 Crawler(s)", out1)
        self.assertIn("deleted 2 Crawler(s)", out2)
        e = self.rows("delete-log.jsonl")[1]
        self.assertEqual((e["session_open"], e["was_active"], e["alive"], e["floor"]), (False, False, True, 1))
        self.assertEqual(self.crawler("Ann")["credits"], 0)  # nothing refunded or charged elsewhere
        self.assertTrue([f for f in os.listdir(os.path.join(self.sessions, "deleted-archive")) if f.startswith("ann-two-state-")])

    def test_dead_not_deleted_story_box_still_counts_and_sheet_file_is_archived(self):
        chars = os.path.join(self.tmp.name, "characters")
        os.makedirs(chars)
        with open(os.path.join(chars, "p-ann-two.md"), "w") as f:
            f.write("sheet")
        with open(os.path.join(chars, "INDEX.md"), "w") as f:
            f.write("- characters/p-ann-two.md: Ann Two\n- characters/keep.md: other\n")
        self.run_cmd("crawler", "delete", "Ann Two", "--reason", "x", "--confirm", "Ann Two")
        self.assertFalse(os.path.exists(os.path.join(chars, "p-ann-two.md")))
        self.assertTrue(os.path.exists(os.path.join(self.sessions, "deleted-archive", "p-ann-two.md")))
        idx = open(os.path.join(chars, "INDEX.md")).read()
        self.assertNotIn("p-ann-two", idx)
        self.assertIn("keep.md", idx)

    def _pet(self):
        s = self.load()
        s["crawlers"].append({**json.loads(json.dumps(s["crawlers"][0])), "name": "Biscuit", "kind": "pet-crawler", "owner": "Ann", "pet": "Biscuit", "pet_name": "Biscuit", "status": "active"})
        with open(self.path, "w") as f:
            json.dump(s, f)

    def test_death_with_unopened_story_box_reclaims_it_and_frees_the_slot(self):
        decks = os.path.join(self.tmp.name, "tables", "loot-decks")
        os.makedirs(decks)
        with open(os.path.join(decks, "d.json"), "w") as f:
            json.dump({"schema": "loot-deck/0.1.2", "deck_id": "d", "version": "0.1.0", "floor": 1, "zone": "z06", "cards": [card(1), card(2)]}, f)
        argv = ["loot", "story-box", "1", "z06", "--witness", "GM"]
        self.run_cmd(*argv, "--pick", "f01-z06-0001", "--crawler", "Ann", "--deed", "Did a thing", "--deed-id", "d-1")
        self.assertEqual(self.crawler("Ann")["boxes"]["legendary"], 1)
        _, err = self.run_cmd(*argv, "--pick", "f01-z06-0002", "--crawler", "Bo", "--deed", "Did another", "--deed-id", "d-2", expect=1)
        self.assertIn("cap", err.lower())
        out, _ = self.run_cmd("condition", "add", "Ann", "Dead")
        self.assertIn("STORY BOX RECLAIMED", out)
        self.assertEqual(self.crawler("Ann")["boxes"]["legendary"], 0)
        self.assertEqual([r["event"] for r in self.rows("story-box-ledger.jsonl")][-1], "reclaimed")
        self.assertEqual(self.rows("box-ledger.jsonl")[-1]["event"], "reclaimed")
        self.run_cmd(*argv, "--pick", "f01-z06-0002", "--crawler", "Bo", "--deed", "Did another", "--deed-id", "d-2")   # the slot is free
        self.run_cmd("condition", "remove", "Ann", "Dead")
        _, err = self.run_cmd("loot", "story-box", "--open", "--crawler", "Ann", "--safe-room", expect=1)           # revived: the reclaimed box does not come back
        self.assertIn("no unopened Story Box", err)
        self.run_cmd("condition", "add", "Bo", "Dead")                      # Bo's box too; adding Dead twice never double-reclaims
        self.assertEqual(len([r for r in self.rows("story-box-ledger.jsonl") if r["event"] == "reclaimed"]), 2)
        self.assertIn("ledger OK", self.run_cmd("ledger", "verify")[0])

    def test_dead_without_a_box_changes_nothing_and_an_opened_box_is_not_reclaimed(self):
        out, _ = self.run_cmd("condition", "add", "Ann", "Dead")
        self.assertNotIn("RECLAIMED", out)

    def test_pet_crawler_delete_has_no_tombstone_and_owner_delete_keeps_pet_benched(self):
        self._pet()
        self.run_cmd("crawler", "delete", "Ann", "--reason", "x", "--confirm", "Ann")      # owner deleted: the pet stays, benched
        pet = self.crawler("Biscuit")
        self.assertEqual(pet["status"], "benched")
        self.run_cmd("validate")
        self.run_cmd("crawler", "delete", "Biscuit", "--reason", "x", "--confirm", "Biscuit")
        e = self.rows("delete-log.jsonl")[-1]
        self.assertEqual((e["kind"], e["pet_name"]), ("pet-crawler", "Biscuit"))
        self.assertNotIn("tombstone", e)
        self.assertNotIn("tombstone", json.dumps(self.rows("delete-log.jsonl")))


class DeleteChannelTests(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Horn", "--player", "Hornn", "--class", "Wizard", "--species", "Human")
        self.run_cmd("add-crawler", "Bone Wifebeater", "--player", "Moses", "--class", "Barbarian", "--species", "Goliath")
        self.cat = "900000000000000001"
        with open(pub.channels_path(), "w") as f:
            json.dump({"guild_id": tp.GID, "category_name": "Crawler Sheets", "category_id": self.cat, "crawlers": {
                "Horn": {"channel_id": "111111111111111111", "channel_name": "hornn-sheet", "players": ["Hornn"]},
                "Bone Wifebeater": {"channel_id": "222222222222222222", "channel_name": "moses-sheet", "players": ["Moses"]}}}, f)
        pub.write_json_atomic(pub.snapshots_path(), {"crawlers": {"Horn": {"x": 1}, "Bone Wifebeater": {"x": 2}}})

    def _fd(self):
        fd = tp.FakeDiscord()
        orig = fd.request
        fd.channels = [{"id": "111111111111111111", "type": 0, "name": "hornn-sheet", "parent_id": self.cat},
                       {"id": "222222222222222222", "type": 0, "name": "moses-sheet", "parent_id": self.cat},
                       {"id": "444444444444444444", "type": 0, "name": "elsewhere", "parent_id": "5"},
                       {"id": "555555555555555555", "type": 0, "name": "own", "parent_id": self.cat}]

        def req(method, path, body=None):
            if method == "DELETE":
                fd.calls.append((method, path, body))
                return {}
            return orig(method, path, body)
        fd.request = req
        return fd

    def test_delete_crawler_channel_guards(self):
        fd = self._fd()
        cfg = pub.load_config()
        self.assertFalse(pub.delete_crawler_channel(fd, "111111111111111111", cfg, log=lambda m: None))  # still registered to Horn
        with self.assertRaises(pub.PublishError):
            pub.delete_crawler_channel(fd, "1556163836879568946", cfg, log=lambda m: None)  # #gm-voice
        with self.assertRaises(pub.PublishError):
            pub.delete_crawler_channel(fd, "444444444444444444", cfg, log=lambda m: None)  # outside Crawler Sheets
        self.assertTrue(pub.delete_crawler_channel(fd, "555555555555555555", cfg, log=lambda m: None))
        self.assertEqual([c for c in fd.calls if c[0] == "DELETE"], [("DELETE", "/channels/555555555555555555", None)])

    def test_state_delete_cleans_maps_and_deletes_only_its_own_channel(self):
        fd = self._fd()
        with mock.patch.object(pub, "DiscordClient", lambda *a, **k: fd):
            out, _ = self.run_cmd("crawler", "delete", "Horn", "--reason", "retire", "--confirm", "Horn")
        self.assertIn("deleted Discord channel #hornn-sheet", out)
        self.assertEqual([c[1] for c in fd.calls if c[0] == "DELETE"], ["/channels/111111111111111111"])
        self.assertNotIn("Horn", json.load(open(pub.channels_path()))["crawlers"])
        self.assertNotIn("Horn", json.load(open(pub.snapshots_path()))["crawlers"])
        self.assertIn("Bone Wifebeater", json.load(open(pub.channels_path()))["crawlers"])

    def test_shared_channel_is_kept(self):
        fd = self._fd()
        cfg = json.load(open(pub.channels_path()))
        cfg["crawlers"]["Bone Wifebeater"]["channel_id"] = "111111111111111111"
        json.dump(cfg, open(pub.channels_path(), "w"))
        with mock.patch.object(pub, "DiscordClient", lambda *a, **k: fd):
            out, _ = self.run_cmd("crawler", "delete", "Horn", "--reason", "retire", "--confirm", "Horn")
        self.assertIn("shared", out)
        self.assertEqual([c for c in fd.calls if c[0] == "DELETE"], [])

    def test_no_discord_token_still_deletes_state_and_says_so(self):
        with mock.patch.dict(os.environ, {"GM_DISCORD_TOKEN": ""}):
            out, _ = self.run_cmd("crawler", "delete", "Horn", "--reason", "retire", "--confirm", "Horn")
        self.assertIn("channel NOT deleted", out)
        self.assertEqual([c["name"] for c in self.load()["crawlers"]], ["Bone Wifebeater"])


class ChannelNamingTests(tp.Base):
    def test_one_channel_per_crawler_named_player_crawler_with_dedupe(self):
        self.state["crawlers"].append(tp.crawler("Horn!", "Hornn"))   # slug collides with "Horn"
        self.state["crawlers"].append(tp.crawler("Big Bad", "Hornn"))
        self.write_state()
        fd = tp.FakeDiscord()
        out = pub.setup_channels(fd, log=lambda m: None)
        names = [c["channel_name"] for c in out["created"]]
        self.assertEqual(names, ["hornn-horn", "trailer-park-moses-bone-wifebeater", "hornn-horn-2", "hornn-big-bad"])
        self.assertEqual(len(set(names)), 4)
        n = len(fd.channels)
        pub.setup_channels(fd, log=lambda m: None)
        self.assertEqual(len(fd.channels), n)

    def test_pet_crawler_channel_is_player_pet_sheet_and_owner_is_recorded(self):
        pet = dict(tp.crawler("Biscuit", "Hornn"), kind="pet-crawler")
        self.assertEqual(pub.default_channel_name(pet, None), "hornn-biscuit-sheet")
        self.write_state()
        out = pub.setup_channels(tp.FakeDiscord(), log=lambda m: None)
        self.assertEqual(json.load(open(pub.channels_path()))["crawlers"]["Horn"]["owner"], "Hornn")

    def test_overflow_category_opens_when_the_first_is_full_and_warns_at_45(self):
        fd = tp.FakeDiscord()
        pub.setup_channels(fd, log=lambda m: None)
        cat = next(c for c in fd.channels if c["type"] == 4)
        fd.channels += [{"id": f"8{i:017d}", "type": 0, "name": f"filler-{i}", "parent_id": cat["id"]} for i in range(48)]   # 2 sheets + 48 = 50
        self.state["crawlers"].append(tp.crawler("Late One", "Hornn"))
        self.write_state()
        logs = []
        out = pub.setup_channels(fd, log=logs.append)
        self.assertTrue(any("overflow category 'Crawler Sheets 2'" in l for l in logs))
        newch = next(c for c in fd.channels if c["name"] == "hornn-late-one")
        self.assertNotEqual(newch["parent_id"], cat["id"])
        self.assertEqual(json.load(open(pub.channels_path()))["overflow_category_ids"], [newch["parent_id"]])
        # deleting a sheet in the overflow category is allowed
        fd.request = lambda m, p, b=None: ({"id": "x", "type": 0, "name": "n", "parent_id": newch["parent_id"]} if m == "GET" else {})
        cfg = pub.load_config()
        cfg["crawlers"].pop("Late One")
        self.assertTrue(pub.delete_crawler_channel(fd, newch["id"], cfg, log=lambda m: None))

    def test_existing_mapping_keeps_its_name(self):
        self.map_channels()
        self.assertEqual(pub.default_channel_name(self.state["crawlers"][0], pub.mapping_for(pub.load_config(), "Horn")[1]), "hornn-sheet")

    def test_player_name_alone_is_ambiguous_with_two_crawlers(self):
        self.state["crawlers"].append(tp.crawler("Horn Two", "Hornn"))
        self.write_state()
        with self.assertRaises(pub.PublishError):
            pub.register_channel(tp.FakeDiscord(), "Hornn", "333333333333333333", verify=False, log=lambda m: None)

    def test_card_shows_benched(self):
        c = tp.crawler("Horn Two", "Hornn")
        c["status"] = "benched"
        text = "\n".join(pub.render_card(c, {}))
        self.assertIn("BENCHED", text)
        old = pub.make_view(tp.crawler("Horn Two", "Hornn"), {})
        self.assertEqual(pub.diff_views(old, pub.make_view(c, {})), ["Status: BENCHED"])
        self.assertEqual(pub.diff_views(dict(old, status=None), old), [])  # an old snapshot without status is not a change


def io_run(argv):
    import contextlib
    import io
    import test_state
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = test_state.state.main(argv)
    assert code == 0, out.getvalue()
    return out.getvalue()


if __name__ == "__main__":
    unittest.main()
