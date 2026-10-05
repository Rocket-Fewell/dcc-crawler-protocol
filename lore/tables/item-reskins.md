# Item reskins (SRD 5.2 to flavored names)
Owner: DCC Lore | Status: draft | Version: 0.1.5 | Updated: 2026-10-04
Summary: Flavored display name and one snark line for every SRD 5.2 weapon, armor, shield, ammunition, focus, gear, pack and tool, with SRD reference prices for the Accountant. Names and flavor only.

Table version 0.1.5 (hash and history: `tables/item-reskins.version.json`, `tables/item-reskins.CHANGELOG.md`).

Source of truth: `tables/item-reskins.json` (built by `tools/reskin_build.py` from `tools/reskin_data.py`; checked by `tools/reskin_check.py`).

Display rule: show **Display Name (SRD Name)**. Names and flavor only; no 5e rule changes. Prices are SRD 5.2 reference values for the Accountant. **They always key off `srd_id`, never the display name.**

**ID scheme:** stable kebab-case `srd_id` (e.g. `quarterstaff`, `chain-mail`, `explorers-pack`), stored on the sheet; lookup by `srd_id`; fallback to `srd_name` if missing (then `legacy_names`).

Counts: weapon 38, armor 12, shield 1, ammunition 5, focus 14, gear 74, pack 7, tool 40 (total 191).

**Generic ids are category headers, not purchasable** (`resolve_to_variant: true`): `arcane-focus`, `druidic-focus`, `holy-symbol`, `artisans-tools`, `gaming-set`, `musical-instrument`. Each lists its concrete `variants`, all priced; /create and the vending wall must resolve a generic to a variant srd_id before showing or pricing it. The only other null prices are the non_srd canon items (`heal-critter-potion`, `pet-carrier`), which are purchasable and priced in credits (`price_credits_proposed`: Accountant proposal, Syndicate to confirm).

## Weapons

