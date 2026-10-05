# Core Book Chapter 6 — Magic Item Shortlist v0.1
Owner: DCC Lore | Status: draft | Version: 0.1 | Updated: 2026-10-05
Summary: Book-ready shortlist (30–50) for the human Core Rulebook Items chapter: display name, flavor, tag, rarity/tier, attunement, print-safe mechanics. Companion JSON: `drafts/core-book-magic-items-v0.1.json`.

## How to use
- Mundane gear stays in `tables/item-reskins` (191).
- Floor 1 drawable cards stay in `tables/loot-decks` / campaign loot decks. Rows with a **Deck ref** mean: print a pointer, do not rewrite the card.
- Tags: **SRD** (5e SRD base + `srd_id`), **CANON** (ledger / canon-floor backed), **HOUSE** (table invention or house adaptation).
- Box ceilings: ordinary Silver on Floors 1–2; ordinary Gold on Floors 3–8. Legendary Story Boxes are separate.
- Voice: Crawlers (never champs); saferoom (one word). No novel quotes over 25 words; none used here.

## Counts
- Total: **50**
- By tag: {'CANON': 21, 'HOUSE': 6, 'SRD': 23}
- By rarity: {'Legendary': 3, 'Uncommon': 28, 'Common': 6, 'Rare': 11, 'Very Rare': 2}

