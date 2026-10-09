#!/usr/bin/env python3
"""Start the local table from the repo root: python3 engine/serve.py"""

import sys
from pathlib import Path

_ENGINE = Path(__file__).resolve().parent
_REPO = _ENGINE.parent
sys.path.insert(0, str(_ENGINE))
sys.path.insert(0, str(_REPO / "tools"))

from dcc_engine.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
