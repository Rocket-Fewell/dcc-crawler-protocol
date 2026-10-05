#!/usr/bin/env python3
"""rsync-like FULL mirror into the staging repo (rsync is not installed on the box). Used by backup-push.sh.

Caleb authorized a full backup on 2026-10-04: "i want all files on the github.... everything".
Everything is mirrored EXCEPT: live credentials (.env/.env.*, files matching a credential pattern, listed by name in
CREDENTIAL_EXCLUDES), dependency/cache folders (node_modules, __pycache__, *.pyc, .venv, .git) and files over 50 MB.
Delete-sync: anything in the repo that is no longer in a source is removed (except STAGING_OWNED paths).

ETIQUETTE: /workspace/dcc-campaign/gm-notes/secret/ is copied byte-for-byte and NEVER content-scanned or printed
(it holds GM roll/affinity data, not credentials). Name-based exclusions still apply there.
Sources are only read, never modified.
"""
import fnmatch, importlib.util, io, os, shutil, sys, tarfile
sys.dont_write_bytecode = True   # keep ops/__pycache__ out of the repo

REPO = "/workspace/dcc-repo-staging"

# (source dir, repo-relative destination). Directory symlinks inside sources are followed, so
# dcc-campaign/lore -> /workspace/dcc-lore lands in lore/, dcc-campaign/bot -> discord-voice-bridge lands in bot/,
# and rules/_source-crawler-protocol -> /workspace/crawler-protocol is copied as a folder (git stores duplicates once).
SOURCES = [
    ("/workspace/dcc-campaign", ""),                         # repo root keeps the campaign layout
    ("/workspace/core-book", "core-book"),                  # Core Book manuscript, PDF builds included per Caleb
    ("/workspace/discord-voice-bridge", "discord-voice-bridge"),
    ("/workspace/crawler-protocol", "crawler-protocol"),
    ("/workspace/agent-tools", "agent-tools"),
    ("/workspace/srd", "srd"),
    ("/workspace/backups", "backups"),                      # dcc-campaign/backups is empty today; both merge here
    # unique work found in scratch folders (everything else in the scratch folders is copies/throwaway):
    ("/workspace/tmp/eb", "scratch/tmp-eb"),                # encounter-budget generator gen.py + mkmd.py + versions
    ("/workspace/discord-pass", "scratch/discord-pass"),    # Discord channel snapshot taken before a channel pass
]
SINGLE_FILES = [  # (source file, repo-relative destination)
    ("/workspace/backup-push.sh", "ops/backup-push.sh"),
    ("/workspace/backup-sync.py", "ops/backup-sync.py"),
]
# Files that live only in the staging repo (never deleted by delete-sync, never overwritten by a source file).
STAGING_OWNED = {".gitignore", "README.md", "ops/check_repo_safe.py", "ops/hooks/pre-commit", "ops/README.md"}

# Repo paths kept as git SYMLINKS (repo-relative path -> relative link target) instead of copies of the real file.
# Remote commit 12df0bc (2026-10-05, Cursor cloud agent, co-authored by Caleb) turned these two into symlinks into the
# lore/ mirror so the voice bridge and GM tools see one Lore copy of the item table. On the box,
# dcc-campaign/tables/<name> -> ../../dcc-lore/tables/<name>; without this the mirror would copy real content back.
# A link is only written when its target is part of this sync (lore/tables/<name> is mirrored from /workspace/dcc-lore),
# so it never dangles; otherwise the file falls back to a normal copy with a WARN.
KEEP_SYMLINKS = {
    "tables/item-reskins.json": "../lore/tables/item-reskins.json",
    "tables/item-reskins.version.json": "../lore/tables/item-reskins.version.json",
}

# Top-level names that must never exist in the staging repo. 12df0bc ignores /dcc-campaign/ and /dcc-lore (path aliases
# the Cloud Agent install recreates in ITS checkout); backup-push.sh uses `git add -A --force`, which bypasses
# .gitignore, so the sync refuses to run if they show up here and never writes anything under them.
FORBIDDEN_ROOT_NAMES = {"dcc-campaign", "dcc-lore"}

# Lines that must stay in the staging-owned .gitignore (added by 12df0bc). Re-appended if ever missing.
GITIGNORE_REQUIRED_BLOCK = """
# Path aliases recreated by the Cloud Agent install. The git root is the
# flattened backup; the GM tools and voice bridge still look up
# /workspace/dcc-campaign (decisions, sessions, tools) and /workspace/dcc-lore.
/dcc-campaign/
/dcc-lore
"""

