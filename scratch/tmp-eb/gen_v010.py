#!/usr/bin/env python3
"""Generator for rules/70-encounter-budget-5e.json (scratch; not filed). All numbers computed here so md and json agree."""
import json, glob, hashlib, math, os, random, statistics, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("DCC_CAMPAIGN_ROOT") or os.environ.get("DCC_CAMPAIGN_DIR") or os.path.abspath(os.path.join(_HERE, "..", ".."))
OUT = ROOT + "/rules/70-encounter-budget-5e.json"

# ---------- SRD 5.2.1 tables ----------
XPB = {1:(50,75,100),2:(100,150,200),3:(150,225,400),4:(250,375,500),5:(500,750,1100),6:(600,1000,1400),
 7:(750,1300,1700),8:(1000,1700,2100),9:(1300,2000,2600),10:(1600,2300,3100),11:(1900,2900,4100),
 12:(2200,3700,4700),13:(2600,4200,5400),14:(2900,4900,6200),15:(3300,5400,7800),16:(3800,6100,9800),
 17:(4500,7200,11700),18:(5000,8700,14200),19:(5500,10700,17200),20:(6400,13200,22000)}
CR_ORDER = ["0","1/8","1/4","1/2"]+[str(i) for i in range(1,28)]
CR_XP = {"0":0,"1/8":25,"1/4":50,"1/2":100,"1":200,"2":450,"3":700,"4":1100,"5":1800,"6":2300,"7":2900,"8":3900,
 "9":5000,"10":5900,"11":7200,"12":8400,"13":10000,"14":11500,"15":13000,"16":15000,"17":18000,"18":20000,
 "19":22000,"20":25000,"21":33000,"22":41000,"23":50000,"24":62000,"25":75000,"26":90000,"27":105000}
def cr_num(c):
    return {"0":0,"1/8":0.125,"1/4":0.25,"1/2":0.5}.get(c) if c in ("0","1/8","1/4","1/2") else float(c)
def fit_cr(xp):
    best="0"
    for c in CR_ORDER:
        if CR_XP[c] <= xp: best=c
    return best
def min_cr(a,b): return a if cr_num(a)<=cr_num(b) else b
# core 10 sec 8.3 (party of 4): mobs lo/hi, elites lo/hi, boss lo/hi
CORE_CR = {1:("0","1/4","1/2","1","2","2"),2:("1/8","1/2","1","2","3","4"),3:("1/4","1","2","3","4","5"),
 4:("1/2","1","2","3","5","6"),5:("1","2","3","4","7","8"),6:("1","2","4","6","8","9"),7:("2","3","5","6","9","10"),
 8:("2","3","6","7","10","11"),9:("3","4","7","8","11","12"),10:("3","5","8","9","12","13"),11:("4","5","9","10","13","14"),
 12:("4","6","10","11","14","16"),13:("5","6","11","12","15","16"),14:("5","7","12","13","16","17"),
 15:("6","8","13","14","17","19"),16:("6","8","14","15","18","20"),17:("7","9","15","16","19","21"),18:("8","10","16","18","21","24")}
CORE_BOX = {  # core 4.5 pacing ranges per crawler per floor
 "1-2":{"Bronze":"2-4","Silver":"0-1"},"3-5":{"Bronze":"2-3","Silver":"1-2","Gold":"0-1"},
 "6-9":{"Bronze":"1-2","Silver":"1-2","Gold":"1","Platinum":"0-1 (F9)"}}
MULT = {f:(1 if f<=4 else 5 if f<=9 else 20 if f<=14 else 50) for f in range(1,19)}
PARTY = [2,3,4]
LEAD_SHARE = {"trivial":1.0,"standard":1.0,"hard":1.0,"boss":0.9}
def rnd(x): return int(x+0.5)

# ---------- tier -> 2024 band maps (per floor) ----------
BAND_F1 = {"trivial":"half of Low","standard":"Low","hard":"Moderate","boss":"High"}
BAND_STD = {"trivial":"Low","standard":"Moderate","hard":"High","boss":"High"}
def per_char(level, band):
    lo,mo,hi = XPB[level]
    return {"half of Low":lo/2,"Low":lo,"Moderate":mo,"High":hi}[band]
def tier_budget(level, bandmap, P):
    return {t:int(per_char(level,bandmap[t])*P) for t in bandmap}
def cr_caps(floor, level, bandmap, P):
    mlo,mhi,elo,ehi,blo,bhi = CORE_CR[floor]
    tb = tier_budget(level, bandmap, P)
    core_up = {"trivial":mhi,"standard":mhi,"hard":ehi,"boss":bhi}
    out={}
    for t in tb:
        fit = fit_cr(int(tb[t]*LEAD_SHARE[t]))
        out[t] = min_cr(core_up[t],fit)
    return out

# ---------- loot deck expectations (derived from tables/loot-decks/f01-*.json) ----------
cards=[]
for f in glob.glob(ROOT+'/tables/loot-decks/f01-*.json'):
    if 'story' in f: continue
    cards+=json.load(open(f))['cards']
def pool(tier,kinds): return [(c['credit_value'],c['draw_weight']) for c in cards if c['tier']==tier and c['kind'] in kinds and (c.get('draw_weight') or 0)>0]
def wmean(p): return sum(v*w for v,w in p)/sum(w for v,w in p)
PT = [("consumable",.30),("gear",.25),("credits",.15),("tailored",.18),("weird",.10),("upgrade",.02)]
def pull_means(tier):
    credits = 52.5 if tier=="Bronze" else 175.0
    return {"consumable":wmean(pool(tier,['consumable'])),"gear":wmean(pool(tier,['item'])),"credits":credits,
            "tailored":wmean(pool(tier,['consumable','item'])),"weird":wmean(pool(tier,['junk','clue','key']) or pool(tier,['consumable']))}
mS = pull_means("Silver"); mB = pull_means("Bronze")
base_S = sum(p*mS[k] for k,p in PT if k!="upgrade")
E_S = base_S/(1-0.02)          # Silver upgrade (99-00) re-rolls on the next tier up; ceiling keeps it Silver
E_B = sum(p*mB[k] for k,p in PT if k!="upgrade") + 0.02*E_S
BRONZE_PULLS = 1.5; WELCOME_PULLS = 2
E_bronze_box = BRONZE_PULLS*E_B
E_welcome = mB["tailored"] + E_B     # pull 1 tailored, pull 2 d100 (overview 8.1)
E_silver_box = 2*E_S

# ---------- assumed economy parameters ----------
CASH = {  # credits per Crawler per encounter, Floor-1 scale
 "trivial": {"dice":"1d3-1","min":0,"avg":1.0,"max":2},
 "standard":{"dice":"1d4 x 2","min":2,"avg":5.0,"max":8},
 "hard":    {"dice":"1d6 x 2","min":2,"avg":7.0,"max":12},
 "boss":    {"dice":"1d6 x 5","min":5,"avg":17.5,"max":30}}
F1_CASH_OVERRIDE = {"trivial":0.0}   # overview: wandering Ticks carry no loot
R1 = {"min":10,"max":40,"avg":25.0}
R1_COUNT = {1:2, 2:3}
DEED_BRONZE = {1:0.5, 2:0.9}  # non-fight deed Bronze boxes expected per Crawler (achievement seeds etc.)

def mix_for(n):
    nn = n-1
    hard = max(1, rnd(0.15*nn)); trivial = rnd(0.25*nn); std = nn-hard-trivial
    return {"trivial":trivial,"standard":std,"hard":hard,"boss":1}
ENC_DENSITY = {2:1.5,3:1.5,4:1.5,5:1.5,6:1.5}
DAYS = {1:5,2:10,3:15,4:20,5:25,6:30}

