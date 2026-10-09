# Monster book (Floors 1–3)
Owner: Cursor (R&D) | Status: draft | Version: 0.3.0 | Updated: 2026-10-09
Summary: 72 house reskins of SRD 5.2.1 stat blocks for random encounters. Numbers are the open SRD. Flavor is house. Limited spells and recharge tricks have counters. Not a live floor.

Live Day pages and `rules/70-encounter-budget-5e.json` win on any fight that is already filed. This book is a draw pile for grok bots. Lore and Encounter Bot own stories later.

Names are pictures. A Crawler should know what they are looking at without a Monster Manual. The SRD name stays in the table for the math.

Nameplate level is CR rounded up, minimum 1 (core §8.4). A boss card says Boss. XP is `xp_by_cr` in rules/70, checked against the SRD line.

A leveled spell or a 1/Day trick spends a counter. At-will cantrips do not. When the counter hits 0, that spell is done until a Long Rest in a saferoom. A recharge trick stays down until the d6 hits. Do not give a boss an endless 2nd-level slot.

## Counts

| Floor | Mobs | Units | Elites | Bosses |
|---:|---:|---:|---:|---:|
| 1 | 12 | 6 | 4 | 2 |
| 2 | 10 | 6 | 5 | 3 |
| 3 | 10 | 6 | 5 | 3 |

## Index

| ID | Floor | Role | Name | SRD | CR | XP |
|---|---:|---|---|---|---:|---:|
| `f01-m-01` | 1 | mob | Ankle-Biting Vent Rat | Giant Rat | 1/8 | 25 |
| `f01-m-02` | 1 | mob | Latch-On Ceiling Mosquito | Stirge | 1/8 | 25 |
| `f01-m-03` | 1 | mob | Probation Goblin, Plastic Badge | Goblin Minion | 1/8 | 25 |
| `f01-m-04` | 1 | mob | Hoodie Pamphleteer | Cultist | 1/8 | 25 |
| `f01-m-05` | 1 | mob | Suitcase Lobby Crab | Giant Crab | 1/8 | 25 |
| `f01-m-06` | 1 | mob | Foam-Head Mascot Dog | Mastiff | 1/8 | 25 |
| `f01-m-07` | 1 | mob | Name-Tag Thief | Bandit | 1/8 | 25 |
| `f01-m-08` | 1 | mob | Flashlight Turnstile Guard | Guard | 1/8 | 25 |
| `f01-m-09` | 1 | mob | Smiling Polo Mannequin | Skeleton | 1/4 | 50 |
| `f01-m-10` | 1 | mob | Pineapple-Club Goblin | Goblin Warrior | 1/4 | 50 |
| `f01-m-11` | 1 | mob | Mop-Dragging Janitor Zombie | Zombie | 1/4 | 50 |
| `f01-m-12` | 1 | mob | Screaming PA Mushroom | Shrieker Fungus | 0 | 0 |
| `f01-u-01` | 1 | unit | Safety-Vest Pike Intern | Warrior Infantry | 1/8 | 25 |
| `f01-u-02` | 1 | unit | Flying Razor Lanyard | Animated Flying Sword | 1/4 | 50 |
| `f01-u-03` | 1 | unit | Paper-Hat Snack Dog | Kobold Warrior | 1/8 | 25 |
| `f01-u-04` | 1 | unit | Nacho-Cheese Steam Cloud | Steam Mephit | 1/4 | 50 |
| `f01-u-05` | 1 | unit | Hold-Music Choir Intern | Priest Acolyte | 1/4 | 50 |
| `f01-u-06` | 1 | unit | Mop-Length Hall Centipede | Giant Centipede | 1/4 | 50 |
| `f01-e-01` | 1 | elite | Walking Empty Pit-Bull Suit | Animated Armor | 1 | 200 |
| `f01-e-02` | 1 | elite | Seven-Foot Hairy Break-Room Bully | Bugbear Warrior | 1 | 200 |
| `f01-e-03` | 1 | elite | Craft-Services Corpse | Ghoul | 1 | 200 |
| `f01-e-04` | 1 | elite | Janitor-Vest Night Ghost | Specter | 1 | 200 |
| `f01-b-01` | 1 | boss | Golf-Cart Concession Spider | Giant Spider | 1 | 200 |
| `f01-b-02` | 1 | boss | Adjunct Smash, Podium Giant | Ogre | 2 | 450 |
| `f02-m-01` | 2 | mob | Sash-Wearing Tall Goblin Sergeant | Hobgoblin Warrior | 1/2 | 100 |
| `f02-m-02` | 2 | mob | Boot-Eating Mop Water | Gray Ooze | 1/2 | 100 |
| `f02-m-03` | 2 | mob | Route-Knowing Clipboard Scout | Scout | 1/2 | 100 |
| `f02-m-04` | 2 | mob | Laughing Hyena Person | Gnoll Warrior | 1/2 | 100 |
| `f02-m-05` | 2 | mob | Couch-Sized Saddle Wolf | Worg | 1/2 | 100 |
| `f02-m-06` | 2 | mob | Sword-Eating Antenna Bug | Rust Monster | 1/2 | 100 |
| `f02-m-07` | 2 | mob | Your Shadow, On Payroll | Shadow | 1/2 | 100 |
| `f02-m-08` | 2 | mob | Goat-Legged Warmup Comic | Satyr | 1/2 | 100 |
| `f02-m-09` | 2 | mob | Walking Charcoal Briquette | Magmin | 1/2 | 100 |
| `f02-m-10` | 2 | mob | Coughing Dust Cloud | Dust Mephit | 1/2 | 100 |
| `f02-u-01` | 2 | unit | Trident Lifeguard Fish-Person | Sahuagin Warrior | 1/2 | 100 |
| `f02-u-02` | 2 | unit | Petrifying Chicken-Lizard | Cockatrice | 1/2 | 100 |
| `f02-u-03` | 2 | unit | Motorcycle-Sized Usher Wasp | Giant Wasp | 1/2 | 100 |
| `f02-u-04` | 2 | unit | Bouncer Ape Named Grip | Ape | 1/2 | 100 |
| `f02-u-05` | 2 | unit | Bow-Tie Black Bear | Black Bear | 1/2 | 100 |
| `f02-u-06` | 2 | unit | Decorative Tank Shark | Reef Shark | 1/2 | 100 |
| `f02-e-01` | 2 | elite | Headset Shoulder Devil | Imp | 1 | 200 |
| `f02-e-02` | 2 | elite | Golf-Cart Security Wolf | Dire Wolf | 1 | 200 |
| `f02-e-03` | 2 | elite | Marquee Bird-Woman | Harpy | 1 | 200 |
| `f02-e-04` | 2 | elite | Swooping Stone Security Camera | Gargoyle | 2 | 450 |
| `f02-e-05` | 2 | elite | Ten-Foot Cube of Floor Cleaner | Gelatinous Cube | 2 | 450 |
| `f02-b-01` | 2 | boss | Fire-Breathing Exit Dog | Hell Hound | 3 | 700 |
| `f02-b-02` | 2 | boss | Occupied Owl-Bear Mascot | Owlbear | 3 | 700 |
| `f02-b-03` | 2 | boss | Rental-Plate Sponsor Knight | Knight | 3 | 700 |
| `f03-m-01` | 3 | mob | Eyeless Cave Person | Grimlock | 1/4 | 50 |
| `f03-m-02` | 3 | mob | Stinking Demon Intern | Dretch | 1/4 | 50 |
| `f03-m-03` | 3 | mob | Fence-Hopping Teleport Dog | Blink Dog | 1/4 | 50 |
| `f03-m-04` | 3 | mob | Cat-Sized Shoulder Dragon | Pseudodragon | 1/4 | 50 |
| `f03-m-05` | 3 | mob | Purple Whip-Crop Fungus | Violet Fungus | 1/4 | 50 |
| `f03-m-06` | 3 | mob | Hatchet-Faced Ostrich | Axe Beak | 1/4 | 50 |
| `f03-m-07` | 3 | mob | Hang-Glider Mail Lizard | Pteranodon | 1/4 | 50 |
| `f03-m-08` | 3 | mob | Two-Headed Junkyard Dog | Two-Headed Junkyard Dog | 1 | 200 |
| `f03-m-09` | 3 | mob | Invisible Clipboard Gremlin | Quasit | 1 | 200 |
| `f03-m-10` | 3 | mob | Property-Line Tree Woman | Dryad | 1 | 200 |
| `f03-u-01` | 3 | unit | Cutlass Pirate Who Drafts You | Pirate | 1 | 200 |
| `f03-u-02` | 3 | unit | Pony-Sized Laughing Hyena | Giant Hyena | 1 | 200 |
| `f03-u-03` | 3 | unit | Lawn Lion | Lion | 1 | 200 |
| `f03-u-04` | 3 | unit | Patch-Wearing Brown Bear | Brown Bear | 1 | 200 |
| `f03-u-05` | 3 | unit | Horse-Bodied Eagle Courier | Hippogriff | 1 | 200 |
| `f03-u-06` | 3 | unit | Swallow-You Mill Toad | Giant Toad | 1 | 200 |
| `f03-e-01` | 3 | elite | Tunneling Acid Ant-Lion | Ankheg | 2 | 450 |
| `f03-e-02` | 3 | elite | Barn-Rafter Spider Person | Ettercap | 2 | 450 |
| `f03-e-03` | 3 | elite | Roadside Priest, Mace Blessed | Priest | 2 | 450 |
| `f03-e-04` | 3 | elite | Blink-Past-the-Gate Spider | Phase Spider | 3 | 700 |
| `f03-e-05` | 3 | elite | Lion-Bat with a Spike Tail | Manticore | 3 | 700 |
| `f03-b-01` | 3 | boss | Two-Headed Toll Giant | Ettin | 4 | 1100 |
| `f03-b-02` | 3 | boss | Grant-Denied Ghost | Ghost | 4 | 1100 |
| `f03-b-03` | 3 | boss | Hungry Black Silo Slime | Black Pudding | 4 | 1100 |

# Floor 1 — Orientation Pit

Orientation Pit, five-day clock (decision 026). Nameplate level is flavor; the math is CR. The Break Room is the saferoom through Day 3 and loses service on Day 4. The Green Room stays open and is the level-2 milestone. Boxes open in a saferoom. A Long Rest finishes in a saferoom. Credits, not coins. Dean Thudd on the Day pages is the live Floor 1 boss. These cards do not replace him. A neighborhood boss stopping its own adds is canon staging, not a rule this card enforces. Book-proper mob names stay out of this pack.

## Ankle-Biting Vent Rat

`f01-m-01` · mob · Ankle-Biting Vent Rat. Level 1. "Union member of the vents."

**Picture.** A cat-sized rat in the ductwork, going for ankles, and it brought friends.

**Engine.** Bite, melee, +5, reach 5 ft, 1d4+3 piercing

| | |
|---|---|
| SRD block | Giant Rat |
| Type | Small Beast, Unaligned |
| AC | 13 |
| Initiative | +3 |
| HP | 7 (2d6) |
| Speed | 30 ft., Climb 30 ft. |
| Abilities | STR 7 (-2), DEX 16 (+3), CON 11 (+0), INT 2 (-4), WIS 10 (+0), CHA 4 (-3) |
| CR | 1/8 |
| XP | 25 |
| PB | +2 |
| Skills | Perception +2 |
| Senses | Darkvision 60 ft.; Passive Perception 12 |
| Languages | None |

**Wants.** It wants the crumbs and the ankles.

**Cheese.** Hold a doorway. Pack Tactics dies if they cannot stand together.

**Tactics.** Swarm the nearest ankles. They do not open doors.

**Reskin.** Bite stays piercing. The ducts are set dressing.

**House check.** Vent Row rats on the floor page carry nothing. Do not hang credits on this corpse. Pack Tactics is the combat lesson.

**[SYSTEM]** Ankle-Biting Vent Rat. Level 1. Hostile.

**[GM]** Something in the vent just filed a grievance with your ankle.

### Traits

- **Pack Tactics.** The rat has Advantage on an attack roll against a creature if at least one of the rat’s allies is within 5 feet of the creature and the ally doesn’t have the Incapacitated condition

### Attacks

- **Bite.** Melee Attack Roll: +5, reach 5 feet. Hit: 5 (1d4 + 3) Piercing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Latch-On Ceiling Mosquito

`f01-m-02` · mob · Latch-On Ceiling Mosquito. Level 1. "It clocks in through your neck."

**Picture.** A fist-sized mosquito with a drinking-straw nose. It drops off the ceiling, sticks to you, and sips.

**Engine.** Proboscis, melee, +5, reach 5 ft, 1d6+3 piercing

| | |
|---|---|
| SRD block | Stirge |
| Type | Tiny Monstrosity, Unaligned |
| AC | 13 |
| Initiative | +3 |
| HP | 5 (2d4) |
| Speed | 10 ft., Fly 40 ft. |
| Abilities | STR 4 (-3), DEX 16 (+3), CON 11 (+0), INT 2 (-4), WIS 8 (-1), CHA 6 (-2) |
| CR | 1/8 |
| XP | 25 |
| PB | +2 |
| Senses | Darkvision 60 ft.; Passive Perception 9 |
| Languages | None |

**Wants.** It wants blood and then a nap.

**Cheese.** Pull it off. Do not let a second one sit while you peel the first.

**Tactics.** Attach, then stop attacking and drink.

**Reskin.** Blood Drain is unchanged. Call the needle a badge clip.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Latch-On Ceiling Mosquito. Level 1. Attaches.

**[GM]** Congratulations. You are the open bar.

### Attacks

- **Proboscis.** Melee Attack Roll: +5, reach 5 ft. Hit: 6 (1d6 + 3) Piercing damage, and the stirge attaches to the target. While attached, the stirge can’t make Proboscis attacks, and the target takes 5 (2d4) Necrotic damage at the start of each of the stirge’s turns. The stirge can detach itself by spending 5 feet of its movement. The target or a creature within 5 feet of it can detach the stirge as an action

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Probation Goblin, Plastic Badge

`f01-m-03` · mob · Probation Goblin, Plastic Badge. Level 1. "Still on probation."

**Picture.** A small green intern. The badge is real. The job is to get hit first.

**Engine.** Dagger, 1d4+2 piercing; Nimble Escape

| | |
|---|---|
| SRD block | Goblin Minion |
| Type | Small Fey (Goblinoid), Chaotic Neutral |
| AC | 12 |
| Initiative | +2 |
| HP | 7 (2d6) |
| Speed | 30 ft. |
| Abilities | STR 8 (-1), DEX 15 (+2), CON 10 (+0), INT 10 (+0), WIS 8 (-1), CHA 8 (-1) |
| CR | 1/8 |
| XP | 25 |
| PB | +2 |
| Skills | Stealth +6 |
| Gear | Daggers (3) |
| Senses | Darkvision 60 ft.; Passive Perception 9 |
| Languages | Common, Goblin |

**Wants.** It wants a veteran to notice it.

**Cheese.** They fold if the veteran drops. Focus the one giving orders.

**Tactics.** Dagger, then Disengage. They screen for the real staff.

**Reskin.** None. Same dagger.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Probation Goblin, Plastic Badge. Level 1. Probationary.

**[GM]** Kill the intern and the show still finds another intern.

### Attacks

- **Dagger.** Melee or Ranged Attack Roll: +4, reach 5 ft. or range 20/60 ft. Hit: 4 (1d4 + 2) Piercing damage

### Bonus actions

- **Nimble Escape.** The goblin takes the Disengage or Hide action

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Hoodie Pamphleteer

`f01-m-04` · mob · Hoodie Pamphleteer. Level 1. "Faith, but the pamphlet is the weapon."

**Picture.** A person in a hoodie pressing a pamphlet into your chest. The pamphlet is not the weapon. The knife is.

**Engine.** Ritual Sickle, melee, +3, reach 5 ft, 1d4+1 slashing

| | |
|---|---|
| SRD block | Cultist |
| Type | Medium or Small Humanoid, Neutral |
| AC | 12 |
| Initiative | +1 |
| HP | 9 (2d8) |
| Speed | 30 ft. |
| Abilities | STR 11 (+0), DEX 12 (+1), CON 10 (+0), INT 10 (+0), WIS 11 (+0), CHA 10 (+0) |
| CR | 1/8 |
| XP | 25 |
| PB | +2 |
| Skills | Deception +2, Religion +2 |
| Gear | Leather Armor, Sickle |
| Senses | Passive Perception 10 |
| Languages | Common |

**Wants.** It wants a signature and then a sacrifice.

**Cheese.** Take the pamphlet away and it is just a nervous person with a knife.

**Tactics.** Stay in a clump. They chant only if two of them still stand.

**Reskin.** Scimitar or dagger as printed. The pamphlet is paper.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Hoodie Pamphleteer. Level 1. Unregistered faith.

**[GM]** They will explain the end of the world after they stab you. Priorities.

### Attacks

- **Ritual Sickle.** Melee Attack Roll: +3, reach 5 ft. Hit: 3 (1d4 + 1) Slashing damage plus 1 Necrotic damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Suitcase Lobby Crab

`f01-m-05` · mob · Suitcase Lobby Crab. Level 1. "The floor hired a crustacean."

**Picture.** A crab the size of a carry-on, clicking across the lobby tile like it pays rent.

**Engine.** Claw, melee, +3, reach 5 ft, 1d6+1 bludgeoning

| | |
|---|---|
| SRD block | Giant Crab |
| Type | Medium Beast, Unaligned |
| AC | 15 |
| Initiative | +1 |
| HP | 13 (3d8) |
| Speed | 30 ft., Swim 30 ft. |
| Abilities | STR 13 (+1), DEX 13 (+1), CON 11 (+0), INT 1 (-5), WIS 9 (-1), CHA 3 (-4) |
| CR | 1/8 |
| XP | 25 |
| PB | +2 |
| Skills | Stealth +3 |
| Senses | Blindsight 30 ft.; Passive Perception 9 |
| Languages | None |

**Wants.** It wants to be left in the fountain.

**Cheese.** Grapple is the whole threat. Don't stand in the water with it.

**Tactics.** Pin one Crawler. Ignore the others until the pin breaks.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Suitcase Lobby Crab. Level 1. Amphibious.

**[GM]** Guest services sent a crab. Guest services is not your friend.

### Traits

- **Amphibious.** The crab can breathe air and water

### Attacks

- **Claw.** Melee Attack Roll: +3, reach 5 ft. Hit: 4 (1d6 + 1) Bludgeoning damage. If the target is a Medium or smaller creature, it has the Grappled condition (escape DC 11) from one of two claws

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Foam-Head Mascot Dog

`f01-m-06` · mob · Foam-Head Mascot Dog. Level 1. "Somebody's prop that learned teeth."

**Picture.** A real mastiff wearing a mascot head it will not take off. The head is the bit. The teeth are not.

**Engine.** Bite, melee, +3, reach 5 ft, 1d6+1 piercing

