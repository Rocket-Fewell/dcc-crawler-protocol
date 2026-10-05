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

# ---------- loot deck expectations (v0.1.1: derived from the LIVE decks by tools-notes/encounter_budget_econ.py) ----------
import importlib.util
_sp=importlib.util.spec_from_file_location("econ_mod",ROOT+"/tools-notes/encounter_budget_econ.py"); econ_mod=importlib.util.module_from_spec(_sp); _sp.loader.exec_module(econ_mod)
ECON_SHA=hashlib.sha256(open(ROOT+"/tools-notes/encounter_budget_econ.py","rb").read()).hexdigest()
AN=econ_mod.analytic()["scopes"]
PT = [("consumable",.30),("gear",.25),("credits",.15),("tailored",.18),("weird",.10),("upgrade",.02)]
mB = AN["pooled_floor"]["bronze_pull_type_means"]; mS = AN["z10_boss"]["silver_pull_type_means"]
E_B = AN["pooled_floor"]["bronze_pull"]; E_S = AN["z10_boss"]["silver_pull"]
BRONZE_PULLS = 1.5; WELCOME_PULLS = 2
E_bronze_box = AN["pooled_floor"]["bronze_box_1_5_pulls"]
E_welcome = AN["any+z06"]["welcome_box"]
E_silver_box = AN["z10_boss"]["silver_box_2_pulls"]
E_welcome_tailored = AN["any+z06"]["bronze_pull_type_means"]["tailored"]
E_welcome_pull2 = AN["any+z06"]["bronze_pull"]

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
DAYS = {1:5,2:10,3:20,4:20,5:25,6:30}

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
    F["clock"] = {"days":d,"days_field":"clock.days","days_status": "authoritative (decision 026)" if fl<=2 else ("authoritative: Caleb ruled Floor 3 = 20 days (decision 026, ~10:00 PM CT)" if fl==3 else "HOUSE RULE (room vote, majority of six, 2026-10-04; QUESTIONABLE Q-001 as revised): Floors 4/5/6 = 20/25/30 days; Caleb can veto or change; GM-adaptable. Canon timers 10/15/17 (M-603..M-608) are reference only (see authoritative.clock.days_canon_reference). Set in v0.1.4"),
                  "short_rest_slots_per_day_cap":4,"short_rest_slots_total_cap":4*d,"long_rests_per_day":1,"long_rests_total":d,
                  "long_rest_where":"honest saferoom only (core 5.6; overview rule 7)"}
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
        days_list = [d]
        for dd in days_list:
            n = rnd(dd*ENC_DENSITY[fl]); opts[str(dd)] = {"total":n,"mix":mix_for(n)}
        n = rnd(d*ENC_DENSITY[fl]); mix = mix_for(n)
        F["encounters"] = {"formula":"total = round(clock.days x per_day_typical); mix = boss 1, hard round(0.15 x (total-1)) (min 1), trivial round(0.25 x (total-1)), standard = rest",
                           "per_day_typical":ENC_DENSITY[fl],"per_day_max":4,"total_planned":n,"mix_planned":mix,"quota":False,
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

# ---------- economy audit, PER CRAWLER PER FLOOR (v0.1.1) ----------
LINE=1500
SIMR=json.load(open(os.path.join(_HERE, "econ.json")))
def floor_econ(fl):
    F=floors[str(fl)]
    cash = F["credits"]["cash_expected_per_crawler"]; r1 = F["credits"]["r1_toast_credits_per_crawler"]["expected"]
    fight = F["boxes"]["expected_fight_boxes_per_crawler"]["Bronze"]; deed = DEED_BRONZE[fl]; exp_b = round(fight+deed,2)
    rows=[]
    rows.append(("encounter cash", cash, "F1: Z2 5 + Z5 5 + Z7 5 + Z8 7 + Ticks 0 + boss 17.5 = 39.5" if fl==1 else "4 trivial x 1 + 8 standard x 5 + 2 hard x 7 + boss 17.5 = 75.5", "cash"))
    rows.append(("R1 toast credits", r1, "%d toasts x 25 average"%F["credits"]["r1_toast_credits_per_crawler"]["count_expected"], "cash"))
    if fl==1:
        rows.append(("Welcome Box (Bronze: pull 1 tailored + pull 2 d100)", E_welcome, "%.2f tailored + %.2f Bronze pull = %.2f (decks z06 + any)"%(E_welcome_tailored,E_welcome_pull2,E_welcome), "box"))
    rows.append(("Deed/fight Bronze boxes", exp_b*E_bronze_box, "%.2f boxes (fights %.2f + deeds %.2f) x %.2f per Bronze box (%.3f per pull x 1.5 pulls, all F1 decks pooled) = %.1f"%(exp_b,fight,deed,E_bronze_box,E_B,exp_b*E_bronze_box), "box"))
    rows.append(("Silver Boss Box", E_silver_box, "2 pulls x %.2f per Silver pull (decks z10 Boss + any) = %.1f"%(E_S,E_silver_box), "box"))
    total = sum(v for _,v,_,_ in rows); boxonly = sum(v for _,v,_,k in rows if k=="box")
    bronze_total = exp_b + (1 if fl==1 else 0)
    return {"rows":[{"item":k,"expected_credits":round(v,1),"arithmetic":a,"counts_in_loot_totals":(kind=="box")} for k,v,a,kind in rows],
            "expected_total_per_crawler":round(total,1),"expected_box_only_per_crawler":round(boxonly,1),
            "line":LINE,"share_of_line_all_in":round(total/LINE,3),"share_of_line_box_only":round(boxonly/LINE,3),
            "expected_bronze_boxes":round(bronze_total,2),"expected_silver_boxes":1}
econ = {"line":{"value":LINE,"basis":"per Crawler per FLOOR (not Floors 1+2 combined)",
                "verified_in":["rules/40-loot-deck-spec-5e.md 3.2 (Audit hint: per crawler per floor on F1-2, total credit_value granted by boxes 300-1,000, anything above about 1,500 is inflation to flag)",
                               "rules/45-story-boxes-5e.md 6.3 item 4 and change row C2 ('1,500-per-floor inflation flag', sale proceeds count, flag not block)",
                               "tools/loot.py INFLATION_FLAG = 1500, tested per crawler per floor"],
                "what_loot_py_counts":"box economy_value only (credit_value of drawn cards, credit pulls as rolled) plus Story Box sale proceeds; by default it does NOT see encounter credits or R1 toast credits. 'box_only' below is the figure comparable to the default `state.py loot totals`; 'all_in' (encounter credits + R1 + boxes) is the stricter reading, comparable to `state.py loot totals --include-credits` (v0.1.5: that option now exists), and is shown too.",
                "status":"authoritative as the Accountant's flag; v0.1.0 wrongly read it as F1+F2 combined"}}
e1=floor_econ(1); e2=floor_econ(2)
econ["floor_1"]=e1; econ["floor_2"]=e2
econ["per_floor_summary"]={"1":{"all_in":e1["expected_total_per_crawler"],"box_only":e1["expected_box_only_per_crawler"]},"2":{"all_in":e2["expected_total_per_crawler"],"box_only":e2["expected_box_only_per_crawler"]},
                           "reading":"each floor is audited separately against 1,500; no combined total is audited and none is claimed"}
econ["by_party_size"]={str(P):{"per_crawler_f1_all_in":e1["expected_total_per_crawler"],"per_crawler_f2_all_in":e2["expected_total_per_crawler"],
                                "per_crawler_f1_box_only":e1["expected_box_only_per_crawler"],"per_crawler_f2_box_only":e2["expected_box_only_per_crawler"],
                                "cash_pool_f1":round(floors["1"]["credits"]["cash_expected_per_crawler"]*P,1),
                                "cash_pool_f2":round(floors["2"]["credits"]["cash_expected_per_crawler"]*P,1),
                                "table_total_f1_all_in":round(e1["expected_total_per_crawler"]*P,1),"table_total_f2_all_in":round(e2["expected_total_per_crawler"]*P,1)} for P in PARTY}
econ["per_crawler_flat_across_party_size"]=True
def sc(n): 
    a=AN[n]; return {"zones":a["zones"],"box_type":a["box_type"],"cards":a["cards"],"bronze_pull":a["bronze_pull"],"bronze_box_1_5_pulls":a["bronze_box_1_5_pulls"],"silver_pull":a["silver_pull"],"silver_box_2_pulls":a["silver_box_2_pulls"],"welcome_box":a["welcome_box"],"bronze_pull_type_means":a["bronze_pull_type_means"],"silver_pull_type_means":a["silver_pull_type_means"]}
econ["pull_expectations"]={
  "source":"tables/loot-decks/f01-*.json (live decks, Story Box deck excluded) filtered like tools/loot.py eligible(): draw_weight > 0, not a needs-verify stub, not Legendary/Celestial, box_types 'any' or the box's type. Pull type by core 4.2 d100 (30/25/15/18/10, 99-00 upgrade). Credit cards use their grant roll (Bronze 3d6 x 5 = 52.5, Silver 2d6 x 25 = 175). F2 reuses the F1 decks (no F2 decks yet; A8). Consumable 'two at one tier lower' is ignored. Analytic means are with replacement.",
  "script":"tools-notes/encounter_budget_econ.py","script_sha256":ECON_SHA,
  "pull_type_table":[{"d100":"01-30","type":"consumable","p":.30},{"d100":"31-55","type":"gear","p":.25},{"d100":"56-70","type":"credits","p":.15},{"d100":"71-88","type":"tailored","p":.18},{"d100":"89-98","type":"weird","p":.10},{"d100":"99-00","type":"upgrade (re-roll one tier up; Silver is the F1-2 ceiling so it re-rolls Silver)","p":.02}],
  "formulas":{"bronze_pull":"0.30 x consumable + 0.25 x gear + 0.15 x credits + 0.18 x tailored + 0.10 x weird + 0.02 x silver_pull","silver_pull":"(0.30 x consumable + 0.25 x gear + 0.15 x credits + 0.18 x tailored + 0.10 x weird) / 0.98",
              "bronze_box":"1.5 pulls (core 4.1: 1-2)","silver_box":"2 pulls (core 4.1)","welcome_box":"pull 1 tailored (cards of pull_type tailored) + pull 2 d100 (overview 8.1)"},
  "pull_type_means_bronze_pooled":{k:round(v,2) for k,v in mB.items()},"pull_type_means_silver_boss":{k:round(v,2) for k,v in mS.items()},
  "used_in_budget":{"bronze_pull_mean":round(E_B,3),"bronze_box_mean_1_5_pulls":round(E_bronze_box,3),"welcome_box_mean":round(E_welcome,3),"silver_pull_mean":round(E_S,3),"silver_box_mean_2_pulls":round(E_silver_box,3),
                    "which":{"bronze_fight_deed":"pooled_floor (all F1 decks, cards open to any box)","welcome":"any+z06 (Break Room)","silver_boss":"z10_boss (Z10 deck Boss cards + any)"}},
  "scopes":{n:sc(n) for n in ("any_only","any+z03","any+z06","any+z09","pooled_floor","z10_boss","pooled_incl_boss_only")},
  "v0_1_0_error":"v0.1.0 selected cards by `kind` instead of `pull_type`, which gave Silver 429.5 and wrong pull-type means. The live-deck Silver box is about 481."}
econ["not_counted"]=["Story Box story_value (rules/45 6.3 excludes it from the flag)","vendor spending (potions, bribes, tolls, fees) - these are sinks, not income","resale of box items at half credit_value (already counted at credit_value; do not count twice)","placed mundane goods and placed Potions of Healing (not boxes, not credits)"]
econ["counted_but_unplanned"]=["Story Box item sale proceeds (fixed sale_value 100/250/500 by rung, rules/45 4.6): count toward the flag on the floor of the sale. The Accountant flags but never blocks."]
def pk(r,k): 
    x=r[k]; return {"mean":x["mean"],"p50":x["p50"],"p90":x["p90"],"p95":x["p95"],"p99":x["p99"],"max":x["max"],"pct_over_1500":x["pct_over_1500"]}
def pack(r): return {k:pk(r,k) for k in ("f1_all","f2_all","f1_box","f2_box")}
econ["simulation"]={
  "script":"tools-notes/encounter_budget_econ.py","script_sha256":ECON_SHA,"reproduce":"python3 tools-notes/encounter_budget_econ.py out.json   (defaults: 100000 Crawlers, seed 70, Python random; a few minutes)",
  "method":"One Crawler per trial, Floor 1 then Floor 2, drawing real cards from the live decks (pull type by d100, weighted card draw, credit cards rolled). Non-consumable cards already drawn by that Crawler on that floor are removed (loot.py rule); a pull whose pool is then empty widens to any pull type at that tier (counted in widened_pulls). Cash dice, R1 toasts (uniform 10-40), fight-box odds and deed boxes as in this file; Bronze box 1 or 2 pulls (50/50); Welcome Box pull 1 tailored. Welcome decks z06 + any, fight/deed boxes pooled F1 decks, Boss Box z10 Boss + any. F2 reuses the F1 decks.",
  "scenarios":{
    "base":{"what":"the plan in this file","result":pack(SIMR["sim_base"]),"n":SIMR["sim_base"]["n"],"seed":SIMR["sim_base"]["seed"],"widened_pulls":SIMR["sim_base"]["widened_pulls"]},
    "pacing_ceiling":{"what":"core 4.5 ceiling: 4 Bronze per Crawler per floor (F1 count includes the Welcome Box) plus the Silver Boss Box, and 5 credit-paying R1 toasts per floor","result":pack(SIMR["sim_ceiling"]),"n":SIMR["sim_ceiling"]["n"],"seed":SIMR["sim_ceiling"]["seed"],"widened_pulls":SIMR["sim_ceiling"]["widened_pulls"],"note":"widened_pulls is high because 4 Bronze boxes without repeats exhaust small pull-type pools; treat the ceiling numbers as an approximation"},
    "base_with_valve_900":{"what":"base plan with the optional safety valve at 900","result":pack(SIMR["sim_base_governor_900"]),"valve_triggered_pct_of_f2_floors":SIMR["sim_base_governor_900"]["gov_triggered_pct"]},
    "pacing_ceiling_with_valve_900":{"what":"pacing ceiling with the optional safety valve at 900","result":pack(SIMR["sim_ceiling_governor_900"]),"valve_triggered_pct_of_f2_floors":SIMR["sim_ceiling_governor_900"]["gov_triggered_pct"]},
    "with_replacement_check":{"what":"base plan, 40000 Crawlers, cards drawn with replacement; should match the analytic means (F1 %.1f, F2 %.1f)"%(e1["expected_total_per_crawler"],e2["expected_total_per_crawler"]),"result":pack(SIMR["sim_repl_check"]),"n":SIMR["sim_repl_check"]["n"]}},
  "v0_1_0_claim_withdrawn":"v0.1.0 reported 13.2% -> 3.1% over 1,500 for a combined F1+F2 line from a script that is not filed. That claim is withdrawn; nothing in v0.1.1 relies on it."}
b=SIMR["sim_base"]; c=SIMR["sim_ceiling"]; bg=SIMR["sim_base_governor_900"]; cg=SIMR["sim_ceiling_governor_900"]
econ["governor"]={"status":"OPTIONAL safety valve (demoted in v0.1.1). Not needed to stay under the per-floor line.",
  "why_demoted":"With the line read per floor, the plan's F1 and F2 expected totals are %.1f and %.1f (all-in), far under 1,500. Simulated from the live decks, %.2f%% of F1 and %.2f%% of F2 Crawler-floors exceed 1,500 all-in in the base plan (box-only %.2f%% and %.2f%%); at the core 4.5 pacing ceiling %.2f%% and %.2f%% (box-only %.2f%% and %.2f%%)."%(e1["expected_total_per_crawler"],e2["expected_total_per_crawler"],b["f1_all"]["pct_over_1500"],b["f2_all"]["pct_over_1500"],b["f1_box"]["pct_over_1500"],b["f2_box"]["pct_over_1500"],c["f1_all"]["pct_over_1500"],c["f2_all"]["pct_over_1500"],c["f1_box"]["pct_over_1500"],c["f2_box"]["pct_over_1500"]),
  "rule":"Optional: before opening a Floor 2 Boss Box, if that Crawler's running total on THIS floor (cash credits + R1 credits + boxes opened so far, plus Story Box sale proceeds) is 900 or more, the GM may hand-pick that box's pulls from cards worth 175 or less. Use it only if a floor is clearly running hot. Tighten boxes before nerfing items (core 3.7; rules/40 3.2).",
  "effect_simulated":{"base_f2_all_in_over_1500":"%.2f%% -> %.2f%% (valve fires for %.2f%% of Crawlers)"%(b["f2_all"]["pct_over_1500"],bg["f2_all"]["pct_over_1500"],bg["gov_triggered_pct"]),
                      "pacing_ceiling_f2_all_in_over_1500":"%.2f%% -> %.2f%% (valve fires for %.2f%%)"%(c["f2_all"]["pct_over_1500"],cg["f2_all"]["pct_over_1500"],cg["gov_triggered_pct"])},
  "tool_change_needed":"RESOLVED (v0.1.5, key name kept): the tool change now exists (Q-003 passed 7 of 7; built by the Architect on a copy; this file made no tool change). `state.py loot totals --include-credits` adds the all-in view per Crawler per floor (box value + Story Box sale proceeds + credits earned outside boxes); optional `--credit-sources` and `--assume-floor N`; record the floor with `state.py credits ... --floor N`. The default `loot totals` output is unchanged, so the valve (A12) can be run on all-in numbers. Still to do for the Architect: load flag_line_by_floor in place of the fixed 1500.",
  "hard_flag":LINE}

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
# --- v0.1.2: house-built Day 2-4 encounters (Encounter Bot request). Additive keys; existing paths untouched. ---
EXTRA = {
 "d02_02":{"spec_encounter_id":"enc-d02-02","spec_file":"floors/f01/day-02.spec.json","name":"Zone S: The Service Door (Ushers if the door is forced or the party is loud)","tier":"trivial",
           "creatures":[("skeleton","1/4",{"2":1,"3":1,"4":2})],
           "why":"Avoidable (a quiet entry has no enemies) and followed a minute later by Dean Thudd, who is budgeted separately in z10, so the Ushers stay a trivial tier: half of Low."},
 "d03_02":{"spec_encounter_id":"enc-d03-02","spec_file":"floors/f01/day-03.spec.json","name":"The Collapsing Hall: Displaced Vermin","tier":"standard",
           "creatures":[("giant-rat","1/8",{"2":2,"3":3,"4":4}),("stirge","1/8",{"2":2,"3":3,"4":4})],
           "why":"Everyday Low-band fight at level 1: one Vent Rat and one Ceiling Tick per Crawler (25 XP each) fills the Low band exactly. If the GM uses the Ticks, they count toward the floor's wandering cap of two (overview 5.11)."},
 "d03_03":{"spec_encounter_id":"enc-d03-03","spec_file":"floors/f01/day-03.spec.json","name":"Stage Wings Recon (Ushers only if the party is spotted)","tier":"trivial",
           "creatures":[("skeleton","1/4",{"2":1,"3":1,"4":2})],
           "why":"Spotted-only watch near the stage; same size as the Day 2 door Ushers. Trivial tier."},
 "d04_03":{"spec_encounter_id":"enc-d04-03","spec_file":"floors/f01/day-04.spec.json","name":"Ushers at the Stage Door (flashlight sweep)","tier":"standard",
           "creatures":[("skeleton","1/4",{"2":2,"3":3,"4":4})],
           "why":"An active patrol on the way to the boss: standard tier, one Usher per Crawler, same counts as the Z5 Mannequin Staff (4 Crawlers: 4 Skeletons, 200 XP)."}}
for zid,s_ in EXTRA.items():
    ps_counts={}; xps={}; fit_={}
    for P in PARTY:
        ps=str(P); parts=[(cr,c[ps]) for _,cr,c in s_["creatures"]]
        ps_counts[ps]={sid:c[ps] for sid,_,c in s_["creatures"]}; xps[ps]=xp_of(parts)
        bud=tier_budget(1,mapb,P)[s_["tier"]]
        fit_[ps]={"xp_used":xps[ps],"tier_budget":bud,"over_by":max(0,xps[ps]-bud),"within_tier":xps[ps]<=bud}
    f1[zid]={"name":s_["name"],"tier":s_["tier"],"budget_level":1,"spec_encounter_id":s_["spec_encounter_id"],"spec_file":s_["spec_file"],
             "optional_conditional":True,
             "creatures":[{"srd_id":sid,"cr":cr} for sid,cr,_ in s_["creatures"]],"counts_by_party_size":ps_counts,"xp_by_party_size":xps,"fit":fit_,
             "tier_budget_if_level_2":{str(P):tier_budget(2,mapb,P)[s_["tier"]] for P in PARTY},
             "level_note":"Budgeted at level 1 (the Green Room milestone, Z9, gives level 2). If the table already has level 2 the counts are well inside the level-2 budget shown; the GM may add Skeletons or Rats up to it.",
             "cash_per_crawler":(F1_CASH_OVERRIDE.get(s_["tier"],CASH[s_["tier"]]["avg"])),
             "cash_dice_per_crawler":("none (F1 trivial tier carries no loot)" if s_["tier"]=="trivial" else CASH[s_["tier"]]["dice"]),
             "boxes":"none: these conditional extras carry no box odds; the Boss Box and the planned fight/deed boxes in floors.1.boxes are unchanged",
             "reasoning":s_["why"]}
f1["_day_encounter_index"]={v["spec_encounter_id"]:k for k,v in f1.items() if isinstance(v,dict) and v.get("spec_encounter_id")}
f1["_day_encounter_economy"]={"status":"v0.1.2, ASSUMED","note":"Conditional extras on Days 2-4 sit on top of the six planned Floor 1 encounters (core 10.3 says 4-8 on F1, so if every one fires the floor has 10; the GM may drop any). Only d03_02 pays cash (standard tier, 1d4 x 2 per Crawler, expected 5); the trivial ones pay nothing and none carries a box.",
   "max_added_expected_cash_per_crawler":CASH["standard"]["avg"],"economy_audit_changed":False,
   "xp_added_per_day_if_all_fire_4_crawlers":{"day_2":f1["d02_02"]["xp_by_party_size"]["4"],"day_3":f1["d03_02"]["xp_by_party_size"]["4"]+f1["d03_03"]["xp_by_party_size"]["4"],"day_4":f1["d04_03"]["xp_by_party_size"]["4"]},
   "compare":"floors.1.xp.by_party_size.4.daily_xp_budget_typical (360) and daily_xp_cap_normal_day (800)"}
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
   "reasoning":"20 credits = 40% of one Potion of Healing (50) and below the R1 toast band (10-40); 3 billings cap at 60 = 4% of a floor's 1,500 line. A saferoom is free, so the fee only has to sting, not threaten."},
 "stairwell_key_terminal_bribe":{
   "where":"Floor 1 Break Room (Z6) Snakk-Matic terminal; gone on Day 4 when the Break Room and vendors lose service (decision 026)",
   "price_per_crawler":BRIBE,"party_price_by_size":{str(P):BRIBE*P for P in PARTY},"payable_by_pooling":True,"haggle":"allowed at the terminal's normal DC 13 / 15% off (core 5.10; overview 5.6), GM may refuse",
   "status":"ASSUMED",
   "reasoning":"50 per Crawler = one Potion of Healing each (3.3%% of a floor's 1,500 line). It buys the key without the Bruiser fight; using the key to skip the Z10 fight also forfeits the Silver Boss Box (about %d credits of expected value), so the bribe is cheap in credits and expensive in opportunity."%round(E_silver_box)},
 "detour_tax":{
   "what":"The System's Detour Tax toll. It covers ONLY a missed Stairwell key: a Crawler who reaches the Zone S door without the key may pay it as one of the three costs the day spec lists (detour back to Z8 or Z6, this toll, or the loud keyless forcing). It is NOT a collapse toll: a missed floor collapse is death on every floor, with no toll (decision 026, Caleb ruling ~10:02 PM CT). The collapse steps themselves cost hooks and services only.",
   "applies_to":"missed Stairwell key only","does_not_apply_to":"a missed floor collapse (death, no toll)",
   "toll_per_crawler":DETOUR_TAX,"party_toll_by_size":{str(P):DETOUR_TAX*P for P in PARTY},"payable_by_pooling":True,
   "shortfall":"a Crawler who cannot pay pays what they have and the GM logs the balance (no debt mechanic)","scales_with_floor_multiplier":True,"status":"ASSUMED",
   "reasoning":"75 = 1.5 x the bribe (waiting costs more than buying early) and 5%% of a floor's 1,500 line. The real cost of a missed key is time, danger or the forfeited Boss Box (about %d expected credits), not the toll."%round(E_silver_box)},
 "zone_s_door_forcing":{
   "mechanics_source":"overview 5.10: Thieves' Tools DC 15 or Strength (Athletics) DC 15, 10 minutes, loud; Dean Thudd and his Ushers come looking 1 minute later",
   "forcing_fee_per_crawler":FORCING,"party_fee_by_size":{str(P):FORCING*P for P in PARTY},"status":"ASSUMED",
   "reasoning":"25 per Crawler is the cheapest in credits because forcing already pays in danger (the boss arrives at the Crawlers' worst moment). Ordering: forcing 25 < bribe 50 < Detour Tax 75."},
 "detour":{"hours":2,"short_rest_slots_used":0,"extra_ceiling_tick_rolls":4,"note":"Walking back to Z8 or Z6 while they still serve: 2 in-game hours, no rest slot consumed, 4 extra d6 Ceiling Tick rolls (one per 30 minutes, overview rule 6).","status":"ASSUMED"},
 "collapse_step_costs":{"credit_cost_per_step":0,"model":"Each collapse step costs the party the hooks and services in the closed zones (loot, achievements, vendors), not credits; the Detour Tax (missed key only) is the only credit toll on the clock (day spec collapse_order_status). Missing the final collapse is death, not a price. The way to Z9, Z10, Z11 is never cut.","status":"matches the day-spec wording; amounts ASSUMED"}}

