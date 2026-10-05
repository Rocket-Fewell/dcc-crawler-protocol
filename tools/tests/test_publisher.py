import copy, json, os, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import publisher as pub  # noqa: E402

GID, BOT, EVERYONE = "9000000000000000001", "9000000000000000002", "9000000000000000001"


def jdump(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f)


class FakeDiscord:
    """Records requests; answers the handful of endpoints the publisher uses."""

    def __init__(self, base_perms=pub.P_MANAGE_CHANNELS, fail_posts=0):
        self.calls, self.base, self.fail_posts, self.channels, self.n = [], base_perms, fail_posts, [], 100

    def request(self, method, path, body=None):
        self.calls.append((method, path, body))
        if path == "/users/@me":
            return {"id": BOT, "username": "GM"}
        if path.startswith(f"/guilds/{GID}/members/"):
            return {"roles": ["r1"]}
        if path == f"/guilds/{GID}/roles":
            return [{"id": EVERYONE, "permissions": "0"}, {"id": "r1", "permissions": str(self.base)}]
        if method == "GET" and path == f"/guilds/{GID}/channels":
            return list(self.channels)
        if method == "POST" and path == f"/guilds/{GID}/channels":
            self.n += 1
            ch = {"id": f"70000000000000{self.n}", "guild_id": GID, "type": body["type"], "name": body["name"],
                  "parent_id": body.get("parent_id"), "permission_overwrites": body.get("permission_overwrites", [])}
            self.channels.append(ch)
            return ch
        if method == "GET" and path.startswith("/channels/"):
            cid = path.split("/")[2]
            for ch in self.channels:
                if ch["id"] == cid:
                    return ch
            return {"id": cid, "guild_id": GID, "type": 0, "name": "x", "permission_overwrites": []}
        if method == "POST" and path.endswith("/messages"):
            if self.fail_posts:
                self.fail_posts -= 1
                raise pub.DiscordError(500, "boom")
            self.n += 1
            return {"id": str(self.n)}
        raise AssertionError(f"unexpected {method} {path}")

    def posts(self):
        return [c for c in self.calls if c[0] == "POST" and c[1].endswith("/messages")]


def crawler(name, player, credits=10, inv=None):
    return {"name": name, "player": player, "class": "Wizard", "species": "Human", "level": 1, "xp": 0,
            "hp": {"current": 8, "max": 8, "temp": 0}, "ac": 11, "hit_dice": {"current": 1, "max": 1},
            "abilities": {"str": 10, "dex": 10, "con": 10, "int": 10, "wis": 10, "cha": 10}, "credits": credits,
            "conditions": [], "boxes": {}, "inventory": inv if inv is not None else [{"name": "Rope", "qty": 1}],
            "achievements": [], "fan_profile": "SECRET-DO-NOT-LEAK", "notes": "GM-ONLY"}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        os.makedirs(os.path.join(self.dir, "sessions"))
        os.makedirs(os.path.join(self.dir, "exports"))
        self._env = {k: os.environ.get(k) for k in ("DCC_CAMPAIGN_DIR", "PLAYER_CHANNELS_FILE")}
        os.environ["DCC_CAMPAIGN_DIR"] = self.dir
        os.environ.pop("PLAYER_CHANNELS_FILE", None)
        self.state = {"campaign": {}, "crawlers": [crawler("Horn", "Hornn", 75), crawler("Bone Wifebeater", "Trailer Park Moses", 127)]}
        self.write_state()
        jdump({"items": {"rope": {"category": "gear", "mechanics": "Rope, 50 ft."}}}, os.path.join(self.dir, "exports", "card-data.json"))

    def tearDown(self):
        for k, v in self._env.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
        self.tmp.cleanup()

    def write_state(self):
        jdump(self.state, pub.state_path())

    def map_channels(self):
        jdump({"guild_id": GID, "category_name": "Crawler Sheets", "crawlers": {
            "Horn": {"channel_id": "111111111111111111", "channel_name": "hornn-sheet", "players": ["Hornn", "Caleb"]},
            "Bone Wifebeater": {"channel_id": "222222222222222222", "channel_name": "moses-sheet", "players": ["Moses"]}}},
            pub.channels_path())


class PublishTests(Base):
    def test_first_publish_posts_full_card_to_each_channel_then_nothing(self):
        self.map_channels()
        fd = FakeDiscord()
        res = pub.publish(fd, log=lambda m: None)
        self.assertEqual([r["status"] for r in res], ["posted", "posted"])
        chans = {c[1] for c in fd.posts()}
        self.assertEqual(chans, {"/channels/111111111111111111/messages", "/channels/222222222222222222/messages"})
        text = "\n".join(c[2]["content"] for c in fd.posts())
        self.assertIn("Credits: 75", text)
        self.assertIn("Rope, 50 ft.", text)
        self.assertNotIn("SECRET-DO-NOT-LEAK", text)
        self.assertNotIn("GM-ONLY", text)
        self.assertTrue(all(c[2]["allowed_mentions"] == {"parse": []} for c in fd.posts()))
        fd2 = FakeDiscord()
        res = pub.publish(fd2, log=lambda m: None)
        self.assertEqual([r["status"] for r in res], ["unchanged", "unchanged"])
        self.assertEqual(fd2.posts(), [])

    def test_change_posts_one_card_with_credit_line_first(self):
        self.map_channels()
        pub.publish(FakeDiscord(), log=lambda m: None)
        self.state["crawlers"][0]["credits"] = 125
        self.write_state()
        with open(pub.ledger_path(), "w") as f:
            f.write(json.dumps({"crawler": "Horn", "delta": 50, "balance": 125, "reason": "Bronze box"}) + "\n")
        fd = FakeDiscord()
        pub.publish(fd, log=lambda m: None)
        self.assertEqual(len(fd.posts()), 1)
        self.assertEqual(fd.posts()[0][2]["content"].splitlines()[0], "Credits: 125 (+50, Bronze box)")
        self.assertNotIn("**Changed:**", fd.posts()[0][2]["content"])  # credits-only change: the first line says it all

    def test_diff_without_ledger_uses_snapshot_delta_and_full_flag_forces(self):
        self.map_channels()
        pub.publish(FakeDiscord(), log=lambda m: None)
        self.state["crawlers"][1]["hp"]["current"] = 3
        self.state["crawlers"][1]["credits"] = 100
        self.write_state()
        fd = FakeDiscord()
        pub.publish(fd, ["Moses"], log=lambda m: None)  # player alias
        self.assertEqual(len(fd.posts()), 1)
        first = fd.posts()[0][2]["content"]
        self.assertTrue(first.startswith("Credits: 100 (-27)"))
        self.assertIn("HP 8/8 -> 3/8", first)
        fd3 = FakeDiscord()
        pub.publish(fd3, ["Horn"], full=True, log=lambda m: None)
        self.assertEqual(len(fd3.posts()), 1)

    def test_failed_post_keeps_old_snapshot_so_it_retries(self):
        self.map_channels()
        res = pub.publish(FakeDiscord(fail_posts=1), log=lambda m: None)
        self.assertTrue(res[0]["status"].startswith("failed"))
        self.assertEqual(res[1]["status"], "posted")
        snaps = json.load(open(pub.snapshots_path()))
        self.assertNotIn("Horn", snaps["crawlers"])
        self.assertIn("Bone Wifebeater", snaps["crawlers"])
        fd = FakeDiscord()
        pub.publish(fd, log=lambda m: None)
        self.assertEqual(len(fd.posts()), 1)

    def test_dry_run_posts_nothing_and_writes_no_snapshot(self):
        self.map_channels()
        fd = FakeDiscord()
        res = pub.publish(fd, dry_run=True, log=lambda m: None)
        self.assertEqual(fd.calls, [])
        self.assertEqual(res[0]["status"], "dry-run")
        self.assertFalse(os.path.exists(pub.snapshots_path()))

    def test_unmapped_crawler_is_reported_not_posted(self):
        fd = FakeDiscord()
        res = pub.publish(fd, log=lambda m: None)
        self.assertEqual({r["status"] for r in res}, {"no-channel"})
        self.assertEqual(fd.calls, [])

    def test_long_card_splits_under_limit(self):
        inv = [{"name": f"Item {i}", "qty": 1, "notes": "x" * 150} for i in range(40)]
        self.state["crawlers"][0]["inventory"] = inv
        self.write_state()
        self.map_channels()
        fd = FakeDiscord()
        pub.publish(fd, ["Horn"], log=lambda m: None)
        msgs = [c[2]["content"] for c in fd.posts()]
        self.assertGreater(len(msgs), 2)
        self.assertTrue(all(len(m) < 2000 for m in msgs))
        self.assertTrue(msgs[1].startswith("*Horn card, part 2/"))
        for i in range(40):
            self.assertIn(f"Item {i}**", "\n".join(msgs))

    def test_pack_messages_splits_one_giant_line(self):
        out = pub.pack_messages(["word " * 1000], "X")
        self.assertTrue(all(len(m) < 2000 for m in out) and len(out) > 2)


class ChannelSetupTests(Base):
    def test_setup_creates_category_and_channels_with_locked_down_permissions(self):
        fd = FakeDiscord()
        out = pub.setup_channels(fd, log=lambda m: None)
        self.assertEqual([c["channel_name"] for c in out["created"]], ["hornn-horn", "trailer-park-moses-bone-wifebeater"])
        cfg = json.load(open(pub.channels_path()))
        self.assertTrue(cfg["category_id"])
        self.assertEqual(cfg["crawlers"]["Horn"]["channel_id"], out["created"][0]["channel_id"])
        ch = fd.channels[1]
        ow = {o["id"]: o for o in ch["permission_overwrites"]}
        ev, bot = ow[GID], ow[BOT]
        self.assertTrue(int(ev["deny"]) & pub.P_SEND)
        self.assertFalse(int(ev["allow"]) & pub.P_SEND)
        self.assertTrue(int(ev["allow"]) & pub.P_VIEW)
        self.assertTrue(int(bot["allow"]) & pub.P_SEND)
        # rerun creates nothing more
        n = len(fd.channels)
        pub.setup_channels(fd, log=lambda m: None)
        self.assertEqual(len(fd.channels), n)

    def test_setup_without_manage_channels_creates_nothing_and_explains(self):
        fd = FakeDiscord(base_perms=pub.P_SEND)
        lines = []
        out = pub.setup_channels(fd, log=lines.append)
        self.assertFalse(out["can_manage"])
        self.assertEqual(fd.channels, [])
        self.assertTrue(any("register-channel" in l for l in lines))
        self.assertTrue(any("Manage Channels" in l for l in lines))

    def test_setup_dry_run_creates_nothing(self):
        fd = FakeDiscord()
        out = pub.setup_channels(fd, dry_run=True, log=lambda m: None)
        self.assertEqual(fd.channels, [])
        self.assertIn("plan", out)

    def test_register_channel_validates_access_and_rejects_voice_channels(self):
        fd = FakeDiscord(base_perms=pub.P_VIEW | pub.P_SEND | pub.P_HISTORY)
        pub.register_channel(fd, "Moses", "333333333333333333", log=lambda m: None)
        self.assertEqual(json.load(open(pub.channels_path()))["crawlers"]["Bone Wifebeater"]["channel_id"], "333333333333333333")
        with self.assertRaises(pub.PublishError):
            pub.register_channel(fd, "Horn", "1556163836879568946", log=lambda m: None)   # #gm-voice (was #dcc_mouth)
        with self.assertRaises(pub.PublishError):
            pub.register_channel(fd, "Horn", "1556163778788462602", log=lambda m: None)   # #table-transcript (was #dcc_ears)
        with self.assertRaises(pub.PublishError):
            pub.register_channel(fd, "Horn", "333333333333333333", log=lambda m: None)    # already used
        with self.assertRaises(pub.PublishError):
            pub.register_channel(fd, "Horn", "abc", log=lambda m: None)
        lacking = FakeDiscord(base_perms=pub.P_VIEW)
        with self.assertRaises(pub.PublishError):
            pub.register_channel(lacking, "Horn", "444444444444444444", log=lambda m: None)

    def test_channel_perms_overwrite_math(self):
        ow = [{"id": GID, "type": 0, "allow": "0", "deny": str(pub.P_SEND)}, {"id": BOT, "type": 1, "allow": str(pub.P_SEND), "deny": "0"}]
        base = pub.P_VIEW | pub.P_SEND
        self.assertFalse(pub.channel_perms(base, ow[:1], GID, "5", []) & pub.P_SEND)
        self.assertTrue(pub.channel_perms(base, ow, GID, BOT, []) & pub.P_SEND)


class AutoPublishTests(Base):
    def test_state_change_never_fails_without_token_or_channels(self):
        import state
        old = os.environ.pop("GM_DISCORD_TOKEN", None)
        try:
            state.auto_publish()  # must be a silent no-op
        finally:
            if old is not None:
                os.environ["GM_DISCORD_TOKEN"] = old


if __name__ == "__main__":
    unittest.main()
