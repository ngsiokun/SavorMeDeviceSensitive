# 🍽️ SavorMe Application Workflow - Complete System Flow

## 📋 Master File References
- **Primary Reference**: `SAVORME_MASTER_OVERVIEW.md` (Lines 1-252)
- **File Organization**: `MASTER_FILE_ORGANIZATION.md` (Lines 1-527)
- **System Architecture**: `SYSTEM_WORKFLOW.md` (Referenced in master files)

---

## **🔄 Complete User Journey Workflow**

### **Phase 1: Application Startup**
```
┌─────────────────────────────────────────────────────────────┐
│                    SAVORME STARTUP WORKFLOW                 │
└─────────────────────────────────────────────────────────────┘

1. User runs startup script:
   📁 start.bat (Primary) OR LOCAL_TEST_TOMORROW.bat
   📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 105-113)

2. System auto-detects configuration:
   📁 .env file detection (API keys)
   📁 Reference: SAVORME_MASTER_OVERVIEW.md (Lines 230-248)

3. Services start:
   🚀 Backend: http://127.0.0.1:8000
   🎨 Frontend: http://localhost:5000
   📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 29-32)
```

### **Phase 2: User Profile Creation**
```
┌─────────────────────────────────────────────────────────────┐
│                   USER PROFILE WORKFLOW                     │
└─────────────────────────────────────────────────────────────┘

1. User accesses frontend:
   📁 demo_app/templates/profile.html
   📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 184-186)

2. User inputs profile data:
   • Age, Gender, Height, Weight
   • Activity Level (Sedentary → Very Active)
   • Dietary Preferences (Vegetarian, Vegan, etc.)
   • Food Allergies
   • Cuisine Preferences (Mediterranean, Asian, Mexican, Italian, American)

3. Frontend validation:
   📁 demo_app/static/js/profile.js
   📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 196-198)

4. Backend nutrition calculation:
   📁 app/services/nutrition_calculator.py
   📁 Reference: SAVORME_MASTER_OVERVIEW.md (Lines 19-26)
```

### **Phase 3: Mood Selection**
```
┌─────────────────────────────────────────────────────────────┐
│                    MOOD SELECTION WORKFLOW                  │
└─────────────────────────────────────────────────────────────┘

1. User selects moods:
   📁 demo_app/templates/mood_selection.html
   📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 186-187)

2. Available moods (Evidence-based):
   • Stressed (Magnesium + Omega-3 rich)
   • Fatigued (Iron + Vitamin C rich)
   • Low Mood (Fiber + Omega-3 rich)
   • Irritable (Protein + Fiber rich, low sugar)

3. Intensity levels:
   • A Little (30% weight)
   • Medium (60% weight)
   • Very (100% weight)

4. Frontend processing:
   📁 demo_app/static/js/mood_selection.js
   📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 197-198)
```

### **Phase 4: Mood Interpretation & Recipe Search**
```
┌─────────────────────────────────────────────────────────────┐
│                MOOD INTERPRETATION WORKFLOW                 │
└─────────────────────────────────────────────────────────────┘

1. Mood blend processing:
   📁 app/services/fusion_engine.py
   📁 Reference: SAVORME_MASTER_OVERVIEW.md (Line 23)

2. Flavor profile generation:
   • Flavor bias (calming, energizing, comforting, stabilizing)
   • Texture preference (soft, substantial, comforting, balanced)
   • Culinary tone (calming, energizing, nurturing, balancing)
   • Search keywords (ingredient combinations)

3. Cuisine-aware keyword selection:
   📁 app/services/fusion_engine.py (Lines 196-225)
   📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 66-69)

4. Dynamic ingredient replacement:
   📁 app/services/edamam_client.py (Lines 762-803)
   📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 54-58)
```

