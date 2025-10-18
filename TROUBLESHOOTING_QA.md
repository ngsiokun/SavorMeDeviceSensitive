# SavorMe Troubleshooting Q&A Guide

## 🎯 Purpose
This document contains solutions to common issues encountered during SavorMe development and deployment. Use this as the **first reference** when debugging problems.

**Cross-References**:
- `MASTER_FILE_ORGANIZATION.md` - Complete file inventory
- `AUTOMATED_APP_STARTUP_GUIDE.md` - Startup procedures
- `AUTO_DETECT_ARCHITECTURE.md` - Auto-detect system
- `API_SCHEMA_REFERENCE.md` - API formats

---

## 🚨 CRITICAL: Command Prompt Issues

### Q1: Getting "The token '&&' is not a valid statement separator" error?

**Problem**: Running batch scripts in PowerShell instead of Command Prompt.

**Error Example**:
```
At line:1 char:74
+ ... && ..\venv ...
+    ~~
The token '&&' is not a valid statement separator in this version.
```

**Solution**:
```cmd
# NEVER use PowerShell!
# ALWAYS use Command Prompt (cmd.exe)

# To open Command Prompt:
1. Press Windows + R
2. Type: cmd
3. Press Enter

# Or right-click Start → Command Prompt (NOT PowerShell)
```

**Why**: PowerShell has different syntax than Command Prompt. All SavorMe batch scripts are written for cmd.exe.

**Cross-Reference**: All startup scripts, MASTER_FILE_ORGANIZATION.md

---

## 🔌 Backend Connection Issues

### Q2: "Cannot connect to backend" or "500 Internal Server Error"?

**Problem**: Backend not running or frontend sending wrong data format.

**Solution 1 - Backend Not Running**:
```cmd
# Check if backend is running:
curl http://127.0.0.1:8000/api/v1/health

# If error, start backend:
start-backend-only.bat
```

**Solution 2 - Wrong Data Format**:
The backend expects nested JSON with specific structure:
```json
{
  "mood_blend": { ... },
  "user_profile": { ... },
  "nutrition_targets": { ... },
  "activity_level": "moderate"
}
```

Check `API_SCHEMA_REFERENCE.md` for complete format.

**Solution 3 - Check Backend Terminal**:
- Look at the backend terminal window
- Check for Python errors or tracebacks
- Common issue: Missing Pydantic model fields

**Files to Check**:
- `app/api/routes.py` - Backend endpoints
- `desktop_app/templates/desktop-results.html` - Frontend data transformation
- `demo_app/static/js/recipe_result.js` - Mobile data transformation

**Cross-Reference**: API_SCHEMA_REFERENCE.md, BACKEND_TROUBLESHOOTING_FOR_GEMINI.md

---

## 🖼️ Image Display Issues

### Q3: Recipe images not displaying or showing as broken?

**Problem**: Image URL issues or object-fit CSS problems.

**Solution 1 - Edamam S3 Images**:
```python
# In app/services/edamam_client.py
# Trust Edamam S3 URLs without HEAD request validation
if "edamam-product-images.s3.amazonaws.com" in image_url:
    return image_url  # Trust it
```

**Solution 2 - CSS Object-Fit**:
```css
/* Desktop: Use contain to show full image */
.desktop-recipe-image-large img {
    object-fit: contain;
    height: 450px;
}

/* Mobile: Use cover for better mobile display */
.recipe-image img {
    object-fit: cover;
}
```

**Solution 3 - Fallback Chain**:
1. Try Edamam image URL
2. Try Edamam images.LARGE
3. Fallback to web image search
4. Use placeholder

**Cross-Reference**: FOOD_IMAGE_SYSTEM_GUIDE.md, EDAMAM_IMAGE_BUG_FIX.md

---

## 🔢 Data Formatting Issues

### Q4: Ingredients showing "0.333333333 cup" instead of "0.33 cup"?

**Problem**: No decimal formatting in frontend.

**Solution**:
```javascript
// In desktop-results.html
ingredientText = ingredientText.replace(/(\d+)\.(\d{3,})/g, (match, whole, decimals) => {
    return `${whole}.${decimals.substring(0, 2)}`;
});
```

**Location**: `desktop_app/templates/desktop-results.html` lines ~355-358

**Cross-Reference**: desktop_app/README.md

---

### Q5: Cooking steps showing "PREPARATION:" or "COOKING TIPS:" as numbered steps?

**Problem**: Title steps not filtered out.

