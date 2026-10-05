# Canon Ledger Rules
Owner: DCC Lore | Status: review | Version: 1.11 | Updated: 2026-10-04
Summary: How every future pass must append to CANON-LEDGER.md: one dated entry per finding, with an exact quote and a source tag.

The ledger is `CANON-LEDGER.md` in this folder (reachable as `lore/CANON-LEDGER.md` from the campaign workspace). It is the master "hard memory" of DCC canon. This file is the full procedure; section 0 of the ledger is the short version.

## 1. Core rule: append, never rewrite
1. Future passes **append** to the ledger. They do not rebuild it, reorder it or renumber it.
2. **Every finding gets its own entry** (one table row) containing:
   - **ID**: the next free number for that section's prefix (table below). IDs are permanent.
   - **Quote**: exact text in straight double quotes, **at most 25 words**, copied from a local source file.
     - It must be an exact substring of that file once chapter cites such as `[1|5]` and extra whitespace are normalised.
     - A leading or trailing `…` marks trimming.
     - Escape a literal pipe as `\|`.
     - If there is no usable quote, write `— (none captured)`. The entry then cannot be VERIFIED.
   - **Source tag**: `W:<page>` (`raw/pages/<page>.txt`), `FW2:<file>` (`sources/fanwiki/`), `NL:<file>` (`sources/nl/`), `YT:<id>` (`sources/youtube/<id>.txt`). Use the tag of the file the quote came from, in the same row.
   - **Confidence**: VERIFIED, WIKI-ONLY or UNVERIFIED (section 3).
   - **Date**: `YYYY-MM-DD` the entry was added (America/Chicago).
3. New entries go **below the `APPEND-ONLY` marker in section 9** (use the same column layout as the matching section table) **or** at the end of the matching section's table. Either way, add one line to the **Pass log**: date, pass number, who, summary.
4. **Never delete or silently edit an entry.** To correct one, append a new entry that references the old ID and add an `X-` conflict row. If the whole ledger must be replaced, move the old copy to `_archive/canon-ledger-v<version>.md` and bump the header Version.
5. After appending, bump the header `Updated:` date. Bump `Version` (minor for appends, major for restructuring).
6. Run `python3 tools/ledger_check.py` from the lore folder. It must report `failures: 0`. Fix any quote it rejects.
7. **Do not re-run `tools/ledger_build.py` over a ledger that has had manual appends.** It writes to `work/ledger-rebuild.md` by default. Only pass `CANON-LEDGER.md` as the output path for the initial build.

## 2. ID prefixes and the next free ID (as of 2026-10-04, Pass 20)
| Prefix | Section | Last used | Next free |
|---|---|---|---|
| A- | 1 Achievements | A-190 | A-191 |
| M- | 2 Mechanics rulings (also sec 13–17 process; sec 9.1 Floor 1 creatures/hazards; sec 9.2 Floor 2 rules/creatures/NPCs; sec 9.3 premise verification) | M-650 | M-651 |
| L- | 3 Loot box facts (also sec 13 examples) | L-023 (L-023 sits in sec 3 after L-020; L-021..L-022 are in sec 13) | L-024 |
| L-B | 3b Loot box type index | (see table) | L-B76 (L-B01..L-B75 used) |
| S- / P- / I- / C- / R- | 4a Skills / 4b Spells / 4c Items (I- also sec 13–14) / 4d Classes (C- also sec 12) / 4e Races (R- also sec 11) | S-018 / P-016 / I-035 / C-050 / R-081 | S-019 / P-017 / I-036 / C-051 / R-082 |
| B- | 5 Bosses | B-030 | B-031 |
| H- | 6 Characters (also sec 13–14 examples) | H-057 | H-058 |
| T- | 7 Plot beats (also sec 13–14 examples) | T-073 | T-074 |
| X- | 8 Conflicts / Unverified (X-054..X-056 live in sec 16.1, X-057..X-058 in sec 17.3, X-059..X-065 in sec 9.2c, X-066..X-075 in sec 9.3c) | X-075 (X-A01..X-A21 are generated flags) | X-076 |
| K- (and X-C for crafting conflicts) | 10 Crafting | K-187 (X-C12) | K-188 (X-C13) |
| R- (11.1 process, 11.2 per race) | 11 Races and Floor 3 race selection | R-081 | R-082 |
| C- (12.1 process, 12.2 examples) | 12 Classes and Floor 3/6/9 class selection | C-050 | C-051 |
| M- (13.1–13.4 process; examples H/I/L/T) | 13 Hunters, Sponsors, Prize Carousel & Midnight Market | M-157 | (continued in sec 14) |
| M- (14.1–14.5 process; examples H/I/T) | 14 Gods, Ascendency, Nothing, Faction Wars & T'Ghee | M-209 | (continued in sec 15) |
| M- (single table) | 15 System AI psychology (secondhand unit, Primal Degeneration, fetish, tantrum, avatars) | M-227 | (continued in sec 16; see the M- row above for the current next free ID) |

**R- prefix note (Pass 7):** R- was already the 4e Races prefix (R-001..R-024), so the race-selection rows continue it (R-025..R-081 live in section 11; R-082 is next) instead of starting a new prefix. Section 11 rows have extra columns (Named crawler(s), Cite, Quote 2, Source 2); conflicts for races go to section 8 as X- rows. In section 11, VERIFIED requires a sentence-level wiki chapter cite or a second source family; stub pages with neither are WIKI-ONLY or UNVERIFIED.

