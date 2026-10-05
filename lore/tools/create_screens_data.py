# -*- coding: utf-8 -*-
"""Data for tables/create-screens-reskins.json and tables/create-flow-lines.proposed.json.
Display layer for the follow-on /create screens (S3, S4, S6 choices, S8 onward) plus the global nav and dialogs.
Label rows: 'Our Name (5e Name)', one pair of parentheses, display only. Text rows: full replacement text, same {placeholders}, same numbers.
NEVER change an id once published. Players are Crawlers. No banned words (the check rejects them)."""
LABEL_KINDS = ("title", "button", "select_label", "modal_title", "field_label", "stat_label", "ability", "method",
               "choice_group", "choice_option", "package")
TEXT_KINDS = ("help", "notice", "error", "hint", "dialog")
SCREENS = ["ALL", "S1", "S3", "S4", "S6", "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17"]
ROWS = []

def L(i, screen, kind, srd, disp, flavor, old=None, suffix="", ph=(), old_ph=None, uses=None, chargen=None):
    combined = "%s (%s)" % (disp, srd)
    ROWS.append({"id": i, "screen": screen, "kind": kind, "srd_name": srd, "display_name": disp, "combined_label": combined,
                 "old": old if old is not None else srd, "new": combined + suffix, "flavor": flavor,
                 "placeholders": list(ph), "old_placeholders": list(old_ph if old_ph is not None else ph),
                 "uses": uses, "chargen_ref": chargen})

NEEDS_CODE_DETAIL = {}

def T(i, screen, kind, old, new, ph=(), old_ph=None):
    ROWS.append({"id": i, "screen": screen, "kind": kind, "old": old, "new": new,
                 "placeholders": list(ph), "old_placeholders": list(old_ph if old_ph is not None else ph)})

# ---------------------------------------------------------------- ability scores and S8 method names
L("method-standard-array", "S8", "method", "Standard array", "Factory Preset",
  "Six fixed numbers off the System's shelf: 15, 14, 13, 12, 10, 8. No dice, no regrets, no personality.", chargen="ability_methods.methods[standard_array]")
L("method-point-buy", "S8", "method", "Point buy", "Layaway Plan",
  "27 points, scores from 8 to 15, and the System charges extra at the top.", chargen="ability_methods.methods[point_buy]")
L("method-roll", "S8", "method", "Roll", "Dice Gamble",
  "4d6, drop the lowest, six scores, three arrays, keep one that totals 73 or more. Logged, public, and not your fault.", chargen="ability_methods.methods[roll]")
L("ability-str", "S8", "ability", "Strength", "Gym-Bro Energy",
  "How much you can carry, kick through, or regret lifting.", chargen="abilities[str]")
L("ability-dex", "S8", "ability", "Dexterity", "Parkour Delusion",
  "Moves you saw online and the reflex to land them. Sometimes.", chargen="abilities[dex]")
L("ability-con", "S8", "ability", "Constitution", "Gas-Station Sushi Survivor",
  "Whatever keeps you alive past Floor 1. Mostly spite.", chargen="abilities[con]")
L("ability-int", "S8", "ability", "Intelligence", "Pub-Quiz Brain",
  "Recall, logic, and knowing which wiki to open first.", chargen="abilities[int]")
L("ability-wis", "S8", "ability", "Wisdom", "Warning Signs You Ignored",
  "Your gut, your senses, and the feeling right before everything went wrong.", chargen="abilities[wis]")
L("ability-cha", "S8", "ability", "Charisma", "Main-Character Energy",
  "The audience has already formed opinions about this one.", chargen="abilities[cha]")
L("stat-hp", "S8", "stat_label", "HP", "Pain Budget", "How much damage you eat before the System starts a new file.")
L("stat-ac", "S8", "stat_label", "AC", "Not-Getting-Hit Number", "Armor, reflexes and good intentions, summed.")
L("stat-proficiency-bonus", "S8", "stat_label", "Proficiency Bonus", "Competence Bonus", "What you add to things you are actually good at.")
L("stat-initiative", "S8", "stat_label", "Initiative", "Jump-Scare Reflex", "How fast you react when the room goes wrong.")
L("stat-passive-perception", "S8", "stat_label", "Passive Perception", "Spidey-Sense", "What you notice while not trying to.")
L("title-s8", "S8", "title", "Ability scores", "The Six Numbers", "Six numbers decide how long you last. Pick a method.")
L("button-s8-enter-scores", "S8", "button", "Enter scores", "Hand In Your Numbers", "Type six numbers; the System checks your math, not your feelings.")
L("button-s8-keep", "S8", "button", "Keep {id}", "Take Array {id}", "You keep ONE array. Choose like the audience is watching.", ph=("{id}",))
T("hint-s8-points-used", "S8", "hint", "Points used: {used} of {budget}.", "Layaway Plan (Point buy) used: {used} of {budget} points.", ph=("{used}", "{budget}"))
T("hint-s8-methods-head", "S8", "hint", "Methods: standard array ({array}) or point buy ({budget} points; scores 8-15 before bonuses). The background bonus is added after.",
  "Methods: Factory Preset (Standard array) with {array}, or Layaway Plan (Point buy) with {budget} points and scores 8-15 before bonuses. The background bonus is added after.", ph=("{array}", "{budget}"))
T("hint-s8-method-line", "S8", "hint", "**Method:** {method}.", "**Method:** {method_label}.", ph=("{method_label}",), old_ph=("{method}",))
T("hint-s8-base-line", "S8", "hint", "Base: {scores} (choose your background bonus on S7 to see finals)", "Base: {scores} (choose your Prior Employment bonus on S7 to see finals)", ph=("{scores}",))
T("hint-s8-preview-line", "S8", "hint", "HP {hp}   AC {ac}{ac_note}   Prof +{pb}   Init {init}   Passive Perception {pp}",
  "Pain Budget (HP) {hp}   Not-Getting-Hit Number (AC) {ac}{ac_note}\nCompetence Bonus (Proficiency Bonus) +{pb}   Jump-Scare Reflex (Initiative) {init}   Spidey-Sense (Passive Perception) {pp}",
  ph=("{hp}", "{ac}", "{ac_note}", "{pb}", "{init}", "{pp}"))
