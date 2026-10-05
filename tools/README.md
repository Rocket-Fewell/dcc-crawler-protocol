# Campaign Tools (roll.py, state.py, gm_quirks.py, discord_gm.py spotlight)
Owner: Borent Corp Systems Architect | Status: draft | Version: 1.2 | Updated: 2026-10-04
Summary: Shell tools for the AI GM: real dice with a logged [ROLL] line, a safe live-state manager (sessions/state.json), and the GM-only secret-trait and Affinity commands (state.py gm-quirks / affinity). Python 3 stdlib only.

**Rule for the GM: never invent a roll or edit state by hand. Call these tools, and paste the `[ROLL]` line into the GM output channel (it is never spoken aloud).**

Run from `/workspace/dcc-campaign`. Everything uses `DCC_CAMPAIGN_DIR` (default `/workspace/dcc-campaign`). Exit codes: `0` ok, `1` refused (message on stderr), `2` bad input/usage. `--json` on any command gives machine-readable output.

## roll.py

```
python3 tools/roll.py "<expr>" [--label TEXT] [--who NAME] [--dc N] [--json] [--no-log]
```
Prints one line, and appends it with an ISO timestamp to `sessions/rolls-YYYY-MM-DD.log` (alpha; other sessions use `sessions-data/<id>/rolls-YYYY-MM-DD.log`):
```
$ python3 tools/roll.py "2d20kh1+5" --label "Grimsby Stealth" --who Grimsby
[ROLL] Grimsby Stealth (Grimsby): 2d20kh1+5 -> [17, 4] keep 17 +5 = 22
```

| Expression | Meaning |
|---|---|
| `d20`, `2d6+3`, `1d8+1d4-2` | NdM terms with `+`/`-` terms and constants (multiple terms ok) |
| `2d20kh1` / `kl1` | keep highest / lowest N (`k` = `kh`; N defaults to 1) |
| `4d6dl1` / `dh1` | drop lowest / highest N (at least one die must remain) |
| `adv` / `dis` | = `2d20kh1` / `2d20kl1` |
| `adv+5`, `d20+5 adv`, `d20+5 dis` | shorthand combined with modifiers |

- Natural 20 / natural 1 are detected on **kept, added d20s** and appended: `... = 25 (NAT 20!)`. Advantage/disadvantage use the kept die only.
- `--dc 15` appends `vs DC 15 -> SUCCESS|FAIL` (compare only; the GM still rules on crits).
- Limits: 1-100 dice per term, 2-1000 sides, max 200 dice and 20 terms in total, expression max 200 chars, constants max 100000. Anything else: `[ROLL-ERROR] ...` on stderr, exit 2, nothing logged.
- A leading minus needs `--`: `python3 tools/roll.py -- -d4+10`.
- Randomness: `secrets.SystemRandom` (OS entropy). Labels/names are flattened to one line (max 80 chars).
- `--json` fields: `timestamp, label, who, expression, terms[{rolls,kept,dropped,subtotal}], total, nat20, nat1, dc, success, line`.

## state.py

```
python3 tools/state.py <command> [args] [--json]
```
Live state: `sessions/state.json`. Crawler names are matched case-insensitively (a unique partial name also works).

| Command | Example |
|---|---|
| `init [--floor N] [--zone Z] [--force]` | `state.py init --floor 1 --zone "Orientation Pit"` (campaign: Costly Revives, Ludicrous comfort; `--force` replaces, with backup) |
| `add-crawler NAME --player P --class C --species S [--level --hp-max --ac --credits --abilities]` | `state.py add-crawler Grimsby --player Caleb --class Rogue --species Human --hp-max 30 --ac 15 --abilities dex=16,str=8` |
| `show [CRAWLER]` | `state.py show` (party) / `state.py show grimsby` |
| `get PATH` | `state.py get crawlers.grimsby.hp.current` |
| `set PATH VALUE` | `state.py set campaign.current_floor 2`, `state.py set crawlers.grimsby.boons.- '{"name":"Luck"}'` |
| `hp damage\|heal\|set\|temp CRAWLER N` | `state.py hp damage donut 12`, `hp heal donut 5`, `hp set donut 20 --max 28`, `hp temp donut 8 [--replace]` |
| `credits CRAWLER +N\|-N\|=N` | `state.py credits grimsby -250` (refuses to go negative unless `--allow-debt`) |
| `inventory add\|remove CRAWLER ITEM` | `state.py inventory add grimsby "Healing Potion" --qty 2`; remove: `--qty N` or `--all` |
| `achievement add CRAWLER TITLE` | `state.py achievement add grimsby "Doormat" --note "kicked a door"` |
| `condition add\|remove CRAWLER NAME` | `state.py condition add donut poisoned` |
| `box add\|use CRAWLER TIER [--count N]` | tiers bronze, silver, gold, platinum, legendary, celestial (max 1 celestial) |
| `use-revive CRAWLER [--dry-run] [--note]` | `state.py use-revive donut --dry-run` then without `--dry-run` |
| `use-bypass CRAWLER [--kind K]` | `state.py use-bypass donut --kind cockroach` (not a revive) |
| `snapshot` | writes `sessions/state-snapshot-YYYY-MM-DD.json` (same-day snapshot is overwritten) |
| `validate [--file F]` | schema check; exit 1 on errors |
| `backups` / `restore NAME_OR_PATH` | list `sessions/backups/`; restore (validated; current state is backed up first) |

**Paths** are dotted: `campaign.current_floor`, `party.revives_used`, `limits.*`, `crawlers.<name or index>.hp.max`. `VALUE` is parsed as JSON, else taken as a plain string. A `-` list segment appends (`...inventory.-`). Prefer the dedicated commands; `set` is the escape hatch, and still validates.

**HP rules:** damage hits temp HP first, then current, floor 0. The output flags `AT 0 HP` and `MASSIVE DAMAGE` (overkill >= max HP = instant death in 5e). Heal clamps to max and ignores temp. Temp HP doesn't stack (higher wins; `--replace` forces). `hp set` clamps to 0..max. The tool does not add `unconscious`/`dead` or roll death saves: use `condition add`.

**Revive caps** (decisions 002/005; numbers are in `state.json` `limits`): 1 per crawler ever, 3 per campaign, and 1 per party per 3 floors (next allowed when `current_floor - last_revive_floor >= 3`). `use-revive` refuses with exit 1 and changes nothing when a cap is hit. Keep `campaign.current_floor` up to date. Death bypasses (`use-bypass`) only count; `limits.bypass_per_crawler_cap` is `null` (unlimited) until you set a number.

