# Core Book Items & Monsters — Status Inventory
Owner: DCC Lore | Status: draft | Version: 0.1 | Updated: 2026-10-05
Summary: Read-only inventory for the human Core Rulebook (Items + Monsters chapters). Counts from lore tables/catalogs and campaign floors/rules/loot decks. No campaign edits; sealed paths unread.

Audience: Core Book Author (Valtay) + Caleb. Date of scan: **2026-10-05 ~14:10 CT**.

---

## 0. Bottom line (for Caleb)

**Caleb’s “only Floor 1 mobs exist” is half-right for playable 5e, wrong for canon names.**

| Layer | Floor 1 | Floor 2 | Floors 3–7 |
|---|---|---|---|
| Canon name + notes (ledger-backed tables) | **Yes** — `tables/canon-floor-1.*` (46 mob entries) | **Yes** — `tables/canon-floor-2.*` (22 mob entries) | **No** dedicated canon-floor tables |
| Fan-wiki condensed lists (unverified) | Yes (in `catalog/bestiary-by-floor.md` + `catalog/floor-data.md`) | Yes | Thin name lists only |
| Playable 5e encounter stubs (SRD `srd_id` + house nameplate) | **Yes** — 10 unique nameplates across Days 1–5 | **No** (`rules/70` has budgets/XP only; no `fixed_encounters`) | **No** floors under `floors/f0N/`; no stubs |
| Full bestiary entry (5e stat block + book flavor) | **None anywhere** | **None** | **None** |

Items: a **complete mundane SRD reskin catalog** exists (191). A **player-facing magic-item / DCC-unique catalog for the Core Book does not** — only Floor 1 loot-deck cards + wiki condensed item lists.

---

## 1. Items

### 1.1 Mundane / chargen catalog (book-ready name + short snark)

| Path | Role |
|---|---|
| `/workspace/dcc-lore/tables/item-reskins.json` | Source of truth (v0.1.5) |
| `/workspace/dcc-lore/tables/item-reskins.md` | Human table |
| `/workspace/dcc-lore/tables/item-reskins.version.json` | Hash / history |
| `/workspace/dcc-campaign/tables/item-reskins.json` | Campaign mirror (same family) |

**Counts (191 total; every entry has a distinct `display_name` and a non-empty `snark`):**

| Category | Count | Reskin name | Flavor (`snark`) | Flavor quality |
|---|---:|---:|---:|---|
| weapon | 38 | 38 | 38 | Short snark (3–18 words, avg ~7). Nameplate-ready, **not** full chapter prose. |
| armor | 12 | 12 | 12 | same |
| shield | 1 | 1 | 1 | same |
| ammunition | 5 | 5 | 5 | same |
| focus | 14 | 14 | 14 | same |
| gear | 74 | 74 | 74 | same |
| pack | 7 | 7 | 7 | same |
| tool | 40 | 40 | 40 | same |

Also: **6** generic header ids (`resolve_to_variant: true`) and **2** non-SRD canon items (`heal-critter-potion`, `pet-carrier`). Meta explicitly: **magic items not covered** (`scope_not_covered`).

**Verdict for Core Book Items (mundane):** Ready to draft **name + one-line flavor** from this table. Not a substitute for longer “what it is / how it looks in the Crawl” paragraphs if Valtay wants encyclopedia depth.

### 1.2 Magic items, house items, Story Boxes, loot decks (Floor 1 only)

| Path | What | Counts |
|---|---|---|
| `/workspace/dcc-campaign/tables/loot-decks/*.json` | Live drawable cards (SoT) | **99** cards; all have `reskin_name` + `spoken_line` |
| `/workspace/dcc-lore/tables/loot-decks/` | Lore copies + empty ach deck stub | Same F01 decks + `ach-f01-orientation-pit.json` (no cards) |
| `/workspace/dcc-campaign/rules/40-loot-deck-spec-5e.md` | Deck schema / draw rules | Spec |
| `/workspace/dcc-campaign/rules/42-house-items-f01.md` | Final rules for 4 house items + Story Box cards | Cloak of Many Fashions; Pole of Collapsing; Mystery Key; Potion of Fire Breath; + Enhanced Pet Biscuit & story cards 0056–0060 |
| `/workspace/dcc-campaign/rules/45-story-boxes-5e.md` | Story Box system | Design + 5 worked patterns |
| `/workspace/dcc-lore/catalog/loot-boxes.md` | Wiki box-type catalog | **76** box-type rows (tiers/rules; **UNVERIFIED** wiki) |

