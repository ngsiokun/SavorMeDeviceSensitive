@echo off
echo Restarting Desktop App...

REM Kill existing desktop app process
for /f "tokens=5" %%p in ('netstat -aon ^| find ":5001" ^| find "LISTENING"') do taskkill /PID %%p /F >nul 2>&1

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start desktop app
call venv\Scripts\activate.bat
start "SavorMe Desktop" cmd /c "cd desktop_app && ..\venv\Scripts\python.exe app.py"

REM Wait for it to start
timeout /t 3 /nobreak >nul

REM Test if it's running
curl http://127.0.0.1:5001/ >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Desktop app failed to start
    pause
    exit /b 1
)

echo [OK] Desktop app restarted successfully on http://localhost:5001
pause



