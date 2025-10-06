# SavorMe Configuration Summary

**Date**: October 6, 2025  
**Version**: 3.1.0  
**Status**: Production Ready with Enhanced Scoring Transparency

## 🎯 **Quick Configuration Reference**

### **Active Project Directory**
```
C:\Users\HP\SavorMe\SavorMe-backend\
```

### **Startup Commands**
```cmd
# Primary startup (recommended)
start_savorme_simple.bat

# Professional startup (with diagnostics)
savorme_professional_startup.bat

# Backup startup
start_savorme_reliable.bat
```

### **Access Points**
- **Frontend**: http://localhost:5000
- **Backend**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

### **Essential Files**
- `CUSTOMIZATIONS_PERSISTENT.md` - Complete design system and scoring transparency
- `AUTOMATED_APP_STARTUP_GUIDE.md` - Comprehensive startup guide
- `start_savorme_simple.bat` - Simple startup script
- `requirements.txt` - Dependencies
- `.env` - Environment variables

### **Configuration Files**
- **Environment**: `.env` (API keys and settings)
- **Dependencies**: `requirements.txt` (Python packages)
- **Startup**: `start_savorme_simple.bat` (Simple startup)
- **Documentation**: `CUSTOMIZATIONS_PERSISTENT.md` (Complete guide)

### **API Keys Required**
```env
EDAMAM_APP_ID=your_edamam_app_id
EDAMAM_APP_KEY=your_edamam_app_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

### **Quick Test**
1. Run `start_savorme_simple.bat`
2. Open http://localhost:5000
3. Complete user flow: Landing → Profile → Mood → Recipe
4. Test scoring transparency in nutrient analysis

### **New Features (v3.1.0)**
- **Recipe Match Score Transparency**: Weighted scoring with evidence-based weights
- **Data Source Transparency**: Edamam API + built-in nutrient database
- **Daily Intake Context**: Shows meal targets vs daily needs
- **Enhanced Scoring**: 88% vs 66% explained with nutrient breakdown

### **Troubleshooting**
- Check `.env` file for API keys
- Verify Python and virtual environment
- Review terminal logs for errors
- Use simple startup script for easier debugging

---

*This summary provides quick access to essential configuration information for the SavorMe project with enhanced scoring transparency.*
