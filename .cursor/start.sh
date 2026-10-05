#!/usr/bin/env bash
# Cloud Agent only. Recreates the dcc-campaign and dcc-lore compat aliases
# next to this checkout. The campaign tools should not depend on this.
# No package installs here.
set -euo pipefail
bash "$(dirname "$0")/layout.sh"
