# SavorMe Automated Startup Guide
## Professional AI Consultant - Complete System Implementation

### Overview
This document provides a complete, step-by-step guide for running the SavorMe application with automatic error detection, correction, and validation. The system now includes advanced recipe variety, nutrient target tracking, and comprehensive mood-based nutrition analysis.

### Latest Features (v2.0)
- **Recipe Variety System**: 3x more diverse recipes with intelligent rotation
- **Target Nutrient Values**: Shows exactly how mood needs are met with daily targets
- **Enhanced Nutrient Analysis**: Web-based lookup for comprehensive micronutrient data
- **Session-Based Rotation**: Avoids recipe repeats within 24 hours
- **Mood-Specific Targeting**: Personalized nutrient goals for each mood type
- **Visual Progress Indicators**: ✅🟡🔴 status for nutrient target achievement

---

## Phase 1: Environment Setup & Validation

### Step 1.1: Verify Python Environment
```bash
# Check Python installation
python --version
# Expected: Python 3.8+ (ideally 3.9+)

# If Python not found, try:
py --version
# or
python3 --version
```

### Step 1.2: Create/Verify Virtual Environment
```bash
# Navigate to project directory
cd C:\Users\HP\SavorMe\SavorMe-backend-1

# Create virtual environment (if not exists)
py -m venv venv
# or
python -m venv venv
# or
python3 -m venv venv

# Verify venv creation
dir venv\Scripts\python.exe
```

### Step 1.3: Activate Virtual Environment
```bash
# Windows Command Prompt
venv\Scripts\activate.bat

# Verify activation (should show (venv) in prompt)
echo %VIRTUAL_ENV%
```

### Step 1.4: Install Dependencies
```bash
# Install all requirements
pip install -r requirements.txt

# Verify critical packages
pip list | findstr "fastapi uvicorn flask requests python-dotenv"
```

---

## Phase 2: Configuration Setup

### Step 2.1: Environment File Setup
```bash
# Check if .env exists
if exist .env (
    echo .env file exists
) else (
    echo Creating .env template...
    echo # SavorMe Backend Environment Variables > .env
    echo # Copy this file and add your actual API keys >> .env
    echo. >> .env
    echo # Edamam Recipe API >> .env
    echo EDAMAM_APP_ID=your_edamam_app_id >> .env
    echo EDAMAM_APP_KEY=your_edamam_app_key >> .env
    echo. >> .env
    echo # OpenRouter AI API >> .env
    echo OPENROUTER_API_KEY=your_openrouter_api_key >> .env
    echo. >> .env
    echo # CORS Origins >> .env
    echo CORS_ORIGINS=http://localhost:5000,http://127.0.0.1:5000 >> .env
    echo [OK] .env template created
)
```

### Step 2.2: Verify File Structure
```bash
# Check critical files exist
if exist "app\main.py" (
    echo [OK] Backend main file exists
) else (
    echo [ERROR] Backend main file missing
    exit /b 1
)

if exist "demo_app\app.py" (
    echo [OK] Frontend main file exists
) else (
    echo [ERROR] Frontend main file missing
    exit /b 1
)

if exist "demo_app\templates\index.html" (
    echo [OK] Landing page template exists
) else (
    echo [ERROR] Landing page template missing
    exit /b 1
)

if exist "demo_app\templates\recipe_result.html" (
    echo [OK] Recipe result template exists
) else (
    echo [ERROR] Recipe result template missing
    exit /b 1
)

if exist "demo_app\static\js\recipe_result.js" (
    echo [OK] Recipe result JavaScript exists
) else (
    echo [ERROR] Recipe result JavaScript missing
    exit /b 1
)

if exist "app\services\recipe_rotation.py" (
    echo [OK] Recipe rotation service exists
) else (
    echo [ERROR] Recipe rotation service missing
    exit /b 1
)

if exist "app\services\nutrient_web_lookup.py" (
    echo [OK] Nutrient web lookup service exists
) else (
    echo [ERROR] Nutrient web lookup service missing
    exit /b 1
)
```

---

## Phase 3: Backend Startup & Validation

### Step 3.1: Start Backend Server
```bash
# Start backend with proper error handling
venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Expected output:
# INFO: Uvicorn running on http://127.0.0.1:8000
# INFO: Application startup complete.
```

### Step 3.2: Validate Backend Health
```bash
# Test backend health (in new terminal)
curl http://127.0.0.1:8000/api/v1/health

# Expected response:
# {"status": "healthy", "timestamp": "..."}
```

