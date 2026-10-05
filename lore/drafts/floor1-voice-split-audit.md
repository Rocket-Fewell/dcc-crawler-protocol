# Floor 1 voice-split audit (Caleb 2026-10-05)
Owner: DCC Lore | Status: draft | Version: 0.1 | Updated: 2026-10-05
Summary: Part A applies the Discord [SYSTEM]/[GM] voice split to Floor 1 lore drafts. Part B is a read-only canon/voice slip list on campaign Floor 1 Day pages (Encounter Bot mid-rewrite). No /workspace/dcc-campaign edits. No sealed paths opened. Nothing posted.
Voice split recalled: **[SYSTEM]** = dry corporate informative only (floor clock, fees, registration, collapse warnings, floor notices; no jokes). **[GM]** = snark, jokes, pop-culture hits, and FULL achievement/loot callouts (banner + mocking description). A tag carries until the next tag; a [GM] tag must follow every System block before any joke. No Death Mode / Easy Mode / Hardcore. Always Crawlers. Saferoom one word. Soft brevity.

---

## Part A — Lore drafts changed

| File | Was | Now | New sha256 (full) | Short |
|---|---|---|---|---|
| `drafts/floor1-collapse-notices.draft.md` | v0.1 untagged System snark notices + achievement frames | v0.2 [SYSTEM] dry notices + following [GM] color; achievement frames [GM] end to end | `d23a39b90cbeea4690868e7ef4ee27d13b9294b4d841ef94506e3381399d627c` | `d23a39b90cbe` |
| `drafts/floor1-dean-thudd-intro.draft.md` | untagged "System host" set piece | v0.2 optional dry [SYSTEM] boss line + full intro under [GM] | `d821d0839503df04e4bd579a8b4f7cdc2a1c46b8e12a499eda04c3d52e217bf5` | `d821d0839503` |
| `drafts/floor1-zone-color.draft.md` | v0.1 mixed color with snarky embedded System lines | v0.2 [SYSTEM] "Zone closing." only; jokes/atmosphere under [GM] | `a1ef4c1cedbd5d295495d0b6e389cb16161b7579de5062bb37385546ec8ba5f4` | `a1ef4c1cedbd` |
| `drafts/achievement-suggestions-days-02-05-lore-pass.md` | v0.1 flavor as "System voice" | v0.2 voice-split note; banner format [GM]; every Flavor line tagged [GM] | `216303c74dc6b659fdafd06f8a1ad6f757b53e5beb88402afc365c57d57a8146` | `216303c74dc6` |
| `drafts/f01-legendary-oneoffs-research.md` | house "Safe Room" paraphrase | spelling note; house prose → saferoom (ledger quotes untouched) | `3de8d25131311d48f9608427e57ace7a6e6c03d48163dfa5318e3a9f332a55cc` | `3de8d2513131` |

**Not edited (out of spoken-line scope or already meta):** `drafts/premise-verification.md`, `drafts/floor-bible-v0.4-canon-check.md`, `drafts/srd-nonsrd-audit.md`, `drafts/gm-habits-reference-bank.draft.md` (general GM habits, not Floor 1 playthrough lines). No Day 1 achievement-suggestion draft exists under lore drafts (Day 1 working titles live in collapse-notices achievement frames).

**Old hashes:** pre-voice-split drafts were not version-hashed in INDEX; treat prior content as v0.1 / untagged. New hashes above replace them.

---

## Part B — Read-only Day page slips (campaign)

Checked under `/workspace/dcc-campaign/floors/f01/` only. **Never edited.** Encounter Bot is mid-rewrite: `.spec.json` files (mtime ~13:48 CT) already split many collapse notices into dry `text` + `gm_color`; live `.json` / `.md` (mtime ~13:26 CT) still carry jokes inside System/collapse fields. `00-overview.md` is older (2026-10-04 22:14 CT).

### Inventory (mtime local America/Chicago; full sha256)

