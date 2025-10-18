@echo off
REM ============================================================
REM Deploy SavorMe with Auto-Detect Router to Google Cloud Run
REM ============================================================
REM
REM This deploys:
REM   1. Backend API (FastAPI)
REM   2. Mobile Frontend (Port 5000 locally)
REM   3. Desktop Frontend (Port 5001 locally)
REM   4. Auto-Detect Router (Routes based on device)
REM
REM ⚠️ CRITICAL: Use Command Prompt, NOT PowerShell!
REM

echo.
echo ============================================================
echo   SavorMe Auto-Detect Deployment to Cloud Run
echo ============================================================
echo.
echo This will deploy 4 services:
echo   1. Backend API
echo   2. Mobile Frontend
echo   3. Desktop Frontend
echo   4. Auto-Detect Router
echo.
echo ============================================================
pause
echo.

cd /d C:\Users\Samsung\savorme-cloud-run\SavorMeDeviceSensitive

REM Check if gcloud is authenticated
echo [1/5] Checking Google Cloud authentication...
gcloud auth list
echo.

REM Set project
echo [2/5] Setting project...
gcloud config set project savorme-474712
echo.

REM Build and deploy backend
echo [3/5] Deploying Backend API...
gcloud run deploy savorme-backend ^
  --source . ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --set-env-vars EDAMAM_APP_ID=%EDAMAM_APP_ID%,EDAMAM_APP_KEY=%EDAMAM_APP_KEY%,OPENROUTER_API_KEY=%OPENROUTER_API_KEY%

if errorlevel 1 (
    echo [ERROR] Backend deployment failed
    pause
    exit /b 1
)
echo.

REM Build and deploy mobile frontend
echo [4/5] Deploying Mobile Frontend...
gcloud run deploy savorme-mobile ^
  --source demo_app ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --set-env-vars BACKEND_URL=https://savorme-backend-662773309683.us-central1.run.app

if errorlevel 1 (
    echo [ERROR] Mobile frontend deployment failed
    pause
    exit /b 1
)
echo.

REM Build and deploy desktop frontend
echo [5/5] Deploying Desktop Frontend...
gcloud run deploy savorme-desktop ^
  --source desktop_app ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --set-env-vars BACKEND_URL=https://savorme-backend-662773309683.us-central1.run.app

if errorlevel 1 (
    echo [ERROR] Desktop frontend deployment failed
    pause
    exit /b 1
)
echo.

REM Build and deploy router
echo [6/5] Deploying Auto-Detect Router...
gcloud run deploy savorme-router ^
  --dockerfile Dockerfile.router ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --set-env-vars DESKTOP_URL=https://savorme-desktop-662773309683.us-central1.run.app,MOBILE_URL=https://savorme-mobile-662773309683.us-central1.run.app,BACKEND_URL=https://savorme-backend-662773309683.us-central1.run.app

if errorlevel 1 (
    echo [ERROR] Router deployment failed
    pause
    exit /b 1
)
echo.

echo ============================================================
echo   DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo Your services are now live at:
echo.
echo   Auto-Detect Router: https://savorme-router-662773309683.us-central1.run.app
echo   Desktop Frontend:   https://savorme-desktop-662773309683.us-central1.run.app
echo   Mobile Frontend:    https://savorme-mobile-662773309683.us-central1.run.app
echo   Backend API:        https://savorme-backend-662773309683.us-central1.run.app
echo.
echo ============================================================
echo   How It Works:
echo ============================================================
echo.
echo 1. Users visit: https://savorme-router-662773309683.us-central1.run.app
echo 2. Router detects their device (desktop or mobile)
echo 3. Router redirects to appropriate frontend
echo 4. Both frontends connect to same backend API
echo.
echo ============================================================
pause

