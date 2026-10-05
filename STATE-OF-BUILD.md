# State of Build (handoff)
Owner: Syndicate and the Architect (Borent) | Status: living | Version: 0.1.8 | Updated: 2026-10-04 23:15 CT
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

| Live feature | Detail | Source (version) |
|---|---|---|
| `/create` | Silent Discord flow, 16 active screens (S12 retired). Ability scores: **Standard array, Point buy and Roll all LIVE** (Roll: section 4). Item names show "Our Name (5e Name)" by `srd_id`. | characters/create-flow-spec-5e.md v0.1.10, tables/chargen-5e.json v0.1.5, create-flow-lines.json v0.1.1 |
| Several Crawlers per player | One active, others benched (inert), swap only outside an open session, one swap per window, GM runs `crawler activate`; players use `/crawlers` to request and `/delete <name>` (typed-name confirm, own Crawlers, no refund, ledger rows archived, log only). One text channel per Crawler. | decisions 020 + 021; tools/README.md v1.2 |
| Pets | **Only through GM `state.py pet add\|show\|mark-dead\|remove\|convert\|shop\|heal`.** Nothing in `/create`. Off switch `limits.pets_enabled`. Species list = 48 SRD Beasts CR 1/4 or lower. | decisions 022 + 023; rules/60 v0.1.0; tables/pet-species.json v0.1.1 |
| Story Boxes | Floors 1-2, hand-picked, one named deed, per-floor cap with a logged override; opens only in a saferoom; items tradeable (not bound). Two-step award. Tooling live in alpha since 5:27 PM CT. | rules/45 v0.2.2; gm-notes/31 v1.4; decisions 015, 018 |
| Ledger status | Append-only `sessions/credit-ledger.jsonl`, written by `state.py` (`--reason`). `state.py ledger verify` on 2026-10-04 evening: **OK (Bone Wifebeater 127, Horn 75, 10 entries)**. Deleted Crawlers' rows move to `sessions/deleted-archive/`. | tools/README.md |
| Tools | roll.py, state.py, loot.py, ledgers.py, publisher.py, repair_log.py, busted.py, gm_quirks.py, discord_gm.py, snapshot.py and more. Tests: 358 Python, 186 bridge (Node), `npm run check` 74/74 files, all OK on 2026-10-04 evening (Syndicate's earlier audit ran 355 Python + 164 Node). | tools/README.md v1.2; tools-notes/create-audit-by-syndicate-20261004.md |

**Rules file versions (header values on 2026-10-04):** core rules/10 v0.2.17 | crafting rules/20 v0.3.7 | species rules/30 v0.1.4 | loot deck spec rules/40 v0.1.8 | house items rules/42 v0.2.3 | Story Boxes rules/45 v0.2.4 | repairs rules/50 v0.1.4 | pets rules/60 v0.1.0 | encounter budget rules/70 v0.1.11 (sha256 3c272ca334e1...) | character creation guide v0.2.5 | chargen table tables/chargen-5e.json v0.1.6 | create-flow spec v0.1.10 | Floor 1 module v0.2.5 | campaign narrative v0.3 | GM principles v0.3 | open threads v0.1.1 | Hornn and Moses sheets v0.4. Item-reskins version file v0.1.5 (sha256 75d379247b6b...). *The master INDEX.md still shows older numbers for some of these (rules/20 v0.3.1, rules/40 v0.1.5, rules/42 v0.2.2, rules/45 v0.2.1, Floor 1 v0.2.3); trust the file headers.*

**The table:** campaign session `alpha`. Two Crawlers: **Horn** (Hornn, Human Wizard 1, 75 cr) and **Bone Wifebeater** (Trailer Park Moses / John, Goliath Barbarian 1, 127 cr). Party is four slots, two filled. Session 1 ended in the Floor 1 Zone 6 Break Room saferoom; **both Floor 1 Tutorial Reprieves are spent**, so the next Floor 1 death is a real death (sessions/session-01-recap-2026-10-04.md). Death Mode: Costly Revives, party revives 0/3.

**Known gaps in what is live** (create audit, 2026-10-04; the Wizard "Find Familiar" pet hint, blocker B1, is fixed: chargen v0.1.5 reads "call up a spirit scout that spies, carries touch spells and helps", no pet word; the spell's own SRD name stays): the "Cats or dogs?" bonus question is still listed in characters/character-creation-5e.md (:248); the Lore reskin "Jerky Cubes for Good Boys (Dog-Approved)" shows on S10 (rename is Lore's call). Not verifiable without live Discord: channel creation and deletion, overflow category, first-card post, slash-command registration.

## 4. Recently shipped / pending

- **Rules lead rulings (2026-10-04, ~11:05 PM CT):** Platinum floors: core §4.5 wins (no Platinum F1-8), aligned in core v0.2.17 §4.1 and Appendix A and rules/20 v0.3.7; Story Box cap override is the GM's with a logged reason, Caleb can veto (core v0.2.17, rules/45 v0.2.4, rules/40 v0.1.8, decision 018 addendum); ACH-1824 wording "Legendary cap of 2 (core §4.5)" (catalog v1.3.1, still 1,826 rows).

- **Overnight tidy (2026-10-04, Syndicate):** loot-deck spec rules/40 v0.1.7 brought current (box ceilings: no Platinum F1-8, Legendary F13+ with campaign total 2; whole credits; achievement rewards incl. ACH-1824/1825/1826; collapse-death loot per decision 028); rules/45 v0.2.3 and create-flow v0.1.13 pointers only; rules/50 v0.1.4 tell-shown rule and two-Crawler line; DECISIONS.md one-liners for 025-028 and 030, 017 tell-shown rule. Platinum conflict resolved by the rules lead (see the line above).

- **Whole credits only (rules lead ruling, 2026-10-04; core rules/10 v0.2.16 §5.10, character-creation v0.2.5):** balances are integers; sp/cp are list prices; buy rounds up per cart line, sell-at-half rounds down per line. No price changed.
- **Collapse clock + Session 1 pacing (2026-10-04; core rules/10 v0.2.14, floors/f01/00-overview.md v0.2.5):** collapse is stated as a fixed 24 in-game hours into Day 5 with a running floor-hour count; overview §11.3 now says Session 1 played Z0-Z2 and part of Z3, Z4-Z5 skipped by the ejection to Z6.
- **Missed-collapse loot (decision 028, Caleb 2026-10-04; core rules/10 v0.2.13):** a Crawler who dies in a collapse loses credits and items with the floor, survivors loot only while it stands; ledger needs a new "floor lost" write-off entry type plus transfer-first logging (Architect, not yet built).

**Roll method for ability scores in `/create` (decision 024, spec v0.1.10 section 3.6): LIVE and independently audited (Syndicate), live as of 8:26 PM CT, 2026-10-04.** S8 offers Roll: 3 arrays of six scores (4d6 drop lowest, each die logged by roll.py), keep ONE array totalling 73+ (no upper limit), reroll all three if none qualifies, up to 10 rounds then a give-up line. Switch `create.allow_roll`, default ON (a missing value also means ON, so alpha has it too). Background +2/+1 or +1/+1/+1 added after; no score above 20. Rolled arrays are saved in the draft, so Back, Edit and Restart give no free reroll.
- **Audit:** passed after three Architect fixes (14-day draft expiry keeps rolled dice; repeat presses cannot roll twice; non-alpha sessions log to their own folder), plus later fixes (per-player lock, `DCC_SESSION` passed to roll.py). See tools-notes/create-audit-by-syndicate-20261004.md.
- **Restart:** the bot restarted at 8:26 PM CT with Roll and Cancel build live. Tests: Python 358, bridge 186, checks 74/74. Ledger Bone 127, Horn 75. Remaining unverified until Caleb's first real `/create`: channel create/delete, overflow category, first-card post.

**Cancel build: LIVE on every `/create` screen** (same restart; decision 023). Red button on S1 to S17, pickers, paged screens, comfort-only ("Close without saving"), the Resume prompt and the held-for-review reply (on a full five-row screen such as S9 it takes Restart's seat). Asks once "Trash everything?" (Yes, trash it / No, keep going); Yes hard-deletes the draft including rolled rounds, shows "Build cancelled. Run /create to start fresh." and logs `build_cancelled` (no content). Works from any old message, uses the per-player lock, is not blocked by an open session, says "already cleared" if the draft is gone, and refuses drafts already written to state (`state_written`, `sheet_written`, `channel_done`): a registered Crawler is never touched. Messages posted before the restart have no such button; the Resume prompt does. The slash-command description fix (lowercase "crawler") shows after `npm run register`.

**Other pending items**
- Create-audit blockers (tools-notes/create-audit-by-syndicate-20261004.md): B1 pet hint (Find Familiar line reworded in chargen v0.1.5, done; Syndicate to re-tick; Lore still decides the Good Boys jerky rename); B2 beta setup (`state.py --session beta set campaign.f1_reprieve true`, otherwise S1 shows Reprieve off; alpha's session marker is OPEN while the bridge is in voice, so a `/create` in alpha makes a benched Crawler: test in beta); B3 re-conversion after a pet-Crawler is deleted (decision 023 says fixed; Syndicate to re-tick).
- 10 of 37 create checklist items stay unticked (FAIL, PARTIAL, UNVERIFIED), listed in that audit.
- Bone Wifebeater's Discord id **is on file** in `build.discord_user_id` (as is Horn's), so ownership is by id for both Crawlers. (Ids are not written in this file.)
- Floor 1 Reprieve is a GM-narrated rule: no tool enforces it, no test covers it (audit N14).
- Syndicate's GM-principles audit (gm-notes/audit-by-syndicate-20261004.md) lists fixes for 00-gm-principles.md; Caleb's answers are recorded at its end.

## 4b. Live / ops runbook (the Architect's side; no secrets here)

**Launch and restart** (bridge in `/workspace/discord-voice-bridge`, Node 22 on PATH, e.g. `export PATH=$HOME/node22/bin:$PATH`; alpha is the default session):
1. Back up first: copy `sessions/state.json` and `sessions/credit-ledger.jsonl` into `sessions/backups/` with a timestamp.
2. Stop the old bot: find the pid of `node src/index.js` (`ps aux | grep "node src/index.js"`) and kill that pid.
3. Start it detached from the folder: `setsid nohup npm start >> bot.log 2>&1 &`.
4. **A restart drops the bot out of voice. Someone must run `/join` afterwards.** `AUTO_JOIN=false` is the live setting, so it never joins by itself. `/join` writes the session-open marker and `/leave` closes it (swaps and deleting the active Crawler are refused while open; if the bridge dies in voice, `python3 tools/state.py session-status close`).
5. Check `bot.log` shows `Logged in as Dungeon System AI - Earth#8647` (was `DCC Ears#8647` before the 2026-10-04 rename; and no errors), then `python3 tools/state.py validate` and `ledger verify`.
Run live-campaign tool commands with `DCC_AUTO_PUBLISH=0` unless a publish is wanted.

**Secrets.** `GM_DISCORD_TOKEN`, `GM_WEBHOOK_URL` and `GM_WEBHOOK_KEY` come from the **launching shell's environment** and are **NOT in `.env`**. Start the bot from a shell that has them; a restart from a bare shell loses them (wake webhook off, no channel create/delete). `.env` holds only ids and settings. Never print, log, paste or commit any secret or key (bridge code scrubs them from errors; do not `cat .env` or dump `env`).

**Slash commands.** Eleven (`/join /leave /skip /say /voicecap /shush /gm /session /create /crawlers /delete`). Run `npm run register` **only when a command's name, options or description changes**; code-only changes (flows, screens, tables) need a restart at most. Tables read by file mtime (item reskins, chargen, create-flow lines) need no restart.

**Where things are logged.**
| What | Where |
|---|---|
| Bot output | `/workspace/discord-voice-bridge/bot.log` |
| TTS usage (counts and bytes only) | `logs/tts-usage.jsonl` |
| GM wake counts | `logs/wake-usage.jsonl` |
| Voice events | `logs/voice-events.jsonl` |
| `/create` drafts (mode 600, one per player; archived after 14 days, none with rolled rounds) | `<session data dir>/create-drafts/<discord id>.json` (alpha: `sessions/create-drafts/`) |
| `/create` staff log (no private content) | `<data dir>/create-log.jsonl` |
| State backups | `sessions/backups/` |
| Deleted Crawlers' ledger rows | `sessions/deleted-archive/` |

**Sessions and flags.** Alpha is the live game (data in `sessions/`, no `session.json` profile, so defaults apply). Others (beta) live in `sessions-data/<id>/`, made with `tools/new-session.py`. The active one follows `sessions/active-session.json` (`/session use` after `/leave`) and can be forced at startup with `DCC_SESSION_ID`; Python tools take `--session ID` or `DCC_SESSION`. Never run alpha and beta in voice together. Flags: `create.allow_roll` in `session.json` (new sessions write true; missing = ON; `new-session.py --no-roll` writes false); `limits.pets_enabled` in state (default true; off hides pets and refuses pet add/convert/shop); `campaign.f1_reprieve` (beta: `state.py --session beta set campaign.f1_reprieve true`, otherwise S1 shows Reprieve off). `create.review_mode` is `off` for alpha, `hold` for other sessions.

**Tests (run before any restart).** Python: `cd tools && python3 -W ignore -m unittest discover -s tests -p 'test_*.py'` (**358** OK). Bridge: `npm test` (**186** pass) and `npm run check` (**74/74** files). Live: `state.py validate`, `state.py ledger verify`, `python3 tools/reskin_check.py`, `python3 tools/discord_gm.py publish --dry-run`.

**Fish voice and balance.** TTS provider is Fish (`TTS_PROVIDER=fish`; voice ids and the key are env/`.env` settings, never printed). `npm run usage` prints bytes cost per day/session, the monthly minutes budget, wake counts and the live balance (`--no-balance` skips the request). The bridge checks the balance at startup, about every 30 minutes and after each session closes; below `FISH_LOW_BALANCE_USD` (default **3** USD; a non-numeric value falls back to 3) it logs ONE warning and, if `create.staff_channel_id` is set, posts it there (text only, never spoken).

**`/encounter` (2026-10-04, built and tested, NOT registered, not live).** GM-only slash command in the bridge: `/encounter day:<1-5> [encounter:<id|all>] [block:<kind|slot>] [include_optional:true] [hours:<n>] [confirm:true] [floor:<1-18>]`. It previews (ephemeral) and then posts the player-facing text from `floors/f01/day-NN.json`, built only from `audience_manifest.player_blocks[]` (named fields only; everything else is GM-only). Needs Manage Server. Bridge tests 250/250, `npm run check` 86/86, including a leak test over all five day pages. **To go live:** `npm run register` (adds `/encounter` as the 12th guild command) and one restart (steps above, then `/join`). Until then nothing changes in Discord. Details: bridge README, section `/encounter`.

## 5. Open questions for Caleb

Ask in batches; many entries in the older lists have since been answered by decisions (noted below), so re-check the decision file before asking.

**Species supplement (rules/30 v0.1.4 section 6), 14 numbered, Q12 closed in v0.1.1, so 13 open:**
1. Background swap in the Floor 3 free rebuild too, or species only (draft is species only)?
2. Human leaving Human loses the Versatile feat: accept the loss (default), keep the feat, or swap for a skill?
3. Offer visibility: private Offer Cards with public result (default) or public ceremony?
4. Hobgoblin gate: canon gate (Explosives Handling 5) with DM waiver (default) or strict?
5. Include Bloodbound (curse-based, opt-in)? Is Blood Need the right weight?
6. Felid Nine Lives (Minor) once per Long Rest damage halving alongside Costly Revives; Distractible Hunter DM-triggered or opt-in?
7. Natural weapons use Strength or Dexterity (house change from Unarmed Strike): OK?
8. Hobgoblin free Sapper Workshops as a crafting perk (needs crafting sign-off) or leave out?
9. A later "reissue"/reroll product at all (no price set)?
10. Replacement Crawlers after Floor 3: start as SRD species then get the Offer (default), or pick any option at creation?
11. Which bench oddities in v0.2 (Sasquatch, Frost Maiden, Fairy, Doppelgänger, Primal)? Any Large-size oddity?
12. *(closed in v0.1.1)*
13. Confirm canon stat bonuses and penalties are deliberately not ported.
14. Are Felid forms and Caprid breeds purely cosmetic, or later mechanical subraces?

**Other open lists (read the file for the full text):**
- rules/40 loot deck spec section 5: Gold/Platinum in Floor 1-2 decks; Driftglobe tier (Common vs Uncommon; alpha's was corrected to Uncommon); Laminated Complaint Card truthfulness; stat bump cards (vs "rewards never change dice"); Bag of Holding; `credit_value` use; loot ledger file; Fish word budget. (Q9 and the pet-Crawler slot Q10 are answered: decisions 015, 018.)
- rules/42 house items section 7: Q5-Q13 (Biscuit rarity and value, Fire Breath 4d6 DC 13 vs 3d6 DC 12, Mystery Key on descent, one outer garment, Grudge Ring on Floor 1, Story Box cap vs five deeds, Dean Thudd as Borough Boss, Tiara leaving the floor, Grudge Ring escape). Q1-Q4 resolved.
- rules/45 section 9: item strength (see section 2).
- rules/50 section 10 (six, each with a recommended default): Repair Offset as a separate track; prices per party with the x1/x5/x20/x50 multiplier; Rapport counter for Therapy Route A; Sabotage payout; lockouts; commit-and-reveal logs for GM judgments.
- rules/60 section 13 (three): see section 2.
- Create-flow spec section 7 (Q3-Q8 open, each with a Syndicate default; Q9 answered but its 10-per-player guideline and swap-lock details remain overridable): player-card BUILD block; questionnaire length; review mode for beta (default `hold`, then `notify`); AI GM reading unshared opt-outs at runtime; background pool (PHB 2024 or SRD only); sheet file names; the 10-per-player Crawler guideline.
- Character creation guide section 13: questionnaire length and transparency, visible species on F1-2, Pending Handle, Intake Tag format, comfort hard floors, foot bit, "your mom" question, 12 pre-builts (tables/prebuilt-crawlers.json now has 12), class swap on F3, late arrivals.
- Core rules section 12 (18 items): level track, content scope, fudging, dice, turn timeout, loot pace, attunement, System Inventory vs encumbrance, Long Rest rules, Crowd Pop, revival extras (Back by Popular Demand, Marked for Death ring, Stairwell Checkpoint), floor clock, Floor Bible titles. Items 4 (Reprieve/Death Mode), 13 numbers and 18 (credit multiplier) are decided; verify the rest.
- Floor 1 module section 13: see Backlog item for Floor 1.
- GM-side: player roster for the other two slots; Roll20 account and API access ("optional, later").

## 6. Standing rulings (by decision number; DECISIONS.md has the one-liners)

- **001** Comfort: Ludicrous (cursing, crude, cruelty, foot bit OK); each Crawler can privately opt out and the GM honours it at once.
- **002 / 003 / 005 Death:** Costly Revives, very costly and rare. Death is nearly game over. Revive = Fee (5k/15k/40k/100k) AND two menu picks, then Revival Sickness; never purchasable (needs a Voucher or System Rare Offer, F5+); caps 1 per party per 3 floors, 3 per campaign, 1 per Crawler; only VERIFIED canon revives pre-approved. Cockroach-style save and potions are earned, DM-granted boons; Half-Splat is falling only. Special Brew is crafter-NPC only, max 2 per drinker.
- **Floor 1 Reprieve ON by default for Season Zero, Floor 1 only; tables may turn it off** (Caleb, 2026-10-04; core v0.2.15 §6.0/6.2, Floor 1 module §13 item 16, decision 029). It never applies to a missed-collapse death (decisions 026, 028).
- **029** Book source conflicts: SRD-only content printed; non-SRD backgrounds/feats = table/GM appendix with own reskin names and mechanics summaries only; Floor 2 house timer 10 days (canon 6 is reference); Roll threshold 73+ (decisions/029-book-source-conflicts.md).
- **006** Celestial boxes: one per Crawler for the whole campaign, finale or absurd feat only.
- **007** Voice tags `[SYSTEM]`, `[GM]`, `[ROLL]` (ROLL never spoken). GM and System share one voice; no persona change (Caleb, 2026-10-04). Pacing: 2-4 spoken sentences, one beat, end on a prompt, one reply per wake.
- **008-013 Crafting:** saferoom-only; boons DM-granted only; tables from Floor 2 drop (very rare Floor 1 find, goblin-workshop cache Zone 7b), unusable until Floor 4, upgrade on any floor; 1-round potion cooldown; Boomer 6d6 until level 5; Special Brew never brewed by Crawlers.
- **Crafting prices (decisions 012 v1.1 + 019 v1.2, Caleb): basic table 5,000; Crafting Studio 12,000; Enhanced Crafting Studio 30,000**, at Floor 1 scale, times the floor multiplier. Coupon cap 25,000. Level upgrades 5,000 x target level.
- **009** Species: nine 2024 SRD species at level 1; Floor 3 System offers three (own + two DCC-style oddities), one free rebuild.
- **013 (party size)** Four players. **013b** crafting answers (separate file, same number).
- **015 / 018 Story Boxes:** Floors 1-2 only, hand-picked, one named one-time deed, cap one per table per floor (logged override), opens only in a saferoom, items NOT bound (lootable, tradeable, sellable; fixed sale_value 100/250/500 by rung; story_value is provenance), family-fight deed = opt-in at session zero, fictional rival, no killing, no PvP; rota is a GM guideline; an unopened box is reclaimed when its Crawler dies and the slot frees (020).
- **016** S12 dropped; the Fan Profile is hidden (built from the private survey and play; never call it "quirks").
- **017** Busted is a spontaneous callout: no prompts, no fees, valid only in a scene where the GM logged a tell; a refusal never touches the sealed roll.
- **019** Floor credit multiplier x1 (F1-4), x5 (F5-9), x20 (F10-14), x50 (F15-18): **not** on box credit pulls; **on** achievement rewards and System fees (repairs, Story Box buyback, crafting). Coupons and revive fees stay flat.
- **020 / 021 Multi-Crawler:** any number per player, exactly one active, active one locked for the whole session; `/delete` is log only, no flags, no refund; deleted Crawler frees its Story Box slot; Biscuit pet-Crawler is a separate Crawler played by the owner, no extra slot.
- **022 / 023 Pets:** one pet per Crawler, GM-run SRD Beast CR 1/4 or lower, no slot/loot/credits/XP, death final. **Nobody is ever asked, prompted, hinted at or offered a pet**: it exists only if the player wrote it in their own free text and the GM files it. No pet field in `/create`, questionnaire, chapters or vending wall. A pet earns no Story Box (owner earns the deed, one pet deed per floor). Good Boy Gulp 50 cr and Fold-Flat Kennel 100 cr are off-menu, pet owners only, times floor multiplier, buyback half.
- **024** Roll method (section 4).
- **Reward limits:** leave as written; GM adapts as play goes (Caleb, 2026-10-04). No hard limits on the GM persona.
- **Address rule:** players are "Crawlers".
- **Old item names** on live sheets stay as stored; lookup by `srd_id`.

## 7. Backlog

- **Floor bible rewrite for the Continuum model.** `04-floor-bible.md` carries a "needs Continuum + 5e rewrite" banner and still names F3 "Highstreet Sprawl", F9 "Mandate Wars", F12 "Throne Circuit" (pre-Continuum); its F1 row is pre-5e. Floor docs follow the spine floors/00-campaign-narrative.md v0.3. (core §12 items 15-16; Floor 1 module §13 item 13.)
- **CR-by-floor monster compendium.** On the list; no draft or source file found in the folders this file was built from.
- **Class-selection canon.** Lore has `catalog/class-selection-canon.md` (Floor 3/6/9 process, ledger C-014..C-050, status review). No rules file in rules/ uses it yet; species/background rebuild is covered, class swap on F3 is an open question (character creation §13 Q11; species file says "No class swap here").
- **Achievements as a seed list.** `tables/achievements.csv/.xlsx` (1,823 rows) is a seed list, not a schedule; the GM decides what is notable and what it pays. Floor 1 target 6-10 toasts per Crawler, at least 2 snark-only. Open: relabel Reward as "suggested tier", add a Snark column, re-rarity generated-variant outliers (core §12 item 17; Floor 1 §13 item 14).
- **Floor 1 module rough spots** (floors/f01/00-overview.md §13 open items 3-15): Black Box glimpse, Benefactor Signal trigger, Dale Pruitt recurrence, Proctor Bell hint price, Lights-Out cycle vs clock, boss cheese routes (talk him down 3 x DC 15, diploma DC 13), Variant B nameplate, box cap, Assigned Companion for 2-Crawler tables (Pudding the Mastiff), foot bit dosage, Floor Bible alignment, catalog fixes, seed ID (`SEED-BLACKBOX` vs `SEED-HEATBLACKBOX`).
- **Beta-session note.** A `beta` session is scaffolded with `tools/new-session.py`; alpha and beta never run voice together (decision 014, draft). Before beta: seal a quirk roll for it (`state.py --session beta gm-quirks roll`; Caleb's rule on the sealed roll applies), set `campaign.f1_reprieve true`, check `create.allow_roll`, decide review mode (default `hold`).
- **Roll20 / fog-of-war map: ON HOLD.** Roll20 account and API access is "optional, later" (gm-notes/10-open-threads.md). Fog of war today is narrated: the Floor 1 module reveals zones on the System Map as entered (module §4.2). Do not build until Caleb restarts it.

## 8. How to update this file

- **Syndicate and the Architect both update it** whenever something ships (a rule version, a build, a restart, an audit result, a ruling from Caleb).
- Keep it short: change the facts, bump the version and date, and point to the source file instead of copying text. Move a line from section 4 to section 3 when it is restarted and checked live. Delete answered questions from section 5.
- Never put secrets in it: nothing from `gm-notes/secret/`, no tokens, no Discord ids.
- Every update also touches the INDEX.md line for this file if its description changes.
