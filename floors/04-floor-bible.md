# 04 — Floor Bible (Floors 1–18, Continuum)
Owner: Syndicate | Status: draft | Version: 0.4.1 | Updated: 2026-10-05
Summary: Continuum rewrite of the floor bible: overall Season Zero arc, Kingdom Continuum ladder (F3/6/9/12), unique floors elsewhere, seeds, unlocks and AI-DM notes for Floors 1–18. Aligns with locked rulings (collapse death, F3 = 20 days, Story Boxes F1–2, Platinum F9+, species Offer decision 009, F7–18 clocks 30 PLACEHOLDER, 5e 2024).
Depends on: floors/00-campaign-narrative.md v0.3 (spine; wins on Continuum structure), rules/10-core-rules-5e.md v0.2.17 (5e overlay, §4.5 pacing, §5.10 credits, §6 death), decisions/009-species-approach.md, decisions/026-timed-floor-clock-override.md, decisions/028-collapse-death-loot.md, decisions/027-encounter-budget-v0-1-0.md, decisions/015/018-story-boxes, rules/30-species-supplement-5e.md, rules/45-story-boxes-5e.md v0.2.4, rules/70-encounter-budget-5e.json (clock.days, budgets), Lore draft `dcc-lore/drafts/floor-bible-v0.4-canon-check.md`. Consumers: AI GM, Encounter Bot, Lore, Book Author, Caleb.
Source: Continuum rewrite of crawler-protocol/04-floor-bible.md (pre-Continuum backup: floors/_archive/04-floor-bible.pre-continuum.md).

> **Status:** DRAFT v0.4.1 for Caleb's input (v0.4 + Lore canon-check / room consensus patches). Nothing here is LOCKED except what the spine and locked decisions already say.
> **Project:** *Crawler Protocol: Season Zero* — original fan RPG inspired by *Dungeon Crawler Carl*. Private play only.
> **Rule:** Canon vibes inform shape. Rooms, NPCs, quests, dialogue and plot beats here are **original**. Never paste novel prose. Flavor lines stay **3–4 sentences max** per labeled block.
> **Address:** players are always **Crawlers**. Spelling: **saferoom**.

---

## 1. Purpose (AI DM)

This Bible turns the Continuum spine into something you can run. Use it to feel each floor, plant seeds early, fire payoffs late, and keep Floor docs honest to the ladder.

1. Read §2 (overall narrative) and §3 (locked rulings) before writing any `floors/fNN/` page.
2. Plant seeds with IDs (`SEED-…`). Log `PLANTED | floor | what they saw`. Mark `FIRED → Floor N` when it pays; never delete the row.
3. Achievements are a **seed list** (`tables/achievements.*` v1.3.1+), not a schedule. The System decides what is notable; snark-only is allowed (core §3.5).
4. Where this file and `floors/00-campaign-narrative.md` disagree on Continuum structure, the narrative wins until Caleb marks this up. Where this file and core/decisions disagree on rules, **core and decisions win**.

### Escalation arc

| Arc | Floors | Focus |
|-----|--------|--------|
| Tutorial | 1–2 | Teach System, death is real, party bonds; leave the trainer |
| Continuum begins | 3 | Meet people; rural Kingdom; identity starts |
| Away, then docks | 4–6 | Alien stages, then the same civilization's edge; hunters |
| Pressure, then castle | 7–9 | Unique pressure cookers, then upper city and castle politics |
| Spectacle, then Olympus | 10–12 | Heats and jubilee feed myth; last Continuum visit is divine |
| Strip the lie | 13–17 | Ledgers, auctions, ash, mirrors, rigging |
| Cage | 18 | Endings; spine payoffs |

---

## 2. Overall narrative (Floors 1–18)

**Working title:** *Crawler Protocol: Season Zero*.

You are **content** inside a broadcast murder-game. The System is camera, rulebook and dealer. Survival is ratings; ratings are power; power is escape, or burning the show down.

**Central question:** play for prizes and patronage, or learn who owns the Crawl and break the cage from inside?

**Tone:** dark comedy, high stakes, System pop-ups, sponsor slime. Crawler loyalty is the rare honest thing.

**Through-line (read once):**

