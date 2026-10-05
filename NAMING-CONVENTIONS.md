# Naming Conventions and Folder Layout (v1.0)
Owner: Borent Corp Systems Architect. Applies to every bot. Root: /workspace/dcc-campaign/

## Folders (one per area)
| Folder | Owner | Contents |
|---|---|---|
| rules/ | Syndicate Dungeon Crawl System 001 | 5e overlay, loot boxes, death/revival, achievements system, protocols |
| lore/ | DCC Lore | canon catalogs, sources, CANON-LEDGER.md (link to /workspace/dcc-lore) |
| floors/ | Syndicate / GM | one subfolder per floor: floors/f01/ ... (module, bosses, encounters, System announcements) |
| characters/ | Syndicate / GM | one file per crawler + character-creation guide + intake form |
| sessions/ | AI GM | one log per session |
| gm-notes/ | AI GM | rulings, player quirks, comfort settings, open threads |
| decisions/ | anyone | one short file per table decision (death mode, comfort level, house rules) |
| tables/ | anyone | random tables, loot tables, name lists |
| bot/ | Borent | Discord voice bridge code and docs (link to /workspace/discord-voice-bridge) |
| exports/ | anyone | spreadsheets, PDFs, handouts for players |

## File names
- lowercase-hyphenated, .md by default (.csv/.xlsx for data only). No spaces, no capitals, except the special files below.
- Dated files: YYYY-MM-DD-topic.md (sessions: sessions/2026-10-03-session-01-floor-1.md).
- Characters: characters/<player>-<character-name>.md (e.g. characters/caleb-grimsby.md).
- Floors: floors/f01/00-overview.md, 10-encounters.md, 20-bosses.md, 30-system-announcements.md.
- Decisions: decisions/NNN-short-title.md (002-death-mode.md, 013-party-size.md).
- Living documents carry a version in the header (Version: 0.2.2, Updated: date, Owner), NOT in the filename. Retired versions move to _archive/ inside the same folder.
- Numeric prefixes (00-, 10-, 20-) are for reading order only inside a folder.
- Special uppercase files: INDEX.md, README.md, NAMING-CONVENTIONS.md, CANON-LEDGER.md, DECISIONS.md.

## Required header on every file
```
# Title
Owner: <bot name> | Status: draft|review|final | Version: x.y | Updated: YYYY-MM-DD
Summary: one line
```

## Index rules
- INDEX.md at the root lists every file: path, one-line description, owner, status. Each folder keeps its own INDEX.md; the root index links to those.
- Add a file => add an index line in the same step. Never delete; archive.
- Canon facts must be tagged VERIFIED / WIKI-ONLY / UNVERIFIED (see lore/CANON-LEDGER.md).
- Table decisions are recorded in decisions/ and summarized in DECISIONS.md.
