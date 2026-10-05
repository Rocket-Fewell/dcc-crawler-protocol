"""Multi-campaign session addressing: alpha stays at sessions/; others under sessions-data/<id>/."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CampaignSessionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.env = {**os.environ, "DCC_CAMPAIGN_DIR": self.tmp.name, "DCC_AUTO_PUBLISH": "0"}
        self.env.pop("DCC_SESSION", None)
        os.makedirs(os.path.join(self.tmp.name, "sessions"))
        os.makedirs(os.path.join(self.tmp.name, "gm-notes"))
        os.symlink(TOOLS, os.path.join(self.tmp.name, "tools"))

    def run_py(self, *args, expect=0, env=None):
        r = subprocess.run([sys.executable, *args], capture_output=True, text=True, env=env or self.env)
        self.assertEqual(r.returncode, expect, f"{args}: out={r.stdout!r} err={r.stderr!r}")
        return r.stdout.strip(), r.stderr.strip()

    def test_alpha_paths_unchanged_and_list_includes_new_sessions(self):
        sys.path.insert(0, TOOLS)
        import importlib
        import campaign_session as cs
        importlib.reload(cs)
        # with DCC_CAMPAIGN_DIR patched via env, helpers must follow it
        os.environ["DCC_CAMPAIGN_DIR"] = self.tmp.name
        os.environ.pop("DCC_SESSION", None)
        self.assertTrue(cs.data_dir("alpha").endswith(os.path.join("sessions")))
        self.assertEqual(cs.characters_dir("alpha"), os.path.join(self.tmp.name, "characters"))
        self.assertEqual(cs.sheet_category_name("alpha"), "Crawler Sheets")
        self.assertEqual(cs.sheet_channel_prefix("alpha"), "")
        out, _ = self.run_py(os.path.join(TOOLS, "new-session.py"), "s1", "--label", "Season 1")
        self.assertIn("sessions-data/s1", out)
        self.assertEqual(cs.data_dir("s1"), os.path.join(self.tmp.name, "sessions-data", "s1"))
        self.assertEqual(cs.sheet_category_name("s1"), "Crawler Sheets (s1)")
        self.assertEqual(cs.sheet_channel_prefix("s1"), "s1-")
        self.assertEqual(cs.list_sessions(), ["alpha", "s1"])
        listed, _ = self.run_py(os.path.join(TOOLS, "campaign_session.py"), "list")
        self.assertIn("▶ alpha", listed)
        self.assertIn("• s1", listed)

    def test_new_session_empty_ledger_verifies_and_seeds_channel_map(self):
        self.run_py(os.path.join(TOOLS, "new-session.py"), "s1", "--label", "Season 1")
        base = os.path.join(self.tmp.name, "sessions-data", "s1")
        self.assertEqual(os.path.getsize(os.path.join(base, "credit-ledger.jsonl")), 0)
        with open(os.path.join(base, "state.json"), encoding="utf-8") as f:
            st = json.load(f)
        self.assertEqual(st["crawlers"], [])
        self.assertEqual(st["limits"]["max_crawlers"], 4)
        out, _ = self.run_py(os.path.join(TOOLS, "state.py"), "--session", "s1", "ledger", "verify")
        self.assertIn("ledger OK", out)
        with open(os.path.join(base, "player-channels.json"), encoding="utf-8") as f:
            pc = json.load(f)
        self.assertEqual(pc["category_name"], "Crawler Sheets (s1)")
        self.assertEqual(pc["crawlers"], {})
        # alpha files must not appear under the sandbox sessions/ as state
        self.assertFalse(os.path.exists(os.path.join(self.tmp.name, "sessions", "state.json")))

    def test_publisher_prefixes_non_alpha_channel_names(self):
        self.run_py(os.path.join(TOOLS, "new-session.py"), "s1")
        env = {**self.env, "DCC_SESSION": "s1"}
        r = subprocess.run(
            [sys.executable, "-c",
             "import os,sys; sys.path.insert(0, os.environ['TOOLS']); import publisher as p;\n"
             "print(p.default_channel_name({'name':'Horn','player':'Hornn'}, None));\n"
             "print(p.default_channel_name({'name':'Biscuit','player':'Hornn','kind':'pet-crawler'}, None));\n"
             "print(p.load_config()['category_name'])"],
            capture_output=True, text=True, env={**env, "TOOLS": TOOLS})
        self.assertEqual(r.returncode, 0, r.stderr)
        lines = r.stdout.strip().splitlines()
        self.assertEqual(lines[0], "s1-hornn-horn")
        self.assertEqual(lines[1], "s1-hornn-biscuit-sheet")
        self.assertEqual(lines[2], "Crawler Sheets (s1)")

    def test_cli_use_writes_active_file_without_touching_alpha_data(self):
        self.run_py(os.path.join(TOOLS, "new-session.py"), "s1")
        # seed a fake alpha state so we can detect mutation
        alpha_state = os.path.join(self.tmp.name, "sessions", "state.json")
        with open(alpha_state, "w") as f:
            json.dump({"marker": "alpha-untouched"}, f)
        with open(alpha_state, encoding="utf-8") as f:
            before = f.read()
        self.run_py(os.path.join(TOOLS, "campaign_session.py"), "use", "s1")
        with open(os.path.join(self.tmp.name, "sessions", "active-session.json"), encoding="utf-8") as f:
            active = json.load(f)
        self.assertEqual(active["session"], "s1")
        with open(alpha_state, encoding="utf-8") as f:
            self.assertEqual(f.read(), before)
        show, _ = self.run_py(os.path.join(TOOLS, "campaign_session.py"), "show", env={**self.env})  # follows active file
        self.assertIn("active: s1", show)
        # pin tools back to alpha without rewriting the file
        show_a, _ = self.run_py(os.path.join(TOOLS, "campaign_session.py"), "show",
                                env={**self.env, "DCC_SESSION": "alpha"})
        self.assertIn("active: alpha", show_a)
        self.assertIn("/sessions", show_a.split("data:")[1].splitlines()[0])


if __name__ == "__main__":
    unittest.main()
