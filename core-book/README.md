# Core Book Workspace
Owner: Valtay Corp - Core Book Author | Status: draft | Version: 0.1 | Updated: 2026-10-04
Summary: Filespace for the DCC TTRPG Core Rulebook (300+ pages, final output PDF).

## Folders
- drafts/ : work in progress, one file per day or section; promote to chapters/ when stable
- chapters/ : one file per chapter, ordered: 01-introduction.md, 02-character-creation.md, ... (numeric prefix = book order)
- assets/ : images, tables, fonts, cover art, stylesheets (assets/img/, assets/css/)
- build/ : generated PDF and build scripts only. Never hand edit. Name: dcc-core-rulebook-vX.Y.pdf
- notes/ : outlines, page-count tracker (notes/progress.md), open questions, source-to-chapter map (notes/source-map.md)

## Source material (READ-ONLY, do not edit)
Resolve via `DCC_CAMPAIGN_ROOT` / `DCC_LORE_ROOT` (or sibling folders next to this workspace). Never hardcode `/workspace` or `/home/box`.
- Campaign repo: `rules/`, `floors/`, `decisions/`, `DECISIONS.md`, `NAMING-CONVENTIONS.md`
- Lore (`lore/` in the campaign repo, or a sibling lore tree): `CANON-LEDGER.md`, `catalog/`, `tables/` (canon tags VERIFIED / WIKI-ONLY / UNVERIFIED; HOUSE = our invention)
- Older `crawler-protocol` drafts: superseded by campaign `rules/` where they differ

## Conventions (same as dcc-campaign/NAMING-CONVENTIONS.md)
- lowercase-hyphenated .md filenames; living docs carry the header: Owner | Status | Version | Updated, plus a one-line Summary. Retired versions go to _archive/ in the same folder.
- Keep an INDEX.md in this root listing every file (path, description, status).
- Carry canon tags into the text of the book source so you can decide at print time what to label as HOUSE vs canon.
- Never include GM-only content: nothing from campaign `gm-notes/` (especially `gm-notes/secret/`: GM quirk roll and player affinity are hidden by design). The book may describe the quirk/affinity system only at the level Lore has published as player-facing.
- Do not paste secrets or tokens. Do not use real player names or private comfort settings from gm-notes.

## Building from a fresh checkout
Needs Python 3, `pip install -r core-book/requirements.txt`, `google-chrome` (headless PDF), and `pdftotext` (poppler-utils, for TOC page numbers).
1. `python3 core-book/drafts/gen-ch2-tables.py` (regenerates Ch2 tables; finds `tables/` and `lore/tables/` from the repo root, or set `DCC_CAMPAIGN_ROOT` / `DCC_LORE_ROOT`)
2. `python3 core-book/build/build.py --version 0.1` (writes `build/dcc-core-rulebook-v0.1.pdf`)
