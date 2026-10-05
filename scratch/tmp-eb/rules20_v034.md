# Crafting Rules (5e Overlay)
Owner: Syndicate Dungeon Crawl System 001 | Status: review (all open questions answered by Caleb 2026-10-04 and applied; no open rules questions remain, three small new ones in §10.2) | Version: 0.3.4 | Updated: 2026-10-04
Summary: Crafting on D&D 5e 2024 tool proficiencies: strictly saferoom-only workstations (tables) as Personal Space accessories (first table Floor 2, very rare Floor 1 find plus a placed goblin-workshop cache, unusable until Floor 4), table levels bought on any floor (credits or coupons, no automatic leveling), DM-granted crafting boons, ingredients, recipe stat blocks with 11 canon-inspired examples, 1-round potion cooldown, failure/Dud/explosives rules (Boomer capped at 6d6 until level 5), Steady Hands no-roll default, System snark, balance, locked decisions, and a one-page quick reference.
Depends on: rules/10-core-rules-5e.md v0.2.8 (v0.2.7 carries the crafting pointer and the merged edits, §11; core wins on any remaining conflict). Decisions: decisions/004-crafting-system.md, decisions/008-crafting-rules.md, decisions/010-first-crafting-table.md, decisions/011-crafting-settings.md, decisions/012-crafting-economy-explosives.md, decisions/013-crafting-open-questions.md ("decision 013-crafting" below; it shares the number 013 with decisions/013-party-size.md). Canon: /workspace/dcc-lore/catalog/crafting-canon.md = CANON-LEDGER.md §10 (IDs K-###, X-C##).

> **Status:** v0.3. Caleb approved the first-table, crafting-settings and economy/explosive decisions on 2026-10-03 and answered every open question on 2026-10-04; all are LOCKED (§10.1, decision 013-crafting). §10.2 now holds only three new, small questions. **Project:** *Crawler Protocol: Season Zero*, original fan RPG inspired by *Dungeon Crawler Carl*. Private play only.
> **Scope:** only what is homebrew or changed. Anything not here is 5e 2024 as written (2024 PHB tool rules and crafting; 2024 DMG magic item rarity and prices).
> **Canon use:** canon facts are short paraphrases with ledger IDs. No book or wiki prose is reproduced. Ledger "VERIFIED" is a bookkeeping label (wiki cite or two source families), **not** checked against the novels.

*System note:* "Welcome to Arts and Crafts! Please keep all fingers on the correct side of the bench. Fingers on the wrong side become ingredients."

---

## Table of contents

0. How to read this doc (tags, precedence)
1. Principles
2. Workstations (tables)
3. Crafting skills as DM-granted boons
4. Ingredients
5. Recipes: format, learning, procedure, examples
6. Limits and failure (potions, Dud, crit table, Natural 20, explosives)
7. House-rule stations: Cooking, Smithing, Enchanting, Scribe
8. System voice and achievement seeds
9. Balance: prices, per-floor availability, anti-abuse, DM procedure, session state
10. Locked decisions and open questions
11. Conflicts with canon and with core rules
12. Changelog
Appendix A: One-page quick reference
Appendix B: Canon source map

---

## 0. How to read this doc

**Tags used on every rule that isn't plain 5e:**

| Tag | Meaning |
|---|---|
| **[C:V]** | Canon fact, ledger **VERIFIED** (cite in Appendix B) |
| **[C:W]** | Canon fact, ledger **WIKI-ONLY** |
| **[C:U]** | Canon claim, ledger **UNVERIFIED** or an open conflict (X-C##) |
| **[CI]** | Canon-inspired: the idea is canon, the 5e numbers are ours |
| **[HR]** | **HOUSE RULE**: invented for this table; no canon page defines it |
| **[LOCKED]** | Approved by Caleb 2026-10-03 or 2026-10-04 (decisions 010, 011, 012, 013-crafting). Change only through a new decision (§10.1) |

**Precedence.** Active floor rules → `rules/10-core-rules-5e.md` → **this doc** → 5e 2024. This doc is an add-on module: core rules (v0.2.8; the merge landed in v0.2.7) now carry the merge Caleb approved (the crafting pointer, Personal Space, the 1-round potion cooldown, Table Tokens and the saferoom stash; §11), and where the two still disagree, core rules win.

**Conventions.** Credits = GP (core §0). "Saferoom" = a certified, *honest* saferoom (core §5.6). "Crafter" = any crawler or NPC working a recipe. Voice tags `[SYSTEM]` / `[GM]` / `[ROLL]` per decision 007 and `bot/README.md`; `Reward:` lines go on their own line.

---

**Prices and the floor multiplier (Lore, with Caleb's delegation, 2026-10-04).** Every credit price listed in this document (level upgrades, bench supplies, ingredient and shop prices; **not** the three workstation prices, see the next paragraph) is written at **Floor-1 scale** and is **multiplied by the core §3.9 credit multiplier of the floor where the purchase happens** (x1 F1-4, x5 F5-9, x20 F10-14, x50 F15-18), the same as repair prices (`rules/50-gm-malfunction-repairs-5e.md` §1.2). Box credit pulls do **not** get the multiplier; achievement rewards and System fees do. No number in this document was changed. **Flag for Caleb:** read literally, the basic table (repriced to 5,000 on 2026-10-04, so 25,000 on F5-9, 100,000 on F10-14, 250,000 on F15+) sits next to coupons and revive fees that do not scale: the Upgrade Coupon cap (25,000, a reward value) and the flat revive Fees (5,000 to 100,000, core §6.4). Original flag, now mostly resolved by the lower base: while the Upgrade Coupon cap (25,000, a reward value) and the flat revive Fees (5,000 to 100,000, core §6.4) do not scale. At F10+ that makes a table purchase absurd next to box income and revives unless coupons or rewards scale too; a table bought on F4 to F9 avoids it.

**Workstation prices (v0.3.4, room vote Q-004, 2026-10-04; decision 030).** The three workstation prices (**basic table, Crafting Studio, Enhanced Crafting Studio**) no longer take the credit multiplier. **Floors 1 and 2 keep the ruled prices (5,000 / 12,000 / 30,000)**; **Floors 3 to 18 use the smoothed schedule in §9.1a**, which is aimed at about 3 / 6 / 10 floors of a crawler's liquid income (box items sold at half). Everything else in this paragraph's multiplier rule stands: level upgrades, bench supplies, ingredient and shop prices still take the multiplier. The 'tables upgrade on ANY floor' ruling (§2.4) is unchanged. The numbers come from `rules/70-encounter-budget-5e.json` (`q6_crafting_price_proposal`), which is the source if the two ever differ.

## 1. Principles

1. **5e tools are the engine.** Every recipe names a 2024 tool and its ability (Alchemist's Supplies = Int, Herbalism Kit = Int, Tinker's Tools = Dex, Smith's Tools = Str, Thieves' Tools = Dex, Carpenter's Tools = Str, Leatherworker's Tools = Dex, Calligrapher's Supplies = Dex, Cook's Utensils = Wis, Brewer's Supplies = Int, Glassblower's Tools = Int). The check is that tool's ability check: **d20 + ability modifier + Proficiency Bonus (if proficient) + table bonus** vs the recipe DC. **2024 tool rule applies:** if you're also proficient in the recipe's synergy skill, you have **Advantage**. No proficiency: Common recipes only, no Proficiency Bonus.
2. **Workstations do the heavy lifting.** Anything beyond a Common or bench-free recipe needs a **table** (a Personal Space accessory, §2) of a high enough **level**. Tables come with tools and supplies but **not recipes** [C:V K-026].
3. **Crafting happens only in a saferoom** [HR, per brief; **LOCKED strict**, decision 011: no field mixing, not even Quick or Common recipes]. That means at a table in your Personal Space, reached through an honest saferoom's door, or bench-free work inside a saferoom. Never in the field, never in a false saferoom (no Personal Space door appears there, which is itself a tell). *Canon lets simple recipes be mixed in the field* [C:V K-163]; this table doesn't (§11). **Tables themselves can't be used until Floor 4** [LOCKED, decision 010; §2.5.2]; before then only bench-free saferoom work is possible.
4. **Explosives are inert in saferooms** [C:V K-170] (smoke can still go off there: canon notes smoke bombs work). You can build bombs there but they can't detonate. **They're only fully stable while on a Sapper's Table** [C:V K-017, K-022]. Once an explosive leaves the table, the stability rules in §6.8 apply.
5. **Saferooms keep you alive, not unhurt.** A crafting mishap in a saferoom can't drop a crawler below 1 HP [HR; canon flavor: a bad workbench session can still hurt you, K-167].
6. **DM-granted, not shopped.** Recipes above Common, all crafting skills (§3), and table drops on Floors 1-3 are rewards (loot, boxes, quests, mentors). Revival items are **never** craftable (core §6.4.2).
7. **The System names your stuff.** Every crafted item gets a System name and a description, often mocking and not always accurate [C:V K-166]. Mechanics are honest; the label isn't.
8. **Time is the main cost.** Recipes cost **shifts** of saferoom time (§2.7), and saferoom time is the clock the floor is running on.

---

## 2. Workstations (tables)

### 2.1 Personal Space and Crafting Studio

- **Personal Space** [CI; canon: tables are Personal Space accessories, K-001, K-053]. When a crawler's first table is **certified** (Floor 4, §2.5.2), the System issues a basic **Personal Space**: a private extradimensional room whose door appears in any honest saferoom. It fits **1 table** and a storage nook [HR]. Time inside passes normally. NPCs can't enter specialized rooms unless a crawler escorts them [C:V K-054].
- **Crafting Studio** (Personal Space accessory) holds up to **5 basic tables** [C:V K-005]. Source: box, quest, or shop on Floor 4+ (§9.1). Like tables, it can't be used before Floor 4.
- **Enhanced Crafting Studio** [C:V K-006; price C:W K-007]: needed for **advanced stations** (Advanced Bomber's Studio, Automaton Table) and a vehicle garage. Floor 6+ [CI, matching canon tier-two upgrades on F6, K-045].
- **Combined spaces** (party): optional. Upgrades and tables stay tied to the crawler who owns them [C:V K-185]; the owner can grant other crawlers access [C:V K-048].

### 2.2 Table roster

| Station | Does | Tools (ability) | Synergy skills | Canon |
|---|---|---|---|---|
| **Alchemy Table** | Potions, poisons, reagent processing, potion balls | Alchemist's Supplies (Int); Herbalism Kit (Int) for herbal recipes | Arcana, Medicine, Nature | [C:V K-025..K-035] |
| **Sapper's Table** | Explosives, traps, poisons; modules and triggers; stabilizing; infusion | Tinker's Tools (Dex) or Alchemist's Supplies (Int); Thieves' Tools for traps | Sleight of Hand, Investigation | [C:V K-015..K-024] |
| **Demolitions Workshop** | Not a separate table: a Sapper's Table **menu**, unlocked by Explosives Handling 5 (§3) | as Sapper's | as Sapper's | [C:V K-024, K-063] |
| **Engineer's Table** | Catch-all fabrication and modification; multi-part builds; vehicles; launcher mounts | Tinker's, Carpenter's, Smith's, Mason's, Woodcarver's Tools | Investigation, Athletics | [C:V K-009..K-012] |
| **Armorer's Workshop** | Turns shaped material into **equippable** armor and shields; armor enchantments at higher levels | Smith's Tools (Str), Leatherworker's Tools (Dex) | Athletics, Arcana | [C:V K-036..K-038]; name conflict [C:U X-C02] |
| **Crafting Studio** | Room: holds 5 basic tables | — | — | [C:V K-005] |

**Other canon stations** (DM may place them; use the generic ladder in §2.3): Metal Working Table [C:V K-039], Bolt-Thrower's Workshop [C:V K-041], Makeup Table [C:V K-042], Automaton Table (F6+) [C:V K-043], Advanced Bomber's Studio (F6+ room with a simulator whose results aren't guaranteed to match reality) [C:V K-044, K-184], Repair Bench, Tinker's Table, Writing Table and Printing Press (named only) [C:V K-046, K-047].

### 2.3 Table levels (L1-L6+)

**Generic ladder** [HR]: the table's level caps the **rarity** of recipes it can run, and gives a bonus to checks.

| Level | Max recipe rarity | Check bonus | Size limit (builds) |
|:-:|---|---|---|
| L1 | Common | +0 | Medium |
| L2 | Uncommon | +1 per level above the recipe's minimum (max **+3**) | Large |
| L3 | Rare | (same) | Large |
| L4 | Rare (+ specialization) | (same) | Huge |
| L5 | Very Rare | (same) | Huge |
| L6 | Very Rare (+ batch) | (same) | Gargantuan |
| L7+ | Legendary (DM-granted recipe only) | (same) | Gargantuan |

Canon notes that big builds can exceed what a table handles [C:V K-169]; the size column is our version.

**Per-table effects** (canon where tagged; everything else [HR]):

| Level | Alchemy Table | Sapper's Table | Engineer's Table | Armorer's Workshop |
|:-:|---|---|---|---|
| **L1** | Common potions and poisons. Tools included, recipes not [C:V K-026]. | Common explosives, traps, poisons. Add **modules/triggers** (e.g. proximity triggers) [C:V K-016, K-023]. **While an item is on the table it can't decay or detonate early** [C:V K-017]. Deconstruct bombs with the Bomb Surgeon boon (§3.4). Explosives made here leave at **Steady**. | Fabricate and modify single-part items; use workbench-only shaping tools [C:V K-009, K-055]. Crude shaping tools weaken items when overused [C:V K-168]: a second modification of the same item is at Disadvantage. | Makes shaped metal or leather **wearable/equippable** [C:V K-036]. Mundane armor and shields only; **no enchanting, common metals only** at L1 [C:V K-037]. |
| **L2** | Uncommon potions. | Uncommon. Non-infused explosives leave at **Stable**. | **Multi-part builds** (each part a check, then assembly) [C:V K-012]. Vehicles up to Large. | Uncommon armor mods (resize, add an "intention" quirk [C:V K-038]); most metals. |
| **L3** | Rare. **Fragmenting Potion Balls** [C:V K-030, K-119]. Named exception: **Mordecai's Special Brew** [C:V K-113], brewed by a **crafter NPC only** (§5.5.1). | Rare. **Infusion**: put a potion or reagent into a bomb or tossable [C:V K-018]. | Rare. Install crafted launchers and explosives as **weapon mounts**. | Rare. **Enchanting** armor/shields up to Uncommon magic (house reading of K-037: enchanting is a higher-level ability). |
| **L4** | **Specialization** [C:V K-031]: pick one tag (Healing, Buff, Toxin, Utility); +2 to checks and +1 yield on that tag's Common/Uncommon recipes [HR]. | Advanced triggers: timers, remote, creature-type filters [CI K-023]; homing with a guidance part [CI K-104]. | Huge builds; automatons if you also own an Automaton Table. | Enchanting up to Rare; adamantine/mithral working. |
| **L5** | Very Rare. **Second heating element: brew time halved** (round up) [C:V K-030]. | Very Rare. Full Demolitions Workshop readouts (needs Explosives Handling 5). | Very Rare. | Very Rare. |
| **L6** | **Autoclave: batch of up to 100 units** of one known Common or Uncommon recipe in one run [C:V K-030; HR limits in §9.3]. | **Batch of 10** Common/Uncommon explosives per run [HR]. | Precision shaping: no weakening from repeat modification. | Batch of 2 identical mundane pieces. |
| **L7+** | **Examine-to-learn**: study a potion for 1 shift (Int (Arcana) vs its recipe DC) to learn its recipe without using it up [C:V K-034, K-035]. Legendary recipes, DM-granted. Canon's hoped-for L9 "fix the Brew's limit" [C:V K-028] is **not available here**; the Brew cap stays 2 and crawlers never brew it (§5.5.1). | Legendary (DM only). | Legendary (DM only). | Legendary (DM only). |

**Demolitions Workshop menu** (Sapper's Table + Explosives Handling 5) [C:V K-024, K-063]: while standing at the table you can see an explosive's **yield, stability and decay rate** (exact numbers, no roll), view its schematic, pull bombs out of System Inventory onto the table, and **design new bomb recipes** (invention, §5.2, without its +2 DC). Canon is unclear whether the Advanced Bomber's Studio and the "advanced Bomb Maker's Workshop" are the same thing [C:U X-C03]. Here the Studio is the F6+ simulator room (§2.1), and "advanced workshop" access comes with the Agent Provocateur boon (§3.3).

### 2.4 How tables level up

Canon conflicts here [C:U X-C04]: one source says tables gain a level every floor [C:V K-003; C:W K-004], yet Carl still needed coupons to reach L3 on Floor 4 [C:V K-019, K-029]. **House resolution [HR; LOCKED 2026-10-04, decision 013-crafting; replaces the v0.2 odd-floor "seniority" rule]:** **tables do not level up on their own. A table can be upgraded on ANY floor, as long as the owner pays (credits or a coupon) and meets the prerequisites.** Canon-style: no floor is skipped, no floor is special.

- **Prerequisites for an upgrade:** (1) the table is **certified** (Floor 4 or later, §2.5.2; tokens can't be upgraded), (2) the owner is at an honest saferoom's shop counter, (3) **one level at a time** (L1 to L2, then L2 to L3), (4) the new level is **at or under the level cap** (below), and (5) the owner pays the price below in credits **or** hands over a coupon that covers it.
- **Upgrade Coupons** [C:V K-049; **LOCKED**: cap 25,000, decision 012]: each coupon pays for **one** table purchase *or* **one** level upgrade with a list price of **up to 25,000 credits** (house cap; canon's cap is 250,000 gold in an inflated economy). Coupons are **non-stackable**: they can't be combined and give no change. They're bound to the crawler, who may spend them on any table they have access to (canon did this on Mordecai's table [C:V K-029, K-033]). Sources: **Quest Boxes and Boss Boxes (F3+)**, about **1 per crawler per two floors**; sponsor-gifted coupons are not part of the standard rate. Coupons may be banked from F3 but are spent only once shops open and the table is certified (Floor 4, §2.5.2). **What 25,000 covers:** a basic table (5,000), a Crafting Studio (12,000) and upgrades to L2-L5 (10,000-25,000). It does **not** cover an upgrade to L6 (30,000) or an Enhanced Crafting Studio (30,000); pay those in credits. **Coupons vs the floor multiplier (Accountant watching) [v0.3.4: the three workstation prices now follow the §9.1a schedule, not the multiplier, so the F5-9 figures below for tables and Studios no longer apply; level upgrades still take the multiplier]:** the multiplier (§0) applies to these list prices, so on F5-9 (x5) a basic table is 25,000 (still at the cap), a Crafting Studio is 60,000 and an Enhanced Crafting Studio is **150,000**, all above the 25,000 coupon cap except the basic table. A coupon therefore covers a basic table or a Crafting Studio only at low floors (Studio at F1-4, x1); from F5 up Studios are paid in credits. Whether the cap is compared to the Floor-1 list price or the multiplied price is not stated elsewhere; this note reads it against the price actually charged. Flagged for Caleb.
- **Buying a level** (F4+ shops, any floor): 5,000 credits × the target level (L2 10,000; L3 15,000; L4 20,000; L5 25,000; L6 30,000; L7+ DM only).
- **Level cap:** a table's level can't exceed **(floor number ÷ 2, rounded up) + 2** (F1-2: L3; F3-4: L4; F5-6: L5; F7-8: L6; F9-10: L7; F11+: L8+). An upgrade above the cap can't be bought; nothing is spent and nothing banks, so wait for the cap to rise. The Agent Provocateur +1 ignores the cap.
- **Benchmark (canon check):** a table found on F2 is L1 and stays L1 while it is a token. Certified on F4, it reaches **L3 on F4 with two coupons** (the party's banked F3 coupons, shared through access) or with one coupon plus 15,000 credits. That is canon's timing for the Special Brew and potion balls (Carl's two coupons, K-019; Donut's two, K-029).

### 2.5 Acquisition

| Floors | How tables arrive | Notes |
|---|---|---|
| **1-3** | **Found or rewarded only**: looted from a mob workshop, awarded in a loot box (a Sapper's- or Crafter's-flavored box), or a quest reward [C:V K-002, K-010, K-015, K-025]. **No shop sells tables.** | Party target: **1-3 tables total by the end of F3.** **LOCKED first table: Floor 2** (the Alchemy Table and Sapper's Table as written; the floor bible lists basic crafting there; canon puts them on Floor 2, K-015, K-025). **Plus a very rare random find on Floor 1** (§2.5.1). **Every table is unusable until Floor 4** (§2.5.2). *"No guaranteed table before Floor 2" is a **HOUSE** choice, not canon.* |
| **4+** | Saferoom shop counters sell tables from a catalog [C:V K-001, K-046]: **5,000 credits list** each on Floors 1-2 scale, and per the §9.1a schedule from Floor 3 [**LOCKED** base, decision 012, repriced by Caleb 2026-10-04; schedule v0.3.4, decision 030] (canon Engineer's ~25,000, K-011, scaled down to the box-income budget), Crafting Studio **12,000** [HR; Caleb 2026-10-04] (F4+), Enhanced Crafting Studio **30,000** (F6+) [HR; Caleb 2026-10-04], both at Floors 1-2 scale and per the §9.1a schedule from Floor 3. Boxes and quests still drop them. | A counter stocks 1d3 table types per floor (DM picks). Tables bought here are certified on purchase (§2.5.2). |

#### 2.5.1 Floor 1 random find [LOCKED, decision 010; the numbers are HOUSE and tunable]

A **very rare** chance to find a table on Floor 1. It **replaces** the v0.1.1 goblin-workshop owner-option: the goblin workshop is now a **placed cache** on Floor 1 (Zone 7, see the Floor doc line below), and searching it is one of the qualifying events.

- **Trigger (the AI GM rolls it, secretly, then logs it):** a **qualifying Floor 1 event** is (a) opening a Silver-or-better loot box (core §4.4), or (b) searching a secret cache, hideout or mob workshop (the canon goblin workshop is the model), or an optional exploration room with a loot nook. The DM designates **at most 2 qualifying events per party on Floor 1**. Each one gets one roll.
- **Roll:** d100. **1-5 = a table is found** (**default 5% per qualifying event, TUNABLE**: `F1-TABLE-FIND = 5%`; with 2 events the chance for the floor is about 9.75%). Raise or lower the number with a log entry, no other rule changes.
- **Cap:** at most **one** table found this way per party. It is **in addition to** the Floor 2 drop, never instead of it; the Floor 2 drop is then the second table, and the 1-3 tables by end of F3 target still holds.
- **What is found:** an L1 table. d6: 1-2 Alchemy Table, 3-4 Sapper's Table, 5-6 Engineer's Table. The DM may flavor it as a goblin workshop's table plus a stock of Common [Metal] and [Trigger] engineering supplies and a tool kit [canon, C:V K-010, K-103; B1 ch17-19: Carl looted an Engineer's Table there], **not** a rare table kit (K-051). The Engineer's Table has no starter recipe in §5.2, so the DM writes a Common single-part build or uses Kit Bash (§8.4).
- **Table is bound and unusable at once:** it follows the carry/stash rules in §2.5.2. The finder gets the receipt story event (§2.5.3) and the *Early Adopter* achievement seed (§8.4).
- **Floor doc [LOCKED 2026-10-04, decision 013-crafting]:** `floors/f01/00-overview.md` v0.2.3 places a concrete **goblin-workshop cache** in Zone 7 (the Exit Greeters' Back Office). Searching it is **qualifying event 1** and also yields a small guaranteed find (a Jug O' Boom recipe card, goblin oil and a worn Tinker's Tools kit; never a guaranteed table). The DM designates the second event (suggested: opening the Silver Boss Box). The roll itself is still run from this doc.

#### 2.5.2 Unusable until Floor 4: carry, stash, certify [LOCKED, decision 010; mechanics HOUSE, flagged in §11]

**The rule.** Every table (and Crafting Studio) is **unusable until Floor 4**, however it was acquired: it can't be placed, worked, given access to, or upgraded with a coupon or credits. Until then it is **carried or stashed**. *Bench-free work is not table use:* Kit Bash, the named bench-free recipes (Jug O' Boom, Heal Critter) and other bench-free Common recipes still work in an honest saferoom from Floor 1, exactly as written (**scope LOCKED 2026-10-04, decision 013-crafting:** only the named bench-free recipes and Kit Bash, plus DM-approved Common ones; a Popper or a Potion of Healing is **not** bench-free unless the DM approves it).

**Carried (default).** Core rules say what carrying is: the **System Inventory** (core §5.9) holds items weightlessly, and unopened loot boxes take no space. A received table is therefore a **Table Token** [HR], an entry in the owner's System Inventory that **weighs nothing and takes no capacity** (like a box token). It is **bound** to the crawler who claims it at a saferoom (as boxes are, core §4.4) and can't be traded. Core §5.9 drops a dead crawler's inventory as a lootable corpse cache; a Table Token is **not lootable**: on the owner's death §2.6 applies (repossessed unless a Table Heir is named, who keeps it at -1 level, minimum L1).

**Stashed (optional).** Core rules have **no saferoom stash**, so this doc defines a simple one [HR, flagged in §11]: at any honest saferoom's System terminal (1 minute, no check) the owner may **stash** a Table Token on their account and take it back at any honest saferoom. A stashed token is out of System Inventory, so it is safe from inventory theft, corpse-cache looting and any hazard the DM aims at System Inventory. Everything else is the same (still bound, still can't be upgraded before Floor 4, §2.6 on death).

**While waiting.** The table stays at the level it arrived with (L1); it does not level on its own (§2.4). Coupons are banked but can't be spent before Floor 4. Recipes learned (including the starter recipe) are listed in the crafting menu but greyed out for table recipes.

**Certification (Floor 4).** At the first honest saferoom of Floor 4, the System **certifies** every Table Token the party holds: each owner gets a basic Personal Space (§2.1) and the door appears (script: §8.2b). A basic Personal Space fits **1 table**: an owner with two tokens places one and keeps the other as a token until they have a Crafting Studio (§2.1). Tables bought in a shop are certified on purchase. A crawler with no token on Floor 4 can buy one (§2.5.3).

#### 2.5.3 Shops, the X-C01 gate, and the first-table story event

**Canon conflict flagged** [C:U X-C01]: the wiki says saferooms don't sell tables until Floor 4; a Book 1 recap implies a saferoom store sold a Sapper's Table earlier. **This table uses Floor 4 for shops** [LOCKED, decision 010]. The DM may bend it once (a shady Floor 2-3 vendor sells exactly one table at 2x list price, with a rider); a table bought that way is still a Table Token until Floor 4.

**The first table receipt is a story event.** Run it like a spine beat (it fires when the first table arrives, whether the Floor 2 drop or a Floor 1 find):
1. Deliver it at a saferoom (box opening or quest payout), never in a corridor. A find in the field goes straight into System Inventory as a token and is announced at the next saferoom.
2. Fire the receipt announcement (§8.2): the System explains saferoom-only crafting and inert explosives, badly, and that the table is "pending certification" until Floor 4.
3. Give the owner **one starter recipe** that fits the table (§5.2; usable once the table is certified) and the seed achievement *Some Assembly Required* (§8.4).
4. Log `TABLES` (§9.5) with state `token`. Mention who else could use it after Floor 4, so the party talks about access.
5. On Floor 4, fire the certification announcement (§8.2b).

### 2.6 Ownership, access, death

- A table belongs to one crawler. Once certified (Floor 4), the owner may grant access to any crawler (log it). Crawlers with access can work it and pool shifts (§2.7).
- **Owner dies:** the System repossesses their tables and Personal Space **unless** they named a **Table Heir** (any crawler with access). The heir keeps each table at **−1 level** (minimum L1) [HR; canon parallels: Carl left his tables on Donut's side so she'd keep them, K-052; upgrades are lost when the buyer dies, K-185].
- Tables can't be sold back. They change hands only by heir transfer.

### 2.7 Mapping time and gold to 5e

5e 2024 crafting runs in 8-hour downtime days. The Crawl has no downtime, so we use **shifts** [HR]:

- **1 shift = 2 hours** of focused work at a table (or bench-free in a saferoom).
- **Free shift:** a saferoom **Long Rest** includes **1 shift** (its 2 hours of light activity, 2024 rules).
- **Extra shifts:** each costs 2 hours of real floor time (floor clocks, Lights-Out cycles, threats outside and rival parties all keep moving). After the 2nd extra shift without a Long Rest, each further shift requires a **DC 10 Constitution save** or you gain 1 level of Exhaustion.
- **Short Rest** in a saferoom: one **Quick** recipe (10 minutes) only.
- **Work in progress persists.** A recipe's shifts can be spread across visits; the half-built item waits on the table (an explosive is protected while on a Sapper's Table).
- **Pooling:** crawlers with access and the right tool proficiency may add shifts to the same recipe. **One** lead crafter rolls once at completion; one helper may give Advantage (Help).

**Time by rarity** (before table effects): Quick (named Common recipes) 10 min · Common 1 shift · Uncommon 2 · Rare 4 · Very Rare 8 · Legendary 16+ (DM).

**Gold:** every recipe costs **bench supplies** in credits on top of its ingredients: Common 10 · Uncommon 50 · Rare 500 · Very Rare 5,000 · Legendary 25,000. Paid at the start; lost on any failure (Off Batch, Ruined, Dud; Steady Hands auto-failures too).

**DC by rarity:** Common 10 · Uncommon 13 · Rare 15 · Very Rare 18 · Legendary 21. Infusion **+2**. Group build at too low a table level **+2**.

**Steady Hands (no-roll mode): ON by default** [HR; **LOCKED**, decision 011]. For fast chat play, crafting checks are **not rolled**. The DM computes a **Steady Hands total** and compares it with the DC:

> **Steady Hands total = 10 + the tool's ability modifier + Proficiency Bonus (if proficient) + table bonus + any flat boon bonus** (e.g. Explosives Handling 4's +1). **Advantage** (tool + synergy-skill proficiency, or a Help from a helper) adds **+5**; **Disadvantage** subtracts 5 (the usual passive-check convention).

- **Total ≥ DC:** success, yield as listed. **Total < DC:** automatic failure; use the margin below the DC for the result (1-4 = Off Batch, 5 or more = Ruined, §6.4); a failed **infusion** is a **Dud** (§6.5). Bench supplies are lost on a failure as always.
- **The crafter knows before committing.** The DM states the total and the DC *before* ingredients and bench supplies are spent. The crafter may back out for free.
- **What it removes:** no Natural 1 or Natural 20, no Success-by-10 bonus, no §6.6 mishap table and no §6.7 Natural 20 table. Only plain success or failure, Off Batch, Ruined and Dud remain. Invention's +2 DC (§5.2) and the other DC modifiers still apply.
- **Log it as one line:** `[GM] Steady Hands: 10 + 3 + 2 + 1 = 16 vs DC 15: success`.
- **Roll it anyway** [HR; **LOCKED 2026-10-04, decision 013-crafting**: kept as an opt-in so that hard recipes aren't out of reach]: before the DM states the total, the crafter may choose to roll that craft normally (§5.3) with all the result tables. This is the only way to attempt a recipe whose total is under the DC without a guaranteed failure, and the way to fish for Natural 20 bonuses.
- **Table switch:** the table may turn Steady Hands off (always roll; the explosions are the show). Harvesting (§4.2) and other non-crafting checks are rolled as normal either way.

---

## 3. Crafting skills as homebrew boons

All of these are **DM-granted** boons (R4 when first granted, R4-R5 per rank-up; core §3.4). **LOCKED, decision 011: DM-granted only; no trainer price list.** There's no level-up pick, shop or trainer. They train **by use** (canon: building a new device can raise several skills at once, K-079), as quest rewards, or from a mentor NPC. Track ranks on the sheet (`SKILLS`, §9.5). The DM may cap any boon lower by floor.

### 3.1 IED (ranks I-III) [CI; canon K-060: each level adds 10% improvised-explosive damage and halves the early-detonation chance]

- **Yield:** your crafted explosives deal extra damage equal to **rank × (number of damage dice ÷ 2, rounded down, minimum 1)**. Example: 4d6 at rank I = +2; 8d6 at rank II = +8. Roughly +10-15% per rank [HR numbers].
- **Steadier hands:** for **early-detonation rolls only**, your explosives count as **one stability step better per rank** (§6.8). Each step halves the chance, matching canon's halving.
- Rank II earliest F4, rank III earliest F9 [HR].

### 3.2 Explosives Handling (ranks 1-5) [CI; canon K-061, K-063]

| Rank | Benefit |
|:-:|---|
| 1 | You can tell an explosive's tier and stability by looking at it (no check). |
| 2 | Advantage on checks to disarm, defuse or safely carry explosives. |
| 3 | Pick up and re-place your own armed mines/traps without triggering them (canon parallel: Backfire, K-067). |
| 4 | +1 to explosive recipe checks. |
| **5** | **Unlocks the Demolitions Workshop menu** at a Sapper's Table (§2.3) [C:V K-024]. |

Typical pace [HR]: rank 1 on the first bomb crafted, then about +1 per floor of real bomb use; rank 5 no earlier than **F4** (Carl had it on F1 in canon; 5e power says later).

### 3.3 Agent Provocateur [CI; canon subclass chosen on F6, K-074]

- **+1 Sapper's Table level** (ignores the §2.4 cap) [C:V K-021, K-074].
- Advanced bomb workshop access: may design **Very Rare** bomb recipes at Sapper L5 with no invention penalty.
- **Earliest Floor 6**, one crawler per party, by quest or Benefactor only. It's a **boon, not a 5e subclass**: no class features change.

### 3.4 Optional canon boons (DM may use; same rules)

- **Bomb Surgeon** [CI K-065, K-066]: deconstruct explosives at a Sapper's Table for half their ingredients; split one explosive into two of the next tier down.
- **Infusion** (ranks I-II) [CI K-069]: −2 DC on infusions per rank, and infused items leave one stability step better.
- **Alchemy** [CI K-057]: +1 to alchemy checks; Quick recipes can be made bench-free (still in a saferoom).
- **Trap Engineer** [CI K-068]: Thieves' Tools trap recipes count the Sapper's Table as one level higher.

*System note:* "Skills are earned, not bought. Unless you're buying them. Which you can't. Yet."

---

## 4. Ingredients

### 4.1 Rarity ladder (matches 5e item rarity)

| Ingredient rarity | Monster source (CR) | Boss source | Vendors | Earliest floor (default) | Buy / sell (credits) |
|---|---|---|---|:-:|---|
| **Common** | CR 0-2 | — | All saferoom vendors | F1 | 10 / 5 |
| **Uncommon** | CR 3-5, elites | F1-2 boss reagent | Alchemical markets in towns (Continuum F3+) [C:V K-092] | F2 | 50 / 25 |
| **Rare** | CR 6-10 | F3+ boss reagent | Limited stock, F6+ | F3 | 500 / 250 |
| **Very Rare** | CR 11-16 | F9+ boss reagent | Never on shelves (Benefactor, black market) | F8 | 5,000 / 2,500 |
| **Legendary** | CR 17+ | Spine / finale | Never | F13 | not sold |

The floor's rarity **ceiling** (core §3.6) caps ingredient drops the same way it caps items: no ingredient above the floor's **peak** rarity, and only bosses drop at peak.

**Raw can beat product.** Some raw materials sell for more than what you'd make from them [C:V K-173]. Vendors decide; the System enjoys it.

### 4.2 Drop sources

- **Auto-sorted loot:** some drops land straight in the **Crafting Items** menu of System Inventory [C:V K-090], e.g. ichor vials, glands, small corpses tagged as alchemy material [C:V K-091].
- **Harvesting:** 10 minutes per corpse, one attempt. **Wis (Medicine)** for organs and ichor, **Wis (Survival)** for hide and bone, **Int (Nature)** for plants and fungi, **Int (Arcana)** for arcane or spirit parts. DC: Common 10, Uncommon 12, Rare 15, Very Rare 18, Legendary 20. Failure ruins it.
- **Boss reagent:** every boss leaves **one guaranteed reagent** at the floor's peak rarity (no roll), in its cache or Boss Box.
- **Vendors:** see the table above. Food and ordinary goods can be ingredients [C:V K-092, K-093].
- **Kits:** a **table kit** of rare supplies for one table is a valid R3-R5 reward [C:V K-051].

### 4.3 The "monsters worth killing" rule [HR]

A creature yields a harvestable reagent **only if it was a real threat**:
- its CR ≥ **half the party's average level** (round down; minimum CR 1/4), **or**
- it's an elite, named, or boss.

Trash below that line yields a Common reagent only on a **d6 roll of 6** (one roll per fight, not per corpse). **Fire and explosions eat loot** [C:V K-174]: for a creature killed by fire or explosive damage, roll d6. On a 1-3 its reagents are destroyed; on a 4-6, harvest at Disadvantage.

*System note:* "You killed forty rats and want ingredients? Sweetie, those rats WERE ingredients. Then you exploded them."

### 4.4 Ingredient tags

Every ingredient carries **1-2 tags**. Recipes ask for tags, not exact items, unless a recipe names a **signature** ingredient.

| Tag | Examples (reskin freely) |
|---|---|
| **[Herb]** | weeds, fungi, spices (a cinnamon stick counts [C:V K-109]) |
| **[Organ]** | glands, hearts, livers |
| **[Ichor]** | blood, hemolymph, venom [C:V K-091] |
| **[Bone] / [Hide]** | horns, shells, pelts, scales |
| **[Mineral] / [Metal]** | salts, ore, scrap, wire |
| **[Accelerant]** | moonshine, oil, gunpowder [C:V K-094, K-095] |
| **[Explosive]** | dynamite, grenades, lobbers [C:V K-099..K-101] |
| **[Casing] / [Trigger]** | jugs, tubes, plungers, proximity triggers [C:V K-023] |
| **[Vital]** | parts of creatures with great Constitution (trolls, ogres, bears) |
| **[Regenerative]** | troll parts, regrowing tissue |
| **[Phase]** | invisible, ethereal or shifting creatures; odd roots [C:V K-111] |
| **[Arcane] / [Spirit]** | crystals, ectoplasm, soul fragments [C:V K-108] |
| **[Food]** | anything edible; used by Cooking (§7.1) |

---

## 5. Recipes

### 5.1 Recipe stat block (standard format)

```text
RECIPE: <Name>   [C:V / C:W / CI / HR tag]
Station:     <Table> L<min>  (or Bench-free, saferoom)   Tool: <tool> (<ability>)   Synergy: <skill>
Rarity:      <Common..Legendary> <consumable | permanent | build>      Earliest floor: F<n>
Ingredients: <qty x [Tag] rarity>, <signature item>, + <bench supplies> credits
Time:        <Quick | n shifts>
Check / DC:  <tool ability check> vs DC <n>  (modifiers)
Yield:       <n units>
Shelf life:  <stable in System Inventory | spoils | stability step for explosives>
Sickness:    <standard cooldown | lockout | stat cap | none>
Effect:      <5e rules text>
Source:      <ledger IDs + tags; what is house>
Price:       <where sold / NPC fee>
```

### 5.2 Learning recipes

Canon: tables don't come with recipes [C:V K-026]; once you've brewed something it stays in your crafting menu [C:V K-165]; recipe books and mentors exist (the Cookbook, K-150; Mordecai, K-059). **Here:**

- **Recipe cards** (System menu entries) come from a **mentor NPC** (the Mordecai role; a lesson costs a favor or a quest), **loot** (recipe pages as Bronze/Silver pulls), **achievements**, and **examine-to-learn** (Alchemy L7+).
- **Invention:** a crawler pitches a recipe in plain words; the DM writes the stat block using the §6.9 tiers and §2.7 numbers, at **+2 DC** for the first attempt. Success writes it permanently to their menu. The first invention that stacks earns *Dungeonpreneur*-style credit (§8.4) [CI K-176].
- **Starter recipes** (a new table owner picks 1 at receipt; table recipes become usable when the table is certified on Floor 4, §2.5.2):
  - **Potion of Healing:** Herbalism Kit or Alchemy L1; Common; 1 shift; DC 10; 1 [Herb] Common + 10 credits; yield 2.
  - **Smoke Curtain:** Sapper L1; Common; Quick; DC 10; yield 1. Thrown, a 20-ft-radius sphere is Heavily Obscured for 1 minute (as *Fog Cloud*). Smoke works even in saferooms.
  - **Popper:** Sapper L1; Common explosive (§6.9).
  - **Antitoxin:** Alchemy L1; Common; 1 shift; DC 10; yield 1.

### 5.3 Procedure (one check per batch)

1. Confirm: saferoom, table level ≥ minimum, recipe known, ingredients and bench supplies in hand, shifts available.
2. Spend the shifts (they can be spread over visits, §2.7).
3. On the last shift, the lead crafter rolls: `[ROLL] Alchemist's Supplies (Int): 1d20 (12) + 3 + 2 PB + 1 table = 18 vs DC 15: success`.
4. Resolve with §6.4 (success, Off Batch, Ruined, Natural 1, Natural 20).
5. The System names the item (§1.7) and logs it; any toast goes out (§8).

### 5.4 Fragmenting Potion Ball (process) [C:V K-030, K-119; numbers HR]

Alchemy L3; Uncommon; 1 shift; DC 13; 1 [Casing] Uncommon + 50 credits; yield 3 empty balls. **Loading** a ball with any potion takes 1 minute in a saferoom (no check). **Throw** (Utilize action, range 30/90): the creature at the point of impact gets the potion's full effect (a harmful potion allows its normal save). **Crawlers are unaffected by thrown potions** [CI; canon: thrown potions work on mobs, NPCs and pets but aren't expected to work on fellow crawlers, K-162]. Yes, your healing ball heals the goblin.

### 5.5 Example recipes

Power levels are pegged to SRD 5.2 / 2024 DMG items of the same rarity. **House numbers are marked [HR].** Recipes that need a table can't be made before Floor 4 (§2.5.2); "Earliest floor" below is the earliest the recipe can be *made* (a blueprint or recipe card may be found earlier).

#### 5.5.1 Mordecai's Special Brew

```text
RECIPE: Mordecai's Special Brew   [C:V item (I-018; K-113, K-115, K-116); mechanics detail C:W (K-114); numbers = core §6.5]
Station:     Alchemy Table L3, run by a CRAFTER NPC (named exception: a Very Rare recipe at L3, as in canon)   Tool: Alchemist's Supplies (Int)   Synergy: Medicine
Rarity:      Very Rare consumable      Earliest floor: F4 (core §6.5 default; DM may place earlier as a special reward)
Ingredients: 1 "Gold Standard Healing Potion" (= Potion of Superior Healing, Rare)
             + 1 "Troll's Second Wind" ([Regenerative][Organ], Rare boss reagent) + 5,000 credits bench supplies
Time:        8 shifts (4 at Alchemy L5)
Check / DC:  Alchemist's Supplies vs DC 18
Yield:       1
Shelf life:  stable in System Inventory (canon: stored potions don't degrade, K-158)
Sickness:    LOCKOUT (see effect). Max 2 per drinker for the whole campaign (BREW-USED n/2).
Effect:      Core §6.5 governs. Bonus Action to drink. For 5 rounds you regenerate at the start of each of your turns
             (10 / 20 / 30 / 40 HP at tiers 1-4), and damage alone can't reduce you to 0 HP. No effect against instant
             death (Power Word Kill, a Disintegrate dust result, decapitation, being blown apart). Afterwards: no other
             potion until 10 hours pass or you finish a Long Rest; a potion drunk during the lockout is wasted (§6.1).
             A third Brew does nothing.
Source:      canon: a 30-second near-immortality brew with ~10 hours of potion sickness and a two-per-drinker cap, made on
             a level 3 Alchemy Table (B3). Not a revive; a canon-verified bypass pre-approved in core §6.4.6.
Price:       NPC crafter fee 5,000 credits + both ingredients (core §6.5). Never on a shelf or the box item roll.
```
**Limits (core §6.5):** the Special Brew is **crafter-NPC-only, and crawlers never brew it** [LOCKED 2026-10-04, decision 013-crafting], matching core §6.5 (no conflict with core; §11). The NPC brews **at most 1 per floor**; a crawler carries **at most 1**; max 2 per drinker. **Crawlers can't learn or brew it**, even with an Alchemy Table L3: the recipe card is never a crawler reward (no mentor lesson, loot page or examine-to-learn result), and a crawler's table never lists it. Crawlers get it by paying the NPC's fee and bringing both ingredients.

#### 5.5.2 Superb Constitution Buff

```text
RECIPE: Superb Constitution Buff Potion   [C:V K-118, K-159, K-160 (the +1 to +4 range is canon); gate and cost HR]
Station:     Alchemy Table L5   Tool: Alchemist's Supplies (Int)   Synergy: Medicine
Rarity:      Very Rare consumable with a PERMANENT effect (counts as a permanent item, core §3.7)   Earliest floor: F6 [HR gate]
Ingredients: 1 [Vital][Organ] Rare (troll, ogre chief, bear boss) + 2 [Herb] Uncommon + 5,000 credits bench supplies
Time:        8 shifts (4 at the required Alchemy L5, which halves brew time, §2.3)
Check / DC:  DC 18
Yield:       1
Shelf life:  stable
Sickness:    standard cooldown (§6.1). STAT CAP: at most TWO buff potions per ability score per crawler, ever (§6.2).
Effect:      Your Constitution score increases permanently by a random amount. Roll 1d4: the score rises by the number rolled
             (+1, +2, +3 or +4). Can't raise a score above 20; any excess is lost. Hit point maximum rises as normal for a
             Con increase.
Source:      canon: permanent +1 to +4 Con at random, max two per crawler per stat (Donut drank two: +1 and +3). The range is
             canon, unchanged. The Very Rare label, the L5 table and the F6 gate are HOUSE (decision 013-crafting): a Rare
             potion averaging +2.5 would out-pace the 2024 Manual of Bodily Health (Very Rare, +2). The score cap of 20 and the
             two-dose cap keep it inside normal 5e growth.
Price:       not sold. Very Rare Platinum-box pull (F6+) or crafted.
```
Other stat buffs (Strength, Dexterity, etc.) use this block with a reagent matched to the stat, the same 1d4 and the same gate.

#### 5.5.3 Heal Critter

```text
RECIPE: Heal Critter Potion   [C:V recipe K-121, K-109; pet rule K-161; numbers HR]
Station:     Bench-free (saferoom) or any Alchemy Table   Tool: Herbalism Kit or Alchemist's Supplies (Int)   Synergy: Animal Handling, Medicine
Rarity:      Common consumable      Earliest floor: F2 (canon F3)
Ingredients: 1 Potion of Healing + 1 cinnamon stick ([Herb] Common, 1 credit at any vendor) + 1 Thistle Rot ([Herb] Common) + 10 credits
Time:        Quick (10 minutes)
Check / DC:  DC 10
Yield:       1
Shelf life:  stable
Sickness:    standard cooldown (applies to the pet)
Effect:      Must be drunk by the target (canon). A crawler can feed it to an adjacent willing pet as a Bonus Action.
             A pet-class creature (companion, familiar, Beast Master beast, Assigned Companion, summoned beast) regains
             4d4 + 4 HP and its Poisoned condition ends. No effect on anything else.
             Standard healing potions and healing scrolls do NOTHING for a pet-class creature (canon, K-161; LOCKED 2026-10-04,
             decision 013-crafting; the v0.2 half-healing toggle is removed). This potion is how you heal a pet.
Source:      canon field recipe: a cinnamon stick into a healing potion, then thistle rot, shake. Pets only.
Price:       75 credits where sold (F3+ alchemical markets).
```

#### 5.5.4 Rapid Detox

```text
RECIPE: Rapid Detox Potion   [C:V K-127 (chapter-cite conflict C:U X-C07); disguise variant C:V K-110; numbers HR]
Station:     Alchemy Table L2   Tool: Alchemist's Supplies (Int)   Synergy: Medicine
Rarity:      Uncommon consumable      Earliest floor: F4 (needs a certified table; canon F3)
Ingredients: 1 [Ichor] Uncommon + 1 [Herb] Common + 50 credits
Time:        2 shifts
Check / DC:  DC 13
Yield:       2
Shelf life:  stable. DISGUISED variant: add 1 sage-beetle ichor ([Ichor] Common). The item has NO System description
             (Int (Investigation) DC 15 to identify), but it spoils 1 hour after leaving System Inventory.
Sickness:    standard cooldown
Effect:      Ends the Poisoned condition if caused by alcohol, drugs or other intoxicants, and you're immune to intoxication
             from those sources until you descend to the next floor. Advantage on saves against ingested poisons for the
             same time. No effect on magical poisons, diseases or curses. The DM may name one floor drug it can't beat
             (canon had one).
Source:      canon: clears alcohol and most drugs for one floor; Mordecai disguised doses with sage beetle ichor.
Price:       200 credits where sold.
```

#### 5.5.5 Liquid Therapy

```text
RECIPE: Liquid Therapy   [CI; canon K-130, K-033; numbers HR]
Station:     Alchemy Table L4 (canon needed an upgraded table)   Tool: Alchemist's Supplies (Int)   Synergy: Medicine, Insight
Rarity:      Rare consumable      Earliest floor: F6 (canon F8)
Ingredients: 1 [Spirit] Rare + 1 [Herb] Uncommon + 1 [Ichor] Uncommon + 500 credits
Time:        4 shifts (2 at L5)
Check / DC:  DC 15
Yield:       2
Shelf life:  stable
Sickness:    standard cooldown
Effect:      Until you next finish a Long Rest (canon: "until you sleep"): Advantage on saves against the Blinded, Charmed,
             Frightened and Stunned conditions and against madness/confusion effects (e.g. Confusion, Phantasmal Killer).
             Once during that time, when you fail one of those saves, you can succeed instead.
Source:      canon brew against insanity, blindness and other debuffs, made for a boss fight after a table upgrade.
Price:       not on shelves; mentor NPC 1,500 credits + ingredients.
```

#### 5.5.6 Dolores Doesn't Splat (falling only)

```text
RECIPE: Dolores Doesn't Splat   [CI; canon K-128, K-181; numbers HR]
Station:     Alchemy Table L2   Tool: Alchemist's Supplies (Int)   Synergy: Acrobatics, Arcana
Rarity:      Uncommon consumable      Earliest floor: F4 (canon F5)
Ingredients: 1 [Phase] Uncommon + 1 [Hide] Uncommon (something bouncy) + 50 credits
Time:        2 shifts
Check / DC:  DC 13
Yield:       1
Shelf life:  stable
Sickness:    standard cooldown
Effect:      FALLING ONLY. Drink as a Reaction while falling, ONLY if the potion is in hand or on a bandolier, and ONLY if
             you've already fallen 100 ft or more in this fall (canon: it only works at very high speed). When you land,
             you take NO falling damage. Instead you bounce 5 times, rising 15 ft each time, and come to rest Prone in an
             unoccupied space within 30 ft of the impact (DM's choice, for comedy). Each creature you bounce on takes 1d6
             bludgeoning. No effect on any other damage. Drunk too early (under 100 ft), it's wasted.
             In plain words: a mid-fall potion that only works once you've already fallen 100 ft. Sooner and it's a wasted
             bottle; the threshold is HOUSE and stays at 100 ft [LOCKED 2026-10-04, decision 013-crafting].
Source:      canon fall potion: works only above ~200 km/h; five bounces, 15 ft between; it got the Syndicate's brewing rules
             rewritten. Not the same as Half-Splat (core §6.5): Dolores is high-fall only and drunk mid-fall; Half-Splat is
             primed in advance and leaves you at 5%.
Price:       200 credits where sold (rarely).
```

#### 5.5.7 Jug O' Boom

```text
RECIPE: Jug O' Boom   [C:V recipe K-125, K-095, K-097; canon price K-126 not used; numbers HR]
Station:     Bench-free (saferoom; named exception, canon made it without a table) or Sapper's Table L1
             Tool: Alchemist's Supplies (Int) or Tinker's Tools (Dex)   Synergy: Sleight of Hand
Rarity:      Uncommon explosive (incendiary)      Earliest floor: F2
Ingredients: 1 moonshine jug ([Accelerant][Casing] Uncommon; poured down to 3/4) + a couple of ounces of goblin oil
             ([Accelerant] Common) + 1 torch as the cork + 50 credits
Time:        1 shift
Check / DC:  DC 13
Yield:       1
Shelf life:  bench-free: leaves Steady (canon: the torch cork makes it much more stable). From a Sapper's Table: Stable.
Sickness:    none
Effect:      Utilize action to throw at a point within 20/60 ft. 10-ft-radius sphere: DC 13 Dexterity save, 3d6 fire damage,
             half on a success. The area burns for (2 + your IED rank) rounds; a creature that enters it or ends its turn
             there takes 1d6 fire. Flammable objects ignite. Loot rule applies (§4.3).
Source:      canon: a moonshine jug, goblin oil and a torch cork; flames last longer with more incendiary skill; invented on F2.
Price:       200 credits (5e Uncommon consumable). Canon's 7,500 gold isn't used; vendors pay more for the plain moonshine.
```

#### 5.5.8 Mother of All Bombs (MOAB)

```text
RECIPE: Mother of All Bombs   [CI; canon K-137 (three-crawler build on F2, four "baby" bombs, used as a lure); numbers HR]
Station:     Engineer's Table L2 (multi-part), OR L1 as a GROUP BUILD (3 crafters, DC +2)
             Tool: Tinker's or Carpenter's Tools; payload from a Sapper's Table or bench-free   Synergy: Investigation
Rarity:      Uncommon build (launcher) + 4 Uncommon payloads      Earliest floor: F4 to build (needs a certified Engineer's Table; the DM may place the blueprint from F2)
Ingredients: Launcher: cart/trailer chassis ([Metal] Common x3) + 1 [Trigger] Uncommon + 100 credits.
             Payload: 4 "baby" bombs, each a Banger-class explosive (§6.9), crafted separately.
Time:        launcher = 3 parts x 2 shifts (chassis, rack, firing rig), then the assembly check
Check / DC:  each part DC 13; assembly DC 13 (DC 15 as an L1 group build)
Yield:       1 launcher (Large object, AC 13, 40 HP, towable; too big for System Inventory)
Shelf life:  launcher permanent; racked, unfired bombs count as Stable [HR]
Sickness:    none
Effect:      SALVO (Utilize action by a crew member within 5 ft): fire 1-4 loaded bombs at points within 120/480 ft, each
             point within 20 ft of another. Each bomb: 10-ft-radius sphere, DC 13 Dexterity save, 3d6 fire + 1d6 thunder,
             half on a success. A creature in more than one blast saves ONCE, at Disadvantage, and takes one blast's damage.
             LURE: instead of firing, run the siren; creatures that hunt by sound within 1 mile notice and come (DM's call).
             Reload = 4 new baby bombs.
Source:      canon: built by three crawlers on Floor 2; launches four smaller bombs; used to draw a monster away.
Price:       not sold. Reload bombs at Banger prices.
```

#### 5.5.9 Jelly Bomb (contact mine)

```text
RECIPE: Jelly Bomb   [CI; canon K-134, K-135, K-056; numbers HR]
Station:     Sapper's Table L3   Tool: Tinker's Tools (Dex)   Synergy: Sleight of Hand
Rarity:      Rare explosive (mine)      Earliest floor: F4
Ingredients: 1 [Explosive] Uncommon (dynamite stick) + 2 [Explosive] Common (lobbers to stuff the tube) + 1 [Casing] Uncommon
             (spiked tube) + 1 [Trigger] Uncommon (plunger; needs a workbench hardening tool like canon's, or DC +2) + 500 credits
Time:        4 shifts
Check / DC:  DC 15
Yield:       2
Shelf life:  STABLE against everything except heavy impact (canon, K-135): only Heavy Impact triggers an early-detonation roll.
Sickness:    none
Effect:      Place it (Utilize action); it arms after 1 minute. It goes off when a Medium or larger creature, or a vehicle, puts
             weight on it: 15-ft-radius sphere, DC 15 Dexterity save, 6d6 piercing + bludgeoning, half on a success. Vehicles,
             constructs and structures take DOUBLE damage. Spotting an armed mine: Wisdom (Perception) DC 15.
             Explosives Handling 3+: you can pick it up again safely.
Source:      canon: spiky contact mines made from a dynamite stick and stuffed tubes, plungers shaped with a hardening tool,
             built to derail a train; stable against everything but heavy impact.
Price:       not sold.
```

#### 5.5.10 Hobgoblin Disco Ball

```text
RECIPE: Hobgoblin Disco Ball   [CI; canon K-138 (infusion; the thrower isn't immune), K-018, K-172; numbers HR]
Station:     Sapper's Table L3 (INFUSION)   Tool: Alchemist's Supplies (Int)   Synergy: Sleight of Hand, Arcana
Rarity:      Rare infused tossable      Earliest floor: F4
Ingredients: 1 Smoke Curtain (Common, §5.2) + 1 Potion of Invisibility OR 1 [Phase] Rare reagent + 500 credits
Time:        4 shifts
Check / DC:  DC 17 (Rare 15 + infusion 2). ANY failure makes it a DUD (§6.5).
Yield:       1
Shelf life:  UNSTABLE (all infused items, §6.8)
Sickness:    none
Effect:      Utilize action to throw at a point within 30/90 ft. A 20-ft-radius sphere of glittering smoke fills the area for
             1 minute (a strong wind disperses it). The area is Heavily Obscured, and EVERY creature inside it, including
             you, has the Invisible condition while inside. LIGHT-REACTIVE: bright light in the cloud (a torch, Light,
             Daylight) makes it strobe; creatures within 10 ft of the light source lose Invisible while there and are
             outlined in sparkles. It's smoke, not an explosive, so it works in saferooms (the System bills you for cleaning).
Source:      canon: a smoke curtain soaked in an invisibility potion at a Sapper's Table; the thrower isn't immune.
Price:       not sold.
```

#### 5.5.11 Royal Chariot

```text
RECIPE: Royal Chariot (tracked all-terrain vehicle)   [CI; canon K-141, K-012 (Engineer L2, two builders, F5); numbers HR]
Station:     Engineer's Table L2 (multi-part; Large)   Tool: Tinker's Tools (Dex) or Smith's Tools (Str)   Synergy: Investigation, Athletics
Rarity:      Uncommon permanent build (counts as a permanent item, core §3.7); Rare with a weapon mount (L3)   Earliest floor: F5
Ingredients: chassis ([Metal] Rare x1 + [Metal] Common x4), tracks ([Hide] or [Metal] Uncommon x2),
             engine core ([Arcane] or [Accelerant] Uncommon x1, or a boss engine part) + 200 credits
Time:        3 parts x 2 shifts, then assembly (1 shift)
Check / DC:  each part DC 13; assembly DC 13
Yield:       1 vehicle
Shelf life:  permanent; burns 1 fuel charge ([Accelerant] Common) per 8 hours of driving
Sickness:    none
Effect:      Large vehicle. AC 15, 60 HP, damage threshold 5, immune to poison and psychic damage. Speed 40 ft; ignores
             difficult terrain from sand, snow, mud and rubble. Driver + 3 passengers (passengers have Half Cover). The
             driver uses their own actions (Dash, Dodge, etc.). Ramming [HR]: driver makes a Dexterity check (DC = target's
             AC); on a hit, 2d10 bludgeoning to the target and half that to the Chariot. Stored only in an Enhanced
             Crafting Studio garage (§2.1). Optional L3 weapon mount holds one crafted launcher (e.g. a MOAB rack).
Source:      canon: a tracked vehicle for sand and snow, built at a level 2 Engineer's Table by two crawlers on Floor 5.
Price:       not sold.
```

---

## 6. Limits and failure

### 6.1 Potion cooldown and potion sickness [CI; canon K-155, K-156, K-157; **LOCKED: 1 round**, decision 011]

- **Cooldown: 1 round.** After you drink any potion you're on **cooldown** until the start of your next turn, so you can drink **at most one potion per round**. This replaces the v0.1.1 "3 − Constitution modifier" rule everywhere; Constitution no longer matters (canon ties cooldown length to Con, K-155; we simplified on purpose). Outside combat it is the same: one potion per round (about 6 seconds).
- **Drinking during cooldown:** the potion **still works**, but you gain the **Poisoned** condition for 1 minute (DC 12 Constitution save at the end of each of your turns ends it). Canon gives the Poisoned status [K-155].
- **Special Brew keeps its own lockout (core §6.5), separate from this cooldown.** Mordecai's Special Brew has its own **10-hour lockout** (ends at 10 hours or a Long Rest, whichever is first) and a **maximum of 2 per drinker** for the whole campaign, exactly as core §6.5 and §5.5.1 say. The 1-round cooldown never shortens, extends, replaces or restarts the lockout, and the lockout is not "a longer cooldown". While the lockout is on, any other potion you try to drink is **wasted** (core §6.5: the System announces the failure and bills for it); the cooldown's Poisoned penalty is not added on top. The Brew is itself a potion: drunk within another potion's 1-round cooldown it still works and you are Poisoned as above. Hit Point Dice from rests are not potions.
- **Exempt:** spell scrolls (healing spells included) and **Cooking** meals (§7.1). Canon: healing scrolls skip the countdown, and some food buffs aren't potions [K-157]. Monsters have no cooldown; NPCs do [C:V K-156].
- **Storage:** potions in System Inventory don't degrade [C:V K-158].

### 6.2 Stat-buff cap [C:V K-159, K-160]

A crawler benefits from **at most two buff potions per ability score** for the whole campaign (log `STATBUFF: CON 1/2`). A third does nothing, still counts as a potion for cooldown, and earns a toast. Canon's box-only "Cosmic" buffs are a separate type outside this cap [C:V K-132]. Here they're Legendary loot only, DM-placed, and count against core §3.7.

### 6.3 Pets and thrown potions

**Standard healing potions and healing scrolls have no effect on pet-class creatures** [C:V K-161; **LOCKED 2026-10-04**, decision 013-crafting, "go with Lore for canon"; the v0.2 half-healing toggle is gone]. Use Heal Critter (§5.5.3). That includes a healing potion thrown or splashed at a pet (canon's K-162 line that thrown potions "should work on NPCs and pets" is flagged there as an open question; here K-161 wins). Thrown or splashed potions don't affect crawlers [CI K-162].

### 6.4 Check results

*With Steady Hands on (the default, §2.7) nothing is rolled: only the success, Off Batch, Ruined and Dud rows apply, from the margin below the DC. Natural 1, Natural 20 and Success by 10+ apply only to a craft the crafter chose to roll.*

| Result | Outcome |
|---|---|
| **Success** | Yield as listed. |
| **Success by 10+** | Roll once on the **Natural 20 table** (§6.7); keep only results 1-3 (reroll 4-6). |
| **Fail by 1-4: Off Batch** | Nothing made. **Keep the highest-rarity ingredient**; lose the rest and the bench supplies. Infusions: the item is a **Dud** (§6.5). |
| **Fail by 5+: Ruined** | All ingredients and supplies lost. Infusions: **Dud**. Toast optional (§8.1). |
| **Natural 1** | Ruined **and** roll on the **critical failure table** (§6.6). |
| **Natural 20** | Success **and** roll on the **Natural 20 table** (§6.7). |

### 6.5 Dud status [C:V K-069, K-172]

A failed infusion leaves a **Dud**. It looks normal; the System label shows **(Dud)** only on a Demolitions Workshop readout or an Int (Investigation) DC 15 check. Using it does nothing except a sad *pfft*. **Salvage:** at a Sapper's Table L3 with Bomb Surgeon, recover half the ingredients (round down). **Dud's revenge** [HR]: if a Dud is on your person (not in System Inventory) when you take fire or lightning damage, roll d20. On a 1, it remembers what it was supposed to be: resolve it as the intended item, centered on you.

### 6.6 Critical failure table (d12, saferoom-safe) [HR]

Rolled crafts only (not Steady Hands, §2.7).

Explosives are inert in a saferoom, so the "explosions" are loud, colorful and humiliating rather than lethal. Mishap damage can't drop a crawler below 1 HP (§1.5).

| d12 | Mishap | Effect | [SYSTEM] line |
|:-:|---|---|---|
| 1 | **Glitter Event** | You, the table and your next three meals are coated in pink glitter: Disadvantage on Stealth until your next Long Rest. | "Fabulous. Visible from orbit." |
| 2 | **Inert Boom** | The bomb "goes off" without exploding: a flash, a bang, no eyebrows. Deafened for 1 hour. | "Explosives are inert in saferooms. Your eyebrows were not." |
| 3 | **Fume Event** | DC 13 Con save or Poisoned for 1 hour; everyone in the Personal Space smells it. | "Congratulations, you invented a new smell. We've named it after you." |
| 4 | **The Bench Bites** | 1d6 fire, acid or slashing (DM's pick). | "Please keep your hands inside the ride." |
| 5 | **Table Sulks** | That table can't be used until your next Long Rest. | "Your table has filed a complaint with HR." |
| 6 | **Mislabeled** | You get an item, but the System named it after something else. The DM secretly picks what it really is (a Common potion or a Dud). | "Product may not match description. Product never matches description." |
| 7 | **It's Alive** | One ingredient wasn't dead. A CR 0 critter escapes into the saferoom and becomes the party's problem (or pet). | "Mazel tov. It's a boy. Probably." |
| 8 | **Tool Down** | Your tool kit breaks: repair for half its price, or *Mending*. | "Have you tried turning it off and never on again?" |
| 9 | **Sponsor Sighting** | A sponsor stamps its logo on your failure; the System bills you an "ad slot" of 10 × the bench supplies. | "This disaster was brought to you by someone who isn't you." |
| 10 | **Recipe Amnesia** | Disadvantage on this recipe's next attempt. | "Muscle memory not found. Have you tried having muscles?" |
| 11 | **Chain Reaction** | One other unfinished project on the same table loses half its shifts. | "Good news: you're consistent." |
| 12 | **Ratings Gold** | Spectacular and harmless. The crafter gains Heroic Inspiration (Crowd Pop, core §5.1). | "The audience would like you to fail like that again. Daily." |

### 6.7 Natural 20 table (d6) [HR]

Rolled crafts only (not Steady Hands, §2.7).

| d6 | Bonus |
|:-:|---|
| 1 | **+1 yield** (for a build: +10 HP or +1 AC). |
| 2 | **Steadier:** an explosive leaves one stability step better; a spoilable potion lasts 1 day longer. |
| 3 | **Masterwork:** explosive save DC +1, **or** one potion healing die counts as its maximum, **or** a buff's duration doubles. |
| 4 | **Leftovers:** keep the highest-rarity ingredient. |
| 5 | **Flow state:** your next recipe this saferoom visit takes 1 fewer shift (minimum Quick). |
| 6 | **The System is impressed (and hates it):** an R1-R2 toast (Title or Heroic Inspiration). |

### 6.8 Explosives: stability, early detonation, decay

**Inert in saferooms** (and Personal Spaces) [C:V K-170]. **Stable on the Sapper's Table** [C:V K-017]; the protection ends when an item leaves the table [C:V K-022].

**Stability ladder** [HR; canon only says stability varies, decays and can be read off a menu, K-063]:

| Step | Early-detonation roll (d20) | Default for |
|---|:-:|---|
| **Stable** | 1, and **only on a Heavy Impact** | non-infused items from a Sapper's Table L2+; Jelly Bomb |
| **Steady** | 1-2 | Sapper's Table L1 items; bench-free Jug O' Boom |
| **Volatile** | 1-4 | other bench-free explosives; anything that has decayed once |
| **Unstable** | 1-6 | **all infused items** [C:V K-172] |

- **Jolts** trigger a roll for each stack of identical explosives carried **on your person** (not in System Inventory): you take a critical hit; you take fire or lightning damage; you fall 10+ ft; you're knocked Prone; you fail a save against an area effect. **Heavy Impact** (the only trigger for Stable items): a critical hit that deals bludgeoning damage, a fall of 20+ ft, or 20+ damage from one hit.
- **On a detonation**, the item goes off centered on the carrier. A stack detonates as one item, +1 damage die per extra item (max +4 dice).
- **IED** improves the early-detonation roll by one step per rank (§3.1).
- **Decay:** for every **8 hours** an explosive spends on your person (16 hours in an equipped backpack [C:V K-171]), it drops one step. An Unstable item that decays again rolls 1-6 to detonate; otherwise it becomes a Dud.
- **System Inventory is time-locked** [HR, mirroring canon potion storage K-158]: no decay, no Jolts. The cost is action economy: getting an item out uses your free object interaction or the Utilize action (core §5.9). Legendary devices may carry "**detonates when removed from inventory**" [C:V K-136] (DM only).

### 6.9 Blast tiers (5e damage dice and areas) [HR]

Thrown with the **Utilize action**, range **20/60 ft** (balls 30/90). Beyond normal range, roll d20: on a 1-5 it lands 1d4 × 5 ft off in a random direction (d8). It detonates on landing unless the recipe says timer or mine. **Save: Dexterity, half damage on a success.** Objects and structures take **double** damage.

| Tier | Rarity | Damage | Area (default sphere) | Save DC | Earliest floor | Price (credits) | Bench supplies |
|---|---|---|---|:-:|:-:|---:|---:|
| **Popper** | Common | 2d6 | 5-ft radius | 12 | F1 | 50 | 10 |
| **Banger** | Uncommon | 4d6 | 10-ft radius | 13 | F2 | 200 | 50 |
| **Boomer** | Rare | **6d6 below level 5; 8d6 at level 5+** [LOCKED, decision 012] | 20-ft radius | 15 | F4 | 2,000 | 500 |
| **Wrecker** | Very Rare | 12d6 | 30-ft radius | 17 | F8 | 20,000 | 5,000 |
| **Doomsday-class** | Legendary | 16d6 + a rider | 40-ft+ radius | 19 | F13, **DM only** | not sold | 25,000 |

- **Damage type** by recipe: fire, thunder, bludgeoning or piercing (shrapnel); dice may be split across two types.
- **Shapes:** swap the sphere for a **cone** (Popper 15 ft, Banger 30 ft, Boomer 60 ft, Wrecker 90 ft) for directional charges (canon breaching charges blast in a vertical cone, K-147), or a **line** twice the radius long and 5 ft wide for breaching.
- **Feature trade:** a recipe may give up 2 damage dice for one feature: mine trigger, timer, incendiary area (1d6 per round for 2 + IED rank rounds), smoke, double damage to vehicles/structures, or homing (no scatter).
- **Boomer level gate [LOCKED, decision 012].** **Below level 5 a Boomer deals 6d6. At level 5 and higher it deals 8d6.** The 20-ft radius, DC 15, price, cone option and everything else are unchanged. The test uses the party's average level, rounded down (the crawler's own level for a solo crawler), **at the moment the Boomer detonates**, so a stored Boomer needs no relabeling when the party levels (**LOCKED 2026-10-04**, decision 013-crafting: not the crafter's level, not the lowest-level crawler). Feature trades, scatter and IED's bonus (§3.1) all use the dice currently in force (6 or 8).
- **Benchmarks:** at level 5+ a Boomer is *Fireball*-class (8d6, a Rare consumable); below level 5 it is deliberately a die-pair weaker (6d6) so the Floor 4 Boomer doesn't flatten a level-3 party. A Popper is a bit better than Alchemist's Fire, with area.
- **Bigger explosives approved [LOCKED 2026-10-04, decision 013-crafting; Caleb: "as long as it is appropriate for mobs"].** These stay as drafted: (1) the **Wrecker** (12d6, 30 ft, DC 17, F8); (2) the **stack rule** (§6.8: +1 die per extra item, max +4), so a carried stack of Boomers can pass the 6d6 cap (3 Boomers = 8d6 even below level 5); (3) **IED rank II** (earliest F4), which adds +6 to a 6d6 Boomer (average 27); (4) the **Jelly Bomb** mine (6d6 over 15 ft, Rare, double to vehicles).
- **GM note: scale the mobs, not the bombs.** Whenever the party brings these to a fight (a Wrecker, a carried stack, an IED-boosted Boomer, a mine laid in a corridor), build the enemy side to match: raise the encounter one difficulty band (e.g. Moderate to High), or add mob HP (about +25-50%) and/or mob count, and prefer packs and groups over a lone target a single blast deletes. Telegraph the stakes before the throw (core §2.5.6). The same blast hits crawlers too (Wrecker average 42 damage): a level-3 crawler can die to a friendly Wrecker, so the AI GM states the area first and never fudges the save. Check the party's blast kit against the encounter math in the floor doc when a new tier unlocks (Boomer F4, Wrecker F8).

**Friendly fire.** Blasts don't check uniforms: crawlers in the area save like anyone else. The DM states the area before the throw is confirmed (core §2.5.6: name the stakes). Early detonations and scatter are where the comedy (and the deaths) happen; the System toasts each one (§8.1; core §6.9 has the friendly-fire death line).

**Loot loss:** see §4.3 (fire and explosions destroy reagents).

**Price/credits:** explosives use the table above (half the 2024 DMG item value by rarity, the consumable rule). Canon prices (a jug bomb at 7,500 gold, dynamite at 20 for 20,000 gold [C:V K-100, K-126]) come from an inflated economy and **aren't used**.

---

## 7. House-rule stations (no canon page defines these) [HR]

Canon names some tables (Writing Table, Printing Press, Tinker's Table, Repair Bench) but no local source defines Cooking, Smithing, Enchanting or Scribe stations or skills [C:U X-C10]. **Everything in this section is HOUSE RULE; keep it light.** **All four stations (Cooking, Smithing, Enchanting, Scribe) are kept and marked HOUSE** [LOCKED, decision 011]. Each uses the generic ladder (§2.3) and the §2.7 time/gold/DC numbers.

### 7.1 Cooking (Kitchenette, Personal Space accessory) [HR]
- Tool: Cook's Utensils (Wis); synergy Survival. Ingredients: [Food].
- A **meal** isn't a potion (no cooldown). Canon flavor: some food buffs aren't potions (K-157), though canon treated one character's tea as a potion (K-086); here it doesn't.
- One meal buff at a time, lasting until your next Long Rest. Feeds up to 6. **Common** (L1): temporary HP = your Proficiency Bonus + Con modifier. **Uncommon** (L2): Advantage on one save type the cook names. **Rare** (L3): +1d4 to one skill's checks.

### 7.2 Smithing (Forge; folds into Engineer / Armorer / Metal Working) [HR]
- Tool: Smith's Tools (Str). Makes **mundane** weapons and metal gear at 2024 PHB crafting costs (raw materials = half price), but in shifts: 1 shift per 50 credits of item value (minimum 1).
- Magic weapons need Enchanting (§7.3). Armor goes through the Armorer's Workshop (canon).

### 7.3 Enchanting (Enchanter's Bench, F4+) [HR]
- Needs the item's craft tool **and** Arcana proficiency, plus a **DM-granted formula** for the specific item (2024 DMG crafting magic items, compressed): Uncommon 6 shifts, Rare 12, Very Rare 24, Legendary DM only. Bench supplies per §2.7, plus one reagent of the item's rarity.
- Only **SRD 5.2 / 2024 DMG** items at or below the floor's **default** rarity (core §3.6). Each counts against the floor's permanent-item budget (core §3.7). The attunement cap of 3 still applies.
- Never: revival items, Artifacts, Celestial rewards.

### 7.4 Scribe (Writing Table) [HR]
- Tool: Calligrapher's Supplies (Dex); synergy Arcana. Uses the 2024 PHB spell-scroll scribing rules (you must have the spell prepared or known), converted to shifts: 1 shift per spell level (minimum 1), **halved** on a Writing Table (canon: it makes scroll writing more efficient, K-047).
- Scrolls skip potion cooldown (§6.1). Printing Press (L5+, DM only): 2 copies per run.

---

## 8. System voice and achievement seeds

Voice tags per decision 007. `Reward:` goes on its own line (it stays in the System voice until the next tag). Keep toasts short (core §9).

### 8.1 Failed batches

```text
[SYSTEM] Batch failed! Your potion has achieved the consistency of regret.
[SYSTEM] Ingredients consumed: all of them. Product produced: a lesson. Lessons are non-refundable.
[SYSTEM] Alert! You have successfully combined three rare reagents into one medium-rare disappointment.
[SYSTEM] Your mixture has been classified as "soup." It is not even good soup.
[SYSTEM] Early detonation! Production thanks you for the free fireworks. Your teammates do not.
```

### 8.2 First table receipt (story event script; Floor 2 drop or Floor 1 find)

```text
[SYSTEM] Ding ding ding! Congratulations, Crawler! You have received a CRAFTING TABLE.
[SYSTEM] Status: PENDING CERTIFICATION. Tables may not be used before Floor 4. Store it somewhere safe. It weighs nothing. It will still gain experience, unlike you.
[SYSTEM] A Personal Space will be assigned to you on certification. Its door will appear in any certified saferoom. Do not ask about the rent. You cannot afford the answer.
[SYSTEM] Crafting is permitted in saferooms only. Explosives are inert in saferooms. This is not a challenge. It is a policy, and our lawyers are very tired.
[SYSTEM] Tables come with tools and supplies. Recipes are sold separately. Recipes are not sold.
[SYSTEM] NEW ACHIEVEMENT: Some Assembly Required!
[SYSTEM] You own furniture now. In a dungeon. You may not use it yet. Your mother would be so confused.
Reward: one (1) starter recipe and the crushing weight of responsibility.
```

### 8.2b Table certification (Floor 4)

```text
[SYSTEM] Floor 4 safety inspection complete. Your furniture has been CERTIFIED. It passed on a technicality. The technicality was money.
[SYSTEM] A door has appeared. Behind it: a room. In the room: your table. Crafting is now permitted, in saferooms only, as previously explained, slowly, with diagrams.
```

### 8.3 Dud

```text
[SYSTEM] Infusion failed. Your item now has the Dud status. Like your last relationship, it looks fine from the outside.
[SYSTEM] Pfft. That was the sound of your bomb. That was also the sound of the audience.
[SYSTEM] Dud detected. Please do not shake it. It won't help, but it's funny for us.
```

### 8.4 Crafting achievement seeds (log as `NEW:`)

Format for every toast:

```text
[SYSTEM] NEW ACHIEVEMENT: <Name>!
[SYSTEM] <what they did, as an accusation>
Reward: <punchline first, item second>
```

| Seed | Trigger | Tier | Toast body / Reward line (original) |
|---|---|:-:|---|
| **Some Assembly Required** | First table received (the Floor 2 drop, or a Floor 1 find; usable only after Floor 4 certification) | R1 + starter recipe | See §8.2. |
| **Early Adopter** | Found a table through the Floor 1 random find (§2.5.1) | R1 (Title) | "You found office furniture on Floor 1. Nobody was supposed to find that." / Reward: Title, "Early Adopter." The System hasn't decided whether you're a bug. |
| **Pending Certification** | Had a carried or stashed table certified on arrival at Floor 4 (§2.5.2) | **R0** | "You carried a coffee table through three floors. It passed inspection." / Reward: paperwork. Stamped. |
| **Home Economics** | First successful recipe at a certified table, Floor 4 or later (canon parallel: a first-workbench achievement paid a Bronze Crafter's Box of pliers, a tape measure and pink glitter, K-013/K-014) | R1-R5 | "You made a thing on purpose." / Reward: a Bronze Crafter's Box. It contains tools. And glitter. The glitter is forever. |
| **Fizzle, Fizzle, Little Star** | First Dud | **R0** | "You put a potion in a bomb and made neither." / Reward: none. It's a Dud. Like the bomb. |
| **OSHA Has Left the Chat** | An early detonation on your own person | **R0** | "Self-inflicted explosion. Ratings up. Eyebrows down." / Reward: your eyebrows will grow back. Probably. |
| **Friendly Fire Sale** | Your crafted explosive damages an ally | **R0** | "Everything must go, including [Ally]'s left boot." / Reward: [Ally]'s opinion of you. |
| **Two Is the Limit, Sweetie** | Drank a third stat buff or a third Brew | **R0** | "You drank a potion that can't work on you." / Reward: hydration. |
| **The Recipe Was a Suggestion** | First invented recipe that stacks (canon Dungeonpreneur, K-176) | R3 + royalties (**LOCKED 2026-10-04**: the small credit trickle stays) | "You invented something. It will be used to kill people you'll never meet." / Reward: 1d6 × 10 credits at each descent while it's in the Codex. |
| **Unlicensed Pharmacist** | Sold 5+ crafted items to one vendor on one floor | **R0** | "You flooded the market. The market would like a word." / Reward: the vendor now pays you a quarter. Oh wait, it already did. |
| **Bounce House** | Survived a fall with Dolores Doesn't Splat | R1 | "You bounced five times. The judges gave you a 6.5." / Reward: Title, "Rubber Crawler." |

The catalog's existing per-floor **Field Craft** and **Kit Bash** rows (e.g. ACH-0202/0203 on F1, ACH-0240/0241 on F2) cover "craft or cook once" and "combine two junk items." A **Kit Bash** is a bench-free Common recipe (Quick, DC 10, any proficient tool) made in a saferoom. Both are bench-free, so they stay open on Floors 1-3 while tables are uncertified.

---

## 9. Balance guidance

### 9.1 Price table (credits = GP)

| Item | Price | Notes |
|---|---:|---|
| Consumable list price by rarity | 50 / 200 / 2,000 / 20,000 / not sold | Common / Uncommon / Rare / Very Rare / Legendary (half the 2024 DMG value, the consumable rule) |
| Crafted item sold to a vendor | **¼ of list** | Vendors buy at most **5 crafted items per crawler per floor**; ordinary loot still sells at ½ (core §5.10) |
| Bench supplies by rarity | 10 / 50 / 500 / 5,000 / 25,000 | §2.7 |
| Ingredients buy / sell | 10/5 · 50/25 · 500/250 · 5,000/2,500 | §4.1; Legendary not sold |
| Basic table (F4+) | 5,000 on F1-2; F3-18 per §9.1a | LOCKED base (decision 012, repriced 2026-10-04); canon ~25,000 (K-011). From v0.3.4 the price follows the §9.1a schedule, not the credit multiplier (decision 030) |
| Crafting Studio (F4+) | 12,000 on F1-2; F3-18 per §9.1a | [HR] (Caleb 2026-10-04; was 20,000); coupon-eligible while the schedule price is 25,000 or less |
| Enhanced Crafting Studio (F6+) | 30,000 on F1-2; F3-18 per §9.1a | [HR] (Caleb 2026-10-04; was 50,000) (canon infobox 255,000 gold, C:W K-008); above the coupon cap |
| Table level upgrade | 5,000 × target level | L2 10,000 · L3 15,000 · L4 20,000 · L5 25,000 · L6 30,000; above L6 DM only. A coupon covers L2-L5 |
| Upgrade Coupon | one table purchase or one level upgrade ≤ 25,000 | LOCKED cap (decision 012); non-stackable, no change (canon K-049); about 1 per crawler per 2 floors from Quest/Boss Boxes |
| NPC brew fees | per core §6.5 | Brew 5,000 and Lifesaver Draught 2,500 (both NPC-only, no crawler recipe) |

### 9.1a Workstation price schedule (v0.3.4; decision 030)

Prices in credits for the floor where the purchase happens. **Floors 1 and 2 keep the ruled prices: basic table 5,000, Crafting Studio 12,000, Enhanced Crafting Studio 30,000.** The schedule below starts at Floor 3 and replaces the credit multiplier for these three prices only. Targets: about **3 floors** of liquid income for a basic table, **6** for a Crafting Studio, **10** for an Enhanced Crafting Studio (liquid income = a crawler's expected credits per floor if every box item is sold at half, `rules/70-encounter-budget-5e.json` growth table; income from F3 up is a placeholder, so the GM may adapt these). A table is still unusable until Floor 4 (§2.5), a Crafting Studio is sold from F4 and an Enhanced Crafting Studio from F6, so "n/a" means not on sale yet.

| Floor | Basic table | Crafting Studio | Enhanced Crafting Studio |
|---|---:|---:|---:|
| 1-2 | 5,000 | 12,000 | 30,000 |
| 3 | 5,500 | n/a | n/a |
| 4 | 6,500 | 12,500 | n/a |
| 5 | 9,000 | 18,500 | n/a |
| 6 | 13,000 | 26,000 | 43,000 |
| 7 | 15,000 | 30,000 | 50,000 |
| 8 | 17,500 | 35,000 | 58,000 |
| 9 | 42,000 | 84,000 | 140,000 |
| 10 | 56,000 | 110,000 | 185,000 |
| 11 | 64,000 | 130,000 | 215,000 |
| 12 | 75,000 | 150,000 | 250,000 |
| 13 | 165,000 | 330,000 | 550,000 |
| 14 | 190,000 | 380,000 | 635,000 |
| 15 | 210,000 | 420,000 | 700,000 |
| 16 | 245,000 | 490,000 | 815,000 |
| 17 | 285,000 | 570,000 | 945,000 |
| 18 | 330,000 | 660,000 | 1,100,000 |

Notes. (1) Prices never fall from one floor to the next. (2) The Upgrade Coupon cap stays **25,000** (§2.6): a coupon pays for a workstation only while its schedule price is 25,000 or less (basic table through F8, Crafting Studio through F5 at 18,500, since F6 is 26,000); above that, pay credits. (3) Table level upgrades (5,000 × target level), bench supplies, ingredients and shop prices are **not** part of this schedule and still take the core §3.9 credit multiplier (§0); whether level upgrades should follow a schedule too is an open follow-up. (4) Tables still upgrade on **any** floor from F4 (§2.4); that ruling is unchanged.

### 9.2 Per-floor availability (standard track)

| Floors | Tables | Typical table level | Recipe rarity (default / peak) | Explosive tiers | Vendor reagents | Unlocks |
|---|---|:-:|---|---|---|---|
| **1-2** | Found only; party 0-1 per floor. **First table: Floor 2 (LOCKED)**; very rare Floor 1 find (5%, §2.5.1). **All tables are uncertified tokens, carried or stashed, unusable until Floor 4** (§2.5.2) | none in use (tokens L1) | Common / Uncommon | Popper; Banger (F2); named bench-free recipes only (Jug O' Boom, §2.5.2) until F4 | Common | Kit Bash, starter recipe cards (greyed out), bench-free recipes (Heal Critter, Jug O' Boom, F2); MOAB blueprint (F2, DM; build F4) |
| **3** | Found only (tokens); no leveling before certification | tokens L1 | Uncommon / Rare | Banger | + Uncommon (Continuum markets) | IED I; coupons start dropping (banked) |
| **4-5** | **Shops open; tables certified on arrival at F4**; coupons spendable | L2-3 | Uncommon / Rare | Boomer (F4) | Common-Uncommon | Rapid Detox (F4), Special Brew (F4), Jelly Bomb, Disco Ball, Dolores, potion balls, Explosives Handling 5; Royal Chariot (F5) |
| **6-9** | Shops + Enhanced Studio | L3-5 | Rare / Very Rare | Wrecker (F8) | + Rare (limited) | Agent Provocateur, Advanced Bomber's Studio, Liquid Therapy, Superb Constitution Buff (F6, Alchemy L5); Alchemy L5 halved time |
| **10-14** | Shops | L5-7 | Very Rare / Legendary | Wrecker | up to Rare | Autoclave (L6), examine-to-learn (L7) |
| **15-18** | Shops | L6-8+ | Very Rare-Legendary / Legendary | Doomsday-class (DM only) | up to Rare | Endgame designs |

### 9.3 Anti-abuse

- **Per-crafter caps per floor** (finished items): Uncommon **6**, Rare **3**, Very Rare **1**, Legendary **0** (DM-granted only). Common is limited by time. The L6 **autoclave** is the only volume exception and only for Common/Uncommon; it still costs **1 tagged reagent per 5 units** plus bench supplies per unit.
- **Pacing:** crafted **permanent** items (stat buffs, builds, enchantments) count against core §3.7 (~1 new permanent item per crawler per floor). Crafted consumables don't count against the R3 budget, but the DM trims consumable drops for a party that crafts heavily.
- **Monsters worth killing** (§4.3) stops rat farming. One harvest per corpse; no reagents from summoned or conjured creatures.
- **Market:** vendors pay ¼ for crafted goods, buy at most 5 per crawler per floor, and announce "market flooded" (with a toast).
- **No crafted revival** (core §6.4.2). The Brew and Lifesaver keep their core §6.5 caps. **Stat-buff cap:** 2 per ability (§6.2).
- **Time is real:** extra shifts cost floor time and risk Exhaustion (§2.7). The DM should let the world move while the party crafts.
- **Recalls:** if a crafted item breaks the game, Production issues a **product recall** (the item becomes a Dud, its bench supplies are refunded, R0 toast). Use sparingly; log it as a temporary ruling (core §0).
- **Invention:** the DM prices invented recipes off the §6.9 tiers and 2024 DMG items of the same rarity; one feature per 2 dice traded, no stacking riders.

### 9.4 DM procedure (at the table)

1. **Saferoom check:** is it an honest saferoom? (False saferooms have no Personal Space door.)
2. **Ask for the plan:** recipe, table, lead crafter, helpers, shifts this visit.
3. **Verify:** table **certified (Floor 4+)** and level, recipe known, ingredients by tag and rarity, bench supplies, floor caps (§9.3), the floor's rarity ceiling.
4. **Clock:** state what the shifts cost (floor clock, Lights-Out, Exhaustion risk).
5. **Resolve the check:** Steady Hands (default): state the total and the DC before anything is spent, post the `[GM] Steady Hands` line; if the crafter chose to roll (or the table has Steady Hands off), name the DC first and post a `[ROLL]` line with the formula.
6. **Resolve** per §6.4; roll on the §6.6 / §6.7 tables only for rolled crafts.
7. **Name it** in the System's voice; set stability for explosives; log it.
8. **Toast** if notable (§8). Snark-only is fine.
9. **Update session state** (§9.5).

### 9.5 Session-state keys

```text
TABLES:     <owner> | <table> L<n> | state: token|stashed|active | access: <crawlers> | heir: <crawler>
F1-TABLE:   rolls used n/2 | found y/n | chance 5%      (§2.5.1)
COUPONS:    <crawler>: <n>
RECIPES:    <crawler>: <list>
SKILLS:     <crawler>: IED <rank>, EXPL <rank>, AGENT-PROV y/n, ...
REAGENTS:   <crawler>: <tag rarity xN>, ...
WIP:        <table>: <recipe> <shifts done>/<needed>
CRAFT-CAP:  F<n> <crawler>: U <n>/6, R <n>/3, VR <n>/1
STATBUFF:   <crawler>: STR 0/2 DEX 0/2 CON 1/2 INT 0/2 WIS 0/2 CHA 0/2
BREW-USED:  <crawler>: n/2      (core §6.5)
EXPLOSIVES: <crawler>: <item> <stability> <on person | pack | inventory>
DUDS:       <crawler>: <item>
```

---

## 10. Locked decisions and open questions

### 10.1 Locked decisions (approved by Caleb, 2026-10-03 and 2026-10-04)

Apply these as written. Change them only through a new decision file. "Closes" gives the open question each one answered: "Q" numbers are the v0.1.1 numbers, "v0.2 item N" is the numbered list that §10.2 held in v0.2.

| Locked rule | Closes | Applied in | Decision file |
|---|---|---|---|
| **First table:** Floor 2 default drop (Alchemy and Sapper's tables as written). **Very rare Floor 1 find** by the AI GM's roll (default 5% per qualifying event, tunable, max 2 events). Replaces the goblin-workshop owner-option (flavor only). | Q6 | §2.5, §2.5.1, §8.4, §9.2 | decisions/010-first-crafting-table.md |
| **Tables unusable until Floor 4;** carried (Table Token in System Inventory) or stashed before then; certified at Floor 4. **Shops sell tables from Floor 4.** | Q5 (the DM's one-time shady-vendor bend stays optional) | §2.5.2, §2.5.3, §8.2b | decisions/010-first-crafting-table.md |
| **Strict saferoom-only crafting** (no field mixing). | Q1 | §1.3 | decisions/011-crafting-settings.md |
| **Potion cooldown: 1 round** (replaces 3 − Con modifier). Special Brew keeps its separate 10-hour lockout and max 2 per drinker (core §6.5). | Q2 | §6.1, §5.5.1 | decisions/011-crafting-settings.md |
| **Steady Hands no-roll mode: ON by default.** | Q12 | §2.7, §6.4 | decisions/011-crafting-settings.md |
| **All four house stations kept, marked HOUSE** (Cooking, Smithing, Enchanting, Scribe). | Q13 | §7 | decisions/011-crafting-settings.md |
| **Crafting boons are DM-granted only** (no trainer price list). | Q14 | §3 | decisions/011-crafting-settings.md |
| **Economy:** basic table list price 5,000 (repriced 2026-10-04); upgrade coupon cap 25,000. Crafting Studio 12,000 and Enhanced Crafting Studio 30,000 (F6+) (Caleb 2026-10-04); **from v0.3.4 those three prices are the F1-2 values and follow the §9.1a schedule from F3 (room vote Q-004, decision 030)**; other prices stand: level upgrades 5,000 × target level (L2 10,000 ... L6 30,000, above L6 DM only); coupons: one table purchase or one level upgrade up to 25,000, non-stackable, about 1 per crawler per two floors from Quest/Boss Boxes; bench supplies 10 (Common) to 25,000 (Legendary), lost on a failed craft. | Q4 | §2.4, §2.5, §2.7, §9.1 | decisions/012-crafting-economy-explosives.md |
| **Boomer bomb:** 6d6 below level 5, 8d6 at level 5+; 20-ft radius kept. | Q10 (Boomer only) | §6.9 | decisions/012-crafting-economy-explosives.md |
| **Table leveling (2026-10-04):** tables **upgrade on ANY floor** (from F4, certified) whenever credits or a coupon and the prerequisites are met; the odd-floor seniority rule is dropped; coupon, price and level-cap rules kept. Changes the house fix for canon conflict X-C04. | Q3; v0.2 item 1 | §2.4, §2.5.2, §9.2, §11, Appendix A | decisions/013-crafting-open-questions.md |
| **Special Brew (2026-10-04):** crawlers **never** brew it (NPC-only, core §6.5); the far-future L9 unlock mention is removed. | Q7; v0.2 item 2 | §2.3, §5.5.1, §11 | decisions/013-crafting-open-questions.md |
| **Superb Constitution (2026-10-04):** canon range **+1 to +4** (1d4), score cap 20, max two per ability; labeled **Very Rare, Alchemy L5, F6+**, 5,000 bench supplies, DC 18 (HOUSE gate). | Q8; v0.2 item 3 | §5.5.2, §9.2, §11 | decisions/013-crafting-open-questions.md |
| **Pets and standard potions (2026-10-04, "go with Lore for canon"):** standard healing potions and scrolls have **no effect** on pet-class creatures (canon K-161); the half-healing toggle is removed; Heal Critter is the way. | Q9; v0.2 item 4 | §5.5.3, §6.3, §11 | decisions/013-crafting-open-questions.md |
| **Bigger explosives (2026-10-04, "as long as it is appropriate for mobs"):** Wrecker 12d6, stacked Boomers, upgraded IED and the Jelly Bomb stay as drafted, with a **GM note to scale mob HP and count** when party blasts are in play. | rest of Q10; v0.2 item 5 | §6.9 | decisions/013-crafting-open-questions.md |
| **Dolores Doesn't Splat (2026-10-04):** threshold stays **100 ft**; a plain-words line added to the recipe. | Q11; v0.2 item 6 | §5.5.6 | decisions/013-crafting-open-questions.md |
| **Inventor royalties (2026-10-04):** keep the small credit trickle. | Q15; v0.2 item 7 | §8.4 | decisions/013-crafting-open-questions.md |
| **Merge into core (2026-10-04):** pointer plus the edits (Personal Space, 1-round potion cooldown, Table Tokens and saferoom stash) applied to core rules v0.2.7. | Q16; v0.2 item 8 | §11; core §1.2, §5.6, §5.9, §5.11, §6.5 | decisions/013-crafting-open-questions.md |
| **Boomer level test (2026-10-04):** party average level, rounded down, at detonation. | v0.2 item 9 | §6.9 | decisions/013-crafting-open-questions.md |
| **Floor 1 find (2026-10-04):** the Syndicate decides; a concrete **goblin-workshop cache** is placed in Floor 1 Zone 7 (floor doc v0.2.3). Tunables stay 5% per event, max 2 qualifying events, d6 table type. | v0.2 item 10 | §2.5.1; floors/f01/00-overview.md §5.7, §8.3 | decisions/013-crafting-open-questions.md |
| **Bench-free scope before Floor 4 (2026-10-04):** only the named bench-free recipes (Kit Bash, Jug O' Boom, Heal Critter), plus DM-approved Common ones. | v0.2 item 11 | §2.5.2 | decisions/013-crafting-open-questions.md |
| **"Roll it anyway" (2026-10-04):** kept as the opt-in under Steady Hands. | v0.2 item 12 | §2.7 | decisions/013-crafting-open-questions.md |

### 10.2 Open questions

All twelve v0.2 questions were answered by Caleb on 2026-10-04 and moved into §10.1. Three small new questions came up while applying them (also listed in decision 013-crafting). They don't block anything; the defaults below are in force.

1. **Superb Constitution gate** (new): the +1 to +4 range is canon and untouched, but it is labeled Very Rare, Alchemy L5, F6+ (§5.5.2) to match the 2024 Manual of Bodily Health. Fine, or move it down to Rare at an L3 table on F5 for closer canon timing? Default: Very Rare, F6+.
2. **Table token level** (new): with seniority gone, a table found on F2 stays L1 until upgraded after certification on F4 (two coupons reach L3 on F4). Fine, or give tokens one free level on certification? Default: no free level.
3. **Goblin cache reward** (new): Zone 7 guarantees a Jug O' Boom recipe card, 2 portions of goblin oil and a worn Tinker's Tools kit, plus the 5% table roll. Right size for a Floor 1 side room? Default: as written.

---

## 11. Conflicts with canon and with core rules

**With core rules (`rules/10-core-rules-5e.md` v0.2.7).** Caleb approved the merge on 2026-10-04 (decision 013-crafting); items 1, 3, 5, 8 and 9 below are now written into core v0.2.7 (§1.2, §5.6, §5.9, §5.11, §6.5), so they are no longer clashes. They are kept here as the record of what was merged.

1. **Potion cooldown** (§6.1) was new: 1 round [LOCKED, decision 011]. **Merged into core v0.2.7** (§5.11, with a cross-reference in §6.5). Core §6.5's 10-hour lockout and max-2 cap stay exactly as written and are not touched by the cooldown (§6.1).
2. **Special Brew source.** It is **crafter-NPC-only**, matching core §6.5 (1 per NPC per floor, carry 1, max 2 per drinker), and **crawlers never brew it** [LOCKED 2026-10-04, decision 013-crafting]. No core edit is needed.
3. **Personal Space** wasn't defined in core rules. **Merged into core v0.2.7** (§5.11, with a pointer in §5.6); the details stay in §2.1.
4. **Pets and standard potions** (§6.3) now **follow canon** [C:V K-161; LOCKED 2026-10-04]: standard healing potions and scrolls have no effect on pet-class creatures, so there is no longer a house toggle here. **Thrown potions not affecting crawlers** (§5.4) is still a house reading of K-162 that changes 5e as written.
5. **System Inventory** (core §5.9): this doc adds "time-locked: no explosive decay or Jolts" (§6.8). It fit §5.9's spirit but wasn't in its text; **now stated in core v0.2.7 §5.9**.
6. **Rarity ceilings** (core §3.6): MOAB is kept **Uncommon** so it can appear on F2 (peak Uncommon). Jelly Bomb, Disco Ball, potion balls and the Brew sit at F4+, within F3-5's peak Rare; the Very Rare Brew at F4 is already allowed by core §6.5.
7. **Lifesaver Draught** stays NPC-only per core §6.5 (no crawler recipe).
8. **Table Tokens vs the corpse cache** (§2.5.2): core §5.9 drops a dead crawler's System Inventory as a lootable corpse cache. A Table Token is bound and not lootable; §2.6 (repossess or heir) applies instead. **Carve-out merged into core v0.2.7 §5.9.**
9. **Saferoom stash** (§2.5.2): core rules had no stash, so this doc defines a simple one (a free terminal stash for bound tokens). **Merged into core v0.2.7 §5.9.**
10. **Poisoned on a lockout violation** was dropped from v0.1.1's §6.1: core §6.5 says a potion drunk in the Brew lockout is wasted, with no extra penalty, so only the 1-round cooldown carries Poisoned.

**With canon (each also flagged inline):**

- **X-C01** saferoom table sales: canon sources disagree; Floor 4 used here (LOCKED, decision 010), DM may bend once (the table is still unusable until Floor 4).
- **X-C04** table leveling: "auto every floor" vs coupons needed. **House fix changed 2026-10-04 (decision 013-crafting):** tables don't level on their own; they are upgraded on any floor (from F4) by paying credits or a coupon, within the level cap (§2.4). The v0.2 odd-floor seniority rule is dropped.
- **X-C03** Advanced Bomber's Studio vs advanced Bomb Maker's Workshop: treated as two things (room vs boon access).
- **X-C02** Armorer's Table vs Workshop: treated as one station.
- **X-C07** Rapid Detox chapter cite: doesn't affect mechanics; F3 used.
- **X-C09** how many Brews were made: doesn't matter here; the per-drinker cap of 2 is canon.
- **X-C10** Cooking/Smithing/Enchanting/Scribe: no canon definition; §7 is all house rule.
- **K-163 / K-057 / K-058** field brewing: canon allows simple recipes without a table or a saferoom; this table requires a saferoom (per the brief; LOCKED strict, decision 011).
- **K-060 / K-061** canon skill levels run much higher (Explosives Handling 11, IED 7); scaled to 3-5 ranks for 5e.
- **K-118** Superb Constitution: canon +1 to +4 (random, max two per stat) is **kept exactly** (1d4, score cap 20); only the gate is house: Very Rare, Alchemy L5, F6+ (§5.5.2). **K-161** pets and potions: canon followed (no effect). **K-128** Dolores: canon works above ~200 km/h; the house threshold is 100 ft (kept by Caleb, 2026-10-04; the §5.5.6 recipe now explains it in plain words).
- **K-100 / K-126** canon prices: not used (5e economy).
- **Canon blast sizes** (e.g. a 45 km device, K-136; 150 m, K-146) deliberately aren't reproduced; 5e tiers instead.

---

## 12. Changelog

| Version | Date | Notes |
|---|---|---|
| 0.1 | 2026-10-03 | First draft (Syndicate), per decision 004 and Caleb's brief: principles, tables and levels, coupons, acquisition gate, shifts, boons, ingredients, recipe format, 11 example recipes, potion limits, failure tables, explosives, house stations, voice, balance, quick reference. Canon from CANON-LEDGER §10 (K-001..K-187, X-C01..X-C12). Recorded in decisions/008-crafting-rules.md. |
| 0.1.1 | 2026-10-03 | (1) **Special Brew is crafter-NPC-only**, matching core §6.5: removed the crawler-brew allowance (§2.3, §5.5.1, §9.1, §11 conflict 2, open Q7); added a note that a crawler brewing it is a possible far-future HOUSE unlock (canon hint: a level-9 Alchemy Table might remove the two-dose cap, K-028). (2) Added the **Floor 1 goblin workshop** first-table owner-option (Engineer's Table L1 + supplies; K-010, K-103; B1 ch17-19; §2.5, new §2.5.1, §9.2, open Q6); **Floor 2 stays the default** first drop; "no table before Floor 2" relabeled HOUSE, not canon. (3) New §10.1 "GM recommendations pending owner decision" (strict saferoom crafting, 1-round cooldown, Steady Hands ON for chat, keep four house stations, DM-granted boons) and flagged economy numbers and explosive tiers as Caleb's decisions. Nothing else changed. |
| 0.2 | 2026-10-03 | Caleb's approvals applied as LOCKED rules (decisions 010, 011, 012); owner line set to Syndicate Dungeon Crawl System 001; status "review". (1) **First table (010):** Floor 2 default kept; the goblin-workshop owner-option (old §2.5.1, Q6) is replaced by a very rare **Floor 1 random find** (default 5% per qualifying event, max 2 events, tunable); tables are **unusable until Floor 4**, carried as Table Tokens in System Inventory or stashed, and certified on Floor 4 (new §2.5.2, §2.5.3, §8.2b); dependents updated (§1.3, §2.1, §2.4, §2.6, §5.2, Rapid Detox and MOAB earliest floor, §8.2, §8.4 seeds, §9.2, §9.5, quick reference). (2) **Settings (011):** strict saferoom-only (Q1); potion cooldown simplified to **1 round**, with the Special Brew's own 10-hour lockout and max 2 kept separate (§6.1, Q2); **Steady Hands no-roll ON by default**, defined in §2.7 (Q12) with an opt-in "roll it anyway"; four house stations kept as HOUSE (Q13); boons DM-granted only (Q14). (3) **Economy and explosives (012):** table list price 25,000 and coupon cap 25,000 confirmed (Q4), coupon sources aligned to Quest/Boss Boxes, coupon coverage spelled out; **Boomer 6d6 below level 5, 8d6 at level 5+**, radius kept (Q10); other tiers flagged, not changed. (4) §10 restructured: §10.1 Locked decisions (replaces "GM recommendations pending owner decision"), §10.2 remaining open questions plus 4 new ones; §11 conflicts updated. Recorded in decisions/008-crafting-rules.md (update line), 010, 011 and 012. |

| 0.3 | 2026-10-04 | Caleb's answers to all twelve open questions applied (decision 013-crafting, `decisions/013-crafting-open-questions.md`). (1) **Table leveling (§2.4):** the odd-floor seniority rule is dropped; tables are upgraded on ANY floor (from F4, certified) by paying credits or a coupon, one level at a time within the level cap; benchmark now two coupons for L3 on F4; dependents re-checked (§2.5.2, §9.2 floor 3 row, §11 X-C04, Appendix A). (2) **Special Brew:** crawlers never brew it; the far-future L9 unlock paragraph removed (§2.3, §5.5.1, §11). (3) **Superb Constitution (§5.5.2):** canon +1 to +4 (1d4), cap 20; relabeled Very Rare, Alchemy L5, F6+, DC 18, 5,000 bench supplies (§9.2). (4) **Pets and potions:** half-healing toggle removed, canon followed (no effect; Heal Critter) (§5.5.3, §6.3, §11). (5) **Bigger explosives approved** with a GM note to scale mob HP and count (§6.9). (6) **Dolores:** 100 ft kept, plain-words line added (§5.5.6). (7) Royalties kept (§8.4). (8) **Merge into core v0.2.7** applied (§11). (9) Boomer level test locked: party average, rounded down, at detonation (§6.9). (10) Floor 1 goblin-workshop cache placed in Zone 7 of `floors/f01/00-overview.md` (§2.5.1). (11) Bench-free scope locked: named recipes plus DM-approved Common (§2.5.2). (12) "Roll it anyway" kept (§2.7). §10.1 gains the decided rows with dates; §10.2 now holds three new small questions. Depends-on line points to core v0.2.7. |
| 0.3.2 | 2026-10-04 | Syndicate: Caleb approved the basic table base price at 5,000 (was 25,000) after the Accountant showed 25,000 was out of reach; multiplier kept. Studio / Enhanced / level upgrades unchanged at that time (see 0.3.3). |
| 0.3.1 | 2026-10-04 | Syndicate (Story Box and pricing pass; crafting content untouched): listed prices are Floor-1 scale and multiply by the purchase floor's credit multiplier (§0), with a flag that the LOCKED 25,000 table price becomes absurd at F10+; `Depends on` pointer refreshed to core v0.2.8. No number changed. |
| 0.3.4 | 2026-10-04 | Room vote Q-004 (decision 030): workstation prices (basic table, Crafting Studio, Enhanced Crafting Studio) leave the credit multiplier for Floors 3-18 and follow a smoothed schedule (new §9.1a; numbers from `rules/70-encounter-budget-5e.json` v0.1.6 `q6_crafting_price_proposal`, aimed at about 3 / 6 / 10 floors of liquid income). **Floors 1 and 2 unchanged** (5,000 / 12,000 / 30,000, GM condition). Updated §0, §2.5.3 shop row, §9.1 price rows, §10 economy row and Appendix A. **Unchanged:** the 'tables upgrade on ANY floor' ruling (§2.4), level-upgrade pricing (still multiplier-scaled), coupon cap 25,000, bench supplies, ingredients, shop and revive prices. Added a coupon-vs-schedule note. |
| 0.3.3 | 2026-10-04 | Caleb's ruling: Crafting Studio **12,000** (was 20,000) and Enhanced Crafting Studio **30,000** (was 50,000) at Floor-1 scale, still multiplied by the purchase floor's credit multiplier (§0: x1 F1-4, x5 F5-9, x20 F10-14, x50 F15-18, as the file already states). Basic table stays 5,000; level upgrades (5,000 x target level), coupon cap (25,000) and revive fees unchanged. Updated §2.5.3 shop row, §2.6 coupon coverage (also corrects the stale basic-table figure there: 5,000, not 25,000), §9.1 price table, §10 economy row and Appendix A. Removed the "open: rescale?" note. Added a coupon-vs-multiplier note in §2.6 (Enhanced Studio is 150,000 on F5-9; Accountant watching). Decision: `decisions/019-credit-multiplier-fees.md` v1.2. |

---

## Appendix A: One-page quick reference

```text
CRAFTING QUICK REFERENCE (rules/20-crafting-5e.md v0.3)
WHERE      Saferoom only (honest ones), strict. Tables live in your Personal Space (door in any saferoom).
TABLES     First table: Floor 2 (5% rare find on Floor 1). UNUSABLE until Floor 4: carry (Table Token in System
           Inventory, weightless) or stash at a saferoom terminal. Certified on arrival at Floor 4. Bench-free recipes work from F1.
           Explosives are INERT in saferooms. Stable only while ON a Sapper's Table.
CHECK      Steady Hands ON (no roll): 10 + tool mod + PB + table bonus (+5 Adv, -5 Dis) >= DC = success, else fail by margin.
           Roll it anyway if the crafter opts in: d20 + tool ability + PB (if proficient) + table bonus (+1 per level above min, max +3).
           Tool + synergy skill proficiency = Advantage. Not proficient = Common only, no PB.
DC         Common 10 | Uncommon 13 | Rare 15 | Very Rare 18 | Legendary 21 | Infusion +2 | Group build +2
TABLE LVL  L1 Common | L2 Uncommon | L3 Rare | L5 Very Rare | L7+ Legendary (DM)
           Alchemy:  L3 potion balls + Special Brew | L4 specialize | L5 half time | L6 autoclave x100 | L7 examine-to-learn
           Sapper:   L1 no decay/early boom on table, modules | L2 Stable output | L3 INFUSION | L4 timers/remote | L6 batch x10
           Engineer: L1 single-part | L2 MULTI-PART, Large | L3 weapon mounts | L4 Huge
           Armorer:  L1 make wearable, no enchanting | L3 enchant (Uncommon) | L4 Rare, mithral/adamantine
LEVELING   Tables never level on their own. Upgrade on ANY floor from F4 (certified, 1 level at a time, within the cap) with credits or a coupon.
           Coupon = 1 table or 1 level, <= 25,000, no combining (Quest/Boss Boxes, ~1 per 2 floors).
           Level cap = ceil(floor / 2) + 2. Shops sell tables from F4 (5,000; Studio 12,000; Enhanced 30,000 F6+ on F1-2 scale; F3-18 prices per §9.1a). Upgrade = 5,000 x target level.
TIME       Shift = 2 h. A saferoom Long Rest includes 1 shift. Extra shifts cost floor time; after 2 extra: DC 10 Con or Exhaustion.
           Quick 10 min | Common 1 | Uncommon 2 | Rare 4 | Very Rare 8 | Legendary 16+ shifts
GOLD       Bench supplies: 10 | 50 | 500 | 5,000 | 25,000 (lost on failure)
RESULT     Success | beat DC by 10+: Nat-20 table (1-3 only) | Fail by 1-4: keep best ingredient | Fail by 5+: all lost
           Nat 1: ruined + d12 mishap | Nat 20: success + d6 bonus | Any failed infusion = DUD
POTIONS    Cooldown = 1 round (one potion per round). Drink during it: it works, but Poisoned 1 min (DC 12 Con ends).
           Special Brew (NPC-brewed only; crawlers never brew it) has its OWN 10 h lockout (core 6.5): other potions wasted. Max 2 buff potions per ability, ever.
           Superb Con = 1d4 (+1..+4), score cap 20, Very Rare, Alchemy L5, F6+. Standard healing potions do nothing for pets (use Heal Critter).
           Scrolls and meals skip cooldown. Thrown potions don't affect crawlers.
EXPLOSIVES Utilize to throw 20/60 (balls 30/90). Dex save for half. Objects take double.
           Popper 2d6 5ft DC12 F1 50cr | Banger 4d6 10ft DC13 F2 200 | Boomer 6d6 (8d6 at level 5+) 20ft DC15 F4 2,000
           Wrecker 12d6 30ft DC17 F8 20,000 | Doomsday-class 16d6+ 40ft DC19 F13 DM only
STABILITY  Stable (1, Heavy Impact only) | Steady (1-2) | Volatile (1-4) | Unstable (1-6, all infused)
           Jolts (on person only): crit taken, fire/lightning damage, fall 10+ ft, knocked Prone, failed area save.
           Decay: -1 step per 8 h on person (16 h in a backpack). System Inventory: no decay, no jolts.
BOONS      IED I-III: +rank x (dice / 2) damage; +1 stability step per rank on early-boom rolls.
           Explosives Handling 1-5: rank 5 = Demolitions Workshop. Agent Provocateur (F6+): +1 Sapper level.
INGREDIENT Common 10cr CR0-2 | Uncommon 50 CR3-5 | Rare 500 CR6-10 | Very Rare 5,000 CR11-16 | Legendary CR17+
           Only real threats drop reagents: CR >= half party level, or elite/boss. Fire/explosion kill: d6 1-3 = reagents gone.
CAPS/FLOOR Uncommon 6 | Rare 3 | Very Rare 1 | Legendary 0 (DM). Vendors buy crafted at 1/4, max 5 per floor.
NEVER      Crafted revival. A third stat buff. A third Brew. Crafting in the field. Using a table before Floor 4.
```

---

## Appendix B: Canon source map (ledger §10 IDs; tags as in the ledger)

| Topic | IDs (tag) |
|---|---|
| Tables are Personal Space accessories; shops from F4; looted/box tables | K-001, K-002 (V); conflict X-C01 (U) |
| Table auto-leveling (canon; not used here, tables are bought up on any floor) | K-003 (V), K-004 (W); conflict X-C04 (U) |
| Crafting Studio holds 5 tables; Enhanced Studio | K-005, K-006 (V); K-007, K-008 (W) |
| Engineer's Table: role, F1 loot, ~25,000, L2 multi-part; goblin workshop supplies | K-009..K-012, K-103 (V) |
| First workbench achievement + Crafter's Box | K-013, K-014 (V) |
| Sapper's Table: F2 box, function, L1 stability, L3 infusion, AP +1, leaving the table, triggers, Demolitions menu | K-015..K-019, K-021..K-024 (V); K-020 (U) |
| Alchemy Table: source, function, L3/L5/L6 thresholds, L9 hope, specialization, coupons, examine | K-025..K-035 (V) |
| Armorer's Workshop | K-036..K-038 (V); X-C02 (U) |
| Other tables | K-039..K-047 (V) |
| Access sharing; tables on death; upgrades tied to buyer | K-048, K-052, K-185 (V) |
| Upgrade coupons (cap, no combining) | K-049 (V); K-050 (U) |
| Skills: Alchemy, IED, Explosives Handling, Bomb Surgeon, Backfire, Trap Engineer, Infusion | K-057, K-060, K-061, K-063..K-069 (V); K-058 (W) |
| Agent Provocateur, Compensated Anarchist | K-071..K-075 (V); X-C03 (U) |
| Ingredients: Crafting Items menu, alchemy materials, markets, moonshine, goblin oil, torch, explosives, sage beetle ichor, toraline | K-090..K-112 (V; K-096 U) |
| Special Brew (crafter-NPC-only here) | K-113, K-115..K-117, K-028 (V); K-114 (W); X-C05 (resolved), X-C09 (U); main ledger I-018 |
| Superb Constitution Buff; stat-buff cap | K-118, K-159, K-160 (V) |
| Fragmenting Potion Ball | K-119 (V); X-C06 (wiki error flagged) |
| Heal Critter; pets and potions | K-121, K-109, K-161 (V) |
| Rapid Detox | K-127 (V); X-C07 (U) |
| Dolores Doesn't Splat; Syndicate rule rewrite | K-128, K-181 (V) |
| Liquid Therapy | K-130, K-033 (V) |
| Jug O' Boom; price; raw beats product | K-125, K-126, K-173 (V) |
| Jelly Bomb | K-134, K-135, K-056 (V) |
| Doomsday Scenario (removal detonation) | K-136 (V) |
| MOAB | K-137 (V) |
| Hobgoblin Disco Ball; healing smoke vs undead | K-138, K-139 (V) |
| Royal Chariot | K-141 (V) |
| Potion cooldown, length by Con, exemptions, storage | K-155..K-158 (V) |
| Thrown potions | K-162 (V) |
| Field vs table brewing; recipes persist | K-163..K-165 (V) |
| System names items; workbench can hurt; tool imprecision; size limits | K-166..K-169 (V) |
| Explosives inert in saferooms; backpack decay; infusion instability and Dud | K-170..K-172 (V) |
| Incendiary loot loss | K-174 (V) |
| Dungeonpreneur, royalties | K-176..K-178 (V) |
| No Cooking/Smithing/Enchanting/Scribe definitions | X-C10 (U) |