## Exclusions (this pass)
- All five `needs_verify` parkeds on `f01-any-orientation-pit` (Animal Friendship; Giant Strength Hill; +1 Shield; Handy Haversack; Portable Hole).
- Wiki-only ledger rows (e.g. I-006, I-022) and anything only in `catalog/items.md` without a ledger id.
- Most Celestial / god-slaying / late unique artifacts (Gate of the Feral Gods, Memorial Crystal, Scavenger's Daughter, Bolt of Ophiotaurus, later patches I-029–I-035) — too spoilery or too late for Core Ch.6 shortlist; leave for a later supplement.
- Mundane PHB deck fillers (rope, rations, caltrops, etc.) — covered by item-reskins + decks.

## Weapon (3)

### Longsword +1, Definitely Not Compensating
- **id:** `cmi-036`
- **tag:** SRD | **srd_id:** `weapon-plus-1`
- **rarity:** Uncommon | **tier:** F1–3 Silver (weapon)
- **attunement:** no
- **flavor:** Sharper, meaner, still a stick with opinions. The plus-one is the only honest thing about it.
- **mechanics:** Magic longsword with +1 to attack and damage rolls. (Deck already has +1 quarterstaff as mop; this is the edged cousin.)

### Javelin of Sudden Weather Report
- **id:** `cmi-037`
- **tag:** SRD | **srd_id:** `javelin-of-lightning`
- **rarity:** Uncommon | **tier:** F3–5 Gold
- **attunement:** no
- **flavor:** Throw once. Become the storm. Then it is a normal javelin again and you are still wet.
- **mechanics:** As an action, throw it: transforms into a 5-foot-wide, 120-foot-long lightning bolt line; each creature in line makes a DC 13 Dex save, 4d6 lightning on fail / half on success. Then the javelin returns to mundane form until next dawn.

### Dagger of Regretful Nightlife
- **id:** `cmi-038`
- **tag:** SRD | **srd_id:** `dagger-of-venom`
- **rarity:** Rare | **tier:** F3–8 Gold
- **attunement:** no
- **flavor:** A polite knife until it is not. Poison optional; consequences mandatory.
- **mechanics:** +1 dagger. Action to coat: next hit before 1 minute ends DC 15 Con save or 2d10 poison damage. Recharges at next dawn.

## Armor (2)

### Enchanted Anarchist's Battle Rattle
- **id:** `cmi-023`
- **tag:** CANON | **canon_ref:** I-002
- **rarity:** Very Rare | **tier:** F6+ Platinum Spicy / patch chassis
- **attunement:** yes
- **flavor:** A sleeveless jacket that collects upgrade patches like bad decisions. Fashion for people who blow things up on purpose.
- **mechanics:** Chest slot. While worn and attuned: +1 to each of Strength, Dexterity, Constitution, Intelligence, and Charisma, and roughly +50% range on thrown explosives. Accepts Upgrade Patches (see I-028 Earth patch and later patch rows when printed). Exact AC uses table armor rules for a light magical jacket.

### Adamantine Breastplate, Dent-Resistant
- **id:** `cmi-035`
- **tag:** SRD | **srd_id:** `adamantine-armor`
- **rarity:** Uncommon | **tier:** F3–8 Gold
- **attunement:** no
- **flavor:** Metal that refuses critical hits like a bad review. Heavy. Smug.
- **mechanics:** Any medium or heavy adamantine armor: critical hits against you become normal hits. This entry assumes breastplate form; AC as breastplate.

## Jewelry (8)

### Grudge Ring (Green Glass, Red Stone)
- **id:** `cmi-002`
- **tag:** HOUSE | **canon_ref:** I-025 (inspired; house adaptation)
- **deck_ref:** `f01-any-0057`
- **rarity:** Uncommon | **tier:** F1–2 Legendary Story Box (That's the Spirit!)
- **attunement:** yes
- **flavor:** Pretty little promise that someone, somewhere, is going to have a worse day than you. Wear it like a threat you can afford.
- **mechanics:** See loot card f01-any-0057. House adaptation of the Night Wyrm ring fantasy (I-025); printed table text is the card, not the novel.
- **notes:** Canon ring is I-025; this is the Floor 1 playable stand-in.

### Tiara of Bloody Succession
- **id:** `cmi-003`
- **tag:** HOUSE | **canon_ref:** I-014 (inspired; house adaptation)
- **deck_ref:** `f01-any-0056`
- **rarity:** Uncommon | **tier:** F1–2 Legendary Story Box (Quadruped)
- **attunement:** yes
- **flavor:** Fits heads. Fits paws. Fits egos. The crown does not care which hole you call a face.
- **mechanics:** See loot card f01-any-0056. House quadruped crown inspired by I-014; use card mechanics at the table.

### Enchanted Toe Ring of the Leprous Bandit
- **id:** `cmi-011`
- **tag:** CANON | **canon_ref:** I-021
- **rarity:** Rare | **tier:** F3–5 Gold achievement / specialty boxes
- **attunement:** yes
- **flavor:** Yes, a toe ring. Yes, it is sticky. Yes, you will explain this at the table and nobody will respect you for it.
- **mechanics:** While attuned: gain a Sticky Feet benefit (advantage on checks to keep footing / resist being moved) and a Super Spreader benefit (when you inflict a contagion-style condition the GM tracks, it is easier to pass on—exact disease list is table-ruled). Unique-flavored jewelry.

### Enchanted Crown of the Sepsis Whore
- **id:** `cmi-025`
- **tag:** CANON | **canon_ref:** I-014
- **rarity:** Legendary | **tier:** F1 Legendary Quadruped Box (canon); later reprints rare
- **attunement:** yes
- **flavor:** Who's a dirty girl? The crown already answered. Intelligence up, first impressions weird, infections optional.
- **mechanics:** Head slot. While attuned: +5 Intelligence; +5 to Good First Impression (treat as a social skill bonus); attacks have a chance to inflict a Sepsis-style lingering damage condition (GM table). Legendary one-off fantasy; Floor 1 house tiara card is a milder adaptation (cmi-003).

### Ring of Not Dying as Often
- **id:** `cmi-027`
- **tag:** SRD | **srd_id:** `ring-of-protection`
- **rarity:** Rare | **tier:** F3–8 Gold
- **attunement:** yes
- **flavor:** A plain band that quietly hates incoming dice. Attune it or enjoy being meat.
- **mechanics:** Requires attunement. +1 bonus to AC and saving throws while worn.

### Ring of Vertical Ambition
- **id:** `cmi-028`
- **tag:** SRD | **srd_id:** `ring-of-jumping`
- **rarity:** Uncommon | **tier:** F1–3 Silver
- **attunement:** yes
- **flavor:** Jump farther. Stick landings less often. Physics is optional; ankles are not.
- **mechanics:** Attunement. Jump distance is tripled; still needs a running start when the jump rules say so.

### Brooch of Force-Field Gossip
- **id:** `cmi-031`
- **tag:** SRD | **srd_id:** `brooch-of-shielding`
- **rarity:** Uncommon | **tier:** F1–3 Silver
- **attunement:** yes
- **flavor:** Jewelry that hates Magic Missile personally. Fashionable spite.
- **mechanics:** Attunement. Resistance to force damage; immunity to the Magic Missile spell.

### Periapt of Stubborn Circulatory System
- **id:** `cmi-032`
- **tag:** SRD | **srd_id:** `periapt-of-wound-closure`
- **rarity:** Uncommon | **tier:** F1–3 Silver
- **attunement:** yes
- **flavor:** A pendant that bullies your blood into clotting. Stabilizes losers. Doubles hit-dice drama overnight.
- **mechanics:** Attunement. Automatically stabilize at 0 HP. Whenever you roll Hit Dice to regain HP, double the total.

## Tattoo (2)

### Goblin Pass Tattoo
- **id:** `cmi-012`
- **tag:** CANON | **canon_ref:** I-024; L-018
- **rarity:** Uncommon | **tier:** F1 Silver Goblin Box
- **attunement:** no
- **flavor:** Permanent ink that says you are union-adjacent to the worst roommates in the dungeon. Job interviews are over.
- **mechanics:** Removes automatic goblin hostility and grants free passage through goblin-controlled areas that recognize the mark. Does not stop goblins who already hate you personally.

### Desperado Pass Tattoo
- **id:** `cmi-013`
- **tag:** CANON | **canon_ref:** I-023; L-019
- **rarity:** Uncommon | **tier:** F1+ Asshole's Box (often first)
- **attunement:** no
- **flavor:** Back-of-the-bus club stamp. The nice clubs will smell it on you.
- **mechanics:** Grants Desperado Club access when that venue is in play. If the Crawler already holds another club affiliation, the GM may skip or replace this drop (L-019).

## Wondrous (13)

### Duffel Bag, Roomier Inside
- **id:** `cmi-004`
- **tag:** SRD | **srd_id:** `bag-of-holding`
- **deck_ref:** `f01-any-0052`
- **rarity:** Uncommon | **tier:** F1–2 Silver (loot deck)
- **attunement:** no
- **flavor:** A bag that lies about volume and tells the truth about your life choices. Do not put a bag inside a bag unless you enjoy becoming a cautionary tale.
- **mechanics:** See loot card f01-any-0052. SRD Bag of Holding: extradimensional storage with the usual catastrophic nesting rules.

### Eternally Stained Wifebeater / Wardrobe Hoodie
- **id:** `cmi-005`
- **tag:** HOUSE
- **deck_ref:** `f01-any-0028 (also f01-z09-0015)`
- **rarity:** Common | **tier:** F1–2 Bronze–Silver
- **attunement:** no
- **flavor:** One shirt, infinite outfit crimes. The System finally found a use for laundry day.
- **mechanics:** See loot card f01-any-0028 (Cloak of Many Fashions house item; final text in rules/42 §2).

### Pet Carrier (Inventory Kennel)
- **id:** `cmi-009`
- **tag:** CANON | **canon_ref:** I-012
- **rarity:** Uncommon | **tier:** F1–2 shop / Silver; buyable early
- **attunement:** no
- **flavor:** A pokéball with worse customer support. Your bonded pet goes in. Your dignity does not come out.
- **mechanics:** Lets a bonded pet-class creature ride in inventory safely. Ordinary healing potions still do not work on pets (see Heal Critter).

### Earth Upgrade Patch
- **id:** `cmi-024`
- **tag:** CANON | **canon_ref:** I-028
- **rarity:** Rare | **tier:** F5 Platinum Spicy (sample); Gold+ patch boxes
- **attunement:** no
- **flavor:** Iron-on propaganda for your jacket. Smells like home-world cope.
- **mechanics:** Small patch. While sewn onto a valid patch chassis: +5% Strength and immunity to cloud-based attacks. Sewing may require a tool check.

### Dungeon Anarchist's Cookbook
- **id:** `cmi-026`
- **tag:** CANON | **canon_ref:** I-001; L-022
- **rarity:** Legendary | **tier:** F4+ Prize Carousel / Fan Box path (unique)
- **attunement:** no
- **flavor:** Chicken recipes, goblin recipes, and enough bad ideas to end a season. Unique. Sticky. Do not lend it out.
- **mechanics:** Unique book. Expands Scratchpad by +1 page and functions as a long-running quest/recipe macguffin. Not a random Silver pull.

### Boots of Getting There Faster Than Your Friends
- **id:** `cmi-029`
- **tag:** SRD | **srd_id:** `boots-of-striding-and-springing`
- **rarity:** Uncommon | **tier:** F1–3 Silver
- **attunement:** yes
- **flavor:** Walking shoes for cowards who refuse to die tired. Springing included. Dignity sold separately.
- **mechanics:** Attunement. Walking speed becomes 30 feet if lower; jump distance tripled; hard landings from jumps are softened per SRD.

### Cloak of Please Stop Looking at Me
- **id:** `cmi-030`
- **tag:** SRD | **srd_id:** `cloak-of-elvenkind`
- **rarity:** Uncommon | **tier:** F1–3 Silver
- **attunement:** yes
- **flavor:** Camouflage for people who peaked at hide-and-seek. The hood judges your posture.
- **mechanics:** Attunement. Advantage on Dexterity (Stealth) checks; you can attempt to hide when only lightly obscured by foliage, heavy rain, falling snow, mist, and other natural phenomena.

### Gauntlets of Borrowed Ogre Energy
- **id:** `cmi-033`
- **tag:** SRD | **srd_id:** `gauntlets-of-ogre-power`
- **rarity:** Uncommon | **tier:** F3–5 Gold
- **attunement:** yes
- **flavor:** Hands that insist you are stronger than your character sheet. Gym optional.
- **mechanics:** Attunement. Your Strength score is 19 while worn (no effect if already 19+).

### Headband of Unearned Homework
- **id:** `cmi-034`
- **tag:** SRD | **srd_id:** `headband-of-intellect`
- **rarity:** Uncommon | **tier:** F3–5 Gold
- **attunement:** yes
- **flavor:** A sweatband that does your thinking. Personality optional. Trivia night ruined.
- **mechanics:** Attunement. Your Intelligence score is 19 while worn (no effect if already 19+).

### Decanter of Infinite Hydration Litigation
- **id:** `cmi-045`
- **tag:** SRD | **srd_id:** `decanter-of-endless-water`
- **rarity:** Uncommon | **tier:** F1–3 Silver
- **attunement:** no
- **flavor:** Say the command words. Get a trickle, a fountain, or a geyser. Flood a saferoom and enjoy the review.
- **mechanics:** Produces fresh or salt water on command: stream, fountain, or geyser rates per SRD. Geyser can shove creatures.

### Cap of Soft Drowning Avoidance
- **id:** `cmi-047`
- **tag:** SRD | **srd_id:** `cap-of-water-breathing`
- **rarity:** Uncommon | **tier:** F3–5 Gold (water floors / Knotline)
- **attunement:** no
- **flavor:** A hat that lets you breathe underwater. Style remains a personal failure.
- **mechanics:** While worn, you can breathe underwater.

### Stone of Statistically Suspicious Luck
- **id:** `cmi-048`
- **tag:** SRD | **srd_id:** `stone-of-good-luck`
- **rarity:** Uncommon | **tier:** F3–8 Gold
- **attunement:** yes
- **flavor:** A luckstone that makes failure look optional. Attune it and watch the dice unionize.
- **mechanics:** Attunement. +1 to ability checks and saving throws while carried.

### Orientation Lanyard of Mild Authority
- **id:** `cmi-049`
- **tag:** HOUSE
- **rarity:** Common | **tier:** F1 Bronze–Silver (Orientation Pit)
- **attunement:** no
- **flavor:** Clip-on power. Opens nothing important. Makes NPCs briefly assume you work here, which is worse.
- **mechanics:** Once per day, advantage on one Charisma check against Orientation Pit staff/usher-type NPCs. No door-opening magic; pure social scam.

## Wand (1)

### Wand of Hostile Interior Decorating
- **id:** `cmi-043`
- **tag:** SRD | **srd_id:** `wand-of-web`
- **rarity:** Rare | **tier:** F3–8 Gold
- **attunement:** yes
- **flavor:** Seven charges of sticky architecture. Web the hallway. Web your problems. Web your friends by accident.
- **mechanics:** Attunement. 7 charges; cast web (save DC 15) for 1 charge. Regains 1d6+1 at dawn; on a 1 for daily regain, the wand is destroyed after the last charge is spent (SRD).

## Scroll (1)

### Spell Scroll, Emergency Exit (Misty Step)
- **id:** `cmi-044`
- **tag:** SRD | **srd_id:** `spell-scroll-misty-step`
- **rarity:** Uncommon | **tier:** F1–3 Silver
- **attunement:** no
- **flavor:** A single-use teleport for cowards with good timing. Paperwork vanishes with you.
- **mechanics:** Spell scroll of misty step (2nd-level). Only casters who have the spell on their list can use it; then the scroll is destroyed.

## Potion (12)

### Standard Healing Potion (Dungeon Formula)
- **id:** `cmi-007`
- **tag:** CANON | **canon_ref:** I-009
- **rarity:** Common | **tier:** F1+ Adventurer / tutorial boxes; saferoom stock
- **attunement:** no
- **flavor:** Not the polite red vial from tabletop night. This one negotiates with your hit points like a collections agent.
- **mechanics:** On drink, restore at least half your maximum hit points (dungeon formula). Distinct from the SRD Potion of Healing skins in the Floor 1 decks (those use SRD dice). Prefer this entry when printing DCC-native healing.

### Cheat Code Potion
- **id:** `cmi-008`
- **tag:** CANON | **canon_ref:** I-011
- **rarity:** Uncommon | **tier:** F1–3 Silver loot boxes (short shelf life)
- **attunement:** no
- **flavor:** Tastes like someone left a debug menu open. Drink before it remembers it has a shelf life.
- **mechanics:** Grants +3 levels to one random skill. Perishable: GM may spoil unused doses after a short clock (canon warns of short shelf life).

### Heal Critter Potion
- **id:** `cmi-014`
- **tag:** CANON | **canon_ref:** M-090; K-121; K-109
- **rarity:** Uncommon | **tier:** F2+ craft / Silver; field recipe
- **attunement:** no
- **flavor:** Because the System decided pets do not deserve normal medicine. Brew it ugly. Make the pet drink it.
- **mechanics:** Heals pet-class creatures. Standard healing potions and heal scrolls do nothing for pets. Field recipe (paraphrase): spike a Healing Potion with cinnamon, wait briefly, add Thistle Rot, shake until brown; the pet must consume it.

### Rev-Up Toilet-Grade Moonshine
- **id:** `cmi-016`
- **tag:** CANON | **canon_ref:** K-094
- **rarity:** Uncommon | **tier:** F2 Rev-Up / clurichaun drops
- **attunement:** no
- **flavor:** Accelerant first, beverage second, life coach never. The label is lying about every word except "toilet."
- **mechanics:** Volatile potion/accelerant. On drink: high chance of a permanent +2 to a random ability score, small chance of instant death, and other nasty side effects the GM rolls from the Rev-Up table. Also a crafting reagent for Floor 2 recipes.

### Rev-Up Immunity Smoothie
- **id:** `cmi-017`
- **tag:** CANON | **canon_ref:** K-123; K-124; M-455
- **rarity:** Uncommon | **tier:** F2 craft (Krakaren distillery)
- **attunement:** no
- **flavor:** Blended corpse cocktail with a buzz chaser. Prevents the floor's favorite diseases. Does not fix your taste.
- **mechanics:** While the temporary immunity lasts: ignore Taint and Vigorous Measles (prevention, not cure of an already-active case per M-455). Inflicts a Buzzed debuff. Brewed at the Floor 2 blender station from moonshine plus a Laminak Elite corpse (see K-123).

### Mordecai's Special Brew
- **id:** `cmi-019`
- **tag:** CANON | **canon_ref:** I-018
- **rarity:** Rare | **tier:** F4+ Alchemy Table (guide craft)
- **attunement:** no
- **flavor:** Thirty seconds of "no." Then the bill comes due. Drink only when dying would be embarrassing on camera.
- **mechanics:** For 30 seconds after drinking, the Crawler cannot be killed (treat as immortality/ignore HP 0 for the duration). When it ends, normal death rules resume immediately.

### Level-Up Potion
- **id:** `cmi-020`
- **tag:** CANON | **canon_ref:** I-010
- **rarity:** Rare | **tier:** F4–8 quest rewards (not common shop)
- **attunement:** no
- **flavor:** Bottled homework credit. The System hates giving these out almost as much as you love drinking them.
- **mechanics:** Grants +1 character level when drunk. Quest-gated; do not stock on Floor 1–2 random Silver.

### Cosmic Buff Potion
- **id:** `cmi-021`
- **tag:** CANON | **canon_ref:** I-008; L-014
- **rarity:** Rare | **tier:** F6+ Platinum "Good Shit" / similar
- **attunement:** no
- **flavor:** Pink, frothy, and personally invasive. One stat gets a vacation. The others get jealous.
- **mechanics:** Immediately increase one random ability score by +10 (permanent unless the table rules otherwise). Late-floor Platinum specialty.

### Potion of Selective Existence
- **id:** `cmi-039`
- **tag:** SRD | **srd_id:** `potion-of-invisibility`
- **rarity:** Very Rare | **tier:** F3–8 Gold (rare pull)
- **attunement:** no
- **flavor:** Disappear. Immediately do something loud. Become a parable.
- **mechanics:** Invisible for 1 hour (SRD). Ends early if you attack or cast a spell.

### Potion of Embarrassing Enlargement
- **id:** `cmi-040`
- **tag:** SRD | **srd_id:** `potion-of-growth`
- **rarity:** Uncommon | **tier:** F1–3 Silver
- **attunement:** no
- **flavor:** Enlarge for the bit. Doorways will remember you.
- **mechanics:** Gain the Enlarge effect of enlarge/reduce for 1d4 hours (SRD potion).

### Potion of Temporary Main-Character Energy
- **id:** `cmi-041`
- **tag:** SRD | **srd_id:** `potion-of-heroism`
- **rarity:** Rare | **tier:** F3–8 Gold
- **attunement:** no
- **flavor:** Blessings and temporary hit points in a bottle. Side effects include hubris.
- **mechanics:** Gain 10 temporary HP that last for 1 hour. For the same hour, you are under the bless spell (SRD).

### Elixir of Get Your Life Together
- **id:** `cmi-042`
- **tag:** SRD | **srd_id:** `elixir-of-health`
- **rarity:** Rare | **tier:** F3–8 Gold
- **attunement:** no
- **flavor:** Cures the debuff buffet. Does not cure your decision-making.
- **mechanics:** Cures any disease and removes blinded, deafened, paralyzed, and poisoned conditions (SRD).

## Consumable (8)

### Enhanced Pet Biscuit
- **id:** `cmi-001`
- **tag:** CANON | **canon_ref:** I-007; M-037; M-235; L-020
- **deck_ref:** `f01-any-0055`
- **rarity:** Legendary | **tier:** F1–2 Legendary Story / Pet Box (Silver–Legendary special)
- **attunement:** no
- **flavor:** It looks like a treat. It is a career change with teeth. Feed it only where the System cannot make the punchline worse.
- **mechanics:** See loot card f01-any-0055 and rules/42-house-items-f01.md §6 for table mechanics. Canon: Legendary Pet Box consumable that forces a major random pet outcome (100+ possibilities). Prefer a saferoom.
- **notes:** Do not reprint full rules; point to the card.

### Pocket Dragon Breath Mints
- **id:** `cmi-006`
- **tag:** HOUSE
- **deck_ref:** `f01-any-0041`
- **rarity:** Uncommon | **tier:** F1–2 Silver
- **attunement:** no
- **flavor:** Minty. Regretful. Briefly dragon-adjacent. Exhale problems at people who deserve them.
- **mechanics:** See loot card f01-any-0041 and rules/42 §5 (Potion of Fire Breath house item).

### Goblin Dynamite
- **id:** `cmi-010`
- **tag:** CANON | **canon_ref:** I-013; L-018; canon-floor-1 goblin explosives
- **rarity:** Common | **tier:** F1 Goblin / explosives boxes; Bomb Bard drops
- **attunement:** no
- **flavor:** Lit fuse, bad manners, excellent peer pressure. The clan brought enough for everyone, including you.
- **mechanics:** Thrown explosive. Use alchemist's fire / goblin-bomb table rules from the house Floor 1 budget (or 5e thrown bomb guidelines). Inert inside saferooms (floor rule).

### Pet Biscuit (Plain)
- **id:** `cmi-015`
- **tag:** CANON | **canon_ref:** M-228; M-410
- **deck_ref:** `f01-any-0060 (bulk crate card)`
- **rarity:** Common | **tier:** F1 Pet Box (bulk); F2 pound puzzle
- **attunement:** no
- **flavor:** Dog treat diplomacy. Works until it doesn't. Bulk crates exist for people who collect problems.
- **mechanics:** Feed to a qualifying beast/pet to shift hostility toward neutral in the Floor 2 pound scenario (map dot red→white). Bulk supply appears in Legendary Pet Box samples (500) and card f01-any-0060.

### Jug O'Boom (Craft Pattern)
- **id:** `cmi-018`
- **tag:** CANON | **canon_ref:** K-125
- **rarity:** Uncommon | **tier:** F2+ craft (explosives skill)
- **attunement:** no
- **flavor:** Moonshine jug, goblin oil, torch cork, and a prayer you do not owe anyone. Incendiary handling optional, survival mandatory.
- **mechanics:** Crafted incendiary jug. Burns in a splash radius for a duration based on the thrower's Incendiary Device Handling skill (about 15 seconds per skill level). Use thrown-bomb attack rolls; saferoom-inert.

### Surefire (Guided Projectile Kit)
- **id:** `cmi-022`
- **tag:** CANON | **canon_ref:** I-019
- **rarity:** Rare | **tier:** F5 Sniper's Box / Gold
- **attunement:** no
- **flavor:** Makes your bolt believe in itself. Physics files a complaint.
- **mechanics:** Applied to a projectile: that shot gains the Guided property (ignore ordinary cover/soft miss chances; still requires a legal target and attack roll). One application per kit use.

### Dust of Dramatic Exit
- **id:** `cmi-046`
- **tag:** SRD | **srd_id:** `dust-of-disappearance`
- **rarity:** Uncommon | **tier:** F1–3 Silver
- **attunement:** no
- **flavor:** Throw powder. Vanish with your closest mistakes. Duration varies because the System likes roulette.
- **mechanics:** Toss to coat yourself and nearby creatures: invisible for 2d4 minutes. Attacking or casting ends it early for that creature (SRD).

### Vending Blessing Chip (Single Pull)
- **id:** `cmi-050`
- **tag:** HOUSE
- **rarity:** Common | **tier:** F1 Gore Arcade / vending
- **attunement:** no
- **flavor:** A token that smells like hot coils. Redeem for one free Bronze-tier wall pull. The machine still hates you.
- **mechanics:** Consume to draw once from the local Bronze loot table without spending credits. Nontransferable once slotted.

