# SavorMe Application - Page Layouts & File Structure Reference

## Overview
This document provides a complete reference of all page layouts, file structures, and configurations for the SavorMe application to ensure consistency and prevent getting lost in future development sessions.

## Application Architecture

### Backend (FastAPI)
- **Main File**: `app/main.py`
- **API Routes**: `app/api/routes.py`
- **Configuration**: `app/core/config.py`
- **Services**: `app/services/`
- **Models**: `app/models/`
- **Start Command**: `start_backend.bat` or `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
- **URL**: http://localhost:8000

### Frontend (Flask Demo App)
- **Main File**: `demo_app/app.py`
- **Templates**: `demo_app/templates/`
- **Static Files**: `demo_app/static/`
- **Start Command**: `start_demo.bat` or `python demo_app/app.py`
- **URL**: http://localhost:5000

## Page Layouts & Templates

### 1. Landing Page (`demo_app/templates/index.html`)
**Design**: Dark teal hero section with 2x2 feature grid
**Key Elements**:
- Hero section with gradient background
- Main heading: "Discover Recipes That Match Your Mood"
- Subheading: "Get personalized recipe recommendations based on your emotional state and nutritional needs"
- 2x2 feature grid:
  - Mood-Based Recommendations
  - Nutritional Intelligence
  - Personalized Profiles
  - Evidence-Based Science
- "Get Started" button linking to `/profile`

**CSS**: `demo_app/static/css/main.css`
- `.hero-section` with gradient background
- `.features-section` with 2x2 grid layout
- `.feature-card` styling with hover effects

### 2. Profile Page (`demo_app/templates/profile.html`)
**Design**: Clean form layout with user input fields
**Key Elements**:
- Personal Information section (age, gender, height, weight)
- Cuisine Preferences (multi-select)
- Food Allergies (multi-select)
- Dietary Preference (dropdown)
- Calorie Preference (radio buttons with custom input)
- "Continue to Mood Selection" button

**CSS**: `demo_app/static/css/profile.css`
**JavaScript**: `demo_app/static/js/profile.js`
- Form validation and data persistence
- Dynamic calorie preference handling

### 3. Mood Selection Page (`demo_app/templates/mood_selection.html`)
**Design**: Mood cards with intensity selection
**Key Elements**:
- Mood cards in grid layout (happy, sad, stressed, energetic, calm, anxious, excited, tired)
- Intensity selection (low, medium, high)
- Evidence banner at top
- "Get Recipe Recommendations" button
- Loading spinner during API calls

**CSS**: `demo_app/static/css/mood_selection.css`
**JavaScript**: `demo_app/static/js/mood_selection.js`
- Mood and intensity selection logic
- API integration with backend

### 4. Recipe Result Page (`demo_app/templates/recipe_result.html`)
**Design**: Comprehensive recipe display with multiple sections
**Key Elements**:
- Recipe card with image, name, and basic info
- Match score display
- Rationale section explaining mood-nutrition connection
- Nutrition information
- Evidence section with scientific backing
- Action buttons (Save Recipe, Try Another, Back to Moods)
- Cooking directions

**CSS**: `demo_app/static/css/results.css`
**JavaScript**: `demo_app/static/js/recipe_result.js`
- Dynamic content population
- Navigation functions

## File Structure

```
SavorMe-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI main application
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py              # All API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Configuration settings
│   ├── data/
│   │   ├── __init__.py
│   │   └── mood_mapping.json      # Mood mapping data
│   ├── models/
│   │   ├── __init__.py
│   │   ├── mood.py                # Mood models
│   │   ├── recipe.py              # Recipe models
│   │   └── user.py                # User models
│   └── services/
│       ├── __init__.py
│       ├── canva_client.py        # Canva API integration
│       ├── edamam_client.py       # Edamam API client
│       ├── fusion_engine.py       # Recipe fusion logic
│       ├── mood_nutrition_engine.py # Mood-nutrition mapping
│       ├── nutrition_calculator.py # Nutrition calculations
│       └── openrouter_client.py   # OpenRouter AI client
├── demo_app/
│   ├── app.py                     # Flask demo application
│   ├── requirements.txt           # Frontend dependencies
│   ├── templates/
│   │   ├── index.html             # Landing page
│   │   ├── profile.html           # User profile form
│   │   ├── mood_selection.html    # Mood selection interface
│   │   └── recipe_result.html     # Recipe results display
│   └── static/
│       ├── css/
│       │   ├── main.css           # Global styles + landing page
│       │   ├── profile.css        # Profile page styles
│       │   ├── mood_selection.css # Mood selection styles
│       │   └── results.css        # Recipe results styles
│       └── js/
│           ├── profile.js         # Profile form logic
│           ├── mood_selection.js  # Mood selection logic
│           └── recipe_result.js   # Recipe results logic
├── .env                           # Environment variables
├── requirements.txt               # Backend dependencies
├── start_backend.bat             # Backend startup script
├── start_demo.bat                # Frontend startup script
└── README.md                     # Project documentation
```

## Environment Configuration

### Required API Keys (`.env` file)
```bash
EDAMAM_APP_ID=your_edamam_app_id
EDAMAM_APP_KEY=your_edamam_app_key
OPENROUTER_API_KEY=your_openrouter_api_key
CANVA_CLIENT_ID=your_canva_client_id
CANVA_CLIENT_SECRET=your_canva_client_secret
CANVA_ACCESS_TOKEN=your_canva_access_token
```

## Key API Endpoints

### Backend (FastAPI)
- `GET /docs` - API documentation
- `POST /api/v1/recipes/recommend` - Get recipe recommendations
- `POST /api/v1/nutrition/calculate` - Calculate nutrition
- `POST /api/v1/mood/interpret` - Interpret mood data
- `GET /api/v1/health` - Health check

### Frontend (Flask)
- `GET /` - Landing page
- `GET /profile` - Profile form
- `GET /mood-selection` - Mood selection
- `GET /recipe-result` - Recipe results
- `POST /api/recommend` - Proxy to backend recommendation API

## Startup Commands

### Backend
```bash
# Using batch file
start_backend.bat

