"""Loot deck draws (rules/40-loot-deck-spec-5e.md) for `state.py loot draw|totals|show`.

Decks: <campaign>/tables/loot-decks/*.json whose wrapper schema starts with "loot-deck/" (anything else, e.g. an achievements file,
is skipped). A draw loads the zone's deck plus the floor's `any` deck. Random draws only use cards with draw_weight > 0, never
needs-verify stubs, never Legendary/Celestial; weight-0, Legendary and Celestial cards are hand-pick only (--pick <card_id>).
Legendary one-offs are Story Boxes (state.py `loot story-box`; rules/40 section 2.8). They are NOT bound (lootable, transferable, sellable), capped one box per FLOOR (limits.legendary_cap_per_floor, default 1,
--override-cap "<reason>" to exceed), awarded in two steps (award records the deed, open needs a safe room), and their credit_value is
recorded as story_value (provenance), never as economy value and never auto-credited. A sale pays the card's sale_value x the floor multiplier."""
import glob
import json
import os
import re
import sys

import ledgers
import roll as rolltool

RNG = None  # tests may inject a random.Random
HAND_PICK_ONLY_TIERS = ("legendary", "celestial")
CATEGORY_MAP = {"Weapons": "weapons", "Armor": "armor", "Consumables": "gear", "Keys": "gear", "Misc": "magic"}


class LootError(Exception):
    pass


def decks_dir():
    return os.path.join(os.environ.get("DCC_CAMPAIGN_DIR") or "/workspace/dcc-campaign", "tables", "loot-decks")


def norm_zone(z):
    z = str(z or "").strip().lower()
    m = re.match(r"^z?(\d+)", z)
    return f"z{int(m.group(1)):02d}" if m else z


def is_stub(card):
    """A needs-verify placeholder: never drawn, even by hand-pick."""
    blob = " ".join(str(card.get(k, "")) for k in ("real_5e_name", "canon_status", "source_5e", "notes", "reskin_name")).upper()
    return bool(card.get("needs_verify")) or "NEEDS-VERIFY" in blob or "NEEDS VERIFY" in blob or card.get("stub") is True


def load_decks(floor, zone, directory=None):
    """-> (decks, skipped_files). Only loot-deck/* wrappers for this floor and the zone or `any`."""
    decks, skipped = [], []
    zone = norm_zone(zone)
    for f in sorted(glob.glob(os.path.join(directory or decks_dir(), "*.json"))):
        try:
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            skipped.append(os.path.basename(f))
            continue
        if not (isinstance(d, dict) and str(d.get("schema", "")).startswith("loot-deck/") and isinstance(d.get("cards"), list)):
            skipped.append(os.path.basename(f))
            continue
        if d.get("floor") == floor and norm_zone(d.get("zone")) in (zone, "any"):
            decks.append(d)
    return decks, skipped


def _cards(decks):
    for d in decks:
        for c in d["cards"]:
            if isinstance(c, dict) and c.get("id"):
                yield d, c


def _norm_tier(t):
    return str(t or "").strip().lower()


def eligible(decks, *, crawler, floor, ledger, tier=None, pull_type=None, box_type=None):
    """The random-draw pool: [(deck, card)]."""
    drawn_ids = {e.get("card_id") for e in ledger}
    mine_this_floor = {e.get("card_id") for e in ledger if e.get("crawler") == crawler and e.get("floor") == floor}
    pool = []
    for d, c in _cards(decks):
        if not (isinstance(c.get("draw_weight"), (int, float)) and c["draw_weight"] > 0) or is_stub(c):
            continue
        t = _norm_tier(c.get("tier"))
        if t in HAND_PICK_ONLY_TIERS or (tier and t != _norm_tier(tier)):
            continue
        if pull_type and c.get("pull_type") != pull_type:
            continue
        bt = c.get("box_types") or ["any"]
        if "any" not in bt and (not box_type or box_type not in bt):
            continue
        if c.get("exclusive_to") and _norm_tier(c["exclusive_to"]) != _norm_tier(crawler):
            continue
        if c.get("unique") and c["id"] in drawn_ids:
            continue
        if c.get("kind") not in ("consumable", "credits", "junk") and c["id"] in mine_this_floor:
            continue  # same non-consumable twice to one crawler on one floor
        pool.append((d, c))
    return pool


def weighted_pick(pool, crawler, rng=None):
    """Roll d<sum of weights> with roll.py (logged) and walk the cumulative weights."""
    total = int(sum(c["draw_weight"] for _, c in pool))
    if total <= 1 or len(pool) == 1:
        return pool[0], None
    r = rolltool.roll(f"d{total}", label="Loot draw", who=crawler, rng=rng or RNG)
    n = r["total"]
    acc = 0
    for item in pool:
        acc += int(item[1]["draw_weight"])
        if n <= acc:
            return item, n
    return pool[-1], n


