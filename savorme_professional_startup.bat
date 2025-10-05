@echo off
setlocal enabledelayedexpansion

echo ========================================
echo SavorMe Professional AI Consultant
echo Automated Startup & Diagnostic System
echo ========================================
echo.

REM Set error handling
set "ERROR_COUNT=0"
set "PHASE=0"

REM Function to log errors
:log_error
set /a ERROR_COUNT+=1
echo [ERROR %ERROR_COUNT%] %~1
goto :eof

REM Function to log success
:log_success
echo [SUCCESS] %~1
goto :eof

REM Function to log info
:log_info
echo [INFO] %~1
goto :eof

echo Starting comprehensive diagnostic and startup sequence...
echo.

REM ========================================
REM Phase 1: Environment Setup & Validation
REM ========================================
set /a PHASE+=1
echo Phase %PHASE%: Environment Setup & Validation
echo ----------------------------------------

REM Step 1.1: Verify Python Environment
call :log_info "Checking Python installation..."
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        python3 --version >nul 2>&1
        if %errorlevel% neq 0 (
            call :log_error "Python not found. Please install Python 3.8+"
            goto :diagnostic_failed
        ) else (
            set "PYTHON_CMD=python3"
        )
    ) else (
        set "PYTHON_CMD=py"
    )
) else (
    set "PYTHON_CMD=python"
)

call :log_success "Python found: %PYTHON_CMD%"

REM Step 1.2: Create/Verify Virtual Environment
call :log_info "Checking virtual environment..."
if not exist "venv\Scripts\python.exe" (
    call :log_info "Creating virtual environment..."
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        call :log_error "Failed to create virtual environment"
        goto :diagnostic_failed
    )
    call :log_success "Virtual environment created"
) else (
    call :log_success "Virtual environment exists"
)

REM Step 1.3: Activate Virtual Environment
call :log_info "Activating virtual environment..."
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    call :log_error "Failed to activate virtual environment"
    goto :diagnostic_failed
)
call :log_success "Virtual environment activated"

REM Step 1.4: Install Dependencies
call :log_info "Installing dependencies..."
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    call :log_error "Failed to install dependencies"
    goto :diagnostic_failed
)
call :log_success "Dependencies installed"

REM Verify critical packages
call :log_info "Verifying critical packages..."
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 call :log_error "FastAPI not installed"
pip show uvicorn >nul 2>&1
if %errorlevel% neq 0 call :log_error "Uvicorn not installed"
pip show flask >nul 2>&1
if %errorlevel% neq 0 call :log_error "Flask not installed"
pip show requests >nul 2>&1
if %errorlevel% neq 0 call :log_error "Requests not installed"

REM ========================================
REM Phase 2: Configuration Setup
REM ========================================
set /a PHASE+=1
echo.
echo Phase %PHASE%: Configuration Setup
echo ----------------------------------------

REM Step 2.1: Environment File Setup
call :log_info "Checking .env file..."
if not exist ".env" (
    call :log_info "Creating .env template..."
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
    call :log_success ".env template created"
) else (
    call :log_success ".env file exists"
)

REM Step 2.2: Verify File Structure
call :log_info "Verifying file structure..."
if not exist "app\main.py" (
    call :log_error "Backend main file missing: app\main.py"
    goto :diagnostic_failed
)
if not exist "demo_app\app.py" (
    call :log_error "Frontend main file missing: demo_app\app.py"
    goto :diagnostic_failed
)
if not exist "demo_app\templates\index.html" (
    call :log_error "Landing page template missing: demo_app\templates\index.html"
    goto :diagnostic_failed
)
if not exist "demo_app\templates\recipe_result.html" (
    call :log_error "Recipe result template missing: demo_app\templates\recipe_result.html"
    goto :diagnostic_failed
)
call :log_success "All critical files present"

REM ========================================
REM Phase 3: Backend Startup & Validation
REM ========================================
set /a PHASE+=1
echo.
echo Phase %PHASE%: Backend Startup & Validation
echo ----------------------------------------

REM Step 3.1: Start Backend Server
call :log_info "Starting backend server..."
start "SavorMe Backend" /min cmd /c "venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

REM Wait for backend to start
call :log_info "Waiting for backend to initialize..."
timeout /t 5 /nobreak >nul

