@echo off
setlocal enabledelayedexpansion

REM === Resolve script directory and move there ===
pushd %~dp0

echo ========================================
echo SavorMe Startup (v2 - robust)
echo ========================================
echo.

REM ---- Sanity: must be repo root ----
if not exist "app\main.py" (
  echo [ERROR] Run this from the project root (where app\main.py exists).
  echo         Expected: C:\Users\HP\SavorMe\SavorMe-backend
  pause & exit /b 1
)

REM ---- Check .env ----
if not exist ".env" (
  echo [ERROR] .env missing. Create it first (Edamam / OpenRouter keys).
  pause & exit /b 1
)

REM ---- Create venv if needed ----
if not exist "venv\Scripts\python.exe" (
  echo [INFO] Creating virtual environment...
  py -3 -m venv venv || (echo [ERROR] venv create failed & pause & exit /b 1)
)

REM ---- Activate venv ----
call venv\Scripts\activate.bat || (echo [ERROR] Failed to activate venv & pause & exit /b 1)
set PYTHONUNBUFFERED=1

REM ---- Pin python/pip to venv explicitly ----
set PYTHON=venv\Scripts\python.exe
set PIP=venv\Scripts\pip.exe

REM ---- Install deps (idempotent) ----
echo [INFO] Installing requirements...
%PIP% install -r requirements.txt || (echo [ERROR] pip install failed & pause & exit /b 1)

REM ---- Kill anything on our ports (optional but helpful) ----
for /f "tokens=5" %%p in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /PID %%p /F >nul 2>&1
for /f "tokens=5" %%p in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do taskkill /PID %%p /F >nul 2>&1

REM ---- Log files ----
if not exist logs mkdir logs

REM ---- Start backend (FastAPI/Uvicorn) ----
echo [INFO] Starting backend on 127.0.0.1:8000 ...
start "SavorMe Backend" cmd /c ^
  "call venv\Scripts\activate.bat && ^
   %PYTHON% -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload ^
   1>logs\backend.out.log 2>logs\backend.err.log"

REM ---- Wait for backend health (retry up to 30s) ----
set /a tries=0
:wait_backend
timeout /t 2 /nobreak >nul
set /a tries+=1
curl -s http://127.0.0.1:8000/api/v1/health >nul 2>&1
if errorlevel 1 (
  if !tries! lss 15 goto wait_backend
  echo [ERROR] Backend did not become healthy.
  echo         See logs\backend.err.log and logs\backend.out.log
  goto end_fail
)
echo [OK] Backend healthy.

REM ---- Export BACKEND_URL for the frontend (keeps URL consistent) ----
set BACKEND_URL=http://127.0.0.1:8000

REM ---- Start frontend (Flask) from demo_app ----
echo [INFO] Starting frontend on http://localhost:5000 ...
start "SavorMe Frontend" cmd /c ^
  "cd /d %~dp0demo_app && ^
   call ..\venv\Scripts\activate.bat && ^
   set BACKEND_URL=%BACKEND_URL% && ^
   %PYTHON% app.py 1>..\logs\frontend.out.log 2>..\logs\frontend.err.log"

REM ---- Wait for frontend root (retry up to 30s) ----
set /a ftries=0
:wait_frontend
timeout /t 2 /nobreak >nul
set /a ftries+=1
curl -s http://127.0.0.1:5000/ >nul 2>&1
if errorlevel 1 (
  if !ftries! lss 15 goto wait_frontend
  echo [ERROR] Frontend did not start.
  echo         See logs\frontend.err.log and logs\frontend.out.log
  goto end_fail
)
echo [OK] Frontend reachable.

REM ---- Open browser ----
start http://localhost:5000
echo.
echo ========================================
echo All set. Backend: %BACKEND_URL%
echo Frontend: http://localhost:5000
echo Logs in .\logs\
echo ========================================
goto end_ok

:end_fail
echo.
echo [HINTS]
echo - If the backend crashes immediately, open logs\backend.err.log
echo - Ensure your frontend code uses BACKEND_URL env (or same URL hardcoded).
echo - If you changed ports/hosts, keep both sides in sync.
pause
exit /b 1

:end_ok
popd
endlocal
