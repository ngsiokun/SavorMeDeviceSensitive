# SavorMe Automated Startup Guide
## Professional AI Consultant - Complete System Implementation

### Overview
This document provides a complete, step-by-step guide for running the SavorMe application with automatic error detection, correction, and validation. The system now includes advanced recipe variety, nutrient target tracking, and comprehensive mood-based nutrition analysis.

### 📋 **Critical Documentation Reference**
**IMPORTANT**: Before starting the application, ensure you have reviewed the essential documentation:

**`MASTER_FILE_ORGANIZATION.md`** - **SINGLE SOURCE OF TRUTH** for all project files and configuration
   - Complete file inventory and organization guide
   - Project status, configuration, and startup commands
   - Shows where to find each file and its purpose
   - Contains all essential documentation references
   - Prevents forgotten files during updates
   - Essential for understanding project structure
   - **This file contains all the information from other documentation files**

### ⚠️ **CRITICAL: Use Command Prompt Only**
**ALL COMMANDS IN THIS GUIDE MUST BE RUN VIA COMMAND PROMPT (cmd.exe) AND NEVER USE POWERSHELL.** PowerShell may cause compatibility issues with the batch scripts and environment setup. Always open Command Prompt (cmd.exe) before running any commands from this guide.

### Latest Features (v3.1.2)
- **✅ Image Display Fix**: Fixed critical bug where Edamam recipe images were incorrectly filtered out due to "SignedHeaders" in AWS URLs being matched by the "header" pattern
- **Enhanced Image Validation**: Updated to only check URL path (before query parameters) for generic image patterns, preventing false positives
- **Expanded Generic Patterns**: Added more decorative image indicators (sprite, avatar, social, share, footer, bg, background) for better filtering
- **Robust Error Handling**: Added try-except block for safer URL parsing in image validation
- **✅ Secondary Nutrients Fix (v3.1.1)**: Fixed issue where secondary nutrients (magnesium, iron, B12, folate, vitamin D, omega-3, zinc, vitamin C) were showing as 0mg/0g instead of actual calculated values
- **Enhanced Nutrition Model**: Updated NutritionInfo model to include all secondary nutrients for mood-based scoring
- **Nutrient Enhancement Pipeline**: Added _enhance_recipe_nutrition() method to properly populate secondary nutrients from canonical data
- **Evidence-Based Mood Mapping**: Updated with latest scientific research and meta-analyses
- **EPA-Focused Omega-3**: Targets EPA ≥ 60% of EPA+DHA for optimal mood support
- **Anti-Inflammatory Mediterranean Pattern**: Enhanced with neuroprotective herbs/spices
- **Iron-Supportive Implementation**: Heme/non-heme sources with vitamin C pairing
- **Scientific Claim Accuracy**: Medically safe wording based on evidence strength
- **Enhanced Cooking Directions**: Professional chef-level instructions with comprehensive details
- **Recipe Variety System**: 3x more diverse recipes with intelligent rotation
- **Target Nutrient Values**: Shows exactly how mood needs are met with daily targets
- **Enhanced Nutrient Analysis**: Web-based lookup for comprehensive micronutrient data
- **Session-Based Rotation**: Avoids recipe repeats within 24 hours
- **Mood-Specific Targeting**: Personalized nutrient goals for each mood type
- **Recipe Match Score Transparency**: Weighted scoring system with evidence-based nutrient weights
- **Data Source Transparency**: Clear documentation of Edamam API + built-in nutrient database
- **Visual Progress Indicators**: ✅🟡🔴 status for nutrient target achievement

---

## 🚀 **Startup Workflow Integration**

### **How Startup Scripts Work with Documentation**

When you run `start.bat`, the system follows this integrated workflow:

**All documentation is now consolidated into `MASTER_FILE_ORGANIZATION.md`** - the single source of truth that contains:
- Complete file inventory and organization
- Project status, configuration, and startup commands
- Design system and customization references
- Evidence-based moods system documentation
- Technical workflow and user journey information
- System architecture and data flow details

