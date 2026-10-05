# Pets and Companions (5e Overlay)
Owner: Syndicate | Status: draft | Version: 0.1.0 | Updated: 2026-10-04
Summary: How pets work in the Crawl: a pet is a GM-run SRD Beast of CR 1/4 or lower that a Crawler starts with only if the player wrote it into their own questionnaire free text (nobody is ever asked, prompted, hinted at or offered one); the GM files it on the owner's sheet; no slot, loot, credits or XP; death is final; pets earn no Story Box themselves; the Enhanced Pet Biscuit turns a pet into a pet-Crawler; Good Boy Gulp (pet healing, 50 credits) and the Fold-Flat Kennel (pet carrier, 100 credits) are off-menu items for pet owners only; Assigned Companion compared; what the Architect needs.
Depends on: rules/10-core-rules-5e.md v0.2.11 (§2.4 group size and Assigned Companion, §3.7 pacing, §5.9 System Inventory, §6 death and revival incl. §6.4.7), rules/45-story-boxes-5e.md v0.2.2 (§2.4 pet case, §2.3 rule 8, §4.5 and §4.6), rules/42-house-items-f01.md v0.2.3 (§6 Enhanced Pet Biscuit card f01-any-0055 and Pet Biscuit Crate f01-any-0060), rules/20-crafting-5e.md v0.3.3 (§5.5.3 Heal Critter recipe, §6.3 pets and potions), rules/40-loot-deck-spec-5e.md v0.1.5 (§3.2 price bands), decisions/013-party-size.md, decisions/013-crafting-open-questions.md (answer 4), decisions/018-story-box-answers.md, decisions/019-credit-multiplier-fees.md, decisions/020-multiple-crawlers-active-swap.md, decisions/021-multi-crawler-tooling.md, decisions/022-pets-and-companions.md, characters/create-flow-spec-5e.md v0.1.8 (§8, new §9), tables/item-reskins.json v0.1.4 (Lore; entries `heal-critter-potion`, `pet-carrier`), lore/CANON-LEDGER.md (rows cited in §11). Consumers: AI GM, Borent Corp Systems Architect, the Accountant, DCC Lore, Valtay Corp (book authors: see §2 rule 1).

> **Status:** RULING (Caleb approved the pets rule on 2026-10-04, with the conditions in §2). The file itself is a draft v0.1.0. Item names and prices are filed here; the Accountant's prices are used as given.
> **Project:** *Crawler Protocol: Season Zero*, private fan RPG inspired by *Dungeon Crawler Carl*. Text says **Crawlers**.
> **Tags:** `CANON` = tied to a ledger row; `CANON-INSPIRED` = shaped by canon, mechanics ours; `HOUSE` = our rule. Every canon point below is attributed to a CANON-LEDGER row id and marked **wiki-ledger, not book-checked**. The ledger's own tags are a different thing and are not repeated as claims here. Nothing in this file quotes the novels.

## Contents
1. What a pet is
2. Caleb's conditions: nobody is ever offered a pet
3. Getting a pet: the GM files it
4. The pet at the table
5. Pets and Story Boxes
6. Enhanced Pet Biscuit: pet to pet-Crawler
7. Healing a pet: Good Boy Gulp
8. The Fold-Flat Kennel (Pet Carrier)
9. Pets and floors, safe rooms, encounter budgets
10. Assigned Companion: how it differs
11. Canon basis (ledger rows)
12. What the Architect needs (summary; spec is characters/create-flow-spec-5e.md §9)
13. Open questions (3)
14. Changes for the room
15. Changelog

---

## 1. What a pet is

