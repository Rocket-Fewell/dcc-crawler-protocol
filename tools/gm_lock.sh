#!/bin/bash
# Single-run lock for the Discord GM routine. Usage: gm_lock.sh acquire|release|status [session]
# The lock is per campaign session: alpha (default) uses sessions/.gm-lock, any other session uses sessions-data/<id>/.gm-lock.
# Session = 2nd argument, else $DCC_SESSION, else the persisted active session (sessions/active-session.json), else alpha.
# acquire: exit 0 if lock taken, exit 1 if another run holds a fresh lock (<120s old).
# The lock dir holds an `owner` file (token=$DCC_GM_LOCK_TOKEN, ppid = the calling shell) so `discord_gm.py new` can tell
# whether THIS run holds the lock; it only marks transcript lines read for the holder (see gm-notes/50-cursor-gm-runbook.md).
# Preferred: `discord_gm.py new --lock --wait 90` takes the lock and reads in one step; release with this script or `discord_gm.py unlock`.
C=${DCC_CAMPAIGN_ROOT:-${DCC_CAMPAIGN_DIR:-$(cd "$(dirname "$0")/.." && pwd)}}
S=${2:-${DCC_SESSION:-}}
if [ -z "$S" ] && [ -f "$C/sessions/active-session.json" ]; then
  S=$(sed -n 's/.*"session"[[:space:]]*:[[:space:]]*"\([a-z0-9_-]*\)".*/\1/p' "$C/sessions/active-session.json" | head -1)
fi
S=${S:-alpha}
if [ -n "${DCC_GM_LOCK_DIR:-}" ]; then D="$DCC_GM_LOCK_DIR"
elif [ "$S" = "alpha" ]; then D="$C/sessions/.gm-lock"; else D="$C/sessions-data/$S/.gm-lock"; mkdir -p "$C/sessions-data/$S"; fi
case "$1" in
  acquire)
    if [ -d "$D" ]; then
      age=$(( $(date +%s) - $(stat -c %Y "$D") ))
      if [ "$age" -lt 120 ]; then echo "busy"; exit 1; fi
      rm -f "$D/owner" 2>/dev/null; rmdir "$D" 2>/dev/null || rm -rf "$D"
    fi
    if mkdir "$D" 2>/dev/null; then
      printf 'token=%s\nppid=%s\npid=%s\nat=%s\n' "${DCC_GM_LOCK_TOKEN:-}" "$PPID" "$$" "$(date +%s)" > "$D/owner" 2>/dev/null
      echo "acquired"; exit 0
    fi
    echo "busy"; exit 1 ;;
  release) rm -f "$D/owner" 2>/dev/null; rmdir "$D" 2>/dev/null; echo "released" ;;
  status)
    if [ -d "$D" ] && [ $(( $(date +%s) - $(stat -c %Y "$D") )) -lt 120 ]; then echo "held"; else echo "free"; fi ;;
  *) echo "usage: $0 acquire|release|status [session]"; exit 2 ;;
esac
