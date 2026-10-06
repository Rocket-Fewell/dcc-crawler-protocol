# Skills and Achievements
Owner: Valtay Corp - Core Book Author | Status: draft | Version: 0.2 | Updated: 2026-10-06
Summary: Chapter 5. Ability checks, the 18 SRD 5.2 skills with Crawl examples, proficiency and Expertise, passive checks, group checks, contests, check-calling actions, tools; System skills (general skill track per decision 037: rank-ups from meaningful use, first-time feats, inventive crafting, potions or guild training; GM-granted, no counters; cap 15, or 20 for a species or class family; +1 at ranks 5/10/15; crafting skills, Cockroach Clause); achievements (notability, timing, toast, R0-R6 ladder, Titles, credit multiplier, achievement box tiers by floor, rarity ceilings, hidden Fan Profile tailoring, fair play), Crawl Charms and Blessings, 72 sample achievements (Any / Floor 1 / Floor 2). No pets, no Story Box deeds or list, no Fan Profile fields, no survey, no GM quirk/affinity, no budget totals.
Sources: decision 037 (general System skill track); rules/10-core-rules-5e.md v0.2.22 (§1.1, §2.5.1, §2.5.5, §2.5.6, §3.1-3.9, §4.1-4.2, §4.4, §4.8, §6.5, App. A-C); rules/40-loot-deck-spec-5e.md v0.1.9 (§2.2, §2.4, §2.9); rules/70-encounter-budget-5e.json v0.2.6 (floors.1.achievement_rewards, floors.2.boxes.f2_box_rulings); rules/20-crafting-5e.md v0.3.7 (§1, §3); tables/achievements.csv v1.4 (1,835 rows); create-screens-reskins v0.1.3 (ability display names; skill names stay plain); lore CANON-LEDGER v1.20 (M-008, M-009/S-001; skill track via Lore's Q19 note: M-059, K-070, K-057, K-079, K-064, M-807, M-045, I-011, K-071, K-078, A-143; A-034, A-044, A-047, A-131, A-136, A-139, A-151), lore catalog/skills.md v1.0, mechanics-clarifications §3; SRD 5.2 (CC-BY-4.0).

<!-- BEGIN -->

<!-- Canon tags for this chapter (source-side only; the printed tags are HOUSE / INSPIRED):
     - Achievements as System notifications that reward, mock or warn: lore catalog/achievements.md (WIKI-ONLY overview; individual A- rows mostly VERIFIED wiki cites).
     - Box tiers Bronze..Celestial: ledger L-001 VERIFIED. Boxes open only in saferooms: L-002 VERIFIED. Semi-random contents: L-003 VERIFIED.
     - Skills level by use: lore mechanics-clarifications 3.1 (WIKI, HIGH). Skills generally cap at 15: ledger M-008 VERIFIED (page cite B2 ch2). Cockroach: M-009 / S-001 VERIFIED.
     - System skill track (decision 037, core v0.2.22): sources are canon-shaped, per Lore's Q19 note (all VERIFIED): train by use, potions or a training guild M-059; first-time feat grants a skill K-070, K-057; inventive crafting raises several K-079, K-064; hard or clever use pays extra M-807; Skill Potion +1 M-045; Cheat Code Potion +3 random I-011; class/race bonus K-071; cap 15 M-008, 20 for a race/class family K-078 (Hobgoblin traps/explosives); past 15 in real fights A-143 (achievement name printed per decision 037). Pace (no counters, GM-granted, next safe point) and the +1 at ranks 5/10/15: HOUSE.
     - Reward ladder R0-R6, credit multiplier, achievement box tiers by floor, Charms, Blessings, Cockroach Clause tiers and prices: HOUSE (campaign core rules), Cockroach Clause CANON-INSPIRED.
     - Sample achievement names are the campaign catalog's own (HOUSE) except those marked with a dagger, which echo canon achievement shapes (A-034, A-047, A-131, A-136, A-139 VERIFIED; A-151 WIKI-ONLY; A-044 VERIFIED). No canon achievement text is reproduced. -->

# Skills and Achievements

::: epigraph The System
You have skills! Some of them are even useful. The rest will be graded on a curve, live, in front of an audience of several billion.
:::

Every Crawler is good at something. This chapter is about what happens when your Crawler tries something and the outcome is in doubt: the **ability check**, the **eighteen skills** of the fifth edition rules, and the habits a Crawl table uses to keep checks fast and fair. The second half of the chapter is about what happens when the System decides you did something *notable*: **achievements**, the reward ladder behind them, and a starter list of the kind of deeds the System likes to talk about.

The rules for checks are the **SRD 5.2** rules, written out here in our own words with Crawl examples. Nothing about the math has changed. The achievement rules are ours. {{HOUSE}}

::: sidebar What This Chapter Is Not
This chapter does not explain how the System decides *which* reward suits you. That lives in a hidden profile you never see. It also does not list every achievement in the catalog. The System has the full catalog, and the System does not share.
:::

## Ability Checks

An **ability check** tests what a Crawler can do when failure is possible and interesting: picking a lock while something scratches at the door, talking a vending machine's owner out of a refund policy, or remembering which end of a goblin is the dangerous end. Attack rolls and saving throws are the other two **d20 tests**. This chapter covers checks.

### Making a Check

1. **The GM picks the ability** that fits the task, and a **skill** if one applies (for example, Dexterity (Stealth)).
2. **The GM sets a Difficulty Class (DC).** The table below gives the usual steps.
3. **Roll a d20 and add the ability modifier.** Add your **Proficiency Bonus** if you are proficient in the skill or tool being used.
4. **Meet or beat the DC** and the check succeeds. Fall short and it fails, and the Dungeon gets to decide what failure looks like.

| Task difficulty | DC |
|---|:---:|
| Very easy | 5 |
| Easy | 10 |
| Medium | 15 |
| Hard | 20 |
| Very hard | 25 |
| Nearly impossible | 30 |

Most checks in a session sit at **Easy** or **Medium**. A Very Easy task usually doesn't need a roll at all, and a Nearly Impossible one should be rare enough to be worth an achievement if somebody pulls it off.

### When Not to Roll

Call for a check only when the outcome is uncertain *and* failure would change something. Walking down a hallway, opening an unlocked door and reading a sign do not need dice. A Crawler with all the time in the world and nothing hunting them can usually just succeed at a simple task. In the Crawl that situation is rare, because the floor clock is always running.

### Calling the Check

At this table the System **names the ability, the skill and the DC before the roll** whenever the Crawler would reasonably know what they are up against. That keeps decisions honest: a player who hears "Strength (Athletics), DC 20" for a rusted shutter can choose to look for another way in. {{HOUSE}}

By default the System rolls all dice **in the open** and announces the whole result, so everyone can follow it:

> **Strength (Athletics), DC 15.** Roll 14, plus 5. **19. Success.**

A table may let players roll their own dice instead; agree on it at session zero. The System still rolls some checks **in secret** where the fifth edition rules expect it: a monster's Stealth, an Insight read on a liar, or a trap the Crawler shouldn't see coming. Secret or not, **dice stand**. The System does not fudge rolls in your favor or against you.

::: system
The System does not cheat. The System does not need to. Have you seen your Wisdom score?
:::

### Advantage and Disadvantage

When circumstances help, you have **Advantage**: roll two d20s and use the higher. When they hurt, you have **Disadvantage**: roll two and use the lower. If you have both, they cancel and you roll one d20. Multiple sources of Advantage still mean only two dice. The GM grants Advantage for good tools, good plans and good help, and imposes Disadvantage for bad light, bad footing and bad ideas.

### Natural 20s and Natural 1s

On an ability check, a roll of 20 or 1 is just a number. It is **not** an automatic success or failure. (The automatic hit and miss belong to attack rolls; death saving throws have their own rule.) The System will still comment on your natural 1. It is contractually obligated to.

### Heroic Inspiration

If you have **Heroic Inspiration**, you can spend it to reroll any one die right after you roll it, and you must use the new roll. You can hold only one at a time. The Crawl hands it out for crowd-pleasing moments and as an achievement reward (see "The Reward Ladder" below).

### Using Different Abilities

Each skill is listed under the ability it usually goes with, but the GM may pair a skill with another ability when the task calls for it. Pinning a struggling goblin while you shout questions at it might be Strength (Intimidation). Remembering the layout of a store you worked in might be Intelligence (Survival) instead of Wisdom. The skill says *what you know how to do*; the ability says *how you are doing it*.

## Proficiency and Expertise

Your **Proficiency Bonus** is set by your level and goes up as you descend. Add it to any check that uses a skill or tool you are proficient in.

| Level | Proficiency Bonus |
|---|:---:|
| 1–4 | +2 |
| 5–8 | +3 |
| 9–12 | +4 |
| 13–16 | +5 |
| 17–20 | +6 |

**Where proficiencies come from.** Your Prior Employment (background) gives you two skills and a tool. Your class lets you pick more skills from its list. Some species give one (an Elf's Keen Senses, a Human's Skillful trait), and some feats give several (the Skilled Origin feat gives three). Chapter 2 walks through the picks; you can never be proficient in the same skill twice.

**Expertise.** Some features grant **Expertise** in a skill. When you make a check with that skill, your Proficiency Bonus is **doubled**. A Rogue picks two skills for Expertise at level 1, and a Bard gets it at level 2. Expertise only applies to a skill you are already proficient in.

::: sidebar Plain Names on Purpose
Ability scores have kiosk nicknames on the intake screens (Gym-Bro Energy, Pub-Quiz Brain, and the rest). **Skill names never get a nickname.** Your sheet, the System's roll posts and this book all say Athletics, Perception and Sleight of Hand, so nobody has to translate in the middle of a fight.
:::

## The Eighteen Skills

| Skill | Ability | Covers |
|---|---|---|
| Athletics | Strength | Climbing, jumping, swimming, shoving, grappling, forcing |
| Acrobatics | Dexterity | Balance, tumbling, staying upright, slipping free |
| Sleight of Hand | Dexterity | Pickpocketing, palming, planting, fine manual tricks |
| Stealth | Dexterity | Hiding, sneaking, moving without being noticed |
| Arcana | Intelligence | Spells, magic items, sigils, magical oddities |
| History | Intelligence | Past events, people, places, old institutions |
| Investigation | Intelligence | Deduction, searching for clues, working out how things fit |
| Nature | Intelligence | Terrain, plants, animals, weather |
| Religion | Intelligence | Gods, rites, holy symbols, cults |
| Animal Handling | Wisdom | Calming, steering and reading animals |
| Insight | Wisdom | Reading intent, spotting lies, sensing mood |
| Medicine | Wisdom | Stabilizing the dying, diagnosing illness and poison |
| Perception | Wisdom | Noticing things with your senses |
| Survival | Wisdom | Tracking, foraging, navigating, reading hazards |
| Deception | Charisma | Lying convincingly, disguises, misdirection |
| Intimidation | Charisma | Threats, menace, getting your way by fear |
| Performance | Charisma | Entertaining an audience on purpose |
| Persuasion | Charisma | Honest argument, negotiation, charm |

Constitution has no skills. When the System asks you to keep drinking, keep running or keep holding your breath, it calls for a plain Constitution check.

## Skills by Ability

Each entry below says what the skill covers and gives a handful of ways it comes up in the Crawl. The examples lean on Floors 1 and 2, where most new Crawlers spend their first sessions finding out what their sheet is for. Difficulty words (Easy, Medium, Hard) refer to the DC table above.

### Gym-Bro Energy (Strength)

Strength checks measure raw force: lifting, pushing, pulling, breaking. Without a skill, a Strength check covers forcing a jammed door, bending bars, lifting a collapsed shelf off a friend, or holding a closing gate for one more second.

#### Athletics

**Climbing, jumping, swimming and wrestling.** Athletics covers hard physical effort against the world or against a body: scaling a wall, leaping farther than your normal jump allows, swimming against a current, and breaking free when something has you grappled. (Grappling or shoving a creature yourself uses the SRD's Unarmed Strike options, which call for the target's saving throw, not your check.)

- Hauling yourself up a slick maintenance ladder while the lights strobe (Easy) or a greased one while something bites your ankle (Hard).
- Kicking through a flimsy partition wall to skip a hallway the System obviously wants you to walk down.
- Keeping your grip on a rope bridge when the far end starts to unclip itself.
- Shoving a vending machine over onto a goblin. The System will log the property damage.

### Parkour Delusion (Dexterity)

Dexterity checks measure agility, reflexes and fine control. Without a skill, a Dexterity check covers things like catching a falling vial or steering a stolen shopping cart down a ramp. **Initiative** is a Dexterity check too.

#### Acrobatics

**Balance, tumbling and staying on your feet.** Use Acrobatics to keep your footing on ice, oil or a moving floor, to dive and roll through a gap, or to wriggle free of a grapple when the other ability would be Strength (Athletics).

- Running across a floor slick with something you'd rather not identify.
- Dropping and rolling under a closing shutter.
- Landing on your feet after the floor tilts (the System calls this "a fun surprise").

#### Sleight of Hand

**Quick, careful hands.** Pickpocketing, palming an object, planting something on someone, loosening a bolt without anyone seeing, and other fiddly work done under observation.

- Lifting a keycard off a sleeping guard.
- Palming a small item off a vendor's counter while you haggle. (Getting caught is also an achievement.)
- Tying a tripwire across a doorway while the rest of the party keeps a mob's attention.

#### Stealth

**Not being noticed.** Stealth covers sneaking, hiding and moving quietly. Use it with the **Hide** action (see "Actions That Call for Checks"). Heavy armor that the SRD marks with a Stealth penalty gives you Disadvantage.

- Slipping past a pack of sleeping mobs to reach a loot crate.
- Following a rival party far enough to see where their stairwell is.
- Staying very, very still while something large sniffs the vent you are in.

### Pub-Quiz Brain (Intelligence)

Intelligence checks measure memory, reasoning and knowledge. Without a skill, an Intelligence check covers working out a code, assembling a device from parts, or estimating the value of junk.

#### Arcana

**Magic and the things it leaves behind.** Arcana covers spells, magic items, glyphs, magical traditions and the stranger corners of the Dungeon's machinery.

- Recognizing the spell a goblin shaman is winding up before it finishes.
- Working out what an unidentified magic item probably does before you put it on.
- Spotting that a saferoom's glowing sigil is a little *too* glowing.

#### History

**What happened before.** History covers past events, famous people, lost places, old organizations and the customs that came out of them. In a game where everything inside was destroyed in one afternoon, history includes everything you knew about the world before.

- Remembering how a real-world building of this type was laid out, and where its back exits were.
- Recalling the name and habits of a faction that shows up on a later floor.
- Recognizing a symbol from a museum exhibit that no longer exists.

#### Investigation

**Deduction.** Investigation is searching *and thinking*: noticing that a desk has been moved, working out where a trap's trigger must be from the shape of the room, reading what happened from a scene. Use it with the **Study** action.

- Working out from the scuff marks that the "saferoom" door gets opened from the outside.
- Figuring out how a System puzzle-lock wants to be solved.
- Reading a vendor's price list for the catch.

#### Nature

**The living world.** Nature covers terrain, plants, animals, weather and natural cycles. The Dungeon builds habitats, and Nature tells you how they work.

- Identifying a mushroom as edible, poisonous or "edible once."
- Knowing what a creature eats, and therefore what it might be hunting.
- Predicting that the water in a flooded zone will rise with the "tide."

#### Religion

**Gods and the things done in their names.** Religion covers deities, rites, prayers, holy symbols, religious orders and cults.

- Recognizing a shrine's patron, and whether offering at it is polite or suicidal.
- Spotting that a cult's chant is counting down.
- Knowing which rites a temple NPC will expect from a visitor.

### Warning Signs You Ignored (Wisdom)

Wisdom checks measure awareness, intuition and common sense. Without a skill, a Wisdom check covers getting a gut feeling about a plan or noticing that something about a room is wrong without knowing what.

#### Animal Handling

**Animals and animal-like things.** Animal Handling covers calming a frightened beast, keeping a mount steady, reading an animal's mood and guessing what it will do next. Use it with the **Influence** action when you deal with a Beast or a Monstrosity.

- Talking a cornered, frightened dog out of biting you.
- Noticing that the rats have all stopped moving.
- Keeping a skittish mount from bolting when the fireworks start.

#### Insight

**Reading people.** Insight covers telling whether someone is lying, guessing what they want, and sensing mood and intent from body language and tone. Use it with the **Search** action when the thing you're searching is a creature's state of mind.

- Telling whether a Crawler from another party is really lost or is scouting you.
- Reading whether an NPC's smile means "deal" or "dinner."
- Sensing that the System's cheerful announcement is hiding something. (It is. It always is.)

#### Medicine

**Keeping bodies working.** Medicine covers stabilizing a dying creature, diagnosing an illness, recognizing a poison and working out what killed something. Taking the Help action to stabilize a creature at 0 hit points calls for a DC 10 Wisdom (Medicine) check, as the SRD says.

- Stabilizing an ally at 0 hit points before the next round ends.
- Recognizing which goblin toxin is in the wound, and what it does next.
- Telling from a corpse how long ago something happened, and how.

#### Perception

**Noticing.** Perception covers spotting, hearing and otherwise detecting things with your senses: a hidden creature, a tripwire, a quiet sound. It is the skill most often used passively (see "Passive Checks").

- Hearing claws in the ceiling.
- Spotting the shimmer of a pressure plate in a dusty floor.
- Noticing that the stairwell sign is hand-painted.

#### Survival

**Getting by in hostile terrain.** Survival covers tracking, hunting, finding food and water, finding your way, and reading hazards in the environment. Use it with the **Search** action for tracks and food.

- Following blood drops back to where a mob is nesting.
- Finding your way back to the last saferoom when the map is still fogged.
- Judging that the "shortcut" across the flooded atrium is a very bad idea.

### Main-Character Energy (Charisma)

Charisma checks measure force of personality and how well you deal with an audience. Without a skill, a Charisma check covers a first impression, a toast, or a clumsy attempt to blend into a crowd. Most social checks use the **Influence** action.

#### Deception

**Lying, and being good at it.** Deception covers convincing lies, misleading half-truths, disguises and bluffing. It is opposed by the target's Insight when it matters.

- Convincing a guard that you have every right to be behind the counter.
- Telling a rival party that the hallway behind you is a dead end.
- Pretending you meant to set off that trap.

#### Intimidation

**Getting your way by fear.** Intimidation covers threats, menace, a display of force or a very convincing stare.

- Making a gang of mobs reconsider the fight once their leader drops.
- Persuading a stubborn NPC that you will, in fact, keep breaking things.
- Staring down another Crawler at the last vendor in the zone.

#### Performance

**Entertaining on purpose.** Performance covers music, acting, comedy, dancing, storytelling and anything else done for an audience. In a game that is broadcast to an audience, Performance comes up more than you'd expect.

- Holding a crowd's attention while the rest of the party loots behind them.
- Turning a disaster into a bit the audience enjoys.
- Delivering a one-liner the System decides to replay.

#### Persuasion

**Honest influence.** Persuasion covers good-faith argument, negotiation, diplomacy and charm. Haggling with a vendor is a Charisma check, usually Persuasion (Deception or Intimidation also work; see Chapter 1).

- Haggling a price down at a saferoom vendor.
- Convincing a frightened NPC to come with you.
- Talking a tired party into one more room before the Long Rest.

::: system
Skills update in real time. Please do not attempt to update them yourself by shouting.
:::

## Typical Checks in the Crawl

The GM sets every DC, but these are the kinds of tasks that come up again and again on the early floors, with the check the System usually calls and how hard it tends to be. Use them as a starting point, not a price list.

| Task | Usual check | Usual difficulty |
|---|---|---|
| Force a stuck office door | Strength (Athletics) | Easy to Medium |
| Climb a collapsed escalator | Strength (Athletics) | Medium |
| Cross an oil-slicked floor at a run | Dexterity (Acrobatics) | Medium |
| Pick a cheap lock | Dexterity, with Thieves' Tools | Easy to Medium |
| Pick a System-grade lock | Dexterity, with Thieves' Tools | Hard |
| Sneak past sleeping mobs | Dexterity (Stealth), often as a group check | Medium |
| Identify a common potion by smell | Intelligence (Arcana) or Wisdom (Medicine) | Easy |
| Spot a pressure plate in a dusty corridor | Wisdom (Perception), often passive | Medium |
| Work out which way a trap fires | Intelligence (Investigation) | Medium |
| Follow fresh tracks through debris | Wisdom (Survival) | Easy to Medium |
| Stabilize a dying ally | Wisdom (Medicine) | DC 10 |
| Tell whether an NPC is lying | Wisdom (Insight) vs their Charisma (Deception) | Contest |
| Talk a hesitant NPC into helping | Charisma (Persuasion), Influence action | 15 or the NPC's Intelligence |
| Haggle with a saferoom vendor | Charisma (Persuasion, Deception or Intimidation) | Set by the vendor |
| Hide behind a vending machine | Dexterity (Stealth), Hide action | DC 15 |

## Passive Checks

A **passive check** is a check nobody rolls. It stands for the average result of doing something over and over, or of doing it without thinking. The GM uses passive checks for things a Crawler would notice or understand without asking, and to keep a busy table moving.

**Passive check = 10 + every modifier that normally applies to the check.** Add 5 if you have Advantage on it, and subtract 5 if you have Disadvantage.

- **Passive Perception** is the one on your sheet. The System compares it to a hidden creature's Stealth or a concealed trap's DC whenever you walk into a room.
- The System also uses **passive Investigation** and **passive Insight** freely, so that "anything weird about this room?" and "is this guy lying?" don't always need a roll. This holds at every table, whether you play in chat, by voice or face to face. Rolling is still how you look *harder*. {{HOUSE}}

::: system
The System has computed your passive Perception. It has also computed what you missed. Would you like to know? No. You would not.
:::

## Working Together

### Helping

When you **Help** an ally with a check, pick one of your skill or tool proficiencies that fits the task. Your ally has **Advantage** on their next check with that skill or tool, as long as they make it before the start of your next turn and you are close enough to help in a way that makes sense. The GM decides whether help is possible; two people can't pick one lock faster, but two people can lift one shelf.

### Group Checks

When the whole party tries something together (sneaking down a corridor, climbing a shaft, searching a big room), the GM can call for a **group check**. Everyone rolls. **If at least half the group succeeds, the whole group succeeds.** Otherwise the group fails. Group checks let the strong carry the weak without anyone making twelve separate rolls.

::: sidebar Group Checks and the Session Order
Group checks happen outside the session turn order (Chapter 1). The System resolves them in one beat and moves on. Individual checks during exploration still happen on each Crawler's turn.
:::

## Contests

Sometimes two creatures want opposite things: you are trying to hide and a guard is trying to spot you, or you are holding a door shut while a mob pushes on it. That is a **contest**. Both sides make the appropriate check; the higher total wins. **On a tie, nothing changes**: the situation stays as it was before the contest.

| Situation | Your check | Their check |
|---|---|---|
| Sneaking past a lookout | Dexterity (Stealth) | Wisdom (Perception) |
| Telling a convincing lie | Charisma (Deception) | Wisdom (Insight) |
| Palming an item while watched | Dexterity (Sleight of Hand) | Wisdom (Perception) |
| Wrestling over a weapon | Strength (Athletics) | Strength (Athletics) |
| Holding a door shut | Strength (Athletics) | Strength (Athletics) |
| Slipping out of a crowd's grip | Dexterity (Acrobatics) | Strength (Athletics) |

## Actions That Call for Checks

Several SRD 5.2 actions are built around an ability check. Each one takes your action on your turn.

| Action | Check | Use it to |
|---|---|---|
| **Search** | Wisdom: Insight, Medicine, Perception or Survival | Look for something you can sense: a hidden creature or object, an ailment, someone's state of mind, tracks or food |
| **Study** | Intelligence: Arcana, History, Investigation, Nature or Religion | Think hard about something: a spell, an item, a clue, a creature, a symbol |
| **Hide** | Dexterity (Stealth), DC 15 | Conceal yourself (see below) |
| **Influence** | Charisma (Deception, Intimidation, Performance or Persuasion), or Wisdom (Animal Handling) for a Beast or Monstrosity | Urge a creature to do something it is hesitant about |
| **Utilize** | Varies | Use an object or tool, including System terminals, levers and vending machines |

**Hiding.** To Hide, you must be heavily obscured or behind three-quarters or total cover, and out of any enemy's line of sight. Succeed on a **DC 15 Dexterity (Stealth)** check and you have the **Invisible** condition. Note your total: it becomes the DC for anyone trying to find you with Wisdom (Perception). You stop being hidden if you make a sound louder than a whisper, make an attack roll, cast a spell with a Verbal component, or get found.

**Influence.** The GM decides whether the creature is **willing** (it just does it), **unwilling** (no check will make it), or **hesitant** (you roll). A hesitant creature's DC is **15 or its Intelligence score, whichever is higher**. If you fail, you can't urge it in the same way again for a while, usually a day. Roleplay first; the check settles what the conversation could not.

::: sidebar Influence and the System
The System is not a creature and has no Intelligence score worth mentioning. You cannot Influence it. You can, however, file a complaint at any System terminal, where it will be read aloud for comedic effect.
:::

## Tools

A **tool** is a kit that lets you do something you otherwise could not: Thieves' Tools for locks and traps, Herbalism Kit for remedies, Disguise Kit for faces, Tinker's Tools for gadgets. Each tool in the SRD names the ability it uses and what you can do and make with it.

- **Tool proficiency** adds your Proficiency Bonus to checks made with that tool.
- **Tool plus skill.** If you are proficient with the tool *and* with a skill that applies to the same check, you have **Advantage** on it. Picking a lock with Thieves' Tools while you also know Sleight of Hand is the classic case.
- **No tool, no check.** Some tasks are impossible without the right tool. You can't pick a lock with your opinion of it.

Crafting in the Crawl runs on these same tool proficiencies, at saferoom workstations, with a no-roll default called **Steady Hands**. Chapter 6 covers tables, recipes and crafting skills.

## System Skills

In the source series, the System keeps its own list of **skills**: specific, often ridiculous talents with numbered ranks, from fighting with your fists to lacing your boots. They grow with use, from potions and from training, and they usually top out at 15. {{INSPIRED}}

System skills sit on your sheet under **Skills**, each with a rank. They don't replace the eighteen skills, proficiency or Expertise; those still carry most checks, and your Proficiency Bonus still climbs with your level. A System skill is narrower: one talent the System has noticed you have, like Lockpicking, Cartography or Vending Machine Diplomacy, growing on its own track.

### The Skill Track

**Earning a rank.** A System skill rises **one rank** when you earn it in play: {{INSPIRED}}

- **Meaningful use.** You lean on the skill when it matters and it makes the difference. Hard or clever use counts; routine use doesn't.
- **A first-time feat.** You pull off something for the first time. That can raise a skill, or hand you a new one at rank 1.
- **Inventive crafting.** You build something new. Real invention can raise more than one skill at once.
- **Potions.** A **Skill Potion** adds 1 rank to a skill. A **Cheat Code Potion** adds 3 ranks to a random skill. You don't pick.
- **Guild training.** A training guild the GM places teaches you a rank, usually with strings attached.

**No grinding.** There are no use counters. Swinging at a hundred rats adds up to a hundred dead rats and nothing else. The GM grants every rank, the System announces it, and it applies at the next safe point, where the GM records it on your sheet. {{HOUSE}}

::: system
Skill up! Lockpicking is now rank 5. The door you were working on has filed a complaint.
:::

**Caps.** A System skill tops out at **rank 15**. A skill in your species' or class's own family can climb to **rank 20**: a Hobgoblin's traps and explosives, for example. Pushing a skill past 15 the hard way, through real fights, is a very rare achievement: **You now tread in the realm of gods.** {{INSPIRED}}

**What a rank does.** Each rank widens what the skill can do, and the GM tells you what the new rank opens up. At **ranks 5, 10 and 15** the skill also adds **+1** to d20 checks made with it, so the bonus stacks to +3. {{HOUSE}}

| Rank | Bonus to d20 checks with the skill |
|---|:---:|
| 1–4 | +0 |
| 5–9 | +1 |
| 10–14 | +2 |
| 15–20 | +3 |

The crafting skills and the Cockroach Clause below are System skills with their own short rank scales. Where their rules say something different, their rules win.

### Crafting Skills

These are the System skills a crafter is most likely to see. All of them are GM-granted. The full rules, and the tables and terms they refer to, are in Chapter 6. {{INSPIRED}}

| Skill | Ranks | What it does | Earliest |
|---|:---:|---|---|
| **Explosives Handling** | 1–5 | 1: tell an explosive's tier and stability by looking. 2: Advantage to disarm, defuse or safely carry explosives. 3: pick up and re-place your own armed mines and traps without setting them off. 4: +1 to explosive recipe checks. 5: unlocks the Demolitions Workshop menu at a Sapper's Table. | Rank 5 from Floor 4 |
| **IED** | I–III | Your crafted explosives deal extra damage equal to your rank × half their damage dice (rounded down, minimum 1), and count as one stability step better per rank against early detonation. | Rank II from Floor 4; rank III from Floor 9 |
| **Bomb Surgeon** | — | Take apart an explosive at a Sapper's Table for half its ingredients, or split one into two of the next tier down. | — |
| **Infusion** | I–II | −2 to the DC of infusions per rank; infused items leave the table one stability step better. | — |
| **Alchemy** | — | +1 to alchemy checks; Quick recipes can be made without a table (still in a saferoom). | — |
| **Trap Engineer** | — | Thieves' Tools trap recipes treat your Sapper's Table as one level higher. | — |
| **Agent Provocateur** | — | +1 Sapper's Table level (ignoring the usual cap) and the right to design Very Rare bomb recipes at a level 5 Sapper's Table. One Crawler per party, from a quest or a Benefactor only. | Floor 6 |

Ranks usually come quickly at first. A Crawler typically gains rank 1 of Explosives Handling with their first bomb, then about one rank per floor of real use. {{HOUSE}}

### The Cockroach Clause

The most famous System skill in the source is a death-cheat: once a fight, a chance to shrug off a blow that should have killed you. Our version is the **Cockroach Clause**, a permanent boon in two tiers. {{INSPIRED}}

- **Tier 1.** Once per combat (or, outside combat, once per Short Rest), when a hit or effect would reduce you to 0 hit points or kill you outright from massive damage, you drop to **1 hit point** instead.
- **Tier 2.** As Tier 1, but the **first** such blow in each combat (or each Short Rest outside combat) deals you **no damage at all**. If a second fatal blow lands in the same combat, Tier 1 applies to it, but only once per Long Rest.

Nobody starts with it. The GM grants it as a reward, or a Crawler trains it. Each time the Clause fires counts as a **use**; after five uses, the GM may upgrade Tier 1 to Tier 2. It can also come from a rare training potion, or from a training guild the GM places, at **3,000 credits for Tier 1** and **10,000 credits for Tier 2**, always with strings attached. Like every near-death buffer, it stops a death but never undoes one, and it does nothing against effects that kill without dealing damage. Chapter 9 covers buffers in full. {{HOUSE}}

::: system
Cockroach Clause invoked. You have been informed that you are not allowed to enjoy this.
:::

## Achievements

The System is watching, and the System takes notes. When a Crawler does something **notable**, the System may announce an **achievement**: a banner, a line of commentary, and sometimes a reward. Achievements are how the show tells you it noticed. They are also how most of the Crawl's treasure arrives. {{INSPIRED}}

::: achievement Achievement Unlocked: Achievements
You opened the chapter about achievements. Studying for the test is a choice.

Reward: Nothing. You have been seen, and that is worse.
:::

### Guidelines, Not a Vending Machine

The single rule that governs every achievement: **the System decides.** It decides what is notable, when to say so, and what (if anything) it pays. The achievement catalog the System works from is a **seed list and tone guide**, not a contract. The System may award a catalog entry as written, rename it, change it, or invent a brand-new achievement on the spot. Meeting an entry's criteria never means you are *owed* it. {{HOUSE}}

- **Many achievements pay nothing.** A snark-only banner is a feature. The System enjoys them more than you do.
- **Achievements never grant XP**, and they never turn a failed check into a success.
- **Players can't request rewards.** Asking the System for a specific prize is itself an achievement candidate, and the reward is a joke at your expense.

### What Counts as Notable

The System toasts a moment when it is one of these:

| Kind | Examples |
|---|---|
| **Firsts** | First kill, first loot box, first saferoom, first death save, first time a feature does its thing |
| **Extremes** | Overkill, surviving at 1 hit point, beating something far above your weight, a flawless fight |
| **Creativity** | A plan the rules allow but nobody expected; using the environment; talking a boss down |
| **Comedy** | A running bit, a perfect one-liner, a spectacular failure |
| **Character** | A choice that defines who your Crawler is: mercy, cruelty, loyalty, refusing a sponsor |
| **Mystery** | Touching something the System cares about. These toast *without* explaining why. |
| **The show's agenda** | Whatever Production wants to encourage, or punish, on this floor |

Routine competence is not notable. A normal hit or a passed Easy check gets no banner unless it is your first.

### When the System Announces

| Timing | What it's for |
|---|---|
| **Instant toast** | Snark, small rewards, firsts and comedy. In a fight, the System waits for the end of the round rather than interrupting a turn. |
| **Saferoom claim** | Anything with real loot. The achievement is announced at once; the box or item is **claimed and opened in a saferoom**. |
| **Pending review** | Big or mysterious deeds. "This achievement is under review by Production." It may pay off floors later. |
| **Floor recap** | At descent, the System may post a Floor Summary with stragglers, statistics and a few parting insults. |

**How often.** Expect roughly **one to three toasts per Crawler per session**. The System spreads the spotlight around: a Crawler who hogs the banners finds the System getting bored of them, and noticing someone else.

**Away from the table.** A Crawler running on **Standing Orders** while their player is away still fights and can still die, but earns only snark-only achievements.

### The Toast

Every achievement is read out the same way: a banner, the achievement's name, one line describing what you did (usually phrased as an accusation), and the reward.

::: achievement Strategic Retreat Specialist
You left a fight at full health and nobody laid a hand on you. The audience respects your cardio.

Reward: Their respect, which is non-transferable and worth exactly nothing.
:::

::: achievement Loot Goblin
You opened a crate in the middle of combat.

Reward: You are being attacked.
:::

::: achievement Customer Feedback
You asked the System for a specific reward.

Reward: Your request has been received, logged and laughed at.
:::

Keep toasts short. One line of description and one reward line is the standard; the System saves longer speeches for the moments that earn them.

### The Reward Ladder

When an achievement pays, the System sizes the reward on a seven-step ladder. {{HOUSE}}

| Tier | Name | What you get | Typical use |
|:---:|---|---|---|
| R0 | **Snark-only** | Nothing. Logged. Maybe a cosmetic Title. | Humor, failures, cowardice, brag entries, repeats |
| R1 | **Pocket change** | A few credits and/or a Title | Small firsts, notable-but-routine feats |
| R2 | **Heroic Inspiration** | 5e Heroic Inspiration, as written | Great roleplay, crowd-pleasing stunts, brave choices |
| R3 | **Consumable** | A potion, scroll, ammunition, oil or other one-use item at the floor's rarity | Clever play, survival, crafting |
| R4 | **Minor boon** | A Crawl Charm (below) or a small blessing-style perk | Rare achievements, character moments |
| R5 | **Loot box** | A box, Bronze and up (tier by floor, below) | Big achievements, bosses, floor clears |
| R6 | **Headliner** | A specific magic item at the floor's peak rarity, a permanent Blessing, a story unlock, or (level 19+) an extra Epic Boon | Campaign-defining moments |

**Ladder rules.**

- The System may move a reward **one tier up or down** from the catalog's suggestion freely, and two tiers with a reason.
- **Real mechanical power only comes from R2 to R6.** R0 and R1 are flavor and pocket money.
- **Heroic Inspiration from achievements** arrives at most **once per session** per Crawler, on top of the usual 5e sources.
- The catalog's usual R1 seed is **a Title plus 25 credits** at Floor 1 scale.

### Titles

A **Title** is a cosmetic name the System pins to your Crawler ("Blooded," "Oriented," "Fine Print"). Titles show on your sheet and in the System's announcements. They are cosmetic by default; NPCs and the audience may react to them. A rare Title may carry a tiny narrative effect (a faction recognizes it, a bartender comps you a drink), but **never a number on your sheet**.

### Credits and the Floor Multiplier

Credits in an achievement reward are written at **Floor 1 scale** and multiplied as you descend. The same multiplier applies to System fees. **Credits pulled out of a loot box do not get the multiplier**: box amounts are final on every floor. {{HOUSE}}

| Floors | Achievement credits and System fees |
|---|:---:|
| 1–4 | × 1 |
| 5–9 | × 5 |
| 10–14 | × 20 |
| 15–18 | × 50 |

So a "Title + 25 credits" achievement pays 25 credits on Floor 2, 125 on Floor 6 and 1,250 on Floor 15. All credits are whole numbers (Chapter 1).

### Achievement Boxes

When an achievement pays a loot box (R5), the box's tier depends on how big the deed was and where you did it. The catalog marks each achievement **Common**, **Rare** or **Legendary**. That tag is the *achievement's* rarity, not a box tier. {{HOUSE}}

| Achievement rarity | Usual reward | Box if one is paid: Floors 1–2 | Floors 3–8 | Floors 9–14 | Floors 15–18 |
|---|---|---|---|---|---|
| Common | R0–R1 (R2 if great) | No box by default | No box by default | No box by default | No box by default |
| Rare | R2–R5 | Bronze | Silver | Silver (Gold from Floor 10) | Gold |
| Legendary | R5–R6 | Bronze | Gold | Platinum | Legendary box or Headliner, within the caps |

- **Achievement boxes on Floors 1–2 are Bronze.** Silver there comes only from the Boss Box, or from a GM override with a stated reason. Expect about two or three achievement boxes per Crawler per floor; this is a soft guideline, and the System may pay another for a great moment.
- **The floor's ceiling always wins.** If an achievement names a box above what the floor allows, the System pays the highest tier the floor allows instead. No Platinum boxes are awarded on Floors 1–8.
- **Every box is named for the deed** that earned it, and the System reads the name aloud: a *Bronze Stabbed the Vending Machine Box*, a *Silver Technically Alive, Spiritually Gone Box*. Cheap boxes get short jabs. Expensive ones get long, breathless, insulting names.
- **Boxes open only in a saferoom**, all of them at once, lowest tier first. A box is bound to the Crawler who earned it. What comes out is ordinary loot. Chapter 6 covers the rest.

::: system
Congratulations! Your box has been named after your worst decision of the day. Competition was fierce.
:::

### Rarity Ceilings by Floor

Every ordinary reward respects the floor's **rarity ceiling**, whether it comes from an achievement, a boss, a vendor or a box. (A sponsor's Benefactor Box is the one ordinary exception; Chapter 6 explains.) The **default** column is what a meaningful drop usually is; the **peak** is the best the System will hand out, as a Headliner or boss loot, about once per Crawler per floor arc. {{HOUSE}}

