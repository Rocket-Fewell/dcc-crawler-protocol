"""Tests for the spotlight subcommand of tools/discord_gm.py (no network, no Discord token needed).
Run: python3 -m unittest discover -s tools/tests -p 'test_*.py'"""
import contextlib
import datetime as dt
import importlib.util
import io
import json
import os
import stat
import tempfile
import unittest
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discord_gm", os.path.join(TOOLS, "discord_gm.py"))
gm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gm)


class SpotlightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = os.path.join(self.tmp.name, "sub", "spotlight.json")
        env = mock.patch.dict(os.environ, {"SPOTLIGHT_FILE": self.path, "DCC_SESSION": "alpha"}, clear=False)  # pin alpha: main() follows the live active session and would repoint the module defaults
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop("GM_DISCORD_TOKEN", None)
        os.environ.pop("SPOTLIGHT_MAX_AGE_MINUTES", None)

    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            gm.main(list(argv))
        return out.getvalue()

    def read(self):
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def test_default_path_is_campaign_sessions_spotlight_json(self):
        os.environ.pop("SPOTLIGHT_FILE")
        self.assertTrue(os.path.normpath(gm.spotlight_path()).endswith(os.path.join("dcc-campaign", "sessions", "spotlight.json")))

    def test_set_writes_player_aliases_note_and_iso_timestamp(self):
        out = self.run_cli("spotlight", "set", "Trailer Park Moses", "--alias", "Moses", "--alias", "TPM", "--note", "vending wall")
        self.assertIn("spotlight ON", out)
        d = self.read()
        self.assertEqual(d["player"], "Trailer Park Moses")
        self.assertEqual(d["aliases"], ["Moses", "TPM"])
        self.assertEqual(d["note"], "vending wall")
        ts = dt.datetime.fromisoformat(d["updated"])
        self.assertIsNotNone(ts.tzinfo)
        self.assertLess(abs((dt.datetime.now().astimezone() - ts).total_seconds()), 5)
        self.assertEqual(set(d), {"player", "aliases", "updated", "note"})

    def test_set_does_not_need_discord_token_and_makes_no_network_call(self):
        with mock.patch.object(gm.urllib.request, "urlopen", side_effect=AssertionError("network used")):
            self.run_cli("spotlight", "set", "Hornn")
            self.run_cli("spotlight", "show")
            self.run_cli("spotlight", "clear")

    def test_clear_sets_player_null_and_keeps_file(self):
        self.run_cli("spotlight", "set", "Hornn")
        out = self.run_cli("spotlight", "clear")
        self.assertIn("cleared", out)
        d = self.read()
        self.assertIsNone(d["player"])
        self.assertEqual(d["aliases"], [])
        self.assertEqual(gm.spotlight_state()[0], "open")

    def test_show_reports_each_state(self):
        self.assertIn("OFF", self.run_cli("spotlight", "show"))  # missing file
        self.run_cli("spotlight", "set", "Hornn", "--alias", "H")
        shown = self.run_cli("spotlight", "show")
        self.assertIn("ACTIVE: Hornn", shown)
        self.assertIn("aliases: H", shown)
        old = (dt.datetime.now().astimezone() - dt.timedelta(minutes=45)).isoformat(timespec="seconds")
        with open(self.path, "w") as f:
            json.dump({"player": "Hornn", "aliases": [], "updated": old, "note": ""}, f)
        self.assertIn("STALE", self.run_cli("spotlight", "show"))
        with open(self.path, "w") as f:
            f.write("{not json")
        self.assertIn("malformed", self.run_cli("spotlight", "show"))

    def test_max_age_env_is_honoured(self):
        old = (dt.datetime.now().astimezone() - dt.timedelta(minutes=30)).isoformat(timespec="seconds")
        os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w") as f:
            json.dump({"player": "Hornn", "updated": old}, f)
        self.assertEqual(gm.spotlight_state()[0], "stale")
        with mock.patch.dict(os.environ, {"SPOTLIGHT_MAX_AGE_MINUTES": "60"}):
            self.assertEqual(gm.spotlight_state()[0], "active")

    def test_set_again_refreshes_timestamp(self):
        old = (dt.datetime.now().astimezone() - dt.timedelta(minutes=30)).isoformat(timespec="seconds")
        os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w") as f:
            json.dump({"player": "Hornn", "updated": old}, f)
        self.run_cli("spotlight", "set", "Hornn")
        self.assertEqual(gm.spotlight_state()[0], "active")

    def test_rejects_empty_and_overlong_names(self):
        for bad in ("", "   ", "x" * 101):
            with self.assertRaises(SystemExit):
                self.run_cli("spotlight", "set", bad)
        self.assertFalse(os.path.exists(self.path))

    def test_write_is_atomic_no_temp_files_left_and_old_file_survives_failure(self):
        self.run_cli("spotlight", "set", "Hornn")
        before = self.read()
        with mock.patch.object(gm.os, "replace", side_effect=OSError("disk gone")):
            with self.assertRaises(OSError):
                gm.spotlight_set("Someone Else", path=self.path)
        self.assertEqual(self.read(), before)  # target untouched
        self.assertEqual(os.listdir(os.path.dirname(self.path)), ["spotlight.json"])  # temp cleaned up
        self.assertTrue(stat.S_IMODE(os.stat(self.path).st_mode) & 0o444)  # readable by the bridge

    def test_unicode_names_round_trip(self):
        self.run_cli("spotlight", "set", "José Ñandú")
        self.assertEqual(self.read()["player"], "José Ñandú")

    def test_existing_subcommands_still_parse(self):
        # `say` without a token must fail cleanly on the token, proving the original CLI still dispatches.
        with self.assertRaises(SystemExit) as cm:
            self.run_cli("say", "hello")
        self.assertIn("GM_DISCORD_TOKEN", str(cm.exception))


class StopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = os.path.join(self.tmp.name, "nested", "voice-control.json")
        env = mock.patch.dict(os.environ, {"VOICE_CONTROL_FILE": self.path, "DCC_SESSION": "alpha"})  # pin alpha: main() follows the live active session and would repoint the module defaults
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop("GM_DISCORD_TOKEN", None)

    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            gm.main(list(argv))
        return out.getvalue()

    def read(self):
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def test_default_path(self):
        os.environ.pop("VOICE_CONTROL_FILE")
        self.assertTrue(os.path.normpath(gm.voice_control_path()).endswith(os.path.join("dcc-campaign", "sessions", "voice-control.json")))

    def test_stop_writes_flush_with_unique_id_and_iso_ts(self):
        out = self.run_cli("stop")
        self.assertIn("stop signal written", out)
        d = self.read()
        self.assertEqual(set(d), {"action", "id", "ts"})
        self.assertEqual(d["action"], "flush")
        self.assertTrue(d["id"])
        self.assertIsNotNone(dt.datetime.fromisoformat(d["ts"]).tzinfo)
        first = d["id"]
        self.run_cli("stop")
        self.assertNotEqual(self.read()["id"], first, "every stop gets a new id so the bridge sees a new event")

    def test_stop_needs_no_token_no_network_and_is_atomic(self):
        with mock.patch.object(gm.urllib.request, "urlopen", side_effect=AssertionError("network used")):
            self.run_cli("stop")
        before = self.read()
        with mock.patch.object(gm.os, "replace", side_effect=OSError("disk gone")):
            with self.assertRaises(OSError):
                gm.stop_voice(self.path)
        self.assertEqual(self.read(), before)
        self.assertEqual(os.listdir(os.path.dirname(self.path)), ["voice-control.json"])


if __name__ == "__main__":
    unittest.main()
