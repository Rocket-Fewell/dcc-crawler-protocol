# House Items, Floor 1 (Final Rules Text and Card JSON)
Owner: Syndicate | Status: draft | Version: 0.2.3 | Updated: 2026-10-04
Summary: Final plain-words rules text, schema-exact card JSON, and a field-by-field diff list for Lore's draft cards, for four items not in SRD 5.2 (Cloak of Many Fashions, Pole of Collapsing, Mystery Key, Potion of Fire Breath), plus six Story Box items (Enhanced Pet Biscuit and cards 0056 to 0060 from Lore's f01-any-story-boxes.json) with final rules text, tradeable/sale and deed rules, power notes, GM record lists and open questions.
Depends on: rules/40-loot-deck-spec-5e.md v0.1.5 (§1.1 schema, §2 draw rules incl. §2.8, §3.2 credit ranges, verification log), rules/10-core-rules-5e.md v0.2.8 (§2.4 group size, §3.6 ceilings, §4.1, §4.4, §4.7), rules/loot-deck-srd-check-f01.md, tables/loot-decks/f01-*.json (read only, owned by DCC Lore). Consumers: DCC Lore (applies the diffs to the decks), AI GM, the Accountant (values), Valtay Corp.

> **Status:** DRAFT v0.2.3. Nothing is LOCKED. No deck file was edited; Lore decides what to apply. Caleb approved Story Boxes on 2026-10-04. `rules/45-story-boxes-5e.md` v0.2 is the authoritative system; it remains a draft with one open question left (item strength; Caleb answered the other five on 2026-10-04).
> **Project:** *Crawler Protocol: Season Zero*, private fan RPG inspired by *Dungeon Crawler Carl*.
> **Honesty note:** none of the first four items is in SRD 5.2.1 (checked, see the SRD check file). The DMG versions are described here **from memory and from secondary listings** (Lore's draft cards cite an online mirror of the 2024 DMG; I did not check it against the book). These are **HOUSE rulings written in my own words** in the general shape of the DMG items. No DMG text is copied. If the table owns the 2024 DMG, compare before play; where they differ, this file wins for the Crawl until Caleb says otherwise.
> **Tags:** `HOUSE` = our design. `CANON-INSPIRED` = concept from the books (ledger-tied), mechanics ours. Text uses "Crawlers" throughout.

## Contents
1. What changes in Lore's draft cards (diff list)
2. Cloak of Many Fashions
3. Pole of Collapsing ("Collapsible Tent-Pole")
4. Mystery Key ("Gas-Station Bathroom Key")
5. Potion of Fire Breath
6. Enhanced Pet Biscuit and the other Story Box items (cards 0055 to 0060)
7. Open questions for Caleb
8. Changelog

---

## 1. What changes in Lore's draft cards

Kept as Lore has them (no rule is broken): ids, zones, `draw_weight`, `credit_value` (Cloak 50, Pole 50, Key 25, Fire Breath 200), tiers, `box_name`, `deed`, snark lines, `tailor_tags`. The table lists only fields that should change. Cards covered: `f01-any-0028`, `f01-z09-0015` (Cloak); `f01-any-0029` (Pole); `f01-any-0035`, `f01-z06-0004` (Key); `f01-any-0041` (Fire Breath).

| Card | Field | Now | Change to | Why |
|---|---|---|---|---|
| f01-any-0028 | source_5e | `DMG 2024` | `HOUSE` | Not in SRD 5.2; house design (z09-0015 already says HOUSE) |
| f01-any-0028 | real_5e_name | `Cloak of Many Fashions` | `Cloak of Many Fashions (house)` | Same |
| f01-any-0028, f01-z09-0015 | category | `Armor` | `Misc` | It gives no AC; §1.1 `Armor` is the armor inventory section |
| f01-any-0028, f01-z09-0015 | plain_mechanics.text, limits, duration | draft text, `Cosmetic only. No AC.` / `HOUSE DRAFT mechanics.`, `while worn` | final text in §2 card; duration `until you change it` | Adds the look-only rule, the one-outer-garment limit, "no check bonus" |
| f01-any-0028 | notes | "Mechanics checked vs DMG 2024 text (aidedd mirror)" | "HOUSE design, rules/42 §2; DMG shape from memory" | Syndicate cannot confirm the mirror; avoid implying a book check |
| f01-z09-0015 | notes | points at the rules/40 §3.1 row | point at rules/42 §2 | The §3.1 row now points here |
| f01-any-0029 | source_5e / real_5e_name | `DMG 2024` / `Pole of Collapsing` | `HOUSE` / `Pole of Collapsing (house)` | Not in SRD 5.2 |
| f01-any-0029 | plain_mechanics.text, limits, duration | draft text, `Spec/audit say 'Action'; 2024 DMG text is Magic action.`, `permanent` | final text in §3 card; limits without the spec/audit sentence; duration `until you change it` | Action cost is **Magic action** everywhere; adds "not a weapon" and blocking rules |
| f01-any-0029 | notes | mirror-check claim | "HOUSE design, rules/42 §3" | As above |
| f01-any-0035, f01-z06-0004 | rarity | `n/a` | `Common` | Bronze box headline is Common (core §4.1); an item that is a real item needs a rarity for the §3.6 ceiling check |
| f01-any-0035, f01-z06-0004 | real_5e_name | `Mystery Key (house)` | `Mystery Key (house, single lock)` | The 5e Mystery Key is chance-based; say ours is different |
| f01-any-0035, f01-z06-0004 | plain_mechanics.text, limits, duration, spoken_line, reward | two slightly different texts | one text (§4 card), duration `until used or you leave the floor`, spoken line adds "on this floor" | The two Key cards must read the same; adds the floor limit and what the key cannot open |
| f01-any-0035 | notes | cites "Audit R4" | "HOUSE design, rules/42 §4" plus the GM-only lock advice | Keeps the GM note useful |
| f01-any-0041 | source_5e / real_5e_name | `DMG 2024` / `Potion of Fire Breath` | `HOUSE` / `Potion of Fire Breath (house)` | Not in SRD 5.2 |
| f01-any-0041 | plain_mechanics.text, limits | "at a target within 30 ft" | "at one creature you can see within 30 ft"; limits: one per Bonus Action, single target, fire ignition is GM call | Removes ambiguity |
| f01-any-0041 | notes | "Spec VERIFY resolved with aidedd 5.5 text" | "Numbers follow Lore's draft / secondary listings, not checked against the book" | Accuracy |

No change needed to: rarity (Common, Common, Uncommon), attunement (`null` on all), `action_cost` (Cloak Bonus Action, Pole Magic action, Key Utilize action, Fire Breath Bonus Action), `uses` on Key and Fire Breath.

**Ceiling check (core §3.6 / §4.1):** Floors 1-2 default Common, peak Uncommon. Cloak, Pole and Key are Common (Bronze); Fire Breath is Uncommon (Silver headline). All inside the ceiling, so **no redesign to a smaller version was needed**. None needs attunement.

---

## 2. Cloak of Many Fashions (HOUSE, Common, no attunement)

**Rules text.** You wear it as your outer garment. As a Bonus Action you change its style, color and apparent quality: rags to fine tailoring, hoodie to cape to hi-vis vest, any garment you have seen. It copies **looks only**: no AC, no powers, no bonus to Deception, Disguise or any check, and it cannot copy another cloak's magic. It stays about its own size and weight (1 lb), and touching it reveals nothing odd. You can wear only one outer-garment magic item at a time (house, so this does not stack with a Cloak of Protection reskinned as a vest). No uses, no charges, no limit on changes.

**Why it is balanced:** zero combat value; it is a Common cosmetic, so Bronze with credit_value 50 sits mid-range in the Bronze 0-100 band (spec §3.2).
**Zone and weight (Lore's, kept):** `f01-z09-0015` in the Green Room (costume zone), weight 6, non-unique. `f01-any-0028` is the alpha unique (weight 0, hand-pick, exclusive) and stays as the unique copy.

**Card (replaces the content of `f01-z09-0015`; `f01-any-0028` uses the same text with its own id, zone, weight, unique, exclusive_to, reskin and box fields):**

```json
{
  "id": "f01-z09-0015",
  "floor": 1,
  "zone": "z09",
  "tier": "Bronze",
  "box_types": [
    "any"
  ],
  "pull_type": "gear",
  "kind": "item",
  "reskin_name": "Wardrobe-Rack Hoodie, Many Moods",
  "real_5e_name": "Cloak of Many Fashions (house)",
  "source_5e": "HOUSE",
  "rarity": "Common",
  "attunement": null,
  "category": "Misc",
  "plain_mechanics": {
    "text": "Worn as your outer garment (no attunement). Bonus Action: change its style, color and apparent quality to any cloak, hoodie, cape or vest you have seen. Looks only: no AC, no powers, no bonus to any check. Weight does not change.",
    "action_cost": "Bonus Action",
    "range": null,
    "damage": null,
    "save_dc": null,
    "duration": "until you change it",
    "uses": null,
    "limits": "Cosmetic only. Copies the look of other garments, never their properties or magic. You can wear only one outer-garment magic item at a time (house). It always stays a garment of about its own size. Touching it reveals nothing odd.",
    "weight_lb": 1
  },
  "spoken_line": "Wardrobe-Rack Hoodie, Cloak of Many Fashions. Bonus Action: change its style and color. Looks only.",
  "snark_line": "Looks great on every Crawler. Looks do not stop knives.",
  "reward": "Wardrobe-Rack Hoodie, Cloak of Many Fashions. Bonus Action: change its style and color. Looks only.",
  "canon_status": "CANON-INSPIRED",
  "credit_value": 50,
  "draw_weight": 6,
  "unique": false,
  "tailor_tags": [
    "clothing"
  ],
  "exclusive_to": null,
  "grant": null,
  "ledger": {
    "type": "item",
    "text": "item +1 Bronze box: Wardrobe-Rack Hoodie, Many Moods (Cloak of Many Fashions (house))"
  },
  "box_name": "Changed Outfits Mid-Fight Box",
  "deed": "Switched costumes backstage",
  "notes": "HOUSE design (rules/42-house-items-f01.md §2). Follows the general shape of the DMG cloak from memory; not copied, not checked against the book. Same text for f01-any-0028 (unique, weight 0, exclusive card for the alpha holder): only id, zone, weight, unique, exclusive_to, reskin and box fields differ."
}
```

---

## 3. Pole of Collapsing, reskinned "Collapsible Tent-Pole" (HOUSE, Common, no attunement)

**Rules text.** It works as a 10 ft Pole (SRD 5.2 gear): you can touch something up to 10 ft away, and you have Advantage on a Strength (Athletics) check to vault in a High or Long Jump. While you hold it, a **Magic action** collapses it to a 1 ft rod (weight unchanged, 7 lb) or extends it back to 10 ft. When it extends, it stops where something blocks it; it never pushes or hurts anything, so it is not a weapon. One change per action. No uses, no charges, no limit.

**Why it is balanced:** a Common utility; its use is prodding traps and pressure plates from 10 ft, which the Floor 1 trap lessons already reward. Not a damage tool.
**Zone and weight (Lore's, kept):** `f01-any-0029`, floor-wide deck, weight 6, non-unique (alpha-issued; other Crawlers can still draw it).
**Consistency fix:** the Pole row in spec §3.1 now reads "Magic action" (it said "Action").

**Card:**

```json
{
  "id": "f01-any-0029",
  "floor": 1,
  "zone": "any",
  "tier": "Bronze",
  "box_types": [
    "any"
  ],
  "pull_type": "gear",
  "kind": "item",
  "reskin_name": "Collapsible Tent-Pole",
  "real_5e_name": "Pole of Collapsing (house)",
  "source_5e": "HOUSE",
  "rarity": "Common",
  "attunement": null,
  "category": "Misc",
  "plain_mechanics": {
    "text": "Works as a 10 ft Pole. Magic action while holding it: collapse it to a 1 ft rod (weight unchanged) or extend it back to 10 ft; it stops growing where something blocks it. As a Pole you can touch something up to 10 ft away, and you have Advantage on a Strength (Athletics) check to vault in a High or Long Jump. Not a weapon: extending it pushes and damages nothing.",
    "action_cost": "Magic action",
    "range": null,
    "damage": null,
    "save_dc": null,
    "duration": "until you change it",
    "uses": null,
    "limits": "No attack or damage use; one change per action. Collapsed it is a plain 1 ft rod. Extending into a creature or object stops it at that point.",
    "weight_lb": 7
  },
  "spoken_line": "Collapsible Tent-Pole, Pole of Collapsing. Magic action: collapse to one foot or extend to ten.",
  "snark_line": "Easy to carry. Hard to explain.",
  "reward": "Collapsible Tent-Pole, Pole of Collapsing. Magic action: collapse to one foot or extend to ten.",
  "canon_status": "CANON-INSPIRED",
  "credit_value": 50,
  "draw_weight": 6,
  "unique": false,
  "tailor_tags": [
    "tools"
  ],
  "exclusive_to": null,
  "grant": null,
  "ledger": {
    "type": "item",
    "text": "item +1 Bronze box: Collapsible Tent-Pole (Pole of Collapsing (house))"
  },
  "box_name": "Poked Something Gently Box",
  "deed": "Prodded a trap or hazard from afar",
  "notes": "HOUSE design (rules/42-house-items-f01.md §3). DMG shape from memory, not copied. Action cost is Magic action (2024 term). The Pole part follows the SRD 5.2 Pole. Alpha item, kept low weight for redraw by other Crawlers."
}
```

---

## 4. Mystery Key, reskinned "Gas-Station Bathroom Key on a Hubcap" (HOUSE, Common, no attunement)

**Rules text.** A one-use key. At the draw, the GM picks one lock on the current floor (written in session state, GM only). Utilize action to try the key: on **its** lock it opens it and the key is spent; on any other lock nothing happens and the key is kept. It cannot open a lock sealed by a boss, a spine object or a magic barrier, and the GM never makes it the only way through a required door. If you leave the floor with it unused, it turns into a plain hubcap key worth nothing. 1 lb.

**Accountant check:** it is a one-shot lock opener with a discovery hook, not stronger than one, so `credit_value` stays **25** (Bronze). If a table lets it open any lock on the floor or be reused, raise toward 50 and keep it Bronze.
**GM note:** the Zone S door can be the lock (the service key and Thieves' Tools DC 15 also open it), but using it there lets the party skip Dean Thudd and the Boss Box. Prefer optional rooms: the Break Room supply cabinet, a locker bank, the 3b Lost & Found cage.
**Zones and weights (Lore's, kept):** `f01-any-0035` weight 5 and `f01-z06-0004` (Break Room) weight 6. Both are non-unique; both must carry the same text.
**Not the 5e item:** the real Mystery Key is a chance-based key; this is a different, single-lock house item.

**Card (`f01-z06-0004` uses the same text with zone `z06`, id and weight 6):**

```json
{
  "id": "f01-any-0035",
  "floor": 1,
  "zone": "any",
  "tier": "Bronze",
  "box_types": [
    "any"
  ],
  "pull_type": "weird",
  "kind": "key",
  "reskin_name": "Gas-Station Bathroom Key on a Hubcap",
  "real_5e_name": "Mystery Key (house, single lock)",
  "source_5e": "HOUSE",
  "rarity": "Common",
  "attunement": null,
  "category": "Keys",
  "plain_mechanics": {
    "text": "Utilize action: opens one specific lock on this floor, picked by the GM when the key is drawn (the GM does not say which). On that lock it unlocks it and the key is spent. On any other lock nothing happens and it is not spent. If you leave the floor with it unused, it becomes a plain hubcap key.",
    "action_cost": "Utilize action",
    "range": null,
    "damage": null,
    "save_dc": null,
    "duration": "until used or you leave the floor",
    "uses": {
      "max": 1,
      "recharge": "none"
    },
    "limits": "One use, one lock. Cannot open a lock sealed by a boss, spine object or magic barrier. Never the only way through a required door.",
    "weight_lb": 1
  },
  "spoken_line": "Gas-Station Bathroom Key on a Hubcap. House Mystery Key: opens one GM-chosen lock on this floor; spent on use.",
  "snark_line": "It opens something, and the System is not telling.",
  "reward": "Gas-Station Bathroom Key on a Hubcap. House Mystery Key: opens one GM-chosen lock on this floor; spent on use.",
  "canon_status": "HOUSE",
  "credit_value": 25,
  "draw_weight": 5,
  "unique": false,
  "tailor_tags": [],
  "exclusive_to": null,
  "grant": null,
  "ledger": {
    "type": "key",
    "text": "item +1 Bronze box: Gas-Station Bathroom Key on a Hubcap (Mystery Key (house, single lock))"
  },
  "box_name": "Found the Right Key Eventually Box",
  "deed": "Hunted for a way through a locked door",
  "notes": "HOUSE design (rules/42-house-items-f01.md §4). GM only: pick the lock now and write it into session state, not this deck. Optional rooms are best (Break Room supply cabinet, a locker bank, the 3b Lost & Found cage). Zone S door works but skips the boss and the Boss Box, so decide on purpose. The real 5e Mystery Key is a chance-based key; this is a different item. Same text for f01-z06-0004 (weight 6)."
}
```

---

## 5. Potion of Fire Breath (HOUSE, Uncommon, no attunement)

**Rules text.** Drink it as a Bonus Action. For 1 hour, you can use a Bonus Action to exhale fire at one creature you can see within 30 ft. It makes a Dexterity save, DC 13: 4d6 Fire on a failure, half on a success. After three exhalations, or after 1 hour (whichever comes first), the effect ends. As with any fire effect, the GM may ignite flammable objects that are not worn or carried.

### 5.1 Balance notes (level 1-2)
- Uncommon is the Floors 1-2 peak, so it sits at the ceiling. It is a **Silver** card (Silver boxes are 0-1 per Crawler per floor, core §4.5).
- 4d6 averages 14: a failed save outright kills most Floor 1 mobs; three uses is a strong burst for a level 1-2 Crawler, comparable to three casts of a level 1 spell. It is consumable, one hour, single target.
- Compared with Alchemist's Fire (1d4, Bronze 50), it is a Silver-tier item at credit_value 200, inside the Silver 100-500 range.
- Reskin freely (spec §2.5). The mechanics line must still be read.

**Zone and weight (Lore's, kept):** `f01-any-0041`, floor-wide deck, weight 10, non-unique.
**Option for Caleb (not applied):** if 4d6 feels too hot at level 1, drop it to 3d6, DC 12 (average 10.5) and credit_value 150.

**Card:**

```json
{
  "id": "f01-any-0041",
  "floor": 1,
  "zone": "any",
  "tier": "Silver",
  "box_types": [
    "any"
  ],
  "pull_type": "consumable",
  "kind": "consumable",
  "reskin_name": "Pocket Dragon Breath Mints (Extra Strong)",
  "real_5e_name": "Potion of Fire Breath (house)",
  "source_5e": "HOUSE",
  "rarity": "Uncommon",
  "attunement": null,
  "category": "Consumables",
  "plain_mechanics": {
    "text": "Drink (Bonus Action). For 1 hour, as a Bonus Action you can exhale fire at one creature you can see within 30 ft: Dex save DC 13, 4d6 Fire on a failure, half on a success. Ends after three exhalations or after 1 hour, whichever comes first.",
    "action_cost": "Bonus Action",
    "range": "30 ft",
    "damage": "4d6 Fire (half on save)",
    "save_dc": "Dex DC 13",
    "duration": "1 hour or 3 uses",
    "uses": {
      "max": 3,
      "recharge": "none"
    },
    "limits": "One exhalation per Bonus Action. Single target, no area. Spent after the third exhalation or the hour. As with any fire effect, flammable unattended objects it hits may ignite (GM).",
    "weight_lb": 0.5
  },
  "spoken_line": "Pocket Dragon Breath Mints, Potion of Fire Breath. Three bonus action blasts, thirty feet, four d six fire, dex save thirteen.",
  "snark_line": "Your breath finally has a purpose.",
  "reward": "Pocket Dragon Breath Mints, Potion of Fire Breath. Three bonus action blasts, thirty feet, four d six fire, dex save thirteen.",
  "canon_status": "CANON-INSPIRED",
  "credit_value": 200,
  "draw_weight": 10,
  "unique": false,
  "tailor_tags": [
    "fire",
    "explosives"
  ],
  "exclusive_to": null,
  "grant": null,
  "ledger": {
    "type": "item",
    "text": "item +1 Silver box: Pocket Dragon Breath Mints (Extra Strong) (Potion of Fire Breath (house))"
  },
  "box_name": "Burned the Whole Hallway Box",
  "deed": "Used fire in a closed space",
  "notes": "HOUSE design (rules/42-house-items-f01.md §5). Numbers follow Lore's draft, which matches secondary listings of the DMG potion; not checked against the book. Uncommon, so inside the Floors 1-2 peak. Open: 4d6 at level 1 is strong (rules/42 §5.4)."
}
```

---

## 6. Enhanced Pet Biscuit and the other Story Box items (HOUSE, Legendary Story Boxes)

### 6.1 Canon basis and honesty
- Canon (ledger, wiki-sourced, not checked against the novels): **L-001** (Legendary tier; the Legendary Pet Box Carl opened in the tutorial), **I-007** (Enhanced Pet Biscuit: consumable, effects random, 100+ possible, source Legendary Pet Box), **M-037** (consumers include Donut and Prepotente), **C-028** (pets get classes only through a rare biscuit-type exception; the pet then becomes a Crawler who must pick a class in a saferoom), **R-062** (Prepotente became a Caprid), **A-165** and **A-167** (box names below). The ledger does not give the exact tutorial trigger deed or System text for the Pet Box; `trigger_deed` below is a HOUSE guess for the GM to judge.
- Mechanics are **HOUSE**. Canon effects are random and wide; we state one fixed core effect and a small d4 quirk table so the item is never vague.
- **Story Box status (2026-10-04):** Core §4.1 still states the ordinary floor ceiling, but Caleb approved the narrow Story Box exception. `rules/45-story-boxes-5e.md` v0.2 is the authoritative system; it remains a draft with one open question left (item strength; Caleb answered the other five on 2026-10-04). The Story Box path is active as governed there; this card is `draw_weight` 0 and hand-picked only.

### 6.2 Rules text
**Feed it to your pet (Utilize action, within 5 ft).** The target must be a willing Beast of CR 1/4 or lower that is your pet or companion (the GM decides what counts). It becomes a **Crawler** at once:
- **System actions:** it gets the System interface: inventory (core §5.9), map, achievements, and its own boxes (opened in a saferoom, core §4.4). It can be offered a class.
- **Class and level:** at the next saferoom it picks a class and builds as a Crawler by the character creation rules (characters/character-creation-5e.md), at the party's current level.
- **Stat block upgrade:** its Intelligence, Wisdom and Charisma rise to at least 10; it keeps its Size, Speed, senses and natural attacks; it gains hit points from its class Hit Die. It keeps the Beast type. It has no hands: items that need hands are the GM's call, and spells use paws or tail for somatic parts.
- **Speech:** it speaks Common (Donut-style). The GM may restrict this to System text if speech does not fit the pet.
- **Limits:** one conversion per living pet-Crawler (a deleted pet-Crawler frees it, and a new conversion needs a new biscuit); no effect on a creature that is already a Crawler; irreversible; one Biscuit Quirk (d4: 1 shimmering coat, 2 dramatic voice, 3 Darkvision 30 ft if it has none, 4 GM picks a body change in the style of the species supplement).
- **Companion rules in core:** core §2.4 lets the System issue one **Assigned Companion** only in a 2-Crawler game (CR at most half the party level, takes no loot, can die). A Biscuit-made Crawler is not that: it takes loot, boxes and class levels. Per Caleb (2026-10-04) it is a **separate player-controlled Crawler played by the player who made it** (the pet's owner), takes **no extra player slot** and **counts for encounter budgets**.

### 6.3 Card (Story Box; tier `Legendary` exactly as in the §1.1 enum, `draw_weight` 0, hand-pick only)

`credit_value` is 0 and `story_value` is provenance only (rules/45 §4.5). The item is tradeable and the System buys it back for a fixed `sale_value` of 100 (rung 0, rules/45 §4.6). `story_value` 40,000 is inside the Legendary 20,000-250,000 band (spec §3.2); Caleb may move it.

**Power note (rules/45 §4.5).** `power_note: Story keystone (pattern C), consumed once, rung 0 numbers: the new Crawler is a CR 1/4 Beast stat block plus a class at party level, so it adds a Crawler to encounter budgets and uses the owner's one consumable for the floor. Tradeable like any Story Box item but usable only on the pet named in the deed; cannot be duplicated; one conversion per living pet-Crawler (a deleted pet-Crawler frees its conversion; a new one needs a new biscuit). The new Crawler is a separate player-controlled Crawler played by its owner's player, with no extra player slot. Hook: the pet now has opinions, and the audience adores it.`

```json
{
  "id": "f01-any-0055",
  "floor": 1,
  "zone": "any",
  "tier": "Legendary",
  "box_types": [
    "any"
  ],
  "pull_type": "weird",
  "kind": "consumable",
  "reskin_name": "Enhanced Pet Biscuit",
  "real_5e_name": "Enhanced Pet Biscuit (house: pet-to-Crawler consumable)",
  "source_5e": "HOUSE",
  "rarity": "Legendary",
  "attunement": null,
  "category": "Consumables",
  "plain_mechanics": {
    "text": "Utilize action: feed it to your willing pet (a Beast, CR 1/4 or lower). The pet becomes a Crawler: it gets the System interface (inventory, map, achievements, boxes), speech, Int/Wis/Cha of at least 10, and a class at the next saferoom (level = party level). One biscuit per pet, once. No effect on a creature that is already a Crawler.",
    "action_cost": "Utilize action",
    "range": "5 ft",
    "damage": null,
    "save_dc": null,
    "duration": "permanent",
    "uses": {
      "max": 1,
      "recharge": "none"
    },
    "limits": "Pet only: the GM decides what counts as yours. Irreversible. Roll d4 for one Biscuit Quirk (rules/42 §6.2). Boxes and loot of the new Crawler follow core §4.4 like any Crawler's.",
    "weight_lb": 0.1
  },
  "spoken_line": "Enhanced Pet Biscuit. Feed it to your pet: the pet becomes a Crawler, with a System interface and a class at the next saferoom.",
  "snark_line": "Good boy. Good, billable, ratings-eligible boy.",
  "reward": "Enhanced Pet Biscuit. Feed it to your pet: the pet becomes a Crawler, with a System interface and a class at the next saferoom.",
  "canon_status": "CANON-INSPIRED",
  "credit_value": 0,
  "story_value": 40000,
  "sale_value": 100,
  "bound": false,
  "draw_weight": 0,
  "unique": true,
  "tailor_tags": [
    "pets"
  ],
  "exclusive_to": null,
  "grant": null,
  "ledger": {
    "type": "item",
    "text": "item +1 Legendary Story Box: Enhanced Pet Biscuit (story value 40000)"
  },
  "box_name": "Pet Box",
  "deed": "Brought a pet into the Crawl",
  "notes": "Story Box card (rules/45 §4.5): GM-triggered only, hand-pick, never drawn. trigger_deed: first Crawler at the table to bring a pet into the Crawl, judged by the GM (canon trigger not captured in the ledger). power_note: Story keystone (pattern C), consumed once, rung 0 numbers: the new Crawler is a CR 1/4 Beast stat block plus a class at party level, so it adds a Crawler to encounter budgets and uses the owner's one consumable for the floor. Tradeable like any Story Box item but usable only on the pet named in the deed; cannot be duplicated; one conversion per living pet-Crawler (a deleted pet-Crawler frees its conversion; a new one needs a new biscuit). The new Crawler is a separate player-controlled Crawler played by its owner's player, with no extra player slot. Hook: the pet now has opinions, and the audience adores it. Banner adds the tier: Legendary Pet Box. Item canon I-007 and M-037; mechanics are HOUSE."
}
```

### 6.4 Box stubs (to design, not cards yet)
- **Legendary Quadruped Box** (ledger A-165, F1/B1, VERIFIED cite B1 ch7; no System text captured). Deed: being the first cat to enter the dungeon. Designed in v0.2: see §6.5 (Tiara of Bloody Succession, card 0056).
- **That's the Spirit! Box** (ledger A-167, F1/B3, VERIFIED cite B3 ch19; no System text captured). Deed: entering the dungeon while fighting a family member. Designed in v0.2: see §6.6 (Grudge Ring, card 0057).

### 6.5 Quadruped Box: Tiara of Bloody Succession (card `f01-any-0056`, story_value 60,000, tradeable)

**Basis.** Box and deed are canon (A-165, first cat into the dungeon); the table rule widens the deed to any quadruped companion. Canon contents were the Crown of the Sepsis Whore; every number below is HOUSE. No SRD 5.2 item matches, so it is a house item (checked against the SRD text on the box; no item of that name).

**Rules text.** Wear it (no attunement). It sits on one creature's head and resizes to fit any quadruped or biped. While it is worn:
- You get +2 to Intelligence checks (not saves, attack rolls or spell DCs).
- You have Advantage on your first Charisma (Persuasion) check against each creature that has not met you.
- **Sepsis rider.** Once per turn, right after you hit with an attack, roll a d20. On an 18 or higher the target makes a DC 12 Constitution saving throw or has the Poisoned condition until the end of its next turn. Creatures immune to Poisoned are not affected.
- **Fleeting.** If the Tiara leaves the wearer's head for any reason, it crumbles and the GM places it somewhere else on the same floor, within fair reach of the party and with a clue. The owner puts it on again. If you go downstairs wearing it, it goes with you.
- It gives a non-sapient wearer no speech. Story hook only: wearing it enters the wearer in the Blood Sultanate line of succession (a Floor 9 thread; no effect on Floors 1-2).

**Tradeable.** It belongs to the Crawler whose companion earned it, but it is not bound: it can be traded, looted from a corpse or sold. Buyback `sale_value` 500 (rung 2 until retuned, rules/45 §4.6); `story_value` is provenance only. The owner decides whether the Crawler or the companion wears it.
**Deed trigger.** The first quadruped companion (any four-legged creature, not only a cat) enters the Crawl with a Crawler at the table, judged by the GM.
**POWER NOTE (Syndicate).** +2 on Intelligence checks only and a 15 percent, one-turn Poisoned rider: no AC, attack, save or damage bonus, so armor, weapons and Silver loot stay the main upgrades on Floors 1-2.
**GM records.** The owner, the wearer, the companion's species and the deed; the ledger line `story value 60000` (provenance only); the override reason if this is not the first Story Box on the floor (the same pet probably also earns the Pet Box, so expect an override); each time the Tiara Fleets and where the GM put it; the Blood Sultanate succession flag in session state (Floor 9 thread, no effect before then).

```json
{
  "id": "f01-any-0056",
  "floor": 1,
  "zone": "any",
  "tier": "Legendary",
  "box_types": [
    "any"
  ],
  "pull_type": "weird",
  "kind": "item",
  "reskin_name": "Tiara of Bloody Succession (Fits Any Head, Fits Any Paws)",
  "real_5e_name": "Circlet of Quick Wits (house: Fleeting +Int crown)",
  "source_5e": "HOUSE",
  "rarity": "Uncommon",
  "attunement": null,
  "category": "Misc",
  "plain_mechanics": {
    "text": "Worn on the head by one creature (no attunement); it resizes to fit any quadruped or biped. While worn: +2 bonus to Intelligence checks, and Advantage on your first Charisma (Persuasion) check against each creature that has not met you. Once per turn, right after you hit with an attack, roll a d20: on 18 or higher the target makes a DC 12 Constitution save or has the Poisoned condition until the end of its next turn. Fleeting: if it leaves the wearer's head for any reason it crumbles and the GM places it elsewhere on this floor.",
    "action_cost": "None (passive)",
    "range": "Self",
    "damage": "Poisoned (Sepsis rider)",
    "save_dc": "Con DC 12 (Sepsis rider)",
    "duration": "while worn",
    "uses": null,
    "limits": "The +2 applies to Intelligence checks only, not saves, attack rolls or spell DCs. The Poisoned rider is once per turn and does nothing to creatures immune to Poisoned. One crown exists at a time. It gives a non-sapient wearer no speech. Fleeting: the GM sets the new place within fair reach of the party, with a clue; the owner puts it on again; if you go downstairs wearing it, it goes with you. Not bound: tradeable, lootable and sellable; the owner decides who wears it. Story hook only: wearing it enters the wearer in the Blood Sultanate line of succession (a Floor 9 thread; no effect on Floors 1-2).",
    "weight_lb": 0.5
  },
  "spoken_line": "Tiara of Bloody Succession, Circlet of Quick Wits. Plus two to Intelligence checks, fits any quadruped, and vanishes if removed.",
  "snark_line": "Every four-legged Crawler deserves a crown, and this one comes with a grudge.",
  "reward": "Tiara of Bloody Succession, Circlet of Quick Wits. Plus two to Intelligence checks, fits any quadruped, and vanishes if removed.",
  "canon_status": "CANON-INSPIRED",
  "credit_value": 0,
  "draw_weight": 0,
  "unique": true,
  "tailor_tags": [
    "pets"
  ],
  "exclusive_to": null,
  "grant": null,
  "ledger": {
    "type": "item",
    "text": "item +1 Legendary Story Box: Tiara of Bloody Succession (Circlet of Quick Wits (house)) (story value 60000)"
  },
  "box_name": "Quadruped Box",
  "deed": "First quadruped companion into the Crawl",
  "notes": "HOUSE design (rules/42-house-items-f01.md §6.5). GM-triggered Story Box (spec 2.8): hand-pick only (weight 0), tradeable (not bound), never drawn at random. Cap one per table per floor (log an override to exceed). LEDGER: L-001, A-165, I-014, M-231, M-232. trigger_deed: the first quadruped companion (any four-legged creature, not only a cat) enters the Crawl with a Crawler at the table, judged by the GM. power_note: +2 on Intelligence checks only, no AC, attack, save or damage bonus, and a 15 percent Poisoned rider that lasts one turn, so armor, weapons and Silver loot stay the main upgrades. Canon: box and deed are canon (A-165, VERIFIED B1 ch7; any quadruped is a HOUSE table rule); canon contents were the Crown of the Sepsis Whore; numbers here are HOUSE.",
  "story_value": 60000,
  "sale_value": 500,
  "bound": false
}
```

### 6.6 That's the Spirit! Box: Grudge Ring (card `f01-any-0057`, story_value 80,000, tradeable, session-zero opt-in)

**Basis.** Box and deed are canon (A-167). The canon ring is tied to a killing within a family, so this card runs only with the table's session-zero opt-in; the table rule (rules/45 §2.4, Caleb 2026-10-04) is a fictional rival, opt-in at session zero, no killing, no PvP. Canon ring is +5 percent to all stats plus the Marked for Death skill; the numbers below are HOUSE and the item name is not in SRD 5.2. It is **not** the core §6.7 Marked for Death Band (a revival curse): if one Crawler holds both, only one no-healing rule applies at a time and each mark is tracked on its own.

**Rules text.** Requires attunement (it counts toward the three-item limit) and the session-zero opt-in. Once per Long Rest, spend 30 seconds focusing (so only outside combat) to mark one hostile non-Crawler creature that you can see within 60 ft, that is at full hit points, and that the GM agrees is a real threat (no vermin, no noncombatants). One mark at a time.
- While the mark lives you cannot regain hit points by any means: healing spells, potions, Hit Point Dice, rests and the Stairwell Checkpoint do nothing. Temporary hit points and stabilizing still work.
- When the marked creature dies, from any cause, you regain all your hit points and gain Heroic Inspiration. If you already hold it, give the new one to another Crawler (core rule).
- You can take the ring off at any time. The mark ends, you get no reward, and the use stays spent until your next Long Rest. The mark also ends with no reward if you leave the floor.
- It never marks Crawlers (no PvP, Caleb 2026-10-04).
- Hunters of Floor 6 will target the wearer (GM hook, no effect on Floors 1-2). No permanent stat bonus.

**Tradeable.** Not bound: it can be traded, looted from a corpse or sold. Buyback `sale_value` 500 (rung 2 until retuned, rules/45 §4.6); `story_value` is provenance only.
**Deed trigger.** A Crawler enters the Crawl in a fight with an opted-in fictional rival from their backstory, set up at session zero (no killing, no PvP; rules/45 §2.4). Without the opt-in, do not run it.
**POWER NOTE (Syndicate).** A risk trade, not a free upgrade: no healing of any kind until the mark dies, and the full heal plus Inspiration pays out at most once per Long Rest, so potions, armor and Boss Box loot stay the main upgrades.
**GM records.** The opt-in (who agreed, session zero date) and the reframe used; who is attuned; each mark (creature, zone, start time) and how it ended (died, ring removed, left floor); any Heroic Inspiration passed on; the Floor 6 hunters hook in session state; the ledger line `story value 80000` (provenance only); any cap override.

```json
{
  "id": "f01-any-0057",
  "floor": 1,
  "zone": "any",
  "tier": "Legendary",
  "box_types": [
    "any"
  ],
  "pull_type": "weird",
  "kind": "item",
  "reskin_name": "Grudge Ring (Green Glass, Red Stone)",
  "real_5e_name": "Ring of Divine Suffering (house: Marked for Death ring)",
  "source_5e": "HOUSE",
  "rarity": "Rare",
  "attunement": "yes",
  "category": "Misc",
  "plain_mechanics": {
    "text": "Requires attunement and the table's session-zero opt-in. Once per Long Rest, spend 30 seconds focusing (so outside combat) to mark one hostile non-Crawler creature you can see within 60 ft that is at full hit points and that the GM agrees is a real threat (no vermin, no noncombatants). One mark at a time. While the mark lives you cannot regain hit points by any means (temporary hit points and stabilizing still work). When it dies, from any cause, you regain all your hit points and gain Heroic Inspiration.",
    "action_cost": "30 seconds of focus (outside combat)",
    "range": "60 ft",
    "damage": "Mark (no damage)",
    "save_dc": "None",
    "duration": "until the mark dies, you take the ring off, or you leave the floor",
    "uses": {
      "max": 1,
      "recharge": "long rest"
    },
    "limits": "Session-zero opt-in required (the canon ring is tied to a family killing; use the fictional-rival rule of rules/45 §2.4 instead of kin). Never marks Crawlers (no PvP). No healing of any kind while a mark is active, including potions, spells, Hit Point Dice, rests and the Stairwell Checkpoint. You may take the ring off at any time: the mark ends, you get no reward, and the use is spent until your next Long Rest. The mark ends with no reward if you leave the floor. If you already hold Heroic Inspiration, give the new one to another Crawler (core rule). Counts toward the three attunement slots. Tradeable and sellable (not bound). Hunters of Floor 6 will target the wearer (GM hook, no effect on Floors 1-2). No permanent stat bonus.",
    "weight_lb": 0
  },
  "spoken_line": "Grudge Ring, Ring of Divine Suffering. Once per long rest, mark one foe: no healing for you until it dies, then full health and Inspiration. Opt-in only.",
  "snark_line": "It sounds scary because it is, and it does not care who you were angry at.",
  "reward": "Grudge Ring, Ring of Divine Suffering. Once per long rest, mark one foe: no healing for you until it dies, then full health and Inspiration. Opt-in only.",
  "canon_status": "CANON-INSPIRED",
  "credit_value": 0,
  "draw_weight": 0,
  "unique": true,
  "tailor_tags": [],
  "exclusive_to": null,
  "grant": null,
  "ledger": {
    "type": "item",
    "text": "item +1 Legendary Story Box: Grudge Ring (Ring of Divine Suffering (house)) (story value 80000)"
  },
  "box_name": "That's the Spirit! Box",
  "deed": "Entered the Crawl fighting a fictional rival",
  "notes": "HOUSE design (rules/42-house-items-f01.md §6.6). GM-triggered Story Box (spec 2.8): hand-pick only (weight 0), tradeable (not bound), never drawn at random. Cap one per table per floor (log an override to exceed). LEDGER: L-001, A-167, I-025, S-011, M-233, X-054. trigger_deed: a Crawler enters the Crawl in a fight with an opted-in fictional rival from their backstory, set up at session zero (no killing, no PvP). Do NOT run it without the opt-in: the canon ring is tied to a killing within a family. power_note: double-edged and Rare, so it is a risk trade (no healing until the mark dies, one full heal plus Inspiration per Long Rest at most), not a free upgrade. Canon: box and deed canon (A-167, VERIFIED B3 ch19; Legendary vs Platinum tier conflict X-054, Legendary preferred); canon ring is +5 percent all stats plus the Marked for Death skill (I-025, S-011); numbers here are HOUSE. Not the same item as the core 6.7 Marked for Death Band (revival curse).",
  "story_value": 80000,
  "sale_value": 500,
  "bound": false
}
```

### 6.7 Pacifist's Box: Olive Branch Lanyard (card `f01-any-0058`, story_value 30,000, tradeable)

**Basis.** Pacifist's Box is canon (L-B43, A-092) but the Legendary versions went to Meadow Lark on Floor 3 (B2 ch8), so this Floor 1 version is HOUSE. Name and mechanics are house; no SRD item matches.

**Rules text.** Reaction, once per Long Rest: when a creature you can see, and have not damaged, is about to make an attack roll against you, it makes a DC 13 Wisdom saving throw. On a failure it must pick a different target within its reach or range, or lose the attack.
- It does nothing to a creature that is immune to the Charmed condition (GM call) and does not stop area effects.
- The attacker chooses the new target, which may be one of your allies.

**Tradeable.** Not bound: it can be traded, looted from a corpse or sold. Buyback `sale_value` 500 (rung 2 until retuned, rules/45 §4.6); `story_value` is provenance only.
**Deed trigger.** The Crawler (or the whole party) reaches the Floor 1 stairwell without having killed anything. A kill is a creature reduced to 0 hit points by the Crawler's own attack, spell or action. Traps, allies and the environment do not count against them; the GM judges. If the whole party qualifies there is still one Lanyard and the party names its owner.
**POWER NOTE (Syndicate).** One defensive redirect per Long Rest that only works on foes you have not hurt, with no damage; armor, shields and healing stay the main defenses.
**GM records.** Who qualified and who owns it; the stairwell time and the "no kills" check (what was ruled not to count); each use and its target; the ledger line `story value 30000` (provenance only); any cap override. It is awarded at the Floor 2 threshold, so it never competes with Floor 1 loot.

```json
{
  "id": "f01-any-0058",
  "floor": 1,
  "zone": "any",
  "tier": "Legendary",
  "box_types": [
    "any"
  ],
  "pull_type": "weird",
  "kind": "item",
  "reskin_name": "Olive Branch Lanyard (Laminated, Nobody Got Hurt)",
  "real_5e_name": "Olive Branch Lanyard (house: redirect charm)",
  "source_5e": "HOUSE",
  "rarity": "Uncommon",
  "attunement": null,
  "category": "Misc",
  "plain_mechanics": {
    "text": "Reaction, once per Long Rest: when a creature you can see, and have not damaged, is about to make an attack roll against you, it makes a DC 13 Wisdom save. On a failure it must pick a different target within its reach or range, or lose the attack.",
    "action_cost": "Reaction",
    "range": "Sight",
    "damage": "None",
    "save_dc": "Wis DC 13",
    "duration": "instant",
    "uses": {
      "max": 1,
      "recharge": "long rest"
    },
    "limits": "Only works against a creature you have not damaged. One use per Long Rest. It does nothing to a creature that is immune to the Charmed condition (GM call) and does not stop area effects. The attacker chooses the new target, which may be one of your allies. Tradeable and sellable (not bound).",
    "weight_lb": 0
  },
  "spoken_line": "Olive Branch Lanyard. Once per long rest, a creature you have not hurt that attacks you must pick another target or lose its attack.",
  "snark_line": "Proof that you did it all without hurting anyone, laminated for your convenience.",
  "reward": "Olive Branch Lanyard. Once per long rest, a creature you have not hurt that attacks you must pick another target or lose its attack.",
  "canon_status": "CANON-INSPIRED",
  "credit_value": 0,
  "draw_weight": 0,
  "unique": true,
  "tailor_tags": [
    "pacifist"
  ],
  "exclusive_to": null,
  "grant": null,
  "ledger": {
    "type": "item",
    "text": "item +1 Legendary Story Box: Olive Branch Lanyard (story value 30000)"
  },
  "box_name": "Pacifist's Box",
  "deed": "Left Floor 1 without a single kill",
  "notes": "HOUSE design (rules/42-house-items-f01.md §6.7). GM-triggered Story Box (spec 2.8): hand-pick only (weight 0), tradeable (not bound), never drawn at random. Cap one per table per floor (log an override to exceed). LEDGER: L-001, L-B43, A-092. trigger_deed: the Crawler (or the whole party) reaches the Floor 1 stairwell without having killed anything; traps, allies and the environment killing do not count against them, the GM judges. If the whole party qualifies there is still one Lanyard: the party names its owner. power_note: one defensive redirect per Long Rest that only works on foes you have not hurt, with no damage, so armor, shields and healing stay the main defenses. Canon: Pacifist's Box is canon (L-B43, A-092) but the Legendary Pacifist's Boxes went to Meadow Lark on Floor 3 (B2 ch8), so this is a HOUSE Floor 1 version. Numbers HOUSE.",
  "story_value": 30000,
  "sale_value": 500,
  "bound": false
}
```

### 6.8 Stopped the Porkchop Express Box: Porkchop Express Wheel-Hub Maul (card `f01-any-0059`, story_value 35,000, tradeable)

**Basis.** The canon reward for the first Borough Boss is a Platinum Weapon Box (A-168), so Legendary is an approved HOUSE upgrade for a table-first. In the books Ball of Swine (B-003) is a level 15 Borough Boss; our F1 module (levels 1 to 2) has Dean Thudd (Ogre, CR 2) instead, so he counts as the Borough Boss unless the GM names another. The Maul, Heavy, Two-Handed and Topple are SRD 5.2 weapon terms; the +1 and the shove are house.

**Rules text.** A +1 maul: +1 to attack and damage rolls (Maul: 2d6 Bludgeoning, Heavy, Two-Handed, Topple, 10 lb). Once per Short Rest, when you hit with it, the target makes a DC 12 Strength saving throw or is pushed 10 ft and has the Prone condition.
- Heavy: Small creatures have Disadvantage on attack rolls with it. A Maul is a Martial weapon: without proficiency you add no Proficiency Bonus.
- Huge or larger creatures are unaffected by the push and Prone.
- If you also have the Topple mastery, use one effect per hit, not both.

**Tradeable.** The party names the first holder, but it is not bound: it can be traded, looted from a corpse or sold. Buyback `sale_value` 500 (rung 2 until retuned, rules/45 §4.6); `story_value` is provenance only.
**Deed trigger.** The first party at the table to defeat a Floor 1 Borough Boss, judged by the GM.
**POWER NOTE (Syndicate).** A +1 weapon (Uncommon) with one shove per Short Rest and no new damage dice, so armor, spells and the Silver Boss Box stay relevant.
**GM records.** Which boss, the date and the party; who owns it; each use of the short-rest shove; the ledger line `story value 35000` (provenance only) (separate from the Boss Box, which is the normal Silver reward); any cap override.

```json
{
  "id": "f01-any-0059",
  "floor": 1,
  "zone": "any",
  "tier": "Legendary",
  "box_types": [
    "any"
  ],
  "pull_type": "weird",
  "kind": "item",
  "reskin_name": "Porkchop Express Wheel-Hub Maul",
  "real_5e_name": "+1 Maul (house: Rolling Ruin)",
  "source_5e": "HOUSE",
  "rarity": "Uncommon",
  "attunement": null,
  "category": "Weapons",
  "plain_mechanics": {
    "text": "A +1 maul: +1 bonus to attack and damage rolls (Maul: 2d6 Bludgeoning, Heavy, Two-Handed, Topple, 10 lb). Once per short rest, when you hit with it, the target makes a DC 12 Strength save or is pushed 10 ft and has the Prone condition.",
    "action_cost": "Action",
    "range": "Melee",
    "damage": "2d6+1 Bludgeoning",
    "save_dc": "Str DC 12 (push and Prone)",
    "duration": "instant",
    "uses": {
      "max": 1,
      "recharge": "short rest"
    },
    "limits": "The push and Prone work only once per short rest. Heavy: Small creatures have Disadvantage on attack rolls with it. Huge or larger creatures are unaffected by the push and Prone. It is a Martial weapon: without proficiency you add no Proficiency Bonus. If you also have the Topple mastery, use one effect per hit, not both. Tradeable and sellable (not bound); the party names the first holder.",
    "weight_lb": 10
  },
  "spoken_line": "Porkchop Express Wheel-Hub Maul, plus one maul. Once per short rest, a hit pushes ten feet and knocks the target prone.",
  "snark_line": "Salvaged from something that rolled over a lot of people, and now it is your turn.",
  "reward": "Porkchop Express Wheel-Hub Maul, plus one maul. Once per short rest, a hit pushes ten feet and knocks the target prone.",
  "canon_status": "CANON-INSPIRED",
  "credit_value": 0,
  "draw_weight": 0,
  "unique": true,
  "tailor_tags": [
    "boss"
  ],
  "exclusive_to": null,
  "grant": null,
  "ledger": {
    "type": "item",
    "text": "item +1 Legendary Story Box: Porkchop Express Wheel-Hub Maul (story value 35000)"
  },
  "box_name": "Stopped the Porkchop Express Box",
  "deed": "First party to take down a Floor 1 Borough Boss",
  "notes": "HOUSE design (rules/42-house-items-f01.md §6.8). GM-triggered Story Box (spec 2.8): hand-pick only (weight 0), tradeable (not bound), never drawn at random. Cap one per table per floor (log an override to exceed). LEDGER: L-001, A-168, A-173, B-003. trigger_deed: the first party at the table to defeat a Floor 1 Borough Boss (Ball of Swine or any other the GM names; in the F1 module this is Dean Thudd unless the GM names another), judged by the GM. power_note: a +1 weapon (Uncommon) with one short-rest shove, no new damage dice, so armor and Silver Boss Box loot stay relevant. Canon: the canon reward for the first Borough Boss is a Platinum Weapon Box (A-168, VERIFIED B1 ch14), not Legendary, so Legendary is an approved HOUSE upgrade for a table-first; Ball of Swine is B-003 (level 15 in the books). Numbers HOUSE.",
  "story_value": 35000,
  "sale_value": 500,
  "bound": false
}
```

### 6.9 Pet Box: Pet Biscuit Crate (card `f01-any-0060`, story_value 20,000, tradeable; same box as 0055)

**Basis.** The canon Legendary Pet Box held Pet Biscuit x500 plus the Enhanced Pet Biscuit (M-228). Numbers are HOUSE; no SRD item matches.

**Rules text.** Utilize action, within 5 ft: feed one plain Pet Biscuit to a willing pet or companion Beast. It regains 1d4 hit points and is calm for 1 minute (it does not flee in panic, and you succeed on any Wisdom (Animal Handling) check to settle it).
- A pet gets this benefit from at most 3 biscuits per Long Rest; after that a biscuit is just a snack.
- Plain biscuits only: not Enhanced, no transformation, no effect on a Crawler (including a pet already turned into one by the Enhanced Pet Biscuit).
- The crate holds 500 biscuits and also covers the pet's ordinary food, so the GM does not track pet rations. 25 lb.

**Tradeable.** Not bound: it can be traded, looted from a corpse or sold. Buyback `sale_value` 100 (rung 0, rules/45 §4.6); `story_value` is provenance only.
**Deed trigger.** Same as card 0055: the first Crawler at the table to bring a pet into the Crawl.
**One box.** The crate and the Enhanced Pet Biscuit are two pulls of the one Legendary Pet Box. Award them together as ONE Story Box. Log 0055 normally and log 0060 with the override reason `same box` under the one-per-floor cap.
**POWER NOTE (Syndicate).** 1d4 healing for pets only, capped at 3 per pet per Long Rest, with no combat power, so it never replaces healing potions or Hit Point Dice.
**GM records.** The pet and its owner; the override `same box` on 0060; the ledger lines `story value 40000` (0055) and `story value 20000` (0060), both provenance only; a loose tally of biscuits used (500 will not run out, so no per-biscuit tracking).

```json
{
  "id": "f01-any-0060",
  "floor": 1,
  "zone": "any",
  "tier": "Legendary",
  "box_types": [
    "any"
  ],
  "pull_type": "weird",
  "kind": "item",
  "reskin_name": "Pet Biscuit Crate, Industrial (500)",
  "real_5e_name": "Pet Biscuit, plain (house: x500 supply)",
  "source_5e": "HOUSE",
  "rarity": "Common",
  "attunement": null,
  "category": "Consumables",
  "plain_mechanics": {
    "text": "Utilize action, within 5 ft: feed one plain Pet Biscuit to a willing pet or companion Beast; it regains 1d4 hit points and is calm for 1 minute (it does not flee in panic, and you succeed on any Wisdom (Animal Handling) check to settle it). A pet gets this benefit from at most 3 biscuits per Long Rest. The crate holds 500 biscuits.",
    "action_cost": "Utilize action",
    "range": "5 ft",
    "damage": "Heals 1d4",
    "save_dc": "None",
    "duration": "instant (calm lasts 1 minute)",
    "uses": {
      "max": 500,
      "recharge": "none"
    },
    "limits": "Plain biscuits only: not Enhanced, no transformation, no effect on a Crawler (including a pet already made a Crawler). Beyond 3 biscuits per pet per Long Rest a biscuit is just a snack. It also covers the pet's ordinary food. 25 lb. Tradeable and sellable (not bound). Awarded together with f01-any-0055 as one Story Box.",
    "weight_lb": 25
  },
  "spoken_line": "Pet Biscuit Crate. Five hundred plain biscuits: feed one to a pet to heal one d four and calm it, up to three per pet per long rest.",
  "snark_line": "Enough kibble to feed the entire Orientation Pit, if the Orientation Pit were a good boy.",
  "reward": "Pet Biscuit Crate. Five hundred plain biscuits: feed one to a pet to heal one d four and calm it, up to three per pet per long rest.",
  "canon_status": "CANON-INSPIRED",
  "credit_value": 0,
  "draw_weight": 0,
  "unique": true,
  "tailor_tags": [
    "pets"
  ],
  "exclusive_to": null,
  "grant": null,
  "ledger": {
    "type": "item",
    "text": "item +1 Legendary Story Box: Pet Biscuit Crate (story value 20000)"
  },
  "box_name": "Pet Box",
  "deed": "Brought a pet into the Crawl",
  "notes": "HOUSE design (rules/42-house-items-f01.md §6.9). GM-triggered Story Box (spec 2.8): hand-pick only (weight 0), tradeable (not bound), never drawn at random. LEDGER: L-001, L-020, I-007, M-228. trigger_deed: same deed as f01-any-0055 (the Enhanced Pet Biscuit): the first Crawler at the table to bring a pet into the Crawl. It is the second pull of the same Legendary Pet Box, so it is awarded together with f01-any-0055 as ONE Story Box; log this card with the override reason 'same box' under the one-per-floor cap. power_note: Common-level pet supply, 1d4 healing capped at 3 per pet per Long Rest, no combat power. Canon: the Legendary Pet Box held Pet Biscuit x500 plus the Enhanced Pet Biscuit (M-228, VERIFIED B1 ch5); healing and calm numbers are HOUSE.",
  "story_value": 20000,
  "sale_value": 100,
  "bound": false
}
```

### 6.10 What changes in Lore's Story Box cards (diff list)

Kept as Lore has them: ids, `tier`, `draw_weight` 0, `story_value` (now provenance only), `credit_value` 0, `box_name`, `deed`, `ledger`, snark lines, `tailor_tags`, `unique`, rarity (Uncommon, Rare, Uncommon, Uncommon, Common) and attunement. `bound` is no longer kept: see the first row of the table (Caleb, 2026-10-04). Only fields that change are listed. Lore decides what to apply; the card JSON in §6.5 to §6.9 is the full proposed result.

| Card | Field | Now | Change to | Why |
|---|---|---|---|---|
| 0055 to 0060 | bound, new sale_value, ledger.text, limits, notes | `bound: true`, no `sale_value`, "(story value N, bound)", "Bound (no sale or trade)" | `bound: false`; `sale_value` 100 (0055, 0060) or 500 (0056 to 0059, until retuned); "(story value N)"; "Tradeable and sellable (not bound)" | Caleb 2026-10-04: Story Box items are not bound; fixed System buyback per power rung (rules/45 §4.6); `story_value` is provenance only |
| 0057 | deed, trigger_deed, limits | "fighting kin", relative or kin NPC, PvP clause | fictional rival, no killing, no PvP | One family-fight rule (rules/45 §2.4); the mark mechanic still needs a Lore retune |
| 0056, 0057, 0060 | canon_status | `CANON` | `CANON-INSPIRED` | Box and deed are canon, the mechanics are HOUSE; matches card 0055 |
| 0056 | plain_mechanics.text, limits | draft | §6.5 card | Adds Poisoned wording, per-creature Persuasion, Fleeting placement rule, owner rule |
| 0057 | plain_mechanics.action_cost | `Magic action` | `30 seconds of focus (outside combat)` | A Magic action is one action; the text said 30 seconds |
| 0057 | plain_mechanics.uses.recharge | `5 hours` | `long rest` | Caps the full heal and Inspiration at once per day (core Inspiration pacing) |
| 0057 | plain_mechanics.text, limits, duration, spoken_line, reward | draft | §6.6 card | Hostile real-threat target, ring-removal exit, no-healing list, attunement slot note |
| 0058 | plain_mechanics.limits | "cannot be charmed or frightened" | "immune to the Charmed condition (GM call)" | The effect uses a Wisdom save, not Charmed or Frightened wording |
| 0058 | plain_mechanics.text, spoken_line, reward | draft | §6.7 card | Says "about to make an attack roll" (before the roll) |
| 0059 | plain_mechanics.limits | "Huge or larger creatures are not pushed" | "unaffected by the push and Prone" | The old line left Prone on Huge targets open |
| 0060 | plain_mechanics.text, limits, duration, spoken_line, reward | "GM limits how many a pet can eat per day" | 3 biscuits per pet per Long Rest; Calm defined | A concrete cap instead of a GM call |
| 0056 to 0060 | notes | draft | §6.5 to §6.9 notes | Point at rules/42; keep `trigger_deed` and `power_note` |

---

## 7. Open questions for Caleb

1. **Story Boxes on Floors 1-2 — RESOLVED 2026-10-04.** Caleb approved the narrow exception. `rules/45-story-boxes-5e.md` v0.2 is the authoritative system; it is a draft with one open question left (item strength; Caleb answered the other five on 2026-10-04).
2. **Cap — RESOLVED 2026-10-04.** One Story Box per table per floor, as core (the whole floor, not per play night); a logged override by Caleb only.
3. **Party cap for a pet turned Crawler — RESOLVED 2026-10-04.** A pet-Crawler uses **no player slot**, and it counts as a Crawler for encounter budgets and the 2-6 range.
4. **Who runs a pet-Crawler? — RESOLVED 2026-10-04.** The player who made it (the pet's owner) plays it as a separate player-controlled Crawler.
5. **Biscuit rarity and value.** Legendary rarity and `story_value` 40,000 as proposed?
6. **Fire Breath at level 1.** Keep 4d6, DC 13 (Lore's draft), or use the softer 3d6, DC 12 (§5)?
7. **Key on descent.** Should an unused Mystery Key turn into a plain key when you leave the floor (proposed), or carry to the next floor?
8. **One outer garment.** Keep the house rule that the Cloak shares a position with other cloak-type items?
9. **Rare ring on Floor 1.** The Grudge Ring is Rare and attunement; core §3.6 caps Floors 1-2 at Uncommon (spec §2.8 allows a Legendary box headline, not a stated exception for content). Allow it under the Story Box exception, or cut it to Uncommon (for example heal half your hit points instead of all)?
10. **Story Box cap versus five deeds.** All the Story Box deeds fall on Floor 1 (pet and quadruped at the door, kin fight at session zero, Borough Boss mid-floor, pacifist at the stairs). One per table per floor means most need an override. Keep the cap and override often, or make it one per Crawler per floor?
11. **Borough Boss in our module.** Ball of Swine is level 15; our Floor 1 boss is Dean Thudd (Ogre, CR 2). Confirm Dean counts as the Borough Boss for card 0059.
12. **Tiara leaving the floor.** Proposed: it goes with the wearer downstairs. Alternative: it Fleets to a random place on the next floor.
13. **Grudge Ring escape.** Proposed: the wearer can take the ring off to end a mark at the cost of the reward and that day's use. Alternative: no escape except the target's death (canon-harsher).

---

## 8. Changelog

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-10-04 | First draft: Cloak, Pole, Key, Fire Breath cards and diff list; Enhanced Pet Biscuit (0055) with two box stubs; open questions 1 to 8. |
| 0.2 | 2026-10-04 | Added §6.5 to §6.10: final text, bound, deed, POWER NOTE and GM record lists for Story Box cards 0056 (Tiara of Bloody Succession), 0057 (Grudge Ring), 0058 (Olive Branch Lanyard), 0059 (Wheel-Hub Maul), 0060 (Pet Biscuit Crate, same box as 0055), with a diff list for Lore; box stubs point to the new sections; open questions 9 to 13. Card 0055 and §1 to §5 unchanged. |
| 0.2.1 | 2026-10-04 | Recorded Caleb's Story Box approval and the authoritative rules/45 pointer; added the rules/45 §4.5 power note to card 0055 and its prose. |
| 0.2.2 | 2026-10-04 | Applied Caleb's Story Box answers: Story Box items are tradeable, lootable and sellable (not bound), `bound` false and a fixed `sale_value` per rung on cards 0055 to 0060 (0055 and 0060 = 100, 0056 to 0059 = 500 until retuned), `story_value` provenance only; pet-Crawler is a separate player-controlled Crawler with no extra slot (Q3, Q4 resolved); cap Q2 resolved; Grudge Ring deed text follows the fictional-rival, no-PvP rule. Dependency pointers refreshed (core v0.2.8, rules/40 v0.1.5, rules/45 v0.2). Lore's deck files not edited. |
| 0.2.3 | 2026-10-04 | Biscuit rule: one conversion per living pet-Crawler (tombstone dropped, Caleb confirmed); a new conversion needs a new biscuit. |