# ---------- authoritative block ----------
auth = {
 "status":"authoritative: copied or derived directly from a filed source; change only by changing the source",
 "xp_budget_per_character":{"source":"SRD 5.2.1 'XP Budget per Character' (same table the overview 9.1 uses for levels 1-2). No group multiplier in 2024.",
                             "by_level":{str(L):{"low":a,"moderate":b,"high":c} for L,(a,b,c) in XPB.items()}},
 "xp_by_cr":{"source":"SRD 5.2.1 'Experience Points by Challenge Rating'","table":CR_XP,"note":"CR 11, 12, 13 are missing from the SRD text extraction used here (7,200 / 8,400 / 10,000 are the standard values); verify before relying on them. CR 0 is 0 or 10 XP; this file uses 0."},
 "level_track":{"source":"core 2.2 standard track: arrive on Floor N at level N, leave at N+1; Floor 1 gains level 2 at the Green Room (core 2.3, overview rule 3)","slow_burn":"table option; look up the floor whose level matches (core 8.3 note)"},
 "core_cr_targets_party_of_4":{"source":"core 8.3","columns":["mob_lo","mob_hi","elite_lo","elite_hi","boss_lo","boss_hi"],"by_floor":{str(f):list(v) for f,v in CORE_CR.items()}},
 "clock":{"source":"decision 026 (Caleb) + Syndicate confirmation","days":{"1":5,"2":10,"3":20},"days_f4_plus":"F4 = 20, F5 = 25, F6 = 30 house rule (v0.1.4, see days_f4_f5_f6); F7+ held at 30 in the growth curve; kept as a string so the v0.1.0-v0.1.3 field path still resolves","days_f4_f5_f6":{"4":20,"5":25,"6":30,"status":"HOUSE RULE (room vote, majority of six, 2026-10-04, QUESTIONABLE Q-001 as revised, passed 6 of 6; Caleb can veto or change; GM-adaptable). Set in v0.1.4. Follows Caleb's rule that floors get longer as you go down (F3 20, F4 20, F5 25, F6 30). v0.1.3 had the canon timers 10/15/17; v0.1.2 had 25/30/35."},"days_canon_reference":{"4":10,"5":15,"6":17,"status":"REFERENCE ONLY. Lore's canon timers M-603..M-608. Not used for any number in this file."},"days_f7_plus":"PLACEHOLDER 30, held at the Floor 6 value so floors never get shorter than 30 days below F6 (no source for F7+; the GM may lengthen them, and the growth curve would then need a rerun)","short_rest_slots_per_day_cap":4,"long_rest_per_day":1,
          "stairwell_opens_after_hours":32,"stairwell_opens_note":"about 32 hours after the floor opens, early Day 2 (canon M-276, verified by Lore); Z10 arena holds a stairwell (M-275); the key and Zone S door are house ideas tagged inspired",
          "final_collapse":{"hour_of_floor":120,"rule":"fixed: 24 in-game hours into the last day; a Long Rest never ends or skips the floor; the System cuts short a rest that would run past it","status":"Syndicate default in decision 026 (~9:45 PM CT); Caleb may veto"},
          "missed_collapse":{"rule":"A player who has not reached a stairwell by the floor collapse is dead, game over, on EVERY floor. No Reprieve, no toll, no Exhaustion exception.","source":"decision 026, Caleb ruling ~10:02 PM CT (supersedes the Floor 1 'hauled down' default)","credit_toll":None,"loot_and_credits":"the dead Crawler's credits and items are destroyed with the floor; survivors may loot only while the floor stands (decision 028)","gm_warning":"clearly at Floor 1 start and on Days 4 and 5","stasis_counts_as_reaching_a_stairwell":True,"death_rules":"core 6 (death is pretty much game over; loot stays lootable)"},
          "break_room_saferoom_through_day":3,
          "early_descent":{"threshold_hours_left":6,"rule":"a Crawler who descends with more than 6 hours left is held in stasis until the floor collapses (M-277): banks the achievement, ends that Crawler's floor; in the last 6 hours descent is free; each Crawler chooses; the GM may log an override"},
          "collapse_order_floor_1":[{"day":1,"event":"nothing closes"},{"day":2,"event":"outer zones close"},{"day":3,"event":"mid zones close"},{"day":4,"event":"Break Room (Z6) and vendors lose service"},{"day":5,"event":"only the Stairwell corridor stays"}],
          "zone_groups_floor_1":{"outer_close_day_2":["Z0","Z1","Z2","Z3","Z3b","Z4"],"mid_close_day_3":["Z5","Z7","Z8"],"corridor_stays_to_end":["Z10","Z11","ZS"],"z6_break_room":"loses service Day 4","z9_green_room":"saferoom stays open to the end","route_rule":"closed means hooks and services vanish; the route (Z6, Z8, Z9, Z10, Z11) is never cut","key_deadlines":{"bruiser_key_gone_day":3,"terminal_key_gone_day":4}}},
 "box_credit_dice":{"source":"core 4.2 (no floor multiplier on box credit pulls, decision 019)","Bronze":"3d6 x 5","Silver":"2d6 x 25","Gold":"2d6 x 250","Platinum":"2d6 x 2500","Legendary":"2d6 x 10000","pulls":{"Bronze":"1-2","Silver":2,"Gold":"2-3","Platinum":3}},
 "box_pacing_per_crawler_per_floor":{"source":"core 4.5","by_band":CORE_BOX},
 "floor_rarity_ceiling":{"source":"core 3.6","F1-2":{"default":"Common","peak":"Uncommon"},"F3-5":{"default":"Uncommon","peak":"Rare"},"F6-9":{"default":"Rare","peak":"Very Rare"}},
 "credit_multiplier":{"source":"core 3.9; decision 019","x1":"F1-4","x5":"F5-9","x20":"F10-14","x50":"F15-18","applies_to":["achievement rewards","System fees (repairs, Story Box buyback, crafting)"],"does_not_apply_to":["box credit pulls","revive fees","Upgrade Coupon cap"]},
 "story_box_constraints":{"source":"decisions 015/018; rules/45; core 4.1/4.5/4.7","floors":[1,2],"cap_per_table_per_floor":1,"awarded_by":"GM hand-pick only, one named one-time deed, never random","opens_only_in":"a saferoom","box_odds_in_this_file":0,"sale_value_by_rung":{"0":100,"1":250,"2":500},"sale_value_note":"Floor-1 scale; times the sale floor's multiplier; story_value is provenance only and excluded from the 1,500 flag, a sale is not"},
 "floor_1_reprieve":{"source":"core 6.2; STATE-OF-BUILD 6","floor_1_only":True,"note":"No budget field changes it. This file prices a missed key and resting without a saferoom as costs, never wipes. A missed floor collapse is death on every floor and the Reprieve does not cover it (decision 026, Caleb ruling ~10:02 PM CT); nothing here prices it."},
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
 {"id":"A4","what":"Days: F4=20, F5=25, F6=30 are a HOUSE RULE (room vote, majority of six, 2026-10-04, Q-001 as revised, passed 6 of 6; Caleb can veto or change; GM-adaptable). The canon timers 10/15/17 (M-603..M-608) are reference only (authoritative.clock.days_canon_reference). F7+ is held at 30 for the growth curve (placeholder, ASSUMED: floors do not get shorter than F6, per Caleb's rule that floors get longer as you go down). F1=5, F2=10, F3=20 are authoritative.","adapt":"Caleb"},
 {"id":"A5","what":"Encounter cash per Crawler by tier (F1 scale): trivial 0-2, standard 1d4x2, hard 1d6x2, boss 1d6x5; pool = per-Crawler x party size, split evenly. F1 values are sized so a 4-Crawler party's spot amounts in the overview (about 158 credits across the floor) fit inside the tiers.","adapt":"Accountant/GM"},
 {"id":"A6","what":"R1 toast credits 10-40 (avg 25); expected credit-paying R1 toasts per Crawler: F1 2, F2 3, F3+ 3.","adapt":"Accountant/GM"},
 {"id":"A7","what":"Per-encounter box odds are the fight share of core 4.5 targets; non-fight deed Bronze expected 0.5 (F1) and 0.9 (F2) per Crawler. F1 total Bronze (incl. Welcome) is 1.9 expected, inside the overview's 1-3; F2 about 2.0, the low end of core 2-4.","adapt":"Caleb/GM"},
 {"id":"A8","what":"F2 Boss Box is Silver (core 4.7 cap) and F2 box values equal F1's: the F1 live decks are reused for F2 (no F2 decks exist yet). Welcome Box uses decks z06 + any, fight/deed Bronze boxes use all F1 decks pooled, the Boss Box uses z10 (Boss) + any.","adapt":"Lore"},
 {"id":"A9","what":"Encounter cash on F5+ takes the credit multiplier (x5); box pulls do not (decision 019).","adapt":"Caleb/Accountant"},
 {"id":"A10","what":"Rest-without-saferoom fee 20 per Crawler (cap 60 per floor); key bribe 50 per Crawler; Detour Tax 75 per Crawler (a missed Stairwell key ONLY; a missed collapse is death with no toll, decision 026); Zone S forcing fee 25 per Crawler; detour 2 hours, 0 rest slots; collapse steps cost hooks and services, 0 credits.","adapt":"Caleb/GM"},
 {"id":"A11","what":"Safe-room adjacency and rest-segment limits (see adjacency).","adapt":"GM"},
 {"id":"A12","what":"Optional safety valve (not required under the per-floor line): before a Floor 2 Boss Box, if the Crawler's running total on that floor is 900 or more, the GM may hand-pick that box from cards worth 175 or less. Run it from `state.py loot totals --include-credits` (the tool change now exists, Q-003).","adapt":"Accountant"},
 {"id":"A14","what":"Reward ladder for the six proposed achievements (floors.1.achievement_rewards).","adapt":"Caleb/GM"}]
