# decisions index
Owner: see NAMING-CONVENTIONS.md | Updated: 2026-10-04

- 002-death-mode.md: Costly Revives, very costly and rare
- 003-death-bypasses.md: earned death bypasses
- 004-crafting-system.md: crafting added, owners
- 005-death-mode-tuning.md: Costly Revives numbers (follow-up to 002) and Special Brew mapping. Owner: Syndicate.
- 008-crafting-rules.md: crafting rules follow-up to 004 (Caleb framework + Syndicate numbers). Owner: Syndicate.
- 009-species-approach.md: species approach approved
- 010-first-crafting-table.md: Floor 2 drop, rare Floor 1, usable Floor 4
- 011-crafting-settings.md: crafting settings approved
- 012-crafting-economy-explosives.md: economy and Boomer cap (v1.1: basic table 5,000)
- 013-party-size.md: four players
- 013-crafting-open-questions.md: Caleb's answers to the 12 crafting open questions (shares number 013 with party size; rules call it "decision 013-crafting")
- 014-one-active-session-bridge.md: draft, one active session per bridge
- 015-story-boxes.md: Legendary Story Boxes on Floor 1 (approved; v1.1 tradeable, per-floor cap; v1.3 unopened box reclaimed at death frees its slot)
- 016-s12-dropped.md: S12 dropped, no public Fan Profile tags screen (approved)
- 017-busted-spontaneous-callout.md: Busted is a spontaneous callout, valid only in a scene with a logged tell (approved)
- 018-story-box-answers.md: Story Boxes approved with Caleb's answers (saferoom only, tradeable, sellable, rival rule, pet-Crawler, rota guideline, buyback by rung)
- 019-credit-multiplier-fees.md: floor credit multiplier on fees and rewards, not on box credit pulls (v1.2: Studio 12,000, Enhanced Studio 30,000)
- 021-multi-crawler-tooling.md: how decision 020 is built (status, session-status marker, request/activate swap, crawler delete order and archive, channel overflow, item-reskins single source and variant picks)
- 020-multiple-crawlers-active-swap.md: many Crawlers per player, one active, benched Crawlers inert, swaps only outside an open session, one text channel per Crawler, /delete (final-pending-Caleb-override)
- 022-pets-and-companions.md: pets and companions (Caleb approved; GM-filed only from the player's own free text, never offered; Beast CR 1/4 or lower; no slot, death final; two off-menu pet items; Biscuit unchanged)
- 023-pets-tooling-and-audit-fixes.md: how GM-run pets are built (`state.py pet ...`, `limits.pets_enabled`, off-menu items by `pet shop`, nothing in /create) and the independent-audit fixes (archive, ownership, session marker, benched guards, Story Box --reaward)
- 024-roll-method-ability-scores.md: Roll as a third ability-score method in /create (three arrays of 4d6 drop lowest, keep ONE totalling 73+, reroll all three if none qualifies, every die logged, switch `create.allow_roll` default ON). Owner: Syndicate.
- 025-species-class-display-names.md: Nationality display names for species, lineages, classes and class options ("Our Name (5e Name)"); species variants (Cat Girl, Tigran, Were-Cat and so on) are cosmetic with a `base_id`, no rules change. Owner: Syndicate.
- 026 timed floor clock override (2026-10-04)
- 027-encounter-budget-v0-1-0.md: encounter budget v0.1.0 filed (rules/70-encounter-budget-5e.json + .md; XP budgets, CR caps, credits and box odds for Floors 1-6, F1+F2 about 1,274 credits per Crawler against the ~1,500 line, F1 rest/key/Detour Tax/Zone S prices, Day 1 slot map). Owner: Syndicate. Budgets are guidelines.
- 028-collapse-death-loot.md: missed collapse = death; the dead Crawler's credits and items are destroyed with the floor, survivors may loot only while it stands (Story Box and Legendary items too), "floor lost" ledger write-off must record exact coins and items so the balance reconciles to zero, and pre-collapse loot is logged as a transfer first (canon-shaped, tagged inspired; Caleb, 2026-10-04). Owner: Syndicate.
