# Tools Index
Owner: Borent Corp Systems Architect | Status: draft | Version: 1.2 | Updated: 2026-10-04
Summary: Files in tools/ - the AI GM's dice roller and live-state manager (Python 3, stdlib only).

| Path | Description | Owner | Status |
|---|---|---|---|
| README.md | Exact commands and examples for roll.py and state.py (read this first) | Borent | draft |
| roll.py | Dice roller: NdM, kh/kl/dh/dl, adv/dis, crits; prints [ROLL] line and logs to sessions/rolls-YYYY-MM-DD.log (alpha) or sessions-data/<id>/rolls-YYYY-MM-DD.log (other sessions) | Borent | draft |
| state.py | Live state manager for sessions/state.json: crawlers, HP, inventory, credits, revive/bypass caps, backups, snapshot, validate | Borent | draft |
| tests/test_roll.py | unittest suite for roll.py (parsing, keep/drop, bounds, crits, log, CLI) | Borent | draft |
| tests/test_state.py | unittest suite for state.py (schema, HP clamping, revive caps, backup rotation, atomic write, locking) | Borent | draft |
| gm_quirks.py | GM-only secret trait roll (sealed, committed), degeneration level lookup and per-player Affinity; used through `state.py gm-quirks` / `state.py affinity` | Borent | draft |
| sim_floors.py | Planning-only Monte Carlo of glitch odds and Affinity bands per floor (skeleton) | Borent | draft |
| tests/test_gm_quirks.py | unittest suite for gm_quirks.py and sim_floors.py (schema, roll refusal, commitment, caps, drift, opt-outs, secrecy) | Borent | draft |
| discord_gm.py (spotlight + stop subcommands) | `stop` writes sessions/voice-control.json (bridge flushes speech); `spotlight set/clear/show`: writes sessions/spotlight.json atomically so the Discord bridge only wakes the GM for that player or the wake word "AI" (fails open) | Borent | draft |
| tests/test_discord_gm.py | unittest suite for the spotlight subcommand (atomic write, state, aliases, validation, no network) | Borent | draft |
| snapshot.py | Timestamped backup of characters/sessions/decisions/gm-notes to /workspace/backups/dcc-campaign (keeps 60). Run: python3 tools/snapshot.py --label after-intake | Borent | final |

- `tools/publisher.py` (via `discord_gm.py publish|setup-channels|register-channel|channels`): posts each crawler's full card to their own read-only channel; map `sessions/player-channels.json`, snapshots `sessions/published-snapshots.json`, item text `exports/card-data.json`. See tools/README.md.
- `sessions/credit-ledger.jsonl`: append-only credit ledger written by state.py (`--reason`); `state.py ledger show|verify|import`.
- `tools/new-session.py`, `tools/gm_lock.sh`, `tools/campaign_session.py`: session scaffolding, per-session lock, active-session resolution.
- `tools/loot.py`, `tools/ledgers.py` (via `state.py loot|box|banner`): loot-deck draws, Story Boxes (two-step award/open, safe-room rule, not bound, story_value provenance, deed registry `story-box-ledger.jsonl`), `sell`/`transfer`/`scene`/`party`, box and banner ledgers. Tests: tests/test_loot_ledgers.py, tests/test_create_crawler.py.
- `tools/busted.py`, `tools/repair_log.py` (via `state.py gm-quirks guess`, `state.py repair-log`): Busted-call grading (pure functions, keyword matching in memory only), the tell guard (`repair-log tell`) and the sealed hash-chained repair log. Tests: tests/test_busted.py, tests/test_story_box.py.
| tests/test_ledger.py | unittest suite for the credit ledger (reason/source, verify, import) | Borent | draft |
| tests/test_floor_lost.py | Decision 028: floor-lost write-off and loot-body, on temp copies (balance to 0, exact coins/items recorded, verify, tamper detection, conservation) | Borent | draft |
| tests/test_publisher.py | unittest suite for publisher.py (card render, diffs, channel mapping; no network) | Borent | draft |
| tests/test_safe_room_sales.py | unittest suite for the safe-room rule, two-step Story Box, sell/transfer provenance flags, floor multiplier, pet-crawler | Borent | draft |
| tests/test_crawlers.py | unittest suite for several Crawlers per player: active/benched guards, session marker, swap request/activate and window limit, delete (ledger archive, Story Box slot, pet rule, mocked Discord channel delete), channel naming/overflow | Borent | draft |
| tests/test_pets.py | unittest suite for GM-run plain pets: add/show/mark-dead/remove/convert/shop/heal, refusals, off switch, party companions, card line, owner delete | Borent | draft |
| tests/test_audit_fixes.py | unittest suite for the audit fixes (archive, create benching, delete re-check, legacy sheet files, benched guards, ownership, session marker, ledger verify of the archive) and Story Box --reaward | Borent | draft |
| tests/test_background_reskins.py | Background reskins: ids from chargen, strict coverage, hash, structure, switch (fixtures only) | Borent | draft |
| tests/test_reskins.py | item-reskins.json is a symlink to Lore's file and its sha256 matches item-reskins.version.json | Borent | draft |
| reskin_check.py | sha256 check of tables/item-reskins.json against Lore's version file | Borent | draft |
| background_reskins.py | S7 background display names (Lore's background-reskins.json): --ids lists the 32 ids from chargen-5e.json, strict coverage + sha256 check, --enable/--disable create.background_reskin | Borent | draft |
| create_screens_reskins.py | /create screens display layer (Lore's create-screens-reskins.json): hash + companion check, content rules, --source-map (wired vs not_found), --enable/--disable create.screens_reskin (the rollback) | Borent | draft |
| tests/test_create_screens_reskins.py | Create screens reskins: content rules, hash and companion sha, flag switch, real-file check | Borent | draft |
| species_class_reskins.py | Species/lineage/class/class-option display names (Lore's species-class-reskins.json): --ids lists every id to cover, coverage + sha256 check, label() with plain-5e fallback | Borent | draft |
- Several Crawlers per player (decisions/020, 021): `state.py crawler list|migrate|request|requests|activate|delete`, `state.py session-status`; logs `sessions/swap-log.jsonl`, `swap-requests.jsonl`, `delete-log.jsonl`, archive `sessions/deleted-archive/`. See README.
| check_repo_safe.py | Repo safety check (pre-commit hook `tools/hooks/pre-commit`, installer `install_hooks.sh`): blocks the secret GM notes folder, sessions/, credit-ledger*, .env, logs and secret-shaped content; never prints matched text | Borent | draft |
| tests/test_check_repo_safe.py | check_repo_safe: path rules, content patterns, real pre-commit hook run in a temp repo | Borent | draft |
| tests/test_loot_totals_credits.py | `loot totals --include-credits` (all-in view, A12 valve check, `credits --floor`), default output unchanged | Borent | draft |
| tests/test_loot_flag_lines.py | Per-floor inflation flag lines from the budget file (F1, F2 byte-identical, F3, F15, v0.1.5 map shapes, missing/corrupt file fallback) | Borent | draft |
| tests/test_accountant_job7.py | Accountant round 3: body_loot/floor_lost item fingerprint with a fixed cutoff (2 -> 99 fails verify; tamper cases t20, t21, t24; only pre-#11 rows exempt), priced transfers never income, --credit-sources validation, strict ASCII-digit --coins (no leading zeros), --credit-sources needs --include-credits, transfer wording, "(no floor set)" not "FNone" | Borent | draft |
