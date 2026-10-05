#!/usr/bin/env python3
"""Pass 18 (2026-10-04): builds the Floor 1 creature/hazard/set-piece ledger rows (M-263..) from local sources and
APPENDS them to CANON-LEDGER.md below the APPEND-ONLY marker. Quotes are located programmatically (exact substrings).
Idempotent: refuses to run if the first new ID already exists. Writes work/pass18-row-map.json (key -> ledger id).
Usage: python3 work/pass18_rows.py [--dry]"""
import re, sys, json
sys.path.insert(0, '/workspace/dcc-lore/tools')
from ledger_lib import *
LEDGER = ROOT + '/CANON-LEDGER.md'
START = 263
DATE = '2026-10-04'
# key, summary (paraphrase), source tag(s), exact find-text, optional second tag (2nd family), conf override
R = [
 ('f1_layout','Floor 1 is a square grid of halls; each square holds four neighborhoods, each with its own local mob and neighborhood boss.','W:First Floor','Each square contains four neighborhoods, and each neighborhood has its own area-specific mob and neighborhood boss.'),
 ('f1_mob_spawn','Floor 1 mobs run low level, and a neighborhood stops spawning its mobs once its boss is dead.','W:First Floor','stop spawning in a neighborhood after the local boss is killed.'),
 ('rat_janitor','Rats turn up in every neighborhood and act as the floor\'s janitor mobs, eating dead crawlers.','W:First Floor','These rats also function as the floor\'s "janitor mobs," consuming the corpses of fallen crawlers.'),
 ('rat_bite','Rat bites and scratches can poison; rats burst messily when struck; they are small, hissing and numerous.','W:Rat-kin','Their bite and scratch attacks may inflict the Poison Debuff'),
 ('scatterer_basic','Basic Scatterers are bread-loaf-sized cockroach mobs that die easily; they nest in the Hoarder\'s neighborhood.','W:Scatterer','Approximately the size and shape of a loaf of bread, basic scatterers are easily killed.'),
 ('scatterer_guardian','Scatterer Brood Guardians are the tougher, cat-sized, fast-charging variant.','W:Scatterer','Brood Guardians are approximately cat-sized, and quickly charge at their targets.'),
 ('hoarder_spawn','The Hoarder fights by retching Scatterer minions out of her own mouth.','W:Hoarder','defends it by disgorging Scatterer minions from her own mouth.'),
 ('hoarder_chamber_seal','Early boss rooms seal behind the crawlers: the broken door re-forms and silver bars lock it shut one at a time.','W:Hoarder','the shattered door reforms behind the crawlers, three glowing silver bars lock it in place one by one'),
 ('hoarder_weakness','The Hoarder\'s built-in weakness: killing a minion half-emerged would have jammed her throat.','W:Hoarder','killing a minion before it had fully emerged from her mouth would have trapped the next one behind it and choked her outright'),
 ('boss_no_exit','Floor 1 bosses cannot leave their boss chambers.','W:First Floor','Bosses cannot exit Boss Chambers on this floor.'),
 ('boss_caricature','Neighborhood bosses are caricatures of an Earth or Syndicate stereotype fused with the local mob.','W:First Floor','mostly caricatures of an Earth or Syndicate stereotype mashed together with the local mob'),
 ('boss_one_attack','Floor 1 bosses generally rely on a single signature attack.','W:First Floor','Generally, each boss only has one main attack.'),
 ('boss_stairwell','Every Borough and City Boss arena on Floor 1 contains a stairwell.','W:First Floor','All Borough Bosses and City Bosses on the level have a stairwell in their arena.'),
 ('stair_timing','About 32 hours after opening, 75,000 stairwells appear across Floor 1.','W:First Floor','Roughly (32) hours after the Dungeon opens, 75,000 stairwells are'),
 ('stair_stasis','Descending with more than six hours left holds the crawler in stasis until the floor collapses.','W:First Floor','If a crawler descends the stairs with more than six hours to level collapse, they will be held in stasis until the collapse.'),
 ('restroom_portal','Hallway restroom doors are mismatched Earth doors that all open to the same personal stall.','W:First Floor','the mismatched doors are portals that always open to the same bathroom stall assigned to the crawler'),
 ('restroom_explode','Early bug: a second crawler entering an occupied restroom portal explodes.','W:First Floor','the second crawler explodes in a mess of gore'),
 ('restroom_suction','Early bug: an unexplained toilet-suction hazard for the first sixty hours.','W:First Floor','For the first sixty hours, there is an equally dangerous but unexplained'),
 ('restroom_patch','The System later announced the restroom suction and exploding bugs fixed, scolding crawlers for using hallways as bathrooms.','W:First Floor','The bathroom toilet suction issues and exploding issues have been resolved.'),
 ('saferoom_earth','Floor 1 safe rooms are fast-food joints and rest areas teleported in from Earth.','W:First Floor','these take the form of fast food restaurants and rest areas teleported from Earth\'s surface'),
 ('saferoom_screens','Every safe room carries three TV screens (timers and survivor count, recap, local info).','W:First Floor','All safe rooms have three television screens'),
 ('guildhall_tutorial','Tutorial Guild Halls unlock the full HUD and menus; the guildmaster becomes the crawler\'s Game Guide.','W:First Floor','Crawlers must complete the Tutorial to receive access to the full Heads-Up Display (HUD) and Crawler Menus'),
 ('cascadia_intro','Cascadia\'s opening announcement is delivered in the tone of a manager opening a store.','W:First Floor','Her general tone is similar to a manager opening a store for business'),
 ('goblin_clan','Killing one goblin of a group draws the rest of the clan back shortly afterward.','W:Goblins','If a crawler kills only one goblin in a group, the survivors will return shortly afterward with the rest of the clan.'),
 ('goblin_clubs','Low-level goblins carry sticks topped with pineapples that can fall off mid-fight.','W:Goblins','some wield wooden sticks with pineapples attached to the ends, which can fall off during combat'),
 ('goblin_engineer','A Goblin Engineer drives the Murder Dozer in Carl\'s first goblin encounter.','W:Goblins','The first Goblin Engineer Carl encounters drives the Goblin Murder Dozer and carries a small, curved blade.'),
 ('murder_dozer','The Murder Dozer is a goblin-built steam machine made to run crawlers down.','W:Goblin Murder Dozer','A goblin-built, steam-powered machine designed to mow down and slaughter unsuspecting dungeon crawlers.','FW2:book1-bestiary'),
 ('goblin_bomber','Goblin Bomb Bards are ranged explosive specialists.','W:Goblins','Goblin Bomb Bards are sadistic ranged attackers who specialize in explosives.'),
 ('goblin_shamanka','Goblin Shamankas can enchant objects so an explosion\'s blast is focused.','W:Goblins','Shamankas can enchant objects to direct damage or, in the event of an explosion, focus the blast.'),
 ('goblin_llama_war','Floor 1 goblins and bad llamas are locked in a territorial war over dungeon-made meth.','W:Goblins','the first-floor goblins are locked in a territorial war with bad llamas over dungeon-made meth'),
 ('chieftain_kill','Carl killed the Goblin War Chieftain with a cart of explosives rather than a head-on fight.','W:Boss','Carl bypassed traditional combat by blowing up the Goblin War Chieftain with a cart full of explosives.'),
 ('goblin_workshop','Carl and Donut loot a goblin workshop on Floor 1 in the middle of the goblin-llama meth war (the raid ends with the boss-room blast behind A-124).','W:Goblins','Carl and Donut then use the distraction to loot the goblin workshop'),
 ('llama_spit','Bad Llamas spit lava; the throat is the weak point.','FW2:book1-bestiary','Their spit is lava. Weakness: the throat','W:Bad Llama'),
 ('llama_pouch','A Bad Llama\'s throat pouch glows red before a spit; rupturing it then kills the llama.','W:Bad Llama','It glows red when they prepare to spit; if the pouch is ruptured during this stage, it will burn the llama\'s throat and kill it.'),
 ('rot_sticker_bomb','Rot Stickers latch on, then blow up three seconds later with a knock-down effect.','W:Rot Stickers','Three seconds after attaching, they explode; each blast inflicts the Take Down Effect'),
 ('rot_sticker_swarm','Once a target is knocked down, Rot Stickers swarm it.','W:Rot Stickers','Once the target is knocked down, the rot stickers swarm.'),
 ('trog_poison','Troglodyte attacks can inflict a painful Poison Debuff.','W:Troglodyte','Their attacks may inflict a devastatingly painful Poison Debuff.'),
 ('trog_virtuoso','Troglodyte Virtuosos are small whip-tongue poisoners with a long reach.','W:Troglodyte','Their thin, wet tongues can lash out up to 15ft (4.57m) and both sting like a whip and inflict the Poison Debuff.'),
 ('trog_basher','Troglodyte Bashers are human-sized melee troglodytes.','W:Troglodyte','Troglodyte Bashers are generally level 3 and almost human-sized'),
 ('trog_pygmy','Troglodyte Pygmies are small, fast leaping biters.','W:Troglodyte','They leap at their victims, hissing and bearing their fangs.'),
 ('juicer_room','The Juicer\'s room is a gym held by six Bashers and three Virtuosos.','W:Juicer','The room includes six Troglodyte Bashers and three Troglodyte Virtuosos.'),
 ('juicer_attack','The Juicer\'s main attack is throwing weights that ignite in flight.','W:Juicer','his main attack involves hurling metal weights at his target; the weights catch fire in the air.'),
 ('juicer_weakness','The Juicer\'s high-pressure veins are his weakness.','W:Juicer','His high-pressure veins are his weakness.'),
 ('juicer_stage','When the gym\'s doors shut, boss music plays and the lighting turns red.','W:Juicer','When the glass doors slide shut, boss music plays and the well-lit room turns red.'),
 ('ball_track','The Ball of Swine kills by rolling along concentric floor tracks that shifting walls steer.','W:Ball of Swine','it kills by steamrolling crawlers along concentric tracks governed by shifting dungeon walls'),
 ('ball_wedge','Because the Ball fills its tunnel, it can be wedged in place and stabbed.','W:Ball of Swine','Because the ball fills the corridor completely, it can be wedged.'),
 ('ball_rave','The Ball of Swine arena is staged as a rave: EDM, blacklight, neon and lasers on the beat.','W:Ball of Swine','The boss arena is staged as a rave, with an EDM soundtrack, blacklight, neon, and lasers timed to the beat.'),
 ('ball_stairwell','The arena\'s stairwell sits at the center behind a red forcefield.','W:Ball of Swine','A stairwell down to the Second Floor sits at the center of the arena behind a red forcefield'),
 ('ball_pop','When the sphere bursts, the fight becomes a skirmish against dazed Tusklings.','W:Ball of Swine','Once the sphere pops, the encounter drops into a standard skirmish against more than thirty dazed targets'),
 ('ball_courtyard','The arena has a single gate and a courtyard staging area the Ball will not enter.','W:Ball of Swine','The only entrance is a single vast gate opening onto a courtyard; the ball will not enter that courtyard'),
 ('floating_crystal','A Floor 1 neighborhood boss is a floating crystal that shattered under hammer blows.','W:Brandon Andrews','a floating crystal thing that shattered after a few blows from Brandon\'s hammer'),
 ('street_preacher','The Street Preacher neighborhood boss was patched up to Borough Boss status.','W:First Floor','The Street Preacher neighborhood boss has been upgraded to a Borough Boss.'),
 ('blender_fiend','A patch pulled Blender Fiends off Floor 1 after they killed 15,000 crawlers in one day.','W:First Floor','Blender Fiend mobs have been moved to a lower floor after killing 15,000 crawlers in one day.'),
 ('first_ep_mobs','The first broadcast showed new Floor 1 mobs: spine-covered wolves, fire blobs, floating stingrays and floating eyeballs.','W:First Floor','spine-covered wolves, shapeless fire blobs, floating stingrays that shoot Magic Missiles from their eye stalks, and groups of floating eyeballs'),
 ('ep4_mobs','A later broadcast showed more Floor 1 mobs, including a three-headed baboon and a toothy eggplant.','W:First Floor','New first floor mobs, including a three-headed baboon and an eggplant with teeth.'),
 ('chilly_goat','Chilly Goats are white, fanged goats.','W:Chilly Goat','They are white, horned goats with mouths full of fangs.'),
 ('scat_thug','Scat Thugs are small raccoon-headed spear carriers about as strong as goblins.','W:Scat Thug','They are bipedal racoon-headed monsters that stand approximately 2 ft tall, are roughly as strong as Goblins, and are armed with spears.'),
 ('green_slime','Green Slimes are acidic blobs that dissolve cloth and skin on contact.','W:Slime','Their flesh is acidic and burns on contact.'),
 ('vine_creeper','Vine Creepers are thorny plants that burst from pods and swallow crawlers.','W:Vine Creepers','They are thorny, creeping plants that emerge from giant pods and consume crawlers whole.'),
 ('bugaboo','Bugaboos are lurking, creepy ambushers found on Floors 1-3.','W:Bugaboo','Bugaboos are a type of mob found on the First, Second, and Third Floors.'),
 ('axebeak','An Axebeak is the example mob named on a Borough Field Guide tooltip (name only; no description captured).','W:Borough Field Guide','Mobs Level 2-5. Axebeak.'),
 ('tuskling_knight','Tuskling Knights freshly out of a burst Ball are disoriented, in tuxedos, holding intact wine glasses.','W:Tuskling','Having just emerged from a Ball of Swine, the First Floor Tuskling Knights are disoriented. They wear tuxedos and carry somehow-intact wine glasses.'),
 ('thorn_cadaver','Thorn Cadavers are listed as a Floor 1 spiky undead mob by one fan site only; the kneepads page confirms the mob exists but not its floor.','FW2:book1-bestiary','Spiky undead mob; drops crafting materials including spikes used in Donut\'s kneepads.','UNVERIFIED'),
 ('hobgoblin_maze','Hobgoblins are listed as Floor 1 maze mobs by one fan site only.','FW2:book1-bestiary','Larger goblin variant found in the maze and maze boss areas.','UNVERIFIED'),
]

