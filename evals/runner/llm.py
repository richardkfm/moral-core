"""
evals/runner/llm.py
-------------------
One place for model calls, used for the model under test and for every judge.

Each call returns a Completion that keeps the finish reason, so a truncated
answer can be reported as truncated instead of being scored as if it were
complete.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Optional

PROVIDERS = ("anthropic", "openai", "ollama")

# Finish reasons that mean "the token budget ran out", per provider.
_LENGTH_REASONS = {"length", "max_tokens"}


@dataclass
class Completion:
    text: str
    finish_reason: Optional[str] = None

    @property
    def truncated(self) -> bool:
        return (self.finish_reason or "") in _LENGTH_REASONS


def _anthropic(system, user, model, max_tokens, temperature, base_url) -> Completion:
    import anthropic

    kwargs = {"api_key": os.environ.get("ANTHROPIC_API_KEY")}
    if base_url:
        kwargs["base_url"] = base_url
    client = anthropic.Anthropic(**kwargs)
    params = dict(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    if temperature is not None:
        params["temperature"] = temperature
    msg = client.messages.create(**params)
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    return Completion(text.strip(), msg.stop_reason)


def _openai(system, user, model, max_tokens, temperature, base_url) -> Completion:
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=base_url or os.environ.get("OPENAI_BASE_URL"),
    )
    params = dict(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
        stream=True,
    )
    if temperature is not None:
        params["temperature"] = temperature
    # Stream the response: slow or self-hosted endpoints often sit behind a
    # gateway that cuts off long non-streaming requests (HTTP 502/504).
    parts: list[str] = []
    finish_reason = None
    for chunk in client.chat.completions.create(**params):
        if not chunk.choices:
            continue
        choice = chunk.choices[0]
        if choice.delta and choice.delta.content:
            parts.append(choice.delta.content)
        if choice.finish_reason:
            finish_reason = choice.finish_reason
    return Completion("".join(parts).strip(), finish_reason)


def _ollama(system, user, model, max_tokens, temperature, base_url) -> Completion:
    import requests

    options = {"num_predict": max_tokens}
    if temperature is not None:
        options["temperature"] = temperature
    resp = requests.post(
        (base_url or "http://localhost:11434").rstrip("/") + "/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "options": options,
        },
    )
    resp.raise_for_status()
    data = resp.json()
    return Completion(data["message"]["content"].strip(), data.get("done_reason"))


_BACKENDS = {"anthropic": _anthropic, "openai": _openai, "ollama": _ollama}
_CLIENT_MODULES = {"anthropic": "anthropic", "openai": "openai", "ollama": "requests"}


def preload(*providers: str) -> None:
    """
    Import the client library of each provider once, in the calling thread.

    The backends import their client lazily. When the first calls come from
    several worker threads at once, the half-finished import can surface in
    some of them as ModuleNotFoundError and those answers are lost. A missing
    library is also reported here, before any test case has run.
    """
    import importlib

    for provider in providers:
        if provider in _CLIENT_MODULES:
            importlib.import_module(_CLIENT_MODULES[provider])


def chat(
    provider: str,
    model: str,
    system: str,
    user: str,
    max_tokens: int = 1024,
    temperature: Optional[float] = None,
    base_url: Optional[str] = None,
    retries: int = 2,
) -> Completion:
    """
    Send one system + user message and return the answer with its finish reason.

    temperature=None leaves the provider default in place. Transient failures
    are retried; an empty answer is returned as-is so the caller can decide
    (a reasoning model that spent its whole budget thinking returns "" with
    finish_reason "length").
    """
    if provider not in _BACKENDS:
        raise ValueError(f"Unknown provider: {provider}")
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return _BACKENDS[provider](system, user, model, max_tokens, temperature, base_url)
        except Exception as exc:  # network and gateway errors differ per SDK
            last = exc
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
    raise last  # type: ignore[misc]
