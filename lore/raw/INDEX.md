# Raw Mirror Index
Owner: DCC Lore | Status: review | Version: 1.1 | Updated: 2026-10-03
Summary: Local mirror of the Fandom wiki. raw/pages/ holds 2,017 cleaned page files (one per wiki title, original page-title names, exempt from naming rules).

| Path | Description | Owner | Status |
|---|---|---|---|
| all.json | Wikitext of all 2,017 Fandom wiki pages keyed by title (loaded by tools/wk.py). | DCC Lore | n/a (data/code) |
| clean.py | Converts all.json wikitext into cleaned raw/pages/*.txt. | DCC Lore | n/a (data/code) |
| dl.py | Downloader for the Fandom wiki pages (MediaWiki API). | DCC Lore | n/a (data/code) |
| intro.py | Helper that prints the intro of a cleaned page. | DCC Lore | n/a (data/code) |
| roster_auto.md | Auto-extracted roster of wiki character pages. | DCC Lore | draft |
| titles.txt | List of the 2,017 wiki page titles. | DCC Lore | n/a (data/code) |
| pages/*.txt | 2,017 cleaned wiki page files named by sanitized wiki title (Capitalised, with spaces). Read by tools/voice_index.py, tools/ledger_*.py. | DCC Lore | n/a (data) |
