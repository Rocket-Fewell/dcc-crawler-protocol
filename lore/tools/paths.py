"""Portable roots for DCC lore tools (fresh-checkout safe).

LORE_ROOT      = env DCC_LORE_ROOT, else parent of this tools/ dir (absolute(), not resolve(),
                 so a campaign `lore/` symlink keeps the repo layout).
CAMPAIGN_ROOT  = env DCC_CAMPAIGN_ROOT, else LORE_ROOT.parent if it looks like the campaign
                 repo, else the sibling LORE_ROOT.parent/'dcc-campaign'. Raises if missing.
VOICE_BRIDGE_SRC = env DCC_VOICE_BRIDGE_SRC, else <campaign root>/bot/src/create (repo mirror),
                 else legacy siblings; None only if none exist (callers warn and skip).

Example overrides (not hardcoded paths):
  export DCC_LORE_ROOT=/path/to/lore
  export DCC_CAMPAIGN_ROOT=/path/to/dcc-crawler-protocol
  export DCC_VOICE_BRIDGE_SRC=/path/to/discord-voice-bridge/src/create
"""
from __future__ import annotations

import os
from pathlib import Path

_TOOLS = Path(__file__).absolute().parent
_LORE_DEFAULT = _TOOLS.parent


def _looks_like_campaign(p: Path) -> bool:
    if not p.is_dir():
        return False
    return (p / "NAMING-CONVENTIONS.md").is_file() or (p / "tables" / "chargen-5e.json").is_file()


def lore_root() -> Path:
    env = os.environ.get("DCC_LORE_ROOT")
    if env:
        return Path(env).absolute()
    return _LORE_DEFAULT


def campaign_root() -> Path:
    env = os.environ.get("DCC_CAMPAIGN_ROOT")
    if env:
        p = Path(env).absolute()
        if not p.is_dir():
            raise FileNotFoundError(
                "DCC_CAMPAIGN_ROOT=%s does not exist or is not a directory" % env
            )
        return p
    lore = lore_root()
    parent = lore.parent
    if _looks_like_campaign(parent):
        return parent
    sibling = parent / "dcc-campaign"
    if _looks_like_campaign(sibling):
        return sibling
    raise FileNotFoundError(
        "Cannot find the campaign repo next to lore (%s). "
        "Set DCC_CAMPAIGN_ROOT to the campaign root (the directory that holds "
        "NAMING-CONVENTIONS.md or tables/chargen-5e.json)." % lore
    )


def voice_bridge_src() -> Path | None:
    """Create-screens build code_ref look-up.

    Order: DCC_VOICE_BRIDGE_SRC (explicit override, if set and present), then the repo mirror
    <campaign root>/bot/src/create, then legacy siblings. Returns None only if none exist.
    """
    env = os.environ.get("DCC_VOICE_BRIDGE_SRC")
    if env:
        p = Path(env).absolute()
        if p.is_dir():
            return p
    candidates = []
    try:
        candidates.append(campaign_root() / "bot" / "src" / "create")
    except FileNotFoundError:
        pass
    lore = lore_root()
    candidates += [
        lore.parent / "discord-voice-bridge" / "src" / "create",
        lore.parent.parent / "discord-voice-bridge" / "src" / "create",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return None


# Eager aliases (most scripts import these once at module load)
LORE_ROOT = lore_root()
TOOLS = LORE_ROOT / "tools"
TABLES = LORE_ROOT / "tables"
try:
    CAMPAIGN_ROOT = campaign_root()
except FileNotFoundError:
    CAMPAIGN_ROOT = None  # type: ignore

CHARGEN = (CAMPAIGN_ROOT / "tables" / "chargen-5e.json") if CAMPAIGN_ROOT else None
CREATE_FLOW_LINES = (CAMPAIGN_ROOT / "tables" / "create-flow-lines.json") if CAMPAIGN_ROOT else None
SPECIES_SUPP = (CAMPAIGN_ROOT / "rules" / "30-species-supplement-5e.md") if CAMPAIGN_ROOT else None
VOICE_BRIDGE_SRC = voice_bridge_src()


def require_campaign() -> Path:
    if CAMPAIGN_ROOT is None:
        raise FileNotFoundError(
            "Campaign root not found. Set DCC_CAMPAIGN_ROOT to the campaign repo root."
        )
    return CAMPAIGN_ROOT


def require_chargen() -> Path:
    require_campaign()
    assert CHARGEN is not None
    if not CHARGEN.is_file():
        raise FileNotFoundError(
            "chargen-5e.json not found at %s (set DCC_CAMPAIGN_ROOT)" % CHARGEN
        )
    return CHARGEN
