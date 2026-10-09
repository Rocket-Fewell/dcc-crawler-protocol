"""Repo-relative roots. No machine paths."""

from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = ENGINE_DIR.parent
CARDS_DIR = REPO_ROOT / "Cursor-DCC-CardsReference"
FIXTURES_DIR = ENGINE_DIR / "fixtures"
