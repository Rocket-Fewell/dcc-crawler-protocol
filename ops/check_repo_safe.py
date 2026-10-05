#!/usr/bin/env python3
"""check_repo_safe.py (backup edition): refuse to commit LIVE CREDENTIALS. Nothing else is blocked.

Caleb authorized a full backup on 2026-10-04 ("i want all files on the github.... everything"):
gm-notes/, gm-notes/secret/, sessions/ (state.json, credit-ledger, session.json, backups), player sheets,
logs and exports are ALLOWED. This checker only looks for credentials.

  python3 ops/check_repo_safe.py            # check staged files (same as --staged)
  python3 ops/check_repo_safe.py --staged
  python3 ops/check_repo_safe.py --tree DIR # scan a directory tree on disk

Exit 0 = clean, 1 = credential found, 2 = usage/git error. It NEVER prints a matched value: only path, line, kind.

Blocked paths : .env and .env.* (except .env.example/.sample/.template, which are still content-scanned),
                key/cert files (*.pem, *.key, *.p12, *.pfx), files named token/tokens/*.token.
Blocked content: Discord bot token, Discord webhook URL, GitHub PAT (ghp_/gho_/ghs_/github_pat_), OpenAI-style sk- keys,
                ElevenLabs sk_ keys, FISH/ELEVENLABS/OPENAI/DISCORD key or token assignments, Google/Slack/AWS key
                shapes, PEM private-key blocks, generic *_API_KEY/*_TOKEN/*_SECRET/password assignments with a real value.
Content of gm-notes/secret/ is NOT scanned (GM etiquette: it holds GM roll/affinity data, not credentials; files
are only copied byte-for-byte). Path rules still apply there.
"""
import argparse, os, re, subprocess, sys

ENV_OK = {".env.example", ".env.sample", ".env.template"}
NO_CONTENT_SCAN_PREFIXES = ("gm-notes/secret/",)   # etiquette: never read GM secret notes


def _norm(path):
    p = path.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p.lstrip("/")


def forbidden_path(path):
    """Reason string if the repo-relative path is a credential file by name, else None."""
    base = _norm(path).lower().split("/")[-1]
    if (base == ".env" or base.startswith(".env.")) and base not in ENV_OK:
        return ".env file (live credentials)"
    if base.endswith((".pem", ".key", ".p12", ".pfx")):
        return "key/cert file"
    if base in ("token", "tokens", "token.txt", "tokens.txt", "token.json", "tokens.json") or base.endswith(".token"):
        return "token file"
    return None


def skip_content(path):
    p = _norm(path)
    return any(p.startswith(x) for x in NO_CONTENT_SCAN_PREFIXES)


PLACEHOLDER = re.compile(r"(<[^>]*>|\$\{|\$[A-Za-z_]|%s|\.\.\.|x{4,}|your[-_ ]|example|changeme|redacted|placeholder|"
                         r"os\.environ|process\.env|getenv|\{\{|\bfake\b|\bdummy\b)", re.I)

