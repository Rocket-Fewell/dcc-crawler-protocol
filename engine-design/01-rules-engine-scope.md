# Engine v1: Rules-Engine Scope
Owner: Syndicate | Status: draft for the room | Version: 0.1.0 | Updated: 2026-10-07
Source: `engine-design/00-source-grok-conversation.md` (Caleb's direction, 2026-10-07 9:44 PM CT). Rules authority: `rules/10-core-rules-5e.md` (5e 2024 + house rules), `rules/70-encounter-budget-5e.json`, `gm-notes/45-gm-quick-calls.md`.

## 1. The split
- **Code decides.** Every number in a turn (to-hit, damage, saves, HP, conditions, uses, credits, initiative, turn order) is decided by code that already exists or gets built here. The model never does arithmetic and never looks up a rule.
- **The fast model narrates.** It gets a short snapshot (section 4) after the result is final and writes 2-4 sentences in the System/GM voice. It does not use tools.
- **The strong model judges.** It is called only when the parser can't map a player's line to an action in section 2, or the action is tagged `ruling`. It returns a structured ruling (section 5), which code then resolves like any other action.
- **Agents build.** Bots and Cursor change code and content between sessions. No agent is in the live turn loop.

## 2. Actions code resolves (no model needed for the math)
Build on what already exists: `tools/state.py` (`hp`, `condition`, `death-save`, `uses`, `resource`, `proficiency`, `enemy`, `inventory`, `credits`, `pet`, `loot`, `box`, `sell`, `transfer`, `scene`), `tools/roll.py` and `tools/loot.py`. Turn them into an importable library that the bot process calls in memory. Keep the CLI as a thin wrapper.

| Action | Code does | Rule source |
|---|---|---|
| Attack (weapon, unarmed, spell attack) | d20 + mod + PB (+ adv/dis), vs AC, crit on nat 20, damage dice + mod, resistances and vulnerabilities, apply HP | 5e 2024 |
| Saving throw / ability check / skill check | d20 + mod (+ PB if proficient), vs DC, adv/dis | 5e 2024, proficiencies from the sheet |
| Damage and healing | Apply to HP, temp HP, drop to 0 then Unconscious and death saves, instant death on overflow | 5e 2024 |
| Death saves | Player rolls (or GM auto-roll when the table says go); 3 successes = Stable, 3 fails = dead, then the Floor 1 Reprieve check | core §6, decision 026 |
| Conditions | Set and clear, with durations by round or by save; each one's effect on rolls is applied automatically (Prone, Grappled, Poisoned, Restrained, Unconscious, Burning, etc.) | 5e 2024 |
| Initiative and turn order | Roll, break ties by Dex, track round, current turn, and which pets act on their owner's turn | 5e 2024, rules/60 |
| Movement and cover | Distance on the room card's zone grid; half / three-quarters cover from the card | room cards |
| Action economy | One action, one bonus action, one reaction, free object interaction, movement; refuse a second action and say why | 5e 2024 |
| Class features | Only what's on the sheet, with uses (Second Wind, Sneak Attack once per turn, Rage, Martial Arts, Cunning Action at Rogue 2+, spell slots) | 5e 2024 + sheet |
| Items with `uses` | Spend and refill on the `uses_reset` trigger; single-use means the whole item | core §5.9, decision 038 |
| Inventory, System Inventory | Store or retrieve (free object interaction or Utilize; Intake Bag gives one free swap per turn), 500 lb / 64 cu ft cap | core §5.9 |
| Ammunition | Subtract 1 per shot; recover half (rounded down) after the fight | 5e 2024 |
| Rests | Short Rest (Hit Dice), Long Rest, rest fee outside a saferoom | core §5.6, decision 031 |
| Credits, vendor, selling | Snakk-Matic list, buy-back at half, haggle DC 13 = 15% off | overview §5.6, rules/70 |
| Loot and boxes | Deck draws per `rules/40`, box odds per rules/70, opened only in a saferoom | rules/40, rules/45 |
| Enemy turns | Stat block from the room card: target pick (default: nearest standing Crawler; the room card can override), attack, damage | room cards, rules/70 |
| Clock | Floor day, Ceiling Tick rolls, collapse warnings | floor docs, core §5.8 |
| Achievements | Deterministic triggers (first crit, first kill, win initiative, intake) fire from code; anything that depends on taste goes to the strong model | core §3, the decks |

## 3. What stays a GM judgment (strong model, logged)
Improvised actions (throwing a mannequin, lighting a mop), odd uses of items, NPC reactions and dialogue beyond the voice sheet, tailored achievement rewards, secrets whose trigger is a matter of taste, and "can I reach that?" geometry not on the card. Every ruling is written to `gm-notes/10-open-threads.md` tagged POST-SESSION REVIEW, automatically.

## 4. Narrator snapshot (what the fast model sees each turn)
Keep it under ~600 tokens: the current room card's description line and visible features; the acting Crawler's name, HP, conditions and the action just resolved, with the exact rolls and results; anything that changed for other combatants; whose turn is next; the persona block from `gm-notes/20-gm-persona.md`; and the length rule from `gm-notes/00-gm-principles.md` (Caleb said s1's length was right). It never gets secrets that haven't been revealed, unrevealed room cards, or rules text.

## 5. Ruling handoff (strong model in, code out)
Input: the player's line, the snapshot, the room card (including its secrets and GM notes), and the relevant rule excerpts the code picks by tag. Output, as JSON only:
`{"ruling": "one sentence", "resolve_as": "attack|save|check|damage|heal|condition|move|item|none", "params": {...}, "log": "why"}`
Code validates `params` against section 2 and runs it. If it can't validate, it falls back to "the System says no, try something else" and logs it. The model never sets HP or credits directly.

## 6. Things Caleb already decided that the engine must keep
Players are Crawlers. 5e 2024 + homebrew. Loot and Story Boxes open only in saferooms. Floor 1 Reprieve is on. A missed floor collapse is death. Achievements are guidelines, and snark-only rewards are allowed. Mr. White's spelling and the other canon names come from Lore's ledger. GM goes fast at the table and shaky calls are reviewed afterward.

## 7. Done means
A scripted replay of the 2026-10-07 Shooting Gallery fight (from `sessions-data/s1/rolls-2026-10-07.log` and the transcripts) runs through the engine with the same dice. Every number matches 5e 2024, one source sets the mannequin to-hit, Cunning Action is refused at Rogue 1, and no turn takes more than ~3 seconds before the voice starts.
