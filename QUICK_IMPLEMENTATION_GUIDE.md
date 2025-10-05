# SavorMe Quick Implementation Guide

## 🚀 **Quick Start - Create Complete App**

### **Step 1: Backend Setup (5 minutes)**
```bash
# Create backend structure
mkdir -p app/{api,core,models,services,data}
touch app/__init__.py app/main.py app/api/__init__.py app/api/routes.py
touch app/core/__init__.py app/core/config.py
touch app/models/__init__.py app/models/{user,recipe,mood}.py
touch app/services/__init__.py app/services/{edamam_client,openrouter_client,mood_nutrition_engine,fusion_engine,nutrition_calculator}.py
touch app/data/mood_mapping.json

# Install dependencies
pip install fastapi uvicorn python-dotenv requests pydantic pydantic-settings
```

### **Step 2: Frontend Setup (5 minutes)**
```bash
# Create frontend structure
mkdir -p demo_app/{templates,static/{css,js}}
touch demo_app/app.py
touch demo_app/templates/{index,profile,mood_selection,recipe_result}.html
touch demo_app/static/css/{main,landing,profile,mood_selection,results,recipe_results}.css
touch demo_app/static/js/{profile,mood_selection,recipe_result}.js

# Install dependencies
pip install flask requests
```

### **Step 3: Copy Core Files**
Copy the following files from the existing implementation:
- `app/main.py` - FastAPI application
- `app/api/routes.py` - API endpoints
- `app/core/config.py` - Configuration
- `app/models/*.py` - Data models
- `app/services/*.py` - Service implementations
- `app/data/mood_mapping.json` - Mood mapping data
- `demo_app/app.py` - Flask application
- All HTML templates from `demo_app/templates/`
- All CSS files from `demo_app/static/css/`
- All JavaScript files from `demo_app/static/js/`

### **Step 4: Environment Setup**
```bash
# Create .env file
echo "# SavorMe Backend Environment Variables" > .env
echo "EDAMAM_APP_ID=your_edamam_app_id" >> .env
echo "EDAMAM_APP_KEY=your_edamam_app_key" >> .env
echo "OPENROUTER_API_KEY=your_openrouter_api_key" >> .env
echo "CORS_ORIGINS=http://localhost:5000,http://127.0.0.1:5000" >> .env
```

### **Step 5: Start Applications**
```bash
# Terminal 1 - Backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2 - Frontend
cd demo_app && python app.py
```

### **Step 6: Verify Installation**
1. Open http://localhost:5000 - Landing page should load
2. Click "Start Your Journey" - Profile page should load
3. Fill profile and continue - Mood selection should load
4. Select mood and get recommendation - Recipe should display with cooking directions

## 🔧 **Key Implementation Points**

### **Backend API Structure**
```
POST /api/v1/recipes/recommend
{
  "mood_blend": {
    "moods": [{"mood": "fatigued", "intensity": "very"}]
  },
  "user_profile": {
    "age": 32,
    "gender": "female",
    "height_cm": 165,
    "weight_kg": 60,
    "cuisine_preferences": ["Mediterranean"]
  }
}
```

### **Frontend Flow**
1. **Landing Page** → Profile setup
2. **Profile Page** → Mood selection
3. **Mood Selection** → Recipe recommendation
4. **Recipe Results** → Display with cooking directions

### **Critical Components**
- **Cooking Directions**: AI-generated or fallback based on ingredients
- **Mood Mapping**: Maps moods to nutritional requirements
- **Mobile Design**: Responsive, mobile-first layout
- **Error Handling**: Graceful fallbacks for API failures

## 📋 **Verification Checklist**
- [ ] Backend starts on port 8000
- [ ] Frontend starts on port 5000
- [ ] Landing page loads with correct design
- [ ] Profile form submission works
- [ ] Mood selection interface functions
- [ ] Recipe recommendations generate
- [ ] Cooking directions appear
- [ ] "New Suggestions" button works
- [ ] Mobile responsive design
- [ ] Error handling works

## 🎯 **Success Criteria**
- Complete user flow from landing to recipe results
- Cooking directions always appear (AI or fallback)
- Mobile-first responsive design
- Professional error handling
- Fast loading times (< 2 seconds per page)

---

*This guide provides the fastest path to implement the complete SavorMe application with all features working.*
