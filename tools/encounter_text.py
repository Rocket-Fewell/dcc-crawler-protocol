#!/usr/bin/env python3
"""encounter_text.py - print the player text (default) or GM-only notes of a Floor day page.

Read-only, offline. Reads ONLY floors/fNN/day-NN.json (never gm-notes/secret/, sessions/ or the network).
Player text = exactly the blocks named in audience_manifest.player_blocks (block[entry.field] only), with the
same selection rules as the Discord /encounter command (discord-voice-bridge/src/encounter/extract.js):
optional lines need --include-optional, "show_only_when" lines need --confirm, {hours} needs --hours.
System-voice lines get the same **[SYSTEM]** / **[GM]** tags /encounter posts with (decision 032: dry System for clock/fees/notices; achievements and snark are GM).

  python3 tools/encounter_text.py --day 1                       # all player text for Day 1
  python3 tools/encounter_text.py --day 1 --encounter enc-d01-02
  python3 tools/encounter_text.py --day 5 --zone z10 --hours 6
  python3 tools/encounter_text.py --day 1 --list
  python3 tools/encounter_text.py --day 1 --encounter enc-d01-02 --gm   # GM ONLY - never pipe to say
"""
import argparse
import json
import os
import re
import sys

CAMPAIGN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GM_HEADER = "GM ONLY - DO NOT POST"
SYSTEM_TAG, GM_TAG = "**[SYSTEM]** ", "**[GM]** "
# Allow-list only (mirrors extract.js). ONLY system_notice + exit_warning_read_aloud are System.
# voice_line, route_voice_line, gm_narration, gm_color, and unknown kinds → GM. Decision 032 / agreed Oct 5 2026.
# Safety net: kind == "gm_color" OR path ending in "/gm_color" is always GM (even if mis-tagged as system_notice).
SYSTEM_KINDS = {"system_notice", "exit_warning_read_aloud"}
GM_SKIP_KEYS = {"tag", "audience", "audience_default"}   # rendering noise in --gm output


def is_gm_color(e):
    if not isinstance(e, dict):
        return False
    if e.get("kind") == "gm_color":
        return True
    path = str(e.get("path") or "")
    return path == "gm_color" or path.endswith("/gm_color")


def voice_of(e):
    return "gm" if is_gm_color(e) else ("system" if e.get("kind") in SYSTEM_KINDS else "gm")


class Refusal(Exception):
    pass


def warn(msg):
    print(f"encounter_text: {msg}", file=sys.stderr)


def page_path(campaign, floor, day):
    return os.path.join(campaign, "floors", f"f{floor:02d}", f"day-{day:02d}.json")


def load_page(campaign, floor, day):
    """Mirror of extract.js loadPage: range checks, friendly errors, manifest required."""
    if not 1 <= floor <= 18:
        raise Refusal("Floor must be a whole number from 1 to 18.")
    if not 1 <= day <= 5:
        raise Refusal("Day must be a whole number from 1 to 5.")
    path = page_path(campaign, floor, day)
    try:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
    except FileNotFoundError:
        raise Refusal(f"There is no page for Floor {floor} Day {day} ({os.path.relpath(path, campaign)} is missing).")
    except OSError as e:
        raise Refusal(f"Could not read the Floor {floor} Day {day} page ({e.strerror}).")
    try:
        doc = json.loads(raw)
    except ValueError:
        raise Refusal(f"The Floor {floor} Day {day} page is not valid JSON right now (mid-rebuild?).")
    m = doc.get("audience_manifest") if isinstance(doc, dict) else None
    if not isinstance(m, dict) or not isinstance(m.get("player_blocks"), list):
        raise Refusal(f"The Floor {floor} Day {day} page has no audience manifest; nothing on it is safe to show.")
    if "schema" in m and not str(m["schema"]).startswith("audience/"):
        raise Refusal(f"Unrecognised audience manifest schema on Floor {floor} Day {day}.")
    return doc


def resolve(doc, ptr):
    """JSON pointer through own keys only; None when anything is missing."""
    if not isinstance(ptr, str) or not ptr.startswith("/"):
        return None
    o = doc
    for seg in ptr[1:].split("/"):
        seg = seg.replace("~1", "/").replace("~0", "~")
        if isinstance(o, list):
            if not seg.isdigit() or int(seg) >= len(o):
                return None
            o = o[int(seg)]
        elif isinstance(o, dict) and seg in o:
            o = o[seg]
        else:
            return None
    return o


