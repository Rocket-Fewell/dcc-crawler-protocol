#!/usr/bin/env python3
"""spec_sha256_sans_pin: a provenance hash of a day spec that ignores the pins.

Usage: python3 tools/encounter_bot/spec_hash_sans_pin.py floors/f01/day-NN.spec.json

Method (keep in sync with METHOD below; Syndicate can recompute it independently):
  1. Parse the spec file as JSON.
  2. Delete these keys if present (the pins; nothing else is removed):
       budget_file.version, budget_file.expected_sha256, canon_table.expected_sha256
     The budget version is never written into spec prose; prose uses the token {budget_version},
     which the generator fills at build time, so re-pinning touches only the keys above.
     The spec carries no other build stamp (spec_sha256 and validation exist only in the output JSON).
  3. Serialize with json.dumps(spec, sort_keys=True, separators=(',', ':'), ensure_ascii=False).
  4. sha256 of the UTF-8 bytes, lowercase hex.
Pure local Python 3 standard library.
"""
import hashlib
import json
import sys

PIN_PATHS = (("budget_file", "version"), ("budget_file", "expected_sha256"), ("canon_table", "expected_sha256"))
METHOD = ("sha256 (lowercase hex) of the UTF-8 bytes of json.dumps(spec, sort_keys=True, separators=(',', ':'), ensure_ascii=False), "
          "where spec is the parsed day-NN.spec.json with these keys deleted if present: budget_file.version, budget_file.expected_sha256, "
          "canon_table.expected_sha256. Nothing else is removed: spec prose carries the budget version only as the token {budget_version} "
          "(filled at build time), and the spec holds no other build stamp. Helper: tools/encounter_bot/spec_hash_sans_pin.py <spec>.")


def sans_pin(spec):
    spec = json.loads(json.dumps(spec))  # deep copy
    for parent, key in PIN_PATHS:
        if isinstance(spec.get(parent), dict):
            spec[parent].pop(key, None)
    return spec


def spec_sha256_sans_pin(spec):
    canon = json.dumps(sans_pin(spec), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: spec_hash_sans_pin.py <day-NN.spec.json>", file=sys.stderr)
        return 2
    with open(argv[0], encoding="utf-8") as f:
        print(spec_sha256_sans_pin(json.load(f)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