SECRET_SRC = "/workspace/dcc-campaign/gm-notes/secret"   # copy only; never read for scanning, never print names

EXC_DIRS = {"node_modules", "__pycache__", ".venv", ".git"}
EXC_FILE_GLOBS = ["*.pyc", ".env", ".env.*", ".env.agents"]   # .env.* covers .env.example too (literal rule);
# .env.agents (per-agent #agents webhook URLs, 2026-10-05) is listed explicitly as well so it stays out even if .env.* changes
MAX_BYTES = 50 * 1024 * 1024

# Named credential excludes (repo-relative path -> reason). A file lands here when the credential scan / secret grep
# flags it. Never weaken the grep instead.
CREDENTIAL_EXCLUDES = {
    # 2026-10-04: flagged by the generic secret-assignment pattern (PATH_SECRET test fixture for a localhost mock
    # server). Reviewed with the value masked: looks like a test fixture, not a live credential. Excluded per the rule;
    # Caleb can re-include it after review.
    "discord-voice-bridge/test/wake.test.js": "secret-assignment pattern (test fixture, likely false positive)",
    "bot/test/wake.test.js": "secret-assignment pattern (same file via the dcc-campaign/bot symlink)",
    # 2026-10-05: per-agent Discord webhook URLs for #agents (live credentials). Also caught by the .env.* name rule.
    "discord-voice-bridge/.env.agents": "live Discord webhook URLs (agents_channel.py post --as)",
    "bot/.env.agents": "live Discord webhook URLs (same file via the dcc-campaign/bot symlink)",
}

_spec = importlib.util.spec_from_file_location("crs", os.path.join(REPO, "ops", "check_repo_safe.py"))
crs = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(crs)

report = {"name": [], "big": [], "cred_named": [], "cred_auto": [], "secret_name_excluded": 0, "collisions": []}


def in_secret(src_path):
    rp = os.path.realpath(src_path)
    return rp == SECRET_SRC or rp.startswith(SECRET_SRC + os.sep)


def name_excluded(name):
    return any(fnmatch.fnmatch(name, p) for p in EXC_FILE_GLOBS)


def scan_file(src, rel):
    """Return list of pattern names found (never values). Tarballs: members outside gm-notes/secret are scanned."""
    with open(src, "rb") as fh:
        data = fh.read()
    names = {n for _, n in crs.scan_bytes(data)}
    if rel.endswith((".tar.gz", ".tgz", ".tar")):
        try:
            with tarfile.open(fileobj=io.BytesIO(data)) as tf:
                for m in tf.getmembers():
                    base = m.name.split("/")[-1]
                    if "gm-notes/secret" in m.name:
                        if m.isfile() and crs.forbidden_path(m.name):
                            names.add("tar-member-credential-filename")
                        continue
                    if crs.forbidden_path(m.name):
                        names.add("tar-member-credential-filename"); continue
                    if m.isfile() and m.size < MAX_BYTES:
                        names |= {n for _, n in crs.scan_bytes(tf.extractfile(m).read())}
        except tarfile.TarError:
            pass
    return sorted(names)


def build_want():
    want = {}   # repo rel -> source path
    for s0, d0 in SOURCES:
        if not os.path.isdir(s0):
            print("WARN missing source", s0); continue
        seen = set()
        for root, dirs, files in os.walk(s0, followlinks=True):
            real = os.path.realpath(root)
            if real in seen:
                dirs[:] = []; continue
            seen.add(real)
            dirs[:] = sorted(x for x in dirs if x not in EXC_DIRS)
            secret = in_secret(root)
            for f in sorted(files):
                s = os.path.join(root, f)
                rel = os.path.normpath(os.path.join(d0, os.path.relpath(s, s0)))
                if not os.path.exists(s):
                    print("WARN dangling symlink skipped:", rel); continue
                if name_excluded(f):
                    if secret: report["secret_name_excluded"] += 1
                    else: report["name"].append(rel)
                    continue
                if os.path.getsize(s) > MAX_BYTES:
                    report["big"].append((rel if not secret else "gm-notes/secret/<file>", os.path.getsize(s))); continue
                if rel in CREDENTIAL_EXCLUDES:
                    report["cred_named"].append(rel); continue
                if not secret:
                    hits = scan_file(s, rel)
                    if hits:
                        report["cred_auto"].append((rel, hits)); continue
                if rel.split(os.sep)[0] in FORBIDDEN_ROOT_NAMES:
                    print("WARN skipped path under a forbidden root alias:", rel); continue
                if rel in STAGING_OWNED:
                    print("WARN source file ignored, staging repo owns this path:", rel); continue
                if rel in want:
                    if open(want[rel], "rb").read() != open(s, "rb").read():
                        report["collisions"].append(rel)
                    continue
                want[rel] = s
    for s, rel in SINGLE_FILES:
        if os.path.isfile(s):
            hits = scan_file(s, rel)
            if hits: report["cred_auto"].append((rel, hits))
            else: want[rel] = s
    return want