- A **pet** is a **single SRD 5.2 (2024) Beast of CR 1/4 or lower** that belongs to one Crawler. Any single (non-swarm) SRD Beast of CR 1/4 or lower qualifies (birds, fish, snakes and insects included); water-only Beasts such as the Piranha and Seahorse are GM calls. Swarms, Monstrosities and Celestials are not pets without a GM override. The **GM judges edge cases** (a pack animal, a very large animal that is somehow CR 1/4, a creature that is a Beast only in name). Canon's Lucia Mar arrived with two rottweilers (ledger H-014, wiki-ledger, not book-checked); our table rule is **one pet per Crawler**, and the GM may reskin a mastiff or similar Beast stat block for a rottweiler.
- The **GM runs the pet.** The owner may say what they want it to do; the GM decides what it does and rolls for it.
- A pet takes **no player slot** (decision 013 counts only players), gets **no loot, no credits and no XP of its own**, and is not a Crawler.
- A pet **can die**, and a plain pet's death is **final**: none of the revival rules (core §6.4) apply to a pet. The one canon exception is a story event, not a rule: the Tummy Acher pet return already listed in core §6.4.7 (ledger rows RV-01 to RV-03 as cited there; wiki-ledger, not book-checked) stays a GM-only story beat.
- **Pet-class creature** (a working term, shared with `rules/20-crafting-5e.md` §5.5.3): a pet, companion, familiar, Beast Master beast, Assigned Companion or summoned beast that is not itself a Crawler. **A creature with Intelligence below 2 cannot be a Crawler** by any route at creation; the only way a pet becomes a Crawler is the Enhanced Pet Biscuit (§6), which raises its Intelligence to at least 10 (rules/42 §6.2).

## 2. Caleb's conditions: nobody is ever offered a pet

Caleb approved the pets rule on 2026-10-04 on these conditions. They are rules, not preferences.

1. **No one is asked, prompted, hinted at or offered a pet.** Not in `/create`, not in the questionnaire (S13) or the backstory prompt (S14), not in the book's player chapters, not on the vending wall, not by the GM at session zero.
2. **It is not a freebie.** A Crawler starts with a pet **only if the player thought to write it into their own free text** (a questionnaire answer or the backstory) that they brought a pet. Nothing else starts one. If the text does not say it, there is no pet.
3. **No pet field, checkbox or screen** in `/create` for anyone. The questionnaire contains **no pet question**.
4. The pet items (§7, §8) are **off-menu**: the GM lists them only for a Crawler who already has a pet, on that owner's own card or channel. They never appear on the general vending wall or in player chapters.
5. The feature must be **easy to switch off** (§12 and spec §9: one table setting).

## 3. Getting a pet: the GM files it

1. The GM reads each player's questionnaire free text (S13 answers, S14 backstory) at the **GM review gate** (spec §4.7), the same read the GM already does.
2. If the player wrote that they brought a pet, the GM **judges the fit**: SRD Beast, CR 1/4 or lower, not a creature that cannot be a pet (a swarm, a monster). The GM may decline; if so the GM tells that player privately, plainly, and offers nothing else.
3. If it fits, the **GM files the pet on the owner's sheet** with a GM-run action (spec §9; the Architect names the command). The record holds: name, species (an SRD Beast), a free-text description (the player's own words, trimmed), who filed it, when, status (alive/dead).
4. The pet has **no separate channel and no slot** until the Biscuit (§6). It lives on the owner's Crawler card.
5. The player is told in the fiction only (the GM introduces the animal in play). The GM does **not** announce "pets are allowed" to the table.
6. **Bringing a pet is not a Story Box deed** (rules/45 §2.4): the GM never offers a pet to start the chain.
7. **One pet per Crawler.** A player with several Crawlers (decision 020) may have a pet on each of them if each one's own text said so; a benched Crawler's pet is benched with it. A pet never moves between Crawlers.

## 4. The pet at the table

- **Stat block:** the SRD Beast as written. It does not level and has no class. The GM may rename and reskin it.
- **Death:** the pet dies at 0 hit points (monster rules, no death saves). The GM may let a pet knocked to 0 be left alive if the attacker chose to knock it out. Death is final (§1). Dead pets are marked dead on the owner's sheet; the owner's Crawler gets no credits, boxes or refunds for it.
- **No loot, credits or XP.** Credits, loot and boxes go only to Crawlers. XP (if the table uses XP, core §2.3) is split among Crawlers only; the pet is not counted in the split.
- **Rests:** a pet recovers HP and abilities on a Long Rest in a safe room like a Crawler (house reading: only potions and scrolls are blocked by the canon rule, §7). Short rests: the GM decides, usually none.
- **Pets as targets:** hazards and enemies may target a pet; the GM weighs it like any ally. The 1-round potion cooldown (core §5.11) applies to a pet drinking a potion.