| srd_id | SRD name | Display name | Snark | base_price |
|---|---|---|---|---|
| `club` | Club | Table-Leg Club | Furniture, but angrier. | 1 sp |
| `dagger` | Dagger | Box Cutter | Safety first. Not yours, though. | 2 gp |
| `greatclub` | Greatclub | Fence Post With Opinions | Still has concrete on one end. Nobody asked where the other end has been. | 2 sp |
| `handaxe` | Handaxe | Hatchet From a Camping Display | The tag says 'Not For Use'. The floor disagrees. | 5 gp |
| `javelin` | Javelin | Curtain-Rod Javelin | Pointed end goes toward the problem. | 5 sp |
| `light-hammer` | Light Hammer | Claw Hammer, Borrowed Indefinitely | The neighbor wants it back. The neighbor is not on this floor. | 2 gp |
| `mace` | Mace | Crowbar-Headed Mace | Half tool, half apology. | 5 gp |
| `quarterstaff` | Quarterstaff | Duct-Taped Mop | Cleans up after you, one way or another. | 2 sp |
| `sickle` | Sickle | Garden Sickle | Please do not harvest the party. | 1 gp |
| `spear` | Spear | Broom Handle With a Kitchen Knife Taped On | Reach, courtesy of a junk drawer. | 1 gp |
| `dart` | Dart | Bar-Room Dart | Sharp, cheap, and always one short in the set. | 5 cp |
| `light-crossbow` | Light Crossbow | Nail Gun With a Homemade Stock | Workplace safety training not included. | 25 gp |
| `shortbow` | Shortbow | Compound Bow From a Sporting-Goods Display | Floor model. Sold as-is. All sales final. | 25 gp |
| `sling` | Sling | Slingshot Confiscated From a Kid | Returned to nobody. He's fine. Probably. | 1 sp |
| `battleaxe` | Battleaxe | Wood-Splitting Axe | Firewood is a state of mind. | 10 gp |
| `flail` | Flail | Chain With a Padlock On It | The lock is the weapon. The chain is moral support. | 10 gp |
| `glaive` | Glaive | Lawn Edger on a Pole | Edges everything. Including your enemies. | 20 gp |
| `greataxe` | Greataxe | Fire Axe, BREAK GLASS Sticker Intact | In case of emergency, this is the emergency. | 30 gp |
| `greatsword` | Greatsword | Sheet-Metal Slab on a Pipe Handle | Subtle, like a car door slamming. | 50 gp |
| `halberd` | Halberd | Snow-Plow Blade on a Flagpole | Municipal property. Nobody will check. | 20 gp |
| `lance` | Lance | Jousting Pole From a Renaissance Faire | Best used by someone who has recently regretted something. | 10 gp |
| `longsword` | Longsword | Sharpened Stop Sign | It said STOP. Nobody listened. | 15 gp |
| `maul` | Maul | Spiked Sledgehammer | For problems that cannot be talked down, only knocked down. | 10 gp |
| `morningstar` | Morningstar | Spiked Rebar Club | Building codes weep. | 15 gp |
| `pike` | Pike | Flagpole With a Spearhead Zip-Tied On | Patriotic and extremely poorly secured. | 5 gp |
| `rapier` | Rapier | Sharpened Curtain Rod | Fancy drapes optional. | 25 gp |
| `scimitar` | Scimitar | Curved Souvenir Machete | Bought at a gift shop. Used at a dungeon. | 25 gp |
| `shortsword` | Shortsword | Pawnshop Shortsword | Previous owner's initials still on the grip. | 10 gp |
| `trident` | Trident | Pitchfork From a Haunted Hayride | Three tines, zero customer reviews. | 5 gp |
| `warhammer` | Warhammer | Framing Hammer | Builds things. Also unbuilds them. | 15 gp |
| `war-pick` | War Pick | Roofing Pick, Gently Used | The roof was not the only thing it opened. | 5 gp |
| `whip` | Whip | Bullwhip From a Costume Shop | Comes with a hat nobody is allowed to wear. | 2 gp |
| `blowgun` | Blowgun | Pea Shooter, Industrial Strength | Surprisingly rude for a drinking straw. | 10 gp |
| `hand-crossbow` | Hand Crossbow | Staple Gun on a Pistol Grip | Binds paperwork. Binds enemies to paperwork. | 75 gp |
| `heavy-crossbow` | Heavy Crossbow | Rebar Launcher, Shop-Class Edition | The teacher gave it a C-minus and a restraining order. | 50 gp |
| `longbow` | Longbow | Big Compound Bow, Price Tag Still On | Retail value remains a mystery to everyone but the tag. | 50 gp |
| `musket` | Musket | Reenactor's Musket, Surprisingly Loaded | Historically accurate until it wasn't. | 500 gp |
| `pistol` | Pistol | Starter Pistol, Illegally Upgraded | Meant to start races. Now ends arguments. | 250 gp |

## Armor

| srd_id | SRD name | Display name | Snark | base_price |
|---|---|---|---|---|
| `padded-armor` | Padded Armor | Quilted Moving Blanket Coat | Smells like a stranger's apartment. | 5 gp |
| `leather-armor` | Leather Armor | Motorcycle Jacket | Looks great. Will not save you from asphalt, or from a goblin. | 10 gp |
| `studded-leather-armor` | Studded Leather Armor | Studded Biker Vest | Rivets for personality. | 45 gp |
| `hide-armor` | Hide Armor | Taxidermy Rug Poncho | The bear is not consenting but is not objecting either. | 10 gp |
| `chain-shirt` | Chain Shirt | Chain-Link Vest | Fence by day, armor by Floor 1. | 50 gp |
| `scale-mail` | Scale Mail | Scale Mail From a Cosplay Booth | Convention-grade. Bring a friend to help you sit. | 50 gp |
| `breastplate` | Breastplate | Sheet-Metal Breastplate | Hammered flat by someone with strong feelings. | 400 gp |
| `half-plate-armor` | Half Plate Armor | Hammered Hood-Panel Half Plate | Still faintly says 'Ford'. | 750 gp |
| `ring-mail` | Ring Mail | Washer-Ring Coverall | Hardware aisle couture. | 30 gp |
| `chain-mail` | Chain Mail | Chain-Link Fencing Laced Over a Work Coverall | Stops attacks. Also stops you from sitting. | 75 gp |
| `splint-armor` | Splint Armor | Strapped-On Venetian-Blind Plates | Open, close, survive. | 200 gp |
| `plate-armor` | Plate Armor | Welded Car-Door Plate | The window still rolls down. Do not roll it down. | 1,500 gp |

