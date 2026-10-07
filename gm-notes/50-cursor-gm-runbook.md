# Cursor GM runbook (cloud agent runs the DCC Discord game)

Goal: a Cursor cloud agent, working from a fresh checkout of `Rocket-Fewell/dcc-crawler-protocol`, runs the table
as GM in place of the Grok-based "DCC AI GM" bot. All paths below are repo-relative; run from the repo root.
Secrets come from the repo file `secrets/cursor-gm-secrets.env` (private repo, plain-text tokens, Caleb's order
2026-10-07). Cursor environment variables are **optional** and override any name in that file. Never print the values,
paste them into Discord, or copy them into any other tracked file. If the repo ever goes public, remove that file and
rotate every token first.

## 0. Read first (in this order)
1. `gm-notes/00-gm-principles.md`. Caleb said the s1 flavor length was **perfect**. Do not change it.
2. `decisions/032-voice-split-system-gm.md`: System vs GM voice. `[SYSTEM]` is the dry corporate voice for clock,
   fees, registration, floor/collapse notices, **rules notes and attack corrections**. `[GM]` (or untagged) is the
   snarky narrator. Re-tag `[GM]` after a `[SYSTEM]` line before any snark. `[ROLL]` lines are posted but never spoken.
3. `decisions/034-session-turn-order.md`: roll the Crawler order once at session start and keep it. Combat
   initiative overrides it for that fight only. Hand the spotlight on with `discord_gm.py spotlight set`.
4. `decisions/038-s1-item-mechanics.md`: Intake Bag, Traveler's Clothes and keepsakes. Track uses with `state.py uses`.
5. Floor pages: `floors/INDEX.md`, `floors/04-floor-bible.md`, `floors/f01/`, the current floor's run sheet
   (`gm-notes/40-floor1-run-sheet.md`), `gm-notes/20-gm-persona.md` and `30-player-channel-card-format.md`.
6. **Resume point:** the latest entry in `gm-notes/10-open-threads.md` (e.g. "s1 PAUSED ... RESUME HERE"),
   then `python3 tools/state.py session-status` and `python3 tools/state.py party`.

## 1. Setup
```bash
python3 discord-voice-bridge/scripts/setup-env.py          # secrets/cursor-gm-secrets.env + env overrides -> discord-voice-bridge/.env (+ .env.agents)
set -a; . secrets/cursor-gm-secrets.env; set +a           # the python tools (discord_gm.py, agents_channel.py) read GM_DISCORD_TOKEN etc. from the shell env
cd discord-voice-bridge && npm ci && npm run doctor && cd ..
PYTHONPATH=tools python3 -m unittest discover -s tools/tests -p 'test_*.py'
```
The script reads the secrets file (path override: `DCC_GM_SECRETS_FILE`), lets any set env var win, writes only
names that have a value, prints names (never values), warns about missing required ones, and sets
`DCC_CAMPAIGN_ROOT` to the checkout root. Use `--force` to rebuild an existing `.env`. `.env` and `.env.agents` are gitignored and excluded from the backup.

**Only one bridge per Discord token can run at a time.** Before `npm start` the box bridge must be stopped.
**Architect does that.** Ask Caleb to have Architect stop it and confirm. Do not start yours until then.
```bash
cd discord-voice-bridge && npm start      # joins VOICE_CHANNEL_ID if AUTO_JOIN=true, else a player runs /join
```