**Automated Startup Process** → Follows this guide (`AUTOMATED_APP_STARTUP_GUIDE.md`)
   - Environment setup and validation
   - Backend and frontend startup
   - Error detection and correction
   - References `MASTER_FILE_ORGANIZATION.md` for all file information

### **Quick Start Commands**

#### **Option 1: Simple Startup (Recommended)**
```cmd
cd C:\Users\HP\SavorMe\SavorMe-backend
start.bat
```
*This script automatically references all documentation files and follows the complete workflow.*

#### **Option 2: Professional Startup (Advanced)**
```cmd
cd C:\Users\HP\SavorMe\SavorMe-backend
savorme_professional_startup.bat
```
*This script includes comprehensive diagnostics and follows the complete workflow with detailed logging.*

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
cd C:\Users\HP\SavorMe\SavorMe-backend

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

### ⚠️ **CRITICAL: .env File Setup (Required for API Keys)**

**IMPORTANT**: The `.env` file is **NOT** included in GitHub repositories for security reasons. You must create this file manually after cloning from GitHub.

#### **Step 2.1: Locate and Create .env File**

**File Location**: `C:\Users\HP\SavorMe\SavorMe-backend\.env`

```bash
# Navigate to project root directory
cd C:\Users\HP\SavorMe\SavorMe-backend

# Check if .env exists
if exist .env (
    echo [OK] .env file found
    echo Checking .env file contents...
    type .env
) else (
    echo [WARNING] .env file NOT FOUND
    echo This is normal when cloning from GitHub
    echo Creating .env template...
    
    # Create .env file with template
    echo # SavorMe Backend Environment Variables > .env
    echo # IMPORTANT: Replace the placeholder values with your actual API keys >> .env
    echo # Get your API keys from: >> .env
    echo # - Edamam: https://developer.edamam.com/ >> .env
    echo # - OpenRouter: https://openrouter.ai/ >> .env
    echo. >> .env
    echo # Edamam Recipe API (Required for recipe data) >> .env
    echo EDAMAM_APP_ID=your_edamam_app_id_here >> .env
    echo EDAMAM_APP_KEY=your_edamam_app_key_here >> .env
    echo. >> .env
    echo # OpenRouter AI API (Required for cooking directions) >> .env
    echo OPENROUTER_API_KEY=your_openrouter_api_key_here >> .env
    echo. >> .env
    echo # CORS Origins (Frontend access) >> .env
    echo CORS_ORIGINS=http://localhost:5000,http://127.0.0.1:5000 >> .env
    
    echo [SUCCESS] .env template created
    echo.
    echo ⚠️  CRITICAL: You must now edit .env file and add your actual API keys
    echo.
    echo To edit the .env file:
    echo 1. Open .env in any text editor (Notepad, VS Code, etc.)
    echo 2. Replace "your_edamam_app_id_here" with your actual Edamam App ID
    echo 3. Replace "your_edamam_app_key_here" with your actual Edamam App Key
    echo 4. Replace "your_openrouter_api_key_here" with your actual OpenRouter API Key
    echo 5. Save the file
    echo.
    echo Press any key to continue after you have added your API keys...
    pause
)
```

#### **Step 2.2: Verify .env File Contents**

```bash
# Verify .env file has required variables
echo Checking .env file configuration...

# Check for Edamam credentials
findstr "EDAMAM_APP_ID=" .env | findstr /v "your_edamam_app_id_here" >nul
if %errorlevel% equ 0 (
    echo [OK] EDAMAM_APP_ID is configured
) else (
    echo [ERROR] EDAMAM_APP_ID not properly configured
    echo Please edit .env file and add your actual Edamam App ID
    pause
    exit /b 1
)

findstr "EDAMAM_APP_KEY=" .env | findstr /v "your_edamam_app_key_here" >nul
if %errorlevel% equ 0 (
    echo [OK] EDAMAM_APP_KEY is configured
) else (
    echo [ERROR] EDAMAM_APP_KEY not properly configured
    echo Please edit .env file and add your actual Edamam App Key
    pause
    exit /b 1
)

# Check for OpenRouter credentials
findstr "OPENROUTER_API_KEY=" .env | findstr /v "your_openrouter_api_key_here" >nul
if %errorlevel% equ 0 (
    echo [OK] OPENROUTER_API_KEY is configured
) else (
    echo [ERROR] OPENROUTER_API_KEY not properly configured
    echo Please edit .env file and add your actual OpenRouter API Key
    pause
    exit /b 1
)

echo [SUCCESS] All API keys are properly configured
```

