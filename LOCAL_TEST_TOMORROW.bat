@echo off
echo ============================================================
echo SAVORME LOCAL TESTING - TOMORROW
echo ============================================================
echo.
echo This script will start BOTH backend and frontend for testing.
echo.
echo STEP 1: Starting Backend (Port 8000)...
echo ============================================================
cd /d C:\Users\Samsung\savorme-cloud-run\SavorMeDeviceSensitive
start "SavorMe Backend" cmd /k "call venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
echo Backend starting in new window...
echo.
timeout /t 5 /nobreak
echo.
echo STEP 2: Starting Frontend (Port 5000)...
echo ============================================================
cd /d C:\Users\Samsung\savorme-cloud-run\SavorMeDeviceSensitive\demo_app
start "SavorMe Frontend" cmd /k "set BACKEND_URL=http://127.0.0.1:8000 && python app.py"
echo Frontend starting in new window...
echo.
echo ============================================================
echo BOTH SERVICES STARTED!
echo ============================================================
echo.
echo Backend: http://127.0.0.1:8000/docs
echo Frontend: http://localhost:5000
echo.
echo Wait 10 seconds, then open: http://localhost:5000
echo.
echo To stop: Close both command windows
echo ============================================================
pause

