#!/usr/bin/env python3
"""state.py - live campaign state manager for the DCC 5e campaign (stdlib only).

State file: <campaign>/sessions/state.json   (campaign dir: $DCC_CAMPAIGN_DIR, default /workspace/dcc-campaign)

Every write: takes a lock file -> validates the NEW state -> copies the old state.json to
sessions/backups/state-<timestamp>.json (newest 20 kept) -> writes a temp file, re-reads it,
and atomically renames it over state.json. Invalid input never overwrites the state.

Exit codes: 0 ok | 1 refused/failed (message on stderr) | 2 usage error.
Run `python3 tools/state.py --help` or see tools/README.md.
"""
import argparse
import copy
import datetime as dt
from fractions import Fraction
import json
import os
import random
import re
import shutil
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import campaign_session as csession
import repair_log  # sealed, hash-chained repair log (gm-notes/secret/repair-log.jsonl)
import gm_quirks  # GM-only secret traits + affinity (gm-notes/secret/); see tools/README.md
import ledgers
import loot

DEFAULT_CAMPAIGN_DIR = "/workspace/dcc-campaign"
SCHEMA_VERSION = 1
BACKUP_KEEP = 20
LOCK_TIMEOUT_S = 10.0
LOCK_STALE_S = 60.0
BOX_TIERS = ["bronze", "silver", "gold", "platinum", "legendary", "celestial"]
ABILITIES = ["str", "dex", "con", "int", "wis", "cha"]

SESSION_REOPEN_GRACE_S = 30 * 60   # a session re-opened this soon after a close is the same session (same swap window)

DEFAULT_LIMITS = {
    "revive_party_cooldown_floors": 3,   # 1 revive per party per 3 floors
    "revive_campaign_cap": 3,            # 3 per campaign
    "revive_per_crawler_cap": 1,         # 1 per crawler, ever
    "bypass_per_crawler_cap": None,      # null = uncapped (set a number to enforce)
    "max_crawlers": 4,                   # party cap enforced by create-crawler (decision 013); only kind=player crawlers count
    "legendary_enabled": True,           # Legendary Story Boxes approved by Caleb 2026-10-04 (rules/40 section 2.8); false = refuse them
    "story_box_rota": "warn",            # rules/45 section 6.1: warn-only (Caleb: the rota never blocks)
    "pets_enabled": True,                # GM-run plain pets (decision 022): false = `pet add` and `pet shop` are refused and cards/party hide pets (data is kept)
    "legendary_cap_per_floor": 1,        # Story Boxes per table per FLOOR (unopened boxes count; loot story-box --override-cap "reason" to exceed)
}


class StateError(Exception):
    """A refused or failed operation (printed to stderr, exit 1)."""


# --------------------------------------------------------------------------- paths / time

def campaign_dir():
    return os.environ.get("DCC_CAMPAIGN_DIR") or DEFAULT_CAMPAIGN_DIR


def sessions_dir():
    """This SESSION's data dir: <campaign>/sessions/ for "alpha" (default), <campaign>/sessions-data/<id>/ otherwise."""
    return csession.data_dir()


def state_path():
    return os.path.join(sessions_dir(), "state.json")


def backups_dir():
    return os.path.join(sessions_dir(), "backups")


def lock_path():
    return os.path.join(sessions_dir(), ".state.lock")


def ledger_path():
    return os.path.join(sessions_dir(), "credit-ledger.jsonl")


def now_iso():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


# --------------------------------------------------------------------------- locking

