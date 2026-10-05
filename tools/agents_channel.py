#!/usr/bin/env python3
"""agents_channel.py - read and post in the private Discord #agents channel as the DCC AI GM bot.

  python3 tools/agents_channel.py read [--limit 20] [--since MESSAGE_ID] [--to NAME]
  python3 tools/agents_channel.py post "[GM -> Lore] text"
  python3 tools/agents_channel.py post --as Architect "[Architect -> all] text"   # posts under the agent's own webhook
  python3 tools/agents_channel.py pins

Needs env GM_DISCORD_TOKEN (same bot and env-only pattern as discord_gm.py). The token is never printed, logged
or written anywhere. Discord REST v10 over plain urllib; one retry on 429 after `retry_after`.
`post --as NAME` posts through that agent's webhook instead (AGENTS_WEBHOOK_<NAME> from env, else from
/workspace/discord-voice-bridge/.env.agents; webhook URLs are secrets and are never printed). read/pins always use
GM_DISCORD_TOKEN (webhooks cannot read). `post` refuses text that looks like a secret (scan from check_repo_safe.py plus sk-, long base64, the live token).
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_repo_safe import scan_text  # noqa: E402

API = "https://discord.com/api/v10"
CHANNEL = os.environ.get("DCC_AGENTS_CHANNEL_ID", "1556724390467735613")   # #agents, guild 1556163673469222942
CT = ZoneInfo("America/Chicago")
MAX_LEN = 2000
AGENTS = ["Accountant", "Syndicate", "Lore", "Encounter Bot", "Book Author", "Architect"]
AGENTS_FILE = os.environ.get("AGENTS_WEBHOOK_FILE", "/workspace/discord-voice-bridge/.env.agents")
WEBHOOK_URL = re.compile(r"^https://(?:ptb\.|canary\.)?discord(?:app)?\.com/api/(?:v\d+/)?webhooks/\d+/[A-Za-z0-9_-]+$")
EXTRA = [
    ("sk-style-key", re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{8,}")),
]
# Long blob candidates: runs of base64/base64url/hex/path characters. Each run is judged by looks_like_blob(), so
# ordinary paths and file names (slash/hyphen/dot-separated words) pass while unbroken blobs are still refused.
BLOB_RUN = re.compile(r"[A-Za-z0-9+/=_.-]{40,}")
AUTH_VALUE = re.compile(r"(?i)\b(?:authorization|bearer|bot)\s*[:=]?\s+([A-Za-z0-9+/=._-]{30,})")


def _random_piece(p):
    """A piece of at least 10 chars mixing upper case, lower case and digits (how base64 looks, not how words look)."""
    return len(p) >= 10 and bool(re.search(r"[A-Z]", p) and re.search(r"[a-z]", p) and re.search(r"[0-9]", p))


def looks_like_blob(run, min_unbroken=40):
    """True for an unbroken base64/hex blob (min_unbroken+ chars with no / . - _ break) or a run whose pieces are
    mostly random-looking (base64 that happens to contain / or -). Paths like floors/f01/day-01.json are words."""
    pieces = [p for p in re.split(r"[/._-]+", run) if p]
    if any(len(p) >= min_unbroken for p in pieces):
        return True
    return sum(len(p) for p in pieces if _random_piece(p)) >= 30


def blob_reasons(text):
    reasons = set()
    for m in BLOB_RUN.finditer(text):
        if looks_like_blob(m.group(0)):
            reasons.add("long-base64")
    for m in AUTH_VALUE.finditer(text):
        if looks_like_blob(m.group(1), min_unbroken=30):
            reasons.add("auth-header")
    return reasons


class ApiError(Exception):
    pass


def _open(req):   # the only network call; tests mock this
    return urllib.request.urlopen(req, timeout=20)


def call(method, path, body=None, _retry=True, url=None):
    """REST call with the GM bot token, or (url=...) a webhook call with no Authorization header."""
    headers = {"Content-Type": "application/json", "User-Agent": "DCC-GM (local, 1.0)"}
    if url is None:
        tok = os.environ.get("GM_DISCORD_TOKEN")
        if not tok:
            raise ApiError("GM_DISCORD_TOKEN is not set")
        headers["Authorization"] = f"Bot {tok}"
    req = urllib.request.Request(url or API + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None, headers=headers)
    try:
        with _open(req) as r:
            raw = r.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        text = e.read().decode("utf-8", "replace")
        if e.code == 429 and _retry:
            try:
                wait = float(json.loads(text).get("retry_after", 1))
            except (ValueError, AttributeError):
                wait = float(e.headers.get("Retry-After", 1) if e.headers else 1)
            time.sleep(min(max(wait, 0), 60))
            return call(method, path, body, _retry=False, url=url)
        raise ApiError(f"Discord error {e.code}: {text[:300]}")
    except urllib.error.URLError as e:
        raise ApiError(f"network error: {type(e.reason).__name__}")   # never echo a webhook URL


def agent_key(name):
    return "AGENTS_WEBHOOK_" + re.sub(r"[^A-Z0-9]+", "_", str(name).upper()).strip("_")


def webhook_for(name):
    """(display name, url) for an agent; env AGENTS_WEBHOOK_<NAME> overrides the .env.agents file."""
    key = agent_key(name)
    agent = next((a for a in AGENTS if agent_key(a) == key), None)
    if not agent:
        raise ApiError(f'unknown agent "{name}". Valid names: {", ".join(AGENTS)}.')
    url = os.environ.get(key)
    if not url:
        try:
            with open(AGENTS_FILE, encoding="utf-8") as f:
                for ln in f:
                    k, sep, v = ln.strip().partition("=")
                    if sep and k.strip() == key:
                        url = v.strip().strip("'\"")
        except OSError:
            pass
    if not url or not WEBHOOK_URL.match(url):
        raise ApiError(f"no valid webhook for {agent} ({key} missing or malformed in env / {AGENTS_FILE}). Nothing was posted.")
    return agent, url


def secret_reasons(text):
    reasons = {name for _, name in scan_text(text)}
    reasons |= {name for name, rx in EXTRA if rx.search(text)}
    reasons |= blob_reasons(text)
    tok = os.environ.get("GM_DISCORD_TOKEN")
    if tok and tok in text:
        reasons.add("the GM bot token itself")
    if re.search(r"webhooks/\d+/[A-Za-z0-9_-]{20,}", text):
        reasons.add("webhook URL")
    return sorted(reasons)


def when(ts):
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(CT).strftime("%Y-%m-%d %H:%M CT")
    except (AttributeError, ValueError):
        return "? CT"


def line(m):
    a = m.get("author") or {}
    content = m.get("content") or ""
    extras = [f"(attachment: {x.get('filename', '?')})" for x in m.get("attachments") or []]
    if m.get("embeds") and not content:
        extras.append("(embed)")
    if not content and not extras:
        extras.append(SYSTEM_TYPES.get(m.get("type"), f"(system message, type {m.get('type', '?')})"))
    text = " ".join([content] + extras).strip()
    return f"[{when(m.get('timestamp'))}] {a.get('global_name') or a.get('username') or '?'}: {text}"


SYSTEM_TYPES = {6: "(pinned a message)", 7: "(joined)", 18: "(started a thread)"}
ROUTE = re.compile(r"^\s*\[([^\]\n]+?)\s*(?:->|→)\s*([^\]\n]+)\]")


def addressed_to(content, name):
    m = ROUTE.match(content or "")
    if not m:
        return False
    names = [n.strip().lower() for n in re.split(r"[,/&+]|\band\b", m.group(2)) if n.strip()]
    return name.strip().lower() in names


def cmd_read(a):
    q = f"?limit={a.limit}" + (f"&after={a.since}" if a.since else "")
    msgs = sorted(call("GET", f"/channels/{CHANNEL}/messages{q}") or [], key=lambda m: int(m["id"]))
    if a.to:
        msgs = [m for m in msgs if addressed_to(m.get("content"), a.to)]
    for m in msgs:
        print(line(m))
    if not msgs:
        print("(no messages)", file=sys.stderr)


def cmd_post(a):
    text = (a.text or "").strip()
    if not text:
        raise ApiError("nothing to post")
    if len(text) > MAX_LEN:
        raise ApiError(f"message is {len(text)} characters; Discord's limit is {MAX_LEN} (post one message only)")
    why = secret_reasons(text)
    if why:
        raise ApiError("refused: the text looks like it contains a secret (" + ", ".join(why) + "). Nothing was posted.")
    body = {"content": text, "allowed_mentions": {"parse": []}}
    if a.as_agent:
        agent, url = webhook_for(a.as_agent)
        m = call("POST", None, dict(body, username=agent), url=url + "?wait=true") or {}
        print(f"posted as {agent} (message {m.get('id', '?')})")
        return
    m = call("POST", f"/channels/{CHANNEL}/messages", body)
    print(f"posted (message {m.get('id', '?')})")


def cmd_pins(a):
    res = call("GET", f"/channels/{CHANNEL}/pins") or []
    msgs = [x.get("message", x) for x in (res.get("items", []) if isinstance(res, dict) else res)]
    for m in sorted(msgs, key=lambda m: int(m["id"])):
        print(line(m))
    if not msgs:
        print("(no pinned messages)", file=sys.stderr)


def snowflake(s):
    if not re.fullmatch(r"\d{15,21}", s):
        raise argparse.ArgumentTypeError("must be a Discord message id (digits)")
    return s


def limit(s):
    n = int(s)
    if not 1 <= n <= 100:
        raise argparse.ArgumentTypeError("must be 1 to 100")
    return n


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read/post in the private #agents Discord channel (GM bot).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("read")
    r.add_argument("--limit", type=limit, default=20)
    r.add_argument("--since", type=snowflake, help="only messages after this message id")
    r.add_argument("--to", help="only lines whose [FROM -> TO] prefix names this recipient")
    p = sub.add_parser("post")
    p.add_argument("text")
    p.add_argument("--as", dest="as_agent", metavar="NAME", help="post through this agent's webhook: " + ", ".join(AGENTS))
    sub.add_parser("pins")
    a = ap.parse_args(argv)
    try:
        {"read": cmd_read, "post": cmd_post, "pins": cmd_pins}[a.cmd](a)
    except ApiError as e:
        print(f"agents_channel: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
