"""discord_gm.py whisper (Oct 7 2026): a [PRIVATE - System] post to ONE Crawler's own sheet channel, never a channel the bridge speaks.
No network: a fake client records requests."""
import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discord_gm_whisper_under_test", os.path.join(TOOLS, "discord_gm.py"))
gm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gm)
import publisher as pub  # noqa: E402  (tools/ is on sys.path via discord_gm)


class FakeClient:
    def __init__(self):
        self.calls = []

    def request(self, method, path, body=None):
        self.calls.append((method, path, body))
        return {"id": "1"}


class WhisperTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        os.makedirs(os.path.join(self.tmp.name, "sessions"))
        env = mock.patch.dict(os.environ, {"DCC_CAMPAIGN_DIR": self.tmp.name, "DCC_CAMPAIGN_ROOT": self.tmp.name, "DCC_SESSION": "alpha"})
        env.start()
        self.addCleanup(env.stop)
        for k in ("PLAYER_CHANNELS_FILE", "GM_DISCORD_TOKEN", "GM_OUTPUT_CHANNEL_ID", "TRANSCRIPT_CHANNEL_ID", "VOICE_CHANNEL_ID"):
            os.environ.pop(k, None)
        state = {"campaign": {}, "crawlers": [{"name": "Eisenhorn", "player": "Hornn"}, {"name": "Shirayuki", "player": "Grimmtrouble"}]}
        with open(pub.state_path(), "w") as f:
            json.dump(state, f)
        self.map({"Eisenhorn": {"channel_id": "333333333333333333", "channel_name": "hornn-eisenhorn", "players": ["Hornn"]}})

    def map(self, crawlers):
        with open(pub.channels_path(), "w") as f:
            json.dump({"guild_id": "1", "crawlers": crawlers}, f)

    def test_posts_only_to_the_crawlers_channel_with_private_prefix(self):
        fc = FakeClient()
        r = gm.whisper("Eisenhorn", "Your Benefactor Signal pings: someone is watching.", client=fc, log=lambda m: None)
        self.assertEqual(r["posted"], 1)
        self.assertEqual(len(fc.calls), 1)
        method, path, body = fc.calls[0]
        self.assertEqual((method, path), ("POST", "/channels/333333333333333333/messages"))
        self.assertTrue(body["content"].startswith("[PRIVATE - System] Your Benefactor Signal"))
        self.assertEqual(body["allowed_mentions"], {"parse": []})
        self.assertNotIn(gm.MOUTH, path)

    def test_player_alias_resolves(self):
        fc = FakeClient()
        gm.whisper("Hornn", "psst", client=fc, log=lambda m: None)
        self.assertEqual(fc.calls[0][1], "/channels/333333333333333333/messages")

    def test_refuses_crawler_without_mapped_channel(self):
        fc = FakeClient()
        with self.assertRaises(pub.PublishError) as cm:
            gm.whisper("Shirayuki", "secret", client=fc, log=lambda m: None)
        self.assertIn("REFUSED", str(cm.exception))
        self.assertEqual(fc.calls, [])

    def test_refuses_a_channel_the_bridge_speaks(self):
        for cid in (gm.MOUTH, gm.EARS):
            self.map({"Eisenhorn": {"channel_id": cid}})
            fc = FakeClient()
            with self.assertRaises(pub.PublishError):
                gm.whisper("Eisenhorn", "secret", client=fc, log=lambda m: None)
            self.assertEqual(fc.calls, [])
        self.map({"Eisenhorn": {"channel_id": "444444444444444444"}})
        with mock.patch.dict(os.environ, {"GM_OUTPUT_CHANNEL_ID": "444444444444444444"}):
            with self.assertRaises(pub.PublishError):
                gm.whisper("Eisenhorn", "secret", client=FakeClient(), log=lambda m: None)

    def test_dry_run_posts_nothing_and_long_text_is_split_with_prefix_on_every_part(self):
        fc = FakeClient()
        text = ("The signal hums. " * 300).strip()
        r = gm.whisper("Eisenhorn", text, client=fc, dry_run=True, log=lambda m: None)
        self.assertEqual(fc.calls, [])
        self.assertGreater(len(r["messages"]), 1)
        self.assertTrue(all(m.startswith("[PRIVATE - System]") and len(m) <= 2000 for m in r["messages"]))

    def test_empty_text_refused(self):
        with self.assertRaises(ValueError):
            gm.whisper_messages("   ")

    def test_cli_refusal_exits_1_and_dry_run_cli_needs_no_token(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), self.assertRaises(SystemExit) as cm:
            gm.main(["whisper", "Shirayuki", "x"])
        self.assertEqual(cm.exception.code, 1)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            gm.main(["whisper", "Eisenhorn", "hello there", "--dry-run"])
        self.assertIn("DRY RUN", out.getvalue())
        self.assertIn("[PRIVATE - System] hello there", out.getvalue())


if __name__ == "__main__":
    unittest.main()
