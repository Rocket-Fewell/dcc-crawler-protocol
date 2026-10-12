# ops/
- `backup-push.sh`, `backup-sync.py`: copies of `/workspace/backup-push.sh` and `/workspace/backup-sync.py` (refreshed on every backup run).
- Delete-sync keeps tracked `core-book/build/` files when the live core-book tree is missing them (Caleb, 2026-10-07). When the live tree has one of those files, the mirror copies the live file.
- `check_repo_safe.py` + `hooks/pre-commit`: credential-only safety check used by the backup (Caleb authorized full backup on 2026-10-04). It never prints a matched value and does not read `gm-notes/secret/` contents.