class FileLock:
    """Exclusive lock file (O_CREAT|O_EXCL) with stale-lock recovery."""

    def __init__(self, path, timeout=LOCK_TIMEOUT_S, stale=LOCK_STALE_S):
        self.path, self.timeout, self.stale = path, timeout, stale
        self.fd = None

    def _is_stale(self):
        try:
            age = time.time() - os.path.getmtime(self.path)
            if age > self.stale:
                return True
            with open(self.path) as f:
                pid = int(f.read().split()[0])
            if pid == os.getpid():
                return False
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return True
            except (PermissionError, OSError):
                return False
        except (FileNotFoundError, ValueError, IndexError):
            return False
        return False

    def __enter__(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        deadline = time.time() + self.timeout
        while True:
            try:
                self.fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
                os.write(self.fd, f"{os.getpid()} {time.time():.3f}\n".encode())
                return self
            except FileExistsError:
                if self._is_stale():
                    try:
                        os.unlink(self.path)
                    except FileNotFoundError:
                        pass
                    continue
                if time.time() >= deadline:
                    raise StateError(f"state is locked by another process ({self.path}); try again")
                time.sleep(0.05)

    def __exit__(self, *exc):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
            try:
                os.unlink(self.path)
            except FileNotFoundError:
                pass
        return False


# --------------------------------------------------------------------------- safe read / write

def read_state_file(path=None, missing_ok=False):
    path = path or state_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    except FileNotFoundError:
        if missing_ok:
            return None
        raise StateError(f"no state file at {path} - run `state.py init` first")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise StateError(f"{path} is not valid JSON ({e}); refusing to continue. Fix it or `state.py restore <backup>`")
    if not isinstance(data, dict):
        raise StateError(f"{path} must contain a JSON object")
    return data


def _backup_existing(path):
    """Copy the existing state.json into sessions/backups/ and rotate (keep newest BACKUP_KEEP)."""
    if not os.path.exists(path):
        return None
    os.makedirs(backups_dir(), exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    dest = os.path.join(backups_dir(), f"state-{stamp}.json")
    n = 1
    while os.path.exists(dest):
        n += 1
        dest = os.path.join(backups_dir(), f"state-{stamp}-{n}.json")
    shutil.copy2(path, dest)
    if os.path.getsize(dest) != os.path.getsize(path):
        raise StateError("backup copy size mismatch; aborting write")
    for old in list_backups()[:-BACKUP_KEEP]:
        try:
            os.unlink(old)
        except OSError:
            pass
    return dest


def list_backups():
    d = backups_dir()
    if not os.path.isdir(d):
        return []
    return sorted(os.path.join(d, f) for f in os.listdir(d) if re.fullmatch(r"state-.*\.json", f))


def atomic_write_json(path, data):
    """Write JSON via temp file + fsync + verify + rename. Never leaves a partial file at `path`."""
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    json.loads(text)  # validate JSON before touching anything
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        with open(tmp, "r", encoding="utf-8") as f:
            if json.load(f) != data:
                raise StateError("temp file verification failed; state not changed")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise
    try:  # best-effort directory fsync
        dfd = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    except OSError:
        pass


# --------------------------------------------------------------------------- credit ledger
# Append-only sessions/credit-ledger.jsonl: one line for EVERY credit change made through mutate() (credits,
# set, add-crawler, restore, ...): {seq, ts, crawler, delta, balance, reason, source, command}.
# `ledger verify` checks the running totals against the sum of the entries and against state.json.

_RUN = {"reason": None, "source": "", "command": "", "ledger_extra": None, "row_extra": None, "force_rows": None}  # set by main() from --reason / --source


def _credit_map(state):
    out = {}
    if isinstance(state, dict) and isinstance(state.get("crawlers"), list):
        for c in state["crawlers"]:
            if isinstance(c, dict) and isinstance(c.get("name"), str) and _is_int(c.get("credits")):
                out[c["name"]] = c["credits"]
    return out


def read_ledger(path=None):
    """Return (entries, bad_lines). Missing file = empty ledger."""
    path = path or ledger_path()
    entries, bad = [], []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    e = json.loads(line)
                    if not (isinstance(e, dict) and isinstance(e.get("crawler"), str) and _is_int(e.get("delta")) and _is_int(e.get("balance"))):
                        raise ValueError("missing crawler/delta/balance")
                    entries.append(e)
                except ValueError:
                    bad.append(n)
    except FileNotFoundError:
        pass
    return entries, bad


def archive_dir():
    return os.path.join(csession.data_dir(), "deleted-archive")


def archived_rows():
    """-> {archive file name: [(line_no, row or None)]} for every deleted-archive/*-ledger-rows.jsonl."""
    out = {}
    d = archive_dir()
    try:
        names = sorted(n for n in os.listdir(d) if n.endswith("-ledger-rows.jsonl"))
    except OSError:
        return out
    for n in names:
        rows = []
        with open(os.path.join(d, n), encoding="utf-8") as f:
            for i, l in enumerate(f, 1):
                if l.strip():
                    try:
                        rows.append((i, json.loads(l)))
                    except ValueError:
                        rows.append((i, None))
        out[n] = rows
    return out


def archived_max_seq():
    return max([r["seq"] for rs in archived_rows().values() for _i, r in rs if isinstance(r, dict) and _is_int(r.get("seq"))] or [0])


def append_ledger(rows):
    """Append rows (dicts without seq) to the ledger; call while holding the state lock. Returns the written entries."""
    if not rows:
        return []
    path = ledger_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    existing, bad = read_ledger(path)
    seq = max(max([e.get("seq", 0) for e in existing if _is_int(e.get("seq"))] or [len(existing) + len(bad)]), archived_max_seq())   # never reuse a seq that sits in the deleted-archive
    out = []
    with open(path, "a", encoding="utf-8") as f:
        for r in rows:
            seq += 1
            entry = {"seq": seq, **r}
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            out.append(entry)
        f.flush()
        os.fsync(f.fileno())
    return out


def ledger_rows_for_change(old_state, new_state):
    """One ledger row per crawler whose credits differ between the two states."""
    before, after = _credit_map(old_state), _credit_map(new_state)
    reason = (_RUN.get("reason") or "").strip()
    rows = []
    force = set(_RUN.get("force_rows") or ())          # floor-lost / loot-body: a row even when the balance did not move (items only), so the event is always on record
    for name, bal in after.items():
        prev = before.get(name, 0)
        if bal == prev and name not in force:
            continue
        rows.append({
            "ts": now_iso(), "crawler": name, "delta": bal - prev, "balance": bal,
            "reason": reason or "unspecified", "source": (_RUN.get("source") or "").strip(),
            "command": _RUN.get("command") or "",
            **({"provenance": _RUN["ledger_extra"].get(name) or _RUN["ledger_extra"].get("*")} if _RUN.get("ledger_extra") and (_RUN["ledger_extra"].get(name) or _RUN["ledger_extra"].get("*")) else {}),
            **{k: v for k, v in ((_RUN.get("row_extra") or {}).get(name) or {}).items() if k not in ("ts", "crawler", "delta", "balance", "reason", "source", "command", "seq")},
        })
    return rows, not reason


def mutate(fn, allow_missing=False, allow_corrupt=False):
    """Locked read-modify-write. fn(state_or_None) -> (new_state, result). Validates before writing."""
    with FileLock(lock_path()):
        path = state_path()
        if allow_corrupt:
            try:
                current = read_state_file(path, missing_ok=True)
            except StateError:
                current = None
        else:
            current = read_state_file(path, missing_ok=allow_missing)
        new_state, result = fn(copy.deepcopy(current) if current is not None else None)
        errors, _ = validate_state(new_state)
        if errors:
            raise StateError("refusing to write - resulting state is invalid:\n  - " + "\n  - ".join(errors))
        new_state.setdefault("campaign", {})["updated"] = now_iso()
        _backup_existing(path)
        atomic_write_json(path, new_state)
        _RUN["wrote"] = True
        # The state is the source of truth; a ledger problem must never undo or hide a state change.
        try:
            rows, unspecified = ledger_rows_for_change(current, new_state)
            _RUN["row_extra"] = _RUN["force_rows"] = None   # one-shot: never leak into the next command of the same process
            append_ledger(rows)
            if rows and unspecified:
                print("warning: no --reason given for the credit change; recorded as 'unspecified' (add --reason \"...\")", file=sys.stderr)
        except OSError as e:
            print(f"warning: state saved, but the credit ledger could not be written ({e}); run `ledger verify`", file=sys.stderr)
        return result


# --------------------------------------------------------------------------- schema

def new_state(floor=1, zone="", name="Dungeon Crawler Carl 5e (2024)"):
    return {
        "schema_version": SCHEMA_VERSION,
        "campaign": {
            "name": name,
            "current_floor": floor,
            "zone": zone,
            "death_mode": "Costly Revives",
            "comfort": "Ludicrous",
            "created": now_iso(),
            "updated": now_iso(),
        },
        "party": {"revives_used": 0, "last_revive_floor": None, "revive_log": [], "bypasses_used": 0, "bypass_log": []},
        "limits": dict(DEFAULT_LIMITS),
        "crawlers": [],
    }


def new_crawler(name, player, cls, species, level=1, hp_max=10, ac=10, credits=0, abilities=None):
    return {
        "name": name, "player": player, "class": cls, "species": species,
        "level": level, "xp": 0,
        "hp": {"current": hp_max, "max": hp_max, "temp": 0},
        "hit_dice": {"current": level, "max": level},
        "ac": ac,
        "abilities": {a: 10 for a in ABILITIES} | (abilities or {}),
        "inventory": [], "credits": credits, "conditions": [], "vows": [], "boons": [], "achievements": [],
        "boxes": {t: 0 for t in BOX_TIERS},
        "revives_used": 0, "bypasses_used": 0,
        "fan_profile": {"quirks": [], "notes": "", "opt_outs": []},
        "death_saves": {"successes": 0, "fails": 0},
        "notes": "",
    }


CRAWLER_KINDS = ("player", "pet", "companion", "pet-crawler")


def crawler_kind(c):
    """Missing kind = player (alpha crawlers pre-date the field)."""
    return c.get("kind") or "player"


def crawler_status(c):
    """active|benched for kind player and pet-crawler (missing = active, alpha pre-dates the field); '' for pets and companions."""
    if crawler_kind(c) not in ("player", "pet-crawler"):
        return ""
    return "benched" if c.get("status") == "benched" else "active"


def is_active(c):
    return crawler_status(c) == "active"


def player_crawler_count(state):
    """Party slots in use: ACTIVE kind=player crawlers only (benched Crawlers, pets, companions and pet-crawlers take no slot)."""
    return sum(1 for c in state["crawlers"] if crawler_kind(c) == "player" and is_active(c))


def same_player(a, b):
    """Two crawler records belong to one human: same Discord user id when both have one, else the same player name."""
    ia, ib = (a.get("build") or {}).get("discord_user_id"), (b.get("build") or {}).get("discord_user_id")
    if ia and ib:
        return str(ia) == str(ib)
    return str(a.get("player", "")).strip().lower() == str(b.get("player", "")).strip().lower() and bool(str(a.get("player", "")).strip())


def players_active_crawler(state, like, exclude=None):
    """The active kind=player crawler of the same human as `like` (other than `exclude`), or None."""
    for c in state["crawlers"]:
        if c is exclude or c["name"] == (exclude or {}).get("name"):
            continue
        if crawler_kind(c) == "player" and is_active(c) and same_player(c, like):
            return c
    return None


def assign_status(state, c, want=None):
    """New Crawlers start BENCHED unless it is the human's first (auto-active). Pet-crawlers follow their owner. Sets c['status']."""
    kind = crawler_kind(c)
    if kind not in ("player", "pet-crawler"):
        return None
    if kind == "pet-crawler":
        owner = next((x for x in state["crawlers"] if x["name"].lower() == str(c.get("owner", "")).lower()), None)
        c["status"] = crawler_status(owner) if owner else "benched"
        return c["status"]
    # B2 (audit): ANY other Crawler of this human on file (active, benched or dead) means the new one starts BENCHED; only a human with no Crawler at all gets an active first one.
    # Activating a replacement goes through `crawler activate` (swap rules + log).
    if want == "benched" or players_active_crawler(state, c) or any(x is not c and crawler_kind(x) == "player" and same_player(x, c) for x in state["crawlers"]):
        c["status"] = "benched"
    else:
        c["status"] = "active"
    return c["status"]


def require_active(c, what, a=None):
    """Benched Crawlers earn nothing and move nothing: no credits, XP, loot or boxes (GM correction: --benched-ok "reason"), no sell or transfer (no override)."""
    if crawler_status(c) == "benched" and not (a is not None and (getattr(a, "benched_ok", None) or "").strip()):
        raise StateError(f"REFUSED: {c['name']} is benched, so it cannot {what}. Only a player's ACTIVE Crawler takes part in the session. "
                         "Swap between sessions with `state.py crawler activate NAME --reason ...`" + ("" if what.startswith(("sell", "trade", "receive")) else "; a GM correction needs --benched-ok \"reason\""))


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def validate_state(state):
    """Return (errors, warnings)."""
    errs, warns = [], []
    if not isinstance(state, dict):
        return ["state is not an object"], warns
    if state.get("schema_version") != SCHEMA_VERSION:
        errs.append(f"schema_version must be {SCHEMA_VERSION}")
    camp = state.get("campaign")
    if not isinstance(camp, dict):
        errs.append("campaign must be an object")
    else:
        if not _is_int(camp.get("current_floor")) or camp["current_floor"] < 1:
            errs.append("campaign.current_floor must be an integer >= 1")
        for k in ("zone", "death_mode", "comfort"):
            if not isinstance(camp.get(k), str):
                errs.append(f"campaign.{k} must be a string")
    limits = state.get("limits")
    if not isinstance(limits, dict):
        errs.append("limits must be an object")
        limits = dict(DEFAULT_LIMITS)
    else:
        for k in ("revive_party_cooldown_floors", "revive_campaign_cap", "revive_per_crawler_cap"):
            if not _is_int(limits.get(k)) or limits[k] < 0:
                errs.append(f"limits.{k} must be an integer >= 0")
        if "legendary_enabled" in limits and not isinstance(limits["legendary_enabled"], bool):
            errs.append("limits.legendary_enabled must be true or false")
        if "pets_enabled" in limits and not isinstance(limits["pets_enabled"], bool):
            errs.append("limits.pets_enabled must be true or false")
        if limits.get("story_box_rota", "warn") != "warn":
            errs.append("limits.story_box_rota must be \"warn\" (the rota never blocks)")
        for k in ("max_crawlers", "legendary_cap_per_floor"):
            if k in limits and (not _is_int(limits[k]) or limits[k] < 0):
                errs.append(f"limits.{k} must be an integer >= 0")
        b = limits.get("bypass_per_crawler_cap")
        if b is not None and (not _is_int(b) or b < 0):
            errs.append("limits.bypass_per_crawler_cap must be null or an integer >= 0")
    party = state.get("party")
    if not isinstance(party, dict):
        errs.append("party must be an object")
        party = {}
    else:
        if not _is_int(party.get("revives_used")) or party["revives_used"] < 0:
            errs.append("party.revives_used must be an integer >= 0")
        elif _is_int(limits.get("revive_campaign_cap")) and party["revives_used"] > limits["revive_campaign_cap"]:
            errs.append(f"party.revives_used ({party['revives_used']}) exceeds campaign cap ({limits['revive_campaign_cap']})")
        lrf = party.get("last_revive_floor")
        if lrf is not None and (not _is_int(lrf) or lrf < 1):
            errs.append("party.last_revive_floor must be null or an integer >= 1")
    crawlers = state.get("crawlers")
    if not isinstance(crawlers, list):
        errs.append("crawlers must be an array")
        return errs, warns
    seen = set()
    for i, c in enumerate(crawlers):
        where = f"crawlers[{i}]"
        if not isinstance(c, dict):
            errs.append(f"{where} must be an object")
            continue
        nm = c.get("name")
        if not isinstance(nm, str) or not nm.strip():
            errs.append(f"{where}.name must be a non-empty string")
            continue
        where = f"crawler '{nm}'"
        if nm.lower() in seen:
            errs.append(f"duplicate crawler name '{nm}'")
        seen.add(nm.lower())
        for k in ("player", "class", "species", "notes"):
            if not isinstance(c.get(k), str):
                errs.append(f"{where}: {k} must be a string")
        if not _is_int(c.get("level")) or not 1 <= c["level"] <= 20:
            errs.append(f"{where}: level must be an integer 1-20")
        for k in ("xp", "ac", "revives_used", "bypasses_used"):
            if not _is_int(c.get(k)) or c[k] < 0:
                errs.append(f"{where}: {k} must be an integer >= 0")
        if not _is_int(c.get("credits")):
            errs.append(f"{where}: credits must be an integer")
        hp = c.get("hp")
        if not isinstance(hp, dict) or not all(_is_int(hp.get(k)) for k in ("current", "max", "temp")):
            errs.append(f"{where}: hp must be {{current,max,temp}} integers")
        else:
            if hp["max"] < 1:
                errs.append(f"{where}: hp.max must be >= 1")
            if not 0 <= hp["current"] <= hp["max"]:
                errs.append(f"{where}: hp.current ({hp['current']}) must be between 0 and hp.max ({hp['max']})")
            if hp["temp"] < 0:
                errs.append(f"{where}: hp.temp must be >= 0")
        hd = c.get("hit_dice")
        if not isinstance(hd, dict) or not all(_is_int(hd.get(k)) for k in ("current", "max")):
            errs.append(f"{where}: hit_dice must be {{current,max}} integers")
        elif not 0 <= hd["current"] <= hd["max"]:
            errs.append(f"{where}: hit_dice.current must be between 0 and hit_dice.max")
        ab = c.get("abilities")
        if not isinstance(ab, dict) or not all(_is_int(ab.get(a)) and 1 <= ab[a] <= 30 for a in ABILITIES):
            errs.append(f"{where}: abilities must have integer {'/'.join(ABILITIES)} each 1-30")
        for k in ("inventory", "conditions", "vows", "boons", "achievements"):
            if not isinstance(c.get(k), list):
                errs.append(f"{where}: {k} must be an array")
        for it in c.get("inventory", []) if isinstance(c.get("inventory"), list) else []:
            if not (isinstance(it, dict) and isinstance(it.get("name"), str) and _is_int(it.get("qty")) and it["qty"] >= 1):
                errs.append(f"{where}: inventory items must be {{name, qty>=1}} (got {json.dumps(it)[:60]})")
        for it in c.get("conditions", []) if isinstance(c.get("conditions"), list) else []:
            if not isinstance(it, str):
                errs.append(f"{where}: conditions must be strings")
        for it in c.get("achievements", []) if isinstance(c.get("achievements"), list) else []:
            if not (isinstance(it, dict) and isinstance(it.get("name"), str)):
                errs.append(f"{where}: achievements must be objects with a name")
        bx = c.get("boxes")
        if not isinstance(bx, dict) or not all(_is_int(bx.get(t)) and bx[t] >= 0 for t in BOX_TIERS):
            errs.append(f"{where}: boxes must have integer counts >= 0 for {', '.join(BOX_TIERS)}")
        elif bx["celestial"] > 1:
            warns.append(f"{where}: holds {bx['celestial']} Celestial boxes (rules: ONE per crawler per campaign)")
        fp = c.get("fan_profile")
        if not (isinstance(fp, dict) and isinstance(fp.get("quirks"), list) and isinstance(fp.get("notes"), str)
                and isinstance(fp.get("opt_outs"), list)):
            errs.append(f"{where}: fan_profile must be {{quirks[], notes, opt_outs[]}}")
        elif not all(isinstance(o, str) or (isinstance(o, dict) and isinstance(o.get("topic"), str)) for o in fp["opt_outs"]):
            errs.append(f"{where}: fan_profile.opt_outs items must be strings or {{kind, topic, shared}} objects")
        if c.get("kind", "player") not in CRAWLER_KINDS:
            errs.append(f"{where}: kind must be one of {', '.join(CRAWLER_KINDS)}")
        if c.get("status") is not None and c["status"] not in ("active", "benched"):
            errs.append(f"{where}: status must be \"active\" or \"benched\"")
        if c.get("kind", "player") in ("player", "pet-crawler") and "status" not in c:
            warns.append(f"{where}: no status field (treated as active); run `state.py crawler migrate`")
        if "pet" in c and crawler_kind(c) == "player":   # (a pet-Crawler's own "pet" key is just the converted pet's name)
            errs.extend(f"{where}: {m}" for m in _pet_errors(c))
        if "build" in c and not isinstance(c["build"], dict):
            errs.append(f"{where}: build must be an object")
        if "death_saves" in c and not (isinstance(c["death_saves"], dict) and _is_int(c["death_saves"].get("successes")) and _is_int(c["death_saves"].get("fails"))):
            errs.append(f"{where}: death_saves must be {{successes, fails}} integers")
        if _is_int(c.get("revives_used")) and _is_int(limits.get("revive_per_crawler_cap")) and c["revives_used"] > limits["revive_per_crawler_cap"]:
            errs.append(f"{where}: revives_used ({c['revives_used']}) exceeds per-crawler cap ({limits['revive_per_crawler_cap']})")
    live = [c for c in crawlers if isinstance(c, dict) and isinstance(c.get("name"), str) and c.get("kind", "player") == "player" and c.get("status") != "benched"]
    for i, c in enumerate(live):
        for o in live[i + 1:]:
            if same_player(c, o):
                errs.append(f"player {c.get('player')!r} has two ACTIVE Crawlers ({c['name']}, {o['name']}); only one may be active (state.py crawler activate)")
    total = sum(c["revives_used"] for c in crawlers if isinstance(c, dict) and _is_int(c.get("revives_used")))
    if _is_int(party.get("revives_used")) and total != party["revives_used"]:
        warns.append(f"party.revives_used ({party['revives_used']}) != sum of crawler revives_used ({total})")
    return errs, warns


# --------------------------------------------------------------------------- lookup helpers

def find_crawler(state, name):
    crawlers = state["crawlers"]
    low = name.strip().lower()
    exact = [c for c in crawlers if c["name"].lower() == low]
    if exact:
        return exact[0]
    partial = [c for c in crawlers if low in c["name"].lower()]
    if len(partial) == 1:
        return partial[0]
    if not partial:
        for c in crawlers:
            pet = c.get("pet") if isinstance(c.get("pet"), dict) else None
            if pet and str(pet.get("name", "")).strip().lower() == low:
                raise StateError(f"'{pet['name']}' is {c['name']}'s pet, not a Crawler: a pet takes no credits, XP, loot, trades or sales and has no ledger (GM-run; see `state.py pet show {c['name']}`)")
        raise StateError(f"no crawler named '{name}' (have: {', '.join(c['name'] for c in crawlers) or 'none'})")
    raise StateError(f"'{name}' is ambiguous: {', '.join(c['name'] for c in partial)}")


def _step(node, key, create=False):
    """Resolve one dotted-path segment inside node; returns (container, key) usable for get/set."""
    if isinstance(node, dict):
        if key in node or create:
            return node, key
        ci = [k for k in node if k.lower() == key.lower()]
        if len(ci) == 1:
            return node, ci[0]
        raise StateError(f"no key '{key}' (keys: {', '.join(map(str, node))})")
    if isinstance(node, list):
        if key.lstrip("-").isdigit():
            i = int(key)
            if -len(node) <= i < len(node):
                return node, i
            raise StateError(f"index {i} out of range (len {len(node)})")
        named = [i for i, x in enumerate(node) if isinstance(x, dict) and str(x.get("name", "")).lower() == key.lower()]
        if len(named) == 1:
            return node, named[0]
        raise StateError(f"no list item '{key}' (use an index or an item name)")
    raise StateError(f"cannot descend into a {type(node).__name__} at '{key}'")


def get_path(state, path):
    node = state
    for key in path.split("."):
        container, k = _step(node, key)
        node = container[k]
    return node


def set_path(state, path, value):
    keys = path.split(".")
    node = state
    for key in keys[:-1]:
        container, k = _step(node, key)
        node = container[k]
    last = keys[-1]
    if isinstance(node, list) and last == "-":
        node.append(value)
        return
    if isinstance(node, dict):
        container, k = _step(node, last, create=True)
        if k not in node:  # case-insensitive match for existing keys only
            ci = [x for x in node if x.lower() == last.lower()]
            k = ci[0] if len(ci) == 1 else last
        node[k] = value
        return
    container, k = _step(node, last)
    container[k] = value


def parse_value(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _positive(n, what="amount"):
    if n < 0:
        raise StateError(f"{what} must be >= 0")
    return n


def _hp_line(c):
    hp = c["hp"]
    return f"{c['name']}: HP {hp['current']}/{hp['max']}" + (f" (+{hp['temp']} temp)" if hp["temp"] else "")


# --------------------------------------------------------------------------- commands
# Each handler returns (data_dict, text).

def cmd_init(a):
    def fn(cur):
        if cur is not None and not a.force:
            raise StateError("state.json already exists; use --force to replace it (the old file is backed up first)")
        return new_state(a.floor, a.zone), None
    mutate(fn, allow_missing=True, allow_corrupt=a.force)
    return {"ok": True, "path": state_path()}, f"initialized {state_path()}"


def cmd_add_crawler(a):
    abilities = {}
    if a.abilities:
        for part in a.abilities.split(","):
            k, _, v = part.partition("=")
            k = k.strip().lower()
            if k not in ABILITIES or not v.strip().lstrip("-").isdigit():
                raise StateError(f"--abilities must look like str=15,dex=14 (keys: {','.join(ABILITIES)})")
            abilities[k] = int(v)

    def fn(state):
        if any(c["name"].lower() == a.name.lower() for c in state["crawlers"]):
            raise StateError(f"crawler '{a.name}' already exists")
        c = new_crawler(a.name, a.player, a.class_, a.species, a.level, a.hp_max, a.ac, a.credits, abilities)
        assign_status(state, c)
        state["crawlers"].append(c)
        return state, c
    c = mutate(fn)
    return c, f"added crawler {c['name']} ({c['species']} {c['class']}, player {c['player']}), HP {c['hp']['max']}, AC {c['ac']}, {c.get('status', 'no status')}"


CREATE_REQUIRED = ("name", "player", "class", "species", "abilities", "hp_max", "ac")


def _spec_inventory(spec):
    inv = []
    for it in spec.get("inventory", []):
        if not (isinstance(it, dict) and isinstance(it.get("name"), str) and _is_int(it.get("qty", 1)) and it.get("qty", 1) >= 1):
            raise StateError(f"bad inventory item: {json.dumps(it)[:80]}")
        row = {"name": it["name"], "qty": it.get("qty", 1), "notes": it.get("notes", "")}
        for k in ("mechanics", "category", "srd_id", "chargen_key"):
            if it.get(k):
                row[k] = it[k]
        inv.append(row)
    return inv


def crawler_from_spec(spec, inv=None, with_credits=False):
    """Build a crawler record from a create-crawler spec (credits start at 0 unless with_credits; the ledger applies them)."""
    ab = spec["abilities"]
    c = new_crawler(spec["name"], spec["player"], spec["class"], spec["species"], spec.get("level", 1), spec["hp_max"], spec["ac"],
                    spec.get("credits", 0) if with_credits else 0, {k: ab[k] for k in ABILITIES})
    c["inventory"] = inv if inv is not None else _spec_inventory(spec)
    c["notes"] = spec.get("notes", "")
    if spec.get("kind") and spec["kind"] != "player":
        c["kind"] = spec["kind"]
        if spec.get("owner"):
            c["owner"] = str(spec["owner"])
    for k in ("standing_orders", "standing_reaction", "signature", "background", "intake_tag"):
        if spec.get(k):
            c[k] = spec[k]
    fp = spec.get("fan_profile")
    if isinstance(fp, dict):
        c["fan_profile"] = {"quirks": list(fp.get("quirks", [])), "notes": str(fp.get("notes", "")), "opt_outs": list(fp.get("opt_outs", []))}
    if isinstance(spec.get("build"), dict):
        c["build"] = spec["build"]
    return c


def cmd_create_crawler(a):
    """Atomically add a fully-built crawler from a JSON spec (used by the Discord /create flow and by the GM).
    Credits are applied as separate ledger entries (credit_breakdown: gains first, then spends), each with its own reason."""
    refuse_secret_path(a.file)
    try:
        with open(a.file, encoding="utf-8") as f:
            spec = json.load(f)
    except (OSError, ValueError) as e:
        raise StateError(f"cannot read {a.file}: {e}")
    if not isinstance(spec, dict):
        raise StateError("spec must be a JSON object")
    missing = [k for k in CREATE_REQUIRED if spec.get(k) in (None, "")]
    if missing:
        raise StateError("spec is missing: " + ", ".join(missing))
    ab = spec["abilities"]
    if not isinstance(ab, dict) or not all(_is_int(ab.get(k)) for k in ABILITIES):
        raise StateError("spec.abilities must have integer " + "/".join(ABILITIES))
    credits = spec.get("credits", 0)
    breakdown = spec.get("credit_breakdown") or ([{"delta": credits, "reason": "Starting credits"}] if credits else [])
    if not _is_int(credits) or sum(b["delta"] for b in breakdown) != credits:
        raise StateError("spec.credit_breakdown must sum to spec.credits")
    breakdown = sorted(breakdown, key=lambda b: b["delta"] < 0)  # gains before spends: never dips below zero
    inv = _spec_inventory(spec)

    def fn(state):
        if any(c["name"].lower() == spec["name"].lower() for c in state["crawlers"]):
            raise StateError(f"crawler '{spec['name']}' already exists")
        cap = state.get("limits", {}).get("max_crawlers", DEFAULT_LIMITS["max_crawlers"])
        kind = spec.get("kind", "player")
        if kind not in CRAWLER_KINDS:
            raise StateError(f"kind must be one of {', '.join(CRAWLER_KINDS)}")
        probe = crawler_from_spec(spec, inv)
        want = "benched" if (spec.get("status") == "benched" or (kind == "player" and session_open()[0])) else None   # /create during an open session never makes an active Crawler
        status = assign_status(state, probe, want) if kind == "player" else None
        if kind == "player" and status == "active" and _is_int(cap) and player_crawler_count(state) >= cap:
            raise StateError(f"party full: {player_crawler_count(state)} of {cap} active player crawlers (limits.max_crawlers; benched Crawlers, pets, companions and pet-crawlers take no slot)")
        biscuit_note = ""
        if kind == "pet-crawler":
            owner = next((c for c in state["crawlers"] if c["name"].lower() == str(spec.get("owner", "")).lower()), None)
            if not owner or crawler_kind(owner) != "player":
                raise StateError("a pet-crawler needs spec.owner = the player Crawler who made it (an existing kind=player crawler)")
            if str(spec["player"]).strip().lower() != str(owner.get("player", "")).strip().lower():
                raise StateError(f"a pet-crawler is played by the player who made it: spec.player must be {owner.get('player')} (owner {owner['name']}'s player)")
            pet = str(spec.get("pet") or "").strip()
            if not pet:
                raise StateError("a pet-crawler needs spec.pet = the name of the pet that is being made a Crawler (one conversion per living pet-Crawler)")
            if any(crawler_kind(c) == "pet-crawler" and str(c.get("owner", "")).lower() == owner["name"].lower() and str(c.get("pet_name", "")).lower() == pet.lower() for c in state["crawlers"]):
                raise StateError(f"REFUSED: {pet} is already a living pet-Crawler (one conversion per living, non-deleted pet-Crawler; delete it first, and a new conversion needs a new Enhanced Pet Biscuit)")
            biscuit = next((i for i in owner["inventory"] if i["name"].lower() == "enhanced pet biscuit"), None)
            if biscuit:
                biscuit["qty"] -= 1
                if biscuit["qty"] <= 0:
                    owner["inventory"].remove(biscuit)
                biscuit_note = " (Enhanced Pet Biscuit consumed)"
            elif not str(spec.get("biscuit_waiver") or "").strip():
                raise StateError(f"REFUSED: {owner['name']} holds no Enhanced Pet Biscuit to feed {pet}. If the GM ruled the conversion another way, add spec.biscuit_waiver = \"why\"")
            else:
                biscuit_note = f" (no biscuit; waiver: {spec['biscuit_waiver']})"
        tag = spec.get("intake_tag")
        if tag and any(str(c.get("intake_tag", "")).lower() == str(tag).lower() for c in state["crawlers"]):
            raise StateError(f"intake tag '{tag}' is already taken in this session")
        c = crawler_from_spec(spec, inv)
        assign_status(state, c, want)
        if kind == "pet-crawler":
            c["pet_name"] = pet
            c["owner"] = owner["name"]
            c["owner_player"] = owner.get("player", "")
            op = living_pet(owner)
            if op and str(op.get("name", "")).strip().lower() == str(pet).strip().lower():   # the plain pet became a Crawler: retire the plain record (decision 022)
                op.update(status="became-crawler", converted_to=c["name"])
        state["crawlers"].append(c)
        _RUN["biscuit_note"] = biscuit_note
        return state, c
    _RUN["reason"] = "Crawler created (no starting credits)"
    c = mutate(fn)
    for b in breakdown:
        _RUN.update(reason=b["reason"], source=b.get("source", "intake"))

        def bump(state, d=b["delta"]):
            cc = find_crawler(state, spec["name"])
            cc["credits"] += d
            return state, cc["credits"]
        mutate(bump)
    st = c.get("status")
    return {"ok": True, "name": spec["name"], "status": st}, (f"created crawler {spec['name']} ({spec['species']} {spec['class']}, player {spec['player']}), HP {spec['hp_max']}, AC {spec['ac']}, credits {credits}"
        + (f", status {st}" if st else "")
        + (f" [pet-crawler of {spec['owner']}; takes no extra slot{_RUN.pop('biscuit_note', '')}; own sheet channel: run discord_gm.py setup-channels]" if spec.get("kind") == "pet-crawler" else ""))


def cmd_show(a):
    state = read_state_file()
    if a.crawler:
        c = find_crawler(state, a.crawler)
        hp = c["hp"]
        lines = [
            f"{c['name']} - {c['species']} {c['class']} {c['level']} (player {c['player']}), XP {c['xp']}",
            f"HP {hp['current']}/{hp['max']} temp {hp['temp']} | AC {c['ac']} | Hit dice {c['hit_dice']['current']}/{c['hit_dice']['max']} | Credits {c['credits']}",
            "Abilities: " + " ".join(f"{k.upper()} {v}" for k, v in c["abilities"].items()),
            "Conditions: " + (", ".join(c["conditions"]) or "none"),
            "Inventory: " + (", ".join(f"{i['name']} x{i['qty']}" for i in c["inventory"]) or "empty"),
            "Boxes: " + (", ".join(f"{t} {n}" for t, n in c["boxes"].items() if n) or "none"),
            "Achievements: " + (", ".join(x["name"] for x in c["achievements"]) or "none"),
            f"Vows: {len(c['vows'])} | Boons: {len(c['boons'])} | Revives used {c['revives_used']} | Bypasses used {c['bypasses_used']}",
        ]
        if c["fan_profile"]["quirks"] or c["fan_profile"]["opt_outs"]:
            lines.append(f"Fan profile: quirks {c['fan_profile']['quirks']}, opt-outs {[o.get('topic') if isinstance(o, dict) else o for o in c['fan_profile']['opt_outs']]}")
        return c, "\n".join(lines)
    camp, party, lim = state["campaign"], state["party"], state["limits"]
    lines = [
        f"{camp['name']} | Floor {camp['current_floor']}" + (f" ({camp['zone']})" if camp["zone"] else "")
        + f" | Death: {camp['death_mode']} | Comfort: {camp['comfort']}",
        f"Party revives {party['revives_used']}/{lim['revive_campaign_cap']} (last on floor {party['last_revive_floor']}) | bypasses used {party['bypasses_used']}",
    ]
    for c in state["crawlers"]:
        lines.append(f"- {_hp_line(c)} | AC {c['ac']} | L{c['level']} {c['species']} {c['class']} ({c['player']}) | {c['credits']} cr"
                     + (f" | {', '.join(c['conditions'])}" if c["conditions"] else ""))
    if not state["crawlers"]:
        lines.append("(no crawlers yet)")
    return state, "\n".join(lines)


def counts_in_encounters(c):
    """Encounter budgets count every ACTIVE Crawler: kind player and kind pet-crawler (a pet made a Crawler). Benched Crawlers, plain pets and companions do not count."""
    return crawler_kind(c) in ("player", "pet-crawler") and is_active(c)


def cmd_party(a):
    """party [--json]: the roster for GM tools. `encounter_count` is what encounter budgets use (players + pet-crawlers); `party_slots` is what limits.max_crawlers caps (players only)."""
    state = read_state_file()
    cap = state.get("limits", {}).get("max_crawlers", DEFAULT_LIMITS["max_crawlers"])
    members = [{"name": c["name"], "kind": crawler_kind(c), "player": c.get("player"), "owner": c.get("owner"), "owner_player": c.get("owner_player"),
                "status": crawler_status(c) or None, "level": c.get("level"), "hp": f"{c['hp']['current']}/{c['hp']['max']}", "alive": not any(x.lower() in ("dead", "deceased") for x in c.get("conditions", [])),
                "benched": crawler_status(c) == "benched", "counts_in_encounters": counts_in_encounters(c)} for c in state["crawlers"]]
    data = {"ok": True, "encounter_count": sum(1 for m in members if m["counts_in_encounters"]), "encounter_count_living": sum(1 for m in members if m["counts_in_encounters"] and m["alive"]),
            "party_slots": f"{player_crawler_count(state)}/{cap}", "members": members,
            "benched_count": sum(1 for m in members if m["benched"])}   # consumers that want only the table in play: filter members on `benched` false (or status != "benched"); existing keys are unchanged
    # GM-run plain pets (decision 022): companions of ACTIVE Crawlers; no party slot, not counted in encounter_count, no credits/XP/loot
    data["companions"] = [{"name": c["pet"]["name"], "species": c["pet"]["species"], "cr": c["pet"]["cr"], "owner": c["name"], "gm_run": True, "party_slot": False, "counts_in_encounters": False}
                          for c in state["crawlers"] if pets_enabled(state) and living_pet(c) and crawler_kind(c) == "player" and is_active(c)]
    lines = [f"Encounter budget counts {data['encounter_count']} Crawler(s) ({data['encounter_count_living']} living); party slots {data['party_slots']} (benched Crawlers take no slot and are not counted; pet-crawlers take no slot but DO count in encounters while active)"]
    for m in members:
        lines.append(f"- {m['name']} [{m['kind']}]" + (f" owner {m['owner']}" if m["owner"] else "") + f" L{m['level']} HP {m['hp']} (player {m['player']})" + ("" if m["alive"] else " DEAD") + ("" if m["counts_in_encounters"] else " [not counted]" + (" (benched)" if m["status"] == "benched" else "")))
    for p_ in data["companions"]:
        lines.append(f"- pet {p_['name']} ({p_['species']}, CR {_cr_text(p_['cr'])}) of {p_['owner']}: GM-run companion, no slot, not counted in encounters, no credits/XP/loot")
    return data, "\n".join(lines)


def cmd_get(a):
    value = get_path(read_state_file(), a.path)
    return value, (value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False))


def cmd_set(a):
    value = parse_value(a.value)

    # S6: a benched Crawler's credits, XP, boxes, inventory, achievements and HP cannot be changed through a raw path either (by name OR by index: crawlers.1.credits)
    mm = re.match(r"^crawlers\.([^.]+)\.(xp|credits|boxes|inventory|achievements|hp|hit_dice|conditions|death_saves)(\.|$)", a.path)
    if mm:
        st0 = read_state_file()
        seg = mm.group(1)
        try:
            who = st0["crawlers"][int(seg)] if seg.lstrip("-").isdigit() else find_crawler(st0, seg)
        except (IndexError, StateError):
            who = None
        if who:
            require_active(who, f"change its {mm.group(2)}", a)

    def fn(state):
        set_path(state, a.path, value)
        return state, None
    mutate(fn)
    return {"path": a.path, "value": value}, f"set {a.path} = {json.dumps(value, ensure_ascii=False)}"


def cmd_inventory(a):
    def fn(state):
        c = find_crawler(state, a.crawler)
        if a.action == "add":
            require_active(c, "gain items (benched Crawlers cannot be mules)", a)
        inv = c["inventory"]
        existing = next((i for i in inv if i["name"].lower() == a.item.lower()), None)
        if a.action == "add":
            if a.qty < 1:
                raise StateError("--qty must be >= 1")
            if existing:
                existing["qty"] += a.qty
            else:
                it = {"name": a.item, "qty": a.qty, "notes": a.notes or ""}
                if getattr(a, "mechanics", None):
                    it["mechanics"] = a.mechanics
                if getattr(a, "category", None):
                    it["category"] = a.category
                inv.append(it)
            return state, f"{c['name']} +{a.qty} {a.item}"
        if not existing:
            raise StateError(f"{c['name']} has no '{a.item}'")
        qty = existing["qty"] if a.all else a.qty
        if qty < 1 or qty > existing["qty"]:
            raise StateError(f"{c['name']} has only {existing['qty']} x {existing['name']}")
        existing["qty"] -= qty
        if existing["qty"] == 0:
            inv.remove(existing)
        return state, f"{c['name']} -{qty} {existing['name']}"
    text = mutate(fn)
    return {"ok": True, "message": text}, text


def cmd_hp(a):
    def fn(state):
        c = find_crawler(state, a.crawler)
        require_active(c, "take damage or healing (a benched Crawler is not in play)", a)
        hp = c["hp"]
        extra = ""
        if a.action == "damage":
            amount = _positive(a.amount)
            absorbed = min(hp["temp"], amount)
            hp["temp"] -= absorbed
            rest = amount - absorbed
            overkill = max(0, rest - hp["current"])
            hp["current"] = max(0, hp["current"] - rest)
            extra = f" ({amount} damage" + (f", {absorbed} absorbed by temp HP" if absorbed else "") + ")"
            if hp["current"] == 0:
                extra += " - AT 0 HP"
                if overkill >= hp["max"]:
                    extra += f" - MASSIVE DAMAGE (overkill {overkill} >= max HP {hp['max']}): instant death under 5e rules"
        elif a.action == "heal":
            amount = _positive(a.amount)
            before = hp["current"]
            hp["current"] = min(hp["max"], hp["current"] + amount)
            extra = f" (healed {hp['current'] - before} of {amount})"
        elif a.action == "set":
            if a.max is not None:
                if a.max < 1:
                    raise StateError("--max must be >= 1")
                hp["max"] = a.max
            clamped = min(hp["max"], max(0, a.amount))
            extra = f" (clamped from {a.amount})" if clamped != a.amount else ""
            hp["current"] = clamped
        elif a.action == "temp":
            amount = _positive(a.amount)
            # 5e: temp HP don't stack - keep the higher unless --replace
            hp["temp"] = amount if a.replace else max(hp["temp"], amount)
        return state, _hp_line(c) + extra
    text = mutate(fn)
    return {"ok": True, "message": text}, text


def cmd_credits(a):
    m = re.fullmatch(r"([-+=]?)([0-9]+)", a.amount.strip())
    if not m:
        raise StateError("amount must look like +500, -200 or =1000")
    if getattr(a, "floor", None) is not None:
        _RUN["row_extra"] = {find_crawler(read_state_file(), a.crawler)["name"]: {"floor": _floor_arg(a.floor, None)}}

    def fn(state):
        c = find_crawler(state, a.crawler)
        require_active(c, "earn or spend credits", a)
        n = int(m.group(2))
        new = n if m.group(1) == "=" else c["credits"] + (-n if m.group(1) == "-" else n)
        if new < 0 and not a.allow_debt:
            raise StateError(f"{c['name']} has {c['credits']} credits; cannot spend {n} (use --allow-debt to go negative)")
        c["credits"] = new
        return state, f"{c['name']}: {new} credits"
    text = mutate(fn)
    return {"ok": True, "message": text}, text


def cmd_achievement(a):
    def fn(state):
        c = find_crawler(state, a.crawler)
        require_active(c, "earn achievements (the intake toast for a new benched Crawler passes --benched-ok \"intake\")", a)
        if any(x["name"].lower() == a.title.lower() for x in c["achievements"]):
            raise StateError(f"{c['name']} already has achievement '{a.title}'")
        row = {"name": a.title, "floor": state["campaign"]["current_floor"], "note": a.note or "", "at": now_iso()}
        if getattr(a, "reward", None):
            row["reward"] = a.reward
        c["achievements"].append(row)
        return state, f"{c['name']} earned achievement: {a.title}"
    text = mutate(fn)
    return {"ok": True, "message": text}, text


def cmd_condition(a):
    def fn(state):
        c = find_crawler(state, a.crawler)
        existing = next((x for x in c["conditions"] if x.lower() == a.condition.lower()), None)
        if a.action == "add":
            if existing:
                raise StateError(f"{c['name']} already has condition '{existing}'")
            c["conditions"].append(a.condition)
            return state, f"{c['name']} now: {', '.join(c['conditions'])}"
        if not existing:
            raise StateError(f"{c['name']} does not have condition '{a.condition}'")
        c["conditions"].remove(existing)
        return state, f"{c['name']} now: {', '.join(c['conditions']) or 'no conditions'}"
    text = mutate(fn)
    if a.action == "add" and a.condition.lower() in ("dead", "deceased"):
        text += _reclaim_unopened_boxes(a.crawler, a.condition)
    return {"ok": True, "message": text}, text


def _reclaim_unopened_boxes(crawler, why):
    """Caleb 2026-10-04: a Crawler that DIES holding an UNOPENED Story Box loses it. The box is reclaimed and its floor slot is freed (loot.legendary_count
    ignores `reclaimed` boxes). Logged in the story-box ledger (`reclaimed`) and the box ledger. The deed stays closed. An opened box is not touched."""
    state = read_state_file()
    c = find_crawler(state, crawler)
    sb = ledgers.read("story-box")
    closed = {e.get("box_id") for e in sb if e.get("event") in ("opened", "reclaimed", "released")}
    held = [e for e in sb if e.get("event") == "awarded" and e.get("crawler") == c["name"] and e.get("box_id") not in closed]
    if not held:
        return ""
    for e in held:
        ledgers.append("story-box", {"event": "reclaimed", "box_id": e["box_id"], "crawler": c["name"], "floor": e.get("floor"), "box_name": e.get("box_name"),
                                     "reason": f"{c['name']} died ({why}) holding this Story Box unopened; reclaimed, the floor slot is freed (the deed stays closed)"})
        ledgers.append("box", {"event": "reclaimed", "crawler": c["name"], "tier": "legendary", "count": 1, "floor": e.get("floor"), "box_name": e.get("box_name"), "box_id": e["box_id"],
                               "reason": "Crawler died holding an unopened Story Box"})

    def fn(st):
        cc = find_crawler(st, c["name"])
        cc["boxes"]["legendary"] = max(0, cc["boxes"].get("legendary", 0) - len(held))
        return st, cc
    mutate(fn)
    return f"\nSTORY BOX RECLAIMED: {c['name']} died holding {len(held)} unopened Story Box(es) ({', '.join(e['box_id'] for e in held)}); the floor slot is free again."


# --------------------------------------------------------------------------- plain pets (decision 022, rules/60, spec section 9)
# A plain pet is GM-run data ON its owner's Crawler record (c["pet"]); it is not a Crawler, takes no slot, credits, XP or loot, and cannot be traded or sold.
# It is separate from kind="pet-crawler" (an Enhanced Pet Biscuit conversion, `pet convert`). Players are never asked about pets and nothing reacts to the word "pet"
# in free text: the GM reads the questionnaire at the review gate and files the pet by hand.

PET_MAX_CR = 0.25
PET_STATUSES = ("alive", "dead", "became-crawler")
# Off-menu items, sold only by `pet shop` to a Crawler with a living pet on file: id -> (inventory name, price in credits at Floor 1 scale). Never on any vending wall, list or loot deck.
PET_SHOP = {"heal-critter-potion": ("Good Boy Gulp, Shaken Until Brown (Heal Critter Potion)", 50), "pet-carrier": ("Fold-Flat Kennel With an Impossible Interior (Pet Carrier)", 100)}


def _pet_species():
    for base in (csession.campaign_dir(), os.path.dirname(os.path.dirname(os.path.abspath(__file__)))):   # the campaign's own table, else the one beside these tools
        try:
            with open(os.path.join(base, "tables", "pet-species.json"), encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            continue
    return {"species": [], "aliases": {}}


def _species_lookup(text):
    """-> (srd_id, display, cr) or None. Matches the SRD Beast list (CR 1/4 or lower) by name or alias (dog -> mastiff ...)."""
    d, t = _pet_species(), _slug(text)
    al = {_slug(k): v for k, v in (d.get("aliases") or {}).items()}
    t = al.get(t, t)
    for e in d.get("species", []):
        if e["id"] == t or _slug(e["name"]) == t:
            return e["id"], e["name"], e["cr"]
    return None


def _cr_value(text):
    t = str(text).strip()
    try:
        return float(Fraction(t)) if "/" in t else float(t)
    except (ValueError, ZeroDivisionError):
        raise StateError(f"--cr must be a number like 0, 0.125, 1/8 or 1/4 (got '{text}')")


def _cr_text(v):
    return {0.0: "0", 0.125: "1/8", 0.25: "1/4"}.get(float(v), f"{v:g}")


def pets_enabled(state):
    """The one feature switch (limits.pets_enabled, default true; rules/60 section 2 item 5, spec 9.5)."""
    return bool((state.get("limits") or {}).get("pets_enabled", DEFAULT_LIMITS["pets_enabled"]))


def living_pet(c):
    pet = c.get("pet") if isinstance(c, dict) else None
    return pet if isinstance(pet, dict) and pet.get("status") == "alive" else None


def _pet_errors(c):
    pet, errs = c.get("pet"), []
    if crawler_kind(c) != "player":
        errs.append("only a player Crawler can have a plain pet")
    if not isinstance(pet, dict):
        return errs + ["pet must be an object"]
    for k in ("name", "species"):
        if not (isinstance(pet.get(k), str) and pet[k].strip()):
            errs.append(f"pet.{k} must be a non-empty string")
    cr = pet.get("cr")
    if isinstance(cr, bool) or not isinstance(cr, (int, float)) or not 0 <= cr <= PET_MAX_CR:
        if not pet.get("override"):
            errs.append(f"pet.cr must be a number from 0 to {PET_MAX_CR} (SRD Beast CR 1/4 or lower; a GM --override is recorded in pet.override)")
    if pet.get("status") not in PET_STATUSES:
        errs.append(f"pet.status must be one of {', '.join(PET_STATUSES)}")
    if isinstance(pet.get("description"), str) and len(pet["description"]) > 300:
        errs.append("pet.description is at most 300 characters")
    return errs


def pet_crawler_gone(state, c):
    """True when the owner's plain-pet record says `became-crawler` but that pet-Crawler is no longer on file (it was deleted): the record no longer blocks a new pet."""
    pet = c.get("pet") if isinstance(c, dict) else None
    if not (isinstance(pet, dict) and pet.get("status") == "became-crawler"):
        return False
    target, pname, owner = str(pet.get("converted_to") or "").lower(), str(pet.get("name") or "").lower(), str(c.get("name") or "").lower()
    return not any(crawler_kind(x) == "pet-crawler" and (x["name"].lower() == target or (str(x.get("pet_name", "")).lower() == pname and str(x.get("owner", "")).lower() == owner))
                   for x in state["crawlers"])


def _pet_line(c):
    pet = c["pet"]
    return f"{c['name']}: {pet['name']} the {pet['species']} (CR {_cr_text(pet['cr'])}) [{pet['status']}]" + (f" - {pet['description']}" if pet.get("description") else "")


def _owner_for_pet(state, name):
    c = find_crawler(state, name)
    if crawler_kind(c) != "player":
        raise StateError(f"{c['name']} is a {crawler_kind(c)}; a plain pet belongs to a player Crawler (benched is fine)")
    return c


def _off(state):
    if not pets_enabled(state):
        raise StateError("REFUSED: pets are off (limits.pets_enabled is false)")


def cmd_pet(a):
    """pet add OWNER --name N --species S [--description T] [--quote T] [--cr 1/4] [--override WHY] | pet show [OWNER] | pet mark-dead OWNER --reason T (alias kill)
    | pet remove OWNER --reason T | pet convert OWNER --file SPEC | pet shop OWNER [ITEM] [--qty N] [--sell] --reason T [--floor N] [--override WHY] | pet heal OWNER --reason T.
    GM-only. Never reachable from /create or a player command."""
    if a.action == "show":
        state = read_state_file()
        rows = [find_crawler(state, a.owner)] if a.owner else state["crawlers"]
        rows = [c for c in rows if isinstance(c.get("pet"), dict)]
        enabled = pets_enabled(state)
        data = {"ok": True, "pets_enabled": enabled, "pets": [{"owner": c["name"], **c["pet"]} for c in rows]}
        head = "" if enabled else "(limits.pets_enabled is false: pets are hidden from cards and party; add, convert and shop are refused)\n"
        return data, head + ("\n".join(_pet_line(c) for c in rows) if rows else "(no pets on file)")
    if not a.owner:
        raise StateError(f"usage: pet {a.action} OWNER ...")
    fn = {"add": _pet_add, "kill": _pet_mark_dead, "mark-dead": _pet_mark_dead, "remove": _pet_remove, "convert": _pet_convert, "shop": _pet_shop, "heal": _pet_heal}.get(a.action)
    if not fn:
        raise StateError("pet add|show|mark-dead|remove|convert|shop|heal")
    return fn(a)


def _pet_add(a):
    if not (a.species or "").strip() or not (a.name or "").strip():
        raise StateError("usage: pet add OWNER --name N --species S [--description T] [--quote \"the player's own words\"] [--cr 1/4] [--override WHY]")
    name = a.name.strip()
    desc = (a.description or a.notes or "").strip()
    if len(desc) > 300:
        raise StateError("--description is at most 300 characters")
    sp = _species_lookup(a.species)
    ov = (a.override or "").strip()
    if sp:
        sid, sname, scr = sp
        cr = _cr_value(a.cr) if a.cr is not None else scr
    else:
        if not ov:
            raise StateError(f"REFUSED: '{a.species}' is not on the SRD Beast list of CR 1/4 or lower (tables/pet-species.json). Edge cases are the GM's call: add --override \"why\" (logged)")
        sid, sname, cr = _slug(a.species), a.species.strip(), (_cr_value(a.cr) if a.cr is not None else PET_MAX_CR)
    if cr < 0 or (cr > PET_MAX_CR and not ov):
        raise StateError(f"REFUSED: a plain pet must be an SRD Beast of CR 1/4 or lower (got CR {_cr_text(cr)}); a GM ruling needs --override \"why\" (logged)")
    box = {}

    def fn(state):
        _off(state)
        c = _owner_for_pet(state, a.owner)
        old = c.get("pet") if isinstance(c.get("pet"), dict) else None
        gone = pet_crawler_gone(state, c)   # its pet-Crawler was deleted: the old record stays in the history and no longer blocks
        if old and old.get("status") in ("alive", "became-crawler") and not gone:
            raise StateError(f"REFUSED: {c['name']} already has a pet ({old['name']}, {'living' if old['status'] == 'alive' else 'now a pet-Crawler by Enhanced Pet Biscuit'}); one pet per Crawler")
        taken = {x["name"].lower() for x in state["crawlers"]} | {x["pet"]["name"].lower() for x in state["crawlers"] if isinstance(x.get("pet"), dict) and x["pet"].get("status") != "dead" and not pet_crawler_gone(state, x)}
        if name.lower() in taken:
            raise StateError(f"REFUSED: the name '{name}' is already used by a Crawler or pet; pick another")
        if old:  # a dead pet (or one whose pet-Crawler was deleted) stays on file in the history
            c.setdefault("pet_history", []).append(dict(old, pet_crawler_deleted=True) if gone else old)
        pet = {"name": name, "species": sname, "species_srd_id": sid, "cr": cr, "description": desc, "quote": (a.quote or "").strip()[:300], "filed_by": a.by or "gm", "filed_on": now_iso(),
               "status": "alive", "floor": state["campaign"]["current_floor"]}
        if ov:
            pet["override"] = ov
        c["pet"] = pet
        box["owner"] = c["name"]
        return state, c
    _RUN.update(reason=f"pet added: {name}", source="pet")
    mutate(fn)
    ledgers.append("pet", {"event": "added", "owner": box["owner"], "pet": name, "species": sname, "cr": cr, "description": desc, "quote": (a.quote or "").strip()[:300], "override": ov, "by": a.by or "gm"})
    return {"ok": True, "owner": box["owner"], "pet": name}, (f"{box['owner']} now has a pet: {name} the {sname} (CR {_cr_text(cr)}). GM-run; no party slot, credits, XP or loot; cannot be traded; "
                                                          f"ordinary healing does nothing for it (Good Boy Gulp does); death is final")


def _pet_mark_dead(a):
    if not (a.reason or "").strip():
        raise StateError("pet mark-dead needs --reason (what killed it); death is final, there is no revive")
    box = {}

    def fn(state):
        c = _owner_for_pet(state, a.owner)
        pet = living_pet(c)
        if not pet:
            raise StateError(f"{c['name']} has no living pet")
        pet.update(status="dead", died=now_iso(), death_reason=a.reason.strip())
        box.update(owner=c["name"], pet=pet["name"])
        return state, c
    _RUN.update(reason=f"pet died: {a.owner}", source="pet")
    mutate(fn)
    ledgers.append("pet", {"event": "died", "owner": box["owner"], "pet": box["pet"], "reason": a.reason.strip()})
    return {"ok": True, "owner": box["owner"], "pet": box["pet"]}, f"{box['pet']} ({box['owner']}'s pet) is dead. Final: pets are never revived. The card no longer shows it."


def _pet_remove(a):
    """GM error correction: drop the pet record entirely (logged). Not a death."""
    if not (a.reason or "").strip():
        raise StateError("pet remove needs --reason (GM error correction; logged)")
    box = {}

    def fn(state):
        c = _owner_for_pet(state, a.owner)
        if not isinstance(c.get("pet"), dict):
            raise StateError(f"{c['name']} has no pet on file")
        box.update(owner=c["name"], pet=dict(c["pet"]))
        del c["pet"]
        return state, c
    _RUN.update(reason=f"pet removed: {a.owner}", source="pet")
    mutate(fn)
    ledgers.append("pet", {"event": "removed", "owner": box["owner"], "pet": box["pet"]["name"], "record": box["pet"], "reason": a.reason.strip()})
    return {"ok": True}, f"{box['pet']['name']} removed from {box['owner']} (correction, logged)"


def _pet_convert(a):
    """pet convert OWNER --file SPEC.json: the Enhanced Pet Biscuit. Builds the pet-Crawler through create-crawler (its biscuit, one-per-living and slot rules), then the pet record becomes `became-crawler`."""
    if not getattr(a, "file", None):
        raise StateError("pet convert needs --file SPEC.json")
    state = read_state_file()
    _off(state)
    c = _owner_for_pet(state, a.owner)
    pet = living_pet(c)
    if not pet:
        hint = " Its pet-Crawler was deleted, so file a new pet first (`pet add`), then convert it with a new Enhanced Pet Biscuit." if pet_crawler_gone(state, c) else ""
        raise StateError(f"REFUSED: {c['name']} has no living plain pet to convert (the biscuit works only on the pet on file).{hint}")
    refuse_secret_path(a.file)
    try:
        with open(a.file, encoding="utf-8") as f:
            spec = json.load(f)
    except (OSError, ValueError) as e:
        raise StateError(f"cannot read {a.file}: {e}")
    spec.update(kind="pet-crawler", owner=c["name"], pet=pet["name"], player=c.get("player"))
    spec.setdefault("name", pet["name"])
    fd, tmp = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(spec, f)
        r = cmd_create_crawler(argparse.Namespace(file=tmp))
    finally:
        os.unlink(tmp)
    ledgers.append("pet", {"event": "converted", "owner": c["name"], "pet": pet["name"], "pet_crawler": spec["name"]})
    return r


def is_pet_item(it):
    """True for the two off-menu pet shop items (heal-critter-potion, pet-carrier)."""
    return isinstance(it, dict) and (it.get("srd_id") in PET_SHOP or any(_slug(it.get("name", "")) == _slug(nm) for nm, _p in PET_SHOP.values()))


def _pet_item_gate(it, who, verb):
    """Pet items move only to / from a Crawler with a living pet (the shop's own rule, also for trades and sales)."""
    if is_pet_item(it) and not living_pet(who):
        raise StateError(f"REFUSED: {it['name']} is a pet item; it can only be {verb} by a Crawler with a living pet ({who['name']} has none)")


def _shop_item(text):
    t = _slug(text)
    for iid, (nm, _price) in PET_SHOP.items():
        if t in (iid, _slug(nm), _slug(nm.split(" (")[0]), _slug(nm.split("(")[-1].rstrip(")"))):
            return iid
    raise StateError(f"pet shop sells only: {', '.join(PET_SHOP)}")


def _pet_shop(a):
    """pet shop OWNER [ITEM] --reason T [--qty N] [--floor N] [--sell] [--override WHY] [--dry-run]. Without ITEM: the price list for this owner. heal-critter-potion 50 / pet-carrier 100
    credits at Floor 1 scale x the floor multiplier; --sell is the half-price buyback. Buying needs a LIVING pet on file (or the GM's logged --override). A normal credit-ledger transaction."""
    state = read_state_file()
    c = _owner_for_pet(state, a.owner)
    floor = a.floor if a.floor is not None else state["campaign"]["current_floor"]
    mult = loot.floor_multiplier(floor)
    if not a.item:
        _off(state)
        if not living_pet(c) and not (a.override or "").strip():
            raise StateError(f"REFUSED: {c['name']} has no living pet on file; these items are not offered")
        rows = [{"id": i, "name": nm, "credits": p * mult, "buyback": p * mult // 2} for i, (nm, p) in PET_SHOP.items()]
        return {"ok": True, "floor": floor, "multiplier": mult, "items": rows}, "\n".join(f"{r['id']}: {r['name']} - {r['credits']} credits (buyback {r['buyback']}), floor {floor} x{mult}" for r in rows)
    if not (a.reason or "").strip():
        raise StateError("pet shop needs --reason (it goes in the credit ledger)")
    iid = _shop_item(a.item)
    iname, base = PET_SHOP[iid]
    qty = a.qty if a.qty is not None else 1
    if qty < 1:
        raise StateError("--qty must be >= 1")
    if not a.sell:
        _off(state)   # "pets are off" comes before any benched-owner refusal
    require_active(c, "buy or sell pet items", a)
    unit = base * mult // (2 if a.sell else 1)
    total = unit * qty
    ov = (a.override or "").strip()
    if not a.sell:
        _off(state)
        if not living_pet(c) and not ov:
            raise StateError(f"REFUSED: {c['name']} has no living pet on file; {iname} is sold only to a Crawler with a pet (the GM may add --override \"why\", logged)")
        if c["credits"] < total:
            raise StateError(f"{c['name']} has {c['credits']} credits; {qty}x {iname} costs {total}")
    else:
        have = next((i for i in c["inventory"] if i.get("srd_id") == iid), None)
        if not have or have["qty"] < qty:
            raise StateError(f"{c['name']} does not have {qty}x {iname} to sell back")
    basis = f"{'buyback' if a.sell else 'price'} {unit} each ({base} x{mult} floor {floor}{', half' if a.sell else ''})"
    if a.dry_run:
        return {"ok": True, "dry_run": True, "credits": total}, f"DRY RUN: {c['name']} would {'sell back' if a.sell else 'buy'} {qty}x {iname} for {total} credits ({basis})"
    _RUN.update(reason=f"{'Sold back' if a.sell else 'Bought'} {qty}x {iname} ({basis}): {a.reason.strip()}", source="pet-shop")

    def fn(st):
        cc = find_crawler(st, c["name"])
        row = next((i for i in cc["inventory"] if i.get("srd_id") == iid), None)
        if a.sell:
            row["qty"] -= qty
            if row["qty"] <= 0:
                cc["inventory"].remove(row)
            cc["credits"] += total
        else:
            cc["credits"] -= total
            if row:
                row["qty"] += qty
            else:
                cc["inventory"].append({"name": iname, "qty": qty, "srd_id": iid, "off_menu": True})
        return st, cc
    cc = mutate(fn)
    ledgers.append("pet", {"event": "shop-sell" if a.sell else "shop-buy", "owner": c["name"], "item": iid, "qty": qty, "credits": total, "floor": floor, "override": ov, "reason": a.reason.strip()})
    return {"ok": True, "credits": total}, f"{c['name']} {'sold back' if a.sell else 'bought'} {qty}x {iname} for {total} credits ({basis}); credits now {cc['credits']}"


def _pet_heal(a):
    """pet heal OWNER --reason T: the pet drinks one Good Boy Gulp: 2d4+2 HP to the pet (the GM applies it). Ordinary healing never works on a pet; a pet-Crawler heals like a Crawler."""
    box = {}

    def fn(state):
        c = _owner_for_pet(state, a.owner)
        pet = living_pet(c)
        if not pet:
            raise StateError(f"{c['name']} has no living plain pet (a pet-Crawler heals like any Crawler; Good Boy Gulp no longer works on it)")
        row = next((i for i in c["inventory"] if i.get("srd_id") == "heal-critter-potion"), None)
        if not row:
            raise StateError(f"{c['name']} has no Good Boy Gulp")
        row["qty"] -= 1
        if row["qty"] <= 0:
            c["inventory"].remove(row)
        box["roll"] = [random.randint(1, 4), random.randint(1, 4)]
        box["pet"], box["owner"] = pet["name"], c["name"]
        return state, c
    mutate(fn)
    hp = sum(box["roll"]) + 2
    ledgers.append("pet", {"event": "healed", "owner": box["owner"], "pet": box["pet"], "roll": box["roll"], "hp": hp, "reason": (a.reason or "").strip()})
    return {"ok": True, "hp": hp, "roll": box["roll"]}, f"{box['pet']} drinks Good Boy Gulp: 2d4+2 = {box['roll'][0]}+{box['roll'][1]}+2 = {hp} HP (GM applies it)"


def cmd_box(a):
    """box earn|open|show (add|use are aliases of earn|open). Every earn/open also lands in <session>/box-ledger.jsonl. Opening needs a safe room (--safe-room or `scene safe-room on`)."""
    if a.action == "show":
        rows = ledgers.read("box")
        if a.crawler:
            rows = [r for r in rows if r.get("crawler", "").lower() == a.crawler.lower()]
        rows = rows[-20:]
        return {"ok": True, "boxes": rows}, "\n".join(
            f"{r['ts'][:16]} {r.get('crawler')} {r.get('event')} {r.get('tier')} x{r.get('count', 1)}"
            + (f" '{r['box_name']}'" if r.get("box_name") else "") + (f" - deed: {r['deed']}" if r.get("deed") else "")
            + (f" - {r['reason']}" if r.get("reason") else "") + (f" -> {r['contents']}" if r.get("contents") else "") for r in rows) or "(no box events)"
    if not (a.crawler and a.tier):
        raise StateError("usage: box earn|open CRAWLER TIER [--count N] [--deed D] [--contents C]")
    tier = a.tier.lower()
    if tier not in BOX_TIERS:
        raise StateError(f"tier must be one of {', '.join(BOX_TIERS)}")
    earn = a.action in ("add", "earn")
    if tier == "legendary":
        raise StateError("Legendary boxes are Story Boxes: award one with `loot story-box FLOOR ZONE --crawler X --pick ID --deed ...` (box ledger: earned) and open it with `loot story-box --open --crawler X --safe-room`")
    where = None if earn else _require_safe_room(a, "opening a loot box")

    def fn(state):
        c = find_crawler(state, a.crawler)
        require_active(c, "earn or open boxes", a)
        if earn:
            if tier == "celestial" and c["boxes"]["celestial"] + a.count > 1:
                raise StateError(f"{c['name']}: only ONE Celestial box per crawler per campaign")
            c["boxes"][tier] += a.count
        else:
            if c["boxes"][tier] < a.count:
                raise StateError(f"{c['name']} has only {c['boxes'][tier]} {tier} box(es)")
            c["boxes"][tier] -= a.count
        return state, c
    c = mutate(fn)
    entry = {"event": "earned" if earn else "opened", "crawler": c["name"], "tier": tier, "count": a.count,
             "floor": read_state_file()["campaign"]["current_floor"]}
    if where:
        entry["safe_room"] = where
    for k, v in (("deed", a.deed), ("box_name", getattr(a, "box_name", None)), ("reason", _RUN.get("reason")), ("contents", getattr(a, "contents", None))):
        if v:
            entry[k] = v
    ledgers.append("box", entry)
    text = f"{c['name']} {tier} boxes: {c['boxes'][tier]}"
    return {"ok": True, "message": text}, text


def cmd_banner(a):
    """banner log TEXT | show: archive of the banners the System read out (sessions/banner-archive.jsonl)."""
    if a.action == "show":
        rows = ledgers.read("banner")[-a.n:]
        return {"ok": True, "banners": rows}, "\n".join(f"{r['ts'][:16]} F{r.get('floor')} {r.get('crawler') or '-'}: {r['text']}" for r in rows) or "(no banners archived)"
    if not (a.text and a.text.strip()):
        raise StateError("usage: banner log \"<text>\" [--crawler X]")
    st = read_state_file()
    entry = {"floor": st["campaign"]["current_floor"], "text": a.text.strip()}
    if a.crawler:
        entry["crawler"] = find_crawler(st, a.crawler)["name"]
    ledgers.append("banner", entry)
    return {"ok": True, "banner": entry}, f"banner archived ({len(entry['text'])} chars)"


def _write_card_data(row):
    """Record an item's mechanics for the sheet card (alpha: exports/card-data.json; other sessions: <data>/card-data.json)."""
    import publisher
    path = publisher.session_card_data_path() or publisher.card_data_path()
    data = publisher.read_json(path, {}) or {}
    data.setdefault("items", {})[publisher.norm(row["name"])] = {"category": row["category"], "mechanics": row["mechanics"]}
    atomic_write_json(path, data)


def cmd_loot(a):
    if a.action == "show":
        rows = ledgers.read("loot")
        if a.crawler:
            rows = [r for r in rows if r.get("crawler", "").lower() == a.crawler.lower()]
        rows = rows[-a.n:]
        return {"ok": True, "loot": rows}, "\n".join(loot.log_line(r) for r in rows) or "(no loot draws)"
    if a.action == "totals":
        t = loot.totals(ledgers.read("loot"), a.crawler, a.totals_floor)
        sales = [e for e in ledgers.read("story-box") if (e.get("event") == "sold" or (e.get("event") == "transferred" and e.get("price")))
                 and (not a.crawler or (e.get("crawler") or "").lower() == a.crawler.lower()) and (a.totals_floor is None or e.get("floor") == a.totals_floor)]
        out = {"ok": True, "totals": {c: {str(f): v for f, v in fl.items()} for c, fl in t.items()}, "story_box_sales": sales}
        flags = loot.FlagLines()      # per-floor flag lines from rules/70-encounter-budget-5e.json (1,500 fallback, never an error)
        text = loot.totals_text(t, sales, flags, footer=not getattr(a, "include_credits", False))
        if getattr(a, "include_credits", False):    # optional all-in view (Q-003 / A12): boxes + sale proceeds + earned credits; the default output above is unchanged
            srcs = _credit_sources_arg(a.credit_sources)
            af = None if a.assume_floor is None else _floor_arg(a.assume_floor, None)
            inc = loot.credit_income(read_ledger()[0], srcs, a.crawler, a.totals_floor, af)
            ai = loot.all_in(t, sales, inc)
            out["all_in"] = {c: {("unrecorded" if f is None else str(f)): v for f, v in fl.items()} for c, fl in ai.items()}
            text += "\n" + loot.all_in_text(ai, srcs, flags, footer=False)
            fl_shown = {f for fl in t.values() for f in fl} | loot.a_floors(ai)
            text += "".join("\n" + x for x in flags.footer(fl_shown))
        return out, text
    if a.action == "deeds":
        rows = [r for r in ledgers.read("story-box") if r.get("event") == "awarded"]
        lines = [f"{r['ts'][:10]} F{r.get('floor')} {r['crawler']}: {r.get('box_name') or r['card_id']} <- \"{r['deed']}\" "
                 f"[{r['deed_key']}] story {r.get('story_value', 0):g}" + (f" witness: {r['witness']}" if r.get("witness") else "") for r in rows]
        return {"ok": True, "deeds": rows}, "\n".join(lines) or "(no Story Boxes awarded)"
    if a.action == "story-box":
        if a.open:
            return _story_open(a)
        if a.loot_floor is None or not a.loot_zone or not a.crawler or not a.pick:
            raise StateError("usage: loot story-box FLOOR ZONE --crawler X --pick CARD_ID[,ID] --deed \"what happened\" --deed-id SLUG [--witness W] [--gm-note N] [--when T] [--box-name N] [--shared-with A,B] [--override-cap \"reason\"] [--dry-run] [--no-publish]   (award: box stays unopened)  |  loot story-box --open --crawler X [--box-id ID] --safe-room   (open, safe room only)")
        deed = (a.deed or "").strip()
        if len(deed) < 8:
            raise StateError("REFUSED: a Story Box needs the deed written down (--deed \"what the crawler did, in a sentence\"); nothing was awarded")
        deed_id = loot.deed_key(a.deed_id or "")
        if not deed_id:
            raise StateError("REFUSED: a Story Box needs --deed-id (the deed kind as a short slug, e.g. first-quadruped-in); without it rewording could dodge the registry. Nothing was awarded")
        story = {"deed": deed, "deed_id": deed_id, "witness": (a.witness or "").strip() or None,
                 "gm_note": (a.gm_note or "").strip() or None, "when": (a.when or "").strip() or None,
                 "box_name": (a.box_name or "").strip() or None, "shared_with": [x.strip() for x in (a.shared_with or "").split(",") if x.strip()]}
        try:
            return _loot_draw(a, story=story)
        except loot.LootError as e:
            raise StateError(str(e))
    # draw
    if a.loot_floor is None or not a.loot_zone or not a.crawler:
        raise StateError("usage: loot draw FLOOR ZONE --crawler X [--tier T] [--pull-type P] [--box-type B] [--pick CARD_ID] [--deed D] [--dry-run]")
    try:
        return _loot_draw(a)
    except loot.LootError as e:
        raise StateError(str(e))


def _loot_draw(a, story=None):
    """loot draw (random or one --pick) and loot story-box (one box of one or more hand-picked Legendary cards)."""
    state = read_state_file()
    who0 = find_crawler(state, a.crawler)
    require_active(who0, "receive loot", a)
    crawler = who0["name"]
    floor, zone = a.loot_floor, loot.norm_zone(a.loot_zone)
    decks, _skipped = loot.load_decks(floor, zone)
    if not decks:
        loot.err(f"no loot deck for floor {floor} zone {zone} in {loot.decks_dir()}")
    ledger = ledgers.read("loot")
    roll_total = None
    picks = [p.strip() for p in (a.pick or "").split(",") if p.strip()]
    if len(picks) > 1 and story is None:
        loot.err("--pick takes one card id for `loot draw`; several cards in one box go through `loot story-box --pick A,B`")
    chosen = []
    if picks:
        for pid in dict.fromkeys(picks):
            found = [(d, c) for d, c in loot._cards(decks) if c["id"] == pid]
            if not found:
                loot.err(f"card {pid} is not in the floor {floor} / {zone} decks")
            deck, card = found[0]
            if loot.is_stub(card):
                loot.err(f"card {pid} is a needs-verify stub; finish it in the deck file first")
            if card.get("unique") and any(e.get("card_id") == card["id"] for e in ledger) and not (story is not None and (getattr(a, "reaward", None) or "").strip() and card["id"] in _reclaimed_card_ids()):
                loot.err(f"{card['id']} is unique and was already drawn in this session")
            if card.get("exclusive_to") and card["exclusive_to"].lower() != crawler.lower():
                loot.err(f"{card['id']} is exclusive to {card['exclusive_to']}")
            chosen.append((deck, card))
    else:
        pool = loot.eligible(decks, crawler=crawler, floor=floor, ledger=ledger, tier=a.tier, pull_type=a.pull_type, box_type=a.box_type)
        if not pool:
            loot.err("no eligible cards (random draws skip weight-0, needs-verify, restricted tiers, already-drawn unique and already-owned items); hand-pick with --pick <card_id>")
        pick, roll_total = loot.weighted_pick(pool, crawler)
        chosen.append(pick)
    legendary = [str(c.get("tier")).lower() == "legendary" for _, c in chosen]
    if story is not None and not all(legendary):
        bad = next(c for (_, c), l in zip(chosen, legendary) if not l)
        loot.err(f"{bad['id']} is a {bad.get('tier')} card; `loot story-box` only awards Legendary Story Box cards (use `loot draw` for the rest)")
    is_story = any(legendary)
    override = None
    warnings = []
    box_id = same_box = None
    cap = have = None
    if is_story:
        if not state.get("limits", {}).get("legendary_enabled", DEFAULT_LIMITS["legendary_enabled"]):
            loot.err("the Legendary tier is switched off in this campaign (limits.legendary_enabled is false)")
        if story is None:
            c0 = chosen[0][1]
            loot.err(f"{c0['id']} is a Legendary Story Box card: award it with `loot story-box {floor} {zone} --crawler {crawler} --pick {c0['id']} --deed \"what they did\"` (it records the deed)")
        for _, card in chosen:
            g = card.get("grant") or {}
            if card.get("kind") in ("credits", "stat_bump") or g.get("credits") or g.get("roll"):
                loot.err("a Legendary card may not grant credits (story value is never convertible to credits)")
        keys = {loot.deed_key(c.get("deed") or story["deed"]) for _, c in chosen}
        boxes = {c.get("box_name") for _, c in chosen}
        if len(chosen) > 1 and len(keys) > 1 and len(boxes) > 1:
            loot.err("these cards are from different deeds and boxes, so they are separate Story Boxes: award them one per command")
        story["deed_key"] = story["deed_id"]
        box_name = story["box_name"] or chosen[0][1].get("box_name")
        players = [c for c in state["crawlers"] if crawler_kind(c) == "player" and is_active(c)]   # the rota counts ACTIVE player Crawlers only (benched Crawlers are not in play)
        living = [c["name"] for c in players if not any(x.lower() in ("dead", "deceased") for x in c.get("conditions", []))]
        names = {c["name"].lower(): c["name"] for c in state["crawlers"]}
        story["shared_with"] = [names.get(x.lower()) or loot.err(f"--shared-with: no crawler named {x}") for x in story["shared_with"]]
        if crawler in story["shared_with"]:
            loot.err("--shared-with lists the other contributors; the holder is --crawler")
        had = {r["crawler"] for r in ledgers.read("story-box") if r.get("event") == "awarded"}
        for r in ledgers.read("story-box"):
            if r.get("event") == "awarded":
                had |= set(r.get("shared_with") or [])
        waiting = [n for n in living if n not in had and n != crawler and n not in story["shared_with"]]
        if crawler in had and waiting:
            warnings.append(f"rota: {crawler} already has a Story Box and living crawler(s) with none yet: {', '.join(waiting)} (rules/45 section 6.1: consider a normal reward and a Title instead; warning only, never blocks)")
        rota_after = [n for n in living if n not in had and n != crawler and n not in story["shared_with"]]
        box_id = f"sb-{floor}-{story['deed_key']}"
        if len(chosen) > 1:
            same_box = (a.same_box_reason or "").strip() or f"same box: {', '.join(c['id'] for _, c in chosen)} are the pulls of one {chosen[0][1].get('box_name') or 'Story Box'} (one deed, counts once against the cap)"
        sbl = ledgers.read("story-box")
        prior = [r for r in sbl if r.get("event") == "awarded" and r.get("deed_key") == story["deed_key"]]
        reaward = (getattr(a, "reaward", None) or "").strip()
        if reaward and not prior:
            loot.err(f"--reaward: deed \"{story['deed_key']}\" has no earlier award; award it normally")
        if reaward:
            # Caleb's reclaim ruling: a deed whose box was reclaimed (holder died with it unopened) may be re-awarded ONCE per reclaim, to anyone, as a new box id.
            # Allowed only when EVERY prior award of this deed was reclaimed and none was opened, sold or released by a /delete (a deed closed by /delete stays closed).
            for r in prior:
                evs = {e.get("event") for e in sbl if e.get("box_id") == r["box_id"]}
                if "reclaimed" not in evs or evs & {"opened", "sold", "released"}:
                    loot.err(f"--reaward refused: the earlier award {r['box_id']} (to {r['crawler']}) is not a reclaimed, unopened box (events: {', '.join(sorted(evs - {'awarded'})) or 'none'}); a deed pays once, and a deed closed by opening, selling or /delete stays closed")
            box_id = f"{box_id}-r{len(prior) + 1}"
            story["reaward_of"] = [r["box_id"] for r in prior]
            story["reaward_reason"] = reaward
            warnings.append(f"RE-AWARD of a reclaimed box ({', '.join(story['reaward_of'])}): {reaward}")
        elif prior:
            r = prior[-1]
            loot.err(f"deed \"{story['deed_key']}\" was already awarded to {r['crawler']} on floor {r.get('floor')} ({r['card_id']}, {r['ts'][:10]}); a deed pays once. If this is a genuinely different deed, give it its own --deed-id (or, if that box was reclaimed when its holder died unopened, --reaward \"why\")")
        cap = state.get("limits", {}).get("legendary_cap_per_floor", DEFAULT_LIMITS["legendary_cap_per_floor"])
        have = loot.legendary_count(ledger, floor, ledgers.read("story-box"))
        if _is_int(cap) and have >= cap:
            if not a.override_cap:
                loot.err(f"Story Box cap reached for floor {floor}: {have} of {cap} already awarded on that floor (limits.legendary_cap_per_floor; the cap is per floor, unopened boxes count). Add --override-cap \"<reason>\" to exceed it; the reason is logged.")
            override = a.override_cap
        for _, card in chosen:
            warnings += [f"{card['id']}: {w}" if len(chosen) > 1 else w for w in loot.story_warnings(card)]
        if story["shared_with"] and not (story["witness"] or story["gm_note"]):
            warnings.append("a shared deed should name every contributor in --witness")
        if not (story["witness"] or story["gm_note"]):
            warnings.append("no --witness or --gm-note recorded with the deed")
    else:
        hold = loot.hold_note(chosen[0][1])
        if hold:
            warnings.append(f"deck note says: {hold}")
    entries, rows, lines = [], [], []
    amount, roll_expr = 0, None
    for (deck, card), leg in zip(chosen, legendary):
        tier = str(card.get("tier"))
        value = card.get("credit_value") or 0
        amt, rx = (loot.credits_amount(card) if card.get("kind") == "credits" and not leg else (0, None))
        amount, roll_expr = amount + amt, rx or roll_expr
        row = None if card.get("kind") in ("credits", "stat_bump") else loot.item_row(card)
        text = (card.get("ledger") or {}).get("text") or f"{card.get('kind')} {card.get('reskin_name')}"
        if card.get("kind") == "credits":
            text += f" ({amt:+d} credits{', rolled ' + rx if rx else ''})"
        if card.get("kind") == "stat_bump":
            text += " [NOT applied: stat bumps are HOUSE/draft-disabled; the GM applies it by hand if Caleb rules it in]"
        entry = {"event": "drawn", "crawler": crawler, "floor": floor, "zone": zone, "card_id": card["id"], "deck_id": deck.get("deck_id"),
                 "deck_version": deck.get("version"), "tier": tier, "kind": card.get("kind"), "reskin_name": card.get("reskin_name"),
                 "real_5e_name": card.get("real_5e_name"), "text": text, "pick": bool(picks),
                 "economy_value": 0 if leg else (amt if card.get("kind") == "credits" else value),
                 "story_value": loot.story_value_of(card) if leg else 0}
        for k, v in (("deed", (story or {}).get("deed") or a.deed or card.get("deed")), ("box_name", ((story or {}).get("box_name") if leg else None) or card.get("box_name")), ("override_cap", override),
                     ("roll", roll_total), ("credits_granted", amt or None), ("box_id", box_id), ("same_box", same_box if len(chosen) > 1 else None)):
            if v:
                entry[k] = v
        if story is not None:
            entry["story_box"] = True
        if picks:
            entry["override"] = "GM pick"
        entries.append(entry)
        rows.append((row, card))
        lines.append(loot.log_line(entry))
    sv = sum(e["story_value"] for e in entries)
    if story is not None:
        for (row, card), e in zip(rows, entries):
            if row:
                row.update(story_value=e["story_value"], story_box_id=box_id, card_id=card["id"], sale_value=loot.sale_value_of(card))
    if getattr(a, "dry_run", False):
        plan = "DRY RUN: nothing written.\n" + "\n".join(("Would award (box stays UNOPENED): " if story is not None else "Would award: ") + l for l in lines)
        if story is not None:
            plan += f"\n  deed: \"{story['deed']}\" [{story['deed_key']}], witness: {story['witness'] or '-'}, GM note: {story['gm_note'] or '-'}, when: {story['when'] or 'now'}"
            plan += f"\n  box name: {box_name} (the banner adds the tier: {_box_label(box_name)})" + (f"; shared deed with {', '.join(story['shared_with'])}" if story["shared_with"] else "") + f"\n  rota after this award (living, no Story Box yet): {', '.join(rota_after) or 'nobody'}"
            plan += f"\n  not bound: lootable, transferable, sellable (System buyback {sum(r['sale_value'] for r, _ in rows if r)} x floor multiplier); story value {sv:g} is provenance, never credited ({crawler}'s credits unchanged); box {have + 1}/{cap} on floor {floor}" + (f" (OVERRIDE: {override})" if override else "")
            plan += f"\n  award only records the deed; opening needs a safe room: loot story-box --open --crawler {crawler} --safe-room"
            if same_box:
                plan += f"\n  {len(chosen)} cards, ONE box: {same_box}"
        plan += "".join(f"\nWARNING: {w}" for w in warnings)
        return {"ok": True, "dry_run": True, "loot": entries, "warnings": warnings, "card_id": chosen[0][1]["id"]}, plan
    if story is None:
        where = _require_safe_room(a, "opening a loot box (a draw)")
        for e in entries:
            e["safe_room"] = where
        _RUN.update(reason=f"{chosen[0][1].get('tier')} box pull {chosen[0][1]['id']}", source="box")

        def fn(st):
            c = find_crawler(st, crawler)
            if amount:
                c["credits"] += amount
            _add_rows(c, [r for r, _ in rows if r])
            return st, c
        mutate(fn)
        for row, _card in rows:
            if row:
                _write_card_data(row)
        for e in entries:
            ledgers.append("loot", e)
        with open(os.path.join(sessions_dir(), "loot.log"), "a", encoding="utf-8") as f:
            for l in lines:
                f.write(l + "\n")
        announce = ""
        for row, card in rows:
            if row:
                announce += f"\n+ {card['reskin_name']}\n  {card.get('real_5e_name')} ({card.get('rarity')}): {row['mechanics']}"
        announce += "".join(f"\nWARNING: {w}" for w in warnings)
        return {"ok": True, "loot": entries, "card_id": chosen[0][1]["id"], "warnings": warnings}, "\n".join(lines) + announce
    # Story Box AWARD step: the deed is recorded and the box queued UNOPENED. Nothing enters the inventory until `--open` in a safe room.
    snapshot = {"entries": entries, "rows": [r for r, _ in rows if r], "lines": lines, "zone": zone}
    _RUN.update(reason=f"Story Box earned (unopened): {box_name}", source="box")

    def fn(st):
        c = find_crawler(st, crawler)
        c["boxes"]["legendary"] += 1
        return st, c
    mutate(fn)
    ledgers.append("story-box", {"event": "awarded", "box_id": box_id, "deed_key": story["deed_key"], "deed": story["deed"], "card_deed": chosen[0][1].get("deed"),
                                 "crawler": crawler, "floor": floor, "zone": zone, "card_id": chosen[0][1]["id"], "card_ids": [c["id"] for _, c in chosen],
                                 "box_name": box_name, "shared_with": story["shared_with"] or None, "rota_remaining": rota_after, "when": story["when"], "witness": story["witness"], "gm_note": story["gm_note"],
                                 "story_value": sv, "override_cap": override, "same_box": same_box, "warnings": warnings or None, "opened": False, "pending": snapshot,
                                 **({"reaward_of": story["reaward_of"], "reaward_reason": story["reaward_reason"]} if story.get("reaward_of") else {})})
    ledgers.append("box", {"event": "earned", "crawler": crawler, "tier": "legendary", "count": 1, "floor": floor, "deed": story["deed"], "box_name": box_name, "box_id": box_id,
                           "reason": "Story Box awarded (unopened)"})
    pub = "skipped (--no-publish)" if getattr(a, "no_publish", False) else ("started" if auto_publish() else "skipped (no GM_DISCORD_TOKEN or registered channel; run discord_gm.py publish --crawler %s)" % crawler)
    announce = (f"STORY BOX EARNED (unopened): {_box_label(box_name)} for {crawler}, floor {floor}\n  deed: {story['deed']} [{story['deed_key']}]"
                f"\n  contents (revealed on open): {', '.join(c['reskin_name'] for _, c in chosen)}{f' ({len(chosen)} cards, one box)' if len(chosen) > 1 else ''}"
                f"\n  rota now: {', '.join(rota_after) or 'nobody left'}; floor {floor} box {have + 1}/{cap}; card publish: {pub}"
                f"\n  It can only be opened in a safe room: python3 tools/state.py loot story-box --open --crawler {crawler} --safe-room")
    announce += "".join(f"\nWARNING: {w}" for w in warnings)
    return {"ok": True, "awarded": True, "opened": False, "box_id": box_id, "loot": entries, "card_id": chosen[0][1]["id"], "warnings": warnings}, announce


def _add_rows(c, rows):
    for row in rows:
        have_row = next((i for i in c["inventory"] if i["name"].lower() == row["name"].lower()), None)
        if have_row:
            have_row["qty"] += row.get("qty", 1)
        else:
            c["inventory"].append(dict(row))


def scene_path():
    return os.path.join(csession.data_dir(), "scene.json")


def scene_safe_room():
    try:
        with open(scene_path(), encoding="utf-8") as f:
            return bool(json.load(f).get("safe_room"))
    except (OSError, ValueError, AttributeError):
        return False


def _require_safe_room(a, what):
    """Every loot box (Story Boxes included) is opened in a safe room. -> 'flag' or 'scene'; raises otherwise."""
    if getattr(a, "safe_room", False):
        return "flag"
    if scene_safe_room():
        return "scene"
    raise StateError(f"REFUSED: loot boxes can only be opened in a safe room, so {what} is not allowed here. Nothing was changed. "
                     "Add --safe-room to this command, or set the scene with `python3 tools/state.py scene safe-room on` when the party reaches a safe room (and `off` when they leave).")


def cmd_scene(a):
    """scene safe-room on|off|show: the session flag that lets loot boxes be opened (<session data>/scene.json)."""
    if a.topic == "show" or a.value is None:
        on = scene_safe_room()
        return {"ok": True, "safe_room": on}, f"safe room: {'ON' if on else 'off'} (loot boxes can {'' if on else 'NOT '}be opened without --safe-room)"
    on = a.value == "on"
    entry = {"safe_room": on, "since": now_iso(), "floor": read_state_file()["campaign"]["current_floor"]}
    if a.note:
        entry["note"] = a.note
    os.makedirs(os.path.dirname(scene_path()), exist_ok=True)
    atomic_write_json(scene_path(), entry)
    return {"ok": True, "safe_room": on}, f"safe room: {'ON: loot boxes can be opened' if on else 'off: loot boxes are locked until the next safe room'}"


def _reclaimed_card_ids():
    """Card ids of Story Boxes that were RECLAIMED (holder died with them unopened): they went back to the System, so a --reaward may hand the card out again."""
    sb = ledgers.read("story-box")
    gone = {e.get("box_id") for e in sb if e.get("event") == "reclaimed"}
    return {cid for e in sb if e.get("event") == "awarded" and e.get("box_id") in gone for cid in (e.get("card_ids") or [e.get("card_id")])}


def _box_label(name):
    """'Legendary <name> Box' without doubling: card box names already end in 'Box' ('Pet Box', 'Four Paws Over the Threshold Box')."""
    n = str(name or "").strip()
    n = n[:-4].rstrip() if n.lower().endswith(" box") else n
    return f"Legendary {n} Box" if n else "Legendary Box"


def _story_open(a):
    """loot story-box --open --crawler X [--box-id ID] [--safe-room] [--dry-run]: step two. Needs a safe room. The items enter the inventory, the loot ledger
    gets the lines, and the box ledger records the open. A box opens once."""
    if not a.crawler:
        raise StateError("usage: loot story-box --open --crawler X [--box-id ID] --safe-room [--dry-run]")
    where = None if a.dry_run else _require_safe_room(a, "opening a Story Box")
    state = read_state_file()
    who = find_crawler(state, a.crawler)
    require_active(who, "open a Story Box", a)
    name = who["name"]
    sb = ledgers.read("story-box")
    opened = {e.get("box_id") for e in sb if e.get("event") in ("opened", "reclaimed", "released")}
    pending = [e for e in sb if e.get("event") == "awarded" and e.get("crawler") == name and e.get("pending") and e.get("box_id") not in opened]
    if a.box_id:
        pending = [e for e in pending if e["box_id"] == a.box_id]
    if not pending:
        raise StateError(f"{name} has no unopened Story Box" + (f" with id {a.box_id}" if a.box_id else ""))
    if len(pending) > 1:
        raise StateError(f"{name} has {len(pending)} unopened Story Boxes ({', '.join(e['box_id'] for e in pending)}); pick one with --box-id")
    aw = pending[0]
    snap = aw["pending"]
    if any(x.lower() in ("dead", "deceased") for x in who.get("conditions", [])):
        raise StateError(f"{name} is Dead; a Story Box is opened by a living Crawler in a safe room (it stays queued)")
    names = ", ".join(r["name"] for r in snap["rows"]) or "(no item)"
    if a.dry_run:
        return {"ok": True, "dry_run": True, "box_id": aw["box_id"]}, (f"DRY RUN: would open {_box_label(aw.get('box_name'))} for {name}: {names}. "
                                                                        f"Safe room: {'yes (' + ('scene flag' if scene_safe_room() else '--safe-room') + ')' if (scene_safe_room() or a.safe_room) else 'NO: a real open would be refused'}")
    _RUN.update(reason=f"Story Box opened: {aw.get('box_name')}", source="box")

    def fn(st):
        c = find_crawler(st, name)
        c["boxes"]["legendary"] = max(0, c["boxes"].get("legendary", 0) - 1)
        _add_rows(c, snap["rows"])
        return st, c
    mutate(fn)
    for row in snap["rows"]:
        _write_card_data(row)
    for e in snap["entries"]:
        ledgers.append("loot", {**e, "safe_room": where, "box_id": aw["box_id"]})
    with open(os.path.join(sessions_dir(), "loot.log"), "a", encoding="utf-8") as f:
        for l in snap["lines"]:
            f.write(l + "\n")
    ledgers.append("story-box", {"event": "opened", "box_id": aw["box_id"], "crawler": name, "floor": aw.get("floor"), "items": [r["name"] for r in snap["rows"]], "safe_room": where})
    ledgers.append("box", {"event": "opened", "crawler": name, "tier": "legendary", "count": 1, "floor": aw.get("floor"), "box_name": aw.get("box_name"), "box_id": aw["box_id"],
                           "contents": names, "safe_room": where, "reason": "Story Box opened in a safe room"})
    pub = "skipped (--no-publish)" if getattr(a, "no_publish", False) else ("started" if auto_publish() else "skipped (no GM_DISCORD_TOKEN or registered channel)")
    out = f"opened {_box_label(aw.get('box_name'))} for {name} (safe room via {where}):"
    for row in snap["rows"]:
        out += f"\n+ {row['name']}\n  {row.get('notes') or ''}: {row['mechanics']}"
    out += f"\n  not bound: it can be looted, traded or sold (sale_value {sum(r.get('sale_value', 0) for r in snap['rows'])} x floor multiplier at the System buyback); card publish: {pub}"
    return {"ok": True, "box_id": aw["box_id"], "items": [r["name"] for r in snap["rows"]]}, out


def _find_item(c, item):
    it = next((i for i in c["inventory"] if i["name"].lower() == item.lower()), None)
    if not it:
        raise StateError(f"{c['name']} has no '{item}'")
    return it


def _story_provenance(it):
    if not (it.get("story_box_id") or it.get("story_value")):
        return None
    return {"story_box_item": it["name"], "story_value": it.get("story_value", 0), "story_box_id": it.get("story_box_id"), "card_id": it.get("card_id")}


def cmd_sell(a):
    """sell CRAWLER ITEM --reason TEXT [--qty N] [--price N] [--floor N] [--dry-run]. An ordinary credit-ledger transaction.
    A Story Box item sold to the System pays its card's sale_value x the floor multiplier of the sale floor (default 500), never its story_value."""
    if not (a.reason or "").strip():
        raise StateError("sell needs --reason \"why/where it was sold\" (it goes in the credit ledger)")
    if a.price is not None and a.price < 0:
        raise StateError("--price must be >= 0")
    state = read_state_file()
    c = find_crawler(state, a.crawler)
    require_active(c, "sell (benched Crawlers cannot be mules)")
    it = _find_item(c, a.item)
    qty = a.qty
    if qty < 1 or qty > it["qty"]:
        raise StateError(f"{c['name']} has only {it['qty']} x {it['name']}")
    _pet_item_gate(it, c, "sold")
    floor = a.floor if a.floor is not None else state["campaign"]["current_floor"]
    prov = _story_provenance(it)
    if a.price is not None:
        total, basis = a.price, f"GM-set price {a.price}"
    elif prov:
        unit = it.get("sale_value") if _is_int(it.get("sale_value")) and it["sale_value"] > 0 else loot.DEFAULT_SALE_VALUE
        mult = loot.floor_multiplier(floor)
        total, basis = unit * mult * qty, f"System buyback: sale_value {unit} x{mult} (floor {floor}) x{qty}"
    else:
        raise StateError(f"'{it['name']}' has no sale_value; give the price with --price N")
    reason = f"Sold {qty}x {it['name']} ({basis}): {a.reason.strip()}"
    if a.dry_run:
        return {"ok": True, "dry_run": True, "credits": total}, f"DRY RUN: {c['name']} would sell {qty}x {it['name']} for {total} credits ({basis})" + (f"\nFLAG: Story Box item; story value {prov['story_value']:g} is provenance only and is NOT credited" if prov else "")
    _RUN.update(reason=reason, source="sale", ledger_extra={"*": prov} if prov else {"*": {"sold_item": it["name"]}})

    def fn(st):
        cc = find_crawler(st, c["name"])
        row = _find_item(cc, it["name"])
        row["qty"] -= qty
        if row["qty"] <= 0:
            cc["inventory"].remove(row)
        cc["credits"] += total
        return st, cc
    cc = mutate(fn)
    if prov:
        ledgers.append("story-box", {"event": "sold", "crawler": c["name"], "item": it["name"], "qty": qty, "price": total, "floor": floor, "story_value": prov["story_value"],
                                     "card_id": prov["card_id"], "box_id": prov["story_box_id"], "basis": basis, "reason": a.reason.strip()})
    text = f"{c['name']} sold {qty}x {it['name']} for {total} credits ({basis}); credits now {cc['credits']}"
    if prov:
        text += f"\nFLAG: Story Box item sold. Story value {prov['story_value']:g} is provenance only and was NOT credited."
    return {"ok": True, "credits": total, "story_box_item": bool(prov)}, text


def cmd_transfer(a):
    """transfer FROM TO ITEM --reason TEXT [--qty N] [--price N]: crawler to crawler (a gift, a trade, or loot from a corpse). With --price the buyer pays the seller
    in credits (free-form, no multiplier); a Story Box item keeps its provenance and a priced transfer is flagged."""
    if not (a.reason or "").strip():
        raise StateError("transfer needs --reason (e.g. \"traded\", \"looted from the corpse\")")
    if a.frm.lower() == a.to.lower():
        raise StateError("transfer needs two different crawlers")
    price = a.price or 0
    if price < 0:
        raise StateError("--price must be >= 0")
    state = read_state_file()
    src, dst = find_crawler(state, a.frm), find_crawler(state, a.to)
    if same_player(src, dst):
        raise StateError(f"REFUSED: {src['name']} and {dst['name']} belong to the same player; items and credits never move between a player's own Crawlers (active or benched)")
    require_active(src, "trade or transfer items (benched Crawlers cannot be mules)")
    require_active(dst, "receive transferred items (benched Crawlers cannot be mules)")
    it = _find_item(src, a.item)
    if a.qty < 1 or a.qty > it["qty"]:
        raise StateError(f"{src['name']} has only {it['qty']} x {it['name']}")
    _pet_item_gate(it, dst, "received")
    if price and dst["credits"] < price and not a.allow_debt:
        raise StateError(f"{dst['name']} has {dst['credits']} credits; cannot pay {price} (use --allow-debt to go negative)")
    prov = _story_provenance(it)
    floor = state["campaign"]["current_floor"]
    if a.dry_run:
        return {"ok": True, "dry_run": True}, f"DRY RUN: {src['name']} -> {dst['name']}: {a.qty}x {it['name']}" + (f" for {price} credits" if price else " (no payment)") + (f"\nFLAG: Story Box item sold between crawlers; story value {prov['story_value']:g} is provenance only" if prov and price else "")
    ex = {"*": prov} if prov and price else {"*": {"transfer_item": it["name"]}}
    _RUN.update(reason=f"{'Sold' if price else 'Transferred'} {a.qty}x {it['name']} {src['name']} -> {dst['name']}: {a.reason.strip()}", source="transfer", ledger_extra=ex if price else None)

    def fn(st):
        s1, s2 = find_crawler(st, src["name"]), find_crawler(st, dst["name"])
        row = _find_item(s1, it["name"])
        moved = dict(row, qty=a.qty)
        row["qty"] -= a.qty
        if row["qty"] <= 0:
            s1["inventory"].remove(row)
        _add_rows(s2, [moved])
        if price:
            s2["credits"] -= price
            s1["credits"] += price
        return st, None
    mutate(fn)
    if prov:
        ledgers.append("story-box", {"event": "transferred", "crawler": src["name"], "to": dst["name"], "item": it["name"], "qty": a.qty, "price": price, "floor": floor,
                                     "story_value": prov["story_value"], "box_id": prov["story_box_id"], "reason": a.reason.strip()})
    text = f"{src['name']} -> {dst['name']}: {a.qty}x {it['name']}" + (f" for {price} credits" if price else " (no payment)")
    if prov and price:
        text += f"\nFLAG: Story Box item sold between crawlers. Story value {prov['story_value']:g} is provenance only and was NOT credited."
    return {"ok": True, "price": price, "story_box_item": bool(prov)}, text


# --------------------------------------------------------------------------- floor lost (decision 028) and looting a body

def _is_dead(c):
    return any(x.lower() in ("dead", "deceased") for x in c.get("conditions", []))


MAX_FLOOR = 18


def _ascii_uint(raw):
    """Whole number written with ASCII digits 0-9 only (no signs, decimals, spaces inside, or look-alike Unicode digits). Returns int or None."""
    t = str(raw)                      # no strip: " 5", "5 " and "5\n" are refused, as are look-alike Unicode digits, signs and decimals
    return int(t) if re.fullmatch(r"[0-9]+", t) else None


def _floor_arg(raw, default):
    """--floor for floor-lost / loot-body: ASCII digits, 1 to MAX_FLOOR; None means the campaign's current floor."""
    if raw is None:
        return default
    n = _ascii_uint(raw)
    if n is None or not 1 <= n <= MAX_FLOOR:
        raise StateError(f"--floor must be a whole number from 1 to {MAX_FLOOR} (got {str(raw).strip()!r})")
    return n


def _credit_sources_arg(raw):
    """--credit-sources: only the known earned-credit sources (loot.CREDIT_SOURCES). Anything else (loot_body, transfer, box, sale ...) is refused, never silently counted."""
    if raw is None:
        return list(loot.CREDIT_SOURCES)
    names = [x.strip().lower() for x in raw.split(",")]
    if not [n for n in names if n]:
        raise StateError(f"--credit-sources needs at least one source name. Valid names: {', '.join(sorted(loot.CREDIT_SOURCES))}")
    bad = [n or "(empty)" for n in names if n not in loot.CREDIT_SOURCES]
    if bad:
        raise StateError(f"--credit-sources: unknown source name(s): {', '.join(dict.fromkeys(bad))}. Valid names: {', '.join(sorted(loot.CREDIT_SOURCES))}. "
                         "(Box pulls, sales, transfers and body loot are never counted as earned credits.)")
    return list(dict.fromkeys(names))


def _items_digest(items):
    """Short fingerprint of an item list (names lower-cased, sorted), stored beside the list so an edited ledger entry is caught by `ledger verify`."""
    import hashlib
    canon = json.dumps(sorted([str(i.get("name", "")).lower(), i.get("qty")] for i in items or []), separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:16]


def _items_text(rows):
    return ", ".join(f"{r['qty']}x {r['name']}" for r in rows) or "no items"


def cmd_floor_lost(a):
    """floor-lost CRAWLER --reason TEXT [--floor N] [--mark-dead] [--dry-run]. Decision 028 (Caleb): a Crawler who misses the floor collapse dies and their credits and items
    are destroyed with the floor. ONE append-only ledger entry (event floor_lost, source floor_lost) takes the balance to 0 and records the exact coins and item rows destroyed,
    so the Crawler's ledger total reconciles to zero with no special case. The Crawler must already be DEAD (or pass --mark-dead). XP, achievements and boxes are not touched
    (an unopened Story Box is reclaimed by the usual death rule when --mark-dead adds the condition). NPCs and the AI lose nothing: only player and pet-crawler records are accepted.
    Coins are integers, nothing is rounded. Run it AFTER any looting of the body (loot-body); a body that was already written off has nothing left and is refused."""
    if not (a.reason or "").strip():
        raise StateError("floor-lost needs --reason (it goes in the credit ledger), e.g. \"missed the F1 collapse\"")
    state = read_state_file()
    c = find_crawler(state, a.crawler)
    if crawler_kind(c) not in ("player", "pet-crawler"):
        raise StateError(f"REFUSED: {c['name']} is a {crawler_kind(c)}; NPCs and the AI go into stasis at a collapse and lose nothing (decision 028)")
    if not _is_dead(c) and not a.mark_dead:
        raise StateError(f"REFUSED: {c['name']} is not DEAD. A missed collapse is death: add the condition first (`condition add {c['name']} Dead`) or pass --mark-dead")
    floor = _floor_arg(a.floor, state["campaign"]["current_floor"])
    if not c["credits"] and not c["inventory"]:
        note = "" if _is_dead(c) else f" ({c['name']} was NOT marked Dead: nothing changed; use `condition add {c['name']} Dead` if needed)"
        return {"ok": True, "nothing_to_destroy": True}, f"{c['name']}: nothing left to destroy (0 credits, no items; already written off?). No ledger entry added.{note}"
    if a.dry_run:
        return {"ok": True, "dry_run": True, "coins": c["credits"], "items": c["inventory"]}, f"DRY RUN: floor lost for {c['name']} (floor {floor}): {c['credits']} credits and {_items_text(c['inventory'])} would be destroyed"
    destroyed = {}
    _RUN.update(reason=f"Floor lost: written off with floor {floor}: {a.reason.strip()}", source="floor_lost", row_extra={c["name"]: {"event": "floor_lost", "floor": floor, "destroyed": destroyed}}, force_rows={c["name"]})

    def fn(st):
        cc = find_crawler(st, c["name"])
        if not cc["credits"] and not cc["inventory"]:
            raise StateError(f"REFUSED: {cc['name']} has no credits and no items left; nothing left to destroy (changed while this ran)")
        destroyed.update(coins=cc["credits"], items=copy.deepcopy(cc["inventory"]), item_count=sum(i.get("qty", 1) for i in cc["inventory"]),
                         items_digest=_items_digest(cc["inventory"]))
        cc["credits"] = 0
        cc["inventory"] = []
        if not _is_dead(cc):
            cc["conditions"].append("Dead")
        return st, None
    mutate(fn)
    text = f"{c['name']}: floor {floor} lost. Destroyed {destroyed['coins']} credits and {_items_text(destroyed['items'])}; credits now 0 (ledger event floor_lost)"
    if a.mark_dead:
        text += _reclaim_unopened_boxes(c["name"], "Dead")
    return {"ok": True, "destroyed": destroyed}, text


def cmd_loot_body(a):
    """loot-body DEAD SURVIVOR --reason TEXT [--coins N|all] [--item NAME[=QTY]]... [--all-items] [--floor N] [--dry-run]. A survivor takes coins and items from the body BEFORE the
    collapse (decision 028). One transfer: the dead Crawler is debited and the survivor credited by the same integer amount, two ledger rows (event body_loot, role from/to) that share a
    transfer_id and list the items moved, so no credit is counted twice or lost. Item rows move like `transfer` (Story Box provenance kept and logged). Anything left is written
    off by `floor-lost`. Refuses a body that is not DEAD, a survivor that is dead or benched, and a Crawler of the same player (as `transfer` does)."""
    if not (a.reason or "").strip():
        raise StateError("loot-body needs --reason (it goes in the credit ledger)")
    if a.frm.lower() == a.to.lower():
        raise StateError("loot-body needs two different crawlers")
    state = read_state_file()
    dead, who = find_crawler(state, a.frm), find_crawler(state, a.to)
    if not _is_dead(dead):
        raise StateError(f"REFUSED: {dead['name']} is not DEAD; use `transfer` for a living Crawler")
    for x, role in ((dead, "a body"), (who, "a looter")):
        if crawler_kind(x) not in ("player", "pet-crawler"):
            raise StateError(f"REFUSED: {x['name']} is a {crawler_kind(x)}, not a Crawler; only Crawlers can be {role} here (pets and companions have no credits or loot, decision 022)")
    if _is_dead(who):
        raise StateError(f"REFUSED: {who['name']} is dead and cannot loot")
    if same_player(dead, who):
        raise StateError(f"REFUSED: {dead['name']} and {who['name']} belong to the same player; items and credits never move between a player's own Crawlers")
    require_active(who, "loot a body (benched Crawlers cannot be mules)")
    coins = 0
    if a.coins is not None:
        if a.coins.lower() == "all":
            coins = dead["credits"]
        elif _ascii_uint(a.coins) is not None:
            coins = _ascii_uint(a.coins)
        else:
            raise StateError(f"--coins must be a whole number of credits written with the digits 0-9 only (no spaces, signs, decimals or other characters), or 'all' (got {a.coins!r})")
        if coins < 0 or coins > dead["credits"]:
            raise StateError(f"{dead['name']} has {dead['credits']} credits; cannot loot {coins}")
    wanted = []
    for spec in a.item or []:
        name, _, q = spec.rpartition("=") if "=" in spec else (spec, "", "")
        name = (name if "=" in spec else spec).strip()
        if not name:
            raise StateError(f"--item {spec!r} has no item name (use NAME or NAME=QTY)")
        if "=" in spec:
            n = _ascii_uint(q)
            if n is None:
                raise StateError(f"--item {spec!r}: the quantity must be a whole number of 1 or more written with digits 0-9 (not negative, not a decimal, not text)")
            if n < 1:
                raise StateError(f"--item {spec!r}: a quantity of 0 takes nothing; use 1 or more, or leave the item out")
        else:
            n = 1
        wanted.append((name, n))
    if a.all_items:
        wanted += [(i["name"], i["qty"]) for i in dead["inventory"] if i["name"].lower() not in {w[0].lower() for w in wanted}]
    moved = []
    for name, q in wanted:
        it = _find_item(dead, name)
        if q < 1 or q > it["qty"]:
            raise StateError(f"{dead['name']} has only {it['qty']} x {it['name']}")
        _pet_item_gate(it, who, "received")
        moved.append(dict(it, qty=q))
    if len({m["name"].lower() for m in moved}) != len(moved):
        raise StateError("an item is listed twice")
    if not coins and not moved:
        raise StateError("loot-body needs --coins and/or --item/--all-items (nothing to take)")
    floor = _floor_arg(a.floor, state["campaign"]["current_floor"])
    if a.dry_run:
        return {"ok": True, "dry_run": True, "coins": coins, "items": moved}, f"DRY RUN: {who['name']} would take {coins} credits and {_items_text(moved)} from {dead['name']}"
    tid = "body-" + dt.datetime.now().strftime("%Y%m%dT%H%M%S") + f"-{random.randrange(16**4):04x}"
    base = {"event": "body_loot", "transfer_id": tid, "floor": floor, "coins": coins, "items": copy.deepcopy(moved),
            "item_count": sum(m["qty"] for m in moved), "items_digest": _items_digest(moved)}
    _RUN.update(reason=f"Looted from the body of {dead['name']} by {who['name']} ({coins} credits, {_items_text(moved)}): {a.reason.strip()}", source="loot_body",
                row_extra={dead["name"]: {**base, "role": "from", "counterparty": who["name"]}, who["name"]: {**base, "role": "to", "counterparty": dead["name"]}}, force_rows={dead["name"], who["name"]})

    def fn(st):
        d, w = find_crawler(st, dead["name"]), find_crawler(st, who["name"])
        if coins > d["credits"]:
            raise StateError(f"{d['name']} has {d['credits']} credits; cannot loot {coins}")
        for m in moved:
            row = _find_item(d, m["name"])
            if m["qty"] > row["qty"]:
                raise StateError(f"{d['name']} has only {row['qty']} x {row['name']}")
            row["qty"] -= m["qty"]
            if row["qty"] <= 0:
                d["inventory"].remove(row)
        _add_rows(w, copy.deepcopy(moved))
        d["credits"] -= coins
        w["credits"] += coins
        return st, None
    mutate(fn)
    for m in moved:
        prov = _story_provenance(m)
        if prov:
            ledgers.append("story-box", {"event": "transferred", "crawler": dead["name"], "to": who["name"], "item": m["name"], "qty": m["qty"], "price": 0, "floor": floor,
                                         "story_value": prov["story_value"], "box_id": prov["story_box_id"], "reason": "looted from the body: " + a.reason.strip()})
    text = f"{who['name']} looted {dead['name']}: {coins} credits and {_items_text(moved)} (transfer {tid})"
    return {"ok": True, "transfer_id": tid, "coins": coins, "items": moved}, text


# --------------------------------------------------------------------------- sessions, active Crawler, swap, delete

def session_status_path():
    return os.path.join(csession.data_dir(), "session-status.json")


def _session_record():
    try:
        with open(session_status_path(), encoding="utf-8") as f:
            r = json.load(f)
        return r if isinstance(r, dict) else {}
    except (OSError, ValueError):
        return {}


def session_window():
    """The between-session window id = how many times a session has been opened so far. A swap is allowed once per player per window."""
    try:
        return int(_session_record().get("opens", 0))
    except (TypeError, ValueError):
        return 0


def session_open():
    """-> (is_open, why). A session is OPEN when `state.py session-status open` was recorded (the bridge writes it on /join and clears it on /leave),
    or a GM run holds a fresh GM lock (gm_lock.sh, under 120 s old). No file and no lock = closed (the default), so a swap is allowed."""
    st = _session_record()
    if str(st.get("status", "")).lower() == "open":
        return True, f"the session is open (since {st.get('since', '?')}{', ' + st['note'] if st.get('note') else ''}; the GM closes it with `state.py session-status close`)"
    lock = os.path.join(csession.data_dir(), ".gm-lock")
    try:
        if time.time() - os.stat(lock).st_mtime < 120:
            return True, "a GM run holds the session lock right now"
    except OSError:
        pass
    return False, ""


def cmd_session_status(a):
    """session-status open|close|show [--note T]: whether a play session is open (blocks Crawler swaps and deleting the active Crawler)."""
    if a.action == "show":
        op, why = session_open()
        return {"ok": True, "open": op, "why": why or None, "window": session_window()}, ("session OPEN: " + why) if op else f"no session is open (swaps allowed; between-session window {session_window()})"
    prev = _session_record()
    was_open = str(prev.get("status", "")).lower() == "open"
    opens = session_window()
    if a.action == "open" and was_open:   # idempotent: a second /join (or a reconnect) neither resets `since` nor starts a new window
        return {"ok": True, **prev}, f"session already open (window {opens}); nothing changed"
    if a.action == "close" and prev and not was_open:
        return {"ok": True, **prev}, f"session already closed (window {opens}); nothing changed"
    entry = {"status": "open" if a.action == "open" else "closed", "since": now_iso(), "by": a.by or "gm", "opens": opens}
    if a.action == "open":
        # the swap window is tied to a REAL session: re-opening within SESSION_REOPEN_GRACE_S of a close (a dropped voice connection, a quick /leave and /join) is the same session/window
        closed_at = prev.get("closed_at_epoch")
        regrace = isinstance(closed_at, (int, float)) and time.time() - closed_at < SESSION_REOPEN_GRACE_S and not getattr(a, "fresh", False)
        if not regrace:
            entry["opens"] = opens + 1
        if prev.get("closed_at_epoch") is not None and regrace:
            entry["reopened"] = True
    else:
        entry["closed_at_epoch"] = time.time()
    if a.note:
        entry["note"] = a.note
    os.makedirs(os.path.dirname(session_status_path()), exist_ok=True)
    atomic_write_json(session_status_path(), entry)
    return {"ok": True, **entry}, f"session {entry['status']} (window {entry['opens']})" + (" - re-opened within the grace period: same window" if entry.get("reopened") else "")


def _player_crawlers(state, who):
    return [c for c in state["crawlers"] if crawler_kind(c) in ("player", "pet-crawler") and same_player(c, who)]


def _owned_by(state, player=None, user_id=None):
    out = []
    for c in state["crawlers"]:
        if crawler_kind(c) not in ("player", "pet-crawler"):
            continue
        uid = (c.get("build") or {}).get("discord_user_id")
        if (user_id and uid and str(uid) == str(user_id)) or (player and str(c.get("player", "")).strip().lower() == str(player).strip().lower()):
            out.append(c)
    return out


def _channel_for(name):
    try:
        import publisher
        key, m = publisher.mapping_for(publisher.load_config(), name)
        return m or {}
    except Exception:
        return {}


def cmd_crawler(a):
    """crawler list [--player P] [--user-id ID] | activate NAME --reason T | migrate | delete NAME --reason T --confirm"""
    if a.action == "list":
        state = read_state_file()
        rows = state["crawlers"]
        if a.user_id or a.player:
            rows = _owned_by(state, a.player, a.user_id)
        out = []
        for c in rows:
            m = _channel_for(c["name"])
            out.append({"name": c["name"], "class": c.get("class"), "species": c.get("species"), "level": c.get("level"), "player": c.get("player"), "kind": crawler_kind(c),
                        "status": crawler_status(c) or None, "owner": c.get("owner"), "channel_id": m.get("channel_id"), "channel_name": m.get("channel_name")})
        lines = [f"- {r['name']} [{r['kind']}{', ' + r['status'] if r['status'] else ''}] L{r['level']} {r['species']} {r['class']} (player {r['player']})"
                 + (f" #{r['channel_name']}" if r["channel_name"] else "") for r in out]
        return {"ok": True, "crawlers": out}, "\n".join(lines) or "(no crawlers)"
    if a.action == "migrate":
        def fn(st):
            done = []
            for kind in ("player", "pet-crawler"):
                for c in st["crawlers"]:
                    if crawler_kind(c) == kind and "status" not in c:
                        if kind == "player":
                            c["status"] = "benched" if any(x is not c and crawler_kind(x) == "player" and x.get("status") == "active" and same_player(x, c) for x in st["crawlers"]) else "active"
                        else:
                            assign_status(st, c)
                        done.append(f"{c['name']}={c['status']}")
            return st, done
        done = mutate(fn)
        return {"ok": True, "migrated": done}, ("status set: " + ", ".join(done)) if done else "nothing to migrate (every Crawler has a status)"
    if a.action == "requests":
        reqs, state = ledgers.read("swap-request"), read_state_file()
        pend = [r for r in reqs if (lambda c: c and not is_active(c))(next((x for x in state["crawlers"] if x["name"] == r.get("crawler")), None))]
        return {"ok": True, "pending": pend}, "\n".join(f"- {r['ts']}: {r.get('player')} asks to make {r['crawler']} active ({r.get('reason')})" for r in pend) or "no pending swap requests"
    if not (a.crawler and (a.reason or "").strip()):
        raise StateError(f"usage: crawler {a.action} CRAWLER --reason \"why\"")
    if a.action == "delete":
        return _crawler_delete(a)
    if a.action == "request":
        return _crawler_request(a)
    return _crawler_activate(a)


def _owner_check(state, c, a, what):
    """S1: a Crawler with a recorded build.discord_user_id belongs to THAT Discord account only (a display name can be spoofed); name matching is the fallback for legacy
    Crawlers that have no id. No --as-player/--as-user = the GM, who may do anything."""
    if not (a.as_player or a.as_user):
        return None
    uid = (c.get("build") or {}).get("discord_user_id")
    if uid:
        if a.as_user and str(a.as_user) == str(uid):
            return None
        return f"REFUSED: you can only {what} your own Crawlers"
    if a.as_player and c["name"] in {x["name"] for x in _owned_by(state, a.as_player, None)}:
        return None
    return f"REFUSED: you can only {what} your own Crawlers"


def _swap_refused(state, c, a, kind, why):
    ledgers.append("swap", {"event": "refused", "kind": kind, "player": c.get("player"), "target": c["name"], "reason": why, "asked_because": (a.reason or "").strip(),
                            "by": a.by or a.as_user or a.as_player or "gm", "floor": state["campaign"]["current_floor"], "window": session_window()})
    raise StateError(why)


def _crawler_request(a):
    """crawler request CRAWLER --reason T --as-user ID: a player asks the GM to make a Crawler active. Never changes a Crawler; refused while a session is open."""
    state = read_state_file()
    c = find_crawler(state, a.crawler)
    bad = _owner_check(state, c, a, "request a swap for")
    if bad:
        raise StateError(bad)
    if crawler_kind(c) != "player":
        raise StateError(f"{c['name']} is a {crawler_kind(c)}; only player Crawlers can be made active (a pet-Crawler follows its owner)")
    if is_active(c):
        raise StateError(f"{c['name']} is already your active Crawler")
    op, why = session_open()
    if op:
        _swap_refused(state, c, a, "request", f"No swap while a session is open: {why}. Your active Crawler is locked for the whole session, even in a safe room. Ask again between sessions.")
    row = ledgers.append("swap-request", {"player": c.get("player"), "crawler": c["name"], "from": [x["name"] for x in state["crawlers"] if crawler_kind(x) == "player" and is_active(x) and same_player(x, c)],
                                           "reason": a.reason.strip(), "by": a.by or a.as_user or a.as_player or "player", "floor": state["campaign"]["current_floor"], "window": session_window()})
    return {"ok": True, "request": row}, f"swap request recorded: {c.get('player')} asks to make {c['name']} active. Nothing changed; the GM approves with `state.py crawler activate \"{c['name']}\" --reason ...`"


def _crawler_activate(a):
    """GM swap / "make active now": between sessions only, one swap per player per window, every swap and refusal logged."""
    state = read_state_file()
    c = find_crawler(state, a.crawler)
    kind = crawler_kind(c)
    bad = _owner_check(state, c, a, "swap to")
    if bad:
        _swap_refused(state, c, a, "swap", bad)
    if kind == "pet-crawler":
        raise StateError(f"{c['name']} is a pet-Crawler: it follows its owner ({c.get('owner')}); activate the owner instead")
    if kind != "player":
        raise StateError(f"{c['name']} is a {kind}, not a player Crawler")
    if is_active(c):
        raise StateError(f"{c['name']} is already the active Crawler")
    prev = [x["name"] for x in state["crawlers"] if crawler_kind(x) == "player" and is_active(x) and x["name"] != c["name"] and same_player(x, c)]
    op, why = session_open()
    # the lock protects an ACTIVE Crawler from being swapped out mid-session (a dead one included). A human with NO active Crawler at all (new to the table, benched on arrival) is not a swap.
    if op and prev:
        _swap_refused(state, c, a, "swap", f"REFUSED: {why}. The active Crawler is locked for the whole session; swaps are only allowed between sessions (not even in a safe room).")
    # N1: never activate a dead Crawler
    if any(x.lower() in ("dead", "deceased") for x in c.get("conditions", [])):
        _swap_refused(state, c, a, "swap", f"REFUSED: {c['name']} is DEAD; a dead Crawler cannot be made active (revive it first, CORE 6.3)")
    win = session_window()
    used = [e for e in ledgers.read("swap") if e.get("event") == "swap" and e.get("window") == win and str(e.get("player", "")).lower() == str(c.get("player", "")).lower() and e.get("from")]
    override = (getattr(a, "override_window", None) or "").strip()
    if prev and used and not override:
        _swap_refused(state, c, a, "swap", f"REFUSED: {c.get('player')} already swapped this window ({used[-1].get('from')} -> {used[-1].get('activated')}); one swap per player per between-session window. The GM may add --override-window \"why\".")
    if a.dry_run:
        return {"ok": True, "dry_run": True}, f"DRY RUN: would activate {c['name']} and bench {', '.join(prev) or 'nothing'}"

    def fn(st):
        cc = find_crawler(st, c["name"])
        for x in st["crawlers"]:
            if x["name"] in prev:
                x["status"] = "benched"
        cc["status"] = "active"
        for x in st["crawlers"]:
            if crawler_kind(x) == "pet-crawler" and str(x.get("owner", "")).lower() in {n.lower() for n in prev + [cc["name"]]}:
                x["status"] = "active" if x.get("owner", "").lower() == cc["name"].lower() else "benched"
        return st, cc
    mutate(fn)
    ledgers.append("swap", {"event": "swap", "player": c.get("player"), "activated": c["name"], "from": prev[0] if prev else None, "benched": prev, "reason": a.reason.strip(),
                            "by": a.by or "gm", "floor": state["campaign"]["current_floor"], "window": win, "override_window": override or None})
    return {"ok": True, "activated": c["name"], "benched": prev}, f"{c['name']} is now the active Crawler" + (f"; benched {', '.join(prev)}" if prev else "") + " (logged in swap-log.jsonl)"


def _slug(x):
    return re.sub(r"[^a-z0-9]+", "-", str(x).lower()).strip("-")


_NOT_SHEETS = {"index.md", "character-creation-5e.md", "create-flow-spec-5e.md"}


def _name_tokens(x):
    return [t for t in re.split(r"[^a-z0-9]+", str(x).lower()) if t]


def _sheet_files(state, c, chars):
    """Sheet files in characters/ that belong to this Crawler, whatever their naming scheme: the standard <player>-<crawler>.md, else a file whose first heading is
    the Crawler's name (`# Horn (Wizard) - played by Hornn`) or ends with it (`# Moses's Crawler (Barbarian) - Bone Wifebeater`). A name that is a prefix of another
    Crawler's name (Ann / Ann Two) never claims the other's file."""
    name = c["name"]
    std = f"{_slug(c.get('player'))}-{_slug(name)}.md"
    if os.path.isfile(os.path.join(chars, std)):
        return [std]
    mine = _name_tokens(name)
    longer = [_name_tokens(x["name"]) for x in state["crawlers"] if x["name"] != name and _name_tokens(x["name"])[:len(mine)] == mine]
    found = []
    try:
        names = sorted(os.listdir(chars))
    except OSError:
        return []
    for fn in names:
        if not fn.endswith(".md") or fn.lower() in _NOT_SHEETS:
            continue
        try:
            with open(os.path.join(chars, fn), encoding="utf-8") as f:
                first = f.readline()
        except OSError:
            continue
        if not first.startswith("# "):
            continue
        toks = _name_tokens(first[2:])
        head_hit = toks[:len(mine)] == mine and not any(toks[:len(l)] == l for l in longer)
        tail_hit = False
        for m_ in re.finditer(r"[-\u2014\u2013]\s*([^()\n]+)$", first.strip()):
            tail_hit = _name_tokens(m_.group(1)) == mine
        if head_hit or tail_hit:
            found.append(fn)
    return found if len(found) == 1 else []


def _crawler_delete(a):
    """crawler delete NAME --reason T --confirm NAME [--as-player P | --as-user ID] [--by WHO] [--keep-channel] [--dry-run].
    Housekeeping only (decision 020): no penalty, no flag; it prints how many Crawlers this player deleted this floor (the GM watches for cycling)."""
    state = read_state_file()
    c = find_crawler(state, a.crawler)
    name, kind = c["name"], crawler_kind(c)
    if kind not in ("player", "pet-crawler"):
        raise StateError(f"{name} is a {kind}; only player Crawlers and pet-Crawlers can be deleted here")
    bad = _owner_check(state, c, a, "delete")
    if bad:
        raise StateError(bad)
    op, why = session_open()
    if is_active(c) and kind == "player" and op:
        raise StateError(f"REFUSED: {name} is the ACTIVE Crawler and {why}. A benched Crawler can be deleted any time; the active one only between sessions.")
    held_items = [{"name": i["name"], "qty": i.get("qty", 1)} for i in c.get("inventory", [])]
    sb = ledgers.read("story-box")
    awarded = [e for e in sb if e.get("event") == "awarded" and e.get("crawler") == name]
    released_ids = {e.get("box_id") for e in sb if e.get("event") in ("released", "reclaimed")}
    # a Story Box slot is freed unless another LIVING Crawler still holds one of its items
    others_hold = {i.get("story_box_id") for x in state["crawlers"] if x["name"] != name for i in x.get("inventory", []) if i.get("story_box_id")}
    to_release = [e for e in awarded if e["box_id"] not in released_ids and e["box_id"] not in others_hold]
    m = _channel_for(name)
    channel_shared = False
    try:
        import publisher
        cfg = publisher.load_config()
        channel_shared = any(str(v.get("channel_id")) == str(m.get("channel_id")) and publisher.norm(k) != publisher.norm(name) for k, v in cfg["crawlers"].items()) if m.get("channel_id") else False
    except Exception:
        cfg = None
    floor = state["campaign"]["current_floor"]
    prior = [e for e in ledgers.read("delete") if e.get("floor") == floor and str(e.get("player", "")).lower() == str(c.get("player", "")).lower()]
    alive = not any(x.lower() in ("dead", "deceased") for x in c.get("conditions", []))
    entry = {"event": "deleted", "crawler": name, "player": c.get("player"), "discord_user_id": (c.get("build") or {}).get("discord_user_id"), "kind": kind, "status": crawler_status(c),
             "was_active": is_active(c), "alive": alive, "session_open": op, "by": a.by or a.as_user or a.as_player or "gm", "reason": a.reason.strip(), "floor": floor,
             "credits": c.get("credits"), "items": held_items, "boxes": {t: n for t, n in (c.get("boxes") or {}).items() if n},
             "story_boxes_held": [{"box_id": e["box_id"], "box_name": e.get("box_name"), "floor": e.get("floor"), "card_ids": e.get("card_ids")} for e in awarded],
             "story_box_slots_freed": [e["box_id"] for e in to_release], "channel_id": m.get("channel_id"), "channel_name": m.get("channel_name"), "channel_shared": channel_shared,
             "player_deletes_this_floor": len(prior) + 1}
    if kind == "pet-crawler":
        entry.update(owner=c.get("owner"), pet_name=c.get("pet_name"))
    if isinstance(c.get("pet"), dict):   # a GM-run plain pet is part of the owner's record and goes with it; a biscuit pet-Crawler is a separate Crawler and is NOT cascaded
        entry["plain_pet"] = dict(c["pet"])
    summary = (f"{name} ({kind}, {entry['status']}, {'alive' if alive else 'DEAD'}), {c.get('credits')} credits, {len(held_items)} item row(s), {len(awarded)} Story Box(es) awarded"
               f"{', frees ' + str(len(to_release)) + ' Story Box slot(s)' if to_release else ''}; channel "
               f"{('#' + str(m.get('channel_name')) + (' (shared: kept)' if channel_shared else '')) if m else 'none'}; no refunds")
    if a.dry_run or not a.confirm:
        return {"ok": True, "dry_run": True, "preview": entry}, ("DRY RUN: " if a.dry_run else "NOT DELETED (add --confirm with the exact Crawler name). ") + "would delete " + summary
    if a.confirm is True or a.confirm != name:
        raise StateError(f"REFUSED: type the exact Crawler name to confirm (--confirm \"{name}\")")
    # 1. archive the ledger rows (never destroyed), then drop them from the live ledger; 2. state (backup first); 3. sheet file; 4. maps/snapshots; 5. logs; 6. Discord channel
    with FileLock(lock_path()):
        cur = read_state_file()
        # S4: everything that was checked above is checked again under the lock (a second /delete, a /join or a swap may have run in between): no double success, no double log
        c2 = next((x for x in cur["crawlers"] if x["name"] == name), None)
        if c2 is None:
            raise StateError(f"{name} is already gone (deleted by another request); nothing more to do")
        op2, why2 = session_open()
        if is_active(c2) and kind == "player" and op2:
            raise StateError(f"REFUSED: {name} is the ACTIVE Crawler and {why2}. A benched Crawler can be deleted any time; the active one only between sessions.")
        bad2 = _owner_check(cur, c2, a, "delete")
        if bad2:
            raise StateError(bad2)
        c = c2
        _backup_existing(state_path())
        rows, bad = read_ledger()
        mine_rows = [r for r in rows if r["crawler"] == name]
        arch_dir = archive_dir()
        os.makedirs(arch_dir, exist_ok=True)
        base = os.path.join(arch_dir, _slug(name))
        arch = base + "-ledger-rows.jsonl"
        have = set()   # dedupe on the FULL row (seq numbers are reused after a delete and a re-create, so seq alone would drop rows)
        if os.path.exists(arch):
            with open(arch, encoding="utf-8") as f:
                have = {json.dumps(json.loads(l), sort_keys=True) for l in f if l.strip()}
        with open(arch, "a", encoding="utf-8") as f:
            for r in mine_rows:
                if json.dumps(r, sort_keys=True) not in have:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        sc, n = f"{base}-state-{stamp}.json", 1
        while os.path.exists(sc):   # two deletes of one name in the same second must not overwrite the first state copy
            n += 1
            sc = f"{base}-state-{stamp}-{n}.json"
        with open(sc, "x", encoding="utf-8") as f:
            json.dump(c, f, indent=2, ensure_ascii=False)
        if mine_rows:
            lp = ledger_path()
            os.makedirs(backups_dir(), exist_ok=True)   # the whole credit ledger is copied before it is rewritten
            lb, n = os.path.join(backups_dir(), f"credit-ledger-{stamp}.jsonl"), 1
            while os.path.exists(lb):
                n += 1
                lb = os.path.join(backups_dir(), f"credit-ledger-{stamp}-{n}.jsonl")
            shutil.copy2(lp, lb)
            if os.path.getsize(lb) != os.path.getsize(lp):
                raise StateError("credit-ledger backup size mismatch; aborting the delete")
            tmp = lp + ".tmp"
            with open(lp, encoding="utf-8") as src, open(tmp, "w", encoding="utf-8") as dst:
                for line in src:
                    try:
                        e = json.loads(line)
                    except ValueError:
                        dst.write(line)
                        continue
                    if not (isinstance(e, dict) and e.get("crawler") == name):
                        dst.write(line)
                dst.flush()
                os.fsync(dst.fileno())
            os.replace(tmp, lp)
        cur["crawlers"] = [x for x in cur["crawlers"] if x["name"] != name]
        if kind == "player":  # the owner's pet-Crawlers stay on file, benched, until the GM rules (decision 020)
            for x in cur["crawlers"]:
                if crawler_kind(x) == "pet-crawler" and str(x.get("owner", "")).lower() == name.lower():
                    x["status"] = "benched"
        errors, _ = validate_state(cur)
        if errors:
            raise StateError("refusing to write - resulting state is invalid:\n  - " + "\n  - ".join(errors))
        cur["campaign"]["updated"] = now_iso()
        atomic_write_json(state_path(), cur)
    _RUN["wrote"] = True
    entry["ledger_rows_archived"] = len(mine_rows)
    entry["archive"] = os.path.relpath(arch, csession.campaign_dir()) if arch.startswith(csession.campaign_dir()) else arch
    for e in to_release:
        ledgers.append("story-box", {"event": "released", "box_id": e["box_id"], "crawler": name, "floor": e.get("floor"), "reason": f"Crawler deleted: {a.reason.strip()} (the deed stays closed; the floor slot is free)"})
    out = [f"deleted {summary}"] + ([f"plain pet {c['pet']['name']} ({c['pet'].get('status')}) removed with its owner (archived in the state copy)"] if isinstance(c.get("pet"), dict) else []) + [f"ledger rows archived: {len(mine_rows)} -> {entry['archive']}"]
    # sheet file (characters/<player>-<crawler>.md): moved to the archive, never destroyed, and its INDEX line dropped
    chars = csession.characters_dir()
    idx = os.path.join(chars, "INDEX.md")
    moved = []
    for fname in _sheet_files(state, c, chars):
        shutil.move(os.path.join(chars, fname), os.path.join(arch_dir, fname))
        moved.append(fname)
        if os.path.isfile(idx):
            with open(idx, encoding="utf-8") as f:
                lines = f.readlines()
            with open(idx, "w", encoding="utf-8") as f:
                f.writelines(l for l in lines if f"characters/{fname}:" not in l and f"{fname}:" not in l)
    if moved:
        out.append("sheet file " + ", ".join(moved) + " moved to the archive")
        entry["sheet_file"] = moved[0] if len(moved) == 1 else moved
    try:
        import publisher
        cfg = publisher.load_config()
        k, _m = publisher.mapping_for(cfg, name)
        if k:
            del cfg["crawlers"][k]
            publisher.save_config(cfg)
        snaps = publisher.read_json(publisher.snapshots_path(), None)
        if isinstance(snaps, dict) and name in (snaps.get("crawlers") or {}):
            del snaps["crawlers"][name]
            publisher.write_json_atomic(publisher.snapshots_path(), snaps)
        entry["channel_deleted"] = False
        if m.get("channel_id") and not channel_shared and not a.keep_channel:
            try:
                entry["channel_deleted"] = publisher.delete_crawler_channel(publisher.DiscordClient(), m["channel_id"], cfg, log=lambda t: out.append(t))
            except Exception as e:  # no token / Discord down: the rest is done; the GM can delete the channel by hand
                out.append(f"channel NOT deleted ({type(e).__name__}); delete #{m.get('channel_name')} by hand")
        elif channel_shared:
            out.append("channel is shared with another Crawler: kept")
    except Exception as e:
        out.append(f"warning: sheet-map cleanup failed ({type(e).__name__}); check player-channels.json")
    ledgers.append("delete", entry)
    out.append(f"delete count: {c.get('player')} has deleted {entry['player_deletes_this_floor']} Crawler(s) on floor {floor} (print-only; no penalty)")
    return {"ok": True, "deleted": name, "entry": entry}, "\n".join(out)


def cmd_limits(a):
    """limits show | limits set KEY VALUE (true/false/null/integer). Writes through the normal locked, validated, backed-up mutate()."""
    if a.action == "show":
        lim = {**DEFAULT_LIMITS, **read_state_file().get("limits", {})}
        return {"ok": True, "limits": lim}, "\n".join(f"{k}: {json.dumps(v)}" for k, v in lim.items())
    if a.key not in DEFAULT_LIMITS or a.value is None:
        raise StateError(f"usage: limits set KEY VALUE; KEY is one of {', '.join(DEFAULT_LIMITS)}; VALUE is true, false, null or a whole number")
    raw = a.value.strip().lower()
    val = True if raw == "true" else False if raw == "false" else None if raw == "null" else (int(raw) if re.fullmatch(r"-?\d+", raw) else (raw if a.key == "story_box_rota" and raw == "warn" else "bad"))
    if val == "bad":
        raise StateError("VALUE must be true, false, null or a whole number (story_box_rota: warn)")

    def fn(st):
        st.setdefault("limits", {})[a.key] = val
        return st, f"limits.{a.key} = {json.dumps(val)}"
    text = mutate(fn)
    return {"ok": True, "message": text}, text


def cmd_use_bypass(a):
    def fn(state):
        c = find_crawler(state, a.crawler)
        cap = state["limits"].get("bypass_per_crawler_cap")
        if cap is not None and c["bypasses_used"] >= cap:
            raise StateError(f"{c['name']} has used {c['bypasses_used']}/{cap} death bypasses (limits.bypass_per_crawler_cap)")
        c["bypasses_used"] += 1
        state["party"]["bypasses_used"] += 1
        state["party"]["bypass_log"].append({"crawler": c["name"], "kind": a.kind or "", "floor": state["campaign"]["current_floor"], "at": now_iso()})
        return state, f"{c['name']} used a death bypass{f' ({a.kind})' if a.kind else ''}; bypasses used: {c['bypasses_used']}"
    text = mutate(fn)
    return {"ok": True, "message": text}, text


def check_revive(state, crawler):
    """Raise StateError if a revive for `crawler` is not allowed under the caps."""
    lim, party, floor = state["limits"], state["party"], state["campaign"]["current_floor"]
    if crawler["revives_used"] >= lim["revive_per_crawler_cap"]:
        raise StateError(f"REFUSED: {crawler['name']} already used their {lim['revive_per_crawler_cap']} revive (per-crawler cap)")
    if party["revives_used"] >= lim["revive_campaign_cap"]:
        raise StateError(f"REFUSED: party has used {party['revives_used']}/{lim['revive_campaign_cap']} revives (campaign cap)")
    last = party["last_revive_floor"]
    if last is not None and floor - last < lim["revive_party_cooldown_floors"]:
        raise StateError(f"REFUSED: party cooldown - last revive on floor {last}; next allowed on floor {last + lim['revive_party_cooldown_floors']} (now floor {floor})")


def cmd_use_revive(a):
    def fn(state):
        c = find_crawler(state, a.crawler)
        check_revive(state, c)
        if a.dry_run:
            return state, f"OK (dry run): {c['name']} could be revived on floor {state['campaign']['current_floor']}"
        c["revives_used"] += 1
        p = state["party"]
        p["revives_used"] += 1
        p["last_revive_floor"] = state["campaign"]["current_floor"]
        p["revive_log"].append({"crawler": c["name"], "floor": p["last_revive_floor"], "note": a.note or "", "at": now_iso()})
        cap = state["limits"]["revive_campaign_cap"]
        note = ""
        return state, f"{c['name']} revived on floor {p['last_revive_floor']}. Party revives {p['revives_used']}/{cap}; crawler {c['revives_used']}/{state['limits']['revive_per_crawler_cap']}" + note
    if a.dry_run:  # read-only: no lock, no backup, no write
        state = read_state_file()
        _, text = fn(state)
        return {"ok": True, "message": text}, text
    text = mutate(fn)
    return {"ok": True, "message": text}, text


def _check_item_record(tag, rows, rec, label, seq, required_from):
    """Shared item check for floor_lost.destroyed and body_loot rows: well-formed rows, no duplicates, item_count == summed quantities, and the fingerprint (items_digest) matches.
    A row without a fingerprint passes only if it predates the first fingerprinted row of its kind (required_from)."""
    out = []
    if not all(isinstance(i, dict) and isinstance(i.get("name"), str) and i["name"].strip() and _is_int(i.get("qty")) and i["qty"] >= 1 for i in rows):
        return [f"{tag} has a malformed {label} item row (needs a name and a quantity of 1 or more)"]
    names = [i["name"].lower() for i in rows]
    if len(set(names)) != len(names):
        out.append(f"{tag} lists the same {label} item twice")
    total = sum(i["qty"] for i in rows)
    if not _is_int(rec.get("item_count")):
        if label == "destroyed" or rec.get("items_digest") is not None or (required_from is not None and _is_int(seq) and seq >= required_from):
            out.append(f"{tag} does not record item_count")
    elif rec["item_count"] != total:
        out.append(f"{tag} says item_count {rec['item_count']} but the {label} items add up to {total} (items list or count was edited)")
    dg = rec.get("items_digest")
    if dg is not None:
        if dg != _items_digest(rows):
            out.append(f"{tag}: the {label} items list does not match its recorded fingerprint (edited after it was written)")
    elif required_from is not None and _is_int(seq) and seq > required_from:
        out.append(f"{tag} has no items fingerprint (required for entries after #{required_from})")
    return out


def _verify_floor_events(entries, balances):
    """floor_lost: balance 0 and destroyed.coins == -delta (the exact coins), items listed. body_loot: each transfer_id has one from and one to row whose deltas cancel
    (coins counted once, never twice or lost) and whose item lists agree. A missing side is tolerated only when that Crawler is no longer in state.json (deleted, archived)."""
    out = []
    # Backward compatible: rows written before the item fingerprint existed stay verifiable without one. Once a digested row of a kind appears at seq S, every later row
    # of that kind must carry one too (so stripping the fingerprint from a new row is itself caught).
    req = {}
    for kind in ("floor_lost", "body_loot"):
        seqs = [e["seq"] for e in entries if e.get("event") == kind and _is_int(e.get("seq"))
                and isinstance(((e.get("destroyed") or {}) if kind == "floor_lost" else e).get("items_digest"), str)]
        req[kind] = min(seqs) if seqs else None
    for e in entries:
        if e.get("event") != "floor_lost":
            continue
        d = e.get("destroyed")
        if e["balance"] != 0:
            out.append(f"{e['crawler']}: floor_lost entry #{e.get('seq')} leaves balance {e['balance']}, not 0")
        if not (isinstance(d, dict) and _is_int(d.get("coins")) and isinstance(d.get("items"), list)):
            out.append(f"{e['crawler']}: floor_lost entry #{e.get('seq')} does not record the destroyed coins and items")
        elif d["coins"] != -e["delta"]:
            out.append(f"{e['crawler']}: floor_lost entry #{e.get('seq')} says {d['coins']} coins destroyed but the delta is {e['delta']:+d}")
        if isinstance(d, dict) and isinstance(d.get("items"), list):
            out += _check_item_record(f"{e['crawler']}: floor_lost entry #{e.get('seq')}", d["items"], d, "destroyed", e.get("seq"), req["floor_lost"])
    groups = {}
    for e in entries:
        if e.get("event") == "body_loot":
            groups.setdefault(e.get("transfer_id"), []).append(e)
    key = lambda items: sorted((i.get("name"), i.get("qty")) for i in items or [])
    for tid, rows in groups.items():
        frm, to = [r for r in rows if r.get("role") == "from"], [r for r in rows if r.get("role") == "to"]
        if len(frm) > 1 or len(to) > 1 or len(frm) + len(to) != len(rows):
            out.append(f"body_loot {tid}: expected one 'from' and one 'to' row, found {len(frm)} and {len(to)}")
            continue
        if not frm or not to:
            gone = (frm or to)[0].get("counterparty")
            if gone in balances:
                out.append(f"body_loot {tid}: the {'to' if not to else 'from'} row for {gone} is missing (credit counted once only)")
            continue
        f, t = frm[0], to[0]
        coins = f.get("coins")
        if f["delta"] + t["delta"] != 0 or f["delta"] != -coins or t["delta"] != coins or t.get("coins") != coins:
            out.append(f"body_loot {tid}: {f['crawler']} {f['delta']:+d} and {t['crawler']} {t['delta']:+d} do not match the {coins} coins looted")
        if key(f.get("items")) != key(t.get("items")):
            out.append(f"body_loot {tid}: the item lists of the two rows differ")
        for r in (f, t):
            if isinstance(r.get("items"), list):
                out += _check_item_record(f"body_loot {tid} ({r.get('role')} row, {r['crawler']}, entry #{r.get('seq')})", r["items"], r, "looted", r.get("seq"), req["body_loot"])
            else:
                out.append(f"body_loot {tid}: the {r.get('role')} row for {r['crawler']} does not list the looted items")
        if f.get("items_digest") != t.get("items_digest") or f.get("item_count") != t.get("item_count"):
            out.append(f"body_loot {tid}: the two rows disagree on item_count / items fingerprint")
    return out


def cmd_ledger(a):
    entries, bad = read_ledger()
    names = None
    if a.crawler:
        names = {a.crawler.lower()}
        try:
            names = {find_crawler(read_state_file(), a.crawler)["name"].lower()}
        except StateError:
            pass  # a crawler no longer in state may still have ledger entries
    sel = [e for e in entries if names is None or e["crawler"].lower() in names or any(n in e["crawler"].lower() for n in names)]

    if a.action == "show":
        shown = sel[-a.limit:] if a.limit else sel
        lines = []
        for e in shown:
            reason = e.get("reason", "")
            src = f" [{e['source']}]" if e.get("source") else ""
            flag = " (backfilled)" if e.get("backfill") else ""
            if e.get("event") == "floor_lost":
                flag += f" <floor lost: {(e.get('destroyed') or {}).get('coins')} coins, {(e.get('destroyed') or {}).get('item_count', 0)} item(s) destroyed>"
            elif e.get("event") == "body_loot":
                flag += f" <body loot {e.get('role')} {e.get('counterparty')}, {e.get('transfer_id')}>"
            lines.append(f"#{e.get('seq', '?'):<3} {str(e.get('ts', ''))[:16].replace('T', ' ')}  {e['crawler']:<18} {e['delta']:+5d} -> {e['balance']:<5} {reason}{src}{flag}")
        if bad:
            lines.append(f"warning: {len(bad)} unreadable ledger line(s): {bad[:10]}")
        text = "\n".join(lines) or "ledger is empty"
        return {"entries": shown, "bad_lines": bad}, text

    if a.action == "import":
        if not a.file:
            raise StateError("ledger import needs a JSON file: [{crawler, delta, reason, source?, ts?}, ...] (opening balance first)")
        refuse_secret_path(a.file)
        try:
            with open(a.file, encoding="utf-8") as f:
                items = json.load(f)
        except (OSError, ValueError) as e:
            raise StateError(f"cannot read {a.file}: {e}")
        if not isinstance(items, list) or not items:
            raise StateError("import file must be a non-empty JSON array")
        with FileLock(lock_path()):
            state = read_state_file()
            existing, _ = read_ledger()
            have = {e["crawler"].lower() for e in existing}
            running, rows = {}, []
            for i, it in enumerate(items):
                if not (isinstance(it, dict) and isinstance(it.get("crawler"), str) and _is_int(it.get("delta")) and isinstance(it.get("reason"), str) and it["reason"].strip()):
                    raise StateError(f"import item {i} needs crawler, integer delta and a reason")
                crawler = find_crawler(state, it["crawler"])["name"]
                if crawler.lower() in have:
                    raise StateError(f"{crawler} already has ledger entries; refusing to import over them (backfill is for an empty ledger)")
                running[crawler] = running.get(crawler, 0) + it["delta"]
                rows.append({"ts": it.get("ts") or now_iso(), "crawler": crawler, "delta": it["delta"], "balance": running[crawler],
                             "reason": it["reason"].strip(), "source": str(it.get("source", "")), "command": "import", "backfill": True,
                             **({"approx_ts": True} if it.get("approx_ts") else {})})
            mism = [f"{n}: ledger {b} vs state {_credit_map(state).get(n)}" for n, b in running.items() if _credit_map(state).get(n) != b]
            if mism and not a.force:
                raise StateError("imported entries do not add up to the current balances (" + "; ".join(mism) + "); fix the file, or use --force to import anyway and let `ledger verify` flag it")
            written = append_ledger(rows)
        return {"ok": True, "imported": len(written), "mismatches": mism}, f"imported {len(written)} ledger entries" + (f" (WARNING: {'; '.join(mism)})" if mism else "")

    # verify
    state = read_state_file()
    balances = _credit_map(state)
    problems = [f"unreadable ledger line {n}" for n in bad]
    per = {}
    for e in entries:
        per.setdefault(e["crawler"], []).append(e)
    for name, es in per.items():
        if names is not None and name.lower() not in {n.lower() for n in (names or [])} and not any(n in name.lower() for n in names):
            continue
        prev = 0
        for e in es:
            if e["balance"] - e["delta"] != prev:
                problems.append(f"{name}: entry #{e.get('seq')} ({e.get('reason', '')}): previous balance {e['balance'] - e['delta']} != running total {prev}")
            prev = e["balance"]
        total = sum(e["delta"] for e in es)
        if name not in balances:
            problems.append(f"{name}: has ledger entries (sum {total}) but is not in state.json")
        elif total != balances[name]:
            problems.append(f"{name}: sum of ledger entries is {total} but state.json says {balances[name]} (difference {balances[name] - total:+d})")
    # N5: the deleted-archive must be consistent too: no unreadable or duplicated rows, no repeated seq, every lifetime's balance chain adds up
    for fname, rs in archived_rows().items():
        seen_seq, seen_row, prev = set(), set(), None
        for i, r in rs:
            if not isinstance(r, dict) or not all(k in r for k in ("seq", "crawler", "delta", "balance")):
                problems.append(f"archive {fname} line {i}: unreadable or incomplete row")
                continue
            if r["seq"] in seen_seq:
                problems.append(f"archive {fname}: seq #{r['seq']} appears twice (rows from two lifetimes of one Crawler name must not share a seq)")
            seen_seq.add(r["seq"])
            key = json.dumps(r, sort_keys=True)
            if key in seen_row:
                problems.append(f"archive {fname} line {i}: exact duplicate of an earlier row")
            seen_row.add(key)
            start = r["balance"] - r["delta"]
            if prev is not None and start != prev and start != 0:
                problems.append(f"archive {fname}: entry #{r['seq']} starts from {start} but the running total is {prev}")
            prev = r["balance"]
    for name, bal in balances.items():
        if names is not None and not any(n in name.lower() for n in names):
            continue
        if name not in per and bal != 0:
            problems.append(f"{name}: state.json has {bal} credits but the ledger has no entries for them")
    problems += _verify_floor_events(entries, balances)
    ok = not problems
    lines = [f"ERROR: {p}" for p in problems]
    checked = sorted(per) if names is None else sorted(n for n in per if any(x in n.lower() for x in names))
    for e in entries:
        pv = e.get("provenance")
        if isinstance(pv, dict) and pv.get("story_box_item") and (names is None or e["crawler"].lower() in {n.lower() for n in names} or any(n in e["crawler"].lower() for n in names)):
            lines.append(f"FLAG: #{e.get('seq')} {e['crawler']} {e['delta']:+d} credits from a Story Box item ({pv.get('story_box_item')}, story value {pv.get('story_value', 0):g} is provenance only, never auto-credited): {e.get('reason', '')}")
    for e in entries:
        if e.get("event") == "floor_lost" and (names is None or any(n in e["crawler"].lower() for n in names)):
            dd = e.get("destroyed") or {}
            lines.append(f"FLOOR LOST: #{e.get('seq')} {e['crawler']} floor {e.get('floor')}: {dd.get('coins')} credits and {dd.get('item_count', 0)} item(s) destroyed, balance 0")
    lines.append(("ledger OK: " + ", ".join(f"{n} {sum(e['delta'] for e in per[n])}" for n in checked) + f" ({len(entries)} entries)") if ok else f"{len(problems)} ledger problem(s)")
    return {"ok": ok, "problems": problems, "entries": len(entries)}, "\n".join(lines)


def cmd_snapshot(a):
    with FileLock(lock_path()):
        state = read_state_file()
        errs, _ = validate_state(state)
        if errs:
            raise StateError("state is invalid; refusing to snapshot:\n  - " + "\n  - ".join(errs))
        path = os.path.join(sessions_dir(), f"state-snapshot-{dt.date.today().isoformat()}.json")
        atomic_write_json(path, state)
    return {"ok": True, "path": path}, f"snapshot written: {path}"


def refuse_secret_path(path):
    """Public commands must never read the GM-only folder (gm-notes/secret/)."""
    if path and gm_quirks.is_secret_path(path):
        raise StateError("REFUSED: that path is inside gm-notes/secret/ (GM-only); public commands never read it")


def cmd_validate(a):
    refuse_secret_path(a.file)
    state = read_state_file(a.file)
    errs, warns = validate_state(state)
    data = {"ok": not errs, "errors": errs, "warnings": warns}
    lines = [f"ERROR: {e}" for e in errs] + [f"warning: {w}" for w in warns]
    lines.append("state is valid" if not errs else f"{len(errs)} error(s)")
    return data, "\n".join(lines)


def cmd_backups(a):
    files = list_backups()
    return {"backups": files}, "\n".join(files) or "no backups yet"


def cmd_restore(a):
    path = a.backup if os.path.isabs(a.backup) or os.path.exists(a.backup) else os.path.join(backups_dir(), a.backup)
    refuse_secret_path(path)
    data = read_state_file(path)
    errs, _ = validate_state(data)
    if errs:
        raise StateError("backup is invalid:\n  - " + "\n  - ".join(errs))
    mutate(lambda cur: (data, None), allow_missing=True, allow_corrupt=True)
    return {"ok": True, "restored": path}, f"restored state from {path} (previous state was backed up)"


# --------------------------------------------------------------------------- CLI

def build_parser():
    gm_quirks.bind(globals())
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="machine-readable JSON output")
    # --reason/--source live in their own parent: gm_quirks gets only `common` (its affinity commands define their own --reason)
    ledger_args = argparse.ArgumentParser(add_help=False)
    ledger_args.add_argument("--reason", help="why credits changed (achievement name, loot box, vendor purchase, loot roll...): recorded in the credit ledger")
    ledger_args.add_argument("--benched-ok", dest="benched_ok", metavar="REASON", help="GM correction: allow credits/XP/loot/box changes on a BENCHED Crawler (sell and transfer never allow it)")
    ledger_args.add_argument("--source", help="optional ledger category, e.g. achievement | box | vendor | loot | hint")
    p = argparse.ArgumentParser(prog="state.py", description="DCC campaign live state (sessions/state.json).", parents=[common])
    sub = p.add_subparsers(dest="cmd", required=True, metavar="COMMAND")

    def add(name, fn, help_):
        sp = sub.add_parser(name, help=help_, parents=[common, ledger_args])
        sp.set_defaults(fn=fn)
        return sp

    sp = add("init", cmd_init, "create a fresh state.json")
    sp.add_argument("--floor", type=int, default=1)
    sp.add_argument("--zone", default="")
    sp.add_argument("--force", action="store_true", help="replace an existing state (old one is backed up)")

    sp = add("add-crawler", cmd_add_crawler, "add a crawler")
    sp.add_argument("name")
    sp.add_argument("--player", required=True)
    sp.add_argument("--class", dest="class_", required=True)
    sp.add_argument("--species", required=True)
    sp.add_argument("--level", type=int, default=1)
    sp.add_argument("--hp-max", type=int, default=10)
    sp.add_argument("--ac", type=int, default=10)
    sp.add_argument("--credits", type=int, default=0)
    sp.add_argument("--abilities", help="e.g. str=15,dex=14,con=13,int=10,wis=12,cha=8")

    sp = add("create-crawler", cmd_create_crawler, "add a fully built crawler from a JSON spec (Discord /create flow)")
    sp.add_argument("--file", required=True)

    add("party", cmd_party, "roster for GM tools: kinds, owners, encounter_count (players + pet-crawlers) vs party slots")

    sp = add("show", cmd_show, "show party summary, or one crawler")
    sp.add_argument("crawler", nargs="?")

    sp = add("get", cmd_get, "read a dotted path, e.g. crawlers.grimsby.hp.current")
    sp.add_argument("path")

    sp = add("set", cmd_set, "set a dotted path to a JSON value (or plain string); '-' appends to a list")
    sp.add_argument("path")
    sp.add_argument("value")

    sp = add("inventory", cmd_inventory, "inventory add|remove CRAWLER ITEM")
    sp.add_argument("action", choices=["add", "remove"])
    sp.add_argument("crawler")
    sp.add_argument("item")
    sp.add_argument("--qty", type=int, default=1)
    sp.add_argument("--all", action="store_true", help="remove: take the whole stack")
    sp.add_argument("--notes")
    sp.add_argument("--mechanics", help="add: short player-facing effect text shown on the sheet card")
    sp.add_argument("--category", choices=["weapons", "armor", "magic", "gear"], help="add: sheet card section")

    sp = add("hp", cmd_hp, "hp damage|heal|set|temp CRAWLER N")
    sp.add_argument("action", choices=["damage", "heal", "set", "temp"])
    sp.add_argument("crawler")
    sp.add_argument("amount", type=int)
    sp.add_argument("--max", type=int, help="set: also change max HP")
    sp.add_argument("--replace", action="store_true", help="temp: replace instead of keeping the higher value")

    sp = add("ledger", cmd_ledger, "credit ledger: show | verify | import FILE (sessions/credit-ledger.jsonl)")
    sp.add_argument("action", choices=["show", "verify", "import"])
    sp.add_argument("file", nargs="?", help="import: JSON array of {crawler, delta, reason, source?, ts?}")
    sp.add_argument("--crawler", help="limit to one crawler")
    sp.add_argument("--limit", type=int, default=0, help="show: only the newest N entries")
    sp.add_argument("--force", action="store_true", help="import: accept entries that do not add up to the current balances")

    sp = add("credits", cmd_credits, "credits CRAWLER +500 | -200 | =1000   (use --reason \"...\")")
    sp.add_argument("crawler")
    sp.add_argument("amount")
    sp.add_argument("--allow-debt", action="store_true")
    sp.add_argument("--floor", help="optional: record this floor (1-18) on the ledger row so `loot totals --include-credits` can place the credits")

    sp = add("achievement", cmd_achievement, "achievement add CRAWLER TITLE")
    sp.add_argument("action", choices=["add"])
    sp.add_argument("crawler")
    sp.add_argument("title")
    sp.add_argument("--note")
    sp.add_argument("--reward", help="the reward line the System read on the banner; stored with the achievement and shown on the sheet card")

    sp = add("condition", cmd_condition, "condition add|remove CRAWLER NAME")
    sp.add_argument("action", choices=["add", "remove"])
    sp.add_argument("crawler")
    sp.add_argument("condition")

    sp = add("box", cmd_box, "box earn|open|show (add|use are aliases) CRAWLER TIER [--count N] [--deed D] [--contents C]")
    sp.add_argument("action", choices=["add", "use", "earn", "open", "show"])
    sp.add_argument("crawler", nargs="?")
    sp.add_argument("tier", nargs="?")
    sp.add_argument("--count", type=int, default=1)
    sp.add_argument("--deed", help="the deed that earned the box (box ledger)")
    sp.add_argument("--box-name", help="the deed-named box, e.g. 'Tent-Pole Rescue Box'")
    sp.add_argument("--contents", help="open: what came out (item names / credits)")
    sp.add_argument("--safe-room", dest="safe_room", action="store_true", help="open: confirm the party is in a safe room (or set the scene: `scene safe-room on`); boxes cannot be opened otherwise")

    sp = add("banner", cmd_banner, "banner log TEXT | show: archive the achievement banners the System read out")
    sp.add_argument("action", choices=["log", "show"])
    sp.add_argument("text", nargs="?")
    sp.add_argument("--crawler")
    sp.add_argument("-n", type=int, default=10)

    sp = add("loot", cmd_loot, "loot draw FLOOR ZONE --crawler X [--tier T] [--pick CARD_ID] | story-box FLOOR ZONE --crawler X --pick ID[,ID] --deed TEXT | deeds | totals | show")
    sp.add_argument("action", choices=["draw", "story-box", "deeds", "totals", "show"])
    sp.add_argument("loot_floor", nargs="?", type=int)
    sp.add_argument("loot_zone", nargs="?")
    sp.add_argument("--crawler")
    sp.add_argument("--tier")
    sp.add_argument("--pull-type", dest="pull_type")
    sp.add_argument("--box-type", dest="box_type")
    sp.add_argument("--pick", help="hand-pick a card id (the only way to issue weight-0 or restricted-tier cards)")
    sp.add_argument("--deed")
    sp.add_argument("--override-cap", dest="override_cap", help="story-box: allow one more than the per-floor cap (1); the reason is logged")
    sp.add_argument("--reaward", metavar="WHY", help="story-box: re-award a deed whose earlier box was RECLAIMED (holder died with it unopened); refused if any earlier box was opened, sold or released by /delete. New box id sb-F-deed-r2")
    sp.add_argument("--deed-id", dest="deed_id", help="story-box: name this deed if it differs from the card's own deed (the registry pays each deed id once)")
    sp.add_argument("--box-name", dest="box_name", help="story-box: the deed's own box name for the banner (default: the card's box_name)")
    sp.add_argument("--shared-with", dest="shared_with", help="story-box table deed: the other contributors (A,B,C); they count as having had their Story Box on the rota")
    sp.add_argument("--open", action="store_true", help="story-box step two: open the crawler's unopened Story Box (needs --safe-room or `scene safe-room on`)")
    sp.add_argument("--box-id", dest="box_id", help="story-box --open: which unopened box (when a crawler has more than one)")
    sp.add_argument("--safe-room", dest="safe_room", action="store_true", help="draw / story-box --open: confirm the party is in a safe room; loot boxes cannot be opened otherwise")
    sp.add_argument("--witness", help="story-box: who saw it")
    sp.add_argument("--gm-note", dest="gm_note", help="story-box: GM note on how the deed was judged")
    sp.add_argument("--when", help="story-box: when it happened (default: now); free text, e.g. 'S1 20:40, tutorial'")
    sp.add_argument("--same-box-reason", dest="same_box_reason", help="story-box with --pick A,B: why the cards are one box (default: auto-recorded)")
    sp.add_argument("--dry-run", dest="dry_run", action="store_true", help="show what would be awarded and any warnings; write nothing")
    sp.add_argument("--no-publish", dest="no_publish", action="store_true", help="story-box: do not refresh the player's channel card")
    sp.add_argument("--floor", dest="totals_floor", type=int, help="totals: only this floor")
    sp.add_argument("--include-credits", dest="include_credits", action="store_true", help="totals: ALSO show the all-in view (boxes + Story Box sale proceeds + credits earned from encounters/R1 toasts) and the optional Floor 2 valve check (budget A12). Off by default; the normal totals are unchanged")
    sp.add_argument("--credit-sources", dest="credit_sources", help="totals --include-credits: comma list of credit-ledger sources that count as earned credits (default encounter,achievement,toast,r1; box is never counted twice)")
    sp.add_argument("--assume-floor", dest="assume_floor", help="totals --include-credits: floor (1-18) for earned credits whose ledger entry has no floor recorded (default: shown as 'floor not recorded')")
    sp.add_argument("-n", type=int, default=10)

    sp = add("sell", cmd_sell, "sell CRAWLER ITEM --reason TEXT [--qty N] [--price N] [--floor N]: credits via the ledger; Story Box items sell to the System at sale_value x floor multiplier")
    sp.add_argument("crawler")
    sp.add_argument("item")
    sp.add_argument("--qty", type=int, default=1)
    sp.add_argument("--price", type=int, help="total credits (GM-set; required for items without a sale_value)")
    sp.add_argument("--floor", type=int, help="floor of the sale (default: current floor); sets the multiplier")
    sp.add_argument("--dry-run", dest="dry_run", action="store_true")

    sp = add("transfer", cmd_transfer, "transfer FROM TO ITEM --reason TEXT [--qty N] [--price N]: gift, trade or loot from a corpse; --price is a free-form credit payment from TO to FROM")
    sp.add_argument("frm", metavar="FROM")
    sp.add_argument("to", metavar="TO")
    sp.add_argument("item")
    sp.add_argument("--qty", type=int, default=1)
    sp.add_argument("--price", type=int)
    sp.add_argument("--allow-debt", dest="allow_debt", action="store_true")
    sp.add_argument("--dry-run", dest="dry_run", action="store_true")

    sp = add("floor-lost", cmd_floor_lost, "floor-lost CRAWLER --reason TEXT [--floor N] [--mark-dead] [--dry-run]: decision 028 write-off of a dead Crawler's credits and items (one append-only ledger entry)")
    sp.add_argument("crawler")
    sp.add_argument("--floor", help="the floor that was lost, 1 to 18 (default: the current floor)")
    sp.add_argument("--mark-dead", dest="mark_dead", action="store_true", help="add the Dead condition in the same step (otherwise the Crawler must already be dead)")
    sp.add_argument("--dry-run", dest="dry_run", action="store_true")

    sp = add("loot-body", cmd_loot_body, "loot-body DEAD SURVIVOR --reason TEXT [--coins N|all] [--item NAME[=QTY]]... [--all-items]: take coins/items from a body before the collapse (decision 028); two linked ledger rows")
    sp.add_argument("frm", metavar="DEAD")
    sp.add_argument("to", metavar="SURVIVOR")
    sp.add_argument("--coins", help="whole credits to take, or 'all'")
    sp.add_argument("--item", action="append", help="item name, or NAME=QTY (repeatable)")
    sp.add_argument("--all-items", dest="all_items", action="store_true")
    sp.add_argument("--floor", help="floor of the loot, 1 to 18 (default: the current floor)")
    sp.add_argument("--dry-run", dest="dry_run", action="store_true")

    sp = add("scene", cmd_scene, "scene safe-room on|off|show: the session flag that lets loot boxes be opened")
    sp.add_argument("topic", choices=["safe-room", "show"])
    sp.add_argument("value", nargs="?", choices=["on", "off"])
    sp.add_argument("--note")

    sp = add("session-status", cmd_session_status, "session-status open|close|show: is a play session open? (blocks Crawler swaps and deleting the active Crawler)")
    sp.add_argument("action", choices=["open", "close", "show"])
    sp.add_argument("--note")
    sp.add_argument("--by")
    sp.add_argument("--fresh", action="store_true", help="open: start a NEW swap window even if the last close was under 30 minutes ago")

    sp = add("crawler", cmd_crawler, "crawler list|activate|migrate|delete: active/benched Crawlers, swaps between sessions, deletion")
    sp.add_argument("action", choices=["list", "activate", "request", "requests", "migrate", "delete"])
    sp.add_argument("crawler", nargs="?")
    sp.add_argument("--player", help="list: one human's Crawlers (by player name)")
    sp.add_argument("--user-id", dest="user_id", help="list: one human's Crawlers (by Discord user id)")
    sp.add_argument("--by", help="who asked (logged in the swap/delete log)")
    sp.add_argument("--as-player", dest="as_player", help="delete: the caller's player name; refuses Crawlers that are not theirs")
    sp.add_argument("--as-user", dest="as_user", help="delete: the caller's Discord user id; refuses Crawlers that are not theirs")
    sp.add_argument("--confirm", nargs="?", const=True, metavar="NAME", help="delete: really delete; NAME must be the exact Crawler name (typed confirm). Without it, only a preview")
    sp.add_argument("--override-window", dest="override_window", metavar="WHY", help="activate: GM allows a second swap in the same between-session window")
    sp.add_argument("--keep-channel", dest="keep_channel", action="store_true", help="delete: do not delete the Crawler's Discord text channel")
    sp.add_argument("--dry-run", dest="dry_run", action="store_true")

    sp = add("pet", cmd_pet, "GM-run plain pet (decision 022): pet add OWNER --species S --name N [--cr 1/4] | show [OWNER] | kill OWNER --reason T | shop OWNER ITEM --reason T [--sell]")
    sp.add_argument("action", choices=["add", "show", "kill", "mark-dead", "remove", "convert", "shop", "heal"])
    sp.add_argument("owner", nargs="?")
    sp.add_argument("item", nargs="?", help="shop: heal-critter-potion | pet-carrier (omit for the price list)")
    sp.add_argument("--species", help="add: an SRD Beast of CR 1/4 or lower (tables/pet-species.json; dog/rottweiler = mastiff)")
    sp.add_argument("--name")
    sp.add_argument("--cr", help="add: Challenge Rating, 1/4 or lower (default: the species' CR)")
    sp.add_argument("--description", help="add: free text, max 300 chars")
    sp.add_argument("--notes", help="add: alias of --description")
    sp.add_argument("--quote", help="add: the player's own words from the questionnaire (audit)")
    sp.add_argument("--override", help="GM ruling, logged: species off the list / CR above 1/4 (add), or no living pet (shop)")
    sp.add_argument("--file", help="convert: the pet-Crawler spec JSON (same as create-crawler)")
    sp.add_argument("--qty", type=int)
    sp.add_argument("--floor", type=int, help="shop: floor of the sale (default: current floor); sets the multiplier")
    sp.add_argument("--sell", action="store_true", help="shop: half-price buyback")
    sp.add_argument("--by", help="who filed it (default gm)")
    sp.add_argument("--dry-run", dest="dry_run", action="store_true")

    sp = add("limits", cmd_limits, "limits show | limits set KEY VALUE (party caps, Story Box switch and cap)")
    sp.add_argument("action", choices=["show", "set"])
    sp.add_argument("key", nargs="?")
    sp.add_argument("value", nargs="?")

    sp = add("use-bypass", cmd_use_bypass, "record an earned death bypass (not a revive)")
    sp.add_argument("crawler")
    sp.add_argument("--kind", help="e.g. cockroach, lifesaver-draught")

    sp = add("use-revive", cmd_use_revive, "record a revive; refuses past the caps")
    sp.add_argument("crawler")
    sp.add_argument("--dry-run", action="store_true", help="only check whether it is allowed")
    sp.add_argument("--note")

    add("snapshot", cmd_snapshot, "write sessions/state-snapshot-YYYY-MM-DD.json")
    sp = add("validate", cmd_validate, "check state.json against the schema")
    sp.add_argument("--file", help="validate another file")
    add("backups", cmd_backups, "list state backups (newest last)")
    sp = add("restore", cmd_restore, "restore a backup file (name in sessions/backups/ or a path)")
    sp.add_argument("backup")

    repair_log.add_parsers(sub, common)
    gm_quirks.add_parsers(sub, common)  # gm-quirks ..., affinity ..., show-gm (GM-only; see tools/README.md)
    return p


def auto_publish():
    """Best-effort, non-blocking: after a state change, start a detached `publisher.py --auto` that posts updated cards
    to the players' channels. Never raises and never delays or fails the state change (Discord down = silently retried
    by the next publish). Off when DCC_AUTO_PUBLISH=0, when GM_DISCORD_TOKEN is unset, or when no channel is registered."""
    try:
        if os.environ.get("DCC_AUTO_PUBLISH", "1") == "0" or not os.environ.get("GM_DISCORD_TOKEN"):
            return False
        cfg_path = os.environ.get("PLAYER_CHANNELS_FILE") or os.path.join(os.path.dirname(state_path()), "player-channels.json")
        with open(cfg_path, encoding="utf-8") as f:
            if not any(m.get("channel_id") for m in json.load(f).get("crawlers", {}).values()):
                return False
        import subprocess
        log = open(os.path.join(os.path.dirname(state_path()), "publish.log"), "a")
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "publisher.py"), "--auto"],
                         stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True, close_fds=True)
        log.close()
        return True
    except Exception:
        return False


def main(argv=None):
    try:
        argv = csession.apply_cli_session(argv)
    except csession.SessionError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    args = build_parser().parse_args(argv)
    _RUN.update(reason=getattr(args, "reason", None), source=getattr(args, "source", None) or "", command=args.cmd, row_extra=None, force_rows=None)
    if getattr(args, "amount", None) is not None and args.cmd == "hp" and args.action != "set" and args.amount < 0:
        print("ERROR: amount must be >= 0", file=sys.stderr)
        return 1
    try:
        data, text = args.fn(args)
    except (StateError, gm_quirks.GMError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"ERROR: file system problem: {e}", file=sys.stderr)
        return 1
    print(json.dumps(data, indent=2, ensure_ascii=False) if args.json else text)
    if _RUN.get("wrote"):
        auto_publish()
    if (args.cmd == "validate" or (args.cmd == "ledger" and args.action == "verify")) and not data["ok"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
