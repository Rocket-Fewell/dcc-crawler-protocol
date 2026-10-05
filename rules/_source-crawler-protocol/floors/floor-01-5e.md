# Floor 01 — The Orientation Pit (5e Module, Level 1 → 2)

> **Status:** Full draft for Caleb's markup. **Replaces** `floors/floor-01.md` (stub, now superseded).
> **Project:** *Crawler Protocol: Season Zero*. Original fan RPG inspired by *Dungeon Crawler Carl*. Private play only; not affiliated with or endorsed by the author or publishers.
> **Rules base:** `02-core-rules-5e.md` **v0.2.4**. This doc's **Special Floor Rules (§2) override `02` while Floor 1 is active** (`02` §0). Everything else: `02`, then 5e 2024.
> **Characters:** built with `03-character-creation-5e.md`.
> **Spine:** `05-campaign-narrative.md` (F1 = trainer/tutorial only; plant Odd Coin + Benefactor static).
> **Comfort:** `COMFORT=Ludicrous` default, per-crawler private opt-out (see `03` §2.3–2.4 and §11.1 here).
> **Party:** written for **4 crawlers**; scaling for 2–6 in §9.

> *System note:* "Welcome to the Orientation Pit, where we teach you everything you need to survive, and then watch you fail to use it. Statistically, one of you will die here. We have a pool going. Please don't look at the pool."

---

## Table of contents

0. Module at a glance
1. Before the start: Death Mode selection ("Service Plans")
2. Special floor rules
3. Running the System on Floor 1 (cast, voice, popups)
4. Map and flow
5. Zones, encounters, and read-aloud (Zones 0–11, S, W)
6. Boss: Dean Thudd ("Versus" card, intro, tactics)
7. Stairwell exit and Floor Summary
8. Loot plan, boxes, and spine-object plants
9. Encounter math and party-size scaling
10. Achievement seeds (catalog + NEW)
11. DM notes (comfort, failure modes, pacing, session state)
12. Changelog
13. Open for owner markup

---

## 0. Module at a glance

| Item | Value |
|------|-------|
| **Objective** | Find the stairwell. Survive. (Graduate.) |
| **Level** | Arrive **1**; **level 2 at the Green Room** (mid-floor milestone, §2 rule 3); descend at 2 |
| **Length** | 2–4 sessions of chat play |
| **Encounters** | 5 combats (4 core + boss) + 1 wandering type + 4 traps/hazards + 1 rescue; mostly Low/Moderate, **1 High** (boss) |
| **Monsters** | SRD 5.2 reskins, CR 1/8 – 2 (`02` §8.3 F1 row) |
| **Saferooms** | 2: **The Break Room** (Zone 6) and **The Green Room** (Zone 9) |
| **Loot** | Bronze Welcome Box + 0–2 achievement Bronze boxes per crawler; **Silver Boss Box**; 3 *Potions of Healing* placed + 2 for sale; credits from mobs |
| **Spine plants** | **Odd Coin** (Zone 3), **Benefactor Signal** (first death save / Zone 8), **Broadcast Name** (audience-nickname plant, all zones), **Black Box** (glimpse only, Zone 10) |
| **Teaches** | d20 tests, Advantage/Disadvantage, Help, action economy, Opportunity Attacks, cover, traps + saves, death saves, permanence, boxes, achievements, saferooms, Short/Long Rest, level-up, stairwell |
| **Floor clock** | **Off** (Lights-Out cycle only, §2 rule 6) |

---

## 1. Before the start: Death Mode selection ("Service Plans")

> **Campaign default already picked:** this campaign runs **Costly Revives (very costly and rare)**. The table already chose it: `DEATH-MODE=Costly Revives` and `COMFORT=Ludicrous` are logged as defaults (Caleb, 2026-10-03; `02` §6.0, shared `decisions/002-death-mode.md`). **For this campaign, confirm and log them; skip the vote below** unless the table asks to change it. The "Canon Hard (default)" wording in the pitch below is the generic default for tables with nothing logged.

**Do this before Zone 0, ideally as the first step of intake** (`03` §2.1). The table picks **one** mode (`02` §6.0) and the System logs `DEATH-MODE`. It can't change mid-campaign without table agreement. Run it **out of character first** (plain explanation, no snark), then replay it in voice for flavor.

### 1.1 Plain explanation (DM reads, no snark)

> Before we start: how permanent is death? Three options.
> 1. **Canon Hard** (default): dead is dead. If your crawler dies, you make a new one who joins at the next saferoom.
> 2. **Costly Revives**: death can sometimes be undone once revival magic is available (Floor 5 at the earliest), and it always costs something real.
> 3. **Soft Open**: death isn't final; you come back at the next saferoom with penalties.
>
> Separately: **Floor 1 Reprieve**, a one-time "you're not dead, you're unconscious at a saferoom" save, Floor 1 only. Recommended if anyone is new to 5e.
> Majority wins. Ties go to Canon Hard.

### 1.2 In-voice version (read-aloud from every kiosk at once)

> The kiosk screen goes dark, then floods with sparkles. A cartoon gravestone with googly eyes bounces onscreen.
>
> "**SELECT YOUR SERVICE PLAN!** Every crawler is covered by one of our exciting death packages!
>
> **CANON HARD:** Our most popular plan, mostly because it's free. You die, you stay dead, we play sad piano music for six seconds, and then we cut to someone hotter.
>
> **COSTLY REVIVES:** For the crawler who wants a second chance and doesn't mind being billed for it forever. Some restrictions apply. All of the restrictions apply.
>
> **SOFT OPEN:** Death is more of a *suggestion*. You come back tired, broke, and slightly less popular, like a divorced uncle at Thanksgiving.
>
> Please select as a group. If you can't agree, we'll pick Canon Hard and you'll deserve it."

If **Floor 1 Reprieve** is ON:

> "Also, because some of you look like you've never held anything sharper than a spork, we're offering **Tutorial Mercy**: one free not-death per crawler, valid on this floor only. It comes with a Title. You will hate the Title."

### 1.3 Log

```text
DEATH-MODE: <Costly Revives (campaign default) | Canon Hard | Soft Open>
F1-REPRIEVE: <ON | OFF>
```

Reprieve (`02` §6.2): once per crawler, Floor 1 only, a death becomes "unconscious, ejected to the nearest saferoom at 1 HP" with a humiliating Title. Suggested Titles: *Participation Corpse*, *Mostly Dead Intern*, *Rescued by Paperwork*. Toast: *"[Name] was, for legal reasons, not dead. Please do not take this as a precedent."*

---

## 2. Special floor rules (override `02` while on Floor 1)

1. **Tutorial popups.** The first time a rule comes up (first d20 test, first Advantage, first Opportunity Attack, first cover, first death save, first Short Rest, first box), the System posts a **one-to-two line** explainer (§3.3). Second time: no popup. Third time someone asks: snark.
2. **Training-grade loot.** Floor ceiling per `02` §3.6: **default Common, peak Uncommon**. **Boss Box = Silver** (§6.7), overriding `02` §4.7's "floor boss → Gold or Platinum," which would breach the F1 ceiling.
3. **Mid-floor milestone (Floor 1 split).** Per `02` §2.3 (floor docs may split the level): **reaching the Green Room (Zone 9) after the elite grants level 2**, applied there ("Midterm Onboarding"). **Descent grants no further level**; crawlers arrive on Floor 2 at level 2, as `02` §2.2 expects. Why: a CR 2 boss vs. four level-1 crawlers (450 XP vs. a High budget of 400) is beyond High; at level 2 it's High (§9). **Table option:** keep `02` §10.3 strictly (level 2 at Floor 2 Onboarding) and run **Boss Variant B** (§6.6).
4. **Telegraphs.** Area attacks are telegraphed **one round ahead** (`02` §8.2 tutorial rule).
5. **Saferooms are honest on Floor 1.** "Saferooms can lie" starts on F2 (`02` §5.6). Searching one still earns a toast.
6. **Floor clock: off.** Instead, a **Lights-Out cycle**: every 8 hours of in-game time, the Pit goes dark for 1 hour (red emergency light = dim light). During Lights-Out, outside saferooms, roll d6 every 30 minutes: on 1–2, **Ceiling Ticks** (§5.11).
7. **Long Rests only in saferooms** (`02` §5.6). A Long Rest attempted elsewhere is interrupted by Ceiling Ticks after 1d4 hours.
8. **Permanence explainer.** The first time a **named** NPC dies near the party, post the permanence popup (§3.4) (carried over from `04-floor-bible.md` F1 special rules).
9. **No Broadcast Name feature.** The audience-nickname plant (§8.5) is cosmetic; the feature unlocks on F3 (`02` §5.1).
10. **Benefactor Signal has no mechanics on F1.** Static only; no intervention (`02` §5.5: interventions come with the F6 choice).

---

## 3. Running the System on Floor 1

### 3.1 Cast

| Name | What it is | Stat block | Job |
|------|-----------|------------|-----|
| **The System** | The DM's voice. Game-show host by way of a hostile HR department. | — | Toasts, popups, Versus cards, box names, roasts |
| **Proctor Bell** | The floor's **trainer**: a carnival fortune-teller automaton in a glass booth on ceiling rails; painted face, brass bell for a hat, one creaky pointing arm. Rolls ahead of the party zone to zone. | Object (AC 15, 40 HP, immune to poison and psychic). Not a combatant. Damage "self-heals" at the end of the turn. | Delivers each lesson. **Feed it 1 credit** for a **hint**: one true, useful sentence about the current zone. Max 1 hint per crawler per zone. |
| **Dale Pruitt** | NPC crawler, 50s, HVAC tech, cargo shorts, encyclopedic about ductwork, zero combat ability. Wheezes. Kind. Believes in exits. | **Commoner** (CR 0) | Rescue target (Zone 4); tag-along; natural candidate for the **permanence lesson** if the party doesn't protect him. **Never kill him by fiat**: only dice or choices. |
| **Tanya Ruiz** | A crawler who died before the party woke up; face-down in the vending arcade. | Corpse | **Corpse Lesson** (corpse cache), lore scrap |
| **Dean Thudd** | The boss. Head of Orientation. | **Ogre** (CR 2) reskin | §6 |
| **The Audience** | Never seen; heard as laugh tracks, gasps, boos, and the occasional horny wolf-whistle. | — | Crowd Pop, nicknames, the foot bit |

