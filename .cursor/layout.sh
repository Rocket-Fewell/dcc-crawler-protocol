#!/usr/bin/env bash
# Cloud Agent only. Compat shim for older lookups of dcc-campaign and dcc-lore
# next to this checkout. The campaign tools should not depend on this.
# tables/ under dcc-campaign is a bind mount, not a symlink: the voice-bridge
# tests copy that directory into a sandbox and then write fixtures into the copy.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

ln -sfn "$ROOT/lore" "$ROOT/dcc-lore"

mkdir -p "$ROOT/dcc-campaign"
for item in \
  rules floors decisions tools tools-notes guides characters \
  gm-notes sessions exports bot \
  DECISIONS.md INDEX.md STATE-OF-BUILD.md NAMING-CONVENTIONS.md README.md
do
  ln -sfn "$ROOT/${item}" "$ROOT/dcc-campaign/${item}"
done

tables="$ROOT/dcc-campaign/tables"
if mountpoint -q "$tables"; then
  sudo umount "$tables"
fi
if [ -L "$tables" ]; then
  rm "$tables"
fi
mkdir -p "$tables"
# A bind mount is not stored in the environment snapshot. Keep a real copy on
# disk, then mount the live tables over it when this machine is running.
rsync -a --delete "$ROOT/tables/" "$tables/"
sudo mount --bind "$ROOT/tables" "$tables"
