# How a grok bot draws an encounter
Owner: Cursor (R&D) | Status: draft | Version: 0.1.0 | Updated: 2026-10-09
Summary: Steps for building a random Floor 1–3 fight from this folder without inventing a budget.

1. Read the party size and the floor. Floor 1 before the Green Room is budget level `L1`. Floor 1 boss day after the Green Room is `L2`. Floor 2 is `L2`. Floor 3 is `L3`.
2. Pick a tier: `trivial`, `standard`, `hard`, or `boss`.
3. Read the XP budget and the CR cap from `rules/70-encounter-budget-5e.json` at `floors.<n>.tiers.<band>.xp_budget_total.<party>.<tier>` and `cr_caps`. Do not type a new number.
4. Load `monsters/f0N.json`. Keep a card only when `fits_rules_70_cr_cap[band][party][tier]` is true.
5. Mobs and units fill trivial and standard fights. Elites fill hard fights. Boss cards fill boss fights. A boss fight may add mobs that still fit the cap.
6. Add `xp` times count. Stop at or under the budget. Going over is not a draw.
7. On a clear, grant that XP through the existing state tools. The card's `state_hooks.on_clear_xp` is the per-creature XP, not a new award.
8. A toast, if any, comes from `achievements/catalog.json`. R0 is snark. R2 is Heroic Inspiration. Do not attach a box from this folder.
9. Gear, if any, comes from `items/catalog.json` and still uses the SRD item. List price is the reskin file. It is not a new vending price.
10. Announce with the card's `system_line`, then a [GM] line. Nameplate format is core §8.4.
11. Do not write `sessions/`, `sessions-data/`, `characters/`, or a credit ledger from this folder.
12. If a live Day page already has this fight, use the Day page.

`encounters/sample-recipes.json` is eleven lineups already checked against the 4-Crawler budgets. Copy the shape. Do not treat them as Day specs.

Room cards, when Encounter Bot wants them, can point `encounter.by_party_size` at these ids. The stat block on the card is the SRD block. Encounter Bot still owns `floors/`.
