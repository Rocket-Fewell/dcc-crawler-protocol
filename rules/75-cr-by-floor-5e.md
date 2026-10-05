# CR-by-Floor Encounter Difficulty Compendium (5e 2024)
Owner: Syndicate | Status: **DRAFT** | Version: 0.2.0 | Updated: 2026-10-05
Summary: Per-floor expected party level, budgeted CR/XP bands and Continuum tone notes for Floors 1–18. A GM/Encounter Bot companion to `rules/70-encounter-budget-5e.json`. Numbers come from rules/70; Continuum tone from the floor bible and campaign narrative. No species invented here.
Depends on: `rules/70-encounter-budget-5e.json` **v0.2.0** (XP budgets, CR caps, days, flag lines; the only source the Encounter Bot cites for those numbers), `rules/10-core-rules-5e.md` **v0.2.19** (§2.2 level track, §4.5 box pacing, §8.3 CR targets), `floors/04-floor-bible.md` **v0.4** (titles, Continuum ladder, seeds; creative draft), `floors/00-campaign-narrative.md` **v0.3** (spine; wins on Continuum structure), `floors/f01/` Day pages (Floor 1 only). Decisions 026, 028, Q-001 (clocks and missed-collapse death); decision 033 (F3/F9 double level bumps: arrive F4 at 5, F10 at 12, F18 at 20).

> **Status:** DRAFT v0.2.0 (re-cut for decision 033). Budgets are **guidelines** (rules/70 authority note; Caleb 2026-10-04: the GM may adapt). Nothing here invents creatures, species Offers or Floor 2+ encounter lists.
> **Project:** *Crawler Protocol: Season Zero* — original fan RPG inspired by *Dungeon Crawler Carl*. Private play only.
> **Address:** players are always **Crawlers**. Spelling: **saferoom**.
> **Precedence:** core and decisions win on rules; campaign narrative wins on Continuum structure; rules/70 wins on XP/CR/credit numbers; this file only indexes and explains them.

---

## 0. How to read this

