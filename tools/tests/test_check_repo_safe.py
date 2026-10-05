"""Tests for tools/check_repo_safe.py. All fake secrets are built at run time so this file holds no secret-shaped string."""
import io
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import check_repo_safe as c  # noqa: E402

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "check_repo_safe.py")


def fake_discord_token():
    return "M" + "A" * 23 + "." + "b" * 6 + "." + "c" * 27


def fake_webhook():
    return "https://discord" + ".com/api/webhooks/" + "1" * 18 + "/" + "Ab" * 20


class PathRules(unittest.TestCase):
    def test_blocked(self):
        for p in ["gm-notes/secret/x.md", "gm-notes/secret/deep/y.json", "sessions/state.json", "sessions/session.json",
                  "sessions/credit-ledger.jsonl", "sessions/backups/state.1.json", "credit-ledger.jsonl", "tools/credit-ledger-old.jsonl",
                  ".env", "bot/.env", ".env.local", "bot.log", "logs/other.log", "node_modules/x/index.js", "keys/a.pem", "token.txt",
                  "sessions-data/foo/state.json"]:
            self.assertIsNotNone(c.forbidden_path(p), p)

    def test_allowed(self):
        for p in ["rules/00-overview.md", "gm-notes/00-gm-principles.md", "tools/state.py", "tools/tests/test_state.py", ".env.example",
                  "decisions/028-collapse-death-loot.md", "lore/CANON-LEDGER.md", "tables/loot-decks/a.json"]:
            self.assertIsNone(c.forbidden_path(p), p)


class ContentRules(unittest.TestCase):
    def kinds(self, text, strict=False):
        return {k for _, k in c.scan_text(text, strict)}

    def test_discord_token(self):
        self.assertIn("discord-bot-token", self.kinds("tok = '%s'" % fake_discord_token()))

    def test_webhook_url(self):
        self.assertIn("discord-webhook-url", self.kinds("see " + fake_webhook()))

    def test_openai_key(self):
        self.assertIn("openai-style-key", self.kinds("k=" + "sk-" + "Z9" * 15))

    def test_gm_webhook_assignment(self):
        self.assertIn("gm-webhook-assignment", self.kinds("GM_WEBHOOK_URL=" + "abc123def456ghi789"))
        self.assertIn("gm-webhook-assignment", self.kinds('"GM_WEBHOOK_KEY": "' + "q1w2e3r4t5y6" + '"'))

    def test_gm_webhook_name_only_is_ok_unless_strict(self):
        t = "Secrets come from the shell: GM_WEBHOOK_URL and GM_WEBHOOK_KEY."
        self.assertEqual(self.kinds(t), set())
        self.assertIn("gm-webhook-name-mention(strict)", self.kinds(t, strict=True))

    def test_generic_key_assignment(self):
        self.assertIn("secret-assignment", self.kinds("FISH_API_KEY=" + "a1b2c3d4e5f6g7h8i9j0k1"))

    def test_placeholders_and_prose_pass(self):
        for t in ["OPENAI_API_KEY=<your key here>", "TOKEN=${TOKEN}", "api_key = os.environ['X']", "token: the token is read from env",
                  "The Crawler paid 12 credits.", "sha256 515d92e96d9bbbd5 ledger v1.12", "see tools/README.md for the password policy"]:
            self.assertEqual(self.kinds(t), set(), t)

    def test_never_returns_matched_text(self):
        tok = fake_discord_token()
        for ln, name in c.scan_text("x\n" + tok):
            self.assertNotIn(tok, str(name))
            self.assertEqual(ln, 2)

    def test_binary_skipped(self):
        self.assertEqual(c.scan_bytes(b"\x00\x01" + fake_discord_token().encode()), [])


def git(args, cwd, **kw):
    return subprocess.run(["git", "-c", "user.name=T", "-c", "user.email=t@t.local"] + args, cwd=cwd, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, **kw)


class StagedHook(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        git(["init", "-q"], self.d)
        hook = os.path.join(self.d, ".git", "hooks", "pre-commit")
        with open(hook, "w") as f:
            f.write('#!/bin/sh\nexec python3 "%s" --staged\n' % os.path.abspath(TOOL))
        os.chmod(hook, 0o755)

    def put(self, rel, text):
        p = os.path.join(self.d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(text)

    def test_clean_commit_passes(self):
        self.put("rules/a.md", "# hi\nCrawlers rule.\n")
        git(["add", "-A"], self.d)
        r = git(["commit", "-qm", "ok"], self.d)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_forbidden_paths_block_commit(self):
        for rel in ["gm-notes/secret/x.md", "sessions/state.json", "sessions/credit-ledger.jsonl", ".env"]:
            self.put(rel, "harmless\n")
            git(["add", "-f", rel], self.d)
            r = git(["commit", "-qm", "bad"], self.d)
            self.assertNotEqual(r.returncode, 0, rel)
            self.assertIn("BLOCKED PATH", r.stderr.decode())
            git(["reset", "-q"], self.d)
            os.remove(os.path.join(self.d, rel))

    def test_secret_content_blocks_commit_without_echo(self):
        tok = fake_discord_token()
        self.put("tools/x.py", "T = '%s'\n" % tok)
        git(["add", "-A"], self.d)
        r = git(["commit", "-qm", "bad"], self.d)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("discord-bot-token", r.stderr.decode())
        self.assertNotIn(tok, r.stderr.decode() + r.stdout.decode())

    def test_tree_mode(self):
        self.put("a/b.md", "fine\n")
        self.put("a/c.md", fake_webhook() + "\n")
        out = io.StringIO()
        self.assertEqual(c.check_tree(self.d, out=out), 1)
        self.assertIn("a/c.md:1", out.getvalue())
        self.assertNotIn("webhooks/", out.getvalue())


if __name__ == "__main__":
    unittest.main()
