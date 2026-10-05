#!/usr/bin/env bash
# Recreate the historical /workspace/dcc-campaign and /workspace/dcc-lore paths.
# tables/ is a bind mount, not a symlink: the voice-bridge tests copy that
# directory into a sandbox and then write fixtures into the copy.
set -euo pipefail

ln -sfn /workspace/lore /workspace/dcc-lore

for name in item-reskins.json item-reskins.version.json; do
  ln -sfn "/workspace/lore/tables/${name}" "/workspace/tables/${name}"
done

mkdir -p /workspace/dcc-campaign
for item in \
  rules floors decisions tools tools-notes guides characters \
  gm-notes sessions exports bot \
  DECISIONS.md INDEX.md STATE-OF-BUILD.md NAMING-CONVENTIONS.md README.md
do
  ln -sfn "/workspace/${item}" "/workspace/dcc-campaign/${item}"
done

tables=/workspace/dcc-campaign/tables
if [ -L "$tables" ]; then
  rm "$tables"
fi
mkdir -p "$tables"
if ! mountpoint -q "$tables"; then
  sudo mount --bind /workspace/tables "$tables"
fi
