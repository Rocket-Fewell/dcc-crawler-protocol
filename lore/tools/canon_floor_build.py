#!/usr/bin/env python3
"""Builds tables/canon-floor-1.json and tables/canon-floor-1.md (Floor 1 canon source table for the Encounter Bot).
Data lives in this file; ledger ids are resolved from CANON-LEDGER.md and work/pass18-row-map.json; confidence is COPIED
from the ledger rows (weakest label wins). Run: python3 tools/canon_floor_build.py   then   python3 tools/canon_floor_check.py
Owner: DCC Lore | Written 2026-10-04 (Pass 18)."""
import json, re, os, sys, hashlib
ROOT = '/workspace/dcc-lore'
LEDGER = ROOT + '/CANON-LEDGER.md'
RM = json.load(open(ROOT + '/work/pass18-row-map.json'))
def r(*keys): return [RM[k] for k in keys]
RANK = {'UNVERIFIED': 0, 'WIKI-ONLY': 1, 'VERIFIED': 2}

def load_ledger():
    rows = {}
    for line in open(LEDGER, encoding='utf-8'):
        m = re.match(r'^\| ([A-Z]-[A-Z]?\d+) \|', line)
        if not m: continue
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip().strip('|'))]
        conf = None
        for c in cells:
            if c.startswith(('VERIFIED', 'WIKI-ONLY', 'UNVERIFIED')):
                conf = c.split(' ')[0].split(';')[0]; break
        quotes = [c[1:-1].replace('\\|', '|') for c in cells if len(c) > 2 and c.startswith('"') and c.endswith('"')]
        rows[m.group(1)] = {'conf': conf, 'quotes': quotes}
    return rows
L = load_ledger()
def conf_of(ids):
    cs = [L[i]['conf'] for i in ids if i in L and L[i]['conf']]
    if not cs: return None
    return min(cs, key=lambda c: RANK[c])
def quote_of(rid):
    q = L[rid]['quotes'][0]
    return q

# ---------------------------------------------------------------- item reskins (display names, looked up not typed)
IR = {e['srd_id']: e for e in json.load(open(ROOT + '/tables/item-reskins.json'))['entries']}
def item(srd_id, use):
    e = IR[srd_id]
    return {'srd_id': srd_id, 'srd_name': e['srd_name'], 'game_display_name': e['display_name'], 'used_for': use}

def mob(id, name, tag, rows, role, desc, analog_of=None, display=None, note=None):
    d = {'id': id, 'name': name, 'tag': tag, 'role': role, 'what': desc, 'ledger_rows': rows}
    if display: d['game_display_name'] = display
    if analog_of: d['analog_of'] = analog_of
    if note: d['note'] = note
    return d
def haz(id, name, tag, rows, desc, note=None):
    d = {'id': id, 'name': name, 'tag': tag, 'what': desc, 'ledger_rows': rows}
    if note: d['note'] = note
    return d
def feat(id, name, tag, rows, desc, note=None):
    return haz(id, name, tag, rows, desc, note)
def ann(style, quote_row=None):
    return {'style': style, 'quote': quote_of(quote_row) if quote_row else None, 'quote_row': quote_row}

C = 'canon'; I = 'inspired'; U = 'unverified'
ZONES = []
def zone(**k): ZONES.append(k)

# ================================================================= CANON (book Floor 1)
zone(id='c-floor', name='The First Floor (floor-wide rules)', kind='canon_floor_wide', tag=C,
 name_note='Canon name: The First Floor. House game wraps it as "The Orientation Pit" (see house zones).',
 ledger_rows=r('f1_layout', 'f1_mob_spawn', 'boss_no_exit', 'stair_timing', 'stair_stasis', 'saferoom_earth', 'saferoom_screens', 'cascadia_intro') + ['M-010', 'M-011', 'M-013', 'M-016', 'T-002', 'T-005'],
 staging='A giant square grid of halls split into neighborhoods; each neighborhood has one local mob type and one boss, and its mobs stop respawning when the boss dies. Stairwells only appear about a day and a half in, and saferooms look like transplanted Earth rest stops.',
 announcement=ann('Cascadia talks like a store manager opening for business; patch notes read as cheerful changelogs that scold Crawlers.', None) | {'quote': 'Hello, Crawlers!', 'quote_row': None, 'quote_source': 'W:First Floor (Introductory Announcement)'},
 mobs=[mob('mob-rat', 'Rat', C, r('rat_janitor', 'rat_bite'), 'janitor mob', 'Small, hissing, poisonous-bite rodents that infest every neighborhood and eat dead Crawlers.')],
 hazards=[haz('haz-restroom-portal', 'Hallway restroom portals', C, r('restroom_portal', 'restroom_explode', 'restroom_suction', 'restroom_patch') + ['T-005'],
              'Mismatched Earth doors that all open onto the user\'s own stall; early bugs made a second entrant explode or get sucked in until patches fixed them. Use as a one-off early-floor gag, not a standing hazard.')],
 features=[feat('feat-safe-room-rules', 'Saferoom rules', C, ['M-010', 'M-011', 'M-013', 'K-170'], 'Boxes open only inside; attackers get teleported away; three-strikes rule on violence/theft; explosives are inert.'),
           feat('feat-safe-room-look', 'Earth rest-stop saferooms', C, r('saferoom_earth', 'saferoom_screens'), 'Fast-food joints and waiting rooms from Earth, with three wall screens.'),
           feat('feat-stairwell', 'Stairwells', C, r('stair_timing', 'stair_stasis', 'boss_stairwell') + ['M-016', 'A-139'], 'Appear after the first-day cycle; Borough and City boss arenas always contain one; early descent means stasis until the floor ends.'),
           feat('feat-guild-hall', 'Tutorial Guild Hall', C, r('guildhall_tutorial') + ['A-146', 'H-003'], 'Where the HUD and menus unlock and a guide is assigned.')])

