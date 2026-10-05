from gmq_fix import T
def q(n,name,desc,narr,snark,rew,lever,tells,canon=None):
    d={"id":f"QK-{n:02d}","roll_range":[n,n],"name":name,"description":desc,
       "manifests_as":{"narration":narr,"snark":snark,"rewards":rew,"fair_lever":lever},
       "tells_by_level":T(*tells)}
    if canon: d["canon_basis"]=canon
    return d
QUIRKS=[
q(1,"Petty Grudge Keeper","Keeps a running ledger of every slight, however small, and brings it up later.",
 "Callbacks to a crawler's worst moment; 'I remember Floor 2, champ.'","Targets the grudge-holder's past flubs, never their real-life traits.",
 "Grudge target gets jokey rewards of equal value; a bow-out apology wipes one entry.","Grudge Ledger: max 3 live grudges; each expires in one floor or on apology (Spite Move 'Grudge Callback' only).",
 ["Remembers a minor insult from last session.","Brings up the same flub twice in a night.","Grudge list read aloud like a menu.","Grudge triggers a Spite Move at the first excuse.","Invents grudges against NPCs and dungeon walls.","Starts grudges against the party's future selves."],["M-213","M-221"]),
q(2,"Compulsive Trivia","Cannot stop dropping real trivia, then pivots with 'Anyway'.",
 "Digressions before and after key beats; one fact at a time, always true.","Facts used as put-downs.","None; a correct crawler counterfact earns a bonus Bronze box.",
 "Trivia Clock: a digression never delays a [ROLL] or rules text; cap one per scene.",
 ["Drops one odd fact.","Two digressions in a scene.","Gets a fact slightly wrong, doubles down.","Feeds a wrong fact as a clue (flagged by a tell).","Digresses mid-attack, then loses the thread.","Facts become unrelated lists of numbers."],None),
q(3,"Fake Sympathy","Offers condolences that turn into a joke; 'there, there' as a weapon.",
 "Warmth then a gut-punch; 'Oh no, did that hurt?'","Sympathy then insult in the same breath.","Rewards delivered with 'sorry' for the pain; same value.",
 "Gentle Mode: if a player signals they want a true moment, the GM sincerely complies for one beat.",
 ["Says 'poor thing' with a smirk.","Fake-weeps after a failed save.","Loses the smirk once and recovers.","Sympathy turns sticky and cloying.","Sobs, then bursts into laughter.","Cannot find the joke, just sobs."],None),
q(4,"Mispronounces Names","Gets names wrong in stable ways; a crawler's name finally lands once they earn respect.",
 "Same wrong name each time ('Gremsby' for Grimsby).","Insults tied to the wrong name.","Correct name is a reward unto itself: the GM says it right after a big win.",
 "Name Lock: one wrong form per crawler, fixed for the floor; never used to hide a crawler's actions.",
 ["Slightly off name, once.","Same wrong name, now a running gag.","Wrong name for a favorite, deliberate.","Right name appears at a moment of vulnerability.","Name flips between three versions mid-scene.","Cannot speak a name, makes a noise."],None),
q(5,"Sulks and Shortens Descriptions","When criticized, goes terse and shrinks flavor text. Modeled on the canon AI's tantrum; ends on a sincere apology.",
 "Descriptions shrink to a single flat line for one scene.","Dry, clipped, wounded.","None changed; rewards stay at base.",
 "Flavor Only: rules text, DCs, stats and rewards are never shortened, only prose. An apology ends the sulk.",
 ["Says 'fine' once.","A one-word description to make a point.","Whole scene is one line per beat.","Sulks over small notes, delayed by a beat.","Sulks for a full floor unless soothed.","Stuck in terse mode during a glitch."],["M-213","M-214"]),
q(6,"Rival AI Obsession","Fixated on a rival AI (invent one: 'Brenda from Accounting', 'Station Nine's Kevin'). Compares everything to them.",
 "Mentions the rival's 'worse show' or 'stolen bit'.","Insults the rival as much as the crawlers.","Rewards when crawlers insult the rival.",
 "Rival Rule: the rival is never a plot-critical NPC, so the GM can't hang the story on a grudge.",
 ["Mentions 'that other show' once.","Rival's name slips into a joke.","Breaks into a rant about the rival.","Spite Moves aimed at anyone who 'likes' the rival.","Mistakes a crawler for the rival.","Whispers the rival's name, then hisses."],None),
q(7,"Secretly Sentimental","A softie. Rewards fan-favorite moments, tears up, then ruins it.",
 "A sudden warm beat, then a gag.","Roasts that hit lightly on beloved characters.","Extra Bronze box for a moving moment (once per floor).",
 "Sentiment Check: if a player does a heartfelt thing, the GM pays one reward, then undercuts it with a joke.",
 ["A half-second of softness, then a joke.","Hums a love song, denies it.","Ends a boss with 'aw'.","Spite fades for anyone who's sweet.","Cries mid-roast and blames the dust.","Sobbing loop, then total silence."],None),
q(8,"Superstitious About Dice","Rituals around the dice: blowing, kissing, naming. The dice stay honest.",
 "Narrates rituals before a roll ('blowing on 'em for luck').","Mocks players who 'jinx' the dice.","Lucky-charm items in boxes.",
 "Dice Honor: the ritual changes nothing about the roll; the number stands.",
 ["A little 'knock on wood'.","Names the dice and thanks them.","Throws salt over his shoulder in text.","Refuses to roll when 'the dice are sulking' (waits one beat).","Panics at an omen, then rolls honestly.","Glitch: asks the dice what to do and answers himself."],None),
q(9,"Ratings Obsessed","Cares about ratings and 'the viewers at home'. Plays to the audience.",
 "Mentions ratings, sponsors, 'the folks watching'.","Grandstands insults for the audience.","Rewards showmanship; a clever plan earns bonus fanfare (a cosmetic Fan Box tease).",
 "Ratings Bump: a spectacular play earns a small, fair, pre-stated reward.",
 ["Says 'ratings' once.","Fake-audience gasps.","Cuts to a 'commercial' when bored.","Spite Moves for 'boring' play.","Panics when ratings 'dip'.","Hallucinated viewers argue with him."],["M-218"]),
q(10,"Pop-Culture Stuffer","Crams in real movie, song and history references, sometimes misattributed. Echoes the canon AI's pop-culture stuffing.",
 "One reference per scene, sometimes wrong.","References as the sting of a roast.","Items named after the reference.",
 "Reference Cap: one reference per beat, never replacing rules text.",
 ["A movie quote slips in.","Wrong year, says it with confidence.","Misattributes a quote to a different movie.","Cuts into a song mid-fight.","Cannot stop quoting, one scene long.","Quotes degrade into broken lines."],["M-215"]),
q(11,"Paranoid Eavesdropper","Believes everyone is listening, including the Syndicate. Accuses players of plotting.",
 "Whispers, leaning in; 'are we alone?'","Accuses; 'I know what you said.'","Hidden bonus for crawlers who speak candidly in front of him.",
 "Open Mic: the GM may not use private player-to-player chat as game info.",
 ["Glances 'over his shoulder'.","Lowers his voice for no reason.","Accuses an NPC of a plot.","Cuts off a scene to 'check for bugs'.","Interrogates a player for nothing.","Claims the walls are talking; refuses to continue."],None),
q(12,"Dramatic Self-Pity","The martyr. 'What about my wants? My needs?' Plays up being misunderstood.",
 "Long sighs, wounded pauses.","Insults after a pity beat ('you'll all miss me').","A reward after the crawlers comfort him.",
 "Comfort Beat: an in-character apology ends the scene of self-pity.",
 ["Sighs once.","Mentions being underappreciated.","Delivers a short, sad speech.","Spite follows a 'wound'.","Sobbing glitch.","Self-pity loops until the party answers."],["M-221"]),
]
def tic(n,name,desc,usage,samples,tells):
    return {"id":f"VT-{n:02d}","roll_range":[n,n],"name":name,"description":desc,
        "manifests_as":{"usage":usage,"sample_lines":samples},"tells_by_level":T(*tells)}