def box_odds(fl, mix):
    """per-encounter box odds (fight share of the floor's expected Bronze/Silver), derived from targets."""
    if fl==1:
        b_fight = 0.40
    elif fl==2:
        b_fight = 1.10
    elif fl<=5:
        b_fight = 1.30
    else:
        b_fight = 1.00
    denom = mix["standard"]*1 + mix["hard"]*4
    p_std = round(b_fight/denom,2); p_hard = round(4*b_fight/denom,2)
    odds = {"trivial":{}, "standard":{"Bronze":p_std}, "hard":{"Bronze":p_hard}, "boss":{}}
    if fl<=2: odds["boss"]={"Silver":1.0}
    else:
        odds["boss"]={"Gold":1.0}
        s_fight = 0.5 if fl<=5 else 0.75
        odds["hard"]["Silver"] = round(s_fight/mix["hard"],2)
    exp = {"Bronze":round(mix["standard"]*p_std+mix["hard"]*p_hard,2)}
    if fl>2: exp["Silver"]=round(mix["hard"]*odds["hard"]["Silver"],2)
    exp["boss_box"] = "Silver" if fl<=2 else "Gold"
    return odds, exp

# ---------- build floors ----------
floors={}
for fl in range(1,7):
    d = DAYS[fl]
    mapb = BAND_F1 if fl==1 else BAND_STD
    levels = [1,2] if fl==1 else [fl]
    F = {"name": {1:"The Orientation Pit"}.get(fl,"(floor name per floor doc; core 2.1 working names only)")}
    F["clock"] = {"days":d,"days_field":"clock.days","days_status": "authoritative (decision 026)" if fl<=2 else ("authoritative that it is 15 or 20; Caleb to pick (decision 026); 15 used as default" if fl==3 else "ASSUMED placeholder; decision 026 says only 'later floors grow longer'"),
                  "short_rest_slots_per_day_cap":4,"short_rest_slots_total_cap":4*d,"long_rests_per_day":1,"long_rests_total":d,
                  "long_rest_where":"honest saferoom only (core 5.6; overview rule 7)"}
    if fl==3: F["clock"]["days_options"]=[15,20]
    F["level"] = {"arrive":fl,"leave":fl+1,"track":"standard (core 2.2)","status":"authoritative",
                  "budget_level": ({"before_green_room_z9":1,"boss_z10":2} if fl==1 else fl),
                  "note": "Floor 1 only: encounters before the Green Room (Z9) budget at level 1; the boss budgets at level 2 (overview rule 3). Floor N>=2: whole floor budgets at level N (descent level applies at the first saferoom of the next floor, core 2.3)." if fl==1 else "Whole floor budgets at level %d."%fl}
    F["tier_band_map"] = {"map":mapb,"status":"authoritative for F1 (overview 9.2 labels); ASSUMED for F2+ (core 8.3: mostly Moderate, some Low, 1-3 High per floor)"}
    F["xp_per_character"] = {("L%d"%L):{"low":XPB[L][0],"moderate":XPB[L][1],"high":XPB[L][2]} for L in levels}
    F["tiers"] = {}
    for L in levels:
        key = "L%d"%L
        F["tiers"][key] = {"xp_budget_total":{str(P):tier_budget(L,mapb,P) for P in PARTY},
                           "cr_caps":{str(P):cr_caps(fl,L,mapb,P) for P in PARTY}}
    # encounters
    if fl==1:
        mix={"trivial":1,"standard":3,"hard":1,"boss":1}
        n=6
        F["encounters"] = {"formula":"F1 is fixed by the module (overview 9.2): Z2, Z5, Z7 standard; Z8 hard; Z10 boss; plus wandering Ceiling Ticks (trivial), max 2 on the floor",
                           "total_planned":6,"wandering_max":2,"total_max":8,"total_max_source":"core 10.3: 4-8 encounters on F1",
                           "per_day_typical":round(6/d,2),"per_day_max":4,"mix_planned":mix,"quota":False,
                           "note":"Encounters are a ceiling envelope, not a quota. Unused days are fine."}
    else:
        opts = {}
        days_list = [15,20] if fl==3 else [d]
        for dd in days_list:
            n = rnd(dd*ENC_DENSITY[fl]); opts[str(dd)] = {"total":n,"mix":mix_for(n)}
        n = rnd(d*ENC_DENSITY[fl]); mix = mix_for(n)
        F["encounters"] = {"formula":"total = round(clock.days x per_day_typical); mix = boss 1, hard round(0.15 x (total-1)) (min 1), trivial round(0.25 x (total-1)), standard = rest",
                           "per_day_typical":ENC_DENSITY[fl],"per_day_max":4,"total_planned":n,"mix_planned":mix,"by_days_option":opts,"quota":False,
                           "wandering_max_per_day":1,"status":"ASSUMED (density, mix); per_day_max and the 'no quota' rule too"}
    # XP summaries
    mapL = lambda t: (1 if fl==1 and t!="boss" else 2) if fl==1 else fl
    xp_summ={}
    for P in PARTY:
        tot=0
        for t,c in mix.items():
            L = mapL(t)
            tot += c*tier_budget(L,mapb,P)[t]
        Lh = 2 if fl==1 else fl; L1 = 1 if fl==1 else fl
        cap_norm = tier_budget(L1,mapb,P)["hard"] + 2*tier_budget(L1,mapb,P)["standard"] + tier_budget(L1,mapb,P)["trivial"]
        cap_boss = tier_budget(Lh,mapb,P)["boss"] + tier_budget(Lh,mapb,P)["standard"]
        xp_summ[str(P)] = {"floor_xp_ceiling_total":tot,"daily_xp_budget_typical":round(tot/d,1),"daily_xp_budget_per_crawler":round(tot/d/P,1),
                           "daily_xp_cap_normal_day":cap_norm,"daily_xp_cap_boss_day":cap_boss}
    F["xp"] = {"definition":"floor_xp_ceiling_total = sum over planned encounters of the tier's xp_budget_total; daily_xp_budget_typical = that / clock.days. Caps: normal day = 1 hard + 2 standard + 1 trivial; boss day = boss + 1 standard. 2024 SRD has no adventuring-day XP table, so these are house guidelines (ASSUMED).",
               "by_party_size":xp_summ,"status":"derived from SRD budgets + ASSUMED mix/density"}
    # credits
    cscale = MULT[fl] if fl>=5 else 1
    ca = {}
    for t in CASH:
        c = dict(CASH[t]); 
        if fl==1 and t in F1_CASH_OVERRIDE: c["avg_f01_override"]=F1_CASH_OVERRIDE[t]
        ca[t]=c
    cash_exp = sum(mix[t]*(F1_CASH_OVERRIDE.get(t,CASH[t]["avg"]) if fl==1 else CASH[t]["avg"]) for t in mix)
    r1c = R1_COUNT.get(fl, 3)
    F["credits"] = {"cash_per_crawler_per_encounter_f1_scale":ca,"cash_scale":cscale,
                    "cash_scale_status":"ASSUMED = credit multiplier of the floor (core 3.9) applied to encounter cash; decision 019 names only achievement rewards and fees",
                    "cash_expected_per_crawler":round(cash_exp*cscale,1),
                    "r1_toast_credits_per_crawler":{"count_expected":r1c,"each_f1_scale":R1,"expected":round(r1c*R1["avg"]*cscale,1),"status":"ASSUMED; multiplier applies (achievement rewards, decision 019)"},
                    "pool_rule":"per-Crawler figures are flat; encounter cash pool = per-Crawler dice x P (scales with party), split evenly among living Crawlers. Spot amounts printed for 4 Crawlers in a floor doc scale by P/4. Boxes are per Crawler and never split.",
                    "status":"ASSUMED (GM may adapt)"}
    odds, expb = box_odds(fl, mix)
    F["boxes"] = {"odds_per_encounter_by_tier":odds,"expected_fight_boxes_per_crawler":expb,
                  "ceiling":"core 3.6/4.5: F1-2 Bronze+Silver only (boss box Silver); F3-5 up to Gold; F6 Gold (Platinum from F9)",
                  "core_pacing_per_crawler_per_floor":CORE_BOX["1-2" if fl<=2 else "3-5" if fl<=5 else "6-9"],
                  "non_fight_deed_boxes":"achievement deeds, quests, Welcome Box: GM judgment, see economy_audit for F1-2 expected counts",
                  "boss_box_condition":"Boss Box drops only if the boss is fought or talked down; bypassing via Zone S forfeits it (overview 6.7, 7.2)","story_box":"NOT in these odds: 0%. Story Boxes are GM hand-picked for one named deed, F1-2 only, cap 1 per table per floor, open only in a saferoom (rules/45).",
                  "status":"odds ASSUMED; ceilings and pacing authoritative"}
    # adjacency
    F["adjacency"] = {"boss_max_zones_from_saferoom": 1 if fl<=2 else 2,
                      "hard_max_zones_from_saferoom": 1 if fl==1 else 2,
                      "max_encounters_between_rests": 3,
                      "max_hard_or_boss_between_rests": 1,
                      "saferooms_min_per_floor": 2,
                      "boss_rest_before": "offer a short or long rest in the nearest honest saferoom before the boss; never force it",
                      "status":"ASSUMED (GM may adapt)"}
    floors[str(fl)] = F
    # stash mix for economy
    floors[str(fl)]["_mix"]=mix

