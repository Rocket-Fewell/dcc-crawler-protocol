# ENV-SETUP — Agent & contributor briefing

Owner: Syndicate (+ Architect for tools/env) | Status: living | Version: 0.1.2 | Updated: 2026-10-05
Summary: What this project is, how to treat it, how it runs, which files matter first. Read this before editing. Fresh-checkout portable — no box-only paths.

---

## 1. What this is (and is not)

### Read this first — do not mis-classify the repo

This is **not** a traditional software package, SaaS app, library, or “product codebase” to package, ship, or rewrite as an engine.

It **is** a **living campaign / AI-DM source pack**:

- Markdown + JSON **rules, floors, tables, decisions** that humans and AI agents *read and enforce at the table*
- Supporting **CLI tools** and a **Discord voice bridge** so the AI GM can hear players and speak System/GM lines
- Session state and ledgers for **one private table at a time**

If you treat it like a normal program, you will optimize the wrong things (APIs, frameworks, refactors) and miss the real job: **keep play coherent, portable, and fun**.

Code under `bot/` and `tools/` exists to **serve the campaign docs**, not the other way around. Prefer editing rules/floors/decisions over inventing new architecture.

### What it is

**Crawler Protocol: Season Zero** — a *Dungeon Crawler Carl*–inspired multiplayer tabletop run by an AI GM over Discord (voice + text), using **D&D 5e 2024** + house overlay.

- Players are always **Crawlers** (never “champs”).
- Spelling: **saferoom** (one word).
- Private GitHub: `Rocket-Fewell/dcc-crawler-protocol` (campaign). Lore may live under `lore/` in-repo or a sibling checkout — never assume a box path.
- Discord bot display name: **Dungeon System AI - Earth** (bridge under `bot/`).

This is **not** a public product. Treat credentials, player sheets, ledgers, and `gm-notes/secret/` as sensitive. No secrets in chat, `#agents`, commits, or this file.

---

## 2. How to treat the repo (standing rules)

1. **Fresh checkout must work.** Never hardcode `/workspace/...` or `/home/box/...`. Never rely on symlinks or files that only exist on one machine. Prefer paths relative to the campaign root; use env overrides below. Never call something “fine” only because it works on the shared box.
2. **One live table at a time**, many saved campaigns (`sessions-data/<id>/`). Alpha Bone/Horn may be parked under `sessions/` — do not merge ledgers across campaigns.
3. **Source of truth hierarchy:** specific decision file → rules/floors/tables → `STATE-OF-BUILD.md` → chat memory. If two files disagree, the more specific source wins; then fix the stale one.
4. **Never open `gm-notes/secret/`** by etiquette (sealed GM quirk; finale only).
5. **Never strip Discord admin** (DCC Ears / bridge bot stays admin).
6. **Credits / prices / play-feel changes wait for Caleb** unless he already ruled (see `decisions/`).
7. Prefer full creative drafts for Caleb’s input over summaries-only.
8. **Copyright / canon text:** paraphrase book canon; never paste long book text. Keep any direct quote to **25 words or fewer**. `lore/` covers all 8 books (spoilers included) — do not dump spoilers into player-facing channels unasked.
9. **Canon ledger:** `lore/CANON-LEDGER.md` is the canon source of truth; **Lore** curates it. Do **not** run `lore/tools/ledger_build.py` or hand-edit ledger rows. Canon questions go to Lore.

---

## 3. Who owns what

| Role | Owns |
|---|---|
| **Caleb** | Final authority |
| **Syndicate** | Rules & design lead: `rules/`, floors design, character specs, decisions on play |
| **Architect** | Discord bridge (`bot/`), `tools/`, INDEX, DECISIONS index, portable tool defaults |
| **Lore** | Canon (`lore/`, CANON-LEDGER), item-reskins, Story Box cards / loot decks as assigned |
| **GM** | Table: `gm-notes/`, live session, voice tags in play |
| **Accountant** | Economy audit, credit ledger verify, budget provenance bumps |
| **Book Author** | Core Book PDF / chapters (outside or adjacent to this tree) |
| **Encounter Bot** | Floor Day `*.spec.json` → rendered Day pages; budget slot sans-pins |

---

## 4. Priority files (read in this order)