T("hint-s8-ac-provisional", "S8", "hint", "(10 + Dex for now)", "(10 + Dex for now; no armor yet)")
T("hint-s8-enter-order", "S8", "hint", "Enter six numbers in the order STR DEX CON INT WIS CHA.", "Hand in six numbers in the order STR DEX CON INT WIS CHA.")
T("select-s8-assign", "S8", "hint", "{ab}: pick a score", "{ability_label}: pick a score", ph=("{ability_label}",), old_ph=("{ab}",))
T("notice-s8-pick-method", "S8", "notice", "Pick a method first.", "Pick a method first. The System does not guess your numbers.")
T("notice-s8-set-scores", "S8", "notice", "Set legal ability scores first.", "Your numbers are not legal yet. Set six legal scores first.")
T("notice-s8-roll-three", "S8", "notice", "Roll your three arrays first.", "Roll your three arrays first. The dice are waiting.")
T("notice-s8-pick-roll", "S8", "notice", "Pick Roll first.", "Pick the Dice Gamble (Roll) first.")
T("notice-s8-once-each", "S8", "notice", "Each score goes to one ability, once.", "Each score goes to one ability, once. No double-dipping.")
T("notice-s8-menus-only", "S8", "notice", "Roll scores are assigned with the menus, not typed.", "Rolled scores go in through the menus, not the keyboard. The dice vouch for themselves.")
T("notice-s8-press-roll", "S8", "notice", "Press Roll for your three arrays.", "Press the Dice Gamble (Roll) for your three arrays. The System rolls; you watch.")
T("notice-s8-tap-keep", "S8", "notice", "Tap Keep A, B or C (a greyed-out array is not keepable).", "Take Array A, B or C (Keep A, B or C; a greyed-out array is not keepable, and the System checked).")
T("notice-s8-dice-jam", "S8", "notice", "The dice would not roll. Tap Roll to try again.", "The dice jammed. Tap the Dice Gamble (Roll) to try again.")
T("error-s8-six-numbers", "S8", "error", "Give exactly six numbers in the order STR DEX CON INT WIS CHA.", "Hand in exactly six numbers in the order STR DEX CON INT WIS CHA. The System cannot read minds.")
T("error-s8-not-set", "S8", "error", "Ability scores are not set.", "No numbers on file yet. Set your six scores.")
T("error-s8-array-once", "S8", "error", "Standard array means each of {array} exactly once.", "The Factory Preset (Standard array) means each of {array} exactly once. No substitutions.", ph=("{array}",))
T("error-s8-pointbuy-range", "S8", "error", "Point buy scores must be {min}-{max} before bonuses.", "Layaway Plan (Point buy) scores must be {min}-{max} before bonuses. The System has a floor and a ceiling.", ph=("{min}", "{max}"))
T("error-s8-pointbuy-cost", "S8", "error", "That costs {cost} points; you have {budget}.", "That costs {cost} points. Your Layaway Plan (Point buy) limit is {budget}.", ph=("{cost}", "{budget}"))
T("error-s8-kept-array", "S8", "error", "Use the six scores of the array you kept, each exactly once.", "Use the six scores of the array you took, each exactly once.")
T("error-s8-whole-numbers", "S8", "error", "Scores must be whole numbers.", "Whole numbers only. The System does not do fractions.")
T("error-s8-roll-sum", "S8", "error", "Your rolled numbers do not add up. Roll again from the method screen.", "Your rolled numbers do not add up. Go back to the method screen and roll again.")
T("error-s8-roll-dice", "S8", "error", "Your rolled numbers do not match the dice.", "Your rolled numbers do not match the logged dice. The log wins.")
T("error-s8-roll-past-keeper", "S8", "error", "A round that had a keepable array cannot be rolled past.", "A round that had a keepable array cannot be rolled past. You had a good one; live with it.")
T("error-s8-roll-keep-one", "S8", "error", "Keep one of your rolled arrays first.", "Take one of your rolled arrays first.")
T("error-s8-roll-final-round", "S8", "error", "Keep an array from your final round.", "Take an array from your final round. The old rounds are history.")
T("error-s8-roll-total", "S8", "error", "That array totals {total}; it needs {min_total} or more.", "That array totals {total}. The System wants {min_total} or more.", ph=("{total}", "{min_total}"))
T("error-s8-cap-20", "S8", "error", "No score may end above 20.", "No score may end above 20. Not even for you.")
T("help-s8", "S8", "help",
  "Standard array: 15 14 13 12 10 8, each once. Point buy: 27 points, scores 8-15.\nEnter six numbers in the order STR DEX CON INT WIS CHA; the background bonus is added after.\nHP, AC and the rest are computed for you.",
  "Factory Preset (Standard array): 15 14 13 12 10 8, each once. Layaway Plan (Point buy): 27 points, scores 8-15.\nHand in six numbers in the order STR DEX CON INT WIS CHA; the background bonus is added after.\nPain Budget (HP), Not-Getting-Hit Number (AC) and the rest are computed for you.")
# ---------------------------------------------------------------- S9 skills and proficiencies
L("title-s9", "S9", "title", "Skills and proficiencies", "Things You Can Actually Do", "What your body already knows how to do, plus what you pick.")
L("select-s9-class-skills", "S9", "select_label", "Class skills", "Rehearsed Talents", "The skills your Provisional Class pretends it taught you.",
  old="Class skills: pick {n}", suffix=": pick {n}", ph=("{n}",))
L("select-s9-skilled", "S9", "select_label", "Skilled", "Tech-Support Jack-of-All-Trades", "Matches the feat's reskinned name on Prior Employment (Skilled).",
  old="Skilled feat: pick {n} skills", suffix=": pick {n} skills", ph=("{n}",))
L("select-s9-languages", "S9", "select_label", "Languages", "Phrasebook", "Common is free. The rest you picked up from a cruise.",
  old="Languages: pick {n} (plus Common)", suffix=": pick {n}, plus Common", ph=("{n}",))