**Loot deck card mix (99):** category Misc 45, Consumables 34, Credits 9, Armor 6, Weapons 3, Keys 2.  
**source_5e:** HOUSE 36, PHB 2024 36, SRD 5.2 24, DMG 2024 3.  
`spoken_line` avg ~16 words (nameplate / System line), book-ready as **short announce lines**, not encyclopedia entries.

**Story Boxes:** 10 cards in `f01-any-story-boxes.json` + rules in 42/45. Floor 1–2 Legendary one-offs only.

### 1.3 Wiki / canon item catalogs (research, not Core-Book-ready flavor)

| Path | Counts | Notes |
|---|---|---|
| `/workspace/dcc-lore/catalog/items.md` | **32** potions + **163** other items | Condensed wiki notes; header says **unverified against books** |
| `/workspace/dcc-lore/catalog/crafting-canon.md` | Crafting stations / coupons | Ledger-oriented, not player flavor prose |
| `/workspace/dcc-lore/catalog/upgrade-patches-canon.md` | Patches | same |

### 1.4 What’s missing (items)

1. **No Core-Book magic-item chapter corpus** beyond Floor 1 decks (99) + four house items. Hundreds of DCC-named enchanted/consumable entries in `catalog/items.md` lack reskin display names, SRD mapping, and book-ready flavor.
2. **Categories with no reskin table:** magic items, vehicles/mounts/tack, lifestyle/food (called out in item-reskins meta), potions beyond the two non-SRD pet items, upgrade patches, T’Ghee / celestial gear.
3. **Base SRD mundane:** essentially **covered** (191). No gap list of missing SRD mundane ids in the reskin table.
4. **Floors 2–7 loot decks:** do not exist (only `f01-*`).
5. **PHB 2024 / DMG 2024–sourced cards (39):** fine as table references for play; **do not paste non-SRD book text** into the Core Book — mechanics must stay paraphrased / SRD-safe (see blockers).

---

## 2. Monsters

### 2.1 Playable Floor 1 (encounter stubs → SRD)

Paths: `/workspace/dcc-campaign/floors/f01/day-0{1–5}.json` (+ `.md` / `.spec.json`), budgeted in `/workspace/dcc-campaign/rules/70-encounter-budget-5e.json` (`floors.1.fixed_encounters` only).

**10 unique combat nameplates** (house name + SRD id; no inlined 5e stat block — GM uses SRD):

| our_name | srd_id |
|---|---|
| Vent Rat (Giant Rat) | giant-rat |
| Mannequin Staff (Skeleton) | skeleton |
| Exit Greeter (Goblin Warrior) | goblin-warrior |
| Exit Greeter (Trainee) (Goblin Minion) | goblin-minion |
| Bruiser the Mascot (Unoccupied) (Animated Armor) | animated-armor |
| Lanyard Blade (Animated Flying Sword) | animated-flying-sword |
| Ceiling Tick (Stirge) | stirge |
| Usher (Skeleton) | skeleton |
| Dean Thudd, Head of Orientation (Ogre) | ogre |
| Dean Thudd (JV) (Bugbear Warrior) | bugbear-warrior |

These are **house / inspired** nameplates for the Orientation Pit, not the book’s Floor 1 goblin clan / Hoarder / Juicer roster.

### 2.2 Canon tables (name + notes; not stat blocks)

| Path | Mob entries | Tag mix |
|---|---:|---|
| `/workspace/dcc-lore/tables/canon-floor-1.json` (+ `.md`) | **46** | canon 35, inspired 9, unverified 2 |
| `/workspace/dcc-lore/tables/canon-floor-2.json` (+ `.md`) | **22** | canon 19, unverified 3 |

