# SRD 5.2.1 vs Game Lists: Backgrounds and Origin Feats Audit
Owner: DCC Lore | Status: draft | Version: 0.1 | Updated: 2026-10-04
Summary: Which of the 16 backgrounds and 12 origin-feat entries the game lists are in the CC-BY SRD 5.2.1 and which are not, with a one-line action for each non-SRD item under the rule "print SRD only; non-SRD content lives in a table appendix using our own reskin names and mechanics summaries, no copied non-SRD text". Names only; no non-SRD text is copied here.
Depends on: /workspace/dcc-campaign/tables/chargen-5e.json v0.1.6, characters/create-flow-spec-5e.md (lines 115, 117, 472), tables/background-reskins.json v0.1.2 (32 entries).

## 1. Source and version
- **Document:** System Reference Document 5.2.1 ("SRD 5.2.1"), Wizards of the Coast, licensed CC-BY-4.0. Official download page: https://www.dndbeyond.com/srd (English SRD v5.2.1, listed as published May 01, 2025).
- **File read:** https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf (fetched 2026-10-04; sha256 `8974902d109d6e63672d7c490bde9ccf052410503d9cfa768237154fbc5e3d87`). Read with pdftotext. Its table of contents puts "Character Backgrounds" on p. 83 and "Feat Descriptions" / "Origin Feats" on p. 87.
- **Cross-checks (faithful mirrors, same lists):** https://5e24srd.com/character-origins/character-backgrounds.html, https://www.fantasygrounds.com/library/5e/dd-srd-5-2-1/feats and the D&D Beyond Basic Rules 2024 character-origins page.
- **What the SRD 5.2.1 contains:** exactly **4 backgrounds** (Acolyte, Criminal, Sage, Soldier) and exactly **4 Origin feats** (Alert, Magic Initiate, Savage Attacker, Skilled). Magic Initiate is one feat; the Cleric, Druid or Wizard list is chosen with it. The rest of its feat chapter is General (Ability Score Improvement, Grappler), Fighting Style (Archery, Defense, Great Weapon Fighting, Two-Weapon Fighting) and Epic Boon feats; none of those are listed by the game as Origin feats.
- The SRD names a background's Origin feat; the four backgrounds above use Magic Initiate (Cleric), Alert, Magic Initiate (Wizard) and Savage Attacker. Our chargen-5e.json matches those four on ability triple, feat, skills and tool.
- **Our spec already says the same:** create-flow-spec-5e.md line 117 ("the SRD has only Alert, Magic Initiate, Savage Attacker and Skilled") and open question 7 (line 472: 16 backgrounds vs SRD-only 4); chargen-5e.json lists `srd_backgrounds` = Acolyte, Criminal, Sage, Soldier.

## 2. (a) Backgrounds listed by the game (16)
| Background | In SRD 5.2.1? | Our reskin (background-reskins.json) | Origin feat it grants in chargen-5e.json |
|---|---|---|---|
| Acolyte | **SRD** | Youth-Group Pizza Wrangler (Acolyte) | Magic Initiate (Cleric) |
| Criminal | **SRD** | Call-Center Gift-Card Fraud Specialist (Criminal) | Alert |
| Sage | **SRD** | Adjunct Professor on Four Campuses (Sage) | Magic Initiate (Wizard) |
| Soldier | **SRD** | Black-Friday Mall Security (Soldier) | Savage Attacker |
| Artisan | **non-SRD** | Etsy Shop Founder, Three Sales (Artisan) | Crafter (non-SRD) |
| Charlatan | **non-SRD** | Pyramid-Scheme Boss Babe (Charlatan) | Skilled |
| Entertainer | **non-SRD** | Wedding DJ With One Playlist (Entertainer) | Musician (non-SRD) |
| Farmer | **non-SRD** | Farm-to-Table Influencer (Farmer) | Tough (non-SRD) |
| Guard | **non-SRD** | Hospital Parking-Garage Attendant (Guard) | Alert |
| Guide | **non-SRD** | Trailhead Guide With a Laminated Map (Guide) | Magic Initiate (Druid) |
| Hermit | **non-SRD** | Doomsday Prepper, Collapse Postponed (Hermit) | Healer (non-SRD) |
| Merchant | **non-SRD** | Warehouse Operations Manager (Merchant) | Lucky (non-SRD) |
| Noble | **non-SRD** | Trust-Fund Gallery Owner (Noble) | Skilled |
| Sailor | **non-SRD** | Cruise-Ship Buffet Deckhand (Sailor) | Tavern Brawler (non-SRD) |
| Scribe | **non-SRD** | Law-Firm Paralegal in Redline Hell (Scribe) | Skilled |
| Wayfarer | **non-SRD** | Couch-Surfing Burrito Courier (Wayfarer) | Lucky (non-SRD) |

**Count: 4 SRD, 12 non-SRD.**

