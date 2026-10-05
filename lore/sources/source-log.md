# Pass 2 source log (what was actually read, and how)
Owner: DCC Lore | Status: review | Version: 1.0 | Updated: 2026-10-03
Summary: Log of what sources were actually read in Pass 2 and how.

Written Oct 3, 2026 (CT). Rule used: notes are my own paraphrase; only very short quotes; every external claim carries a reliability tag.

Reliability tags: **[W]** Fandom wiki (mirror in `raw/`), **[R]** Reddit thread (community opinion unless a commenter cites text), **[YT]** YouTube auto-caption transcript (summaries by fans; auto-captions garble names), **[FS]** fan site, **[FW2]** `dungeon-crawler-carl.wiki` (self-described as generated from the books; has errors), **[UNVERIFIED]** not checked against book text.

## Access notes (important for future passes)
- **Reddit**: direct fetch (curl or WebFetch) of reddit.com / old.reddit.com / `.json` is **blocked (HTTP 403, or timeouts)** from the box. Reddit content below was read through the web-search index, which returns the post text and top comments as snippets. That means: threads are partial (top comments only), dates are as reported by the index, and I could not read full comment trees or r/dungeoncrawlercarl wiki/megathreads. **The sub's wiki/FAQ pages and the 245-entry stat-block table on r/DungeonCrawlerCarlRPG were NOT read.**
- **YouTube**: transcripts fetched with `youtube-transcript-api` (venv at `/workspace/yt`), raw files in `sources/youtube/<id>.txt` (local working copies; do not quote at length). Auto-captions mangle proper names (e.g. "Amani" = Imani, "Heckla" = Hekla, "Impropotente" = Prepotente, "Embrus/Embers" = Emberus, "Gruul/Grull" = Gruul).
- **dungeoncrawlercarl.nl** and **crawlerscookbook.com** pages fetched with curl (public); **dungeon-crawler-carl.wiki** (fan site) scraped for per-book overviews and bestiaries into `sources/fanwiki/`.
- No book text consulted directly.

## Sources used
| Tag | Source | URL | Used for |
|---|---|---|---|
| YT | Mana Toast, "Book 3 Chapter-by-Chapter RECAP" (39:44, posted May 13, 2026) | youtube.com/watch?v=FHLzs9fjyU8 | Book 3 beats, numbers (levels, stations, items) |
| YT | Mana Toast, "Book 4 Chapter-by-Chapter RECAP" (29:28, posted Jun 29, 2026) | youtube.com/watch?v=edNtE1movic | Book 4 beats, boss levels, items |
| YT | Book Recaps, Book 3 (4:59) and Book 4 (5:01) shorts-style recaps | youtube.com/watch?v=R6QqZjlm-rA , SwwA5Px34pw | cross-check only (short, partly auto-summarized) |
| YT | Bored In Ohio, Book 3 deep dive (47:47) ; Jason Downs "Book 3 misunderstood" (1:53) ; Lance Jepsen AI-fetish lore (4:14) ; The EXP Live short | r0w4mNaSf-4 , 6cvFdM1lLWU , ua29K1aKKrc , wByubA0akII | opinion/analysis color; AI-personality lore. Deep-dive transcript saved but **not mined** this pass |
| R | "Donut Question" (r/DungeonCrawlerCarl) | reddit.com/r/DungeonCrawlerCarl/comments/1toxizl/ | XP curve speculation, Donut L135 |
| R | "Question about Donut's level" | .../comments/1tm15z3/ | same |
| R | "Question about a specific interaction in book 1" (Apr 4, 2026) | .../comments/1scdxir/ | party XP split ~98% / remainder |
| R | "Does anyone know what Carl's stats are?" | .../comments/1hile73/ | stat-estimate (fan guess), author tracking database remark |
| R | "How does Intelligence work" ; "Carl's intelligence" | .../comments/1vjmgrs/ , 1m7537l/ | INT meaning (mana/recall/spell duration), Wisdom hidden |
| R | "A Pondering on Celestial Boxes" (Jun 30, 2024) | .../comments/1drrlka/ | celestial veto context |
| R | "Can someone remind me of the order of the boss levels" ; "Help me with Boss levels" | .../comments/101m4ao/ , 1g6k869/ | boss-tier order (snippet only via search synthesis) |
| R | Book 3 / Iron Tangle threads (acceptance/frustration, "I need help understanding...", "How did BLANK's BLANK kill BLANK") | .../comments/1v2m4ut/ , 1sz4uh9/ , 1ur10qb/ | reception; Hekla death mechanics (snippet-level) |
| R | Book 4 threads ("Questions regarding book 4", "Question about the Gate of the Feral Gods", etc.) | .../comments/1d4vzzb/ , 1vocdfz/ , 1uwiqjm/ | Gate of Feral Gods interpretation (snippet-level, weak) |
| R | r/DungeonCrawlerCarlRPG: "245 mobs/bosses/NPCs stat blocks" table ; "what does the number in parentheses in stat blocks mean" ; "How to make mobs & bosses" | .../DungeonCrawlerCarlRPG/comments/1w2yl6c/ , 1w0rizx/ , 1vn9ldd/ | **only the titles/summary seen; this is the TTRPG game, not canon**. TODO read via a non-blocked mirror |
| FS | dungeoncrawlercarl.nl explainers (Constitution; boss hierarchy; safe room; achievements/loot boxes) | dungeoncrawlercarl.nl/en/news/... | potion cooldown, boss ladder, XP basics |
| FS | The Crawler's Cookbook recaps Book 3 / Book 4 | crawlerscookbook.com/recaps/book-3/ , book-4/ | plot cross-check; Cookbook lineage claims |
| FS | manatoastmedia.com Book 3 recap (text version of the YouTube video) | manatoastmedia.com/dungeon-crawler-carl-book-3-chapter-by-chapter-recap/ | via search snippet only |
| FW2 | dungeon-crawler-carl.wiki per-book overview + bestiary | dungeon-crawler-carl.wiki/book-N/ | levels and boss tables (see catalog/bestiary-by-floor.md) |
| W | Fandom pages Player Stats, Skills, Loot Boxes, Celestial (reads via search snippets as a cross-check on the local mirror) | dungeon-crawler-carl.fandom.com | consistency check with mechanics.md |

