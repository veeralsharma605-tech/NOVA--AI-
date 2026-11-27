NOVA AI — Windows starter project
================================

WHAT WORKS
- Premium dark-purple responsive chat interface
- FastAPI backend
- Local Ollama integration
- Online OpenAI-compatible provider adapter (optional)
- Auto mode: tries configured online provider, then falls back to Ollama
- Manual Online / Offline / Auto selector
- Chat history saved in this browser
- PWA manifest and offline shell caching

IMPORTANT LIMITATIONS
- Online AI is not configured by default. A compatible provider account and valid credentials may be required. Free quotas vary and are not unlimited.
- Offline AI requires Ollama and a downloaded model.
- The first version does not include accounts, cloud sync, voice, image understanding or public hosting.
- PWA installation requires serving from localhost or HTTPS. This project runs on localhost.
- Local AI speed depends on your CPU/RAM. A 1.5B model is a starting point, not frontier-level intelligence.

STEP 1 — INSTALL PYTHON
Install Python 3.11 or 3.12 for Windows from https://www.python.org/downloads/
During setup, tick "Add Python to PATH".
Open a new Command Prompt and check:
  py --version

STEP 2 — INSTALL OLLAMA
Download from https://ollama.com/download/windows
Install it, then open Command Prompt:
  ollama pull qwen2.5:1.5b
Wait for download to finish.
Test:
  ollama run qwen2.5:1.5b
Type a question, then /bye to exit.
Keep Ollama running when using Offline or Auto mode.

STEP 3 — RUN NOVA
Extract this ZIP to a folder such as Desktop\NOVA_AI.
Double-click run.bat.
The first run installs Python packages and may take a few minutes.
Open Chrome:
  http://127.0.0.1:8000

STEP 4 — ONLINE PROVIDER (OPTIONAL)
Copy .env.example to a new file named .env in the project root.
Fill in ONLINE_BASE_URL, ONLINE_API_KEY and ONLINE_MODEL using the exact
settings supplied by a provider that offers an eligible free tier.
Never paste API keys into frontend files or share them publicly.
Restart run.bat after editing .env.
Use Auto mode to try online first and fall back to local Ollama.

TROUBLESHOOTING
- "py is not recognized": reinstall Python and enable Add Python to PATH.
- Ollama unavailable: open Ollama, then run `ollama list`.
- Model missing: run `ollama pull qwen2.5:1.5b`.
- Port 8000 busy: close the other app using it or change --port in run.bat.
- Online error: verify provider base URL, model name, key and quota.
- Stop server: press Ctrl+C in the Command Prompt window.

PRIVACY
The local Ollama engine runs on your own machine. Online mode sends chat messages
to the configured external provider. Do not send sensitive information to a
provider unless you understand its privacy and data-use terms.