## Shields

| srd_id | SRD name | Display name | Snark | base_price |
|---|---|---|---|---|
| `shield` | Shield | Stop Sign Shield | Traffic law says STOP. Combat law says maybe. | 10 gp |

## Ammunition

| srd_id | SRD name | Display name | Snark | base_price |
|---|---|---|---|---|
| `arrows` | Arrows | Prop Arrows, Foam Tips Removed | Props department did not authorize this. | 1 gp |
| `bolts` | Bolts | Box of Nail-Gun Bolts | Still has the store sticker. Still a hazard. | 1 gp |
| `firearm-bullets` | Bullets, Firearm | Loose Rounds, Pocket Lint Included | Counted twice, still wrong. | 3 gp |
| `sling-bullets` | Bullets, Sling | Bag of Smooth River Rocks | Free from nature. Priced by the dungeon anyway. | 4 cp |
| `needles` | Needles | Sewing Needles, Bulk Craft Pack | Fifty tiny reasons to avoid the sewing aisle. | 1 gp |

## Spellcasting foci

| srd_id | SRD name | Display name | Snark | base_price |
|---|---|---|---|---|
| `arcane-focus` | Arcane Focus | Gift-Shop Crystal Assortment | Pick one. The shop will try to sell you three. | header, not purchasable (resolve to variant) |
| `arcane-focus-crystal` | Arcane Focus (Crystal) | Gift-Shop Crystal | Bought for the vibes. Kept for the spellcasting. | 10 gp |
| `arcane-focus-orb` | Arcane Focus (Orb) | Snow Globe, Gift-Shop Grade | Shake it. Something small and sad happens. | 20 gp |
| `arcane-focus-rod` | Arcane Focus (Rod) | Telescoping Car Antenna | Tunes in to the fundamental frequencies of nonsense. | 10 gp |
| `arcane-focus-staff` | Arcane Focus (Staff) | Glitter-Glued Mop Handle | A craft project with real consequences. | 5 gp |
| `arcane-focus-wand` | Arcane Focus (Wand) | Chopstick With Ambition | Takeout never felt so magical. | 10 gp |
| `druidic-focus` | Druidic Focus | Garden-Center Odds and Ends | Everything in it is technically alive. | header, not purchasable (resolve to variant) |
| `druidic-focus-sprig-of-mistletoe` | Druidic Focus (Sprig of Mistletoe) | Plastic Mistletoe Sprig | Nature, but the Dollar-Store cut. | 1 gp |
| `druidic-focus-wooden-staff` | Druidic Focus (Wooden Staff) | Houseplant-Wrapped Broom Handle | The ficus is the senior druid here. | 5 gp |
| `druidic-focus-yew-wand` | Druidic Focus (Yew Wand) | Branch Snapped Off the Neighbor's Hedge | Pruned by a trespasser with intentions. | 10 gp |
| `holy-symbol` | Holy Symbol | Dashboard Saint on a Lanyard | Protects drivers, travelers, and the occasional Crawler. | header, not purchasable (resolve to variant) |
| `holy-symbol-amulet` | Holy Symbol (Amulet) | Gas-Station Saint Medal | Blessed by a clerk who took a coffee break. | 5 gp |
| `holy-symbol-emblem` | Holy Symbol (Emblem) | Iron-On Emblem Patch | Faith, sold in packs of two. | 5 gp |
| `holy-symbol-reliquary` | Holy Symbol (Reliquary) | Pill-Case Reliquary | Contains what the label says. Probably. | 5 gp |

## Adventuring gear