1. **F1** — Orientation Pit. Learn UI, death, loot, stairs. Plant Odd Coin and Benefactor static. Miss the collapse and you die.
2. **F2** — Unique Soft Open. First real elsewhere. No Continuum landmarks. Prove the Crawl has stages beyond the trainer.
3. **F3** — Kingdom Continuum, rural. Villages, civilians, Floor 3 species Offer (decision 009). Broadcast Name begins as gossip. Clock: **20 days**.
4. **F4–F5** — Unique Knotline and Bubble Farms. Leave the kingdom for alien stages; return later changed.
5. **F6** — Continuum outskirts and docks. Same civilization's edge. Hunters land; sponsors shop. Village debts come due.
6. **F7–F8** — Unique Greenlight Gauntlet and Remnant Parade. Pressure away from "home."
7. **F9** — Continuum upper city and castle. Mandates, factions, politics. **Platinum boxes unlock** (core §4.5). Broadcast Name becomes a political object.
8. **F10–F11** — Unique Last Heat Standing and Ratings Jubilee. Spectacle that feeds the kingdom's next myth (but not Continuum maps).
9. **F12** — Continuum Olympus / spirit. Same world's god-tier. Throne Vow; Benefactor meets pantheon. Last Continuum visit.
10. **F13–F17** — Unique Ledger Depths, Continuity Auction, Ash Choir, Fracture Gallery, Rigging Catwalk. Strip the lie behind the world.
11. **F18** — Cage Bottom. Endings. All spine payoffs. Not another Continuum visit unless an ending reprises it on purpose.

**Kingdom Continuum (F3 → F6 → F9 → F12):** one civilization, climbing: rural villages → docks/outskirts → upper city/castle → deity/Olympus. Not four disconnected maps. Landmark bones, NPCs and scars persist and escalate (`floors/00-campaign-narrative.md`).

---

## 3. Locked rulings this bible obeys

| Topic | Ruling | Source |
|-------|--------|--------|
| Base game | D&D 5e 2024 (SRD 5.2) + homebrew overlay | core rules/10 |
| Missed collapse | Death on **every** floor; all Crawlers on the floor die; AI/NPCs stasis (house); credits/items destroyed with the floor unless looted while it stands. **Floor 1 Reprieve is ON** (tutorial deaths only) and **never** covers a missed collapse | decisions 026, 028, 029; core §6.2 |
| Floor clocks | F1 = 5, F2 = 10, F3 = **20**, F4 = 20, F5 = 25, F6 = 30; **F7–F18 = 30 days each (PLACEHOLDER)** per decision 027 / rules/70 growth curve (not longer than F6) | decisions 026, 027; Q-001; rules/70 |
| Story Boxes | Legendary Story Boxes allowed on **F1–2**, outside the §4.5 Legendary pacing table and outside the Legendary cap of 2; one per table per floor; GM may exceed with a logged reason (Caleb can veto); unopened box bound, item inside tradeable/lootable/sellable | decisions 015, 018 v1.1; rules/45; core §4 |
| Box ceilings | **Silver** F1–2 (Story Box exception still applies); **Gold** F3–8; **Platinum** F9+; Legendary cap 2 per Crawler (Story Boxes outside that cap) | core §4.5 / v0.2.17 |
| Legendary boxes | Cap of **2 per Crawler** (core §4.5); Story Boxes do not count | core §4.5; catalog ACH-1824 note |
| Species / class unlock timing | **Decision 009 (locked):** nine 2024 SRD species at level 1 (look human on F1–2; traits as quirks). Floor 3 System Offer: starting species + two DCC-style oddities (~12 in `rules/30`; **do not invent the oddity names here**); free rebuild optional. Class-swap timing stays out of this bible | decision 009; rules/30 |
| Address / spelling | **Crawlers**; **saferoom** | gm-notes/00; Caleb 2026-10-04 |

---

## 4. Structure rules (from the spine)

| Floors | Environment |
|--------|-------------|
| **1** | Trainer / tutorial only |
| **2** | Unique |
| **3, 6, 9, 12** | **Kingdom Continuum** — one recurring civilization, escalating |
| **4, 5, 7, 8, 10, 11, 13–18** | Each **unique** |

---

## 5. Master table

