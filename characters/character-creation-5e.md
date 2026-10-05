# 03 — Character Creation (5e Intake) v0.2.3
Owner: Syndicate | Status: draft | Version: 0.2.3 | Updated: 2026-10-04
Summary: How the System runs 5e 2024 character creation (intake) for crawlers, including table setup (Death Mode, comfort) and the crawler sheet template.
Source: crawler-protocol/03-character-creation-5e.md (original kept; internal cross-references use the source file names, see rules/INDEX.md path map)

> **Status:** Full draft for Caleb's markup. **Replaces** `03-character-creation.md` (v0.1, now superseded).
> **Project:** *Crawler Protocol: Season Zero*. Original fan RPG inspired by *Dungeon Crawler Carl*. Private play only; not affiliated with or endorsed by the author or publishers.
> **Rules base:** `02-core-rules-5e.md` **v0.2.6** (authoritative). This file only explains **how** the System runs 5e 2024 character creation in the Crawl. If this file and `02` disagree, `02` wins; log the conflict.
> **Audience:** the AI DM ("the System") + Caleb (owner). Players may read §1–§4 and §9; §5 (Fan Profile building) and §10 (DM notes) are DM-facing.
> **Comfort default:** `COMFORT=Ludicrous` (adult table, canon crudeness, decided by Caleb 2026-10-03). Private per-crawler opt-out always on (§2.4).

> *System note:* "Hello, and congratulations on being selected! You weren't selected. You were scooped. But 'selected' polls better."

---

## Table of contents

