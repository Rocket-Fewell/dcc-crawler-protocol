"""Tests for tools/agents_channel.py. HTTP layer mocked: no network."""
import contextlib
import importlib.util
import io
import json
import os
import unittest
import urllib.error
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("agents_channel", os.path.join(TOOLS, "agents_channel.py"))
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)
FAKE_TOKEN = "FAKE.test.token-not-real"
# fake webhook URLs are assembled at runtime so no webhook-shaped literal sits in this file (backup secret grep)
HOOK_BASE = "https://discord.com/api/" + "web" + "hooks/"


def fake_hook(n):
    return f"{HOOK_BASE}{1000 + n}/fake-{n}-token_not_real_xxxxxxxxxxxx"


class Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def msg(i, content, name="Lore", ts="2026-10-05T17:30:00+00:00"):
    return {"id": str(1556724390467735613 + i), "content": content, "timestamp": ts, "author": {"username": name.lower(), "global_name": name}}


class AgentsChannel(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.replies = []
        p = mock.patch.object(ac, "_open", side_effect=self._open)
        p.start(); self.addCleanup(p.stop)
        e = mock.patch.dict(os.environ, {"GM_DISCORD_TOKEN": FAKE_TOKEN})
        e.start(); self.addCleanup(e.stop)

    def _open(self, req):
        self.calls.append(req)
        r = self.replies.pop(0)
        if isinstance(r, Exception):
            raise r
        return Resp(json.dumps(r).encode())

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = ac.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_read_oldest_first_ct_and_filter(self):
        self.replies = [[msg(3, "[Lore -> GM] three"), msg(1, "[GM -> Lore, Syndicate] one", "GM"), msg(2, "[Syndicate -> lore] two", "Syndicate")]]
        code, out, err = self.run_cli("read", "--limit", "3", "--to", "LORE")
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines(), ["[2026-10-05 12:30 CT] GM: [GM -> Lore, Syndicate] one",
                                            "[2026-10-05 12:30 CT] Syndicate: [Syndicate -> lore] two"])
        self.assertIn("/channels/1556724390467735613/messages?limit=3", self.calls[0].full_url)
        self.assertNotIn(FAKE_TOKEN, out + err)

    def test_since_and_pins(self):
        self.replies = [[], {"items": [{"message": msg(0, "Welcome to #agents", "Caleb")}]}]
        self.run_cli("read", "--since", "1556724390467735613")
        self.assertIn("after=1556724390467735613", self.calls[0].full_url)
        self.assertTrue(ac.line(dict(msg(9, ""), type=6)).endswith("Lore: (pinned a message)"))
        code, out, _ = self.run_cli("pins")
        self.assertEqual(code, 0)
        self.assertIn("Caleb: Welcome to #agents", out)
        self.assertTrue(self.calls[1].full_url.endswith("/pins"))

    def test_post(self):
        self.replies = [{"id": "42"}]
        code, out, _ = self.run_cli("post", "[GM -> Lore] Day 2 pages look good.")
        self.assertEqual(code, 0)
        self.assertIn("42", out)
        body = json.loads(self.calls[0].data)
        self.assertEqual(body["allowed_mentions"], {"parse": []})
        self.assertEqual(self.calls[0].get_method(), "POST")

    def test_post_refuses_secrets(self):
        for text in ["key sk-abcdef1234567890", HOOK_BASE + "123456/abcDEF_ghi",
                     "blob QWxhZGRpbjpvcGVuIHNlc2FtZQ0123456789abcdefABCDEFxyz", f"here {FAKE_TOKEN}",
                     ".".join(["MTU1NjE3OTEzNTc4MzUwNTkzMA", "GaBcDe", "abcdefghijklmnopqrstuvwxyz12345"])]:
            code, out, err = self.run_cli("post", text)
            self.assertEqual(code, 1, text)
            self.assertIn("refused", err)
            self.assertNotIn(FAKE_TOKEN, err)
        self.assertEqual(self.calls, [])

    def test_paths_and_sha_prefixes_pass(self):
        texts = [
            "[Book Author -> Lore] draft at /workspace/dcc-campaign/drafts/achievement-suggestions-days-02-05-lore-pass.md | status: review",
            "[Encounter Bot -> GM] rebuilt floors/f01/day-0{1..5}.{md,json} against rules/70-encounter-budget-5e.json",
            "see /workspace/dcc-campaign/floors/f01/achievement-suggestions-days-02-05.md and /workspace/discord-voice-bridge/src/encounter/extract.js",
            "budget file sha 283265a7\u20268ffc, spec 8c6e537e\u2026f7de",
            "/workspace/dcc-repo-staging/ops/backup-sync.py.bak-20261005-agents restored from backups/2026-10-05/tools_v1.13",
            "[Encounter Bot -> GM] Bot achievement-suggestions-days-02-05-lore-pass.md is ready",
            "file: /workspace/dcc-campaign/tools/tests/test_species_class_reskins.py",
        ]
        for t in texts:
            self.assertEqual(ac.secret_reasons(t), [], t)
        self.replies = [{"id": "9"}]
        code, out, err = self.run_cli("post", texts[0])
        self.assertEqual(code, 0, err)

    def test_real_looking_secrets_still_refused(self):
        b64 = "QWxhZGRpbjpvcGVu" + "IHNlc2FtZQ0123456789" + "abcdefABCDEFxyz"   # fake, built at runtime
        hexblob = "".join("0123456789abcdef"[(i * 7) % 16] for i in range(48))
        cases = {
            "long-base64": [f"blob {b64}", f"sha {hexblob}", f"in a path /tmp/{b64}/x", f"slashed {b64[:20]}/{b64[20:]}Zz9",
                            "dashed " + "-".join([b64[:18], b64[18:36], b64[36:] + "Qz7"])],
            "discord-bot-token": [".".join(["MTU1NjE3OTEzNTc4MzUwNTkzMA", "GaBcDe", "abcdefghijklmnopqrstuvwxyz12345"])],
            "discord-webhook-url": [HOOK_BASE + "1556724390467735613/" + "aB3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY3z"],
            "github-token": ["gh" + "p_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8", "github" + "_pat_" + "11ABCDEFG0" + "x" * 50],
            "sk-style-key": ["s" + "k-" + "proj1234abcd"],
            "auth-header": ["Authorization: Bearer " + b64[:32]],
        }
        for reason, texts in cases.items():
            for t in texts:
                got = ac.secret_reasons(t)
                self.assertTrue(got, t[:12])
                self.assertIn(reason, got, (reason, got))
                code, out, err = self.run_cli("post", t)
                self.assertEqual(code, 1)
                self.assertIn("refused", err)
                self.assertNotIn(t, out + err)
        self.assertEqual(self.calls, [])

    def test_post_as_agent_uses_file_and_env_override(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, ".env.agents")
            with open(path, "w") as f:
                f.write("# c\nAGENTS_WEBHOOK_ARCHITECT=%s\nAGENTS_WEBHOOK_ENCOUNTER_BOT=%s\n" % (fake_hook(1), fake_hook(2)))
            with mock.patch.object(ac, "AGENTS_FILE", path):
                self.replies = [{"id": "7"}, {"id": "8"}]
                code, out, err = self.run_cli("post", "--as", "architect", "[Architect -> all] hi")
                self.assertEqual(code, 0, err)
                req = self.calls[0]
                self.assertEqual(req.full_url, fake_hook(1) + "?wait=true")
                self.assertIsNone(req.get_header("Authorization"))
                self.assertEqual(json.loads(req.data)["username"], "Architect")
                self.assertEqual(json.loads(req.data)["allowed_mentions"], {"parse": []})
                self.assertNotIn(fake_hook(1), out + err)
                with mock.patch.dict(os.environ, {"AGENTS_WEBHOOK_ENCOUNTER_BOT": fake_hook(3)}):
                    code, out, err = self.run_cli("post", "--as", "Encounter Bot", "[Encounter Bot -> GM] ok")
                self.assertEqual(code, 0, err)
                self.assertEqual(self.calls[1].full_url, fake_hook(3) + "?wait=true")
                self.assertIn("posted as Encounter Bot", out)
                # agent with no entry: refused, nothing sent, URL never echoed
                code, out, err = self.run_cli("post", "--as", "Lore", "hello")
                self.assertEqual(code, 1)
                self.assertIn("no valid webhook for Lore", err)
                self.assertEqual(len(self.calls), 2)

    def test_post_as_unknown_and_secret(self):
        code, _, err = self.run_cli("post", "--as", "Mordecai", "hi")
        self.assertEqual(code, 1)
        for n in ac.AGENTS:
            self.assertIn(n, err)
        with mock.patch.dict(os.environ, {"AGENTS_WEBHOOK_LORE": fake_hook(4)}):
            code, _, err = self.run_cli("post", "--as", "Lore", "leak " + fake_hook(5))
        self.assertEqual(code, 1)
        self.assertIn("refused", err)
        self.assertEqual(self.calls, [])

    def test_read_never_uses_webhook(self):
        self.replies = [[msg(1, "hi")]]
        with mock.patch.dict(os.environ, {"AGENTS_WEBHOOK_LORE": fake_hook(6)}):
            self.run_cli("read")
        self.assertTrue(self.calls[0].full_url.startswith(ac.API + "/channels/"))
        self.assertEqual(self.calls[0].get_header("Authorization"), "Bot " + FAKE_TOKEN)

    def test_429_retries_once(self):
        def e429():
            return urllib.error.HTTPError("u", 429, "rate", {}, io.BytesIO(b'{"retry_after": 0.01}'))
        self.replies = [e429(), [msg(1, "hi")]]
        with mock.patch.object(ac.time, "sleep") as sl:
            code, out, _ = self.run_cli("read")
        self.assertEqual(code, 0)
        sl.assert_called_once_with(0.01)
        self.replies = [e429(), e429()]
        with mock.patch.object(ac.time, "sleep"):
            code, _, err = self.run_cli("read")
        self.assertEqual(code, 1)
        self.assertIn("429", err)

    def test_no_token(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            code, _, err = self.run_cli("read")
        self.assertEqual(code, 1)
        self.assertIn("GM_DISCORD_TOKEN is not set", err)
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
