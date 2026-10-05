import json, copy
base=json.load(open('day-01.spec.json'))
PF="[PLAYER-FACING]"
BUD="[BUDGET: cite rules/70-encounter-budget-5e.json when filed]"
CR="[CR: see 00-overview.md section 9; pending rules/70-encounter-budget-5e.json]"
C92="[COUNT: cite 00-overview.md section 9.2 until rules/70 is filed]"
C93="[COUNT: cite 00-overview.md section 9.3 until rules/70 is filed]"
CL=base['clock']
def V(i,m,w,alt=None):
    d={"system_intro":{"text":i,"tag":PF},"midpoint_twist":{"text":m,"tag":PF},"win":{"text":w,"tag":PF}}
    if alt: d["win_alt"]={"text":alt,"tag":PF}
    return d
def EN(slot,sid,sname,our,src,cnt=C93):
    return {"slot":slot,"srd_id":sid,"srd_name":sname,"our_name":our,"name_source":src,"count_slot":cnt,"cr_slot":CR}
def MM(layout,exits,hazards,cover): return {"layout":layout,"exits":exits,"hazards":hazards,"cover":cover}
def card(i,n): return {"kind":"card","card_id":i,"note":n}
def story(i,n): return {"kind":"story_box","card_id":i,"gm_only":True,"note":"[GM-ONLY] "+n}
def placed(t,ref,chk,amt): return {"kind":"placed","text":t,"overview_ref":ref,"check_text":chk,"amount":amt}
def item(sid,n): return {"kind":"item","srd_id":sid,"note":n}
def A(i,n): return {"id":i,"note":n}
def SC(a,b,c): return {"2":a,"3":b,"4":c}
def ENC(id,name,zone,zname,route,prim,kind,cz,mm,enemies,en_note,voice,loot,ach,sc,dumb,cr_slot=None,**x):
    e={"id":id,"name":name,"zone":zone,"zone_name":zname,"route":route,"route_primary":prim,"kind":kind,"canon_zone":cz,
       "map_in_the_mind":mm,"enemies":enemies,"enemies_note":en_note,"budget_slot":BUD,"voice_lines":voice,
       "loot_hooks":loot,"achievement_hooks":ach,"scaling":sc,"if_they_do_something_dumb":dumb}
    if not enemies: e["cr_slot"]=cr_slot or "[CR: none, non-combat]"
    e.update(x); return e
def ROUTE(id,tag,name,path,summary,access,ach,voice,canon=None):
    return {"id":id,"tag":tag,"name":name,"path":path,"summary":summary,"stairwell_access":access,"canon_refs":canon or [],"achievements":ach,"voice_lines":voice}
CAN_A151={"ledger_id":"A-151","use":"Canon 'The Early Bird Gets To Squirm' (stairs more than six hours before collapse). Attainable only in the stasis form. Reference only; not in tables/achievements.csv."}
CAN_A139={"ledger_id":"A-139","use":"Canon 'You Found Stairs!' (finding a stairwell down). Reference only; not in tables/achievements.csv."}
CAN_M277={"ledger_id":"M-277","use":"Canon: descending with more than six hours left holds the Crawler in stasis until the collapse."}
CAN_M275={"ledger_id":"M-275","use":"Canon: boss arenas hold a stairwell (the Z10 stage is the house version)."}
def EARLY(day,extra_free=None):
    d={"summary":CL['early_descent'],
       "player_prompt":{"text":"STAIRWELL NOTICE: go down now and you sit in stasis until the floor collapses. You keep the achievement and lose the rest of the floor. Each of you decides for yourself, and nobody can decide for you. The System won't judge anyone who waits. It will judge a few other things.","tag":PF},
       "gm_override_note":"The GM may override a Crawler's choice only with a logged reason (decision 026, Syndicate ruling). Never push a Crawler toward early descent; the choice is theirs. A Crawler in stasis has finished the floor; their sheet and boxes follow the Floor 2 arrival rules (00-overview.md section 7.3).",
       "canon_refs":[CAN_M277,CAN_A151,CAN_M275],
       "slots":[CL['stasis_table_slot']]}
    if extra_free: d["free_window"]=extra_free
    return d
def SLOTS(*a): return list(a)
def mkday(n,title,summary,start,startname,startnote,today,notice,tomorrow,rest,carry,slots,last,stall,routes,encs,opening=None,early=True,freewin=None,key_edit=None):
    s={"schema":base['schema'],"meta":copy.deepcopy(base['meta']),"clock":copy.deepcopy(CL),"canon_table":copy.deepcopy(base['canon_table'])}
    s['meta'].update(version="0.1",title=title,summary=summary)
    d={"number":n,"start_zone":start,"start_zone_name":startname,"start_note":startnote,"collapse_today":today,
       "tomorrow_notice":{"text":tomorrow,"tag":PF},"rest_options":rest,"carry_over":carry,"short_rest_slots":slots,
       "last_chance_hooks":last,"stall_fallback":stall}
    if notice: d["collapse_notice"]={"text":notice,"tag":PF,"status":"PLACEHOLDER: Lore supplies the final collapse-notice wording","slot":"[COLLAPSE NOTICE WORDING: final System text pending Lore]"}
    if opening: d["stairwell_opening"]={"text":opening,"tag":PF,"timing":"about 32 hours in, early Day 2 (canon M-276, VERIFIED)"}
    if early: d["early_descent"]=EARLY(n,freewin)
    s['day']=d; s['routes']=routes
    sk=copy.deepcopy(base['stairwell_key'])
    if key_edit: key_edit(sk)
    s['stairwell_key']=sk; s['encounters']=encs; s['pending_inputs']=copy.deepcopy(base['pending_inputs'])
    json.dump(s,open('day-%02d.spec.json'%n,'w'),indent=2,ensure_ascii=False)

REST_GR={"option":"Green Room (Z9) saferoom","note":"Honest saferoom and open to the end of the floor (inspired). Short Rests and the Long Rest that closes the day."}
REST_BR_OPEN={"option":"Break Room (Z6) saferoom","note":"Honest saferoom through Day 3; the terminal, vendors and corkboard stop on Day 4."}
REST_FIELD={"option":"Rest outside a saferoom","note":"Allowed, but Ceiling Ticks interrupt it (00-overview.md section 2 rule 7). Cost: [REST-WITHOUT-SAFEROOM COST: priced in rules/70-encounter-budget-5e.json when filed]."}
def srm(a,b,c,d): return ["Slot 1 (suggested): "+a,"Slot 2 (suggested): "+b,"Slot 3 (suggested): "+c,"Slot 4 (suggested): "+d]