**Solution**:
```javascript
// Filter out title steps
const validSteps = (recipe.cooking_directions || []).filter(step => {
    const stepText = typeof step === 'string' ? step : (step.text || step.instruction || '');
    if (!stepText || stepText.trim().length === 0) return false;
    
    // Filter out all-caps titles
    const trimmedText = stepText.trim();
    if (/^[A-Z\s]+:?\s*$/.test(trimmedText)) return false;
    if (/^(PREPARATION|COOKING STEPS|COOKING TIPS|TIPS|NOTES):?\s*$/i.test(trimmedText)) return false;
    
    return true;
});
```

**Location**: `desktop_app/templates/desktop-results.html` lines ~374-385

---

### Q6: Step count shows "27 steps" but only 24 actual steps displayed?

**Problem**: Counting steps before filtering out empty/title steps.

**Solution**: Count after filtering:
```javascript
// Count AFTER filtering
const validSteps = (recipe.cooking_directions || []).filter(step => {
    // ... filtering logic ...
});
return validSteps.length;  // Use filtered count
```

**Location**: `desktop_app/templates/desktop-results.html` lines ~306-312

---

## 📱 Device Detection Issues

### Q7: Wrong version showing (desktop on mobile or vice versa)?

**Problem**: Device detection not working or router not running.

**Solution 1 - Check Router**:
```cmd
# Is router running?
curl http://localhost:8080/health

# Check device detection:
curl http://localhost:8080/api/device-info
```

**Solution 2 - Check User-Agent**:
```python
# In app_router.py
def is_mobile_device(user_agent):
    mobile_keywords = [
        'mobile', 'android', 'iphone', 'ipad', 'ipod',
        'blackberry', 'windows phone', 'webos', 'opera mini',
        'tablet'
    ]
    return any(keyword in user_agent.lower() for keyword in mobile_keywords)
```

**Solution 3 - Direct Access**:
If router isn't working, access directly:
- Desktop: http://localhost:5001
- Mobile: http://localhost:5000

**Cross-Reference**: AUTO_DETECT_ARCHITECTURE.md, app_router.py

---

## 🚀 Startup Issues

### Q8: "Port already in use" error?

**Problem**: Previous instance still running.

**Solution**:
```cmd
# Clean up all processes:
cleanup-processes.bat

# Or manually:
netstat -ano | findstr :8000
netstat -ano | findstr :5000
netstat -ano | findstr :5001
netstat -ano | findstr :8080

# Then kill the process:
taskkill /PID <process_id> /F
```

**Cross-Reference**: cleanup-processes.bat

---

### Q9: Virtual environment activation fails?

**Problem**: venv not created or wrong Python version.

**Solution**:
```cmd
# Recreate venv:
cd C:\Users\Samsung\savorme-cloud-run\SavorMeDeviceSensitive
python -m venv venv

# Or use py launcher:
py -3 -m venv venv

# Activate:
venv\Scripts\activate.bat

# Install dependencies:
pip install -r requirements.txt
```

---

### Q10: ".env file not found" error?

**Problem**: Environment variables missing.

**Solution**:
```cmd
# Create .env file with:
EDAMAM_APP_ID=your_edamam_app_id
EDAMAM_APP_KEY=your_edamam_app_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Or copy from parent directory:
copy ..\.env .env
```

**Location**: Project root directory

---

## 🎨 UI/Layout Issues

### Q11: Food picture too zoomed in or not fitting frame?

**Problem**: Wrong object-fit CSS value.

**Solution**:
```css
/* For desktop - show full image */
.desktop-recipe-image-large img {
    width: 100%;
    height: 100%;
    object-fit: cover;        /* Fills frame, may crop */
    object-position: center;
}

/* Or use contain to show entire image */
object-fit: contain;  /* Shows entire image, may have letterboxing */
```

**Location**: `desktop_app/static/css/desktop-results.css`

---

### Q12: Ingredients or cooking steps showing "[Object Object]"?

**Problem**: Not properly parsing object properties.

**Solution**:
```javascript
// Parse ingredient object
if (typeof ing === 'string') {
    ingredientText = ing;
} else if (ing && typeof ing === 'object') {
    const amount = ing.amount || ing.quantity || '';
    const name = ing.name || ing.text || ing.ingredient || '';
    ingredientText = amount ? `${amount} ${name}` : name;
}

// Parse step object
const stepText = typeof step === 'string' ? step : (step.text || step.instruction || '');
```

**Location**: `desktop_app/templates/desktop-results.html`

---

## 🔄 Data Flow Issues

### Q13: "Try Another Recipe" button not working?

**Problem**: Wrong sessionStorage key or API format.

**Solution**:
```javascript
// Use correct sessionStorage key
const storedData = sessionStorage.getItem('desktopRequestData');  // Not 'requestData'

// Transform to backend format
const backendData = transformToBackendFormat(requestData);

// Call through Flask proxy, not direct
const response = await fetch('/api/recipes/recommend', {  // Not backend URL directly
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(backendData)
});
```

