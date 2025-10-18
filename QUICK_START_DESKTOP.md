# 🖥️ SavorMe Desktop App - Quick Start Guide

## ✅ Current Status
- **Backend:** Running on http://127.0.0.1:8000
- **Desktop App:** Running on http://localhost:5001
- **Status:** ✅ Both services are healthy and connected

## 🚀 Quick Start

### Access the App
Open your browser and navigate to:
```
http://localhost:5001
```

### Test the Connection
```batch
curl http://127.0.0.1:5001/api/health
```

## 📋 User Flow

1. **Landing Page** (http://localhost:5001)
   - Click "Get Started"

2. **Profile Page** (http://localhost:5001/profile)
   - Enter your age, gender, height, weight
   - Select dietary preferences (vegetarian, vegan, etc.)
   - Choose cuisine preferences (Italian, Mexican, etc.)
   - Add any food allergies
   - Click "Continue"

3. **Mood Selection** (http://localhost:5001/mood)
   - Select 1-3 moods:
     - 😰 Stressed/Anxious
     - 😴 Fatigued/Low Energy
     - 😔 Low Mood/Sad
     - 😠 Irritable/Cranky
   - Choose intensity (A little, Medium, Very)
   - Click "Get My Recipe Recommendation"

4. **Results Page** (http://localhost:5001/results)
   - View your personalized recipe recommendation
   - See nutrition information
   - Click "View Full Recipe" to see cooking instructions
   - Save recipe to favorites

## 🔧 If Services Are Not Running

### Start Both Services
```batch
cmd /c start-desktop-with-backend.bat
```

### Or Start Separately

**Start Backend:**
```batch
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Start Desktop App:**
```batch
call venv\Scripts\activate.bat
cd desktop_app
python app.py
```

### Restart Desktop App Only
```batch
cmd /c restart-desktop.bat
```

## 🐛 Troubleshooting

### Desktop App Won't Start
1. Check if port 5001 is already in use
2. Check logs: `logs\desktop.err.log`
3. Make sure backend is running first

### Backend Won't Start
1. Check if port 8000 is already in use
2. Check logs: `logs\backend.err.log`
3. Verify `.env` file exists with API keys

### Recipe Recommendations Failing
1. Verify backend health: `curl http://127.0.0.1:8000/api/v1/health`
2. Verify desktop health: `curl http://127.0.0.1:5001/api/health`
3. Check browser console for JavaScript errors (F12)
4. Check backend logs for API errors

### Kill Stuck Processes
```batch
REM Kill process on port 8000
for /f "tokens=5" %p in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /PID %p /F

REM Kill process on port 5001
for /f "tokens=5" %p in ('netstat -aon ^| find ":5001" ^| find "LISTENING"') do taskkill /PID %p /F
```

## 📊 API Endpoints

### Desktop App (Port 5001)
- `GET /` - Landing page
- `GET /profile` - Profile page
- `GET /mood` - Mood selection page
- `GET /results` - Recipe results page
- `POST /api/nutrition/calculate` - Calculate nutrition targets
- `POST /api/mood/interpret` - Interpret mood selection
- `POST /api/recipes/recommend` - Get recipe recommendation
- `GET /api/health` - Health check

### Backend API (Port 8000)
- `GET /` - API information
- `GET /docs` - Interactive API documentation
- `GET /api/v1/health` - Health check
- `POST /api/v1/nutrition/calculate` - Calculate nutrition
- `POST /api/v1/mood/interpret` - Interpret mood
- `POST /api/v1/recipes/recommend` - Recommend recipe

## 📝 Important Notes

⚠️ **Use Command Prompt (cmd.exe), NOT PowerShell**

⚠️ **Required Ports:**
- 8000 (Backend)
- 5001 (Desktop App)

⚠️ **Required Files:**
- `.env` file with API keys
- Virtual environment activated
- All dependencies installed

## 🔗 Links

- Desktop App: http://localhost:5001
- Backend API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs
- Mobile App: http://localhost:5000

## 📚 Documentation

For detailed information, see:
- `DESKTOP_APP_FIX_SUMMARY.md` - Complete fix documentation
- `CUSTOMIZATIONS_PERSISTENT.md` - Full project documentation
- `README.md` - Project overview

---

**Last Updated:** October 18, 2025
**Status:** ✅ All Systems Operational



