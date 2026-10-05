"""Regenerates INDEX.md (lore root) and the per-folder INDEX.md files (catalog, sources, parts, tools, raw, _archive) from DESC below.
Every file in the lore folder needs one line in DESC (or a folder-level rule); missing files are printed and listed as '(no description yet)'.
Usage: python3 tools/gen_index.py   (owner is always DCC Lore; status is read from the file header when present)"""
import os,re,glob
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).absolute().parent))
from paths import LORE_ROOT
ROOT=str(LORE_ROOT); DATE='2026-10-03'
YT={'FHLzs9fjyU8':'Mana Toast Book 3 chapter-by-chapter recap (auto-captions)','edNtE1movic':'Mana Toast Book 4 chapter-by-chapter recap','R6QqZjlm-rA':'Book Recaps short recap of Book 3','SwwA5Px34pw':'Book Recaps short recap of Book 4','r0w4mNaSf-4':'Bored In Ohio Book 3 deep-dive reaction podcast (not yet mined)','6cvFdM1lLWU':'Jason Downs short "Book 3 misunderstood"','ua29K1aKKrc':'Lance Jepsen short on AI-fetish lore','wByubA0akII':'The EXP Live short','j6jRXuCgsAA':'Mana Toast Book 1 recap','sS36rv-jPLg':'Mana Toast Book 2 recap','TKcMxF2dA3w':'Mana Toast Book 5 recap','7Q49XeziMX0':'Mana Toast Book 6 recap','FurNY4o0uCo':'Mana Toast Book 7 recap','kk6nspvVf_M':'Mana Toast Book 8 recap','QTk6BtBipPk':'Bookborn Books 1-7 recap (contains errors)'}
DESC={
'INDEX.md':'This index: one line per file in the lore folder.',
'CANON-LEDGER.md':'Master canon ledger: dated entries with exact quotes, source tags and VERIFIED/WIKI-ONLY/UNVERIFIED confidence. Append-only.',
'ledger-rules.md':'Rules for appending to the ledger (IDs, quote limit, confidence, dating).',
'status-and-todo.md':'Pass history, coverage tables, source caveats and the running TODO list (the old INDEX body, plus Pass 4).',
'mechanics.md':'25-section mechanics reference (stats, XP, death, loot boxes, bosses, safe rooms, parties, AI behaviour).',
'characters.md':'Character roster: curated core cast plus auto-extracted wiki roster.',
'floors-and-plot-by-book.md':'Floor table and per-book plot summaries through Book 8 (full spoilers).',
'catalog/INDEX.md':'Index of the catalog folder.','sources/INDEX.md':'Index of the sources folder.','parts/INDEX.md':'Index of the parts folder.','tools/INDEX.md':'Index of the tools folder.','raw/INDEX.md':'Index of the raw wiki mirror.','_archive/INDEX.md':'Index of retired versions.',
'_archive/index-pass3.md':'Retired copy of INDEX.md after Pass 3 (live content moved to status-and-todo.md).',
'_archive/canon-ledger-draft.md':'Scratch draft of the ledger from the first build, kept for history.',
'parts/m1.md':'Working copy of mechanics.md sections 0-11.','parts/m2.md':'Working copy of mechanics.md sections 12-22.','parts/m3.md':'Working copy of mechanics.md sections 23-25.',
'parts/_archive/index-pass1.md':'Retired Pass 1 version of the lore index.',
'sources/source-log.md':'Log of every external source used, access method and limits.',
'sources/reddit/threads.md':'Reddit thread notes (unread snippets only; Reddit blocked).',
'raw/all.json':'Wikitext of all 2,017 Fandom wiki pages keyed by title (loaded by tools/wk.py).',
'raw/titles.txt':'List of the 2,017 wiki page titles.','raw/roster_auto.md':'Auto-extracted roster of wiki character pages.',
'raw/clean.py':'Converts all.json wikitext into cleaned raw/pages/*.txt.','raw/dl.py':'Downloader for the Fandom wiki pages (MediaWiki API).','raw/intro.py':'Helper that prints the intro of a cleaned page.',
'tools/wk.py':'Loader/parsers for raw/all.json shared by generators.','tools/gen.py':'Regenerates the table-based catalogs in catalog/ from raw/all.json.','tools/voice_index.py':'Regenerates catalog/system-voice-index.md.','tools/yt_fetch.py':'Fetches YouTube auto-caption transcripts into sources/youtube/.',
'tools/apply_headers.py':'Adds the convention header to every .md file (run after regenerating catalogs).','tools/gen_index.py':'Regenerates INDEX.md and the folder INDEX.md files.',
'tools/ledger_lib.py':'Helpers for the ledger tools: page lookup, quote extraction, trimming.','tools/ledger_ach.py':'Builds the achievements rows for the ledger.','tools/ledger_spec_mech.py':'Specs for the ledger mechanics rulings (M-).','tools/ledger_spec_other.py':'Specs for loot, skills, spells, items, classes, races, bosses, characters, plot beats.',
'tools/ledger_build.py':'Builds the initial CANON-LEDGER.md (do not re-run over an appended ledger).','tools/ledger_check.py':'Checks every ledger quote is an exact substring of its source and <=25 words.',
'sources/fanwiki/fetch.py':'Fetcher for the generated fan wiki (dungeon-crawler-carl.wiki).',
}
CATDESC_FROM_HEADER=True
def hdr(p):
    try: L=open(p,errors='ignore').read().split('\n')[:3]
    except: return None
    if len(L)>2 and L[1].startswith('Owner:'):
        st=re.search(r'Status: (\w+)',L[1]); sm=L[2][len('Summary: '):] if L[2].startswith('Summary:') else ''
        return (st.group(1) if st else '?'),sm