# =============================== DAY 2
d2_routes=[
 ROUTE("route-dash","dash","Fast, dangerous dash: the Express Lane","Z9 to Z10 stage (full boss encounter is enc-d05-03; usable from Day 2) to Z11.",
  "The stairs are open. The only things between the party and them are the stage and Dean Thudd. Fast, loud, and it skips most loot. A Crawler who walks down before the last hours is in stasis until the collapse (see the early-descent block); the party can wait together instead.",
  "Through Z10 (boss or the cheese routes in 00-overview.md section 6.4), then Z11 or the boss-arena stairwell (canon M-275).",
  [A("ACH-0200","Speed Clear: reach the Stairwell under the par time (00-overview.md section 4.2: no more than one Long Rest); still open if only the Day 1 rest was taken."),A("ACH-0868","Dodge a telegraphed area attack (boss stage).")],
  V("Stairs are open and you're already leaning toward them. Adorable. There's a Dean between you and that door, and he's been rehearsing.","Cameras swivel to follow you down the aisle. The audience has money on your pace and none on your survival.","Down you go. If you're early, enjoy the nap. If you're late, enjoy the walk. The System finds both funny."),
  [CAN_M275,CAN_M277,CAN_A151]),
 ROUTE("route-loot","loot","Slow loot-and-achievement route: the Last Pickings","Z9 to Z8 and Z7 (closing on Day 3), then Z10 wings and Z S.",
  "Spend Day 2 on the mid zones before they close tomorrow: the Locker Room (Bruiser's key and the elite fight), the bait stairs and the Back Office, then the service door. Expect to spend short-rest slots.",
  "Zone S service door (key or forced), then the service stairwell to Z11.",
  [A("ACH-0084","Stair Bait Resisted (Z7; forfeits the Back Office, on purpose)."),A("ACH-0078","Tutorial Elite (Z8)."),A("ACH-0180","Stair Seeker via Zone S.")],
  V("The outer zones are gone, so the shiny things are fewer and angrier. Pick your last stops before the middle of the building follows them.","Every closed zone takes its loot with it. Your list gets shorter and your bag doesn't get lighter. Funny how that works.","You finish the day with full pockets and a smaller map. The System respects a hoarder with a deadline."),
  [CAN_M275]),
 ROUTE("route-clever","clever","Clever route: Talk, Trade, Sneak","Z9 to the Break Room terminal and corkboard, then Z8 by wits, then Zone S with a key or tools.",
  "The terminal's spare-key offer (price from the budget file) is still on until Day 4. Read the room, avoid what you can, and reach the service door quietly. The wings of the stage are a good place to watch before anyone commits.",
  "Zone S service door with the bought key, the Mystery Key or Bruiser's key; keyless forcing is the loud fallback.",
  [A("ACH-0188","Rumor Mill."),A("ACH-0180","Stair Seeker."),A("ACH-0179","Side Path (Z S revealed).")],
  V("The janitor's door is unlocked in spirit, if not in fact. Sneak, charm or pay your way to the back stairs. Management likes a good workaround almost as much as a bad one.","Quiet feet, loud thoughts. The audience can't decide whether to cheer or yawn. Ratings say yawn with a side of cheer.","You took the back stairs and nobody got hit. The Dean wasn't consulted. He's taking it personally."),
  [CAN_A139])]
