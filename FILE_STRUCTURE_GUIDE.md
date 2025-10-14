# 📁 SavorMe File Structure Guide

## 🎯 **ESSENTIAL FILES - WHAT EACH ONE DOES**

### **⭐ START HERE TOMORROW**
- **`RESUME_WORK_TOMORROW.md`** - Copy/paste this into Cursor to resume work
- **`LOCAL_TEST_TOMORROW.bat`** - Double-click to test locally
- **`DEPLOY_TO_CLOUD_RUN.bat`** - Double-click to deploy to Cloud Run

---

## 📂 **APPLICATION CODE** (The actual app)

### **Frontend App** (`frontend_app/`)
- **`app.py`** - Flask server (proxies API calls to backend)
- **`templates/`** - HTML pages (index, profile, mood_selection, recipe_result)
- **`static/js/`** - JavaScript files (handles user interactions)
- **`static/css/`** - Styling files
- **`Dockerfile`** - How to build frontend for Cloud Run
- **`requirements.txt`** - Python packages needed

### **Local Testing Frontend** (`demo_app/`)
- Same structure as `frontend_app/`
- Used for local testing only
- **Modified today:** Fixed `recipe_result.js` button event listener

### **Backend Microservices** (`backend_app/`)

#### **Router Service** (`router/`)
- **`main.py`** - API Gateway (orchestrates all microservices)
- **Modified today:** Updated service URLs, fixed Pydantic serialization
- Routes: `/api/v1/recipes/recommend`, `/api/v1/health`

#### **User Nutrition Service** (`backend_app/user-nutrition-service/`)
- **`main.py`** - Calculates nutrition targets based on user profile
- **Modified today:** Fixed port to 8080, fixed imports

#### **Recipe Service** (`backend_app/recipe-service/`)
- **`main.py`** - Searches Edamam API for recipes
- **Modified today:** Added cuisine mapping, fallback logic for Edamam API

#### **Mood AI Service** (`backend_app/mood-ai-service/`)
- **`main.py`** - Interprets moods and generates AI content
- **Modified today:** Fixed port to 8080, added MoodInterpretation import

### **Monolithic Backend** (`app/`)
- **`main.py`** - Original combined backend (for local testing)
- **Modified today:** Fixed indentation error
- Used when testing locally with `demo_app/`

---

## 📋 **DEPLOYMENT FILES**

### **Cloud Run**
- **`cloudbuild.yaml`** - Defines how to build and deploy all 5 services
- **`deploy-to-cloud-run.bat`** - DEPRECATED (use `DEPLOY_TO_CLOUD_RUN.bat` instead)
- **`DEPLOY_TO_CLOUD_RUN.bat`** - ⭐ NEW: Clean deployment script

### **Docker**
- **`docker-compose.yml`** - Runs all services locally in Docker
- Each service has its own `Dockerfile`

---

## 📚 **DOCUMENTATION FILES** (Read these to understand the project)

### **⭐ Core Documentation**
- **`README.md`** - Project overview
- **`SAVORME_MASTER_OVERVIEW.md`** - Complete system overview
- **`SYSTEM_WORKFLOW.md`** - How the system works end-to-end
- **`FILE_STRUCTURE_GUIDE.md`** - ⭐ THIS FILE!

### **Setup Guides**
- **`SETUP_INSTRUCTIONS.md`** - Initial setup for this computer
- **`QUICK_START_OTHER_COMPUTER.md`** - Setup for different computer
- **`OTHER_COMPUTER_SETUP.md`** - Detailed setup for different computer
- **`CLONE_SETUP_GUIDE.md`** - How to clone and set up from GitHub
- **`setup_new_clone.bat`** - Automated setup script

### **Deployment Guides**
- **`CLOUD_RUN_DEPLOYMENT.md`** - Cloud Run deployment details
- **`DEPLOYMENT_GUIDE.md`** - General deployment guide
- **`DEPLOYMENT_READY.md`** - Pre-deployment checklist

### **Development Guides**
- **`MASTER_FILE_ORGANIZATION.md`** - How files are organized
- **`COPY_PASTE_THESE_COMMANDS.md`** - Common commands
- **`CUSTOMIZATIONS_PERSISTENT.md`** - User preferences/customizations

### **Status & Progress**
- **`PROJECT_STATUS.md`** - Current project status
- **`RESUME_TOMORROW.md`** - Progress log from today
- **`WHATS_NEW.md`** - Recent changes
- **`AUTOMATED_APP_STARTUP_GUIDE.md`** - How to start the app

---

## 🔧 **UTILITY SCRIPTS** (Helper batch files)

### **Local Testing**
- **`LOCAL_TEST_TOMORROW.bat`** - ⭐ NEW: Start both frontend and backend
- **`start.bat`** - Start monolithic backend only

### **Deployment**
- **`deploy-frontend-only.bat`** - Deploy only frontend (not recommended)

### **Git & GitHub**
- **`github-setup.bat`** - Initial GitHub setup
- **`push-to-github.bat`** - Push changes to GitHub

### **Docker**
- **`start-microservices.bat`** - Start all microservices in Docker
- **`setup-microservices.bat`** - Setup microservices
- **`test-docker-builds.bat`** - Test Docker builds

### **Setup**
- **`check-setup.bat`** - Verify environment setup
- **`setup_new_clone.bat`** - Setup fresh clone

---

## 📦 **DATA FILES**

### **Mood & Nutrition Data** (`app/data/`)
- **`mood_mapping.json`** - Maps moods to nutrients
- **`edamam_constants.py`** - Edamam API constants (cuisines, diets, etc.)

### **Shared Models** (`backend_app/shared/` and service-level `shared_models.py`)
- **`models.py`** or **`shared_models.py`** - Data models used across services
- Modified today: Each service now has its own `shared_models.py`

---

## 🗑️ **FILES YOU CAN IGNORE**

- **`venv/`** - Python virtual environment (auto-generated)
- **`__pycache__/`** - Python cache files (auto-generated)
- **`GoogleCloudSDKInstaller.exe`** - Google Cloud SDK installer
- **`TRANSFER_PACKAGE.md`** - Packaging instructions (rarely used)
- **`SETUP_REQUIREMENTS.md`** - Initial requirements doc

---

## 🎯 **TOMORROW'S WORKFLOW**

1. **Open Cursor**
2. **Paste content from `RESUME_WORK_TOMORROW.md`**
3. **Double-click `LOCAL_TEST_TOMORROW.bat`** to test locally
4. **Test all 4 cuisines:** Mediterranean, Asian, Italian, Mexican
5. **Test all 4 moods:** Stressed, Fatigued, Low Mood, Irritable
6. **If all works:** Double-click `DEPLOY_TO_CLOUD_RUN.bat`
7. **Done!** 🎉

---

## 📊 **FILE COUNT SUMMARY**

| Category | Count | Purpose |
|----------|-------|---------|
| Application Code | 20+ files | The actual SavorMe app |
| Documentation | 15 files | Guides and explanations |
| Utility Scripts | 10 files | Helper batch files |
| Data Files | 3 files | Mood/nutrition mappings |
| Config Files | 5 files | Docker, Cloud Run config |

---

**Last Updated:** October 14, 2025  
**Status:** Local app working perfectly, ready for Cloud Run deployment