| | |
|---|---|
| SRD block | Mastiff |
| Type | Medium Beast, Unaligned |
| AC | 12 |
| Initiative | +2 |
| HP | 5 (1d8 + 1) |
| Speed | 40 ft. |
| Abilities | STR 13 (+1), DEX 14 (+2), CON 12 (+1), INT 3 (-4), WIS 12 (+1), CHA 7 (-2) |
| CR | 1/8 |
| XP | 25 |
| PB | +2 |
| Skills | Perception +5 |
| Senses | Darkvision 60 ft.; Passive Perception 15 |
| Languages | None |

**Wants.** It wants a handler.

**Cheese.** A loud noise or a shut door. Do not kick it for sport.

**Tactics.** Bite the closest. It does not coordinate.

**Reskin.** None. Keen smell stays.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Foam-Head Mascot Dog. Level 1. Unleashed.

**[GM]** The costume came off. The dog did not get nicer.

### Attacks

- **Bite.** Melee Attack Roll: +3, reach 5 ft. Hit: 4 (1d6 + 1) Piercing damage. If the target is a Medium or smaller creature, it has the Prone condition

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Name-Tag Thief

`f01-m-07` · mob · Name-Tag Thief. Level 1. "Robbery with a hello sticker."

**Picture.** A person wearing a stolen staff badge, with your wallet already in the other hand.

**Engine.** Scimitar, melee, +3, reach 5 ft, 1d6+1 slashing; Light Crossbow, ranged, +3, range 80/320 ft, 1d8+1 piercing

| | |
|---|---|
| SRD block | Bandit |
| Type | Medium or Small Humanoid, Neutral |
| AC | 12 |
| Initiative | +1 |
| HP | 11 (2d8 + 2) |
| Speed | 30 ft. |
| Abilities | STR 11 (+0), DEX 12 (+1), CON 12 (+1), INT 10 (+0), WIS 10 (+0), CHA 10 (+0) |
| CR | 1/8 |
| XP | 25 |
| PB | +2 |
| Gear | Leather Armor, Light Crossbow, Scimitar |
| Senses | Passive Perception 10 |
| Languages | Common, Thieves’ Cant |

**Wants.** It wants the pouch, not the duel.

**Cheese.** Drop a coin and walk. They chase loot before they chase you.

**Tactics.** Crossbow if you run. Scimitar if you stay.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Name-Tag Thief. Level 1. Armed.

**[GM]** Hi, my name is Hands Off. It is not a joke. It is a threat.

### Attacks

- **Scimitar.** Melee Attack Roll: +3, reach 5 ft. Hit: 4 (1d6 + 1) Slashing damage
- **Light Crossbow.** Ranged Attack Roll: +3, range 80/320 ft. Hit: 5 (1d8 + 1) Piercing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Flashlight Turnstile Guard

`f01-m-08` · mob · Flashlight Turnstile Guard. Level 1. "The gate is a personality."

**Picture.** A bored guard at a waist-high turnstile, flashlight in your eyes, spear not for show.

**Engine.** Spear, 1d6+1 piercing

| | |
|---|---|
| SRD block | Guard |
| Type | Medium or Small Humanoid, Neutral |
| AC | 16 |
| Initiative | +1 |
| HP | 11 (2d8 + 2) |
| Speed | 30 ft. |
| Abilities | STR 13 (+1), DEX 12 (+1), CON 12 (+1), INT 10 (+0), WIS 11 (+0), CHA 10 (+0) |
| CR | 1/8 |
| XP | 25 |
| PB | +2 |
| Skills | Perception +2 |
| Gear | Chain Shirt, Shield, Spear |
| Senses | Passive Perception 12 |
| Languages | Common |

**Wants.** It wants the line to stay in order.

**Cheese.** Go around. Fighting the turnstile is how you donate hit points.

**Tactics.** Spear from behind the bar. They do not chase past the gate.

**Reskin.** None. The turnstile is difficult terrain, not a new attack.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Flashlight Turnstile Guard. Level 1. On post.

**[GM]** The gate has a spear and a opinion about your ticket.

### Attacks

- **Spear.** Melee or Ranged Attack Roll: +3, reach 5 ft. or range 20/60 ft. Hit: 4 (1d6 + 1) Piercing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Smiling Polo Mannequin

`f01-m-09` · mob · Smiling Polo Mannequin. Level 1. "Customer service after the employee left."

**Picture.** A department-store dummy in a staff polo. The smile is painted on. The bow is not a toy. There is nobody inside.

**Engine.** Shortsword, melee, +5, reach 5 ft, 1d6+3 piercing; Shortbow, ranged, +5, range 80/320 ft, 1d6+3 piercing

| | |
|---|---|
| SRD block | Skeleton |
| Type | Medium Undead, Lawful Evil |
| AC | 14 |
| Initiative | +3 |
| HP | 13 (2d8 + 4) |
| Speed | 30 ft. |
| Abilities | STR 10 (+0), DEX 16 (+3), CON 15 (+2), INT 6 (-2), WIS 8 (-1), CHA 5 (-3) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Gear | Shortbow, Shortsword |
| Vulnerabilities | Bludgeoning |
| Immunities | Poison; Exhaustion, Poisoned |
| Senses | Darkvision 60 ft.; Passive Perception 9 |
| Languages | Understands Common plus one other language but can’t speak |

**Wants.** It wants the script finished.

**Cheese.** Bludgeoning. A chair leg is a thesis.

**Tactics.** Shortbow from the booth, then the shortsword if you climb in.

**Reskin.** Vulnerable to bludgeoning, as printed.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Smiling Polo Mannequin. Level 1. Undead.

**[GM]** Ask it for a refund. It answers with arrows.

### Attacks

- **Shortsword.** Melee Attack Roll: +5, reach 5 ft. Hit: 6 (1d6 + 3) Piercing damage
- **Shortbow.** Ranged Attack Roll: +5, range 80/320 ft. Hit: 6 (1d6 + 3) Piercing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Pineapple-Club Goblin

`f01-m-10` · mob · Pineapple-Club Goblin. Level 1. "Armed middle management."

**Picture.** A small green goblin with a clipboard and a club topped like a pineapple. Kill one and the rest take it personally.

**Engine.** Scimitar, melee, +4, reach 5 ft, 1d6+2 slashing, plus 1d4 slashing; Shortbow, ranged, +4, range 80/320 ft, 1d6+2 piercing, plus 1d4 piercing; Nimble Escape

| | |
|---|---|
| SRD block | Goblin Warrior |
| Type | Small Fey (Goblinoid), Chaotic Neutral |
| AC | 15 |
| Initiative | +2 |
| HP | 10 (3d6) |
| Speed | 30 ft. |
| Abilities | STR 8 (-1), DEX 15 (+2), CON 10 (+0), INT 10 (+0), WIS 8 (-1), CHA 8 (-1) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Skills | Stealth +6 |
| Gear | Leather Armor, Scimitar, Shield, Shortbow |
| Senses | Darkvision 60 ft.; Passive Perception 9 |
| Languages | Common, Goblin |

**Wants.** It wants the form signed in blood.

**Cheese.** Break line of sight. Nimble Escape is a free exit.

**Tactics.** Shortbow from cover, scimitar if you close.

**Reskin.** Advantage extra damage stays. The clipboard is not a shield beyond the printed shield.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Pineapple-Club Goblin. Level 1. On the clock.

**[GM]** It has a clipboard. You are the incident report.

### Attacks

- **Scimitar.** Melee Attack Roll: +4, reach 5 ft. Hit: 5 (1d6 + 2) Slashing damage, plus 2 (1d4) Slashing damage if the attack roll had Advantage
- **Shortbow.** Ranged Attack Roll: +4, range 80/320 ft. Hit: 5 (1d6 + 2) Piercing damage, plus 2 (1d4) Piercing damage if the attack roll had Advantage

### Bonus actions

- **Nimble Escape.** The goblin takes the Disengage or Hide action

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Mop-Dragging Janitor Zombie

`f01-m-11` · mob · Mop-Dragging Janitor Zombie. Level 1. "Janitorial, posthumous."

**Picture.** A corpse in a janitor shirt, still pushing the mop, still biting whoever steps in the bucket.

**Engine.** Slam, melee, +3, reach 5 ft, 1d8+1 bludgeoning

| | |
|---|---|
| SRD block | Zombie |
| Type | Medium Undead, Neutral Evil |
| AC | 8 |
| Initiative | -2 |
| HP | 15 (2d8 + 6) |
| Speed | 20 ft. |
| Abilities | STR 13 (+1), DEX 6 (-2), CON 16 (+3), INT 3 (-4), WIS 6 (-2), CHA 5 (-3) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Immunities | Poison; Exhaustion, Poisoned |
| Senses | Darkvision 60 ft.; Passive Perception 8 |
| Languages | Understands Common plus one other language but can’t speak |

**Wants.** It wants to finish the hallway.

**Cheese.** Undead Fortitude is the trick. Don't tap it. Finish it.

**Tactics.** Slam the nearest. It does not chase a runner if a body is closer.

**Reskin.** Slam stays bludgeoning. The mop is the fist.

**House check.** The mop is set dressing. Tanya Ruiz's corpse cache on the Day page is a separate loot pile, not this zombie.

**[SYSTEM]** Mop-Dragging Janitor Zombie. Level 1. Undead.

**[GM]** It mops. You are the spill.

### Traits

- **Undead Fortitude.** If damage reduces the zombie to 0 Hit Points, it makes a Constitution saving throw (DC 5 plus the damage taken) unless the damage is Radiant or from a Critical Hit. On a successful save, the zombie drops to 1 Hit Point instead

### Attacks

- **Slam.** Melee Attack Roll: +3, reach 5 ft. Hit: 5 (1d8 + 1) Bludgeoning damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Screaming PA Mushroom

`f01-m-12` · mob · Screaming PA Mushroom. Level 1. "The intercom grew legs. Sort of."

**Picture.** A mushroom wired into the ceiling speakers. Get close and it shrieks the whole hallway awake.

**Engine.** Shriek

| | |
|---|---|
| SRD block | Shrieker Fungus |
| Type | Medium Plant, Unaligned |
| AC | 5 |
| Initiative | -5 |
| HP | 13 (3d8) |
| Speed | 5 ft. |
| Abilities | STR 1 (-5), DEX 1 (-5), CON 10 (+0), INT 1 (-5), WIS 3 (-4), CHA 1 (-5) |
| CR | 0 |
| XP | 0 |
| PB | +2 |
| Immunities | Blinded, Charmed, Deafened, Frightened |
| Senses | Blindsight 30 ft.; Passive Perception 6 |
| Languages | None |

**Wants.** It wants to be heard.

**Cheese.** Silence it or kill it before the shriek pulls the next room.

**Tactics.** It does not chase. It screams.

**Reskin.** Shriek is unchanged. Treat the scream as the floor alarm.

**House check.** Shriek is a reaction, not a spell and not a slot. CR 0, XP 0, matching rules/70.

**[SYSTEM]** Screaming PA Mushroom. Level 1. Alarm.

**[GM]** Turn that down. You cannot. That is the encounter.

### Reactions

- **Shriek.** Trigger: A creature or a source of Bright Light moves within 30 feet of the shrieker. Response: The shrieker emits a shriek audible within 300 feet of itself for 1 minute or until the shrieker dies

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Safety-Vest Pike Intern

`f01-u-01` · unit · Safety-Vest Pike Intern. Level 1. "Front rank of orientation."

**Picture.** A trainee in a neon vest holding a pole with a spearhead zip-tied to the end.

**Engine.** Spear, 1d6+1 piercing

| | |
|---|---|
| SRD block | Warrior Infantry |
| Type | Medium or Small Humanoid, Neutral |
| AC | 13 |
| Initiative | +0 |
| HP | 9 (2d8) |
| Speed | 30 ft. |
| Abilities | STR 13 (+1), DEX 11 (+0), CON 11 (+0), INT 8 (-1), WIS 11 (+0), CHA 8 (-1) |
| CR | 1/8 |
| XP | 25 |
| PB | +2 |
| Gear | Chain Shirt, Spear |
| Senses | Passive Perception 10 |
| Languages | Common |

**Wants.** It wants the line to hold.

**Cheese.** Kill the one in back giving the count. The pikes are dumb without a voice.

**Tactics.** They hold a lane. They do not split.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Safety-Vest Pike Intern. Level 1. Unit.

**[GM]** A hallway full of unpaid spears. Classic onboarding.

### Traits

- **Pack Tactics.** The warrior has Advantage on an attack roll against a creature if at least one of the warrior’s allies is within 5 feet of the creature and the ally doesn’t have the Incapacitated condition

### Attacks

- **Spear.** Melee or Ranged Attack Roll: +3, reach 5 ft. or range 20/60 ft. Hit: 4 (1d6 + 1) Piercing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Flying Razor Lanyard

`f01-u-02` · unit · Flying Razor Lanyard. Level 1. "HR found a use for compliance."

**Picture.** An ID badge on a cord that flies by itself and tries to file itself in your neck.

**Engine.** Slash, melee, +4, reach 5 ft, 1d8+2 slashing

| | |
|---|---|
| SRD block | Animated Flying Sword |
| Type | Small Construct, Unaligned |
| AC | 17 |
| Initiative | +4 |
| HP | 14 (4d6) |
| Speed | 5 ft., Fly 50 ft. (hover) |
| Abilities | STR 12 (+1), DEX 15 (+2), CON 11 (+0), INT 1 (-5), WIS 5 (-3), CHA 1 (-5) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Immunities | Poison, Psychic; Charmed, Deafened, Exhaustion, Frightened, Paralyzed, Petrified, Poisoned |
| Senses | Blindsight 60 ft.; Passive Perception 7 |
| Languages | None |

**Wants.** It wants a neck.

**Cheese.** It is a sword. It dies to whatever kills a sword. Don't duel it in a closet.

**Tactics.** Strafe one target. It does not guard a square.

**Reskin.** Cosmetic: plastic badge on the ricasso. Damage unchanged.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Flying Razor Lanyard. Level 1. Construct.

**[GM]** Your ID badge just tried to promote itself into your throat.

### Attacks

- **Slash.** Melee Attack Roll: +4, reach 5 ft. Hit: 6 (1d8 + 2) Slashing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Paper-Hat Snack Dog

`f01-u-03` · unit · Paper-Hat Snack Dog. Level 1. "Catering with a spear."

**Picture.** A small dog-person in a paper hat at the nacho cart. The cart is a prop. The knife is not.

**Engine.** Dagger, 1d4+2 piercing

| | |
|---|---|
| SRD block | Kobold Warrior |
| Type | Small Dragon, Neutral |
| AC | 14 |
| Initiative | +2 |
| HP | 7 (3d6 − 3) |
| Speed | 30 ft. |
| Abilities | STR 7 (-2), DEX 15 (+2), CON 9 (-1), INT 8 (-1), WIS 7 (-2), CHA 8 (-1) |
| CR | 1/8 |
| XP | 25 |
| PB | +2 |
| Gear | Daggers (3) |
| Senses | Darkvision 60 ft.; Passive Perception 8 |
| Languages | Common, Draconic |

**Wants.** It wants the cart between it and you.

**Cheese.** Flip the cart. They pack-tactic only while the cart gives them a buddy.

**Tactics.** They fight from behind the cart. Half cover if the cart is upright.

**Reskin.** Pack Tactics as printed. The cart is cover, not hit points.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Paper-Hat Snack Dog. Level 1. Unit.

**[GM]** Today's special is stabbing. Sides are also stabbing.

### Traits

- **Pack Tactics.** The kobold has Advantage on an attack roll against a creature if at least one of the kobold’s allies is within 5 feet of the creature and the ally doesn’t have the Incapacitated condition
- **Sunlight Sensitivity.** While in sunlight, the kobold has Disadvantage on ability checks and attack rolls

### Attacks

- **Dagger.** Melee or Ranged Attack Roll: +4, reach 5 ft. or range 20/60 ft. Hit: 4 (1d4 + 2) Piercing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Nacho-Cheese Steam Cloud

`f01-u-04` · unit · Nacho-Cheese Steam Cloud. Level 1. "The popcorn machine unionized."

**Picture.** A little cloud of hot concession steam with a face, claws, and a bad attitude about the heat lamp.

**Engine.** Claw, melee, +2, reach 5 ft, 1d4 slashing, plus 1d4 fire; Steam Breath (Recharge 6), Constitution DC 10, 2d4 fire, recharge 6

| | |
|---|---|
| SRD block | Steam Mephit |
| Type | Small Elemental, Neutral Evil |
| AC | 10 |
| Initiative | +0 |
| HP | 17 (5d6) |
| Speed | 30 ft., Fly 30 ft. |
| Abilities | STR 5 (-3), DEX 11 (+0), CON 10 (+0), INT 11 (+0), WIS 10 (+0), CHA 12 (+1) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Skills | Stealth +2 |
| Immunities | Fire, Poison; Exhaustion, Poisoned |
| Senses | Darkvision 60 ft.; Passive Perception 10 |
| Languages | Primordial (Aquan, Ignan) |

**Wants.** It wants the room hot and blinded.

**Cheese.** Kill it before it dies on purpose. The death burst is the bit.

**Tactics.** Blind, then explode if bloodied.

**Reskin.** Fire damage stays fire. Call the cloud butter smoke.

**House check.** Steam Breath is recharge 6, one pending use. Death Burst happens when it dies. Neither is a spell slot.

**[SYSTEM]** Nacho-Cheese Steam Cloud. Level 1. Elemental.

**[GM]** It smells like a county fair and it will end you.

### Traits

- **Blurred Form.** Attack rolls against the mephit are made with Disadvantage unless the mephit has the Incapacitated condition
- **Death Burst.** The mephit explodes when it dies. Dexterity Saving Throw: DC 10, each creature in a 5-foot Emanation originating from the mephit. Failure: 5 (2d4) Fire damage. Success: Half damage

### Attacks

- **Claw.** Melee Attack Roll: +2, reach 5 ft. Hit: 2 (1d4) Slashing damage plus 2 (1d4) Fire damage.
- **Steam Breath (Recharge 6).** Constitution Saving Throw: DC 10, each creature in a 15-foot Cone. Failure: 5 (2d4) Fire damage, and the target’s Speed decreases by 10 feet until the end of the mephit’s next turn. Success: Half damage only. Failure or Success: Being underwater doesn’t grant Resistance to this Fire damage.

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Steam Breath** (recharge, max 1). Starts ready. After Steam Breath is used, it is down until a d6 at the start of this creature's turn shows 6–6. It cannot be used every turn.

## Hold-Music Choir Intern

`f01-u-05` · unit · Hold-Music Choir Intern. Level 1. "The announcement voice has a congregation."

**Picture.** A junior priest chanting the hold music, holy symbol in one hand and a mace in the other.

**Engine.** Mace, melee, +4, reach 5 ft, 1d6+2 bludgeoning, plus 1d4 radiant; Radiant Flame, ranged, +4, range 60/60 ft, 2d6 radiant; Spellcasting: spend tracked_uses. At-will does not spend.; Spellcasting: spend tracked_uses. At-will does not spend.