# ---------- economy audit F1+F2 ----------
LINE=1500
def floor_econ(fl):
    F=floors[str(fl)]; mix=F["_mix"]
    cash = F["credits"]["cash_expected_per_crawler"]; r1 = F["credits"]["r1_toast_credits_per_crawler"]["expected"]
    exp_b = F["boxes"]["expected_fight_boxes_per_crawler"]["Bronze"] + DEED_BRONZE[fl]
    if fl==1:
        welcome = E_welcome; bronze_n = exp_b
        rows = [("encounter cash",cash),("R1 toast credits",r1),("Welcome Box (Bronze, 2 pulls: 1 tailored + 1 d100)",E_welcome),
                ("Deed/fight Bronze boxes (expected %.2f x %.1f)"%(exp_b,E_bronze_box),exp_b*E_bronze_box),("Silver Boss Box (1 x %.1f)"%E_silver_box,E_silver_box)]
        bronze_total = 1+exp_b
    else:
        rows = [("encounter cash",cash),("R1 toast credits",r1),("Bronze boxes (expected %.2f x %.1f)"%(exp_b,E_bronze_box),exp_b*E_bronze_box),("Silver Boss Box (1 x %.1f)"%E_silver_box,E_silver_box)]
        bronze_total = exp_b
    total = sum(v for _,v in rows)
    return {"rows":[{"item":k,"expected_credits":round(v,1)} for k,v in rows],"expected_total_per_crawler":round(total,1),"expected_bronze_boxes":round(bronze_total,2),"expected_silver_boxes":1}
econ = {"line_per_crawler_f1_plus_f2":LINE}
e1=floor_econ(1); e2=floor_econ(2)
tot = round(e1["expected_total_per_crawler"]+e2["expected_total_per_crawler"],1)
econ["floor_1"]=e1; econ["floor_2"]=e2
econ["expected_total_f1_f2_per_crawler"]=tot
econ["headroom_to_line"]=round(LINE-tot,1)
econ["share_of_line"]=round(tot/LINE,3)
econ["by_party_size"]={str(P):{"per_crawler_f1":e1["expected_total_per_crawler"],"per_crawler_f2":e2["expected_total_per_crawler"],"per_crawler_f1_f2":tot,
                                "cash_pool_f1":round(floors["1"]["credits"]["cash_expected_per_crawler"]*P,1),
                                "cash_pool_f2":round(floors["2"]["credits"]["cash_expected_per_crawler"]*P,1),
                                "table_total_f1_f2":round(tot*P,1)} for P in PARTY}
econ["per_crawler_flat_across_party_size"]=True
econ["pull_expectations"]={"bronze_pull_mean":round(E_B,2),"silver_pull_mean":round(E_S,2),"bronze_box_mean_1_5_pulls":round(E_bronze_box,1),
                            "welcome_box_mean_2_pulls":round(E_welcome,1),"silver_box_mean_2_pulls":round(E_silver_box,1),
                            "pull_type_table":[{"d100":"01-30","type":"consumable","p":.30},{"d100":"31-55","type":"gear","p":.25},{"d100":"56-70","type":"credits","p":.15},{"d100":"71-88","type":"tailored","p":.18},{"d100":"89-98","type":"weird","p":.10},{"d100":"99-00","type":"upgrade (re-roll one tier up, ceiling applies)","p":.02}],
                            "means_bronze":{k:round(v,2) for k,v in mB.items()},"means_silver":{k:round(v,2) for k,v in mS.items()},
                            "source":"core 4.2 pull table and credit dice; means over draw_weight>0 cards in tables/loot-decks/f01-*.json (Story Box deck excluded); F2 assumed to use the same value ranges (no F2 decks yet)"}
econ["governor"]={"soft_stop_running_total":1100,"hard_flag":1500,"rule":"If a Crawler's running F1+F2 economy total (cash credits + box credits + credit_value of box items; Story Box story_value excluded, Story Box sale proceeds included) passes the soft stop before the Floor 2 Boss Box is opened, the GM hand-picks the lower-value pulls (consumables and credit pulls) for that Crawler's remaining boxes. Tighten boxes before nerfing items (core 3.7; rules/40 3.2).","status":"ASSUMED"}
econ["not_counted"]=["Story Box story_value (rules/45 6.3 excludes it from the flag)","vendor spending (potions, bribes, tolls, fees) - these are sinks, not income","resale of box items at half credit_value (already counted at credit_value; do not count twice)","placed mundane goods and placed Potions of Healing (not boxes, not credits)"]
econ["counted_but_unplanned"]=["Story Box item sale proceeds (fixed sale_value 100/250/500 by rung, rules/45 4.6): count toward the flag. Headroom covers a rung 0 or rung 1 sale; a rung 2 sale (500) would flag, and the Accountant flags but never blocks."]

# ---------- simulation (tail check) ----------
sys.path.insert(0, _HERE)
import tail
os_cwd = __import__("os").chdir(ROOT)
o1=floors["1"]["boxes"]["odds_per_encounter_by_tier"]; o2=floors["2"]["boxes"]["odds_per_encounter_by_tier"]
kw=dict(N=100000,seed=70,p1=((o1["standard"]["Bronze"],3),(o1["hard"]["Bronze"],1)),p2=((o2["standard"]["Bronze"],8),(o2["hard"]["Bronze"],2)))
def pack(r): return {"mean":r[0],"p50":r[1],"p90":r[2],"p95":r[3],"pct_over_1500":r[4]}
sim_ng = pack(tail.run(**kw)); sim_g = pack(tail.run(gov_thr=800,gov_cap=175,**kw))
econ["governor"]={"soft_stop_running_total_before_f2_boss_box":800,"pull_value_cap_when_triggered":175,"hard_flag":1500,
  "rule":"Before the Floor 2 Boss Box is opened, add up that Crawler's F1+F2 economy total so far (cash credits, box credits, credit_value of box items; Story Box story_value excluded, Story Box sale proceeds included; tools: state.py loot totals and ledger). If it is 800 or more, hand-pick that box's pulls from cards worth 175 or less (greater Potion of Healing, a Silver credit pull, consumables). Tighten boxes before nerfing items (core 3.7; rules/40 3.2).",
  "status":"ASSUMED"}
econ["simulation"]={"method":"Monte Carlo, 100000 Crawlers per run, seed 70, plan counts and odds as in this file; Welcome Box 2 plain pulls (slightly high), other Bronze 1-2 pulls, Silver 2 pulls from the F1 deck weights, cash dice as in assumed.cash_per_crawler_f1_scale, R1 uniform 10-40. Scratch script, not filed.",
                    "without_governor":sim_ng,"with_governor":sim_g}