REM Step 3.2: Validate Backend Health
call :log_info "Testing backend health..."
curl -s http://127.0.0.1:8000/api/v1/health >nul 2>&1
if %errorlevel% neq 0 (
    call :log_error "Backend health check failed"
    call :log_info "Backend may still be starting up, waiting..."
    timeout /t 10 /nobreak >nul
    curl -s http://127.0.0.1:8000/api/v1/health >nul 2>&1
    if %errorlevel% neq 0 (
        call :log_error "Backend failed to start properly"
        goto :diagnostic_failed
    )
)
call :log_success "Backend is healthy and running"

REM ========================================
REM Phase 4: Frontend Startup & Validation
REM ========================================
set /a PHASE+=1
echo.
echo Phase %PHASE%: Frontend Startup & Validation
echo ----------------------------------------

REM Step 4.1: Start Frontend Server
call :log_info "Starting frontend server..."
start "SavorMe Frontend" /min cmd /c "cd demo_app && ..\venv\Scripts\activate.bat && python app.py"

REM Wait for frontend to start
call :log_info "Waiting for frontend to initialize..."
timeout /t 5 /nobreak >nul

REM Step 4.2: Validate Frontend Routes
call :log_info "Testing frontend routes..."
curl -s http://localhost:5000/ >nul 2>&1
if %errorlevel% neq 0 (
    call :log_error "Frontend health check failed"
    call :log_info "Frontend may still be starting up, waiting..."
    timeout /t 10 /nobreak >nul
    curl -s http://localhost:5000/ >nul 2>&1
    if %errorlevel% neq 0 (
        call :log_error "Frontend failed to start properly"
        goto :diagnostic_failed
    )
)
call :log_success "Frontend is healthy and running"

REM ========================================
REM Phase 5: Integration Testing
REM ========================================
set /a PHASE+=1
echo.
echo Phase %PHASE%: Integration Testing
echo ----------------------------------------

REM Step 5.1: Test API Integration
call :log_info "Testing backend-frontend integration..."
curl -s http://127.0.0.1:8000/docs >nul 2>&1
if %errorlevel% neq 0 (
    call :log_error "API documentation not accessible"
) else (
    call :log_success "API documentation accessible"
)

REM ========================================
REM Phase 6: Final Validation
REM ========================================
set /a PHASE+=1
echo.
echo Phase %PHASE%: Final System Validation
echo ----------------------------------------

echo.
echo ========================================
echo SYSTEM STATUS SUMMARY
echo ========================================
echo Backend URL: http://127.0.0.1:8000
echo Frontend URL: http://localhost:5000
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Error Count: %ERROR_COUNT%
echo.

if %ERROR_COUNT% gtr 0 (
    echo [WARNING] %ERROR_COUNT% errors detected during startup
    echo Please review the error messages above
) else (
    echo [SUCCESS] All systems operational!
    echo.
    echo ========================================
    echo NEXT STEPS:
    echo ========================================
    echo 1. Open your browser to: http://localhost:5000
    echo 2. Test the complete user flow:
    echo    - Landing page (mobile-first vertical layout)
    echo    - Click "Start Your Journey"
    echo    - Complete profile form
    echo    - Select mood preferences
    echo    - View recipe recommendations
    echo.
    echo 3. Check API documentation: http://127.0.0.1:8000/docs
    echo.
    echo Both servers are running in minimized windows.
    echo Close this window when done testing.
)

echo.
echo Press any key to open the application in your browser...
pause >nul

REM Open browser to frontend
start http://localhost:5000

echo.
echo ========================================
echo SavorMe Professional Startup Complete
echo ========================================
echo.
echo The application is now running with:
echo - Mobile-first responsive design
echo - Complete error handling
echo - Professional-grade deployment
echo.
echo Both backend and frontend servers are running.
echo Close the minimized command windows to stop the servers.
echo.
pause
goto :eof

:diagnostic_failed
echo.
echo ========================================
echo DIAGNOSTIC FAILED
echo ========================================
echo.
echo %ERROR_COUNT% errors were detected during startup.
echo Please review the error messages above and:
echo.
echo 1. Check that Python 3.8+ is installed
echo 2. Verify all project files are present
echo 3. Ensure no other applications are using ports 8000 or 5000
echo 4. Run this script again after fixing any issues
echo.
echo For detailed troubleshooting, see: AUTOMATED_APP_STARTUP_GUIDE.md
echo.
pause
exit /b 1