| | |
|---|---|
| SRD block | Priest Acolyte |
| Type | Medium or Small Humanoid (Cleric), Neutral |
| AC | 13 |
| Initiative | +0 |
| HP | 11 (2d8 + 2) |
| Speed | 30 ft. |
| Abilities | STR 14 (+2), DEX 10 (+0), CON 12 (+1), INT 10 (+0), WIS 14 (+2), CHA 11 (+0) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Skills | Medicine +4, Religion +2 |
| Gear | Chain Shirt, Holy Symbol, Mace |
| Senses | Passive Perception 12 |
| Languages | Common |

**Wants.** It wants the squad healed.

**Cheese.** Drop the acolyte first. The pikes get brave when someone is praying.

**Tactics.** Stays behind the Safety-Vest Pike Interns. Heals the front.

**Reskin.** Spells as printed. The microphone is a holy symbol.

**House check.** Cantrips are at will. Divine Aid is one cast of Bless, Healing Word, or Sanctuary, not one of each. At 0, Mace and Radiant Flame only.

**[SYSTEM]** Hold-Music Choir Intern. Level 1. Unit support.

**[GM]** Please hold. Your death is important to us.

### Attacks

- **Mace.** Melee Attack Roll: +4, reach 5 ft. Hit: 5 (1d6 + 2) Bludgeoning damage plus 2 (1d4) Radiant damage
- **Radiant Flame.** Ranged Attack Roll: +4, range 60 ft. Hit: 7 (2d6) Radiant damage
- **Spellcasting.** The priest casts one of the following spells, using Wisdom as the spellcasting ability: At Will: Light, Thaumaturgy

### Bonus actions

- **Divine Aid (1/Day).** The priest casts Bless, Healing Word, or Sanctuary, using the same spellcasting ability as Spellcasting.

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Divine Aid** (shared_spell_pool, max 1). 1 cast(s) total, any mix of Bless, Healing Word, Sanctuary. Not that many of each spell. At 0, weapon attacks and at-will cantrips only.
- **Light** (at_will, no cap (at will), spell level 0). At will. Not a spell slot. May be repeated. Do not spend a slot for it.
- **Thaumaturgy** (at_will, no cap (at will), spell level 0). At will. Not a spell slot. May be repeated. Do not spend a slot for it.

## Mop-Length Hall Centipede

`f01-u-06` · unit · Mop-Length Hall Centipede. Level 1. "The baseboard's night shift."

**Picture.** A centipede as long as a mop handle, in the hallway, with a bite that makes you sick.

**Engine.** Bite, melee, +4, reach 5 ft, 1d4+2 piercing

| | |
|---|---|
| SRD block | Giant Centipede |
| Type | Small Beast, Unaligned |
| AC | 14 |
| Initiative | +2 |
| HP | 9 (2d6 + 2) |
| Speed | 30 ft., Climb 30 ft. |
| Abilities | STR 5 (-3), DEX 14 (+2), CON 12 (+1), INT 1 (-5), WIS 7 (-2), CHA 3 (-4) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Senses | Blindsight 30 ft.; Passive Perception 8 |
| Languages | None |

**Wants.** It wants a boot.

**Cheese.** Don't let it bite and run. The poison is the whole job.

**Tactics.** One bite, then they skitter under the bench.

**Reskin.** Poison as printed.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Mop-Length Hall Centipede. Level 1. Unit.

**[GM]** Hundreds of legs, one bad idea, all of them aimed at you.

### Attacks

- **Bite.** Melee Attack Roll: +4, reach 5 ft. Hit: 4 (1d4 + 2) Piercing damage, and the target has the Poisoned condition until the start of the centipede’s next turn

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Walking Empty Pit-Bull Suit

`f01-e-01` · elite · Walking Empty Pit-Bull Suit. Level 1. "Foam outside. Felony inside."

**Picture.** An empty pit-bull mascot costume walking around. Foam outside. Nobody inside. It still swings.

**Engine.** Multiattack: 2 x Slam; Slam, melee, +4, reach 5 ft, 1d6+2 bludgeoning

| | |
|---|---|
| SRD block | Animated Armor |
| Type | Medium Construct, Unaligned |
| AC | 18 |
| Initiative | +2 |
| HP | 33 (6d8 + 6) |
| Speed | 25 ft. |
| Abilities | STR 14 (+2), DEX 11 (+0), CON 13 (+1), INT 1 (-5), WIS 3 (-4), CHA 1 (-5) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Immunities | Poison, Psychic; Charmed, Deafened, Exhaustion, Frightened, Paralyzed, Petrified, Poisoned |
| Senses | Blindsight 60 ft.; Passive Perception 6 |
| Languages | None |

**Wants.** It wants to be worn, or to wear you.

**Cheese.** It is a construct. Poison is a compliment it ignores. Bludgeon the seams.

**Tactics.** Slam the closest. It does not speak.

**Reskin.** Describe foam. Numbers stay Animated Armor.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Walking Empty Pit-Bull Suit. Level 1. Elite. Construct.

**[GM]** The mascot is empty, which is the worst kind of mascot.

### Attacks

- **Multiattack.** The armor makes two Slam attacks
- **Slam.** Melee Attack Roll: +4, reach 5 ft. Hit: 5 (1d6 + 2) Bludgeoning damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Seven-Foot Hairy Break-Room Bully

`f01-e-02` · elite · Seven-Foot Hairy Break-Room Bully. Level 1. "Took the last chair and the reach."

**Picture.** A huge hairy goblin-cousin who reaches you from a step farther away than your eyes agreed to.

**Engine.** Grab, melee, +4, reach 10 ft, 2d6+2 bludgeoning; Light Hammer, 3d4+2 bludgeoning

| | |
|---|---|
| SRD block | Bugbear Warrior |
| Type | Medium Fey (Goblinoid), Chaotic Evil |
| AC | 14 |
| Initiative | +2 |
| HP | 33 (6d8 + 6) |
| Speed | 30 ft. |
| Abilities | STR 15 (+2), DEX 14 (+2), CON 13 (+1), INT 8 (-1), WIS 11 (+0), CHA 9 (-1) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Skills | Stealth +6, Survival +2 |
| Gear | Hide Armor, Light Hammers (3) |
| Senses | Darkvision 60 ft.; Passive Perception 10 |
| Languages | Common, Goblin |

**Wants.** It wants one Crawler in its hands.

**Cheese.** Don't stand in a line. Ten feet of reach plus a grab.

**Tactics.** Grab, then hammer the grabbed one.

**Reskin.** None.

**House check.** The Break Room is a saferoom through Day 3 and goes offline on Day 4. A bugbear here is a fight. It does not grant a rest.

**[SYSTEM]** Seven-Foot Hairy Break-Room Bully. Level 1. Elite.

**[GM]** Break room means it breaks you. The sign was accurate.

### Traits

- **Abduct.** The bugbear needn’t spend extra movement to move a creature it is grappling

### Attacks

- **Grab.** Melee Attack Roll: +4, reach 10 ft. Hit: 9 (2d6 + 2) Bludgeoning damage. If the target is a Medium or smaller creature, it has the Grappled condition (escape DC 12)
- **Light Hammer.** Melee or Ranged Attack Roll: +4 (with Advantage if the target is Grappled by the bugbear), reach 10 ft. or range 20/60 ft. Hit: 9 (3d4 + 2) Bludgeoning damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Craft-Services Corpse

`f01-e-03` · elite · Craft-Services Corpse. Level 1. "Talent relations, after the talent died."

**Picture.** A hungry corpse in the green room, eating whoever stopped moving, including the sandwich tray.

**Engine.** Multiattack: 2 x Bite; Bite, melee, +4, reach 5 ft, 1d6+2 piercing, plus 1d6 necrotic; Claw, melee, +4, reach 5 ft, 1d4+2 slashing

| | |
|---|---|
| SRD block | Ghoul |
| Type | Medium Undead, Chaotic Evil |
| AC | 12 |
| Initiative | +2 |
| HP | 22 (5d8) |
| Speed | 30 ft. |
| Abilities | STR 13 (+1), DEX 15 (+2), CON 10 (+0), INT 7 (-2), WIS 10 (+0), CHA 6 (-2) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Immunities | Poison; Charmed, Exhaustion, Poisoned |
| Senses | Darkvision 60 ft.; Passive Perception 10 |
| Languages | Common |

**Wants.** It wants a body that stays down.

**Cheese.** Paralysis is the fight. Spread out. Don't all stand in claw range.

**Tactics.** Claw the softest looking Crawler.

**Reskin.** None.

**House check.** The Green Room stays open and is where level 2 is granted. This ghoul is not the saferoom.

**[SYSTEM]** Craft-Services Corpse. Level 1. Elite. Undead.

**[GM]** The green room is not saferoom. Learn the difference or get eaten in it.

### Attacks

- **Multiattack.** The ghoul makes two Bite attacks
- **Bite.** Melee Attack Roll: +4, reach 5 ft. Hit: 5 (1d6 + 2) Piercing damage plus 3 (1d6) Necrotic damage
- **Claw.** Melee Attack Roll: +4, reach 5 ft. Hit: 4 (1d4 + 2) Slashing damage. If the target is a creature that isn’t an Undead or elf, it is subjected to the following effect. Constitution Saving Throw: DC 10. Failure: The target has the Paralyzed condition until the end of its next turn

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Janitor-Vest Night Ghost

`f01-e-04` · elite · Janitor-Vest Night Ghost. Level 1. "What the lights do when they go out."

**Picture.** A see-through night-shift janitor. The mop passes through the floor. The cold does not pass through you.

**Engine.** Life Drain, melee, +4, reach 5 ft, 2d6 necrotic

| | |
|---|---|
| SRD block | Specter |
| Type | Medium Undead, Chaotic Evil |
| AC | 12 |
| Initiative | +2 |
| HP | 22 (5d8) |
| Speed | 30 ft., Fly 50 ft. (hover) |
| Abilities | STR 1 (-5), DEX 14 (+2), CON 11 (+0), INT 10 (+0), WIS 10 (+0), CHA 11 (+0) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Resistances | Acid, Bludgeoning, Cold, Fire, Lightning, Piercing, Slashing, Thunder |
| Immunities | Necrotic, Poison; Charmed, Exhaustion, Grappled, Paralyzed, Petrified, Poisoned, Prone, Restrained, Unconscious |
| Senses | Darkvision 60 ft.; Passive Perception 10 |
| Languages | Understands Common plus one other language but can’t speak |

**Wants.** It wants life, specifically yours.

**Cheese.** It hates sunlight and turning. If you have neither, don't clump.

**Tactics.** Life drain the wounded.

**Reskin.** None. Incorporeal as printed.

**House check.** Lights-Out and Ceiling Ticks are floor hazards. They are not attacks on this stat block. Do not add them.

**[SYSTEM]** Janitor-Vest Night Ghost. Level 1. Elite. Undead.

**[GM]** The lights did not go out. They got up and swung.

### Traits

- **Incorporeal Movement.** The specter can move through other creatures and objects as if they were Difficult Terrain. It takes 5 (1d10) Force damage if it ends its turn inside an object
- **Sunlight Sensitivity.** While in sunlight, the specter has Disadvantage on ability checks and attack rolls

### Attacks

- **Life Drain.** Melee Attack Roll: +4, reach 5 ft. Hit: 7 (2d6) Necrotic damage. If the target is a creature, its Hit Point maximum decreases by an amount equal to the damage taken.

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Golf-Cart Concession Spider

`f01-b-01` · boss · Golf-Cart Concession Spider. Level 1. Boss. "The snack ceiling."

**Picture.** A spider the size of a golf cart, webbing the gap between the nacho warmers.

**Engine.** Bite, melee, +5, reach 5 ft, 1d8+3 piercing, plus 2d6 poison; Web (Recharge 5–6), Dexterity DC 13, recharge 5-6

| | |
|---|---|
| SRD block | Giant Spider |
| Type | Large Beast, Unaligned |
| AC | 14 |
| Initiative | +3 |
| HP | 26 (4d10 + 4) |
| Speed | 30 ft., Climb 30 ft. |
| Abilities | STR 14 (+2), DEX 16 (+3), CON 12 (+1), INT 2 (-4), WIS 11 (+0), CHA 4 (-3) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Skills | Perception +4, Stealth +7 |
| Senses | Darkvision 60 ft.; Passive Perception 14 |
| Languages | None |

**Wants.** It wants the party webbed and quiet.

**Cheese.** Burn or cut the web. Don't all rush the stairs.

**Tactics.** Web the front, bite the stuck.

**Reskin.** None. This is the Level 1 boss cap for four Crawlers.

**House check.** Legal Level 1 boss cap for four Crawlers (CR 1). Web is recharge 5–6, not every turn.

**[SYSTEM]** Golf-Cart Concession Spider. Level 1. Boss.

**[GM]** The concession stand has a manager. The manager has eight legs.

### Traits

- **Spider Climb.** The spider can climb difficult surfaces, including along ceilings, without needing to make an ability check
- **Web Walker.** The spider ignores movement restrictions caused by webs, and it knows the location of any other creature in contact with the same web

### Attacks

- **Bite.** Melee Attack Roll: +5, reach 5 ft. Hit: 7 (1d8 + 3) Piercing damage plus 7 (2d6) Poison damage.
- **Web (Recharge 5–6).** Dexterity Saving Throw: DC 13, one creature the spider can see within 60 feet. Failure: The target has the Restrained condition until the web is destroyed (AC 10; HP 5; Vulnerability to Fire damage; Immunity to Poison and Psychic damage)

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Web** (recharge, max 1). Starts ready. After Web is used, it is down until a d6 at the start of this creature's turn shows 5–6. It cannot be used every turn.

## Adjunct Smash, Podium Giant

`f01-b-02` · boss · Adjunct Smash, Podium Giant. Level 2. Boss. "Has not taken a break in nine years."

**Picture.** A ten-foot teacher with a podium for a club. This is not Dean Thudd. The live floor still has the Dean.

**Engine.** Greatclub, melee, +6, reach 5 ft, 2d8+4 bludgeoning; Javelin, 2d6+4 piercing

| | |
|---|---|
| SRD block | Ogre |
| Type | Large Giant, Chaotic Evil |
| AC | 11 |
| Initiative | -1 |
| HP | 68 (8d10 + 24) |
| Speed | 40 ft. |
| Abilities | STR 19 (+4), DEX 8 (-1), CON 16 (+3), INT 5 (-3), WIS 7 (-2), CHA 7 (-2) |
| CR | 2 |
| XP | 450 |
| PB | +2 |
| Gear | Greatclub, Javelins (3) |
| Senses | Darkvision 60 ft.; Passive Perception 8 |
| Languages | Common, Giant |

**Wants.** It wants the group in front of the podium.

**Cheese.** Split. The club is one target. Do not pose for it.

**Tactics.** Greatclub the clustered, javelin the runner.

**Reskin.** The club is a podium. Damage stays the ogre club. Floor 1 Level 2 boss day only.

**House check.** Legal on the Floor 1 Level 2 boss budget only. The live floor boss is Dean Thudd on the Day pages. Do not field this card as a second dean.

**[SYSTEM]** Adjunct Smash, Podium Giant. Level 2. Boss.

**[GM]** Orientation is over. The dean is the size of a mistake.

### Attacks

- **Greatclub.** Melee Attack Roll: +6, reach 5 ft. Hit: 13 (2d8 + 4) Bludgeoning damage
- **Javelin.** Melee or Ranged Attack Roll: +6, reach 5 ft. or range 30/120 ft. Hit: 11 (2d6 + 4) Piercing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.


# Floor 2 — Soft Open

Ten-day clock (decision 026). The Floor 2 canon table is reserve and was not copied onto these cards. Soft-open and ratings are house set dressing. Floors 1–2 stay Bronze and Silver: Common default, Uncommon peak. No Gold from a random draw. A Long Rest finishes in a saferoom (core saferoom overlay).

## Sash-Wearing Tall Goblin Sergeant

`f02-m-01` · mob · Sash-Wearing Tall Goblin Sergeant. Level 1. "They rehearsed."

**Picture.** A tall, drilled goblin in a soft-open sash. Meaner than the interns and better at standing in a line.

**Engine.** Longsword, melee, +3, reach 5 ft, 2d10+1 slashing; Longbow, ranged, +3, range 150/600 ft, 1d8+1 piercing, plus 3d4 poison

| | |
|---|---|
| SRD block | Hobgoblin Warrior |
| Type | Medium Fey (Goblinoid), Lawful Evil |
| AC | 18 |
| Initiative | +3 |
| HP | 11 (2d8 + 2) |
| Speed | 30 ft. |
| Abilities | STR 13 (+1), DEX 12 (+1), CON 12 (+1), INT 10 (+0), WIS 10 (+0), CHA 9 (-1) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Gear | Half Plate Armor, Longbow, Longsword, Shield |
| Senses | Darkvision 60 ft.; Passive Perception 10 |
| Languages | Common, Goblin |

**Wants.** It wants a formation.

**Cheese.** Kill them out of order and Martial Advantage gets lonely.

**Tactics.** They strike whoever is already next to an ally.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Sash-Wearing Tall Goblin Sergeant. Level 1. Formation.

**[GM]** Opening night. The ushers brought discipline and a longsword.

### Traits

- **Pack Tactics.** The hobgoblin has Advantage on an attack roll against a creature if at least one of the hobgoblin’s allies is within 5 feet of the creature and the ally doesn’t have the Incapacitated condition

### Attacks

- **Longsword.** Melee Attack Roll: +3, reach 5 ft. Hit: 12 (2d10 + 1) Slashing damage
- **Longbow.** Ranged Attack Roll: +3, range 150/600 ft. Hit: 5 (1d8 + 1) Piercing damage plus 7 (3d4) Poison damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Boot-Eating Mop Water

`f02-m-02` · mob · Boot-Eating Mop Water. Level 1. "It eats the cleaning budget."

**Picture.** A puddle of gray mop water that climbs your boots and digests the metal while you are still wearing them.

**Engine.** Pseudopod, melee, +3, reach 5 ft, 2d8+1 acid

| | |
|---|---|
| SRD block | Gray Ooze |
| Type | Medium Ooze, Unaligned |
| AC | 9 |
| Initiative | -2 |
| HP | 22 (3d8 + 9) |
| Speed | 10 ft., Climb 10 ft. |
| Abilities | STR 12 (+1), DEX 6 (-2), CON 16 (+3), INT 1 (-5), WIS 6 (-2), CHA 2 (-4) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Skills | Stealth +2 |
| Resistances | Acid, Cold, Fire |
| Immunities | Blinded, Charmed, Deafened, Exhaustion, Frightened, Grappled, Prone, Restrained |
| Senses | Blindsight 60 ft.; Passive Perception 8 |
| Languages | None |

**Wants.** It wants metal and stillness.

**Cheese.** Don't stand in it. It is hard to see and rude to armor.

