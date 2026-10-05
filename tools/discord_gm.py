#!/usr/bin/env python3
"""Discord bridge for the AI GM (posts as the "DCC AI GM" bot; reads player transcripts).

Usage:
  python3 tools/discord_gm.py say "[GM] You open the door. It smells like regret."
  python3 tools/discord_gm.py say --file reply.txt
  python3 tools/discord_gm.py read [--limit 30] [--after MESSAGE_ID]   # player transcript from #table-transcript (formerly #dcc_ears)
  python3 tools/discord_gm.py new                                       # only transcript lines not yet seen
  python3 tools/discord_gm.py spotlight set "Player Name" [--alias X ...] [--note "why"]   # wake only on that player
  python3 tools/discord_gm.py spotlight show | clear                    # (no Discord token needed)
  python3 tools/discord_gm.py publish [--crawler X] [--full] [--dry-run]   # post each changed crawler's FULL card to their channel
  python3 tools/discord_gm.py setup-channels [--dry-run]                 # create 'Crawler Sheets' + one channel per CRAWLER (named <player>-<crawler>, e.g. hornn-horn)
  python3 tools/discord_gm.py register-channel <crawler> <channel-id>    # or point a crawler at a channel you made yourself
  python3 tools/discord_gm.py channels                                   # show the crawler -> channel map and bot access
  python3 tools/discord_gm.py stop                                      # kill switch: bridge stops talking + clears its queue

Tags (decision 032 / Caleb Oct 5 2026): [SYSTEM] = dry corporate System voice (clock, fees,
registration, collapse/floor notices; no jokes). [GM] or untagged = snarky narrator (achievements,
loot-box callouts, jokes). After a [SYSTEM] line, re-tag [GM] before any snark (tag carry-over).
[ROLL] lines are posted but never spoken. Needs env GM_DISCORD_TOKEN (never print it).
Posts over 2000 chars are split into several messages. State of 'new' is kept in sessions/.discord-cursor.
"""
import argparse, json, os, sys, tempfile, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datetime import datetime, timedelta

API = "https://discord.com/api/v10"
MOUTH = os.environ.get("DCC_MOUTH_CHANNEL_ID", "1556163836879568946")
EARS = os.environ.get("DCC_EARS_CHANNEL_ID", "1556163778788462602")
CURSOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sessions", ".discord-cursor")


