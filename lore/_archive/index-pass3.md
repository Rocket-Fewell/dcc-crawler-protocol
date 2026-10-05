# DCC Lore Knowledge Base - INDEX (Pass 1 written Oct 3, 2026 CT; extended by Pass 2 same day - see "Pass 2" sections below)
Owner: DCC Lore | Status: final | Version: 1.0 | Updated: 2026-10-03
Summary: Retired copy of INDEX.md as it stood after Pass 3; its content lives on in status-and-todo.md.

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
4. Loot-box drop tables, crafting/Midnight Market, Prize Carousel, Unwashed/Blood Hunters - **PARTIAL** (box tiers, Celestial rules, sample loot per box page; no drop tables exist in canon; Prize Carousel only in Book 3 notes). Crafting/Midnight Market/Hunters not done.
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
