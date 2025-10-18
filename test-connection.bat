@echo off
echo ============================================
echo Testing SavorMe Frontend-Backend Connection
echo ============================================
echo.

echo 1. Testing Backend Health (Port 8000)...
curl -s http://127.0.0.1:8000/api/v1/health
if errorlevel 1 (
    echo [ERROR] Backend is not responding!
    pause
    exit /b 1
)
echo [OK] Backend is healthy
echo.

echo 2. Testing Desktop App Health (Port 5001)...
curl -s http://127.0.0.1:5001/api/health
if errorlevel 1 (
    echo [ERROR] Desktop app is not responding!
    pause
    exit /b 1
)
echo [OK] Desktop app is healthy
echo.

echo 3. Testing Nutrition Calculation API...
curl -X POST http://127.0.0.1:5001/api/nutrition/calculate -H "Content-Type: application/json" -d "{\"age\":30,\"gender\":\"male\",\"height_cm\":175,\"weight_kg\":70,\"dietary_preference\":\"none\",\"food_allergies\":[],\"cuisine_preferences\":[]}"
echo.
if errorlevel 1 (
    echo [ERROR] Nutrition calculation failed!
    pause
    exit /b 1
)
echo [OK] Nutrition API is working
echo.

echo ============================================
echo All tests passed! Frontend and Backend are properly connected.
echo ============================================
pause


