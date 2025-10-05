@echo off
setlocal

echo ========================================
echo SavorMe Reliable Startup
echo ========================================
echo.

echo [INFO] Checking environment...

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo [INFO] Please run setup_new_clone.bat first
    pause
    goto :eof
)

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found, creating template...
    echo # SavorMe Backend Environment Variables > .env
    echo # Copy this file and add your actual API keys >> .env
    echo. >> .env
    echo # Edamam Recipe API >> .env
    echo EDAMAM_APP_ID=your_edamam_app_id >> .env
    echo EDAMAM_APP_KEY=your_edamam_app_key >> .env
    echo. >> .env
    echo # OpenRouter AI API >> .env
    echo OPENROUTER_API_KEY=your_openrouter_api_key >> .env
    echo. >> .env
    echo # CORS Origins >> .env
    echo CORS_ORIGINS=http://localhost:5000,http://127.0.0.1:5000 >> .env
    echo [OK] .env template created
)

echo [INFO] Starting SavorMe Backend API...
echo [INFO] Backend will be available at: http://127.0.0.1:8000
echo [INFO] API Documentation: http://127.0.0.1:8000/docs
echo [INFO] Press Ctrl+C to stop the server
echo.

REM Start the application using virtual environment Python
venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

endlocal