**Floor 1 canon examples:** Rat, Scatterers, Hoarder, Goblin family, Bad Llama, Rot Sticker, Troglodytes / Juicer, Ball of Swine / Tusklings, roster oddities (Chilly Goat, Bugaboo, etc.).  
**Floor 2 canon examples:** Krakaren Clone, Brindle Grub cycle, Danger Dingo / Kobolds / Ralph, Mind Horror, Rage Elemental, Death Watch roster. Gaps/backlog called out inside the Floor 2 JSON (`gaps`, `refinement_backlog`, `open_conflicts`).

### 2.3 Fan-wiki condensed bestiary (research only)

| Path | Content |
|---|---|
| `/workspace/dcc-lore/catalog/bestiary-by-floor.md` | Floor-grouped name tables; header **[UNVERIFIED – fan-wiki only]** |
| `/workspace/dcc-lore/catalog/bosses.md` | ~40 wiki boss rows (notes, not 5e blocks) |
| `/workspace/dcc-lore/catalog/floor-data.md` | Per-floor notable-mob name dumps (F1–18 wiki) |
| `/workspace/dcc-lore/sources/fanwiki/book{1–8}-bestiary.txt` | Raw scrapes |

**Approx. unique name rows in bestiary-by-floor (dedupe not perfect; wiki noise):** F1 mobs ~10 listed + bosses 3; F2 mobs ~12 + bosses 3; F3/4/5/6/8/11 sparse boss/mob name lists (often overlapping). **None** are full bestiary entries.

### 2.4 Planned vs missing Floors 3–7

| Floor | Campaign floor pack | Budget creatures | Canon-floor table | Wiki name list | Full bestiary |
|---:|---|---|---|---|---|
| 1 | `floors/f01/` complete Days 1–5 | Yes | Yes | Yes | No |
| 2 | **Missing** (`floors/f02/` absent) | Budgets/XP only in rules/70 | Yes | Yes | No |
| 3–6 | Missing | Budgets/XP only through F6 in rules/70; **0** fixed creatures | No | Thin wiki lists in floor-data / bestiary | No |
| 7 | Missing | Not even a floor key with creatures in rules/70 sample | No | Thin / later-book | No |

CR guidance only: `/workspace/dcc-campaign/rules/75-cr-by-floor-5e.md` (bands for F1–18; no mob roster). Narrative seeds: `/workspace/dcc-campaign/floors/04-floor-bible.md`, `/workspace/dcc-campaign/floors/00-campaign-narrative.md`.

**Plain statement:** For Core Book Monsters, Valtay can draft **flavor + “use SRD X”** for the 10 Floor 1 house stubs and can cite canon **names/behavior notes** for F1–F2. Everything else is wiki research or blank. Floors 3–7 need a Lore canon bestiary pass before book draft.

---

## 3. Blocked / don’t-print-yet

### 3.1 VERIFY / unverified / inspired / open

| Item | Where | Action |
|---|---|---|
| **5 parked loot candidates** (`needs_verify`) | `tables/loot-decks/f01-any-orientation-pit.json` | Not drawable: Potion of Animal Friendship; Potion of Giant Strength (Hill); +1 Shield; Heward’s Handy Haversack; Portable Hole — SRD/print confirmation or Floor 1 ceiling |
| Wiki catalogs | `catalog/items.md`, `loot-boxes.md`, `bestiary-by-floor.md`, `bosses.md`, `floor-data.md` | Marked unverified / wiki-only — **do not treat as book-verified canon** |
| Floor 2 conflicts / backlog | `canon-floor-2.json` (`open_conflicts`, `refinement_backlog`, e.g. Blimp boss identity, Rot Stickers on F2) | Don’t print contested lines as fact |
| Inspired F1 house mobs | Vent Rat, Mannequin Staff, Exit Greeters, Bruiser, Dean Thudd, etc. | Fine as **HOUSE**; label as such if Core Book mixes canon and Orientation Pit |
| Story Box open questions | `rules/42` §7, `rules/45` | Don’t lock contested sale/deed edges without Caleb |