| srd_id | SRD name | Display name | Snark | base_price |
|---|---|---|---|---|
| `acid` | Acid | Battery-Acid Slushie | Brain freeze is the least of your concerns. | 25 gp |
| `alchemists-fire` | Alchemist's Fire | Flaming Hot Nacho Cheese Pouch | Extra hot. Extra cheese. Extra problem. | 50 gp |
| `antitoxin` | Antitoxin | Gas-Station Pepto, Chewable | Chalky cure for dubious meals. | 50 gp |
| `backpack` | Backpack | Lost-and-Found Backpack | Someone is missing this. They have bigger problems now. | 2 gp |
| `ball-bearings` | Ball Bearings | Bag of Lost Marbles (Not Yours) | Sorry, kid. The dungeon needs them. | 1 gp |
| `barrel` | Barrel | Pickle Barrel, Previous Tenant Unknown | Smells like a decision made years ago. | 2 gp |
| `basket` | Basket | Easter Basket, Post-Easter | Plastic grass still in the corners. | 4 sp |
| `bedroll` | Bedroll | Gym-Locker Sleeping Bag | Faint hint of old sneaker. Surprisingly comfortable. | 1 gp |
| `bell` | Bell | Staff-Lounge Hand Bell | Rings for attention. Receives none. | 1 gp |
| `blanket` | Blanket | Waiting-Room Blanket | Warm. Damp. Do not ask. | 5 sp |
| `block-and-tackle` | Block and Tackle | Curtain Rigging Pulley, Stage Left | Lifts heavy things. Drops heavier ones. | 1 gp |
| `book` | Book | Paperback Someone Else Annotated | The margin notes are better than the plot. | 25 gp |
| `glass-bottle` | Bottle, Glass | Empty Bottle, Deposit Pending | Worth five cents somewhere nicer. | 2 gp |
| `bucket` | Bucket | Janitor's Bucket, Contents Unknown | Do not look. Do not smell. | 5 cp |
| `caltrops` | Caltrops | Bag of LEGO, Barefoot Edition | Every parent's nightmare, now weaponized. | 1 gp |
| `candle` | Candle | Dressing-Room Candle, Scented Like a Funeral | Mood lighting for the end times. | 1 cp |
| `crossbow-bolt-case` | Case, Crossbow Bolt | Fishing-Tackle Box, Bolts Only | No fish. Many regrets. | 1 gp |
| `map-or-scroll-case` | Case, Map or Scroll | Poster Tube, Slightly Dented | Home to many maps and one confused spider. | 1 gp |
| `chain` | Chain | Bike-Lock Chain Missing the Lock | Missing the lock, long on attitude. | 5 gp |
| `chest` | Chest | Footlocker With a Name Scratched Off | Whoever owned it left in a hurry. | 5 gp |
| `climbers-kit` | Climber's Kit | Hardware-Store Harness (Pitons Included, Regrettably) | Assembly required. Instructions in a language of screaming. | 25 gp |
| `fine-clothes` | Clothes, Fine | Midterm Blazer, Embroidered STAFF | Wear it to look important. Do not get caught. | 15 gp |
| `travelers-clothes` | Clothes, Traveler's | Thrift-Store Road-Trip Outfit | Slightly stained. Fully committed. | 2 gp |
| `component-pouch` | Component Pouch | Fanny Pack of Random Junk | Contains everything and nothing, depending on the spell. | 25 gp |
| `costume` | Costume | Mascot Head, Sweaty (Not That One) | The head stays on. The questions stay unanswered. | 5 gp |
| `crowbar` | Crowbar | Paint-Can Pry Bar | Opens cans. Opens crates. Opens opportunities. | 2 gp |
| `flask` | Flask | Hip Flask, Engraved To Someone Else | Never ask who Dave was. | 2 cp |
| `grappling-hook` | Grappling Hook | Coat-Hanger Grapple | Bent into hope. | 2 gp |
| `healers-kit` | Healer's Kit | Break-Room First-Aid Kit, Lightly Bitten | One bandage left and it has teeth marks. | 5 gp |
| `holy-water` | Holy Water | Communion Cup, Chilled | Served cold. Banishes things warm. | 25 gp |
| `hunting-trap` | Hunting Trap | Raccoon Trap, Industrial | Catches raccoons, Crawlers, and bad ideas. | 5 gp |
| `ink` | Ink | Printer Cartridge, Leaking | Ink is expensive; leaks are free. | 10 gp |
| `ink-pen` | Ink Pen | Hotel Pen, Chewed | Property of a better establishment. | 2 cp |
| `jug` | Jug | Milk Jug, Rinsed Once | Once is optimistic. | 2 cp |
| `ladder` | Ladder | Step Stool Optimistically Called a Ladder | Rated for exactly one hopeful Crawler. | 1 sp |
| `lamp` | Lamp | Desk Lamp With a Cord Cut Off | Unplugged and unbothered. | 5 sp |
| `bullseye-lantern` | Lantern, Bullseye | Spotlight Borrowed From the Drama Club | Everyone gets their moment. Aim it where you want. | 10 gp |
| `hooded-lantern` | Lantern, Hooded | Big Honking Flashlight | Batteries sold separately. The dungeon doesn't sell batteries. | 5 gp |
| `lock` | Lock | Padlock for a Locker Nobody Owns | Keeps out the problem you do not have yet. | 10 gp |
| `magnifying-glass` | Magnifying Glass | Dean's List Magnifying Glass | Finds clues, spiders, and your own mistakes. | 100 gp |
| `manacles` | Manacles | Plastic Zip-Cuffs | Great for detaining. Terrible at being a long-term solution. | 2 gp |
| `map` | Map | Staff Map, Coffee-Stained | You are here. Probably. Under the stain. | 1 gp |
| `mirror` | Mirror | Vanity Mirror, Half the Bulbs Dead | Reflects poorly on everyone. | 5 gp |
| `net` | Net | Volleyball Net, Reclaimed | Match point. For the enemy. | 1 gp |
| `oil` | Oil | Cooking Spray, Industrial Drum Size | Slips, burns, and ruins pans. | 1 sp |
| `paper` | Paper | Sticky-Note Pad, Neon | Reminders. Bright ones. Unwelcome ones. | 2 sp |
| `parchment` | Parchment | Printer Paper | Jam not included. Jam guaranteed. | 1 sp |
| `perfume` | Perfume | Dressing-Room Body Spray, Industrial Lilac | Fragrant enough to qualify as a weapon. | 5 gp |
| `basic-poison` | Poison, Basic | Unlabeled Bottle From Under the Sink | Do not mix with bleach. Do mix with enemies. | 100 gp |
| `pole` | Pole | Telescoping Light-Bulb Pole | Ten feet of poking reach, with a socket on the end. | 5 cp |
| `iron-pot` | Pot, Iron | Cast-Iron Pot | Heavy, durable, and judgmental. | 2 gp |
| `potion-of-healing` | Potion of Healing | Sports Drink, Mystery Flavor | Tastes like the color blue and a minor miracle. | 50 gp |
| `pouch` | Pouch | Ziplock Pouch | Zip slightly cracked. Shows its age. | 5 sp |
| `quiver` | Quiver | Quiver Made From a Cut-Up Backpack | Upcycling is a coping strategy. | 1 gp |
| `portable-ram` | Ram, Portable | Fire-Department Door Ram, Surplus | Knocks. Then really knocks. | 4 gp |
| `rations` | Rations | Gas-Station Jerky Cubes (Mystery Meat, Sealed Since 2019) | Chewy, salty, and nobody asks what animal. | 5 sp |
| `robe` | Robe | Sad Hotel Robe | Monogrammed. Stolen. Fits nobody. | 1 gp |
| `rope` | Rope | Extension Cord, Fifty Feet, Unplugged | Strong enough to climb. Weak enough to disappoint. | 1 gp |
| `sack` | Sack | Plastic Grocery Bag, Reused 40 Times | Holds the world, barely. | 1 cp |
| `shovel` | Shovel | Snow Shovel | Out of season. Out of options. | 2 gp |
| `signal-whistle` | Signal Whistle | Hotel Desk Bell, Ding Ding | Ring for service. Service is a crawler horde. | 5 cp |
| `spell-scroll-cantrip` | Spell Scroll (Cantrip) | Cantrip Sticky Note | Say it quick before the glue gives out. | 30 gp |
| `spell-scroll-level-1` | Spell Scroll (Level 1) | Level 1 Index Card | One use only. Laminate at your own risk. | 50 gp |
| `iron-spikes` | Spikes, Iron | Bag of Railroad Spikes | Holds doors shut. Holds grudges tighter. | 1 gp |
| `spyglass` | Spyglass | Souvenir Telescope From a Scenic Overlook | Costs a quarter at the overlook. Costs far more here. | 1,000 gp |
| `string` | String | Ball of Twine, Kitten-Tested | Frayed on one end, claimed by a cat. | 1 sp |
| `tent` | Tent | Dorm-Room Pup Tent | Fits two, if they are very good friends. | 2 gp |
| `tinderbox` | Tinderbox | Matchbook | Last match lit. Please do not ask who lit the others. | 5 sp |
| `torch` | Torch | Tiki Torch, Unlicensed | Backyard luau energy in a very dark room. | 1 cp |
| `vial` | Vial | Sample Vial From the Clinic | Previously contained something. Previously. | 1 gp |
| `waterskin` | Waterskin | Squeeze Water Bottle | BPA status unknown. Dungeon doesn't care. | 2 sp |
| `spellbook` | Spellbook | Cracked Phone App | Spells autosave. Rarely sync. | 50 gp |
| `heal-critter-potion` | Heal Critter Potion (canon item, no SRD entry) | Good Boy Gulp, Shaken Until Brown | Only works if the pet drinks it. Ordinary healing does nothing for pets. Do not drink it yourself. | 50 credits proposed (non-SRD canon, Floor-1 scale; Syndicate to confirm) |
| `pet-carrier` | Pet Carrier (canon item, no SRD entry) | Fold-Flat Kennel With an Impossible Interior | Fits one bonded pet in your inventory, safely. Where the pet goes while inside is not our department. | 100 credits proposed (non-SRD canon, Floor-1 scale; Syndicate to confirm) |

