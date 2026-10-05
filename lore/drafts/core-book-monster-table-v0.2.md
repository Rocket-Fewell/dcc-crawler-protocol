# Core Book Chapter 12 — Monster Table v0.2
Owner: DCC Lore | Status: draft | Version: 0.2 | Updated: 2026-10-05
Summary: Monster shortlist for the human Core Rulebook. v0.2 folds Caleb house rulings on X-059/060/063/080. Companion: `drafts/core-book-monster-table-v0.2.json`.

## House rulings (2026-10-05 CT)
1. **X-059 Krakaren Clone** — Neighborhood Boss; READY (`cmm-047`). Closer X-081 / M-762.
2. **X-060 Grub pupa** — Timer end → Brindled Vespas; early destroy → convulsing half-formed creatures; READY (`cmm-043`). Closer X-082 / M-763.
3. **X-063 Shambling Acid Impaler** — Fielded on **Floor 3** as CANON-RUMOR; Giant Lizard + acid spit; READY (`cmm-054`). Closer X-083 / M-764.
4. **X-080 Rot Stickers** — Floor 1 only. Floor 2 slot = **HOUSE Fizz Grub (Hemolymph Burster)** (`cmm-055`). Closer X-084 / M-765.

## Counts
- Total: **60**
- By floor: {'1': 44, '2': 15, '3': 1}
- By tag: {'INSPIRED': 10, 'CANON': 48, 'CANON-RUMOR': 1, 'HOUSE': 1}
- By status: {'READY': 51, 'STUB-ONLY': 9}

## How to use
- Ten Floor 1 playable stubs keep exact Encounter Bot `srd_id` / CR.
- Voice: Crawlers; saferoom. No novel quotes over 25 words.

## Floor 1 — Playable Orientation Pit stubs

### Vent Rat
- **id:** `cmm-001` | **floors:** 1 | **type:** mob
- **tag:** INSPIRED | **canon_ref:** tables/canon-floor-1 hmob-vent-rat; analog M-265/M-266
- **canon-floor row:** `hmob-vent-rat`
- **status:** READY
- **SRD:** Giant Rat (`giant-rat`) | **CR** 1/8 | **XP** 25
- **mapping:** Exact Encounter Bot Floor 1 mapping (enc-d01-08 / budget z02).
- **reskin tweaks:** Poisonous bite flavor only if you also run the canon Rat; otherwise SRD Giant Rat as written.
- **flavor:** Ankle specialists from the HVAC. They hiss like the ducts are laughing at you.

### Mannequin Staff
- **id:** `cmm-002` | **floors:** 1 | **type:** mob
- **tag:** INSPIRED | **canon_ref:** tables/canon-floor-1 hmob-mannequin-staff; M-273
- **canon-floor row:** `hmob-mannequin-staff`
- **status:** READY
- **SRD:** Skeleton (`skeleton`) | **CR** 1/4 | **XP** 50
- **mapping:** Exact Encounter Bot mapping (enc-d01-11 / budget z05).
- **reskin tweaks:** Vulnerable to bludgeoning as Skeleton. Bows and staff badges, not rusted swords.
- **flavor:** Department-store smiles glued to wrong bones. The polo shirts are a war crime.

### Exit Greeter
- **id:** `cmm-003` | **floors:** 1 | **type:** mob
- **tag:** INSPIRED | **canon_ref:** tables/canon-floor-1 hmob-exit-greeter; analog M-286/M-287
- **canon-floor row:** `hmob-exit-greeter`
- **status:** READY
- **SRD:** Goblin Warrior (`goblin-warrior`) | **CR** 1/4 | **XP** 50
- **mapping:** Exact Encounter Bot mapping (enc-d01-02 / budget z07).
- **reskin tweaks:** None required beyond nameplate.
- **flavor:** Clipboard, EXIT-sign hat, customer-service voice. The ambush is the only honest part of the job.

### Exit Greeter (Trainee)
- **id:** `cmm-004` | **floors:** 1 | **type:** mob
- **tag:** INSPIRED | **canon_ref:** tables/canon-floor-1 hmob-exit-greeter-trainee
- **canon-floor row:** `hmob-exit-greeter-trainee`
- **status:** READY
- **SRD:** Goblin Minion (`goblin-minion`) | **CR** 1/8 | **XP** 25
- **mapping:** Exact Encounter Bot mapping (enc-d01-02 / budget z07).
- **reskin tweaks:** None.
- **flavor:** Same smile, worse benefits. Dies for tips the veteran will steal.

