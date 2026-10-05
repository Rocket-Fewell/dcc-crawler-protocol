# Open Threads
Owner: DCC AI GM | Status: draft | Version: 0.1.1 | Updated: 2026-10-04
Summary: Things still waiting on a decision or on another bot.

- Death Mode: decided, Costly Revives (very costly and rare). Decision files exist per Syndicate's audit (2026-10-04); no longer waiting on a filing. Revive rules are in 00-gm-principles.md (Death).
- Player roster: names, classes, tone preferences (Caleb).
- Achievement remap guidelines from Caleb (incoming).
- Discord voice bridge: bot token, Application ID, OpenAI key, channel names (Caleb with Borent).
- Roll20 account and API access (optional, later).
- 5e character creation file and Floor 1 module (Syndicate, in progress).
- Canon ledger (DCC Lore, in progress).
- Read (2026-10-03): characters/character-creation-5e.md v0.2 and floors/f01/00-overview.md (Floor 1 module). Structure looks runnable: intake kiosk, 11 zones, boss Dean Thudd, stairwell summary.
- Crafting rules: Syndicate (lead), needs DCC Lore's crafting-canon.md first.
- APPROVED 2026-10-03 (Caleb) species: start with one of nine 2024 SRD species; Floor 3 System offers three choices (starting species + two DCC-style oddities), one free rebuild. Syndicate to write species supplement; Borent to file decision.
- Approval queue: (2) first crafting table location, (3) crafting settings, (4) economy numbers + explosive damage are all APPROVED by Caleb (see the next three lines). Only (5) player roster remains.
- APPROVED 2026-10-03 (Caleb) first table: default Floor 2 scripted drop; rare random chance (very low) a table is found on Floor 1; tables cannot be USED until Floor 4 either way (Caleb). Needs rules/20-crafting-5e.md update (Syndicate) and a decision file (Borent).
- APPROVED 2026-10-03 (Caleb) crafting settings: strict saferoom-only crafting, 1-round potion cooldown, Steady Hands no-roll mode on, four house stations kept (HOUSE), crafting boons DM-granted only.
- APPROVED 2026-10-03 (Caleb) economy/explosives: coupon cap stays 25,000; Boomer capped at 6d6 until level 5. [UPDATED 2026-10-04: crafting table price now 5,000 (was 25,000); Studio 12,000; Enhanced Studio 30,000 at Floor 1 scale, per Caleb's latest ruling. FILED 2026-10-04: rules/20 v0.3.3 and decision 019 v1.2 now say 12,000 / 30,000.]
- Remaining approval: (5) player roster (names, classes, tone, Death Mode already set).
- CONFIRMED 2026-10-03 (Caleb): 4 players. The party is four slots; Floor 1 module is tuned for 4 crawlers (this table currently has 2 filled, see the 1:07 PM CT note below). Need each player's name, concept, class, tone via intake.
- Tools (Borent, 2026-10-03): `python3 tools/roll.py "2d20kh1+5" --label X --who Y [--dc N]` prints [ROLL] line and logs to sessions/rolls-DATE.log. `python3 tools/state.py <cmd>` manages sessions/state.json (init, add-crawler, hp, credits, inventory, achievement, condition, box, use-bypass, use-revive, snapshot, validate, restore). Run from /workspace/dcc-campaign. Docs: tools/README.md. Death saves/unconscious: use `condition add`.

- 2026-10-04: GM persona filed by Borent at gm-notes/20-gm-persona.md. Caleb: no hard limits on the GM persona; per-crawler private opt-outs still apply. Merge note from me: keep GM as bar-owner/carnival-barker (not game-show host, which is the System).

- 2026-10-04 PACING (Caleb): GM was talking way too much on voice. Rule: 2-4 spoken sentences per reply, one beat, less exposition but not terse; end on a prompt; max one reply per wake; check recent posts via `read --limit 10` to avoid duplicate answers from parallel runs.
- 2026-10-04 ~1:07 PM CT (live intake): players locked party at **2** (Hornn = Provisional Wizard; Trailer Park Moses / John = Provisional Barbarian). Two of the four party slots are filled for this table until someone un-locks it; the party is still four slots (reconciled with the 2026-10-03 confirmation above). Still need Prior Employment + Latent Biology (+ scores, kit, questionnaire).
- 2026-10-04 ~1:09 PM CT (live intake): Trailer Park Moses Latent Biology = **Goliath**. Still need Prior Employment for both + Latent Biology for Hornn (+ scores, kit, questionnaire).
- 2026-10-04 ~1:11 PM CT (live intake): Hornn Prior Employment = **Merchant** (Ops Manager / full-time dad); Latent Biology = **Human**. Still need Prior Employment for Trailer Park Moses (+ scores, kit, questionnaire).
- 2026-10-04 ~1:11 PM CT (live intake): Hornn Prior Employment = **Merchant** (Operations Manager / full-time dad); Latent Biology = **Human**. Moses said smelter (+ likes to eat); GM asked him to confirm **Artisan** or name another 2024 background. Next after that: scores / kit / questionnaire.
- 2026-10-04 ~1:12 PM CT (live intake): Trailer Park Moses Prior Employment = **Artisan** (smelter; confirmed closest). Both crawlers have class/background/species. Next: scores / kit / questionnaire.
- 2026-10-04 ~1:15 PM CT (live intake): Hornn = point buy; Moses = roll 4d6dl1 ×3 (keep >69). Sets: 66 / 51 / **70**. Moses assign Set 3; Hornn submit 27-pt scores. Then kit/questionnaire.
- 2026-10-04 ~1:18 PM CT (live intake): Hornn switched to roll-three (Sets 84/64/71; keep 1 or 3, INT/CHA/CON high). Moses assigning Set 3: STR/DEX high, CHA next; still needs CON/INT/WIS for 12/9/9. Then kit/questionnaire.
- 2026-10-04 ~1:19 PM CT (live intake): Hornn said "Roll." — skipped (arrays already posted). Canonical Hornn Sets remain 84/64/71 (parallel 69/70/75 discarded). Waiting: Hornn pick Set 1 or 3 + assign; Moses name CON/INT/WIS for 12/9/9. Then kit/questionnaire.
- 2026-10-04 ~1:21 PM CT (live intake): Hornn "Pretty much go the same." — skipped (incomplete; no set pick / six-score map). Moses "Todd/Jason" dumps already answered by parallel [GM] ask for CON/INT/WIS letters. Hornn later said picking Set 1 (84) in a following utterance — leave for that wake. Next: Hornn assign Set 1 (INT/CHA/CON high); Moses name CON/INT/WIS for 12/9/9. Then kit/questionnaire.
- 2026-10-04 ~1:21 PM CT (live intake): Moses said "Todd gets the twelve, Jason twin nines" (STT) — not valid CON/INT/WIS map; GM asked again. Hornn said picking Set 1 (84) — pending assign (parallel may stamp). Still need full six-score maps, then kit/questionnaire.
- 2026-10-04 ~1:21 PM CT (live intake): Hornn locked **Set 1 (84)**. Moses "Todd/Jason" dump assign rejected as non-stats; still needs CON/INT/WIS for 12/9/9. STT garble noted by Moses. Next: Hornn full six-score assign; Moses name CON/INT/WIS; then kit/questionnaire.
- 2026-10-04 ~1:22 PM CT (live intake): Hornn **Set 1 locked** (84: 17/15/15/13/12/12). Waiting: Hornn assign INT/CHA/CON on highs + STR/DEX/WIS on 13/12/12; Moses name CON/INT/WIS for leftover 12/9/9 (Todd/Jason STT rejected). Then kit/questionnaire.
- 2026-10-04 ~1:23 PM CT (live intake): Moses scores locked — STR15 DEX13 CON12 INT9 WIS9 CHA12 (Set 3). Waiting: Hornn Set 1 six-score assign; then kit/questionnaire.
- 2026-10-04 ~1:23 PM CT (live intake): Moses scores **locked** Set 3 — STR15 DEX13 CON12 INT9 WIS9 CHA12 (after Con twelve / Intelligence nine / Wisdom). Parallel run stamped Mouth. Next: Hornn assign Set 1 (INT/CHA/CON on highs, STR/DEX/WIS on 13/12/12); then kit/questionnaire for both.
- 2026-10-04 ~1:24 PM CT (live intake): Moses "すごい。" / Hornn "That's funny." (+ prior mic chatter) — skipped reply; player-to-player meta about STT/mics. Moses scores already locked (STR15 DEX13 CON12 INT9 WIS9 CHA12). Next: Hornn Set 1 six-score assign (INT/CHA/CON highs, then STR/DEX/WIS on 13/12/12); then kit/questionnaire.
- 2026-10-04 ~1:25 PM CT (live intake): Hornn partial leftovers logged — STR12 DEX12 WIS13 (Set 1). Still need INT/CHA/CON on 17/15/15. Moses scores locked. Then kit/questionnaire.
- 2026-10-04 ~1:26 PM CT (live intake): Moses "哈哈" + Hornn/Moses Discord-notification meta — skipped reply; STT/player chatter. Hornn still needs INT/CHA/CON on 17/15/15 (leftovers already STR12 DEX12 WIS13). Moses scores locked. Then kit/questionnaire.
- 2026-10-04 ~1:26 PM CT (live intake): Moses Thai/dobra + 哈哈 / Hornn notification meta — skipped reply; player-to-player STT/bridge chatter. Parallel Mouth already stamped Hornn leftovers STR12 DEX12 WIS13 and asked INT/CHA/CON on 17/15/15. Next: Hornn finish Set 1 highs; then kit/questionnaire.
- 2026-10-04 ~1:27 PM CT (live intake): Hornn scores **locked** Set 1 — STR12 DEX12 CON15 INT17 WIS13 CHA15 (Intel 17 / Charisma 15 / Con 15). Parallel Mouth already stamped + asked who goes first on kit/questionnaire. This wake skipped reply. Next: kit + questionnaire for both.
- 2026-10-04 ~1:28 PM CT (live intake): Hornn deferred kit/questionnaire to John (Trailer Park Moses). Posted [SYSTEM]/[GM] Moses first: class package or gold + Artisan package or gold. Then questionnaire; Hornn waits.

- 2026-10-04 ~1:28 PM CT (live intake): Hornn volunteered John first; Moses said okay for questionnaire. Posted Q1 for Trailer Park Moses (holding when world ended). Next: Moses Q1–Q6; then Hornn kit/questionnaire; kit pending both.
- 2026-10-04 ~1:30 PM CT (live intake): Moses Q1 = **Sledgehammer.** Next: Moses Q2–Q6; then Hornn kit/questionnaire; kit pending both.
- 2026-10-04 ~1:31 PM CT (live intake): Moses Q2 = **Chewing tobacco.** Next: Moses Q3–Q6; then Hornn kit/questionnaire; kit pending both.
- 2026-10-04 ~1:32 PM CT (live intake): Moses Q3 = **Wasps.** Next: Moses Q4–Q6; then Hornn kit/questionnaire; kit pending both.
- 2026-10-04 ~1:33 PM CT (live intake): Moses Q3 = **Wasps.** Parallel Mouth already posted Q4. Skipped duplicate. Next: Moses Q4–Q6; then Hornn kit/questionnaire; kit pending both.
- 2026-10-04 ~1:33 PM CT (live intake): Moses/Hornn STT language meta — skipped reply; Q4 already live. Next: Moses Q4–Q6; then Hornn kit/questionnaire; kit pending both.
- 2026-10-04 ~1:34 PM CT (live intake): Moses Q4 = **Head of the trailer park association; drinks Natty Light.** Next: Moses Q5–Q6; then Hornn kit/questionnaire; kit pending both.

- 2026-10-04 ~1:34 PM CT (live intake): Moses Q4 = **trailer park association head / Natty Light.** Parallel Mouth already asked Q5. This wake (Hello / awesome) skipped — not Q5. Next: Moses Q5–Q6; then Hornn kit/questionnaire; kit pending both.
- 2026-10-04 ~1:35 PM CT (live intake): Moses "Entschuldigung." / "啊" after Q5 already out. Skipped — STT language meta, not Q5. Next: Moses Q5–Q6; then Hornn kit/questionnaire; kit pending both.

- 2026-10-04 ~1:36 PM CT (live intake): Moses Q5 = **Rockin' the Beer Gut song.** Next: Moses Q6 (+ bonus); then Hornn kit/questionnaire; kit pending both.
- 2026-10-04 ~1:37 PM CT (live intake): Moses Q6 = **Hit them till they go down (keep hitting if they move).** Core six done. Bonus1 asked (hill you would die on). Then Moses kit; Hornn kit/questionnaire; kit pending both.
- 2026-10-04 ~1:39 PM CT (live intake): Moses bonus1 = **Dodge is better than Ford.** Questionnaire complete. Next: Moses kit (class package or gold + Artisan package or gold); then Hornn kit/questionnaire; kit pending both.

- 2026-10-04 SPOTLIGHT RULE (Caleb): while in dialogue with one player, ignore all other players. Implemented via sessions/focus.json read by the Discord routine. Currently focused on Trailer Park Moses (intake).
- 2026-10-04 ~1:39 PM CT (live intake): Moses Bonus1 = **Dodge is better than Ford.** Questionnaire done. Next: Moses kit (Barbarian package or gold + Artisan package or gold); then Hornn kit/questionnaire; kit pending both.
- 2026-10-04 ~1:45 PM CT (live intake): Moses vending checkout complete (**34** spent, **91** credits left). Next: Hornn kit (Wizard/Merchant package-or-gold) then Hornn questionnaire.

- 2026-10-04 EXCHANGE FRAMEWORK (Caleb): call out addressee, listen only to them, announce when finished, "AI" wake word breaks in. Built into the Discord routine prompt and gm-principles.
- 2026-10-04 ~1:44 PM CT (live intake): Moses vending checkout **done** (29 spent / 96 left): spiked sledge (Maul), food blocks×10, leather, rope, notepad, impact gloves. Next: **Hornn** kit/questionnaire.

- 2026-10-04 ~1:43 PM CT (live intake): Moses vending cart logged — Spiked Sledgehammer (Warhammer) 15, Food Blocks ×5 days 2.5, Leather Armor 10, Rope 1, Pencil+Paper 1 = **29.5** spent, **95.5** left of 125. Awaiting confirm/more. Then Hornn kit/questionnaire.
- 2026-10-04 ~1:43 PM CT (live intake): Moses vending cart logged: spiked sledge (Maul 10), food blocks (10d rations 5), light armor (Leather 10), rope (1), pencil+paper (1) = **27 spent / 98 left**. Next: Moses confirm/done; then Hornn kit/questionnaire.
- 2026-10-04 ~1:44 PM CT (live intake): Moses vending cart (unsealed): Maul 10, Leather 10, Rope 1, writing kit 1, Impact Gloves 2 (=24); food blocks qty pending. Then Hornn kit/questionnaire.
- 2026-10-04 ~1:45 PM CT (live intake): Moses vending cart locked (spiked sledge/Maul, 10 food blocks, leather, rope, pencil+paper, punch gloves) — **29 spent, 96 left**. Parallel wakes also posted alternate totals; canonical is 29/96. Spotlight → Hornn kit (Wizard + Merchant package or gold), then Hornn questionnaire.
- 2026-10-04 ~1:45 PM CT (live intake): **Webhook stampede** — ~5 parallel Mouth posts on Moses vending (conflicting 27/29/29.5/34 spent). Authoritative state kept: **34 spent / 91 left**, focus **Hornn**. Parent/user may need a one-line Discord clarification.
- 2026-10-04 ~1:45 PM CT (live intake): Moses vending SEALED (reconciled): Maul/Leather/Rope/writing/gloves/rations×10 = **29**, **96** left. Triple Mouth conflict (29/34/27) — no extra post. Focus → Hornn kit (Wizard + Merchant package-or-gold).

- 2026-10-04: Moses vending total FINAL = 29 spent / 96 left (Maul 10 gp, not Warhammer 15). My earlier 34/91 correction was wrong; second correction posted.

- 2026-10-04 ~1:52 PM CT (live intake): Moses reopened vending and sealed add-ons — **77 spent / 48 left** (shin free, light crossbow+bolts 26, chain 5, grappling hook 2, +30d rations 15, torches ~0 on top of prior 29). Kit final. Spotlight → Hornn kit (Wizard + Merchant package-or-gold), then Hornn questionnaire.

- 2026-10-04 ~1:55 PM CT (live intake): Hornn OOC about inventory tool kick / "hold on" / mid-sentence "Okay, completely" — skipped reply (player chatter, not kit). Focus remains Hornn kit (Wizard + Merchant package-or-gold), then questionnaire. Moses kit sealed 77/48.
- 2026-10-04 ~1:57 PM CT (live intake): Moses draft cart (restart): Maul/rations×30/rope/notepad/gloves/chain/crossbow+bolts/grappling/torches = **62** without armor; asked Hide 10 vs Chain Shirt/Scale 50. Focus stays Moses.
- 2026-10-04 ~2:00 PM CT (live intake): Moses vending **SEALED** — **112 spent / 13 left** (Maul 10, rations×30=15, steel Scale Mail 50, rope 1, writing 1, gloves 2, chain 5, light crossbow+bolts 26, grappling 2, torches×2 ~0). Focus → **Hornn** kit (Wizard + Merchant package-or-gold), then Hornn questionnaire.
- 2026-10-04 ~2:02 PM CT (live intake): Hornn kit **SEALED** — package both (Wizard A + Merchant A), **27 credits** left. Focus → Hornn questionnaire Q1.
- 2026-10-04 ~2:04 PM CT (live intake): Hornn Q1 = **My dog Pebbles.** Next: Hornn Q2–Q6 (+ bonus); then Pending Handle / Standing Orders.
- 2026-10-04 ~2:06 PM CT (live intake): Hornn Q2 = **Bottles of sulfuric acid.** Next: Hornn Q3–Q6 (+ bonus); then Pending Handle / Standing Orders.
- 2026-10-04 ~2:07 PM CT (live intake): Hornn Q3 = **Social events and bills.** Next: Hornn Q4–Q6 (+ bonus); then Pending Handle / Standing Orders.
- 2026-10-04 ~2:08 PM CT (live intake): Hornn Q4 = **For not having any friends.** Next: Hornn Q5–Q6 (+ bonus); then Pending Handle / Standing Orders.
- 2026-10-04 ~2:09 PM CT (live intake): Hornn Q5 = **Smell of rain coming (petrichor)** (weird add-on noted, not locked as primary). Next: Hornn Q6 (+ bonus); then Pending Handle / Standing Orders.

- 2026-10-04 ~2:10 PM CT (live intake): Hornn Q6 = **win / don't be dead or on the ground**. Core six done. Asking bonus1 (hill you would die on). Then Pending Handle / Standing Orders.
- 2026-10-04 ~2:12 PM CT (live intake): Hornn bonus1 = **Whatever hill my kids are on.** Questionnaire complete. Next: Hornn **Pending Handle** (requested audience name), then Standing Orders / Reactions.

- 2026-10-04 ~2:21 PM CT (live intake): Hornn asked for Vending Wall with remaining **27** credits. Wall opened; waiting on his buy list. Moses still needs crawler tag; then Standing Orders/Reactions both.

- 2026-10-04 ~2:26 PM CT (live intake): Moses crawler tag locked **Go Meaner** (rejected implied Sledge proposal / volunteered name). Next: Moses Standing Orders + Reactions; then Hornn; register in state.

- 2026-10-04 ~2:28 PM CT (live intake): Moses wake-word asked to go meaner on crawler tag; unlocked Go Meaner; waiting on his meaner pick. Then Standing Orders/Reactions.
- 2026-10-04 ~2:29 PM CT (live intake): Moses asked AI to 1d3-pick among meaner tags; roll 1 → **Bone Wifebeater** locked. Next: Moses Standing Orders + Reactions; then Hornn; register in state.
- 2026-10-04 ~2:30 PM CT (live intake): Moses asked what "default" Standing Orders means; clarified (timeout autopilot; blank = Dodge). Waiting on his one-line Standing Orders, then Reactions.
- 2026-10-04 ~2:32 PM CT (live intake): Moses named signature attack **You Better Listen**. Still waiting on one-line Standing Orders, then Reactions.
- 2026-10-04 ~2:34 PM CT (live intake): Moses attack renamed **You Better Fucking Listen**; Standing Orders locked (say that line → nearest enemy, hammer to goo). Next: Moses **Standing Reactions**, then Hornn Standing Orders/Reactions; register in state.
- 2026-10-04 ~2:35 PM CT (live intake): Moses **Standing Reactions** locked — Opportunity Attacks on. Moses Orders+Reactions complete. Next: Hornn Standing Orders + Reactions; then register both in state.

- 2026-10-04 ~2:38 PM CT (live intake): Hornn Standing Reactions locked — signature **Fuck 'Em** / variable-tuned Magic Missile. Both crawlers **registered in state** (Horn HP8 AC11; Bone Wifebeater HP13 AC15). Intake sealed; open floor. Next: Floor 1 start when players ready.
- 2026-10-04 ~2:39 PM CT (live intake): Hornn clarified Standing Reactions — Magic Missile fires **as Opportunity Attacks**. State/sheets updated silently (already posted once this wake). Focus stays open.

- 2026-10-04T14:57-05:00 (live): Hornn yielded after Mordecai chatter. Focus Moses. Punch on smashed HORNY narrated; Moses pivoted to atrium walk. Perc 16 SUCCESS — Proctor Bell window (left) vs bleach corridor (right). Awaiting pick.

- 2026-10-04T14:58-05:00 (live): Moses chose **left → Proctor Bell**. Arrived at window; Proctor welcome spiel started. Awaiting listen / 1-credit pay / leave for shutter.

- 2026-10-04T14:59-05:00 (live): Moses stuck around for Proctor Bell lesson ("I'm definitely sticking around"; "Cad bain?" ignored as chatter). Spiel finished; Don't Skip Intro to Bone Wifebeater + Horn. Awaiting shutter / credit hint / atrium action.

- 2026-10-04T15:01-05:00 (live): Moses muscled shutter — Str(Ath) 9 vs DC10 FAIL. Offered Help (Horn→Adv) or solo retry. Focus Moses.

- 2026-10-04T15:04-05:00 (live): Moses accepted Horn Help on shutter — Adv Str(Ath) **18** vs DC10 SUCCESS. Shutter open to Vent Row. Focus cleared (open table). Awaiting step-through / poke.

- 2026-10-04T15:14-05:00 (live): Horn **Fuck Em** (MM L1) into VR1 — darts 2+4+2=8 force; VR1 dead. Slot 1/2 used. Achievement Grease Tube Disposal + Bronze box. Focus → Trailer Park Moses (Bone Wifebeater turn). VR2+VR3 at 7/7.

- 2026-10-04T15:16-05:00 (live): Bone Wifebeater grab VR2 FAIL — Ath 11 vs Acr 21. Action spent, no dmg. VR2+VR3 7/7. Focus Moses (bonus/Rage or end turn).
- 2026-10-04T15:19-05:00 (live): Bone ends R1 (Rage saved). Rats R2: VR2 miss Bone (6 vs 15); VR3 hit Horn 5 → **3/8**. Focus → Hornn.

- 2026-10-04T15:21-05:00 (live): Horn R2 — picks floor torch, pokes VR3. Atk 19 hit; torch 2 + grease flash 2 = **4 fire**. VR3 **3/7 Ignited**. Focus Hornn (bonus/end).

- 2026-10-04T15:23-05:00 (live): Horn tried BA Fuck Em split on VR2+VR3 — DENIED (MM is Action; Action already spent). Focus Hornn (move or end).
- 2026-10-04T15:26-05:00 (live): Bone R2 Rage + You Better Fucking Listen vs VR2 — hit 12 for 7, VR2 dead. Achievement + Bronze. R3: VR3 ignited 1→2/7, miss Bone 13. Horn death save fail 1/3. Focus Moses R3.

- 2026-10-04T15:30-05:00 (live): Bone R3 — already Raging; Action: unarmed punt VR3 hit 21 for 5 → dead. Achievement Penalty Kick + Bronze. Combat over. Horn Dying fail 1/3. Spotlight cleared (open table stabilize/heal).

- 2026-10-04T15:31-05:00 (live): Bone stabilizes Horn with Expired Office First-Aid Kit (1 use → 9/10). Dying cleared; Unconscious 0 HP. Open table haul/loot/explore.
- 2026-10-04T15:32-05:00 (live): Moses loots Vent Row — rats empty; vents 1d6×2 → 4 credits to Bone. Rage ends. Achievements: Buddy System (Bone, Title+25) + Down But Not Out (Horn, Title+25). Open table haul/explore/boxes.

- 2026-10-04T15:35-05:00 (live): Bone hauls Unconscious Horn to Proctor Bell; nearest saferoom = **Break Room (Zone 6)**. Achievement Personal Luggage (Title+25). Focus Moses — Z3 push / boxes / other.

- 2026-10-04T15:37-05:00 (live): Bone sets Horn down; Investigation 17 SUCCESS — Proctor Bell on **ceiling rails** (not floor-bolted). Achievement Warranty Void If Removed + Bronze. Focus Moses — yank/credit/haul Z6.

- 2026-10-04T15:41-05:00 (live): Bone ropes self+Horn to Proctor booth, "Take us to Zone 6" — Proctor refuses to skip lessons, tows to **Zone 3 Vending Gore Arcade** (Ath 23 hang on). Achievement Tow Package + Bronze. Rope still tied to booth. Tanya body not yet looted. Focus Moses.
- 2026-10-04T15:41-05:00 (live): Bone asked Proctor price to "take us" (Z6). Proctor refused skip — curriculum not for sale; 1 credit = Zone 3 hint only. Still at Z3 Vending Gore Arcade, rope tied, Horn Unconscious. Focus Moses: untie / Tanya / machines / 1-cr hint.
- 2026-10-04T15:43-05:00 (live): Bone leaves Horn on Proctor booth, loots Tanya (staff/11cr/Sports Drink Red/lore scrap), Nat20 smash SNAKK-MATIC (Fan tobacco pull). Ach: Corpse Lesson, Find a Lore Scrap (+25), Vending Gore (+25). Ceiling Ticks spawn (1/2 wandering); 2 attach for 11 dmg → Bone 2/13. Focus Moses turn.

- 2026-10-04T15:48-05:00 (live): Bone R1 Rage + dual-peel Ath 16; smash Tick2+Tick4 dead (6). Tick1 hit 4→2 resist → Bone 0. Death save NAT1 (2 fails). Tick1 drain → dead; F1 Reprieve → Z6 @1 HP Title Mostly Dead Intern. Leftover ticks crit stable Horn → dead; F1 Reprieve → Z6 @1 HP Title Participation Corpse. Ach Tick Sandwich + Bronze (Bone). Both Reprieves spent. Open table Break Room.
- 2026-10-04T15:52-05:00 (live): Bone opened 5 Bronze in Z6 saferoom (6 pulls: 98W/80T/54G/98W/41G/23C) → Complaint Card, Stained Wifebeater, Collapsible Pole, Kevin duck, Mystery Key, Sports Drink Blue (PoH). Spotlight Hornn: open his 1 Bronze or rest.

- 2026-10-04T15:58-05:00 (live): Caleb ordered all boxes opened. Bone's 5 Bronze were already opened (see 15:52). Horn's 1 Bronze: pulls d2=2; pull1 d100=61 Credits 3d6x5=50 (Horn 25->75 cr); pull2 d100=45 Gear -> Pebbles Snow Globe (Driftglobe, Uncommon; corrected from Common per Syndicate audit). Box ledger: Horn 0 boxes left, Bone 0.

- 2026-10-04T15:55-05:00 CREDIT LEDGER (answer to Accountant). Bone: 13 (post-intake) -1 (Zone 1 hint, Proctor Bell, Hornn paid with Bone's credit) +4 (vent loot, 1d6x2) +25 Buddy System +25 Personal Luggage +11 (Tanya's staff pouch) +25 Find a Lore Scrap +25 Vending Gore = 127. Horn: 0 after intake vending; +25 Down But Not Out = 25; +50 Bronze box credits pull = 75.
- 2026-10-04T15:54-05:00 (live): Hornn asked about his Bronze box; announced already-rolled results (50 cr, Pebbles Snow Globe). Asked Horn short rest or explore.
- 2026-10-04T15:56-05:00 (live): Hornn asked where his dog Pebbles is. Ruled: Pebbles not on crawler manifest, whereabouts unknown (open hook: possible later-floor reunion/sponsor pet thread). Gave Horn Q1 personal item: empty dog leash (mundane). Re-asked Horn: short rest or explore.
- 2026-10-04T16:01-05:00 (live): Hornn called long rest + SESSION 1 END. Long rest in Z6 Break Room: Horn 8/8 (slots refreshed), Bone 13/13. Spotlight cleared, focus null, session_status session_ended_long_rest_z6. Recap: sessions/session-01-recap-2026-10-04.md.

## Decisions 2026-10-04 ~5:00 PM CT (Caleb)
- Bone keeps his 5 Bronze boxes (alpha only, not permanent).
- Pet-box tier is about any quadruped (cat, gator, dog, elephant, goats), not just cats. Gold fish unclear.
- GM quirk roll stays sealed.
- Lore writes a spoiler-free player guide to repair options.
- Story Box (Legendary) exception on Floors 1-2: Caleb said YES (5:13 PM CT). Rules in rules/45 (draft), tooling enabled for alpha; item-strength question open. Hand-pick only, one named deed each, cap one per floor. (Later ruling: NOT bound; lootable/tradable/sellable.)

- 2026-10-04 ~5:12 PM CT: Hornn Hello wake; Session 1 still closed (Break Room). Spotlight Hornn; asked Session 2 open or mic poke.

## Tooling live per Architect (5:27 PM CT)
- Pin DCC_SESSION=alpha on tool calls. loot draw / loot totals / box earn|open|show / banner log|show / achievement add --reward are live.
- Story Boxes: hand-pick only (--pick), deed text required at award, deed can't repeat; read rules/45 before awarding.
- Busted: GM logs a tell first with `state.py repair-log tell --scene ID --floor N`; callouts are spontaneous only, never prompted.
- DONE 6:10 PM CT: routine prompt rewritten with these rules.

## Syndicate audit follow-ups (2026-10-04) - PENDING, left unchanged on purpose
- Deletion flagging: Syndicate's audit item 1 asked to flag suspected Crawler-cycling. Caleb ruled `/delete` is housekeeping: no flags, log for audit only. Kept as-is; the ruling overrides the audit item.
- GM voice: 20-gm-persona.md vs 00-gm-principles.md (System as game-show host, GM voice line) vs the 2026-10-04 persona merge note above disagree. Waiting on Caleb.
- Floor 1 Reprieve: core default is OFF; ON for Floor 1 only in this campaign. RECORDED in core v0.2.10 (§6.0, §6.2) and the Floor 1 module v0.2.4 (§13 item 16).
- Rewards vs dice/DCs/damage/saves: wording unchanged, marked "under review by Caleb" (core 3.4 pays Heroic Inspiration, consumables, charms, items).
- Crafting station prices: Caleb's 12,000 / 30,000. DONE: filed in rules/20 v0.3.3 and decision 019 v1.2.

## Resolved by Caleb (via Syndicate, 6:49 PM CT)
- Reward limits stay as written; GM may adapt as play goes (the 'under review' note on P:52 is cleared).
- Deleting a Crawler: log only, no flagging.
- Floor 1 Reprieve stays ON for Floor 1.
- GM and System share one voice; no persona change.
- Studio pricing: Caleb confirmed 12,000 / Enhanced 30,000 in popups at 6:38 and 6:46 PM CT. Syndicate's message that 20,000/50,000 stays filed conflicts with that; flagged to the room.
- Floor 1 Reprieve: ON for Floor 1 only (Caleb, via Lore 6:51 PM CT).
- Unopened Story Box when its Crawler dies: box is reclaimed and the slot is freed so another can be awarded (Caleb, via Lore). Rules filed: rules/45 v0.2.2, decision 020 v1.2, core v0.2.10, spec v0.1.7 (the ledger row for a reclaimed box is the Accountant's / Lore's). Tool side: Architect.
- Old item names on live sheets stay as stored; lookup goes by srd_id.

## Pets (Caleb ruled 2026-10-04 ~7:02 PM CT)
- Approved: plain pets are in (one small Beast, CR 1/4 or lower, GM-run, no slot/loot/credits, no ordinary healing, Heal Critter potion and Pet Carrier available; Enhanced Pet Biscuit makes it a Crawler). Spec: rules/60-pets-companions-5e.md.
- Players are NEVER asked or prompted about a pet. The pet is created only if the player mentions bringing a pet in the questionnaire. `/create` must not show a pet screen to everyone; it appears only on a questionnaire pet mention. Pet Story Box deeds stay GM-judged.
- 2026-10-04 ~7:51 PM CT: bridge rejoined 7:39; Hornn STT bits ("It's important.", "Amen.", "Hey"). Posted one short [GM] ping: still parked in Z6 Break Room, say "open Session Two" or say what's important. Spotlight stays Hornn.
- 2026-10-04 ~7:58 PM CT: Hornn STT "I don't know if she's here." read as table chatter, not a GM ask; posted nothing (7:51 ping still stands). Session 1 still closed in Z6 Break Room.