zone(id='c-hoarder', name="The Hoarder's neighborhood (Scatterer nest)", kind='canon_boss', tag=C,
 name_note='Canon boss: the Hoarder, a first Neighborhood Boss.',
 ledger_rows=['B-001', 'T-004', 'A-011', 'M-014'] + r('hoarder_spawn', 'hoarder_chamber_seal', 'hoarder_weakness'),
 staging='Once Crawlers step into the boss room the broken door re-forms and locks behind them. The boss rises out of the garbage and retches out bugs; her built-in weakness is that the flow of minions can be choked at her mouth.',
 announcement=ann('Deadpan achievement popup states plainly what the Crawler just did to the boss.', 'A-011'),
 mobs=[mob('mob-scatterer', 'Scatterer', C, r('scatterer_basic'), 'mob', 'Bread-loaf-sized cockroach swarm mob.'),
       mob('mob-scatterer-brood-guardian', 'Scatterer Brood Guardian', C, r('scatterer_guardian'), 'mob', 'Cat-sized, faster, tougher cockroach that charges.'),
       mob('boss-hoarder', 'The Hoarder', C, ['B-001'] + r('hoarder_spawn', 'hoarder_weakness'), 'boss', 'Giant garbage-troll boss who vomits Scatterers; one signature trick, one clean weakness.')],
 hazards=[haz('haz-sealed-chamber', 'Sealing boss chamber', C, r('hoarder_chamber_seal', 'boss_no_exit'), 'Door re-forms behind Crawlers and locks with glowing bars; the boss never leaves the room.')],
 features=[])

zone(id='c-goblin-quarter', name='Goblin territory (Murder Dozer, workshop and the meth war)', kind='canon_setpiece', tag=C,
 name_note='Canon: Floor 1 goblin clan area; the clan\'s boss is the Goblin War Chieftain.',
 ledger_rows=r('goblin_clan', 'goblin_clubs', 'goblin_engineer', 'murder_dozer', 'goblin_bomber', 'goblin_shamanka', 'goblin_llama_war', 'chieftain_kill', 'goblin_workshop') + ['I-013', 'I-024', 'A-009', 'A-094'],
 staging='Goblins rush in numbers and come back with the whole clan if you only kill one; the opening gag is a steam-powered Murder Dozer. The clan boss is meant to be beaten with cleverness (a cart of munitions), not toe-to-toe.',
 announcement=ann('Explosion achievements fire as gleeful popups about causing a wall-shaking boom.', 'A-009'),
 mobs=[mob('mob-goblin', 'Goblin', C, r('goblin_clan', 'goblin_clubs'), 'mob', 'Small, green, clever, loud; pineapple-topped clubs; the clan answers for a killed member.'),
       mob('mob-goblin-engineer', 'Goblin Engineer', C, r('goblin_engineer'), 'mob', 'Machine-driver in odd headgear; the first one pilots the Murder Dozer.'),
       mob('mob-goblin-bomb-bard', 'Goblin Bomb Bard', C, r('goblin_bomber'), 'mob', 'Ranged explosives specialist.'),
       mob('mob-goblin-shamanka', 'Goblin Shamanka', C, r('goblin_shamanka'), 'mob', 'Magic-using clan leader who can focus a blast.'),
       mob('mob-murder-dozer', 'Goblin Murder Dozer', C, r('murder_dozer'), 'vehicle', 'Spiked, steam-powered goblin juggernaut meant to run Crawlers down.'),
       mob('boss-goblin-war-chieftain', 'Goblin War Chieftain', C, r('chieftain_kill'), 'boss', 'Goblin clan boss; canon beat is killing it with a cart of explosives.')],
 hazards=[haz('haz-goblin-explosives', 'Goblin explosives', C, ['I-013'] + r('goblin_bomber'), 'Dynamite and sparking bombs lobbed by Bomb Bards.')],
 features=[feat('feat-goblin-workshop', 'Goblin workshop', C, r('goblin_workshop') + ['A-124'], 'A goblin base that can be looted; the canon raid ends with an infamous boss-room explosion (mature content, optional).'),
           feat('feat-meth-war', 'Goblin vs llama meth war', C, r('goblin_llama_war'), 'Background turf war between the clan and the llamas that Crawlers can inflame.')])

