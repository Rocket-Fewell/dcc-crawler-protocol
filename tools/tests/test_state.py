"""Tests for tools/state.py. Run: python3 -m unittest discover -s tools/tests -p 'test_*.py'"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("state", os.path.join(TOOLS, "state.py"))
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)


class StateTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        patcher = mock.patch.dict(os.environ, {"DCC_CAMPAIGN_DIR": self.tmp.name})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.sessions = os.path.join(self.tmp.name, "sessions")
        self.path = os.path.join(self.sessions, "state.json")

    # helpers
    def run_cmd(self, *argv, expect=0):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = state.main(list(argv))
            except SystemExit as e:  # argparse usage errors
                code = e.code
        self.assertEqual(code, expect, f"{argv}: stdout={out.getvalue()!r} stderr={err.getvalue()!r}")
        return out.getvalue().strip(), err.getvalue().strip()

    def load(self):
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def read_json(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def read_text(path):
        with open(path, encoding="utf-8") as f:
            return f.read()

    def digest(self):
        with open(self.path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def backups(self):
        return state.list_backups()

    def init_party(self):
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Grimsby", "--player", "Caleb", "--class", "Rogue", "--species", "Human", "--hp-max", "30", "--ac", "15")
        self.run_cmd("add-crawler", "Donut", "--player", "Sam", "--class", "Bard", "--species", "Cat", "--hp-max", "20")
        self.run_cmd("add-crawler", "Mongo", "--player", "Ann", "--class", "Fighter", "--species", "Dragonborn", "--hp-max", "40")
        self.run_cmd("add-crawler", "Carl", "--player", "Bo", "--class", "Barbarian", "--species", "Human", "--hp-max", "45")

    def crawler(self, name):
        return next(c for c in self.load()["crawlers"] if c["name"] == name)


class SchemaTests(StateTestCase):
    def test_init_schema(self):
        self.run_cmd("init", "--floor", "2", "--zone", "Orientation Pit")
        s = self.load()
        self.assertEqual(s["campaign"]["current_floor"], 2)
        self.assertEqual(s["campaign"]["zone"], "Orientation Pit")
        self.assertEqual(s["campaign"]["death_mode"], "Costly Revives")
        self.assertEqual(s["campaign"]["comfort"], "Ludicrous")
        self.assertEqual(s["party"]["revives_used"], 0)
        self.assertEqual(s["crawlers"], [])
        self.assertEqual((s["limits"]["revive_party_cooldown_floors"], s["limits"]["revive_campaign_cap"], s["limits"]["revive_per_crawler_cap"]), (3, 3, 1))
        self.assertEqual(state.validate_state(s), ([], []))

    def test_init_refuses_overwrite_without_force(self):
        self.run_cmd("init")
        before = self.digest()
        _, err = self.run_cmd("init", expect=1)
        self.assertIn("already exists", err)
        self.assertEqual(self.digest(), before)
        self.run_cmd("init", "--force")
        self.assertEqual(len(self.backups()), 1)

    def test_add_crawler_schema(self):
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Grimsby", "--player", "Caleb", "--class", "Rogue", "--species", "Human", "--abilities", "dex=18,str=8")
        c = self.crawler("Grimsby")
        for key in ("name", "player", "class", "species", "level", "xp", "hp", "hit_dice", "ac", "abilities", "inventory", "credits",
                    "conditions", "vows", "boons", "achievements", "boxes", "revives_used", "bypasses_used", "fan_profile", "notes"):
            self.assertIn(key, c)
        self.assertEqual(c["abilities"]["dex"], 18)
        self.assertEqual(c["abilities"]["wis"], 10)
        self.assertEqual(set(c["boxes"]), {"bronze", "silver", "gold", "platinum", "legendary", "celestial"})
        self.assertEqual(set(c["fan_profile"]), {"quirks", "notes", "opt_outs"})
        self.assertEqual(c["hp"], {"current": 10, "max": 10, "temp": 0})
        _, err = self.run_cmd("add-crawler", "grimsby", "--player", "X", "--class", "Y", "--species", "Z", expect=1)
        self.assertIn("already exists", err)
        _, err = self.run_cmd("add-crawler", "Bad", "--player", "X", "--class", "Y", "--species", "Z", "--abilities", "foo=3", expect=1)

    def test_commands_need_init(self):
        _, err = self.run_cmd("show", expect=1)
        self.assertIn("init", err)
        _, err = self.run_cmd("hp", "damage", "x", "1", expect=1)
        self.assertFalse(os.path.exists(self.path))

    def test_get_set_paths(self):
        self.init_party()
        out, _ = self.run_cmd("get", "crawlers.grimsby.hp.max")  # lookup by crawler name, case-insensitive
        self.assertEqual(out.strip(), "30")
        self.run_cmd("get", "crawlers.0.name")
        self.run_cmd("set", "campaign.current_floor", "3")
        self.run_cmd("set", "campaign.zone", "The Pit")  # plain string
        self.run_cmd("set", "crawlers.grimsby.fan_profile.quirks.-", '"loves tea"')  # append
        self.run_cmd("set", "crawlers.donut.notes", '"json string"')
        s = self.load()
        self.assertEqual((s["campaign"]["current_floor"], s["campaign"]["zone"]), (3, "The Pit"))
        self.assertEqual(self.crawler("Grimsby")["fan_profile"]["quirks"], ["loves tea"])
        self.assertEqual(self.crawler("Donut")["notes"], "json string")
        _, err = self.run_cmd("get", "crawlers.nobody.hp", expect=1)
        _, err = self.run_cmd("get", "campaign.nope", expect=1)

    def test_validate_reports_problems(self):
        self.init_party()
        self.assertIn("valid", self.run_cmd("validate")[0])
        bad = self.load()
        bad["crawlers"][0]["hp"]["current"] = 99
        bad["crawlers"][1]["boxes"].pop("gold")
        bad_path = os.path.join(self.tmp.name, "bad.json")
        with open(bad_path, "w") as f:
            json.dump(bad, f)
        out, _ = self.run_cmd("validate", "--file", bad_path, expect=1)
        self.assertIn("hp.current", out)
        self.assertIn("boxes", out)


class HpTests(StateTestCase):
    def setUp(self):
        super().setUp()
        self.init_party()

    def hp(self, name):
        return self.crawler(name)["hp"]

    def test_damage_clamps_at_zero(self):
        out, _ = self.run_cmd("hp", "damage", "Donut", "5")
        self.assertEqual(self.hp("Donut"), {"current": 15, "max": 20, "temp": 0})
        out, _ = self.run_cmd("hp", "damage", "Donut", "17")  # more than current, less than max overkill
        self.assertEqual(self.hp("Donut")["current"], 0)
        self.assertIn("AT 0 HP", out)
        self.assertNotIn("MASSIVE", out)

    def test_massive_damage_flagged(self):
        out, _ = self.run_cmd("hp", "damage", "Donut", "100")
        self.assertEqual(self.hp("Donut")["current"], 0)
        self.assertIn("MASSIVE DAMAGE", out)

    def test_temp_hp_absorbs_first(self):
        self.run_cmd("hp", "temp", "Grimsby", "8")
        self.run_cmd("hp", "damage", "Grimsby", "5")
        self.assertEqual(self.hp("Grimsby"), {"current": 30, "max": 30, "temp": 3})
        self.run_cmd("hp", "damage", "Grimsby", "10")
        self.assertEqual(self.hp("Grimsby"), {"current": 23, "max": 30, "temp": 0})

    def test_temp_hp_does_not_stack(self):
        self.run_cmd("hp", "temp", "Grimsby", "8")
        self.run_cmd("hp", "temp", "Grimsby", "5")
        self.assertEqual(self.hp("Grimsby")["temp"], 8)
        self.run_cmd("hp", "temp", "Grimsby", "12")
        self.assertEqual(self.hp("Grimsby")["temp"], 12)
        self.run_cmd("hp", "temp", "Grimsby", "2", "--replace")
        self.assertEqual(self.hp("Grimsby")["temp"], 2)

    def test_heal_clamps_to_max_and_ignores_temp(self):
        self.run_cmd("hp", "damage", "Mongo", "10")
        self.run_cmd("hp", "temp", "Mongo", "4")
        out, _ = self.run_cmd("hp", "heal", "Mongo", "50")
        self.assertEqual(self.hp("Mongo"), {"current": 40, "max": 40, "temp": 4})
        self.assertIn("healed 10 of 50", out)

    def test_set_clamps_and_max_change(self):
        out, _ = self.run_cmd("hp", "set", "Carl", "500")
        self.assertEqual(self.hp("Carl")["current"], 45)
        self.assertIn("clamped", out)
        self.run_cmd("hp", "set", "Carl", "-5")
        self.assertEqual(self.hp("Carl")["current"], 0)
        self.run_cmd("hp", "set", "Carl", "10", "--max", "60")
        self.assertEqual(self.hp("Carl"), {"current": 10, "max": 60, "temp": 0})
        self.run_cmd("hp", "set", "Carl", "50", "--max", "20")  # shrinking max clamps current
        self.assertEqual(self.hp("Carl"), {"current": 20, "max": 20, "temp": 0})
        self.run_cmd("hp", "set", "Carl", "5", "--max", "0", expect=1)

    def test_negative_amounts_rejected_without_writing(self):
        before = self.digest()
        for action in ("damage", "heal", "temp"):
            self.run_cmd("hp", action, "Carl", "-3", expect=1)
        self.assertEqual(self.digest(), before)

    def test_unknown_or_ambiguous_crawler(self):
        _, err = self.run_cmd("hp", "damage", "Nobody", "1", expect=1)
        self.assertIn("no crawler", err)
        self.run_cmd("add-crawler", "Carla", "--player", "Z", "--class", "Cleric", "--species", "Elf")
        _, err = self.run_cmd("hp", "damage", "Carl", "1")  # exact match wins over partial
        _, err = self.run_cmd("hp", "damage", "ar", "1", expect=1)
        self.assertIn("ambiguous", err)


class RevivalTests(StateTestCase):
    def setUp(self):
        super().setUp()
        self.init_party()

    def test_revive_increments_counters(self):
        out, _ = self.run_cmd("use-revive", "Donut")
        s = self.load()
        self.assertEqual(s["party"]["revives_used"], 1)
        self.assertEqual(s["party"]["last_revive_floor"], 1)
        self.assertEqual(self.crawler("Donut")["revives_used"], 1)
        self.assertEqual(s["party"]["revive_log"][0]["crawler"], "Donut")

    def test_per_crawler_cap(self):
        self.run_cmd("use-revive", "Donut")
        self.run_cmd("set", "campaign.current_floor", "10")
        before = self.digest()
        _, err = self.run_cmd("use-revive", "Donut", expect=1)
        self.assertIn("per-crawler cap", err)
        self.assertEqual(self.digest(), before)

    def test_party_cooldown_one_per_three_floors(self):
        self.run_cmd("use-revive", "Donut")  # floor 1
        _, err = self.run_cmd("use-revive", "Grimsby", expect=1)
        self.assertIn("cooldown", err)
        self.run_cmd("set", "campaign.current_floor", "3")
        self.run_cmd("use-revive", "Grimsby", expect=1)  # only 2 floors later
        self.run_cmd("set", "campaign.current_floor", "4")
        self.run_cmd("use-revive", "Grimsby")  # 3 floors later: allowed
        self.assertEqual(self.load()["party"]["revives_used"], 2)

    def test_campaign_cap_of_three(self):
        for floor, who in ((1, "Donut"), (4, "Grimsby"), (7, "Mongo")):
            self.run_cmd("set", "campaign.current_floor", str(floor))
            self.run_cmd("use-revive", who)
        self.run_cmd("set", "campaign.current_floor", "20")
        before = self.digest()
        _, err = self.run_cmd("use-revive", "Carl", expect=1)
        self.assertIn("campaign cap", err)
        self.assertEqual(self.load()["party"]["revives_used"], 3)
        self.assertEqual(self.digest(), before)

    def test_dry_run_does_not_write(self):
        before, n = self.digest(), len(self.backups())
        out, _ = self.run_cmd("use-revive", "Donut", "--dry-run")
        self.assertIn("could be revived", out)
        self.assertEqual((self.digest(), len(self.backups())), (before, n))
        self.run_cmd("use-revive", "Donut")
        self.run_cmd("use-revive", "Donut", "--dry-run", expect=1)

    def test_hand_edit_past_cap_is_rejected_by_validation(self):
        self.run_cmd("set", "crawlers.donut.revives_used", "2", expect=1)
        self.run_cmd("set", "party.revives_used", "4", expect=1)

    def test_bypass_counts_and_optional_cap(self):
        self.run_cmd("use-bypass", "Donut", "--kind", "cockroach")
        self.run_cmd("use-bypass", "Donut")
        s = self.load()
        self.assertEqual(self.crawler("Donut")["bypasses_used"], 2)
        self.assertEqual(s["party"]["bypasses_used"], 2)
        self.assertEqual(s["party"]["revives_used"], 0)  # bypass is not a revive
        self.run_cmd("set", "limits.bypass_per_crawler_cap", "2")
        _, err = self.run_cmd("use-bypass", "Donut", expect=1)
        self.assertIn("bypasses", err)
        self.run_cmd("use-bypass", "Grimsby")


class InventoryEtcTests(StateTestCase):
    def setUp(self):
        super().setUp()
        self.init_party()

    def test_inventory_add_stack_remove(self):
        self.run_cmd("inventory", "add", "Grimsby", "Healing Potion", "--qty", "2")
        self.run_cmd("inventory", "add", "Grimsby", "healing potion")
        self.assertEqual(self.crawler("Grimsby")["inventory"], [{"name": "Healing Potion", "qty": 3, "notes": ""}])
        self.run_cmd("inventory", "remove", "Grimsby", "Healing Potion", "--qty", "2")
        self.assertEqual(self.crawler("Grimsby")["inventory"][0]["qty"], 1)
        self.run_cmd("inventory", "remove", "Grimsby", "Healing Potion", "--qty", "5", expect=1)
        self.run_cmd("inventory", "remove", "Grimsby", "Healing Potion")
        self.assertEqual(self.crawler("Grimsby")["inventory"], [])
        self.run_cmd("inventory", "remove", "Grimsby", "Healing Potion", expect=1)
        self.run_cmd("inventory", "add", "Grimsby", "Rope", "--qty", "0", expect=1)

    def test_credits(self):
        self.run_cmd("credits", "Grimsby", "+500")
        self.run_cmd("credits", "Grimsby", "-200")
        self.assertEqual(self.crawler("Grimsby")["credits"], 300)
        self.run_cmd("credits", "Grimsby", "-301", expect=1)
        self.assertEqual(self.crawler("Grimsby")["credits"], 300)
        self.run_cmd("credits", "Grimsby", "-301", "--allow-debt")
        self.assertEqual(self.crawler("Grimsby")["credits"], -1)
        self.run_cmd("credits", "Grimsby", "=1000")
        self.assertEqual(self.crawler("Grimsby")["credits"], 1000)
        self.run_cmd("credits", "Grimsby", "abc", expect=1)

    def test_conditions_and_achievements(self):
        self.run_cmd("condition", "add", "Donut", "Poisoned")
        self.run_cmd("condition", "add", "Donut", "poisoned", expect=1)
        self.run_cmd("condition", "remove", "Donut", "POISONED")
        self.run_cmd("condition", "remove", "Donut", "poisoned", expect=1)
        self.assertEqual(self.crawler("Donut")["conditions"], [])
        self.run_cmd("achievement", "add", "Donut", "Doormat", "--note", "kicked a door")
        self.run_cmd("achievement", "add", "Donut", "doormat", expect=1)
        a = self.crawler("Donut")["achievements"]
        self.assertEqual((len(a), a[0]["name"], a[0]["floor"]), (1, "Doormat", 1))

    def test_boxes(self):
        self.run_cmd("box", "add", "Carl", "gold", "--count", "2")
        _, err = self.run_cmd("box", "use", "Carl", "gold", expect=1)
        self.assertIn("safe room", err)
        self.assertEqual(self.crawler("Carl")["boxes"]["gold"], 2)
        self.run_cmd("box", "use", "Carl", "gold", "--safe-room")
        self.assertEqual(self.crawler("Carl")["boxes"]["gold"], 1)
        self.run_cmd("box", "use", "Carl", "silver", "--safe-room", expect=1)
        self.run_cmd("box", "add", "Carl", "mythic", expect=1)
        self.run_cmd("box", "add", "Carl", "celestial")
        self.run_cmd("box", "add", "Carl", "celestial", expect=1)  # one per crawler

    def test_show_and_json(self):
        out, _ = self.run_cmd("show")
        self.assertIn("Floor 1", out)
        self.assertIn("Grimsby: HP 30/30", out)
        out, _ = self.run_cmd("show", "grimsby")
        self.assertIn("Human Rogue", out)
        out, _ = self.run_cmd("show", "grimsby", "--json")
        self.assertEqual(json.loads(out)["name"], "Grimsby")
        out, _ = self.run_cmd("hp", "damage", "Grimsby", "1", "--json")
        self.assertTrue(json.loads(out)["ok"])


class WriteSafetyTests(StateTestCase):
    def test_backup_created_before_each_write(self):
        self.run_cmd("init")
        self.assertEqual(self.backups(), [])  # nothing existed before the first write
        self.run_cmd("add-crawler", "Grimsby", "--player", "C", "--class", "Rogue", "--species", "Human")
        self.assertEqual(len(self.backups()), 1)
        self.assertEqual(self.read_json(self.backups()[0])["crawlers"], [])  # holds the PRE-write state
        self.run_cmd("hp", "damage", "Grimsby", "3")
        self.assertEqual(len(self.backups()), 2)
        self.assertEqual(self.read_json(self.backups()[-1])["crawlers"][0]["hp"]["current"], 10)

    def test_backup_rotation_keeps_last_20(self):
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Grimsby", "--player", "C", "--class", "Rogue", "--species", "Human", "--hp-max", "100")
        for _ in range(30):
            self.run_cmd("hp", "damage", "Grimsby", "1")
        backups = self.backups()
        self.assertEqual(len(backups), 20)
        newest = self.read_json(backups[-1])
        oldest = self.read_json(backups[0])
        self.assertEqual(newest["crawlers"][0]["hp"]["current"], 100 - 29)  # state before the final write
        self.assertEqual(oldest["crawlers"][0]["hp"]["current"], 100 - 10)
        self.assertEqual(backups, sorted(backups))

    def test_read_only_commands_do_not_write_or_backup(self):
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Grimsby", "--player", "C", "--class", "Rogue", "--species", "Human")
        before, n = self.digest(), len(self.backups())
        for argv in (["show"], ["show", "grimsby"], ["get", "campaign"], ["validate"], ["backups"]):
            self.run_cmd(*argv)
        self.assertEqual((self.digest(), len(self.backups())), (before, n))

    def test_invalid_input_never_overwrites(self):
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Grimsby", "--player", "C", "--class", "Rogue", "--species", "Human")
        before, n = self.digest(), len(self.backups())
        for argv in (
            ["set", "crawlers.grimsby.hp.current", "9999"],
            ["set", "crawlers.grimsby.level", '"high"'],
            ["set", "crawlers.grimsby.hp", "null"],
            ["set", "campaign", "[]"],
            ["set", "crawlers", '{"a":1}'],
            ["set", "crawlers.grimsby.inventory.-", '"just a string"'],
            ["set", "crawlers.grimsby.boxes.bronze", "-1"],
            ["set", "nope.deeper.path", "1"],
            ["hp", "damage", "Grimsby", "-1"],
            ["inventory", "remove", "Grimsby", "nothing"],
            ["restore", "does-not-exist.json"],
        ):
            self.run_cmd(*argv, expect=1)
        self.assertEqual((self.digest(), len(self.backups())), (before, n), "state or backups changed after refused writes")
        self.assertEqual([f for f in os.listdir(self.sessions) if f.startswith(".tmp")], [])

    def test_corrupt_state_is_never_overwritten(self):
        self.run_cmd("init")
        with open(self.path, "w") as f:
            f.write('{"broken": ')
        before = self.digest()
        for argv in (["show"], ["hp", "damage", "x", "1"], ["set", "campaign.zone", "x"], ["snapshot"], ["add-crawler", "A", "--player", "p", "--class", "c", "--species", "s"]):
            _, err = self.run_cmd(*argv, expect=1)
            self.assertIn("not valid JSON", err)
        self.assertEqual(self.digest(), before)
        _, err = self.run_cmd("init", expect=1)  # even init refuses without --force
        self.assertEqual(self.digest(), before)
        self.run_cmd("init", "--force")  # explicit: backs up the corrupt file first
        self.assertEqual(len(self.backups()), 1)
        self.assertEqual(self.read_text(self.backups()[0]), '{"broken": ')

    def test_atomic_replace_failure_leaves_original(self):
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Grimsby", "--player", "C", "--class", "Rogue", "--species", "Human")
        before = self.digest()
        with mock.patch.object(state.os, "replace", side_effect=OSError("disk exploded")):
            self.run_cmd("hp", "damage", "Grimsby", "5", expect=1)
        self.assertEqual(self.digest(), before)
        self.assertEqual([f for f in os.listdir(self.sessions) if f.startswith(".tmp")], [], "temp file left behind")
        self.assertFalse(os.path.exists(os.path.join(self.sessions, ".state.lock")), "lock left behind")
        self.run_cmd("hp", "damage", "Grimsby", "5")  # recovers afterwards
        self.assertEqual(self.crawler("Grimsby")["hp"]["current"], 5)

    def test_unserializable_data_rejected_before_touching_files(self):
        self.run_cmd("init")
        before = self.digest()
        with self.assertRaises(TypeError):
            state.atomic_write_json(self.path, {"x": object()})
        self.assertEqual(self.digest(), before)
        self.assertEqual([f for f in os.listdir(self.sessions) if f.startswith(".tmp")], [])

    def test_lock_blocks_then_times_out(self):
        self.run_cmd("init")
        with state.FileLock(state.lock_path()):
            t = time.time()
            with self.assertRaises(state.StateError):
                with state.FileLock(state.lock_path(), timeout=0.3):
                    pass
            self.assertGreaterEqual(time.time() - t, 0.25)
        with state.FileLock(state.lock_path(), timeout=0.3):  # released afterwards
            pass
        self.assertFalse(os.path.exists(state.lock_path()))

    def test_stale_lock_is_recovered(self):
        self.run_cmd("init")
        with open(state.lock_path(), "w") as f:
            f.write("999999 0\n")  # dead pid
        self.run_cmd("add-crawler", "Grimsby", "--player", "C", "--class", "Rogue", "--species", "Human")
        old = time.time() - 3600  # live pid but very old lock
        with open(state.lock_path(), "w") as f:
            f.write(f"{os.getppid()} 0\n")
        os.utime(state.lock_path(), (old, old))
        self.run_cmd("hp", "damage", "Grimsby", "1")
        self.assertFalse(os.path.exists(state.lock_path()))

    def test_concurrent_writers_do_not_lose_updates(self):
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Grimsby", "--player", "C", "--class", "Rogue", "--species", "Human", "--hp-max", "500")
        n = 8
        procs = [subprocess.Popen([sys.executable, os.path.join(TOOLS, "state.py"), "inventory", "add", "Grimsby", f"Item{i}"],
                                  env=dict(os.environ), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for i in range(n)]
        procs += [subprocess.Popen([sys.executable, os.path.join(TOOLS, "state.py"), "hp", "damage", "Grimsby", "10"],
                                   env=dict(os.environ), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(n)]
        results = [(p.wait(), p.stderr.read()) for p in procs]
        self.assertTrue(all(code == 0 for code, _ in results), results)
        c = self.crawler("Grimsby")
        self.assertEqual(sorted(i["name"] for i in c["inventory"]), sorted(f"Item{i}" for i in range(n)))
        self.assertEqual(c["hp"]["current"], 500 - 10 * n)
        self.assertEqual(state.validate_state(self.load()), ([], []))

    def test_snapshot_and_restore(self):
        self.run_cmd("init")
        self.run_cmd("add-crawler", "Grimsby", "--player", "C", "--class", "Rogue", "--species", "Human", "--hp-max", "30")
        out, _ = self.run_cmd("snapshot")
        snap = [f for f in os.listdir(self.sessions) if f.startswith("state-snapshot-")]
        self.assertEqual(len(snap), 1)
        self.assertRegex(snap[0], r"^state-snapshot-\d{4}-\d{2}-\d{2}\.json$")
        self.assertEqual(self.read_json(os.path.join(self.sessions, snap[0])), self.load())
        self.run_cmd("hp", "damage", "Grimsby", "20")
        self.run_cmd("restore", os.path.join(self.sessions, snap[0]))
        self.assertEqual(self.crawler("Grimsby")["hp"]["current"], 30)
        self.assertGreaterEqual(len(self.backups()), 1)  # pre-restore state was backed up

    def test_default_dir_resolves_without_env(self):
        """With DCC_CAMPAIGN_ROOT/DIR unset, campaign_dir() resolves via tools/ parent (portable)."""
        with mock.patch.dict(os.environ):
            os.environ.pop("DCC_CAMPAIGN_DIR", None)
            os.environ.pop("DCC_CAMPAIGN_ROOT", None)
            os.environ.pop("DCC_SESSION", None)
            import dcc_paths
            expected = str(dcc_paths.campaign_root())  # reads env live
            self.assertEqual(state.campaign_dir(), expected)
            # Data dir follows DCC_SESSION / sessions/active-session.json / alpha (not hard-coded to alpha).
            self.assertEqual(state.state_path(), os.path.join(state.csession.data_dir(), "state.json"))
            self.assertTrue(state.state_path().startswith(expected + os.sep))


if __name__ == "__main__":
    unittest.main()
