"""Shooting Gallery slice. Dice are scripted. Nothing is written under sessions/."""

import json
import sys
import unittest
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine"))
sys.path.insert(0, str(ROOT / "tools"))

from dcc_engine.cards import load_monster  # noqa: E402
from dcc_engine.clauses import classify, split_clauses  # noqa: E402
from dcc_engine.server import serve_background  # noqa: E402
from dcc_engine.table import ScriptedRng, Table  # noqa: E402
import roll  # noqa: E402


def _say(table, text, dice):
    return table.resolve_line(text, rng=ScriptedRng(dice))


class SplitTests(unittest.TestCase):
    def test_compound_sentence_splits_left_to_right(self):
        parts = split_clauses(
            "I get behind the sandbags, then I shoot the first mannequin, and I yell"
        )
        self.assertEqual(parts, [
            "I get behind the sandbags",
            "I shoot the first mannequin",
            "I yell",
        ])

    def test_body_swing_is_two_clauses(self):
        parts = split_clauses("I pick up the body and swing it at the other mannequin")
        self.assertEqual(
            [classify(part, held="body" if index else None)["kind"] for index, part in enumerate(parts)],
            ["object", "ruling"],
        )


class GalleryTests(unittest.TestCase):
    def setUp(self):
        self.table = Table(party_size=2)
        self.calls = []
        self._append = roll.append_log
        roll.append_log = lambda *args, **kwargs: self.calls.append(1)

    def tearDown(self):
        roll.append_log = self._append

    def test_mannequin_to_hit_comes_from_the_card(self):
        card = load_monster("f01-m-09")
        shortbow = next(item for item in card["local"]["attacks"] if item["name"] == "Shortbow")
        self.assertEqual(shortbow["to_hit"], 5)
        self.assertEqual(shortbow["damage"]["dice"], "1d6+3")
        enemy = self.table.enemies[0]
        self.assertEqual(enemy["ranged"]["to_hit"], 5)
        self.assertEqual(enemy["hp"], 13)
        self.assertEqual(len(self.table.enemies), 2)

    def test_shot_updates_hit_points_and_names_the_second_action(self):
        result = _say(
            self.table,
            "I shoot the first mannequin, then I hide, then I yell",
            [15, 4],
        )
        text = " ".join(line["text"] for line in result["say"])
        self.assertIn("Eldritch Blast", text)
        self.assertIn("1d20+6", text)
        self.assertIn("1d10", text)
        self.assertEqual(self.table.enemies[0]["hp"], 9)
        self.assertIn("Did not happen", text)
        self.assertIn("yell", text.lower())
        self.assertFalse(self.table.crawler["action"])
        self.assertEqual(self.calls, [])

    def test_cunning_action_refused_at_rogue_1_and_the_shot_still_happens(self):
        self.assertEqual(self.table.crawler["name"], "Raithen")
        self.assertEqual(self.table.crawler["class_name"], "Warlock")
        self.assertEqual(self.table.crawler["level"], 1)
        _say(self.table, "I cunning action hide, then I cast eldritch blast at the first mannequin", [15, 4])
        system = " ".join(line["text"] for line in self.table.log)
        self.assertIn("Cunning Action starts at Rogue 2", system)
        self.assertEqual(self.table.enemies[0]["hp"], 9)
        self.assertFalse(self.table.crawler["hidden"])

    def test_cover_then_attack_spends_movement_and_the_action(self):
        _say(self.table, "I get behind the sandbags, then I cast eldritch blast at the first mannequin", [15, 4])
        self.assertEqual(self.table.crawler["cover"], "half")
        self.assertEqual(self.table.crawler["movement_left"], 15)
        self.assertEqual(self.table.enemies[0]["hp"], 9)
        self.assertIn("costs nothing", " ".join(
            line["text"] for line in _say(self.table, "I yell", [])["say"]
        ).lower())

    def test_swinging_the_body_is_a_ruling_then_a_bludgeoning_roll(self):
        _say(self.table, "I pick up the body and swing it at the other mannequin", [18, 2])
        self.assertEqual(self.table.held, "body")
        self.assertFalse(self.table.crawler["object"])
        other = self.table.enemies[1]
        self.assertEqual(other["hp"], 9)
        spoken = " ".join(line["text"] for line in self.table.log)
        self.assertIn("1d20-2", spoken)
        self.assertIn("Vulnerable to bludgeoning", spoken)
        self.assertEqual(self.table.enemies[0]["hp"], 13)

    def test_undo_restores_hit_points(self):
        _say(self.table, "I shoot the first mannequin", [15, 4])
        self.assertEqual(self.table.enemies[0]["hp"], 9)
        self.table.undo()
        self.assertEqual(self.table.enemies[0]["hp"], 13)
        self.assertTrue(self.table.crawler["action"])
        self.assertTrue(any("undone" in line["text"].lower() for line in self.table.log))

    def test_correction_sets_hit_points_without_a_roll(self):
        view = self.table.correct_hp("ms-1", 1)
        self.assertEqual(view["enemies"][0]["hp"], 1)
        self.assertTrue(any(line["text"].startswith("[SYSTEM] Correction:") for line in view["log"]))

    def test_question_does_not_spend_the_turn(self):
        before = self.table.enemies[0]["hp"]
        _say(self.table, "can I shoot the mannequin?", [])
        self.assertEqual(self.table.enemies[0]["hp"], before)
        self.assertEqual(self.table.resolutions, 0)
        self.assertTrue(self.table.crawler["action"])

    def test_enemy_shortbow_uses_the_card_bonus(self):
        _say(self.table, "I end turn", [10, 3, 1])
        spoken = " ".join(line["text"] for line in self.table.log)
        self.assertIn("1d20+5", spoken)
        self.assertEqual(self.table.crawler["hp"], 6)
        self.assertEqual(self.table.round, 2)
        self.assertTrue(self.table.crawler["action"])

    def test_player_view_hides_the_gm_note(self):
        self.assertNotIn("gm_note", self.table.player_view())
        self.assertIn("gm_note", self.table.gm_view())

    def test_rogue_2_hide_is_a_bonus_and_the_shot_is_the_action(self):
        self.table.crawler["class_name"] = "Rogue"
        self.table.crawler["level"] = 2
        _say(
            self.table,
            "I cunning action hide, then I shoot the first mannequin",
            [12, 18, 3, 4],
        )
        self.assertIn("Stealth", " ".join(line["text"] for line in self.table.log))
        self.assertFalse(self.table.crawler["bonus"])
        self.assertFalse(self.table.crawler["action"])
        self.assertEqual(self.table.enemies[0]["hp"], 9)

    def test_card_copy_is_raithen_and_hides_secrets(self):
        view = self.table.player_view()
        text = view["crawler"]["card_text"]
        self.assertIn("**RAITHEN**", text)
        self.assertIn("Eldritch Blast**: +6 to hit, 1d10 force", text)
        self.assertIn("Pact Magic slots: 1/1", text)
        self.assertIn("Credits: 100", text)
        self.assertIn("Duct-Taped Mop", text)
        self.assertNotIn("pupils", text.lower())
        self.assertNotIn("ducky", text.lower())
        enemy = view["enemies"][0]
        self.assertEqual(enemy["hp"], 13)
        self.assertIn("Level 1", enemy["nameplate"])
        self.assertNotIn("attacks", enemy)
        self.assertNotIn("card", enemy)
        self.assertNotIn("ac", enemy)
        self.assertNotIn("how_to_cheese", enemy)
        table_enemy = self.table.gm_view()["enemies"][0]
        self.assertEqual(table_enemy["attacks"][0]["name"], "Shortbow")
        self.assertEqual(table_enemy["attacks"][0]["to_hit"], 5)
        self.assertIn("how_to_cheese", table_enemy)

    def test_mop_is_bludgeoning_and_the_mannequin_card_doubles_it(self):
        _say(self.table, "I swing the mop at the first mannequin", [16, 6])
        self.assertEqual(self.table.enemies[0]["hp"], 5)
        spoken = " ".join(line["text"] for line in self.table.log)
        self.assertIn("1d20+0", spoken)
        self.assertIn("Vulnerable to bludgeoning", spoken)
        self.assertIn("doubled to 8", spoken)

    def test_witch_bolt_spends_the_pact_slot_on_the_card(self):
        _say(self.table, "I cast witch bolt at the first mannequin", [16, 6, 6])
        self.assertEqual(self.table.enemies[0]["hp"], 1)
        text = self.table.player_view()["crawler"]["card_text"]
        self.assertIn("Pact Magic slots: 0/1", text)
        self.assertIn("2d12", " ".join(line["text"] for line in self.table.log))

    def test_full_cards_reach_the_player_and_cheese_stays_on_the_table(self):
        view = self.table.player_view()
        titles = [section["title"] for section in view["crawler"]["card_sections"]]
        for title in (
            "Attacks",
            "Spellcasting",
            "Features & traits",
            "Rests",
            "Gear",
            "Achievements",
            "Standing Orders",
        ):
            self.assertIn(title, titles)
        gear = next(section["text"] for section in view["crawler"]["card_sections"] if section["title"] == "Gear")
        self.assertIn("Extension Cord", gear)
        self.assertIn("Intake Bag", gear)
        achievements = next(section["text"] for section in view["crawler"]["card_sections"] if section["title"] == "Achievements")
        self.assertIn("Paperwork Survivor", achievements)
        self.assertEqual(
            view["crawler"]["card_text"],
            "\n".join(section["text"] for section in view["crawler"]["card_sections"]),
        )
        self.assertEqual(
            {spell["name"] for spell in view["crawler"]["spells"]},
            {"Witch Bolt", "Armor of Agathys", "Shield"},
        )
        enemy = view["enemies"][0]
        shown = json.dumps(enemy)
        self.assertIn("Behind the far counter.", enemy["where"])
        self.assertNotIn("Shortbow", shown)
        self.assertNotIn("Bludgeoning", shown)
        self.assertNotIn("Darkvision", shown)
        self.assertNotIn("how_to_cheese", enemy)
        self.assertNotIn("what_it_wants", enemy)
        self.assertNotIn("chair leg", shown.lower())
        self.assertIn("sandbags", " ".join(view["room_card"]["features"]))
        self.assertNotIn("room_gm", view)
        gm_enemy = self.table.gm_view()["enemies"][0]
        card = gm_enemy["card"]
        labels = {label["name"]: label["text"] for label in card["labels"]}
        self.assertEqual(labels["Vulnerabilities"], "Bludgeoning")
        self.assertIn("Darkvision 60 ft.", labels["Senses"])
        actions = {action["name"]: action["text"] for action in card["actions"]}
        self.assertIn("80/320", actions["Shortbow"])
        self.assertIn("1d6 + 3", actions["Shortsword"])
        self.assertEqual(card["abilities"][1]["key"], "dex")
        self.assertEqual(card["abilities"][1]["score"], 16)
        self.assertIn("chair leg", gm_enemy["how_to_cheese"].lower())
        self.assertIn("script", gm_enemy["what_it_wants"].lower())
        self.assertEqual(self.table.gm_view()["room_gm"]["audience"], "gm")


