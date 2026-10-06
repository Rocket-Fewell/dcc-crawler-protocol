# Discord Voice Bridge (AI-GM edition)

A Discord bot that connects a tabletop RPG voice channel to an AI Game Master — built for a *Dungeon Crawler Carl* style campaign, but nothing in it is campaign-specific.

```
 players talk in voice ──► [STT bridge] ──► Whisper / gpt-4o-transcribe ──► #transcript   ──► (your AI GM reads this)
 (your AI GM writes)   ──► #gm-output ──► [TTS bridge] ──► OpenAI TTS / ElevenLabs ──► spoken in the voice channel
```

* **STT** – per-user receive streams (`@discordjs/voice`) → Opus decode → 16 kHz mono WAV → OpenAI transcription. End of utterance = ~1 s of silence. Short/quiet clips and known Whisper hallucinations ("Thanks for watching") are dropped. Posts `**DisplayName**: "text"`. Other bots and the bot itself are never transcribed.
* **TTS** – every new message in the GM output channel is parsed for voice tags (see below), stripped of markdown/emoji/code, split into sentence-size chunks, synthesized (prefetching a couple of chunks ahead) and played in order, using the narrator or the System voice per line. `/skip` and `/say` included.
* **Slash commands:** `/join [channel]`, `/leave`, `/skip [all]`, `/say <text> [voice: gm|system]`, `/voicecap [action: reset|set] [minutes]`, `/shush`, `/gm <pause|resume|status>`, `/session <status|list|use>`, `/create` (character creation, below), `/crawlers`, `/delete <name>`, `/encounter` (GM only, below). Twelve in all (`/encounter` is built and tested but NOT registered yet); `npm run register` is only needed when a command's name, options or description changes.

---

## Requirements

| Thing | Version / note |
|---|---|
| **Node.js** | **>= 22.12.0**. The task brief said ">=20", but Discord now **requires** DAVE (end-to-end encrypted voice) and the first `@discordjs/voice` release with DAVE (0.19.x) declares `engines.node >= 22.12.0`. `@discordjs/voice` 0.18 (Node 18+) has no DAVE and will be refused by Discord's voice servers. |
| **ffmpeg** | Must be on `PATH` (`apt install ffmpeg`, `brew install ffmpeg`, or included in the Dockerfile). Used by `prism-media` to turn TTS MP3 into 48 kHz Opus. |
| **Discord DAVE (E2EE)** | Handled by `@discordjs/voice` ^0.19.2 + `@snazzah/davey` (a prebuilt native lib, listed as an explicit dependency). `joinVoiceChannel` is called with `daveEncryption: true`. Run `npm run doctor` and confirm the "DAVE Libraries" section shows `@snazzah/davey`. |
| **Opus** | `opusscript` (pure JS/WASM, no compile step) is the default decoder. For lower CPU you can optionally `npm i @discordjs/opus` (native build; needs a build toolchain). |
| **Encryption** | `sodium-native` (prebuilt) + Node's native `aes-256-gcm`. |
| **API keys** | OpenAI (STT, and TTS by default). ElevenLabs only if `TTS_PROVIDER=elevenlabs`. Fish Audio only if `TTS_PROVIDER=fish`. |

Dependency versions were checked against npm on 2026-10-03: discord.js 14.27.0, @discordjs/voice 0.19.2, @snazzah/davey 0.1.12, prism-media 1.3.5, opusscript 0.0.8 (pinned to `^0.0.8` because prism-media 1.3.5 peer-depends on it; 0.1.x causes an `ERESOLVE`), dotenv 18.0.5, sodium-native 5.1.0. `npm audit` reports 0 vulnerabilities. STT/TTS HTTP calls use Node's built-in `fetch`, so there is no OpenAI SDK dependency.

---

## Setup, step by step

### 1. Create the Discord application and bot
1. Go to <https://discord.com/developers/applications> → **New Application**.
2. **General Information** → copy the **Application ID** → this is `CLIENT_ID`.
3. **Bot** tab → **Reset Token** → copy it → this is `DISCORD_TOKEN` (keep it secret).
4. Still on the **Bot** tab, under **Privileged Gateway Intents**, turn on **MESSAGE CONTENT INTENT** and save. (Without it the bot cannot read GM messages in order to speak them. Guilds, Guild Voice States and Guild Messages are non-privileged and requested automatically.)
5. Leave "Public Bot" off if you don't want others inviting it.

### 2. Invite the bot
Open this URL (replace `YOUR_CLIENT_ID`):

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot%20applications.commands&permissions=3214336
```

`permissions=3214336` = **View Channels** (1024) + **Send Messages** (2048) + **Read Message History** (65536) + **Connect** (1048576) + **Speak** (2097152). Scopes: `bot` and `applications.commands`.

Make sure the bot's role can see/connect/speak in your voice channel and can view + send in the transcript channel and view + read history in the GM output channel (channel-level overrides win over role permissions).

### 3. Get the IDs
Discord → **User Settings → Advanced → Developer Mode ON**. Then right-click and **Copy ID**:
* server icon → `GUILD_ID`
* voice channel → `VOICE_CHANNEL_ID`
* transcript text channel → `TRANSCRIPT_CHANNEL_ID`
* GM output text channel → `GM_OUTPUT_CHANNEL_ID`
* (optional) your AI GM's bot/user/webhook → add to `GM_ALLOWED_AUTHOR_IDS` (comma-separated) to speak only that author's messages.

### 4. Install and configure
```bash
cd discord-voice-bridge
node -v                # must be >= 22.12
ffmpeg -version        # must exist
npm install
cp .env.example .env   # then edit .env
npm run doctor         # shows opus / encryption / DAVE / ffmpeg status
```
Fill in at minimum: `DISCORD_TOKEN`, `CLIENT_ID`, `GUILD_ID`, `TRANSCRIPT_CHANNEL_ID`, `GM_OUTPUT_CHANNEL_ID`, `OPENAI_API_KEY` (and `VOICE_CHANNEL_ID` if you want `AUTO_JOIN=true` or a `/join` fallback).

### 5. Register slash commands (once, or when commands change)
```bash
npm run register
```
Commands are registered to your guild only, so they appear instantly.

### 6. Run
```bash
npm start
```
Then, in Discord, sit in the voice channel and type `/join` (or set `AUTO_JOIN=true`). Talk — transcripts appear in the transcript channel. Post in the GM output channel — the bot reads it aloud.

---

## Fish Audio provider (`TTS_PROVIDER=fish`)

Custom-voice TTS via <https://docs.fish.audio> (`POST https://api.fish.audio/v1/tts`, `Authorization: Bearer $FISH_API_KEY`, a `model` header, JSON body with `reference_id`). The default stays `openai`; nothing changes until you set `TTS_PROVIDER=fish`.