def call(method, path, body=None):
    tok = os.environ.get("GM_DISCORD_TOKEN")
    if not tok:
        sys.exit("GM_DISCORD_TOKEN is not set")
    req = urllib.request.Request(API + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bot {tok}", "Content-Type": "application/json", "User-Agent": "DCC-GM (local, 1.0)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Discord error {e.code}: {e.read().decode()[:300]}")


def split(text, n=1900):
    out, cur = [], ""
    for para in text.split("\n"):
        while len(para) > n:
            cut = para.rfind(" ", 0, n) or n
            out.append((cur + "\n" + para[:cut]).strip("\n") if cur else para[:cut]); cur = ""; para = para[cut:].lstrip()
        if len(cur) + len(para) + 1 > n:
            out.append(cur); cur = para
        else:
            cur = (cur + "\n" + para) if cur else para
    if cur: out.append(cur)
    return [c for c in out if c.strip()]


def fetch(limit, after=None):
    q = f"?limit={limit}" + (f"&after={after}" if after else "")
    msgs = call("GET", f"/channels/{EARS}/messages{q}")
    return sorted(msgs, key=lambda m: int(m["id"]))


def show(msgs):
    for m in msgs:
        print(f"[{m['id']}] {m['content']}")


# ---- spotlight: tells the Discord bridge whom to wake the GM for -------------------------------------------
# File shared with the bridge (discord-voice-bridge/src/spotlight.js): {"player","aliases","updated","note"}.
# While a player is set and the file is fresh (SPOTLIGHT_MAX_AGE_MINUTES, default 20), the bridge wakes the GM
# only for that player's speech, or for anyone saying the standalone word "AI". Anything else (cleared, missing,
# malformed, stale) means open floor: every line wakes the GM. Re-run `spotlight set` to keep a long exchange fresh.
SPOTLIGHT_DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sessions", "spotlight.json")


def spotlight_path():
    return os.environ.get("SPOTLIGHT_FILE") or SPOTLIGHT_DEFAULT


def spotlight_max_age_minutes():
    try:
        return max(1.0, float(os.environ.get("SPOTLIGHT_MAX_AGE_MINUTES", "20")))
    except ValueError:
        return 20.0


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def write_json_atomic(path, data):
    """Write JSON via a temp file in the same directory + os.replace, so the bridge never reads a half-written file."""
    path = os.path.abspath(path)
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".spotlight-", suffix=".tmp", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def spotlight_set(player, aliases=(), note="", path=None):
    player = (player or "").strip()
    if not player:
        raise ValueError("player name must not be empty")
    if len(player) > 100:
        raise ValueError("player name too long (max 100 chars)")
    aliases = [a.strip() for a in aliases if a and a.strip()]
    data = {"player": player, "aliases": aliases, "updated": now_iso(), "note": (note or "").strip()}
    write_json_atomic(path or spotlight_path(), data)
    return data


def spotlight_clear(path=None):
    data = {"player": None, "aliases": [], "updated": now_iso(), "note": ""}
    write_json_atomic(path or spotlight_path(), data)
    return data


def spotlight_state(path=None, now=None):
    """Return (status, data|None) where status is one of: active, stale, open, missing, malformed."""
    path = path or spotlight_path()
    if not os.path.exists(path):
        return "missing", None
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("not an object")
    except (OSError, ValueError):
        return "malformed", None
    player = data.get("player")
    if not isinstance(player, str) or not player.strip():
        return "open", data
    try:
        updated = datetime.fromisoformat(str(data.get("updated")).replace("Z", "+00:00"))
        if updated.tzinfo is None:
            updated = updated.astimezone()
    except ValueError:
        return "stale", data  # no usable timestamp => the bridge treats it as open floor
    now = now or datetime.now().astimezone()
    if now - updated > timedelta(minutes=spotlight_max_age_minutes()):
        return "stale", data
    return "active", data


def spotlight_main(a):
    path = spotlight_path()
    if a.action == "set":
        try:
            d = spotlight_set(a.player, a.alias or [], a.note or "", path)
        except ValueError as e:
            sys.exit(f"spotlight: {e}")
        extra = f" (aliases: {', '.join(d['aliases'])})" if d["aliases"] else ""
        print(f"spotlight ON: {d['player']}{extra}. Only that player (or anyone saying \"AI\") will wake the GM. "
              f"Expires after {spotlight_max_age_minutes():g} min unless you set it again; run `spotlight clear` when done.")
    elif a.action == "clear":
        spotlight_clear(path)
        print("spotlight cleared: open floor, every player line wakes the GM.")
    else:  # show
        status, d = spotlight_state(path)
        if status == "active":
            extra = f", aliases: {', '.join(d.get('aliases') or [])}" if d.get("aliases") else ""
            print(f"spotlight ACTIVE: {d['player']}{extra} (set {d.get('updated')}" + (f", note: {d['note']}" if d.get("note") else "") + ")")
        elif status == "stale":
            print(f"spotlight STALE (older than {spotlight_max_age_minutes():g} min): treated as open floor. Last player: {d.get('player')}")
        elif status == "malformed":
            print("spotlight file is unreadable/malformed: the bridge treats it as open floor (fails open).")
        else:
            print("spotlight OFF: open floor, every player line wakes the GM.")


# ---- stop: kill switch for the bridge's speech --------------------------------------------------------------
# Writes {"action":"flush","id":"<unique>","ts":"ISO"} atomically; the bridge polls the file and, on a new id,
# stops playback and clears its whole TTS queue. Messages posted afterwards are spoken normally.
VOICE_CONTROL_DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sessions", "voice-control.json")


def voice_control_path():
    return os.environ.get("VOICE_CONTROL_FILE") or VOICE_CONTROL_DEFAULT


def stop_voice(path=None):
    import uuid
    data = {"action": "flush", "id": uuid.uuid4().hex, "ts": now_iso()}
    write_json_atomic(path or voice_control_path(), data)
    return data


def publisher_main(a):
    """publish / setup-channels / register-channel / channels (see tools/publisher.py). Returns the exit code."""
    import publisher as pub
    try:
        if a.cmd == "publish":
            client = None if a.dry_run else pub.DiscordClient()
            res = pub.publish(client, [a.crawler] if a.crawler else None, full=a.full, dry_run=a.dry_run)
            return 1 if any(r["status"].startswith("failed") for r in res) else 0
        client = pub.DiscordClient()
        if a.cmd == "setup-channels":
            r = pub.setup_channels(client, dry_run=a.dry_run)
            for c in r.get("created", []):
                print(f"{c['crawler']}: #{c['channel_name']} id {c['channel_id']}")
            return 0 if r.get("can_manage") else 2
        if a.cmd == "register-channel":
            pub.register_channel(client, a.crawler, a.channel_id, verify=not a.no_verify)
            return 0
        pub.channel_status(client)
        return 0
    except (pub.PublishError, pub.DiscordError) as e:
        print(f"publisher: {e}", file=sys.stderr)
        return 1


def use_session(argv):
    """Pick the campaign session (--session before the command, --campaign-session anywhere, $DCC_SESSION, or the bridge's
    active session). alpha keeps every default above; another session redirects the channels and state files to its own."""
    import campaign_session as cs
    try:
        argv = cs.apply_cli_session(argv)
    except cs.SessionError as e:
        sys.exit(f"ERROR: {e}")
    sid = cs.session_id()
    if sid != cs.DEFAULT_SESSION:
        global MOUTH, EARS, CURSOR, SPOTLIGHT_DEFAULT, VOICE_CONTROL_DEFAULT
        try:
            with open(cs.session_file(sid), encoding="utf-8") as f:
                cfg = json.load(f)
        except (OSError, ValueError):
            cfg = {}
        # Same-table sessions (env_prefix "") share alpha's .env channel names; prefer session.json, then DCC_*, then bridge names.
        MOUTH = str(cfg.get("mouth_channel_id") or os.environ.get("DCC_MOUTH_CHANNEL_ID") or os.environ.get("GM_OUTPUT_CHANNEL_ID") or "")
        EARS = str(cfg.get("ears_channel_id") or os.environ.get("DCC_EARS_CHANNEL_ID") or os.environ.get("TRANSCRIPT_CHANNEL_ID") or "")
        if not (MOUTH and EARS):
            sys.exit(f"session '{sid}' has no mouth/ears channel ids: set mouth_channel_id and ears_channel_id in {cs.session_file(sid)}")
        CURSOR = os.path.join(cs.data_dir(sid), ".discord-cursor")
        SPOTLIGHT_DEFAULT = os.path.join(cs.data_dir(sid), "spotlight.json")
        VOICE_CONTROL_DEFAULT = os.path.join(cs.data_dir(sid), "voice-control.json")
    return argv


def main(argv=None):
    argv = use_session(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("say"); s.add_argument("text", nargs="?"); s.add_argument("--file")
    r = sub.add_parser("read"); r.add_argument("--limit", type=int, default=30); r.add_argument("--after")
    sub.add_parser("new")
    pb = sub.add_parser("publish", help="post changed crawlers' full cards to their own channels")
    pb.add_argument("--crawler"); pb.add_argument("--full", action="store_true", help="post even if nothing changed"); pb.add_argument("--dry-run", action="store_true")
    sc = sub.add_parser("setup-channels", help="create the Crawler Sheets category + one channel per Crawler (<player>-<crawler>)"); sc.add_argument("--dry-run", action="store_true")
    rc = sub.add_parser("register-channel", help="use an existing channel for a crawler"); rc.add_argument("crawler"); rc.add_argument("channel_id"); rc.add_argument("--no-verify", action="store_true")
    sub.add_parser("channels", help="show the crawler -> channel map")
    sub.add_parser("stop", help="stop the bridge's current speech and clear its queue")
    sp = sub.add_parser("spotlight", help="limit which player's speech wakes the GM")
    sps = sp.add_subparsers(dest="action", required=True)
    ss = sps.add_parser("set"); ss.add_argument("player"); ss.add_argument("--alias", action="append"); ss.add_argument("--note")
    sps.add_parser("clear"); sps.add_parser("show")
    a = ap.parse_args(argv)
    if a.cmd == "spotlight":
        return spotlight_main(a)
    if a.cmd in ("publish", "setup-channels", "register-channel", "channels"):
        code = publisher_main(a)
        if code:
            sys.exit(code)
        return
    if a.cmd == "stop":
        d = stop_voice()
        print(f"stop signal written (id {d['id'][:8]}): the bridge will stop talking and clear its speech queue within a second. "
              "It does not delete anything already posted in #gm-voice (formerly #gm-voice).")
        return
    if a.cmd == "say":
        text = open(a.file).read() if a.file else a.text
        if not text or not text.strip():
            sys.exit("nothing to say")
        for chunk in split(text.strip()):
            call("POST", f"/channels/{MOUTH}/messages", {"content": chunk, "allowed_mentions": {"parse": []}})
        print("posted")
    elif a.cmd == "read":
        show(fetch(min(a.limit, 100), a.after))
    elif a.cmd == "new":
        last = open(CURSOR).read().strip() if os.path.exists(CURSOR) else None
        msgs = fetch(100, last) if last else fetch(30)
        if msgs:
            open(CURSOR, "w").write(msgs[-1]["id"])
            show(msgs)
        else:
            print("(no new player speech)")

if __name__ == "__main__":
    main()
