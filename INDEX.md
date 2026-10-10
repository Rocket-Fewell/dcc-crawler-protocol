# Master Index
Owner: Borent Corp Systems Architect | Status: draft | Version: 0.2.3 | Updated: 2026-10-06
Summary: Every file in the campaign workspace, one line each.

| Path | Description | Owner | Status |
|---|---|---|---|
| NAMING-CONVENTIONS.md | Folder layout and file naming rules | Borent | final |
| STATE-OF-BUILD.md | Handoff: who owns what, what needs Caleb, what is live vs pending, open questions, standing rulings, backlog, how to update, live/ops runbook (v0.1.10) | Syndicate + Architect | living |
| ENV-SETUP.md | Agent/contributor briefing: what this is, how it runs, how to treat it, priority files, env vars (fresh-checkout portable) | Syndicate + Architect | living |
| Cursor-DCC-CardsReference/INDEX.md | R&D card pack: 72 picture-named Floor 1–3 monsters, 191 gear cards, loot boxes, and a local-play set (actions, conditions, blank state, Floor 1 room stubs). Not a live floor. | Cursor | draft |
| engine/README.md | Local table process. `/` walks Floor 1 and Floor 2 from the day-page voice lines, then a local Floor 3 script. `/player` is still the Shooting Gallery slice. Listen is on only during that Crawler's turn. Discord stays the voice. Opt-in `DCC_TABLE_URL` hook is off until set. | Cursor | draft |
| engine/FOR-GROKS.md | Handoff for the Grok bots: what the local table is, where it is saved, progress against the 2026-10-07 conversation, and what is still open. | Cursor | handoff |
| engine/NEXT.md | Plan: rebuild Discord Floor 1 (days 1–5) on the lean table from the cards that already exist. The hook stays on the Gallery. | Cursor | plan |
| lore/INDEX.md | Canon catalogs, sources and research tools | DCC Lore | living |
| lore/CANON-LEDGER.md | Verified/unverified canon findings with sources | DCC Lore | in progress |
| rules/_source-crawler-protocol/02-core-rules-5e.md | 5e (2024) overlay: loot boxes, death and revival | Syndicate | draft v0.2.2 |
| rules/_source-crawler-protocol/05-campaign-narrative.md | Story spine | Syndicate | draft |
| bot/README.md | Discord voice bridge: setup and tag contract | Borent | draft |
| agent-discord/README.md | Channel agent (own bot token): listen, wake a Cursor automation, post one reply. Not the GM voice bridge. | channel agent | draft |
| agent-discord/PROMPT.md | Prompt the Cursor automation runs on each Discord wake | channel agent | draft |
| agent-discord/discord_agent.py | `whoami`, `read`, `new`, `say`, `listen` for one text channel | channel agent | draft |
| decisions/002-death-mode.md | Death Mode decision: Costly Revives, very costly and rare | Borent | final |
| decisions/003-death-bypasses.md | Earned death bypasses vs revives | Borent | final |
| decisions/004-crafting-system.md | Crafting system added; ownership split | Borent | final |
| rules/10-core-rules-5e.md | 5e (2024) overlay: achievements, loot boxes, death/revival, Floor 1 quickstart, crafting pointer, pets pointer, Roll method pointer, System skills by use (§6.5.1) | Syndicate | draft v0.2.22 |
| characters/character-creation-5e.md | 5e character creation (intake) guide and crawler sheet template (§3.6: Roll method) | Syndicate | draft v0.2.5 |
| characters/create-flow-spec-5e.md | Create flow spec: screen-by-screen build spec for the silent Discord /create flow (16 active screens, S12 retired; data model, edge cases, glossary, beta test script; section 8: several Crawlers per player; section 9: GM-filed pets, no pet question in /create; S8 Roll method (v0.1.10), active Crawler, session lock, text channel per Crawler, /delete, NEEDS BUILD list; acceptance and audit checklists) | Syndicate | draft v0.1.13 |
| characters/hornn-wizard.md | Hornn crawler sheet (Wizard, Human, Merchant), intake sealed and registered in state | AI GM | draft v0.4 |
| characters/moses-barbarian.md | Trailer Park Moses (John) crawler sheet (Barbarian, Goliath, Artisan), intake sealed and registered in state | AI GM | draft v0.4 |
| floors/f01/00-overview.md | Floor 1 The Orientation Pit: full 5e module (zones, boss, announcements, goblin-workshop cache) | Syndicate | draft v0.2.5 |
| floors/00-campaign-narrative.md | Campaign spine: Continuum floor structure and story arc | Syndicate | draft v0.3 |
| floors/04-floor-bible.md | Continuum floor bible: F1–18 arc, Continuum ladder, unique floors, seeds (for Caleb's input) | Syndicate | draft v0.4 |
| tables/achievements.csv | Achievement catalog, 1,826 rows (data); card in tables/achievements.md | Syndicate | draft |
| tables/achievements.xlsx | Achievement catalog, same data with filters (data) | Syndicate | draft |
| tables/achievements.md | Header card for the achievement catalog | Syndicate | draft v1.5 |
| tables/chargen-5e.json | /create data (2024 PHB written from memory; see meta.verify_todo; v0.1.5 rewords Find Familiar (no pet hint); v0.1.6 notes cite the current version; ability_methods.roll added in v0.1.4) | Syndicate | draft v0.1.6 |
| tables/create-flow-lines.json | System lines and survey pool for the /create flow | Borent | draft |
| tables/item-reskins.json | SRD item -> flavored name table (189 entries). A SYMLINK to ../../dcc-lore/tables/item-reskins.json (single source, owner Lore); hash in item-reskins.version.json | Lore | draft |
| tables/pet-species.json | SRD Beast list (CR 1/4 or lower) for GM-run pets | Borent | draft |
| tables/prebuilt-crawlers.json | 12 legal pre-built crawlers for /create | Borent | draft |
| DECISIONS.md | One-line summary of every table decision (001-035, 037; 036 pending) | Borent | living |
| gm-notes/INDEX.md | Index of the GM notes (secret folder intentionally not listed) | AI GM | draft |
| gm-notes/00-gm-principles.md | How the AI GM runs the table (ruleset, voice tags, rewards, loot, comfort, address rule) | AI GM | draft v0.1 |
| gm-notes/10-open-threads.md | Pending decisions, handoffs and live-session log | AI GM | draft v0.1 |
| gm-notes/20-gm-persona.md | The [GM] narrator persona and voice prompt | Borent | draft v0.1 |
| gm-notes/30-player-channel-card-format.md | Player-channel crawler card format | AI GM | draft v0.1 |
| gm-notes/31-story-box-how-to.md | One-page GM how-to for awarding a Legendary Story Box | Borent | final |
| exports/sheet-horn.md | Player-facing sheet export, Horn | AI GM | v1 |
| exports/sheet-bone-wifebeater.md | Player-facing sheet export, Bone Wifebeater | AI GM | v1 |
| exports/card-data.json | Item text used by publisher.py for crawler cards | AI GM | current |
| decisions/005-death-mode-tuning.md | Costly Revives numbers (follow-up to 002) and Special Brew mapping | Syndicate | final |
| rules/_archive/core-rules-v0.1-superseded.md | Retired v0.1 core rules | Syndicate | retired |
| characters/_archive/character-creation-v0.1-superseded.md | Retired v0.1 character creation | Syndicate | retired |
| floors/f01/_archive/floor-01-v0.1-stub-superseded.md | Retired v0.1 Floor 1 stub | Syndicate | retired |
| rules/20-crafting-5e.md | Crafting rules: tables/levels, ingredients, recipes, potion limits, explosives, failure, quick reference | Syndicate | review v0.3.7 |
| rules/30-species-supplement-5e.md | Species supplement: Floor 3 Offer procedure, rebuild rules, 12 DCC-style oddities, balance table, open questions, source map | Syndicate | draft v0.1.4 |
| rules/40-loot-deck-spec-5e.md | Loot deck spec: JSON card + deck format, GM draw rules, Floor 1-2 item reference, sample cards | Syndicate | draft v0.1.8 |
| rules/42-house-items-f01.md | House items F1: final rules text, card JSON, Lore diff list (Cloak of Many Fashions, Pole of Collapsing, Mystery Key, Potion of Fire Breath) plus Enhanced Pet Biscuit | Syndicate | draft v0.2.3 |
| rules/45-story-boxes-5e.md | Story Boxes: deed checklist and anti-farming, GM procedure, Floor 1-2 power ladder with 5 sample cards (fixed sale_value per rung), spotlight guideline, looting/trading/death/resale rules, core amendment, 1 open question, Changes for the room (Lore/Architect/Accountant) | Syndicate | draft v0.2.4 |
| rules/50-gm-malfunction-repairs-5e.md | GM malfunction repairs: proposed rulings for the eight open items in the Lore player guide (costs, DCs, quests, failure, Tribute judging, Busted callout, stacking, Repair Offset); quirk-agnostic | Syndicate | draft v0.1.4 |
| rules/loot-deck-srd-check-f01.md | SRD 5.2 check of Floor 1 loot deck cards (findings only) | Syndicate | draft |
| decisions/008-crafting-rules.md | Crafting rules decision (follow-up to 004): framework + Syndicate numbers | Syndicate | final |
| decisions/009-species-approach.md | Species approach: SRD nine plus Floor 3 offer | Borent | final |
| decisions/010-first-crafting-table.md | First crafting table location and use rules | Borent | final |
| decisions/011-crafting-settings.md | Approved crafting settings | Borent | final |
| decisions/012-crafting-economy-explosives.md | Crafting economy numbers and Boomer cap | Borent | final |
| decisions/013-party-size.md | Party size: four players | Borent | final |
| decisions/014-one-active-session-bridge.md | One active session per Discord bridge; /session status|list|use | Borent | draft |
| decisions/015-story-boxes.md | Legendary Story Boxes on Floors 1-2 (approved exception; hand-pick, tradeable, logged) | Borent | final v1.1 |
| decisions/016-s12-dropped.md | S12 dropped: no public Fan Profile tags screen; Fan Profile is hidden | Syndicate | final |
| decisions/017-busted-spontaneous-callout.md | Busted is a spontaneous callout (no prompts, no fees; valid only in a scene with a logged tell) | Syndicate | final |
| decisions/018-story-box-answers.md | Story Boxes approved with Caleb's answers (saferoom only, tradeable and sellable, rival rule, pet-Crawler, rota guideline, buyback by rung) | Syndicate | final |
| decisions/019-credit-multiplier-fees.md | Floor credit multiplier: not on box credit pulls; on rewards and System fees (repairs, buyback, crafting prices) | Syndicate | final |
| rules/60-pets-companions-5e.md | Pets and companions: GM-filed Beast CR 1/4 or lower, never offered, no pet field in /create, Biscuit link, two off-menu pet items, Assigned Companion compared | Syndicate | draft v0.1.0 |
| rules/75-cr-by-floor-5e.md | CR-by-floor encounter-difficulty compendium (F1–18): level bands, CR/XP from rules/70, Continuum tone F3/6/9/12; DRAFT | Syndicate | draft v0.1.0 |
|