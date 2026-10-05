#!/usr/bin/env python3
"""Builds tables/create-screens-reskins.json, tables/create-flow-lines.proposed.json and tables/create-screens-reskins.audit.md
(+ .version.json and a CHANGELOG line) from create_screens_data.py. Same discipline as background_reskin_build.py:
stage, check the stage, then write. Usage: python3 tools/create_screens_build.py [--note "text"]   (patch version bumps every build)"""
import json, os, re, sys, hashlib, datetime, subprocess, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import create_screens_data as D
OUT = os.path.join(HERE, "..", "tables")
P = {"main": os.path.join(OUT, "create-screens-reskins.json"), "lines": os.path.join(OUT, "create-flow-lines.proposed.json"),
     "audit": os.path.join(OUT, "create-screens-reskins.audit.md"), "ver": os.path.join(OUT, "create-screens-reskins.version.json"),
     "log": os.path.join(OUT, "create-screens-reskins.CHANGELOG.md")}
from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parent))
from paths import CREATE_FLOW_LINES as _ORIG, VOICE_BRIDGE_SRC as _VBS
ORIG = str(_ORIG) if _ORIG else ""
SRC = str(_VBS) if _VBS else ""
if not ORIG:
    sys.exit("create_screens_build: create-flow-lines.json not found (set DCC_CAMPAIGN_ROOT)")
if not SRC:
    print("WARN: DCC_VOICE_BRIDGE_SRC / discord-voice-bridge/src/create not found; code_ref look-up will be skipped", file=sys.stderr)
NOTE = sys.argv[sys.argv.index("--note") + 1] if "--note" in sys.argv else None
PH = re.compile(r"\{[a-z_]+\}")
def sha(path): return hashlib.sha256(open(path, "rb").read()).hexdigest()
srcs = ({f: open(os.path.join(SRC, f), encoding="utf-8").read().split("\n") for f in ("screens.js", "rules.js", "flow.js", "ui.js") if os.path.exists(os.path.join(SRC, f))} if SRC else {})
def locate(old):
    """Best-effort code reference (read-only look at the bridge source). The check does not depend on it."""
    if not srcs: return None, "no_source"
    frags = [f.strip() for part in re.split(r"\n", old) for f in PH.split(part) if len(f.strip()) >= 6]
    if not frags: return None, "not_found"
    frag = max(frags, key=len)
    for name, lines in srcs.items():
        for n, ln in enumerate(lines, 1):
            if frag in ln or frag.replace("'", "\\'") in ln: return "src/create/%s:%d" % (name, n), "found"
    return None, "not_found"
entries = []
for r in D.ROWS:
    e = dict(r)
    ref, m = locate(e["old"])
    e["code_ref"] = ref; e["source_match"] = m
    e["needs_code"] = True
    e["state"] = "label" if e["kind"] in D.LABEL_KINDS else "text"
    if e["screen"] == "ALL": e["plain_on"] = list(D.PLAIN_VIEWS)
    if e["id"] in D.NEEDS_CODE_DETAIL: e["needs_code_detail"] = D.NEEDS_CODE_DETAIL[e["id"]]
    entries.append(e)
entries.sort(key=lambda e: (D.SCREENS.index(e["screen"]), e["id"]))
counts_screen = collections.Counter(e["screen"] for e in entries); counts_kind = collections.Counter(e["kind"] for e in entries)
def snap(es): return {e["id"]: e["new"] for e in es}
prev_ver, prev_snap = None, {}
if os.path.exists(P["ver"]):
    pv = json.load(open(P["ver"], encoding="utf-8")); prev_ver, prev_snap = pv["version"], pv.get("snapshot", {})
def bump(v): a, b, c = (int(x) for x in v.split(".")); return "%d.%d.%d" % (a, b, c + 1)
NEW_VER = bump(prev_ver) if prev_ver else "0.1.0"
cur = snap(entries)
diff = {"since_version": prev_ver, "added": sorted(set(cur) - set(prev_snap)), "removed": sorted(set(prev_snap) - set(cur)),
        "renamed": sorted(k for k in set(cur) & set(prev_snap) if prev_snap[k] != cur[k])}
