@echo off
echo ========================================
echo Starting SavorMe Application (Reliable)
echo ========================================

echo.
echo Step 1: Clearing Python cache...
if exist app\__pycache__ rd /s /q app\__pycache__ 2>nul
if exist app\api\__pycache__ rd /s /q app\api\__pycache__ 2>nul
if exist app\models\__pycache__ rd /s /q app\models\__pycache__ 2>nul
if exist app\services\__pycache__ rd /s /q app\services\__pycache__ 2>nul
if exist app\core\__pycache__ rd /s /q app\core\__pycache__ 2>nul
if exist app\data\__pycache__ rd /s /q app\data\__pycache__ 2>nul

echo.
echo Step 2: Testing imports...
venv\Scripts\python.exe test_imports.py
if %errorlevel% neq 0 (
    echo ❌ Import test failed! Please check the errors above.
    pause
    exit /b 1
)

echo.
echo Step 3: Starting backend server...
echo Backend will run on: http://127.0.0.1:8000
start "SavorMe Backend" cmd /c "venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

echo.
echo Step 4: Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Step 5: Starting frontend server...
echo Frontend will run on: http://localhost:5000
start "SavorMe Frontend" cmd /c "cd demo_app && ..\venv\Scripts\python.exe app.py"

echo.
echo ========================================
echo ✅ Both servers started successfully!
echo ========================================
echo.
echo 🌐 Frontend: http://localhost:5000
echo 🔧 Backend:  http://127.0.0.1:8000
echo 📚 API Docs: http://127.0.0.1:8000/docs
echo.
echo Press any key to exit this window...
pause >nul