| Column / tag | Meaning |
|---|---|
| **Arrive / leave level** | Standard track (core v0.2.19 §2.2, decision 033): arrive Floor N at level **N** on F1–3, **N+1** on F4–9, **N+2** on F10–18; leave at arrive+1. F3 and F9 end bosses grant +1 and the normal descent/onboarding +1 still fires (F4 at 5, F10 at 12). F18 arrives at the level-20 cap (finale 19–20 levels removed). Floor 1 split: pre–Green Room at L1, boss at L2 (rules/70 `floors.1.level`). |
| **Budget level** | The party level used for SRD XP budgets and CR caps on that floor (= arrive level). |
| **core §8.3 row** | core §8.3 is still keyed by floor with a party-level column from the old N/N+1 track; rules/70 v0.2.0 uses the row whose **party level matches** the arrive level (core §8.3's slow-burn rule; levels 19–20 use row 18). |
| **Tier** | trivial / standard / hard / boss (rules/70 `tiers`). F1 maps half-Low / Low / Moderate / High; F2+ maps Low / Moderate / High / High. |
| **CR caps (4 Crawlers)** | Lead-creature CR ceiling for a 4-Crawler party (rules/70 `floors.N.tiers.*.cr_caps.4`). Caps for 2 and 3 Crawlers are in the JSON. |
| **XP budget (4 Crawlers)** | Total XP envelope for one encounter of that tier (rules/70). Daily and floor ceilings are also in the JSON. |
| **Days** | Floor clock. F1–3 authoritative (decision 026); F4–6 house rule (Q-001); F7+ placeholder held at 30 in rules/70's growth curve (ASSUMED). |
| **Flag line** | Credits per Crawler per floor at which the Accountant flags (never blocks). Source of truth: rules/70 `flag_line_by_floor`. |
| **PLACEHOLDER** | Missing data; do not invent. Needs Encounter Bot, Caleb, or a later floor doc. |
| **Continuum** | Kingdom Continuum visits: F3 rural → F6 docks → F9 castle → F12 Olympus (bible §6; narrative wins on structure). |

**What this file does not do.** It does not list enemy species for Floors 2–18. It does not replace Day specs. It does not invent Offer timing or oddities (rules/30; waiting on Caleb).

---

## 1. Quick table (4-Crawler party)

| Floor | Title (bible) | Kind | Arrive→leave | Days | Enc. planned (mix T/S/H/B) | Trivial CR | Standard CR | Hard CR | Boss CR | Daily XP (typ.) | Flag line | Notes |
|---:|---|---|---|---:|---|---|---|---|---|---:|---:|---|
| 1 | Orientation Pit | Tutorial | 1→2 | **5** | 6 (1/3/1/1) | ≤1/4 | ≤1/4 | ≤1 | ≤1 (≤**2** at Z10) | 360 | 1,500 | Boss budgets at L2. Module: `floors/f01/`. |
| 2 | Soft Open | Unique | 2→3 | **10** | 15 (4/8/2/1) | ≤1/2 | ≤1/2 | ≤2 | ≤3 | 880 | 1,500 | No Continuum landmarks. PLACEHOLDER: no Day specs yet. |
| 3 | Continuum — Rural | Continuum | 3→4 | **20** | 30 (7/18/4/1) | ≤1 | ≤1 | ≤3 | ≤4 | 1,420 | 6,500 | First Gold band. Identity **tease only**. |
| 4 | The Knotline | Unique | 5→6 | **20** | 30 (7/18/4/1) | ≤2 | ≤2 | ≤4 | ≤8 | 4,500 | 6,500 | Tables usable from F4 (rules/20). |
| 5 | Bubble Farms | Unique | 6→7 | **25** | 38 (9/22/6/1) | ≤2 | ≤2 | ≤6 | ≤9 | 5,952 | 9,000 | Credit multiplier ×5 begins (cash/R1/fees). |
| 6 | Continuum — Docks | Continuum | 7→8 | **30** | 45 (11/26/7/1) | ≤3 | ≤3 | ≤6 | ≤10 | 7,420 | 13,500 | Hunters; still no Platinum. |
| 7 | Greenlight Gauntlet | Unique | 8→9 | *30†* | PLACEHOLDER | mob 2–3 | — | elite 6–7 | boss 10–11 | PLACEHOLDER | 13,500 | core §8.3 ranges only. |
| 8 | Remnant Parade | Unique | 9→10 | *30†* | PLACEHOLDER | 3–4 | — | 7–8 | 11–12 | PLACEHOLDER | 13,500 | Last pre-Platinum floor. |
| 9 | Continuum — Castle | Continuum | 10→11 | *30†* | PLACEHOLDER | 3–5 | — | 8–9 | 12–13 | PLACEHOLDER | 65,500 | **Platinum unlocks** (core §4.5). |
| 10 | Last Heat Standing | Unique | 12→13 | *30†* | PLACEHOLDER | 4–6 | — | 10–11 | 14–16 | PLACEHOLDER | 79,000 | Multiplier ×20. |
| 11 | Ratings Jubilee | Unique | 13→14 | *30†* | PLACEHOLDER | 5–6 | — | 11–12 | 15–16 | PLACEHOLDER | 79,000 | Spectacle; not Continuum grid. |
| 12 | Continuum — Olympus | Continuum | 14→15 | *30†* | PLACEHOLDER | 5–7 | — | 12–13 | 16–17 | PLACEHOLDER | 79,000 | Last Continuum visit. |
| 13 | Ledger Depths | Unique | 15→16 | *30†* | PLACEHOLDER | 6–8 | — | 13–14 | 17–19 | PLACEHOLDER | 308,500 | Legendary boxes begin (0.5 / Crawler). |
| 14 | Continuity Auction | Unique | 16→17 | *30†* | PLACEHOLDER | 6–8 | — | 14–15 | 18–20 | PLACEHOLDER | 308,500 | Legendary 0.5 / Crawler. |
| 15 | Ash Choir | Unique | 17→18 | *30†* | PLACEHOLDER | 7–9 | — | 15–16 | 19–21 | PLACEHOLDER | 263,500 | Legendary 0.25 / Crawler; mult ×50. Flag dip intentional. |
| 16 | Fracture Gallery | Unique | 18→19 | *30†* | PLACEHOLDER | 8–10 | — | 16–18 | 21–24 | PLACEHOLDER | 263,500 | |
| 17 | Rigging Catwalk | Unique | 19→20 | *30†* | PLACEHOLDER | 8–10 | — | 16–18 | 21–24 | PLACEHOLDER | 263,500 | |
| 18 | Cage Bottom | Endings | 20→20 (cap) | *30†* | PLACEHOLDER | 8–10 | — | 16–18 | 21–24 | PLACEHOLDER | 263,500 | Spine payoffs. |

† Days for F7–18 are **ASSUMED** in rules/70's growth curve (held at F6 = 30 so floors never get shorter). Decision 026 only says later floors grow longer. Confirm with Caleb (rules/70 Q2 follow-up).

For Floors 7–18 the "Trivial / Hard / Boss" columns above are **core §8.3** mob / elite / boss ranges (row matched by party level, decision 033) from rules/70 `floors_7_18` (not yet turned into trivial/standard/hard/boss CR caps the way F1–6 are). Encounter Bot must derive caps with the formula in `floors_7_18.steps` when those floors are written.

---

## 2. Method (rules/70, not reinvented)

1. **Level = arrive level** on the standard track (core v0.2.19 §2.2, decision 033): N on F1–3, N+1 on F4–9, N+2 on F10–18 (F18 = 20, cap), except Floor 1's L1→L2 split at the Green Room / boss. The core §8.3 CR range is the row whose party level matches (levels 19–20 use row 18).
2. **Tier XP budget** = SRD 2024 per-character Low/Moderate/High at the budget level × party size (rules/70). F1 uses a half-Low trivial band; F2+ uses Low for trivial.
3. **CR cap** = min(core §8.3 upper bound for the tier, highest CR whose XP ≤ lead_share × tier budget); lead_share = 0.9 for boss, 1.0 otherwise (rules/70 A1 / `floors_7_18.steps`).
4. **Encounter count (F2+)** = round(days × 1.5); mix ≈ boss 1, hard 15% of the rest (min 1), trivial 25%, standard = remainder (rules/70 A3). Floor 1 is the module's fixed list (4–8 fights; core 10.3), not that formula.
5. **Credits / boxes:** flag lines and box odds live in rules/70; this file only points. Legendary cap = **2 per Crawler** (core §4.5); Story Boxes (F1–2) are a separate track outside that cap and outside the Legendary pacing table (rules/70 `story_boxes_note`).
6. **Pick creatures from the SRD** (or already-filed house lists). Reskin (core §8.1). **Do not invent species** here.

Party sizes supported: 2, 3, 4. Credits per Crawler stay flat; XP budgets and enemy counts scale (rules/70 `party_sizes`).

---

## 3. Floor pages

### Floor 1 — The Orientation Pit *(tutorial)*

| Field | Value | Source |
|---|---|---|
| Arrive / leave | L1 → L2 | core §2.2; rules/70 `floors.1.level` |
| Budget level | L1 before Z9 Green Room; **L2 for Z10 boss** | rules/70; overview rule 3 |
| Days | **5** (authoritative) | decision 026 |
| Encounters | 6 planned: Z2, Z5, Z7 standard; Z8 hard; wandering Ceiling Ticks trivial (max 2); Z10 boss. Plus conditional Day 2–4 house fights (`d02_02`, `d03_02`, `d03_03`, `d04_03`) | rules/70 `fixed_encounters`; `floors/f01/` |
| Daily XP (4 Crawlers) | **360** typical | rules/70 |
| Flag line | **1,500** | rules/70 |

**CR caps / XP budgets (4 Crawlers)**

| Tier | CR cap @ L1 | XP @ L1 | CR cap @ L2 (boss day) | XP @ L2 |
|---|---|---:|---|---:|
| trivial | 1/4 | 100 | 1/4 | 200 |
| standard | 1/4 | 200 | 1/4 | 400 |
| hard | 1 | 300 | 1 | 600 |
| boss | 1 | 400 | **2** | **800** |

**Filed SRD creatures (do not expand inventively):** giant rat (CR 1/8), skeleton (1/4), goblin warrior (1/4), goblin minion (1/8), animated armor (1), animated flying sword (1/4), stirge (1/8), ogre (2), bugbear warrior (1). Counts and fit: rules/70 `floors.1.fixed_encounters.*`. Day pages: `floors/f01/day-01.md` … `day-05.md`.

**Tone (bible):** Concrete corridors, vending gore, cheerful UI over corpses. Teach the System; warn about collapse on Days 1, 4 and 5. Missed collapse = death (no Reprieve coverage for collapse). Floor 1 Reprieve still covers other tutorial deaths once per Crawler.

**Credits note:** Detour Tax = missed Stairwell key only (75 / Crawler). Rest without saferoom, key bribe, Zone S door: rules/70 `floors.1.prices`.

**Needs:** nothing for CR math (filed). Encounter Bot owns Day specs and must keep the budget pin current.

---

### Floor 2 — Soft Open *(unique)*

| Field | Value | Source |
|---|---|---|
| Arrive / leave | L2 → L3 | core §2.2 |
| Budget level | 2 | rules/70 |
| Days | **10** | decision 026 |
| Encounters (formula) | 15 (4 trivial / 8 standard / 2 hard / 1 boss) | rules/70 |
| Daily XP (4) | **880** | rules/70 |
| Flag line | **1,500** | rules/70 |

**CR caps / XP (4 Crawlers, L2)**

| Tier | CR cap | XP budget |
|---|---|---:|
| trivial | 1/2 | 400 |
| standard | 1/2 | 600 |
| hard | 2 | 800 |
| boss | 3 | 800 |

**Tone (bible):** Rec-room aesthetics over killboxes; first recurring NPCs; traps that teach attention. **No Kingdom Continuum landmarks.** Story Boxes still allowed (F1–2 exception).

**PLACEHOLDER — needs Encounter Bot / Syndicate:** entire Day-spec set (`floors/f02/`), enemy lists, zone map, saferoom tolls (prices from rules/70 when set). Lore: Floor 2 canon table stays in reserve until Floor 1 is played (Q-002 HOLD).

---

### Floor 3 — Kingdom Continuum *(Rural)* — Continuum visit 1/4

| Field | Value | Source |
|---|---|---|
| Arrive / leave | L3 → L4 | core §2.2 |
| Budget level | 3 | rules/70 |
| Days | **20** | Caleb / decision 026 |
| Encounters | 30 (7/18/4/1) | rules/70 |
| Daily XP (4) | **1,420** | rules/70 |
| Flag line | **6,500** | rules/70 |

**CR caps / XP (4 Crawlers, L3):** trivial ≤1 (600 XP); standard ≤1 (900); hard ≤3 (1,600); boss ≤4 (1,600).

**Continuum tone (bible §6 / narrative):** Dirt roads, harvest markets, Wellspring / Millroad / Low Chapel bones. Civilians matter. Broadcast Name begins as gossip. Social play unlocked. **Identity: tease only — do not invent Offer timing, rebuilds or oddities** (waiting on Caleb; rules/30). Gold boxes available (core §4.5 F3–5); still no Platinum. Open with recognition of *being somewhere real*.

**PLACEHOLDER:** `floors/f03/` module, Continuum NPC ledger, militia/settlement encounter packs. Encounter Bot when Caleb marks the bible.

---

### Floor 4 — The Knotline *(unique)*

| Field | Value | Source |
|---|---|---|
| Arrive / leave | **L5 → L6** (F3 boss +1, then F4 onboarding +1; decision 033) | core §2.2 |
| Budget level | 5 (core §8.3 row 5) | rules/70 |
| Days | **20** (house rule Q-001) | |
| Encounters | 30 (7/18/4/1) | |
| Daily XP (4) | **4,500** | |
| Flag line | **6,500** | |

**CR caps / XP (4, L5):** trivial ≤2 (2,000); standard ≤2 (3,000); hard ≤4 (4,400); boss ≤8 (4,400).

**Tone (bible):** Non-Euclidean transit; switching yards; schedules that lie. Puzzle floor with teeth. No Continuum landmarks on-stage except as rumors.

**Also:** crafting tables become usable (rules/20; unusable until F4). Workstation prices follow the F3+ schedule (decision 030).

**PLACEHOLDER:** entire Floor 4 module.

---

### Floor 5 — Bubble Farms *(unique)*

| Field | Value | Source |
|---|---|---|
| Arrive / leave | **L6 → L7** | core §2.2 |
| Budget level | 6 (core §8.3 row 6) | rules/70 |
| Days | **25** (Q-001) | |
| Encounters | 38 (9/22/6/1) | |
| Daily XP (4) | **5,952** | |
| Flag line | **9,000** | |

**CR caps / XP (4, L6):** trivial ≤2 (2,400); standard ≤2 (4,000); hard ≤6 (5,600); boss ≤9 (5,600).

**Tone (bible):** Greenhouse horror and wonder; pocket biomes under glass; soft countdown separate from floor collapse. Credit multiplier ×5 begins for encounter credits, R1 and fees (box pulls do not take it).

**PLACEHOLDER:** entire Floor 5 module; bubble-rupture local disaster rules.

---

### Floor 6 — Kingdom Continuum *(Outskirts & Docks)* — Continuum visit 2/4

| Field | Value | Source |
|---|---|---|
| Arrive / leave | **L7 → L8** | core §2.2 |
| Budget level | 7 (core §8.3 row 7) | rules/70 |
| Days | **30** (Q-001) | |
| Encounters | 45 (11/26/7/1) | |
| Daily XP (4) | **7,420** | |
| Flag line | **13,500** | |

**CR caps / XP (4, L7):** trivial ≤3 (3,000); standard ≤3 (5,200); hard ≤6 (6,800); boss ≤10 (6,800).

**Continuum tone:** Same civilization at the waterline. Ports, warehouses, customs, sponsor skyboxes. **Hunters** as licensed outsiders. Rural debts come due on the pier. Recognition first, then frontier pressure. Still **no Platinum** (F9+).

**PLACEHOLDER:** Floor 6 module; hunter stat blocks (SRD picks only until a filed list exists); sponsor booth economy.

---

### Floors 7–8 — Unique pressure *(Greenlight Gauntlet; Remnant Parade)*

| Field | F7 | F8 |
|---|---|---|
| Arrive → leave | 8→9 | 9→10 |
| Budget level | 8 | 9 |
| Days | PLACEHOLDER (growth curve uses 30) | same |
| core §8.3 CR (row 8 / row 9) | mob 2–3; elite 6–7; boss 10–11 | mob 3–4; elite 7–8; boss 11–12 |
| Per-Crawler XP bands | L 1,000 / M 1,700 / H 2,100 | L 1,300 / M 2,000 / H 2,600 |
| Flag line | 13,500 | 13,500 |
| Credit mult | ×5 | ×5 |

**Tone:** F7 timed race / maze; F8 memory-echo combat and identity as weapon (bible). Last floors before Platinum.

**PLACEHOLDER:** days (Caleb); encounter mix and CR caps derived by Encounter Bot from `floors_7_18.steps`; full modules.

---

### Floor 9 — Kingdom Continuum *(Upper City & Castle)* — Continuum visit 3/4

| Field | Value |
|---|---|
| Arrive / leave | 10→11 (end boss +1 → 11; F10 onboarding +1 → arrive F10 at 12; decision 033) |
| Budget level | 10 |
| Days | PLACEHOLDER (growth curve 30) |
| core §8.3 (row 10) | mob 3–5; elite 8–9; boss 12–13 |
| Per-Crawler XP | L 1,600 / M 2,300 / H 3,100 |
| Flag line | **65,500** |
| Credit mult | ×5 |

**Continuum tone:** Boulevards, guild halls, noble houses, the **castle**. Broadcast Name is a political object. Mandates, factions, diplomacy/sabotage. Dock sponsors have court seats; rural shrines are state religion. **Platinum boxes unlock** (core §4.5 / bible locked ruling).

**PLACEHOLDER:** days; module; faction encounter packs; Platinum boss-box procedure (rules/40 when F9+ decks exist).

---

### Floors 10–11 — Unique spectacle *(Last Heat Standing; Ratings Jubilee)*

| Field | F10 | F11 |
|---|---|---|
| Level band | 12→13 | 13→14 |
| core §8.3 (row 12 / row 13) | mob 4–6; elite 10–11; boss 14–16 | mob 5–6; elite 11–12; boss 15–16 |
| Per-Crawler XP | 2,200 / 3,700 / 4,700 | 2,600 / 4,200 / 5,400 |
| Flag line | 79,000 | 79,000 |
| Credit mult | **×20** | ×20 |

**Tone:** Elimination heats / garage culture (F10); parade and arena for viewers, not Continuum grid (F11). Named opponents; VIP tickets.

**PLACEHOLDER:** days; modules; named-opponent guidelines for Encounter Bot.

---

### Floor 12 — Kingdom Continuum *(Olympus / Spirit)* — Continuum visit 4/4 (last)

| Field | Value |
|---|---|
| Arrive / leave | 14→15 |
| Budget level | 14 |
| Days | PLACEHOLDER (growth curve 30) |
| core §8.3 (row 14) | mob 5–7; elite 12–13; boss 16–17 |
| Per-Crawler XP | L 2,900 / M 4,900 / H 6,200 |
| Flag line | 79,000 |
| Credit mult | ×20 |

**Continuum tone:** Same world's god-tier. Storm thrones, chapel gods made flesh, Millroad as a sacred path among stars. Castle politics become divine politics. Throne Vow; Benefactor meets pantheon. Landmark bones from F3/F6/F9 scale one last time. **Not** a random heaven — continuation of rural → docks → castle.

**PLACEHOLDER:** days; module; deity-patronage mechanical hooks (do not invent pantheon species).

---

### Floors 13–17 — Strip the lie *(Ledger Depths; Continuity Auction; Ash Choir; Fracture Gallery; Rigging Catwalk)*

| Floor | Level (arrive→leave) | core §8.3 mob / elite / boss (row) | Per-Crawler L/M/H | Flag | Mult | Legendary / Crawler (core §4.5 mid) |
|---:|---|---|---|---:|---:|---|
| 13 | 15→16 | 6–8 / 13–14 / 17–19 (row 15) | 3,300 / 5,400 / 7,800 | 308,500 | ×20 | **0.5** |
| 14 | 16→17 | 6–8 / 14–15 / 18–20 (row 16) | 3,800 / 6,100 / 9,800 | 308,500 | ×20 | **0.5** |
| 15 | 17→18 | 7–9 / 15–16 / 19–21 (row 17) | 4,500 / 7,200 / 11,700 | **263,500** | **×50** | **0.25** |
| 16 | 18→19 | 8–10 / 16–18 / 21–24 (row 18) | 5,000 / 8,700 / 14,200 | 263,500 | ×50 | 0.25 |
| 17 | 19→20 | 8–10 / 16–18 / 21–24 (row 18) | 5,500 / 10,700 / 17,200 | 263,500 | ×50 | 0.25 |

The F15 flag-line dip is **intentional** (Legendary 0.5 on F13–14 vs 0.25 on F15–18 keeps each Crawler's total at 2; rules/70 v0.1.11). Flag lines need not be monotonic.

**Tone (bible one-liners):** ledgers and debts made flesh; auctions of continuity; ash and choir; mirrors/fracture; the crawl's rigging made walkable. Strip the lie behind the world.

**PLACEHOLDER:** all modules; days; derived CR caps; F13+ loot decks (none exist yet — Gold/Platinum/Legendary values in the growth curve are placeholders).

---

### Floor 18 — Cage Bottom *(endings)*

| Field | Value |
|---|---|
| Arrive / leave | **20 → 20** (level cap on arrival; decision 033 removed the finale 19–20 levels; replacement finale reward is an open follow-up) |
| Budget level | 20 |
| Days | PLACEHOLDER (growth curve 30) |
| core §8.3 (row 18, party level 18–20) | mob 8–10; elite 16–18; boss 21–24 |
| Per-Crawler XP | L 6,400 / M 13,200 / H 22,000 |
| Flag line | 263,500 |
| Credit mult | ×50 |
| Legendary / Crawler | 0.25 |

**Tone:** Endings. All spine payoffs. Not another Continuum visit unless an ending reprises it on purpose (bible).

**PLACEHOLDER:** ending branches; final boss structure; whether days stay at 30 or lengthen (Caleb); replacement finale reward for the removed 19–20 levels (decision 033 open item; GM/Syndicate).

**Note (decision 033):** Floors 16, 17 and 18 (arrive L18, L19, L20) all read core §8.3 row 18, so their CR ranges are the same; the XP budgets still rise with level.

---

## 4. Continuum difficulty notes (F3 / F6 / F9 / F12)

These floors share one civilization. Difficulty should rise with **social and spiritual altitude**, not with a new bestiary each time.

| Visit | Floor | Pressure that is *not* just higher CR |
|---|---|---|
| 1 Rural | 3 | Civilians as stakes; militia call-ups; fame that sticks. Hard fights are rare; standard and social scenes carry the day. |
| 2 Docks | 6 | Hunters (licensed PvE pressure) + sponsor riders. Same faces under worse weather. Hard CR up to 6, boss to 10 (L7, decision 033). |
| 3 Castle | 9 | Politics as dungeon: mandates, factions, etiquette traps. Platinum enters the reward track. Boss CR band 12–13 (L10). |
| 4 Olympus | 12 | Divine patronage and vow-fire. Landmark bones become myth. Boss CR band 16–17 (L14). Last Continuum visit. |

When writing Continuum encounters, prefer **reskinned SRD** creatures and recurring Continuum NPCs over new species. Species Offer timing remains **waiting on Caleb**.

---

## 5. Open work (Encounter Bot / Caleb / Syndicate)

| Who | What |
|---|---|
| **Encounter Bot** | Keep Day 1–5 budget pins on rules/70 v0.2.0+ (F1 sans-pin hashes unchanged by decision 033); write Floor 2+ Day specs when floor docs exist; derive F7–18 trivial/standard/hard/boss CR caps from `floors_7_18.steps` (not done in this draft); re-pin after every rules/70 bump. |
| **Caleb** | Confirm F7+ day counts (rules/70 Q2 follow-up; growth curve holds at 30); mark floor bible v0.4; species/class Offer timing (rules/30); any veto on Continuum working titles. |
| **Syndicate / Lore** | Floor 2+ modules (`floors/fNN/`); Continuum NPC ledger; hunter and faction packs from SRD only until filed; F3+ loot decks (growth-curve Gold+ values are placeholders). |
| **Accountant** | v0.2.0 re-cut for decision 033 done (levels, XP, CR only; credits, boxes, flag lines unchanged because they are keyed by floor). Re-audit if F7+ days or mix change. |
| **This file** | Expand per-floor pages when modules land; add 2- and 3-Crawler CR columns if Encounter Bot wants them in-line (already in JSON). |

---

## 6. Changelog

| Version | Date | Notes |
|---|---|---|
| 0.2.0 | 2026-10-05 | Accountant re-cut for decision 033 / core v0.2.19: arrive levels F4–9 = N+1, F10–18 = N+2 (F4 at 5, F10 at 12, F18 at 20 cap, finale 19–20 removed). F4–F6 CR caps, XP and daily XP from rules/70 v0.2.0 (budget levels 5/6/7); F7–F18 core §8.3 ranges and per-Crawler XP shifted to the row/level matching the arrive level (levels 19–20 use row 18). F1–F3, days, flag lines, credits and boxes unchanged. |
| 0.1.0 | 2026-10-05 | First DRAFT. Indexes rules/70 v0.1.11 CR/XP/days/flag lines for F1–18; Continuum tone from floor bible v0.4 and narrative v0.3; Floor 1 cites only filed SRD creatures. No species invented. Placeholders marked for F2+ modules and F7+ day counts. |

