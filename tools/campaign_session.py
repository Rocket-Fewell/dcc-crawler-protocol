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
_ID = re.compile(r"^[a-z0-9][a-z0-9_-]{0,30}$")
RESERVED = {"backups", "secret", "archive", "sessions", "characters", "tmp"}

# Portable root: DCC_CAMPAIGN_ROOT (preferred) or legacy DCC_CAMPAIGN_DIR, else tools/'s parent.
import dcc_paths as _paths  # noqa: E402  (same tools/ folder; stdlib + sibling)
DEFAULT_CAMPAIGN_DIR = _paths.CAMPAIGN_ROOT  # resolved at import; env overrides still read live in campaign_dir()


class SessionError(Exception):
    pass


def valid_id(sid):
    return bool(_ID.match(sid or "")) and sid not in RESERVED


def campaign_dir():
    return str(_paths.campaign_root())


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



def sheet_category_name(sid=None):
    """Discord category for Crawler sheet channels. Alpha keeps the historical name; others are session-scoped so they never share alpha's category."""
    sid = sid or session_id()
    return "Crawler Sheets" if is_alpha(sid) else f"Crawler Sheets ({sid})"


def sheet_channel_prefix(sid=None):
    """Prefix for new sheet channel names. Empty for alpha; "<id>-" otherwise so names cannot collide with alpha's #hornn-sheet etc. in the same guild."""
    sid = sid or session_id()
    return "" if is_alpha(sid) else f"{sid}-"


def write_active(sid, by=None):
    """Persist the active session (same file the bridge `/session use` writes). Tools without --session / DCC_SESSION follow this. Does not restart the bot."""
    sid = (sid or "").strip().lower()
    if sid != DEFAULT_SESSION and not valid_id(sid):
        raise SessionError(f"bad session id {sid!r}")
    path = active_file()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.{os.getpid()}.tmp"
    payload = {"session": sid, "updated": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "by": by}
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f)
        f.write("\n")
    os.replace(tmp, path)
    return path


def session_exists(sid=None):
    sid = sid or session_id()
    if sid == DEFAULT_SESSION:
        return True
    d = data_dir(sid)
    return os.path.exists(os.path.join(d, "state.json")) or os.path.exists(session_file(sid))


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


def _cli(argv=None):
    """list | show | use <id> — inspect / mark the active campaign session (alpha stays at sessions/; others under sessions-data/<id>/)."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__.strip())
        print()
        print("Usage:")
        print("  python3 tools/campaign_session.py list")
        print("  python3 tools/campaign_session.py show")
        print("  python3 tools/campaign_session.py use <id>   # writes sessions/active-session.json; bridge picks it up on /session use or restart")
        print("Create a new empty campaign: python3 tools/new-session.py <id>")
        return 0
    cmd = argv[0]
    if cmd == "list":
        active = session_id()
        for sid in list_sessions():
            mark = "▶" if sid == active else "•"
            label = ""
            try:
                with open(session_file(sid), encoding="utf-8") as f:
                    label = (json.load(f) or {}).get("label") or ""
            except (OSError, ValueError):
                pass
            extra = f" - {label}" if label else ""
            where = data_dir(sid)
            print(f"{mark} {sid}{extra}  ({where})")
        return 0
    if cmd == "show":
        sid = session_id()
        print(f"active: {sid}")
        print(f"data:   {data_dir(sid)}")
        print(f"chars:  {characters_dir(sid)}")
        print(f"source: {'DCC_SESSION' if os.environ.get('DCC_SESSION') else ('active-session.json' if persisted_active() else 'default')}")
        return 0
    if cmd == "use":
        if len(argv) < 2:
            raise SessionError("use needs a session id")
        sid = argv[1].strip().lower()
        if not session_exists(sid):
            raise SessionError(f"no session {sid!r}; create with: python3 tools/new-session.py {sid}")
        path = write_active(sid, by="cli")
        print(f"marked active: {sid} (wrote {path})")
        print("Bridge: /leave then /session use", sid, "(or set DCC_SESSION="+sid+" and restart). Tools without --session follow this file.")
        return 0
    raise SessionError(f"unknown command {cmd!r} (list|show|use)")


if __name__ == "__main__":
    try:
        raise SystemExit(_cli())
    except SessionError as e:
        print(f"campaign_session: {e}", file=sys.stderr)
        raise SystemExit(2)