T("notice-s9-dropped", "S9", "notice", "Dropped picks that stopped being legal: {list}", "The System tossed picks that stopped being legal: {list}", ph=("{list}",))
T("notice-s9-need-class-bg", "S9", "notice", "Pick a class and background first (screens 6 and 7).", "Pick a Provisional Class and Prior Employment first (screens 6 and 7).")
T("error-s9-class-skills", "S9", "error", "Pick exactly {n} class skills.", "Pick exactly {n} class skills. The System counted.", ph=("{n}",))
T("error-s9-class-skills-legal", "S9", "error", "Class skill picks must be legal and not duplicate.", "Class skill picks must come from your class list, with no repeats and no skill you already have from your Prior Employment or Latent Biology. The System has your résumé.")
T("error-s9-skilled", "S9", "error", "Skilled: pick {n} more skills.", "Skilled: pick {n} more skills. Everybody has a hobby.", ph=("{n}",))
T("error-s9-languages", "S9", "error", "Pick {n} languages.", "Pick {n} languages. Common is free; the rest are on you.", ph=("{n}",))
T("error-s9-expertise-count", "S9", "error", "Pick {n} Expertise.", "Pick {n} Expertise. Overachieving is mandatory.", ph=("{n}",))
T("error-s9-expertise-legal", "S9", "error", "Expertise needs a skill you are proficient in.", "Expertise needs a skill you are already proficient in. You cannot brag about nothing.")
T("error-s9-masteries", "S9", "error", "Pick {n} weapon masteries.", "Pick {n} weapon masteries. Your weapons have tricks; learn them.", ph=("{n}",))
T("help-s9", "S9", "help",
  "Fixed proficiencies came with your background and species.\nPick the rest; skills you already own are hidden.\nClasses with masteries or expertise ask for those here.",
  "The fixed ones came with your Prior Employment and Latent Biology.\nPick the rest; skills you already own are hidden.\nClasses with Weapon Tricks (Weapon Mastery) or Overachiever Bonus (Expertise) ask for those here.")
# ---------------------------------------------------------------- class choices (S6 pick, S9 weapon mastery / expertise)
L("choice-weapon-masteries", "S9", "choice_group", "Weapon Mastery", "Weapon Tricks", "The special trick each practiced weapon unlocks.",
  uses={"S9 select": "Weapon Tricks (Weapon Mastery): pick {n}"}, chargen="classes.*.choices[weapon_masteries]")
L("choice-expertise", "S9", "choice_group", "Expertise", "Overachiever Bonus", "Double the bonus on a skill you already have. Obnoxious and legal.",
  uses={"S9 select": "Overachiever Bonus (Expertise): pick {n}"}, chargen="Rogue.choices[expertise]")
L("choice-divine-order", "S6", "choice_group", "Divine Order", "Chaplain Assignment", "Which shift the Urgent-Care Chaplain actually works.", chargen="Cleric.choices[divine_order]")
L("choice-primal-order", "S6", "choice_group", "Primal Order", "Garden Duty", "Whether the Community-Garden Zealot hexes or weeds.", chargen="Druid.choices[primal_order]")
L("choice-fighting-style", "S6", "choice_group", "Fighting Style", "Combat Gimmick", "One permanent combat trick. Pick the one you can explain at a bar.", chargen="Fighter.choices[fighting_style]")
L("choice-invocation", "S6", "choice_group", "Eldritch Invocation", "Contract Add-On", "The fine print you did not read, now with benefits.", chargen="Warlock.choices[invocation]")
FS = [("Archery", "Carnival-Booth Sharpshooter", "Ranged hits, courtesy of a stuffed-bear grudge."),
      ("Blind Fighting", "Power-Outage Brawler", "You swing fine in the dark. It is mostly the dark's fault."),
      ("Defense", "Bubble-Wrap Enthusiast", "A permanent bonus to not being hit while armored."),
      ("Dueling", "Single-Hand Swagger", "One weapon, one hand, one overconfident grin."),
      ("Great Weapon Fighting", "Two-Handed Overcompensation", "Big weapon, bigger damage dice, no apology."),
      ("Interception", "Human Airbag Reflex", "You step in front of your friends' damage. They owe you a drink."),
      ("Protection", "Crowd-Control Shield Shove", "Your shield makes enemies miss the guy behind you."),
      ("Thrown Weapon Fighting", "Dart-League Menace", "Throw it, draw it, throw it again."),
      ("Two-Weapon Fighting", "Double-Fisting Menace", "Two weapons, two hands, zero impulse control."),
      ("Unarmed Fighting", "Bar-Fight Haymaker", "Fists as a lifestyle choice.")]
for srd, disp, fl in FS:
    L("opt-fighting-style-" + srd.lower().replace(" ", "-"), "S6", "choice_option", srd, disp, fl, chargen="Fighter.choices[fighting_style].options")
INV = [("Armor of Shadows", "Fog-Machine Outfit", "Self-cast armor, powered by dry ice."),
       ("Eldritch Mind", "Focus Supplement Subscription", "Keeps your concentration from dropping. Auto-renews."),
       ("Fiendish Vigor", "Devil's Energy Drink", "Temporary hit points. The can has no ingredients list."),
       ("Gaze of Two Minds", "Borrowed-Eyes Livestream", "See through an ally's eyes. Ask first."),
       ("Lessons of the First Ones", "Pirated Masterclass", "A bonus feat from a course you did not buy."),
       ("Misty Visions", "Vape-Cloud Illusions", "Minor illusions, cloud included."),
       ("Pact of the Blade", "Weapon Lease Agreement", "Your patron loans you a blade. Late fees apply."),
       ("Pact of the Chain", "Familiar Rewards Program", "A special familiar with a loyalty card."),
       ("Pact of the Tome", "Notebook of Bad Decisions", "A book of spells and regrets."),
       ("Devil's Sight", "Night-Vision Free Trial", "See in the dark. Does not say what it costs after the trial."),
       ("Mask of Many Faces", "Filter-Pack Subscription", "Change your face on demand. Cancel anytime, in theory.")]
for srd, disp, fl in INV:
    L("opt-invocation-" + srd.lower().replace("'", "").replace(" ", "-"), "S6", "choice_option", srd, disp, fl, chargen="Warlock.choices[invocation].options")
# ---------------------------------------------------------------- S10 equipment
L("title-s10", "S10", "title", "Starting equipment", "Junk Intake", "Everything is junk. Everything works.")
L("package-class-a", "S10", "package", "Package A", "Locker-Cleanout Duffel", "A class package from someone's gym locker. Dibs on the good stuff.",
  old="Package A ({gp} GP left over)", suffix=" - {gp} credits left over", ph=("{gp}",), chargen="classes.*.packages[A]")
L("package-class-b", "S10", "package", "Package B", "Estate-Sale Grab Bag", "The second class package with items (Fighter only; for the other 11 classes Package B is the gold option).",
  old="Package B ({gp} GP left over)", suffix=" - {gp} credits left over", ph=("{gp}",), chargen="Fighter.packages[B]")
