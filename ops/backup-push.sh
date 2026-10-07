#!/usr/bin/env bash
# FULL backup: pull GitHub first, mirror the whole DCC project -> staging repo, credential-check, commit, push to the
# private GitHub backup.
# BRANCH MODE (default since 2026-10-05, decision 035 "nothing reaches main without review and a bot vote"): the mirror is
# committed to branch backup/nightly (based on current origin/main every run, by merge, never force) and pushed there;
# a standing PR merges it into main. This script never pushes main, never force-pushes, never deletes branches and does
# not open the PR. Steps: pull-first (unchanged) -> branch = origin/backup/nightly + merge origin/main (conflict: abort,
# push nothing, CONFLICT line, exit 3) or a new branch from origin/main -> mirror -> same secret checks -> if the tree
# equals origin/main: "NO CHANGES vs main", push nothing -> commit, push backup/nightly -> BACKUP SUMMARY block
# (added/modified/deleted vs origin/main, deleted paths, NEEDS_CALEB: yes|no).
# Markers: .backup-last-synced-sha = last origin/main applied to live (pull-first base); .backup-last-branch-sha = branch
# head this backup last pushed (backup-sync.py OWN rule: merged backup content is not mistaken for a GitHub edit).
# BACKUP_TARGET=main restores the old push-to-main behaviour (emergencies only). Default BACKUP_TARGET=branch.
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
# live, no push; branch mode also commits locally on the staging branch so the summary has a head sha - the next run
# resets the local branch to GitHub's)
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
  local BRANCH_MARKER="${DCC_BACKUP_BRANCH_MARKER:-$BOX/.backup-last-branch-sha}"
  local TARGET="${BACKUP_TARGET:-branch}"
  local BRANCH=backup/nightly   # fixed on purpose (no env override): the push refspec can never name main
  local MSG="${1:-Sync campaign design files}"
  : "${GITHUB_BACKUP_TOKEN:?GITHUB_BACKUP_TOKEN not set}"
  case "$TARGET" in branch|main) ;; *) echo "STOP: BACKUP_TARGET must be 'branch' (default) or 'main', got '$TARGET'" >&2; return 1;; esac
  echo "BACKUP_TARGET=$TARGET"
  export DCC_BACKUP_REPO="$REPO" DCC_BACKUP_MARKER="$MARKER" DCC_BACKUP_BRANCH_MARKER="$BRANCH_MARKER"
  local AUTH="Authorization: Basic $(printf 'x-access-token:%s' "$GITHUB_BACKUP_TOKEN" | base64 -w0)"
  local ID=(-c user.name="Borent Architect" -c user.email="borent-architect@users.noreply.github.com")

  # (all exclusions live in backup-sync.py)

  cd "$REPO"
  git remote get-url origin >/dev/null 2>&1 && git remote set-url origin "$URL" || git remote add origin "$URL"

  # 0. the pull fast-forwards staging's local main, so staging must sit on main (after a branch-mode run it sits on
  # backup/nightly). Uncommitted mirror output is regenerated every run and may be dropped; staging-owned files
  # (STAGING_OWNED in backup-sync.py) are not regenerated, so an uncommitted edit to one stops the run.
  if [ "$(git symbolic-ref -q --short HEAD || true)" != main ]; then
    local OWNED_DIRTY
    OWNED_DIRTY="$(git status --porcelain -- .gitignore README.md ops/check_repo_safe.py ops/hooks/pre-commit ops/README.md)"
    if [ -n "$OWNED_DIRTY" ]; then
      printf '%s\n' "$OWNED_DIRTY" >&2
      echo "BACKUP STOPPED: staging-owned file(s) above have uncommitted edits on $(git rev-parse --abbrev-ref HEAD); commit or move them first. Nothing was pushed." >&2
      return 4
    fi
    git checkout -q -f main
  fi

  # 1. pull-first: fetch GitHub main, apply upstream changes to live (3-way vs the marker), fast-forward staging
  git -c credential.helper= -c "http.extraHeader=$AUTH" fetch -q origin "+refs/heads/main:refs/remotes/origin/main"
  # also fetch backup/nightly if it exists (read-only), so the pull's OWN rule has the last pushed branch head's objects
  local RB
  RB="$(git -c credential.helper= -c "http.extraHeader=$AUTH" ls-remote origin "refs/heads/$BRANCH" | cut -f1)"
  if [ -n "$RB" ]; then
    git -c credential.helper= -c "http.extraHeader=$AUTH" fetch -q origin "+refs/heads/$BRANCH:refs/remotes/origin/$BRANCH"
  fi
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
  local UP FOREIGN=no
  UP="$(git rev-parse refs/remotes/origin/main)"

  # 1b. branch mode: live now holds origin/main -> record it (pull-first base), then put staging on backup/nightly
  if [ "$TARGET" = branch ]; then
    if [ -z "${DRY_RUN:-}" ]; then
      printf '%s\n' "$UP" > "$MARKER.tmp" && mv "$MARKER.tmp" "$MARKER"
      echo "marker: origin/main $UP applied to live -> $MARKER"
    fi
    if [ -n "$RB" ]; then
      if [ "$RB" != "$(cat "$BRANCH_MARKER" 2>/dev/null || true)" ]; then
        FOREIGN=yes
        echo "WARN: origin/$BRANCH is at ${RB:0:12}, not the head this backup last pushed ($(cat "$BRANCH_MARKER" 2>/dev/null || echo none)). Someone else committed to it; the mirror will replace their edits with live wherever they differ. NEEDS_CALEB." >&2
      fi
      git checkout -q -f -B "$BRANCH" "refs/remotes/origin/$BRANCH"
      if ! git "${ID[@]}" merge -q --no-edit -m "Merge origin/main into $BRANCH" "$UP" >/dev/null 2>&1; then   # quiet: git would print paths unmasked
        git diff --name-only --diff-filter=U | sed 's#^gm-notes/secret/.*#gm-notes/secret/<file>#; s#^#CONFLICT path: #' >&2
        git merge --abort 2>/dev/null || true
        git checkout -q -f main
        echo "CONFLICT: merging origin/main ${UP:0:12} into $BRANCH ${RB:0:12} conflicts (merge aborted). Nothing was pushed. Flag Caleb: resolve on GitHub (update the PR branch) or merge/close the PR, then re-run." >&2
        return 3
      fi
      echo "branch: $BRANCH = origin/$BRANCH ${RB:0:12} + origin/main ${UP:0:12} -> $(git rev-parse --short=12 HEAD)"
    else
      git checkout -q -f -B "$BRANCH" "$UP"
      echo "branch: $BRANCH not on GitHub yet; created locally from origin/main ${UP:0:12}"
    fi
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
  # Allowlist (Caleb order 2026-10-07): secrets/cursor-gm-secrets.env holds plain-text bot tokens for the Cursor GM
  # in this private repo on purpose. Exactly that one path is skipped here; every other file is still grepped.
  if git ls-files -z -- . ':(exclude)gm-notes/secret' ':(exclude,literal)secrets/cursor-gm-secrets.env' | xargs -0 -r sh -c 'grep -IlE \
     -e "github_pat_[A-Za-z0-9_]{20,}" -e "gh[pousr]_[A-Za-z0-9]{30,}" -e "sk-[A-Za-z0-9_-]{20,}" -e "sk_[0-9a-f]{40,}" \
     -e "discord(app)?\.com/api/(v[0-9]+/)?webhooks/[0-9]+" -e "[MNO][A-Za-z0-9_-]{23,27}\.[A-Za-z0-9_-]{6,7}\.[A-Za-z0-9_-]{27,}" \
     -- "$@"' sh ; then
    echo "STOP: secret-looking pattern found in files listed above" >&2; return 1
  fi
  if [ "$TARGET" = branch ]; then
    branch_finish; return $?
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
# Branch mode, after mirror + secret checks (runs in main()'s scope: uses its locals).
branch_finish() {
  if git diff --cached --quiet "$UP"; then
    echo "NO CHANGES vs main"
    backup_summary "no_changes" "$(git rev-parse HEAD)"; return 0
  fi
  if ! git diff --cached --quiet; then
    git "${ID[@]}" commit -q --author="Borent Architect <borent-architect@users.noreply.github.com>" -m "$MSG"
  fi
  local HEAD_SHA; HEAD_SHA="$(git rev-parse HEAD)"
  if [ -n "${DRY_RUN:-}" ]; then
    echo "DRY_RUN: committed locally on $BRANCH (${HEAD_SHA:0:12}), NOT pushed"
    backup_summary "dry_run_not_pushed" "$HEAD_SHA"; return 0
  fi
  if [ "$HEAD_SHA" = "$RB" ]; then
    echo "origin/$BRANCH already holds this tree; nothing to push"
  else
    case "$BRANCH" in main|master|"") echo "STOP: refusing to push to '$BRANCH'" >&2; return 1;; esac
    git -c credential.helper= -c "http.extraHeader=$AUTH" push origin "refs/heads/$BRANCH:refs/heads/$BRANCH"   # never --force
  fi
  local REMOTE MAIN_NOW
  REMOTE="$(git -c credential.helper= -c "http.extraHeader=$AUTH" ls-remote origin "refs/heads/$BRANCH" | cut -f1)"
  MAIN_NOW="$(git -c credential.helper= -c "http.extraHeader=$AUTH" ls-remote origin refs/heads/main | cut -f1)"
  echo "local : $HEAD_SHA"
  echo "remote: $REMOTE ($BRANCH)"
  echo "main  : $MAIN_NOW (origin/main at start: $UP)"
  if [ "$HEAD_SHA" != "$REMOTE" ]; then
    echo "WARN: remote $BRANCH != local HEAD after push; branch marker left at $(cat "$BRANCH_MARKER" 2>/dev/null)" >&2; return 5
  fi
  printf '%s\n' "$HEAD_SHA" > "$BRANCH_MARKER.tmp" && mv "$BRANCH_MARKER.tmp" "$BRANCH_MARKER"
  echo "branch marker: $HEAD_SHA -> $BRANCH_MARKER"
  if [ "$URL" = "$GH_URL" ]; then
    curl -s -H "$AUTH" -H 'Accept: application/vnd.github+json' https://api.github.com/repos/Rocket-Fewell/dcc-crawler-protocol | python3 -c 'import sys,json; print("private=",json.load(sys.stdin).get("private"))'
  fi
  backup_summary "pushed" "$HEAD_SHA"
}

