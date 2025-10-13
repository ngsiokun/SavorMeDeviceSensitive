@echo off
setlocal enabledelayedexpansion

REM ========================================
REM SavorMe Microservices Setup Script
REM This script prepares the environment for microservices
REM ========================================

REM === Get the absolute path to the project root ===
set PROJECT_ROOT=%~dp0
cd /d "%PROJECT_ROOT%"

echo ========================================
echo SavorMe Microservices Setup
echo ========================================
echo.

REM === Check if venv exists ===
if not exist "venv\Scripts\python.exe" (
    echo [INFO] Virtual environment not found. Creating...
    py -3 -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created successfully
)

REM === Activate venv ===
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM === Set Python and Pip ===
set PYTHON=%PROJECT_ROOT%venv\Scripts\python.exe
set PIP=%PROJECT_ROOT%venv\Scripts\pip.exe

REM === Check .env file ===
echo [INFO] Checking .env file...
if not exist ".env" (
    echo [INFO] .env not found in project directory.
    echo [INFO] Checking parent directory...
    if exist "..\.env" (
        echo [INFO] Found .env in parent directory. Copying...
        copy "..\.env" ".env" >nul
        if errorlevel 1 (
            echo [ERROR] Failed to copy .env file
            pause
            exit /b 1
        )
        echo [OK] .env copied successfully
    ) else (
        echo [WARNING] .env file not found!
        echo [WARNING] Please create .env with required API keys:
        echo            - EDAMAM_APP_ID
        echo            - EDAMAM_APP_KEY
        echo            - OPENROUTER_API_KEY
        echo.
        echo [WARNING] Continuing setup, but services will fail without API keys...
        timeout /t 5
    )
) else (
    echo [OK] .env file found
)

REM === Upgrade pip ===
echo [INFO] Upgrading pip...
%PIP% install --upgrade pip >nul 2>&1

REM === Install main requirements ===
echo [INFO] Installing main requirements...
%PIP% install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install main requirements
    pause
    exit /b 1
)
echo [OK] Main requirements installed

REM === Install microservice requirements ===
echo.
echo [INFO] Installing microservice requirements...

REM User Nutrition Service
if exist "backend_app\user-nutrition-service\requirements.txt" (
    echo [INFO] Installing User Nutrition Service requirements...
    %PIP% install -r backend_app\user-nutrition-service\requirements.txt
    if errorlevel 1 (
        echo [WARNING] User Nutrition Service requirements installation had issues
    ) else (
        echo [OK] User Nutrition Service requirements installed
    )
)

REM Recipe Service
if exist "backend_app\recipe-service\requirements.txt" (
    echo [INFO] Installing Recipe Service requirements...
    %PIP% install -r backend_app\recipe-service\requirements.txt
    if errorlevel 1 (
        echo [WARNING] Recipe Service requirements installation had issues
    ) else (
        echo [OK] Recipe Service requirements installed
    )
)

REM Mood AI Service
if exist "backend_app\mood-ai-service\requirements.txt" (
    echo [INFO] Installing Mood AI Service requirements...
    %PIP% install -r backend_app\mood-ai-service\requirements.txt
    if errorlevel 1 (
        echo [WARNING] Mood AI Service requirements installation had issues
    ) else (
        echo [OK] Mood AI Service requirements installed
    )
)

REM Router/API Gateway
if exist "router\requirements.txt" (
    echo [INFO] Installing API Gateway requirements...
    %PIP% install -r router\requirements.txt
    if errorlevel 1 (
        echo [WARNING] API Gateway requirements installation had issues
    ) else (
        echo [OK] API Gateway requirements installed
    )
)

REM Frontend App
if exist "frontend_app\requirements.txt" (
    echo [INFO] Installing Frontend App requirements...
    %PIP% install -r frontend_app\requirements.txt
    if errorlevel 1 (
        echo [WARNING] Frontend App requirements installation had issues
    ) else (
        echo [OK] Frontend App requirements installed
    )
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now run the microservices with:
echo    start-microservices.bat
echo.
echo Or run the monolithic app with:
echo    start.bat
echo.
pause