zone(id='c-llama', name='Bad Llama neighborhood', kind='canon_neighborhood', tag=C,
 ledger_rows=r('llama_spit', 'llama_pouch', 'goblin_llama_war'),
 staging='Horse-sized llamas lob glowing lava spit; the plan is to read the glow, then hit the throat pouch. They are the other side of the goblin turf war.',
 announcement=ann('No dedicated announcement captured; use the standard Crawler-hostile mob nameplate with a snarky one-liner.'),
 mobs=[mob('mob-bad-llama', 'Bad Llama', C, r('llama_spit', 'llama_pouch'), 'mob', 'Lava-spitting, meth-dealing llama; throat pouch is the weak point.')],
 hazards=[haz('haz-lava-spit', 'Lava spit', C, r('llama_spit', 'llama_pouch'), 'Ranged glob that scorches; the throat pouch glows before a spit and bursting it kills the llama.')],
 features=[])

zone(id='c-rot-sticker', name='Rot Sticker neighborhood', kind='canon_neighborhood', tag=C,
 ledger_rows=r('rot_sticker_bomb', 'rot_sticker_swarm'),
 staging='Wall-running suicide bombers attach, pop a few seconds later and knock the Crawler down; the rest then swarm the one on the floor.',
 announcement=ann('No dedicated announcement captured.'),
 mobs=[mob('mob-rot-sticker', 'Rot Sticker', C, r('rot_sticker_bomb', 'rot_sticker_swarm'), 'mob', 'Small, chittering ravioli-shaped kamikaze mob that runs on walls and ceilings.')],
 hazards=[haz('haz-take-down-swarm', 'Knockdown-then-swarm', C, r('rot_sticker_bomb', 'rot_sticker_swarm'), 'The self-destruct knocks the target down; swarming follows.')],
 features=[])

zone(id='c-juicer', name="The Juicer's gym (troglodyte neighborhood)", kind='canon_boss', tag=C,
 name_note='Canon boss: the Juicer, a Neighborhood Boss in the troglodyte area.',
 ledger_rows=['B-002', 'A-115'] + r('juicer_room', 'juicer_attack', 'juicer_weakness', 'juicer_stage', 'trog_poison', 'trog_virtuoso', 'trog_basher', 'trog_pygmy'),
 staging='Automatic gym doors slide shut, the lights turn red and boss music kicks in. A pack of troglodyte support mobs poison and tie up the Crawlers while the boss lobs flaming weights; the winning idea is to hit his overstrained veins.',
 announcement=ann('A clever kill gets a deadpan popup from the System (here, using one mob\'s body against another).', 'A-115'),
 mobs=[mob('mob-troglodyte-basher', 'Troglodyte Basher', C, r('trog_basher'), 'mob', 'Human-sized melee troglodyte in the Juicer\'s room.'),
       mob('mob-troglodyte-virtuoso', 'Troglodyte Virtuoso', C, r('trog_virtuoso'), 'mob', 'Small whip-tongued poisoner with long reach.'),
       mob('mob-troglodyte-pygmy', 'Troglodyte Pygmy', C, r('trog_pygmy'), 'mob', 'Tiny, fast, leaping biter.'),
       mob('boss-juicer', 'The Juicer', C, ['B-002'] + r('juicer_attack', 'juicer_weakness'), 'boss', 'Steroid-bloated lizard-man boss who throws burning free weights.')],
 hazards=[haz('haz-troglodyte-poison', 'Troglodyte poison', C, r('trog_poison', 'trog_virtuoso'), 'Bites and tongue lashes can apply the painful Poison Debuff.'),
          haz('haz-flaming-weights', 'Flaming thrown weights', C, r('juicer_attack'), 'The boss\'s one signature attack: heavy plates that ignite in flight.')],
 features=[feat('feat-boss-room-lockdown', 'Boss room lights and music', C, r('juicer_stage'), 'Doors close, red lights, boss music: the canon "fight begins" beat.')])

zone(id='c-ball-of-swine', name='Ball of Swine arena (Borough Boss)', kind='canon_boss', tag=C,
 name_note='Canon boss: the Ball of Swine, a.k.a. the Porkchop Express, a Borough Boss. Tier wording disputed once (X-009).',
 ledger_rows=['B-003', 'A-010', 'T-006', 'X-009'] + r('ball_track', 'ball_wedge', 'ball_rave', 'ball_stairwell', 'ball_pop', 'ball_courtyard', 'tuskling_knight'),
 staging='A concentric maze of tunnels with a safe courtyard at the gate. A fused sphere of aristocrats rolls on floor tracks while rising and falling walls steer it at the Crawlers, all staged as a rave. Wedge it in place, break it open, then mop up the dazed Tusklings; the stairwell is in the middle.',
 announcement=ann('A short "you have found a Borough Boss chamber" popup in the usual deadpan.', 'A-010'),
 mobs=[mob('boss-ball-of-swine', 'Ball of Swine', C, ['B-003'] + r('ball_track', 'ball_wedge'), 'boss', 'Rolling battle formation of fused Tusklings; one attack: roll over you.'),
       mob('mob-tuskling-knight', 'Tuskling Knight', C, r('tuskling_knight', 'ball_pop'), 'minion', 'Tuxedoed pig-faced aristocrat; weak and unarmed once the ball pops.'),
       mob('mob-tuskling-courtesan', 'Tuskling Courtesan', C, r('ball_pop'), 'minion', 'Gowned female Tuskling, slightly tougher than a Knight.'),
       mob('mob-tuskling-dominatrix', 'Tuskling Dominatrix', C, ['B-003'], 'minion', 'Last Tuskling standing; a leader of the formation.', note='Appears on the wiki page for the Ball; no dedicated ledger quote beyond B-003.')],
 hazards=[haz('haz-rolling-tracks', 'Rolling tracks and shifting walls', C, r('ball_track', 'ball_rave'), 'Grooves in the floor mark the sphere\'s path; walls rise and fall to redirect it; loud music hides its approach.'),
          haz('haz-ball-forcefield', 'Forcefielded stairwell', C, r('ball_stairwell'), 'The exit sits behind a red forcefield until the boss dies.')],
 features=[feat('feat-ball-courtyard', 'Staging courtyard', C, r('ball_courtyard'), 'A single gate and a courtyard the Ball will not enter; Crawlers can plan there.'),
           feat('feat-ball-wedge', 'Wedge weakness', C, r('ball_wedge'), 'The sphere fills the tunnel, so a solid angled ramp can pin it.')])

