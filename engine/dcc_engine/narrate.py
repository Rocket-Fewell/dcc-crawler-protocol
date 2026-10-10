"""Fake fast narrator. It may only speak numbers already on the result."""


def pack(events):
    """Collapse a chain into one System line, unspoken rolls, and one GM line."""
    system, rolls, gm = [], [], []
    for event in events:
        channel = event["channel"]
        if channel == "system":
            system.append(event["text"])
        elif channel == "roll":
            rolls.append(event["text"])
        elif channel == "gm":
            gm.append(event["text"])
    packed = []
    if system:
        packed.append({"voice": "SYSTEM", "speak": True, "text": "[SYSTEM] " + " ".join(system)})
    for line in rolls:
        packed.append({"voice": "ROLL", "speak": False, "text": line})
    if gm:
        packed.append({"voice": "GM", "speak": True, "text": "[GM] " + " ".join(gm)})
    return packed


def attack_gm(actor, attack_name, target_name, hit, damage, dtype, hp_left, killed, crit):
    painted = "mannequin" in target_name.lower() or "smiling polo" in target_name.lower()
    if not hit:
        if painted:
            return f"Your {attack_name} misses {target_name}. It is still smiling."
        return f"Your {attack_name} misses {target_name}. It looks offended, which is not the same as hurt."
    blow = f"Your {attack_name} hits {target_name}."
    if crit:
        blow += " Critical."
    blow += f" {damage} {dtype} damage."
    if killed:
        if painted:
            return blow + " It drops the bow and keeps smiling on the floor."
        return blow + " Down. The audience will want a replay anyway."
    return blow + f" It has {hp_left} hit points left."


def enemy_gm(name, attack_name, hit, damage, dtype, hp_left, dropped):
    if not hit:
        return f"{name} misses with {attack_name}."
    line = f"{name} hits with {attack_name}. {damage} {dtype} damage."
    if dropped:
        return line + " You drop to 0 hit points."
    return line + f" You have {hp_left} hit points left."
