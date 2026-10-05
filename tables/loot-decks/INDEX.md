# Loot decks (campaign root)

Relative symlinks (`../../lore/tables/loot-decks/<deck>.json`) to Lore's deck files in `lore/tables/loot-decks/` (source of truth: Lore; `lore/` is a symlink on the box and a real folder in the GitHub repo, so the links resolve in both). `state.py loot draw` reads from here.
Only deck files (`f01-*.json`, schema `loot-deck/*`) are linked; the achievements file (`ach-*.json`) is intentionally not linked.