zone(id='c-floating-crystal', name='Floating-crystal neighborhood boss', kind='canon_boss', tag=C,
 ledger_rows=r('floating_crystal'),
 staging='A brittle, hovering crystal boss that a heavy hitter can shatter in a few blows. Little else is recorded.',
 announcement=ann('No announcement captured.'),
 mobs=[mob('boss-floating-crystal', 'Floating crystal', C, r('floating_crystal'), 'boss', 'Neighborhood boss that looks like a hovering crystal.')],
 hazards=[], features=[], gaps=['No ledger quote on attacks, chamber or System intro.'])

zone(id='c-street-preacher', name='Street Preacher (neighborhood boss, patched to Borough Boss)', kind='canon_boss', tag=C,
 ledger_rows=r('street_preacher'),
 staging='Only the patch-note upgrade from Neighborhood to Borough Boss is recorded; use as flavor for a promoted boss.',
 announcement=ann('Patch-note style: the System announces the promotion in a changelog bullet.'),
 mobs=[mob('boss-street-preacher', 'Street Preacher', C, r('street_preacher'), 'boss', 'Boss promoted by patch; no fight description captured.')],
 hazards=[], features=[], gaps=['No ledger quote on how it fights.'])

zone(id='c-roster', name='Other Floor 1 neighborhoods (mob roster)', kind='canon_roster', tag=C,
 ledger_rows=r('chilly_goat', 'scat_thug', 'green_slime', 'vine_creeper', 'bugaboo', 'axebeak', 'blender_fiend', 'first_ep_mobs', 'ep4_mobs', 'thorn_cadaver', 'hobgoblin_maze'),
 staging='Pick-list of other Floor 1 mobs that have no ledger-backed set-piece yet; use as local neighborhood flavor. Items marked unverified rest on a single fan-site list.',
 announcement=ann('Broadcast-recap style: new mobs are introduced on the show with a quick highlight reel.'),
 mobs=[mob('mob-chilly-goat', 'Chilly Goat', C, r('chilly_goat'), 'mob', 'White horned goat with a mouth full of fangs.'),
       mob('mob-scat-thug', 'Scat Thug', C, r('scat_thug'), 'mob', 'Raccoon-headed spear carrier about as strong as a goblin.'),
       mob('mob-green-slime', 'Green Slime', C, r('green_slime'), 'mob', 'Acidic blob that dissolves cloth and skin.'),
       mob('mob-vine-creeper', 'Vine Creeper', C, r('vine_creeper'), 'mob', 'Thorny plant that bursts from pods and swallows Crawlers.'),
       mob('mob-bugaboo', 'Bugaboo', C, r('bugaboo'), 'mob', 'Lurking, creepy ambusher.'),
       mob('mob-axebeak', 'Axebeak', C, r('axebeak'), 'mob', 'Named mob only.', note='Name only; nothing else captured.'),
       mob('mob-blender-fiend', 'Blender Fiend (patched out)', C, r('blender_fiend'), 'mob', 'Collective mob removed from Floor 1 by patch after a mass kill. Use as a rumor, not an encounter.'),
       mob('mob-spine-wolf', 'Spine-covered wolf', C, r('first_ep_mobs'), 'mob', 'Seen in the first episode; no further detail.'),
       mob('mob-fire-blob', 'Fire blob', C, r('first_ep_mobs'), 'mob', 'Shapeless flaming blob seen in the first episode.'),
       mob('mob-floating-stingray', 'Floating stingray', C, r('first_ep_mobs'), 'mob', 'Hovering ray that fires Magic Missiles from its eye stalks.'),
       mob('mob-floating-eyeball', 'Floating eyeball', C, r('first_ep_mobs'), 'mob', 'Groups of drifting eyeballs seen in the first episode.'),
       mob('mob-three-headed-baboon', 'Three-headed baboon', C, r('ep4_mobs'), 'mob', 'New mob shown in a later recap.'),
       mob('mob-toothy-eggplant', 'Eggplant with teeth', C, r('ep4_mobs'), 'mob', 'New mob shown in a later recap.'),
       mob('mob-thorn-cadaver', 'Thorn Cadaver', U, r('thorn_cadaver'), 'mob', 'Spiky undead mob; floor placement from one fan site only.', note='Mob exists (kneepads page), Floor 1 placement unconfirmed.'),
       mob('mob-hobgoblin-maze', 'Hobgoblin (maze)', U, r('hobgoblin_maze'), 'mob', 'Large goblinoid claimed for the maze areas by one fan site.')],
 hazards=[], features=[])