## Pass 3 (Oct 3, 2026 CT)
| Type | Source | Access | Used for / limits |
|---|---|---|---|
| YT | Mana Toast B1 recap `j6jRXuCgsAA` (44:19), B2 `sS36rv-jPLg` (37:41), B5 `TKcMxF2dA3w` (43:05), B6 `7Q49XeziMX0` (56:20), B7 `FurNY4o0uCo` (1:42:48), B8 `kk6nspvVf_M` (1:32:55) | youtube_transcript_api via `tools/yt_fetch.py` | chapter beats, numbers; auto-caption name garbling |
| YT | Bookborn "Books 1-7 recap" `QTk6BtBipPk` (55:16) | same | Floor 7 confirmation; contains errors (e.g. Li Na ring on "seventh floor") |
| YT-blocked | Hello Crawlers podcast Ep 25 `tqmd62wcI6c`; `bkCQ9-_8GjE`; `F8_f7qcrYk4` | "YouTube is blocking requests" | **not retried via workarounds** |
| Reddit | reddit.com | HTTP 403 from the box | **skipped, not circumvented** |
| W | Fandom mirror pages: Book 1/2/5/6/7/8 Chapter Summaries, Seventh Floor, Seventh Floor Pole Position, Gate of the Feral Gods, Memorial Crystal, Crafting, Midnight Market, Prize Carousel, Hunters, Unwashed, Blood Hunter, Boon, Upgrade Patch, Skyfowl, Kua-Tin, Bopca, Mantis, achievement/item/spell/class pages (AI Description sections) | local `raw/` | voice quotes (short), chapter beats, gap-fills |
| WEB | dungeoncrawlercarl.nl (Jul 15 and Aug 20, 2026 news), CinemaBlend (updated Sep 25, 2026), ScreenRant, crawlerscookbook.com, Dinniman Patreon prologue post (June 16, 2026, via search/fetch), mattdinniman.com (no Book 9 listing), Variety quote (July 2026) via search snippets | WebSearch / WebFetch / curl | Book 9 status; Peacock/Deluxe Edition facts unverified |
- Not covered: audiobook, "extra Pineapple Cabaret chapters", Dinniman Q&A videos, the book texts themselves.
- Revival pass web sources (2026-10-03): chapter-summaries.com B4, Storiluna B4 ch13, Mana Toast B2 recap, generated fan wiki (Yarilo/Geyrun/Donut), Book 9 pages; Reddit 403; excerpts saved in `sources/web/revival-web-snippets.txt` (WEB: tags); not ledger-quotable.

## Pass 7 (2026-10-03): races and Floor 3 race selection
| Type | Source | Access | Used for / limits |
|---|---|---|---|
| NL | dungeoncrawlercarl.nl 'How race and class work' (26 Jul 2026) | WebFetch, saved to sources/nl/how-race-and-class-work.txt | second family for three recommendations, hundreds of options, ~80%, banked stat points |
| WEB | crawlerscookbook.com/floors/floor-3/ | WebFetch, excerpts in sources/web/race-selection-web-snippets.txt | cross-check; calls Primal 'enhanced' (rejected, X-040) |
| YT | Mana Toast B2 sS36rv-jPLg, Bookborn QTk6BtBipPk, Mana Toast B3/B4/B5/B6 | local transcripts | 320/398 options, Carl's three recommendations, race picks by Katia, Bautista, Elle, Chris, Maggie, Popovs, Sister Ines |
| W | Fandom mirror: Crawler, Tutorial, Tutorial Guild Hall, Third Floor and 40+ race and crawler pages | local raw/pages | main quotes |
| Reddit | r/DungeonCrawlerCarl threads (80% claim, Mordecai forms) | search snippets only (403) | not used for any VERIFIED label |
| W-live | Fandom Grulke and Nodling pages | HTTP 403 | local mirror used; live Tutorial Guild Hall page matched the mirror |
| WEB | afterword.to chapter summaries (B1 ch30, 37, 39, 45, 46), manatoastmedia B1 recap, Fandom Meadow Lark, dungeon-crawler-carl.wiki bestiary, one Reddit snippet | search snippets, saved in sources/web/f02-web-snippets.txt | Floor 2 canon gaps; web-only rows M-521..M-524 (UNVERIFIED); conflicts X-061, X-064 |
| WEB | Nerdist overview, Wikipedia plot summary, simulacra.ink World Dungeon page, manatoastmedia B1 recap, crawlerscookbook Floor 1 page, Fandom Transformation/Dungeon/Stairwells/First Floor snippets | search snippets, saved in sources/web/premise-web-snippets.txt | Premise verification (ledger 9.3); web-only rows M-645..M-650 (UNVERIFIED); Fandom snippets matched the local mirror |
| W-live | Fandom Second Floor page | HTTP 403 on direct fetch; search snippet matched the local mirror | local mirror used |
