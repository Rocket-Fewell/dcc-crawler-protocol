"""Idempotently puts the NAMING-CONVENTIONS header on every .md file under the lore root (outside raw/ and work/):
    # Title
    Owner: DCC Lore | Status: ... | Version: x.y | Updated: YYYY-MM-DD
    Summary: one line
Run after tools/gen.py or tools/voice_index.py (both call it at the end) because they rewrite the catalog files.
Usage: python3 tools/apply_headers.py"""
import os,re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).absolute().parent))
from paths import LORE_ROOT
ROOT=str(LORE_ROOT)
DATE='2026-10-03'
# path -> (status, version, summary)  [title comes from the file's own first '# ' line]
META={
'catalog/achievements.md':('review','1.0','Achievement catalog: 150 wiki pages plus master-list-only and unnamed hub entries, with triggers and rewards.'),
'catalog/benefits-and-status-effects.md':('review','1.0','Benefits (static traits) and status effects, one line each from the wiki.'),
'catalog/bestiary-by-floor.md':('review','1.0','Monsters and boss levels grouped by floor, fan-wiki derived.'),
'catalog/books-1-2-6-7-detail.md':('review','1.0','Chapter-level beats, gap fills and conflicts for Books 1, 2, 6 and 7.'),
'catalog/books-3-4-detail.md':('review','1.0','Chapter-level beats, numbers and open questions for Books 3 and 4.'),
'catalog/books-5-8-detail.md':('review','1.0','Chapter-level beats, Floor 7, numbers and conflicts for Books 5 and 8.'),
'catalog/bosses.md':('review','1.0','Boss stat blocks and the boss tier ladder, wiki-derived.'),
'catalog/classes.md':('review','1.0','How classes work plus the class list with notes.'),
'catalog/floor-data.md':('review','1.0','Per-floor data sheet for Floors 1-18 (crawler counts, level ranges, exits) from wiki infoboxes.'),
'catalog/items.md':('review','1.0','Items and potions catalog with one-line notes.'),
'catalog/loot-boxes.md':('review','1.0','Loot box tiers, rules and one row per box type page.'),
'catalog/mechanics-clarifications.md':('review','1.0','Pass 2 clarifications on XP, stats, skills, loot boxes, bosses and safe rooms.'),
'catalog/quests.md':('review','1.0','Quest catalog with condensed descriptions and book/spoiler tags.'),
'catalog/class-selection-canon.md':('review','1.0','How Floor 3/6/9 class selection works (AI recommendations, Earth Classes, endorsements, Four Seasons, Character Actor) with pointers to ledger rows C-014..C-050 and conflicts X-042..X-047.'),
'catalog/hunters-and-sponsors-canon.md':('review','1.0','Floor 6+ hunters (trophies, Masquerade Prize Counter), sponsor auctions/Benefactor/Fan boxes, Prize Carousel, Midnight Market; pointers to ledger M-119..M-157 and conflicts X-048..X-051.'),
'catalog/gods-faction-wars-canon.md':('review','1.0','Gods/worship/Soul Armor/deity sponsorship, Celestial Ascendency, Nothing, Faction Wars, T\'Ghee; pointers to ledger M-158..M-209 and conflicts X-052..X-053.'),
'catalog/race-selection-canon.md':('review','1.0','How Floor 3 race selection works and a per-race table (what it is, named crawler, cite, confidence) with pointers to ledger rows R-025..R-081 and conflicts X-031..X-041.'),
'catalog/races.md':('review','1.0','Races catalog with notes; one line per wiki race page.'),
'catalog/reconciliation.md':('review','1.0','Pass 3 reconciliation of old [UNVERIFIED] tags, gap fills and open items (renamed from reconciliation-pass3.md).'),
'catalog/skills.md':('review','1.0','Skills catalog: 100 wiki pages with one-line notes.'),
'catalog/spells.md':('review','1.0','Spells catalog: 95 wiki pages with one-line notes.'),
'catalog/system-voice-index.md':('review','1.0','Generated index of wiki pages that carry System/AI voice sections (names only, no excerpts).'),
'catalog/system-voice.md':('review','1.0','System/AI voice catalog and style guide for emulating the dungeon announcer.'),
'characters.md':('review','1.0','Character roster: crawlers, NPCs, gods and pets, with notes through Book 8.'),
'mechanics.md':('review','1.0','25-section mechanics reference: stats, XP, death, loot boxes, bosses, safe rooms, parties and more.'),
'floors-and-plot-by-book.md':('review','1.0','Floor-by-floor and book-by-book plot summary through Book 8 (full spoilers).'),
'parts/m1.md':('draft','1.0','Working copy of mechanics.md sections 0-11.'),
'parts/m2.md':('draft','1.0','Working copy of mechanics.md sections 12-22.'),
'parts/m3.md':('draft','1.0','Working copy of mechanics.md sections 23-25.'),
'parts/_archive/index-pass1.md':('final','1.0','Retired Pass 1 version of the lore index, kept for history.'),
'sources/source-log.md':('review','1.0','Log of what sources were actually read in Pass 2 and how.'),
'raw/roster_auto.md':('draft','1.0','Auto-extracted roster of all wiki character pages (generated; feeds characters.md Part B).'),
'sources/reddit/threads.md':('review','1.0','Notes on Reddit threads; Reddit was blocked (403), so these are unread snippets only.'),
'_archive/index-pass3.md':('final','1.0','Retired copy of INDEX.md as it stood after Pass 3; its content lives on in status-and-todo.md.'),
}
def apply(rel,status,ver,summ,title=None):
    p=os.path.join(ROOT,rel)
    if not os.path.exists(p): return False
    L=open(p).read().split('\n')
    if len(L)>2 and L[1].startswith('Owner: ') and L[2].startswith('Summary: '): return False
    if L and L[0].startswith('# '): t=L[0]; rest=L[1:]
    else: t='# '+(title or os.path.basename(rel)[:-3].replace('-',' ').title()); rest=L
    if rest and rest[0].strip(): rest=['']+rest
    L=[t,f'Owner: DCC Lore | Status: {status} | Version: {ver} | Updated: {DATE}',f'Summary: {summ}']+rest
    open(p,'w').write('\n'.join(L)); return True
def main():
    n=0
    for rel,(s,v,m) in META.items(): n+=apply(rel,s,v,m)
    return n
if __name__=='__main__': print('headers added:',main())
