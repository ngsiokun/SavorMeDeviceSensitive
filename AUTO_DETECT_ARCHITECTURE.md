# SavorMe Auto-Detect Architecture v4.0.0

## 🎯 Purpose
This document explains how SavorMe automatically detects whether a user is on desktop or mobile and serves the appropriate version, while keeping **frontend and backend completely SEPARATE** for easier debugging.

**Cross-References**:
- `MASTER_FILE_ORGANIZATION.md` - Complete file inventory
- `AUTOMATED_APP_STARTUP_GUIDE.md` - Startup procedures
- `app_router.py` - Device detection router implementation

---

## 🏗️ Architecture Overview

### The Problem
- Users shouldn't have to manually choose desktop vs mobile
- Desktop and mobile apps must stay SEPARATE for debugging
- Backend must be completely separate from frontend

### The Solution: Router Pattern
```
User Request
     ↓
app_router.py (Port 8080)
  │
  ├→ Detects: Desktop browser → http://localhost:5001 (desktop_app/)
  │
  └→ Detects: Mobile browser → http://localhost:5000 (demo_app/)
     
Both connect to: Backend API (Port 8000, app/)
```

### Why This Approach?
✅ **Complete Separation**: Each service runs independently
✅ **Easy Debugging**: Check the specific service's terminal window
✅ **Automatic Detection**: User gets correct version automatically
✅ **No File Mixing**: Desktop and mobile code never interact
✅ **Backend Independence**: API service completely separate

---

## 📂 File Structure (Separated)

```
SavorMeDeviceSensitive/
│
├── app/                          # BACKEND (Port 8000)
│   ├── main.py                   # FastAPI application
│   ├── api/routes.py            # API endpoints
│   └── services/                # Business logic
│
├── desktop_app/                  # DESKTOP FRONTEND (Port 5001)
│   ├── app.py                    # Desktop Flask app
│   ├── templates/desktop-*.html # Desktop templates
│   └── static/css/desktop-*.css # Desktop styles
│
├── demo_app/                     # MOBILE FRONTEND (Port 5000)
│   ├── app.py                    # Mobile Flask app
│   ├── templates/*.html         # Mobile templates
│   └── static/                  # Mobile assets
│
├── app_router.py                 # DEVICE ROUTER (Port 8080)
│   └── Device detection logic    # Routes to desktop or mobile
│
└── START-ALL-SEPARATE.bat       # Starts all 4 services separately
```

---

## 🔍 Device Detection Logic

### Location: `app_router.py`

### Detection Method
```python
def is_mobile_device(user_agent):
    """Detect if request is from mobile device"""
    mobile_keywords = [
        'mobile', 'android', 'iphone', 'ipad', 'ipod',
        'blackberry', 'windows phone', 'webos', 'opera mini',
        'tablet'
    ]
    user_agent_lower = user_agent.lower()
    return any(keyword in user_agent_lower for keyword in mobile_keywords)
```

### Routing Logic
```
IF User-Agent contains mobile keywords:
    → Redirect to http://localhost:5000 (Mobile)
ELSE:
    → Redirect to http://localhost:5001 (Desktop)
```

---

## 🚀 Startup Options

### Option 1: AUTO-DETECT (Recommended) ⭐
```cmd
START-ALL-SEPARATE.bat
```
**What it does**:
- Starts Backend (port 8000) in separate window
- Starts Mobile Frontend (port 5000) in separate window
- Starts Desktop Frontend (port 5001) in separate window
- Starts Device Router (port 8080) in separate window

**Access**: http://localhost:8080 (automatically routes to correct version)

**Advantages**:
- ✅ Automatic device detection
- ✅ All services separate for debugging
- ✅ Best for production-like testing
- ✅ Frontend/backend completely separated

### Option 2: Desktop Only
```cmd
START-BOTH-SERVICES.bat
```
- Backend (port 8000)
- Desktop Frontend (port 5001)

### Option 3: Mobile Only
```cmd
start.bat
(Choose option 3)
```
- Backend (port 8000)
- Mobile Frontend (port 5000)

### Option 4: Interactive Menu
```cmd
start.bat
```
Presents menu to choose from all options.

---

## 🐛 Debugging Strategy

### Service Separation for Debugging

| Issue Type | Check Window | Port | Service |
|------------|-------------|------|---------|
| **API errors** | Backend window | 8000 | app/main.py |
| **Desktop layout issues** | Desktop window | 5001 | desktop_app/app.py |
| **Mobile layout issues** | Mobile window | 5000 | demo_app/app.py |
| **Device detection issues** | Router window | 8080 | app_router.py |

### Example Debugging Scenarios

#### Scenario 1: Recipe not loading on desktop
1. Check **Desktop window** (port 5001) for errors
2. Check **Backend window** (port 8000) for API errors
3. Don't touch Mobile window - it's separate!