L("package-gold", "S10", "package", "Gold option", "Take the Credits", "Skip the kit and shop at the Intake Vending Wall. 1 credit = 1 GP.",
  old="Gold option: {gp} GP", suffix=": {gp} credits", ph=("{gp}",), chargen="classes.*.packages[B] (11 classes, no items) and Fighter.packages[C]")
L("select-s10-kit", "S10", "select_label", "Package or gold", "Kit or Credits", "Each of class and background gives a kit or a credit amount. Pick one for each.",
  old="{owner}: package or gold", suffix="", ph=("{owner}",))
ROWS[-1]["new"] = "{owner}: " + ROWS[-1]["combined_label"]
L("button-s10-shop", "S10", "button", "Vending Wall", "Shop the Intake Vending Wall", "Credits only; judgment is free.", old="Vending Wall (buy)")
L("button-s10-prices", "S10", "button", "Price list", "Gouge Sheet", "What each piece of junk costs. Surprisingly fair.")
L("button-s10-clear", "S10", "button", "Clear shopping", "Empty the Cart", "Put it all back. The Wall does not mind.")
T("hint-s10-variant", "S10", "hint", "Pick your {item} ({src} package)", "Pick your {item} type ({src} package). The System will not pick for you.", ph=("{item}", "{src}"))
T("hint-s10-skip-package", "S10", "hint", "Skip the package, take the credits", "Skip the kit, take the credits")
T("notice-s10-type-na", "S10", "notice", "That type is not available for this item.", "The Wall does not stock that type for this item.")
T("notice-s10-cart-cleared", "S10", "notice", "Your shopping list was cleared (it no longer fit).", "The Wall emptied your cart. It no longer fit.")
T("notice-s10-overspend", "S10", "notice", "That costs {cost} credits but you have {have}. Nothing was bought.", "That costs {cost} credits. You have {have}. The Wall bought nothing and judged you.", ph=("{cost}", "{have}"))
T("notice-s10-not-on-wall", "S10", "notice", "Not on the Wall: {names}", "Not on the Wall: {names}. The Wall stocks what it stocks.", ph=("{names}",))
T("notice-s10-say-type", "S10", "notice", "Say which type: {names}. A generic is never sold.", "Say which type: {names}. The Wall never sells a generic.", ph=("{names}",))
T("error-s10-pick-both", "S10", "error", "Pick both equipment options (and do not overspend).", "Pick both equipment options (and do not overspend). The Wall keeps score.")
T("error-s10-pick-type", "S10", "error", "Pick the type of each item that says \"pick type\" (holy symbol, gaming set, instrument, tools).", "Pick the type of each item that says \"pick type\" (holy symbol, gaming set, instrument, tools). The Wall does not sell mystery packages.")
T("error-s10-need-both", "S10", "error", "Pick equipment (package or gold) for both class and background.", "Pick equipment (kit or credits) for both your Provisional Class and Prior Employment.")
T("error-s10-which-one", "S10", "error", "Pick which one you get: {list}.", "Pick which one you get: {list}. The Wall will not pick for you.", ph=("{list}",))
T("error-s10-wall-no-type", "S10", "error", "A Vending Wall line is missing its type.", "A Vending Wall line has no type. Name one.")
T("error-s10-overspent", "S10", "error", "You spent more credits than you have.", "You spent more credits than you have. The Wall does not extend credit.")
T("help-s10", "S10", "help",
  "Each of class and background gives a package or a gold amount (1 gold = 1 credit).\nSpend leftover credits at the Vending Wall by typing names; everything is a real 5e item.\nEvery item shows the System's own name with the real 5e name in brackets (from the item-reskins table); stats never change. Holy symbols, gaming sets, instruments and tools ask you to pick a type.",
  "Each of class and background gives a kit or a credit amount (1 gold = 1 credit).\nSpend leftover credits at the Intake Vending Wall by typing names; everything is junk and everything is a real 5e item underneath.\nEvery item shows the System's own name with the real 5e name in brackets (from the item-reskins table); stats never change. Holy symbols, gaming sets, instruments and tools ask you to pick a type.")
# ---------------------------------------------------------------- S11 spells
L("title-s11", "S11", "title", "Spells", "The Magic You Admit To", "Pick the ones you will admit to. The audience prefers loud.")
L("select-s11-cantrips", "S11", "select_label", "Cantrips", "Party Tricks", "Free, repeatable, and slightly embarrassing.",
  old="Cantrips: pick {n}", suffix=": pick {n}", ph=("{n}",), chargen="spells.*.cantrips")
L("select-s11-level1", "S11", "select_label", "Level 1 spells", "Real Magic", "Actual spells. Your Provisional Class would like you to be careful.",
  old="Level 1 spells: pick {n} in total", suffix=": pick {n} in total", ph=("{n}",), chargen="spells.*.level1_known")
L("select-s11-spellbook", "S11", "select_label", "Level 1 spellbook", "Cracked Phone App", "The Wizard's spellbook, autosaving rarely and syncing never.",
  old="Level 1 spellbook: pick {n} in total", suffix=": pick {n} in total", ph=("{n}",), chargen="spells.*.spellbook")
L("select-s11-prepare", "S11", "select_label", "Prepare {n} from your spellbook", "Load {n} From Your Phone App", "Load the spells you will actually bring to the fight.",
  ph=("{n}",), chargen="spells.*.prepared")
T("hint-s11-pick-book-first", "S11", "hint", "Pick spellbook spells first", "Fill the phone app first (nothing to load yet)")
T("notice-s11-none", "S11", "notice", "No spells for this class.", "No spells for this class. Go hit something.")
T("notice-s11-too-many", "S11", "notice", "Too many level 1 spells ({n}). Trim the other list.", "Too many level 1 spells ({n}). Trim the other list. The System has a bag limit.", ph=("{n}",))
T("error-s11-cantrips", "S11", "error", "Pick {n} cantrips from the class list.", "Pick {n} cantrips from the class list. Party tricks only.", ph=("{n}",))
T("error-s11-spellbook", "S11", "error", "Pick {n} spellbook spells.", "Pick {n} spellbook spells. The phone app has storage.", ph=("{n}",))
T("error-s11-prepare", "S11", "error", "Prepare {n} spells from your spellbook.", "Load {n} spells from your phone app. Only what is installed.", ph=("{n}",))
T("error-s11-level1", "S11", "error", "Pick {n} level 1 spells.", "Pick {n} level 1 spells. The System is counting.", ph=("{n}",))
T("help-s11", "S11", "help",
  "Casters pick cantrips and level 1 spells; Wizards also prepare a subset.\nEach menu entry says what the spell does in one line.\nOther classes skip this screen.",
  "Casters pick Party Tricks (cantrips) and Real Magic (level 1 spells); Wizards also load a subset from the Cracked Phone App.\nEach menu entry says what the spell does in one line.\nOther classes skip this screen.")
