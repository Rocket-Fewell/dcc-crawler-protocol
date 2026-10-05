# Decision 016: S12 dropped (no public Fan Profile tags screen)
Owner: Syndicate | Status: final | Version: 1.0 | Updated: 2026-10-04
Summary: The /create screen that asked players to pick public Fan Profile tags (S12) is dropped. The Fan Profile is hidden and is built by the System from the private S13 survey and from play.

- Decided by: Caleb, 2026-10-04.
- Screen S12 is retired and intentionally skipped. Screen numbers stay stable (no renumbering): 16 active screens, S1-S17 with S12 retired. See characters/create-flow-spec-5e.md v0.1.2 and its change log.
- Players never see or pick Fan Profile tags. Story Box tailoring uses the hidden profile only for the item's reskin and hook, never its power (rules/45 §5.3). `tailor_tags` on cards carry broad themes, never survey text.
- Tooling that handled `fan_profile.public_tags[]` or the `Fan tags:` card line is to be removed (create-flow spec §7 item 9; Architect).
- Wording in rules/40 §1.1 and §2.4 was changed to "hidden Fan Profile" in rules/40 v0.1.4.