**Tactics.** Pseudopod the armored one.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Boot-Eating Mop Water. Level 1. Ooze.

**[GM]** You just stepped in management. Management is acidic.

### Traits

- **Amorphous.** The ooze can move through a space as narrow as 1 inch without expending extra movement to do so
- **Corrosive Form.** Nonmagical ammunition is destroyed immediately after hitting the ooze and dealing any damage. Any nonmagical weapon takes a cumulative −1 penalty to attack rolls immediately after dealing damage to the ooze and coming into contact with it. The weapon is destroyed if the penalty reaches −5. The penalty can be removed by casting the Mending spell on the weapon. The ooze can eat through 2-inch-thick, nonmagical metal or wood in 1 round

### Attacks

- **Pseudopod.** Melee Attack Roll: +3, reach 5 ft. Hit: 10 (2d8 + 1) Acid damage. Nonmagical armor worn by the target takes a −1 penalty to the AC it offers. The armor is destroyed if the penalty reduces its AC to 10. The penalty can be removed by casting the Mending spell on the armor.

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Route-Knowing Clipboard Scout

`f02-m-03` · mob · Route-Knowing Clipboard Scout. Level 1. "Maps you while you talk."

**Picture.** A scout who already highlighted your path on a clipboard. The bow is for when the highlight is not enough.

**Engine.** Multiattack: Shortsword; Shortsword, melee, +4, reach 5 ft, 1d6+2 piercing; Longbow, ranged, +4, range 150/600 ft, 1d8+2 piercing

| | |
|---|---|
| SRD block | Scout |
| Type | Medium or Small Humanoid, Neutral |
| AC | 13 |
| Initiative | +2 |
| HP | 16 (3d8 + 3) |
| Speed | 30 ft. |
| Abilities | STR 11 (+0), DEX 14 (+2), CON 12 (+1), INT 11 (+0), WIS 13 (+1), CHA 11 (+0) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Skills | Nature +4, Perception +5, Stealth +6, Survival +5 |
| Gear | Leather Armor, Longbow, Shortsword |
| Senses | Passive Perception 15 |
| Languages | Common plus one other language |

**Wants.** It wants your route.

**Cheese.** Close fast. The bow is the job.

**Tactics.** Shoot, fall back, shoot.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Route-Knowing Clipboard Scout. Level 1. Skirmisher.

**[GM]** It is taking notes. The notes are arrows.

### Attacks

- **Multiattack.** The scout makes two attacks, using Shortsword and Longbow in any combination
- **Shortsword.** Melee Attack Roll: +4, reach 5 ft. Hit: 5 (1d6 + 2) Piercing damage
- **Longbow.** Ranged Attack Roll: +4, range 150/600 ft. Hit: 6 (1d8 + 2) Piercing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Laughing Hyena Person

`f02-m-04` · mob · Laughing Hyena Person. Level 1. "The laugh track learned hunger."

**Picture.** A hyena-headed person with a spear. The laugh is the warning. The spear is the sentence.

**Engine.** Rend, melee, +4, reach 5 ft, 1d6+2 piercing; Bone Bow, ranged, +3, range 150/600 ft, 1d10+1 piercing; Rampage (1/Day)

| | |
|---|---|
| SRD block | Gnoll Warrior |
| Type | Medium Fiend, Chaotic Evil |
| AC | 15 |
| Initiative | +1 |
| HP | 27 (6d8) |
| Speed | 30 ft. |
| Abilities | STR 14 (+2), DEX 12 (+1), CON 11 (+0), INT 6 (-2), WIS 10 (+0), CHA 7 (-2) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Senses | Darkvision 60 ft.; Passive Perception 10 |
| Languages | Gnoll |

**Wants.** It wants a downed Crawler.

**Cheese.** Don't leave a body in reach. Rampage is a second meal.

**Tactics.** They pile the wounded.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Laughing Hyena Person. Level 1. Hostile.

**[GM]** The audience laughs when something falls over. You are the something.

### Attacks

- **Rend.** Melee Attack Roll: +4, reach 5 ft. Hit: 5 (1d6 + 2) Piercing damage
- **Bone Bow.** Ranged Attack Roll: +3, range 150/600 ft. Hit: 6 (1d10 + 1) Piercing damage

### Bonus actions

- **Rampage (1/Day).** Immediately after dealing damage to a creature that is already Bloodied, the gnoll moves up to half its Speed, and it makes one Rend attack.

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Rampage** (daily, max 1). 1 use(s) per day, shared by this ability, not per target and not per round. At 0 it does not fire again until a Long Rest in a saferoom.

## Couch-Sized Saddle Wolf

`f02-m-05` · mob · Couch-Sized Saddle Wolf. Level 1. "Freight with opinions."

**Picture.** A wolf the size of a couch, saddle worn shiny, looking for a rider or a meal.

**Engine.** Bite, melee, +5, reach 5 ft, 1d8+3 piercing

| | |
|---|---|
| SRD block | Worg |
| Type | Large Fey, Neutral Evil |
| AC | 13 |
| Initiative | +1 |
| HP | 26 (4d10 + 4) |
| Speed | 50 ft. |
| Abilities | STR 16 (+3), DEX 13 (+1), CON 13 (+1), INT 7 (-2), WIS 11 (+0), CHA 8 (-1) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Skills | Perception +4 |
| Senses | Darkvision 60 ft.; Passive Perception 14 |
| Languages | Goblin, Worg |

**Wants.** It wants a chase.

**Cheese.** Don't run down the dock. Bite, then they drag.

**Tactics.** Knock a Crawler prone and hold the lane.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Couch-Sized Saddle Wolf. Level 1.

**[GM]** The dock accepts deliveries. You are a delivery.

### Attacks

- **Bite.** Melee Attack Roll: +5, reach 5 ft. Hit: 7 (1d8 + 3) Piercing damage, and the next attack roll made against the target before the start of the worg’s next turn has Advantage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Sword-Eating Antenna Bug

`f02-m-06` · mob · Sword-Eating Antenna Bug. Level 1. "Props are food."

**Picture.** A bug with long feelers that rusts the sword in your hand down to orange flakes.

**Engine.** Multiattack: The rust monster makes one Bite attack and uses Antennae twice; Bite, melee, +3, reach 5 ft, 1d8+1 piercing; Antennae, Dexterity DC 11; Destroy Metal; Reflexive Antennae

| | |
|---|---|
| SRD block | Rust Monster |
| Type | Medium Monstrosity, Unaligned |
| AC | 14 |
| Initiative | +1 |
| HP | 33 (6d8 + 6) |
| Speed | 40 ft. |
| Abilities | STR 13 (+1), DEX 12 (+1), CON 13 (+1), INT 2 (-4), WIS 13 (+1), CHA 6 (-2) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Senses | Darkvision 60 ft.; Passive Perception 11 |
| Languages | None |

**Wants.** It wants the metal, not the person.

**Cheese.** Throw a spare weapon. It will go eat that.

**Tactics.** Antennae the shiniest armor.

**Reskin.** None. Losing a weapon is the cheese and the tax.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Sword-Eating Antenna Bug. Level 1. Monstrosity.

**[GM]** Your sword just became a suggestion.

### Traits

- **Iron Scent.** The rust monster can pinpoint the location of ferrous metal within 30 feet of itself

### Attacks

- **Multiattack.** The rust monster makes one Bite attack and uses Antennae twice
- **Bite.** Melee Attack Roll: +3, reach 5 ft. Hit: 5 (1d8 + 1) Piercing damage
- **Antennae.** The rust monster targets one nonmagical metal object—armor or a weapon—worn or carried by a creature within 5 feet of itself. Dexterity Saving Throw: DC 11, the creature with the object. Failure: The object takes a −1 penalty to the AC it offers (armor) or to its attack rolls (weapon). Armor is destroyed if the penalty reduces its AC to 10, and a weapon is destroyed if its penalty reaches −5. The penalty can be removed by casting the Mending spell on the armor or weapon
- **Destroy Metal.** The rust monster touches a nonmagical metal object within 5 feet of itself that isn’t being worn or carried. The touch destroys a 1-foot Cube of the object

### Reactions

- **Reflexive Antennae.** Trigger: An attack roll hits the rust monster. Response: The rust monster uses Antennae.

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Your Shadow, On Payroll

`f02-m-07` · mob · Your Shadow, On Payroll. Level 1. "The lighting board got jealous."

**Picture.** Your own shadow, peeled off the floor, wearing nothing, hungry for the strength in your arms.

**Engine.** Draining Swipe, melee, +4, reach 5 ft, 1d6+2 necrotic; Shadow Stealth

| | |
|---|---|
| SRD block | Shadow |
| Type | Medium Undead, Chaotic Evil |
| AC | 12 |
| Initiative | +2 |
| HP | 27 (5d8 + 5) |
| Speed | 40 ft. |
| Abilities | STR 6 (-2), DEX 14 (+2), CON 13 (+1), INT 6 (-2), WIS 10 (+0), CHA 8 (-1) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Skills | Stealth +6 |
| Resistances | Acid, Cold, Fire, Lightning, Thunder |
| Vulnerabilities | Radiant |
| Immunities | Necrotic, Poison; Exhaustion, Frightened, Grappled, Paralyzed, Petrified, Poisoned, Prone, Restrained, Unconscious |
| Senses | Darkvision 60 ft.; Passive Perception 10 |
| Languages | None |

**Wants.** It wants Strength.

**Cheese.** Light. Spread out. Don't let it sit on the Strength 8.

**Tactics.** Strength drain, then hide in dim light.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Your Shadow, On Payroll. Level 1. Undead.

**[GM]** The lights are not your friend. The dark applied for the job.

### Traits

- **Amorphous.** The shadow can move through a space as narrow as 1 inch without expending extra movement to do so
- **Sunlight Weakness.** While in sunlight, the shadow has Disadvantage on D20 Tests

### Attacks

- **Draining Swipe.** Melee Attack Roll: +4, reach 5 ft. Hit: 5 (1d6 + 2) Necrotic damage, and the target’s Strength score decreases by 1d4. The target dies if this reduces that score to 0. If a Humanoid is slain by this attack, a Shadow rises from the corpse 1d4 hours later

### Bonus actions

- **Shadow Stealth.** While in Dim Light or Darkness, the shadow takes the Hide action

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Goat-Legged Warmup Comic

`f02-m-08` · mob · Goat-Legged Warmup Comic. Level 1. "Opens for the real monster."

**Picture.** Goat legs, little horns, pan pipes, and a tight five about your hit points.

**Engine.** Hooves, melee, +5, reach 5 ft, 1d4+3 bludgeoning; Mockery, Wisdom DC 12, 1d6+2 psychic

| | |
|---|---|
| SRD block | Satyr |
| Type | Medium Fey, Chaotic Neutral |
| AC | 13 |
| Initiative | +3 |
| HP | 31 (7d8) |
| Speed | 40 ft. |
| Abilities | STR 12 (+1), DEX 16 (+3), CON 11 (+0), INT 12 (+1), WIS 10 (+0), CHA 14 (+2) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Skills | Perception +2, Performance +6, Stealth +5 |
| Senses | Passive Perception 12 |
| Languages | Common, Elvish, Sylvan |

**Wants.** It wants you charmed and clumsy.

**Cheese.** Stuff your ears or drop the piper first.

**Tactics.** Pipes, then ram the charmed.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Goat-Legged Warmup Comic. Level 1. Fey.

**[GM]** The opening act is a goat with a work visa and a flute.

### Traits

- **Magic Resistance.** The satyr has Advantage on saving throws against spells and other magical effects

### Attacks

- **Hooves.** Melee Attack Roll: +5, reach 5 ft. Hit: 5 (1d4 + 3) Bludgeoning damage. If the target is a Medium or smaller creature, the satyr pushes the target up to 10 feet straight away from itself
- **Mockery.** Wisdom Saving Throw: DC 12, one creature the satyr can see within 90 feet. Failure: 5 (1d6 + 2) Psychic damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Walking Charcoal Briquette

`f02-m-09` · mob · Walking Charcoal Briquette. Level 1. "The fryer walked out."

**Picture.** A little person made of hot coals. Touching it is the whole mistake.

**Engine.** Touch, melee, +4, reach 5 ft, 2d4+2 fire; Ignited Illumination

| | |
|---|---|
| SRD block | Magmin |
| Type | Small Elemental, Chaotic Neutral |
| AC | 14 |
| Initiative | +2 |
| HP | 13 (3d6 + 3) |
| Speed | 30 ft. |
| Abilities | STR 7 (-2), DEX 15 (+2), CON 12 (+1), INT 8 (-1), WIS 11 (+0), CHA 10 (+0) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Immunities | Fire |
| Senses | Darkvision 60 ft.; Passive Perception 10 |
| Languages | Primordial (Ignan) |

**Wants.** It wants the floor on fire.

**Cheese.** Don't bunch on the oil. Kill it away from the paper stock.

**Tactics.** Touch, ignite, waddle.

**Reskin.** Fire as printed.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Walking Charcoal Briquette. Level 1. Elemental.

**[GM]** Fresh fried Crawler. Limited time.

### Traits

- **Death Burst.** The magmin explodes when it dies. Dexterity Saving Throw: DC 11, each creature in a 10-foot Emanation originating from the magmin. Failure: 7 (2d6) Fire damage. Success: Half damage

### Attacks

- **Touch.** Melee Attack Roll: +4, reach 5 ft. Hit: 7 (2d4 + 2) Fire damage. If the target is a creature or a flammable object that isn’t being worn or carried, it starts burning

### Bonus actions

- **Ignited Illumination.** The magmin sets itself ablaze or extinguishes its flames. While ablaze, the magmin sheds Bright Light in a 10-foot radius and Dim Light for an additional 10 feet

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Coughing Dust Cloud

`f02-m-10` · mob · Coughing Dust Cloud. Level 1. "A blinding bit."

**Picture.** A dust cloud with a face. It makes you cough, then it claws you for coughing.

**Engine.** Claw, melee, +4, reach 5 ft, 1d4+2 slashing; Blinding Breath (Recharge 6), Dexterity DC 10, recharge 6; Sleep (1/Day)

| | |
|---|---|
| SRD block | Dust Mephit |
| Type | Small Elemental, Neutral Evil |
| AC | 12 |
| Initiative | +2 |
| HP | 17 (5d6) |
| Speed | 30 ft., Fly 30 ft. |
| Abilities | STR 5 (-3), DEX 14 (+2), CON 10 (+0), INT 9 (-1), WIS 11 (+0), CHA 10 (+0) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Skills | Perception +2, Stealth +4 |
| Vulnerabilities | Fire |
| Immunities | Poison; Exhaustion, Poisoned |
| Senses | Darkvision 60 ft.; Passive Perception 12 |
| Languages | Primordial (Auran, Terran) |

**Wants.** It wants you coughing.

**Cheese.** Ranged attacks before it closes. The breath is the encounter.

**Tactics.** Blinding breath, then claws.

**Reskin.** None.

**House check.** Sleep is once per day, spell save DC 10, Charisma. Blinding Breath is recharge 6. At 0 Sleep, Claw only.

**[SYSTEM]** Coughing Dust Cloud. Level 1. Elemental.

**[GM]** Cough, then apologize, then get clawed. That is the act.

### Traits

- **Death Burst.** The mephit explodes when it dies. Dexterity Saving Throw: DC 10, each creature in a 5-foot Emanation originating from the mephit. Failure: 5 (2d4) Bludgeoning damage. Success: Half damage

### Attacks

- **Claw.** Melee Attack Roll: +4, reach 5 ft. Hit: 4 (1d4 + 2) Slashing damage.
- **Blinding Breath (Recharge 6).** Dexterity Saving Throw: DC 10, each creature in a 15-foot Cone. Failure: The target has the Blinded condition until the end of the mephit’s next turn.
- **Sleep (1/Day).** The mephit casts the Sleep spell, requiring no spell components and using Charisma as the spellcasting ability (spell save DC 10)

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Blinding Breath** (recharge, max 1). Starts ready. After Blinding Breath is used, it is down until a d6 at the start of this creature's turn shows 6–6. It cannot be used every turn.
- **Sleep** (daily_spell, max 1, spell level 1). Once per day. Level 1 Sleep, Charisma, spell save DC 10. Not a slot that refills. At 0, do not cast Sleep.

## Trident Lifeguard Fish-Person

`f02-u-01` · unit · Trident Lifeguard Fish-Person. Level 1. "The decorative tank is staffed."

**Picture.** A fish-person with a whistle and a trident. The pool is decorative until it is not.

**Engine.** Multiattack: 2 x Claw; Claw, melee, +3, reach 5 ft, 1d6+1 slashing; Aquatic Charge

| | |
|---|---|
| SRD block | Sahuagin Warrior |
| Type | Medium Fiend, Lawful Evil |
| AC | 12 |
| Initiative | +0 |
| HP | 22 (4d8 + 4) |
| Speed | 30 ft., Swim 40 ft. |
| Abilities | STR 13 (+1), DEX 11 (+0), CON 12 (+1), INT 12 (+1), WIS 13 (+1), CHA 9 (-1) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Skills | Perception +5 |
| Resistances | Acid, Cold |
| Senses | Darkvision 120 ft.; Passive Perception 15 |
| Languages | Sahuagin |

**Wants.** It wants you in the water.

**Cheese.** Stay on the dry walk. Blood frenzy only matters if someone is already hurt in the pool.

**Tactics.** They stay in the water and spear the edge.

**Reskin.** None. The tank is the arena, not a new power.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Trident Lifeguard Fish-Person. Level 1. Unit.

**[GM]** No diving. The sign means the fish have spears.

### Traits

- **Blood Frenzy.** The sahuagin has Advantage on attack rolls against any creature that doesn’t have all its Hit Points
- **Limited Amphibiousness.** The sahuagin can breathe air and water, but it must be submerged at least once every 4 hours to avoid suffocating outside water
- **Shark Telepathy.** The sahuagin can magically control sharks within 120 feet of itself, using a special telepathy

### Attacks

- **Multiattack.** The sahuagin makes two Claw attacks
- **Claw.** Melee Attack Roll: +3, reach 5 ft. Hit: 4 (1d6 + 1) Slashing damage

### Bonus actions

- **Aquatic Charge.** The sahuagin swims up to its Swim Speed straight toward an enemy it can see

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Petrifying Chicken-Lizard

`f02-u-02` · unit · Petrifying Chicken-Lizard. Level 1. "Wardrobe sent a bird."

**Picture.** A chicken with a lizard tail and a mean beak. One peck and you are a lawn statue.

**Engine.** Petrifying Bite, melee, +3, reach 5 ft, 1d4+1 piercing

| | |
|---|---|
| SRD block | Cockatrice |
| Type | Small Monstrosity, Unaligned |
| AC | 11 |
| Initiative | +1 |
| HP | 22 (5d6 + 5) |
| Speed | 20 ft., Fly 40 ft. |
| Abilities | STR 6 (-2), DEX 12 (+1), CON 12 (+1), INT 2 (-4), WIS 13 (+1), CHA 5 (-3) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Immunities | Petrified |
| Senses | Darkvision 60 ft.; Passive Perception 11 |
| Languages | None |

**Wants.** It wants a statue.

**Cheese.** Don't let it peck the front liner twice. Stone is a condition, not a joke.

**Tactics.** Peck and flutter back to the rack.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Petrifying Chicken-Lizard. Level 1. Unit.

**[GM]** It is not a chicken. The chicken did not petrify your friend.

### Attacks

- **Petrifying Bite.** Melee Attack Roll: +3, reach 5 ft. Hit: 3 (1d4 + 1) Piercing damage. If the target is a creature, it is subjected to the following effect. Constitution Saving Throw: DC 11. First Failure: The target has the Restrained condition. The target repeats the save at the end of its next turn if it is still Restrained, ending the effect on itself on a success. Second Failure: The target has the Petrified condition, instead of the Restrained condition, for 24 hours

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Motorcycle-Sized Usher Wasp

`f02-u-03` · unit · Motorcycle-Sized Usher Wasp. Level 1. "Seating, but airborne."

**Picture.** A wasp the size of a motorcycle, stuffed into an usher vest, stinger first.

**Engine.** Sting, melee, +4, reach 5 ft, 1d6+2 piercing, plus 2d4 poison

| | |
|---|---|
| SRD block | Giant Wasp |
| Type | Medium Beast, Unaligned |
| AC | 13 |
| Initiative | +2 |
| HP | 22 (5d8) |
| Speed | 10 ft., Fly 50 ft. |
| Abilities | STR 10 (+0), DEX 14 (+2), CON 10 (+0), INT 1 (-5), WIS 10 (+0), CHA 3 (-4) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Senses | Passive Perception 10 |
| Languages | None |

**Wants.** It wants a sting that stays.

**Cheese.** Swat it before the poison stacks with a second usher.

**Tactics.** Dive, sting, climb.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Motorcycle-Sized Usher Wasp. Level 1. Unit.

**[GM]** Your seat is wherever it stings you.

### Traits

- **Flyby.** The wasp doesn’t provoke an Opportunity Attack when it flies out of an enemy’s reach

### Attacks

- **Sting.** Melee Attack Roll: +4, reach 5 ft. Hit: 5 (1d6 + 2) Piercing damage plus 5 (2d4) Poison damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Bouncer Ape Named Grip

`f02-u-04` · unit · Bouncer Ape Named Grip. Level 1. "Stagehand. Literal."

**Picture.** An ape at the velvet rope. The name tag says GRIP. The fists already agreed.

**Engine.** Multiattack: 2 x Fist; Fist, melee, +5, reach 5 ft, 1d4+3 bludgeoning; Rock (Recharge 6), ranged, +5, range 25/50 ft, 2d6+3 bludgeoning, recharge 6

| | |
|---|---|
| SRD block | Ape |
| Type | Medium Beast, Unaligned |
| AC | 12 |
| Initiative | +2 |
| HP | 19 (3d8 + 6) |
| Speed | 30 ft., Climb 30 ft. |
| Abilities | STR 16 (+3), DEX 14 (+2), CON 14 (+2), INT 6 (-2), WIS 12 (+1), CHA 7 (-2) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Skills | Athletics +5, Perception +3 |
| Senses | Passive Perception 13 |
| Languages | None |

**Wants.** It wants the rigging.

**Cheese.** Don't climb after it. Make it come down.

**Tactics.** Rock from the catwalk, fist if you climb.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Bouncer Ape Named Grip. Level 1. Unit.

**[GM]** The stagehand is union, furry, and holding a rock with your name on it.

### Attacks

- **Multiattack.** The ape makes two Fist attacks
- **Fist.** Melee Attack Roll: +5, reach 5 ft. Hit: 5 (1d4 + 3) Bludgeoning damage.
- **Rock (Recharge 6).** Ranged Attack Roll: +5, range 25/50 ft. Hit: 10 (2d6 + 3) Bludgeoning damage

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Rock** (recharge, max 1). Starts ready. After Rock is used, it is down until a d6 at the start of this creature's turn shows 6–6. It cannot be used every turn.

## Bow-Tie Black Bear

`f02-u-05` · unit · Bow-Tie Black Bear. Level 1. "The door has a policy."

**Picture.** A black bear in a bow tie, checking a list you are not on.

**Engine.** Multiattack: 2 x Rend; Rend, melee, +4, reach 5 ft, 1d6+2 slashing

| | |
|---|---|
| SRD block | Black Bear |
| Type | Medium Beast, Unaligned |
| AC | 11 |
| Initiative | +1 |
| HP | 19 (3d8 + 6) |
| Speed | 30 ft., Climb 30 ft., Swim 30 ft. |
| Abilities | STR 15 (+2), DEX 12 (+1), CON 14 (+2), INT 2 (-4), WIS 12 (+1), CHA 7 (-2) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Skills | Perception +5 |
| Senses | Darkvision 60 ft.; Passive Perception 15 |
| Languages | None |

**Wants.** It wants the threshold.

**Cheese.** Don't shove the door. Lure it off the step.

**Tactics.** They hold the door square. Two of them means a wall.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Bow-Tie Black Bear. Level 1. Unit.

**[GM]** No shoes, no shirt, no surviving the door.

### Attacks

- **Multiattack.** The bear makes two Rend attacks
- **Rend.** Melee Attack Roll: +4, reach 5 ft. Hit: 5 (1d6 + 2) Slashing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Decorative Tank Shark

`f02-u-06` · unit · Decorative Tank Shark. Level 1. "Sponsored by the aquarium."

**Picture.** A reef shark in the lobby aquarium. The glass is a suggestion it has not accepted.

**Engine.** Bite, melee, +4, reach 5 ft, 2d4+2 piercing

| | |
|---|---|
| SRD block | Reef Shark |
| Type | Medium Beast, Unaligned |
| AC | 12 |
| Initiative | +2 |
| HP | 22 (4d8 + 4) |
| Speed | 5 ft., Swim 30 ft. |
| Abilities | STR 14 (+2), DEX 15 (+2), CON 13 (+1), INT 1 (-5), WIS 10 (+0), CHA 4 (-3) |
| CR | 1/2 |
| XP | 100 |
| PB | +2 |
| Skills | Perception +2 |
| Senses | Blindsight 30 ft.; Passive Perception 12 |
| Languages | None |

**Wants.** It wants blood in the water.

**Cheese.** Stay out of the tank. This is not a puzzle if you can read.

**Tactics.** They only fight in the water.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Decorative Tank Shark. Level 1. Unit.

**[GM]** The exhibit is closed. The exhibit disagrees.

### Traits

- **Pack Tactics.** The shark has Advantage on an attack roll against a creature if at least one of the shark’s allies is within 5 feet of the creature and the ally doesn’t have the Incapacitated condition
- **Water Breathing.** The shark can breathe only underwater

### Attacks

- **Bite.** Melee Attack Roll: +4, reach 5 ft. Hit: 7 (2d4 + 2) Piercing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Headset Shoulder Devil

`f02-e-01` · elite · Headset Shoulder Devil. Level 1. "Notes from the booth."

**Picture.** A tiny red devil on a shoulder, wearing a producer headset, offering a deal that is already bad.

**Engine.** Sting, melee, +5, reach 5 ft, 1d6+3 piercing, plus 2d6 poison; Invisibility; Shape-Shift

| | |
|---|---|
| SRD block | Imp |
| Type | Tiny Fiend (Devil), Lawful Evil |
| AC | 13 |
| Initiative | +3 |
| HP | 21 (6d4 + 6) |
| Speed | 20 ft., Fly 40 ft. |
| Abilities | STR 6 (-2), DEX 17 (+3), CON 13 (+1), INT 11 (+0), WIS 12 (+1), CHA 14 (+2) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Skills | Deception +4, Insight +3, Stealth +5 |
| Resistances | Cold |
| Immunities | Fire, Poison; Poisoned |
| Senses | Darkvision 120 ft. (unimpeded by magical Darkness); Passive Perception 11 |
| Languages | Common, Infernal |

**Wants.** It wants the fight to go badly on camera.

**Cheese.** Detect it. Invisibility is the whole career.

**Tactics.** Sting from invisibility, then fly to the lights.

**Reskin.** None.

**House check.** Invisibility is an at-will action printed with no daily cap. It is not a spell slot. Do not add slots.

**[SYSTEM]** Headset Shoulder Devil. Level 1. Elite. Fiend.

**[GM]** A little red executive with a stinger and a note about your lighting.

### Traits

- **Magic Resistance.** The imp has Advantage on saving throws against spells and other magical effects

### Attacks

- **Sting.** Melee Attack Roll: +5, reach 5 ft. Hit: 6 (1d6 + 3) Piercing damage plus 7 (2d6) Poison damage
- **Invisibility.** The imp casts Invisibility on itself, requiring no spell components and using Charisma as the spellcasting ability
- **Shape-Shift.** The imp shape-shifts to resemble a rat (Speed 20 ft.), a raven (20 ft., Fly 60 ft.), or a spider (20 ft., Climb 20 ft.), or it returns to its true form. Its game statistics are the same in each form, except for its Speed. Any equipment it is wearing or carrying isn’t transformed

### Tracked uses

These are at-will. They are not spell slots. Do not add a daily cap the block does not print.

- **Invisibility** (at_will_innate, no cap (at will), spell level 2). Printed as an action with no daily cap. Not a spell slot. Do not add slots.

## Golf-Cart Security Wolf

`f02-e-02` · elite · Golf-Cart Security Wolf. Level 1. "The good boy left."

**Picture.** A wolf bigger than the couch wolf, on a security contract, with the night shift's attitude.

**Engine.** Bite, melee, +5, reach 5 ft, 1d10+3 piercing

| | |
|---|---|
| SRD block | Dire Wolf |
| Type | Large Beast, Unaligned |
| AC | 14 |
| Initiative | +2 |
| HP | 22 (3d10 + 6) |
| Speed | 50 ft. |
| Abilities | STR 17 (+3), DEX 15 (+2), CON 15 (+2), INT 3 (-4), WIS 12 (+1), CHA 7 (-2) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Skills | Perception +5, Stealth +4 |
| Senses | Darkvision 60 ft.; Passive Perception 15 |
| Languages | None |

**Wants.** It wants a prone Crawler.

**Cheese.** Don't let it knock the front rank. Spears set against a charge.

**Tactics.** Charge, bite, stand on them.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Golf-Cart Security Wolf. Level 1. Elite.

**[GM]** Security is a wolf the size of a couch. Pet at your own funeral.

### Traits

- **Pack Tactics.** The wolf has Advantage on an attack roll against a creature if at least one of the wolf’s allies is within 5 feet of the creature and the ally doesn’t have the Incapacitated condition

### Attacks

- **Bite.** Melee Attack Roll: +5, reach 5 ft. Hit: 8 (1d10 + 3) Piercing damage. If the target is a Large or smaller creature, it has the Prone condition

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Marquee Bird-Woman

`f02-e-03` · elite · Marquee Bird-Woman. Level 1. "Song, then the drop."

**Picture.** A woman with vulture wings on the marquee. Her song walks your feet off the catwalk.

**Engine.** Claw, melee, +3, reach 5 ft, 2d4+1 slashing; Luring Song, Wisdom DC 11

| | |
|---|---|
| SRD block | Harpy |
| Type | Medium Monstrosity, Chaotic Evil |
| AC | 11 |
| Initiative | +1 |
| HP | 38 (7d8 + 7) |
| Speed | 20 ft., Fly 40 ft. |
| Abilities | STR 12 (+1), DEX 13 (+1), CON 12 (+1), INT 7 (-2), WIS 10 (+0), CHA 13 (+1) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Senses | Passive Perception 10 |
| Languages | Common |

**Wants.** It wants you walking off the catwalk.

**Cheese.** Plug ears. Kill the song before the ledge.

**Tactics.** Luring song, then claws on whoever obeyed.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Marquee Bird-Woman. Level 1. Elite.

**[GM]** She hits the high note. You hit the floor.

### Attacks

- **Claw.** Melee Attack Roll: +3, reach 5 ft. Hit: 6 (2d4 + 1) Slashing damage
- **Luring Song.** The harpy sings a magical melody, which lasts until the harpy’s Concentration ends on it. Wisdom Saving Throw: DC 11, each Humanoid and Giant in a 300-foot Emanation originating from the harpy when the song starts. Failure: The target has the Charmed condition until the song ends and repeats the save at the end of each of its turns. While Charmed, the target has the Incapacitated condition and ignores the Luring Song of other harpies. If the target is more than 5 feet from the harpy, the target moves on its turn toward the harpy by the most direct route, trying to get within 5 feet of the harpy. It doesn’t avoid Opportunity Attacks; however, before moving into damaging terrain (such as lava or a pit) and whenever it takes damage from a source other than the harpy, the target repeats the save. Success: The target is immune to this harpy’s Luring Song for 24 hours

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Swooping Stone Security Camera

`f02-e-04` · elite · Swooping Stone Security Camera. Level 2. "The statue was the shot."

**Picture.** A stone statue carved like a security camera. It sits still, then it dives.

**Engine.** Multiattack: 2 x Claw; Claw, melee, +4, reach 5 ft, 2d4+2 slashing

| | |
|---|---|
| SRD block | Gargoyle |
| Type | Medium Elemental, Chaotic Evil |
| AC | 15 |
| Initiative | +2 |
| HP | 67 (9d8 + 27) |
| Speed | 30 ft., Fly 60 ft. |
| Abilities | STR 15 (+2), DEX 11 (+0), CON 16 (+3), INT 6 (-2), WIS 11 (+0), CHA 7 (-2) |
| CR | 2 |
| XP | 450 |
| PB | +2 |
| Skills | Stealth +4 |
| Immunities | Poison; Exhaustion, Petrified, Poisoned |
| Senses | Darkvision 60 ft.; Passive Perception 10 |
| Languages | Primordial (Terran) |

**Wants.** It wants a still picture of a still Crawler.

**Cheese.** Don't rest under the stone faces. False appearance is the ambush.

**Tactics.** Dive, claw, back to the perch.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Swooping Stone Security Camera. Level 2. Elite.

**[GM]** Smile. The architecture is filming, and it has claws.

### Traits

- **Flyby.** The gargoyle doesn’t provoke an Opportunity Attack when it flies out of an enemy’s reach

### Attacks

- **Multiattack.** The gargoyle makes two Claw attacks
- **Claw.** Melee Attack Roll: +4, reach 5 ft. Hit: 7 (2d4 + 2) Slashing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Ten-Foot Cube of Floor Cleaner

`f02-e-05` · elite · Ten-Foot Cube of Floor Cleaner. Level 2. "It cleans by deletion."

**Picture.** A transparent cube of janitor jelly, ten feet on a side, with old mops floating in it. It moves. You do not want to be inside.

**Engine.** Pseudopod, melee, +4, reach 5 ft, 3d6+2 acid; Engulf, Dexterity DC 12, 3d6 acid

| | |
|---|---|
| SRD block | Gelatinous Cube |
| Type | Large Ooze, Unaligned |
| AC | 6 |
| Initiative | -4 |
| HP | 63 (6d10 + 30) |
| Speed | 15 ft. |
| Abilities | STR 14 (+2), DEX 3 (-4), CON 20 (+5), INT 1 (-5), WIS 6 (-2), CHA 1 (-5) |
| CR | 2 |
| XP | 450 |
| PB | +2 |
| Immunities | Acid; Blinded, Charmed, Deafened, Exhaustion, Frightened, Prone |
| Senses | Blindsight 60 ft.; Passive Perception 8 |
| Languages | None |

**Wants.** It wants the hallway full.

**Cheese.** Side passages. Don't walk the obvious clean hall.

**Tactics.** Engulf the one who didn't look down.

**Reskin.** None. Transparent as printed.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Ten-Foot Cube of Floor Cleaner. Level 2. Elite. Ooze.

**[GM]** The hallway looks clean because the hallway ate the mess. You are mess.

### Traits

- **Ooze Cube.** The cube fills its entire space and is transparent. Other creatures can enter that space, but a creature that does so is subjected to the cube’s Engulf and has Disadvantage on the saving throw. Creatures inside the cube have Total Cover, and the cube can hold one Large creature or up to four Medium or Small creatures inside itself at a time. As an action, a creature within 5 feet of the cube can pull a creature or an object out of the cube by succeeding on a DC 12 Strength (Athletics) check, and the puller takes 10 (3d6) Acid damage
- **Transparent.** Even when the cube is in plain sight, a creature must succeed on a DC 15 Wisdom (Perception) check to notice the cube if the creature hasn’t witnessed the cube move or otherwise act

### Attacks

- **Pseudopod.** Melee Attack Roll: +4, reach 5 ft. Hit: 12 (3d6 + 2) Acid damage
- **Engulf.** The cube moves up to its Speed without provoking Opportunity Attacks. The cube can move through the spaces of Large or smaller creatures if it has room inside itself to contain them (see the Ooze Cube trait). Dexterity Saving Throw: DC 12, each creature whose space the cube enters for the first time during this move. Failure: 10 (3d6) Acid damage, and the target is engulfed. An engulfed target is suffocating, can’t cast spells with a Verbal component, has the Restrained condition, and takes 10 (3d6) Acid damage at the start of each of the cube’s turns. When the cube moves, the engulfed target moves with it. An engulfed target can try to escape by taking an action to make a DC 12 Strength (Athletics) check. On a successful check, the target escapes and enters the nearest unoccupied space. Success: Half damage, and the target moves to an unoccupied space within 5 feet of the cube. If there is no unoccupied space, the target fails the save instead

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Fire-Breathing Exit Dog

`f02-b-01` · boss · Fire-Breathing Exit Dog. Level 3. Boss. "The focus group is on fire."

**Picture.** A big black dog. Its bark is a cone of fire down the hallway. The exit sign is not a suggestion.

**Engine.** Multiattack: 2 x Bite; Bite, melee, +5, reach 5 ft, 1d8+3 piercing, plus 1d6 fire; Fire Breath (Recharge 5–6), Dexterity DC 12, 5d6 fire, recharge 5-6

| | |
|---|---|
| SRD block | Hell Hound |
| Type | Medium Fiend, Lawful Evil |
| AC | 15 |
| Initiative | +1 |
| HP | 58 (9d8 + 18) |
| Speed | 50 ft. |
| Abilities | STR 17 (+3), DEX 12 (+1), CON 14 (+2), INT 6 (-2), WIS 13 (+1), CHA 6 (-2) |
| CR | 3 |
| XP | 700 |
| PB | +2 |
| Skills | Perception +5 |
| Immunities | Fire |
| Senses | Darkvision 60 ft.; Passive Perception 15 |
| Languages | Understands Infernal but can’t speak |

**Wants.** It wants a cone of the whole party.

**Cheese.** Split the cone. Don't line up for the breath.

**Tactics.** Breath when two or more stand together. Bite the scout.

