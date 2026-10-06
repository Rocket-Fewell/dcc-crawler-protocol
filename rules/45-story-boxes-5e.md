# Story Boxes (5e Overlay)
Owner: Syndicate | Status: draft | Version: 0.2.4 | Updated: 2026-10-04
Summary: Design of the Legendary Story Box for Floors 1-2: what counts as a Story-Box deed (checklist, anti-farming, example deeds), the GM procedure in the System's voice, the power ladder (3 patterns, 5 worked cards in loot-deck schema 0.1.2), how Story Boxes differ from Benefactor Boxes and relate to achievements and the Fan Profile, the spotlight guideline across four Crawlers, looting, trading, death and resale rules, the beta reset, the core amendment text, one open question, and the changes the room must make (Lore, Architect, Accountant).
Depends on: rules/40-loot-deck-spec-5e.md v0.1.7 (§1.1 fields, `story_value` and `bound`, schema `loot-deck/0.1.2`, §2.5 announcing, §2.8 short rule, §3.2 audit hint), rules/42-house-items-f01.md v0.2.3 §6 (Enhanced Pet Biscuit, card f01-any-0055), rules/10-core-rules-5e.md v0.2.16 (§3.4-3.8, §4.1, §4.4, §4.5, §4.7, §6.2, §6.9), gm-notes/00-gm-principles.md ("Achievement announcements", "Loot box and item detail", exchange framework), gm-notes/30-player-channel-card-format.md, characters/create-flow-spec-5e.md v0.1.13 (hidden Fan Profile, S13), `dcc-lore/drafts/f01-legendary-oneoffs-research.md`, `tables/loot-decks/f01-any-story-boxes.json` (Lore's first five cards, read only), tools/state.py `loot story-box` (read only). Consumers: AI GM (runs it), Architect/Borent (tooling), the Accountant (story-value line), DCC Lore (deck), Valtay Corp (player book: do NOT print §2.5 or §2.6).

> **Status:** DRAFT v0.2.4. Nothing here is LOCKED except what the room already agreed (§1.2). Caleb answered five of the six open questions on 2026-10-04 (§9); only item strength (old Q2) stays open. **Project:** *Crawler Protocol: Season Zero*, private fan RPG inspired by *Dungeon Crawler Carl*.
> **Why this exists:** Caleb approved Legendary Story Boxes on Floor 1 (2026-10-04) and asked for "a really good system". Canon puts three Legendary boxes on Floor 1 or the tutorial. A Season Zero table needs one that is rare, fair, readable and hard to farm.
> **Who reads it:** the AI GM and Caleb. Players do not see §2.5, §2.6 or the card list; they cannot request a Story Box (core §3.5 rule 6).
> **Tags:** `CANON` = tied to a CANON-LEDGER entry; `CANON-INSPIRED` = shaped by canon, not a canon item; `HOUSE` = our invention. Canon claims here are ledger rows L-001, I-007, M-037, A-165, A-167 (wiki-sourced, VERIFIED in the ledger, **not checked against the novels**) and the Lore research draft. System lines are written fresh in the voice described in `dcc-lore/catalog/system-voice.md` §1.2; nothing is copied. Players are "Crawlers".

## Contents
1. What a Story Box is, and what the room already agreed
2. Deeds: what qualifies, anti-farming, example deeds
3. GM procedure (step by step)
4. The power ladder: rules, three patterns, five worked cards
5. Story Box vs Benefactor Box; achievements; Fan Profile tailoring
6. Spotlight guideline, looting, trading, death, resale, and the beta reset
7. Core amendment text (applied to core v0.2.8)
8. For the Architect: what exists, what is missing
9. Open question for Caleb (1 open, 5 answered 2026-10-04)
10. Changes for the room (Lore, Architect, Accountant)

---

## 1. What a Story Box is, and what the room already agreed

### 1.1 In one paragraph
A **Story Box** is a **Legendary** box that the GM hands to one Crawler (or one table) for **one named, one-time deed** that nobody scripted. It is named after the deed, it holds one hand-made item that echoes the deed, and it is **tradeable**: once opened it is an ordinary item that can be traded, looted from a corpse or sold per canon, though its `story_value` is never turned into credits automatically (§6.5). On Floors 1-2 the item's **numbers stay small**; the "Legendary" is in the story, the banner and the book-keeping. Canon shape: Carl's Legendary Pet Box held the Enhanced Pet Biscuit that made Donut a Crawler (L-001, I-007, M-037); Donut's Legendary Quadruped Box (A-165); Frank Q's Legendary That's the Spirit! Box (A-167). In our game "Quadruped" means **any quadruped companion** (cat, dog, goat, pig, gator), not only cats.

### 1.2 Agreed by the room (treat as fixed; Caleb can change them)
| # | Rule |
|--:|---|
| 1 | **Hand-pick only.** Never a random draw, never an upgrade roll. `draw_weight` is 0. |
| 2 | **Tradeable and lootable** (Caleb, 2026-10-04). Story Box items are not bound: once opened they can be traded, looted from corpses and sold per canon. `story_value` is tracked apart from credits and is never converted automatically; a sale is a normal credit transaction (§6.5). |
| 3 | **One named deed per box,** with the deed sentence written **at award time**, not afterward. |
| 4 | **A deed cannot pay twice** (for anyone, in that session). |
| 5 | **Cap: one per table per floor** (the whole floor, not per play night), which **the GM may override with a logged reason** (Caleb can veto; Caleb's ruling, 2026-10-04, later than decision 018). This is the only hard limit on awards; the spotlight rota is a GM guideline (§6.1), and the GM may adapt as play goes. **Count rule (Caleb, 2026-10-04):** the cap counts only Story Boxes held by live (non-deleted) Crawlers. Deleting a Crawler with `/delete` frees its slot; its archived ledger rows are for audit only and do not count. A dead Crawler that is not deleted still counts if it holds an opened or already-awarded Story Box item (§6.3). **A Story Box reclaimed unopened at its Crawler's death does not count** (Caleb, 2026-10-04): its slot is freed, so the per-floor cap and the "one per living Crawler" counting treat it as not held (§6.3). The Crawler must be the player's active Crawler to receive one (create-flow spec §8). |
| 6 | **`story_value` has its own ledger line** and is **excluded from the Accountant's 1,500-credit economy flag** when awarded. If the item is later sold, the sale price is an ordinary credit transaction and is flagged like any other (§6.5). |
| 7 | **Every card carries a power note** (`power_note:` in `notes`; format in §4.3). |
| 8 | Tooling is the Architect's job (§8, §10). This file is the design. |
| 9 | **Saferoom only.** Like every loot box, a Story Box can be opened only in a saferoom (core §4.4, unchanged). The deed is recorded and announced at award time; the box is held unopened until the next saferoom. |

### 1.3 Terms
| Term | Meaning |
|---|---|
| deed | The one thing the Crawler did, written as one plain sentence in the past tense. |
| deed kind | The sentence with the names removed ("first quadruped companion through the entry"). A kind pays once per session. |
| table deed | A deed done by several Crawlers together; it pays one box (§6.2). |
| spotlight guideline | GM guideline: try to give every living Crawler a first Story Box before anyone gets a second (§6.1). Not a hard rule. |
| power note | The GM-side line that says how strong the item is for the floor and what is locked (§4.3). |

---

## 2. Deeds: what qualifies

### 2.1 The checklist (the GM runs it silently at the moment, in under a minute)
**Hard gates. Every one must be a yes, or it is not a Story Box (pay a normal achievement instead).**
| # | Gate | Plain test |
|--|---|---|
| G1 | **First of its kind in this session** | Run `state.py loot deeds` and the achievement log. Would an earlier deed's one-sentence summary also fit this one? If yes, it is the same kind: no. |
| G2 | **Unscripted** | The GM did not offer it, hint at it, put it in a quest, or let an NPC suggest it. The players chose it. |
| G3 | **Risky or absurdly creative** | Something real was on the line (HP, a resource, a relationship, a stuck-with-it choice), or the plan was one nobody saw coming and the rules still allowed it. |
| G4 | **Witnessed** | At least one other Crawler or the System-on-camera saw it, and it is in the roll log or text channel so the GM can quote it. Two players quietly arranging it between themselves fails G2. |
| G5 | **Not farmable** | The same situation cannot be rebuilt on demand. If the deed is a recipe, it is not a deed. |
| G6 | **One sentence** | The GM can write the deed in one sentence of 25 words or fewer, without "and then". |

**Soft signals. At least two of four.**
| # | Signal |
|--|---|
| S1 | The table gasped, laughed or went quiet (the pub test: they will retell it). |
| S2 | It cost something visible, and the Crawler paid it. |
| S3 | It says who this Crawler is (core §3.2 item 5). |
| S4 | It echoes a canon first (a pet, a quadruped, a fight with a fictional rival) in a way the table made its own. |

**Not enough on their own:** being first to kill something, clearing a zone, finishing a quest, a good roll, a clever joke, or "no one else tried it". Those pay normal achievements (core §3.4).

### 2.2 The deed record
Write these **before the banner** (this is "award time"): the **deed** sentence, the **deed id** (the kind as a lowercase slug, e.g. `first-quadruped-in`), the **witness** names, a one-line **GM note** saying which gates and signals it met, and the **time**. The same sentence is read in the banner. If the GM changes it afterward, keep the original and add an addendum line; never overwrite. Never put a Line, a Veil, or anything from a private survey answer in any of these fields: `state.py loot deeds` prints them.

### 2.3 Anti-farming and anti-exploit rules
1. **The kind closes.** Once a deed kind pays, it is closed for everyone for the rest of the session. Always pass `--deed-id` so rewording cannot dodge the registry.
2. **No variant-splitting.** One act earns at most one Story Box. The same act viewed as "the owner's deed" and "the animal's deed" is one deed.
3. **No asking.** Asking about Story Boxes, or saying out loud that you are doing it for the box, ends the chance for that deed and earns an R0 "Customer Feedback" toast (core §3.5 rule 6, §3.8).
4. **No set-ups.** A pre-arranged deed between players, a deed that only works because the GM nudged, or risk that was neutralised in advance fails G2/G3. Self-harm for loot pays R0 and may draw a complication (core §3.8).
5. **No PvP.** A fight between Crawlers never earns a Story Box.
6. **Retcons.** After the banner, only Caleb can undo a Story Box. A table-consent retcon before the banner simply means no deed happened.
7. **Dying, looting or selling does not reopen it.** Death, revival, looting, trading, selling or a restart never makes a closed deed pay again (§6.3, §6.5).
8. **Pets are not manufactured.** One Enhanced Pet Biscuit per pet, ever; no crafting or duplicating a second one. The Biscuit is tradeable like any Story Box item, but it works only on the pet named in the deed, so a trade never makes a second pet-Crawler.
9. **The cap is the cap.** It is the one hard limit on awards. The GM may override it with a logged reason (Caleb can veto).
10. **Missing record means missing box.** If the deed sentence or a witness line is absent by the end of the session, the Accountant flags it and Caleb decides.
11. **The examples stay secret.** §2.5 and §2.6 are GM-only. Do not paste them into player text, the book, a channel or a banner.

### 2.4 Two special cases (the ones canon gave us)

**The pet-companion case.** Canon paid two different boxes for a cat on Floor 1: one for the person who brought it (Pet Box, with a biscuit) and one for the animal being the first of its kind (Quadruped Box). With a cap of one per floor, the table version is **one pet deed per floor**:
- If the deed is **the owner's act** (carried it through the entry, shielded it, went back for it), award the **Pet Box** (the Enhanced Pet Biscuit, rules/42 §6).
- If the deed is **the animal's own act** (it did something absurd and brave that decided a scene), award the **Quadruped Box** (a crown or collar-type item worn by the animal; example 1, §4.4). The ledger name is the owner Crawler; the item sits on the animal.
- If both happen on the same floor, only the first is a Story Box. The second is paid as a normal Silver box at most (Floor 1 cap in core §4.5) and a Title, logged "story-eligible, capped" so the GM can override the cap with a logged reason (Caleb can veto) or move it to Floor 2 if the deed there is new.
- Bringing a pet to **creation** is not a deed. The deed needs a beat in play where something was at risk (G3). The GM never offers a pet to start the chain (G2).
- Any quadruped counts. A Biscuit-made pet-Crawler is a **separate player-controlled Crawler, played by the player who made it** (the pet's owner, who used the Biscuit). It takes **no extra player slot** and **counts for encounter budgets** like any Crawler (rules/42 §6.2).

**The rival-fight case (canon's family fight, made safe).** Canon's Frank Q killed a relative on the way in (M-233). We do not run that. The one table rule:
- **Opt-in at session zero,** privately, by the player: a **fictional rival** from their backstory (S14), made up with the GM. Never a real person. Never a child. Never another Crawler (**no PvP**).
- The GM does **not** stage the fight (G2). The player brings the rival into play; the deed is a **live fight or confrontation in the first scene or first fight of Floor 1** that the Crawler resolves in a way the table remembers. **No killing:** the rival is beaten, driven off, spared or talked down and walks away alive. A killing blow is not a deed and pays a normal achievement at most.
- If the player's private Lines or Veils (create flow S2) touch family or violence, **do not offer this deed and do not say why.** If the topic comes up in play and trips a Line/Veil, fade it out and pay a normal achievement. The GM obeys opt-outs without showing them (create-flow spec §4.7).
- The canon ring (a curse tied to a death, I-025) is not used. Example 2 in §4.4 is this rule.

### 2.5 Example deeds for a four-player Floor 1 table (GM only)
Crawlers A, B, C, D. Each row is what the GM would log. Floors 1-2 are low-level, so the stakes are small but real.
| # | Deed sentence (as logged) | Why it passes | Box (deed-named) | Card |
|--:|---|---|---|---|
| 1 | "A carried the family goat through the entry and stood over it in the first fight." | First pet in the session; the player chose it (G2); real HP risk (G3); all four saw it (G4) | Pet Box | Enhanced Pet Biscuit (f01-any-0055) |
| 2 | "B's dog dragged the Floor 1 vending machine over a mob to save C." | Absurd, decided a scene, animal's own act | Four Paws Over the Threshold Box | Example 1 |
| 3 | "C met an opted-in fictional rival in the first fight and settled it on camera without killing." | Opt-in; unscripted; the table remembers | Family Reunion, Now Streaming Box | Example 2 |
| 4 | "D talked a named ogre-sized hostile into standing down at 2 HP, using its own contract." | Real risk, creative, witnessed | Talked It Into Quitting Box | Example 3 |
| 5 | "A beat a named Floor 1 hostile using only the room, never raising a weapon." | Creative, risky, not a recipe (the room differs) | Let the Room Do It Box | Example 4 |
| 6 | "A, B, C and D each did one needed job in one improvised plan against the zone's elite." | A table deed (§6.2) | Four-Way Handshake Box | Example 5 |
| 7 | "B carried a wounded stranger NPC across two rooms at 1 HP and refused the shortcut." | Cost paid; says who B is | (hand-made keystone) | Pattern C |
| 8 | "D sat on the trapdoor for the whole fight so the others could finish the puzzle." | Absurd, risky, witnessed, one-time | (hand-made echo) | Pattern A |

### 2.6 Near-misses (pay a normal achievement, Title or R0)
First to kill a boss (that is a Boss Box); cleared a zone; won with a great roll; repeated a previous stunt ("Again? Production has seen this episode."); a deed someone asked about; two players rehearsing a "spontaneous" plan; fighting another Crawler; any deed the GM set up. For a campaign first that fails the gates, "Trailblazing <X>" pays at most a Silver box on Floor 1 (GM principles, Lore audit).

---

## 3. GM procedure (step by step)

Use the Exchange framework: name the player you are addressing, set the spotlight with `python3 tools/discord_gm.py spotlight set "<player>"`, and `spotlight clear` when done. Keep the spoken parts short (Fish budget): banner, one description line, reward.

**Step 1. Notice.** Say nothing. Mark the time in the log. Run the §2.1 gates and signals. If a hard gate fails, stop and pay a normal achievement. If the gates pass but you have no card that fits, say **"Achievement under review by Production"** (core §3.3, Pending Review), finish the scene, and design the item between sessions; deliver it at the next session start. Never improvise a strong item under pressure.

**Step 2. Write the deed.** In the log write the §2.2 record: deed sentence, deed id, witness, GM note. Pick the **box name from that sentence** (a short taunt that names the specific bad idea; roast the choice, never the person; core §4.8). Check the cap (hard) and the spotlight guideline (§6.1): who has a Story Box, who might be next.

**Step 3. Pick the card.** Hand-pick from the Story Box deck, never roll for it. Check the power note against §4.1. Tailor the reskin to the Crawler's hidden Fan Profile if it helps (§5.3). Run `state.py loot story-box ... --dry-run` to see the plan and any warnings.

**Step 4. Announce** (text and voice in the same beat, calm moment: not mid-turn in combat; end of the round at the earliest). The deed is recorded and announced now, at award time; the box is **not** opened now (Step 6). The banner follows the Achievement announcements rule (decision 032: **[GM]** voice for banner + description + Reward punchline; never [SYSTEM]):
```
[GM] New achievement! <Deed Title>.
<one line, second person, what they did, with a jab at the choice>
Reward: You've received a Legendary <Deed Taunt> Box!
```
Pet case:
```
[GM] New achievement! Four Paws Over the Threshold.
You marched a creature with four legs into a building built to eat people. It did not consent. It looks great.
Reward: You've received a Legendary Four Paws Over the Threshold Box!
```
Family case:
```
[GM] New achievement! Family Reunion, Now Streaming.
You met the rival you left behind and finished the argument in front of an audience. Seven million viewers just learned your whole childhood.
Reward: You've received a Legendary Family Reunion, Now Streaming Box!
```
**Step 5. Hold the box.** The box goes into the Crawler's System Inventory **unopened**, with one snarky hold line (no dice) under **[GM]** (decision 032):
`[GM] Box held. Production will open it in a saferoom, where the lawyers can watch.`
Then let the table react for one beat and play on.

**Step 6. Open in the next saferoom** (Caleb, 2026-10-04: loot boxes, Story Boxes included, can ONLY be opened in a saferoom; core §4.4 is unchanged). If the Crawler dies first, the unopened box is reclaimed with their other unopened boxes (core §6.2); the deed stays recorded (no second payout) but the box no longer counts toward the cap, so another Crawler can be awarded one (§6.3). At the opening give one beat of suspense, one snarky line under **[GM]**, no dice (the contents are already chosen; do not fake a roll):
`[GM] Opening. Production asks the audience to hold its applause. The audience declines.`
Then read the item the way rules/40 §2.5 says, with the power note's player-visible parts:
```
+ <reskin_name>
  <real_5e_name> (<rarity>): <plain_mechanics.text>
  Power: <what it cannot do; what is locked and when it unlocks>
  Story value <n> (provenance, not credits). Tradeable: it can be traded, looted or sold.
  "<snark_line>"
```
A Story Box holds **one headline item** and at most **one small extra** (a Bronze-value consumable or a clue). It never holds credits or a stat bump.

**Step 7. Record at award time** (right after the banner; do not wait for the saferoom). Run it for real, copying the §2.2 text exactly (until the Architect adds `--hold`, §10, record the award and open it in the saferoom with the same command):
`python3 tools/state.py loot story-box 1 any --crawler <name> --pick <card_id> --deed "<sentence>" --deed-id <slug> --witness "<names>" --gm-note "<gates met>" --when "<time>"` (add `--override-cap "<reason>"` when the GM overrides the cap; the reason is logged and Caleb can veto).

**Step 8. Ledger lines.** Three things must exist after Step 7:
1. **Box ledger** (`story-box`): deed, deed id, witness, floor, card, box name, status (`held` until opened, then `opened`), override reason if any.
2. **Loot ledger:** `economy_value 0`, `story_value <n>`, `pick: true`, `override: GM pick`.
3. **Credit ledger:** **no line at award** (credits unchanged; story value never converts). The Accountant reports story value on its own line and leaves it out of the 1,500 flag. A later sale is a normal credit line (§6.5).

**Step 9. Sheet card** (when the box is opened). The publisher posts the change post to the Crawler's channel: the item line with its mechanics, the visible power line and the unlock line; `exports/card-data.json` carries the item text (the tool writes it). Add the achievement to the card (`ACHIEVEMENTS: <name> - Legendary <Box> (<item>)`) and, if you like, the deed name as a cosmetic Title. Hidden notes (`trigger_deed`, hook, Fan Profile reasons) never go on the card.

**Step 10. Hand back.** Say aloud who has the spotlight next (Exchange framework). Give the other three Crawlers their **spotlight return** within the session (§6.1). Note in the log: cap used for floor 1, spotlight guideline now reads <names without one>.

---

## 4. The power ladder

### 4.1 Rules for the power note
1. **Legendary in story, small in numbers.** The box is Legendary. On Floors 1-2 the item's **numbers** must sit within the floor ceiling (core §3.6: default Common, peak Uncommon).
2. **Four rungs.** Rung 0 **Story only** (no numbers). Rung 1 **Utility** (no damage; one problem solved, at most once per long rest, or once per floor). Rung 2 **Capped edge** (one small combat effect, once per long rest: one Advantage or Disadvantage, or damage no bigger than 1d6, or a DC no higher than 12). Rung 3 does not exist on Floors 1-2.
3. **Rarity label follows the numbers.** An item with any combat number is labelled Common or Uncommon. A story-only item may carry any label, because it has no numbers.
4. **Never, on Floor 1-2:** a permanent bonus to AC, saves, attack, damage, spell DC, an ability score, hit points or speed; an extra action, attack or reaction; healing or a revival effect (rewards never change dice, DCs, damage, saves or revives); credits; a stat bump; attunement.
5. **Budget.** A permanent Story Box item uses the holder's one permanent magic item for the floor (core §3.7: Floors 1-2, 0-1). A consumable one (Biscuit, Truce Chit) counts as one R3 consumable. Neither is "free on top".
6. **The deed is the manual.** The item does one thing, and that thing is what the Crawler did. No generic bonuses.
7. **A hook, not a penalty.** Each card has a story cost: the rival knows your name, the audience is watching, the room is now a suspect. The hook never lowers the Crawler's numbers.
8. **Locks and scaling.** Anything stronger than rung 1-2 is **dormant** and written on the card with its unlock: a level (3) or an arrival (Floor 3). Unlocks come in **named steps**, never as free growth, and the new step must fit the new floor's ceiling. Dormant parts count for nothing until they wake; the GM re-checks the budget then.
9. **Two tests.** *Swap test:* if a different Crawler held it, would it break a level 1-2 fight? *One-roll test:* used every encounter all floor, does it change an outcome by more than one die roll?
10. **The holder uses it.** Story Box items are not bound (Caleb, 2026-10-04): lending, gifting, trading, looting and selling are allowed, and whoever holds the item can use it within its own limits (a companion item still needs its companion). Payouts already made for the deed (Heroic Inspiration, a pet made a Crawler) stay with the Crawler who earned them and never repeat. The item counts against the holder's budget (rule 5), and dormant unlocks follow the holder's level.

### 4.2 Three design patterns
| Pattern | Idea | Floor 1 shape | Grows by | Examples |
|---|---|---|---|---|
| **A. Echo** | The item does the deed's one move, in miniature, once per rest. | Rung 1-2, uses 1 per long rest | Never on Floors 1-2; Floor 3+ step by story | 2, 4 |
| **B. Seed** | A small thing now with a written unlock. | Rung 1; strong parts dormant | Level 3, then Floor 3 | 1 |
| **C. Keystone** | A one-time change in the story, not in the numbers. | Consumed or spent once, no numbers beyond a short duration | Does not grow; it ends | 3, Biscuit |
| (Trophy) | Rung 0: a keepsake or table prize with a small perk. | Story or navigation only | None | 5 |

### 4.3 Power note format
In `notes`, as one line the Accountant can read: `power_note: <class>, rung <0-2>; <what it cannot do>; <locked: what, unlocks when>; Hook: <story cost>`. The player-visible half goes into `plain_mechanics.limits` (what it can't do and when the locked part wakes). `trigger_deed:` goes on its own line in `notes`. Any card without `power_note:` earns a tool warning.

### 4.4 Five worked cards (loot-deck schema `loot-deck/0.1.2`; all HOUSE or CANON-INSPIRED)
`credit_value` is 0 on every card; `story_value` is **provenance only** (Legendary band, rules/40 §3.2, kept at the low end; never a price or a buyback base); `sale_value` is the fixed System buyback for the card's power rung (§4.6); `bound` is `false` (tradeable, lootable, sellable; Caleb, 2026-10-04); `draw_weight` is 0 (hand-pick). Ids `f01-any-0061` to `0065` are proposals (Lore's deck ends at 0060). The card for the Pet Box is the existing Biscuit, `f01-any-0055`; §4.5 gives its power note.

**Example 1: Little Crown, Four-Paw Fit**
```json
{ "id": "f01-any-0061", "floor": 1, "zone": "any", "tier": "Legendary", "box_types": ["any"], "pull_type": "weird",
  "kind": "item", "reskin_name": "Little Crown, Four-Paw Fit", "real_5e_name": "Circlet of the Crowd (house: quadruped charm crown)", "source_5e": "HOUSE", "rarity": "Uncommon", "attunement": null, "category": "Misc",
  "plain_mechanics": { "text": "Worn by one quadruped companion (resizes to fit; no attunement). Once per long rest, when the wearer or its owner meets a creature that has not met either of them, one of the two may make one Charisma (Persuasion or Performance) check with Advantage; say so before rolling. Dormant part: at owner level 3 it gains a second use per long rest. No effect on attacks, saves, AC or damage.",
    "action_cost": "none", "range": "30 ft (wearer and owner within 30 ft of each other)", "damage": null, "save_dc": null, "duration": "one check", "uses": {"max": 1, "recharge": "long rest"},
    "limits": "Quadruped wearer only. Second use stays locked until the owner is level 3. If the companion dies, the crown is ordinary loot.", "weight_lb": 0.5 },
  "spoken_line": "Little Crown, Circlet of the Crowd. Once per rest, the wearer or its owner rolls one Charisma check with Advantage.",
  "snark_line": "Four legs, one crown, zero understanding of taxes. The audience has already voted.",
  "reward": "Little Crown, Circlet of the Crowd. Once per rest, the wearer or its owner rolls one Charisma check with Advantage.",
  "canon_status": "CANON-INSPIRED", "credit_value": 0, "story_value": 30000, "sale_value": 250, "bound": false, "draw_weight": 0, "unique": true, "tailor_tags": ["pets"], "exclusive_to": null, "grant": null,
  "ledger": {"type": "item", "text": "item +1 Legendary Story Box: Little Crown, Four-Paw Fit (story value 30000)"},
  "box_name": "Four Paws Over the Threshold Box", "deed": "Brought a four-legged companion into the Crawl and got it through the first fight alive",
  "notes": "Canon basis: ledger L-001, A-165 (Legendary Quadruped Box, first cat in; Donut), I-014. Pattern B (Seed). trigger_deed: first quadruped companion (any four-legged creature, not only a cat) that enters the Crawl with a Crawler at the table AND gets through a first fight alive because of a risk its owner or the animal took; GM judged. power_note: Utility, rung 1 now; rung 2 later by named step only (level 3: second use). One social Advantage per rest, no combat numbers. Hook: the audience adores the wearer, and anything hostile that likes crowns can notice it. Recipient: the owner Crawler is the ledger name; the item sits on the companion." }
```

**Example 2: Grudge Pin, Enamel (Family Reunion 2019)**
```json
{ "id": "f01-any-0062", "floor": 1, "zone": "any", "tier": "Legendary", "box_types": ["any"], "pull_type": "weird",
  "kind": "item", "reskin_name": "Grudge Pin, Enamel (Family Reunion 2019)", "real_5e_name": "Pin of Settled Scores (house: grudge charm)", "source_5e": "HOUSE", "rarity": "Common", "attunement": null, "category": "Misc",
  "plain_mechanics": { "text": "Pin worn on clothing (no attunement). When you earn it, name one fictional rival from your backstory (never a real person; the GM approves the name). While you can see that rival or anyone acting for them, you have Advantage on saving throws against being Frightened. The first time the table plays out that rival being beaten without being killed, spared or forgiven, you gain Heroic Inspiration, once ever; after that the pin is a keepsake with no effect.",
    "action_cost": "none", "range": "self", "damage": null, "save_dc": null, "duration": "while the rival is in view", "uses": {"max": 1, "recharge": "none"},
    "limits": "PvP never counts and the rival is never another Crawler. The GM may swap the rival for a different fictional one at any time, without giving a reason. The Inspiration is a one-time payout, paid once ever to the Crawler who earned the deed; if the pin changes hands, the new holder keeps only the fear-save edge against that rival.", "weight_lb": 0 },
  "spoken_line": "Grudge Pin, Pin of Settled Scores. Advantage on fear saves near your rival, and Inspiration when the score is settled.",
  "snark_line": "Nothing says family like a signed waiver. The audience is eating this up with a spoon.",
  "reward": "Grudge Pin, Pin of Settled Scores. Advantage on fear saves near your rival, and Inspiration when the score is settled.",
  "canon_status": "CANON-INSPIRED", "credit_value": 0, "story_value": 25000, "sale_value": 250, "bound": false, "draw_weight": 0, "unique": true, "tailor_tags": ["rivals"], "exclusive_to": null, "grant": null,
  "ledger": {"type": "item", "text": "item +1 Legendary Story Box: Grudge Pin, Enamel (story value 25000)"},
  "box_name": "Family Reunion, Now Streaming Box", "deed": "Faced a fictional rival in the first fight of the Crawl and settled the score on camera",
  "notes": "Canon basis: ledger A-167 (Legendary That's the Spirit! Box, entering while fighting a family member; Frank Q), I-025. Content: HOUSE reframe, opt-in at session zero, a fictional rival NPC, no killing, no PvP, nothing cursed. Pattern A (Echo). trigger_deed: the Crawler enters or begins Floor 1 in a live fight with an opted-in fictional rival from the backstory and resolves it without killing in a way the table remembers; never staged by the GM, never PvP. power_note: Story plus one small save edge (rung 1); the Inspiration is a single one-time payout and then the pin goes inert. Hook: the rival now knows the Crawler by name." }
```

**Example 3: Laminated Truce Chit (Do Not Fold)**
```json
{ "id": "f01-any-0063", "floor": 1, "zone": "any", "tier": "Legendary", "box_types": ["any"], "pull_type": "weird",
  "kind": "consumable", "reskin_name": "Laminated Truce Chit (Do Not Fold)", "real_5e_name": "Truce Chit (house: one-shot parley)", "source_5e": "HOUSE", "rarity": "Uncommon", "attunement": null, "category": "Consumables",
  "plain_mechanics": { "text": "Utilize action, once: hold it up to one creature you can see within 30 ft that has Intelligence 6 or higher, is hostile, and has not yet attacked this scene. It must hear you out: for 1 minute it will not attack you or your allies and will talk if it can. This ends at once if you or an ally hurts or threatens it. The chit is spent.",
    "action_cost": "Utilize action", "range": "30 ft", "damage": null, "save_dc": null, "duration": "1 minute", "uses": {"max": 1, "recharge": "none"},
    "limits": "Not usable on a floor boss, on a creature already in a fight with you, or on anything with Intelligence 5 or lower. It buys a conversation, not a win: the usual checks still apply to what is said.", "weight_lb": 0 },
  "spoken_line": "Laminated Truce Chit, a house parley token. One use: one smart hostile creature must hear you out for one minute.",
  "snark_line": "Valid for one conversation. Void if you say 'but hear me out' twice.",
  "reward": "Laminated Truce Chit, a house parley token. One use: one smart hostile creature must hear you out for one minute.",
  "canon_status": "HOUSE", "credit_value": 0, "story_value": 20000, "sale_value": 250, "bound": false, "draw_weight": 0, "unique": true, "tailor_tags": [], "exclusive_to": null, "grant": null,
  "ledger": {"type": "item", "text": "item +1 Legendary Story Box: Laminated Truce Chit (story value 20000)"},
  "box_name": "Talked It Into Quitting Box", "deed": "Talked a named hostile out of a fight, with the whole table watching, using its own rules against it",
  "notes": "Pattern C (Keystone). trigger_deed: a named Floor 1 hostile (not a floor boss) that was about to fight stands down because of the Crawler's words and plan, first time at the table, risk real (low HP, no escape), witnessed. power_note: Story keystone, single use, no numbers beyond 1 minute; floor bosses excluded. Hook: the creature remembers who talked to it. Tradeable consumable; if unused it carries to the next floor." }
```

**Example 4: Annotated Floor Plan (Coffee Ring Included)**
```json
{ "id": "f01-any-0064", "floor": 1, "zone": "any", "tier": "Legendary", "box_types": ["any"], "pull_type": "weird",
  "kind": "item", "reskin_name": "Annotated Floor Plan (Coffee Ring Included)", "real_5e_name": "Plan of Unfair Advantage (house: environment charm)", "source_5e": "HOUSE", "rarity": "Uncommon", "attunement": null, "category": "Misc",
  "plain_mechanics": { "text": "Folded plan carried in your System Inventory (no attunement). Once per long rest, when you use a Utilize action on part of the room (a trap, door, shelf, light, vending machine) against a creature, that creature has Disadvantage on the first saving throw it makes against that effect. The effect must be something the room already offers; the plan adds no damage and no new effect.",
    "action_cost": "None (passive)", "range": "as the Utilize action", "damage": null, "save_dc": null, "duration": "one saving throw", "uses": {"max": 1, "recharge": "long rest"},
    "limits": "One use per long rest, never on a floor boss. The GM decides what the room offers.", "weight_lb": 0 },
  "spoken_line": "Annotated Floor Plan, Plan of Unfair Advantage. Once per rest, a room trick you use gives its target Disadvantage on its first save.",
  "snark_line": "Every coffee ring marks a trap that worked. The cleaning staff has stopped asking.",
  "reward": "Annotated Floor Plan, Plan of Unfair Advantage. Once per rest, a room trick you use gives its target Disadvantage on its first save.",
  "canon_status": "HOUSE", "credit_value": 0, "story_value": 30000, "sale_value": 500, "bound": false, "draw_weight": 0, "unique": true, "tailor_tags": ["traps"], "exclusive_to": null, "grant": null,
  "ledger": {"type": "item", "text": "item +1 Legendary Story Box: Annotated Floor Plan (story value 30000)"},
  "box_name": "Let the Room Do It Box", "deed": "Beat a named Floor 1 hostile using only the room, never raising a weapon",
  "notes": "Pattern A (Echo). trigger_deed: first Crawler at the table to defeat or drive off a named hostile using only the environment, without a weapon attack or spell of their own, at real risk. power_note: Capped, rung 2: Disadvantage on one save per long rest, no damage dice, no DC, no new action. Hook: the room is now a suspect; the System starts moving the furniture." }
```

**Example 5: Group Photo, Mid-Handshake (Framed)**
```json
{ "id": "f01-any-0065", "floor": 1, "zone": "any", "tier": "Legendary", "box_types": ["any"], "pull_type": "weird",
  "kind": "item", "reskin_name": "Group Photo, Mid-Handshake (Framed)", "real_5e_name": "Keepsake of the Four (house: table-deed trophy)", "source_5e": "HOUSE", "rarity": "Common", "attunement": null, "category": "Misc",
  "plain_mechanics": { "text": "Framed photo held by one Crawler (the table picks the holder; the GM default is a Crawler without a Story Box yet). While all four pictured Crawlers are alive and within 1 mile of each other, each of them always knows the compass direction to the others. Once per floor, the holder may ask the System to replay the moment in the photo: a free recap of who stood where when the plan began. No combat effect.",
    "action_cost": "none", "range": "1 mile", "damage": null, "save_dc": null, "duration": "while all four are alive", "uses": {"max": 1, "recharge": "none"},
    "limits": "A dead pictured Crawler shows in grey and drops out of the direction sense. A replacement Crawler is not in the photo. Story and navigation only.", "weight_lb": 1 },
  "spoken_line": "Group Photo, Keepsake of the Four. While all four of you live, each always knows the direction to the others.",
  "snark_line": "Everybody smile. Production wants this on the poster. Production has already chosen the poster.",
  "reward": "Group Photo, Keepsake of the Four. While all four of you live, each always knows the direction to the others.",
  "canon_status": "HOUSE", "credit_value": 0, "story_value": 20000, "sale_value": 100, "bound": false, "draw_weight": 0, "unique": true, "tailor_tags": [], "exclusive_to": null, "grant": null,
  "ledger": {"type": "item", "text": "item +1 Legendary Story Box: Group Photo, Mid-Handshake (story value 20000)"},
  "box_name": "Four-Way Handshake Box", "deed": "All four Crawlers carried out one plan, each with a different job, and it worked",
  "notes": "Table deed (rules/45 section 6.2): counts as the one Story Box deed of every Crawler named in the deed line; the GM names all four in --witness and logs the other three as sharing it. Pattern: Trophy (rung 0 plus a navigation perk). trigger_deed: all four Crawlers each did a distinct, necessary part of one improvised plan against something above their weight, unscripted, with real risk. power_note: Story and navigation only, no combat numbers. Hook: if one Crawler dies, the photo greys them out where everyone can see." }
```
### 4.5 Power note for the existing Enhanced Pet Biscuit (card f01-any-0055, rules/42 §6.3)
Add this line to the end of that card's `notes` (Syndicate/Lore apply it; this file does not edit rules/42):
`power_note: Story keystone (pattern C), consumed once, rung 0 numbers: the new Crawler is a CR 1/4 Beast stat block plus a class at party level, so it adds a Crawler to encounter budgets and uses the owner's one consumable for the floor. Tradeable like any Story Box item but usable only on the pet named in the deed; cannot be duplicated; one conversion per living pet-Crawler (a deleted pet-Crawler frees its conversion; a new one needs a new biscuit). The new Crawler is a separate player-controlled Crawler played by its owner's player, with no extra player slot. Hook: the pet now has opinions, and the audience adores it.`

### 4.6 Sale value (System buyback) by power rung
Story Box items sell. The System's buyback is a **fixed `sale_value` per power rung**, written on the card. **`story_value` is provenance only and is never a price, a buyback base or a trade-in credit.**

| Rung (§4.1) | `sale_value` (Floor-1 scale) | Cards |
|---|--:|---|
| 0 Story only | 100 | Group Photo (example 5), Enhanced Pet Biscuit `f01-any-0055`, Pet Biscuit Crate `f01-any-0060` |
| 1 Utility | 250 | Little Crown (example 1), Grudge Pin (example 2), Laminated Truce Chit (example 3) |
| 2 Capped edge | 500 | Annotated Floor Plan (example 4); Lore's cards `f01-any-0056` to `0059` are treated as rung 2 (500) until they are retuned |

1. **A System fee.** The buyback is paid by the System, so it multiplies by the **credit multiplier of the floor where the sale happens** (core: x1 F1-4, x5 F5-9, x20 F10-14, x50 F15-18), exactly like repair prices (rules/50 §1.2). Box credit pulls do not get that multiplier (rules/40 §3.2).
2. **Sales between Crawlers are free-form:** any price, or none. They are logged as an ordinary credit transfer between the two credit ledgers, with `story_value` kept as provenance in the note (§6.5).
3. A card without `sale_value` is read as its rung from the `power_note:`; the Architect's tool may default to 500 and warn.

---

## 5. Story Box vs Benefactor Box; achievements; Fan Profile

### 5.1 Story Box vs Benefactor Box
| | **Story Box** | **Benefactor Box** (core §4.7) |
|---|---|---|
| Who sends it | The System, for a deed (box name taken from the deed) | A sponsor; no Crawler deed needed |
| Trigger | One named, unscripted, witnessed, one-time deed | A sponsor's whim, a deal or a rider (§5.2 of core) |
| Floor ceiling | Stays inside it: small numbers, Legendary label on the box | **May exceed it**: off-world tech, glitchy gear |
| Power | Capped by §4.1 (rungs 0-2 on Floors 1-2) | Not tied to tier; a Bronze one can beat a Gold ordinary box |
| Value | `story_value` (provenance only, never a price) plus a fixed `sale_value` by rung (§4.6); the award is excluded from the 1,500 flag, a sale is not | Ordinary `credit_value`; counts in the economy audit |
| Trade | Box is bound until opened (core §4.4); the opened item trades, loots and sells (§6.5) | Box is bound until opened (core §4.4); contents then trade as ordinary items |
| Cap | One per table per floor (GM override with a logged reason; Caleb can veto) | About one per sponsor per floor; outside the pacing table |
| Contents | One hand-made item that echoes the deed | Odd items, gadgets, a rider |
| Who picks | GM, hand-pick only | GM; sponsor's style |
The room chose **not** to route Story Boxes through Benefactor Boxes (rules/40 Q9, option B): a Benefactor Box has no deed and would break the "named deed" rule.

### 5.2 How a Story Box relates to achievements
- A Story Box is always the reward of a **new, named achievement** (`NEW:<name>`), never a catalog row. Log it `ACH | <crawler> | NEW:<name> | R6-Story | Legendary <Box> | F1/<session>` (core §3.8). It is the Crawler's one **Headliner** (R6, 0-1 per floor, core §3.7) delivered in a box.
- **One act, one box.** Other toasts for the same act pay R0 only ("Production has seen this episode"). A Story Box does not count toward the §4.5 box table or the Floor 1 cap of two achievement boxes per Crawler (GM principles); it does count as the Crawler's Headliner.
- After a Story Box, that Crawler's small toasts go **snark-only for the rest of the session** (the spotlight-balance rule).
- Rewards never change dice, DCs, damage, saves or revives, and never touch the secret affinity or quirk systems (GM principles). Every Story Box card honours that (§4.1 rule 4).

### 5.3 Fan Profile tailoring (allowed, because it is a hand-pick)
- Tailor the **item, not the power** (core §3.5 rule 3). The Fan Profile (hidden; built by the System from the S13 private survey notes and from play; players never see it) may choose the reskin, the form and which pattern fits the build. The ladder, not the profile, sets the numbers.
- **Build-aware, never build-servile.** A talker gets the Truce Chit; a trapper gets the floor plan. The hook should be a story the Crawler would not have picked.
- **No pettiness.** A Story Box is a reward; never tailor it against a Crawler who annoyed the System.
- **Do not expose the private data.** Never quote a survey answer ("you told us..."), never name a Line, Veil or any opt-out in the banner, the deed line, the witness line, the GM note, the ledger or the card. If a tailored reskin or hook would touch an opt-out, **swap it silently** and say nothing. `tailor_tags` on Story cards carry broad themes (`pets`, `traps`, `rivals`), never survey text.
- The create flow no longer asks for public tags (create-flow spec v0.1.2); rules/40 §1.1 and §2.4 still say "public Fan Profile" and need that wording updated by Syndicate (§8).

---

## 6. Spotlight guideline, looting, trading, death, resale, and the beta reset

### 6.1 Four Crawlers: the spotlight guideline (GM guidance, not a hard rule)
The **cap is the only hard rule**: at most one Story Box per table per floor, which the GM may override with a logged reason (Caleb can veto). Everything else in this section is GM guidance.
1. **Spotlight guideline: try to give every living Crawler a first Story Box before anyone gets a second.** If a deed would give a second box to a Crawler while others have none, the GM may still award it (cap permitting) and logs one line saying why, or may pay a normal reward (Silver at most on Floor 1) plus a Title and log "story-eligible, capped". A deed pays once: Story Box or normal, not both.
2. **Tie-breaks for who earns it** when two Crawlers qualify at once: (a) the one who took the bigger risk; (b) the one with no Story Box yet; (c) the one who has opened fewer boxes this floor; (d) the table votes. No dice.
3. **Spotlight return.** When one Crawler gets a Story Box, try to frame a spotlight scene for each of the other three in the same session and pay any earned notable moment (Heroic Inspiration, a consumable, a Title). Those are earned, not gifted.
4. **The item is small on purpose** (§4.1), so the holder is not ahead in power.
5. The GM keeps `spotlight: <names without one>` in the log after every award.
6. **Duplicate-theme pairs: at most one box per pair.** These cards reward the same deed, so one award uses one card (or, for the Pet Box, the one two-card box) and never both as separate boxes: **0055 / 0060** (Pet Box: Enhanced Pet Biscuit + Pet Biscuit Crate; awarded together as ONE box with `--pick f01-any-0055,f01-any-0060`, the existing "same box" rule), **0056 / 0061** (a four-legged companion: Quadruped Box vs Four Paws Over the Threshold) and **0057 / 0062** (a fictional rival: That's the Spirit! vs Family Reunion, Now Streaming). Pick the card whose wording fits what happened.

### 6.2 Shared deeds
- **Table deed** (every active Crawler, or all but one plus a witness; so a four-player table needs all four or three plus a witness, and a two-player table needs both, or one plus a witness): it pays **one** box. The GM names every contributor in `--witness`; each gets a Title; **all of them count as having had their Story Box** for the spotlight guideline. The holder is chosen by the §6.1 tie-breaks; the item is built to help the whole table (example 5).
- **Pair deed** (two Crawlers): the box goes to the one who took the bigger risk; the partner gets a Title and Heroic Inspiration; only the holder counts for the spotlight guideline.
- **Simultaneous deeds:** the first one in the log wins; the other becomes a normal achievement.
- **Pets:** the owner's player gets the box; the item may sit on the animal (example 1).

### 6.3 Death, revival, leaving, theft
Caleb (2026-10-04): death is nearly game over, and Story Box items are **not bound**. They are lootable from corpses, transferable and sellable, as in canon. Revival stays very costly and rare (core §6); nothing here is a free second chance.

| Event | The item | The deed and the cap |
|---|---|---|
| Crawler dies (Canon Hard, Costly Revives or Soft Open) | An opened item is **ordinary loot**. It drops in the corpse cache with the rest of System Inventory (core §5.9, §6.2) and the party, or anything else, may take it, trade it or sell it. No repossession, no reissue. A Dead Crawler Card (core §6.9, cosmetic) may name the deed | The deed stays closed. For an opened or already-awarded item the cap slot stays used until the dead Crawler is deleted (§1.2 row 5). The dead Crawler leaves the spotlight list |
| Unopened Story Box at death | Reclaimed by the System like every unopened box (core §6.2; boxes are bound until opened, §4.4). A box held for the next saferoom is at risk until then | The deed was recorded at award time, so it stays closed (no second payout for it). **The box is gone and the Story Box slot is freed (Caleb, 2026-10-04):** it no longer counts toward the per-floor cap or the "one per living Crawler" counting, so the GM may award another Crawler one. No replacement box for the dead Crawler. The ledger row for the reclaimed box is the Accountant's / Lore's (Lore handles the card side; the Accountant tracks it), not the GM's |
| Soft Open (Syndicated) | The Crawler returns at the next saferoom; the item stays where it dropped (core §6.2). The party may hand it back | Same |
| Floor 1 Reprieve | Keeps everything | Same |
| Revived (Voucher or Rare Offer) | **No reissue.** The item is wherever it ended up; the party may hand it back if they kept it | No second payout. Back on the spotlight list in their old place (they count as having had one) |
| Replacement Crawler | Fresh sheet (core §6.3); the party may hand them the item (it is tradeable) | Closed deed stays closed; joins the spotlight list as "none yet" |
| Player leaves; Crawler retired or made an NPC ally | The item stays in that Crawler's inventory like any ordinary item; the player may hand it to the party before leaving | Cap slot stays used. The Crawler drops off the spotlight list |
| Companion holder dies | Ordinary loot on the body; the owner keeps the deed | No replacement item |
| Owner dies, companion lives | The companion keeps what it wears unless someone takes it, and becomes a GM-run NPC | None |
| Stolen, disarmed or taken | Ordinary theft and disarm rules apply; the System does not return it | None |
| Traded or sold | Goes to the new holder (§6.5) | No new payout |
| Going downstairs | Items persist across floors; locked parts wake as written | The next floor has its own cap |

### 6.4 What the beta (a new session) resets
Everything the **session** owns starts empty: the deed registry (`story-box` ledger), the cap counters, the spotlight list, the loot ledger, the story-value totals, the unlock progress, and the `unique` flags. The four beta Crawlers are new people: **no item, deed, Story Box or story value carries over from alpha**, and an alpha deed does not close a beta deed ("first of its kind" means first in that session). Deck files are session-agnostic (rules/40 §2.7), so the same cards are available again in beta. The Accountant reports story value per session. Alpha's boxes stay in alpha's reports. ("Session" here is the campaign instance, alpha or beta. The cap is **per floor** across all play nights of that instance, not per play night.)

### 6.5 Looting, trading and selling (resale note)
1. **Looting.** An opened Story Box item sits in System Inventory and drops with the corpse cache (core §5.9). A looter earns no deed and no payout; the item simply has a new holder.
2. **Trading and gifting.** Free-form, at any price including none. Log it as an ordinary credit transfer between the two credit ledgers (`reason: Story Box sale: <item>`), with the card's `story_value` and the original deed id kept as provenance in the note.
3. **Selling to the System.** Fixed `sale_value` by power rung (§4.6) times the credit multiplier of the floor where the sale happens. It is an ordinary credit-ledger line (`reason: Story Box buyback: <item>`) with `story_value` kept as provenance. `story_value` is never the price.
4. **The Accountant bites the bullet.** Sale proceeds are normal credits and count toward the 1,500-per-floor inflation flag like any other credits. The Accountant **flags it, not blocks it**: the sale goes through and the flag appears in the report.
5. **No reopening.** A sale, trade or loot never reopens the deed or the cap, and never pays a second deed payout.
6. **Unopened boxes cannot be traded or sold** (core §4.4); only the opened item can.

---

## 7. Core amendment text (applied to core v0.2.8)

> **Note (v0.2.4):** the quote below is the text as first applied. Since core v0.2.17 the cap override reads "the GM may exceed it with a logged reason; Caleb can veto" (Caleb's ruling, 2026-10-04).

The one line, placed in core §4.1 (after the floor-ceiling paragraph), §4.5 (under the table) and §4.7 (a new "Story Box" row):

> **Story Box exception** (HOUSE; Caleb, 2026-10-04): one Legendary Story Box per table per floor (a logged override by Caleb may exceed it) is allowed on Floors 1-2, hand-picked by the GM for a single named one-time deed (recorded and announced at award time; the box is held unopened until a saferoom, §4.4 as written). Once opened, the item is ordinary loot: tradeable, lootable from a corpse and sellable (fixed System buyback by power rung; `story_value` is provenance, never credits). Its power note keeps its numbers inside the floor ceiling (§3.6); it sits outside the §4.5 pacing table and does not touch the Celestial cap. Full rules: `rules/45-story-boxes-5e.md`.

Celestial rules (one per Crawler, DM-gated) are unchanged. Rules/40 §2.8 stays as the short rule; this file is the design that wins on detail.

---

## 8. For the Architect: what exists, what is missing
Read from `tools/state.py` `loot story-box` and `tools/loot.py` (not edited):
- **Exists:** hand-pick only, `--deed` (8+ characters), `--deed-id`, `--witness`, `--gm-note`, `--when`, `--override-cap`, `--dry-run`, cap per floor (counted in the campaign instance's ledger), deed registry per session (a deed key pays once), `bound` and `story_value` on the loot line, credits untouched, warning when `power_note:` or a witness is missing, `loot deeds`, `loot totals` (economy and story separately).
- **Missing or suggested:** (1) make `--deed-id` required (without it the key comes from the card's `deed` text, and rewording can dodge it); (2) `--box-name` so the banner can use the deed's wording; (3) the rota check (§6.1) is now a guideline: warn only, never block (drop the `hard` option of `limits.story_box_rota`); (4) `--shared-with A,B,C` for table deeds (§6.2); (5) the `--repossess` and `--restore` paths are dropped: there is no repossession and no reissue after revival (§6.3); (6) warn when `trigger_deed:` is missing; (7) a `--hold` pending state is now required (Caleb picked saferoom-only opening). See §10 for the full change list.
- **Existing deck vs the ladder (§4.1):** `f01-any-0056` (+2 Intelligence checks and a poison rider), `f01-any-0057` (Rare, attunement, can't regain hit points) and `f01-any-0059` (+1 maul) break rule 4; `f01-any-0058` (DC 13) is over the rung 2 DC cap; `f01-any-0060` is fine. Lore/Syndicate to retune before use. This file does not edit the deck.
- **Wording to fix elsewhere (not done here):** rules/40 §1.1 `tailor_tags` ("Public Fan Profile hooks only") and §2.4 ("public Fan Profile") still imply public tags; rules/40 §2.8 should point to this file.

---

## 9. Open question for Caleb (1 open; 5 answered 2026-10-04)

**Still open: how strong are Story Box items on Floors 1-2?** The ladder (§4.1: rungs 0-2, at most one small Advantage/Disadvantage, 1d6 or DC 12, once per rest; strong parts locked until level 3 or Floor 3) stays the **GM default** until Caleb says otherwise. The alternative is story-only items. Lore's cards `f01-any-0056` to `0059` are over the ladder (§8) and are left as they are; they count as rung 2 (500) for buyback until retuned (§4.6).

**Answered (Caleb, 2026-10-04):**
| Old question | Answer | Where it landed |
|---|---|---|
| 1. When does the box open? | Loot boxes, Story Boxes included, open ONLY in a saferoom. Core §4.4 stays as is. The deed is recorded and announced at award time; the box is held unopened until the next saferoom. The "end of scene" option is removed | §1.2 row 9, §3 steps 4-6 |
| 3. Death | Death is nearly game over. Legendary / Story Box items are NOT bound: lootable from corpses, transferable and sellable, as in canon. The named-deed record and no second payout stay. The cap stays used for opened items; an unopened box reclaimed at death frees its slot (v0.2.2) | §6.3, §6.5 |
| 4. Family-fight deed | One rule: opt-in at session zero, fictional rival, no killing, no PvP. Alternatives removed | §2.4 |
| 5. Pet-Crawler | A separate player-controlled Crawler played by the player who made it (the owner). No extra player slot. Counts for encounter budgets | §2.4, §4.5 |
| 6. Is the rota hard? | No. It is a GM guideline ("try to give every living Crawler a first Story Box before anyone gets a second"). Only the per-floor cap with a logged override is hard | §6.1 |
| Buyback (Lore, with Caleb's delegation) | Fixed `sale_value` by rung (100 / 250 / 500, Floor-1 scale, times the sale floor's multiplier). `story_value` is provenance only | §4.6, §6.5 |

---

## 10. Changes for the room
Every spot that must change because Story Box items are tradeable, lootable and sellable, and the box opens only in a saferoom. Line numbers are from 2026-10-04 evening and may have moved; **the Architect was already editing `tools/loot.py` while this was written, so check each line against the current file.** Nothing in `dcc-lore/` or Lore's decks was edited by this change.

### 10.1 DCC Lore (decks and canon files; owner Lore)
| # | Where | Change |
|--:|---|---|
| L1 | `tables/loot-decks/f01-any-story-boxes.json`, cards 0055 to 0060 | `"bound": true` becomes `"bound": false` (tradeable) |
| L2 | Same cards, `ledger.text` | Drop ", bound" from "(story value N, bound)" |
| L3 | Same cards | Add `"sale_value"` by rung: 0055 = 100, 0060 = 100, 0056 to 0059 = 500 until retuned. `story_value` stays as provenance only |
| L4 | Same cards, `plain_mechanics.limits` | Remove "Bound (no sale or trade)", "Bound to the Crawler the party names" and similar. Card 0056 (Tiara): the owner still decides who wears it, but it is no longer bound to the owner. Exact strings: `rules/42-house-items-f01.md` §6.5 to §6.9 |
| L5 | Same cards, `notes` | 0055 and 0060 power notes: replace "Cannot be given away or duplicated" with the rules/45 §4.5 wording. 0055: the new Crawler is a separate player-controlled Crawler, no extra player slot |
| L6 | Card 0057 (Grudge Ring) | Its mark mechanic and the "every player opted into PvP" clause conflict with the rival rule (opt-in at session zero, fictional rival, no killing, no PvP). Retune or hold it; trigger_deed and `deed` text should say "fictional rival", not relative |
| L7 | Cards 0056 to 0059 | Still over the power ladder (§8). Item strength was delegated to Lore on 2026-10-04 (small items on F1-2, strong parts locked to L3/F3); Lore is retuning them, and until done they count as rung 2 for buyback |
| L8 | Deck schema | Optional `sale_value` field (rules/40 §1.1, schema `loot-deck/0.1.2`). A deck that uses it says `loot-deck/0.1.2` |
| L9 | rules/45 example cards 0061 to 0065 | APPROVED by Caleb 2026-10-04 for the deck. Lore adopts them: `bound` false, `sale_value` and the rival wording are already in the proposals |
| L10 | Player guides or catalog text that call Story Box items "bound" or "never sold" | Rewrite to "tradeable, lootable, sellable; value is provenance" |

### 10.2 The Architect (Borent; tools and tool docs)
| # | Where | Change |
|--:|---|---|
| A1 | `tools/loot.py` (docstring, `item_row` where `row["bound"] = True`, totals header "story value (bound, NOT economy)") | Story Box rows get `bound: false`, carry `sale_value` and `story_value` provenance; wording "provenance, NOT economy" |
| A2 | `tools/state.py` `loot story-box` (inventory row `bound`, ledger `"bound": True`, plan text "bound: cannot be sold or traded", announce text "[BOUND] cannot be sold or traded") | Replace with tradeable text; store `sale_value`; plan line shows buyback value |
| A3 | `tools/state.py` `show` (`[BOUND]` tag) and `tools/publisher.py` (`"bound"`, `[BOUND: cannot be sold or traded]`) | No [BOUND] tag on Story Box items; show "Story value N (provenance)" |
| A4 | `tools/state.py` `loot story-box --repossess` / `--restore` and the revive note ("Story Box item(s) are held by the System") | Remove or disable: no repossession, no reissue (§6.3). Corpse-cache looting must carry Story Box items like any item |
| A5 | `tools/state.py` `loot story-box` | Add `--hold`: record the deed, ledgers and card at award time but keep the box unopened in the Crawler's boxes until it is opened in a saferoom; award-time and opened-time events in the `story-box` ledger |
| A6 | Box-opening command | Refuse to open any box outside a saferoom (core §4.4); a held Story Box opens through the normal box-opening path |
| A7 | New: System buyback (for example `loot sell`) | Pays `sale_value` times the credit multiplier of the sale floor (x1/x5/x20/x50); writes a credit-ledger line (`Story Box buyback: <item>`, `story_value` in the note), a loot-ledger line and a `story-box` ledger `sold` event; never pays `story_value`; no deed payout |
| A8 | New or existing give/trade command | Crawler-to-Crawler transfer with optional price; logs an ordinary credit transfer in both credit ledgers with `story_value` and deed id kept as provenance |
| A9 | `limits.story_box_rota` (`DEFAULT_LIMITS`, validation, `loot story-box` rota check, `limits set`) | Warn only; remove the `hard` option; message text becomes "spotlight guideline"; remove "an override never skips the rota" and the "until Caleb rules on open question 6" text; "rota now" in the announce text becomes "spotlight" |
| A10 | Cap wording in `state.py` limits comments, `loot.py` docstring, `tools/README.md` (lines near 179 to 183), `tools/new-session.py`, `gm-notes/31-story-box-how-to.md` | "per floor" (the whole floor, all play nights of that campaign instance), not "per session" |
| A11 | `state.py` `create-crawler` kinds, party cap and encounter budgets | A Biscuit-made pet-Crawler is `kind: pet`: no player slot (already so), **controlled by its owner's player** (add an owner or controller field), and it **counts for encounter budgets** (check the headcount used for budgets) |
| A12 | `tools/tests/test_story_box.py` (fixtures with `bound: True`, rota, repossess and restore tests), `tools/tests/test_loot_ledgers.py` ("Legendary cap + bound") | Update to tradeable items, hold, sale and no repossession |
| A13 | `tools/README.md`, `tools/INDEX.md` (rows for `loot.py` and test_story_box), root `INDEX.md` rows for those tools | Descriptions say "bound" and "rota"; update |
| A14 | `gm-notes/31-story-box-how-to.md` (final, Borent): "item added (bound)", "The item is bound: cannot be sold or traded", cap wording | Rewrite to the rules above. Keep "do not quote story value as money in play" |
| A15 | `decisions/015-story-boxes.md` | Updated by Syndicate in this change; Borent to confirm it matches the tool behaviour |
| A16 | `loot story-box` cap check (v0.2.1, Caleb 2026-10-04) | Count only Story Boxes held by live (non-deleted) Crawlers; ignore archived rows from `/delete` (kept for audit and the Accountant). A dead Crawler that is not deleted still counts when it holds an opened or already-awarded item; a Story Box reclaimed unopened at death does not count (v0.2.2; the reclaim row is the Accountant's / Lore's). See `characters/create-flow-spec-5e.md` §8.4 item 11 |

### 10.3 The Accountant (credit audit and reports)
| # | Where | Change |
|--:|---|---|
| C1 | Ledger rules | Story Box award: still no credit line, `story_value` on its own line (provenance), excluded from the 1,500 flag. Sale or trade: a normal credit line or transfer, with `story_value` and deed id in the note |
| C2 | Inflation flag (1,500 credits per Crawler per floor, rules/40 §3.2) | Sale proceeds count. **Flag it, do not block it.** The report shows the flag; the sale is never reversed |
| C3 | Buyback check | `sale_value` must match the rung table (§4.6) times the sale floor's multiplier; any other price paid by the System is an error. Sales between Crawlers are free-form and never an error |
| C4 | Story value totals | Report by earner and deed; the current holder may differ after loot or trade. A cap override needs the GM's logged reason (Caleb can veto) |
| C5 | Box credit pulls | Do not apply the floor multiplier to box credit pulls (rules/40 §3.2); achievement rewards and System fees (buyback, repairs, crafting prices) keep it |
| C6 | Missing record | Missing deed sentence or witness line at the end of the session is still flagged (§2.3 rule 10) |
| C7 | Reclaimed unopened Story Box (v0.2.2, Caleb 2026-10-04) | When a Crawler dies holding an unopened Story Box, the System reclaims it and the slot is freed. The ledger row for the reclaimed box is the Accountant's / Lore's (Lore: card side; Accountant: tracking). Archived and reclaimed rows are audit-only for the cap |

### 10.4 Others (for completeness)
| # | Who | Change |
|--:|---|---|
| G1 | AI GM (`gm-notes/10-open-threads.md` line near 155: "Hand-pick only, bound, one named deed each...") | Update to tradeable; saferoom-only opening; spotlight guideline |
| G2 | Valtay Corp (player book) | Do not print §2.5 or §2.6; Story Box items are tradeable and lootable; death is nearly game over |

---

## Change log

| Version | Date | Notes |
|---|---|---|
| v0.2.4 | 2026-10-04 | Caleb's ruling (later than decision 018): the rota is a guideline only and the one hard Story Box rule is one per floor, which **the GM can override with a logged reason**; the GM may adapt as play goes; Caleb can veto. Changed in §1.2 row 5, §2.3 item 9, §2.4, the award command, the comparison table, §6 intro, the audit table C4, and a note on §7. Unopened box still bound (core §4.4); item inside tradeable, lootable, sellable. |
| v0.2.3 | 2026-10-04 | Tidy only: `Depends on` pointers refreshed (rules/40 v0.1.7, rules/42 v0.2.3, core v0.2.16, create-flow v0.1.13); "safe room" spelled "saferoom" in prose; "Crawler" capitalized in prose. No rule changed. |
| v0.2.2 | 2026-10-04 | Death rule (Caleb): a Story Box that is still UNOPENED when its Crawler dies is reclaimed by the System and its slot is freed, so another Crawler can be awarded one (per-floor cap and "one per living Crawler" counting). Opened or already-awarded Story Box items are unchanged: lootable, not bound, cap slot stays used until the dead Crawler is deleted. The deed stays closed (no second payout). Also (no Caleb ruling needed, D-6): table-deed wording in §6.2 now reads "every active Crawler, or all but one plus a witness" so it works at a two-player table. Edits: §1.2 row 5, §3 step 6, §6.2, §6.3 two rows, §9 answered row 3, §10.2 row A16, §10.3 new row C7 (ledger row for a reclaimed box is the Accountant's / Lore's). Source: `decisions/020-multiple-crawlers-active-swap.md` v1.2. §6.1 item 6 records the duplicate-theme pairs (0055/0060, 0056/0061, 0057/0062; at most one box per pair). |
| v0.2.1 | 2026-10-04 | Cap count rule (Caleb): deleting a Crawler frees its Story Box slot; the one-per-floor cap counts only Story Boxes held by live (non-deleted) Crawlers, archived ledger rows are audit-only; a dead Crawler not yet deleted still counts. One note in §1.2 row 5, one in §6.3, Architect row A16 in §10.2. The cap itself (one per table per floor, logged override by Caleb only) is unchanged. Source: `decisions/020-multiple-crawlers-active-swap.md`. |
| v0.2 | 2026-10-04 | Caleb's answers (decision 018): tradeable, saferoom-only opening, rota guideline, buyback by rung. |
