#!/usr/bin/env python3
"""Discord channel agent: read a text channel and post replies as a bot.

This is a separate bot from the table's GM voice bridge. It never uses
GM_DISCORD_TOKEN and it never posts to the GM channels unless those ids
are what AGENT_DISCORD_CHANNEL_ID points at.

  python3 agent-discord/discord_agent.py whoami
  python3 agent-discord/discord_agent.py read [--limit 30] [--after MESSAGE_ID]
  python3 agent-discord/discord_agent.py new
  python3 agent-discord/discord_agent.py say "hello" | --file reply.txt
  python3 agent-discord/discord_agent.py listen

Env (never print the secret values):
  AGENT_DISCORD_TOKEN          bot token
  AGENT_DISCORD_CHANNEL_ID     channel to read and post in
  AGENT_STATE_DIR              cursor files (default: agent-discord/state)
  AGENT_WAKE_URL               optional Cursor automation webhook
  AGENT_WAKE_KEY               optional bearer key for that webhook
  AGENT_POLL_SECONDS           listen poll interval (default 4)
  AGENT_WAKE_DEBOUNCE_SECONDS  wait after the last new line (default 2.5)
  AGENT_WAKE_MAX_WAIT_SECONDS  send even if lines keep arriving (default 8)

`listen` posts one wake per burst of other people's messages. `new` is a
separate cursor, so a wake does not mark those lines as already answered.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://discord.com/api/v10"
HERE = os.path.dirname(os.path.abspath(__file__))
UA = "discord-channel-agent (local, 1.0)"


class DiscordError(RuntimeError):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        url = getattr(req, "full_url", None) or "http://redacted"
        raise urllib.error.HTTPError(url, code, "redirect refused", headers, fp)


def scrub(text, secrets):
    out = text or ""
    for secret in secrets:
        if secret:
            out = out.replace(secret, "[redacted]")
    return out


def split_text(text, n=1900):
    out, cur = [], ""

    def flush():
        nonlocal cur
        if cur.strip():
            out.append(cur)
        cur = ""

    for para in text.split("\n"):
        while len(para) > n:
            flush()
            cut = para.rfind(" ", 0, n)
            if cut <= 0:
                cut = n
            out.append(para[:cut])
            para = para[cut:].lstrip()
        if not para:
            continue
        if cur and len(cur) + 1 + len(para) > n:
            flush()
        cur = (cur + "\n" + para) if cur else para
    flush()
    return out


def author_name(message):
    author = message.get("author") or {}
    return author.get("global_name") or author.get("username") or "unknown"


def message_text(message):
    content = (message.get("content") or "").strip()
    names = []
    for att in message.get("attachments") or []:
        names.append(att.get("filename") or "attachment")
    if names:
        extra = " ".join(names)
        content = (content + " " + extra).strip() if content else extra
    return content


def is_self(message, me_id):
    author = message.get("author") or {}
    return bool(me_id) and str(author.get("id") or "") == str(me_id)


def incoming(messages, me_id):
    rows = []
    for message in messages:
        if is_self(message, me_id):
            continue
        text = message_text(message)
        if not text:
            continue
        rows.append(message)
    return rows


def format_line(message):
    author = message.get("author") or {}
    flag = " [bot]" if author.get("bot") else ""
    return f"[{message.get('id')}] {author_name(message)}{flag}: {message_text(message)}"


def wake_payload(channel_id, messages):
    lines = []
    for message in messages:
        lines.append({
            "id": str(message.get("id") or ""),
            "author": author_name(message),
            "bot": bool((message.get("author") or {}).get("bot")),
            "text": message_text(message),
        })
    return {
        "event": "channel_message",
        "channel_id": str(channel_id),
        "lines": lines,
        "hint": (
            "Run: python3 agent-discord/discord_agent.py new  "
            "then reply with: python3 agent-discord/discord_agent.py say ..."
        ),
    }


class WakeBatch:
    """Hold lines until a quiet gap, or until max_wait after the first line."""

    def __init__(self, debounce_s, max_wait_s):
        self.debounce_s = debounce_s
        self.max_wait_s = max_wait_s
        self.lines = []
        self.first = None
        self.last = None
        self.pending_high = None

    def add(self, messages, now, high_id):
        if not messages:
            return
        if self.first is None:
            self.first = now
        self.last = now
        self.lines.extend(messages)
        if high_id is not None:
            self.pending_high = str(high_id)

    def ready(self, now):
        if not self.lines or self.first is None or self.last is None:
            return False
        if now - self.last >= self.debounce_s:
            return True
        return now - self.first >= self.max_wait_s

    def take(self):
        lines = self.lines
        high = self.pending_high
        self.lines = []
        self.first = None
        self.last = None
        self.pending_high = None
        return lines, high

    def restore(self, lines, high, now):
        self.lines = list(lines) + self.lines
        self.pending_high = high
        self.first = now
        self.last = now


class CursorStore:
    def __init__(self, directory):
        self.directory = directory
        self.wake_path = os.path.join(directory, "wake-cursor")
        self.read_path = os.path.join(directory, "read-cursor")

    def _read(self, path):
        try:
            with open(path, encoding="utf-8") as f:
                value = f.read().strip()
            return value or None
        except OSError:
            return None

    def _write(self, path, value):
        os.makedirs(self.directory, exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(str(value))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)

    def wake_cursor(self):
        return self._read(self.wake_path)

    def set_wake_cursor(self, message_id):
        self._write(self.wake_path, message_id)

    def read_cursor(self):
        return self._read(self.read_path)

    def set_read_cursor(self, message_id):
        self._write(self.read_path, message_id)


def http_json(method, path, token, body=None, timeout=20):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read()
            return json.loads(raw.decode() or "null")
    except urllib.error.HTTPError as e:
        detail = scrub(e.read().decode("utf-8", "replace")[:300], [token])
        raise DiscordError(f"Discord error {e.code}: {detail}") from None
    except urllib.error.URLError as e:
        raise DiscordError("Discord network error") from e


def http_status(url, body, key=None, timeout=20, opener=None):
    data = json.dumps(body).encode()
    headers = {"Content-Type": "application/json", "User-Agent": UA}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    if opener is None:
        opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(req, timeout=timeout) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code


class DiscordClient:
    def __init__(self, token, channel_id, transport=None):
        self.token = token
        self.channel_id = str(channel_id)
        self.transport = transport or http_json
        self._me = None

    def me(self):
        if self._me is None:
            self._me = self.transport("GET", "/users/@me", self.token)
        return self._me

    @property
    def me_id(self):
        return str((self.me() or {}).get("id") or "")

    def fetch(self, limit=30, after=None):
        limit = max(1, min(int(limit), 100))
        query = f"?limit={limit}" + (f"&after={after}" if after else "")
        messages = self.transport("GET", f"/channels/{self.channel_id}/messages{query}", self.token)
        if not isinstance(messages, list):
            raise DiscordError("Discord returned an unexpected message list")
        return sorted(messages, key=lambda m: int(m["id"]))

    def post(self, content):
        body = {"content": content, "allowed_mentions": {"parse": []}}
        return self.transport("POST", f"/channels/{self.channel_id}/messages", self.token, body)


def require_env():
    token = os.environ.get("AGENT_DISCORD_TOKEN")
    channel = os.environ.get("AGENT_DISCORD_CHANNEL_ID")
    missing = []
    if not token:
        missing.append("AGENT_DISCORD_TOKEN")
    if not channel:
        missing.append("AGENT_DISCORD_CHANNEL_ID")
    if missing:
        raise DiscordError("missing " + ", ".join(missing))
    return token, channel


def state_dir():
    return os.environ.get("AGENT_STATE_DIR") or os.path.join(HERE, "state")


def env_float(name, default):
    try:
        return float(os.environ.get(name, default))
    except (TypeError, ValueError):
        return float(default)


def show(messages):
    for message in messages:
        print(format_line(message))


def cmd_whoami(client):
    me = client.me()
    name = me.get("global_name") or me.get("username") or "unknown"
    print(f"Logged in as {name} id {me.get('id')} channel {client.channel_id}")


def cmd_read(client, limit, after):
    show(client.fetch(limit, after))


def cmd_new(client, store):
    last = store.read_cursor()
    messages = client.fetch(100 if last else 30, last)
    if messages:
        store.set_read_cursor(messages[-1]["id"])
    rows = incoming(messages, client.me_id)
    if rows:
        show(rows)
    else:
        print("(no new messages)")


def cmd_say(client, text):
    text = (text or "").strip()
    if not text:
        raise DiscordError("nothing to say")
    for chunk in split_text(text):
        client.post(chunk)
    print("posted")


def cmd_listen_tick(client, store, batch, now, wake_fn):
    """One listen step. Returns waiting, woke, wake_failed, quiet, or advanced."""
    if batch.lines and not batch.ready(now):
        return "waiting"
    if batch.ready(now):
        lines, high = batch.take()
        ok = True if wake_fn is None else bool(wake_fn(lines))
        if ok and high:
            store.set_wake_cursor(high)
            return "woke"
        batch.restore(lines, high, now)
        return "wake_failed"
    last = store.wake_cursor()
    messages = client.fetch(100 if last else 30, last)
    if not messages:
        return "quiet"
    high = messages[-1]["id"]
    rows = incoming(messages, client.me_id)
    if not rows:
        store.set_wake_cursor(high)
        return "advanced"
    batch.add(rows, now, high)
    return "waiting"


def make_wake_fn(url, key):
    if not url:
        def local(lines):
            for message in lines:
                print(format_line(message))
            return True
        return local

    def remote(lines):
        channel = os.environ.get("AGENT_DISCORD_CHANNEL_ID") or ""
        status = http_status(url, wake_payload(channel, lines), key)
        if 200 <= status < 300:
            print(f"wake sent: HTTP {status} ({len(lines)} lines)")
            return True
        print(f"wake failed: HTTP {status}", file=sys.stderr)
        return False

    return remote


def listen_loop(client, store, wake_fn, poll_s, debounce_s, max_wait_s, sleep=time.sleep, clock=time.monotonic):
    batch = WakeBatch(debounce_s, max_wait_s)
    while True:
        result = cmd_listen_tick(client, store, batch, clock(), wake_fn)
        if result == "wake_failed":
            sleep(min(poll_s, 5))
        else:
            sleep(poll_s)


def build_parser():
    parser = argparse.ArgumentParser(description="Discord channel agent")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami")
    read = sub.add_parser("read")
    read.add_argument("--limit", type=int, default=30)
    read.add_argument("--after")
    sub.add_parser("new")
    say = sub.add_parser("say")
    say.add_argument("text", nargs="?")
    say.add_argument("--file")
    sub.add_parser("listen")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        token, channel = require_env()
        client = DiscordClient(token, channel)
        store = CursorStore(state_dir())
        if args.cmd == "whoami":
            cmd_whoami(client)
        elif args.cmd == "read":
            cmd_read(client, args.limit, args.after)
        elif args.cmd == "new":
            cmd_new(client, store)
        elif args.cmd == "say":
            text = open(args.file, encoding="utf-8").read() if args.file else args.text
            cmd_say(client, text)
        elif args.cmd == "listen":
            wake = make_wake_fn(os.environ.get("AGENT_WAKE_URL"), os.environ.get("AGENT_WAKE_KEY"))
            listen_loop(
                client,
                store,
                wake,
                env_float("AGENT_POLL_SECONDS", 4),
                env_float("AGENT_WAKE_DEBOUNCE_SECONDS", 2.5),
                env_float("AGENT_WAKE_MAX_WAIT_SECONDS", 8),
            )
    except DiscordError as e:
        token = os.environ.get("AGENT_DISCORD_TOKEN") or ""
        key = os.environ.get("AGENT_WAKE_KEY") or ""
        print(scrub(str(e), [token, key]), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
