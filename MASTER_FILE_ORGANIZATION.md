# SavorMe Master File Organization

## 🎯 **Purpose**
This document provides a comprehensive overview of all files in the SavorMe project, organized by category and purpose, to ensure efficient management and avoid forgotten files.

## 📁 **File Categories & Organization**

### **1. CORE APPLICATION FILES** ⭐ (Essential - Never Delete)

#### **Backend Core**
```
app/
├── main.py                    # FastAPI application entry point
├── api/routes.py              # API endpoints
├── core/config.py             # Configuration management
├── models/                    # Data models
│   ├── user.py               # User profile models
│   ├── mood.py               # Mood mapping models
│   └── recipe.py             # Recipe data models
├── services/                  # Business logic services
│   ├── edamam_client.py      # Recipe search service
│   ├── openrouter_client.py  # AI cooking directions
│   ├── mood_nutrition_engine.py # Mood-to-nutrition mapping
│   ├── fusion_engine.py      # Recipe recommendation logic
│   ├── nutrition_calculator.py # Nutritional analysis
│   └── canva_client.py       # Canva integration (if used)
└── data/
    └── mood_mapping.json     # Mood-to-nutrition mapping data
```

#### **Frontend Core**
```
demo_app/
├── app.py                    # Flask application entry point
├── templates/                # HTML templates
│   ├── index.html           # Landing page
│   ├── profile.html         # User profile page
│   ├── mood_selection.html  # Mood selection page
│   └── recipe_result.html   # Recipe results page
├── static/css/              # Stylesheets
│   ├── main.css            # Base styles
│   ├── landing.css         # Landing page styles
│   ├── profile.css         # Profile page styles
│   ├── mood_selection.css  # Mood selection styles
│   ├── results.css         # Results page styles
│   └── recipe_results.css  # Recipe results styles
└── static/js/              # JavaScript files
    ├── profile.js          # Profile page logic
    ├── mood_selection.js   # Mood selection logic
    └── recipe_result.js    # Recipe results logic
```

#### **Configuration Files**
```
requirements.txt             # Python dependencies
.env                        # Environment variables
.gitignore                  # Git ignore rules
```

### **2. STARTUP & DEPLOYMENT SCRIPTS** 🚀 (Essential for Operation)

#### **Primary Startup Scripts** (Use These)
```
start_savorme_simple.bat            # ⭐ SIMPLE STARTUP SCRIPT - RECOMMENDED
savorme_professional_startup.bat    # ⭐ PROFESSIONAL STARTUP - Advanced diagnostics
start_savorme_reliable.bat          # ⭐ RELIABLE STARTUP - Backup option
```

#### **Legacy/Backup Scripts** (Keep but Don't Use)
```
setup_new_clone.bat                # Environment setup
start_savorme_auto.bat             # Auto startup
start_backend.bat                  # Backend only
start_demo.bat                     # Frontend only
start_app_reliable.bat             # Alternative startup
start_with_setup.py                # Python startup script
```

### **3. DOCUMENTATION FILES** 📚 (Organized by Priority)

#### **Master Documentation** (Essential Reading)
```
SAVORME_MASTER_OVERVIEW.md             # ⭐ COMPLETE PROJECT REFERENCE (NEW)
CUSTOMIZATIONS_PERSISTENT.md           # ⭐ DESIGN SYSTEM & SCORING TRANSPARENCY (CRITICAL)
AUTOMATED_APP_STARTUP_GUIDE.md         # ⭐ COMPREHENSIVE STARTUP GUIDE
MASTER_FILE_ORGANIZATION.md            # ⭐ FILE ORGANIZATION & PRIORITIES
TECHNICAL_SPECIFICATION_COMPLETE.md    # ⭐ COMPLETE TECHNICAL BLUEPRINT
QUICK_IMPLEMENTATION_GUIDE.md          # ⭐ QUICK START GUIDE
README.md                              # ⭐ PROJECT OVERVIEW
```