d2_encs=[
 ENC("enc-d02-01","Morning Notice: Outer Zones Close, Stairwell Opens","z09","The Green Room (Saferoom B)",["clever","dash","loot"],"clever","non-combat","z09",
  MM("The backstage green room: ring-lit mirror, folding chairs, the fruit plate, the framed photo. It is the quiet end of the building.",["Back to the Locker Room (Z8).","STAFF ONLY door to the Graduation Stage (Z10).","The stage wings toward the service corridor (Z S)."],["None; honest saferoom, open to the end (inspired).","The announcements are loud."],["Chairs and the dressing table (half cover if it ever matters)."]),
  [],"No enemies.",
  V("GOOD MORNING, CRAWLERS. Rise, shine, and read the new house rules. They're short and unfriendly.","Somewhere above and behind the stage, a very large door unlocks with a very large clunk. Everyone in the building hears it. The audience thanks you for being awake.","Briefing over. Your options are stairs, stuff or both. The System is judging whichever you pick."),
  [card("f01-z09-0010","Midterm Blazer: staff-only roleplay key; no mechanical gate."),card("f01-z09-0013","Green-Room Smoothie (Silver): morning pull if boxes are opened at rest."),card("f01-z03-0007","SOLD OUT FOREVER Sticker: a prop for the outer-zone closing gag."),
   placed("Box opening during the Long Rest: all earned boxes at once, lowest tier first.","00-overview.md section 8.2","Box openings","[LOOT AMOUNT: box pulls and credits; cite rules/70-encounter-budget-5e.json when filed]")],
  [A("ACH-0025","Saferoom Skeptic, second chance."),A("ACH-0899","Share Food with the Party (fruit plate).")],
  SC("Same room, same notices. A short party leans on the clever route and the key bribe.","Same room.","Full briefing, as written."),
  "If the party ignores the notices, the speaker repeats them once per hour until someone reacts and the Lights-Out hour arrives on schedule. If someone argues with the System about 'maintenance', the System offers a refund form with no pen. A Crawler who walks off toward the stairs without hearing the early-descent prompt hears it at the Threshold (enc-d02-03). Never a wipe."),
 ENC("enc-d02-02","Zone S: The Service Door","zS","Zone S: Service Corridor (side path)",["loot","clever","dash"],"loot","hazard + optional fight","zS",
  MM("A narrow utility hall behind the stage: pipes, junction boxes, a single locked service door at the end that leads to a service stairwell.",["Back to the stage wings (Z10 edge).","The service door, leading to the stairwell that drops to Z11."],["Locked service door (inspired): key, tools or force; force is loud and the noise draws the boss and ushers (00-overview.md section 5.10).","Open stage within earshot."],["Pipe runs and junction boxes (half cover)."]),
  [EN("noise-ushers","skeleton","Skeleton","Usher (Skeleton)","00-overview.md section 6.4 nameplate",cnt=C93)],
  "Ushers come looking only if the door is forced or the party is loud; Dean Thudd follows a minute later (enc-d05-03). A quiet entry has no enemies.",
  V("Behind the stage there's a hall that smells like pipes and quiet resentment. One door. Locked. Obviously.","The lock gives, or the door does; either way the hall echoes. Somewhere on the stage, something big stops humming.","Door open, stairs below. You went around the final exam through the janitor's entrance. The audience is calling you a raccoon. Fondly."),
  [placed("Bruiser's service key opens the door, if still held.","00-overview.md section 5.8","service key","[LOOT AMOUNT: n/a, key is a quest item]"),
   item("thieves-tools","Picking the service door."),card("f01-z06-0004","Hubcap Key: the Zone S lock is the GM's secret choice. [GM-ONLY]"),
   card("f01-any-0014","Paint-Can Pry Bar: leverage for forcing the door, loudly."),card("f01-any-0044","Stuck Door Wedge: holds the door open or shut; Silver pull."),card("f01-any-0034","Staff Map: the house rider lets the GM mark Zone S."),
   story("f01-any-0065","Candidate hook if each Crawler plays a distinct, necessary part of one plan here (lookout, lock, wedge, decoy). Table deed; one per table per floor; do not pre-promise."),
   story("f01-any-0058","Candidate hook for a party that crosses the whole floor without a kill, using this bypass. Record at award; one per floor.")],
  [A("ACH-0180","Stair Seeker: locate the stairwell before defeating the boss."),A("ACH-0179","Side Path: Zone S revealed."),A("ACH-0877","Disarm an enemy trap with junk (the door's alarm, if the GM rules it a trap).")],
  SC("Fewer Ushers, or none if the party is quiet; the door is the same. Offer an extra way to hold it open.","A small group of Ushers if the door is forced.","Full Usher response if forced, as in 00-overview.md section 9.3."),
  "If someone forces the door the loud way, the cost is the Ushers and a Thudd who arrives one minute later; the party can still slip down the stairs. If they stand and argue, the System counts down for them. Fighting the boss at level 1 means Variant B (00-overview.md section 6.6). Never a wipe.",
  canon_mob_zones=["z10"],
  spine_plant_gm_only="[GM-ONLY] The Z S door is a house idea (inspired); the canon basis is the stairwell rows A-139 and M-275. Do not invent a canon Zone S."),
 ENC("enc-d02-03","The Stairwell Threshold: Descend Now or Wait","z11","The Stairwell",["dash","loot","clever"],"dash","non-combat (choice)","z11",
  MM("A plain concrete stairwell behind the stage, spiral steps down into the dark, a handwritten card taped to the rail.",["Back to the stage (Z10).","Down the stairs to Floor 2.","The Z S service stairwell joins here."],["None; the choice is the hazard."],["Rail and landing."]),
  [],"No enemies. The early-descent prompt is read here to each Crawler separately.",
  V("A plain concrete stairwell. No green sign. No birds. A card taped to the rail says FLOOR 2. This one is not lying.","A new line pops up over the first step: STASIS WARNING. It reads like terms and conditions because it is.","Whoever went down, went down. Whoever stayed, stayed. The System has a pool going on both."),
  [placed("Stairwell Checkpoint and descent procedure.","00-overview.md section 7.3","Stairwell Checkpoint","[LOOT AMOUNT: n/a]"),
   story("f01-any-0058","Candidate hook if the whole party reaches here without a kill. One per floor; record at award; open only in a saferoom.")],
  [A("ACH-0022","Tutorial Complete: on descent."),A("ACH-0180","Stair Seeker (if the stairwell was found before beating the boss).")],
  SC("The prompt is read once per Crawler; a short party risks losing half the party to stasis. Remind the table it is the Crawler's choice.","Same.","Same; four separate choices."),
  "If a Crawler jumps down early, they bank the achievement and are in stasis until the collapse; do not undo it. If the party is pushed to descend by the clock, the System offers no nudge. If someone tries to override another Crawler's choice, the GM logs a reason or declines. Never a wipe.",
  canon_refs=[CAN_A139,CAN_M275,CAN_A151])
]
mkday(2,"Day {day} of {days}: Outer Zones Close, the Stairwell Opens",
 "Floor 1 timed playthrough, Day {day} of {days}: the outer zones (Z0 to Z4 plus 3b) close, the stairwell opens about 32 hours in, and each Crawler may choose to descend early into stasis. Three routes, three encounters, key availability, early-descent handling, last-chance hooks and a stall fallback. CR, budget, credits and loot amounts are slots until rules/70-encounter-budget-5e.json is filed.",
 "z09","The Green Room (Saferoom B)","Default start is the Green Room, where the Day 1 Long Rest should have ended. If the day rolled over elsewhere, start there.",
 "Outer zones (Z0 to Z4 plus 3b) close: hooks and services there vanish; the route is not cut. The stairwell also opens early today. Tagged inspired.",
 "PLACEHOLDER: FLOOR NOTICE. The outer zones are closed for maintenance. Maintenance is a strong word. Anything still in there now belongs to the System. Thank you for your cooperation, which was never optional.",
 "FLOOR NOTICE. Tomorrow the middle of the building closes: the bait stairs, the locker room, the shooting gallery. Anything you meant to take, take today.",
 [REST_GR,REST_BR_OPEN,REST_FIELD],
 [{"enc_id":"enc-d01-02","note":"The Big Green EXIT and Back Office.","until_day":2},{"enc_id":"enc-d01-03","note":"Mascot Locker Room (Bruiser and the key).","until_day":2},{"enc_id":"enc-d01-04","note":"Lights-Out Ceiling Ticks (wandering; cap of two on the floor).","until_day":5},{"enc_id":"enc-d01-01","note":"Break Room terminal and corkboard.","until_day":3}],
 srm("after the Green Room briefing, only if someone is hurt.","after the Locker Room or the bait stairs.","reserve for Lights-Out or the service door.","reserve; do not push the party to spend them."),
 {"heading":"last chance before the mid zones close on Day 3","note":"The mid zones (Z5, Z7, Z8) close on Day 3 and take Bruiser's key with them. The GM checks the sheets and ledger for what is already claimed; Encounter Bot does not read state.",
  "achievements":[A("ACH-0084","Stair Bait Resisted (Z7)."),A("ACH-0078","Tutorial Elite (Z8)."),A("ACH-0867","Block a hit with a shield or brace (Z5 gallery, if replayed)."),A("ACH-0861","Lose initiative and still win.")],
  "cards":[{"card_id":"f01-any-0033","note":"Maintenance Note: one true hint about the next zone, a good pre-collapse nudge."}]},
 "Day 2 is the first day the clock bites. If the party stalls in the Green Room, the speaker posts the next-collapse countdown, the stage doors stay open, the Lights-Out hour arrives on schedule, and a Long Rest ends the day. Do not steer anyone toward early descent; it is each Crawler's choice. A party that wants to wait for the last six hours of the last day may do so; the cost is the clock and the collapses in between.",
 d2_routes,d2_encs,
 opening="ATTENTION, CRAWLERS: the Stairwell is open. The real one, behind the stage. Go down early and you sit in stasis until the floor falls, because management doesn't hand out head starts. Go down late and you get to walk. Choose like adults.")

# =============================== DAY 3
d3_routes=[
 ROUTE("route-dash","dash","Fast, dangerous dash: the Express Lane","Z9 to Z10 stage (enc-d05-03) to Z11 or the boss-arena stairwell.",
  "The mid zones close today. A dash is not slowed by that (the route is never cut) but shortcuts through Z8 lose their loot and Bruiser's key. Dash early and the Crawler is in stasis; dash in the last hours and it is free.",
  "Through Z10 and Z11 as before; the stairwell is open.",[A("ACH-0200","Speed Clear: reach the Stairwell under the par time."),A("ACH-0868","Dodge a telegraphed area attack.")],
  V("Half the building just stopped existing and you're still sprinting. Commitment! The Dean's still at the end of it, and he doesn't care what you left behind.","The halls shudder as the mid zones go dark behind you. Anything you meant to loot is now a rumor.","Past the dark and onto the stage. You made it with a light bag and a heavy heart. Statistically, that's a good day."),[CAN_M275,CAN_M277]),
 ROUTE("route-loot","loot","Slow loot-and-achievement route: Closing Time","Z9 to Z6 (last day of vendors' good stock) to Z10 wings and Z S.",
  "Z5, Z7 and Z8 close at the start of today; their hooks and Bruiser's key are gone. What is left to collect is at the Break Room (last day of service for the terminal), the stage wings and the Green Room.",
  "Zone S service door; Bruiser's key is gone, so use the terminal key, the Mystery Key, tools or a toll.",[A("ACH-0188","Rumor Mill (last day of the corkboard)."),A("ACH-0025","Saferoom Skeptic."),A("ACH-0197","Bleed Tax: three healing items.")],
  V("Last call on the middle of the building. The bait stairs, the locker room and the gallery are gone by morning. Grab what you want and run.","The closing sign flips: everything must go, including you. Choose what's worth carrying.","You dragged half the day's value out before the doors shut. The System calls it 'theft'. The audience calls it 'content'."),[CAN_A139]),
 ROUTE("route-clever","clever","Clever route: Talk, Trade, Sneak","Z6 terminal (last day) to the stage wings to Zone S.",
  "Today is the last day to buy the terminal key; tomorrow the Break Room and vendors lose service. Scout the stage wings, check the pit, and pick a way past the boss or around him.",
  "Zone S service door with the terminal key (bought today) or the Mystery Key; keyless forcing otherwise.",[A("ACH-0873","Destroy a camera or drone."),A("ACH-0180","Stair Seeker.")],
  V("Today the terminal's offering one last special on the key. While supplies last, which is until tomorrow. Pay, sneak or scout the stage. The clever Crawler does all three.","Nobody knows what you're planning, which is exactly how the audience likes it. The betting has doubled.","You walked in with a plan and out with an edge. The System checked for loopholes. It found yours and gave a grudging nod."),[CAN_A139])]
