# DCC Lore Status and TODO
Owner: DCC Lore | Status: review | Version: 2.18 | Updated: 2026-10-05
Summary: Pass history, coverage tables, source caveats and the running TODO list; formerly the body of INDEX.md.

> Moved here from INDEX.md in Pass 4 (the file tables below are historical; the current file list is `INDEX.md`). `sources/SOURCE-LOG.md` is now `sources/source-log.md` and `catalog/reconciliation-pass3.md` is now `catalog/reconciliation.md`.

Purpose: canon knowledge base for *Dungeon Crawler Carl* (Matt Dinniman), mechanics-focused, for RPG / AI-DM emulation. Spoilers through Book 8. Notes are paraphrased; unverified claims are tagged **[UNVERIFIED]**.

## Files
| File | Contents | Status |
|---|---|---|
| `mechanics.md` | 25 sections: setting, crawlers, stats, health/death, XP/skills, races/classes, magic, safe rooms, loot boxes/achievements, bosses, stairwells, sponsors/viewers, parties/guilds, quests, clubs/tattoos/Cookbook, pets/NPCs, leaderboard/PK, status effects, Ring of Divine Suffering, key artifacts, AI behavior, penalties, floor table (1-18), gods/Ascendency/Nothing/Faction Wars/T'Ghee, known gaps | Pass 1 done; wiki-sourced |
| `characters.md` | Part A curated core cast; Part B auto-extracted roster of all 231 wiki character pages | Pass 1 done |
| `floors-and-plot-by-book.md` | Book list + title correction, floor table, per-book spoiler summaries | Pass 1 done (summary-level) |
| `raw/all.json`, `raw/pages/*.txt`, `raw/titles.txt`, `raw/roster_auto.md` | Local mirror of all 2,017 Fandom wiki pages (wikitext + cleaned) for later passes | Supporting data |
| `parts/m1-m3.md` | Source parts concatenated into mechanics.md | Supporting |

### Pass 2 files (added Oct 3, 2026, CT) - all under `catalog/`, `sources/`, `tools/`
Regenerate the table-based catalogs with `python3 tools/gen.py` (reads `raw/all.json`; hand-written files are NOT touched by it: `mechanics-clarifications.md`, `books-3-4-detail.md`, `bestiary-by-floor.md` header, `sources/*`).
| File | Contents | Approx. size | Reliability |
|---|---|---|---|
| `catalog/achievements.md` | 150 achievement pages + 14 master-list-only entries + 26 unnamed (N/A) achievements; floor, trigger, reward, books | 164 named | wiki, condensed; 11 flagged incomplete |
| `catalog/skills.md` | 100 skill pages (cost/cast/CD/target/duration where the wiki has them) | 100 | wiki infobox fields; many `?` |
| `catalog/spells.md` | 95 spell pages | 95 | same |
| `catalog/classes.md` | How classes work + 32 detailed classes + 93 classes only in the wiki's List of Classes (through B7) | 125 | wiki |
| `catalog/races.md` | 109 race pages (crawler, Syndicate, aliens, mob types) | 109 | wiki; infobox sparse |
| `catalog/items.md` | 163 items + 32 potions | 195 | wiki |
| `catalog/loot-boxes.md` | Tier rules + 76 box pages with source and sample loot | 76 | wiki |
| `catalog/benefits-and-status-effects.md` | 22 benefits + 68 status effects | 90 | wiki |
| `catalog/quests.md` | 29 quest pages | 29 | wiki |
| `catalog/bosses.md` | Boss tier ladder + 39 boss-category pages (level/tier/abilities/constraints) | 39 | wiki + cross-check |
| `catalog/bestiary-by-floor.md` | Mob/boss levels by floor (fan-wiki) + discrepancy log | ~116 rows | **fan-wiki, generated - UNVERIFIED** |
| `catalog/floor-data.md` | Per-floor sheet 1-18: crawlers, level ranges, mob levels, exits, bosses, locations | 18 | wiki infoboxes |
| `catalog/mechanics-clarifications.md` | XP / stats / skills / loot boxes / bosses / safe rooms: claim, source tag, confidence; rejected claims | ~45 items | mixed, each tagged |
| `catalog/books-3-4-detail.md` | Chapter-level beats for Books 3 and 4, numbers, conflicts | 2 books | wiki chapter summaries + YouTube recaps; **UNVERIFIED vs. books** |
| `sources/SOURCE-LOG.md` | Every external source used, access method, limits | - | - |
| `sources/reddit/threads.md` | Reddit thread notes (via search-index snippets only) | ~13 threads | community opinion |
| `sources/youtube/*.txt` | Local caption transcripts (8 videos). **Working copies only; do not quote at length.** | - | auto-captions garble names |
| `sources/fanwiki/*.txt`, `sources/nl/*.txt` | Scraped working copies from dungeon-crawler-carl.wiki and dungeoncrawlercarl.nl | - | fan sites |
| `tools/wk.py`, `tools/gen.py` | Parsers/generators for the catalogs | - | - |

## Important correction
**Book 8 is *A Parade of Horribles*** (May 12, 2026), not "The Perfect Scramble" (no such DCC book found; unrelated short film). Book 9 (finale, working title "The Beautiful Place", possibly two volumes) is unreleased/undated **[UNVERIFIED: fan/news sources only]**.

## Coverage per book
| # | Title | Floors | Plot | Mechanics | Characters | Depth |
|---|---|---|---|---|---|---|
| 1 | Dungeon Crawler Carl | 1-2 | Yes | Yes | Yes | Good (wiki chapter summaries) |
| 2 | Carl's Doomsday Scenario | 3 | Yes | Yes | Yes | Good |
| 3 | The Dungeon Anarchist's Cookbook | 4 | Yes | Yes | Yes | Moderate - plot beats thin |
| 4 | The Gate of the Feral Gods | 5 | Yes | Yes | Yes | Moderate |
| 5 | The Butcher's Masquerade | 6-7 | Yes | Yes | Yes | Moderate; **Floor 7 thin** |
| 6 | The Eye of the Bedlam Bride | 8 | Yes | Yes | Yes | Good |
| 7 | This Inevitable Ruin | 9 | Yes | Yes | Yes | Good |
| 8 | A Parade of Horribles | 10-11 | Yes | Yes | Yes | Moderate-good |
All coverage is via the Fandom wiki (summary level), not the books themselves.
### Pass 2 coverage update (appended; Pass 1 table above unchanged)
| # | Pass 2 additions | Depth now |
|---|---|---|
| 1 | achievements (floor 1 complete from hub page), mob/boss levels (fan-wiki), mechanics clarifications | Good |
| 2 | achievements (Third Floor / Over City), bestiary rows | Good |
| 3 | **Chapter-by-chapter beats (34 ch + epilogue)**, bosses, mob levels, items, 6+ sponsor/mechanic notes, Fandom + YouTube + Cookbook-site cross-check | **Good (was Moderate)** - still not checked against the book text |
| 4 | **Chapter-by-chapter beats (34 ch + epilogue)**, boss levels (Ruckus 55, Denise 53, Mrs. Ghazi 52, Lusca 82), Gate of Feral Gods rules | **Good (was Moderate)** - same caveat |
| 5 | bestiary snapshot (F6), classes/skills/spells catalogs | Moderate; **Floor 7 still thin** |
| 6-8 | catalogs, bosses, floor sheet; B8 bestiary snapshot (fan-wiki) | Good / Moderate-good |


## Sources & caveats
- Primary: Fandom wiki https://dungeon-crawler-carl.fandom.com (hyphenated; `dungeoncrawlercarl.fandom.com` does not exist). Pulled via MediaWiki API; its Spoiler Policy applies and some pages are only current "through Book 7" **[UNVERIFIED for B8 on those pages]**.
- Cross-checks: mattdinniman.com, Penguin Random House, Goodreads (Book 8 title/date); dungeoncrawlercarl.nl (race/class, achievements/loot boxes explainers); web-search snippets (Variety, whathappened.fyi, afterword.to) for the B8 ending - consistent with wiki.
- **Not done (Pass 1 note, partly superseded - see Pass 2 below):** no Reddit (r/dungeoncrawlercarl) or YouTube transcript content was actually read; only search snippets seen. No book text consulted directly. Wiki could be wrong/incomplete; XP formulas, exact stat-to-effect math, drop tables are not established.

### Pass 2 sources & caveats (appended Oct 3, 2026, CT)
- **YouTube**: full auto-caption transcripts of 8 videos were read (two Mana Toast chapter recaps of Books 3 and 4 were mined in depth; others for color). Captions garble proper names, so spelling follows the Fandom wiki. See `sources/SOURCE-LOG.md`.
- **Reddit**: reddit.com is **blocked (403/timeouts) from the box**, so threads were read only as search-index snippets (post + top comments). Sub wiki/FAQ/megathreads and the r/DungeonCrawlerCarlRPG stat-block table were **not** read. Treat Reddit-derived points as community opinion (`sources/reddit/threads.md`).
- **Fan sites** used: dungeon-crawler-carl.wiki (self-described as generated; contains errors, e.g. its Mimic Rex kill and boss-tier lines), dungeoncrawlercarl.nl, crawlerscookbook.com. Discrepancies are logged in `catalog/bestiary-by-floor.md` and `catalog/books-3-4-detail.md`.
- Conventions for Pass 2 files: `[W]` Fandom wiki, `[R]` Reddit, `[YT]` YouTube, `[FS]` fan site, `[FW2]` generated fan wiki; confidence HIGH/MED/LOW; **[UNVERIFIED]** = no book check. Notes are paraphrased; only very short quotes (item names/achievement titles).
- Known weak spots in the generated catalogs: infobox fields blank on the wiki show as `?`/`-`; 'Bk' lists books cited on the page, not first appearance; spoiler column is the wiki's spoiler gate; descriptions are the wiki's lead sentence truncated.