#### **Setup & Deployment Guides** (Important)
```
CONFIGURATION_SUMMARY.md               # Quick configuration reference (NEW)
SAVORME_PROJECT_STATUS.md              # Project status overview (NEW)
DIRECTORY_CLEANUP_ANALYSIS.md          # Directory organization analysis (NEW)
STARTUP_GUIDE.md                       # General startup instructions
RUN_DEMO_INSTRUCTIONS.md               # Demo running instructions
```

#### **System Design & Architecture** (Reference)
```
SYSTEM_DESIGN_FINAL.md                 # System architecture
SYSTEM_WORKFLOW.md                     # Application workflow
PAGE_LAYOUTS_REFERENCE.md              # Page layout specifications
MOOD_TO_RECIPE_FLOW.md                 # Mood-to-recipe process
```

#### **Legacy Documentation** (Archive - Can be Consolidated)
```
AUTOMATED_REVIEW_IMPLEMENTATION_GUIDE.md
AUTOMATIC_SETUP_IMPLEMENTATION.md
CLONE_SETUP_GUIDE.md
COMPREHENSIVE_UPDATE_SUMMARY.md
DIRECTORY_CLEANUP_ANALYSIS.md
documentation_fix_report.md
DOCUMENTATION_REVIEW_CHECKLIST.md
documentation_review_report.md
EVIDENCE_BASED_MOODS_v2.md
FINAL_VERIFICATION_CHECKLIST.md
MAPPING_DATA_SOURCES.md
QUICK_START_COMMANDS.md
REVIEW_PROCESS_IMPROVEMENT_SUMMARY.md
CLEANUP_COMPLETION_REPORT.md
```

### **4. UTILITY & TESTING FILES** 🔧 (Development Tools)

#### **Testing & Development**
```
test_imports.py                        # Import testing
test_api.json                          # API testing data
batch_fix_documentation.py             # Documentation automation
docs_review_automation.py              # Documentation review
```

### **5. VIRTUAL ENVIRONMENT** 🐍 (Auto-Generated)
```
venv/                                  # Python virtual environment
├── Scripts/                          # Activation scripts
├── Lib/site-packages/                # Installed packages
└── pyvenv.cfg                        # Environment config
```

## 🎯 **File Usage Priority Matrix**

### **ESSENTIAL FILES** (Must Keep - Core Functionality)
- All files in `app/` directory
- All files in `demo_app/` directory
- `requirements.txt`
- `.env`
- `savorme_professional_startup.bat`
- `TECHNICAL_SPECIFICATION_COMPLETE.md`
- `QUICK_IMPLEMENTATION_GUIDE.md`
- `CUSTOMIZATIONS_PERSISTENT.md` ⚠️ **CRITICAL FOR PAGE REBUILDING**
- `AUTOMATED_APP_STARTUP_GUIDE.md` ⚠️ **CRITICAL FOR DEPLOYMENT**
- `README.md`

### **IMPORTANT FILES** (Should Keep - Operational)
- `start_savorme_reliable.bat`
- `STARTUP_GUIDE.md`
- `SYSTEM_DESIGN_FINAL.md`
- `PAGE_LAYOUTS_REFERENCE.md`

### **REFERENCE FILES** (Can Keep - Documentation)
- `SYSTEM_WORKFLOW.md`
- `MOOD_TO_RECIPE_FLOW.md`
- `RUN_DEMO_INSTRUCTIONS.md`

### **LEGACY FILES** (Can Archive/Delete - Redundant)
- All other `.md` files (consolidated into master docs)
- `start_with_setup.py` (replaced by batch scripts)
- `test_api.json` (if not actively used)

## 🔄 **Recommended File Consolidation**

### **Create Master Documentation**
1. **Merge all setup guides** into `AUTOMATED_APP_STARTUP_GUIDE.md`
2. **Merge all system design docs** into `SYSTEM_DESIGN_FINAL.md`
3. **Archive legacy documentation** into `docs/archive/` folder
4. **Keep only essential startup scripts**

### **File Cleanup Actions**
1. **Delete redundant documentation files**
2. **Consolidate startup scripts** (keep only 2-3 best ones)
3. **Archive legacy files** instead of deleting
4. **Create clear file naming conventions**