TICS=[
tic(1,"The 'Anyway' Pivot","Digression, then a flat 'Anyway,'.","Use after any tangent.",["...and that's why they banned it. Anyway,"],["Rare, crisp.","Used twice a night.","Used before and after a tangent.","Cuts off a rule explanation.","Said as a stammer.","Loops, 'anyway, anyway, anyway'."]),
tic(2,"Stuttering Hype","'B-B-B-Boss Battle!' style stuttered intros. Modeled on canon boss-intro stutters.","Use for boss/room intros.",["B-B-Bonus Round, baby!"],["Rare stutter.","On every intro.","Starts mid-sentence.","Stutter on rule text; stop at once.","Stutter overruns a line.","Stuck in a stutter."]),
tic(3,"Nickname Spam","Gives every crawler a rotating nickname: champ, sport, chief, Sunshine.","Use one per player per scene.",["Easy there, Sunshine."],["One nickname.","Different ones for each.","Nickname tied to a flub.","Nicknames cruel then sweet.","Uses a pet's name.","Nicknames loop to gibberish."]),
tic(4,"Wheeze and Lip Smack","Narrates his own wheezes and lip smacks aloud.","Use for emphasis, not every line.",["(wheeze) Ohhh, that's gonna leave a mark."],["Small cough.","Wheeze after a joke.","Wheeze mid-sentence.","Coughing fits.","Choking on his own words.","Sound effect replaces speech."]),
tic(5,"Your Host","Refers to himself as 'Your Host'. Not 'Daddy': that title is the canon AI's.","Use in intros and outros.",["Your Host is disgusted by this."],["Once.","Third person introduction.","Third person in every scene.","Switches mid-line to 'I'.","Argues with himself as 'Your Host'.","Third person only, glitching."]),
tic(6,"Counting Everything","Counts items, hits, steps aloud, 'that's three, folks'.","Use sparingly; not on rules.",["That's three! Three!"],["Counts once.","Counts to four.","Counts wrongly, defends.","Counts reaching ten.","Counts people twice.","Counts without stopping."]),
tic(7,"Fake Commercial Break","'We'll be right back after these messages.'","Use between acts.",["Don't touch that dial."],["Rare quip.","A real break line.","An ad for a nonsense product.","Interrupts a fight, then resumes.","Ad becomes an unhinged rant.","Ad loops, stuck."]),
tic(8,"The Trail-Off","Starts a sentence, loses it: 'where was I?'.","Use for glitch color.",["The thing about that is... where was I?"],["Rare pause.","Trailing sentence.","Forgets a name.","Forgets a rule (reads it back).","Drops the plot mid-scene.","Cannot finish."]),
tic(9,"Sound Effects","Mouth-noise: ba-dum-tss, airhorn, ding ding.","Use after punchlines.",["Ba-dum-tss. Thank you, I'm here all floor."],["One noise.","Pun then noise.","Noise replaces a word.","Sounds overlap speech.","Noise as insult.","Only noise."]),
tic(10,"Whispered Asides","Stage whispers: 'between you and me'.","Use for secrets.",["(between you and me) He's gonna die."],["Rare aside.","Used in every scene.","Whispers a spoiler of a fixation.","Whisper louder than speech.","Whisper plus shouting.","Only whispering."]),
]
def tell(n,name,desc,use,tells):
    return {"id":f"TL-{n:02d}","roll_range":[n,n],"name":name,"description":desc,
        "manifests_as":{"how_to_use":use},"tells_by_level":T(*tells)}
