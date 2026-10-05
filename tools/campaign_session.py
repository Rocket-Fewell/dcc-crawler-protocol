"""Session addressing for parallel campaigns ("alpha" is the live game; others are e.g. "beta").

A SESSION is one campaign table: its own state.json, ledgers, publisher snapshots, channel map, spotlight/voice-control files,
GM-only quirk roll + affinity, characters/ and roll logs. Rules, decks, lore, floors and tools are SHARED and hold no session state.

Selecting a session (same for every tool): `--session <id>` anywhere on the command line, else $DCC_SESSION, else the
bridge-persisted active session (sessions/active-session.json, written by `/session use`), else "alpha".

Layout (alpha is exactly where it always was; nothing moves):
    alpha  data   <campaign>/sessions/                      secret <campaign>/gm-notes/secret/                  characters <campaign>/characters/
    <id>   data   <campaign>/sessions-data/<id>/            secret <campaign>/gm-notes/secret/sessions/<id>/    characters <data>/characters/
"""
import json
import os
import re
import sys

DEFAULT_SESSION = "alpha"
DEFAULT_CAMPAIGN_DIR = "/workspace/dcc-campaign"
_ID = re.compile(r"^[a-z0-9][a-z0-9_-]{0,30}$")
RESERVED = {"backups", "secret", "archive", "sessions", "characters", "tmp"}


class SessionError(Exception):
    pass


def valid_id(sid):
    return bool(_ID.match(sid or "")) and sid not in RESERVED


def campaign_dir():
    return os.environ.get("DCC_CAMPAIGN_DIR") or DEFAULT_CAMPAIGN_DIR


def active_file():
    """The bridge's persisted choice (`/session use <id>`). Lives in the alpha data dir so it never moves."""
    return os.path.join(campaign_dir(), "sessions", "active-session.json")


def persisted_active():
    try:
        with open(active_file(), encoding="utf-8") as f:
            sid = str(json.load(f).get("session", "")).strip().lower()
        return sid if valid_id(sid) else None
    except (OSError, ValueError, AttributeError):
        return None


def session_id():
    sid = (os.environ.get("DCC_SESSION") or persisted_active() or DEFAULT_SESSION).strip().lower()
    if sid != DEFAULT_SESSION and not valid_id(sid):
        raise SessionError(f"bad session id {sid!r}: use a-z 0-9 _ - (max 31 chars; not {', '.join(sorted(RESERVED))})")
    return sid


def is_alpha(sid=None):
    return (sid or session_id()) == DEFAULT_SESSION


def data_dir(sid=None):
    sid = sid or session_id()
    return os.path.join(campaign_dir(), "sessions") if sid == DEFAULT_SESSION else os.path.join(campaign_dir(), "sessions-data", sid)


def secret_dir(sid=None):
    sid = sid or session_id()
    base = os.path.join(campaign_dir(), "gm-notes", "secret")
    return base if sid == DEFAULT_SESSION else os.path.join(base, "sessions", sid)


def characters_dir(sid=None):
    sid = sid or session_id()
    return os.path.join(campaign_dir(), "characters") if sid == DEFAULT_SESSION else os.path.join(data_dir(sid), "characters")


def session_file(sid=None):
    """Per-session non-secret config (channels, labels, Fish cap share); secrets stay in env vars named in it."""
    return os.path.join(data_dir(sid), "session.json")


def list_sessions():
    out = [DEFAULT_SESSION]
    root = os.path.join(campaign_dir(), "sessions-data")
    if os.path.isdir(root):
        out += sorted(d for d in os.listdir(root) if valid_id(d) and os.path.isdir(os.path.join(root, d)))
    return out


def apply_cli_session(argv=None):
    """Pick the session from the command line, export it as $DCC_SESSION (so child processes and every path helper see it) and
    return argv without the flag. Call first thing in main() of every tool.

    Forms: `tool.py --session beta <command> ...` (the flag must come BEFORE the command, because `affinity add --session S` already
    uses --session for the in-game session label) or `--campaign-session beta` anywhere. Or set DCC_SESSION=beta."""
    argv = list(sys.argv[1:] if argv is None else argv)
    out, i, leading = [], 0, True
    while i < len(argv):
        a = argv[i]
        if a == "--campaign-session" or (leading and a == "--session"):
            if i + 1 >= len(argv):
                raise SessionError(f"{a} needs a session id")
            os.environ["DCC_SESSION"] = argv[i + 1].strip().lower()
            i += 2
            continue
        if a.startswith("--campaign-session=") or (leading and a.startswith("--session=")):
            os.environ["DCC_SESSION"] = a.split("=", 1)[1].strip().lower()
            i += 1
            continue
        if not a.startswith("-"):
            leading = False
        out.append(a)
        i += 1
    session_id()  # validates
    return out
