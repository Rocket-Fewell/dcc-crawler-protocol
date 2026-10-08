#!/usr/bin/env python3
"""Discord bridge for the AI GM (posts as the "DCC AI GM" bot; reads player transcripts).

Usage:
  python3 tools/discord_gm.py say "[GM] You open the door. It smells like regret."
  python3 tools/discord_gm.py say --file reply.txt
  python3 tools/discord_gm.py read [--limit 30] [--after MESSAGE_ID]   # player transcript from #table-transcript (formerly #dcc_ears)
  python3 tools/discord_gm.py new --lock [--wait 90]                    # take the GM turn lock, then read lines not yet seen (preferred)
  python3 tools/discord_gm.py new [--peek]                              # read only; marks lines read only if this run holds the lock (or no run does)
  python3 tools/discord_gm.py unlock [--force]                          # release the turn lock this run holds (same as gm_lock.sh release)
  python3 tools/discord_gm.py spotlight set "Player Name" [--alias X ...] [--note "why"]   # wake only on that player
  python3 tools/discord_gm.py spotlight show | clear                    # (no Discord token needed)
  python3 tools/discord_gm.py whisper CRAWLER "text" | --file F [--dry-run]   # PRIVATE post to that Crawler's own sheet channel only (never spoken)
  python3 tools/discord_gm.py publish [--crawler X] [--full] [--dry-run]   # post each changed crawler's FULL card to their channel
  python3 tools/discord_gm.py setup-channels [--dry-run]                 # create 'Crawler Sheets' + one channel per CRAWLER (named <player>-<crawler>, e.g. hornn-horn)
  python3 tools/discord_gm.py register-channel <crawler> <channel-id>    # or point a crawler at a channel you made yourself
  python3 tools/discord_gm.py channels                                   # show the crawler -> channel map and bot access
  python3 tools/discord_gm.py stop                                      # kill switch: bridge stops talking + clears its queue

Tags (decision 032 / agreed Oct 5 2026): [SYSTEM] = dry corporate System voice (clock, fees,
registration, collapse/floor notices; no jokes). [GM] or untagged = snarky narrator (achievements,
loot-box callouts, gm_narration, gm_color, jokes). After a [SYSTEM] line, re-tag [GM] before any snark.
Manifest kinds (same allow-list as extract.js / encounter_text.py): ONLY `system_notice` and
`exit_warning_read_aloud` map to [SYSTEM]; `voice_line`, `route_voice_line`, `gm_narration`,
`gm_color`, and unknown kinds map to [GM]. [ROLL] lines are posted but never spoken.
Needs env GM_DISCORD_TOKEN (never print it).
Posts over 2000 chars are split into several messages. State of 'new' is kept in sessions/.discord-cursor.
Turn lock (Oct 7 2026 fix, lost table lines): `new` advances the read cursor only when this run holds the GM turn lock
(tools/gm_lock.sh, <data>/.gm-lock) or when no run holds it. While ANOTHER run holds it, `new` only peeks: it prints the
lines marked PEEK and leaves them unread for the next turn. `new --lock` takes the lock first (waits up to --wait seconds).
"""
import argparse, json, os, shutil, sys, tempfile, time, urllib.request, urllib.error
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


# ---- GM turn lock (same directory and 120 s staleness as tools/gm_lock.sh) -----------------------------------------
# Ownership: gm_lock.sh / `new --lock` write <lock>/owner with token=$DCC_GM_LOCK_TOKEN and ppid=<calling shell>. A run holds
# the lock when its DCC_GM_LOCK_TOKEN matches, or (no token on the lock) when it runs from the same shell that took it.
LOCK_FRESH_S = 120


def lock_dir():
    return os.environ.get("DCC_GM_LOCK_DIR") or os.path.join(os.path.dirname(os.path.abspath(CURSOR)), ".gm-lock")


def _lock_owner(d):
    try:
        with open(os.path.join(d, "owner"), encoding="utf-8") as f:
            return dict(line.rstrip("\n").split("=", 1) for line in f if "=" in line)
    except OSError:
        return None


def lock_state(d=None, now=None):
    """-> 'free' (no fresh lock), 'mine' (this run holds it), 'other' (another run holds it) or 'unknown' (fresh lock, no owner info)."""
    d = d or lock_dir()
    try:
        age = (now or time.time()) - os.stat(d).st_mtime
    except OSError:
        return "free"
    if not os.path.isdir(d) or age >= LOCK_FRESH_S:
        return "free"
    owner = _lock_owner(d)
    if owner is None:
        return "unknown"
    tok = os.environ.get("DCC_GM_LOCK_TOKEN", "")
    if owner.get("token"):
        return "mine" if tok and owner["token"] == tok else "other"
    return "mine" if owner.get("ppid") == str(os.getppid()) else "other"


