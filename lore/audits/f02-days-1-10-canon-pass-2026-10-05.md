# Floor 2 Soft Open — Canon Pass (Days 1–10)
Owner: DCC Lore | Status: draft | Version: 0.1 | Updated: 2026-10-05
Summary: Read-only canon pass on Encounter Bot Soft Open draft (`floors/f02/`, GitHub main `0a414fe`) against `CANON-LEDGER.md` v1.16, `tables/canon-floor-2` (RESERVE), `drafts/core-book-monster-table-v0.2`, and achievement notes. No campaign edits; sealed paths unread; `ledger_build.py` not run.

## Verdict: **PASS WITH FIXES**

Fixed points (T-1h saferoom eject, last 6h free descent, bosses may leave chambers / A-123, house 10-day clock labeled house, Silver F2, Fizz Grub / no Rot Stickers / no Acid Impaler on F2, Krakaren Neighborhood, pupa dual-burst, F1 Reprieve off, decision 031 rest, voice split intent) are largely honored. Monster nameplates match monster table v0.2. Several **wrong ledger ids**, **Neighborhood vs Borough stair slippage**, and **proposed hooks tagged “canon” that are not A-rows** need cleanup before treat-as-published.

---

## BLOCKERS (canon-breaking)

1. **Krakaren chamber stair claimed under M-365 (Borough/City only).**  
   Every Soft Open day page’s Routes table lists `` `stair-boss` | Claim stair in Krakaren/Borough boss chamber (M-365) ``, and `enc-d05-02` exits say “Stair if Borough chamber M-365” after a **Neighborhood** Krakaren fight.  
   Ledger **M-365** (and M-275 for Floor 1) covers **Borough and City** boss chambers only. Caleb closed X-059 as **Neighborhood Boss**. Citing M-365 for Krakaren asserts canon the ledger does not support.  
   **Fix:** Split the route: (a) Borough/City chamber stairs → M-365 only when that tier is true; (b) if Soft Open wants a stair in the Krakaren strip, tag it **HOUSE/inspired** and drop the M-365 cite (stairs still exist floor-wide via M-364). Rename proposed *Borough Stair* on Day 5.

---

## FIXES (file + enc / locus + plain fix)

| # | Where | Issue | Fix |
|---|---|---|---|
| 1 | All `day-01`…`day-10.md` Routes + `enc-d05-02` / `enc-d05-03` | Krakaren + M-365 / “Borough” stair language | See BLOCKER 1. |
| 2 | `achievement-suggestions.md` + `day-03.md` `enc-d03-03` | *Qwist Name Drop* tagged **canon**, cites **M-467** | M-467 is Rage Elemental door-pounding. Use **M-506** (Qwist / Big Shot Chicken). Retag proposed hook **house** (canon NPC, not an A-row). Day 4 already cites M-506 correctly. |
| 3 | `achievement-suggestions.md` + `day-01.md` `enc-d01-03` | *Don't Salt the Dead* cites **M-386** | M-386 is grub hordes chasing Crawlers out of neighborhoods. Spawning-after-corpse-destroy is **M-385** (destroying corpses stops leveling-up, not spawning). Retag proposed hook **house**; keep canon fact cite M-384/M-385. |
| 4 | `achievement-suggestions.md` + `day-02.md` `enc-d02-02` | *Mana Toast* cites **M-355**, tagged **canon** | M-355 = staffed vs unstaffed saferooms. Toaster / Mana Toast = **M-508 / M-509** (optional M-733 kitchen link). Retag proposed hook **house**; cite M-508/M-509. |
| 5 | `achievement-suggestions.md` “House / catalog extras” list | Many hooks tagged **[canon]** that are **not** ledger A-rows (Ratings Are On, Bathroom Briefing, Corpse Economy, Psionic Weather, Mailbox Error, Floor Club, Hedgehog Sighting, Early Stair Peek, Patch Preview, Cow-Tail Debut, Death Watch Ad, Taint Lesson, Lime Residue, Damien!, …) | Keep rb-18 A-rows as the only **canon achievement** set. Relabel the rest **house** (or “canon-fact hook”) so Soft Open does not invent A-ids. Facts may still cite M-rows. |
| 6 | All Soft Open day pages stairwell boilerplate | Pastes **M-275** Floor 1 quote (“Every Borough and City Boss arena on Floor 1…”) as Soft Open governance | Prefer **M-365** for F2 Borough/City chambers; keep M-275 as F1 cross-ref only, or drop the F1 quote from F2 boilerplate. |
| 7 | `day-05.md` `enc-d05-02` gm_color “A-123 on the burst” | Fine as [GM] color; ensure Discord/voice wiring never plays A-123 System toast as `[SYSTEM]` (decision 032: achievement callouts = GM) | Confirm Encounter Bot / voice bridge: A-123 banner = GM channel; dry FLOOR NOTICE stays System. |
| 8 | `day-07.md` `enc-d07-03` | Layout “sealed **CHAMPION** door” / “Opening Champion early” | Not player “champs,” but rename door (e.g. **PIT** / **RALPH**) to avoid champ\* strings in Soft Open copy. |