def group_of(doc, e):
    if isinstance(e.get("encounter"), str) and e["encounter"]:
        return e["encounter"]
    m = re.match(r"^/routes/(\d+)(/|$)", e["path"])
    if m:
        routes = doc.get("routes") or []
        i = int(m.group(1))
        rid = routes[i].get("id") if i < len(routes) and isinstance(routes[i], dict) else None
        return rid if isinstance(rid, str) and rid else f"route-{i}"
    return "day"


def entries(doc):
    out = []
    for e in doc["audience_manifest"]["player_blocks"]:
        if isinstance(e, dict) and all(isinstance(e.get(k), str) for k in ("path", "kind", "field")):
            out.append(dict(e, group=group_of(doc, e), voice=voice_of(e)))
    return out


def groups(doc):
    """(id, title, zone) for every encounter and route on the page, plus 'day'."""
    rows = [("day", "Day-level notices", None)]
    for r in doc.get("routes") or []:
        if isinstance(r, dict) and r.get("id"):
            rows.append((r["id"], r.get("name", ""), None))
    for enc in doc.get("encounters") or []:
        if isinstance(enc, dict) and enc.get("id"):
            rows.append((enc["id"], enc.get("name", ""), enc.get("zone")))
    return rows


def norm_zone(z):
    z = str(z).strip().lower()
    z = z[1:] if re.fullmatch(r"z\w+", z) else z
    return z.lstrip("0") or "0" if z.isdigit() else z


def pick_group(doc, want):
    ids = [g[0] for g in groups(doc)]
    hit = next((g for g in ids if g.lower() == want.strip().lower()), None)
    if not hit:
        raise Refusal(f'No encounter or route "{want}" on this page. Available: {", ".join(ids)}.')
    return hit


def zone_ids(doc, zone):
    """Encounter ids in a zone, or None when the page has no zone data (flag ignored)."""
    encs = [e for e in doc.get("encounters") or [] if isinstance(e, dict) and e.get("zone")]
    if not encs:
        warn("this page has no zone data; --zone ignored")
        return None
    ids = {e["id"] for e in encs if norm_zone(e["zone"]) == norm_zone(zone)}
    if not ids:
        raise Refusal(f'No encounter in zone "{zone}". Zones on this page: {", ".join(sorted({e["zone"] for e in encs}))}.')
    return ids


def page_uses_hours(doc):
    for e in entries(doc):
        if "hours" in (e.get("needs_fill") or []):
            return True
    return False


def player_items(doc, scope, hours=None, include_optional=False, confirm=False):
    """Mirror of extract.js buildPreview: returns ([(voice, text)], notes)."""
    items, notes, skipped_opt, waiting = [], [], 0, {}
    for e in entries(doc):
        if not scope(e):
            continue
        need = e.get("needs_fill") if isinstance(e.get("needs_fill"), list) else []
        if "hours" in need and hours is None:
            notes.append(f"skipped {e['path']}: it has an {{hours}} placeholder; re-run with --hours N")
            continue
        other = [n for n in need if n != "hours"]
        if other:
            notes.append(f"skipped {e['path']}: needs {', '.join(map(str, other))}")
            continue
        if e.get("show_only_when") and not confirm:
            k = str(e["show_only_when"])[:140]
            waiting[k] = waiting.get(k, 0) + 1
            continue
        if e.get("optional") is True and not include_optional:
            skipped_opt += 1
            continue
        block = resolve(doc, e["path"])
        value = block.get(e["field"]) if isinstance(block, dict) else None   # ONLY the named field
        texts = []
        if isinstance(value, str):
            texts.append(value)
        elif isinstance(value, list):
            popt = e.get("paragraphs_optional") if isinstance(e.get("paragraphs_optional"), list) else []
            for i, p in enumerate(value):
                t = p if isinstance(p, str) else p.get("text") if isinstance(p, dict) and isinstance(p.get("text"), str) else None
                if t is None:
                    continue
                if ((i < len(popt) and popt[i] is True) or (isinstance(p, dict) and p.get("optional") is True)) and not include_optional:
                    skipped_opt += 1
                    continue
                texts.append(t)
        for t in texts:
            t = t.strip()
            if not t:
                continue
            if hours is not None:
                t = t.replace("{hours}", f"{hours:g}")
            left = re.search(r"\{[A-Za-z_]+\}", t)
            if left:
                notes.append(f"skipped {e['path']}: still has {left.group(0)}")
                continue
            items.append((e["voice"], t))
    if skipped_opt:
        notes.append(f"{skipped_opt} optional line(s) skipped; add --include-optional to show them")
    for cond, n in waiting.items():
        notes.append(f"{n} block(s) held back, shown only when {cond}; add --confirm once true")
    return items, notes


