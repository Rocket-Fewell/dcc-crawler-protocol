# Loot Deck Spec (5e Overlay)
Owner: Syndicate | Status: draft | Version: 0.1.6 | Updated: 2026-10-04
Summary: JSON card and deck-file format for pre-built per-floor/zone loot decks (every card says exactly what the item is and does), GM draw rules, a starter 5e item stat reference for Floors 1-2, five sample cards, a Legendary Story Box rule (§2.8), and open questions.
Depends on: rules/42-house-items-f01.md v0.2.2 (final text for the four house items and the Enhanced Pet Biscuit), rules/10-core-rules-5e.md v0.2.8 (§3.5 tailoring, §3.6 ceilings, §4 loot boxes incl. the Story Box exception; wins on any conflict), rules/45-story-boxes-5e.md v0.2 (Story Box design), decisions/015-story-boxes.md, gm-notes/30-player-channel-card-format.md, gm-notes/00-gm-principles.md ("Loot box and item detail", "Achievement announcements"). Consumers: DCC Lore (writes decks), AI GM (draws and reads), Borent (`state.py loot draw <floor> <zone>`, Discord bridge), the Accountant (credit audit), Valtay Corp core book (formats item entries from these fields).

> **Status:** DRAFT v0.1.5. Nothing here is LOCKED except the Story Box exception (§2.8), which Caleb approved on 2026-10-04. Six tiers and the Celestial cap (one per crawler) are LOCKED in core §4 and only referenced here. **Project:** *Crawler Protocol: Season Zero*, private fan RPG inspired by *Dungeon Crawler Carl*.
> **Why this exists:** Caleb's alpha-run feedback (2026-10-04): loot box items lacked detail. Rule: **every item states exactly what it is and what it does.** A card is the unit that makes that impossible to forget.
> **Scope:** format and procedure only. Box tiers, pulls (d100) and credits-per-pull stay in core §4.2.
> **Tags:** `CANON` = fact tied to a CANON-LEDGER entry; `CANON-INSPIRED` = shaped by canon but not a canon item; `HOUSE` = our invention. `VERIFY` = I was not sure of the exact 2024 number/rarity; check the SRD 5.2 / 2024 DMG before a card goes live. Canon claims here: tiers L-001, saferoom opening L-002, semi-random contents L-003, Pet Biscuit I-007, limited stat potions K-159 (all ledger VERIFIED, wiki-sourced, **not** checked against the novels). Voice skeletons come from `dcc-lore/catalog/system-voice.md` §1.2 (paraphrased, no quotes copied).

## Contents
1. Card schema and deck file (field list in one place)
2. Rules for the GM drawing cards
3. Starter stat reference (Floors 1-2)
4. Five sample cards
5. Open questions for Caleb

---

## 1. Card schema and deck file

**Format: plain JSON** (UTF-8, one deck per file, no comments, no trailing commas). Path: `tables/loot-decks/f<FF>-<zone>-<slug>.json` (e.g. `tables/loot-decks/f01-z06-break-room.json`; floor-wide decks use zone `any`). `state.py loot draw <floor> <zone>` loads the deck for that zone plus the floor's `any` deck. **Field names are stable: do not rename; add new fields only with a `schema` bump.**

### 1.1 Field list (one place; Valtay Corp formats from these names)

| Field | Type | Req | Meaning |
|---|---|:-:|---|
| `id` | string | Y | Unique: `f<FF>-<zone>-<NNNN>` (`f01-z06-0003`). Never reused. |
| `floor` | int | Y | 1-18 |
| `zone` | string | Y | `z00`..`z11`, `zS`, or `any` (F1 zones per floors/f01/00-overview.md §4.1) |
| `tier` | enum | Y | `Bronze` `Silver` `Gold` `Platinum` `Legendary` `Celestial` (core §4.1) |
| `box_types` | string[] | Y | `["any"]` or limited: `Boss`, `Quest`, `Fan`, `Benefactor` (core §4.7) |
| `pull_type` | enum | Y | Core §4.2 row: `consumable` `gear` `credits` `tailored` `weird` (`upgrade` is a roll result, not a card type) |
| `kind` | enum | Y | `item` `consumable` `credits` `key` `pet` `stat_bump` `junk` (no mechanics gag) `clue` (lore scrap, seed) |
| `reskin_name` | string | Y | What the crawler sees first |
| `real_5e_name` | string | Y | The actual 5e (or house) item. Never blank. |
| `source_5e` | enum | Y | `SRD 5.2` `DMG 2024` `PHB 2024` `Other 5e (VERIFY)` `HOUSE` (named `source_5e`, not `5e_source`, so scripts can use it as an identifier) |
| `rarity` | enum | Y | `Mundane` `Common` `Uncommon` `Rare` `Very Rare` `Legendary` `Artifact` `n/a` |
| `attunement` | string/null | Y | `null` or `"yes"` or `"yes: spellcaster"` etc. (cap 3, core §4.6) |
| `category` | enum | Y | Inventory-card section: `Weapons` `Armor` `Consumables` `Keys` `Misc`; or `Credits` / `Stats` (not inventory lines; shown in the credits line / sheet) |
| `plain_mechanics` | object | Y | See 1.2. Never dropped on announce. |
| `spoken_line` | string | Y | **<= 25 words**, voice-safe, includes reskin name, real name and the one key effect. Numbers spelled for speech ("one d four"). |
| `snark_line` | string | Y | One System-voice line. Text channel by default; spoken only if the Fish budget allows. |
| `reward` | string | Y | **Read-aloud and tone group** (with `spoken_line`, `snark_line`): the exact reward line the System reads on the achievement banner. May be snark-only (no item named). Also surfaces on the player's sheet card via `state.py achievement add --reward`. |
| `canon_status` | enum | Y | `CANON` `CANON-INSPIRED` `HOUSE`. Describes the **flavor/concept**; mechanics are 5e unless `source_5e` is `HOUSE`. |
| `credit_value` | number | Y | Estimated economy value in credits (1 credit = 1 GP, core §5.10). For `credits` cards: the actual amount (or expected value if rolled, see `grant`). For audit only; never a sale price promise. |
| `draw_weight` | int | Y | 0-100 relative weight inside the filtered pool. **0 = never auto-drawn** (GM hand-pick only). |
| `unique` | bool | Y | `true` = at most one copy per party for the whole campaign (see §2.3) |
| `tailor_tags` | string[] | Y | System-only broad-theme hooks from the hidden Fan Profile, built by the System from survey answers kept in private notes and from play (`["dogs","hats","explosives"]`). No public tags and nothing from the profile is exposed. Empty `[]` if none. Never secret quirk/affinity data. |
| `exclusive_to` | string/null | Y | Crawler name for a running-gag card; else `null` |
| `grant` | object/null | Y | Non-item payloads, see 1.3. `null` for plain items. |
| `ledger` | object | Y | `{ "type": "credits|item|stat_bump|key|pet|clue", "text": "..." }`, the line the bridge logs (1.4) |
| `box_name` | string | Y | The box is named after the deed, canon style, without the tier prefix (e.g. `"Tent-Pole Rescue Box"`; the banner adds the tier). Rule in 2.6. Never a "Desperado Box". |
| `deed` | string | Y | What the crawler did to earn the box (e.g. `"Rescued the tent-pole"`). Logged in the box ledger. |
| `notes` | string | Y | GM-only notes; may be `""`. Never read aloud. For a Story Box card (§2.8) it also holds a `trigger_deed:` line. |
| `story_value` | number | N | **Optional, Story Box cards only** (tier `Legendary`, §2.8). Value in the §3.2 Legendary range, logged on its own ledger line with the deed. **Provenance only:** never a price or a buyback base. Absent on every other card. |
| `bound` | boolean | N | **Optional, with `story_value`.** `true` = cannot be sold or traded. Story Box cards now use `false` (tradeable, lootable, sellable; Caleb, 2026-10-04). Absent on other cards. |
| `sale_value` | number | N | **Optional, Story Box cards only.** The System's fixed buyback in credits at Floor-1 scale, set by power rung (rules/45 §4.6: rung 0 = 100, rung 1 = 250, rung 2 = 500). A System fee, so it multiplies by the floor credit multiplier of the sale floor. Never derived from `story_value`. Absent on other cards. |