## Starting equipment packs

| srd_id | SRD name | Display name | Snark | base_price |
|---|---|---|---|---|
| `burglars-pack` | Burglar's Pack | Gym Bag of Suspicious Hardware | The zipper never quite closes. Neither does the explanation. | 16 gp |
| `diplomats-pack` | Diplomat's Pack | Conference Tote Bag, Lanyards Included | Network or die. Possibly both. | 39 gp |
| `dungeoneers-pack` | Dungeoneer's Pack | Maintenance-Closet Duffel | Everything you need to maintain a dungeon you'll never leave. | 12 gp |
| `entertainers-pack` | Entertainer's Pack | Backstage Roller Bag | One wheel squeaks, as foretold. | 40 gp |
| `explorers-pack` | Explorer's Pack | Lost-and-Found Duffel, Someone Else's Gym Clothes | Pack light, smell heavy. | 10 gp |
| `priests-pack` | Priest's Pack | Church-Basement Donation Bag | Folding chairs sold separately. Guilt included. | 33 gp |
| `scholars-pack` | Scholar's Pack | Library Tote With Highlighters | Everything is highlighted. Nothing is understood. | 40 gp |

## Tools, kits, gaming sets, instruments

| srd_id | SRD name | Display name | Snark | base_price |
|---|---|---|---|---|
| `artisans-tools` | Artisan's Tools | Hardware-Store Tool Roll | Pick a trade. The roll covers it. Mostly. | header, not purchasable (resolve to variant) |
| `alchemists-supplies` | Alchemist's Supplies | Confiscated Chemistry Set | Half the vials say DO NOT. | 50 gp |
| `brewers-supplies` | Brewer's Supplies | Home-Brew Kit, Bubbling Ominously | Smells like bread. Hits like a Tuesday. | 20 gp |
| `calligraphers-supplies` | Calligrapher's Supplies | Gel Pens and a Highlighter | Elegant penmanship at a 2-for-1. | 10 gp |
| `carpenters-tools` | Carpenter's Tools | Dollar-Store Tool Roll | The tape measure is a suggestion. | 8 gp |
| `cartographers-tools` | Cartographer's Tools | Road Atlas and Sharpies | Draw the dungeon. Hope it holds still. | 15 gp |
| `cobblers-tools` | Cobbler's Tools | Shoe-Repair Kit, Glue Dried Out | Fixes soles. Not souls. | 5 gp |
| `cooks-utensils` | Cook's Utensils | Spatula and Tongs From a Food Truck | The truck is gone. The seasoning remains. | 1 gp |
| `glassblowers-tools` | Glassblower's Tools | Blowpipe From a Craft Fair | Hot, delicate, and poorly insured. | 30 gp |
| `jewelers-tools` | Jeweler's Tools | Loupe and Pliers From a Pawnshop | Appraises everything. Values nothing. | 25 gp |
| `leatherworkers-tools` | Leatherworker's Tools | Belt-Punch and Awl Kit | Holes in everything, including the plan. | 5 gp |
| `masons-tools` | Mason's Tools | Trowel and Level, Tile-Shop Surplus | Level is crooked. Wall is crooked. Life is crooked. | 10 gp |
| `painters-supplies` | Painter's Supplies | Paint-by-Numbers Kit, Half Used | Every number is a lie. Color anyway. | 10 gp |
| `potters-tools` | Potter's Tools | Clay Block and a Spinning Office Chair | Throws pots. Throws up. Same chair. | 10 gp |
| `smiths-tools` | Smith's Tools | Tongs and a Hammer From a Welding Shop | Heats things up. Smacks things down. | 20 gp |
| `tinkers-tools` | Tinker's Tools | Junk Drawer of Screws and Gears | Somewhere in here is the one spare part you need. | 50 gp |
| `weavers-tools` | Weaver's Tools | Friendship-Bracelet Loom | Binds friends. Binds enemies when finished. | 1 gp |
| `woodcarvers-tools` | Woodcarver's Tools | Whittling Knife and Popsicle Sticks | Carves anything you do not need. | 1 gp |
| `disguise-kit` | Disguise Kit | Stage Makeup Kit, Half-Dried | Transforms you into someone else, badly. | 25 gp |
| `forgery-kit` | Forgery Kit | Office Supply Drawer | Stamps, pens, tape. The raw materials of fraud. | 15 gp |
| `herbalism-kit` | Herbalism Kit | Tea-Bag Tin | Chamomile fixes almost nothing. The bottom layer fixes the rest. | 5 gp |
| `navigators-tools` | Navigator's Tools | Gas-Station GPS Kit | Recalculating. Recalculating. Recalculating. | 25 gp |
| `poisoners-kit` | Poisoner's Kit | Pest-Control Tech's Toolkit | Rats not included. Rats are the first victims. | 50 gp |
| `thieves-tools` | Thieves' Tools | Bobby Pins and a Gift Card | Opens locks. Closes accounts. | 25 gp |
| `gaming-set` | Gaming Set | Deck of Cards | Stacked, marked, or just sticky. | header, not purchasable (resolve to variant) |
| `dice` | Dice | Bag of Mismatched Casino Dice | Some are loaded. Some are just heavy. | 1 sp |
| `dragonchess` | Dragonchess | Chess Set, Several Kings Missing | Replaced with salt shakers. Kings are lucky to be missing. | 1 gp |
| `playing-cards` | Playing Cards | Pinochle Deck, Sticky | Do not ask about the stickiness. | 5 sp |
| `three-dragon-ante` | Three-Dragon Ante | Trading-Card Binder, Mostly Bulk | Three dragons, one rare, many regrets. | 1 gp |
| `musical-instrument` | Musical Instrument | Karaoke Mic With One Working Song | The song is always the same. The audience is always doomed. | header, not purchasable (resolve to variant) |
| `bagpipes` | Bagpipes | Bagpipes From a Funeral Home Closet | Sounds like a dirge. Is a dirge. | 30 gp |
| `drum` | Drum | Plastic Bucket Drum | Street-corner percussion with a side of gravity. | 6 gp |
| `dulcimer` | Dulcimer | Garage-Sale Dulcimer | Three strings, one story, no refunds. | 25 gp |
| `flute` | Flute | Fourth-Grade Recorder | Still has someone's teeth marks. | 2 gp |
| `horn` | Horn | Vuvuzela, Sports-Bar Surplus | Announces you from three rooms away. | 3 gp |
| `lute` | Lute | Ukulele With Pretensions | Thinks it is a lute. Is fooled by the lighting. | 35 gp |
| `lyre` | Lyre | Harp-Shaped Wall Decor | Plucked from a spa's lobby. | 30 gp |
| `pan-flute` | Pan Flute | Pan Flute From a Gift Shop | Comes with a tiny plastic Pan. Nobody knows why. | 12 gp |
| `shawm` | Shawm | Kazoo, Extended Edition | The extension does nothing. The kazoo knows. | 2 gp |
| `viol` | Viol | Cello Case With Three Strings Left | The fourth string wanted a better life. | 30 gp |