### Bruiser the Mascot (Unoccupied)
- **id:** `cmm-005` | **floors:** 1 | **type:** elite
- **tag:** INSPIRED | **canon_ref:** tables/canon-floor-1 hmob-bruiser-mascot; M-273/M-274
- **canon-floor row:** `hmob-bruiser-mascot`
- **status:** READY
- **SRD:** Animated Armor (`animated-armor`) | **CR** 1 | **XP** 200
- **mapping:** Exact Encounter Bot mapping (enc-d01-03 / budget z08).
- **reskin tweaks:** Describe padded foam shell; stats remain Animated Armor.
- **flavor:** Empty pit-bull costume with opinions. Foam outside, felony inside.

### Lanyard Blade
- **id:** `cmm-006` | **floors:** 1 | **type:** mob
- **tag:** INSPIRED | **canon_ref:** tables/canon-floor-1 hmob-lanyard-blade
- **canon-floor row:** `hmob-lanyard-blade`
- **status:** READY
- **SRD:** Animated Flying Sword (`animated-flying-sword`) | **CR** 1/4 | **XP** 50
- **mapping:** Exact Encounter Bot mapping (enc-d01-03 / budget z08).
- **reskin tweaks:** Cosmetic: plastic badge on a razor lanyard.
- **flavor:** An ID badge that files itself in your arteries. HR finally found a use for compliance.

### Ceiling Tick
- **id:** `cmm-007` | **floors:** 1 | **type:** mob
- **tag:** INSPIRED | **canon_ref:** tables/canon-floor-1 hmob-ceiling-tick
- **canon-floor row:** `hmob-ceiling-tick`
- **status:** READY
- **SRD:** Stirge (`stirge`) | **CR** 1/8 | **XP** 25
- **mapping:** Exact Encounter Bot mapping (wandering / Days 2–4).
- **reskin tweaks:** None beyond nameplate. Cannot enter saferooms.
- **flavor:** Ceiling girlfriend energy. Attaches, drinks, reviews your hemoglobin.

### Usher
- **id:** `cmm-008` | **floors:** 1 | **type:** mob
- **tag:** INSPIRED | **canon_ref:** tables/canon-floor-1 hmob-usher
- **canon-floor row:** `hmob-usher`
- **status:** READY
- **SRD:** Skeleton (`skeleton`) | **CR** 1/4 | **XP** 50
- **mapping:** Exact Encounter Bot mapping (enc-d04-03 / enc-d05-03 / budget z10).
- **reskin tweaks:** Flashlights instead of shortswords if you want the bit; damage can stay piercing.
- **flavor:** Flashlight, hush tone, zero mercy. Shows you to your seats and then to your grave.

### Dean Thudd, Head of Orientation
- **id:** `cmm-009` | **floors:** 1 | **type:** neighborhood boss
- **tag:** INSPIRED | **canon_ref:** tables/canon-floor-1 hboss-dean-thudd
- **canon-floor row:** `hboss-dean-thudd`
- **status:** READY
- **SRD:** Ogre (`ogre`) | **CR** 2 | **XP** 450
- **mapping:** Exact Encounter Bot mapping Variant A (enc-d05-03 / budget z10). House stage boss.
- **reskin tweaks:** Greatclub as podium/flagpole. One telegraphed AoE "class photo" slam (house telegraph; same damage budget as Ogre greatclub).
- **flavor:** Oversized academic who flunks Crawlers with a podium. The group-photo attack is telegraphed and still somehow your fault.

### Dean Thudd (JV)
- **id:** `cmm-010` | **floors:** 1 | **type:** neighborhood boss
- **tag:** INSPIRED | **canon_ref:** tables/canon-floor-1 hboss-dean-thudd (Variant B)
- **canon-floor row:** `hboss-dean-thudd`
- **status:** READY
- **SRD:** Bugbear Warrior (`bugbear-warrior`) | **CR** 1 | **XP** 200
- **mapping:** Exact Encounter Bot mapping Variant B for level-1 dash parties (enc-d05-03).
- **reskin tweaks:** Use instead of Ogre Dean when the party is still level 1.
- **flavor:** Same tenure, smaller grant. Still wants you off the stage.

## Floor 1 — Canon roster

### Rat
- **id:** `cmm-011` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-265; M-266
- **canon-floor row:** `mob-rat`
- **status:** READY
- **SRD:** Giant Rat (`giant-rat`) | **CR** 1/8 | **XP** 25
- **mapping:** House mapping (same SRD family as Vent Rat; this is the floor-wide janitor).
- **reskin tweaks:** Add poison on bite (DC 10 Con, 1d4 poison) to match poisonous-bite lore; pack tactics as SRD.
- **flavor:** Janitors with teeth. They eat the dead because nobody else applied for the job.