# Machine-readable summary vs origin/main ($UP). gm-notes/secret/ names are never printed (masked).
backup_summary() {
  local RESULT="$1" HEAD_SHA="$2"
  local DIFF_ARGS=("$UP" "$HEAD_SHA")
  [ "$RESULT" = "no_changes" ] && DIFF_ARGS=(--cached "$UP")
  git diff --name-status --no-renames -z "${DIFF_ARGS[@]}" | \
    RESULT="$RESULT" HEAD_SHA="$HEAD_SHA" BRANCH="$BRANCH" UP="$UP" FOREIGN="$FOREIGN" python3 -c '
import os, re, sys
toks = sys.stdin.buffer.read().decode("utf-8", "surrogateescape").split("\0")
add, mod, dele = [], [], []
for st, rel in zip(toks[0::2], toks[1::2]):
    if not st: continue
    (add if st[0] == "A" else dele if st[0] == "D" else mod).append(rel)
SECRETY = re.compile(r"(^|/)\.env($|\.)|secret|credential|passw|token|api[_-]?key|private[_-]?key|webhook|id_rsa|id_ed25519|\.(pem|key|p12|pfx)$", re.I)
show = lambda r: "gm-notes/secret/<file>" if r.startswith("gm-notes/secret/") else r
sec = [r for r in add + mod + dele if SECRETY.search(r)]
foreign = os.environ["FOREIGN"] == "yes"
ROTATING = re.compile(r"^(dcc-campaign/)?sessions(-data/[^/]+)?/backups/")  # auto-rotated state snapshots, not content deletions
real_dele = [r for r in dele if not ROTATING.search(r)]
need = bool(real_dele or sec or foreign)
e = os.environ
print("=== BACKUP SUMMARY ===")
print("target: branch")
print("branch: " + e["BRANCH"])
print("result: " + e["RESULT"])
print("head_sha: " + e["HEAD_SHA"])
print("origin_main_sha: " + e["UP"])
print("added: %d" % len(add))
print("modified: %d" % len(mod))
print("deleted: %d" % len(dele))
for r in dele: print("deleted_path: " + show(r) + ("  (rotating snapshot)" if r not in real_dele else ""))
print("deleted_content_files: %d" % len(real_dele))
print("secret_related_paths: %d" % len(sec))
for r in sec: print("secret_related_path: " + show(r))
print("foreign_commits_on_branch: " + ("yes" if foreign else "no"))
print("NEEDS_CALEB: " + ("yes" if need else "no"))
print("=== END BACKUP SUMMARY ===")
'
}
main "$@"; exit $?