def copy_if_changed(s, d):
    if os.path.isfile(d) and not os.path.islink(d) and os.path.getsize(d) == os.path.getsize(s):
        with open(s, "rb") as a, open(d, "rb") as b:
            if a.read() == b.read():
                return False
    if os.path.islink(d) or os.path.isdir(d):
        shutil.rmtree(d) if os.path.isdir(d) and not os.path.islink(d) else os.remove(d)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)    # follows file symlinks -> real content
    return True


def ensure_symlink(d, target):
    """Make d a symlink to target (relative). Returns True if anything changed."""
    if os.path.islink(d) and os.readlink(d) == target:
        return False
    if os.path.islink(d) or os.path.isfile(d):
        os.remove(d)
    elif os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    os.symlink(target, d)
    return True


def ensure_gitignore_block():
    """Never lose the 12df0bc alias-ignore lines in the staging-owned .gitignore."""
    p = os.path.join(REPO, ".gitignore")
    cur = open(p).read() if os.path.isfile(p) else ""
    need = [l for l in GITIGNORE_REQUIRED_BLOCK.strip().splitlines() if not l.startswith("#")]
    if all(l in cur.splitlines() for l in need):
        return
    with open(p, "a") as fh:
        fh.write(("" if cur.endswith("\n") or not cur else "\n") + GITIGNORE_REQUIRED_BLOCK)
    print("restored .gitignore alias lines (12df0bc)")


def main():
    bad = [n for n in sorted(FORBIDDEN_ROOT_NAMES) if os.path.lexists(os.path.join(REPO, n))]
    if bad:
        # Do not delete-sync into them (could be a bind mount/symlink to live data) and do not let `git add --force` take them.
        sys.exit("STOP: forbidden alias path(s) at staging repo root: %s - remove by hand after checking what they are" % ", ".join(bad))
    want = build_want()
    links = {}
    for rel, target in KEEP_SYMLINKS.items():
        tgt_rel = os.path.normpath(os.path.join(os.path.dirname(rel), target))
        if tgt_rel in want:
            want.pop(rel, None); links[rel] = target
        else:
            print("WARN KEEP_SYMLINKS target %s not mirrored; %s kept as a plain copy" % (tgt_rel, rel))
    changed = sum(copy_if_changed(s, os.path.join(REPO, rel)) for rel, s in want.items())
    changed += sum(ensure_symlink(os.path.join(REPO, rel), t) for rel, t in links.items())
    ensure_gitignore_block()
    deleted = 0
    for root, dirs, files in os.walk(REPO, topdown=True):
        if root == REPO:
            dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), REPO)
            if rel not in want and rel not in STAGING_OWNED and rel not in links:
                os.remove(os.path.join(root, f)); deleted += 1
                if not rel.startswith("gm-notes/secret/"): print("deleted", rel)
    for root, dirs, files in os.walk(REPO, topdown=False):
        if ".git" in os.path.relpath(root, REPO).split(os.sep): continue
        if root != REPO and not os.listdir(root): os.rmdir(root)
    total = sum(os.path.getsize(s) for s in want.values())
    print("mirror: %d files wanted (%.1f MB), %d copied/updated, %d deleted" % (len(want), total / 1e6, changed, deleted))
    for rel, t in links.items(): print("symlink kept (KEEP_SYMLINKS, 12df0bc): %s -> %s" % (rel, t))
    for rel in report["name"]: print("EXCLUDED (.env name rule):", rel)
    if report["secret_name_excluded"]: print("EXCLUDED (.env name rule) inside gm-notes/secret: %d file(s)" % report["secret_name_excluded"])
    for rel, sz in report["big"]: print("EXCLUDED (>50 MB, %.1f MB): %s" % (sz / 1e6, rel))
    for rel in report["cred_named"]: print("EXCLUDED (CREDENTIAL_EXCLUDES: %s): %s" % (CREDENTIAL_EXCLUDES[rel], rel))
    for rel, hits in report["cred_auto"]:
        print("EXCLUDED (credential pattern %s, NOT in CREDENTIAL_EXCLUDES yet - add it): %s" % (",".join(hits), rel))
    for rel in report["collisions"]: print("WARN path collision between sources (first source kept):", rel)


if __name__ == "__main__":
    main()