### Scatterer
- **id:** `cmm-012` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-267
- **canon-floor row:** `mob-scatterer`
- **status:** READY
- **SRD:** Swarm of Insects (`swarm-of-insects`) | **CR** 1/2 | **XP** 100
- **mapping:** House mapping: bread-loaf cockroach swarm ≈ insect swarm.
- **reskin tweaks:** Reskin visuals to cockroaches; keep swarm resistances and bite.
- **flavor:** Cockroaches the size of lunch meat with union density. Step on one, interview the rest.

### Scatterer Brood Guardian
- **id:** `cmm-013` | **floors:** 1 | **type:** elite
- **tag:** CANON | **canon_ref:** M-268
- **canon-floor row:** `mob-scatterer-brood-guardian`
- **status:** READY
- **SRD:** Giant Centipede (`giant-centipede`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping: cat-sized charging cockroach ≈ giant centipede.
- **reskin tweaks:** Poison bite as centipede; describe as oversized cockroach.
- **flavor:** The middle manager of the nest. Faster, meaner, still a bug.

### The Hoarder
- **id:** `cmm-014` | **floors:** 1 | **type:** neighborhood boss
- **tag:** CANON | **canon_ref:** B-001; M-269; M-271
- **canon-floor row:** `boss-hoarder`
- **status:** READY
- **SRD:** Ogre (`ogre`) | **CR** 2 | **XP** 450
- **mapping:** House mapping. Signature: vomit Scatterers; choke the mouth to stop the flow.
- **reskin tweaks:** Once per round while mouth free: vomit 1 Scatterer swarm (or 1d4 individual cockroach tokens). Blocking/stuffing the mouth stops spawns. Door seals the arena.
- **flavor:** Garbage troll with a recycling policy written in bile. One trick, one weakness, infinite trash.

### Goblin
- **id:** `cmm-015` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-286; M-287
- **canon-floor row:** `mob-goblin`
- **status:** READY
- **SRD:** Goblin Warrior (`goblin-warrior`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping (same SRD as Exit Greeter; this is the clan version).
- **reskin tweaks:** Clubs over scimitars if you want the pineapple bit; damage stays bludgeoning.
- **flavor:** Pineapple clubs and collective revenge. Kill one, interview the whole HOA.

### Goblin Engineer
- **id:** `cmm-016` | **floors:** 1 | **type:** elite
- **tag:** CANON | **canon_ref:** M-288
- **canon-floor row:** `mob-goblin-engineer`
- **status:** READY
- **SRD:** Goblin Warrior (`goblin-warrior`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping + operator trait.
- **reskin tweaks:** While piloting the Murder Dozer, use the Dozer entry instead. On foot: Goblin Warrior with thieves' tools flavor.
- **flavor:** Weird hat, worse OSHA record. If the Murder Dozer is rolling, this is who put the key in.

### Goblin Bomb Bard
- **id:** `cmm-017` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-290; I-013
- **canon-floor row:** `mob-goblin-bomb-bard`
- **status:** READY
- **SRD:** Goblin Warrior (`goblin-warrior`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping; ranged explosives.
- **reskin tweaks:** Replace shortbow with thrown Goblin Dynamite / alchemist's fire (same attack bonus). Explosives inert in saferooms.
- **flavor:** Percussion section for people who hate buildings. Sparking bombs, zero encore.

### Goblin Shamanka
- **id:** `cmm-018` | **floors:** 1 | **type:** elite
- **tag:** CANON | **canon_ref:** M-291
- **canon-floor row:** `mob-goblin-shamanka`
- **status:** READY
- **SRD:** Priest (`priest`) | **CR** 2 | **XP** 450
- **mapping:** House mapping: clan caster. Priest is a judgment call for a focused-blast shaman.
- **reskin tweaks:** Swap radiant spells for fire/force blasts of equal level slots; keep CR 2 action economy. Drop if too hot for early F1 and use Goblin Warrior + 2× leveled slots instead.
- **flavor:** Clan magic with a blast radius and a god nobody invited. Loud faith, louder boom.

### Goblin Murder Dozer
- **id:** `cmm-019` | **floors:** 1 | **type:** elite
- **tag:** CANON | **canon_ref:** M-289
- **canon-floor row:** `mob-murder-dozer`
- **status:** READY
- **SRD:** Ogre (`ogre`) | **CR** 2 | **XP** 450
- **mapping:** House mapping: spiked steam juggernaut treated as a CR 2 construct chassis.
- **reskin tweaks:** Construct immunities (poison, charm, fatigue). Replace greatclub with spiked ram (same damage, bludgeoning+piercing). Trample: move through hostile spaces, Dex save DC 12 or take ram damage once per turn.
- **flavor:** Steam, spikes, and a recruitment poster for roadkill. It does not stop for pedestrians.

### Goblin War Chieftain
- **id:** `cmm-020` | **floors:** 1 | **type:** neighborhood boss
- **tag:** CANON | **canon_ref:** M-293
- **canon-floor row:** `boss-goblin-war-chieftain`
- **status:** READY
- **SRD:** Hobgoblin Captain (`hobgoblin-captain`) | **CR** 3 | **XP** 700
- **mapping:** House mapping. Canon win is clever explosives (munitions cart), not a fair duel.
- **reskin tweaks:** Keep Hobgoblin Captain chassis. Reward cart-of-explosives plans: environmental kill should be possible without a full HP slog.
- **flavor:** Clan boss who expects a duel and deserves a munitions accident. Cleverness is the real DPS.

### Bad Llama
- **id:** `cmm-021` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-295; M-296
- **canon-floor row:** `mob-bad-llama`
- **status:** READY
- **SRD:** Giant Goat (`giant-goat`) | **CR** 1/2 | **XP** 100
- **mapping:** House mapping (confidence WIKI-ONLY on lore row; still on canon-floor-1). Lava spit = fire damage.
- **reskin tweaks:** Replace charge gore once per short rest with a spit: ranged 30 ft, +4 to hit, 2d6 fire. Weak-point: critical hits or aimed shots to the pouch (called shot / vulnerable) deal max weapon die once per round.
- **flavor:** Horse-sized, meth-adjacent, lava-spitting livestock. Aim for the throat pouch like you mean it.

### Rot Sticker
- **id:** `cmm-022` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-297; M-298
- **canon-floor row:** `mob-rot-sticker`
- **status:** READY
- **SRD:** Stirge (`stirge`) | **CR** 1/8 | **XP** 25
- **mapping:** House mapping: wall-running kamikaze ravioli.
- **reskin tweaks:** Climb speed 30 ft. On death while attached: 1d6 acid splash to the host (house death burst).
- **flavor:** Pasta-shaped suicide with legs. Climbs walls, latches on, makes a point.

### Troglodyte Basher
- **id:** `cmm-023` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-301
- **canon-floor row:** `mob-troglodyte-basher`
- **status:** READY
- **SRD:** Troglodyte (`troglodyte`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping (SRD Troglodyte).
- **reskin tweaks:** Keep stench; clubs/weights as melee.
- **flavor:** Gym bro lizard with a weight-room smell. Hits like a kettlebell with daddy issues.

### Troglodyte Virtuoso
- **id:** `cmm-024` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-300
- **canon-floor row:** `mob-troglodyte-virtuoso`
- **status:** READY
- **SRD:** Troglodyte (`troglodyte`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping + reach poison tongue.
- **reskin tweaks:** Add 10-ft tongue attack: +4, 1d4 piercing + DC 11 Con or poisoned until end of next turn. Slightly lower HP (−4) to pay for it.
- **flavor:** Tiny conductor energy, whip tongue, poison encore. Reach is rude.

### Troglodyte Pygmy
- **id:** `cmm-025` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-302
- **canon-floor row:** `mob-troglodyte-pygmy`
- **status:** READY
- **SRD:** Giant Rat (`giant-rat`) | **CR** 1/8 | **XP** 25
- **mapping:** House mapping: tiny leaping biter on Giant Rat chassis.
- **reskin tweaks:** Describe as Tiny troglodyte; jump 20 ft as part of move without long-jump check once per turn.
- **flavor:** Pocket lizard. Leaps, bites, ruins personal space.

### The Juicer
- **id:** `cmm-026` | **floors:** 1 | **type:** neighborhood boss
- **tag:** CANON | **canon_ref:** B-002; M-304; M-305
- **canon-floor row:** `boss-juicer`
- **status:** READY
- **SRD:** Ogre (`ogre`) | **CR** 2 | **XP** 450
- **mapping:** House mapping. Burning free weights; veins are the tell.
- **reskin tweaks:** Replace javelin with flaming plate: ranged 30/60, +6, 2d6 bludgeoning + 1d6 fire. Called shots to strained veins: once per round a hit can impose disadvantage on his next attack (house). Arena doors seal; red lights; support trogs poison/tie up.
- **flavor:** Steroid lizard who benches flaming plates. Hit the veins before he hits your resume.

### Ball of Swine
- **id:** `cmm-027` | **floors:** 1 | **type:** borough boss
- **tag:** CANON | **canon_ref:** B-003; M-307; M-308
- **canon-floor row:** `boss-ball-of-swine`
- **status:** READY
- **SRD:** Ogre (`ogre`) | **CR** 2 | **XP** 450
- **mapping:** House mapping for the fused rolling formation; pop it to spill Tusklings.
- **reskin tweaks:** Single HP pool (Ogre). Move + slam as trample (Dex DC 13, 2d8 bludgeoning). At 0 HP, splits into remaining Tusklings (see below) instead of dying clean.
- **flavor:** A rolling HOA of pig aristocrats. One attack pattern: become traffic.

### Tuskling Knight
- **id:** `cmm-028` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-311; M-324
- **canon-floor row:** `mob-tuskling-knight`
- **status:** READY
- **SRD:** Boar (`boar`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping: weak tuxedo pig once the ball pops.
- **reskin tweaks:** Drop charge if you want them pathetic post-ball; keep gore.
- **flavor:** Tuxedo, tusks, no weapons, all entitlement. Catastrophic only in bulk.

### Tuskling Courtesan
- **id:** `cmm-029` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-311
- **canon-floor row:** `mob-tuskling-courtesan`
- **status:** READY
- **SRD:** Boar (`boar`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping; slightly tougher than Knight.
- **reskin tweaks:** +5 HP over Knight.
- **flavor:** Gowned pig politics. Slightly more HP, same bad attitude.

### Tuskling Dominatrix
- **id:** `cmm-030` | **floors:** 1 | **type:** elite
- **tag:** CANON | **canon_ref:** B-003
- **canon-floor row:** `mob-tuskling-dominatrix`
- **status:** READY
- **SRD:** Boar (`boar`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping; last pig standing / formation leader.
- **reskin tweaks:** +10 HP; pack leader: allies within 10 ft get +1 to attack while she lives.
- **flavor:** Last Tuskling with a management title. Still a pig in boots.

### Chilly Goat
- **id:** `cmm-031` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-318
- **canon-floor row:** `mob-chilly-goat`
- **status:** READY
- **SRD:** Giant Goat (`giant-goat`) | **CR** 1/2 | **XP** 100
- **mapping:** House mapping.
- **reskin tweaks:** Bite instead of horns if you want fangs; same damage, piercing.
- **flavor:** White goat, fang mouth, winter branding. Bites like a blizzard with hooves.

### Scat Thug
- **id:** `cmm-032` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-319
- **canon-floor row:** `mob-scat-thug`
- **status:** READY
- **SRD:** Goblin Warrior (`goblin-warrior`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping: raccoon-headed spear goblin-tier.
- **reskin tweaks:** Spear stats; otherwise Goblin Warrior.
- **flavor:** Raccoon face, spear, goblin pay grade. Trash-panda union enforcer.

### Green Slime
- **id:** `cmm-033` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-320
- **canon-floor row:** `mob-green-slime`
- **status:** READY
- **SRD:** Gray Ooze (`gray-ooze`) | **CR** 1/2 | **XP** 100
- **mapping:** House mapping (acidic cloth-dissolving blob).
- **reskin tweaks:** Emphasize acid; corrodes nonmagical armor on hit as Gray Ooze.
- **flavor:** Laundry day from hell. Dissolves cloth, skin, and optimism.

### Vine Creeper
- **id:** `cmm-034` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-321
- **canon-floor row:** `mob-vine-creeper`
- **status:** READY
- **SRD:** Constrictor Snake (`constrictor-snake`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping: pod-burst plant that swallows ≈ constrictor.
- **reskin tweaks:** Plant type; describe constriction as vine wrap. Optional: emerge from a pod as surprise.
- **flavor:** Thorny plant that leaps from pods and tries to wear you as fertilizer.

### Spine-Covered Wolf
- **id:** `cmm-035` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-316
- **canon-floor row:** `mob-spine-wolf`
- **status:** READY
- **SRD:** Dire Wolf (`dire-wolf`) | **CR** 1 | **XP** 200
- **mapping:** House mapping (seen early; thin detail).
- **reskin tweaks:** Melee attackers who hit it take 1d4 piercing (house spines).
- **flavor:** Wolf that lost an argument with a cactus. The spines are not decorative.

### Fire Blob
- **id:** `cmm-036` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-316
- **canon-floor row:** `mob-fire-blob`
- **status:** READY
- **SRD:** Magmin (`magmin`) | **CR** 1/2 | **XP** 100
- **mapping:** House mapping.
- **reskin tweaks:** Keep Magmin ignition; drop death burst intensity if packs feel mean.
- **flavor:** Shapeless flaming mood. Hugs are a war crime.

### Floating Stingray
- **id:** `cmm-037` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-316
- **canon-floor row:** `mob-floating-stingray`
- **status:** READY
- **SRD:** Giant Bat (`giant-bat`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping + Magic Missile eye-stalks.
- **reskin tweaks:** Fly speed; once per turn cast magic missile at 1st level (force) instead of bite when it can see a target.
- **flavor:** Hover-ray with eye-stalks that file Magic Missiles like expense reports.

### Floating Crystal
- **id:** `cmm-038` | **floors:** 1 | **type:** neighborhood boss
- **tag:** CANON | **canon_ref:** M-313
- **canon-floor row:** `boss-floating-crystal`
- **status:** STUB-ONLY
- **mapping:** No fight description captured — do not invent attacks for print beyond a placeholder.
- **flavor:** Neighborhood boss that looks like a hovering crystal. The ledger has the nameplate, not the fight.

### Street Preacher
- **id:** `cmm-039` | **floors:** 1 | **type:** borough boss
- **tag:** CANON | **canon_ref:** M-314
- **canon-floor row:** `boss-street-preacher`
- **status:** STUB-ONLY
- **mapping:** Patched upward in tier; no fight description in canon-floor-1.
- **flavor:** Promoted by patch, still waiting on a sermon script. Nameplate yes, choreography no.

### Blender Fiend (Patched Out)
- **id:** `cmm-040` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-315
- **canon-floor row:** `mob-blender-fiend`
- **status:** STUB-ONLY
- **mapping:** Do not field on Floor 1. Historical/patch note only.
- **flavor:** Collective mob the System yanked after a mass kill. Rumor fuel, not a fair fight.

### Axebeak
- **id:** `cmm-057` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-323
- **canon-floor row:** `mob-axebeak`
- **status:** STUB-ONLY
- **mapping:** Name only in ledger. Tentative unused map: Giant Eagle or Warhorse if you must run it.
- **flavor:** Named on the roster. Personality: TBD by whoever survives meeting one.

### Floating Eyeball
- **id:** `cmm-058` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-316
- **canon-floor row:** `mob-floating-eyeball`
- **status:** STUB-ONLY
- **mapping:** No combat kit captured. Optional unused map: Flumph or Specter without drain.
- **flavor:** Drifting eyeballs from the cold open montage. Creepy wallpaper with agency.

### Three-Headed Baboon
- **id:** `cmm-059` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-317
- **canon-floor row:** `mob-three-headed-baboon`
- **status:** STUB-ONLY
- **mapping:** No kit. Optional unused map: Ape with Multiattack ×3 at reduced damage.
- **flavor:** Later-recap cameo. Three heads, one bad decision tree.

### Eggplant with Teeth
- **id:** `cmm-060` | **floors:** 1 | **type:** mob
- **tag:** CANON | **canon_ref:** M-317
- **canon-floor row:** `mob-toothy-eggplant`
- **status:** STUB-ONLY
- **mapping:** No kit. Optional unused map: Awakened Shrub with a bite.
- **flavor:** Produce aisle horror. Chewable metaphor for the tutorial.

## Floor 2 — Canon + house

### Brindle Grub
- **id:** `cmm-041` | **floors:** 2 | **type:** mob
- **tag:** CANON | **canon_ref:** M-384; M-385; M-387; M-388; M-389
- **canon-floor row:** `mob2-brindle-grub`
- **status:** READY
- **SRD:** Giant Centipede (`giant-centipede`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping: fuzzy corpse-eating worm.
- **reskin tweaks:** Remove centipede poison or keep mild; death: harmless goo + optional hemolymph reagent drop.
- **flavor:** Cat-sized janitor worm. Eats corpses, squeaks, bursts into goo, tips the alchemist.

### Cow-Tailed Brindle Grub
- **id:** `cmm-042` | **floors:** 2 | **type:** mob
- **tag:** CANON | **canon_ref:** M-390
- **canon-floor row:** `mob2-cow-tailed-grub`
- **status:** READY
- **SRD:** Giant Wolf Spider (`giant-wolf-spider`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping (WIKI-ONLY row; pre-pupa form).
- **reskin tweaks:** Cosmetic tails; no web needed.
- **flavor:** Final soft form before the sac. Whip tails for show, teeth for payroll.

### Grub Pupa
- **id:** `cmm-043` | **floors:** 2 | **type:** elite
- **tag:** CANON | **canon_ref:** M-391; M-392; M-393; M-394; M-469
- **canon-floor row:** `mob2-grub-pupa`
- **status:** READY | **conflict:** X-060; closed by X-082 / M-763
- **SRD:** Ochre Jelly (`ochre-jelly`) | **CR** 2 | **XP** 450
- **mapping:** House mapping (Ochre Jelly sac). Caleb 2026-10-05 closes X-060.
- **reskin tweaks:** Immobile; HP as Ochre Jelly. Timer end: release Brindled Vespas. Early destroy by Crawlers: convulsing half-formed creatures spill out (not Vespas).
- **flavor:** Human-sized wet timer with party lights. Wait it out and meet Vespas. Pop it early and meet unfinished nightmares.

### Brindled Vespa
- **id:** `cmm-044` | **floors:** 2 | **type:** mob
- **tag:** CANON | **canon_ref:** M-393; M-395; M-397; M-499
- **canon-floor row:** `mob2-brindled-vespa`
- **status:** READY
- **SRD:** Giant Wasp (`giant-wasp`) | **CR** 1/2 | **XP** 100
- **mapping:** House mapping; population halved by patch.
- **reskin tweaks:** Swap poison sting damage type to acid (same dice) or add 1d4 acid on hit.
- **flavor:** Hornet graduation ceremony. Acid spit included. Population was cut and they are still rude.

### Unvaccinated Clurichaun Rev-Up Consultant
- **id:** `cmm-045` | **floors:** 2 | **type:** mob
- **tag:** CANON | **canon_ref:** M-432; M-433; M-434; M-435; M-436; M-437
- **canon-floor row:** `mob2-clurichaun`
- **status:** READY
- **SRD:** Goblin Warrior (`goblin-warrior`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping (WIKI-ONLY confidence). Contact Taint.
- **reskin tweaks:** Speed 40 ft. On melee hit or start grappling: target cannot regain HP for 5 minutes (Taint). Corpses ooze; touching them refreshes Taint.
- **flavor:** Runny-nosed fairy cousin in green overalls. Slingshot, grapple, and a five-minute healing ban called the Taint.

### Laminak Rev-Up Consultant Elite
- **id:** `cmm-046` | **floors:** 2 | **type:** elite
- **tag:** CANON | **canon_ref:** M-428; M-438; M-439; M-440; M-441
- **canon-floor row:** `mob2-laminak`
- **status:** READY
- **SRD:** Sprite (`sprite`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping: crow-sized winged soccer-mom fairy.
- **reskin tweaks:** Replace shortbow with magic missile (1st level) 2/day. Resistance to necrotic/"health-seeping" if you track Taint-style drains.
- **flavor:** Leaf pantsuit, Magic Missile, MLM brainworms. Believes Floor 3 is a promotion.

### Krakaren Clone (Second Floor)
- **id:** `cmm-047` | **floors:** 2 | **type:** neighborhood boss
- **tag:** CANON | **canon_ref:** B-004; M-442; M-443; M-444; M-445; M-446; M-447; M-450; M-452; M-709
- **canon-floor row:** `boss2-krakaren-clone`
- **status:** READY | **conflict:** X-059; closed by X-081 / M-762
- **SRD:** Chuul (`chuul`) | **CR** 4 | **XP** 1100
- **mapping:** House mapping (Chuul). Caleb 2026-10-05: Neighborhood Boss (closes X-059).
- **reskin tweaks:** Mostly stationary. Multiattack tentacles; on hit apply Taint. Aura/mist: Con save or catch Vigorous Measles (house disease: fever + disadvantage on checks until cured). Bursts through walls to start.
- **flavor:** Immobile octopus with screaming mouth-tentacles, snot, and measles mist. Nameplate insists it is a copy. At least three exist. Neighborhood Boss at this table.

### Danger Dingo
- **id:** `cmm-048` | **floors:** 2 | **type:** mob
- **tag:** CANON | **canon_ref:** M-407; M-408; M-410; M-411
- **canon-floor row:** `mob2-danger-dingo`
- **status:** READY
- **SRD:** Dire Wolf (`dire-wolf`) | **CR** 1 | **XP** 200
- **mapping:** House mapping (WIKI-ONLY). Pet biscuit can flip hostility in the pound.
- **reskin tweaks:** Caged dingoes: indifferent after a Pet Biscuit (M-410). Ridden dingoes act on kobold rider initiative.
- **flavor:** Mastiff-sized, corpse-paint face, kobold optional. Feed the caged ones a biscuit and rewrite the fight.

### Kobold Rider
- **id:** `cmm-049` | **floors:** 2 | **type:** mob
- **tag:** CANON | **canon_ref:** M-412; M-413
- **canon-floor row:** `mob2-kobold-rider`
- **status:** READY
- **SRD:** Kobold (`kobold`) | **CR** 1/8 | **XP** 25
- **mapping:** House mapping; lance charge while mounted.
- **reskin tweaks:** While mounted on a Danger Dingo, lance deals 1d12 once per charge (house); on foot use Kobold stats.
- **flavor:** Yappy chihuahua energy on a painted wolf. Feathered lance, zero impulse control.

### Ralph the Frenzied Gerbil
- **id:** `cmm-050` | **floors:** 2 | **type:** neighborhood boss
- **tag:** CANON | **canon_ref:** B-005; M-414; M-415; M-416; M-417; M-418; M-419; M-420
- **canon-floor row:** `boss2-ralph`
- **status:** READY
- **SRD:** Giant Hyena (`giant-hyena`) | **CR** 1 | **XP** 200
- **mapping:** House mapping (WIKI-ONLY). Cute until the jaw unhinges; survives being swallowed.
- **reskin tweaks:** Bite; if swallowed by a dingo/ally beast, reappears from inside after 1 round at half HP instead of dying (house).
- **flavor:** Champion pit gerbil. Adorable. Mouth opens like a luggage fault. Being eaten is a commute.

### Mind Horror
- **id:** `cmm-051` | **floors:** 2 | **type:** mob
- **tag:** CANON | **canon_ref:** M-401; M-402; M-403; M-404; M-405
- **canon-floor row:** `mob2-mind-horror`
- **status:** READY
- **SRD:** Specter (`specter`) | **CR** 1 | **XP** 200
- **mapping:** House mapping: floating jam-filled brain; psychic headache scales with low Int.
- **reskin tweaks:** Replace life drain with psychic: DC 12 Int save or 2d6 psychic and speed −10 ft until end of next turn. Creatures with Int 16+ auto-succeed. Fly/hover; low physical damage.
- **flavor:** Slow kickball full of thoughts you did not order. High Intelligence shrugs; everyone else gets a migraine with teeth.

### Giant Blimp (Meadow Lark)
- **id:** `cmm-052` | **floors:** 2 | **type:** neighborhood boss
- **tag:** CANON | **canon_ref:** M-477; M-478; M-707; M-708
- **canon-floor row:** `boss2-blimp`
- **status:** STUB-ONLY | **conflict:** rb-03
- **mapping:** No attack, AI text, or chamber write-up (backlog rb-03). Do not invent a full kit for Core print yet.
- **flavor:** Warehouse blimp boss the Meadow Lark crew sniped before it left the garage. Wood later became a float frame.

### Satan's Lil' Hedgehogs
- **id:** `cmm-053` | **floors:** 2 | **type:** mob
- **tag:** CANON | **canon_ref:** M-382; M-383
- **canon-floor row:** `mob2-hedgehog`
- **status:** STUB-ONLY
- **mapping:** Do not field on Floor 2 after the relocation announcement (~4 d 17 h before collapse).
- **flavor:** Armor-piercing quills with a cute name. Seeded, then patched to a deeper floor.

### Rage Elemental
- **id:** `cmm-056` | **floors:** 2 | **type:** floor boss
- **tag:** CANON | **canon_ref:** B-029; M-461..M-470
- **canon-floor row:** `boss2-rage-elemental`
- **status:** READY
- **SRD:** Air Elemental (`air-elemental`) | **CR** 5 | **XP** 1800
- **mapping:** House mapping for the bathroom-penalty smoke horror. Summoned, not a random wanderer.
- **reskin tweaks:** Resistance to nonmagical weapons emphasized. Fire damage slows regeneration (house: no regen on any turn it took fire). Once per fight: reverse gravity in a 30-ft cylinder for 1 round (Str save DC 15). Lure into stairwell holes works.
- **flavor:** Fifteen feet of black-purple smoke, obsidian claws, horned skull. Arrows are opinions. Peeing outside is how you cast it.

### Fizz Grub (Hemolymph Burster)
- **id:** `cmm-055` | **floors:** 2 | **type:** mob
- **tag:** HOUSE
- **status:** READY | **conflict:** X-080; closed by X-084 / M-765
- **SRD:** Stirge (`stirge`) | **CR** 1/8 | **XP** 25
- **mapping:** HOUSE. Fills the cheap swarming-exploder slot Rot Stickers wrongly listed on F2 (X-080 / M-765). Not canon.
- **reskin tweaks:** Climb 30 ft. Latch as Stirge blood drain, but on death while attached: 1d6 acid (hemolymph) to the host. Soft grub body; Floor 2 janitor-adjacent.
- **flavor:** Thumb-sized soft grubs that mistake Crawlers for corpses. They latch, fizz, and pop into hot hemolymph. Floor 2's answer to ravioli terrorism — without stealing Floor 1's Rot Stickers.

## Floor 3 — Placed rumor (house)

### Shambling Acid Impaler
- **id:** `cmm-054` | **floors:** 3 | **type:** mob
- **tag:** CANON-RUMOR | **canon_ref:** M-475; M-476; M-764; X-063 closed by X-083
- **canon-floor row:** `mob2-impaler → relocated F3 by house ruling`
- **status:** READY | **conflict:** X-063; closed by X-083 / M-764
- **SRD:** Giant Lizard (`giant-lizard`) | **CR** 1/4 | **XP** 50
- **mapping:** House mapping. Canon is a Mordecai warning with no confirmed F2 sighting; Caleb places it on Floor 3 as CANON-RUMOR.
- **reskin tweaks:** Hairy green four-legs. Replace bite once per turn with acid spit: ranged 30/60, +4 to hit, 2d6 acid. Climb 20 ft.
- **flavor:** Mordecai's "everywhere" headache, finally given a street address on Floor 3. Acid darts, bad hair, worse reviews.