# ================================================================= HOUSE (The Orientation Pit)
HOUSE_NOTE = 'House zone: tag inspired. Canon rows listed are the nearest canon basis, not proof the zone itself is canon.'
S_ROWS = ['M-010', 'M-011', 'M-013', 'K-170', 'A-184']

zone(id='z00', name='Zone 0: Intake Hall', kind='house_zone', tag=I, name_note=HOUSE_NOTE,
 ledger_rows=['T-002'] + r('cascadia_intro'),
 staging='Pure intake. Crawlers step out of the booths into a long hall under a cynical welcome banner; no fight.',
 announcement=ann('Bureaucratic welcome-desk tone; a hallway screen gets one Crawler\'s name wrong.'),
 mobs=[], hazards=[], features=[])
zone(id='z01', name='Zone 1: The Atrium', kind='house_zone', tag=I, name_note=HOUSE_NOTE,
 ledger_rows=r('guildhall_tutorial') + ['H-003', 'A-145', 'A-146'],
 staging='Teaching room around a dead fountain. A rail-mounted fortune-teller automaton coaches the first skill tests against a jammed shutter and a graffitied directory.',
 announcement=ann('Faux-cheerful tutorial-guide voice that promises to teach Crawlers to live "briefly".'),
 mobs=[],
 hazards=[haz('hz-jammed-shutter', 'Jammed security shutter', I, [], 'The obstacle that teaches skill checks and helping; no combat.'),
          haz('hz-fountain-coins', 'Corroded fountain coins', I, [], 'Sharp-edged bait that nicks the greedy.')],
 features=[feat('npc-proctor-bell', 'Proctor Bell (guide automaton)', I, ['H-003'] + r('guildhall_tutorial'), 'House analog of the Tutorial Game Guide: glass booth on ceiling rails, rolls ahead of the party zone to zone.')])
zone(id='z02', name='Zone 2: Vent Row', kind='house_zone', tag=I, name_note=HOUSE_NOTE,
 ledger_rows=r('rat_janitor', 'rat_bite'),
 staging='First fight: rats burst from two banks of bent vent grates while UI brackets pop over the openings. Teaches initiative, opportunity attacks and flanking.',
 announcement=ann('Dry post-fight quip comparing the win to a menial night-shift job.'),
 mobs=[mob('hmob-vent-rat', 'Vent Rat', I, r('rat_janitor', 'rat_bite'), 'mob', 'House reskin of the canon floor rat; pack biter that likes ankles.', analog_of='mob-rat')],
 hazards=[haz('hz-vent-ambush', 'Vent ambush points', I, r('rat_janitor'), 'Bent grates are where the pack emerges from.')],
 features=[])
zone(id='z03', name='Zone 3: Vending Gore Arcade', kind='house_zone', tag=I, name_note=HOUSE_NOTE,
 ledger_rows=['A-185'] + r('rat_janitor'),
 staging='A long hall of breathing vending machines around a fallen Crawler\'s body. Teaches looting, corpse looting and the cost of reaching into a hungry machine.',
 announcement=ann('Snarky achievement popups; vending machines speak in cheerful consumer slogans.'),
 mobs=[],
 hazards=[haz('hz-hungry-vendors', 'Hungry Vendors', I, [], 'Intact machines bite and hold a reaching arm; prying them open is loud.')],
 features=[feat('npc-tanya-ruiz', 'Tanya Ruiz (fallen Crawler, lore scrap)', I, ['A-185'], 'A corpse that doubles as a loot-lesson and a hint note.')],
 table_refs=['f01-z03-vending-gore-arcade'])
zone(id='z04', name='Zone 4: Hall of Fair Warnings', kind='house_zone', tag=I, name_note=HOUSE_NOTE,
 ledger_rows=['A-040', 'A-145'] + r('rat_bite'),
 staging='A clean corridor of honest warning signs and three traps, with a rescue target hanging in a net. Teaches saves, trap spotting and disarming with junk.',
 announcement=ann('Mock-exasperated deadpan: the signs said TRAP, repeatedly, and the System notes that reading was available.'),
 mobs=[],
 hazards=[haz('hz-welcome-mat', 'T1 Welcome Mat', I, ['A-040'], 'Pressure plates swing a wet-floor sign into whoever steps on them.'),
          haz('hz-ticket-please', 'T2 Ticket, Please', I, ['A-040'] + r('rat_bite'), 'Turnstile with a hidden needle that poisons (canon uses a Poison Debuff on early mobs).'),
          haz('hz-snare-net', 'T3 Snare net', I, ['A-040'], 'Holds the rescue target; restrains anyone caught.')],
 features=[feat('npc-dale-pruitt', 'Dale Pruitt (rescue NPC)', I, [], 'Civilian ductwork enthusiast, house NPC; a permanence lesson if not protected.')],
 items=[item('net', 'Dale\'s snare net'), item('thieves-tools', 'Disarming and picking')])
