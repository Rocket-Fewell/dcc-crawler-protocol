"""Room-card checks. Matches engine-design/03-room-card-format.md."""

from __future__ import annotations

EXIT_KINDS = ("door", "vent", "stairs")
TRIGGERS = ("on_enter", "on_search", "clock", "noise")
SECRET_TYPES = ("check", "item", "action", "clock")


def snapshot_text(room):
    parts = [room.get("narrator_line") or ""]
    parts.extend(map_lines(room))
    return " ".join(part for part in parts if part)


def narration_tokens(room):
    """Rough tokens for the narrator snapshot: characters divided by 4."""
    text = snapshot_text(room)
    if not text.strip():
        return 0
    return (len(text) + 3) // 4


def ends_sentence(text):
    stripped = (text or "").strip()
    return bool(stripped) and stripped[-1] in ".!?"


def map_lines(room):
    mapping = room.get("map") or {}
    lines = []
    for key in ("layout", "cover", "hazards", "extra"):
        val = mapping.get(key)
        if isinstance(val, list):
            lines.extend(str(x) for x in val if str(x).strip())
        elif val and str(val).strip():
            lines.append(str(val))
    return lines


def check_encounter(enc, where):
    errs = []
    if enc.get("trigger") not in TRIGGERS:
        errs.append("%s trigger invalid" % where)
    if not enc.get("enc_id"):
        errs.append("%s missing enc_id" % where)
    return errs


def check_room(room, where):
    errs = []
    for key in ("id", "floor", "zone", "name", "days_open", "narrator_line", "read_aloud",
                "positions", "map", "exits", "encounters", "secrets", "loot", "npcs",
                "voice_lines", "rest", "gm_notes", "flags", "source"):
        if key not in room:
            errs.append("%s missing %s" % (where, key))
    if not isinstance(room.get("days_open"), list) or not room.get("days_open"):
        errs.append("%s days_open must be a non-empty list" % where)
    if room.get("narrator_line") and not ends_sentence(room.get("narrator_line")):
        errs.append("%s narrator_line does not end a sentence" % where)
    if room.get("read_aloud") and not ends_sentence(room.get("read_aloud")):
        errs.append("%s read_aloud does not end a sentence" % where)
    if not isinstance(room.get("positions"), list):
        errs.append("%s positions must be a list" % where)
    else:
        for i, pos in enumerate(room.get("positions") or []):
            if not isinstance(pos, dict) or not pos.get("id") or not pos.get("name"):
                errs.append("%s position %d needs id and name" % (where, i))
    if room.get("rest") is not None and not isinstance(room.get("rest"), dict):
        errs.append("%s rest must be null or an object" % where)
    lines = map_lines(room)
    if len(lines) > 4:
        errs.append("%s map has %d lines (max 4)" % (where, len(lines)))
    for i, line in enumerate(lines):
        if not ends_sentence(line):
            errs.append("%s map line %d does not end a sentence" % (where, i))
    if narration_tokens(room) > 150:
        errs.append("%s narration snapshot is over 150 tokens" % where)
    for i, ex in enumerate(room.get("exits") or []):
        if ex.get("kind") not in EXIT_KINDS:
            errs.append("%s exit %d kind must be door, vent, or stairs" % (where, i))
        if not ex.get("to"):
            errs.append("%s exit %d missing to" % (where, i))
    for i, enc in enumerate(room.get("encounters") or []):
        errs.extend(check_encounter(enc, "%s encounter %d" % (where, i)))
    for i, enc in enumerate(room.get("day_encounters") or []):
        errs.extend(check_encounter(enc, "%s day_encounter %d" % (where, i)))
    for i, sec in enumerate(room.get("secrets") or []):
        trigs = sec.get("triggers") if isinstance(sec.get("triggers"), list) else []
        if sec.get("trigger"):
            trigs = [sec["trigger"]] + [t for t in trigs if t is not sec.get("trigger")]
        if not trigs:
            errs.append("%s secret %d missing trigger" % (where, i))
        for trig in trigs:
            if not isinstance(trig, dict) or trig.get("type") not in SECRET_TYPES:
                errs.append("%s secret %d trigger type invalid" % (where, i))
        if not sec.get("reveal_text"):
            errs.append("%s secret %d missing reveal_text" % (where, i))
        if "gm_note" in sec and not isinstance(sec.get("gm_note"), str):
            errs.append("%s secret %d gm_note must be a string" % (where, i))
    voices = room.get("voice_lines") or {}
    for key in ("intro", "twist", "win"):
        if key not in voices:
            errs.append("%s voice_lines missing %s" % (where, key))
        elif isinstance(voices.get(key), str) and voices.get(key) and not ends_sentence(voices.get(key)):
            errs.append("%s voice_lines.%s does not end a sentence" % (where, key))
    flags = room.get("flags") or {}
    for key in ("cleared", "looted", "rested"):
        if key not in flags:
            errs.append("%s flags missing %s" % (where, key))
    src = room.get("source") or {}
    if not src.get("spec") or not src.get("enc_id"):
        errs.append("%s source needs spec and enc_id" % where)
    return errs


def check_stat(block, where):
    errs = []
    for key in ("id", "name", "ac", "hp", "attacks"):
        if key not in block:
            errs.append("%s missing %s" % (where, key))
    attacks = block.get("attacks") or []
    if not attacks:
        errs.append("%s needs one attack" % where)
    bonuses = []
    for atk in attacks:
        if "to_hit" not in atk or "damage" not in atk:
            errs.append("%s attack missing to_hit or damage" % where)
        else:
            bonuses.append(int(atk["to_hit"]))
    if bonuses and len(set(bonuses)) != 1:
        errs.append("%s has more than one to-hit" % where)
    return errs
