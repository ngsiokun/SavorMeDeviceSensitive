@echo off
setlocal enabledelayedexpansion

REM ========================================
REM SavorMe Setup Validation Script
REM Checks what's installed and what's missing
REM ========================================

echo ========================================
echo SavorMe Setup Validation
echo ========================================
echo.

set MISSING_COUNT=0

REM === Check Google Cloud SDK ===
echo [CHECK] Google Cloud SDK...
gcloud version >nul 2>&1
if errorlevel 1 (
    echo [❌ MISSING] Google Cloud SDK not found
    echo [INFO] Install from: https://cloud.google.com/sdk/docs/install
    set /a MISSING_COUNT+=1
) else (
    echo [✅ FOUND] Google Cloud SDK installed
    for /f "tokens=*" %%i in ('gcloud version --format="value(Google Cloud SDK)"') do set GCLOUD_VERSION=%%i
    echo [INFO] Version: !GCLOUD_VERSION!
)

REM === Check Docker ===
echo.
echo [CHECK] Docker Desktop...
docker version >nul 2>&1
if errorlevel 1 (
    echo [❌ MISSING] Docker Desktop not found
    echo [INFO] Install from: https://www.docker.com/products/docker-desktop/
    echo [INFO] Note: Docker is optional for deployment (Cloud Build handles it)
    set /a MISSING_COUNT+=1
) else (
    echo [✅ FOUND] Docker Desktop installed
    for /f "tokens=*" %%i in ('docker version --format "{{.Server.Version}}" 2^>nul') do set DOCKER_VERSION=%%i
    if "!DOCKER_VERSION!"=="" (
        echo [⚠️  WARNING] Docker Desktop may not be running
    ) else (
        echo [INFO] Version: !DOCKER_VERSION!
    )
)

REM === Check .env file ===
echo.
echo [CHECK] Environment file...
if exist ".env" (
    echo [✅ FOUND] .env file exists
    echo [INFO] Make sure it contains: EDAMAM_APP_ID, EDAMAM_APP_KEY, OPENROUTER_API_KEY
) else (
    echo [❌ MISSING] .env file not found
    echo [INFO] Copy your .env file to the project root directory
    set /a MISSING_COUNT+=1
)

REM === Check Google Cloud Authentication ===
echo.
echo [CHECK] Google Cloud Authentication...
gcloud auth list --filter=status:ACTIVE --format="value(account)" >nul 2>&1
if errorlevel 1 (
    echo [❌ NOT AUTHENTICATED] Not logged into Google Cloud
    echo [INFO] Run: gcloud auth login
    set /a MISSING_COUNT+=1
) else (
    echo [✅ AUTHENTICATED] Logged into Google Cloud
    for /f "tokens=*" %%i in ('gcloud auth list --filter=status:ACTIVE --format="value(account)"') do set GCLOUD_ACCOUNT=%%i
    echo [INFO] Account: !GCLOUD_ACCOUNT!
)

REM === Check Google Cloud Project ===
echo.
echo [CHECK] Google Cloud Project...
for /f "tokens=*" %%i in ('gcloud config get-value project 2^>nul') do set PROJECT_ID=%%i
if "%PROJECT_ID%"=="" (
    echo [❌ NO PROJECT] No Google Cloud project set
    echo [INFO] Run: gcloud config set project YOUR_PROJECT_ID
    set /a MISSING_COUNT+=1
) else (
    echo [✅ PROJECT SET] Google Cloud project configured
    echo [INFO] Project ID: %PROJECT_ID%
)

REM === Summary ===
echo.
echo ========================================
echo Setup Summary
echo ========================================
echo.

if %MISSING_COUNT%==0 (
    echo [🎉 READY TO DEPLOY!]
    echo.
    echo Everything is set up correctly. You can now run:
    echo.
    echo   .\deploy-to-cloud-run.bat
    echo.
    echo Or test Docker builds first:
    echo.
    echo   .\test-docker-builds.bat
) else (
    echo [⚠️  SETUP INCOMPLETE]
    echo.
    echo Missing %MISSING_COUNT% requirement(s). Please install/setup:
    echo.
    echo 1. Google Cloud SDK (required for deployment)
    echo 2. Docker Desktop (optional, for local testing)
    echo 3. .env file with API keys
    echo 4. Google Cloud authentication
    echo 5. Google Cloud project configuration
    echo.
    echo See SETUP_REQUIREMENTS.md for detailed instructions.
)

echo.
pause