### **Phase 5: Recipe Search & Scoring**
```
┌─────────────────────────────────────────────────────────────┐
│                 RECIPE SEARCH & SCORING WORKFLOW            │
└─────────────────────────────────────────────────────────────┘

1. Edamam API search:
   📁 app/services/edamam_client.py
   📁 Reference: SAVORME_MASTER_OVERVIEW.md (Line 24)

2. Recipe filtering:
   • Cuisine type filtering
   • Dietary preference filtering
   • Allergy filtering
   • Calorie range (15-50% of daily needs)
   • Protein range (10-60% of daily needs)

3. Evidence-based nutrition scoring:
   📁 app/services/mood_nutrition_engine.py
   📁 Reference: SAVORME_MASTER_OVERVIEW.md (Line 23)

4. Scoring transparency:
   • Weighted scoring with evidence-based weights
   • Data source transparency (Edamam API + built-in database)
   • Daily intake context (meal vs daily targets)
   • Nutrient breakdown (individual contributions)
   📁 Reference: SAVORME_MASTER_OVERVIEW.md (Lines 160-164)
```

### **Phase 6: Recipe Enhancement & AI Content**
```
┌─────────────────────────────────────────────────────────────┐
│                RECIPE ENHANCEMENT WORKFLOW                  │
└─────────────────────────────────────────────────────────────┘

1. Image enhancement:
   📁 app/services/web_image_search.py
   📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 72-75)

2. Nutrition enhancement:
   📁 app/services/nutrient_web_lookup.py
   📁 Reference: SAVORME_MASTER_OVERVIEW.md (Line 25)

3. AI content generation:
   📁 app/services/openrouter_client.py
   📁 Reference: SAVORME_MASTER_OVERVIEW.md (Line 26)

4. Cooking directions generation:
   • Professional chef-level instructions
   • 1200 token limit for thorough instructions
   • Sectioned format (PREPARATION, COOKING, FINISHING, TIPS)
   📁 Reference: SAVORME_MASTER_OVERVIEW.md (Lines 166-172)
```

### **Phase 7: Recipe Variety & Rotation**
```
┌─────────────────────────────────────────────────────────────┐
│                 RECIPE VARIETY WORKFLOW                     │
└─────────────────────────────────────────────────────────────┘

1. Variety tracking:
   📁 app/services/recipe_rotation.py
   📁 Reference: SAVORME_MASTER_OVERVIEW.md (Line 26)

2. Recent recipe filtering:
   • Track last 10 keywords
   • Track last 15 ingredients
   • Prevent repetitive recommendations

3. Variety boosting:
   • Prioritize new ingredients
   • Avoid recently used recipes
   • Session-based tracking
```

### **Phase 8: Results Display**
```
┌─────────────────────────────────────────────────────────────┐
│                   RESULTS DISPLAY WORKFLOW                  │
└─────────────────────────────────────────────────────────────┘

1. Recipe results page:
   📁 demo_app/templates/recipe_result.html
   📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 187-188)

2. JavaScript-driven display:
   📁 demo_app/static/js/recipe_result.js
   📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 198)

3. Enhanced styling:
   📁 demo_app/static/css/recipe_results.css
   📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 194-195)

4. Display components:
   • Recipe image (high-resolution, smart fallback)
   • Recipe name and description
   • Ingredients list
   • Cooking directions (AI-generated)
   • Nutrition information
   • Emotional rationale (AI-generated)
   • Scoring transparency
```

---

## **🏗️ Microservices Architecture Workflow**

### **Local Development (Monolithic)**
```
┌─────────────────────────────────────────────────────────────┐
│                    LOCAL DEVELOPMENT FLOW                  │
└─────────────────────────────────────────────────────────────┘

Frontend (Flask) → Backend (FastAPI) → External APIs
     ↓                    ↓                    ↓
demo_app/            app/              Edamam API
├── app.py            ├── main.py       OpenRouter API
├── templates/        ├── api/routes.py  Web Image Search
└── static/           └── services/     Nutrient Web Lookup
```

