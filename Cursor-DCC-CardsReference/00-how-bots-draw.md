# How a grok bot draws an encounter
Owner: Cursor (R&D) | Status: draft | Version: 0.3.0 | Updated: 2026-10-09
Summary: Steps for building a random Floor 1–3 fight from this folder without inventing a budget.

1. Read the party size and the floor. Floor 1 before the Green Room is budget level `L1`. Floor 1 boss day after the Green Room is `L2`. Floor 2 is `L2`. Floor 3 is `L3`.
2. Pick a tier: `trivial`, `standard`, `hard`, or `boss`.
3. Read the XP budget and the CR cap from `rules/70-encounter-budget-5e.json` at `floors.<n>.tiers.<band>.xp_budget_total.<party>.<tier>` and `cr_caps`. Do not type a new number.
4. Load `monsters/f0N.json`. Keep a card only when `fits_rules_70_cr_cap[band][party][tier]` is true.
5. Mobs and units fill trivial and standard fights. Elites fill hard fights. Boss cards fill boss fights. A boss fight may add mobs that still fit the cap.
6. Add `xp` times count. Stop at or under the budget. Going over is not a draw.
7. On a clear, grant that XP through the existing state tools. The card's `state_hooks.on_clear_xp` is the per-creature XP, not a new award.
8. A toast, if any, comes from `achievements/catalog.json`. R0 is snark. R2 is Heroic Inspiration. Do not attach a box from this folder.
9. On each creature, read `tracked_uses`. Spend one from a pool when that spell or trick is used. At-will rows have `max` null and may repeat. A `shared_spell_pool` spends one use no matter which listed spell was chosen. A `recharge` row stays down until a d6 at the start of that creature's turn hits `recharge_on`. When a numbered pool is 0, use weapon or natural attacks. Do not refill daily uses until a Long Rest in a saferoom, and do not invent slots.
10. Mundane gear comes from `items/catalog.json`. List price is the reskin file. It is not a new vending price. Category headers with `resolve_to_variant` true are not for sale until a variant id is picked.
11. A loot box, if a deck already allows one, comes from `items/loot-boxes.json`. Use the filed deck card. Spend `tracked_uses` on charges (a wand at 0 does not fire; a healer's kit at 0 does not stabilize). `rules_40` rows with status `candidate` are proposals, `draw_weight` 0. Do not roll them.
12. Announce the picture name (`display_name`), then the card's `system_line`, then a [GM] line. Do not say the SRD name out loud unless a Crawler asks what the math block is. Nameplate format is core §8.4. Read `picture` and `house_flavor.card_note` before you invent a story. Dean Thudd on the Day pages is the Floor 1 boss. This pack does not replace him. A local engine, when one exists, rolls `local.attacks` and does not ask a model for the dice. See `local/00-how-local-play-works.md`.
13. Do not write `sessions/`, `sessions-data/`, `characters/`, or a credit ledger from this folder.
14. If a live Day page already has this fight, use the Day page.

`encounters/sample-recipes.json` is eleven lineups already checked against the 4-Crawler budgets. Copy the shape. Do not treat them as Day specs.

Room cards, when Encounter Bot wants them, can point `encounter.by_party_size` at these ids. The stat block on the card is the SRD block. Encounter Bot still owns `floors/`.
