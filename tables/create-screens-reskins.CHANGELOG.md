# create-screens-reskins CHANGELOG
Owner: DCC Lore | Status: draft | Version: 0.1 | Updated: 2026-10-04
Summary: One line per build of tables/create-screens-reskins.json and its companions (version, short sha256, entry count, diff).

- 2026-10-04 | v0.1.0 | sha256 352406d6346b | 188 entries | first build: S3/S4, S6 choices, S8 onward labels, texts, nav; 11 proposed create-flow-lines rewrites; +188 added, -0 removed, 0 renamed | proposed lines 11/38 keys
- 2026-10-04 | v0.1.1 | sha256 7a7562cbbdd5 | 192 entries | S8 head/method/base/preview lines; budget, min and max as placeholders where the bridge reads them from the tables; +4 added, -0 removed, 5 renamed | proposed lines 11/38 keys
- 2026-10-04 | v0.1.2 | sha256 4f189925d47c | 200 entries | v0.1.2: Syndicate audit F1-F12 applied (already line, plain views, S10 vocabulary, help-s16/title-s16, needs_code detail, nav-more, Cracked Phone App, bare method names, Restart vs Cancel, coverage gaps); +12 added, -4 removed, 25 renamed | proposed lines 10/38 keys
  - v0.1.2 delivery note (Syndicate F6): deliver the proposed lines through the bridge merge layer (mergeProposedLines); copying over create-flow-lines.json fails test/roll.test.js:249 and :308. Keys already and near_dup have no consumer in the bridge today. Needs_code: hint-s8-method-line ({method_label}), select-s8-assign ({ability_label}), plus every row (hook by id).
- 2026-10-04 | v0.1.3 | sha256 c0e7d1f5ab86 | 201 entries | v0.1.3: cp rule resolved (money-cp-rule), new row hint-money-cp, needs_code detail on both money rows; +1 added, -0 removed, 0 renamed | proposed lines 10/38 keys
  - v0.1.3 (Caleb approved the gp-note): cp rule resolved as audit row money-cp-rule; new row hint-money-cp ({amount} credits; n/100, whole credits without decimals); hint-money-gp unit word credit/credits. Needs_code: hint-money-cp ({amount}), package labels in background menu (see background-reskins meta.needs_code).