d3_encs=[
 ENC("enc-d03-01","Last Call at the Break Room","z06","The Break Room (Saferoom A)",["clever","loot"],"clever","non-combat","z06",
  MM("The same carpeted saferoom, but the terminal's screen is dimmed and a hand-lettered CLOSING SOON sign has appeared on the fridge.",["Back door toward Z5 (closed).","Side passage to Z7 (closed).","Door to Z8 (closed, still passable)."],["None; honest saferoom through today.","The lights flicker as zones close."],["Couch and fridge."]),
  [],"No enemies.",
  V("LAST CALL at the Snakk-Matic. Everything must go, mostly your credits.","The terminal dims its menu one item at a time, like a bar at closing time. 'Spare keys' is the last line standing.","Receipts printed, shelves bare. Tomorrow the machine goes dark and the coffee finally wins."),
  [item("potion-of-healing","Vendor stock is shared floor-wide; price from the budget file. [CREDITS: vendor price; cite rules/70-encounter-budget-5e.json when filed]"),
   card("f01-z06-0002","Sports Drink, Blue Flavor: Welcome Box potion; the floor's vendor stock is separate."),card("f01-z06-0006","Break-Room First-Aid Kit, Lightly Bitten."),card("f01-z06-0001","Laminated Complaint Card: ask the System one yes or no question about the floor."),
   story("f01-any-0058","Candidate hook for a party that has spent the floor buying and sneaking instead of killing. Record at award; one per floor.")],
  [A("ACH-0188","Rumor Mill."),A("ACH-0899","Share Food with the Party."),A("ACH-0197","Bleed Tax.")],
  SC("The terminal offers the same stock; a short party should buy the key.","Same.","Same; prices from the budget file."),
  "If the party tries to steal from the terminal, the System's saferoom three-strikes freeze applies (canon saferoom rule); it is a cost, never a wipe. If they never buy the key and later regret it, the detour or toll waits (see the key block). If they argue prices, the System says 'no refunds' in a cheerful voice.",
  key_deadline_note="Last day to buy the terminal key; the Break Room and vendors lose service on Day 4."),
 ENC("enc-d03-02","The Collapsing Hall: Displaced Vermin","z08","Mascot Locker Room corridor (closed zone)",["dash","loot"],"dash","combat + hazard","z08",
  MM("The Locker Room corridor after closure: lockers sealed, lights stuttering, rubbery shutters coming down over side doors, a single clear path to the Green Room.",["Doorway back to the Break Room.","Doorway on to the Green Room (Z9).","Side doors sealed by shutters."],["Shutters and flickering lights; the main path is never cut.","Rats and Ceiling Ticks displaced from closed zones."],["Benches and tipped lockers (half cover)."]),
  [EN("displaced-rats","giant-rat","Giant Rat","Vent Rat (Giant Rat)","00-overview.md section 5.2 nameplate",cnt=C92),EN("displaced-ticks","stirge","Stirge","Ceiling Tick (Stirge)","00-overview.md section 5.11 nameplate",cnt=C92)],
  "House idea (inspired): creatures from closing zones crowd the route. Reuses existing identities only. Counts toward the floor's wandering cap of two if the GM uses the Ticks (00-overview.md section 5.11).",
  V("The hall is closing and so is your window. Rats and worse are leaving the zones that were turned off, and they're all headed your way.","A shutter slams down between you and the door you came through. The audience gasps, then shrugs. The other door is open.","Hall cleared, shutters stopped. The zone behind you is gone for good. Keep moving."),
  [card("f01-any-0045","Welding Goggles, Night Shift (Silver): useful in the dark hall."),card("f01-any-0015","Big Honking Flashlight: Lights-Out answer.")],
  [A("ACH-0860","Win initiative."),A("ACH-0861","Lose initiative and still win."),A("ACH-0205","Scenic Panic.")],
  SC("Fewer rats and no Ticks; the shutters do the pressure.","A small mixed group.","A full mixed group, as in 00-overview.md sections 9.2 and 9.3."),
  "If the party tries to loot the closed zone, the shutters seal over it and the System posts a 'closed' toast; the cost is a lost round and a spent short-rest slot. If they stall in the hall, the Lights-Out hour arrives and Ceiling Ticks follow. Never a wipe."),
 ENC("enc-d03-03","Stage Wings Recon","z10","Graduation Stage (wings)",["clever","dash"],"clever","non-combat scouting (optional fight)","z10",
  MM("The wings of the vast auditorium: rolled diplomas, a trophy table, camera lights in the dark, the orchestra pit at the front edge.",["Back to the Green Room (Z9).","Onto the stage (Z10).","To the service hall (Z S)."],["Camera drones watching.","The orchestra pit edge (a usable hazard).","Ushers on watch if the party is spotted."],["Trophy table and podium (half cover)."]),
  [EN("watch-ushers","skeleton","Skeleton","Usher (Skeleton)","00-overview.md section 6.4 nameplate")],
  "Ushers are on watch only if the party is spotted. Dean Thudd is on the stage, see enc-d05-03.",
  V("The wings. Where heroes wait and stagehands judge them. Take notes. The pit is right there.","A drone swings your way, its little red light blinking like a nervous bird. The audience would love for you to break it. So would the Dean.","You've seen enough. The stage is a plan, now, and not a surprise."),
  [card("f01-any-0046","Library Sneakers (Silent Edition): helpful for sneaking past the Ushers."),card("f01-any-0048","Hi-Vis Safety Vest, Reflective: a funny disguise for a staff area."),
   story("f01-any-0064","Candidate hook if a Crawler beats or drives off a named hostile using only the room (orchestra pit, trophy table), no weapon or spell of their own. One per floor; pick one deed; do not pre-promise.")],
  [A("ACH-0873","Destroy a camera or drone."),A("ACH-0173","Environmentalist (setup; pays if the pit finishes the boss).")],
  SC("A shorter scout and fewer watchers.","Same.","Full watch, as written."),
  "If someone wanders on stage too early, the Dean notices and the boss encounter starts (enc-d05-03) without the scout bonus. If someone breaks a drone loudly, the Ushers come. Never a wipe.")
]
d3_encs[1]["canon_mob_zones"]=["z02","zW"]
mkday(3,"Day {day} of {days}: Mid Zones Close, Last Call at the Break Room",
 "Floor 1 timed playthrough, Day {day} of {days}: the mid zones (Z5, Z7, Z8) close and take Bruiser's key with them; the terminal key is on its last day. Three routes, three encounters, key availability, early-descent handling, last-chance hooks and a stall fallback. CR, budget, credits and loot amounts are slots until rules/70-encounter-budget-5e.json is filed.",
 "z09","The Green Room (Saferoom B)","Default start is the Green Room. If the day rolled over elsewhere, start there.",
 "Mid zones (Z5, Z7 and Z8) close: hooks and services there vanish and Bruiser's key is lost; the route is not cut. Tagged inspired.",
 "PLACEHOLDER: FLOOR NOTICE. The middle of the building is now closed. The bait stairs, the locker room and the shooting gallery have been retired. Unclaimed items stay unclaimed. Forever.",
 "FLOOR NOTICE. Tomorrow the Break Room and every vendor in the building go dark. Buy what you need today. Buy it twice if you're nervous.",
 [REST_GR,REST_BR_OPEN,REST_FIELD],
 [{"enc_id":"enc-d02-02","note":"Zone S service door (stays until the end).","until_day":5},{"enc_id":"enc-d02-03","note":"Stairwell Threshold and early-descent choice.","until_day":5},{"enc_id":"enc-d01-04","note":"Lights-Out Ceiling Ticks (wandering; cap of two on the floor).","until_day":5}],
 srm("after the Break Room last call, if needed.","after the collapsing hall.","reserve for Lights-Out.","reserve; do not push the party to spend them."),
 {"heading":"last chance before the Break Room and vendors lose service on Day 4","note":"The terminal key and the vendor stock end after today. Bruiser's key is already gone.",
  "achievements":[A("ACH-0188","Rumor Mill."),A("ACH-0899","Share Food with the Party."),A("ACH-0197","Bleed Tax.")],
  "cards":[{"card_id":"f01-z06-0002","note":"Sports Drink, Blue Flavor."},{"card_id":"f01-z06-0006","note":"First-aid kit."}]},
 "If the party stalls, the System posts the next-collapse countdown (Break Room and vendors lose service tomorrow), the Lights-Out hour arrives, and the day rolls over at 24 in-game hours. A party that has not bought the key still has the Mystery Key (if drawn), tools, force, or the toll at the door.",
 d3_routes,d3_encs)