| Floors | Default rarity | Peak rarity | Notes |
|---|---|---|---|
| 1–2 | Common | Uncommon | Consumables dominate; one Uncommon per Crawler by the end of Floor 2 is fine |
| 3–5 | Uncommon | Rare | The first Rare usually comes from a floor boss or a Legendary achievement |
| 6–9 | Rare | Very Rare | Sponsors and hunters bring the shiny stuff |
| 10–14 | Very Rare | Legendary | Legendary items stay rare: about one per Crawler across this band |
| 15–18 | Very Rare or Legendary | Legendary (Artifacts only through the story) | Endgame loadouts |

### Tailored Rewards

The System personalizes rewards. **Same achievement, different Crawler, different prize.** Two Crawlers who earn the same toast may get different items of the same tier: one gets the crossbow, the other gets the hat. The System fits rewards to your build and to a **hidden Fan Profile** that it builds itself, from play. You never see the profile, you can't edit it, and nothing you say at the table will make the System admit it exists. Tailoring changes *which* item you get, never how much power the floor hands out. {{INSPIRED}}

::: system
Congratulations! You are the only Crawler on this floor to receive this item. Nobody else wanted one. Please stop crying, you're scaring the audience.
:::

### Fair Play

The System is petty, but it keeps the books honest. {{HOUSE}}

