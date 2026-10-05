# Decision 031: Field-rest fee (Season Zero)

Summary: Clarifies the rest-without-a-saferoom price so Ch1 and Floor 1 pages stay in sync.

## Ruling (Syndicate, 2026-10-05; matches filed Floor 1 Day pages + core §5.6)

1. A **field rest is a Short Rest only**. Long Rest remains saferoom-only (core §5.6).
2. A Short Rest in a spot that is **already quiet** is **free**. No fee.
3. The rules/70 price (**20 credits per Crawler**, **cap 60 per Crawler per floor**) **buys quiet** for a Short Rest where the area is **not** quiet. It never grants a Long Rest.
4. A Long Rest attempt outside a saferoom is **interrupted** (Floor 1: Ceiling Ticks after 1d4 hours). Paying the fee does **not** purchase that Long Rest.

## Not this

- The fee is **not** "20 credits for any Short Rest outside a saferoom."
- The fee is **not** only a surcharge on a failed Long Rest attempt with Short Rests always free regardless of noise — quiet Short Rests are free; noisy ones use the fee to buy quiet.

## Sources

- Core §5.6 (Long Rest saferoom-only; Short Rest anywhere reasonably quiet)
- `rules/70-encounter-budget-5e.json` `floors.1.prices.rest_without_saferoom`
- Floor 1 Day 1–5 GM ruling ("no fee if the spot is already quiet… fee only buys quiet where the area is not")

## Follow-up

- Book Author: patch Ch1 to this wording.
- Encounter Bot: keep Day page GM ruling; do not reframe the fee as Long-Rest-failure-only.
- Architect: optional later — align the JSON `applies_to` string with this ruling (wording only).
