#!/usr/bin/env python3
"""sim_floors.py - Monte Carlo SKELETON for the GM degeneration ladder and Affinity bands (stdlib only).

Planning aid only. It reads the public ladder / affinity numbers from lore's gm-quirks.json and simulates
random campaigns; it does NOT roll the real traits, never touches <campaign>/gm-notes/secret/ or any campaign
file, and uses a seeded `random.Random` (a simulation, not the secret roll).

Usage:
  python3 tools/sim_floors.py [--trials 2000] [--floors 12] [--scenes 4] [--players 4] [--seed 1]
                              [--p-positive 0.55] [--stress-prob 0.15] [--events-per-scene 1.0] [--json]
Output per floor: effective level mix, P(at least one glitch), mean glitches per floor, and the share of
player-floors in each Affinity band (events: random +/-1..3 per the table's point values, scene cap, range clamp,
1-point drift per floor).
Model limits (TODO): events are independent coin-flips (no fixation matching), stress is i.i.d. per floor,
no repairs (RP-01..05), one glitch d20 per scene.
"""
import argparse
import json
import os
import random
import sys

DEFAULT_TABLE = os.environ.get("DCC_GM_QUIRKS_TABLE") or "/workspace/dcc-lore/tables/gm-quirks.json"


def load_table(path=None):
    with open(path or DEFAULT_TABLE, encoding="utf-8") as f:
        return json.load(f)


def level_for_floor(ladder, floor):
    for e in ladder:
        if floor >= e["floor_min"] and (e["floor_max"] is None or floor <= e["floor_max"]):
            return e["level"]
    raise ValueError(f"no ladder level for floor {floor}")


def band_name(bands, value):
    return next(b["name"] for b in bands if b["min"] <= value <= b["max"])


def simulate(table, trials=2000, floors=12, scenes=4, players=4, seed=1, p_positive=0.55, stress_prob=0.15, events_per_scene=1.0):
    rng = random.Random(seed)
    ladder, aff = table["ladder"], table["meta"]["affinity"]
    lo, hi, cap = aff["range"]["min"], aff["range"]["max"], aff["scene_cap"]
    points = aff["point_values"]
    bands = aff["bands"]
    per_floor = [{"levels": {}, "glitch_floors": 0, "glitches": 0, "bands": {b["name"]: 0 for b in bands}} for _ in range(floors)]
    for _ in range(trials):
        score = [aff["range"]["start"]] * players
        for f in range(floors):
            if f:  # drift at each new floor
                score = [s - min(aff["drift_per_floor"], abs(s)) * (1 if s > 0 else -1) for s in score]
            stress = rng.choice((-1, 1)) if rng.random() < stress_prob else 0
            eff = max(0, min(5, level_for_floor(ladder, f + 1) + stress))
            gmax = ladder[eff]["glitch_check_d20_max"]
            slot = per_floor[f]
            slot["levels"][eff] = slot["levels"].get(eff, 0) + 1
            g = sum(1 for _s in range(scenes) if rng.randint(1, 20) <= gmax)
            slot["glitches"] += g
            slot["glitch_floors"] += g > 0
            for p in range(players):
                for _s in range(scenes):
                    scene_net = 0
                    n = int(events_per_scene) + (1 if rng.random() < events_per_scene - int(events_per_scene) else 0)
                    for _e in range(n):
                        d = rng.choice(points) * (1 if rng.random() < p_positive else -1)
                        applied = max(-cap, min(cap, scene_net + d)) - scene_net
                        applied = max(lo, min(hi, score[p] + applied)) - score[p]
                        scene_net += applied
                        score[p] += applied
                slot["bands"][band_name(bands, score[p])] += 1
    out = []
    for f, slot in enumerate(per_floor):
        out.append({
            "floor": f + 1,
            "level_mix": {str(k): round(v / trials, 3) for k, v in sorted(slot["levels"].items())},
            "p_any_glitch": round(slot["glitch_floors"] / trials, 3),
            "mean_glitches": round(slot["glitches"] / trials, 3),
            "band_share": {k: round(v / (trials * players), 3) for k, v in slot["bands"].items()},
        })
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Monte Carlo skeleton for the GM ladder and Affinity bands (planning aid)")
    ap.add_argument("--table", help="path to gm-quirks.json")
    ap.add_argument("--trials", type=int, default=2000)
    ap.add_argument("--floors", type=int, default=12)
    ap.add_argument("--scenes", type=int, default=4, help="scenes per floor")
    ap.add_argument("--players", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--p-positive", type=float, default=0.55)
    ap.add_argument("--stress-prob", type=float, default=0.15, help="chance a floor gets stress +1 or -1")
    ap.add_argument("--events-per-scene", type=float, default=1.0, help="mean scored events per player per scene")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if min(a.trials, a.floors, a.scenes, a.players) < 1 or not 0 <= a.p_positive <= 1 or not 0 <= a.stress_prob <= 1:
        print("ERROR: trials/floors/scenes/players must be >= 1 and probabilities within 0..1", file=sys.stderr)
        return 2
    rows = simulate(load_table(a.table), a.trials, a.floors, a.scenes, a.players, a.seed, a.p_positive, a.stress_prob, a.events_per_scene)
    if a.json:
        print(json.dumps(rows, indent=2))
        return 0
    print(f"{a.trials} trials, {a.players} players, {a.scenes} scenes/floor, seed {a.seed}")
    for r in rows:
        bands = " ".join(f"{k.split()[0][:4]} {v:.0%}" for k, v in r["band_share"].items())
        print(f"F{r['floor']:>2} levels {r['level_mix']} | P(glitch) {r['p_any_glitch']:.0%} mean {r['mean_glitches']} | {bands}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