- **No farming.** Repeat a stunt on purpose and it pays snark after the first time. "Again? Production has seen this episode."
- **No double dipping.** The same achievement never pays the same Crawler twice. The same *kind* of deed on a new floor can pay again, possibly smaller.
- **No self-harm for loot.** A stunt that endangers the party just to trigger a toast pays snark and may draw a complication.
- **No catalog hunting.** Players who read the catalog and hunt its rows get roasted. The catalog belongs to the System.
- **Shared deeds.** When two Crawlers earn something together, both get the toast. Tangible rewards are split or tailored separately.
- **No take-backs.** Removing an awarded achievement needs the table's agreement or a clear rules error.

### Example of Play

Here is how checks and achievements fit together at the table. The System is the GM; Dev, Ines and Rook are three Crawlers on Floor 1.

> **System:** The corridor ends in a shuttered snack kiosk. Something behind the shutter is chewing. Dev, it's your move.
>
> **Dev:** I take the Help action for Ines. I'll hold the bottom of the shutter so it doesn't rattle when she lifts it. I'm proficient in Stealth.
>
> **System:** Noted. Ines, your move. Rook, your passive Perception tells you the chewing just stopped.
>
> **Ines:** I lift the shutter quietly and look in.
>
> **System:** Lifting it is easy. Doing it quietly is not: Dexterity (Stealth), DC 15, and Dev's help gives you Advantage. Rolls 9 and 17, take the 17, plus 5: 22. The shutter goes up without a sound. Inside: four rats the size of beagles, and a crate.
>
> **Rook:** My move. I throw a lit flare into the kiosk, drag the shutter back down and lean on it.
>
> **System:** The rats push back. Strength (Athletics) contest. Your 18 beats their 11. The kiosk is now an oven, and the rats have stopped pushing.