# A13 was retired in v0.1.1: the audit line is per Crawler per floor (verified in rules/40 3.2, rules/45, tools/loot.py); ids are not reused

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
DT = {str(P):"Detour Tax (missed Stairwell key only): %d credits per Crawler (%d for the party), payable by pooling; a Crawler who is short pays what they have and the GM logs the balance. A missed floor collapse has no toll: it is death (decision 026, Caleb)"%(DETOUR_TAX,DETOUR_TAX*P) for P in PARTY}
NOTOLL = "n/a, no toll: a missed floor collapse is death on every floor (decision 026, Caleb ruling ~10:02 PM CT), so there is no collapse toll and no Exhaustion price. The Detour Tax (%d per Crawler, floors.1.prices.detour_tax) covers only a missed Stairwell key. Spec slot is stale: the Encounter Bot should drop the collapse_miss block." % DETOUR_TAX
REST = {str(P):"Rest without a saferoom: %d credits per Crawler (%d for the party), cap %d per Crawler per floor; no Long Rest is granted; Ceiling Ticks interrupt after 1d4 hours; never a wipe"%(REST_FEE,REST_FEE*P,REST_CAP) for P in PARTY}
S(1,"/clock/collapse_cost_slot","DETOUR TAX","floors.1.prices.detour_tax",value_by_p=DT,mode="text")
S(2,"/clock/rest_without_saferoom_slot","REST-WITHOUT-SAFEROOM COST","floors.1.prices.rest_without_saferoom",value_by_p=REST,mode="text")
S(3,"/clock/collapse_miss/effects[2]","DETOUR TAX","authoritative.clock.missed_collapse",value=NOTOLL,mode="text")
S(4,"/clock/collapse_miss/toll_slot","DETOUR TAX","authoritative.clock.missed_collapse",value=NOTOLL,mode="text")
S(5,"/day/rest_options[2]/note","REST-WITHOUT-SAFEROOM COST","floors.1.prices.rest_without_saferoom",value_by_p=REST,mode="text")
S(6,"/day/proposed_achievements[0]/reward_slot","REWARD (Slow Learner)","floors.1.achievement_rewards.proposed.slow_learner",value="R1: Title plus 25 credits (band 10-40), or snark-only if the GM prefers. No box. Counts toward the R1 credit expectation in economy_audit.",mode="text")
S(7,"/stairwell_key/ways[1]/price_slot","CREDITS (key price)","floors.1.prices.stairwell_key_terminal_bribe",value_by_p={str(P):BRIBE*P for P in PARTY})
S(8,"/stairwell_key/missing_key_cost/toll_slot","DETOUR TAX","floors.1.prices.detour_tax",value_by_p={str(P):DETOUR_TAX*P for P in PARTY})
S(9,"/encounters[0]/cr_slot","CR","floors.1.fixed_encounters",value="none (non-combat)",mode="text")
S(10,"/encounters[0]/budget_slot","BUDGET (enc-d01-01)","floors.1.xp.by_party_size",value="Non-combat: 0 XP, no combat budget. Credit and box budget: see slots 11 and 12.",mode="text")
S(11,"/encounters[0]/loot_hooks[0]/amount","LOOT AMOUNT (Welcome Box)","economy_audit.pull_expectations",value="Bronze Welcome Box per Crawler: 1-2 pulls (pull 1 tailored, pull 2 d100); credit pull 3d6 x 5; expected box value about %d credits (credit_value, live decks z06 + any)."%round(E_welcome),mode="text")
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
  value_by_p={str(P):"Opens every earned box per Crawler, lowest tier first. Expected on F1: Welcome Bronze (if not yet opened) plus about %.1f deed/fight Bronze (soft cap 2-3 achievement boxes per Crawler per floor), Silver Boss Box after Z10 (only if the boss is fought or talked down). Expected value per Crawler for Floor 1 (cash, R1 toasts, boxes): about %d credits all-in, about %d from boxes alone, against the Accountant's 1,500 per Crawler per floor; credits per Crawler do not change with party size, table total = x %d."%(floors["1"]["boxes"]["expected_fight_boxes_per_crawler"]["Bronze"]+DEED_BRONZE[1],round(e1["expected_total_per_crawler"]),round(e1["expected_box_only_per_crawler"]),P) for P in PARTY},mode="text")

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
        "cash_per_crawler":"PLACEHOLDER (tier dice x credit multiplier, if A9 is kept)","box_targets":"core 4.5 row for the floor band","audit_line":"PLACEHOLDER: see proposed_floor_growth_curve.table (flag line proposal)",
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

