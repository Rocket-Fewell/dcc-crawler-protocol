"""SQLite persistence. Files live under engine-data/ and are git-ignored."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def data_dir():
    raw = os.environ.get("ENGINE_DATA_DIR")
    path = Path(raw) if raw else ROOT / "engine-data"
    path.mkdir(parents=True, exist_ok=True)
    return path


class Store:
    def __init__(self, campaign="f01"):
        self.path = data_dir() / ("%s.sqlite" % campaign)
        self.conn = sqlite3.connect(self.path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS actions (id INTEGER PRIMARY KEY, kind TEXT, payload TEXT)"
        )
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS snapshot (id INTEGER PRIMARY KEY CHECK (id = 1), payload TEXT)"
        )
        self.conn.commit()

    def save_action(self, kind, payload):
        self.conn.execute(
            "INSERT INTO actions (kind, payload) VALUES (?, ?)",
            (kind, json.dumps(payload, ensure_ascii=False)),
        )
        self.conn.execute(
            "INSERT INTO snapshot (id, payload) VALUES (1, ?) ON CONFLICT(id) DO UPDATE SET payload = excluded.payload",
            (json.dumps(payload, ensure_ascii=False),),
        )
        self.conn.commit()
        return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    def close(self):
        self.conn.close()
