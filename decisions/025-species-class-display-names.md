# Decision 025: Nationality display names for species and classes; species variants are cosmetic

- **Date:** 2026-10-04. **Owner:** Syndicate Dungeon Crawl System 001. **Caleb's call:** yes (room messages and his private chat with Lore).
- **Display layer only.** Species, lineages, classes and class options show in `/create` as "Our Name (5e Name)" from Lore's `species-class-reskins` table (item-reskin pattern). Ids, stats, rules and ledger rows use the 5e ids. Real nationalities, played for comedy, no risk flags (Caleb).
- **Variants are cosmetic.** Caleb wants each sub-type as its own pick (for example Felid: Cat, Cat Girl, Tigran, Were-Cat; Caprid breeds, Dragonborn colours). Default ruling, closing species supplement question 14: every variant is a **display name** with a `base_id` pointing to its 5e species or lineage id, and takes that base entry's rules unchanged. Tigran included (Felid, Medium or Small as the base allows). If Caleb later wants a variant to have its own mechanics, it needs a rules entry from Syndicate first.
- **Guardrail (GM):** the coverage check fails on any variant with a missing or unknown `base_id`.
- **Approved by Caleb 2026-10-04 (9:00 PM CT):** `species-class-reskins.json` v0.1.5, 74 entries, sha256 3a3a49b05d93661e4b5699039941006caf9ba9a2f00115c649cd8e21bdfc552d. Unique nationality per entry. Scope in `/create`: nine SRD species, 24 lineages, 12 classes, 4 class options; all variants wait for the Floor 3 Offer.
- **Lajabless:** Radiant and Skull entries are state labels, not a pick. A Lajabless starts in Radiant (rules/30 §4.7). Caprid breeds and Nodling heads are cosmetic Offer picks, no rules change.
- **Go-live:** the Architect re-syncs to v0.1.5, runs the strict check, flips the flag and restarts.
