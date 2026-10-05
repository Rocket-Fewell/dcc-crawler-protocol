# Decision 032: Voice split — dry [SYSTEM] vs snarky [GM]

Summary: Table TTS / GM-output tag contract: System is dry corporate; achievements, loot-box color, and jokes are narrator/GM.

## Ruling (Caleb, Oct 5 2026; filed by the rules designer)

1. **`[SYSTEM]`** = dry, informative, corporate voice: game clock/timers, fees, registration, collapse warnings, floor notices, welcome/registration announcements. **No jokes.**
2. **`[GM]`** (or untagged) = snarky narrator voice: achievements (**both** the banner/header **and** the mocking description), loot-box callouts/openings, all jokes and color.
3. Tag contract remains per-line at line start (markdown like `**[SYSTEM]**` allowed); a tag applies to its line and all following lines until the next tag; `[ROLL]` is never spoken; untagged = narrator. See `bot/README.md` / `src/tags.js`.
4. **Carry-over:** a message that mixes a System line then snark must **re-tag `[GM]`** before the snark.
5. Where snark is removed from System lines, **the GM picks it up**. The GM should always be ready to crack a joke or drop a pop-culture reference, especially right after a dry `[SYSTEM]` line (start that beat with `[GM]`).

## Supersedes / clarifies

- Decision **007** (tag names exist) stays; this decision defines **what content** each tag carries.
- Earlier table notes that treated achievements / loot-box reveals as `[SYSTEM]` or that said "GM and System share one voice" are **superseded** for spoken tagging.
- Canon System AI snark in `lore/catalog/system-voice.md` still guides **joke tone**; at this table those jokes are spoken under **`[GM]`**.

## Consumers

- Discord voice bridge: `src/tags.js`, `src/encounter/extract.js` (`SYSTEM_KINDS` allow-list; unknown kinds = GM), OpenAI System TTS instructions default.
- Campaign tools: `tools/encounter_text.py` (same allow-list), `tools/discord_gm.py` tag blurb.
- GM-facing docs: `gm-notes/00-gm-principles.md`, `gm-notes/20-gm-persona.md`, `rules/40` §2.5, `rules/45` announce steps, `bot/README.md`.

## Follow-up

- Encounter Bot: scrub Day-page System `voice_line` / `route_voice_line` snark; move achievement/loot color to GM; optional joke beats use manifest kind `gm_color` (extract/encounter_text treat unknown kinds including `gm_color` as narration; `/encounter` preview lists the kind).
