"""Fix (Oct 7 2026, lost table lines): `discord_gm.py new` marks transcript lines read only while THIS run holds the GM turn lock
(tools/gm_lock.sh) or while no run holds it. No network: fetch() is mocked. Run: python3 -m unittest discover -s tools/tests -p 'test_*.py'"""
import contextlib
import importlib.util
import io
import os
import subprocess
import tempfile
import time
import unittest
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discord_gm_lock_under_test", os.path.join(TOOLS, "discord_gm.py"))
gm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gm)

MSGS = [{"id": "101", "content": "Hornn: I swing the mop."}, {"id": "102", "content": "Moses: Turbo bites it."}]


class TurnLockTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lock = os.path.join(self.tmp.name, ".gm-lock")
        self.cursor = os.path.join(self.tmp.name, ".discord-cursor")
        env = mock.patch.dict(os.environ, {"DCC_SESSION": "alpha", "DCC_GM_LOCK_DIR": self.lock, "DCC_CAMPAIGN_ROOT": self.tmp.name})
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop("DCC_GM_LOCK_TOKEN", None)
        cur = mock.patch.object(gm, "CURSOR", self.cursor)
        cur.start()
        self.addCleanup(cur.stop)
        self.fetch = mock.patch.object(gm, "fetch", side_effect=lambda limit, after=None: [m for m in MSGS if not after or int(m["id"]) > int(after)])
        self.fetch.start()
        self.addCleanup(self.fetch.stop)
        with open(self.cursor, "w") as f:
            f.write("100")

    def cursor_value(self):
        return open(self.cursor).read().strip()

    def other_run_holds_lock(self, token="other-run", ppid="1"):
        os.mkdir(self.lock)
        with open(os.path.join(self.lock, "owner"), "w") as f:
            f.write(f"token={token}\nppid={ppid}\npid=1\nat={int(time.time())}\n")

    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            gm.main(list(argv))
        return out.getvalue()

    def test_no_lock_held_reads_and_marks_read_as_before(self):
        out = self.run_cli("new")
        self.assertIn("[101] Hornn", out)
        self.assertEqual(self.cursor_value(), "102")
        self.assertIn("(no new player speech)", self.run_cli("new"))

    def test_other_run_holding_lock_peeks_without_marking_read(self):
        self.other_run_holds_lock()
        out = self.run_cli("new")
        self.assertIn("PEEK ONLY", out)
        self.assertIn("[102] Moses", out)
        self.assertEqual(self.cursor_value(), "100", "lines must stay unread for the run that holds the lock")

    def test_lock_without_owner_info_is_treated_as_someone_else(self):
        os.mkdir(self.lock)
        self.assertEqual(gm.lock_state(), "unknown")
        self.run_cli("new")
        self.assertEqual(self.cursor_value(), "100")

    def test_new_lock_takes_lock_then_reads_and_marks(self):
        out = self.run_cli("new", "--lock")
        self.assertIn("[101]", out)
        self.assertEqual(self.cursor_value(), "102")
        self.assertTrue(os.path.isdir(self.lock))
        self.assertEqual(gm.lock_state(), "mine")
        self.assertIn("released", self.run_cli("unlock"))
        self.assertFalse(os.path.exists(self.lock))

    def test_new_lock_busy_reads_nothing_and_exits_1(self):
        self.other_run_holds_lock()
        with self.assertRaises(SystemExit) as cm:
            self.run_cli("new", "--lock")
        self.assertEqual(cm.exception.code, 1)
        gm.fetch.assert_not_called()
        self.assertEqual(self.cursor_value(), "100")
        self.assertTrue(os.path.isdir(self.lock), "the other run's lock is untouched")

    def test_new_lock_wait_gets_the_turn_once_the_other_run_releases(self):
        self.other_run_holds_lock()
        calls = {"n": 0}
        real_sleep = time.sleep

        def fake_sleep(s):
            calls["n"] += 1
            if calls["n"] == 2:   # the other run finishes and releases
                gm.lock_release(force=True)
            real_sleep(0)
        with mock.patch.object(gm.time, "sleep", side_effect=fake_sleep):
            status, msgs = gm.read_new("lock", wait=30, poll=0.01)
        self.assertEqual(status, "read")
        self.assertEqual([m["id"] for m in msgs], ["101", "102"])
        self.assertEqual(self.cursor_value(), "102")

    def test_stale_lock_is_replaced(self):
        self.other_run_holds_lock()
        old = time.time() - 300
        os.utime(self.lock, (old, old))
        self.assertEqual(gm.lock_state(), "free")
        self.run_cli("new", "--lock")
        self.assertEqual(gm.lock_state(), "mine")
        self.assertEqual(self.cursor_value(), "102")

    def test_peek_never_advances_even_with_lock(self):
        self.run_cli("new", "--lock")
        with open(self.cursor, "w") as f:
            f.write("100")
        self.run_cli("new", "--peek")
        self.assertEqual(self.cursor_value(), "100")

    def test_token_ownership(self):
        os.environ["DCC_GM_LOCK_TOKEN"] = "run-A"
        self.assertTrue(gm.lock_acquire())
        self.assertEqual(gm.lock_state(), "mine")
        os.environ["DCC_GM_LOCK_TOKEN"] = "run-B"
        self.assertEqual(gm.lock_state(), "other")
        self.run_cli("new")
        self.assertEqual(self.cursor_value(), "100")
        os.environ["DCC_GM_LOCK_TOKEN"] = "run-A"
        self.run_cli("new")
        self.assertEqual(self.cursor_value(), "102")

    def test_unlock_refuses_another_runs_lock_unless_forced(self):
        self.other_run_holds_lock()
        with self.assertRaises(SystemExit):
            self.run_cli("unlock")
        self.assertTrue(os.path.isdir(self.lock))
        self.run_cli("unlock", "--force")
        self.assertFalse(os.path.exists(self.lock))

    def test_lock_and_peek_together_is_refused(self):
        with self.assertRaises(SystemExit):
            self.run_cli("new", "--lock", "--peek")

    def test_default_lock_dir_sits_next_to_the_cursor(self):
        os.environ.pop("DCC_GM_LOCK_DIR")
        self.assertEqual(gm.lock_dir(), os.path.join(self.tmp.name, ".gm-lock"))


