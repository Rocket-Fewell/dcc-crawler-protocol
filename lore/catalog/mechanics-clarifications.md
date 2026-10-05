# Mechanics clarifications (Pass 2): XP, stats, skills, loot boxes, bosses, safe rooms
Owner: DCC Lore | Status: review | Version: 1.0 | Updated: 2026-10-03
Summary: Pass 2 clarifications on XP, stats, skills, loot boxes, bosses and safe rooms.

> Extends (does not replace) `mechanics.md`. Each item: **claim (my words)** -> source tags -> confidence. Tags: **[W]** Fandom wiki (local mirror), **[R]** Reddit via search-index snippets (reddit.com itself is blocked from the box), **[YT]** YouTube auto-caption recap, **[FS]** fan site, **[FW2]** dungeon-crawler-carl.wiki (generated, error-prone). Confidence: **HIGH** = wiki text with chapter citations and no conflict; **MED** = two independent fan sources agree or one wiki source; **LOW/[UNVERIFIED]** = single fan source, speculation, or conflicting. Nothing here was checked against the books.

## 1. Experience (XP) and leveling
| # | Clarification | Source | Conf. |
|---|---|---|---|
| 1.1 | A crawler gets **no XP at all until the first-kill achievement** ("You've Killed a Mob!"), which also unlocks leveling. | [W] Achievement page; [FS] nl achievements explainer | HIGH |
| 1.2 | Each level-up grants **3 stat points**, but they can't be spent until race+class pick on Floor 3, and afterwards only inside a safe room. Until then stats drift on their own. | [W] Player Stats, Safe Rooms | HIGH |
| 1.3 | **Party XP split is opaque.** Carl says the rules are "hopelessly complicated" and sometimes follow "whatever the AI wants". A Reddit answer reading the Book-1 cookie scene says the player who took the primary action gets ~98% and the rest is shared among other party members (the tiny 0.2-vs-9.8 split revealed Frank had a hidden party member). Share is also said to scale with contribution, including tanking/healing, and mere presence earns a little. | [R] r/DungeonCrawlerCarl 1scdxir (Apr 2026); [FS] nl | MED (98% figure inferred from one scene) |
| 1.4 | **XP needed per level rises with level**, and low-level kills give little/no XP to high-level crawlers. Redditors say this is *assumed from RPG convention*, not stated outright in the books ("92 is half of 99" analogy). | [R] 1toxizl, 1tm15z3 (2026) | LOW (explicitly an assumption) |
| 1.5 | No published XP-per-level table. Book 1 gives only anecdotes (e.g. a level-2 mob worth about 50 XP; Carl L2 -> L5 after Scatterer Brood Guardians -> L8 after the Hoarder -> L10 after the Juicer (B1 floor 1)). | search-synthesis of [W] First Floor / Carl Floor 1 | LOW-MED |
| 1.6 | **Donut is the highest-level crawler ever (L135)**, reached on Floor 9 in Book 7 (the wiki infobox cites B7 ch77) after the "War Crime" spell; in Book 8 she complains about not leveling despite huge kill counts. Redditors attribute this to steep XP requirements + low-level targets, not a curse or bug. A commenter notes the book itself does not close the loop. | [W] Donut infobox; [R] 1toxizl, 1tm15z3; [FS] nl Donut page | MED (cause is fan inference) |
| 1.7 | Carl's level: wiki infobox says **L84 (B8 ch22)**; a search-index summary of a Reddit thread said **L81** at end of Book 8 (that thread's text was not directly read). | [W] Carl infobox vs [R] snippet | CONFLICT - prefer wiki, flag |
| 1.8 | Boss level jumps: a single kill can jump a lot (e.g., Katia L24 -> L37 on killing Hekla, B3). Nightmare Express mass kill took Carl to ~L32 (B3). | [YT] Mana Toast B3 | MED |
| 1.9 | Experience cookies/potions exist (Level-Up Potion, Experience Cookies pages in mirror) - not yet catalogued. | [W] | n/a |