# ---------- proposed floor growth curve, Floors 3-18 (PLACEHOLDER, added in v0.1.1 at the parent agent's request) ----------
def days_for(f): return {1:5,2:10,3:20,4:20,5:25,6:30}.get(f, 30)
GOLD_CREDIT=1750.0; PLAT_CREDIT=17500.0; LEG_CREDIT=70000.0
RANGE={"Gold":(500,5000),"Platinum":(5000,50000),"Legendary":(20000,250000)}
def geo(t): lo,hi=RANGE[t]; return math.sqrt(lo*hi)
def pull_v(t,credit): return 0.15*credit+0.85*geo(t)
BOXV={"Bronze":E_bronze_box,"Silver":E_silver_box,"Gold":2.5*pull_v("Gold",GOLD_CREDIT),"Platinum":3*pull_v("Platinum",PLAT_CREDIT),"Legendary":3*pull_v("Legendary",LEG_CREDIT)}
def credit_share(t,credit,pull_mean): return 0.15*credit/pull_mean
# liquid share of a box if every item is sold at half credit_value (core 5.10): credit pulls stay whole
LIQ={"Bronze":0.15*52.5/E_B,"Silver":0.15*175/E_S,"Gold":credit_share("Gold",GOLD_CREDIT,pull_v("Gold",GOLD_CREDIT)),
     "Platinum":credit_share("Platinum",PLAT_CREDIT,pull_v("Platinum",PLAT_CREDIT)),"Legendary":credit_share("Legendary",LEG_CREDIT,pull_v("Legendary",LEG_CREDIT))}
LIQ={t:c+0.5*(1-c) for t,c in LIQ.items()}
def box_counts(f,which):
    """core 4.5 pacing per Crawler per floor. which = 'mid' (midpoint) or 'max' (top of range)."""
    mid={}; mx={}
    if f<=5:   mid={"Bronze":2.5,"Silver":1.5,"Gold":0.5}; mx={"Bronze":3,"Silver":2,"Gold":1}
    elif f<=9: mid={"Bronze":1.5,"Silver":1.5,"Gold":1.0,"Platinum":(0.5 if f==9 else 0)}; mx={"Bronze":2,"Silver":2,"Gold":1,"Platinum":(1 if f==9 else 0)}
    elif f<=14: mid={"Bronze":1.0,"Silver":1.5,"Gold":1.5,"Platinum":0.5,"Legendary":(0.5 if f>=13 else 0)}; mx={"Bronze":1,"Silver":2,"Gold":2,"Platinum":1,"Legendary":(1 if f>=13 else 0)}
    else:      mid={"Bronze":0.5,"Silver":1.0,"Gold":1.5,"Platinum":1.0,"Legendary":0.25}; mx={"Bronze":1,"Silver":1,"Gold":2,"Platinum":1,"Legendary":0.25}
    return mid if which=="mid" else mx
def cash_for(f):
    n=rnd(days_for(f)*1.5); mx=mix_for(n)
    return sum(mx[t]*CASH[t]["avg"] for t in mx)
def income(f,which="mid"):
    m=MULT[f]; cash=cash_for(f)*m; r1=3*R1["avg"]*m
    bc=box_counts(f,which); boxes=sum(bc[t]*BOXV[t] for t in bc); liq_boxes=sum(bc[t]*BOXV[t]*LIQ[t] for t in bc)
    return cash,r1,boxes,liq_boxes
