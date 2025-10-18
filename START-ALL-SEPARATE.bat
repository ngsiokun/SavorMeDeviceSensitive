@echo off
REM ========================================
REM SavorMe - Start All Services Separately
REM v4.0.0 - Automatic Device Detection
REM ========================================
REM 
REM ⚠️ CRITICAL: Use Command Prompt (cmd.exe), NOT PowerShell!
REM
REM This script starts THREE SEPARATE services:
REM   1. Backend (port 8000) - API service
REM   2. Desktop Frontend (port 5001) - Desktop version
REM   3. Mobile Frontend (port 5000) - Mobile version
REM   4. Router (port 8080) - Auto-detects device
REM
REM Why separate? Easier debugging!
REM - Backend issue? Check backend terminal
REM - Desktop issue? Check desktop terminal
REM - Mobile issue? Check mobile terminal
REM

echo.
echo ========================================
echo   SavorMe v4.0.0 - Separate Services
echo   Automatic Device Detection
echo ========================================
echo.
echo ╔═══════════════════════════════════════╗
echo ║  FRONTEND + BACKEND SEPARATION        ║
echo ║  Each service runs in its own window  ║
echo ║  For easier debugging!                ║
echo ╚═══════════════════════════════════════╝
echo.
echo Starting services in separate windows...
echo.

cd /d "%~dp0"

REM Kill any existing processes on our ports
echo Cleaning up existing processes...
for /f "tokens=5" %%p in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /PID %%p /F >nul 2>&1
for /f "tokens=5" %%p in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do taskkill /PID %%p /F >nul 2>&1
for /f "tokens=5" %%p in ('netstat -aon ^| find ":5001" ^| find "LISTENING"') do taskkill /PID %%p /F >nul 2>&1
for /f "tokens=5" %%p in ('netstat -aon ^| find ":8080" ^| find "LISTENING"') do taskkill /PID %%p /F >nul 2>&1

echo.
echo [1/4] Starting Backend (port 8000)...
start "SavorMe Backend [8000]" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo [2/4] Starting Mobile Frontend (port 5000)...
start "SavorMe Mobile [5000]" cmd /k "cd /d %~dp0demo_app && ..\venv\Scripts\activate.bat && python app.py"

timeout /t 2 /nobreak >nul

echo [3/4] Starting Desktop Frontend (port 5001)...
start "SavorMe Desktop [5001]" cmd /k "cd /d %~dp0desktop_app && ..\venv\Scripts\activate.bat && python app.py"

timeout /t 2 /nobreak >nul

echo [4/4] Starting Device Router (port 8080)...
start "SavorMe Router [8080]" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && python app_router.py"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   All Services Started!
echo ========================================
echo.
echo Service Status:
echo  ✓ Backend:  http://127.0.0.1:8000
echo  ✓ Mobile:   http://localhost:5000
echo  ✓ Desktop:  http://localhost:5001
echo  ✓ Router:   http://localhost:8080
echo.
echo ========================================
echo   Access Points:
echo ========================================
echo.
echo  AUTO-DETECT (Recommended):
echo    http://localhost:8080
echo    → Routes to desktop or mobile automatically
echo.
echo  DIRECT ACCESS:
echo    Desktop: http://localhost:5001
echo    Mobile:  http://localhost:5000
echo.
echo  BACKEND API:
echo    http://127.0.0.1:8000
echo    Docs: http://127.0.0.1:8000/docs
echo.
echo ========================================
echo   Debugging Made Easy:
echo ========================================
echo.
echo  4 separate windows opened:
echo    [8000] Backend - API issues
echo    [5000] Mobile - Mobile frontend issues  
echo    [5001] Desktop - Desktop frontend issues
echo    [8080] Router - Device detection issues
echo.
echo  Check the appropriate window for errors!
echo.
echo ========================================
echo.

REM Wait a bit more then open browser to router
timeout /t 3 /nobreak >nul
start http://localhost:8080

echo.
echo Browser opened to router (port 8080)
echo The router will automatically detect your device
echo and show you the right version!
echo.
echo Press any key to close this window...
echo (All services will keep running in their windows)
pause >nul