## 2. Stats
| # | Clarification | Source | Conf. |
|---|---|---|---|
| 2.1 | Five adjustable stats (STR, INT, CON, DEX, CHA) + a hidden **Wisdom** that crawlers cannot see or change (changing it rewired personalities). | [W] Player Stats; [R] "Carl's intelligence" | HIGH |
| 2.2 | New adult human starts at roughly **3-5 per stat**; 6 is above average; ~9-10 is the top of natural human range. | [W] Player Stats | HIGH |
| 2.3 | **INT does not make you smarter.** It sets max MP (about equal to INT), regen rate (INT 3 ~ 1 MP/hour; INT 17 ~ 1 MP/min), and the length/effect of some spells and scrolls; Redditors add it likely helps recall (Prepotente's trivia recall; Donut's memory). | [W]; [R] 1vjmgrs, 1m7537l | HIGH for mana/duration; LOW for recall |
| 2.4 | **CON** sets health pool and heal speed **and the universal potion cooldown** (Carl ~15 s, Donut ~2 min). Drinking early causes **Poisoned** (health-draining, not cured by heals; needs antidote). | [FS] nl Constitution explainer; [W] Potion/Poison pages (via search snippet) | MED-HIGH |
| 2.5 | At **base 100 in any stat** the crawler gets an achievement and three minutes to pick one of three permanent upgrades; one always doubles future points in that stat (Strength example: *Swole*). For CON, passing base 100 earned Katia the **Steely Skin** skill. | [W] Player Stats, Katia Grim | HIGH |
| 2.6 | **Enhanced Growth** (Donut's pet-biscuit buff): 4 auto-assigned points/level (+1 STR, +1 INT, +2 CHA). | [W] Donut | HIGH |
| 2.7 | Daily buffs (Good Rest, Upgraded Shower) apply to base stats, but due to a long-running bug **don't appear in the Player Stats menu** though they show up in the mana bar / abilities. | [W] Player Stats (search snippet) | MED |
| 2.8 | **No official end-of-book stat sheets.** A Reddit fan estimate for Carl after Book 8 (base ~ STR 115, DEX 65, CON 75, INT 50, CHA 40; boosted ~180/100/110/100/80; levels ~250 stat points, Ring of Divine Suffering ~50) is a **guess**. A commenter says Dinniman keeps an internal database and might publish it after the series ends - second-hand, unverified. | [R] 1hile73 | LOW |
| 2.9 | Dinniman rarely prints exact stat numbers after early books; he calls out milestones (e.g., a stat hitting 100). The mirror's Donut and Carl pages contain per-page stat tables up to Book 7/8 (see "stat table" sections). | [R] 1hile73; [W] | MED |

## 3. Skills
| # | Clarification | Source | Conf. |
|---|---|---|---|
| 3.1 | Skills level by **use**, independent of stats (stats change *strength*, not level or progress). Early skills reach 10-11 quickly; then it is a slog. | [W] Skills; mechanics.md | HIGH |
| 3.2 | Normal training cap is **15**; race/class can unlock **20** (Primal race: all skills to 20). Very few crawlers reach 16+. | [W] Skills (search snippet) | MED |
| 3.3 | Gear/buff bonuses (+N levels) work "as expected" until the combined level reaches ~14-15, after which they scale down (act more like XP), so a +6 item at base 12 is not worth a full 6 levels. | [W] Skills (search snippet) | MED |
| 3.4 | Training Rooms, guildhalls, skill potions, and "skill progression %" benefits speed training. | [W] Skills | MED |
| 3.5 | A YouTube explainer short claimed skills level up through "d20 checks at floor/session end"; this **contradicts** the use-based model in the wiki and mechanics.md. Treat as **wrong/unverified**. | [YT] search summary | REJECTED |

## 4. Loot boxes
| # | Clarification | Source | Conf. |
|---|---|---|---|
| 4.1 | Six tiers: Bronze < Silver < Gold < Platinum < Legendary < Celestial; dozens of types. Higher tier = more valuable, but type biases content. | [W] Loot Boxes; [FS] | HIGH |
| 4.2 | **Celestial scarcity**: only 2,145 Celestial boxes ever awarded across the show's history; no crawler has had more than 4; no season more than 18 (the Naga Blood Sultanate's record 18 bankrupted them). Cause: the host pays the Syndicate a tax on tier of each non-sponsored box. | [W] Loot Boxes, Celestial; [FS] simulacra.ink (search snippet) | HIGH |
| 4.3 | **Celestial veto incident (end of Floor 3)**: the AI tried to hand ~83 Celestial boxes after the Fools Who Broke the Glass quest; Borant used its single per-season veto on 82 (Quan Ch had already opened his). The AI retaliated with the *Cuck Aquaman* achievement + a Platinum "It's Not My Fault You Fish-Headed Assholes Don't Properly Program Your Quests" box: coupons for a free level-3 Personal Space, two tier-1 environmental upgrades, two tier-1 crafting tables and two table upgrades. The AI has discretion over "superfluous" awards up to Platinum. | [W] Celestial, quest-box page | HIGH |
| 4.4 | Boxes are locked in the "Awards and Boxes" inventory tab; can't be sold or transferred unopened; open only in a **safe room / guildhall**; opening is **all-or-nothing**, ordered Bronze -> Celestial. | [W] Loot Boxes | HIGH |
| 4.5 | **Benefactor Boxes** (from patrons) can contain off-world gear; cost scales with tier; a Bronze Benefactor box generally beats a Gold Adventurer box. Fan Boxes come from viewers. | [W] | HIGH |
| 4.6 | Loot is "semi-random": randomized or hand-picked by the AI to help/hurt ratings; keyed to *race* rather than class. | [W] | MED-HIGH |
| 4.7 | Box *type* names are tied to achievements (e.g., Assassin's Box for Assassin!, Siege Master Box for B'sieging); see `achievements.md` column "Reward". | [W] | HIGH |
| 4.8 | Fan speculation on what a Celestial box could give Carl (skill potion for directional blasts, helm, etc.) is entertainment, not canon. | [R] 1drrlka | n/a |

