@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
cd desktop_app
echo Starting Desktop App on http://localhost:5001
echo Press Ctrl+C to stop
python app.py


