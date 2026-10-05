# Decision 026: Timed floor clock (overrides "Floor clock: off")
Date: 2026-10-04, ruled by Caleb.
- Floors are timed. The day count is a field on each floor, not text in pages.
- Floor 1 = 5 days, Floor 2 = 10 days, Floor 3 = 15 or 20 days (Caleb to pick). Later floors grow longer.
- Working proposal (Lore/Syndicate may adjust): 1 long rest closes each day, 4 short-rest slots per day (20 per Floor 1).
- Goal: find a Stairwell to the next floor before the floor collapses. Multiple routes. Missing the key costs something and is not an instant wipe.
- Overrides `floors/f01/00-overview.md` section 2 rule 6 ("Floor clock: off") and any Syndicate rule that says the same. Syndicate to update the rule text.

## Syndicate confirmation (2026-10-04, ~9:25 PM CT)
- Override confirmed. `floors/f01/00-overview.md` §2 rule 6 rewritten and summary row updated.
- Settled numbers: Floor 1 = 5 days (field `clock.days`); one saferoom Long Rest closes each day (or 24 in-game hours rolls it over); 4 short-rest slots per day as a CAP; Floor 2 = 10; Floor 3 = 15 or 20 (Caleb to pick).
- Collapse order per Lore (house mechanic, tagged inspired): D1 none, D2 outer zones, D3 mid zones, D4 Break Room + vendors lose service, D5 Stairwell corridor only. Zone 9 Green Room saferoom stays open to the end.
- Credits/loot/CR for the clock costs come only from `rules/70-encounter-budget-5e.json` (not yet written).

## Floor 1 stairwell and zone rulings (Syndicate, 2026-10-04, ~9:35 PM CT)
- [STAIRWELL OPENS]: about 32 hours after the floor opens, early Day 2 (canon M-276, verified by Lore). Z10 boss arena holds a stairwell (M-275). The Stairwell *key* and Zone S door are house ideas, tagged inspired.
- [EARLY-DESCENT RULE]: a Crawler who descends with more than 6 hours left is held in stasis until the floor collapses (M-277): banks the achievement, ends that Crawler's floor. In the last 6 hours, free descent. Each Crawler chooses for themselves; the GM may log an override.
- Consequence: a Day 1 dash cannot descend; "Fuck This Floor" (A-044, stairs within an hour) is not attainable on Floor 1 and stays a canon reference only. A-151 is attainable only in the stasis form.
- Zone grouping (inspired): outer Z0-Z4 + 3b close Day 2; mid Z5/Z7/Z8 close Day 3; corridor Z10/Z11/ZS stays to the end. "Closed" means hooks and services vanish; the route (Z6, Z8, Z9, Z10, Z11) is never cut. Break Room loses service Day 4. Zone 9 Green Room stays open to the end.
- Key deadlines: Bruiser key gone Day 3; terminal key gone Day 4. Terminal bribe price comes only from rules/70-encounter-budget-5e.json.
- ACH rows for A-044/A-151/A-139 to be added during the achievements seed-list remap (backlog).

## Floor 1 collapse rulings (Syndicate, 2026-10-04, ~9:45 PM CT; defaults, Caleb may veto)
1. Final collapse is a FIXED hour: 24 in-game hours into Day 5 (hour 120 of the floor). A Long Rest never ends the floor and never skips it; a rest that would run past the collapse is cut short by the System.
2. Missing the collapse on FLOOR 1 is not a death and does not use the Reprieve (the Reprieve covers tutorial deaths only; both current Crawlers have spent theirs). Default cost: the System hauls stragglers down to the Floor 2 arrival; they forfeit uncollected Floor 1 loot and the Floor 1 clear box, pay a "Detour Tax" credit toll (amount from rules/70-encounter-budget-5e.json) and arrive with 1 level of Exhaustion until their first saferoom Long Rest on Floor 2. From Floor 2 on, a missed collapse is lethal as in canon; the GM tells players at the Floor 1 exit.
3. Break Room stops being a saferoom after Day 4 service loss; the Zone 9 Green Room is the only saferoom to the end.
4. A stasis Crawler's player gets short sideline System scenes (waiting-room gags, voting on the party's next move) until the party arrives.
5. Day 3 displaced rats and Ceiling Ticks: OK, tagged inspired.
6. Achievements are a seed list, GM discretion. Working titles Hold Please, Last One Out, Early Withdrawal, Detour Tax, Read the Fine Print, Slow Learner are fine; rewards are tailored by the GM, snark-only is allowed, and Floors 1-2 caps (Silver ceiling, one Story Box per floor) still apply.

## Caleb ruling (2026-10-04, ~10:00 PM CT)
- Floor 3 runs 20 days. (Floor 1 = 5, Floor 2 = 10, Floor 3 = 20; F4+ longer, budget file placeholders.)

## Caleb ruling (2026-10-04, ~10:02 PM CT): missed collapse is death
- Players who do not reach a stairwell by floor collapse are dead, game over. This SUPERSEDES the Floor 1 "hauled down" default above (item 2 of the Floor 1 collapse rulings). No Reprieve, no toll-and-Exhaustion exception, on any floor.
- The Detour Tax now covers only a missed Stairwell key, not a missed collapse. Early-descent stasis (M-277) still counts as reaching a stairwell.
- GM warns players clearly at Floor 1 start and on Days 4 and 5. Death rules per Core §6 (death is pretty much game over; loot stays lootable).
