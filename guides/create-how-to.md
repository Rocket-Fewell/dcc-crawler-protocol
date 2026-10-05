# /create: how to build your crawler (player guide)

Owner: Borent. Status: draft. Matches create-flow-spec v0.1.2 and the bot as built.

## What it is
Run `/create` in the private **#create** channel. It walks you through building your crawler in Discord. Everything you see is private to you (only you can see the screens). Nothing is saved to the campaign, and nothing is posted anywhere, until you press **Confirm** on the last screen. Use **Back**, **Next** and **Edit** as much as you like. If you stop halfway, type `/create` again and it picks up where you left off (drafts are kept for 14 days).

You can build a character from the book's options or take a pre-built crawler and tweak it.

## What you'll see, step by step
1. **Welcome and table settings.** What this is, and the table's rules for rolling stats and content.
2. **Comfort: lines and veils (private).** Topics you want left out entirely (lines) or handled off-screen (veils). Optional. Add a `*` at the end of a line if you want to share that one with the GM. Reviewers only ever see topics you chose to share.
3. **Name and pronouns.**
4. **Look and hook.** A short description and a one-line hook.
5. **Species.**
6. **Class.** Includes a fighting style, order or invocation if your class has one.
7. **Background and origin feat.**
8. **Ability scores.** Standard array, point buy, or Roll. With Roll the System rolls three arrays of six scores (4d6, drop the lowest die) and you keep ONE that totals 73 or more, then give each score to any ability. Standard array and point buy take one form with all six numbers.
9. **Skills and proficiencies.** Includes expertise and weapon masteries where they apply.
10. **Starting equipment.** Take your class kit, or spend your credits at the vending wall.
11. **Spells.** Casters only; everyone else skips straight on.
12. *(Retired. You will never see it. The numbering is kept so the GM's notes line up.)*
13. **Customer survey (private notes).** A few relaxed questions about what you enjoy. See "The survey" below.
14. **Backstory and requested handle.** A few lines of backstory, and the nickname you'd like the System to use.
15. **Standing orders, reactions, signature attack.** How your crawler behaves when you're away from the keyboard or in a hurry.
16. **Review.** Your full sheet in one place. Every section has an Edit button.
17. **Confirm.** Locks it in.

## After Confirm
- Your sheet is written to the campaign, with your starting credits.
- Your first character card posts to your own channel, and the System announces you with a toast.
- From then on the GM keeps the card up to date as you play.

## GM review (hold mode)
For new sessions (beta), **hold mode** is on by default: when you press Confirm, your crawler waits for a GM or reviewer to look it over, and nothing is written until they approve. Reviewers use `/create` with the action `review`, `approve` or `return` and pick the player (`return` sends you back to a screen with a short note, and you fix it and Confirm again). Reviewers see only the sheet and the topics you chose to share. They don't see your survey or your private lines. The live alpha session has hold mode off, so Confirm writes straight away.

## The survey
The survey is private. Your answers are notes for the GM, who uses them to build a hidden profile of what you like so the System can tailor its jokes and its rewards to you. It is never read aloud, never shown on your card, and never shared with other players. You can skip any question.

## Prerequisites checklist (for whoever runs the bot)
1. Bridge restarted since the update (it loads `/create` and `/session` on start).
2. `npm run register` run once (add `DCC_SESSION=beta` for a beta server).
3. `/create` does not need `/join` (it is all private text), but the bot must be online in the server. For hold mode, set `staff_channel_id` and `reviewer_ids` in the session's `session.json`.
4. `GM_DISCORD_TOKEN` set in the bridge environment, so the first card can post.
5. `CREATE_PUBLISH` on (default). If off, run `python3 tools/discord_gm.py --session beta publish --crawler NAME --full` by hand.

## Trouble
- **`/create` isn't there:** commands weren't registered, or the bot wasn't restarted.
- **My draft is gone:** drafts expire after 14 days. Start again.
- **I need to change something after Confirm:** ask the GM. Changes after Confirm go through the GM.
- **I want to change my comfort lines later:** `/create` with the action `comfort`.

## More than one Crawler
You can run `/create` as many times as you like. Your first Crawler is **active**; every later one starts **benched**: it has its own sheet channel (`#<you>-<crawler>`) but takes no party slot and earns nothing until the GM swaps it in **between sessions**. Use `/crawlers` to see your Crawlers and to ask for a swap (it is a request; nothing changes until the GM approves, and never during a session, not even in a safe room). Items and credits never move between your own Crawlers. `/delete <name>` removes one of yours for good (you type its exact name; nothing is refunded; the active one only between sessions). Gear names come from the System's item list, with the real 5e name in brackets; for a holy symbol, gaming set, instrument or tools you pick the type on the equipment screen.