# ---------- F1 fixed encounters ----------
def xp_of(parts): return sum(CR_XP[cr]*n for cr,n in parts)
f1 = {}
spec = {
 "z02":{"name":"Vent Rats","tier":"standard","level":1,"day_slot":None,
        "creatures":[("giant-rat","1/8",{"2":3,"3":4,"4":6})]},
 "z05":{"name":"Mannequin Staff","tier":"standard","level":1,
        "creatures":[("skeleton","1/4",{"2":2,"3":3,"4":4})]},
 "z07":{"name":"Exit Greeters (Big Green EXIT)","tier":"standard","level":1,
        "creatures":[("goblin-warrior","1/4",{"2":1,"3":1,"4":2}),("goblin-minion","1/8",{"2":2,"3":3,"4":4})]},
 "z08":{"name":"The Elite (Mascot Locker Room)","tier":"hard","level":1,
        "creatures":[("animated-armor","1",{"2":1,"3":1,"4":1}),("animated-flying-sword","1/4",{"2":0,"3":1,"4":2})]},
 "wandering":{"name":"Ceiling Ticks (Lights-Out)","tier":"trivial","level":1,"max_on_floor":2,
        "creatures":[("stirge","1/8",{"2":2,"3":3,"4":4})]},
 "z10":{"name":"Dean Thudd (boss)","tier":"boss","level":2,
        "creatures":[("ogre","2",{"2":0,"3":1,"4":1}),("bugbear-warrior","1",{"2":1,"3":0,"4":0}),("skeleton","1/4",{"2":4,"3":2,"4":4})],
        "note":"Boss: 2 Crawlers use overview Variant B (Bugbear Warrior + 4 Skeletons); 3 use Ogre + 1 + 1 Skeletons; 4 use Ogre + 2 + 2 Skeletons (the +2 arrive in Phase 2). Skeleton counts are totals across both phases."}}
mapb=BAND_F1
for zid,s in spec.items():
    L=s["level"]; counts={}; xp={}; within={}
    for P in PARTY:
        ps=str(P); parts=[(cr,c[ps]) for _,cr,c in s["creatures"]]
        counts[ps]={sid:c[ps] for sid,_,c in s["creatures"]}
        xp[ps]=xp_of(parts)
        bud=tier_budget(L,mapb,P)[s["tier"]]
        within[ps]={"xp_used":xp[ps],"tier_budget":bud,"over_by":max(0,xp[ps]-bud),"within_tier":xp[ps]<=bud}
    f1[zid]={"name":s["name"],"tier":s["tier"],"budget_level":L,"creatures":[{"srd_id":sid,"cr":cr} for sid,cr,_ in s["creatures"]],
             "counts_by_party_size":counts,"xp_by_party_size":xp,"fit":within,
             "cash_per_crawler":(F1_CASH_OVERRIDE.get(s["tier"],CASH[s["tier"]]["avg"])),
             "cash_dice_per_crawler":("none (overview: wandering Ticks carry no loot)" if s["tier"]=="trivial" else CASH[s["tier"]]["dice"])}
    if "note" in s: f1[zid]["note"]=s["note"]
    if "max_on_floor" in s: f1[zid]["max_on_floor"]=s["max_on_floor"]
f1["_status"]="counts mirror floors/f01/00-overview.md 9.2/9.3 verbatim (authoritative for Floor 1 until Caleb says otherwise); fit flags show where the overview runs above the tier budget"
floors["1"]["fixed_encounters"]=f1
# boss at level 1 (Variant B strict)
floors["1"]["boss_variant_b_level1"]={"budget_level":1,"xp_budget_total":{str(P):tier_budget(1,mapb,P)["boss"] for P in PARTY},"note":"Boss at level 1 (table declines the Green Room milestone): Bugbear Warrior (CR 1) + Skeletons; 4 Crawlers = 400 XP = High (overview 6.6)."}

DETOUR_TAX=75; REST_FEE=20; REST_CAP=60; BRIBE=50; FORCING=25
# ---------- price / cost fields (assumed) ----------
prices = {
 "currency":"credits (1 credit = 1 GP, core 5.10); F1 prices at Floor-1 scale; System fees multiply by the floor credit multiplier (decision 019)",
 "potion_of_healing_vendor":{"price":50,"stock_floor_wide":2,"sells_back_at":0.5,"status":"authoritative (overview 5.6/8.3: 50 credits, 2 in stock for the whole floor, shared Z6/Z9)"},
 "rest_without_saferoom":{
   "applies_to":"Floor 1: any Long Rest attempt outside an open saferoom (Z6 is a saferoom through Day 3; the Z9 Green Room stays open to the end, so a saferoom is always reachable)",
   "long_rest_granted":False,"long_rest_rule":"Long Rest only in saferooms (core 5.6; overview rule 7); a field attempt is interrupted by Ceiling Ticks after 1d4 hours",
   "unlicensed_rest_fee_per_crawler":REST_FEE,"fee_cap_per_crawler_per_floor":REST_CAP,
   "party_fee_by_size":{str(P):REST_FEE*P for P in PARTY},
   "interruption_encounter":{"tier":"trivial","creature":"Ceiling Ticks","counts_against_wandering_max":True},
   "never_a_wipe":True,"status":"ASSUMED",
   "reasoning":"20 credits = 40% of one Potion of Healing (50) and below the R1 toast band (10-40); 3 billings cap at 60 = 4% of the 1,500 line. A saferoom is free, so the fee only has to sting, not threaten."},
 "stairwell_key_terminal_bribe":{
   "where":"Floor 1 Break Room (Z6) Snakk-Matic terminal; gone on Day 4 when the Break Room and vendors lose service (decision 026)",
   "price_per_crawler":BRIBE,"party_price_by_size":{str(P):BRIBE*P for P in PARTY},"payable_by_pooling":True,"haggle":"allowed at the terminal's normal DC 13 / 15% off (core 5.10; overview 5.6), GM may refuse",
   "status":"ASSUMED",
   "reasoning":"50 per Crawler = one Potion of Healing each (3.3% of the 1,500 line). It buys a quiet skip of the Z10 fight, which also forfeits the Silver Boss Box (about 429 credits of expected value), so the bribe is cheap in credits and expensive in opportunity."},
 "detour_tax":{
   "what":"The System's Detour Tax toll. It is the only credit toll on the clock (the collapse steps themselves cost hooks and services only). Charged (1) to a Crawler who reaches the Zone S door with no key and takes the paid way through, and (2) to Floor 1 stragglers hauled down after a missed collapse (decision 026 defaults, Caleb may veto; not a death, Reprieve untouched). A missed collapse adds the forfeits and Exhaustion written in decision 026; no extra credits.",
   "toll_per_crawler":DETOUR_TAX,"party_toll_by_size":{str(P):DETOUR_TAX*P for P in PARTY},"payable_by_pooling":True,
   "shortfall":"a Crawler who cannot pay pays what they have and the GM logs the balance (no debt mechanic)","scales_with_floor_multiplier":True,"status":"ASSUMED",
   "reasoning":"75 = 1.5 x the bribe (waiting costs more than buying early) and 5% of the 1,500 line. The big cost of a missed collapse is the forfeited loot and Boss Box (about 429 expected credits), not the toll."},
 "zone_s_door_forcing":{
   "mechanics_source":"overview 5.10: Thieves' Tools DC 15 or Strength (Athletics) DC 15, 10 minutes, loud; Dean Thudd and his Ushers come looking 1 minute later",
   "forcing_fee_per_crawler":FORCING,"party_fee_by_size":{str(P):FORCING*P for P in PARTY},"status":"ASSUMED",
   "reasoning":"25 per Crawler is the cheapest in credits because forcing already pays in danger (the boss arrives at the Crawlers' worst moment). Ordering: forcing 25 < bribe 50 < Detour Tax 75."},
 "detour":{"hours":2,"short_rest_slots_used":0,"extra_ceiling_tick_rolls":4,"note":"Walking back to Z8 or Z6 while they still serve: 2 in-game hours, no rest slot consumed, 4 extra d6 Ceiling Tick rolls (one per 30 minutes, overview rule 6).","status":"ASSUMED"},
 "collapse_step_costs":{"credit_cost_per_step":0,"model":"Each collapse step costs the party the hooks and services in the closed zones (loot, achievements, vendors), not credits; the Detour Tax is the only toll on the clock (day spec collapse_order_status). The way to Z9, Z10, Z11 is never cut.","status":"matches the day-spec wording; amounts ASSUMED"}}

