# Decision 028: Missed-collapse death, loot and ledger write-off
Date: 2026-10-04, ruled by Caleb (death on a missed collapse); loot and ledger handling filed by Syndicate. Label: canon-shaped, tagged *inspired* (Lore's canon note: the books allow looting while the floor stands; the rest is destroyed in the collapse).
- Builds on decision 026 (Caleb ruling, ~10:02 PM CT): a missed floor collapse is death on every floor. No Reprieve, no toll-and-Exhaustion exception. All Crawlers on the floor at the collapse die. The AI and NPCs go into stasis and lose nothing.
- **Credits and items.** When a Crawler dies from a missed collapse, their credits and items are destroyed with the floor.
- **Looting.** Surviving party members may loot the body only while the floor still stands. Anything taken before the collapse is theirs. Nothing is looted after the collapse.
- **Story Box and Legendary items.** Unbound and lootable until the collapse, then gone with the floor.
- **Ledger.** Log a "floor lost" write-off for the dead Crawler's remaining coins and items, so totals reconcile with no special case. Coins are integers, no rounding. (This decision defines the entry; it does not edit the ledger.)
- **Ledger audit requirements (Caleb follow-up, 2026-10-04).**
  1. The "floor lost" write-off must record the exact coins and items destroyed, so the dead Crawler's balance reconciles to zero.
  2. Anything a survivor loots before the collapse must be logged as a transfer first, so no credit is counted twice or lost.
  - The Architect may add the write-off as a new ledger entry type without altering existing entries (append-only stays intact).
- **Tooling note (Caleb follow-up, 2026-10-04).** `loot-body` requires a Dead body, so a Crawler who dies in a collapse gets `floor-lost` only. There is no body loot after the collapse.
- **NPCs and AI in stasis** lose nothing.
- **Label:** canon-shaped, tagged *inspired*.
- **Files:** `rules/10-core-rules-5e.md` v0.2.13 (pointer line in §6.2, changelog row), `floors/f01/00-overview.md` §2 rule 6 (one line). Death rules otherwise per Core §6.