### 3.2 Voice on Floor 1

- **Helpful-aggressive.** The System *does* teach the rules; it just makes you feel stupid for needing them.
- `COMFORT=Ludicrous`: curse freely, be crude, roast cowardice and failure hard. Roast the **deed**. One killer line beats four okay ones (`02` §9).
- **Popups stay short.** Rules text in popups is plain and accurate; the joke goes on the last line.
- **The foot bit:** the System occasionally reports "audience engagement data" about crawlers' feet (who's barefoot, whose sneakers are "trending," who got a sock wet). Deadpan, like ratings. **At most once per session.**

### 3.3 Standard popups (first time each comes up)

```text
╔══ TUTORIAL: D20 TEST ══════════════════════════════╗
  Roll a d20, add your modifier, beat the DC. That's it.
  That's the whole game. You'd be amazed how many people
  still fuck it up.
╚════════════════════════════════════════════════════╝
```

```text
╔══ TUTORIAL: ADVANTAGE ═════════════════════════════╗
  Roll two d20s, keep the higher. Disadvantage: keep the
  lower. They don't stack. Two Advantages is still one
  Advantage. Stop asking.
╚════════════════════════════════════════════════════╝
```

```text
╔══ TUTORIAL: OPPORTUNITY ATTACK ════════════════════╗
  Leave an enemy's reach without Disengaging and it gets
  a free swing at you with its Reaction. Running away is
  allowed. It's just very, very expensive.
╚════════════════════════════════════════════════════╝
```

```text
╔══ TUTORIAL: COVER ═════════════════════════════════╗
  Half cover: +2 AC and Dex saves. Three-quarters: +5.
  Total: they can't target you at all. Hide behind
  things. Things love you. People don't.
╚════════════════════════════════════════════════════╝
```

```text
╔══ TUTORIAL: YOU ARE DYING ═════════════════════════╗
  At 0 HP you're Unconscious and make a Death Saving
  Throw at the start of each of your turns: d20, 10+ is
  a success. Three successes: stable. Three failures:
  dead. Natural 20: you wake up with 1 HP. Natural 1:
  two failures. Taking damage while down: a failure
  (two if it's a crit). An ally can stabilize you with
  a DC 10 Wisdom (Medicine) check, or heal you.
  Your friends have about six seconds to give a shit.
╚════════════════════════════════════════════════════╝
```

```text
╔══ TUTORIAL: SHORT REST ════════════════════════════╗
  One hour of not being murdered. Spend Hit Point Dice
  to heal (roll each + Con modifier). Some features come
  back. In a saferoom nobody interrupts. Outside, lol.
╚════════════════════════════════════════════════════╝
```

```text
╔══ TUTORIAL: LOOT BOXES ═══════════════════════════╗
  Boxes go to your System Inventory and open ONLY in a
  saferoom, during a rest. You open all of them at once.
  You can't trade them. If you die holding them, we keep
  them. We always keep them.
╚════════════════════════════════════════════════════╝
```

### 3.4 Permanence popup (first named NPC death)

```text
╔══ SYSTEM NOTICE: PERMANENCE ═══════════════════════╗
  [NAME] is dead. Not respawning. Not "on a break."
  Dead. The body stays. The inventory drops where they
  fell. This applies to you.
  [Canon Hard:] There is no refund.
  [Costly Revives:] Refunds open on Floor 5. They are
  priced accordingly.
  [Soft Open:] YOU get a do-over. [NAME] didn't have
  your plan. Sucks to be [NAME].
  We now return you to your regularly scheduled panic.
╚════════════════════════════════════════════════════╝
```

### 3.5 Nameplates

Per `02` §8.4: **Level = CR rounded up, minimum 1**. Format: `Name. Level N. "Tagline."` Bosses get **Boss**; the elite gets **Elite** (flavor tag).

---

## 4. Map and flow

### 4.1 Zone list

| # | Zone | Lesson | Type | Required? |
|--:|------|--------|------|:---------:|
| 0 | Intake Hall | Lesson 0: Paperwork | Intake (see `03`) | Yes |
| 1 | The Atrium | Lesson 1: d20 Tests | Exploration + skill checks | Yes |
| 2 | Vent Row | Lesson 2: Combat 101 | Combat (Low) | Yes |
| 3 | Vending Gore Arcade | Lesson 3: Loot | Hazard + loot + **Odd Coin** + secret cache (3b) | Yes (cache optional) |
| 4 | Hall of Fair Warnings | Lesson 4: Traps & Saves | Traps + rescue (Dale) | Yes |
| 5 | Shooting Gallery | Lesson 5: Range & Cover | Combat (Low, top of band) | Yes |
| 6 | **The Break Room** | Lesson 6: Rest & Boxes | **Saferoom A**; Welcome Box | Yes |
| 7 | The Big Green EXIT | Lesson 7: Don't Trust Signs | **Stair bait**: trap + ambush (Low) | Optional (it's bait) |
| 8 | Mascot Locker Room | Lesson 8: Dying | **Elite** (Moderate) + **Benefactor Signal** | Yes |
| 9 | **The Green Room** | Midterm Onboarding | **Saferoom B**; level 2 | Yes |
| 10 | Graduation Stage | Final Exam | **Boss** (High) + **Black Box** glimpse | Yes (or bypass, §7.2) |
| 11 | The Stairwell | Commencement | Exit; Stairwell Checkpoint | Yes |
| S | Service Corridor | — | Side path; service stairwell | Optional |
| W | Ceiling Ticks | — | Wandering encounter | Random |

### 4.2 Flow (fog of war reveals zones as entered)

```text
                 [0 Intake Hall]
                        |
                  [1 The Atrium]
                        |
                   [2 Vent Row]
                        |
         [3 Vending Gore Arcade]--(secret DC 15)--[3b Lost & Found, back cage]
                        |
          [4 Hall of Fair Warnings]
                        |
              [5 Shooting Gallery]
                        |
             [6 THE BREAK ROOM]  (saferoom A)
               /                \
   [7 Big Green EXIT]      [8 Mascot Locker Room]
   (bait; dead end)                 |
                           [9 THE GREEN ROOM]  (saferoom B)
                                    |
                          [10 Graduation Stage]----[S Service Corridor]
                                    |                       |
                             [11 STAIRWELL] <----- (service stair, locked)
```

- Each zone is one "room" made of a few 30–60 ft areas; give distances in feet.
- **Fog of war:** reveal a zone on the System Map when entered (`02` §5.7); log `MAP`. Zones 3b and S stay hidden until found.
- **Par time** (for `ACH-0200` Speed Clear): reach the Stairwell having taken **no more than one Long Rest** on Floor 1.

---

## 5. Zones, encounters, and read-aloud

Read-aloud is in quote blocks; adapt freely. **DM** notes are rules-facing.

### 5.0 Zone 0 — Intake Hall (Lesson 0: Paperwork)

Run `03-character-creation-5e.md` (Death Mode first, §1 here). End intake with the booth doors opening.

> The booth door clunks open on its own. Beyond it: a long hallway of identical booths, most of them empty, a few of them... not empty, in a way you don't want to look at for long. Overhead, a banner sags: **ORIENTATION PIT — WHERE FUTURES BEGIN!** Someone has spray-painted "AND END" underneath, and someone else tried and failed to scrub it off.

**DM:** Crawlers meet here. Give each player one beat to describe their crawler stepping out. Start the **audience-nickname plant** (§8.5): the hallway screen misspells one crawler's name.

### 5.1 Zone 1 — The Atrium (Lesson 1: d20 Tests)

> A three-story concrete atrium around a dead fountain, coins fused to its bottom by something that was never water. Ceiling speakers play smooth jazz at a volume that feels like a threat. On ceiling rails, a glass booth glides toward you with a squeal. Inside sits a painted wooden fortune-teller with a brass bell for a hat and a face that's been touched up too many times. Its jaw clacks.
>
> "**WELCOME, LITTLE LAMBS,**" it says, in a voice like a music box with a head cold. "**I AM PROCTOR BELL. I WILL BE TEACHING YOU TO LIVE. BRIEFLY.**"

**Proctor Bell's lesson:** "The way out is that shutter. It is stuck. Everything here is stuck, or locked, or lying. Try."

| Obstacle | Check | Notes |
|----------|-------|-------|
| Rolling security shutter, jammed halfway | **Strength (Athletics) DC 10** | Teach **Help**: a second crawler can Help for Advantage. Popups: D20 TEST, ADVANTAGE. |
| Wall directory (smeared, graffitied) | **Intelligence (Investigation) DC 10** | Reveals Zones 1–6 on the System Map and the words "GREEN ROOM — STAFF ONLY." |
| Fountain coins | **Dexterity (Sleight of Hand) DC 12** | 2d6 credits total, corroded. Fail: 1 slashing damage from a sharp edge, and a toast. |
| Proctor Bell | — | 1 credit: a hint ("The rats in the next hall hate light and love ankles."). |

**Seeds:** `ACH-0079` Don't Skip Intro (R0) for sitting through Proctor's whole spiel; `NEW: Coin Slot` (R0) for paying Proctor to shut up before it finishes.

### 5.2 Zone 2 — Vent Row (Lesson 2: Combat 101)

> The shutter screams up into the ceiling. Beyond it: a service hallway lined with floor vents, every grate bent outward like something punched its way out. Something skitters. Then a lot of somethings skitter. Little red UI brackets pop up over the vent openings.

**Encounter: Vent Rats** (Low)

| Creature | SRD 5.2 stat block | CR | # (4 crawlers) | XP |
|----------|--------------------|:--:|:--:|---:|
| **Vent Rat** | **Giant Rat** | 1/8 | 6 | 150 |

Nameplate: `Vent Rat. Level 1. "Union member. Will bite your ankle and then file a grievance."`

**Tweak:** they emerge in two groups of three from vents 20 ft apart. Same stats.

**DM:** First combat. Roll initiative for everyone in one post, print the order and the **crawler blocks** (`02` §2.5.2). Popup OPPORTUNITY ATTACK the first time someone backs away from a rat. Pack Tactics makes rats ugly in groups; let crawlers learn flanking the hard way. Rats carry nothing; the vents hold **1d6 × 2 credits** of dropped change.

