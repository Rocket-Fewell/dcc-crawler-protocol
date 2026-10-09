"""In-memory Shooting Gallery. Code rolls. A line is resolved once. Undo restores it."""

import copy
import re

from dcc_engine.cards import (
    crawler_from_card,
    gallery_count,
    has_cunning,
    load_monster,
    load_pilot,
    load_room,
    monster_combatant,
)
from dcc_engine.clauses import classify, is_question, split_clauses
from dcc_engine.dice import double_dice, roll_expr
from dcc_engine.narrate import attack_gm, enemy_gm, pack

_TARGET_OTHER = re.compile(r"\b(?:other|second|2|b)\b", re.IGNORECASE)
_TARGET_FIRST = re.compile(r"\b(?:first|1|a)\b", re.IGNORECASE)
_DICE_EXPR = re.compile(r"^\d*d\d+(?:[+-]\d+)?$")
COVER_FT = 15
CLOSE_FT = 30


class ScriptedRng:
    """Test die. Production passes nothing and roll.py uses SystemRandom."""

    def __init__(self, numbers):
        self.numbers = list(numbers)

    def randint(self, low, high):
        if not self.numbers:
            raise RuntimeError("scripted dice ran out")
        rolled = self.numbers.pop(0)
        if rolled < low or rolled > high:
            raise RuntimeError(f"scripted {rolled} is outside {low}..{high}")
        return rolled