**Note**: This feature was removed in v4.0.0 due to Edamam API returning same results.

---

### Q14: Profile form submits but doesn't connect to backend?

**Problem**: Form only saves to sessionStorage without API call.

**Solution**:
```javascript
// In desktop-profile.html
async function handleSubmit(e) {
    e.preventDefault();
    
    // Make actual API call
    const response = await fetch('/api/nutrition/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    });
    
    // Then save to sessionStorage and redirect
    sessionStorage.setItem('desktopProfileData', JSON.stringify(result));
    window.location.href = '/mood';
}
```

**Location**: `desktop_app/templates/desktop-profile.html`

---

## 📊 API Issues

### Q15: "No recipes found" or empty results?

**Problem**: Too restrictive search filters or unsupported ingredients.

**Solution 1 - Check Search Query**:
```python
# Backend logs show search params
print(f"Search params: {search_params}")
print(f"Edamam API response hits: {len(search_results.get('hits', []))}")
```

**Solution 2 - Loosen Restrictions**:
```python
# In app/services/edamam_client.py
# Remove or widen calorie/protein ranges if too restrictive
# Check cuisine_types are Edamam-compatible
# Use dynamic ingredient replacement for exotic ingredients
```

**Solution 3 - Check Edamam API**:
```cmd
# Test Edamam API directly
curl "https://api.edamam.com/api/recipes/v2?type=public&q=chicken&app_id=YOUR_ID&app_key=YOUR_KEY"
```

**Cross-Reference**: EDAMAM_API_INTEGRATION_GUIDE.md, EDAMAM_COMPATIBILITY_FIX.md

---

### Q16: Secondary nutrients showing as 0mg?

**Problem**: Nutrients not enhanced from raw Edamam data.

**Solution**:
```python
# In app/api/routes.py
# Extract full nutrients per serving
nutrients_raw = edamam_client.extract_full_nutrients_per_serving(recipe_data)

# Enhance recipe with secondary nutrients
recipe = edamam_client._enhance_recipe_nutrition(recipe, nutrients)
```

**Check**: Magnesium, Iron, Folate, Vitamin D, Zinc should show actual values

**Cross-Reference**: app/services/edamam_client.py lines 300-320

---

## 🛠️ Development/Debugging Issues

### Q17: How to debug which service has the error?

**Problem**: Multiple services running, unclear where error is.

**Solution - Use Separate Windows**:
```cmd
# Start with separate windows:
START-ALL-SEPARATE.bat

# This creates 4 windows:
# [8000] Backend - Check for Python errors
# [5000] Mobile - Check for frontend errors
# [5001] Desktop - Check for frontend errors
# [8080] Router - Check for routing errors

# Look at the appropriate window for your issue!
```

**Architecture**:
- Frontend issue? → Check frontend window (5000 or 5001)
- API issue? → Check backend window (8000)
- Wrong device version? → Check router window (8080)
- Data format issue? → Check both frontend + backend

**Cross-Reference**: AUTO_DETECT_ARCHITECTURE.md

---

### Q18: Changes not showing up after edit?

**Problem**: Browser cache or server not reloading.

**Solution 1 - Clear Browser Cache**:
```
Ctrl + Shift + R (hard refresh)
Or Ctrl + F5
```

**Solution 2 - Restart Service**:
```cmd
# Desktop only:
restart-desktop.bat

# All services:
cleanup-processes.bat
START.bat
```

**Solution 3 - Check File**:
- Verify file was actually saved
- Check you're editing the right file (desktop vs mobile)
- Check terminal for syntax errors

---

## 📝 Documentation Issues

### Q19: Can't find where a feature is documented?

**Solution - Check MASTER_FILE_ORGANIZATION.md FIRST**:
```
1. Open MASTER_FILE_ORGANIZATION.md
2. Search for your topic (Ctrl + F)
3. It will tell you which file to check
4. All files cross-reference each other
```

**Common Topics**:
- API formats → API_SCHEMA_REFERENCE.md
- Edamam API → EDAMAM_JSON_FORMAT.md, EDAMAM_API_INTEGRATION_GUIDE.md
- Auto-detect → AUTO_DETECT_ARCHITECTURE.md
- Desktop app → desktop_app/README.md
- Startup → AUTOMATED_APP_STARTUP_GUIDE.md

---

### Q20: Documentation seems outdated?

**Problem**: Documentation not updated for v4.0.0.

