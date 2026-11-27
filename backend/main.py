from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import urllib.request
import urllib.error
import os

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

from ai_engine import generate_reply, OLLAMA_URL, OLLAMA_MODEL, ONLINE_BASE_URL, ONLINE_MODEL

app = FastAPI(title="NOVA AI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class ChatRequest(BaseModel):
    messages: list[dict] = Field(min_length=1, max_length=30)
    mode: str = "auto"

@app.get("/api/health")
def health():
    ollama_ok = False
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=3) as r:
            ollama_ok = r.status == 200
    except Exception:
        pass
    return {
        "status": "ok",
        "ollama_available": ollama_ok,
        "ollama_model": OLLAMA_MODEL,
        "online_configured": bool(ONLINE_BASE_URL and ONLINE_MODEL),
    }

@app.post("/api/chat")
def chat(request: ChatRequest):
    if request.mode not in ("auto", "online", "offline"):
        raise HTTPException(status_code=400, detail="Invalid AI mode.")
    clean_messages = []
    for item in request.messages:
        role = item.get("role")
        content = item.get("content")
        if role not in ("system", "user", "assistant") or not isinstance(content, str):
            raise HTTPException(status_code=400, detail="Invalid message format.")
        clean_messages.append({"role": role, "content": content[:12000]})
    try:
        answer, engine = generate_reply(clean_messages, request.mode)
        if not answer:
            raise RuntimeError("The AI provider returned an empty response.")
        return {"reply": answer, "engine": engine}
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"AI engine unavailable: {str(exc)[:300]}"
        )

app.mount("/", StaticFiles(directory=ROOT / "frontend", html=True), name="frontend")
