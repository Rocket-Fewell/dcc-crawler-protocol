#!/usr/bin/env python3
"""Scaffold a fresh campaign session (e.g. beta) next to the live one. Never touches alpha and refuses to overwrite.

  python3 tools/new-session.py beta --label "Beta table" [--guild ID --ears ID --mouth ID --voice ID]
                               [--review hold|notify|off] [--staff-channel ID] [--floor 1]

Creates sessions-data/<id>/ with: empty state (state.py init), a NEW sealed GM quirk roll + zeroed affinity under
gm-notes/secret/sessions/<id>/, empty ledgers, session.json (no secrets), characters/ (+INDEX.md) and create-drafts/.
It does NOT switch the bridge: use `/session use <id>` (leave voice first). Discord channels: run
`python3 tools/discord_gm.py --session <id> setup-channels` once the guild id is in session.json.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import campaign_session as cs  # noqa: E402


def run(*args, env=None):
    r = subprocess.run([sys.executable, os.path.join(HERE, "state.py"), *args], capture_output=True, text=True, env=env)
    if r.returncode:
        sys.exit(f"state.py {' '.join(args)} failed: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id")
    ap.add_argument("--label", default="")
    ap.add_argument("--guild")
    ap.add_argument("--ears")
    ap.add_argument("--mouth")
    ap.add_argument("--voice")
    ap.add_argument("--review", choices=["hold", "notify", "off"], default="hold")
    ap.add_argument("--staff-channel")
    ap.add_argument("--no-roll", action="store_true", help="write create.allow_roll=false (the Roll ability method is ON by default, decision 024)")
    ap.add_argument("--floor", default="1")
    ap.add_argument("--fish-monthly-minutes", type=int, default=100)
    a = ap.parse_args(argv)
    sid = a.id.strip().lower()
    if sid == "alpha" or not cs.valid_id(sid):
        sys.exit("session id must be a-z, 0-9, _ or - (and not 'alpha', which is the live game)")
    env = dict(os.environ, DCC_AUTO_PUBLISH="0")
    env.pop("DCC_SESSION", None)
    data = os.path.join(cs.campaign_dir(), "sessions-data", sid)
    if os.path.exists(os.path.join(data, "state.json")) or os.path.exists(os.path.join(data, "session.json")):
        sys.exit(f"session '{sid}' already exists at {data}; refusing to overwrite (move or delete it by hand)")
    for sub in ("", "characters", "create-drafts"):
        os.makedirs(os.path.join(data, sub), exist_ok=True)
    out = [f"created {data}"]
    run("--session", sid, "init", "--floor", str(a.floor), env=env)
    out.append("state.json initialised (Costly Revives, Ludicrous defaults, max_crawlers 4, Story Boxes on: limits.legendary_enabled true, cap 1 per floor)")
    run("--session", sid, "gm-quirks", "roll", env=env)
    out.append("sealed GM quirk roll + zeroed affinity written (gm-notes/secret/sessions/%s/); nothing printed" % sid)
    for f in ("credit-ledger.jsonl", "box-ledger.jsonl", "loot-ledger.jsonl", "banner-archive.jsonl", "story-box-ledger.jsonl"):
        open(os.path.join(data, f), "a").close()
    profile = {"label": a.label or sid.capitalize(), "env_prefix": sid.upper() + "_",
               "fish_monthly_minutes": a.fish_monthly_minutes,
               "create": {"review_mode": a.review, "allow_roll": not a.no_roll, "content_source": "phb", "staff_channel_id": a.staff_channel, "reviewer_ids": []}}
    for k, v in (("guild_id", a.guild), ("ears_channel_id", a.ears), ("mouth_channel_id", a.mouth), ("voice_channel_id", a.voice)):
        if v:
            profile[k] = v
    with open(os.path.join(data, "session.json"), "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
    idx = os.path.join(data, "characters", "INDEX.md")
    with open(idx, "w", encoding="utf-8") as f:
        f.write(f"# characters index (session {sid})\nOwner: see NAMING-CONVENTIONS.md | Updated: {__import__('datetime').date.today()}\n\n")
    out.append("session.json written (no secrets). Secrets go in .env as %sGM_WEBHOOK_URL / %sGM_WEBHOOK_KEY / %sGM_DISCORD_TOKEN" % ((profile["env_prefix"],) * 3))
    out.append("next: set guild/channel ids in session.json, `discord_gm.py --session %s setup-channels`, then `/session use %s` in Discord" % (sid, sid))
    print("\n".join(out))


if __name__ == "__main__":
    main()
