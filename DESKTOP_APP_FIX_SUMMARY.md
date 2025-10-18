# SavorMe Desktop App - Backend Connection Fix

## Issue Summary
The desktop app (running on port 5001) could not connect to the FastAPI backend for recipe recommendations, resulting in 500 Internal Server Error.

## Root Causes Identified

### 1. Backend Service Not Running
- FastAPI backend was not started on port 8000
- Desktop app requires backend API to process recipe recommendations

### 2. Incorrect API Endpoint Paths
- Desktop app was calling endpoints without the `/api/v1/` prefix
- Backend routes are mounted under `/api/v1/` prefix
- **Fixed endpoints:**
  - ❌ `/nutrition/calculate` → ✅ `/api/v1/nutrition/calculate`
  - ❌ `/mood/interpret` → ✅ `/api/v1/mood/interpret`
  - ❌ `/recipes/recommend` → ✅ `/api/v1/recipes/recommend`
  - ❌ `/health` → ✅ `/api/v1/health`

### 3. Data Format Mismatch
- Desktop app was sending data in a different format than the backend expected
- Backend requires specific Pydantic model structures (`MoodBlend`, `UserProfile`)
- **Added transformation function** in `desktop-results.html` to convert frontend data to backend format

### 4. Response Format Mismatch
- Desktop app expected an array of recipes (`data.recipes[]`)
- Backend returns a single recommendation object (`data.recipe`)
- **Updated display logic** to handle single recipe response with full recommendation data

### 5. Encoding Issue
- Desktop app had Unicode encoding errors with emoji characters in print statements
- Caused app to crash on startup in Windows Command Prompt
- **Fixed**: Removed emoji characters from print statements

## Files Modified

### 1. `desktop_app/app.py`
- Fixed all API endpoint paths to include `/api/v1/` prefix
- Removed emoji characters causing encoding errors

### 2. `desktop_app/templates/desktop-results.html`
- Added `transformToBackendFormat()` function to convert form data to backend API format
- Updated `displayResults()` to handle single recipe recommendation response
- Updated modal view to display recipe using correct field names from backend
- Added proper error handling and logging

### 3. `start-desktop-with-backend.bat` (NEW)
- Created automated startup script for both backend and desktop app
- Includes health checks and automatic port cleanup
- Provides clear status messages

### 4. `restart-desktop.bat` (NEW)
- Quick restart script for desktop app only
- Useful for applying changes without restarting backend

## How to Start the Application

### Option 1: Start Both Services Together
```batch
cmd /c start-desktop-with-backend.bat
```

### Option 2: Start Services Separately

#### Start Backend (Port 8000)
```batch
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Start Desktop App (Port 5001)
```batch
call venv\Scripts\activate.bat
cd desktop_app
python app.py
```

## Testing the Fix

### 1. Test Backend Health
```batch
curl http://127.0.0.1:8000/api/v1/health
```
**Expected Response:**
```json
{
  "status": "healthy",
  "version": "2.1.0",
  "service": "SavorMe Backend API",
  "timestamp": "2025-10-05T00:00:00Z"
}
```

### 2. Test Desktop App Health
```batch
curl http://127.0.0.1:5001/api/health
```
**Expected Response:**
```json
{
  "service": "SavorMe Backend API",
  "status": "healthy",
  "timestamp": "2025-10-05T00:00:00Z",
  "version": "2.1.0"
}
```

### 3. Test End-to-End Flow
1. Open browser: http://localhost:5001
2. Navigate to Profile page
3. Fill in profile information (age, gender, height, weight, etc.)
4. Click "Continue" to Mood Selection
5. Select 1-3 moods (stressed, fatigued, sad, or irritable)
6. Select mood intensity
7. Click "Get My Recipe Recommendation"
8. Verify recipe results display correctly with:
   - Recipe image
   - Recipe name and cuisine type
   - Emotional rationale
   - Nutrition information
   - Cooking instructions (in modal)
   - Ingredients list (in modal)

## API Request Format

### Desktop App Sends:
```javascript
{
  "mood_blend": {
    "moods": [
      { "mood": "stressed", "intensity": "medium" },
      { "mood": "fatigued", "intensity": "medium" }
    ]
  },
  "user_profile": {
    "age": 30,
    "gender": "male",
    "height_cm": 175,
    "weight_kg": 70,
    "cuisine_preferences": ["italian", "mexican"],
    "food_allergies": [],
    "dietary_preference": "none"
  },
  "activity_level": "moderate"
}
```

### Backend Returns:
```javascript
{
  "recipe": {
    "name": "Recipe Name",
    "image_url": "https://...",
    "cuisine_type": "Italian",
    "ingredients": ["ingredient 1", "ingredient 2"],
    "cooking_directions": ["step 1", "step 2"],
    "nutrition": {
      "calories": 450,
      "protein_g": 25,
      "carbs_g": 40,
      "fat_g": 15,
      "fiber_g": 8
    },
    "servings": 4,
    "prep_time": 30
  },
  "emotional_rationale": "This recipe is perfect because...",
  "flavor_alignment": {
    "nutrient_match_score": 85
  },
  "mood_description": "When feeling stressed and fatigued..."
}
```

## Current Status

✅ **All Issues Fixed**
- Backend service running on port 8000
- Desktop app running on port 5001
- API endpoints correctly configured
- Data transformation working
- Response display working
- Health checks passing

## Next Steps (Optional Enhancements)

1. **Error Handling**: Add more detailed error messages for specific failure scenarios
2. **Loading States**: Improve loading indicators during API calls
3. **Caching**: Implement client-side caching for profile data
4. **Multiple Recipes**: Add support for displaying multiple recipe recommendations
5. **Recipe History**: Track and display user's recipe history
6. **Favorites**: Implement backend persistence for saved recipes

## Important Notes

⚠️ **Always use Command Prompt (cmd.exe), NOT PowerShell!**
- PowerShell has issues with batch scripts and `&&` operators
- The startup scripts are designed for Command Prompt

⚠️ **Port Requirements:**
- Backend: 8000
- Desktop App: 5001
- Make sure these ports are not in use by other applications

⚠️ **Environment Requirements:**
- Virtual environment must be activated
- All dependencies installed via `requirements.txt`
- `.env` file with API keys must exist

## Logs Location
- Backend: `logs/backend.out.log`, `logs/backend.err.log`
- Desktop: `logs/desktop.out.log`, `logs/desktop.err.log`

---

**Date Fixed:** October 18, 2025
**Status:** ✅ Complete and Working



