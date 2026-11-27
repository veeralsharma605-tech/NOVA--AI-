import json
import os
import urllib.request
import urllib.error

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
ONLINE_BASE_URL = os.getenv("ONLINE_BASE_URL", "").rstrip("/")
ONLINE_API_KEY = os.getenv("ONLINE_API_KEY", "")
ONLINE_MODEL = os.getenv("ONLINE_MODEL", "")

def _post_json(url, payload, headers=None, timeout=120):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        **(headers or {})
    }, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))

def ask_ollama(messages):
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    }
    result = _post_json(f"{OLLAMA_URL}/api/chat", payload, timeout=180)
    return result.get("message", {}).get("content", "").strip()

def ask_online(messages):
    if not ONLINE_BASE_URL or not ONLINE_MODEL:
        raise RuntimeError("Online provider is not configured.")
    headers = {}
    if ONLINE_API_KEY:
        headers["Authorization"] = f"Bearer {ONLINE_API_KEY}"
    payload = {
        "model": ONLINE_MODEL,
        "messages": messages,
        "stream": False
    }
    result = _post_json(
        f"{ONLINE_BASE_URL}/chat/completions",
        payload,
        headers=headers,
        timeout=90
    )
    return result["choices"][0]["message"]["content"].strip()

def generate_reply(messages, mode="auto"):
    if mode == "offline":
        return ask_ollama(messages), "offline"
    if mode == "online":
        return ask_online(messages), "online"

    # Auto mode: try configured online provider first, then local Ollama.
    if ONLINE_BASE_URL and ONLINE_MODEL:
        try:
            return ask_online(messages), "online"
        except Exception:
            pass
    return ask_ollama(messages), "offline"
