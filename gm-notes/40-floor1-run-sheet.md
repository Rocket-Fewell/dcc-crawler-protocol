# Floor 1 Run Sheet
Owner: DCC AI GM | Status: draft | Version: 0.2 | Updated: 2026-10-05
Summary: At-the-table cheat sheet for Floor 1 (5 days): opener and death warning, clock, per-day table, pacing, carry-on tracker, ledger commands. Cites only numbers from the files named in each section. [SLOT] = missing, fill in or ask Caleb. Players are Crawlers, always. One live campaign at a time (`sessions/active-session.json`); tools take `--session` / `DCC_SESSION`.

## 0. Campaign
- **Live default (2026-10-08):** `s2` (Season 2) — cold open, fresh Floor 1 Day 1 world, max 4 Crawlers; Raithen (Hornn) carried over from s1 with 100 credits. `s1` (2026-10-05 to 2026-10-07, party wipe) is the archive. Confirm with Architect before spending.
- **Parked save:** `alpha` — Horn (Wizard / Hornn) and Bone Wifebeater (Barbarian / Trailer Park Moses) in Z6 Break Room; Reprieves spent; credits Bone 127 / Horn 75. Resume only if Caleb switches the live campaign back.

## 1. Opening
### A. New campaign / cold open (`s2`; was `s1`) — enc-d01-06
- **Where:** surface glowing stairwell → Floor 1 Intake (Z0) → atrium (Z1) → tutorial zones → Z6 Break Room.
- **Clock:** floor hour 0 when surface entrances open (horn / beams). One-hour Native window is hours 0–1.
- **Run first:** `python3 tools/encounter_text.py --day 1 --encounter enc-d01-06` (pipe player text to `discord_gm.py say`). Hand-tag if a wink still lands as System until Architect narrows SYSTEM_KINDS.
- **Dry [SYSTEM]:** horn, one-hour window, Native vs Crawler, registration, booth open. **[GM]:** crawler color, jokes, atrium jaw beat.
- **Collapse warning:** after Floor 1 schedule is announced (Break Room / clock-on), not during the Native window. Tick F1 start then.

### B. Resume alpha (Z6) — enc-d01-01
- **Where:** Z6 Break Room (Saferoom A). Horn + Bone Wifebeater, L1, Reprieves spent — a death now is real. Floor hour: [SLOT].
- **Run first:** enc-d01-01 Clock On: Break Room Briefing. Welcome Box only if not yet held.

### Voice tags (decision 032)
- **[SYSTEM]** dry only: clock, fees, registration, collapse, floor notices.
- **[GM]** snark, ACH banners + mock, loot-box callouts, every joke. Always re-tag `[GM]` after a System block.
- Flavor: soft guideline — punchy, no five-minute monologues; longer when the moment earns it.

### Required collapse warning (decision 026)
Say plainly, then in voice. Approved line:
> "Reach a stairwell before the collapse or you do not leave. This is not a toll. This is not a detour. This is the end."
- **Warn again:** Floor 1 start (after schedule is live), Day 4, Day 5. Tick: [ ] F1 start  [ ] Day 4  [ ] Day 5. Also before anyone descends.

## 2. Clock cheat sheet (decisions 026, 028; overview 2.6; rules/70 JSON v0.1.1)
- **Length:** 5 days. Day ends at the party's saferoom Long Rest, or at 24 in-game hours (System rolls it over). Lights-Out: every 8 h the Pit goes dark for 1 h; outside saferooms roll d6 every 30 min, 1-2 = Ceiling Ticks.
- **Rests:** up to 4 short-rest slots per day (CAP, 20 total), 1 Long Rest per day, Long Rests only in saferooms. Field rest = Short Rest only, 20 cr/Crawler (cap 60/floor), party 40 (2 Crawlers). No saferoom Long Rest ever ends or skips the collapse; the System cuts it short.
- **Collapse:** fixed, 24 in-game hours into Day 5 (hour 120 of the floor). NOTE: "24 h into Day 5" only equals hour 120 if every day was 24 h; keep a running floor-hour count.
- **Stairwell opens:** ~32 h in, early Day 2 (M-276). Z10 arena holds one (M-275). Real one is behind the stage (Z11). Z7 Big Green EXIT is bait. Zone S door leads to the service stairwell, which drops to Z11.
- **Early descent:** more than 6 h left = stasis until collapse (M-277), banks the achievement, ends that Crawler's floor, counts as reaching a stairwell. Last 6 h (hours 114-120, derived) = free descent. Each Crawler chooses. Stasis Crawler gets short sideline System scenes. GM may log an override.
- **Zones close (hooks and services vanish; route Z6, Z8, Z9, Z10, Z11 is never cut):** D1 none. D2 outer Z0-Z4 + 3b. D3 mid Z5, Z7, Z8 (Bruiser key gone). D4 Z6 Break Room and vendors lose service (terminal key gone). D5 only Z10, Z11, ZS + Z9.
- **Saferooms:** Z6 through Day 3 only. **Z9 Green Room is the only saferoom after Day 4 service loss** and stays open to the end.
- **Key ways to Zone S:** Bruiser's head (Z8, until D3), terminal bribe (Z6, until D4; 50/Crawler, 100 for 2), Mystery Key if GM picks it, Thieves' Tools or Athletics (25/Crawler forcing fee, 50 for 2; loud, Thudd and Ushers arrive 1 min later). **Missed key only** = Detour Tax 75/Crawler (150 for 2). Never for a missed collapse.
- **Potion of Healing at Snakk-Matic:** 50 cr, 2 in stock floor-wide.

