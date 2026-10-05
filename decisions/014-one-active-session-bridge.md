# Decision 014: One Active Session per Bridge (DRAFT, not yet approved)
Owner: Borent | Status: draft | Version: 0.1 | Updated: 2026-10-04
Summary: The Dungeon System AI - Earth (formerly DCC Ears) bridge serves one session at a time; alpha and beta never run voice together.

- `/session status|list|use` switches the active session (after `/leave`). GM tools follow the persisted active session unless `DCC_SESSION` is set; pin `DCC_SESSION=alpha` in the alpha GM routine.
- Per-session state under `sessions-data/<id>/`; alpha keeps `sessions/`. Usage rows carry `dcc_session`; wake budget and the monthly Fish share are per session.
- Story Boxes (Legendary) are per session: the per-floor cap and the deed registry live in each session's own ledgers (decision 015).
- Needs Caleb approval before it is cited as policy.