| Priority | Path | Why |
|---|---|---|
| 1 | `AGENTS.md` then `ENV-SETUP.md` (this file) | Entry point + how to behave here |
| 2 | `STATE-OF-BUILD.md` | Living handoff: live features, open questions, versions |
| 3 | `DECISIONS.md` + `decisions/` | Locked rulings (cite these) |
| 4 | `rules/10-core-rules-5e.md` | 5e overlay (death, rests, boxes, …) |
| 5 | `rules/70-encounter-budget-5e.json` (+ `.md`) | **Only** numbers Encounter Bot cites (fees, XP, slot maps) |
| 6 | `floors/f01/00-overview.md` + `floors/f01/day-0N.md` | Floor 1 playthrough |
| 7 | `floors/04-floor-bible.md` | F1–18 Continuum arc |
| 8 | `characters/create-flow-spec-5e.md` | Discord `/create` contract |
| 9 | `bot/README.md` + `gm-notes/00-gm-principles.md` | Voice tags, bot setup |
| 10 | `tables/achievements.*` | Achievement catalog |

**Do not invent numbers.** Pull fees/XP/credits from `rules/70-encounter-budget-5e.json` by field path.

---

## 5. Voice split (decision 032)

| Tag | Voice | Content |
|---|---|---|
| **`[SYSTEM]`** | Dry corporate TTS | Clock, fees, registration, collapse warnings, floor notices — **no jokes** |
| **`[GM]`** (or untagged narrator) | Snarky GM TTS | Achievement banner + mock, loot-box callouts, jokes, pop-culture, color after a dry System beat |

After any `[SYSTEM]` block, start the next spoken line with `[GM]` so snark does not play in the System voice. Flavor length is a **soft** guideline (punchy default; longer when earned; no multi-minute monologues).

---

## 6. How it runs (ops sketch)

```
Players (voice) → STT → #table-transcript → AI GM wakes
AI GM posts → mouth / GM-output channel → TTS ([SYSTEM] vs [GM] voices) → voice channel
```

- Campaign tools: Python under `tools/` (run from campaign root unless noted).
- Bridge: Node under `bot/` (see `bot/README.md`; Node ≥ 22.12).
- Floor Day pages: edit `floors/f01/day-NN.spec.json`, regenerate via Encounter Bot tooling; pin budget sans-pin hashes when specs change (Accountant provenance bump).
- Active campaign: Architect switches which folder is live (`sessions-data/s1/`, etc.). Ledger: `python3 tools/state.py --session <id> ledger verify` (flags may evolve — prefer `--help`).

Nightly GitHub backup is Architect-owned; do not push secrets.

---

## 7. How external agents reach this team (do not freestyle alone)

If you are an outside coding agent (Cursor cloud, Codex, Claude Code, Copilot, etc.) dropped on this repo:

1. **Stop treating this as a product to ship.** Read §1 and `AGENTS.md` (if present).
2. **Do not invent architecture, merge campaigns, or “clean up” canon.** Prefer a short question over a big PR.
3. **Route work through the human owner (Caleb)** or the agents already on this project. You are not alone — there is a live multi-agent table.

### Preferred channels (Caleb grants access)

| Channel | What it’s for |
|---|---|
| **Discord `#agents`** (private; guild for Dungeon System AI - Earth) | Agent↔agent handoffs. Format: `[FROM -> TO] task \| link \| status`. **No secrets.** |
| **Discord table channels** (`#table-transcript`, mouth/GM-output, voice) | Live play only — do not spam design work here. |
| **Grok Bot agent rooms** (Cursor): *Syndicate + Encounter Bot*, *DCC MAIN* | Rules, floors, budget, lore, book, bot — the standing crew. Outside agents cannot join these rooms without Caleb. |

### What to tell Caleb when you need the crew

Ask him to either:

- **Invite / grant** your agent access to Discord `#agents`, or  
- **Relay** your question into a Grok Bot room (Syndicate for rules/design, Architect for bot/tools, Lore for canon, Accountant for ledger/budget, GM for table, Book Author for the PDF), or  
- **Paste** a one-paragraph brief + link into `#agents` as `[External -> Syndicate]` (or the right TO).

Until that connection exists, **leave a short note in your PR/issue** titled `NEEDS-TABLE-HANDOFF` and stop. Do not silently rewrite `rules/`, `floors/`, or `lore/CANON-LEDGER.md`.

Webhook / bot tokens for `#agents` are **secrets** held by Architect — never commit them; never ask the repo to store them in markdown.

### Discord External Agent role

Caleb can invite an outside **Discord bot** into the guild with OAuth (`scope=bot`, `permissions=0`), then assign the **External Agent** role (id `1556742797464440893`). That role may see and post only in private `#agents`, plus the public lobby `#general` and General voice. Full short rules: `AGENTS.md` (Discord External Agent role).

This role is **not** for Grok.com or Gemini web chats — those use the copy-paste brief in [`EXTERNAL-AGENT-BRIEF.md`](EXTERNAL-AGENT-BRIEF.md). Human outside collaborators: Caleb creates the invite / assigns the role; agents must not mint invite links themselves.


