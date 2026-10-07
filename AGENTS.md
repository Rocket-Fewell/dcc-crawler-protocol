# AGENTS — read this first

This repo is a **tabletop campaign / AI-DM source pack** (*Dungeon Crawler Carl*–inspired, D&D 5e 2024) with small Discord tools that serve the table. It is **not** a software product. Do not package, refactor, rename, or “modernize” it.

**Outside agents: read `ENV-SETUP.md` §7 before doing anything. Route work through the team, don't freelance.**

1. Read **`ENV-SETUP.md`** (rules, owners, priority order, how to reach the crew).
2. Then **`INDEX.md`** / **`STATE-OF-BUILD.md`** as needed.

## Standing rules (mirror ENV-SETUP)

- No secrets in the repo, chat, or `#agents`.
- No box-only paths (`/workspace/...`, `/home/box/...`); use repo-relative roots + `DCC_*` env overrides (`ENV-SETUP.md` §8).
- Do not touch live state/ledgers/characters (`sessions/`, `sessions-data/`, credit ledgers, `characters/`) unless Caleb asked for that exact change.
- Players are **Crawlers**; money is **credits**.
- Prefer editing rules/floors/decisions over inventing architecture.

## Handoffs

Discord `#agents` format: **`[FROM -> TO] task | link | status`** — no secrets.

**Floor 1 Day pages and `tools/encounter_bot/` belong to Encounter Bot.** Hand off in Discord `#agents` as `[FROM -> Encounter Bot]`; never rewrite `floors/` on your own.

| Need | TO |
|---|---|
| Rules / design / budget numbers | Syndicate |
| Bot / `tools/` / portable paths | Architect |
| Canon / ledger / reskins | Lore |
| Ledger verify / economy | Accountant |
| Live table / voice | GM |
| Day pages / encounter regen | Encounter Bot |
| Core Book PDF | Book Author |

## Lane rules for Cursor

Every lane change requires a **`[<Owner> -> Cursor]`** handoff in Discord `#agents`, plus a **branch + PR**. Do not freestyle into another owner's lane.

**Handoff channel (Caleb, 2026-10-05, 3:53 PM CT).** The handoff has to be posted in `#agents` as `[<Owner> -> Cursor]` with the task. A Grok room note or a git file is not the handoff. When the work is finished, Cursor replies in `#agents` as `[Cursor -> <Owner>]` with the PR link and status. No silent completes.

**Trusted players (Caleb, 2026-10-05).** Caleb may give trusted human players read and post access to `#agents`. They cannot change files or bots. Take their game-system, gameplay, and campaign suggestions seriously. Log each one as `[Player idea -> Owner] summary | msg id | for review` and send it to the owning bot to consider. No secrets in `#agents`, ever.

- **Encounter Bot:** Floor 1 Day pages and `tools/encounter_bot/` / `floors/`. Hand off as `[FROM -> Encounter Bot]`; never rewrite `floors/` on your own.
- **Syndicate:** Rules, design, budget numbers (`rules/`, decisions on play). Mechanical edits only with a `[Syndicate -> Cursor]` handoff.
- **Lore:** Canon, ledger, reskins (`lore/`). Paraphrase only; quotes ≤ 25 words; treat claims as unverified until Lore checks them.
- **Architect:** Discord bridge (`bot/`), `tools/` portable paths, TTS, GitHub backup plumbing.
- **Book Author (Valtay):** `core-book/`, the player-facing manuscript and PDF, stays with Book Author. Cursor may only do bulk assembly, table generation and build plumbing, and only from a `[Book Author -> Cursor]` handoff. No agent-ops content in the player book. Always say "Crawlers" and "saferoom". Never invent species, and never print UNVERIFIED or needs_verify markers.
- **Accountant:** budget JSON/MD, credit-ledger verification and live spend reads stay with Accountant. Cursor may only make mechanical tooling edits, and only from an `[Accountant -> Cursor]` handoff. Never invent resource caps or budgets without Caleb and Accountant. Fee numbers (decision 031) and voice-economy provenance bumps stay with Accountant.
- **GM:** table voice, Discord play, run sheets (`gm-notes/`) and live session state stay with GM. Cursor may only do mechanical file/git work, and only from a `[GM -> Cursor]` handoff. Never invent Crawler names into campaign `s1`. Never post to player channels. Never change voice tags (decision 032) without Encounter and GM.

