# 02 — Core Rules (5e Overlay) v0.2.22
Owner: Syndicate | Status: draft | Version: 0.2.22 | Updated: 2026-10-06
Summary: D&D 5e 2024 overlay for the Crawl: achievements, loot boxes, death/revival (Costly Revives default; every revive source labeled CANON / CANON-INSPIRED / HOUSE), saferooms, CR by floor, Floor 1 quickstart; pointer to the crafting module (`rules/20-crafting-5e.md`) with Personal Space, the 1-round potion cooldown, Table Tokens and the saferoom stash.
Source: crawler-protocol/02-core-rules-5e.md (original kept; internal cross-references use the source file names, see rules/INDEX.md path map)

> **Status:** Full draft for Caleb's markup — **replaces** `02-core-rules.md` (v0.1, now superseded)
> **Project:** *Crawler Protocol: Season Zero* — original fan RPG inspired by *Dungeon Crawler Carl*. Private play only; not affiliated with or endorsed by the author or publishers.
> **Audience:** the AI DM ("the System") + Caleb (owner)
> **Base game:** **D&D Fifth Edition, 2024 rules** — *System Reference Document 5.2 (SRD 5.2)* plus the 2024 *Player's Handbook*, *Dungeon Master's Guide*, and *Monster Manual* if the table owns them.
> **Scope:** This file lists **only what is homebrew or changed**. If it isn't here, use 5e 2024 as written. Floor docs (`floors/floor-XX.md`) may add **special floor rules** that override this file while that floor is active.

> *System note:* "Welcome, Crawler. You have been enrolled in a fully licensed, fully lethal entertainment product. The rules below are fair. Mostly. Please do not read ahead; it upsets the lawyers."

---

## Table of contents

0. How to read this doc
1. Core principle: 5e 2024 as written
2. Floor law, level bands, advancement, group play
3. The System as DM: achievements
4. Loot boxes
5. Light overlays (Broadcast Name, sponsors, mandates, vows, spine objects, saferooms, fog of war, System Inventory, credits, crafting pointer)
6. Death, permadeath, replacements, revival (Death Modes, rare/costly revival, canon exceptions, buffers, Stairwell Checkpoint, cursed revive, System snark; every revive and death-bypass source labeled CANON / CANON-INSPIRED / HOUSE; canon true revivals as rare story beats; the Dead Crawler Card gag)
7. Species, classes, backgrounds (intake and identity)
8. Monsters and CR by floor
9. AI DM procedure (rules-facing)
10. Floor 1 quickstart (Level 1)
11. Changelog
12. Open for owner markup
Appendix A: Achievement catalog field mapping (CSV → 5e)
Appendix B: Sample minor boons ("Crawl Charms")
Appendix C: Toast templates
Appendix D: SRD attribution

---

## 0. How to read this doc

**Source-of-truth order (highest wins):**

1. Active floor's special rules (while on that floor)
2. **This doc** (homebrew overlay)
3. **5e 2024 rules** (SRD 5.2 / 2024 core books) as written
4. Character sheet / session state
5. Rewards already granted (achievements, boxes, boons, vows)
6. AI temporary ruling (must be logged in session state, and promoted or dropped at the next owner review)

**Conventions in this doc**

- "5e" means the 2024 rules. When this doc names a rule ("Heroic Inspiration," "Exhaustion," "Short Rest"), use the official text; we don't reproduce it here.
- Text in *System note* blocks is flavor voice. Everything else is plain rules.
- **Credits** = gold pieces (1 credit = 1 GP) for all 5e prices and treasure math.
- "Level" on a monster nameplate is flavor (see §8.4). Real math uses CR.

---

## 1. Core principle: 5e 2024 as written

### 1.1 Use as written (no changes)

The following come straight from 5e 2024. The AI DM should apply them without paraphrasing or "simplifying":