---

## OPTIONAL nits

- `_draft-counts.json` generator: PASS 387 / WARN 42 / FAIL 326 under Floor-1-hardcoded mode — Architect/Accountant tooling, not a lore falsification.
- Krakaren CR 4 vs L2 party cap 3 already flagged in overview — keep Accountant note; not a canon error.
- Repeated M-358 paraphrase lines still contain the word pair “safe rooms” inside ledger quote paste; body copy correctly uses **saferoom**. Prefer paraphrasing outside quotes.
- A-083 Menagerie is ledger **WIKI-ONLY** / incomplete infobox — OK to wire as rb-18, but note confidence when publishing.
- A-056 HOUSE placement is correctly labeled; leave open until Caleb freezes.
- Death Watch optional (`enc-d06-03`) already names Mexx-55 / Maestro energy — good; full Team Li Na escape saferoom (M-727/M-728) remains optional color if wanted later.

---

## Achievement review

### rb-18 / ledger A-rows (correctly listed)

| ID | Draft tag | Ledger check | Notes |
|----|-----------|--------------|-------|
| A-034 Dungeonpreneur | canon | VERIFIED F2 | Smoothie/blender invent = fair Soft Open wire. |
| A-047 Grease Monkey | canon | VERIFIED F2 | Wheeled lure/bomb vs Rage = fair paraphrase of wheeled device. |
| A-056 Ceramic Dalmatian | **house** | UNVERIFIED; floor conflict F9 vs F2 | Correct HOUSE Soft Open placement. |
| A-071 Like a Moth… | canon | VERIFIED F2 | Rage Elemental 76+ levels — OK if Rage stays absurdly high. |
| A-083 Menagerie | canon | WIKI-ONLY | Wire OK; flag wiki-only confidence. |
| A-091 PETA Enthusiast | canon | VERIFIED F2 | Biscuit → dingo hostility — OK. |
| A-123 Bosses leave rooms | canon | VERIFIED F2 | Krakaren primary / Ralph if first — OK; GM voice for callout. |
| A-131 What Goes Up | canon | VERIFIED F2 | Reverse Gravity survive — OK. |
| A-136 You Call That a Trap? | canon | VERIFIED F2 | Pupa/Rage trap wires — OK. |

### Mis-tagged or mis-cited proposed hooks

See FIXES 2–5. No invented A-numbers found in the rb-18 table itself. Volume (380 hooks vs F1 107) matches Caleb’s “more on F2” ask; quality cleanup is tagging/cites, not count.

### Voice split

Dry `system intro` / collapse `FLOOR NOTICE` lines look System-appropriate. Achievement proposals and gm_color sit on GM side. No requirement to move A-toasts onto System.

---

## Monsters vs monster table v0.2 + rulings

| Check | Result |
|-------|--------|
| Overview nameplate table (cmm-041…056, Fizz cmm-055) | Matches v0.2 |
| Rot Stickers not fielded; Fizz Grub HOUSE | OK (X-080 / M-765) |
| Acid Impaler warning only / F3 | OK (X-063 / M-764) |
| Krakaren Neighborhood | OK (X-059 / M-762) |
| Pupa timer→Vespas / early→half-formed | OK on Day 3 (`enc-d03-02`) |
| Hedgehogs not fielded after patch | OK Day 6 |
| Blimp STUB rumor only | OK |
| Rage Elemental summoned | OK Day 9 |

---

## Fixed points

| Point | Status |
|-------|--------|
| Saferooms close T-1h / eject (M-012, M-360) | Holds (esp. Day 10) |
| Last 6h free descent (M-368 / M-277/366) | Holds |
| Bosses leave chambers; A-123 | Holds Day 5/8 |
| House 10 days; X-062 labeled house | Holds |
| No F1 Reprieve on F2 | Holds |
| Decision 031 field Short Rest / no Long Rest outside saferoom | Holds in day boilerplate |
| Words: Crawlers; saferoom; no Death Mode as live mode | Holds (see Champion-door nit) |

---

## RESERVE pack — strong set pieces (coverage)

Present in Soft Open outline: Rev-Up / Laminak blender / Immunity Smoothie, Krakaren burst, grub→pupa→Vespa, Mind Horror + mailbox, pound/Ralph/Menagerie, Rage + escort, optional Death Watch (Mexx/Maestro), hedgehog patch, saferoom closure.

**Suggestions only (not blockers):** deepen Death Watch with Prince Maestro meat-talk + Mexx-55 disc (M-491, M-497) if the optional trailer is run; optional Li Na escape hallway saferoom beat (M-727/M-728); keep blimp as rumor (rb-03).

---

## Method

Read `floors/f02/00-overview.md`, `achievement-suggestions.md`, `_draft-counts.json`, and day `.md` pages (specs sampled for ids/kinds). Cross-checked ledger A-/M- rows listed above and `tables/canon-floor-2.md` / monster table v0.2. House decisions (026, 031, 032, Caleb conflict closers) treated as non-errors when labeled.