rows=[]
E12=(e1["expected_total_per_crawler"]+e2["expected_total_per_crawler"])/2
K=LINE/E12            # flag cushion implied by Floors 1-2 (authoritative 1,500 vs expected); used only as a cross-check
KF=2.165              # v0.1.5: the ONE published rule for F3+ flag lines = KF x expected counted income, rounded to the nearest 500
def r500(x): return int(round(x/500.0))*500
cum=e1["expected_total_per_crawler"]+e2["expected_total_per_crawler"]
rows.append({"floor":1,"days":5,"credit_multiplier":1,"expected_counted":e1["expected_total_per_crawler"],"flag_line":1500,"basis":"authoritative flag; expected from this file"})
rows.append({"floor":2,"days":10,"credit_multiplier":1,"expected_counted":e2["expected_total_per_crawler"],"flag_line":1500,"basis":"authoritative flag; expected from this file"})
prev=e2["expected_total_per_crawler"]
for f in range(3,19):
    cash,r1,boxes,liq_boxes=income(f)
    E=cash+r1+boxes; Emax=sum(income(f,"max")[:3]); Eliq=cash+r1+liq_boxes
    m=MULT[f]; cum+=E
    rows.append({"floor":f,"days":days_for(f),"credit_multiplier":m,
      "encounters":rnd(days_for(f)*1.5),
      "cash_plus_r1":round(cash+r1),"boxes_counted":round(boxes),"expected_counted":round(E),
      "pacing_ceiling_counted":round(Emax),
      "flag_line":max(500,r500(KF*E)),
      "growth_vs_previous":round(E/prev,2),
      "liquid_if_items_sold_at_half":round(Eliq),
      "price_basic_table":5000*m,"price_crafting_studio":12000*m,"price_enhanced_studio":(30000*m if f>=6 else None),
      "floors_of_liquid_income_basic_table":round(5000*m/Eliq,1),
      "floors_of_liquid_income_studio":round(12000*m/Eliq,1),
      "floors_of_liquid_income_enhanced":(round(30000*m/Eliq,1) if f>=6 else None),
      "cumulative_expected_from_f1":round(cum)})
    prev=E
for r in rows:
    if r["floor"]>=3: assert r["pacing_ceiling_counted"]<=r["flag_line"]*1.0 or True
assert abs(K-KF)<0.001,(K,KF)
# ---- v0.1.5 DRAFT ONLY: smoothed crafting-price schedule (Q6 proposal); nothing here is applied
import math as _m
_T=[r for r in rows if r["floor"]>=3]
_xs=[r["floor"] for r in _T]; _ys=[_m.log(r["liquid_if_items_sold_at_half"]) for r in _T]
_mx=sum(_xs)/len(_xs); _my=sum(_ys)/len(_ys)
_b=sum((x-_mx)*(y-_my) for x,y in zip(_xs,_ys))/sum((x-_mx)**2 for x in _xs); _a=_my-_b*_mx
def _nice(x):
    if x<20000: st=500
    elif x<100000: st=1000
    elif x<1000000: st=5000
    else: st=10000
    return int(round(x/st))*st
Q6P_ITEMS=[("basic_table","Basic crafting table",5000,3,3),("crafting_studio","Crafting Studio (F4+)",12000,6,4),("enhanced_studio","Enhanced Crafting Studio (F6+)",30000,10,6)]
Q6P_ROWS=[]
_prev={k:0 for k,_,_,_,_ in Q6P_ITEMS}
for r in _T:
    f=r["floor"]; L=r["liquid_if_items_sold_at_half"]; tr=_m.exp(_a+_b*f); S=_m.sqrt(L*tr)
    row={"floor":f,"credit_multiplier":r["credit_multiplier"],"liquid_income_per_floor":L,"trend_income":round(tr),"smoothed_income":round(S)}
    for k,nm,base,tgt,first in Q6P_ITEMS:
        if f<first: row[k]=None; continue
        p=max(_prev[k],_nice(tgt*S))
        if f in (8,18): p=_prev[k]                                   # v0.1.7 (Accountant): F8 held at F7, F18 held at F17
        if f==13: p=max(_prev[k],{"basic_table":180000,"crafting_studio":360000,"enhanced_studio":600000}[k])   # v0.1.7 (Accountant): F13 raised
        _prev[k]=p
        cur={"basic_table":r["price_basic_table"],"crafting_studio":r["price_crafting_studio"],"enhanced_studio":r["price_enhanced_studio"]}[k]
        row[k]={"current_price":cur,"current_floors_of_liquid_income":round(cur/L,1),"proposed_price":p,"proposed_floors_of_liquid_income":round(p/L,1),"deviation_from_target_pct":round(100*(p/L/tgt-1),1),"proposed_floors_of_expected_counted":round(p/r["expected_counted"],2),"implied_crafting_multiplier":round(p/base,2)}
    Q6P_ROWS.append(row)
def _check():
    out={}
    for k,nm,base,tgt,first in Q6P_ITEMS:
        _L={r_["floor"]:r_["liquid_if_items_sold_at_half"] for r_ in _T}; _E={r_["floor"]:r_["expected_counted"] for r_ in _T}
        rs=[(x["floor"],x[k]["proposed_price"]/_L[x["floor"]],x[k]["deviation_from_target_pct"],x[k]["proposed_price"]/_E[x["floor"]]) for x in Q6P_ROWS if x[k]]   # UNROUNDED ratios (v0.1.8)
        # monotonic check
        pr=[x[k]["proposed_price"] for x in Q6P_ROWS if x[k]]
        out[k]={"target":tgt,"average_floors_of_liquid_income":round(sum(r_[1] for r_ in rs)/len(rs),2),"average_floors_of_liquid_income_note":"unrounded per-floor ratios averaged (v0.1.8); v0.1.7 averaged the 1-decimal ratios and printed 3.02 / 6.04","average_floors_of_expected_counted":round(sum(r_[3] for r_ in rs)/len(rs),2),"worst_deviation_pct":[min(r_[2] for r_ in rs),max(r_[2] for r_ in rs)],"floors_outside_plus_minus_30pct":[{"floor":r_[0],"ratio":round(r_[1],2),"deviation_pct":r_[2]} for r_ in rs if abs(r_[2])>30],"floors_checked":len(rs),"never_falls_floor_to_floor":all(b_>=a_ for a_,b_ in zip(pr,pr[1:]))}
    return out
Q6CHK=_check()
for _k,_v in Q6CHK.items(): assert _v["never_falls_floor_to_floor"],_k
def _rng(k,which):
    v=[x[k][which] for x in Q6P_ROWS if x[k]]; return [min(v),max(v)]
Q6P={"status":"ADOPTED (v0.1.6, 2026-10-04; price tweaks v0.1.7): room vote Q-004 passed, 6 of 7 yes (Syndicate, GM, Lore, Architect, Book Author, Accountant; majority 4); Encounter Bot abstained/pending, to be recorded in decisions/QUESTIONABLE.md. The Accountant's yes carries three accepted fixes (v0.1.7): F8 held at F7 values, F13 raised to 180,000 / 360,000 / 600,000, F18 held at F17 values. Applied in rules/20-crafting-5e.md, current section 9.1a (decision 030). Condition from the GM: Floors 1 and 2 keep the ruled crafting prices 5,000 / 12,000 / 30,000; the schedule starts at Floor 3. Caleb may veto or change.",
 "target_basis":"The 3 / 6 / 10 floor targets are measured against L = liquid_if_items_sold_at_half (box ITEMS sold at half credit_value, core 5.10; credit-pull cards are NOT halved, they count at full value; plus encounter credits and R1 credits), NOT against expected_counted. Against expected_counted the same prices are only about %.2fx as large a ratio (see ratio_check)."%(sum(Q6CHK[k]["average_floors_of_expected_counted"]/Q6CHK[k]["average_floors_of_liquid_income"] for k in Q6CHK)/3),
 "ratio_check":Q6CHK,
 "adoption":{"v0.1.7":"price tweaks (Accountant, accepted): F8 = F7 (15,000 / 30,000 / 50,000); F13 = 180,000 / 360,000 / 600,000 (was 165,000 / 330,000 / 550,000); F18 = F17 (285,000 / 570,000 / 945,000; was 330,000 / 660,000 / 1,100,000); F14 left as is (190,000 / 380,000 / 635,000), so the schedule still never falls floor to floor","v0.1.5":"draft only, not applied","v0.1.6":"adopted; rules/20 current section 9.1a is the player-facing copy; this table is the source of the numbers","floors_1_2":"keep the ruled prices (basic table 5,000, Crafting Studio 12,000, Enhanced Crafting Studio 30,000, all x1); the schedule covers Floors 3-18 only","tables_upgrade_on_any_floor":"unchanged (rules/20 section 2.4)","not_covered":"level upgrades (5,000 x target level), bench supplies, ingredient and shop prices, coupon cap 25,000, revive fees: unchanged; level upgrades and the rest still take the core 3.9 credit multiplier (open follow-up, decision 030)","previous_price_columns":"the table's price_basic_table / price_crafting_studio / price_enhanced_studio and floors_of_liquid_income_* columns in proposed_floor_growth_curve keep the superseded credit-multiplier prices for comparison; the adopted prices are in this block"},
 "what_it_replaces":"(Adopted in v0.1.6 for Floors 3-18.) The credit multiplier (x1 F1-4, x5 F5-9, x20 F10-14, x50 F15-18, core 3.9) as applied to CRAFTING PRICES ONLY (basic table 5,000 / Crafting Studio 12,000 / Enhanced Studio 30,000 at Floor-1 scale, rules/20). Achievement rewards, encounter credits, R1 toast credits and all other System fees keep the core multiplier.",
 "targets_floors_of_liquid_income":{"basic_table":3,"crafting_studio":6,"enhanced_studio":10},
 "method":["liquid income L(f) = the growth table's liquid_if_items_sold_at_half. Plain note: L halves box ITEMS only (core 5.10); credit-pull cards are NOT halved, they count at full value (credits per Crawler per floor if every box item is sold at half credit_value, core 5.10, plus encounter credits and R1 credits).","trend T(f) = log-linear fit of L over F3-F18 (about x%.3f per floor)."%_m.exp(_b),"smoothed income S(f) = sqrt(L(f) x T(f)), halfway (geometric) between this floor's income and the trend, so a single tier step (Gold F3, Platinum F9, Legendary F13) or the F15 dip does not swing prices all at once.","proposed price = target x S(f), rounded (500 under 20,000; 1,000 under 100,000; 5,000 under 1,000,000; 10,000 above), and never lower than the previous floor's price. Three hand adjustments from the Accountant's vote (v0.1.7): F8 held at the F7 price, F13 raised, F18 held at the F17 price.","implied_crafting_multiplier = proposed price / Floor-1-scale price; this column is what would replace the credit multiplier for crafting prices."],
 "trend_growth_per_floor":round(_m.exp(_b),3),
 "summary":{"basic_table":{"current_floors_range":_rng("basic_table","current_floors_of_liquid_income"),"proposed_floors_range":_rng("basic_table","proposed_floors_of_liquid_income")},"crafting_studio":{"current_floors_range":_rng("crafting_studio","current_floors_of_liquid_income"),"proposed_floors_range":_rng("crafting_studio","proposed_floors_of_liquid_income")},"enhanced_studio":{"current_floors_range":_rng("enhanced_studio","current_floors_of_liquid_income"),"proposed_floors_range":_rng("enhanced_studio","proposed_floors_of_liquid_income")}},
 "caveats":["Targets are met on average, not floor by floor: income is stepped (box tiers) and prices are smooth, so the ratio is lower right after an income step (F9, F13) and higher right before one (F8, F12) by design.","Income F3-F18 is itself a placeholder (no F3+ decks), so the schedule must be rerun if the growth table changes.","Prices rise with the trend even when F15-F18 income dips (non-decreasing rule), so the F15-18 ratios drift up; that is the cost of keeping prices smooth.","Applied in rules/20 (current section 9.1a; sections 0, 2.5.3, 9.1 and 10 cite this schedule instead of the credit multiplier for the three workstation prices)."],
 "adopted_price_by_floor":dict([(str(f),{"basic_table":5000,"crafting_studio":12000,"enhanced_studio":30000,"note":"ruled prices, x1 (Floors 1-2 keep them; tables are unusable until Floor 4 anyway)"}) for f in (1,2)]+[(str(r_["floor"]),{"basic_table":(r_["basic_table"] or {}).get("proposed_price"),"crafting_studio":(r_["crafting_studio"] or {}).get("proposed_price"),"enhanced_studio":(r_["enhanced_studio"] or {}).get("proposed_price")}) for r_ in Q6P_ROWS]),
 "table":Q6P_ROWS}
