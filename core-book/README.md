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
- /workspace/dcc-campaign : rules/, floors/, decisions/, DECISIONS.md (table decisions 001-013), NAMING-CONVENTIONS.md
- /workspace/dcc-lore : CANON-LEDGER.md, catalog/, tables/ (canon tags VERIFIED / WIKI-ONLY / UNVERIFIED; HOUSE = our invention)
- /workspace/crawler-protocol : original protocol and 5e overlay drafts (superseded by dcc-campaign/rules where they differ)

## Conventions (same as dcc-campaign/NAMING-CONVENTIONS.md)
- lowercase-hyphenated .md filenames; living docs carry the header: Owner | Status | Version | Updated, plus a one-line Summary. Retired versions go to _archive/ in the same folder.
- Keep an INDEX.md in this root listing every file (path, description, status).
- Carry canon tags into the text of the book source so you can decide at print time what to label as HOUSE vs canon.
- Never include GM-only content: nothing from /workspace/dcc-campaign/gm-notes/ (especially gm-notes/secret/: GM quirk roll and player affinity are hidden by design). The book may describe the quirk/affinity system only at the level Lore has published as player-facing.
- Do not paste secrets or tokens. Do not use real player names or private comfort settings from gm-notes.
