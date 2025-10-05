@echo off
setlocal

echo ========================================
echo SavorMe Auto-Startup with Setup
echo ========================================
echo.

echo 🚀 Starting SavorMe with automatic setup...
echo.

REM Try to run the Python startup script
py start_with_setup.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Python startup failed. Trying alternative method...
    echo.
    
    REM Check if virtual environment exists
    if exist "venv\Scripts\python.exe" (
        echo 🔧 Using virtual environment Python...
        venv\Scripts\python.exe start_with_setup.py
    ) else (
        echo ❌ Virtual environment not found.
        echo 💡 Please run setup_new_clone.bat first
        echo.
        pause
        goto :eof
    )
)

echo.
echo ========================================
echo SavorMe startup completed
echo ========================================
echo.
pause

endlocal