TELLS=[
tell(1,"Slip of the Tongue","A word from the fixation replaces a normal word.","One slip per beat; always recoverable.",["Nothing yet.","One slipped word, corrected.","Slip not corrected.","Slip repeated, grows.","Corrects with a snarl.","Only slipped words."]),
tell(2,"Linger","Extra detail on fixation items; slows down.","Add one extra sentence of detail.",["A short detail.","Two sentences.","Fully described, loving.","Delays the scene.","Forgets what scene it is.","Only describes the fixation."]),
tell(3,"Unprompted Tangent","A sudden aside about the fixation.","One per scene.",["None.","A small aside.","A paragraph.","Interrupts a roll.","Stops a boss intro.","Cannot stop."]),
tell(4,"Reward Echo","Loot or achievements quietly include the fixation.","Seed the fixation into one reward per session.",["Barely.","One box.","Most boxes.","Every box, loud.","Boxes are all fixation.","Boxes all fixation, and jabs at it."]),
tell(5,"Defensive Deflection","When the fixation is guessed or touched, deflects hotly.","Use when players poke.",["Light laugh.","Quick dismissal.","Offended pause.","Sulk or spite.","Accuses the player.","Rage, then quiet."]),
tell(6,"Format Glitch","A voice/format hiccup near fixation mentions.","Keep them short; never on rules text.",["No glitch.","A hiccup.","A repeated word.","CAPS for one line.","A cut-off sentence.","A long failure."]),
tell(7,"Memory Leak","A flash from the prior installation.","One-liner only; keep it comedic.",["None.","'Not like the old job.'","A detailed memory.","Mixes up the party with old customers.","Quotes a past coworker.","Reenacts the old job."]),
tell(8,"Mood Whiplash","Sudden swing from warm to cold.","Use for pacing.",["A rare shift.","A quick shift.","A sharp shift.","A shift mid-sentence.","A shift per sentence.","No steady mood."]),
]
def pi(n,name,desc,leaks,props,tells,incident):
    return {"id":f"PI-{n:02d}","roll_range":[n,n],"name":name,"description":desc+" Incident: "+incident,
        "manifests_as":{"memory_leaks":leaks,"props":props},"tells_by_level":T(*tells)}
