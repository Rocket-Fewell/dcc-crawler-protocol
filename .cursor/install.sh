#!/usr/bin/env bash
# Cloud Agent install. Idempotent. Must exit.
set -euo pipefail

if ! command -v ffmpeg >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends ffmpeg ca-certificates
fi

if ! command -v node >/dev/null 2>&1 || ! node -e 'const p=process.versions.node.split(".").map(Number); if (p[0]<22 || (p[0]===22 && p[1]<12)) process.exit(1)'; then
  NODE_VERSION=22.22.2
  curl -fsSL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz" \
    | sudo tar -xJ -C /usr/local --strip-components=1
fi

bash "$(dirname "$0")/layout.sh"

npm ci --prefix /workspace/discord-voice-bridge
npm ci --prefix /workspace/bot
