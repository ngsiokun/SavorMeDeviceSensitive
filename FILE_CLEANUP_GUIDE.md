# SavorMe v4.0.0 - File Cleanup Guide

## 🎯 Purpose
This guide helps identify which files to keep and which can be safely deleted after the v4.0.0 upgrade.

---

## ❌ FILES TO DELETE (Obsolete/Temporary)

### Test Files (No longer needed)
```
✗ test-api-direct.py                 # Old API testing script
✗ test-backend-direct.bat            # Old backend testing
✗ test-connection.bat                # Replaced by health checks
✗ test-docker-builds.bat             # Only for Docker deployment (optional)
```

### Obsolete Startup Scripts
```
✗ START-UNIFIED.bat                  # Replaced by START.bat
✗ unified_app.py                     # Not recommended - use app_router.py
✗ start-desktop-with-backend.bat     # Replaced by START-BOTH-SERVICES.bat
✗ restart-all.bat                    # Replaced by cleanup + restart scripts
```

### Temporary Consultation Files
```
✗ CHATGPT_HELP_REQUEST.md            # Temporary help request
✗ GEMINI_DEPLOYMENT_CONSULTATION.md  # Temporary consultation
✗ BACKEND_TROUBLESHOOTING_FOR_GEMINI.md # Temporary troubleshooting (can archive)
```

---

## ✅ FILES TO KEEP (Essential)

### Core Application Files
```
✓ app/                    # Backend API (FastAPI)
✓ desktop_app/            # Desktop frontend
✓ demo_app/               # Mobile frontend
✓ app_router.py           # Device detection router ⭐
```

### Startup Scripts (Essential)
```
✓ START.bat               # ⭐ MAIN - Auto-detect, no menu
✓ START-ALL-SEPARATE.bat  # All services separate for debugging
✓ start.bat               # Interactive menu
✓ START-BOTH-SERVICES.bat # Desktop + Backend
✓ start-backend-only.bat  # Backend only
✓ start-desktop-only.bat  # Desktop only
✓ restart-desktop.bat     # Restart desktop
✓ cleanup-processes.bat   # Clean up processes
✓ setup_new_clone.bat     # Setup for new clones
```

### Master Documentation
```
✓ MASTER_FILE_ORGANIZATION.md          # ⭐ SINGLE SOURCE OF TRUTH
✓ AUTOMATED_APP_STARTUP_GUIDE.md       # ⭐ Startup guide
✓ CUSTOMIZATIONS_PERSISTENT.md         # ⭐ Design system
✓ AUTO_DETECT_ARCHITECTURE.md          # ⭐ Auto-detect system
✓ README.md                            # Project overview
✓ API_SCHEMA_REFERENCE.md              # API schemas
✓ EDAMAM_JSON_FORMAT.md                # Edamam format
✓ CLEANUP_SUMMARY_V4.md                # v4.0.0 cleanup summary
✓ FILE_CLEANUP_GUIDE.md                # This file
```

### Technical Documentation
```
✓ EDAMAM_API_INTEGRATION_GUIDE.md
✓ MOOD_INGREDIENT_CONVERSION_GUIDE.md
✓ FOOD_IMAGE_SYSTEM_GUIDE.md
✓ EDAMAM_COMPATIBILITY_FIX.md
✓ PROBLEMATIC_INGREDIENTS_FIX.md
✓ IMAGE_ARCHITECTURE_DECISION.md
```

### Desktop App Documentation
```
✓ desktop_app/README.md               # Desktop docs
✓ DESKTOP_QUICK_START.md              # Quick start
```

### Configuration Files
```
✓ requirements.txt
✓ .env
✓ .gitignore
✓ docker-compose.yml
```

---

## 🤔 OPTIONAL (Keep if needed)

### Docker/Cloud Deployment
```
? test-docker-builds.bat              # Only if deploying to Docker
? deploy-to-cloud-run.bat             # Only for Cloud Run deployment
? deploy-frontend-only.bat            # Only for Cloud Run
? cloudbuild.yaml                     # Only for Cloud Run
? Dockerfile, Dockerfile.frontend, etc. # Only for Docker
```

### Microservices (If not used)
```
? start-microservices.bat             # Only if using microservices
? setup-microservices.bat             # Only if using microservices
? backend_app/                        # Only for microservices deployment
? router/                             # Only for microservices gateway
```

### Alternative Frontend (If not used)
```
? frontend_app/                       # Alternative frontend (if not used)
```

---

## 🚀 Quick Cleanup

Run this command to automatically delete obsolete files:
```cmd
CLEANUP-OLD-FILES.bat
```

This will safely remove:
- Test files
- Obsolete startup scripts
- Temporary consultation files

---

## 📊 Before vs After

### Before Cleanup
```
Total Files: ~150+ files
- Many test files
- Duplicate startup scripts
- Temporary help files
- Confusing file structure
```

### After Cleanup
```
Total Files: ~120 essential files
- Clear startup options (START.bat ⭐)
- Organized documentation
- Only essential scripts
- Easy to navigate
```

---

## 🔍 How to Verify

### Check if file is essential:
1. Is it referenced in `MASTER_FILE_ORGANIZATION.md`? → **KEEP**
2. Is it a test/temp file? → **DELETE**
3. Is it a duplicate startup script? → **DELETE** (keep only new ones)
4. Not sure? → Check this guide or keep it

### Safe to delete if:
- ✗ File name starts with "test-"
- ✗ File name starts with "old-" or "backup-"
- ✗ File contains "TEMP", "HELP_REQUEST", "CONSULTATION"
- ✗ Duplicate of newer script (e.g., START-UNIFIED.bat → START.bat)

---

## 📝 Post-Cleanup Checklist

After cleanup, verify:
- [ ] `START.bat` exists and works
- [ ] `app_router.py` exists
- [ ] `MASTER_FILE_ORGANIZATION.md` is updated
- [ ] All documentation files exist
- [ ] Desktop and mobile apps still work
- [ ] Backend still connects

---

## 🎯 Recommended Action

1. **Review** this guide
2. **Run** `CLEANUP-OLD-FILES.bat` to auto-delete obsolete files
3. **Test** `START.bat` to ensure everything works
4. **Archive** (don't delete) if unsure about a file

---

**Version**: 4.0.0  
**Last Updated**: October 2025  
**Cross-Reference**: MASTER_FILE_ORGANIZATION.md

