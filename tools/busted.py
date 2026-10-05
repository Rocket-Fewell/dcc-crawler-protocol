"""Busted-guess grading (rules/50 section 6.2), pure functions: no file or sealed-roll access here.

grade(kind, text, traits) -> True/False. `traits` is a list of sealed table entries for the guessed kind (the caller resolves them
from the sealed roll in memory). A call is Busted when the kind is equal AND the wording matches the sealed trait's keywords:
lenient on wording (stemming, stop words, word order, synonyms listed in the keyword list), strict on meaning (a lone filler word
never matches; entries without an explicit keyword list get one derived in memory from their own name and description).
Nothing here prints, logs or returns which keyword matched."""
import re

KINDS = {"fixation": "fixation", "fix": "fixation", "fx": "fixation", "quirk": "quirk", "tic": "tic", "verbal-tic": "tic", "vt": "tic",
         "tell": "tell", "prior-installation": "prior_installation", "prior": "prior_installation", "installation": "prior_installation",
         "pi": "prior_installation"}
MAX_WORDS = 30
STOP = set("""a an the of on in at to for from with without by and or but nor so is are was were be been being it its it's this that these those
he she they them his her their there here as if then than too very can could would should will just not no yes do does did done has have had
about into over under up down out off again more most some any each other such only own same also unit gm system thing things like really
always never when while who whom what which why how all both few many much one two three i you we us our your""".split())
GENERIC_NAME = set("""obsession fixation fixated love loves hate hates need needs habit tic quirk verbal tell prior installation memory leak
leaks reaction reacts talks talk says say speaks strange odd weird thing behavior behaviour""".split())


def stem(w):
    w = w.lower().replace("\u2019", "'")
    w = re.sub(r"'s$", "", w)
    w = re.sub(r"[^a-z0-9]", "", w)
    if len(w) > 4 and w.endswith("ies"):
        w = w[:-3] + "y"
    elif len(w) > 5 and w.endswith("ing"):
        w = w[:-3]
    elif len(w) > 4 and w.endswith("ed"):
        w = w[:-2]
    elif len(w) > 4 and w.endswith("es") and w[-3] in "sxz":
        w = w[:-2]
    elif len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        w = w[:-1]
    if len(w) > 3 and w[-1] == w[-2] and w[-1] not in "lszf" and w[-1] not in "aeiou":
        w = w[:-1]
    return w


def tokens(text):
    out = []
    for raw in re.findall(r"[A-Za-z0-9'\u2019]+", str(text or "")):
        if raw.lower() in STOP:
            continue
        s = stem(raw)
        if s and s not in STOP and (len(s) > 1 or s.isdigit()):
            out.append(s)
    return out


def same_word(a, b):
    if a == b:
        return True
    s, l = (a, b) if len(a) <= len(b) else (b, a)
    return len(s) >= 4 and l.startswith(s) and len(l) - len(s) <= 3


def has(bag, word):
    return any(same_word(word, t) for t in bag)


def call_key(kind, text):
    """Normalised identity of a call, used to bar repeats: the kind plus the sorted distinct word stems (wording and order do not matter)."""
    return str(KINDS.get(str(kind).strip().lower(), kind)) + ": " + " ".join(sorted(set(tokens(text))))


def check_text(text):
    toks = tokens(text)
    if not toks:
        return "the call needs some words"
    if len(re.findall(r"\S+", str(text))) > MAX_WORDS:
        return f"keep the call short (at most {MAX_WORDS} words)"
    return None


def _strong_weak(entry, explicit_keys):
    """-> (strong phrases [token lists], weak tokens). Built in memory only."""
    strong = []
    for k in explicit_keys:
        t = tokens(k)
        if t:
            strong.append(t)
    for w in tokens(entry.get("name", "")):
        if w not in GENERIC_NAME and len(w) >= 3:
            strong.append([w])
    weak = set(tokens(entry.get("description", "")))
    for t in (entry.get("affinity") or {}).get("trigger_themes", []) or []:
        weak |= set(tokens(t))
    weak -= {w for p in strong for w in p}
    weak = {w for w in weak if w not in GENERIC_NAME and len(w) >= 4}
    return strong, weak


def grade(kind, text, traits):
    kind = KINDS.get(str(kind).strip().lower())
    bag = tokens(text)
    if not kind or not bag or not traits:
        return False
    if kind == "tell":
        weak = set()
        for e in traits:
            for v in (e.get("tells_by_level") or {}).values():
                weak |= {w for w in tokens(v) if w not in GENERIC_NAME and len(w) >= 4}
        return sum(1 for w in weak if has(bag, w)) >= 3
    for e in traits:
        explicit = (e.get("affinity") or {}).get("trigger_keywords", []) or []
        strong, weak = _strong_weak(e, explicit)
        for phrase in strong:
            if all(has(bag, w) for w in phrase):
                return True
        if sum(1 for w in weak if has(bag, w)) >= 2:
            return True
    return False
