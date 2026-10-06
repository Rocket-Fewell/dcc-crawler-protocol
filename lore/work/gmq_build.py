import os as _os
_LORE = _os.environ.get('DCC_LORE_ROOT') or _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
import json,sys
sys.path.insert(0,'.')
from gmq_fix import FIX
from gmq_rest import QUIRKS,TICS,TELLS,PI
from gmq_aff import AFF,GENERIC
from gmq_cfg import *
ids={"AB-5":"AB-FAVOR","AB-4":"AB-MILD","AB-3":"AB-NEUTRAL","AB-2":"AB-PETTY","AB-1":"AB-VINDICTIVE"}
for b in AFFMETA["bands"]: b["id"]=ids[b["id"]]
AFFMETA["generic_pleases"]=GENERIC["pleases"];AFFMETA["generic_offends"]=GENERIC["offends"]
for f in FIX:
    n=f["roll_range"][0]; f["affinity"]=AFF[n]
# lucky number variants
FIX[10]["variants"]=[{"roll":"d6","values":[7,13,42,69,88,404]}]
doc={
 "meta":{"schema_version":"1.1","doc":"catalog/gm-quirk-framework.md","owner":"DCC Lore","updated":"2026-10-04",
  "tag_note":"All tables are HOUSE design. canon_basis lists ledger IDs in CANON-LEDGER.md section 15 (M-210..M-227) and M-033.",
  "visibility":"GM-ONLY. Never print any rolled result or affinity value in public 'show', exports or voice output.",
  "rolls":{"prior_installation":"1d8","fixation":"1d20","quirks":"2d12 (reroll duplicates)","tic":"1d10","order":["prior_installation","fixation","fixation_variant","quirks","tic"]},
  "stress":{"range":[-1,1],"plus_one_when":["Syndicate/Borant overrules a GM discretionary ruling (canon M-220/M-221)","a Spite Move is refused or mocked"],"minus_one_when":["a successful Tribute (RP-01)","a successful repair"],"effective_level":"clamp(ladder_level_for_floor + stress, 0, 5)"},
  "affinity":AFFMETA},
 "prior_installation":PI,"fixations":FIX,"quirks":QUIRKS,"tics":TICS,"tells":TELLS,"ladder":LADDER,"spite_moves":SPITE,"repair_options":REPAIR}
json.dump(doc,open(_os.path.join(_LORE, 'tables/gm-quirks.json'),'w'),indent=2,ensure_ascii=False)
print({k:len(v) for k,v in doc.items() if isinstance(v,list)})