Optional fields: a deck that omits `story_value`, `bound` and `sale_value` stays valid (schema label `loot-deck/0.1.1`); a deck that uses them says `loot-deck/0.1.2` (proposed bump; Borent confirms). On a Story Box card `credit_value` is `0`.

### 1.2 `plain_mechanics` (all keys present; `null` when not applicable)

| Key | Meaning |
|---|---|
| `text` | **Required one-liner**, plain English, posted to the text channel and written into state inventory notes. Names the action cost, range, damage, save DC, duration, uses and limits that apply. |
| `action_cost` | `Action`, `Bonus Action`, `Magic action`, `Utilize action`, `Reaction`, `None (passive)`, or `none` |
| `range` | e.g. `"20 ft"` |
| `damage` | e.g. `"1d4 Fire"` |
| `save_dc` | e.g. `"Dex DC 10"` |
| `duration` | e.g. `"1 hour"` |
| `uses` | `{ "max": n, "recharge": "none" | "dawn" | "short rest" | "long rest" | "floor" | "1d6+1 at dawn" }` or `null` |
| `limits` | free text: restrictions, failure/destroy conditions |
| `weight_lb` | number (0 allowed) |

### 1.3 Credits, stat bumps, keys, pets (`grant`)

- **Credits:** `kind:"credits"`, `category:"Credits"`, `grant:{"credits":30,"roll":"3d6x5"}`. If `credits` is a number, that is the amount (it must have been produced by `tools/roll.py` or hand-authored as a *placed* amount, noted in `notes`). If `credits` is `null` and `roll` is set, the GM rolls at draw time (preferred, real dice) and `credit_value` is the expected value. Ranges: Bronze 3d6x5 (15-90), Silver 2d6x25 (50-300), Gold 2d6x250 (500-3,000), Platinum 2d6x2,500, Legendary 2d6x10,000 (core §4.2).
- **Stat bump:** `kind:"stat_bump"`, `category:"Stats"`, `grant:{"ability":"STR","amount":1,"permanent":true,"max_score":20}` (temporary: `"permanent":false,"duration":"1 hour"`). **HOUSE; draft-disabled.** Permanent bumps are above the F1-2 ceiling (core §3.6) and "rewards never change dice, DCs, damage, saves" (GM principles); default `draw_weight` 0 until Caleb rules (§5 Q4). Canon note: stat-boost potions are limited in number of uses (ledger K-159); keep a lifetime cap per crawler if enabled.
- **Key:** `kind:"key"`, `category:"Keys"`. State what it opens in `notes` (GM only) and say in `plain_mechanics.limits` whether it is consumed.
- **Pet:** `kind:"pet"`. Pets are DM-run creatures; mechanics text must give the 5e stat block used (e.g. SRD Cat) and HP. Canon seed: Pet Box / Pet Biscuit (L-B45, I-007) = CANON-INSPIRED.

### 1.4 Ledger lines (what the bridge logs on a draw)

Human line = `ledger.text`. Structured line (proposed; Borent confirms):
```
LOOT | <crawler> | F<floor>/<zone> | <card id> | <tier> | <kind> | value <credit_value> | <ledger.text>
```
Examples of `ledger.text`: `credits +50 Bronze box`; `item +1 Bronze box: Laminated Complaint Card`; `stat_bump STR +1 Gold box`. Credits also post the change-post line from gm-notes/30: `Credits: 25 -> 75 (+50, Bronze box pull)` and append to `sessions/credit-ledger.jsonl` (`delta`, `balance`, `reason`:`"Bronze box pull f01-z06-0005"`, `source`:`"box"`). Item draws log `credit_value` so the Accountant can total value granted per crawler per floor.

### 1.5 Deck file wrapper + full example

```json
{
  "schema": "loot-deck/0.1.1",
  "deck_id": "f01-z06-break-room",
  "version": "0.1.0",
  "floor": 1,
  "zone": "z06",
  "zone_name": "The Break Room",
  "owner": "DCC Lore",
  "updated": "2026-10-04",
  "cards": [
    {
      "id": "f01-z06-0001",
      "floor": 1,
      "zone": "z06",
      "tier": "Bronze",
      "box_types": ["any"],
      "pull_type": "weird",
      "kind": "consumable",
      "reskin_name": "Laminated Complaint Card",
      "real_5e_name": "Laminated Complaint Card (house: single-use oracle)",
      "source_5e": "HOUSE",
      "rarity": "Common",
      "attunement": null,
      "category": "Consumables",
      "plain_mechanics": {
        "text": "Utilize action, once: ask the System one yes/no question about the current floor; it answers truthfully, yes or no. The card is then spent.",
        "action_cost": "Utilize action",
        "range": null,
        "damage": null,
        "save_dc": null,
        "duration": "instant",
        "uses": { "max": 1, "recharge": "none" },
        "limits": "Must be a yes/no question about the floor you are on. A question that is not yes/no is refused and the card is not spent.",
        "weight_lb": 0
      },
      "spoken_line": "Laminated Complaint Card. One use: ask the System one yes-or-no question about this floor. It must answer truthfully.",
      "snark_line": "File it carefully. The System has never lost a complaint. It just files them under 'Funny.'",
      "reward": "Laminated Complaint Card. One use: ask the System one yes-or-no question about this floor. It must answer truthfully.",
      "canon_status": "HOUSE",
      "credit_value": 25,
      "draw_weight": 10,
      "unique": false,
      "tailor_tags": [],
      "exclusive_to": null,
      "grant": null,
      "ledger": { "type": "item", "text": "item +1 Bronze box: Laminated Complaint Card" },
      "box_name": "Filed a Formal Complaint Box",
      "deed": "Filed a formal complaint with the System",
      "notes": "Alpha-test item (2026-10-04). Open: are spine secrets exempt from 'truthfully'? (§5 Q3)"
    }
  ]
}
```