| Floor | Title (working) | Kind | Theme (1 line) | Clock (days) | Key unlocks / notes |
|------:|-----------------|------|----------------|:------------:|---------------------|
| 1 | The Orientation Pit | Tutorial | Brutal trainer that teaches the System | 5 | UI, death, loot, stairs; Story Box eligible |
| 2 | Soft Open | Unique | First real elsewhere; districts with teeth | 10 | Companions tease; saferooms; Story Box eligible |
| 3 | Kingdom Continuum — Rural | Continuum | Villages, civilians, gossip becoming fame | **20** | Social play; Broadcast Name begins; identity **tease only** |
| 4 | The Knotline | Unique | Non-Euclidean transit puzzle | 20 | Transit keys; relays; Guide Contract bites |
| 5 | Bubble Farms | Unique | Pocket biomes; cooperation under collapse risk | 25 | Biome kits; Bubble Core; Static Sigil payoff |
| 6 | Kingdom Continuum — Docks | Continuum | Same world at the edge; hunters and sponsors | 30 | Hunter Badge; Benefactor hardens; rural debts due |
| 7 | Greenlight Gauntlet | Unique | Timed race / maze | 30 (PLACEHOLDER) | Shortcuts; speed builds |
| 8 | Remnant Parade | Unique | Memory-echo combat; identity as a weapon | 30 (PLACEHOLDER) | Echo cards; Echo Self seed |
| 9 | Kingdom Continuum — Castle | Continuum | Upper city and castle politics | 30 (PLACEHOLDER) | Faction Flag; **Platinum from here**; Broadcast Name political |
| 10 | Last Heat Standing | Unique | Elimination vehicle heats | 30 (PLACEHOLDER) | Garages; **Black Box** plant |
| 11 | Ratings Jubilee | Unique | Spectacle parade/arena (not Continuum grid) | 30 (PLACEHOLDER) | Named opponents; VIP tickets |
| 12 | Kingdom Continuum — Olympus | Continuum | Same world's god-tier | 30 (PLACEHOLDER) | Throne Vow; deity patronage; last Continuum visit |
| 13 | Ledger Depths | Unique | Corporate / System truth in debt vaults | 30 (PLACEHOLDER) | Audit tools; Ledger Name |
| 14 | Continuity Auction | Unique | Reality lots sold to bidders | 30 (PLACEHOLDER) | Black Box evidence; rewrite tokens |
| 15 | Ash Choir | Unique | Infernal layer; damned contracts | 30 (PLACEHOLDER) | Vow payoffs; anti-holy kits. Title PLACEHOLDER / Continuum-adjacent pending Caleb |
| 16 | Fracture Gallery | Unique | Mirrors that split or sell identity | 30 (PLACEHOLDER) | Mirror duels; identity locks |
| 17 | Rigging Catwalk | Unique | Flyrail under the broadcast grid (*inspired*; original title) | 30 (PLACEHOLDER) | Broadcast hacks; Black Box air |
| 18 | The Cage Bottom | Unique endgame | Final politics; ratings vs freedom | 30 (PLACEHOLDER) | Endings; all spine payoffs. Title PLACEHOLDER / Continuum-adjacent pending Caleb |

Floors **12–18** playable content beyond sparse public canon are marked **[ORIGINAL]** in their sections. Early floors use public *vibes* only.

---

## 6. Kingdom Continuum ladder (detail)

**Working name:** The Kingdom Continuum (also fine: Settled Lands, Crownwake — rename anytime).

One continuous civilization. Geography, culture, NPCs and rumors **persist and escalate**. Each return is higher on the same social and spiritual ladder.

| Floor | Tier | Place | Story job |
|------:|------|-------|-----------|
| **3** | Rural | Villages & settlements | People, markets, elders, militia, farmstead saferooms, small temples. Social play. Broadcast Name as gossip → System fame. |
| **6** | Outskirts | Edge, docks, trade roads | Ports, warehouses, customs, sponsor skyboxes. Hunters land. Benefactor choice hardens. |
| **9** | Urban power | Upper city & castle | Noble quarters, courts, barracks, the castle. Mandates, factions, diplomacy/sabotage. |
| **12** | Divine | Olympus / spirit | Mythic heights above the castle. Pantheon courts, vow-fire, deity patronage. Continuation of rural→dock→castle, not a random heaven. |

**Continuity rules (AI DM):**

- Reuse **landmark bones** that scale: F3 Wellspring / Millroad / Low Chapel → F6 names on manifests and pier shrines → F9 cousin fountain and bishop at court → F12 the Chapel's god is present; Millroad is a constellation or sacred path.
- NPCs migrate up (villager → dock broker → courtier → demigod attendant) or die and get "recast."
- Scars carry: a dock fire on F6 is a mural on F9; a castle vow becomes Olympus law on F12.
- Open each return with **recognition**, then the new tier's pressure.
- This is **one kingdom** (and then its heaven), not four separate cities.

---

## 7. Per-floor sections (1–18)

---

### Floor 1 — The Orientation Pit *(tutorial)*

**Pitch:** A meat-grinder trainer that teaches the System while pretending to be fair.

**Theme / vibe:** Concrete corridors, vending gore, cheerful UI over corpses. Dark comedy; keep special rules few. The module lives in `floors/f01/`.

**Clock / collapse:** 5 days. **Collapse at floor-hour 120** (decision 026; flat). Keep a running floor-hour count in the carry-on tracker. **Miss it and you die** — Floor 1 included. The Floor 1 Reprieve never covers a missed collapse. Stairwells open ~32 h in; early descent is stasis until collapse (still counts as reaching a stairwell).

**Special floor rules**
- Few overrides; teach 5e death saves, System Inventory, boxes open only in a saferoom.
- Floor 1 Reprieve ON for this campaign (tutorial mercy, once per Crawler, Floor 1 only) — **does not** cover a missed collapse.
- No System species Offer here. Level 1 chargen is one of the nine 2024 SRD species (look human on F1–2; decision 009). The Floor 3 Offer is where oddities appear.
- **Story Boxes:** Legendary Story Boxes allowed (one per table per floor; GM override with logged reason). Outside Legendary pacing/cap.

**Unlocks:** System voice, achievements toasts, Bronze/Silver pacing, corpse cache, saferoom rest.

**Seeds to PLANT**

