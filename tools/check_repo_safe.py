#!/usr/bin/env python3
"""check_repo_safe.py: refuse to commit secrets or live campaign state.

Used by the git pre-commit hook (tools/hooks/pre-commit) and runnable by hand.

  python3 tools/check_repo_safe.py            # check the staged files of the current git repo (same as --staged)
  python3 tools/check_repo_safe.py --staged
  python3 tools/check_repo_safe.py --tree DIR # scan a directory tree on disk (used before an export is committed)
  python3 tools/check_repo_safe.py --strict   # also fail on bare mentions of GM_WEBHOOK (default: only a value assignment fails)

Exit 0 = clean, 1 = something blocked, 2 = usage/git error.

It NEVER prints a matched value: only the path, the line number and the kind of pattern.

Blocked paths: anything under gm-notes/secret/; sessions/ and sessions-data/ (state.json, session.json, ledgers,
backups, rolls logs); credit-ledger*; .env and .env.* (except .env.example/.env.sample/.env.template); bot.log and *.log;
node_modules/; key/cert files (*.pem, *.key, *.p12, *.pfx); files whose name is "token"/"tokens"/"*.token".

Blocked content: Discord bot token shape, Discord webhook URLs, GM_WEBHOOK_* / *_API_KEY / *_TOKEN / *_SECRET style
assignments with a real-looking value, OpenAI (sk-...), Google (AIza...), GitHub (ghp_/github_pat_), Slack (xox...),
AWS (AKIA...) key shapes and PEM private-key headers.
"""
import argparse
import os
import re
import subprocess
import sys

# ---------------------------------------------------------------- paths
ENV_OK = {".env.example", ".env.sample", ".env.template"}


def forbidden_path(path):
    """Return a short reason string if the repo-relative path must never be committed, else None."""
    p = path.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    p = p.lstrip("/")
    low = p.lower()
    parts = low.split("/")
    base = parts[-1]
    if low.startswith("gm-notes/secret/") or "/gm-notes/secret/" in low or low == "gm-notes/secret":
        return "under gm-notes/secret/"
    if "sessions" in parts[:-1] or "sessions-data" in parts[:-1]:
        return "under sessions/ (live state, ledger, backups)"
    if base == "state.json" and "sessions" in parts:
        return "sessions/state.json"
    if base.startswith("credit-ledger"):
        return "credit-ledger*"
    if base.startswith(".env") and base not in ENV_OK:
        return ".env file"
    if base == "bot.log" or base.endswith(".log"):
        return "log file"
    if "node_modules" in parts[:-1]:
        return "node_modules/"
    if base.endswith((".pem", ".key", ".p12", ".pfx")):
        return "key/cert file"
    if base in ("token", "tokens", "token.txt", "tokens.txt", "token.json", "tokens.json") or base.endswith(".token"):
        return "token file"
    return None


# ---------------------------------------------------------------- content
PLACEHOLDER = re.compile(r"(<[^>]*>|\$\{|\$[A-Za-z_]|%s|\.\.\.|x{4,}|your[-_ ]|example|changeme|redacted|placeholder|"
                         r"os\.environ|process\.env|getenv|\{\{|\bfake\b|\bdummy\b)", re.I)

