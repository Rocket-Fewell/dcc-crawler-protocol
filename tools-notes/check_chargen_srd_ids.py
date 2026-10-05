#!/usr/bin/env python3
"""Check tables/chargen-5e.json items carry valid srd_id values from DCC Lore's item-reskins.json.

Read-only. Usage: python3 check_chargen_srd_ids.py [chargen.json] [item-reskins.json]
Exit 1 on any error. INFO lines are not errors.
"""
import json, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
CG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'tables', 'chargen-5e.json')
RS = sys.argv[2] if len(sys.argv) > 2 else '/workspace/dcc-lore/tables/item-reskins.json'

cg = json.load(open(CG))
rs = json.load(open(RS))
ent = {e['srd_id']: e for e in rs['entries']}
chargen_to_srd = {k: e['srd_id'] for e in rs['entries'] for k in e['chargen_keys']}
errors, info = [], []
# generic 'Varies' header ids (never priced); Lore also marks arcane-focus / druidic-focus as headers
HEADERS = {'arcane-focus', 'druidic-focus', 'holy-symbol', 'gaming-set', 'musical-instrument', 'artisans-tools'}

items = cg['items']
for k, it in items.items():
    sid = it.get('srd_id')
    if not sid:
        errors.append(f"{k}: missing srd_id"); continue
    if sid not in ent:
        errors.append(f"{k}: srd_id '{sid}' unknown in item-reskins.json"); continue
    if chargen_to_srd.get(k) != sid:
        errors.append(f"{k}: srd_id '{sid}' != Lore chargen_keys mapping '{chargen_to_srd.get(k)}'")
    is_header = ent[sid]['base_price_cp'] is None and sid in HEADERS
    if is_header:
        if it.get('srd_id_kind') != 'header' or not it.get('needs_variant_choice') or not it.get('srd_variant_ids'):
            errors.append(f"{k}: srd_id '{sid}' is a generic header; needs srd_id_kind='header', needs_variant_choice and srd_variant_ids")
    elif it.get('srd_id_kind') == 'header':
        errors.append(f"{k}: marked header but '{sid}' is not a header id")
    for v in it.get('srd_variant_ids', []):
        if v not in ent:
            errors.append(f"{k}: srd_variant_id '{v}' unknown")
    lp = ent[sid]['base_price_cp']
    if lp is None:
        info.append(f"{k}: Lore base_price null ({'HEADER, player must choose a variant' if it.get('srd_id_kind')=='header' else 'single item, price from chargen'}); chargen {it.get('cost_cp', 'no')} cp")
    elif lp != it['cost_cp']:
        errors.append(f"{k}: cost_cp {it['cost_cp']} != Lore base_price_cp {lp}")
for k in chargen_to_srd:
    if k not in items:
        errors.append(f"Lore maps chargen key '{k}' that is not in chargen items")

# package / background item keys must exist in items
used = set()
for sec in ('classes', 'backgrounds'):
    for n, c in cg[sec].items():
        for p in c.get('packages', []):
            for key, qty in p['items']:
                used.add(key)
                if key not in items:
                    errors.append(f"{sec}.{n} package {p['id']}: unknown item key '{key}'")
srd_ids = [it.get('srd_id') for it in items.values()]
unknown = sorted({s for s in srd_ids if s not in ent})

print(f"chargen items: {len(items)}; with srd_id: {sum(1 for s in srd_ids if s)}; distinct srd_ids: {len(set(srd_ids))}")
print(f"entries pointing at a header id (need player variant choice): {[k for k,i in items.items() if i.get('srd_id') in HEADERS]}")
print(f"unknown srd_ids: {unknown or 'none'}")
print(f"starting-equipment keys used by packages: {len(used)} (Lore says 66)")
print(f"meta.version: {cg['meta']['version']}")
for i in info: print("INFO:", i)
for e in errors: print("ERROR:", e)
print(f"{len(errors)} errors")
sys.exit(1 if errors else 0)
