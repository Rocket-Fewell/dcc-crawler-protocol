# Decision 024: Roll method for ability scores in /create
Owner: Syndicate | Status: final | Version: 1.0 | Updated: 2026-10-04
Summary: `/create` S8 offers a third ability-score method, Roll (the method used at the first character creation): the System rolls three arrays of six scores (4d6, drop lowest), the player keeps ONE array that totals 73 or more, then assigns the scores to abilities. If none of the three qualifies, the System rerolls all three. Every die is logged. Switch: `create.allow_roll`, default ON. Standard array and point buy are unchanged.

- **Approved by:** Caleb (asked for it); spec agreed by the GM and Lore, 2026-10-04. Number 024: 023 was taken (pets tooling). No earlier decision covers ability generation, so this is a new file.
- **Ruling.**
  1. Methods at S8: Standard array (15, 14, 13, 12, 10, 8), Point buy (27 points), Roll. 2024 rules still apply: background increases (+2/+1 or +1/+1/+1) are added after assignment.
  2. **Roll:** 3 arrays x 6 scores, each score 4d6 drop lowest (`roll.py "4d6dl1"`). The player keeps ONE array, and only an array whose six scores total **above 72 (73 or more)** may be kept. **No upper limit on the total** (Caleb). The player assigns each score to the ability of their choice.
  3. **None qualifies:** the System rerolls all three arrays, and repeats until at least one qualifies. There is no voluntary reroll.
  4. **Logging:** every die roll goes to the roll log through `tools/roll.py` (one `[ROLL]` line per score, rerolled rounds included).
  5. **Switch:** `create.allow_roll` (session `create` settings, same place as `review_mode`), **default ON**. Off = Roll is hidden at S8 and nothing else changes. This replaces the old default-OFF `create.allow_roll` of spec v0.1.9 (same name, new default and meaning).
  6. **Cap:** one 4d6-drop-lowest score is 3 to 18. A background +2 can reach 20 at most; +1 reaches 19. No score may go above 20 after background increases (2024 rule); the tool still clamps and refuses above 20.
- **Math (Lore's figure checked by Syndicate, exact enumeration):** P(one array totals 73+) = 56.2%; P(all three miss) = 8.4%. Total of six scores ranges 18-108, mean 73.5. **Correction to the spec note:** the standard array totals 72, but point buy does not always: with 27 points the most a point-buy set can total is 75 (e.g. 13,13,13,12,12,12). The rule stays as agreed (73 or more); it just is not "always above both other methods".
- **Supersedes:** GUIDE §3.6 "rolling only if the table agrees, one reroll set for the whole table" and spec Open Q1 (resolved).
- **Design defaults (Syndicate, Caleb may override):** the rolled arrays are saved in the draft and shown again on Back/Edit/Restart (no free rerolls); auto-reroll safety stop after 10 rounds (then the player is sent to the other two methods).
- **Files:** characters/create-flow-spec-5e.md v0.1.10 (S8, checklist, Architect lines); characters/character-creation-5e.md v0.2.3 (§3.6); tables/chargen-5e.json v0.1.4 (`ability_methods`); rules/10-core-rules-5e.md v0.2.12 (§10.1 pointer). Architect builds the code and `tables/create-flow-lines.json` lines (spec §3.6).