### **Cloud Deployment (Microservices)**
```
┌─────────────────────────────────────────────────────────────┐
│                   CLOUD DEPLOYMENT FLOW                     │
└─────────────────────────────────────────────────────────────┘

Frontend → API Gateway → Microservices → External APIs
    ↓           ↓            ↓              ↓
savorme-    savorme-    mood-ai-      Edamam API
frontend    router      service       OpenRouter API
            │           recipe-       Web Image Search
            │           service       Nutrient Web Lookup
            │           user-nutrition-
            │           service
```

---

## **📊 Key Performance Metrics**

### **Success Rates (v3.2.0)**
- **Recipe Success Rate**: 95%+ (up from 60% due to exotic ingredients)
- **Image Loading**: 100% success rate with smart fallbacks
- **UI Responsiveness**: All interactive elements provide immediate feedback
- **Error Reduction**: 90% fewer user-facing errors
- **📁 Reference**: MASTER_FILE_ORGANIZATION.md (Lines 91-95)

### **Technical Improvements**
- **Dynamic Ingredient Replacement**: 99% reduction in recipe search failures
- **Smart Image Selection**: High-resolution images with intelligent matching
- **Enhanced UX**: Visual feedback for all interactions
- **📁 Reference**: MASTER_FILE_ORGANIZATION.md (Lines 52-75)

---

## **🔧 Critical File Dependencies**

### **Essential Files (Never Delete)**
```
📁 app/                    # Core backend functionality
📁 demo_app/              # Frontend application
📁 requirements.txt       # Dependencies
📁 .env                   # Environment variables
📁 start.bat             # Primary startup script
📁 Reference: MASTER_FILE_ORGANIZATION.md (Lines 368-378)
```

### **Master Documentation Files**
```
📁 SAVORME_MASTER_OVERVIEW.md      # Project overview & integration
📁 MASTER_FILE_ORGANIZATION.md     # File organization & status
📁 CUSTOMIZATIONS_PERSISTENT.md    # Design system & scoring transparency
📁 AUTOMATED_APP_STARTUP_GUIDE.md  # Startup procedures
📁 Reference: SAVORME_MASTER_OVERVIEW.md (Lines 39-65)
```

### **Technical Documentation**
```
📁 EDAMAM_API_INTEGRATION_GUIDE.md        # Edamam API documentation
📁 MOOD_INGREDIENT_CONVERSION_GUIDE.md   # Mood conversion system
📁 FOOD_IMAGE_SYSTEM_GUIDE.md            # Image handling system
📁 Reference: SAVORME_MASTER_OVERVIEW.md (Lines 103-109)
```

---

## **⚠️ Critical Maintenance Notes**

### **Always Update Together**
1. **SAVORME_MASTER_OVERVIEW.md** - Project status changes
2. **MASTER_FILE_ORGANIZATION.md** - File structure changes  
3. **CUSTOMIZATIONS_PERSISTENT.md** - Design system changes
4. **AUTOMATED_APP_STARTUP_GUIDE.md** - Startup procedure changes
- **📁 Reference**: SAVORME_MASTER_OVERVIEW.md (Lines 223-227)

### **Command Prompt Requirement**
- **NEVER use PowerShell** - Always use Command Prompt (cmd.exe)
- **📁 Reference**: SAVORME_MASTER_OVERVIEW.md (Lines 3-4)

### **Evidence-Based Nutrition**
- All nutrition claims must be evidence-based and medically safe
- **📁 Reference**: SAVORME_MASTER_OVERVIEW.md (Line 225)

---

## **🎯 Quick Reference Commands**

### **Startup Commands**
```cmd
# Primary startup (recommended)
start.bat

# Local testing with validation
LOCAL_TEST_TOMORROW.bat

# First-time setup for new clones
setup_new_clone.bat
```

### **Access Points**
- **Frontend**: http://localhost:5000
- **Backend**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

---

*This comprehensive workflow shows how your SavorMe application processes user input through mood interpretation, recipe search, evidence-based scoring, and AI enhancement to provide personalized recipe recommendations. All references point to your master documentation files for complete system understanding.*
