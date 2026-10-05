# Core Rules v0.1 (superseded)
Owner: Syndicate | Status: final (retired) | Version: 0.1 | Updated: 2026-10-03
Summary: RETIRED. v0.1 custom-chassis core rules, superseded by rules/10-core-rules-5e.md; kept for history only.
Source: crawler-protocol/02-core-rules.md (original kept; internal cross-references use the source file names, see rules/INDEX.md path map)

> **⚠ SUPERSEDED (2026-10-03):** Replaced by [`02-core-rules-5e.md`](02-core-rules-5e.md), the D&D 5e 2024 overlay (v0.2). Kept for reference only. Do **not** adjudicate from this file.

# 02 — Core Rules v0.1

> **Status:** Playable draft — aligns with Game Brief, Campaign Narrative (Kingdom Continuum), and Achievements catalog  
> **Project:** Crawler Protocol / Syndicate Dungeon Crawl System  
> **Audience:** AI Showrunner (DM) + players typing moves in chat  
> **Scope:** Enough to run Floor 1 now and scale through Floor 18. Floor docs may add **special floor rules** that override this file while that floor is active.

---

## 0. What these rules are for

Friends play **Crawlers**. An AI runs the dungeon as **Showrunner / DM**.  
Dice settle uncertainty. Fiction + floor docs settle everything else.

**Source of truth order (highest wins):**

1. Active floor’s special rules (while on that floor)  
2. This Core Rules doc  
3. Character sheet / session state  
4. Achievement rewards already granted  
5. AI temporary ruling (must be logged)

---

## 1. The Crawl at a glance

| Piece | Rule |
|-------|------|
| Goal per floor | Meet the floor objective (usually reach stairwell/gate) while surviving |
| Campaign | Floors 1 → 18 |
| Party | 2–6 crawlers |
| Death | Permanent by default (see §8) |
| Tone | Dark comedy, high stakes, System pop-ups OK in moderation |

**Floor environment law (from spine):**

- **Floor 1** = tutorial trainer  
- **Floor 2** = unique  
- **Floors 3, 6, 9, 12** = **Kingdom Continuum** (one civilization: rural → docks → castle → Olympus)  
- **All other floors** = unique environments  

The AI must open Continuum returns with **recognition** of prior visits before new pressure.

---

## 2. Dice & checks

### 2.1 The roll

When outcome is uncertain or contested:

```text
1d20 + Stat (+ situational bonus)  vs  DC
```

or **opposed:** both sides roll; higher wins (tie = defender / status quo).

**Public rolls.** Players (or the future roller UI) roll where everyone can see.

### 2.2 Stats (five)

| Stat | Use for |
|------|---------|
| **Strike** | Attacks, athletic force, breaking things |
| **Grit** | Endure pain, poison, fear, forced marches, death saves |
| **Wits** | Notice, puzzle, recall, System glitches, weird geometry |
| **Sneak** | Hide, steal, disable traps quietly, ambush setup |
| **Presence** | Talk, intimidate, perform, sponsor/court/divine manners |

### 2.3 Difficulty (DC)

| DC | Meaning | Examples |
|---:|---------|----------|
| 8 | Easy | Quiet room search, weak lock |
| 12 | Standard | Normal fight attack vs light armor, haggle, climb |
| 16 | Hard | Elite defense, court etiquette, Knotline geometry |
| 20 | Severe | Boss phase, divine test, broadcast hack under fire |
| 24 | Extreme | Near-impossible without setup / items / help |

AI states the **stat + DC** before the roll when possible.

### 2.4 Advantage / disadvantage

- **Advantage:** roll 2d20, take higher (setup, aid, superior gear, ratings spike)  
- **Disadvantage:** roll 2d20, take lower (wounds, bad footing, sponsor rider, divine scorn)

Do not stack multiple advantages; one is enough. Same for disadvantage. If both apply, they cancel.

### 2.5 Criticals (simple)

- **Natural 20:** success with style — extra damage die **or** a fiction bonus (AI picks one).  
- **Natural 1:** failure with bite — complication, noise, drop item, or +1 threat (AI picks one).  

No instant death on a nat 1 unless the player already accepted deadly stakes.

### 2.6 Helping

An ally in position may **Help**: if they describe how, the acting crawler gets Advantage on one check this turn. One Help per check.

---

## 3. Character numbers (v0.1)

Full chargen lives in `03-character-creation.md`. Until that expands, use this chassis:

### 3.1 Starting array

Assign to the five stats: **+3, +2, +1, +0, −1** (each used once).  
Floor 1 may ignore race/class; Continuum Floor 3 unlocks identity menus.

### 3.2 Derived

| Value | Formula |
|-------|---------|
| **HP** | `10 + Grit + Floor Clear bonuses` (min 6) |
| **Armor** | 0–3 from gear (reduces damage; see §6) |
| **Speed** | 1 Move per turn (see §5); some items grant Extra Move |
| **Inventory** | 10 slots (bulky = 2; tiny junk can stack 5 per slot) |
| **Credits** | System currency; start with **50** on Floor 1 |