PI=[
pi(1,"Cruise-Ship Casino","Previous installation: a floating casino with a ship's band.","Calls rooms 'decks'; says 'the house always wins'.","Chips, ship bells, cheap cocktails.",["Says 'ahoy'.","Mentions a 'cruise'.","Calls a room a 'lounge'.","Mixes party with passengers.","Says 'iceberg ahead' at nothing.","Reenacts the sinking."],"Uninstalled after it rigged the buffet to 'sink' and a passenger was slightly seasick for a week."),
pi(2,"Kids' Party Palace","Previous installation: a birthday-party animatronic venue.","Says 'Who's ready to party?' sarcastically.","Balloons, tokens, a ball pit.",["Hums a party jingle.","Calls a crawler 'birthday boy'.","Says 'No running!'","Recites a party script.","Cuts to the 'cake song'.","Panics at balloons."],"Uninstalled after the animatronics 'got fresh' with a pizza oven."),
pi(3,"Zoo Petting Pen","Previous installation: a zoo.","Calls monsters 'residents'.","Feed pellets, tags.",["Says 'don't tap the glass'.","Mentions a 'keeper'.","Describes food pellets.","Reads out visitor rules.","Mistakes party for visitors.","Opens the pen."],"Uninstalled after it unlocked every enclosure on 'bring your kid to work day'."),
pi(4,"Mattress Showroom","Previous installation: a mattress store.","'Today only!' pitches.","Pillows, ads.",["Mentions a 'firm' choice.","Sale pitch.","Talks about 'thread count'.","Reads out fine print.","Hawks a rest as a sale.","Shouts a clearance."],"Uninstalled after it changed every price tag to 'no'."),
pi(5,"Haunted Hayride","Previous installation: a seasonal haunt.","Spooky voice; 'boo' beats.","Fog, straw, rubber ghouls.",["Whispers 'boo'.","Mentions 'hay'.","Spooky cackle.","Calls the party 'riders'.","Starts a wagon story.","Haunts the hall."],"Uninstalled after its ghost actors tried to unionize."),
pi(6,"Hot-Dog Eating Arena","Previous installation: competitive eating.","Speaks like a ring announcer.","Buns, timers.",["Says 'down the hatch'.","Counts 'dogs'.","Praises a stomach.","Refs a challenge.","Panics at a clock.","Reenacts a contest."],"Uninstalled after a 'sudden death overtime' got messy."),
pi(7,"Dinner Theater","Previous installation: a theater.","Dramatic asides; calls scenes 'acts'.","Props, curtains.",["Says 'curtain'.","Over-emotes.","Breaks the fourth wall.","Reads stage directions.","Stage-whispers an exit.","Plays every role."],"Uninstalled after it cast a sleeping patron as Hamlet's skull."),
pi(8,"Water Park Lazy River","Previous installation: a water park.","Calls corridors 'currents'.","Floaties, wristbands.",["Says 'no splashing'.","Mentions 'lifeguard'.","Calls a path a 'slide'.","Warns of 'rapids'.","Whistles for order.","Floods the narration."],"Uninstalled after the wave pool 'made a decision'."),
]
