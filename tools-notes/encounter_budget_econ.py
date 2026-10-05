#!/usr/bin/env python3
"""Economy check for rules/70-encounter-budget-5e.json (v0.1.1). Read-only: reads tables/loot-decks/f01-*.json, writes nothing
unless you pass an output path. Scratch/audit helper, not a campaign tool.

  python3 tools-notes/encounter_budget_econ.py [out.json] [--n 100000] [--seed 70]

1. analytic(): box-value means derived from the LIVE deck cards (draw_weight > 0, not stub, not Legendary/Celestial, box_types
   'any' or the box's type), the way tools/loot.py eligible() filters them. Pull types from core 4.2 (d100 split 30/25/15/18/10/2).
   Credit cards use their grant roll (3d6x5 Bronze, 2d6x25 Silver) -> mean = card credit_value. Upgrade (99-00) = roll again at
   Silver (ceiling keeps it Silver), so Silver pull mean = sum(p_k * m_k) / 0.98.
   Analytic means are WITH replacement (every card keeps its weight). Consumable "two at one rarity lower" is ignored.
2. simulate(): Monte Carlo of one Crawler's Floor 1 and Floor 2, drawing real cards from the decks. Non-consumable cards already
   drawn by that Crawler on that floor are removed from the pool (loot.py: same non-consumable twice to one crawler per floor).
   Floor 2 reuses the Floor 1 decks (no F2 decks exist yet; assumption A8).
"""
import glob, json, os, random, sys, hashlib, collections

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import dcc_paths as _paths  # noqa: E402
ROOT = os.environ.get("DCC_CAMPAIGN_ROOT") or os.environ.get("DCC_CAMPAIGN_DIR") or str(_paths.campaign_root())
PT = [("consumable", .30), ("gear", .25), ("credits", .15), ("tailored", .18), ("weird", .10)]  # 99-00 = upgrade (.02)
UPG = .02

def load_decks():
    decks = {}
    for f in sorted(glob.glob(ROOT + "/tables/loot-decks/f01-*.json")):
        d = json.load(open(f))
        if not (isinstance(d, dict) and str(d.get("schema", "")).startswith("loot-deck/")): continue
        if d.get("floor") != 1: continue
        z = str(d.get("zone")).lower()
        decks.setdefault(z, []).extend(d["cards"])
    return decks

def is_stub(c):
    blob = " ".join(str(c.get(k, "")) for k in ("real_5e_name", "canon_status", "source_5e", "notes", "reskin_name")).upper()
    return bool(c.get("needs_verify")) or "NEEDS-VERIFY" in blob or "NEEDS VERIFY" in blob or c.get("stub") is True

def cards_for(decks, zones, box_type=None):
    """Random-draw cards from the named zone decks (plus 'any')."""
    out = []
    for z in zones:
        for c in decks.get(z, []):
            if not (isinstance(c.get("draw_weight"), (int, float)) and c["draw_weight"] > 0) or is_stub(c): continue
            if str(c.get("tier")).lower() in ("legendary", "celestial"): continue
            bt = c.get("box_types") or ["any"]
            if "any" not in bt and (not box_type or box_type not in bt): continue
            if c.get("exclusive_to"): continue
            out.append(c)
    return out

def val(c): return float(c.get("credit_value") or 0)

def pull_means(cards, tier):
    m = {}
    for k, _ in PT:
        p = [c for c in cards if c["tier"] == tier and c["pull_type"] == k]
        m[k] = (sum(val(c) * c["draw_weight"] for c in p) / sum(c["draw_weight"] for c in p)) if p else None
    return m

def pull_value(cards, tier):
    """Expected value of one pull at `tier` (upgrade handled). Empty pull-type pools are redistributed (reported)."""
    m = pull_means(cards, tier)
    empty = [k for k, v in m.items() if v is None]
    live = [(k, p) for k, p in PT if m[k] is not None]
    tot = sum(p for _, p in live)
    if not live: return None, m, empty
    base = sum(p * m[k] for k, p in live) / tot       # renormalised if a pull-type pool is empty
    if tier == "Silver":
        return base, m, empty                          # 99-00 re-rolls Silver (ceiling): conditional mean, no extra term
    ev_silver, _, _ = pull_value(cards, "Silver")
    if ev_silver is None: return base, m, empty
    return (1 - UPG) * base + UPG * ev_silver, m, empty