zone(id='z05', name='Zone 5: Shooting Gallery', kind='house_zone', tag=I, name_note=HOUSE_NOTE,
 ledger_rows=r('boss_caricature'),
 staging='A carnival range with plywood cutouts and moving conveyors; staff mannequins fire from behind a far counter. Teaches cover and ranged combat.',
 announcement=ann('Carnival-barker patter about cover; jokes at the cutouts\' expense.'),
 mobs=[mob('hmob-mannequin-staff', 'Mannequin Staff', I, r('boss_caricature'), 'mob', 'Smiling department-store mannequins in staff polos with bows; Earth-stereotype mob in the canon tutorial spirit.', display=None)],
 hazards=[haz('hz-conveyors', 'Prize-carousel conveyors', I, [], 'Conveyor belts carry a standing Crawler along the room.')],
 features=[],
 items=[item('shortbow', 'The mannequins\' bows (closest reskin; floor doc calls them pink toy bows)')])
zone(id='z06', name='Zone 6: The Break Room (Saferoom A)', kind='house_zone', tag=I, name_note=HOUSE_NOTE + ' Saferoom rules themselves are canon.',
 ledger_rows=S_ROWS + r('saferoom_earth', 'saferoom_screens') + ['L-002'],
 staging='A break-room-themed saferoom: first box-opening ceremony, a vendor terminal and a rumor corkboard. Nothing may hurt Crawlers inside except each other.',
 announcement=ann('Saferoom certification in a warm-hug-before-a-pickpocket voice; a game-show drumroll opens the first box.'),
 mobs=[], hazards=[],
 features=[feat('feat-saferoom-a', 'Saferoom services', C, S_ROWS + ['L-002'], 'Rest, box opening, protection from mobs; explosives inert.'),
           feat('feat-breakroom-dressing', 'Break Room theming (couch, fridge, corkboard, vendor)', I, r('saferoom_earth'), 'House dressing in the canon Earth-rest-stop style.')],
 table_refs=['f01-z06-break-room'])
zone(id='z07', name='Zone 7: The Big Green EXIT', kind='house_zone', tag=I, name_note=HOUSE_NOTE,
 ledger_rows=r('stair_timing', 'boss_stairwell', 'goblin_clan', 'goblin_clubs', 'goblin_workshop') + ['A-139', 'A-040'],
 staging='Stair bait: a glowing EXIT, birdsong and fresh air lead to a landing over a trapdoor pit where goblin-style greeters wait. Walking away is the smart play; going down opens a hidden goblin workshop.',
 announcement=ann('Faux-sincere exit-sign voice; the System congratulates anyone who declines the bait.'),
 mobs=[mob('hmob-exit-greeter', 'Exit Greeter', I, r('goblin_clan', 'goblin_clubs'), 'mob', 'Clipboard-carrying goblin-style staff in EXIT-sign hats who ambush at the landing.', analog_of='mob-goblin'),
       mob('hmob-exit-greeter-trainee', 'Exit Greeter (Trainee)', I, r('goblin_clan'), 'minion', 'Junior version of the greeter.', analog_of='mob-goblin')],
 hazards=[haz('hz-trapdoor', 'T4 Trapdoor of Opportunity', I, ['A-040', 'A-139'], 'Concealed floor over a short pit with broken glass; the stairs are fake.')],
 features=[feat('feat-greeter-office', "Greeters' back office (goblin workshop)", I, r('goblin_workshop'), 'Hidden closet-workshop in the goblin-workshop tradition; optional find.')])
zone(id='z08', name='Zone 8: Mascot Locker Room', kind='house_zone', tag=I, name_note=HOUSE_NOTE,
 ledger_rows=r('boss_caricature', 'boss_one_attack'),
 staging='An empty mascot costume unhooks itself while name-badge blades take flight. The fight is built to be the first likely death-save lesson; the System switches to a dying-Crawler popup.',
 announcement=ann('Sports-broadcast mock-hype for the mascot; a stern "this lesson is about dying" aside from the guide.'),
 mobs=[mob('hmob-bruiser-mascot', 'Bruiser the Mascot (Unoccupied)', I, r('boss_caricature', 'boss_one_attack'), 'elite', 'Giant empty pit-bull mascot costume; padded foam over something heavy.'),
       mob('hmob-lanyard-blade', 'Lanyard Blade', I, [], 'minion', 'Animated ID badge on a lanyard with razor edges.')],
 hazards=[haz('hz-cracked-mirror', 'Cracked mirror wall', I, [], 'Reflection lags and teases species; atmosphere only.')],
 features=[])
zone(id='z09', name='Zone 9: The Green Room (Saferoom B)', kind='house_zone', tag=I, name_note=HOUSE_NOTE + ' Saferoom rules themselves are canon.',
 ledger_rows=S_ROWS + r('saferoom_earth', 'saferoom_screens') + ['L-002'],
 staging='Backstage saferoom before the finale: rest, box opening and a creepy framed photo of the Dean with crossed-out crawlers.',
 announcement=ann('Same saferoom certification voice as the Break Room, but with "statistically, this is where we lose people" gallows humor.'),
 mobs=[], hazards=[],
 features=[feat('feat-saferoom-b', 'Saferoom services', C, S_ROWS + ['L-002'], 'Rest, box opening, protection from mobs; explosives inert.')],
 table_refs=['f01-z09-green-room'])