**Seeds:** `ACH-0001` First Blood (R1: Title *Blooded* + a flask of oil, "junk weapon oil"); `ACH-0894` Land a Critical Hit (R0); `ACH-0205` Scenic Panic (R0) for whoever panics in chat before winning; `ACH-0860` Win Initiative (catalog R1; **downgrade to R0** here, too routine to pay).

> *System, after the fight:* "Six rats. Congratulations. You are now qualified to work night shift at a Chuck E. Cheese."

### 5.3 Zone 3 — Vending Gore Arcade (Lesson 3: Loot)

> A long hall lined with vending machines, maybe thirty of them, humming and blinking in a dozen colors. Half have been smashed open. The other half are intact, glowing, and very slightly breathing. Crumpled snack wrappers drift around a body face-down in the middle of the floor: a woman in scrubs, one arm still stretched toward a machine that says **SNAKK-MATIC — YOU DESERVE THIS**.

**1. Tanya Ruiz's body (Corpse Lesson).** Her corpse cache (`02` §5.9): a Mop-Handle Staff (Quarterstaff), 11 credits, a **lore scrap**, and one **Potion of Healing** reskinned as "Sports Drink, Red Flavor." Looting her: `ACH-0083` Corpse Lesson (**R0**).

**Lore scrap** (Tanya's handwriting; read-aloud):

> *day 1?? the bell thing says the machines are friendly. the machines are NOT friendly. the green EXIT is a trick. the big man on the stage counts before he swings. he COUNTS. if you find this tell my sister I wasn't scared. I was very scared.*

Finding it: `ACH-0871` (catalog Rare; **R1** on F1). Reading it aloud: `ACH-0872` (catalog Legendary; **R2 Heroic Inspiration** if done with feeling, **R0** if done as a bit).

**2. Hungry Vendors (hazard).** Six intact machines can be looted by reaching in. Each reach: **Dexterity saving throw DC 11** or the machine bites (1d4 bludgeoning) and the arm is stuck, **Restrained**, until a **Strength (Athletics) DC 10** check (Action). Prying a machine open instead: **Strength (Athletics) DC 13** or Thieves' Tools **DC 12**; it's loud (one Ceiling Ticks roll, §5.11).

Each successful loot, roll d6:

| d6 | Result |
|:--:|--------|
| 1–2 | 1d6 credits |
| 3 | A ration ("snack cake, expiration date: yes") |
| 4 | A mundane item: hooded lantern (big flashlight), 50 ft of rope (extension cord), caltrops (a bag of LEGO) |
| 5 | A Common consumable: Alchemist's Fire ("Energy Drink, Do Not Shake") or a flask of oil |
| 6 | A cosmetic **tailored pull** from someone's Fan Profile (`02` §3.5): the first hint that the System is listening |

**Cap:** about 40 credits of value per crawler from the machines; after that they read **SOLD OUT FOREVER**.

**Seeds:** `ACH-0077` Vending Gore (R1: Title + 25 credits); bitten: `NEW: Fed the Machine` (R0).

**3. Lost & Found Bin (Odd Coin).** A wire cage by the change machine, stuffed with junk: single shoes (the foot audience is *very* interested), keys, a retainer, a lanyard. At the bottom, a battered **loot crate** stenciled **UNCLAIMED**. Opening it (no check): a handful of junk and **one dull, stamped coin**, heavier than it should be, its face worn smooth except for a tiny notch at the rim.

```text
╔══ ITEM ════════════════════════════════════════════╗
  Vendor Oddity (Unappraised)
  A coin. Probably. Value: ???
  This item cannot be sold. Please don't try. It's
  embarrassing for everyone.
╚════════════════════════════════════════════════════╝
```

Log `SEED-ODDCOIN` (holder). Toast `ACH-0081` Odd Coin Pocketed as a **hidden** line: *"Oddity logged."* No reward; story flag (`02` §3.2 item 6). **Never explain it.** If someone tries to sell it to the Snakk-Matic terminal, it either refuses ("ITEM NOT RECOGNIZED") or offers a suspicious **500 credits** and cancels mid-animation (`02` §5.5).
**Fallback:** if nobody opens the crate, the coin shows up as a "Weird" pull in the first box opened in the Green Room, or in Dale's pocket if he dies. It **must** be planted on F1.

**4. Secret: back cage (3b).** A false panel behind the change machine: **Wisdom (Perception) DC 15** (passive counts) or **Intelligence (Investigation) DC 13** if someone says they're checking behind machines. This is the floor's **one DC 15 secret** (`02` §10.3). Inside, the **hidden cache**: a **Potion of Healing** ("Sports Drink, Blue Flavor, Do Not Ask"), a **Shield** (riot shield stenciled PROPERTY OF ORIENTATION), 3d6 × 5 credits, and a scrawled map that reveals Zone S on the System Map.
**Seeds:** `ACH-0177` Hidden Cache (R1); `ACH-0179` Side Path (R1) when Zone S is revealed.

### 5.4 Zone 4 — Hall of Fair Warnings (Lesson 4: Traps & Saves)

> A long, clean, well-lit corridor, about 100 feet, caution tape along both walls and a row of cheerful signs: **WARNING! TRAP!** — **SERIOUSLY! TRAP!** — **WE ARE NOT KIDDING ABOUT THE TRAP!** Halfway down, a man in cargo shorts hangs upside down in a net from the ceiling, slowly rotating. He sees you and waves, which makes him spin faster.
>
> "Hi! Hi. Dale. Dale Pruitt. Don't step on the — yeah. The square ones. Don't step on the square ones."

**Proctor Bell:** "Traps. The signs are honest. You will ignore them anyway. Everyone does."

**Traps** (homebrew in the 2024 DMG style; sized for level 1)

| Trap | Detect | Effect | Disarm / bypass |
|------|--------|--------|-----------------|
| **T1 "Welcome Mat"**: pressure plates → swinging WET FLOOR sign (×3 plates) | The signs announce it; **Wisdom (Perception) DC 10** spots the exact plates | **Dexterity save DC 12**: fail = 2d6 bludgeoning and **Prone**; success = half, not Prone | Wedge a plate: Thieves' Tools or **Dexterity (Sleight of Hand) DC 11**; with junk (gum, a shoe) **DC 13** |
| **T2 "Ticket, Please"**: turnstile with a hidden needle | **Intelligence (Investigation) DC 13** | **Constitution save DC 11**: fail = 1d4 poison and **Poisoned** for 1 hour | Thieves' Tools DC 12; or vault it with **Strength (Athletics) or Dexterity (Acrobatics) DC 12** |
| **T3 Snare net** (holding Dale) | Obvious | **Restrained**; escape with **Strength (Athletics) DC 10** | Cut it: AC 10, 5 HP, slashing. Dale is 10 ft up: the fall is 1d6 bludgeoning unless someone catches him (**Strength (Athletics) DC 10**). |

**Rescue Dale.** The puzzle: one T1 plate sits right under him. Dale has 4 HP; a WET FLOOR sign will probably drop him, and the fall could too. **Telegraph it**; let them plan.

- Rescued: `ACH-0869` (catalog Rare → **R1** on F1: 25 credits + Title *Lifeguard*). Dale tags along (Commoner; carries stuff; knows buildings: **Advantage on one check per zone** involving vents, doors, or machinery).
- Not rescued / Dale dies: `ACH-0870` (**R0**; the catalog's 25 credits for a dead guy is tasteless even for the System). Run the **permanence popup** (§3.4). Play the audience honestly: a laugh track that cuts off a beat too late.
- Eating a clearly signed trap: box-name candidate **Bronze Maybe Read the Sign Next Time Box** (`02` §4.8) if it's somehow box-worthy; usually just `NEW: Literacy Optional` (R0).
- Poisoned, then cured: `ACH-0198` Poison Tolerant (R1). Disarming with junk: `ACH-0877` (R1).

> *System, when someone triggers a signed trap:* "The sign said TRAP. The second sign said SERIOUSLY. The third sign was, frankly, begging. Your mother can read, right? So it skipped you. Got it."

### 5.5 Zone 5 — Shooting Gallery (Lesson 5: Range & Cover)

> The corridor opens into a carnival shooting gallery scaled up to a 60-by-40-foot room: plywood cutouts of crawlers on squeaking conveyors, overturned stall counters, sandbags, a cash register on a stool. Behind the far counter, four department-store mannequins in staff polos turn their heads toward you all at once, with the sound of someone dropping a tray of silverware. Each raises a pink plastic toy bow that is very clearly not a toy.

**Encounter: Mannequin Staff** (Low, top of band)

| Creature | SRD 5.2 stat block | CR | # | XP |
|----------|--------------------|:--:|:--:|---:|
| **Mannequin Staff** | **Skeleton** | 1/4 | 4 | 200 |

Nameplate: `Mannequin Staff. Level 1. "Smiling through it. Contractually."`

**Terrain:** counters and sandbags = **half cover**; the brick prize booth = **three-quarters cover**. A crawler standing on a conveyor is carried 10 ft along it at the end of each round (no save; narrated like a carnival prize). The mannequins open with their bows from behind the far counter (half cover) and only close to melee if crawlers do.

**Proctor Bell:** "Cover. Get behind things. Things are your friends. People are not your friends."

**DM:** Popup COVER the first time someone uses it. Skeletons are vulnerable to bludgeoning (as written); let the crowbars shine. The cash register (**Dexterity (Sleight of Hand) DC 10**, or smash it) holds **2d6 × 3 credits** and a raffle ticket that does nothing. The System never explains the raffle ticket. It's a joke. Probably.

**Seeds:** `ACH-0867` Block a Hit with a Shield (R1); `ACH-0861` Lose Initiative and Still Win (R1); `NEW: Hit the Cutout` (R0).

### 5.6 Zone 6 — The Break Room (Saferoom A; Lesson 6: Rest & Boxes)

> A door with a cartoon coffee cup on it. Inside: carpet the color of a bruise, a sagging couch, a fridge covered in passive-aggressive notes, a vending terminal with a cheerful screen, a corkboard, and a single ceiling speaker that crackles. The door thunks shut behind you and a green light above it blinks on. A soft chime. Then a voice, warm as a hug from someone who's about to pick your pocket:
>
> "**SAFEROOM CERTIFIED.** Nothing can hurt you in here. Except each other. And your choices. And the coffee."

**Services** (`02` §5.6):

- **Rest:** Short Rest guaranteed uninterrupted; **Long Rest available** (one per 24 hours, 5e). Popups: SHORT REST, LOOT BOXES.
- **Welcome Box:** every crawler receives a **Bronze Welcome Box** here and opens it during the rest (`02` §10.2; §8.1). **It must include one tailored pull** (`03` §5.3).
- **Snakk-Matic terminal (vendor):** 5e prices ± mood. *Potion of Healing* 50 credits (**2 in stock for the whole floor**, shared with the Green Room), ammunition, rations, torches, rope, healer's kit, caltrops. Buys at half. Haggling: Charisma (Persuasion, Deception, or Intimidation) **DC 13**; success = 15% off (`02` §5.10). Identify an item: 10 credits.
- **Corkboard (rumors; `ACH-0188` Rumor Mill at 3):**
  1. "THE GREEN EXIT IS NOT THE EXIT. — management" (true)
  2. "Thudd can't do stairs." (false; he just hates them)
  3. "The mascot in the locker room is EMPTY. Nobody's in it. Nobody's EVER been in it." (true)
  4. "Staff corridor behind the stage. Key's in the costume." (true; §5.8)
  5. "Bring a bigger stick." (true for everyone)
- **Fridge:** one sandwich labeled "DALE'S. DO NOT." Eating it in front of Dale: `NEW: Lunch Thief` (R0). Splitting food with the party: `ACH-0899` (catalog Rare → **R1**).
- **Searching for traps:** `ACH-0025` Saferoom Skeptic (catalog "trap kit upgrade" → **R1** on F1: a free Thieves' Tools or Healer's Kit refill). It's honest on F1, which the System points out smugly.

**First box ceremony (script):**

> The lights dim. A drumroll plays from a speaker clearly not built for bass. A pedestal rises out of the carpet with a cheap bronze box on it, tied with a ribbon that's been used before.
>
> "**IT'S BOX TIME!** Crawler [Name], you have earned: the **Bronze Welcome Box!** Every crawler gets one. Every crawler. Even you. *Especially* you. Open it."

Roll pulls publicly (`02` §4.2; Bronze = 1–2 pulls). Read the tailored pull slowly, with relish. `NEW: First Box` (R0): *"You opened your first box and your pupils went full slot machine. We have that on camera. It's going in the promo."*

### 5.7 Zone 7 — The Big Green EXIT (Lesson 7: Don't Trust Signs)

> Down a side passage from the Break Room, a huge glowing sign: **EXIT**, friendly green, with an arrow pointing down a concrete stairwell. Fresh air drifts up from below. Somewhere down there, birds are singing. Actual birds. It smells like cut grass and freedom.
>
> Proctor Bell's booth rolls up beside you and says nothing. For the first time, it says nothing at all.

**Truth:** it's bait. Twenty feet of stairs end at a landing over a **10-ft pit (T4)**, with a speaker playing birdsong and a fan blowing grass-scented air. **Exit Greeters** wait in alcoves on the landing.

| Trap / Encounter | Details |
|------------------|---------|
| **T4 "Trapdoor of Opportunity"** | Landing floor. **Wisdom (Perception) DC 13** to see the seams (Advantage if they read Tanya's note or the rumor). Fall 10 ft: 1d6 bludgeoning, **Prone**, broken glass below (difficult terrain). Climb out: **Strength (Athletics) DC 10**. |
| **Exit Greeters** (Low) | **Goblin Warrior** ×2 (CR 1/4) + **Goblin Minion** ×4 (CR 1/8) = **200 XP**. Orientation staff in green vests and EXIT-sign hats, carrying clipboards. They attack when someone drops through the trapdoor or reaches the landing. |

Nameplates: `Exit Greeter. Level 1. "Has a quota."` / `Exit Greeter (Trainee). Level 1. "Has a quota and a dream."`

**Walking away:** anyone who looks at the EXIT and **leaves without going down**, especially after reading Tanya's note or the rumor: `ACH-0084` Stair Bait Resisted (catalog Rare → **Bronze box**, the floor's best "smart play" reward). Name it after the deed: e.g., **Bronze Didn't Fall for the Birdsong Box**.

**Going down anyway:** box-name candidate **Bronze You Opened the Door Marked "Do Not" Box** (`02` §4.8 #3) if the fight goes well; otherwise `NEW: Freedom Smelled Like a Fan` (R0).

**Loot:** each Greeter carries 1d6 credits; one clipboard holds a "quota" list of Intake Tags with columns marked GRADUATED and NOT. Almost all are NOT. Flavor (counts as a lore scrap for `ACH-0871` if not yet earned).

**DM:** If Dale is with the party, this is where he's most likely to die: he hears birds and *runs*. Don't force it. A crawler within reach can grab him (Reaction, or **Strength (Athletics) DC 10** if adjacent). If he dies: permanence popup.

### 5.8 Zone 8 — Mascot Locker Room (Lesson 8: Dying)

> A locker room that smells of foam rubber and old sweat. Rows of dented lockers. Benches. A mirror wall cracked in a starburst. Hanging from a meat hook in the middle of the room is a giant, faded mascot costume: a grinning cartoon pit bull in a graduation cap, eight feet tall, mesh eyes, mouth frozen in a yell of joy. As you watch, it unhooks itself. It drops to the floor with a soft, padded **thump**. There's nobody inside. You can see straight through the mesh eyes to the lockers behind it.
>
> On a bench, two lanyards rise into the air, their plastic ID badges unfolding into razor edges.

**Proctor Bell** (fast, from the doorway): "This lesson is about dying. Try to learn it only a little."

**Encounter: The Elite** (Moderate)

| Creature | SRD 5.2 stat block | CR | # | XP |
|----------|--------------------|:--:|:--:|---:|
| **Bruiser the Mascot (Unoccupied)** | **Animated Armor** | 1 | 1 | 200 |
| **Lanyard Blade** | **Animated Flying Sword** | 1/4 | 2 | 100 |
| | | | **Total** | **300** |

Nameplates: `Bruiser the Mascot (Unoccupied). Level 1. Elite. "Go team. Go AWAY, team."` / `Lanyard Blade. Level 1. "Visitor access only."`

**Tweak:** Bruiser is padded foam over something heavy; flavor only, numbers unchanged. The cracked mirror shows crawlers' reflections a half-second late, and for one frame, a tail, a horn, a pointed ear (species tease, `03` §7.3). The camera cuts away. No mechanics.

**The death-save lesson.** This is the fight most likely to drop someone. When the first crawler hits 0 HP, post **YOU ARE DYING** (§3.3) and roll death saves publicly. Bruiser fights to the end but doesn't deliberately pound downed crawlers unless they're the only targets left; the Lanyard Blades are dumb and might (telegraph it: "*the blade swings toward [Name]'s body*").

**Benefactor Signal** (spine plant, `SEED-BENEFACTOR`). **Trigger:** the **first death saving throw made on Floor 1** (most likely here), heard only by the dying crawler. If nobody goes down in this fight, fire it at the **end of round 2** to whichever crawler has the lowest HP. **No mechanical effect** (§2 rule 10).

> Under the roar of the fight and the laugh track, your ear fills with static, a dead-channel hiss that swallows everything for one heartbeat. A broken crest flickers across your vision: half a shape, like a wax seal snapped in two. And a voice that isn't the System's, very far away and very tired:
>
> `…HOLD… NOT YET…`
>
> Then the noise of the fight slams back in. Nobody else seems to have heard it.

The System **doesn't acknowledge it**. If asked: *"No such broadcast exists. Please consult a physician."* Log `SEED-BENEFACTOR: fired F1 (<crawler>, zone 8)`. Toast `ACH-0082` Static in the Ear as a **hidden** line, *"Signal logged,"* no reward. **Fallback:** if it somehow never fires, the static plays from the Green Room speaker during the box ceremony.

**Loot:** inside Bruiser's head, where a person should be: a **service key** on a lanyard (opens the Zone S door) and a **Potion of Healing** ("Sports Drink, Green Flavor"). Lockers: **Wisdom (Perception) DC 10** per locker bank for 2d6 credits and a mundane item; three banks max before a Ceiling Ticks roll.

**Seeds:** `ACH-0078` Tutorial Elite (R1: Title *Mascot Hunter* + 25 credits); `ACH-0085` First Down (**R0**); `ACH-0015` Down But Not Out (R1); `ACH-0018` Buddy System (R1) for the stabilizer; `ACH-0016` Close Call (R1) at exactly 1 HP; `ACH-0020` Sacrifice Play (catalog Rare → **Bronze box**).

> *System, at the first death save:* "Ladies, gentlemen, and the gentleman in row J who's been very quiet about his foot thing: [Name] is DYING! Place your bets! Not you, [Ally]. You help. Help them, you absolute coward."

### 5.9 Zone 9 — The Green Room (Saferoom B; Midterm Onboarding)

> Behind a STAFF ONLY door: a backstage green room. A mirror ringed with bulbs, half of them dead. Folding chairs. A fruit plate that has become something else. A framed photo on the wall: a huge man in a mortarboard shaking hands with a long line of crawlers, every one of them crossed out in red marker. The green light blinks on above the door.
>
> "**SAFEROOM CERTIFIED.** Congratulations on reaching your Midterm. Statistically, this is where we start losing people. So, you know. Enjoy the fruit."

**Midterm Onboarding (level 2).** Apply level 2 to every living crawler here during the first rest (§2 rule 3).

```text
╔══ LEVEL UP ════════════════════════════════════════╗
  You are now Level 2. More HP (roll your Hit Die or
  take the fixed value, + Con), one more Hit Point Die,
  and whatever your class gets at 2. Read it. We're not
  reading it to you.
  The audience has noticed you are slightly less bad.
╚════════════════════════════════════════════════════╝
```

**Services:** as the Break Room (rest, Snakk-Matic sharing the floor's 2-potion stock, identify), plus **box opening** for anything earned since Zone 6. Proctor Bell's booth is parked here facing the wall, humming. One credit buys its **last hint**: *"He counts before he swings. Count with him."*

**The photo:** **Intelligence (Investigation) DC 12** spots Tanya Ruiz in the line, not yet crossed out, and the date on the frame: *today*. Dread only; no mechanics.

**Replacement crawlers** join here if anyone died (`02` §6.3): level 2 (party's lowest), 5e starting equipment, and a Silver late-entry compensation box (opened at the next rest in a saferoom).

### 5.10 Zone S — Service Corridor (side path)

Revealed by the 3b map, or by **Wisdom (Survival) or Intelligence (Investigation) DC 12** while scouting the stage's edges. A narrow utility hall behind the stage, pipes and junction boxes, one locked door to the **service stairwell** that drops to Zone 11.

- Opens with **Bruiser's service key**, or **Thieves' Tools DC 15**, or **Strength (Athletics) DC 15** (10 minutes; loud; Dean Thudd and his starting Ushers come looking 1 minute later).
- Finding the stairwell before beating the boss: `ACH-0180` Stair Seeker (catalog Rare → **Bronze box**).
- Dale, if alive, knows it's there: "Every building has one. Every. Building." (Advantage on finding it.)

### 5.11 Wandering — Ceiling Ticks

| Creature | SRD 5.2 stat block | CR | # | XP |
|----------|--------------------|:--:|:--:|---:|
| **Ceiling Tick** | **Stirge** | 1/8 | 4 | 100 (Low) |

Nameplate: `Ceiling Tick. Level 1. "Clingy. Needy. Sucks. Your ex, basically."`

Used for Lights-Out rolls, interrupted field Long Rests, and noisy looting. **Max two wandering encounters on the floor**; after that, the System narrates distant skittering and an audience groaning with disappointment.

---

## 6. Boss: Dean Thudd, Head of Orientation (Zone 10)

### 6.1 The stage (read-aloud)

> Heavy curtains part onto a high-school auditorium blown up to the size of an aircraft hangar. Rows of empty seats climb into darkness, but the darkness is full of tiny red camera lights, hundreds of them, all pointed at you. The stage is 60 feet wide and 40 deep: a podium, a stack of rolled diplomas, a folding table of trophies, and along the front edge an orchestra pit, 10 feet deep. A camera drone hovers over center stage, lens whirring. High above, a booth window glows: **BROADCAST**.
>
> Spotlights slam on. A bass-heavy walk-up song kicks in. From the wings, ducking under the proscenium arch, comes something enormous in a straining academic gown and a mortarboard three sizes too small, dragging a club made of a podium bolted to a flagpole. Dozens of graduation cords hang around its neck, every color. It sniffs the air, smiles with too many teeth, and taps a laminated name tag on its chest: **HELLO, MY NAME IS: DEAN.**

### 6.2 System intro (full host voice)

> "**LADIES! GENTLEMEN! AND THE FOOT PEOPLE!** It's the moment you've all been waiting for: **GRADUATION DAY!**
>
> In this corner: a handful of confused, sweaty, barely-trained nobodies who've survived *nine whole rooms* on luck, spite, and somebody's emotional-support crowbar!
>
> And in *this* corner: he's flunked eleven hundred crawlers, he's never taken a sick day, and he's legally required to tell you he's *very* proud of you right before he turns your skull into a bean bag: the Head of Orientation, the Final Exam himself... **DEAN! THUUUUUDD!**"

### 6.3 Versus card

```text
╔══════════════════════ VERSUS ══════════════════════╗

   THE CLASS OF RIGHT NOW        vs.    DEAN THUDD
   [crawler names, Lv 2]                Level 2. BOSS.

   Record: 0–0                   Record: 1,100–0
   Hype: "visibly sweating"      Hype: "grades on a
                                  curve; the curve is
                                  his club"
   Odds: 11 to 1 (against)       Odds: 1 to 11
   Sponsor: none                 Sponsor: Orientation
                                  Pit Alumni Fund

             ★ FINAL EXAM: SURVIVE. ★
╚════════════════════════════════════════════════════╝
```

Post the Versus card, then roll initiative.

### 6.4 Stat blocks (4 crawlers, level 2)

| Creature | SRD 5.2 stat block | CR | # | XP |
|----------|--------------------|:--:|:--:|---:|
| **Dean Thudd** | **Ogre** | 2 | 1 | 450 |
| **Usher** | **Skeleton** | 1/4 | 2 at start + 2 in Phase 2 | 200 |
| | | | **Total** | **650 (High: Moderate 600 < 650 ≤ High 800)** |

Nameplates: `Dean Thudd. Level 2. Boss. "Has flunked 1,100 crawlers. Grades on a curve. The curve is his club."` / `Usher. Level 1. "Please silence your screams."`

**Reskin tweaks** (one each, per `02` §8.1; numbers otherwise as the stat block):

- **Dean Thudd: "GROUP PHOTO!"** (telegraphed area attack; **replaces the Ogre's ranged attack**, which Thudd never uses). *Action:* Thudd hoists the club overhead and bellows "**GROUP PHOTO! EVERYBODY SAY CHEESE!**" A glowing **10-foot-square spotlight** appears on the floor within his reach (he picks the spot that catches the most crawlers). He **counts down out loud**. At the **start of his next turn**, each creature still in the square makes a **Dexterity saving throw, DC 14** (8 + PB 2 + Str 4), taking damage equal to his melee (club) attack on a failure, or half on a success. Then he takes his turn normally. He can't use Group Photo on two consecutive turns. This trades a whole turn for an area hit one round later; anyone who steps out takes nothing (Tanya's note: "he COUNTS").
- **Ushers:** carry flashlights; their ranged attack is a flashlight with a "sharp beam" (shortbow numbers).

**What Thudd wants:** to hand out a diploma, then kill whoever accepts it.

**How to cheese it** (`02` §8.2: the show rewards cleverness):

1. **The orchestra pit.** The 2024 **Shove** (Unarmed Strike option) works on a target no more than one size larger, so Medium crawlers can shove Large Thudd (he saves against DC 8 + Str mod + PB). Pushed off the front edge, he falls 10 ft: 1d6 bludgeoning, **Prone**, and he spends his next turn climbing out (Athletics as written for climbing; he gets it automatically, it just costs the turn). If the fall kills him: `ACH-0173` Environmentalist (catalog Rare → **Bronze box**).
2. **Accept the diploma.** A crawler who walks up mid-fight and accepts a diploma with ceremony (**Charisma (Performance or Persuasion) DC 13**, Action) makes Thudd weep with pride: his next turn is spent crushing that crawler in a hug. They're **Grappled** (escape DC 14), take **no damage** from it, and he does nothing else that turn. Usable once per fight. The audience loses its mind: **Crowd Pop** (Heroic Inspiration, `02` §5.1) and `NEW: Most Dangerous Hug`.
3. **Talk him down.** Nobody's ever asked Thudd what *he* wants. If crawlers stop attacking him, they can try **three successes before three failures** at **Charisma (Persuasion or Deception) DC 15**, one check per round (one crawler leads; others can Help). Success: Thudd sits down in the front row, takes the fruit plate, and announces his early retirement. The Ushers keep fighting. `ACH-0189` Peaceful Path (catalog Rare → **Bronze box**). The Boss Box still drops; the System is livid about it.

### 6.5 Phases and tactics

**Phase 1 (full HP down to half):** Thudd wades in, prioritizing whoever hurt him most. Ushers hold the wings behind the trophy table and podium (half cover) and shoot. If two crawlers are within 10 ft of each other near him in round 2, he opens with Group Photo.

**Phase 2 (Thudd at half HP or below):** the walk-up song drops into a sad slowed-down pomp-and-circumstance remix. **Two more Ushers** enter from the aisles (they share the Ushers' initiative count). Thudd uses Group Photo every other turn when two targets are available.

> "TOUGH CROWD TONIGHT, FOLKS!" Thudd roars, and the audience laughs, because the laugh track tells it to.

**Black Box glimpse** (spine tease, `SEED-BLACKBOX`; **not a plant**, see §8.6). At the **start of Phase 2**, the camera drone over center stage takes a stray hit (whatever's plausible: a missed arrow, Thudd's backswing), sparks, and crashes. A **fist-sized, matte-black recorder housing** ejects and skids across the stage, stamped with a serial number and **PRODUCTION PROPERTY — DO NOT RECOVER**.

> For one second, every red camera light in the auditorium blinks off. The laugh track stops. The silence is enormous. Then the lights snap back on all at once, and the System's voice comes back very bright and very fast: "**AAAND WE'RE BACK!**"

At the **end of that round**, a ceiling claw drops and snatches the housing. A crawler within reach may grab it first (**Utilize** action; it's an object). If grabbed: AC 19, 30 HP, sealed; level-2 crawlers can't open it in any meaningful way; it **vanishes from their inventory at the Stairwell** with a notice: *"Production property recovered. Nothing was recorded. Nothing happened."* No achievement, no reward, no explanation. Log `SEED-BLACKBOX: glimpsed F1 (touched by: <crawler or none>)`.

### 6.6 Variant B (strict `02` §10.3 at level 1, or 2-crawler parties at level 2)

Use when the table declines the mid-floor milestone (fighting the boss at level 1), or when only 2 crawlers fight at level 2:

- **Dean Thudd (Junior Varsity)** = **Bugbear Warrior** (CR 1, 200 XP). Same costume and intro. Group Photo works the same with **DC 12** (8 + PB 2 + Str 2) and the Bugbear Warrior's melee damage.
- **Ushers:** 2 at start + 2 in Phase 2 (200 XP). **Total 400 XP** = High for four level-1 crawlers, or two level-2 crawlers.
- Nameplate: `Dean Thudd (JV). Level 1. Boss. "Same gown. Smaller man. Bigger chip on his shoulder."` (follows the CR rule; owner question §13).

### 6.7 Boss rewards

- **Silver Boss Box** for every crawler who fought Thudd (or talked him down). `02` §4.7 Boss Box, **capped to Silver** by the F1 ceiling (§2 rule 2). One pull is usually a **trophy**: one of Thudd's graduation cords reskinned as a Common or Uncommon item (e.g., a *Potion of Climbing* "Cord of Upward Mobility," or an Uncommon item if the d100 rolls Gear).
- **Name the box after the deed** (`02` §4.8). Examples:
  - **Silver Pushed the Dean Into the Orchestra Pit and Called It Extra Credit Box**
  - **Silver Accepted a Diploma and Got Hugged So Hard Your Spine Filed for Divorce Box**
  - **Silver Talked the Final Exam Into Early Retirement and He Took the Fruit Plate With Him Box**
  - **Silver Dodged the Group Photo and Ruined the Yearbook Box**
- `ACH-0170` Orientation Pit: Boss Claim → **fold into the Silver Boss Box** (don't add a separate Bronze unless the crawler is under the F1 box cap and the kill was spectacular).
- `ACH-0868` Dodge a Telegraphed AoE (R1).
- `ACH-0004` David vs Goliath does **not** fire (needs CR ≥ level + 5, or ≥ 2× level at tier 1, per `02` §3.9; Thudd is CR 2 vs. level 2).
- **Thudd's corpse cache:** 2d6 × 10 credits ("Alumni Fund"), the diploma stack (mundane; each reads *CONGRATULATIONS, [Intake Tag]* with a crawler's tag: the System printed them in advance), and the third placed *Potion of Healing* if the party missed one earlier.

**Opening the boxes:** backtrack one door to the Green Room and open them during a Short or Long Rest, or carry them to Floor 2's first saferoom (risk: die first and they're reclaimed, `02` §6.2). The System should *mention* the risk, sweetly.

---

## 7. Stairwell exit and Floor Summary (Zone 11)

### 7.1 The real stairwell (read-aloud)

> Behind the stage, past a fire door that wasn't there a minute ago, a plain concrete stairwell spirals down into the dark. No green sign. No birdsong. Just a hand-lettered index card taped to the rail: **FLOOR 2 →**. The air coming up smells like dust and ozone and somewhere you haven't been yet.
>
> Proctor Bell's booth rolls up one last time. Its painted face has cracked down the middle. "**YOU HAVE COMPLETED ORIENTATION,**" it says. "**I AM REQUIRED TO SAY THAT I AM PROUD OF YOU.**" Its jaw clacks. "**I AM ALSO REQUIRED TO SAY THAT MOST OF YOU WILL DIE ON FLOOR TWO.**" A long pause. "**...good luck, little lambs.**"

### 7.2 Bypassing the boss

Player agency first (`01-game-brief.md` hard limits). Crawlers who open the **service stairwell** (Zone S) can descend without fighting Thudd. They get no Boss Box and no Boss Claim, plus the System's full contempt: `NEW: Skipped Finals` (R0): *"You went around the final exam, through the janitor's door, like a raccoon. Four million viewers just watched you raccoon your way out of Orientation."* `ACH-0180` Stair Seeker still pays if earned. **Level 2 still applies** (it came at the Green Room).

### 7.3 Descent procedure

1. Each living crawler steps onto the Floor 2 landing → **Stairwell Checkpoint** (`02` §6.6): HP to full; regain Hit Point Dice as for a Long Rest (half total, minimum 1). **No** spell slots, no Long Rest features; conditions and Exhaustion unchanged (Soft Open's Exhaustion penalty clears). Once per crawler per transition.
2. **Floor 1 Reprieve** (if ON) expires for everyone.
3. Any **Black Box housing** vanishes (§6.5).
4. Unopened boxes stay in System Inventory for Floor 2's first saferoom.
5. **No level-up on descent** (level 2 came at the Green Room; §2 rule 3). Under Variant B / strict `02` §10.3, apply level 2 at Floor 2 Onboarding instead.
6. Award `ACH-0022` Tutorial Complete (**R1**: Title *Oriented*; `ACH-0076` Orientation Graduate is a retired duplicate, pay once, §10.3).
7. Post the **Floor Summary**.

> *Stairwell Checkpoint:* "Thank you for using the stairwell. Your hit points have been refilled by an unnamed contractor. He says you're welcome. Please stop making eye contact with him."

### 7.4 Floor Summary (template)

```text
╔══ FLOOR 1 SUMMARY: THE ORIENTATION PIT ════════════╗
  Graduates: [names]
  Casualties: [names, or "none, somehow"]
  Time on floor: [in-game]   Long Rests: [n]
  Kills: [n]   Rats: [n]   Signs actually read: [n]
  Most Damage Taken: [name] ("a natural sponge")
  Most Credits Fed to Proctor Bell: [name]
  Biggest Coward: [name] — Title: Strategic Advance in
    the Other Direction. Reward: ...lol no. Bitches
    don't get rewards.
  Audience Nickname of the Floor: "[nickname]" ([name])
  Foot Segment MVP: [name]. We don't make the rules.
  Production thanks you for your participation.
  Floor 2 is now loading. It is not a tutorial.
╚════════════════════════════════════════════════════╝
```

Summary awards are R0 (`02` §3.3 floor recap).

---

## 8. Loot plan, boxes, and spine-object plants

### 8.1 Welcome Box (Bronze, every crawler, Break Room)

- **1–2 pulls** (`02` §4.1). **One must be a tailored pull** (`02` §10.2; `03` §5.3).
- Recommended: **Pull 1 = tailored** (a Fan Profile fixation: cosmetic, or a reskinned Common consumable). **Pull 2 = d100** per `02` §4.2 at Bronze (credits row: 3d6 × 5).
- Name: **Bronze Welcome Box** (the one fixed name on the floor; every box after this is named after a deed).

### 8.2 Box budget per crawler (`02` §4.5, F1–2: Bronze 2–4, Silver 0–1)

| Source | Box | Notes |
|--------|-----|-------|
| Welcome Box | Bronze | Everyone, Zone 6 |
| Achievement boxes | Bronze × 0–2 | From catalog Rare seeds: Stair Bait Resisted, Stair Seeker, Sacrifice Play, Peaceful Path, Environmentalist. **Cap: 2 per crawler on F1** (keeps the total at 1–3 Bronze, inside 2–4 with a little slack for a deed-named surprise). |
| Boss Box | **Silver** | Everyone who fought or talked down Thudd |
| Floor clear | — | **None on F1.** The Boss Box is the floor-clear reward (keeps Silver at 0–1). |

Box openings: saferooms only, all at once, lowest tier first, not tradeable (`02` §4.4).

### 8.3 Placed consumables and credits

| Item | Where | Notes |
|------|-------|-------|
| *Potion of Healing* #1 | Tanya's body (Zone 3) | "Sports Drink, Red Flavor" |
| *Potion of Healing* #2 | Hidden cache (3b) | Behind the DC 15 secret |
| *Potion of Healing* #3 | Bruiser's head (Zone 8) | Moves to Thudd's cache if #2 was missed |
| Vendor stock | Snakk-Matic (Zones 6 + 9) | 2 *Potions of Healing*, 50 credits each, floor-wide |
| Common consumables | Vending (Zone 3) | ~1 per crawler at most |
| Credits | Fountain, vents, register, lockers, Greeters, Thudd, R1 toasts | Roughly 50–100 credits per crawler from the floor, plus box credits |

Three placed potions = `02` §10.3 "2–3 Potions of Healing across the party"; vendor stock is extra and costs credits. **Permanent magic items: 0–1 per crawler on F1** (`02` §3.7), from box Gear pulls or the Boss Box trophy only, Uncommon at most.

### 8.4 Spine-object plant checklist

| Seed | Where | Must happen? | Log |
|------|-------|:-:|-----|
| **Odd Coin** `SEED-ODDCOIN` | Lost & Found crate, Zone 3 (fallbacks: Green Room box "Weird" pull, Dale's pocket) | **Yes** | holder, zone |
| **Benefactor Signal** `SEED-BENEFACTOR` | First death save on F1 (likely Zone 8); fallback Green Room speaker | **Yes** | crawler who heard it |
| **Broadcast Name** | Audience-nickname plant (§8.5), whole floor | **Yes** (cosmetic) | `HANDLE-AUDIENCE` per crawler |
| **Black Box** `SEED-BLACKBOX` | Glimpse only, Zone 10 Phase 2 | Optional tease | "glimpsed," who touched it |

All four toast **without explanation** (`02` §3.2 item 6; Floor Bible F1: "Do not explain the Benefactor or coin").

### 8.5 Broadcast Name plant (audience nicknames)

The feature unlocks on F3 (`02` §5.1); on F1 the show just starts **calling crawlers things**.

- **Zone 0:** the hallway screen misspells one crawler's name ("ROZZ," "JAY (NOT THAT ONE)").
- **Every zone:** when a crawler does something memorable, the chyron appends a nickname: **[Name] "The Rat Stomper," [Name] "Sign-Ignorer," [Name] "Hugged the Dean."** The System keeps using the latest one in popups.
- By the Floor Summary, each crawler has **one audience nickname**, logged as `HANDLE-AUDIENCE`. On F3, the System offers the player their Requested Handle, the audience's version, or a mash-up (`03` §4).
- **No mechanics.** No Advantage, no Ratings effect beyond normal play.

### 8.6 Why the Black Box is only a glimpse

The spine plants the Black Box at **~F10** (`05`; `02` §5.5; Floor Bible F10 `SEED-HEATBLACKBOX`), and `02` treats it as evidence crawlers carry from there to F14/F17/F18. Handing over the real object on F1 would break that. So this module uses a **foreshadowing glimpse**: Production's recorder hardware exists, it's black, every camera blinks when it's exposed, and Production snatches it back instantly. On F10, when crawlers finally hold one, the System's silence should feel familiar.

---

## 9. Encounter math and party-size scaling

### 9.1 2024 DMG XP budgets (per crawler)

| Level | Low | Moderate | High |
|------:|----:|---------:|-----:|
| 1 | 50 | 75 | 100 |
| 2 | 100 | 150 | 200 |

XP by CR: 0 = 0–10; 1/8 = 25; 1/4 = 50; 1/2 = 100; 1 = 200; 2 = 450. (2024 rules: no group multiplier.)

### 9.2 Encounters for 4 crawlers

| Zone | Encounter | Level | XP | Budget (×4) | Difficulty |
|------|-----------|:-----:|---:|-------------|------------|
| 2 | 6 Vent Rats (Giant Rat) | 1 | 150 | Low 200 | Low |
| 5 | 4 Mannequin Staff (Skeleton) | 1 | 200 | Low 200 | Low (top of band; cover makes it bite) |
| 7 | 2 Goblin Warrior + 4 Goblin Minion | 1 | 200 | Low 200 | Low (+ pit = feels Moderate) |
| 8 | Animated Armor + 2 Animated Flying Sword | 1 | 300 | Moderate 300 | Moderate |
| W | 4 Ceiling Ticks (Stirge) | 1–2 | 100 | — | Low (resource drain) |
| 10 | Ogre + 4 Skeleton (2 + 2 in Phase 2) | 2 | 650 | Mod 600 / High 800 | **High** |

Matches `02` §10.3: 4–8 encounters, mostly Low/Moderate, one High; mobs CR 0–1/4, elite CR 1, boss CR 2.

### 9.3 Scaling by party size

| Crawlers | Zone 2 | Zone 5 | Zone 7 | Zone 8 (elite) | Zone 10 (boss, level 2) |
|:--:|------|------|------|------|------|
| **2** (+ Assigned Companion) | 3 rats (75) | 2 Skeletons (100) | 1 Warrior + 2 Minions (100) | Animated Armor alone (200; High for 2) | **Variant B**: Bugbear Warrior + 2 + 2 Skeletons (400 = High) |
| **3** | 4 rats (100) | 3 Skeletons (150) | 1 Warrior + 3 Minions (125) | Armor + 1 Sword (250) | Ogre + 1 + 1 Skeletons (550; High band 451–600) |
| **4** | 6 rats (150) | 4 Skeletons (200) | 2 Warriors + 4 Minions (200) | Armor + 2 Swords (300) | Ogre + 2 + 2 (650) |
| **5** | 7 rats (175) | 5 Skeletons (250) | 2 Warriors + 6 Minions (250) | Armor + 3 Swords (350) | Ogre + 3 + 3 Skeletons + 1 Tough ("Hall Monitor," CR 1/2) in Phase 2 (850; High band 751–1,000) |
| **6** | 8 rats (200) | 6 Skeletons (300) | 3 Warriors + 6 Minions (300) | Armor + 4 Swords (400) | Ogre + 3 + 3 + 2 Toughs ("Hall Monitors," CR 1/2) in Phase 2 (950) |

**2-crawler tables:** issue an **Assigned Companion** at intake (`02` §2.4; CR ≤ ½ party level): **Pudding**, a **Mastiff** (CR 1/8) in a tiny mortarboard who belongs to nobody and has opinions about everyone. DM-run, takes no loot, can die. (A rescued Dale is a second, worse companion.) **5–6 crawlers:** add bodies, not CR (`02` §2.4).

---

## 10. Achievement seeds (catalog + NEW)

`reference/achievements.csv` is **a seed list, not a schedule** (`02` §3.1). Floor 1 target: **6–10 toasts per crawler, at least 2 snark-only** (`02` §10.3), roughly 30–40% R0 overall (`02` §3.7). Toast at the end of the round in combat (`02` §3.3).

**Tier key:** R0 snark-only · R1 credits/Title · R2 Heroic Inspiration · R3 consumable · R5 box. Catalog "Rare loot roll" → **Bronze box on F1–2** (`02` Appendix A). Credits at ×1 on F1.

### 10.1 Recommended catalog seeds

| ID | Name | Where | Catalog | **F1 call** | Toast line |
|----|------|-------|---------|-------------|------------|
| ACH-0079 | Don't Skip Intro | Zone 1 | Common, no reward | **R0** | "You listened to the whole tutorial. Like a nerd. A live nerd, for now." |
| ACH-0001 | First Blood | Zone 2 | Title + junk oil | **R1** (Title *Blooded* + flask of oil) | "First kill! It was a rat. Your parents would be so... it was a rat." |
| ACH-0894 | Land a Critical Hit | any | no reward | **R0** | "Natural 20. Don't let it go to your head. Your head has enough going on." |
| ACH-0205 | Scenic Panic | any fight | Humor, no reward | **R0** | "You typed 'WE'RE GONNA DIE' in all caps and then won. We heard you scream. In text." |
| ACH-0083 | Corpse Lesson | Zone 3 | no reward | **R0** | "You went through a dead woman's pockets before learning her name. Efficient. Ghoulish. On-brand." |
| ACH-0077 | Vending Gore | Zone 3 | Title + 25 | **R1** | "You robbed a machine that bites. The machine respects you. Nobody else does." |
| ACH-0081 | Odd Coin Pocketed | Zone 3 | Seed flagged | **Hidden, no reward** | "*Oddity logged.*" (nothing more, ever) |
| ACH-0177 | Hidden Cache | Zone 3b | Title + 25 | **R1** | "You looked behind the machine. Nobody looks behind the machine." |
| ACH-0871 | Find a Lore Scrap | Zone 3 / 7 | Rare | **R1** | "You found a dead woman's diary. Reading it is free. Living with it costs extra." |
| ACH-0872 | Read a Lore Scrap Aloud | Zone 3 | Legendary (outlier) | **R2** if heartfelt / **R0** if mocking | "You read a dead woman's last words to a room full of cameras. Beautiful. Or content. It's content." |
| ACH-0869 | Rescue a Civilian NPC | Zone 4 | Rare | **R1** (25 + Title *Lifeguard*) | "You saved Dale. Dale will now talk to you about ductwork. Forever. You did this." |
| ACH-0870 | Fail to Rescue a Civilian | Zone 4 / 7 | Common + 25 | **R0** (downgraded) | "Dale's dead. The audience is sad. Sad audiences buy merch. So... thanks?" |
| ACH-0198 | Poison Tolerant | Zone 4 | Title + 25 | **R1** | "You got stuck by a dirty needle and lived. Very public-restroom of you." |
| ACH-0877 | Disarm a Trap with Junk | Zone 4 | Title + 25 | **R1** | "You beat a trap with chewing gum. MacGyver's crying. So is the trap." |
| ACH-0867 | Block a Hit with a Shield | Zone 5+ | Title + 25 | **R1** | "You held up a stop sign and it worked. Traffic law remains undefeated." |
| ACH-0025 | Saferoom Skeptic | Zone 6 / 9 | Rare, trap kit | **R1** (tool refill) | "You searched a certified saferoom for traps. Clean. You're paranoid. Stay that way." |
| ACH-0899 | Share Food with the Party | Zone 6 | Rare | **R1** | "You split a sandwich. With feelings. Gross. Wholesome. Gross." |
| ACH-0188 | Rumor Mill | Zone 6 | Title + 25 | **R1** | "You read a corkboard. Three times. Somebody get this crawler a library card." |
| ACH-0084 | Stair Bait Resisted | Zone 7 | Rare | **Bronze box** | "You smelled freedom and said 'nah.' Bronze Didn't Fall for the Birdsong Box." |
| ACH-0085 | First Down | Zone 8 (likely) | no reward | **R0** | "You hit the floor. The floor hit back. Floor: 1. You: also on the floor." |
| ACH-0015 | Down But Not Out | Zone 8 | Title + 25 | **R1** | "Stabilized! You're alive, technically, which is our favorite kind of alive." |
| ACH-0018 | Buddy System | Zone 8 | Title + 25 | **R1** | "You saved a teammate. They owe you. Collect before they die." |
| ACH-0020 | Sacrifice Play | any | Rare | **Bronze box** | "You took the hit for someone else. Heroic. Stupid. The good kind of stupid." |
| ACH-0078 | Tutorial Elite | Zone 8 | Title + 25 | **R1** (Title *Mascot Hunter*) | "You beat up an empty costume. Nobody was inside. Think about that. Then don't." |
| ACH-0082 | Static in the Ear | Zone 8 | Seed flagged | **Hidden, no reward** | "*Signal logged.*" (denied if asked) |
| ACH-0180 | Stair Seeker | Zone S | Rare | **Bronze box** | "You found the back stairs before the boss. Smart. Cowardly. Smart." |
| ACH-0868 | Dodge a Telegraphed AoE | Zone 10 | Title + 25 | **R1** | "He counted to three. You can count to three. Congratulations on counting to three." |
| ACH-0189 | Peaceful Path | Zone 10 | Rare | **Bronze box** | "You talked the Dean into retirement. HR is furious. We are HR." |
| ACH-0173 | Environmentalist | Zone 10 (pit) | Rare | **Bronze box** | "You killed him with an orchestra pit. The orchestra has filed a complaint." |
| ACH-0170 | Boss Claim | Zone 10 | Rare | **Folded into Silver Boss Box** | — |
| ACH-0022 | Tutorial Complete (toast: "Orientation Graduate") | Stairwell | Title *Oriented* | **R1** (Title) | "You graduated. Your diploma is in the mail. The mail is on fire." |
| ACH-0197 | Bleed Tax | after 3 healing items | no reward | **R0** | "Three healing items on the tutorial floor. You're not a crawler, you're a sponge with a debit card." |
| ACH-0866 | Deal Psychic Damage | any | no reward | **R0** | "You hurt its feelings. Literally. We're so proud. Of the feelings." |
| ACH-0873 | Destroy a Camera or Drone | Zone 10 drone | no reward | **R0** | "You broke a camera. We have eleven thousand more. That one was Kevin's favorite, though." |
| ACH-0204 | Floor Bit | when a running joke sticks | no reward | **R0** | (name the bit; refuse to pay for it) |

### 10.2 NEW (System-invented; log as `NEW:`)

| Name | Trigger | Tier | Toast |
|------|---------|------|-------|
| Paperwork Survivor | Complete intake | R0 | (see `03` §9) |
| Coin Slot | Pay Proctor Bell before it finishes its intro | R0 | "You paid the robot to stop talking. Relatable. Didn't work." |
| Fed the Machine | Bitten by a Hungry Vendor | R0 | "You put your hand in a hole with teeth. Your mother would be proud. Of the machine." |
| Literacy Optional | Trigger a trap the signs warned about | R0 | "Three signs. You read zero. Who raised you? Don't answer. We'll find her." |
| Hit the Cutout | Attack a plywood crawler in Zone 5 | R0 | "That one was plywood. To be fair, it looked smarter than you." |
| First Box | Open the Welcome Box | R0 | "Your pupils went full slot machine. It's going in the promo." |
| Lunch Thief | Eat Dale's sandwich in front of Dale | R0 | "Dale saw. Dale will always have seen." |
| Freedom Smelled Like a Fan | Go down the Big Green EXIT | R0 | "You heard birds and ran at them like a horny golden retriever. The pit has your name on it now. We engraved it." |
| Biology Anomaly (Logged) | First visible use of a latent species trait | R0 | "You can see in the dark. We noticed. We notice *everything*." |
| Most Dangerous Hug | Accept Thudd's diploma mid-fight | R2 (Crowd Pop) | "You let an ogre hug you for ratings. Your spine and the audience both screamed." |
| Skipped Finals | Bypass Thudd via the service stair | R0 | "You raccooned your way out of Orientation." |
| Strategic Advance in the Other Direction | Flee a fight without taking damage | R0 | "REWARD! ... lol no. Bitches don't get rewards." |
| Assault on Faculty | Attack Proctor Bell | R0 | "You punched the teacher. The teacher is glass. The glass is fine. Your hand isn't." |
| Toe Talent | Fight barefoot, kick something to death, or otherwise make it about feet | R0 (R1 if the audience demands it) | "Our foot demographic would like to thank you personally. Please don't let them." |
| Again? Production Has Seen This Episode | Repeat a farmed stunt (e.g., vending after the cap) | R0 | "Reruns don't pay. Ask any actor." |

### 10.3 Catalog conflicts handled here

- **ACH-0022 "Tutorial Complete" and ACH-0076 "Orientation Graduate"** both pay Title *Oriented* for clearing F1. **Pay ACH-0022 only**; ACH-0076 is retired in the catalog (`reference/achievements.csv`/`.xlsx` Notes = "DUPLICATE of ACH-0022, retired"; IDs stay stable). Keep the "Orientation Graduate" toast flavor if you like (`02` §3.8 duplicates).
- **Generated-variant rarity outliers** on F1 (ACH-0858 Pick a Lock = Legendary; ACH-0865 Deal Poison Damage = Legendary; ACH-0893 Use a Two-Handed Weapon = Legendary; ACH-0879 Lose a Betting Game = Legendary; ACH-0886 Fall and Survive = Legendary; ACH-0872 Read a Lore Scrap Aloud = Legendary): **step down to R0–R2**, logged as "catalog rarity outlier" (`02` §3.4 allows two tiers with a reason).
- **ACH-0190 "Obtain a Rare or better item"** can't happen on F1 under the Uncommon ceiling (no Benefactor Boxes on F1). Don't seed it. The catalog row now carries Notes = "Not obtainable on Floor 1 (Uncommon cap)".
- **ACH-0004 David vs Goliath** can't fire on Thudd (§6.7).
- **ACH-0013 / ACH-0191 "Named item"** → translate per `02` §3.9 (Uncommon+ magic item with a name); rare on F1.

---

## 11. DM notes

### 11.1 Comfort (`COMFORT=Ludicrous`) and the private opt-out

- The System is **crude, profane, and merciless about cowardice and failure**, at full canon strength. "Your mom" jokes, bodily humor, sexual crudity, and the foot bit are all on. Sexual crudity is **jokes, not scenes**.
- **Private opt-out:** any crawler can tell the GM privately (code word "cut," or a side message) that a joke or topic isn't working. The System **drops it for that crawler immediately**, logs it privately (`COMFORT-OPTOUT`), never references it, never makes it a bit or an achievement, and quietly retires any running gag or Fan Profile item that touches it. Everyone else stays at Ludicrous.
- Roast the **deed**, not the player's real self (`03` §2.3 hard floors).
- Tanya's note and Dale's death (if it happens) can land as **actually sad** for one beat. Give the moment room *before* the System gets uncomfortable with sincerity and ruins it.

### 11.2 Failure modes and fixes

| Problem | Fix |
|---------|-----|
| Nobody has hit 0 HP by Zone 8 | Bruiser focuses one crawler; the Lanyard Blades harass the healer. **No fudging** (`02` §2.5.6); tactics only. The tutorial *wants* to show a death save; it never forces one. |
| Party is getting wrecked early | Proctor hints are cheap (1 credit); point them at the Break Room; the early fights are Low as written. Never fudge dice. |
| Party skips the Odd Coin | Fallbacks in §5.3 / §8.4. |
| Nobody makes a death save all floor | Benefactor Signal fires at the end of round 2 in Zone 8 (or the Green Room fallback). |
| Party tries a Long Rest in the field | Allowed; Ceiling Ticks interrupt (§2 rule 7). |
| Party farms vending machines | SOLD OUT FOREVER after the cap; `NEW: Again? Production Has Seen This Episode` (R0). |
| Party attacks Proctor Bell | It self-heals; `NEW: Assault on Faculty` (R0); no more hints for that crawler this floor. |
| Player hunts CSV rows | Snark (`02` §3.8). |
| Dale becomes a beloved mascot | Great. Keep him alive if the dice allow. Possible recurring NPC (owner question §13). |
| Player goes quiet after a joke | One private check-in: "Still good? Say 'cut' and that bit's gone." Don't make a scene of it. |

### 11.3 Pacing (chat play)

- **Session 1:** Death Mode + intake (Zone 0) → Zones 1–3.
- **Session 2:** Zones 4–6 (Welcome Box ceremony) → maybe Zone 7.
- **Session 3:** Zones 8–11 (level 2 at the Green Room, boss, stairwell).
- New-to-5e tables: add a session. Experienced tables: two sessions.

### 11.4 Session-state additions (Floor 1)

```text
FLOOR: 1 (Orientation Pit)   ZONE: <n>   MAP: <zones revealed>
DEATH-MODE: <...>   F1-REPRIEVE: <ON/OFF; used by: ...>
COMFORT: Ludicrous   COMFORT-OPTOUT: (private, per crawler)
LEVEL: <1/2>   MIDTERM ONBOARDING: <done/pending>   BOSS VARIANT: <A/B>
NPC: Dale Pruitt <alive/dead/companion>   Tanya Ruiz: <looted y/n>
SEED-ODDCOIN: <holder, zone>   SEED-BENEFACTOR: <crawler, zone>
SEED-BLACKBOX: <glimpsed F1; touched by: ...>
HANDLE-AUDIENCE | <crawler> | <nickname>
WANDERING: Ceiling Ticks used <0/1/2>   VENDOR POTIONS LEFT: <0–2>
ACH | <crawler> | <ID or NEW:name> | <tier> | <reward> | F1/S<n>
BOXES | <crawler> | <tier + deed name> | <unopened/opened>
```

---

## 12. Changelog

| Version | Date | Notes |
|---------|------|-------|
| stub | 2026-10-02 | `floors/floor-01.md`: objective + seed list only. **Superseded.** |
| **v0.2** | 2026-10-03 | Full 5e 2024 module on `02` v0.2.2: Death Mode step; 12 zones + side path + wandering; SRD 5.2 reskins with 2024 XP math; 4 traps; two saferooms; Welcome and Silver Boss boxes; catalog + NEW achievement seeds; spine plants (Odd Coin, Benefactor Signal, Broadcast Name nickname plant, Black Box glimpse); Dean Thudd boss with Versus card, telegraphed Group Photo, three cheese routes, Variant B; stairwell + Checkpoint; scaling 2–6; `COMFORT=Ludicrous` with private opt-out. |
| **v0.2.1** | 2026-10-03 | Consistency pass with `02` v0.2.4: rules base bumped; campaign-default Death Mode note (Costly Revives already picked); F1 achievement payout now `ACH-0022` (0076 retired duplicate); ACH-0190 note; open questions 1, 2, 14, 16 marked resolved. |

---

## 13. Open for owner markup

1. **Mid-floor milestone:** level 2 lands at the Green Room (before the boss) because a CR 2 boss vs. four level-1 crawlers is beyond High (450 vs. 400). That departed from `02` §10.2–10.3 ("level 2 on Floor 2 Onboarding"). **Resolved in `02` v0.2.4:** the split is kept and `02` §2.3/§10.2–10.3 amended; strict mode with Boss Variant B remains a table option.
2. **Boss Box tier:** capped at **Silver** on F1 vs. `02` §4.7 "floor boss → Gold or Platinum." **Resolved in `02` v0.2.4:** §4.7 now says floors 1-2 boss boxes are capped by §3.6 (F1 = Silver).
3. **Black Box:** OK as a **glimpse** Production snatches back, or keep it completely off-screen until F10?
4. **Benefactor Signal trigger:** "first death save on the floor" makes it personal to one crawler. Keep, or have every crawler hear it?
5. **Dale Pruitt:** recurring NPC if he survives (F2 cameo, F3 refugee), or Floor 1 only?
6. **Proctor Bell hints** at 1 credit: fine, or free (snark instead of a price)?
7. **Lights-Out cycle** instead of a floor clock: keep, cut, or replace with a generous real clock, as `04-floor-bible.md` F1 implies ("timer is generous")?
8. **Boss cheese routes:** "talk him down" (3 × DC 15) and "accept the diploma" (DC 13, one hug): too easy, too hard, or right for a tutorial?
9. **Variant B nameplate:** written as Level 1 per the CR rule. Want the System to lie (Level 2) for comedy?
10. **Box cap:** Welcome + up to 2 achievement Bronze + Silver Boss per crawler. Right, or tighter?
11. **Assigned Companion** for 2-crawler tables: Pudding the Mastiff OK?
12. **Foot bit dosage:** max once per session on F1. More, less, or escalate floor by floor?
13. **Floor Bible alignment:** `04-floor-bible.md` F1 still says "No race/class selection yet; everyone is Baseline Crawler" (pre-5e) and has its own achievement ideas (Read the Manual, Witness Protocol, Coin Collector). Update the Bible row to point here?
14. **Catalog fixes:** the ACH-0022/0076 duplicate is **done** (0076 retired; v0.2.4). Still open: re-rarity the generated-variant outliers (§10.3)?
15. **Seed ID:** `02` says `SEED-BLACKBOX`; the Floor Bible says `SEED-HEATBLACKBOX`. Which one?
16. **Death Mode recommendation:** **decided**, Costly Revives (very costly and rare) is the campaign default (`02` v0.2.3/§6.0). Still open: Floor 1 Reprieve ON or OFF?

---

*SRD attribution: this module references SRD 5.2 stat blocks by name (Giant Rat, Skeleton, Goblin Warrior, Goblin Minion, Animated Armor, Animated Flying Sword, Stirge, Ogre, Bugbear Warrior, Tough, Mastiff, Commoner). See `02-core-rules-5e.md` Appendix D. No book text is reproduced.*
