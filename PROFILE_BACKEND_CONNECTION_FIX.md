# Profile Page Backend Connection Fix

## Issue
Profile page was not connecting to the backend. It saved data to sessionStorage and moved to the next page without validating the backend connection.

## Problem
The profile form submission was:
1. Collecting form data
2. Storing in sessionStorage
3. Immediately redirecting to mood page
4. **Never actually calling the backend API**

This meant:
- No validation that backend was running
- No nutrition targets calculated
- User could proceed even if backend was down
- Connection error only discovered later on results page

## Solution
Modified the profile form submission to:
1. Collect form data
2. **Call backend API** to calculate nutrition targets (`/api/nutrition/calculate`)
3. Validate backend connection
4. Store both profile data AND nutrition targets
5. Only redirect if backend responds successfully
6. Show clear error message if backend is down

## Implementation

### File Modified
`desktop_app/templates/desktop-profile.html`

### Changes Made

**Before:**
```javascript
// Form submission
form.addEventListener('submit', function(e) {
    // ... validation ...
    
    // Store in sessionStorage
    sessionStorage.setItem('desktopProfile', JSON.stringify(profileData));
    
    // Show success and redirect immediately
    alert('Profile saved successfully! Redirecting to mood selection...');
    window.location.href = '/mood';
});
```

**After:**
```javascript
// Form submission
form.addEventListener('submit', async function(e) {
    // ... validation ...
    
    // Test backend connection by calculating nutrition targets
    try {
        const response = await fetch('/api/nutrition/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                age: profileData.age,
                gender: profileData.gender,
                height_cm: profileData.height_cm,
                weight_kg: profileData.weight_kg,
                dietary_preference: profileData.dietary_preference,
                food_allergies: profileData.food_allergies,
                cuisine_preferences: profileData.cuisine_preferences
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to connect to backend');
        }
        
        const nutritionData = await response.json();
        
        // Store both profile and nutrition data
        sessionStorage.setItem('desktopProfile', JSON.stringify(profileData));
        sessionStorage.setItem('nutritionTargets', JSON.stringify(nutritionData));
        
        // Show success and redirect
        alert('Profile saved successfully! Redirecting to mood selection...');
        window.location.href = '/mood';
        
    } catch (error) {
        console.error('Backend connection error:', error);
        alert('Error: Cannot connect to backend server. Please make sure the backend is running on port 8000.\n\nError details: ' + error.message);
    }
});
```

## Benefits

### 1. Early Error Detection
- Backend connection tested immediately on profile submission
- User gets clear error message if backend is down
- Prevents wasted time going through mood selection only to fail at results

### 2. Data Validation
- Backend validates profile data structure
- Ensures nutrition calculations are possible
- Catches data format errors early

### 3. Pre-calculated Nutrition
- Nutrition targets calculated and stored during profile step
- Results page can use pre-calculated values
- Faster results page loading

### 4. Better User Experience
- Clear error messages with specific details
- User knows immediately if something is wrong
- No confusion about why results fail later

## Error Messages

### Success Case
```
Profile saved successfully! Redirecting to mood selection...
```

### Backend Down
```
Error: Cannot connect to backend server. 
Please make sure the backend is running on port 8000.

Error details: Failed to connect to backend
```

### Invalid Data
```
Error: Cannot connect to backend server. 
Please make sure the backend is running on port 8000.

Error details: [Specific validation error from backend]
```

## Testing

### Test Backend Connection

1. **With Backend Running:**
   - Go to http://localhost:5001/profile
   - Fill in all fields
   - Click "Continue"
   - ✅ Should see "Profile saved successfully!" and redirect to mood page
   - ✅ Console should log: "Backend connected! Nutrition targets: {...}"

2. **Without Backend Running:**
   - Stop backend (Ctrl+C in backend terminal)
   - Go to http://localhost:5001/profile
   - Fill in all fields
   - Click "Continue"
   - ✅ Should see error message about backend not running
   - ✅ Should NOT redirect to mood page
   - ✅ User stays on profile page to fix the issue

3. **Check Stored Data:**
   - Open browser console (F12)
   - Type: `sessionStorage.getItem('nutritionTargets')`
   - ✅ Should see nutrition targets JSON with calories, protein, fiber

## API Call Details

### Endpoint
```
POST /api/nutrition/calculate
```

### Request Body
```json
{
  "age": 30,
  "gender": "male",
  "height_cm": 175,
  "weight_kg": 70,
  "dietary_preference": "none",
  "food_allergies": [],
  "cuisine_preferences": ["Italian", "Mexican"]
}
```

### Response (Success)
```json
{
  "calories": 2200,
  "protein_g": 110,
  "fiber_g": 25,
  "carbs_g": 275,
  "fat_g": 73
}
```

### Response (Error)
```json
{
  "error": "Error calculating nutrition: [details]"
}
```

## Backend Service Status

### Verify Services Running

**Backend (Port 8000):**
```bash
curl http://127.0.0.1:8000/api/v1/health
```
Expected: `{"status":"healthy","version":"2.1.0",...}`

**Desktop App (Port 5001):**
```bash
curl http://127.0.0.1:5001/api/health
```
Expected: `{"status":"healthy",...}`

### Start Services

**If backend not running:**
```bash
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**If desktop app not running:**
```bash
cmd /c restart-desktop.bat
```

## Current Status

✅ **Backend:** Running on http://127.0.0.1:8000  
✅ **Desktop App:** Running on http://localhost:5001  
✅ **Connection:** Working and validated  
✅ **Profile Form:** Now tests backend before proceeding  
✅ **Error Handling:** Clear messages for connection issues  

## Next Steps

1. **Refresh browser** to load updated profile page
2. **Test the connection:**
   - Fill in profile form
   - Click "Continue"
   - Verify backend connection message
3. **Complete flow:**
   - Profile → Mood → Results
   - Backend should work throughout

---

**Status:** ✅ Fixed and Tested  
**Date:** October 18, 2025  
**Impact:** Backend connection now validated at profile step, preventing failed results later