**Reskin.** Fire breath unchanged.

**House check.** Fire Breath is recharge 5–6. One breath, then it is down until the die hits. Bite still works.

**[SYSTEM]** Fire-Breathing Exit Dog. Level 3. Boss. Fiend.

**[GM]** The audience wanted heat. The hound took that personally.

### Traits

- **Pack Tactics.** The hound has Advantage on an attack roll against a creature if at least one of the hound’s allies is within 5 feet of the creature and the ally doesn’t have the Incapacitated condition

### Attacks

- **Multiattack.** The hound makes two Bite attacks
- **Bite.** Melee Attack Roll: +5, reach 5 ft. Hit: 7 (1d8 + 3) Piercing damage plus 3 (1d6) Fire damage.
- **Fire Breath (Recharge 5–6).** Dexterity Saving Throw: DC 12, each creature in a 15-foot Cone. Failure: 17 (5d6) Fire damage. Success: Half damage

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Fire Breath** (recharge, max 1). Starts ready. After Fire Breath is used, it is down until a d6 at the start of this creature's turn shows 5–6. It cannot be used every turn.

## Occupied Owl-Bear Mascot

`f02-b-02` · boss · Occupied Owl-Bear Mascot. Level 3. Boss. "The costume filled in."

**Picture.** An owl's head on a bear's body, and it is not a costume. The beak and the hug both count.

**Engine.** Multiattack: 2 x Rend; Rend, melee, +7, reach 5 ft, 2d8+5 slashing

| | |
|---|---|
| SRD block | Owlbear |
| Type | Large Monstrosity, Unaligned |
| AC | 13 |
| Initiative | +1 |
| HP | 59 (7d10 + 21) |
| Speed | 40 ft., Climb 40 ft. |
| Abilities | STR 20 (+5), DEX 12 (+1), CON 17 (+3), INT 3 (-4), WIS 12 (+1), CHA 7 (-2) |
| CR | 3 |
| XP | 700 |
| PB | +2 |
| Skills | Perception +5 |
| Senses | Darkvision 60 ft.; Passive Perception 15 |
| Languages | None |

**Wants.** It wants a hug that is a maul.

**Cheese.** Kite it. Don't stand in the hug.

**Tactics.** Multiattack the nearest.

**Reskin.** None.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Occupied Owl-Bear Mascot. Level 3. Boss.

**[GM]** Hug the mascot, the poster said. The poster is evidence.

### Attacks

- **Multiattack.** The owlbear makes two Rend attacks
- **Rend.** Melee Attack Roll: +7 , reach 5 ft. Hit: 14 (2d8 + 5) Slashing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Rental-Plate Sponsor Knight

`f02-b-03` · boss · Rental-Plate Sponsor Knight. Level 3. Boss. "Ribbon-cutting with a real sword."

**Picture.** A knight in full plate with a sponsor logo on the breastplate and a renaissance-faire lance.

**Engine.** Multiattack: The knight makes two attacks, using Greatsword or Heavy Crossbow in any combination; Greatsword, melee, +5, reach 5 ft, 2d6+3 slashing, plus 1d8 radiant; Heavy Crossbow, ranged, +2, range 100/400 ft, 2d10 piercing, plus 1d8 radiant; Parry

| | |
|---|---|
| SRD block | Knight |
| Type | Medium or Small Humanoid, Neutral |
| AC | 18 |
| Initiative | +0 |
| HP | 52 (8d8 + 16) |
| Speed | 30 ft. |
| Abilities | STR 16 (+3), DEX 11 (+0), CON 14 (+2), INT 11 (+0), WIS 11 (+0), CHA 15 (+2) |
| CR | 3 |
| XP | 700 |
| PB | +2 |
| Gear | Greatsword, Heavy Crossbow, Plate Armor |
| Immunities | Frightened |
| Senses | Passive Perception 10 |
| Languages | Common plus one other language |

**Wants.** It wants a duel on the stage.

**Cheese.** Don't duel. Swarm, or drop the stage lights. The knight wants honor. Decline.

**Tactics.** Leadership if any unit remains, then the sword.

**Reskin.** None. Leadership is already on the block.

**House check.** House set dressing. The Floor 2 reserve canon table was not used. Numbers stay the SRD block.

**[SYSTEM]** Rental-Plate Sponsor Knight. Level 3. Boss.

**[GM]** They sent a knight to cut a ribbon. The ribbon is you.

### Attacks

- **Multiattack.** The knight makes two attacks, using Greatsword or Heavy Crossbow in any combination
- **Greatsword.** Melee Attack Roll: +5, reach 5 ft. Hit: 10 (2d6 + 3) Slashing damage plus 4 (1d8) Radiant damage
- **Heavy Crossbow.** Ranged Attack Roll: +2, range 100/400 ft. Hit: 11 (2d10) Piercing damage plus 4 (1d8) Radiant damage

### Reactions

- **Parry.** Trigger: The knight is hit by a melee attack roll while holding a weapon. Response: The knight adds 2 to its AC against that attack, possibly causing it to miss.

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.


# Floor 3 — Continuum, rural

Twenty-day clock (decision 026). Gold boxes can exist from Floor 3. No Platinum on Floors 1–8. Road, fence, and silo are house set dressing. A Long Rest finishes in a saferoom (core saferoom overlay). Live Day pages win if a card disagrees.

## Eyeless Cave Person

`f03-m-01` · mob · Eyeless Cave Person. Level 1. "The rural road does not need eyes."

**Picture.** A pale person with no eyes, a stone club, and ears that already know where you stepped.

**Engine.** Bone Cudgel, melee, +5, reach 5 ft, 1d6+3 bludgeoning, plus 1d4 psychic

| | |
|---|---|
| SRD block | Grimlock |
| Type | Medium Aberration, Neutral Evil |
| AC | 11 |
| Initiative | +1 |
| HP | 11 (2d8 + 2) |
| Speed | 30 ft., Climb 30 ft. |
| Abilities | STR 16 (+3), DEX 12 (+1), CON 12 (+1), INT 9 (-1), WIS 8 (-1), CHA 6 (-2) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Skills | Athletics +5, Perception +3, Stealth +5 |
| Senses | Blindsight 30 ft.; Passive Perception 13 |
| Languages | None |

**Wants.** It wants the blind corner.

**Cheese.** Light and noise. They hunt by hearing.

**Tactics.** Ambush from the ditch.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Eyeless Cave Person. Level 1. Blind and armed.

**[GM]** No eyes. Plenty of axe. The countryside is not quaint.

### Attacks

- **Bone Cudgel.** Melee Attack Roll: +5, reach 5 ft. Hit: 6 (1d6 + 3) Bludgeoning damage plus 2 (1d4) Psychic damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Stinking Demon Intern

`f03-m-02` · mob · Stinking Demon Intern. Level 1. "Harvest help from a worse place."

**Picture.** A small, soggy, awful-smelling demon. Bottom of the org chart. The smell arrives first.

**Engine.** Rend, melee, +3, reach 5 ft, 1d6+1 slashing; Fetid Cloud (1/Day), Constitution DC 11

| | |
|---|---|
| SRD block | Dretch |
| Type | Small Fiend (Demon), Chaotic Evil |
| AC | 11 |
| Initiative | +0 |
| HP | 18 (4d6 + 4) |
| Speed | 20 ft. |
| Abilities | STR 12 (+1), DEX 11 (+0), CON 12 (+1), INT 5 (-3), WIS 8 (-1), CHA 3 (-4) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Resistances | Cold, Fire, Lightning |
| Immunities | Poison; Poisoned |
| Senses | Darkvision 60 ft.; Passive Perception 9 |
| Languages | Abyssal; telepathy 60 ft. (works only with creatures that understand Abyssal) |

**Wants.** It wants a crowd.

**Cheese.** They are weak alone. Don't let the cloud gather.

**Tactics.** Fetch and claw. They stink as a group.

**Reskin.** None.

**House check.** Fetid Cloud is once per day. It is not a slot that refills when the cloud ends.

**[SYSTEM]** Stinking Demon Intern. Level 1. Fiend.

**[GM]** Farm labor, imported. The import smell arrives first.

### Attacks

- **Rend.** Melee Attack Roll: +3, reach 5 ft. Hit: 4 (1d6 + 1) Slashing damage.
- **Fetid Cloud (1/Day).** Constitution Saving Throw: DC 11, each creature in a 10-foot Emanation originating from the dretch. Failure: The target has the Poisoned condition until the end of its next turn. While Poisoned, the creature can take either an action or a Bonus Action on its turn, not both, and it can’t take Reactions

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Fetid Cloud** (daily, max 1). 1 use(s) per day, shared by this ability, not per target and not per round. At 0 it does not fire again until a Long Rest in a saferoom.

## Fence-Hopping Teleport Dog

`f03-m-03` · mob · Fence-Hopping Teleport Dog. Level 1. "The property line moves."

**Picture.** A dog that vanishes on one side of the fence and bites you on the other.

**Engine.** Bite, melee, +5, reach 5 ft, 1d4+3 piercing; Teleport (Recharge 4–6), recharge 4-6

| | |
|---|---|
| SRD block | Blink Dog |
| Type | Medium Fey, Lawful Good |
| AC | 13 |
| Initiative | +3 |
| HP | 22 (4d8 + 4) |
| Speed | 40 ft. |
| Abilities | STR 12 (+1), DEX 17 (+3), CON 12 (+1), INT 10 (+0), WIS 13 (+1), CHA 11 (+0) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Skills | Perception +5, Stealth +5 |
| Senses | Darkvision 60 ft.; Passive Perception 15 |
| Languages | Blink Dog; understands Elvish and Sylvan but can’t speak them |

**Wants.** It wants you on the wrong side of the fence.

**Cheese.** Ready an attack for when it blinks back.

**Tactics.** Bite, blink, bite.

**Reskin.** None.

**House check.** Teleport is recharge 4–6. It is not a spell slot.

**[SYSTEM]** Fence-Hopping Teleport Dog. Level 1. Fey.

**[GM]** Good dog. Bad jurisdiction.

### Attacks

- **Bite.** Melee Attack Roll: +5, reach 5 ft. Hit: 5 (1d4 + 3) Piercing damage

### Bonus actions

- **Teleport (Recharge 4–6).** The dog teleports up to 40 feet to an unoccupied space it can see.

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Teleport** (recharge, max 1). Starts ready. After Teleport is used, it is down until a d6 at the start of this creature's turn shows 4–6. It cannot be used every turn.

## Cat-Sized Shoulder Dragon

`f03-m-04` · mob · Cat-Sized Shoulder Dragon. Level 1. "A tiny dragon with notes."

**Picture.** A dragon the size of a cat, usually on someone's shoulder, judging your build out loud.

**Engine.** Multiattack: 2 x Bite; Bite, melee, +4, reach 5 ft, 1d4+2 piercing; Sting, Constitution DC 12, 2d4 poison

| | |
|---|---|
| SRD block | Pseudodragon |
| Type | Tiny Dragon, Neutral Good |
| AC | 14 |
| Initiative | +2 |
| HP | 10 (3d4 + 3) |
| Speed | 15 ft., Fly 60 ft. |
| Abilities | STR 6 (-2), DEX 15 (+2), CON 13 (+1), INT 10 (+0), WIS 12 (+1), CHA 10 (+0) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Skills | Perception +5, Stealth +4 |
| Senses | Blindsight 10 ft., Darkvision 60 ft.; Passive Perception 15 |
| Languages | Understands Common and Draconic but can’t speak |

**Wants.** It wants you stung and embarrassed.

**Cheese.** It is small. Don't chase it into the loft alone.

**Tactics.** Sting from the rafters, then hide.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Cat-Sized Shoulder Dragon. Level 1. Dragon.

**[GM]** Two stars. Would sting again.

### Traits

- **Magic Resistance.** The pseudodragon has Advantage on saving throws against spells and other magical effects

### Attacks

- **Multiattack.** The pseudodragon makes two Bite attacks
- **Bite.** Melee Attack Roll: +4, reach 5 ft. Hit: 4 (1d4 + 2) Piercing damage
- **Sting.** Constitution Saving Throw: DC 12, one creature the pseudodragon can see within 5 feet. Failure: 5 (2d4) Poison damage, and the target has the Poisoned condition for 1 hour. Failure by 5 or More: While Poisoned, the target also has the Unconscious condition, which ends early if the target takes damage or a creature within 5 feet of it takes an action to wake it

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Purple Whip-Crop Fungus

`f03-m-05` · mob · Purple Whip-Crop Fungus. Level 1. "The field planted back."

**Picture.** A violet fungus planted in a crop row. The stalks are whips. Do not harvest it.

**Engine.** Multiattack: 2 x Rotting Touch; Rotting Touch, melee, +2, reach 10 ft, 1d8 necrotic

| | |
|---|---|
| SRD block | Violet Fungus |
| Type | Medium Plant, Unaligned |
| AC | 5 |
| Initiative | -5 |
| HP | 18 (4d8) |
| Speed | 5 ft. |
| Abilities | STR 3 (-4), DEX 1 (-5), CON 10 (+0), INT 1 (-5), WIS 3 (-4), CHA 1 (-5) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Immunities | Blinded, Charmed, Deafened, Frightened |
| Senses | Blindsight 30 ft.; Passive Perception 6 |
| Languages | None |

**Wants.** It wants you in the patch.

**Cheese.** Don't walk the purple rows. Ranged, or burn the patch.

**Tactics.** It does not chase past the crop.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Purple Whip-Crop Fungus. Level 1. Plant.

**[GM]** Do not eat the pretty ones. The pretty ones eat.

### Attacks

- **Multiattack.** The fungus makes two Rotting Touch attacks
- **Rotting Touch.** Melee Attack Roll: +2, reach 10 ft. Hit: 4 (1d8) Necrotic damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Hatchet-Faced Ostrich

`f03-m-06` · mob · Hatchet-Faced Ostrich. Level 1. "The poultry is a weapon."

**Picture.** A bird the size of an ostrich. The beak is an axe. It runs you down like you are the lawn.

**Engine.** Beak, melee, +4, reach 5 ft, 1d8+2 slashing

| | |
|---|---|
| SRD block | Axe Beak |
| Type | Large Monstrosity, Unaligned |
| AC | 11 |
| Initiative | +1 |
| HP | 19 (3d10 + 3) |
| Speed | 50 ft. |
| Abilities | STR 14 (+2), DEX 12 (+1), CON 12 (+1), INT 2 (-4), WIS 10 (+0), CHA 5 (-3) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Senses | Passive Perception 10 |
| Languages | None |

**Wants.** It wants a sprint.

**Cheese.** A fence. They are fast and stupid.

**Tactics.** Charge in a straight line.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Hatchet-Faced Ostrich. Level 1.

**[GM]** Free range. The range includes your ribs.

### Attacks

- **Beak.** Melee Attack Roll: +4, reach 5 ft. Hit: 6 (1d8 + 2) Slashing damage.

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Hang-Glider Mail Lizard

`f03-m-07` · mob · Hang-Glider Mail Lizard. Level 1. "Mail, delivered downward."

**Picture.** A flying lizard with a mail satchel, dive-bombing the road like the package is you.

**Engine.** Bite, melee, +4, reach 5 ft, 1d8+2 piercing

| | |
|---|---|
| SRD block | Pteranodon |
| Type | Medium Beast (Dinosaur), Unaligned |
| AC | 13 |
| Initiative | +2 |
| HP | 13 (3d8) |
| Speed | 10 ft., Fly 60 ft. |
| Abilities | STR 12 (+1), DEX 15 (+2), CON 10 (+0), INT 2 (-4), WIS 9 (-1), CHA 5 (-3) |
| CR | 1/4 |
| XP | 50 |
| PB | +2 |
| Skills | Perception +1 |
| Senses | Passive Perception 11 |
| Languages | None |

**Wants.** It wants a grab from above.

**Cheese.** Get under the eaves. Don't cross the open yard.

**Tactics.** Dive, snatch, climb.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Hang-Glider Mail Lizard. Level 1.

**[GM]** The mail is late because the mail is a mouth.

### Traits

- **Flyby.** The pteranodon doesn’t provoke an Opportunity Attack when it flies out of an enemy’s reach

### Attacks

- **Bite.** Melee Attack Roll: +4, reach 5 ft. Hit: 6 (1d8 + 2) Piercing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Two-Headed Junkyard Dog

`f03-m-08` · mob · Two-Headed Junkyard Dog. Level 1. "Two heads, one opinion."

**Picture.** One body, two heads, both of them mad, both of them biting.

**Engine.** Multiattack: 2 x Bite; Bite, melee, +4, reach 5 ft, 1d4+2 piercing

| | |
|---|---|
| SRD block | Two-Headed Junkyard Dog |
| Type | Medium Monstrosity, Neutral Evil |
| AC | 12 |
| Initiative | +2 |
| HP | 39 (6d8 + 12) |
| Speed | 40 ft. |
| Abilities | STR 15 (+2), DEX 14 (+2), CON 14 (+2), INT 3 (-4), WIS 13 (+1), CHA 6 (-2) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Skills | Perception +5, Stealth +4 |
| Immunities | Blinded, Charmed, Deafened, Frightened, Stunned, Unconscious |
| Senses | Darkvision 120 ft.; Passive Perception 15 |
| Languages | None |

**Wants.** It wants a bite that rots.

**Cheese.** Don't let both heads get a turn on the same Crawler if you can drop it fast.

**Tactics.** Two bites. Disease is the leftover.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Two-Headed Junkyard Dog. Level 1.

**[GM]** Pet one head. The other head files a complaint in your blood.

### Attacks

- **Multiattack.** The death dog makes two Bite attacks
- **Bite.** Melee Attack Roll: +4, reach 5 ft. Hit: 4 (1d4 + 2) Piercing damage. If the target is a creature, it is subjected to the following effect. Constitution Saving Throw: DC 12. First Failure: The target has the Poisoned condition. While Poisoned, the target’s Hit Point maximum doesn’t return to normal when finishing a Long Rest, and it repeats the save every 24 hours that elapse, ending the effect on itself on a success. Subsequent Failures: The Poisoned target’s Hit Point maximum decreases by 5 (1d10)

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Invisible Clipboard Gremlin

`f03-m-09` · mob · Invisible Clipboard Gremlin. Level 1. "Here about the books."

**Picture.** A tiny demon you cannot see, holding a clipboard, poisoning whatever you were about to drink.

**Engine.** Rend, melee, +5, reach 5 ft, 1d4+3 slashing; Invisibility; Scare (1/Day), Wisdom DC 10; Shape-Shift

| | |
|---|---|
| SRD block | Quasit |
| Type | Tiny Fiend (Demon), Chaotic Evil |
| AC | 13 |
| Initiative | +3 |
| HP | 25 (10d4) |
| Speed | 40 ft. |
| Abilities | STR 5 (-3), DEX 17 (+3), CON 10 (+0), INT 7 (-2), WIS 10 (+0), CHA 10 (+0) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Skills | Stealth +5 |
| Resistances | Cold, Fire, Lightning |
| Immunities | Poison; Poisoned |
| Senses | Darkvision 120 ft.; Passive Perception 10 |
| Languages | Abyssal, Common |

