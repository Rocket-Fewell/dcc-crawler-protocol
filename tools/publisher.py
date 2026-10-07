#!/usr/bin/env python3
"""publisher.py - posts each crawler's FULL state card to that player's own Discord text channel.

State files stay the source of truth (sessions/state.json, sessions/credit-ledger.jsonl, exports/card-data.json);
this module only READS them and posts. It is driven by `python3 tools/discord_gm.py publish|setup-channels|
register-channel|channels` and (best-effort, in the background) by state.py after every successful change.

* One NEW post per change (never edits): the full card, split across messages of < 2000 chars.
* Line 1 of every card: `Credits: <total> (<last change>, <reason>)`. The last change comes from the credit ledger when its
  last entry matches the current balance, else from the diff against the last published snapshot.
* Snapshots: sessions/published-snapshots.json (what was last posted, per crawler). No diff and no --full = nothing posted.
* Channel map: sessions/player-channels.json  (crawler -> channel id). Cards only go to mapped channels.
* Never reads gm-notes/ and never prints the bot token. Player channels are NOT the voice channel (#gm-voice, formerly #dcc_mouth) and NOT
  the transcript channel (#table-transcript, formerly #dcc_ears), so the bridge neither speaks nor wakes the GM for them.
"""
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request

API = "https://discord.com/api/v10"
MSG_LIMIT = 1900          # Discord's hard limit is 2000; keep headroom
import dcc_paths as _paths  # noqa: E402
DEFAULT_CAMPAIGN_DIR = _paths.CAMPAIGN_ROOT

# Permission bits
P_ADMIN, P_MANAGE_CHANNELS = 1 << 3, 1 << 4
P_ADD_REACTIONS, P_VIEW, P_SEND, P_EMBED, P_HISTORY = 1 << 6, 1 << 10, 1 << 11, 1 << 14, 1 << 16
BOT_ALLOW = P_VIEW | P_SEND | P_EMBED | P_HISTORY
EVERYONE_ALLOW = P_VIEW | P_HISTORY
EVERYONE_DENY = P_SEND | P_ADD_REACTIONS


class PublishError(Exception):
    pass


class DiscordError(Exception):
    def __init__(self, status, message=""):
        super().__init__(f"Discord HTTP {status}" + (f": {message}" if message else ""))
        self.status = status


# --------------------------------------------------------------------------- paths

def campaign_dir():
    return str(_paths.campaign_root())


def sessions_dir():
    """This session's data dir (alpha: <campaign>/sessions, others: <campaign>/sessions-data/<id>)."""
    import campaign_session
    return campaign_session.data_dir()


def session_config():
    """Non-secret per-session settings from <data>/session.json ({} for alpha or when absent)."""
    import campaign_session
    try:
        return read_json(campaign_session.session_file(), {}) or {}
    except PublishError:
        return {}


def state_path():
    return os.path.join(sessions_dir(), "state.json")


def channels_path():
    return os.environ.get("PLAYER_CHANNELS_FILE") or os.path.join(sessions_dir(), "player-channels.json")


def snapshots_path():
    return os.path.join(sessions_dir(), "published-snapshots.json")


def ledger_path():
    return os.path.join(sessions_dir(), "credit-ledger.jsonl")


def card_data_path():
    return os.path.join(campaign_dir(), "exports", "card-data.json")


def session_card_data_path():
    import campaign_session
    return None if campaign_session.is_alpha() else os.path.join(sessions_dir(), "card-data.json")


def now_iso():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


# --------------------------------------------------------------------------- json files

def read_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except (OSError, ValueError) as e:
        raise PublishError(f"cannot read {path}: {e}")


def write_json_atomic(path, data):
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