def lock_acquire(d=None):
    """Take the lock like `gm_lock.sh acquire` (a stale lock is replaced). True when taken (or already held by this run)."""
    d = d or lock_dir()
    st = lock_state(d)
    if st == "mine":
        os.utime(d)   # refresh: a long turn keeps its lock
        return True
    if st != "free":
        return False
    if os.path.isdir(d):   # stale
        shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    try:
        os.mkdir(d)
    except FileExistsError:
        return False
    with open(os.path.join(d, "owner"), "w", encoding="utf-8") as f:
        f.write(f"token={os.environ.get('DCC_GM_LOCK_TOKEN', '')}\nppid={os.getppid()}\npid={os.getpid()}\nat={int(time.time())}\n")
    return True


def lock_release(d=None, force=False):
    """-> 'released' | 'free' | 'not-yours'. Removes the lock only when this run holds it (or --force)."""
    d = d or lock_dir()
    st = lock_state(d)
    if st == "free" and not os.path.isdir(d):
        return "free"
    if st in ("other", "unknown") and not force:
        return "not-yours"
    shutil.rmtree(d, ignore_errors=True)
    return "released"


def read_new(mode="auto", wait=0.0, poll=2.0):
    """`new`: -> (status, msgs). mode 'lock' takes the lock first (status 'busy' = nothing read, nothing marked);
    'peek' never advances the cursor; 'auto' advances only when the lock is free or held by this run, else peeks."""
    if mode == "lock":
        end = time.time() + max(0.0, wait)
        while not lock_acquire():
            if time.time() >= end:
                return "busy", []
            time.sleep(poll)
        advance = True
    elif mode == "peek":
        advance = False
    else:
        st = lock_state()
        if st == "mine":
            os.utime(lock_dir())
        advance = st in ("free", "mine")
    last = open(CURSOR).read().strip() if os.path.exists(CURSOR) else None
    msgs = fetch(100, last) if last else fetch(30)
    if msgs and advance:
        open(CURSOR, "w").write(msgs[-1]["id"])
    return ("read" if advance else "peek"), msgs


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


# ---- whisper: a private System message to ONE Crawler's own sheet channel (secret triggers, e.g. the Benefactor Signal) ----
# Uses the same crawler -> channel map as `publish` / `channels` (<data>/player-channels.json). Refuses a Crawler with no mapped
# channel, and refuses any channel the bridge reads or speaks (#gm-voice / GM output, #table-transcript, the voice channel), so a
# whisper is never read aloud. Every post starts with WHISPER_PREFIX. The text is not logged anywhere by this tool.
WHISPER_PREFIX = "[PRIVATE - System]"


def _bridge_channel_ids():
    import publisher as pub
    ids = set(pub.protected_channel_ids()) | {MOUTH, EARS}
    for k in ("GM_OUTPUT_CHANNEL_ID", "TRANSCRIPT_CHANNEL_ID", "VOICE_CHANNEL_ID", "DCC_MOUTH_CHANNEL_ID", "DCC_EARS_CHANNEL_ID"):
        if os.environ.get(k):
            ids.add(os.environ[k])
    return {str(i) for i in ids if i}


def whisper_target(crawler):
    """-> (crawler record, channel id, channel name). Raises publisher.PublishError when it must not be sent."""
    import publisher as pub
    state = pub.read_json(pub.state_path(), None)
    if not isinstance(state, dict):
        raise pub.PublishError(f"no readable state at {pub.state_path()}")
    cfg = pub.load_config()
    c = pub.resolve_crawler(crawler, state, cfg)
    _key, m = pub.mapping_for(cfg, c["name"])
    cid = str((m or {}).get("channel_id") or "").strip()
    if not cid:
        raise pub.PublishError(f"REFUSED: {c['name']} has no private sheet channel mapped (see `discord_gm.py channels`; "
                               f"`setup-channels` or `register-channel '{c['name']}' <id>`). Nothing was posted.")
    if cid in _bridge_channel_ids():
        raise pub.PublishError(f"REFUSED: {c['name']}'s mapped channel is a voice/transcript channel the bridge reads aloud; nothing was posted. Fix the channel map.")
    return c, cid, (m or {}).get("channel_name") or cid


def whisper_messages(text):
    body = (text or "").strip()
    if not body:
        raise ValueError("nothing to whisper")
    lim = 1900 - len(WHISPER_PREFIX) - 10
    parts = [chunk[i:i + lim] for chunk in split(body, lim) for i in range(0, len(chunk), lim)]   # hard cap: a word longer than lim still fits Discord's 2000
    return [f"{WHISPER_PREFIX} {p}" if i == 0 else f"{WHISPER_PREFIX} (cont.) {p}" for i, p in enumerate(parts)]