::: achievement Closed for Renovations
You locked a room full of mobs in with a fire and held the door.

Reward: Bronze Pest Control Is a Lifestyle Box. Claim it at the next saferoom.
:::

> **System:** Rook gets the toast. The box goes into Rook's System Inventory unopened. It opens at the next saferoom, with any other boxes Rook is holding. Dev, the crate is yours to loot when the smoke clears.

The example shows the habits this chapter describes: the System names the check and DC up front, rolls in the open, uses passive Perception to share a clue, resolves a Help and a contest in session order, toasts once the moment is over, and holds the box for a saferoom. It also shows the most important rule of achievements: nothing on the sheet said this would earn one. The System decided it did.

## Crawl Charms and Blessings

A **Crawl Charm** is the System's favorite R4 reward: a small, one-use or few-use supernatural gift, built like the Charms of the fifth edition *Dungeon Master's Guide*. Unless a Charm says otherwise, it vanishes when its uses run out **or when you descend**, whichever comes first. **You can hold two Charms at once.** {{HOUSE}}

| Charm | Effect |
|---|---|
| **Second Season** | Once: when you would drop to 0 hit points, drop to 1 hit point instead. |
| **Commercial Break** | Once: gain a Short Rest's benefits in 1 minute (out of combat only). |
| **Fan Mail** | Twice: gain Heroic Inspiration when you otherwise wouldn't; you still can't hold more than one. |
| **Slow-Mo Replay** | Once: as a Reaction, after you see a d20 result within 30 feet, force a reroll. |
| **Product Placement** | Once: pull any mundane item worth 25 credits or less from your System Inventory, even if you never had one. |
| **Stage Lighting** | 3 uses: as a Bonus Action, outline a creature you can see in light until the end of your next turn. Attacks against it have Advantage, and it can't benefit from being Invisible. |
| **Contract Fine Print** | Once: Advantage on a check to find a loophole, read a contract, or argue with a System terminal. |
| **Laugh Track** | Once: as an action, one creature within 30 feet makes a Wisdom save (DC 8 + your Proficiency Bonus + your highest mental ability modifier) or has the Incapacitated condition until the end of its next turn, laughing. |
| **Map Leak** | Once: reveal the nearest saferoom or stairwell on your System Map. |
| **Stunt Double** | Once: when a creature hits you with an attack, an ally within 5 feet may take the damage instead (their choice). |
| **Sponsor's Bottle** | Once: as a Bonus Action, a Potion of Healing appears in your hand. It is branded. |
| **Encore** | Once: regain one expended spell slot of level 2 or lower, or one use of a feature that recharges on a Short Rest. |

