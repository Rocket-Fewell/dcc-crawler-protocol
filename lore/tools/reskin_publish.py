#!/usr/bin/env python3
"""Prints a ready-to-post one-paragraph summary of the current item-reskins build.
Usage: python3 tools/reskin_publish.py [--build [--note "text"]]
 --build  runs tools/reskin_build.py first (which bumps the version and runs reskin_check on the result).
Without --build it verifies that the table on disk still matches tables/item-reskins.version.json (sha256), runs
reskin_check, and prints the summary. Exit 1 (nothing printed to post) if the table is out of sync or a check fails."""
import json, os, sys, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(HERE, "..", "tables")
py = sys.executable
if "--build" in sys.argv:
    cmd = [py, os.path.join(HERE, "reskin_build.py")]
    if "--note" in sys.argv: cmd += ["--note", sys.argv[sys.argv.index("--note") + 1]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit("build failed:\n" + r.stdout + r.stderr)
r = subprocess.run([py, os.path.join(HERE, "reskin_check.py")], capture_output=True, text=True)
if r.returncode: sys.exit("reskin_check failed:\n" + r.stdout)
v = json.load(open(os.path.join(T, "item-reskins.version.json"), encoding="utf-8"))
sha = hashlib.sha256(open(os.path.join(T, "item-reskins.json"), "rb").read()).hexdigest()
if sha != v["sha256"]: sys.exit("item-reskins.json changed since the last build (sha mismatch): run tools/reskin_build.py first")
d = v["diff"]
def ids(xs, n=8):
    xs = [x if isinstance(x, str) else "%s (%s->%s cp)" % (x["srd_id"], x["from_cp"], x["to_cp"]) for x in xs]
    return "" if not xs else " (" + ", ".join(xs[:n]) + (", +%d more" % (len(xs) - n) if len(xs) > n else "") + ")"
since = ("since v%s" % d["since_version"]) if d.get("since_version") else "(first tracked build)"
txt = ("Item reskin table v%s is published: tables/item-reskins.json, sha256 %s, %d entries, built %s. "
       "Changes %s: %d added%s, %d removed%s, %d price changes%s, %d renamed%s. "
       "Ids are stable kebab-case srd_id (stored on the sheet, lookup by srd_id, fallback to srd_name); base_price is SRD reference only and always keys off srd_id, never the display name. "
       "The six generic headers (arcane-focus, druidic-focus, holy-symbol, gaming-set, musical-instrument, artisans-tools) are not purchasable and must resolve to a variant id.%s") % (
    v["version"], v["sha256"][:12], v["entry_count"], v["built_at"], since, len(d["added"]), ids(d["added"]), len(d["removed"]), ids(d["removed"]),
    len(d["price_changed"]), ids(d["price_changed"]), len(d["renamed"]), ids(d["renamed"]), (" Note: %s." % v["note"].rstrip(".")) if v.get("note") else "")
print(txt)