class Table:
    def __init__(self, party_size=2, crawler=None):
        room = load_room("enc-d01-11")
        count, stat_id = gallery_count(room, party_size)
        monster = load_monster(stat_id)
        self.room_id = room["id"]
        self.room_name = room["name"]
        self.narrator_line = room["narrator_line"]
        self.gm_note = room.get("gm_notes") or ""
        self.party_size = party_size if str(party_size) in {"2", "3", "4"} else 2
        self.enemies = [monster_combatant(monster, index) for index in range(1, count + 1)]
        self.crawler = crawler_from_card(crawler or load_pilot())
        self.round = 1
        self.in_melee = False
        self.held = None
        self.last_target = None
        self.log = []
        self.raw = []
        self._undo = []
        self.resolutions = 0
        self.log.append({
            "voice": "GM",
            "speak": True,
            "text": "[GM] " + self.narrator_line,
        })
        self.log.append({
            "voice": "SYSTEM",
            "speak": True,
            "text": (
                "[SYSTEM] Your turn. One action, one bonus action, one reaction, "
                "one free object interaction, and your movement."
            ),
        })

    def player_view(self):
        crawler = self.crawler
        return {
            "room": self.room_name,
            "round": self.round,
            "narrator_line": self.narrator_line,
            "in_melee": self.in_melee,
            "crawler": _public_crawler(crawler),
            "enemies": [_public_enemy(enemy) for enemy in self.enemies],
            "log": list(self.log),
            "gallery_clear": all(enemy["hp"] <= 0 for enemy in self.enemies),
        }

    def gm_view(self):
        view = self.player_view()
        view["raw"] = list(self.raw)
        view["gm_note"] = self.gm_note
        view["undo_depth"] = len(self._undo)
        view["resolutions"] = self.resolutions
        return view

    def seat(self, card):
        if self.resolutions:
            raise ValueError("Undo back to the open room before seating a different Crawler.")
        checked = _validate_seat(card)
        self.crawler = crawler_from_card(checked)
        self.held = None
        self.log.append({
            "voice": "SYSTEM",
            "speak": True,
            "text": f"[SYSTEM] {self.crawler['name']} is seated. The fight has not started.",
        })
        return self.player_view()

    def resolve_line(self, text, rng=None):
        spoken = (text or "").strip()
        if not spoken:
            raise ValueError("empty line")
        if is_question(spoken):
            self.raw.append(spoken)
            line = {
                "voice": "SYSTEM",
                "speak": True,
                "text": "[SYSTEM] A question does not spend the turn.",
            }
            self.log.append({"voice": "YOU", "speak": False, "text": spoken})
            self.log.append(line)
            return {"say": [line], "view": self.player_view()}

        self.raw.append(spoken)
        self.log.append({"voice": "YOU", "speak": False, "text": spoken})
        self._undo.append(self._capture())
        events = []
        clauses = split_clauses(spoken)
        stopped = False
        for index, raw in enumerate(clauses):
            clause = classify(raw, held=self.held)
            if clause["kind"] == "question":
                events.append({"channel": "system", "text": "A question does not spend the turn."})
                continue
            outcome = self._apply(clause, rng)
            events.extend(outcome["events"])
            if outcome["stop"]:
                rest = clauses[index + 1:]
                named = "; ".join(rest) if rest else clause["text"]
                if rest:
                    named = clause["text"] + "; " + "; ".join(rest)
                events.append({
                    "channel": "system",
                    "text": outcome["reason"] + " Did not happen: " + named + ".",
                })
                stopped = True
                break
        if not events:
            events.append({"channel": "system", "text": "Nothing in that line changed the table."})
        packed = pack(events)
        self.log.extend(packed)
        self.resolutions += 1
        return {"say": packed, "view": self.player_view()}

    def undo(self):
        if not self._undo:
            raise ValueError("nothing to undo")
        state = self._undo.pop()
        self._restore(state)
        self.log.append({
            "voice": "SYSTEM",
            "speak": True,
            "text": "[SYSTEM] Last resolution undone.",
        })
        return self.gm_view()

    def correct_hp(self, target_id, hp):
        target = self._find(target_id)
        if target is None:
            raise ValueError("no combatant with that id")
        value = int(hp)
        if value < 0 or value > target["hp_max"]:
            raise ValueError(f"hit points must be 0 to {target['hp_max']}")
        self._undo.append(self._capture())
        target["hp"] = value
        if target["hp"] > 0 and "down" in target["conditions"]:
            target["conditions"] = [item for item in target["conditions"] if item != "down"]
        if target["hp"] == 0 and "down" not in target["conditions"]:
            target["conditions"].append("down")
        self.resolutions += 1
        self.log.append({
            "voice": "SYSTEM",
            "speak": True,
            "text": f"[SYSTEM] Correction: {target['name']} hit points set to {value}.",
        })
        return self.gm_view()

    def _apply(self, clause, rng):
        kind = clause["kind"]
        if self.crawler["hp"] <= 0 and kind not in {"end", "question"}:
            if kind == "ruling" and "death" in clause["text"].lower():
                return self._death_save(rng)
            if re.search(r"\b(?:death save|go)\b", clause["text"], re.IGNORECASE):
                return self._death_save(rng)
            return {
                "stop": True,
                "reason": "You are at 0 hit points.",
                "events": [],
            }
        if kind == "end":
            return self._end_turn(rng)
        if kind == "flavor":
            return {"stop": False, "reason": "", "events": [
                {"channel": "gm", "text": "That costs nothing."},
            ]}
        if kind == "question":
            return {"stop": False, "reason": "", "events": [
                {"channel": "system", "text": "A question does not spend the turn."},
            ]}
        if kind == "move":
            return self._move(clause)
        if kind == "object":
            return self._object(clause)
        if kind == "attack":
            return self._player_attack(clause, rng, improvised=False)
        if kind == "ruling":
            return self._ruling(clause, rng)
        if kind in {"hide", "dash", "disengage", "dodge"}:
            return self._action_or_bonus(clause, rng)
        return {
            "stop": False,
            "reason": "",
            "events": [{"channel": "system", "text": "The System doesn't support that. Try something else."}],
        }

    def _action_or_bonus(self, clause, rng):
        crawler = self.crawler
        bonus_intent = clause["bonus"]
        feature = clause["kind"]
        label = feature.capitalize()
        if bonus_intent and not has_cunning(crawler):
            return {
                "stop": False,
                "reason": "",
                "events": [{
                    "channel": "system",
                    "text": f"Cunning Action starts at Rogue 2. {label} does not happen as a bonus action.",
                }],
            }
        if bonus_intent or (not crawler["action"] and has_cunning(crawler)):
            if not has_cunning(crawler):
                return {
                    "stop": True,
                    "reason": (
                        f"You already used your action on {crawler['spent_action']}. "
                        "Cunning Action starts at Rogue 2."
                    ),
                    "events": [],
                }
            if not crawler["bonus"]:
                return {
                    "stop": True,
                    "reason": "You already used your bonus action.",
                    "events": [],
                }
            crawler["bonus"] = False
            return self._spend_feature(clause, rng, paid="bonus action")
        if not crawler["action"]:
            if has_cunning(crawler) and crawler["bonus"] and feature in {"hide", "dash", "disengage"}:
                crawler["bonus"] = False
                return self._spend_feature(clause, rng, paid="bonus action")
            return {
                "stop": True,
                "reason": (
                    f"You already used your action on {crawler['spent_action']}. "
                    "Cunning Action starts at Rogue 2."
                    if not has_cunning(crawler) and feature in {"hide", "dash", "disengage"}
                    else f"You already used your action on {crawler['spent_action']}."
                ),
                "events": [],
            }
        crawler["action"] = False
        crawler["spent_action"] = label
        return self._spend_feature(clause, rng, paid="action")

    def _spend_feature(self, clause, rng, paid):
        feature = clause["kind"]
        crawler = self.crawler
        events = [{"channel": "system", "text": f"{feature.capitalize()} spends your {paid}."}]
        if feature == "dash":
            crawler["movement_left"] += crawler["speed_ft"]
            events.append({"channel": "gm", "text": f"You can still move {crawler['movement_left']} feet."})
        elif feature == "disengage":
            crawler["disengaged"] = True
            events.append({"channel": "gm", "text": "Your movement does not provoke this turn."})
        elif feature == "dodge":
            crawler["dodging"] = True
            events.append({"channel": "gm", "text": "Attacks against you have disadvantage until your next turn."})
        elif feature == "hide":
            events.extend(self._hide(rng))
        return {"stop": False, "reason": "", "events": events}

    def _hide(self, rng):
        crawler = self.crawler
        mod = crawler["dex_mod"] + (crawler["pb"] if "stealth" in crawler["skills"] else 0)
        dc = min(enemy["passive_perception"] for enemy in self.enemies if enemy["hp"] > 0)
        rolled = roll_expr(f"1d20{mod:+d}", rng, "Stealth", crawler["name"])
        success = rolled["total"] >= dc
        crawler["hidden"] = success
        text = "You are hidden." if success else "You are not hidden."
        return [
            {"channel": "roll", "text": rolled["line"]},
            {"channel": "system", "text": f"Stealth versus passive Perception {dc}. {text}"},
        ]

    def _move(self, clause):
        crawler = self.crawler
        need = CLOSE_FT if clause["into_melee"] else COVER_FT if clause["cover"] else 10
        if crawler["movement_left"] < need:
            return {
                "stop": False,
                "reason": "",
                "events": [{
                    "channel": "system",
                    "text": f"You have {crawler['movement_left']} feet left. That move does not happen.",
                }],
            }
        crawler["movement_left"] -= need
        events = [{"channel": "system", "text": f"Movement spent: {need} feet. {crawler['movement_left']} feet left."}]
        if clause["into_melee"]:
            self.in_melee = True
            events.append({"channel": "gm", "text": "You are in the booth. The bows are for the open floor."})
        elif clause["cover"]:
            crawler["cover"] = "half"
            events.append({"channel": "gm", "text": "You are behind half cover."})
        else:
            events.append({"channel": "gm", "text": "You move."})
        return {"stop": False, "reason": "", "events": events}

    def _object(self, clause):
        crawler = self.crawler
        if not crawler["object"]:
            return {
                "stop": False,
                "reason": "",
                "events": [{
                    "channel": "system",
                    "text": "You already used your free object interaction. That does not happen.",
                }],
            }
        crawler["object"] = False
        self.held = clause.get("held") or "item"
        events = [{"channel": "system", "text": "Free object interaction spent."}]
        if self.held == "body":
            events.append({"channel": "gm", "text": "You have the body."})
        return {"stop": False, "reason": "", "events": events}

    def _ruling(self, clause, rng):
        """No action card matched. The stand-in judge may only name an attack. Code rolls it."""
        ruling = _fake_ruling(clause["text"])
        if ruling["resolve_as"] != "attack":
            return {
                "stop": False,
                "reason": "",
                "events": [{
                    "channel": "system",
                    "text": "The System doesn't support that. Try something else.",
                }],
            }
        params = ruling["params"]
        if not _DICE_EXPR.fullmatch(params.get("damage_dice", "")):
            return {
                "stop": False,
                "reason": "",
                "events": [{"channel": "system", "text": "The System doesn't support that. Try something else."}],
            }
        if params.get("damage_type") not in {"bludgeoning", "piercing", "slashing"}:
            return {
                "stop": False,
                "reason": "",
                "events": [{"channel": "system", "text": "The System doesn't support that. Try something else."}],
            }
        note = {
            "channel": "system",
            "text": ruling["ruling"] + " Code rolls it.",
        }
        attack = self._player_attack(clause, rng, improvised=True, params=params)
        attack["events"].insert(0, note)
        return attack

    def _player_attack(self, clause, rng, improvised, params=None):
        crawler = self.crawler
        if not crawler["action"]:
            return {
                "stop": True,
                "reason": f"You already used your action on {crawler['spent_action']}.",
                "events": [],
            }
        target = _pick_target(self.enemies, clause["text"], self.last_target)
        if target is None:
            return {
                "stop": False,
                "reason": "",
                "events": [{"channel": "system", "text": "Nothing is left standing."}],
            }
        if improvised:
            bonus = crawler["str_mod"]
            attack = {
                "name": "Improvised attack",
                "to_hit": bonus,
                "damage": params["damage_dice"],
                "type": params["damage_type"],
            }
        else:
            if not crawler["attacks"]:
                return {
                    "stop": False,
                    "reason": "",
                    "events": [{"channel": "system", "text": "No attack is listed on your card."}],
                }
            attack = dict(crawler["attacks"][0])
        crawler["action"] = False
        crawler["spent_action"] = attack["name"]
        advantage = crawler["hidden"]
        crawler["hidden"] = False
        ac = target["ac"] + (0 if self.in_melee else 2)
        events = [{"channel": "system", "text": f"Action spent: {attack['name']} against {target['name']}."}]
        events.extend(_strike(
            rng,
            crawler["name"],
            attack,
            target,
            ac,
            advantage=advantage,
            disadvantage=False,
            who_phrase="you",
        ))
        self.last_target = target["id"]
        return {"stop": False, "reason": "", "events": events}

    def _end_turn(self, rng):
        events = [{"channel": "system", "text": "Turn ended."}]
        if all(enemy["hp"] <= 0 for enemy in self.enemies):
            events.append({
                "channel": "gm",
                "text": "The gallery is clear. The Day page still owns the register. This slice does not pay credits.",
            })
            self._refresh()
            return {"stop": False, "reason": "", "events": events}
        if self.crawler["hp"] <= 0:
            events.append({"channel": "system", "text": "Enemies skip a downed Crawler."})
            self._refresh()
            return {"stop": False, "reason": "", "events": events}
        for enemy in self.enemies:
            if enemy["hp"] <= 0:
                continue
            attack = dict(enemy["melee"] if self.in_melee else enemy["ranged"])
            ac = self.crawler["ac"]
            if self.crawler["cover"] == "half":
                ac += 2
            elif self.crawler["cover"] == "three-quarters":
                ac += 5
            events.extend(_strike(
                rng,
                enemy["name"],
                attack,
                self.crawler,
                ac,
                advantage=False,
                disadvantage=self.crawler["dodging"],
                who_phrase="enemy",
            ))
            if self.crawler["hp"] <= 0:
                events.append({"channel": "system", "text": "The remaining enemies skip a downed Crawler."})
                break
        self._refresh()
        events.append({"channel": "system", "text": f"Round {self.round}. Your turn."})
        return {"stop": False, "reason": "", "events": events}

    def _death_save(self, rng):
        crawler = self.crawler
        rolled = roll_expr("1d20", rng, "Death save", crawler["name"])
        total = rolled["total"]
        if rolled["nat20"] or total == 20:
            crawler["hp"] = 1
            crawler["death_success"] = 0
            crawler["death_fail"] = 0
            crawler["conditions"] = [item for item in crawler["conditions"] if item != "down"]
            note = "Natural 20. You are at 1 hit point."
        elif rolled["nat1"] or total == 1:
            crawler["death_fail"] += 2
            note = "Natural 1 counts as two failures."
        elif total >= 10:
            crawler["death_success"] += 1
            note = "Success."
        else:
            crawler["death_fail"] += 1
            note = "Failure."
        if crawler["death_success"] >= 3:
            note = "Three successes. You are stable."
        if crawler["death_fail"] >= 3:
            note = "Three failures. You are dead. Only Caleb ends a campaign."
        return {
            "stop": False,
            "reason": "",
            "events": [
                {"channel": "roll", "text": rolled["line"]},
                {"channel": "system", "text": f"Death save {total}. {note}"},
            ],
        }

    def _refresh(self):
        crawler = self.crawler
        crawler["action"] = True
        crawler["bonus"] = True
        crawler["reaction"] = True
        crawler["object"] = True
        crawler["movement_left"] = crawler["speed_ft"]
        crawler["dodging"] = False
        crawler["disengaged"] = False
        crawler["spent_action"] = ""
        self.round += 1

    def _find(self, target_id):
        if self.crawler["id"] == target_id or self.crawler["name"] == target_id:
            return self.crawler
        for enemy in self.enemies:
            if enemy["id"] == target_id or enemy["name"] == target_id:
                return enemy
        return None

    def _capture(self):
        return copy.deepcopy({
            "crawler": self.crawler,
            "enemies": self.enemies,
            "log": self.log,
            "raw": self.raw,
            "round": self.round,
            "in_melee": self.in_melee,
            "held": self.held,
            "last_target": self.last_target,
            "resolutions": self.resolutions,
        })

    def _restore(self, state):
        self.crawler = state["crawler"]
        self.enemies = state["enemies"]
        self.log = state["log"]
        self.raw = state["raw"]
        self.round = state["round"]
        self.in_melee = state["in_melee"]
        self.held = state["held"]
        self.last_target = state["last_target"]
        self.resolutions = state["resolutions"]


