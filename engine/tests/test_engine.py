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

from dcc_engine.model import ModelClient  # noqa: E402
from dcc_engine.rules import ScriptedRng, attack, cunning_action  # noqa: E402
from dcc_engine.rooms import load_room, resolve_room  # noqa: E402
from dcc_engine.schema import narration_tokens  # noqa: E402
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
        self.assertEqual(mannequin["attacks"][0]["to_hit"], 4)
        rng = ScriptedRng(script["rolls"])
        hit = attack(crawler, mannequin, rng)
        self.assertTrue(hit["hit"])
        self.assertEqual(hit["d20"], 18)
        self.assertEqual(hit["total"], 23)
        self.assertEqual(hit["damage"], 9)
        self.assertEqual(mannequin["hp"], 4)
        reply = attack(mannequin, crawler, rng)
        self.assertEqual(reply["to_hit"], 4)
        self.assertEqual(reply["d20"], 11)
        self.assertEqual(reply["total"], 15)
        self.assertTrue(reply["hit"])
        self.assertEqual(reply["damage"], 6)
        self.assertEqual(crawler["hp"], 4)
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

    def test_day_4_break_room_layer_closes_vendors(self):
        room = load_room("f01-z06", day=4)
        self.assertEqual(room.get("vendors"), "closed")
        self.assertFalse(room.get("saferoom"))


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


if __name__ == "__main__":
    unittest.main()