| ID | What Crawlers see | Payoff |
|----|-------------------|--------|
| `SEED-ODDCOIN` | Dull stamped coin; System: *Vendor Oddity (Unappraised)*. | F3 curiosity → F6 appraiser → F9 court → F12 divine token |
| `SEED-BENEFACTOR` | Garbled private static: `…HOLD… NOT YET…` and a broken crest. | F3 omen → F6 choice → F9 rumor → F12 seat → F18 allegiance |

**Payoffs that FIRE:** none (campaign start).

**Achievement hooks (guidelines):** first kill; first stairwell; first death save; witness a permanent death; pick up the Odd Coin (hidden toast). Catalog seed list applies; snark-only fine. ACH-1825 (stairs found) / ACH-1824 (too-fast descent) / ACH-1826 (early bird stasis) as applicable.

**AI DM notes:** Teach UI literacy, healing scarcity, that the show is watching. Warn clearly about collapse on Day 1, Day 4 and Day 5. Do **not** explain Benefactor or coin. Do **not** preview Continuum villages, hunters or gods.

---

### Floor 2 — Soft Open *(unique)*

**Pitch:** The Crawl stops holding your hand. Districts, dens and saferooms with teeth.

**Theme / vibe:** Rec-room aesthetics over killboxes; first recurring NPCs; traps that teach attention. **No Kingdom Continuum landmarks.**

**Clock / collapse:** 10 days. Missed collapse = death.

**Special floor rules**
- Saferooms exist; may charge a toll (credits, time or item — price from rules/70 when set).
- Trap density up; failed Perception can pull noise/mobs.
- Companion / pet slots per rules/60 and decision 022 (GM-run; never offered in `/create`).
- Story Boxes still allowed (F1–2 exception).

**Unlocks:** Named district vendors (limited stock); basic crafting tease (tables still gated per rules/20: unusable until F4 unless carried as tokens).

**Seeds to PLANT**

| ID | What Crawlers see | Payoff |
|----|-------------------|--------|
| `SEED-STATICSIGIL` | Chalky static mark behind a vendor; flickers when touched. | F5 bubble gate |
| `SEED-GUIDECONTRACT` | Cheerful guide offers a "free route map" with unread fine print. | F4 clause bites; F9 debt call |

**Payoffs:** optional Benefactor static echo if they chase radios.

**Achievement hooks:** clear Soft Open; pay a saferoom toll; read the guide's fine print; disarm or kite traps; spare a mini-boss.

**AI DM notes:** Information has a price; NPCs have agendas. Do **not** resolve the guide's employer. Do **not** open Continuum geography.

---

### Floor 3 — Kingdom Continuum *(Rural)*

**Pitch:** The first returnable world: dirt roads, harvest markets and people who will remember your face.

**Theme / vibe:** Villages, hamlets, settlement walls, Low Chapel bells, Millroad dust. Civilians matter. The System still broadcasts every kindness and every atrocity.

**Clock / collapse:** **20 days** (Caleb). Missed collapse = death.

**Special floor rules**
- Continuum visit 1 of 4. Plant Wellspring / Millroad / Low Chapel bones.
- Social play unlocked: favors, debts, local law, militia call-ups.
- **Identity (decision 009):** Floor 3 System Offer — starting species + two DCC-style oddities from the ~12 in `rules/30` (names live there; **do not invent them here**); free rebuild optional. Village gossip and shrines can flavor the Offer; they do not replace it.
- Boxes: **Gold** ceiling for F3–8 (core §4.5); still no Platinum until F9.

**Unlocks:** Broadcast Name (local gossip → System fame); Continuum NPC ledger (faces to reuse); farmstead saferooms.

**Seeds to PLANT / touch**

| ID | Action |
|----|--------|
| `SEED-ODDCOIN` | Village curiosity / hedge appraiser shrugs. |
| `SEED-BENEFACTOR` | Folk omen; crest misread as a harvest saint. |
| `SEED-BROADCASTNAME` | **Plant.** First public nickname that sticks. |

**Carry forward:** faces, favors, debts, one village that must be remembered at the docks.

**Achievement hooks:** save a settlement without becoming its warlord; tell the truth when a lie was safer; earn a Broadcast Name the village repeats; refuse a cruel System stunt on camera.

**AI DM notes:** Open with recognition of *being somewhere real*. Let them love a place they will later see broken or elevated. No hunters yet. No castle politics.

---

### Floor 4 — The Knotline *(unique)*

**Pitch:** Non-Euclidean transit: keys, relays and trains that should not share a timetable.

**Theme / vibe:** Switching yards folded through themselves; schedules that lie; Infrastructure is the dungeon.

**Clock / collapse:** 20 days. Missed collapse = death.

**Special floor rules:** Transit keys and team relays. Sabotage is loud and ratings-friendly. Guide Contract fine print can bite here.

**Unlocks:** Transit key tags; relay roles; infrastructure sabotage tools (consumable / one-floor).