## 3. (b) Origin feats listed by the game (12 entries = 10 distinct feats)
| Listed feat | In SRD 5.2.1? | Our reskin |
|---|---|---|
| Alert | **SRD** | Night-Shift Insomniac (Alert) |
| Magic Initiate (Cleric) | **SRD** (Magic Initiate, Cleric list) | Group-Chat Prayer Warrior |
| Magic Initiate (Druid) | **SRD** (Magic Initiate, Druid list) | Houseplant Whisperer |
| Magic Initiate (Wizard) | **SRD** (Magic Initiate, Wizard list) | Wikipedia Rabbit-Hole Scholar |
| Savage Attacker | **SRD** | Drive-Thru Fry-Station Veteran (Savage Attacker) |
| Skilled | **SRD** | Tech-Support Jack-of-All-Trades (Skilled) |
| Crafter | **non-SRD** | Hot-Glue Gunslinger (Crafter) |
| Healer | **non-SRD** | Weekend CPR-Class Graduate (Healer) |
| Lucky | **non-SRD** | Scratch-Ticket Gambler (Lucky) |
| Musician | **non-SRD** | Karaoke Night Regular (Musician) |
| Tavern Brawler | **non-SRD** | HOA-Meeting Brawler (Tavern Brawler) |
| Tough | **non-SRD** | Gym Bro Who Spots at Dawn (Tough) |

**Count: 6 entries SRD (4 distinct feats: Alert, Magic Initiate x3 lists, Savage Attacker, Skilled), 6 non-SRD.**

Other background-reskins rows (the two ability-bonus picks `asi-2-1` and `asi-1-1-1`, and the starting-gear `package-a`/`package-b`) are generic mechanics and not named content: the SRD's "Parts of a Background" describes the three-ability choice and the A-or-50-GP equipment choice. Nothing to flag.

## 4. (c) One-line action per non-SRD item
Rule applied: **print SRD only; non-SRD content lives in a table appendix using our own reskin names and mechanics summaries (written by us, no copied text).** In an SRD-only printing, show only the 4 SRD backgrounds and 4 SRD Origin feats; Human's Versatile feat (spec S7) then picks from those 4.

**Non-SRD backgrounds (12)**
- **Artisan:** move to the appendix under our name "Etsy Shop Founder, Three Sales"; write our own one-line mechanics summary (ability triple, feat, 2 skills, tool); its feat Crafter is also non-SRD, so give that row its own entry too.
- **Charlatan:** appendix under "Pyramid-Scheme Boss Babe"; own mechanics summary; its feat Skilled is SRD, so only the background shell is non-SRD.
- **Entertainer:** appendix under "Wedding DJ With One Playlist"; own summary; feat Musician is non-SRD (see below).
- **Farmer:** appendix under "Farm-to-Table Influencer"; own summary; feat Tough is non-SRD.
- **Guard:** appendix under "Hospital Parking-Garage Attendant"; own summary; feat Alert is SRD.
- **Guide:** appendix under "Trailhead Guide With a Laminated Map"; own summary; feat Magic Initiate (Druid list) is SRD.
- **Hermit:** appendix under "Doomsday Prepper, Collapse Postponed"; own summary; feat Healer is non-SRD.
- **Merchant:** appendix under "Warehouse Operations Manager"; own summary; feat Lucky is non-SRD.
- **Noble:** appendix under "Trust-Fund Gallery Owner"; own summary; feat Skilled is SRD.
- **Sailor:** appendix under "Cruise-Ship Buffet Deckhand"; own summary; feat Tavern Brawler is non-SRD.
- **Scribe:** appendix under "Law-Firm Paralegal in Redline Hell"; own summary; feat Skilled is SRD.
- **Wayfarer:** appendix under "Couch-Surfing Burrito Courier"; own summary; feat Lucky is non-SRD.

**Non-SRD origin feats (6)**
- **Crafter:** appendix under "Hot-Glue Gunslinger"; own mechanics summary, no book text; needed by Artisan.
- **Healer:** appendix under "Weekend CPR-Class Graduate"; own summary; needed by Hermit. Do not confuse with the SRD Healer's Kit item.
- **Lucky:** appendix under "Scratch-Ticket Gambler"; own summary; needed by Merchant and Wayfarer.
- **Musician:** appendix under "Karaoke Night Regular"; own summary; needed by Entertainer.
- **Tavern Brawler:** appendix under "HOA-Meeting Brawler"; own summary; needed by Sailor.
- **Tough:** appendix under "Gym Bro Who Spots at Dawn"; own summary; needed by Farmer.

## 5. Cross-cutting notes for Syndicate and the Architect
1. **Printed labels:** background-reskins labels read "Our Name (5e Name)". For the 12 non-SRD backgrounds and 6 non-SRD feats the parenthetical prints the non-SRD name. In an SRD-only or print build, show our reskin name alone for those rows (names are not book text, but the project rule says non-SRD content uses our own names). Decision for Caleb.
2. **Mechanics summaries:** the chargen-5e.json lines for the non-SRD rows are written by us ("names, numbers and one-line plain effects; no book text", per its meta). Keep them our own wording in the appendix; do not paste from the 2024 PHB.
3. **Dependencies:** 7 of the 12 non-SRD backgrounds hang on a non-SRD feat (Artisan, Entertainer, Farmer, Hermit, Merchant, Sailor, Wayfarer; Merchant and Wayfarer share Lucky). The other 5 (Charlatan, Guard, Guide, Noble, Scribe) use an SRD feat.
4. **Attribution:** printing any SRD 5.2.1 content needs the CC-BY attribution statement quoted on p. 1 of the SRD (Core Appendix D already covers this).
5. **Nothing in this audit changes a file in /workspace/dcc-campaign or tables.** background-reskins.json is unchanged.
