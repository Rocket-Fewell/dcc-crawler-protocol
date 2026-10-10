"""Floor 1 through Floor 3 on the local table. Day pages stay the voice. Nothing here writes the live game."""

from dcc_engine.cards import filed_party, party_note
from dcc_engine.player_card import seat_raithen
from dcc_engine.script import load_script, npc_names
from dcc_engine.table import Table

_NEXT = (
    "next",
    "continue",
    "move on",
    "go on",
    "we move on",
    "i move on",
    "onward",
    "keep going",
)


def _ready(crawler):
    crawler["action"] = True
    crawler["bonus"] = True
    crawler["reaction"] = True
    crawler["object"] = True
    crawler["movement_left"] = crawler.get("speed_ft") or 30
    crawler["ac_bonus"] = 0
    crawler["cover"] = None
    crawler["disadvantage_on_attack"] = False
    crawler["advantage_on_attack"] = False


def _say_line(line):
    voice = line.get("voice") or "GM"
    text = (line.get("text") or "").strip()
    if not text:
        return None
    if voice == "SYSTEM":
        return {"voice": "SYSTEM", "speak": True, "text": "[SYSTEM] " + text}
    if voice == "NPC":
        name = line.get("npc") or "NPC"
        return {"voice": "NPC", "speak": True, "text": f"[NPC: {name}] {text}"}
    return {"voice": "GM", "speak": True, "text": "[GM] " + text}


def _room_for(scene):
    if scene.get("room"):
        return scene["room"]
    slots = []
    for enemy in scene.get("enemies") or []:
        if not enemy.get("stat_card"):
            continue
        counts = enemy.get("counts_by_party_size")
        if not counts:
            count = int(enemy.get("count") or 1)
            counts = {"2": count, "3": count, "4": count}
        slots.append({
            "spoken_name": enemy.get("spoken_name") or "",
            "stat_card": enemy["stat_card"],
            "counts_by_party_size": counts,
        })
    if not slots:
        return None
    return {
        "id": scene["key"],
        "name": scene["title"],
        "narrator_line": scene["title"],
        "read_aloud": "",
        "layout": "",
        "features": [],
        "exits": [],
        "encounter": {"enemies": slots, "quick_run": {}},
    }


class Playthrough:
    """One seat, every filed scene, then the local Floor 3 script."""

    def __init__(self, party_size=2, rng=None):
        self.party_size, self.count_key = filed_party(party_size)
        self.rng = rng
        self.scenes = load_script()
        self.index = 0
        self.crawler = seat_raithen()
        self.known_npcs = set(npc_names())
        self.fight = None
        self.log = []
        self.said = set()
        self._enter()

    @property
    def scene(self):
        if self.index >= len(self.scenes):
            return None
        return self.scenes[self.index]

    @property
    def done(self):
        return self.scene is None

    def _push(self, line):
        if line.get("voice") == "NPC" and line.get("npc") not in self.known_npcs:
            line = dict(line)
            line["voice"] = "GM"
        packed = _say_line(line)
        if packed:
            self.log.append(packed)
        return packed

    def _lines(self, when):
        scene = self.scene
        if not scene:
            return []
        spoken = []
        for line in scene.get("lines") or []:
            if line.get("when") != when:
                continue
            key = (scene["key"], when, line.get("text"))
            if key in self.said:
                continue
            self.said.add(key)
            packed = self._push(line)
            if packed:
                spoken.append(packed)
        return spoken

    def _enter(self):
        scene = self.scene
        if not scene:
            self._push({
                "voice": "GM",
                "text": "That's the county. Floor 3 is behind you. The narrator had a wonderful time. You should be concerned.",
            })
            return
        self._lines("open")
        room = _room_for(scene)
        self.fight = None
        if not room:
            return
        _ready(self.crawler)
        try:
            fight = Table(
                party_size=self.party_size,
                room=room,
                use_slot_names=True,
                quiet=True,
                seated=self.crawler,
            )
        except (KeyError, ValueError, StopIteration):
            self._push({
                "voice": "GM",
                "text": "No local attack card for that body yet. The line still stands. Say next.",
            })
            return
        if not fight.enemies:
            return
        self.fight = fight
        self._push({
            "voice": "SYSTEM",
            "text": "Your turn. One action, one bonus action, one reaction, one free object interaction, and your movement.",
        })

    def advance(self):
        if self.done:
            return {"ok": True, "say": [], "view": self.view(), "done": True}
        say = self._lines("win")
        self.fight = None
        self.index += 1
        before = len(self.log)
        self._enter()
        say.extend(self.log[before:])
        return {"ok": True, "say": say, "view": self.view(), "done": self.done}

    def resolve_line(self, text):
        raw = (text or "").strip()
        low = " ".join(raw.lower().split())
        if low in _NEXT or low.startswith("next "):
            return self.advance()
        if self.fight is not None:
            result = self.fight.resolve_line(raw, rng=self.rng)
            if result.get("say"):
                self.log.extend(result["say"])
            alive = [enemy for enemy in self.fight.enemies if enemy["hp"] > 0]
            if self.fight.enemies and not alive:
                result.setdefault("say", [])
                result["say"].extend(self._lines("win"))
            elif alive and sum(enemy["hp"] for enemy in alive) * 2 <= sum(enemy["hp_max"] for enemy in self.fight.enemies):
                result.setdefault("say", [])
                result["say"].extend(self._lines("mid"))
            result["view"] = self.view()
            return result
        self._push({
            "voice": "GM",
            "text": "Say it like you mean it, or say next. The floor heard you. It is choosing to be difficult about it.",
        })
        return {
            "ok": True,
            "say": [self.log[-1]],
            "view": self.view(),
            "nothing": True,
        }

    def your_turn(self):
        if self.done:
            return False
        if self.fight is not None and any(enemy["hp"] > 0 for enemy in self.fight.enemies):
            return self.fight.your_turn()
        return int(self.crawler.get("death_fail") or 0) < 3

    def view(self):
        scene = self.scene
        fight = self.fight.player_view() if self.fight is not None else None
        crawler = fight["crawler"] if fight else {
            "name": self.crawler["name"],
            "class_name": self.crawler["class_name"],
            "level": self.crawler["level"],
            "hp": self.crawler["hp"],
            "hp_max": self.crawler["hp_max"],
            "ac": self.crawler["ac"],
            "attacks": [],
            "spells": [],
        }
        return {
            "mode": "playthrough",
            "party_size": self.party_size,
            "count_key": self.count_key,
            "party_line": party_note(self.party_size, self.count_key),
            "done": self.done,
            "index": self.index,
            "count": len(self.scenes),
            "floor": None if scene is None else scene["floor"],
            "day": None if scene is None else scene["day"],
            "scene_id": None if scene is None else scene["id"],
            "title": "Floor 3 is behind you" if scene is None else scene["title"],
            "kind": "" if scene is None else scene["kind"],
            "your_turn": self.your_turn(),
            "crawler": crawler,
            "enemies": [] if fight is None else fight["enemies"],
            "log": [{"voice": line["voice"], "text": line["text"]} for line in self.log],
        }
