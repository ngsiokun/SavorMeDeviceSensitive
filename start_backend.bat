@echo off
echo ========================================
echo Starting SavorMe Backend
echo ========================================

cd /d "%~dp0"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Clear Python cache
echo Clearing Python cache...
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul

echo.
echo Starting FastAPI backend on http://localhost:8000
echo.

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause

