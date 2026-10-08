"""publisher.diff_views / views_differ (Oct 7 2026): HP, conditions, item counts, pet HP, death saves, class resources and
proficiencies must each trigger a card update; older snapshots missing keys must neither crash nor force a repost."""
import copy
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import publisher as pub  # noqa: E402


def crawler(**kw):
    c = {"name": "Mr. White", "player": "Moses", "class": "Monk", "species": "Human", "level": 1, "xp": 0,
         "hp": {"current": 11, "max": 11, "temp": 0}, "ac": 15, "hit_dice": {"current": 1, "max": 1},
         "abilities": {"str": 10, "dex": 16, "con": 12, "int": 10, "wis": 14, "cha": 8}, "credits": 11,
         "conditions": [], "boxes": {}, "inventory": [{"name": "Rope", "qty": 1}, {"name": "Potion of Healing", "qty": 2}],
         "achievements": [], "death_saves": {"successes": 0, "fails": 0}}
    c.update(kw)
    return c


class DiffTests(unittest.TestCase):
    def views(self, edit, base=None):
        c = base or crawler()
        old = pub.make_view(c, {})
        c2 = copy.deepcopy(c)
        edit(c2)
        new = pub.make_view(c2, {})
        return old, new, pub.diff_views(old, new), pub.views_differ(old, new)

    def test_hp_current_max_and_temp_changes(self):
        _, _, ch, d = self.views(lambda c: c["hp"].update(current=2))
        self.assertEqual(ch, ["HP 11/11 -> 2/11"])
        self.assertTrue(d)
        _, _, ch, _ = self.views(lambda c: c["hp"].update(current=0))
        self.assertIn("HP 11/11 -> 0/11", ch)
        _, _, ch, _ = self.views(lambda c: c["hp"].update(temp=4))
        self.assertEqual(ch, ["HP 11/11 -> 11/11 (+4 temp)"])
        _, _, ch, _ = self.views(lambda c: c["hp"].update(max=13))
        self.assertEqual(ch, ["HP 11/11 -> 11/13"])

    def test_snapshot_without_hp_temp_is_not_a_change_but_a_real_change_is(self):
        old, new, _, _ = self.views(lambda c: None)
        del old["hp"]["temp"]
        self.assertEqual(pub.diff_views(old, new), [])
        self.assertFalse(pub.views_differ(old, new))
        new["hp"]["current"] = 5
        self.assertEqual(pub.diff_views(old, new), ["HP 11/11 -> 5/11"])

    def test_conditions_add_remove_case_and_order(self):
        base = crawler(conditions=["Prone"])
        _, _, ch, _ = self.views(lambda c: c["conditions"].extend(["Unconscious", "Stable"]), base)
        self.assertEqual(ch, ["Condition: +Unconscious", "Condition: +Stable"])
        _, _, ch, d = self.views(lambda c: c["conditions"].remove("Prone"), crawler(conditions=["Prone"]))
        self.assertEqual(ch, ["Condition: -Prone"])
        self.assertTrue(d)
        _, _, ch, d = self.views(lambda c: c.update(conditions=["Stable", "Unconscious"]), crawler(conditions=["Unconscious", "Stable"]))
        self.assertEqual((ch, d), ([], False))   # order only: nothing visible changed
        _, _, ch, d = self.views(lambda c: c.update(conditions=["Poisoned (1 hr)"]), crawler(conditions=["Poisoned"]))
        self.assertEqual(ch, ["Condition: +Poisoned (1 hr)", "Condition: -Poisoned"])

    def test_item_counts_and_uses(self):
        _, _, ch, _ = self.views(lambda c: c["inventory"][1].update(qty=1))
        self.assertEqual(ch, ["Potion of Healing: x2 -> x1"])
        _, _, ch, _ = self.views(lambda c: c["inventory"].pop(1))
        self.assertEqual(ch, ["- Potion of Healing"])
        base = crawler(inventory=[{"name": "Healer's Kit", "qty": 1, "uses": 10, "uses_max": 10, "uses_reset": "never"}])
        _, _, ch, _ = self.views(lambda c: c["inventory"][0].update(uses=9), base)
        self.assertEqual(ch, ["Healer's Kit: uses 10 -> 9"])

    def test_death_saves_and_missing_vs_zero(self):
        _, _, ch, _ = self.views(lambda c: c["death_saves"].update(fails=1))
        self.assertEqual(ch, ["Death saves 0 successes / 1 fails"])
        old, new, _, _ = self.views(lambda c: None)
        old["death_saves"] = None   # a crawler written before the field: same as 0/0
        self.assertEqual(pub.diff_views(old, new), [])
        self.assertFalse(pub.views_differ(old, new))

    def test_pet_hp_change_gets_its_own_line(self):
        base = crawler(pet={"name": "Turbo", "species": "Wolf", "species_srd_id": "wolf", "cr": 0.25, "status": "alive", "hp_current": 11, "hp_max": 11})
        _, _, ch, d = self.views(lambda c: c["pet"].update(hp_current=4), base)
        self.assertEqual(ch, ["Pet Turbo HP 11 -> 4/11"])
        self.assertTrue(d)
        _, _, ch, _ = self.views(lambda c: c["pet"].update(status="dead"), base)
        self.assertEqual(ch, ["Pet: -Turbo"])

    def test_resources_and_proficiencies(self):
        base = crawler(resources=[{"name": "Second Wind", "uses": 2, "uses_max": 2, "uses_reset": "short_rest"}], proficiencies=["Acrobatics"])
        _, _, ch, _ = self.views(lambda c: c["resources"][0].update(uses=1), base)
        self.assertEqual(ch, ["Second Wind: 2/2 per short rest -> 1/2 per short rest"])
        _, _, ch, _ = self.views(lambda c: c["resources"].append({"name": "Focus", "uses": 1, "uses_max": 1, "uses_reset": "short_rest"}), base)
        self.assertEqual(ch, ["+ Resource Focus 1/1 per short rest"])
        _, _, ch, _ = self.views(lambda c: c["proficiencies"].append("Stealth"), base)
        self.assertEqual(ch, ["Proficiency: +Stealth"])

    def test_snapshot_from_before_new_keys_never_forces_a_repost_or_crashes(self):
        c = crawler(resources=[{"name": "Second Wind", "uses": 2, "uses_max": 2, "uses_reset": "short_rest"}], proficiencies=["Acrobatics"])
        new = pub.make_view(c, {})
        old = copy.deepcopy(new)
        for k in ("resources", "proficiencies", "expertise", "conditions", "death_saves", "pet", "hit_dice", "boxes"):
            old.pop(k, None)
        self.assertEqual(pub.diff_views(old, new), [])
        self.assertFalse(pub.views_differ(old, new))
        old.pop("hp")
        old.pop("inventory")
        pub.diff_views(old, new)   # must not raise


class PublishEndToEnd(unittest.TestCase):
    """A state.py-style HP/condition edit reposts the card through publish() (no Discord: a fake client)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        os.makedirs(os.path.join(self.tmp.name, "sessions"))
        p = mock.patch.dict(os.environ, {"DCC_CAMPAIGN_DIR": self.tmp.name, "DCC_CAMPAIGN_ROOT": self.tmp.name, "DCC_SESSION": "alpha"})
        p.start()
        self.addCleanup(p.stop)
        os.environ.pop("PLAYER_CHANNELS_FILE", None)
        self.state = {"campaign": {}, "crawlers": [crawler()]}
        self.save()
        with open(pub.channels_path(), "w") as f:
            json.dump({"guild_id": "1", "crawlers": {"Mr. White": {"channel_id": "222222222222222222"}}}, f)

    def save(self):
        with open(pub.state_path(), "w") as f:
            json.dump(self.state, f)

    def publish(self):
        posts = []

        class Fake:
            def request(self, method, path, body=None):
                posts.append(body["content"])
                return {"id": str(len(posts))}
        return pub.publish(Fake(), log=lambda m: None)[0], posts

    def test_hp_then_conditions_then_death_saves_each_repost(self):
        self.assertEqual(self.publish()[0]["status"], "posted")
        self.assertEqual(self.publish()[0]["status"], "unchanged")
        self.state["crawlers"][0]["hp"]["current"] = 0
        self.save()
        res, posts = self.publish()
        self.assertEqual((res["status"], res["changes"]), ("posted", ["HP 11/11 -> 0/11"]))
        self.assertIn("Death saves: 0 successes / 0 fails", "\n".join(posts))
        self.state["crawlers"][0]["conditions"] = ["Unconscious"]
        self.save()
        self.assertEqual(self.publish()[0]["changes"], ["Condition: +Unconscious"])
        self.state["crawlers"][0]["death_saves"]["fails"] = 2
        self.save()
        self.assertEqual(self.publish()[0]["changes"], ["Death saves 0 successes / 2 fails"])


if __name__ == "__main__":
    unittest.main()
