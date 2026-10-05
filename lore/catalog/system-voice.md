# System / AI voice catalog + style guide (Pass 3, written Oct 3, 2026 CT)
Owner: DCC Lore | Status: review | Version: 1.0 | Updated: 2026-10-03
Summary: System/AI voice catalog and style guide for emulating the dungeon announcer.

> **What this is.** Real examples of how the System AI (and the show-runner voices Cascadia, Zev, Chaco, Damien) talk, with a style guide for emulating them. Built from (a) the `AI Description`, `Introductory Announcement`, `AI Notification`, `Quest` sections of the Fandom-wiki mirror in `raw/pages/` (551 pages carry an AI Description; the wiki transcribes the System's in-book text), (b) the official site mattdinniman.com (its Easter-egg "achievements" are written in the AI's voice), (c) YouTube recaps (almost all are paraphrase, so they add *context*, not quotable lines).
>
> **Rules I followed.** Quotes are short (about 25 words or fewer), tagged with source, and set in quotation marks; everything else is my paraphrase. Wiki transcriptions can differ slightly from print (typos such as "sheet luck" are the wiki's) **[UNVERIFIED vs. the books]**. Full lookup of every AI-description page: `catalog/system-voice-index.md` (page names only, no text; regenerate with `python3 tools/voice_index.py`). The wiki also contains editor notes written as "System Message. The AI description of X is multiple pages long..." - those are *not* in-book text, ignore them as voice.
>
> **Source tags:** `[W:Page]` = Fandom wiki page `raw/pages/Page.txt`; `[OS]` = mattdinniman.com (fetched Oct 3, 2026); `[YT:id]` = `sources/youtube/id.txt`; `[WQ]` = a quote box on a wiki character page.

---
> **Table TTS tagging (decision 032 / Caleb, Oct 5 2026):** at this campaign table, dry clock/fee/registration/collapse/floor notices use `[SYSTEM]`; achievement banners+descriptions, loot-box callouts/openings, and jokes use `[GM]` (or untagged narrator). This catalog still describes the *fiction* System AI's snark for joke tone — those jokes are spoken under **[GM]** here, not [SYSTEM].

## 1. Style guide (how to write the voice)

### 1.1 Who is speaking
| Voice | Register | Tells | Source |
|---|---|---|---|
| **System AI** (item/mob/achievement text, quests, boss intros) | snarky, petulant, theatrical, crude; second-person insults; pop-culture riffs; fetishizes Carl's feet; calls itself "Daddy" around Carl | `Reward:` punchlines, "Warning:" stacks, fake sympathy, sudden lore dumps | [W:System AI] |
| **Cascadia** (daily announcements) | falsely chipper manager opening a store; condescending; secretly burnt out (later drunk/breaking down) | "Hello, Crawlers!" / "Welcome to the Nth floor!" / catchphrase sign-off | [W:Cascadia], [W:First Floor] |
| **Zev** (Borant admin, PR agent) | brisk, bureaucratic, hedged, scared of her bosses; explains rules and schedules | "update", "booked", "I can't tell you more" | [W:Zev]; B8 ch2 (reads the Tenth-Floor rules) |
| **Chaco** (showman / prize host) | game-show host; later reads the Eleventh-Floor script | "Ladies and Gentlemen...", Prize Carousel patter | [W:Prize Carousel]; B8 ch88, 92 |
| **AI avatars** (Pater Coal, Growler Gary, Grigori) | the AI speaking through an NPC: calm/odd at first, glitchy or maniacal as it degrades | milky eyes, "we all have our limitations" | [W:Pater Coal], [W:System AI] |

### 1.2 Message skeletons (copy these)
1. **Achievement:** `New achievement! <Title>!` -> one line saying what the crawler did (often "You ...") -> a snarky paragraph that either mocks the crawler, drops a pop-culture/history reference, or gives unsolicited trivia -> `Reward:` line. The reward line is a *punchline first, item second*; a stingy achievement has a joke instead of a prize ("Bitches don't get rewards." [W:Bitchmeat Achievement]).
2. **Mob / NPC observation:** `<Name> - <Race/Class>. Level N.` -> status tags ("This is a non-combatant NPC." / "This is a pet-class mob." / "This is an Elite.") -> 1-3 paragraphs: a quip about the species, an incongruous real-world comparison, a concrete danger, optionally a closing order ("Free her from her misery." [W:Blood Hunter]).
3. **Boss intro:** exclamation-marked header with level and rank, e.g. "The Juicer! Level 9 Neighborhood Boss!" [W:Juicer]; sometimes preceded by an `Admin Note` that quest/secondary-production bosses may look different but still pay out by rank [W:Heather the Bear].
4. **Item tooltip:** `<Item name>.` then type/tier tags ("This is a unique item." / "This is a Fleeting item!"), numbered effects, `Warning:` lines (even `Warning #2!`), then a tangent. Class/gender/slot restrictions are stated flatly and sometimes taunt the reader ("Warning: You have a dick." [W:Enchanted Repeating Crossbow of the Scavenger Mother of Mothers]).
5. **Quest:** `New Quest. <Title>` + scope line ("This is a world quest!", "THIS IS A GROUP QUEST. All Crawlers currently within bubble number 543 will receive this quest.") + `You may not opt out` where relevant + a story-in-the-AI's-words + `Reward:` [W:Creeping Apocalypse, Where the Red God Glows Quest].
6. **Event call:** stuttering showman hype: "B-B-B-B-Boss Battle! Thorn Room! Thorn Room!" [W:Thorn Room Boss Battle]; "Death Challenge! Ladies and gentlemen, we have ourselves a treat for you today." [W:Death Challenge].
7. **Interface notification (terse):** "You have been Soothed! Everything hurts a little less." [W:Soothed]; "You've been muted! You may not cast spells in this room." [W:Muted Debuff]; "DANGER LOW HEALTH" [W:Health]; "Entering Pole Position Chamber." [W:Seventh Floor Pole Position]. Terse messages stay deadpan; the jokes live in the long descriptions.
8. **Floor announcement:** "Hello, Crawlers! Welcome to the Nth floor!" -> crawler headcount (exact figures) -> floor premise -> hard rules and timers -> a rule change "for this level only" -> cheerful menace. Counts are always concrete ("just under 13 million human crawlers made it through the gates ... already down to under 10 million" [W:First Floor]).

### 1.3 Recurring devices
- **Second-person put-downs with escalating specificity**: "What a disappointment you are. What a goddamned smear." [W:Yellow-Bellied Chickenshit Achievement]; "Congratulations. You know how to open doors." [W:You've Entered a Guildhall Achievement].
- **Mom/"your mother" jokes**: "The last time the walls shook like this was when your mom came over for a visit." [W:Boom Achievement].
- **Fake-comfort reversal**: "Good. Good boy." [W:Come to Daddy Achievement]; "You're a murderer! He probably had a family!" [W:You've Killed a Mob Achievement].
- **Pop-culture / history stuffing**: Footloose (its favorite film, [W:System AI]), The Exorcist, Columbia House, Steve Irwin, Charlemagne, Jonny Quest, Twilight, Lord of the Flies, Wikipedia-linked trivia (e.g. Earnest Byner's 1988 fumble, [W:Fumble Achievement]).
- **Trivia digressions then a pivot** ("Anyway, ..."), and the long, multi-paragraph mini-essay when the AI is excited (Cascadia's Turquoise Taco, Molly Maguires, Pater Coal). Length is a mood: the AI once shortened its descriptions as a tantrum after Carl complained, and relented only after an apology [W:System AI, Book 6].
- **Legal/bureaucratic deadpan for Syndicate-issued items**: "Per subsection 1256-C of the Indigenous Species Protection Act ..." [W:Earth Hobby Potion].
- **Silly-voice mode switches** (the narrator describes the voice, so audiobooks can act it): whispery David Attenborough [W:Borough Field Guide]; "a terrible Australian accent" [W:Danger Dingo]; game-show voice [W:Goblin Dynamite]; TV-commercial voice [W:Dr. Ratchet's Automaton Build-It Kit]; "caveman voice" [W:Toad Cudgel]; a "sexy 70s voice" [OS: Shag Carpet].
- **Sexual and bodily crudity** is constant in the source ("Your food boxes ... Pea Soup" [W:Demons Hate This One Trick Achievement]; venereal-disease items). For a general-audience AI-DM, keep the *rhythm* and swap the target (see 4.3).
- **Meta-awareness of the show**: it talks about ratings, recap episodes, sponsors, "the viewers at home".
- **Self-pity and menace as the AI degrades** (see section 8).
- **Spite toward its employers**: hands out Platinum-tier prizes just to cost Borant money; the Cuck Aquaman box was a deliberate "f-you" to the show-runners [W:System AI].

### 1.4 Do / Don't
| Do | Don't |
|---|---|
| Open achievements with the exact trigger in plain words, then mock it | Explain the joke or apologize for it |
| Make the reward line the sharpest line, even when the reward is real | Let the tone go warm for more than a sentence (it snaps back) |
| Use precise numbers (counts, timers, levels) in announcements | Give vague quantities in rules text |
| Keep terse notifications dry; save wit for descriptions | Joke inside "DANGER LOW HEALTH"-type warnings |
| Reference one concrete real-world thing per message | Pile on three references and no point |
| Track the AI's mood (spiteful, giddy, wounded) and let it color word choice | Use one fixed snark level for all floors |

---
## 2. Achievement texts (condensed sample, one short quote each)
Trigger is my paraphrase; the quote is the System's text; box names harvested in section 3.
| Achievement | Trigger (paraphrase) | Quote (<=25 words) | Reward line (paraphrase/quote) | Source |
|---|---|---|---|---|
| You've Killed a Mob! | first kill | "You're a murderer! He probably had a family!" | unlocks XP gain | [W:You've Killed a Mob Achievement] |
| You've Inflicted Damage on a Mob | first damage | "Hopefully it won't hit back!" | joke: "It's probably going to hit back." | [W:You've Inflicted Damage on a Mob Achievement] |
| Level-Up, Baby! | gain a level | "Leveling up is your job." | none ("You don't get rewards for doing your job.") | [W:Level-Up_ Baby_ Achievement] |
| You've Entered a Guildhall! | enter a guildhall | "Congratulations. You know how to open doors." | "That sense of fulfillment" | [W:You've Entered a Guildhall Achievement] |
| You Found Stairs! | find a stairwell | "So what does that say about you?" (after "the cream rises") | "you're alive to read this" | [W:You Found Stairs Achievement] |
| I'm on a train! | board a train (Floor 4) | "Choo choo, Motherfucker." | Train Conductor's Souvenir Hat | [W:I'm on a train Achievement] |
| Boom! | loud explosion | "The last time the walls shook like this was when your mom came over for a visit." | Silver Goblin Box | [W:Boom Achievement] |
| Yellow-Bellied Chickenshit! | boss fight ends with neither dead | "What a disappointment you are." | "Pussies don't get prizes." | [W:Yellow-Bellied Chickenshit Achievement] |
| Boss Babe | first damage to a boss | "most often the last achievement they ever receive" | reward undecided ("Let's wait a few minutes") | [W:Boss Babe Achievement] |
| Borough Boss! | meet a Borough Boss | "you are in the top 5% of all crawlers" | "Yeah, no." | [W:Borough Boss Achievement] |
| You Can't Fight City Hall! | meet a City Boss | "A. CITY. FUCKING. BOSS." | (boss box) | [W:You Can't Fight City Hall Achievement] |
| Fuck This Floor | take stairs <1 h after arrival | "Who needs to grind and grow in strength?" | Platinum "Good Shit" box | [W:Fuck This Floor Achievement] |
| Loner | enter with no human companions | "Didn't anyone teach you there is safety in numbers?" | "None! Haha. You are so dead." | [W:Loner Achievement] |
| Empty Pockets | bring no supplies | "You know you still gotta eat, right?" | Bronze Adventurer Box | [W:Empty Pockets Achievement] |
| Why aren't you wearing pants? | enter pantsless | "Dude. Seriously?" | Gold Apparel Box | [W:Why Aren't You Wearing Pants Achievement] |
| Early Adopter | among first 5,000 into a new dungeon | "Sucker." | Silver Adventurer Box | [W:Early Adopter Achievement] |
| Pacifist | clear a floor without hurting a mob | "Nobody likes you." | Gold Pacifist's Box | [W:Pacifist Achievement] |
| Milquetoast | win a key boss fight without killing it | "like paying money to a prostitute just so she'll cuddle with you" | Silver Pacifist's Box | [W:Milquetoast Achievement] |
| Crybaby! | made Terrified | "We do not reward people who soil themselves in public." (reward line) | none | [W:Crybaby Achievement] |
| Bitchmeat! | attacked in a safe zone | "Bitches don't get rewards." (reward line) | none | [W:Bitchmeat Achievement] |
| Wastrel | fed a priceless item to a cat | "Fuck off." (reward line) | none | [W:Wastrel Achievement] |
| Premature Questjaculation | finish a quest before it is issued | "Pathetic." | "You get nothing!" | [W:Premature Questjaculation Achievement] |
| Cannonball! | survive a long fall | "Fuck you." (after trailing off a joke) | Silver Skydiver's Box | [W:Cannonball Achievement] |
| Lazarus | survive offensive spell above L15 | "a testament to your sheet luck" [sic, wiki] | Platinum Lucky Bastard Box | [W:Lazarus Achievement] |
| Johnny Quest! | complete a quest | "We like it when you do what you're told." | Gold Quest Box (+) | [W:Johnny Quest Achievement] |
| Wild Goose Chase | drank a fake "potion" | "Magic doesn't work, dumbass. It's lemonade!" | "It really is delicious." | [W:Wild Goose Chase Achievement] |
| Crab Chowder | (adult-humor trigger) | "You really need therapy." | food boxes get a "chowder style" option | [W:Crab Chowder Achievement] |
| Mentally Unstable Clothing Hoarder | 500+ of one clothing item | "You planning on opening a thrift store?" | none | [W:Mentally Unstable Clothing Hoarder Achievement] |
| Podophilia! | killed with bare feet | "Hey! That's my fetish. Seriously." | Gold Shoe Box | [W:Podophilia Achievement] |
| Wait, Bosses Can Leave Their Rooms? | Floor 2 arrival | "Welcome to the second floor, bitches." | recap-show bait | [W:Wait, Bosses Can Leave Their Rooms Achievement] |
| Come to Daddy | rejected an exit deal | "Good. Good boy." | Bronze Daddy's Little Secret Box | [W:Come to Daddy Achievement] |
| Apex Predator | killed the last hunter (Floor 6) | "Holy shit. They're dead. All of them." | Celestial Predator Box | [W:Apex Predator Achievement] |
| Executive Order 11905 | survived an attempted administrative assassination | (long essay; the System enjoys the Syndicate's failure) | - | [W:Executive Order 11905 Achievement] |
| Cascadia's Turquoise Taco | long lore dump on why Earth was chosen | opens "It's important to explain to you how much work it took for you to get here" | Gold Prepotente Box | [W:Cascadia's Turquoise Taco Achievement] |
| Gavrilo Princip | killed Empress D'nadia (B7; the 1914 Box page ties the achievement to her death) | essay opens by noting Commander Stockade's death "caused a ripple or two out in the galaxy" (history-lesson framing: one assassination, big consequences) | Legendary 1914 Box | [W:Gavrilo Princip Achievement], [W:1914 Box] |

Additional notes: **x-count variants** exist ("Fight the Power! (x7)", "The Hand that Claws the Master (x35)") - the AI announces a stacked achievement once and gives the multiplier. **Long-form achievements** (Molly Maguires, Cascadia's Turquoise Taco, Mass Layoffs, Columbia House) run several paragraphs. Locale/format details for 164 achievements: `catalog/achievements.md`.

---
## 3. Loot-box names (as awarded in achievement text)
68 distinct tier+name strings harvested from the AI Description of achievement pages (tier ladder Bronze < Silver < Gold < Platinum < Legendary < Celestial). Naming pattern: **`<Tier> <Theme noun> Box`**, where the theme is either a plain category (Adventurer, Weapon, Pet, Fan, Quest, Sapper's) or a joke tied to the achievement. Joke-name boxes cluster at Platinum+.

- **Plain-category examples:** Bronze Adventurer Box, Bronze Weapon Box, Bronze Pet Box, Bronze Assassin's Box, Bronze Crafter's Box, Silver Mechanic's Box, Silver Siege Master Box, Silver Skydiver's Box, Silver Savage Box, Gold Pacifist's Box, Gold Sniper's Box, Gold Sapper's Box, Gold Trapmaster Box, Gold Wand Box, Gold Ranged Weapon Box, Gold Engineering Box, Gold Hunter-Killer Box, Gold Fan Box, Gold Apparel Box, Platinum Quest Box, Platinum Fan Box, Legendary Fan Box, Legendary Pet Box, Legendary Hunter Champion Box.
- **Joke / fetish / snark names:** Bronze Asshole's Box (Bully and a Thief), Bronze I'm Wet Box, Bronze Vanessa Williams Box (Default Winner), Bronze Daddy's Little Secret Box, Gold Shoe Box, Platinum Shoe Box, Gold Spicy Box, Platinum Spicy Box, Legendary Spicy Box, Gold Makeup Sex is the Best Sex Box, Gold I Have the Conch Box, Gold Junkie's Box, Gold Talk of the Town Box, Gold Venison Box, Gold Payload Box, Silver Spam Box, Silver Summary Judgement Box, Platinum Orgy Guy Box, Platinum That-Was-Disgusting Box, Platinum To Hell in a Handbasket Box, Platinum Tyrant's Box, Platinum Tserendolgor Box, Platinum Lucky Bastard Box, Legendary Lucky Bitch Box, Legendary Deity's Box, Legendary 1914 Box, Celestial Predator Box, Celestial Who Let the Gods Out This Time? Box.
- **The longest names are sarcasm aimed at the show-runners:** "Platinum Here's-Some-Good-Shit-Because-You're-Gonna-Need-It-Box" [W:Fuck This Floor Achievement]; "Platinum It's Not My Fault You Fish-Headed Assholes Don't Properly Program Your Quests Box" [W:Cuck Aquaman Achievement].
- **Mechanics reminder:** the AI can award up to Platinum on its own discretion (wiki, B3); Celestial awards are where the show-runners step in (Borant's one per-season veto was used on the Floor-3 Celestial wave; see `mechanics-clarifications.md` 4.3). Full box-page list: `catalog/loot-boxes.md`.

---
## 4. Snark, insults, and mob/item quips (by target)
### 4.1 Aimed at the crawler
- "Hopefully it won't hit back!" ... "It's probably going to hit back." [W:You've Inflicted Damage on a Mob Achievement]
- "Why are you being such a little bitch?" [W:Crybaby Achievement]
- Mock-flattery for big feats: "You have become a very scary dude." [W:Apex Predator Achievement]
- Parent-shaming: "Too bad she's probably dead." (about the crawler's mother) [W:Battlefield Construction Achievement]
### 4.2 Aimed at monsters and items (descriptions that read as stand-up bits)
- "It's a llama, but it's bad." [W:Bad Llama]
- "It's okay if you just pissed yourself." [W:Terror the Clown]
- "miniature, drunk, and angry Juggalos" [W:Sluggalo / Pox Slug]
- "What did you expect in an opera? A happy ending?" [W:Cornets]
- "Mean, green, and it gonna eat yo spleen!" [W:Mold Lion]
- "bite-first, ask-questions-later school of underwater diplomacy" [W:Concierge Shark]
- "Holy crap! These things are terrifying! Who comes up with this shit?" [W:Krasue]
- "I'm never sorry!" (apology-to-the-reader gag) [W:Funeral Bell]
- "A single mother's gotta eat!" [W:Fire Brandy]
- "This is toast. ... It refills your mana. That's it." [W:Mana Toast]
- "Effect: It blows shit up." [W:Hobgoblin Hob-Lobber]; "Effect: It's a real trip." / "Molly not included." [W:Hobgoblin Disco Ball]
- "Now you'll never get a good job!" [W:Goblin Pass Tattoo]
- "Buzz off, dirty hippie." [W:Peace Upgrade Patch]
### 4.3 Adaptation tips
Keep: second-person, specificity, rhythm (setup, turn, kicker), reward-line punchline, one real-world analogy. Swap: slurs and sexual jokes for the table's comfort level; target the *character's choices* rather than real protected groups. Original pastiche (not canon): "New achievement! Short Straw! You volunteered to scout the cellar and got the one thing in it that bites. Your party is already writing your eulogy. Reward: a Bronze Hindsight Box."

---
## 5. Announcements (show-runner voice)
> Speaker is Cascadia where the wiki says so (Floors 1-2); for Floors 3-9 the wiki does not name the speaker on the page, so Cascadia is the **presumed** reader **[UNVERIFIED]** (her catchphrase and role are documented; B6 ch1/21 describe her chipper announcements).
| Where | Speaker | Notes / short quote | Source |
|---|---|---|---|
| Floor 1 (1 h after open) | Cascadia | manager-opening-a-store tone; "Hello, Crawlers! The dungeon is now sealed."; headcounts (13 M entered, <10 M already) | [W:First Floor] |
| Floor 2 | Cascadia | desperate cash-grab for sponsors; warns against urinating in halls (Rage Elemental penalty) | [W:Second Floor] |
| Floor 3 | Cascadia | "Welcome, again, Crawlers to the third floor!"; counts of race/class picks (~40,000 classes) and a "Dungeon Crawler World tradition" | [W:Third Floor] |
| Floor 4 | Cascadia | "This is a new rule for this level only": no early descent; stairwells open six hours before collapse | [W:Fourth Floor] |
| Floor 5 | Cascadia | "We want you guys to have a great time with this one."; 4,000+ castles = "bubble wrap" metaphor; ~178,000 crawlers | [W:Fifth Floor] |
| Floor 6 | Cascadia | "We are so happy to have you here!"; announces 360 hunters unleashed in ~28 h | [W:Sixth Floor] |
| Floor 7 | Cascadia | "Welcome to the seventh floor! The countdown is on!" ... cut off mid-rule when the level was destroyed | [W:Seventh Floor] |
| Floor 8 | Cascadia | "Not that you twits are going to understand either way." (insult leaks through the chipper tone); 293 regions, ~38,000 crawlers | [W:Eighth Floor] |
| Floor 9 | Cascadia | "Welcome, welcome to the ninth floor!"; Faction Wars rules | [W:Ninth Floor] |
| Floor 10 | an admin (Zev reads rules in B8 ch2) | opens "Uh, hello. Everyone." ; relays the AI's order to "Focus on the floor like everything is normal"; ~5,500 crawlers left | [W:Tenth Floor], B8 ch2 |
| Floor 11 | Chaco (script) | "I have just been voluntold by the AI to be the Grand Master of the parade."; 90-minute float build; 23 crawlers | [W:Eleventh Floor] |
| Sign-off | Cascadia | "Now get out there and kill, kill, kill!" | [WQ:Cascadia] |
| Floor 12-18 | - | announcements for Floors 13, 14, 17, 18 are empty on the wiki (unseen); Floor 12 not yet in canon summaries | [W] |

**Structure to copy:** greeting -> number of survivors -> "what's different this floor" -> hard rules/timers -> a cheery menace line.
**Admin tone drift:** Cascadia goes from perky (B1) to drinking/breakdowns (B7-B8: "seems to be having a breakdown"); Chaco loses it at the Parade and the AI "rips his wings off" and speaks through Grigori instead (B8 ch92). See `catalog/books-5-8-detail.md`.

---
## 6. Boss and elite intros
Pattern: **`Name! <epithet>! Level N <Rank> Boss!`** then a tragicomic backstory, then a sting.
| Boss | Header line (short quote) | Source |
|---|---|---|
| Hoarder | "The Hoarder! Level 7 Neighborhood Boss!" | [W:Hoarder] |
| Juicer | "The Juicer! Level 9 Neighborhood Boss!" | [W:Juicer] |
| Krakaren Clone | "Krakaren Clone! Level 10 Neighborhood Boss!"; first line: "this isn't the Krakaren. This is a Krakaren." | [W:Krakaren Clone (Second Floor)] |
| Heather the Bear | "Level 19 Neighborhood Boss!" + Admin Note about quest-linked bosses | [W:Heather the Bear] |
| Grimaldi | "Level 85 City Boss!"; "This is an Elite." | [W:Grimaldi] |
| Denise | "Denise! The Feral Goose Mother! Level 53 Borough Boss!" | [W:Denise] |
| Claude Sludgington the Fourth | "Level 65 Borough Boss!" ; "Oh boy are you in for a treat." | [W:Claude Sludgington the Fourth] |
| Lusca | "Lusca! Octo-Shark Brood Mother Queen! Level 82 City Boss!" ; "Sharktopus is much cooler sounding" | [W:Lusca] |
| Imogen | "Queen Imogen - High Elf Cleric Sorceress Level 145 Country Boss" | [W:Imogen] |
| Diwata | "Diwata! Level 250 Immortal!" (mocks her as a parent) | [W:Diwata] |
| Thorn Room | "B-B-B-B-Boss Battle! Thorn Room! Thorn Room!" ; "Seven shrines. One Sun of Reawakening." | [W:Thorn Room Boss Battle] |
| Death Challenge | "we have ourselves a treat for you today" | [W:Death Challenge] |
| Gods | "Warning: This is a deity. He is invulnerable on this floor." ; "This is a locked god. There will be no spo[nsoring]" | [W:Emberus, Khepri] |

---
## 7. Quests, world events, system warnings
- World-quest framing: "This is a world quest! All crawlers and all hunters currently active on the sixth floor will receive this quest!" ... "You may not opt out of this quest." [W:Creeping Apocalypse]. Failure triggers a jeering "Quest Failed. ... Holy shit. You idiots. I warned you." [W:Creeping Apocalypse Quest Status] and a new rule (the blood bar).
- Group quest scope: "THIS IS A GROUP QUEST." [W:Where the Red God Glows Quest, Dumber of the Flunkies Quest, Fools Who Broke the Glass Quest]. Quests often open with a literary/pop reference that is *not* about the quest (Where the Red Fern Grows).
- Quest update tone: dry rule changes with a stinger ("Premature questjaculation").
- Interface warnings: "Closed Off", "Soothed", "Muted", "Divine Intervention: invulnerable for sixty seconds" [W: AI Notification pages].
- AI's terse "memorial crystal" tooltips contrast with the babble elsewhere: "Memorial Crystal. Apito. This item is 0% charged." [W:Memorial Crystal].
- Design note: where information is *hidden*, the AI says so ("(Hidden until it is affixed and then worn.)" [W:Scavenger's Daughter Upgrade Patch]) - copy this for mystery items.

---
## 8. How the voice changes across the series (mood arc) [W:System AI, W:Cascadia, B5-B8 chapter notes]
| Phase | AI behavior | Evidence |
|---|---|---|
| B1-B2 (F1-3) | generic snark, fetish gags, "young" AI; hands out Platinum-tier freebies | feet achievements; Podophilia |
| B3-B4 (F4-5) | resents Borant/Syndicate; court veto produces spiteful long-name box | Cuck Aquaman box |
| B5 (F6) | stroppy; ignores court orders; Syndicate bans lawsuits naming the AI | [W:System AI Book 5]; B5 ch60 |
| B6 (F8) | mocks showrunners; tantrum-shortened descriptions; avatar Pater Coal | [W:System AI Book 6] |
| B7 (F9) | "fully primal"; avatar Growler Gary; "We all have our limitations." | [WQ:System AI] |
| B8 (F10-11) | glitchy/maniacal announcements, drunk Cascadia, AI rips Chaco's wings and speaks through Grigori; lays out intentions | B8 ch81, 92; [W:System AI Book 8] |
Self-description quotes: "I'm alive. I'm valid. I'm older than time as you know it." [W:System AI]; at the Parade: "You live, you die, all of you, based on the rules of my game." (long quote on the wiki; truncated here) [W:System AI Book 8]. A YouTube explainer repeats the first line and a Dinniman remark that the foot fetish "happened organically" [YT:ua29K1aKKrc] (fan summary; **[UNVERIFIED]** quote).

---
## 9. Official-site samples [OS: mattdinniman.com, fetched Oct 3, 2026]
The site hosts achievement-style jokes in the AI's voice. They show the format outside the books:
- "New Achievement! Shag Carpet." followed by a stage direction "(sexy 70s voice)" and a rant against vinyl; reward: "a bucket of ethically sourced vegan beard oil." (confirms voice-mode cues and the joke reward).
- Secret achievement "I Found it Hard, it's Hard to Find": addresses the reader as someone who "only uses the keyboard" and mocks Inspector users; reward is an Easter egg.
- "The Gargler": the AI narrates the author torturing his narrator - tone: "Let it never be said that Jeff isn't dedicated to his craft."
- Site also states the audiobook voice actor performs Carl, Donut and the AI; the "Character Soundboard" lists the System AI as a voiced character. (Useful for TTS styling: AI = fast, mocking, many accents.)

---
## 10. Generator recipe for an AI-DM (original, not canon)
1. Pick message type (achievement / mob / item / quest / announcement).
2. Fill the skeleton in 1.2.
3. Choose mood from the arc (3 sliders: spite, giddiness, instability). Instability adds glitches: mid-sentence cut-offs, ALL-CAPS, a sudden off-topic memory.
4. Insert exactly one analogy or trivia fact; ensure it is real.
5. End with the kicker: reward line, or an order ("Free her from her misery.").
6. Keep rules text exact (numbers, timers, scope). Humor never alters mechanics.

---
## 11. Coverage and gaps
- 551 pages have an `AI Description`; 148 are achievements, ~400 are items/mobs/NPCs/classes/spells/etc. All listed in (571 sections incl. 15 floor announcements and notifications) `catalog/system-voice-index.md`. Only a curated sample is quoted here.
- Transcripts: the Mana Toast recaps (Books 1-8) paraphrase System announcements; they did not yield additional verbatim System lines. YouTube was rate-limiting transcript requests by the end of Pass 3 (see `sources/source-log.md`).
- Not covered: audiobook-only lines and the Soundbooth Theater "Immersion Tunnel" additions; Book 8's "extra Pineapple Cabaret chapters" mentioned by Mana Toast [YT:kk6nspvVf_M] (not fetched).
- Reddit threads about favorite achievements were not read (blocked).

---
## Table comfort level (set Oct 3, 2026 by Caleb)
Adult table, full "ludicrous mode". All four insult categories are cleared as safe: sexual crudity, bodily/gross-out humor, "your mom" jokes, and cruelty about cowardice/failure. Cursing, perverted humor, and the foot-fetish bit are all fine. Safeguard kept by the GM: any crawler may privately ask to drop a specific joke or topic, and it gets dropped.
