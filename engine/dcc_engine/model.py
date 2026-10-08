"""Narration client. Tests use fake mode. A live call needs ENGINE_MODEL_BASE_URL."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

# A hung call must not stall the table for half a minute.
MODEL_TIMEOUT_SECONDS = 8


def strong_model_name():
    return os.environ.get("ENGINE_STRONG_MODEL") or "gpt-4o"


def _take_sentences(buf, final):
    """Pull finished sentences out of a stream buffer. Leave a partial tail."""
    ready = []
    start = 0
    i = 0
    while i < len(buf):
        ch = buf[i]
        if ch in ".!?":
            prev = buf[i - 1] if i else ""
            nxt = buf[i + 1] if i + 1 < len(buf) else ""
            boundary = (nxt == "" and final) or nxt.isspace()
            if prev not in ".!?" and boundary:
                sentence = buf[start:i + 1].strip()
                if sentence:
                    ready.append(sentence)
                start = i + 1
        i += 1
    return ready, buf[start:]


def iter_sentences(chunks):
    """Yield whole sentences as chunks arrive. The bridge speaks one sentence at a time."""
    buf = ""
    for chunk in chunks:
        if not chunk:
            continue
        buf += chunk
        ready, buf = _take_sentences(buf, final=False)
        for sentence in ready:
            yield sentence
    ready, buf = _take_sentences(buf, final=True)
    for sentence in ready:
        yield sentence
    if buf.strip():
        yield buf.strip()


def fake_sentences(snapshot):
    """Echo the resolved result. The model does not roll or change hit points."""
    result = snapshot.get("result") or {}
    if result.get("ok") is False:
        yield result.get("reason") or "The System says no."
        return
    if "hit" in result:
        yield "%s rolls %s, total %s against AC %s. Hit: %s. Damage %s. %s has %s hit points." % (
            result.get("attacker"), result.get("d20"), result.get("total"), result.get("ac"),
            "yes" if result.get("hit") else "no", result.get("damage"),
            result.get("target"), result.get("target_hp"),
        )
        return
    text = snapshot.get("line") or snapshot.get("narrator_line") or "The room waits."
    yield text


class ModelClient:
    def __init__(self, fake=None, fake_ruling=None, fake_class=None):
        if fake is None:
            fake = os.environ.get("ENGINE_FAKE_MODEL", "1") != "0"
        self.fake = fake
        self.fake_ruling = fake_ruling
        self.fake_class = fake_class

    def classify(self, text):
        """Fast model. Returns chatter, engine, or ruling. None means use the word fallback."""
        if self.fake:
            return self.fake_class
        try:
            return self._fast_class(text)
        except Exception:
            return None

    def stream(self, snapshot):
        if self.fake:
            yield from fake_sentences(snapshot)
            return
        try:
            yield from iter_sentences(self._raw_chunks(snapshot))
        except (urllib.error.URLError, TimeoutError, OSError):
            yield from fake_sentences(snapshot)

    def rule(self, snapshot):
        """Strong model. Fake mode returns a ruling JSON and does not call a network."""
        if self.fake:
            if self.fake_ruling:
                return self.fake_ruling
            return {
                "ruling": "Nothing on the card covers that.",
                "resolve_as": "none",
                "params": {},
                "log": "fake strong model",
            }
        try:
            return self._strong_rule(snapshot)
        except (urllib.error.URLError, TimeoutError, OSError):
            return {
                "ruling": "Nothing on the card covers that.",
                "resolve_as": "none",
                "params": {},
                "log": "model unavailable",
            }

    def _api_key(self):
        key = os.environ.get("ENGINE_MODEL_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("ENGINE_MODEL_API_KEY or OPENAI_API_KEY is required for a live model call")
        return key

    def _post(self, body):
        base = os.environ.get("ENGINE_MODEL_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        req = urllib.request.Request(
            base + "/chat/completions",
            data=json.dumps(body).encode(),
            headers={"Authorization": "Bearer " + self._api_key(), "Content-Type": "application/json"},
        )
        return urllib.request.urlopen(req, timeout=MODEL_TIMEOUT_SECONDS)

    def _raw_chunks(self, snapshot):
        model = os.environ.get("ENGINE_FAST_MODEL", "gpt-4o-mini")
        body = {
            "model": model,
            "stream": True,
            "messages": [
                {"role": "system", "content": "Narrate in two to four sentences. Do not change any number."},
                {"role": "user", "content": json.dumps(snapshot, ensure_ascii=False)},
            ],
        }
        resp = self._post(body)
        with resp:
            for raw in resp:
                line = raw.decode().strip()
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                chunk = json.loads(data)
                delta = (((chunk.get("choices") or [{}])[0].get("delta") or {}).get("content"))
                if delta:
                    yield delta

    def _fast_class(self, text):
        try:
            self._api_key()
        except RuntimeError:
            return None
        body = {
            "model": os.environ.get("ENGINE_FAST_MODEL", "gpt-4o-mini"),
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Classify the player line. Return one JSON object only: "
                        "{\"class\": \"chatter\"|\"engine\"|\"ruling\"}. "
                        "engine is an attack or Cunning Action. "
                        "ruling is any other attempted action. "
                        "chatter is talk, scene questions, and negated actions."
                    ),
                },
                {"role": "user", "content": text or ""},
            ],
        }
        resp = self._post(body)
        with resp:
            payload = json.loads(resp.read().decode())
        content = (((payload.get("choices") or [{}])[0].get("message") or {}).get("content")) or ""
        content = content.strip()
        if content.startswith("```"):
            content = content.strip("`")
            content = content.split("\n", 1)[-1]
        try:
            label = (json.loads(content) or {}).get("class")
        except json.JSONDecodeError:
            return None
        if label in ("chatter", "engine", "ruling"):
            return label
        return None

    def _strong_rule(self, snapshot):
        body = {
            "model": strong_model_name(),
            "stream": False,
            "messages": [
                {"role": "system", "content": "Return one JSON object only: {\"ruling\": \"one sentence\", \"resolve_as\": \"attack|save|check|damage|heal|condition|move|item|none\", \"params\": {}, \"log\": \"why\"}. Do not set hit points or credits."},
                {"role": "user", "content": json.dumps(snapshot, ensure_ascii=False)},
            ],
        }
        resp = self._post(body)
        with resp:
            payload = json.loads(resp.read().decode())
        content = (((payload.get("choices") or [{}])[0].get("message") or {}).get("content")) or ""
        return json.loads(content)
