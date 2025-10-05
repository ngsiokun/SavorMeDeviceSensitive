# SavorMe Master Guide - Complete Application Reference

## 🎯 **Purpose**
This is the single, comprehensive guide for the SavorMe application. It consolidates all essential information from multiple documentation files into one authoritative source.

---

## 📋 **Table of Contents**
1. [Quick Start](#quick-start)
2. [System Architecture](#system-architecture)
3. [File Organization](#file-organization)
4. [Setup & Installation](#setup--installation)
5. [Application Features](#application-features)
6. [Technical Implementation](#technical-implementation)
7. [Troubleshooting](#troubleshooting)
8. [Maintenance](#maintenance)

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- Git
- Command Prompt (Windows)

### **One-Command Setup**
```cmd
savorme_professional_startup.bat
```

### **Manual Setup** (if needed)
```cmd
# 1. Setup environment
setup_new_clone.bat

# 2. Start backend
start_savorme_reliable.bat

# 3. Start frontend (new terminal)
cd demo_app && ..\venv\Scripts\activate.bat && python app.py
```

### **Access Points**
- **Frontend**: http://localhost:5000
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

---

## 🏗️ **System Architecture**

### **Overall Structure**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   External APIs │
│   (Flask)       │◄──►│   (FastAPI)     │◄──►│   (Edamam, AI)  │
│   Port: 5000    │    │   Port: 8000    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Technology Stack**
- **Backend**: FastAPI + Uvicorn
- **Frontend**: Flask + Jinja2 + Custom CSS
- **External APIs**: Edamam Recipe API, OpenRouter AI API
- **Design**: Mobile-first, responsive

---

## 📁 **File Organization**

### **Essential Files** (Never Delete)
```
app/                           # Backend application
├── main.py                   # FastAPI entry point
├── api/routes.py             # API endpoints
├── core/config.py            # Configuration
├── models/                   # Data models
├── services/                 # Business logic
└── data/mood_mapping.json    # Mood data

demo_app/                     # Frontend application
├── app.py                    # Flask entry point
├── templates/                # HTML templates
├── static/css/               # Stylesheets
└── static/js/                # JavaScript

savorme_professional_startup.bat  # Main startup script
requirements.txt              # Dependencies
.env                         # Environment variables
```

### **Documentation Files** (Reference)
```
SAVORME_MASTER_GUIDE.md           # This file - Complete reference
TECHNICAL_SPECIFICATION_COMPLETE.md # Technical details
CUSTOMIZATIONS_PERSISTENT.md      # Design system
README.md                         # Project overview
```

---

## ⚙️ **Setup & Installation**

### **Environment Setup**
1. **Clone Repository**
   ```cmd
   git clone <repository-url>
   cd SavorMe-backend-1
   ```

2. **Create Virtual Environment**
   ```cmd
   py -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```cmd
   # Create .env file with your API keys
   EDAMAM_APP_ID=your_edamam_app_id
   EDAMAM_APP_KEY=your_edamam_app_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

### **Startup Options**

#### **Option 1: Professional Startup** (Recommended)
```cmd
savorme_professional_startup.bat
```

#### **Option 2: Reliable Startup**
```cmd
start_savorme_reliable.bat
```

#### **Option 3: Manual Startup**
```cmd
# Terminal 1 - Backend
venv\Scripts\activate
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2 - Frontend
cd demo_app
..\venv\Scripts\activate
python app.py
```

---

## 🎨 **Application Features**

### **User Flow**
1. **Landing Page** → Mobile-first design with hero section and feature grid
2. **Profile Setup** → User demographics and preferences
3. **Mood Selection** → Select current mood and intensity
4. **Recipe Results** → Personalized recipe with cooking directions

### **Key Features**
- **Mood-Based Recommendations**: Maps moods to nutritional needs
- **AI Cooking Directions**: Generated or intelligent fallback
- **Mobile-First Design**: Responsive, smartphone-optimized
- **Professional Error Handling**: Graceful fallbacks and user feedback
- **Session Management**: Maintains user data across pages

### **Design System**
- **Colors**: Dark teal (#0F766E) to dark green (#065F46)
- **Typography**: System fonts with clear hierarchy
- **Layout**: Mobile-first, vertical stacking
- **Effects**: Glassmorphic cards with backdrop blur

---

## 🔧 **Technical Implementation**

### **Backend API Endpoints**
```python
# Health Check
GET /api/v1/health

# Recipe Recommendation
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

### **Frontend-Backend Integration**
```javascript
// API Communication
fetch('/api/recommend', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(requestData)
})
.then(response => response.json())
.then(data => {
  // Handle response
  sessionStorage.setItem('recipeResult', JSON.stringify(data));
  window.location.href = '/recipe-result';
})
.catch(error => {
  // Error handling
  console.error('Error:', error);
});
```

### **Cooking Directions System**
```python
# AI-Generated Directions (when API available)
async def generate_cooking_directions(recipe_name, ingredients, cuisine_type):
    # Call OpenRouter AI API
    # Generate step-by-step instructions
    
# Fallback Directions (when API unavailable)
def _generate_fallback_directions(recipe_name, ingredients, cuisine_type):
    # Analyze ingredients
    # Generate appropriate cooking steps
    # Return 5-6 practical steps
```

---

## 🔍 **Troubleshooting**

### **Common Issues**

#### **1. Backend Won't Start**
```cmd
# Check Python installation
python --version

# Check virtual environment
venv\Scripts\activate
python -c "import fastapi"

# Check dependencies
pip install -r requirements.txt
```

#### **2. Frontend Won't Load**
```cmd
# Check Flask installation
pip install flask

# Check port availability
netstat -an | findstr :5000
```

#### **3. API Errors**
- Check `.env` file for API keys
- Verify API key validity
- Check network connectivity
- Review error logs in terminal

#### **4. Cooking Directions Missing**
- Verify OpenRouter API key in `.env`
- Check fallback system is working
- Review `openrouter_client.py` logs

### **Error Codes**
- **422**: Invalid request data
- **401**: Unauthorized (API key issues)
- **500**: Server error
- **404**: No recipes found

---

## 🔄 **Maintenance**

### **Regular Tasks**
1. **Update Dependencies**
   ```cmd
   pip install --upgrade -r requirements.txt
   ```

2. **Test Application**
   ```cmd
   # Run startup script
   savorme_professional_startup.bat
   
   # Test user flow
   # 1. Landing page loads
   # 2. Profile setup works
   # 3. Mood selection functions
   # 4. Recipe recommendations generate
   # 5. Cooking directions appear
   ```

3. **Clean Up Files**
   - Archive old documentation
   - Remove unused scripts
   - Update file organization

### **Before Each Release**
- [ ] Test all startup scripts
- [ ] Verify all features work
- [ ] Update documentation
- [ ] Check error handling
- [ ] Test mobile responsiveness

### **Monthly Maintenance**
- [ ] Review and consolidate documentation
- [ ] Clean up unused files
- [ ] Update dependencies
- [ ] Test all essential functions

---

## 📚 **Additional Resources**

### **Detailed Documentation**
- `TECHNICAL_SPECIFICATION_COMPLETE.md` - Complete technical details
- `CUSTOMIZATIONS_PERSISTENT.md` - Design system and customizations
- `MASTER_FILE_ORGANIZATION.md` - File organization guide

### **Quick References**
- `QUICK_IMPLEMENTATION_GUIDE.md` - Fast implementation steps
- `AUTOMATED_APP_STARTUP_GUIDE.md` - Automated startup process

### **Support**
- Check terminal logs for error messages
- Review API documentation at http://127.0.0.1:8000/docs
- Test individual components separately

---

## ✅ **Success Criteria**

### **Application is Working When:**
- [ ] Backend starts on port 8000
- [ ] Frontend starts on port 5000
- [ ] Landing page loads with correct design
- [ ] Profile form submission works
- [ ] Mood selection interface functions
- [ ] Recipe recommendations generate
- [ ] Cooking directions appear (AI or fallback)
- [ ] "New Suggestions" button works
- [ ] Mobile responsive design works
- [ ] Error handling provides user feedback

### **Performance Standards**
- **Page Load Time**: < 2 seconds
- **API Response Time**: < 5 seconds
- **Mobile Responsiveness**: Works on screens 320px+
- **Error Recovery**: Graceful fallbacks for all failures

---

*This master guide provides everything needed to understand, deploy, and maintain the SavorMe application effectively.*