## 3. Per-day table (day pages 01-05; Z = zone; counts for ushers/vermin = [SLOT] on pages)
| Day | Starts | MUST happen | CAN happen |
|---|---|---|---|
| 1 | stair / Z0→Z6 | Cold open (enc-d01-06) then tutorial zones → Break Room briefing + death warning; route declared; Long Rest in Z9; Day 2 preview | Terminal key buy; Z7 bait + Greeters + Back Office; Z8 Locker Room elite (Bruiser key); Ticks at Lights-Out; last-chance outer hooks; Welcome Box |
| 2 | Z9 | Morning notice: outer zones closed, stairwell open; if any Crawler reaches Z11, read stasis prompt to each Crawler separately | Zone S door (key, tools, force); look at the stage; Z6/Z7/Z8 loot before they close D3; early descent (stasis) |
| 3 | Z9 | Notice: mid zones closed, Bruiser key gone; Break Room still saferoom and terminal still sells | Last Call at Break Room (buy key, restock); Collapsing Hall with displaced rats/Ticks (Z8, counts [SLOT]); Stage Wings recon |
| 4 | Z9 | **Warning #2**; Break Room off service, terminal key gone, Z9 only saferoom; tell them about the free descent in the last 6 h | Field rest in the dark halls (Ticks); Ushers at the stage door ([SLOT] count); Green Room night shift |
| 5 | Z9 | **Warning #3** with {hours} left filled in; everyone reaches a stairwell before hour 120; read missed-floor line only if someone is still on the floor at the collapse | Dean Thudd (fight, Variant B at L1 or 2 Crawlers, or talk down); Zone S Toll Turnstile (key, tools, force or toll); free descent in last 6 h |

## 4. Table-pace tips
- Flavor: soft guideline (Caleb 2026-10-05) — punchy, no five-minute monologues; longer when the moment earns it. Long set pieces OK for boss / stage / cold open.
- Full quality stays: worldbuilding, interactivity, and the Crawlers' actions carry on. Short does not mean thin. Ask what they do, then react.
- Day pages have "Optional quick run" blocks (e.g. Break Room about 8 min). Optional safety net only, never the default.
- Announce items as `Our Name (5e Name)` with real mechanics. Announce every achievement: banner, one line, `Reward:` on its own line. Put boss headers and Reward lines on their own lines.
- Stalling: the clock is the pressure (System repeats day count, Lights-Out arrives). Do not push the party to spend the 4 rest slots.

## 5. Carry-on tracker (copy per session; plain notes, not written to state)
- Floor hour: ___ / 120   Day: ___   Session: ___   Warnings given: F1 [ ]  D4 [ ]  D5 [ ]
- Route declared: ___   Key way used: bruiser [ ] terminal [ ] mystery [ ] tools [ ] force [ ] tax [ ]   Key holder: ___
- Zones closed so far: D2 outer [ ]  D3 mid [ ]  D4 Break Room [ ]  Hooks left behind: ___
- Short rests used today: _/4   Long Rest taken in: ___   Field-rest fees paid (cap 60/Crawler): ___
- Wandering Ticks used: _/2 (state.json shows 1 used; Day 3 displaced Ticks count if used)   Potions left at vendor: _/2
- Achievements triggered (state first, do not re-grant; Vending Gore and Find a Lore Scrap are already on Bone): ___. Seeds: Slow Learner, Read the Fine Print, Last One Out, Detour Tax, Early Withdrawal, Hold Please (rewards in rules/70 JSON, GM may adapt). Boxes per Crawler this floor: soft 2-3.
- Loot taken from bodies (who, from whom, what, floor still standing y/n): ___ (Tanya Ruiz already looted per state.json)
- Credits vs audit line, per Crawler per floor (rules/70 JSON economy_audit): line 1,500. Floor 1 plan 666.1 all-in, 576.6 box-only. Counts: cash, R1 toasts, box credit_value, Story Box sale proceeds. Not counted: vendor spend, bribes, tolls, Story Box story_value.
  Snapshot from state.json before Session 2: Horn 75 cr, Bone 127 cr. Re-check live: `DCC_SESSION=alpha python3 tools/state.py loot totals`. Running: Horn ___  Bone ___ (flag, never block, at 1,500).
- Story Box: one per floor, hand-picked, deed text at award, opened only in a saferoom: awarded [ ] to ___.

## 6. Ledger commands for collapse deaths (tools/README.md, decision 028)
Prefix `DCC_SESSION=alpha`. Use `--dry-run` first. Order: loot-body first, then floor-lost.
1. `python3 tools/state.py loot-body DEAD SURVIVOR --reason "..." [--coins N|all] [--item NAME[=QTY]] [--all-items] --floor 1` (only while the floor still stands; two linked rows; refuses a body that is not Dead).
2. `python3 tools/state.py floor-lost CRAWLER --reason "..." --floor 1 [--mark-dead]` (one write-off row, balance to 0, inventory emptied; run AFTER looting; refuses NPCs/AI).
3. `python3 tools/state.py ledger verify`.
- NPCs and the AI go to stasis and lose nothing. Unopened Story Box is reclaimed on death. Credits, items, Story/Legendary items die with the floor.
- Gap to decide: loot-body needs a Dead body, but a collapse death happens after the floor ends. In practice loot-body only fits a Crawler who died EARLIER; a pure collapse death gets floor-lost alone.

## 7. Source conflicts to know about (which wins)
- rules/70 .md (v0.1.0) says audit line is F1+F2 combined and Detour Tax covers a missed collapse. Use the JSON (v0.1.1): per floor, missed key only.
- decision 026 item 2 ("hauled down", Exhaustion) is superseded by Caleb's 10:02 PM ruling in the same file.
- overview 11.3 pacing and day-01.md ("Z0-Z5 played in session one") disagree with state.json (ejected from Z3 to Z6; no sign Z4 Dale rescue or Z5 Mannequin Staff were run). Check sheets before closing outer hooks.