zone(id='z10', name='Zone 10: Graduation Stage (Dean Thudd)', kind='house_boss', tag=I, name_note=HOUSE_NOTE,
 ledger_rows=['M-014', 'A-010'] + r('boss_no_exit', 'boss_caricature', 'boss_one_attack', 'ball_rave', 'ball_track', 'ball_wedge', 'hoarder_chamber_seal'),
 staging='A hangar-sized auditorium with an orchestra pit and hundreds of camera lights. A hulking dean in a tiny mortarboard fights with one telegraphed area attack; clever play (pit, diploma, talking him down) is rewarded.',
 announcement=ann('Full game-show host voice: a title-bout introduction, a versus card and hype for the champion, matching the canon boss-intro style.'),
 mobs=[mob('hboss-dean-thudd', 'Dean Thudd, Head of Orientation', I, r('boss_caricature', 'boss_one_attack', 'boss_no_exit'), 'boss', 'House boss: oversized dean who flunks Crawlers with a podium-and-flagpole club; one telegraphed group-photo attack.', note='Item reskin hint only: nearest reskin for the club is the greatclub.'),
       mob('hmob-usher', 'Usher', I, [], 'minion', 'Flashlight-armed theater usher; joins in the second half of the fight.')],
 hazards=[haz('hz-orchestra-pit', 'Orchestra pit', I, r('ball_wedge'), 'Front-of-stage drop that can be used against the boss.'),
          haz('hz-group-photo', 'Group Photo spotlight', I, r('boss_one_attack', 'ball_track'), 'Telegraphed floor spotlight and countdown; dodge it or pay.')],
 features=[],
 items=[item('greatclub', "Dean Thudd's club (closest reskin)")],
 table_refs=['f01-z10-graduation-stage', 'f01-any-story-boxes'])
zone(id='z11', name='Zone 11: The Stairwell', kind='house_zone', tag=I, name_note=HOUSE_NOTE,
 ledger_rows=['M-016', 'A-139', 'T-006'] + r('boss_stairwell', 'stair_timing', 'stair_stasis'),
 staging='A plain concrete stairwell behind the stage; the real exit, no bait. The System closes the floor with a summary card.',
 announcement=ann('End-of-show sign-off: the guide automaton begrudgingly says it is proud, then warns that most will die next floor.'),
 mobs=[], hazards=[],
 features=[feat('feat-real-stairwell', 'Real stairwell and floor summary', C, ['M-016', 'A-139'] + r('boss_stairwell'), 'Canon stairwell mechanic; the checkpoint and summary card are house additions.')])
zone(id='zS', name='Zone S: Service Corridor (side path)', kind='house_zone', tag=I, name_note=HOUSE_NOTE,
 ledger_rows=['A-139'] + r('boss_stairwell'),
 staging='Hidden utility hall to a service stairwell that bypasses the boss. Forcing the door is loud.',
 announcement=ann('Contemptuous raccoon-through-the-janitor-door joke for skipping the final exam.'),
 mobs=[],
 hazards=[haz('hz-service-door', 'Locked service door', I, ['A-139'], 'Opens with the right key or tools; noise draws the boss.')],
 features=[],
 items=[item('thieves-tools', 'Picking the service door')])
zone(id='zW', name='Zone W: Ceiling Ticks (wandering encounter)', kind='house_wander', tag=I, name_note=HOUSE_NOTE,
 ledger_rows=[],
 staging='Random wandering encounter used for Lights-Out cycles, interrupted field rests and noisy looting. No canon basis found.',
 announcement=ann('Needy-ex joke on the nameplate; hinting the audience groans after the wandering cap.'),
 mobs=[mob('hmob-ceiling-tick', 'Ceiling Tick', I, [], 'wanderer', 'Clingy blood-sucking ceiling parasite.')],
 hazards=[haz('hz-lights-out', 'Lights-Out cycle', I, [], 'Periodic darkness where wanderers are rolled.')],
 features=[])

# ----------------------------------------------------------------- finalize
def finalize(ZONES):
    for z in ZONES:
        z.setdefault('table_refs', []); z.setdefault('items', []); z.setdefault('gaps', [])
        z['ledger_rows'] = sorted(set(z['ledger_rows']), key=lambda x: (x[0], int(re.sub(r'\D', '', x))))
        conflicts = [x for x in z['ledger_rows'] if x.startswith('X-')]
        z['conflicts'] = conflicts
        z['ledger_rows'] = [x for x in z['ledger_rows'] if not x.startswith('X-')]
        z['confidence'] = conf_of(z['ledger_rows'])
        z['confidence_scope'] = 'weakest ledger row listed (canon basis for inspired entries)'
        for k in ('mobs', 'hazards', 'features'):
            for e in z[k]:
                e['ledger_rows'] = sorted(set(e['ledger_rows']), key=lambda x: (x[0], int(re.sub(r'\D', '', x))))
                e['confidence'] = conf_of(e['ledger_rows'])
                if e['tag'] == U and e['confidence'] != 'UNVERIFIED': raise SystemExit('unverified tag but ledger conf ' + str(e['confidence']))
                if e['tag'] == C and not e['ledger_rows']: raise SystemExit('canon entry without ledger row: ' + e['id'])
                if k != 'mobs' and e['tag'] == C and e['confidence'] is None: raise SystemExit('no conf ' + e['id'])
        if z['tag'] == C and not z['ledger_rows']: raise SystemExit('canon zone without rows ' + z['id'])

