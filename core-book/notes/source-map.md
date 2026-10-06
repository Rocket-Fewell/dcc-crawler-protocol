# Source Map
Owner: Valtay Corp - Core Book Author | Status: draft | Version: 0.5 | Updated: 2026-10-06
Summary: Which source fed which chapter, with versions and known conflicts.

| Chapter | Sources |
|---|---|
| 1 | rules/10-core-rules-5e.md v0.2.22; rules/70-encounter-budget-5e.json v0.2.6 (floors.1.achievement_rewards, floors.2.boxes.f2_box_rulings); rules/40-loot-deck-spec-5e.md v0.1.9; rules/20-crafting-5e.md v0.3.7+; decisions 018, 026-031, 033, 034; characters/character-creation-5e.md v0.2.5 |
| 2 | decision 036; rules/30-species-supplement-5e.md v0.2.1 (§2.0, §2.3, §3, §3.2a, §3.7); core v0.2.21 (§7 re-checked against v0.2.23); characters/character-creation-5e.md v0.2.5; characters/create-flow-spec-5e.md v0.1.13; tables/chargen-5e.json v0.1.6; species-class-reskins v0.1.7; background-reskins v0.1.2; create-screens-reskins v0.1.3; decisions 024, 029, 033 |
| 3 | decision 036 (species, Floor 3 Identity Market); decision 025 (cosmetic variants); decision 037 (skill families); rules/30-species-supplement-5e.md v0.2.3 (Latent Biology, tells, Offer, Unbroken Original, rebuild, Large Crawlers §3.8, natural weapons, oddity stat blocks, §2.9 class options locked); rules/10-core-rules-5e.md v0.2.23 (§6.3, §6.5.1, §7.1-7.3); characters/character-creation-5e.md (header v0.2.5, change log v0.2.6); species-class-reskins v0.1.7 (display names; class options locked); SRD 5.2 (CC-BY-4.0) species traits by name |
| 4 | same chargen + reskins as Ch2; decisions 024, 029, 033; core v0.2.17 overlays (rests, Midterm Onboarding, credits); SRD 5.2 class/background chassis |
| 5 | decisions 036, 037 (System skill track); rules/10-core-rules-5e.md v0.2.23 (§6.3, §6.5.1 added; §1.1, §2.5.1, §2.5.5, §2.5.6, §3.1-3.9, §4.1-4.2, §4.4, §4.8, §6.5 Cockroach Clause, App. A-C); rules/40-loot-deck-spec-5e.md v0.1.9 (§2.2, §2.4, §2.9); rules/70-encounter-budget-5e.json v0.2.6 (F1/F2 achievement box rulings only; no totals); rules/20-crafting-5e.md v0.3.7 (§1, §3 crafting skills); tables/achievements.csv v1.4 (1,835 rows; 72 curated rows); create-screens-reskins v0.1.3 (ability display names; skill names plain); lore CANON-LEDGER v1.20 (M-008, M-009/S-001; A-034, A-044, A-047, A-131, A-136, A-139 VERIFIED; A-151 WIKI-ONLY); lore catalog/skills.md v1.0, mechanics-clarifications §3 (WIKI); SRD 5.2 (CC-BY-4.0) ability checks, skills, actions, tools |

## Conflicts (superseded text, resolved in favor of decisions)
- Core older "Reprieve default OFF" / haul-down: superseded by 026/028/029 (ON default; collapse death everywhere).
- character-creation stale "Credits = GP" display / Cardboard Box / gold wording: fixed in v0.2.4–0.2.5.
- Spec S7 16 backgrounds / 12 Origin feats vs SRD 4 / 4: printed SRD full; non-SRD appendix reskin-only (029).
- Canon Floor 2 timer 6 days vs house 10 days: house wins (029).
- F4-6 day counts: house 20/25/30 (027/budget v0.1.4+); F7-18 not printed.
- Legendary cap 2 is per Crawler; Story Boxes separate track (018, budget v0.1.11, core §4.5).
- Achievement box tier on Floors 1-2: core Appendix A says a Legendary-loot achievement pays Silver on F1-2; budget floors.1.achievement_rewards (R5 = Bronze on F1-2, Silver only as the Boss Box) and floors.2.boxes.f2_box_rulings (Syndicate 2026-10-05 18:36, soft 2-3 per Crawler per floor per Caleb ~21:15) say Bronze. Floor rules outrank core (core §0), so Ch1/Ch5 print Bronze. **Resolved in core v0.2.22:** Bronze on F1-2; Silver only from the Boss Box or a stated GM override (Q20 closed).
- Canon skills level by use and cap ~15 (M-008): campaign has no general skill-leveling rule; only crafting skills (rules/20 §3) and the Cockroach Clause (core §6.5). **Resolved by decision 037 / core v0.2.22:** general skill track printed in Ch5 (Q19 closed).
- **Ch3 / decision 036 vs rules/30 (2026-10-06):**
  - rules/30 on disk is v0.2.1 (the brief said v0.2); v0.2.1 used.
  - Sapper workshop: rules/30 and rules/20 say "any honest saferoom", 036 says "any saferoom". Printed "any saferoom" plus "A false saferoom is not a saferoom, and has no workshop."
  - Hobgoblin gate Explosives Handling 5 vs the skill track (rank 5 not before Floor 4, rules/20 / Ch5): at the Floor 3 Offer only the GM waiver can open it. Printed both as written; flagged as an open question.
  - Caprid: one rules/30 breed note reads as Small, but 025 makes breeds cosmetic. Printed as cosmetic: no Caprid is Large, size per the stat block.
  - Nodling: rules/30 describes two heads only; 025 lists head variants as cosmetic. Printed as cosmetic.
  - Felid Nine Lives "If it triggers" wording ambiguous; printed "When it triggers".
  - rules/30 §1.4 has a duplicated table; ignored the duplicate.
  - character-creation header says v0.2.5, change log v0.2.6; cited both.
  - Ch2 still describes some kiosk tooling (pre-existing; open question 14). Not touched in this pass.