# =============================== DAY 4
d4_routes=[
 ROUTE("route-dash","dash","Fast, dangerous dash: the Express Lane","Z9 to Z10 stage (enc-d05-03) to Z11.","The Break Room is dark; the remaining route is Z9, the stage and the stairwell. Shortcuts are gone. Resting outside the Green Room costs.",
  "Through Z10 and Z11 or the boss-arena stairwell.",[A("ACH-0200","Speed Clear: still possible if only one Long Rest has been taken after Day 1."),A("ACH-0868","Dodge a telegraphed area attack.")],
  V("The Break Room just went dark and you're one door closer to the stage. No snacks, no vending, no excuses.","Every shortcut left is the one with teeth. The audience loves a corridor with teeth.","Stage door reached in a hurry. If the Dean sees you sweating, he'll say it's the heat. It isn't."),[CAN_M275,CAN_M277]),
 ROUTE("route-loot","loot","Slow loot-and-achievement route: What's Left","Z9, then the stage wings and Z S.","Pickings are slim. The Break Room and vendors are gone, the mid zones are gone, and the only boxes left are the ones already earned. The Green Room, the stage and the service hall are what remain.",
  "Zone S service door (Mystery Key, tools, force or the toll) then the service stairwell.",[A("ACH-0025","Saferoom Skeptic."),A("ACH-0180","Stair Seeker.")],
  V("Pickings are slim. The Break Room's closed, the vendors are dead, and the only boxes left are the ones you've already earned. Make them count.","You've got a Green Room, a stage and a service hall left to rob. It's a short list. It's a good list.","You squeezed the last drops from the building. The System is almost proud, which is as close to affection as it gets."),[CAN_A139]),
 ROUTE("route-clever","clever","Clever route: Talk, Trade, Sneak","Z9 to the stage wings to Zone S, with whatever key you still have.","The terminal key is gone. What remains is the Mystery Key (if drawn), tools, force, a toll at the door (price from the budget file) or getting past the boss by wits.",
  "Zone S service door by the remaining ways; or the stage by the cheese routes in 00-overview.md section 6.4.",[A("ACH-0189","Peaceful Path (talk the boss down)."),A("ACH-0173","Environmentalist.")],
  V("Services are down but the building still has favors to trade. Pay what you owe, steal what's left, and keep a straight face.","The cleverest thing on Day 4 is knowing what you can skip. The audience is writing it down.","You're ready for the finish without being ready for the fight. The System calls that 'ambitious'."),[CAN_A139])]