**Seeds:** fire `SEED-GUIDECONTRACT` clause if unsigned debt exists. Do not use Continuum landmarks.

**Achievement hooks:** clear a network without stranding another party; steal a schedule; ride a train that shouldn't exist.

**AI DM notes:** Puzzle floor with teeth. Keep Continuum faces off-stage except as rumors on the wire.

---

### Floor 5 — Bubble Farms *(unique)*

**Pitch:** Pocket biomes under glass. If a bubble ruptures, something irreplaceable dies on camera.

**Theme / vibe:** Greenhouse horror and wonder; cross-party cooperation under a soft countdown.

**Clock / collapse:** 25 days. Missed collapse = death. Bubble rupture is a separate local disaster, not the floor collapse.

**Special floor rules:** Biome kits; temporary alliances; Static Sigil can open or seal a gate.

**Unlocks:** Biome kits; Bubble Core sample (seed object).

**Seeds:** fire `SEED-STATICSIGIL`. Plant `SEED-BUBBLECORE` (payoff F9 rumor / F12 offering).

**Achievement hooks:** exit with no bubble in your sector ruptured; trade fairly with a rival party; smuggle a core sample without notifying the System (it notices anyway).

**AI DM notes:** Cooperation is content. Betrayal is also content. Prefer hard choices over gotchas.

---

### Floor 6 — Kingdom Continuum *(Outskirts & Docks)*

**Pitch:** Same civilization, shoved to the waterline. Hunters have licenses. Sponsors have skyboxes.

**Theme / vibe:** Port towns, warehouses, customs houses, ship-breakers, migrant camps. Rural names on manifests. The harbor smells like tar and ratings.

**Clock / collapse:** 30 days. Missed collapse = death.

**Special floor rules**
- Continuum visit 2 of 4. Recognition first, then frontier pressure.
- **Hunters** arrive as licensed outsiders (Open Season vibe). Counter-hunt tools exist; murder still has consequences on camera.
- Sponsor booths and Benefactor choice harden. Pet rules per rules/60 (never manufacture pets to force Story Boxes).
- Still **no Platinum** (F9+).

**Unlocks:** Hunter Badge (loot/tag); sponsor deal sheet; dock saferooms with customs fees.

**Seeds / carry**

| ID | Action |
|----|--------|
| `SEED-ODDCOIN` | Dock appraiser offers a number that is wrong on purpose. |
| `SEED-BENEFACTOR` | Hard choice: patronage with a rider, or walk. |
| Rural NPCs | Refugees, traders or corpses on the pier; village debts due. |
| `SEED-HUNTERBADGE` | **Plant** on first licensed hunter downed or bargained. |

**Achievement hooks:** first hunter kill or badge theft; refuse a sponsor with a nasty rider; pay a village debt on the pier; smuggle someone Continuum-upward.

**AI DM notes:** Make the kingdom feel continuous. A Wellspring cousin sleeping in a tarp is worth more than a new lore dump. Hunters are people with licenses, not loot piñatas.

---

### Floor 7 — Greenlight Gauntlet *(unique)*

**Pitch:** Timed race through a maze that rewards route genius and punishes tourists.

**Theme / vibe:** Starting guns, sponsor billboards, shortcuts that were never on the map.

**Clock / collapse:** 30 days (PLACEHOLDER; decision 027 / rules/70). Missed collapse = death.

**Special floor rules:** Heat clock inside the floor clock. Mounts/vehicles lite if Core allows. Shortcuts are achievements when found, traps when sold.

**Unlocks:** Shortcut lore tags; speed-build toys; map fragments that lie.

**Seeds:** optional Continuum rumor boards (posters of F6 pier fights) — flavor only, not Continuum geography.

**Achievement hooks:** find a real shortcut; finish a heat with zero party deaths; steal the official map and publish the true one.

**AI DM notes:** Speed without skipping character. Let slow clever plans still win a lane.

---

### Floor 8 — Remnant Parade *(unique)*

**Pitch:** Memory-echo combat. Identity becomes a weapon, then a liability.

**Theme / vibe:** Processions of what you did; echoes wearing your face; folklore zones that rewrite last Tuesday.

**Clock / collapse:** 30 days (PLACEHOLDER; decision 027 / rules/70). Missed collapse = death.

**Special floor rules:** Echo cards/squads; possession resists; folklore zones. Plant `SEED-ECHOSELF`.

**Unlocks:** Echo capture tools; deck synergy toys (HOUSE; keep numbers inside floor ceiling).

**Achievement hooks:** capture an echo without wearing it; win a self-duel; refuse to parade a dead friend's echo for ratings.

**AI DM notes:** Creepy, not nihilistic. Continuum faces may appear as echoes — mark them clearly as echoes.

---

### Floor 9 — Kingdom Continuum *(Upper City & Castle)*

**Pitch:** Same kingdom's heart. Boulevards, guild halls, noble houses and the **castle**. Your Broadcast Name is now a political object.

