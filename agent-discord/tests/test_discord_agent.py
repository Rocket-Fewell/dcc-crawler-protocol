"""No-network tests for the Discord channel agent.
Run from the repo root: python3 -m unittest agent-discord/tests/test_discord_agent.py
"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import discord_agent as agent


def message(mid, text, author="Ada", author_id="2", bot=False, attachments=None):
    return {
        "id": str(mid),
        "content": text,
        "author": {"id": author_id, "username": author, "global_name": author, "bot": bot},
        "attachments": attachments or [],
    }


class FakeTransport:
    def __init__(self, me_id="1"):
        self.me_id = me_id
        self.calls = []
        self.messages = []

    def __call__(self, method, path, token, body=None, timeout=20):
        self.calls.append((method, path, body))
        if path == "/users/@me":
            return {"id": self.me_id, "username": "channel-agent"}
        if method == "GET" and path.startswith("/channels/"):
            return list(self.messages)
        if method == "POST" and path.endswith("/messages"):
            return {"id": "99", "content": body["content"]}
        raise AssertionError(path)


class FormatTests(unittest.TestCase):
    def test_split_keeps_paragraphs_under_limit(self):
        parts = agent.split_text("hello\n" + ("word " * 80), n=50)
        self.assertGreater(len(parts), 1)
        self.assertTrue(all(len(p) <= 50 for p in parts))
        self.assertIn("hello", parts[0])

    def test_incoming_skips_self_and_empty(self):
        rows = [
            message(1, "hi", author_id="1"),
            message(2, "   ", author_id="2"),
            message(3, "", author_id="3", attachments=[{"filename": "map.png"}]),
            message(4, "next", author_id="4", bot=True),
        ]
        kept = agent.incoming(rows, "1")
        self.assertEqual([m["id"] for m in kept], ["3", "4"])
        self.assertIn("[bot]", agent.format_line(rows[3]))
        self.assertIn("map.png", agent.format_line(rows[2]))

    def test_wake_payload_has_no_token(self):
        payload = agent.wake_payload("42", [message(7, "hello there")])
        blob = json.dumps(payload)
        self.assertNotIn("token", blob.lower())
        self.assertEqual(payload["event"], "channel_message")
        self.assertEqual(payload["lines"][0]["text"], "hello there")
        self.assertIn("discord_agent.py new", payload["hint"])


class CursorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = agent.CursorStore(self.tmp.name)
        self.transport = FakeTransport()
        self.client = agent.DiscordClient("tok", "555", transport=self.transport)

    def test_new_advances_read_cursor_and_hides_self(self):
        self.transport.messages = [message(10, "mine", author_id="1"), message(11, "yours", author_id="2")]
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            agent.cmd_new(self.client, self.store)
        self.assertIn("yours", out.getvalue())
        self.assertNotIn("mine", out.getvalue())
        self.assertEqual(self.store.read_cursor(), "11")
        self.assertIsNone(self.store.wake_cursor())

    def test_new_empty(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            agent.cmd_new(self.client, self.store)
        self.assertIn("(no new messages)", out.getvalue())

    def test_say_disables_mentions_and_splits(self):
        with contextlib.redirect_stdout(io.StringIO()):
            agent.cmd_say(self.client, "a " * 1000)
        posts = [c for c in self.transport.calls if c[0] == "POST"]
        self.assertGreater(len(posts), 1)
        self.assertEqual(posts[0][2]["allowed_mentions"], {"parse": []})

    def test_say_refuses_blank(self):
        with self.assertRaises(agent.DiscordError):
            agent.cmd_say(self.client, "  ")

    def test_listen_wakes_once_after_debounce_and_keeps_read_cursor(self):
        self.transport.messages = [message(5, "one"), message(6, "two")]
        batch = agent.WakeBatch(2.5, 8)
        woke = []

        def wake_fn(lines):
            woke.append([m["id"] for m in lines])
            return True

        self.assertEqual(agent.cmd_listen_tick(self.client, self.store, batch, 0, wake_fn), "waiting")
        self.assertIsNone(self.store.wake_cursor())
        self.transport.messages = []
        self.assertEqual(agent.cmd_listen_tick(self.client, self.store, batch, 1, wake_fn), "waiting")
        self.assertEqual(agent.cmd_listen_tick(self.client, self.store, batch, 3, wake_fn), "woke")
        self.assertEqual(woke, [["5", "6"]])
        self.assertEqual(self.store.wake_cursor(), "6")
        self.assertIsNone(self.store.read_cursor())

    def test_listen_does_not_advance_when_wake_fails(self):
        self.transport.messages = [message(8, "stay")]
        batch = agent.WakeBatch(0, 8)
        self.assertEqual(agent.cmd_listen_tick(self.client, self.store, batch, 0, lambda lines: False), "waiting")
        self.assertEqual(agent.cmd_listen_tick(self.client, self.store, batch, 1, lambda lines: False), "wake_failed")
        self.assertIsNone(self.store.wake_cursor())
        self.assertTrue(batch.lines)

    def test_own_messages_advance_without_a_wake(self):
        self.transport.messages = [message(3, "echo", author_id="1")]
        batch = agent.WakeBatch(2.5, 8)
        self.assertEqual(agent.cmd_listen_tick(self.client, self.store, batch, 0, lambda lines: True), "advanced")
        self.assertEqual(self.store.wake_cursor(), "3")
        self.assertFalse(batch.lines)


class HttpTests(unittest.TestCase):
    def test_redirect_is_refused(self):
        handler = agent.NoRedirect()
        with self.assertRaises(urllib.error.HTTPError):
            handler.redirect_request(None, None, 302, "found", None, "https://example.invalid")

    def test_http_status_sends_bearer_and_returns_code(self):
        captured = {}

        class Response:
            status = 204

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        class Opener:
            def open(self, req, timeout=20):
                captured["url"] = req.full_url
                captured["auth"] = req.get_header("Authorization")
                captured["body"] = json.loads(req.data.decode())
                return Response()

        status = agent.http_status("https://example.invalid/hook", {"event": "channel_message"}, "sekrit", opener=Opener())
        self.assertEqual(status, 204)
        self.assertEqual(captured["auth"], "Bearer sekrit")
        self.assertEqual(captured["body"]["event"], "channel_message")

    def test_missing_env(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(agent.DiscordError) as ctx:
                agent.require_env()
        self.assertIn("AGENT_DISCORD_TOKEN", str(ctx.exception))
        self.assertIn("AGENT_DISCORD_CHANNEL_ID", str(ctx.exception))

    def test_scrub_removes_secrets(self):
        self.assertEqual(agent.scrub("bad TOKEN and KEY", ["TOKEN", "KEY"]), "bad [redacted] and [redacted]")

    def test_cli_missing_env_exits_without_printing_a_value(self):
        err = io.StringIO()
        with mock.patch.dict(os.environ, {"AGENT_DISCORD_TOKEN": "", "AGENT_DISCORD_CHANNEL_ID": ""}, clear=False):
            with contextlib.redirect_stderr(err):
                code = agent.main(["whoami"])
        self.assertEqual(code, 1)
        self.assertIn("AGENT_DISCORD_TOKEN", err.getvalue())


if __name__ == "__main__":
    unittest.main()