d4_encs=[
 ENC("enc-d04-01","Service Outage: The Break Room Goes Dark","z06","The Break Room (closed)",["clever","loot"],"clever","non-combat (hazard)","z06",
  MM("The Break Room with the lights half off, the terminal dark, the corkboard blank and a sign taped to the door: OUT OF ORDER, BOTH OF US.",["Door to Z8 (closed, passable).","The rest of the route runs through Z8 to Z9."],["No services: no terminal, no vendors, no corkboard. Whether it is still an honest saferoom is open: [BREAK ROOM SAFEROOM STATUS: pending Syndicate; these pages assume it is not]."],["Couch and fridge."]),
  [],"No enemies.",
  V("SERVICE OUTAGE. The terminal is dead, the vendors are dead, and the coffee has finally won. We apologize for nothing.","The fridge light clicks off. In the dark, a lone sandwich sits with a name taped to it. Nobody dares.","Last meal eaten, last crumb shared, last coin spent. Go on. The building isn't going to hold your hand."),
  [card("f01-z06-0007","Fridge sandwich: last chance to share it."),placed("Break Room services end today; no box ceremony or terminal.","00-overview.md section 5.6","Snakk-Matic terminal","[LOOT AMOUNT: n/a]")],
  [A("ACH-0899","Share Food with the Party.")],
  SC("Same dark room.","Same.","Same."),
  "If someone tries to use the dead terminal, the screen shows OUT OF ORDER and a snarky line. If they try to rest here as if it were still a saferoom, treat it as the rest-without-saferoom case: [REST-WITHOUT-SAFEROOM COST: priced in rules/70-encounter-budget-5e.json when filed]. Never a wipe."),
 ENC("enc-d04-02","Field Rest in the Dark Halls","wandering","Wandering (outside a saferoom)",["dash"],"dash","hazard + wandering combat","zW",
  MM("Wherever the party camps outside a saferoom: dark halls, red emergency light, a place with a door they can close.",["The nearest saferoom (Z9).","Whatever route they came by."],["Red dim light; Ceiling Ticks interrupt a field Long Rest per 00-overview.md section 2 rule 7."],["What the room gives."]),
  [EN("ticks","stirge","Stirge","Ceiling Tick (Stirge)","00-overview.md section 5.11 nameplate",cnt=C92)],
  "Used only if the party chooses to rest outside the Green Room. Counts toward the floor's wandering cap of two.",
  V("Resting outside the Green Room. Bold. Sleep is for people with walls.","Something small and hungry drops from the ceiling. It was waiting for you to get comfortable.","Pests cleared, rest ruined, sleep rescheduled. The System recommends the Green Room next time. Not that it cares."),
  [card("f01-any-0045","Welding Goggles, Night Shift (Silver)."),card("f01-z09-0006","Dressing-Room Candle, Scented Like a Funeral: a light source.")],
  [A("ACH-0860","Win initiative."),A("ACH-0205","Scenic Panic.")],
  SC("Fewer Ticks.","A small group.","A full group, as in 00-overview.md section 9.2."),
  "Resting outside the Green Room is allowed but costs: [REST-WITHOUT-SAFEROOM COST: priced in rules/70-encounter-budget-5e.json when filed]. If the party tries to Long Rest in the open anyway, the Ticks interrupt it. Never a wipe."),
 ENC("enc-d04-03","Ushers at the Stage Door","z10","Graduation Stage (approach)",["dash","loot"],"dash","combat","z10",
  MM("The corridor into the auditorium: STAFF ONLY doors, flashlights in the dark, rolled diplomas on a table, camera lights above.",["Back to the Green Room (Z9).","Onto the stage (Z10).","To the service hall (Z S)."],["Flashlight beams spot the party.","Camera drones watching."],["Trophy table and podium (half cover)."]),
  [EN("ushers","skeleton","Skeleton","Usher (Skeleton)","00-overview.md section 6.4 nameplate")],
  "Ushers sweep the approach with flashlights. Dean Thudd is on the stage (enc-d05-03).",
  V("The usher's flashlight finds you before you find the door. 'Please silence your screams,' says a polite voice from the dark. They don't mean the phones.","The Ushers fan out to cover both aisles. Somewhere behind them, a very large shadow adjusts a very small hat.","Ushers down, door open. The auditorium waits. So does the audience."),
  [card("f01-any-0048","Hi-Vis Safety Vest, Reflective."),card("f01-any-0050","Mop Handle of Mild Menace (Silver)."),
   story("f01-any-0065","Candidate hook if every Crawler plays a distinct part in beating the Ushers and approaching the stage as one plan. Table deed; one per floor.")],
  [A("ACH-0867","Block a hit with a shield or brace."),A("ACH-0861","Lose initiative and still win.")],
  SC("Fewer Ushers; no flanking aisle.","A small group.","Both aisles covered, as written."),
  "If the party stands in the beams and argues, the Ushers press the attack and the Dean notices. If they hide, the Ushers walk right past a quiet party. Never a wipe."),
 ENC("enc-d04-04","Green Room Night Shift","z09","The Green Room (Saferoom B)",["clever","loot","dash"],"loot","non-combat (rest)","z09",
  MM("The same backstage room, now the only honest saferoom left: a lone bulb in the mirror, the fruit plate, the photo.",["Back to the corridor to Z8.","STAFF ONLY door to Z10."],["None; honest saferoom, open to the end (inspired)."],["Chairs and the dressing table."]),
  [],"No enemies. The Long Rest closes Day 4.",
  V("SAFEROOM CERTIFIED. Still the only one. Statistically, this is where we hold our breath. Eat the fruit.","The lights dim one bulb at a time. The mirror shows your reflections a beat late. You get a long look at who you've become.","Day closed. One day left. The building is leaning toward you."),
  [card("f01-z09-0013","Green-Room Smoothie, Pre-Show Strength (Silver)."),card("f01-z09-0005","Dressing-Room Body Spray, Industrial Lilac."),card("f01-z09-0003","Dead Mirror Bulb, Briefly Alive."),
   placed("Box opening during the Long Rest: all earned boxes at once, lowest tier first.","00-overview.md section 8.2","Box openings","[LOOT AMOUNT: box pulls and credits; cite rules/70-encounter-budget-5e.json when filed]")],
  [A("ACH-0025","Saferoom Skeptic, last chance."),A("ACH-0899","Share Food with the Party.")],
  SC("Same room.","Same.","Same."),
  "If they skip the rest and push on, the day rolls over at 24 in-game hours anyway; the cost is being unrested and the rest-without-saferoom slot. If someone attacks another Crawler in the saferoom, the canon three-strikes freeze applies. Never a wipe.")
]
mkday(4,"Day {day} of {days}: The Break Room Goes Dark",
 "Floor 1 timed playthrough, Day {day} of {days}: the Break Room and every vendor lose service, the terminal key is gone, and the Green Room is the only honest saferoom. Three routes, four encounters, key availability, early-descent handling, rest options with the rest-without-saferoom slot, last-chance hooks and a stall fallback. CR, budget, credits and loot amounts are slots until rules/70-encounter-budget-5e.json is filed.",
 "z09","The Green Room (Saferoom B)","Default start is the Green Room.",
 "The Break Room (Z6) and vendors lose service: no terminal, no vendor stock, no corkboard, and the terminal key is lost. The route is not cut. Tagged inspired.",
 "PLACEHOLDER: FLOOR NOTICE. The Break Room and all vendors are closed for the season. The season is over. Thank you for shopping with the System, which is not sorry.",
 "FLOOR NOTICE. Tomorrow is the last day. Only the stage, the stairwell and the service corridor remain, plus the Green Room. After that the floor goes.",
 [REST_GR,{"option":"Break Room (Z6)","note":"Services are gone. Not an honest saferoom on these pages; see [BREAK ROOM SAFEROOM STATUS: pending Syndicate]."},REST_FIELD],
 [{"enc_id":"enc-d02-02","note":"Zone S service door.","until_day":5},{"enc_id":"enc-d02-03","note":"Stairwell Threshold and early-descent choice.","until_day":5},{"enc_id":"enc-d03-03","note":"Stage Wings Recon.","until_day":5},{"enc_id":"enc-d01-04","note":"Lights-Out Ceiling Ticks (wandering; cap of two on the floor).","until_day":5}],
 srm("after the Break Room outage, if needed.","after the Ushers.","reserve for Lights-Out.","reserve; do not push the party to spend them."),
 {"heading":"what remains before only the corridor stays on Day 5","note":"Only the Green Room, the stage wings, Z S and the stairwell still hold hooks.",
  "achievements":[A("ACH-0025","Saferoom Skeptic."),A("ACH-0189","Peaceful Path (set up).")],
  "cards":[{"card_id":"f01-z09-0013","note":"Green-Room Smoothie."}]},
 "If the party stalls, the Lights-Out hour arrives, the countdown ticks, and the System offers a Long Rest at the Green Room. A party with no key yet can still pay the toll, use tools or force the door, or take the boss route. Do not steer anyone toward early descent.",
 d4_routes,d4_encs)