OVERRIDE = {'juicer_room':'VERIFIED (page cite B1 ch24; same fight, next paragraphs of the page)','rot_sticker_bomb':'VERIFIED (page cite B1 ch19; cite sits on the next paragraph of the page)'}
def stripped(tag): return norm_ws(strip_cites(src_text(tag)))
def find_snip(tag, find):
    cands = [find, find.replace("'", "\u2019"), find.replace('"', '\u201c')]
    raw = src_text(tag)
    for f in cands:
        words = norm_ws(f).split(' ')
        pat = r'(?:\s|\[\d+\|[^\]]+\])+'.join(re.escape(w) for w in words)
        m = re.search(pat, raw)
        if m:
            return f, raw, m
    return None, raw, None
def cites_after(raw, m):
    tail = raw[m.end():]
    s = re.match(r'([^.!?\[]*[.!?"\u201d]*)((?:\[\d+\|[^\]]+\])+)', tail)
    if s: return cites_in(s.group(2)), 'sentence'
    # page cite: first cite group later in the same paragraph, else last group earlier in it
    para_after = tail.split('\n\n')[0]
    g = re.search(r'((?:\[\d+\|[^\]]+\])+)', para_after)
    if g: return cites_in(g.group(1)), 'page'
    head = raw[:m.start()]
    para_before = head.split('\n\n')[-1]
    gs = re.findall(r'((?:\[\d+\|[^\]]+\])+)', para_before)
    if gs: return cites_in(gs[-1]), 'page'
    return [], 'none'