def desc(rel):
    if rel in DESC: return DESC[rel]
    if rel.endswith('.md'):
        h=hdr(os.path.join(ROOT,rel))
        if h: return h[1]
    if rel.startswith('sources/youtube/'): return 'Transcript: '+YT.get(os.path.basename(rel)[:-4],'YouTube recap')+' (working copy; do not quote at length)'
    if rel.startswith('sources/fanwiki/') and rel.endswith('.txt'):
        return 'Fan-wiki (dungeon-crawler-carl.wiki) page scrape: '+os.path.basename(rel)[:-4].replace('-',' ')
    if rel.startswith('sources/nl/'): return 'dungeoncrawlercarl.nl explainer: '+os.path.basename(rel)[:-4].replace('-',' ')
    if rel.startswith('work/'): return 'Scratch data from earlier passes (not KB content)'
    return '(no description yet)'
def status(rel):
    if rel.endswith('.md'):
        h=hdr(os.path.join(ROOT,rel))
        if h: return h[0]
    return 'n/a (data/code)'
def files(d):
    out=[]
    for dp,dn,fn in os.walk(os.path.join(ROOT,d)):
        dn[:]=[x for x in dn if x not in('__pycache__','pages','_archive')]
        for f in sorted(fn): out.append(os.path.relpath(os.path.join(dp,f),ROOT))
    return sorted(out)
def table(rels,base=''):
    r=['| Path | Description | Owner | Status |','|---|---|---|---|']
    for x in rels:
        r.append(f'| {x[len(base):]} | {desc(x)} | DCC Lore | {status(x)} |')
        if desc(x)=='(no description yet)': print('MISSING DESC',x)
    return '\n'.join(r)
def write(rel,title,summ,body):
    open(os.path.join(ROOT,rel),'w').write(f'# {title}\nOwner: DCC Lore | Status: review | Version: 1.1 | Updated: {DATE}\nSummary: {summ}\n\n{body}\n')