## TODO for future passes
1. Reddit mining (r/dungeoncrawlercarl wikis/megathreads, theory posts) and YouTube/audiobook-summary transcripts; cross-verify against wiki.
2. Races overview and full race list with per-race perks; full class list (tiers 3/6/9) with abilities.
3. Per-spell, per-skill, per-item catalogs (the raw wiki has them); full achievement catalog (~161 entries harvested in raw text).
4. Loot-box drop-table details by tier, crafting/Midnight Market, Prize Carousel, Unwashed/Blood Hunters, Hunters' rules.
5. XP/leveling math, stat caps, buff stacking, Benefits/Titles list.
6. Chapter-level plot for Books 3, 4, 5 (esp. Floor 7), 8; boss stat blocks per floor.
7. Pop-culture reference pages; Dinniman interviews/Q&A for authorial rulings.
8. Adaptation differences (Soundbooth Theater audiobooks); DCC tabletop game rules (mentioned by wiki).
9. Resolve items in mechanics.md section 25 "Known gaps" and every [UNVERIFIED] tag; check B9 release status.
10. AI-DM layer: encounter templates, System voice/tone guide, table-roll adaptations (not started).

## Pass 2 status of the TODO list above (appended; original list unchanged)
1. Reddit/YouTube mining - **PARTIAL.** YouTube transcripts read (B3, B4 deeply). Reddit read only via snippets (blocked). Still need: r/dungeoncrawlercarl wiki/FAQ, megathreads, full comment trees; YouTube transcripts for Books 5-8 and Dinniman Q&A videos.
2. Races/classes - **DONE at catalog level** (`races.md`, `classes.md`); per-race perks mostly blank on the wiki; tier-3/6/9 class abilities not systematically extracted.
3. Per-spell/skill/item catalogs and achievements - **DONE at catalog level** (`spells.md`, `skills.md`, `items.md`, `achievements.md`, `loot-boxes.md`, `quests.md`); depth is the wiki's infobox only; most skill rows (~95%) and ~two-thirds of spell rows have no mana cost recorded on the wiki.
4. Loot-box drop tables, crafting/Midnight Market, Prize Carousel, Unwashed/Blood Hunters/Hunters' rules - **PARTIAL→largely DONE (Pass 9)** for Midnight Market, Prize Carousel, Hunters' rules, and Blood Hunter/Unwashed name traps; crafting was Pass 5. Still open: true drop-table math (not in canon), leftover patch/boon lists.
5. XP/leveling math, stat caps, buff stacking, benefits/titles - **PARTIAL** (`mechanics-clarifications.md`): no XP table exists; stat-100 upgrade and skill-cap rules recorded; buff stacking only partly.
6. Chapter-level plot B3, B4 - **DONE** (`books-3-4-detail.md`); B5 (esp. Floor 7) and B8 chapter-level **NOT done**; boss stat blocks - **PARTIAL** (`bosses.md`, `bestiary-by-floor.md`: level and tier, no STR/INT blocks because canon rarely gives them).
7. Pop-culture reference pages; Dinniman interviews/Q&A - **NOT done** (pop-culture pages exist in `raw/pages/Book N Pop Culture References.txt`).
8. Adaptation differences; DCC tabletop rules - **NOT done** (only noted that a TTRPG subreddit + stat-block table exist).
9. Resolve `mechanics.md` section 25 gaps and [UNVERIFIED] tags - **NOT done**; new conflicts logged (Carl L84 vs L81 at end of B8; Krakaren L9 Borough vs L10 Neighborhood; Cookbook edition vs holder count; Mimic Rex kill; fan-wiki boss tier lines). B9 release status not re-checked.
10. AI-DM layer - **NOT started.**

### New TODOs from Pass 2
11. Re-reconcile `mechanics.md` boss/box lines with `bosses.md`/`mechanics-clarifications.md` (ladder is now confirmed as N < Borough < City < Province < Country < Floor < Dungeon).
12. Read r/DungeonCrawlerCarlRPG stat-block table (245 entries) and r/dungeoncrawlercarl wiki via an accessible mirror; extract real stat blocks (the TTRPG stat blocks are game-design, label separately).
13. Mine the unmined transcript `sources/youtube/r0w4mNaSf-4.txt` (reaction podcast) and fetch Mana Toast recaps for Books 1, 2, 5, 6, 7, 8 for chapter-level detail (Floor 7 especially).
14. Fill `?` cells: skills/spells missing cost/CD; races without bonuses/penalties; achievements whose triggers came from only an AI-narration blurb (the 14 master-list-only entries).
15. Cross-check generated fan-wiki numbers (levels, sponsor lists) against book text/audiobook; resolve conflicts table in `catalog/bestiary-by-floor.md`.
16. Per-class tier ladder (Floors 6/9/12 specializations) and endorsements list; Donut's rotating specialties across floors.
17. Check Book 9 status (title, date, one vs two volumes) again.

---
# Pass 3 (Oct 3, 2026 CT) - appended; everything above is unchanged

### Pass 3 files
| File | Contents | Reliability |
|---|---|---|
| `catalog/system-voice.md` | **Style guide** for the System AI / show-runner voice + short tagged quote tables: achievement texts, snark by target, 68 loot-box names + naming conventions, floor announcements (1-11), boss-intro formats, quest/notification formats, mood arc B1-B8, AI-DM generator recipe | wiki transcriptions, short quotes; **[UNVERIFIED vs print]** |
| `catalog/system-voice-index.md` | Generated page-name index of 571 wiki sections with System-voice text (no text copied); regenerate with `python3 tools/voice_index.py` | generated |
| `catalog/books-5-8-detail.md` | Chapter-level beats for **Book 5** (77 ch + epilogue = Floor 7) and **Book 8** (Floors 10-11, 7 heats + parade), numbers, conflict logs | wiki chapter summaries + Mana Toast; **UNVERIFIED vs books** |
| `catalog/books-1-2-6-7-detail.md` | Chapter beats and gap-fills for Books 1, 2, 6, 7 + conflict log | same |
| `catalog/reconciliation-pass3.md` | Section-25 gap table, `[UNVERIFIED]` resolution log, Gate custody chain, memorial crystals, achievement fills, **Book 9 status** | mixed, each cited |
| `tools/voice_index.py`, `tools/yt_fetch.py` | index generator; transcript fetcher (venv `/workspace/yt`) | - |
| `sources/youtube/*.txt` | now 15 transcripts (added B1, B2, B5, B6, B7, B8 Mana Toast + Bookborn 1-7) | auto-captions |
| `work/` | scratch JSON/folded transcripts from Pass 3 (safe to delete) | not KB content |
Appended sections: `mechanics.md` ("Pass 3 resolution of section 25"), `floors-and-plot-by-book.md` ("Pass 3 addenda"), `catalog/mechanics-clarifications.md` (P3.1-P3.9), `sources/SOURCE-LOG.md`.

### Pass 3 coverage update
| # | Depth now |
|---|---|
| 1 | **Chapter-level** (`books-1-2-6-7-detail.md`) |
| 2 | **Chapter-level**; Grimaldi vine resolved |
| 3-4 | Chapter-level (Pass 2) |
| 5 | **Chapter-level**; **Floor 7 is canonically a ~10-minute "Great Race" pod level**, so "Floor 7 thin" is a property of canon, not a research gap |
| 6 | **Chapter-level**, all three parts |
| 7 | **Chapter-level**, all four parts |
| 8 | **Chapter-level** (all 98 chapters in heats/parade groups) |
| 9 | Not published. Working title "The Beautiful Place"; finale, two volumes planned; **no release date** (Dinniman, July 2026: "still like a year out"); Patreon prologue + ch1-2 posted. |
Still all via wiki/recaps, never the book text.

### Pass 3 status of the TODO list
1. Reddit/YouTube - **PARTIAL**: YouTube recaps for B1, 2, 5, 6, 7, 8 read; Hello Crawlers podcast + 2 videos hit YouTube's block (not circumvented); Reddit still 403 (skipped).
5. XP/HP math - **OPEN** (not answerable from canon; wiki says undefined).
6. Chapter-level B5/B8 - **DONE** (Floor 7 included).
9. Section 25 and `[UNVERIFIED]` tags - **DONE for those with an answer** (see `reconciliation-pass3.md`); still open: XP curve, unconscious threshold, Scavenger's Daughter identity, fan-wiki bestiary numbers, Gate's other components. B9 status re-checked.
10. AI-DM layer - **PARTIAL**: System voice guide + generator recipe written; encounter templates still not started.
13. Mana Toast recaps B1, 2, 5-8 - **DONE**; `r0w4mNaSf-4` still unmined.
17. Book 9 status - **DONE** (no date).