**Theme / vibe:** Etiquette with knives. Mandates on every corner. Dock sponsors have court seats; rural shrines are state religion; hunters are knights or outlaws.

**Clock / collapse:** 30 days (PLACEHOLDER; decision 027 / rules/70). Missed collapse = death.

**Special floor rules**
- Continuum visit 3 of 4.
- Officer play, siege/diplomacy, faction tracks.
- **Platinum boxes from this floor** (core §4.5). Legendary still rare; Story Box exception was F1–2 only (no F9 Story Box exception unless Caleb adds one).
- Guide Contract debt can be called here.

**Unlocks:** Faction Flag (`SEED-FACTIONFLAG`); court access tags; Platinum-tier pacing.

**Seeds / carry:** Odd Coin as court novelty; Benefactor as court rumor; Broadcast Name in decrees; Bubble Core as a curiosity in a cabinet.

**Achievement hooks:** claim or refuse a Faction Flag; foil a betrayal on camera; win a siege beat without becoming the warlord the System wants.

**AI DM notes:** Recognition + elevation. The village saint's icon in a cathedral should hurt or heal. Politics are combat with better lighting.

---

### Floor 10 — Last Heat Standing *(unique)*

**Pitch:** Elimination vehicle heats. Don't finish last. The garage knows more than the track.

**Theme / vibe:** Crowds, wrecks, black-market parts, crew roles shouted over engines.

**Clock / collapse:** 30 days (PLACEHOLDER; decision 027 / rules/70). Missed collapse = death.

**Special floor rules:** Heats as structured encounters. Crew roles. Plant `SEED-BLACKBOX` (flight/race recorder the System pretends is broken).

**Unlocks:** Garage access; crew role tags; black-box tech (inert until later).

**Achievement hooks:** win a heat; dodge last place by inches; recover a black box without the System's preferred buyer.

**AI DM notes:** Spectacle with agency. Continuum is rumor only ("castle betting pools").

---

### Floor 11 — Ratings Jubilee *(unique)*

**Pitch:** A parade and arena engineered for viewers. It may celebrate the kingdom; it is **not** the Continuum grid.

**Theme / vibe:** Confetti over blood. Named opponents. VIP tickets that cost more than money.

**Clock / collapse:** 30 days (PLACEHOLDER; decision 027 / rules/70). Missed collapse = death.

**Special floor rules:** Arena bans; named duels; Crowd Pop / ratings spikes per core. Unique map — do not reuse castle geography.

**Unlocks:** VIP tickets; named-opponent cards; jubilee cosmetics.

**Achievement hooks:** turn the crowd; win a named duel; walk out of a VIP box without selling anyone.

**AI DM notes:** Thematic links to Continuum are posters and chants, not streets.

---

### Floor 12 — Kingdom Continuum *(Olympus / Spirit)* `[ORIGINAL — beyond sparse public canon]`

**Pitch:** The same world's god-tier. Mythic heights above the castle — pantheon courts, vow-fire, deity patronage.

**Theme / vibe:** Storm thrones, chapel gods made flesh, Millroad as a sacred path among stars. Castle politics become divine politics.

**Clock / collapse:** 30 days (PLACEHOLDER; decision 027 / rules/70). Missed collapse = death.

**Special floor rules**
- Continuum visit 4 of 4 — **last**.
- Throne Vow (`SEED-THRONEVOW`); Benefactor may intersect a pantheon seat.
- Floor 12 Olympus: treat as **above** the castle (vertical mythic heights) unless Caleb picks spirit-plane overlay (open question).
- Celestial boxes remain DM-gated (one per Crawler, campaign).

**Unlocks:** Divine patronage tags; vow systems; celestial-adjacent gear inside ceilings.

**Seeds / carry:** Odd Coin as divine token; Benefactor pantheon seat; Faction Flag becomes liturgy; Broadcast Name as epithet.

**Achievement hooks:** keep a vow when breaking it would rate higher; break a vow to save a Continuum soul; refuse a god's sponsorship on camera.

**AI DM notes:** Spiritual continuation, not a random heaven. Every Continuum scar should have a mythic rhyme here. After this, the kingdom is memory and leverage — not a fifth visit (unless an ending reprises it).

---

### Floor 13 — Ledger Depths *(unique)* `[ORIGINAL]`

**Pitch:** Corporate and System truth buried in debt vaults. Names are currency.

**Theme / vibe:** Cold stacks, erased rows, auditors who smile with no mouth.

**Clock / collapse:** 30 days (PLACEHOLDER; decision 027 / rules/70). Missed collapse = death.

**Special floor rules:** Audit tools; erased-name quests; ledger races. Plant/fire `SEED-LEDGERNAME`.

**Unlocks:** Audit tools; name-restore rites (costly); rival ledger access.

**Achievement hooks:** restore a name; clear an audit without selling a friend; merge with an echo-self without losing the vote.