### 3.2 Copyright / non-SRD risk

- Loot cards cite **PHB 2024 (36)** and **DMG 2024 (3)** — print **paraphrased mechanics only**; no near-verbatim PHB/DMG passages.
- Wiki catalogs are condensed; still **fan-derived**. Prefer ledger-backed paraphrases (`CANON-LEDGER.md`) over wiki prose for anything printed.
- Heuristic scan did not find clean >25-word book-quote blocks in bosses/bestiary; items.md is table-shaped (low verbatim risk) but remains unverified.

### 3.3 Crafting Studio prices (12k / 30k)

**Already updated in** `/workspace/dcc-campaign/rules/20-crafting-5e.md` §9.1 / §9.1a:

- Floors 1–2: Crafting Studio **12,000**, Enhanced **30,000** (changelog: was 20,000 / 50,000).
- Higher floors use the smoothed schedule (e.g. F7 Enhanced **50,000** is intentional scale, not the old F1–2 price).

No stale “Studio = 20,000 / Enhanced = 50,000 on F1–2” live rule found; only historical “was …” notes.

---

## 4. Ready now vs Lore next

### Ready for Valtay to draft now

1. **Items — mundane chapter skeleton:** all 191 reskins (name + snark); display rule `Display Name (SRD Name)`.
2. **Items — Floor 1 magic/consumable appendix:** 99 loot-deck cards + 4 house items + Story Box explainer (cite 40/42/45; don’t invent F2+ decks).
3. **Monsters — Floor 1 Orientation Pit appendix:** 10 stubs with “stats: SRD \<id\>” + house flavor (pull color from day pages / overview nameplates, not sealed notes).
4. **Monsters — Floor 1–2 canon name appendix (sidebar / appendix):** from `canon-floor-1/2` (names + one-line notes), clearly tagged canon vs inspired vs unverified.

### Lore should produce next (rough sizes)

| Deliverable | Rough size | Why |
|---|---|---|
| **Canon bestiary list Floors 3–7** (names, floor, tag, ledger rows, 1–2 sentence behavior, suggested SRD analogue — **no** copied book text) | ~80–150 rows / ~15–25 pages md+json | Unblocks Monsters chapter beyond F2; wiki lists are not enough |
| **Monster reskin / nameplate table** for F1 house + F1–2 canon priority mobs | ~40–60 entries (display name, SRD id, 1 snark, tag) | Parallel to item-reskins; gives Valtay consistent voice |
| **Book-ready item flavor expansion** (optional): 2–4 sentences each for top ~40 chargen + F1 loot icons | ~40 blurbs | Only if Core Book wants more than snark lines |
| **Magic / DCC-unique item shortlist for Core Book** (SRD-safe paraphrase + reskin) from `catalog/items.md` priority set | Start with ~30–50 “print in Core” picks | Avoid dumping all 195 wiki rows |
| **Floor 2 playable stub list** (SRD mapping + counts) for Encounter Bot | ~15–25 creatures | After bestiary list; campaign still has no `floors/f02/` |

---

## 5. Key paths (quick index)

**Items:** `tables/item-reskins.*`, `catalog/items.md`, `catalog/loot-boxes.md`, `campaign/tables/loot-decks/`, `campaign/rules/40|42|45-*.md`  
**Monsters:** `tables/canon-floor-1.*`, `tables/canon-floor-2.*`, `catalog/bestiary-by-floor.md`, `catalog/bosses.md`, `catalog/floor-data.md`, `campaign/floors/f01/day-*.json`, `campaign/rules/70-encounter-budget-5e.json`, `campaign/rules/75-cr-by-floor-5e.md`  
**Canon:** `CANON-LEDGER.md` v1.15 (not opened for quote extraction in this pass beyond table refs already in canon-floor files)

---

## 6. Method notes

- Read-only on `/workspace/dcc-campaign`; wrote only this lore draft + INDEX hash.
- Never opened `gm-notes/secret/` or sealed paths; did not run `ledger_build.py`.
- Counts are from JSON/markdown structure on disk at scan time; claimed Encounter Bot pins from other jobs are out of scope here.
