# SavorMe Desktop Application

## 🖥️ Overview
The SavorMe Desktop Application is a **separate, optimized version** of SavorMe designed for desktop and laptop screens (1024px and wider). It provides an enhanced user experience with improved layouts, better spacing, and desktop-optimized interactions.

**⚠️ IMPORTANT**: This is a **SEPARATE application** from the mobile version (`demo_app/`). Do not mix files between the two applications to avoid debugging nightmares.

---

## 📁 File Structure

```
desktop_app/
├── app.py                     # Flask application (Port 5001)
├── requirements.txt           # Desktop-specific dependencies
├── README.md                  # This file
├── templates/                 # Desktop HTML templates
│   ├── desktop-index.html    # Landing page
│   ├── desktop-profile.html  # Profile/nutrition form
│   ├── desktop-mood.html     # Mood selection
│   └── desktop-results.html  # Recipe results
└── static/css/               # Desktop stylesheets
    ├── desktop-main.css      # Base styles
    ├── desktop-landing.css   # Landing page styles
    ├── desktop-profile.css   # Profile page styles
    ├── desktop-mood.css      # Mood selection styles
    └── desktop-results.css   # Results page styles
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Virtual environment set up (from root directory)
- Backend service running on port 8000

### ⚠️ CRITICAL: Shell Requirement
```
ALWAYS USE: Command Prompt (cmd.exe)
NEVER USE: PowerShell (causes syntax errors with && operator)
```

### Starting Desktop App + Backend

**Option 1: Start Both Services (Recommended)**
```cmd
cd C:\Users\Samsung\savorme-cloud-run\SavorMeDeviceSensitive
START-BOTH-SERVICES.bat
```
This starts:
- Backend on port 8000
- Desktop app on port 5001

**Option 2: Start Desktop App Only**
```cmd
cd C:\Users\Samsung\savorme-cloud-run\SavorMeDeviceSensitive
start-desktop-only.bat
```

**Option 3: Manual Start**
```cmd
cd C:\Users\Samsung\savorme-cloud-run\SavorMeDeviceSensitive\desktop_app
..\venv\Scripts\python.exe app.py
```

### Access Points
- **Desktop App**: http://localhost:5001
- **Backend API**: http://127.0.0.1:8000
- **Mobile App**: http://localhost:5000 (separate)

---

## 🎨 Key Features

### Desktop-Specific Optimizations
1. **Wider Layouts**: Optimized for screens 1024px+
2. **Enhanced Spacing**: Better use of screen real estate
3. **Improved Typography**: Larger, more readable fonts
4. **Better Navigation**: Desktop-optimized header and navigation
5. **Full-Width Recipe Cards**: Single, detailed recipe display
6. **Medical Disclaimers**: Comprehensive legal notices
7. **Smooth Transitions**: No popup alerts, smooth page transitions

### Pages
1. **Landing Page** (`/`)
   - Desktop hero section
   - Feature grid
   - Medical disclaimer section
   
2. **Profile Page** (`/profile`)
   - User information form
   - Nutrition targets calculation
   - Cuisine preferences with "Surprise Me" logic
   - Smooth backend connection

3. **Mood Selection** (`/mood`)
   - Multi-select mood interface (up to 3 moods)
   - Intensity levels
   - Visual feedback

4. **Results Page** (`/results`)
   - Full-width recipe card
   - High-quality food images (object-fit: cover)
   - Ingredients with decimal formatting (max 2 decimals)
   - Cooking steps (filtered, no title steps)
   - Nutrient Match Score Summary modal
   - Medical disclaimer
   - "Save Recipe" functionality

---

## 🔧 Technical Architecture

### Backend Connection
The desktop app is a **Flask frontend** that connects to the **FastAPI backend**:

```python
BACKEND_URL = "http://127.0.0.1:8000"

# API Endpoints used:
# - POST /api/v1/nutrition/calculate
# - POST /api/v1/mood/interpret
# - POST /api/v1/recipes/recommend
```

### Data Flow
```
User Input (Profile) 
    → POST /api/nutrition/calculate 
    → Store in sessionStorage
    
User Input (Mood)
    → Store in sessionStorage
    
Results Page Load
    → Retrieve sessionStorage data
    → Transform to backend format
    → POST /api/recipes/recommend
    → Display recipe
