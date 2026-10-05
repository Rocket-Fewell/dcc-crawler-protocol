import json
D=json.load(open('/workspace/dcc-lore/tables/gm-quirks.json'))
def esc(s): return str(s).replace('|','\\|')
def rr(e): return str(e['roll_range'][0]) if e['roll_range'][0]==e['roll_range'][1] else f"{e['roll_range'][0]}-{e['roll_range'][1]}"
def fixtab():
    o="| d20 | ID | Name | Description | Rewards | Achievements | Insults | Box contents |\n|---|---|---|---|---|---|---|---|\n"
    for e in D['fixations']:
        m=e['manifests_as']
        o+=f"| {rr(e)} | {e['id']} | **{esc(e['name'])}** | {esc(e['description'])} | {esc(m['rewards'])} | {esc(m['achievements'])} | {esc(m['insults'])} | {esc(m['box_contents'])} |\n"
    return o
def tellsfix(tb):
    o="| ID | Name | L0 | L1 | L2 | L3 | L4 | L5 |\n|---|---|---|---|---|---|---|---|\n"
    for e in tb:
        t=e['tells_by_level']
        o+=f"| {e['id']} | {esc(e['name'])} | "+" | ".join(esc(t[str(i)]) for i in range(6))+" |\n"
    return o
def quirktab():
    o="| d12 | ID | Name | Description | Narration | Snark | Rewards | Fair lever |\n|---|---|---|---|---|---|---|---|\n"
    for e in D['quirks']:
        m=e['manifests_as']
        o+=f"| {rr(e)} | {e['id']} | **{esc(e['name'])}** | {esc(e['description'])} | {esc(m['narration'])} | {esc(m['snark'])} | {esc(m['rewards'])} | {esc(m['fair_lever'])} |\n"
    return o
def tictab():
    o="| d10 | ID | Name | Description | Usage | Sample |\n|---|---|---|---|---|---|\n"
    for e in D['tics']:
        m=e['manifests_as']
        o+=f"| {rr(e)} | {e['id']} | **{esc(e['name'])}** | {esc(e['description'])} | {esc(m['usage'])} | {esc(m['sample_lines'][0])} |\n"
    return o
def pitab():
    o="| d8 | ID | Name | Prior job and incident | Memory leaks | Props |\n|---|---|---|---|---|---|\n"
    for e in D['prior_installation']:
        m=e['manifests_as']
        o+=f"| {rr(e)} | {e['id']} | **{esc(e['name'])}** | {esc(e['description'])} | {esc(m['memory_leaks'])} | {esc(m['props'])} |\n"
    return o
def tellgen():
    o="| d8 | ID | Tell | What it is | How to use |\n|---|---|---|---|---|\n"
    for e in D['tells']:
        o+=f"| {rr(e)} | {e['id']} | **{esc(e['name'])}** | {esc(e['description'])} | {esc(e['manifests_as']['how_to_use'])} |\n"
    return o
def aff():
    o="| ID | Name | Trigger keywords | Pleases (points) | Offends (points) |\n|---|---|---|---|---|\n"
    for e in D['fixations']:
        a=e['affinity']
        pl="; ".join(f"{esc(x['action'])} (+{x['points']})" for x in a['pleases'])
        of="; ".join(f"{esc(x['action'])} ({x['points']})" for x in a['offends'])
        o+=f"| {e['id']} | {esc(e['name'])} | {esc(', '.join(a['trigger_keywords']))} | {pl} | {of} |\n"
    return o
def ladder():
    o="| Lvl | Name | Floors | Narration | Reward generosity | Snark | Glitch (d20 <=) | Tells/session | Fixation intrusions | Spite pts/floor |\n|---|---|---|---|---|---|---|---|---|---|\n"
    for l in D['ladder']:
        fl=f"{l['floor_min']}-{l['floor_max']}" if l['floor_max'] else f"{l['floor_min']}+"
        o+=f"| {l['level']} | **{l['name']}** | {fl} | {esc(l['narration_style'])} | {esc(l['reward_generosity'])} | {l['snark_level']}/5 | {l['glitch_check_d20_max']} | {l['tells_per_session']['min']}-{l['tells_per_session']['max']} | {l['fixation_intrusions_per_session']['min']}-{l['fixation_intrusions_per_session']['max']} | {l['spite_points_per_floor']} |\n"
    return o
def glitch():
    o="| Lvl | Glitch moments (examples) | Fair levers |\n|---|---|---|\n"
    for l in D['ladder']:
        o+=f"| {l['level']} {l['name']} | {esc('; '.join(l['glitch_moments']))} | {esc('; '.join(l['fair_levers']))} |\n"
    return o
def spite():
    o="| ID | Move | What it does | Min level | Cost | Fairness guard |\n|---|---|---|---|---|---|\n"
    for s in D['spite_moves']:
        o+=f"| {s['id']} | **{esc(s['name'])}** | {esc(s['description'])} | {s['min_level']} | {s['cost']} | {esc(s['fairness_guard'])} |\n"
    return o
def repair():
    o="| ID | Option | What it does | Level change | Duration | Requires | Side effects |\n|---|---|---|---|---|---|---|\n"
    for s in D['repair_options']:
        o+=f"| {s['id']} | **{esc(s['name'])}** | {esc(s['description'])} | {s['level_delta']:+d} | {s['duration']} | {esc(s['requires'])} | {esc(s['side_effects'])} |\n"
    return o
def bands():
    o="| Band | Affinity | Effects |\n|---|---|---|\n"
    for b in D['meta']['affinity']['bands']:
        o+=f"| **{b['name']}** | {b['min']:+d}..{b['max']:+d} | {esc(' '.join(b['effects']))} |\n"
    return o
exec(open('gmq_prose.py').read())
open('/workspace/dcc-lore/catalog/gm-quirk-framework.md','w').write(MD)
print(len(MD))
