"""tables/species-class-reskins.json (Lore's format): ids, coverage, hash, labels with plain-5e fallback. Placeholder names live ONLY in fixtures here."""
import hashlib
import json
import os
import shutil
import tempfile
import unittest

from test_state import TOOLS
import sys
sys.path.insert(0, TOOLS)
import species_class_reskins as scr  # noqa: E402

CAMPAIGN = os.path.dirname(TOOLS)
LIVE_TABLES = os.path.join(CAMPAIGN, "tables")
LORE_FILE = "/workspace/dcc-lore/tables/species-class-reskins.json"


def ent(i, kind, srd, disp, parent=None, short=None):
    return {"id": i, "kind": kind, "parent_id": parent, "srd_name": srd, "display_name": disp, "combined_label": f"{disp} ({short or srd})",
            "nation": None if kind.startswith("class") else "Testland", "flavor": "x", "spoken": "x"}


FIXTURE = {
    "schema": "species-class-reskins/0.1.0",
    "meta": {"version": "9.9.9", "title": "TEST FIXTURE, PLACEHOLDER NAMES ONLY"},
    "entries": [
        ent("human", "species", "Human", "PLACEHOLDER Meatsack"),
        {**ent("elf-high", "species_lineage", "High Elf", "PLACEHOLDER Ivy League", "elf"), "base_id": "elf", "chargen_value": "High Elf", "rules_entry": True},
        ent("wizard", "class", "Wizard", "PLACEHOLDER Grad Student"),
        ent("cleric-protector", "class_option", "Protector (Divine Order)", "PLACEHOLDER Bodyguard", "cleric", short="Protector"),
    ],
}