def build():
    import copy
    ZONES_ = copy.deepcopy(ZONES)
    finalize(ZONES_)
    doc = {
     'schema': 'canon-floor-1/0.1.0',
     'floor': 1,
     'floor_name_canon': 'The First Floor',
     'floor_name_house': 'The Orientation Pit',
     'owner': 'DCC Lore',
     'updated': '2026-10-04',
     'ledger_version': re.search(r'Version: ([\d.]+)', open(LEDGER).read().split('\n')[1]).group(1),
     'consumer': 'Encounter Bot (floors/f01/)',
     'players_are': 'Crawlers',
     'tag_legend': {
       'canon': 'Appears in the books per the ledger (wiki-sourced; nothing here was checked against the novels, see ledger section 0).',
       'inspired': 'House-game extension. ledger_rows then name the nearest canon basis only.',
       'unverified': 'Claimed as canon but the ledger row is UNVERIFIED (single fan-site claim) or the claim is thin.'},
     'confidence_legend': 'Copied from the ledger Confidence column (VERIFIED / WIKI-ONLY / UNVERIFIED); several rows -> weakest label. null = no ledger row (pure house content).',
     'out_of_scope': 'No CR, levels, difficulty, credits or loot amounts: Syndicate rules/10 and the loot decks own those. table_refs only point at existing deck ids. GM-only spine seeds are deliberately left out.',
     'how_to_use': 'Pick canon entries for flavor and staging; house zones list the canon basis for reskinned mobs. announcement.quote is a ledger-row quote (25 words or fewer) or null; otherwise paraphrase the style.',
     'zones': ZONES_,
    }
    return doc

def md(doc):
    out = ['# Canon Floor 1 source table (readable view)',
           'Owner: DCC Lore | Status: draft | Version: 0.1 | Updated: 2026-10-04',
           'Summary: Readable view of tables/canon-floor-1.json: Floor 1 zones, bosses and set-pieces with mobs, hazards, staging, announcement style, tag and ledger row ids. No CR, levels, credits or loot.', '',
           f"Generated by tools/canon_floor_build.py from CANON-LEDGER.md v{doc['ledger_version']}. Do not edit by hand; edit the builder and re-run. Tags: **canon** (books, per ledger), **inspired** (house extension; rows = nearest canon basis), **unverified**. Confidence is copied from the ledger.", '']
    for z in doc['zones']:
        out.append(f"## {z['id']} - {z['name']}")
        out.append(f"- Kind: {z['kind']} | Tag: **{z['tag']}** | Confidence: {(z['confidence'] + (' (of the canon basis)' if z['tag'] == 'inspired' else '')) if z['confidence'] else 'n/a (no ledger row)'}")
        if z.get('name_note'): out.append(f"- Name note: {z['name_note']}")
        out.append(f"- Ledger rows: {', '.join(z['ledger_rows']) or 'none'}" + (f" | Conflicts: {', '.join(z['conflicts'])}" if z['conflicts'] else ''))
        out.append(f"- Staging: {z['staging']}")
        a = z['announcement']
        out.append(f"- Announcement style: {a['style']}" + (f" Quote ({a.get('quote_row') or a.get('quote_source')}): \"{a['quote']}\"" if a.get('quote') else ''))
        if z['table_refs']: out.append(f"- Table refs: {', '.join(z['table_refs'])}")
        for k, label in (('mobs', 'Mobs'), ('hazards', 'Hazards'), ('features', 'Features / NPCs')):
            if z[k]:
                out.append(f"- {label}:")
                for e in z[k]:
                    extra = f" (analog of {e['analog_of']})" if e.get('analog_of') else ''
                    out.append(f"  - **{e['name']}** [{e['tag']}, {e['confidence'] or 'no ledger row'}] rows: {', '.join(e['ledger_rows']) or 'none'}{extra} - {e['what']}" + (f" _{e['note']}_" if e.get('note') else ''))
        if z['items']:
            out.append('- Item display names (item-reskins.json): ' + '; '.join(f"{i['srd_name']} = {i['game_display_name']} ({i['used_for']})" for i in z['items']))
        if z['gaps']: out.append('- Gaps: ' + ' '.join(z['gaps']))
        out.append('')
    return '\n'.join(out)

if __name__ == '__main__':
    doc = build()
    jp = ROOT + '/tables/canon-floor-1.json'
    open(jp, 'w', encoding='utf-8').write(json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    open(ROOT + '/tables/canon-floor-1.md', 'w', encoding='utf-8').write(md(doc) + '\n')
    print('sha256', hashlib.sha256(open(jp, 'rb').read()).hexdigest())
    nm = sum(len(z['mobs']) for z in ZONES); nh = sum(len(z['hazards']) for z in ZONES); nf = sum(len(z['features']) for z in ZONES)
    print('zones', len(ZONES), 'mobs', nm, 'hazards', nh, 'features', nf)