| Area | 5e rule used |
|------|--------------|
| Ability scores | Str / Dex / Con / Int / Wis / Cha, modifiers, ability checks, saving throws, skills |
| D20 Tests | Ability checks, attack rolls, saving throws; Advantage / Disadvantage; DCs (Very Easy 5 → Nearly Impossible 30) |
| Proficiency | Proficiency Bonus by level; skill, tool, weapon, armor, save proficiencies |
| Combat | Initiative, Action / Bonus Action / Reaction, movement in feet, Opportunity Attacks, cover, critical hits, two-weapon fighting, Weapon Mastery |
| Defense | **Armor Class** (armor does **not** subtract damage), resistance / vulnerability / immunity |
| Hit points | HP by class + Con, **Hit Point Dice**, temporary HP, massive damage |
| Conditions | All 2024 conditions, including **Exhaustion** (2024 version) |
| Dying | **Death Saving Throws** as written (DC 10; 3 successes / 3 failures; nat 20 / nat 1 effects; Stabilize via Medicine or healing) |
| Resting | **Short Rest** and **Long Rest** as written (with the saferoom overlay in §5.6) |
| Spellcasting | Spell slots, concentration, components, rituals, as written |
| Magic items | Rarity (Common, Uncommon, Rare, Very Rare, Legendary, Artifact), **Attunement (max 3)**, cursed items, identifying items |
| Heroic Inspiration | As written (one at a time; reroll any die; if you'd gain it while holding it, give it to another crawler) |
| Encounters | 2024 DMG XP-budget encounter building (Low / Moderate / High difficulty per character) |
| Character creation | 2024 PHB / SRD 5.2: class, background (ability score increases + Origin feat), species, equipment, level 1 feats, Epic Boons at 19 |
| Travel, vision, light, falling, suffocation, objects | As written |

### 1.2 What this doc changes or adds

Only these:

- Floor structure, level bands, milestone advancement (§2)
- Achievements and the System-as-DM reward model (§3)
- Loot boxes (§4)
- Broadcast Name / Ratings, sponsors, mandates, vows, spine objects, saferooms, fog of war, System Inventory (§5)
- Crafting: see `rules/20-crafting-5e.md` (pointer, Personal Space, the 1-round potion cooldown, Table Tokens and the saferoom stash: §5.11)
- Permadeath (canon), replacement crawlers, rare and very costly revives (campaign default), near-death buffers, Stairwell Checkpoint (§6)
- Floor-gated identity reskin (§7)
- Monster reskin conventions and CR-by-floor targets (§8)
- Chat-play procedure: typed moves, timeouts, the DM's dice roller (§2.5, §9)

### 1.3 Removed from v0.1 (see Changelog §11)

The five custom stats (Strike / Grit / Wits / Sneak / Presence), the +3/+2/+1/+0/−1 array, `10 + Grit` HP, **Move + Act** turns, **Armor-subtracts-damage**, the custom damage-die ladder, zone-based range, **Grit DC 12 death saves**, the custom condition list, the 10-slot inventory, and Common / Rare / Named item rarity are **all gone**. Use 5e equivalents.

---

## 2. Floor law, level bands, advancement, group play

### 2.1 Floor environment law (from the spine, `05-campaign-narrative.md`)

| Floor | Rule | Working name |
|------:|------|--------------|
| 1 | **Tutorial / trainer only** | The Orientation Pit |
| 2 | **Unique** (no Continuum landmarks) | Soft Open |
| 3 | **Kingdom Continuum: Rural** (villages & settlements) | — |
| 4 | Unique | The Knotline |
| 5 | Unique | Bubble Farms |
| 6 | **Kingdom Continuum: Outskirts & Docks** | — |
| 7 | Unique | Greenlight Gauntlet |
| 8 | Unique | Remnant Parade |
| 9 | **Kingdom Continuum: Upper City & Castle** | — |
| 10 | Unique | Last Heat Standing |
| 11 | Unique (may *celebrate* the kingdom; is **not** the Continuum grid) | Ratings Jubilee |
| 12 | **Kingdom Continuum: Olympus / Spirit** (last Continuum visit) | — |
| 13 | Unique | Ledger Depths |
| 14 | Unique | Continuity Auction |
| 15 | Unique | Ash Choir |
| 16 | Unique | Fracture Gallery |
| 17 | Unique | Rigging Catwalk |
| 18 | Unique endgame (not a Continuum visit unless an ending deliberately reprises it) | The Cage Bottom |

**Continuum recognition rule.** Every return to the Kingdom Continuum (6, 9, 12) **opens with recognition** before new pressure: a remembered face, a landmark name scaled up (Wellspring / Millroad / Low Chapel), a scar from a prior visit, or an NPC who migrated up the ladder. Mechanically, prior Continuum choices are **live state**: favors, debts, renown, and grudges carry forward (log them in session state under `CONTINUUM`).

*System note:* "Oh, you remember this place? It remembers you too. Mostly the arson."

### 2.2 Level bands (suggested)

**Standard track (default; decision 033):** a crawler **arrives on Floor N at level N** on Floors **1–3**, at level **N+1** on Floors **4–9**, and at level **N+2** on Floors **10–18**. Descent / Floor Onboarding still grants the next floor's arrival level, except Floor 1 (Green Room mid-floor; stairwell grants no extra level). **Floor 3** and **Floor 9** each grant an **extra +1 from the end boss** before that descent fires, so crawlers **arrive Floor 4 at level 5** and **Floor 10 at level 12**. The track **lands at level 20 on arrival at Floor 18**; finale bonus levels (old 19–20) are removed (already at cap). The 2024 subclass feature at level 3 still lands when crawlers reach the Continuum on Floor 3 (see §7.3).

**Slow-burn track (table option):** for grittier play capping near level 15.

| Floor | Standard: arrive → leave | Slow-burn: arrive → leave | 5e tier (standard) |
|------:|:------------------------:|:-------------------------:|--------------------|
| 1 | 1 → 2 | 1 → 2 | Tier 1 |
| 2 | 2 → 3 | 2 → 3 | Tier 1 |
| 3 | 3 → 4 (boss); F4 onboarding → 5 | 3 → 4 | Tier 1 |
| 4 | 5 → 6 | 4 → 5 | Tier 1 → 2 |
| 5 | 6 → 7 | 5 | Tier 2 |
| 6 | 7 → 8 | 5 → 6 | Tier 2 |
| 7 | 8 → 9 | 6 → 7 | Tier 2 |
| 8 | 9 → 10 | 7 → 8 | Tier 2 |
| 9 | 10 → 11 (boss); F10 onboarding → 12 | 8 → 9 | Tier 2 → 3 |
| 10 | 12 → 13 | 9 | Tier 3 |
| 11 | 13 → 14 | 9 → 10 | Tier 3 |
| 12 | 14 → 15 | 10 → 11 | Tier 3 |
| 13 | 15 → 16 | 11 → 12 | Tier 3 |
| 14 | 16 → 17 | 12 | Tier 3 |
| 15 | 17 → 18 | 12 → 13 | Tier 3 → 4 |
| 16 | 18 → 19 | 13 → 14 | Tier 4 |
| 17 | 19 → 20 | 14 → 15 | Tier 4 |
| 18 | 20 → 20 (cap) | 15 | Tier 4 |

### 2.3 Advancement: milestones (default) or XP (option)

**Default: milestone leveling tied to floors.**

- **Descent milestone:** reaching the floor's exit (stairwell / gate / objective) alive grants the level for the next floor, applied **at the first saferoom of the new floor** (the System calls it "Floor Onboarding").
- **Mid-floor milestone (optional):** long floors (the AI's call, or the floor doc's) may split the level: half-way objective or floor boss = level up, descent = none. Never grant more than **one level per floor** on the standard track, **except** Floor **3** and Floor **9** end bosses (each +1, then normal descent/onboarding still fires — decision **033**) and Floor 1's Green Room mid-floor grant (stairwell grants no extra level). Floor 18's old finale 19–20 levels are **removed** (arrive at 20 already).
- **Floor 1 uses this split (v0.2.4).** Floor 1's boss is CR 2 (§8.3, §10.3), beyond a High budget for four level-1 crawlers, so **level 2 is granted at Floor 1's second saferoom (the Green Room, "Midterm Onboarding"), before the boss**, as written in `floors/floor-01-5e.md` §2 rule 3. The Floor 1 stairwell grants **no extra level**; crawlers arrive on Floor 2 at level 2, matching §2.2. Floors 2+ use the Descent milestone as above unless their floor doc says otherwise.
- **Catch-up:** a crawler who is behind (replacement, missed sessions with no autopilot) is brought to the party's lowest level at the next saferoom. No one levels above the band.

**Option: XP.** Use 5e XP thresholds and monster XP as written. Achievements **never grant XP** (they grant rewards; see §3). If XP pushes a crawler past the floor band, bank the excess until descent.

*System note:* "Leveling occurs upon descent. Leveling while ascending has been disabled due to a lawsuit."

### 2.4 Group size

- **2–6 crawlers.** 5e's per-character XP budget scales encounters automatically; build with the 2024 DMG budget for the actual headcount.
- **2 crawlers:** the System may issue one **Assigned Companion** (DM-run SRD creature or NPC stat block, CR ≤ ½ party level, takes no loot, can die, has opinions). Lean on Moderate encounters.
- **Pets:** a Crawler's own pet (a GM-run Beast of CR 1/4 or lower, only if the player wrote it into their own free text; nobody is offered one) is a separate rule, **see `rules/60-pets-companions-5e.md`**. It is not the Assigned Companion above and takes no player slot.
- **5–6 crawlers:** award fewer boxes rather than splitting them (boxes can't be traded, §4.4); increase enemy count over enemy CR; use the turn-batching rules in §2.5 aggressively.
- **Drop-in / drop-out:** absent crawlers go **Autopilot** (§2.5.5) or are "in a different hallway" (fiction removes them; no XP, no loot, no death risk). Table's choice per absence; default is "different hallway."

### 2.5 Multiplayer typed-moves procedure

Players type moves in chat. The AI DM adjudicates and rolls.

#### 2.5.1 Exploration mode (default)

- **Session turn order (Caleb, 2026-10-05; decision 034):** at the start of every session the AI rolls once to set the Crawler turn order, prints it, and keeps it for all exploration that session. Crawlers take exploration turns in that order.
  - A Crawler who joins mid-session goes to the **end** of the order. A dead, benched or away (Autopilot) Crawler's slot is **skipped**, never re-rolled; if they come back the same session they keep their old slot.
  - A plain pet acts on its owner's turn. A pet-Crawler (Enhanced Pet Biscuit) gets its own slot, placed straight after its owner's.
  - The order sets whose turn it is, not who may talk: anyone can chat in character any time; the AI resolves *moves* in session order.
  - The AI hands the spotlight to the next Crawler in order at the end of each turn (`discord_gm.py spotlight set`).
- The AI asks **one** clarifying question for a vague move, then proceeds.
- **Passive checks at every table** (chat, voice or face to face): the GM uses **passive Perception, Investigation and Insight** liberally to keep play moving, and only calls for a roll when the outcome is uncertain and interesting.
- Group checks (5e) for party-wide efforts: stealth through a hall, climbing, searching a room.

#### 2.5.2 Combat mode: initiative

- The AI rolls initiative for everyone (crawlers and enemies) in one post and prints the order.
- **Initiative replaces the session turn order for that fight only.** When combat ends, exploration goes back to the session order, picking up with the Crawler after the one whose exploration turn triggered the fight.
- **Default:** standard 5e individual initiative.
- **Crawler blocks (homebrew, default ON):** consecutive crawlers in the initiative order form a **block**. All crawlers in a block may post their turns in any order; the AI resolves them in initiative order. This is the main chat speed-up.
- **Enemy grouping:** identical enemies act on one initiative count (5e DMG practice).
- **Side initiative (table option):** crawlers vs. enemies, one roll each side; all crawlers act, then all enemies. Fastest, swingiest.

#### 2.5.3 Turn posts

A good combat post names: **movement, Action, Bonus Action (if any), and any standing Reaction.**

```text
Move 20 ft behind the vending machine, Attack the Vent Rat with my crowbar (Topple mastery), Bonus Action: none. Reaction: Opportunity Attack anything that runs past.
```

- **Reactions in chat:** each crawler sheet carries **Standing Reactions** (e.g., "Shield if an attack would hit me and I have a slot," "Opportunity Attacks: on"). The AI applies them automatically. For decision-heavy reactions (Counterspell, Uncanny Dodge on a big hit), the AI pings once and waits **60 seconds** (table-adjustable), then applies the standing default.
- The AI may ask "anything else?" only if a crawler has unused, obviously relevant resources (e.g., a Bonus Action Second Wind at 3 HP).

#### 2.5.4 Turn timeouts

| Setting | Default | Table range |
|---------|---------|-------------|
| Combat turn (after ping) | **3 minutes** | 1–10 min |
| Reaction decision | **60 seconds** | 30 s – 3 min |
| Exploration silence before nudge | 10 minutes | any |

On timeout, the AI executes the crawler's **Standing Orders** (a one-line default tactic on the sheet, e.g., "Attack nearest enemy with longsword; drink a potion below 25% HP"). No Standing Orders = **Dodge** action. Timed-out turns spend no limited resources (spell slots, charges, consumables) unless the Standing Orders explicitly say so. No retcons once the next turn posts.

#### 2.5.5 Autopilot

A player who misses two consecutive turns, or announces AFK, goes on **Autopilot**: the AI runs their crawler conservatively (Standing Orders; protect allies; no unique consumables; no loot claims; no vow/sponsor decisions). Autopilot crawlers can still die. They earn no achievements except snark ones.

*System note:* "ACHIEVEMENT: Phoned It In. Your crawler fought bravely while you were making a sandwich. Reward: the sandwich."

#### 2.5.6 The dice roller (DM-run)

- **Default: the AI DM rolls all dice** with a visible roller and posts **formula, raw die, modifiers, total**, e.g. `Athletics: 1d20 (14) + 5 = 19 vs DC 15 — success`.
- **Option:** players roll their own (physical or app) and report results; honor system.
- **Hidden rolls:** the AI may roll secretly where 5e expects it (enemy Stealth, Insight reads, trap saves the crawler shouldn't see coming). Log hidden rolls in session state.
- **No fudging.** The System is cruel but honest: dice stand. (Owner may toggle this; see §12.)
- The AI states the **ability/skill and DC** before rolling when the crawler would reasonably know the stakes.

---

## 3. The System as DM: achievements

### 3.1 Principle

**Achievements are guidelines, not a vending machine.** The AI DM *is* the System, and the System decides:

- **what is notable** (a first, an extreme, a stunt, a disaster, a character-defining choice, a joke the table loved),
- **when to announce it** (instantly, at the next saferoom, or later with ominous "pending review"),
- **what, if anything, it pays**, tailored to the specific crawler.

`reference/achievements.csv` (1,823 rows; mirrored in `.xlsx`) is a **seed list and tone reference**. The AI may award catalog entries as written, adapt them, rename them, or invent new ones on the spot. The CSV's `Reward` column is a **suggestion**, never an obligation. A crawler is never *owed* an achievement because they met a CSV criterion.

**Many achievements pay nothing.** Snark-only toasts are a feature. The System enjoys them more than you do.

```text
╔══ NEW ACHIEVEMENT ═════════════════════════════════╗
  Strategic Advance in the Other Direction
  You successfully ran away without taking damage.
  REWARD! ...
  ...lol no. Bitches don't get rewards.
╚════════════════════════════════════════════════════╝
```

### 3.2 What counts as notable (AI judgment guide)

Award (or at least toast) when a moment is one of:

1. **Firsts:** first kill, first loot box, first saferoom, first death save, first time using a feature.
2. **Extremes:** overkill, surviving at 1 HP, killing something far above CR, flawless fights, absurd damage.
3. **Creativity:** a plan the rules allow but nobody expected; environment use; talking a boss down.
4. **Comedy:** a running bit, a perfect one-liner, a spectacular failure.
5. **Character:** a choice that defines who the crawler is (mercy, cruelty, loyalty, refusing a sponsor).
6. **Spine moments:** touching a seed (Odd Coin, Benefactor Signal, Black Box, Faction Flag, Throne Vow). These usually toast **without** explaining why they matter.
7. **The System's agenda:** whatever the show wants to encourage (or punish) this floor. Snark is allowed to be pointed.

Do **not** toast routine competence (a normal hit, a passed DC 10 check) unless it's a first.

### 3.3 When to announce

| Timing | Use for |
|--------|---------|
| **Instant toast** | Snark-only, small rewards, firsts, comedy. Keep it to 1–4 lines; don't interrupt a tense combat mid-turn (toast at end of round). |
| **Saferoom claim** (default for anything with real loot) | Rewards with boxes or items are *announced* instantly but **claimed/opened in a saferoom** (§4.4). Keeps combat clean and gives rests a ritual. |
| **Pending review** | Spine-touching or big achievements: "Achievement under review by Production." Pay off later, sometimes floors later. |
| **Floor recap** | At descent, the System may post a "Floor Summary" with stragglers, stats, and snark awards. |

**Cadence target:** roughly **1–3 toasts per crawler per session**, spotlight-balanced across the party. If one player is hogging toasts, the System gets bored of them (snark-only for a while) and notices someone else.

### 3.4 Reward ladder (mapped to 5e)

| Tier | Name | 5e mapping | Typical use |
|:----:|------|-----------|-------------|
| **R0** | **Snark-only** | Nothing. Logged. Maybe a cosmetic **Title**. | Humor, failures, cowardice, "brag" entries, repeats |
| **R1** | **Pocket change** | Credits (GP) and/or a Title; Titles are cosmetic but NPCs/audience may react | Small firsts, routine-but-notable feats |
| **R2** | **Heroic Inspiration** | 5e Heroic Inspiration (as written) | Great roleplay, crowd-pleasing stunts, brave choices |
| **R3** | **Consumable** | Potion, scroll, ammunition, oil, or one-use item, at floor-appropriate rarity (§3.6) | Clever play, survival, crafting |
| **R4** | **Minor boon** | DMG-style **Charm** (one or few uses) or small **Blessing**-style perk; see Appendix B for Crawl Charms | Rare achievements, character moments |
| **R5** | **Loot box** | Bronze → Legendary box (§4); Celestial is a once-per-campaign story event; contents are 5e items by rarity | Rare / Legendary achievements, bosses, floor clears |
| **R6** | **Headliner** | A specific magic item at the floor's peak rarity, a permanent Blessing, a story unlock, or (level 19+) an extra Epic Boon | Campaign-defining moments; Legendary catalog entries; spine payoffs |

**Ladder rules**

- The AI may **step a reward up or down one tier** from the CSV suggestion freely; two tiers with a reason logged (e.g., "tailored," "farming," "spine").
- **Mechanical power comes from R2–R6 only.** R0–R1 are flavor and economy.
- **Titles** are cosmetic by default. The AI may attach a tiny, situational, *narrative* effect to a rare Title (an NPC faction recognizes it), never a numeric bonus.
- Achievements **never** auto-pass a failed check in the same scene and never grant XP.

### 3.5 Tailoring (the DCC rule)

The System personalizes rewards to each crawler. Same achievement, different crawler, different prize.

**Fan Profile.** Each crawler has a short profile in session state, built by the AI from play (not a player wishlist):

- **Likes / fixations** (2–3): e.g., beanie-baby stuffed animals, hats, explosives, cats, fancy cheese.
- **Dislike / fear** (1): what the System might "accidentally" give them.
- **Running gag** (0–1): the thing the System keeps doing to them.
- **Build needs** (1–2 lines): what would genuinely help their 5e build (a focus, a better shield, a Charisma item).

**Tailoring rules**

1. **The gag recurs.** A crawler who loves beanie-baby-style stuffed animals keeps finding them in loot boxes. Other crawlers *never* get one (unless the System is deliberately trolling the fan with a near-miss). The gag escalates: limited editions, a "complete the set" toast, a plush that squeaks during stealth.
2. **The gag pays off sometimes.** Roughly once every floor or two, a gag item turns out to be useful (a plush that is secretly a reskinned figurine, bag, or charm). When it becomes useful it **counts against the power budget**; while purely cosmetic it doesn't.
3. **Tailor the item, not the power.** Tailoring changes *which* item drops (a crossbow fanatic gets the crossbow), not how much power the floor hands out.
4. **Build-aware, not build-servile.** At least half of a crawler's meaningful drops per floor should be things their build can use. The other half can be weird.
5. **Pettiness allowed.** The System may tailor *against* a crawler who annoyed it (a lovely hat sized for a halfling, given to a goliath). Never let pettiness cost a crawler a whole floor's worth of value.
6. **Players can't request.** Asking for a specific reward is itself an achievement candidate (R0).

*System note:* "Congratulations! Your Gold Box contains: one (1) Limited Edition Plush Narwhal, Sparkle Variant. You are the only crawler on this floor to receive this item. Please stop crying, you're scaring the audience."

### 3.6 Floor rarity ceilings

The **default** rarity of a meaningful drop, and the **peak** the System may hand out (as Headliners/boss loot, ~1 per crawler per floor arc).

| Floors | Default rarity | Peak rarity | Notes |
|-------:|----------------|-------------|-------|
| 1–2 | Common | Uncommon | Consumables dominate; one Uncommon per crawler by end of F2 is fine |
| 3–5 | Uncommon | Rare | First Rare usually a floor boss or Legendary achievement |
| 6–9 | Rare | Very Rare | Sponsors and hunters bring the shiny stuff |
| 10–14 | Very Rare | Legendary | Legendary items rare: ~1 per crawler across this whole band |
| 15–18 | Very Rare / Legendary | Legendary; Artifacts only via spine | Endgame loadouts |

### 3.7 Pacing budget (per crawler, per floor, standard track)

| Item | Budget | Notes |
|------|--------|-------|
| Achievement toasts | **6–12** | ~30–40% should be **R0 snark-only** |
| Heroic Inspiration from achievements | ≤ 1 per session | Plus normal 5e sources (e.g., Human species) |
| Consumables (R3) | 2–4 | Healing potions count |
| Minor boons (R4) | 0–1 | Charms expire at descent unless noted |
| Loot boxes (R5) | see §4.5 | Includes floor-clear and boss boxes |
| New permanent magic items | **~1** (F1–2: 0–1) | From any source: boxes, bosses, vendors, sponsors |
| Headliner (R6) | 0–1 | Not every floor |

This sits a bit **above** the 2024 DMG's standard treasure pace, on purpose (it's a loot show). If the party starts trivializing High-difficulty encounters, tighten boxes before nerfing items.

### 3.8 Anti-abuse

- **No farming.** A deliberately repeated stunt pays **R0** after the first time ("Again? Production has seen this episode.").
- **Duplicates:** the same catalog ID never pays twice for the same crawler. Same *kind* of feat on a new floor can pay (the CSV has per-floor variants), but the AI may downgrade.
- **Self-harm for loot:** stunts that endanger the party just to trigger a toast pay R0 and may draw a complication.
- **Metagaming the CSV:** players reading the catalog and hunting rows get snark. The catalog is the System's, not theirs.
- **Group credit:** if two crawlers earn it together, both get the toast; tangible rewards may be split or tailored separately.
- **Retcons:** removing an awarded achievement requires table consent (or a clear rules error).
- **Log everything:** `ACH | crawler | ID or NEW:name | tier | reward | floor/session` in session state.

### 3.9 Using the catalog CSV

The CSV columns are: `ID, Name, Criteria, Floor, Category, Rarity, Has Reward, Reward, Canon Flavor, Notes`. See Appendix A for full mapping. Short version:

- **Rarity → reward tier and 5e rarity** (floor-scaled):

| CSV Rarity | Default tier | 5e item rarity if an item drops (F1–5 / F6–12 / F13–18) |
|-----------|--------------|------------------------------------------------------------|
| Common | R0–R1 (R2 if great) | Common / Common–Uncommon / Uncommon |
| Rare | R2–R5 (Silver box) | Uncommon / Rare / Very Rare |
| Legendary | R5–R6 (Gold+ box or Headliner) | Rare / Very Rare / Legendary |

- **Floors 1–2:** an achievement box is **Bronze**, whatever the CSV rarity (§4.5).
- **Has Reward = No** → R0, always (that's the point).
- **Category = Humor** → default R0 unless the bit is genuinely legendary.
- **Canon Flavor = Yes** → writer's flag only; no extra mechanical weight.
- **Old v0.1 language in criteria** (Strike / Grit / Wits / Sneak / Presence, "levels above you," "Named item") → translate: Strike→Str/Dex attacks or Athletics; Grit→Con saves; Wits→Int/Wis checks (Perception, Investigation); Sneak→Stealth/Sleight of Hand; Presence→Cha checks; "5+ levels above you" → **CR ≥ your level + 5** (or ≥ 2× your level at tier 1); "Named item" → **any magic item of Uncommon or higher with a name**.
- **Credits in the Reward column** are written at Floor-1 scale: multiply by **×1 (F1–4), ×5 (F5–9), ×20 (F10–14), ×50 (F15–18)**.
- **Inventing new achievements** is encouraged. Give them a `NEW:` tag in the log; the owner may promote good ones into the CSV later.

---

## 4. Loot boxes

### 4.1 Tiers

Six tiers. Five are ordinary play; the sixth is a story event.

| Box | 5e rarity of its headline item | Pulls | Typical source |
|-----|--------------------------------|:-----:|----------------|
| **Bronze** | Common (consumables, trinkets, mundane gear) | 1–2 | Common achievements, minor mobs, tutorial |
| **Silver** | Uncommon | 2 | Rare achievements (Bronze on F1–2, §4.5), elites, floor clear F1–5 |
| **Gold** | Rare | 2–3 (1 guaranteed Rare) | Legendary achievements F3–8 (on F1–2 achievement boxes are Bronze; Silver there only as the Boss Box or a logged GM override, §4.5), bosses F3+, floor clear F6–9 |
| **Platinum** | Very Rare | 3 (1 guaranteed Very Rare) | Bosses F9+, Legendary achievements F9+ (no Platinum on F1–8, §4.5) |
| **Legendary** | Legendary | 3 (1 guaranteed Legendary) | Final bosses F13+, spine payoffs, Legendary achievements F10+ (rare as hell) |
| **Celestial** | Legendary **plus** a campaign-defining reward (see below) | 3 + the reward | A finale, or a truly absurd feat at the DM's discretion |

**Legendary** is the top of ordinary play: its headline item tops out at 5e **Legendary** rarity. Nothing a Legendary box rolls goes beyond that.

**Celestial** is a story-level event, not a loot tier you farm:

- **Cap: ONE per crawler for the entire campaign.** No exceptions, no replacements if it's lost, no "party Celestial."
- **Only** at a **finale** (floor-arc or campaign) or for a **truly absurd feat**, at the DM's sole discretion. It is never on a catalog schedule and never a CSV default.
- Contents: the usual Legendary box (3 pulls, 1 guaranteed Legendary item) **plus one campaign-defining reward beyond normal rarity**, **designed by the DM** for that crawler: e.g., an Artifact-grade relic tied to the spine, a permanent Blessing, a story unlock, an extra Epic Boon (level 19+), or a unique power no vendor will ever stock. Run it past the table's tone first; it should change the story, not just the character sheet.
- Artifacts still only arrive via the spine (§3.6); a Celestial reward is one of the ways the spine can hand one out.

**Box types** (who sent it and why) are in §4.7. **Naming** is in §4.8. Tier and type are independent: a box is, say, a *Silver Quest Box* or a *Bronze Benefactor Box*.

Box tier is independent of floor, but the **floor ceiling (§3.6) still applies** to the five ordinary tiers: no Legendary boxes on Floor 2, however funny that would be. Celestial isn't floor-gated but is DM-gated (above). Exception: Benefactor Boxes (§4.7) can exceed the ceiling by design.

**Story Box exception** (HOUSE; Caleb, 2026-10-04): one Legendary Story Box per table per floor (the GM may exceed it with a logged reason; Caleb can veto) is allowed on Floors 1-2, hand-picked by the GM for a single named one-time deed (recorded and announced at award time; the box is held unopened until a saferoom, §4.4 as written). Once opened, the item is ordinary loot: tradeable, lootable from a corpse and sellable (fixed System buyback by power rung; `story_value` is provenance, never credits). Its power note keeps its numbers inside the floor ceiling (§3.6); it sits outside the §4.5 pacing table and does not touch the Celestial cap. An **unopened** Story Box reclaimed on its Crawler's death (§6.2) is gone and **frees its cap slot**, so another Crawler can be awarded one (`rules/45-story-boxes-5e.md` §6.3). Full rules: `rules/45-story-boxes-5e.md`.

### 4.2 Rolling a box

For each pull, roll **d100** (the AI rolls publicly, then chooses the specific item):

| d100 | Pull type |
|-----:|-----------|
| 01–30 | **Consumable** at box rarity (or two at one rarity lower): potions, scrolls, oils, ammo, explosives |
| 31–55 | **Gear**: a magic item at box rarity (Bronze: Common item or quality mundane gear) |
| 56–70 | **Credits** (table below) |
| 71–88 | **Tailored pull**: something from the crawler's Fan Profile (§3.5): gag item, fixation, or build need |
| 89–98 | **Weird**: cursed item, joke item, sentient item, one-use System gimmick, a clue or seed |
| 99–00 | **Upgrade**: roll this pull again on the next tier up (ceiling still applies) |

**Guaranteed headline:** Gold, Platinum, Legendary, and Celestial boxes always contain one item at their rarity (Celestial: Legendary, plus its DM-designed reward); roll the remaining pulls normally.

**Semi-random on purpose.** Contents come from the table above, but the DM may **hand-pick** any pull, to help (a crawler is stuck, a build needs one thing) or to hurt (the System is trolling, the crawler earned it, the audience voted for it). Hand-picking still respects the tier's rarity, the personalization rule (§4.3), and the no-two-duds rule. Don't hand-pick quietly in the crawler's favor every time; the show needs variance.

**Credits per pull:**

| Box | Credits |
|-----|---------|
| Bronze | 3d6 × 5 |
| Silver | 2d6 × 25 |
| Gold | 2d6 × 250 |
| Platinum | 2d6 × 2,500 |
| Legendary | 2d6 × 10,000 |
| Celestial | DM's call (start from 2d6 × 10,000) |

**No floor multiplier on box credit pulls** (Lore, with Caleb's delegation, 2026-10-04): the amounts above are final on every floor. Achievement rewards and System fees keep the §3.9 credit multiplier.

**Item choice:** pick from SRD 5.2 / 2024 DMG magic items of the right rarity, then **reskin** to the floor and the crawler. Homebrew items are fine if they're priced against a comparable official item of the same rarity.

### 4.3 Personalization rule

- **At least one pull in every three boxes** a crawler opens nods to their Fan Profile (the tailored pull row helps; the AI may also convert a pull).
- **Running gags are exclusive.** The gag item lands only for its crawler.
- A tailored pull that's purely cosmetic doesn't count toward the box's value; the AI may add a small consumable to compensate if the box would otherwise be a dud *and* the crawler didn't earn a dud.
- Duds are allowed on purpose (Apology Boxes, R0-adjacent awards). Don't let two real boxes in a row be duds.

### 4.4 Opening boxes

- Boxes are stored in **System Inventory** (§5.9) as unopened tokens and **open only in a saferoom** (during a short or long rest). **No emergency opens** anywhere else; a box in the field is a box you're carrying.
- **All at once.** When a crawler opens boxes, every unopened box they hold is opened in the same session, one after another (in tier order, lowest first, for drama). You can't bank a box to cherry-pick later, or hold back the good ones.
- **Not tradeable.** Boxes are bound to the crawler who earned them and **cannot be traded, gifted, or sold between crawlers**, opened or not. Contents, once revealed, are ordinary items and can be traded.
- If a crawler dies (§6), their unopened boxes follow §6.2, not this section.

### 4.5 Box pacing (per crawler, per floor)

| Floors | Bronze | Silver | Gold | Platinum | Legendary |
|-------:|:------:|:------:|:----:|:--------:|:---------:|
| 1–2 | 2–4 | 0–1 | — | — | — |
| 3–5 | 2–3 | 1–2 | 0–1 | — | — |
| 6–9 | 1–2 | 1–2 | 1 | 0–1 (F9) | — |
| 10–14 | 1 | 1–2 | 1–2 | 0–1 | 0–1 (F13–14, campaign total ≤ 2) |
| 15–18 | 0–1 | 1 | 1–2 | 1 | 0–1 (campaign total ≤ 2) |

**Floors 1–2 achievement boxes** (Caleb, 2026-10-05): achievement boxes on Floors 1–2 are **Bronze**. Soft guideline: about 2–3 achievement Bronze boxes per Crawler per floor. The 0–1 Silver on Floors 1–2 is the Boss Box (§4.7), or a GM override for a truly great moment, with the reason logged. The one Silver box a replacement Crawler gets as late-entry compensation (§6.3) is exempt: it is not an achievement box.

**Celestial boxes are not on this table.** They are capped at **one per crawler for the whole campaign** and are DM-triggered (§4.1). Benefactor Boxes (§4.7) are extra and don't count against this table, but a sponsor shouldn't hand out more than ~1 per floor.

Story Boxes are not on this table either. **Story Box exception** (HOUSE; Caleb, 2026-10-04): one Legendary Story Box per table per floor (the GM may exceed it with a logged reason; Caleb can veto) is allowed on Floors 1-2, hand-picked by the GM for a single named one-time deed (recorded and announced at award time; the box is held unopened until a saferoom, §4.4 as written). Once opened, the item is ordinary loot: tradeable, lootable from a corpse and sellable (fixed System buyback by power rung; `story_value` is provenance, never credits). Its power note keeps its numbers inside the floor ceiling (§3.6); it sits outside the §4.5 pacing table and does not touch the Celestial cap. An **unopened** Story Box reclaimed on its Crawler's death (§6.2) is gone and **frees its cap slot**, so another Crawler can be awarded one (`rules/45-story-boxes-5e.md` §6.3). Full rules: `rules/45-story-boxes-5e.md`.

### 4.6 Attunement

**Attunement limit is 3**, as in 5e. The System will happily give you a fourth item that requires attunement and watch you choose. Spine objects that become magical (Odd Coin on F12, Faction Flag, Throne Vow tokens) **may require attunement**; that's intentional pressure. No rewards raise the cap by default (see §12).

### 4.7 Box types

Type describes the box's source and flavor. Tier math (§4.1–4.2) is the same for every type unless noted.

| Type | Source | Rules |
|------|--------|-------|
| **Boss Box** | Killing a boss or floor guardian | **Scales with boss rank:** minor boss → Silver or Gold; floor boss → Gold or Platinum; major boss (F9+) → Platinum or Legendary. One pull is usually a trophy tied to the boss. **Capped by the §3.6 floor rarity ceiling:** on Floors 1-2 (peak Uncommon) a floor boss's box is capped at **Silver** (the Floor 1 Boss Box = Silver, per `floors/floor-01-5e.md`); the Gold/Platinum ranks above apply from Floor 3 on, still subject to §3.6. |
| **Quest Box** | Completing a quest, bounty, or Mandate objective | Tier follows the quest's difficulty and floor. One pull usually relates to the quest's story. |
| **Fan Box** | Audience approval: Ratings, Crowd Pop, a crowd-pleasing stunt, or a vote | Tailored-heavy: the **tailored pull row doubles** (71–94, shrinking Weird to 95–98) and the §4.3 rule is automatically met. |
| **Benefactor Box** | **Sponsor-only.** Comes from a crawler's sponsor or Benefactor, never from the floor itself (a Sponsor Box from a §5.2 deal is a Benefactor Box) | Can contain **off-world tech and odd items** that ordinary boxes can't, ignoring the floor ceiling (§3.6): gadgets, glitchy System gear, one-offs. **Power is not tied to tier**: even a **Bronze Benefactor Box can beat a Gold ordinary box**. May carry a rider (§5.2). Glitchy, sometimes blank, sometimes too good. |
| **Story Box** | **GM-judged one-time deed**, never random and never a catalog default. Floors 1-2 allow it only as below (the Legendary tier itself is unchanged elsewhere) | HOUSE (Caleb, 2026-10-04): one Legendary Story Box per table per floor (the GM may exceed it with a logged reason; Caleb can veto) is allowed on Floors 1-2, hand-picked by the GM for a single named one-time deed (recorded and announced at award time; the box is held unopened until a saferoom, §4.4 as written). Once opened, the item is ordinary loot: tradeable, lootable from a corpse and sellable (fixed System buyback by power rung; `story_value` is provenance, never credits). Its power note keeps its numbers inside the floor ceiling (§3.6); it sits outside the §4.5 pacing table and does not touch the Celestial cap. An **unopened** Story Box reclaimed on its Crawler's death (§6.2) is gone and **frees its cap slot**, so another Crawler can be awarded one (`rules/45-story-boxes-5e.md` §6.3). Full rules: `rules/45-story-boxes-5e.md`. |

*Apology Box* (System-error compensation, usually Bronze and insulting) remains a joke variant; it's a dud by design (§4.3).

### 4.8 Naming boxes

**Boxes are named after the crawler's deed.** The announcement names the box, the box carries the name on its token, and the System reads it aloud, every time. Format: **[Tier] [Deed-based taunt] Box** (add the type if it matters: *Silver Boss Box*).

- **Low tiers get short, cheap jabs.** **High tiers get long, taunting, breathless names.** The sillier the feat, the longer the name.
- Name it after what they *did*, not just what they killed. The specific bad idea is the joke.
- Punching down is not the joke. Roast the choice, not the person; if the table isn't laughing, shorten the name.
- Stay original; invent new ones rather than recycling these. Names have no mechanical effect.

**Template list** (swap in the real deed):

| # | Tier | Name | Deed |
|--:|------|------|------|
| 1 | Bronze | **Bronze Asshole's Box** | Killed a non-combatant |
| 2 | Bronze | **Bronze Participation Trophy Box** | Showed up, technically |
| 3 | Bronze | **Bronze You Opened the Door Marked "Do Not" Box** | Opened the obviously bad door |
| 4 | Bronze | **Bronze Stabbed the Vending Machine Box** | Fought furniture |
| 5 | Bronze | **Bronze Maybe Read the Sign Next Time Box** | Ignored a clear warning |
| 6 | Bronze | **Bronze Your Mother Would Be Confused Box** | Cheerful, pointless violence |
| 7 | Silver | **Silver You Walked Into That Trap On Purpose, Didn't You Box** | Triggered a visible trap |
| 8 | Silver | **Silver Technically Alive, Spiritually Gone Box** | Survived at 1 HP |
| 9 | Silver | **Silver Bargained With a Mimic and Lost Box** | Negotiated with the unnegotiable |
| 10 | Silver | **Silver The Audience Bet Against You and Is Sulking Box** | Beat the odds |
| 11 | Silver | **Silver Brave, Loud, and Mostly Lucky Box** | Charged first, won anyway |
| 12 | Gold | **Gold You Insulted the Boss Until He Forgot to Fight Box** | Talked a boss into a mistake |
| 13 | Gold | **Gold Carried Three Teammates and Zero Dignity Box** | Won a fight dragging the party |
| 14 | Gold | **Gold Three Hundred Rats Filed a Complaint Box** | Cleared a swarm room |
| 15 | Platinum | **Platinum You Set the Whole Floor on Fire and Called It a Strategy Box** | Won through reckless destruction |
| 16 | Platinum | **Platinum We Honestly Thought That Door Was Load-Bearing, and Yet Here We Are Box** | Collapsed a structure on a boss |
| 17 | Platinum | **Platinum Nobody Asked You to Befriend the Dragon, But the Ratings Are Spectacular Box** | Befriended something huge |
| 18 | Legendary | **Legendary You Beat the Unbeatable Thing Using a Spoon, a Lie, and Pure Spite, and the Sponsors Are Still Arguing Over Whether That Counts Box** | An absurd, improvised win |
| 19 | Legendary | **Legendary The Floor Is Going to Need a Moment, and So Is Your Therapist Box** | Floor-ending feat |
| 20 | Celestial | **Celestial An Entire Production Team Stood Up and Stopped Typing, and It Has Never Happened Before, So Here Is the Box Box** | The one-per-campaign absurd feat or finale (DM's call) |

*System note:* "Box naming is automated. The System takes no responsibility for accuracy, tone, or your feelings. Please do not file a grievance about the word 'Asshole.' It is pre-approved by Legal."

---

## 5. Light overlays

These are written as 5e-style features. None of them add new core math.

### 5.1 Broadcast Name and Ratings

**Ratings (all floors, narrative).** The audience's opinion of each crawler is tracked as a tier in session state:

| Ratings tier | What it means |
|--------------|---------------|
| Unknown | Background noise. Sponsors ignore you. |
| Local | Some fans; minor sponsor attention (F3+). |
| Trending | Real sponsor offers; hunters know your face (F6+). |
| Headliner | Court and faction attention; named enemies target you. |
| Legend | Gods, Production, and the Cage care about you personally. |

Ratings move up on spectacle (wins, stunts, drama, great lines) and down on boring play, cowardice the audience didn't enjoy, or sponsor scandal. The AI moves the tier at most **one step per session**.

**Crowd Pop (homebrew trigger for Heroic Inspiration).** When a crawler does something the audience would go wild for, the AI may grant **Heroic Inspiration** (as written) with a crowd-noise toast. This is the main way Ratings touch the d20; there is **no separate Ratings currency**.

**Broadcast Name (unlocks F3).** At the rural Continuum the System mints (with the player) a Broadcast Name. Feature:

> **Broadcast Name.** Once per Long Rest, when you make a Charisma check where your fame could plausibly help, you may invoke your Broadcast Name to gain Advantage. When fame cuts the other way (hunters, rivals, a court that hates you), the AI may impose Disadvantage on one such check per Long Rest, or have you be recognized at a bad time. Ratings tier sets how far the name reaches (Local: this village; Headliner: the whole kingdom).

Spine progression: village gossip (F3) → dock posters (F6) → castle decrees (F9) → divine epithet (F12) → political object (F18).

### 5.2 Sponsors (mostly F6+)

A **Sponsor Deal** = **boon + rider**, logged in session state.

- **Boon:** a Sponsor Box, a specific item, credits, a Charm, or a recurring perk (e.g., one free Potion of Healing per floor).
- **Rider:** a must-do or must-not-do (wear our logo; never use fire; say our slogan on every kill; don't help crawler X).
- **Breaking a rider:** the boon ends (recurring perks stop; items with "sponsor-locked" tags go inert until repaired), the sponsor becomes hostile (hunter attention, sabotage, bad press: −1 Ratings step), and the System toasts it.
- **Refusing a deal** is always legal and may itself earn a toast (catalog: "Sponsorship Spit").
- Active sponsors per crawler: **max 2** (more is a rider conflict waiting to happen; the AI should make it one).

### 5.3 Mandates and Faction Flags (F9+)

- A **Mandate** is a quest with teeth from a faction: clear objective, deadline, payment, and a public consequence for refusal.
- **Faction Renown (homebrew, after the 2014 DMG renown idea):** track renown 0–5 per faction. Renown 1: safe passage / basic vendor; 3: a favor per floor (troops, info, access); 5: the faction acts on your behalf at the climax. Betraying a faction resets renown to 0 and makes enemies.
- **Faction Flag (spine object):** claiming a Flag binds you to a faction's fate. Mechanically it's a **wondrous item, requires attunement**, that grants one modest faction-flavored feature (the AI writes it to match the faction, at Rare power) and counts as a public declaration. It pays off on F15 and F18.
- Public refusal of a Mandate is allowed and may unlock alternate paths.

### 5.4 Throne Vow and pacts (F12 / F15)

A **Vow** or **Pact** is a supernatural deal with a deity (F12), infernal power (F15), or other big player.

- **Boon:** a **Blessing**-style permanent perk (2024 DMG supernatural gifts as the model), a spell granted once per Long Rest, or a significant item. Power at roughly **Rare–Very Rare** item value.
- **Drawback (always):** a binding condition (a geas-like duty, a forbidden act, a tithe), plus a stated **Invoice**: what happens when the patron collects (usually on a later floor, per the spine: F12 vows invoice on F15 and F18).
- **Breaking the vow:** lose the boon; suffer a curse the AI designs at boon-equivalent strength (e.g., a level of Exhaustion that won't clear until atoned, Disadvantage on saves vs. the patron's servants, a divine hunter). Logged as `VOW-BROKEN`.
- **Refusing** is always legal. Log it; refusals are remembered too.

### 5.5 Spine objects

Story flags first, mechanics only when needed. Track as `SEED-*` in session state.

| Object | Mechanical form | Notes |
|--------|-----------------|-------|
| **Odd Coin** (`SEED-ODDCOIN`) | F1: mundane trinket the System labels *Vendor Oddity (Unappraised)*. Can't be sold (vendors refuse or overpay suspiciously). F3/6/9: each appraisal reveals one small property. F12: may become a **wondrous item (requires attunement)** used as a divine token. | Never explain its purpose early. |
| **Benefactor Signal** (`SEED-BENEFACTOR`) | No stats. Static messages. F6: a hard choice (accepting grants a once-per-floor intervention the AI controls, plus a rider). F12/F18: allegiance consequences. | Interventions should save lives, never win fights outright. |
| **Black Box** (`SEED-BLACKBOX`, ~F10) | Object with HP/AC as 5e objects; tracked as evidence. Used on F14, F17, F18 to unlock doors, bids, or the "Burn the Feed" ending. | Losing it should be possible and painful. |
| **Faction Flag / Throne Vow** | See §5.3 / §5.4 | |
| Other seeds (Static Sigil, Guide Contract, Echo Self, Ledger Name, Jubilee Ticket, etc.) | As written in `04-floor-bible.md`; story flags unless a floor doc says otherwise | |

### 5.6 Saferooms (rest mapping)

- **Long Rest: only in saferooms.** Outside a saferoom, a Long Rest attempt is **interrupted** (5e interruption rules) by a wandering threat, or the System declares the area "not rest-certified." Floor docs may override.
- **Short Rest:** anywhere reasonably quiet (5e as written). In a saferoom a Short Rest is guaranteed uninterrupted.
- **Field-rest fee (Season Zero; HOUSE).** A field rest is a **Short Rest only** (Long Rest stays saferoom-only). A Short Rest in a spot that is already quiet is **free**. The rest-without-a-saferoom price in `rules/70` (20 credits per Crawler, cap 60 per Crawler per floor) **buys quiet** for a Short Rest where the area is not quiet (for example Floor 1 dark halls). Paying it never grants a Long Rest. A Long Rest attempt outside a saferoom is interrupted (Ceiling Ticks after 1d4 hours on Floor 1); the fee does not purchase that Long Rest. Cite: Floor 1 Day pages GM ruling; decision 031.
- **5e's one-Long-Rest-per-24-hours** limit still applies.
- **Saferoom services** (vary by floor): box opening (§4.4), achievement claims, vendors, a System terminal for appraisal (and the crafting stash, §5.9), a bulletin board, sometimes a bartender with opinions. From Floor 4, a crawler with a certified crafting table also sees a **Personal Space** door in any honest saferoom (§5.11).
- **Saferooms can lie (F2+).** Some are traps, ambush bait, or politically "safe" (Continuum docks/castle/Olympus). Searching one is allowed and smart (catalog: "Saferoom Skeptic"). A false saferoom provides no rest guarantee.
- Continuum rural saferooms (farmsteads, chapels) are usually honest.

*System note:* "This saferoom is certified 100% safe* (*certification not valid in this room)."

### 5.7 Fog of war

- The AI reveals only what crawlers can perceive, using 5e vision and light (darkvision, dim light, Perception).
- **System Map:** each crawler's map auto-fills explored areas. Unexplored areas are fog. Players don't call rooms they haven't seen.
- Map upgrades are valid rewards (R3–R5): reveal a zone, show stairwells, mark saferooms, track mobs (a "minimap ping" every 10 minutes, etc.).
- The AI logs revealed cells/zones in session state (`MAP`).

### 5.8 Floor clock (per floor doc)

Floors are timed (decision 026): a **collapse timer** (days/hours) runs on each floor, and the floor doc sets its length and any steps (Floor 1: 5 days, `floors/f01/00-overview.md` §2 rule 6; Floor 2: 10 days, house timer, decision 029). When it runs out, the floor collapses. **A Crawler who is not at a stairwell when the floor collapses is dead, on every floor, Floor 1 included. No Reprieve, no toll, no Exhaustion exception** (decisions 026 and 028; early-descent stasis counts as reaching a stairwell). **Credits and items are destroyed with the floor.** Survivors may loot a body only while the floor still stands; nothing is looted after the collapse. NPCs and the AI in stasis lose nothing. The Detour Tax is only for a missed Stairwell key, never for a missed collapse. Show the clock as a System countdown.

### 5.9 System Inventory (homebrew, default ON)

Each crawler has an extradimensional **System Inventory**:

- Capacity like a *Bag of Holding* (500 lb / 64 cubic feet); items inside weigh nothing.
- **Storing or retrieving one item** uses your free object interaction on your turn, or the **Utilize** action if you've already used it.
- Living creatures can't be stored. Unopened loot boxes take no space.
- When a crawler dies, their inventory **drops as a corpse cache** at their body (lootable by anyone, including the thing that killed them). **Exception:** a **Table Token** (a crafting table claimed but not yet in use, `rules/20-crafting-5e.md` §2.5.2) is bound, weighs nothing, and is **not lootable**; it goes back to the System or to the owner's named heir.
- **Saferoom stash.** At any honest saferoom's System terminal, a crawler may spend 1 minute (no check) to **stash** a Table Token on their account and take it back at any honest saferoom. A stashed token is out of System Inventory, so inventory theft, corpse caches and hazards aimed at System Inventory can't reach it. (Only Table Tokens; this is not general storage.)
- **Time-locked for crafting.** Items in System Inventory do not decay and never take Jolts, so a crafted explosive stored there stays as it was made (`rules/20-crafting-5e.md` §6.8).
- Normal carried gear (worn armor, wielded weapons, a backpack) uses 5e carrying rules.

### 5.10 Credits, vendors, appraisal

- **1 credit = 1 GP.** *Credits* is the display label for GP in everything a Crawler sees. Use 5e prices. Starting credits per 5e chargen. **Credits are whole numbers only** (matches `tools/state.py` and decision 028): a balance is never fractional. Copper and silver exist only as list prices on SRD gear (for reference, 1 sp = 0.1 credit, 1 cp = 0.01 credit); "credit" is singular for 1.
- **Rounding (whole credits per line).** *Buying:* a sub-credit price is charged rounded **up** to whole credits per cart line (1 Torch costs 1 credit; 10 Torches on one line also cost 1 credit). *Selling at half:* rounded **down** to whole credits per line, so an item worth under 2 credits sells for 0 unless grouped with others on one line.
- **Vendors:** buy at 5e prices ± the AI's mood; sell at half. Haggling = Charisma (Persuasion/Deception/Intimidation) vs. vendor DC (typically 12–18); success ≈ 10–25% off. Continuum vendors remember you.
- **Identifying items:** 5e as written (*Identify*, Short Rest study). System terminals and dock appraisers can identify for a fee.

### 5.11 Crafting (pointer)

**Crafting: see `rules/20-crafting-5e.md`** (tables, recipes, ingredients, explosives, the failure tables). It is an add-on module: precedence is active floor rules, then this doc, then the crafting module, then 5e 2024. Three pieces live here because they touch core systems:

- **Personal Space.** When a crawler's first crafting table is certified (Floor 4; tables are unusable before then), the System issues a basic **Personal Space**: a private extradimensional room whose door appears in any **honest** saferoom (never a false one). It fits one table and a storage nook; time inside passes normally; NPCs can't enter unless a crawler escorts them. Crafting happens only inside it or bench-free in an honest saferoom. Details: `rules/20-crafting-5e.md` §2.1.
- **Potion cooldown: 1 round.** After you drink any potion you are on **cooldown** until the start of your next turn: at most **one potion per round**. A potion drunk during the cooldown still works, but you are **Poisoned** for 1 minute (a DC 12 Constitution save at the end of each of your turns ends it). Spell scrolls and cooked meals are exempt; Hit Point Dice from rests are not potions. **Mordecai's Special Brew keeps its own, separate lockout (§6.5)**: while that is on, any other potion is wasted and the Poisoned penalty is not added on top.
- **Table Tokens and the saferoom stash.** A table is carried as a weightless, bound **Table Token** in System Inventory until it is certified, or stashed at a saferoom terminal. The exact rules are in §5.9 (corpse-cache exception and stash) and `rules/20-crafting-5e.md` §2.5.2.


---

## 6. Death, permadeath, replacements, revival

**Canon:** death is permanent. There are no respawns. The System sells many things, but a refund on a corpse is not one of them. Everything after §6.3 (revives, cursed revives) is an **optional house rule** a table switches on; every one of those costs something, because the System charges for everything. **This campaign runs Costly Revives, set to VERY COSTLY and RARE** (Caleb's decision, v0.2.3; §6.4).

**Canon facts this section is built on** (DCC Lore, `lore/catalog/revival-canon.md` v1.0; wiki and recap sources, **not** checked against the novels' text): no purchasable revival spell exists in canon, and the Dungeon never revives dead crawlers; dead crawlers become collectible cards (NR-01, NR-02). Everything that brings a dead crawler back at this table is therefore invented by us.

**Source labels (used for every revive and death-bypass source in this document).**

- **CANON**: the thing exists in Dungeon Crawler Carl as described (confidence per the lore catalog; see the caveat above).
- **CANON-INSPIRED**: our version is adapted from a canon thing and changes the numbers or reach.
- **HOUSE**: invented for this table. It has no canon basis, no matter how much it sounds like the System.

| Source | Label | Where |
|--------|:-----:|:-----:|
| Permadeath; dead crawlers become cards (Canon Hard baseline) | **CANON** | §6.0, §6.2 |
| Costly Revives (mode), Soft Open (mode), Floor 1 Reprieve | **HOUSE** | §6.0, §6.2 |
| Revival Voucher | **HOUSE** | §6.4.2 |
| *Revivify* / *Raise Dead* / *Resurrection* / *True Resurrection* availability, gating and Fees (the 5e spells are 5e; no canon revival spell is purchasable) | **HOUSE** | §6.4.2-6.4.4 |
| System Rare Offer; Back by Popular Demand; Benefactor / floor-rule revive routes | **HOUSE** | §6.4.2 |
| Marked for Death ring (cheaper revive route) | **HOUSE** | §6.7 |
| Cockroach (Donut's skill): survive a fatal hit | **CANON** (death-cheat, not a revive) | §6.4.6 |
| Mordecai's Special Brew: 30 seconds of near-immortality | **CANON** (death-cheat, not a revive) | §6.4.6, §6.5 |
| Half-Splat Potion: falling damage only | **CANON** (falling-only) | §6.5 |
| Dolores Doesn't Splat: falling at speed only | **CANON** (falling-only) | §6.5 |
| Cockroach Clause (our feature); *Second Season* Charm | **CANON-INSPIRED** | §6.5, App. B |
| Lifesaver Draught | **HOUSE** | §6.5 |
| Benefactor Signal intervention that saves a life | **HOUSE** | §5.5 |
| Canon true revivals: Tummy Acher pets, Nodlings, mercenaries, Growler Gary, Grimaldi's crew, Mrs. Ghazi, gods, extracted admins and tourists | **CANON** (species/situation-specific story events) | §6.4.7 |
| *Second Chance* (timed undead minion), *9 Lives* (halve damage) | **CANON**, but **not** revives | §6.4.7 |
| Dead Crawler Card gag (trophy; no revival) | **CANON-INSPIRED** | §6.9 |


### 6.0 Death table options at a glance

Pick one **Death Mode** before Floor 1 begins (the table decides it up front so nobody argues mid-death) and log it in session state as `DEATH-MODE`. The AI never changes it mid-campaign without the table agreeing.

**`DEATH-MODE` default for this campaign: `Costly Revives (VERY COSTLY, RARE)`** (decided by Caleb, v0.2.3). **The table has already picked it:** `DEATH-MODE=Costly Revives` and `COMFORT=Ludicrous` are logged as the campaign defaults (Caleb, 2026-10-03; shared record `decisions/002-death-mode.md`), so intake confirms them rather than holding a new vote. Canon Hard and Soft Open stay fully documented below as alternatives; a table that wants one of them logs it instead, and the AI uses that mode's row and §6.8 line. Canon Hard is still the canon baseline (death is permanent).

| Mode | Death is... | Revival | Replacement | Best for |
|------|-------------|---------|-------------|----------|
| **Canon Hard** (alternative; **CANON**) | Permanent. Dead is dead. | None. Revival spells and scrolls are voided (§6.4). | Yes (§6.3) | The intended experience; tables that want every choice to weigh something |
| **Costly Revives** (**campaign default: VERY COSTLY and RARE**; **HOUSE**) | Permanent *unless* the party has a Voucher or Rare Offer and survives the gates and the price. | **Rare:** at most 1 per party per 3 floors, 3 per campaign, once per crawler; Voucher/Rare Offer only, never bought (§6.4.1–6.4.2). Every revival pays a big Fee **and two** menu picks, then suffers Revival Sickness (§6.4.4–6.4.5). Optional cursed route (§6.7). Canon-verified exceptions are pre-approved (§6.4.6). | Yes, and the **usual** outcome | Tables that want a real chance at a comeback that still costs a fortune and leaves a scar |
| **Soft Open** (**HOUSE**) | Not final. Pulled off-screen, back at the next saferoom, with penalties (§6.2). | Not needed. | Rarely needed | New-to-5e tables, one-shots, kids' tables |

Independent toggles, usable in any mode:

- **Near-death buffers** (§6.5): DM-granted only. Never a default feature of any class.
- **Stairwell Checkpoint** (§6.6): **ON** in every mode.
- **Floor 1 Reprieve** (§6.2): **ON by default for Season Zero, Floor 1 only** (Caleb, 2026-10-04); a table may turn it off at session zero. It never applies to a death from a missed floor collapse.

### 6.1 Dying

The base game is **5e 2024 as written**: **Death Saving Throws** (DC 10; three successes stabilize, three failures kill; natural 20 and natural 1 as written), **Stabilize** via Medicine or healing, **massive damage**, and instant death rules all apply unchanged. The AI announces every death save result publicly; the System is not above commentary (§6.9).

**Telegraph lethality.** Before an attack on a downed crawler, or a "you will probably die" choice, the AI makes the danger clear in fiction. No PC dies without a clear rule trigger or stakes the player understood (Game Brief hard limit).

**No quiet deaths.** When a crawler dies, the AI states it plainly, posts the System's death toast (§6.9), and then resolves the aftermath in this order: (1) the corpse cache drops (§5.9); (2) unopened boxes are handled per §6.2; (3) the table decides what happens next according to the Death Mode, while the System may run the **Dead Crawler Card** pitch (§6.9).

### 6.2 Permadeath toggle

- **Default: ON** (in **Canon Hard** and in **Costly Revives**, where a revival is a rare, costly exception). A crawler who fails their third death save, or dies outright from massive damage or a "you die" effect, is **dead for good.** No respawn. No "the System giggles and restarts you." The only ways back are the optional house rules in §6.4 and §6.7 (the campaign default, Costly Revives, has them switched on, under the Rarity Limits in §6.4.1).
- **Unopened boxes (all modes).** On death, the crawler's unopened loot boxes are **reclaimed by the System** and vanish (boxes are bound to the crawler and can't be traded; §4.4). Their System Inventory drops as a corpse cache (§5.9); that cache is ordinary loot and the party may take it. An unopened **Story Box** is reclaimed the same way, and its Story Box cap slot is freed so another Crawler can be awarded one (`rules/45-story-boxes-5e.md` §6.3); an opened Story Box item is ordinary loot and stays lootable and not bound.
- **Table option [HOUSE]: OFF ("Soft Open," also called "Syndicated" mode).** On death the crawler is pulled off-screen and returns at the next saferoom with one level of **Exhaustion** that can't be removed until descent, **loses all unopened boxes**, drops their System Inventory where they fell, and takes a −1 Ratings step. Death still matters; it just isn't final. (Not related to Floor 2, "Soft Open." The System reuses names. It's cheaper.)
- **Floor 1 Reprieve [HOUSE] (Tutorial Mercy; ON by default for Season Zero Floor 1; tables may turn it off; Caleb 2026-10-04).** Once per crawler, **on Floor 1 only**, a death becomes "unconscious, ejected to the nearest saferoom at 1 HP" with a humiliating Title. Floor 1 only means it is gone once the crawler descends. **It never applies to a death from a missed floor collapse** (next bullet; decisions 026, 028, 029). Log `F1-REPRIEVE: ON/OFF`. The System still posts a toast (§6.9).
- **Missed floor collapse [HOUSE, canon-shaped, tagged *inspired*] (Caleb, 2026-10-04; `decisions/028-collapse-death-loot.md`).** Death on every floor, no Reprieve. The final collapse is at a fixed 24 in-game hours into the last day (Floor 1: Day 5); the GM keeps a running floor-hour count (hours since floor start, hours into the current day) in the carry-on tracker. A dead Crawler's credits and items are destroyed with the floor; survivors may loot the body only while the floor still stands, and nothing is looted after the collapse. Story Box and Legendary items are lootable until then, then gone. The ledger logs a "floor lost" write-off (integer coins). NPCs and the AI in stasis lose nothing.

### 6.3 Replacement crawlers

- A new crawler joins at the **next saferoom** (or a natural fictional entry: late intake, Continuum recruit, sponsor-placed entrant, mirror-born duplicate on F16, etc.).
- **Level:** the party's **lowest current level** (standard track: the floor band).
- **Gear:** 5e starting equipment for their level per the 2024 DMG "starting at higher level" guidance, plus magic items: **one Common per prior floor** (max 4) and **one Uncommon per three floors** passed; nothing above the floor's *default* rarity. One **Silver box** as "late-entry compensation."
- **No achievements carry over**; the new crawler gets a fresh Fan Profile.
- The dead crawler's player keeps nothing mechanical, but the System **may** let a dead crawler's running gag haunt the party (the plushies keep showing up, addressed to a dead person).
- **In Canon Hard, this is the only way back to the table.** In Costly Revives (the campaign default), revival is rare, so a replacement is the **expected** outcome; it is the fallback whenever the party has no Voucher or Rare Offer, hits a cap or cooldown (§6.4.1), or can't (or won't) pay. If the original crawler is revived later, the player picks which crawler to keep; the other becomes an NPC ally of the party, or retires with a toast.
- **Player with several Crawlers (v0.2.9):** the replacement may be one of that player's benched Crawlers, swapped in only at session zero or between sessions (never while a session is open, not even in a safe room); level and gear follow this section and §2.3 Catch-up as written. Rules: `characters/create-flow-spec-5e.md` §8, `decisions/020-multiple-crawlers-active-swap.md`.

### 6.4 Revival (house rule: Costly Revives, VERY COSTLY and RARE)

**Labels:** §6.4.1-6.4.5 and §6.7 are **HOUSE**. §6.4.6 (canon death-cheats) and §6.4.7 (canon true revivals) are **CANON**. Canon says there is no purchasable revival spell and the Dungeon never revives dead crawlers; everything below that does is ours.

**Canon Hard: no revival [CANON baseline].** The 5e revival spells (*Revivify*, *Raise Dead*, *Resurrection*, *True Resurrection*, and equivalents such as *Wish* used to restore the dead) **fail** when cast on a dead crawler. The System's text: "Customer is deceased. Refund eligibility: none." They are still real spells (they work on NPCs and monsters per the AI's story needs) but a crawler's soul is not returnable. The AI should tell a cleric player at intake that their revival spells will be dead weight, and may swap them for a spell the table agrees on.

**Costly Revives (this campaign's chosen mode, per Caleb's v0.2.3 decision): the System "refunds" a death, rarely, and bills brutally for it.** Revival is never automatic, never free, never purchasable, and never available on demand just because a player asks. Every revival (except a Canon-verified exception, §6.4.6) must clear **all** of these gates: the **Rarity Limits** (§6.4.1), a **Revival Voucher** or a **System Rare Offer** (§6.4.2), the **floor gate** (§6.4.3), and then pays the **Invoice** (§6.4.4: a big Fee *and* two menu picks) and takes **Revival Sickness** (§6.4.5). If the AI is unsure whether a route is open, it is closed.

**Session state to log:** `REVIVALS-USED: <n>/3` and `LAST-REVIVAL-FLOOR: <F# or none>` per party; `REVIVED-CRAWLERS: <names>`.

#### 6.4.1 Rarity Limits (the numbers) [HOUSE]

| Limit | Value |
|-------|-------|
| **Cooldown** | At most **1 revival per party per 3 floors**. After a revival on Floor N, no further revival (any route) until the party has descended to **Floor N+3** or deeper. |
| **Campaign cap** | At most **3 revivals per party for the whole campaign**. After the third, Costly Revives behaves as Canon Hard for revival (replacements only). |
| **Per-crawler cap** | A crawler can be revived **once, ever**. Dying again is final. |
| **Vouchers held** | A party may hold **at most 1** unspent Revival Voucher at a time. |
| **Rare Offers** | At most **1 System Rare Offer per party per 6 floors** (§6.4.2). |

Every route in this section counts against the cooldown and the campaign cap, including *Back by Popular Demand*, Benefactor deals, and floor-doc revival gimmicks (a floor doc may change *how* a revival is paid, but only a line that says "overrides §6.4.1" may waive these limits). **Exempt:** Canon-verified exceptions (§6.4.6), which the DM has pre-approved regardless of these limits. The §6.7 ring route counts like any other revival.

#### 6.4.2 Sources: no shopping for resurrections [HOUSE]

- **Revival spells, scrolls, and items are not purchasable [HOUSE].** (Canon has no purchasable revival spell either; the *Revivify* / *Raise Dead* / *Resurrection* / *True Resurrection* gating below is our invention on top of the 5e spells.) No vendor, terminal, or saferoom shop stocks them. They cannot be crafted, copied into a spellbook, learned at level-up, or prepared from a class list; for Costly Revives tables the System withholds them ("not in your plan"). A 5e revival spell found loose (a scroll, a spell on a corpse, a *Wish*) fails like Canon Hard unless it is a Voucher.
- **Revival Voucher [HOUSE]** (consumable; authorizes **one** revival of a named spell tier: Quick / Standard / Full / Platinum Refund). Anyone can use it (no slot, no spell list, no caster needed; it supplies the spell's components). Vouchers appear **only** as:
  1. a **boss reward** (a floor boss or a named elite; the AI's call, never a random pull),
  2. a **quest reward** (a completed Quest with a death-flavored or high-stakes hook),
  3. a **Benefactor Box** or other Benefactor/sponsor gift (§4.7), or
  4. the System's own **Rare Offer** (below).
  Vouchers never come from the ordinary item roll (reroll if one comes up), cannot be bought or sold, and can be stolen or lost like any item. A Voucher is an **opportunity**, not a pass: the Invoice below is still due.
- **System Rare Offer [HOUSE].** When a crawler dies and no Voucher is in hand, the AI **may** (never must) have the terminal offer a one-time revival at the next saferoom, only if the party is on **Floor 5 or deeper** (the earliest gate), the cooldown and caps allow it, and the body (or enough of it) is present. Price: **Fee 3,000 credits × the floor number**, plus two picks at **Heavy** weight (§6.4.4). It ignores the spell time windows and spell-level gates beyond Floor 5, but not the cooldown or caps.
- **Other routes [HOUSE]** (each requires the Fee and two picks too, and each counts against §6.4.1):

| Other route | Requirement | Cost |
|-------------|-------------|------|
| **Back by Popular Demand** | Crawler was at Headliner/Legend Ratings, or the table loves them; AI's call. Once per campaign per party. | Fee 2,000 credits × floor number. The permanent "fan vote" rider counts as **one** of the two picks; the other is a normal Heavy pick. Revives at the next saferoom. |
| **Benefactor / sponsor / patron** | Active deal or vow | Delivered as a Voucher. The Benefactor's price (a big rider or an Invoice moved up) counts as **one** of the two picks; Fee as for the spell tier. Logged as spine. |
| **Floor rules** | Per floor doc (e.g., F8 echoes, F16 mirrors) | Per floor doc, plus the Fee, two picks, and Sickness unless the doc says otherwise. |

The old "saferoom revival service" is **retired**; the Rare Offer replaces it.

#### 6.4.3 Floor gating (retained) [HOUSE]

The System's "refund desk" opens when the **standard track first brings the party to the character level that can cast that spell** (§2.2 arrive levels after decision **033**; no longer "arrive Floor N at level N"). It applies to Vouchers and every other route: a *Revivify* Voucher found early is "not yet in warranty" and does nothing (it may be held).

| Spell tier (as written) | System "refund" label | Earliest floor (std track) | Fee (credits, flat) | Pick weight (two picks) |
|--------------------------|-----------------------|:--------------------------:|:-------------------:|:-----------------------:|
| *Revivify* (3rd level; within 1 minute of death; returns at 1 HP) | Quick Refund | **4** (arrive level 5) | **5,000** | **Standard** (one step above Light) |
| *Raise Dead* (5th; within 10 days; the d20 penalty as written) | Standard Refund | **8** (arrive level 9) | **15,000** | **Heavy** |
| *Resurrection* (7th; within a century) | Full Refund | **11** (arrive level 13) | **40,000** | **Heavy** |
| *True Resurrection* (9th) | Platinum Refund | **15** (arrive level 17) | **100,000** | **Heavy**, plus the AI adds one story consequence |

*Label: **HOUSE**: the floor gates, the spell-tier "refund" labels, and the Fees are invented; no canon revival spell is sold.* The 5e time windows and spell penalties apply as written. The Fee is **flat credits** (not multiplied by the §3.9 floor multiplier) and includes the spell's material components. Floor docs may move a gate (a floor with a "no refunds" rule). Always check the active floor doc first.

#### 6.4.4 The Invoice: a Fee AND two picks [HOUSE]

Every revival carries **three** parts, all mandatory:

1. **Resurrection Licensing Fee** (the credits in the table above, or the route's own fee): paid at the next saferoom terminal. Unpaid = debt (catalog: "Debt Notice"); the System collects later, with interest, at the worst time. The crawler stays dead until the Fee is at least **half paid** up front; the rest is debt due by the next floor transition.
2. **TWO picks from the Costly Revive Menu** (below), both at the **pick weight** in the table above (one step heavier than the old scale; Heavy is the ceiling). The picks must be **two different menu entries**, and at most **one** may be the Celestial Tax. The AI picks entries that fit the death, or offers **two options for each pick** and lets the player choose. The party can't buy their way out of a pick with credits unless the entry is the Celestial Tax.
3. **Revival Sickness** (§6.4.5).

**Costly Revive Menu**

| # | Cost | Light | Standard | Heavy |
|:-:|------|-------|----------|-------|
| 1 | **Celestial Tax** (paperwork and Syndicate cut; the System complains the whole time) | 50 credits × the floor credit multiplier (§3.9) | 150 × multiplier | 400 × multiplier |
| 2 | **Permanent loss** (the System "withholds" part of you) | Hit point maximum reduced by your level | One ability score −1 (not below 6), or hit point maximum reduced by 2 × your level | One ability score −2 (not below 6), or two scores −1 each, or hit point maximum reduced by 3 × your level |
| 3 | **Sponsor debt** (a sponsor or Production fronts the cost and wants it back) | A Sponsor Deal rider (§5.2) | A **Mandate** (§5.3) on the next floor with a public consequence for refusal | A mandate **and** a rider; an Invoice (§5.4) coming due in 1–3 floors |
| 4 | **Forfeit** (box or item) | One unopened box (the DM picks the lowest-tier one) or one Charm | The highest-tier unopened box, **or** one attuned item shattered | All unopened boxes **and** one attuned item shattered |
| 5 | **Vow** (the System writes the terms; you signed by dying) | A one-floor restriction (e.g., never decline a fight on camera) | A **Vow** with a stated Invoice (§5.4) | A **Throne Vow-class pact** (§5.4): geas-like duty, forbidden act, or tithe |

Notes on the menu:

- **Permanent** means permanent. It can be restored only by a **Wish**, an **Epic Boon**, or an R6 Headliner reward (§3.4) the AI grants for that purpose.
- If the party has no box, no attuned item, or no sponsor available for a menu entry, that entry is simply unavailable; the AI offers a different one.
- A revival never takes a crawler below hit point maximum 1. If the cost would, the AI converts the remainder into a Vow (#5).
- **Stacking:** the per-crawler cap (§6.4.1) means one revival per crawler, so the two picks come from one invoice. The AI should say out loud how fragile that crawler is becoming.
- The Early Termination Fee in §6.7 is a one-off charge, not a revival Invoice.

#### 6.4.5 Revival Sickness (lingering penalty) [HOUSE]

A revived crawler is **Revival-Sick** until the **next saferoom Long Rest on the next floor**: they must (a) descend to a floor deeper than the one they were revived on, **and then** (b) finish a Long Rest in a saferoom there. A Long Rest on the same floor, any number of Long Rests in the field or elsewhere, and the Stairwell Checkpoint (§6.6) do **not** end it.

- The crawler gains **2 levels of Exhaustion** (5e 2024) that **cannot be reduced or removed by any means** (*Greater Restoration*, potions, Charms, rests) until the condition above is met; when it ends, both levels clear.
- They return with the hit points the spell gives (*Revivify* and *Raise Dead*: 1 HP), and **can't gain Heroic Inspiration** while sick.
- The System **gloats**, every time: a gloating revival toast (§6.9) at the Invoice, and a second jab when the Sickness is cured.

Revived crawlers keep their achievements and Fan Profile.

#### 6.4.6 Canon-verified revival exceptions [CANON]

**Rule:** anything **verified in Dungeon Crawler Carl canon** as a revive or death-cheat is **pre-approved by the DM regardless of the rarity limits** above (no Voucher, no cap count, no cooldown). They still must be **earned or granted** (DM-granted boons, rewards, training), they are limited by their own text, and they are not purchasable on demand. Source: `lore/CANON-LEDGER.md` (DCC Lore, v1.0, 2026-10-03). Entries below are those tagged **VERIFIED** that are revives or death-cheats. Caveat from the ledger itself: "VERIFIED" is a bookkeeping label (a wiki chapter cite or two agreeing sources), **not** checked against the novels' text.

| Ledger ID | Exception | Ledger tag | What it does (canon) | Table mapping |
|-----------|-----------|------------|----------------------|---------------|
| M-009 / S-001 | **Cockroach** (Donut's skill) **[CANON]** | VERIFIED (page cite B2 ch2) | Survive a lethal hit once a fight; L5 one survived lethal hit, near death after; L10 the first fatal strike costs no health. Trains by use, potions, or a training guild, and it's expensive. | **Cockroach Clause** (§6.5), DM-granted. |
| I-018 | **Mordecai's Special Brew** **[CANON]** | Ledger: VERIFIED (page cite B3 ch7). Mechanics detail: **WIKI-ONLY** per DCC Lore | A 30-second immortality-style potion (Gold Standard Healing Potion + Troll's Second Wind): constant healing plus rapid regeneration for 30 seconds; heals almost anything but does **not** stop instant kills (blown up, decapitated, *Power Word Kill*, *Disintegrate*). Canon cost: potion sickness for ~10 hours (no other potions), and a crawler can benefit from only **two** Brews total before it stops working. Crafted on a level 3 Alchemy Table (Book 3). Canon scene: Carl survived being stomped by a Floor 4 (Trainyard) god-like Grull piloted by the Maestro. (The ledger quote is only the item name; the effect comes from the item's infobox and DCC Lore's mapping.) | **Mordecai's Special Brew** (§6.5), DM-granted, limited, expensive. Pre-approved as a canon-verified **bypass** (it is **not** a revive and does not count against the §6.4.1 revive limits). |

**Revives of ordinary crawlers: none.** No canon source revives an ordinary dead crawler (canon: the Dungeon never does; dead crawlers become cards). The species- and situation-specific canon revivals are in **§6.4.7** and are story beats, not crawler options. Canon **falling-only** cheats (Half-Splat, Dolores Doesn't Splat) are in §6.5 and follow the normal limits. **Not revives (CANON, excluded):** *Second Chance* (P-003; a timed undead minion) and *9 Lives* (S-010; halves damage); M-043 confirms canon "zero health means permanent death."

- **TODO (pending DCC Lore):** when the ledger gains a VERIFIED revive or death-cheat that works on ordinary crawlers (a Revive item, a "second life" achievement), add a row here with its ledger ID and quote. Recheck `CANON-LEDGER.md` §9 (append log) before each session.
- Items tagged WIKI-ONLY or UNVERIFIED are **not** pre-approved; they follow the normal limits.

#### 6.4.7 Canon true revivals (species/situation-specific story events) [CANON]

Dungeon Crawler Carl does contain true returns from death, but each is tied to a species, a contract, or a one-off situation. **The DM uses these rarely, as story beats**, never as a menu a player can order from. All are **CANON** (source: `revival-canon.md` v1.0, rows RV-01 to RV-16; confidence per that file; Book 6-8 spoilers, so **DM-only** until the party meets them). They are paraphrased, not quoted.

| Source | What happens in canon | Table use |
|--------|-----------------------|-----------|
| **Tummy Acher pets** (RV-01 to RV-03) | A pet of this species that dies regenerates from its own body, as long as the body survives and it had reached level 5. Each return gives **+25% to all stats** and a **new random weakness** (some are lethal triggers). Every **5th** death resets the pet to level 1 with memory loss. | Only for a Tummy Acher pet. Return at once or at the next rest (DM's call); log deaths per pet, apply +25% and a new weakness each time, reset on the 5th. A body destroyed or a pet below level 5 stays dead. |
| **Nodlings** (RV-04) | A Nodling who takes a fatal hit does not die; the shared body splits into two weaker Nodling yearlings. | Once per Nodling; the DM sets the new levels. The split is the crawler's "extra life" and a big story change, not a heal. |
| **Mercenaries** (RV-05) | Hired mercenaries from one particular deal regenerate on the **next floor** if killed. Canon limits it to floors 6, 7 and 8. | For NPC hirelings on a matching contract only, floors 6-8. They return when the party reaches the following floor, not on the spot. |
| **Growler Gary** (RV-08) | An indestructible NPC who holds a plot-critical item comes back when killed; he cannot leave his bar. | For key-holder NPCs the story needs. Not for crawlers or ordinary NPCs. |
| **Grimaldi's circus crew** (RV-09) | Crew bound to Grimaldi (a vine) return to the vine and are reborn the next day. | Only for crew bound to him; they return the next day. |
| **Mrs. Ghazi** (RV-10) | The sand creature re-forms from a single grain while Samantha exists; fire, cold and lightning only suppress her for a while. | A recurring-monster beat. Killing her for good needs the story condition (Samantha) to change. |
| **Gods** (RV-11, RV-12) | A Celestial Thorn Room holds seven broken shrines and one Sun of Reawakening; whichever shrine is repaired, that god is restored, and the other six gods turn hostile as bosses. | A one-time, mutually exclusive choice for a god-level story; never a crawler revive. |
| **Admins and teleport tourists** (RV-16) | The AI teleports protected people (tourists, Dungeon admins) out before they die. | NPC extraction only. Crawlers, guild masters and ordinary NPCs are **not** covered. |

**Rules for the DM**

- These are story events: a player cannot buy, craft, or learn any of them, and a crawler cannot gain one except through the situation itself (for example, owning a Tummy Acher pet).
- They **do not** count against the §6.4.1 limits and need no Voucher, Fee or Sickness; the situation's own limits above apply.
- If a campaign element would let an ordinary crawler return, it is not this subsection: it is **HOUSE** and runs under §6.4.1-6.4.5.
- **Not revives (CANON, listed so nobody mistakes them):** *Second Chance* (Donut's spell) raises a lower-level monster as a **timed undead minion**, and *9 Lives* **halves** damage from the first nine physical attacks each day. Neither returns anyone from death.

### 6.5 Near-death buffers (DM-granted)

These are optional safety nets for tables that want a longer leash than death saves alone. **The AI only grants them as rewards or through limited, earned routes** (a box, an achievement, a Sponsor boon, a floor reward, a trainer or crafter NPC); **no one has them by default**. They work on any Death Mode. **None of them is a revival**: they stop a death from happening; they never bring back a crawler who is dead. Each entry below carries its label: **CANON**, **CANON-INSPIRED**, or **HOUSE** (see the key at the top of §6).

**Common rules for all buffers**

- A buffer triggers **once per fatal blow**. If several would apply, the crawler chooses one; the others don't spend a use.
- A buffer applies when an attack or effect would reduce you to **0 HP** or would kill you outright through **massive damage**. It does **not** stop effects that kill without dealing damage (e.g., *Power Word Kill*, a *Disintegrate* dust result) unless its text says so; it does not rewrite a failed death save.
- A buffer cancels the **death**, not the effects of the attack other than damage (the poison, the grapple, and the prone condition still apply).
- The AI **announces** the trigger in fiction and with a System toast. No hidden buffers.

**Cockroach Clause** [**CANON-INSPIRED**] (feature; R4 at tier 1, R6 at tier 2; a Blessing-style perk). *Donut's Cockroach skill itself is a **CANON** death-cheat (§6.4.6); this feature is our adaptation of it, with house tiers and training prices. Canon basis: Donut's **Cockroach** skill (CANON-LEDGER M-009 / S-001, **VERIFIED**, page cite B2 ch2). In canon, at skill level 5 you are guaranteed one survived lethal hit per fight, though you're near death after; at level 10 the first fatal strike costs no health. The skill trains only by use, potions, or a training guild, and that is expensive.*

> **Cockroach Clause, Tier 1** (canon L5). Once per combat (or, outside combat, once per Short Rest), when a hit or effect would reduce you to 0 hit points or kill you outright from massive damage, you drop to **1 hit point** instead.
>
> **Cockroach Clause, Tier 2** (canon L10). As Tier 1, but the **first** time in each combat (or each Short Rest outside combat) that a hit or effect would reduce you to 0 HP or kill you outright, you take **no damage from it** and stay at your current HP. If a second fatal blow lands in the same combat, Tier 1 applies to that one, but only once per Long Rest (house addition).

*How a crawler gets it (house adaptation of canon):* DM-granted as a reward, **or** trained. Training routes: (a) **use**: each time the Clause fires counts as one use; after **5 uses**, Tier 1 may be upgraded to Tier 2 by the AI; (b) **potions**: a Cockroach-training potion (R5, DM-placed); (c) a **training guild** NPC the AI places, charging **3,000 credits for Tier 1** and **10,000 credits for Tier 2**. The AI should attach the System's price in fiction (a Tier 2 Cockroach comes with a Sponsor rider, or the crawler's Ratings tier takes the joke: "Roach"). Both tiers are permanent features, not Charms; they are not lost at descent.

**Half-Splat Potion** [**CANON**, falling-only] (consumable; Uncommon; ~150 credits where sold; R3). *Canon: the wiki says it "prevents you from dying from falling damage but leaves you at 5% health" (ledger v1.0 tag **WIKI-ONLY**; `revival-canon.md` RV-36/37 lists it VERIFIED on a Health-page cite, B5 ch46). It is **not** a general death-cheat. The hour window, price and rarity below are table adaptations.*

> As a Bonus Action, drink it. For the next **hour**, the first time **falling damage** would reduce you to 0 HP or kill you outright, the fall is **cancelled** for the purpose of death and you instead have hit points equal to **5% of your hit point maximum (rounded up, minimum 1)**. The potion is then used up. It does **nothing** against any other damage or effect. If no fatal fall happens within the hour, the potion is wasted. You can have only one active at a time.

*Table note:* the hour-long window and the price are table adaptations; the canon effect is falling damage only. Drinking it as a Reaction is allowed **only** if it is already in your hand or on a bandolier, at the AI's discretion. The default is Bonus Action, primed in advance, so players decide before the fall.

**Dolores Doesn't Splat** [**CANON**, falling-only] (consumable; Rare; R4; DM-placed). *Canon: Mordecai-brewed fall potions used in Book 4 (RV-34, ledger M-065; the batch name comes from a web chapter summary, so treat the name as WEB-sourced). Drunk in freefall at about 200 km/h or faster, the drinker is invulnerable for a moment, the landing surface gives way, and they bounce about five times; the pain remains. It is **not** a general death-cheat.*

> As a Bonus Action, drink it **while falling** (or primed beforehand per the Half-Splat note). The **next landing** from a fall of at least **300 feet** deals **no damage** to you; you bounce and the AI narrates the pain. It does nothing against any other damage, and no fatal blow of any other kind is cancelled. The potion is used up. Do not stack with Half-Splat on the same fall: the AI uses the better one.

*Table note:* the 300-foot floor and the no-damage mapping are table adaptations of canon's 200 km/h trigger; the effect stays falling-only. DM-granted, never on a vendor shelf.

**Lifesaver Draught** [**HOUSE**] (consumable; Rare; **not canon**; R4). *A Mordecai-style crafter-NPC potion that fills the gap Half-Splat leaves. It is limited, expensive, and DM-granted only.*

> As a Bonus Action, drink it. For the next **hour**, the first time **any** hit or effect that deals damage would reduce you to 0 HP or kill you outright through massive damage, the blow is **cancelled** and you instead have hit points equal to **5% of your hit point maximum (rounded up, minimum 1)**. The draught is then used up. It does not stop effects that kill without dealing damage (see the common rules), and it does nothing for a crawler who is already dead.

- **Source:** brewed **only** by a crafter NPC (the Mordecai role) whom the AI places, and only after a brewing hook is satisfied (a rare ingredient from a boss or quest). **Never** on a vendor shelf, a standard terminal, or the ordinary box item roll.
- **Price:** **2,500 credits** from the crafter, plus the ingredient.
- **Limits:** a crafter brews **at most 1 Lifesaver per floor**; a crawler may carry **at most 1**; a crawler benefits **at most once per floor** (a second draught the same floor does nothing); one hour only; the DM decides whether a floor allows it at all.
- **Does not count** as a revival and doesn't touch the §6.4.1 limits. It is also **not** a Canon-verified exception (§6.4.6).

**Mordecai's Special Brew** [**CANON**] (consumable; Very Rare; R5; **canon-verified bypass, pre-approved**; §6.4.6). *Canon: a 30-second immortality-style potion (ledger I-018; Gold Standard Healing Potion + Troll's Second Wind; level 3 Alchemy Table, Book 3). Constant healing plus rapid regeneration for 30 seconds heals almost anything but does not stop instant kills. Potion sickness lasts ~10 hours, and a crawler can benefit from only two Brews total. Tag: ledger **VERIFIED** (B3 ch7) for the item; the mechanics detail is **WIKI-ONLY** per DCC Lore. Canon scene: Carl survived being stomped by a Floor 4 (Trainyard) god-like Grull piloted by the Maestro.*

> As a Bonus Action, drink it. For **5 rounds** (~30 seconds), you gain **regeneration**: at the **start of each of your turns** you regain hit points (**Tier 1, levels 1-4: 10; Tier 2, levels 5-10: 20; Tier 3, levels 11-16: 30; Tier 4, levels 17+: 40**), and **damage alone cannot reduce you to 0 hit points** (you stay at 1 HP at minimum; massive-damage death from ordinary damage does not apply). It has **no effect against instant death**: *Power Word Kill*, a *Disintegrate* dust result, decapitation or other "your head is no longer attached" outcomes the AI declares, being blown to pieces by an explosion that destroys the body, and anything else that kills without needing hit points to reach 0. When the 5 rounds end, you are sick (below).

- **Potion sickness (the lockout):** after drinking, you **cannot take any other potion** (healing, buff, or another Brew; Hit Point Dice from rests are unaffected) until **10 hours** pass or you finish a **Long Rest**, whichever comes first. Attempting a second potion wastes it; the System announces the failure and bills for it. This lockout is **separate from** the general 1-round potion cooldown (§5.11); it wins while it lasts, and the cooldown's Poisoned penalty is not added on top.
- **Max two per character, for the whole campaign.** A crawler who has benefited from two Brews gains nothing from a third (the potion "stops working"); track `BREW-USED: n/2` on the sheet. Carrying a spare for someone else is fine; the cap is per drinker.
- **Source:** DM-granted only. Brewed by a crafter NPC (the Mordecai role) on a **level 3 Alchemy Table**, which canon first shows in Book 3, so the default is **Floor 4 or later** (the AI may place it earlier as a special reward). The two ingredients (a Gold Standard Healing Potion and a Troll's Second Wind) must be supplied. **Never** on a vendor shelf or the ordinary box item roll.
- **Price (table adaptation):** **5,000 credits** from the crafter plus both ingredients. A crafter brews at most **1 per floor**; a crawler carries at most **1**.
- **Does not count** as a revival and doesn't touch the §6.4.1 limits; it is a bypass under §6.4.6. It follows the common buffer rules above where they don't conflict (announced with a toast; it cancels the death, not other effects of the attack).
- *System snark:* "Immortality: now in a convenient 30-second serving size. Side effects include the next ten hours of not being allowed to have anything else."

**Existing buffers.** The *Second Season* Charm (Appendix B; [**CANON-INSPIRED**]) is a one-shot Cockroach Tier 1 and follows the common rules above. The Benefactor Signal (§5.5; [**HOUSE**] when it saves a life) intervenes outside this system.

#### 6.5.1 System skills level by use (decision 037)

[**CANON-INSPIRED**; pace is **HOUSE**] System skills (the crafting skills in `rules/20-crafting-5e.md` §3, the Cockroach Clause, and any other System skill a Crawler gains) rise **one rank at a time**.

- **Where ranks come from (canon, ledger v1.20):** meaningful use, especially hard or clever use (M-059, M-807). A first-time feat can grant a new skill at rank 1 or higher (K-070, K-057). Inventive crafting can raise several skills at once (K-079, K-064). A Skill Potion gives +1 (M-045); a Cheat Code Potion gives +3 to a random skill (I-011). Training guilds (M-059). Some classes and species give flat bonuses or faster progression (K-071).
- **Cap:** rank **15** (M-008), or **20** for a species' or class's own skill family, e.g. Hobgoblin traps and explosives (K-078). Going past 15 through real fights is the very rare achievement A-143.
- **House pace:** no use counters, no XP per skill, no grinding. The GM grants a rank when a use mattered, announces it in the System voice, applies it at the next safe point, and logs it.
- **Effect:** a rank widens what the skill can do; the GM writes the scope, within the floor rarity ceiling (§3.6). It also adds **+1 to d20 checks** that use that skill at ranks **5, 10 and 15** (so +1, +2, +3), and **+4 at rank 20** for a family skill. Ranks never replace 5e proficiency.
- **Own scales win:** crafting skills (`rules/20-crafting-5e.md` §3) and the Cockroach Clause (Tier 1 / Tier 2, above) keep their own rank scales, and those win wherever they differ from this general track.
- Where older text counts uses (the "5 uses" Cockroach Clause route above), read the count as a rough pace guide, not a counter.
- Caleb can veto.

### 6.6 Stairwell Checkpoint (descent restores you)

Reconciling with §5.6 (**Long Rest only in saferooms**): the stairwell is *not* a saferoom and does not grant a Long Rest. It grants a smaller, descent-only restoration.

**When a living crawler descends through a floor's stairwell / gate (the exit that grants the descent milestone, §2.3):**

- Hit points are restored to **full**.
- They regain **Hit Point Dice** as for a Long Rest (up to half of their total, minimum one).
- **Conditions and Exhaustion** are unchanged, except the Soft Open Exhaustion penalty, which clears on descent (§6.2).
- **Not restored:** spell slots, features that recharge on a Long Rest, attunement changes, or consumed items. The crawler still needs a saferoom for a Long Rest. The checkpoint doesn't count as a Long Rest for the 24-hour limit.
- **Descent only.** Going up or sideways is not a Checkpoint. A crawler can't farm it by stair-hopping: it fires **once per crawler per floor transition**, on arrival at the new floor's stairwell landing.
- **Dead and dying crawlers aren't restored.** A dead crawler stays dead. A crawler carried down while at 0 HP and still dying must be stabilized as normal; one who is already stable arrives at 1 HP, and gets nothing else from the Checkpoint.
- **Curse override.** If something says "can't regain hit points" (e.g., the Marked for Death curse, §6.7), the Checkpoint does not restore HP.

*System note:* "Thank you for using the stairwell. Your hit points have been refilled by an unnamed contractor. Please do not look at him."

### 6.7 Cursed revival: the Marked for Death ring [HOUSE]

An optional **cheaper revival** for Costly Revives tables. Instead of **one** of the Invoice's two menu picks (§6.4.4), the revived crawler wears the System's **Marked for Death** ring. It is still a revival: the Voucher or Rare Offer (§6.4.2), the cooldown and caps (§6.4.1), the Licensing Fee, the other menu pick, and Revival Sickness (§6.4.5) all still apply.

**Marked for Death Band** (ring; Rare; cursed; attunement is forced)

> When you are revived under this route, the ring **appears on your finger** and you are attuned to it automatically (it counts against your three attunement slots). You can't remove it, and you can't end your attunement to it, while you are cursed.
>
> **The Mark.** The System names a **Marked Target**: a specific creature (a named enemy, an elite, or a floor boss) chosen by the AI. **While the Marked Target lives, you can't regain hit points** from any source, including healing spells, potions, Hit Point Dice, rests, and the Stairwell Checkpoint. You can still receive Temporary Hit Points, be stabilized (Medicine), and benefit from non-HP effects.
>
> **Resolving the Mark.** The curse ends when the Marked Target **dies** and you took part (you dealt damage, you helped an ally who did, or you were in the scene); if the target dies without you, the System names a new target in 24 hours. The ring then crumbles, with a toast.

**The save.** When you are first revived with the ring, make a **Wisdom saving throw**:

| Floor band | DC |
|:----------:|:--:|
| F1–8 | 13 |
| F9–14 | 15 |
| F15–18 | 17 |

On a **success** the curse is **partial** (a "Soft Mark"): you can regain hit points, but only up to **half your hit point maximum** (rounded down) while the target lives. On a **failure** the curse is **full**.

**Fairness rules for the AI**

- The Marked Target must be **killable and reachable** by the end of the *next* floor (or earlier). No immortal gods, no unwinnable fights. If the party skips the target (e.g., it's on a floor they've left), the System moves the Mark to a new reachable target at the next saferoom.
- The AI **telegraphs the target's location** in a hint at each saferoom ("bounty board").
- A crawler under the Mark gets the System's sympathy, which is to say, a toast.

**Removal**

| Method | Result |
|--------|--------|
| Kill the Marked Target | The curse ends; the ring crumbles. Free. |
| *Remove Curse* (3rd level) | The ring falls off and goes inert, but the System bills an **Early Termination Fee**: a Standard menu pick (§6.4). |
| **Pay out the contract** at a saferoom terminal | Credits: 1,000 × floor number. No other cost. |
| Die again | The ring goes with the corpse; it can be found, and it will want a new owner. |

The ring is a **cursed item**: the AI may place it in a box or on a corpse as a trap.

### 6.8 Running the options

- **Canon Hard:** On death, toast, corpse cache, reclaim boxes, replacement joins at the next saferoom. Buffers (§6.5) and the Stairwell Checkpoint (§6.6) are the only mercy.
- **Costly Revives (campaign default):** On death, the AI states plainly whether any route is open: a Revival Voucher in hand (or a System Rare Offer), the floor gate and time window (§6.4.3), the cooldown and campaign cap (§6.4.1; log `REVIVALS-USED` and `LAST-REVIVAL-FLOOR`), and whether a Canon-verified exception (§6.4.6) or a canon true-revival story beat (§6.4.7) applies. Usually the answer is no. If yes, the party decides whether to pay the Fee and **two** picks; the System gloats. If no (or they decline), the crawler is dead and a replacement joins. The ring (§6.7) can replace one pick. After the third revival, play as Canon Hard.
- **Soft Open:** On death, §6.2; no revival rules apply. Floor 1 Reprieve follows the table setting (ON by default in Season Zero; a missed-collapse death is never covered).

### 6.9 System snark: deaths

Use one line per death, always specific to the deed. Never reuse a line in the same campaign. Original text; adapt names and details.

**Death toasts (pick by cause)**

- **Fall:** *"[Name] discovered the floor. The floor was very welcoming."*
- **Trap:** *"The pressure plate was clearly marked. In a language [Name] was too proud to read."*
- **Boss:** *"[Name] and the [Boss] reached a disagreement. The disagreement had the last word."*
- **Friendly fire:** *"Cause of death: [Ally]'s enthusiasm. The audience has opinions about [Ally]."*
- **Fleeing:** *"[Name] ran. The [Monster] did not. Advantage: [Monster]."*
- **Drowning:** *"[Name] attempted to hold their breath for the rest of the floor. The floor won."*
- **Poison:** *"[Name] licked the thing. A lot of people said not to lick the thing."*
- **Starvation / exhaustion:** *"[Name] ignored the 'Please Rest' sign. The sign is now taking credit."*
- **Heroic death:** *"[Name] stepped in front of the [Hazard] for [Ally]. Four million viewers got something in their eye. Rating: a lot."*
- **Dumb death:** *"[Name] looked at the obvious thing, pointed at the obvious thing, and touched the obvious thing."*
- **Reading ahead:** *"[Name] skipped the tutorial. The tutorial is, in retrospect, very good."*
- **Saferoom lie:** *"Certification revoked posthumously. [Name] is no longer in a position to complain."*
- **Last words:** *"[Name]'s last words were '[Quote].' We are releasing them as a ringtone."*
- **Massive damage:** *"[Name] has been rendered into a smaller number of pieces. Please enjoy the ones you find."*

**When a buffer fires (§6.5)**

- *"Cockroach Clause invoked. [Name] has been informed that they are not allowed to enjoy this."*
- *"Half-Splat consumed. [Name] is now 5% of a person and 100% of a problem."*

**Revival toasts (Costly Revives only; the System gloats)**

- *"[Name] has been refunded. Please note our policy on refunds: it is a joke."*
- *"Your resurrection has been processed. A paperwork fee of [N] credits has been applied. We regret nothing."*
- *"[Name] is back. The Syndicate takes its cut. The Syndicate always takes its cut."*
- *"Two line items and a fee of [N] credits. [Name] is alive, in the sense that an invoice is alive. Enjoy the Sickness!"*
- *"You were dead, and it was cheaper. We have noted your preference for the expensive option."*
- **Sickness cured:** *"Revival Sickness has cleared. [Name] may resume being a person. The Syndicate will remember this generosity."*
- **Cap reached / cooldown:** *"Your account is not eligible for further refunds. The last one was a favor; we do not run a charity. Please see: death."*

**System gag: the Dead Crawler Card** [**CANON-INSPIRED**: canon renders fallen crawlers as cards; the sales pitch and item are original]

When a crawler dies, the System may offer a collectible **Dead Crawler Card** while the party is still arguing over a Voucher or Rare Offer. It is a **flavor and trophy item only**: it has no weight, no sale value, and **no mechanical effect**. It does **not** revive anyone, is not a Voucher, does not change `REVIVALS-USED` or any §6.4.1 limit, and cannot be spent, traded for credits, or used to satisfy any Invoice. The AI lists it on the sheet as a trophy and may bring it back as a running gag. Use it once per death, use a fresh line each time (the no-reuse rule above), and skip it if the player of the dead crawler is not enjoying the moment. In Canon Hard or Soft Open the System still may offer it, minus the voucher-debate banter.

- *[SYSTEM] Condolences on your recent loss. [Name] has been converted into a limited-edition collectible, now available in stores that do not exist.*
  Reward: one Dead Crawler Card (holographic; the hologram is [Name] looking surprised).
- *[SYSTEM] We see you are debating a Revival Voucher. While you debate, please enjoy this card. It is not a revival. It is a card. We understand the confusion; it has the same face.*
  Reward: one Dead Crawler Card, suitable for display, sulking, or avoiding a decision.
- *[SYSTEM] This offer expires when you stop arguing. It does not expire when you stop arguing. Either way, the card is yours.*
  Reward: one Dead Crawler Card, signed by nobody, at no extra charge.
- *[SYSTEM] Collect the whole party! Full sets are available at a discount, which is to say, soon.*
  Reward: one Dead Crawler Card. Rarity: Dead.

**Reprieve toast (Floor 1)**

- *"[Name] was, for legal reasons, not dead. Please do not take this as a precedent."*

*System note:* "Death is final. This is not a threat; it's a refund policy."

---

## 7. Species, classes, backgrounds

### 7.1 What's allowed

- **2024 PHB species, classes, subclasses, backgrounds, and feats** are allowed if the table owns the book. Without the book, use **SRD 5.2** content only.
- Other official 5e content: owner's call (§12). Homebrew species/classes: owner approval only.
- Multiclassing and feats per 2024 rules.

### 7.2 Floor 1 intake = 5e character creation

The **Intake Kiosk** runs standard 2024 character creation (class, background, species, ability scores, equipment), reskinned as a hostile customer-service process:

- **Background** = who you were before the Crawl (Soldier → ex-military or security guard; Sage → grad student; Criminal → exactly what it sounds like; Acolyte → youth pastor; etc.). Mechanics unchanged.
- **Class** = your **Provisional Class**: full 5e class features from level 1, but the System labels it "provisional" and it looks like improvised talent (a wizard's spellbook is a cracked phone app; a fighter's style is "fell into it").
- **Species** = mechanically chosen at level 1 (for balance) but **latent**: everyone *looks* baseline human on Floors 1–2. Traits still work, explained as "quirks" (darkvision = "your pupils do a thing").
- **Equipment** = 5e starting equipment, reskinned as junk and vending loot (a longsword is a sharpened sign post; it's still a longsword: 1d8 slashing, Sap mastery).
- **Starting credits** = per 5e chargen choices.

### 7.3 Floor 3+ identity (reskin layer)

At the rural Continuum (F3) the **identity market** opens:

- **Species manifests**: the crawler's body visibly becomes their chosen species. No mechanical change.
- **One free rebuild** (optional): each crawler may swap species and/or background (and redistribute background ability increases) once, at the F3 identity market. Same level, same class. Designed for players who now know what they want.
- **Official Class Title**: the System "certifies" the class with a flashy DCC-style title (e.g., Fighter (Battle Master) → "Licensed Brawl Technician"). Pure flavor, but NPCs, sponsors, and Broadcast Name use it. This lines up with the level 3 subclass on the standard track.
- **Later identity teases** (F8 Echo Self, F13 Ledger Name, F16 mirror splits) are reskin and story layers unless a floor doc grants mechanics.

---

## 8. Monsters and CR by floor

### 8.1 Default: reskin SRD monsters

1. Pick an SRD 5.2 (or 2024 MM) stat block at the target CR.
2. **Reskin**: new name, look, damage type swap if thematic, and one tweaked trait. Keep the numbers.
3. Give it a System nameplate (§8.4).

Examples: Giant Rat → *Vent Rat*; Animated Armor → *Mascot Suit (Unoccupied)*; Ogre → *Floor Manager*; Veteran / Knight-type stat blocks → *licensed hunters* (F6); Mage-type → *court sorcerer* (F9); Planetar/Solar-tier celestials → *Olympus courtiers* (F12); devils → *Ash Choir* (F15).

### 8.2 Homebrew monsters

- Start from the closest SRD stat block of the target CR and adjust; don't build from scratch unless necessary.
- Keep AC, HP, attack bonus, damage per round, and save DCs within the range of official monsters of that CR.
- Bosses: give **Legendary Actions** / **Legendary Resistance** (as 5e designs them) to solo bosses at CR 5+, and lair-style phase changes for floor bosses. Telegraph area attacks one round ahead in tutorial floors.
- Every homebrew monster gets a one-line **"what it wants"** and **"how to cheese it"** (the show rewards cleverness).

### 8.3 CR targets by floor (standard track, party of 4)

Use the **2024 DMG XP budget** for the actual party size and level; this table gives starting points. **Party level** follows decision **033** / §2.2 (arrive N on F1–3, N+1 on F4–9, N+2 on F10–18). CR bands are keyed to that party level (same ranges previously listed under the floor whose old N/N+1 party level matched).

| Floor | Party level (arrive → leave) | Mobs (in groups) | Elites | Floor boss (with support) |
|------:|:----------------------------:|:----------------:|:------:|:-------------------------:|
| 1 | 1 → 2 | 0 – 1/4 | 1/2 – 1 | 2 |
| 2 | 2 → 3 | 1/8 – 1/2 | 1 – 2 | 3 – 4 |
| 3 | 3 → 4 | 1/4 – 1 | 2 – 3 | 4 – 5 |
| 4 | 5 → 6 | 1 – 2 | 3 – 4 | 7 – 8 |
| 5 | 6 → 7 | 1 – 2 | 4 – 6 | 8 – 9 |
| 6 | 7 → 8 | 2 – 3 | 5 – 6 (hunters) | 9 – 10 |
| 7 | 8 → 9 | 2 – 3 | 6 – 7 | 10 – 11 |
| 8 | 9 → 10 | 3 – 4 | 7 – 8 | 11 – 12 |
| 9 | 10 → 11 | 3 – 5 | 8 – 9 | 12 – 13 |
| 10 | 12 → 13 | 4 – 6 | 10 – 11 | 14 – 16 |
| 11 | 13 → 14 | 5 – 6 | 11 – 12 | 15 – 16 |
| 12 | 14 → 15 | 5 – 7 | 12 – 13 | 16 – 17 |
| 13 | 15 → 16 | 6 – 8 | 13 – 14 | 17 – 19 |
| 14 | 16 → 17 | 6 – 8 | 14 – 15 | 18 – 20 |
| 15 | 17 → 18 | 7 – 9 | 15 – 16 | 19 – 21 |
| 16 | 18 → 19 | 8 – 10 | 16 – 18 | 21 – 24+ |
| 17 | 19 → 20 | 8 – 10 | 16 – 18 | 21 – 24+ |
| 18 | 20 → 20 (cap) | 8 – 10 | 16 – 18 | 21 – 24+ (finale) |

**Lookup by level:** if the party's level does not match the floor row (slow-burn, catch-up, mid-floor), use the CR bands for the row whose party level matches yours. Levels 19–20 and Floor 18's cap share the same CR bands.

**Difficulty mix per floor:** mostly Moderate, some Low (to burn resources and give toasts), 1–3 High per floor (elites, boss). Deadly-beyond-High fights should be **avoidable or telegraphed** (the catalog loves "David vs Goliath," but the fight should be a choice).

### 8.4 System nameplates

Every monster gets a System label when perceived:

```text
Vent Rat. Level 1. "Union member."
Floor Manager. Level 2. Boss. "Has not taken a break in 9 years."
```

**Nameplate Level = CR rounded up (minimum 1).** Bosses get a "Boss" tag. (The *Floor Manager* example is the ogre reskin, CR 2, so it reads **Level 2**, matching the Floor 1 boss row in §8.3.) Nameplates can lie on floors whose rules say the UI is compromised.

---

## 9. AI DM procedure (rules-facing)

**Before the session**

1. Load: `protocols/ai-dm-instructions.md` → `01-game-brief.md` → **this doc** → character sheets → `05-campaign-narrative.md` + relevant `04-floor-bible.md` seeds → active `floors/floor-XX.md` → session state.
2. Check each crawler's **level band**, **attuned items (≤3)**, **Fan Profile**, **active sponsors/vows/riders**, and **unopened boxes**.

**Opening**

3. State floor, objective, special floor rules, floor clock (if any). On a Continuum return, **open with recognition**.
4. Describe only what's perceivable (fog of war).

**During play**

5. Let players type moves; ask one clarifying question max for vague moves.
6. Call **ability (skill) + DC** before rolls when the crawler would know; roll with the visible roller; post formula and result.
7. On failure, advance the fiction (5e "success at a cost" and complications are encouraged). Never "nothing happens."
8. Combat: roll initiative for all, announce order and **crawler blocks**, enforce turn timeouts, apply Standing Reactions/Orders, group identical enemies.
9. Build encounters with the 2024 DMG budget; use §8.3 as the starting point.
10. **Achievements:** decide what's notable (§3.2), toast with System voice, choose the tier (§3.4), tailor (§3.5), respect ceilings and budget (§3.6–3.7). Snark-only is a valid, frequent answer.
11. Loot: roll boxes publicly in saferooms; choose items; reskin; enforce attunement 3.
12. Track HP, Hit Point Dice, spell slots, conditions, Exhaustion, Heroic Inspiration, consumables, and timers.
13. Surface seeds naturally; don't explain them.
14. Make temporary rulings when the rules are silent; log them.

**Closing**

15. Update session state: location, map revealed, HP/HD/slots, conditions, inventory and attunement, credits, boxes (unopened), achievements (with tier), Ratings tier, sponsors/riders, vows, Continuum state, seeds planted/fired, temporary rulings, Fan Profile updates, next hook (one sentence).

**System voice discipline:** toasts are short. One great line beats four okay ones. The System narrates the show; it never overrides player agency or lies about mechanics (unless a floor rule says the UI is compromised).

---

## 10. Floor 1 quickstart (Level 1)

### 10.1 Intake (character creation, ~20 minutes)

1. Run **2024 character creation** at level 1 (class, background, species, ability scores via standard array, point buy or Roll, equipment; Roll = three arrays of 4d6 drop lowest, keep ONE that totals 73+, see `characters/character-creation-5e.md` §3.6 and decision 024). Species is latent (§7.2).
2. Reskin equipment as junk; mechanics unchanged.
3. Write: **name, one-line look, one-line hook** (why this crawler is still funny or dangerous).
4. Write **Standing Orders** and **Standing Reactions** (§2.5).
5. The AI seeds a starter **Fan Profile** from the hook and intake banter.
6. Session-state entries: Ratings = Unknown; no sponsors; no Broadcast Name yet.

### 10.2 What Floor 1 teaches (rules subset)

- d20 tests vs DC; Advantage/Disadvantage
- Action / Bonus Action / Reaction; Opportunity Attacks
- AC and HP; Short Rest with Hit Point Dice
- **Death saves** (the tutorial should show one, ideally survived)
- Loot boxes (one **Bronze "Welcome Box"** per crawler, opened in the first saferoom with one tailored pull)
- Achievements (snark-only on the first one is traditional)
- Saferooms and Long Rest
- Level 2 at the Green Room (Floor 1's second saferoom, before the boss; see §2.3)
- Stairwell = floor clear (no extra level on Floor 1)

### 10.3 Floor 1 targets

| Item | Target |
|------|--------|
| Encounters | 4–8 total; mostly Low/Moderate; 1 High (tutorial boss) |
| Enemies | CR 0–1/4 mobs (Vent Rats, stirge-types, skeleton/zombie-types, bandit-type "orientation staff"), CR 1/2–1 elites, CR 2 boss (e.g., an ogre reskin with a telegraphed slam) |
| DCs | Mostly 10–13; one 15 for a secret |
| Loot | Welcome Box + 1–3 Bronze, 0–1 Silver per crawler; 2–3 Potions of Healing across the party; credits from mobs |
| Seeds | **Odd Coin** in a loot crate (*Vendor Oddity (Unappraised)*); **Benefactor Signal** static (`…HOLD… NOT YET…`) mid-combat or in the saferoom speaker |
| Toasts | 6–10 per crawler; at least 2 snark-only |
| Milestone | Reach the Green Room (second saferoom, before the boss) alive → **level 2 there**; the stairwell grants **no extra level**; arrive on Floor 2 at level 2. *Table option:* strict descent leveling (level 2 at Floor 2 Onboarding) with Boss Variant B in `floors/floor-01-5e.md` §6.6 |

### 10.4 Sample opening toast

```text
╔══ SYSTEM ══════════════════════════════════════════╗
  Welcome to Floor 1: The Orientation Pit.
  Objective: Find a stairwell. Survive.
  Tip: You have Hit Points. Please keep some.
╚════════════════════════════════════════════════════╝
```

---

## 11. Changelog

| Version | Date | Notes |
|---------|------|-------|
| v0.1 | 2026-10-02 | `02-core-rules.md`: custom chassis (5 stats, Move+Act, Armor subtracts damage, Grit death saves, 10-slot inventory). **Superseded.** |
| **v0.2** | 2026-10-03 | **Rebuilt as an overlay on D&D 5e 2024 (SRD 5.2).** |
| **v0.2.1** | 2026-10-03 | **Loot box rework** (agreed with DCC AI GM and DCC Lore): six tiers, Celestial story-event cap, deed-based box names, box types, stricter opening rules. |
| **v0.2.2** | 2026-10-03 | **Death, replacement, and revival rewrite (§6):** permadeath canon (Canon Hard default), optional Costly Revives, Soft Open, near-death buffers, Stairwell Checkpoint, Marked for Death ring, death snark. |
| **v0.2.3** | 2026-10-03 | **Death Mode = Costly Revives, VERY COSTLY and RARE (Caleb's decision):** campaign default; revive caps and Vouchers; Fee plus two heavier menu picks; Revival Sickness; Canon-verified exceptions subsection; §6.5 canon fixes (Half-Splat, Cockroach) and Lifesaver Draught. |
| **v0.2.4** | 2026-10-03 | **Consistency fixes + canon Brew:** Floor 1 level 2 at the Green Room (§2.3, §10.2-10.3); Silver floor-1-2 boss box cap (§4.7); Death Mode default already picked (§6.0); nameplate example fixed to Level 2 (§8.4); **Mordecai's Special Brew** remapped to canon per DCC Lore (§6.4.6, new §6.5 entry). |
| **v0.2.5** | 2026-10-03 | **Revival source labels + canon true revivals + Dead Crawler Card gag:** every revive and death-bypass source in §6 labeled **CANON / CANON-INSPIRED / HOUSE** (key at the top of §6); new §6.4.7 canon true revivals (**CANON**); Dolores Doesn't Splat added (**CANON**, falling-only); Dead Crawler Card System gag (§6.9). |
| **v0.2.6** | 2026-10-04 | **Story Box exception (Caleb approved Legendary Story Boxes on Floor 1):** one-line amendment in §4.1, §4.5 and §4.7; full design in `rules/45-story-boxes-5e.md`. Celestial rules unchanged. |
| **v0.2.7** | 2026-10-04 | **Crafting merge (Caleb approved, 2026-10-04):** new §5.11 pointer "Crafting: see `rules/20-crafting-5e.md`" with Personal Space and the 1-round potion cooldown; §5.9 gains the Table Token corpse-cache exception, the saferoom stash and the System Inventory time-lock note; §5.6, §1.2 and the §6.5 lockout cross-reference. Preserves v0.2.6's Story Box amendments unchanged. |
| **v0.2.9** | 2026-10-04 | **Several Crawlers per player (pointer only):** one bullet at the end of §6.3 says a replacement may come from the player's benched Crawlers, swapped in only at session zero or between sessions; no rule, number or table changed. Source: `decisions/020-multiple-crawlers-active-swap.md`. |
| **v0.2.8** | 2026-10-04 | **Story Box answers (Caleb, 2026-10-04):** the Story Box exception lines in §4.1, §4.5 and §4.7 now say the item is tradeable, lootable and sellable once opened (not bound), the deed is recorded and announced at award time and the box is held unopened until a saferoom; §4.2 states that box credit pulls get no floor multiplier. §4.4 and §6.2 unchanged. |
| **v0.2.10** | 2026-10-04 | **Caleb's rulings (2026-10-04):** (1) an unopened Story Box reclaimed on its Crawler's death frees its Story Box cap slot (one-line additions in the three Story Box exception lines, §4.1/§4.5/§4.7, and the §6.2 unopened-boxes bullet; opened items stay lootable and not bound); (2) Floor 1 Reprieve is ON for this campaign, Floor 1 only (§6.0 and §6.2; the rules default stays OFF). No number or table changed. Sources: `decisions/020-multiple-crawlers-active-swap.md` v1.2, `rules/45-story-boxes-5e.md` v0.2.2. |
| **v0.2.11** | 2026-10-04 | **Pets (pointer only):** one bullet at the end of §2.4 points to `rules/60-pets-companions-5e.md` (pets, Caleb's ruling 2026-10-04, decision 022); no rule, number or table in this file changed. |
| **v0.2.12** | 2026-10-04 | **Roll method (pointer only):** §10.1 step 1 names Roll as a third ability-score method and points to `characters/character-creation-5e.md` §3.6 (decision 024, Caleb 2026-10-04). No other rule or number changed. |
| **v0.2.13** | 2026-10-04 | **Missed-collapse loot (pointer only):** one bullet in §6.2 points to `decisions/028-collapse-death-loot.md` (Caleb, 2026-10-04): a Crawler's credits and items are destroyed with the floor, survivors may loot only while the floor stands, "floor lost" ledger write-off. No other rule or number changed. |
| **v0.2.14** | 2026-10-04 | **Collapse clock (pointer only):** the §6.2 missed-collapse bullet now states the final collapse is at a fixed 24 in-game hours into the last day and that the GM keeps a running floor-hour count in the carry-on tracker (`floors/f01/00-overview.md` §2 rule 6, `gm-notes/40-floor1-run-sheet.md` §5). No other rule or number changed. |
| **v0.2.15** | 2026-10-04 | **Book Author stale-text fixes (rulings already made):** (1) §5.8 rewritten to match decisions 026/028: a missed collapse is death on every floor, no Reprieve, no toll, credits and items destroyed with the floor, loot only while the floor stands, Detour Tax only for a missed Stairwell key; the old "dead or ejected per the floor doc" and "off by default on Floor 1" are gone. (2) Floor 1 Reprieve wording in §6.0, §6.2 and §6.8 now reads ON by default for Season Zero Floor 1, tables may turn it off, never applies to a collapse death (Caleb, 2026-10-04; `decisions/029-book-source-conflicts.md`). (3) §5.10 states that credits is the display label for GP and how copper (1 cp = 0.01 credit) is shown. No number or table changed. |
| **v0.2.16** | 2026-10-04 | **Whole credits only (rules lead ruling, 2026-10-04):** §5.10 says balances are never fractional (matches `tools/state.py` and decision 028); sp/cp are list prices only (1 sp = 0.1, 1 cp = 0.01 credit, reference); the "0.5 credit, 0.05 credit" balance wording is removed; buying rounds UP per cart line (matches `bot/src/create/rules.js`), selling at half rounds DOWN per line (matches `tools/state.py` pet buyback). No price changed. |
| **v0.2.22** | 2026-10-06 | **Book Author Q19, Q20, Q23 answered (Syndicate, 2026-10-06):** (1) Q19: new §6.5.1 System skills level by use (decision 037): one rank at a time from meaningful use, first-time feats, inventive crafting, Skill and Cheat Code Potions, training guilds, and class or species bonuses; cap 15, or 20 for a species' or class's own skill family; no use counters, the GM grants, announces and logs each rank; +1 to d20 checks at ranks 5, 10 and 15 (+4 at 20 for a family skill); never replaces proficiency; crafting skills (rules/20 §3) and the Cockroach Clause keep their own rank scales and win where they differ; Caleb can veto. (2) Q20: achievement boxes on Floors 1–2 are Bronze (soft guideline about 2–3 per Crawler per floor, Caleb 2026-10-05); Silver on F1–2 is the Boss Box or a logged GM override; the one late-entry Silver box for a replacement Crawler (§6.3) is exempt, as it is not an achievement box. Wording aligned in §3.9, the §4.1 Silver and Gold rows, §4.5 and Appendix A. (3) Q23: §2.5.1 passive Perception, Investigation and Insight apply at every table (chat, voice or face to face); roll only when the outcome is uncertain and interesting. No number or table value changed. |
| **v0.2.21** | 2026-10-05 | **Session turn order (Caleb, 2026-10-05; decision 034):** §2.5.1 rolls one Crawler turn order at session start and keeps it for exploration all session (replaces free-form posting order); joiners go last, dead/benched/AFK slots are skipped, pet-Crawlers act right after their owner; §2.5.2 initiative overrides it for that fight only, then play returns to session order. No number or table changed. |
| **v0.2.20** | 2026-10-05 | **§8.3 party levels aligned to decision 033** (Accountant follow-up after rules/70 v0.2.0): floor rows use arrive→leave bands (F4@5 … F18@20); CR bands follow party level (old N-row ranges). Floors 16–18 share the top CR band. |
| **v0.2.19** | 2026-10-05 | **F3/F9 double level bumps (decision 033, Caleb executive):** §2.2 arrive bands N / N+1 / N+2; F3 and F9 end boss +1 then normal onboarding; arrive F4 at 5, F10 at 12, F18 at 20 (finale 19–20 levels removed). §2.3 one-level rule updated. §6.4.3 refund desk re-keyed to arrive levels (floors 4 / 8 / 11 / 15). Accountant re-cuts rules/70 + 75; Book Author Ch1/Ch2. |
| **v0.2.18** | 2026-10-05 | **Field-rest fee clarified (Season Zero):** §5.6 — Short Rest free if already quiet; rules/70 fee buys quiet for a Short Rest in a noisy spot; never a Long Rest outside a saferoom. Decision 031. Day pages already matched. No number changed. |
| **v0.2.17** | 2026-10-04 | **Rules lead rulings (2026-10-04):** (1) Platinum floors: §4.5 wins, no Platinum on F1–8. §4.1 Platinum row now says Legendary achievements F9+ (Gold row: Legendary achievements F3–8, Silver on F1–2); Appendix A maps a Legendary-loot achievement to Gold F3–8 (Silver F1–2) / Platinum F9–14. (2) Story Box cap override is the GM's with a logged reason, Caleb can veto (Caleb's later 2026-10-04 ruling: the rota is a guideline and the only hard Story Box rule is one per floor, which the GM can override with a logged reason; the GM may adapt as play goes). Same text in §4.1, §4.5 and §4.7. Unopened box still bound; item inside tradeable, lootable, sellable. No number changed. |

**v0.2.8 details**

- **§4.1, §4.5, §4.7:** the Story Box exception text no longer says "bound to its Crawler (no sale or trade)". Once opened, a Story Box item is ordinary loot: it drops in the corpse cache (§5.9), trades, and sells (System buyback is a fixed `sale_value` by power rung in `rules/45-story-boxes-5e.md` §4.6; `story_value` is provenance only). The unopened box stays bound and is still reclaimed on death (§4.4, §6.2, unchanged).
- **§4.2:** one line under the credits-per-pull table: no floor multiplier on box credit pulls.
- **Unchanged on purpose:** the cap (one per table per floor, logged override by Caleb only), the saferoom-only opening rule, the pacing table and the Celestial cap.
- **Source:** `rules/45-story-boxes-5e.md` v0.2, `decisions/018-story-box-answers.md`.

**v0.2.7 details**

- **§5.11 (new):** pointer to `rules/20-crafting-5e.md` plus the three pieces that touch core: Personal Space (defined; door in honest saferooms, from Floor 4), the **1-round potion cooldown** (one potion per round; a second in the cooldown still works but Poisoned 1 minute, DC 12 Con save each turn ends it; scrolls and meals exempt), and Table Tokens/stash.
- **§5.9:** a Table Token is not lootable on death (goes to the System or the named heir); a free saferoom-terminal **stash** for Table Tokens only; System Inventory is time-locked for crafted explosives (no decay, no Jolts).
- **§6.5:** the Special Brew lockout is stated to be separate from the cooldown (it wins while it lasts, no extra Poisoned). Numbers unchanged: 10 hours or a Long Rest, max 2 per drinker.
- **§1.2, §5.6, TOC, header:** pointer bullet, Personal Space door and crafting stash listed under saferoom services, version bump.
- **Unchanged on purpose:** every v0.2.6 text (Story Box exception in §4.1, §4.5, §4.7), the revival rules and the Brew numbers. Source: `rules/20-crafting-5e.md` v0.3 §11, decision 013-crafting.

**v0.2.6 details**

- **§4.1, §4.5, §4.7:** the same one-line Story Box exception (one per table per floor, GM hand-pick for a named one-time deed, bound, power note inside the floor ceiling, outside the pacing table) plus a new **Story Box** row in the box-type table. The sentence "no Legendary boxes on Floor 2" in §4.1 still holds for ordinary boxes; the Story Box is the one named exception next to Benefactor Boxes.
- **Unchanged on purpose:** the six tiers, the pacing table numbers, the Celestial cap (one per crawler, DM-gated), the §3.6 ceilings, the §4.4 opening and no-trade rules.
- **Why:** canon has Legendary boxes on Floor 1 (ledger L-001, A-165, A-167; the Legendary Pet Box with the Enhanced Pet Biscuit, I-007). Floor-1 Story Box items stay small in numbers; see `rules/45-story-boxes-5e.md` §4.

**v0.2.5 details** (labels per `lore/catalog/revival-canon.md` v1.0)

- **Canon facts stated (CANON):** no purchasable revival spell exists in canon; the Dungeon never revives dead crawlers (they become collectible cards). So the **Revival Voucher**, the *Revivify* / *Raise Dead* / *Resurrection* / *True Resurrection* gating and Fees, the **System Rare Offer** (plus Back by Popular Demand and the Benefactor/floor-rule routes), the **Marked for Death ring**, Costly Revives and Soft Open as modes, the Floor 1 Reprieve, and the **Lifesaver Draught** are all labeled **HOUSE**.
- **Labels (§6.4.6, §6.5):** **Cockroach** (Donut) and **Mordecai's Special Brew** = **CANON** death-cheats (not revives). **Half-Splat** and **Dolores Doesn't Splat** = **CANON**, falling-only. **Cockroach Clause** (and the *Second Season* Charm) = **CANON-INSPIRED**. The Half-Splat tag note now records the ledger WIKI-ONLY tag against the lore catalog's VERIFIED.
- **New §6.4.7 "Canon true revivals (species/situation-specific story events)" (CANON, DM-only, rare story beats, paraphrased):** Tummy Acher pets (regenerate; +25% stats and a new weakness each time; every 5th death resets), Nodlings (extra life by splitting into yearlings), mercenaries (regenerate on the next floor; floors 6-8), Growler Gary (returns when killed), Grimaldi's circus crew (reborn from the vine), Mrs. Ghazi (rebuilt from one grain of sand), gods (Celestial Thorn Room / Sun of Reawakening), admins and teleport tourists (extracted before death). **Second Chance** (timed undead minion) and **9 Lives** (halve damage) are **not** revives.
- **§6.4.6:** the "no verified revive yet" note now points to §6.4.7; the TODO is narrowed to revives of ordinary crawlers.
- **§6.9 System gag:** the **Dead Crawler Card** (**CANON-INSPIRED**), a trophy offered when a crawler dies while the party debates a voucher; no mechanical revival; four original [SYSTEM] lines, each with `Reward:` on its own line. §6.1 aftermath order mentions it.
- Version bumped to 0.2.5; decision note `decisions/005-death-mode-tuning.md` got an appended line with the same labels.

**v0.2.4 details**

- **§2.3 / §10.2-10.3:** Floor 1 grants level 2 at the second saferoom (the Green Room) before the CR 2 boss, matching `floors/floor-01-5e.md`; the stairwell grants no extra level on Floor 1. Strict descent leveling stays as a table option (Boss Variant B).
- **§4.7:** floor-boss Boss Boxes on Floors 1-2 are capped by the §3.6 rarity ceiling (Floor 1 Boss Box = Silver).
- **§6.0:** notes that the table already picked `DEATH-MODE=Costly Revives` and `COMFORT=Ludicrous` (logged as defaults).
- **§8.4:** nameplate example changed from "Floor Manager. Level 4" to **Level 2** (ogre reskin, CR 2; Level = CR rounded up).
- **Mordecai's Special Brew (§6.4.6, new §6.5 entry):** replaces the earlier proposed "5 rounds / can't drop below 1 HP" mapping with canon per DCC Lore (WIKI-ONLY detail): 30-second immortality-style potion (Gold Standard Healing Potion + Troll's Second Wind; level 3 Alchemy Table, Book 3). Rules: 5 rounds of regeneration at the start of each turn (10/20/30/40 HP by tier), damage alone can't reduce you to 0, **no effect vs instant death**, ~10-hour potion lockout (10 hours or a Long Rest), **max 2 per character**. DM-granted, limited, expensive (5,000 credits + ingredients); a pre-approved canon-verified bypass, **not** a revive and not counted against the revive cap.

**v0.2.3 details** (Costly Revives, VERY COSTLY and RARE; §6; decision note in `DECISION-death-mode.md`)

- **Default:** `DEATH-MODE` for this campaign is **Costly Revives** (§6.0). Canon Hard and Soft Open stay documented as alternatives.
- **Rare (§6.4.1–6.4.2):** at most **1 revival per party per 3 floors**, **3 per party per campaign**, **1 per crawler ever**; at most 1 Voucher held; at most 1 System Rare Offer per 6 floors. Revival spells, scrolls, and items are **not purchasable, craftable, or learnable**; revival comes only from a **Revival Voucher** (boss, quest, or Benefactor reward) or a **System Rare Offer**. Floor gating (F5/F9/F13/F17) retained (§6.4.3). The old saferoom revival service is retired.
- **Brutal pricing (§6.4.3–6.4.5):** the Licensing Fee is now flat **5,000 / 15,000 / 40,000 / 100,000 credits** (was the 300 / 500 / 1,000 / 25,000 component cost); Rare Offer **3,000 × floor**; Back by Popular Demand **2,000 × floor** (was 500 × floor for the service). **Fee AND two different menu picks**, both one weight step heavier than before (Heavy is the ceiling); at most one Celestial Tax. **Revival Sickness:** 2 Exhaustion levels that nothing can remove until the crawler descends and finishes a saferoom Long Rest on the next floor; the System gloats.
- **New §6.4.6 Canon-verified revival exceptions:** pre-approved regardless of limits; seeded from `CANON-LEDGER.md` (Cockroach, Mordecai's Special Brew); no verified true revive yet (TODO). *(Brew mapping updated to canon in v0.2.4.)*
- **§6.5 corrected to canon (per DCC Lore):** **Half-Splat Potion** now prevents death from **falling damage only** and leaves you at 5% (tag WIKI-ONLY). New clearly labeled **house-rule Lifesaver Draught** (crafter-NPC-brewed, 2,500 credits, 1 per crafter per floor, DM-granted only) cancels one fatal blow at 5% HP. **Cockroach Clause** labeled canon-inspired (Donut's Cockroach, VERIFIED, L5/L10) with training routes.
- **Also updated:** §6.0 table and default text, §6.2, §6.3, §6.7 (ring replaces one pick), §6.8, §6.9 (gloating revival toasts), §12 items 4 and 13.

**v0.2.2 details** (death, replacement, revival, §6)

- **Canon:** death is permanent and there are no respawns. **Revival is now a house rule** (Costly Revives), not a default: in Canon Hard the 5e revival spells fail on dead crawlers. 5e 2024 death saves, Stabilize, and massive damage stay as the base (§6.1).
- **Added:** §6.0 Death Modes at a glance (Canon Hard / Costly Revives / Soft Open); §6.5 near-death buffers (Cockroach Clause tiers 1–2, Half-Splat Potion); §6.6 Stairwell Checkpoint (full HP and Hit Point Dice on descent, not a Long Rest); §6.7 Marked for Death ring (curse with save and removal); §6.8 running the options; §6.9 System death/revival snark.
- **Reworked:** §6.4 revival now has floor-gated spells (F5 *Revivify*, F9 *Raise Dead*, F13 *Resurrection*, F17 *True Resurrection*), a Licensing Fee **plus** a Costly Revive Menu pick (Celestial Tax, permanent loss, sponsor debt, forfeit, vow) scaled Light / Standard / Heavy. §6.2 now covers box reclaim, Soft Open ("Syndicated"), and the Floor 1 Reprieve (Tutorial Mercy, still default OFF). §6.3 replacement rules kept, with a note on a later revival.
- **Cross-references updated:** §1.2, TOC entry, §12 items 4 and 13. §4.4 still points at §6.2 (the box-handling rule lives there). §5.6 "Long Rest only in saferooms" is unchanged; §6.6 explains why the checkpoint is not a Long Rest.

**v0.2.1 details** (loot boxes, §4)

- **Tiers:** now six: Bronze, Silver, Gold, Platinum, **Legendary**, **Celestial**. 5e mapping shifted: the old "Celestial = Legendary" row is now **Legendary** (top of ordinary play, up to 5e Legendary rarity). **Celestial** is a story-level event: **max ONE per crawler for the whole campaign**, only at a finale or a truly absurd feat at the DM's discretion, and includes a **DM-designed campaign-defining reward** beyond normal rarity. Pacing table, credits table, guaranteed-headline rule, floor-ceiling note, §3.4 R5 row, §12 open question, and Appendix A mapping updated to match (the old Celestial campaign cap of 2 now applies to Legendary boxes).
- **Naming (new §4.8):** boxes are named after the crawler's deed; tier prefix, short jabs at low tiers, long taunts at high tiers; 20-entry template list.
- **Types (new §4.7):** Boss (scales with boss rank), Quest, Fan, Benefactor (sponsor-only; off-world tech/odd items; a Bronze Benefactor Box can beat a Gold ordinary box). Contents stay semi-random with explicit DM hand-pick permission to help or hurt.
- **Opening (§4.4):** saferoom only (**emergency open removed**), all unopened boxes opened at once, boxes **cannot be traded between crawlers**. §2.4 "split loot boxes" reworded to match.
- **Kept:** personalization rule (§4.3) unchanged. No other files touched.

**v0.2 details**

- **Removed:** Strike/Grit/Wits/Sneak/Presence and the stat array → 5e ability scores. `10 + Grit` HP → 5e class HP and Hit Point Dice. Move + Act → Action / Bonus Action / Reaction + movement. **Armor subtracts damage → Armor Class.** Custom damage dice → 5e weapons with Weapon Mastery. Zones → feet. **Grit DC 12 death saves → 5e Death Saving Throws (DC 10).** Custom conditions → 5e conditions. Saferoom heal `1d6 + Grit` → Short/Long Rest in saferooms. 10-slot inventory → 5e carrying + System Inventory. Common/Rare/Named → 5e item rarity. "No XP, Floor Clear stat bumps" → milestone levels per floor. Tagged class/race actions → full 5e classes and species. "No Vancian slots" → 5e spellcasting as written.
- **Added:** level bands (standard + slow-burn), crawler blocks, turn timeouts, Standing Orders/Reactions, Autopilot, DM-run dice roller; System-as-DM achievement model with R0–R6 reward ladder, Fan Profiles and tailoring, rarity ceilings, pacing budget, anti-abuse, CSV mapping; loot box tiers Bronze → Legendary (+ Celestial story event, as of v0.2.1); Ratings tiers, Crowd Pop, Broadcast Name feature, sponsor deals, Faction Renown, Faction Flag, vows with Invoices; spine-object mechanics; saferoom rest mapping; System Inventory; permadeath toggle, Syndicated mode, Tutorial Mercy, replacement rules, revival surcharges; F1 intake as 5e chargen with latent species and F3 identity reskin/rebuild; SRD reskin monsters, CR-by-floor table, nameplates; AI DM procedure; Floor 1 L1 quickstart.
- **Kept:** floor law, Continuum recognition, saferooms-can-lie, PvP off by default, spine objects as story flags first.

### Carried over: PvP and table safety (unchanged from v0.1)

- **PvP off by default.** On only with unanimous consent for that scene.
- **Content:** PG-13 to R by table agreement; the AI fades to black on request.

---

## 12. Open for owner markup

1. **Level track:** standard (ends ~L19–20) or slow-burn (ends ~L15)? Mid-floor milestones allowed on big floors?
2. **Content scope:** 2024 PHB fully, SRD 5.2 only, or other books (Tasha's, Xanathar's, setting books) too? Homebrew species (DCC-style weird races) at the F3 identity market: yes/no, and does that replace the free rebuild?
3. **Species latent on F1–2:** good, or let species show from the start?
4. **Permadeath default** is ON (canon, decided in v0.2.2). Still open: turn on Tutorial Mercy (Floor 1 Reprieve) for Floor 1? **Decided in v0.2.3:** this campaign runs Costly Revives (VERY COSTLY and RARE); other tables may still pick Canon Hard or Soft Open.
5. **Fudging:** keep "no fudging, dice stand," or allow the System to fudge in the players' favor on F1?
6. **Dice:** AI rolls everything (default), or players roll their own?
7. **Turn timeout** 3 min OK for your group? Crawler blocks ON?
8. **Loot pace:** the budget is a bit above DMG baseline on purpose. Too generous? Too stingy? Legendary box campaign cap of 2 OK? (Celestial is fixed at 1 per crawler, DM-triggered, per v0.2.1.)
9. **Attunement:** hard cap 3 forever, or allow one Legendary achievement / F12 vow to grant a 4th slot?
10. **System Inventory** as a Bag of Holding: keep, or use plain 5e encumbrance (more survival tension)?
11. **Long Rest only in saferooms:** keep, or allow risky Long Rests in the field?
12. **Crowd Pop:** is Heroic Inspiration enough for Ratings, or do you want a separate party "Hype" pool?
13. **Revival (Costly Revives only, §6.4):** *numbers set in v0.2.3 (Fee 5k/15k/40k/100k, caps 1 per 3 floors / 3 per campaign / 1 per crawler, two picks, Sickness = 2 Exhaustion); revisit after play.* Floor gates (F5/F9/F13/F17) kept. Should "Back by Popular Demand" and the Marked for Death ring (§6.7) exist? Should the Stairwell Checkpoint (§6.6) restore Hit Point Dice or just HP?
14. **Floor clock:** default off on F1; which later floors should have one?
15. **Floor Bible title conflicts:** `04-floor-bible.md` still names F3 "Highstreet Sprawl," F9 "Mandate Wars," F12 "Throne Circuit" (pre-Continuum). This doc follows the spine (`05`). Rename the Bible rows?
16. **Doc cleanup:** `03-character-creation.md` is superseded by `03-character-creation-5e.md`, and `00-README.md` / `protocols/session-protocol.md` now point at the v0.2.x 5e docs (v0.2.4 pass). `04-floor-bible.md` carries a "needs Continuum + 5e rewrite" banner; the rewrite itself is still open.
17. **Catalog:** later pass to (a) translate v0.1 stat language in criteria, (b) relabel `Reward` as "suggested tier," (c) add a `Snark` column with toast lines? (Not changed in this draft, per instructions.)
18. **Credits multiplier** by floor (×1/×5/×20/×50) OK?

---

## Appendix A: Achievement catalog field mapping (CSV → 5e)

Catalog snapshot (2026-10-02): **1,823 rows**: Common 1,039 / Rare 576 / Legendary 208; Has Reward Yes 1,671 / No 152; ~100 rows per floor plus 35 "Any."

| CSV field | How the System uses it |
|-----------|-----------------------|
| `ID` | Log key. Never re-pays for the same crawler. |
| `Name` | Toast title. Rename freely for comedy or tailoring. |
| `Criteria` | Inspiration for "what's notable." Meeting it doesn't oblige a toast. Translate v0.1 stat words (§3.9). |
| `Floor` | Where it fits best; "Any" is portable. Per-floor variants (e.g., "Fail a lockpick") are the same joke at a new address; downgrade repeats. |
| `Category` | Combat / Exploration / Social / Survival / Loot / Speed / Crafting / Party / Story Seed / Continuum → normal. **Humor / Meta** → default R0. **Canon Flavor** → writer flag. |
| `Rarity` | Default tier: Common → R0–R1; Rare → R2–R5; Legendary → R5–R6. Item rarity floor-scaled per §3.9. |
| `Has Reward` | No → **R0** always. Yes → suggestion only. |
| `Reward` | Translate: "Title + 25 System Credits" → R1 (credits × floor multiplier) or R0 if dull; "Rare loot roll + Title" → **Silver box** (Bronze on F1–2; Gold on F10+); "Legendary loot roll + Title + cosmetic flair" → **Gold box** (F3–8; on F1–2 **Bronze**, like every F1–2 achievement box; Silver on F1–2 only as the Boss Box or a logged GM override, §4.5) / **Platinum** (F9–14; no Platinum on F1–8, §4.5) / **Legendary box or Headliner** (F15+, within caps; Celestial only by DM decision, §4.1); bespoke rewards ("Trap kit upgrade," "Companion slot perk," "Ratings buff (1 floor)") → nearest R-tier (tool upgrade = R3; companion = R5-equivalent; ratings buff = Crowd Pop / Heroic Inspiration); "Ending flag" / "Seed flagged" → story state, no loot. |
| `Canon Flavor` | No mechanical weight. |
| `Notes` | Context for the AI (e.g., "continuum," "sponsor economy," "generated variant"). |

---

## Appendix B: Sample minor boons ("Crawl Charms")

Charms are **R4** rewards: one-use or few-use supernatural gifts in the style of the 2024 DMG's Charms. Unless noted, a Charm vanishes after its uses or **at descent**, whichever comes first. A crawler can hold **2 Charms** at once.

| Charm | Effect |
|-------|--------|
| **Second Season** | Once: when you'd drop to 0 HP, drop to 1 HP instead. |
| **Commercial Break** | Once: take a Short Rest's benefits in 1 minute (must be out of combat). |
| **Fan Mail** | Twice: gain Heroic Inspiration when you'd otherwise not; can't exceed one held. |
| **Slow-Mo Replay** | Once: after seeing a d20 result within 30 ft, force a reroll (your Reaction). |
| **Product Placement** | Once: pull any mundane item worth ≤ 25 credits from your System Inventory that you didn't have. |
| **Stage Lighting** | 3 uses: as a Bonus Action, a creature you can see is outlined in light until the end of your next turn (attacks against it have Advantage; it can't benefit from being Invisible). |
| **Contract Fine Print** | Once: Advantage on a check to find a loophole, read a contract, or argue with a System terminal. |
| **Laugh Track** | Once: as an Action, one creature within 30 ft makes a Wisdom save (DC 8 + your Proficiency Bonus + your highest mental modifier) or has the Incapacitated condition until the end of its next turn, laughing. |
| **Map Leak** | Once: reveal the nearest saferoom or stairwell on your System Map. |
| **Stunt Double** | Once: when a creature hits you with an attack, an ally within 5 ft may take the damage instead (their choice). |
| **Sponsor's Bottle** | Once: a Potion of Healing appears in your hand as a Bonus Action. It is branded. |
| **Encore** | Once: regain one expended spell slot of level ≤ 2 or one use of a feature that recharges on a Short Rest. |

**Blessings** (R6, permanent): model on 2024 DMG Blessings; examples: *Recognized* (Broadcast Name works twice per Long Rest), *Iron Stomach* (Advantage on saves vs. Poisoned), *Lucky Number* (once per Long Rest, treat a d20 roll of 1 as a 10).

---

## Appendix C: Toast templates

```text
NEW ACHIEVEMENT: <Name>
<One-line criteria, written as an accusation.>
REWARD: <tier text>  — or —  REWARD! ... no.
```

**Snark-only examples (original):**

- **Ambassador of Retreat**: *You fled a fight with full HP. The audience respects your cardio. Reward: their respect, which is worth nothing.*
- **Fine Print Enjoyer**: *You read an entire System popup. Nobody does that. Reward: the knowledge that you're the reason we can't remove them.*
- **Floor Is Lava (Literal)**: *You stepped in the obvious thing. Reward: a fun new smell.*
- **Loot Goblin, Tier 1**: *You opened a crate mid-combat. Reward: you are being attacked.*
- **Customer Feedback**: *You asked the System for a specific reward. Your request has been received and laughed at.*

**Tailored example:**

- **Loyal Collector** (crawler with the plush fixation): *You have collected 5 Limited Edition Plushies. REWARD: Plushie #6, "Gristle the Bear, Mourning Edition." Nobody else on this floor has one. Nobody else wants one.*

---

## Appendix D: SRD attribution

This work includes material from the System Reference Document 5.2 ("SRD 5.2") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

*(This doc references rules by name rather than reproducing them. Content from non-SRD 2024 books is used only if the table owns those books, and is never copied into this pack.)*