def fmt(cs):
    by = {}
    for c in cs:
        b, ch = c.split(':', 1)
        by.setdefault(b, [])
        if ch not in by[b]: by[b].append(ch)
    out = []
    for b, chs in by.items():
        out.append(f'{b} ch' + ','.join(chs) if all(x.isdigit() for x in chs) else f'{b} ' + ','.join(chs))
    return '; '.join(out)

def main():
    dry = '--dry' in sys.argv
    led = open(LEDGER).read()
    if f'| M-{START} |' in led:
        print('already appended'); return 1
    rows = []; idmap = {}
    for i, r in enumerate(R):
        key, summ, tag, find = r[:4]
        extra = r[4] if len(r) > 4 else None
        rid = f'M-{START+i}'
        f, raw, m = find_snip(tag, find)
        if not m: print('NOT FOUND', key, find); sys.exit(2)
        core = norm_ws(f)
        if len(core.split()) > 25: print('TOO LONG', key); sys.exit(2)
        cs, kind = cites_after(raw, m)
        tags = tag; second = None
        conf = None
        if extra == 'UNVERIFIED': conf = 'UNVERIFIED (single fan-site claim; floor placement not confirmed by a second source)'
        elif extra:
            tags = f'{tag}; {extra}'
        if key in OVERRIDE: conf = OVERRIDE[key]
        if conf is None:
            if kind == 'sentence': conf = f'VERIFIED (cite {fmt(cs)})'
            elif kind == 'page': conf = f'VERIFIED (page cite {fmt(cs)})'
            else: conf = 'WIKI-ONLY'
            if extra and (extra.startswith('FW2') or tag.startswith('FW2')):
                conf = (conf + '; 2 families') if conf.startswith('VERIFIED') else 'VERIFIED (2 sources)'
        # exact-substring quote of the (cite-stripped, whitespace-normalised) text; keep wiki wording
        quote = core
        # ledger quotes must not contain a bare pipe
        quote = quote.replace('|', '\\|')
        rows.append(f'| {rid} | {summ} | "{quote}" | {tags} | {conf} | {DATE} |')
        idmap[key] = rid
    block = ['', '### 9.1 Floor 1 creatures, hazards and set-pieces (Pass 18, 2026-10-04; prefix M- continues mechanics rulings; feeds tables/canon-floor-1.json)',
             'Source: local Fandom mirror pages (and one FW2 bestiary). Same caveat as section 0: nothing here was read against the novels. Quotes are wiki wording, not novel text. "page cite" = a chapter cite sits elsewhere in the same paragraph of the wiki page. Two rows (Thorn Cadaver, Hobgoblin maze) rest on one fan site and stay UNVERIFIED.',
             '', '| ID | Ruling (paraphrase) | Source quote (<=25 words) | Source | Confidence | Date |', '|---|---|---|---|---|---|'] + rows + ['']
    marker = '<!-- APPEND-ONLY BELOW THIS LINE.'
    idx = led.index(marker); eol = led.index('\n', idx) + 1
    new = led[:eol] + '\n'.join(block) + led[eol:]
    json.dump(idmap, open(ROOT + '/work/pass18-row-map.json', 'w'), indent=1)
    if dry:
        print('\n'.join(block)); return 0
    open(LEDGER, 'w').write(new)
    print('appended', len(rows), 'rows M-%d..M-%d' % (START, START + len(rows) - 1))
    return 0
sys.exit(main())