def format_player(items):
    """Same voice tagging as extract.js toMessages: [SYSTEM] on System lines, [GM] on narration when mixed."""
    mixed = any(v == "system" for v, _ in items)
    return "\n\n".join((SYSTEM_TAG if v == "system" else GM_TAG if mixed else "") + t for v, t in items)


def render(o, skip, ptr="", ind=0):
    """Indented plain-text dump of a GM-side object, leaving out every manifest player block."""
    pad, lines = "  " * ind, []
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{ptr}/{k}"
            if k in GM_SKIP_KEYS or p in skip:
                continue
            if isinstance(v, (dict, list)):
                sub = render(v, skip, p, ind + 1)
                if sub:
                    lines += [f"{pad}{k}:"] + sub
            elif v not in (None, ""):
                lines.append(f"{pad}{k}: {v}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            sub = render(v, skip, f"{ptr}/{i}", ind + 1)
            if sub:
                lines.append(f"{pad}- " + sub[0].lstrip())
                lines += sub[1:]
    elif o not in (None, ""):
        lines.append(f"{pad}{o}")
    return lines


def gm_text(doc, floor, day, keep):
    skip = {e["path"] for e in entries(doc)}
    out = [GM_HEADER, f"Floor {floor} Day {day}"]
    sections = []
    if keep("day"):
        sections += [("day", "Day", doc.get("day")), ("stairwell_key", "Stairwell key", doc.get("stairwell_key"))]
    for i, r in enumerate(doc.get("routes") or []):
        if isinstance(r, dict) and keep(r.get("id")):
            sections.append((f"routes/{i}", f"{r.get('id')}: {r.get('name', '')}", r))
    for i, enc in enumerate(doc.get("encounters") or []):
        if isinstance(enc, dict) and keep(enc.get("id")):
            sections.append((f"encounters/{i}", f"{enc.get('id')}: {enc.get('name', '')} ({enc.get('zone', '?')})", enc))
    for ptr, title, obj in sections:
        if obj is None:
            continue
        out += ["", f"== {title} =="] + render(obj, skip, "/" + ptr)
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Player text (default) or GM-only notes of a Floor day page. Read-only, offline.")
    ap.add_argument("--day", type=int, required=True)
    ap.add_argument("--floor", type=int, default=1)
    ap.add_argument("--encounter", help="encounter or route id, or 'day' for the day-level notices (default: everything)")
    ap.add_argument("--zone", help="only encounters in this zone (z06, 6, zS, wandering)")
    ap.add_argument("--hours", type=float, help="in-game hours left; fills {hours} (e.g. the Day 5 collapse notice)")
    ap.add_argument("--include-optional", action="store_true", help="also optional lines (zone colour, optional set-piece paragraphs)")
    ap.add_argument("--confirm", action="store_true", help='the "shown only when" condition is true (e.g. achievement awarded)')
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--gm", action="store_true", help="GM-only notes (never the default; never post)")
    mode.add_argument("--list", action="store_true", help="list encounter and route ids with titles")
    ap.add_argument("--campaign-dir", default=CAMPAIGN, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    try:
        doc = load_page(a.campaign_dir, a.floor, a.day)
        if a.list:
            for gid, title, zone in groups(doc)[1:]:
                print(f"{gid}\t{title}" + (f" ({zone})" if zone else ""))
            return 0
        wanted = pick_group(doc, a.encounter) if a.encounter else None
        zids = zone_ids(doc, a.zone) if a.zone else None
        if a.hours is not None:
            if not 0 <= a.hours <= 24:
                raise Refusal("--hours must be from 0 to 24.")
            if not page_uses_hours(doc):
                warn("this page has no {hours} data; --hours ignored")
                a.hours = None

        def keep(gid):
            return (wanted is None or gid == wanted) and (zids is None or gid in zids)

        if a.gm:
            print(gm_text(doc, a.floor, a.day, keep))
            return 0
        items, notes = player_items(doc, lambda e: keep(e["group"]), a.hours, a.include_optional, a.confirm)
        for n in notes:
            warn(n)
        if not items:
            raise Refusal("Nothing player-facing in that scope.")
        print(format_player(items))
        return 0
    except Refusal as e:
        warn(str(e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
