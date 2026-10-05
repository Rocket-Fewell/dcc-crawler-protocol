#!/usr/bin/env python3
"""Snapshot the campaign data (characters, sessions, state, decisions, gm-notes) to a timestamped tar.gz.

Usage: python3 tools/snapshot.py [--label after-intake] [--keep 60]
Writes to $DCC_BACKUP_DIR (default: <campaign-parent>/backups/dcc-campaign, mode 700).
Includes sessions-data/ (every non-alpha session) and gm-notes/secret/ (incl. per-session secrets) (the backup folder is private); never copy these archives into shared folders.
Also writes a player-safe CSV-free summary line to stdout (file count and size only).
"""
import argparse, os, re, tarfile, time
import dcc_paths as _paths  # noqa: E402
ROOT = str(_paths.campaign_root())
DEST = os.environ.get("DCC_BACKUP_DIR") or str(_paths.campaign_root().parent / "backups" / "dcc-campaign")
INCLUDE = ["characters", "sessions", "sessions-data", "decisions", "gm-notes", "floors", "rules", "tables", "DECISIONS.md", "INDEX.md"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="")
    ap.add_argument("--keep", type=int, default=60, help="keep this many newest snapshots")
    a = ap.parse_args()
    os.makedirs(DEST, mode=0o700, exist_ok=True)
    label = re.sub(r"[^a-z0-9-]+", "-", a.label.lower()).strip("-")
    name = time.strftime("%Y%m%d-%H%M%S") + ("-" + label if label else "") + ".tar.gz"
    path = os.path.join(DEST, name)
    n = 0
    with tarfile.open(path, "w:gz") as tf:
        for item in INCLUDE:
            p = os.path.join(ROOT, item)
            if not os.path.exists(p):
                continue
            def flt(ti):
                nonlocal n
                if "/backups/" in ti.name or ti.name.endswith("/backups"):
                    return None
                if ti.isfile(): n += 1
                return ti
            tf.add(p, arcname=os.path.join("dcc-campaign", item), filter=flt)
    os.chmod(path, 0o600)
    snaps = sorted(f for f in os.listdir(DEST) if f.endswith(".tar.gz"))
    for old in snaps[:-a.keep]:
        os.remove(os.path.join(DEST, old))
    print(f"snapshot saved: {path} ({n} files, {os.path.getsize(path)//1024} KB)")

if __name__ == "__main__":
    main()
