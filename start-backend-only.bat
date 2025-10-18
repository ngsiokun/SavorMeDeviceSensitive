@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
echo Starting Backend on http://127.0.0.1:8000
echo Press Ctrl+C to stop
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload


