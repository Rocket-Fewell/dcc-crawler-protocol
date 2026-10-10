"""Floors 1–3 on the local table. The day-page lines stay the voice."""

import unittest

from dcc_engine.narrate import attack_gm
from urllib.request import urlopen

from dcc_engine.playthrough import Playthrough
from dcc_engine.script import load_script, npc_names
from dcc_engine.server import serve_background
from dcc_engine.table import ScriptedRng
from tools import roll


def _text(lines):
    return " ".join(line.get("text") or "" for line in lines)


class PlaythroughTests(unittest.TestCase):
    def test_a_miss_keeps_the_mannequin_joke_and_does_not_paint_it_on_a_rat(self):
        smile = attack_gm("Raithen", "Eldritch Blast", "Smiling Polo Mannequin 1", False, 0, "force", 13, False, False)
        rat = attack_gm("Raithen", "Eldritch Blast", "Vent Rat 1", False, 0, "force", 7, False, False)
        self.assertIn("still smiling", smile)
        self.assertNotIn("smiling", rat)
        self.assertIn("offended", rat)

    def test_script_keeps_the_filed_voice_and_the_local_floor_3_ending(self):
        scenes = load_script()
        floors = {scene["floor"] for scene in scenes}
        self.assertEqual(floors, {1, 2, 3})
        cold = next(scene for scene in scenes if scene["floor"] == 1 and scene["id"] == "enc-d01-06")
        self.assertIn("horn sounds across the city", _text(cold["lines"]))
        dean = next(scene for scene in scenes if scene["floor"] == 1 and scene["id"] == "enc-d05-03")
        dean_text = _text(dean["lines"])
        self.assertIn("Dean Thudd", dean_text)
        self.assertIn("OPINIONS ABOUT YOUR FEET", dean_text)
        self.assertIn("head of Orientation himself: Dean Thudd!", dean_text)
        krakaren = next(scene for scene in scenes if scene["floor"] == 2 and scene["id"] == "enc-d05-02")
        self.assertIn("Not the original. Still your problem.", _text(krakaren["lines"]))
        self.assertEqual(scenes[-1]["id"], "f03-15")
        self.assertIn("Floor 3 ends under your boots", _text(scenes[-1]["lines"]))
        known = set(npc_names())
        heard = []
        for scene in scenes:
            for line in scene["lines"]:
                if line.get("voice") == "NPC":
                    heard.append(line["npc"])
                    self.assertIn(line["npc"], known)
        for name in ("Village Elder", "Hedge Appraiser", "Low Chapel Bishop", "Village Saint", "Benefactor", "Guide"):
            self.assertIn(name, heard)

    def test_walk_speaks_dean_by_his_name_and_does_not_log_a_session(self):
        calls = []
        previous = roll.append_log
        roll.append_log = lambda *args, **kwargs: calls.append(1)
        try:
            play = Playthrough(rng=ScriptedRng([15, 4]))
            self.assertFalse(play.done)
            self.assertIn("[SYSTEM]", play.log[0]["text"])
            seen_dean = False
            seen_elder = False
            seen_shot = False
            guard = 0
            while not play.done and guard < 400:
                scene = play.scene
                if scene["floor"] == 1 and scene["id"] == "enc-d01-11" and not seen_shot:
                    self.assertIsNotNone(play.fight)
                    before = play.fight.enemies[0]["hp"]
                    play.resolve_line("I cast eldritch blast at the first one")
                    self.assertLess(play.fight.enemies[0]["hp"], before)
                    seen_shot = True
                if scene["floor"] == 1 and scene["id"] == "enc-d05-03":
                    names = " ".join(enemy["name"] for enemy in play.fight.enemies)
                    self.assertIn("Dean Thudd (JV)", names)
                    self.assertNotIn("Adjunct Smash", names)
                    blob = _text(play.log)
                    self.assertIn("OPINIONS ABOUT YOUR FEET", blob)
                    self.assertIn("[GM]", blob)
                    seen_dean = True
                if scene["id"] == "f03-02":
                    self.assertIn("[NPC: Village Elder]", _text(play.log))
                    seen_elder = True
                play.advance()
                guard += 1
            self.assertTrue(play.done)
            self.assertTrue(seen_shot)
            self.assertTrue(seen_dean)
            self.assertTrue(seen_elder)
            self.assertIn("Floor 3 is behind you", play.view()["title"])
            self.assertEqual(calls, [])
        finally:
            roll.append_log = previous

    def test_pages_keep_the_gallery_and_open_the_walk(self):
        server = serve_background("127.0.0.1", 0)
        self.addCleanup(server.shutdown)
        self.addCleanup(server.server_close)
        base = f"http://127.0.0.1:{server.server_address[1]}"
        with urlopen(base + "/", timeout=5) as response:
            page = response.read().decode("utf-8")
        self.assertIn("Floors 1", page)
        self.assertIn('id="listen"', page)
        with urlopen(base + "/player", timeout=5) as response:
            gallery = response.read().decode("utf-8")
        self.assertIn("Shooting Gallery", gallery)
        with urlopen(base + "/api/play", timeout=5) as response:
            body = response.read().decode("utf-8")
        self.assertIn("outer zones close", body)
        self.assertIn("[GM]", body)
        self.assertNotIn("Adjunct Smash", body)
