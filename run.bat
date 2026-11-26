@echo off
cd /d "%~dp0"
if not exist ".venv" (
  echo Creating Python virtual environment...
  py -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
echo.
echo Starting NOVA AI...
echo Open http://127.0.0.1:8000 in Chrome.
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
pause
