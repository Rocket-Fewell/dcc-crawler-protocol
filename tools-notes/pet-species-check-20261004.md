# Pet species check: tables/pet-species.json vs SRD 5.2.1 Beasts (CR <= 1/4)

Date: 2026-10-04 | Checked: `tables/pet-species.json` v0.1.0 (51 species, 22 aliases) and `rules/60-pets-companions-5e.md` v0.1.0
Result: **`tables/pet-species.json` was NOT edited.** Findings only.

Method: downloaded the official **SRD 5.2.1 PDF** (CC-BY-4.0, hosted by Wizards' partner at srd.aetherobjects.com), extracted text by column and read every stat block header (size, type, CR). Cross-checked against two web mirrors (LorePanic, OmnisGM). All three agree on every CR and type used below.

## 0. Summary

| Result | Count |
|---|---|
| Entries OK (real SRD 5.2.1 Beast, CR correct, same name) | 42 |
| Entries OK but name differs in the 2024 SRD (rename needed) | 4 |
| Entries wrong: real Beast but CR wrong | 1 (Baboon) |
| Entries wrong: not type Beast in SRD 5.2.1 | 4 (Axe Beak, Flying Snake, Giant Owl, Stirge) |
| SRD Beast CR <= 1/4 missing from file | 1 (Pteranodon, CR 1/4) |

The SRD 5.2.1 has **48 plain Beast stat blocks of CR <= 1/4** (24 at CR 0, 9 at CR 1/8, 15 at CR 1/4). The file covers 47 of them (the 4 renamed ones included) and misses Pteranodon.

## 1. Entries OK (42): real SRD 5.2.1 Beast, CR matches, name matches

CR 0: badger, bat, cat, crab, deer, eagle, frog, giant-fire-beetle, goat, hawk, hyena, jackal, lizard, octopus, owl, rat, raven, scorpion, spider, vulture, weasel (21)
CR 1/8: blood-hawk, camel, giant-crab, giant-rat, giant-weasel, mastiff, mule, pony (8)
CR 1/4: boar, constrictor-snake, draft-horse, elk, giant-badger, giant-bat, giant-centipede, giant-frog, giant-lizard, giant-wolf-spider, panther, riding-horse, wolf (13)

## 2. Entries wrong (5)

| id | In file | SRD 5.2.1 says | Why wrong | Fix |
|---|---|---|---|---|
| baboon | CR 0.125 (1/8) | Small Beast, **CR 0** | CR is wrong (Beast status and the <= 1/4 cap are fine, so it stays eligible) | Set `cr` to 0.0 |
| axe-beak | Beast CR 1/4 | Large **Monstrosity**, CR 1/4 | Not a Beast (it is in the A-Z monster section, not the Animals section) | Remove from the table. A GM can still allow it with `--override` |
| flying-snake | Beast CR 1/8 | Tiny **Monstrosity**, CR 1/8 | Not a Beast in 5.2.1 | Remove. Plain Venomous Snake (CR 1/8) covers snakes |
| giant-owl | Beast CR 1/4 | Large **Celestial**, CR 1/4 | Not a Beast in 5.2.1 (Giant Eagle and Giant Elk also became Celestials, and Giant Vulture a Monstrosity; none are on the file anyway) | Remove. Plain Owl (CR 0) is the legal owl |
| stirge | Beast CR 1/8 | Tiny **Monstrosity**, CR 1/8 (SRD p. 329-330) | Not a Beast | Remove |

Caution for the Architect: `state.py` (`_species_lookup`, around line 1120 and the REFUSED message around line 1222) accepts exactly what is in this table. Until it is corrected, `pet add --species axe-beak|flying-snake|giant-owl|stirge` is accepted without `--override` even though none is an SRD Beast.

## 3. Name differences in the 2024 SRD (entries that are legal Beasts under a new name)

| In file (id / name) | SRD 5.2.1 name | CR | Note |
|---|---|---|---|
| quipper / Quipper | **Piranha** | 0 | Tiny Beast. Aquatic |
| sea-horse / Sea Horse | **Seahorse** (one word) | 0 | Tiny Beast. Aquatic |
| poisonous-snake / Poisonous Snake | **Venomous Snake** | 1/8 | Tiny Beast |
| giant-poisonous-snake / Giant Poisonous Snake | **Giant Venomous Snake** | 1/4 | Medium Beast |

Suggested fix: rename `name` and `id` to the 2024 names and add the old names as aliases (`quipper`, `sea-horse`, `poisonous-snake`, `giant-poisonous-snake`) so lookups and old notes still work. The existing aliases `snake` and `viper` point at `poisonous-snake`, so retarget them to the new id.

## 4. Entries missing (1)

| SRD 5.2.1 Beast | Size | CR | Note |
|---|---|---|---|
| **Pteranodon** | Medium Beast (Dinosaur) | **1/4** | Flying dinosaur. A GM may judge it an odd pet, but it fits the rule as written |

Everything else in the 48-creature set is already in the file (see sections 1 and 3).

Edge cases that are NOT plain CR <= 1/4 Beasts and are left out on purpose (GM `--override` only):
- Swarms (type "Swarm of Tiny Beasts"): Swarm of Bats (1/4), Swarm of Rats (1/4), Swarm of Ravens (1/4). They are swarms, not single animals.
- Giant Fly (SRD p. 222, from the Figurine of Wondrous Power: Large Beast, CR 0, XP 0) and Giant Insect (spell stat block, no CR). These are magic-item and spell stat blocks, not Animals entries.
- Dire Wolf, Warhorse, Giant Seahorse, Ape, Black Bear and others are CR 1/2 or higher, so correctly excluded.

## 5. Aliases (checked, no SRD problem)

Every alias target exists in the species list. `dog/puppy/rottweiler -> mastiff` (CR 1/8) is fine. `pony: pony` is a redundant self-alias. `bird -> hawk` and `crow -> raven` are fine. After the renames in section 3, retarget `snake` and `viper`. If axe-beak, flying-snake, giant-owl and stirge are removed, no alias is affected.

## 6. Notes on rules/60-pets-companions-5e.md

- Section 1 says "a single SRD 5.2 (2024) Beast of CR 1/4 or lower". That matches the SRD, and with the fixes above the table agrees with it.
- Section 1 also says "Any four-legged creature on the SRD Beast list qualifies". The Beast list also holds birds, fish, insects, snakes, a crab and an octopus, all of which the table includes (eagle, hawk, owl, raven, vulture, frog, octopus, piranha, seahorse, spider, scorpion, snakes...). The two statements disagree; the sentence should probably say "any non-swarm Beast". Also, Piranha and Seahorse cannot live out of water. They are legal under the rule but the GM should judge them (the rule already says the GM judges edge cases).
- The table's own `note` says "SRD 5.x ... from memory ... Syndicate to verify". That verification is this file. Once fixed, update the note and bump the version.
- Rule text lists no specific species, so nothing in it needs changing for names or CRs.

## 7. Sources used

1. **SRD 5.2.1 PDF (official text, CC-BY-4.0):** https://srd.aetherobjects.com/AE-EDC-SRD_CC_v5.2.1.pdf (364 pages). Animals section pp. 344-364, monster A-Z section pp. ~256-343 (Axe Beak p. 260, Stirge pp. 329-330), Giant Fly p. 222. Primary source for every type and CR above.
2. **LorePanic Beast list (mirror of 5.2.1):** https://lorepanic.com/bestiary/type/beast. Counts 84 Beasts (24 at CR 0, 9 at CR 1/8, 15 at CR 1/4), which matches my count. Lists Pteranodon at CR 1/4, Piranha, Seahorse, Venomous Snake and Giant Venomous Snake.
3. **OmnisGM SRD 5.2 CR 0 animals:** https://rules.omnisgm.com/en/dnd/srd-5.2/animals/cr/0/. 24 CR 0 Beasts including Baboon (CR 0), Piranha and Seahorse.
4. **Fantasy Grounds SRD 5.2.1 Animals library:** https://www.fantasygrounds.com/library/5e/dd-srd-5-2-1/animals. Spot check only; its search snippet shows a Giant Eagle as a Medium Beast CR 1/8, which disagrees with the official PDF (Large Celestial, CR 1) and looks like older-edition data. The PDF wins.
5. D&D Beyond free-rules Creature Stat Blocks page (fetched, read only for spot checks).

Local copy used for the extraction: `/workspace/srdcheck/` on the box (srd.pdf, animals.txt).