def credits_amount(card, rng=None):
    g = card.get("grant") or {}
    if isinstance(g.get("credits"), int):
        return g["credits"], None
    expr = g.get("roll")
    if expr:
        m = re.match(r"^(\d*d\d+)\s*x\s*(\d+)$", expr.replace(",", ""), re.I)
        base, mult = (m.group(1), int(m.group(2))) if m else (expr, 1)
        r = rolltool.roll(base, label=f"Loot credits {card['id']}", who=None, rng=rng or RNG)
        return r["total"] * mult, expr
    return int(card.get("credit_value") or 0), None


INFLATION_FLAG = 1500  # rules/40 section 3.2 audit hint: economy credit_value per crawler per floor on F1-2; story_value is excluded; also the fallback for every floor


# --- per-floor flag line (Syndicate ruling): rules/70-encounter-budget-5e.json is the source of truth. Floors 1-2 stay 1,500; Floor 3+ = 2.165 x expected counted income
# rounded to the nearest 500, which the file records per floor. Read order: (1) a per-floor flag map added in v0.1.5 or later (key name found by name, see _find_flag_map),
# (2) proposed_floor_growth_curve.table[].flag_line (v0.1.4), (3) 1,500 with a note (never an error).
BUDGET_REL = os.path.join("rules", "70-encounter-budget-5e.json")
FLAG_MAP_KEYS = ("flag_lines", "flag_line_by_floor", "flag_lines_by_floor", "flag_by_floor", "per_floor_flag", "per_floor_flags", "per_floor_flag_lines", "floor_flag_lines", "flag_map")
FLAG_VALUE_KEYS = ("flag_line", "flag", "line", "value")


def budget_path():
    return os.path.join(os.environ.get("DCC_CAMPAIGN_DIR") or "/workspace/dcc-campaign", BUDGET_REL)


def _floor_of(key):
    m = re.search(r"(\d+)$", str(key).strip())
    return int(m.group(1)) if m else None


def _flag_value(v):
    if isinstance(v, dict):
        for k in FLAG_VALUE_KEYS:
            if k in v:
                return _flag_value(v[k])
        return None
    return int(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 else None


def _parse_flag_map(m):
    out = {}
    if isinstance(m, dict):
        items = list(m.items())
    elif isinstance(m, list):
        items = [(r.get("floor"), r) for r in m if isinstance(r, dict) and r.get("floor") is not None]
    else:
        return out
    for k, v in items:
        f, val = _floor_of(k), _flag_value(v)
        if f is not None and 1 <= f <= 18 and val:
            out[f] = val
    return out


def _find_flag_map(d):
    """(path, {floor: value}) of a per-floor flag map in the budget file (v0.1.5+), or (None, {}). Tries the likely names under the top level, economy_audit and
    proposed_floor_growth_curve first, then any key containing 'flag' (skipping the v0.1.4 table rows) whose value looks like a floor-keyed map."""
    for base_name, base in (("", d), ("economy_audit", d.get("economy_audit")), ("proposed_floor_growth_curve", d.get("proposed_floor_growth_curve")),
                            ("economy_audit.governor", (d.get("economy_audit") or {}).get("governor") if isinstance(d.get("economy_audit"), dict) else None)):
        if isinstance(base, dict):
            for k in FLAG_MAP_KEYS:
                m = _parse_flag_map(base.get(k))
                if len(m) >= 2:
                    return (base_name + "." if base_name else "") + k, m
    found = []

    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                p = f"{path}.{k}" if path else k
                if "flag" in str(k).lower() and isinstance(v, (dict, list)) and not p.startswith("proposed_floor_growth_curve.table"):
                    m = _parse_flag_map(v)
                    if len(m) >= 2:
                        found.append((p, m))
                        continue
                walk(v, p)
        elif isinstance(o, list) and not path.startswith("proposed_floor_growth_curve.table"):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]")
    walk(d, "")
    return found[0] if found else (None, {})


