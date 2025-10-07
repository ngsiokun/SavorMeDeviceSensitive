@echo off
echo ========================================
echo SavorMe Professional Startup
echo Automated Setup & Launch System
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "app\main.py" (
    echo ERROR: Not in SavorMe directory. Please run from C:\Users\HP\SavorMe\SavorMe-backend
    pause
    exit /b 1
)

REM Documentation Integration Check
echo Checking documentation integration...
if not exist "MASTER_FILE_ORGANIZATION.md" (
    echo WARNING: MASTER_FILE_ORGANIZATION.md not found
    echo Please ensure all documentation files are present
)
if not exist "CUSTOMIZATIONS_PERSISTENT.md" (
    echo WARNING: CUSTOMIZATIONS_PERSISTENT.md not found
    echo Please ensure design system documentation is present
)
if not exist "SAVORME_MASTER_OVERVIEW.md" (
    echo WARNING: SAVORME_MASTER_OVERVIEW.md not found
    echo Please ensure project overview documentation is present
)
echo Documentation check complete.
echo.

REM Critical .env File Check
echo Checking .env file for API keys...
if not exist ".env" (
    echo ERROR: .env file not found!
    echo.
    echo This is normal when cloning from GitHub.
    echo The .env file contains your API keys and is not included in the repository.
    echo.
    echo Please follow these steps:
    echo 1. See AUTOMATED_APP_STARTUP_GUIDE.md Phase 2 for detailed instructions
    echo 2. Create .env file with your API keys
    echo 3. Get Edamam API keys from: https://developer.edamam.com/
    echo 4. Get OpenRouter API key from: https://openrouter.ai/
    echo.
    echo Press any key to exit and set up your .env file...
    pause >nul
    exit /b 1
) else (
    echo .env file found, checking configuration...
    findstr "EDAMAM_APP_ID=" .env | findstr /v "your_edamam_app_id_here" >nul
    if %errorlevel% neq 0 (
        echo ERROR: EDAMAM_APP_ID not properly configured in .env file
        echo Please edit .env file and add your actual Edamam App ID
        pause
        exit /b 1
    )
    findstr "EDAMAM_APP_KEY=" .env | findstr /v "your_edamam_app_key_here" >nul
    if %errorlevel% neq 0 (
        echo ERROR: EDAMAM_APP_KEY not properly configured in .env file
        echo Please edit .env file and add your actual Edamam App Key
        pause
        exit /b 1
    )
    findstr "OPENROUTER_API_KEY=" .env | findstr /v "your_openrouter_api_key_here" >nul
    if %errorlevel% neq 0 (
        echo ERROR: OPENROUTER_API_KEY not properly configured in .env file
        echo Please edit .env file and add your actual OpenRouter API Key
        pause
        exit /b 1
    )
    echo API keys configuration verified.
)
echo.

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

REM Wait for backend to start and verify
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul
curl -s http://127.0.0.1:8000/api/v1/health >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Backend health check failed, but continuing...
    echo Backend may still be starting up
) else (
    echo Backend health check passed
)

REM Start frontend
echo Starting frontend server...
start "SavorMe Frontend" /min cmd /c "cd demo_app && ..\venv\Scripts\activate.bat && python app.py"

REM Wait for frontend to start and verify
echo Waiting for frontend to initialize...
timeout /t 5 /nobreak >nul
curl -s http://localhost:5000/ >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Frontend health check failed, but continuing...
    echo Frontend may still be starting up
) else (
    echo Frontend health check passed
)

REM Open browser
echo Opening browser...
start http://localhost:5000

echo.
echo ========================================
echo SavorMe Professional Startup Complete!
echo ========================================
echo.
echo Backend URL: http://127.0.0.1:8000
echo Frontend URL: http://localhost:5000
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Both servers are running in minimized windows.
echo The application should open in your browser shortly.
echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo 1. Test the complete user flow:
echo    - Landing page (mobile-first vertical layout)
echo    - Click "Start Your Journey"
echo    - Complete profile form
echo    - Select mood preferences
echo    - View recipe recommendations
echo.
echo 2. Check API documentation: http://127.0.0.1:8000/docs
echo.
echo ========================================
echo Documentation Integration Complete
echo ========================================
echo.
echo This startup script integrates with:
echo - MASTER_FILE_ORGANIZATION.md (file structure)
echo - CUSTOMIZATIONS_PERSISTENT.md (design system)
echo - SAVORME_MASTER_OVERVIEW.md (project overview)
echo - AUTOMATED_APP_STARTUP_GUIDE.md (this process)
echo.
echo For detailed troubleshooting, see AUTOMATED_APP_STARTUP_GUIDE.md
echo.
echo Press any key to close this window...
pause >nul