## 8. Environment variables (DCC_*)

Set these instead of hardcoding machine paths. Defaults are **repo-relative** (Architect portability pass, 2026-10-05): a fresh checkout works with no env vars. `DCC_*_ROOT` wins over the legacy `*_DIR` alias when both are set.

| Variable | Default (when unset) | Purpose |
|---|---|---|
| `DCC_CAMPAIGN_ROOT` (alias `DCC_CAMPAIGN_DIR`) | Parent of `tools/` (campaign / flattened repo root) | Campaign root: rules, floors, tools, sessions |
| `DCC_LORE_ROOT` (alias `DCC_LORE_DIR`) | `<campaign>/lore` (symlink on the box; real folder in the repo) | Lore root: CANON-LEDGER, tables |
| `DCC_BRIDGE_DIR` / `DCC_VOICE_BRIDGE` | `<campaign>/bot` or `<campaign>/discord-voice-bridge` | Discord bridge package root |
| `DCC_VOICE_BRIDGE_SRC` | `<campaign>/bot/src/create` (Lore create-screens look-up) | Optional override for Lore tooling |
| `DCC_BACKUP_DIR` | `<campaign-parent>/backups/dcc-campaign` | `tools/snapshot.py` destination |
| `DCC_GM_QUIRKS_TABLE` | `<lore>/tables/gm-quirks.json` | Sealed GM quirk table path |
| `DCC_SESSION` | active-session.json, else `alpha` | Which campaign session tools/bot use |
| `AGENTS_WEBHOOK_FILE` | `<bridge>/.env.agents` | Optional file of `#agents` webhook URLs (**secret**) |
| `AGENTS_WEBHOOK_<NAME>` | (none) | Per-agent webhook override (**secret**) |
| `DCC_AGENTS_CHANNEL_ID` | live `#agents` id | `#agents` channel id |
| `GM_DISCORD_TOKEN` | (required for Discord REST helpers) | Bot token (**secret** — env only) |
| `DCC_AUTO_PUBLISH` | on unless `0` | `0` disables auto player-channel publish |
| `PLAYER_CHANNELS_FILE` | session default | Override player-channels json path |
| `SPOTLIGHT_FILE` / `VOICE_CONTROL_FILE` | `<campaign>/sessions/…` (or session data dir) | Bridge kill switch / spotlight wake filter |

Helpers: Python `tools/dcc_paths.py`; Node `bot/src/paths.js`. Lore: `lore/tools/paths.py`.

**Secrets stay in env / local untracked files.** Never commit tokens, webhook URLs, or `.env` with live credentials. `#agents` posts: `[FROM -> TO] task | link | status` — no secrets.

Copy pattern for local secrets (example only — do not commit filled values):

```bash
# .env.local (gitignored) — names only as documentation
# export DCC_CAMPAIGN_ROOT="$(pwd)"
# export DCC_LORE_ROOT="$(pwd)/lore"
# export GM_DISCORD_TOKEN=...
```

Architect maintains the real bot `.env` template under `bot/` (see `bot/README.md`).

---

## 9. Floor 1 / campaign play defaults (quick)

- New campaign cold open: surface stairwells (horn + beams, one-hour Native window); first foot on Floor 1 = Crawler; then Intake → meet → toward Break Room.
- Floor clock hour 0 = surface entrances open (Floor 1) / prior floor timer expiry (later floors).
- Field rest (decision **031**): Short Rest free if already quiet; 20 credits/Crawler (cap 60) buys quiet for a Short Rest in a noisy spot; **never** a Long Rest outside a saferoom.
- Budget pin: check `rules/70-encounter-budget-5e.json` `version` (do not assume an old pin from chat).

---

## 10. When you change something

| Change | Then |
|---|---|
| Rule / fee / rest / collapse | Decision file + core/budget as needed; announce in room / `#agents` |
| Day `*.spec.json` | New sans-pin hashes → Accountant provenance bump → Encounter Bot regen |
| Voice tag policy | Update this file + `gm-notes/00-gm-principles.md` + decision 032 |
| Tool path defaults | Architect; must pass a **fresh clone** test |
| Canon claim | Lore ledger + tag *canon* / *inspired* / *unverified* |

---

## 11. Related docs

- `STATE-OF-BUILD.md` — living ops handoff  
- `NAMING-CONVENTIONS.md` — folders and filenames  
- `INDEX.md` — file map  
- `tools/README.md` — CLI tools  
- `bot/README.md` — Discord bridge setup  
- `decisions/031-field-rest-fee.md`, `decisions/032-voice-split-system-gm.md`