#### **Step 2.3: API Key Setup Instructions**

**If you need to get API keys:**

1. **Edamam Recipe API** (Required for recipe data):
   - Go to: https://developer.edamam.com/
   - Sign up for a free account
   - Create a new application
   - Copy your App ID and App Key

2. **OpenRouter AI API** (Required for cooking directions):
   - Go to: https://openrouter.ai/
   - Sign up for an account
   - Get your API key from the dashboard

3. **Edit .env file**:
   - Open `C:\Users\HP\SavorMe\SavorMe-backend\.env` in any text editor
   - Replace the placeholder values with your actual API keys
   - Save the file

#### **Step 2.4: Test API Connectivity**

```bash
# Test if API keys work (optional but recommended)
echo Testing API connectivity...
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

edamam_id = os.getenv('EDAMAM_APP_ID')
edamam_key = os.getenv('EDAMAM_APP_KEY')
openrouter_key = os.getenv('OPENROUTER_API_KEY')

if edamam_id and edamam_id != 'your_edamam_app_id_here':
    print('[OK] Edamam App ID is configured')
else:
    print('[WARNING] Edamam App ID not configured')

if edamam_key and edamam_key != 'your_edamam_app_key_here':
    print('[OK] Edamam App Key is configured')
else:
    print('[WARNING] Edamam App Key not configured')

if openrouter_key and openrouter_key != 'your_openrouter_api_key_here':
    print('[OK] OpenRouter API Key is configured')
else:
    print('[WARNING] OpenRouter API Key not configured')
"
```

### Step 2.2: Verify File Structure & Customizations
```bash
# Check critical files exist (refer to CUSTOMIZATIONS_PERSISTENT.md for complete list)
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

# Landing Page Customizations (see CUSTOMIZATIONS_PERSISTENT.md Section 1)
if exist "demo_app\templates\index.html" (
    echo [OK] Landing page template exists
) else (
    echo [ERROR] Landing page template missing - see CUSTOMIZATIONS_PERSISTENT.md
    exit /b 1
)

if exist "demo_app\static\css\landing.css" (
    echo [OK] Landing page CSS exists
) else (
    echo [ERROR] Landing page CSS missing - see CUSTOMIZATIONS_PERSISTENT.md
    exit /b 1
)

# Recipe Results Page Customizations (see CUSTOMIZATIONS_PERSISTENT.md Section 2)
if exist "demo_app\templates\recipe_result.html" (
    echo [OK] Recipe result template exists
) else (
    echo [ERROR] Recipe result template missing - see CUSTOMIZATIONS_PERSISTENT.md
    exit /b 1
)

if exist "demo_app\static\js\recipe_result.js" (
    echo [OK] Recipe result JavaScript exists
) else (
    echo [ERROR] Recipe result JavaScript missing - see CUSTOMIZATIONS_PERSISTENT.md
    exit /b 1
)

if exist "demo_app\static\css\recipe_results.css" (
    echo [OK] Recipe results CSS exists
) else (
    echo [ERROR] Recipe results CSS missing - see CUSTOMIZATIONS_PERSISTENT.md
    exit /b 1
)

# Backend Services
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

# Backend Cooking Directions Fix (see CUSTOMIZATIONS_PERSISTENT.md Section 4)
if exist "app\services\openrouter_client.py" (
    echo [OK] OpenRouter client with cooking directions exists
) else (
    echo [ERROR] OpenRouter client missing - see CUSTOMIZATIONS_PERSISTENT.md
    exit /b 1
)

# Professional Startup System (see CUSTOMIZATIONS_PERSISTENT.md Section 5)
if exist "savorme_professional_startup.bat" (
    echo [OK] Professional startup script exists
) else (
    echo [ERROR] Professional startup script missing - see CUSTOMIZATIONS_PERSISTENT.md
    exit /b 1
)

if exist "CUSTOMIZATIONS_PERSISTENT.md" (
    echo [OK] Customizations persistent file exists
) else (
    echo [ERROR] CUSTOMIZATIONS_PERSISTENT.md missing - CRITICAL for proper page rebuilding
    exit /b 1
)
```

