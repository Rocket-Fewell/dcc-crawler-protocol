#!/usr/bin/env python3
"""rsync-like FULL mirror into the staging repo (rsync is not installed on the box). Used by backup-push.sh.

Caleb authorized a full backup on 2026-10-04: "i want all files on the github.... everything".
Everything is mirrored EXCEPT: live credentials (.env/.env.*, files matching a credential pattern, listed by name in
CREDENTIAL_EXCLUDES), dependency/cache folders (node_modules, __pycache__, *.pyc, .venv, .git), per-machine agents-channel poll cursors/lastseen (RUNTIME_EXCLUDES), and files over 50 MB.
Delete-sync: anything in the repo that is no longer in a source is removed (except STAGING_OWNED paths).

ETIQUETTE: gm-notes/secret/ under the campaign root is copied byte-for-byte and NEVER content-scanned or printed
(it holds GM roll/affinity data, not credentials). Name-based exclusions still apply there.
The mirror only reads sources. `--pull` (below) is the one mode that writes to them.

PULL-FIRST (`backup-sync.py --pull`, run by backup-push.sh before the mirror; Caleb approved 2026-10-05):
GitHub changes since the last commit this backup pushed (marker file) are brought into the live sources so the
mirror does not revert them. Per upstream-changed path, 3-way on content: live == upstream -> nothing; live ==
marker version -> apply upstream to live (old live file backed up first); otherwise CONFLICT. Any CONFLICT or
BLOCKED path stops the whole run before anything is written (exit 3). Protected paths (session state, ledgers,
player sheets, GM secrets, logs, keys) and excluded paths are never written. Then staging fast-forwards to
origin/main. DRY_RUN=1 prints the plan only.
OWN rule (2026-10-05, branch-mode backup, decision 035): the nightly now pushes to branch backup/nightly and a PR merges
it into main, so main's changes since the marker include this backup's OWN branch content. A path whose GitHub version
(mode + blob) equals the version in the branch head this backup last pushed (DCC_BACKUP_BRANCH_MARKER, default
<box>/.backup-last-branch-sha) is not a GitHub edit: live is kept (category OWN), the mirror carries live onward,
nothing is written to live. Missing/invalid branch marker = rule off (more CONFLICTs, never fewer).

Paths: a fresh checkout runs this file from ops/ and reads the checkout (DCC_BACKUP_REPO /
DCC_CAMPAIGN_ROOT override). The box copy that lives outside the repo defaults to the live trees under
DCC_BOX_ROOT (default /workspace). Those box paths are not used when this file is the ops/ copy.
"""
import fnmatch, hashlib, importlib.util, io, os, shutil, subprocess, sys, tarfile, time
sys.dont_write_bytecode = True   # keep ops/__pycache__ out of the repo

_HERE = os.path.dirname(os.path.abspath(__file__))
_IN_REPO = os.path.basename(_HERE) == "ops" and os.path.isfile(os.path.join(_HERE, "check_repo_safe.py"))
BOX = os.environ.get("DCC_BOX_ROOT") or "/workspace"   # box copy only

if os.environ.get("DCC_BACKUP_REPO"):
    REPO = os.environ["DCC_BACKUP_REPO"]
elif _IN_REPO:
    REPO = os.path.dirname(_HERE)
else:
    REPO = os.path.join(BOX, "dcc-repo-staging")   # box copy of this script, outside the checkout

CAMP = os.environ.get("DCC_CAMPAIGN_ROOT") or os.environ.get("DCC_CAMPAIGN_DIR")
if not CAMP:
    CAMP = REPO if _IN_REPO else os.path.join(BOX, "dcc-campaign")


def _src(repo_rel, box_rel):
    """Repo-relative when this file is ops/backup-sync.py. Box path (under BOX) only for the outside copy."""
    if _IN_REPO:
        return os.path.join(REPO, repo_rel)
    return os.path.join(BOX, box_rel)


