# Discord Voice Bridge
# Node >= 22.12 is required by @discordjs/voice 0.19 (DAVE / E2EE voice support).
FROM node:22-bookworm-slim

# ffmpeg is required to transcode TTS audio (mp3) to Opus for Discord.
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg ca-certificates tini \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV NODE_ENV=production

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY src ./src
COPY scripts ./scripts
# Usage log (mount a volume here to keep it: see docker-compose.yml)
RUN mkdir -p /app/logs && chown node:node /app/logs

USER node
# tini reaps ffmpeg child processes and forwards SIGTERM for a clean shutdown.
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["node", "src/index.js"]
