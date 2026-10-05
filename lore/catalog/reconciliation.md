# Pass 3 reconciliation - mechanics.md section 25, old [UNVERIFIED] tags, gap-fills, Book 9 status (Oct 3, 2026 CT)
Owner: DCC Lore | Status: review | Version: 1.0 | Updated: 2026-10-03
Summary: Pass 3 reconciliation of old [UNVERIFIED] tags, gap fills and open items (renamed from reconciliation-pass3.md).

Tags: **[W]** Fandom mirror in `raw/`, **[YT]** transcripts in `sources/youtube/`, **[WEB]** fetched web pages (see `sources/source-log.md`). Status words: **RESOLVED** (answered by a cited source), **PARTIAL**, **OPEN**. Nothing here was checked against the novels.

## A. `mechanics.md` section 25 - gap-by-gap

| # | Original gap (Pass 1) | Status after Pass 3 | Where / note |
|---|---|---|---|
| 1 | Per-spell, per-item, per-race rules | **RESOLVED at catalog level** | `catalog/spells.md`, `items.md`, `races.md`, `classes.md`, `skills.md`; per-page numbers are wiki-level, not tested against the books. |
| 2 | Full achievement catalog | **RESOLVED** (148 achievement pages with AI-voice text; ~35 sample quotes) | `catalog/achievements.md`, `catalog/system-voice.md`, `catalog/system-voice-index.md`. 11 rows were tagged "infobox incomplete" - see section C. |
| 3 | XP curve / level thresholds | **OPEN (probably unanswerable)** | Wiki states the formula "has never been defined". No new data in recaps (they only give level milestones). |
| 4 | HP / mana formulas beyond HP~CON, MP~INT | **PARTIAL** | `mechanics-clarifications.md` 2.3: INT sets max MP (~INT), regen scales with INT (INT 3 ~1 MP/hour; INT 17 ~1 MP/min), spell/scroll strength. HP formula still only "tied to CON". |
| 5a | Patch / boon / benefit / skill lists | **RESOLVED at catalog level** | `catalog/benefits-and-status-effects.md`, `skills.md`; patches = fleeting items sewn on the Battle Rattle (wiki lists 9, 8 equippable); boons = god-granted buffs lasting a day to a floor. |
| 5b | Crafting tables | **PARTIAL -> RESOLVED enough** | Tables level up when a floor collapses; safe rooms sell workbenches only from Floor 4; a Dungeonpreneur pays royalties (1 gold per kill; cash-out fee 2 gold + 25%) [W Crafting]. |
| 5c | Midnight Market | **RESOLVED** | Carl gets access on Floor 9 via a Reaper Spider Minion patch (B7 ch4); hidden at the bottom of the Desperado Club; merchant is **Paca** (agent of Krakaren Prime; B7 ch69-78) [W Midnight Market]. |
| 5d | Prize Carousel | **RESOLVED** | Chaco's fan-box mini-game: nine prizes, ten minutes, unscannable; Carl chose the Cookbook in Book 3 [W]. |
| 5e | Skyfowl / Bopca / Kua-Tin / Mantis | **RESOLVED (wiki-level)** | Skyfowl: eagle-headed, Mordecai's birth race. Bopca: shaggy dwarf-like safe-room attendants (Tally). Kua-Tin: mudskipper water-breathers who own Borant. Mantis: hive species; the Dark Hive hunts on Floor 6. |
| 5f | Hunters' rules | **RESOLVED** | Arrive on Floor 6, base in Zockau, ~360 at L50, hunt crawlers for gear sold to Faction Wars leaders; kill trophies are **hands** used as prize currency; see `books-5-8-detail.md`. |
| 5g | Blood Hunter show | **RESOLVED** | Scripted drama starring Viscount Fog and his mount Sierra (L65 Neighborhood Boss); produced by Blood Hunter Holdings, owned by the Blood Sultanate (B7 ch44). Killed Miriam Dom (B5) -> Prepotente's revenge on the Nagas (B7 ch45). |
| 5h | Unwashed | **PARTIAL** | Architect Houston describes the Unwashed (B7 ch44) - many treat them as superstition. Wiki lists "The Beautiful Place" among their names. |
| 6 | Reddit and YouTube not mined | **PARTIAL** | YouTube: 6 recap transcripts added (B1, B2, B5, B6, B7, B8) + Bookborn 1-7. Reddit: still HTTP 403 from the box; **not circumvented**. Hello Crawlers podcast and two other videos hit YouTube's request block - **not circumvented**. |

## B. Old `[UNVERIFIED]` tags - resolution log