# (source dir, repo-relative destination). Directory symlinks inside sources are followed, so
# a campaign lore/ symlink lands in lore/, bot/ lands in bot/ when the source is the live tree,
# and rules/_source-crawler-protocol is copied as a folder (git stores duplicates once).
SOURCES = [
    (CAMP, ""),                                              # repo root keeps the campaign layout
    (_src("core-book", "core-book"), "core-book"),
    (_src("discord-voice-bridge", "discord-voice-bridge"), "discord-voice-bridge"),
    (_src("crawler-protocol", "crawler-protocol"), "crawler-protocol"),
    # agent-tools/ dropped Oct 6 2026 (Caleb): raw tool dumps, incl. inbox listings - not campaign content.
    (_src("srd", "srd"), "srd"),
    (os.environ["DCC_BACKUP_DIR"] if _IN_REPO and os.environ.get("DCC_BACKUP_DIR") else _src("backups", "backups"), "backups"),
    # unique work found in scratch folders (everything else in the scratch folders is copies/throwaway):
    (_src("scratch/tmp-eb", "tmp/eb"), "scratch/tmp-eb"),
    (_src("scratch/discord-pass", "discord-pass"), "scratch/discord-pass"),
]
if _IN_REPO:
    SINGLE_FILES = [  # already in the checkout; keep them in the wanted set so delete-sync leaves them
        (os.path.join(_HERE, "backup-push.sh"), "ops/backup-push.sh"),
        (os.path.join(_HERE, "backup-sync.py"), "ops/backup-sync.py"),
    ]
else:
    SINGLE_FILES = [
        (os.environ.get("DCC_BACKUP_PUSH") or os.path.join(BOX, "backup-push.sh"), "ops/backup-push.sh"),
        (os.environ.get("DCC_BACKUP_SYNC") or os.path.join(BOX, "backup-sync.py"), "ops/backup-sync.py"),
    ]

# Pull-first state (box copy only; both live outside every mirrored source).
MARKER = os.environ.get("DCC_BACKUP_MARKER") or os.path.join(BOX, ".backup-last-synced-sha")
BRANCH_MARKER = os.environ.get("DCC_BACKUP_BRANCH_MARKER") or os.path.join(BOX, ".backup-last-branch-sha")
PULL_BAK = os.environ.get("DCC_PULL_BAK_DIR") or os.path.join(BOX, "backup-pull-bak")
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

