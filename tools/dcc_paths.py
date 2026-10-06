"""Portable roots for DCC campaign tools (fresh-checkout safe).

CAMPAIGN_ROOT = env DCC_CAMPAIGN_ROOT, else legacy DCC_CAMPAIGN_DIR, else parent of
                this tools/ dir (works in the flattened repo layout).
LORE_ROOT     = env DCC_LORE_ROOT, else <campaign>/lore, else sibling dcc-lore.
BRIDGE_ROOT   = env DCC_BRIDGE_DIR, else <campaign>/bot, else
                <campaign>/discord-voice-bridge, else a sibling discord-voice-bridge.

ROOT wins over the legacy *_DIR alias when both are set. absolute() is used (not
resolve()) so a campaign lore/ symlink keeps the repo layout.
"""
from __future__ import annotations

import os
from pathlib import Path

# abspath (not Path.absolute()) collapses a ".." segment. Tests insert tools/tests/..
# on sys.path; Path.absolute() would then treat the campaign root as tools/tests.
# abspath does not resolve symlinks, so a lore/ symlink still keeps the repo layout.
_TOOLS = Path(os.path.abspath(__file__)).parent
_CAMPAIGN_FROM_FILE = _TOOLS.parent


def _looks_like_lore(p: Path) -> bool:
    if not p.is_dir():
        return False
    return (p / "CANON-LEDGER.md").is_file() or (p / "tables").is_dir()


def _env_path(*names: str) -> Path | None:
    for name in names:
        raw = os.environ.get(name)
        if raw:
            return Path(raw).absolute()
    return None


def campaign_root() -> Path:
    """Campaign root (holds tools/, tables/, sessions/). Prefer env overrides."""
    env = _env_path("DCC_CAMPAIGN_ROOT", "DCC_CAMPAIGN_DIR")
    if env is not None:
        return env
    return _CAMPAIGN_FROM_FILE


def lore_root() -> Path:
    """Lore root (holds tables/, CANON-LEDGER.md). Prefer env, then campaign/lore.

    A temp DCC_CAMPAIGN_DIR with no lore of its own falls back to the checkout
    beside this file, so a sandboxed session still sees the public tables.
    """
    env = _env_path("DCC_LORE_ROOT", "DCC_LORE_DIR")
    if env is not None:
        return env
    camp = campaign_root()
    via_campaign = camp / "lore"
    if _looks_like_lore(via_campaign):
        return via_campaign.absolute()
    sibling = camp.parent / "dcc-lore"
    if _looks_like_lore(sibling):
        return sibling.absolute()
    via_file = _CAMPAIGN_FROM_FILE / "lore"
    if via_file != via_campaign and _looks_like_lore(via_file):
        return via_file.absolute()
    return via_campaign.absolute()


def bridge_root() -> Path:
    """Discord voice bridge package root (holds src/, package.json, .env.agents)."""
    env = _env_path("DCC_BRIDGE_DIR", "DCC_VOICE_BRIDGE")
    if env is not None:
        return env
    camp = campaign_root()
    for cand in (camp / "bot", camp / "discord-voice-bridge"):
        if (cand / "package.json").is_file() or (cand / "src").is_dir():
            return cand.absolute()
    sibling = camp.parent / "discord-voice-bridge"
    if (sibling / "package.json").is_file() or (sibling / "src").is_dir():
        return sibling.absolute()
    return (camp / "bot").absolute()


def agents_webhook_file() -> Path:
    """Per-agent Discord webhook file (.env.agents). Override with AGENTS_WEBHOOK_FILE."""
    env = os.environ.get("AGENTS_WEBHOOK_FILE")
    if env:
        return Path(env).absolute()
    return bridge_root() / ".env.agents"


# Eager string aliases for older call sites that want a str path
CAMPAIGN_ROOT = str(campaign_root())
LORE_ROOT = str(lore_root())
BRIDGE_ROOT = str(bridge_root())
# Legacy name kept so `from dcc_paths import DEFAULT_CAMPAIGN_DIR` still works.
DEFAULT_CAMPAIGN_DIR = CAMPAIGN_ROOT