## 2. How a turn works (from the bridge code)
- **Player voice -> text.** The bridge (`DISCORD_TOKEN` bot) transcribes voice with OpenAI STT (`src/stt.js`) and
  posts each utterance to the transcript channel `TRANSCRIPT_CHANNEL_ID` (#table-transcript, formerly #dcc_ears).
- **Wake.** If `GM_WEBHOOK_URL` is set, `src/wake.js` batches new transcript lines (`GM_WAKE_DEBOUNCE_MS`,
  `GM_WAKE_MAX_WAIT_MS`, `GM_WAKE_MIN_INTERVAL_MS`, `GM_WAKE_IDLE_MAX_WAIT_MS`, `WAKE_MAX_PER_HOUR`) and POSTs a
  small JSON payload with `GM_WEBHOOK_KEY` as the auth header. The payload hint says: *run `discord_gm.py new`, then
  reply with `discord_gm.py say`*. The payload never carries the transcript itself. A spotlight
  (`sessions/spotlight.json`) limits which player's speech wakes the GM (fails open). `/gm pause|resume` gates wakes.
  **A Cursor cloud agent has no inbound wake URL.** Leave `GM_WEBHOOK_URL` unset and **poll** instead (loop below).
- **Read.** `python3 tools/discord_gm.py new` prints only transcript lines not seen yet (cursor in
  `sessions/.discord-cursor`). Use `read --limit 30` for context. Typed player text in the same channel shows up too.
- **Reply.** `python3 tools/discord_gm.py say "[GM] ..."` (or `say --file reply.txt`) posts as the GM bot
  (`GM_DISCORD_TOKEN`) to the GM output channel (`DCC_MOUTH_CHANNEL_ID` in the tool, default the live
  `GM_OUTPUT_CHANNEL_ID`). The bridge speaks every new message there whose author is in `GM_ALLOWED_AUTHOR_IDS`, in the
  narrator or System voice by tag. Fish (`TTS_PROVIDER=fish`) is capped per join by `FISH_SESSION_CAP_MINUTES`.
  Posts over 2000 chars are split. Emergency stop: `discord_gm.py stop`.
- **Rolls.** `python3 tools/roll.py "1d20+5" --label "Attack" --who <Crawler> --dc 13`. Paste its `[ROLL]` line.
- **State.** `python3 tools/state.py <cmd>`: `hp`, `credits`, `inventory`, `condition`, `achievement`, `box`,
  `loot`, `scene`, `crawler`, `party`, `show`, `session-status`,
  `uses spend|restore|set CRAWLER ITEM [n]`, `uses reset [CRAWLER] --per session|...` (decision 038 items),
  `validate`, `snapshot`. Never hand-edit `sessions/state.json`.
- **Cards.** After state changes: `python3 tools/discord_gm.py publish` (changed Crawlers only; `--crawler X`, `--full`, `--dry-run`).

### GM loop
```
start: roll turn order (034), print it, `spotlight set <first player>`
loop:  discord_gm.py new  -> nothing new? wait ~5-10 s and poll again
       resolve the active Crawler's action: roll.py, state.py, then the reply via discord_gm.py say ([SYSTEM]/[GM] tags)
       publish if sheets changed; spotlight set <next Crawler>
```
**Unclear rulings:** make a fair call at the table, then log it in `gm-notes/10-open-threads.md` (date, CT time,
question, what you ruled) for **Syndicate's batch review**. Do not ask other bots live. Never post to `#agents` or player channels outside play.

## 3. End of session
```bash
python3 tools/discord_gm.py spotlight clear
python3 tools/state.py validate && python3 tools/state.py snapshot    # sessions/state-snapshot-<date>.json
python3 tools/discord_gm.py publish --full
python3 tools/snapshot.py --label end-of-session   # optional tarball; needs DCC_BACKUP_DIR (lands outside the repo by default)
```
Add a "PAUSED, RESUME HERE" entry to `gm-notes/10-open-threads.md`: position, initiative, HP, and anything still pending.
Ask Caleb (via Architect) to restart the box bridge once yours is stopped (Ctrl-C).

**Commit and push to a session branch. Never to `main` and never to `backup/nightly`** (that branch belongs to the 3:45 AM
nightly backup, decision 035):
```bash
git checkout -b session/s1-$(date +%Y%m%d)
git add sessions/ characters/ gm-notes/10-open-threads.md   # plus any other GM-lane files you changed
git commit -m "s1 session <date>: state + open threads" && git push -u origin HEAD
```
Open a PR into `main`. Once it is merged, the box's `backup-sync.py --pull` brings the changes into the live files,
so Architect gets them back. If the box changed the same files in the meantime, pull-first stops with a CONFLICT and
Architect resolves it. The pre-commit hook (`tools/install_hooks.sh`, `check_repo_safe.py`) blocks secrets. Run it.
