@echo off
setlocal

REM ⚠️  CRITICAL: This script MUST be run in Command Prompt (cmd.exe), NOT PowerShell!
REM    PowerShell causes compatibility issues with batch scripts and environment setup.
REM    Always use: cmd.exe or Command Prompt

echo ========================================
echo SavorMe Clone Setup Script
echo ========================================
echo.
echo ⚠️  REMINDER: Run this in Command Prompt (cmd.exe), NOT PowerShell!
echo.

echo Step 1: Creating virtual environment...
py -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    goto :eof
)
echo [OK] Virtual environment created

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    goto :eof
)
echo [OK] Virtual environment activated

echo.
echo Step 3: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    goto :eof
)
echo [OK] Dependencies installed

echo.
echo Step 4: Testing imports...
call venv\Scripts\python.exe -c "import fastapi, uvicorn, flask, requests; print('All imports successful')"
if %errorlevel% neq 0 (
    echo ❌ Import test failed
    goto :eof
)
echo [OK] All imports successful

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy .env from C:\Users\HP\SavorMe to this directory, OR
echo    Create .env with your API keys
echo 2. Run: start.bat
echo.
echo Note: start.bat will automatically copy .env from parent directory if found
echo.
echo Access points:
echo - Frontend: http://localhost:5000
echo - Backend:  http://127.0.0.1:8000
echo - API Docs: http://127.0.0.1:8000/docs
echo.

endlocal