### Step 3.3: Test Backend API Endpoints
```bash
# Test main API endpoint
curl http://127.0.0.1:8000/docs

# Should return HTML documentation page
```

---

## Phase 4: Frontend Startup & Validation

### Step 4.1: Start Frontend Server (New Terminal)
```bash
# Navigate to demo_app directory
cd demo_app

# Activate virtual environment
..\venv\Scripts\activate.bat

# Start Flask frontend
python app.py

# Expected output:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

### Step 4.2: Validate Frontend Routes
```bash
# Test frontend health (in new terminal)
curl http://localhost:5000/

# Should return HTML landing page
```

---

## Phase 5: Integration Testing

### Step 5.1: Test Complete User Flow
1. **Landing Page**: Open http://localhost:5000
   - Verify mobile-first vertical layout
   - Check hero section with SavorMe branding
   - Verify 2x2 feature grid below hero
   - Test "Start Your Journey →" button

2. **Profile Page**: Click "Start Your Journey →"
   - Should navigate to /profile
   - Verify form fields (age, gender, height, weight, etc.)
   - Test form submission

3. **Mood Selection**: Complete profile and proceed
   - Should navigate to /mood-selection
   - Verify mood selection interface
   - Test mood selection and submission

4. **Recipe Results**: Submit mood selection
   - Should navigate to /recipe-result
   - Verify loading spinner appears
   - Check recipe data displays properly
   - Verify match score, rationale, nutrition sections
   - **NEW**: Test "Nutrient Match Score" button for detailed analysis
   - **NEW**: Verify target nutrient values with percentages
   - **NEW**: Check visual status indicators (✅🟡🔴)
   - **NEW**: Test "Another Recipe Suggestion" for variety
   - **NEW**: Verify recipe rotation (no repeats within 24 hours)

### Step 5.2: API Integration Validation
```bash
# Test backend-frontend communication
curl -X POST http://127.0.0.1:8000/api/v1/recipes/recommend \
  -H "Content-Type: application/json" \
  -d '{"mood_blend": {"moods": [{"mood": "stressed", "intensity": "medium"}]}, "user_profile": {"age": 32, "gender": "female", "height_cm": 165, "weight_kg": 60, "cuisine_preferences": ["Mediterranean"], "food_allergies": [], "dietary_preference": "none"}}'

# Should return recipe recommendation JSON with enhanced features:
# - Recipe variety rotation
# - Comprehensive nutrient data
# - Target nutrient values
# - Mood-specific nutritional targeting
```

### Step 5.3: Recipe Variety Testing
```bash
# Test multiple recipe requests to verify variety
# Run this command 3-5 times and verify different recipes are returned
for /L %i in (1,1,3) do curl -X POST http://127.0.0.1:8000/api/v1/recipes/recommend \
  -H "Content-Type: application/json" \
  -d '{"mood_blend": {"moods": [{"mood": "stressed", "intensity": "medium"}]}, "user_profile": {"age": 32, "gender": "female", "height_cm": 165, "weight_kg": 60}}'

# Expected: Different recipes with variety in protein sources, cuisines, cooking methods
```

---

## Phase 6: Error Handling & Recovery

### Step 6.1: Common Error Scenarios
1. **Backend Connection Failed**
   - Check if backend is running on port 8000
   - Verify virtual environment is activated
   - Check for port conflicts

2. **Frontend Template Errors**
   - Verify all HTML templates exist
   - Check template syntax and Jinja2 variables
   - Validate CSS and JS file paths

3. **API Key Issues**
   - Verify .env file has proper API keys
   - Test API endpoints with valid credentials
   - Check rate limiting and quotas

4. **Database/Session Issues**
   - Clear browser cache and cookies
   - Restart both frontend and backend
   - Check session storage in browser dev tools

5. **Recipe Variety Issues**
   - Check recipe rotation service is running
   - Verify session tracking is working
   - Test with different mood combinations

6. **Nutrient Data Issues**
   - Verify web lookup service is functional
   - Check Edamam API response includes totalNutrients
   - Test fallback nutrient analysis

### Step 6.2: Automatic Recovery Procedures
```bash
# Kill any existing processes
taskkill /f /im python.exe 2>nul
taskkill /f /im uvicorn.exe 2>nul

