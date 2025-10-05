@echo off
setlocal

echo ========================================
echo SavorMe Clone Setup Script
echo ========================================
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
call venv\Scripts\python.exe test_imports.py
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
echo 1. Copy your .env file with API keys
echo 2. Run: start_app_reliable.bat
echo.
echo Access points:
echo - Frontend: http://localhost:5000
echo - Backend:  http://127.0.0.1:8000
echo - API Docs: http://127.0.0.1:8000/docs
echo.

endlocal