class FlagLines:
    """Per-floor inflation flag lines read from the budget file. Never raises: a missing/unreadable file or key means 1,500 (INFLATION_FLAG) plus a note for Floor 3+."""

    def __init__(self, path=None):
        self.map, self.source, self.version, self.problem = {}, None, None, None
        path = path or budget_path()
        try:
            with open(path, encoding="utf-8") as f:
                d = json.load(f)
        except FileNotFoundError:
            self.problem = "budget file rules/70-encounter-budget-5e.json not found"
            return
        except (OSError, ValueError) as e:
            self.problem = f"budget file unreadable ({type(e).__name__})"
            return
        if not isinstance(d, dict):
            self.problem = "budget file is not a JSON object"
            return
        self.version = d.get("version")
        key, m = _find_flag_map(d)
        if m:
            self.map, self.source = m, f"{key} (v{self.version})"
        else:
            tbl = (d.get("proposed_floor_growth_curve") or {}).get("table") if isinstance(d.get("proposed_floor_growth_curve"), dict) else None
            m = _parse_flag_map(tbl)
            if m:
                self.map, self.source = m, f"proposed_floor_growth_curve.table[].flag_line (v{self.version})"
            else:
                self.problem = "no per-floor flag line found in the budget file"

    def line(self, floor):
        """(value, note_or_None). Floor 1-2 without a file value is a silent 1,500; Floor 3+ without one is 1,500 plus a note."""
        if isinstance(floor, int) and floor in self.map:
            return self.map[floor], None
        if isinstance(floor, int) and floor >= 3:
            return INFLATION_FLAG, f"F{floor}: no flag line in the budget file ({self.problem or 'floor missing from its flag map'}); using the default {INFLATION_FLAG:,} credits, which is not floor-scaled"
        return INFLATION_FLAG, None

    def footer(self, floors):
        """Lines naming the flag line used for each Floor 3+ shown (nothing for Floor 1-2, so their output is unchanged)."""
        fl = sorted({f for f in floors if isinstance(f, int) and f >= 3})
        if not fl:
            return []
        out = []
        used = [f for f in fl if f in self.map]
        if used:
            out.append("FLAG LINES in use (credits per Crawler for the floor, source " + (self.source or "?") + "): " + ", ".join(f"F{f} {self.map[f]:,}" for f in used))
        out += ["NOTE: " + self.line(f)[1] for f in fl if f not in self.map]
        return out


def deed_key(text):
    """Normalised deed id used by the story-box registry: lower-case words joined by '-'."""
    return re.sub(r"[^a-z0-9]+", "-", str(text or "").lower()).strip("-")


def hold_note(card):
    """The HOLD line a deck author left in `notes` (e.g. Lore's 'HOLD (Lore): ...'), or None. Surfaced as a warning, never blocks."""
    m = re.search(r"\bHOLD\b.*", str(card.get("notes") or ""), re.S)
    return m.group(0).strip()[:300] if m else None


def story_value_of(card):
    """Story Box worth: `story_value`, falling back to `credit_value` for decks that predate the field. Never spendable."""
    return card.get("story_value") if card.get("story_value") else (card.get("credit_value") or 0)


def story_warnings(card):
    w = []
    if not re.search(r"power_note\s*:", str(card.get("notes") or ""), re.I):
        w.append("card has no power note (no 'power_note:' in notes): the Accountant cannot judge how strong it is for the floor")
    if not re.search(r"trigger_deed\s*:", str(card.get("notes") or ""), re.I):
        w.append("card has no trigger_deed: line in its notes, so nothing says what deed it is for")
    if not str((card.get("plain_mechanics") or {}).get("text") or "").strip():
        w.append("card states no effect (plain_mechanics.text is empty): the player would get an item with no stated effect")
    h = hold_note(card)
    if h:
        w.append(f"deck note says: {h}")
    return w


def legendary_count(ledger, floor, story_ledger=None):
    """Story Boxes on this floor held by LIVING Crawlers. Cards awarded together share a box_id and count once. Counts the deed registry
    (award step, so an unopened box counts) and the loot ledger (older entries without a registry line count each). A box with a `released`
    event (its holder's Crawler was deleted) no longer counts: archived rows are audit-only."""
    released = {e.get("box_id") for e in story_ledger or [] if e.get("event") in ("released", "reclaimed")}
    boxes, n = set(), 0
    for e in story_ledger or []:
        if e.get("event") == "awarded" and e.get("floor") == floor and e.get("box_id") and e["box_id"] not in released:
            boxes.add(e["box_id"])
    for e in ledger:
        if _norm_tier(e.get("tier")) == "legendary" and e.get("floor") == floor:
            if e.get("box_id"):
                if e["box_id"] not in released:
                    boxes.add(e["box_id"])
            else:
                n += 1
    return n + len(boxes)


DEFAULT_SALE_VALUE = 500  # System buyback of a Story Box item when the card has no sale_value (Floor-1 scale)


def floor_multiplier(floor):
    """Credit multiplier by floor (rules/10 section 3.9): x1 F1-4, x5 F5-9, x20 F10-14, x50 F15+."""
    f = int(floor)
    return 1 if f <= 4 else 5 if f <= 9 else 20 if f <= 14 else 50