class HttpTests(unittest.TestCase):
    def test_player_page_and_gm_undo(self):
        httpd = serve_background("127.0.0.1", 0)
        self.addCleanup(httpd.shutdown)
        self.addCleanup(httpd.server_close)
        host, port = httpd.server_address[:2]
        base = f"http://{host}:{port}"

        page = urllib.request.urlopen(base + "/player").read().decode("utf-8")
        self.assertIn("Shooting Gallery", page)
        self.assertIn("What you do", page)
        self.assertNotIn("max-height: 380px", page)
        self.assertIn("overflow: hidden", page)
        self.assertIn('id="sheet"', page)
        self.assertNotIn("how_to_cheese", page)
        self.assertNotIn("chair leg", page.lower())
        self.assertNotIn("Vulnerabilities", page)
        self.assertNotIn("Attacks roll against", page)

        before = json.load(urllib.request.urlopen(base + "/api/player"))
        self.assertEqual(before["crawler"]["name"], "Raithen")
        self.assertIn("Eldritch Blast", before["crawler"]["card_text"])
        self.assertEqual(before["enemies"][0]["name"], "Smiling Polo Mannequin 1")
        self.assertEqual(before["enemies"][0]["hp"], 13)
        self.assertNotIn("attacks", before["enemies"][0])
        self.assertNotIn("card", before["enemies"][0])
        self.assertNotIn("gm_note", before)
        self.assertNotIn("how_to_cheese", before["enemies"][0])
        self.assertIn("Gear", [section["title"] for section in before["crawler"]["card_sections"]])

        httpd.scripts.append([15, 4])
        request = urllib.request.Request(
            base + "/api/line",
            data=json.dumps({"text": "I shoot the first mannequin"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        after = json.load(urllib.request.urlopen(request))
        self.assertEqual(after["view"]["enemies"][0]["hp"], 9)
        self.assertTrue(any(line["voice"] == "ROLL" and line["speak"] is False for line in after["say"]))
        self.assertTrue(any(line["voice"] == "GM" and line["speak"] is True for line in after["say"]))

        undone = json.load(urllib.request.urlopen(urllib.request.Request(base + "/api/undo", data=b"", method="POST")))
        self.assertEqual(undone["view"]["enemies"][0]["hp"], 13)
        gm = json.load(urllib.request.urlopen(base + "/api/gm"))
        self.assertIn("gm_note", gm)
        self.assertIn("I shoot the first mannequin", gm["raw"])
        self.assertEqual(gm["enemies"][0]["attacks"][0]["to_hit"], 5)
        self.assertEqual(
            next(label["text"] for label in gm["enemies"][0]["card"]["labels"] if label["name"] == "Vulnerabilities"),
            "Bludgeoning",
        )


if __name__ == "__main__":
    unittest.main()
