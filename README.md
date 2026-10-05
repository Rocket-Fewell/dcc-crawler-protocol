# DCC campaign: rules, floors, tools and canon (local staging repo)

Design and tooling repo for the Dungeon Crawler campaign run on Discord: house rules, decisions, Floor 1 day pages, loot/achievement/reskin tables, the Python campaign tools and their tests, and Lore's canon tables and ledger. Start with `INDEX.md` and `STATE-OF-BUILD.md`.

## Layout
- `rules/` house rules (5e core, crafting, species, loot decks, story boxes, pets, encounter budget). `decisions/` numbered decision records (026 timed floor clock, 028 collapse death and loot).
- `floors/` the Floor 1 campaign narrative and day pages (`floors/f01/`). `tables/` generated tables (achievements, loot decks, reskins, chargen).
- `tools/` Python campaign tools, `tools/tests/` the unittest suite, `tools/encounter_bot/` the Encounter Bot, `tools/check_repo_safe.py` the safety check.
- `characters/` character-creation rules and the /create flow spec only. `lore/` Lore's tables and the canon ledger (`lore/CANON-LEDGER.md`).

## Not in this repo (by design)
Live state and secrets never go in: `gm-notes/secret/`, `sessions/` (state.json, credit ledger, backups, session.json), `.env`, `bot.log`, `node_modules/`, tokens, webhook URLs and API keys, the live player sheets under `characters/`, and the bot's own source (`discord-voice-bridge`). `.gitignore` covers them, and `tools/check_repo_safe.py` blocks them even with `git add -f`.

## Safety hook
Run `sh tools/install_hooks.sh` once after cloning or creating the repo; it installs `tools/hooks/pre-commit`, which runs `python3 tools/check_repo_safe.py --staged` and refuses the commit if a staged path is forbidden or a staged file matches a secret pattern (Discord bot token shape, Discord webhook URL, `GM_WEBHOOK_*=value`, API-key-like assignments, OpenAI/Google/GitHub/Slack/AWS key shapes, private-key blocks). It never prints the matched text. Run `python3 tools/check_repo_safe.py --tree .` to scan the whole working tree. Tests: `cd tools && python3 -m unittest discover -s tests -p 'test_*.py'`.

## Push procedure (for tomorrow, only after Caleb approves)
Do nothing until Caleb says go. Then: confirm the hook is installed (`ls .git/hooks/pre-commit`), run `python3 tools/check_repo_safe.py --tree .` and `git status` (must be clean, one commit by "Borent Architect"), create a **private** repository on GitHub under the account Caleb names (never public, never initialised with a README or licence so history stays unrelated-free), add it with `git remote add origin <url>`, review `git log --stat | head` once more, and push with `git push -u origin main`; afterwards check on GitHub that the repo shows as Private, that none of `gm-notes/secret/`, `sessions/` or `.env` exist in it, and rotate any credential immediately if the checker ever reported a hit. Use a fine-grained token or the `gh` login Caleb provides at that time, and do not store it in the repo.
