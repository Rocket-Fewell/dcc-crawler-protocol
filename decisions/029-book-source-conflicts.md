# Decision 029: Book source conflicts (SRD vs non-SRD, Reprieve default, Floor 2 timer)
Owner: Syndicate | Status: final | Version: 1.0 | Updated: 2026-10-04
Summary: Rulings that settle source conflicts found by the Book Author: SRD-only content is printed in the book; non-SRD backgrounds and feats are table/GM appendix material (our own reskin names and mechanics summaries only); the Floor 2 house timer is 10 days; the Floor 1 Reprieve is ON by default for Season Zero Floor 1 and never covers a collapse death.

Filed 2026-10-04 on rulings already made (item 4 confirmed by Caleb, 2026-10-04). Apply them; do not re-ask.

1. **SRD-only content is printed in the book.** The book prints only content that is in the SRD 5.2 (and our own original text). Nothing from the 2024 PHB, DMG or Monster Manual outside the SRD is reproduced.
2. **Non-SRD backgrounds and feats are appendix material.** Backgrounds and origin feats listed in /create S7 and `tables/chargen-5e.json` that are not in the SRD are treated as **table/GM appendix** material, not printed rules text. In the appendix each one appears under **our own reskin name** (`tables/background-reskins.json`, display names) with a **short mechanics summary in our own words**. No non-SRD text is copied. The plain 5e names and the numbers stay in the data tables and state, unchanged.
3. **Floor 2 house timer is 10 days.** This is the house rule (decision 026: Floor 1 = 5 days, Floor 2 = 10, Floor 3 = 20). The canon figure of 6 days for Floor 2 is **reference only** and is not the rule at this table.
4. **Floor 1 Reprieve default.** The Reprieve is **ON by default for Season Zero, Floor 1 only**; a table may turn it off at session zero (`F1-REPRIEVE: ON/OFF`). It **never applies to a death from a missed floor collapse**: that is death on every floor, no Reprieve, no toll (decisions 026 and 028). The Detour Tax covers only a missed Stairwell key. This replaces the older wording "default OFF in the rules, ON for this campaign" and the Floor 1 collapse default in decision 026 item 2 (already superseded by the 026 Caleb ruling of ~10:02 PM CT).
5. **Ability-score Roll threshold (verification note).** The keep threshold is **73 or more** (above 72, the standard array total). Sources: decision 024, `tables/chargen-5e.json` `ability_methods.roll.keep_min_total` = 73, and the bridge constant `ROLL_MIN_TOTAL = 73`. Book text should say "73 or more".

- **Files:** `rules/10-core-rules-5e.md` v0.2.15 (§5.8, §5.10, §6.0, §6.2, §6.8), `characters/character-creation-5e.md` v0.2.4, `tables/chargen-5e.json` v0.1.6 (notes cite the current version), `STATE-OF-BUILD.md` v0.1.5.

## Addendum (2026-10-04, Syndicate): print format for non-SRD backgrounds and feats
Source: Lore's `drafts/srd-nonsrd-audit.md` (sha256 8ee1c6072bfc9266f4f5e512b0079e1c36e4ea64ace6ba1f3ea74b0473140481; SRD 5.2.1, CC-BY-4.0). The SRD has 4 backgrounds (Acolyte, Criminal, Sage, Soldier) and 4 origin feats (Alert, Magic Initiate, Savage Attacker, Skilled).
Ruling: the printed book shows the 4 SRD backgrounds and the SRD origin feats in full. The 12 non-SRD backgrounds and 6 non-SRD feats (Crafter, Healer, Lucky, Musician, Tavern Brawler, Tough) go in a table appendix under our reskin names only, with our own mechanics summaries, no parenthetical 5e name and no copied book text. Human's Versatile feat picks from the 4 SRD feats. Caleb may veto.