class PublishLock:
    """Serialises publishers so rapid state changes cannot post the same card twice."""

    def __init__(self, timeout=90.0):
        self.timeout = timeout
        self.fh = None

    def __enter__(self):
        os.makedirs(sessions_dir(), exist_ok=True)
        self.fh = open(os.path.join(sessions_dir(), ".publish.lock"), "a")
        end = time.time() + self.timeout
        while True:
            try:
                fcntl.flock(self.fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except OSError:
                if time.time() > end:
                    raise PublishError("another publish is running (lock timeout)")
                time.sleep(0.1)

    def __exit__(self, *exc):
        try:
            fcntl.flock(self.fh, fcntl.LOCK_UN)
        finally:
            self.fh.close()
        return False


# --------------------------------------------------------------------------- Discord client

class DiscordClient:
    """Minimal Discord REST client for the GM bot. The token comes from $GM_DISCORD_TOKEN and is never printed."""

    def __init__(self, token=None):
        self.token = token or os.environ.get("GM_DISCORD_TOKEN")
        if not self.token:
            raise PublishError("GM_DISCORD_TOKEN is not set")

    def request(self, method, path, body=None, _retried=False):
        req = urllib.request.Request(
            API + path, method=method, data=json.dumps(body).encode() if body is not None else None,
            headers={"Authorization": f"Bot {self.token}", "Content-Type": "application/json", "User-Agent": "DCC-GM (local, 1.0)"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                raw = r.read()
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", "replace")
            if e.code == 429 and not _retried:
                try:
                    wait = float(json.loads(text).get("retry_after", 1))
                except (ValueError, AttributeError):
                    wait = 1.0
                time.sleep(min(wait, 10))
                return self.request(method, path, body, _retried=True)
            msg = ""
            try:
                j = json.loads(text)
                msg = f"{j.get('message', '')} (code {j.get('code', '?')})"
            except ValueError:
                pass
            raise DiscordError(e.code, msg)
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise DiscordError(0, f"network error {type(e).__name__}")


# --------------------------------------------------------------------------- name matching / config

def norm(s):
    return re.sub(r"\s+", " ", str(s or "").strip().lower())


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", norm(s)).strip("-") or "player"


def load_config():
    import campaign_session
    cat = campaign_session.sheet_category_name()
    cfg = read_json(channels_path(), None)
    if cfg is None:
        cfg = {"guild_id": "", "category_name": cat, "category_id": "", "crawlers": {}}
    cfg.setdefault("guild_id", "")
    cfg.setdefault("category_name", cat)  # non-alpha defaults to "Crawler Sheets (<id>)" so sheets never share alpha's category
    cfg.setdefault("category_id", "")
    cfg.setdefault("crawlers", {})
    return cfg


def save_config(cfg):
    write_json_atomic(channels_path(), cfg)


def resolve_crawler(name, state, cfg):
    """Accept a crawler name, a unique partial name, or a player alias; return the crawler dict from state."""
    low = norm(name)
    crawlers = state.get("crawlers", [])
    for c in crawlers:
        if norm(c["name"]) == low:
            return c
    # a player name (or alias) picks that player's Crawler only when it is unambiguous: players can have several Crawlers
    by_player = [c for c in crawlers if norm(c.get("player")) == low]
    for key, m in cfg.get("crawlers", {}).items():
        if low in [norm(p) for p in m.get("players", [])]:
            by_player += [c for c in crawlers if norm(c["name"]) == norm(key) and c not in by_player]
    if len(by_player) == 1:
        return by_player[0]
    if len(by_player) > 1:
        raise PublishError(f"'{name}' has several Crawlers ({', '.join(c['name'] for c in by_player)}): name the Crawler")
    part = [c for c in crawlers if low in norm(c["name"]) or low in norm(c.get("player"))]
    if len(part) == 1:
        return part[0]
    raise PublishError(f"no unique crawler matches '{name}' (have: {', '.join(c['name'] for c in crawlers) or 'none'})")


def mapping_for(cfg, crawler_name):
    for key, m in cfg.get("crawlers", {}).items():
        if norm(key) == norm(crawler_name):
            return key, m
    return None, None


# --------------------------------------------------------------------------- card data / ledger

def load_card_data():
    """Shared item catalog (exports/card-data.json) overlaid with this session's own <data>/card-data.json (non-alpha)."""
    data = read_json(card_data_path(), {}) or {}
    extra = session_card_data_path()
    if extra:
        own = read_json(extra, {}) or {}
        data = {**data, "items": {**(data.get("items") or {}), **(own.get("items") or {})}, "crawlers": dict(own.get("crawlers") or {})}
    return data


def read_ledger(path=None):
    out = []
    try:
        with open(path or ledger_path(), encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                    if isinstance(e, dict) and isinstance(e.get("crawler"), str):
                        out.append(e)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return out


def signed(n):
    return f"{n:+d}"


def last_credit_change(crawler, ledger, old_view):
    """(delta, reason) of the most recent credit change, or None."""
    mine = [e for e in ledger if norm(e["crawler"]) == norm(crawler["name"])]
    if mine and mine[-1].get("balance") == crawler["credits"]:
        e = mine[-1]
        reason = e.get("reason", "")
        return e["delta"], ("" if reason == "unspecified" else reason)
    if old_view is not None and old_view.get("credits") != crawler["credits"]:
        return crawler["credits"] - old_view["credits"], ""
    return None


# --------------------------------------------------------------------------- views, diff

def item_info(item, data):
    meta = (data.get("items") or {}).get(norm(item["name"])) or {}
    mech = item.get("mechanics") or meta.get("mechanics") or ""
    if not mech and item.get("notes"):
        mech = item["notes"]
    return {"category": item.get("category") or meta.get("category") or "gear", "mechanics": mech}


def _notes_sig(notes):
    """Short fingerprint of an item's GM notes: lets a notes-only edit count as a change without copying the note text into the view/snapshot."""
    text = str(notes or "").strip()
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12] if text else ""


def _status(c):
    """active|benched for player Crawlers and pet-Crawlers; None for plain pets and companions (state.py crawler_status)."""
    if (c.get("kind") or "player") not in ("player", "pet-crawler"):
        return None
    return "benched" if c.get("status") == "benched" else "active"


PET_ITEM_IDS = ("heal-critter-potion", "pet-carrier")


def make_view(c, data):
    """The player-visible slice of a crawler. Nothing else (fan_profile, notes, ...) can ever reach Discord."""
    inv = []
    has_pet = bool(pet_public(c, data))
    for it in c.get("inventory", []):
        if not has_pet and (it.get("srd_id") in PET_ITEM_IDS):   # a leftover pet item stays on file but is not shown without a living pet (or with pets off)
            continue
        info = item_info(it, data)
        inv.append({"name": it["name"], "qty": it.get("qty", 1), "uses": it.get("uses"), "uses_max": it.get("uses_max"),
                    "uses_reset": it.get("uses_reset"), "category": info["category"], "mechanics": info["mechanics"],
                    "notes_sig": _notes_sig(it.get("notes"))})
    extras = (data.get("crawlers") or {}).get(c["name"], {})
    return {
        "name": c["name"], "player": c.get("player", ""), "status": _status(c), "class": c.get("class", ""), "species": c.get("species", ""),
        "level": c.get("level"), "xp": c.get("xp"), "hp": dict(c["hp"]), "ac": c.get("ac"), "hit_dice": dict(c.get("hit_dice", {})),
        "abilities": dict(c.get("abilities", {})), "credits": c.get("credits"),
        "conditions": list(c.get("conditions", [])),
        "boxes": {t: n for t, n in (c.get("boxes") or {}).items() if n},
        "death_saves": dict(c["death_saves"]) if isinstance(c.get("death_saves"), dict) else None,
        "inventory": inv,
        "achievements": [a["name"] for a in c.get("achievements", []) if isinstance(a, dict) and a.get("name")],
        "achievement_text": {a["name"]: str(a["reward"]) for a in c.get("achievements", []) if isinstance(a, dict) and a.get("name") and a.get("reward")},
        "standing_orders": c.get("standing_orders") or extras.get("standing_orders") or "",
        "standing_reaction": c.get("standing_reaction") or extras.get("standing_reaction") or "",
        "signature": c.get("signature") or extras.get("signature") or "",
        "build": build_public(c.get("build")),
        "pet": pet_public(c, data),
    }


def _pet_stats(srd_id):
    """Public SRD stat fields for a pet species from tables/pet-species.json (ac, hp, attacks). Missing or empty values stay out ({} / None)."""
    try:
        with open(os.path.join(campaign_dir(), "tables", "pet-species.json"), encoding="utf-8") as f:
            table = json.load(f)
    except (OSError, ValueError):
        return {}
    return next((e for e in table.get("species", []) if isinstance(e, dict) and e.get("id") == srd_id), None) or {}


def _pet_kind(pet):
    """What the pet IS on the sheet: pet.kind (e.g. 'raccoon' on a Cat stat block), else its species, lower case."""
    return str(pet.get("kind") or pet.get("species") or "pet").strip().lower()


def _pet_display_name(pet):
    """'unnamed <kind>' for a pet the player has not named yet (pet.unnamed, no name, or the GM placeholder '<Species> (unnamed)')."""
    name = str(pet.get("name") or "").strip()
    if pet.get("unnamed") is True or not name or re.search(r"\(unnamed\)\s*$", name, re.I):
        return f"unnamed {_pet_kind(pet)}"
    return name


def _int_or_none(v):
    return v if isinstance(v, int) and not isinstance(v, bool) else None


def pet_public(c, data):
    """The owner's plain pet (decision 022), only while it is alive and pets are enabled; None otherwise, so nothing about pets shows on a sheet without one.
    PUBLIC fields only: display name, kind, species, CR, HP current/max, AC and up to two attacks (pet record first, then the species table).
    Never description, quote, filed_by or any other GM note. A field with no value is left out (the card then shows less, never '?')."""
    pet = c.get("pet")
    if not isinstance(pet, dict) or pet.get("status") != "alive" or not (data or {}).get("pets_enabled", True):
        return None
    cr = pet.get("cr")
    crt = {0: "0", 0.125: "1/8", 0.25: "1/4"}.get(cr, str(cr))
    st = _pet_stats(pet.get("species_srd_id"))
    out = {"name": _pet_display_name(pet), "species": str(pet.get("species", "")), "kind": _pet_kind(pet), "cr": crt}
    hp_max = _int_or_none(pet.get("hp_max")) if pet.get("hp_max") is not None else _int_or_none(st.get("hp"))
    hp_cur = _int_or_none(pet.get("hp_current"))
    if hp_cur is None and hp_max is not None:
        hp_cur = hp_max
    if hp_cur is not None:
        out["hp_current"] = hp_cur
    if hp_max is not None:
        out["hp_max"] = hp_max
    ac = _int_or_none(pet.get("ac")) if pet.get("ac") is not None else _int_or_none(st.get("ac"))
    if ac is not None:
        out["ac"] = ac
    attacks = []
    for a in (pet.get("attacks") or st.get("attacks") or [])[:2]:
        if isinstance(a, dict) and str(a.get("name") or "").strip():
            row = {"name": str(a["name"]).strip(), "damage": str(a.get("damage") or "").strip()}
            if _int_or_none(a.get("to_hit")) is not None:
                row["to_hit"] = a["to_hit"]
            attacks.append(row)
    if attacks:
        out["attacks"] = attacks
    return out


def pet_block(p):
    """Short pet block for the owner's card: a header line (name, kind, stat block if reskinned, CR), then HP/AC and attacks only when known."""
    kind = p.get("kind") or p.get("species", "").lower()
    reskin = f", {p['species']} stat block" if p.get("species") and p["species"].lower() != kind else ""
    lines = [f"**Pet (GM-run): {p['name']}** - {kind}{reskin} (CR {p['cr']})"]
    stats = []
    if p.get("hp_current") is not None:
        stats.append(f"HP {p['hp_current']}/{p['hp_max']}" if p.get("hp_max") is not None else f"HP {p['hp_current']}")
    if p.get("ac") is not None:
        stats.append(f"AC {p['ac']}")
    if stats:
        lines.append("  ".join(stats))
    for a in p.get("attacks") or []:
        th = f" {int(a['to_hit']):+d} to hit," if a.get("to_hit") is not None else ""
        dmg = a.get("damage") or ""
        lines.append(f"{a['name']}:{th} {dmg}".rstrip(" ,") if (th or dmg) else a["name"])
    return "\n".join(lines)


def _join(x):
    return ", ".join(str(i) for i in x) if isinstance(x, list) else str(x)


def build_public(b):
    """Player-visible BUILD lines from a crawler's build{} (whitelist: never survey, opt-outs, rolls or notes)."""
    if not isinstance(b, dict):
        return []
    out = []
    feats = [f for f in (b.get("origin_feat"), b.get("extra_origin_feat")) if f]
    cc = b.get("class_choices") if isinstance(b.get("class_choices"), dict) else {}
    pairs = [("Origin feat", feats), ("Class picks", [v for k, v in cc.items() if k not in ("masteries", "expertise") and v]),
             ("Skills", b.get("skills")), ("Expertise", b.get("expertise") or cc.get("expertise")), ("Tools", b.get("tools")),
             ("Weapon mastery", b.get("weapon_masteries")), ("Languages", b.get("languages"))]
    for label, val in pairs:
        if val:
            out.append(f"{label}: {_join(val)}")
    sp = b.get("spells") if isinstance(b.get("spells"), dict) else {}
    for label, key in (("Cantrips", "cantrips"), ("Prepared", "prepared"), ("Spellbook", "spellbook")):
        if sp.get(key):
            out.append(f"{label}: {_join(sp[key])}")
    return out


def _hp(v):
    t = f" (+{v['hp']['temp']} temp)" if v["hp"].get("temp") else ""
    return f"{v['hp']['current']}/{v['hp']['max']}{t}"


def diff_views(old, new):
    """Short human-readable list of what changed since the last published view ([] = nothing visible changed)."""
    if old is None:
        return []
    ch = []
    if old["hp"] != new["hp"]:
        ch.append(f"HP {_hp(old)} -> {_hp(new)}")
    if (old.get("status") or "active") != (new.get("status") or "active"):
        ch.append(f"Status: {(new.get('status') or 'active').upper()}")
    for key, label in (("credits", "Credits"), ("ac", "AC"), ("level", "Level"), ("xp", "XP")):
        if old.get(key) != new.get(key):
            ch.append(f"{label} {old.get(key)} -> {new.get(key)}")
    if old.get("pet") != new.get("pet"):
        ch.append(f"Pet: {new['pet']['name']}" if new.get("pet") else f"Pet: -{(old.get('pet') or {}).get('name', '')}")
    if old.get("hit_dice") != new.get("hit_dice"):
        ch.append(f"Hit Dice {old['hit_dice'].get('current')}/{old['hit_dice'].get('max')} -> {new['hit_dice'].get('current')}/{new['hit_dice'].get('max')}")
    for a, v in new["abilities"].items():
        if old["abilities"].get(a) != v:
            ch.append(f"{a.upper()} {old['abilities'].get(a)} -> {v}")
    for cond in new["conditions"]:
        if cond not in old["conditions"]:
            ch.append(f"Condition: +{cond}")
    for cond in old["conditions"]:
        if cond not in new["conditions"]:
            ch.append(f"Condition: -{cond}")
    if old.get("death_saves") != new.get("death_saves"):
        d = new.get("death_saves") or {}
        ch.append(f"Death saves {d.get('successes', 0)} successes / {d.get('fails', 0)} fails")
    if old["boxes"] != new["boxes"]:
        ch.append("Boxes: " + (", ".join(f"{t} {n}" for t, n in new["boxes"].items()) or "none"))
    oi, ni = _keyed_items(old["inventory"]), _keyed_items(new["inventory"])
    for k, i in ni.items():
        label = _item_label(k)
        if k not in oi:
            ch.append(f"+ {label}" + (f" x{i['qty']}" if i["qty"] > 1 else ""))
            continue
        parts = _item_changes(oi[k], i)
        if parts:
            ch.append(f"{label}: " + ", ".join(parts))
    for k in oi:
        if k not in ni:
            ch.append(f"- {_item_label(k)}")
    for a in new["achievements"]:
        if a not in old["achievements"]:
            ch.append(f"Achievement: {a}")
    if not ch and views_differ(old, new):
        ch.append("Sheet details updated")   # safety net: a visible field changed that has no line of its own above
    return ch


def _keyed_items(items):
    """(name, n) -> item, so two stacks with the same name are compared one-to-one instead of collapsing into one."""
    out, seen = {}, {}
    for i in items:
        n = seen.get(i["name"], 0)
        seen[i["name"]] = n + 1
        out[(i["name"], n)] = i
    return out


def _item_label(key):
    name, n = key
    return name if n == 0 else f"{name} #{n + 1}"


def _differs(a, b, k):
    """A field counts as changed only when both views carry it: a snapshot written before the field existed never forces a repost."""
    return k in a and k in b and a[k] != b[k]


def _item_changes(o, i):
    """Every visible change to one inventory row: qty, uses (count, max, reset), mechanics text, notes, sheet section."""
    parts = []
    if _differs(o, i, "qty"):
        parts.append(f"x{o['qty']} -> x{i['qty']}")
    if any(_differs(o, i, k) for k in ("uses_max", "uses_reset")):
        parts.append(f"uses {uses_text(o) or 'none'} -> {uses_text(i) or 'none'}")
    elif _differs(o, i, "uses"):
        parts.append(f"uses {o.get('uses')} -> {i.get('uses')}")
    if _differs(o, i, "mechanics"):
        parts.append("mechanics updated")
    if _differs(o, i, "notes_sig"):
        parts.append("notes updated")
    if _differs(o, i, "category"):
        parts.append(f"moved to {i['category']}")
    return parts


def views_differ(old, new):
    """True when any player-visible field differs. Keys missing from the older view (written before the key existed) are skipped,
    including per-item keys, so adding a view field never reposts every card by itself."""
    if old is None:
        return True
    for k in set(old) & set(new):
        if k == "inventory":
            oi, ni = _keyed_items(old[k]), _keyed_items(new[k])
            if set(oi) != set(ni) or any(_differs(oi[x], ni[x], f) for x in ni for f in set(oi[x]) | set(ni[x])):
                return True
        elif k == "status":
            if (old[k] or "active") != (new[k] or "active"):   # a snapshot from before status existed reads as active
                return True
        elif k == "conditions":
            if sorted(map(str, old[k] or [])) != sorted(map(str, new[k] or [])):
                return True
        elif old[k] != new[k]:
            return True
    return False


# --------------------------------------------------------------------------- rendering

def credits_line(c, change):
    line = f"Credits: {c['credits']}"
    if change:
        delta, reason = change
        line += f" ({signed(delta)}{', ' + reason if reason else ''})"
    return line


def achievement_rewards(v, ledger):
    """achievement name -> credit reward (+25) when the ledger has an entry that names it."""
    out = {}
    mine = [e for e in ledger if norm(e["crawler"]) == norm(v["name"]) and e.get("delta", 0) > 0]
    for a in v["achievements"]:
        for e in mine:
            if norm(a) and norm(a) in norm(e.get("reason", "")):
                out[a] = e["delta"]
                break
    return out


USES_RESET_LABELS = {"session": "per session", "short_rest": "per short rest", "long_rest": "per long rest", "day": "per day",
                     "floor": "per floor", "never": "one-time, does not reset"}


def _reset_key(r):
    return re.sub(r"[\s-]+", "_", str(r or "").strip().lower())


def uses_text(i):
    """'1/1 per session' when the item tracks resetting uses (uses_reset set), '9/10' for plain uses/uses_max, '' when it tracks none."""
    if i.get("uses") is None or not i.get("uses_max"):
        return ""
    base = f"{i['uses']}/{i['uses_max']}"
    r = i.get("uses_reset")
    if not r:
        return base
    label = USES_RESET_LABELS.get(_reset_key(r)) or f"resets: {r}"
    return f"{base} {label}" if label.startswith("per ") else f"{base}, {label}"


def item_line(i):
    qty = f" x{i['qty']}" if i["qty"] > 1 else ""
    if i.get("uses_reset") and uses_text(i):
        uses = f" [Uses: {uses_text(i)}]"   # optional per-session/rest tracking (uses_reset); items without it render exactly as before
    else:
        uses = f" [{i['uses']}/{i['uses_max']} uses]" if i.get("uses") is not None and i.get("uses_max") else ""
    mech = f": {i['mechanics']}" if i["mechanics"] else ": (no mechanics on file - ask the GM)"
    return f"- **{i['name']}**{qty}{uses}{mech}"


def _species_class_label(v):
    """'Our Species (Human) Our Class (Wizard)' from tables/species-class-reskins.json (Lore's combined_label); the plain 5e names when the approved table is not in place,
    the session does not set create.species_class_reskin true, or anything fails (state keeps the 5e names)."""
    plain = f"{v['species']} {v['class']}"
    try:
        if (session_config().get("create") or {}).get("species_class_reskin") is not True:
            return plain   # OFF unless the session says true (names not approved by Caleb yet)
        here = os.path.dirname(os.path.abspath(__file__))
        if here not in sys.path:
            sys.path.insert(0, here)
        import species_class_reskins as scr
        return f"{scr.species_label(v['species'])} {scr.class_label(v['class'])}"
    except Exception:
        return plain


def render_card(c, data, ledger=None, old_view=None, changes=None):
    """Return the list of Discord message strings (each < 2000 chars) for one crawler's full card."""
    ledger = ledger or []
    v = make_view(c, data)
    change = last_credit_change(c, ledger, old_view)
    head = [credits_line(c, change)]
    head.append(f"**{v['name'].upper()}** - {_species_class_label(v)} {v['level']} ({v['player']})")
    if v.get("status") == "benched":
        head.append("**BENCHED**: not in play this session. This sheet stays up; the player can swap Crawlers between sessions.")
    hd = v["hit_dice"]
    boxes = ", ".join(f"{t} {n}" for t, n in v["boxes"].items()) or "none"
    head.append("```\n" + f"HP {_hp(v)}  AC {v['ac']}  XP {v['xp']}  Hit Dice {hd.get('current')}/{hd.get('max')}\n"
                + "  ".join(f"{a.upper()} {s}" for a, s in v["abilities"].items()) + "\n```")
    head.append(f"Conditions: {', '.join(v['conditions']) or 'none'} | Loot boxes: {boxes}")
    if v.get("pet"):
        head.append(pet_block(v["pet"]))
    if v["death_saves"] and (v["death_saves"].get("successes") or v["death_saves"].get("fails")):
        head.append(f"Death saves: {v['death_saves'].get('successes', 0)} successes / {v['death_saves'].get('fails', 0)} fails")
    for label, key in (("Standing Orders", "standing_orders"), ("Signature attack", "signature"), ("Standing Reaction", "standing_reaction")):
        if v[key]:
            head.append(f"{label}: {v[key]}")
    shown = [x for x in (changes or []) if not x.startswith("Credits ")]  # the first line already says it
    if shown:
        text = "; ".join(shown)
        head.append("**Changed:** " + (text if len(text) < 700 else text[:697] + "..."))
    blocks = ["\n".join(head)]

    cats = data.get("categories") or [["weapons", "Weapons & focus"], ["armor", "Armor & clothing"], ["magic", "Magic & special"], ["gear", "Gear"]]
    known = {k for k, _ in cats}
    for key, title in cats + [["other", "Other"]]:
        its = [i for i in v["inventory"] if (i["category"] if i["category"] in known else "other") == key]
        if its:
            blocks.append(f"**{title}**\n" + "\n".join(item_line(i) for i in its))
    if not v["inventory"]:
        blocks.append("**Inventory**\n(empty)")
    if v.get("build"):
        blocks.append("**Build**\n" + "\n".join(v["build"]))
    rewards = achievement_rewards(v, ledger)
    if v["achievements"]:
        txt = v.get("achievement_text") or {}
        one = lambda a: a + (f" (+{rewards[a]})" if a in rewards else "") + (f": {txt[a]}" if a in txt else "")  # noqa: E731
        blocks.append("**Achievements**\n" + ("\n".join("- " + one(a) for a in v["achievements"]) if txt else "; ".join(one(a) for a in v["achievements"])))
    return pack_messages(blocks, v["name"])


def pack_messages(blocks, label, limit=MSG_LIMIT):
    """Greedily pack blocks into messages under `limit`; split an oversize block on line (then word) boundaries."""
    pieces = []
    for b in blocks:
        if len(b) <= limit:
            pieces.append(b)
            continue
        cur = ""
        for line in b.split("\n"):
            while len(line) > limit:
                cut = line.rfind(" ", 0, limit)
                cut = cut if cut > limit // 2 else limit
                if cur:
                    pieces.append(cur)
                    cur = ""
                pieces.append(line[:cut])
                line = line[cut:].lstrip()
            if len(cur) + len(line) + 1 > limit:
                pieces.append(cur)
                cur = line
            else:
                cur = f"{cur}\n{line}" if cur else line
        if cur:
            pieces.append(cur)
    msgs, cur = [], ""
    for p in pieces:
        if cur and len(cur) + len(p) + 2 > limit - 40:  # headroom for the "part n/m" marker on continuations
            msgs.append(cur)
            cur = p
        else:
            cur = f"{cur}\n\n{p}" if cur else p
    if cur:
        msgs.append(cur)
    if len(msgs) > 1:
        total = len(msgs)
        msgs = [m if i == 0 else f"*{label} card, part {i + 1}/{total}*\n{m}" for i, m in enumerate(msgs)]
    return msgs


# --------------------------------------------------------------------------- publish

def publish(client, crawler_names=None, full=False, dry_run=False, log=print):
    """Post a new full card for every crawler whose visible state changed since its last published snapshot.
    Returns a list of result dicts. Updates the snapshot only after ALL parts of a card were posted."""
    results = []
    with PublishLock():
        state = read_json(state_path(), None)
        if not isinstance(state, dict):
            raise PublishError(f"no readable state at {state_path()}")
        cfg = load_config()
        data = {**load_card_data(), "pets_enabled": (state.get("limits") or {}).get("pets_enabled", True)}
        ledger = read_ledger()
        snaps = read_json(snapshots_path(), {"version": 1, "crawlers": {}}) or {"version": 1, "crawlers": {}}
        snaps.setdefault("crawlers", {})
        if crawler_names:
            targets = [resolve_crawler(n, state, cfg) for n in crawler_names]
        else:
            targets = list(state.get("crawlers", []))
        for c in targets:
            key, m = mapping_for(cfg, c["name"])
            res = {"crawler": c["name"], "status": "", "parts": 0, "changes": []}
            results.append(res)
            if not m or not m.get("channel_id"):
                res["status"] = "no-channel"
                log(f"{c['name']}: no channel registered (run setup-channels, or register-channel '{c['name']}' <channel-id>)")
                continue
            old = (snaps["crawlers"].get(c["name"]) or {}).get("view")
            new = make_view(c, data)
            changes = diff_views(old, new)   # also non-empty whenever views_differ(old, new): any visible field change reposts
            if old is not None and not changes and not full:
                res["status"] = "unchanged"
                log(f"{c['name']}: no visible changes since the last card")
                continue
            if old is None:
                changes = []
                res["first"] = True
            msgs = render_card(c, data, ledger, old, changes)
            res.update(parts=len(msgs), changes=changes)
            if dry_run:
                res["status"] = "dry-run"
                res["messages"] = msgs
                log(f"--- {c['name']} -> #{m.get('channel_name', '?')} ({len(msgs)} message(s), dry run) ---")
                for i, t in enumerate(msgs, 1):
                    log(t if len(msgs) == 1 else f"[message {i}/{len(msgs)}]\n{t}")
                continue
            ids = []
            try:
                for t in msgs:
                    r = client.request("POST", f"/channels/{m['channel_id']}/messages", {"content": t, "allowed_mentions": {"parse": []}})
                    ids.append(str((r or {}).get("id", "")))
            except DiscordError as e:
                res["status"] = f"failed: {e}"
                res["posted_before_failure"] = len(ids)
                log(f"{c['name']}: posting failed ({e}); snapshot NOT updated, the next publish will retry"
                    + (f" ({len(ids)} of {len(msgs)} parts were already posted)" if ids else ""))
                continue
            snaps["crawlers"][c["name"]] = {"published_at": now_iso(), "view": new, "message_ids": ids}
            write_json_atomic(snapshots_path(), snaps)
            res["status"] = "posted"
            log(f"{c['name']}: posted full card ({len(msgs)} message(s)) to #{m.get('channel_name', m['channel_id'])}")
    return results


# --------------------------------------------------------------------------- permissions / channel setup

def compute_base_perms(roles, member, guild_id):
    by_id = {r["id"]: r for r in roles}
    perms = int(by_id.get(guild_id, {}).get("permissions", 0))
    for rid in member.get("roles", []):
        perms |= int(by_id.get(rid, {}).get("permissions", 0))
    return perms


def channel_perms(base, overwrites, guild_id, member_id, role_ids):
    """Standard Discord channel permission calculation for one member."""
    if base & P_ADMIN:
        return (1 << 53) - 1
    perms = base
    ow = {(o["type"], str(o["id"])): o for o in overwrites or []}
    e = ow.get((0, str(guild_id)))
    if e:
        perms = (perms & ~int(e["deny"])) | int(e["allow"])
    allow = deny = 0
    for rid in role_ids:
        o = ow.get((0, str(rid)))
        if o:
            allow |= int(o["allow"])
            deny |= int(o["deny"])
    perms = (perms & ~deny) | allow
    o = ow.get((1, str(member_id)))
    if o:
        perms = (perms & ~int(o["deny"])) | int(o["allow"])
    return perms


def bot_context(client, guild_id):
    me = client.request("GET", "/users/@me")
    member = client.request("GET", f"/guilds/{guild_id}/members/{me['id']}")
    roles = client.request("GET", f"/guilds/{guild_id}/roles")
    return {"bot_id": str(me["id"]), "bot_name": me.get("username", ""), "member": member, "roles": roles,
            "base": compute_base_perms(roles, member, str(guild_id))}


def guild_id_for(client, cfg):
    if cfg.get("guild_id"):
        return str(cfg["guild_id"])
    ears = session_config().get("ears_channel_id") or os.environ.get("DCC_EARS_CHANNEL_ID", "1556163778788462602")
    return str(client.request("GET", f"/channels/{ears}")["guild_id"])


def protected_channel_ids():
    ids = {os.environ.get("DCC_MOUTH_CHANNEL_ID", "1556163836879568946"), os.environ.get("DCC_EARS_CHANNEL_ID", "1556163778788462602")}
    cfg = session_config()
    ids |= {str(cfg[k]) for k in ("mouth_channel_id", "ears_channel_id", "voice_channel_id") if cfg.get(k)}
    return ids


def default_channel_name(crawler, m):
    """Sheet channel slug. Alpha: <player>-<crawler> (or pet ...-sheet). Other campaigns: <session>-<player>-<crawler> so names cannot collide with alpha in the same guild."""
    if m and m.get("channel_name"):
        return slug(m["channel_name"])
    import campaign_session
    prefix = campaign_session.sheet_channel_prefix()  # "" for alpha, "s1-" etc. otherwise
    budget = max(1, 100 - len(prefix))
    if crawler.get("kind") == "pet-crawler":  # <player>-<pet>-sheet keeps it with its owner's channels
        body = f"{slug(crawler.get('player') or crawler['name'])}-{slug(crawler['name'])}"[: max(1, budget - 6)] + "-sheet"
    else:
        body = f"{slug(crawler.get('player') or crawler['name'])}-{slug(crawler['name'])}"[:budget]
    return (prefix + body)[:100]


CATEGORY_LIMIT, CATEGORY_WARN = 50, 45   # Discord allows 50 channels per category; warn at 45, then open "Crawler Sheets 2", 3, ...


def setup_channels(client, dry_run=False, log=print):
    """Create the 'Crawler Sheets' category and one text channel per crawler that has none, then register them."""
    state = read_json(state_path(), None)
    if not isinstance(state, dict):
        raise PublishError(f"no readable state at {state_path()}")
    cfg = load_config()
    gid = guild_id_for(client, cfg)
    ctx = bot_context(client, gid)
    can_manage = bool(ctx["base"] & (P_ADMIN | P_MANAGE_CHANNELS))
    need = []
    for c in state.get("crawlers", []):
        key, m = mapping_for(cfg, c["name"])
        if m and m.get("channel_id"):
            continue
        need.append((c, m, default_channel_name(c, m)))
    # duplicates by name: two Crawlers (or an already-registered channel) never share a channel name
    used = {slug(v.get("channel_name")) for v in cfg["crawlers"].values() if v.get("channel_name")}
    named = []
    for c, m, base in need:
        nm, n = base, 1
        while nm in used:
            n += 1
            nm = f"{base[:96]}-{n}"
        used.add(nm)
        named.append((c, m, nm))
    need = named
    log(f"Bot '{ctx['bot_name']}' in guild {gid}: Manage Channels = {'YES' if can_manage else 'NO'}")
    if not need:
        log("Every crawler already has a registered channel; nothing to create.")
        return {"created": [], "can_manage": can_manage}
    if not can_manage:
        log("The GM bot role lacks Manage Channels, so channels cannot be created automatically. Choose one:")
        log("  A) Grant 'Manage Channels' to the GM bot role (Server Settings > Roles), then re-run `discord_gm.py setup-channels`.")
        log("  B) Create the channel(s) yourself, then register each with `discord_gm.py register-channel <crawler> <channel-id>`:")
        for c, m, name in need:
            log(f"     - #{name}  (for {c['name']}, player {c.get('player', '?')})")
        log("     Suggested: put them in a category named 'Crawler Sheets', readable by everyone; let only the GM bot post")
        log("     (grant the GM bot View Channel + Send Messages + Read Message History there).")
        return {"created": [], "can_manage": False, "needed": [n for _, _, n in need]}
    existing = client.request("GET", f"/guilds/{gid}/channels")
    cat_name = cfg.get("category_name") or "Crawler Sheets"
    cat = next((ch for ch in existing if ch.get("type") == 4 and norm(ch["name"]) == norm(cat_name)), None)
    plan = [f"category '{cat_name}'" + (" (exists)" if cat else " (create)")] + [f"text channel #{n} for {c['name']}" for c, _, n in need]
    if dry_run:
        log("Dry run - would do: " + "; ".join(plan))
        return {"created": [], "can_manage": True, "plan": plan}
    overwrites = [
        {"id": gid, "type": 0, "allow": str(EVERYONE_ALLOW), "deny": str(EVERYONE_DENY)},   # everyone reads, cannot post
        {"id": ctx["bot_id"], "type": 1, "allow": str(BOT_ALLOW), "deny": "0"},             # the GM bot posts
    ]
    if not cat:
        cat = client.request("POST", f"/guilds/{gid}/channels", {"name": cat_name, "type": 4})
        log(f"Created category '{cat_name}'")
    cfg["guild_id"], cfg["category_id"] = gid, str(cat["id"])
    created = []
    known = list(existing)
    cats = [str(cat["id"])] + [str(x) for x in cfg.get("overflow_category_ids", [])]
    for c, m, name in need:
        registered = {str(v.get("channel_id")) for v in cfg["crawlers"].values() if v.get("channel_id")}
        ch = next((x for x in existing if x.get("type") == 0 and x.get("name") == name and str(x.get("parent_id")) in cats and str(x["id"]) not in registered), None)
        if ch:
            log(f"#{name} already exists in the category; registering it")
        else:
            target = next((cid for cid in cats if sum(1 for x in known if str(x.get("parent_id")) == cid) < CATEGORY_LIMIT), None)
            if target is None:   # every sheet category is full: open Crawler Sheets 2, 3, ... instead of failing
                nm = f"{cat_name} {len(cats) + 1}"
                oc = next((x for x in existing if x.get("type") == 4 and norm(x["name"]) == norm(nm)), None) or client.request("POST", f"/guilds/{gid}/channels", {"name": nm, "type": 4})
                target = str(oc["id"])
                cats.append(target)
                cfg["overflow_category_ids"] = cats[1:]
                log(f"Category full ({CATEGORY_LIMIT} channels): using overflow category '{nm}'")
            elif sum(1 for x in known if str(x.get("parent_id")) == target) >= CATEGORY_WARN:
                log(f"WARNING: category {target} has {sum(1 for x in known if str(x.get('parent_id')) == target)} of {CATEGORY_LIMIT} channels; new sheets will move to an overflow category.")
            ch = client.request("POST", f"/guilds/{gid}/channels", {
                "name": name, "type": 0, "parent_id": target, "permission_overwrites": overwrites,
                "topic": f"{c['name']}'s character sheet - posted by the GM bot after every change. Read-only."})
            known.append(ch)
            log(f"Created #{name}")
        if str(ch["id"]) in protected_channel_ids():
            raise PublishError("refusing to register the voice/transcript channel as a sheet channel")
        entry = cfg["crawlers"].setdefault(c["name"], {"players": [c.get("player", "")]})
        entry.update(channel_id=str(ch["id"]), channel_name=name, owner=c.get("player", ""))
        created.append({"crawler": c["name"], "channel_name": name, "channel_id": str(ch["id"])})
        save_config(cfg)
    return {"created": created, "can_manage": True}


def delete_crawler_channel(client, channel_id, cfg=None, log=print):
    """Delete ONE Crawler's own sheet channel (state.py crawler delete). Refuses the voice/transcript channels, a channel another Crawler still uses,
    anything outside the Crawler Sheets category, and anything that is not a plain text channel. Returns True when deleted."""
    cfg = cfg or load_config()
    cid = str(channel_id)
    if cid in protected_channel_ids():
        raise PublishError("refusing to delete the voice/transcript channel")
    if any(str(v.get("channel_id")) == cid for v in cfg.get("crawlers", {}).values()):
        log("channel is still registered to another Crawler: kept")
        return False
    ch = client.request("GET", f"/channels/{cid}")
    if ch.get("type") != 0:
        raise PublishError("not a plain text channel; not deleting")
    allowed = {str(x) for x in [cfg.get("category_id"), *cfg.get("overflow_category_ids", [])] if x}
    if not allowed or str(ch.get("parent_id")) not in allowed:
        raise PublishError("that channel is not in the Crawler Sheets category; not deleting")
    client.request("DELETE", f"/channels/{cid}")
    log(f"deleted Discord channel #{ch.get('name')}")
    return True


def check_channel_access(client, channel_id):
    """(ok, problems[]) - can the GM bot view and post in this channel? Needs the channel to exist."""
    problems = []
    ch = client.request("GET", f"/channels/{channel_id}")
    if ch.get("type") not in (0, 5):
        problems.append("not a text channel")
    gid = str(ch.get("guild_id", ""))
    ctx = bot_context(client, gid)
    perms = channel_perms(ctx["base"], ch.get("permission_overwrites"), gid, ctx["bot_id"], ctx["member"].get("roles", []))
    for bit, label in ((P_VIEW, "View Channel"), (P_SEND, "Send Messages"), (P_HISTORY, "Read Message History")):
        if not perms & bit:
            problems.append(f"GM bot lacks {label} there")
    return ch, problems


def register_channel(client, crawler_name, channel_id, verify=True, log=print):
    if not re.fullmatch(r"\d{15,25}", str(channel_id)):
        raise PublishError("channel id must be the numeric Discord channel ID (Developer Mode > right-click channel > Copy Channel ID)")
    if str(channel_id) in protected_channel_ids():
        raise PublishError("that is the voice (#gm-voice) or transcript (#table-transcript) channel; sheet cards must go to a separate channel")
    state = read_json(state_path(), None) or {"crawlers": []}
    cfg = load_config()
    c = resolve_crawler(crawler_name, state, cfg)
    for key, m in cfg["crawlers"].items():
        if str(m.get("channel_id")) == str(channel_id) and norm(key) != norm(c["name"]):
            raise PublishError(f"that channel is already registered for {key}")
    name = ""
    if verify:
        ch, problems = check_channel_access(client, channel_id)
        name = ch.get("name", "")
        if problems:
            raise PublishError("cannot use that channel: " + "; ".join(problems) +
                               ". Give the GM bot View Channel + Send Messages + Read Message History there (or use --no-verify).")
        cfg["guild_id"] = cfg.get("guild_id") or str(ch.get("guild_id", ""))
    entry = cfg["crawlers"].setdefault(c["name"], {"players": [c.get("player", "")]})
    entry["owner"] = c.get("player", "")
    entry["channel_id"] = str(channel_id)
    if name:
        entry["channel_name"] = name
    save_config(cfg)
    log(f"Registered #{name or channel_id} for {c['name']}")
    return entry


def channel_status(client=None, log=print):
    state = read_json(state_path(), None) or {"crawlers": []}
    cfg = load_config()
    rows = []
    for c in state.get("crawlers", []):
        key, m = mapping_for(cfg, c["name"])
        cid = (m or {}).get("channel_id") or ""
        row = {"crawler": c["name"], "player": c.get("player", ""), "status": _status(c), "channel_name": (m or {}).get("channel_name", ""), "channel_id": cid, "access": "n/a"}
        if cid and client:
            try:
                _, probs = check_channel_access(client, cid)
                row["access"] = "OK" if not probs else "; ".join(probs)
            except (DiscordError, PublishError) as e:
                row["access"] = f"cannot check ({e})"
        rows.append(row)
        log(f"{c['name']} ({c.get('player', '')}{', ' + row['status'] if row['status'] else ''}): " + (f"#{row['channel_name']} id {cid}, GM bot access: {row['access']}" if cid else "no channel registered"))
    return rows


# --------------------------------------------------------------------------- background entry point (state.py)

def auto_main(delay=3.0):
    """Run by state.py in the background after a state change: wait briefly so a burst of changes coalesces into one
    card, then publish whatever differs from the snapshot. Errors only go to sessions/publish.log."""
    time.sleep(delay)
    try:
        publish(DiscordClient(), log=lambda m: print(f"{now_iso()} {m}", flush=True))
    except (PublishError, DiscordError) as e:
        print(f"{now_iso()} auto-publish skipped: {e}", flush=True)
    return 0


if __name__ == "__main__":
    import campaign_session
    campaign_session.apply_cli_session()
    if "--render-spec" in sys.argv:  # preview the first full card for a create-crawler spec (used by /create review); prints JSON
        import state as _state
        _spec = json.load(open(sys.argv[sys.argv.index("--render-spec") + 1], encoding="utf-8"))
        _c = _state.crawler_from_spec(_spec, with_credits=True)
        print(json.dumps(render_card(_c, load_card_data(), [])))
        sys.exit(0)
    if "--auto" in sys.argv:
        sys.exit(auto_main(float(os.environ.get("DCC_AUTO_PUBLISH_DELAY", "3"))))
    print("use: python3 tools/discord_gm.py publish | setup-channels | register-channel | channels")
