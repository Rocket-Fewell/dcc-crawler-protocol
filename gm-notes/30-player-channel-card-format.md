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