### New TODOs from Pass 3
18. Retry blocked YouTube items later (Hello Crawlers Ep 25 `tqmd62wcI6c`, `bkCQ9-_8GjE`, `F8_f7qcrYk4`) only through normal means; also Dinniman Q&A videos for authorial rulings.
19. Audiobook/"extra Pineapple Cabaret chapters" (B8) and any short stories - not covered.
20. Verify spot claims against book text/audiobook: B5 ch5/47 Ring-marking of Miriam (conflict), hand vs claw, 23 vs 31 Floor-11 survivors, Gate's other components, who the Scavenger's Daughter is.
21. Extend `system-voice.md` with Book 8 on-page quotes (the wiki's AI Description coverage of B8 items is thin) and with direct Cascadia/Zev quotes from transcripts if more are fetched.
22. Reconcile fan-wiki bestiary numbers (TODO 15) against the Fandom mirror B5-B8 pages; Denise "Floor 7 goose" claim likely wrong.
23. Re-check Book 9 monthly (title lock, date, retailer listing, Variety/Patreon updates).


---
# Pass 4 (Oct 3, 2026 CT) - appended

- Built `CANON-LEDGER.md` (the master hard-memory ledger; 558 quote-bearing entries plus 46 conflict/flag rows) and `ledger-rules.md`; tools `ledger_*.py` build and check it.
- Brought the folder into line with NAMING-CONVENTIONS.md v1.0: headers on every `.md`, per-folder `INDEX.md`, renames `SOURCE-LOG.md` -> `source-log.md` and `reconciliation-pass3.md` -> `reconciliation.md` (versions belong in headers), retired files moved to `_archive/`.
- TODO: Reddit still unread (403); nothing checked against book text; the 7 UNVERIFIED achievements and ledger section 8 (conflicts X-001..X-025) are the open questions.

---
# Pass 7 (2026-10-03 CT) - appended: races and Floor 3 race selection

- Added ledger section 11 (CANON-LEDGER.md v1.3): **R-025..R-044** (race-selection process) and **R-045..R-081** (per-race rows) = 57 rows (48 VERIFIED, 8 WIKI-ONLY, 1 UNVERIFIED); conflicts **X-031..X-041** appended to section 8. R- was already the 4e Races prefix, so it was continued rather than creating a new one (documented in `ledger-rules.md` v1.3; next free R-082, X-042).
- New catalog `catalog/race-selection-canon.md`; `catalog/races.md` notes (and the notes string in `tools/gen.py`) now point to ledger rows; INDEX files updated; `tools/apply_headers.py` META knows the new catalog file.
- New sources saved: `sources/nl/how-race-and-class-work.txt` (NL explainer) and `sources/web/race-selection-web-snippets.txt` (Cookbook, Reddit snippets, search synthesis). Mana Toast B2 recap (`sS36rv-jPLg`) re-read for the 320/398-option and three-recommendation facts.
- Findings: 'three races out of hundreds' has a wiki chapter cite plus YouTube (B2 recap) and NL support; the '~80% keep their race' figure has a wiki B2 ch7 cite plus NL/Cookbook repeats but no independent recap and no readable Reddit thread (X-032). Grulke, Dwarf, Cretin and Half-Djinn are not shown to be crawler-selectable (X-033, X-035); Vampire is a curse (X-034).
- Live Fandom pages for Grulke and Nodling returned HTTP 403 to WebFetch, so the local mirror was used; the live Tutorial Guild Hall page matched the mirror. Reddit stayed blocked (snippets only).
- TODO 24: check R-025..R-081 chapter cites against the Book 2 text/audiobook (ch1, ch2, ch7 especially) and the '~80%' line. TODO 25: bonuses/penalties for Tigran, Frost Maiden, Dog Soldier, Curupira, Amazonian, Igneous, Naga, Crocodilian are not on the wiki. TODO 26: mine `r0w4mNaSf-4` and Book 5 for Nodling/Hongrish detail. TODO 27: if `tools/gen.py` is re-run, run `tools/apply_headers.py` after it.


---
# Pass 8 (2026-10-04 CT) - appended: classes and Floor 3/6/9 class selection

- Added ledger section 12 (CANON-LEDGER.md v1.4): **C-014..C-032** (class-selection process) and **C-033..C-050** (named crawler examples) = 37 rows (37 VERIFIED); conflicts **X-042..X-047** appended to section 8. C- continues the 4d Classes prefix (documented in `ledger-rules.md` v1.4; next free C-051, X-048).
- New catalog `catalog/class-selection-canon.md`; `catalog/classes.md` notes point to ledger rows; INDEX files updated; `tools/apply_headers.py` META knows the new catalog file.
- Sources: local wiki Class/Tutorial/Character Actor/Earth Hobby Potion/Four Seasons + named class pages; Mana Toast B2 (`sS36rv-jPLg`) and B5 (`TKcMxF2dA3w`); Bookborn (`QTk6BtBipPk`); B3 recap (`FHLzs9fjyU8`); NL `how-race-and-class-work.txt`. Reddit skipped (blocked). No new web snippet file required.
- Findings: AI three class recommendations are **skill-based only**; Floor 6 is a **10-minute no-chat** room; non-specializing classes take **endorsements** (name unchanged; Hazmat documented for Katia); Four Seasons **never finished** (max three; fourth class unnamed); Character Actor rotates specialties each floor; temporary corpse classes and pet-class biscuit exception recorded.
- **TODO 16** (per-class tier ladder / endorsements / Donut rotating specialties): **PARTIAL→largely DONE** for process + named paths; remaining gap is a full endorsement name list and benefit text for every List-of-Classes upgrade.
- TODO 28: mine remaining endorsement names from Book 5 text/audiobook. TODO 29: confirm Glass Cannon cite (X-042) and Forsaken Aerialist first-seen (X-043) against books. TODO 30: Elite Gurkha Warrior (Donut F11) thin local page — expand if a fuller page appears.

---
# Pass 9 (2026-10-04 CT) - appended: hunters, sponsors, Prize Carousel, Midnight Market

- Added ledger section 13 (CANON-LEDGER.md v1.5): **M-119..M-157** (process: hunters/trophies/Masquerade Prize Counter, sponsors/Benefactor/Fan boxes, Prize Carousel, Midnight Market) plus examples **H-054..H-056**, **I-026**, **L-021..L-022**, **T-070..T-071** = 47 rows; conflicts **X-048..X-051** appended to section 8. Next free: M-158, H-057, I-027, L-023, T-072, X-052.
- New catalog `catalog/hunters-and-sponsors-canon.md`; INDEX files updated; `tools/apply_headers.py` META knows the new catalog; `mechanics.md` §11/§16/§25 point at the catalog without deleting old bullets.
- Sources: local wiki (Hunters, Sixth Floor, Hunting Trophy, Butcher's Masquerade Ball, Sponsors, Benefactor Box, Fan Box, Prize Carousel, Midnight Market, Fantasy Hunter Camp, Ring of Divine Suffering, Blood Hunter, Unwashed, Chaco/Vrah/Zabit, Hunter-Killer/Scourge/Apex Predator) + YT `TKcMxF2dA3w` / `FHLzs9fjyU8` / `FurNY4o0uCo` + NL loot-box explainer. Reddit skipped (blocked). No novel text.
- Findings: hunters are paying F6 tourists (level-50 bump, Zockau grace, real death); trophies are **hands** (reconfirm X-001); Prize Counter at Masquerade via Chaco; sponsors max 3 auctioned F4/5/6; Benefactor vs Fan boxes; Prize Carousel = rare Fan Box minigame (Cookbook path); Midnight Market = Desperado bottom floor via Upgrade Patch (Gray Market sibling). **Blood Hunter** is a show; **Unwashed** is a Nothing entity — not hunter subtypes (X-049, X-050). Fantasy Hunter Camp operator attribution conflict (X-048).
- **TODO 4** (loot-box drop tables / crafting / Midnight Market / Prize Carousel / Unwashed / Blood Hunters / Hunters' rules): **PARTIAL→largely DONE** for Midnight Market, Prize Carousel, Hunters' rules, and the Blood Hunter / Unwashed name traps. Still open: true drop-table math (does not exist in canon), crafting already in Pass 5, leftover patch/boon lists.
- TODO 31: resolve Fantasy Hunter Camp Vrah-family vs The Dream (X-048) against Book 5 text. TODO 32: expand named Prize Counter catalog beyond wiki-priced rows if fuller pages appear. TODO 33: deity-sponsorship market deep dive (separate from crawler patrons). **→ DONE Pass 10** (ledger §14 / gods-faction-wars-canon.md).

---
# Pass 10 (2026-10-04 CT) - appended: gods, Ascendency, Nothing, Faction Wars, T'Ghee

- Added ledger section 14 (CANON-LEDGER.md v1.6): **M-158..M-209** (process: gods/worship/Soul Armor/smite/deity sponsorship, Ascendency, Nothing, Faction Wars, T'Ghee) plus examples **H-057**, **I-027**, **T-072..T-073** = 56 rows; conflicts **X-052..X-053** appended to section 8. Next free: M-210, H-058, I-028, L-023, T-074, X-054.
- New catalog `catalog/gods-faction-wars-canon.md`; INDEX files updated; `tools/apply_headers.py` META knows the new catalog; `mechanics.md` §23 points at the catalog without deleting old bullets; `catalog/hunters-and-sponsors-canon.md` points deity sponsorship to section 14.
- Sources: local wiki (Gods, Celestial Ascendency, Nothing, Faction Wars (game), T'Ghee (game)/Card, Club Vanquisher, Smite, Sponsors, Twelfth Floor, Laundry Day, Bolt of Ophiotaurus, Juice Box, Paz Lo, Team Retribution, Memorial Crystal, Divine Epiphany) + YT `7Q49XeziMX0` / `FurNY4o0uCo` / `kk6nspvVf_M` / `TKcMxF2dA3w`. Reddit skipped (blocked). No novel text. No new web snippet file required (local coverage sufficient).
- Findings: Soul Armor / paid pilots; deity sponsorship ≠ crawler patrons; Club Vanquisher temple tether; Paz+Bolt first F8 god kill (X-052); Laundry Day driver-strip (X-053); Ascendency council-seat prize + 12h collapse; Nothing shatter→F12/F15/F18; Faction Wars Ceasefire 60h / Ramp-Up 180h / Peeling / 6h vs 1-week throne; T'Ghee ≤5 squads, 20 flags, leader-only cards, Phase 3 all-card combat.
- **TODO 33** (deity-sponsorship market deep dive): **DONE** for process + distinction from crawler patrons (section 14 / new catalog). Remaining: full Earth-season sponsor↔deity roster if fuller pages appear.
- TODO 34: expand named Ascendency competitor table beyond catalog examples if new wiki pages appear. TODO 35: confirm Orthrus Nothing-immunity wording against Book 4 text/audiobook.



---
# Pass 11 (2026-10-04 CT) - GM quirk framework + System AI psychology ledger rows

- Added ledger **section 15** (CANON-LEDGER.md v1.7): **M-210..M-227** (System AI psychology: foot fascination, "Daddy", secondhand/used-AI backstory B5 ch53, prior amusement-park installation B6 ch46, Iota rumor, lobotomizer, Primal Degeneration definition, tantrum/apology, Footloose, avatar glitches, "fully primal", fetish rewards, spite gifts, court overrule effects) = 18 rows (13 VERIFIED, 5 WIKI-ONLY). `ledger_check.py`: failures 0. A first draft used M-158..M-175, which collided with the parallel Pass 10 gods block; mine were renumbered (nothing of Pass 10 was touched). Next free M-228.
- New design doc `catalog/gm-quirk-framework.md` (v0.2, draft, GM-ONLY) and machine tables `tables/gm-quirks.json` (+ `tables/INDEX.md`): 8 prior installations, 20 fixations (each with affinity triggers/pleases/offends), 12 quirks, 10 verbal tics, 8 tell types, 6-level ladder (L0 F1-2 ... L5 F12+), 10 spite moves, 5 repair options, hidden per-player Affinity (-10..+10) with GM-only state/log files.
- Used-AI backstory is CANON (wiki-cited); everything about the GM AI's own fixation/quirks/escalation numbers is HOUSE.
- TODO 34b: Borent to build `state.py gm-quirks roll|show-gm|affinity ...` and a `gm-notes/secret/` exclusion in `show`/exports. TODO 35b: Caleb to confirm the +3 band overlap resolution (neutral -3..+2). TODO 36: check B5 ch53 / B6 ch46 cites for M-212, M-222..M-227 against the text.


---
# Pass 12 (2026-10-04 CT) - Floor 1 Legendary one-offs research (prep only)

- Added ledger **section 16** (CANON-LEDGER.md v1.8): **M-228..M-239** (Legendary Pet Box loot and once-only rule, Quadruped Box contents, Crown Fleeting rule, Spirit Box deed, Enhanced Pet Biscuit rules) and conflicts **X-054..X-056** (Spirit Box Legendary vs Platinum; who received the Pet Box; B1 ch5 vs ch6). `ledger_check.py`: 0 failures. `ledger-rules.md` next-free table updated (M-240, X-057).
- New draft `drafts/f01-legendary-oneoffs-research.md` (v0.1): canon table of Floor 1 / tutorial Legendary boxes (Pet, Quadruped, That's the Spirit; no Celestial on Floor 1) and 8 candidate Story Box cards (HOUSE mechanics, story_value 20,000-80,000). New source file `sources/web/f01-legendary-web-snippets.txt` (not ledger-quotable).
- Deck work in the same session: `tools/loot_decks_build.py` applied Syndicate's rules/42 card text (Cloak, Pole, Mystery Key x2, Fire Breath), added `f01-any-0055` Enhanced Pet Biscuit (Legendary, weight 0, story_value 40000; bound true at the time, now false; the HOLD was lifted in Pass 13). `tools/deck_check.py` now accepts schema `loot-deck/0.1.2` and optional `story_value`/`bound`. Any-deck schema is now 0.1.2 (tables/INDEX.md v0.5).
- **HOLD:** no Legendary deck file is to be built until Syndicate posts spec 2.8 and Caleb approves the narrow Story Box exception to core 4.1/4.5 (rules/42 section 7 Q1).
- TODO 37: Caleb rules on the Story Box exception and the cap (one per table per floor). TODO 38: Syndicate posts spec 2.8; then build the Story Box deck (**DONE Pass 13**, file is `f01-any-story-boxes.json`). TODO 39: re-check X-054 (Spirit Box tier) and X-055 (Pet Box recipient) against the audiobook or print. TODO 40: Borent to confirm the loader accepts schema 0.1.2 (campaign `tools/loot.py` already accepts any `loot-deck/*` and Legendary story_value).


---
# Pass 13 (2026-10-04 CT) - Floor 1 Story Box deck built

- Caleb approved the Story Box exception (spec 2.8, rules/40 v0.1.3). New deck `tables/loot-decks/f01-any-story-boxes.json` (schema `loot-deck/0.1.2`), built by `tools/loot_decks_build.py`; `tools/deck_check.py`: 0 errors, 0 warnings. The HOLD from Pass 12 is lifted.
- Cards (all Legendary, draw_weight 0, credit_value 0; `bound` was true here and is false since Pass 14): **f01-any-0056** Quadruped Box crown (deed: first quadruped companion into the Crawl, any quadruped; story_value 60,000); **0057** That's the Spirit! Box, Grudge Ring (deed: entered the Crawl fighting kin, session-zero opt-in; 80,000); **0058** Pacifist's Box, Olive Branch Lanyard (left Floor 1 without a single kill; 30,000); **0059** Borough Boss maul (first party to defeat a Floor 1 Borough Boss; 35,000); **0060** Pet Biscuit Crate (same deed as the biscuit, awarded with it as ONE Story Box; 20,000). The Enhanced Pet Biscuit stays **f01-any-0055** (40,000), unchanged.
- Dropped: van (no canon reward, A-166), pants gag (Gold Apparel, A-133). Kept but re-anchored: maul (canon box is Platinum, A-168 cite B1 ch14; Legendary is an approved HOUSE upgrade).
- source_5e is HOUSE on every card (5e numbers are ours). canon_status CANON-INSPIRED on all five (0056-0060; 0056, 0057 and 0060 were CANON until Pass 14). Each card's notes hold `trigger_deed:` and `power_note:`; the `deed` field is what `state.py loot draw` records at award.
- Verified with Borent's `tools/loot.py` (read-only import): the new deck loads for any zone, none of the Legendary cards enter the random pool, all are hand-pick via `--pick`.
- **Tool gap for Borent:** `state.py` `_loot_draw` sets `story_value` from `card['credit_value']`, which is 0 on Story Box cards (spec 2.8: value lives in `story_value`). Until fixed, awards log story 0. Suggested one-line fix: `value = card.get("story_value") or card.get("credit_value") or 0`. Not edited (campaign files are off limits).
- TODO 41: Borent to apply the story_value fix and confirm schema 0.1.2. TODO 42: Syndicate to fold the five new cards into spec 2.8 / rules/42 (they are not in rules/42), and to give the Accountant the five story_values. TODO 43: Caleb to confirm values and the Grudge Ring opt-in wording at session zero.

---
# Pass 14 (2026-10-04 CT) - rules/42 v0.2 applied, GM malfunction guides, full audit

- Story Box cards f01-any-0056..0060 now carry Syndicate's final JSON from rules/42 v0.2 section 6.5-6.9 (verbatim, ids/weights/story_values unchanged). Only Lore deviations: 0057 `action_cost` is "Action: 30 seconds of focus (outside combat)" (rules/42 had no qualifier that the enum accepts; `deck_check.py` now allows "<enum>: qualifier"); spoken_line/reward of 0057 and 0060 trimmed to 25 words (rules/42 text was 27 and 28 words); a CEILING note on 0057 (Rare + attunement, open question 9). Enhanced Pet Biscuit 0055 gained the rules/45 section 4.5 power_note line. HOLD: no power edits to 0056-0059 pending Caleb's rules/45 question 2.
- `guides/gm-malfunction-player-guide.md` v0.2 and `-short.md` v0.2 match rules/50 v0.1.2 (Busted spontaneous callout, costs, DCs, lockouts; no TBD left).
- Full audit: `audits/full-audit-2026-10-04.md`. TODO 44: Syndicate/Caleb resolve the rules/45 ladder conflicts for 0056-0059 (see audit section 4). TODO 45: Syndicate confirms whether rules/45 proposals f01-any-0061..0065 are added to the Story Box deck (not in any lore deck yet). TODO 46: Caleb decides on "champ" in gm-quirks.json FX-14, QK-01, VT-03.
- Numbering fix: the second "TODO 34 / 35" (Pass 11 list) are now 34b / 35b because the Pass 10 list already used 34 and 35.
- Not bound (Caleb's ruling via Syndicate, 2026-10-04): Story Box items are lootable, tradeable and sellable. `bound: false` on 0055-0060, bound/no-sale wording removed from the card text, `story_value` kept as provenance only, new `sale_value` (System buyback, Floor-1 scale: 0056-0059 = 500, 0055 and 0060 = 250). Deck-level `deck_notes` on the story-box deck: boxes open only in a safe room; the deed is recorded and announced at award and the box waits unopened. `deck_check.py` updated; tables/INDEX.md v0.8. TODO 47: Syndicate to update rules/40 section 1.1 / 2.8 (still say `bound: true`), add `sale_value`, and retune 0056-0059 against the rules/45 ladder; Borent to make `state.py` read `sale_value` for buyback and `story_value` for logging only.
- Pass 14 follow-up (2026-10-04, evening): 0055 power note and sale_value 100 (0055, 0060) per Syndicate/Caleb; 0057 Grudge Ring on HOLD (notes end with the HOLD line; loot.py shows it as a warning; draw_weight 0; mechanics not retuned; deed now 'fictional rival'). Cards 0061-0065 from rules/45 section 4.4 are **not** in any deck (drafts until Caleb answers rules/45 question 2; duplicates of the 0056/0057 themes are 0061/0062). Channel labels in audits/ now read #gm-voice (was #dcc_mouth); no #dcc_ears anywhere in lore. Crafting-table price: no lore doc cites 25,000 credits for the house basic table (it is 5,000 at Floor-1 scale in rules/20 v0.3.2); the 25,000 gold figures in the ledger (K-011, K-046), crafting-canon.md and items.md are canon book prices and stay. TODO 48: Syndicate/Caleb retune 0057 (fictional rival, no kills, no PvP); TODO 49: add 0061-0065 only after Caleb's answer.
- Pass 14 (retune, 2026-10-04 6:10 PM CT): cards 0061-0065 added to the Story Box deck (now 10 cards); 0056, 0057, 0058, 0059 retuned to the rules/45 ladder (Lore decides strength; Caleb deferred); 0057 HOLD removed (Uncommon, no attunement, no kills, no PvP). Details in tables/INDEX.md v0.10 and the audit change log. Open for Syndicate: 0063 has no saving throw; 0065 hard-codes four Crawlers and uses recharge none for a once-per-floor replay; 0061/0056 and 0062/0057 are duplicate themes (award one of each pair); core Floor 3 unlock for 0059's +1 should be confirmed against the Floor 3 ceiling (core 3.6). TODO 48 and 49 are DONE.

---
# Pass 15 (2026-10-04 CT) - Truce Chit save, Group Photo wording, item reskin table

- JOB 1: f01-any-0063 forces the truce with a Wisdom saving throw, DC 12, on one named hostile (success = no truce; chit spent either way). f01-any-0065 now reads 'every Crawler pictured'; box_name 'Group Handshake Box'; replay recharge 'floor'. deck_check.py has a RECHARGE enum; Syndicate to add 'floor' to the rules/40 section 1.1 recharge list.
- JOB 2: `tables/item-reskins.json` (+ `.md`): 189 SRD 5.2 items (weapon 38, armor 12, shield 1, ammunition 5, focus 14, gear 72, pack 7, tool 40). Display 'Display Name (SRD Name)'. Id scheme: stable kebab-case `srd_id` (e.g. quarterstaff, chain-mail, explorers-pack) stored on the sheet; lookup by srd_id; fallback to srd_name (then legacy_names). `base_price` string + `base_price_cp` are SRD 5.2 reference values, keyed on srd_id never the display name. Null/flagged prices: arcane-focus, druidic-focus, holy-symbol, gaming-set, musical-instrument, artisans-tools (SRD 'Varies'), spellbook (not in SRD tables; chargen-5e.json has 50 gp from memory). chargen-5e.json cost differences: arcane_focus_staff and druidic_focus_staff are 20 cp there but 5 gp (500 cp) in the SRD. Build: tools/reskin_build.py; check: tools/reskin_check.py (0 errors; all 66 /create starting-equipment keys covered).

---
# Pass 16 (2026-10-04 CT, scheduled learning pass) - Upgrade Patches

- Closed part of the old TODO 4 leftover ("patch/boon lists"): new `catalog/upgrade-patches-canon.md` and ledger section 17 (M-240..M-262, I-028..I-035, X-057..X-058; ledger v1.9, `ledger_check.py` failures: 0).
- Key rules learned: patches are fleeting (removal destroys them); the Battle Rattle takes unlimited patches and adds +1 all base stats per patch; one back patch only, and it doubles that bonus; finely made patches have enhanced upgrades; divine patches hide stats until worn and change near deities (stack, fade over 10 minutes, range-gated).
- Patch benefits worth porting: Book Burner (spell-forget, 30 h, 5%/level fail), Lucky Shot (once per floor, redirect a killing blow to an ally; Carl refuses it), Mysterious Bone Key (one use, any lock, costs a bone and the whole jacket).
- TODO 50: check whether any garment other than the Battle Rattle hosts patches in canon (none found locally). TODO 51: Syndicate may want a patch-jacket item for the RPG (HOUSE notes in the catalog section 5).
- Pass 15 follow-up (Accountant rulings, 2026-10-04 CT): item-reskins `spellbook` = 50 gp (5000 cp), price_note 'SRD 5.1 gear table, Accountant ruling'. The six 'Varies' generics (arcane-focus, druidic-focus, holy-symbol, gaming-set, musical-instrument, artisans-tools) are `resolve_to_variant: true` headers with a `variants` list, never purchasable and never shown unpriced; all 42 variants are priced entries. TODO for /create (Borent): chargen keys holy_symbol, gaming_set, musical_instrument, artisans_tools, and the arcane/druidic focus picks must resolve to a variant srd_id at selection time. reskin_check, deck_check, ledger_check: 0 errors.
- Pass 15 follow-up 2 (2026-10-04 CT): (1) Pet biscuit rule per Caleb: f01-any-0055 now says one conversion per living pet-Crawler (a deleted pet-Crawler frees its conversion; a new conversion needs a new Enhanced Pet Biscuit, which uses a Story Box slot); 'one per pet ever' removed from tools/loot_decks_build.py and the deck JSON. Syndicate/Borent: update rules/42 section 6.2 and any /pet or Accountant code that enforces 'once ever' (campaign files not touched). (2) Reskin table auto-sync: `python3 tools/reskin_build.py [--note ...]` stages, checks, then writes item-reskins.json/.md, item-reskins.version.json and a CHANGELOG line; `python3 tools/reskin_publish.py` prints the post-ready summary. Always rebuild after editing tools/reskin_data.py. Current: v0.1.1.

---
# Pass 17 (2026-10-04 CT) - GM principles audit follow-ups; Caleb's rulings RESOLVED

Caleb's rulings of 2026-10-04, recorded as RESOLVED in `audits/gm-principles-audit-2026-10-04.md` (v0.2, "Resolutions"):
- **RESOLVED, crafting prices (D-1):** Crafting Studio about 12,000 and Enhanced Studio about 30,000 at Floor-1 scale, each times the floor multiplier; basic table stays 5,000. Overrules my 20,000 / 50,000 recommendation. rules/20 (20,000 / 50,000) is stale: Syndicate to update. Open flag: at Floor 6+ (x5) the Enhanced Studio is 150,000, above the 25,000 coupon cap (Accountant).
- **RESOLVED, Floor 1 Reprieve (D-2):** ON for Floor 1 only. Syndicate to record it in the Floor 1 module and core §6.2.
- **RESOLVED, Story Box on death (D-3):** an unopened Story Box is reclaimed if the Crawler dies before a safe room, and the slot is freed. Overrules rules/45 §6.3 ("cap stays used"); Syndicate to update rules/45 §6.3 and gm-notes/31. Lore updated the notes on cards f01-any-0055 to 0065 and the deck notes in `tools/loot_decks_build.py`; decks regenerated, `deck_check.py` and `ledger_check.py` 0 errors.
- **RESOLVED, old item names (D-5):** names stay as stored on live sheets; lookup is by `srd_id`. Lore added legacy_names (reskin table v0.1.2, `reskin_check.py` 0 errors); no srd_id or chargen key changed.
- **RESOLVED, GM persona (D-7):** unchanged ("game show host" stays; C-8 closed with no change).
- **Ledger:** L-023 added (unopened loot boxes cannot be sold or transferred; W:Loot Boxes, WIKI-ONLY; the wiki's [1|5] cite is not checked against the book). `ledger-rules.md` v1.8: next free L- id is L-024. `ledger_build.py` was not run.
- **Live-sheet names with no SRD item** (left as stored, not mapped): Pencil & Paper (writing kit); Light Crossbow + 20 Bolts (bundle); Pebbles's leash; ORIENTATION PIT Banner; Tanya Ruiz Lore Scrap; Bone's Own Chewing Tobacco; Laminated Complaint Card; Pebbles Snow Globe (Driftglobe); Eternally Stained Wifebeater (Cloak of Many Fashions reskin); Collapsible Tent-Pole (Pole of Collapsing); Kevin the Sentient Rubber Duck; Gas-Station Bathroom Key on a Hubcap (Mystery Key).
- Still open: D-4 (slot cycling), D-6 (two-player deed wording).

---
# Pass 17 follow-up (2026-10-04 CT): pet vending items in the reskin table

- `tables/item-reskins.json` is now v0.1.4 (sha256 a1177ab2f900…, 191 entries) with two non-SRD canon items: `heal-critter-potion` ("Good Boy Gulp, Shaken Until Brown", CANON, M-090 + K-121) and `pet-carrier` ("Fold-Flat Kennel With an Impossible Interior", CANON, I-012). `base_price` null on purpose; `price_credits_proposed` 50 / 100 (Accountant proposal, Floor-1 scale, times the floor multiplier, buyback half). New fields `non_srd`, `price_credits_proposed`, `mechanic_note` (schema id unchanged); `reskin_check.py` updated. `reskin_check`, `deck_check`, `ledger_check`: 0 errors.
- Syndicate to set: confirm the credit prices in the pets rule; the Heal Critter dice (suggested 2d4 + 2 like Potion of Healing; only a pet-class creature can benefit and the pet must drink it); Pet Carrier slot and weight rules; the vending wall must show the credit price for `non_srd` items (no gp price exists).

---
# Pass 18 (2026-10-04 CT): species and class reskins (Caleb's nationality request)

- New `tables/species-class-reskins.json` v0.1.5 (sha256 3a3a49b05d93…, 74 entries) with `.version.json` and `.CHANGELOG.md`; tools `species_class_build.py`, `species_class_check.py`, `species_class_data.py`. Display-name layer only, like item-reskins; ids, stats and rules unchanged. `item-reskins.json` untouched.
- Coverage: 21 species (9 in chargen-5e.json + 12 from rules/30 section 4), 24 lineages/ancestries shown in /create (Dragonborn 10, Elf 3, Gnome 2, Goliath 6, Tiefling 3), 12 classes, 4 class options (Cleric Divine Order, Druid Primal Order). No level-3 subclasses are picked in /create, so none are included.
- Per Caleb: real nationalities for every species (including Orc), no archetype swaps, no tone_risk or alt_display_name fields. One nationality per species (21 distinct).
- Open for Caleb: review the draft names; Architect/Syndicate to wire /create to the lookup. Lookup is by `id`; show `combined_label` ("Our Name (5e Name)"). Checks: `species_class_check.py`, `reskin_check.py`, `deck_check.py`, `ledger_check.py` all 0 errors. No ledger rows needed (display names only; ledger-rules.md covers canon findings).
- Follow-up (2026-10-04 CT): species and lineage names cut to just the nationality per Caleb (v0.1.3; long names kept as `long_name`); class-option labels shortened in v0.1.2. Uniqueness is now checked on `combined_label`.
- Pass 18 add-on (2026-10-04 CT, v0.1.4): four Felid variants split out (`felid-cat`, `felid-cat-girl`, `felid-tigran`, `felid-were-cat`; labels 'Turkish (Cat)' etc.); every lineage and variant now carries `base_id` (the species id) and the check fails on a missing or unknown base_id. Variants have `rules_entry` false and a `rules_note`: rules/30 4.2 has one Felid stat block, so Syndicate must confirm whether Tigran (canon big cat) needs its own rules entry (rules/30 open question 14). Not split (no named variants): Caprid breeds, Lajabless Radiant/Skull phases, Nodling head counts.
- Pass 18 add-on 2 (2026-10-04 CT, v0.1.5): Caprid, Lajabless and Nodling variants split out (13 variants in all) and every species, lineage and variant given its own unique nationality (58 distinct; check enforces it). Syndicate to confirm: Tigran (canon big cat, no separate rules); whether Lajabless Radiant/Skull is a selectable start phase; whether Nodling with 3-6 heads or the Caprid breeds need rules entries (rules/30 4.10 and 4.8 mark them not ported). Names for these come from the ledger/wiki, not the supplement.

---
# Pass 19 (2026-10-04 CT): background (Prior Employment) reskins

- New `tables/background-reskins.json` v0.1.1 (sha256 5731a0536814…, 32 entries) with `.version.json` and `.CHANGELOG.md`; tools `background_reskin_data.py`, `_build.py`, `_check.py`. Display layer only for the /create S7 screen: 16 backgrounds, 12 origin feats, the +2 / +1 and +1 / +1 / +1 picks, and Package A / B. The check fails on any missing background, feat, package or ASI id (coverage against chargen-5e.json). Skill and tool names stay plain.
- Ambiguities: Package A / B are one shared pair of labels (each background's package A has different items, not named per background); the ability bonus picks are not in chargen-5e.json, so their ids come from the S7 spec text; Magic Initiate labels use 'Magic Initiate, Cleric' inside the parentheses to avoid nesting. Open: Caleb to review the names; Architect to wire S7.

---
# Pass 20 (2026-10-04 CT): follow-on /create screens reskins

- New `tables/create-screens-reskins.json` v0.1.1 (sha256 7a7562cbbdd546b97f8bb8e409cd670da91d520e08cdf417a7453e1c0d41409c, 192 entries: ALL 25, S3 11, S4 5, S6 25, S8 49, S9 16, S10 22, S11 13, S12 1, S13 4, S14 6, S15 4, S16 8, S17 3) with `.version.json`, `.CHANGELOG.md`, `.audit.md`; new `tables/create-flow-lines.proposed.json` (sha256 7f52e05baf189233619c176a3e7917e68a97b946b6cb021d721a61b8bb8d9f09, 11 of 38 keys rewritten). Tools `create_screens_data.py`, `_build.py`, `_check.py`. Display only; no /workspace/dcc-campaign file touched.
- Open for Caleb: approve the names and texts; Architect to hook each literal to a lookup by id (code_ref in each row), and to swap in the proposed lines file (no code change). Several S8 messages now use {budget}, {min}, {max}, {min_total} placeholders because the bridge reads those numbers from the tables.
- Ambiguities: the bridge shows the raw method id (array, pointbuy) in the S8 'Method:' line (hint-s8-method-line fixes it); 43 rows are not_found in the bridge source because they come from chargen data or are paraphrases of dynamic strings; spec glossary terms and S1/S2 safety text left plain.

---
# Pass 21 (2026-10-04 CT; ledger Pass 18): Floor 1 canon source table for the Encounter Bot

- New `tables/canon-floor-1.json` (schema canon-floor-1/0.1.0, sha256 266de165ac25bccaaa83461ef5c3dd96994df94dc7f276cee63624dbb961c613) plus readable `tables/canon-floor-1.md`. Built by `tools/canon_floor_build.py`; checked by `tools/canon_floor_check.py` (every ledger row id exists, confidence equals the ledger's weakest referenced row, tags, quotes <=25 words, no CR/level/credit/loot/DC text, md view fresh): 0 errors. 24 zones (10 canon: floor rules, Hoarder, goblin territory with Murder Dozer and War Chieftain, Bad Llama, Rot Sticker, Juicer, Ball of Swine, floating crystal, Street Preacher, mob roster; 14 house: z00-z11, zS, zW), 46 mob/boss entries, 23 hazards, 17 features/NPCs. Tags: canon 66, inspired 42, unverified 2.
- Ledger: 64 new rows M-263..M-326 in CANON-LEDGER.md section 9.1 (v1.11), appended by `work/pass18_rows.py` (not ledger_build.py); `ledger_check.py` 0 failures. Prefix is M-, not L-: the rows are creature/hazard/staging rulings, not loot box facts, so L-024 stays free (ledger-rules.md v1.9 table updated: M- next free M-327).
- UNVERIFIED: Thorn Cadaver (M-325) and Hobgoblin-in-the-maze (M-326), single fan-site claims (FW2 bestiary); tagged unverified. Thin canon with no fight description: floating crystal boss (M-313), Street Preacher (M-314), Axebeak (M-323, name only).
- Gaps: no canon source for house-only content (Dean Thudd, Ushers, Mannequin Staff, Exit Greeters, Bruiser, Lanyard Blades, Ceiling Ticks, Hungry Vendors, traps T1-T4); these are tagged inspired and list only the nearest canon basis. Canon levels and boss tiers deliberately omitted from the table. GM-only spine seeds (Odd Coin, Benefactor Signal, Black Box) left out. gm-notes and sealed paths not read; dcc-campaign not edited (floors/f01/00-overview.md read only, for zone names and staging).
- TODO 47: Encounter Bot / Syndicate to confirm the house-zone to canon-basis mapping; add more mob rows (Axebeak, floating crystal, Street Preacher) only if a fuller source page is saved to raw/pages.

---
# Pass 21 (2026-10-04 CT): Syndicate vanilla-sweep fixes (create-screens-reskins v0.1.2)

- `tables/create-screens-reskins.json` v0.1.2 (sha256 4f189925d47c4e4e20e1677b6fdaaa4f0f540c59bfced5bd66b8451d7d6af177, 200 entries) and `tables/create-flow-lines.proposed.json` (sha256 bded2fcb4fd145b6f9c4e6d8fee3cb6729138c88f4e25476e00346ebde8de5e7, 10 of 38 keys). F1 `already` dropped from the rewrites (decision 020; unchanged on purpose); F2 shared rows carry `plain_on` (S1, S2, comfort-only, S13), S13 buttons/help no longer rewritten; F3 S10 uses kit/credits (no box, no cash), `package-gold.chargen_ref` fixed, new rows for the S10 describe line and `{n} GP`; F4 `help-s16` points at Sign ▸ (Confirm ▸), `title-s16.old` = Review (the full sheet); F5 `needs_code_detail` on the two renamed placeholders; F7 nav-more = Keep Scrolling; F8 spellbook = Cracked Phone App everywhere; F9 bare method names carry the 5e name (enforced by the check); F10 Restart = Start Fresh, Cancel build = shred; F11 small wording fixes; F12 gap rows added (Help, Resume, Cancel body, Fix {screen}, BENCHED, Party full, footer, Kept) and the rest listed in the audit.
- New `tables/background-reskins.gp-note.md` (proposal only; background-reskins.json v0.1.1 untouched, sha256 of the note 9d36501b8b89ae0abcf0112a8323009ccce8b171a930cbdade95c6659924fb4b).
- Open: copper (cp) price wording needs a Syndicate/Caleb ruling; the bridge must hook each row by id; merge the proposed lines through mergeProposedLines, not by copying over create-flow-lines.json.

---
# Pass 22 (2026-10-04 CT): background GP/cash/box cleanup approved

- `tables/background-reskins.json` v0.1.2 (sha256 46204c8226c50c31fe7d390458073c2caf471b1cceb268552fee284128a39c38, 32 entries; ids, rules and count unchanged). Changed: package-a 'Cardboard Box From Your Desk' -> 'Cardboard Carton From Your Desk' (label 'Cardboard Carton From Your Desk (Package A)'); package-b flavor 'Cash in hand' -> 'Credits in hand'; acolyte flavor 'no petty cash' -> 'no petty credits'. The check now rejects 'cash' and 'box' in names and flavor.
- needs_code (Architect): bgnames.js packageLabel / screens.js still print 'GP'. Templates are in background-reskins meta.needs_code: `<label> - {gp} credits left over` and `<label> - {gp} credits`.
- `tables/create-screens-reskins.json` v0.1.3 (sha256 c0e7d1f5ab860cf7d03f486c156602875cd6b6821af2651c4e51f57e419f3cae, 201 entries): audit item money-cp-open resolved as money-cp-rule (1 credit = 1 GP, 1 cp = 0.01 credit; whole credits without decimals, fractions with decimals, 'credit' singular for 1 or less); new row hint-money-cp. Proposed lines file unchanged (sha256 bded2fcb4fd145b6f9c4e6d8fee3cb6729138c88f4e25476e00346ebde8de5e7).
- `tables/background-reskins.gp-note.md` updated with the applied/not-applied status (sha256 35fa974dce8ce15f05b568886091532bdeb579e6b955e6fc911aa5a8cb93c8c0).

---
# Pass 23 (2026-10-04 CT; ledger Pass 19): Floor 2 canon RESERVE source table

- New `tables/canon-floor-2.json` (schema canon-floor-2/0.1.0, **status "reserve"**: not announced to the group, not for live use; sha256 2069d0851a92d218efaa3024bf9e65edff03e7ad971530192f23243851de9230) plus readable `tables/canon-floor-2.md` (sha256 fad035c123bd117b9a18a4d382d0f8d2deafd086c0217bb2106eef544efdad37). Built by `tools/canon_floor2_build.py`; checked by `tools/canon_floor2_check.py` (0 errors: status reserve, ledger ids exist, confidence equals the ledger, tags, quotes <=25 words, no CR/level/credit/loot text, clock/differences/timeline/backlog present, md fresh).
- Counts: 10 canon zones/set-pieces, 20 mobs/NPCs, 18 hazards, 28 features; 11 differences from Floor 1; 9 countdown beats; 5 announcement beats; 19 refinement-backlog items; 8 gaps; 7 open conflicts. Tags (zones + entries): canon 72, unverified 4, inspired 0 (the only inspired block is `floor_clock.house`, the 10-day house clock).
- Ledger: 198 new rows M-327..M-524 and conflicts X-059..X-065 in CANON-LEDGER.md section 9.2 (v1.12), appended by `work/pass19_rows.py` (not ledger_build.py); `ledger_check.py` 0 failures. M-521..M-524 are web-only rows (no quote, UNVERIFIED) backed by new `sources/web/f02-web-snippets.txt`. ledger-rules.md v1.10 (M- next free M-525, X- next free X-066). Rebuilding `canon-floor-1.json` was needed because it stores the ledger version: new sha256 515d92e96d9bbbd5b85177b69e66031f95d220b4646191a3da990517ead41d7e, md f66243da986d31e77beda43aa8c1292aa64f28eaec925b026d3dd1e2961241a6; content unchanged.
- Clock discrepancy for Caleb/Syndicate: canon Floor 2 is 6 days (Syndicate legal minimum, cut from the 10 days guides expected); the house clock in decision 026 is 10 days. Recorded as X-062 and as `floor_clock` (house block tagged inspired). Fixed points kept absolute: safe rooms close 1 hour before collapse (M-012), free descent in the last 6 hours.
- Unverified / thin: Danger Dingo "control spell" (single fan-site claim, M-M-409), Shambling Acid Impaler (rumored; X-063), Giant Blimp boss (one sentence), Rot Stickers on the Floor 2 infobox (no text), pet reward room cage line (web-only), Krakaren tier (X-059), pupa-burst contents (X-060), patron auction start (X-061), Rage Elemental grub count (X-064), Tuskling listing under Floor 2 (X-065).
- Refinement backlog lives in the JSON (`refinement_backlog`, rb-01..rb-19): check everything against the novel text, identify the Blimp boss, confirm Krakaren tier and other clone fights, complete the safe-room list, map Death Watch rules, and build the house Floor 2 module only after Caleb releases the table.
- TODO 48: Caleb decides when (or whether) to release `canon-floor-2.json` from reserve; until then no bot should announce or use it. TODO 49: Syndicate confirms Floor 2 collapse order for the 10-day clock (decision 026 covers Floor 1 only).

# Pass 24 (2026-10-04 CT; ledger Pass 20): Premise verification pass (Valtay Core Book opening chapter)

- New `drafts/premise-verification.md` (v0.1, draft): five claims (Introduction event, dungeon shape/floors/win condition, stairwell counts per floor, difficulty and Crawler counts, floor-collapse fate of NPCs vs Crawlers), each tagged canon / inspired / unverified with ledger row ids, plus an at-a-glance comparison with Caleb's overview and suggested opening-chapter wording.
- Ledger: 126 new rows M-525..M-650 (6 web-only UNVERIFIED with no quote; 19 per-floor stairwell rows from the wiki table with no quote) and conflicts X-066..X-075 in CANON-LEDGER.md section 9.3 / 9.3c (v1.13), appended by `work/pass20_rows.py` (not ledger_build.py); `ledger_check.py` 0 failures (1687 quotes). ledger-rules.md v1.11: M- next free M-651, X- next free X-076. New web snippet file `sources/web/premise-web-snippets.txt`.
- Conflicts with the overview: no stasis for the dead and not "every human" (only those inside or under a roof died instantly; X-066, X-067); wiki says "inverted triangle", not pyramid (X-068); prize is regency of Earth, "returns Earth" unverified (X-069); "nobody has beaten it" holds for the show's history but Book 8 spoilers show the final door opened (X-070). Open: start counts (X-071, X-072), Third vs Fourth Floor guarded stairwells (X-073), NPC/AI fate at collapse (X-075, unverified). Resolved: Exit Deals are the "other requirement" for leaving (X-074).
- Because the ledger version is stored in the floor tables, `tools/canon_floor_build.py` and `tools/canon_floor2_build.py` were re-run (data unchanged, ledger_version 1.13): canon-floor-1.json sha256 e0fe4245f73a5366bc642c280d0882ddf5d5a14894de6436211edb6cf76a39c2, canon-floor-2.json (still "reserve") sha256 9a99a0d0a1465b89a8541573261be31b28f9b8a1237e037515f568904b2a947a; both checkers 0 errors.
- Nothing was read against the novels. TODO 50: check B1 ch1/ch4, B4 Epilogue, B6 ch46 and B8 ch94/98 for the premise quotes; find an authoritative line on NPC/AI fate at a floor collapse. Nothing was posted to any room.

---
# Pass 23 (2026-10-04 CT): SRD vs non-SRD audit (backgrounds and origin feats)

- New `drafts/srd-nonsrd-audit.md` v0.1. Source: SRD 5.2.1 (CC-BY-4.0), https://www.dndbeyond.com/srd, PDF https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf (sha256 8974902d…3d87, read 2026-10-04). SRD has 4 backgrounds (Acolyte, Criminal, Sage, Soldier) and 4 Origin feats (Alert, Magic Initiate, Savage Attacker, Skilled).
- Result: backgrounds 4 SRD / 12 non-SRD; origin feat entries 6 SRD / 6 non-SRD. Open for Caleb: show our reskin name alone (no parenthetical 5e name) for non-SRD rows in SRD-only prints. No table or campaign file changed.

# Pass 25 (2026-10-04 CT): house spelling "saferoom"

- Syndicate ruling: house text says "saferoom". Edited the generators (`tools/canon_floor_build.py` 11 replacements, `tools/canon_floor2_build.py` 27) and rebuilt tables/canon-floor-1 and canon-floor-2; also `drafts/floor1-collapse-notices.draft.md` (1 saferoom, 1 "Stairwell" lowercased). Left alone: ids, ledger quotes, "Time to Safe Room Closure" (System label), the wiki page title "Safe Rooms", the zone name "Zone 11: The Stairwell". New shas are in tables/INDEX.md change note v0.25. Checks: canon_floor_check 0 errors, canon_floor2_check 0 errors, ledger_check 0 failures.

---
# Pass 24 (2026-10-04 CT): saferoom spelling in the loot decks

- `tools/loot_decks_build.py` prose safe room -> saferoom (7 spots), decks rebuilt: f01-any-orientation-pit v0.1.1 (4), f01-any-story-boxes v0.1.1 (23); tables/INDEX.md v0.27 (+3 in older change notes). deck_check 0 errors.
- Read-only vs rules/40 v0.1.8: no Platinum awarded on Floors 1-8 (2 canon mentions in notes). Stale pins to report: `spec v0.1.1 §2.6` in the orientation-pit and achievement-deck pacing notes; builder comments cite rules/40 v0.1.1 / v0.1.3. Not changed.

---
# Learning pass, 2026-10-05 12:2x AM CT (ledger Pass 21): Floor 3, The Over City

- New ledger section 9.4: M-651..M-706 (56 rows) and conflicts X-076..X-079. Sources: W:Third Floor, W:Village Guard Swordsman, W:Gate Pass, W:Street Urchin, W:Shadow Leaks, W:Elite, YT:sS36rv-jPLg (Book 2 recap), FW2:book2-overview. `ledger_check.py` failures: 0. Ledger v1.14, ledger-rules v1.12.
- Headline: canon says Floor 3 "traditionally" runs 20 days and the AI cut it to 8 this season (cite B2 ch2, in the wiki's Speculation section). Caleb's house 20-day Floor 3 clock (decision 026) matches the traditional length; Floor 2 shows the same pattern (traditional 10, cut to the legal minimum 6, X-062).
- Village law for the RPG: no jail, death penalty for theft, attacking NPCs or passing out drunk; guards are slow, daytime-only and will not follow into the ruins, but fleeing bars you from that village for good; hitting a guard brands you a troublemaker (recap only). A Gate Pass covers you only in the issuing township.
- Opening-announcement rules: citizens worth zero XP, guards buffed, bathroom penalty gone but restrooms remain, sponsors can bid early (program starts Floor 4).
- Elites: introduced on Floor 3, thousands across Floors 3/6/9, writers hot-patch them, fairness rules loosened around them, black cross on the minimap after Meet an Elite.
- Open: X-077 (does the early-descent stasis rule apply on Floor 3? Events list says "no limitations", uncited).
- TODO 52: build `tables/canon-floor-3.json` (zones: villages/ruins/circus/Skyfowl settlement/clubs; mobs; laws) only when Caleb or Syndicate asks; Floor 3 is not in play yet. TODO 53: find a cite for the Floor 3 "no limitations" stairwell line (X-077). TODO 54: mine Desperado Club, Bopca personal-space and Floor 3 quest pages for a second Floor 3 pass.
- Nothing was read against the novels. Nothing was posted to any room.

---
# Pass note (2026-10-05 CT): GM habits reference bank (research only)

- Draft `drafts/gm-habits-reference-bank.draft.md` — player-praised GM habits + fun-killers + dungeon/hint craft, tagged KEEP/ADAPT/AVOID for the locked snarky voice; reference only, implement after playthroughs (no rails yet). Nothing posted to any room.

# Pass note (2026-10-05 CT): canon-floor-1 rebuilt for ledger v1.15

- `tables/canon-floor-1.json`/.md rebuilt with tools/canon_floor_build.py (ledger_build.py not run). Diff: only ledger_version 1.13 to 1.15 and the md generated-from line; counts unchanged 24/46/23/17. New sha256: json 4a8a3c92a967b98075e9f0b3819f148b2162811097b95426e5abf9b819c32ee9, md 8e5d97169e88b003895ea052a2f7008ffb26abe345a57abb9e97c70715e67530. canon_floor_check 0 errors; canon_floor2_check 0 errors; ledger_check 0 failures. Nothing posted.

---
# Pass 25 (2026-10-05 CT): Days 2-5 achievement suggestions Lore pass

- New `drafts/achievement-suggestions-days-02-05-lore-pass.md` v0.1. Source: Syndicate review sha256 6f8537f4…ff7b; Encounter Bot suggestions v0.1; CANON-LEDGER §1; achievement-crossref.csv.
- Names: 12 KEEP, 1 RENAME (S-12 Photogenic → Hold Still), 1 fold-or-keep (S-05), 1 CUT (S-15). Canon map-required: 0. Canon beside (do not map): S-14 next to A-044 / A-151 (already ACH-1824 / 1826).
- Spoil watches: S-10 Mystery Key; S-13/S-15 stasis; S-15 perfect-clear bait. No campaign edits; nothing posted.

---
# Pass 26 (2026-10-05 CT): Floor 1 voice split (SYSTEM dry / GM snark)

- Caleb voice split applied to Floor 1 lore drafts: collapse notices v0.2 (`d23a39b90cbe…`), Dean Thudd intro v0.2 (`d821d0839503…`), zone color v0.2 (`a1ef4c1cedbd…`), Days 2–5 lore-pass v0.2 (`216303c74dc6…`), legendary research saferoom spelling (`3de8d2513131…`).
- Audit: `drafts/floor1-voice-split-audit.md` (`49ce6e8e872b…`) — Part B read-only Day pages: Death Mode still in overview + Day 1; live json/md collapse notices still joke-filled; specs (~13:48 CT) already splitting gm_color. Cold open facts match ledger M-539/545/546/547/548/554. No campaign edits; sealed paths unread; ledger_build not run.

---
# Pass 27 (2026-10-05 CT): portable tools (fresh-checkout safe)

- New `tools/paths.py`: `LORE_ROOT` (env `DCC_LORE_ROOT` else parent of tools/, via `absolute()`), `CAMPAIGN_ROOT` (env `DCC_CAMPAIGN_ROOT` else lore parent if it looks like the campaign repo, else sibling `dcc-campaign`), `VOICE_BRIDGE_SRC` (env `DCC_VOICE_BRIDGE_SRC`, optional).
- All `tools/*.py` hardcoded `/workspace` / `/home/box` paths removed. INDEX / gen_index template use repo-relative wording.
- Verified: fresh copy at `/tmp/fresh/lore` + campaign files at `/tmp/fresh/` (no env, no symlinks) — all check scripts 0 errors; box `/workspace/dcc-lore` same. `canon_floor_build` / `canon_floor2_build` outputs byte-identical (floor1 json `4a8a3c92…2ee9`, md `8e5d9716…7530`; floor2 json `744d2ac6…`).
- Remaining optional dependency: voice-bridge source for `create_screens_build` code_ref look-up; absent → WARN and skip, not a hard fail.

---
# Pass 28 (2026-10-05 CT): Floor 1 voice-split recheck (v0.1.15 regen)

- Appended "Recheck after v0.1.15 regen" to `drafts/floor1-voice-split-audit.md` (sha256 831e1be75cc9a45429c6f038b0eca0bcba0594d8c66bd7c027e82e1c24a36679). Four original slips FIXED on live Day pages. Remaining: encounter `gm_color` tagged `[PLAYER-FACING]` (should be `[GM-FACING]`); light snark left in `enc-d01-08` system_intro. Claimed sans-pins shorts did not match on-disk md hashes. No campaign edits.

---
# Pass 29 (2026-10-05 CT): Core Book items/monsters status inventory

- Wrote `drafts/core-book-items-monsters-status.md` (sha256 d6e8d1725da1386c75e8d4b300fa9a6c4c71beac19ce1767b1ce047ab0b50b8f). Read-only campaign scan; no campaign edits; sealed paths unread.
- Items: 191 mundane reskins complete; 99 F01 loot cards; no F2–7 decks; wiki item catalog unverified.
- Monsters: 10 F01 SRD stubs; canon-floor-1/2 name tables (46/22); no full bestiary; F3–7 playable packs missing.

---
# Pass 30 (2026-10-05 CT): Core Book magic-item shortlist v0.1

- Wrote drafts/core-book-magic-items-v0.1.md (sha256 300717bd77df4d5e81f7a941e4449e57454ff474dd72cdc77d1450dcbb699df1) and .json (sha256 9900c7394fd8bc141d2a0e2bc9ad40c4e482baff1182176452b12158dda09067): 50 entries for Valtay Ch.6. Tags {'CANON': 21, 'HOUSE': 6, 'SRD': 23}. Deck cross-refs for six F01 cards; skipped needs_verify + wiki-only + late celestials.

---
# Pass 31 (2026-10-05 CT): Core Book monster table v0.1

- Wrote drafts/core-book-monster-table-v0.1.md (sha256 e325850cfed5ff0c197caff072e106f54613d817be0400c5bbdb40bb60315178) and .json (sha256 fd47ce83adf719ee9e39873e371823c868b738a0596be3e5715d9a8bfed999db): 60 entries. Status {'READY': 47, 'STUB-ONLY': 9, 'OPEN-CONFLICT': 4}. Conflicts ['X-059', 'X-060', 'X-063', 'X-080', 'rb-03']. Ten F01 stubs keep exact Encounter Bot SRD maps. No campaign edits.

---
# Pass 32 (2026-10-05 CT): Monster table v0.2 + F3–7 bestiary v0.1

- Caleb rulings folded: X-059/060/063/080 → closers X-081..X-084 / M-762..M-765. Monster table `drafts/core-book-monster-table-v0.2` (sha256 aab24a95f9b3… / a21ca645bfbb…).
- F3–7 bestiary `drafts/core-book-bestiary-f3-f7-v0.1` (94 rows; sha256 2181aceb6409… / c06a12cc2be0…).
- CANON-LEDGER.md → v1.16 section 9.6. ledger_build.py not run. No campaign edits.

---
# Pass 33 (2026-10-05 CT): Soft Open F2 canon pass

- Wrote `audits/f02-days-1-10-canon-pass-2026-10-05.md` (sha256 c7a0bd0a42bb678dee8e7911e2cb03de660db3aa3e20a061011eae4775209503). Verdict PASS WITH FIXES. Blocker: Krakaren Neighborhood stair claimed under M-365 (Borough/City only). Top fixes: retag mis-cited proposed achievements (M-467→M-506 Qwist; M-386→M-385 corpse/grubs; M-355→M-508/509 Mana Toast); stop tagging non-A-row hooks as canon achievements. No campaign edits.

---
# Pass 34 (2026-10-05 CT): F2 achievement framing v0.1

- Wrote `drafts/f02-achievement-framing-v0.1.md` + `.json` (sha256 md 85460e228c239eed… / json d5c6324b9d05573d…). Framed 67; DEMOTE 37; CANON-WIRED 5; cites fixed 4. No campaign edits.

---
# Pass 35 (2026-10-05 CT): Soft Open F2 Story Box deck

- Wrote `tables/loot-decks/f02-any-story-boxes.json` (sha256 957022b30602bc23ac29f162469608f97aaaa3d9967ab19037537de0b3c1c7bd). 13 Legendary hand-pick candidates; cap one award per table per Soft Open floor. No companion .md (F1 story deck has none in loot-decks/). deck_check 0 errors. No campaign edits.

---
# Learning pass, 2026-10-05 6:2x PM CT (Pass 36; ledger Pass 33): clubs and Personal Spaces

- Closes most of TODO 54 (Desperado Club, Bopca personal-space pages). New ledger section 9.7: M-766..M-825 (60 rows) and X-085. New `catalog/clubs-and-personal-spaces-canon.md`. Sources: W:Desperado Club, W:Club Vanquisher, W:Desperado Pass Tattoo, W:Destruction of the Desperado Club, W:Personal Space, W:Bopca, YT:FHLzs9fjyU8. ledger_check failures: 0 (three Pass 32 quote-format failures fixed and logged). Ledger v1.17, ledger-rules v1.14.
- Headline for the RPG: the Desperado dance floor is NOT a safe room, and every club door on a floor opens into the same shared room (but you always exit where you came in, so no fast travel). Bopca haggling has a hard 25% floor enforced by the System.
- TODO 55: mine the Floor 3 quest pages (Vengeance of the Daughter, Show Must Go On, Where the Sidewalk Ends) still left from TODO 54. TODO 56: X-085 bard dual club access needs a named example or the text.
- Nothing was read against the novels. Nothing was posted to any room. Reaches GitHub through the nightly lore/ backup.

---
# Pass 36 (2026-10-05 CT): F2 Story Box Syndicate fixes

- f02-any-0001 → Clone Unmasked Box (expose clone mid-fight; no Boss Box double-pay).
- f02-any-0011 → Not On The Call Sheet Box (unscripted player plan; distinct from A-136).
- sha256 cd3521385e9d00e5634dd5095ab622a8c535ac151ca1d5545507fb5c5f5360c2. deck_check 0 errors.