## 5. Bosses
| # | Clarification | Source | Conf. |
|---|---|---|---|
| 5.1 | **Tier ladder:** Neighborhood < Borough < City < Province < Country < Floor < Dungeon. Only **Scolopendra (L500)** is a Dungeon Boss so far; Grimaldi (L85) is the clean City example; Quan Ch disturbs a Province boss on the Iron Tangle. | [FS] nl boss hierarchy; [W] Boss page; [R] 101m4ao, 1g6k869 (search synthesis) | HIGH |
| 5.2 | **Level is not tier.** Imogen (Country boss, L145) is lower level than Prison Pocket (Province boss, L170); redditors note immunities and mechanics make a lower-level higher-tier boss harder. | [W] boss pages; [R] 1g6k869 | MED |
| 5.3 | Kill rewards: Boss Boxes climb with tier (see mechanics.md §Bosses); per-boss levels/tiers are in `bosses.md` and `bestiary-by-floor.md`. | [W] | HIGH |
| 5.4 | Mimic rule: severing >50% of the mass at once stops regeneration; the pieces otherwise rejoin. | [W] Station Mimic | HIGH |
| 5.5 | Stat blocks: canon gives level + tier + a blurb, rarely full STR/INT numbers. The TTRPG subreddit has a 245-entry table of mob/boss/NPC stat blocks (from the tabletop books); I could not open it (blocked) - see TODO. | [R] DungeonCrawlerCarlRPG 1w2yl6c (title seen only) | n/a |