## 5. Pets and Story Boxes

- **A pet never gets a Story Box itself.** Story Boxes go to Crawlers, for a named, one-time deed (rules/45). The pet's owner earns the box when the **owner** earns the deed in play.
- The existing cards cover it (rules/45 §2.4): **first pet into the Crawl** (Pet Box: the Enhanced Pet Biscuit, card f01-any-0055); **first four-legged companion** (Quadruped Box, a crown or collar-type item worn by the animal); and the **first fictional rival** (a separate deed, rules/45 §2.4). The two pet-themed boxes are one theme: at most **one box per duplicate-theme pair**, so **one pet deed per floor**; if both happen the second pays a normal Silver box at most plus a Title, as rules/45 §2.4 already says.
- **Pair 0055 and 0060 is one two-card Pet Box.** The Enhanced Pet Biscuit (0055) and the Pet Biscuit Crate (0060) are two pulls of one Legendary Pet Box and are awarded together, logged once under the cap (rules/42 §6.9; rules/45).
- Having a pet is **not** a deed. The deed needs a beat in play where something was at risk (rules/45 G3), and the GM never stages one for the pet.
- Neither the potion (§7) nor the kennel (§8) is a loot-deck card or a Story Box item. They are System vending goods with prices (§7, §8).

## 6. Enhanced Pet Biscuit: pet to pet-Crawler

Rules text lives in `rules/42-house-items-f01.md` §6.2 and is unchanged. This section records the table rule it sits in.

- **Who and what:** feeding the Biscuit to a **willing pet Beast of CR 1/4 or lower** converts it into a **full Crawler** (Donut-style, ledger M-037, I-007, C-028; wiki-ledger, not book-checked). It works only on the pet named in the deed (rules/45 §2.3 rule 8), which in practice is the pet filed on the owner's sheet.
- **Controlled by the owner as its own Crawler.** It takes **no extra player slot** and counts for encounter budgets like any Crawler (decision 018). It has its **own sheet channel** named `<player>-<pet>-sheet` (decision 020 and 021) and its own Crawler record.
- **One conversion per living pet-Crawler.** A deleted pet-Crawler frees its conversion; a new conversion needs a **new Biscuit** (decision 021, no tombstone).
- **The owner deleted:** the pet-Crawler stays **benched on file** and is removed only by its own `/delete` (decision 020 v1.2).
- **After conversion** the creature is a Crawler: core §6 (death, revival) and §5.9 apply to it like any Crawler, and it is **no longer a pet-class creature** for the healing rule (§7), the kennel (§8) or this file's pet rules. Its old pet record on the owner's sheet is closed ("became a Crawler").
- The owner's pet items (potion, kennel) stop being listed once the owner has no plain pet on file.

## 7. Healing a pet: Good Boy Gulp

**Canon rule (CANON, ledger K-161, M-090; wiki-ledger, not book-checked), already locked in decision 013-crafting answer 4 and `rules/20-crafting-5e.md` §6.3:** ordinary healing potions and healing scrolls **do nothing** on pet-class creatures. A purpose-brewed Heal Critter potion works (ledger K-121, M-090; wiki-ledger, not book-checked). Nothing here changes that.