orig = json.load(open(ORIG, encoding="utf-8"))
meta = {
 "title": "Follow-on /create screens reskins: S3/S4 and S8 onward labels, buttons, selects, notices, errors, help, nav and dialogs -> DCC display text (display only)",
 "owner": "DCC Lore", "updated": datetime.date.today().isoformat(), "version": NEW_VER,
 "version_file": "tables/create-screens-reskins.version.json (sha256, built_at, entry_count, diff, companions); history in tables/create-screens-reskins.CHANGELOG.md",
 "id_scheme": {"id": "Stable kebab-case id per UI string. Prefix says the kind: method-, ability-, stat-, title-, button-, select-, modal-, field-, package-, choice-, opt-, nav-, dialog-, notice-, error-, hint-, help-. Never change once published.",
               "chargen_ref": "Where the 5e name comes from in tables/chargen-5e.json, when it does.",
               "lookup": "Look up by id. Fall back to the old text (also stored) when an id is missing."},
 "display_rule": "Label rows (state=label): new == combined_label == 'Our Name (5e Name)' (+ a suffix such as ': pick {n}'), exactly one pair of parentheses in the combined label, unique combined labels. Text rows (state=text): new replaces old; same {placeholders}, same numbers, rules facts unchanged. Display only: ids, values, numbers, skill/tool/spell names and the logged-dice wording are untouched.",
 "delivery": {
   "a": "This file: labels and texts keyed by id. The bridge hard-codes these strings today (see code_ref), so each row needs a one-time code hook: replace the literal with a lookup by id (the same pattern as lineageLabel/featLabel; gate with a setting like create.background_reskin until Caleb approves).",
   "b": "tables/create-flow-lines.proposed.json: the vanilla create-flow-lines keys rewritten with the same keys, placeholders and variant counts. Deliver through the bridge's merge layer (mergeProposedLines in screenstext.js, behind the flag). Copying it over create-flow-lines.json would fail test/roll.test.js:249 and :308 (they assert the old S8_roll_closed and S8_roll_keep_ok text; per Syndicate audit F6). Keys already and near_dup have no consumer in the bridge today."},
 "plain_views": {"views": D.PLAIN_VIEWS, "rule": "Rows with screen ALL carry plain_on. On those views (S1, S2, the comfort-only view, the S13 survey) show the old text, not the new one. No S2 or survey-specific rows are rewritten."},
 "needs_code_items": sorted(list(D.NEEDS_CODE_DETAIL)) + ["every row: the bridge hard-codes the literal today (see code_ref); hook by id, with old as the drift-guard text"],
 "source_match": "found = the old text was located in src/create at build time (code_ref). not_found = the old text is a paraphrase of a dynamic string; the Architect should confirm the exact literal.",
 "tone": "DCC System voice (see create-flow-lines.json): dry, clear, snark aimed at the job, the choices and the gear, never the person. Adults-only table, cursing cleared. Crawlers, never the other word.",
 "counts": {"by_screen": dict(counts_screen), "by_kind": dict(counts_kind)}, "total": len(entries),
 "consumers": ["/create S3, S4, S6 choices, S8 to S17 and the shared nav/dialogs"],
}
doc = {"schema": "create-screens-reskins/0.1.0", "meta": meta, "entries": entries,
       "vanilla_on_purpose": [{"id": a, "what": b, "why": c} for a, b, c in D.AUDIT],
       "line_keys": {"flavored": sorted(D.LINES), "left_vanilla_or_already_flavored": D.LINES_LEFT}}
