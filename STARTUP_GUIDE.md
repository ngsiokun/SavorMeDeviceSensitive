# SavorMe Application - Complete Startup Guide

## 🚀 Quick Start (Always Use This Order)

### 1. Environment Setup
```cmd
# Activate virtual environment
venv\Scripts\activate.bat

# Verify Python version
py --version
```

### 2. Start Backend Server
```cmd
# Option 1: Use batch file
start_backend.bat

# Option 2: Manual command
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Start Frontend Server (In New Terminal)
```cmd
# Option 1: Use batch file
start_demo.bat

# Option 2: Manual command
cd demo_app
python app.py
```

### 4. Verify Both Servers Are Running
```cmd
# Check backend health
curl -s http://localhost:8000/api/v1/health

# Check frontend
curl -s -I http://localhost:5000
```

## 📱 Application URLs

- **Frontend (Main App)**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Troubleshooting Checklist

### If Backend Won't Start:
1. Check if port 8000 is free: `netstat -an | findstr :8000`
2. Verify .env file exists and has API keys
3. Check virtual environment is activated
4. Look for Python import errors in terminal

### If Frontend Won't Start:
1. Check if port 5000 is free: `netstat -an | findstr :5000`
2. Verify you're in the correct directory
3. Check if backend is running first
4. Look for Flask errors in terminal

### If API Calls Fail:
1. Verify both servers are running
2. Check backend logs for errors
3. Test API directly: `curl -s http://localhost:8000/api/v1/health`

## 📁 Key Files & Their Purpose

### Backend Files:
- `app/main.py` - FastAPI application entry point
- `app/api/routes.py` - All API endpoints
- `app/core/config.py` - Configuration and API keys
- `app/services/` - Business logic services
- `.env` - API keys and environment variables

### Frontend Files:
- `demo_app/app.py` - Flask application
- `demo_app/templates/` - HTML templates
- `demo_app/static/css/` - Stylesheets
- `demo_app/static/js/` - JavaScript files

### Configuration Files:
- `requirements.txt` - Backend dependencies
- `demo_app/requirements.txt` - Frontend dependencies
- `start_backend.bat` - Backend startup script
- `start_demo.bat` - Frontend startup script

## 🎨 Current UI Status (Last Updated)

### Landing Page:
- ✅ Dark teal-green hero section
- ✅ Green feature cards with glass effect
- ✅ "Start Your Journey" button working

### Profile Page:
- ✅ User input form working
- ✅ Session storage for profile data
- ✅ Navigation to mood selection

### Mood Selection Page:
- ✅ Green evidence banner (not yellow)
- ✅ Colored mood card borders:
  - Stressed: Blue (#3B82F6)
  - Fatigued: Red (#EF4444)
  - Low Mood: Purple (#8B5CF6)
  - Irritable: Orange (#F97316)
- ✅ Working "Get My Recipe Recommendation" button
- ✅ API integration functional

### Recipe Results Page:
- ✅ Complete recipe display
- ✅ All sections populated (match score, rationale, nutrition, evidence)
- ✅ Back navigation working

## 🔑 Required API Keys (.env file)

```bash
EDAMAM_APP_ID=f96cea5d
EDAMAM_APP_KEY=afb66c232e1090ece34618db1acc1136
OPENROUTER_API_KEY=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
CANVA_CLIENT_ID=OC-AZ18LZejb8u9
CANVA_CLIENT_SECRET=cnvcabIK0GL8IGLogkvCHxXKS862m3Uys_3rJFyW_7
```

## 🚨 Common Issues & Solutions

### Issue: "Python was not found"
**Solution**: Use `py` command instead of `python` or `python3`

### Issue: "UnboundLocalError: cannot access local variable 'requests'"
**Solution**: This was fixed - ensure you're using the latest committed version

### Issue: "Connection refused" errors
**Solution**: 
1. Start backend first, wait for "Application startup complete"
2. Then start frontend
3. Verify both are running on correct ports

### Issue: Button not working on mood selection
**Solution**: This was fixed - button should work when moods are selected

### Issue: Files reverting to old state
**Solution**: Always commit changes with:
```cmd
git add .
git commit -m "Description of changes"
git push origin main
```

## 📋 Pre-Flight Checklist (Run Before Each Test)

- [ ] Virtual environment activated
- [ ] .env file exists with API keys
- [ ] No uncommitted changes (`git status` shows clean)
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Both servers respond to health checks
- [ ] Can navigate through all pages
- [ ] Mood selection button works
- [ ] Recipe recommendation generates successfully

## 🎯 Success Indicators

✅ **Backend Healthy**: `{"status":"healthy","service":"SavorMe Backend"}`
✅ **Frontend Loading**: HTTP 200 response from localhost:5000
✅ **Mood Selection**: Can select moods and button enables
✅ **Recipe Generation**: API returns recipe data successfully
✅ **Navigation**: Can move between all pages smoothly

## 📞 Emergency Commands

### Kill All Python Processes:
```cmd
taskkill /f /im python.exe
```

### Check What's Using Ports:
```cmd
netstat -an | findstr :5000
netstat -an | findstr :8000
```

### Reset to Last Working State:
```cmd
git checkout -- .
```

### Force Restart Everything:
```cmd
# Kill processes
taskkill /f /im python.exe

# Restart backend
start_backend.bat

# In new terminal, restart frontend
start_demo.bat
```

---

**Last Updated**: October 5, 2025
**Status**: All systems functional and tested
**Next Steps**: Use this guide every time you start the application