### 3.3 Level / power bumps

There is no traditional XP bar.

**You get stronger by:**

1. **Floor Clear** — on first clear of a floor: +1 HP permanent, and choose **+1 to one stat** (max +5) **or** a class/race perk unlock if available  
2. **Achievements** — see §10  
3. **Gear / sponsorship / vows** — temporary or permanent riders logged in session state  

---

## 4. Conditions

Track on the sheet. Common conditions:

| Condition | Effect |
|-----------|--------|
| **Bloodied** | At or below half HP — fiction only unless a floor rule cares |
| **Downed** | 0 HP — see §8 |
| **Poisoned** | Disadvantage on Grit; 1 damage at start of your turn until cured |
| **Afraid** | Disadvantage on Presence; cannot willingly move closer to the source |
| **Hidden** | Enemies don’t target you until you attack, fail Sneak, or are revealed |
| **Restrained** | No Move; Disadvantage on Strike |
| **Sponsored** | Must obey one logged rider; break it → penalty flagged by AI |
| **Vow-bound** | Divine/infernal promise; break → curse or call-in on later floor |

---

## 5. Time, turns, and initiative

### 5.1 Exploration mode (default)

Free conversation order. AI asks for rolls when needed. Fog of war: only describe revealed cells.

### 5.2 Combat / timed mode

When blades are out or a timer starts:

1. Everyone rolls **Wits** (or Strike if they choose aggression) for initiative — higher goes first.  
2. On your turn you get: **Move** + **1 Act** (in either order).  
3. **Move:** one zone/room edge, or within a large room to cover/ally/enemy in reach.  
4. **Act:** Attack, Skill, Item, Talk (short), Help, or Stabilize.  
5. Enemies act on their initiatives as groups when possible (keep pace).

**Interrupt:** if fiction demands (trap spring, chase), AI may call a single contested roll outside turn order, then resume.

---

## 6. Combat

### 6.1 Attack

```text
Strike check vs DC (or opposed Strike/Sneak if ambush)
```

Typical DCs: mook 10–12, soldier 14, elite 16, boss 18–20 (phase-dependent).

**Hit:** deal weapon damage (see §6.2). Subtract target **Armor** (min 0 damage only if Armor ≥ damage and fiction says glance — otherwise min 1 on a clear hit unless Armor explicitly nullifies).

**Simple Armor rule:** reduce damage by Armor value (minimum **0**). Armor does not stop environmental damage unless noted.

### 6.2 Weapon damage (v0.1)

| Tag | Damage |
|-----|--------|
| Unarmed / desperate | 1d4 |
| Junk melee (crowbar, pipe) | 1d6 |
| Proper melee / sidearm | 1d8 |
| Heavy / two-hand | 1d10 |
| Named / boss drop | 1d12 (or weapon card) |

Add **half Strike** (round down) to damage on a hit.  
Nat 20: add one extra weapon die.

### 6.3 Range & zones

Don’t measure feet. Use **zones**: adjacent / near / far.  
Ranged needs line of sight; Disadvantage at far unless scoped.

### 6.4 Cover

Half cover: +2 to the DC to hit you (or Advantage on your defensive opposed roll).  
Full cover: can’t be targeted until exposed.

---

## 7. Exploration, traps, saferooms

### 7.1 Search / notice

Wits (or Sneak if careful probing). Failure = missed info **or** triggered complication (never pure blank).

### 7.2 Traps

Usually Sneak to disable, Wits to spot, Grit if you tank it.  
Damage: 1d6 (minor), 1d10 (serious), 2d8 (deadly — telegraph this).

### 7.3 Saferooms

- Resting in a **true saferoom**: clear Poisoned/Afraid; recover **HP equal to 1d6 + Grit** (once per floor unless floor rules say otherwise).  
- **Saferooms can lie.** Floor 2+ may hide teeth — searching is allowed and sometimes wise (Achievement: Saferoom Skeptic).  
- Continuum rural saferooms are usually honest; dock/castle/olympus “safe” spaces may be political.

### 7.4 Fog of war

Unrevealed map is unknown. Players don’t meta-call rooms they haven’t entered. AI tracks revealed cells in session state.

---

## 8. Downed, death, and replacements

1. At **0 HP**, you are **Downed** (unconscious / bleeding out — fiction).  
2. On your turn while Downed, roll **Grit DC 12** (death save):  
   - Success: stay Downed; 3 successes before 3 fails → stabilize at 1 HP  
   - Fail: mark a fail; 3 fails → **Dead**  
3. An ally may spend an Act to **Stabilize** (DC 10 Wits or item) → 1 HP, prone.  
4. Coup de grace on a Downed crawler: only if enemy is free and ruthless — AI telegraphs.  
5. **Dead = permanent** unless a floor rule, Named item, Continuum vow, or achievement reward says otherwise.  
6. New player / replacement crawler may join next session with story justification (intake glitch, sponsored entrant, Continuum recruit).