class Sandbox(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.t = self.tmp.name
        shutil.copy(os.path.join(LIVE_TABLES, "chargen-5e.json"), self.t)
        self.path = os.path.join(self.t, "species-class-reskins.json")
        self._env = os.environ.get("SPECIES_CLASS_RESKINS_PATH")
        os.environ["SPECIES_CLASS_RESKINS_PATH"] = self.path

    def tearDown(self):
        if self._env is None:
            os.environ.pop("SPECIES_CLASS_RESKINS_PATH", None)
        else:
            os.environ["SPECIES_CLASS_RESKINS_PATH"] = self._env
        self.tmp.cleanup()

    def write(self, data, version=True):
        with open(self.path, "w") as f:
            json.dump(data, f)
        if version:
            with open(scr.version_path(self.path), "w") as f:
                json.dump({"version": "9.9.9", "sha256": scr.sha256_of(self.path), "entry_count": len(data.get("entries", []))}, f)


class RequiredIds(unittest.TestCase):
    def test_ids_follow_lores_scheme_and_count(self):
        req = scr.required_ids()
        by = {r["id"]: r for r in req}
        kinds = [r["kind"] for r in req]
        self.assertEqual((kinds.count("species"), kinds.count("species_lineage"), kinds.count("class"), kinds.count("class_option")), (21, 24, 12, 4))
        self.assertEqual((by["elf-high"]["base_id"], by["elf-high"]["chargen_value"]), ("elf", "High Elf"))
        self.assertEqual(len([r for r in req if r["shown_in_create"]]), 49)
        for i in ("elf-high", "elf-drow", "gnome-rock", "dragonborn-black", "tiefling-infernal", "goliath-storm", "cleric-protector", "druid-warden", "wizard", "human", "raptorkin"):
            self.assertIn(i, by)
        self.assertEqual(by["elf-high"]["srd_name"], "High Elf")
        self.assertEqual(by["dragonborn-red"]["srd_name"], "Red Dragonborn")
        self.assertEqual(by["cleric-thaumaturge"]["srd_name"], "Thaumaturge (Divine Order)")
        self.assertFalse(by["naga"]["shown_in_create"])

    def test_kid_and_lineage_id(self):
        self.assertEqual(scr.kid("Cleric-Protector!"), "cleric-protector")
        self.assertEqual(scr.lineage_id("Elf", "High Elf"), "elf-high")
        self.assertEqual(scr.lineage_id("Gnome", "Rock Gnome"), "gnome-rock")
        self.assertEqual(scr.lineage_id("Dragonborn", "Black"), "dragonborn-black")


class Labels(Sandbox):
    def test_absent_table_and_missing_entries_fall_back_to_the_plain_name(self):
        self.assertEqual(scr.species_label("Human"), "Human")
        self.write(FIXTURE)
        self.assertEqual(scr.species_label("Human"), "PLACEHOLDER Meatsack (Human)")
        self.assertEqual(scr.class_label("Wizard"), "PLACEHOLDER Grad Student (Wizard)")
        self.assertEqual(scr.class_label("Fighter"), "Fighter")
        self.assertEqual(scr.label("elf-high", "High Elf"), "PLACEHOLDER Ivy League (High Elf)")
        self.assertEqual(scr.label("cleric-protector", "Protector"), "PLACEHOLDER Bodyguard (Protector)")   # combined_label as written, never rebuilt

    def test_garbage_never_crashes_or_blanks(self):
        for bad in ("{not json", "[]", '{"entries": "oops"}', '{"entries": [1, null, {"id": 5}, {"id": "wizard", "display_name": 7}]}', '{"entries": [{"id": "wizard"}]}'):
            with open(self.path, "w") as f:
                f.write(bad)
            self.assertEqual(scr.class_label("Wizard"), "Wizard")


class Check(Sandbox):
    def test_absent_ok_warn_fail(self):
        self.assertEqual(scr.check_hash(self.path)[0], "absent")
        self.assertEqual(scr.main([]), 0, "no table in place is fine")
        self.write(FIXTURE, version=False)
        self.assertEqual(scr.check_hash(self.path)[0], "warn")
        self.write(FIXTURE)
        self.assertEqual(scr.check_hash(self.path)[0], "ok")
        d = json.load(open(self.path))
        d["entries"].append(ent("dwarf", "species", "Dwarf", "x"))
        json.dump(d, open(self.path, "w"))
        self.assertEqual(scr.check_hash(self.path)[0], "fail")
        self.assertEqual(scr.main([]), 1)

    def test_coverage_and_strict(self):
        self.write(FIXTURE)
        rep = scr.check(tables=self.t)
        self.assertEqual((rep["required"], rep["covered"]), (49, 4))
        self.assertIn("dwarf", rep["missing"])
        self.assertEqual(rep["errors"], [])
        self.assertEqual(scr.main([]), 0)
        self.assertEqual(scr.main(["--strict"]), 1)
        self.assertEqual(scr.check(tables=self.t, include_house=True)["required"], 61)

    def test_structure_errors_and_warnings(self):
        bad = {"schema": "nope", "entries": [ent("human", "species", "Human", "A"), ent("human", "species", "Human", "B"),
                                             {"id": "orc", "kind": "species", "srd_name": "Orc", "display_name": "Champ Hunter", "combined_label": "Champ Hunter (Orc)"},
                                             dict(ent("elf", "species", "Elf", "Mismatch"), combined_label="Something Else (Elf)"),
                                             dict(ent("dwarf", "species", "Dwarf", "Nest"), combined_label="Nest (Dwarf (Nested))"),
                                             {"display_name": "no id"}]}
        self.write(bad)
        rep = scr.check(tables=self.t)
        text = "\n".join(rep["errors"])
        for needle in ("schema must be", "duplicate id", "never champs", "combined_label should be", "without an id"):
            self.assertIn(needle, text)
        self.assertTrue(any("nested parentheses" in w for w in rep["warnings"]))
        self.assertEqual(scr.main([]), 1)

    def test_long_labels_keep_the_5e_name(self):
        e = ent("human", "species", "Human", "Z" * 120)
        lab = scr.entry_label(e)
        self.assertLessEqual(len(lab), 100)
        self.assertTrue(lab.endswith("(Human)"))


VFIX = {
    "schema": "species-class-reskins/0.1.0",
    "meta": {"version": "9.9.9"},
    "entries": [
        ent("elf", "species", "Elf", "PLACEHOLDER Pointy"),
        {**ent("elf-high", "species_lineage", "High Elf", "PLACEHOLDER Ivy", "elf"), "base_id": "elf", "chargen_value": "High Elf", "rules_entry": True},
        ent("felid", "species", "Felid", "PLACEHOLDER Whiskers"),
        {**ent("felid-cat", "species_variant", "Cat", "PLACEHOLDER Tabby", "felid"), "base_id": "felid", "chargen_value": None, "rules_entry": False},
    ],
}


class Variants(Sandbox):
    def errs(self, data):
        self.write(data)
        return "\n".join(scr.check(tables=self.t)["errors"])

    def test_good_variant_file_passes(self):
        self.assertEqual(self.errs(VFIX), "")
        self.assertEqual(scr.label("felid-cat", "Cat", kind="species_variant"), "PLACEHOLDER Tabby (Cat)")
        self.assertEqual(scr.species_label("Felid"), "PLACEHOLDER Whiskers (Felid)")
        self.assertEqual(scr.label("felid-cat", "Cat", kind="species"), "Cat", "a variant id never answers a species lookup")

    def test_variant_base_problems_fail(self):
        def mod(i, **kw):
            return {**VFIX, "entries": [({**e, **kw} if e["id"] == i else e) for e in VFIX["entries"]]}
        self.assertIn("base_id missing", self.errs(mod("felid-cat", base_id=None)))
        self.assertIn("is not a known species", self.errs(mod("felid-cat", base_id="narwhal")))
        self.assertIn("base_id 'felid' != parent_id", self.errs(mod("felid-cat", parent_id="elf")))
        self.assertIn("must not carry a chargen_value", self.errs(mod("felid-cat", chargen_value="Cat")))
        self.assertIn("rules_entry false", self.errs(mod("felid-cat", rules_entry=True)))
        self.assertIn("not an exact chargen-5e.json option", self.errs(mod("elf-high", chargen_value="high elf")))
        self.assertIn("base_id missing", self.errs(mod("elf-high", base_id=None)))

    def test_ambiguous_mappings_fail(self):
        two = {**VFIX, "entries": VFIX["entries"] + [{**ent("elf-high2", "species_lineage", "High Elf", "PLACEHOLDER Dup", "elf"), "base_id": "elf", "chargen_value": "High Elf", "rules_entry": True}]}
        text = self.errs(two)
        self.assertIn("same (base_id, chargen_value)", text)
        self.assertIn("same (base_id, srd_name)", text)
        dup = {**VFIX, "entries": VFIX["entries"] + [{**ent("felid-cat-2", "species_variant", "Cat", "PLACEHOLDER Dup", "felid"), "base_id": "felid", "chargen_value": None, "rules_entry": False}]}
        self.assertIn("same (base_id, srd_name)", self.errs(dup))
        coll = {**VFIX, "entries": VFIX["entries"] + [{**ent("orc", "species_variant", "Orcish", "PLACEHOLDER", "elf"), "base_id": "elf", "chargen_value": None, "rules_entry": False}]}
        self.assertIn("collides with a species/class id", self.errs(coll))

    def test_enable_disable_flag_writes_session_json_only(self):
        c = tempfile.mkdtemp()
        p = scr.set_flag(True, "alpha", campaign=c)
        self.assertEqual(p, os.path.join(c, "sessions", "session.json"))
        self.assertTrue(json.load(open(p))["create"]["species_class_reskin"])
        scr.set_flag(False, "beta", campaign=c)
        self.assertFalse(json.load(open(os.path.join(c, "sessions-data", "beta", "session.json")))["create"]["species_class_reskin"])
        shutil.rmtree(c)


class LiveAndLore(unittest.TestCase):
    def test_live_tables_copy_is_valid_and_complete_when_present(self):
        env = os.environ.pop("SPECIES_CLASS_RESKINS_PATH", None)
        try:
            rep = scr.check()
        finally:
            if env is not None:
                os.environ["SPECIES_CLASS_RESKINS_PATH"] = env
        self.assertIn(rep["hash"]["status"], ("absent", "ok"), rep["hash"]["message"])
        self.assertEqual(rep["errors"], [])
        if rep["hash"]["status"] == "ok":
            self.assertEqual(rep["missing"], [], "the copy in tables/ must cover every /create id")

    @unittest.skipUnless(os.path.exists(LORE_FILE), "Lore's file not on this box")
    def test_lores_current_file_covers_everything_in_create(self):
        rep = scr.check(path=LORE_FILE, include_house=True)
        self.assertEqual(rep["errors"], [], rep["errors"])
        self.assertEqual(rep["missing"], [], "Lore's table must cover every id (strict)")
        self.assertEqual(rep["hash"]["status"], "ok", rep["hash"]["message"])

    def test_publisher_card_uses_labels_and_falls_back(self):
        import publisher
        v = {"species": "Human", "class": "Wizard"}
        real_cfg = publisher.session_config
        try:
            publisher.session_config = lambda: {}   # never read the live session.json (Caleb may have switched the names on): the default is OFF
            self.assertEqual(publisher._species_class_label(v), "Human Wizard")   # switch off (default): plain names even with the copy in tables/
        finally:
            publisher.session_config = real_cfg
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "species-class-reskins.json")
            json.dump(FIXTURE, open(p, "w"))
            os.environ["SPECIES_CLASS_RESKINS_PATH"] = p
            real_cfg = publisher.session_config
            try:
                publisher.session_config = lambda: {"create": {"species_class_reskin": True}}
                self.assertEqual(publisher._species_class_label(v), "PLACEHOLDER Meatsack (Human) PLACEHOLDER Grad Student (Wizard)")
                publisher.session_config = lambda: {"create": {"species_class_reskin": False}}
                self.assertEqual(publisher._species_class_label(v), "Human Wizard")
            finally:
                publisher.session_config = real_cfg
                os.environ.pop("SPECIES_CLASS_RESKINS_PATH", None)


if __name__ == "__main__":
    unittest.main()