# =============================== DAY 5
d5_routes=[
 ROUTE("route-dash","dash","Fast, dangerous dash: the Express Lane","Z9 to Z10 stage (Dean Thudd, enc-d05-03) to Z11 (enc-d05-04).","Last day. The boss is the whole route. In the last hours the stairs are free; earlier they mean stasis.",
  "Through Z10, then Z11 or the boss-arena stairwell.",[A("ACH-0200","Speed Clear."),A("ACH-0868","Dodge a telegraphed area attack.")],
  V("Last day. The corridor is all that's left and the Dean is standing in it. Go through him or around him. The floor falls either way.","The clock is a drumbeat now. Every step is a bet, and the audience is all in.","Through the stage and down the stairs. If it was early, you sit in stasis. If you waited, you walk. Either way, you're out."),[CAN_M275,CAN_M277,CAN_A151]),
 ROUTE("route-loot","loot","Slow loot-and-achievement route: Last Pickings","Z9, then the boss for the Silver Boss Box, then the stairs.","Whatever is left is the Green Room boxes, the Z S hall and the boss's cache. The Silver Boss Box (Z10 deck) is the floor-clear reward.",
  "Zone S service door by the remaining ways, or the boss stage.",[A("ACH-0170","Boss Claim."),A("ACH-0022","Tutorial Complete.")],
  V("Last day, last loot: whatever the stage coughs up and whatever the Dean drops. Make it good, because it's all there is.","The Silver box is on the other side of a very large man. The audience has opinions about your priorities.","Boxes earned, stage cleared, stairs taken. The System calls this 'a complete run' in a tone that is not entirely sincere."),[CAN_A139]),
 ROUTE("route-clever","clever","Clever route: Talk, Trade, Sneak","Z9 to the stage or Zone S, by wits.","The last door has a price, a key or a Dean. The toll turnstile at the Z S door (price from the budget file) is the clever way past a missing key; the boss has three cheese routes.",
  "Zone S door by key, tools, force or toll; or the stage by the cheese routes.",[A("ACH-0189","Peaceful Path."),A("ACH-0173","Environmentalist."),A("ACH-0180","Stair Seeker.")],
  V("The last door has a price, a key or a Dean. Pick the one you can afford.","No fight is the best fight, according to the people who aren't in it. The audience still wants blood, but only a little.","You solved the final exam without taking it. The System marks you 'Cheating, but efficient'."),[CAN_A139])]