**Blessings** are permanent R6 rewards, built like the *Dungeon Master's Guide*'s Blessings. Three examples: **Recognized** (your Broadcast Name works twice per Long Rest instead of once), **Iron Stomach** (Advantage on saving throws against the Poisoned condition), and **Lucky Number** (once per Long Rest, treat a d20 roll of 1 as a 10). {{HOUSE}}


## Sample Achievements

Here is a starter set drawn from the System's catalog, chosen for Floors 1 and 2 and for achievements that work on any floor. It is a **seed list**, not a menu. The System decides what is notable, and it will rename these, adapt them, skip them and invent new ones. The full catalog runs to well over a thousand entries, and the System keeps it to itself.

**How to read the table.** *Floor* is where the entry fits best ("Any" travels). *Rarity* is the achievement's own tag (Common, Rare, Legendary). *Typical reward* is the catalog's suggestion before the System tailors it:

- **Snark only:** a banner and a line, nothing else (R0).
- **Title + 25 credits:** pocket change at Floor 1 scale (R1); the credits take the floor multiplier.
- **Box + Title:** an achievement box at the floor's tier, which is **Bronze on Floors 1–2** (R5).
- **Big box + Title + flair:** the Legendary-achievement box for the floor (Bronze on Floors 1–2, Gold on 3–8) plus a cosmetic flourish.

