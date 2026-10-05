# ops/
- `backup-push.sh`, `backup-sync.py`: copies of `/workspace/backup-push.sh` and `/workspace/backup-sync.py` (refreshed on every backup run).
- `check_repo_safe.py` + `hooks/pre-commit`: credential-only safety check used by the backup (Caleb authorized full backup on 2026-10-04). It never prints a matched value and does not read `gm-notes/secret/` contents.