class GmLockShellTests(unittest.TestCase):
    """gm_lock.sh writes the owner file the Python side reads; release removes the (non-empty) lock dir."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.lock = os.path.join(self.tmp.name, "sessions", ".gm-lock")
        os.makedirs(os.path.dirname(self.lock))
        self.env = {**os.environ, "DCC_CAMPAIGN_ROOT": self.tmp.name, "DCC_SESSION": "alpha", "DCC_GM_LOCK_TOKEN": "tok-1"}
        self.env.pop("DCC_GM_LOCK_DIR", None)

    def sh(self, *args):
        return subprocess.run(["bash", os.path.join(TOOLS, "gm_lock.sh"), *args], env=self.env, capture_output=True, text=True)

    def test_acquire_writes_owner_busy_then_release(self):
        r = self.sh("acquire")
        self.assertEqual((r.returncode, r.stdout.strip()), (0, "acquired"))
        owner = open(os.path.join(self.lock, "owner")).read()
        self.assertIn("token=tok-1", owner)
        self.assertIn("ppid=", owner)
        self.assertEqual(self.sh("acquire").returncode, 1)
        self.assertEqual(self.sh("status").stdout.strip(), "held")
        with mock.patch.dict(os.environ, {"DCC_GM_LOCK_DIR": self.lock, "DCC_GM_LOCK_TOKEN": "tok-1"}):
            self.assertEqual(gm.lock_state(self.lock), "mine")
        with mock.patch.dict(os.environ, {"DCC_GM_LOCK_TOKEN": "tok-2"}):
            self.assertEqual(gm.lock_state(self.lock), "other")
        self.assertEqual(self.sh("release").stdout.strip(), "released")
        self.assertFalse(os.path.exists(self.lock))
        self.assertEqual(self.sh("status").stdout.strip(), "free")


if __name__ == "__main__":
    unittest.main()
