# Player Channel Card Format (proposed)
Owner: AI GM | Status: draft | Version: 0.2 | Updated: 2026-10-04
Summary: Proposed text format for the per-player Discord channel (e.g. #hornn) where the System posts character state and inventory changes as a running thread. Source of truth stays sessions/state.json; the publisher reads it and posts.

## Two kinds of posts
1. **Change post** (every time state changes, one short post per event):
```
[Floor 1 | Break Room] Horn
Credits: 25 -> 75 (+50, Bronze box pull)
+ Pebbles Snow Globe (Driftglobe, Uncommon): command word to light/douse (no action); floats; 1 hr, no charges
```
2. **Full sheet card** (pinned/reposted after a rest, level-up, or on request):
```
HORN - Human Wizard 1 (Hornn)   HP 8/8  AC 11  Credits 75  XP 0
STR 12 DEX 12 CON 15 INT 17 WIS 13 CHA 15
Conditions: none   Boxes: none   Titles: (list)
INVENTORY
- Box Cutters x2 (Dagger): 1d4 piercing, finesse, light, thrown 20/60
- ...
ACHIEVEMENTS: name - reward
```
## Rules
- Every item shows real mechanics under its reskinned name (see 00-gm-principles.md, item detail).
- Each credit change shows old -> new, the amount, and the source (the credit ledger Accountant asked for).
- Secrets never appear: GM quirks, affinity, the hidden Fan Profile, survey answers and opt-outs.
- Benched Crawlers' cards carry a BENCHED header (see 00-gm-principles.md, Multiple Crawlers).
- Needs per-item `notes` in state.json inventory (already supported) and a per-change `reason` field.

## Combat block (Caleb, 2026-10-07 10:39 PM CT: cards must show this)
Every card shows, right under the HP/AC line, computed from the build (never hand-typed):
- **Attacks:** one line per weapon and attack cantrip: name, to-hit, damage and type, range, key property. Example: `Eldritch Blast: +6 to hit, 1d10 force, 120 ft`.
- **Spellcasting:** save DC, spell attack bonus, and slots as used/max with when they come back. Example: `Pact Magic slots 1/1 (level 1), back on a Short Rest | Save DC 14 | Spell attack +6`. Every known spell with one-line mechanics.
- **Features and traits:** class features, species traits and feats, each with uses as used/max and its reset (Second Wind 1/2 per Short Rest, Rage 2/2 per Long Rest, and so on).
- **Rests:** Hit Dice used/max with the die size, and the party's Short Rests used today out of 4.
- **Death saves:** shown only when at 0 HP, as successes and failures.
Uses and slots update on the card the moment they're spent.
