"""Split a spoken line into clauses and match each one to an action card."""

import re

# Longer joins first so "and then" is not also split on "and".
_SPLIT = re.compile(
    r"\s*,?\s*and then\s+|\s*,?\s*then\s+|\s*;\s*|\s*,\s*and\s+|\s+\band\b\s+|\s*,\s*",
    re.IGNORECASE,
)

_IMPROVISED = re.compile(
    r"\b(?:swing|throw|hurl|smash|whack|beat|club)\b.{0,40}\b(?:body|corpse|dummy)\b"
    r"|\b(?:body|corpse|dummy)\b.{0,40}\b(?:swing|throw|hurl|smash|whack|beat|club)\b",
    re.IGNORECASE,
)
_SWING_IT = re.compile(
    r"\b(?:swing|throw|hurl|smash|whack|beat)\s+it\b",
    re.IGNORECASE,
)
_ATTACK = re.compile(
    r"\b(?:attack|swing|shoot|hit|stab|punch|fire|loose)\b",
    re.IGNORECASE,
)
_HIDE = re.compile(r"\b(?:hide|sneak)\b", re.IGNORECASE)
_DASH = re.compile(r"\b(?:dash)\b", re.IGNORECASE)
_RUN = re.compile(r"\brun\b", re.IGNORECASE)
_DISENGAGE = re.compile(r"\b(?:disengage|back off)\b", re.IGNORECASE)
_DODGE = re.compile(r"\bdodge\b", re.IGNORECASE)
_CLOSE = re.compile(
    r"\b(?:climb|hop the counter|rush|close in|close to melee|jump the counter)\b",
    re.IGNORECASE,
)
_COVER = re.compile(
    r"\b(?:sandbag|sandbags|take cover|get behind|behind the)\b",
    re.IGNORECASE,
)
_MOVE = re.compile(r"\b(?:move|go|walk)\b", re.IGNORECASE)
_OBJECT = re.compile(
    r"\b(?:pick up|pickup|grab|draw|stow|sheathe|pocket)\b",
    re.IGNORECASE,
)
_BODY = re.compile(r"\b(?:body|corpse)\b", re.IGNORECASE)
_FLAVOR = re.compile(
    r"\b(?:yell|shout|scream|laugh|smile|wave|taunt|look around)\b",
    re.IGNORECASE,
)
_BONUS = re.compile(r"\bcunning\b|\bbonus(?:\s+action)?\b", re.IGNORECASE)
_END = re.compile(
    r"\b(?:end turn|i'm done|im done|that's all|thats all)\b",
    re.IGNORECASE,
)
_QUESTION = re.compile(
    r"^(?:can i|could i|what|who|where|how|why|ai)\b",
    re.IGNORECASE,
)


def split_clauses(text):
    parts = _SPLIT.split(text or "")
    cleaned = []
    for part in parts:
        piece = part.strip(" .\t")
        if piece:
            cleaned.append(piece)
    return cleaned


def is_question(text):
    stripped = (text or "").strip()
    return stripped.endswith("?") or bool(_QUESTION.match(stripped))


def classify(clause, held=None):
    """Return a clause card. Improvised weapon use is a ruling, not a listed attack."""
    text = clause.strip()
    low = text.lower()
    bonus = bool(_BONUS.search(low))
    base = {"text": text, "bonus": bonus, "cover": False, "into_melee": False}
    if is_question(text):
        return {**base, "kind": "question"}
    if low in {"done", "pass", "i pass"} or (_END.search(low) and not _ATTACK.search(low)):
        return {**base, "kind": "end"}
    improvised = bool(_IMPROVISED.search(low)) or (
        held in {"body", "corpse"} and bool(_SWING_IT.search(low))
    )
    if improvised:
        return {**base, "kind": "ruling"}
    if _ATTACK.search(low):
        return {**base, "kind": "attack", "cover": bool(_COVER.search(low))}
    if _HIDE.search(low):
        return {**base, "kind": "hide"}
    if _DASH.search(low) or (_RUN.search(low) and not _COVER.search(low)):
        return {**base, "kind": "dash"}
    if _DISENGAGE.search(low):
        return {**base, "kind": "disengage"}
    if _DODGE.search(low):
        return {**base, "kind": "dodge"}
    if _CLOSE.search(low):
        return {**base, "kind": "move", "into_melee": True}
    if _COVER.search(low) or _MOVE.search(low):
        return {**base, "kind": "move", "cover": bool(_COVER.search(low))}
    if _OBJECT.search(low):
        kind = "object"
        if _BODY.search(low):
            return {**base, "kind": kind, "held": "body"}
        return {**base, "kind": kind, "held": "item"}
    if _FLAVOR.search(low):
        return {**base, "kind": "flavor"}
    return {**base, "kind": "ruling"}
