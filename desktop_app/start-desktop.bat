@echo off
echo.
echo ========================================
echo    SavorMe Desktop Version Startup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

REM Check if backend is running
echo Checking backend connection...
curl -s http://127.0.0.1:8000/health >nul 2>&1
if errorlevel 1 (
    echo WARNING: Backend not detected at http://127.0.0.1:8000
    echo Please ensure the backend is running before using the desktop version
    echo.
)

REM Start desktop application
echo.
echo Starting SavorMe Desktop Version...
echo.
echo Desktop URL: http://localhost:5001
echo Mobile URL:  http://localhost:5000
echo Backend URL: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause




