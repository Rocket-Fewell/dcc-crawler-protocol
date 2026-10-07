"""Nightly mirror keeps tracked core-book/build/ when the live tree dropped it.

Run: PYTHONPATH=tools python3 -m unittest tools.tests.test_backup_preserve_build
The mirror under test is a copy of ops/backup-sync.py placed outside ops/, so it takes
the box-copy path (live trees separate from the staging repo).
"""
import importlib.util
import os
import shutil
import stat
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SYNC_SRC = os.path.join(ROOT, "ops", "backup-sync.py")
CHECK_SRC = os.path.join(ROOT, "ops", "check_repo_safe.py")


def _load_sync():
    spec = importlib.util.spec_from_file_location("backup_sync_under_test", SYNC_SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _git(repo, *args):
    r = subprocess.run(
        ["git", "-C", repo, "-c", "user.name=Backup Test", "-c", "user.email=backup-test@example.com", *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        raise AssertionError("git %s failed: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def _write(path, text, mode=0o644):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.chmod(path, mode)


def _run_mirror(box, staging, campaign):
    script = os.path.join(box, "backup-sync.py")
    shutil.copy(SYNC_SRC, script)
    env = os.environ.copy()
    env["DCC_BOX_ROOT"] = box
    env["DCC_BACKUP_REPO"] = staging
    env["DCC_CAMPAIGN_ROOT"] = campaign
    for key in ("DCC_BACKUP_DIR", "DCC_CAMPAIGN_DIR", "DCC_BACKUP_SYNC", "DCC_BACKUP_PUSH", "DRY_RUN"):
        env.pop(key, None)
    r = subprocess.run(["python3", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    return r


class PreserveCoreBookBuildTests(unittest.TestCase):
    def test_prefix_is_core_book_build(self):
        mod = _load_sync()
        self.assertIn("core-book/build/", mod.PRESERVE_IF_SOURCE_MISSING)

    def test_gap_in_live_tree_keeps_main_blobs_and_still_deletes_other_files(self):
        """backup/nightly already deleted build/; origin/main still has it; live source lacks it."""
        with tempfile.TemporaryDirectory() as tmp:
            box = os.path.join(tmp, "box")
            staging = os.path.join(tmp, "staging")
            campaign = os.path.join(tmp, "campaign")
            os.makedirs(box)
            os.makedirs(staging)
            _git(staging, "init", "-b", "main")
            os.makedirs(os.path.join(staging, "ops"))
            shutil.copy(CHECK_SRC, os.path.join(staging, "ops", "check_repo_safe.py"))
            _write(os.path.join(staging, "core-book", "build", "build.py"), "FROM_MAIN\n", 0o755)
            _write(os.path.join(staging, "core-book", "build", "pages.json"), "{}\n")
            _write(os.path.join(staging, "core-book", "build", ".env"), "placeholder=1\n")
            _write(os.path.join(staging, "notes", "only-main.md"), "only on main\n")
            _write(os.path.join(staging, "stray.txt"), "stray\n")
            _git(staging, "add", "-A")
            _git(staging, "commit", "-m", "main has build")
            mode = _git(staging, "ls-tree", "HEAD", "core-book/build/build.py").split()[0]
            self.assertEqual(mode, "100755", _git(staging, "ls-tree", "HEAD", "core-book/build/build.py"))
            _git(staging, "update-ref", "refs/remotes/origin/main", "HEAD")
            _git(staging, "checkout", "-b", "backup/nightly")
            _git(staging, "rm", "-r", "core-book/build", "notes/only-main.md")
            _git(staging, "commit", "-m", "nightly deleted build")
            _write(os.path.join(staging, "core-book", "build", "scratch.txt"), "scratch\n")
            _write(os.path.join(box, "core-book", "README.md"), "live-readme\n")
            _write(os.path.join(campaign, "rules", "from-campaign.md"), "camp\n")

            r = _run_mirror(box, staging, campaign)
            self.assertEqual(r.returncode, 0, r.stdout + "\n" + r.stderr)
            out = r.stdout
            self.assertIn("preserved (missing from live source, kept refs/remotes/origin/main): core-book/build/build.py", out)
            self.assertIn("preserved (missing from live source, kept refs/remotes/origin/main): core-book/build/pages.json", out)
            self.assertNotIn("core-book/build/.env", out)
            self.assertIn("deleted stray.txt", out)
            self.assertIn("deleted core-book/build/scratch.txt", out)
            self.assertNotIn("notes/only-main.md", out)

            build_py = os.path.join(staging, "core-book", "build", "build.py")
            with open(build_py, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "FROM_MAIN\n")
            self.assertEqual(stat.S_IMODE(os.stat(build_py).st_mode), 0o755)
            with open(os.path.join(staging, "core-book", "build", "pages.json"), encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "{}\n")
            self.assertEqual(stat.S_IMODE(os.stat(os.path.join(staging, "core-book", "build", "pages.json")).st_mode), 0o644)
            self.assertFalse(os.path.exists(os.path.join(staging, "core-book", "build", ".env")))
            self.assertFalse(os.path.exists(os.path.join(staging, "core-book", "build", "scratch.txt")))
            self.assertFalse(os.path.exists(os.path.join(staging, "notes", "only-main.md")))
            self.assertFalse(os.path.exists(os.path.join(staging, "stray.txt")))
            with open(os.path.join(staging, "core-book", "README.md"), encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "live-readme\n")
            with open(os.path.join(staging, "rules", "from-campaign.md"), encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "camp\n")

    def test_live_file_wins_and_missing_sibling_is_kept_from_head(self):
        with tempfile.TemporaryDirectory() as tmp:
            box = os.path.join(tmp, "box")
            staging = os.path.join(tmp, "staging")
            campaign = os.path.join(tmp, "campaign")
            os.makedirs(box)
            os.makedirs(staging)
            os.makedirs(campaign)
            _git(staging, "init", "-b", "main")
            os.makedirs(os.path.join(staging, "ops"))
            shutil.copy(CHECK_SRC, os.path.join(staging, "ops", "check_repo_safe.py"))
            _write(os.path.join(staging, "core-book", "build", "build.py"), "GIT\n", 0o755)
            _write(os.path.join(staging, "core-book", "build", "pages.json"), "GITJSON\n")
            _git(staging, "add", "-A")
            _git(staging, "commit", "-m", "tracked build")
            _git(staging, "update-ref", "refs/remotes/origin/main", "HEAD")
            _write(os.path.join(box, "core-book", "build", "build.py"), "LIVE\n")

            r = _run_mirror(box, staging, campaign)
            self.assertEqual(r.returncode, 0, r.stdout + "\n" + r.stderr)
            self.assertNotIn("core-book/build/build.py", r.stdout)
            self.assertIn("preserved (missing from live source, already HEAD): core-book/build/pages.json", r.stdout)
            with open(os.path.join(staging, "core-book", "build", "build.py"), encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "LIVE\n")
            with open(os.path.join(staging, "core-book", "build", "pages.json"), encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "GITJSON\n")


if __name__ == "__main__":
    unittest.main()