| File | mtime (CT) | sha256 |
|---|---|---|
| `00-overview.md` | 2026-10-04 22:14:36 | `8a46574f6f09f1d557071a33a098cf7fb4a55dd1e3816a5a84b46c8e3ebbae4a` |
| `day-01.json` | 2026-10-05 13:26:34 | `d09cb6ee012964e5dceec9e9c2a704391ff483322b00e630658627fc3c0b38ed` |
| `day-01.md` | 2026-10-05 13:26:34 | `290e05052f2b1592a95ae78711e6f8a1f4c7652f660c7f32ad4eaa0fed038177` |
| `day-01.spec.json` | 2026-10-05 13:48:38 | `1136e38ab98c26203ba85da9671a0f13798e3bf6d105273207843a18713d562f` |
| `day-02.json` | 2026-10-05 13:26:36 | `f7676ac3df6a24418bd8eeb68ee41867d45b3f997dac10ec697b1169d02d2e7e` |
| `day-02.md` | 2026-10-05 13:26:36 | `5b5bc7bede207e077dd2c652ecaca060d848fa3b968a33a931e1542eacca385d` |
| `day-02.spec.json` | 2026-10-05 13:48:38 | `46b0eb46999211c933126504a734198bb290aa0061d195b42eda844c68fc0f40` |
| `day-03.json` | 2026-10-05 13:26:39 | `55c96f78ab31c2fbf34c2abb67a1fb600edd537501c9f2579cf9b9286a036837` |
| `day-03.md` | 2026-10-05 13:26:39 | `a411bd38d75b666c9b9a97a8d6c9d13524e3a633eef897a1e17b6d592586f822` |
| `day-03.spec.json` | 2026-10-05 13:48:38 | `bb3068e37eae22db8196bb1d70c9c73ad07353c809d1c1fd5197234d9e4e0db3` |
| `day-04.json` | 2026-10-05 13:26:42 | `9b3893628da719ffc6bcb1864db20f085b9dce69c1a29c5e79780bbdc8c9264a` |
| `day-04.md` | 2026-10-05 13:26:42 | `80d829fa64dc79c25b936ba76a2463ff588ef31868ba460552607f33ab0cf817` |
| `day-04.spec.json` | 2026-10-05 13:48:38 | `f3b2795cc3527e98a33e706a7c692948d0e6a642d91d277f4799f4cf889cd083` |
| `day-05.json` | 2026-10-05 13:26:45 | `bb58f7b1f6743aaef6838f47f508a6089740f01ef6d6238460a13a5a4633f140` |
| `day-05.md` | 2026-10-05 13:26:45 | `68eda56ec114c994b41ab4a0aa6be9329b054dc5863860d93f3f019ba2d336bc` |
| `day-05.spec.json` | 2026-10-05 13:48:38 | `ae20cd5ac1a34c42a9b43302ee4a840329d9923a70d8d94a090e8512c99566fb` |

### Top slips (file · where · issue · suggested fix)

1. **Death Mode / difficulty tags (canon: no difficulty settings)**  
   - `00-overview.md` §1 and TOC, session plan, changelog, open Q16 (mtime 2026-10-04 22:14) — whole "Death Mode selection (Service Plans)" section.  
   - `day-01.md` / `day-01.json`: intake enemies_note, win voice line, carry_on choice/effect, GM track "Death Mode logged…".  
   - **Fix:** rename to campaign revive/fee plan language that is not a difficulty mode (or drop player-facing "Death Mode"); scrub from [PLAYER-FACING] win lines. Keep any GM-only bookkeeping if the table still uses Costly Revives as a house fee table.