**Solution - Key Files Must Be Updated**:
```
✓ MASTER_FILE_ORGANIZATION.md (v4.0.0)
✓ AUTOMATED_APP_STARTUP_GUIDE.md (v4.0.0)
✓ AUTO_DETECT_ARCHITECTURE.md (NEW)
✓ desktop_app/README.md (NEW)
✓ TROUBLESHOOTING_QA.md (This file)

Check version number at top of each file!
```

---

## 🎯 Medical Disclaimer Issues

### Q21: Where are medical disclaimers displayed?

**Answer - 3 Locations**:
```
1. Landing Page (desktop-index.html)
   - Bottom of page, before footer
   - Comprehensive disclaimer section

2. Results Page (desktop-results.html)
   - After action buttons
   - Before "Try Different Mood" section

3. Nutrient Match Score Modal
   - Bottom of modal
   - After scientific evidence section
```

**All disclaimers state**:
- SavorMe is for healthy eating support
- NOT intended for medical purposes
- NOT a substitute for professional advice
- Consult healthcare providers for medical issues

---

## 🔐 Security/Privacy Issues

### Q22: Where are recipes saved when user clicks "Save Recipe"?

**Answer**: Browser's localStorage (client-side only)
```javascript
// In desktop-results.html
localStorage.setItem('savedRecipes', JSON.stringify(savedRecipes));

// Location: Browser's localStorage for http://localhost:5001
// NOT saved to backend database
// Persists until browser data is cleared
```

**To view saved recipes**:
```
1. Open browser DevTools (F12)
2. Go to Application tab
3. Expand Local Storage
4. Click http://localhost:5001
5. Look for 'savedRecipes' key
```

---

## 🎓 Learning/Onboarding Issues

### Q23: New developer joining - where to start?

**Recommended Reading Order**:
```
1. README.md - Project overview
2. MASTER_FILE_ORGANIZATION.md - File structure
3. AUTO_DETECT_ARCHITECTURE.md - How app works
4. AUTOMATED_APP_STARTUP_GUIDE.md - How to run it
5. desktop_app/README.md (if working on desktop)
6. This file (TROUBLESHOOTING_QA.md) - Common issues

Then explore:
- API_SCHEMA_REFERENCE.md - API formats
- EDAMAM_JSON_FORMAT.md - Edamam API
- CUSTOMIZATIONS_PERSISTENT.md - Design system
```

**First Steps**:
```cmd
1. Clone repo
2. Run: setup_new_clone.bat
3. Run: START.bat
4. Visit: http://localhost:8080
5. Test the app!
```

---

## 📊 Quick Reference

### Common Commands
```cmd
# Start everything (recommended)
START.bat

# Start with debugging
START-ALL-SEPARATE.bat

# Clean up processes
cleanup-processes.bat

# Restart desktop only
restart-desktop.bat

# Test backend health
curl http://127.0.0.1:8000/api/v1/health
```

### Common Ports
```
8080 - Router (auto-detect)
8000 - Backend API
5001 - Desktop Frontend
5000 - Mobile Frontend
```

### Common File Locations
```
Backend API: app/api/routes.py
Desktop Frontend: desktop_app/app.py
Mobile Frontend: demo_app/app.py
Device Router: app_router.py
API Schemas: API_SCHEMA_REFERENCE.md
```

---

## 🆘 Still Stuck?

### If None of These Solutions Work:

1. **Check MASTER_FILE_ORGANIZATION.md** - Find the relevant file
2. **Check specific documentation** - Each feature has its own doc
3. **Check terminal windows** - Look for Python/JavaScript errors
4. **Check browser console** - F12 → Console tab
5. **Restart everything** - `cleanup-processes.bat` then `START.bat`
6. **Check this file** - Search for your error message (Ctrl + F)

### Debugging Checklist:
- [ ] Using Command Prompt (not PowerShell)?
- [ ] Backend running? (curl http://127.0.0.1:8000/api/v1/health)
- [ ] Correct port? (8080 for auto-detect, 5001 for desktop, 5000 for mobile)
- [ ] .env file present with API keys?
- [ ] Virtual environment activated?
- [ ] Dependencies installed? (pip install -r requirements.txt)
- [ ] Browser cache cleared? (Ctrl + Shift + R)

---

**Version**: 4.0.0  
**Last Updated**: October 2025  
**Cross-Reference**: MASTER_FILE_ORGANIZATION.md  
**Maintainer**: SavorMe Development Team

---

## 📝 Adding New Q&A Entries

When you encounter a new issue and solve it:
1. Add it to this file
2. Update MASTER_FILE_ORGANIZATION.md to reference it
3. Cross-reference in relevant technical docs
4. Include file locations and code snippets
5. Keep solutions practical and tested