---

## 2. Rules for the GM drawing cards

### 2.1 Procedure (extends core §4.2; semi-random on purpose, L-003)
1. Open boxes only in a saferoom, all at once, lowest tier first (core §4.4; canon L-002).
2. For each pull, roll d100 with `tools/roll.py` and read the §4.2 row to get `pull_type` (consumable / gear / credits / tailored / weird; 99-00 = roll again one tier up, ceiling permitting).
3. **Weighted draw:** filter the deck(s) by `tier` (box tier; consumable pulls may also take one tier down), `pull_type`, `box_types` containing `any` or the box's type, `draw_weight > 0`, floor rarity ceiling (3.6: F1-2 default Common, peak Uncommon), then pick by `draw_weight`. Roll the weights with `roll.py` (`d<sum>`); never "feel" a number.
4. **Hand-pick** is allowed (core §4.2) but log `override: GM pick` in the session log. Don't quietly favor one crawler.
5. Mark the card drawn in state (`loot.drawn[]`). Announce (2.5), write inventory notes (2.5), log the ledger line (1.4).

### 2.2 Tier weighting and ceilings
- Box tier is set by the deed (core §4.1, §4.7, pacing §4.5). **Floors 1-2: Bronze and Silver only** (Boss Box = Silver). The approved GM-triggered Story Box exception (§2.8) is governed by `rules/45-story-boxes-5e.md` v0.2. Gold/Platinum cards in F1-2 decks are `draw_weight: 0` and `box_types:["Benefactor"]` (Benefactor boxes may exceed the ceiling, core §4.7) or hand-picked.
- Suggested within-deck weights (HOUSE, tunable): common consumable 20-30, cheap gear 10-20, uncommon item 5-10, weird/joke 5-10, key 3-5, anything unique 1-5.
- **Celestial:** never auto-drawn. Celestial cards live only in a hand-built per-crawler deck, `draw_weight: 0`. Before issuing, check the crawler has not had one (`state.py box` enforces max 1). The System grumbles about the Syndicate tax (GM principles). Contents follow core §4.1 (Legendary box plus a DM-designed reward).

### 2.3 Duplicates
- `unique: true` = once per **party** for the campaign; remove from the live pool when drawn. Spine-adjacent items, named NPC trophies, and one-off House oddities are unique.
- Non-unique consumables (potions, oils) may repeat; two of the **same non-consumable** may not appear in one box or go to the same crawler in one floor. Reroll once, then the GM picks.
- Duds (`kind:"junk"`) are allowed but never two real boxes in a row for a crawler (core §4.3).

### 2.4 Tailoring (core §3.5, "achievements are guidelines")
- A `tailored` pull matches `tailor_tags` against the crawler's **hidden** Fan Profile (likes, fixations, running gag), built by the System from survey answers kept in private notes and from play. There are no public tags and nothing from the profile is exposed. At least 1 pull in every 3 boxes nods to the profile (core §4.3); the Welcome Box must include one (floor 1 §5.6).
- Gag cards are exclusive: `exclusive_to` = that crawler; other crawlers never draw them. Gags escalate; about once a floor or two a gag turns out to be useful, and then it counts against the power budget.
- Tailor the item, not the power. Build-aware, not build-servile (half of meaningful drops usable by the build). Pettiness allowed, but never a whole floor's worth of value.
- Tailoring never uses GM-secret quirk or affinity data (secrets never appear, gm-notes/30).
- A GM-written one-off card (made at the table) must be saved into the deck file afterward with a full schema entry.

### 2.5 Announcing: reskin freely, never drop the mechanics
- The GM **may** rename (`reskin_name`), rephrase `spoken_line`/`snark_line`, and add flavor.
- The GM **must not** change `real_5e_name`, `plain_mechanics`, `rarity`, `credit_value`, or omit them. Changing mechanics requires a logged override.
- **Announcement = speak and post in the same beat:**
```
[SYSTEM] <Tier> <deed-named> Box. Pull 1 of 2.
Reward: <reward>   (the card's `reward` field; the item read-out itself uses <spoken_line>)
```
then the text channel gets (reskin first; real name and mechanics beneath, matching gm-notes/30):
```
+ <reskin_name>
  <real_5e_name> (<rarity>[, attunement]): <plain_mechanics.text>
  "<snark_line>"
```
- The same `plain_mechanics.text` is written to the crawler's inventory notes in state. Credits post the old -> new line. Keep the banner short (Fish cost): banner, one description line, reward.

### 2.6 Naming and box ledger
- **Name every box after the deed that earned it** (`box_name`, `deed`; core §4.8). Never use a "Desperado Box": canon has no such box. The Desperado Pass Tattoo comes in a first Asshole's Box (CANON L-019, per DCC Lore). Benefactor boxes with no crawler deed may use the type-only name `Benefactor Box`.
- **Box cap:** core has no fixed "2 Bronze boxes per floor" cap. Floor 1 Bronze/Silver box limits are the pacing table in core §4.5 (Floors 1-2: 2-4 Bronze, 0-1 Silver per crawler per floor); core §4.8 covers naming only. Any overage is logged in the box ledger (with `deed`).

---

### 2.7 Running more than one session (alpha and beta)
- Deck files are session-agnostic: no session names, crawler names or draw state inside a deck file. Every session reads the same files in `tables/loot-decks/`.
- Draw history (`loot.drawn[]`), the box ledger, and `unique` checks belong to the session's own state, so a one-of-a-kind item drawn in one session never blocks another session.
- `loot draw` and the loot ledger need to take a session ID or state path (proposed to the Architect). A deck never changes mid-session; if a deck version changes, a running session keeps the version it started on.
- Credit totals for the Accountant's audit are counted per session, per crawler, per floor.

### 2.8 Legendary one-off boxes on Floors 1-2 (Story Boxes) [HOUSE, APPROVED by Caleb 2026-10-04; authoritative system: `rules/45-story-boxes-5e.md` v0.2]