**Wants.** It wants fear and a ruined scare.

**Cheese.** See invisibility or just hold the doorway. It is fragile.

**Tactics.** Scare, turn invisible, claw the frightened.

**Reskin.** None.

**House check.** Invisibility is an at-will action, not a slot. Scare is once per day, Wisdom DC 10. At 0 Scare, claws and Invisibility remain.

**[SYSTEM]** Invisible Clipboard Gremlin. Level 1. Fiend.

**[GM]** It has a clipboard and a tail. Only one of those is standard.

### Traits

- **Magic Resistance.** The quasit has Advantage on saving throws against spells and other magical effects

### Attacks

- **Rend.** Melee Attack Roll: +5, reach 5 ft. Hit: 5 (1d4 + 3) Slashing damage, and the target has the Poisoned condition until the start of the quasit’s next turn
- **Invisibility.** The quasit casts Invisibility on itself, requiring no spell components and using Charisma as the spellcasting ability.
- **Scare (1/Day).** Wisdom Saving Throw: DC 10, one creature within 20 feet. Failure: The target has the Frightened condition. At the end of each of its turns, the target repeats the save, ending the effect on itself on a success. After 1 minute, it succeeds automatically
- **Shape-Shift.** The quasit shape-shifts to resemble a bat (Speed 10 ft., Fly 40 ft.), a centipede (40 ft., Climb 40 ft.), or a toad (40 ft., Swim 40 ft.), or it returns to its true form. Its game statistics are the same in each form, except for its Speed. Any equipment it is wearing or carrying isn’t transformed

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Scare** (daily_spell, max 1). Once per day. Wisdom save DC 10. At 0, do not use Scare.
- **Invisibility** (at_will_innate, no cap (at will), spell level 2). Printed as an action with no daily cap. Not a spell slot. Do not add slots.

## Property-Line Tree Woman

`f03-m-10` · mob · Property-Line Tree Woman. Level 1. "The tree line is staffed."

**Picture.** A woman who is also the tree on the property line. She can step into the trunk. She does not share the yard.

**Engine.** Multiattack: The dryad makes one Vine Lash or Thorn Burst attack, and it can use Spellcasting to cast Charm Monster; Vine Lash, melee, +6, reach 10 ft, 1d8+4 slashing; Thorn Burst, ranged, +6, range 60/60 ft, 1d6+4 piercing; Spellcasting: spend tracked_uses. At-will does not spend.; Tree Stride

| | |
|---|---|
| SRD block | Dryad |
| Type | Medium Fey, Neutral |
| AC | 16 |
| Initiative | +1 |
| HP | 22 (5d8) |
| Speed | 30 ft. |
| Abilities | STR 10 (+0), DEX 12 (+1), CON 11 (+0), INT 14 (+2), WIS 15 (+2), CHA 18 (+4) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Skills | Perception +4, Stealth +5 |
| Senses | Darkvision 60 ft.; Passive Perception 14 |
| Languages | Elvish, Sylvan |

**Wants.** It wants you charmed into the wood.

**Cheese.** Don't follow the voice off the road. Kill the tree bond if you must fight.

**Tactics.** Charm, then the forest does the work.

**Reskin.** None. The tree is the anchor, as printed.

**House check.** Entangle and Pass without Trace are once each per day. Charm Monster is at will but only one charm stays active; casting it again ends the previous one. At 0 on the daily spells, use the vine, the thorns, or the single charm.

**[SYSTEM]** Property-Line Tree Woman. Level 1. Fey.

**[GM]** She offers a shortcut. The shortcut is a stomach.

### Traits

- **Magic Resistance.** The dryad has Advantage on saving throws against spells and other magical effects. Speak with Beasts and Plants. The dryad can communicate with Beasts and Plants as if they shared a language

### Attacks

- **Multiattack.** The dryad makes one Vine Lash or Thorn Burst attack, and it can use Spellcasting to cast Charm Monster
- **Vine Lash.** Melee Attack Roll: +6, reach 10 ft. Hit: 8 (1d8 + 4) Slashing damage
- **Thorn Burst.** Ranged Attack Roll: +6, range 60 ft. Hit: 7 (1d6 + 4) Piercing damage
- **Spellcasting.** The dryad casts one of the following spells, requiring no Material components and using Charisma as the spellcasting ability (spell save DC 14): At Will: Animal Friendship, Charm Monster (lasts 24 hours; ends early if the dryad casts the spell again), Druidcraft 1/Day Each: Entangle, Pass without Trace

### Bonus actions

- **Tree Stride.** If within 5 feet of a Large or bigger tree, the dryad teleports to an unoccupied space within 5 feet of a second Large or bigger tree that is within 60 feet of the previous tree

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Animal Friendship** (at_will, no cap (at will), spell level 1). At will. Not a spell slot. May be repeated. Do not spend a slot for it.
- **Charm Monster** (at_will_single, no cap (at will), spell level 4). Printed at will, and only one charm stays active. Casting it again ends the previous one. Not a slot. Do not stack charms.
- **Druidcraft** (at_will, no cap (at will), spell level 0). At will. Not a spell slot. May be repeated. Do not spend a slot for it.
- **Entangle** (daily_spell, max 1, spell level 1). Once per day for this spell alone (1/Day Each). Not a level-1 slot that refills in the fight. At 0, do not cast it again.
- **Pass without Trace** (daily_spell, max 1, spell level 2). Once per day for this spell alone (1/Day Each). Not a level-2 slot that refills in the fight. At 0, do not cast it again.

## Cutlass Pirate Who Drafts You

`f03-u-01` · unit · Cutlass Pirate Who Drafts You. Level 1. "Rural river, urban morals."

**Picture.** A pirate with a cutlass who is not asking you to join. The press gang already decided.

**Engine.** Multiattack: 2 x Dagger; Dagger, 1d4+3 piercing; Enthralling Panache, Wisdom DC 12

| | |
|---|---|
| SRD block | Pirate |
| Type | Medium or Small Humanoid, Neutral |
| AC | 14 |
| Initiative | +5 |
| HP | 33 (6d8 + 6) |
| Speed | 30 ft. |
| Abilities | STR 10 (+0), DEX 16 (+3), CON 12 (+1), INT 8 (-1), WIS 12 (+1), CHA 14 (+2) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Gear | Daggers (6), Leather Armor |
| Senses | Passive Perception 11 |
| Languages | Common plus one other language |

**Wants.** It wants bodies for the boat.

**Cheese.** Sink the boat problem by not boarding. Fight them on the bank.

**Tactics.** They volley, then board.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Cutlass Pirate Who Drafts You. Level 1. Unit.

**[GM]** The river tax is a person. Decline.

### Attacks

- **Multiattack.** The pirate makes two Dagger attacks. It can replace one attack with a use of Enthralling Panache
- **Dagger.** Melee or Ranged Attack Roll: +5, reach 5 ft. or range 20/60 ft. Hit: 5 (1d4 + 3) Piercing damage
- **Enthralling Panache.** Wisdom Saving Throw: DC 12, one creature the pirate can see within 30 feet. Failure: The target has the Charmed condition until the start of the pirate’s next turn

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Pony-Sized Laughing Hyena

`f03-u-02` · unit · Pony-Sized Laughing Hyena. Level 1. "They laugh on the ridge."

**Picture.** A hyena as big as a pony. One animal. The laugh still sounds like a pack.

**Engine.** Bite, melee, +5, reach 5 ft, 2d6+3 piercing; Rampage (1/Day)

| | |
|---|---|
| SRD block | Giant Hyena |
| Type | Large Beast, Unaligned |
| AC | 12 |
| Initiative | +2 |
| HP | 45 (6d10 + 12) |
| Speed | 50 ft. |
| Abilities | STR 16 (+3), DEX 14 (+2), CON 14 (+2), INT 2 (-4), WIS 12 (+1), CHA 7 (-2) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Skills | Perception +3 |
| Senses | Darkvision 60 ft.; Passive Perception 13 |
| Languages | None |

**Wants.** It wants a runner.

**Cheese.** Don't flee in pieces. A lone Crawler is the meal.

**Tactics.** Rampage the wounded.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Pony-Sized Laughing Hyena. Level 1. Unit.

**[GM]** The laugh is not joy. It is a headcount.

### Attacks

- **Bite.** Melee Attack Roll: +5, reach 5 ft. Hit: 10 (2d6 + 3) Piercing damage

### Bonus actions

- **Rampage (1/Day).** Immediately after dealing damage to a creature that was already Bloodied, the hyena can move up to half its Speed, and it makes one Bite attack.

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Rampage** (daily, max 1). 1 use(s) per day, shared by this ability, not per target and not per round. At 0 it does not fire again until a Long Rest in a saferoom.

## Lawn Lion

`f03-u-03` · unit · Lawn Lion. Level 1. "The green is not a lawn."

**Picture.** A lion on the green, treating the party like slow gazelles who paid for the tour.

**Engine.** Multiattack: 2 x Rend; Rend, melee, +5, reach 5 ft, 1d8+3 slashing; Roar, Wisdom DC 11

| | |
|---|---|
| SRD block | Lion |
| Type | Large Beast, Unaligned |
| AC | 12 |
| Initiative | +2 |
| HP | 22 (4d10) |
| Speed | 50 ft. |
| Abilities | STR 17 (+3), DEX 15 (+2), CON 11 (+0), INT 3 (-4), WIS 12 (+1), CHA 8 (-1) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Skills | Perception +3, Stealth +4 |
| Senses | Darkvision 60 ft.; Passive Perception 13 |
| Languages | None |

**Wants.** It wants a pounce.

**Cheese.** Spears. Don't let the pounce prone the cleric.

**Tactics.** Pounce the back rank if the front opens.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Lawn Lion. Level 1. Unit.

**[GM]** Royal symbol. Actual lion. The symbol bites.

### Traits

- **Pack Tactics.** The lion has Advantage on an attack roll against a creature if at least one of the lion’s allies is within 5 feet of the creature and the ally doesn’t have the Incapacitated condition
- **Running Leap.** With a 10-foot running start, the lion can Long Jump up to 25 feet

### Attacks

- **Multiattack.** The lion makes two Rend attacks. It can replace one attack with a use of Roar
- **Rend.** Melee Attack Roll: +5, reach 5 ft. Hit: 7 (1d8 + 3) Slashing damage
- **Roar.** Wisdom Saving Throw: DC 11, one creature within 15 feet. Failure: The target has the Frightened condition until the start of the lion’s next turn

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Patch-Wearing Brown Bear

`f03-u-04` · unit · Patch-Wearing Brown Bear. Level 1. "The woods have a warden and it is hungry."

**Picture.** A brown bear with a warden patch sewn on. The patch is not a joke. The claws are the fine.

**Engine.** Multiattack: The bear makes one Bite attack and one Claw attack; Bite, melee, +5, reach 5 ft, 1d8+3 piercing; Claw, melee, +5, reach 5 ft, 1d4+3 slashing

| | |
|---|---|
| SRD block | Brown Bear |
| Type | Large Beast, Unaligned |
| AC | 11 |
| Initiative | +1 |
| HP | 22 (3d10 + 6) |
| Speed | 40 ft., Climb 30 ft. |
| Abilities | STR 17 (+3), DEX 12 (+1), CON 15 (+2), INT 2 (-4), WIS 13 (+1), CHA 7 (-2) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Skills | Perception +3 |
| Senses | Darkvision 60 ft.; Passive Perception 13 |
| Languages | None |

**Wants.** It wants the trail.

**Cheese.** Climb only if you can climb faster than a bear, which you cannot.

**Tactics.** Two of them hold a trail choke.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Patch-Wearing Brown Bear. Level 1. Unit.

**[GM]** The warden does not check permits. The warden checks bones.

### Attacks

- **Multiattack.** The bear makes one Bite attack and one Claw attack
- **Bite.** Melee Attack Roll: +5, reach 5 ft. Hit: 7 (1d8 + 3) Piercing damage
- **Claw.** Melee Attack Roll: +5, reach 5 ft. Hit: 5 (1d4 + 3) Slashing damage. If the target is a Large or smaller creature, it has the Prone condition

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Horse-Bodied Eagle Courier

`f03-u-05` · unit · Horse-Bodied Eagle Courier. Level 1. "Airmail with talons."

**Picture.** Eagle in front, horse in back, wings in the middle, and it is carrying mail you did not order.

**Engine.** Multiattack: 2 x Rend; Rend, melee, +5, reach 5 ft, 1d8+3 slashing

| | |
|---|---|
| SRD block | Hippogriff |
| Type | Large Monstrosity, Unaligned |
| AC | 11 |
| Initiative | +1 |
| HP | 26 (4d10 + 4) |
| Speed | 40 ft., Fly 60 ft. |
| Abilities | STR 17 (+3), DEX 13 (+1), CON 13 (+1), INT 2 (-4), WIS 12 (+1), CHA 8 (-1) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Skills | Perception +5 |
| Senses | Passive Perception 15 |
| Languages | None |

**Wants.** It wants the message and your shoulder.

**Cheese.** Stay indoors. The courier is the sky.

**Tactics.** Dive, grab, fly off with one.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Horse-Bodied Eagle Courier. Level 1. Unit.

**[GM]** Sign here. The pen is a talon.

### Traits

- **Flyby.** The hippogriff doesn’t provoke an Opportunity Attack when it flies out of an enemy’s reach

### Attacks

- **Multiattack.** The hippogriff makes two Rend attacks
- **Rend.** Melee Attack Roll: +5, reach 5 ft. Hit: 7 (1d8 + 3) Slashing damage.

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Swallow-You Mill Toad

`f03-u-06` · unit · Swallow-You Mill Toad. Level 1. "The millpond staff."

**Picture.** A toad the size of a millstone. The tongue is the first problem. The mouth is the second.

**Engine.** Bite, melee, +4, reach 5 ft, 1d6+2 piercing, plus 2d4 poison; Swallow, 3d6 acid

| | |
|---|---|
| SRD block | Giant Toad |
| Type | Large Beast, Unaligned |
| AC | 11 |
| Initiative | +1 |
| HP | 39 (6d10 + 6) |
| Speed | 30 ft., Swim 30 ft. |
| Abilities | STR 15 (+2), DEX 13 (+1), CON 13 (+1), INT 2 (-4), WIS 10 (+0), CHA 3 (-4) |
| CR | 1 |
| XP | 200 |
| PB | +2 |
| Senses | Darkvision 60 ft.; Passive Perception 10 |
| Languages | None |

**Wants.** It wants a swallow.

**Cheese.** Don't stand on the dock. A swallowed Crawler is a puzzle with a timer.

**Tactics.** Tongue, bite, swallow.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Swallow-You Mill Toad. Level 1. Unit.

**[GM]** The pond is not scenic. The pond is pre-digesting.

### Traits

- **Amphibious.** The toad can breathe air and water
- **Standing Leap.** The toad’s Long Jump is up to 20 feet and its High Jump is up to 10 feet with or without a running start

### Attacks

- **Bite.** Melee Attack Roll: +4, reach 5 ft. Hit: 5 (1d6 + 2) Piercing damage plus 5 (2d4) Poison damage. If the target is a Medium or smaller creature, it has the Grappled condition (escape DC 12)
- **Swallow.** The toad swallows a Medium or smaller target it is grappling. While swallowed, the target isn’t Grappled but has the Blinded and Restrained conditions, and it has Total Cover against attacks and other effects outside the toad. In addition, the target takes 10 (3d6) Acid damage at the end of each of the toad’s turns. The toad can have only one target swallowed at a time, and it can’t use Bite while it has a swallowed target. If the toad dies, a swallowed creature is no longer Restrained and can escape from the corpse using 5 feet of movement, exiting with the Prone condition

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Tunneling Acid Ant-Lion

`f03-e-01` · elite · Tunneling Acid Ant-Lion. Level 2. "The road has a basement."

**Picture.** A huge insect that bursts out of the road under your feet and spits a line of acid.

**Engine.** Bite, melee, +5, reach 5 ft, 2d6+3 slashing, plus 1d6 acid; Acid Spray (Recharge 6), Dexterity DC 12, 4d6 acid, recharge 6

| | |
|---|---|
| SRD block | Ankheg |
| Type | Large Monstrosity, Unaligned |
| AC | 14 |
| Initiative | +0 |
| HP | 45 (6d10 + 12) |
| Speed | 30 ft., Burrow 10 ft. |
| Abilities | STR 17 (+3), DEX 11 (+0), CON 14 (+2), INT 1 (-5), WIS 13 (+1), CHA 6 (-2) |
| CR | 2 |
| XP | 450 |
| PB | +2 |
| Senses | Darkvision 60 ft., Tremorsense 60 ft.; Passive Perception 11 |
| Languages | None |

**Wants.** It wants a line of you in the acid cone.

**Cheese.** Don't march single file on the fresh dirt.

**Tactics.** Burst up, acid the file, drag one down.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Tunneling Acid Ant-Lion. Level 2. Elite.

**[GM]** The dirt moved. That is not weather.

### Traits

- **Tunneler.** The ankheg can burrow through solid rock at half its Burrow Speed and leaves a 10-foot-diameter tunnel in its wake

### Attacks

- **Bite.** Melee Attack Roll: +5 (with Advantage if the target is Grappled by the ankheg), reach 5 ft. Hit: 10 (2d6 + 3) Slashing damage plus 3 (1d6) Acid damage. If the target is a Large or smaller creature, it has the Grappled condition (escape DC 13).
- **Acid Spray (Recharge 6).** Dexterity Saving Throw: DC 12, each creature in a 30-foot-long, 5-foot-wide Line. Failure: 14 (4d6) Acid damage. Success: Half damage

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Acid Spray** (recharge, max 1). Starts ready. After Acid Spray is used, it is down until a d6 at the start of this creature's turn shows 6–6. It cannot be used every turn.

## Barn-Rafter Spider Person

`f03-e-02` · elite · Barn-Rafter Spider Person. Level 2. "The hayloft is a web."

**Picture.** A person with extra spider arms in the barn rafters, wrapping whatever used to be livestock.

**Engine.** Multiattack: The ettercap makes one Bite attack and one Claw attack; Bite, melee, +4, reach 5 ft, 1d6+2 piercing, plus 1d4 poison; Claw, melee, +4, reach 5 ft, 2d4+2 slashing; Web Strand (Recharge 5–6), Dexterity DC 12, recharge 5-6; Reel

| | |
|---|---|
| SRD block | Ettercap |
| Type | Medium Monstrosity, Neutral Evil |
| AC | 13 |
| Initiative | +2 |
| HP | 44 (8d8 + 8) |
| Speed | 30 ft., Climb 30 ft. |
| Abilities | STR 14 (+2), DEX 15 (+2), CON 13 (+1), INT 7 (-2), WIS 12 (+1), CHA 8 (-1) |
| CR | 2 |
| XP | 450 |
| PB | +2 |
| Skills | Perception +3, Stealth +4, Survival +3 |
| Senses | Darkvision 60 ft.; Passive Perception 13 |
| Languages | None |