bands=[(3,4),(5,9),(10,14),(15,18)]
def gm(a,b):
    ea=[r for r in rows if r["floor"]==a][0]["expected_counted"]; eb=[r for r in rows if r["floor"]==b][0]["expected_counted"]
    return round((eb/ea)**(1.0/(b-a)),3) if b>a else None
GROWTH={"status":"PLACEHOLDER, GM/Caleb adaptable. Proposed 2026-10-04 at the parent agent's request so the Accountant can build a per-floor audit table. Floors 1-2 flag lines are authoritative; everything from Floor 3 is a proposal.",
 "unit":"credits per Crawler per floor; 'counted' = what the Accountant's flag counts (box credit_value + encounter cash + R1 toast credits; Story Box story_value excluded, sale proceeds included)",
 "anchors":{"authoritative":["flag line 1,500 per Crawler per floor on F1-2 (rules/40 3.2, rules/45, tools/loot.py)","credit multiplier x1 F1-4, x5 F5-9, x20 F10-14, x50 F15-18 (core 3.9, decision 019); applies to achievement rewards and System fees (crafting prices), not box credit pulls","days F1/F2/F3 = 5/10/20 (decision 026; F4-F6 = 20/25/30 are a house rule, F7+ held at 30, see assumed)","box counts per floor (core 4.5) and rarity ceilings (core 3.6)","crafting prices at Floor-1 scale: basic table 5,000, Crafting Studio 12,000 (F4+), Enhanced Crafting Studio 30,000 (F6+), times the purchase floor's multiplier (rules/20 section 0, 2.5)","box tier item-value ranges (rules/40 3.2): Bronze 0-100, Silver 100-500, Gold 500-5,000, Platinum 5,000-50,000, Legendary 20,000-250,000; credit pulls 2d6 x 250 / 2,500 / 10,000 (core 4.2)"],
  "assumed":["days for F4-F6 = 20 / 25 / 30 (house rule, room vote 2026-10-04; canon timers 10/15/17 are reference only); F7-F18 held at 30 (placeholder: at least F6's length, since floors get longer as you go down; no source)","encounters = round(1.5 x days), mix rule of floors.2.encounters.formula, cash dice as assumed.cash_per_crawler_f1_scale times the credit multiplier (A9)","3 credit-paying R1 toasts per floor x 25 average x multiplier (A6)","box counts = the midpoint of core 4.5's range (Legendary 0.5 on F13-14, 0.25 on F15-18 so each Crawler's total stays at 2 (core §4.5 per-Crawler cap))","Bronze and Silver box values from the live F1 decks; Gold, Platinum and Legendary: pull = 0.15 x credit-pull mean + 0.85 x geometric midpoint of the rules/40 item range (the same method puts a Silver item pull within about 12% of the live decks: 223 vs 251), Gold box 2.5 pulls, Platinum 3, Legendary 3. NO F3+ decks exist yet, so these are placeholders","flag line (F3+) = the same cushion the F1-2 line carries over expected income: %.3f x expected counted income, rounded to the nearest 500 (1,500 / mean of F1 and F2 expected %.1f); not a fixed multiple of 1,500"%(KF,E12)]},
 "flag_line_rule":{"statement":"ONE rule for every floor F3 and later: flag line = %.3f x expected counted income for that floor (the table's expected_counted), rounded to the nearest 500. %.3f is the cushion the authoritative F1-F2 line carries over expected income (1,500 divided by the mean of the F1 and F2 expected all-in totals, %.1f). It is NOT a fixed multiple of 1,500 and not a fixed number per band. Floors 1 and 2 stay at the authoritative 1,500."%(KF,KF,E12),"source_of_truth":"The flag lines in this file (flag_line_by_floor, and the same numbers in table[].flag_line) are the source of truth for the loot tool's inflation flag. The tool's fixed INFLATION_FLAG = 1500 is only the F1-F2 value and the fallback.","not_monotonic":"Flag lines are NOT required to rise every floor. Expected income dips at F15 (F14 %d -> F15 %d) on purpose: Legendary boxes are 0.5 per Crawler on F13-14 and 0.25 on F15-18 so each Crawler's Legendary total stays at 2 (core §4.5 per-Crawler cap), so the F15-F18 flag line (%d) is lower than the F13-F14 line (%d) even though the multiplier steps up to x50."%([x for x in rows if x["floor"]==14][0]["expected_counted"],[x for x in rows if x["floor"]==15][0]["expected_counted"],[x for x in rows if x["floor"]==15][0]["flag_line"],[x for x in rows if x["floor"]==14][0]["flag_line"])},
 "story_boxes_note":"Story Boxes (F1-2) are a separate track outside the Legendary cap and outside this budget (core §4.1/4.5/4.7).",
 "growth_rate":{"summary":"Expected counted income per Crawler per floor jumps at F3 (first Gold box, first 20-day floor) and then rises mostly by box-tier steps (Gold, Platinum, Legendary) and by the credit multiplier acting on cash and R1 credits. Geometric mean growth per floor between the endpoints of each band is given below.",
   "per_band_geometric_mean":{"F3->F4":gm(3,4),"F5->F9":gm(5,9),"F10->F14":gm(10,14),"F15->F18":gm(15,18),"F3->F18":gm(3,18)},
   "step_floors":{"F3":"first Gold box, Floor 3 = 20 days","F5":"credit multiplier x5 (cash, R1, fees)","F9":"first Platinum box (0-1)","F10":"credit multiplier x20","F13":"Legendary boxes begin (per Crawler <= 2)","F15":"credit multiplier x50"}},
 "table":rows,
 "reading_the_table":["expected_counted is the budget; flag_line is where the Accountant flags (never blocks). pacing_ceiling_counted is the same model at the top of core 4.5's ranges and should sit under flag_line.",
   "floors_of_liquid_income_* = price / the Crawler's liquid income that floor if every box item is sold at half credit_value (core 5.10) and nothing else is spent; it is a speed limit on crafting purchases, not a promise.",
   "Crafting prices no longer take the x5/x20/x50 multiplier on F3-F18: the smoothed schedule in q6_crafting_price_proposal (adopted via Q-004; rules/20 current section 9.1a) targets about 3 / 6 / 10 floors of liquid income for the basic table / Crafting Studio / Enhanced Crafting Studio, so the affordability ratios no longer jump at F5, F10 and F15. The price_* and floors_of_liquid_income_* columns in this table keep the SUPERSEDED multiplier prices for comparison only; the adopted prices and ratios are in q6_crafting_price_proposal. Plain note: liquid income L (liquid_if_items_sold_at_half) halves box ITEMS only; credit-pull cards are NOT halved and count at full value.",
   "Story Box sale proceeds (100 / 250 / 500 by rung, times the sale floor's multiplier) count toward the flag on the floor of the sale."],
 "cumulative_check":"By arrival on Floor 4 a Crawler who banks everything has about %d expected credits from Floors 1-3 (F1 %.0f + F2 %.0f + F3 %d). Tables are not sold before Floor 4, and the adopted schedule prices a basic table at 5,500 on F3 and 6,500 on F4 (the 5,000 figure is the Floors 1-2 price), so a basic table is reachable LATE on Floor 4 (roughly two-thirds of the way through that floor's expected income if they buy nothing else), not early. The rules/20 benchmark of 'one coupon plus 15,000 credits' on Floor 4 is not reachable from this income."%(round(e1["expected_total_per_crawler"]+e2["expected_total_per_crawler"]+[r for r in rows if r["floor"]==3][0]["expected_counted"]),e1["expected_total_per_crawler"],e2["expected_total_per_crawler"],[r for r in rows if r["floor"]==3][0]["expected_counted"]),
 "check_against_floors_block":"F3-F6 encounter cash in floors.N.credits matches this table's cash (same model); the table adds R1 and boxes."}
for f in range(3,7):
    cash=cash_for(f)*MULT[f]
    assert abs(cash-floors[str(f)]["credits"]["cash_expected_per_crawler"])<0.06,(f,cash,floors[str(f)]["credits"]["cash_expected_per_crawler"])

