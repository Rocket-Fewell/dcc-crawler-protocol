"""gm_quirks.py - GM-only quirk roll, commitment, degeneration level and per-player Affinity (stdlib only).

Used through state.py (single entry point):
  python3 tools/state.py gm-quirks roll | show-gm | verify | status | level FLOOR | reveal ...
  python3 tools/state.py affinity add|drift|status|register|new-scene ...   (also: gm-quirks affinity ...)

Design doc : gm-notes/secret/gm-quirk-framework.md   (GM-only; section 10 is the schema README)
Tables     : lore/tables/gm-quirks.json           (authoritative; env DCC_GM_QUIRKS_TABLE overrides the path)
Secret dir : <campaign>/gm-notes/secret/          (dir 0700, files 0600; NEVER read by show/snapshot/export/validate)

Nothing here prints a rolled trait except `show-gm` and `reveal` (with a warning banner), and
`affinity ...` (GM-only banner). The `roll` command prints only a neutral confirmation, and writes only a
neutral line to the public roll log (never the dice results).

This module has no import of state.py (state.py imports it): state.py hands over its primitives
(FileLock, atomic_write_json, ...) through bind(). Errors are GMError; state.main prints them and exits 1.
"""
import copy
import datetime as dt
import hashlib
import json
import os
import re
import secrets
import shutil
import sys
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import roll as roll_mod  # noqa: E402  (sibling module; stdlib only)

RUNTIME_SCHEMA_VERSION = "1.0"
BACKUP_KEEP = 20
NEUTRAL_ROLL_MESSAGE = "GM traits rolled and sealed"
OVERRIDE_FLAGS = "--force --i-know-this-reveals"
GM_BANNER = ("*** GM-ONLY / SECRET: for your private reasoning. NEVER paste, quote, hint at or speak this output "
             "in chat, voice, a [ROLL] line or any file. ***")
DEFAULT_TABLE_PATHS = ["lore/tables/gm-quirks.json", "/workspace/dcc-lore/tables/gm-quirks.json"]
TABLE_KEYS = ["meta", "prior_installation", "fixations", "quirks", "tics", "tells", "ladder", "spite_moves", "repair_options"]
ROLL_TABLES = {"prior_installation": "PI", "fixations": "FX", "quirks": "QK", "tics": "VT", "tells": "TL"}
MANIFEST_KEYS = {
    "fixations": {"rewards", "achievements", "insults", "box_contents"},
    "quirks": {"narration", "snark", "rewards", "fair_lever"},
    "tics": {"usage", "sample_lines"},
    "tells": {"how_to_use"},
    "prior_installation": {"memory_leaks", "props"},
}
PLAYER_KEYS = {"display_name", "character", "affinity", "scene_id", "scene_delta", "last_drift_floor", "flags"}
LOG_KEYS = ["ts", "session", "floor", "scene", "player_id", "kind", "raw_delta", "delta", "reason", "evidence",
            "fixation_id", "matched_trigger", "affinity_before", "affinity_after", "capped"]
PLAYER_ID_RE = re.compile(r"[a-z0-9][a-z0-9_-]{0,31}")
MAX_EVIDENCE_WORDS = 25

# test hook: the one source of randomness for the roll (secrets.randbelow). Tests may patch this.
_randbelow = secrets.randbelow


class GMError(Exception):
    """A refused or failed GM-quirk operation (printed to stderr by state.main, exit 1)."""


core = None  # set by bind(): the state.py primitives


def bind(state_module_globals):
    """Receive state.py's primitives (called by state.build_parser)."""
    global core
    names = ("FileLock", "StateError", "atomic_write_json", "now_iso", "campaign_dir", "read_state_file")
    core = types.SimpleNamespace(**{n: state_module_globals[n] for n in names})


# --------------------------------------------------------------------------- paths / files

def _need_core():
    if core is None:
        raise GMError("gm_quirks is not bound to state.py; run it through `python3 tools/state.py`")
    return core


def _campaign():
    return _need_core().campaign_dir()


def table_path():
    env = os.environ.get("DCC_GM_QUIRKS_TABLE")
    if env:
        return env
    for p in DEFAULT_TABLE_PATHS:
        full = p if os.path.isabs(p) else os.path.join(_campaign(), p)
        if os.path.exists(full):
            return full
    return os.path.join(_campaign(), DEFAULT_TABLE_PATHS[0])


_table_cache = {}


def load_table():
    """Load + validate lore's gm-quirks.json (cached per path+mtime)."""
    path = table_path()
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        raise GMError(f"GM quirk table not found at {path} (set DCC_GM_QUIRKS_TABLE or link lore/)")
    key = (path, mtime)
    if key not in _table_cache:
        try:
            with open(path, encoding="utf-8") as f:
                table = json.load(f)
        except json.JSONDecodeError as e:
            raise GMError(f"{path} is not valid JSON ({e})")
        errs = validate_table(table)
        if errs:
            raise GMError(f"{path} does not match the documented schema:\n  - " + "\n  - ".join(errs[:12]))
        _table_cache.clear()
        _table_cache[key] = table
    return _table_cache[key]


def _meta_path(table, key, default):
    rel = table["meta"]["affinity"].get(key) or default
    parts = rel.replace("\\", "/").split("/")
    if parts[:2] != ["gm-notes", "secret"] or len(parts) != 3 or parts[2] in ("", ".", "..") or ".." in parts:
        raise GMError(f"table meta.affinity.{key} must be gm-notes/secret/<file> (got {rel!r})")
    return os.path.join(secret_dir(), parts[2])   # per-session: alpha = gm-notes/secret/, others = gm-notes/secret/sessions/<id>/


def secret_dir():
    import campaign_session
    return campaign_session.secret_dir()


def roll_path(table):
    return _meta_path(table, "roll_file", "gm-notes/secret/gm-quirk-roll.json")


def affinity_path(table):
    return _meta_path(table, "state_file", "gm-notes/secret/gm-affinity.json")


def log_path(table):
    return _meta_path(table, "log_file", "gm-notes/secret/gm-affinity-log.jsonl")


def is_secret_path(path):
    """True if `path` is inside <campaign>/gm-notes/secret (used to keep public commands away from it)."""
    try:
        real = os.path.realpath(path)
        sec = os.path.realpath(secret_dir())
        return real == sec or real.startswith(sec + os.sep)
    except (OSError, GMError):
        return False


def ensure_secret_dir(sub=None):
    d = secret_dir()
    parent = os.path.dirname(d)
    os.makedirs(parent, exist_ok=True)
    if os.path.basename(parent) == "sessions":  # gm-notes/secret/sessions/ (non-alpha sessions)
        os.chmod(parent, 0o700)
    for path in ([d] + ([os.path.join(d, sub)] if sub else [])):
        os.makedirs(path, mode=0o700, exist_ok=True)
        os.chmod(path, 0o700)
    return os.path.join(d, sub) if sub else d


