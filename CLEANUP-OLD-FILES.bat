@echo off
REM ========================================
REM SavorMe - Cleanup Old/Test Files
REM v4.0.0 Cleanup Script
REM ========================================
REM
REM This script removes obsolete test files and temporary files
REM that are no longer needed after v4.0.0 upgrade
REM

echo.
echo ========================================
echo   SavorMe File Cleanup v4.0.0
echo ========================================
echo.
echo This will DELETE obsolete test and temporary files.
echo.
echo Files to be deleted:
echo   - test-api-direct.py
echo   - test-backend-direct.bat
echo   - test-connection.bat (if not used)
echo   - START-UNIFIED.bat (obsolete)
echo   - unified_app.py (not recommended approach)
echo   - start-desktop-with-backend.bat (replaced)
echo   - CHATGPT_HELP_REQUEST.md (temporary)
echo   - GEMINI_DEPLOYMENT_CONSULTATION.md (temporary)
echo   - BACKEND_TROUBLESHOOTING_FOR_GEMINI.md (temporary)
echo.
echo ========================================
echo.
set /p confirm="Are you sure you want to delete these files? (Y/N): "

if /i not "%confirm%"=="Y" (
    echo.
    echo Cleanup cancelled.
    pause
    exit /b 0
)

echo.
echo Starting cleanup...
echo.

REM Delete test files
if exist "test-api-direct.py" (
    del "test-api-direct.py"
    echo [DELETED] test-api-direct.py
)

if exist "test-backend-direct.bat" (
    del "test-backend-direct.bat"
    echo [DELETED] test-backend-direct.bat
)

REM Delete obsolete startup files
if exist "START-UNIFIED.bat" (
    del "START-UNIFIED.bat"
    echo [DELETED] START-UNIFIED.bat
)

if exist "unified_app.py" (
    del "unified_app.py"
    echo [DELETED] unified_app.py
)

if exist "start-desktop-with-backend.bat" (
    del "start-desktop-with-backend.bat"
    echo [DELETED] start-desktop-with-backend.bat
)

if exist "restart-all.bat" (
    del "restart-all.bat"
    echo [DELETED] restart-all.bat
)

REM Delete temporary consultation files
if exist "CHATGPT_HELP_REQUEST.md" (
    del "CHATGPT_HELP_REQUEST.md"
    echo [DELETED] CHATGPT_HELP_REQUEST.md
)

if exist "GEMINI_DEPLOYMENT_CONSULTATION.md" (
    del "GEMINI_DEPLOYMENT_CONSULTATION.md"
    echo [DELETED] GEMINI_DEPLOYMENT_CONSULTATION.md
)

if exist "BACKEND_TROUBLESHOOTING_FOR_GEMINI.md" (
    del "BACKEND_TROUBLESHOOTING_FOR_GEMINI.md"
    echo [DELETED] BACKEND_TROUBLESHOOTING_FOR_GEMINI.md (replaced by TROUBLESHOOTING_QA.md)
)

if exist "BACKEND_CONNECTION_TROUBLESHOOTING.md" (
    del "BACKEND_CONNECTION_TROUBLESHOOTING.md"
    echo [DELETED] BACKEND_CONNECTION_TROUBLESHOOTING.md (replaced by TROUBLESHOOTING_QA.md)
)

echo.
echo ========================================
echo   Cleanup Complete!
echo ========================================
echo.
echo Obsolete files have been removed.
echo.
echo Your project now has only essential files:
echo   ✓ START.bat (auto-detect)
echo   ✓ app_router.py (device router)
echo   ✓ All documentation up to date
echo.
pause