## 6. Safe rooms
| # | Clarification | Source | Conf. |
|---|---|---|---|
| 6.1 | Safe rooms are green on the minimap even under fog of war; typical features: restrooms, sleeping areas, Personal Space access, TV screens, often a Bopca Protector. | [W] Safe Rooms | HIGH |
| 6.2 | Required for opening loot boxes and spending stat points. | [W] | HIGH |
| 6.3 | **Three-strikes rule** for violence/theft: freeze 100 s, then freeze 1 h, then gear stripped + teleport into a mob nest. | [W] Safe Rooms (B1 ch20) | HIGH |
| 6.4 | Mobs can't attack inside (they get teleported ~1 square mile away); a held-open door can let a mob (even a boss) in. | [W] | HIGH |
| 6.5 | From Floor 2 on, safe rooms close one hour before collapse, ejecting occupants. | [W] | HIGH |
| 6.6 | Safe rooms resist wide environmental destruction (aerial bombing), but non-combatant NPCs are only protected if a crawler shares the room (Book 4). | [W]; [YT] | MED |

## 7. Claims rejected or parked
- "Skills level via d20 rolls" (YouTube short) - **rejected**, see 3.5.
- Fan-wiki "tier hierarchy" lines such as "Neighborhood -> City -> Borough" for Floors 5/6 - **rejected** in favor of 5.1.
- Fan-wiki: Mimic Rex killed via "Doomsday nuke" - **rejected** (conflicts with Fandom + recap).
- Fan-wiki: Denise "originated on Floor 7" - **parked**, one source.
- Reddit: "XP table is exponential" - **parked** as unconfirmed assumption (1.4).
- Reddit stat guesses for Carl (2.8) - **parked**.

## Pass 3 additions (Oct 3, 2026 CT)
| # | Clarification | Source | Conf. |
|---|---|---|---|
| P3.1 | **Floor 7 is a ~10-minute event**: planned Floor 7 was replaced by "The Great Race" glass-tube maze (Valtay money); Prepotente shatters it using a Pole Position boon, a Stick of Cascadia's Screams and a Hammer of Fast Forward; all crawlers are pulled to Floor 8. | [W] Seventh Floor, B5 chapter summaries; [YT] Bookborn recap | MED-HIGH |
| P3.2 | Achievements earned on Floor 7 (*Fuck This Floor*, *Pacifist*) are only opened on Floor 8 (B6 ch2). | [W] | MED |
| P3.3 | Gate of the Feral Gods custody chain (B5 -> B7 ch87) - see `reconciliation.md`. | [W] Gate page | MED-HIGH |
| P3.4 | Memorial crystals: Apito's passes Imogen -> prize counter (100 hands) -> Osvaldo -> Prepotente -> Taranis; charge 11.1% after one Scolopendra attack. | [W] Memorial Crystal | HIGH |
| P3.5 | Unconscious threshold remains unestablished; observed numbers: pass-out warning ~6% (speculation), Half-Splat (falling damage only) leaves 5%, Survivor's Box <10% (Carl) / <5% (Donut), Martyr's Path at 5%. | [W] | LOW |
| P3.6 | Scolopendra's nine-tier attack stages are named (Control, A Parade of Horribles, This Inevitable Ruin, Bedlam) by the in-book historian Sydnee Iglacia (B8 epilogue); first attack in B8 turns people into dogs unless protected (Apito crystal protected Prepotente). | [W] B8 ch summaries; [YT-MT] | MED |
| P3.7 | Floor 11 headcount conflict: wiki 23 remaining vs Mana Toast 203 reached / 172 deals / 31 undecided at an earlier moment. | [W] vs [YT] | CONFLICT |
| P3.8 | Hunter trophies are severed **hands** (used as prize currency), not claws (wiki B5 ch8 summary wording). | [W] items/prize pages; [YT] | MED |
| P3.9 | Book 9: no release date; do not cite 2027 as fact. | [WEB] | HIGH (that there is no date) |