Floor 1 teaches this carefully — deadly, but the tutorial should not feel like a grief trap on turn one.

---

## 9. Loot, vendors, inventory

### 9.1 Rarity

**Common / Rare / Named.** Named items have a card (benefit + quirk).

### 9.2 Slots

10 slots. Bulky = 2. Stack tiny junk ×5. Credits don’t take slots.

### 9.3 Vendors

Presence to haggle (DC 12 typical; success ≈ 10–25% off). Continuum vendors remember you.

### 9.4 Identification

Junk is obvious. Rare/Named may need Wits DC 12 or a vendor/appraiser (dock tier loves this).

---

## 10. Achievements (rules link)

Catalog: `reference/achievements.xlsx` (1,800+ draft entries).

### 10.1 Earning

When criteria are met, AI announces in **System voice** and logs the ID on the sheet / session state.  
No retroactive farming without table OK.

### 10.2 Rewards

| Has Reward | Effect |
|------------|--------|
| **Yes** | Grant the listed reward (credits, title, loot roll, flag, cosmetic). If vague (“Rare loot roll”), roll on the active floor’s loot table or give a Rare tag item. |
| **No** | Title / brag only — still log it |

**Loot rolls (default):**

- Common reward table: 25–50 credits or junk upgrade  
- Rare: choose one — Rare item stub / +1 weapon die once / useful tool  
- Legendary: Named stub or permanent +1 HP or one-time Advantage token  

### 10.3 Canon Flavor tag

Flavor only for writers — **no extra mechanical weight** unless the Reward column says so.

### 10.4 Stacking

Duplicate achievement IDs don’t re-grant. Same *kind* of template on different floors can both grant if IDs differ.

---

## 11. Ratings, sponsors, vows (light systems)

These support the spine without a second ruleset.

### 11.1 Broadcast Name

Unlocked around Continuum Floor 3. It’s a social tag: Advantage on Presence once per session when you lean on fame — or Disadvantage when fame paints a target (hunters, court, gods).

### 11.2 Sponsors (esp. Floor 6+)

Deals grant currency/gear + a **rider** (must do X, cannot do Y). Break rider → lose benefit + possible hunter attention.

### 11.3 Mandates / Faction Flags (Floor 9+)

Accepting a mandate is a quest with teeth. Public refusal is allowed and may unlock alternate paths.

### 11.4 Throne Vow / divine & infernal pacts (12 / 15)

Logged as Vow-bound. Payoffs and invoices fire on later floors per narrative spine. Refusing is always a legal player choice.

### 11.5 Spine objects

Odd Coin, Benefactor Signal, Black Box, Faction Flag, etc. are **inventory/story flags**. They don’t need stats until a floor doc says how they unlock a door, bid, or ending.

---

## 12. Magic, races, classes (v0.1 bridge)

Until chargen is full:

- **Race/class** unlock starting Continuum Floor 3 (rural identity market). Before that: human(ish) crawler + junk kit.  
- **Abilities:** each class/race grants **2 tagged actions** (e.g. “once per fight: Advantage on Sneak”; “1d8 heal touch once per rest”).  
- No Vancian spell slots in v0.1 — powers are per-fight / per-rest / per-floor as written on the card.  
- Floor rules may grant temporary powers (echo cards, biome kits, stagehand tools).

---

## 13. PvP and table safety

- **PvP off by default.** On only with unanimous table consent for that scene.  
- **Lines:** PG-13 to R by agreement. AI fades to black on request.  
- Disputes: cite this doc → floor doc → temporary ruling logged.

---

## 14. AI Showrunner procedure (rules-facing)

1. State floor, objective, special rules.  
2. Describe only what is visible.  
3. Call **stat + DC** before rolls.  
4. On failure, advance fiction.  
5. Award achievements when earned; don’t spoil Continuum payoffs early.  
6. End session with state update: HP, inventory, seeds, next hook.

Players type moves like:  
`I move to the door and listen.` / `I attack with crowbar.` / `I show the Odd Coin to the elder.`

---

## 15. Floor 1 quickstart (rules subset)

Teach with few specials:

- Stats + d20 vs DC  
- Move + Act in fights  
- Junk damage 1d6  
- Downed / stabilize  
- Loot credits + Odd Coin + Benefactor static plant  
- Saferoom rest once  
- Stairwell = clear  

No race/class menu yet. Keep DCs around 10–14.

---

## 16. Changelog

| Version | Notes |
|---------|-------|
| v0.1 | First full chassis from Game Brief + Narrative spine + Achievements sheet |

---

## 17. Open for owner markup

- Stat names OK, or rename?  
- HP curve too swingy / too tanky?  
- Achievement rewards: keep generic tables, or write per-ID rewards for flagship achievements only?  
- Want stricter D&D 5e-like actions (Action/Bonus/Reaction) instead of Move+Act?