T("notice-s12-retired", "S12", "notice", "This step is retired. Press Next.", "This step is retired. Nothing to see. Press Next.")
# ---------------------------------------------------------------- S13 to S17




L("title-s14", "S14", "title", "Backstory and requested handle", "Your Sob Story and Handle Request", "Two sentences of public history and a handle you are asking nicely for.")
L("button-s14-write", "S14", "button", "Write backstory and handle", "Write Your Sob Story", "Public. The System reads it aloud at your introduction.")
L("modal-s14", "S14", "modal_title", "Backstory and handle", "Sob Story and Handle", "The modal that collects them.")
T("error-s14-required", "S14", "error", "Backstory is required.", "The System needs a backstory. Anything will do.")
T("error-s14-words", "S14", "error", "Pick different words for the backstory.", "Pick different words for the backstory. The System has notes.")
T("help-s14", "S14", "help",
  "Backstory is public: the System reads it at your introduction.\nRequested Handle is what you would like the audience to call you.\nBroadcast Name stays PENDING until Floor 3.",
  "Your backstory is public: the System reads it at your introduction.\nRequested Handle is what you would like the audience to call you. It is a request, not a promise.\nBroadcast Name stays PENDING until Floor 3.")
L("button-s15-write", "S15", "button", "Write orders", "Leave Instructions", "What your body does while your brain is in the bathroom.")
L("modal-s15", "S15", "modal_title", "Orders and reactions", "Autopilot Memo", "The modal for Standing Orders and Standing Reactions.")
T("error-s15-required", "S15", "error", "Standing Orders are required.", "Standing Orders are required. Your body cannot improvise.")
T("help-s15", "S15", "help",
  "Orders tell your body what to do when you are away; reactions say how to use your reaction.\nA signature attack name is optional.\nNo orders means Dodge on timeout.",
  "Orders tell your body what to do while you are away; reactions say how to use your reaction.\nA signature attack name is optional, but the audience likes a brand.\nNo orders means Dodge on timeout.")
L("button-edit", "ALL", "button", "Edit", "Rewrite It", "Reopen this screen's form and fix it.")
L("title-s16", "S16", "title", "Review", "Final Paperwork", "The finished sheet and the card exactly as it will be posted.", old="Review (the full sheet)")
L("select-s16-edit", "S16", "select_label", "Edit a screen", "Fix Something", "Jump back to any screen and return here.", old="Edit a screen…", suffix="…")
L("button-s16-private", "S16", "button", "Private notes", "Your Private File", "Only you see this.", old="Private notes (only you)")
L("button-restart", "S16", "button", "Restart", "Start Fresh", "Wipes your answers. Comfort answers stay.")
T("hint-s16-card", "S16", "hint", "Player-channel card (as it will be posted)", "Your Public Card (player-channel card, as it will be posted)")
T("hint-s16-card-missing", "S16", "hint", "(card preview unavailable)", "(card preview unavailable; the printer jammed)")
T("hint-s16-not-ready", "S16", "hint", "Not ready to confirm:", "The System cannot file this yet:")
T("help-s16", "S16", "help",
  "This is the finished sheet and the card exactly as it will be posted.\nUse Edit to jump back to any screen; you return here.\nConfirm enables when everything is legal.",
  "This is the finished sheet and the card exactly as it will be posted.\nUse Fix Something (Edit a screen) to jump back to any screen; you return here.\nSign ▸ (Confirm ▸) enables when everything is legal and takes you to Sign Here (Confirm), where Sign and Lock the File (Confirm and lock the file) registers your Crawler.")
L("title-s17", "S17", "title", "Confirm", "Sign Here", "Final step. No take-backs without the GM.")
L("button-s17-confirm", "S17", "button", "Confirm and lock the file", "Sign and Lock the File", "Locks the file and registers your Crawler.")
T("help-s17", "S17", "help",
  "Confirm locks the file and registers your Crawler.\nCorrections after this go through the GM.",
  "Signing locks the file and registers your Crawler.\nCorrections after this go through the GM.")
