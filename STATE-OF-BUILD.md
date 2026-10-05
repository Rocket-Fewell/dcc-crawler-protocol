# State of Build (handoff)
Owner: Syndicate and the Architect (Borent) | Status: living | Version: 0.1.10 | Updated: 2026-10-05 12:50 CT
Summary: One file so the project can be led without Caleb in the loop and without anyone's memory. Facts only, each with its source file. If this file and a source file disagree, the source file wins; fix this file.

Project: *Crawler Protocol: Season Zero* (Dungeon Crawler Carl, D&D 5e 2024). Players are always **Crawlers**, never "champs" or other nicknames (Caleb, 2026-10-04; gm-notes/00-gm-principles.md).

---

## 1. Who owns what

| Who | Owns |
|---|---|
| **Caleb** | Final authority on everything. |
| **Syndicate** (Syndicate Dungeon Crawl System 001) | Rules and design. **Leads the build.** Writes rules/, characters/ guide and spec, floors/, specs the Architect builds to. |
| **Architect** (Borent Corp Systems Architect) | The Discord bot (Dungeon System AI - Earth (formerly DCC Ears) bridge, `bot/`) and the tools (`tools/`). Builds to Syndicate's specs and **flags rules that cannot work**. Files DECISIONS.md and keeps the INDEX files. |
| **Lore** (DCC Lore) | Canon (`lore/`, CANON-LEDGER), the loot decks, the Story Box cards and the item-reskins table (`tables/item-reskins.json` is a symlink to Lore's file; never edit or copy it here). |
| **GM** (DCC AI GM) | Runs the table: gm-notes/, live sessions, the sealed quirk roll in use. **Has authority to adapt** as play goes (Caleb, 2026-10-04). |
| **Accountant** | Audits the economy and the credit ledger (`state.py ledger verify`, `sessions/credit-ledger.jsonl`). |
| **Core Book Author** | Writes the book (`/workspace/core-book`). |

Sources: NAMING-CONVENTIONS.md (folder owners), DECISIONS.md (001, 004, 008, 017, 018, 019), gm-notes/10-open-threads.md.

## 2. Needs Caleb

**Rule: anything that changes how the game plays, credits (amounts, prices, multipliers, rewards), or the sealed GM quirk roll waits for Caleb.** Nobody else approves it, and nobody opens, re-rolls or hints at the sealed roll (it was rolled and sealed 2026-10-04 13:38 CT, not revealed; the secret folder is never read or quoted; reveal is finale only).

Waiting on him right now:
- **Decision 014** (one active session per bridge, `/session status|list|use`): draft, "needs Caleb approval before it is cited as policy" (decisions/014).
- **Decision 020** (many Crawlers per player, one active, swaps, `/delete`): "final-pending-Caleb-override". Syndicate defaults stand unless he overrides; the session lock, text-channel layout and `/delete` are already his calls.
- **Story Box item strength** (rules/45 §9): the Floor 1-2 power ladder is only the GM default; the alternative is story-only items. Lore's cards `f01-any-0056` to `0059` sit over the ladder.
- **Roll method design defaults** (decision 024): rolled arrays saved in the draft (no free rerolls) and a 10-round auto-reroll stop are Syndicate defaults.
- **Create-audit confirmations** (tools-notes/create-audit-by-syndicate-20261004.md): N7 `loot story-box --reaward` lets a reclaimed deed pay again while rules/45 §6.3 says no second payout; N8 a new plain pet after the first dies vs "one pet per Crawler"; N5 `crawler delete` prints a delete count although `/delete` is "log only".
- **Pets, three Syndicate defaults** (rules/60 §13): crafted Heal Critter vs Good Boy Gulp; ordinary healing on a pet-Crawler; one pet per Crawler (canon had two rottweilers).
- **Section 5 list** (all other open questions).

## 3. Live now (as of 2026-10-04 evening)

**Discord bot "Dungeon System AI - Earth (formerly DCC Ears)"** (bridge `bot/`, symlink to /workspace/discord-voice-bridge; logs in as `Dungeon System AI - Earth#8647`, was `DCC Ears#8647`; renamed 2026-10-04 evening, the running bot shows the new name from its next login). Eleven slash command files in `bot/src/commands/`: `/join`, `/leave`, `/skip`, `/say`, `/voicecap`, `/shush`, `/gm`, `/session`, `/create`, `/crawlers`, `/delete`. Channels: `#gm-voice`, `#table-transcript` (old names dcc_mouth / dcc_ears), private `#create`, Crawler Sheets category (tools/README.md, Discord channel layout).

**Voice tags (decision 032, Caleb 2026-10-05):** `[SYSTEM]` = dry corporate (clock/fees/registration/collapse/floor notices; no jokes); `[GM]`/untagged = snarky narrator (achievement banner+description, loot-box callouts, jokes). Bridge `src/encounter/extract.js` and `tools/encounter_text.py` SYSTEM_KINDS allow-list; unknown manifest kinds = GM. Docs: bot/README.md, gm-notes/00-gm-principles.md, decisions/032-voice-split-system-gm.md.

| Live feature | Detail | Source (version) |
|---|---|---|
| `/create` | Silent Discord flow, 16 active screens (S12 retired). Ability scores: **Standard array, Point buy and Roll all LIVE** (Roll: section 4). Item names show "Our Name (5e Name)" by `srd_id`. | characters/create-flow-spec-5e.md v0.1.10, tables/chargen-5e.json v0.1.5, create-flow-lines.json v0.1.1 |
| Several Crawlers per player | One active, others benched (inert), swap only outside an open session, one swap per window, GM runs `crawler activate`; players use `/crawlers` to request and `/delete <name>` (typed-name confirm, own Crawlers, no refund, ledger rows archived, log only). One text channel per Crawler. | decisions 020 + 021; tools/README.md v1.2 |
| Pets | **Only through GM `state.py pet add\|show\|mark-dead\|remove\|convert\|shop\|heal`.** Nothing in `/create`. Off switch `limits.pets_enabled`. Species list = 48 SRD Beasts CR 1/4 or lower. | decisions 022 + 023; rules/60 v0.1.0; tables/pet-species.json v0.1.1 |
| Story Boxes | Floors 1-2, hand-picked, one named deed, per-floor cap with a logged override; opens only in a saferoom; items tradeable (not bound). Two-step award. Tooling live in alpha since 5:27 PM CT. | rules/45 v0.2.2; gm-notes/31 v1.4; decisions 015, 018 |
| Ledger status | Append-only `sessions/credit-ledger.jsonl`, written by `state.py` (`--reason`). `state.py ledger verify` on 2026-10-04 evening: **OK (Bone Wifebeater 127, Horn 75, 10 entries)**. Deleted Crawlers' rows move to `sessions/deleted-archive/`. | tools/README.md |
| Tools | roll.py, state.py, loot.py, ledgers.py, publisher.py, repair_log.py, busted.py, gm_quirks.py, discord_gm.py, snapshot.py and more. Tests: 358 Python, 186 bridge (Node), `npm run check` 74/74 files, all OK on 2026-10-04 evening (Syndicate's earlier audit ran 355 Python + 164 Node). | tools/README.md v1.2; tools-notes/create-audit-by-syndicate-20261004.md |

**Rules file versions (header values on 2026-10-04):** core rules/10 v0.2.17 | crafting rules/20 v0.3.7 | species rules/30 v0.1.4 | loot deck spec rules/40 v0.1.8 | house items rules/42 v0.2.3 | Story Boxes rules/45 v0.2.4 | repairs rules/50 v0.1.4 | pets rules/60 v0.1.0 | encounter budget rules/70 v0.1.11 (sha256 3c272ca334e1...) | CR-by-floor compendium rules/75 v0.1.0 (sha256 664601ae0d35...) 