**C- prefix note (Pass 8):** C- was already the 4d Classes prefix (C-001..C-013), so class-selection rows continue it (C-014..C-050 live in section 12; C-051 is next). Section 12 uses the same extra-column layout as section 11; conflicts for classes go to section 8 as X-042..X-047.

**M- / section 13 note (Pass 9):** Mechanics rulings continue the M- prefix for hunter/sponsor/Prize Carousel/Midnight Market *process* rules (M-119..M-157 in section 13; M-158 is next). Example rows reuse H-/I-/L-/T-. Conflicts for this pass are X-048..X-051.

**M- / section 14 note (Pass 10):** Gods/Ascendency/Nothing/Faction Wars/T'Ghee *process* rules continue M- (M-158..M-209 in section 14; M-210 is next). Examples H-057, I-027, T-072..T-073. Conflicts X-052..X-053. Deepens earlier thin rows M-029..M-032 without renumbering.

Always check the tail of the section before choosing an ID. If the table above is stale, the ledger wins.

## 3. Confidence labels
- **VERIFIED**: at least one of these holds:
  - the wiki page or row carries a **book-chapter citation** (record it, e.g. `cite B4 ch34`);
  - **two independent source families** agree. Families: Fandom wiki, FW2 generated fan wiki, NL fan site, YouTube recap transcripts. Two pages of the same family do not count as independent.
- **WIKI-ONLY**: one wiki source and no chapter citation.
- **UNVERIFIED**: no usable quote, incomplete wiki infobox, unresolved conflict, single fan-site claim, or a claim the sources themselves hedge.
- **No source in this folder is the novels' text.** VERIFIED is a bookkeeping label defined above. Only mark something confirmed against the book if someone has actually read the passage, and say so in the entry.
- Never invent facts. If a quote can't be found locally, the finding is UNVERIFIED or does not go in.

## 4. Conflicts
- When two sources disagree (floor numbers, names, rewards, dates), do not pick silently. Keep both claims in a new `X-` row with both source tags, the resolution if any, and the date.
- Reddit was blocked (HTTP 403) in earlier passes and is only referenced as unread snippets. Do not cite Reddit as a source unless the thread text was actually read and saved under `sources/`.

## 5. Checklist for a pass
1. Read `CANON-LEDGER.md` section 0 and the Pass log.
2. Find the finding in `raw/pages/`, `sources/` or a new saved source, and copy the quote.
3. Append the entries with the next IDs, a source tag, a confidence and a date.
4. Add a Pass log line and update the header date and version.
5. Run `python3 tools/ledger_check.py` and confirm `failures: 0`.
6. Update `INDEX.md` if you added or changed files in this folder. See `/workspace/dcc-campaign/NAMING-CONVENTIONS.md`: headers on every file, lowercase-hyphenated names, old versions in `_archive/`, never delete.

**Section 17 note (Pass 16):** Upgrade Patch process rules continue M- (M-240..M-262); per-patch rows continue I- (I-028..I-035); conflicts X-057..X-058 live in 17.3.

**Section 9.1 note (Pass 18):** Floor 1 creature, hazard and set-piece rows (mobs, boss-chamber staging, stairwell, safe-room and restroom rules) were appended as M-263..M-326 in section 9.1, below the APPEND-ONLY marker, because the ledger has no creature prefix and none of them are loot box facts (L- stays at L-023; L-024 is still free for a real loot box fact). Conflicts: none opened. Only the two FW2-only rows (M-325 Thorn Cadaver, M-326 Hobgoblin maze) are UNVERIFIED.

**Section 9.2 note (Pass 19):** Floor 2 rules, creature, hazard, NPC and set-piece rows were appended as M-327..M-524 in section 9.2 (placed just above the Pass log, after 9.1), feeding `tables/canon-floor-2.json` (status "reserve"). Four rows (M-521..M-524) are web-only: a chapter-summary site, no quote, labelled UNVERIFIED; the snippets live in `sources/web/f02-web-snippets.txt` (WEB: is not a tag kind in `ledger_check.py`, same as Pass 12). Conflicts X-059..X-065 are in 9.2c; X-062 records the canon six-day Floor 2 timer against the house 10-day clock (decision 026). Levels, difficulty, credits and loot amounts were deliberately left out. Next free: M-525, X-066.

**Section 9.3 note (Pass 20):** Premise-verification rows were appended as M-525..M-650 in section 9.3 (just above the Pass log, after 9.2), feeding `drafts/premise-verification.md`. Five claims: the Introduction event, dungeon shape/floor count/win condition, stairwell counts per floor, difficulty and Crawler counts, and floor-collapse fate of NPCs vs Crawlers. Nineteen rows (M-626..M-644: the Earth-surface row and Floors 1-18) have no quote because the wiki Floor Breakdown table has no quotable sentence; they were checked in script against the announced halving rule. Six rows (M-645..M-650) are web-only (no quote, UNVERIFIED), snippets in `sources/web/premise-web-snippets.txt`. Conflicts with the overview and other open questions are X-066..X-075 in 9.3c. Counts, timers in days and stairwell numbers are canon facts and were captured; levels, credits and loot amounts were not. Next free: M-651, X-076.
