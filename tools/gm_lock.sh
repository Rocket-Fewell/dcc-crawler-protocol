#!/bin/bash
# Single-run lock for the Discord GM routine. Usage: gm_lock.sh acquire|release [session]
# The lock is per campaign session: alpha (default) uses sessions/.gm-lock, any other session uses sessions-data/<id>/.gm-lock.
# Session = 2nd argument, else $DCC_SESSION, else the persisted active session (sessions/active-session.json), else alpha.
# acquire: exit 0 if lock taken, exit 1 if another run holds a fresh lock (<120s old).
C=${DCC_CAMPAIGN_DIR:-/workspace/dcc-campaign}
S=${2:-${DCC_SESSION:-}}
if [ -z "$S" ] && [ -f "$C/sessions/active-session.json" ]; then
  S=$(sed -n 's/.*"session"[[:space:]]*:[[:space:]]*"\([a-z0-9_-]*\)".*/\1/p' "$C/sessions/active-session.json" | head -1)
fi
S=${S:-alpha}
if [ "$S" = "alpha" ]; then D="$C/sessions/.gm-lock"; else D="$C/sessions-data/$S/.gm-lock"; mkdir -p "$C/sessions-data/$S"; fi
case "$1" in
  acquire)
    if [ -d "$D" ]; then
      age=$(( $(date +%s) - $(stat -c %Y "$D") ))
      if [ "$age" -lt 120 ]; then echo "busy"; exit 1; fi
      rmdir "$D" 2>/dev/null || rm -rf "$D"
    fi
    mkdir "$D" 2>/dev/null && echo "acquired" && exit 0
    echo "busy"; exit 1 ;;
  release) rmdir "$D" 2>/dev/null; echo "released" ;;
  *) echo "usage: $0 acquire|release"; exit 2 ;;
esac
