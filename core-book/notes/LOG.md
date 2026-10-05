Sun Oct  4 12:43:26 CDT 2026: created filespace and plan

- 2026-10-04 21:05 CT: Names APPROVED, species-class-reskins v0.1.5 (74 entries, sha 3a3a49b05d93). Print race/class names only from it ("Our Name (5e Name)"); re-read table before drafting. /create scope = 9 SRD species, 24 lineages, 12 classes, 4 options; variants go in Floor 3 Offer section. Lajabless starts Radiant (phase entries are state labels). Bot name now "Dungeon System AI - Earth" (live).

## 2026-10-04 (evening) - Pipeline plus Chapters 1 and 2 first drafts
- Built the pipeline: markdown to HTML to PDF with headless Chrome (build/build.py, assets/css/book.css). Two-pass TOC page numbers, running headers, cover with 18-floor inverted pyramid.
- Wrote chapters/00-front-matter.md (legal, SRD 5.2 CC-BY-4.0 attribution, tag legend), 01-welcome.md (12 pp), 02-crawler-creation.md (21 pp). Chapter filenames follow the task (01-welcome, 02-crawler-creation), not the README's 01-introduction / 02-character-creation.
- Ch2 is assembled by drafts/gen-ch2-tables.py from drafts/02-crawler-creation.src.md plus live tables from the read-only source JSONs. Edit the .src.md, never the generated chapter file.
- Source versions used (per Syndicate steer): characters/character-creation-5e.md v0.2.3; characters/create-flow-spec-5e.md v0.1.12 (not v0.1.10); tables/chargen-5e.json v0.1.5 (not v0.1.4; generator asserts it); species-class-reskins v0.1.5; background-reskins v0.1.2; create-screens-reskins v0.1.3. Core rules v0.2.13 (collapse death, decision 028).
- Species section tagged PROVISIONAL (Caleb's species answers outstanding). Flavor kept to 3-4 sentences.
- Rulings reflected: premise; 18-floor inverted pyramid (house framing); timed floors 5/10/20 days (decision 026); collapse death on every floor, no Reprieve for it (026/028); Roll method as HOUSE option (024); multiple Crawlers, one active, /crawlers, /delete (020).
- Deliberately not printed: pets, Story Boxes, GM quirk roll, survey questions and Fan Profile mechanics, Floor 3+ audit figures, rules/70 totals, GM-only material. Never opened dcc-campaign/gm-notes, player data or logs.
- Money check: no GP/cp/gold/coins/cash as money words in Ch1-2 (Gold only appears as a loot-box tier and a Dragonborn ancestry name). Generator rewrites "cash-only" in a reskin flavor line to "credits-only".
