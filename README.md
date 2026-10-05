# DCC campaign: rules, floors, tools and canon (local staging repo)

Design and tooling repo for the Dungeon Crawler campaign run on Discord: house rules, decisions, Floor 1 day pages, loot/achievement/reskin tables, the Python campaign tools and their tests, and Lore's canon tables and ledger. Start with `INDEX.md` and `STATE-OF-BUILD.md`.

## Full backup (authorized by Caleb, 2026-10-04)
This repo is a FULL private backup of the project, refreshed by `ops/backup-push.sh` (copy of `/workspace/backup-push.sh`), which runs `ops/backup-sync.py` to mirror (with delete-sync) every source below.

## Layout
- Repo root = all of `/workspace/dcc-campaign`: `rules/`, `floors/`, `decisions/`, `tables/`, `tools/`, `tools-notes/`, `guides/`, `characters/` (incl. live sheets), `gm-notes/` (incl. `gm-notes/secret/`), `sessions/` (state, ledgers, logs, backups), `exports/`, `bot/` (the campaign's symlink to discord-voice-bridge, stored as a copy) and `rules/_source-crawler-protocol/`.
- `lore/` = all of `/workspace/dcc-lore` (the campaign's `lore` symlink).
- `core-book/`, `discord-voice-bridge/`, `crawler-protocol/`, `agent-tools/`, `srd/`, `backups/` = the `/workspace` folders of the same name.
- `scratch/tmp-eb/` (encounter-budget generator and its versions) and `scratch/discord-pass/` (Discord channel snapshot): the only unique material found in the box's scratch folders.
- `ops/` the backup scripts and the credential-only checker `ops/check_repo_safe.py` with its hook `ops/hooks/pre-commit`.

## What is left out
Only live credentials (`.env`, `.env.*`, any file matching a credential pattern, named in `CREDENTIAL_EXCLUDES` in `ops/backup-sync.py`), dependency/cache folders (`node_modules`, `__pycache__`, `*.pyc`, `.venv`, nested `.git`) and files over 50 MB.

Note: `tools/check_repo_safe.py` and `tools/hooks/pre-commit` here are faithful copies of the campaign's own (older, path-blocking) versions. The backup does NOT use them; it uses `ops/check_repo_safe.py`, which checks credentials only.
