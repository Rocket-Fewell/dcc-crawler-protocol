# Tools Index
Owner: DCC Lore | Status: review | Version: 2.0 | Updated: 2026-10-05
Summary: Scripts that generate catalogs, the ledger and the indexes. Roots come from tools/paths.py (repo-relative; optional env overrides). Do not hardcode box paths.

| Path | Description | Owner | Status |
|---|---|---|---|
| paths.py | Shared LORE_ROOT / CAMPAIGN_ROOT / VOICE_BRIDGE_SRC helper (env DCC_LORE_ROOT, DCC_CAMPAIGN_ROOT, DCC_VOICE_BRIDGE_SRC; absolute() not resolve()). | DCC Lore | n/a (data/code) |
| apply_headers.py | Adds the convention header to every .md file (run after regenerating catalogs). | DCC Lore | n/a (data/code) |
| gen.py | Regenerates the table-based catalogs in catalog/ from raw/all.json. | DCC Lore | n/a (data/code) |
| gen_index.py | Regenerates INDEX.md and the folder INDEX.md files. | DCC Lore | n/a (data/code) |
| ledger_ach.py | Builds the achievements rows for the ledger. | DCC Lore | n/a (data/code) |
| ledger_build.py | Builds the initial CANON-LEDGER.md (do not re-run over an appended ledger). | DCC Lore | n/a (data/code) |
| ledger_check.py | Checks every ledger quote is an exact substring of its source and <=25 words. | DCC Lore | n/a (data/code) |
| ledger_lib.py | Helpers for the ledger tools: page lookup, quote extraction, trimming. | DCC Lore | n/a (data/code) |
| ledger_spec_mech.py | Specs for the ledger mechanics rulings (M-). | DCC Lore | n/a (data/code) |
| ledger_spec_other.py | Specs for loot, skills, spells, items, classes, races, bosses, characters, plot beats. | DCC Lore | n/a (data/code) |
| voice_index.py | Regenerates catalog/system-voice-index.md. | DCC Lore | n/a (data/code) |
| wk.py | Loader/parsers for raw/all.json shared by generators. | DCC Lore | n/a (data/code) |
| yt_fetch.py | Fetches YouTube auto-caption transcripts into sources/youtube/. | DCC Lore | n/a (data/code) |
| loot_decks_build.py | Builds the Floor 1 loot decks (tables/loot-decks/f01-*.json). | DCC Lore | n/a (data/code) |
| ach_deck_build.py | Builds the Floor 1 achievement deck JSON. | DCC Lore | n/a (data/code) |
| deck_check.py | Validates loot-deck and achievement-deck JSON (fields, unique ids, weights, credit ranges, counts by tier). | DCC Lore | n/a (data/code) |
| reskin_build.py | Builds tables/item-reskins.json and .md from reskin_data.py. | DCC Lore | n/a (data/code) |
| reskin_data.py | Names, snark, SRD 5.2 reference prices for item-reskins. | DCC Lore | n/a (data/code) |
| reskin_check.py | Validates item-reskins.json and /create starting-equipment coverage. | DCC Lore | n/a (data/code) |
| reskin_publish.py | Prints the post-ready summary of the current reskin build (version, sha256, diff). | DCC Lore | n/a (data/code) |
| species_class_data.py | Names, flavor and nationality for species-class-reskins (21 species, 24 lineages, 12 classes, 4 class options). | DCC Lore | n/a (data/code) |
| species_class_build.py | Builds tables/species-class-reskins.json, its version file (version, sha256, diff) and CHANGELOG line; runs the check on the stage first. | DCC Lore | n/a (data/code) |
| species_class_check.py | Validates species-class-reskins.json, coverage against chargen-5e.json and rules/30, and the sha256 against the version file. | DCC Lore | n/a (data/code) |
| background_reskin_data.py | Names and flavor for background-reskins (16 backgrounds, origin feats, ability bonus picks, packages A/B). | DCC Lore | n/a (data/code) |
| background_reskin_build.py | Builds tables/background-reskins.json, its version file and CHANGELOG line; checks the stage first. | DCC Lore | n/a (data/code) |
| background_reskin_check.py | Validates background-reskins.json, coverage against chargen-5e.json (fails on a missing id) and the sha256. | DCC Lore | n/a (data/code) |
| create_screens_data.py | Names, texts and audit rows for create-screens-reskins and the 11 proposed create-flow-lines rewrites. | DCC Lore | n/a (data/code) |
| create_screens_build.py | Builds create-screens-reskins.json, create-flow-lines.proposed.json, the audit md, version file and CHANGELOG line; checks the stage first. | DCC Lore | n/a (data/code) |
| create_screens_check.py | Validates the reskins and the proposed lines; coverage against chargen-5e.json and every create-flow-lines key (fails on a missing id/key), placeholders and rule numbers, sha256. | DCC Lore | n/a (data/code) |
| canon_floor_build.py | Builds tables/canon-floor-1.json and .md (data in the script; ledger confidence copied from CANON-LEDGER.md; ids from work/pass18-row-map.json). | DCC Lore | n/a (data/code) |
| canon_floor_check.py | Validates canon-floor-1.json: every ledger row id exists, confidence matches the ledger, tags, quotes <=25 words, no CR/level/credit/loot text, md view fresh. | DCC Lore | n/a (data/code) |
| canon_floor2_build.py | Builds tables/canon-floor-2.json and .md (Floor 2 RESERVE canon table; data in the script; ledger confidence copied from CANON-LEDGER.md; ids from work/pass19-row-map.json and work/pass18-row-map.json). | DCC Lore | n/a (data/code) |
| canon_floor2_check.py | Validates canon-floor-2.json: status "reserve", every ledger row id exists, confidence matches the ledger, tags, quotes <=25 words, no CR/level/credit/loot text, clock/differences/timeline/backlog sections present, md view fresh. | DCC Lore | n/a (data/code) |

Change note v2.0 (2026-10-05): all tools use `paths.py` (LORE_ROOT / CAMPAIGN_ROOT / VOICE_BRIDGE_SRC). Env overrides: `DCC_LORE_ROOT`, `DCC_CAMPAIGN_ROOT`, `DCC_VOICE_BRIDGE_SRC`. No hardcoded `/workspace` or `/home/box` paths. Fresh-checkout verified.

- 2026-10-05: `paths.voice_bridge_src()` now checks `DCC_VOICE_BRIDGE_SRC`, then the repo mirror `<campaign root>/bot/src/create`, then legacy siblings; warn-and-skip only if none exist (Architect request).