```

### Session Storage Keys
- `desktopProfileData` - User profile information
- `desktopMoodData` - Selected moods and intensities
- `desktopRequestData` - Combined request data for API
- `savedRecipes` - Saved recipes (localStorage)

---

## 🎯 Desktop vs Mobile Differences

| Feature | Desktop App | Mobile App |
|---------|-------------|------------|
| **Port** | 5001 | 5000 |
| **File Prefix** | `desktop-*` | No prefix |
| **Layout** | Single column, wider | Multi-column, responsive |
| **Recipe Display** | Full-width card | Card grid |
| **Image Size** | 450px height | Smaller, responsive |
| **Navigation** | Desktop header | Mobile-optimized |
| **Spacing** | Generous (24px+) | Compact (12-16px) |
| **Font Sizes** | Larger (16-20px base) | Smaller (14-16px base) |

**⚠️ CRITICAL**: Keep these apps SEPARATE. Do not copy files between them. If you need to debug one, focus on its specific directory only.

---

## 🐛 Debugging

### Common Issues

**Issue 1: "Cannot connect to backend"**
```cmd
# Solution: Ensure backend is running
start-backend-only.bat

# Test backend health
curl http://127.0.0.1:8000/api/v1/health
```

**Issue 2: "PowerShell syntax error"**
```
Error: The token '&&' is not a valid statement separator
```
```cmd
# Solution: Use Command Prompt, not PowerShell
# Right-click Start → Command Prompt (or Run → cmd)
```

**Issue 3: "Port 5001 already in use"**
```cmd
# Solution: Kill existing processes
cleanup-processes.bat

# Or manually:
netstat -ano | findstr :5001
taskkill /PID <process_id> /F
```

**Issue 4: "Recipe image not loading"**
- Check browser console (F12) for errors
- Verify backend is returning image URLs
- Check `desktop-results.html` image styling

**Issue 5: "Ingredients show many decimals"**
- Fixed in v4.0.0 with decimal formatter
- Check `desktop-results.html` lines 339-358

### Debug Logs
```cmd
# Desktop app logs appear in terminal where you ran START-BOTH-SERVICES.bat
# Backend logs appear in separate backend terminal window
```

---

## 📋 File Cross-References

**Master Documentation**:
- `MASTER_FILE_ORGANIZATION.md` - Lists all desktop app files
- `README.md` (root) - Project overview
- `API_SCHEMA_REFERENCE.md` - Backend API format
- `EDAMAM_JSON_FORMAT.md` - Edamam API response format

**Related Scripts**:
- `START-BOTH-SERVICES.bat` - Start both services
- `start-desktop-only.bat` - Desktop app only
- `start-backend-only.bat` - Backend only
- `cleanup-processes.bat` - Kill all processes
- `restart-desktop.bat` - Restart desktop app
- `test-connection.bat` - Test connectivity

---

## 🔐 Medical Disclaimers

The desktop app includes **three** medical disclaimer locations:

1. **Landing Page**: Comprehensive disclaimer before footer
2. **Results Page**: Disclaimer after action buttons
3. **Nutrient Modal**: Disclaimer in match score summary

These disclaimers state that SavorMe is for **supporting healthy eating habits** and is **NOT intended for medical purposes**.

---

## 🎨 Styling Guide

### CSS Variables
```css
:root {
    --desktop-primary: #0F766E;
    --desktop-primary-hover: #0D9488;
    --desktop-text-primary: #1F2937;
    --desktop-text-secondary: #6B7280;
    --desktop-background: #F9FAFB;
    --desktop-border: #E5E7EB;
    --desktop-spacing-sm: 8px;
    --desktop-spacing-md: 16px;
    --desktop-spacing-lg: 24px;
    --desktop-spacing-xl: 32px;
}
```

### Breakpoints
- **Desktop**: 1024px and above
- **Tablet**: 768px - 1023px (responsive adjustments)
- **Mobile**: Below 768px (use mobile app instead)

---

## 🚀 Deployment Notes

### Local Development
- Desktop app runs on port 5001
- Uses same backend as mobile app (port 8000)
- No separate deployment needed for local testing

### Production Considerations
- Consider serving desktop and mobile from same domain with responsive design
- Or maintain separate deployments with different URLs
- Current setup: Local development only

---

## 📝 Version History

### v4.0.0 (October 2025) - Desktop App Release
- ✅ Separate desktop application created
- ✅ Desktop-optimized layouts and spacing
- ✅ Medical disclaimers added (3 locations)
- ✅ Decimal formatting for ingredients (max 2 decimals)
- ✅ Filtered cooking steps (no title steps)
- ✅ Full-width recipe card design
- ✅ Smooth page transitions (no alert popups)
- ✅ "Surprise Me" cuisine preference logic
- ✅ Recipe save functionality (localStorage)
- ✅ Nutrient Match Score Summary modal
- ✅ Enhanced food image display (object-fit: cover, 450px)

---

## 📞 Support & Contact

For issues or questions:
1. Check `MASTER_FILE_ORGANIZATION.md`
2. Review `BACKEND_TROUBLESHOOTING_FOR_GEMINI.md`
3. Check backend terminal for errors
4. Verify Command Prompt is being used (not PowerShell)

---

**Last Updated**: October 2025  
**Maintained By**: SavorMe Development Team  
**Cross-Reference**: `MASTER_FILE_ORGANIZATION.md` Section 1.4 (Frontend Applications)