def sub(d): return [x for x in files(d)+[os.path.relpath(os.path.join(dp,f),ROOT) for dp,_,fn in os.walk(os.path.join(ROOT,d,'_archive')) for f in fn] if x!=d+'/INDEX.md']
# folder indexes
for d,title,summ in [('catalog','Catalog Index','One line per catalog file (generated wiki tables and hand-written clarifications).'),
 ('sources','Sources Index','One line per source file; transcripts and scrapes are working copies, not quotable at length.'),
 ('parts','Parts Index','Working parts of mechanics.md and the archived Pass 1 index.'),
 ('tools','Tools Index','Scripts that generate catalogs, the ledger and the indexes. Paths inside them are absolute or relative to this folder; do not move them.'),
 ('raw','Raw Mirror Index','Local mirror of the Fandom wiki. raw/pages/ holds 2,017 cleaned page files (one per wiki title, original page-title names, exempt from naming rules).')]:
    rels=[x for x in files(d)+[os.path.relpath(os.path.join(dp,f),ROOT) for dp,_,fn in os.walk(os.path.join(ROOT,d,'_archive')) for f in fn] if x!=d+'/INDEX.md']
    body=table(sorted(rels),d+'/')
    if d=='raw': body+='\n| pages/*.txt | 2,017 cleaned wiki page files named by sanitized wiki title (Capitalised, with spaces). Read by tools/voice_index.py, tools/ledger_*.py. | DCC Lore | n/a (data) |'
    write(d+'/INDEX.md',title,summ,body)
a=[os.path.relpath(os.path.join(ROOT,'_archive',f),ROOT) for f in sorted(os.listdir(os.path.join(ROOT,'_archive'))) if f!='INDEX.md']
write('_archive/INDEX.md','Archive Index','Retired versions kept for history; never delete.',table(a,'_archive/'))
top=['INDEX.md','CANON-LEDGER.md','ledger-rules.md','status-and-todo.md','mechanics.md','characters.md','floors-and-plot-by-book.md']
cat=[x for x in files('catalog')]
body=f"""Canon knowledge base for *Dungeon Crawler Carl* (spoilers through Book 8). Part of the campaign workspace as `lore/` (repo-relative; on some boxes a symlink into this tree). Rules: campaign root `NAMING-CONVENTIONS.md` (sibling of `lore/` in a fresh checkout, or set `DCC_CAMPAIGN_ROOT`).

**Start here:** `CANON-LEDGER.md` is the master record of canon findings (each with an exact quote, source tag, confidence and date). Add to it only by the procedure in `ledger-rules.md`. Nothing in this folder was checked against the novels' text.

## Convention notes for this folder
- New files use lowercase-hyphenated names. Exceptions: the special files INDEX.md and CANON-LEDGER.md, and the **data mirrors** named after wiki titles or video IDs (`raw/pages/*.txt`, `sources/**/*.txt`), plus code in `tools/` and `raw/`.
- Every `.md` file starts with the standard header (title, Owner/Status/Version/Updated, Summary). Data mirrors (`.txt`, `.json`) and scripts are exempt because tools read them verbatim.
- Version lives in the header; retired versions go to `_archive/` (or `parts/_archive/`). Nothing is deleted.
- Catalogs are regenerated by `tools/gen.py` / `tools/voice_index.py`, which call `tools/apply_headers.py` so the headers survive.
- Folder indexes: [catalog](catalog/INDEX.md), [sources](sources/INDEX.md), [parts](parts/INDEX.md), [tools](tools/INDEX.md), [raw](raw/INDEX.md), [_archive](_archive/INDEX.md). `work/` is scratch.

## Top-level files
{table(top)}

## catalog/
{table(sorted(cat),'')}

## parts/
{table(sorted(sub('parts')))}

## sources/
{table(sorted(sub('sources')))}

## tools/
{table(files('tools'))}

## raw/ (wiki mirror)
{table(files('raw'))}
| raw/pages/*.txt | 2,017 cleaned Fandom wiki page files, one per wiki title (Capitalised names with spaces; exempt data mirror). Source for most ledger quotes (tag `W:<page>`). | DCC Lore | n/a (data) |

## _archive/
{table(sorted(sub('_archive')) if False else [os.path.relpath(os.path.join(ROOT,'_archive',f),ROOT) for f in sorted(os.listdir(os.path.join(ROOT,'_archive')))])}

## work/ (scratch)
Scratch JSON/transcript folds from Pass 3 (`work/*.json`, `*.fold`, `b7wiki.txt`). Not KB content; safe for tools to overwrite. Ledger rebuilds write to `work/ledger-rebuild.md`.
"""
write('INDEX.md','DCC Lore Index','One line per file in the lore folder: path, description, owner, status.',body)
