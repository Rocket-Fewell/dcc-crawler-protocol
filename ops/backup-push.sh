#!/usr/bin/env bash
# FULL backup: pull GitHub first, mirror the whole DCC project -> staging repo, credential-check, commit, push to the
# private GitHub backup.
# Caleb authorized a full backup on 2026-10-04 ("i want all files on the github.... everything"): only live credentials,
# dependency/cache folders and files over 50 MB are left out (see backup-sync.py).
# Pull-first (Caleb approved 2026-10-05): before the mirror, GitHub changes since the last commit this backup pushed
# (marker file) are applied to the live files, so merged PRs are not reverted by the mirror. See backup-sync.py --pull.
# Exit codes: 0 ok; 3 CONFLICT (GitHub and live both changed a path, or GitHub touched a protected path: nothing written,
# nothing pushed); 4 STOP (cannot pull safely: marker missing, staging diverged, history rewritten); other = error.
# Token is read ONLY from env GITHUB_BACKUP_TOKEN (never printed, never stored in .git/config).
# The checkout copy (ops/backup-push.sh) does not pull, mirror, commit, or push.
# DRY_RUN=1 prints the checkout path and exits. The nightly push is the box copy
# of this script, which lives outside the repo.
# Box usage: GITHUB_BACKUP_TOKEN=... backup-push.sh ["commit message"]   (DRY_RUN=1: pull plan + mirror, no writes to
# live, no commit, no push)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ "$(basename "$SCRIPT_DIR")" = "ops" ] && [ -f "$SCRIPT_DIR/backup-sync.py" ]; then
  REPO="${DCC_BACKUP_REPO:-$(cd "$SCRIPT_DIR/.." && pwd)}"
  if [ -n "${DRY_RUN:-}" ]; then
    echo "DRY_RUN: ops/backup-push.sh does not mirror, commit, or push from a checkout."
    echo "REPO=$REPO"
    echo "Nightly push stays on the box copy of this script."
    exit 0
  fi
  echo "STOP: ops/backup-push.sh in a checkout does not commit or push. The box copy outside the repo does the nightly backup. DRY_RUN=1 prints the checkout path and exits." >&2
  exit 1
fi

# Everything runs inside main(): bash parses the whole function before running it, so the pull step may replace this
# file (ops/backup-push.sh changed on GitHub) without breaking the run in progress. The new copy runs next time.
main() {
  local BOX="${DCC_BOX_ROOT:-/workspace}"
  local REPO="${DCC_BACKUP_REPO:-$BOX/dcc-repo-staging}"
  local SYNC="${DCC_BACKUP_SYNC:-$BOX/backup-sync.py}"
  local MARKER="${DCC_BACKUP_MARKER:-$BOX/.backup-last-synced-sha}"
  local GH_URL=https://github.com/Rocket-Fewell/dcc-crawler-protocol.git
  local URL="${DCC_BACKUP_URL:-$GH_URL}"
  local MSG="${1:-Sync campaign design files}"
  : "${GITHUB_BACKUP_TOKEN:?GITHUB_BACKUP_TOKEN not set}"
  export DCC_BACKUP_REPO="$REPO" DCC_BACKUP_MARKER="$MARKER"
  local AUTH="Authorization: Basic $(printf 'x-access-token:%s' "$GITHUB_BACKUP_TOKEN" | base64 -w0)"

  # (all exclusions live in backup-sync.py)

  cd "$REPO"
  git remote get-url origin >/dev/null 2>&1 && git remote set-url origin "$URL" || git remote add origin "$URL"

  # 1. pull-first: fetch GitHub main, apply upstream changes to live (3-way vs the marker), fast-forward staging
  git -c credential.helper= -c "http.extraHeader=$AUTH" fetch -q origin "+refs/heads/main:refs/remotes/origin/main"
  local rc=0
  python3 "$SYNC" --pull || rc=$?
  if [ "$rc" -ne 0 ]; then
    if [ "$rc" -eq 3 ]; then
      echo "BACKUP STOPPED: CONFLICT (exit 3). Nothing was pushed. Flag Caleb with the CONFLICT/BLOCKED lines above." >&2
    else
      echo "BACKUP STOPPED: pull step exit $rc. Nothing was pushed." >&2
    fi
    return "$rc"
  fi

  # 2. mirror live -> staging, safety checks, commit, push
  python3 "$SYNC"   # rsync-like full mirror (rsync is not installed)
  cp ops/hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit   # credential-only hook
  # --force: mirrored folders carry their own .gitignore (e.g. discord-voice-bridge ignores logs/ and *.log); the
  # mirror already decides what belongs here, so nested ignore files must not drop logs.
  git add -A --force
  # safety checks (on the staged tree): credentials only
  python3 ops/check_repo_safe.py --staged
  # Secret grep. gm-notes/secret/ is skipped by design (GM etiquette: roll/affinity data, never read; copied byte-for-byte).
  # -- ends options so a tracked file named like --help cannot make grep print usage (and trip this check).
  if git ls-files -z -- . ':(exclude)gm-notes/secret' | xargs -0 -r sh -c 'grep -IlE \
     -e "github_pat_[A-Za-z0-9_]{20,}" -e "gh[pousr]_[A-Za-z0-9]{30,}" -e "sk-[A-Za-z0-9_-]{20,}" -e "sk_[0-9a-f]{40,}" \
     -e "discord(app)?\.com/api/(v[0-9]+/)?webhooks/[0-9]+" -e "[MNO][A-Za-z0-9_-]{23,27}\.[A-Za-z0-9_-]{6,7}\.[A-Za-z0-9_-]{27,}" \
     -- "$@"' sh ; then
    echo "STOP: secret-looking pattern found in files listed above" >&2; return 1
  fi
  if [ -n "${DRY_RUN:-}" ]; then
    echo "changed paths vs last commit: $(git status --short | wc -l)"
    echo "files in tree: $(git ls-files | wc -l)"
    echo "tree size: $(git ls-files -z | xargs -0 du -cb --apparent-size | tail -1 | cut -f1) bytes"
    echo "DRY_RUN: stopping before commit"; return 0
  fi
  if git diff --cached --quiet; then echo "Nothing to commit."; else
    git -c user.name="Borent Architect" -c user.email="borent-architect@users.noreply.github.com" commit -q --author="Borent Architect <borent-architect@users.noreply.github.com>" -m "$MSG"
  fi
  git -c credential.helper= -c "http.extraHeader=$AUTH" push origin main:main   # never --force
  local LOCAL REMOTE
  LOCAL="$(git rev-parse HEAD)"
  REMOTE="$(git -c credential.helper= -c "http.extraHeader=$AUTH" ls-remote origin refs/heads/main | cut -f1)"
  echo "local : $LOCAL"
  echo "remote: $REMOTE"
  # 3. marker = what GitHub now holds from this backup (base for the next pull-first 3-way)
  if [ "$LOCAL" = "$REMOTE" ]; then
    printf '%s\n' "$LOCAL" > "$MARKER.tmp" && mv "$MARKER.tmp" "$MARKER"
    echo "marker: $LOCAL -> $MARKER"
  else
    echo "WARN: remote main != local HEAD after push; marker left at $(cat "$MARKER" 2>/dev/null)" >&2; return 5
  fi
  if [ "$URL" = "$GH_URL" ]; then
    curl -s -H "$AUTH" -H 'Accept: application/vnd.github+json' https://api.github.com/repos/Rocket-Fewell/dcc-crawler-protocol | python3 -c 'import sys,json; print("private=",json.load(sys.stdin).get("private"))'
  fi
}
main "$@"; exit $?