def lock():
    ensure_secret_dir()
    return core.FileLock(os.path.join(secret_dir(), ".gm.lock"))


def write_secret_json(path, data):
    ensure_secret_dir()
    core.atomic_write_json(path, data)
    os.chmod(path, 0o600)


def read_secret_json(path, what, missing_ok=False):
    try:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
    except FileNotFoundError:
        if missing_ok:
            return None
        raise GMError(f"no {what} yet")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise GMError(f"the {what} is not valid JSON; refusing to continue (restore it from gm-notes/secret/backups or archive)")
    if not isinstance(data, dict):
        raise GMError(f"the {what} must contain a JSON object")
    return data


def backup_secret(path, prefix, subdir="backups"):
    """Copy an existing secret file into gm-notes/secret/<subdir>/ (0600) and rotate (newest BACKUP_KEEP)."""
    if not os.path.exists(path):
        return None
    d = ensure_secret_dir(subdir)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    dest = os.path.join(d, f"{prefix}-{stamp}.json")
    n = 1
    while os.path.exists(dest):
        n += 1
        dest = os.path.join(d, f"{prefix}-{stamp}-{n}.json")
    shutil.copy2(path, dest)
    os.chmod(dest, 0o600)
    if os.path.getsize(dest) != os.path.getsize(path):
        raise GMError("backup copy size mismatch; aborting write")
    if subdir == "backups":
        olds = sorted(f for f in os.listdir(d) if f.startswith(prefix + "-") and f.endswith(".json"))
        for old in olds[:-BACKUP_KEEP]:
            try:
                os.unlink(os.path.join(d, old))
            except OSError:
                pass
    return dest


def append_jsonl(path, entries):
    ensure_secret_dir()
    data = "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entries).encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try:
        os.write(fd, data)  # one O_APPEND write
        os.fsync(fd)
    finally:
        os.close(fd)
    os.chmod(path, 0o600)


# --------------------------------------------------------------------------- helpers

