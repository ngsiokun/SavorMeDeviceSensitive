@echo off
echo ========================================
echo Starting SavorMe Desktop + Backend
echo ========================================
echo.

cd /d "%~dp0"

echo Starting Backend on port 8000...
start "SavorMe Backend (Port 8000)" cmd /k "venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo Starting Desktop App on port 5001...
start "SavorMe Desktop (Port 5001)" cmd /k "cd desktop_app && ..\venv\Scripts\python.exe app.py"

echo.
echo ========================================
echo Both services started!
echo ========================================
echo Backend: http://127.0.0.1:8000
echo Desktop: http://127.0.0.1:5001
echo.
echo Two new windows should have opened.
echo Keep them open to see logs and errors.
echo ========================================
pause

