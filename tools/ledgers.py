"""Per-session append-only JSONL ledgers next to state.json: box ledger, loot ledger, banner archive, story-box (deed registry) ledger.

All paths follow campaign_session.data_dir(), so alpha writes to sessions/ and beta to sessions-data/beta/. Appends are single
write() calls in O_APPEND mode (atomic for lines this small), so concurrent GM tools cannot interleave a line."""
import json
import os
import time

import campaign_session as csession

FILES = {"box": "box-ledger.jsonl", "loot": "loot-ledger.jsonl", "banner": "banner-archive.jsonl",
         "story-box": "story-box-ledger.jsonl", "swap": "swap-log.jsonl", "delete": "delete-log.jsonl", "swap-request": "swap-requests.jsonl", "pet": "pet-log.jsonl"}


def path(kind):
    return os.path.join(csession.data_dir(), FILES[kind])


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")[:-2] + ":" + time.strftime("%z")[-2:]


def append(kind, entry):
    entry = {"ts": now_iso(), "session": csession.session_id(), **entry}
    p = path(kind)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n"
    fd = os.open(p, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        os.write(fd, line.encode("utf-8"))
    finally:
        os.close(fd)
    return entry


def read(kind):
    out = []
    try:
        with open(path(kind), encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                    if isinstance(e, dict):
                        out.append(e)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return out
