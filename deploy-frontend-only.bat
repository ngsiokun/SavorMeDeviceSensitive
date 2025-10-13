@echo off
setlocal enabledelayedexpansion

REM ========================================
REM SavorMe Frontend-Only Cloud Run Deployment
REM This deploys just the frontend for quick testing
REM ========================================

echo ========================================
echo SavorMe Frontend-Only Deployment
echo ========================================
echo.

REM === Check if gcloud is installed ===
gcloud version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Google Cloud SDK not found!
    echo [ERROR] Please install gcloud CLI first:
    echo         https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM === Check if user is authenticated ===
gcloud auth list --filter=status:ACTIVE --format="value(account)" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Not authenticated with Google Cloud
    echo [INFO] Please run: gcloud auth login
    pause
    exit /b 1
)

REM === Get current project ===
for /f "tokens=*" %%i in ('gcloud config get-value project') do set PROJECT_ID=%%i
if "%PROJECT_ID%"=="" (
    echo [ERROR] No Google Cloud project set!
    echo [INFO] Please run: gcloud config set project YOUR_PROJECT_ID
    pause
    exit /b 1
)

echo [INFO] Current project: %PROJECT_ID%
echo.

REM === Enable required APIs ===
echo [INFO] Enabling required Google Cloud APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

REM === Build and deploy frontend only ===
echo.
echo [INFO] Building and deploying frontend to Cloud Run...
echo.

REM Build the frontend image
gcloud builds submit --tag gcr.io/%PROJECT_ID%/savorme-frontend ./frontend_app

if errorlevel 1 (
    echo.
    echo [ERROR] Frontend build failed!
    echo [INFO] Check the build logs above for details
    pause
    exit /b 1
)

REM Deploy to Cloud Run
gcloud run deploy savorme-frontend \
    --image gcr.io/%PROJECT_ID%/savorme-frontend \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10 \
    --set-env-vars BACKEND_URL=https://your-backend-url-here

if errorlevel 1 (
    echo.
    echo [ERROR] Frontend deployment failed!
    echo [INFO] Check the deployment logs above for details
    pause
    exit /b 1
)

echo.
echo ========================================
echo Frontend Deployment Complete!
echo ========================================
echo.
echo Your frontend is now deployed to Cloud Run:
echo https://savorme-frontend-%PROJECT_ID%-uc.a.run.app
echo.
echo NOTE: You need to update the BACKEND_URL environment variable
echo to point to your actual backend service URL.
echo.
echo Opening frontend in browser...
start https://savorme-frontend-%PROJECT_ID%-uc.a.run.app
echo.
pause
