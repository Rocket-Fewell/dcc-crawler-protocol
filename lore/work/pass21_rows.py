#!/usr/bin/env python3
import os as _os
_LORE = _os.environ.get('DCC_LORE_ROOT') or _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
"""Pass 21 (2026-10-05): Floor 3 (The Over City) rules, setting and creatures (M-651.. and X-076..). APPENDS section 9.4 to
CANON-LEDGER.md just before '### Pass log'. Quotes located programmatically (exact substrings). Idempotent: refuses if M-651 exists.
Writes work/pass21-row-map.json. Usage: python3 work/pass21_rows.py [--dry]"""
import re, sys, json
sys.path.insert(0, _os.path.join(_LORE, 'tools'))
from ledger_lib import *
LEDGER = ROOT + '/CANON-LEDGER.md'
START = 651
XSTART = 76
DATE = '2026-10-05'
TF='W:Third Floor'; VG='W:Village Guard Swordsman'; EL='W:Elite'; GP='W:Gate Pass'; SU='W:Street Urchin'; YT2='YT:sS36rv-jPLg'
R = [
 ('f3_name','Floor 3 is The Over City, the first floor of the "Volcano" storyline.',TF,'The Over City is the Dungeon\'s Third Floor and the first floor of the "Volcano" storyline'),
 ('f3_volcano','It is the first of six urban Volcano floors (3, 6, 9, 12, 15, 18 per the page\'s speculation section), layers of one giant crater.',TF,'The Over City is the first of six special urban "Volcano" storyline floors'),
 ('f3_size','Size: about the state of Arizona, roughly 300,000 square km.',TF,'The Over City is approximately the size of the state of Arizona, covering roughly 300,000 km²'),
 ('f3_smaller','It is much smaller than Floors 1 and 2.',TF,'the floor is significantly smaller than the first and second floors'),
 ('f3_sky','The open sky is fake: an illusory ceiling with nebulae and a red sun, still underground.',TF,'an artificial sky shows a dark expanse, colorful nebulae, and a blazing red sun, but it is actually an illusory ceiling'),
 ('f3_planks','Ground is wooden planks; hundreds of small villages sit inside wide stretches of abandoned city.',TF,'The floor itself is made of wooden planks, and there are hundreds of small, scattered villages surrounded by wide swaths of abandoned city.'),
 ('f3_entry_random','Arrival point is random: where you left Floor 2 does not matter.',TF,'Where a crawler exited the Second Floor has no bearing on where they enter this floor; entry is completely random'),
 ('f3_cataclysm','Backstory: after the Cataclysm (Scolopendra\'s poison gas), survivors\' descendants live in protected villages and the monsters roam the ruins.',TF,'The descendants of the survivors live in the scattered, protected villages, while the resulting monsters roam the moss-covered, crumbling brick ruins'),
 ('f3_timer_trad','Timer: Floor 3 traditionally runs 20 days; this season the AI cut it to 8 days. (Matches the house 20-day clock, decision 026.)',TF,'the Third Floor is traditionally allowed to run for 20 days, but the system AI forced the timer down to just 8 days'),
 ('f3_restrooms','Opening announcement: bathroom penalties are gone, but restrooms still exist (pubs, some shops, and in the ruins).',TF,'While the bathroom penalties have been removed, we want to remind the crawlers that restrooms still populate this floor.'),
 ('f3_sponsor_early','Sponsors may place early bids on Floor 3.',TF,'potential sponsors now have the ability to put in early bids'),
 ('f3_sponsor_f4','The sponsorship program officially starts on Floor 4.',TF,'the program doesn\'t officially get underway until the fourth floor'),
 ('f3_npc_legal','Killing non-combatant NPCs is technically not against the rules, only discouraged.',TF,'While this practice is technically not against the rules'),
 ('f3_npc_xp','Citizens are worth zero XP on Floor 3.',TF,'we have adjusted the experience counter for citizens down to zero'),
 ('f3_guard_buff','City guards got a slight stat boost at the same time.',TF,'In addition, city guards have been given a slight boost in stats.'),
 ('f3_npc_xp_yt','The Book 2 recap agrees: non-combat NPC XP zeroed and guards buffed.',YT2,'experience from killing non-combat NPCs has been zeroed out and city guards buffed'),
 ('f3_villages','Villages are sanctuaries guarded by high-level guards.',TF,'They act as sanctuaries and are fiercely protected by high-level guards'),
 ('f3_execute','Guards execute Crawlers for stealing, attacking NPCs, or even passing out drunk.',TF,'who will execute crawlers for crimes like stealing, attacking NPCs, or even passing out drunk'),
 ('f3_nojail','There is no jail on Floor 3, only the death penalty (Mordecai).',VG,'There is no jail here. Only the death penalty.'),
 ('f3_run','Escape rule: guards are slow but many; run into the ruins and they will not follow.',VG,'Run from them and into the ruins. They won\'t follow you there.'),
 ('f3_banned','Cost of escaping: you can never return to that village.',VG,'You will never be able to return to that particular village.'),
 ('f3_dayduty','Village guards are only on duty while the sun is up.',VG,'They are only on duty when the sun is up'),
 ('f3_troublemaker','Punching a guard got Carl branded a troublemaker: every guard attacks him on sight.',YT2,'becoming branded as a troublemaker so now all guards will attack him on site'),
 ('f3_gatepass','A Gate Pass from a magistrate keeps guards off you, as long as you are not too obvious about the crime.',GP,'This letter gets the city guard off your back as long you\'re not being too overt with your current criminal enterprise.'),
 ('f3_gatepass_local','A Gate Pass only works in the township that issued it.',GP,'Pass only works within the township in which it was issued.'),
 ('f3_ruins','The ruins outside the village gates are fog-covered and full of deadly mobs.',TF,'The ruins are the abandoned, fog-covered expanses of the city outside the village gates, filled with deadly mobs.'),
 ('f3_inns','Village inns are safe rooms and show on the minimap.',TF,'Inns in various Over City villages are listed as safe rooms on crawler minimaps.'),
 ('f3_safe_ruins','Safe rooms also appear every few miles in the ruins.',TF,'Safe rooms are also scattered every few miles in the ruins'),
 ('f3_barebones','Bare-bones safe rooms still exist alongside the full-service ones.',TF,'but "bare-bones versions" still appear as well'),
 ('f3_manager_tp','A manager (Mordecai, via Former Child Actor) teleports to any safe room his Crawler enters, for the rest of the crawl.',TF,'he will instantly teleport to any safe room they enter'),
 ('f3_stairs_cond','From Floor 3 on, some stairwells only appear once a condition is met (a quest, a boss kill).',TF,'some stairwells will only be revealed when certain conditions are met, like completing a quest or defeating a boss'),
 ('f3_stairs_nolimit','Events list: no time limit on entering Floor 3 stairwells (see X-077).',TF,'Stairwells: No limitations on time to enter Stairwells.'),
 ('f3_earlybird','Early Bird Gets to Squirm: going down more than 6 hours before collapse; no reward.',TF,'Went down Stairwells more than 6 hours before level collapse'),
 ('f3_npc_engineered','Over City NPCs are bio-engineered beings owned by Borant.',TF,'Non-player characters (NPCs) in the Over City are biologically engineered entities, created and owned by the Borant Corporation.'),
 ('f3_npc_memory','NPC memories are rewritten every season; they do not know they are artificial.',TF,'their memories are routinely altered for each new season of the game'),
 ('f3_guildhalls','Villages range tiny to extra-large and hold class and race guildhalls; some races have no guild.',TF,'contain class- and race-specific guildhalls, though some races may not have a guild'),
 ('f3_stores','Random stores start appearing on the map from Floor 3.',TF,'Random stores also begin populating the map on this floor'),
 ('f3_daynight','Day-night cycle: mobs roam at all hours but night is much more dangerous.',TF,'Mobs roam the ruins at all times but are significantly more dangerous at night'),
 ('f3_daynight_yt','The recap agrees that night is much more dangerous than day.',YT2,'The floor has a day-night cycle with nighttime being significantly more dangerous than daytime.'),
 ('f3_urchin_job','Street Urchins (night janitor mobs) clear corpses and trash.',SU,'to remove dead bodies and any other refuse left behind by inconsiderate crawlers'),
 ('f3_urchin_peace','Urchins ignore you unless you bother them or block their work.',SU,'They won\'t bother you if you don\'t bother them. But you best not get in their way.'),
 ('f3_shadowleaks','Shadow Leaks: smoke-like ghost mobs with a stinging cold attack, at night in the Skyfowl settlement.','W:Shadow Leaks','smoke-like ghost mobs that utilize a stinging cold attack'),
 ('f3_stealth','Some mobs have stealth: hidden from the minimap but visible to the eye; spotting one adds the dot.',TF,'cloaks them from crawler minimaps but offers no invisibility'),
 ('f3_corrupt','Any location labelled "corrupt" can hold mobs, even a temple.',TF,'any location labeled "corrupt" can have mobs inside, even if it was not supposed to'),
 ('f3_fear','Circus mobs are immune to Fear ("scary-ass mobs").',TF,'scary-ass mobs are immune to Fear effects'),
 ('f3_nbmap','A neighborhood boss kill still gives a map upgrade on Floor 3.',TF,'Defeating a neighborhood boss yields a map upgrade.'),
 ('f3_cityboss','When Carl found Grimaldi, nobody that season had fought a city boss and lived.',TF,'no one has taken on a city boss and survived'),
 ('f3_elites','Floor 3 introduces Elites: powerful non-boss NPCs with heavy plot armor running scripted soap-opera stories.',TF,'This floor introduces "Elites," highly powerful, non-boss entities with heavy plot armor.'),
 ('f3_elite_floors','Thousands of Elites spread across Floors 3, 6 and 9 and move freely between them.',EL,'thousands of Elites are spread across the third, sixth, and ninth floors, traveling freely between them'),
 ('f3_elite_patch','Writers hot-patch an Elite\'s instructions if the story goes off course.',EL,'hot patch new instructions right into the elite\'s mind'),
 ('f3_elite_fair','The dungeon\'s fairness rules are applied loosely when an Elite is involved.',EL,'the rules meant to keep the dungeon "fair" for crawlers are applied loosely whenever an Elite is involved'),
 ('f3_elite_redshirt','In an Elite\'s story the Crawler is the expendable extra (Mordecai).',EL,'Most of these elites have very thick plot armor, and in those stories, you\'re the extra.'),
 ('f3_elite_run','Elite storylines run whether or not Crawlers get involved (recap).',YT2,'these story lines run whether or not crawlers get involved'),
 ('f3_elite_map','After Meet an Elite, every Elite shows on the minimap as a black cross.',EL,'every Elite is marked on the minimap with a black cross'),
 ('f3_clubs','Urban floors open access to intergalactic nightclubs (Desperado Club).',TF,'The urban levels introduce access to intergalactic nightclubs.'),
 ('f3_vanquisher','Club Vanquisher: exclusive country-club style, for clerics and the elite.',TF,'Club Vanquisher is an exclusive, country-club-style establishment for clerics and the elite'),
]
OVERRIDE = {
 'f3_timer_trad': 'VERIFIED (cite B2 ch2; the line sits in the page\'s Speculation section, so only the 20-to-8 cut is fact, the Primal Degeneration reading is speculation)',
 'f3_npc_xp_yt': 'VERIFIED (2 sources: recap transcript + W:Third Floor announcement)',
 'f3_daynight_yt': 'VERIFIED (2 sources: recap transcript + wiki cite B2 ch12)',
 'f3_elite_run': 'VERIFIED (2 sources: recap transcript + W:Elite cite B2 ch7)',
 'f3_troublemaker': 'WIKI-ONLY (recap transcript, auto-captions; "on site" is the caption\'s spelling)',
 'f3_stairs_nolimit': 'WIKI-ONLY (Events list, no cite; conflicts with M-277, see X-077)',
 'f3_earlybird': 'WIKI-ONLY (achievement table row, no cite)',
}
X = [
  ('x_f3timer','Floor 3 timer: canon 8 days vs traditional 20 vs house 20',
   (TF,'the Third Floor is traditionally allowed to run for 20 days, but the system AI forced the timer down to just 8 days'),
   ('note','Floor 3 = 20 days on the house clock (Floor 1 = 5, Floor 2 = 10)','Syndicate decision 026 (Caleb, 2026-10-04)'),
   'RESOLVED. The house 20 days is the canon traditional length; the 8 days is this season\'s AI cut (same pattern as Floor 2: traditional 10 cut to the legal minimum 6, X-062). PREFERRED: keep 20. The infobox and the Dungeon table say 8 (M-629).'),
  ('x_f3early','Early descent on Floor 3: stasis rule vs "no limitations"',
   ('W:Dungeon','the crawler will be placed in stasis until the countdown begins on the next floor'),
   (TF,'Stairwells: No limitations on time to enter Stairwells.'),
   'OPEN. The Floor 3 Events list is uncited; the Early Bird Gets to Squirm row shows early descent happened (no reward) but not whether stasis applied. PREFERRED: keep the general stasis rule (M-277) unless a cite turns up.'),
  ('x_f3shape','Over City setting: "above-ground" vs underground with illusory sky',
   ('FW2:book2-overview','a vast above-ground urban environment with towers, sky bridges, and vertical architecture'),
   (TF,'it is actually an illusory ceiling'),
   'RESOLVED. PREFERRED: Fandom (cites B2 ch1-4): underground, fake sky, ceiling just above four-story buildings, wooden-plank streets. The fan-overview wording is wrong.'),
  ('x_f3guards','Guard justice: death vs escape',
   (TF,'Infractions result in death, as there are no jails or leniency.'),
   (VG,'Run from them and into the ruins. They won\'t follow you there.'),
   'RESOLVED (both hold). PREFERRED: caught means death; running to the ruins works, but you are barred from that village for good, and guards only work daytime. Hitting a guard brands you a troublemaker (recap, M-673).'),
]
def stripped(tag): return norm_ws(strip_cites(src_text(tag)))
def find_snip(tag, find):
    cands = [find, find.replace("'", "\u2019"), find.replace('"', '\u201c')]
    raw = src_text(tag)
    for f in cands:
        words = norm_ws(f).split(' ')
        pat = r'(?:\s|\[\d+\|[^\]]+\])+'.join(re.escape(w) for w in words)
        m = re.search(pat, raw)
        if m: return f, raw, m
    return None, raw, None