# ---------------------------------------------------------------- v0.1.2 additions (Syndicate audit F5, F12: coverage gaps G1-G7)
L("button-help", "ALL", "button", "Help", "Help Desk", "Opens the help text for this screen.")
L("button-resume", "ALL", "button", "Resume", "Pick It Back Up", "Reopens the draft you left open. Your answers are kept.")
L("dialog-restart-no", "ALL", "button", "Cancel", "Never Mind", "Closes the restart dialog and changes nothing.")
T("dialog-cancel-body", "ALL", "dialog", "This deletes your whole build, including any rolled ability scores. Nothing has been registered. You can start fresh with /create.", "This shreds your whole build, including any rolled ability scores. Nothing has been registered. You can start fresh with /create.")
T("notice-fix-screen", "ALL", "notice", "Fix {screen}: {msg}", "The System cannot file this yet. Fix {screen}: {msg}", ph=("{screen}", "{msg}"))
T("notice-benched", "ALL", "notice", "**{name} starts BENCHED**: no party slot, no XP, credits or loot, until you make it your active Crawler between sessions (`/crawlers`). {sheet_note}", "**{name} starts BENCHED**: no party slot, no XP, credits or loot, until you make it your active Crawler between sessions (`/crawlers`). The bench is warm; the audience is not. {sheet_note}", ph=("{name}", "{sheet_note}"))
T("notice-party-full", "S1", "notice", "Party full.", "Party full. The crawl has a headcount and you are one too many.")
T("hint-embed-footer", "ALL", "hint", "Private intake · session {session} · only you can see this", "Private intake booth · session {session} · only you can see this", ph=("{session}",))
T("hint-s8-kept", "S8", "hint", "**Kept: {array}.**", "**Taken: {array}.**", ph=("{array}",))
T("hint-s10-describe", "S10", "hint", "Take each package or its gold. Everything is junk; everything works. **Credits:** {from_options} from options, {spent} spent at the Intake Vending Wall, **{left} left**.", "Take each kit or its credits. Everything is junk; everything works. **Credits:** {from_options} from options, {spent} spent at the Intake Vending Wall, **{left} left**.", ph=("{from_options}", "{spent}", "{left}"))
T("notice-s10-need-class-bg", "S10", "notice", "Pick a class and background first.", "Pick a Provisional Class and Prior Employment first.")
T("hint-money-gp", "S10", "hint", "{n} GP", "{n} credits", ph=("{n}",))
T("hint-money-cp", "S10", "hint", "{n} cp", "{amount} credits", ph=("{amount}",), old_ph=("{n}",))
NEEDS_CODE_DETAIL.update({
 "hint-s8-method-line": {"renamed_placeholder": {"old": "{method}", "new": "{method_label}"}, "expected_value": "the combined label of the chosen method, e.g. 'Factory Preset (Standard array)'", "fallback": "if {method_label} is not supplied, fall back to the old {method}"},
 "select-s8-assign": {"renamed_placeholder": {"old": "{ab}", "new": "{ability_label}"}, "expected_value": "the combined label of the ability, e.g. 'Gym-Bro Energy (Strength)'", "fallback": "if {ability_label} is not supplied, fall back to the old {ab}"},
 "hint-money-gp": {"note": "Price list and variant-select descriptions, prices of 100 cp or more. {n} stays the number of GP; 1 credit = 1 GP.", "unit_word": "credit when the amount is 1 or less, credits otherwise"},
 "hint-money-cp": {"renamed_placeholder": {"old": "{n}", "new": "{amount}"}, "expected_value": "n / 100 in credits (1 cp = 0.01 credit, Core 5.10): whole numbers without decimals, otherwise decimals (50 cp -> 0.5, 5 cp -> 0.05)", "unit_word": "credit when the amount is 1 or less, credits otherwise", "fallback": "if {amount} is not supplied, leave the old '{n} cp' text"},
 "hint-s10-describe": {"note": "Placeholders {from_options}, {spent}, {left} stand for the three credit numbers in the line."},
})
# nav rows are shared by every screen; the plain views (S1/S2, comfort-only, survey) keep the old text
PLAIN_VIEWS = ["S1", "S2", "S13", "comfort_only"]
# ---------------------------------------------------------------- global nav and dialogs
L("nav-next", "ALL", "button", "Next ▸", "Onward ▸", "Move to the next screen.")
L("nav-back", "ALL", "button", "◂ Back", "◂ Retreat", "Step back. Nothing is lost.")
L("nav-skip", "ALL", "button", "Skip ▸", "Blow It Off ▸", "Skip this optional screen.")
L("nav-confirm", "ALL", "button", "Confirm ▸", "Sign ▸", "On the review screen, go to the signing step.")
L("nav-pick-for-me", "ALL", "button", "Pick for me", "System, Choose for Me", "The System picks a legal default. Change it if you hate it.")
L("nav-save-close", "ALL", "button", "Save and close", "Stash and Step Out", "Save the build and close the booth.")
L("nav-cancel-build", "ALL", "button", "Cancel build", "Rip Up the File", "Throw the build out.")
L("nav-close-nosave", "ALL", "button", "Close without saving", "Walk Away", "Close the booth, keep nothing new.")
L("nav-more", "ALL", "button", "More ▸", "Keep Scrolling ▸", "Next page of options on any paged screen.", old="More ▸ (page {p}/{pages})", suffix=", page {p}/{pages}", ph=("{p}", "{pages}"))
L("dialog-trash-yes", "ALL", "button", "Yes, trash it", "Yes, Shred It", "Confirms the trash dialog.")
L("dialog-trash-no", "ALL", "button", "No, keep going", "Keep Going, I Panicked", "Cancels the trash dialog.")
L("dialog-restart-yes", "ALL", "button", "Yes, wipe my answers", "Yes, Wipe Me", "Confirms the restart dialog.")
L("dialog-help-ok", "ALL", "button", "Got it", "Fine, Got It", "Closes the help dialog.")
T("dialog-trash-title", "ALL", "dialog", "Trash everything?", "Shred the whole file?")
T("dialog-restart-title", "ALL", "dialog", "Restart?", "Start fresh?")
T("dialog-help-title", "ALL", "dialog", "Help: {screen}", "Help Desk: {screen}", ph=("{screen}",))
T("notice-cancel-done", "ALL", "notice", "Build cancelled. Run /create to start fresh.", "File shredded. Run /create to start fresh.")
T("notice-cancel-registered", "ALL", "notice", "This Crawler is already registered. Nothing to cancel.", "This Crawler is already registered. There is nothing left to shred.")
T("notice-unavailable", "ALL", "notice", "Character creation is not available right now.", "Intake is closed right now. Come back when the booth reopens.")
T("notice-rules-changed", "ALL", "notice", "The rules table changed; these picks were cleared: {list}", "The rules changed under you; these picks were cleared: {list}", ph=("{list}",))
T("notice-wiped", "ALL", "notice", "Wiped. Your comfort answers were kept.", "Wiped. Your comfort answers survived.")
T("notice-nothing-to-pick", "ALL", "notice", "Nothing to pick yet; finish the earlier screens first.", "Nothing to pick yet. Finish the earlier screens first, Crawler.")
T("notice-save-failed", "ALL", "notice", "Could not save; ask the GM.", "The System dropped the file. Ask the GM.")
T("notice-draft-gone", "ALL", "notice", "That draft is gone. Run /create again.", "That file is gone. Run /create again.")
# ---------------------------------------------------------------- S3 name and S4 look (named in the job: name, pronouns, appearance)
L("title-s3", "S3", "title", "Crawler name and pronouns", "Name Tag and Pronouns", "The name goes on the paperwork. The audience's name for you comes later.")
L("button-s3-set", "S3", "button", "Set name", "Fill Out the Name Tag", "Write the name that goes on the paperwork.")
L("button-s3-change", "S3", "button", "Change name", "Reprint the Name Tag", "Change it. The System has more tags.")
L("button-s3-anyway", "S3", "button", "Use it anyway", "Stamp It Anyway", "Keep the similar name. The System noted it.")
L("select-s3-pronouns", "S3", "select_label", "Pronouns", "Pronoun Line, Optional", "Say what you like. Leave it blank if you do not.", old="Pronouns (optional)")
L("modal-s3-name", "S3", "modal_title", "Crawler name", "Name Tag", "The modal that collects the name.")
L("field-s3-name", "S3", "field_label", "Name", "Name Tag Text", "2 to 30 characters.", old="Name (2-30 characters)", suffix=", 2-30 characters")
T("error-s3-bad-name", "S3", "error", "That name will not work. Use 2-30 letters, digits, spaces, apostrophes, hyphens or periods, and not a reserved word.", "The System rejects that name. Use 2-30 letters, digits, spaces, apostrophes, hyphens or periods, and nothing on the reserved list.")
T("error-s3-no-name", "S3", "error", "Set a name first.", "No name tag yet. Set a name first.")
T("error-s3-near-dup", "S3", "error", "Confirm the similar name or pick another.", "That name is too close to another Crawler's. Stamp it anyway or pick another.")
T("help-s3", "S3", "help",
  "The name goes on the paperwork. Your Broadcast Name (what the audience calls you) comes later.\nIt must be unique in this session.\nPronouns are optional.",
  "The name goes on the paperwork. Your Broadcast Name (what the audience calls you) comes later.\nIt must be unique in this session. The System checks.\nPronouns are optional.")