**Basis.** In the books a Legendary box shows up very early: ledger L-001 (six tiers; the Legendary Pet Box Carl opened in the tutorial, cite B1 ch5), I-007 and M-037 (the Enhanced Pet Biscuit from that box; Donut and Prepotente consumed these), A-165 (Legendary Quadruped Box, B1 ch7) and A-167 (Legendary That's the Spirit! Box, B3 ch19). All wiki-sourced and VERIFIED in the ledger, none checked against the novels.

**Core conflict (resolved).** Caleb approved the Story Box exception on 2026-10-04 and core §4.1, §4.5 and §4.7 carry the one-line amendment (core v0.2.8). The authoritative system is `rules/45-story-boxes-5e.md` v0.2, a draft with one open question left (item strength; Caleb answered the other five on 2026-10-04) (decision `decisions/015-story-boxes.md`). Before that, core §4.1 listed Legendary as an ordinary tier but says the floor ceiling (§3.6, peak Uncommon on Floors 1-2) still applies to the five ordinary tiers, with no Legendary boxes on Floor 2. Core §4.5 shows no Legendary box on Floors 1-2. The only exemptions were Benefactor Boxes (§4.7) and Celestial (DM-gated, one per Crawler). A Story Box was not covered by those, so it is now a **narrow, approved exception**: hand-picked, bound, one named one-time deed, one per table per floor, with a logged override to exceed the cap. Where this section and core differ, core wins.

**Rules (all HOUSE, tunable):**
1. **GM-triggered only.** A Story Box is for a rare, one-time, first-of-its-kind deed that the GM judges on the spot. It is never a random draw, never an upgrade roll (the 99-00 row stops at the ceiling), and never part of the pacing table (§4.5).
2. **Cards.** Tier `Legendary`; `draw_weight` 0; hand-pick only; `box_name` from the deed without the tier prefix (e.g. `"Pet Box"`; the banner adds the tier: Legendary Pet Box); the trigger goes in `notes` as `trigger_deed: ...`. No other new fields besides optional `story_value` and `bound` (§1.1).
3. **Cap.** At most **one Story Box per table per Floor**, counted from the session's loot ledger across the whole floor, not per play night (a logged override may exceed it).
4. **Contents.** Hand-designed. The headline is at most 5e **Legendary** rarity (core §4.1, a Legendary box's top). Every item is stated per the `plain_mechanics` rule (action cost, range, duration, uses, limits). Prefer items that open a new option or story thread over raw numbers; GM principles say rewards never change dice, DCs or saves. Other pulls follow core §4.1 (the Legendary box's three pulls) but should be small and Floor-appropriate.
5. **Value and sale.** `credit_value` is `0`. `story_value` (the §3.2 Legendary range, 20,000-250,000) is **provenance only**: logged on its own ledger line with the deed, never a price, never a buyback base, never converted to credits. Story Box items are **not bound** (`bound: false`): once opened they trade, loot and sell. The System's buyback is a fixed `sale_value` per power rung (rules/45 §4.6: rung 0 = 100, rung 1 = 250, rung 2 = 500 at Floor-1 scale); as a System fee it multiplies by the floor credit multiplier of the sale floor. Sales between Crawlers are free-form ordinary credit transfers with `story_value` kept as provenance. The Accountant excludes the award's `story_value` from the 1,500-per-floor inflation flag (§3.2 audit hint) and reports it separately each session, but counts sale proceeds like any credits and **flags, never blocks**.
6. **Tools (request to the Architect; Borent confirms).** `state.py loot draw` treats Legendary cards as hand-pick only (`--pick <card_id>`), checks the one-per-table-per-floor cap in each session's loot ledger with a logged override option, and `loot totals` reports economy value and story value separately.
7. **Celestial stays separate.** A Story Box does not count against the one-per-Crawler Celestial cap and never replaces it.
8. **Announce** as in §2.5: banner plus the item line; the banner names the tier, so the box reads "Legendary Pet Box". Never drop the mechanics line.
9. **Opening.** Saferoom only, like every loot box (core §4.4, unchanged). The deed is recorded and announced at award time; the box is held unopened until the next saferoom.

First example: Enhanced Pet Biscuit (`f01-any-0055`, `rules/42-house-items-f01.md` §6). Two additional box stubs (Legendary Quadruped Box, That's the Spirit! Box) are listed there as to-design.

## 3. Starter stat reference (Floors 1-2)

Tier = suggested card tier. `Value` = suggested `credit_value`: **mundane = 2024 PHB equipment price** (I am confident of the ones listed); magic = **HOUSE estimate** scaled to the tier table (3.2), not the DMG price. Mechanics are paraphrased from the 2024 SRD 5.2 / PHB / DMG from memory; **VERIFY** marks anything I'm not sure of. "Utilize" is the 2024 action for using an object. Weights in lb.

### 3.1 Items

**A. Alpha-test items (2026-10-04)**

| Reskin / item | Tier | Real item (rarity, source) | Plain mechanics | Value | Flag |
|---|---|---|---|---:|---|
| Laminated Complaint Card | Bronze | HOUSE one-use oracle | Utilize, once: System truthfully answers one yes/no question about the current floor. | 25 | HOUSE |
| Eternally Stained Wifebeater | Bronze | Cloak of Many Fashions (house, Common) | Worn as your outer garment; Bonus Action to change its style, color and apparent quality (looks only: no AC, no powers, no check bonus); one outer-garment magic item at a time. | 50 | HOUSE design, final text in rules/42-house-items-f01.md §2 (not in SRD 5.2; DMG shape from memory, not copied) |
| Collapsible Tent-Pole | Bronze | Pole of Collapsing (house, Common) | 10 ft Pole; Magic action while holding it collapses it to 1 ft or extends it to 10 ft (stops at obstacles). No attack/damage use. | 50 | HOUSE design, final text in rules/42-house-items-f01.md §3 (not in SRD 5.2; DMG shape from memory, not copied) |
| Kevin the Sentient Rubber Duck | Bronze | HOUSE joke item | No mechanics. Gives terrible advice only. 0 lb. | 0 | HOUSE |
| Gas-Station Bathroom Key on a Hubcap | Bronze | HOUSE "Mystery Key" analog (Common) | Utilize: opens one specific lock on the current floor chosen by the GM at draw time (GM-only); spent on use; becomes a plain key if you leave the floor unused. 1 lb. | 25 | HOUSE, final text in rules/42-house-items-f01.md §4; the 5e Mystery Key is a different (chance-based) item |
| Sports Drink, Blue Flavor | Bronze | Potion of Healing (Common) | Drink (Bonus Action): regain 2d4+2 HP. | 50 | |
| Pebbles Snow Globe | Bronze (hand-pick) | Driftglobe (Uncommon) | Within 60 ft, command word casts Light (1 hr) or Daylight (once per dawn); another word floats it up to 5 ft and it follows you. | 100 | Hand-picked into a Bronze box (`draw_weight` 0). Uncommon is within the F1-2 peak (core §3.6); Bronze boxes normally headline Common (core §4.1), so this is a logged GM hand-pick (core §4.2) |

**B. Consumables**

| Item | Tier | Rarity | Plain mechanics | Value | Flag |
|---|---|---|---|---:|---|
| Potion of Healing | Bronze | Common | Bonus Action to drink (or give): regain 2d4+2 HP. | 50 | |
| Potion of Greater Healing | Silver | Uncommon | Bonus Action: regain 4d4+4 HP. | 150 | SRD 5.2 checked (dice, Uncommon; SRD name is Potion of Healing (greater)); price VERIFY: not in SRD 5.2, HOUSE estimate |
| Potion of Superior Healing | Gold | Rare | Bonus Action: regain 8d4+8 HP. | 500 | SRD 5.2 checked (dice, Rare; SRD name is Potion of Healing (superior)); price VERIFY: not in SRD 5.2, HOUSE estimate |
| Potion of Climbing | Bronze | Common | Bonus Action; 1 hour: gain a Climb Speed equal to your Speed; Advantage on Athletics checks to climb. | 60 | |
| Potion of Water Breathing | Silver | Uncommon | Drink: breathe underwater for 24 hours. | 150 | |
| Potion of Resistance | Silver | Uncommon | Drink (Bonus Action): Resistance to one damage type for 1 hour; the GM picks the type or rolls d10 (acid, cold, fire, force, lightning, necrotic, poison, psychic, radiant, thunder). | 200 | SRD 5.2 checked (type is GM choice or d10, not potion color) |
| Potion of Giant Strength (Hill) | Silver | Uncommon | Drink: Strength becomes 21 for 1 hour (no effect if already 21+). | 200 | |
| Potion of Animal Friendship | Silver | Uncommon | Drink (Bonus Action): cast Animal Friendship once at level 3 (Wis save DC 13): up to 3 Beasts you can see within 30 ft are Charmed for 24 hours; it ends if you or an ally damages the target. | 150 | SRD 5.2 checked (old row said at will for 1 hour) |
| Potion of Fire Breath | Silver | Uncommon | Drink (Bonus Action); within 1 hour, exhale fire (Bonus Action) up to 3 times at one creature within 30 ft: Dex DC 13, 4d6 Fire, half on a save. | 200 | HOUSE design, final text in rules/42-house-items-f01.md §5 (not in SRD 5.2; numbers follow secondary listings of the DMG potion, not checked against the book) |
| Spell Scroll (cantrip or 1st level) | Bronze | Common | Read it (the spell's normal casting time) to cast the spell once, only if it is on your class spell list; no Material components; scroll save DC 13, attack bonus +5; the scroll crumbles after. | 75 | SRD 5.2 checked (SRD prices: cantrip 30 GP, level 1 50 GP; 75 is a HOUSE estimate) |
| Alchemist's Fire | Bronze | Mundane | Attack action (replace one attack): throw at a target you can see within 20 ft; Dex save (DC 8 + thrower's Dex modifier + Proficiency Bonus) or it takes 1d4 Fire at once and starts burning (1d4 Fire at the start of each of its turns until put out: an action to drop Prone and roll, or doused). 1 lb. | 50 | SRD 5.2 checked (Dex save, not an attack roll; no DC 10 Utilize to extinguish) |
| Acid (vial) | Bronze | Mundane | Utilize: throw up to 20 ft, ranged attack; hit = 2d6 Acid. 1 lb. | 25 | |
| Holy Water (flask) | Bronze | Mundane | Utilize: throw up to 20 ft, ranged attack; hit on a Fiend or Undead = 2d8 Radiant. 1 lb. | 25 | |
| Antitoxin | Bronze | Mundane | Drink (Bonus Action): Advantage on saves to avoid or end Poisoned for 1 hour. | 50 | SRD 5.2 checked |
| Oil (flask) | Bronze | Mundane | Attack action (replace one attack): throw at a target within 20 ft; Dex save (DC 8 + Dex modifier + Proficiency Bonus) or it is covered for 1 minute, and Fire damage in that time adds 5 Fire. Or Utilize: pour on a 5-ft square within 5 ft; if lit it deals 5 Fire (once per turn) to creatures entering or ending their turn there until the end of the turn 2 rounds later. Also lamp or lantern fuel (6 hours per flask). 1 lb. | 0.1 | SRD 5.2 checked (1 SP) |
| Ball Bearings (bag of 1,000) | Bronze | Mundane | Utilize: spill over a 10-ft square; a creature entering the area for the first time on a turn must succeed on a DC 10 Dex save or fall Prone; 10 minutes to pick up again. 2 lb. | 1 | SRD 5.2 checked (area is within 10 ft of you) |
| Caltrops (bag of 20) | Bronze | Mundane | Utilize: cover a 5-ft square; entering creature: DC 15 Dex save or stops moving, takes 1 piercing, Speed -10 until it regains 1 HP. 2 lb. | 1 | |
| Healer's Kit (10 uses) | Bronze | Mundane | Utilize, 1 use: stabilize a creature at 0 HP without a Medicine check. 3 lb. | 5 | |
| Torch | Bronze | Mundane | Burns 1 hour: bright light 20 ft, dim 20 ft more. Melee hit with it = 1 Fire. 1 lb. | 0.01 | |

**C. Tools and gear**

| Item | Tier | Rarity | Plain mechanics | Value | Flag |
|---|---|---|---|---:|---|
| Rope, hempen (50 ft) | Bronze | Mundane | Utilize: tie a knot (DC 10 Dex (Sleight of Hand)); burst with a DC 20 Strength (Athletics) check; binds an unwilling creature only if it is Grappled, Incapacitated or Restrained (escape DC 15 Dex (Acrobatics)). 5 lb. | 1 | SRD 5.2 checked (weight 5 lb; burst DC is 20 not 17; SRD gives no HP or length) |
| Crowbar | Bronze | Mundane | Advantage on Strength checks where leverage helps. 5 lb. | 2 | SRD 5.2 checked |
| Lock | Bronze | Mundane | Comes with a key; picking it needs Thieves' Tools, DC 15 Dex. 1 lb. | 10 | |
| Net | Bronze | Mundane | Attack action (replace one attack): throw at a creature you can see within 15 ft; Dex save (DC 8 + Dex modifier + Proficiency Bonus) or it is Restrained until it escapes (Huge or larger succeed automatically). Escape: the target or a creature within 5 ft uses an action for a DC 10 Strength (Athletics) check, or the net is destroyed (AC 10, 5 HP). 3 lb. | 1 | SRD 5.2 checked (Dex save, not an attack roll; size limit is Huge) |
| Hunting Trap | Bronze | Mundane | Set with Utilize; creature stepping on the plate: DC 13 Dex save or 1d4 piercing and Speed 0 until the start of its next turn, then movement limited by the 3-ft chain until freed (action, DC 13 Strength (Athletics); each failed check deals 1 piercing). 25 lb. | 5 | SRD 5.2 checked (free DC 13 confirmed) |
| Lantern, hooded | Bronze | Mundane | Bright 30 ft, dim 30 ft more; 6 hours per oil flask; Bonus Action to lower the hood (dim light 5 ft only) or raise it. 2 lb. | 5 | SRD 5.2 checked |
| Climber's Kit | Bronze | Mundane | Utilize to anchor yourself: you can't fall more than 25 ft from the anchor point and can't move more than 25 ft from it without undoing the anchor as a Bonus Action. 12 lb. | 25 | SRD 5.2 checked |
| Bag of Holding | Silver | Uncommon | Holds up to 500 lb / 64 cu ft; bag weighs 5 lb; Utilize to retrieve an item. | 400 | SRD 5.2 checked (weight was 15 lb here). Redundant with System Inventory (core §5.9); give as a physical stash/gag |
| Heward's Handy Haversack | Gold | Rare | Backpack with three extradimensional pouches: central up to 500 lb / 64 cu ft, each side up to 200 lb / 25 cu ft; always weighs 5 lb; retrieve an item with a Utilize or Bonus Action (it is always on top). | 1,500 | SRD 5.2 checked (Rare; SRD name is Handy Haversack, no "Heward's") |
| Portable Hole | Gold | Rare | Magic action to unfold into a hole 6 ft across, 10 ft deep; fold away with a Magic action. | 1,500 | SRD 5.2 checked (Rare) |
| Rope of Climbing | Silver | Uncommon | 60 ft, holds up to 3,000 lb; Magic action while holding one end: the other end moves toward a spot you pick (10 ft when commanded, 10 ft at the start of each of your turns), or fastens, unfastens, knots or coils; knotted it is 50 ft long and gives Advantage on climbing checks; AC 20, 20 HP, regains 1 HP per 5 minutes. | 300 | SRD 5.2 checked |
| Immovable Rod | Silver | Uncommon | Action: press the button to fix it in place; DC 30 Strength to move; holds ~8,000 lb. 2 lb. | 300 | |

**D. Wearables and wands**

| Item | Tier | Rarity | Plain mechanics | Value | Flag |
|---|---|---|---|---:|---|
| Boots of Elvenkind | Silver | Uncommon | Steps make no sound on any surface; Advantage on Dexterity (Stealth) checks. No attunement. | 250 | SRD 5.2 checked (Advantage applies to all Stealth checks, not just moving silently) |
| Goggles of Night | Silver | Uncommon | Darkvision 60 ft (adds 60 ft if you have it). | 250 | |
| Gloves of Thievery | Silver | Uncommon | +5 to Dexterity (Sleight of Hand) checks; imperceptible while worn. No attunement. | 250 | SRD 5.2 checked (no lock-picking bonus in SRD 5.2) |
| Cloak of Protection | Silver | Uncommon | Attunement: +1 AC and +1 to saving throws. | 400 | |
| Bracers of Archery | Silver | Uncommon | Attunement: proficiency with longbow and shortbow; +2 damage with them. | 400 | |
| Pearl of Power | Silver | Uncommon | Attunement (spellcaster): Action, once per dawn: regain one expended spell slot up to 3rd level. | 400 | |
| +1 Weapon | Silver | Uncommon | +1 to attack and damage rolls. | 400 | |
| Shield, +1 | Silver | Uncommon | +1 AC while holding it, on top of the shield's own bonus. | 400 | SRD 5.2 checked (+1 is Uncommon) |
| Ring of Protection | Gold | Rare | Attunement: +1 AC and +1 to saving throws. | 1,500 | |
| Wand of Magic Missiles | Silver | Uncommon | 7 charges; Magic action, spend 1-3 charges: 1 = Magic Missile (3 darts, 1d4+1 force each), +1 dart per extra charge; regains 1d6+1 at dawn; if you spend the last charge, d20: on a 1 it crumbles. | 300 | |

---

### 3.2 Suggested `credit_value` ranges per tier (HOUSE, tunable)

| Tier | Item value range | Credits-pull range (core §4.2) | Note |
|---|---|---|---|
| Bronze | 0-100 | 15-90 (3d6x5) | Junk and 0-value gags allowed |
| Silver | 100-500 | 50-300 (2d6x25) | Uncommon headline items |
| Gold | 500-5,000 | 500-3,000 (2d6x250) | Rare headline items |
| Platinum | 5,000-50,000 | 5,000-30,000 | Not on F1-2 |
| Legendary | 20,000-250,000 | 20,000-120,000 | Not on F1-2 as an ordinary box. A GM-triggered Story Box (§2.8) logs this range as `story_value` (provenance only), not `credit_value` |
| Celestial | DM's call | DM's call | One per crawler |

**Floor multiplier (Lore, with Caleb's delegation, 2026-10-04).** Box credit pulls use the ranges above (and core §4.2) as written and do **not** get the floor credit multiplier on top. Achievement rewards and System fees (buyback, repairs, crafting prices) keep it (core §3.9).

**Audit hint (HOUSE):** per crawler per floor on F1-2, total `credit_value` granted by boxes should land around 300-1,000 (2-4 Bronze plus 0-1 Silver, core §4.5). Treat anything above about 1,500 as inflation to flag, and re-tune weights before nerfing items (core §3.7). `story_value` from Story Boxes (§2.8) is **excluded** from this flag and reported separately. Sale proceeds from a Story Box item are ordinary credits: they count toward the flag, and the Accountant flags them but never blocks the sale (rules/45 §6.5).

---

## 4. Five sample cards

All deck-file entries (fields from §1; showing only the `cards` entries). Sample 1 is the Laminated Complaint Card in §1.5. Read-aloud renderings sit under each. Mechanics are per §3; sample 3 and 4 numbers match the §3 rows.

**Sample 2: Bronze, Alchemist's Fire reskin (Vending Gore Arcade)**
```json
{ "id": "f01-z03-0004", "floor": 1, "zone": "z03", "tier": "Bronze", "box_types": ["any"], "pull_type": "consumable",
  "kind": "consumable", "reskin_name": "Flaming Hot Nacho Cheese Pouch", "real_5e_name": "Alchemist's Fire",
  "source_5e": "PHB 2024", "rarity": "Mundane", "attunement": null, "category": "Consumables",
  "plain_mechanics": { "text": "Attack action (replace one attack): throw at a target you can see within 20 ft; Dex save (DC 8 + thrower's Dex modifier + Proficiency Bonus) or it takes 1d4 Fire and starts burning (1d4 Fire at the start of each of its turns until put out by dropping Prone and rolling, or doused). One use, 1 lb.",
    "action_cost": "Action", "range": "20 ft", "damage": "1d4 Fire per turn", "save_dc": "Dex DC 8 + Dex mod + Proficiency Bonus",
    "duration": "until extinguished", "uses": { "max": 1, "recharge": "none" }, "limits": "Consumed on throw.", "weight_lb": 1 },
  "spoken_line": "Flaming Hot Nacho Cheese Pouch, Alchemist's Fire. Thrown twenty feet; a failed save means one d four fire damage each turn until doused.",
  "snark_line": "Do not lick the nozzle. We already tried. The audience is still recovering.",
  "reward": "Flaming Hot Nacho Cheese Pouch, Alchemist's Fire. Thrown twenty feet; a failed save means one d four fire damage each turn until doused.",
  "canon_status": "HOUSE", "credit_value": 50, "draw_weight": 15, "unique": false, "tailor_tags": ["explosives", "fire"],
  "exclusive_to": null, "grant": null,
  "ledger": { "type": "item", "text": "item +1 Bronze box: Flaming Hot Nacho Cheese Pouch (Alchemist's Fire)" },
  "box_name": "Stabbed the Vending Machine Box", "deed": "Fought a vending machine",
  "notes": "Reskin of mundane gear; price from 2024 PHB. SRD 5.2 checked (Dex save, burning timing)." }
```
```
[SYSTEM] Bronze Stabbed the Vending Machine Box. Pull 1 of 2.
Reward: Flaming Hot Nacho Cheese Pouch, Alchemist's Fire. Thrown twenty feet; a failed save means one d four fire damage each turn until doused.
```

**Sample 3: Silver, Wand of Magic Missiles (Floor 2, floor-wide deck)**
```json
{ "id": "f02-any-0012", "floor": 2, "zone": "any", "tier": "Silver", "box_types": ["any"], "pull_type": "gear",
  "kind": "item", "reskin_name": "Pre-Owned Laser Pointer (Cat Not Included)", "real_5e_name": "Wand of Magic Missiles",
  "source_5e": "SRD 5.2", "rarity": "Uncommon", "attunement": null, "category": "Weapons",
  "plain_mechanics": { "text": "Magic action: spend 1-3 of 7 charges to cast Magic Missile (1 charge = 3 darts, 1d4+1 Force each, auto-hit, 120 ft; each extra charge adds 1 dart). Regains 1d6+1 charges at dawn. If you spend the last charge, roll d20: on a 1 the wand crumbles to ash. 1 lb.",
    "action_cost": "Magic action", "range": "120 ft", "damage": "1d4+1 Force per dart", "save_dc": null, "duration": "instant",
    "uses": { "max": 7, "recharge": "1d6+1 at dawn" }, "limits": "Destroyed on a 1 (d20) after the last charge is spent.", "weight_lb": 1 },
  "spoken_line": "Pre-Owned Laser Pointer, Wand of Magic Missiles. Seven charges; one charge fires three darts, one d four plus one force each.",
  "snark_line": "Previous owner: a man named Gary. Gary is not available for comment. Gary is a stain.",
  "reward": "Pre-Owned Laser Pointer, Wand of Magic Missiles. Seven charges; one charge fires three darts, one d four plus one force each.",
  "canon_status": "HOUSE", "credit_value": 300, "draw_weight": 6, "unique": false, "tailor_tags": ["magic missile", "cats"],
  "exclusive_to": null, "grant": null,
  "ledger": { "type": "item", "text": "item +1 Silver box: Pre-Owned Laser Pointer (Wand of Magic Missiles)" },
  "box_name": "Brave, Loud, and Mostly Lucky Box", "deed": "Charged first, won anyway",
  "notes": "SRD 5.2 checked: each extra charge raises the spell level by 1, and Magic Missile gains one dart per level above 1. The crawler may not know Gary." }
```
```
[SYSTEM] Silver Brave, Loud, and Mostly Lucky Box. Pull 2 of 2.
Reward: Pre-Owned Laser Pointer, Wand of Magic Missiles. Seven charges; one charge fires three darts, one d four plus one force each.
```

**Sample 4: Gold, Ring of Protection (Benefactor-only on Floor 2; draw_weight 0)**
```json
{ "id": "f02-any-0031", "floor": 2, "zone": "any", "tier": "Gold", "box_types": ["Benefactor"], "pull_type": "gear",
  "kind": "item", "reskin_name": "Class Ring, Graduating Class of Nobody", "real_5e_name": "Ring of Protection",
  "source_5e": "SRD 5.2", "rarity": "Rare", "attunement": "yes", "category": "Misc",
  "plain_mechanics": { "text": "Requires attunement. While worn: +1 bonus to Armor Class and +1 bonus to all saving throws. No charges, no action to use.",
    "action_cost": "None (passive)", "range": null, "damage": null, "save_dc": null, "duration": "while worn and attuned",
    "uses": null, "limits": "Counts toward the 3-item attunement limit.", "weight_lb": 0 },
  "spoken_line": "Class Ring, Graduating Class of Nobody: Ring of Protection. Attune it for plus one Armor Class and plus one on all saving throws.",
  "snark_line": "Stamped inside: 'Go Fighting Nothing.' The school mascot was a blank space. We respect the commitment.",
  "reward": "Class Ring, Graduating Class of Nobody: Ring of Protection. Attune it for plus one Armor Class and plus one on all saving throws.",
  "canon_status": "HOUSE", "credit_value": 1500, "draw_weight": 0, "unique": true, "tailor_tags": [],
  "exclusive_to": null, "grant": null,
  "ledger": { "type": "item", "text": "item +1 Gold Benefactor box: Class Ring, Graduating Class of Nobody (Ring of Protection)" },
  "box_name": "Benefactor Box", "deed": "Sponsor gift (no crawler deed)",
  "notes": "Rare is above the F1-2 ceiling (peak Uncommon), so Benefactor-only or hand-picked (core §3.6, §4.7). Unique: one per party." }
```
```
[SYSTEM] Gold Benefactor Box. A sponsor is feeling generous. Do not ask why.
Reward: Class Ring, Graduating Class of Nobody: Ring of Protection. Attune it for plus one Armor Class and plus one on all saving throws.
```

**Sample 5: Bronze credits card (Break Room)**
```json
{ "id": "f01-z06-0005", "floor": 1, "zone": "z06", "tier": "Bronze", "box_types": ["any"], "pull_type": "credits",
  "kind": "credits", "reskin_name": "Thirty Credits, Slightly Damp", "real_5e_name": "30 credits (30 gp)",
  "source_5e": "HOUSE", "rarity": "n/a", "attunement": null, "category": "Credits",
  "plain_mechanics": { "text": "Adds 30 credits to your balance. No weight. (Bronze: 3d6x5.)",
    "action_cost": "none", "range": null, "damage": null, "save_dc": null, "duration": "instant",
    "uses": null, "limits": "Added when the box is opened.", "weight_lb": 0 },
  "spoken_line": "Thirty credits, added to your balance. They are damp. Do not ask what from.",
  "snark_line": "Please spend it before it ferments.",
  "reward": "Thirty credits, added to your balance. They are damp. Do not ask what from.",
  "canon_status": "CANON-INSPIRED", "credit_value": 30, "draw_weight": 25, "unique": false, "tailor_tags": [],
  "exclusive_to": null, "grant": { "credits": 30, "roll": "3d6x5" },
  "ledger": { "type": "credits", "text": "credits +30 Bronze box" },
  "box_name": "Participation Trophy Box", "deed": "Showed up, technically",
  "notes": "Pre-rolled with tools/roll.py: [ROLL] 3d6 -> [2, 3, 1] = 6, x5 = 30 (--no-log, spec sample only). Prefer credits:null and roll at draw. Credit boxes are canon-shaped (tiered boxes, L-001); the amount math is HOUSE core §4.2." }
```
```
[SYSTEM] Bronze Participation Trophy Box. Pull 1 of 1.
Reward: Thirty credits, added to your balance. They are damp. Do not ask what from.
Credits: 25 -> 55 (+30, Bronze box pull)
```

---

## 5. Open questions for Caleb

1. Gold/Platinum cards in Floor 1-2 decks: keep as Benefactor-only or hand-pick-only (as drafted), or drop them until Floor 3?
2. Alpha Driftglobe (Common) vs Uncommon in the 2024 books: keep Bronze Driftglobe as a house ruling, or move it to Silver?
3. Laminated Complaint Card: may the System lie or refuse on spine secrets (Odd Coin, Black Box, Benefactor), or always answer truthfully, no exceptions?
4. Stat bump cards: off until you rule? If on, permanent only from Gold up, with a lifetime cap, or never on F1-2? (GM principles say rewards never change dice, DCs or saves.)
5. Bag of Holding is redundant with System Inventory: ban it from decks, or give it a new job (a droppable, stealable physical stash)?
6. Is `credit_value` allowed to feed XP-like pacing checks, or is it audit-only?
7. Should item draws also log to a new `sessions/loot-ledger.jsonl` (Borent), or only to the existing credit ledger and state notes?
8. Fish budget: is 25 words per `spoken_line` right, and should `snark_line` always go to text only?
9. ~~Story Boxes (§2.8)~~ RESOLVED 2026-10-04: Caleb approved the narrow exception; cap is one per table per floor with a logged override (core §4.1, decision 015).
10. A pet turned Crawler by the Enhanced Pet Biscuit: does it use one of the four player slots (decision 013)? Proposed default: no, but it counts for encounter budgets (details in rules/42-house-items-f01.md §7).

---

## Verification log (2026-10-04, v0.1.2; v0.1.3 note below)

Source: SRD 5.2.1 (Wizards of the Coast, CC-BY-4.0), official PDF; paraphrased, nothing copied. Of 27 VERIFY tags on items and sample-card notes, 21 resolved and 6 remain.

**Confirmed, no change (rarity/numbers match):** Crowbar; Hooded Lantern radius (bright 30 ft, dim 30 ft more, 6 hours per Oil flask); +1 Shield rarity (Uncommon); Wand of Magic Missiles (extra charges raise spell level, one more dart each); Antitoxin; Hunting Trap free DC 13; Ball Bearings; Climber's Kit.

**Changed (old -> new):**
- Potion of Animal Friendship: "cast Animal Friendship at will for 1 hour" -> once, level 3 version, save DC 13, up to 3 Beasts, 24 hours.
- Potion of Resistance: type "set by the potion's color" -> GM picks or rolls d10 (10 types listed); 1 hour confirmed.
- Spell Scroll: "Magic action" -> the spell's normal casting time; spell must be on your list; scroll save DC 13, attack +5 for cantrip and level 1.
- Alchemist's Fire: ranged attack hit + DC 10 Dex check to put out -> Dex save (DC 8 + Dex + Proficiency Bonus) for 1d4 Fire and burning; put out by dropping Prone and rolling. Sample 2 card text, action_cost, save_dc, spoken_line, reward, banner and notes changed to match.
- Oil: Utilize douse -> thrown with Attack action (Dex save, +5 Fire) or poured on a 5-ft square.
- Rope: burst DC 17 -> DC 20; "2 HP" removed (SRD gives none); weight 5 lb confirmed.
- Net: attack hit -> Dex save, 15 ft range, Huge or larger auto-succeed, net 5 HP.
- Boots of Elvenkind: Advantage on Stealth only when moving silently -> Advantage on all Dexterity (Stealth) checks.
- Gloves of Thievery: "+5 to Sleight of Hand and lock-picking" -> Sleight of Hand only; no attunement.
- Portable Hole: "Action" -> Magic action (open and fold); Rare confirmed.
- Heward's Handy Haversack: vague text -> pouch sizes, 5 lb, Utilize or Bonus Action to retrieve; SRD name is Handy Haversack.
- Rope of Climbing: vague text -> full limits (3,000 lb, 10 ft per turn, 50 ft when knotted, AC 20, HP 20).
- Bag of Holding (untagged): weight 15 lb -> 5 lb.

**Still unverified, now HOUSE rulings in rules/42-house-items-f01.md (v0.2.1: the four VERIFY tags in §3.1 were replaced by pointers there; they remain unchecked against the printed DMG):** Cloak of Many Fashions; Pole of Collapsing; Mystery Key (5e item; a secondary 2024 listing says Common, 5% chance to unlock, key vanishes after use); Potion of Fire Breath (secondary listings: Bonus Action, 30 ft, Dex DC 13, 4d6 Fire, 3 uses in 1 hour, Uncommon); Potion of Greater Healing and Superior Healing prices (SRD prices only Potion of Healing at 50 GP; 150 and 500 stay HOUSE estimates; the dice and rarities are confirmed: 4d4+4 Uncommon, 8d4+8 Rare).

**Floor 1 deck check:** see rules/loot-deck-srd-check-f01.md. 66 non-HOUSE cards checked: 56 OK, 6 DIFF (Arrows missing the recovery rule; Cure Wounds and Healing Word scrolls with a non-SRD Construct/Undead limit; Signal Whistle value 0.5 should be 0.05, two cards; Oil card f01-z03-0006 missing the save DC), 4 NOT IN SRD (Driftglobe, Cloak of Many Fashions, Pole of Collapsing, Potion of Fire Breath). Deck files not edited.

**Affects other files:** the f01 deck cards for Alchemist's Fire, Net, Oil, Rope and Bag of Holding already use the corrected numbers; the Alchemist's Fire snark/reward lines in any other deck still saying "hit" should say "failed save". `source_5e` label "PHB 2024" on SRD gear is fine; Potion names in the SRD use "Potion of Healing (greater)/(superior)".


**v0.1.4 (2026-10-04, audit):** Story Box exception marked approved in §2.8, Open question 9 resolved, header status and core pointer brought to v0.2.6; `tailor_tags` and the tailored-pull rule now say the Fan Profile is hidden (S12 dropped). No schema change.

**v0.1.6 (2026-10-04):** `uses.recharge` gains `"floor"` (once per floor, used by 0065 Group Photo).

**v0.1.5 (2026-10-04, Story Box answers):** Story Box items are not bound (`bound: false`) and sell for a fixed `sale_value` per power rung; `story_value` is provenance only; optional `sale_value` field added to the schema 0.1.2 table; saferoom-only opening (rule 9); the cap is per floor, not per play night; box credit pulls get no floor multiplier (§3.2); dependency pointers refreshed to core v0.2.8, rules/42 v0.2.2 and rules/45 v0.2.
