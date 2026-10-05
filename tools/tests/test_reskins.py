"""item-reskins.json is a single source: our tables/ entry is a symlink to Lore's file, and its hash must match Lore's version file."""
import hashlib
import json
import os
import tempfile
import unittest

from test_state import TOOLS
import sys
sys.path.insert(0, TOOLS)
import reskin_check  # noqa: E402


class ReskinSourceTests(unittest.TestCase):
    def test_live_table_is_a_symlink_and_hash_matches_lores_version_file(self):
        link = os.path.join(reskin_check.TABLES, "item-reskins.json")
        self.assertTrue(os.path.islink(link), "tables/item-reskins.json must be a symlink to Lore's file, not a copy")
        st, msg = reskin_check.check()
        self.assertEqual(st, "ok", msg)

    def test_mismatch_fails_and_missing_version_only_warns(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "item-reskins.json"), "w") as f:
                f.write('{"entries": []}')
            self.assertEqual(reskin_check.check(d)[0], "warn")
            with open(os.path.join(d, "item-reskins.version.json"), "w") as f:
                json.dump({"sha256": "0" * 64}, f)
            self.assertEqual(reskin_check.check(d)[0], "fail")
            with open(os.path.join(d, "item-reskins.version.json"), "w") as f:
                json.dump({"sha256": hashlib.sha256(b'{"entries": []}').hexdigest()}, f)
            self.assertEqual(reskin_check.check(d)[0], "ok")


if __name__ == "__main__":
    unittest.main()
