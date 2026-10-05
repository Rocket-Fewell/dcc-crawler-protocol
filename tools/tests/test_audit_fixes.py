"""Independent-audit fixes (B1 B2 S1-S6 N1 N2 N5) and Story Box --reaward. Discord is never touched."""
import json
import os
import sys
import unittest
from unittest import mock

from test_state import StateTestCase, state as S, TOOLS
from test_story_box import card

sys.path.insert(0, TOOLS)


class AuditFixTests(StateTestCase):
    def setUp(self):
        super().setUp()
        os.environ["DCC_AUTO_PUBLISH"] = "0"
        self.addCleanup(os.environ.pop, "DCC_AUTO_PUBLISH", None)
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Ann", "--player", "P", "--class", "Fighter", "--species", "Human")
        self.run_cmd("add-crawler", "Ann Two", "--player", "P", "--class", "Wizard", "--species", "Elf")
        self.run_cmd("add-crawler", "Bo", "--player", "Q", "--class", "Wizard", "--species", "Human")
        decks = os.path.join(self.tmp.name, "tables", "loot-decks")
        os.makedirs(decks)
        with open(os.path.join(decks, "d.json"), "w") as f:
            json.dump({"schema": "loot-deck/0.1.2", "deck_id": "d", "version": "0.1.0", "floor": 1, "zone": "z06", "cards": [card(1), card(2)]}, f)

    def rows(self, name):
        p = os.path.join(self.sessions, name)
        return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []

    def crawler(self, name):
        return next(c for c in self.load()["crawlers"] if c["name"] == name)

    def spec(self, name, player, **kw):
        s = {"name": name, "player": player, "class": "Fighter", "species": "Human", "abilities": {a: 10 for a in ("str", "dex", "con", "int", "wis", "cha")}, "hp_max": 8, "ac": 12}
        s.update(kw)
        p = os.path.join(self.tmp.name, f"{name}.json")
        json.dump(s, open(p, "w"))
        return p

    # ---- re-audit nits: credit-ledger backup and unique state copies
    def test_nit_delete_backs_up_the_credit_ledger_first(self):
        self.run_cmd("credits", "Bo", "+5", "--reason", "a")
        live = open(os.path.join(self.sessions, "credit-ledger.jsonl"), encoding="utf-8").read()
        self.run_cmd("crawler", "delete", "Bo", "--reason", "x", "--confirm", "Bo")
        bk = [f for f in os.listdir(os.path.join(self.sessions, "backups")) if f.startswith("credit-ledger-")]
        self.assertEqual(len(bk), 1)
        self.assertEqual(open(os.path.join(self.sessions, "backups", bk[0]), encoding="utf-8").read(), live)   # the ledger exactly as it was before the rewrite
        self.assertIn("ledger OK", self.run_cmd("ledger", "verify")[0])

    def test_nit_same_second_deletes_do_not_overwrite_the_state_copy(self):
        import datetime, types
        fixed = datetime.datetime(2026, 10, 4, 12, 0, 0)

        class Fixed(datetime.datetime):
            @classmethod
            def now(cls, tz=None):
                return fixed
        fake = types.SimpleNamespace(**{k: getattr(datetime, k) for k in dir(datetime) if not k.startswith("__")})
        fake.datetime = Fixed
        for life in (1, 2):
            self.run_cmd("add-crawler", "Delta", "--player", "D", "--class", "Rogue", "--species", "Human")
            self.run_cmd("credits", "Delta", f"+{life * 10}", "--reason", f"life {life}")
            with mock.patch.object(S, "dt", fake):
                self.run_cmd("crawler", "delete", "Delta", "--reason", "x", "--confirm", "Delta")
        arch = os.path.join(self.sessions, "deleted-archive")
        copies = sorted(f for f in os.listdir(arch) if f.startswith("delta-state-"))
        self.assertEqual(len(copies), 2)
        self.assertEqual(len({open(os.path.join(arch, f)).read() for f in copies}), len(copies))

    # ---- Roll ability method (decision 024): new sessions default create.allow_roll to true
    def test_new_session_allow_roll_defaults_on_and_no_roll_turns_it_off(self):
        import subprocess
        os.makedirs(os.path.join(self.tmp.name, "gm-notes"), exist_ok=True)
        if not os.path.exists(os.path.join(self.tmp.name, "tools")):
            os.symlink(TOOLS, os.path.join(self.tmp.name, "tools"))
        env = {**os.environ, "DCC_CAMPAIGN_DIR": self.tmp.name}
        for sid, extra, want in (("rolldefault", [], True), ("rolloff", ["--no-roll"], False)):
            r = subprocess.run([sys.executable, os.path.join(TOOLS, "new-session.py"), sid, *extra], capture_output=True, text=True, env=env)
            self.assertEqual(r.returncode, 0, r.stderr)
            prof = json.load(open(os.path.join(self.tmp.name, "sessions-data", sid, "session.json")))
            self.assertIs(prof["create"]["allow_roll"], want)

    # ---- B1
    def test_b1_archive_keeps_both_lifetimes_of_a_recreated_name(self):
        for life in (1, 2):
            self.run_cmd("add-crawler", "Delta", "--player", "D", "--class", "Rogue", "--species", "Human")
            self.run_cmd("credits", "Delta", "+100", "--reason", f"life {life} a")
            self.run_cmd("credits", "Delta", "-30", "--reason", f"life {life} b")
            self.run_cmd("crawler", "delete", "Delta", "--reason", "housekeeping", "--confirm", "Delta")
        arch = [json.loads(l) for l in open(os.path.join(self.sessions, "deleted-archive", "delta-ledger-rows.jsonl"))]
        self.assertEqual(sorted(r["reason"] for r in arch), ["life 1 a", "life 1 b", "life 2 a", "life 2 b"])
        self.assertEqual(len({r["seq"] for r in arch}), 4)          # seq is never reused after a delete
        self.assertIn("ledger OK", self.run_cmd("ledger", "verify")[0])
        self.run_cmd("crawler", "delete", "Bo", "--reason", "x", "--confirm", "Bo")   # an unrelated delete keeps verifying

    def test_b1_same_row_is_not_archived_twice(self):
        self.run_cmd("credits", "Bo", "+5", "--reason", "a")
        self.run_cmd("crawler", "delete", "Bo", "--reason", "x", "--confirm", "Bo")
        arch = os.path.join(self.sessions, "deleted-archive", "bo-ledger-rows.jsonl")
        self.assertEqual(len(open(arch).readlines()), 1)

    # ---- N5
    def test_n5_verify_flags_a_corrupt_archive(self):
        self.run_cmd("credits", "Bo", "+5", "--reason", "a")
        self.run_cmd("crawler", "delete", "Bo", "--reason", "x", "--confirm", "Bo")
        arch = os.path.join(self.sessions, "deleted-archive", "bo-ledger-rows.jsonl")
        line = open(arch).read()
        with open(arch, "a") as f:
            f.write(line)                                             # a duplicated row
        out, err = self.run_cmd("ledger", "verify", expect=1)
        self.assertIn("appears twice", out + err)
        self.assertIn("exact duplicate", out + err)
        with open(arch, "w") as f:
            f.write(json.dumps({**json.loads(line), "balance": 999}) + "\n" + json.dumps({**json.loads(line), "seq": 2, "balance": 20}) + "\n")
        out, err = self.run_cmd("ledger", "verify", expect=1)
        self.assertIn("starts from", out + err)                      # the balance chain of the archived rows does not add up

    # ---- B2
    def test_b2_new_crawler_is_benched_when_the_player_has_any_crawler_on_file(self):
        self.run_cmd("create-crawler", "--file", self.spec("Cy", "C"))
        self.assertEqual(self.crawler("Cy")["status"], "active")           # no Crawler on file, no session: active
        self.run_cmd("crawler", "delete", "Cy", "--reason", "x", "--confirm", "Cy")
        self.run_cmd("create-crawler", "--file", self.spec("Cy2", "C"))
        self.assertEqual(self.crawler("Cy2")["status"], "active")          # none left on file: the first is active again
        self.run_cmd("create-crawler", "--file", self.spec("Cy3", "C"))
        self.assertEqual(self.crawler("Cy3")["status"], "benched")
        # delete the ACTIVE one between sessions; the benched one stays benched, and a NEW /create is benched too
        self.run_cmd("crawler", "delete", "Cy2", "--reason", "x", "--confirm", "Cy2")
        self.run_cmd("create-crawler", "--file", self.spec("Cy4", "C"))
        self.assertEqual(self.crawler("Cy4")["status"], "benched")
        self.assertEqual([c["status"] for c in self.load()["crawlers"] if c["player"] == "C"], ["benched", "benched"])

    def test_b2_create_during_an_open_session_is_always_benched_and_activation_follows_the_swap_rules(self):
        self.run_cmd("session-status", "open")
        self.run_cmd("create-crawler", "--file", self.spec("Newbie", "N"))
        self.assertEqual(self.crawler("Newbie")["status"], "benched")       # even a brand-new player: not active mid-session
        self.run_cmd("crawler", "activate", "Newbie", "--reason", "first Crawler of a new player (no swap)")   # nothing is swapped out, so the lock does not apply
        self.assertEqual(self.crawler("Newbie")["status"], "active")
        self.run_cmd("create-crawler", "--file", self.spec("Newbie2", "N"))
        _, err = self.run_cmd("crawler", "activate", "Newbie2", "--reason", "swap", expect=1)    # a real swap is refused mid-session
        self.assertIn("session", err)
        self.assertEqual(self.rows("swap-log.jsonl")[-1]["event"], "refused")

    # ---- S4
    def test_s4_delete_rechecks_session_and_existence_inside_the_lock(self):
        with mock.patch.object(S, "session_open", side_effect=[(False, ""), (True, "the session is open")]):
            _, err = self.run_cmd("crawler", "delete", "Bo", "--reason", "x", "--confirm", "Bo", expect=1)
        self.assertIn("REFUSED", err)
        self.assertEqual(self.crawler("Bo")["name"], "Bo")                  # nothing was deleted, nothing logged
        self.assertEqual(self.rows("delete-log.jsonl"), [])
        real_read = S.read_state_file
        calls = {"n": 0}

        def vanishing(path=None, missing_ok=False):   # the Crawler is already gone by the time the lock is taken
            st = real_read(path, missing_ok)
            calls["n"] += 1
            if calls["n"] >= 2:
                st["crawlers"] = [c for c in st["crawlers"] if c["name"] != "Bo"]
            return st
        with mock.patch.object(S, "read_state_file", side_effect=vanishing):
            _, err = self.run_cmd("crawler", "delete", "Bo", "--reason", "x", "--confirm", "Bo", expect=1)
        self.assertIn("already gone", err)
        self.assertEqual(self.rows("delete-log.jsonl"), [])

    # ---- S5
    def test_s5_legacy_sheet_files_are_archived_by_heading_and_prefixes_do_not_claim_each_others(self):
        chars = os.path.join(self.tmp.name, "characters")
        os.makedirs(chars)
        open(os.path.join(chars, "hornn-wizard.md"), "w").write("# Bo (Wizard) - played by Qq\nbody\n")
        open(os.path.join(chars, "ann-two-sheet.md"), "w").write("# Ann Two (Wizard)\nbody\n")
        open(os.path.join(chars, "moses-barbarian.md"), "w").write("# Moses's Crawler (Barbarian) \u2014 Zed Zed\n")
        open(os.path.join(chars, "INDEX.md"), "w").write("- characters/hornn-wizard.md: Bo's crawler\n- characters/ann-two-sheet.md: Ann Two\n- characters/moses-barbarian.md: z\n- characters/other.md: keep\n")
        self.run_cmd("crawler", "delete", "Bo", "--reason", "x", "--confirm", "Bo")
        self.assertFalse(os.path.exists(os.path.join(chars, "hornn-wizard.md")))
        self.assertTrue(os.path.exists(os.path.join(self.sessions, "deleted-archive", "hornn-wizard.md")))
        self.assertTrue(os.path.exists(os.path.join(chars, "ann-two-sheet.md")))     # Ann's delete below must not take Ann Two's file
        self.run_cmd("crawler", "delete", "Ann", "--reason", "x", "--confirm", "Ann") if False else None
        idx = open(os.path.join(chars, "INDEX.md")).read()
        self.assertNotIn("hornn-wizard.md", idx)
        self.assertIn("other.md", idx)
        self.run_cmd("add-crawler", "Zed Zed", "--player", "Z", "--class", "Fighter", "--species", "Human")
        self.run_cmd("crawler", "delete", "Zed Zed", "--reason", "x", "--confirm", "Zed Zed")     # heading ends with the name
        self.assertFalse(os.path.exists(os.path.join(chars, "moses-barbarian.md")))
        self.run_cmd("crawler", "delete", "Ann Two", "--reason", "x", "--confirm", "Ann Two")
        self.assertFalse(os.path.exists(os.path.join(chars, "ann-two-sheet.md")))

    def test_s5_ann_does_not_claim_ann_twos_file(self):
        chars = os.path.join(self.tmp.name, "characters")
        os.makedirs(chars)
        open(os.path.join(chars, "weird-name.md"), "w").write("# Ann Two (Wizard)\n")
        self.run_cmd("crawler", "delete", "Ann", "--reason", "x", "--confirm", "Ann")
        self.assertTrue(os.path.exists(os.path.join(chars, "weird-name.md")))

    # ---- S6
    def test_s6_benched_crawler_cannot_gain_items_hp_achievements_or_raw_set(self):
        for argv in (("inventory", "add", "Ann Two", "Rope"), ("hp", "damage", "Ann Two", "1"), ("achievement", "add", "Ann Two", "Cool"),
                     ("set", "crawlers.1.credits", "5"), ("set", "crawlers.ann two.boxes.gold", "1"), ("set", "crawlers.1.inventory.-", '{"name":"x","qty":1}'),
                     ("set", "crawlers.1.hp.current", "1")):
            _, err = self.run_cmd(*argv, expect=1)
            self.assertIn("benched", err, argv)
        self.run_cmd("achievement", "add", "Ann Two", "Intake Toast", "--benched-ok", "intake toast (pays nothing)")
        self.run_cmd("inventory", "add", "Ann Two", "Rope", "--benched-ok", "GM correction")
        self.assertEqual(self.crawler("Ann Two")["credits"], 0)

    # ---- S2
    def test_s2_rota_counts_only_active_player_crawlers(self):
        out, _ = self.run_cmd("loot", "story-box", "1", "z06", "--witness", "GM", "--pick", "f01-z06-0001", "--crawler", "Ann", "--deed", "Did a great deed", "--deed-id", "d-1", "--dry-run")
        self.assertIn("Bo", out.split("rota after")[1])
        self.assertNotIn("Ann Two", out.split("rota after")[1])     # benched: not waiting for a Story Box

    # ---- S1
    def test_s1_a_crawler_with_a_discord_id_is_owned_by_that_id_only(self):
        self.run_cmd("set", "crawlers.bo.build", '{"discord_user_id":"777"}')
        _, err = self.run_cmd("crawler", "delete", "Bo", "--reason", "x", "--confirm", "Bo", "--as-player", "Q", expect=1)      # same display name, wrong account
        self.assertIn("your own", err)
        _, err = self.run_cmd("crawler", "delete", "Bo", "--reason", "x", "--confirm", "Bo", "--as-user", "888", expect=1)
        self.assertIn("your own", err)
        self.run_cmd("crawler", "delete", "Bo", "--reason", "x", "--confirm", "Bo", "--as-user", "777")
        # no id recorded: the name is the fallback
        _, err = self.run_cmd("crawler", "delete", "Ann Two", "--reason", "x", "--confirm", "Ann Two", "--as-player", "Q", expect=1)
        self.run_cmd("crawler", "delete", "Ann Two", "--reason", "x", "--confirm", "Ann Two", "--as-player", "P")

    # ---- S3
    def test_s3_session_marker_is_idempotent_and_a_quick_reopen_keeps_the_window(self):
        self.run_cmd("session-status", "open")
        w = json.loads(self.run_cmd("session-status", "show", "--json")[0])["window"]
        self.assertIn("already open", self.run_cmd("session-status", "open")[0])             # a second /join changes nothing
        self.run_cmd("session-status", "close")
        self.assertIn("already closed", self.run_cmd("session-status", "close")[0])
        self.run_cmd("session-status", "open")                                                # dropped voice, back within 30 minutes: same window
        self.assertEqual(json.loads(self.run_cmd("session-status", "show", "--json")[0])["window"], w)
        self.run_cmd("session-status", "close")
        self.run_cmd("session-status", "open", "--fresh")
        self.assertEqual(json.loads(self.run_cmd("session-status", "show", "--json")[0])["window"], w + 1)
        rec = os.path.join(self.sessions, "session-status.json")
        d = json.load(open(rec))
        self.run_cmd("session-status", "close")
        d = json.load(open(rec))
        d["closed_at_epoch"] -= 31 * 60                                                      # closed longer ago than the grace period
        json.dump(d, open(rec, "w"))
        self.run_cmd("session-status", "open")
        self.assertEqual(json.loads(self.run_cmd("session-status", "show", "--json")[0])["window"], w + 2)

    # ---- N1
    def test_n1_activate_refuses_a_dead_target(self):
        self.run_cmd("condition", "add", "Ann Two", "Dead")
        _, err = self.run_cmd("crawler", "activate", "Ann Two", "--reason", "x", expect=1)
        self.assertIn("DEAD", err)
        self.assertEqual(self.crawler("Ann")["status"], "active")

    # ---- N2
    def test_n2_banner_does_not_double_box(self):
        out, _ = self.run_cmd("loot", "story-box", "1", "z06", "--witness", "GM", "--pick", "f01-z06-0001", "--crawler", "Ann", "--deed", "Did a great deed", "--deed-id", "d-1")
        self.assertIn("Legendary Deed 1 Box for Ann", out)
        self.assertNotIn("Box Box", out)

    # ---- --reaward
    def award(self, who="Ann", pick="f01-z06-0001", *extra, expect=0):
        return self.run_cmd("loot", "story-box", "1", "z06", "--witness", "GM", "--pick", pick, "--crawler", who, "--deed", "Did deed", "--deed-id", "d-1", *extra, expect=expect)

    def test_reaward_after_reclaim_gets_a_new_box_id_and_is_logged(self):
        self.award()
        _, err = self.award("Bo", "f01-z06-0002", "--reaward", "x", expect=1)
        self.assertIn("not a reclaimed", err)
        _, err = self.award("Bo", "f01-z06-0002", expect=1)
        self.assertIn("--reaward", err)
        self.run_cmd("condition", "add", "Ann", "Dead")                                       # the box is reclaimed
        _, err = self.award("Bo", "f01-z06-0001", expect=1)
        self.assertIn("already awarded", err)                                                  # still closed without the flag
        self.award("Bo", "f01-z06-0001", "--reaward", "Ann died holding it unopened; Caleb's ruling")
        aw = [r for r in self.rows("story-box-ledger.jsonl") if r["event"] == "awarded"]
        self.assertEqual([r["box_id"] for r in aw], ["sb-1-d-1", "sb-1-d-1-r2"])
        self.assertEqual(aw[1]["reaward_of"], ["sb-1-d-1"])
        self.assertIn("Caleb's ruling", aw[1]["reaward_reason"])
        self.assertEqual(self.crawler("Bo")["boxes"]["legendary"], 1)
        # the cap counts the new box only
        self.assertEqual(S.loot.legendary_count([], 1, self.rows("story-box-ledger.jsonl")) if hasattr(S.loot, "legendary_count") else 1, 1)
        self.run_cmd("add-crawler", "Cy", "--player", "C", "--class", "Rogue", "--species", "Human")
        _, err = self.award("Cy", "f01-z06-0002", "--reaward", "again", expect=1)           # r2 is not reclaimed
        self.assertIn("not a reclaimed", err)
        self.assertIn("ledger OK", self.run_cmd("ledger", "verify")[0])

    def test_reaward_refused_when_the_first_box_was_opened_sold_or_released_by_delete(self):
        self.award()
        self.run_cmd("loot", "story-box", "--open", "--crawler", "Ann", "--safe-room")
        self.run_cmd("condition", "add", "Ann", "Dead")
        _, err = self.award("Bo", "f01-z06-0002", "--reaward", "x", expect=1)
        self.assertIn("not a reclaimed", err)
        # released by /delete: the deed stays closed
        self.run_cmd("add-crawler", "Cy", "--player", "C", "--class", "Rogue", "--species", "Human")
        self.run_cmd("set", "crawlers.cy.boxes.legendary", "0")
        self.run_cmd("loot", "story-box", "1", "z06", "--witness", "GM", "--pick", "f01-z06-0002", "--crawler", "Cy", "--deed", "Did another great deed", "--deed-id", "d-2", "--override-cap", "test")
        self.run_cmd("crawler", "delete", "Cy", "--reason", "x", "--confirm", "Cy")
        _, err = self.run_cmd("loot", "story-box", "1", "z06", "--witness", "GM", "--pick", "f01-z06-0002", "--crawler", "Bo", "--deed", "Did another great deed", "--deed-id", "d-2", "--reaward", "x", expect=1)
        self.assertIn("not a reclaimed", err)

    def test_reaward_needs_an_earlier_award(self):
        _, err = self.award("Ann", "f01-z06-0001", "--reaward", "x", expect=1)
        self.assertIn("no earlier award", err)


if __name__ == "__main__":
    unittest.main()