# proposed lines: the full file shape, so it can be swapped in
lines = {k: (D.LINES[k] if k in D.LINES else v) for k, v in orig["lines"].items()}
pm = dict(orig["meta"])
pm.update({"version": "0.1.2", "based_on": "create-flow-lines.json v%s" % orig["meta"].get("version"), "based_on_sha256": sha(ORIG),
           "status": "PROPOSED (Lore). Not live. Swap in only after Caleb approves. Same keys, same {placeholders}, up to 3 variants each, every rule number kept.",
           "changed_keys": sorted(D.LINES), "unchanged_keys": sorted(set(orig["lines"]) - set(D.LINES)), "unused_in_bridge": ["already", "near_dup"], "delivery": "Use the merge layer (mergeProposedLines). A straight copy over create-flow-lines.json fails test/roll.test.js:249 and :308 until those two assertions are updated.",
           "label_dependency": "Rewritten lines name the new labels in 'Our Name (5e Name)' form (Factory Preset, Layaway Plan, Dice Gamble, Stamp It Anyway), so they still read correctly if the label hooks are not applied yet."})
prop = {"meta": pm, "lines": lines, "survey": orig["survey"]}
STAGE = {k: v + ".tmp" for k, v in P.items() if k in ("main", "lines", "audit")}
json.dump(doc, open(STAGE["main"], "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(STAGE["main"], "a").write("\n")
json.dump(prop, open(STAGE["lines"], "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(STAGE["lines"], "a").write("\n")
md = ["# create-screens-reskins audit: left vanilla on purpose",
      "Owner: DCC Lore | Status: draft | Version: %s | Updated: %s" % (NEW_VER, datetime.date.today().isoformat()),
      "Summary: What the follow-on /create screens still show in plain 5e or plain System text on purpose, and why. Generated by tools/create_screens_build.py from create_screens_data.py.", "",
      "## Strings left vanilla", ""]
md += ["- **%s**: %s. Why: %s" % (a, b, c) for a, b, c in D.AUDIT]
md += ["", "## create-flow-lines keys not rewritten", ""] + ["- `%s`: %s" % (k, v) for k, v in D.LINES_LEFT.items()]
md += ["", "## create-flow-lines keys rewritten (%d)" % len(D.LINES), "", ", ".join("`%s`" % k for k in sorted(D.LINES)), ""]
open(STAGE["audit"], "w", encoding="utf-8").write("\n".join(md))
r = subprocess.run([sys.executable, os.path.join(HERE, "create_screens_check.py"), "--stage", STAGE["main"], STAGE["lines"]], capture_output=True, text=True)
if r.returncode:
    sys.stdout.write(r.stdout)
    for p in STAGE.values(): os.remove(p)
    sys.exit("create_screens_check failed on the staged build; nothing written")
for k, p in STAGE.items(): os.replace(p, P[k])
now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
msha = sha(P["main"])
json.dump({"version": NEW_VER, "sha256": msha, "built_at": now, "entry_count": len(entries), "note": NOTE, "diff": diff,
           "companions": {"tables/create-flow-lines.proposed.json": {"sha256": sha(P["lines"]), "changed_keys": len(D.LINES), "total_keys": len(lines)},
                          "tables/create-screens-reskins.audit.md": {"sha256": sha(P["audit"])}},
           "snapshot": cur}, open(P["ver"], "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(P["ver"], "a").write("\n")
new_log = not os.path.exists(P["log"])
with open(P["log"], "a", encoding="utf-8") as f:
    if new_log: f.write("# create-screens-reskins CHANGELOG\nOwner: DCC Lore | Status: draft | Version: 0.1 | Updated: %s\nSummary: One line per build of tables/create-screens-reskins.json and its companions (version, short sha256, entry count, diff).\n\n" % datetime.date.today().isoformat())
    f.write("- %s | v%s | sha256 %s | %d entries | %s; +%d added, -%d removed, %d renamed | proposed lines %d/%d keys\n" % (datetime.date.today().isoformat(), NEW_VER, msha[:12], len(entries), NOTE or "build", len(diff["added"]), len(diff["removed"]), len(diff["renamed"]), len(D.LINES), len(lines)))
print("wrote %d entries (%s)" % (len(entries), dict(counts_screen)))
print("version %s sha256 %s" % (NEW_VER, msha))
print("proposed lines sha256 %s" % sha(P["lines"]))