# Per-machine #agents poll cursors / lastseen (runtime; changes often). backup-sync excludes these.
lore/state/agents-channel-last.txt
sessions/agents-channel-*.txt
sessions/agents-channel-*.lastseen
sessions-data/*/agents-channel-*.txt
sessions-data/*/agents-channel-*.lastseen
"""

SECRET_SRC = os.path.join(CAMP, "gm-notes", "secret")   # copy only; never read for scanning, never print names

EXC_DIRS = {"node_modules", "__pycache__", ".venv", ".git"}
EXC_FILE_GLOBS = ["*.pyc", ".env", ".env.*", ".env.agents"]   # .env.* covers .env.example too (literal rule);
# .env.agents (per-agent #agents webhook URLs, 2026-10-05) is listed explicitly as well so it stays out even if .env.* changes
MAX_BYTES = 50 * 1024 * 1024

# Per-machine routine state (agents_channel poll cursors / lastseen). Changes every ~15 min on the box; not campaign
# design. Matched as repo-relative paths (fnmatch). Box copies are left alone; delete-sync drops them from the repo.
RUNTIME_EXCLUDES = [
    "lore/state/agents-channel-last.txt",
    "sessions/agents-channel-*.txt",
    "sessions/agents-channel-*.lastseen",
    "sessions-data/*/agents-channel-*.txt",
    "sessions-data/*/agents-channel-*.lastseen",
]

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

report = {"name": [], "big": [], "cred_named": [], "cred_auto": [], "runtime": [], "secret_name_excluded": 0, "collisions": []}


def in_secret(src_path):
    rp = os.path.realpath(src_path)
    return rp == SECRET_SRC or rp.startswith(SECRET_SRC + os.sep)


def name_excluded(name):
    return any(fnmatch.fnmatch(name, p) for p in EXC_FILE_GLOBS)


def runtime_excluded(rel):
    return any(fnmatch.fnmatch(rel, p) for p in RUNTIME_EXCLUDES)


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
            skip = set(EXC_DIRS)
            if os.path.realpath(s0) == os.path.realpath(REPO):
                skip |= FORBIDDEN_ROOT_NAMES
            dirs[:] = sorted(x for x in dirs if x not in skip)
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
                if runtime_excluded(rel):
                    report.setdefault("runtime", []).append(rel)
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


def mirror_main():
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
            dirs[:] = [d for d in dirs if d != ".git" and d not in FORBIDDEN_ROOT_NAMES]
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
    for rel in report["runtime"]: print("EXCLUDED (runtime poll state):", rel)
    if report["secret_name_excluded"]: print("EXCLUDED (.env name rule) inside gm-notes/secret: %d file(s)" % report["secret_name_excluded"])
    for rel, sz in report["big"]: print("EXCLUDED (>50 MB, %.1f MB): %s" % (sz / 1e6, rel))
    for rel in report["cred_named"]: print("EXCLUDED (CREDENTIAL_EXCLUDES: %s): %s" % (CREDENTIAL_EXCLUDES[rel], rel))
    for rel, hits in report["cred_auto"]:
        print("EXCLUDED (credential pattern %s, NOT in CREDENTIAL_EXCLUDES yet - add it): %s" % (",".join(hits), rel))
    for rel in report["collisions"]: print("WARN path collision between sources (first source kept):", rel)



# ------------------------------------------------------------------ pull-first (box copy only) ---------------------
# Repo paths the pull never writes to live, even when GitHub changed them (fnmatch on the repo-relative path and on
# the real path behind any symlink). If GitHub changed one and live does not already match, the path is BLOCKED and
# the whole run stops, so the mirror cannot quietly revert GitHub either. Caleb decides.
PULL_PROTECTED = [
    ("sessions/*", "live session state"),
    ("sessions-data/*", "live session state / ledgers"),
    ("characters/*", "player sheets"),
    ("gm-notes/secret/*", "GM secrets"),
    ("lore/state/*", "Lore runtime state"),
    ("bot/logs/*", "bot runtime logs"),
    ("discord-voice-bridge/logs/*", "bot runtime logs"),
    ("*.log", "runtime log"),
    ("*ledger*.jsonl", "ledger"),
]
# Design docs under characters/ (not player sheets): pulled under the normal rules.
PULL_PROTECTED_ALLOW = ["characters/INDEX.md", "characters/character-creation-5e.md",
                        "characters/create-flow-spec-5e.md", "characters/_archive/*"]
EXIT_CONFLICT = 3   # CONFLICT / BLOCKED: nothing written to live, staging not moved, nothing pushed
EXIT_STOP = 4       # cannot pull safely (marker missing, history rewritten, staging diverged, ...)
CAT_ORDER = ["CONFLICT", "BLOCKED", "KEPT", "APPLY", "NOOP", "OWN", "STAGING", "DROPPED"]


def _git(*args, check=True):
    r = subprocess.run(["git", "-C", REPO] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), r.stderr.decode(errors="replace").strip()))
    return r


def _gits(*args):
    return _git(*args).stdout.decode().strip()


def _is_ancestor(a, b):
    return _git("merge-base", "--is-ancestor", a, b, check=False).returncode == 0


_OBJ_FMT = []


def _blob_id(data):
    if not _OBJ_FMT:
        r = _git("rev-parse", "--show-object-format", check=False)
        _OBJ_FMT.append(r.stdout.decode().strip() if r.returncode == 0 else "sha1")
    h = hashlib.sha256() if _OBJ_FMT[0] == "sha256" else hashlib.sha1()
    h.update(b"blob %d\0" % len(data)); h.update(data)
    return h.hexdigest()


def _blob(sha):
    return _git("cat-file", "blob", sha).stdout


def _shown(rel):
    return "gm-notes/secret/<file>" if rel.startswith("gm-notes/secret/") else rel   # never print secret names


def live_path_for(rel):
    """Live file the mirror reads for repo path rel (same source order as the mirror walk), or None."""
    for s, r in SINGLE_FILES:
        if r == rel:
            return s
    cands = []
    for s0, d0 in SOURCES:
        if d0 == "":
            sub = rel
        elif rel.startswith(d0 + "/"):
            sub = rel[len(d0) + 1:]
        else:
            continue
        cands.append((len(d0), os.path.join(s0, sub)))
    if not cands:
        return None
    for _, p in cands:                       # existing file: first source wins, like the mirror
        if os.path.lexists(p):
            return p
    for _, p in cands:                       # new file: first source whose folder already exists
        if os.path.isdir(os.path.dirname(p)):
            return p
    return max(cands, key=lambda c: c[0])[1]  # new folder: the most specific source


def _camp_links():
    out = []
    if os.path.isdir(CAMP):
        for e in os.scandir(CAMP):
            if e.is_symlink() and os.path.isdir(e.path):
                out.append((os.path.realpath(e.path), e.name))
    return out


def _allowed_roots():
    roots = {os.path.realpath(s0) for s0, _ in SOURCES if os.path.isdir(s0)}
    roots |= {r for r, _ in _camp_links()}
    return roots


def _within(path, roots):
    rp = os.path.realpath(path)
    return any(rp == r or rp.startswith(r + os.sep) for r in roots)


def _canon_rels(rel, live):
    """rel plus the repo-relative names of the real file behind it (so a symlinked alias cannot dodge a rule)."""
    out = {rel}
    rp = os.path.realpath(live)
    pairs = [(os.path.realpath(s0), d0) for s0, d0 in SOURCES] + _camp_links()
    for r0, d0 in pairs:
        if rp.startswith(r0 + os.sep):
            out.add(os.path.normpath(os.path.join(d0, os.path.relpath(rp, r0))))
    return out


def protected_reason(rel, live):
    for c in _canon_rels(rel, live):
        if any(fnmatch.fnmatch(c, a) for a in PULL_PROTECTED_ALLOW):
            continue
        for pat, why in PULL_PROTECTED:
            if fnmatch.fnmatch(c, pat):
                return why
    return None


def excluded_reason(rel):
    """Why the mirror leaves rel out of the repo (so the pull must not write it to live either), or None."""
    parts = rel.split("/")
    if parts[0] in FORBIDDEN_ROOT_NAMES:
        return "forbidden root alias"
    if any(p in EXC_DIRS for p in parts[:-1]):
        return "dependency/cache folder"
    if name_excluded(parts[-1]):
        return ".env name rule"
    if runtime_excluded(rel):
        return "runtime poll state"
    if rel in CREDENTIAL_EXCLUDES:
        return "CREDENTIAL_EXCLUDES"
    return crs.forbidden_path(rel)


def _live_id(p):
    if not os.path.lexists(p):
        return None, None
    if os.path.isdir(p):
        return "DIR", None
    if not os.path.exists(p):
        return "DANGLING", None
    with open(p, "rb") as fh:
        return _blob_id(fh.read()), bool(os.stat(p).st_mode & 0o100)


def _diff_raw(a, b):
    out = _git("diff", "--raw", "--no-renames", "--no-abbrev", "-z", a, b).stdout.decode("utf-8", "surrogateescape")
    toks = out.split("\0")
    items, i = [], 0
    while i < len(toks) - 1:
        meta = toks[i]
        if not meta.startswith(":"):
            i += 1; continue
        om, nm, osha, nsha, st = meta[1:].split()
        items.append({"rel": toks[i + 1], "omode": om, "nmode": nm, "osha": osha, "nsha": nsha, "st": st[0]})
        i += 2
    return items


def _own_tree():
    """{rel: (mode, sha)} of the branch head this backup last pushed (OWN rule), or None when the marker is unusable."""
    if not os.path.isfile(BRANCH_MARKER):
        return None, None
    sha = open(BRANCH_MARKER).read().strip()
    if not sha or _git("cat-file", "-e", sha + "^{commit}", check=False).returncode:
        print("PULL: WARN branch marker %s (%r) is not a commit here; OWN rule off" % (BRANCH_MARKER, sha))
        return None, None
    sha = _gits("rev-parse", sha + "^{commit}")
    out = _git("ls-tree", "-r", "-z", "--full-tree", sha).stdout.decode("utf-8", "surrogateescape")
    tree = {}
    for e in out.split("\0"):
        if "\t" in e:
            meta, rel = e.split("\t", 1)
            mode, _typ, osha = meta.split()
            tree[rel] = (mode, osha)
    return sha, tree


def _dirty_paths():
    out = _git("status", "--porcelain=v1", "-z", "--no-renames", "--untracked-files=all").stdout.decode("utf-8", "surrogateescape")
    return {e[3:] for e in out.split("\0") if len(e) > 3}


def _set_mode(path, exec_bit, new):
    old = 0o644 if new else os.stat(path).st_mode & 0o7777
    mode = old | ((old & 0o444) >> 2) if exec_bit else old & ~0o111
    os.chmod(path, mode)


def _write_live(live, data, exec_bit):
    target = os.path.realpath(live) if os.path.islink(live) else live
    os.makedirs(os.path.dirname(target), exist_ok=True)
    new = not os.path.exists(target)
    tmp = "%s.pull-tmp-%d" % (target, os.getpid())
    with open(tmp, "wb") as fh:
        fh.write(data)
    if not new:
        shutil.copymode(target, tmp)
    _set_mode(tmp, exec_bit, new)
    os.replace(tmp, target)   # new inode: a running copy of backup-push.sh keeps reading its old file


def pull_main():
    dry = bool(os.environ.get("DRY_RUN"))
    tag = "DRY_RUN " if dry else ""

    def stop(msg):
        print("PULL STOP: " + msg)
        print("PULL-RESULT: STOP")
        return EXIT_STOP

    if _IN_REPO:
        return stop("--pull is for the box copy of backup-sync.py (outside the repo). In a checkout use git pull.")
    if not os.path.isfile(MARKER):
        return stop("marker file %s is missing. Set it to the last commit this backup pushed, after checking live "
                    "matches it (normally: git -C %s rev-parse HEAD > %s)." % (MARKER, REPO, MARKER))
    marker = open(MARKER).read().strip()
    if not marker or _git("cat-file", "-e", marker + "^{commit}", check=False).returncode:
        return stop("marker %r (%s) is not a commit in %s" % (marker, MARKER, REPO))
    marker = _gits("rev-parse", marker + "^{commit}")
    r = _git("rev-parse", "--verify", "-q", "refs/remotes/origin/main^{commit}", check=False)
    if r.returncode:
        return stop("refs/remotes/origin/main is missing; fetch origin main first")
    up = r.stdout.decode().strip()
    head = _gits("rev-parse", "HEAD")
    if not _is_ancestor(marker, up):
        return stop("origin/main %s does not contain the marker %s (history rewritten upstream?). Nothing done."
                    % (up[:12], marker[:12]))
    if head == up or _is_ancestor(up, head):
        ff = None
    elif _is_ancestor(head, up):
        ff = up
    else:
        return stop("staging HEAD %s and origin/main %s have diverged; a fast-forward is impossible. Nothing done."
                    % (head[:12], up[:12]))
    keep_live = set(os.environ.get("DCC_PULL_KEEP_LIVE", "").replace(",", " ").split())
    print("PULL: marker %s -> origin/main %s (staging HEAD %s)" % (marker[:12], up[:12], head[:12]))
    own_sha, own = _own_tree()
    if own_sha:
        print("PULL: OWN rule base = last pushed branch head %s" % own_sha[:12])

    roots = _allowed_roots()
    single = {s for s, _ in SINGLE_FILES}
    plan = []
    for it in (_diff_raw(marker, up) if marker != up else []):
        rel = it["rel"]
        it.update(cat=None, why="", live=None, live_x=None)
        it["up_id"] = None if it["nmode"] == "000000" else it["nsha"]
        it["base_id"] = None if it["omode"] == "000000" else it["osha"]
        it["up_x"] = it["nmode"] == "100755"
        ex = excluded_reason(rel)
        if rel in STAGING_OWNED:
            it["cat"], it["why"] = "STAGING", "staging-owned; fast-forward only"
        elif ex:
            it["cat"], it["why"] = "DROPPED", "excluded by the mirror (%s); not written to live, the mirror leaves it out of the repo" % ex
        elif {it["omode"], it["nmode"]} & {"120000", "160000"}:
            if rel in KEEP_SYMLINKS and it["nmode"] == "120000" and _blob(it["nsha"]).decode(errors="replace") == KEEP_SYMLINKS[rel]:
                it["cat"], it["why"] = "NOOP", "KEEP_SYMLINKS link"
            else:
                it["cat"], it["why"] = "BLOCKED", "git symlink/submodule entry; the mirror controls these"
        else:
            live = it["live"] = live_path_for(rel)
            if live is None:
                it["cat"], it["why"] = "BLOCKED", "no live source for this path"
            elif live not in single and not _within(live, roots):
                it["cat"], it["why"] = "BLOCKED", "maps outside the live trees"
            else:
                lid, lx = _live_id(live)
                it["live_x"] = lx
                prot = protected_reason(rel, live)
                hits = sorted({n for _, n in crs.scan_bytes(_blob(it["nsha"]))}) if it["up_id"] and not prot and lid != it["up_id"] else []
                if lid in ("DIR", "DANGLING"):
                    it["cat"], it["why"] = "CONFLICT", "live path is a folder or a dangling symlink"
                elif lid == it["up_id"]:
                    it["cat"], it["why"] = "NOOP", "live already matches GitHub"
                elif own is not None and own.get(rel) == ((it["nmode"], it["nsha"]) if it["up_id"] else None):
                    it["cat"], it["why"] = "OWN", "GitHub has this backup's own branch version; live changed since, live kept"
                elif prot:
                    it["cat"], it["why"] = "BLOCKED", "protected (%s): never written by the pull; GitHub changed it and live differs" % prot
                elif it["up_id"] and int(_gits("cat-file", "-s", it["nsha"])) > MAX_BYTES:
                    it["cat"], it["why"] = "DROPPED", "over 50 MB; the mirror leaves it out"
                elif hits:
                    it["cat"], it["why"] = "BLOCKED", "credential pattern in the GitHub version (%s)" % ",".join(hits)
                elif lid == it["base_id"]:
                    it["cat"] = "APPLY"
                    it["why"] = {"A": "add", "D": "delete"}.get(it["st"], "update")
                else:
                    it["cat"], it["why"] = "CONFLICT", "live changed since the marker and differs from GitHub"
        plan.append(it)

    # Two repo paths, one live file (bot/ is discord-voice-bridge/ on the box): GitHub versions must agree.
    groups = {}
    for it in plan:
        if it["cat"] in ("APPLY", "NOOP") and it["live"]:
            groups.setdefault(os.path.realpath(it["live"]), []).append(it)
    for its in groups.values():
        if len(its) > 1 and len({i["up_id"] for i in its}) > 1:
            for i in its:
                i["cat"] = "CONFLICT"
                i["why"] = "same live file as %s; GitHub versions differ" % ", ".join(_shown(j["rel"]) for j in its if j is not i)

    for it in plan:
        if any(fnmatch.fnmatch(it["rel"], k) for k in keep_live) and it["cat"] in ("APPLY", "CONFLICT", "BLOCKED"):
            it["why"] = "DCC_PULL_KEEP_LIVE: live kept, the mirror will put the live version on GitHub (was %s: %s)" % (it["cat"], it["why"])
            it["cat"] = "KEPT"

    # Staging paths the fast-forward touches that hold uncommitted mirror output (e.g. from a DRY_RUN).
    dirty_touch = set()
    if ff:
        touched = set(_gits("diff", "--name-only", "--no-renames", head, up).splitlines())
        dirty_touch = touched & _dirty_paths()
        for p in sorted(dirty_touch & STAGING_OWNED):
            plan.append({"rel": p, "st": "M", "cat": "BLOCKED", "why": "staging has an uncommitted edit to this staging-owned file"})

    by = {c: [i for i in plan if i["cat"] == c] for c in CAT_ORDER}
    held = dry or bool(by["CONFLICT"] or by["BLOCKED"])
    for c in CAT_ORDER:
        for i in by[c]:
            shown_c = "WOULD-APPLY" if c == "APPLY" and held else c
            print("%s%-8s %s %s  (%s)" % (tag, shown_c, i["st"], _shown(i["rel"]), i["why"]))
    lore = [i["rel"] for i in by["APPLY"] if i["rel"].startswith("lore/")]
    lore_noop = [i["rel"] for i in by["NOOP"] if i["rel"].startswith("lore/")]
    if lore or lore_noop:
        print("LORE: GitHub changed %d lore/ path(s) (%d %sapplied, %d already matched). Tell Lore:"
              % (len(lore) + len(lore_noop), len(lore), "to be " if dry else "", len(lore_noop)))
        for rel in lore + lore_noop:
            print("LORE:   " + rel)
    counts = " ".join("%s=%d" % (c.lower(), len(by[c])) for c in CAT_ORDER)
    if not plan:
        print("PULL: nothing changed on GitHub since the marker")
    blocking = by["CONFLICT"] + by["BLOCKED"]
    if blocking:
        print("CONFLICT: %d path(s) above need Caleb (CONFLICT = GitHub and live both changed; BLOCKED = the pull may not "
              "write it). Nothing was written to live, staging was not fast-forwarded, nothing will be pushed." % len(blocking))
        print("CONFLICT: fix by making each live file the version you want (GitHub's: git -C %s show origin/main:<path>), "
              "then re-run; or keep live with DCC_PULL_KEEP_LIVE=\"<path or glob> ...\" for one run (the backup then overwrites GitHub's version)." % REPO)
        print("PULL-RESULT: CONFLICT %s" % counts)
        return EXIT_CONFLICT
    if dry:
        if ff:
            print("DRY_RUN: would fast-forward staging %s -> %s%s" % (head[:12], up[:12],
                  " (after resetting %d uncommitted mirror path(s) it touches)" % len(dirty_touch) if dirty_touch else ""))
        print("DRY_RUN: nothing written to live, staging not moved")
        print("PULL-RESULT: DRY-RUN %s" % counts)
        return 0

    if by["APPLY"]:
        bak = os.path.join(PULL_BAK, time.strftime("%Y%m%d-%H%M%S"))
        os.makedirs(bak, exist_ok=True)
        for i in by["APPLY"]:
            if os.path.isfile(i["live"]):
                d = os.path.join(bak, "files", i["rel"])
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(i["live"], d)
        with open(os.path.join(bak, "PULL-REPORT.txt"), "w") as fh:
            fh.write("marker %s -> origin/main %s\n" % (marker, up))
            for c in CAT_ORDER:
                for i in by[c]:
                    fh.write("%-8s %s %s -> %s  (%s)\n" % (c, i["st"], _shown(i["rel"]), i.get("live") or "-", i["why"]))
        for i in by["APPLY"]:
            if i["up_id"] is None:
                os.remove(i["live"])
            else:
                data = _blob(i["nsha"])
                if _blob_id(data) != i["nsha"]:
                    raise RuntimeError("blob check failed for " + _shown(i["rel"]))
                _write_live(i["live"], data, i["up_x"])
        print("PULL: applied %d path(s) to live; previous live files in %s" % (len(by["APPLY"]), bak))
    for i in by["NOOP"]:   # content already matches; carry GitHub's exec bit so the mirror does not flip it back
        if i.get("live") and i.get("up_id") and i.get("live_x") is not None and i["live_x"] != i["up_x"] \
                and not protected_reason(i["rel"], i["live"]):
            _set_mode(os.path.realpath(i["live"]), i["up_x"], False)
            print("PULL: exec bit set to GitHub's on " + _shown(i["rel"]))
    if ff:
        for p in sorted(dirty_touch - STAGING_OWNED):
            if _git("cat-file", "-e", "HEAD:" + p, check=False).returncode == 0:
                _git("checkout", "-q", "HEAD", "--", p)
            else:
                _git("rm", "-q", "--cached", "--ignore-unmatch", "--", p)
                fp = os.path.join(REPO, p)
                if os.path.lexists(fp) and not os.path.isdir(fp):
                    os.remove(fp)
        r = _git("merge", "--ff-only", "-q", up, check=False)
        if r.returncode:
            print("PULL STOP: fast-forward failed: " + r.stderr.decode(errors="replace").strip())
            print("PULL-RESULT: STOP (live was already updated; see %s)" % PULL_BAK)
            return EXIT_STOP
        print("PULL: staging fast-forwarded %s -> %s" % (head[:12], up[:12]))
    print("PULL-RESULT: OK %s" % counts)
    return 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["--pull"]:
        sys.exit(pull_main())
    mirror_main()
