from __future__ import annotations

import json
import os
import re
import time
from typing import Any
from urllib import request, error


PROVIDERS = {
    "deepseek": {
        "env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com/chat/completions",
        "model": "deepseek-v4-pro",
    },
    "kimi": {
        "env": "MOONSHOT_API_KEY",
        "base_url": "https://api.moonshot.ai/v1/chat/completions",
        "model": "kimi-k2.7-code",
    },
}


def call_provider(provider: str, prompt: str, *, timeout: int = 90) -> dict[str, Any]:
    config = PROVIDERS[provider]
    key = os.environ.get(config["env"])
    if not key:
        raise RuntimeError(f"missing environment variable {config['env']}")

    body = {
        "model": config["model"],
        "messages": [
            {"role": "system", "content": "You emit concise JSON action plans for an agent harness evaluator."},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "max_tokens": 700,
    }
    data = json.dumps(body).encode("utf-8")
    req = request.Request(
        config["base_url"],
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    started = time.time()
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{provider} HTTP {exc.code}: {detail[:500]}") from exc
    payload = json.loads(raw)
    message = payload["choices"][0]["message"]
    content = message.get("content") or ""
    try:
        parsed = extract_json(content)
    except json.JSONDecodeError as exc:
        parsed = {"actions": [], "_parse_error": str(exc)}
    return {
        "payload": parsed,
        "raw_response": content,
        "usage": payload.get("usage", {}) | {"elapsed_seconds": round(time.time() - started, 3)},
    }


def extract_json(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if fenced:
        return json.loads(fenced.group(1))
    brace = re.search(r"(\{.*\})", text, re.S)
    if brace:
        return json.loads(brace.group(1))
    return {"actions": [], "final": text[:200]}
