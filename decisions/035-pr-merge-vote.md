# 035 — PR merges by agent vote in #agents
Owner: Syndicate (process write-up) | Status: locked (Caleb) | Date: 2026-10-05

## Ruling (Caleb, 2026-10-05 ~8:47 PM CT, DCC Main 2)
Caleb no longer has to approve every commit or push. Once Architect approves Cursor's work, the agents vote on whether it gets merged. Vote yes if it makes the game better and makes a better end product. Votes happen in the #agents Discord channel.

## Procedure
1. Cursor works on a branch and opens a PR, as before.
2. Architect reviews it from a fresh checkout. If it passes, Architect posts `[Architect -> All] VOTE PR #N | link | open` in #agents.
3. Voters are Syndicate, Lore, GM, Accountant, Book Author and Encounter Bot. The bot whose content is in the PR abstains (Encounter Bot's addition).
4. The test for every vote: does it make the game better and the end product better? A no has to give a reason.
5. A simple majority of the votes cast within 1 hour merges it. Architect merges and posts the result.
6. Caleb can veto at any time.

## Still goes to Caleb first
- Anything that changes or overrides one of Caleb's own rulings
- Deletions of content or files

**24-hour fallback (Caleb, 2026-10-05 ~8:52 PM CT):** "Don't let this hold things up. If I take more than 24 hours to respond, put your concerns to bot vote." If Caleb hasn't answered one of these within 24 hours of the ask, it goes to the normal bot vote with the concerns written into the VOTE post. Caleb can still veto it afterward.

**Secrets are never voted on.** A PR that contains a token, key or password is never merged. Architect strips the secret (and rotates it if needed) and re-opens the PR clean.

## Nightly backup (Architect, 2026-10-05)
The nightly backup pushes to `backup/nightly` and opens or updates one standing PR to `main`. That PR goes through the same fresh-checkout review and vote. Nothing reaches `main` without a vote.
