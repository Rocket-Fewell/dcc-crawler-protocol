#!/usr/bin/env python3
"""Hash check for tables/item-reskins.json (single source = Lore's file; ours is a symlink). Usage: python3 tools/reskin_check.py
Exits 1 on a hash mismatch; a missing version file is only a warning (exit 0).
Owner: Architect | Status: draft | Version: 0.1.0 | Updated: 2026-10-04
Summary: sha256 of item-reskins.json must equal the sha256 in item-reskins.version.json (Lore's file), so nobody keeps a divergent copy."""
import hashlib
import json
import os
import sys

TABLES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tables")


def check(tables=TABLES):
    """-> (status, message). status: ok | warn (no version file) | fail (mismatch or unreadable) | missing."""
    table = os.path.join(tables, "item-reskins.json")
    version = os.path.join(tables, "item-reskins.version.json")
    if not os.path.exists(table):
        return "missing", f"{table} not found"
    if not os.path.exists(version):
        return "warn", "item-reskins.version.json not found; cannot verify the table hash"
    try:
        want = json.load(open(version, encoding="utf-8"))["sha256"]
    except (OSError, ValueError, KeyError) as e:
        return "fail", f"cannot read sha256 from the version file: {e}"
    got = hashlib.sha256(open(table, "rb").read()).hexdigest()
    if got != want:
        return "fail", f"item-reskins.json sha256 {got[:12]} does not match the version file {want[:12]}: a divergent copy? Re-link to Lore's file"
    return "ok", f"item-reskins.json matches the version file ({want[:12]})"


if __name__ == "__main__":
    st, msg = check()
    print(f"{st.upper()}: {msg}")
    sys.exit(1 if st in ("fail", "missing") else 0)
