"""Room-card checks. Matches engine-design/03-room-card-format.md."""

from __future__ import annotations

EXIT_KINDS = ("door", "vent", "stairs")
TRIGGERS = ("on_enter", "on_search", "clock", "noise")
SECRET_TYPES = ("check", "item", "action", "clock")


def narration_tokens(room):
    """Whitespace tokens in the narrator snapshot (narrator line plus map lines)."""
    parts = [room.get("narrator_line") or ""]
    mapping = room.get("map") or {}
    for key in ("layout", "cover", "hazards", "extra"):
        val = mapping.get(key)
        if isinstance(val, list):
            parts.extend(str(x) for x in val)
        elif val:
            parts.append(str(val))
    return len(" ".join(parts).split())


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


def check_room(room, where):
    errs = []
    for key in ("id", "floor", "zone", "name", "days_open", "narrator_line", "map", "exits",
                "encounters", "secrets", "loot", "npcs", "voice_lines", "flags", "source"):
        if key not in room:
            errs.append("%s missing %s" % (where, key))
    if not isinstance(room.get("days_open"), list) or not room.get("days_open"):
        errs.append("%s days_open must be a non-empty list" % where)
    lines = map_lines(room)
    if len(lines) > 4:
        errs.append("%s map has %d lines (max 4)" % (where, len(lines)))
    if narration_tokens(room) > 150:
        errs.append("%s narration snapshot is over 150 tokens" % where)
    for i, ex in enumerate(room.get("exits") or []):
        if ex.get("kind") not in EXIT_KINDS:
            errs.append("%s exit %d kind must be door, vent, or stairs" % (where, i))
        if not ex.get("to"):
            errs.append("%s exit %d missing to" % (where, i))
    for i, enc in enumerate(room.get("encounters") or []):
        if enc.get("trigger") not in TRIGGERS:
            errs.append("%s encounter %d trigger invalid" % (where, i))
        if not enc.get("enc_id"):
            errs.append("%s encounter %d missing enc_id" % (where, i))
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
    flags = room.get("flags") or {}
    for key in ("cleared", "looted", "rested"):
        if key not in flags:
            errs.append("%s flags missing %s" % (where, key))
    voices = room.get("voice_lines") or {}
    for key in ("intro", "twist", "win"):
        if key not in voices:
            errs.append("%s voice_lines missing %s" % (where, key))
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