---

## Phase 2.5: Customization Verification (CRITICAL)

### Step 2.5.1: Review Customizations Persistent File
```bash
# Open and review the customizations file
type CUSTOMIZATIONS_PERSISTENT.md

# This file contains:
# - Complete design system specifications
# - All modified file locations and changes
# - Essential code snippets for rebuilding pages
# - Verification checklists for each component
# - Color palette, typography, and layout principles
```

### Step 2.5.2: Verify Design System Elements
Based on `CUSTOMIZATIONS_PERSISTENT.md`, verify these critical design elements:

#### **Color Palette Verification**
- **Primary**: #0F766E (Dark Teal)
- **Secondary**: #065F46 (Dark Green)  
- **Accent**: #10B981 (Green)
- **Background**: #F0FDF4 (Light Green)

#### **Typography Verification**
- **Font Family**: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
- **Hero Title**: 36px, font-weight 800
- **Subtitle**: 16px, font-weight 600
- **Body**: 14px, line-height 1.5

#### **Layout Principles Verification**
- **Mobile-First**: All designs start with mobile (414px width)
- **Vertical Stacking**: Hero section above feature grid
- **Glassmorphic Effects**: Semi-transparent cards with blur
- **Consistent Spacing**: 20px margins, 16px gaps

### Step 2.5.3: Critical JavaScript Functions Check
Verify these essential functions exist in `demo_app/static/js/recipe_result.js`:
- `generateDetailedRationale()` - Enhanced nutritional analysis
- `showNutrientAnalysis()` - Modal display with comprehensive data
- `generateNewRecommendation()` - Seamless recipe exploration
- `generatePage()` - Dynamic page generation
- `addEventListeners()` - Button functionality

### Step 2.5.4: Enhanced Cooking Directions Verification
Verify the cooking directions system provides comprehensive instructions (see `CUSTOMIZATIONS_PERSISTENT.md` Section 4):

#### **AI-Generated Directions (When API Available):**
- **Token Limit**: 1200 tokens (increased from 500) for detailed instructions
- **Professional Prompt**: Requests preparation, cooking steps, finishing, and tips
- **Comprehensive Format**: Sectioned instructions with specific temperatures and times
- **Beginner-Friendly**: Clear enough for someone new to cooking

#### **Fallback Directions (When API Unavailable):**
- **Sectioned Format**: PREPARATION, COOKING STEPS, FINISHING, and TIPS sections
- **Ingredient-Specific Methods**: Different approaches for meat, fish, vegetables, pasta
- **Specific Temperatures**: 375°F for meat, 400°F for fish, 425°F for vegetables
- **Professional Techniques**: Resting meat, reserving pasta water, proper browning
- **Pro Tips Included**: Common mistakes to avoid, cooking techniques, equipment guidance

### Step 2.5.5: Evidence-Based Nutrient Targeting Verification
Ensure the system tracks these nutrients with updated evidence-based targets (see `CUSTOMIZATIONS_PERSISTENT.md` Section 3):

#### **Primary Mood-Supporting Nutrients:**
- **Magnesium (120mg target)** - Low-Moderate evidence for stress response
- **EPA-Rich Omega-3 (≥60% EPA of EPA+DHA)** - Small-to-modest effects in meta-analyses
- **Iron (6mg per meal)** - Moderate-Strong evidence for fatigue when deficient
- **B-Vitamins (Folate, B6, B12)** - Correlations with mood, supportive building blocks
- **Fiber (8-10g per meal)** - Gut-brain axis health and blood sugar stability

#### **Secondary Supportive Nutrients:**
- **Vitamin D (400 IU per meal)** - Low evidence, associations with mood
- **Zinc (3mg per meal)** - Essential mineral for brain and nervous system
- **Selenium** - Emerging evidence for cognitive/emotional regulation
- **Vitamin C (30mg per meal)** - Enhances non-heme iron absorption