| Location | Old tag | New status | Evidence |
|---|---|---|---|
| mechanics.md l.3-4 | general caveat | **Kept** (still fan-source based) | - |
| mechanics.md l.38 | Unconscious threshold ~5-6% | **OPEN**, narrowed | Wiki "Health" page lists the number under Speculation (Carl got a pass-out warning at ~6%). Half-Splat potions leave the drinker at 5% [W]. Survivor's Box thresholds: Carl <10%, Donut <5% [W]. Martyr's Path triggers at 5% (B6 ch69) [W]. Best reading: pass-out risk at roughly 5-10% depending on the build, **not** a fixed rule. |
| mechanics.md l.150 (Gate custody) | custody chain | **RESOLVED (except watches)** | See chain below. |
| mechanics.md l.151 (Scavenger's Daughter) | which child | **PARTIAL** | Patch came from a Celestial Predator Box (B6 ch3). Rosetta tells the Scavenger myth (B8 ch69); B7 ch78 the War Mages claim to have "found the Scavenger's Daughter" and leave. Identity remains **OPEN**. |
| mechanics.md l.159 (Eulogist/Apothecary/Primals) | wiki-only | **Corroborated** | B8 ch92 (AI explains Primals via Grigori) - wiki + Mana Toast agree; B6 ch48 Orren and ch51 Paulie/Residuals. |
| floors-and-plot-by-book.md l.46 | Grimaldi vine plan | **RESOLVED** | B2 ch10-11: poisoned-blood trick. |
| floors-and-plot-by-book.md l.18 | Book 8 title correction / Book 9 | **Updated** | See section D. |
| bestiary-by-floor.md l.12 | Denise origin (7th floor goose) | **OPEN, likely wrong** | Floor 7 was an ~10-minute pod level with no mobs; "feral goose from 7th floor" in the fan-wiki is not supported by the Fandom mirror. Treat as **fan-wiki error**. |
| bestiary-by-floor.md l.13 | Carl level F4->F5 | **unchanged** | no new data |
| loot-boxes.md l.10 | Celestial tax | **MED** | Reaffirmed by Celestial page (2,145 awarded ever; max 18 per season) [W]. Still unverified against text. |
| floor-data.md l.5 | Floors 12+ speculative | **Updated**: Floors 12-18 are only sketched by the books so far | B8 epilogue: Floor 12 = Ascendency Game start; Sheol = Floor 15; Floor 18 exits; see `books-5-8-detail.md`. |

### Gate of the Feral Gods - custody chain (resolves mechanics.md l.150)
1. **B4:** assembled/used (see `books-3-4-detail.md`).
2. **B5 start of Floor 6:** Borant can't seize it; Carl lends it via lawyer **Quasar** for a receipt promising return on **Floor 9** + four mercenaries + two replica spells (Teleport to Stairwell, Zerzura). (Wiki chapter summary says "until level 9", a slip.) Handler: **Orren**.
3. **B6 ch51:** Orren refuses an early return.
4. **B7 ch1:** returned (dungeon mailbox).
5. **B7 ch59-61:** Elle opens it in Dream territory -> Meatus, Harpocrates; Eris appears (ch61). Afterward **Akuma** takes it.
6. **B7 ch69:** War Mages trade it at the Midnight Market to **Paca** for five hell-kissed Conscription potions.
7. **B7 ch76-78:** Eris tells Carl where it is (inside Paca's stomach); Carl gives the location to **Justice Light** and the sluggalos, who retrieve it.
8. **B7 ch87:** its winding box becomes a permanent tear; Justice Light's trap shatters the Nothing.
- **Not stated:** the fate of its two "watches"/other components; B8 never mentions it again. **OPEN.**

### Memorial crystals - who holds what
- **Apito:** Imogen's neck -> prize counter, 100 hands (B5 ch67) -> reverts to her body and is looted by **Osvaldo** (B5 ch75-77) -> Prepotente (B7 ch78; B8 ch41) -> pulled off by a deity, **Taranis** (B8 ch98). Charge: 11.1% after one Scolopendra attack (B8). It protected Prepotente from the dachshund transformation.
- **Ysalte:** Paz's totem kills Ysalte (B6 ch69) -> Osvaldo holds it -> **Britney** takes it after killing Osvaldo (B8 ch83).
- **Emberus:** Carl finds it after the parade (B8 ch98).

## C. Achievement rows previously "infobox incomplete" - fills from `raw/pages`
| Achievement | Reward / box (from the AI text) | Cite |
|---|---|---|
| Celestial Orgy of Chaos | Celestial **Who Let the Gods Out This Time?** Box | B7 |
| I'll Take the Ceramic Dalmatian, Pat! | the reward is the Reward Room itself (no box) | - |
| Marked for Life | Platinum **Apostate Box** | B6 ch2 |
| Menagerie | Reward Room (a key to a single cage) | - |
| Rock Bottom | Gold **I'm Wet Box** | B4 ch28 |
| Scourge | Legendary **Hunter Champion Box** | B6 ch2 |
| Uprooted | no box; "this achievement is the reward" | B5 |
| Why Aren't You Wearing Pants? | Gold **Apparel Box** | B1 ch2 |
| You have discovered a Celestial Thorn Room! | narration reward (Bret Michaels rose quip) | B6 ch15 |
| It Burns Dunnit | no Reward text on page | B1 |
| Oh shit! A country Boss! | no standalone raw page found | B6 |

## D. Book 9 - release status re-check (Oct 3, 2026) [WEB]
- **Working title:** "The Beautiful Place" (Dinniman's Patreon prologue post, June 16, 2026: "book 9, The Beautiful Place (Working title)"). Not locked. The Unwashed's alias on the wiki suggests a thematic link - **my inference, unverified**.
- **Format:** series finale; written as one book but planned as **two physical volumes** with a cliffhanger at the end of the first [dungeoncrawlercarl.nl, Jul 15 and Aug 20, 2026; CinemaBlend (updated Sep 25, 2026)].
- **Release date:** **none announced.** Dinniman told Variety (July 2026) he is "still like a year out". Any "2027" date is speculation. mattdinniman.com lists no Book 9 page.
- **Progress:** prologue posted to Patreon June 2026; chapters 1-2 in August 2026.
- **Opening situation:** Floor 12 (Ascendency Games), Carl alone in a cotton field.
- **Related:** *Book 1 Deluxe Edition* due Nov 17, 2026 (CinemaBlend); *Operation Bounce House* (standalone, 2026); Peacock adaptation via Fuzzy Door (Chris Yost writing, Dinniman EP) - from a YouTube summary, **unverified**.
- Reddit not consulted (403).