def cites_after(raw, m):
    tail = raw[m.end():]
    s = re.match(r'([^.!?\[]*[.!?"\u201d]*)((?:\[\d+\|[^\]]+\])+)', tail)
    if s: return cites_in(s.group(2)), 'sentence'
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
        if not m: print('NOT FOUND', key, '|', tag, '|', find); continue
        core = norm_ws(f)
        if len(core.split()) > 25: print('TOO LONG', key, len(core.split())); continue
        cs, kind = cites_after(raw, m)
        tags = tag
        if kind == 'sentence': conf = f'VERIFIED (cite {fmt(cs)})'
        elif kind == 'page': conf = f'VERIFIED (page cite {fmt(cs)})'
        else: conf = 'WIKI-ONLY'
        if tag.startswith('YT:') or tag.startswith('FW2:'):
            conf = 'UNVERIFIED (single transcript or fan-overview claim; not read against the novel)' if tag.startswith('FW2:') else 'WIKI-ONLY (recap transcript, auto-captions)'
        if key in OVERRIDE: conf = OVERRIDE[key]
        quote = core.replace('|', '\\|')
        rows.append(f'| {rid} | {summ} | "{quote}" | {tags} | {conf} | {DATE} |')
        idmap[key] = rid
    if len(rows) != len(R): print('ABORT: some rows failed'); sys.exit(2)
    n = START + len(R)
    last_m = n - 1
    xrows = []
    for j, (key, topic, A, B, status) in enumerate(X):
        xid = f'X-{XSTART+j:03d}'
        def cell(src):
            if src[0] == 'note': return f'{src[1]}', src[2]
            tag, find = src
            f, raw, m = find_snip(tag, find)
            if not m: print('X NOT FOUND', key, tag, find); sys.exit(2)
            c = norm_ws(f)
            if len(c.split()) > 25: print('X TOO LONG', key); sys.exit(2)
            return '"' + c.replace('|', '\\|') + '"', tag
        ta, sa = cell(A); tb, sb = cell(B)
        xrows.append(f'| {xid} | {topic} | {ta} | {sa} | {tb} | {sb} | {status} | {DATE} |')
        idmap[key] = xid
    block = ['', '### 9.4 Floor 3 (The Over City): setting, laws, timer, safe rooms, stairwells, night mobs and Elites (Pass 21, 2026-10-05; prefix M- continues mechanics rulings)',
             'Source: local Fandom mirror pages (Third Floor, Village Guard Swordsman, Gate Pass, Street Urchin, Shadow Leaks, Elite), the Book 2 recap transcript (YT:sS36rv-jPLg) and one fan overview (FW2). Same caveat as section 0: nothing here was read against the novels. Quotes are wiki or caption wording, not novel text. "page cite" = a chapter cite sits elsewhere in the same paragraph. Race/class selection on Floor 3 is already in sections 11-12; Floor 3 achievements are in section 1. Levels, credits and loot amounts are deliberately not captured. Existing anchors: M-277, M-629, R-042, R-043, X-031, X-062, L-009.',
             '', '| ID | Ruling (paraphrase) | Source quote (<=25 words) | Source | Confidence | Date |', '|---|---|---|---|---|---|'] + rows + ['',
             f'#### 9.4c Floor 3 conflicts (X-{XSTART:03d}..X-{XSTART+len(X)-1:03d})', '',
             '| ID | Topic | Reading A (quote or note) | Source A | Reading B (quote or note) | Source B | Status | Date |', '|---|---|---|---|---|---|---|---|'] + xrows + ['']
    marker = '### Pass log'
    idx = led.index(marker)
    new = led[:idx] + '\n'.join(block).lstrip('\n') + '\n' + led[idx:]
    json.dump(idmap, open(ROOT + '/work/pass21-row-map.json', 'w'), indent=1)
    print('rows', len(rows), f'M-{START}..M-{last_m}', 'X', len(xrows), f'X-{XSTART}..X-{XSTART+len(X)-1}')
    if dry:
        print('\n'.join(block)[:2500]); return 0
    open(LEDGER, 'w').write(new)
    print('appended')
    return 0
sys.exit(main())