# (name, regex, value_group or None). Superset of the grep in backup-push.sh.
PATTERNS = [
    ("discord-bot-token", re.compile(r"(?<![A-Za-z0-9_-])[MNO][A-Za-z0-9_-]{23,27}\.[A-Za-z0-9_-]{6,7}\.[A-Za-z0-9_-]{27,}(?![A-Za-z0-9_-])"), None),
    ("discord-bot-token-grep", re.compile(r"[MNO][A-Za-z0-9_-]{23,27}\.[A-Za-z0-9_-]{6,7}\.[A-Za-z0-9_-]{27,}"), None),
    ("discord-mfa-token", re.compile(r"(?<![A-Za-z0-9_-])mfa\.[A-Za-z0-9_-]{80,}"), None),
    ("discord-webhook-url", re.compile(r"discord(?:app)?\.com/api/(?:v[0-9]+/)?webhooks/[0-9]+", re.I), None),
    ("openai-style-key", re.compile(r"sk-[A-Za-z0-9_-]{20,}"), None),
    ("elevenlabs-key", re.compile(r"(?<![A-Za-z0-9])sk_[0-9a-f]{40,}"), None),
    ("github-token", re.compile(r"github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{30,}"), None),
    ("google-api-key", re.compile(r"(?<![A-Za-z0-9])AIza[0-9A-Za-z_-]{35}"), None),
    ("slack-token", re.compile(r"(?<![A-Za-z0-9])xox[baprs]-[A-Za-z0-9-]{10,}"), None),
    ("aws-access-key", re.compile(r"(?<![A-Za-z0-9])AKIA[0-9A-Z]{16}(?![A-Za-z0-9])"), None),
    ("private-key-block", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY"), None),
    ("provider-key-assignment", re.compile(r"(?i)\b(?:FISH|ELEVEN(?:LABS)?|XI|OPENAI|DISCORD)[A-Za-z0-9_]*(?:KEY|TOKEN|SECRET)[\"']?\s*[=:]\s*[\"']?([A-Za-z0-9_\-]{20,})"), 1),
    # GM webhook: only the credential-bearing names (KEY/SECRET/TOKEN/PASS). GM_WEBHOOK_URL/_AUTH_HEADER/_AUTH_SCHEME
    # are config, not credentials; a Discord webhook URL value is still caught by discord-webhook-url above.
    ("gm-webhook-assignment", re.compile(r"GM_WEBHOOK\w*(?:KEY|SECRET|TOKEN|PASS)\w*[\"']?\s*[=:]\s*[\"']?([^\s\"'<>$%{(),;]{6,})"), 1),
    ("secret-assignment", re.compile(r"(?i)\b[A-Za-z0-9_]*(?:api[_-]?key|secret|token|passwd|password|webhook[_-]?key)[A-Za-z0-9_]*[\"']?\s*[=:]\s*[\"']?([A-Za-z0-9_\-/+=.]{20,})"), 1),
]


def scan_text(text):
    """Sorted list of (line_number, pattern_name). Never returns the matched text."""
    hits = set()
    for i, line in enumerate(text.splitlines(), 1):
        if len(line) > 20000:
            line = line[:20000]
        for name, rx, grp in PATTERNS:
            for m in rx.finditer(line):
                if grp is not None:
                    val = m.group(grp)
                    if PLACEHOLDER.search(val):
                        continue
                    if name in ("secret-assignment", "provider-key-assignment") and not (
                            re.search(r"[A-Za-z]", val) and re.search(r"[0-9]", val)):
                        continue   # words/paths/ids with no letter+digit mix are not key-like
                hits.add((i, name))
    return sorted(hits)


def scan_bytes(data):
    if b"\x00" in data[:8192]:
        return []   # binary: path rules only (same as grep -I)
    return scan_text(data.decode("utf-8", "replace"))


def _git(args, cwd=None, inp=None):
    return subprocess.run(["git"] + args, cwd=cwd, input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def staged_files(cwd=None):
    r = _git(["diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"], cwd)
    if r.returncode != 0:
        raise RuntimeError("git diff --cached failed: " + r.stderr.decode("utf-8", "replace").strip())
    return [p for p in r.stdout.decode("utf-8", "surrogateescape").split("\0") if p]


def check_staged(cwd=None, out=sys.stderr):
    problems = []
    for path in staged_files(cwd):
        why = forbidden_path(path)
        if why:
            problems.append("BLOCKED PATH   %s  (%s)" % (path, why)); continue
        if skip_content(path):
            continue
        blob = _git(["show", ":" + path], cwd)
        if blob.returncode != 0:
            continue
        for ln, name in scan_bytes(blob.stdout):
            problems.append("SECRET PATTERN %s:%d  (%s)" % (path, ln, name))
    return report(problems, out)


def check_tree(root, out=sys.stderr):
    problems = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != ".git"]
        for f in fn:
            full = os.path.join(dp, f); rel = os.path.relpath(full, root)
            why = forbidden_path(rel)
            if why:
                problems.append("BLOCKED PATH   %s  (%s)" % (rel, why)); continue
            if skip_content(rel):
                continue
            try:
                with open(full, "rb") as fh:
                    data = fh.read()
            except OSError:
                continue
            for ln, name in scan_bytes(data):
                problems.append("SECRET PATTERN %s:%d  (%s)" % (rel, ln, name))
    return report(problems, out)


def report(problems, out):
    if problems:
        out.write("check_repo_safe: FAILED, %d credential problem(s). Matched text is never printed.\n" % len(problems))
        for p in problems:
            out.write("  " + p + "\n")
        out.write("Add the file to CREDENTIAL_EXCLUDES in ops/backup-sync.py and re-sync.\n")
        return 1
    out.write("check_repo_safe: OK (credentials only; full backup authorized by Caleb 2026-10-04)\n")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--staged", action="store_true", help="check staged files (default)")
    ap.add_argument("--tree", metavar="DIR", help="scan a directory on disk instead")
    a = ap.parse_args(argv)
    try:
        return check_tree(a.tree) if a.tree else check_staged()
    except RuntimeError as e:
        sys.stderr.write("check_repo_safe: %s\n" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