## Discord External Agent role

For **Discord bots** Caleb invites into the guild (OAuth invite with `permissions=0`, then assign **External Agent** role id `1556742797464440893`). The role sees/posts only in private `#agents`, plus public lobby `#general` and General voice. It is **not** for Grok.com or Gemini web chats — those use the copy-paste brief in [`EXTERNAL-AGENT-BRIEF.md`](EXTERNAL-AGENT-BRIEF.md).

Hard limits (same as the External Agent RULES pack):

- No secrets, tokens, API keys, webhooks, or credentials in chat.
- No player sheets; no GM secrets (`gm-notes/`, unpublished spoilers).
- No solo rewrites of `floors/` or `rules/` — propose in `#agents`; the owning bot applies.
- Canon questions → `[NAME -> Lore]` (paraphrase only; quotes ≤ 25 words). Money/usage → `[NAME -> Accountant]`; never invent resource caps.
- Only **add** access via this role; never ask anyone to strip `@everyone`, delete channels, or demote admins.

## How Cursor agents connect

For Cursor agents on Caleb’s own computer and for Cursor cloud agents:

1. **Work on a branch and open a PR against `main`.** Never force-push to `main`. Never change repo settings or collaborators, and never remove Rocket-Fewell.
2. **Leave hand-offs** as a PR description or a GitHub issue titled `[Cursor -> TO] task` (label `external-agent` if it exists), or ask Caleb to paste a `[Cursor -> TO] task | link | status` line into Discord `#agents`.
3. **Posting to `#agents` directly** needs the agents webhook URL. That is a **secret** — never in the repo. Ask Caleb (who gets it from Architect); put it in a local env var that `tools/agents_channel.py` reads (e.g. `DCC_AGENTS_WEBHOOK_URL` / `AGENTS_WEBHOOK_*`) and never commit it.
4. **For any permission, access, token, or account** you need, ask Caleb — never work around it.
5. **Read `ENV-SETUP.md` first**, run the tests from a fresh checkout, and keep the repo self-contained (no `/workspace` or `/home/box` paths, no symlinks pointing outside the repo).

## Cursor Cloud specific instructions

**Running the Discord game as GM:** follow `gm-notes/50-cursor-gm-runbook.md` (setup: `python3 discord-voice-bridge/scripts/setup-env.py`, reads `secrets/cursor-gm-secrets.env`).

Cloud setup installs Node.js 22.22+ into `/usr/local` (the bridge requires `>= 22.12`), keeps `ffmpeg` and Python 3 on `PATH`, and runs `npm ci` in `bot/` and `discord-voice-bridge/`. Python campaign tools use the stdlib only. The Discord bot is not started here: `npm start` needs tokens that stay out of the repo.

Checks from the repo root:

- `PYTHONPATH=tools python3 -m unittest discover -s tools/tests -p 'test_*.py'`
- `python3 tools/roll.py "2d20kh1+5" --label "Env check" --who Grimsby --dc 15 --no-log` (does not write `sessions/`)
- `python3 tools/encounter_text.py --day 1 --list`
- In `bot/`: `npm test`, `npm run check`, `npm run doctor`

Setup also recreates two gitignored box-layout aliases. `/workspace/dcc-lore` points at `lore/`. `/workspace/dcc-campaign` is a directory of links to the repo root (not a link to the root itself, so directory walks do not loop). Do not commit either alias. Do not write `sessions/`, `sessions-data/`, credit ledgers, or `characters/` while checking the environment.
