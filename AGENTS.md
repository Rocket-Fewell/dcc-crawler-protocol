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