#### Scenario 2: Mobile layout broken
1. Check **Mobile window** (port 5000) for errors
2. Check **Backend window** (port 8000) if API issue
3. Don't touch Desktop window - it's separate!

#### Scenario 3: Wrong version showing
1. Check **Router window** (port 8080) - see detection logs
2. Check User-Agent being detected
3. Use `/api/device-info` endpoint to debug

---

## 🔌 Port Map

| Service | Port | Purpose | File |
|---------|------|---------|------|
| **Router** | 8080 | Auto-detect & route | `app_router.py` |
| **Desktop** | 5001 | Desktop frontend | `desktop_app/app.py` |
| **Mobile** | 5000 | Mobile frontend | `demo_app/app.py` |
| **Backend** | 8000 | API service | `app/main.py` |

---

## 📊 Data Flow

### User Journey with Auto-Detect
```
1. User visits http://localhost:8080
        ↓
2. Router checks User-Agent
        ↓
3. Router redirects to:
   - Desktop (5001) if desktop browser
   - Mobile (5000) if mobile browser
        ↓
4. Frontend loads appropriate templates
        ↓
5. Frontend calls Backend API (8000)
        ↓
6. Backend processes and returns data
        ↓
7. Frontend displays results
```

### Backend Communication (Both Frontends)
```
Desktop (5001) ──┐
                 ├──→ Backend API (8000)
Mobile (5000) ───┘
```

Both frontends connect to the same backend API independently.

---

## 🔑 Key Endpoints

### Router Endpoints (Port 8080)
- `GET /` - Auto-detect and route
- `GET /profile` - Auto-detect and route
- `GET /mood` - Auto-detect and route
- `GET /results` - Auto-detect and route
- `GET /health` - Health check
- `GET /api/device-info` - Debug device detection

### Frontend Endpoints (Ports 5000, 5001)
- `GET /` - Landing page
- `GET /profile` - Profile form
- `GET /mood` - Mood selection
- `GET /results` - Recipe results
- `POST /api/nutrition/calculate` - Proxy to backend
- `POST /api/recipes/recommend` - Proxy to backend

### Backend Endpoints (Port 8000)
- `GET /api/v1/health` - Health check
- `POST /api/v1/nutrition/calculate` - Calculate nutrition
- `POST /api/v1/mood/interpret` - Interpret mood
- `POST /api/v1/recipes/recommend` - Get recipe

---

## ✅ Separation Benefits

### 1. **Debugging Isolation**
- Desktop bug? Only check desktop_app/
- Mobile bug? Only check demo_app/
- API bug? Only check app/
- No confusion about which code is running

### 2. **Independent Development**
- Team A works on desktop
- Team B works on mobile
- Team C works on backend
- No code conflicts

### 3. **Easier Testing**
- Test desktop version directly (port 5001)
- Test mobile version directly (port 5000)
- Test backend directly (port 8000)
- Test routing separately (port 8080)

### 4. **Clear Logs**
- Each service has its own terminal window
- No mixed logs
- Easy to trace errors

---

## 📝 File Cross-References

| File | Purpose | References |
|------|---------|-----------|
| `app_router.py` | Device detection router | This document |
| `START-ALL-SEPARATE.bat` | Start all services | This document |
| `start.bat` | Interactive menu | This document, START-ALL-SEPARATE.bat |
| `desktop_app/app.py` | Desktop frontend | desktop_app/README.md |
| `demo_app/app.py` | Mobile frontend | demo_app/README.md |
| `app/main.py` | Backend API | AUTOMATED_APP_STARTUP_GUIDE.md |
| `MASTER_FILE_ORGANIZATION.md` | All files | This document |

---

## 🎯 Recommended Workflow

### For Development:
```cmd
START-ALL-SEPARATE.bat
```
- All services in separate windows
- Easy debugging
- Auto-detect enabled
- Access: http://localhost:8080

### For Desktop-Only Testing:
```cmd
START-BOTH-SERVICES.bat
```
- Backend + Desktop only
- Faster startup
- Access: http://localhost:5001

### For Mobile-Only Testing:
```cmd
start.bat → Choose option 3
```
- Backend + Mobile only
- Faster startup
- Access: http://localhost:5000

---

## 🔄 Migration from v3.x

### What Changed:
- **Old**: Manual choice between desktop and mobile
- **New**: Automatic device detection with router

### What Stayed the Same:
- Frontend and backend files (no code changes needed)
- API endpoints unchanged
- Port numbers for direct access unchanged
- Debugging approach improved

### New Files:
- `app_router.py` - Device router
- `START-ALL-SEPARATE.bat` - Startup script
- `AUTO_DETECT_ARCHITECTURE.md` - This document

---

**Version**: 4.0.0  
**Last Updated**: October 2025  
**Architecture**: Separate Services with Auto-Detection Router  
**Cross-Reference**: MASTER_FILE_ORGANIZATION.md

