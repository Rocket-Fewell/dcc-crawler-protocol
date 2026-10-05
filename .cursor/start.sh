#!/usr/bin/env bash
# Per-boot layout. The campaign tools and the voice bridge default to
# /workspace/dcc-campaign and /workspace/dcc-lore. No package installs here.
set -euo pipefail
bash "$(dirname "$0")/layout.sh"
