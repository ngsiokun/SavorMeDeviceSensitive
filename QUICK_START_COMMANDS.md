# SavorMe - Quick Start Commands

## 🚀 Start Application (Copy & Paste These Commands)

### Terminal 1 - Backend:
```cmd
venv\Scripts\activate.bat
start_backend.bat
```

### Terminal 2 - Frontend:
```cmd
venv\Scripts\activate.bat
start_demo.bat
```

### Verify Both Running:
```cmd
curl -s http://localhost:8000/api/v1/health
curl -s -I http://localhost:5000
```

## 🌐 Application URLs
- **Main App**: http://localhost:5000
- **API Docs**: http://localhost:8000/docs

## 🔧 If Something Goes Wrong:

### Check Status:
```cmd
git status
netstat -an | findstr :5000
netstat -an | findstr :8000
```

### Kill All Python:
```cmd
taskkill /f /im python.exe
```

### Restart Everything:
```cmd
start_backend.bat
# Then in new terminal:
start_demo.bat
```

## ✅ Success Check:
1. Backend shows: "Application startup complete"
2. Frontend shows: "Running on http://127.0.0.1:5000"
3. Can access http://localhost:5000 in browser
4. Mood selection page works and button is functional
5. Evidence banner is green (not yellow)
6. Mood cards have colored borders (blue, red, purple, orange)

## 🎯 Current Working Features:
- ✅ 4 evidence-based moods (Stressed, Fatigued, Low Mood, Irritable)
- ✅ Green evidence banner with scientific research note
- ✅ Colored mood card borders for easy identification
- ✅ Working "Get My Recipe Recommendation" button
- ✅ Complete recipe results with all sections populated
- ✅ All API integrations functional

---
**Remember**: Always use Command Prompt (cmd), never PowerShell!
