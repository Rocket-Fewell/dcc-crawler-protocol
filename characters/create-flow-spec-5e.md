# Create Flow Spec (Discord /create, 5e Overlay)
Owner: Syndicate | Status: draft | Version: 0.1.12 | Updated: 2026-10-04
Summary: Screen-by-screen build spec for Borent's silent, private, text-only Discord `/create` flow (one player at a time, no GM wake): 16 active screens (S1-S17; S12 retired, numbers kept stable), prompts, limits, validation, what is written where, the data model, edge cases, a shared term glossary, a beta checklist with a 10-step test script, open questions, and (v0.1.4) the rules for several Crawlers per player, the one active Crawler, the session lock on swaps, the decided sheet layout (one text channel per Crawler), `/delete`, the tool requirements marked NEEDS BUILD, an acceptance checklist and an audit checklist. The Fan Profile is hidden: the System builds it from the S13 survey (private notes) and from play.
Depends on: characters/character-creation-5e.md v0.2.3 (the intake guide; wins on any chargen conflict), rules/10-core-rules-5e.md v0.2.12 (core), decisions/024-roll-method-ability-scores.md (Roll method, S8), rules/60-pets-companions-5e.md v0.1.0 and decisions/022-pets-and-companions.md (new §9, pets), decisions/020-multiple-crawlers-active-swap.md, rules/30-species-supplement-5e.md v0.1.4 and decisions/009-species-approach.md (Floor 1 species = SRD nine; Offer on Floor 3), decisions/013-party-size.md, gm-notes/30-player-channel-card-format.md, tools/README.md and tools/state.py (`create-crawler`), tools/campaign_session.py. Consumers: Borent Corp Systems Architect (codes it), Valtay Corp (core book author; player-facing guide uses the same screen names, steps and terms), AI GM (reads the result, never runs the flow).

> **Status:** DRAFT v0.1.4. Nothing here is LOCKED. **v0.1.4 adds §8 (several Crawlers per player, one active Crawler, swaps only outside an open session, sheet channels, `/delete`), an acceptance checklist and an audit checklist at the end; the session lock is Caleb's (2026-10-04), the rest of §8 is a Syndicate default, Caleb may override.** **v0.1.2 (Caleb, 2026-10-04): the "pick public Fan Profile tags" screen is dropped; S12 is retired and the flow runs S11 to S13.** **Project:** *Crawler Protocol: Season Zero*, private fan RPG inspired by *Dungeon Crawler Carl*.
> **Why this exists:** alpha intake ran through the GM by voice and typing. Beta has four new players; `/create` moves intake to a private text flow so the GM's wake budget goes to play.
> **Tags:** `VERIFY` = I am not sure of the exact 2024 / SRD 5.2 number or list; check the book before coding. `NEEDS state.py support` = not in tools/state.py today (see §3.3). Section refs: **GUIDE §n** = characters/character-creation-5e.md, **CORE §n** = rules/10-core-rules-5e.md. Limits marked *(design)* are Borent engineering proposals, not game rules.

---

## 1. Overview

**Who runs it.** One player, in Discord, privately. Slash command `/create` (uses the active session, see below). Every screen is an ephemeral (only-you) message with buttons, select menus and text boxes. **Text only: no voice, no TTS, no #gm-voice post, nothing in #table-transcript.** It does **not** call the GM (no LLM, no wake, no spotlight/focus change). All System lines come from a fixed line table (`tables/create-flow-lines.json`, NEEDS writing: Valtay or Syndicate, see §3.4), so the flow is free and repeatable.

**Session.** Every tool takes `--session <id>` **before** the subcommand (`python3 tools/state.py --session beta create-crawler --file spec.json`); else `$DCC_SESSION`; else the bridge's active session; else `alpha` (tools/campaign_session.py). **alpha** is the default and is the live game. **beta** is a *new session with new player characters*: its own state, ledger, channel map and characters folder.

| What | alpha | other session `<id>` (e.g. beta) |
|---|---|---|
| State + ledger + channel map + drafts | `sessions/` | `sessions-data/<id>/` |
| Crawler sheet file | `characters/<player>-<crawler>.md` | `sessions-data/<id>/characters/<player>-<crawler>.md` |
| Sealed GM quirk roll | `gm-notes/secret/` | `gm-notes/secret/sessions/<id>/` |

**What it writes** (only after S17 Confirm; nothing earlier touches live state):
1. The **crawler sheet file** (name per NAMING-CONVENTIONS: `<player>-<crawler-name>.md`, lowercase-hyphenated).
2. The **session state** through `state.py --session <id> create-crawler --file <spec>` (atomic; credits go in as separate ledger rows with reasons).
3. The Crawler's **sheet channel** registration (`#<player>-<crawler>`, layout in §8.3) and the **first full card** (publisher, format in gm-notes/30).
Before S17, answers live only in a private draft file (§3.4).

**What it never touches.** Other players' drafts, sheets or channels; anything in `gm-notes/secret/` (the sealed quirk roll, Affinity); `sessions/focus.json`, `spotlight.json`, `voice-control.json`; table settings (Death Mode, Comfort level, Floor 1 Reprieve: shown read-only on S1, changed only by Caleb per GUIDE §2); the GM's channels. It never shows a player another player's draft or opt-outs.

**Screens.** S1-S17, but **S12 is RETIRED, intentionally skipped** (Caleb, 2026-10-04): 16 active screens. Numbers are not reused or renumbered, so the built flow, the line table and the book keep pointing at the same names. After S11 (or S10 for non-casters, since S11 is skipped for them) the player goes straight to S13.

**One-line rules of the flow.** Level 1 only (CORE §10.1; Floor 1). No custom stats, no homebrew species or classes, no magic items at creation (GUIDE §6.5). 2024 PHB content if the table owns it, otherwise SRD 5.2 only (CORE §7.1); the data table (§3.4) carries which. **Species = the SRD nine**; the Floor 3 Offer (species supplement §2, decision 009) is not part of this flow.

**Controls on every screen.** `[Back]` goes to the previous screen and keeps all answers. `[Skip]` only where a screen says so. `[Restart]` (§4.1) wipes the draft after a confirm button, **except** S2 (comfort stays). `[Help]` shows a 3-line plain explanation (no new rules). `[Pick for me]` appears on mechanical screens (S5-S11): the System chooses a legal default, says so openly, and the player may change it (GUIDE §8.1 "System Picks For You").

---

## 2. Screens

Prompt text is the System's voice: dry, snarky, clear. The rule text under it is plain. Snark aims at the job, the choices and the gear, never the person (GUIDE §2.3 hard floors, CORE §4.8). Lines below are samples; final wording lives in the line table.