#### **Evidence Level Verification:**
- **Strong Evidence**: Iron deficiency → fatigue (clinical guidelines)
- **Moderate Evidence**: Mediterranean diet → mood improvement (observational + some RCTs)
- **Low-Moderate Evidence**: Omega-3 EPA, magnesium, B-vitamins (mixed RCT results)

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

### Step 5.1: Test Complete User Flow (Refer to CUSTOMIZATIONS_PERSISTENT.md)
1. **Landing Page**: Open http://localhost:5000
   - Verify mobile-first vertical layout (see CUSTOMIZATIONS_PERSISTENT.md Section 1)
   - Check hero section with SavorMe branding
   - Verify 2x2 feature grid below hero
   - Test "Start Your Journey →" button
   - **CRITICAL**: Verify dark teal gradient background (#0F766E to #065F46)
   - **CRITICAL**: Check glassmorphic card effects with backdrop blur

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
   - **CRITICAL**: Test "Nutrient Match Score" button for detailed analysis (see CUSTOMIZATIONS_PERSISTENT.md Section 2)
   - **CRITICAL**: Verify target nutrient values with percentages
   - **CRITICAL**: Check visual status indicators (✅🟡🔴)
   - **CRITICAL**: Test "Another Recipe Suggestion" for variety (replaces "Got it!" button)
   - **CRITICAL**: Verify recipe rotation (no repeats within 24 hours)
   - **CRITICAL**: Verify mobile smartphone design with status bar
   - **CRITICAL**: Check evidence-based nutrient analysis with updated scientific targets
   - **CRITICAL**: Verify EPA-focused omega-3 recommendations (≥60% EPA of EPA+DHA)
   - **CRITICAL**: Test iron-supportive recipes with heme/non-heme + vitamin C pairing
   - **CRITICAL**: Verify Mediterranean pattern with anti-inflammatory herbs/spices
   - **CRITICAL**: Check medically safe claim wording throughout
   - **CRITICAL**: Test scientific evidence section with updated research backing
   - **CRITICAL**: Verify Recipe Match Score Transparency with weighted scoring breakdown
   - **CRITICAL**: Check data source display (Edamam API + built-in database)
   - **CRITICAL**: Verify nutrient contribution display with individual scores and weights

### Step 5.2: API Integration Validation
```bash
# Test backend-frontend communication
curl -X POST http://127.0.0.1:8000/api/v1/recipes/recommend \
  -H "Content-Type: application/json" \
  -d '{"mood_blend": {"moods": [{"mood": "stressed", "intensity": "medium"}]}, "user_profile": {"age": 32, "gender": "female", "height_cm": 165, "weight_kg": 60, "cuisine_preferences": ["Mediterranean"], "food_allergies": [], "dietary_preference": "none"}}'

# Should return recipe recommendation JSON with enhanced features:
# - Evidence-based mood mapping (v2.2)
# - EPA-focused omega-3 targeting (≥60% EPA of EPA+DHA)
# - Iron-supportive recipes with heme/non-heme + vitamin C
# - Mediterranean pattern with anti-inflammatory herbs/spices
# - Medically safe claim wording
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
# Also verify evidence-based nutrient targeting:
# - EPA-rich omega-3 sources (salmon, mackerel, sardines)
# - Iron-supportive combinations (heme + non-heme + vitamin C)
# - Mediterranean pattern with anti-inflammatory herbs/spices
# - Medically safe claim wording throughout
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
   - Verify EPA-focused omega-3 targeting (≥60% EPA of EPA+DHA)
   - Check iron-supportive combinations with vitamin C pairing
   - Validate Mediterranean pattern with anti-inflammatory herbs/spices

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
- [ ] **NEW**: Evidence-based mood mapping (v2.2) working correctly
- [ ] **NEW**: EPA-focused omega-3 targeting (≥60% EPA of EPA+DHA)
- [ ] **NEW**: Iron-supportive recipes with heme/non-heme + vitamin C
- [ ] **NEW**: Mediterranean pattern with anti-inflammatory herbs/spices
- [ ] **NEW**: Medically safe claim wording throughout
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

## Success Criteria (Based on CUSTOMIZATIONS_PERSISTENT.md)

The application is considered successfully deployed when:

### **Core Functionality**
- ✅ Backend starts without errors on port 8000
- ✅ Frontend starts without errors on port 5000
- ✅ Complete user flow works: Landing → Profile → Mood → Results
- ✅ API endpoints respond correctly
- ✅ Error handling provides meaningful feedback
- ✅ All templates render without errors
- ✅ Session storage works correctly
- ✅ Loading states display properly

### **Landing Page Customizations (CUSTOMIZATIONS_PERSISTENT.md Section 1)**
- ✅ Mobile-first vertical layout (hero section on top, 2x2 feature grid below)
- ✅ Dark teal gradient background (#0F766E to #065F46)
- ✅ Glassmorphic cards with backdrop blur effects
- ✅ Proper responsive design for all screen sizes
- ✅ Consistent typography and spacing
- ✅ "Start Your Journey →" button works correctly

### **Recipe Results Page Customizations (CUSTOMIZATIONS_PERSISTENT.md Section 2)**
- ✅ Mobile-first smartphone design with status bar
- ✅ Pure JavaScript-driven page generation (no HTML templates needed)
- ✅ Comprehensive nutrient analysis modal with detailed breakdown
- ✅ Enhanced "Why This Recipe?" section with specific nutritional data
- ✅ "Another Recipe Suggestion" button (replaces "Got it!" button)
- ✅ Scientific evidence section with research backing
- ✅ 8 key mood-supporting nutrients analysis
- ✅ Proper loading states and error handling
- ✅ Consistent color scheme and typography

### **Comprehensive Nutrient Analysis System (CUSTOMIZATIONS_PERSISTENT.md Section 3)**
- ✅ Enhanced "Why This Recipe?" section with detailed nutritional rationale
- ✅ Comprehensive nutrient highlights with 8 key mood-supporting nutrients
- ✅ Scientific evidence section with research backing
- ✅ "Another Recipe Suggestion" button for seamless recipe exploration
- ✅ Detailed nutritional breakdown with percentages and targets
- ✅ Mood-specific nutrient benefits explanation

### **Backend Cooking Directions Fix (CUSTOMIZATIONS_PERSISTENT.md Section 4)**
- ✅ Fallback cooking directions generation
- ✅ Intelligent ingredient analysis for cooking methods
- ✅ Proper error handling when API keys are missing
- ✅ Step-by-step cooking instructions instead of just links

### **Enhanced Features (v2.2)**
- ✅ Evidence-based mood mapping with latest scientific research
- ✅ EPA-focused omega-3 targeting (≥60% EPA of EPA+DHA)
- ✅ Iron-supportive recipes with heme/non-heme + vitamin C pairing
- ✅ Mediterranean pattern with anti-inflammatory herbs/spices
- ✅ Medically safe claim wording based on evidence strength
- ✅ Recipe variety system provides diverse recommendations
- ✅ Target nutrient values show progress toward daily goals
- ✅ Visual indicators (✅🟡🔴) display nutrient target achievement
- ✅ Recipe rotation prevents repeats within 24 hours
- ✅ Enhanced nutrient analysis includes micronutrients
- ✅ Mood-specific nutritional targeting is accurate
- ✅ "Another Recipe Suggestion" button works correctly

### **Design System Verification (CUSTOMIZATIONS_PERSISTENT.md Design System)**
- ✅ Color palette: Primary #0F766E, Secondary #065F46, Accent #10B981, Background #F0FDF4
- ✅ Typography: -apple-system font family, proper sizing and weights
- ✅ Layout principles: Mobile-first, vertical stacking, glassmorphic effects
- ✅ Consistent spacing: 20px margins, 16px gaps

---

## Enhanced Features Guide (v2.2)

### Evidence-Based Mood Mapping
The system now uses the latest scientific research:
- **EPA-focused Omega-3**: Targets EPA ≥ 60% of EPA+DHA based on meta-analyses
- **Iron-Supportive Implementation**: Heme/non-heme sources with vitamin C pairing
- **Mediterranean Anti-Inflammatory Pattern**: Enhanced with neuroprotective herbs/spices
- **Medically Safe Claims**: Evidence-based wording that's clinically appropriate
- **Evidence Level Transparency**: Honest assessment of research strength

### Recipe Variety System
The system provides 3x more recipe variety through:
- **60+ keyword combinations** per mood (vs 20 previously)
- **Intelligent rotation** that avoids repeats within 24 hours
- **Variety boosting** that prioritizes different protein sources, cuisines, and cooking methods
- **Session tracking** to ensure diverse recommendations

### Target Nutrient Values
Users now see exactly how their mood needs are met:
- **Evidence-based targets** for all mood-supporting nutrients
- **Percentage achievement** (e.g., "45mg of 120mg target (38%)")
- **Visual indicators**: ✅ (50%+), 🟡 (25-49%), 🔴 (<25%)
- **Mood-specific targeting** with personalized nutrient goals

### Enhanced Nutrient Analysis
- **Web-based lookup** for comprehensive micronutrient data
- **Ingredient analysis** that recognizes nutrient patterns
- **Fallback system** with estimated benefits when detailed data unavailable
- **Mood-specific explanations** for why each nutrient matters
- **Scientific evidence backing** with appropriate disclaimers

### Testing the Enhanced Features
1. **Evidence-Based Targeting**: Verify EPA-rich omega-3 sources and iron-supportive combinations
2. **Recipe Variety**: Get 3-5 consecutive recommendations and verify different recipes
3. **Nutrient Targets**: Click "Nutrient Match Score" and verify target values display
4. **Visual Indicators**: Check that ✅🟡🔴 icons appear based on target achievement
5. **Rotation**: Verify no recipe repeats within the same session
6. **Mood Targeting**: Test different moods and verify appropriate nutrient focus
7. **Mediterranean Pattern**: Check for anti-inflammatory herbs/spices in recommendations
8. **Safe Claims**: Verify medically appropriate wording throughout

---

## 🔧 **Critical Maintenance Notes**

### **Before Any Deployment or Clone:**
1. **ALWAYS** review `CUSTOMIZATIONS_PERSISTENT.md` first
2. **VERIFY** all customized files are present and contain the correct code
3. **TEST** the design system elements (colors, typography, layout)
4. **VALIDATE** all JavaScript functions are working correctly
5. **CONFIRM** evidence-based nutrient targeting is working (v2.2)
6. **VERIFY** EPA-focused omega-3 targeting (≥60% EPA of EPA+DHA)
7. **CHECK** iron-supportive recipes with heme/non-heme + vitamin C
8. **VALIDATE** Mediterranean pattern with anti-inflammatory herbs/spices
9. **ENSURE** medically safe claim wording throughout

### **If Pages Don't Look Right:**
1. Check `CUSTOMIZATIONS_PERSISTENT.md` for the exact specifications
2. Verify all CSS files contain the correct styling
3. Ensure JavaScript functions match the code snippets in the persistent file
4. Test the design system elements against the documented specifications
5. Verify evidence-based nutrient targeting is working correctly
6. Check EPA-focused omega-3 recommendations are appearing
7. Ensure iron-supportive combinations with vitamin C are being suggested
8. Validate Mediterranean pattern with anti-inflammatory herbs/spices

### **For New Developers:**
- `CUSTOMIZATIONS_PERSISTENT.md` is your complete reference guide
- It contains all the code snippets needed to rebuild pages correctly
- Follow the verification checklists to ensure proper implementation
- The design system ensures consistent quality across all deployments
- **Evidence-based approach**: All recommendations are backed by scientific research
- **EPA-focused omega-3**: Prioritize EPA ≥ 60% of EPA+DHA for mood support
- **Iron-supportive recipes**: Combine heme/non-heme sources with vitamin C
- **Mediterranean pattern**: Use anti-inflammatory herbs/spices for neuroprotection
- **Medically safe claims**: All wording is clinically appropriate and evidence-based

---

*This guide ensures professional-grade deployment with comprehensive error handling, validation, and enhanced user experience features at every step. The CUSTOMIZATIONS_PERSISTENT.md file is your blueprint for maintaining consistent quality and branding across all SavorMe deployments.*
