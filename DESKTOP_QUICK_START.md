# 🖥️ SavorMe Desktop App - Quick Start Guide

## ⚠️ CRITICAL: Command Prompt Only!
```
ALWAYS USE: Command Prompt (cmd.exe)
NEVER USE: PowerShell (causes && operator errors)
```

## 🚀 Start Desktop App (1 Command)

```cmd
cd C:\Users\Samsung\savorme-cloud-run\SavorMeDeviceSensitive
START-BOTH-SERVICES.bat
```

This starts:
- **Backend**: http://127.0.0.1:8000
- **Desktop**: http://localhost:5001

## 📂 Desktop vs Mobile Separation

| App | Port | Directory | Purpose |
|-----|------|-----------|---------|
| **Desktop** | 5001 | `desktop_app/` | Screens 1024px+ |
| **Mobile** | 5000 | `demo_app/` | Mobile/responsive |

**⚠️ DO NOT MIX FILES** between desktop and mobile apps!

## 📋 Key Files

### Desktop App Files (desktop_app/)
- `app.py` - Flask app (port 5001)
- `templates/desktop-*.html` - Desktop templates
- `static/css/desktop-*.css` - Desktop styles
- `requirements.txt` - Desktop dependencies
- `README.md` - Full documentation

### Startup Scripts
- `START-BOTH-SERVICES.bat` - Backend + Desktop
- `start-backend-only.bat` - Backend only
- `start-desktop-only.bat` - Desktop only
- `cleanup-processes.bat` - Kill all processes
- `restart-desktop.bat` - Restart desktop

## ✨ Desktop Features
- ✅ Full-width recipe cards
- ✅ Medical disclaimers (3 locations)
- ✅ Decimal formatting (max 2 decimals)
- ✅ Filtered cooking steps
- ✅ Smooth transitions
- ✅ Save recipes
- ✅ Nutrient match score modal

## 📖 Full Documentation
- `desktop_app/README.md` - Complete desktop docs
- `MASTER_FILE_ORGANIZATION.md` - All files reference
- `API_SCHEMA_REFERENCE.md` - API format
- `EDAMAM_JSON_FORMAT.md` - Edamam API format

---

**Version**: 4.0.0 (Desktop + Mobile Separation)  
**Last Updated**: October 2025