# (name, regex, value_group or None)
PATTERNS = [
    ("discord-bot-token", re.compile(r"(?<![A-Za-z0-9_-])[MNO][A-Za-z0-9_-]{23,27}\.[A-Za-z0-9_-]{6,7}\.[A-Za-z0-9_-]{27,}(?![A-Za-z0-9_-])"), None),
    ("discord-mfa-token", re.compile(r"(?<![A-Za-z0-9_-])mfa\.[A-Za-z0-9_-]{80,}"), None),
    ("discord-webhook-url", re.compile(r"https?://(?:[a-z0-9-]+\.)?discord(?:app)?\.com/api/(?:v\d+/)?webhooks/\d+/[A-Za-z0-9_-]+", re.I), None),
    ("openai-style-key", re.compile(r"(?<![A-Za-z0-9])sk-(?:proj-|live-|svcacct-)?[A-Za-z0-9_-]{20,}"), None),
    ("google-api-key", re.compile(r"(?<![A-Za-z0-9])AIza[0-9A-Za-z_-]{35}"), None),
    ("github-token", re.compile(r"(?<![A-Za-z0-9])(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})"), None),
    ("slack-token", re.compile(r"(?<![A-Za-z0-9])xox[baprs]-[A-Za-z0-9-]{10,}"), None),
    ("aws-access-key", re.compile(r"(?<![A-Za-z0-9])AKIA[0-9A-Z]{16}(?![A-Za-z0-9])"), None),
    ("private-key-block", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY"), None),
    # NAME=value assignments (env style, JSON "NAME": "value", python NAME = "value")
    ("gm-webhook-assignment", re.compile(r"GM_WEBHOOK\w*[\"']?\s*[=:]\s*[\"']?([^\s\"'<>$%{(),;]{6,})"), 1),
    ("secret-assignment", re.compile(r"(?i)\b[A-Za-z0-9_]*(?:api[_-]?key|secret|token|passwd|password|webhook[_-]?key)[A-Za-z0-9_]*[\"']?\s*[=:]\s*[\"']?([A-Za-z0-9_\-/+=.]{20,})"), 1),
]
BARE_MENTION = re.compile(r"GM_WEBHOOK")


def scan_text(text, strict=False):
    """Return a sorted list of (line_number, pattern_name). Never returns the matched text."""
    hits = set()
    for i, line in enumerate(text.splitlines(), 1):
        if len(line) > 4000:
            line = line[:4000]
        for name, rx, grp in PATTERNS:
            for m in rx.finditer(line):
                if grp is not None:
                    val = m.group(grp)
                    if PLACEHOLDER.search(val):
                        continue
                    if name == "secret-assignment" and not (re.search(r"[A-Za-z]", val) and re.search(r"[0-9]", val)):
                        continue   # words/paths/ids with no letter+digit mix are not key-like
                hits.add((i, name))
        if strict and BARE_MENTION.search(line):
            hits.add((i, "gm-webhook-name-mention(strict)"))
    return sorted(hits)


def scan_bytes(data, strict=False):
    if b"\x00" in data[:8192]:
        return []   # binary: path rules only
    return scan_text(data.decode("utf-8", "replace"), strict=strict)


# ---------------------------------------------------------------- drivers
def _git(args, cwd=None):
    return subprocess.run(["git"] + args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def staged_files(cwd=None):
    r = _git(["diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"], cwd)
    if r.returncode != 0:
        raise RuntimeError("git diff --cached failed: " + r.stderr.decode("utf-8", "replace").strip())
    return [p for p in r.stdout.decode("utf-8", "surrogateescape").split("\0") if p]


def check_staged(cwd=None, strict=False, out=sys.stderr):
    problems = []
    for path in staged_files(cwd):
        why = forbidden_path(path)
        if why:
            problems.append("BLOCKED PATH   %s  (%s)" % (path, why))
            continue
        blob = _git(["show", ":" + path], cwd)
        if blob.returncode != 0:
            continue
        for ln, name in scan_bytes(blob.stdout, strict):
            problems.append("SECRET PATTERN %s:%d  (%s)" % (path, ln, name))
    return report(problems, out)


def check_tree(root, strict=False, out=sys.stderr):
    problems = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != ".git"]
        for f in fn:
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, root)
            why = forbidden_path(rel)
            if why:
                problems.append("BLOCKED PATH   %s  (%s)" % (rel, why))
                continue
            try:
                with open(full, "rb") as fh:
                    data = fh.read()
            except OSError:
                continue
            for ln, name in scan_bytes(data, strict):
                problems.append("SECRET PATTERN %s:%d  (%s)" % (rel, ln, name))
    return report(problems, out)


def report(problems, out):
    if problems:
        out.write("check_repo_safe: FAILED, %d problem(s). Matched text is never printed.\n" % len(problems))
        for p in problems:
            out.write("  " + p + "\n")
        out.write("Unstage/remove the item (git rm --cached <path>) and add it to .gitignore if it is a live file.\n")
        return 1
    out.write("check_repo_safe: OK\n")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--staged", action="store_true", help="check staged files (default)")
    ap.add_argument("--tree", metavar="DIR", help="scan a directory on disk instead")
    ap.add_argument("--strict", action="store_true", help="also fail on bare GM_WEBHOOK name mentions")
    a = ap.parse_args(argv)
    try:
        if a.tree:
            return check_tree(a.tree, a.strict)
        return check_staged(strict=a.strict)
    except RuntimeError as e:
        sys.stderr.write("check_repo_safe: %s\n" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