**Good Boy Gulp, Shaken Until Brown** (house name from Lore, item id `heal-critter-potion`; the canon item is the Heal Critter potion). Working description: HOUSE numbers.
- **Effect:** a pet-class creature that drinks it regains **2d4 + 2 hit points**, like a Potion of Healing. It does **nothing** for any other creature. It is not a revive: a dead pet stays dead.
- **How it is used:** the target must drink it (K-121). The owner may give it to an adjacent willing pet as a Bonus Action.
- **Price (the Accountant's):** **50 credits** at Floor-1 scale, times the floor credit multiplier (x1 F1-4, x5 F5-9, x20 F10-14, x50 F15-18; decision 019). **System buyback is half the price** on the sale floor (25 at Floor-1 scale).
- **Off-menu:** listed only for a Crawler who already has a plain pet on file (§2 item 4). Not on the vending wall, not in player chapters.
- **Not a loot-deck or Story Box item.** `credit_value` is not used; it has no card id.
- The crafted version in `rules/20-crafting-5e.md` §5.5.3 is a separate path for a Crawler with the right tools; see §13 question 1 for the number differences.

## 8. The Fold-Flat Kennel (Pet Carrier)

**Fold-Flat Kennel With an Impossible Interior** (house name from Lore, item id `pet-carrier`; canon item is the Pet Carrier, ledger I-012: "magical carrier ... bonded pets into a crawler's inventory", wiki-ledger, not book-checked). HOUSE numbers, my own words:
- **Size and weight:** it is **one item of 2 lb** in System Inventory (or carried folded). It holds **one bonded pet**: the owner's own pet Beast of CR 1/4 or lower.
- **Stowing:** Utilize action, with the pet within 5 feet and willing. The pet vanishes into the kennel. While stowed it is **safe**: it cannot be targeted, takes no damage, needs no food or air, and no time passes for it. It does not count toward the inventory capacity (core §5.9) and adds no weight; this is the **one exception** to "living creatures can't be stored".
- **Releasing:** Bonus Action; the pet appears in an unoccupied space within 5 feet of the owner.
- **Travel without a roll:** a stowed pet **moves with its owner between rooms and floors with no roll**. The GM uses the kennel to move a pet through a hazard, a stairwell crowd, a long chase or a forced separation without a check.
- **Limits:** a pet-Crawler cannot be stowed (it is a Crawler); the kennel holds one pet; a hostile effect that forces a creature out of inventory ends the stow.
- **If the owner dies:** the inventory drops as a corpse cache (core §5.9); the pet is released unharmed at the body and is a GM-run creature that is no longer anyone's Crawler pet. The kennel is ordinary loot.
- **Price (the Accountant's):** **100 credits** at Floor-1 scale, times the floor credit multiplier. **Buyback is half the price.**
- **Off-menu**, like the potion. It is bought, not drawn from a box; it is not a loot-deck or Story Box item and does not use the floor's box pacing (core §3.7).

## 9. Pets and floors, safe rooms, encounter budgets

- **Floors and rooms:** a pet **travels with its owner** between rooms and between floors. On a stairwell descent the pet comes along with its owner (core §6.6). Where the fiction makes keeping a pet close hard (a collapse, a chasm, a crowded stairwell, a panicking animal), the GM may call for a Wisdom (Animal Handling) check or let it get separated. **Stowed in the kennel, no roll is needed** (§8).
- **Safe rooms:** a pet is welcome in a safe room, rests there (§4), and can be healed there. It does not shop, open boxes or use the terminal. A false saferoom (core §5.6) endangers the pet as it does everyone.
- **Benched owners:** a benched Crawler's pet is benched with it: not in play, no update.
- **Encounter budgets:** a pet counts as a **minor ally**, at the GM's discretion. Keep it light: the GM does not rebuild budgets for it; where a fight is close, nudge the enemy side up by about one CR 1/4 creature (the pet's own XP value) or leave the budget alone. A **pet-Crawler counts as a full Crawler** (decision 018), as before.

## 10. Assigned Companion: how it differs

The **System's Assigned Companion** for a 2-Crawler table (core §2.4) is a separate GM-run rule. It stays as written. Both are GM-run; both take no loot and can die. Differences:
| | Pet (this file) | Assigned Companion (core §2.4) |
|---|---|---|
| Who gets one | A Crawler whose player wrote it into their own free text | A 2-Crawler table, issued by the System |
| Table size | Any | 2 Crawlers only (also used as the GM's temporary stand-in after a mid-session death, decision 020) |
| What it is | An SRD Beast of CR 1/4 or lower, bonded to one owner | A GM-run SRD creature or NPC stat block, CR at most half the party level |
| Belongs to | One owner Crawler | The table |
| Share of party credits and loot | None | None (it takes no share of party credits or loot) |
| Death | Final; no revive | It can die; the System may issue another at the GM's choice |
| Healing | Good Boy Gulp only (ordinary potions do nothing) | Rules/20 §5.5.3 lists it as pet-class, so the same potion rule applies |
| Biscuit | Can become a Crawler (§6) | Not a pet; the Biscuit needs the owner's pet |

## 11. Canon basis (all wiki-ledger, not book-checked)

| Point | Ledger row | Where used |
|---|---|---|
| Lucia Mar arrived with two rottweilers | H-014 | §1 |
| Enhanced Pet Biscuit; Donut and Prepotente consumed it | I-007, M-037 | §6 |
| Pets get classes only via a rare biscuit-type exception | C-028 | §1, §6 |
| Ordinary healing potions/scrolls do nothing on pet-class creatures | K-161, M-090 | §7 |
| Heal Critter potion exists; the pet must drink it | K-121, M-090 | §7 |
| Pet Carrier lets a bonded pet into the inventory | I-012 | §8 |

Everything else (the INT-below-2 line, the one-pet limit, GM filing, off-menu, prices, kennel and potion numbers, rest rule, budget rule) is **HOUSE**.

## 12. What the Architect needs (summary)

The proposal and unticked checklist are in `characters/create-flow-spec-5e.md` §9 (v0.1.8). In one paragraph: **no pet field, screen or question anywhere in `/create`, and the S13 survey pool must lose its existing "Cats or dogs?" bonus question (`tables/create-flow-lines.json`, id `pets`)**; a GM-run action files a pet (name, SRD Beast species validated as CR 1/4 or lower, free text) on the owner's sheet; a biscuit action converts it; a table setting turns the whole feature off; `non_srd` pet items are listed only on a pet owner's own card or channel, never the shared wall, and the item lookup must show credit prices for `non_srd` items.

## 13. Open questions (3)

1. **Crafted Heal Critter vs vending Good Boy Gulp.** `rules/20-crafting-5e.md` §5.5.3 says the crafted potion heals 4d4 + 4 and is priced 75 credits at F3+ alchemical markets. The Accountant's vending item here heals 2d4 + 2 for 50. Default: they stay two different things (a crafted one is better and costs ingredients and time; the vending one is the cheap pet-owner stock). Syndicate/Accountant to confirm or align.
2. **Pet-Crawler and ordinary healing.** Default filed here: after the Biscuit it is a Crawler, so ordinary healing works and Good Boy Gulp no longer does. Caleb may prefer the old rule to stay on it.
3. **Two-animal canon.** Canon had two rottweilers (H-014). Default: one pet per Crawler; the GM may treat a bonded pair as one creature for flavor only. Caleb may widen to two.

## 14. Changes for the room

- **Architect (Borent):** spec §9 and its checklist; remove the "Cats or dogs?" survey bonus question (`pets`) from `tables/create-flow-lines.json`; add the GM pet action and the feature switch; filter `non_srd` pet items off the shared vending wall; show credit prices for `non_srd` items in the lookup.
- **Lore:** `tables/item-reskins.json` v0.1.4 already has `heal-critter-potion` ("Good Boy Gulp, Shaken Until Brown") and `pet-carrier` ("Fold-Flat Kennel With an Impossible Interior"); set `price_credits_proposed` to the confirmed 50 and 100 and copy the mechanic notes from §7 and §8.
- **Accountant:** buyback is half; both prices carry the floor multiplier (decision 019); both items are purchases, not loot-deck cards.
- **GM notes:** `gm-notes/00-gm-principles.md` "Pets" section should point here (not edited in this change).
- **rules/20:** §5.5.3 price and dice vs §7 (question 1).

## 15. Changelog

- **v0.1.0 (2026-10-04):** first file. Ruling by Caleb (2026-10-04) on the pets design proposed by the GM and Lore, with his conditions (nobody is offered a pet; only a pet written into a player's own free text; no pet field in `/create`; potion and kennel off-menu). Items named by Lore; prices from the Accountant. Decision 022.

---
*SRD attribution: this file references 5e rules by name and does not reproduce book text; see CORE Appendix D.*