def _strike(rng, actor, attack, target, ac, advantage, disadvantage, who_phrase):
    bonus = int(attack["to_hit"])
    if advantage and not disadvantage:
        expr = f"2d20kh1{bonus:+d}"
    elif disadvantage and not advantage:
        expr = f"2d20kl1{bonus:+d}"
    else:
        expr = f"1d20{bonus:+d}"
    hit_roll = roll_expr(expr, rng, attack["name"], actor)
    crit = bool(hit_roll["nat20"])
    miss = bool(hit_roll["nat1"]) and not crit
    hit = crit or (not miss and hit_roll["total"] >= ac)
    events = [{"channel": "roll", "text": hit_roll["line"]}]
    damage = 0
    if hit:
        dice = attack["damage"]
        if crit:
            dice = double_dice(dice)
        damage_roll = roll_expr(dice, rng, "Damage", actor)
        damage = max(0, int(damage_roll["total"]))
        dtype = attack["type"]
        events.append({"channel": "roll", "text": damage_roll["line"]})
        if dtype in target.get("immunities", []):
            damage = 0
            events.append({"channel": "system", "text": f"Immune to {dtype}. Damage is 0."})
        elif dtype in target.get("vulnerabilities", []):
            damage *= 2
            events.append({"channel": "system", "text": f"Vulnerable to {dtype}. Damage is doubled to {damage}."})
        elif dtype in target.get("resistances", []):
            damage //= 2
            events.append({"channel": "system", "text": f"Resistant to {dtype}. Damage is halved to {damage}."})
        target["hp"] = max(0, target["hp"] - damage)
        if target["hp"] == 0 and "down" not in target["conditions"]:
            target["conditions"].append("down")
    killed = target["hp"] == 0 and hit
    if who_phrase == "you":
        events.append({
            "channel": "gm",
            "text": attack_gm(
                actor, attack["name"], target["name"], hit, damage, attack["type"],
                target["hp"], killed, crit,
            ),
        })
    else:
        events.append({
            "channel": "gm",
            "text": enemy_gm(
                actor, attack["name"], hit, damage, attack["type"], target["hp"], killed,
            ),
        })
    events.append({
        "channel": "system",
        "text": f"{'Hit' if hit else 'Miss'} versus AC {ac}." + (f" {damage} damage." if hit else ""),
    })
    return events