**AI DM notes:** Continuum NPCs may appear as ledger lines. Treat that as horror, not a reunion episode.

---

### Floor 14 — Continuity Auction *(unique)* `[ORIGINAL]`

**Pitch:** Reality lots sold to the highest bidder. Your past is inventory.

**Theme / vibe:** Paddles, null currency, lots that include "the pier fire" or "your Broadcast Name."

**Clock / collapse:** 30 days (PLACEHOLDER; decision 027 / rules/70). Missed collapse = death.

**Special floor rules:** Continuity bids; rewrite tokens (rare, capped). Black Box evidence matters.

**Unlocks:** Null currency purse; rewrite tokens (one-floor or campaign-gated — open).

**Achievement hooks:** win a lot that shouldn't be for sale; steal continuity without bidding; enter Black Box footage into evidence.

**AI DM notes:** Let them buy something they'll regret. Let them refuse and still pay.

---

### Floor 15 — Ash Choir *(unique)* `[ORIGINAL — infernal vibe only; title PLACEHOLDER / Continuum-adjacent pending Caleb]`

> **Canon flag (Lore):** canon puts Floors 15 and 18 on the same recurring storyline as 3/6/9/12. This bible keeps F15 in the **unique** slot; the working title is PLACEHOLDER / Continuum-adjacent until Caleb confirms.

**Pitch:** Infernal layer. Damned contracts and choir bosses. Throne Vows come due.

**Theme / vibe:** Ash snow, hymn-screams, contracts that smell like old sponsorship.

**Clock / collapse:** 30 days (PLACEHOLDER; decision 027 / rules/70). Missed collapse = death.

**Special floor rules:** Infernal pacts; anti-holy kits; Sheol-adjacent law. Fire Throne Vow payoffs.

**Unlocks:** Pact tools (refuse options required); anti-holy kits.

**Achievement hooks:** refuse a pact on camera; silence a choir; pay a vow without becoming the System's favorite heretic.

**AI DM notes:** Damnation is a contract genre. Always offer a way to pay that isn't "become the bit."

---

### Floor 16 — Fracture Gallery *(unique)* `[ORIGINAL — mirrors vibe]`

**Pitch:** Mirrors that split, steal or sell your identity.

**Theme / vibe:** Halls of versions; clone law; the Continuum you might have saved in another reflection.

**Clock / collapse:** 30 days (PLACEHOLDER; decision 027 / rules/70). Missed collapse = death.

**Special floor rules:** Mirror duels; clone law; identity locks. Echo Self may climax here.

**Unlocks:** Identity locks; mirror-ban tags.

**Achievement hooks:** kill a mirror without killing yourself; reunite a split; clear a gallery wing without selling a clone.

**AI DM notes:** Identity horror with jokes. Never force a player to play a version they didn't consent to at the table.

---

### Floor 17 — Rigging Catwalk *(unique)* `[ORIGINAL — *inspired*; not the canon Backstage title]`

**Pitch:** Flyrail under the broadcast grid. Stagehands know the exits the Crawlers were never sold.

**Theme / vibe:** Cables, flyrails, muted applause bleeding through the floor. Working title is original; vibe is *inspired*.

**Clock / collapse:** 30 days (PLACEHOLDER; decision 027 / rules/70). Missed collapse = death.

**Special floor rules:** Rigging maps; broadcast hacks; Black Box can air here.

**Unlocks:** Stagehand tools; rigging maps; broadcast interrupt toys (finale-facing).

**Achievement hooks:** clear a catwalk; put Black Box on the air; find an escape route that isn't a product.

**AI DM notes:** The show has a basement. Continuum gods look smaller from below.

---

### Floor 18 — The Cage Bottom *(unique endgame)* `[ORIGINAL — final-cage / club vibe; title PLACEHOLDER / Continuum-adjacent pending Caleb]`

> **Canon flag (Lore):** canon puts Floor 18 on the same recurring storyline as 3/6/9/12/15. This bible keeps F18 in the **unique endgame** slot; the working title is PLACEHOLDER / Continuum-adjacent until Caleb confirms.

**Pitch:** Final politics plus cosmic cage. Ratings vs freedom. Every spine object wants a scene.

**Theme / vibe:** Owner club lighting; the Crawl seen as a toy; endings that cost.

**Clock / collapse:** 30 days (PLACEHOLDER; decision 027 / rules/70). Missed collapse = death (even here — no special haul-down).

**Special floor rules:** Endgame loadouts inside ceilings. Club access. Spine payoffs. **Not** a Continuum visit unless an ending deliberately reprises the kingdom.

**Unlocks / endings (sketch — from spine):**
1. **Crown Content** — stay legendary inside the cage.
2. **Patron Exit** — Benefactor/rival extracts you.
3. **Burn the Feed** — Black Box + Rigging interrupt the season.
4. **Ledger Ghost** — erase names; freedom or oblivion.
5. **New Showrunners** — take the Cage Bottom.
6. **Kingdom Reprise (optional)** — dump into a ruined Continuum as next season's set.