# ---------- authoritative block ----------
auth = {
 "status":"authoritative: copied or derived directly from a filed source; change only by changing the source",
 "xp_budget_per_character":{"source":"SRD 5.2.1 'XP Budget per Character' (same table the overview 9.1 uses for levels 1-2). No group multiplier in 2024.",
                             "by_level":{str(L):{"low":a,"moderate":b,"high":c} for L,(a,b,c) in XPB.items()}},
 "xp_by_cr":{"source":"SRD 5.2.1 'Experience Points by Challenge Rating'","table":CR_XP,"note":"CR 11, 12, 13 are missing from the SRD text extraction used here (7,200 / 8,400 / 10,000 are the standard values); verify before relying on them. CR 0 is 0 or 10 XP; this file uses 0."},
 "level_track":{"source":"core 2.2 standard track: arrive on Floor N at level N, leave at N+1; Floor 1 gains level 2 at the Green Room (core 2.3, overview rule 3)","slow_burn":"table option; look up the floor whose level matches (core 8.3 note)"},
 "core_cr_targets_party_of_4":{"source":"core 8.3","columns":["mob_lo","mob_hi","elite_lo","elite_hi","boss_lo","boss_hi"],"by_floor":{str(f):list(v) for f,v in CORE_CR.items()}},
 "clock":{"source":"decision 026 (Caleb) + Syndicate confirmation","days":{"1":5,"2":10,"3":"15 or 20 (Caleb to pick)"},"short_rest_slots_per_day_cap":4,"long_rest_per_day":1,
          "stairwell_opens_after_hours":32,"stairwell_opens_note":"about 32 hours after the floor opens, early Day 2 (canon M-276, verified by Lore); Z10 arena holds a stairwell (M-275); the key and Zone S door are house ideas tagged inspired",
          "final_collapse":{"hour_of_floor":120,"rule":"fixed: 24 in-game hours into the last day; a Long Rest never ends or skips the floor; the System cuts short a rest that would run past it","status":"Syndicate default in decision 026 (~9:45 PM CT); Caleb may veto"},
          "break_room_saferoom_through_day":3,
          "early_descent":{"threshold_hours_left":6,"rule":"a Crawler who descends with more than 6 hours left is held in stasis until the floor collapses (M-277): banks the achievement, ends that Crawler's floor; in the last 6 hours descent is free; each Crawler chooses; the GM may log an override"},
          "collapse_order_floor_1":[{"day":1,"event":"nothing closes"},{"day":2,"event":"outer zones close"},{"day":3,"event":"mid zones close"},{"day":4,"event":"Break Room (Z6) and vendors lose service"},{"day":5,"event":"only the Stairwell corridor stays"}],
          "zone_groups_floor_1":{"outer_close_day_2":["Z0","Z1","Z2","Z3","Z3b","Z4"],"mid_close_day_3":["Z5","Z7","Z8"],"corridor_stays_to_end":["Z10","Z11","ZS"],"z6_break_room":"loses service Day 4","z9_green_room":"saferoom stays open to the end","route_rule":"closed means hooks and services vanish; the route (Z6, Z8, Z9, Z10, Z11) is never cut","key_deadlines":{"bruiser_key_gone_day":3,"terminal_key_gone_day":4}}},
 "box_credit_dice":{"source":"core 4.2 (no floor multiplier on box credit pulls, decision 019)","Bronze":"3d6 x 5","Silver":"2d6 x 25","Gold":"2d6 x 250","Platinum":"2d6 x 2500","Legendary":"2d6 x 10000","pulls":{"Bronze":"1-2","Silver":2,"Gold":"2-3","Platinum":3}},
 "box_pacing_per_crawler_per_floor":{"source":"core 4.5","by_band":CORE_BOX},
 "floor_rarity_ceiling":{"source":"core 3.6","F1-2":{"default":"Common","peak":"Uncommon"},"F3-5":{"default":"Uncommon","peak":"Rare"},"F6-9":{"default":"Rare","peak":"Very Rare"}},
 "credit_multiplier":{"source":"core 3.9; decision 019","x1":"F1-4","x5":"F5-9","x20":"F10-14","x50":"F15-18","applies_to":["achievement rewards","System fees (repairs, Story Box buyback, crafting)"],"does_not_apply_to":["box credit pulls","revive fees","Upgrade Coupon cap"]},
 "story_box_constraints":{"source":"decisions 015/018; rules/45; core 4.1/4.5/4.7","floors":[1,2],"cap_per_table_per_floor":1,"awarded_by":"GM hand-pick only, one named one-time deed, never random","opens_only_in":"a saferoom","box_odds_in_this_file":0,"sale_value_by_rung":{"0":100,"1":250,"2":500},"sale_value_note":"Floor-1 scale; times the sale floor's multiplier; story_value is provenance only and excluded from the 1,500 flag, a sale is not"},
 "floor_1_reprieve":{"source":"core 6.2; STATE-OF-BUILD 6","floor_1_only":True,"note":"No budget field changes it; this file prices missing keys, rest and clock costs as costs, never wipes."},
 "saferoom_rules":{"source":"core 5.6; overview rule 5/7","long_rest":"saferooms only","short_rest":"anywhere reasonably quiet; guaranteed in a saferoom","floor_1_saferooms":["Z6 Break Room","Z9 Green Room"],"honest_on_floor_1":True,"saferooms_can_lie_from":2},
 "floor_1_encounter_composition":"see floors.1.fixed_encounters (mirrors overview 9.2/9.3)"}

adj_global = {"status":"ASSUMED (GM may adapt)","fields":{
  "boss_max_zones_from_saferoom":"F1-2: 1 (one door; F1 Z10 sits one door from the Z9 Green Room per overview 6.7); F3+: 2",
  "hard_max_zones_from_saferoom":"F1: 1 (Z8 sits between Z6 and Z9); F2+: 2",
  "max_encounters_between_rests":3,"max_hard_or_boss_between_rests":1,
  "wandering_encounters":"F1: max 2 on the floor (overview 5.11, authoritative); F2+: max 1 per day",
  "saferooms_min_per_floor":2,
  "rule_of_thumb":"A Crawler should never be more than two fights from an honest saferoom on F1-2."}}

assumed_list = [
 {"id":"A1","what":"Tier-to-band map: F1 trivial=half of Low, standard=Low, hard=Moderate, boss=High (matches overview 9.2). F2+ trivial=Low, standard=Moderate, hard=High (elite), boss=High (core 8.3: mostly Moderate, some Low, 1-3 High per floor).","adapt":"Caleb/GM"},
 {"id":"A2","what":"Boss lead creature fits within 90% of the High total so support has room; other tiers 100%.","adapt":"Caleb/GM"},
 {"id":"A3","what":"Encounter density: F1 fixed list (6 planned, max 8); F2-F6 1.5 encounters per clock day, no quota; mix = boss 1, hard 15%, trivial 25%, standard rest.","adapt":"Caleb/GM"},
 {"id":"A4","what":"Days: F4=20, F5=25, F6=30 are placeholders (decision 026 says only that later floors grow longer); F3 defaults to 15 and also lists 20.","adapt":"Caleb"},
 {"id":"A5","what":"Encounter cash per Crawler by tier (F1 scale): trivial 0-2, standard 1d4x2, hard 1d6x2, boss 1d6x5; pool = per-Crawler x party size, split evenly. F1 values are sized so a 4-Crawler party's spot amounts in the overview (about 158 credits across the floor) fit inside the tiers.","adapt":"Accountant/GM"},
 {"id":"A6","what":"R1 toast credits 10-40 (avg 25); expected credit-paying R1 toasts per Crawler: F1 2, F2 3, F3+ 3.","adapt":"Accountant/GM"},
 {"id":"A7","what":"Per-encounter box odds are the fight share of core 4.5 targets; non-fight deed Bronze expected 0.5 (F1) and 0.9 (F2) per Crawler. F1 total Bronze (incl. Welcome) is 1.9 expected, inside the overview's 1-3; F2 about 2.0, the low end of core 2-4.","adapt":"Caleb/GM"},
 {"id":"A8","what":"F2 Boss Box is Silver (core 4.7 cap) and F2 box values equal F1's (no F2 decks exist yet).","adapt":"Lore"},
 {"id":"A9","what":"Encounter cash on F5+ takes the credit multiplier (x5); box pulls do not (decision 019).","adapt":"Caleb/Accountant"},
 {"id":"A10","what":"Rest-without-saferoom fee 20 per Crawler (cap 60 per floor); key bribe 50 per Crawler; Detour Tax 75 per Crawler (missed key and Floor 1 missed collapse); Zone S forcing fee 25 per Crawler; detour 2 hours, 0 rest slots; collapse steps cost hooks and services, 0 credits.","adapt":"Caleb/GM"},
 {"id":"A11","what":"Safe-room adjacency and rest-segment limits (see adjacency).","adapt":"GM"},
 {"id":"A12","what":"Economy governor: before the F2 Boss Box, if a Crawler's F1+F2 running total is 800 or more, that box is hand-picked from cards worth 175 or less; hard flag stays 1,500 (Accountant).","adapt":"Accountant"},
 {"id":"A14","what":"Reward ladder for the six proposed achievements (floors.1.achievement_rewards).","adapt":"Caleb/GM"},
 {"id":"A13","what":"The audit line is read as F1+F2 combined per Crawler (the stricter reading); rules/40 3.2 words the hint as 'per crawler per floor'.","adapt":"Accountant"}]