def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _clean(text, limit=200):
    text = re.sub(r"[\x00-\x1f\x7f]+", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()[:limit]


def slug(text):
    return re.sub(r"[^a-z0-9_-]+", "-", (text or "").strip().lower()).strip("-")[:32]


def campaign_id():
    """Stable id from state.json (campaign name + created date), else from the campaign folder name."""
    try:
        st = core.read_state_file(missing_ok=True)
    except Exception:
        st = None
    if st and isinstance(st.get("campaign"), dict) and st["campaign"].get("name"):
        c = st["campaign"]
        return (slug(c["name"]) + "-" + str(c.get("created", ""))[:10]).strip("-")
    return slug(os.path.basename(os.path.abspath(_campaign()))) or "dcc-campaign"


def dice_sides(table, which):
    """Die size of a roll table, read from meta.rolls (tells are a d8)."""
    if which == "tells":
        return 8
    key = {"prior_installation": "prior_installation", "fixations": "fixation", "quirks": "quirks", "tics": "tic"}[which]
    m = re.search(r"\d*d(\d+)", table["meta"]["rolls"][key])
    return int(m.group(1))


def entry_for_roll(entries, value):
    for e in entries:
        if e["roll_range"][0] <= value <= e["roll_range"][1]:
            return e
    raise GMError(f"no table entry covers roll {value}")


def entry_by_id(entries, eid):
    for e in entries:
        if e["id"] == eid:
            return e
    return None


# --------------------------------------------------------------------------- table schema validation

def validate_table(t):
    """Check a gm-quirks.json against framework section 10. Returns a list of errors."""
    errs = []
    if not isinstance(t, dict):
        return ["table is not an object"]
    for k in TABLE_KEYS:
        if k not in t:
            errs.append(f"missing top-level key '{k}'")
    extra = [k for k in t if k not in TABLE_KEYS]
    if extra:
        errs.append(f"unexpected top-level keys: {extra}")
    if errs:
        return errs
    meta = t["meta"]
    if not isinstance(meta, dict):
        return ["meta must be an object"]
    if not str(meta.get("schema_version", "")).startswith("1."):
        errs.append("meta.schema_version must be 1.x (this tool understands schema 1)")
    for k in ("doc", "owner", "updated", "tag_note", "visibility", "rolls", "stress", "affinity"):
        if k not in meta:
            errs.append(f"meta.{k} missing")
    if errs:
        return errs
    rolls = meta["rolls"]
    if not (isinstance(rolls, dict) and all(k in rolls for k in ("prior_installation", "fixation", "quirks", "tic", "order"))):
        return errs + ["meta.rolls must have prior_installation, fixation, quirks, tic, order[]"]
    if rolls["order"] != ["prior_installation", "fixation", "fixation_variant", "quirks", "tic"]:
        errs.append("meta.rolls.order is not the order this tool implements")
    aff = meta["affinity"]
    for k in ("range", "scene_cap", "point_values", "drift_per_floor", "drift_direction", "bands", "state_file", "log_file",
              "roll_file", "visibility", "state_schema", "log_schema", "roll_schema"):
        if k not in aff:
            errs.append(f"meta.affinity.{k} missing")
    if errs:
        return errs
    rng = aff["range"]
    if not (isinstance(rng, dict) and all(_is_int(rng.get(k)) for k in ("min", "max", "start")) and rng["min"] < rng["max"]
            and rng["min"] <= rng["start"] <= rng["max"]):
        errs.append("meta.affinity.range must be integer {min,max,start}")
    if not (_is_int(aff["scene_cap"]) and aff["scene_cap"] >= 1):
        errs.append("meta.affinity.scene_cap must be an integer >= 1")
    if not (_is_int(aff["drift_per_floor"]) and aff["drift_per_floor"] >= 0) or aff["drift_direction"] != "toward_zero":
        errs.append("meta.affinity drift_per_floor must be an int >= 0 and drift_direction 'toward_zero'")
    if aff["visibility"] != "gm_only":
        errs.append("meta.affinity.visibility must be 'gm_only'")
    if errs:
        return errs
    # bands: ordered coverage of min..max, no gap, no overlap
    bands = aff["bands"]
    if not (isinstance(bands, list) and bands and all(isinstance(b, dict) and _is_int(b.get("min")) and _is_int(b.get("max"))
                                                     and isinstance(b.get("name"), str) and isinstance(b.get("id"), str) for b in bands)):
        errs.append("meta.affinity.bands must be a list of {id,name,min,max,effects}")
    else:
        covered = []
        for b in bands:
            if b["min"] > b["max"]:
                errs.append(f"band {b['id']}: min > max")
            covered += list(range(b["min"], b["max"] + 1))
        if sorted(covered) != list(range(rng["min"], rng["max"] + 1)):
            errs.append("meta.affinity.bands must cover min..max exactly once (no gaps or overlaps)")
    # roll tables
    for name, prefix in ROLL_TABLES.items():
        entries = t[name]
        if not isinstance(entries, list) or not entries:
            errs.append(f"{name} must be a non-empty array")
            continue
        sides = dice_sides(t, name) if name != "tells" else 8
        seen, covered = set(), []
        for i, e in enumerate(entries):
            where = f"{name}[{i}]"
            if not isinstance(e, dict):
                errs.append(f"{where} must be an object")
                continue
            eid = e.get("id")
            if not (isinstance(eid, str) and re.fullmatch(prefix + r"-\d\d", eid)):
                errs.append(f"{where}.id must look like {prefix}-NN")
                continue
            if eid in seen:
                errs.append(f"duplicate id {eid}")
            seen.add(eid)
            rr = e.get("roll_range")
            if not (isinstance(rr, list) and len(rr) == 2 and all(_is_int(x) for x in rr) and 1 <= rr[0] <= rr[1] <= sides):
                errs.append(f"{eid}: roll_range must be [min,max] within 1..{sides}")
            else:
                covered += list(range(rr[0], rr[1] + 1))
            for k in ("name", "description"):
                if not (isinstance(e.get(k), str) and e[k]):
                    errs.append(f"{eid}: {k} must be a non-empty string")
            mk = e.get("manifests_as")
            if not (isinstance(mk, dict) and set(mk) == MANIFEST_KEYS[name]):
                errs.append(f"{eid}: manifests_as keys must be {sorted(MANIFEST_KEYS[name])}")
            tl = e.get("tells_by_level")
            if not (isinstance(tl, dict) and set(tl) == {"0", "1", "2", "3", "4", "5"} and all(isinstance(v, str) for v in tl.values())):
                errs.append(f"{eid}: tells_by_level must have string keys '0'..'5'")
            if name == "fixations":
                af = e.get("affinity")
                if not (isinstance(af, dict) and isinstance(af.get("trigger_keywords"), list) and isinstance(af.get("trigger_themes"), list)
                        and isinstance(af.get("pleases"), list) and isinstance(af.get("offends"), list)):
                    errs.append(f"{eid}: affinity must have trigger_keywords[], trigger_themes[], pleases[], offends[]")
                else:
                    for p in af["pleases"]:
                        if not (isinstance(p, dict) and _is_int(p.get("points")) and 1 <= p["points"] <= 3 and isinstance(p.get("action"), str)):
                            errs.append(f"{eid}: pleases points must be 1..3")
                    for p in af["offends"]:
                        if not (isinstance(p, dict) and _is_int(p.get("points")) and -3 <= p["points"] <= -1 and isinstance(p.get("action"), str)):
                            errs.append(f"{eid}: offends points must be -3..-1")
                for v in e.get("variants", []):
                    if not (isinstance(v, dict) and re.fullmatch(r"d\d+", str(v.get("roll", ""))) and isinstance(v.get("values"), list)
                            and v["values"] and int(v["roll"][1:]) == len(v["values"])):
                        errs.append(f"{eid}: variants must be {{roll:'dN', values:[N items]}}")
        if sorted(covered) != list(range(1, sides + 1)):
            errs.append(f"{name}: roll_range values must cover 1..{sides} exactly once")
    # ladder
    lad = t["ladder"]
    need = ["level", "name", "floor_min", "floor_max", "summary", "narration_style", "reward_generosity", "snark_level",
            "glitch_check_d20_max", "glitch_moments", "tells_per_session", "fixation_intrusions_per_session",
            "spite_points_per_floor", "fair_levers", "canon_basis", "tag"]
    if not (isinstance(lad, list) and [e.get("level") for e in lad if isinstance(e, dict)] == list(range(len(lad))) and len(lad) == 6):
        errs.append("ladder must have entries for levels 0..5 in order")
    else:
        lerrs, prev_max = [], 0
        for e in lad:
            miss = [k for k in need if k not in e]
            if miss:
                lerrs.append(f"ladder L{e['level']}: missing {miss}")
                continue
            if prev_max is None or e["floor_min"] != prev_max + 1:
                lerrs.append(f"ladder L{e['level']}: floor_min must follow the previous level's floor_max")
            if e["floor_max"] is None:
                if e["level"] != 5:
                    lerrs.append(f"ladder L{e['level']}: only the last level may be open-ended")
                prev_max = None
            else:
                prev_max = e["floor_max"]
            if not (_is_int(e["glitch_check_d20_max"]) and 0 <= e["glitch_check_d20_max"] <= 20):
                lerrs.append(f"ladder L{e['level']}: glitch_check_d20_max must be 0..20")
            if not (_is_int(e["snark_level"]) and 1 <= e["snark_level"] <= 5):
                lerrs.append(f"ladder L{e['level']}: snark_level must be 1..5")
        if not lerrs and lad[-1]["floor_max"] is not None:
            lerrs.append("the last ladder level must be open-ended (floor_max null)")
        errs += lerrs
    for name in ("spite_moves", "repair_options"):
        if not (isinstance(t[name], list) and t[name]):
            errs.append(f"{name} must be a non-empty array")
    return errs


# --------------------------------------------------------------------------- commitment / roll file

def canonical_rolls(rolls):
    return json.dumps(rolls, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def commitment_for(rolls, nonce):
    """sha256( canonical_json(rolls) + "|" + nonce ), utf-8, lowercase hex."""
    return hashlib.sha256((canonical_rolls(rolls) + "|" + nonce).encode("utf-8")).hexdigest()


def validate_roll_data(data, table):
    errs = []
    keys = {"schema_version", "campaign_id", "rolled_at", "rng", "nonce", "rolls", "commitment_sha256", "revealed"}
    if set(data) != keys:
        return [f"roll file keys must be exactly {sorted(keys)}"]
    for k in ("schema_version", "campaign_id", "rolled_at", "rng", "nonce"):
        if not (isinstance(data[k], str) and data[k]):
            errs.append(f"{k} must be a non-empty string")
    if not (isinstance(data["nonce"], str) and re.fullmatch(r"[0-9a-f]{32,}", data["nonce"])):
        errs.append("nonce must be lowercase hex (>= 128 bits)")
    if not (isinstance(data["commitment_sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", data["commitment_sha256"])):
        errs.append("commitment_sha256 must be 64 hex chars")
    if not isinstance(data["revealed"], bool):
        errs.append("revealed must be a boolean")
    r = data["rolls"]
    if not (isinstance(r, dict) and set(r) == {"prior_installation", "fixation", "fixation_variant", "quirks", "tic"}):
        return errs + ["rolls must have exactly prior_installation, fixation, fixation_variant, quirks[2], tic"]
    if entry_by_id(table["prior_installation"], r["prior_installation"]) is None:
        errs.append("rolls.prior_installation is not a table id")
    fx = entry_by_id(table["fixations"], r["fixation"])
    if fx is None:
        errs.append("rolls.fixation is not a table id")
    else:
        variants = fx.get("variants") or []
        if variants:
            allowed = [str(v) for v in variants[0]["values"]]
            if r["fixation_variant"] not in allowed:
                errs.append("rolls.fixation_variant must be one of the fixation's variant values")
        elif r["fixation_variant"] is not None:
            errs.append("rolls.fixation_variant must be null for this fixation")
    q = r["quirks"]
    if not (isinstance(q, list) and len(q) == 2 and q[0] != q[1] and all(entry_by_id(table["quirks"], x) for x in q)):
        errs.append("rolls.quirks must be two distinct quirk ids")
    if entry_by_id(table["tics"], r["tic"]) is None:
        errs.append("rolls.tic is not a table id")
    return errs


def load_roll(table, must_exist=True):
    data = read_secret_json(roll_path(table), "GM quirk roll", missing_ok=not must_exist)
    if data is None:
        return None
    errs = validate_roll_data(data, table)
    if errs:
        raise GMError("the sealed roll file is invalid: " + "; ".join(errs[:4]))
    return data


def do_roll(table):
    """Roll the traits with secure randomness. Order per meta.rolls.order. Returns the `rolls` object."""
    def d(sides):
        return _randbelow(sides) + 1
    pi = entry_for_roll(table["prior_installation"], d(dice_sides(table, "prior_installation")))
    fx = entry_for_roll(table["fixations"], d(dice_sides(table, "fixations")))
    variant = None
    if fx.get("variants"):
        spec = fx["variants"][0]
        variant = str(spec["values"][d(int(spec["roll"][1:])) - 1])
    qsides = dice_sides(table, "quirks")
    q1 = entry_for_roll(table["quirks"], d(qsides))
    q2 = entry_for_roll(table["quirks"], d(qsides))
    while q2["id"] == q1["id"]:  # "reroll duplicates"
        q2 = entry_for_roll(table["quirks"], d(qsides))
    tic = entry_for_roll(table["tics"], d(dice_sides(table, "tics")))
    return {"prior_installation": pi["id"], "fixation": fx["id"], "fixation_variant": variant,
            "quirks": [q1["id"], q2["id"]], "tic": tic["id"]}


def _public_roll_log(line):
    entry = {"timestamp": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "line": line}
    try:
        roll_mod.append_log(entry)
        return True
    except OSError as e:
        print(f"[ROLL-WARN] could not write roll log: {e}", file=sys.stderr)
        return False


def cmd_gm_roll(a):
    _need_core()
    table = load_table()
    path = roll_path(table)
    if a.force != a.i_know_this_reveals:
        raise GMError(f"--force and --i-know-this-reveals must be given together ({OVERRIDE_FLAGS})")
    override = a.force and a.i_know_this_reveals
    with lock():
        exists = os.path.exists(path)
        if exists and not override:
            raise GMError("REFUSED: the GM traits are already rolled and sealed; rerolling would break the commitment the table was "
                          f"told. Deliberate override (archives the old file, logs a public notice): roll {OVERRIDE_FLAGS}")
        archived = None
        if exists:
            archived = backup_secret(path, "gm-quirk-roll", subdir="archive")
        rolls = do_roll(table)
        nonce = secrets.token_hex(32)
        data = {
            "schema_version": RUNTIME_SCHEMA_VERSION,
            "campaign_id": a.campaign_id or campaign_id(),
            "rolled_at": core.now_iso(),
            "rng": "secrets.randbelow",
            "nonce": nonce,
            "rolls": rolls,
            "commitment_sha256": commitment_for(rolls, nonce),
            "revealed": False,
        }
        errs = validate_roll_data(data, table)
        if errs:
            raise GMError("internal error: rolled data failed validation: " + "; ".join(errs))
        write_secret_json(path, data)
    # Public roll log: NEVER the results, nothing that depends on them (no dice count: a variant die would leak FX-11).
    line = ("[ROLL] GM trait dice: rolled and sealed in the GM-only file (results secret)"
            + (" - OVERRIDE: previous roll archived, table should be told" if archived else "")
            + f" - commitment sha256:{data['commitment_sha256']}")
    _public_roll_log(line)
    return {"ok": True, "message": NEUTRAL_ROLL_MESSAGE}, NEUTRAL_ROLL_MESSAGE


def cmd_gm_verify(a):
    _need_core()
    table = load_table()
    data = load_roll(table)
    expected = commitment_for(data["rolls"], data["nonce"])
    ok = secrets.compare_digest(expected, data["commitment_sha256"])
    if not ok:
        raise GMError("VERIFY FAILED: the stored commitment does NOT match the sealed roll + nonce (file edited?)")
    return ({"ok": True, "commitment_sha256": data["commitment_sha256"]},
            f"commitment OK: sha256(canonical rolls + '|' + nonce) matches {data['commitment_sha256']}")


def cmd_gm_status(a):
    """Public: only whether the roll exists, when, and the commitment hash (safe to publish)."""
    _need_core()
    table = load_table()
    data = load_roll(table, must_exist=False)
    if data is None:
        return {"rolled": False}, "GM traits: not rolled yet (run `gm-quirks roll` once before Floor 1)"
    return ({"rolled": True, "rolled_at": data["rolled_at"], "commitment_sha256": data["commitment_sha256"], "revealed": data["revealed"]},
            f"GM traits: rolled and sealed at {data['rolled_at']}\ncommitment sha256: {data['commitment_sha256']}\nrevealed: {'yes' if data['revealed'] else 'no'}")


def _render_traits(table, data, level=None):
    r = data["rolls"]
    pi = entry_by_id(table["prior_installation"], r["prior_installation"])
    fx = entry_by_id(table["fixations"], r["fixation"])
    qs = [entry_by_id(table["quirks"], q) for q in r["quirks"]]
    vt = entry_by_id(table["tics"], r["tic"])
    levels = [str(level)] if level is not None else ["0", "1", "2", "3", "4", "5"]

    def tells(e, indent="    "):
        return "\n".join(f"{indent}L{lv}: {e['tells_by_level'][lv]}" for lv in levels)

    def manif(e):
        return "\n".join(f"    {k}: {v if not isinstance(v, list) else ' | '.join(v)}" for k, v in e["manifests_as"].items())

    out = [GM_BANNER, "", f"PRIOR INSTALLATION: {pi['id']} {pi['name']}", f"  {pi['description']}", manif(pi), "  tells by level:", tells(pi)]
    out += ["", f"FIXATION: {fx['id']} {fx['name']}" + (f"  [variant roll: {r['fixation_variant']}]" if r["fixation_variant"] else ""),
            f"  {fx['description']}", manif(fx)]
    af = fx["affinity"]
    out += ["  affinity trigger keywords: " + ", ".join(af["trigger_keywords"]),
            "  affinity themes: " + "; ".join(af["trigger_themes"]),
            "  pleases: " + "; ".join(f"{p['action']} ({p['points']:+d})" for p in af["pleases"]),
            "  offends: " + "; ".join(f"{p['action']} ({p['points']:+d})" for p in af["offends"]),
            "  tells by level:", tells(fx)]
    for i, q in enumerate(qs, 1):
        out += ["", f"QUIRK {i}: {q['id']} {q['name']}", f"  {q['description']}", manif(q), "  tells by level:", tells(q)]
    out += ["", f"VERBAL TIC: {vt['id']} {vt['name']}", f"  {vt['description']}", manif(vt), "  tells by level:", tells(vt)]
    if level is not None:
        out += ["", f"GENERIC TELL TABLE (d8) at level {level}:"]
        out += [f"    {t['id']} {t['name']}: {t['tells_by_level'][str(level)]}" for t in table["tells"]]
    out += ["", f"rolled_at: {data['rolled_at']} | commitment sha256: {data['commitment_sha256']} | revealed: {data['revealed']}", "", GM_BANNER]
    return "\n".join(out)


def cmd_show_gm(a):
    _need_core()
    table = load_table()
    if a.level is not None and not 0 <= a.level <= 5:
        raise GMError("--level must be 0..5")
    data = load_roll(table)
    payload = {"warning": GM_BANNER, "rolls": data["rolls"], "rolled_at": data["rolled_at"],
               "commitment_sha256": data["commitment_sha256"], "revealed": data["revealed"]}
    return payload, _render_traits(table, data, a.level)


def cmd_reveal(a):
    _need_core()
    if not a.i_know_this_reveals:
        raise GMError(f"REFUSED: reveal prints the nonce and the roll for the finale; add --i-know-this-reveals to confirm")
    table = load_table()
    with lock():
        data = load_roll(table)
        if commitment_for(data["rolls"], data["nonce"]) != data["commitment_sha256"]:
            raise GMError("VERIFY FAILED: commitment does not match; not revealing")
        backup_secret(roll_path(table), "gm-quirk-roll", subdir="archive")
        data["revealed"] = True
        write_secret_json(roll_path(table), data)
    _public_roll_log(f"[ROLL] GM trait roll REVEALED by the GM (finale) - commitment sha256:{data['commitment_sha256']}")
    text = (_render_traits(table, data) + f"\n\nFINALE REVEAL - nonce: {data['nonce']}\n"
            "Players can verify: sha256 of (canonical JSON of rolls with sorted keys and compact separators) + '|' + nonce "
            "equals the published commitment (see tools/README.md).")
    return {"rolls": data["rolls"], "nonce": data["nonce"], "commitment_sha256": data["commitment_sha256"], "revealed": True}, text


# --------------------------------------------------------------------------- Busted guess (rules/50 section 6)

GUESS_ERR = "could not grade this call"


def _sealed_traits(table, data, kind):
    """The sealed table entries for one guess kind, resolved in memory only (never returned to a caller that prints)."""
    r = data["rolls"]
    if kind == "fixation":
        return [entry_by_id(table["fixations"], r["fixation"])]
    if kind == "quirk":
        return [entry_by_id(table["quirks"], q) for q in r["quirks"]]
    if kind == "tic":
        return [entry_by_id(table["tics"], r["tic"])]
    if kind == "prior_installation":
        return [entry_by_id(table["prior_installation"], r["prior_installation"])]
    return ([entry_by_id(table["fixations"], r["fixation"]), entry_by_id(table["tics"], r["tic"]), entry_by_id(table["prior_installation"], r["prior_installation"])]
            + [entry_by_id(table["quirks"], q) for q in r["quirks"]])  # tell: every sealed trait's tells


def cmd_guess(a):
    """Print ONLY "Busted" or "Not busted". One call per crawler per scene; a repeated call is rejected; no other consequence for a miss.
    A correct call records Therapy unlocked (Floor 8+, 250 x multiplier, no DC). Only the player's text and the result are logged."""
    import busted
    import repair_log
    _need_core()
    kind = busted.KINDS.get((a.kind or "").strip().lower())
    text = re.sub(r"\s+", " ", a.trigger or "").strip()
    scene = _clean(a.scene or "", 60)
    problem = (None if kind else "unknown kind (use fixation, quirk, tic, tell or prior-installation)") or ("a call needs --crawler, --floor and --scene" if not (a.crawler and scene and a.floor and a.floor >= 1) else None) or busted.check_text(text)
    if problem:
        raise GMError(problem)
    try:
        crawlers = {c["name"].lower(): c["name"] for c in core.read_state_file().get("crawlers", [])}
    except Exception:
        crawlers = {}
    if crawlers and a.crawler.strip().lower() not in crawlers:
        raise GMError("unknown crawler")
    who = crawlers.get(a.crawler.strip().lower(), _clean(a.crawler, 60))
    key = busted.call_key(kind, text)
    with lock():
        try:
            log = repair_log.read_entries()
            if not repair_log.tell_shown(log, scene, a.floor):
                raise GMError("no tell was shown this scene")  # decided from the repair log alone: the sealed roll is not consulted
            calls = [e for e in log if e.get("type") == "busted_call" and e["crawler"].lower() == who.lower()]
            if any(e["result"] == "Busted" for e in calls):
                raise GMError("already Busted: Therapy is unlocked, no more calls needed")
            if any(busted.call_key(e["kind"], e["text"]) == key for e in calls):
                raise GMError("that call was already made; a call cannot be repeated")
            if any(e["scene"] == scene for e in calls):
                raise GMError("one call per crawler per scene")
            try:
                table = load_table()
                data = load_roll(table)
                traits = _sealed_traits(table, data, kind)
                hit = busted.grade(kind, text, traits)
            except Exception:
                raise GMError(GUESS_ERR)
            del traits, data  # nothing sealed leaves this function
            result = "Busted" if hit else "Not busted"
            repair_log.append({"type": "busted_call", "crawler": who, "floor": a.floor, "scene": scene, "kind": kind, "text": text[:200],
                               "result": result, "therapy_unlocked": hit, "therapy_min_floor": 8})
        except repair_log.RepairLogError as e:
            raise GMError(str(e))
    return {"result": result}, result


# --------------------------------------------------------------------------- degeneration ladder (public)

def ladder_entry_for_floor(table, floor):
    for e in table["ladder"]:
        if floor >= e["floor_min"] and (e["floor_max"] is None or floor <= e["floor_max"]):
            return e
    raise GMError(f"no ladder level covers floor {floor}")


def cmd_level(a):
    _need_core()
    table = load_table()
    if a.floor < 1:
        raise GMError("floor must be >= 1")
    if a.stress not in (-1, 0, 1):
        raise GMError("--stress must be -1, 0 or 1")
    base = ladder_entry_for_floor(table, a.floor)
    eff = table["ladder"][max(0, min(5, base["level"] + a.stress))]
    g = eff["glitch_check_d20_max"]
    data = {
        "floor": a.floor, "base_level": base["level"], "stress": a.stress, "effective_level": eff["level"],
        "name": eff["name"], "glitch_check_d20_max": g, "tells_per_session": eff["tells_per_session"],
        "fixation_intrusions_per_session": eff["fixation_intrusions_per_session"], "spite_points_per_floor": eff["spite_points_per_floor"],
        "snark_level": eff["snark_level"],
    }
    glitch = "never (no glitch check)" if g == 0 else f"glitch moment if the open d20 <= {g}"
    text = (f"Floor {a.floor}: base level {base['level']} ({base['name']}), stress {a.stress:+d} -> effective level {eff['level']} ({eff['name']})\n"
            f"Glitch check (once per scene, roll d20 with roll.py): {glitch}\n"
            f"Tells/session {eff['tells_per_session']['min']}-{eff['tells_per_session']['max']} | spite points/floor {eff['spite_points_per_floor']} | snark {eff['snark_level']}/5")
    return data, text


# --------------------------------------------------------------------------- affinity

def band_for(table, value):
    for b in table["meta"]["affinity"]["bands"]:
        if b["min"] <= value <= b["max"]:
            return b
    raise GMError(f"no affinity band covers {value}")


def validate_affinity(data, table):
    errs = []
    a = table["meta"]["affinity"]
    lo, hi, cap = a["range"]["min"], a["range"]["max"], a["scene_cap"]
    if not isinstance(data, dict) or set(data) != {"schema_version", "campaign_id", "updated", "players"}:
        return ["affinity file keys must be exactly schema_version, campaign_id, updated, players"]
    for k in ("schema_version", "campaign_id", "updated"):
        if not isinstance(data[k], str) or not data[k]:
            errs.append(f"{k} must be a non-empty string")
    if not isinstance(data["players"], dict):
        return errs + ["players must be an object"]
    for pid, p in data["players"].items():
        if not PLAYER_ID_RE.fullmatch(pid):
            errs.append(f"player id '{pid}' must be lowercase a-z0-9_- (max 32)")
            continue
        if not (isinstance(p, dict) and set(p) == PLAYER_KEYS):
            errs.append(f"player '{pid}': keys must be exactly {sorted(PLAYER_KEYS)}")
            continue
        for k in ("display_name", "character", "scene_id"):
            if not isinstance(p[k], str):
                errs.append(f"player '{pid}': {k} must be a string")
        if not (_is_int(p["affinity"]) and lo <= p["affinity"] <= hi):
            errs.append(f"player '{pid}': affinity must be an integer {lo}..{hi}")
        if not (_is_int(p["scene_delta"]) and -cap <= p["scene_delta"] <= cap):
            errs.append(f"player '{pid}': scene_delta must be an integer {-cap}..{cap}")
        if not (_is_int(p["last_drift_floor"]) and p["last_drift_floor"] >= 0):
            errs.append(f"player '{pid}': last_drift_floor must be an integer >= 0")
        if not (isinstance(p["flags"], list) and all(isinstance(x, str) for x in p["flags"])):
            errs.append(f"player '{pid}': flags must be an array of strings")
    return errs


def _affinity_mutate(table, fn, allow_missing=False):
    """Locked read-modify-write of gm-affinity.json. fn(data_or_None) -> (new_data, result, log_entries).
    Order: validate -> backup old -> atomic write state -> append log lines."""
    path = affinity_path(table)
    with lock():
        cur = read_secret_json(path, "affinity file (register players first: affinity register)", missing_ok=allow_missing)
        if cur is not None:
            errs = validate_affinity(cur, table)
            if errs:
                raise GMError("the affinity file is invalid; refusing to change it: " + "; ".join(errs[:4]))
        new, result, entries = fn(copy.deepcopy(cur) if cur is not None else None)
        errs = validate_affinity(new, table)
        if errs:
            raise GMError("refusing to write - resulting affinity file is invalid: " + "; ".join(errs[:4]))
        new["updated"] = core.now_iso()
        backup_secret(path, "gm-affinity")
        write_secret_json(path, new)
        if entries:
            try:
                append_jsonl(log_path(table), entries)
            except OSError as e:
                raise GMError(f"affinity was updated but the log append failed ({e}); fix and add the log line by hand")
        return result


def _read_affinity(table):
    data = read_secret_json(affinity_path(table), "affinity file (register players first: affinity register)")
    errs = validate_affinity(data, table)
    if errs:
        raise GMError("the affinity file is invalid: " + "; ".join(errs[:4]))
    return data


def _find_player(data, player_id):
    pid = (player_id or "").strip().lower()
    if pid in data["players"]:
        return pid
    raise GMError(f"player '{player_id}' is not registered for affinity (registered: {', '.join(data['players']) or 'none'}); "
                  "use `affinity register`")


def _state_crawlers(player_id=None):
    """Crawlers from state.json (read-only). Missing file -> []; corrupt -> GMError (cannot check opt-outs safely)."""
    try:
        st = core.read_state_file(missing_ok=True)
    except core.StateError as e:
        raise GMError(f"cannot read state.json to check private opt-outs, so no scoring: {e}")
    crawlers = (st or {}).get("crawlers", [])
    if not isinstance(crawlers, list):
        return []
    out = [c for c in crawlers if isinstance(c, dict)]
    if player_id is not None:
        out = [c for c in out if slug(str(c.get("player", ""))) == player_id]
    return out


def _opt_out_hit(crawlers, free_text, topic_terms):
    """True if any opt-out of these crawlers covers the topic. Opt-out text is never echoed back."""
    low_free = [t.lower() for t in free_text if t]
    topics = [t.lower() for t in topic_terms if t]
    for c in crawlers:
        fp = c.get("fan_profile") if isinstance(c.get("fan_profile"), dict) else {}
        for raw in fp.get("opt_outs", []) or []:
            term = str(raw.get("topic", "") if isinstance(raw, dict) else raw).strip().lower()
            if len(term) < 2:
                continue
            if any(term in t for t in low_free):
                return True
            for t in topics:
                if term in t or (len(t) >= 3 and t in term):
                    return True
    return False


def cmd_aff_register(a):
    _need_core()
    table = load_table()
    start = table["meta"]["affinity"]["range"]["start"]
    cur_floor = 0
    try:
        st = core.read_state_file(missing_ok=True)
        if st:
            cur_floor = int(st["campaign"]["current_floor"])
    except (core.StateError, KeyError, TypeError, ValueError):
        pass
    floor = cur_floor if a.floor is None else a.floor
    if floor < 0:
        raise GMError("--floor must be >= 0")
    targets = []  # (pid, display_name, character)
    if a.from_state:
        for c in _state_crawlers():
            pid = slug(str(c.get("player", "")))
            if PLAYER_ID_RE.fullmatch(pid):
                targets.append((pid, str(c.get("player")), str(c.get("name", ""))))
        if not targets:
            raise GMError("no crawlers in state.json to register")
    else:
        if not a.player_id:
            raise GMError("give a player_id, or --from-state")
        pid = a.player_id.strip().lower()
        if not PLAYER_ID_RE.fullmatch(pid):
            raise GMError("player_id must be lowercase letters, digits, '_' or '-' (max 32), e.g. the slug of the crawler's player name")
        crawlers = _state_crawlers(pid)
        name = a.name or (str(crawlers[0].get("player")) if crawlers else None)
        char = a.character or (str(crawlers[0].get("name")) if crawlers else None)
        if not name or not char:
            raise GMError("no matching crawler in state.json: give --name and --character")
        targets.append((pid, _clean(name, 60), _clean(char, 60)))

    def fn(data):
        if data is None:
            data = {"schema_version": RUNTIME_SCHEMA_VERSION, "campaign_id": campaign_id(), "updated": core.now_iso(), "players": {}}
        added, skipped = [], []
        for pid, name, char in targets:
            if pid in data["players"]:
                if not a.from_state:
                    raise GMError(f"player '{pid}' is already registered")
                skipped.append(pid)
                continue
            data["players"][pid] = {"display_name": name, "character": char, "affinity": start, "scene_id": "", "scene_delta": 0,
                                    "last_drift_floor": floor, "flags": []}
            added.append(pid)
        return data, {"added": added, "skipped": skipped}, []
    res = _affinity_mutate(table, fn, allow_missing=True)
    msg = f"[GM-ONLY] registered: {', '.join(res['added']) or 'none'}" + (f" | already registered: {', '.join(res['skipped'])}" if res["skipped"] else "")
    return {"ok": True, **res}, msg


def cmd_aff_add(a):
    _need_core()
    table = load_table()
    aff = table["meta"]["affinity"]
    lo, hi, cap = aff["range"]["min"], aff["range"]["max"], aff["scene_cap"]
    if not _is_int(a.delta) or a.delta == 0 or not lo <= a.delta <= hi:
        raise GMError(f"delta must be a non-zero integer between {lo} and {hi:+d} (usual values are +/-1..3)")
    if a.floor < 1:
        raise GMError("--floor must be >= 1")
    reason = _clean(a.reason)
    if not reason:
        raise GMError("--reason is required (say why, in a short sentence)")
    evidence = _clean(a.evidence or "", 400)
    if len(evidence.split()) > MAX_EVIDENCE_WORDS:
        raise GMError(f"--evidence must be at most {MAX_EVIDENCE_WORDS} words (a short quote or a description of the action)")
    session, scene = _clean(a.session, 60), _clean(a.scene, 60)
    if not session or not scene:
        raise GMError("--session and --scene must not be empty")
    trigger = _clean(a.trigger or "", 100)
    fx = None
    fixation_id = None
    if a.fixation_id:
        fixation_id = a.fixation_id.strip().upper()
        fx = entry_by_id(table["fixations"], fixation_id)
        if fx is None:
            raise GMError("--fixation-id must be a fixation id like FX-07 from the table")
    pid_in = a.player_id.strip().lower()

    def fn(data):
        pid = _find_player(data, pid_in)
        if fx is not None:  # must be the sealed fixation; the mismatch message does not reveal the real one
            sealed = load_roll(table, must_exist=False)
            if sealed is None or sealed["rolls"]["fixation"] != fixation_id:
                raise GMError("REFUSED: --fixation-id does not match the sealed fixation (or nothing is sealed yet); "
                              "omit it for generic scoring")
        topic_terms = [trigger] + ([fx["id"], fx["name"]] + fx["affinity"]["trigger_keywords"] if fx else [])
        if _opt_out_hit(_state_crawlers(pid), [reason, evidence, trigger], topic_terms):
            raise GMError("REFUSED: this player has a private opt-out covering this topic; opted-out topics are never scored. Nothing changed.")
        p = data["players"][pid]
        if p["scene_id"] != scene:  # first score in a new scene: the scene tally starts over
            p["scene_id"], p["scene_delta"] = scene, 0
        before, sd_before = p["affinity"], p["scene_delta"]
        allowed_scene = max(-cap, min(cap, sd_before + a.delta)) - sd_before  # net +/-cap per scene
        new_aff = max(lo, min(hi, before + allowed_scene))
        applied = new_aff - before
        p["affinity"] = new_aff
        p["scene_delta"] = sd_before + applied
        capped = applied != a.delta
        entry = {"ts": core.now_iso(), "session": session, "floor": a.floor, "scene": scene, "player_id": pid, "kind": "event",
                 "raw_delta": a.delta, "delta": applied, "reason": reason, "evidence": evidence, "fixation_id": fixation_id,
                 "matched_trigger": trigger, "affinity_before": before, "affinity_after": new_aff, "capped": capped}
        res = {"player_id": pid, "raw_delta": a.delta, "delta": applied, "capped": capped, "affinity": new_aff,
               "band": band_for(table, new_aff)["name"], "scene_delta": p["scene_delta"], "scene": scene}
        return data, res, [entry]
    res = _affinity_mutate(table, fn)
    msg = (f"[GM-ONLY] {res['player_id']}: {res['raw_delta']:+d} requested, {res['delta']:+d} applied"
           + (" (CAPPED)" if res["capped"] else "") + f" -> affinity {res['affinity']:+d} ({res['band']}), scene delta {res['scene_delta']:+d}/{cap}")
    return {"warning": GM_BANNER, **res}, msg


def cmd_aff_drift(a):
    _need_core()
    table = load_table()
    step = table["meta"]["affinity"]["drift_per_floor"]
    if a.floor < 1:
        raise GMError("--floor must be >= 1")
    session = _clean(a.session or "", 60)

    def fn(data):
        res, entries = [], []
        for pid, p in data["players"].items():
            if p["last_drift_floor"] >= a.floor:  # already drifted for this floor (or a later one): idempotent
                res.append({"player_id": pid, "applied": False, "affinity": p["affinity"]})
                continue
            before = p["affinity"]
            move = min(step, abs(before)) * (-1 if before > 0 else 1)
            p["affinity"] = before + move
            p["last_drift_floor"] = a.floor
            res.append({"player_id": pid, "applied": True, "delta": move, "affinity": p["affinity"]})
            if move:
                entries.append({"ts": core.now_iso(), "session": session, "floor": a.floor, "scene": "", "player_id": pid, "kind": "drift",
                                "raw_delta": move, "delta": move, "reason": f"floor {a.floor} drift toward 0", "evidence": "",
                                "fixation_id": None, "matched_trigger": "", "affinity_before": before, "affinity_after": p["affinity"],
                                "capped": False})
        return data, res, entries
    res = _affinity_mutate(table, fn)
    lines = [f"[GM-ONLY] drift for floor {a.floor}:"]
    for r in res:
        if not r["applied"]:
            lines.append(f"  {r['player_id']}: already drifted for floor >= {a.floor} (no change)")
        else:
            lines.append(f"  {r['player_id']}: {r['delta']:+d} -> {r['affinity']:+d}" if r["delta"] else f"  {r['player_id']}: at 0, no change")
    return {"warning": GM_BANNER, "floor": a.floor, "players": res}, "\n".join(lines)


def cmd_aff_status(a):
    _need_core()
    table = load_table()
    data = _read_affinity(table)
    cap = table["meta"]["affinity"]["scene_cap"]
    ids = [_find_player(data, a.player_id)] if a.player_id else list(data["players"])
    rows = []
    for pid in ids:
        p = data["players"][pid]
        rows.append({"player_id": pid, "display_name": p["display_name"], "character": p["character"], "affinity": p["affinity"],
                     "band": band_for(table, p["affinity"])["name"], "scene_id": p["scene_id"], "scene_delta": p["scene_delta"],
                     "last_drift_floor": p["last_drift_floor"], "flags": p["flags"]})
    lines = [GM_BANNER]
    for r in rows:
        lines.append(f"{r['player_id']} ({r['character']}): affinity {r['affinity']:+d} [{r['band']}] | scene '{r['scene_id']}' delta {r['scene_delta']:+d}/{cap}"
                     f" | last drift floor {r['last_drift_floor']}" + (f" | flags {','.join(r['flags'])}" if r["flags"] else ""))
    if not rows:
        lines.append("(no players registered)")
    return {"warning": GM_BANNER, "players": rows}, "\n".join(lines)


def cmd_aff_new_scene(a):
    _need_core()
    table = load_table()
    scene = _clean(a.scene_id, 60)
    if not scene:
        raise GMError("scene id must not be empty")

    def fn(data):
        reset, same = [], []
        for pid, p in data["players"].items():
            if p["scene_id"] == scene:
                same.append(pid)  # calling again with the current scene id must not reopen the cap
            else:
                p["scene_id"], p["scene_delta"] = scene, 0
                reset.append(pid)
        return data, {"scene": scene, "reset": reset, "unchanged": same}, []
    res = _affinity_mutate(table, fn)
    return {"ok": True, **res}, (f"[GM-ONLY] scene '{scene}': scene deltas reset for {len(res['reset'])} player(s)"
                                  + (f"; {len(res['unchanged'])} already in this scene (kept)" if res["unchanged"] else ""))


# --------------------------------------------------------------------------- CLI wiring

def add_parsers(sub, common):
    """Register `gm-quirks`, `affinity` and `show-gm` on state.py's subparsers."""
    def leaf(parent_sub, name, fn, help_, bind_json=True):
        sp = parent_sub.add_parser(name, help=help_, parents=[common] if bind_json else [])
        sp.set_defaults(fn=fn)
        return sp

    def affinity_commands(asub):
        sp = leaf(asub, "register", cmd_aff_register, "register a player (defaults from state.json crawlers) or --from-state for all")
        sp.add_argument("player_id", nargs="?", help="lowercase id = slug of the crawler's player name in state.json (e.g. caleb)")
        sp.add_argument("--name", help="display name (default: crawler's player)")
        sp.add_argument("--character", help="character name (default: the crawler's name)")
        sp.add_argument("--floor", type=int, help="floor to treat as already drifted (default: state.json current_floor, else 0)")
        sp.add_argument("--from-state", action="store_true", help="register every crawler's player from state.json (idempotent)")
        sp = leaf(asub, "add", cmd_aff_add, "score a player: affinity add <player_id> <delta> --reason ... --scene S --floor N --session X")
        sp.add_argument("player_id")
        sp.add_argument("delta", type=int, help="-10..+10 (usual +/-1..3); the scene net is clamped to +/-3")
        sp.add_argument("--reason", required=True, help="REQUIRED short reason")
        sp.add_argument("--evidence", help="quote (<= 25 words) or short description of the action")
        sp.add_argument("--fixation-id", help="FX-NN (must match the sealed fixation)")
        sp.add_argument("--trigger", help="the matched trigger keyword/theme")
        sp.add_argument("--scene", required=True)
        sp.add_argument("--floor", type=int, required=True)
        sp.add_argument("--session", required=True)
        sp = leaf(asub, "drift", cmd_aff_drift, "once per floor: every score moves 1 toward 0 (idempotent per floor)")
        sp.add_argument("--floor", type=int, required=True)
        sp.add_argument("--session")
        sp = leaf(asub, "status", cmd_aff_status, "show affinity, band and scene delta (GM-only)")
        sp.add_argument("player_id", nargs="?")
        sp = leaf(asub, "new-scene", cmd_aff_new_scene, "start a scene: reset every player's scene delta")
        sp.add_argument("scene_id")

    gq = sub.add_parser("gm-quirks", help="GM-only secret traits: roll | show-gm | verify | status | level | reveal | affinity ...")
    gsub = gq.add_subparsers(dest="gm_cmd", required=True, metavar="SUBCOMMAND")
    sp = leaf(gsub, "roll", cmd_gm_roll, "roll + seal the GM's secret traits ONCE (prints only a neutral confirmation)")
    sp.add_argument("--force", action="store_true", help=f"with --i-know-this-reveals: replace an existing roll (old one is archived)")
    sp.add_argument("--i-know-this-reveals", action="store_true")
    sp.add_argument("--campaign-id", help="override the derived campaign id")
    sp = leaf(gsub, "show-gm", cmd_show_gm, "GM-ONLY: print the sealed traits (warning banner)")
    sp.add_argument("--level", type=int, help="print only the tells for this level 0..5 (adds the generic tell table)")
    leaf(gsub, "verify", cmd_gm_verify, "recompute the commitment hash from the sealed roll + nonce (prints no traits)")
    leaf(gsub, "status", cmd_gm_status, "public: is it rolled, when, and the commitment hash")
    sp = leaf(gsub, "level", cmd_level, "effective degeneration level + glitch d20 max for a floor (public)")
    sp.add_argument("floor", type=int)
    sp.add_argument("--stress", type=int, default=0, choices=[-1, 0, 1])
    sp = leaf(gsub, "guess", cmd_guess, "Busted call: prints only 'Busted' or 'Not busted' (one call per crawler per scene)")
    sp.add_argument("--crawler", required=True)
    sp.add_argument("--floor", type=int, required=True)
    sp.add_argument("--scene", required=True, help="scene id: one call per crawler per scene")
    sp.add_argument("--kind", required=True, help="fixation | quirk | tic | tell | prior-installation")
    sp.add_argument("--trigger", required=True, help="the player's call, in their own words")
    sp = leaf(gsub, "reveal", cmd_reveal, "FINALE: mark revealed and print the roll + nonce")
    sp.add_argument("--i-know-this-reveals", action="store_true")
    gaff = gsub.add_parser("affinity", help="same as top-level `affinity`")
    affinity_commands(gaff.add_subparsers(dest="aff_cmd", required=True, metavar="SUBCOMMAND"))

    aff = sub.add_parser("affinity", help="GM-only per-player Affinity: register | add | drift | status | new-scene")
    affinity_commands(aff.add_subparsers(dest="aff_cmd", required=True, metavar="SUBCOMMAND"))

    leaf(sub, "show-gm", cmd_show_gm, "GM-ONLY alias of `gm-quirks show-gm`").add_argument("--level", type=int)


if __name__ == "__main__":  # python3 tools/gm_quirks.py guess --crawler X ...  (goes through state.py for locking and paths)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import state as _state
    raise SystemExit(_state.main(["gm-quirks"] + sys.argv[1:]))
