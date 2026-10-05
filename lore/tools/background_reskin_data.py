"""Data for background-reskins (display-name layer for the /create S7 'Prior Employment' screen; rules untouched).
Row: (id, kind, parent_id, srd_name, chargen_value, display_name, flavor[, label_name])
 kind: background | choice
 parent_id: None for backgrounds; for choices the S7 group key: origin-feat | background-asi | background-kit
 chargen_value: exact string in chargen-5e.json (background key, origin_feats entry, package id) or the spec string for the ASI picks
 label_name (optional): short 5e name used in combined_label when srd_name itself contains parentheses (no nested parentheses)
Voice: prior jobs that went badly, modern Earth, petty and funny. One industry and one punchline per entry. Adults-only table.
"""
ROWS = [
# ---------------- 16 backgrounds (chargen-5e.json backgrounds; the placeholder 'job' there is kept in chargen_job by the build)
("acolyte","background",None,"Acolyte","Acolyte","Youth-Group Pizza Wrangler","Ran Wednesday-night youth group on two pizzas and divine patience. Found out heaven has no petty credits."),
("artisan","background",None,"Artisan","Artisan","Etsy Shop Founder, Three Sales","Your handmade candle empire grossed 41 dollars, and 40 of it was your mother. The glue gun is still plugged in."),
("charlatan","background",None,"Charlatan","Charlatan","Pyramid-Scheme Boss Babe","Sold leggings, essential oils and a dream to everyone you ever met. Your upline still posts about your journey."),
("criminal","background",None,"Criminal","Criminal","Call-Center Gift-Card Fraud Specialist","Talked 400 strangers into reading you their card numbers 'for verification'. Your headset is evidence now."),
("entertainer","background",None,"Entertainer","Entertainer","Wedding DJ With One Playlist","Played the Cupid Shuffle at nine years of receptions, and the bride's dad still found a reason to be mad."),
("farmer","background",None,"Farmer","Farmer","Farm-to-Table Influencer","Fourteen thousand followers, one goat, zero crops. The goat has the better engagement rate."),
("guard","background",None,"Guard","Guard","Hospital Parking-Garage Attendant","Defended a ticket machine from nine thousand people with 'no change'. The boom gate is your only friend."),
("guide","background",None,"Guide","Guide","Trailhead Guide With a Laminated Map","Led conga lines of tourists up a hill swearing it was 'only ten more minutes'. It was never ten minutes."),
("hermit","background",None,"Hermit","Hermit","Doomsday Prepper, Collapse Postponed","Stockpiled four years of canned beans and a bunker for an apocalypse that got canceled for weather."),
("merchant","background",None,"Merchant","Merchant","Warehouse Operations Manager","Ran a million-square-foot warehouse by calling people family and rationing bathroom breaks. HR has a binder with your name on it."),
("noble","background",None,"Noble","Noble","Trust-Fund Gallery Owner","Opened a gallery to show your own paintings with your grandmother's money. Sold exactly one, to your grandmother."),
("sage","background",None,"Sage","Sage","Adjunct Professor on Four Campuses","Taught intro rhetoric at four colleges for the combined salary of one decent sandwich. Parking cost more than the pay."),
("sailor","background",None,"Sailor","Sailor","Cruise-Ship Buffet Deckhand","Mopped a buffet line the length of a football field. You can identify a norovirus rumor by sound alone."),
("scribe","background",None,"Scribe","Scribe","Law-Firm Paralegal in Redline Hell","Highlighted 'herein' eleven thousand times and billed in six-minute increments. Your wrist has a pension plan."),
("soldier","background",None,"Soldier","Soldier","Black-Friday Mall Security","Stood between a discount toaster and four hundred people. You lost the toaster but kept the vest."),
("wayfarer","background",None,"Wayfarer","Wayfarer","Couch-Surfing Burrito Courier","Delivered dinners by day and slept on six couches a month. Your car smells like both, and you know every sofa in three counties."),
# ---------------- origin feats (chargen-5e.json origin_feats; shown on S7 for each background and for Human's extra feat)
("feat-alert","choice","origin-feat","Alert","Alert","Night-Shift Insomniac","Hasn't slept through the night since the 2019 inventory audit. Nothing sneaks up on someone who counts ceiling tiles."),
("feat-crafter","choice","origin-feat","Crafter","Crafter","Hot-Glue Gunslinger","Fixes everything with a glue gun and optimism. The repair holds until it is looked at."),
("feat-healer","choice","origin-feat","Healer","Healer","Weekend CPR-Class Graduate","Passed a two-hour course on a dummy named Annie. Everybody's choking is now your business."),
("feat-lucky","choice","origin-feat","Lucky","Lucky","Scratch-Ticket Gambler","Never won more than twelve dollars. Somehow always the twelve you needed."),
("feat-magic-initiate-cleric","choice","origin-feat","Magic Initiate (Cleric)","Magic Initiate (Cleric)","Group-Chat Prayer Warrior","Types 'thoughts and prayers' faster than anybody alive. Surprisingly, some of them land.","Magic Initiate, Cleric"),
("feat-magic-initiate-druid","choice","origin-feat","Magic Initiate (Druid)","Magic Initiate (Druid)","Houseplant Whisperer","Talks to a pothos nine times a day. The pothos has opinions about your landlord.","Magic Initiate, Druid"),
("feat-magic-initiate-wizard","choice","origin-feat","Magic Initiate (Wizard)","Magic Initiate (Wizard)","Wikipedia Rabbit-Hole Scholar","Started on 'lasagna' and finished on medieval siege engines at 4 AM. Knows one real spell and no lasagna recipe.","Magic Initiate, Wizard"),
("feat-musician","choice","origin-feat","Musician","Musician","Karaoke Night Regular","Owns the Wednesday slot and a laminated song list. Has been asked to stop, kindly, by four different bartenders."),
("feat-savage-attacker","choice","origin-feat","Savage Attacker","Savage Attacker","Drive-Thru Fry-Station Veteran","Survived a Friday rush on a fryer with a mind of its own. When you strike, you strike twice for good measure."),
("feat-skilled","choice","origin-feat","Skilled","Skilled","Tech-Support Jack-of-All-Trades","Fixed printers, passwords and one marriage over a screen-share. Have you tried turning it off and on again?"),
("feat-tavern-brawler","choice","origin-feat","Tavern Brawler","Tavern Brawler","HOA-Meeting Brawler","Got into a fistfight over a mailbox color at a public hearing. The minutes are still being disputed."),
("feat-tough","choice","origin-feat","Tough","Tough","Gym Bro Who Spots at Dawn","Lifts at 5 AM and tells everyone about it. Your hit points are made of protein powder and spite."),
# ---------------- the ability bonus pick on S7 (spec S7 'ASI choice (2024)')
("asi-2-1","choice","background-asi","+2 / +1","+2 / +1","Merit Raise and a Gift Card","Two points to one stat, one point to another. Management called it recognition."),
("asi-1-1-1","choice","background-asi","+1 / +1 / +1","+1 / +1 / +1","Everyone Gets a Participation Trophy","One point to each of the three stats the job listed. Nobody wins, and everybody gets a little something."),
# ---------------- starting-gear packages (chargen-5e.json backgrounds.*.packages: id A = the listed items, id B = the 50 GP option)
("package-a","choice","background-kit","Package A","A","Cardboard Carton From Your Desk","Whatever you carried out the front door when they walked you out. It is mostly yours."),
("package-b","choice","background-kit","Package B","B","Severance Envelope, Unmarked","Credits in hand, no gear, and a note that says 'good luck'. Shop at the Vending Wall and hope."),
]