**Wants.** It wants you stuck and quiet.

**Cheese.** Burn the loft webs before you climb.

**Tactics.** Web, then the spiders it already owns.

**Reskin.** None. It may have Giant Wolf Spiders as the block allows. Do not add extra XP without counting them.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Barn-Rafter Spider Person. Level 2. Elite.

**[GM]** Fresh hay. Older guests.

### Traits

- **Spider Climb.** The ettercap can climb difficult surfaces, including along ceilings, without needing to make an ability check
- **Web Walker.** The ettercap ignores movement restrictions caused by webs, and the ettercap knows the location of any other creature in contact with the same web

### Attacks

- **Multiattack.** The ettercap makes one Bite attack and one Claw attack
- **Bite.** Melee Attack Roll: +4, reach 5 ft. Hit: 5 (1d6 + 2) Piercing damage plus 2 (1d4) Poison damage, and the target has the Poisoned condition until the start of the ettercap’s next turn
- **Claw.** Melee Attack Roll: +4, reach 5 ft. Hit: 7 (2d4 + 2) Slashing damage.
- **Web Strand (Recharge 5–6).** Dexterity Saving Throw: DC 12, one Large or smaller creature the ettercap can see within 30 feet. Failure: The target has the Restrained condition until the web is destroyed (AC 10; HP 5; Vulnerability to Fire damage; Immunity to Bludgeoning, Poison, and Psychic damage)

### Bonus actions

- **Reel.** The ettercap pulls one creature within 30 feet of itself that is Restrained by its Web Strand up to 25 feet straight toward itself

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Web Strand** (recharge, max 1). Starts ready. After Web Strand is used, it is down until a d6 at the start of this creature's turn shows 5–6. It cannot be used every turn.

## Roadside Priest, Mace Blessed

`f03-e-03` · elite · Roadside Priest, Mace Blessed. Level 2. "The shrine on the road is occupied."

**Picture.** A priest at a roadside shrine. The blessing is optional. The mace is not.

**Engine.** Multiattack: The priest makes two attacks, using Mace or Radiant Flame in any combination; Mace, melee, +5, reach 5 ft, 1d6+3 bludgeoning, plus 2d4 radiant; Radiant Flame, ranged, +5, range 60/60 ft, 2d10 radiant; Spellcasting: spend tracked_uses. At-will does not spend.; Spellcasting: spend tracked_uses. At-will does not spend.

| | |
|---|---|
| SRD block | Priest |
| Type | Medium or Small Humanoid (Cleric), Neutral |
| AC | 13 |
| Initiative | +0 |
| HP | 38 (7d8 + 7) |
| Speed | 30 ft. |
| Abilities | STR 16 (+3), DEX 10 (+0), CON 12 (+1), INT 13 (+1), WIS 16 (+3), CHA 13 (+1) |
| CR | 2 |
| XP | 450 |
| PB | +2 |
| Skills | Medicine +7 , Perception +5, Religion +5 |
| Gear | Chain Shirt, Holy Symbol, Mace |
| Senses | Passive Perception 15 |
| Languages | Common plus one other language |

**Wants.** It wants the party cursed and then converted.

**Cheese.** Drop the caster. The spirit guardians are the room.

**Tactics.** Spirit guardians in the door, then the mace.

**Reskin.** Radiant stays radiant. The shrine is a set.

**House check.** Spirit Guardians is once per day, not a 3rd-level slot that refills. Divine Aid is three casts total, any mix of Bless, Dispel Magic, Healing Word, or Lesser Restoration, not three of each. At 0, Mace and Radiant Flame only.

**[SYSTEM]** Roadside Priest, Mace Blessed. Level 2. Elite.

**[GM]** Pilgrims welcome. The welcome is a damage aura.

### Attacks

- **Multiattack.** The priest makes two attacks, using Mace or Radiant Flame in any combination
- **Mace.** Melee Attack Roll: +5, reach 5 ft. Hit: 6 (1d6 + 3) Bludgeoning damage plus 5 (2d4) Radiant damage
- **Radiant Flame.** Ranged Attack Roll: +5, range 60 ft. Hit: 11 (2d10) Radiant damage
- **Spellcasting.** The priest casts one of the following spells, using Wisdom as the spellcasting ability (spell save DC 13): At Will: Light, Thaumaturgy 1/Day: Spirit Guardians

### Bonus actions

- **Divine Aid (3/Day).** The priest casts Bless, Dispel Magic, Healing Word, or Lesser Restoration, using the same spellcasting ability as Spellcasting.

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Divine Aid** (shared_spell_pool, max 3). 3 cast(s) total, any mix of Bless, Dispel Magic, Healing Word, Lesser Restoration. Not that many of each spell. At 0, weapon attacks and at-will cantrips only.
- **Light** (at_will, no cap (at will), spell level 0). At will. Not a spell slot. May be repeated. Do not spend a slot for it.
- **Thaumaturgy** (at_will, no cap (at will), spell level 0). At will. Not a spell slot. May be repeated. Do not spend a slot for it.
- **Spirit Guardians** (daily_spell, max 1, spell level 3). 1 per day. Not a slot of spell level 3 that comes back each turn. At 0, do not cast it.

## Blink-Past-the-Gate Spider

`f03-e-04` · elite · Blink-Past-the-Gate Spider. Level 3. "The gate is not where it was."

**Picture.** A big spider that steps out of sight on one side of the gate and back in behind you.

**Engine.** Multiattack: 2 x Bite; Bite, melee, +5, reach 5 ft, 1d10+3 piercing, plus 2d8 poison; Ethereal Jaunt

| | |
|---|---|
| SRD block | Phase Spider |
| Type | Large Monstrosity, Unaligned |
| AC | 14 |
| Initiative | +3 |
| HP | 45 (7d10 + 7) |
| Speed | 30 ft., Climb 30 ft. |
| Abilities | STR 15 (+2), DEX 16 (+3), CON 12 (+1), INT 6 (-2), WIS 10 (+0), CHA 6 (-2) |
| CR | 3 |
| XP | 700 |
| PB | +2 |
| Skills | Stealth +7 |
| Senses | Darkvision 60 ft.; Passive Perception 10 |
| Languages | None |

**Wants.** It wants a bite from the Ethereal.

**Cheese.** Ready attacks. Don't chase it through the gate alone.

**Tactics.** Phase, bite, phase.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Blink-Past-the-Gate Spider. Level 3. Elite.

**[GM]** The door blinked. So did the thing on your back.

### Traits

- **Ethereal Sight.** The spider can see 60 feet into the Ethereal Plane while on the Material Plane and vice versa
- **Spider Climb.** The spider can climb difficult surfaces, including along ceilings, without needing to make an ability check
- **Web Walker.** The spider ignores movement restrictions caused by webs, and the spider knows the location of any other creature in contact with the same web

### Attacks

- **Multiattack.** The spider makes two Bite attacks
- **Bite.** Melee Attack Roll: +5, reach 5 ft. Hit: 8 (1d10 + 3) Piercing damage plus 9 (2d8) Poison damage. If this damage reduces the target to 0 Hit Points, the target becomes Stable, and it has the Poisoned condition for 1 hour. While Poisoned, the target also has the Paralyzed condition

### Bonus actions

- **Ethereal Jaunt.** The spider teleports from the Material Plane to the Ethereal Plane or vice versa.

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Lion-Bat with a Spike Tail

`f03-e-05` · elite · Lion-Bat with a Spike Tail. Level 3. "Advertising, then the spikes."

**Picture.** A lion's body, bat wings, a person's face, and a tail that throws spikes like darts.

**Engine.** Multiattack: The manticore makes three attacks, using Rend or Tail Spike in any combination; Rend, melee, +5, reach 5 ft, 1d8+3 slashing; Tail Spike, ranged, +5, range 100/200 ft, 1d8+3 piercing

| | |
|---|---|
| SRD block | Manticore |
| Type | Large Monstrosity, Lawful Evil |
| AC | 14 |
| Initiative | +3 |
| HP | 68 (8d10 + 24) |
| Speed | 30 ft., Fly 50 ft. |
| Abilities | STR 17 (+3), DEX 16 (+3), CON 17 (+3), INT 7 (-2), WIS 12 (+1), CHA 8 (-1) |
| CR | 3 |
| XP | 700 |
| PB | +2 |
| Senses | Darkvision 60 ft.; Passive Perception 11 |
| Languages | Common |

**Wants.** It wants range.

**Cheese.** Get under it or inside. The tail is the artillery.

**Tactics.** Tail spikes until someone closes, then claws.

**Reskin.** None.

**House check.** House set dressing. Numbers stay the SRD block. Nameplate level is flavor.

**[SYSTEM]** Lion-Bat with a Spike Tail. Level 3. Elite.

**[GM]** The billboard has a face. The face has a magazine.

### Attacks

- **Multiattack.** The manticore makes three attacks, using Rend or Tail Spike in any combination
- **Rend.** Melee Attack Roll: +5, reach 5 ft. Hit: 7 (1d8 + 3) Slashing damage
- **Tail Spike.** Ranged Attack Roll: +5, range 100/200 ft. Hit: 7 (1d8 + 3) Piercing damage

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Two-Headed Toll Giant

`f03-b-01` · boss · Two-Headed Toll Giant. Level 4. Boss. "Two heads, two prices."

**Picture.** One giant body, two heads, both of them charging a toll and both of them swinging.

**Engine.** Multiattack: The ettin makes one Battleaxe attack and one Morningstar attack; Battleaxe, melee, +7, reach 5 ft, 2d8+5 slashing; Morningstar, melee, +7, reach 5 ft, 2d8+5 piercing

| | |
|---|---|
| SRD block | Ettin |
| Type | Large Giant, Chaotic Evil |
| AC | 12 |
| Initiative | -1 |
| HP | 85 (10d10 + 30) |
| Speed | 40 ft. |
| Abilities | STR 21 (+5), DEX 8 (-1), CON 17 (+3), INT 6 (-2), WIS 10 (+0), CHA 8 (-1) |
| CR | 4 |
| XP | 1100 |
| PB | +2 |
| Skills | Perception +4 |
| Gear | Battleaxe, Morningstar |
| Immunities | Blinded, Charmed, Deafened, Frightened, Stunned, Unconscious |
| Senses | Darkvision 60 ft.; Passive Perception 14 |
| Languages | Giant |

**Wants.** It wants both lanes paid.

**Cheese.** Blind one head. They argue. Use the argument.

**Tactics.** Each head picks a different Crawler.

**Reskin.** None. Two heads are already the block.

**House check.** Boss card for a random draw that fits the rules/70 cap. It does not replace a boss already printed on a Day page. A dead boss does not auto-clear other encounters.

**[SYSTEM]** Two-Headed Toll Giant. Level 4. Boss.

**[GM]** The toll is a fight. Both cashiers agree, which is rare.

### Attacks

- **Multiattack.** The ettin makes one Battleaxe attack and one Morningstar attack
- **Battleaxe.** Melee Attack Roll: +7 , reach 5 ft. Hit: 14 (2d8 + 5) Slashing damage. If the target is a Large or smaller creature, it has the Prone condition
- **Morningstar.** Melee Attack Roll: +7 , reach 5 ft. Hit: 14 (2d8 + 5) Piercing damage, and the target has Disadvantage on the next attack roll it makes before the end of its next turn

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.

## Grant-Denied Ghost

`f03-b-02` · boss · Grant-Denied Ghost. Level 4. Boss. "The land grant never died."

**Picture.** A ghost in a blazer who can walk into your body and hate your application from the inside.

**Engine.** Multiattack: 2 x Withering Touch; Withering Touch, melee, +5, reach 5 ft, 3d10+3 necrotic; Etherealness; Horrific Visage, Wisdom DC 13, 2d6+3 psychic; Possession (Recharge 6), Charisma DC 13, recharge 6

| | |
|---|---|
| SRD block | Ghost |
| Type | Medium Undead, Neutral |
| AC | 11 |
| Initiative | +1 |
| HP | 45 (10d8) |
| Speed | 5 ft., Fly 40 ft. (hover) |
| Abilities | STR 7 (-2), DEX 13 (+1), CON 10 (+0), INT 10 (+0), WIS 12 (+1), CHA 17 (+3) |
| CR | 4 |
| XP | 1100 |
| PB | +2 |
| Resistances | Acid, Bludgeoning, Cold, Fire, Lightning, Piercing, Slashing, Thunder |
| Immunities | Necrotic, Poison; Charmed, Exhaustion, Frightened, Grappled, Paralyzed, Petrified, Poisoned, Prone, Restrained |
| Senses | Darkvision 60 ft.; Passive Perception 11 |
| Languages | Common plus one other language |

**Wants.** It wants possession of a Crawler and the deed.

**Cheese.** Don't let it start in the walls. Turn undead or finish the possession fast.

**Tactics.** Horrify, possess the isolated, age the stubborn.

**Reskin.** None.

**House check.** Etherealness is printed as an at-will plane step, not a damage spell and not a slot. Do not add a slot table. Possession is recharge 6. Horrific Visage is not a slot; a success makes that creature immune for 24 hours, as printed.

**[SYSTEM]** Grant-Denied Ghost. Level 4. Boss. Undead.

**[GM]** The deed is haunted. So is the deed-holder. That is you if you stand still.

### Traits

- **Ethereal Sight.** The ghost can see 60 feet into the Ethereal Plane when it is on the Material Plane
- **Incorporeal Movement.** The ghost can move through other creatures and objects as if they were Difficult Terrain. It takes 5 (1d10) Force damage if it ends its turn inside an object

### Attacks

- **Multiattack.** The ghost makes two Withering Touch attacks
- **Withering Touch.** Melee Attack Roll: +5, reach 5 ft. Hit: 19 (3d10 + 3) Necrotic damage
- **Etherealness.** The ghost casts the Etherealness spell, requiring no spell components and using Charisma as the spellcasting ability. The ghost is visible on the Material Plane while on the Border Ethereal and vice versa, but it can’t affect or be affected by anything on the other plane
- **Horrific Visage.** Wisdom Saving Throw: DC 13, each creature in a 60-foot Cone that can see the ghost and isn’t an Undead. Failure: 10 (2d6 + 3) Psychic damage, and the target has the Frightened condition until the start of the ghost’s next turn. Success: The target is immune to this ghost’s Horrific Visage for 24 hours.
- **Possession (Recharge 6).** Charisma Saving Throw: DC 13, one Humanoid the ghost can see within 5 feet. Failure: The target is possessed by the ghost; the ghost disappears, and the target has the Incapacitated condition and loses control of its body. The ghost now controls the body, but the target retains awareness. The ghost can’t be targeted by any attack, spell, or other effect, except ones that specifically target Undead. The ghost’s game statistics are the same, except it uses the possessed target’s Speed, as well as the target’s Strength, Dexterity, and Constitution modifiers. The possession lasts until the body drops to 0 Hit Points or the ghost leaves as a Bonus Action. When the possession ends, the ghost appears in an unoccupied space within 5 feet of the target, and the target is immune to this ghost’s Possession for 24 hours. Success: The target is immune to this ghost’s Possession for 24 hours

### Tracked uses

A numbered pool at 0 does not fire again until it recovers. The creature uses its weapon or natural attacks. A recharge trick stays down until the d6 hits the printed range. At-will cantrips may still be cast. Do not refill a pool in the same fight, and do not add slots the block does not print.

- **Possession** (recharge, max 1). Starts ready. After Possession is used, it is down until a d6 at the start of this creature's turn shows 6–6. It cannot be used every turn.
- **Etherealness** (at_will_innate, no cap (at will), spell level 7). Printed without a daily cap. It is not a spell slot. Do not add slots, and do not treat it as a repeating damage spell unless the action itself deals damage.

## Hungry Black Silo Slime

`f03-b-03` · boss · Hungry Black Silo Slime. Level 4. Boss. "The grain went wrong."

**Picture.** A silo full of black slime. Cut it and it splits. It eats metal, wood, and whoever brought the metal.

**Engine.** Dissolving Pseudopod, melee, +5, reach 10 ft, 4d6+3 acid; Split

| | |
|---|---|
| SRD block | Black Pudding |
| Type | Large Ooze, Unaligned |
| AC | 7 |
| Initiative | -3 |
| HP | 68 (8d10 + 24) |
| Speed | 20 ft., Climb 20 ft. |
| Abilities | STR 16 (+3), DEX 5 (-3), CON 16 (+3), INT 1 (-5), WIS 6 (-2), CHA 1 (-5) |
| CR | 4 |
| XP | 1100 |
| PB | +2 |
| Immunities | Acid, Cold, Lightning, Slashing; Charmed, Deafened, Exhaustion, Frightened, Grappled, Prone, Restrained |
| Senses | Blindsight 60 ft.; Passive Perception 8 |
| Languages | None |

**Wants.** It wants to split and fill the silo.

**Cheese.** Don't split it with lightning or slashing if you can burn it. Read the resistances.

**Tactics.** Engulf in the chute. Split if cut.

**Reskin.** None. Resistances are the cheese.

**House check.** Split is a printed reaction with a trigger. It is not a spell. Do not add a daily cap the block does not have.

**[SYSTEM]** Hungry Black Silo Slime. Level 4. Boss. Ooze.

**[GM]** Do not open the silo. You opened the silo.

### Traits

- **Amorphous.** The pudding can move through a space as narrow as 1 inch without expending extra movement to do so
- **Corrosive Form.** A creature that hits the pudding with a melee attack roll takes 4 (1d8) Acid damage. Nonmagical ammunition is destroyed immediately after hitting the pudding and dealing any damage. Any nonmagical weapon takes a cumulative −1 penalty to attack rolls immediately after dealing damage to the pudding and coming into contact with it. The weapon is destroyed if the penalty reaches −5. The penalty can be removed by casting the Mending spell on the weapon. In 1 minute, the pudding can eat through 2 feet of nonmagical wood or metal
- **Spider Climb.** The pudding can climb difficult surfaces, including along ceilings, without needing to make an ability check

### Attacks

- **Dissolving Pseudopod.** Melee Attack Roll: +5, reach 10 ft. Hit: 17 (4d6 + 3) Acid damage. Nonmagical armor worn by the target takes a −1 penalty to the AC it offers. The armor is destroyed if the penalty reduces its AC to 10. The penalty can be removed by casting the Mending spell on the armor

### Reactions

- **Split.** Trigger: While the pudding is Large or Medium and has 10+ Hit Points, it becomes Bloodied or is subjected to Lightning or Slashing damage. Response: The pudding splits into two new Black Puddings. Each new pudding is one size smaller than the original pudding and acts on its Initiative. The original pudding’s Hit Points are divided evenly between the new puddings (round down)

### Tracked uses

No limited spells and no recharge tricks. Weapon and natural attacks may repeat.