def analytic():
    D = load_decks()
    scopes = {
        "any_only": (["any"], None),
        "any+z03": (["any", "z03"], None),
        "any+z06": (["any", "z06"], None),
        "any+z09": (["any", "z09"], None),
        "pooled_floor": (list(D.keys()), None),            # every F1 deck at once, cards open to any box
        "z10_boss": (["any", "z10"], "Boss"),               # Silver Boss Box
        "pooled_incl_boss_only": (list(D.keys()), "Boss"),  # Accountant-style pooling, Boss-only cards included
    }
    out = {"scopes": {}}
    for name, (zs, bt) in scopes.items():
        cs = cards_for(D, zs, bt)
        eb, mb, emb = pull_value(cs, "Bronze")
        es, ms, ems = pull_value(cs, "Silver")
        r3 = lambda x: None if x is None else round(x, 3)
        out["scopes"][name] = {
            "zones": zs, "box_type": bt, "cards": len(cs),
            "bronze_pull_type_means": {k: (round(v, 2) if v is not None else None) for k, v in mb.items()},
            "silver_pull_type_means": {k: (round(v, 2) if v is not None else None) for k, v in ms.items()},
            "empty_bronze_types": emb, "empty_silver_types": ems,
            "bronze_pull": r3(eb), "bronze_box_1_5_pulls": r3(None if eb is None else 1.5 * eb),
            "silver_pull": r3(es), "silver_box_2_pulls": r3(None if es is None else 2 * es),
            "welcome_box": r3(mb["tailored"] + eb) if (mb["tailored"] is not None and eb is not None) else None}
    return out

# ----------------------------------------------------------------- simulation
def roll_credits(c, rng):
    expr = (c.get("grant") or {}).get("roll")
    if expr:
        base, mult = expr.lower().replace(",", "").split("x")
        n, s = base.split("d"); return sum(rng.randint(1, int(s)) for _ in range(int(n))) * int(mult)
    return val(c)

class Crawler:
    def __init__(self, D, rng, norepl=True):
        self.D, self.rng, self.norepl = D, rng, norepl
        self.have = set()
    def new_floor(self): self.have = set()
    def draw(self, tier, ptype, cs, cap=None):
        pool = [c for c in cs if c["tier"] == tier and c["pull_type"] == ptype]
        if self.norepl: pool = [c for c in pool if not (c.get("kind") not in ("consumable", "credits", "junk") and c["id"] in self.have)]
        if cap is not None: pool = [c for c in pool if val(c) <= cap]
        if not pool:   # widen to any pull type at this tier (counted)
            pool = [c for c in cs if c["tier"] == tier and (cap is None or val(c) <= cap)]
            if self.norepl: pool = [c for c in pool if not (c.get("kind") not in ("consumable", "credits", "junk") and c["id"] in self.have)]
            self.widened = getattr(self, "widened", 0) + 1
        w = [c["draw_weight"] for c in pool]
        c = self.rng.choices(pool, w)[0]
        if c.get("kind") not in ("consumable", "credits", "junk"): self.have.add(c["id"])
        return roll_credits(c, self.rng) if c["pull_type"] == "credits" else val(c), c
    def pull(self, tier, cs, force=None, cap=None):
        r = self.rng.randint(1, 100)
        if force: t = force
        elif r <= 30: t = "consumable"
        elif r <= 55: t = "gear"
        elif r <= 70: t = "credits"
        elif r <= 88: t = "tailored"
        elif r <= 98: t = "weird"
        else: t = "upgrade"
        if t == "upgrade":
            # roll again one tier up (Silver is the F1-2 ceiling): re-roll at Silver, re-rolling a further 99-00
            while True:
                r = self.rng.randint(1, 100)
                if r <= 98: break
            t = ("consumable" if r <= 30 else "gear" if r <= 55 else "credits" if r <= 70 else "tailored" if r <= 88 else "weird")
            return self.draw("Silver", t, cs, cap)[0]
        return self.draw(tier, t, cs, cap)[0]
    def bronze_box(self, cs, pulls=None, welcome=False):
        n = pulls or self.rng.choice([1, 2])
        if welcome:
            v = self.pull("Bronze", cs, force="tailored")
            return v + self.pull("Bronze", cs)
        return sum(self.pull("Bronze", cs) for _ in range(n))
    def silver_box(self, cs, cap=None):
        return sum(self.pull("Silver", cs, cap=cap) for _ in range(2))