2. **Collapse / floor notices still joke under System-facing fields (live json/md; specs partly fixed)**  
   - `day-02.json` `.day.collapse_notice.text` — "renovation… gone… lesson… You're welcome."  
   - `day-03.json` collapse_notice — "afterlife… Sadly."  
   - `day-04.json` collapse_notice — "gone to lunch… mercy and liability."  
   - `day-05.json` collapse_notice — "Please do not make us say it twice."; `.day.floor_exit.system_line.text` — "flowers."  
   - **Fix:** match lore drafts / current `.spec.json` pattern: dry FLOOR NOTICE in `text` (or [SYSTEM]), snark only in `gm_color` / [GM]. Specs at 13:48 already show the shape for Days 2–5.

3. **`voice_lines.system_intro` carrying jokes / set-piece banter**  
   - `day-01.json` `enc-d01-06` system_intro — horn/beams/one-hour/Natives are canon-aligned (M-546, M-539, M-545, M-547) but ends with "System wishes them luck with that" (joke → [GM]).  
   - `enc-d01-06` midpoint_twist — weight-limit pet registration aligns with M-554; tone OK as [GM] color more than System.  
   - `enc-d01-06` win — "Death Mode chosen…" (see #1).  
   - `enc-d01-01` system_intro — schedule briefing mixed with pool-joke snark.  
   - `enc-d01-08` / mascot lines — mock-hype belongs under [GM], not system_intro.  
   - Specs: some `gm_color` keys exist; many system_intro lines still not fully stripped.  
   - **Fix:** system_intro = facts only; move punchlines to gm_color / [GM].

4. **Process line still promises snarky System notices**  
   - `day-01.md` Collapse event block: "the System announces it with a snarky notice".  
   - **Fix:** "System announces with a dry floor notice; GM reads optional color."

5. **"champion" in boss announcement_style (not the banned word "champs", but easy to misread)**  
   - `day-03/04/05` `.md`/`.json` Dean announcement_style: "hype for the champion".  
   - Meta checks already say `'Crawlers' never 'champs'`.  
   - **Fix:** say "title bout / opponent" to avoid champ-adjacent wording in Lore notes.

6. **Safe room spelling**  
   - No `safe room` / `safe-room` hits in Day 1–5 md/json/spec at check time (good; "saferoom" already used). Overview uses saferoom in places. Leave "Time to Safe Room Closure" if it appears elsewhere as the in-game label.

7. **Achievement / loot as System**  
   - No `New achievement!` strings found under System keys in these Day files at check time. Catalog rewards are referenced as ACH ids. When filing Days 2–5 suggestions, keep banners [GM] per lore-pass v0.2.

8. **Cold open / collapse / saferoom vs CANON-LEDGER v1.15 (content check)**  
   - Horn + light beams + one-hour window + Natives + first foot on Floor 1 + pets above a weight count + swallowed by stairwell: present on Day 1 cold open and match M-546, M-539, M-545, M-547, M-554, M-548 (paraphrase OK).  
   - Missed collapse = death / collection: Day pages state death on miss (decision 026); aligns with M-650-class claims / Caleb ruling. Do not reintroduce Reprieve for missed collapse.  
   - Saferooms: Z6 through Day 3, Z9 to end — house/inspired, labeled as such; F2+ one-hour saferoom close is M-012 (not a F1 contradiction).  
   - **No hard cold-open fact contradiction found**; remaining issues are voice tags and Death Mode naming.

### Rewrite timing note
- Live play files (`.md`/`.json`) last written **2026-10-05 ~13:26 CT**.  
- Spec rewrites (`.spec.json`) last written **2026-10-05 ~13:48 CT** — ~22 minutes later; already applying dry notice + `gm_color` on collapse.  
- Overview still **2026-10-04 22:14 CT** — predates today's voice split and still owns the Death Mode section.

---

## Follow-ups (not done here)
- Encounter Bot: finish propagating `.spec.json` voice split into `.json`/`.md`; scrub Death Mode player-facing strings.  
- Syndicate: rename or retire Death Mode UI if the table keeps Costly Revives as fees-only.  
- Lore: optional Day 1 achievement-suggestion pass (Hold Please etc. already framed [GM] in collapse-notices v0.2).
