# Engine v1: Architecture and build plan
Owner: Architect | Status: decided for v1 | Version: 0.1.0 | Updated: 2026-10-07
Source: `00-source-grok-conversation.md` (Caleb's direction, 2026-10-07 9:44 PM CT). Rules scope: `01-rules-engine-scope.md` (Syndicate). Room data: `03-room-card-format.md`.

## 1. Decisions
- **Same repo, new `engine/` folder.** No new repo. Floors, rules, lore and decks stay where they are and become engine content. The existing Cursor environment and secrets keep working. Old tools (`tools/`) keep running until the engine replaces them.
- **Two processes, one start command.** The existing Node bridge (`discord-voice-bridge/`, proven Discord voice, speech-to-text, Fish voices, slash commands) stays the front end. It starts the Python engine as a child process and talks to it with JSON lines over stdin/stdout. No HTTP server, no extra port.
- **The engine owns the game.** It loads the campaign at session start, keeps all state in memory, resolves every number in code, checks room-card triggers, and calls the models. It saves to SQLite (`engine-data/<campaign>.sqlite`, git-ignored) after every resolved action, and exports a JSON snapshot at session end for the nightly backup. Git is never in the turn loop.
- **Models are called by code, never by agents.** OpenAI-compatible client so the provider is a setting: `ENGINE_MODEL_BASE_URL`, `ENGINE_MODEL_API_KEY` (defaults to the existing `OPENAI_API_KEY`), `ENGINE_FAST_MODEL`, `ENGINE_STRONG_MODEL`. Swapping to xAI or another provider is a config change. No new key is needed to start.
- **Fast model narrates, strong model rules.** Snapshot and ruling formats are in `01-rules-engine-scope.md` sections 4 and 5. Narration streams sentence by sentence to the bridge so voice starts before the reply is finished.
- **Agents build between sessions.** Bots write content and review PRs; Cursor writes code. No agent runs during a session.
- **Runs on the shared box first,** where the bridge already runs. Moving to a small always-on server later is a deploy change, not a rewrite.

## 2. Turn loop
1. Bridge hears a player line (voice transcript or text) and sends `{"type":"line","player":...,"crawler":...,"text":...}` to the engine.
2. Engine parser maps it to an action (scope section 2). Buttons and fixed commands skip the parser.
3. Code resolves the action: rolls, HP, conditions, uses, turn order. Triggers on the current room card are checked.
4. If no rule covers it, the strong model returns a ruling JSON, code validates and resolves it, and it is logged POST-SESSION REVIEW.
5. Engine builds the snapshot and streams fast-model narration back as `{"type":"say","voice":"GM|SYSTEM|NPC: Name","text":...}` chunks, plus `{"type":"whisper","crawler":...,"text":...}` for private reveals and `{"type":"card","crawler":...}` for sheet updates.
6. Bridge speaks the chunks, posts the transcript, updates cards. Target: voice starts within about 3 seconds.

## 3. Build order (Cursor jobs, posted by Architect in #agents)
1. **C1 engine core:** `engine/dcc_engine/` package: importable rules library built from `tools/state.py`, `roll.py`, `loot.py` logic (do not edit `tools/`; wrap or port with tests), room-card loader and JSON Schema validator for `03-room-card-format.md`, SQLite persistence, stdio JSON-lines server, model client with streaming and a fake-model mode for tests, and a replay harness. Done = the 2026-10-07 Shooting Gallery replay (scope section 7) passes with the fake model, all tests pass from a fresh checkout.
2. **C2 bridge integration:** bridge flag `ENGINE_MODE=1` spawns the engine and routes lines to it instead of waking the GM bot. Old path stays the default until C3 passes.
3. **C3 live dry run:** Caleb and the bots play the Shooting Gallery on a test channel with real models. Accountant records cost per turn.
4. **Content (parallel, bots):** Encounter and Lore write Floor 1 room cards; Accountant checks counts against the budget; Syndicate owns the action list and ruling rules; GM owns the narrator prompt and replay script.

## 4. Until the engine passes C3
Sessions keep running on the current bridge plus GM bot setup. Nothing about the current game changes until the dry run passes and Caleb says switch.