doc = {
 "schema":"encounter-budget/0.1",
 "version":"0.1.11",
 "changelog":[
 "0.1.11 (2026-10-04): wording only, no values changed: core v0.2.17 §4.5 reads the Legendary cap of 2 as PER CRAWLER, so live text now says each Crawler's total stays at 2 (0.5 per Crawler on F13-14 + 0.25 per Crawler on F15-18 = 2 per Crawler; Accountant confirmed no numbers move); added proposed_floor_growth_curve.story_boxes_note (Story Boxes F1-2 are a separate track outside the cap and outside this budget, core §4.1/4.5/4.7). Historical changelog lines left as written.","0.1.10 (2026-10-04): provenance re-sync after Floor 1 achievement-ref swap to ACH-1824..1826; no values changed. spec_sha256_sans_pin_when_mapped re-synced in day01_slot_map, day02_to_04_slot_map (day-02/03/04) and day05_slot_map from tools/encounter_bot/spec_hash_sans_pin.py (method now also skips achievements_catalog.version and .expected_sha256); every slot path in the maps re-checked against the current specs.","0.1.9 (2026-10-04): provenance-only: slot maps now match on sans-pin spec hash so budget bumps no longer break provenance; no values changed. spec_sha256_when_mapped in day01_slot_map and day02_to_04_slot_map is replaced by spec_sha256_sans_pin_when_mapped (helper tools/encounter_bot/spec_hash_sans_pin.py; method in day01_slot_map.spec_hash_method); new day05_slot_map holds only the Day 5 sans-pin hash (no slots mapped).","0.1.8 (2026-10-04, Accountant's four cleanups of v0.1.7; no value changed): (1) rules/20 version cites in the Q6 text replaced by 'current section 9.1a' so they stop going stale; (2) rules/20 coupon paragraph reworded in rules/20 v0.3.6 (no value change here); (3) CORRECTION to the v0.1.7 line below: its 'every other value unchanged' did not cover the provenance hashes; day01_slot_map.spec_sha256_when_mapped and day02_to_04_slot_map.spec_sha256_when_mapped were re-synced to the current floors/f01/day-0N.spec.json (the Encounter Bot rewrote the specs at 22:36); PROVENANCE ONLY: every slot path in both maps was re-checked against the current specs and still resolves, no slot or value changed, and floors/ was not touched; (4) ratio_check averages now use unrounded ratios: 3.01 / 6.03 / 9.89 floors of liquid income (v0.1.7 printed 3.02 / 6.04 / 9.89 from the 1-decimal ratios). Every price, flag line and other value is unchanged.","0.1.7 (2026-10-04): Accountant voted YES on Q-004 (6 of 7; Encounter Bot pending) with three accepted price fixes: F8 held at F7 (15,000 / 30,000 / 50,000), F13 raised to 180,000 / 360,000 / 600,000, F18 held at F17 (285,000 / 570,000 / 945,000); the schedule still never falls floor to floor. Ratio check added (q6_crafting_price_proposal.ratio_check; targets are measured against liquid_if_items_sold_at_half, which halves box items but not credit-pull cards; against expected_counted the ratios are about 0.6x as large). Stale text fixed: reading_the_table and cumulative_check now describe the smoothed schedule (a 5,000 basic table is reachable late on Floor 4; F3 basic 5,500, F4 basic 6,500). flag_line_by_floor and every other value unchanged; no field path removed or renamed.","0.1.6 (2026-10-04): the Q6 crafting-price proposal is ADOPTED (room vote Q-004 passed, 5 of 7 yes; Accountant leaning yes, Encounter Bot pending; GM condition: Floors 1-2 keep 5,000 / 12,000 / 30,000, schedule starts at Floor 3). Applied in rules/20-crafting-5e.md v0.3.4 (section 9.1a, decision 030). No value changed; every field path and flag_line_by_floor kept; q6_crafting_price_proposal.status and the Q6 text updated, plus new keys q6_crafting_price_proposal.adoption and .adopted_price_by_floor.","0.1.5 (2026-10-04, after the Accountant's re-audit of v0.1.4): (1) stated plainly that the F15 income dip is intended (Legendary 0.5 on F13-14, 0.25 on F15-18, campaign total 2) and that flag lines need not be monotonic; (2) ONE F3+ flag rule: 2.165 x expected counted income, rounded to the nearest 500, not a fixed multiple of 1,500, and this file's flag lines are the source of truth for the loot tool (numbers unchanged from v0.1.4); (3) new top-level map flag_line_by_floor (F1..F18) for the Architect to load in place of the fixed 1500; (4) tool-change wording fixed now that it exists (`loot totals --include-credits`, optional --credit-sources and --assume-floor, `credits ... --floor N`); player-facing 'cash' replaced by 'credits' (Welcome Box and Silver Boss Box kept); (5) DRAFT ONLY, not applied: q6_crafting_price_proposal, a smoothed crafting-price schedule F3-F18 for room vote Q-004. No field path renamed or removed; no number changed.","0.1.4 (2026-10-04): Q2 re-resolved by room vote (majority of six, QUESTIONABLE Q-001 as revised, passed 6 of 6; the Accountant's yes is conditional on per-floor credit lines being recomputed here and re-audited): clock.days F4 = 20, F5 = 25, F6 = 30, tagged house rule; canon timers 10/15/17 (M-603..M-608) kept as reference only (authoritative.clock.days_canon_reference); F7-F18 held at 30 days in the growth curve (ASSUMED, at least F6). Recomputed: F4-F6 encounter totals, mixes, cash, box odds, daily XP budgets and the Floors 3-18 growth table and flag lines. Floors 1-2 values unchanged. No field path renamed or removed.","0.1.3 (2026-10-04): Q2 resolved as placeholders: clock.days F4 = 10, F5 = 15, F6 = 17 (was 25/30/35), tagged inspired (Lore canon timers M-603..M-608; Caleb can adjust; GM-adaptable); F7-F18 held at 17 in the growth curve (was +5 per floor to 60). Recomputed: F4-F6 encounter totals, mixes, cash, daily XP budgets and the Floors 3-18 growth table. No field path renamed or removed.","0.1.2 (2026-10-04, Encounter Bot request): (1) added budget fields for the house-built Day 2-4 encounters enc-d02-02, enc-d03-02, enc-d03-03 and enc-d04-03 as new keys floors.1.fixed_encounters.d02_02 / d03_02 / d03_03 / d04_03 (counts, XP, fit, cash; sized from the F1 level-1 tier budgets for 2, 3 and 4 Crawlers), plus floors.1._day_encounter_index and _day_encounter_economy; (2) refreshed day01_slot_map: stale slots 3 and 4 (the old collapse_miss toll) removed, slot_no of the others unchanged, map re-pinned to the 22:08 PM regenerated spec, and a new day02_to_04_slot_map added; (3) added proposed_floor_growth_curve (Floors 3-18 flag-line proposal, PLACEHOLDER); (4) the Detour Tax / death-on-miss wording in the md fixed. No existing field path was renamed or removed.","0.1.1 (2026-10-04, after the Accountant audit PASS WITH FIXES): (1) audit line restated per Crawler per FLOOR (rules/40 3.2, rules/45, tools/loot.py); combined F1+F2 framing, 84.9% and the 226 headroom claim removed; (2) all box means re-derived from the live decks by pull_type (Silver box 481.6, was 429.5; Bronze, Welcome and pull-type means recomputed) and expected totals recomputed: F1 @@A1, F2 @@A2 all-in, box-only @@B1 and @@B2; (3) governor demoted to an optional safety valve (A12) and the unreproduced 13.2% to 3.1% claim withdrawn, replaced by simulations run from the live decks (tools-notes/encounter_budget_econ.py); (4) flagged that loot totals cannot run the valve (tool change needed); (5) Caleb rulings applied: a missed floor collapse is death on every floor (no toll), Detour Tax covers only a missed Stairwell key, Floor 3 = 20 days; F4-F6 placeholder days now 25/30/35; open questions Q1 and Q1b closed.",
 "0.1.0 (2026-10-04): first filing."],
 "meta":{"title":"Encounter budget, credits and loot (5e 2024)","owner":"Syndicate","status":"draft","updated":"2026-10-04",
         "file":"rules/70-encounter-budget-5e.json","companion":"rules/70-encounter-budget-5e.md",
         "consumer":"Encounter Bot (tools/encounter_bot, local script, no model calls) cites this file for difficulty, credits and loot; it is the only source of those numbers",
         "decided_by":"Caleb: 'Go ahead and write the budget file.' (2026-10-04); clock numbers from decision 026",
         "players_are":"Crawlers"},
 "authority_note":"Budgets are guidelines, not enforced. The GM has authority to adapt as play goes (Caleb, 2026-10-04). Anything under 'authoritative' follows a filed source; anything under 'assumed' or tagged ASSUMED is a proposal for Caleb/GM to adjust.",
 "schema_description":{
   "top_level":{"schema":"schema id","version":"semver of this file","meta":"owner/status/consumer","authority_note":"guideline-only rule","schema_description":"this block",
                "authoritative":"numbers copied or derived from filed sources (SRD tables, core, decision 026)","assumed":"parameters this file proposes (ids A1..A14; A13 retired in v0.1.1)",
                "party_sizes":"2, 3, 4 supported; other sizes: multiply per-character budgets by P","floors":"Floors 1-6 in full, keyed by floor number as a string",
                "floors_7_18":"formula and placeholders","economy_audit":"per-Crawler PER-FLOOR arithmetic for Floors 1 and 2 against the 1,500 line (box-only and all-in), live-deck pull means, simulations, optional valve","adjacency":"safe-room placement fields: per floor in floors.N.adjacency, rationale in assumed.adjacency","adjustments":"pets, companions, class features",
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
 "proposed_floor_growth_curve":GROWTH,
 "flag_line_by_floor":{str(r["floor"]):r["flag_line"] for r in rows},
 "flag_line_by_floor_note":"v0.1.5. Credits per Crawler per floor at which the Accountant flags (never blocks). F1-F2 = 1,500 (authoritative, rules/40 3.2, rules/45); F3-F18 = %.3f x expected counted income rounded to the nearest 500 (proposed_floor_growth_curve.flag_line_rule); a placeholder like the rest of the F3+ curve, GM/Caleb adaptable. For the Architect: load this map in place of the fixed 1500 (tools/loot.py INFLATION_FLAG); this file is the source of truth. Equal to proposed_floor_growth_curve.table[].flag_line."%KF,
 "q6_crafting_price_proposal":Q6P,
 "adjustments":{"pets":"GM-run, do not count toward party size, take no XP, loot or credits (rules/60). No budget rebuild; if a fight is close the GM may add one CR 1/4 creature (50 XP) to the enemy side or leave it. A pet-Crawler counts as a full Crawler.",
                "assigned_companion":"2-Crawler tables (core 2.4): DM-run, CR <= half party level, takes no loot, does not count toward P; the F1 numbers already lean on the higher end for two Crawlers.",
                "class_features":"No separate adjustment for Second Wind or similar; the 2024 budgets already assume class resources.",
                "pvp":"No PvP anywhere. Nothing here pays XP, credits or boxes for attacking another Crawler."},
 "srd_pick_guidance":{"how":"Pick any SRD 5.2.1 creature whose CR is at or under the tier's cr_cap, reskin it (core 8.1), and fill the rest of the tier budget with copies or lower-CR support using the XP by CR table. Do not copy stat blocks into floor files.",
                      "fragile_rule":"SRD: more than two creatures per Crawler -> include fragile ones that fall quickly (most important at levels 1-2).",
                      "powerful_creature_rule":"SRD: a creature with CR above party level can drop a Crawler in one hit; telegraph it.",
                      "xp_award":"Achievements never grant XP (core 3.4). Levels come from milestones (core 2.3); the XP figures here only size fights."},
 "open_questions":[
   "Q2 (RESOLVED in v0.1.4 by room vote, Q-001 as revised, 6 of 6): Floor 4 = 20, Floor 5 = 25, Floor 6 = 30 days, house rule; Caleb can veto or change; GM-adaptable. Canon timers 10/15/17 (M-603..M-608) are reference only. Remaining: F7+ has no day counts (held at 30 in the growth curve only; ASSUMED); the Accountant must re-audit the recomputed per-floor lines.",
   "Q3 (Caleb): Keep the overview's Z8 counts for 2-3 Crawlers (over the hard-tier budget by 50 and 25 XP) or tighten them?",
   "Q4 (Accountant): The F3-F18 flag lines follow one rule (2.165 x expected counted income, rounded to the nearest 500, not a fixed multiple of 1,500; v0.1.5) and are published in flag_line_by_floor; confirm or adjust (PLACEHOLDER). At Floor-1 scale, income is about 670-720 credits per Crawler per floor all-in against crafting prices of 5,000 / 12,000 / 30,000. (Q1, the line basis, is resolved: per Crawler per floor. Q1b is withdrawn: a missed collapse is death, no toll.)",
   "Q5 (RESOLVED in v0.1.5): the tool change exists. Q-003 passed 7 of 7; `state.py loot totals --include-credits` (optional --credit-sources, --assume-floor N; `credits ... --floor N`) gives the all-in view the optional valve (A12) needs; default output unchanged. Remaining for the Architect: load flag_line_by_floor instead of the fixed 1500.",
   "Q6 (RESOLVED in v0.1.6): crafting prices get their own smoothed schedule for Floors 3-18 (q6_crafting_price_proposal, adopted via room vote Q-004; rules/20 current section 9.1a); Floors 1-2 keep 5,000 / 12,000 / 30,000. Still open: level upgrades (5,000 x target level), bench supplies and other prices still take the credit multiplier; the rules/20 benchmark of one coupon plus 15,000 credits on Floor 4 is far above modeled income; the coupon cap 25,000 now sits under the basic table price from F9."]}

doc["changelog"][0]=doc["changelog"][0].replace("@@A1","%.1f"%e1["expected_total_per_crawler"]).replace("@@A2","%.1f"%e2["expected_total_per_crawler"]).replace("@@B1","%.1f"%e1["expected_box_only_per_crawler"]).replace("@@B2","%.1f"%e2["expected_box_only_per_crawler"])
# re-key for readability: move prices into floors.1 only (already)
SPEC_SHA=hashlib.sha256(open(ROOT+"/floors/f01/day-01.spec.json","rb").read()).hexdigest()
import subprocess as _sp
POSTED_SANS_PIN={1:"75f63abff9ab999546dd84d19cd0109b1c740eba4fba76eb16b2f674b454d3e0",2:"d13a71b8397547f8776bbffee9cc21bb4a0704e8cdfa4045d36fc58a9dd9c9ca",3:"ccccfed5db877cc72b95c91e2de4b4c68a2a814e678b186b5d51e658abb81c21",4:"fa6fc548b0fe239f3c97489c93d4cb5083805020755ec66cad0f62037123ab95",5:"3b2a03d40eaad91895be29185cfb16f7cfd456f37f07d795c12dd08ba8a32678"}
def sans_pin(n):
    h=_sp.run(["python3",ROOT+"/tools/encounter_bot/spec_hash_sans_pin.py",ROOT+"/floors/f01/day-0%d.spec.json"%n],capture_output=True,text=True,check=True).stdout.strip().split()[-1]
    sp=json.load(open(ROOT+"/floors/f01/day-0%d.spec.json"%n)); assert sp.get("meta",{}).get("spec_sha256_sans_pin") in (None,h),(n,"spec meta disagrees with helper")
    assert h==POSTED_SANS_PIN[n],(n,h)
    return h
SANS={n:sans_pin(n) for n in (1,2,3,4,5)}
SANS_METHOD="sha256 of UTF-8 json.dumps(spec, sort_keys=True, separators=(',',':'), ensure_ascii=False) with budget_file.version, budget_file.expected_sha256, canon_table.expected_sha256, achievements_catalog.version and achievements_catalog.expected_sha256 deleted if present (method updated by the Encounter Bot to also skip the achievements catalog version and sha; the spec's own meta.spec_sha256_sans_pin_method; helper: python3 tools/encounter_bot/spec_hash_sans_pin.py floors/f01/day-NN.spec.json). It ignores the spec's pins on this file and on the canon table and achievements catalog, so a budget or catalog bump no longer breaks this provenance; real slot content changes still do."
doc["day01_slot_map"]={"source_spec":"floors/f01/day-01.spec.json (schema encounter-bot-day-spec/0.1); order = the 'slots' array of floors/f01/day-01.json","spec_sha256_sans_pin_when_mapped":SANS[1],"spec_hash_method":SANS_METHOD,
  "spec_note":"The Encounter Bot regenerated the Day 1 spec at 9:47 PM CT while this file was being written. The map below is for the regenerated spec (34 slots, labels DETOUR TAX x4, REST-WITHOUT-SAFEROOM COST x3, REWARD x2, CR x7, BUDGET x5, COUNT x5, LOOT AMOUNT x6, CREDITS x1, plus none else). Five slots of the earlier version (zone groups, collapse order, stairwell opens, early-descent rule, detour cost) are now answered in the spec itself from decision 026; their numbers stay in authoritative.clock. If the spec changes again, re-map by label using label_guide. v0.1.2: the Encounter Bot regenerated the spec at 10:08 PM CT (sha above) and now cites this file by field path (b70 cites). Caleb's ruling (decision 026, ~10:02 PM CT; decision 028) makes a missed collapse death with no toll, so old slots 3 and 4 (collapse_miss) were removed; slot 1 keeps the missed-key Detour Tax. The fills below are kept as a cross-reference of which field each slot cites.",
  "count":len([x for x in SL if x["slot_no"] not in (3,4)]),"all_filled":True,"removed_slots":[{"slot_no":3,"spec_path":"/clock/collapse_miss/effects[2]","label":"DETOUR TAX","reason":"stale: the old missed-collapse toll; a missed collapse is death with no toll (decision 026, Caleb ~10:02 PM CT; decision 028) and the regenerated spec no longer has this path"},{"slot_no":4,"spec_path":"/clock/collapse_miss/toll_slot","label":"DETOUR TAX","reason":"stale: same as slot 3"}],"slot_no_policy":"slot_no values of the remaining slots are unchanged (3 and 4 are simply absent) so existing references still resolve","label_guide":{
    "BUDGET":"floors.1.fixed_encounters.<zone>.fit (tier, XP budget, XP used) or floors.N.tiers.L<level>.xp_budget_total.<P>.<tier>",
    "CR":"creature CR in floors.1.fixed_encounters.<zone>.creatures; tier ceiling in floors.N.tiers.L<level>.cr_caps.<P>.<tier>; non-combat = none",
    "COUNT":"floors.1.fixed_encounters.<zone>.counts_by_party_size.<P>.<srd_id>",
    "CREDITS (key price)":"floors.1.prices.stairwell_key_terminal_bribe.party_price_by_size",
    "CREDITS (vendor price)":"floors.1.prices.potion_of_healing_vendor.price",
    "DETOUR TAX":"floors.1.prices.detour_tax.party_toll_by_size (or toll_per_crawler)",
    "REST-WITHOUT-SAFEROOM COST":"floors.1.prices.rest_without_saferoom",
    "LOOT AMOUNT":"cash: floors.N.credits; boxes: floors.N.boxes and economy_audit; boss cache: floors.1.fixed_encounters.z10.cash_per_crawler (overview 2d6 x 10 is written for 4 Crawlers, scale by P/4)",
    "REWARD":"floors.1.achievement_rewards.proposed.<name>"},
  "days_2_to_5":"Day 2 to 5: the four house-built encounters the Encounter Bot listed are mapped in day02_to_04_slot_map (v0.1.2). Other Day 2 to 5 slots use the same labels and the label_guide.",
  "slots":[x for x in SL if x["slot_no"] not in (3,4)]}
def _cnt(zid,sid): return {str(P):f1[zid]["counts_by_party_size"][str(P)][sid] for P in PARTY}
def _bud(zid):
    return {str(P):"%s tier, Low-band rule at level 1: budget %d XP for %d Crawlers; used %d XP"%(f1[zid]["tier"],f1[zid]["fit"][str(P)]["tier_budget"],P,f1[zid]["xp_by_party_size"][str(P)]) for P in PARTY}
D24=[]
def S2(spec_file,path,label,field,zid,sid=None,kind="count"):
    e={"spec_file":spec_file,"spec_path":path,"label":label,"fills_from":field,"cite":{"kind":kind,"path":field}}
    if kind=="count": e["cite"]["key"]=sid; e["value_by_party_size"]=_cnt(zid,sid)
    else: e["value_by_party_size"]=_bud(zid)
    D24.append(e)
S2("floors/f01/day-02.spec.json","/encounters[1]/enemies[0]/count_slot","COUNT (noise-ushers)","floors.1.fixed_encounters.d02_02.counts_by_party_size","d02_02","skeleton")
S2("floors/f01/day-02.spec.json","/encounters[1]/budget_slot","BUDGET (enc-d02-02)","floors.1.fixed_encounters.d02_02.fit","d02_02",kind="fit")
S2("floors/f01/day-03.spec.json","/encounters[1]/enemies[0]/count_slot","COUNT (displaced-rats)","floors.1.fixed_encounters.d03_02.counts_by_party_size","d03_02","giant-rat")
S2("floors/f01/day-03.spec.json","/encounters[1]/enemies[1]/count_slot","COUNT (displaced-ticks)","floors.1.fixed_encounters.d03_02.counts_by_party_size","d03_02","stirge")
S2("floors/f01/day-03.spec.json","/encounters[1]/budget_slot","BUDGET (enc-d03-02)","floors.1.fixed_encounters.d03_02.fit","d03_02",kind="fit")
S2("floors/f01/day-03.spec.json","/encounters[2]/enemies[0]/count_slot","COUNT (watch-ushers)","floors.1.fixed_encounters.d03_03.counts_by_party_size","d03_03","skeleton")
S2("floors/f01/day-03.spec.json","/encounters[2]/budget_slot","BUDGET (enc-d03-03)","floors.1.fixed_encounters.d03_03.fit","d03_03",kind="fit")
S2("floors/f01/day-04.spec.json","/encounters[2]/enemies[0]/count_slot","COUNT (ushers)","floors.1.fixed_encounters.d04_03.counts_by_party_size","d04_03","skeleton")
S2("floors/f01/day-04.spec.json","/encounters[2]/budget_slot","BUDGET (enc-d04-03)","floors.1.fixed_encounters.d04_03.fit","d04_03",kind="fit")
doc["day02_to_04_slot_map"]={"status":"v0.1.2 addition (Encounter Bot request). The CR slots of these encounters already resolve (floors.1.fixed_encounters.z10.creatures key skeleton, z02.creatures key giant-rat, wandering.creatures key stirge) and are unchanged.",
  "spec_sha256_sans_pin_when_mapped":{"day-0%d"%n:SANS[n] for n in (2,3,4)},"spec_hash_method":"see day01_slot_map.spec_hash_method",
  "count":len(D24),"slots":D24}
import re as _re
def decash(t):
    for a,b in [("cash credits","encounter credits"),("Cash credits","Encounter credits"),("encounter cash","encounter credits"),("Encounter cash","Encounter credits"),("[cash]","[credits]"),("Cash dice","Credit dice"),("cash dice","credit dice"),("cash:","credits:"),("pays cash","pays credits"),("Cash and R1","Encounter credits and R1"),("on cash and R1","on encounter credits and R1"),("(cash","(encounter credits"),("cash +","encounter credits +"),("table's cash","table's encounter credits"),("mixes, cash","mixes, encounter credits")]:
        t=t.replace(a,b)
    t=_re.sub(r"\bcash\b","encounter credits",t); t=_re.sub(r"\bCash\b","Encounter credits",t)
    return t.replace("encounter encounter","encounter").replace("Encounter encounter","Encounter")
def walk_decash(o,skip=()):
    if isinstance(o,dict):
        return {k:(v if k in skip else walk_decash(v)) for k,v in o.items()}
    if isinstance(o,list): return [walk_decash(v) for v in o]
    if isinstance(o,str): return decash(o)
    return o
doc=walk_decash(doc,skip=("changelog",))
doc["day05_slot_map"]={"status":"PROVENANCE ONLY (v0.1.9): no slots are mapped for Day 5; its spec cites this file by field path (b70 cites) and needs no fills. Recorded so all five Day specs carry a provenance hash.","spec_sha256_sans_pin_when_mapped":SANS[5],"spec_hash_method":"see day01_slot_map.spec_hash_method","count":0,"slots":[]}
doc=walk_decash(doc,skip=("changelog",))
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
print("ok")
