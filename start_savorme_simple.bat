@echo off
echo ========================================
echo SavorMe Simple Startup
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "app\main.py" (
    echo ERROR: Not in SavorMe directory. Please run from C:\Users\HP\SavorMe\SavorMe-backend
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Start backend
echo Starting backend server...
start "SavorMe Backend" /min cmd /c "venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo Starting frontend server...
start "SavorMe Frontend" /min cmd /c "cd demo_app && ..\venv\Scripts\activate.bat && python app.py"

REM Wait a moment for frontend to start
timeout /t 3 /nobreak >nul

REM Open browser
echo Opening browser...
start http://localhost:5000

echo.
echo ========================================
echo SavorMe is starting up!
echo ========================================
echo.
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5000
echo.
echo The application should open in your browser shortly.
echo If not, manually navigate to: http://localhost:5000
echo.
echo Press any key to close this window...
pause >nul
