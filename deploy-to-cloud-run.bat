@echo off
setlocal enabledelayedexpansion

REM ========================================
REM SavorMe Cloud Run Deployment Script
REM ========================================

echo ========================================
echo SavorMe Cloud Run Deployment
echo ========================================
echo.

REM === Set gcloud path ===
set GCLOUD_PATH=C:\Users\Samsung\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd

REM === Check if gcloud is installed ===
"%GCLOUD_PATH%" version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Google Cloud SDK not found at %GCLOUD_PATH%!
    echo [ERROR] Please install gcloud CLI first:
    echo         https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM === Check if user is authenticated ===
"%GCLOUD_PATH%" auth list --filter=status:ACTIVE --format="value(account)" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Not authenticated with Google Cloud
    echo [INFO] Please run: gcloud auth login
    pause
    exit /b 1
)

REM === Get current project ===
for /f "tokens=*" %%i in ('"%GCLOUD_PATH%" config get-value project') do set PROJECT_ID=%%i
if "%PROJECT_ID%"=="" (
    echo [ERROR] No Google Cloud project set!
    echo [INFO] Please run: gcloud config set project YOUR_PROJECT_ID
    pause
    exit /b 1
)

echo [INFO] Current project: %PROJECT_ID%
echo.

REM === Check if .env file exists ===
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo [WARNING] Make sure your environment variables are set in Cloud Run
    echo.
)

REM === Enable required APIs ===
echo [INFO] Enabling required Google Cloud APIs...
"%GCLOUD_PATH%" services enable cloudbuild.googleapis.com
"%GCLOUD_PATH%" services enable run.googleapis.com
"%GCLOUD_PATH%" services enable containerregistry.googleapis.com

REM === Get current Git commit SHA ===
echo [INFO] Getting current Git commit SHA...
FOR /F "delims=" %%i IN ('git rev-parse HEAD') DO (
    SET CURRENT_COMMIT_SHA=%%i
)

IF NOT DEFINED CURRENT_COMMIT_SHA (
    echo [ERROR] Could not determine Git commit SHA. Make sure you are in a Git repository.
    pause
    exit /b 1
)

echo [INFO] Using commit SHA: %CURRENT_COMMIT_SHA%

REM === Build and deploy using Cloud Build ===
echo.
echo [INFO] Starting deployment using Cloud Build...
echo [INFO] This will build and deploy all services to Cloud Run
echo.

"%GCLOUD_PATH%" builds submit --config cloudbuild.yaml . --substitutions=COMMIT_SHA="%CURRENT_COMMIT_SHA%"

if errorlevel 1 (
    echo.
    echo [ERROR] Deployment failed!
    echo [INFO] Check the build logs above for details
    pause
    exit /b 1
)

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Your services are now deployed to Cloud Run:
echo.
echo Frontend: https://savorme-frontend-%PROJECT_ID%-uc.a.run.app
echo API Gateway: https://savorme-router-%PROJECT_ID%-uc.a.run.app
echo.
echo Individual Services:
echo - User Nutrition: https://savorme-user-nutrition-%PROJECT_ID%-uc.a.run.app
echo - Recipe Service: https://savorme-recipe-%PROJECT_ID%-uc.a.run.app
echo - Mood AI Service: https://savorme-mood-ai-%PROJECT_ID%-uc.a.run.app
echo.
echo Opening frontend in browser...
start https://savorme-frontend-%PROJECT_ID%-uc.a.run.app
echo.
pause
