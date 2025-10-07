# SavorMe Clone Setup Guide

⚠️ **CRITICAL**: Always use Command Prompt (cmd.exe), NEVER PowerShell when running setup scripts!
PowerShell causes compatibility issues with batch scripts and environment setup.

**Date**: October 5, 2025  
**Purpose**: Guide for setting up SavorMe from GitHub clone

## 🎯 Quick Answer to Your Question

**No, cloning from GitHub will NOT automatically connect to your existing `C:\Users\HP\SavorMe` configuration.** Here's why and how to set it up:

## 📋 What Happens When You Clone

### **✅ What Gets Cloned:**
- Complete application code (backend + frontend)
- All documentation files (16 comprehensive guides)
- Startup scripts and testing tools
- Configuration templates

### **❌ What Does NOT Get Cloned:**
- **`.env` file** (your API keys - excluded for security)
- **`venv/` directory** (virtual environment)
- **`__pycache__/` directories** (Python cache)

## 🚀 Setup Process After Cloning

### **Option 1: Automatic Setup (Recommended)**
```cmd
# After cloning
cd [your-new-clone-directory]
start_savorme_auto.bat
```

### **Option 2: Python Setup Script**
```cmd
# After cloning
cd [your-new-clone-directory]
py start_with_setup.py
```

### **Option 3: Manual Setup**
```cmd
# 1. Create virtual environment
py -m venv venv
venv\Scripts\activate.bat

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test imports
venv\Scripts\python.exe test_imports.py

# 4. Copy your .env file
copy C:\Users\HP\SavorMe\SavorMe-backend\.env .env

# 5. Start application
start_app_reliable.bat
```

## 🔑 API Configuration

### **Copy Your Existing Configuration:**
```cmd
# Copy your working .env file
copy C:\Users\HP\SavorMe\SavorMe-backend\.env [new-clone-directory]\.env
```

### **Or Create New .env File:**
```cmd
# Create new .env file with your API keys
EDAMAM_APP_ID=your_edamam_app_id
EDAMAM_APP_KEY=your_edamam_app_key
OPENROUTER_API_KEY=your_openrouter_api_key
CANVA_CLIENT_ID=your_canva_client_id
CANVA_CLIENT_SECRET=your_canva_client_secret
```

## 📁 Directory Structure After Clone

```
[your-new-clone-directory]/
├── app/                          # Backend application
├── demo_app/                     # Frontend application
├── venv/                         # Virtual environment (created)
├── .env                          # API configuration (copied)
├── requirements.txt              # Dependencies
├── start_app_reliable.bat        # Startup script
├── setup_new_clone.bat           # Setup script
├── test_imports.py               # Import validation
├── README.md                     # Project documentation
├── STARTUP_GUIDE.md              # Startup instructions
├── QUICK_START_COMMANDS.md       # Quick commands
├── FINAL_VERIFICATION_CHECKLIST.md # Verification checklist
├── PAGE_LAYOUTS_REFERENCE.md     # *(Merged into CUSTOMIZATIONS_PERSISTENT.md)*
├── EVIDENCE_BASED_MOODS_v2.md    # Scientific foundation
├── SYSTEM_DESIGN_FINAL.md        # System architecture
├── SYSTEM_WORKFLOW.md            # Workflow documentation
├── MOOD_TO_RECIPE_FLOW.md        # Technical flow
├── MAPPING_DATA_SOURCES.md       # Data sources
├── RUN_DEMO_INSTRUCTIONS.md      # Demo instructions
├── AUTOMATED_REVIEW_IMPLEMENTATION_GUIDE.md # Automation guide
├── DOCUMENTATION_REVIEW_CHECKLIST.md # Documentation standards
├── REVIEW_PROCESS_IMPROVEMENT_SUMMARY.md # Process improvements
├── docs_review_automation.py     # Documentation automation
├── batch_fix_documentation.py    # Batch fixing tool
├── documentation_fix_report.md   # Fix report
├── documentation_review_report.md # Review report
├── DIRECTORY_CLEANUP_ANALYSIS.md # Cleanup analysis
└── CLEANUP_COMPLETION_REPORT.md  # Cleanup completion report
```

## 🎯 Best Practices

### **1. Keep Your Original Directory**
- **Keep**: `C:\Users\HP\SavorMe\SavorMe-backend\` as your main working directory
- **Use clones**: For testing, development branches, or sharing

### **2. API Key Management**
- **Never commit**: `.env` files to GitHub (they're in `.gitignore`)
- **Always copy**: Your working `.env` file to new clones
- **Keep secure**: Your API keys are private and should not be shared

### **3. Virtual Environment**
- **Each clone**: Needs its own virtual environment
- **Isolated**: Dependencies won't conflict between clones
- **Clean**: Fresh environment for each project instance

## 🚀 Quick Start Commands

### **After Cloning:**
```cmd
# Navigate to clone directory
cd [your-clone-directory]

# Run automated setup
setup_new_clone.bat

⚠️ **CRITICAL**: Run in Command Prompt (cmd.exe), NOT PowerShell!

# Copy your API configuration
copy C:\Users\HP\SavorMe\SavorMe-backend\.env .env

# Start the application
start_app_reliable.bat
```

### **Access Points:**
- **Frontend**: http://localhost:5000
- **Backend**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

## ✅ Verification Checklist

After setup, verify:
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] Import test passes
- [ ] `.env` file copied with API keys
- [ ] Application starts without errors
- [ ] Frontend accessible at http://localhost:5000
- [ ] Backend accessible at http://127.0.0.1:8000

## 🎯 Summary

**Cloning from GitHub gives you the complete application code and documentation, but you need to:**
1. **Create virtual environment**
2. **Install dependencies**
3. **Copy your API configuration**
4. **Start the application**

**The `setup_new_clone.bat` script automates steps 1-3, making the process seamless!**
