# SavorMe Repository Split Guide

This guide classifies all files into three categories:
1. **Backend Repository** - Files for SavorMe-backend
2. **Frontend Repository** - Files for SavorMe-frontend  
3. **Common** - Files needed in both repositories

---

## 🔧 BACKEND REPOSITORY FILES
**Repository**: `SavorMe-backend`

### Core Backend Application
```
app/
├── __init__.py
├── main.py
├── api/
│   ├── __init__.py
│   └── routes.py
├── core/
│   ├── __init__.py
│   └── config.py
├── models/
│   ├── __init__.py
│   ├── mood.py
│   ├── recipe.py
│   └── user.py
├── services/
│   ├── __init__.py
│   ├── edamam_client.py
│   ├── fusion_engine.py
│   ├── mood_nutrition_engine.py
│   ├── nutrition_calculator.py
│   └── openrouter_client.py
└── data/
    ├── __init__.py
    └── mood_mapping.json
```

### Backend Root Files
```
main.py                          # Legacy entry point (can be removed)
requirements.txt                 # Python backend dependencies
.env                            # Environment variables (API keys)
start_backend.bat               # Backend server start script
.gitignore                      # Git ignore rules
```

### Backend Documentation
```
README.md                        # Main project README (backend-focused)
QUICK_START_GUIDE.md            # How to run the backend
MAPPING_STRATEGY.md             # Technical mapping architecture
EVIDENCE_BASED_MOODS_v2.md      # Mood system documentation
MOOD_TO_RECIPE_FLOW.md          # Complete flow documentation
SYSTEM_DESIGN_FINAL.md          # Final system design
IMPLEMENTATION_ROADMAP.md       # Development roadmap
MAPPING_DATA_SOURCES.md         # Data source documentation
```

---

## 🎨 FRONTEND REPOSITORY FILES
**Repository**: `SavorMe-frontend`

### Demo App (Frontend)
```
demo_app/
├── app.py                      # Flask frontend server
├── requirements.txt            # Python frontend dependencies
├── README.md                   # Frontend-specific README
├── templates/
│   ├── index.html             # Landing page
│   ├── profile.html           # User profile form
│   ├── mood_selection.html    # Mood selection UI
│   └── recipe_result.html     # Recipe display page
└── static/
    ├── css/
    │   ├── main.css           # Global styles
    │   ├── profile.css        # Profile page styles
    │   └── results.css        # Results page styles
    └── js/
        ├── mood_selection.js  # Mood selection logic
        ├── profile.js         # Profile form logic
        └── recipe_result.js   # Recipe display logic
```

### Frontend Root Files
```
start_demo.bat                  # Demo app start script
.gitignore                      # Git ignore rules (same as backend)
```

### Frontend Documentation
```
README.md                       # Frontend-specific README
FRONTEND_UPDATE_GUIDE.md        # Guide for updating frontend
RUN_DEMO_INSTRUCTIONS.md        # How to run the demo
```

---

## 📚 COMMON FILES (Both Repositories)

These files should exist in **BOTH** repositories with the same content:

### Documentation (Keep in Both)
```
EVIDENCE_BASED_MOODS_v2.md      # Explains the 4 mood system
MOOD_TO_RECIPE_FLOW.md          # Shows complete user flow
```

### Environment Setup (Adapted per Repository)
```
.gitignore                      # Same for both
.env.example                    # Template for environment variables
```

### README Files (Different Content)
```
README.md                       # Backend: Focus on API setup
                               # Frontend: Focus on demo app setup
```

---

## 📋 RECOMMENDED REPOSITORY STRUCTURE

### Backend Repository (`SavorMe-backend`)
```
SavorMe-backend/
├── app/                        # FastAPI application
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   └── data/
├── docs/                       # Documentation folder
│   ├── EVIDENCE_BASED_MOODS_v2.md
│   ├── MOOD_TO_RECIPE_FLOW.md
│   ├── MAPPING_STRATEGY.md
│   ├── SYSTEM_DESIGN_FINAL.md
│   └── IMPLEMENTATION_ROADMAP.md
├── main.py
├── requirements.txt
├── start_backend.bat
├── .env.example
├── .gitignore
└── README.md                   # Backend setup & API docs
```

### Frontend Repository (`SavorMe-frontend`)
```
SavorMe-frontend/
├── templates/                  # HTML templates
│   ├── index.html
│   ├── profile.html
│   ├── mood_selection.html
│   └── recipe_result.html
├── static/                     # CSS & JS assets
│   ├── css/
│   └── js/
├── docs/                       # Shared documentation
│   ├── EVIDENCE_BASED_MOODS_v2.md
│   └── MOOD_TO_RECIPE_FLOW.md
├── app.py                      # Flask server
├── requirements.txt
├── start_demo.bat
├── .env.example
├── .gitignore
└── README.md                   # Frontend setup & demo instructions
```

---

## 🚀 MIGRATION STEPS

### Step 1: Create Frontend Repository
```bash
# Create new directory
mkdir SavorMe-frontend
cd SavorMe-frontend

# Initialize git
git init
git remote add origin https://github.com/YOUR_USERNAME/SavorMe-frontend.git

# Copy frontend files
# (See FRONTEND REPOSITORY FILES section above)

# Create initial commit
git add .
git commit -m "Initial frontend setup with Flask demo app"
git push -u origin main
```

### Step 2: Clean Backend Repository
```bash
cd SavorMe-1

# Remove frontend-only files
rm -rf demo_app/
rm start_demo.bat
rm RUN_DEMO_INSTRUCTIONS.md
rm FRONTEND_UPDATE_GUIDE.md

# Organize documentation
mkdir docs
mv *.md docs/
mv docs/README.md ./

# Commit cleanup
git add .
git commit -m "Restructure as backend-only repository"
git push origin main
```

### Step 3: Update README Files

**Backend README**: Focus on:
- API endpoints
- Environment setup
- Running the FastAPI server
- API documentation

**Frontend README**: Focus on:
- Demo app features
- Running the Flask server
- Connecting to backend
- UI screenshots

---

## 🔗 CROSS-REPOSITORY COMMUNICATION

### Backend Configuration
The frontend needs to know the backend URL:
```python
# frontend .env
BACKEND_URL=http://localhost:8000
```

### Frontend Configuration
The backend should allow CORS for frontend:
```python
# backend app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 NOTES

1. **Virtual Environments**: Each repository should have its own `venv/` (already in `.gitignore`)
2. **API Keys**: Both repos need `.env` files with appropriate keys
3. **Documentation**: Keep core concept docs (moods, flow) in both repos for reference
4. **Dependencies**: Separate `requirements.txt` for backend (FastAPI) and frontend (Flask)
5. **Start Scripts**: Each repo has its own start script (`start_backend.bat` vs `start_demo.bat`)

---

## ✅ CHECKLIST

- [ ] Create `SavorMe-frontend` repository on GitHub
- [ ] Copy frontend files to new repo
- [ ] Remove frontend files from backend repo
- [ ] Update both README files
- [ ] Test backend independently
- [ ] Test frontend with backend
- [ ] Update `.env.example` in both repos
- [ ] Add CORS middleware to backend
- [ ] Update documentation links