# Or directly
venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend
```bash
# Using batch file
start_demo.bat

# Or directly
cd demo_app
python app.py
```

## Design Specifications

### Color Scheme
- Primary: Dark teal (#2C5F5F)
- Secondary: Light teal (#4A9B9B)
- Accent: Orange (#FF6B35)
- Background: Light gray (#F8F9FA)
- Text: Dark gray (#333333)

### Typography
- Headings: Bold, larger font sizes
- Body text: Regular weight, readable font sizes
- Buttons: Bold, uppercase text

### Layout Principles
- Responsive design for mobile and desktop
- Clean, minimal interface
- Consistent spacing and alignment
- Clear visual hierarchy
- Intuitive navigation flow

## Data Flow

1. **User Profile** → Profile form collects user data
2. **Mood Selection** → User selects mood and intensity
3. **API Call** → Frontend sends data to backend
4. **Backend Processing** → Mood-nutrition engine processes request
5. **Recipe Search** → Edamam API searches for recipes
6. **AI Enhancement** → OpenRouter AI enhances recommendations
7. **Results Display** → Frontend displays comprehensive results

## Common Issues & Solutions

### Backend Issues
- **Import Errors**: Check `from typing import` statements
- **API Key Issues**: Verify `.env` file format and encoding
- **Port Conflicts**: Ensure port 8000 is available

### Frontend Issues
- **Template Not Found**: Check file paths in `demo_app/templates/`
- **CSS Not Loading**: Use `{{ url_for('static', filename='...') }}`
- **JavaScript Errors**: Check function names match HTML onclick calls

### Environment Issues
- **Python Not Found**: Use `py` command instead of `python`
- **Virtual Environment**: Use `py -m venv venv` to create
- **Activation**: Use `venv\Scripts\activate.bat` in Command Prompt

## Git Repository
- **Remote URL**: https://github.com/yourusername/SavorMe-backend.git
- **Main Branch**: main
- **Status**: All files committed and pushed

## Current Working State (October 5, 2025)

### ✅ All Critical Issues Resolved:
1. **API Import Error**: Fixed duplicate `import requests` in `demo_app/app.py`
2. **Mood Selection Colors**: Evidence banner now uses green theme (not yellow)
3. **Mood Card Borders**: Each mood has specific colored borders:
   - Stressed: Blue (#3B82F6)
   - Fatigued: Red (#EF4444) 
   - Low Mood: Purple (#8B5CF6)
   - Irritable: Orange (#F97316)
4. **Button Functionality**: "Get My Recipe Recommendation" button works properly
5. **File Persistence**: All changes committed and pushed to GitHub

### ✅ Verified Working Features:
- Landing page with teal-green hero and feature grid
- Profile page with form validation and session storage
- Mood selection with colored cards and working button
- Recipe results with complete data display
- Backend API returning proper recipe recommendations
- Frontend-backend communication working

### ✅ Documentation Created:
- `STARTUP_GUIDE.md` - Comprehensive startup and troubleshooting guide
- `QUICK_START_COMMANDS.md` - Quick reference commands
- `PAGE_LAYOUTS_REFERENCE.md` - Complete layout reference

## Next Steps for Development
1. ✅ Test all page flows end-to-end - COMPLETED
2. ✅ Implement error handling and validation - COMPLETED
3. ✅ Add loading states and user feedback - COMPLETED
4. ✅ Optimize API response times - COMPLETED
5. Add unit tests for critical functions
6. Implement user authentication
7. Add recipe saving and favorites functionality

---

**Last Updated**: October 5, 2025
**Status**: Fully functional application with complete frontend-backend integration - ALL ISSUES RESOLVED
