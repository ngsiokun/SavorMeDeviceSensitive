@echo off
echo Cleaning up all SavorMe processes...

REM Kill all processes on port 8000 (Backend)
echo Killing backend processes on port 8000...
for /f "tokens=5" %%p in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing PID %%p
    taskkill /PID %%p /F >nul 2>&1
)

REM Kill all processes on port 5001 (Desktop App)
echo Killing desktop app processes on port 5001...
for /f "tokens=5" %%p in ('netstat -aon ^| findstr :5001 ^| findstr LISTENING') do (
    echo Killing PID %%p
    taskkill /PID %%p /F >nul 2>&1
)

REM Kill all processes on port 5000 (Mobile App)
echo Killing mobile app processes on port 5000...
for /f "tokens=5" %%p in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    echo Killing PID %%p
    taskkill /PID %%p /F >nul 2>&1
)

echo.
echo All processes cleaned up!
echo.
pause