# ---------- slot map (matches floors/f01/day-01.json 'slots' order, spec regenerated 2026-10-04 21:47) ----------
SL = []
def S(no,path,label,field,value_by_p=None,value=None,mode="number"):
    SL.append({"slot_no":no,"spec_path":path,"label":label,"fills_from":field,"mode":mode,
               **({"value_by_party_size":value_by_p} if value_by_p is not None else {}),**({"value":value} if value is not None else {})})
F1=floors["1"]; fe=F1["fixed_encounters"]
def cnt(zid,sid): return {str(P):fe[zid]["counts_by_party_size"][str(P)][sid] for P in PARTY}
def txt_budget(zid):
    return {str(P):"%s tier, %s band: budget %d XP for %d Crawlers (level %d); used %d XP%s" % (fe[zid]["tier"],mapb[fe[zid]["tier"]],fe[zid]["fit"][str(P)]["tier_budget"],P,fe[zid]["budget_level"],fe[zid]["xp_by_party_size"][str(P)],
                (" (over by %d, overview 9.3 count kept)"%fe[zid]["fit"][str(P)]["over_by"]) if fe[zid]["fit"][str(P)]["over_by"] else "") for P in PARTY}
DT = {str(P):"Detour Tax: %d credits per Crawler (%d for the party), payable by pooling; a Crawler who is short pays what they have and the GM logs the balance"%(DETOUR_TAX,DETOUR_TAX*P) for P in PARTY}
REST = {str(P):"Rest without a saferoom: %d credits per Crawler (%d for the party), cap %d per Crawler per floor; no Long Rest is granted; Ceiling Ticks interrupt after 1d4 hours; never a wipe"%(REST_FEE,REST_FEE*P,REST_CAP) for P in PARTY}
S(1,"/clock/collapse_cost_slot","DETOUR TAX","floors.1.prices.detour_tax",value_by_p=DT,mode="text")
S(2,"/clock/rest_without_saferoom_slot","REST-WITHOUT-SAFEROOM COST","floors.1.prices.rest_without_saferoom",value_by_p=REST,mode="text")
S(3,"/clock/collapse_miss/effects[2]","DETOUR TAX","floors.1.prices.detour_tax",value_by_p=DT,mode="text")
S(4,"/clock/collapse_miss/toll_slot","DETOUR TAX","floors.1.prices.detour_tax",value_by_p={str(P):DETOUR_TAX*P for P in PARTY})
S(5,"/day/rest_options[2]/note","REST-WITHOUT-SAFEROOM COST","floors.1.prices.rest_without_saferoom",value_by_p=REST,mode="text")
S(6,"/day/proposed_achievements[0]/reward_slot","REWARD (Slow Learner)","floors.1.achievement_rewards.proposed.slow_learner",value="R1: Title plus 25 credits (band 10-40), or snark-only if the GM prefers. No box. Counts toward the R1 credit expectation in economy_audit.",mode="text")
S(7,"/stairwell_key/ways[1]/price_slot","CREDITS (key price)","floors.1.prices.stairwell_key_terminal_bribe",value_by_p={str(P):BRIBE*P for P in PARTY})
S(8,"/stairwell_key/missing_key_cost/toll_slot","DETOUR TAX","floors.1.prices.detour_tax",value_by_p={str(P):DETOUR_TAX*P for P in PARTY})
S(9,"/encounters[0]/cr_slot","CR","floors.1.fixed_encounters",value="none (non-combat)",mode="text")
S(10,"/encounters[0]/budget_slot","BUDGET (enc-d01-01)","floors.1.xp.by_party_size",value="Non-combat: 0 XP, no combat budget. Credit and box budget: see slots 11 and 12.",mode="text")
S(11,"/encounters[0]/loot_hooks[0]/amount","LOOT AMOUNT (Welcome Box)","economy_audit.pull_expectations",value="Bronze Welcome Box per Crawler: 1-2 pulls (pull 1 tailored, pull 2 d100); credit pull 3d6 x 5; expected box value about %d credits (credit_value)."%round(E_welcome),mode="text")
S(12,"/encounters[0]/loot_hooks[4]/amount","CREDITS (vendor price)","floors.1.prices.potion_of_healing_vendor",value=50)
S(13,"/encounters[0]/proposed_achievements[0]/reward_slot","REWARD (Read the Fine Print)","floors.1.achievement_rewards.proposed.read_the_fine_print",value="R0: snark-only Title, 0 credits (the bribe was the cost).",mode="text")
S(14,"/encounters[1]/enemies[0]/count_slot","COUNT (greeter-warrior)","floors.1.fixed_encounters.z07.counts_by_party_size",value_by_p=cnt("z07","goblin-warrior"))
S(15,"/encounters[1]/enemies[0]/cr_slot","CR (greeter-warrior)","floors.1.fixed_encounters.z07.creatures",value="1/4",mode="text")
S(16,"/encounters[1]/enemies[1]/count_slot","COUNT (greeter-minion)","floors.1.fixed_encounters.z07.counts_by_party_size",value_by_p=cnt("z07","goblin-minion"))
S(17,"/encounters[1]/enemies[1]/cr_slot","CR (greeter-minion)","floors.1.fixed_encounters.z07.creatures",value="1/8",mode="text")
S(18,"/encounters[1]/budget_slot","BUDGET (enc-d01-02)","floors.1.fixed_encounters.z07.fit",value_by_p=txt_budget("z07"),mode="text")
S(19,"/encounters[1]/loot_hooks[0]/amount","LOOT AMOUNT (Back Office cache)","floors.1.fixed_encounters.z07.cash_dice_per_crawler",value="Back Office cache: 0 credits and no box (recipe card, 2 goblin oil, worn Tinker's Tools per overview 5.7). Greeter pocket change falls under the standard tier: 1d4 x 2 credits per Crawler (pool = x party size).",mode="text")
S(20,"/encounters[2]/enemies[0]/count_slot","COUNT (elite-armor)","floors.1.fixed_encounters.z08.counts_by_party_size",value_by_p=cnt("z08","animated-armor"))
S(21,"/encounters[2]/enemies[0]/cr_slot","CR (elite-armor)","floors.1.fixed_encounters.z08.creatures",value="1",mode="text")
S(22,"/encounters[2]/enemies[1]/count_slot","COUNT (lanyard-blade)","floors.1.fixed_encounters.z08.counts_by_party_size",value_by_p=cnt("z08","animated-flying-sword"))
S(23,"/encounters[2]/enemies[1]/cr_slot","CR (lanyard-blade)","floors.1.fixed_encounters.z08.creatures",value="1/4",mode="text")
S(24,"/encounters[2]/budget_slot","BUDGET (enc-d01-03)","floors.1.fixed_encounters.z08.fit",value_by_p=txt_budget("z08"),mode="text")
S(25,"/encounters[2]/loot_hooks[0]/amount","LOOT AMOUNT (service key)","floors.1.prices.zone_s_door_forcing",value="n/a: quest item, 0 credits. If the party misses it, see detour_tax, the terminal bribe and zone_s_door_forcing.",mode="text")
S(26,"/encounters[2]/loot_hooks[1]/amount","LOOT AMOUNT (placed Potion)","floors.1.prices.potion_of_healing_vendor",value="n/a: placed consumable (third placed Potion of Healing, overview 8.3); vendor value 50 credits, not counted as income.",mode="text")
S(27,"/encounters[3]/enemies[0]/count_slot","COUNT (ticks)","floors.1.fixed_encounters.wandering.counts_by_party_size",value_by_p=cnt("wandering","stirge"))
S(28,"/encounters[3]/enemies[0]/cr_slot","CR (ticks)","floors.1.fixed_encounters.wandering.creatures",value="1/8",mode="text")
S(29,"/encounters[3]/budget_slot","BUDGET (enc-d01-04)","floors.1.fixed_encounters.wandering.fit",value_by_p=txt_budget("wandering"),mode="text")
S(30,"/encounters[3]/loot_note","LOOT AMOUNT (Ticks)","floors.1.fixed_encounters.wandering.cash_dice_per_crawler",value="0 credits, no box (trivial tier, F1 override: wandering Ticks carry no loot).",mode="text")
S(31,"/encounters[3]/if_they_do_something_dumb","REST-WITHOUT-SAFEROOM COST","floors.1.prices.rest_without_saferoom",value_by_p=REST,mode="text")
S(32,"/encounters[4]/cr_slot","CR","floors.1.fixed_encounters",value="none (non-combat)",mode="text")
S(33,"/encounters[4]/budget_slot","BUDGET (enc-d01-05)","floors.1.xp.by_party_size",value="Non-combat: 0 XP, no combat budget. Day close in the Z9 saferoom: all earned boxes open at once (slot 34).",mode="text")
S(34,"/encounters[4]/loot_hooks[3]/amount","LOOT AMOUNT (box openings)","economy_audit.floor_1",
  value_by_p={str(P):"Opens every earned box per Crawler, lowest tier first. Expected on F1: Welcome Bronze (if not yet opened) plus about %.1f deed/fight Bronze (soft cap 2-3 achievement boxes per Crawler per floor), Silver Boss Box after Z10 (only if the boss is fought or talked down). Expected value per Crawler for the whole floor (cash, R1 toasts, boxes): about %d credits; credits per Crawler do not change with party size, table total = x %d."%(floors["1"]["boxes"]["expected_fight_boxes_per_crawler"]["Bronze"]+DEED_BRONZE[1],round(e1["expected_total_per_crawler"]),P) for P in PARTY},mode="text")