def sale_value_of(card):
    v = card.get("sale_value")
    return v if isinstance(v, int) and not isinstance(v, bool) and v > 0 else DEFAULT_SALE_VALUE


def item_row(card):
    pm = card.get("plain_mechanics") or {}
    uses = pm.get("uses") if isinstance(pm.get("uses"), dict) else None
    row = {"name": card["reskin_name"], "qty": 1, "notes": card.get("real_5e_name", ""),
           "mechanics": pm.get("text") or "", "category": CATEGORY_MAP.get(card.get("category"), "gear")}
    if uses and isinstance(uses.get("max"), int):
        row["uses"] = uses["max"]
        row["uses_max"] = uses["max"]
    return row


def totals(ledger, crawler=None, floor=None):
    """{crawler: {floor: {economy, story, items, legendary}}} plus grand totals. Economy excludes Legendary and story values."""
    out = {}
    for e in ledger:
        if crawler and (e.get("crawler") or "").lower() != crawler.lower():
            continue
        if floor is not None and e.get("floor") != floor:
            continue
        slot = out.setdefault(e["crawler"], {}).setdefault(e.get("floor"), {"economy_value": 0, "story_value": 0, "draws": 0, "legendary": 0})
        slot["draws"] += 1
        slot["economy_value"] += e.get("economy_value") or 0
        slot["story_value"] += e.get("story_value") or 0
        slot["legendary"] += 1 if _norm_tier(e.get("tier")) == "legendary" else 0
    return out


# --- optional all-in view (Q-003 / budget A12 + Q5): boxes + Story Box sale proceeds + credits earned outside boxes (encounter payouts, R1 toast credits).
# Off unless `loot totals --include-credits` is used; the default output is unchanged. Credits are always called credits.
CREDIT_SOURCES = ("encounter", "achievement", "toast", "r1")   # credit-ledger `source` values that count as earned credits; `box` is excluded (box value already counts it)
VALVE_FLOOR, VALVE_AT, VALVE_CARD_MAX = 2, 900, 175            # rules/70-encounter-budget-5e.md A12: Floor 2 Boss Box hand-pick when the running total reaches 900 (cards worth 175 or less)


def credit_income(entries, sources=CREDIT_SOURCES, crawler=None, floor=None, assume_floor=None):
    """{crawler: {floor_or_None: credits}}: positive credit-ledger deltas whose source is in `sources`. The floor is the entry's own `floor` field (record it with
    `state.py credits ... --floor N`); entries with none go to `assume_floor` if given, else to the None bucket (floor not recorded). Spending (negative deltas), sales,
    transfers, body loot, write-offs, intake credits and box pulls (already in box value) are never counted here."""
    want = {s.strip().lower() for s in sources}
    out = {}
    for e in entries:
        if not isinstance(e, dict) or (e.get("source") or "").strip().lower() not in want:
            continue
        d = e.get("delta")
        if not isinstance(d, int) or isinstance(d, bool) or d <= 0:
            continue
        if crawler and (e.get("crawler") or "").lower() != crawler.lower():
            continue
        fl = e.get("floor") if isinstance(e.get("floor"), int) else assume_floor
        if floor is not None and fl != floor:
            continue
        slot = out.setdefault(e["crawler"], {})
        slot[fl] = slot.get(fl, 0) + d
    return out


def all_in(t, sales, income):
    """{crawler: {floor: {boxes, sale_proceeds, earned_credits, all_in}}} from the box totals, Story Box sales and credit_income()."""
    proceeds = sale_proceeds(sales)
    keys = set()
    for c, fl in t.items():
        keys |= {(c, f) for f in fl}
    for c, fl in income.items():
        keys |= {(c, f) for f in fl}
    out = {}
    for c, f in keys:
        b = (t.get(c, {}).get(f) or {}).get("economy_value", 0)
        p = proceeds.get((c, f), 0)
        i = income.get(c, {}).get(f, 0)
        out.setdefault(c, {})[f] = {"boxes": b, "sale_proceeds": p, "earned_credits": i, "all_in": b + p + i}
    return out


def a_floors(a):
    return {f for fl in a.values() for f in fl}


