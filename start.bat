@echo off
REM ========================================
REM SavorMe Auto-Start v4.0.0
REM Automatic Device Detection - No Menu
REM ========================================
REM 
REM ⚠️ CRITICAL: Use Command Prompt (cmd.exe), NOT PowerShell!
REM
REM This script automatically starts all services with auto-detect enabled.
REM No menu, no choices - just run and go!
REM

echo.
echo ========================================
echo   SavorMe v4.0.0 - Auto Starting...
echo ========================================
echo.
echo Starting all services with automatic device detection...
echo.
echo  Backend:  Port 8000
echo  Mobile:   Port 5000
echo  Desktop:  Port 5001
echo  Router:   Port 8080 (Auto-Detect)
echo.
echo ========================================
echo.

REM Call the auto-detect startup script
call START-ALL-SEPARATE.bat