Achievement names marked † borrow the *shape* of a deed from the source series; the names and wording here are ours. {{INSPIRED}}

<!-- Source rows (tables/achievements.csv v1.4), in table order:
     Combat: ACH-0001 0002 0003 0004 0005 0019 0170 0171 0173 0174 0207 0861.
     Exploration: ACH-0006 0007 0008 0025 0177 0183 0218 0088 0087 0239.
     Social: ACH-0009 0010 0011 0187 0189 0222 0226 0902 0905.
     Survival and Party: ACH-0015 0016 0017 0018 0020 0196 0198 0899.
     Loot and Crafting: ACH-0012 0013 0034 0077 0080 0192 0193 0202 0203 1827 1828 1835.
     Humor and Meta: ACH-0014 0021 0022 0023 0024 0030 0032 0033 0035 0079 0085 0197 0204 0205 0873 0895 0898 0086.
     Once ever: ACH-1824 1825 1826.
     Criteria translated from the catalog's v0.1 stat words per core 3.9 (Presence -> Charisma; "5+ levels above you" -> CR; "Named item" -> named magic item of Uncommon+). Floor-specific notes, encounter wiring and spoilers are not printed. Excluded on purpose: pet / companion rows, Story Seed rows, rows with known rarity outliers. -->

### Combat