## 📋 **File Maintenance Checklist**

### **Before Each Release**
- [ ] Update `README.md` with latest features
- [ ] Update `TECHNICAL_SPECIFICATION_COMPLETE.md` with changes
- [ ] Test all startup scripts
- [ ] Archive old documentation files
- [ ] Update version numbers in scripts

### **Monthly Maintenance**
- [ ] Review and consolidate documentation
- [ ] Clean up unused files
- [ ] Update file organization document
- [ ] Test all essential files

## 🔗 **Critical Documentation Relationships**

### **Documentation Dependencies**
The following files work together and should be used in conjunction:

1. **`CUSTOMIZATIONS_PERSISTENT.md`** ← **MASTER REFERENCE**
   - Contains all design system specifications
   - Lists all customized files and their changes
   - Provides code snippets for rebuilding pages
   - **Recipe Match Score Transparency System** with weighted scoring breakdown
   - **Data source documentation** (Edamam API + built-in nutrient database)
   - **MUST BE REVIEWED** before any deployment or clone

2. **`AUTOMATED_APP_STARTUP_GUIDE.md`** ← **DEPLOYMENT GUIDE**
   - References `CUSTOMIZATIONS_PERSISTENT.md` throughout
   - Includes Command Prompt requirement (never PowerShell)
   - Provides step-by-step verification of all customizations
   - **MUST BE USED** for proper deployment

3. **`TECHNICAL_SPECIFICATION_COMPLETE.md`** ← **TECHNICAL BLUEPRINT**
   - Complete system architecture and functionality
   - Works with both customization and startup guides

4. **`QUICK_IMPLEMENTATION_GUIDE.md`** ← **QUICK REFERENCE**
   - Fast setup instructions
   - Complements the automated startup guide

### **File Usage Workflow**
```
CUSTOMIZATIONS_PERSISTENT.md (Review First)
           ↓
AUTOMATED_APP_STARTUP_GUIDE.md (Follow for Deployment)
           ↓
TECHNICAL_SPECIFICATION_COMPLETE.md (Reference for Details)
           ↓
QUICK_IMPLEMENTATION_GUIDE.md (Quick Setup)
```

### **Critical Files for Page Rebuilding**
Based on `CUSTOMIZATIONS_PERSISTENT.md`, these files are essential for proper page reconstruction:

#### **Landing Page Customizations**
- `demo_app/templates/index.html` - Landing page template
- `demo_app/static/css/landing.css` - Landing page styling

#### **Recipe Results Page Customizations**
- `demo_app/templates/recipe_result.html` - Minimal template for JavaScript-driven page
- `demo_app/static/js/recipe_result.js` - Complete JavaScript functionality
- `demo_app/static/css/recipe_results.css` - Complete styling

#### **Backend Customizations**
- `app/services/openrouter_client.py` - Cooking directions fix

#### **Design System Files**
- All CSS files in `demo_app/static/css/`
- All JavaScript files in `demo_app/static/js/`
- All template files in `demo_app/templates/`

**⚠️ WARNING**: If any of these files are missing or modified incorrectly, the pages will not display properly. Always reference `CUSTOMIZATIONS_PERSISTENT.md` for the exact specifications.

## 🚀 **Quick Start File Priority**

### **For New Developers**
1. Read `README.md` first
2. Read `TECHNICAL_SPECIFICATION_COMPLETE.md`
3. **CRITICAL**: Review `CUSTOMIZATIONS_PERSISTENT.md` for design system
4. Use `savorme_professional_startup.bat` to start
5. Follow `AUTOMATED_APP_STARTUP_GUIDE.md` for complete setup

### **For Deployment**
1. **ALWAYS** review `CUSTOMIZATIONS_PERSISTENT.md` first
2. Use `savorme_professional_startup.bat`
3. Follow `AUTOMATED_APP_STARTUP_GUIDE.md` (includes Command Prompt requirement)
4. Reference `QUICK_IMPLEMENTATION_GUIDE.md` for setup
5. Verify all customization files are present and correct

---

*This master file organization ensures efficient project management and prevents important files from being forgotten or lost.*
