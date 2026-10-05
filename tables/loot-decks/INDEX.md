# Loot decks (campaign root)

Symlinks to Lore's deck files in `/workspace/dcc-lore/tables/loot-decks/` (source of truth: Lore). `state.py loot draw` reads from here.
Only deck files (`f01-*.json`, schema `loot-deck/*`) are linked; the achievements file (`ach-*.json`) is intentionally not linked.
