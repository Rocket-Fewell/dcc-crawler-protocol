# Floor 2 Soft Open — Achievement Suggestions
Owner: Encounter Bot | Status: draft (revision) | Updated: 2026-10-05
Summary: Suggested hooks for Syndicate (framing/rewards) and Lore (canon pass). Not live awards.
Soft Open is the **FINAL** district name (Caleb 2026-10-05). A-056 / ACH-1829 stays **house**.

## Counts (Caleb: F2 possible total must exceed F1)
- **Floor 1** hook instances (day specs): **107**; unique catalog/proposed ids ~**46**; per-day average **21.4**.
- **Floor 2** deed instances (hooks + proposed): **363** (hooks **254** + proposed **109**); demoted-to-flavor (no deed) **3**; unique catalog ACH ids **97** + unique proposed names ~**109**; per-day average **36.3** (~**1.7×** F1 daily avg).
- Math note (Syndicate 18:04 CT): compare F2 **daily** avg to F1 **daily** avg (21.4), **not** F2 total÷F1 daily. Correct ratio ≈ **1.7×** (target ~1.5–2×). Prior header wrongly showed ~17.76×.
- Per-day Floor 2 deed totals: D1=36, D2=34, D3=36, D4=36, D5=37, D6=36, D7=36, D8=38, D9=38, D10=36
- F2 deed total **363** > F1 total **107**: **YES** (still clearly above Floor 1 after demotions).

## Canon Soft Open set (rb-18) — ACH-1827..1835 wired
| ACH | Ledger | Name | Tag | Wire | Trigger |
|-----|--------|------|-----|------|---------|
| ACH-1827 | A-034 | Dungeonpreneur | **canon** | enc-d04-02, enc-d09-02 | Invent stackable weapon/device/potion (smoothie/blender/trap kit). |
| ACH-1828 | A-047 | Grease Monkey | **canon** | enc-d09-03 | Build/deploy wheeled lure/bomb into stairwell vs Rage Elemental. |
| ACH-1829 | A-056 | I'll Take the Ceramic Dalmatian, Pat! | **house** | enc-d08-03 | Discover reward room (Menagerie). HOUSE Soft Open placement; canon floor unsettled. |
| ACH-1830 | A-071 | Like a Moth to the Flame | **canon** | enc-d09-03 | Deal damage to mob 76+ levels higher (Rage Elemental). |
| ACH-1831 | A-083 | Menagerie | **canon** | enc-d08-03 | Discover pet reward room after Ralph. |
| ACH-1832 | A-091 | PETA Enthusiast | **canon** | enc-d07-02, enc-d08-01 | Feed pet biscuit; remove Danger Dingo hostility. |
| ACH-1833 | A-123 | Wait, Bosses Can Leave Their Rooms? | **canon** | enc-d05-02, enc-d08-02 | First boss bursts out of chamber (Krakaren; Ralph if first). |
| ACH-1834 | A-131 | What Goes Up | **canon** | enc-d09-03 | Survive Reverse Gravity from Rage Elemental. |
| ACH-1835 | A-136 | You Call That a Trap? | **canon** | enc-d03-02, enc-d09-02 | Injure a mob with a trap you left. |

Notes:
- Catalog source: `tables/achievements.csv` ACH-1827..ACH-1835 (Syndicate seed).
- **ACH-1829 / A-056** remains **house** for Soft Open (Caleb; canon floor unsettled).
- **ACH-1833 / A-123** fires on first boss-out-of-room (Krakaren primary; Ralph if first). Krakaren is HOUSE CR 3 Neighborhood Boss.
- Rewards = Syndicate seed list; System decides; snark-only OK; F2 box ceiling core 4.5 + Story Box exception.

## Demoted to flavor (no deed) — Syndicate 18:04 CT
These stay as `flavor_lines` only; **not** achievements:
| Former name | Where | Reason |
|-------------|-------|--------|
| Hedgehog Sighting | enc-d02-03 | No real deed (rumor / do not field cmm-053). |
| F1 Reprieve Reminder | enc-d02-03 | No real deed (F2 reminder only). |
| Wrong Floor Impaler | enc-d03-02 | No real deed (warning; Impaler is F3). |

## House / catalog extras
Each day encounter carries Soft Open catalog `achievement_hooks` plus remaining `proposed_achievements` (demoted three removed from proposed).
Selected proposed (non-rb-18) highlights remain in day specs; highlights list unchanged except the three demotions above.

## Conflicts / open
- Rewards/slots: Syndicate only.
- Story Box F2 deck ids (f02-any-story-NN) need Lore/Syndicate card file.
- Accountant: `floors.2.fixed_encounters` pins (budget file not edited by Encounter Bot).
- Krakaren: HOUSE CR 3 on Chuul chassis — closed by Caleb; no over-cap flag.