# Restart backend
venv\Scripts\activate.bat
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# In new terminal, restart frontend
cd demo_app
..\venv\Scripts\activate.bat
python app.py
```

---

## Phase 7: Performance & Optimization

### Step 7.1: Load Testing
```bash
# Test concurrent requests
for /L %i in (1,1,10) do start curl http://localhost:5000
```

### Step 7.2: Memory Usage Check
```bash
# Monitor Python processes
tasklist | findstr python
```

---

## Phase 8: Deployment Validation

### Step 8.1: Production Readiness Check
- [ ] All dependencies installed
- [ ] Environment variables configured
- [ ] Error handling implemented
- [ ] User flow tested end-to-end
- [ ] API endpoints responding correctly
- [ ] Frontend-backend communication working
- [ ] Mobile-first design verified
- [ ] Loading states and error messages working
- [ ] **NEW**: Recipe variety system working (no repeats)
- [ ] **NEW**: Target nutrient values displaying correctly
- [ ] **NEW**: Nutrient analysis with visual indicators
- [ ] **NEW**: Recipe rotation service functional
- [ ] **NEW**: Web-based nutrient lookup working
- [ ] **NEW**: Mood-specific nutrient targeting accurate

### Step 8.2: Final Validation Commands
```bash
# Complete system check
echo "=== BACKEND HEALTH ==="
curl http://127.0.0.1:8000/api/v1/health

echo "=== FRONTEND HEALTH ==="
curl http://localhost:5000/

echo "=== API DOCUMENTATION ==="
curl http://127.0.0.1:8000/docs

echo "=== SYSTEM STATUS ==="
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5000
echo API Docs: http://127.0.0.1:8000/docs
```

---

## Emergency Recovery Procedures

### If Everything Fails:
1. **Complete Reset**
   ```bash
   # Delete virtual environment
   rmdir /s /q venv
   
   # Recreate from scratch
   py -m venv venv
   venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

2. **File System Check**
   ```bash
   # Verify all critical files
   dir app\main.py
   dir demo_app\app.py
   dir demo_app\templates\*.html
   dir requirements.txt
   dir .env
   ```

3. **Network Troubleshooting**
   ```bash
   # Check port availability
   netstat -an | findstr ":8000"
   netstat -an | findstr ":5000"
   ```

---

## Success Criteria

The application is considered successfully deployed when:
- ✅ Backend starts without errors on port 8000
- ✅ Frontend starts without errors on port 5000
- ✅ Landing page displays mobile-first vertical layout
- ✅ Complete user flow works: Landing → Profile → Mood → Results
- ✅ API endpoints respond correctly
- ✅ Error handling provides meaningful feedback
- ✅ All templates render without errors
- ✅ Session storage works correctly
- ✅ Loading states display properly
- ✅ **NEW**: Recipe variety system provides diverse recommendations
- ✅ **NEW**: Target nutrient values show progress toward daily goals
- ✅ **NEW**: Visual indicators (✅🟡🔴) display nutrient target achievement
- ✅ **NEW**: Recipe rotation prevents repeats within 24 hours
- ✅ **NEW**: Enhanced nutrient analysis includes micronutrients
- ✅ **NEW**: Mood-specific nutritional targeting is accurate
- ✅ **NEW**: "Another Recipe Suggestion" button works correctly

---

## Enhanced Features Guide (v2.0)

### Recipe Variety System
The system now provides 3x more recipe variety through:
- **60+ keyword combinations** per mood (vs 20 previously)
- **Intelligent rotation** that avoids repeats within 24 hours
- **Variety boosting** that prioritizes different protein sources, cuisines, and cooking methods
- **Session tracking** to ensure diverse recommendations

### Target Nutrient Values
Users now see exactly how their mood needs are met:
- **Daily targets** for all mood-supporting nutrients
- **Percentage achievement** (e.g., "45mg of 120mg target (38%)")
- **Visual indicators**: ✅ (50%+), 🟡 (25-49%), 🔴 (<25%)
- **Mood-specific targeting** with personalized nutrient goals

### Enhanced Nutrient Analysis
- **Web-based lookup** for comprehensive micronutrient data
- **Ingredient analysis** that recognizes nutrient patterns
- **Fallback system** with estimated benefits when detailed data unavailable
- **Mood-specific explanations** for why each nutrient matters

### Testing the Enhanced Features
1. **Recipe Variety**: Get 3-5 consecutive recommendations and verify different recipes
2. **Nutrient Targets**: Click "Nutrient Match Score" and verify target values display
3. **Visual Indicators**: Check that ✅🟡🔴 icons appear based on target achievement
4. **Rotation**: Verify no recipe repeats within the same session
5. **Mood Targeting**: Test different moods and verify appropriate nutrient focus

---

*This guide ensures professional-grade deployment with comprehensive error handling, validation, and enhanced user experience features at every step.*