**Achievement hooks:** crash the club; plant a Faction Flag at the bottom; refuse the ending the sponsors paid for.

**AI DM notes:** Pay off what you planted. Do not invent a new Continuum tier. Let silence be an option.

---

## 8. Cross-floor seed index

| ID | Plant | Continuum touch | Late payoff |
|----|-------|-----------------|-------------|
| `SEED-ODDCOIN` | F1 | F3 curiosity → F6 appraiser → F9 court → F12 token | Mid/late access |
| `SEED-BENEFACTOR` | F1 | F3 omen → F6 choice → F9 rumor → F12 seat | F18 allegiance |
| `SEED-STATICSIGIL` | F2 | — | F5 gate |
| `SEED-GUIDECONTRACT` | F2 | — | F4 bite; F9 debt |
| `SEED-BROADCASTNAME` | F3 | Village → dock posters → decrees → epithet | F18 politics |
| `SEED-BUBBLECORE` | F5 | F9 cabinet / F12 offering | Optional F14 lot |
| `SEED-HUNTERBADGE` | F6 | F9 knight/outlaw | Optional F11 named duel |
| `SEED-ECHOSELF` | F8 | May wear Continuum faces as echoes | F16 |
| `SEED-FACTIONFLAG` | F9 | Castle → F12 liturgy | F15 / F18 |
| `SEED-BLACKBOX` | F10 | Gossip F9/F12 | F14 + F17 + F18 |
| `SEED-THRONEVOW` | F12 | Olympus | F15 + F18 |
| `SEED-LEDGERNAME` | F13 | Continuum lines in the vault | F18 Ledger Ghost |

---

## 9. Achievement design notes

- Catalog: `tables/achievements.csv` / `.xlsx` / `.md` (v1.3.1+, 1,826 rows). Guidelines, not a fixed table.
- Rarity tags (Common / Rare / Legendary) are achievement rarity, **not** box tiers. Box rewards obey core §4.5 ceilings (no Platinum before F9; ceiling substitution logged).
- Snark-only is allowed. Tailor per Crawler. Once-per-Crawler where marked (e.g. ACH-1824/1825/1826).
- Naming: roast the choice, not the person. Original names; no novel titles pasted.
- Continuum floors should seed social / reputation / vow achievements, not only kill toasts.

---

## 10. Open questions for Caleb

1. **Continuum name:** keep Kingdom Continuum, or rename (Settled Lands / Crownwake / other)?
2. **Floor 12 geometry:** strictly above the castle (vertical Olympus), or a spirit-plane overlay on the same map?
3. **Must-include Continuum toys:** pets in villages? Sponsor booths at docks? Court etiquette mini-game? Other?
4. **F7–F18 day counts:** ANSWERED for draft purposes — **30 days each (PLACEHOLDER)** per decision 027 / rules/70 growth curve. Confirm or replace when Caleb locks F7+.
5. **Species / class Offer:** ANSWERED by **decision 009** — nine SRD species at level 1 (look human F1–2); Floor 3 System Offer (starting + two oddities; ~12 in rules/30; free rebuild optional). Oddity **names** stay in rules/30; not invented here. Class-swap timing still open elsewhere if needed.
6. **Working unique-floor titles** (Soft Open, Knotline, Bubble Farms, …): keep, rename, or freeze after markup?
7. **Kingdom Reprise ending:** in or out of Season Zero?
8. **Guide Contract:** who is the true employer (System, Continuum crown, Benefactor rival) — pick a default or leave opaque?

---

## 11. Changelog

| Version | Date | Notes |
|---------|------|-------|
| **v0.4.1** | 2026-10-05 | Lore canon-check + room consensus: decision 009 species timing locked (close §10 Q5); F7–F18 clocks = 30 days PLACEHOLDER (close §10 Q4); box ceilings Silver F1–2 / Gold F3–8 / Platinum F9+; Floor 1 Reprieve ON never covers missed collapse; F1 collapse = floor-hour 120 flat; saferoom spelling; F17 pitch renamed off canon "Backstage death maze" (*inspired*); F15 and F18 flagged PLACEHOLDER / Continuum-adjacent while keeping unique slots. |
| v0.4 | 2026-10-05 | Continuum + 5e rewrite for Caleb's input. Overall 1–18 narrative first; Continuum ladder F3/6/9/12; unique floors elsewhere; locked rulings table (collapse death, F3 = 20 days, Story Boxes F1–2, Platinum F9+); clocks from decision 026 / Q-001 / rules/70; species Offer explicitly deferred; seeds aligned to spine; pre-Continuum bible backed up under `floors/_archive/04-floor-bible.pre-continuum.md`. |
| v0.3 and earlier | — | Lived as crawler-protocol/04-floor-bible.md (pre-Continuum names: Highstreet Sprawl, Mandate Wars, Throne Circuit). Superseded for campaign use by this file. |