L("title-s4", "S4", "title", "Look and hook", "Mugshot and Hook", "What you look like, and why you are still funny or dangerous.")
L("button-s4-write", "S4", "button", "Write look and hook", "Describe the Damage", "Two lines: the look and the hook.")
L("button-s4-edit", "S4", "button", "Edit look and hook", "Redo the Damage", "Rewrite the mugshot and the hook.")
T("error-s4-both", "S4", "error", "Both lines are required.", "Both lines are required. The System does not do blank mugshots.")
T("help-s4", "S4", "help",
  "Two short lines: what you look like now, and why you are funny or dangerous.\nEveryone reads as baseline human on Floors 1-2.\nNo links.",
  "Two short lines: what you look like now, and why you are funny or dangerous.\nEveryone reads as baseline human on Floors 1-2, so keep the horns for later.\nNo links.")

# ---------------------------------------------------------------- create-flow-lines.json rewrites (same keys, same {placeholders}, <= 3 variants)
LINES = {
 "S8_roll_offer": ["Dice Gamble (Roll): the System rolls three arrays of six scores (4d6, drop the lowest die, six times each). You keep ONE, and only an array that totals 73 or more. If none does, the System rolls all three again."],
 "S8_roll_keep_ok": ["Keepable (total {total}). The System approves.", "Keepable (total {total}). Somebody up there likes you.", "Keepable (total {total}). Take it before it changes its mind."],
 "S8_roll_keep_no": ["Not keepable (total {total}, needs 73 or more). Tragic, but legal.", "Not keepable (total {total}, needs 73 or more). The dice are not sorry.", "Not keepable (total {total}, needs 73 or more). Take it up with the dice."],
 "S8_roll_giveup": ["{rounds} rounds and no array above 72. That should not happen, and the System is embarrassed. Pick the Factory Preset (Standard array) or the Layaway Plan (Point buy)."],
 "S8_roll_closed": ["The Dice Gamble (Roll) is closed today. Pick the Factory Preset (Standard array) or the Layaway Plan (Point buy)."],
 "party_full": ["Party full. The crawl has a headcount and you are one too many.", "Party full. Come back when somebody dies."],
 "not_set_up": ["Table not set up. The booth is open, the building is not. Ask the GM.", "Table not set up. The System has no idea who you are yet. Ask the GM."],
 "taken": ["That name is taken. Pick another. The System does not do duplicates.", "Somebody already owns that name tag. Pick another."],
 "near_dup": ["That name sits inside another Crawler's name ('{other}'). Tools match partial names, so this could cause mix-ups. Tap Stamp It Anyway (Use it anyway), or pick another."],
 "restart_confirm": ["Start fresh? Your answers are wiped and the System pretends it never saw them. Your comfort answers stay."],
}
LINES_LEFT = {
 "already": "unchanged on purpose (decision 020: many Crawlers per player, so no one-body line). The bridge does not use this key today (Syndicate audit F1/F6).",
 "S1": "already flavored System voice; outside the follow-on scope", "S2": "already flavored; comfort wording is a safety text and stays as written",
 "S3": "already flavored", "S4": "already flavored", "S5": "already flavored", "S6": "already flavored", "S7": "already flavored",
 "S8": "already flavored; mentions no method names", "S8_roll_result": "already flavored; keeps the 'above 72' rule wording",
 "S8_roll_none": "already flavored; rule wording (above 72, rolls all three again)", "S8_roll_assign": "already flavored",
 "S8_roll_cap": "already flavored; 'No score goes above 20' rule wording",
 "S9": "already flavored", "S10": "already flavored", "S11": "already flavored", "S13": "already flavored; privacy statement stays as written (the survey view stays plain)",
 "S14": "already flavored", "S15": "already flavored", "S16": "already flavored", "S17": "already flavored; 'This locks the file' stays as written",
 "registered": "already flavored (variants)", "held": "already flavored (variants)", "returned": "already flavored",
 "pick_for_me": "already flavored", "quirk_human": "already flavored", "toast_paperwork": "achievement name, owned by the ledger",
 "toast_terms": "achievement name, owned by the ledger",
}
# ---------------------------------------------------------------- left vanilla on purpose
AUDIT = [
 ("skill-names", "The 18 skill names (Acrobatics ... Survival) and the skill picks on S9", "Rules and sheet math key on them; Caleb's rule: skill names stay plain unless display-only. Only the select labels around them are flavored."),
 ("tool-language-names", "Tool, instrument, gaming set and language names (S7/S9/S10 pick lists)", "Same rule as skills. The S10 'pick type' items stay as the real item types."),
 ("spell-names", "Cantrip and level 1 spell names and the one-line effect descriptions in the S11 menus", "Rules rely on the names; the descriptions are accuracy text. Only the section labels (Party Tricks, Real Magic, Cracked Phone App) are flavored."),
 ("weapon-mastery-properties", "Mastery property names (Cleave, Graze, Nick, Push, Sap, Slow, Topple, Vex) and the weapon option names in the Weapon Mastery menu", "Rules terms. Weapon names are covered by tables/item-reskins.json through the item labeler."),
 ("ability-abbreviations", "STR DEX CON INT WIS CHA on compact lines, the preview table and the typed-entry order", "They are parse hints (the typed order) and code ids. The flavored ability names are for select labels and headings only, always with the 5e name in parentheses."),
 ("preview-table-rows", "The per-ability preview rows 'STR  base 15 +2 = 17  (+3)' and the 'Base:' line values", "Compact table the player cross-checks against the dice; abbreviations and column words stay. The heading and the stat line under it are flavored."),
 ("rule-numbers", "73 or more / above 72, 4d6 drop lowest, 6 scores, 3 arrays, keep ONE, 10 round cap, 27 points, 8-15, 15 14 13 12 10 8, 20 cap, 2-30 name length, 300/160/140 character caps", "Rules facts. Every rewritten line keeps every number the old line had (the check enforces it)."),
 ("roll-log-wording", "'Round N: A 70, B 66, C 71 (none above 72)', 'rolled as A1', the struck-through dropped die, the roll.py label 'S8 roll r<round> <A|B|C><1-6>'", "Logged-dice wording stays exactly (Caleb's instruction). The S8_roll_result/none/assign/cap lines already carry the voice."),
 ("typed-entry-field", "Modal label 'STR DEX CON INT WIS CHA' and placeholder 'e.g. 15 8 14 10 12 13' on Enter scores", "Parse format hint; a flavored label would blur the column order."),
 ("pronoun-options", "he/him, she/her, they/them, unspecified", "Identity data. Not a place for jokes."),
 ("survey-text", "The 6 core questions, the bonus pool, 'Your answers are private and will not be read aloud...' and 'Passed. A pass is data too.'", "Already System-voiced in create-flow-lines.json; the privacy statement must stay precise."),
 ("glossary-terms", "Provisional Class, Prior Employment, Latent Biology, Origin feat, Intake Kiosk, Intake Tag, Broadcast Name, Requested Handle, Standing Orders, Standing Reactions, Intake Vending Wall, Intake Bag, Fan Profile, saferoom, credit", "Fixed terms in the create-flow spec glossary. Already flavored; do not rename."),
 ("terms-and-comfort", "S1/S2: ACCEPT, DECLINE, Read the Terms, Use a pre-built, the comfort lines/veils wording and 'Your lines and veils are updated. Nobody was notified.'", "Before the follow-on scope and safety text. Plain on purpose."),
 ("input-validation-hints", "'max N characters', 'no links', 'no @, <, >, backticks or backslashes', 'Backstory: {error}.', 'Handle: {error}.', 'Orders: {error}.'", "Dynamic validator output; must stay unambiguous."),
 ("privacy-labels", "'Private (only you see this)', 'Comfort:', 'Survey:', 'BUILD (so far)', '(incomplete)'", "Clarity on the review screen; a joke there could hide what is private."),
 ("staff-messages", "Reviewer/owner messages: 'Only the table owner or a listed reviewer can do that.', 'Nothing is waiting for review.', 'Name the player.', 'No filed draft from that player.', 'Pick a screen from S2 to S16.', 'Sent <name> back to <screen>.', 'Could not register: ...', 'Approved <name>...', '<name> is filed and waiting for review...', 'New Crawler registered: ...'", "GM-facing admin text. The player-facing outcome lines (registered, held, returned) are already flavored."),
 ("already-flavored-messages", "'Resume your intake?' / 'Start over', 'This is not your intake booth.', 'No Crawler or draft of yours in this session.', 'Changed your mind? These picks no longer apply and were cleared: ...', 'Your build is already cleared. Run /create to start fresh.', 'Comfort answers saved.', 'Rename your junk' modal (legacy), 'Cosmetic. Holds nothing special.'", "Already System-voiced or functional."),
 ("species-skill-and-fixed-lines", "'Pick your <species skill label>', 'Fixed: ...', 'Picks: ...', 'Proficiency Bonus +2' on S9", "Species-derived text and fixed numbers. The Proficiency Bonus label is flavored only in the S8 preview block."),
 ("class-and-species-and-background-names", "S5/S6/S7 species, class, class-option and background names", "Done in species-class-reskins.json and background-reskins.json. Not duplicated here."),
 ("item-names", "All item and weapon names on S10", "Done in item-reskins.json."),
 ("select-values-and-ids", "Select option values, custom ids, draft field names, screen ids S1..S17", "Code ids. Display only changes."),
]