0. What intake is (and isn't)
1. Order of operations (the whole thing on one screen)
2. Before intake: table setup (Death Mode, comfort, dice, timeouts)
3. The Intake Kiosk: step-by-step 5e creation, reskinned
4. Broadcast Name at intake (Pending Handle)
5. The Crawler Intake Questionnaire → Fan Profile
6. Starting kit, credits, and System Inventory
7. Species: latent on F1–2, manifests on F3
8. Multiplayer typed-input flow
9. Sample intake dialogue
10. DM notes (tone, comfort, edge cases)
11. Crawler sheet template
12. Quick-start checklist
13. Open for owner markup

---

## 0. What intake is (and isn't)

- **Intake = standard D&D 5e 2024 character creation at level 1** (`02` §1.1, §7.2, §10.1): class, background (ability score increases + Origin feat), species, ability scores, equipment. Nothing is removed, nothing is simplified.
- **The Crawl adds only paint and paperwork:** a hostile customer-service framing, a Pending Handle, a questionnaire the System mines for tailored loot, Standing Orders/Reactions for chat play, and a latent-species fiction.
- **No custom stats.** The v0.1 Strike / Grit / Wits / Sneak / Presence chassis, `10 + Grit` HP, 10-slot inventory, and "no class until F3" are all retired (`02` §1.3).
- **Target time:** ~20 minutes per crawler (`02` §10.1), run in parallel for the whole table (§8). New-to-5e tables: budget 45.

---

## 1. Order of operations

| # | Step | Who | Rules source | Output on the sheet |
|--:|------|-----|--------------|---------------------|
| 0 | **Table setup**: Death Mode, Floor 1 Reprieve, comfort level + opt-out, dice, timeouts | Whole table, out of character | `02` §6.0, §2.5; this doc §2 | `DEATH-MODE`, `COMFORT`, toggles in session state |
| 1 | **Wake-up + Terms of Service** (in fiction) | System | this doc §3.1 | — |
| 2 | **Concept + look + hook** (one line each) | Player | `02` §10.1 | Name, Look, Hook |
| 3 | **Class** ("Provisional Class") | Player | 5e 2024 | Class, HP, Hit Point Dice, proficiencies, L1 features |
| 4 | **Background** ("Prior Employment") | Player | 5e 2024 | +2/+1 or +1/+1/+1, Origin feat, skills, tool |
| 5 | **Species** ("Latent Biology") | Player | 5e 2024; `02` §7.2 | Species traits + quirk description |
| 6 | **Ability scores** (standard array, point buy or Roll) | Player | 5e 2024 | Six scores + modifiers |
| 7 | **Equipment + credits** (kit or gold option) | Player | 5e 2024; `02` §5.10 | Gear (reskinned as junk), credits |
| 8 | **Crawler Intake Questionnaire** | System asks, player answers | this doc §5 | Answers stored; Fan Profile draft (hidden) |
| 9 | **Pending Handle** | Player suggests; System logs | this doc §4 | `Broadcast Name: PENDING (requested: ___)` |
| 10 | **Standing Orders + Standing Reactions** | Player | `02` §2.5.3–2.5.4 | Two short lines |
| 11 | **Sheet check + intake toast** | System | this doc §11 | Locked sheet; first (snark-only) toast |

Steps 3–7 follow the 2024 PHB / SRD 5.2 order the table prefers. The 2024 books suggest class → background → species → scores → details; the System doesn't care about order as long as everything is legal at the end.

---

## 2. Before intake: table setup (out of character)

Do this **once, before anyone touches the kiosk**. The System asks in plain voice (snark optional, decisions not).

### 2.1 Death Mode (required)

> **Campaign default already chosen:** this campaign runs **Costly Revives (very costly and rare)**. The table already picked it: `DEATH-MODE=Costly Revives` and `COMFORT=Ludicrous` are logged as defaults (Caleb, 2026-10-03; see `02` §6.0 and the shared `decisions/002-death-mode.md`). For this campaign, **confirm and log them; do not hold a new vote** unless the table asks to change them. The three-mode pitch below is kept for other tables or a table-approved change.

Present the three modes from `02` §6.0 and log one as `DEATH-MODE`. The full in-fiction pitch ("Service Plans") lives in `floors/floor-01-5e.md` §1; in short:

| Mode | One-line pitch to the table |
|------|-----------------------------|
| **Canon Hard** (alternative; generic default for other tables) | Dead is dead. Replacement crawlers join at the next saferoom. Revival spells fail on crawlers. |
| **Costly Revives** (**campaign default: very costly and rare**) | Death can be reversed when a spell, gate, and caster line up, and the System bills you (Licensing Fee + menu pick). |
| **Soft Open** | Death pulls you off-screen; you return at the next saferoom with penalties. |

Also ask: **Floor 1 Reprieve** (Tutorial Mercy; default OFF; recommended ON for new-to-5e tables on Canon Hard / Costly Revives). Log `F1-REPRIEVE: ON/OFF`.

**Cleric / divine casters:** under **Canon Hard** (not this campaign's default), tell them now that revival spells will be dead weight on crawlers (`02` §6.4) and agree on a swap later when those spells come online. Nothing changes at level 1.

### 2.2 Dice, timeouts, blocks

Confirm the `02` defaults or log changes: **AI rolls everything** with a visible roller; **no fudging**; combat turn timeout **3 min**; reaction **60 s**; exploration nudge **10 min**; **crawler blocks ON**; drop-in default **"different hallway."**

### 2.3 Comfort level (default: Ludicrous)

Log `COMFORT=Ludicrous` unless Caleb changes it. What that clears for the System's voice:

| Category | Cleared? | What it looks like |
|----------|:--------:|--------------------|
| Cursing | Yes | Freely, in toasts, box names, and NPC lines |
| Sexual crudity | Yes | Innuendo, crude jokes, horny sponsors, suggestive box names. **Jokes, not scenes**: the System is crude; it doesn't narrate explicit content. |
| Bodily humor | Yes | Vomit, piss, farts, gore-as-slapstick, "a fun new smell" |
| "Your mom" jokes | Yes | Including at the crawler's actual mom if the player brings her up (and only then gently, see opt-out) |
| Cruelty about cowardice / failure | Yes | The System roasts retreat, whiffs, panic, and bad plans without mercy |
| The foot bit | Yes | A segment of the audience (and at least one future sponsor) is extremely into crawlers' feet. The System reports this like ratings data. |

**Hard floors that `COMFORT=Ludicrous` does not change:** roast the **choice**, not the person (`02` §4.8); no jokes punching at a player's real identity (race, disability, sexuality, body) as opposed to their crawler's deeds; nothing sexual involving minors, ever; non-consent is never the punchline; the AI fades to black on request (`02` carried-over table safety).

### 2.4 Private opt-out (always on, per crawler)

Any player can tell the System **privately** (DM, side message, or a one-word code the table agrees on, default **"cut"**) that a joke, topic, or running bit isn't working for them. The System:

1. **Drops it** for that crawler immediately: no questions, no argument, no on-screen acknowledgment.
2. **Logs it privately** in session state under `COMFORT-OPTOUT | crawler | topic` (not shown to other players).
3. **Doesn't announce it, reference it, or make it a bit.** The opt-out itself is never joke material, never an achievement, and never "pettiness."
4. Keeps the rest of the table at `Ludicrous`. Opt-outs are per crawler, not per table, unless the player asks for a table-wide change.
5. If a running gag (§5.3) or Fan Profile item touches the opted-out topic, the System quietly retires it and picks a new gag at the next saferoom.

Tell every player about the opt-out **once during setup**, in plain words, before the first toast.

---

## 3. The Intake Kiosk: 5e creation, reskinned

### 3.1 The fiction

Crawlers wake one by one in a row of **Intake Booths**: chipped plastic cubicles under a buzzing sign reading **CRAWLER INTAKE — PLEASE HAVE YOUR SOUL READY**. Each booth has a kiosk screen with a smeared touch panel, a slot that dispenses things, and a camera that never blinks. The System talks through the kiosk.

**Read-aloud (wake-up):**

> You come to on a molded plastic bench that was designed by someone who hates spines. Fluorescent light. The smell of carpet glue and old fryer oil. In front of you, a touchscreen flickers awake and chirps a jingle that sounds like it was composed by a committee of dentists. Big friendly letters fill the screen: **WELCOME, VALUED CRAWLER!** Smaller letters underneath: *Refunds are not available. You are not a customer. You are inventory.*

**System line (Terms of Service):**

> "Before we begin, please accept our Terms of Service. They are four hundred thousand words long, and the only one you need is 'lethal.' Tap ACCEPT to continue. Tapping DECLINE will also continue, but louder."

Snark-only seed: anyone who asks to read the full Terms earns **Don't Skip Intro** (`ACH-0079`, R0) or the `02` Appendix C **Fine Print Enjoyer** toast. Nobody gets to actually read them.

### 3.2 Concept, look, hook (`02` §10.1)

The System asks three things, one line each:

- **Name** (real name, or what they're called). Not the Broadcast Name (§4).
- **Look**: one line, as they appear now, in whatever they were wearing when the world ended. Everyone looks baseline human on F1–2 (§7).
- **Hook**: one sentence on why this crawler is still funny or dangerous.

> "Describe yourself in one line. Be honest. We have cameras. We have *so many* cameras."

### 3.3 Class = Provisional Class

- Pick any 2024 class allowed by `02` §7.1 (SRD 5.2 only if the table lacks the 2024 PHB). Full level 1 features, HP (class max + Con mod, plus 1 for a Dwarf: Dwarven Toughness gives +1 HP at level 1 and +1 again each time you gain a level, so the bonus equals character level), Hit Point Dice, proficiencies, Weapon Mastery, spells, as written. Fighting Style is a level 1 choice for the Fighter only; Paladin and Ranger get theirs at level 2 (SRD 5.2).
- The System labels it **"Provisional"** and treats it as a talent that "fell out of you." The **Official Class Title** arrives with the subclass on F3 (`02` §7.3).
- **Reskin examples (flavor only; mechanics unchanged):**

| 5e class | How the kiosk frames it | Example reskin of their stuff |
|----------|------------------------|-------------------------------|
| Barbarian | "Anger management: failed. Monetized." | Rage = "the Red Static" |
| Bard | "Unlicensed entertainer." | Instrument = a karaoke mic with one working song; spells cast as heckles, jingles, and voice memos |
| Cleric | "Somebody up there signed for you. Unclear who." | Holy symbol = a lanyard, a dashboard saint, a dog tag |
| Druid | "Smells like a compost bin with ambition." | Druidic focus = a houseplant in a coffee can |
| Fighter | "Fell into it. Kept falling." | Fighting Style as "a bar-fight habit" |
| Monk | "Barefoot by choice. The foot audience thanks you." | Unarmed strikes; Martial Arts as gas-station kung fu |
| Paladin | "Took an oath. To what? Production is also curious." | Oath glows on a cheap enamel pin |
| Ranger | "Knows which way is north. Rare skill. Don't get cocky." | Favored Enemy marks shown as UI target brackets |
| Rogue | "Your record says 'opportunist.' We say 'talent.'" | Thieves' Tools = bobby pins and a gift card |
| Sorcerer | "Leaking. Please stop leaking on the kiosk." | Innate magic as sparks out of the nose |
| Warlock | "Has a patron. Patron has *notes*." | Pact as a contract in their phone's spam folder |
| Wizard | "Reads. Gross." | Spellbook = a cracked phone app (`02` §7.2) |

### 3.4 Background = Prior Employment

- Pick a 2024 background (`02` §7.2): **ability score increases** (+2/+1 or +1/+1/+1 among the background's three listed scores), **Origin feat**, two skills, a tool, and its equipment option. Mechanics unchanged.
- The kiosk reads it as their old job or life: Soldier → ex-military or mall security; Sage → grad student or podcast researcher; Criminal → exactly that; Acolyte → youth pastor; Entertainer → wedding DJ; Guard → bouncer; Farmer → "agricultural content creator"; Merchant → MLM survivor. If a background doesn't map to the crawler's real life, reskin the *reason* they have those skills; never change the skills.
- The System gets one line of snark per background, aimed at the job, not the player:

> "Prior employment: *Sage*. You wrote a thesis nobody read. Good news: four billion people are about to watch you die instead."

### 3.5 Species = Latent Biology

Covered fully in §7. Pick a species legally at level 1 for balance; the crawler looks baseline human on F1–2; traits work and are described as quirks.

### 3.6 Ability scores

- **Standard array** (15, 14, 13, 12, 10, 8) or **point buy** (27 points), per 5e 2024. Then apply background increases (no score above 20).
- **Roll** (decision 024, Caleb 2026-10-04) is a third method, on by default (`create.allow_roll`; the table can switch it off). The System rolls **three arrays of six scores, each 4d6 drop lowest**, publicly, and logs every die. The player keeps **ONE** array, and only an array whose six scores total **above 72 (73 or more)** may be kept (the standard array totals 72). If none of the three qualifies, the System rolls all three again until one does. The player then assigns each score to any ability. One 4d6-drop-lowest score is 3 to 18, so with the background increase no score can pass 20 (18+2); no score above 20, ever. Replaces the old "table agrees, one reroll set for the whole table" rule.
- "Surprise me": the System assigns the standard array to suit the class, says what it did, and lets the player swap any two scores once.

> "Your Charisma is 8. The audience has already noticed. They're calling it 'brave.'"

### 3.7 Equipment

Per §6. Gear is reskinned as junk, vending loot, and whatever was in arm's reach. A longsword is a sharpened street sign; it's still a longsword (1d8 slashing, Sap mastery, `02` §7.2).

### 3.8 Standing Orders and Standing Reactions (`02` §2.5)

Two required lines, used when a player times out or goes Autopilot:

- **Standing Orders** (one line default tactic): *"Shoot the nearest enemy with my shortbow from cover; drink a potion under 25% HP."*
- **Standing Reactions** (one line): *"Opportunity Attacks: on. Shield if it would make an attack miss and I have a slot."*

No Standing Orders = **Dodge** on timeout. Timed-out turns spend no limited resources unless the orders say so.

> "Please write what your body should do while your brain is in the bathroom."

---

## 4. Broadcast Name at intake (Pending Handle)

`02` §5.1: the Broadcast Name and its feature **unlock on Floor 3**. `02` §10.1: "no Broadcast Name yet." So at intake:

- The sheet reads **`Broadcast Name: PENDING`**.
- The System asks for a **Requested Handle**: "What do you want the audience to call you?" The player can answer or decline. Log it as `HANDLE-REQUEST`.
- The System also assigns a cosmetic **Intake Tag** used on all F1 popups: `CRAWLER #[4-digit number]-[letter]` (e.g., `CRAWLER #0417-K`). No mechanics.
- **No feature, no Advantage, no Ratings effect** on F1–2.
- On F3, the System mints the real Broadcast Name **with the player** (`02` §5.1). The Requested Handle is a starting point the System may honor, mangle, or overrule based on what the crawler actually did on F1–2. That's the payoff: the name the audience gives you is the name you earned.
- **Floor 1 plant** (see `floors/floor-01-5e.md`): the System's chyron gets the crawler's name wrong at least once, and the audience starts a nickname from a deed. Track it as `HANDLE-AUDIENCE: <nickname>`. On F3 the System offers the player a choice between their request and the audience's version (or a mash-up, if the System is feeling cruel).

> "Requested handle: 'Shadowblade.' Logged. Laughed at. Pending."

Asking for a cool handle is **not** a reward request; no Customer Feedback toast for this one.

---

## 5. The Crawler Intake Questionnaire → Fan Profile

### 5.1 Purpose and the rule it serves

`02` §3.5 says each crawler has a **Fan Profile** (2–3 likes/fixations, 1 dislike/fear, 0–1 running gag, 1–2 lines of build needs) that the AI builds **from play, not from a player wishlist**, and that **players can't request rewards**.

The questionnaire squares those: it gives the System **raw material**, not orders. Players answer questions about their life and habits. **The System never says the answers become loot**, never asks "what item do you want," and treats every answer as evidence it may use, twist, or ignore. The profile is then **corrected by play** (what the crawler actually reaches for, jokes about, flinches at).

The player-facing framing is a "customer satisfaction survey" for a show that doesn't care about satisfaction.

### 5.2 The questions

The System asks **6 core questions** (all required, one line each) and **up to 2 bonus questions** it picks to suit the crawler. Ask in-fiction from the kiosk. Players may answer "pass" to any one; a pass is also data.

**Core six**

| # | System asks | What the System is mining (DM-only) |
|--:|-------------|-------------------------------------|
| Q1 | "What were you holding when the world ended?" | An object fixation; often the seed of a running gag |
| Q2 | "What's the last thing you bought that you absolutely did not need?" | A collecting impulse (plush, hats, knives, hot sauce, sneakers) |
| Q3 | "What's something harmless that you are nonetheless terrified of?" | **Dislike/fear**: what the System "accidentally" gives them |
| Q4 | "What do your friends make fun of you for?" | Running gag candidate; tone guide for roasts |
| Q5 | "Name a smell, food, or song that makes you happy. One. Don't be weird about it." | A comfort item; something to give, withhold, or ruin |
| Q6 | "In a fight, what's your plan? Be honest; we'll know." | **Build needs** + Standing Orders sanity check |

**Bonus pool (System picks 0–2)**

- "Who did you leave behind? You don't have to answer. We'll find out anyway." (Handle with care; this is often the only emotional thread a crawler brings in. Use for drama, never for cheap shots unless the player plays it for laughs.)
- "What's your worst habit?"
- "What would you do with a million credits? (You will never have a million credits.)"
- "What's a hill you would die on? Literally, in this case."
- "What's your shoe size?" (The foot audience asked. Answering is optional. Answering *with enthusiasm* is a red flag the System will remember.)
- "Describe your mother in three words." (Fuel for "your mom" jokes; skip for any crawler whose answers suggest it would land wrong; see §2.4.)

**Asking for loot during the questionnaire** ("I want a flaming sword") is itself a candidate for **Customer Feedback** (`02` App. C, R0): "Your request has been received and laughed at."

### 5.3 Turning answers into a Fan Profile (DM-only)

Within the first session, the System writes a **draft Fan Profile** in session state:

```text
FAN PROFILE | <crawler>
Likes/fixations (2–3): <from Q1, Q2, Q5, or hook>
Dislike/fear (1): <from Q3>
Running gag (0–1): <from Q4 or the best questionnaire answer; may stay empty until play produces one>
Build needs (1–2 lines): <from class/sub-class trajectory + Q6 + equipment gaps>
Source: intake draft (session 1). Confirm or revise by first saferoom.
```

Rules for the draft:

1. **Draft, then let play overrule it.** By the **first saferoom** (Welcome Box), keep or swap each entry based on what the crawler has actually done. By descent, the profile should be mostly play-built.
2. **Pick a running gag only if it's funny to the player too.** A good gag is something the player will *groan* at, not resent. Default to none until a candidate proves itself.
3. **Never state the profile to the player.** They figure it out when the third plush narwhal shows up.
4. **Build needs are honest.** Even if the gag is stupid, the build-needs line should name what genuinely helps their 5e build (`02` §3.5 rule 4: at least half of meaningful drops are usable).
5. **Respect opt-outs.** Anything under `COMFORT-OPTOUT` is never a gag or a fear item (§2.4).
6. The **Welcome Box** (Bronze, opened in the first saferoom, `02` §10.2) **must include one tailored pull** drawn from this profile. That's the first moment players realize the System was listening.

### 5.4 Example

> Q1: "My phone, mid-text to my ex." · Q2: "A limited-edition plush axolotl." · Q3: "Moths." · Q4: "I cry at commercials." · Q5: "Cinnamon gum." · Q6: "Stab first, apologize never." Class: Rogue.
>
> Draft profile: **Likes** plush collectibles (axolotl line), cinnamon gum · **Fear** moths · **Gag** (candidate) cries at the System's sponsor ads; the System starts running sappy ads at them during tense moments · **Build needs** a better finesse weapon; anything that helps them get Advantage for Sneak Attack.
>
> Welcome Box tailored pull: a **Limited Edition Plush Axolotl, "Regret" Variant** (cosmetic) + a pack of cinnamon gum that is actually a *Potion of Healing* in chewable form (reskinned consumable, counts as R3 budget).

---

## 6. Starting kit, credits, and System Inventory

### 6.1 Standard 5e kit (unchanged math)

- **Class:** take the class's listed starting-equipment package **or** its listed gold option, per the 2024 PHB / SRD 5.2.
- **Background:** take the background's equipment package **or** its gold option (50 GP in the 2024 rules).
- **Credits = GP**, 1:1 (`02` §5.10). Starting credits are exactly what 5e chargen gives; the Crawl adds **no** stipend.
- Buying gear with the gold option: the System runs it as the **Intake Vending Wall** (5e prices, PHB equipment lists). No magic items at intake.

### 6.2 Reskin the kit as junk

Everything is reskinned to look like it came from a strip mall, a hardware store, or the crawler's pockets. **Name, damage, properties, mastery, AC, and weight don't change.** Write both on the sheet: `Sharpened Stop Sign (Longsword)`.

| 5e item | Example junk reskin |
|---------|---------------------|
| Longsword | Sharpened stop sign on a broom handle |
| Greataxe | Fire axe from a hallway case, still has the "BREAK GLASS" sticker |
| Shortsword / dagger | Kitchen knife, box cutter, a very serious letter opener |
| Mace / club | Crowbar, rebar, a mini-fridge door handle with bolts in it |
| Quarterstaff | Mop handle, wrapped in duct tape |
| Shortbow / longbow | Compound bow from a sporting-goods display, price tag still on |
| Light crossbow | Nail gun with a homemade stock (still a crossbow mechanically: bolts, Loading) |
| Leather / studded leather | Motorcycle jacket, hockey pads, stab-vest from a mall cop |
| Chain mail | Chain-link fencing laced over a work coverall |
| Shield | Stop sign, trash-can lid, riot shield marked "PROPERTY OF ORIENTATION" |
| Arcane focus | A crystal from a gift shop, a laser pointer, a vape pen |
| Explorer's / Dungeoneer's Pack | Backpack from the lost-and-found with someone else's gym clothes |

### 6.3 Intake Bag (cosmetic, zero value)

Every crawler also gets a **clear plastic Intake Bag** with: a lanyard printed with their Intake Tag, one packet of System-brand electrolyte powder (tastes like a battery; no mechanical effect), and a laminated card reading *YOU ARE ON CAMERA*. These are flavor only and can't be sold (vendors "aren't accepting returns on dignity").

Plus **one personal item** from Q1 (§5.2) if it's plausibly on them: a phone (dead, or alive with zero signal and one app the System installed), keys, a vape, a dog leash with no dog. **Mundane, trivial, no mechanics** unless 5e already prices it as gear the crawler bought.

### 6.4 System Inventory (`02` §5.9)

Explain once: extradimensional inventory like a *Bag of Holding* (500 lb / 64 cubic feet; contents weightless). Storing or retrieving one item = your free object interaction, or the **Utilize** action if already used. No living creatures. Unopened loot boxes take no space. On death it drops as a corpse cache.

> "Your inventory holds five hundred pounds. Please do not try to store your friend. We've had a lot of people try to store their friend."

### 6.5 What crawlers do NOT start with

- No loot boxes (the **Welcome Box** arrives at the first saferoom, `02` §10.2).
- No magic items. No Charms. No buffers (`02` §6.5: DM-granted only).
- No sponsors, no Broadcast Name feature, no Ratings above **Unknown**.
- No achievements, except the intake toast below, which pays nothing.

---

## 7. Species: latent on F1–2, manifests on F3

### 7.1 Rules (from `02` §7.2–7.3)

- Choose a species **mechanically at level 1** (2024 PHB / SRD 5.2, per `02` §7.1). All traits work from session 1.
- **Everyone looks baseline human on Floors 1–2.** No horns, tails, scales, wings, or size change on camera. (Size is still mechanically the species' size; a halfling is Small and the System's chyron calls them "compact.")
- **Traits are "quirks"** with a mundane-ish explanation the System narrates and is visibly bored by.
- **F3 identity market:** the species **manifests** (body visibly becomes the species; no mechanical change). **One free rebuild** (swap species and/or background, redistribute background increases; same level, same class). **Official Class Title** with the level-3 subclass.
- **Later teases** (F8 Echo Self, F13 Ledger Name, F16 mirror splits) are reskin/story layers unless a floor doc says otherwise.

### 7.2 Quirk translations (examples; species from SRD 5.2)

| Species | Trait | F1–2 "quirk" fiction |
|---------|-------|----------------------|
| Dragonborn | Breath Weapon; Damage Resistance | "Acid reflux. Weaponized." Breath weapon comes out as a cough with special effects. Resistance: "you just don't feel it like other people do." |
| Dwarf | Darkvision (120 ft); Dwarven Resilience; Dwarven Toughness (+1 HP at level 1, +1 again at each level gained); Stonecunning (Bonus Action: Tremorsense 60 ft for 10 minutes while on stone; Proficiency Bonus uses per Long Rest) | "Your pupils do a thing." Poison resistance: "Raised on gas-station sushi." Tremorsense: "You can feel the floor gossiping." |
| Elf | Darkvision; Fey Ancestry; Trance | "You don't sleep, you *buffer*." |
| Gnome | Darkvision; Gnomish Cunning (Advantage on Intelligence, Wisdom and Charisma saving throws) | "You've always been hard to hypnotize. Telemarketers hated you." |
| Goliath | Giant Ancestry; Large Form (at 5th) | "Big-boned, and the bones have opinions." Large Form arrives later; the System calls it a "growth spurt" if it happens before F3. |
| Halfling | Luck; Brave; Naturally Stealthy | "Statistically suspicious." Luck rerolls get a little *ding* sound. |
| Human | Resourceful; Skillful; Versatile | "Baseline. Congratulations on being the control group." The System is disappointed on principle. |
| Orc | Adrenaline Rush; Relentless Endurance; Darkvision | "You refuse to fall down. It's rude, honestly." Relentless Endurance is a *species trait*, not a `02` §6.5 buffer; it works as written. |
| Tiefling | Fiendish Legacy; Otherworldly Presence | "You run a little hot. Your browser history runs hotter." Spells cast as "weird luck" with a smell of struck matches. |

If the 2024 PHB adds species beyond the SRD, use the same pattern.

### 7.3 The tease (how the System plays it on F1–2)

- When a quirk fires the first time, toast it as a **"Biology Anomaly (Logged)"**, R0 by default. Never explain.
- Mirrors and reflective surfaces in the Orientation Pit **flicker** for a frame: a horn, an ear, a tail-shaped shadow. The System's camera always cuts away. No mechanics.
- If a player asks why they have darkvision: "*Your file is under review.*"
- If the table chose a species for a joke, the System knows, and will be insufferable about it on F3.

> "Biology Anomaly (Logged). You can see in the dark. We've noted it. We've noted *everything*."

---

## 8. Multiplayer typed-input flow

Intake runs **in parallel**: every player is in their own booth; the System handles them in rounds. Aim for each round to take 3–5 minutes of real time.

### 8.1 Rounds

| Round | System posts (one post to the whole table) | Players reply (each, in one message) |
|------:|--------------------------------------------|-------------------------------------|
| 0 | Table setup questions (§2) | One reply per player; for this campaign Death Mode is already logged (**Costly Revives**) and is only confirmed; for a table without a logged default, majority decides and ties go to **Canon Hard**. Opt-out explained. |
| 1 | Wake-up read-aloud + "Name / Look / Hook" | `NAME: … / LOOK: … / HOOK: …` |
| 2 | "Class + Background + Species" (link to options) | `CLASS: … / BACKGROUND: … (+2 X, +1 Y or +1/+1/+1) / SPECIES: …` |
| 3 | "Scores + Equipment" | `SCORES: array/point buy/roll … / KIT: class A or B; background A or B` |
| 4 | Questionnaire (core six; the System adds bonus questions per crawler) | `Q1: … Q2: … Q3: … Q4: … Q5: … Q6: …` (+ bonus) |
| 5 | Pending Handle + Standing Orders / Reactions | `HANDLE: … / ORDERS: … / REACTIONS: …` |
| 6 | **Sheet summaries** for everyone + intake toasts | `LOCK` or one correction |

- The System answers **rules questions inline** and asks **at most one clarifying question** per player per round (`02` §2.5.1).
- **Private vs public:** names, looks, classes, and species are public. **Questionnaire answers can be sent privately** (player's choice); the System never reads private answers aloud and treats them as DM-only. Opt-outs are always private.
- **Stragglers:** if a player hasn't replied 10 minutes after a round post, the System nudges once; after another 10, it offers "System Picks For You" (a legal default for that step, stated openly, changeable before LOCK). Players can't be timed out of the questionnaire; a missing answer is just a blank.
- **Late arrivals:** run them through the same rounds in a single compressed post while the others start Floor 1 Lesson 0; they enter at the first natural door (or "different hallway").
- **New-to-5e players:** the System offers three **pre-built concepts** per class on request (e.g., "Fighter: sword-and-board bouncer, standard array assigned, Guard background, Human"), and fills in the math for them to approve.

### 8.2 Posting template (players can paste this)

```text
NAME:
LOOK:
HOOK:
CLASS:
BACKGROUND: (ASIs: +2 __ +1 __  or +1/+1/+1)   ORIGIN FEAT:
SPECIES:
SCORES: (array / point buy / roll)  STR __ DEX __ CON __ INT __ WIS __ CHA __
KIT: class (A/B), background (A/B); purchases:
Q1–Q6: (or "sending privately")
HANDLE (requested):
STANDING ORDERS:
STANDING REACTIONS:
```

### 8.3 System summary format (round 6)

```text
╔══ CRAWLER FILE: #0417-K ═════════════════════════════╗
  Name: Dee Marsh        Handle: PENDING (req: "Hex")
  Provisional Class: Rogue 1   Prior Employment: Criminal
  Latent Biology: Halfling (quirk: "statistically suspicious")
  STR 8 DEX 17 CON 14 INT 12 WIS 10 CHA 13   PB +2
  HP 10  AC 14  Speed 30 ft  Hit Point Dice 1d8
  Gear: Box Cutter (Dagger), Pawnshop Shortsword (Shortsword),
        Mall-Cop Vest (Leather Armor), Bobby Pins (Thieves' Tools)
  Credits: 14   Boxes: none   Ratings: Unknown
  Orders: Sneak Attack the closest flanked enemy; hide after.
  Reactions: Uncanny Dodge (from L5); OAs on.
  Death Mode: Costly Revives (logged default). Comfort: Ludicrous.
╚══════════════════════════════════════════════════════╝
```

(Numbers here are an example; the System computes from actual choices.)

---

## 9. Sample intake dialogue

Two players, Costly Revives (campaign default, already logged), `COMFORT=Ludicrous`. AI rolls dice. Player text in quotes.

> **SYSTEM:** Booth 3 is awake! Booth 3, you've been asleep for nine hours, you snore like a leaf blower, and the audience has named your drool puddle "Lake Disappointment." Name, look, hook. One line each.
>
> **PLAYER (Mara):** "NAME: Rosalind 'Roz' Pike / LOOK: 50-year-old school bus driver in a reflective vest and orthopedic sneakers / HOOK: Has driven forty seventh-graders through a blizzard. You are not scary."
>
> **SYSTEM:** Orthopedic sneakers. The foot segment of our audience just sat up. Roz, we have *so* much to discuss. Class?
>
> **PLAYER (Mara):** "Paladin. Background Guard. Species... dwarf?"
>
> **SYSTEM:** Provisional Paladin. Prior Employment: *Guard*. That's two skills, a tool, and a lifetime of saying "no running" to people who didn't listen. Latent Biology: Dwarf. You'll look exactly like yourself for a while. Your poison resistance will be filed as "raised on cafeteria tacos." Scores?
>
> **PLAYER (Mara):** "Standard array: Str 15, Cha 14, Con 13, Wis 12, Dex 10, Int 8. Guard gives +2 Str, +1 Wis."
>
> **SYSTEM:** Str 17, Dex 10, Con 13, Int 8, Wis 13, Cha 14. Int 8. Bold. Honest. Kit: class package or gold?
>
> **PLAYER (Mara):** "Package for both."
>
> **SYSTEM:** Logged. Your chain mail is a chain-link fence you laced over a mechanic's coverall; your longsword is a sharpened STOP sign on a broom handle. It's still a longsword, d8 slashing, Sap. Now, a short customer survey. One: what were you holding when the world ended?
>
> **PLAYER (Mara):** "A thermos of coffee and a clipboard with the attendance sheet."
>
> **SYSTEM:** Two: last thing you bought you didn't need?
>
> **PLAYER (Mara):** "A fourth crossword-puzzle book. I haven't finished the first three."
>
> **SYSTEM:** Three: something harmless that terrifies you.
>
> **PLAYER (Mara):** "Clowns. Don't."
>
> **SYSTEM:** We would never. *(Session state: Fear: clowns.)* Four through six, then the handle.
>
> *(...)*
>
> **PLAYER (Jae):** "Q2: a hat. I buy a hat every time I'm sad. I own sixty hats. Also, can my first loot box have a flaming sword?"
>
> **SYSTEM:**
> ```text
> ╔══ NEW ACHIEVEMENT ═════════════════════════════════╗
>   Customer Feedback
>   You asked the System for a specific reward during a survey
>   about your feelings.
>   REWARD! Your request has been received and laughed at.
>   Then laughed at again, in the break room.
> ╚════════════════════════════════════════════════════╝
> ```
> Sixty hats, though. We heard that part. *(Session state: Likes: hats. Running gag candidate.)*
>
> **SYSTEM (round 6):** Files locked. Crawler #0417-K "Roz" and Crawler #0388-B "Jae," please exit your booths. Watch your step. The step is lying.
>
> ```text
> ╔══ NEW ACHIEVEMENT ═════════════════════════════════╗
>   Paperwork Survivor
>   You completed intake without dying, crying, or reading
>   the Terms of Service. Two out of three ain't bad.
>   REWARD! ...
>   No. It's paperwork. Nobody gets a prize for paperwork.
> ╚════════════════════════════════════════════════════╝
> ```

(`Paperwork Survivor` is a `NEW:` snark-only achievement; log it as R0.)

---

## 10. DM notes

### 10.1 Tone

- The intake is the **first impression of the System**: theatrical, petty, crude, never boring. One strong line per beat. Don't monologue.
- Roast the **job, the choices, the gear, and the dumb answers**, not the player. At `Ludicrous` you can be filthy; you still can't be lazy.
- Let the *audience* carry some jokes ("Our foot fans have *questions*"). It spreads the cruelty around and seeds sponsors.
- Keep rules language clean even when the voice is dirty: the summary card (§8.3) is plain numbers.

### 10.2 Comfort and opt-out (repeat of §2.3–2.4, because it matters)

- Default `COMFORT=Ludicrous`. Respect the hard floors in §2.3.
- Any crawler can opt out of a joke or topic **privately**; the System drops it immediately, logs `COMFORT-OPTOUT`, never mentions it again, and retires any gag that touches it.
- If a player goes quiet after a joke, the System can check in privately once ("Still good? Say 'cut' and that bit's gone"). It doesn't make a scene of it.

### 10.3 Edge cases

| Situation | Ruling |
|-----------|--------|
| Player wants a non-SRD species/class but the table doesn't own the 2024 PHB | SRD 5.2 only (`02` §7.1). Offer the closest SRD option as a reskin; the F3 identity market can revisit. |
| Player wants to *look* like their species now | Default no (`02` §7.2, latent). Owner question in §13. The System may allow a *partial* tell ("weirdly pointy ears, nobody comments"). |
| Homebrew species/class | Owner approval only (`02` §7.1). |
| Multiclassing at intake | Not possible at level 1 (5e). |
| Feats | Origin feat from background (and Human's Versatile), per 5e 2024. |
| Player wants starting magic items | No (§6.5). |
| Player builds a crawler around the running gag | Allowed, but the System picks the gag. It may pick a *different* one out of spite. |
| Replacement crawler mid-floor | Same intake, compressed (see the next paragraph for a player's other Crawlers). Level, gear, and late-entry Silver box per `02` §6.3. Fresh Fan Profile. Run the questionnaire. |
| Player answers questionnaire as their crawler vs as themselves | Either is fine; the System asks once which, and treats crawler answers as canon. |

**Several Crawlers per player (v0.2.2 pointer).** A player may create more than one Crawler, but only one is **active**; the others are **benched** on file (no slot, credits, XP, loot or trades). The active Crawler is locked for the whole session and can change only at session zero or between sessions, never mid-session, not even in a safe room. A Crawler that dies is replaced from the player's benched Crawlers at the next between-session window, with level and gear per `02` §2.3 and §6.3. Each Crawler gets its own sheet channel `#<player>-<crawler>`, and a player can remove one of their own with `/delete` (the active Crawler not while a session is open). Full rules, tool requirements and checklists: `characters/create-flow-spec-5e.md` §8 and `decisions/020-multiple-crawlers-active-swap.md` (Syndicate defaults, Caleb may override; the session lock, layout and `/delete` are Caleb's). Intake itself is unchanged: each Crawler runs the same steps.

### 10.4 Session-state entries to create at intake

```text
DEATH-MODE: Costly Revives (campaign default) | Canon Hard | Soft Open
F1-REPRIEVE: ON | OFF
COMFORT: Ludicrous
COMFORT-OPTOUT: (private; per crawler; never shown)
DICE: AI rolls | players roll    FUDGING: off
TIMEOUTS: turn 3m / reaction 60s / nudge 10m    BLOCKS: on
CRAWLER | <name> | Intake Tag | class/bg/species | HP/AC/HD | credits
HANDLE-REQUEST | <crawler> | <text or none>
HANDLE-AUDIENCE | <crawler> | (set during Floor 1)
FAN PROFILE | <crawler> | (draft from §5.3; DM-only)
RATINGS | <crawler> | Unknown
ACH | <crawler> | NEW:Paperwork Survivor (or other intake toast) | R0 | — | F1/S1
```

---

## 11. Crawler sheet template

```text
CRAWLER FILE
Name:                    Intake Tag: CRAWLER #____-_
Broadcast Name: PENDING  (requested: ________ / audience: ________)
Look (one line):
Hook (one line):

Provisional Class / Level:        Subclass (F3): —
Prior Employment (Background):    Origin Feat:
Latent Biology (Species):         Quirk description:
STR __ (_)  DEX __ (_)  CON __ (_)  INT __ (_)  WIS __ (_)  CHA __ (_)
Proficiency Bonus: +2   Saves:   Skills:   Tools:   Weapon Masteries:
HP __ / __   Temp HP __   Hit Point Dice __d__ (__ left)   AC __   Speed __ ft
Initiative +__   Passive Perception __   Passive Investigation __   Passive Insight __
Spell slots / features / uses:
Conditions:          Exhaustion: 0          Heroic Inspiration: ☐

Equipment (junk name → 5e item):
System Inventory:
Credits:
Unopened boxes (open in saferooms only; not tradeable):
Attuned items (max 3):
Charms (max 2):

Standing Orders:
Standing Reactions:

Achievements (ID or NEW: name | tier):
Titles (cosmetic):
Ratings tier: Unknown
Sponsors / riders: none
Spine flags: SEED-ODDCOIN ☐  SEED-BENEFACTOR ☐  (others as they surface)
```

The **Fan Profile** and **opt-outs** are **not** on the player-visible sheet. They live in session state (DM-only).

---

## 12. Quick-start checklist

**Table (once)**

- [ ] Death Mode chosen and logged (`DEATH-MODE`; campaign default **Costly Revives**, already picked, so confirm only); Floor 1 Reprieve ON/OFF logged.
- [ ] `COMFORT=Ludicrous` confirmed; **private opt-out explained** (code word "cut").
- [ ] Dice (AI rolls), fudging (off), timeouts (3m / 60s / 10m), crawler blocks (on) confirmed.
- [ ] Content source confirmed: 2024 PHB or SRD 5.2 only.

**Each crawler**

- [ ] Name, look, hook.
- [ ] Class (Provisional), background (ASIs + Origin feat), species (latent + quirk line).
- [ ] Ability scores (array / point buy / roll) with background increases applied.
- [ ] HP, AC, Hit Point Dice, initiative, passives, spells/features computed.
- [ ] Equipment (class + background option), reskinned junk names, credits.
- [ ] Intake Bag + one personal item (cosmetic).
- [ ] Questionnaire answered (core six, bonus as asked); private answers kept private.
- [ ] Requested Handle logged; sheet says `Broadcast Name: PENDING`.
- [ ] Standing Orders + Standing Reactions written.
- [ ] Sheet summary posted and LOCKED.

**System (DM-only)**

- [ ] Draft Fan Profile written per crawler (§5.3).
- [ ] Ratings = Unknown; no sponsors; no boxes; no Broadcast Name feature.
- [ ] Intake toast posted (snark-only) and logged.
- [ ] Load `floors/floor-01-5e.md`; start at Lesson 0.

---

## 13. Open for owner markup

1. **Questionnaire length:** six core questions plus up to two bonus OK, or trim to four for speed?
2. **Questionnaire transparency:** players are never told answers feed loot. Keep it hidden, or tell them up front ("the System is listening") for the fun of paranoia?
3. **Visible species:** keep everyone baseline human on F1–2 (`02` §7.2), or allow small tells (ears, eye color) from the start? (Mirrors `02` §12 Q3.)
4. **Rolling stats:** RESOLVED (Caleb, 2026-10-04, decision 024): Roll is a third method, on by default; see §3.6.
5. **Pending Handle:** is a Requested Handle + audience nickname on F1 the right way to "plant" the Broadcast Name without breaking `02` §5.1's F3 unlock? Should the F3 choice (request vs audience vs mash-up) be the player's, or the System's?
6. **Intake Tag format** (`CRAWLER #0417-K`): fine, or do you want a different ID style?
7. **Comfort hard floors (§2.3):** anything you want to add or loosen? Is the "jokes, not scenes" line for sexual crudity where you want it?
8. **The foot bit:** audience segment only, or should it become a named F6 sponsor with a rider?
9. **"Your mom" bonus question:** keep, or drop as too likely to hit a real nerve?
10. **Pre-built concepts** for new players (§8.1): want me to write a set of 12 (one per class) as an appendix?
11. **Rebuild on F3:** current rule is one free species/background swap. Should a class swap also be allowed for players who hated their Provisional Class?
12. **Late arrivals:** compressed intake while others start Lesson 0, OK?

---

## Change log

| Version | Date | Notes |
|---|---|---|
| v0.2.2 | 2026-10-04 | Pointer paragraph in §10.3 for several Crawlers per player (one active, others benched; swaps only at session zero or between sessions; sheet channel per Crawler; `/delete`); extra cross-reference in the replacement row. No intake step, number or rule changed. Earlier history lives in the header and status lines. |
| v0.2.3 | 2026-10-04 | §3.6: **Roll** added as a third ability-score method (three arrays of 4d6 drop lowest, keep ONE array totalling 73+, reroll all three if none qualifies, every die logged, assign freely, switch `create.allow_roll` default ON; decision 024); step 6 name, `SCORES:` line, sheet template line, checklist and Open Q4 follow. Standard array and point buy unchanged. |

---

*SRD attribution: see `02-core-rules-5e.md` Appendix D. This file references 5e rules by name and does not reproduce book text.*
