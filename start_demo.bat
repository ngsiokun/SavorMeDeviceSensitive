@echo off
echo ========================================
echo Starting SavorMe Demo App
echo ========================================

cd /d "%~dp0\demo_app"

REM Activate virtual environment
call ..\venv\Scripts\activate.bat

echo.
echo Starting Flask demo app on http://localhost:5000
echo.

py app.py

pause