### S1. Welcome and table settings
- **Prompt:** "Welcome, Crawler. This is your private intake booth. Nobody else can see this. The Terms of Service are four hundred thousand words long and the only one you need is 'lethal.' Tap ACCEPT. DECLINE also continues, but louder."
- **Shows (read-only):** session id, Death Mode (Costly Revives), Comfort (Ludicrous), Floor 1 Reprieve on/off, "Party: N of 4 active Crawlers" (no names of drafts) and, for a returning player, "You have M Crawlers on file; your active one is <name>".
- **Choices:** `[ACCEPT]` `[DECLINE]` (both continue) `[Use a pre-built]` (§4.6) `[Read the Terms]` (grants the snark toast **Don't Skip Intro**, GUIDE §3.1, at Confirm; the Terms are not shown).
- **Validation:** a player may already have Crawlers in this session (§8: any number; the new one is benched unless it is the player's first). The "party full" check counts **active** Crawlers only and applies when the new Crawler would be active, i.e. the player's first (§4.4, §8). Else refuse with a plain message.
- **Writes:** draft `session`, `discord_user_id`, `started_at`, `flow_version`. Back: none. Skip: none.

### S2. Comfort: lines and veils (private)
- **Prompt:** "Table comfort is Ludicrous. That's the default, not a promise. Tell us privately what you don't want. No explanation needed. We won't ask, we won't joke about it, and nobody else sees this."
- **Plain meaning:** a **line** = never appears, anywhere. A **veil** = may exist off-screen but is never shown or described (the System fades to black). The word **cut** still works any time during play (GUIDE §2.4); it needs no setup.
- **Choices:** up to 6 *(design)* free-text topics, each marked **Line** or **Veil**, max 60 characters each. Optional per topic: `[Share with the GM]` (default off). `[Skip]` = none.
- **Validation:** text only; no explanation field exists. Stored exactly as typed. The hard floors in GUIDE §2.3 apply regardless and are not listed as options.
- **Writes:** draft `optouts[]` -> state `fan_profile.opt_outs[]` (§3.1). The runtime GM filter reads every entry to obey it (opt-outs are honored from any state, GUIDE §2.4); **only entries marked shared** appear in any review view (§4.7). Not on the sheet file, not on the card, never posted.
- **Nav:** Back: S1. Skip: allowed. Restart: S2 is kept. The player can reopen S2 any time by `/create comfort` (no sheet change, no GM wake).

### S3. Crawler name and pronouns
- **Prompt:** "Name for the paperwork. Not your Broadcast Name; that's earned on Floor 3. Pronouns, if you like. The cameras will guess otherwise."
- **Choices:** crawler name (text); pronouns (pick he/him, she/her, they/them, or type up to 20 chars; `[Skip]` = "unspecified").
- **Validation (name):** 2-30 chars *(design)*; letters, digits, space, apostrophe, hyphen, period; no `@ # / \` or markdown or line breaks; not a reserved word (`gm`, `ai`, `system`, `party`, `all`, `everyone`). Unique case-insensitive in this session (state.py refuses duplicates; a player's second Crawler is fine with a different name, §8.2 item 1). Warn (not block) if it contains or sits inside another crawler's name, because tools match partial names (§4.3). Slug for the file name = lowercase, hyphens.
- **Writes:** `name`, `build.pronouns`. Back: S2. Skip: pronouns only.

### S4. Look and hook
- **Prompt:** "One line: what you look like right now, in whatever you were wearing when the world ended. One line: why you are still funny or dangerous. We have cameras. We have so many cameras."
- **Choices:** look (max 160 chars), hook (max 160 chars). Both required (CORE §10.1 step 3).
- **Validation:** non-empty, no links. The look is the *Floors 1-2* look; everyone reads as baseline human (CORE §7.2), so species features stay out of the look (the tool warns on "horns / tail / scales / wings"; player may keep them as a costume).
- **Writes:** `build.look`, `build.hook`. Back: S3. Skip: none.

### S5. Species (Latent Biology)
- **Prompt:** "Latent Biology. Pick one. You'll look human on Floors 1-2 and the traits will get filed as quirks. Your file is under review."
- **Choices (exactly the SRD nine, decision 009):** each button shows plain effects. Traits are named as in GUIDE §7.2; size, speed and exact numbers come from the data table (SRD 5.2 checked: sizes Medium or Small, Speed 30 ft except Goliath 35 ft).

| Species | Plain stat effects (names from GUIDE §7.2) |
|---|---|
| Dragonborn | Breath Weapon (a ranged area attack you can use a few times per Long Rest); Damage Resistance to one damage type (your ancestry); Darkvision 60 ft (SRD 5.2 checked) |
| Dwarf | Darkvision (120 ft); Dwarven Resilience (resist poison, better saves against it); Dwarven Toughness (+1 HP, and +1 more at each level); Stonecunning (Bonus Action: Tremorsense 60 ft for 10 minutes while on stone; Proficiency Bonus uses per Long Rest) |
| Elf | Darkvision; Fey Ancestry (harder to charm); Keen Senses (one free skill: Insight, Perception or Survival); Trance (rest without sleeping); lineage pick |
| Gnome | Darkvision; Gnomish Cunning (Advantage on Int, Wis and Cha saves); lineage pick |
| Goliath | Giant Ancestry (one special power from a list); Large Form at level 5 (not on Floor 1) |
| Halfling | Luck (reroll natural 1s); Brave; Naturally Stealthy |
| Human | Resourceful (Heroic Inspiration); Skillful (one extra skill); Versatile (one extra Origin feat) |
| Orc | Adrenaline Rush; Relentless Endurance (drop to 1 HP instead of 0, once per Long Rest); Darkvision |
| Tiefling | Fiendish Legacy (pick a legacy: resistance + spells); Otherworldly Presence; Darkvision |

- **Sub-choices (asked right after, only if the species has them):** Dragonborn ancestry; Elf, Gnome and Tiefling lineage/legacy; Goliath ancestry; Human Skillful skill (asked on S9) and Versatile feat (asked on S7 with the Origin feat). Exact option lists from the data table. SRD 5.2 checked: Dragonborn 10 dragon types, Elf 3 lineages (Drow, High Elf, Wood Elf), Gnome 2 (Forest, Rock), Goliath 6 giant ancestries, Tiefling 3 legacies (Abyssal, Chthonic, Infernal).
- **Footer on the screen:** "Floor 3: the System will offer you a rebuild. Optional. It's in the Terms." (no oddity names shown; species supplement §2).
- **Writes:** `species` (e.g. `Human`), `build.species_choice` (sub-choice), `build.quirk` (the System's quirk line for that species, from the line table). Back: S4. Skip: none. Changing species later in the flow only re-asks the sub-choice.

### S6. Class (Provisional Class)
- **Prompt:** "Provisional Class. A talent that fell out of you. The official title comes later, with the paperwork. Level 1 only. No multiclassing; we don't have the forms."
- **Choices (SRD 5.2, all 12 classes; Hit Die SRD 5.2 checked):**

| Class | One-line plain description |
|---|---|
| Barbarian | Rage-powered frontline tank; hits hard, shrugs off damage (d12) |
| Bard | Talker and support caster; inspires allies, many skills (d8) |
| Cleric | Divine caster; heals, buffs, and holds the line in armor (d8) |
| Druid | Nature caster with a shapeshift later; strong control spells (d8) |
| Fighter | Weapons and armor expert; simple, tough, reliable (d10) |
| Monk | Unarmed martial artist; fast, mobile, hard to pin down (d8) |
| Paladin | Armored holy warrior; big melee hits plus healing and smites (d10) |
| Ranger | Hunter and scout; bows, tracking, light nature magic (d10) |
| Rogue | Sneaky precision striker; skills, Sneak Attack, expertise (d8) |
| Sorcerer | Born caster with few spells and high power; flexible magic (d6) |
| Warlock | Pact caster; few slots that recharge fast, plus invocations (d8) |
| Wizard | Spellbook caster with the widest spell list; fragile (d6) |

- **Class choices at level 1** (only the ones this class has; list per class from the data table; SRD 5.2 checked, level 1 only: Fighter gets a Fighting Style (Paladin and Ranger get theirs at level 2), Cleric a Divine Order (Protector or Thaumaturge), Druid a Primal Order (Magician or Warden), Warlock 1 Eldritch Invocation, Rogue Expertise in 2 skills (Bard gets Expertise at level 2), Weapon Mastery picks Barbarian 2, Fighter 3, Paladin 2, Ranger 2, Rogue 2): Fighting Style or Divine Order or Primal Order, Expertise, Eldritch Invocation, Weapon Mastery picks. Each is a short select menu.
- **Writes:** `class` (e.g. `Wizard`), `level` = 1, `build.hit_die`, `build.class_choices{}`. HP is computed at S8 (class Hit Die max + Con modifier, GUIDE §3.3). Back: S5. Skip: none. If the player used a pre-built (§4.6) the class is preset but changeable.

### S7. Background (Prior Employment) and Origin feat
- **Prompt:** "Prior Employment. What you did before the crawl. Pick the job; the System will quietly decide what that says about you."
- **Choices:** 2024 PHB backgrounds if the table owns the book (Acolyte, Artisan, Charlatan, Criminal, Entertainer, Farmer, Guard, Guide, Hermit, Merchant, Noble, Sage, Sailor, Scribe, Soldier, Wayfarer; `VERIFY` list: not in SRD 5.2 except Acolyte, Criminal, Sage, Soldier; the other 12 are from memory/PHB), else SRD 5.2's four (SRD 5.2 checked: Acolyte, Criminal, Sage, Soldier). Each button shows: its three listed ability scores, its Origin feat, its two skills, its tool (all from the data table).
- **ASI choice (2024):** the background lists three ability scores. The player picks **+2 / +1** (two of the three) **or +1 / +1 / +1** (all three). No score above 20 (GUIDE §3.4, §3.6). Shown as a live preview; applied on S8.
- **Origin feat:** fixed by the background; plus Human's Versatile feat if S5 = Human (pick from the Origin feat list; SRD 5.2 checked: the SRD has only Alert, Magic Initiate, Savage Attacker and Skilled, the full PHB list is longer and not in the SRD).
- **Reskin note** (flavor only): "reskin the *reason* you have those skills; never change the skills" (GUIDE §3.4). The System adds one line of snark about the job from the line table.
- **Writes:** `background`, `build.background_asi{}`, `build.origin_feat`, `build.extra_origin_feat` (Human only). Back: S6. Skip: none.

### S8. Ability scores (the mechanics step)
- **Methods (GUIDE §3.6, §10.4, decision 024):** **Standard array** (15, 14, 13, 12, 10, 8), **Point buy** (27 points) and **Roll**. Standard array and point buy are always offered and are unchanged. **Roll** is offered while the session setting `create.allow_roll` is **true (default ON; v0.1.10, Caleb)**; off = the button is hidden and S8 looks exactly as before. Under every method the S7 background increases (+2/+1 or +1/+1/+1) are added **after** the base scores are set. `[Pick for me]` is unchanged (standard array to suit the class, one swap).
- **Prompt:** "Six numbers decide how long you last. Pick a method. The audience has opinions about your Charisma already." Method screen, Roll on: buttons `[Standard array] [Point buy] [Roll]`; under Roll: "Roll: the System rolls three arrays of six scores (4d6, drop the lowest die, six times each). You keep ONE, and only an array that totals 73 or more. If none does, the System rolls all three again." Roll off: two buttons, no Roll text.
- **Screens inside S8:** (a) method buttons; (b) assign: array = one select menu per ability, each value used once; point buy shows the points left (27 start; cost table SRD 5.2 checked: 8=0, 9=1, 10=2, 11=3, 12=4, 13=5, 14=7, 15=9; scores 8-15 before bonuses); **Roll = see "Roll method" below**; (c) preview table: base + background bonus = final, modifier, and a computed block: **HP** (Hit Die max + Con modifier), **AC** (from kit, so shown as "10 + Dex for now" until S10), **Proficiency Bonus +2**, initiative, passive Perception. All computed by the tool, never typed.
- **Roll method (v0.1.10, decision 024).**
  1. **Roll:** on `[Roll]` the System rolls **three arrays (A, B, C) of six scores**; every score is **4d6, drop the lowest die** (one call per score: `python3 tools/roll.py "4d6dl1" --who "<Crawler name>" --label "S8 roll r<round> <A|B|C><1-6>"`, 18 calls per round). The totals are summed by the tool, never typed.
  2. **Screen "three arrays":** each array on its own row, scores high to low with the dice shown (dropped die struck through), the total, and a status: `Keepable (total 78)` or `Not keepable (total 70, needs 73 or more)`. Buttons `[Keep A] [Keep B] [Keep C]`; a button for an array totalling 72 or less is disabled and says why.
  3. **Rule:** only an array whose six scores total **above 72 (73+)** may be kept. (Standard array totals 72; point buy totals at most 75.) **No upper limit on the total** (Caleb). The player keeps exactly ONE; the other two are discarded but stay in `build.score_rolls`. No voluntary reroll.
  4. **None qualifies:** if none of the three totals above 72 (about 8.4% of rounds; each array qualifies 56.2% of the time), the System shows the failed round with the "none qualify" line, **rerolls all three arrays**, and repeats until at least one qualifies. Every round is logged and stored. *(design)* Safety stop after 10 rounds: error line, the player is sent back to the other two methods, the stop is logged.
  5. **Assignment chooser:** after `[Keep X]`, one select menu per ability (STR, DEX, CON, INT, WIS, CHA), each of the six kept scores used exactly once (equal scores are separate entries), so "the 15 goes to Dex" works. Then the preview (c).
  6. **Cap:** one 4d6-drop-lowest score is **3 to 18** before any bonus. The 2024 background increase (+2/+1 or +1/+1/+1) can **never take a score above 20**: 18+2 = 20 at most (+1 = 19), so rolled scores cannot hit the cap on their own, but validation still enforces "no score above 20" for every method.
  7. **Logging (GM-rules roll logging):** every die roll goes through `tools/roll.py`, so each gets a `[ROLL]` line in `sessions/rolls-YYYY-MM-DD.log` (alpha; other sessions use `sessions-data/<id>/rolls-YYYY-MM-DD.log`) (README format; see "Architect: roll-log entries" below). Rerolled rounds are logged too.
  8. **No free rerolls *(design, Syndicate default, Caleb may override)*:** the rounds are saved in the draft when rolled. Back, Edit, changing method and returning to Roll, and Restart all show the **same** saved rounds (as S2 comfort survives Restart, the saved rounds survive Restart for that player's draft); only the Confirm at S17 or deleting the draft ends them.
  9. **Switch off:** `create.allow_roll = false` hides `[Roll]` and its text. A press on an old Roll button is refused with the "closed" line. A draft that already kept an array and moved past S8 is unaffected; a draft still at S8 on Roll goes back to the method screen with the saved rounds held (shown again if the switch comes back on).
- **Validation:** array values used exactly once; point buy total exactly 27 or fewer left unspent *(design: allow leftover)*; roll: the kept array's total is above 72 (re-checked from the stored dice at S17), each score used once; final score at most 20 (CORE §1.1 via 5e as written); abilities stored as integers 1-30 (state.py rule).
- **Writes:** `abilities{str..cha}` (final), `build.score_method` (`array|pointbuy|roll`), `build.score_base{}` (the assigned base scores), `build.score_rolls` (roll only; shape under "Architect: state fields" below), `hp_max`, `build.initiative`, `build.passives{}`. Back: S7. Skip: none. Changing S5-S7 later re-runs this screen's preview automatically.

### S9. Skills and proficiencies
- **Prompt:** "Proficiencies. What your body already knows how to do. The fixed ones came with the job. Pick the rest."
- **Order matters:** fixed grants first (background's two skills and tool; species grants), then class picks. The picker hides skills already owned; if a pick would duplicate, the tool asks for a different one (`VERIFY`: not in SRD 5.2, which has no swap rule; the 2014 PHB did; treat as a table/tool rule).
- **Choices:** class skill picks (count and list per class from the data table; SRD 5.2 checked: Bard 3 from any skill, Ranger 3, Rogue 4, every other class 2); Human Skillful skill; Elf, if the species gives a skill pick (SRD 5.2 checked: Elf Keen Senses, one of Insight, Perception, Survival); Expertise picks (Rogue at level 1, two skills; SRD 5.2 checked); Weapon Mastery picks for classes that have them (Barbarian, Fighter, Paladin, Ranger, Rogue; count per class: Barbarian 2, Fighter 3, Paladin 2, Ranger 2, Rogue 2; SRD 5.2 checked).
- **Auto-filled and shown:** saving throws, armor and weapon proficiencies, tool, languages (Common plus two picks from the Standard Languages table; SRD 5.2 checked), Proficiency Bonus +2.
- **Validation:** exact counts; no duplicates; only legal lists.
- **Writes:** `build.skills[]`, `build.expertise[]`, `build.tools[]`, `build.saves[]`, `build.weapon_masteries[]`, `build.languages[]`. Back: S8. Skip: none (`[Pick for me]` fills the picks).

### S10. Starting equipment: package or gold
- **Prompt:** "Equipment. Take the package, or take the cash and shop at the Intake Vending Wall. Everything is junk. Everything works."
- **Two separate choices (GUIDE §6.1):** (1) **class**: package A **or** the class gold option; (2) **background**: package A **or** its gold option (50 GP, GUIDE §6.1). Each package screen lists items with their real 5e name. Gold from a package (leftover GP) counts.
- **Vending Wall:** if the player has credits to spend, a store list (5e prices, PHB equipment; **no magic items**, GUIDE §6.1, §6.5). Player may spend any amount up to what they hold, leftover stays as credits. `[Pick for me]` = the AI-buyout style used in alpha (a sensible kit, stated openly).
- **Item names (required; Caleb, 2026-10-04; replaces the old junk-name picker):** every item shows the System's own name with the 5e name in brackets, read from **`tables/item-reskins.json`** (Lore; schema item-reskins/0.1.0, 189 entries) by the item's stable `srd_id` (kebab-case, e.g. `quarterstaff`): show `combined_label`, e.g. *Duct-Taped Mop (Quarterstaff)*. The player does not pick or type a name here. Each chargen item in `tables/chargen-5e.json` (v0.1.2) carries an `srd_id`; the **sheet stores the `srd_id`**, and dice, damage, properties, mastery, AC, weight and **prices always key off the id, never the display name**. If an id has no table entry, fall back to the plain 5e name so a screen is never blank. **Variant headers** (`holy-symbol`, `gaming-set`, `musical-instrument`, `artisans-tools`, `arcane-focus`, `druidic-focus`): the player picks a specific variant on this screen, the sheet stores the variant's id, the price comes from that variant, and a header is never shown priced or stored. NEEDS BUILD (Architect): the lookup, the variant pick, and a test that every chargen id resolves and no header reaches a sheet. Players may still rename an item later through the GM (cosmetic).
- **Auto-added, no choice:** **Intake Bag** (cosmetic, zero value, GUIDE §6.3) as one inventory line. A personal item is *not* auto-added unless the player names one on S13 Q1 (cosmetic, mundane).
- **Credits math (CORE §5.10: 1 credit = 1 GP; GUIDE §6.1 no stipend):** `starting_credits` = GP from the chosen class option + background option. Each vending purchase is a negative ledger row. Credits left must be 0 or more.
- **Computed:** AC from worn armor and shield, plus Dex as the armor rules say, else 10 + Dex (Unarmored Defense, SRD 5.2 checked: Barbarian 10 + Dex + Con with no armor, a shield is allowed; Monk 10 + Dex + Wis with no armor and no shield).
- **Writes:** `inventory[]` (`name`, `qty`, `notes`, `mechanics`, `category` = weapons|armor|magic|gear), `ac`, `credits`, `credit_breakdown[]`, `build.kit{class_option, background_option}`. Back: S9 (kit choices kept unless class or background changed). Skip: none.

### S11. Spells (casters only; other classes skip automatically)
- **Prompt:** "Spells. Pick the ones you'll admit to. The audience prefers loud."
- **Counts at level 1 (SRD 5.2 class tables checked):**

| Class | Cantrips | Level 1 spells | Notes |
|---|---:|---:|---|
| Bard | 2 | 4 | prepared |
| Cleric | 3 | 4 | prepared |
| Druid | 2 | 4 | prepared |
| Sorcerer | 4 | 2 | prepared |
| Warlock | 2 | 2 | Pact Magic; 1 slot at level 1 |
| Wizard | 3 | 6 in spellbook, 4 prepared | spellbook is reskinned (a cracked phone app) |
| Paladin | 0 | 2 | prepared (2024), SRD 5.2 checked |
| Ranger | 0 | 2 | prepared (2024), SRD 5.2 checked |
| Barbarian, Fighter, Monk, Rogue | none | none | screen is skipped |

- **Choices:** paged lists (Discord menus max 25 options) from the class spell list; each entry shows level, school, one-line plain effect from the data table (no book text copied). Revival spells on Cleric lists: show the plain note from CORE §6.4 if the table is on Canon Hard; not in the campaign default (Costly Revives, GUIDE §2.1).
- **Validation:** exact counts; only the class list; level 1 slots shown (from the class table; SRD 5.2 checked: 2 slots for Bard, Cleric, Druid, Paladin, Ranger, Sorcerer, Wizard; 1 for Warlock).
- **Writes:** `build.spells{cantrips[], prepared[], spellbook[]}`, `build.spell_slots{"1":N}`, `build.spellcasting_ability`. Back: S10. Next: S13 (S12 is retired). Skip: automatic for non-casters.

### S12. RETIRED, intentionally skipped
- **Decision:** Caleb dropped the "pick public Fan Profile tags" screen on 2026-10-04. The number S12 stays in the list so screen names line up everywhere; **do not renumber and do not reuse S12 for anything else.**
- **What the flow does:** no prompt, no choices, no draft answer, no state field. Next from S11 (or S10 when S11 is skipped) goes to S13. Back from S13 goes to S11 (or S10 for a non-caster). Edit, Restart and Resume all skip S12.
- **Why:** the Fan Profile is hidden. Players do not see it and do not set it (CORE §3.5, GUIDE §5.3). The System builds it from the S13 survey answers (stored as private notes) and from play. Asking for tags invited a wishlist.
- **Removed with it:** the `fan_profile.public_tags[]` field, the `Fan tags:` card line, and the line-table entry `S12` in `tables/create-flow-lines.json`.
- **Writes:** nothing.

### S13. Customer survey (private notes)
- **Prompt:** "A short customer satisfaction survey. Your answers are private and will not be read aloud. Pass on any."
- **Questions (GUIDE §5.2, core six):** Q1 holding when the world ended; Q2 last unneeded purchase; Q3 harmless thing that terrifies you; Q4 what friends roast you for; Q5 a smell, food or song that makes you happy; Q6 your fight plan. Bonus (0-2): the System picks from the bonus pool, excluding anything touching an S2 Line or Veil ("Describe your mother" is dropped by default, GUIDE Open Q9).
- **Choices:** one line each, max 140 chars; `[Pass]` on any (a pass is data, GUIDE §5.2).
- **Validation:** none beyond length. The System **never says answers become loot** (GUIDE §5.1).
- **What it is for:** S13 is the only place the System asks the player for seed material. The answers are stored as **private notes**; the System reads them to start the hidden **Fan Profile** (likes, fear, running gag, build needs; CORE §3.5, GUIDE §5.3) and keeps refining it from play. The player never sees the profile and the System never says an answer became loot.
- **Writes:** `fan_profile.notes` (one string, `Q1: ... | Q2: ...`) and `build.survey{}` kept private (never on the card). Back: S11 (S10 for non-casters; S12 is retired). Skip: whole screen allowed (the profile is then built from play alone).

### S14. Backstory and requested handle
- **Prompt:** "What did you do before the crawl? Two sentences. The System will read it out at your introduction, so make it worth reading out. Then: what should the audience call you? It's a request, not a promise."
- **Choices:** backstory (max 300 chars; **public**, used in the System's intro; the screen says so); Requested Handle (max 30 chars; `[Skip]` = none).
- **Validation:** non-empty backstory; same text rules as S3 (no links); Lines and Veils from S2 are never quoted back.
- **Writes:** `build.backstory`, `build.handle_request` (log key `HANDLE-REQUEST`, GUIDE §4), `build.broadcast_name` = `PENDING`. Back: S13. Skip: handle only.

### S15. Standing Orders, Standing Reactions, signature attack
- **Prompt:** "Write what your body should do while your brain is in the bathroom. One line for orders. One for reactions. And if you want a name for your best trick, give it one."
- **Choices:** Standing Orders (max 200 chars, required, GUIDE §3.8; no orders = Dodge on timeout); Standing Reactions (max 200 chars; default text "Opportunity Attacks: on"); signature attack name (optional, max 40 chars; names a real attack or spell the crawler has, the tool lists the options).
- **Writes:** `standing_orders`, `standing_reaction` (state.py's spelling, singular), `signature`. Back: S14. Skip: reactions and signature.

### S16. Review (the full sheet)
- **Prompt:** "Here's the file. Read it like it's going to be read aloud, because parts of it will be."
- **Shows** the finished sheet as a **BUILD block** (species + choice, class + choices, background + ASI + Origin feat, skills, tools, masteries, spells, backstory, handle request, orders; no tags and no Fan Profile, because the profile is hidden) followed by the **player-channel card** exactly as the publisher will post it (gm-notes/30 full-card format: header line, ability line, Conditions/Boxes/Titles, INVENTORY with mechanics, ACHIEVEMENTS none). The player's own private survey answers and opt-outs show only to this player, on a separate "Private (only you see this)" fold; the System's Fan Profile is never shown, to anyone but the GM.
- **Choices:** `[Edit <screen>]` (jumps to S3-S15, except the retired S12, and returns here), `[Restart]`, `[Confirm]` (to S17).
- **Validation:** whole-draft legality check before `[Confirm]` enables (every list valid, counts exact, name still free, credits at least 0, party under 4). Any failure names the screen to fix.
- **Writes:** nothing. Back: S15.

### S17. Confirm (the only screen that writes)
- **Prompt:** "Confirm? This locks the file. Corrections after this go through the GM."
- **Steps in order (resume-safe, §4.2):**
  1. Re-run validation and the name check.
  2. Assign the **Intake Tag** `CRAWLER #NNNN-L` (4 digits + 1 letter, unique in the session; cosmetic, GUIDE §4).
  3. If review mode is `hold` (§4.7): save draft as `awaiting_review`, tell the player "filed, pending review", stop. Else continue.
  4. Write the spec JSON to the drafts folder (§3.4) and run `state.py --session <id> create-crawler --file <spec>`. Credits: starting rows first (`reason: "Starting credits: <class option> + <background option>"`, `source: intake`), then one negative row per vending purchase.
  5. Write `<characters dir>/<player>-<crawler>.md` (header per NAMING-CONVENTIONS, content = BUILD block + card).
  6. Register the Crawler's sheet channel `#<player>-<crawler>` under Crawler Sheets (layout §8.3; `discord_gm.py --session <id> setup-channels` or `register-channel`, which NEEDS BUILD for the new naming and the 50-channel overflow) and run `discord_gm.py --session <id> publish --crawler <name> --full` so the **first card** is posted. The auto-publisher also fires after step 4 (a detached job); `--full` makes sure the card is complete.
  7. Add the snark toast achievement for intake (`Paperwork Survivor`, R0, GUIDE §9, pays nothing) via `state.py achievement add`; plus **Don't Skip Intro** if S1 `[Read the Terms]` was used.
  8. Send the player a private "You're registered" message and add one line to a staff log (`create-log.jsonl`, no private content).
  9. Delete the draft.
- **Not granted at Confirm:** no loot boxes (the Welcome Box arrives at the first saferoom, CORE §10.2), no magic items, no Ratings above Unknown, no sponsor (GUIDE §6.5).
- **Back:** none after Confirm. Skip: none.

---

## 3. Data model

### 3.1 Finished crawler (one JSON for `state.py create-crawler`, plus the `build` extension)
Example = Horn. Fields marked in §3.3 do not exist in state.py yet. Values come from characters/hornn-wizard.md and sessions/state.json; anything the sheet does not record is `null` and explained in §3.5.

```json
{
  "name": "Horn",
  "player": "Hornn",
  "class": "Wizard",
  "species": "Human",
  "level": 1,
  "hp_max": 8,
  "ac": 11,
  "abilities": {"str": 12, "dex": 12, "con": 15, "int": 17, "wis": 13, "cha": 15},
  "background": "Merchant",
  "intake_tag": "CRAWLER #NNNN-L",
  "credits": 0,
  "credit_breakdown": [
    {"delta": 5,  "reason": "Starting credits: Wizard package A", "source": "intake"},
    {"delta": 22, "reason": "Starting credits: Merchant package A", "source": "intake"},
    {"delta": -6, "reason": "Vending Wall: Rations x12", "source": "intake"}, {"delta": -1, "reason": "Vending Wall: Rope 50 ft", "source": "intake"},
    {"delta": -5, "reason": "Vending Wall: Healer's Kit", "source": "intake"}, {"delta": -2, "reason": "Vending Wall: Crowbar", "source": "intake"},
    {"delta": -1, "reason": "Vending Wall: Ball Bearings", "source": "intake"}, {"delta": -5, "reason": "Vending Wall: Steel Mirror", "source": "intake"},
    {"delta": -5, "reason": "Vending Wall: Chain 10 ft", "source": "intake"}, {"delta": -2, "reason": "Vending Wall: Grappling Hook", "source": "intake"}
  ],
  "inventory": [
    {"name": "Box Cutters (Daggers)", "qty": 2, "notes": "", "mechanics": "1d4 piercing, Finesse, Light, Thrown (range 20/60).", "category": "weapons"},
    {"name": "Cracked Phone App (Spellbook)", "qty": 1, "notes": "", "mechanics": "Holds your wizard spells; ritual-cast from it.", "category": "weapons"}
  ],
  "standing_orders": "Make it to the nearest available safe room unhindered by mobs; if none, follow the closest party member with the highest Strength.",
  "standing_reaction": "Opportunity Attacks: fire Fuck 'Em (variable-tuned Magic Missile)",
  "signature": "Fuck 'Em",
  "fan_profile": {
    "quirks": [],
    "notes": "Q1: My dog Pebbles | Q2: Bottles of sulfuric acid | Q3: Social events and bills | ...",
    "opt_outs": []
  },
  "notes": "",
  "build": {
    "pronouns": null,
    "look": "Cad Bane with long hair, a mullet; cowboy-hippie-wizard-rocket-scientist vibe",
    "hook": null,
    "backstory": "(sample backstory text)",
    "species_choice": null,
    "background_asi": null,
    "origin_feat": null,
    "score_method": "roll 4d6dl1, three arrays, kept set 1",
    "skills": null, "tools": ["Navigator's Tools"], "saves": null, "weapon_masteries": null,
    "spells": {"cantrips": null, "prepared": ["Magic Missile"], "spellbook": null},
    "handle_request": null, "broadcast_name": "PENDING",
    "kit": {"class_option": "package A", "background_option": "package A"},
    "created_via": "create-flow", "flow_version": "0.1.2"
  }
}
```
(Inventory cut to 2 of Horn's 16 intake items for space; the credit rows are complete and sum to `credits` = 0, as `create-crawler` requires. `fan_profile.quirks` stays empty at creation: the System fills the Fan Profile from the survey notes and from play. Worked example: §3.5.)

### 3.2 Field map
Each screen's **Writes** line above is the field map. **Supported by `create-crawler` today:** `name, player, class, species, level, hp_max, ac, abilities, background, intake_tag, credits + credit_breakdown, inventory[] (name, qty, notes, mechanics, category), standing_orders, standing_reaction, signature, fan_profile {quirks, notes, opt_outs}, notes`. Everything else is `NEEDS state.py support` (next section).

### 3.3 NEEDS state.py support (consolidated)
1. `create-crawler` copies a new `build{}` object (free-form, copied whole; today it drops unknown keys).
2. `fan_profile.opt_outs[]` as objects `{kind, topic, shared}`; check the GM runtime filter and the publisher both tolerate non-string items.
3. Hit Die **size** (state has `hit_dice {current,max}` only; die size lives in `build.hit_die`).
4. Death saves object (`death_saves`) is on Horn's live record but not in `new_crawler` / `create-crawler`; add `{successes:0, fails:0}` default.
5. Unique `intake_tag` check per session.
6. Party cap: `limits.max_crawlers` (default 4) checked by `create-crawler` (decision 013).
7. `tools/README.md` does not document `create-crawler`; add the spec format and the `credit_breakdown` rule (sums to `credits`; gains first).
8. Publisher: post **no** `fan_profile` field on any card (the Fan Profile is hidden); add `build` display lines if Caleb approves card format v0.2 (Open Q3).
9. **Remove (v0.1.2):** tools that already handle `fan_profile.public_tags[]` or the `Fan tags:` card line (state.py, publisher.py, tools/README.md, tests, `tables/create-flow-lines.json` S12 entry) must drop it; see the report to Borent.

### 3.4 Other files the flow needs (not state.py)
| File | Owner | Content |
|---|---|---|
| `sessions[-data/<id>]/create-drafts/<discord-user-id>.json` (mode 600) | Borent | the in-progress draft: `{screen, answers, optouts, status, updated}` |
| `tables/chargen-5e.json` | Borent builds from SRD 5.2 / PHB, Valtay checks | species, classes, backgrounds, skills, kits, prices, spell lists, plain effect lines |
| `tables/create-flow-lines.json` | Syndicate/Valtay | all System lines by screen, with 3 variants each |
| `tables/prebuilt-crawlers.json` | Syndicate | pre-builts (§4.6; GUIDE Open Q10) |

### 3.5 Worked example: Horn through the flow (only data in his sheet)
Source: characters/hornn-wizard.md v0.4 and sessions/state.json. Blank = not recorded; the real flow would have asked.

| Screen | Horn's answer |
|---|---|
| S1-S2 | Accepted (his sheet lists the toast Don't Skip Intro). Opt-outs: none recorded |
| S3-S4 | Name **Horn** (player Hornn); pronouns not recorded. Look: "Cad Bane with long hair, a mullet; cowboy-hippie-wizard-rocket-scientist vibe"; hook not recorded |
| S5 | **Human**; quirk line "Baseline. Congratulations on being the control group." (GUIDE §7.2); Versatile and Skillful picks not recorded |
| S6 | **Wizard** 1, Hit Die d6 (SRD 5.2 checked) |
| S7 | **Merchant**; the sheet does **not** record the +2/+1 choice or the Origin feat |
| S8 | Rolled 4d6 drop lowest, three arrays, kept set 1 (84; under the v0.1.10 Roll rule this array would qualify, 84 is above 72): STR 12, DEX 12, CON 15, INT 17, WIS 13, CHA 15. HP **8** (d6 max 6 + CON 2), AC **11** (10 + DEX 1; robe gives none). The scores sum to 84, the raw rolled total, so the Merchant bonus is not visibly applied: `VERIFY` before the flow reuses this sheet as a test fixture |
| S9 | Tools: Navigator's Tools (Merchant package). Skills not recorded |
| S10 | Wizard **package A** (2 Daggers, Arcane Focus (Quarterstaff), Robe, Spellbook, Scholar's Pack, 5 GP) + Merchant **package A** (Navigator's Tools, 2 Pouches, Traveler's Clothes, 22 GP) = **27 credits**. Spent all 27: Rations x12 6, Rope 1, Healer's Kit 5, Crowbar 2, Ball Bearings 1, Steel Mirror 5, Chain 5, Grappling Hook 2. **Credits left 0** |
| S11 | Magic Missile (his signature "Fuck 'Em"); other spells not recorded |
| S12 | RETIRED, intentionally skipped. Horn has no tags; the System builds his hidden Fan Profile from the S13 answers below and from play |
| S13 | Q1 My dog Pebbles; Q2 Bottles of sulfuric acid; Q3 Social events and bills; Q4 For not having any friends; Q5 Smell of rain coming (petrichor); Q6 Win and not be the one on the ground or dead; Bonus1 Whatever hill my kids are on |
| S14 | Backstory: (sample text); Requested Handle not recorded; Broadcast Name PENDING |
| S15 | Orders: nearest available safe room unhindered by mobs, else follow the closest party member with the highest Strength. Reactions: Opportunity Attacks fire Fuck 'Em (variable-tuned Magic Missile). Signature: Fuck 'Em |
| S16 | Card (gm-notes/30 format): `HORN - Human Wizard 1 (Hornn)   HP 8/8  AC 11  Credits 0  XP 0` / `STR 12 DEX 12 CON 15 INT 17 WIS 13 CHA 15` / `Conditions: none   Boxes: none   Titles: (none)` / `INVENTORY` with `Box Cutters x2 (Dagger): 1d4 piercing, finesse, light, thrown 20/60` and the rest of his intake items |
| S17 | Credits ledger: +5, +22, then eight negatives totalling -27, balance 0. Intake Tag not recorded; the flow would assign one. Items later in his sheet (Snow Globe, Banner) are play loot, not intake |

---

### 3.6 Roll method: what the Architect built (v0.1.10, decision 024; built and audited, live since 2026-10-04 20:26 CT)
**Switch.** `create.allow_roll` (boolean, session `create` settings next to `review_mode`; **default true**). `tools/new-session.py` writes `"allow_roll": true` for a new session (`--no-roll` writes false; a missing or non-boolean value also means ON); documented in tools/README.md. Read it every time S8 renders and on every Roll press. (No `limits.*` copy: one switch only.)

**State fields (draft, then `build` on Confirm).** `build.score_method` = `"array" | "pointbuy" | "roll"`; `build.score_base{str..cha}` = the assigned base scores; `build.score_rolls` (roll only):
```json
{"rounds": [
  {"round": 1, "qualified": false, "arrays": [
    {"id": "A", "dice": [[5,3,1,6],[4,4,2,6],[3,3,5,2],[6,6,4,1],[2,5,5,3],[4,1,6,2]], "scores": [14,14,11,16,13,12], "total": 80, "keepable": true}, "...B...", "...C..."]}],
 "kept": {"round": 1, "array": "A"}}
```
`dice` are the four d6 as rolled (lowest dropped when summing); `total` and `keepable` (`total > 72`) are computed by the tool and re-checked from `dice` at S17. Saved in the draft the moment a round is rolled (no free rerolls, §2 S8 item 8).

**Roll-log entries.** One `tools/roll.py` call per score, 18 per round, `--who` = the Crawler's name (S3), `--label "S8 roll r<round> <A|B|C><1-6>"`, expression `4d6dl1`. Example line in `sessions/rolls-YYYY-MM-DD.log` (alpha; other sessions use `sessions-data/<id>/rolls-YYYY-MM-DD.log`): `[ROLL] S8 roll r1 A1 (Horn): 4d6dl1 -> [5, 3, 1, 6] keep 5, 3, 6 = 14`. Rerolled rounds (r2, r3...) are logged the same way. The keep choice is not a die roll; it lives in `build.score_rolls.kept`.

**Screen text and lines.** Add these keys to `tables/create-flow-lines.json` (Architect's file; Syndicate does NOT edit it). The existing `S8` line stays unchanged. Placeholders: `{total}`, `{rounds}`.
- `S8_roll_offer`: "Roll: the System rolls three arrays of six scores (4d6, drop the lowest die, six times each). You keep ONE, and only an array that totals 73 or more. If none does, the System rolls all three again."
- `S8_roll_result`: "Three arrays. Keep one that totals above 72. The numbers are not wrong. They are just yours."
- `S8_roll_keep_ok`: "Keepable (total {total})"
- `S8_roll_keep_no`: "Not keepable (total {total}, needs 73 or more)"
- `S8_roll_none`: "None of the three totals above 72. The System has filed your luck and is rolling all three again."
- `S8_roll_assign`: "Assign your scores. Each number goes to one ability, once. Decide where the highest one goes first; the audience is watching."
- `S8_roll_cap`: "Background bonuses are added after. No score goes above 20."
- `S8_roll_giveup`: "{rounds} rounds and no array above 72. That should not happen. Pick the standard array or point buy."
- `S8_roll_closed`: "That method is closed today. Pick the standard array or point buy."

**Also retire/replace.** The old reroll-allowance idea (Open Q1) is gone: no counter. `new-session.py` default is true as above. `guides/create-how-to.md` line 18 now calls Roll a normal third method (Borent's file).

## 4. Edge cases

### 4.1 Re-roll and restart
- **Back** never loses answers. **Edit** from S16 keeps the rest and re-validates dependents (species/class/background changes re-run S8-S11 previews, drop picks that became illegal, and say which).
- **Restart** (confirm button, then wipe all answers except S2 comfort). Two restarts in a row are allowed; there is no limit and no penalty.
- **Rerolling stats (v0.1.10):** there is no player reroll. The only reroll is the System's, when none of the three arrays totals above 72 (S8 Roll method item 4). Every round is logged and kept in `build.score_rolls`; Back, Edit and Restart show the same saved rounds (no free rerolls).

### 4.2 Disconnect or timeout (resume)
- The draft is saved after every screen (§3.4). `/create` with a draft open re-posts the **current screen** with a "Resume / Start over" prompt. Discord interaction messages go stale after about 15 minutes (Borent to confirm), so the bot re-sends rather than editing.
- Drafts idle for 14 days *(design)* are archived to `create-drafts/_archive/`; nothing is deleted.
- **Crash during S17:** the draft keeps `status: state_written` / `sheet_written` / `channel_done`; resume continues from the first undone step. `create-crawler` refuses a duplicate name, so a retry after step 4 is safe (skip step 4 if the crawler already exists for that player).
- No nudges, no straggler timers (this is not a table round).

### 4.3 Duplicate names
Case-insensitive duplicates are refused by the tool and by S3. This is a name check, not a one-Crawler-per-player check: the same player's second Crawler with a different name passes (§8.2 item 1); an identical name for the same player is refused; an identical name for another player is also refused, because tools match Crawlers by name. Near-duplicates (one name contains another: `Horn` / `Hornet`): warn and require a second tap, because tools match crawlers by exact name first, then a unique partial. Two players picking the same name at the same time: the first to Confirm wins; the other is sent back to S3 with the plain message "taken".

### 4.4 Party size is four (decision 013)
- `create-crawler` and S1 stop at **4 active Crawlers per session** (`limits.max_crawlers`, NEEDS). A fifth player's first `/create` gets "Party full." Benched Crawlers take no slot (§8).
- **v0.1.4:** a Discord user may have **many Crawlers** per session (§8); exactly one is active. Replacement after a death is a GM-run step: the player's benched Crawler is swapped in **between sessions** (§8.2 item 8), with level, gear and the late-entry Silver box per CORE §6.3 as written there.
- Fewer than four players is fine (CORE §2.4: 2-6 crawlers).

### 4.5 Table setup is not in the flow
Death Mode, Floor 1 Reprieve, dice, timeouts and blocks (GUIDE §2) are set by Caleb; S1 only shows them. Unset in a new session = "Table not set up" and the flow stops.

### 4.6 Pre-built shortcut
S1 `[Use a pre-built]` shows 12 concepts (one per class, 36 later; GUIDE §8.1, Open Q10) with name, class, background, species, array assignment and kit A/A, all legal. Choosing one fills S5-S11 and S15. The player **still does** S2 (comfort), S3 (name), S4 (look/hook), S13-S14 and S16-S17, and can `[Edit]` any pre-filled screen. A pre-built never skips review or Confirm. Marked `build.created_via: "create-flow-prebuilt"`. `tables/prebuilt-crawlers.json` NEEDS writing (Syndicate).

### 4.7 GM review gate
- **Setting:** `create.review_mode` per session: `off` (register at Confirm), `notify` (register, post a staff note), `hold` (S17 stops at step 3; nothing reaches state until approved). Recommended for beta: `hold`.
- **What the reviewer sees:** the BUILD block, the card, backstory, handle request, and **only** opt-outs the player marked **shared** (as topic and Line/Veil). Unshared opt-outs show as "Opt-outs: set (private)" with a count and nothing else. Survey answers show only if the player chose to share (`S13` has no share switch in v0.1; default private, reviewer sees "Survey: answered"). The Fan Profile is not a review item: it does not exist until the System builds it after creation.
- **Reviewer actions:** `/create approve <player>` (runs S17 step 4 onward) or `/create return <player> <screen> <note>` (sends the player back to a screen with a short note; their other answers stay). Who may use them: Caleb and the GM role (Borent to wire).
- **Important:** the AI GM still **obeys every opt-out** at runtime (GUIDE §2.4); "private" here means not visible in review views or to other players, not ignored.

### 4.8 Other cases
| Situation | Ruling |
|---|---|
| Player wants a non-SRD species or class, table lacks PHB | SRD only; the screen explains and offers the closest option (CORE §7.1, GUIDE §10.3) |
| Homebrew species or class | Not in the flow (owner approval only, CORE §7.1) |
| A rule changed after drafts were saved | Drafts record `flow_version` and `chargen_table_version`; a mismatch re-validates on resume |
| Two sessions (alpha and beta) | The draft folder is per session; `/create` uses the active session and shows its id on S1 |

---

## 5. Terms glossary (tool and book must use these exact words)

Rule: in the System's voice use the flavor term first; in rules text use the plain 5e term, and on first use show both: `Prior Employment (background)`. Spelling is fixed. Capitalization: capitalize the flavor terms; lowercase the plain terms.

| Term | Means | Do not say | Source |
|---|---|---|---|
| crawler | a player character in the Crawl | PC, player (for the character), adventurer | CORE, GUIDE |
| the System | the in-world voice and rules engine (also the AI as DM) | the AI, the bot (in player text) | GUIDE |
| Provisional Class | class at level 1 (the Official Class Title comes on Floor 3) | final class | GUIDE §3.3, CORE §7.3 |
| Prior Employment | background | job class | GUIDE §3.4 |
| Roll (ability-score method) | the S8 method: three arrays of six 4d6-drop-lowest scores, keep ONE that totals 73 or more | reroll (for the System's reroll when none qualifies, say "the System rolls again") | decision 024 |
| Latent Biology | species (traits work now; body manifests on Floor 3) | race | GUIDE §3.5, CORE §7.2 |
| Origin feat | the feat a 2024 background gives | background feat | CORE §1.1 |
| Standing Orders / Standing Reactions | the two default lines used on timeout or Autopilot | macros, scripts | GUIDE §3.8 |
| Signature attack | the optional name a player gives their best attack | | state `signature` |
| Fan Profile | the System's **hidden** file used to tailor loot. The System builds it from the S13 survey answers (stored as private notes) and from play; players never see it and never set it | wishlist, loot preferences, tags | CORE §3.5, GUIDE §5.3 |
| Private notes | the player's S13 survey answers, kept in `fan_profile.notes`; never shown, never read aloud, never on the card | public tags, requests, wants | this file |
| Retired screen | a screen number kept in the list but skipped (S12 since v0.1.2); never renumber, never reuse | deleted screen | this file |
| Line / Veil | private opt-outs: a line never appears; a veil is faded to black. Plus the word **cut** in play | safeword list | GUIDE §2.4 |
| COMFORT | table content level; campaign value Ludicrous | rating | GUIDE §2.3 |
| Intake Kiosk | the in-fiction place where `/create` happens | character builder | GUIDE §3.1 |
| Death Mode | Costly Revives (campaign default) | difficulty | CORE §6.0, decision 002 |
| Floor 1 Reprieve | once-per-crawler Floor 1 death mercy (table option) | respawn | CORE §6.2 |
| Intake Tag | cosmetic `CRAWLER #0417-K` | ID, serial | GUIDE §4 |
| Broadcast Name / Requested Handle | the name the audience uses (PENDING until Floor 3) / the player's request | username | GUIDE §4, CORE §5.1 |
| credit | in-world money, 1 credit = 1 GP | gold, coins (in System text) | CORE §5.10 |
| Intake Vending Wall | where leftover gold buys gear at 5e prices | shop | GUIDE §6.1 |
| System Inventory | extradimensional inventory | backpack | CORE §5.9 |
| saferoom | the one-word safe room where Long Rests and box opening happen | safe room, safehouse | CORE §5.6 |
| Welcome Box | the first Bronze loot box, opened in the first saferoom | starter pack | CORE §10.2 |
| Benefactor | a sponsor who sends Benefactor Boxes; no crawler has one at creation (sponsors mostly Floor 6+). Not the same as a Warlock's patron | patron, god | CORE §4.7, §5.2 |
| active Crawler | the one Crawler a player has in play this session; the only one that counts for party, slots, budgets, credits, XP, loot and boxes (pet-Crawlers go with their owner) | main, current character | §8, decision 020 |
| benched Crawler | a Crawler on file that is not active: no slot, no credits, no XP, no loot, no trades | inactive, backup, alt | §8, decision 020 |
| session | one campaign table: `alpha` is live, `beta` is the new table | save, campaign (for a table) | tools/campaign_session.py |

---

## 6. Beta checklist and test script

### 6.1 What a new session with four new players needs
- [ ] New session created: data folder `sessions-data/beta/`; `state.py --session beta init --floor 1` (campaign defaults: Costly Revives, Ludicrous); F1 Reprieve set by Caleb; dice and timeouts confirmed (GUIDE §2).
- [ ] GM quirk roll sealed for beta (`state.py --session beta gm-quirks roll`); the flow never reads it.
- [ ] `tables/chargen-5e.json`, `tables/create-flow-lines.json` finished and version-stamped; VERIFY items closed.
- [ ] Discord: bot has Manage Channels (for `setup-channels`) or channels are made by hand and registered; the "Crawler Sheets" category exists for beta; a staff channel for review notes.
- [ ] Review mode decided (Open Q5); `create.allow_roll` checked (default ON since v0.1.10; Roll is a normal S8 method); content source set (2024 PHB owned or SRD only).
- [ ] Four players linked to Discord ids (unique `player` names); Valtay's player guide uses the §5 terms and the S1-S17 names (S12 is retired: 16 active screens).
- [ ] Sheet channel: on confirm, `/create` files `#<player>-<crawler>` under Crawler Sheets (pet-Crawlers `#<player>-<pet>-sheet`) and posts the first card; a category holds 50 channels, so the tool opens an overflow category (§8.3). In hold mode the channel appears only after a reviewer approves. GM confirms with `discord_gm.py channels` and runs `setup-channels` by hand on a miss (Caleb, 2026-10-04).
- [ ] Voice bridge unaffected: nothing from `/create` appears in #gm-voice or #table-transcript; wake usage log shows 0 wakes from the flow.

### 6.2 Ten-item test script
| # | Test | Expected |
|--:|---|---|
| 1 | Run `/create` in beta as player A through the 16 active screens (S1-S17 without S12) with defaults (standard array, Human Fighter, Soldier) | Draft saved each screen; Fighter skips S11 and S12, so Back from S13 lands on S10 (a caster lands on S11); S12 never appears; no `public_tags` key in the saved state; at S17 one crawler appears in `sessions-data/beta/state.json`; sheet file in `sessions-data/beta/characters/`; alpha `sessions/state.json` unchanged (compare checksums) |
| 2 | Check A's numbers by hand | HP = Hit Die max + Con modifier; AC matches worn armor; abilities = base + background bonus; no score above 20 |
| 3 | Credits: A takes package + package, then a second crawler B takes gold + vending | A credits = GP from packages; B balance after spends is at least 0; `state.py --session beta ledger verify` exits 0 and shows `intake` rows with reasons |
| 4 | Disconnect A's client at S9, return an hour later | `/create` offers Resume at S9; answers kept; no duplicate draft |
| 5 | Player C enters two Lines and one Veil at S2, marks one shared; finish with `review_mode: hold` | Reviewer view shows the shared topic only, plus "Opt-outs: set (private)"; unshared topics appear nowhere (grep the card, the sheet file, the channel, the staff note, `create-log.jsonl`) |
| 6 | Two players type the same name at the same time; a third types `Horn` when `Hornet` exists | First Confirm wins; second is sent back to S3 with "taken"; near-duplicate warning shows |
| 7 | Player D picks a Wizard: S11 asks cantrip and spell counts per the table; a Fighter skips S11 | Counts match the verified class table; invalid counts block Next; the Fighter never sees S11 |
| 8 | Fifth `/create` after four crawlers are registered | "Party full." No draft, no write |
| 9 | Player E uses `[Use a pre-built]` and changes the species at S16 `[Edit]` | Pre-filled screens legal; the edit re-validates dependent picks; Confirm succeeds; `created_via: create-flow-prebuilt` |
| 10 | After all four register: card check and isolation check | Each player's channel has exactly one first full card in gm-notes/30 format with credits line first; no private survey, no opt-outs, no tags and no Fan Profile content in any channel; GM wake log shows 0 wakes from the flow; nothing under `gm-notes/secret/` changed (hash) |

---

## 7. Open questions for Caleb (6 open, 3 resolved)

1. **Rolling stats in beta?** **RESOLVED by Caleb, 2026-10-04 (decision 024):** Roll is a third method at S8: three arrays of 4d6-drop-lowest, keep ONE that totals above 72 (no upper limit), reroll all three if none qualifies, every die logged, switch `create.allow_roll` default ON. No table vote and no reroll allowance.
2. **Fan Profile visibility.** **RESOLVED by Caleb, 2026-10-04: the public-tags screen is dropped.** The Fan Profile is hidden and built by the System from the S13 survey answers (private notes) and from play (CORE §3.5, GUIDE §5.3). S12 is retired (number kept), `public_tags[]` and the `Fan tags:` card line are gone, and asking for a specific item is still Customer Feedback.
3. **Show new fields on the player card?** gm-notes/30 shows no class features, skills or spells. **Default:** add a BUILD block (skills, spells, Origin feat) to the first card; no tags and no Fan Profile line (hidden); update gm-notes/30 to v0.2.
4. **Questionnaire length.** GUIDE Open Q1: six core plus up to two bonus, or fewer? **Default:** keep the six, bonus 0-2, all skippable.
5. **Review mode for beta.** `off`, `notify` or `hold`? **Default:** `hold` for the four beta sheets, then `notify`.
6. **Opt-outs and the GM.** Spec: the AI GM obeys all opt-outs but reviewers see only shared topics. Is the AI GM allowed to read unshared Line/Veil text at runtime? **Default:** yes (it must, to obey), never quoted, never shown in review views or logs.
7. **Background pool.** Table owns the 2024 PHB (16 backgrounds) or SRD only (4)? **Default:** PHB 2024 if you own it; alpha already used Merchant and Artisan, which are PHB backgrounds.
8. **Sheet file names.** NAMING-CONVENTIONS says `<player>-<character-name>.md`; alpha files are `hornn-wizard.md` and `moses-barbarian.md`. **Default:** new files follow the convention (`hornn-horn.md`); leave alpha files as they are.
9. **Sheet layout for many Crawlers.** **RESOLVED by Caleb, 2026-10-04:** one text channel per Crawler under Crawler Sheets, named `<player>-<crawler>` (e.g. `#hornn-horn`); no forums, no Community mode (§8.3). Still a Syndicate default for you to override: the 10-per-player guideline, benched Crawlers, and the swap lock details in §8.2.

---

## 8. Multiple Crawlers per player and the active Crawler

**Status of this section.** Every ruling here is a **Syndicate default, Caleb may override** (`decisions/020-multiple-crawlers-active-swap.md`, status final-pending-Caleb-override), with these exceptions: the **session lock** in §8.2 items 5-7 is Caleb's change of 2026-10-04 (characters belong to one campaign, and nobody brings a different Crawler in halfway through a session). The sheet layout (§8.3, one text channel per Crawler) and the `/delete` command (§8.5) are Caleb's decisions of 2026-10-04. No new numbers are invented: level and gear for a late entrant cite CORE §2.3 and §6.3, and the Story Box cap cites `rules/45-story-boxes-5e.md` §1.2 and §6.1.

### 8.1 Terms
- **Campaign:** the table a Crawler is filed in (the state session id, e.g. `alpha` or `beta`, §1). A Crawler belongs to **one campaign** and never moves to another.
- **Play session ("session" below):** one sitting, from the moment the GM opens it until the GM closes it. **Open session** = between those two moments. **Outside an open session** = session zero or between sessions (before the next session starts).
- **Active Crawler / benched Crawler:** see the glossary (§5). A player's Crawlers are all filed under their Discord account; exactly one is active.

### 8.2 Rulings (Syndicate default, Caleb may override)
1. **Any number of Crawlers.** A player may create as many Crawlers as they like. Soft guideline: **10 per player**; the GM may allow more. `/create` **always creates a new Crawler**. The duplicate check (§4.3) never blocks a second Crawler for the same player; it blocks only an identical name (case-insensitive) for the same player. It also still blocks an identical name used by another player, because tools find Crawlers by name (resolved this way on purpose).
2. **One campaign per Crawler.** A Crawler is filed in one campaign (alpha, beta, ...) and its sheet, state record and ledger stay there. It cannot be copied or moved into another campaign.
3. **Exactly one active Crawler per player.** **Pet-Crawlers are the exception:** they take no slot, count as active with their owner, and are played by the owner (`rules/45-story-boxes-5e.md` §2.4; rules/42 §6.2). Only the **active** Crawler counts toward the party, the 4 slots (decision 013) and encounter budgets, earns credits, XP and achievements, can receive loot, boxes or Story Boxes, and takes part in the session.
4. **Benched Crawlers stay on file and are inert.** No slot, no credits, no XP, no loot, no boxes, no ledger changes, and **no trades in or out**: a player cannot move items or credits between their own Crawlers (CORE §4.4 already makes boxes untradeable; items and credits fall under this rule).
5. **New Crawlers.** The first Crawler a player creates is active automatically. A later `/create` makes the new Crawler **benched**. The player may pick **"make active now"** on S17 or via `/crawlers`; it needs GM approval and is allowed **only outside an open session** (session zero or between sessions). During an open session the option is refused with a plain message, even in a safe room.
6. **Swap rule (the session lock).** Each player **locks one active Crawler for the whole session**. The active Crawler can change **only at session zero or between sessions, before the next session starts**. The tool and `/crawlers` **refuse any swap while a session is open, even in a safe room.** The GM runs the swap and **logs every one** (who, from, to, floor, reason, date). **One swap per player per between-session window.** A swap is a file change: it does not enter the fiction. The swapped-in Crawler enters play at the next saferoom or a natural fictional entry (CORE §6.3).
7. **Mid-session death.** A dead Crawler is pretty much game over (CORE §6.2; Costly Revives stays very costly and rare, §6.4; nothing here weakens that). The player **cannot** bring in a benched Crawler during the open session. Until the next between-session window the player either **sits out** (watches; no XP, loot or ledger changes) or, if the GM offers, plays a **temporary GM-offered companion** under the existing rule: CORE §2.4 Assigned Companion (GM-run, takes no loot, can die, has opinions). That rule is written for 2-Crawler tables, so using it here is part of this default. If the player already has a pet-Crawler (item 3), it simply continues with its owner. At the next between-session window the player may swap in one of their **benched Crawlers** as the replacement, under item 6 and item 8. If the dead Crawler is revived later, CORE §6.3's last line applies: the player picks which Crawler to keep.
8. **Level and gear of a swapped-in Crawler.** It keeps its own level, kit, achievements and credits as filed. If it is behind the party, the existing catch-up rule applies: it is brought to the **party's lowest current level at the next saferoom**, and no one levels above the floor band (CORE §2.3 Catch-up, §6.3 Level). The GM does not grant more than that. The §6.3 gear package and the one **Silver late-entry box** are for a **brand-new entrant**: a benched Crawler swapped in does **not** get them, and a Crawler created after a death and made active is a §6.3 replacement as written. The GM decides which case applies and logs it.
9. **Story Boxes.** The one-per-table-per-floor cap and the spotlight rota (`rules/45-story-boxes-5e.md` §1.2, §6.1) count the **active** Crawler only. A Story Box award goes to the active Crawler. A benched Crawler is not on the spotlight list. Deleting a Crawler frees its Story Box slot (§8.5 item 7: the cap counts only Story Boxes held by live, non-deleted Crawlers). A Story Box reclaimed unopened when its Crawler dies also frees its slot (§8.5 item 7).
10. **Abuse guard.** Using benched Crawlers as item or credit mules is not allowed. The GM may refuse any swap or "make active now" and logs why. `/delete` is **log only, no flags or alerts** (§8.5 items 6 and 8).

### 8.3 Sheet layout (DECIDED by Caleb, 2026-10-04: one text channel per Crawler)
**Decision.** Every Crawler gets **its own text channel** under the **Crawler Sheets** category, named **`<player>-<crawler>`** (lowercase, hyphens; e.g. `#hornn-horn`, `#hornn-testpally`, `#moses-bone`). A player's channels share a name prefix, so they sit together and each one is a click. No forums, no Community mode. (A Discord forum per player was considered and dropped.)
- **Pet-Crawlers** get their own owner-prefixed channel in the same style as today's `<name>-sheet` channels: **`<player>-<pet>-sheet`** (e.g. `#hornn-biscuit-sheet`). The prefix keeps it with its owner's channels.
- **Benched Crawlers** keep their channel and card (the header shows BENCHED). The first full card posts on Confirm as today (S17 step 6).
- **Limit.** A Discord category holds at most **50 channels**. With the 10-per-player guideline and four players that is 40 plus pets, so the tool must warn the GM at 45 and then file new sheets in an overflow category (`Crawler Sheets 2`, `Crawler Sheets 3`, ...) instead of failing. Channel names are 1-100 characters; the tool shortens a long `<crawler>` slug and keeps it unique.
- **Rename and delete.** A Crawler's channel is removed only by `/delete` (§8.5). The name of a channel never changes the sheet map key, which is the crawler id (§8.4 item 2).

### 8.4 Tool requirements for the Architect (all NEEDS BUILD)
1. **Per-Crawler sheet channel** (§8.3): on Confirm create `#<player>-<crawler>` under Crawler Sheets (pet-Crawlers `#<player>-<pet>-sheet`), post the first card, and move to an overflow category before the 50-channel limit. Keep the existing `setup-channels` / `register-channel` behaviour working for old entries.
2. **`state.json` sheet map keyed by crawler id**, with `owner` (the player) as a field on each entry; no map keyed by player. Replaces the player-keyed channel map for new Crawlers; old entries keep working.
3. **`active` flag per player**, enforced in `party --json` and everywhere a Crawler is chosen: party size, the 4-slot cap, encounter budgets, credits, XP, achievements, loot, boxes, Story Boxes (cap and rota), and the ledger. Benched Crawlers are refused with a clear message. Pet-Crawlers follow their owner's active state and take no slot.
4. **Session open/closed marker** the tools can read, so a swap (and an active-Crawler delete) can be refused while a session is open (use the existing active-session record if it can carry this).
5. **GM-only `state.py` swap command** (name for the Architect to choose, e.g. `crawler swap <player> --to <crawler> --reason ...`): **refuses while a session is open, even in a safe room**; enforces one swap per player per between-session window; refuses a swap when the target is not that player's Crawler; writes the **swap log** (who, from, to, floor, reason, date, GM) and a refused-swap log line with the reason (abuse guard). Also covers the approved "make active now".
6. **`/create` creates benched Crawlers** for a player who already has one; the player's first Crawler is active; `create-crawler` stops enforcing one Crawler per player and counts only active, non-pet Crawlers against `limits.max_crawlers`; duplicate check per §4.3.
7. **`/crawlers` player command** (name may differ): lists the player's own Crawlers (name, class, level, active or benched, floor) with links to their sheet channels, shows the active one, and lets the player **request** a swap or "make active now". The request goes to the GM, who approves with the swap command (item 5). **While a session is open it refuses with a plain message**; it never changes state by itself.
8. **Transfer guard:** item, credit and box moves between two Crawlers owned by the same player are refused, whether benched or active.
9. **Publisher:** keep benched sheets posted and mark them BENCHED; update the card header on swap; no new fields on the card beyond that.
10. **`/delete <name>` command and a `state.py` delete step** (§8.5): own Crawlers only; typed-name confirm; refuses the active Crawler while a session is open; removes the sheet file, the card record and the text channel; archives the Crawler's state record, sheet file and ledger rows (moved, never destroyed) so `ledger verify` still passes on the live ledger and the archive; writes the delete log.
11. **Story Box cap check ignores archived and reclaimed rows:** `loot story-box` counts, per floor, only Story Boxes held by non-deleted Crawlers. Archived (deleted) rows stay for audit and the Accountant and never count. A dead Crawler that has not been deleted still counts when it holds an opened or already-awarded Story Box item (rules/45 §6.3). **A Story Box reclaimed unopened at its Crawler's death does not count** (its slot is freed; the ledger row for the reclaimed box is the Accountant's / Lore's, rules/45 §6.3).
12. **Biscuit rule: one conversion per LIVING pet-Crawler** (no tombstone; confirmed by Caleb 2026-10-04). The conversion check looks only at non-deleted pet-Crawlers. Deleting a pet-Crawler removes it like any Crawler; a new conversion needs a new Enhanced Pet Biscuit, which needs a freed Story Box slot, so no free reset.
13. **Delete log, log only:** `/delete` writes the delete log (§8.5 item 6) and nothing else: **log only, no flags or alerts**, no warning to the player or the GM, no block (§8.5 item 8).

### 8.5 `/delete <name>`: removing a Crawler (Caleb, 2026-10-04; details are Syndicate defaults)
1. **Who and what.** A player runs `/delete <name>` and may pick **only their own Crawlers** (the name list shows only theirs; another player's Crawler is refused). It deletes the Crawler's **sheet file**, its **published card record** and its **text channel**.
2. **Confirm step.** The bot first says plainly what goes away and that nothing is refunded, then asks for a second step: the player **types the exact Crawler name** (a button alone is not enough; the default answer is cancel). Resolved this way because the brief allowed a button or a typed name.
3. **Active Crawler.** The **active** Crawler **cannot be deleted while a session is open.** Benched Crawlers can be deleted at any time. The active Crawler can be deleted between sessions (or at session zero). That leaves the player with no active Crawler, so they name a new one in the same window; that pick is the window's one swap and the GM logs it (§8.2 item 6).
4. **Ledger and archive.** The Crawler's ledger rows are **moved** to an archive, never destroyed (today's precedent is `sessions/test-archive/`; the Architect may use an equivalent such as `sessions/deleted-archive/`), together with a copy of its state record and sheet file, so `ledger verify` still passes and the Accountant can reconcile the vanished credits and items. (NAMING-CONVENTIONS: never delete, archive.)
5. **No refund, no un-spend.** Deletion refunds nothing and un-spends nothing. The Crawler's credits, gear and boxes leave with it; nothing moves to another Crawler or the party.
6. **GM log.** The GM logs each deletion: who, which Crawler, when, session state (open or closed), whether it was active, alive or dead, and the floor. **Log only, no flags or alerts.**
7. **Story Boxes (Caleb's correction, 2026-10-04).** Deleting a Crawler **frees its Story Box slot**. The one-per-table-per-floor cap counts only Story Boxes held by **live (non-deleted) Crawlers**; archived rows are for audit only and do not count. A **dead** Crawler that is not deleted still counts when it holds an opened or already-awarded Story Box item, as in `rules/45-story-boxes-5e.md` §6.3, until its player deletes it. **A Story Box that is still UNOPENED when its Crawler dies is reclaimed by the System and its slot is freed** (Caleb, 2026-10-04): it no longer counts toward the per-floor cap or the one-per-living-Crawler counting, and another Crawler can be awarded one. Opened or already-awarded Story Box items stay lootable and not bound. The ledger row for a reclaimed box is the Accountant's / Lore's. The deed record stays closed: a deleted deed is not paid twice (rules/45 §2.3).
8. **Cycling.** There is no hard anti-farm rule (Caleb: "we want this hard, but there should be some serotonin and dopamine hits along the way"). `/delete` is **log only, no flags or alerts** (Caleb, 2026-10-04): the GM logs it and raises nothing, including for suspected Crawler-cycling (create, win a Story Box, delete, repeat); the log is there for audit if Caleb ever asks.
9. **Pet-Crawlers.** A pet-Crawler made with the Enhanced Pet Biscuit can be deleted **only on its own**, never as a side effect of deleting its owner's other Crawlers, and deleting its owner's Crawler does not delete the pet: the pet-Crawler **stays on file, benched,** and is removed only by its own `/delete` (Caleb, 2026-10-04). The **biscuit is not restored.** No tombstone is kept (§8.4 item 12): the rule is **one conversion per living pet-Crawler**, so a deleted pet frees its conversion, and a new one needs a new biscuit (one Story Box per floor). Confirmed by Caleb 2026-10-04.
10. **Dead Crawlers.** Deleting a dead Crawler is allowed; corpse loot was already resolved by the existing death rules (CORE §5.9, §6.2).

### 8.6 Interaction with earlier sections
S1, S3, S17 step 6, §4.3, §4.4, §6.1 and the glossary were edited in v0.1.4 to match; test 8 in §6.2 still holds (a fifth player's first `/create` gets "Party full."). The acceptance checklist and the audit checklist for the create feature are the last sections of this file.


## 9. Pets (GM-filed companions): requirements for the Architect

**Status.** The rule is a ruling (Caleb approved the pets rule, 2026-10-04; `decisions/022-pets-and-companions.md`, `rules/60-pets-companions-5e.md`). Command names, field names and file layout below are **proposals**; the Architect decides them. The checklist at the end of this section is unticked.

### 9.1 The one hard rule: `/create` knows nothing about pets
- **No pet field, checkbox, screen, button, choice, hint or help text** in `/create` for anyone, in any screen S1-S17. Players are never asked, prompted, hinted at or offered a pet. A pet exists only if the player wrote it into their **own free text** (an S13 answer or the S14 backstory) and the GM then files it.
- **The questionnaire contains no pet question.** Today `tables/create-flow-lines.json` has a bonus survey question with id `pets` ("Cats or dogs? Wrong answer either way, but tell us."). It must be **removed** (and any test or doc that names it), because it asks about pets. Removing it is a content change only; S13's rules do not change.
- The same silence applies to the book's player chapters (Valtay Corp), the Discord player channels and the vending wall (9.4).
- Nothing in the flow highlights, flags or reacts to the word "pet" in free text. The GM finds it by reading, at the GM review gate (§4.7).

### 9.2 GM-run action: file a pet
- A **GM-side command** (working name `pet add`; the Architect names it) stores the companion on the **owner's Crawler record/sheet**. Proposed fields on the owner: `pet: { name, species_srd_id, description, quote, filed_by, filed_on, status: alive|dead|became-crawler }`. `quote` is the player's own free-text words (trimmed), kept for audit.
- **Inputs:** owner (Crawler name), pet name, species (an SRD 5.2 Beast, chosen from a list of CR 1/4 or lower Beasts, e.g. `tables/pet-species.json`, a new file the Architect builds from the SRD Beast list), free-text description (max 300 chars).
- **Validation:** species must be on the CR <= 1/4 Beast list; one living pet per Crawler (refuse a second with a plain message); the owner must exist and be non-deleted. A species outside the list needs the GM's `--override "reason"` (edge cases are the GM's call; logged).
- **No separate channel, no slot, no credits, XP or loot rows, no ledger entries for the pet.** The owner's card shows a one-line `Pet:` entry once filed, and only on the owner's own sheet channel.
- **Other GM actions:** `pet mark-dead` (final; no revive path), `pet remove` (GM error correction; logged). Optional: `pet stow|release` (the kennel) as a marker.
- Benched Crawlers keep their pet record; the pet is inert with its owner (§8.2 item 4).

### 9.3 Biscuit conversion
- A GM-run action (working name `pet convert`) turns the owner's living pet into a **pet-Crawler**: create a Crawler record (`kind: pet-crawler`, owner set, no slot), its sheet channel **`<player>-<pet>-sheet`**, close the pet record (`status: became-crawler`), consume the Enhanced Pet Biscuit. **One conversion per living pet-Crawler**; refuse if one exists; a new conversion needs a new biscuit (§8.4 item 12, decision 021). The pet-Crawler stays benched on file if its owner is deleted (§8.5 item 9). Existing pet-Crawler rules (§8) are unchanged.

### 9.4 Pet items are off-menu
- Item ids `heal-critter-potion` ("Good Boy Gulp, Shaken Until Brown", 50 credits) and `pet-carrier` ("Fold-Flat Kennel With an Impossible Interior", 100 credits) are in `tables/item-reskins.json` v0.1.4 as `non_srd`. Prices are Floor-1 scale times the floor multiplier; buyback is half.
- They are listed **only on the card or channel of a Crawler who has a living plain pet on file**, never on the shared vending wall, never in a player chapter, never in an S10 gear list.
- **Credit prices:** the item lookup must show a credit price for `non_srd` items (the `base_price` fields are null for them; use `price_credits_proposed`, or its confirmed field).
- Purchase is refused for a Crawler with no living plain pet on file (the GM can override and logs why).

### 9.5 Feature switch
- One table setting (working name `pets.enabled`, default **true**) turns the feature off. When off: the pet-add and convert actions refuse with "pets are off", `pet:` lines are hidden, the two items are not listed anywhere, and nothing else changes. Existing pet records stay on file, inert. The Architect should keep every pet code path behind this one check.

### 9.6 Checklist (all unticked; see also the Acceptance checklist: pets at the end of this file)

---

*SRD attribution: this file references 5e rules by name and does not reproduce book text; see CORE Appendix D.*

---

## Verification log (2026-10-04, v0.1.1)

Source: SRD 5.2.1 (Wizards of the Coast, CC-BY-4.0), read from the official PDF. Rules paraphrased; nothing copied. Of 23 item-level VERIFY tags, 19 resolved and 4 remain.

**Confirmed, no change needed:** Hit Die for all 12 classes (d12 Barbarian; d10 Fighter, Paladin, Ranger; d8 Bard, Cleric, Druid, Monk, Rogue, Warlock; d6 Sorcerer, Wizard); class one-line descriptions; level 1 cantrip and prepared-spell counts (Bard 2/4, Cleric 3/4, Druid 2/4, Sorcerer 4/2, Warlock 2/2, Wizard 3/4 with 6 in the spellbook, Paladin and Ranger 0/2); Weapon Mastery classes (Barbarian, Fighter, Paladin, Ranger, Rogue); Rogue Expertise at level 1; Unarmored Defense for Barbarian and Monk; 27 points and 8-15 range for point buy; SRD has exactly four backgrounds; Wizard package A is 5 GP and every background offers a package or 50 GP; Dragonborn Darkvision 60 ft; sub-choice lists for Dragonborn, Elf, Gnome, Goliath, Tiefling, Human.

**Changed (old -> new):**
- Species table, Dwarf: "Stonecunning (stone lore)" -> Bonus Action Tremorsense 60 ft for 10 minutes, Proficiency Bonus uses per Long Rest; added Dwarven Toughness (+1 HP, +1 per level) and Darkvision 120 ft.
- Species table, Gnome: "Gnomish Cunning (better mental saves against magic)" -> Advantage on Int, Wis and Cha saves.
- Species table, Elf: added Keen Senses (one free skill: Insight, Perception or Survival); this is the Elf skill pick S9 asks about.
- Spells table, Sorcerer note: "known/prepared per book" -> "prepared" (SRD 5.2 Sorcerer prepares 2 at level 1). Warlock note: "slot count from table" -> "1 slot at level 1".
- VERIFY tags replaced with "SRD 5.2 checked" plus the numbers: point buy costs (8=0, 9=1, 10=2, 11=3, 12=4, 13=5, 14=7, 15=9); skill pick counts (Bard 3 any, Ranger 3, Rogue 4, others 2); Weapon Mastery counts (Barbarian 2, Fighter 3, Paladin 2, Ranger 2, Rogue 2); level 1 class choices (Fighting Style is Fighter only at level 1, Paladin and Ranger get it at level 2; Divine Order = Protector or Thaumaturge; Primal Order = Magician or Warden; Warlock picks 1 invocation); languages (Common plus two from the Standard Languages table); Origin feats in the SRD (Alert, Magic Initiate, Savage Attacker, Skilled only); level 1 slots (2 for the other casters, 1 for Warlock).

**Still unverified (VERIFY kept):**
- The 12 non-SRD PHB backgrounds (Artisan, Charlatan, Entertainer, Farmer, Guard, Guide, Hermit, Merchant, Noble, Sailor, Scribe, Wayfarer): not in SRD 5.2; from memory/PHB.
- Duplicate-skill replacement: SRD 5.2 has no swap rule (the 2014 SRD did); kept as a table/tool rule.
- Roll method (S8, v0.1.10): a house method, decision 024, not an SRD item (SRD 5.2 lists standard array and point buy; rolling is a 2024 PHB option).
- Horn's sheet fixture, Merchant bonus (§3.5 S8): a sheet check, not an SRD item; Merchant is not in the SRD.

**Affects other files:** Dwarf HP gets +1 at level 1 and +1 per level (S8 HP formula and test 2 in §6.2 need a Dwarf exception; GUIDE §3.3 and character-creation-5e.md should say so). Gnome save wording and Dwarf Stonecunning appear in GUIDE §7.2 if copied from here. Paladin and Ranger get no Fighting Style at level 1 (S6, S9 and the data table must not offer one). Line 6 and `flow_version` were brought to 0.1.2 in v0.1.2.

---

## Change log

- **v0.1.12 (2026-10-04, edited by the Architect from Syndicate's Roll audit notes N2 and the §3.6 wording):** §3.6 no longer says NEEDS BUILD or that `new-session.py` writes false (it is built and writes true; `--no-roll` writes false); the roll log is `sessions/rolls-*.log` for alpha and `sessions-data/<id>/rolls-*.log` for other sessions (S8 item 7, roll-log entries, checklist). No rule changed.
- **v0.1.11 (2026-10-04, Syndicate Roll audit):** ticked all 8 items of the Roll acceptance checklist after checking them against the built bridge code, `tables/create-flow-lines.json` and 358 Python plus 186 Node tests, driven in an isolated copy (never live state, ledger, bot or Discord); the nine `S8_roll_*` lines match §3.6 word for word; ~56% of arrays total 73+ in simulation (exact 56.23%). Noted, not changed: the bridge's new **Cancel build** button (decision 023) hard-deletes the draft including rolled rounds, so a cancelled build gets a fresh roll (deliberate, Caleb's request, the one exception to "no free rerolls"); §3.6 still says NEEDS BUILD although it is built. No screen, limit or data field changes.
- **v0.1.10 (2026-10-04, Caleb's request, decision 024):** S8 gains the third method **Roll** (three arrays of 4d6-drop-lowest, keep ONE array that totals 73+, no upper limit, System rerolls all three if none qualifies, every die logged by `roll.py`, assignment chooser, 20 cap restated); switch `create.allow_roll` now **default ON** (was off); new §3.6 lists what the Architect builds (switch, state fields, roll-log entries, the exact `create-flow-lines.json` lines); §4.1, Open Q1 (resolved), §6.1, glossary and Horn's fixture note updated; new unticked checklist below. Standard array and point buy unchanged. Correction filed: point buy can total up to 75, not always 72.
- **v0.1.9 (2026-10-04, Syndicate audit of the Architect's /create build):** ticked only the checklist items verified against code, data and the existing test suites run on an isolated copy (355 Python and 164 Node tests pass). Open items stay unticked with a short reason. Full evidence, blockers and nits: `tools-notes/create-audit-by-syndicate-20261004.md`. No screen, limit or data field changes.
- **v0.1.8 (2026-10-04, Caleb's ruling on pets):** new §9 (GM-filed pets: `/create` knows nothing about pets, no pet question in the questionnaire, GM-run pet-add and convert actions, off-menu pet items, one feature switch) and an unticked acceptance checklist for pets; `Depends on` gains rules/60 v0.1.0 and decision 022. No screen, limit or data field in S1-S17 changes. Finding: the S13 bonus pool has a `pets` question in `tables/create-flow-lines.json` that must go.
- **v0.1.7 (2026-10-04, Caleb's rulings):** (1) `/delete` is **log only, no flags or alerts**: wording changed in §8.2 item 10, §8.4 item 13 and §8.5 items 6 and 8 (decision 020 v1.2); (2) a Story Box still UNOPENED when its Crawler dies is reclaimed by the System and its slot is freed: §8.2 item 9, §8.4 item 11, §8.5 item 7 and the acceptance checklist (rules/45 v0.2.2); the ledger row for a reclaimed box is the Accountant's / Lore's; (3) a pet-Crawler stays on file, benched, when its owner Crawler is deleted, and is removed only by its own `/delete` (§8.5 item 9). Floor 1 Reprieve is ON for Floor 1 only (table setting, shown read-only on S1; core v0.2.10).
- **v0.1.6 (2026-10-04):** pet tombstone dropped (confirmed by Caleb): biscuit rule is one conversion per living pet-Crawler.
- **v0.1.5 (2026-10-04):** S10 item names now come from `tables/item-reskins.json` by `srd_id` (display `combined_label`, store the id, price by id, variant headers need a pick); chargen-5e.json v0.1.2 carries `srd_id`. The old 3-junk-names picker is retired.
- **v0.1.4 (2026-10-04):** new §8 "Multiple Crawlers per player and the active Crawler": any number of Crawlers, one active per player, benched Crawlers inert, **active Crawler changes only at session zero or between sessions, never while a session is open, not even in a safe room** (Caleb's session lock), mid-session death handling, Story Box and abuse rules, **sheet layout decided by Caleb: one text channel per Crawler `#<player>-<crawler>` under Crawler Sheets (no forums; 50-channel category limit)**, new **`/delete <name>`** command (§8.5; deleting frees the Crawler's Story Box slot, archive not destroy, pet tombstone), tool requirements marked NEEDS BUILD; matching edits in the header, S1 validation, S3, S17 step 6, §4.3, §4.4, §6.1, glossary (active Crawler, benched Crawler) and Open Q9 (resolved). Acceptance checklist and audit checklist for the create feature added at the end. Source: `decisions/020-multiple-crawlers-active-swap.md`.
- **v0.1.3 (2026-10-04):** refreshed the `Depends on` pointers only (core v0.2.8, species supplement v0.1.4, character-creation v0.2.1). No flow, screen or data change.
- **v0.1.2 (2026-10-04, Caleb's decision):** dropped the public Fan Profile tags screen. S12 is retired and intentionally skipped (numbers stay stable: 16 active screens, not 17). Removed `fan_profile.public_tags[]` and its NEEDS state.py bullet (old §3.3 bullets 3-9 are now 2-8, plus a new bullet 9 listing what to remove from existing tools); S13 survey answers are the private notes the System builds the hidden Fan Profile from; review screen, glossary (Fan Profile reworded, Fan tags removed, Private notes and Retired screen added), §4.6, §4.7, worked example, beta checklist and test script counts updated; open question 2 resolved; `flow_version` example is 0.1.2.

---

## Acceptance checklist: multiple Crawlers per player (v0.1.4)

Tick when built and tested. Ticked 2026-10-04 by the Syndicate audit only where verified (v0.1.9); the rest stay open with a reason.

- [x] A player creates three Crawlers from one Discord account; the first is active, the other two are benched; the party shows one slot for that player. (verified 2026-10-04)
- [x] The duplicate check allows a second Crawler for the same player with a different name, refuses an identical name for the same player, and refuses an identical name used by another player. (verified 2026-10-04)
- [ ] Every Crawler has its own text channel `#<player>-<crawler>` under Crawler Sheets (pet-Crawlers `#<player>-<pet>-sheet`), a player can open every one of their own sheets, and a new category opens before the 50-channel limit. _(2026-10-04: code and mock-Discord tests pass; live channel creation, the 50-channel overflow and `<player>-<pet>-sheet` UNVERIFIED without Discord)_
- [x] The sheet map in `state.json` is keyed by crawler id with an `owner` field. (verified 2026-10-04: key is the Crawler name, unique per session; new entries carry `owner`; the two alpha entries predate it and have none)
- [ ] `party --json` lists only active Crawlers; benched Crawlers get no credits, XP, loot, boxes, Story Boxes or ledger rows, and the cap and rota count the active Crawler only. _(2026-10-04: counts and guards PASS, but `party --json` also lists benched Crawlers, flagged `status: benched`, `counts_in_encounters: false`; reword or filter)_
- [x] A transfer of an item or credits between two Crawlers of the same player is refused. (verified 2026-10-04)
- [x] While a session is open, `/crawlers` and the GM swap command both refuse a swap and "make active now", including inside a safe room. (verified 2026-10-04, safe-room flag on or off)
- [x] Between sessions, the GM swap command works once per player per window, writes the swap log (who, from, to, floor, reason), and a refused swap writes the reason. (verified 2026-10-04)
- [ ] After a mid-session death, the player cannot swap until the next between-session window; the replacement comes from the player's benched Crawlers and is caught up to the party's lowest level at the next saferoom (CORE §2.3, §6.3). _(2026-10-04: the swap refusal PASSES; the catch-up to the party's lowest level at the next saferoom is a GM rule with no tool, UNVERIFIED)_
- [x] `/crawlers` lists the player's own Crawlers and sends a swap request to the GM without changing state. (verified 2026-10-04)
- [x] `/delete` refuses another player's Crawler, asks for the typed name, and cancels by default. (verified 2026-10-04)
- [x] `/delete` refuses the active Crawler while a session is open; a benched Crawler can be deleted; the active Crawler can be deleted between sessions and the player then names a new active Crawler. (verified 2026-10-04)
- [ ] After `/delete`, the sheet file, the card record and the text channel are gone, the ledger rows are in the archive, `ledger verify` passes, and the delete log has who, which Crawler, when and session state; nothing was refunded. _(2026-10-04: file move, ledger archive, verify, log PASS; live channel removal is mock-tested only)_
- [x] A Story Box held by a deleted Crawler no longer counts toward the one-per-floor cap; a dead Crawler that is not deleted still counts when it holds an opened or already-awarded Story Box item. (verified 2026-10-04)
- [x] A Story Box still unopened when its Crawler dies is reclaimed and no longer counts toward the cap or the one-per-living-Crawler count, so another Crawler can be awarded one; the reclaim ledger row is the Accountant's / Lore's. (verified 2026-10-04)
- [x] `/delete` writes the delete log only: no flag, alert or warning is raised. (verified 2026-10-04; the tool also prints the player's delete count to the GM, a nit)
- [ ] Biscuit: a second conversion is refused while the first pet-Crawler is alive; after that pet-Crawler is deleted a new conversion is allowed (with a new biscuit); deleting the owner's other Crawler does not delete the pet, which stays on file, benched, until its own `/delete`. _(2026-10-04: FAIL in part. After the pet-Crawler is deleted, `pet convert` refuses (no living plain pet) and `pet add` refuses (record stays `became-crawler`); only raw `create-crawler` can make the new pet-Crawler)_

---

## Acceptance checklist: pets (v0.1.8)

Ticked 2026-10-04 by the Syndicate audit only where verified (v0.1.9); the rest stay open with a reason.

- [ ] No player ever sees a pet prompt, field, checkbox, choice or hint in the questionnaire (S13/S14), in `/create` (S1-S17), in the book's player chapters or on the vending wall; a text search of the player-facing strings finds no pet offer. _(2026-10-04: FAIL. S11 Wizard menu shows Find Familiar "summon a spirit pet"; see the audit note)_
- [ ] The S13 bonus question `pets` ("Cats or dogs?") is removed from `tables/create-flow-lines.json` and from any test that names it. _(2026-10-04: PASS in the table and tests; FAIL in `characters/character-creation-5e.md:248`, which still lists "Cats or dogs?")_
- [x] A GM-run action files a pet on the owner's sheet only if the species is on the SRD Beast CR <= 1/4 list (an override needs a logged reason); a second living pet on one Crawler is refused. (verified 2026-10-04)
- [x] A filed pet has no slot, no channel, no credits, XP or loot rows and no ledger entries; it shows only as a one-line `Pet:` on the owner's own sheet. (verified 2026-10-04)
- [ ] The Biscuit conversion creates a pet-Crawler with sheet channel `<player>-<pet>-sheet`, closes the pet record, consumes the biscuit, is refused when a living pet-Crawler already exists, and the pet-Crawler stays benched on file when its owner is deleted. _(2026-10-04: same gap as the Biscuit item above; the rest PASSES)_
- [x] A dead pet cannot be revived by any revival command; the dead flag is final. (verified 2026-10-04; no revival command exists; raw `state.py set` can still flip the flag, a nit)
- [x] `heal-critter-potion` and `pet-carrier` are not on the shared vending wall or in any gear list, appear only on the card/channel of a Crawler with a living plain pet, and are refused for a Crawler without one. (verified 2026-10-04)
- [x] The item lookup shows credit prices (50 and 100) for these `non_srd` items; buyback is half. (verified 2026-10-04 via `pet shop`)
- [x] `pets.enabled = false` turns every pet path off (actions refuse, lines hidden, items not listed) with no other change. (verified 2026-10-04; the switch is `limits.pets_enabled`)

---

## Acceptance checklist: Roll method (v0.1.10)

Ticked 2026-10-04 (v0.1.11) by the Syndicate Roll audit, run on an isolated copy with no Discord; evidence in `tools-notes/create-audit-by-syndicate-20261004.md`, section "Roll method audit". Not exercised in live Discord.

- [x] Three arrays shown: pressing `[Roll]` at S8 shows three arrays (A, B, C) of six scores each, each score 4d6 drop lowest, with totals. (verified 2026-10-04, v0.1.11; real roll.py: 18 calls r1 A1..C6, draft dice = logged dice, scores = best three, totals summed by the bridge; `screens.js:147-172`, `flow.js:49-62`, `rules.js:79-95`)
- [x] Only arrays above 72 are keepable: an array totalling 72 or less cannot be kept (button disabled, reason shown); 73+ can; no upper limit on the total. (verified 2026-10-04, v0.1.11; a 72 array is disabled, 73 and a 108 array are keepable; `rules.js:76,89`, `screens.js:413,434`)
- [x] Reroll-all when none qualify: if none of the three totals above 72, all three are rolled again automatically, repeated until one qualifies; no voluntary reroll exists. (verified 2026-10-04, v0.1.11; 3 rounds = 54 calls; Roll pressed again makes 0 calls; 10 rounds = giveup line + `roll_giveup` log; `screens.js:157-168`)
- [x] Rolls logged: every die roll (all 18 per round, rerolled rounds too) has a `[ROLL]` line in `sessions/rolls-YYYY-MM-DD.log` (alpha; other sessions use `sessions-data/<id>/rolls-YYYY-MM-DD.log`) with the Crawler name and label. (verified 2026-10-04, v0.1.11; 18 lines per round, `[ROLL] S8 roll r1 A1 (Quill): 4d6dl1 -> ...`; alpha writes `sessions/rolls-*.log`, any other session `sessions-data/<id>/rolls-*.log`, `campaign_session.py:63`)
- [x] Assignment chooser: the player assigns each kept score to an ability of their choice, each score once; the preview adds the background +2/+1 or +1/+1/+1 after; no final score above 20. (verified 2026-10-04, v0.1.11; six selects, a used score is not offered again, equal scores kept separate; 18 + 2 = 20 is the most; backstop `rules.js:349`; `screens.js:137-145,442-453`)
- [x] Switch off hides it: `create.allow_roll = false` removes Roll from S8; standard array and point buy behave as before; default for a new session is true. (verified 2026-10-04, v0.1.11; button and text gone, a stale Roll press gets the closed line, a draft that already kept an array can still Confirm; new-session.py writes true, `new-session.py:63`; a missing value is ON, `settings.js:10`)
- [x] Back, Edit and Restart at S8 show the same saved rounds (no free rerolls); `build.score_rolls` keeps all rounds and the kept array. (verified 2026-10-04, v0.1.11; Back, S16 Edit, method change, Restart all 0 new calls; S17 recompute from the dice refuses a tampered die; `flow.js:70`, `commit.js:75`, `rules.js:98-123`; the one exception is the deliberate Cancel build, which hard-deletes the draft, `flow.js:310`)
- [x] Standard array, point buy and `[Pick for me]` are unchanged (existing tests still pass). (verified 2026-10-04, v0.1.11; Pick for me = standard array, point buy form works with Roll on and off; 358 Python and 186 Node tests pass in an isolated copy)

---

## Audit checklist for the create feature (full audit once all tasks are done, before the test; Caleb, 2026-10-04)

Ticked 2026-10-04 by the Syndicate audit only where verified (v0.1.9); the rest stay open with a reason.

- [x] Every screen is reachable: S1-S17 run in order with S12 skipped, Back, Edit, Restart and Resume work on each. (verified 2026-10-04)
- [x] S12 is retired: no prompt, no draft answer, no state field, no `public_tags`, no `Fan tags:` line, no `S12` entry in `tables/create-flow-lines.json`. (verified 2026-10-04)
- [x] Item names come from `tables/item-reskins.json` by `srd_id`, with a fallback to the plain 5e name when there is no entry; the 5e mechanics line is never blank (S10; file NEEDS BUILD if it does not exist yet). (verified 2026-10-04)
- [ ] The Crawler's sheet channel is filed under Crawler Sheets with the first card on Confirm (hold mode: only after approval). _(2026-10-04: code and mock-Discord tests pass; live Discord UNVERIFIED)_
- [x] Multi-Crawler: second and later Crawlers are benched, names pass the duplicate check as in §4.3, one active Crawler per player. (verified 2026-10-04)
- [x] Swap lock: no swap and no "make active now" while a session is open, even in a safe room; swaps between sessions are logged. (verified 2026-10-04)
- [x] `/delete`: own Crawlers only, typed-name confirm, active Crawler blocked while a session is open, archive, delete log, no pet tombstone (dropped). (verified 2026-10-04)
- [x] Ledger: `state.py ledger verify` exits 0 after create, swap and delete; archived rows reconcile with the Accountant. (verified 2026-10-04)
- [x] No file contains the word "champs" (the address rule in gm-notes/00-gm-principles.md is the only mention allowed); all text says Crawlers. (verified 2026-10-04 for all player-facing and rules text; meta lines such as the item-reskins `tone` note still say "never 'champ'")
- [x] Slots and party counts: the 4 slots, `party --json`, encounter budgets and the Story Box cap count active, non-deleted Crawlers only; pet-Crawlers take no slot. (verified 2026-10-04)
- [ ] Pets: nothing in `/create`, the questionnaire, the player chapters or the vending wall mentions, asks about or offers a pet (§9.1). _(2026-10-04: FAIL, same Find Familiar line)_