def all_in_text(a, sources, flags=None, footer=True):
    flags = flags or FlagLines()
    lines = ["ALL-IN credits per Crawler per floor (boxes + Story Box sale proceeds + earned credits from sources: " + ", ".join(sources) + "):"]
    unassigned = 0
    for c, floors in sorted(a.items()):
        for fl, v in sorted(floors.items(), key=lambda kv: (kv[0] is None, kv[0])):
            if fl is None:
                unassigned += v["earned_credits"]
            lines.append(f"- {c} " + floor_label(fl) + f": boxes {v['boxes']:g} + sale proceeds {v['sale_proceeds']:g} + earned credits {v['earned_credits']:g} = all-in {v['all_in']:g}")
            limit = flags.line(fl)[0]
            if v["all_in"] > limit:
                lines.append(f"FLAG: {c} {floor_label(fl)} all-in {v['all_in']:g} is over {limit:,} credits for the floor")
            if fl == VALVE_FLOOR:
                lines.append(f"VALVE (optional, A12): {c} {floor_label(fl)} all-in {v['all_in']:g} " + (f"has reached {VALVE_AT}: the GM may hand-pick the Boss Box from cards worth {VALVE_CARD_MAX} or less" if v["all_in"] >= VALVE_AT else f"is below {VALVE_AT}: no valve"))
    if unassigned:
        lines.append(f"NOTE: {unassigned:g} earned credits have no floor recorded; pass --assume-floor N, or record --floor N on `credits` from now on")
    if footer:
        lines += flags.footer(a_floors(a))
    return "\n".join(lines)


def floor_label(fl):
    """'F3' for a floor, 'no floor set' when none was recorded (never 'FNone')."""
    return f"F{fl}" if fl is not None else "no floor set"


def sale_proceeds(sales):
    """{(crawler, floor): credits} from Story Box SALES to the System only. A priced Crawler-to-Crawler transfer moves credits between players; it is never income."""
    out = {}
    for e in sales:
        if e.get("event") != "sold":
            continue
        k = (e.get("crawler"), e.get("floor"))
        out[k] = out.get(k, 0) + (e.get("price") or 0)
    return out


def totals_text(t, sales=(), flags=None, footer=True):
    flags = flags or FlagLines()
    if not t and not sales:
        return "no loot draws recorded"
    story = any(v["story_value"] or v["legendary"] for fl in t.values() for v in fl.values())
    lines = ["crawler / floor: economy value | story value (provenance, NOT economy) | draws" if story else "crawler / floor: economy value | draws"]
    ge = gs = 0
    for c, floors in sorted(t.items()):
        for fl, v in sorted(floors.items(), key=lambda kv: (kv[0] is None, kv[0])):
            lines.append(f"- {c} {floor_label(fl)}: economy {v['economy_value']:g} | " + (f"story {v['story_value']:g} | " if story else "") + f"{v['draws']} draw(s)" + (f" ({v['legendary']} Legendary)" if v["legendary"] else ""))
            ge += v["economy_value"]
            gs += v["story_value"]
    proceeds = sale_proceeds(sales)
    for c, floors in sorted(t.items()):
        for fl, v in sorted(floors.items(), key=lambda kv: (kv[0] is None, kv[0])):
            pr = proceeds.get((c, fl), 0)
            limit = flags.line(fl)[0]
            if v["economy_value"] + pr > limit:
                lines.append(f"FLAG: {c} {floor_label(fl)} economy value {v['economy_value']:g}" + (f" + {pr:g} Story Box sale proceeds" if pr else "") + f" is over {limit:,} (the award's story value is excluded; sale proceeds count)")
    for e in sales:
        lines.append(f"FLAG: {e.get('crawler')} " + ("sold" if e.get("event") == "sold" else f"transferred (for {e.get('price', 0)} credits) to {e.get('to')}") +
                     f" Story Box item {e.get('item')} on {floor_label(e.get('floor'))}: " + (f"{e.get('price', 0)} credits received" if e.get("event") == "sold" else f"{e.get('price', 0)} credits changed hands between Crawlers, NOT counted as income (a transfer is not a sale)") + f", story value {e.get('story_value', 0):g} is provenance only and was NOT credited ({e.get('reason', '')})")
    lines.append(f"TOTAL economy {ge:g} (what the Accountant audits)" + (f" | story {gs:g} (reported separately)" if story else ""))
    if footer:
        lines += flags.footer({fl for floors in t.values() for fl in floors})
    return "\n".join(lines)


def log_line(e):
    val = f"story {e['story_value']:g}" if e.get("story_value") else f"value {e.get('economy_value', 0):g}"
    return f"LOOT | {e['crawler']} | F{int(e['floor']):02d}/{e['zone']} | {e['card_id']} | {e['tier']} | {e['kind']} | {val} | {e.get('text', '')}"


def err(msg):
    raise LootError(msg)


if __name__ == "__main__":  # pragma: no cover
    print(__doc__)
    sys.exit(0)
