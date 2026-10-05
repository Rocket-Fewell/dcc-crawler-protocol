# background-reskins GP/cp note (approved by Caleb 2026-10-04; table side applied in background-reskins v0.1.2)
Owner: DCC Lore | Status: review | Version: 0.2 | Updated: 2026-10-04
Summary: Every string that shows GP/cp or cash next to the Caleb-approved background labels, with proposed replacements that use credits. background-reskins.json (v0.1.1, live) is NOT changed; this is a proposal only (Syndicate audit, section 4 and F3).

## Rule behind it
1 credit = 1 GP (core 5.10, spec glossary: say credits, not gold, in System text). Amounts and `{gp}` stay exactly as in chargen-5e.json. Do not convert anything. How copper (cp) reads in credits is NOT settled (see create-screens-reskins vanilla_on_purpose `money-cp-open`).

## A. Strings printed with the background labels (built in the bridge, not stored in the table)
The table stores only the name. The bridge appends the amount: `packageLabel(t, p.id, gpText, plain)` in bgnames.js, called from screens.js (S10 background menu).

| Where | Current text | Proposed text |
|---|---|---|
| S10 background menu, package with items | `Cardboard Box From Your Desk (Package A) - {gp} GP left over` | `Cardboard Box From Your Desk (Package A) - {gp} credits left over` |
| S10 background menu, gold option | `Severance Envelope, Unmarked (Package B) - {gp} GP` | `Severance Envelope, Unmarked (Package B) - {gp} credits` |
| bgnames.js comment/example | `Our Name (Package A) - 8 GP left over` | `Our Name (Package A) - 8 credits left over` |

Delivery options for the later v0.1.2: (1) change the two gpText templates in the bridge to the credits wording (the class menu already uses it through `package-class-a`, `package-class-b` and `package-gold` in create-screens-reskins), or (2) add two template fields to background-reskins (`amount_text_items`, `amount_text_gold`) and have the bridge read them. Either way the class and background menus then agree.

Resulting labels per background (amounts from chargen-5e.json, 16 backgrounds):

| Background | Package | Current | Proposed |
|---|---|---|---|
| Acolyte | A | Cardboard Box From Your Desk (Package A) - 8 GP left over | Cardboard Box From Your Desk (Package A) - 8 credits left over |
| Acolyte | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Artisan | A | Cardboard Box From Your Desk (Package A) - 32 GP left over | Cardboard Box From Your Desk (Package A) - 32 credits left over |
| Artisan | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Charlatan | A | Cardboard Box From Your Desk (Package A) - 15 GP left over | Cardboard Box From Your Desk (Package A) - 15 credits left over |
| Charlatan | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Criminal | A | Cardboard Box From Your Desk (Package A) - 16 GP left over | Cardboard Box From Your Desk (Package A) - 16 credits left over |
| Criminal | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Entertainer | A | Cardboard Box From Your Desk (Package A) - 11 GP left over | Cardboard Box From Your Desk (Package A) - 11 credits left over |
| Entertainer | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Farmer | A | Cardboard Box From Your Desk (Package A) - 30 GP left over | Cardboard Box From Your Desk (Package A) - 30 credits left over |
| Farmer | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Guard | A | Cardboard Box From Your Desk (Package A) - 12 GP left over | Cardboard Box From Your Desk (Package A) - 12 credits left over |
| Guard | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Guide | A | Cardboard Box From Your Desk (Package A) - 3 GP left over | Cardboard Box From Your Desk (Package A) - 3 credits left over |
| Guide | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Hermit | A | Cardboard Box From Your Desk (Package A) - 16 GP left over | Cardboard Box From Your Desk (Package A) - 16 credits left over |
| Hermit | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Merchant | A | Cardboard Box From Your Desk (Package A) - 22 GP left over | Cardboard Box From Your Desk (Package A) - 22 credits left over |
| Merchant | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Noble | A | Cardboard Box From Your Desk (Package A) - 29 GP left over | Cardboard Box From Your Desk (Package A) - 29 credits left over |
| Noble | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Sage | A | Cardboard Box From Your Desk (Package A) - 8 GP left over | Cardboard Box From Your Desk (Package A) - 8 credits left over |
| Sage | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Sailor | A | Cardboard Box From Your Desk (Package A) - 20 GP left over | Cardboard Box From Your Desk (Package A) - 20 credits left over |
| Sailor | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Scribe | A | Cardboard Box From Your Desk (Package A) - 23 GP left over | Cardboard Box From Your Desk (Package A) - 23 credits left over |
| Scribe | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Soldier | A | Cardboard Box From Your Desk (Package A) - 14 GP left over | Cardboard Box From Your Desk (Package A) - 14 credits left over |
| Soldier | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |
| Wayfarer | A | Cardboard Box From Your Desk (Package A) - 16 GP left over | Cardboard Box From Your Desk (Package A) - 16 credits left over |
| Wayfarer | B | Severance Envelope, Unmarked (Package B) - 50 GP | Severance Envelope, Unmarked (Package B) - 50 credits |

## B. Strings inside the table that use money words (flavor only, not units)
| Entry id | Field | Current | Proposed |
|---|---|---|---|
| acolyte | flavor | Ran Wednesday-night youth group on two pizzas and divine patience. Found out heaven has no petty cash. | Ran Wednesday-night youth group on two pizzas and divine patience. Found out heaven has no petty credits. |
| package-b | flavor | Cash in hand, no gear, and a note that says 'good luck'. Shop at the Vending Wall and hope. | Credits in hand, no gear, and a note that says 'good luck'. Shop at the Vending Wall and hope. |

Both are jokes, not unit labels. They are listed so the S10 vocabulary stays consistent (credits, never cash); keep them if Caleb prefers the idiom ('petty cash').

## C. Name that collides with loot boxes (Syndicate F3)
| Entry id | Field | Current | Proposed |
|---|---|---|---|
| package-a | display_name / combined_label | Cardboard Box From Your Desk / Cardboard Box From Your Desk (Package A) | Cardboard Carton From Your Desk / Cardboard Carton From Your Desk (Package A) |

Reason: 'box' on S10 collides with loot boxes (Welcome Box, Bronze box). The package-a flavor line does not use the word.

## D. Not in the background table (S10 shared text)
Price list and variant-select descriptions print `{n} GP` for 100 cp or more and `{n} cp` below that (screens.js `priceText`). `{n} GP` becomes `{n} credits` (row `hint-money-gp` in create-screens-reskins v0.1.2). The `cp` form waits for a ruling.

## Status (2026-10-04, after Caleb's approval)
- APPLIED in background-reskins v0.1.2: section B (package-b and acolyte flavor, no 'cash') and section C (package-a is now 'Cardboard Carton From Your Desk (Package A)'). Ids, rules and the 32-entry count unchanged.
- NOT applied (needs_code, Architect): section A, the credits wording appended by bgnames.js packageLabel / screens.js. Templates: `<combined_label> - {gp} credits left over` and `<combined_label> - {gp} credits`. Amounts are the unchanged chargen-5e.json gp numbers (all whole numbers).
- Money rule (resolved): 1 credit = 1 GP (Core 5.10), 1 cp = 0.01 credit; whole credits print without decimals (15 credits), fractions with decimals (0.5 credit); 'credit' singular for an amount of 1 or less. Recorded in create-screens-reskins v0.1.3 (audit row money-cp-rule; rows hint-money-gp, hint-money-cp).