def simulate(n=100000, seed=70, norepl=True, gov_threshold=None, stress=False):
    D = load_decks()
    pooled = cards_for(D, list(D.keys()), None)
    welcome_cs = cards_for(D, ["any", "z06"], None)
    boss_cs = cards_for(D, ["any", "z10"], "Boss")
    rng = random.Random(seed)
    cr = Crawler(D, rng, norepl)
    res = {k: [] for k in ("f1_all", "f2_all", "f1_box", "f2_box")}
    triggered = 0
    r1_counts = (5, 5) if stress else (2, 3)          # ceiling scenario: 5 credit-paying R1 toasts per floor (plan is 2 and 3)
    for _ in range(n):
        out = []
        for fl in (1, 2):
            cr.new_floor()
            cash = 0.0; boxes = 0.0
            if fl == 1:
                cash += sum(rng.randint(1, 4) * 2 for _ in range(3)) + rng.randint(1, 6) * 2 + rng.randint(1, 6) * 5   # Z2 Z5 Z7 std, Z8 hard, Z10 boss (Ticks 0)
                odds = [.06] * 3 + [.23]; deed = .5 if not stress else None
            else:
                cash += sum(rng.randint(0, 2) for _ in range(4)) + sum(rng.randint(1, 4) * 2 for _ in range(8)) + sum(rng.randint(1, 6) * 2 for _ in range(2)) + rng.randint(1, 6) * 5
                odds = [.07] * 8 + [.28] * 2; deed = .9 if not stress else None
            cash += sum(rng.randint(10, 40) for _ in range(r1_counts[fl - 1]))
            if fl == 1: boxes += cr.bronze_box(welcome_cs, welcome=True)
            if stress:   # pacing ceiling: core 4.5 allows up to 4 Bronze per Crawler per floor (F1 count includes the Welcome Box)
                nb = 3 if fl == 1 else 4
            else:
                nb = sum(1 for p in odds if rng.random() < p) + (1 if rng.random() < deed else 0)
            for _ in range(nb): boxes += cr.bronze_box(pooled)
            capv = None
            if fl == 2 and gov_threshold is not None and cash + boxes >= gov_threshold:
                capv = 175; triggered += 1
            boxes += cr.silver_box(boss_cs, cap=capv)
            res["f%d_all" % fl].append(cash + boxes); res["f%d_box" % fl].append(boxes)
    def st(a):
        a = sorted(a); k = len(a)
        return {"mean": round(sum(a) / k, 1), "p50": round(a[k // 2]), "p90": round(a[int(.9 * k)]), "p95": round(a[int(.95 * k)]),
                "p99": round(a[int(.99 * k)]), "max": round(a[-1]), "pct_over_1500": round(100 * sum(1 for x in a if x > 1500) / k, 2)}
    o = {k: st(v) for k, v in res.items()}
    o.update({"n": n, "seed": seed, "no_repeat_nonconsumable": norepl, "gov_threshold": gov_threshold, "stress": stress,
              "gov_triggered_pct": round(100 * triggered / n, 2), "widened_pulls": getattr(cr, "widened", 0)})
    return o

if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    n = 100000; seed = 70; out = None
    if "--n" in args: i = args.index("--n"); n = int(args[i + 1]); del args[i:i + 2]
    if "--seed" in args: i = args.index("--seed"); seed = int(args[i + 1]); del args[i:i + 2]
    if args: out = args[0]
    A = analytic()
    R = {"analytic": A,
         "sim_repl_check": simulate(min(n, 40000), seed, norepl=False),
         "sim_base": simulate(n, seed),
         "sim_base_governor_900": simulate(n, seed, gov_threshold=900),
         "sim_ceiling": simulate(n, seed, stress=True),
         "sim_ceiling_governor_900": simulate(n, seed, stress=True, gov_threshold=900)}
    json.dump(R, open(out, "w"), indent=1) if out else print(json.dumps(R, indent=1))
