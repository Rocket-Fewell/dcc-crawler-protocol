"""Decision 032: dry [SYSTEM] vs snarky [GM] — pin SYSTEM_KINDS and format_player tagging."""
import importlib.util
import os
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("encounter_text", os.path.join(TOOLS, "encounter_text.py"))
et = importlib.util.module_from_spec(spec)
spec.loader.exec_module(et)


class VoiceTags032(unittest.TestCase):
    def test_system_kinds_allow_list(self):
        self.assertIn("voice_line", et.SYSTEM_KINDS)
        self.assertIn("route_voice_line", et.SYSTEM_KINDS)
        self.assertIn("system_notice", et.SYSTEM_KINDS)
        self.assertIn("exit_warning_read_aloud", et.SYSTEM_KINDS)
        self.assertNotIn("achievement_narration", et.SYSTEM_KINDS)
        self.assertNotIn("gm_color", et.SYSTEM_KINDS)
        self.assertNotIn("loot_box_callout", et.SYSTEM_KINDS)

    def test_achievement_and_unknown_are_gm_registration_collapse_are_system(self):
        doc = {
            "audience_manifest": {
                "schema": "audience/1",
                "player_blocks": [
                    {"path": "/day/collapse_notice", "kind": "system_notice", "field": "text"},
                    {"path": "/day/registration", "kind": "system_notice", "field": "text"},
                    {"path": "/day/fee", "kind": "system_notice", "field": "text"},
                    {"path": "/day/floor_exit/gm_warning", "kind": "exit_warning_read_aloud", "field": "text"},
                    {"path": "/encounters/0/proposed_achievements/0", "kind": "achievement_narration", "field": "narration", "encounter": "enc-x"},
                    {"path": "/encounters/0/loot_open", "kind": "loot_box_callout", "field": "text", "encounter": "enc-x"},
                    {"path": "/encounters/0/color", "kind": "gm_color", "field": "text", "encounter": "enc-x"},
                ],
            },
            "day": {
                "collapse_notice": {"text": "The floor collapses in 6 hours. Crawlers, move."},
                "registration": {"text": "Welcome. Registration complete."},
                "fee": {"text": "Field-rest fee: 20 credits."},
                "floor_exit": {"gm_warning": {"text": "Reach a stairwell or you do not leave."}},
            },
            "encounters": [
                {
                    "id": "enc-x",
                    "proposed_achievements": [{"narration": "New achievement! Test Pilot. You pressed the button."}],
                    "loot_open": {"text": "Bronze Deed Box. Pull 1 of 2."},
                    "color": {"text": "The audience snickers."},
                }
            ],
            "routes": [],
        }
        by_path = {e["path"]: e for e in et.entries(doc)}
        self.assertEqual(by_path["/day/collapse_notice"]["voice"], "system")
        self.assertEqual(by_path["/day/registration"]["voice"], "system")
        self.assertEqual(by_path["/day/fee"]["voice"], "system")
        self.assertEqual(by_path["/day/floor_exit/gm_warning"]["voice"], "system")
        self.assertEqual(by_path["/encounters/0/proposed_achievements/0"]["voice"], "gm")
        self.assertEqual(by_path["/encounters/0/loot_open"]["voice"], "gm")
        self.assertEqual(by_path["/encounters/0/color"]["voice"], "gm")

        items, _ = et.player_items(doc, lambda e: True, hours=None, include_optional=True, confirm=True)
        out = et.format_player(items)
        self.assertIn("**[SYSTEM]** The floor collapses in 6 hours", out)
        self.assertIn("**[SYSTEM]** Welcome. Registration complete.", out)
        self.assertIn("**[SYSTEM]** Field-rest fee: 20 credits.", out)
        self.assertIn("**[SYSTEM]** Reach a stairwell", out)
        self.assertIn("**[GM]** New achievement! Test Pilot.", out)
        self.assertIn("**[GM]** Bronze Deed Box.", out)
        self.assertIn("**[GM]** The audience snickers.", out)
        for snark in ("New achievement!", "Bronze Deed Box", "audience snickers"):
            for chunk in out.split("\n\n"):
                if snark in chunk:
                    self.assertFalse(chunk.startswith("**[SYSTEM]**"), chunk)


    def test_stale_manifest_gm_color_path_forces_gm_voice(self):
        """Safety net: path .../gm_color or kind gm_color is GM even when kind is still voice_line."""
        joke = "The System wishes the surface crowd luck with that. Also: yes, the dog gets a nameplate."
        doc = {
            "audience_manifest": {
                "schema": "audience/1",
                "player_blocks": [
                    {"path": "/encounters/0/voice_lines/registration", "kind": "voice_line", "field": "text", "encounter": "enc-d01-06"},
                    {"path": "/encounters/0/voice_lines/gm_color", "kind": "voice_line", "field": "text", "encounter": "enc-d01-06"},
                    {"path": "/encounters/0/extra", "kind": "gm_color", "field": "text", "encounter": "enc-d01-06"},
                ],
            },
            "day": {},
            "encounters": [{
                "id": "enc-d01-06",
                "voice_lines": {
                    "registration": {"text": "Welcome. Registration complete."},
                    "gm_color": {"text": joke},
                },
                "extra": {"text": "Extra snark beat."},
            }],
            "routes": [],
        }
        by_path = {e["path"]: e for e in et.entries(doc)}
        self.assertEqual(by_path["/encounters/0/voice_lines/registration"]["voice"], "system")
        self.assertEqual(by_path["/encounters/0/voice_lines/gm_color"]["voice"], "gm")
        self.assertEqual(by_path["/encounters/0/extra"]["voice"], "gm")
        items, _ = et.player_items(doc, lambda e: e.get("encounter") == "enc-d01-06", hours=None, include_optional=True, confirm=True)
        out = et.format_player(items)
        self.assertIn("**[SYSTEM]** Welcome. Registration complete.", out)
        self.assertIn("**[GM]** " + joke.split(".")[0], out)  # tagged GM
        self.assertIn(joke, out)
        for chunk in out.split("\n\n"):
            if "dog gets a nameplate" in chunk:
                self.assertFalse(chunk.startswith("**[SYSTEM]** "), chunk)
                self.assertTrue(chunk.startswith("**[GM]** ") or "**[GM]**" in chunk, chunk)


if __name__ == "__main__":
    unittest.main()
