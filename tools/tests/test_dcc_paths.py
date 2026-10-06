"""Portable roots. A dotted import path and a temp campaign dir must still find lore/."""
import os
import subprocess
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMPAIGN = os.path.dirname(TOOLS)


class DccPathsTests(unittest.TestCase):
    def test_dotted_sys_path_and_temp_campaign_still_find_gm_quirks(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = (
                "import os, sys\n"
                "root = sys.argv[1]\n"
                "tmp = sys.argv[2]\n"
                "sys.path.insert(0, os.path.join(root, 'tools', 'tests', '..'))\n"
                "os.environ['DCC_CAMPAIGN_DIR'] = tmp\n"
                "os.environ.pop('DCC_CAMPAIGN_ROOT', None)\n"
                "os.environ.pop('DCC_LORE_ROOT', None)\n"
                "os.environ.pop('DCC_LORE_DIR', None)\n"
                "import dcc_paths\n"
                "assert os.path.abspath(str(dcc_paths._CAMPAIGN_FROM_FILE)) == os.path.abspath(root), dcc_paths._CAMPAIGN_FROM_FILE\n"
                "assert os.path.abspath(str(dcc_paths.campaign_root())) == os.path.abspath(tmp)\n"
                "table = dcc_paths.lore_root() / 'tables' / 'gm-quirks.json'\n"
                "assert table.is_file(), table\n"
                "assert os.path.abspath(str(table)).startswith(os.path.abspath(root) + os.sep)\n"
            )
            r = subprocess.run(
                [sys.executable, "-c", script, CAMPAIGN, tmp],
                capture_output=True, text=True,
            )
        self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == "__main__":
    unittest.main()