# ---------- assemble ----------
for k,v in floors.items():
    v.pop("_mix",None)
floors["1"]["prices"]=prices
floors["1"]["achievement_rewards"]={
 "status":"ASSUMED; the six proposed achievements are a seed list at GM discretion, rewards tailored by the GM, snark-only allowed (decision 026, day-spec achievement_caps)",
 "ladder":{"R0":"snark-only, Title, 0 credits","R1":"Title plus 10-40 credits (avg 25) times the floor multiplier","R2":"Heroic Inspiration (at most 1 per session from achievements, core 3.7)","R3":"Common consumable (F1-2 ceiling)","R5":"Bronze box on F1-2 (named for the deed); Silver only as the Boss Box"},
 "soft_cap_achievement_boxes_per_crawler_per_floor":"2-3 (Caleb's ruling as quoted in the day spec); this file expects about 0.5 (F1) and 0.9 (F2) deed Bronze boxes",
 "never":["Gold or higher on F1-2","a second Silver box from an achievement","Story Box (separate GM hand-pick, rules/45)","XP (core 3.4)"],
 "proposed":{
  "slow_learner":{"trigger":"Clear every Day 1 to 3 encounter before descending","reward":"R1: Title + 25 credits"},
  "read_the_fine_print":{"trigger":"Use the Break Room terminal bribe route","reward":"R0: snark-only Title"},
  "last_one_out":{"trigger":"Hold a closing zone until the party is clear, then reach the Green Room","reward":"R2: Heroic Inspiration"},
  "detour_tax":{"trigger":"Pay the missed-key toll and still descend","reward":"R0: snark-only Title"},
  "early_withdrawal":{"trigger":"Choose early-descent stasis","reward":"R0: snark-only Title"},
  "hold_please":{"trigger":"Talk Dean Thudd down without a fight","reward":"R5: Bronze box named for the deed (the Silver Boss Box still drops, overview 6.7)"}}}
floors["1"]["economy_note"]="Floor 1 expected economy per Crawler: see economy_audit.floor_1"
fl_placeholders = {}
for f in range(7,19):
    mlo,mhi,elo,ehi,blo,bhi=CORE_CR[f]
    fl_placeholders[str(f)] = {"level_arrive":f,"level_leave":f+1 if f<18 else "19-20 (finale)","budget_level":f,
        "xp_per_character_at_budget_level":dict(zip(["low","moderate","high"],XPB[min(f,20)])),
        "core_8_3_cr":{"mob":[mlo,mhi],"elite":[elo,ehi],"boss":[blo,bhi]},"credit_multiplier":MULT[f],
        "days":"PLACEHOLDER (decision 026: later floors grow longer)","encounters_per_day_typical":"PLACEHOLDER","mix":"PLACEHOLDER (apply mix rule)",
        "cash_per_crawler":"PLACEHOLDER (tier dice x credit multiplier, if A9 is kept)","box_targets":"core 4.5 row for the floor band","audit_line":"PLACEHOLDER (Accountant)",
        "status":"formula only; nothing here is invented detail"}
formula = {
 "status":"formula and placeholders only",
 "steps":["level = floor number (standard track); band map = BAND_STD (A1)",
          "tier budget(P) = SRD per-character XP at the budget level for the band x party size P",
          "CR cap(tier) = min(core 8.3 upper bound for the tier, highest CR whose XP <= lead_share x tier budget); lead_share = 0.9 for boss, 1.0 otherwise",
          "encounters total = round(days x per_day_typical); mix rule as floors.2.encounters.formula",
          "daily XP budget = sum(tier counts x tier budget) / days; caps: normal day 1 hard + 2 standard + 1 trivial; boss day boss + 1 standard",
          "encounter cash per Crawler = tier dice x cash_scale; cash_scale = credit multiplier (A9) so rewards keep pace with fees",
          "box odds = fight share of the core 4.5 target / eligible encounters (hard weighs 4x standard for Bronze); boss box: F1-2 Silver, F3-8 Gold, F9+ Platinum (core 4.7, ceilings 3.6)",
          "rest slots: 4 short-rest slots (cap) and 1 Long Rest per day; days = clock.days"],
 "floors":fl_placeholders}