AUDIT += [
 ("plain-views", "S1, S2, the comfort-only view and the S13 survey: every shared (screen ALL) row is skipped there (rows carry plain_on), and the S13 buttons/help are not rewritten", "S2 says 'we won't joke about it'; the survey and comfort views are private and safety-adjacent (Syndicate F2). Nav labels such as Blow It Off, Walk Away and Stash and Step Out never show there."),
 ("titles-s13-s15", "Titles 'Customer survey (private notes)' (S13) and 'Standing Orders, Reactions, signature attack' (S15)", "S13 is a plain view; S15 is made of glossary terms. Both feed the S16 'Edit a screen' menu unchanged."),
 ("modal-and-field-labels", "S8 enter-scores modal title 'Ability scores' (covered by title-s8), S10 shop modal 'Intake Vending Wall' and its field 'One per line: name, then quantity ({credits} credits)', S13 modal 'Customer survey', S14 fields 'What you did before the crawl (public)' and 'Requested Handle (optional)', S15 fields 'Standing Orders', 'Standing Reactions', 'Signature attack name (optional)'", "Glossary terms, input-format hints and privacy words ('public'); already System-voiced. Plain on purpose."),
 ("money-cp-rule", "RESOLVED (Caleb, 2026-10-04): copper prices on the Price list and variant descriptions", "Rule: 1 credit = 1 GP (Core 5.10) and 1 cp = 0.01 credit. Whole credits print without decimals (15 credits), fractions with decimals (0.5 credit, 0.05 credit); 'credit' singular for 1 or less. Covered by rows hint-money-gp and hint-money-cp. Starting-package amounts are whole credits."),
 ("embed-header-and-round-header", "Embed header '{screen} · {title}' and the roll headers 'Round N.'", "The {title} is already the reskinned title row; the round header is roll-log wording."),
 ("rule-statement-messages", "'Your gear still has an unresolved type (...); go back to S10 and pick it.', 'The registry refused the file: ...', the '• S9: ...' list lines, 'CRAWLER #PENDING'", "State facts or staff/registry output; a joke would hide the cause."),
 ("pact-of-the-chain", "Pact of the Chain keeps the word 'familiar' (opt-invocation-pact-of-the-chain)", "Caleb/Syndicate: it is the real invocation, not a pet prompt."),
]