def _pick_target(enemies, text, last_id):
    standing = [enemy for enemy in enemies if enemy["hp"] > 0]
    if not standing:
        return None
    if _TARGET_OTHER.search(text):
        if last_id:
            for enemy in standing:
                if enemy["id"] != last_id:
                    return enemy
        if len(standing) > 1:
            return standing[1]
        return standing[-1]
    if _TARGET_FIRST.search(text):
        return standing[0]
    low = text.lower()
    for enemy in standing:
        if enemy["id"] in low or enemy["name"].lower() in low:
            return enemy
    return standing[0]


def _fake_ruling(text):
    """Stand-in for the strong model. It does not set hit points."""
    if re.search(r"\b(?:swing|throw|hurl|smash|whack|beat|club)\b", text, re.IGNORECASE):
        return {
            "ruling": "Swinging that is an improvised attack.",
            "resolve_as": "attack",
            "params": {"damage_dice": "1d4", "damage_type": "bludgeoning", "proficient": False},
            "log": "no action card matched a weapon; improvised bludgeoning",
        }
    return {"ruling": "No.", "resolve_as": "none", "params": {}, "log": "no match"}


def _public_crawler(crawler):
    return {
        "id": crawler["id"],
        "name": crawler["name"],
        "class_name": crawler["class_name"],
        "level": crawler["level"],
        "hp": crawler["hp"],
        "hp_max": crawler["hp_max"],
        "ac": crawler["ac"],
        "cover": crawler["cover"],
        "hidden": crawler["hidden"],
        "conditions": list(crawler["conditions"]),
        "movement_left": crawler["movement_left"],
        "action": crawler["action"],
        "bonus": crawler["bonus"],
        "reaction": crawler["reaction"],
        "object": crawler["object"],
        "attacks": list(crawler["attacks"]),
    }


