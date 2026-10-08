"""Narration client. Tests use fake mode. A live call needs ENGINE_MODEL_BASE_URL."""

from __future__ import annotations

import json
import os
import urllib.request


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
    def __init__(self, fake=None):
        if fake is None:
            fake = os.environ.get("ENGINE_FAKE_MODEL", "1") != "0"
        self.fake = fake

    def stream(self, snapshot):
        if self.fake:
            yield from fake_sentences(snapshot)
            return
        yield from self._openai_stream(snapshot)

    def _openai_stream(self, snapshot):
        base = os.environ.get("ENGINE_MODEL_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        key = os.environ.get("ENGINE_MODEL_API_KEY") or os.environ.get("OPENAI_API_KEY")
        model = os.environ.get("ENGINE_FAST_MODEL", "gpt-4o-mini")
        body = {
            "model": model,
            "stream": True,
            "messages": [
                {"role": "system", "content": "Narrate in two to four sentences. Do not change any number."},
                {"role": "user", "content": json.dumps(snapshot, ensure_ascii=False)},
            ],
        }
        req = urllib.request.Request(
            base + "/chat/completions",
            data=json.dumps(body).encode(),
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
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