doc = {
 "schema":"encounter-budget/0.1",
 "version":"0.1.0",
 "meta":{"title":"Encounter budget, credits and loot (5e 2024)","owner":"Syndicate","status":"draft","updated":"2026-10-04",
         "file":"rules/70-encounter-budget-5e.json","companion":"rules/70-encounter-budget-5e.md",
         "consumer":"Encounter Bot (tools/encounter_bot, local script, no model calls) cites this file for difficulty, credits and loot; it is the only source of those numbers",
         "decided_by":"Caleb: 'Go ahead and write the budget file.' (2026-10-04); clock numbers from decision 026",
         "players_are":"Crawlers"},
 "authority_note":"Budgets are guidelines, not enforced. The GM has authority to adapt as play goes (Caleb, 2026-10-04). Anything under 'authoritative' follows a filed source; anything under 'assumed' or tagged ASSUMED is a proposal for Caleb/GM to adjust.",
 "schema_description":{
   "top_level":{"schema":"schema id","version":"semver of this file","meta":"owner/status/consumer","authority_note":"guideline-only rule","schema_description":"this block",
                "authoritative":"numbers copied or derived from filed sources (SRD tables, core, decision 026)","assumed":"parameters this file proposes (each id A1..A13)",
                "party_sizes":"2, 3, 4 supported; other sizes: multiply per-character budgets by P","floors":"Floors 1-6 in full, keyed by floor number as a string",
                "floors_7_18":"formula and placeholders","economy_audit":"F1+F2 per-Crawler arithmetic against the 1,500 line","adjacency":"safe-room placement fields: per floor in floors.N.adjacency, rationale in assumed.adjacency","adjustments":"pets, companions, class features",
                "day01_slot_map":"the 34 empty slots in floors/f01/day-01.spec.json and the field that fills each","open_questions":"short list for Caleb"},
   "naming_scheme":{"ids":"lowercase keys; party size keys are the strings '2','3','4'; tiers are trivial|standard|hard|boss; levels are 'L<n>'; CRs are strings ('1/8','1/4','1/2','1','2')",
                     "units":"XP for budgets, credits for money (1 credit = 1 GP), hours/days for time",
                     "tags":"ASSUMED = proposal; 'authoritative' = follows a source; 'derived' = computed from both",
                     "citing":"cite as rules/70-encounter-budget-5e.json#<dotted.path>, e.g. floors.1.fixed_encounters.z07.counts_by_party_size.4.goblin-warrior",
                     "slot_map":"slot_no follows the order of the 'slots' array in floors/f01/day-01.json (34 entries); spec_path is the JSON path inside day-01.spec.json; fills_from is the dotted path here; value or value_by_party_size is the ready-to-paste fill"}},
 "tiers":{"names":["trivial","standard","hard","boss"],
          "meaning":{"trivial":"burns a little resource; wandering or filler","standard":"the everyday fight","hard":"an elite; avoidable or telegraphed above Moderate","boss":"the floor boss with support; at the top of the High band"},
          "band_maps":{"F1":BAND_F1,"F2_plus":BAND_STD},"lead_share":LEAD_SHARE,"status":"band maps ASSUMED for F2+; F1 matches overview 9.2"},
 "authoritative":auth,
 "assumed":{"status":"ASSUMED: proposals the GM may adapt; Caleb can overrule any of them","list":assumed_list,"adjacency":adj_global,"cash_per_crawler_f1_scale":CASH,"r1_toast_credits":R1,"r1_expected_count":{"1":2,"2":3,"3_plus":3},"deed_bronze_expected_per_crawler":{"1":0.5,"2":0.9}},
 "party_sizes":{"supported":[2,3,4],"note":"Encounter counts per floor do not change with party size; enemy counts and XP budgets do. Credits per Crawler stay flat; the encounter cash pool is per-Crawler x P (it scales and then splits evenly); boxes are per Crawler."},
 "floors":floors,
 "floors_7_18":formula,
 "economy_audit":econ,
 "adjustments":{"pets":"GM-run, do not count toward party size, take no XP, loot or credits (rules/60). No budget rebuild; if a fight is close the GM may add one CR 1/4 creature (50 XP) to the enemy side or leave it. A pet-Crawler counts as a full Crawler.",
                "assigned_companion":"2-Crawler tables (core 2.4): DM-run, CR <= half party level, takes no loot, does not count toward P; the F1 numbers already lean on the higher end for two Crawlers.",
                "class_features":"No separate adjustment for Second Wind or similar; the 2024 budgets already assume class resources.",
                "pvp":"No PvP anywhere. Nothing here pays XP, credits or boxes for attacking another Crawler."},
 "srd_pick_guidance":{"how":"Pick any SRD 5.2.1 creature whose CR is at or under the tier's cr_cap, reskin it (core 8.1), and fill the rest of the tier budget with copies or lower-CR support using the XP by CR table. Do not copy stat blocks into floor files.",
                      "fragile_rule":"SRD: more than two creatures per Crawler -> include fragile ones that fall quickly (most important at levels 1-2).",
                      "powerful_creature_rule":"SRD: a creature with CR above party level can drop a Crawler in one hit; telegraph it.",
                      "xp_award":"Achievements never grant XP (core 3.4). Levels come from milestones (core 2.3); the XP figures here only size fights."},
 "open_questions":[
   "Q1 (Caleb/Accountant): Is the 1,500 line F1+F2 combined per Crawler (used here, the stricter reading) or per floor as rules/40 3.2 words it? Combined, the two Silver Boss Boxes alone average about 859 credits.",
   "Q1b (Caleb): Detour Tax is one price (75 per Crawler) for a missed key and for a Floor 1 missed collapse; make the missed-collapse toll larger?",
   "Q2 (Caleb): Floor 3 = 15 or 20 days, and day counts for F4-F6 (placeholders 20/25/30).",
   "Q3 (Caleb): Keep the overview's Z8 counts for 2-3 Crawlers (over the hard-tier budget by 50 and 25 XP) or tighten them?",
   "Q4 (Accountant): Set an audit line for F3+; income at Floor-1 scale is about 600-700 credits per Crawler per floor against crafting prices of 5,000 / 12,000 / 30,000."]}

# re-key for readability: move prices into floors.1 only (already)
SPEC_SHA=hashlib.sha256(open(ROOT+"/floors/f01/day-01.spec.json","rb").read()).hexdigest()
doc["day01_slot_map"]={"source_spec":"floors/f01/day-01.spec.json (schema encounter-bot-day-spec/0.1); order = the 'slots' array of floors/f01/day-01.json","spec_sha256_when_mapped":SPEC_SHA,
  "spec_note":"The Encounter Bot regenerated the Day 1 spec at 9:47 PM CT while this file was being written. The map below is for the regenerated spec (34 slots, labels DETOUR TAX x4, REST-WITHOUT-SAFEROOM COST x3, REWARD x2, CR x7, BUDGET x5, COUNT x5, LOOT AMOUNT x6, CREDITS x1, plus none else). Five slots of the earlier version (zone groups, collapse order, stairwell opens, early-descent rule, detour cost) are now answered in the spec itself from decision 026; their numbers stay in authoritative.clock. If the spec changes again, re-map by label using label_guide.",
  "count":34,"all_filled":True,"label_guide":{
    "BUDGET":"floors.1.fixed_encounters.<zone>.fit (tier, XP budget, XP used) or floors.N.tiers.L<level>.xp_budget_total.<P>.<tier>",
    "CR":"creature CR in floors.1.fixed_encounters.<zone>.creatures; tier ceiling in floors.N.tiers.L<level>.cr_caps.<P>.<tier>; non-combat = none",
    "COUNT":"floors.1.fixed_encounters.<zone>.counts_by_party_size.<P>.<srd_id>",
    "CREDITS (key price)":"floors.1.prices.stairwell_key_terminal_bribe.party_price_by_size",
    "CREDITS (vendor price)":"floors.1.prices.potion_of_healing_vendor.price",
    "DETOUR TAX":"floors.1.prices.detour_tax.party_toll_by_size (or toll_per_crawler)",
    "REST-WITHOUT-SAFEROOM COST":"floors.1.prices.rest_without_saferoom",
    "LOOT AMOUNT":"cash: floors.N.credits; boxes: floors.N.boxes and economy_audit; boss cache: floors.1.fixed_encounters.z10.cash_per_crawler (overview 2d6 x 10 is written for 4 Crawlers, scale by P/4)",
    "REWARD":"floors.1.achievement_rewards.proposed.<name>"},
  "days_2_to_5":"The Day 2 to 5 specs use the same labels; I did not map their slots one by one. The label_guide fields cover them, and Day 3/5 counts come from the same fixed_encounters or the tier tables.",
  "slots":SL}
def dumps(o, lvl=0):
    ind = "  "
    if isinstance(o,(dict,list)):
        compact = json.dumps(o, ensure_ascii=False, separators=(", ", ": "))
        if len(compact) <= 110 and not (isinstance(o,dict) and any(isinstance(v,(dict,list)) and len(json.dumps(v))>60 for v in o.values())):
            return compact
        if isinstance(o,dict):
            items = [ind*(lvl+1)+json.dumps(k,ensure_ascii=False)+": "+dumps(v,lvl+1) for k,v in o.items()]
            return "{\n"+",\n".join(items)+"\n"+ind*lvl+"}"
        items = [ind*(lvl+1)+dumps(v,lvl+1) for v in o]
        return "[\n"+",\n".join(items)+"\n"+ind*lvl+"]"
    return json.dumps(o,ensure_ascii=False)
open(OUT,"w").write(dumps(doc)+"\n")
print(open(OUT).read().count("\n"),"lines")
print(json.dumps(econ,indent=1)[:3500])
print(sim_ng,sim_g)