| Achievement | Floor | What you did | Rarity | Typical reward |
|---|:---:|---|---|---|
| First Blood | Any | Landed the killing blow on your first mob. | Common | Title (Blooded) + a junk weapon oil |
| Overkill Artist | Any | Dealt at least three times a target's remaining hit points in one hit. | Rare | Box + Title |
| Crowd Control King | Any | Put a controlling condition on five or more enemies in one fight. | Rare | Box + Title |
| David vs Goliath | Any | Killed a creature whose CR is at least your level + 5 (at levels 1–4, at least twice your level). | Legendary | Big box + Title + flair |
| No Hit Wonder | Any | Won a fight without taking any damage. | Rare | Box + Title |
| Combo Meal | Any | Finished a kill together with an ally in the same round. | Rare | Box + Title |
| Boss Claim | 1 | Defeated the floor's boss or gate guardian. | Rare | Box + Title |
| Minion Mower | 1 | Defeated 25 ordinary enemies on one floor. | Common | Title + 25 credits |
| Environmentalist | 1 | Killed an enemy with a floor hazard. | Rare | Box + Title |
| Perfect Ambush | 1 | Started a fight hidden and won it without an ally dropping. | Rare | Box + Title |
| Elite Hunter | 2 | Defeated three elite enemies on Floor 2. | Rare | Box + Title |
| Lost Initiative, Won Anyway | 1 | Lost initiative and still won the fight. | Common | Title + 25 credits |

### Exploration

| Achievement | Floor | What you did | Rarity | Typical reward |
|---|:---:|---|---|---|
| Cartographer's Scratch | Any | Revealed half of a floor's map. | Common | Title + 25 credits |
| Full Fog Breaker | Any | Revealed an entire floor's map. | Legendary | Map cosmetic + box |
| Secret Door Sniffer | Any | Found three hidden doors on one floor. | Rare | Box + Title |
| Saferoom Skeptic | Any | Walked into a saferoom and immediately searched it for traps. | Rare | A tool upgrade (trap kit) |
| Hidden Cache | 1 | Found a hidden loot cache. | Common | Title + 25 credits |
| Locksmith | 1 | Opened five locked containers on one floor. | Common | Title + 25 credits |
| Stair Seeker | 2 | Located the stairwell before the floor's boss was dead. | Rare | Box + Title |
| Saferoom With Teeth | 2 | Discovered that a saferoom was hiding a hazard. | Common | Title + 25 credits |
| Trap Sense Tingling | 2 | Disarmed three traps on Floor 2. | Rare | Box + Title |
| Slow Burn | 2 | Took the long route on purpose and still cleared the floor. | Common | Title + 25 credits |

### Social

| Achievement | Floor | What you did | Rarity | Typical reward |
|---|:---:|---|---|---|
| Silver Tongue | Any | Succeeded on five Charisma checks in one session. | Common | Title + 25 credits |
| Barter Baron | Any | Haggled a vendor's price down by a quarter or more. | Rare | Box + Title |
| Name Dropper | Any | Invoked your Broadcast Name for a social benefit (Floor 3 and later). | Rare | Box + Title |
| Vendor Regular | 1 | Bought from the same vendor twice. | Common | Title + 25 credits |
| Peaceful Path | 1 | Ended a hostile encounter by talking. | Rare | Box + Title |
| Local Contact | 2 | Gained a named NPC ally. | Common | Title + 25 credits |
| Rumor Mill | 2 | Collected three rumors on one floor. | Common | Title + 25 credits |
| Pay a Fine | 1 | Paid a fine. On purpose or otherwise. | Common | Title + 25 credits |
| The Honest Option | 1 | Told the truth when a lie would have been safer. | Common | Title + 25 credits |