**Crawler fields:** name, player, class, species, level, xp, hp{current,max,temp}, hit_dice{current,max}, ac, abilities{str..cha}, inventory[{name,qty,notes}], credits, conditions[], vows[], boons[], achievements[{name,floor,note,at}], boxes{bronze..celestial}, revives_used, bypasses_used, fan_profile{quirks[],notes,opt_outs[]}, notes.

**Write safety (every write):** lock file `sessions/.state.lock` (stale locks auto-cleared) -> validate the new state (invalid = refuse, nothing written, no backup) -> copy the old file to `sessions/backups/state-<timestamp>.json` (newest 20 kept) -> temp file + fsync + re-read check -> atomic rename. A corrupt `state.json` is never overwritten: commands stop with "not valid JSON" (fix it, or `restore`). Read-only commands never write.

## Public ladder lookup and sealed-roll status (safe to print)

```
python3 tools/state.py gm-quirks level FLOOR [--stress -1|0|1] [--json]
python3 tools/state.py gm-quirks status [--json]
python3 tools/state.py gm-quirks verify
```
- `level 7 --stress 1` -> effective degeneration level (floor level + stress, clamped 0..5; F1-2 L0, F3-4 L1, F5-6 L2, F7-8 L3, F9-11 L4, F12+ L5), its name, and the **glitch d20 max** (a glitch moment if the open d20 is at or below it; 0 = never). Numbers come from `lore/tables/gm-quirks.json`. It never touches the secret roll and says nothing about the GM's traits. Roll the glitch d20 yourself with `roll.py d20`.
- `status` says whether the traits are sealed, when, and prints the **commitment hash** (safe to publish to the table). `verify` recomputes the hash from the sealed file and prints only OK / FAILED.

## GM-ONLY: secret traits and Affinity (do not paste this section's command output anywhere public)

The dungeon-AI GM has hidden traits rolled **once per campaign** (design: `gm-notes/secret/gm-quirk-framework.md`; tables: `lore/tables/gm-quirks.json`, found via `<campaign>/lore/` or `$DCC_GM_QUIRKS_TABLE`) and a hidden Affinity score per player. Everything lives in `gm-notes/secret/` (folder mode 700, files mode 600). `show`, `get`, `snapshot`, `validate`, `backups`, exports and every other public command never read that folder, and `validate --file` / `restore` refuse paths inside it. The tool prints a GM-ONLY banner on every command that shows secret data: **never paste, quote, hint at, voice or save that output.**

```
python3 tools/state.py gm-quirks roll [--campaign-id ID]         # ONCE, before Floor 1. Prints only: GM traits rolled and sealed
python3 tools/state.py gm-quirks roll --force --i-know-this-reveals   # deliberate override: old file archived, public roll log says so
python3 tools/state.py gm-quirks show-gm [--level 0..5] [--json]  # (alias: state.py show-gm) read your traits privately; --level limits tells to one level
python3 tools/state.py gm-quirks reveal --i-know-this-reveals     # FINALE ONLY: marks revealed, prints roll + nonce
```
- `roll` uses `secrets.randbelow` (OS entropy): prior installation d8, fixation d20 (+ d6 variant if the fixation has one), 2 distinct quirks d12 (duplicates rerolled), tic d10. A second `roll` exits 1 and changes nothing. The public roll log (`sessions/rolls-*.log`) gets **one neutral line** (rolled and sealed, plus the commitment hash); the results are never logged there.
- **Commitment** = `sha256( canonical_json(rolls) + "|" + nonce )` (UTF-8, lowercase hex; canonical = `json.dumps(rolls, sort_keys=True, separators=(",", ":"))`). Publish the hash from `gm-quirks status`. At the finale `reveal` prints the nonce so anyone can recompute it.
- The sealed file is never edited by the tools (only the `revealed` flag changes, via `reveal`, which archives a copy first). Repairs change the *level*, never the roll.

```
python3 tools/state.py affinity register PLAYER_ID [--name N --character C --floor F]   # defaults come from state.json crawlers
python3 tools/state.py affinity register --from-state                                    # all crawlers' players, idempotent
python3 tools/state.py affinity add PLAYER_ID DELTA --reason "..." --scene SCENE --floor N --session S [--evidence "<=25 words"] [--fixation-id FX-NN] [--trigger KEYWORD]
python3 tools/state.py affinity new-scene SCENE_ID
python3 tools/state.py affinity drift --floor N [--session S]
python3 tools/state.py affinity status [PLAYER_ID] [--json]
```
(`gm-quirks affinity ...` is an alias.) Player ids are the lowercase player name from `state.json` (Caleb -> `caleb`).
- `add`: `--reason`, `--scene`, `--floor`, `--session` are required; player must be registered; DELTA is a non-zero integer -10..+10 (normal use +/-1..3). Score stays in -10..+10, and the **net change per player per scene is clamped to +/-3**: the log records `raw_delta` (asked) vs `delta` (applied) and `capped`. A new `--scene` id starts that player's tally over; `new-scene` resets everyone at once (repeating the *current* scene id does not reopen the cap).
- **Opt-outs:** a crawler's private `fan_profile.opt_outs` (state.json) always wins. If an opt-out term appears in the trigger, reason or evidence, or matches the fixation named by `--fixation-id`, `add` refuses (exit 1, nothing logged) without echoing the opt-out. If state.json is unreadable, scoring is refused.
- `--fixation-id` must equal the sealed fixation (a mismatch is refused and does not say what the real one is). Leave it off for generic scoring.
- `drift --floor N`: every score moves 1 toward 0, once per floor (tracked in `last_drift_floor`; repeated calls are no-ops, and skipping floors still drifts once). Run it when a floor starts. Players registered during floor N owe no drift for floor N.
- Bands come from the JSON (`Favor +7..+10`, `Mild perks +3..+6`, `Neutral -3..+2`, `Petty -6..-4`, `Vindictive -10..-7`). Affinity never changes dice, DCs, damage or rules text.
- Files: `gm-quirk-roll.json`, `gm-affinity.json` (backed up before every write into `gm-notes/secret/backups/`, newest 20 kept), `gm-affinity-log.jsonl` (append-only audit log), `archive/` (replaced or revealed roll files). Locking: `gm-notes/secret/.gm.lock`.
- Permissions note: there is no git repo in `/workspace/dcc-campaign`. If one is ever created, add `gm-notes/secret/` to `.gitignore` before the first commit, and keep it out of any export or zip.

`python3 tools/sim_floors.py [--trials N --floors N --scenes N --players N --seed N --json]` is a planning-only Monte Carlo (level mix, glitch odds and Affinity band shares per floor). It reads only the public numbers and never touches the campaign folder.

## discord_gm.py spotlight (limit which player wakes the GM)

The Discord bridge wakes the GM (paid run) whenever a player line is transcribed. During a one-player exchange, tell it who to listen to:

```
python3 tools/discord_gm.py spotlight set "Trailer Park Moses" [--alias Moses --alias TPM] [--note "vending wall"]
python3 tools/discord_gm.py spotlight show
python3 tools/discord_gm.py spotlight clear        # when the exchange is finished
```

* Writes `sessions/spotlight.json` atomically (override the path with `SPOTLIGHT_FILE`): `{"player","aliases","updated","note"}`. No Discord token or network needed.
* While set, the bridge wakes the GM only for (a) that player (name match is case/accent-insensitive; the name or an alias may be a substring of the player's Discord display name/username or vice versa, so give the name they use in voice chat) or (b) **any** player saying the standalone word "AI" ("hey AI", "A.I.", "A I"; not "said", "main", "again"). Every line is still posted to #table-transcript; you read them with `discord_gm.py new` as usual.
* **Fails open:** player `null`, a missing/empty/malformed file, or an `updated` older than `SPOTLIGHT_MAX_AGE_MINUTES` (default 20) all mean open floor: every line wakes you. For an exchange longer than 20 minutes, run `spotlight set` again (same arguments) to refresh the timestamp.
* **Always `spotlight clear` when you say you are finished**, so the table is not left muted.
* `npm run usage` in the bridge reports wakes fired, lines skipped by the spotlight, wake-word overrides and an upper-bound estimate of saved wake-ups.

## discord_gm.py stop (kill switch for the bridge's voice)

```
python3 tools/discord_gm.py stop
```

Writes `sessions/voice-control.json` (`VOICE_CONTROL_FILE`) atomically as `{"action":"flush","id":"<unique>","ts":"..."}`. Within about a second the Discord bridge stops the current speech and clears its whole TTS queue (same as the players' `/shush`). It does not delete messages already posted in #gm-voice, and anything you post afterwards is spoken normally. Needs no Discord token. Players can also use `/shush` (stop talking) and `/gm pause|resume|status` (stop/restart waking you).

## Tests
```
PYTHONPATH=tools python3 -m unittest discover -s tools/tests -p 'test_*.py'      # 358 tests (run from the campaign root; PYTHONPATH=tools lets the tests import the tools), temp dirs via DCC_CAMPAIGN_DIR, no network, Discord always mocked
```
`tests/test_gm_quirks.py` covers the sealed roll, commitment, caps, drift, opt-outs and the proof that no public command or file outside `gm-notes/secret/` ever carries secret content. Test files use underscores because Python cannot import hyphenated module names; the tools are single words.

## Credit ledger (state.py)

Every credit change made through `state.py` (credits, set, add-crawler, restore...) appends a line to `sessions/credit-ledger.jsonl`:
`{seq, ts, crawler, delta, balance, reason, source, command}`. Pass `--reason "Achievement: Buddy System" [--source achievement|box|vendor|loot|hint]`
on any state.py command that changes credits; without it the entry is stored as `unspecified` and a warning is printed.

- `python3 tools/state.py ledger show [--crawler X] [--limit N]`
- `python3 tools/state.py ledger verify` - running totals vs the sum of entries vs state.json (exit 1 on problems)
- `python3 tools/state.py floor-lost CRAWLER --reason TEXT [--floor N] [--mark-dead] [--dry-run]` - decision 028 write-off: a Crawler who misses the floor collapse is dead and their credits and items are destroyed with the floor. ONE append-only ledger entry (`event: floor_lost`, `source: floor_lost`, `delta` = minus the balance, `balance` 0, `destroyed: {coins, items[], item_count}`) so the Crawler's total reconciles to 0 with no special case; the inventory is emptied. The Crawler must already be Dead (or pass `--mark-dead`, which also adds the condition and applies the usual unopened-Story-Box reclaim). Refuses NPCs/the AI (they lose nothing) and a body with nothing left. XP, achievements and loot boxes are not touched. Run it AFTER looting.
- `python3 tools/state.py loot-body DEAD SURVIVOR --reason TEXT [--coins N|all] [--item NAME[=QTY]]... [--all-items] [--floor N] [--dry-run]` - a survivor takes coins/items from the body while the floor still stands. Two linked ledger rows (`event: body_loot`, `role: from|to`, shared `transfer_id`, `coins`, `items`) debit the body and credit the survivor by the same integer, so no credit is counted twice or lost; items move like `transfer` (Story Box provenance kept). Refuses a body that is not Dead, a dead/benched survivor, and a Crawler of the same player. `ledger verify` checks both events (floor_lost balance 0 and destroyed.coins = -delta; every body_loot pair cancels and its item lists agree).
- **Accountant fixes for `floor-lost` / `loot-body` (job 3).** `--item NAME=QTY` takes a whole number of 1 or more written with ASCII digits 0-9: `Rope=-1`, `Rope=abc`, `Rope=2.5`, `Rope=` and a missing name are refused with a clear message, `Rope=0` is refused as "a quantity of 0 takes nothing" (it is never silently turned into 1); a bare `--item Rope` still means 1. `--coins` and `--floor` accept ASCII digits only (look-alike Unicode digits such as Arabic-Indic or fullwidth are refused), `--floor` must be 1 to 18, and `credits` amounts are ASCII-only too. `loot-body` refuses a pet or companion as the looter (and as the body): only player and pet-crawler records can loot (decision 022). `floor-lost` on a Crawler with nothing left now exits 0 with "nothing left to destroy" and adds no ledger entry (it used to exit 1). New `floor_lost` entries also store `destroyed.items_digest`; `ledger verify` fails when `destroyed.item_count` does not equal the summed item quantities (items emptied or a quantity edited), when an item row is malformed or repeated, or when the items list no longer matches its fingerprint (list and count edited together). Tests: `tests/test_floor_lost.py` (`AccountantFixesCase`).
- `python3 tools/state.py ledger import file.json` - one-time backfill into an EMPTY ledger (`approx_ts` marks guessed times)
- Fixed: `credits Bone 25` (no sign) used to parse as +5; unsigned now means +25. Prefer `+25`, `-5`, `=100`.

## Player channel publisher (discord_gm.py -> publisher.py)

Each crawler gets a read-only text channel in the "Crawler Sheets" category. The GM bot posts a NEW FULL CARD (line 1 = `Credits: N (+delta, reason)`,
HP/AC/abilities, conditions, standing orders/reaction, inventory grouped Weapons / Armor / Magic / Gear with short effect text, achievements)
whenever the player-visible state differs from the last published snapshot. Long cards split into several messages. State files stay the source of truth;
only the fields above are ever posted (never fan_profile, notes, or anything under gm-notes/).

- `python3 tools/discord_gm.py publish [--crawler X] [--full] [--dry-run]` - post changed cards (`--full` re-posts even if unchanged)
- `python3 tools/discord_gm.py channels` - crawler -> channel map + whether the GM bot can post there
- `python3 tools/discord_gm.py setup-channels [--dry-run]` - create the category and ONE channel PER CRAWLER, named `<player>-<crawler>` (e.g. `hornn-horn`; pet-Crawlers `<player>-<pet>-sheet`; duplicate names get `-2`, `-3`; at 45 channels it warns, at 50 it opens `Crawler Sheets 2`, `3`, ...). Needs Manage Channels on the GM bot role; otherwise prints the manual steps. Existing mapped channels (`#hornn-sheet`, `#moses-sheet`) keep their names.
- `python3 tools/discord_gm.py register-channel <crawler> <channel-id> [--no-verify]` - use a channel you created yourself (name a Crawler, not a player: a player with several Crawlers is ambiguous). The map is keyed by Crawler name and each entry carries `owner` (the player).
- Automatic: after any state.py change a detached `publisher.py --auto` waits ~3 s (coalescing bursts), then publishes. Best effort: never blocks or fails the state change; failures go to `sessions/publish.log` and the next publish retries. Off with `DCC_AUTO_PUBLISH=0`.
- Files: `sessions/player-channels.json` (map), `sessions/published-snapshots.json` (last posted), `exports/card-data.json` (item category + effect text; an item's own `notes` overrides it).
  Add a new item to card-data.json so its card line shows the effect.
- The channels are not #gm-voice (formerly #dcc_mouth; the only channel the bridge speaks) and not #table-transcript (formerly #dcc_ears; what the bridge's STT posts into and what wakes the GM), so nothing posted there is spoken or wakes the GM.

## create-crawler, kinds, sessions (state.py)
- `state.py [--session X] create-crawler --file spec.json`: builds a crawler from a spec (name, player, class, species, abilities, build{}, opt-outs as strings or `{kind, topic, shared}`, `kind` player|pet|companion|pet-crawler + `owner`, intake_tag unique). Credits come from `credit_breakdown` rows: one `Starting credits: <Class> package A|gold option` row per source, then one `Vending Wall:` row per purchase. Only `kind: player` crawlers count toward `limits.max_crawlers` (default 4). `--session X` goes BEFORE the subcommand.
- `new-session.py <id> [--no-roll]`: scaffolds a non-alpha session (refuses `alpha`, refuses to overwrite). Does not switch the bridge's active session. Its `session.json` gets `create.allow_roll: true` (the Roll ability method at `/create` S8, decision 024; `--no-roll` writes false). A missing or non-boolean `allow_roll` also means ON; the live alpha has no profile and so offers Roll. The bridge logs every Roll die through `roll.py` (`S8 roll r<round> <A|B|C><1-6>`, 18 per round).
- Bridge `/create` **Cancel build** (decision 023): a red button on every `/create` screen asks "Trash everything?" once (Yes, trash it / No, keep going), then deletes the uncommitted draft including its rolled rounds, so a fresh `/create` gets a fresh roll; it works on old messages and during an open session, and a draft already written to state (a registered Crawler) is refused and left untouched. Logged as `build_cancelled` (no content) in `create-log.jsonl`.
- `gm_lock.sh acquire|release [session]`: per-session lock (alpha: `sessions/.gm-lock`, others: `sessions-data/<id>/.gm-lock`). Session resolves from arg, `DCC_SESSION`, persisted active file, then alpha.

## Loot, boxes, banner (state.py, loot.py, ledgers.py)
- **Safe-room rule (Caleb, 2026-10-04): every loot box, Story Boxes included, opens only in a safe room.** `box open`, `loot draw` (a draw is a box pull) and `loot story-box --open` refuse with "loot boxes can only be opened in a safe room" unless the command has `--safe-room` or the scene flag is on: `python3 tools/state.py scene safe-room on|off|show [--note T]` (stored in the session's `scene.json`; turn it off when the party leaves). `--dry-run` is allowed anywhere. The ledger lines record `safe_room: flag|scene`. Earning a box (`box earn`) needs no safe room.
- `loot draw FLOOR ZONE --crawler X [--tier T] [--pull-type P] [--box-type B] [--pick ID] [--deed D] [--safe-room]`: reads `tables/loot-decks/*.json` wrappers with `schema: loot-deck/*` (other JSON there is skipped). Random draws skip needs-verify stubs, weight-0 and restricted-tier cards, other crawlers' exclusives, already-drawn uniques, and a repeat of the same non-consumable on one floor. Weight-0 and restricted-tier cards only via `--pick`. Each draw updates inventory (or credits, ledger reason `<Tier> box pull <id>`, source `box`), `card-data.json`, `loot-ledger.jsonl`, `loot.log`.
- `loot totals [--crawler X] [--floor N] [--json]`: per-crawler economy value and, if present, story value (separate). Sales of Story Box items are listed as `FLAG:` lines and counted toward the 1,500-per-floor inflation flag (the award's story value is not). `loot show [-n N] [--crawler X]`.
- `loot totals ... --include-credits [--credit-sources a,b] [--assume-floor N]` (optional, Q-003 / budget A12 + Q5; the plain `loot totals` above is unchanged): adds an ALL-IN section per Crawler per floor = box value + Story Box sale proceeds + credits earned outside boxes (credit-ledger entries with a positive `delta` and `source` `encounter`, `achievement`, `toast` or `r1`; box pulls are not counted twice; spending, sales, transfers, body loot, write-offs and intake credits are never counted). Record the floor on those entries with `credits CRAWLER +N --reason ... --source encounter --floor N`; entries without a floor are shown as "floor not recorded" unless you pass `--assume-floor N`. All-in over 1,500 credits for a floor is flagged. For Floor 2 it also prints the optional A12 valve check: at an all-in running total of 900 or more the GM may hand-pick the Boss Box from cards worth 175 or less (a GM option, nothing is enforced). `--json` adds an `all_in` object. Tests: `tests/test_loot_totals_credits.py`.
- **Story Boxes (Legendary, approved by Caleb 2026-10-04, rules/40 §2.8)**: hand-pick only, never random; `loot draw` refuses Legendary cards and points to `loot story-box`. Two steps:
  1. **Award** (any time): `loot story-box FLOOR ZONE --crawler X --pick ID[,ID] --deed "what happened" --deed-id SLUG [--witness W] [--gm-note N] [--when T] [--box-name N] [--shared-with A,B] [--override-cap "reason"] [--dry-run] [--no-publish]` records the deed in `story-box-ledger.jsonl`, writes a box-ledger `earned` line, adds 1 `legendary` to the crawler's unopened boxes and announces "STORY BOX EARNED (unopened)". Nothing enters the inventory yet. `--dry-run` checks everything and writes nothing.
  2. **Open** (safe room only): `loot story-box --open --crawler X [--box-id ID] --safe-room [--dry-run]` adds the item(s), writes `card-data.json`, the loot ledger lines and a box-ledger `opened` line, then refreshes the player's card. A box opens once; a Dead crawler can't open one (it stays queued).
  Rules: cap **1 Story Box per FLOOR** (`limits.legendary_cap_per_floor`; an unopened box counts; more needs `--override-cap "reason"`, logged); each deed pays once (registry key = `--deed-id`); `--pick A,B` is one box (same deed or box name), counted once, with a recorded same-box reason; the spotlight rota ("every living Crawler gets a first before anyone a second") only **warns**, it never blocks. Story Box items are **not bound**: they can be looted from corpses, transferred and sold (an old `bound` field is still readable but ignored; no `[BOUND]` marker). `story_value` (card `story_value`, else `credit_value`) is provenance only: `economy_value` is 0, it is never auto-credited, a Legendary card that grants credits is refused. Each item row carries `story_value`, `story_box_id`, `card_id` and `sale_value` (the card's, default 500). Warnings (never blocking): no `power_note:` in the card notes, empty effect text, a deck HOLD note, no witness/GM note.
  `loot deeds` lists the registry. `limits show|set KEY VALUE` (`legendary_enabled`, `legendary_cap_per_floor`, `max_crawlers`, revive caps).
- `sell CRAWLER ITEM --reason TEXT [--qty N] [--price N] [--floor N] [--dry-run]`: an ordinary credit-ledger transaction (source `sale`). A Story Box item sold to the System pays the card's `sale_value` (100/250/500 at Floor-1 scale, default 500) x the floor multiplier of the sale floor (x1 F1-4, x5 F5-9, x20 F10-14, x50 F15+; `--floor` overrides the current floor), never its story value. `--price N` sets the total by hand (needed for items with no sale_value). Story Box sales are FLAGGED, not blocked, in `loot totals` and `ledger verify` (the ledger line keeps `provenance.story_value`). Credit multipliers: box pulls get **no** floor multiplier (card credits are paid as written); achievement rewards and System fees do; the buyback uses the sale floor's multiplier.
- `transfer FROM TO ITEM --reason TEXT [--qty N] [--price N] [--allow-debt] [--dry-run]`: crawler to crawler: a gift, a trade, or loot from a corpse. `--price` is a free-form credit payment from TO to FROM (two ledger lines, no multiplier); a priced Story Box transfer is flagged like a sale. Provenance moves with the item. Pet-Crawlers are not items and can't be traded, sold or looted.
- `box earn|open|show` (`add|use` are aliases): box-ledger entries with `--deed --box-name --contents --reason`; `open` needs `--safe-room`/scene flag. Legendary boxes are Story Boxes only (use `loot story-box`).
- `banner log "<text>" [--crawler X]`, `banner show [-n N]`: `banner-archive.jsonl`.
- `achievement add ... --reward TEXT`: reward text is stored and shown on the card.

## Busted call and the sealed repair log (rules/50 §6, §10)
- `state.py gm-quirks guess --crawler X --floor N --scene ID --kind fixation|quirk|tic|tell|prior-installation --trigger "the player's call"` (also `python3 tools/gm_quirks.py guess ...`): prints ONLY `Busted` or `Not busted`. A call is valid only in a scene where the GM logged a tell (`repair-log tell --scene S --floor N`, scene + floor only, no quirk details); otherwise it is refused with "no tell was shown this scene" before the sealed roll is consulted (the refused call does not use up the scene). Kind must be equal and the wording must match the sealed trait's keywords (lenient on wording, strict on meaning; traits without a keyword list get one derived in memory). One call per crawler per scene; a repeated call (same kind and words) is rejected; a miss has no other consequence (no fee, no Stress, no per-floor limit). A hit records Therapy unlocked (Floor 8+, 250 x multiplier, no DC). Grading lives in `tools/busted.py` (pure functions); the repair log in `tools/repair_log.py`. Only the player's text and the result are logged. Errors are generic and never leak sealed data.
- `state.py repair-log add --kind fit|busted|rapport --value V --crawler X --floor N [--scene S] [--note T]`: commits the GM's call BEFORE the dice into `gm-notes/secret/repair-log.jsonl` (mode 600, append-only, hash-chained, random nonce per line). Prints only `committed #N` and the chain head. `repair-log tell --scene S --floor N` records that a tell was shown (opens Busted calls for that scene), `repair-log verify` checks the chain, `repair-log calls` lists the players' own calls, `repair-log reveal --finale` prints everything (refuses without `--finale`).

## Pet-Crawlers (Enhanced Pet Biscuit)
`create-crawler` with `"kind": "pet-crawler"`, `"owner": "<the player Crawler who made it>"`, `"pet": "<pet name>"` and `"player"` = the owner's player (refused otherwise): the pet becomes its own Crawler, played by the player who made it, and takes **no extra slot** (only `kind: player` counts toward `max_crawlers`; not on the Story Box rota). It consumes one `Enhanced Pet Biscuit` from the owner's inventory (no biscuit: refused unless `"biscuit_waiver": "why"`). **One conversion per LIVING (non-deleted) pet-Crawler** (Caleb 2026-10-04, no tombstone): a second conversion of the same owner+pet is refused while the first pet-Crawler exists; after `crawler delete` a new conversion is allowed, and still needs a NEW Enhanced Pet Biscuit (the old one is not restored). `state.py party [--json]` lists the roster for GM tools: `encounter_count` (players + pet-crawlers, use it for encounter budgets) vs `party_slots` (players only). It gets its own sheet channel `<player>-<pet>-sheet` from `discord_gm.py setup-channels`. A pet-Crawler follows its owner's active/benched state; deleting its owner leaves it on file, benched. An unused biscuit is an ordinary item (tradable, sellable, lootable); a fed one is consumed. The pet-Crawler itself can't be traded, sold or looted.

## Plain pets (GM-run; decision 022 rules, decision 023 tooling)
A plain pet is data on its owner's Crawler record (`pet`), run by the GM. It is not a Crawler (no slot, credits, XP, loot, trades, sales or ledger rows) and is separate from a biscuit pet-Crawler. **Nothing in `/create`, the questionnaire or any player command knows about pets**; the GM reads the free text and files the pet.
- `state.py pet add OWNER --name N --species S [--description T] [--quote "player's words"] [--cr 1/4] [--override WHY]`: species must be on `tables/pet-species.json` (the 48 plain SRD 5.2.1 Beasts of CR 1/4 or lower, no swarms; dog/rottweiler = mastiff, snake = venomous snake; Axe Beak, Stirge, Flying Snake, Giant Owl, swarms and Giant Fly need an override); anything else needs `--override` (logged). Refused when the owner already has a living pet (or a pet that became a pet-Crawler that is still on file; once that pet-Crawler is deleted a new pet and a new conversion are allowed), when pets are off, or the name is taken. A benched owner may have a pet.
- `pet show [OWNER]`, `pet mark-dead OWNER --reason T` (alias `kill`; final, no revive), `pet remove OWNER --reason T` (error correction, logged), `pet convert OWNER --file SPEC.json` (the Enhanced Pet Biscuit: runs `create-crawler` for the pet-Crawler with its biscuit, slot and one-conversion rules, then the plain pet becomes `became-crawler`; Good Boy Gulp stops working on it).
- `pet shop OWNER` lists the two off-menu items with prices; `pet shop OWNER heal-critter-potion|pet-carrier --reason T [--qty N] [--floor N] [--sell] [--override WHY]` buys (50 / 100 credits at Floor 1 scale x the floor multiplier through the credit ledger) or sells back at half. Buying needs a LIVING pet on file (or the GM's logged `--override`); benched Crawlers cannot buy. `pet heal OWNER --reason T` spends a Good Boy Gulp (2d4+2, the GM applies it).
- Log: `pet-log.jsonl` (added, died, removed, converted, shop-buy, shop-sell, healed). Card: one `Pet (GM-run): name, species (CR)` line on the owner's own card, only while the pet is alive. `party --json` lists it under `companions` (no slot, `counts_in_encounters: false`; the encounter budget is the GM's call, rules/60 section 9). `/delete` of the owner removes the plain pet with it (kept in the archived state copy); a biscuit pet-Crawler is a separate Crawler and is not cascaded.
- **Switch:** `state.py limits set pets_enabled false` (default true): `pet add`, `pet convert` and `pet shop` refuse ("pets are off"), cards and `party` hide pets, existing records stay on file. The bridge never lists `non_srd` items (heal-critter-potion, pet-carrier): they are dropped from `/create`, the price list and every shop lookup.

## Audit fixes (2026-10-04)
- `/delete` archives never lose rows (dedupe on the full row; ledger `seq` never reuses a number that sits in `deleted-archive/`), re-checks existence, session and ownership inside the lock, and archives a legacy sheet file by its heading (e.g. `hornn-wizard.md`). `ledger verify` also checks the archive (no duplicate rows or seq, balance chains add up).
- A new Crawler starts **benched** if its human has ANY Crawler on file or a session is open; only a human with none and no session gets an active first one. `crawler activate` refuses a dead target; the session lock stops a swap-out of an active Crawler but not the first activation of a human who has none.
- Ownership: a Crawler with `build.discord_user_id` is owned by that account only; name matching is the fallback for legacy Crawlers with no id (Horn now has hers; Bone Wifebeater's id is still to be set: `state.py set crawlers.bone-wifebeater.build '{"discord_user_id":"ID"}'`).
- Benched Crawlers: `inventory add`, `hp`, `achievement add` (intake toast passes `--benched-ok`) and raw `set crawlers.<name|index>.credits|xp|boxes|inventory|achievements|hp...` are refused. The Story Box rota counts active player Crawlers only; the banner no longer says "Box Box".
- `session-status open` is idempotent and a re-open within 30 minutes of a close keeps the same swap window (`--fresh` starts a new one); the bridge closes the marker on any voice leave and on shutdown.
- `loot story-box ... --reaward "why"`: re-award a deed whose earlier box was RECLAIMED (holder died unopened); refused if any earlier box was opened, sold or released by `/delete`. New box id `sb-F-deed-r2`, logged with `reaward_of` and the reason.

## Several Crawlers per player: active / benched, session lock, swaps, delete (decisions/020 + 021)
- **Status.** Every player Crawler and pet-Crawler has `status: active|benched`. A human's first Crawler is active; later ones start BENCHED (`add-crawler`/`create-crawler` do it; a human = same `build.discord_user_id`, else the same `player` name). Only the ACTIVE Crawler takes a party slot, counts in `party --json` `encounter_count`, earns credits/XP/boxes/loot/Story Boxes, or can trade. Benched Crawlers are refused with a clear message (GM correction: `--benched-ok "why"`; never for sell/transfer). Benched sheets stay published and show **BENCHED**. `state validate` fails if one human has two active player Crawlers.
- **Moves between a player's own Crawlers are refused** (`transfer`), active or benched. Starting credits come only from the Crawler's own `/create`.
- **Death with an unopened Story Box (Caleb 2026-10-04):** `state.py condition add X Dead` (or `Deceased`) reclaims every unopened Story Box that Crawler holds: a `reclaimed` event in `story-box-ledger.jsonl` and `box-ledger.jsonl`, `boxes.legendary` goes down, and `loot.legendary_count` no longer counts the box, so the floor slot is free. The deed stays closed; a revived Crawler does not get the box back; an opened box is untouched.
- `state.py crawler list [--player P | --user-id ID]` - the roster. `state.py crawler migrate` - set `status` where missing (idempotent; run once on an old state).
- **Session marker.** `state.py session-status open|close|show [--note T]` writes `<data>/session-status.json` (`status`, `since`, `opens` = the between-session window counter). A session counts as OPEN when that file says open OR a GM run holds a fresh `.gm-lock` (< 120 s). The bridge `/join` writes `open` and `/leave` writes `close` (best effort, needs a bridge restart to load). **A stuck "open" (bridge crashed in voice) is cleared with `state.py session-status close`.**
- **Swap lock.** `state.py crawler request CRAWLER --reason T --as-user ID|--as-player P` records a player's request (`sessions/swap-requests.jsonl`; changes nothing); `crawler requests` lists pending ones. `state.py crawler activate CRAWLER --reason T [--by GM] [--dry-run] [--override-window WHY]` is the GM command: REFUSED while a session is open (even in a safe room), when the target is not that player's Crawler (with `--as-*`), or when the player already swapped in this window (one swap per player per between-session window; the first activation after the active Crawler was deleted is not a swap). It benches the previous active one and its pet-Crawlers, and logs to the append-only `sessions/swap-log.jsonl` (`event: swap` with who/from/to/floor/reason/window; `event: refused` with the reason).
- **Delete.** `state.py crawler delete CRAWLER --reason T --confirm CRAWLER [--as-user ID|--as-player P] [--by WHO] [--keep-channel] [--dry-run]` (housekeeping: no penalty, no flag). Without `--confirm NAME` (the exact name) it only previews. Refuses another player's Crawler (with `--as-*`) and the ACTIVE Crawler while a session is open (a benched one can go any time). Order, under the state lock: ledger rows move to `sessions/deleted-archive/<crawler>-ledger-rows.jsonl` and out of `credit-ledger.jsonl` (so `ledger verify` still passes), a state backup is taken, the state record is copied to `deleted-archive/<crawler>-state-<ts>.json`, the Crawler leaves `state.json`, its sheet file `characters/<player>-<crawler>.md` moves to the archive (its INDEX line is dropped), its `player-channels.json` entry and published snapshot go, and its own Discord text channel is deleted (never the voice/transcript channels, never a channel another Crawler still uses, only inside the Crawler Sheets categories; no token or an API error = state still deleted, channel left, message says so). Nothing is refunded. A Story Box awarded to it gets a `released` event in `story-box-ledger.jsonl` unless another living Crawler still holds one of its items: the per-floor cap (`loot.legendary_count`) then no longer counts it; the deed stays closed. A dead Crawler that is not deleted still counts (unless it died holding an UNOPENED box: see below). Its pet-Crawlers stay on file, benched. The append-only `sessions/delete-log.jsonl` records who, when, credits/items/boxes held, active/benched, alive/dead, session open/closed and the floor, and the command prints how many Crawlers that player has deleted this floor (print-only, for the GM to spot cycling).
- Bridge: `/crawlers` (ephemeral list with sheet-channel links and a "request a swap" menu; a request only, refused with a plain message while a session is open) and `/delete <name>` (autocomplete lists only your own; warning, then a button, then you type the exact name; Cancel is the default). `/create` by a player who already has a Crawler creates a benched one filed under the same `player` name. Bridge restart + `npm run register` load them.
- `python3 tools/reskin_check.py` - checks that `tables/item-reskins.json` (a symlink to Lore's file, never a copy) matches the sha256 in `item-reskins.version.json`; exit 1 on a mismatch, a missing version file only warns. The bridge warns at startup too.

## Species and class reskins (species, lineages, classes, class options)
Flavor display names for what `/create` lists or names, the sibling of the item reskin table. **Names and flavor only**: the 5e name stays the id; state.json, the ledger, dice, stats and rules never read this table. Content: **DCC Lore**'s file (adopted as is, not reinvented). Wiring and tool: Architect. Decision note: decisions/023.

- **Files:** `tables/species-class-reskins.json` (schema `species-class-reskins/0.1.0`, `entries[]`) and `tables/species-class-reskins.version.json` (`version`, `sha256`, `entry_count`, ...), copied together from `/workspace/dcc-lore/tables/` (Lore builds them with its `tools/species_class_build.py` and checks them with `tools/species_class_check.py`). Override path: `SPECIES_CLASS_RESKINS_PATH`. **Lore's v0.1.4 (65 entries, sha256 eccfef79fddf...) is copied into `tables/` but INERT: not live until Caleb approves.** The names show only when `create.species_class_reskin` is exactly `true` in the session's `session.json` (default OFF; with the flag off or no file every name is plain 5e). To go live: `python3 tools/species_class_reskins.py --enable [--session ID]` (config only; no register; the tables are read by mtime, but the bridge CODE needs one restart once). To stop: `--disable`. Variants (`species_variant`, e.g. Felid cat/cat-girl/tigran/were-cat) are display-only with `base_id`/`rules_entry: false`, arrive at the Floor 3 Offer and have no `/create` UI; lineages carry `base_id` + `chargen_value` (the exact chargen option string). The checker fails on a missing/unknown `base_id`, a base/parent mismatch, a variant with a `chargen_value`, a lineage `chargen_value` that is not an exact chargen option, duplicates and id collisions.
- **Entry (Lore's fields):** `id`, `kind` (`species` | `species_variant` | `species_lineage` | `class` | `class_option`), `base_id`, `chargen_value`, `rules_entry`, `long_label`, `parent_id`, `srd_name`, `display_name`, `combined_label` (**"Our Name (5e Name)"**), `nation`, `flavor`, `spoken`. The bridge shows `combined_label` exactly as written (never rebuilt, so Lore can change the wording and the parenthesis form); if it is missing the bridge uses `display_name (srd_name)`, and if the entry is missing it shows the plain 5e name. Labels over 100 characters (a Discord select limit) are cut at the display name and keep `(5e Name)`.
- **Ids** (Lore's scheme: lower-case kebab, apostrophes dropped): species `elf`; class `wizard`; lineage `<species>-<option without " Elf"/" Gnome">` (`elf-high`, `gnome-rock`, `dragonborn-black`, `goliath-storm`, `tiefling-infernal`); class option `<class>-<option>` (`cleric-protector`, `druid-warden`). Subclasses: `/create` is level 1 and shows none (Lore: "No level-3 subclasses are chosen in /create").
- **Where it shows:** S1 pre-built list, S5 species and lineage (picker and text), S6 class and class option (Cleric Divine Order, Druid Primal Order; picker and text), S10 class prompt, the S11 spell line, S16 BUILD block, S17 line, the Crawler sheet file (`characters/*.md`), staff/review notes, the `/crawlers` list and the Discord card heading (publisher). Not changed: state.json, the credit ledger, `state.py` output (GM tooling), the repo INDEX line a commit adds, `build.*` fields.
- **List every id that must be covered:** `python3 tools/species_class_reskins.py --ids` (add `--json` for a machine list). Today **61 ids: 21 species (9 shown in `/create` + 12 Floor 3 oddities from rules/30 section 4), 24 lineages, 12 classes, 4 class options**; 49 are shown in `/create`.
- **Check coverage + hash:** `python3 tools/species_class_reskins.py` (the `tables/` copy: structure, sha256 vs the version file, coverage; "ABSENT" and exit 0 when not in place), `--path /workspace/dcc-lore/tables/species-class-reskins.json --strict --house` (check Lore's file before copying: exit 1 on any missing id, a hash mismatch or a structure error), `--json`. Lore's own `python3 tools/species_class_check.py` (in `/workspace/dcc-lore`) is the stricter content check. Tests: `tools/tests/test_species_class_reskins.py`, bridge `test/names.test.js` (fixtures only; placeholders never ship).

## Background reskins (S7 Prior Employment)
Display names for what `/create` S7 (and the S10 background package) lists: the sibling of the species/class table. **Names and flavor only**; ids, state.json, the ledger and the rules keep the 5e names. Content: **DCC Lore**'s `background-reskins.json` (adopted as is). Wiring and tool: Architect.

- **Files:** `tables/background-reskins.json` (schema `background-reskins/0.1.0`, `entries[]`) + `tables/background-reskins.version.json`, copied together from `/workspace/dcc-lore/tables/` (Lore builds them with `tools/background_reskin_build.py`, checks them with `tools/background_reskin_check.py`). v0.1.1, 32 entries, copied into `tables/`. **Caleb approved v0.1.1 (sha256 5731a0536814..., 2026-10-04); `create.background_reskin` is TRUE in `sessions/session.json`.** Rollback: `python3 tools/background_reskins.py --disable` (or set the flag false/remove it); config only, no restart for the tables. Override path `BACKGROUND_RESKINS_PATH`.
- **Entry:** `id`, `kind` (`background` | `choice`), `parent_id` (`origin-feat` | `background-asi` | `background-kit` for a choice), `srd_name`, `display_name`, `combined_label` (**"Our Name (5e Name)"**, shown as written), `chargen_value` (the exact chargen-5e.json string), `flavor`; optional `label_name` (the short 5e name used in the label when `srd_name` has parentheses, e.g. "Magic Initiate, Cleric") and `chargen_job`. Ids: background = lower-cased key (`acolyte`), `feat-<origin feat>` (12), `asi-2-1`, `asi-1-1-1`, `package-a`, `package-b` (one shared pair for all backgrounds). 16 + 12 + 2 + 2 = 32 required.
- **Switch:** the names show only when `create.background_reskin` is exactly `true` in the session's `session.json` (default OFF). `python3 tools/background_reskins.py --enable [--session ID]` / `--disable` writes that flag (config only; no register; the tables are read by mtime, the bridge CODE needs one restart once). With the flag off, no file or a missing entry, S7 shows exactly the current text.
- **Where it shows:** S7 background picker and heading (plus its flavor line), the +2/+1 and +1/+1/+1 choices (`Our Name (+2 / +1): +2 INT / +1 WIS`, rules text kept), the Human extra Origin feat select, and the S10 background package select (`Our Name (Package A) - 8 GP left over`). Not changed: S1, S16/S17 text, the sheet, commit.js, state.json, the ledger.
- **Check:** `python3 tools/background_reskins.py --ids` (the 32 required ids), `python3 tools/background_reskins.py --strict` (the tables/ copy: sha256 vs the version file, structure, exact `chargen_value`/`srd_name`/`label_name` match, no nested parentheses, 5e names only; exit 1 on a missing id; "ABSENT", exit 0 when not in place), `--path /workspace/dcc-lore/tables/background-reskins.json --strict` to check Lore's file before copying, `--json`. Tests: `tools/tests/test_background_reskins.py`, bridge `test/bgnames.test.js` (fixtures with placeholder names, plus Lore's real file in a sandbox copy).
- **Drop-in of a new Lore version:** `python3 tools/background_reskins.py --path /workspace/dcc-lore/tables/background-reskins.json --strict`, then copy `background-reskins.json` and `background-reskins.version.json` together into `tables/` and re-run `--strict`. No restart for the tables, no register.
- **More screens later:** the bridge loads every display table through one registry (`src/create/layers.js`: id, file, flag `create.<x>_reskin`, string overrides by screen + id with fallback to the current text); a new Lore table is one registered layer plus an entry in this README and its own coverage tool.

## Discord channel layout (guild 1556163673469222942)
Categories: **GM/Voice** (`#gm-voice` id 1556163836879568946, formerly #dcc_mouth; `#table-transcript` id 1556163778788462602, formerly #dcc_ears), **Create** (`#create` id 1556436391255212073, private: players, DCC AI GM and Dungeon System AI - Earth (formerly DCC Ears) only; players run `/create` there and every reply is ephemeral), **Crawler Sheets** (read-only for players), plus the old Text Channels (`#general`) and Voice Channels. Only the names and parents changed; the bridge and the tools use channel IDs. `discord_gm.py read` reads the transcript channel. Who can see `#create`: the two player accounts by user-level overwrite, plus the role `new role` (id 1556406404267507802): give a new player that role in Discord (the GM bot cannot assign roles) and they can use `#create`.

### Create screens reskins (the later /create screens)
Lore's display text for S3-S17 (buttons, labels, hints, help, dialogs, notices, errors): `tables/create-screens-reskins.json` (schema `create-screens-reskins/0.1.0`, 192 rows) + `tables/create-screens-reskins.version.json` (sha256, and the sha of the companion `tables/create-flow-lines.proposed.json`). DISPLAY ONLY: ids, state.json, the ledger, amounts, package values and the rules never change; "credits" for GP is wording only.
- **Switch:** shown only while `create.screens_reskin` is exactly `true` in the session's `session.json`. The same flag merges the proposed v0.1.2 flow lines over `create-flow-lines.json` (placeholders and rule numbers must survive, else the current line stays). `create-flow-lines.json` is never overwritten.
- **Safety:** a row applies only if its `old` still matches the bridge's current text, every `{placeholder}` is supplied and the rule numbers survive; otherwise the plain text shows.
- **Rollback (instant, no restart):** `python3 tools/create_screens_reskins.py --disable` (`--enable` turns it on; `--session ID` for a non-alpha session).
- **Check:** `python3 tools/create_screens_reskins.py [--path FILE] [--strict]` (hash, companion sha, placeholders, numbers, label rule, lengths); `--source-map` lists rows the bridge does not wire; `--ids` lists every row.
- **Drop-in of a new Lore version (e.g. 0.1.2):** copy the json and its version file together into `tables/`, run the check; the bridge reloads by file mtime, no restart.

**Money words (2026-10-04, Syndicate ruling: 1 credit = 1 GP, 1 cp = 0.01 credit).** `/create` shows only "credits" (package labels, `Credits: N from options`, price lists, the S10 menus/help/intro line, `Party`-style errors that said gold/cash) through `src/create/money.js` (bridge, needs the restart), whatever the screens flag says. DISPLAY ONLY: price math, totals, ledger values, package values, ids and the `{gp}` placeholder keep their integer values; decimals (50 cp = 0.5 credit, singular for 1 or less) are formatting at the last step and never summed. `python3 tools/create_screens_reskins.py --money-words` lists Lore text that still says GP/cp/gold/cash (report only; Lore's tables are not edited). The stored ledger reason for the gold option ("Starting credits: ... gold option") is unchanged on purpose.
- **plain_on:** a row whose `plain_on` lists S1, S2, S13 or comfort_only shows its old text on that view.

## Repo safety check (git export)
`python3 tools/check_repo_safe.py` (default `--staged`) fails if a staged path is in the secret GM notes folder or under `sessions/`, is `credit-ledger*`, `.env*`, a log, `node_modules/` or a key file, or if staged content matches a secret shape (Discord bot token, Discord webhook URL, `GM_WEBHOOK_*=value`, API-key-like assignments, OpenAI/Google/GitHub/Slack/AWS keys, private-key blocks). `--tree DIR` scans a directory; `--strict` also fails on bare `GM_WEBHOOK` name mentions. It prints path, line and pattern type only, never the matched text. `sh tools/install_hooks.sh` installs `tools/hooks/pre-commit` into a clone. Tests: `tests/test_check_repo_safe.py`.