```env
TTS_PROVIDER=fish
FISH_API_KEY=...                      # secret; never logged or printed (also scrubbed from error text)
FISH_VOICE_ID_NARRATOR=<model id>     # [GM] and untagged lines
FISH_VOICE_ID_SYSTEM=<model id>       # [SYSTEM] lines
FISH_MODEL=s2.1-pro                   # optional
```
* **Tag contract is unchanged:** `[SYSTEM]` -> system voice id, `[GM]`/untagged -> narrator voice id, `[ROLL]` is never sent to Fish (it is dropped before synthesis). If only one voice id is set it is used for both (a startup warning says so). `/say voice:system|gm` works the same way.
* **Prepaid credit and cost**: Fish bills $15 per 1M UTF-8 bytes of text. `npm run usage` prints the bytes cost per day and per bot session (bytes are logged per synthesized message, never the text) and the live balance from `GET https://api.fish.audio/wallet/self/api-credit` (`credit` is dollars as a string; `--no-balance` skips the request). The bridge checks the balance at startup, every ~30 minutes and after each session closes; under `$FISH_LOW_BALANCE_USD` (default 3) it logs ONE warning and, if the session's `create.staff_channel_id` is set, posts it there (text only, never spoken, no `[SYSTEM]` tag). The key is never printed.
* **Voice ids (`reference_id`)**: the id of a Fish voice model. Per the Fish docs, find ids in the Voice Library or create your own via Voice Cloning; ids look like `9a9cf47702da476aa4629e2506d4a857` (32 hex characters, normally visible in the voice's page URL in the dashboard). Via API: `curl -H "Authorization: Bearer $FISH_API_KEY" "https://api.fish.audio/model?self=true&page_size=50"` lists your models (`_id` is the reference id); drop `self=true` and add `&title=...` to search the library.
* **Try it with a real key** (spends a few characters of credit; the key is never printed): put the three `FISH_*` values in `.env`, then `node scripts/fish-smoke.js "Test line"`. It writes `fish-smoke-gm.mp3` and `fish-smoke-system.mp3` and prints time-to-first-audio. Then set `TTS_PROVIDER=fish`, restart, `/join`, post `[SYSTEM] hello` in the GM channel, and run `npm run usage`.
* **Models** (`FISH_MODEL`, sent as the `model` header): `s2.1-pro` (default; Fish's recommended production model), `s2.1-pro-free` ($0 for testing/small use, no latency guarantees), `s2-pro`, `s1`. Docs say an omitted/unknown model falls back to `s2.1-pro`.
* **Streaming / latency:** the bot reads Fish's chunked HTTP response as a stream and hands it to ffmpeg while it is still arriving, so playback starts on the first audio bytes instead of after the whole chunk is generated. `FISH_LATENCY=balanced` (default) trades a little quality for speed; use `low` for fastest, `normal` for best quality. Default format is `mp3` (44.1 kHz, 128 kbps); `opus` (48 kHz) and `wav` are also accepted. ffmpeg is still required.
* **Billing & limits (per Fish docs, 2026-10-03):** billed per **UTF-8 byte** of input text, $15 per million bytes on paid models (~12 hours of speech per million bytes); `s2.1-pro-free` is $0. Concurrency limits, not per-minute limits: 5 simultaneous requests (<$100 prepaid), 15 (>=$100), 50 (>=$1000). Over the limit the API returns HTTP 429 with no `Retry-After`; the bot retries with backoff (500 ms, 1 s, 2 s). HTTP 401 = bad key, 402 = no balance (not retried). `TTS_PREFETCH` (default 2) keeps the bot well inside the 5-request starter tier.
* Expression tags: `s1` uses `(parenthesis)` emotion tags; the S2 family accepts natural-language expression control in text (see Fish's Emotion Control docs). The bot only strips Markdown, so such tags pass through to Fish. Tag syntax is model-specific: test before relying on it. Avoid `[...]` at the *start of a line* in GM output, because the bot reads those as `[SYSTEM]/[GM]/[ROLL]` tags.

## TTS usage log and credit tracking

Every synthesized chunk (any provider) appends one line to `logs/tts-usage.jsonl` (override with `TTS_USAGE_LOG`; disable with `TTS_USAGE_LOG_ENABLED=false`). Only counts are stored - never text or keys:

```json
{"ts":"2026-10-03T23:10:04.120Z","date":"2026-10-03","month":"2026-10","session":"20261003T231000-a1b2","provider":"fish","voice":"system","model":"s2.1-pro","chars":212,"utf8_bytes":214,"minutes":0.2358,"minutes_source":"estimate","audio_seconds":null,"ok":true}
```
`session` identifies one run of the bot process. `voice` is the tag voice (`gm`/`system`). `minutes` is the real audio duration when known (Fish MP3 is fixed-bitrate, so duration is computed exactly from the bytes received; `minutes_source:"audio"`), otherwise `chars / 900` (`TTS_USAGE_CHARS_PER_MINUTE`; `minutes_source:"estimate"`). Failed synths are logged with `ok:false` and excluded from totals.

```bash
npm run usage                                   # per day, per month, per bot session (grouped by date), per voice + monthly cap
node scripts/tts-usage-summary.js --month 2026-10 --provider fish
node scripts/tts-usage-summary.js --wake-file PATH   # GM wake-up counts (default logs/wake-usage.jsonl)
node scripts/tts-usage-summary.js --json        # or --csv, for the accountant's spreadsheet
FISH_MONTHLY_CAP_MINUTES=300 node scripts/tts-usage-summary.js --fail-on-warn   # exit 3 at >= 80% (cron/alerts)
```
The cap check (default **200 minutes/month**, `FISH_MONTHLY_CAP_MINUTES` or `--cap`) covers the Fish provider by default (`--cap-provider all` for everything) for the selected/current month, prints percent used and minutes remaining, **warns at 80%** and flags at 100%. The report also shows estimated Fish cost (UTF-8 bytes x $15/M; `$0` for `-free` models) - an estimate, not an invoice. Back up or rotate `logs/` like any log (it is gitignored and mounted as a volume in `docker-compose.yml`).

## Per-session voice cap (`FISH_SESSION_CAP_MINUTES`)

A hard limit on how many minutes of GM speech one voice session may spend (default **50**, `0` = off). A *session* starts at `/join` (or auto-join) and ends at `/leave` or a bot restart; **the counter resets on every new join**. It applies to whichever `TTS_PROVIDER` is active (the name is Fish-flavoured because that is the metered one).

* The counter uses the same minutes `logs/tts-usage.jsonl` records (measured audio when known, else `chars / TTS_USAGE_CHARS_PER_MINUTE`). Each chunk's estimate is reserved when synthesis starts, so prefetched chunks count immediately.
* **At 80%** the bot logs a warning and posts one notice in the transcript channel (`#table-transcript`, formerly `#dcc_ears`).
* **At 100%** nothing more is synthesized (the provider is not called, so no spend). The bot posts **one** notice in `#table-transcript` saying the session voice cap was reached and that text continues in the GM channel (`#dcc_mouth`), then stays quiet; GM messages keep appearing there as text. `/say` is refused with an ephemeral message. Audio already queued or playing finishes.
* `/voicecap` shows `used / cap` minutes (anyone). `/voicecap action:reset` zeroes the counter and re-arms the notices; `/voicecap action:set minutes:90` changes the cap until the bot restarts (`0` = no cap). Reset/set need the **Manage Server** permission (or being the server owner).
* After adding the command, register it once: `npm run register` (see below), then restart the bot.

## Wake-up filter: spotlight

The DCC AI GM runs "spotlight" exchanges: it addresses one player and listens only to them until it says it is finished. Waking the GM (a paid run) for every other line is wasted, so the wake webhook is filtered. **Transcripts are unaffected**: every line is still posted to the transcript channel; only the wake POST is filtered.

* State file: `<campaign>/sessions/spotlight.json` (`SPOTLIGHT_FILE`; campaign root from `DCC_CAMPAIGN_ROOT` / `DCC_CAMPAIGN_DIR`), `{"player":"<name or null>","aliases":["..."],"updated":"ISO ts","note":""}`. The GM writes it with `python3 tools/discord_gm.py spotlight set|clear|show`. It is read on every line, so changes apply immediately (no restart).
* **Player set** -> a line counts toward a wake only if (a) the speaker's Discord display name or username matches the player or an alias (case- and accent-insensitive; matching if either contains the other; a 1-character name only matches exactly), or (b) the line contains the standalone wake word **AI** (`AI`, `A.I.`, `A I`, `hey AI`, any case; not `said`, `main`, `again`, `mail`...). A wake-word line from a non-spotlight player still wakes the GM (payload shape unchanged; the bridge logs it and counts it as an override).
* **Fails open:** player null/empty, a missing, empty, unreadable or malformed file, a missing/invalid `updated`, or a file older than `SPOTLIGHT_MAX_AGE_MINUTES` (20) all mean *open floor*: every line wakes the GM. An error in the filter never blocks a wake. `SPOTLIGHT_FILTER_ENABLED=false` turns the filter off.
* **Accounting:** each skipped line appends `{ts,date,session,skipped:true,speaker_matched:false,reason:"spotlight",lines:1}` to `logs/wake-usage.jsonl` (no names or text); each fired wake records how many wake-word override lines it carried. `npm run usage` shows per day and per bot session: wakes fired, lines skipped, lines dropped while paused, wake-word overrides, and **estimated wake-ups saved (upper bound = skipped + paused lines; batching would have merged some)**.

## Voice safety commands and protections

* **`/shush`** (anyone, ephemeral reply): stops playback at once and clears the whole speech queue. It does not stop the GM from running (use `/gm pause`).
* **File kill switch:** `python3 tools/discord_gm.py stop` (in the campaign repo) atomically writes `sessions/voice-control.json` (`VOICE_CONTROL_FILE`) as `{"action":"flush","id":"<unique>","ts":"..."}`. The bridge polls it every `VOICE_CONTROL_POLL_MS` (500); a new `id` flushes playback and the queue exactly like `/shush`. The id already in the file when the bot starts is ignored, so a stale file never flushes on boot. Anything posted afterwards is spoken normally.
* **`/gm pause | resume | status`** (anyone, ephemeral): `pause` stops sending the GM wake webhook (transcripts are still posted; lines are logged as skipped, reason `paused`; lines waiting for a wake are dropped). The state is saved to `GM_WAKE_STATE_FILE` and survives restarts; default is on (resumed). `status` also shows whether the webhook is configured and who has the spotlight.
* **Duplicate suppression:** a GM message whose speakable text equals (whitespace/case-normalized), or nearly equals (one contains the other and the shorter is > 90% of the longer), text from the **same author** that was spoken or queued within `DUPLICATE_WINDOW_SECONDS` (120) is dropped before synthesis (no TTS spend) and logged. `/shush`, `/skip` and a flush forget the history, since the text was not actually heard. `0` disables.
* **Backlog safeguard:** if more than `MAX_QUEUED_CHUNKS` (12) chunks or `MAX_QUEUED_SECONDS` (90, estimated as chars / `TTS_USAGE_CHARS_PER_MINUTE`) are pending, the **oldest pending messages are dropped** and the newest is kept (the message currently being spoken and the newest are never dropped, even if one huge message exceeds the limit). One notice is posted in the transcript channel (at most one per minute) and the drop is logged. `0` disables a limit.
* Dropped duplicates, backlog trims and flushes are counted in `logs/voice-events.jsonl` (no message text) and reported by `npm run usage`.

## GM wake webhook (optional)

The AI GM is an agent that only runs when woken. With the wake notifier enabled, the bot POSTs a small JSON webhook whenever **new player speech** lands in the transcript channel (`#table-transcript`, formerly `#dcc_ears`; the channel NAME was changed, the bridge uses IDs; the payload `channel` label stays `dcc_ears`, written by this bot's own STT; GM posts and slash-command text never trigger it).

**It is OFF unless `GM_WEBHOOK_URL` is set.** Restart the bot after changing `.env`.

```json
{"event":"player_speech","channel":"dcc_ears",
 "lines":[{"speaker":"Name","text":"...","ts":"2026-10-04T05:00:00.000Z"}],
 "hint":"Run: python3 tools/discord_gm.py new  then reply with: python3 tools/discord_gm.py say ..."}
```

**Timing**

* **Debounce** – waits `GM_WAKE_DEBOUNCE_MS` (2500) after the *last* line and batches everything in between, so a speaker finishing a sentence sends ONE wake. Capped at `GM_WAKE_MAX_WAIT_MS` (8000) after the first line of the batch.
* **One at a time** – nothing is sent while the previous POST is still in flight; lines that arrive meanwhile go into the next wake.
* **Rate limit** – at most one wake per `GM_WAKE_MIN_INTERVAL_MS` (4000); extra lines are carried forward.
* **No talking over itself** – if the TTS queue is busy or audio is playing, the wake is held until it is idle (max extra wait `GM_WAKE_IDLE_MAX_WAIT_MS`, 15000, then it sends anyway). Lines that arrive in the meantime are included.
* **Failures** – network errors and 5xx are retried once; 4xx are not. After that the batch is dropped (the GM re-reads the channel with `discord_gm.py new` on its next wake), and the bot keeps running. Redirects are not followed.

**Auth** (`GM_WEBHOOK_KEY` is the secret)

| Setup | Result |
|---|---|
| defaults | `Authorization: Bearer <key>` |
| `GM_WEBHOOK_AUTH_SCHEME=Token` | `Authorization: Token <key>` |
| `GM_WEBHOOK_AUTH_HEADER=X-Api-Key` | `X-Api-Key: <key>` (raw key unless a scheme is set) |
| `GM_WEBHOOK_AUTH_SCHEME=` (set, empty) | raw key: `Authorization: <key>` |
| `GM_WEBHOOK_KEY_IN_QUERY=true` (or a param name) | `?key=<key>` appended to the URL, no auth header |

**Secrets** – the URL and key are never logged; logs contain only lines like `GM wake sent: HTTP 200 (2 lines)`, `GM wake failed: HTTP 500`, or `network error ECONNREFUSED` (an error code only). Keep them in `.env` (git-ignored).

**Hourly budget and rate limits** - the GM platform limits automation runs per hour (e.g. `Automation run rate limit exceeded: ... 100 per hour`). The bridge keeps a rolling 60-minute budget, `WAKE_MAX_PER_HOUR` (default **60**, `0` = off), counting every wake POST (each HTTP attempt, so a retried wake counts twice; successful or failed; rate-limited rejections and skipped lines do not count).
* **Budget exhausted:** lines are **held, never dropped**. They accumulate (up to 1000) and go out as **one batched wake** when the oldest counted wake leaves the window. Each held line is logged once to `wake-usage.jsonl` as `{skipped:true, reason:"budget"}` (counted as *held*, not as savings). The first time the budget blocks, one notice is posted in the transcript channel: "GM wake budget reached, replies resume at HH:MM". The logs warn once at 80%.
* **Rate-limit responses:** an HTTP 400 (or 429) whose body contains "rate limit" is treated as a rate limit, not a failure: the lines are kept, the bridge backs off `WAKE_RATE_LIMIT_BACKOFF_MS` (5 minutes), then retries one batched wake. The response body is only checked for that phrase and is never logged or stored; the log shows just `GM wake rate limited (HTTP 400): backing off 5 min`. One notice is posted per episode. A plain 400 is still treated as a failure.
* **Restarts keep the count:** the budget and any running backoff are rebuilt at startup from `logs/wake-usage.jsonl` (needs `WAKE_USAGE_LOG_ENABLED=true`; records written before this feature are counted, except legacy 400s, which were rate-limit rejections). `wake-test` POSTs are not logged, so they are not counted.
* `/gm status` shows "Wakes used in the last hour: N / budget", held lines and the resume time. `npm run usage` shows wakes in the last 60 min vs the budget, and per day/session columns `rate-lim` (wakes the server rejected) and `held` (lines held by the budget).

**Counting wakes** - every wake appends one line to `logs/wake-usage.jsonl` (`{ts,date,session,lines,ok,status}`; no URL, key or text). `npm run usage` reports wake-ups per day and per bot session. Disable with `WAKE_USAGE_LOG_ENABLED=false`; move with `WAKE_USAGE_LOG`.

**Test it** (does not need the bot running): `npm run wake-test` sends one test payload (`"test": true`, speaker "Wake Test") using the `.env` values and prints only `HTTP <status>`. Exit code 0 means a 2xx.

## GM output tag contract

Messages in `GM_OUTPUT_CHANNEL_ID` may tag lines to choose who speaks them. **Decision 032 (Caleb, Oct 5 2026)** splits what each voice is for:

| Tag | Behaviour |
|---|---|
| `[SYSTEM] text` | Spoken in the **System** voice: **dry, informative, corporate** (game clock/timers, fees, registration, collapse warnings, floor notices, welcome/registration announcements). **No jokes.** |
| `[GM] text` | Spoken in the **narrator** voice: **snarky** (achievement banner **and** mocking description, loot-box callouts/openings, all jokes and color) |
| *(no tag)* | Narrator voice (same as `[GM]`) |
| `[ROLL] text` | **Never spoken** (dice math, mechanics bookkeeping) |

Rules:
* Tags are matched **per line**, case-insensitively, at the **start** of a line. Leading whitespace and markdown such as `**[SYSTEM]**` or `> [GM]` is tolerated; an optional `:` after the tag is stripped. A tag in the middle of a line (`He said [SYSTEM] aloud`) is plain text.
* **A tag applies until the next tag**: untagged lines after `[SYSTEM]` stay in the System voice; untagged lines after `[ROLL]` stay silent. Lines before any tag are narrator voice. A message may contain any number of tagged lines.
* **Mixed messages:** if a System line is followed by snark in the same message, **re-tag `[GM]`** before the snark so carry-over does not keep speaking it as System.
* The tag is **stripped** before speaking. Tag-looking lines inside ``` code fences are ignored (code is never spoken anyway).
* Message text and each embed (if `TTS_READ_EMBEDS=true`) are parsed independently, so a `[ROLL]` in the body doesn't silence an embed.
* Voice order is preserved: `[SYSTEM] a` / `[GM] b` / `[SYSTEM] c` plays a, b, c in that order, each in its own voice.

Example message:
```
[SYSTEM] The floor collapses in 6 hours. Crawlers, move.
[ROLL] Carl: d20+3 = 17 vs DC 14, success
[GM] New achievement! **Doormat**. You held the door. The audience held its laughter.
Reward: one (1) lukewarm box.
[GM] Carl kicks the door open. The goblin inside looks up, deeply offended.
```
speaks the clock line in the System voice, skips the roll, and speaks the achievement and narration as the narrator.

**Length limits** (after tags and markdown are stripped): messages are split at sentence boundaries into chunks of at most `TTS_CHUNK_MAX_CHARS` (default **600**; a single sentence longer than that is split at commas/spaces). The total spoken text per message is hard-capped at `TTS_MAX_MESSAGE_CHARS` (default **1500**); anything beyond is dropped, cutting at the last complete sentence that fits (a warning is logged). Chunks stay sentence-sized for low latency rather than being packed up to the maximum.

**Voices:** the System voice has its own settings: `OPENAI_TTS_SYSTEM_MODEL/VOICE/INSTRUCTIONS/SPEED` (defaults: narrator's model, `coral`, dry corporate instructions per decision 032) or, for ElevenLabs, `ELEVENLABS_SYSTEM_VOICE_ID/MODEL_ID/STABILITY/SIMILARITY` (if `ELEVENLABS_SYSTEM_VOICE_ID` is empty, System lines use the narrator voice and a warning is logged). `/say` takes an optional `voice` (`gm` default, or `system`) used for untagged text; tags inside the `/say` text still apply.

---

## Configuration reference

See `.env.example` — every variable is documented there. Highlights:

| Variable | Default | Meaning |
|---|---|---|
| `AUTO_JOIN` | `false` | Join `VOICE_CHANNEL_ID` on startup |
| `GM_ALLOWED_AUTHOR_IDS` | *(empty = anyone but the bot)* | Whose GM-output messages are spoken |
| `STT_MODEL` | `gpt-4o-transcribe` | or `gpt-4o-mini-transcribe` / `whisper-1` |
| `STT_LANGUAGE` | `en` | ISO-639-1 hint; strongly reduces hallucinations |
| `STT_PROMPT` | campaign names | Vocabulary hint (character/place names) |
| `STT_SILENCE_MS` | `1000` | Silence that ends an utterance |
| `STT_MIN_DURATION_MS` / `STT_MIN_RMS` | `700` / `250` | Skip clips shorter / quieter than this |
| `TTS_PROVIDER` | `openai` | `openai`, `elevenlabs` or `fish` |
| `FISH_API_KEY` / `FISH_VOICE_ID_NARRATOR` / `FISH_VOICE_ID_SYSTEM` | – | Fish Audio credentials and voice (reference) ids |
| `FISH_MODEL` / `FISH_LATENCY` / `FISH_FORMAT` | `s2.1-pro` / `balanced` / `mp3` | Fish model, latency mode, audio format |
| `FISH_SESSION_CAP_MINUTES` | `50` (`0` = off) | Hard cap on spoken minutes per voice session; see [Per-session voice cap](#per-session-voice-cap-fish_session_cap_minutes) |
| `WAKE_USAGE_LOG` / `WAKE_USAGE_LOG_ENABLED` | `logs/wake-usage.jsonl` / `true` | One JSONL line per GM wake, counted by `npm run usage` |
| `WAKE_MAX_PER_HOUR` / `WAKE_RATE_LIMIT_BACKOFF_MS` | `60` (`0` = off) / `300000` | Rolling-hour wake budget; backoff after a "rate limit" response (see [GM wake webhook](#gm-wake-webhook-optional)) |
| `SPOTLIGHT_FILTER_ENABLED` / `SPOTLIGHT_FILE` / `SPOTLIGHT_MAX_AGE_MINUTES` | `true` / `<campaign>/sessions/spotlight.json` / `20` | Spotlight wake filter (fails open); see [Wake-up filter](#wake-up-filter-spotlight) |
| `GM_WAKE_STATE_FILE` | `logs/gm-wake-state.json` | Persisted `/gm pause` state |
| `DUPLICATE_WINDOW_SECONDS` | `120` (`0` = off) | Drop identical/near-identical GM messages from the same author |
| `MAX_QUEUED_CHUNKS` / `MAX_QUEUED_SECONDS` | `12` / `90` (`0` = off) | Backlog safeguard: drop the oldest pending messages |
| `VOICE_CONTROL_ENABLED` / `VOICE_CONTROL_FILE` / `VOICE_CONTROL_POLL_MS` | `true` / `<campaign>/sessions/voice-control.json` / `500` | File kill switch (`discord_gm.py stop`) |
| `VOICE_EVENTS_LOG_ENABLED` / `VOICE_EVENTS_LOG` | `true` / `logs/voice-events.jsonl` | Counts of duplicates dropped, backlog trims, flushes |
| `GM_WEBHOOK_URL` / `GM_WEBHOOK_KEY` | unset (feature OFF) | GM wake webhook endpoint and secret; see [GM wake webhook](#gm-wake-webhook-optional) |
| `GM_WEBHOOK_AUTH_HEADER` / `GM_WEBHOOK_AUTH_SCHEME` / `GM_WEBHOOK_KEY_IN_QUERY` | `Authorization` / `Bearer` / off | How the key is sent |
| `GM_WAKE_DEBOUNCE_MS` / `GM_WAKE_MAX_WAIT_MS` / `GM_WAKE_MIN_INTERVAL_MS` / `GM_WAKE_IDLE_MAX_WAIT_MS` | `2500` / `8000` / `4000` / `15000` | Wake batching and rate limits |
| `TTS_USAGE_LOG` / `FISH_MONTHLY_CAP_MINUTES` | `logs/tts-usage.jsonl` / `200` | Usage log path; monthly minutes budget for `npm run usage` |
| `OPENAI_TTS_MODEL` / `_VOICE` / `_INSTRUCTIONS` | `gpt-4o-mini-tts` / `onyx` / grim announcer | Narrator voice; `instructions` only applies to gpt-4o-mini-tts |
| `OPENAI_TTS_SYSTEM_MODEL` / `_VOICE` / `_INSTRUCTIONS` / `_SPEED` | narrator's / `coral` / dry corporate (decision 032) / narrator's | `[SYSTEM]` voice |
| `ELEVENLABS_VOICE_ID` / `_MODEL_ID` | – / `eleven_flash_v2_5` | Narrator voice (needed for ElevenLabs) |
| `ELEVENLABS_SYSTEM_VOICE_ID` / `_MODEL_ID` / `_STABILITY` / `_SIMILARITY` | narrator's / narrator's / `0.35` / narrator's | `[SYSTEM]` voice |
| `TTS_CHUNK_MAX_CHARS` | `600` | Max characters per synthesized chunk (split at sentence boundaries) |
| `TTS_MAX_MESSAGE_CHARS` | `1500` | Hard cap on spoken characters per message; the rest is dropped |

Tuning tips: if quiet players get ignored, lower `STT_MIN_RMS` (try `120`); if keyboard/breath noise gets transcribed, raise it. Set `LOG_LEVEL=debug` to see every skipped clip and why.

## Behaviour notes
* **Echo / feedback:** the bot's own voice is never transcribed (Discord does not echo it back, and the bot's user ID is explicitly ignored). If the GM audio leaks through a player's speakers into their mic, that is picked up as that player — use headphones.
* **Bots are ignored** in STT; **only messages from other users/bots** (never itself) in the GM output channel are spoken. A message in the GM channel is ignored while the bot isn't in voice.
* **Transcript ordering:** transcriptions run in parallel (up to `STT_CONCURRENCY`) but are posted in the order the utterances ended.
* **`[ROLL]` lines are silent**, and messages containing only `[ROLL]` lines are ignored entirely.
* **`/skip`** skips the chunk being spoken and the rest of that GM message; `/skip all:true` empties the queue. `/leave` also clears it.
* **Restricting who can use commands:** Server Settings → Integrations → your bot → set command permissions.
* Transcription mentions are disabled (`allowedMentions: none`), so a player saying "at everyone" can't ping anyone.

## Running 24/7

The bot is a single long-running process with outbound-only connections (Discord gateway, Discord voice UDP, OpenAI/ElevenLabs HTTPS) – no inbound ports needed. A 1 vCPU / 1 GB VPS (Hetzner, DigitalOcean, Linode, Oracle free tier, etc.) is plenty for a table-sized group. Pick a region close to your Discord voice region for lower latency. Don't use serverless/Heroku-style platforms that sleep or block UDP.

### Option A – Docker (recommended)
```bash
cp .env.example .env && nano .env
docker compose build
docker compose run --rm bot node src/register-commands.js   # once
docker compose up -d
docker compose logs -f
```
The image is `node:22-bookworm-slim` + ffmpeg, runs as the non-root `node` user under `tini`, and `restart: unless-stopped` brings it back after crashes/reboots.

### Option B – pm2
```bash
# Node >= 22.12 + ffmpeg installed on the host
npm install -g pm2
npm ci --omit=dev
pm2 start ecosystem.config.cjs
pm2 save
pm2 startup        # run the command it prints, so pm2 starts on boot
pm2 logs discord-voice-bridge
```
Update with `git pull && npm ci --omit=dev && pm2 restart discord-voice-bridge`.

### Option C – systemd
```ini
# /etc/systemd/system/discord-voice-bridge.service
[Unit]
Description=Discord Voice Bridge
After=network-online.target

[Service]
WorkingDirectory=/opt/discord-voice-bridge
ExecStart=/usr/bin/node src/index.js
Restart=always
RestartSec=5
User=botuser

[Install]
WantedBy=multi-user.target
```

## Costs (rough)
STT is billed per audio minute of *speech clips only* (silence is never sent). TTS is billed per character spoken; use `GM_ALLOWED_AUTHOR_IDS`, `[ROLL]` tags and `TTS_MAX_MESSAGE_CHARS` to cap runaway output.

## Development
```bash
npm run check   # node --check on every file
npm test        # unit + pipeline tests (real Opus encode/decode, fake Discord, no network)
npm run doctor  # dependency/ffmpeg/DAVE report
npm run usage   # TTS usage totals + monthly cap + GM wake-up counts
npm run wake-test  # send one test GM wake webhook (prints only the HTTP status)
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `Invalid configuration:` on start | Fill in the listed variables in `.env`. |
| `Used disallowed intents` | Enable **Message Content Intent** in the Developer Portal → Bot. |
| Bot joins but no audio is heard / connection loops, close code **4017** | Discord is enforcing DAVE: you're on an old `@discordjs/voice` or `@snazzah/davey` is missing. `npm run doctor`, then `npm i @discordjs/voice@latest @snazzah/davey@latest`. |
| Joined but nothing is transcribed | The bot must not be server-deafened; check `LOG_LEVEL=debug` for "too quiet"/"too short"; check the transcript channel permissions. |
| TTS silent | ffmpeg missing (`npm run doctor`), bot lacks **Speak**, or the API key/voice is wrong (see error log). |
| `/join` says missing permissions | Grant View Channel, Connect, Speak on that voice channel. |
| Occasional "compressed data passed is corrupted" at debug level | Harmless packet loss/DAVE transition noise; the clip is still processed. |

## /create (character creation)
Players run it in the private `#create` channel (category Create; visible only to players, the GM bot and this bot; replies are ephemeral). The bridge does not enforce the channel.
Ephemeral, no TTS, no posts to #table-transcript/#gm-voice, no GM wake. Nothing is written until S17 Confirm. Drafts: `<dataDir>/create-drafts/<uid>.json` (mode 600, archived after 14 days). Per-session settings in `session.json` under `create`: `review_mode` (hold for non-alpha, off for alpha), `allow_roll`, `content_source`, `staff_channel_id`, `reviewer_ids`. Screen S12 (fan tags) is retired and skipped (numbering kept); fan tags come from the survey only and never appear on a card. Hold-mode reviewers use `/create review|approve|return`. Needs `npm run register` plus a bridge restart. Tests: `test/create.test.js` (includes the spec's 10-item script in sandboxes under /tmp); `node scripts/create-script-test.js` prints the report.

### Roll method (S8) and Cancel build
* **Roll** is one of three ability-score methods on S8 (Standard array, Point buy, Roll). On by default; `create.allow_roll` in `session.json` switches it (new sessions write true, `new-session.py --no-roll` writes false, a missing value means ON). The System rolls three arrays of six scores (`roll.py 4d6dl1`, 18 logged calls per round, label `S8 roll r<round> <A|B|C><1-6>`); the player keeps ONE array totalling 73 or more; if none qualifies all three are rolled again, up to 10 rounds, then a give-up line. Rolled rounds are saved in the draft (`scoreRolls`), so Back, Edit, a method change and Restart give no free reroll; the commit stores `build.score_method`, `build.score_base`, `build.score_rolls` and S17 re-checks every total from the dice. `max_roll_arrays` no longer exists. Tests: `test/roll.test.js`.
* **Cancel build** is a red button on every `/create` screen (S1 to S17, pickers, paged screens, comfort-only as "Close without saving", the Resume prompt and the held-for-review reply; on a full five-row screen it takes Restart's seat). It asks once, "Trash everything?" (Yes, trash it / No, keep going). Yes hard-deletes the whole draft file, rolled rounds included (a fresh `/create` rolls fresh), shows "Build cancelled. Run /create to start fresh." and logs `build_cancelled` (no content) to `create-log.jsonl`. It works on an old message, takes the per-player lock, is not blocked by an open session, and says "already cleared" if the draft is gone. Drafts already written to state (`state_written`, `sheet_written`, `channel_done`) are refused: a registered Crawler is never touched. Tests: `test/cancel.test.js`.

### Species and class display names
`/create` shows species, lineages (elf lineage, dragonborn colour, ...), classes and the Cleric/Druid order options as `Our Name (5e Name)`, taken verbatim from the `combined_label` of Lore's `tables/species-class-reskins.json` (+ `species-class-reskins.version.json`; entry ids in Lore's scheme: `elf`, `elf-high`, `wizard`, `cleric-protector`). Read by file mtime (no restart); a missing file or entry shows the plain 5e name; state.json, the ledger and the rules keep the 5e names. **Not live until Caleb approves:** Lore's v0.1.4 copy sits in `tables/` but is inert; the names show only when `create.species_class_reskin` is exactly `true` in the session's `session.json` (default OFF; flip with `python3 tools/species_class_reskins.py --enable` / `--disable`, no restart for the tables). Variants (Felid cat, cat-girl, ...) are display-only and arrive at the Floor 3 Offer, not in `/create` (it offers only the nine SRD species); the loader keeps `base_id` (lineages map by `base_id` + the exact chargen option in `chargen_value`) and rules/state always use `base_id`. Startup logs `species-class-reskins: ...` (hash check). Coverage: `python3 tools/species_class_reskins.py` in the campaign repo. Tests: `test/names.test.js`.

### Background names (S7) and the display-layer mechanism
`/create` S7 (Prior Employment) can show `Our Name (5e Name)` for the 16 backgrounds, the +2/+1 and +1/+1/+1 bonus choices, the Origin feats (incl. the Human extra feat) and, on S10, the background's starting-gear Package A/B, from Lore's `tables/background-reskins.json` (+ `background-reskins.version.json`; schema `background-reskins/0.1.0`, entries `kind` `background` | `choice` with `parent_id` `origin-feat` | `background-asi` | `background-kit`; ids `acolyte`, `feat-magic-initiate-cleric`, `asi-2-1`, `asi-1-1-1`, `package-a`/`package-b` shared by all backgrounds; `chargen_value` = the exact chargen string). The label is `combined_label` as written (Lore's `label_name` keeps it free of nested parentheses; the loader flattens any that remain), the entry's `flavor` shows under the chosen background and as the option description. **Approved by Caleb (v0.1.1); switched on in the alpha session.json.** It shows only when `create.background_reskin` is exactly `true` in the session's `session.json` (default OFF); roll back with `python3 tools/background_reskins.py --disable` (`--enable` to turn on). Display only: select values, drafts, state.json, the ledger, the sheet and the rules keep the 5e names. Any missing file/entry shows the current plain text.

Both name tables run on one mechanism, `src/create/layers.js`: a layer is `{id, file, flag, env, tkey}` registered with `registerLayer()`; every registered layer gets its own `create.<flag>` switch (exactly `true`, default OFF), is loaded by file mtime on each request (no restart; a broken file is ignored), has its sha256 checked at startup (`src/index.js` logs `<file>: ...`), and exposes `layerEntry(t, tkey, {id, kind, parent, value})` (by id, else kind+parent+chargen_value) and `layerText(t, tkey, screen, id, fallback, vars)` (string override by screen and id, `{var}` placeholders; a missing entry or unfilled placeholder gives the current text). Lore's later screen tables (abilities, skills, equipment, spells, messages...) are one `registerLayer()` call plus the lookups on their screens. Tests: `test/bgnames.test.js`, `test/names.test.js`.

### Several Crawlers per player: /crawlers, /delete, item names
* A player's 2nd+ `/create` makes a **benched** Crawler (no party slot, inert) filed under the same `player` name; the first is active. Duplicate names are still refused. Each Crawler gets its own sheet channel `<player>-<crawler>` (`setup-channels`).
* `/crawlers` (ephemeral): your Crawlers with active/benched and sheet-channel links, and a menu to **request** a swap (`state.py crawler request`; it never changes state; refused with a plain message while a session is open; if `staff_channel_id` is set, the GM gets a note and runs `state.py crawler activate`).
* `/delete <name>`: autocomplete lists only your own Crawlers; a warning, then a button, then you type the exact name (Cancel is the default); runs `state.py crawler delete ... --confirm NAME --as-user ID --by ID` (needs `GM_DISCORD_TOKEN` in the bridge env to remove the Crawler's channel; without it the Crawler is still deleted and the reply says the channel stays).
* `/join` writes `state.py session-status open` and `/leave` writes `close` (best effort). While open, swaps and deleting the active Crawler are refused. If the bridge dies in voice the marker stays open: `python3 tools/state.py session-status close`.
* Item names: `tables/item-reskins.json` (symlink to Lore's file; override `ITEM_RESKINS_PATH`) by `srd_id`; the old chargen `junk` field is never read. Header items (holy symbol, gaming set, instrument, artisan's tools, arcane/druidic focus generics) get a variant menu on S10, the sheet stores the variant `srd_id`, the price is the variant's own `base_price_cp` (Vending Wall x floor multiplier), and a header can never be committed. Startup logs a warning when the table's sha256 does not match `item-reskins.version.json`.
* New commands and the code need `npm run register` and a bridge restart. Tests: `test/crawlers.test.js`.

## /encounter (GM only; built, not yet registered)
`/encounter day:<1-5> [encounter:<id|all>] [block:<kind or slot>] [include_optional:true] [hours:<number>] [confirm:true] [floor:<1-18>]`

Shows the invoker an **ephemeral preview** of exactly what players may see from a Floor day page, then a **Post** button posts it publicly in the channel (**Cancel** posts nothing). Needs **Manage Server** (or being the server owner), the same helper `/session use` and `/voicecap` use; the command is also hidden from everyone else by default (`default_member_permissions`), the autocomplete answers nobody else, and the button re-checks the permission.
* **Source:** `floors/f01/day-NN.json`, loaded fresh on every call (no restart for rebuilt pages). Built from `audience_manifest.player_blocks[]` only: for each entry the bridge reads just the named `field` (set pieces: each paragraph's `text`) at the entry's JSON pointer. Everything else in the file is GM-only and is never read for output, including `day.gm_warning`, `loot_hooks`, `carry_on`, `quick_run`, `stall_fallback`, `[GM-FACING]`/`[GM-ONLY]` text and block metadata (`hours_note`, `gm_note`, `source`, `status`, `title` ...). `day.floor_exit.gm_warning` IS shown (the manifest says its text is read to the players), as slot `floor_exit_warning`.
* **Scope:** no `encounter` = the day-level notices (tomorrow, collapse, stairwell opening, early descent, floor exit); `encounter:enc-d02-01` = that encounter; a route id such as `route-dash` = that route's voice lines; `all` = everything. `block` takes a kind (`voice_line`, `route_voice_line`, `system_notice`, `zone_color`, `set_piece`, `exit_warning_read_aloud`, `achievement_narration`) or a slot (`system_intro`, `midpoint_twist`, `win`, `win_alt`, `collapse_notice`, ...). Autocomplete offers the names. The preview's header also lists which block kinds exist per group (names only).
* **Flags:** `collapse_notice` needs `hours:<number>` (fills `{hours}`); without it the command refuses with a clear message and shows nothing. Entries marked `optional` (zone colour, optional set-piece paragraphs) are skipped unless `include_optional:true`. Entries with `show_only_when` (achievement narration) are held back with a note until you pass `confirm:true`. Entries needing any other fill are skipped, and a leftover `{placeholder}` is never shown.
* **Output:** System-voice lines are posted as `**[SYSTEM]** text` (the bold tag in `src/tags.js`); narration is plain, tagged `**[GM]**` only when it shares a message with a System line. Messages are grouped up to 1,900 characters and long texts split at sentence ends; more than 12 messages at once is refused (narrow it). Mentions are disabled. Previews live in memory for 30 minutes (a restart expires them; run the command again).
* **Errors:** a missing day page, a page mid-rebuild (invalid JSON), a page with no manifest, or a floor other than 1 gives a short ephemeral explanation; it never crashes.
* **Rollout:** the code and the command definition are in `src/commands/encounter.js` / `src/encounter/extract.js` and in the command list, but nothing is live until `npm run register` (adds `/encounter`, guild commands) and a bridge restart. Tests: `test/encounter.test.js` (includes the leak test over `floors/f01/day-01..05.json`).

## /session
`/session status|list|use`: the bridge serves one active session at a time (use after `/leave`). See campaign decision 014 (draft).

### /create screens layer (`screens`, flag `create.screens_reskin`)
`src/create/screenstext.js` registers two layers on the display mechanism (`layers.js`): `screens` (`tables/create-screens-reskins.json`) and `screens_lines` (`tables/create-flow-lines.proposed.json`, merged over the flow lines by `mergeProposedLines`). Call sites use `tx(t, id, currentText, vars)` / `txd(t, id, dataString)`: the row's `new` is used only when the layer is on, the row's `old` still matches the call site (drift guard), all placeholders are supplied and rule numbers survive; otherwise the current text. Flag off (default) = byte-identical output. A new table version drops in by mtime, no restart. Rollback: `python3 tools/create_screens_reskins.py --disable` in the campaign. `src/create/rules.js` error strings and `screens.js` screen text are wired; `stat-*` rows only appear inside the preview line and the sheet.

### Money words (`src/create/money.js`)
`money(text)` rewrites GP / cp / gold / cash to "credits" (1 credit = 1 GP, 1 cp = 0.01 credit; whole credits without decimals, fractions with, singular for an amount of 1 or less) on the bridge's money sentences: S10 package labels (class and background, `<label> - N credits left over`), the S10 menus, intro, help and errors, price lists (`priceText`: integer cp in, credits text out) and the S10 flow line. Display only: `rules.js` math, totals, ledger values and `{gp}` are never read from the text (test/money.test.js pins the line costs and cart totals to the pre-change integers). Lore's rows `hint-money-gp` / `hint-money-cp` are used when present. Rows with `plain_on` (S1, S2, S13, comfort-only) show the old text on those views (`viewT` in screenstext.js).

## New-player roles (Oct 6 2026)

`src/roles.js`, run on every start (idempotent, additive only) and by `npm run roles:sync` (`-- --dry-run` to preview):

- Every human gets a personal role named after their Discord username, tracked by user id in `<campaign>/sessions/player-roles.json` (a taken name gets `-2`, `-3`, ...). Bots are skipped.
- The shared **Crawler** role: read + send in #agents, #gm-voice, #general, #table-transcript and #create; View/Connect/Speak/Voice Activity (+ text chat) in the GM voice channel (`VOICE_CHANNEL_ID`, "General"); role-level **Deafen Members**. Never Mute Members. Members holding **External Agent** keep that setup and do not get Crawler.
- Players **see only those channels plus their own sheet**: the Crawler role has View Channel denied on every other channel and category (categories that hold a players' channel are left alone). @everyone is never changed.
- Sheet channels (every session's `player-channels.json`: alpha `sessions/` and `sessions-data/<id>/`; owners from that session's `state.json` `build.discord_user_id`): Crawler denied, the owner's personal role allowed View + Read History + Send (a role allow beats a role deny). A sheet with no clear owner is just hidden.
- Channels created later: hidden from Crawler at once on ChannelCreate unless the name/id is on the players' list; a new sheet gets its owner's allow 5 s later (when the channel map is saved) and again from `/create`, which locks right after `setup-channels`, before the first card. A channel made while the bridge is down is fixed by the next start-up sync or `npm run roles:sync`.
- Join: `guildMemberAdd` when the **Server Members Intent** is enabled in the Developer Portal (detected at start; `DISCORD_MEMBERS_INTENT=true|false` forces it). Without it a new human gets their roles the first time they post, use a command or join voice.
- GM voice guard: if the bridge bot is server-muted it unmutes itself at once. A server-deafen is left alone and posts nothing (local log line only). While deafened the bridge hears nothing: no transcription, no GM wake from speech.
- `ROLES_SYNC_ON_START=false` skips the start-up sync. `PLAYER_ACCESS_CHANNELS` adds channel names/ids to the Crawler list. `PLAYER_ROLES_FILE` overrides the store path.
