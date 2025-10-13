@echo off
setlocal enabledelayedexpansion

REM ========================================
REM SavorMe Docker Build Test Script
REM Tests all Docker builds locally before deployment
REM ========================================

echo ========================================
echo SavorMe Docker Build Tests
echo ========================================
echo.

REM === Check if Docker is running ===
docker version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker not found or not running!
    echo [ERROR] Please install Docker Desktop and start it
    pause
    exit /b 1
)

echo [INFO] Docker is running
echo.

REM === Test Frontend Build ===
echo [TEST] Building frontend Docker image...
docker build -t savorme-frontend-test ./frontend_app
if errorlevel 1 (
    echo [FAILED] Frontend build failed
    goto cleanup
) else (
    echo [PASSED] Frontend build successful
)

REM === Test User Nutrition Service Build ===
echo [TEST] Building user-nutrition service Docker image...
docker build -t savorme-user-nutrition-test ./backend_app/user-nutrition-service
if errorlevel 1 (
    echo [FAILED] User Nutrition service build failed
    goto cleanup
) else (
    echo [PASSED] User Nutrition service build successful
)

REM === Test Recipe Service Build ===
echo [TEST] Building recipe service Docker image...
docker build -t savorme-recipe-test ./backend_app/recipe-service
if errorlevel 1 (
    echo [FAILED] Recipe service build failed
    goto cleanup
) else (
    echo [PASSED] Recipe service build successful
)

REM === Test Mood AI Service Build ===
echo [TEST] Building mood-ai service Docker image...
docker build -t savorme-mood-ai-test ./backend_app/mood-ai-service
if errorlevel 1 (
    echo [FAILED] Mood AI service build failed
    goto cleanup
) else (
    echo [PASSED] Mood AI service build successful
)

REM === Test Router Build ===
echo [TEST] Building router (API Gateway) Docker image...
docker build -t savorme-router-test ./router
if errorlevel 1 (
    echo [FAILED] Router build failed
    goto cleanup
) else (
    echo [PASSED] Router build successful
)

echo.
echo ========================================
echo All Docker Builds Successful! ✅
echo ========================================
echo.
echo You can now proceed with Cloud Run deployment:
echo    deploy-to-cloud-run.bat
echo.
echo Or deploy just the frontend:
echo    deploy-frontend-only.bat
echo.
goto end

:cleanup
echo.
echo ========================================
echo Docker Build Tests Failed ❌
echo ========================================
echo.
echo Please fix the build errors before deploying to Cloud Run.
echo Check the error messages above for details.
echo.
echo Common issues:
echo - Missing .env file
echo - Incorrect file paths in Dockerfile
echo - Missing dependencies in requirements.txt
echo.

:end
echo Cleaning up test images...
docker rmi savorme-frontend-test savorme-user-nutrition-test savorme-recipe-test savorme-mood-ai-test savorme-router-test >nul 2>&1
echo Done.
pause
