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
if mountpoint -q "$tables"; then
  sudo umount "$tables"
fi
if [ -L "$tables" ]; then
  rm "$tables"
fi
mkdir -p "$tables"
# A bind mount is not stored in the environment snapshot. Keep a real copy on
# disk, then mount the live tables over it when this machine is running.
rsync -a --delete /workspace/tables/ "$tables/"
sudo mount --bind /workspace/tables "$tables"