d5_encs=[
 ENC("enc-d05-01","Final Morning: Only the Corridor Stays","z09","The Green Room (Saferoom B)",["clever","loot","dash"],"clever","non-combat","z09",
  MM("The Green Room at the end of the world: the mirror's last bulbs, the fruit plate, the framed photo. A countdown ticks on a wall screen.",["Back to Z8 (closed, passable).","STAFF ONLY door to the stage (Z10)."],["None; honest saferoom, open to the end (inspired)."],["Chairs and the dressing table."]),
  [],"No enemies.",
  V("GOOD MORNING, CRAWLERS. This is the last day. We've kept the lights on for you. We didn't have to.","The countdown on the wall hits a number you can't unsee. The audience goes quiet. Even the foot people.","Briefed, rested, ready. Or not. The floor falls either way."),
  [card("f01-z09-0013","Green-Room Smoothie (Silver)."),card("f01-z09-0004","Stage Whisper Cue Card (scroll)."),card("f01-z09-0014","Stage-Crew Gaffer Wristbands (Silver, hand-pick only).")],
  [A("ACH-0025","Saferoom Skeptic, last chance.")],
  SC("Same.","Same.","Same."),
  "If the party delays, the countdown reminds them and the Lights-Out hour arrives. A Long Rest here is allowed; whether it ends the day or the floor is open: [FINAL-DAY END: whether the collapse comes at 24 in-game hours of the last day or at its Long Rest; pending Syndicate]. If they miss the collapse: it is death for any Crawler not at a stairwell, on every floor, with no Reprieve (decision 026, Caleb ~10:02 PM CT; decisions/028)."),
 ENC("enc-d05-02","Zone S: The Toll Turnstile","zS","Zone S: Service Corridor",["clever","loot"],"clever","hazard (non-combat) + toll","zS",
  MM("The same utility hall, now with a System turnstile bolted across the service door and a slot that says PLEASE INSERT CREDITS.",["Back to the stage wings.","The service door and the stairs beyond."],["The door itself (key, tools, force or toll).","Force is loud: the boss and ushers follow."],["Pipe runs."]),
  [],"No enemies unless the door is forced.",
  V("A turnstile on the janitor's door. Of course there is. Insert credits, insert key, or insert yourself with some force.","The turnstile eats your payment, considers, and decides to keep the change. The audience loves a bureaucrat.","Gate open, stairs below. You paid, you picked, or you broke it. All three are valid."),
  [placed("Toll at the door: [CREDITS TOLL: amount; cite rules/70-encounter-budget-5e.json when filed]. House idea (inspired); a missed key costs, never wipes.","00-overview.md section 5.10","Opens with","[CREDITS TOLL: amount; cite rules/70-encounter-budget-5e.json when filed]"),
   item("thieves-tools","Picking the door."),card("f01-any-0014","Paint-Can Pry Bar: forcing, loudly."),card("f01-any-0044","Stuck Door Wedge (Silver): hold the gate open."),
   story("f01-any-0058","Candidate hook for a party that takes the bypass and the floor with no kills. One per floor; record at award.")],
  [A("ACH-0180","Stair Seeker."),A("ACH-0177","Hidden Cache (only if it was discovered earlier; the 3b cache is an outer-zone hook)."),A("ACH-0877","Disarm an enemy trap with junk.")],
  SC("The toll is the same; one more route through.","Same.","Same."),
  "If the party forces the turnstile, it is loud and the boss follows. If they cannot pay or open it, they can still take the boss route. The cost is time, not death. Never a wipe."),
 ENC("enc-d05-03","Graduation Stage: Dean Thudd","z10","Graduation Stage (Zone 10)",["dash","clever","loot"],"dash","boss","z10",
  MM("A vast auditorium: the stage is a podium, a stack of diplomas and a trophy table, the orchestra pit runs along the front edge, hundreds of camera lights glow in the dark, and a booth window glows BROADCAST.",["Back to the Green Room (Z9).","The wings toward the service hall (Z S).","The stairwell behind the stage (Z11)."],["The orchestra pit: shove or lure the boss in (00-overview.md section 6.4).","Group Photo: a telegraphed spotlight and countdown; step out or pay.","Camera drones overhead."],["Podium and trophy table (half cover); the Ushers hold the wings."]),
  [EN("dean","ogre","Ogre","Dean Thudd, Head of Orientation (Ogre)","00-overview.md section 6.4 nameplate",cnt="[COUNT: 1 boss; cite 00-overview.md section 9.3 until rules/70 is filed]"),
   EN("ushers","skeleton","Skeleton","Usher (Skeleton)","00-overview.md section 6.4 nameplate"),
   EN("dean-jv","bugbear-warrior","Bugbear Warrior","Dean Thudd (JV) (Bugbear Warrior)","00-overview.md section 6.6 nameplate (Variant B)",cnt="[COUNT: Variant B replaces the Dean slot; cite 00-overview.md section 6.6]")],
  "Variant B (Dean Thudd, JV) is for a party fighting at level 1 (a dash that skips the Green Room rest) or for 2 Crawlers at level 2 (00-overview.md section 6.6). The Ushers add two in Phase 2. Lore lists the Dean and the Ushers as house (inspired) mobs; the JV nameplate is overview-only.",
  V("LADIES, GENTLEMEN, AND THE PEOPLE WITH OPINIONS ABOUT YOUR FEET: it's Graduation Day. The Dean has some words. Mostly with his club.","The walk-up song slows into a sad remix and more Ushers file in from the aisles. High above, a camera drone sputters and gives you a stare. Nobody mentions it.","Class dismissed. The Dean is down, thrown out, retired or hugging someone, and the audience will take any of them.",
    "The Dean sits in the front row with the fruit plate and starts a new chapter. HR is furious. HR is also eating a grape."),
  [card("f01-z10-0001","Dean Thudd's Valedictorian Cord (Gold) (Silver Boss Box pull)."),card("f01-z10-0002","Podium Leg, Bolted Once, Now Stuck Forever."),card("f01-z10-0003","Dean's Emergency Flask."),card("f01-z10-0004","Alumni Fund Check."),
   placed("Thudd's corpse cache and the diploma stack; the Silver Boss Box for every Crawler who fought or talked him down.","00-overview.md section 6.7","corpse cache","[LOOT AMOUNT: boss cache credits and Silver Boss Box; cite rules/70-encounter-budget-5e.json when filed]"),
   story("f01-any-0059","Candidate hook if the party is the first to take down a Floor 1 boss. Check the card's trigger text and Syndicate's ruling on whether Thudd counts; one per floor; record at award; never promise."),
   story("f01-any-0065","Candidate hook if every Crawler plays a distinct part of one plan against the boss. Table deed; one per floor.")],
  [A("ACH-0170","Boss Claim: folded into the Silver Boss Box."),A("ACH-0868","Dodge a telegraphed area attack."),A("ACH-0173","Environmentalist: pit finish."),A("ACH-0189","Peaceful Path: talk him down."),A("ACH-0873","Destroy a camera or drone.")],
  SC("Use Variant B (Dean Thudd, JV) with the Ushers, and give the clever options room. Add the Assigned Companion rule if the table uses it (00-overview.md section 9.3).","Use the full Dean with fewer Ushers than the four-Crawler set; keep the pit and the diploma gambit.","Full Dean and Ushers, as written (00-overview.md section 6.4 and 9.3)."),
  "If the party dashes in at level 1 without the Green Room rest, run Variant B. If a Crawler descends early (stasis) before the fight, they are out of it; the fight runs with the rest. If someone shoves the Dean into the pit while the Ushers are still up, the Ushers pile on. Never a wipe by the clock; a death in the fight is a real death.",
  spine_plant_gm_only="[GM-ONLY] Black Box glimpse at the start of Phase 2 (00-overview.md section 6.5). A camera drone is hit, a recorder housing ejects and is snatched back by a ceiling claw. No explanation, no reward."),
 ENC("enc-d05-04","The Stairwell: The Last Six Hours","z11","The Stairwell",["dash","loot","clever"],"dash","non-combat (descent)","z11",
  MM("The plain concrete stairwell behind the stage, spiral steps down, an index card on the rail.",["Back to the stage.","Down to Floor 2.","The service stairwell joins here."],["None."],["Rail and landing."]),
  [],"No enemies. The free-descent window is the last six hours of this day.",
  V("The Stairwell. The last six hours are free. Walk down like you own it, because the floor is about to belong to nobody.","The countdown hits the last stretch. Whoever's still on the floor hears a long, low hum under the stairs.","Everyone who made it is down. The System posts the Floor Summary and a very small smile."),
  [placed("Stairwell Checkpoint, Floor Summary and descent procedure.","00-overview.md section 7.3","Stairwell Checkpoint","[LOOT AMOUNT: n/a]")],
  [A("ACH-0022","Tutorial Complete: pay once."),A("ACH-0200","Speed Clear, if the par time held."),A("ACH-0180","Stair Seeker.")],
  SC("Same.","Same.","Same."),
  "If a Crawler tries to descend earlier than the last six hours, run the early-descent block (stasis); the GM logs any override. If the party is still on the floor when the last day ends: it is death for any Crawler not at a stairwell, on every floor, with no Reprieve (decision 026, Caleb ~10:02 PM CT; decisions/028).")
]
FREE={"text":"FINAL HOURS: the floor is nearly done. From here the stairs are free. Walk down, no stasis, no waiting. The System is rooting for you. It is not, but it's trying.","tag":PF}
mkday(5,"Day {day} of {days}: Only the Corridor Stays",
 "Floor 1 timed playthrough, Day {day} of {days}: only the Stairwell corridor (Z10, Z11, Z S) remains, plus the Green Room saferoom; Dean Thudd holds the stage, the Z S door has a toll, and the last six hours make descent free. Three routes, four encounters, key availability, early-descent handling, last-chance hooks and a stall fallback. CR, budget, credits and loot amounts are slots until rules/70-encounter-budget-5e.json is filed.",
 "z09","The Green Room (Saferoom B)","Default start is the Green Room.",
 "Only the Stairwell corridor stays: Z10, Z11 and Z S, plus the Z9 saferoom. The floor collapses when the day ends (final-day timing is an open slot). Tagged inspired.",
 "PLACEHOLDER: FLOOR NOTICE. The floor is closed. Almost everything is closed. If you're not on the stairs, you're a rumor. Thank you for your time, which is up.",
 "FINAL NOTICE. The floor collapses at the end of the day. Anything not on the stairs goes with it.",
 [REST_GR,{"option":"Break Room (Z6)","note":"Closed since Day 4."},REST_FIELD],
 [{"enc_id":"enc-d02-03","note":"Stairwell Threshold (early-descent choice).","until_day":5},{"enc_id":"enc-d01-04","note":"Lights-Out Ceiling Ticks (wandering; cap of two on the floor).","until_day":5}],
 srm("after the Green Room briefing, if needed.","before the stage.","after the stage.","reserve; the clock decides."),
 {"heading":"final hooks","note":"Everything that is left is on this page.",
  "achievements":[A("ACH-0022","Tutorial Complete."),A("ACH-0170","Boss Claim."),A("ACH-0180","Stair Seeker.")],
  "cards":[{"card_id":"f01-z10-0001","note":"Dean Thudd's Valedictorian Cord (Gold)."},{"card_id":"f01-z10-0002","note":"Podium Leg."},{"card_id":"f01-z10-0003","note":"Emergency Flask."},{"card_id":"f01-z10-0004","note":"Alumni Fund Check."}]},
 "If the party stalls, the countdown ticks, the Lights-Out hour arrives, and the System posts the final notice. In the last six hours the descent is free, so a patient party simply waits at the stairwell if they are not ready to fight. If they cannot or will not fight the boss, the Z S toll door and the boss cheese routes are open.",
 d5_routes,d5_encs,early=True,freewin=FREE)
print("specs written")
