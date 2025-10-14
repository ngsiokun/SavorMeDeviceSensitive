# 🧪 Local Testing Guide

## 📋 Prerequisites
- `.env` file with API keys
- Virtual environment activated
- Python 3.12

## 🚀 Start Local Services

### Option 1: Start Everything (Recommended)
```cmd
start.bat
```
This will start:
- Backend: http://127.0.0.1:8000
- Frontend: http://localhost:5000

### Option 2: Manual Start (for debugging)

**Terminal 1 - Backend:**
```cmd
venv\Scripts\activate
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```cmd
cd demo_app
venv\Scripts\activate
set BACKEND_URL=http://127.0.0.1:8000
python app.py
```

## ✅ Test Checklist

### 1. Backend Health Check
Open: http://127.0.0.1:8000/docs

Check:
- [ ] `/health` endpoint returns 200
- [ ] `/api/v1/recipes/recommend` is available
- [ ] Can see all API endpoints

### 2. Frontend Access
Open: http://localhost:5000

Check:
- [ ] Landing page loads
- [ ] "Start Your Journey" button works

### 3. Profile Page
Check:
- [ ] All form fields editable
- [ ] Cuisine dropdown shows:
  - 🎲 Surprise Me
  - 🫒 Mediterranean (selected by default)
  - 🍜 Asian
  - 🍝 Italian
  - 🌮 Mexican
- [ ] "Continue to Mood Selection" works

### 4. Mood Selection
Check:
- [ ] Can select up to 3 moods
- [ ] Intensity buttons work (A little, Medium, Very)
- [ ] "Get My Recipe Recommendation" button enabled

### 5. Recipe Results
Test each cuisine:

**Test 1: Mediterranean + Stressed**
- Expected: Greek/Mediterranean recipe with calming ingredients

**Test 2: Asian + Fatigued**
- Expected: Asian recipe with energizing ingredients

**Test 3: Italian + Low Mood**
- Expected: Italian recipe with mood-boosting nutrients

**Test 4: Mexican + Irritable**
- Expected: Mexican recipe with stabilizing ingredients

**Test 5: Surprise Me + Multiple Moods**
- Expected: Any cuisine, balanced recipe

### 6. Error Handling
- [ ] If API fails, shows friendly error message
- [ ] Can navigate back and try again
- [ ] No console errors

## 🐛 Common Issues

### Backend won't start
```cmd
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process if needed
taskkill /PID <PID> /F
```

### Frontend won't connect
- Check `BACKEND_URL` environment variable
- Check backend is running on port 8000
- Check browser console for errors

### No recipes found
- Check `.env` has valid `EDAMAM_APP_ID` and `EDAMAM_APP_KEY`
- Try "Surprise Me" cuisine (no cuisine filter)
- Check backend logs for errors

## 📊 Expected Response Times (Local)
- Backend startup: 2-3 seconds
- Recipe recommendation: 2-5 seconds
- Page navigation: <1 second

## ✅ Success Criteria
- [ ] All 4 cuisines work
- [ ] All 4 moods generate recipes
- [ ] Nutritional info displays correctly
- [ ] No errors in console
- [ ] Fast response times
- [ ] Beautiful UI on both mobile and desktop views

---

**Once local testing passes, proceed to Cloud Run deployment! 🚀**