def _public_enemy(enemy):
    return {
        "id": enemy["id"],
        "name": enemy["name"],
        "picture": enemy["picture"],
        "spoken_name": enemy["spoken_name"],
        "hp": enemy["hp"],
        "hp_max": enemy["hp_max"],
        "ac": enemy["ac"],
        "conditions": list(enemy["conditions"]),
    }


def _validate_seat(card):
    if not isinstance(card, dict):
        raise ValueError("seat card must be an object")
    name = str(card.get("name") or "").strip()
    if not name or len(name) > 40 or re.search(r"[\r\n]", name):
        raise ValueError("name is required, one line, 40 characters or fewer")
    level = int(card.get("level") or 1)
    if level < 1 or level > 20:
        raise ValueError("level must be 1 to 20")
    hp = int(card.get("hp") or 0)
    hp_max = int(card.get("hp_max") or hp)
    ac = int(card.get("ac") or 10)
    if hp < 1 or hp_max < hp or hp_max > 999 or ac < 1 or ac > 30:
        raise ValueError("hit points and AC are out of range")
    attack = card.get("attack") or {}
    to_hit = int(attack.get("to_hit"))
    damage = str(attack.get("damage") or "").replace(" ", "")
    if to_hit < -5 or to_hit > 20 or not _DICE_EXPR.fullmatch(damage):
        raise ValueError("attack needs a to-hit and damage dice")
    dtype = str(attack.get("type") or "piercing").lower()
    if dtype not in {"bludgeoning", "piercing", "slashing"}:
        raise ValueError("damage type must be bludgeoning, piercing, or slashing")
    return {
        "id": "crawler",
        "name": name,
        "class": str(card.get("class_name") or card.get("class") or "").strip()[:40],
        "level": level,
        "hp": {"current": hp, "max": hp_max},
        "ac": ac,
        "speed_ft": 30,
        "abilities": {
            "str_mod": int(card.get("str_mod") or 0),
            "dex_mod": int(card.get("dex_mod") or 0),
        },
        "proficiency_bonus": int(card.get("pb") or 2),
        "skills": card.get("skills") or [],
        "attacks": [{
            "name": str(attack.get("name") or "Attack")[:40],
            "to_hit": to_hit,
            "damage": damage,
            "type": dtype,
        }],
    }