### Survival and Party

| Achievement | Floor | What you did | Rarity | Typical reward |
|---|:---:|---|---|---|
| Down But Not Out | Any | Were stabilized from 0 hit points. | Common | Title + 25 credits |
| Close Call | Any | Survived at exactly 1 hit point. | Common | Title + 25 credits |
| Wipe Adjacent | Any | Were the only one left standing after a near-wipe. | Legendary | Big box + Title + flair |
| Buddy System | Any | Stabilized an ally or got them back on their feet. | Common | Title + 25 credits |
| Sacrifice Play | Any | Took a hit that would have dropped an ally. | Rare | Box + Title |
| Ironman Cub | 1 | Cleared Floor 1 without anyone in the party dropping to 0 hit points. | Legendary | Big box + Title + flair |
| Poison Tolerant | 1 | Suffered a poison or disease and got it cured. | Common | Title + 25 credits |
| Share the Snacks | 1 | Shared your food with the party. | Rare | Box + Title |

### Loot and Crafting

| Achievement | Floor | What you did | Rarity | Typical reward |
|---|:---:|---|---|---|
| Pocket Lint | Any | Looted your first container. | Common | 25 credits |
| Named Drop | Any | Obtained a named magic item of Uncommon rarity or better. | Rare | Box + Title |
| Loot Council | Any | Let the party vote on who gets a named item. | Common | Title + 25 credits |
| Vending Gore | 1 | Looted a vending machine on Floor 1. | Common | Title + 25 credits |
| Crowbar Starter | 1 | Equipped a junk melee weapon as your first weapon. | Common | Title + 25 credits |
| Junk Architect | 1 | Looted fifteen junk items on one floor. | Common | Title + 25 credits |
| Full Sellout | 1 | Sold ten items to vendors on one floor. | Common | Title + 25 credits |
| Field Craft | 1 | Crafted or cooked something for the first time on this floor. | Common | Title + 25 credits |
| Kit Bash | 1 | Combined two junk items into something useful. | Rare | Box + Title |
| Dungeonpreneur † | Any | Invented a new weapon, device or potion (first time). | Rare | The System decides: usually a Title, sometimes an ongoing trickle of credits |
| Grease Monkey † | Any | Built a wheeled lure, bomb or similar contraption and sent it into a fight (once ever). | Rare | Box + Title |
| You Call That a Trap? † | Any | Hurt a mob with a trap or hazard you left lying around on purpose. | Rare | Box (floor tier) |

### Humor and Meta

| Achievement | Floor | What you did | Rarity | Typical reward |
|---|:---:|---|---|---|
| Hoarder | Any | Carried twenty different junk items at once. | Common | Snark only |
| Bad Idea Bear | Any | Proposed a plan everyone agreed was terrible, then pulled it off. | Rare | Box + Title |
| Tutorial Complete | Any | Finished Floor 1 alive. | Common | Title (Oriented) |
| Season Ticket | Any | Played five sessions. | Common | Title + 25 credits |
| Rules Lawyer Adjacent | Any | Cited a line of this book that changed a ruling. | Rare | Title (Fine Print) |
| The Audience Is Watching | Any | Caused a ratings spike. | Rare | Heroic Inspiration, with applause |
| Achievement for Achievements | Any | Earned 25 achievements in one campaign. | Common | Title (Collector) |
| Patch Notes Incoming | Any | Survived a rule change in the middle of a floor. | Rare | Box + Title |
| Murder-Show Smile | Any | Delivered a post-kill one-liner the table was still quoting later. | Common | Snark only |
| Don't Skip Intro | 1 | Read or listened to an entire System tutorial popup. | Common | Snark only |
| First Down | 1 | Dropped to 0 hit points on Floor 1. | Common | Snark only |
| Bleed Tax | 1 | Used up three healing items on one floor. | Common | Snark only |
| Floor Bit | 1 | Started a running joke the table kept using. | Common | Snark only |
| Scenic Panic | 1 | Panicked out loud before a fight you then won. | Common | Snark only |
| Camera Shy | 1 | Destroyed a camera or a drone. | Common | Snark only |
| Critical Failure | 1 | Rolled a natural 1 at the worst possible moment. | Common | Title + 25 credits |
| Too Proud to Heal | 1 | Refused healing out of pride. | Common | Title + 25 credits |
| Soft Open Survivor | 2 | Cleared Floor 2. | Common | Title + 25 credits |

### Once Ever

A few achievements can only be earned **once per Crawler, ever**, however many floors you see.

| Achievement | Floor | What you did | Rarity | Typical reward |
|---|:---:|---|---|---|
| Not Unpacking † | Any | Took a stairwell down within one in-game hour of arriving on a floor. | Legendary | A Platinum box, paid at the floor's ceiling tier, + Title |
| Down Is a Direction † | Any | Found a stairwell down to the next floor. | Common | Snark only |
| Left Before the Cake † | Any | Went down a stairwell more than six hours before the floor collapsed. | Rare | Title (Left Before the Cake) |

::: system
Congratulations on finding the stairs! They go down. So, eventually, will you.
:::

::: house Inventing Achievements
The best achievements are the ones nobody planned. When the table laughs, gasps or groans at something a Crawler did, that is an achievement. Give it a name that sounds like an accusation, write one line saying what happened, pick a tier from the ladder, and keep the reward inside the floor's ceiling. Most invented achievements should be snark-only or a Title. Save the boxes for deeds the table will still be talking about next session.
:::

## Quick Reference

| Rule | Summary |
|---|---|
| Ability check | d20 + ability modifier + Proficiency Bonus (if proficient) vs DC |
| DCs | 5 / 10 / 15 / 20 / 25 / 30: Very easy to Nearly impossible |
| Calling the check | The System names ability, skill and DC first when the Crawler would know the stakes; dice in the open; dice stand |
| Natural 20 or 1 | No special effect on ability checks |
| Expertise | Double Proficiency Bonus for that skill |
| Passive check | 10 + modifiers (+5 Advantage, −5 Disadvantage) |
| Help | Ally gets Advantage on their next check with a skill or tool you're proficient in |
| Group check | At least half succeed, everyone succeeds |
| Contest | Higher total wins; a tie changes nothing |
| Tool + skill | Advantage when you're proficient in both |
| System skills | +1 rank for meaningful use, a first-time feat, inventive crafting, a potion or guild training; GM grants it, no counters; cap 15 (20 for your species' or class's family); +1 to checks at ranks 5, 10, 15 |
| Achievements | The System decides; many pay nothing; never XP; no requests |
| Reward ladder | R0 snark · R1 pocket change · R2 Heroic Inspiration · R3 consumable · R4 Charm · R5 box · R6 Headliner |
| Credit multiplier | Achievement credits and System fees × 1 / 5 / 20 / 50 by floor band; box credit pulls never |
| Achievement boxes | Bronze on Floors 1–2 (Silver only from the Boss Box or a stated GM override); floor ceiling always wins; open only in a saferoom |
| Charms | Hold two; gone when used up or at descent |

::: system
That concludes the skills portion of your evaluation. Your score has been recorded. You may not see it. It is very funny.
:::