def whisper(crawler, text, client=None, dry_run=False, log=print):
    import publisher as pub
    msgs = whisper_messages(text)
    c, cid, cname = whisper_target(crawler)
    if dry_run:
        log(f"DRY RUN: would post {len(msgs)} private message(s) to #{cname} ({c['name']} only); nothing posted.")
        for t in msgs:
            log(t)
        return {"crawler": c["name"], "channel_id": cid, "messages": msgs, "posted": 0}
    client = client or pub.DiscordClient()
    for t in msgs:
        client.request("POST", f"/channels/{cid}/messages", {"content": t, "allowed_mentions": {"parse": []}})
    log(f"whispered to #{cname} ({c['name']} only; {len(msgs)} message(s); not spoken)")
    return {"crawler": c["name"], "channel_id": cid, "messages": msgs, "posted": len(msgs)}


def publisher_main(a):
    """publish / setup-channels / register-channel / channels (see tools/publisher.py). Returns the exit code."""
    import publisher as pub
    try:
        if a.cmd == "publish":
            client = None if a.dry_run else pub.DiscordClient()
            if a.note and not a.crawler:
                print("publish --note needs --crawler (the note goes on that one card)", file=sys.stderr)
                return 2
            res = pub.publish(client, [a.crawler] if a.crawler else None, full=a.full, dry_run=a.dry_run, note=a.note)
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
    nw = sub.add_parser("new", help="transcript lines not yet seen (marked read only while this run holds the GM turn lock, or no run does)")
    nw.add_argument("--lock", action="store_true", help="take the GM turn lock first (like gm_lock.sh acquire); busy = nothing read, exit 1")
    nw.add_argument("--wait", type=float, default=0.0, help="with --lock: keep trying for up to N seconds while another run holds it")
    nw.add_argument("--peek", action="store_true", help="show the lines but never mark them read")
    ul = sub.add_parser("unlock", help="release the GM turn lock held by this run"); ul.add_argument("--force", action="store_true", help="remove it even if another run holds it")
    pb = sub.add_parser("publish", help="post changed crawlers' full cards to their own channels")
    pb.add_argument("--crawler"); pb.add_argument("--full", action="store_true", help="post even if nothing changed"); pb.add_argument("--dry-run", action="store_true")
    pb.add_argument("--note", help="GM text shown first on that card's Changed line, this post only (needs --crawler)")
    sc = sub.add_parser("setup-channels", help="create the Crawler Sheets category + one channel per Crawler (<player>-<crawler>)"); sc.add_argument("--dry-run", action="store_true")
    rc = sub.add_parser("register-channel", help="use an existing channel for a crawler"); rc.add_argument("crawler"); rc.add_argument("channel_id"); rc.add_argument("--no-verify", action="store_true")
    sub.add_parser("channels", help="show the crawler -> channel map")
    wh = sub.add_parser("whisper", help="post a [PRIVATE - System] message to ONE Crawler's own sheet channel (never the voice channel)")
    wh.add_argument("crawler"); wh.add_argument("text", nargs="?"); wh.add_argument("--file"); wh.add_argument("--dry-run", action="store_true")
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
    if a.cmd == "whisper":
        import publisher as pub
        text = open(a.file, encoding="utf-8").read() if a.file else a.text
        try:
            whisper(a.crawler, text, dry_run=a.dry_run)
        except ValueError as e:
            sys.exit(f"whisper: {e}")
        except (pub.PublishError, pub.DiscordError) as e:
            print(f"whisper: {e}", file=sys.stderr)
            sys.exit(1)
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
    elif a.cmd == "unlock":
        r = lock_release(force=a.force)
        print({"released": "released", "free": "released (no lock was held)",
               "not-yours": "NOT released: another GM run holds the turn lock (use --force only if it is stuck)"}[r])
        if r == "not-yours":
            sys.exit(1)
    elif a.cmd == "new":
        if a.lock and a.peek:
            sys.exit("new: --lock and --peek cannot be used together")
        status, msgs = read_new("lock" if a.lock else "peek" if a.peek else "auto", a.wait)
        if status == "busy":
            print("busy: another GM run holds the turn lock; nothing read, nothing marked read. That run answers; retry with --wait.")
            sys.exit(1)
        if status == "peek" and not a.peek:
            print("PEEK ONLY (not marked read): another GM run holds the turn lock and will get these lines. Do not answer them; "
                  "use `discord_gm.py new --lock --wait 90` to take the next turn.")
        if msgs:
            show(msgs)
        else:
            print("(no new player speech)")

if __name__ == "__main__":
    main()
