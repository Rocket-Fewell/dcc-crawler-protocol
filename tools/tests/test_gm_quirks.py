"""Tests for tools/gm_quirks.py (exposed through state.py) and tools/sim_floors.py.
Run: python3 -m unittest discover -s tools/tests -p 'test_*.py'
Every test works in a temp campaign dir (DCC_CAMPAIGN_DIR); the real campaign's gm-notes/secret is never touched.
"""
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMPAIGN_REAL = os.path.dirname(TOOLS)
STATE_PY = os.path.join(TOOLS, "state.py")
spec = importlib.util.spec_from_file_location("state", STATE_PY)
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)
import gm_quirks as gq  # noqa: E402  (state.py put tools/ on sys.path)

TABLE_PATH = gq.DEFAULT_TABLE_PATHS[1]
ID_RE = re.compile(r"\b(?:PI|FX|QK|VT)-\d\d\b")


def load_real_table():
    with open(TABLE_PATH, encoding="utf-8") as f:
        return json.load(f)


TABLE = load_real_table()


def slurp(path, mode="r"):
    with open(path, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
        return f.read()


def forced(*rolls):
    """Patch value for gm_quirks._randbelow: yields the given 1-based die results in order."""
    it = iter(rolls)
    return lambda n: next(it) - 1


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p = mock.patch.dict(os.environ, {"DCC_CAMPAIGN_DIR": self.tmp.name})
        p.start()
        self.addCleanup(p.stop)
        os.environ.pop("DCC_GM_QUIRKS_TABLE", None)
        self.root = self.tmp.name
        self.secret = os.path.join(self.root, "gm-notes", "secret")
        self.roll_file = os.path.join(self.secret, "gm-quirk-roll.json")
        self.aff_file = os.path.join(self.secret, "gm-affinity.json")
        self.log_file = os.path.join(self.secret, "gm-affinity-log.jsonl")

    # --- helpers
    def run_cmd(self, *argv, expect=0, rolls=None):
        out, err = io.StringIO(), io.StringIO()
        ctx = mock.patch.object(gq, "_randbelow", forced(*rolls)) if rolls else contextlib.nullcontext()
        with ctx, contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = state.main(list(argv))
            except SystemExit as e:
                code = e.code
        self.assertEqual(code, expect, f"{argv}: stdout={out.getvalue()!r} stderr={err.getvalue()!r}")
        return out.getvalue().strip(), err.getvalue().strip()

    def sub(self, *argv):
        """Run state.py in a real subprocess (for concurrency tests)."""
        env = dict(os.environ, DCC_CAMPAIGN_DIR=self.root)
        return subprocess.Popen([sys.executable, STATE_PY, *argv], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    @staticmethod
    def read_json(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def write(path, text):
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def nbackups(self):
        d = os.path.join(self.secret, "backups")
        return len(os.listdir(d)) if os.path.isdir(d) else 0

    def log_lines(self):
        if not os.path.exists(self.log_file):
            return []
        with open(self.log_file, encoding="utf-8") as f:
            return [json.loads(x) for x in f if x.strip()]

    def mode(self, path):
        return os.stat(path).st_mode & 0o777

    def init_party(self):
        self.run_cmd("init", "--floor", "1")
        for name, player in (("Grimsby", "Caleb"), ("Donut", "Sam"), ("Mongo", "Ann"), ("Carl", "Bo")):
            self.run_cmd("add-crawler", name, "--player", player, "--class", "Fighter", "--species", "Human")

    def seal(self, pi=5, fx=7, q1=11, q2=3, tic=4, variant=None):
        """Roll with forced dice (1-based). Returns the stored rolls object."""
        dice = [pi, fx] + ([variant] if variant else []) + [q1, q2, tic]
        out, _ = self.run_cmd("gm-quirks", "roll", rolls=dice)
        self.assertEqual(out, "GM traits rolled and sealed")
        return self.read_json(self.roll_file)["rolls"]

    def register_all(self):
        self.init_party()
        self.run_cmd("affinity", "register", "--from-state")

    def add(self, player, delta, scene="s1", floor=1, session="S1", reason="because", *extra, expect=0):
        return self.run_cmd("affinity", "add", player, str(delta), "--reason", reason, "--scene", scene, "--floor", str(floor),
                            "--session", session, *extra, expect=expect)

    def aff(self, pid):
        return self.read_json(self.aff_file)["players"][pid]


# =========================================================================== table schema

class TableSchemaTests(unittest.TestCase):
    def test_real_table_validates(self):
        self.assertEqual(gq.validate_table(TABLE), [])

    def test_top_level_keys_and_counts(self):
        self.assertEqual(list(TABLE), gq.TABLE_KEYS)
        self.assertEqual([len(TABLE[k]) for k in ("prior_installation", "fixations", "quirks", "tics", "tells")], [8, 20, 12, 10, 8])

    def test_dice_sizes_come_from_meta(self):
        self.assertEqual([gq.dice_sides(TABLE, k) for k in ("prior_installation", "fixations", "quirks", "tics", "tells")], [8, 20, 12, 10, 8])

    def test_ladder_matches_the_documented_floor_mapping(self):
        expect = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 4, 10: 4, 11: 4, 12: 5, 13: 5, 99: 5}
        for floor, level in expect.items():
            self.assertEqual(gq.ladder_entry_for_floor(TABLE, floor)["level"], level, f"floor {floor}")

    def test_bands_cover_the_range_exactly(self):
        names = [gq.band_for(TABLE, v)["name"] for v in range(-10, 11)]
        self.assertEqual(names[0], "Vindictive")
        self.assertEqual(names[-1], "Favor")
        self.assertEqual(gq.band_for(TABLE, 3)["name"], "Mild perks")   # the +3 overlap is resolved: neutral is -3..+2
        self.assertEqual(gq.band_for(TABLE, 2)["name"], "Neutral")
        self.assertEqual(gq.band_for(TABLE, -3)["name"], "Neutral")
        self.assertEqual(gq.band_for(TABLE, -4)["name"], "Petty")

    def test_every_fixation_has_affinity_triggers(self):
        for fx in TABLE["fixations"]:
            self.assertTrue(fx["affinity"]["trigger_keywords"], fx["id"])
            self.assertTrue(all(1 <= p["points"] <= 3 for p in fx["affinity"]["pleases"]), fx["id"])
            self.assertTrue(all(-3 <= p["points"] <= -1 for p in fx["affinity"]["offends"]), fx["id"])

    def test_validator_catches_breakage(self):
        def broken(mutate):
            t = copy.deepcopy(TABLE)
            mutate(t)
            return gq.validate_table(t)
        self.assertTrue(broken(lambda t: t.pop("tells")))
        self.assertTrue(broken(lambda t: t["fixations"].append(copy.deepcopy(t["fixations"][0]))))              # duplicate id
        self.assertTrue(broken(lambda t: t["fixations"][3].update(roll_range=[3, 3])))                          # overlap / gap
        self.assertTrue(broken(lambda t: t["meta"]["affinity"]["bands"][2].update(min=-2)))                     # gap in bands
        self.assertTrue(broken(lambda t: t["ladder"][2].update(floor_min=6)))                                   # gap in ladder
        self.assertTrue(broken(lambda t: t["fixations"][10]["variants"][0].update(values=[1, 2])))              # variant size != die
        self.assertTrue(broken(lambda t: t["quirks"][0]["manifests_as"].pop("snark")))
        self.assertTrue(broken(lambda t: t["fixations"][0]["affinity"]["pleases"][0].update(points=7)))
        self.assertTrue(broken(lambda t: t["tics"][0].update(id="XX-01")))
        self.assertTrue(broken(lambda t: t["meta"].update(schema_version="2.0")))


class TableRefusalTests(Base):
    def test_roll_refuses_an_invalid_table_and_writes_nothing(self):
        bad = load_real_table()
        bad["quirks"].pop()
        path = os.path.join(self.root, "bad.json")
        with open(path, "w") as f:
            json.dump(bad, f)
        with mock.patch.dict(os.environ, {"DCC_GM_QUIRKS_TABLE": path}):
            _, err = self.run_cmd("gm-quirks", "roll", expect=1)
        self.assertIn("does not match the documented schema", err)
        self.assertFalse(os.path.exists(self.roll_file))

    def test_roll_refuses_when_the_table_is_missing(self):
        with mock.patch.dict(os.environ, {"DCC_GM_QUIRKS_TABLE": os.path.join(self.root, "nope.json")}):
            _, err = self.run_cmd("gm-quirks", "roll", expect=1)
        self.assertIn("not found", err)

    def test_meta_paths_must_stay_in_secret_dir(self):
        bad = load_real_table()
        bad["meta"]["affinity"]["roll_file"] = "sessions/gm-quirk-roll.json"
        path = os.path.join(self.root, "bad.json")
        with open(path, "w") as f:
            json.dump(bad, f)
        with mock.patch.dict(os.environ, {"DCC_GM_QUIRKS_TABLE": path}):
            _, err = self.run_cmd("gm-quirks", "roll", expect=1)
        self.assertIn("gm-notes/secret", err)
        self.assertFalse(os.path.exists(os.path.join(self.root, "sessions", "gm-quirk-roll.json")))


# =========================================================================== roll

class RollTests(Base):
    def test_roll_prints_only_the_neutral_confirmation(self):
        out, err = self.run_cmd("gm-quirks", "roll", rolls=[5, 7, 11, 3, 4])
        self.assertEqual(out, "GM traits rolled and sealed")
        self.assertEqual(err, "")

    def test_roll_stdout_never_contains_any_trait_id_or_name_for_all_20_fixations(self):
        names = [e["name"] for k in ("prior_installation", "fixations", "quirks", "tics") for e in TABLE[k]]
        for i, fx in enumerate(TABLE["fixations"], 1):
            with self.subTest(fixation=fx["id"]):
                with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, {"DCC_CAMPAIGN_DIR": d}):
                    dice = [(i % 8) + 1, i] + ([1 + i % 6] if fx.get("variants") else []) + [(i % 12) + 1, ((i + 4) % 12) + 1, (i % 10) + 1]
                    out, err = self.run_cmd("gm-quirks", "roll", rolls=dice)
                    out2, err2 = self.run_cmd("--json", "gm-quirks", "status")
                    text = out + err + out2 + err2
                    self.assertEqual(out, "GM traits rolled and sealed")
                    self.assertFalse(ID_RE.search(text), text)
                    for n in names:
                        self.assertNotIn(n.lower(), text.lower())
                    data = self.read_json(os.path.join(d, "gm-notes", "secret", "gm-quirk-roll.json"))
                    self.assertEqual(data["rolls"]["fixation"], fx["id"])
                    self.assertEqual(data["rolls"]["fixation_variant"] is not None, bool(fx.get("variants")))
                    log = slurp(os.path.join(d, "sessions", [f for f in os.listdir(os.path.join(d, "sessions")) if f.startswith("rolls-")][0]))
                    self.assertFalse(ID_RE.search(log), log)

    def test_json_output_is_neutral_too(self):
        with mock.patch.object(gq, "_randbelow", forced(1, 12, 1, 2, 3)):
            out, _ = self.run_cmd("gm-quirks", "roll", "--json")
        self.assertEqual(json.loads(out), {"ok": True, "message": "GM traits rolled and sealed"})

    def test_roll_file_schema_and_permissions(self):
        os.makedirs(os.path.join(self.root, "gm-notes", "secret"), mode=0o755)
        os.chmod(self.secret, 0o755)  # pre-existing loose dir must be tightened
        rolls = self.seal(pi=2, fx=18, q1=6, q2=9, tic=10)
        data = self.read_json(self.roll_file)
        self.assertEqual(set(data), {"schema_version", "campaign_id", "rolled_at", "rng", "nonce", "rolls", "commitment_sha256", "revealed"})
        self.assertEqual(set(data["rolls"]), {"prior_installation", "fixation", "fixation_variant", "quirks", "tic"})
        self.assertEqual(rolls, {"prior_installation": "PI-02", "fixation": "FX-18", "fixation_variant": None, "quirks": ["QK-06", "QK-09"], "tic": "VT-10"})
        self.assertEqual(data["rng"], "secrets.randbelow")
        self.assertIs(data["revealed"], False)
        self.assertRegex(data["nonce"], r"^[0-9a-f]{64}$")
        self.assertRegex(data["commitment_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(gq.validate_roll_data(data, TABLE), [])
        self.assertEqual(self.mode(self.roll_file), 0o600)
        self.assertEqual(self.mode(self.secret), 0o700)

    def test_commitment_is_sha256_of_canonical_rolls_plus_nonce(self):
        self.seal()
        data = self.read_json(self.roll_file)
        canon = json.dumps(data["rolls"], sort_keys=True, separators=(",", ":"))
        self.assertEqual(hashlib.sha256((canon + "|" + data["nonce"]).encode()).hexdigest(), data["commitment_sha256"])

    def test_fixation_variant_rolled_only_for_fx11(self):
        rolls = self.seal(fx=11, variant=6)
        self.assertEqual(rolls["fixation"], "FX-11")
        self.assertEqual(rolls["fixation_variant"], "404")
        with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, {"DCC_CAMPAIGN_DIR": d}):
            self.run_cmd("gm-quirks", "roll", rolls=[1, 12, 1, 2, 3])  # FX-12 consumes no variant die
            self.assertIsNone(self.read_json(os.path.join(d, "gm-notes", "secret", "gm-quirk-roll.json"))["rolls"]["fixation_variant"])

    def test_duplicate_quirk_is_rerolled(self):
        self.run_cmd("gm-quirks", "roll", rolls=[1, 1, 5, 5, 5, 8, 1])  # q2 rolls 5, 5, then 8
        data = self.read_json(self.roll_file)
        self.assertEqual(data["rolls"]["quirks"], ["QK-05", "QK-08"])
        self.assertEqual(data["rolls"]["tic"], "VT-01")

    def test_real_randomness_always_gives_valid_distinct_results(self):
        seen_fx, seen_pi = set(), set()
        for _ in range(400):
            r = gq.do_roll(TABLE)
            self.assertNotEqual(r["quirks"][0], r["quirks"][1])
            seen_fx.add(r["fixation"])
            seen_pi.add(r["prior_installation"])
            self.assertEqual(gq.validate_roll_data({"schema_version": "1.0", "campaign_id": "x", "rolled_at": "t", "rng": "r", "nonce": "a" * 64,
                                                    "rolls": r, "commitment_sha256": "b" * 64, "revealed": False}, TABLE), [])
        self.assertGreater(len(seen_fx), 12)  # not stuck
        self.assertEqual(gq.secrets.randbelow, gq._randbelow)  # the real source is secrets.randbelow

    def test_second_roll_is_refused_and_changes_nothing(self):
        self.seal()
        before = slurp(self.roll_file, "rb")
        _, err = self.run_cmd("gm-quirks", "roll", expect=1, rolls=[1, 1, 1, 2, 1])
        self.assertIn("already rolled", err)
        self.assertIn("--force --i-know-this-reveals", err)
        self.assertFalse(ID_RE.search(err))
        self.assertEqual(slurp(self.roll_file, "rb"), before)
        self.assertFalse(os.path.exists(os.path.join(self.secret, "archive")))

    def test_force_needs_both_flags(self):
        self.seal()
        before = slurp(self.roll_file, "rb")
        self.run_cmd("gm-quirks", "roll", "--force", expect=1)
        self.run_cmd("gm-quirks", "roll", "--i-know-this-reveals", expect=1)
        self.assertEqual(slurp(self.roll_file, "rb"), before)

    def test_override_archives_the_old_roll_and_announces_publicly(self):
        self.seal(fx=3)
        old = slurp(self.roll_file, "rb")
        out, _ = self.run_cmd("gm-quirks", "roll", "--force", "--i-know-this-reveals", rolls=[8, 20, 12, 1, 10])
        self.assertEqual(out, "GM traits rolled and sealed")
        archive = os.path.join(self.secret, "archive")
        files = os.listdir(archive)
        self.assertEqual(len(files), 1)
        self.assertEqual(slurp(os.path.join(archive, files[0]), "rb"), old)
        self.assertEqual(self.mode(os.path.join(archive, files[0])), 0o600)
        self.assertEqual(self.mode(archive), 0o700)
        self.assertEqual(self.read_json(self.roll_file)["rolls"]["fixation"], "FX-20")
        self.run_cmd("gm-quirks", "verify")
        log = slurp(self.public_log())
        self.assertIn("OVERRIDE", log)
        self.assertEqual(log.count("GM trait dice"), 2)
        self.assertFalse(ID_RE.search(log))

    def public_log(self):
        d = os.path.join(self.root, "sessions")
        return os.path.join(d, [f for f in os.listdir(d) if f.startswith("rolls-")][0])

    def test_public_roll_log_gets_a_neutral_line_only(self):
        self.seal(pi=4, fx=11, variant=2, q1=7, q2=8, tic=9)
        data = self.read_json(self.roll_file)
        log = slurp(self.public_log())
        self.assertEqual(len(log.strip().splitlines()), 1)
        self.assertIn("[ROLL] GM trait dice: rolled and sealed", log)
        self.assertIn(data["commitment_sha256"], log)       # the commitment is meant to be public
        self.assertNotIn(data["nonce"], log)
        self.assertFalse(ID_RE.search(log))
        self.assertNotIn("13", log.split("[ROLL]")[1].split("sha256")[0])       # the FX-11 variant value (13) is not logged

    def test_concurrent_rolls_only_one_wins(self):
        procs = [self.sub("gm-quirks", "roll") for _ in range(5)]
        codes = []
        for p in procs:
            out, err = p.communicate(timeout=60)
            codes.append(p.returncode)
            self.assertFalse(ID_RE.search(out + err))
        self.assertEqual(sorted(codes), [0, 1, 1, 1, 1])
        self.run_cmd("gm-quirks", "verify")

    def test_campaign_id_defaults_and_override(self):
        self.init_party()
        self.run_cmd("gm-quirks", "roll", "--campaign-id", "dcc-test", rolls=[1, 1, 1, 2, 1])
        self.assertEqual(self.read_json(self.roll_file)["campaign_id"], "dcc-test")
        with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, {"DCC_CAMPAIGN_DIR": d}):
            self.run_cmd("init")
            self.run_cmd("gm-quirks", "roll", rolls=[1, 1, 1, 2, 1])
            cid = self.read_json(os.path.join(d, "gm-notes", "secret", "gm-quirk-roll.json"))["campaign_id"]
            self.assertTrue(cid.startswith("dungeon-crawler-carl-5e-2024"), cid)


# =========================================================================== verify / status / show-gm / reveal

class VerifyShowTests(Base):
    def test_verify_ok_prints_no_traits(self):
        rolls = self.seal()
        out, err = self.run_cmd("gm-quirks", "verify")
        self.assertIn("commitment OK", out)
        self.assertFalse(ID_RE.search(out + err))
        self.assertIn(self.read_json(self.roll_file)["commitment_sha256"], out)

    def test_verify_detects_every_kind_of_tampering(self):
        self.seal()
        original = self.read_json(self.roll_file)
        for label, edit in (("rolls", lambda d: d["rolls"].update(tic="VT-01")), ("quirks", lambda d: d["rolls"].update(quirks=["QK-01", "QK-02"])),
                            ("nonce", lambda d: d.update(nonce="0" * 64)), ("commitment", lambda d: d.update(commitment_sha256="0" * 64))):
            with self.subTest(label):
                d = copy.deepcopy(original)
                edit(d)
                with open(self.roll_file, "w") as f:
                    json.dump(d, f)
                _, err = self.run_cmd("gm-quirks", "verify", expect=1)
                self.assertTrue("VERIFY FAILED" in err or "invalid" in err, err)
                self.assertFalse(ID_RE.search(err))
        with open(self.roll_file, "w") as f:
            json.dump(original, f)
        self.run_cmd("gm-quirks", "verify")

    def test_verify_without_roll_or_with_garbage(self):
        _, err = self.run_cmd("gm-quirks", "verify", expect=1)
        self.assertIn("no GM quirk roll", err)
        os.makedirs(self.secret)
        self.write(self.roll_file, "{not json")
        _, err = self.run_cmd("gm-quirks", "verify", expect=1)
        self.assertIn("not valid JSON", err)
        self.assertNotIn("not json", err)

    def test_status_before_and_after(self):
        out, _ = self.run_cmd("gm-quirks", "status")
        self.assertIn("not rolled yet", out)
        self.assertFalse(os.path.exists(self.secret))  # read-only: creates nothing
        self.seal()
        out, _ = self.run_cmd("gm-quirks", "status")
        self.assertIn("rolled and sealed", out)
        self.assertIn(self.read_json(self.roll_file)["commitment_sha256"], out)
        self.assertFalse(ID_RE.search(out))

    def test_show_gm_prints_traits_with_banner(self):
        self.seal(pi=5, fx=7, q1=11, q2=3, tic=4)
        out, _ = self.run_cmd("gm-quirks", "show-gm")
        lines = out.splitlines()
        self.assertIn("GM-ONLY", lines[0])
        self.assertIn("GM-ONLY", lines[-1])
        for want in ("PI-05 Haunted Hayride", "FX-07 Soup", "QK-11 Paranoid Eavesdropper", "QK-03 Fake Sympathy", "VT-04 Wheeze and Lip Smack"):
            self.assertIn(want, out)
        self.assertIn("soup, broth", out)  # fixation affinity keywords for the GM
        top, _ = self.run_cmd("show-gm")   # top-level alias
        self.assertEqual(top, out)

    def test_show_gm_level_filters_tells(self):
        self.seal()
        out, _ = self.run_cmd("gm-quirks", "show-gm", "--level", "2")
        self.assertIn("L2:", out)
        self.assertNotIn("L4:", out)
        self.assertIn("GENERIC TELL TABLE", out)
        self.run_cmd("gm-quirks", "show-gm", "--level", "9", expect=1)

    def test_show_gm_json_has_warning_and_rolls(self):
        rolls = self.seal()
        out, _ = self.run_cmd("gm-quirks", "show-gm", "--json")
        data = json.loads(out)
        self.assertIn("GM-ONLY", data["warning"])
        self.assertEqual(data["rolls"], rolls)

    def test_show_gm_needs_a_roll(self):
        _, err = self.run_cmd("gm-quirks", "show-gm", expect=1)
        self.assertIn("no GM quirk roll", err)

    def test_reveal_requires_flag_marks_revealed_and_stays_verifiable(self):
        self.seal()
        self.run_cmd("gm-quirks", "reveal", expect=1)
        self.assertIs(self.read_json(self.roll_file)["revealed"], False)
        out, _ = self.run_cmd("gm-quirks", "reveal", "--i-know-this-reveals")
        data = self.read_json(self.roll_file)
        self.assertIs(data["revealed"], True)
        self.assertIn(data["nonce"], out)
        self.run_cmd("gm-quirks", "verify")
        self.assertEqual(len(os.listdir(os.path.join(self.secret, "archive"))), 1)
        log = slurp(os.path.join(self.root, "sessions", [f for f in os.listdir(os.path.join(self.root, "sessions")) if f.startswith("rolls-")][0]))
        self.assertIn("REVEALED", log)
        self.assertFalse(ID_RE.search(log))
        self.assertNotIn(data["nonce"], log)
        status, _ = self.run_cmd("gm-quirks", "status")
        self.assertIn("revealed: yes", status)


# =========================================================================== level (public)

class LevelTests(Base):
    def level(self, floor, stress=0):
        out, _ = self.run_cmd("gm-quirks", "level", str(floor), "--stress", str(stress), "--json")
        return json.loads(out)

    def test_floor_to_level_mapping(self):
        for floor, lvl in {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 4, 10: 4, 11: 4, 12: 5, 13: 5, 40: 5}.items():
            self.assertEqual(self.level(floor)["effective_level"], lvl, floor)

    def test_stress_modifier_and_clamping(self):
        self.assertEqual(self.level(1, -1)["effective_level"], 0)    # clamp at 0
        self.assertEqual(self.level(2, 1)["effective_level"], 1)
        self.assertEqual(self.level(5, 1)["effective_level"], 3)
        self.assertEqual(self.level(9, -1)["effective_level"], 3)
        self.assertEqual(self.level(12, 1)["effective_level"], 5)    # clamp at 5
        self.assertEqual(self.level(11, 1)["effective_level"], 5)
        self.assertEqual(self.level(5, 1)["base_level"], 2)

    def test_glitch_max_read_from_json(self):
        for e in TABLE["ladder"]:
            floor = e["floor_min"]
            self.assertEqual(self.level(floor)["glitch_check_d20_max"], e["glitch_check_d20_max"])
        self.assertEqual([self.level(f)["glitch_check_d20_max"] for f in (1, 3, 5, 7, 9, 12)], [0, 1, 3, 4, 6, 8])
        self.assertEqual(self.level(5, 1)["glitch_check_d20_max"], TABLE["ladder"][3]["glitch_check_d20_max"])

    def test_text_output_and_no_secret_involvement(self):
        out, _ = self.run_cmd("gm-quirks", "level", "7")
        self.assertIn("effective level 3 (Vindictive)", out)
        self.assertIn("d20 <= 4", out)
        out0, _ = self.run_cmd("gm-quirks", "level", "1")
        self.assertIn("never", out0)
        self.assertFalse(os.path.exists(self.secret))   # works with nothing rolled; creates nothing
        self.assertFalse(ID_RE.search(out + out0))

    def test_level_output_is_identical_before_and_after_a_roll(self):
        before, _ = self.run_cmd("gm-quirks", "level", "6", "--stress", "1")
        self.seal(fx=13)
        after, _ = self.run_cmd("gm-quirks", "level", "6", "--stress", "1")
        self.assertEqual(before, after)

    def test_bad_input(self):
        self.run_cmd("gm-quirks", "level", "0", expect=1)
        self.run_cmd("gm-quirks", "level", "3", "--stress", "2", expect=2)


# =========================================================================== affinity

class AffinityRegisterTests(Base):
    def test_register_from_state_uses_existing_player_names(self):
        self.init_party()
        out, _ = self.run_cmd("affinity", "register", "--from-state")
        self.assertIn("caleb", out)
        data = self.read_json(self.aff_file)
        self.assertEqual(set(data), {"schema_version", "campaign_id", "updated", "players"})
        self.assertEqual(set(data["players"]), {"caleb", "sam", "ann", "bo"})
        p = data["players"]["caleb"]
        self.assertEqual(set(p), {"display_name", "character", "affinity", "scene_id", "scene_delta", "last_drift_floor", "flags"})
        self.assertEqual((p["display_name"], p["character"], p["affinity"], p["scene_delta"], p["flags"]), ("Caleb", "Grimsby", 0, 0, []))
        self.assertEqual(p["last_drift_floor"], 1)   # registered during floor 1: no drift owed for floor 1
        self.assertEqual(self.mode(self.aff_file), 0o600)
        self.assertEqual(self.mode(self.secret), 0o700)
        self.assertEqual(gq.validate_affinity(data, TABLE), [])

    def test_from_state_is_idempotent_and_keeps_scores(self):
        self.register_all()
        self.add("caleb", 2)
        out, _ = self.run_cmd("affinity", "register", "--from-state")
        self.assertIn("already registered", out)
        self.assertEqual(self.aff("caleb")["affinity"], 2)

    def test_register_single_defaults_and_explicit(self):
        self.init_party()
        self.run_cmd("affinity", "register", "sam")
        self.assertEqual(self.aff("sam")["character"], "Donut")
        self.run_cmd("affinity", "register", "guest", "--name", "Guest", "--character", "Mr Test", "--floor", "4")
        self.assertEqual(self.aff("guest")["last_drift_floor"], 4)
        _, err = self.run_cmd("affinity", "register", "sam", expect=1)
        self.assertIn("already registered", err)
        _, err = self.run_cmd("affinity", "register", "stranger", expect=1)   # not in state.json, no --name/--character
        self.assertIn("--name", err)
        self.run_cmd("affinity", "register", "Bad Id!", "--name", "x", "--character", "y", expect=1)

    def test_register_works_without_state_json(self):
        self.run_cmd("affinity", "register", "ann", "--name", "Ann", "--character", "Mongo")
        self.assertEqual(self.aff("ann")["last_drift_floor"], 0)


class AffinityAddTests(Base):
    def setUp(self):
        super().setUp()
        self.register_all()

    def test_reason_is_required(self):
        before = slurp(self.aff_file, "rb")
        self.run_cmd("affinity", "add", "caleb", "1", "--scene", "s", "--floor", "1", "--session", "S", expect=2)        # missing option
        _, err = self.add("caleb", 1, reason="   ", expect=1)                                                              # blank
        self.assertIn("--reason is required", err)
        self.assertEqual(slurp(self.aff_file, "rb"), before)
        self.assertEqual(self.log_lines(), [])

    def test_unregistered_player_rejected(self):
        _, err = self.add("nobody", 1, expect=1)
        self.assertIn("not registered", err)
        self.assertEqual(self.log_lines(), [])

    def test_no_affinity_file_yet(self):
        os.unlink(self.aff_file)
        _, err = self.add("caleb", 1, expect=1)
        self.assertIn("register", err)

    def test_delta_range(self):
        for bad in (0, 11, -11):
            _, err = self.add("caleb", bad, expect=1)
            self.assertIn("delta", err)
        self.run_cmd("affinity", "add", "caleb", "abc", "--reason", "x", "--scene", "s", "--floor", "1", "--session", "S", expect=2)
        self.add("caleb", -3)
        self.add("caleb", "+2", "s1")

    def test_basic_add_updates_state_and_log(self):
        self.seal(fx=1)
        out, _ = self.add("CALEB", 2, "scene-7", 3, "S02", "bragged about boots", "--evidence", "my boots are the best",
                          "--fixation-id", "FX-01", "--trigger", "boot")
        self.assertIn("+2 applied", out)
        self.assertIn("[GM-ONLY]", out)
        p = self.aff("caleb")
        self.assertEqual((p["affinity"], p["scene_id"], p["scene_delta"]), (2, "scene-7", 2))
        (entry,) = self.log_lines()
        self.assertEqual(list(entry), gq.LOG_KEYS)
        self.assertEqual((entry["session"], entry["floor"], entry["scene"], entry["player_id"], entry["kind"]), ("S02", 3, "scene-7", "caleb", "event"))
        self.assertEqual((entry["raw_delta"], entry["delta"], entry["affinity_before"], entry["affinity_after"], entry["capped"]), (2, 2, 0, 2, False))
        self.assertEqual((entry["reason"], entry["evidence"], entry["fixation_id"], entry["matched_trigger"]),
                         ("bragged about boots", "my boots are the best", "FX-01", "boot"))
        self.assertEqual(self.mode(self.log_file), 0o600)

    def test_scene_cap_clamps_and_records_raw_vs_applied(self):
        self.add("caleb", 3)
        out, _ = self.add("caleb", 2)
        self.assertIn("CAPPED", out)
        self.assertEqual(self.aff("caleb")["affinity"], 3)
        self.assertEqual(self.aff("caleb")["scene_delta"], 3)
        entries = self.log_lines()
        self.assertEqual([(e["raw_delta"], e["delta"], e["capped"]) for e in entries], [(3, 3, False), (2, 0, True)])

    def test_partial_cap(self):
        self.add("caleb", 2)
        self.add("caleb", 3)
        e = self.log_lines()[-1]
        self.assertEqual((e["raw_delta"], e["delta"], e["capped"], e["affinity_after"]), (3, 1, True, 3))

    def test_negative_cap_and_net_semantics(self):
        self.add("caleb", -3)
        self.add("caleb", -1)
        self.assertEqual((self.aff("caleb")["affinity"], self.aff("caleb")["scene_delta"]), (-3, -3))
        self.add("caleb", 3)            # net is -3 -> only +3 more allowed up to the +3 ceiling: all of it goes through
        self.assertEqual((self.aff("caleb")["affinity"], self.aff("caleb")["scene_delta"]), (0, 0))
        self.add("caleb", 3)
        self.assertEqual(self.aff("caleb")["affinity"], 3)
        e = self.log_lines()[-1]
        self.assertFalse(e["capped"])

    def test_big_requested_delta_is_clamped_to_scene_cap(self):
        self.add("caleb", 9)
        e = self.log_lines()[-1]
        self.assertEqual((e["raw_delta"], e["delta"], e["capped"]), (9, 3, True))

    def test_new_scene_id_restarts_the_tally(self):
        self.add("caleb", 3, "s1")
        self.add("caleb", 3, "s2")
        p = self.aff("caleb")
        self.assertEqual((p["affinity"], p["scene_id"], p["scene_delta"]), (6, "s2", 3))

    def test_tallies_are_per_player(self):
        self.add("caleb", 3)
        self.add("sam", 3)
        self.assertEqual((self.aff("caleb")["affinity"], self.aff("sam")["affinity"]), (3, 3))

    def test_range_clamp_at_plus_and_minus_ten(self):
        for i in range(4):
            self.add("caleb", 3, f"up{i}")
        self.assertEqual(self.aff("caleb")["affinity"], 10)
        out, _ = self.add("caleb", 3, "up-x")
        self.assertIn("CAPPED", out)
        e = self.log_lines()[-1]
        self.assertEqual((e["raw_delta"], e["delta"], e["affinity_before"], e["affinity_after"], e["capped"]), (3, 0, 10, 10, True))
        for i in range(8):
            self.add("sam", -3, f"dn{i}")
        self.assertEqual(self.aff("sam")["affinity"], -10)
        self.assertEqual(self.aff("sam")["scene_delta"], 0)       # the range clamp ate it: scene tally only counts applied points

    def test_evidence_word_limit(self):
        self.add("caleb", 1, "s1", 1, "S", "ok", "--evidence", " ".join(["w"] * 25))
        _, err = self.add("caleb", 1, "s2", 1, "S", "too long", "--evidence", " ".join(["w"] * 26), expect=1)
        self.assertIn("25 words", err)

    def test_fixation_id_must_match_the_sealed_fixation(self):
        _, err = self.add("caleb", 1, "s1", 1, "S", "r", "--fixation-id", "FX-07", expect=1)      # nothing sealed yet
        self.assertIn("does not match", err)
        self.seal(fx=7)
        self.add("caleb", 1, "s1", 1, "S", "r", "--fixation-id", "fx-07")
        _, err = self.add("caleb", 1, "s1", 1, "S", "r", "--fixation-id", "FX-09", expect=1)
        self.assertIn("does not match", err)
        self.assertNotIn("FX-07", err)             # a wrong guess is never told the real one
        _, err = self.add("caleb", 1, "s1", 1, "S", "r", "--fixation-id", "FX-99", expect=1)
        self.assertIn("table", err)
        self.assertEqual(len(self.log_lines()), 1)

    def test_every_write_backs_up_the_previous_file(self):
        backups = os.path.join(self.secret, "backups")
        self.add("sam", 1)          # make sure the backups folder exists (the very first write has nothing to back up)
        n0 = self.nbackups()
        before = slurp(self.aff_file, "rb")
        self.add("caleb", 1)
        files = sorted(os.listdir(backups))
        self.assertEqual(len(files), n0 + 1)
        newest = max((os.path.join(backups, f) for f in files), key=os.path.getmtime)
        self.assertEqual(slurp(newest, "rb"), before)
        self.assertEqual(self.mode(newest), 0o600)
        self.assertEqual(self.mode(backups), 0o700)

    def test_backup_rotation_keeps_newest_20(self):
        for i in range(25):
            self.add("caleb", 1 if i % 2 == 0 else -1, f"s{i}")
        self.assertEqual(len(os.listdir(os.path.join(self.secret, "backups"))), 20)

    def test_invalid_existing_file_is_never_overwritten(self):
        bad = self.read_json(self.aff_file)
        bad["players"]["caleb"]["affinity"] = 99
        self.write(self.aff_file, json.dumps(bad))
        before = slurp(self.aff_file, "rb")
        _, err = self.add("caleb", 1, expect=1)
        self.assertIn("invalid", err)
        self.assertEqual(slurp(self.aff_file, "rb"), before)
        self.write(self.aff_file, "{oops")
        _, err = self.add("caleb", 1, expect=1)
        self.assertIn("not valid JSON", err)
        self.assertEqual(slurp(self.aff_file), "{oops")

    def test_no_temp_or_lock_files_left_behind(self):
        self.add("caleb", 1)
        self.run_cmd("affinity", "drift", "--floor", "2")
        left = [f for f in os.listdir(self.secret) if f.startswith(".tmp-") or f.endswith(".lock")]
        self.assertEqual(left, [])

    def test_parallel_adds_are_serialized_and_capped(self):
        procs = [self.sub("affinity", "add", "caleb", "1", "--reason", f"r{i}", "--scene", "same", "--floor", "1", "--session", "S") for i in range(8)]
        for p in procs:
            out, err = p.communicate(timeout=90)
            self.assertEqual(p.returncode, 0, out + err)
        self.assertEqual(self.aff("caleb")["affinity"], 3)
        entries = self.log_lines()
        self.assertEqual(len(entries), 8)
        self.assertEqual(sum(e["capped"] for e in entries), 5)
        self.assertEqual(sum(e["delta"] for e in entries), 3)

    def test_gm_quirks_affinity_alias(self):
        self.run_cmd("gm-quirks", "affinity", "add", "caleb", "1", "--reason", "x", "--scene", "s", "--floor", "1", "--session", "S")
        out, _ = self.run_cmd("gm-quirks", "affinity", "status", "caleb")
        self.assertIn("+1", out)

    def test_json_output_has_warning(self):
        out, _ = self.run_cmd("affinity", "add", "caleb", "2", "--reason", "x", "--scene", "s", "--floor", "1", "--session", "S", "--json")
        data = json.loads(out)
        self.assertEqual((data["delta"], data["affinity"], data["band"]), (2, 2, "Neutral"))
        self.assertIn("GM-ONLY", data["warning"])


class OptOutTests(Base):
    def setUp(self):
        super().setUp()
        self.register_all()
        self.run_cmd("set", "crawlers.grimsby.fan_profile.opt_outs", '["mom jokes", "hairpiece"]')

    def test_opted_out_fixation_topic_is_never_scored(self):
        self.seal(fx=13)   # Moms
        before = slurp(self.aff_file, "rb")
        for sign in (1, -2):
            _, err = self.add("caleb", sign, "s1", 1, "S", "reacted", "--fixation-id", "FX-13", expect=1)
            self.assertIn("private opt-out", err)
        self.assertEqual(slurp(self.aff_file, "rb"), before)
        self.assertEqual(self.log_lines(), [])

    def test_trigger_reason_and_evidence_are_checked(self):
        self.add("caleb", 1, "s1", 1, "S", "x", "--trigger", "your hairpiece", expect=1)
        self.add("caleb", -1, "s1", 1, "S", "x", "--evidence", "told a mom jokes story", expect=1)
        self.add("caleb", 1, "s1", 1, "S", "he laughed at the mom jokes", expect=1)
        self.assertEqual(self.log_lines(), [])

    def test_other_topics_and_other_players_are_scored(self):
        self.add("caleb", 1, "s1", 1, "S", "praised soup")
        self.add("sam", 1, "s1", 1, "S", "mom jokes are fine for sam", "--trigger", "mom")
        self.assertEqual(len(self.log_lines()), 2)

    def test_refusal_does_not_echo_the_opt_out_list(self):
        _, err = self.add("caleb", 1, "s1", 1, "S", "x", "--trigger", "hairpiece", expect=1)
        self.assertNotIn("hairpiece", err)
        self.assertNotIn("mom jokes", err)

    def test_unreadable_state_blocks_scoring(self):
        self.write(os.path.join(self.root, "sessions", "state.json"), "{broken")
        _, err = self.add("caleb", 1, expect=1)
        self.assertIn("opt-out", err)
        self.assertEqual(self.log_lines(), [])

    def test_drift_is_not_an_opt_out_topic(self):
        self.add("sam", 3)
        self.run_cmd("affinity", "drift", "--floor", "2")
        self.assertEqual(self.aff("sam")["affinity"], 2)


class DriftTests(Base):
    def setUp(self):
        super().setUp()
        self.register_all()

    def test_drift_moves_one_point_toward_zero(self):
        self.add("caleb", 3)
        self.add("sam", -2)
        self.add("ann", 1, "s1")
        out, _ = self.run_cmd("affinity", "drift", "--floor", "2", "--session", "S2")
        self.assertEqual((self.aff("caleb")["affinity"], self.aff("sam")["affinity"], self.aff("ann")["affinity"], self.aff("bo")["affinity"]), (2, -1, 0, 0))
        self.assertTrue(all(p["last_drift_floor"] == 2 for p in self.read_json(self.aff_file)["players"].values()))
        drifts = [e for e in self.log_lines() if e["kind"] == "drift"]
        self.assertEqual(sorted((e["player_id"], e["delta"], e["affinity_before"], e["affinity_after"]) for e in drifts),
                         [("ann", -1, 1, 0), ("caleb", -1, 3, 2), ("sam", 1, -2, -1)])    # zero scores log nothing
        self.assertEqual(set(drifts[0]), set(gq.LOG_KEYS))
        self.assertEqual(drifts[0]["session"], "S2")

    def test_repeated_calls_for_the_same_floor_are_idempotent(self):
        for pid in ("caleb", "sam"):
            for i in range(3):
                self.add(pid, 3, f"{pid}{i}")
        self.run_cmd("affinity", "drift", "--floor", "2")
        snap = slurp(self.aff_file, "rb").replace(b"\n", b"")
        logs = len(self.log_lines())
        out, _ = self.run_cmd("affinity", "drift", "--floor", "2")
        self.assertIn("already drifted", out)
        self.run_cmd("affinity", "drift", "--floor", "2")
        self.assertEqual(self.aff("caleb")["affinity"], 8)
        self.assertEqual(len(self.log_lines()), logs)
        self.assertEqual(json.loads(slurp(self.aff_file))["players"]["caleb"]["last_drift_floor"], 2)

    def test_earlier_floor_does_not_drift_again(self):
        self.add("caleb", 3)
        self.run_cmd("affinity", "drift", "--floor", "3")
        self.run_cmd("affinity", "drift", "--floor", "2")
        self.assertEqual(self.aff("caleb")["affinity"], 2)

    def test_next_floor_drifts_again_and_never_overshoots_zero(self):
        self.add("caleb", 1)
        self.run_cmd("affinity", "drift", "--floor", "2")
        self.run_cmd("affinity", "drift", "--floor", "3")
        self.assertEqual(self.aff("caleb")["affinity"], 0)
        self.run_cmd("affinity", "drift", "--floor", "4")
        self.assertEqual(self.aff("caleb")["affinity"], 0)

    def test_skipping_floors_still_drifts_one_point(self):
        self.add("caleb", 3)
        self.run_cmd("affinity", "drift", "--floor", "5")
        self.assertEqual(self.aff("caleb")["affinity"], 2)

    def test_floor_of_registration_owes_no_drift(self):
        self.add("caleb", 2)
        self.run_cmd("affinity", "drift", "--floor", "1")      # registered during floor 1
        self.assertEqual(self.aff("caleb")["affinity"], 2)

    def test_drift_does_not_touch_the_scene_tally_and_is_backed_up(self):
        self.add("caleb", 3)
        n = self.nbackups()
        self.run_cmd("affinity", "drift", "--floor", "2")
        self.assertEqual(self.aff("caleb")["scene_delta"], 3)
        self.assertEqual(self.nbackups(), n + 1)

    def test_floor_validation(self):
        self.run_cmd("affinity", "drift", "--floor", "0", expect=1)
        self.run_cmd("affinity", "drift", expect=2)


class StatusAndSceneTests(Base):
    def setUp(self):
        super().setUp()
        self.register_all()

    def test_status_shows_affinity_band_and_scene_delta(self):
        self.add("caleb", 3, scene="alpha")
        out, _ = self.run_cmd("affinity", "status", "caleb")
        self.assertIn("GM-ONLY", out.splitlines()[0])
        self.assertIn("affinity +3 [Mild perks]", out)
        self.assertIn("scene 'alpha' delta +3/3", out)
        out, _ = self.run_cmd("affinity", "status")
        self.assertEqual(len([l for l in out.splitlines() if "affinity" in l]), 4)
        self.run_cmd("affinity", "status", "nobody", expect=1)

    def test_every_score_maps_to_the_band_from_the_json(self):
        data = self.read_json(self.aff_file)
        for v in range(-10, 11):
            data["players"]["caleb"]["affinity"] = v
            with open(self.aff_file, "w") as f:
                json.dump(data, f)
            out, _ = self.run_cmd("affinity", "status", "caleb", "--json")
            want = next(b["name"] for b in TABLE["meta"]["affinity"]["bands"] if b["min"] <= v <= b["max"])
            self.assertEqual(json.loads(out)["players"][0]["band"], want, v)

    def test_status_is_read_only(self):
        before = slurp(self.aff_file, "rb")
        n = self.nbackups()
        self.run_cmd("affinity", "status")
        self.assertEqual(slurp(self.aff_file, "rb"), before)
        self.assertEqual(self.nbackups(), n)

    def test_new_scene_resets_all_scene_deltas(self):
        self.add("caleb", 3, "s1")
        self.add("sam", -2, "s1")
        self.run_cmd("affinity", "new-scene", "s2")
        for pid in ("caleb", "sam", "ann", "bo"):
            self.assertEqual((self.aff(pid)["scene_id"], self.aff(pid)["scene_delta"]), ("s2", 0))
        self.assertEqual(self.aff("caleb")["affinity"], 3)       # scores untouched
        self.add("caleb", 3, "s2")                                # a fresh cap
        self.assertEqual(self.aff("caleb")["affinity"], 6)

    def test_repeating_the_current_scene_id_does_not_reopen_the_cap(self):
        self.add("caleb", 3, "s1")
        out, _ = self.run_cmd("affinity", "new-scene", "s1")
        self.assertEqual(self.aff("caleb")["scene_delta"], 3)
        self.add("caleb", 2, "s1")
        self.assertEqual(self.aff("caleb")["affinity"], 3)


# =========================================================================== secrecy

class SecrecyTests(Base):
    MARK_REASON = "ZZREASON-91827"
    MARK_EVIDENCE = "ZZEVIDENCE-77412"

    def build_campaign(self):
        self.init_party()
        self.rolls = self.seal(pi=5, fx=7, q1=11, q2=3, tic=4)
        self.run_cmd("affinity", "register", "--from-state")
        self.add("caleb", 3, "s1", 1, "S1", self.MARK_REASON, "--evidence", self.MARK_EVIDENCE, "--fixation-id", "FX-07", "--trigger", "soup")
        self.run_cmd("affinity", "drift", "--floor", "2")
        data = self.read_json(self.roll_file)
        secrets_ = [data["nonce"], self.MARK_REASON, self.MARK_EVIDENCE]
        for key, table in (("prior_installation", "prior_installation"), ("fixation", "fixations"), ("tic", "tics")):
            e = gq.entry_by_id(TABLE[table], data["rolls"][key])
            secrets_ += [e["id"], e["name"], e["description"][:40]]
        for q in data["rolls"]["quirks"]:
            e = gq.entry_by_id(TABLE["quirks"], q)
            secrets_ += [e["id"], e["name"], e["description"][:40]]
        return secrets_

    def public_commands(self):
        return [
            ["show"], ["show", "grimsby"], ["show", "--json"], ["show", "grimsby", "--json"], ["--json", "show"], ["get", "campaign.name"], ["get", "crawlers"],
            ["get", "party"], ["validate"], ["validate", "--json"], ["backups"], ["snapshot"], ["hp", "damage", "grimsby", "3"], ["hp", "heal", "grimsby", "3"],
            ["inventory", "add", "donut", "Rope"], ["credits", "mongo", "+10"], ["achievement", "add", "carl", "Hi"], ["condition", "add", "carl", "prone"],
            ["box", "add", "carl", "bronze"], ["use-bypass", "carl"], ["use-revive", "carl", "--dry-run"], ["set", "campaign.zone", "Pit"], ["backups", "--json"],
            ["gm-quirks", "status"], ["gm-quirks", "status", "--json"], ["gm-quirks", "level", "6"], ["gm-quirks", "level", "6", "--json"],
            ["--help"], ["gm-quirks", "--help"], ["affinity", "--help"], ["gm-quirks", "roll", "--help"], ["snapshot"], ["restore", "nonexistent.json"],
        ]

    def test_secret_content_never_appears_in_any_public_command_output(self):
        secrets_ = self.build_campaign()
        for argv in self.public_commands():
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                try:
                    state.main(list(argv))
                except SystemExit:
                    pass
            text = out.getvalue() + err.getvalue()
            self.assertFalse(ID_RE.search(text), f"{argv}: trait id in output")
            for s in secrets_:
                self.assertNotIn(s, text, f"{argv}: leaked {s[:20]!r}")
        # a second pass with state.main running as a real subprocess (what the GM actually does)
        for argv in (["show"], ["validate"], ["snapshot"], ["backups"], ["gm-quirks", "status"], ["gm-quirks", "level", "9"]):
            p = self.sub(*argv)
            out, err = p.communicate(timeout=60)
            for s in secrets_:
                self.assertNotIn(s, out + err, f"{argv}: leaked {s[:20]!r} (subprocess)")

    def test_no_file_outside_the_secret_folder_contains_secrets(self):
        secrets_ = self.build_campaign()
        for argv in self.public_commands():
            try:
                self.run_cmd(*argv, expect=0)
            except AssertionError:
                pass
            except SystemExit:
                pass
        self.run_cmd("init", "--force")      # make the backup rotation and a second snapshot happen too
        self.run_cmd("snapshot")
        scanned = 0
        for base, dirs, files in os.walk(self.root):
            if os.path.realpath(base).startswith(os.path.realpath(self.secret)):
                continue
            for f in files:
                scanned += 1
                with open(os.path.join(base, f), encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
                self.assertFalse(ID_RE.search(text), os.path.join(base, f))
                for s in secrets_:
                    self.assertNotIn(s, text, os.path.join(base, f))
        self.assertGreater(scanned, 4)    # state, backups, snapshot, roll log, ...
        self.assertTrue(os.path.exists(self.roll_file))   # and the secrets really are in the secret folder

    def test_state_snapshot_and_show_do_not_read_the_secret_folder(self):
        self.build_campaign()
        opened = []
        real_open = open

        def spy(path, *a, **k):
            if isinstance(path, (str, bytes, os.PathLike)) and os.path.realpath(os.fsdecode(path)).startswith(os.path.realpath(self.secret)):
                opened.append(path)
            return real_open(path, *a, **k)
        with mock.patch("builtins.open", spy):
            for argv in (["show"], ["show", "grimsby"], ["snapshot"], ["validate"], ["backups"], ["get", "campaign"], ["hp", "damage", "carl", "1"]):
                self.run_cmd(*argv)
        self.assertEqual(opened, [])

    def test_state_py_refuses_to_read_secret_files_as_state(self):
        self.build_campaign()
        for argv in (["validate", "--file", self.roll_file], ["validate", "--file", self.aff_file], ["restore", self.roll_file],
                     ["restore", "../gm-notes/secret/gm-quirk-roll.json"]):
            _, err = self.run_cmd(*argv, expect=1)
            self.assertNotIn(self.read_json(self.roll_file)["nonce"], err)
        _, err = self.run_cmd("validate", "--file", self.roll_file, expect=1)
        self.assertIn("gm-notes/secret", err)

    def test_secret_files_are_private(self):
        self.build_campaign()
        self.assertEqual(self.mode(self.secret), 0o700)
        for base, dirs, files in os.walk(self.secret):
            for d in dirs:
                self.assertEqual(self.mode(os.path.join(base, d)), 0o700, d)
            for f in files:
                self.assertEqual(self.mode(os.path.join(base, f)), 0o600, f)

    def test_errors_do_not_leak_either(self):
        secrets_ = self.build_campaign()
        for argv in (["gm-quirks", "roll"], ["gm-quirks", "roll", "--force"], ["affinity", "add", "caleb", "1", "--reason", "x", "--scene", "s", "--floor", "1",
                                                                            "--session", "S", "--fixation-id", "FX-02"], ["gm-quirks", "reveal"]):
            _, err = self.run_cmd(*argv, expect=1)
            self.assertFalse(ID_RE.search(err))
            for s in secrets_:
                self.assertNotIn(s, err)

    def test_repo_docs_do_not_index_or_contain_secret_content(self):
        for rel in ("INDEX.md", "tools/INDEX.md", "exports/INDEX.md", "sessions/INDEX.md", "tools/README.md"):
            path = os.path.join(CAMPAIGN_REAL, rel)
            if not os.path.exists(path):
                continue
            text = slurp(path)
            self.assertFalse(ID_RE.search(text), f"{rel} contains trait ids")
            if rel != "tools/README.md":
                self.assertNotIn("gm-notes/secret/", text, f"{rel} must not index the secret folder")
                self.assertNotIn("gm-quirk-roll", text, rel)
        gm_index = slurp(os.path.join(CAMPAIGN_REAL, "gm-notes", "INDEX.md"))
        self.assertIn("gm-notes/secret/", gm_index)           # one generic line for the folder
        self.assertNotIn("gm-quirk-roll", gm_index)
        self.assertNotIn("gm-affinity", gm_index)
        readme = slurp(os.path.join(CAMPAIGN_REAL, "tools", "README.md"))
        self.assertIn("GM-ONLY", readme)
        for fx in TABLE["fixations"]:
            self.assertNotIn(fx["name"], readme, "the fixation list must not be in the public README")


# =========================================================================== sim_floors

class SimTests(unittest.TestCase):
    def test_simulation_skeleton_runs_and_is_consistent(self):
        spec2 = importlib.util.spec_from_file_location("sim_floors", os.path.join(TOOLS, "sim_floors.py"))
        sim = importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(sim)
        rows = sim.simulate(TABLE, trials=60, floors=12, seed=3)
        self.assertEqual(len(rows), 12)
        for r in rows:
            self.assertAlmostEqual(sum(r["band_share"].values()), 1.0, places=1)
            self.assertAlmostEqual(sum(r["level_mix"].values()), 1.0, places=1)
        self.assertEqual(rows[0]["p_any_glitch"] <= rows[-1]["p_any_glitch"], True)
        self.assertEqual(sim.simulate(TABLE, trials=20, seed=5), sim.simulate(TABLE, trials=20, seed=5))   # seeded
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(sim.main(["--trials", "20", "--floors", "3", "--json"]), 0)
        self.assertEqual(len(json.loads(out.getvalue())), 3)
        self.assertEqual(sim.main(["--trials", "0"]), 2)


if __name__ == "__main__":
    unittest.main()
