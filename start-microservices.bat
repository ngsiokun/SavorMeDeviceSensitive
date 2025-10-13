@echo off
setlocal enabledelayedexpansion

REM === Get the absolute path to the project root ===
set PROJECT_ROOT=%~dp0
cd /d "%PROJECT_ROOT%"

echo ========================================
echo Starting SavorMe Microservices Architecture
echo ========================================
echo.

REM === Check if venv exists ===
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo [ERROR] Please run start.bat first to set up the environment.
    pause
    exit /b 1
)

REM === Set Python and Pip to venv explicitly ===
set PYTHON=%PROJECT_ROOT%venv\Scripts\python.exe
set PIP=%PROJECT_ROOT%venv\Scripts\pip.exe

REM === Check .env file ===
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo [ERROR] Please copy .env file to project root.
    pause
    exit /b 1
)

REM === Kill any existing processes on our ports ===
echo [INFO] Cleaning up existing processes...
for /f "tokens=5" %%p in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /PID %%p /F >nul 2>&1
for /f "tokens=5" %%p in ('netstat -aon ^| find ":8001" ^| find "LISTENING"') do taskkill /PID %%p /F >nul 2>&1
for /f "tokens=5" %%p in ('netstat -aon ^| find ":8002" ^| find "LISTENING"') do taskkill /PID %%p /F >nul 2>&1
for /f "tokens=5" %%p in ('netstat -aon ^| find ":8003" ^| find "LISTENING"') do taskkill /PID %%p /F >nul 2>&1
for /f "tokens=5" %%p in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do taskkill /PID %%p /F >nul 2>&1

echo.
echo [1/5] Starting User Nutrition Service (Port 8001)...
start "User-Nutrition-Service" cmd /k "cd /d %PROJECT_ROOT%backend_app\user-nutrition-service ^&^& call %PROJECT_ROOT%venv\Scripts\activate.bat ^&^& %PYTHON% main.py"

timeout /t 2 /nobreak >nul

echo [2/5] Starting Recipe Service (Port 8002)...
start "Recipe-Service" cmd /k "cd /d %PROJECT_ROOT%backend_app\recipe-service ^&^& call %PROJECT_ROOT%venv\Scripts\activate.bat ^&^& %PYTHON% main.py"

timeout /t 2 /nobreak >nul

echo [3/5] Starting Mood AI Service (Port 8003)...
start "Mood-AI-Service" cmd /k "cd /d %PROJECT_ROOT%backend_app\mood-ai-service ^&^& call %PROJECT_ROOT%venv\Scripts\activate.bat ^&^& %PYTHON% main.py"

timeout /t 2 /nobreak >nul

echo [4/5] Starting API Gateway (Port 8000)...
start "API-Gateway" cmd /k "cd /d %PROJECT_ROOT%router ^&^& call %PROJECT_ROOT%venv\Scripts\activate.bat ^&^& %PYTHON% main.py"

timeout /t 2 /nobreak >nul

echo [5/5] Starting Frontend App (Port 5000)...
start "Frontend-App" cmd /k "cd /d %PROJECT_ROOT%frontend_app ^&^& call %PROJECT_ROOT%venv\Scripts\activate.bat ^&^& %PYTHON% app.py"

echo.
echo ========================================
echo All services are starting...
echo ========================================
echo.
echo Waiting for services to initialize (10 seconds)...
timeout /t 10 /nobreak >nul
echo.
echo ========================================
echo Access Points:
echo ========================================
echo - Frontend:         http://localhost:5000
echo - API Gateway:      http://localhost:8000
echo - API Docs:         http://localhost:8000/docs
echo - Gateway Health:   http://localhost:8000/health
echo.
echo ========================================
echo Individual Service Health Checks:
echo ========================================
echo - User Nutrition:   http://localhost:8001/health
echo - Recipe Service:   http://localhost:8002/health
echo - Mood AI Service:  http://localhost:8003/health
echo.
echo ========================================
echo TIP: Check the individual service windows for errors
echo TIP: Press Ctrl+C in any window to stop that service
echo ========================================
echo.
echo Opening frontend in browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:5000
echo.
pause
