"""C1 tests: rules, room graph, replay, stdio server."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(ROOT / "tools"))

from dcc_engine.model import ModelClient, iter_sentences, strong_model_name  # noqa: E402
from dcc_engine.rules import ScriptedRng, attack, cunning_action  # noqa: E402
from dcc_engine.rooms import load_room, resolve_room  # noqa: E402
from dcc_engine.schema import check_room, label_cut_off, narration_tokens  # noqa: E402
from dcc_engine.server import handle  # noqa: E402
from dcc_engine.store import Store  # noqa: E402
from dcc_engine.validate import validate_tree  # noqa: E402

FIX = ENGINE / "tests" / "fixtures"


def load(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


class RulesTests(unittest.TestCase):
    def test_cunning_action_refused_at_rogue_1(self):
        crawler = load("crawler-rogue.json")
        result = cunning_action(crawler, "dash")
        self.assertFalse(result["ok"])
        self.assertIn("Rogue 1", result["reason"])

    def test_one_mannequin_to_hit_and_scripted_dice(self):
        mannequin = load("mannequin-staff.json")
        crawler = load("crawler-rogue.json")
        script = load("dice-script.json")
        self.assertEqual(len({a["to_hit"] for a in mannequin["attacks"]}), 1)
        self.assertEqual(mannequin["attacks"][0]["to_hit"], 5)
        self.assertEqual(mannequin["ac"], 14)
        self.assertEqual(mannequin["attacks"][0]["damage"], "1d6+3")
        rng = ScriptedRng(script["rolls"])
        hit = attack(crawler, mannequin, rng)
        self.assertTrue(hit["hit"])
        self.assertEqual(hit["d20"], 18)
        self.assertEqual(hit["total"], 23)
        self.assertEqual(hit["damage"], 9)
        self.assertEqual(mannequin["hp"], 4)
        reply = attack(mannequin, crawler, rng)
        self.assertEqual(reply["to_hit"], 5)
        self.assertEqual(reply["d20"], 11)
        self.assertEqual(reply["total"], 16)
        self.assertTrue(reply["hit"])
        self.assertEqual(reply["damage"], 7)
        self.assertEqual(crawler["hp"], 3)
        self.assertEqual(rng.rolls, [])


class RoomTests(unittest.TestCase):
    def test_generated_floor_validates(self):
        errs = validate_tree(ENGINE / "data")
        self.assertEqual(errs, [], "\n".join(errs))

    def test_shooting_gallery_count_comes_from_budget(self):
        room = resolve_room(load_room("f01-z05"), 2)
        enc = room["encounters"][0]
        self.assertEqual(enc["count_ref"]["path"], "floors.1.fixed_encounters.z05.counts_by_party_size")
        self.assertEqual(enc["count"], 2)
        self.assertLessEqual(narration_tokens(room), 150)

    def test_lore_z03_and_back_cage(self):
        arcade = load_room("f01-z03")
        ids = [s["id"] for s in arcade["secrets"]]
        self.assertEqual(ids, ["unclaimed-crate", "odd-coin-identify", "back-cage"])
        identify = arcade["secrets"][1]
        self.assertEqual(identify["reveal_text"], "ITEM NOT RECOGNIZED.")
        self.assertEqual(identify["trigger"]["item"], "Vendor Oddity (Unappraised)")
        self.assertIn("Never explain it.", identify["gm_note"])
        plant = arcade["secrets"][0]
        self.assertEqual(plant["grants"]["item"], "Vendor Oddity (Unappraised)")
        self.assertIn("A coin. Probably.", plant["grants"]["box_text"])
        self.assertEqual(plant["achievement"]["id"], "ACH-0081")
        cage = arcade["secrets"][2]
        skills = [t["skill"] for t in cage["triggers"]]
        self.assertEqual(skills, ["Perception", "Investigation"])
        back = load_room("f01-z03b")
        self.assertEqual(back["voice_lines"]["win"], "The map is scrawled in a hurry, and it shows a door that isn't on yours.")
        labels = [row.get("label") or row.get("item") or row.get("roll") for row in back["loot"]]
        self.assertIn("Sports Drink, Blue Flavor, Do Not Ask", labels)
        self.assertIn("3d6 x 5", labels)
        self.assertEqual([a["id"] for a in back["achievements"]], ["ACH-0177", "ACH-0179"])

    def test_day_4_break_room_layer_closes_vendors(self):
        room = load_room("f01-z06", day=4)
        self.assertEqual(room.get("vendors"), "closed")
        self.assertFalse(room.get("saferoom"))
        self.assertIsNone(room.get("rest"))
        self.assertEqual(room.get("day_encounters"), [])
        self.assertEqual(room.get("loot"), [])
        self.assertTrue(room.get("closed"))
        self.assertTrue(room.get("passable"))
        resolved = resolve_room(room, 3)
        self.assertEqual(resolved["encounters"], [])

    def test_day_layers_keep_later_fights(self):
        stage = load_room("f01-z10")
        self.assertNotIn("enc-d03-03", [e["enc_id"] for e in stage["encounters"]])
        self.assertNotIn("enc-d02-02", [e["enc_id"] for e in load_room("f01-zS")["encounters"]])
        self.assertNotIn("enc-d02-03", [e["enc_id"] for e in load_room("f01-z11")["encounters"]])
        day3 = resolve_room(load_room("f01-z10", day=3), 3)
        self.assertIn("enc-d03-03", [e["enc_id"] for e in day3["encounters"]])
        day4 = resolve_room(load_room("f01-z10", day=4), 3)
        ushers = [e for e in day4["encounters"] if e["enc_id"] == "enc-d04-03"]
        self.assertEqual(len(ushers), 1)
        self.assertEqual(ushers[0]["trigger"], "on_enter")
        self.assertNotIn("enc-d03-03", [e["enc_id"] for e in day4["encounters"]])
        # This branch's budget file is still pre-v0.2.9, so the live party-3 cell is 3.
        # PR #27 sets it to 2. The resolver returns 2 when the budget says 2.
        self.assertEqual(ushers[0]["count"], 2)
        boss = resolve_room(load_room("f01-z10", day=5), 3)
        boss_rows = [e for e in boss["encounters"] if e["enc_id"] == "enc-d05-03"]
        self.assertTrue(boss_rows)
        self.assertTrue(all(e["trigger"] == "on_enter" for e in boss_rows))
        vermin = resolve_room(load_room("f01-z08", day=3), 3)
        self.assertIn("enc-d03-02", [e["enc_id"] for e in vermin["encounters"]])
        green = load_room("f01-z09", day=5)
        self.assertTrue(green.get("open"))
        self.assertIn("enc-d05-01", [e["enc_id"] for e in green.get("day_encounters") or []])
        service = resolve_room(load_room("f01-zS", day=2), 3)
        self.assertTrue(any(e["enc_id"] == "enc-d02-02" and e["trigger"] == "on_enter" for e in service["encounters"]))
        stairs = resolve_room(load_room("f01-z11", day=2), 3)
        self.assertIn("enc-d02-03", [e["enc_id"] for e in stairs["encounters"]])

    def test_wandering_has_a_card(self):
        room = load_room("f01-wandering")
        self.assertIn("enc-d01-04", [e["enc_id"] for e in room["encounters"]])
        self.assertEqual(room["zone"], "wandering")
        day4 = resolve_room(load_room("f01-wandering", day=4), 3)
        self.assertIn("enc-d04-02", [e["enc_id"] for e in day4["encounters"]])

    def test_fights_trigger_on_enter(self):
        greeters = load_room("f01-z07")
        self.assertTrue(greeters["encounters"])
        self.assertTrue(all(e["trigger"] == "on_enter" for e in greeters["encounters"]))

    def test_narrator_lines_end_a_sentence(self):
        room = load_room("f01-z05")
        self.assertTrue(room["narrator_line"].endswith("."))
        self.assertNotIn(" Each", room["narrator_line"])
        self.assertIn("read_aloud", room)
        self.assertIn("positions", room)
        self.assertIn("gm_notes", room)
        self.assertIn("rest", room)
        broken = json.loads(json.dumps(room))
        broken["narrator_line"] = "The hall stops mid"
        errs = check_room(broken, "sample")
        self.assertTrue(any("sentence" in err for err in errs))
        self.assertTrue(label_cut_off("Counters and sandbags (half cover); the brick prize"))
        self.assertFalse(label_cut_off(room["positions"][1]["name"]))
        for pos in room["positions"]:
            self.assertFalse(label_cut_off(pos["name"]), pos["name"])

    def test_lore_followups_and_saferoom_rest(self):
        arcade = load_room("f01-z03")
        self.assertEqual(
            arcade["voice_lines"]["win"],
            "Pockets full, one arm slightly chewed, and the machines already restocking like nothing happened.",
        )
        self.assertEqual(arcade["secrets"][0]["id"], "unclaimed-crate")
        gallery = load_room("f01-z05")
        self.assertEqual(gallery["secrets"], [])
        self.assertEqual(
            [row["id"] for row in gallery["achievements"]],
            ["ACH-0867", "ACH-0861", "ach-f01-0033"],
        )
        self.assertEqual(
            gallery["npcs"][0]["line"],
            "Cover. Get behind things. Things are your friends. People are not your friends.",
        )
        self.assertIn("Smiling through it.", gallery["nameplate"])
        self.assertEqual(gallery["popups"][0]["id"], "COVER")
        self.assertTrue(any(row.get("item") == "cash register" for row in gallery["loot"]))
        break_room = load_room("f01-z06")
        self.assertEqual(break_room["rest"]["kind"], "long")
        self.assertNotIn("{days}", break_room["narrator_line"])
        self.assertNotIn("{days}", break_room["read_aloud"])
        self.assertNotIn("{days}", break_room["voice_lines"]["intro"])
        self.assertIn("5 days", break_room["read_aloud"])
        green = load_room("f01-z09")
        self.assertEqual(green["rest"]["kind"], "long")
        self.assertEqual(green["rest"]["boxes"], "open")

    def test_closed_rooms_have_no_fight_loot_or_rest(self):
        for room_id in ("f01-z05", "f01-z07", "f01-z08"):
            room = load_room(room_id, day=4)
            self.assertTrue(room.get("closed"), room_id)
            self.assertTrue(room.get("passable"), room_id)
            self.assertEqual(resolve_room(room, 3)["encounters"], [], room_id)
            self.assertEqual(room.get("loot"), [], room_id)
            self.assertIsNone(room.get("rest"), room_id)
        locker = load_room("f01-z08", day=4)
        self.assertEqual(locker.get("npcs"), [])
        self.assertIsNone(locker.get("key"))
        day3 = resolve_room(load_room("f01-z08", day=3), 3)
        self.assertIn("enc-d03-02", [row["enc_id"] for row in day3["encounters"]])


class ServerTests(unittest.TestCase):
    def test_stdio_refuses_cunning_action_and_stores_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["ENGINE_DATA_DIR"] = tmp
            try:
                state = {
                    "crawler": load("crawler-rogue.json"),
                    "narrator_line": "Mannequins wait behind the counter.",
                    "rng": ScriptedRng([12, 3]),
                    "target_id": "mannequin",
                    "combatants": {
                        "crawler": load("crawler-rogue.json"),
                        "mannequin": load("mannequin-staff.json"),
                    },
                }
                model = ModelClient(fake=True)
                store = Store(campaign="test")
                outs = handle({"type": "line", "player": "table", "crawler": "Crawler", "text": "I use Cunning Action to dash"}, state, model, store)
                self.assertTrue(outs)
                self.assertIn("Rogue 1", outs[0]["text"])
                self.assertEqual(outs[0]["voice"], "SYSTEM")
                store.close()
                self.assertTrue((Path(tmp) / "test.sqlite").is_file())
            finally:
                os.environ.pop("ENGINE_DATA_DIR", None)

    def test_module_serves_one_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ)
            env["ENGINE_DATA_DIR"] = tmp
            env["PYTHONPATH"] = str(ENGINE) + os.pathsep + env.get("PYTHONPATH", "")
            proc = subprocess.run(
                [sys.executable, "-m", "dcc_engine"],
                input='{"type":"line","player":"table","crawler":"Crawler","text":"hello"}\n',
                text=True,
                capture_output=True,
                cwd=str(ROOT),
                env=env,
                timeout=20,
            )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        msg = json.loads(proc.stdout.strip().splitlines()[0])
        self.assertEqual(msg["type"], "say")
        self.assertIn("hello", msg["text"])


class ModelTests(unittest.TestCase):
    def test_stream_yields_whole_sentences(self):
        chunks = ["Hello. The room ", "waits. Still going"]
        self.assertEqual(list(iter_sentences(chunks)), ["Hello.", "The room waits.", "Still going"])

    def test_live_call_without_a_key_names_the_env(self):
        client = ModelClient(fake=False)
        saved = {}
        for name in ("ENGINE_MODEL_API_KEY", "OPENAI_API_KEY"):
            saved[name] = os.environ.pop(name, None)
        try:
            with self.assertRaises(RuntimeError) as caught:
                list(client.stream({"line": "hello"}))
            self.assertIn("ENGINE_MODEL_API_KEY", str(caught.exception))
        finally:
            for name, value in saved.items():
                if value is not None:
                    os.environ[name] = value

    def test_fake_strong_model_ruling_resolves_as_attack(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["ENGINE_DATA_DIR"] = tmp
            try:
                state = {
                    "crawler": load("crawler-rogue.json"),
                    "narrator_line": "Mannequins wait behind the counter.",
                    "rng": ScriptedRng([18, 6]),
                    "target_id": "mannequin",
                    "combatants": {
                        "crawler": load("crawler-rogue.json"),
                        "mannequin": load("mannequin-staff.json"),
                    },
                }
                model = ModelClient(fake=True, fake_ruling={
                    "ruling": "Throwing the mannequin is an attack.",
                    "resolve_as": "attack",
                    "params": {"attacker": "crawler", "target": "mannequin"},
                    "log": "improvised throw",
                })
                store = Store(campaign="test")
                outs = handle({"type": "line", "player": "table", "crawler": "Crawler", "text": "I throw the mannequin"}, state, model, store)
                self.assertTrue(any(row.get("type") == "card" for row in outs))
                self.assertEqual(state["combatants"]["mannequin"]["hp"], 4)
                self.assertEqual(strong_model_name(), os.environ.get("ENGINE_STRONG_MODEL") or "gpt-4o")
                store.close()
            finally:
                os.environ.pop("ENGINE_DATA_DIR", None)

    def test_bad_ruling_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["ENGINE_DATA_DIR"] = tmp
            try:
                state = {"narrator_line": "The room waits.", "crawler": load("crawler-rogue.json")}
                model = ModelClient(fake=True, fake_ruling={
                    "ruling": "No.",
                    "resolve_as": "wish",
                    "params": {},
                    "log": "not an action",
                })
                store = Store(campaign="test")
                outs = handle({"type": "line", "text": "I cast the floor away"}, state, model, store)
                self.assertIn("The System says no", outs[0]["text"])
                store.close()
            finally:
                os.environ.pop("ENGINE_DATA_DIR", None)

    def test_chatter_does_not_call_the_strong_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["ENGINE_DATA_DIR"] = tmp
            try:
                state = {
                    "narrator_line": "The room waits.",
                    "rng": ScriptedRng([18, 6]),
                    "combatants": {
                        "crawler": load("crawler-rogue.json"),
                        "mannequin": load("mannequin-staff.json"),
                    },
                }
                model = ModelClient(fake=True, fake_ruling={
                    "ruling": "Throwing the mannequin is an attack.",
                    "resolve_as": "attack",
                    "params": {"attacker": "crawler", "target": "mannequin"},
                    "log": "should not run",
                })
                store = Store(campaign="test")
                outs = handle({"type": "line", "text": "hello"}, state, model, store)
                self.assertIn("hello", outs[0]["text"])
                self.assertEqual(state["combatants"]["mannequin"]["hp"], 13)
                store.close()
            finally:
                os.environ.pop("ENGINE_DATA_DIR", None)

    def test_heal_ruling_changes_hit_points(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["ENGINE_DATA_DIR"] = tmp
            try:
                crawler = load("crawler-rogue.json")
                crawler["hp"] = 4
                state = {
                    "narrator_line": "The room waits.",
                    "combatants": {"crawler": crawler},
                }
                model = ModelClient(fake=True, fake_ruling={
                    "ruling": "The potion works.",
                    "resolve_as": "heal",
                    "params": {"target": "crawler", "amount": 3},
                    "log": "potion",
                })
                store = Store(campaign="test")
                outs = handle({"type": "line", "text": "I use the potion"}, state, model, store)
                self.assertEqual(crawler["hp"], 7)
                self.assertIn("potion", outs[0]["text"].lower())
                store.close()
            finally:
                os.environ.pop("ENGINE_DATA_DIR", None)


if __name__ == "__main__":
    unittest.main()
