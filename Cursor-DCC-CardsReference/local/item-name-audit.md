# Item name audit
Owner: Cursor (R&D) | Status: draft | Version: 0.3.0 | Updated: 2026-10-09
Summary: Which gear names changed, and which Lore names were already a picture.

Lore's filed name stays on `lore_display_name`. The live reskin table was not edited.
A future local engine shows `display_name`. Prices were not changed.

## Punched up

| Card | Was | Now |
|---|---|---|
| `cdr-gear-sickle` | Garden Sickle | Orange Weed-Whacker Sickle |
| `cdr-gear-dart` | Bar-Room Dart | Sticky Bar Dart, Two Short of a Set |
| `cdr-gear-battleaxe` | Wood-Splitting Axe | Firewood Axe, People Count as Wood |
| `cdr-gear-warhammer` | Framing Hammer | Stud-Finder Framing Hammer |
| `cdr-gear-parchment` | Printer Paper | Shrink-Wrapped Ream of Printer Paper |
| `cdr-gear-iron-pot` | Cast-Iron Pot | Cast-Iron Pot, Still Has Chili |
| `cdr-gear-pouch` | Ziplock Pouch | Suspicious Ziplock Pouch |
| `cdr-gear-shovel` | Snow Shovel | Off-Season Snow Shovel |
| `cdr-gear-tinderbox` | Matchbook | Matchbook from a Bar That Burned |
| `cdr-gear-gaming-set` | Deck of Cards | Deck of Cards, Ace Already Missing |

Kept Lore's name on 181 cards. Those names already show the object.
Attack or AC lines are on 52 cards. Weapons cite `srd/srd.txt`. Armor and shields cite `tables/chargen-5e.json`.
Gear with no filed attack or AC line is marked `local.playable` false. The engine must not invent a number for those.
