# SavorMe Technical Specification - Complete Application Blueprint

## 🎯 **Purpose**
This document provides a comprehensive technical specification for creating the complete SavorMe application from scratch, including frontend, backend, integration, pages, and cooking directions system.

## 📋 **Table of Contents**
1. [System Architecture](#system-architecture)
2. [Backend API Specification](#backend-api-specification)
3. [Frontend Application Structure](#frontend-application-structure)
4. [Page Layouts and Components](#page-layouts-and-components)
5. [Frontend-Backend Integration](#frontend-backend-integration)
6. [Cooking Directions System](#cooking-directions-system)
7. [Implementation Steps](#implementation-steps)
8. [Quality Assurance](#quality-assurance)

---

## 🏗️ **System Architecture**

### **Overall Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   External APIs │
│   (Flask)       │◄──►│   (FastAPI)     │◄──►│   (Edamam, AI)  │
│   Port: 5000    │    │   Port: 8000    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Technology Stack**
- **Backend**: FastAPI (Python) + Uvicorn
- **Frontend**: Flask (Python) + Jinja2 Templates
- **Database**: In-memory (for demo) / PostgreSQL (production)
- **External APIs**: Edamam Recipe API, OpenRouter AI API
- **Styling**: Custom CSS (mobile-first design)

---

## 🔧 **Backend API Specification**

### **Core Services Structure**
```
app/
├── main.py                 # FastAPI application entry point
├── api/
│   └── routes.py          # API endpoints
├── core/
│   └── config.py          # Configuration management
├── models/
│   ├── user.py            # User profile models
│   ├── mood.py            # Mood mapping models
│   └── recipe.py          # Recipe data models
├── services/
│   ├── edamam_client.py   # Recipe search service
│   ├── openrouter_client.py # AI cooking directions
│   ├── mood_nutrition_engine.py # Mood-to-nutrition mapping
│   ├── fusion_engine.py   # Recipe recommendation logic
│   └── nutrition_calculator.py # Nutritional analysis
└── data/
    └── mood_mapping.json  # Mood-to-nutrition mapping data
```

### **API Endpoints**

#### **1. Health Check**
```python
@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
```

#### **2. Recipe Recommendation**
```python
@app.post("/api/v1/recipes/recommend")
async def recommend_recipe(request: RecipeRecommendationRequest):
    """
    Generate recipe recommendations based on mood and user profile
    """
    # Implementation steps:
    # 1. Validate input data
    # 2. Map mood to nutrition requirements
    # 3. Search Edamam API for recipes
    # 4. Generate cooking directions via AI
    # 5. Return complete recipe with directions
```

#### **3. User Profile Management**
```python
@app.post("/api/v1/users/profile")
async def create_user_profile(profile: UserProfile):
    """Create or update user profile"""
    
@app.get("/api/v1/users/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Retrieve user profile"""
```

### **Data Models**

#### **User Profile Model**
```python
class UserProfile(BaseModel):
    age: int
    gender: str
    height_cm: int
    weight_kg: float
    cuisine_preferences: List[str]
    food_allergies: List[str]
    dietary_preference: str
    calorie_preference: str
    custom_calories: Optional[int] = None
```

#### **Mood Blend Model**
```python
class MoodBlend(BaseModel):
    moods: List[MoodIntensity]
    
class MoodIntensity(BaseModel):
    mood: str
    intensity: str  # low, medium, high, very
```

#### **Recipe Model**
```python
class Recipe(BaseModel):
    recipe_id: str
    name: str
    image_url: str
    ingredients: List[Ingredient]
    cooking_directions: List[str]
    nutritional_info: NutritionalInfo
    emotional_rationale: str
    evidence: List[str]
```

---

## 🎨 **Frontend Application Structure**

### **Flask Application Structure**
```
demo_app/
├── app.py                  # Flask application entry point
├── templates/              # Jinja2 HTML templates
│   ├── index.html         # Landing page
│   ├── profile.html       # User profile page
│   ├── mood_selection.html # Mood selection page
│   └── recipe_result.html # Recipe results page
├── static/
│   ├── css/               # Stylesheets
│   │   ├── main.css       # Base styles
│   │   ├── landing.css    # Landing page styles
│   │   ├── profile.css    # Profile page styles
│   │   ├── mood_selection.css # Mood selection styles
│   │   ├── results.css    # Results page styles
│   │   └── recipe_results.css # Recipe results styles
│   └── js/                # JavaScript files
│       ├── profile.js     # Profile page logic
│       ├── mood_selection.js # Mood selection logic
│       └── recipe_result.js # Recipe results logic
└── README.md              # Frontend documentation
```

### **Flask Routes**
```python
@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/profile')
def profile():
    """User profile setup"""
    return render_template('profile.html')

@app.route('/mood-selection')
def mood_selection():
    """Mood selection interface"""
    return render_template('mood_selection.html')

@app.route('/recipe-result')
def recipe_result():
    """Recipe results display"""
    return render_template('recipe_result.html')

@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    """Proxy to backend API"""
    # Forward request to backend
    # Handle response and errors
```

---

## 📱 **Page Layouts and Components**

### **1. Landing Page (index.html)**
```html
<!DOCTYPE html>
<html>
<head>
    <title>SavorMe - Mood-Based Recipe Companion</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/landing.css') }}">
</head>
<body>
    <div class="landing-container">
        <!-- Hero Section -->
        <div class="hero-section">
            <div class="hero-icon">🍽️</div>
            <h1 class="hero-title">SavorMe</h1>
            <p class="hero-subtitle">Your Mood-Based Recipe Companion</p>
            <p class="hero-description">Discover personalized recipes that match your current mood and nutritional needs</p>
            <a href="/profile" class="hero-cta-btn">Start Your Journey →</a>
        </div>
        
        <!-- Features Section -->
        <div class="features-section">
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🎭</div>
                    <h3 class="feature-title">Mood Analysis</h3>
                    <p class="feature-description">Select your current mood for personalized recommendations</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🍎</div>
                    <h3 class="feature-title">Nutrition Focus</h3>
                    <p class="feature-description">Get recipes tailored to your nutritional needs</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">👤</div>
                    <h3 class="feature-title">Personal Profile</h3>
                    <p class="feature-description">Customize based on your preferences and dietary requirements</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔬</div>
                    <h3 class="feature-title">Evidence-Based</h3>
                    <p class="feature-description">Recommendations backed by nutritional science</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

### **2. User Profile Page (profile.html)**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Your Profile - SavorMe</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/profile.css') }}">
</head>
<body>
    <div class="profile-container">
        <div class="profile-header">
            <h1>Create Your Profile</h1>
            <p>Help us personalize your recipe recommendations</p>
        </div>
        
        <form class="profile-form" id="profileForm">
            <div class="form-group">
                <label for="age">Age</label>
                <input type="number" id="age" name="age" min="13" max="120" required>
            </div>
            
            <div class="form-group">
                <label for="gender">Gender</label>
                <select id="gender" name="gender" required>
                    <option value="">Select Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="height">Height (cm)</label>
                <input type="number" id="height" name="height_cm" min="100" max="250" required>
            </div>
            
            <div class="form-group">
                <label for="weight">Weight (kg)</label>
                <input type="number" id="weight" name="weight_kg" min="30" max="300" step="0.1" required>
            </div>
            
            <div class="form-group">
                <label for="cuisine">Preferred Cuisines</label>
                <div class="checkbox-group">
                    <label><input type="checkbox" name="cuisine" value="Mediterranean"> Mediterranean</label>
                    <label><input type="checkbox" name="cuisine" value="Asian"> Asian</label>
                    <label><input type="checkbox" name="cuisine" value="Italian"> Italian</label>
                    <label><input type="checkbox" name="cuisine" value="Mexican"> Mexican</label>
                </div>
            </div>
            
            <button type="submit" class="submit-btn">Continue to Mood Selection</button>
        </form>
    </div>
    
    <script src="{{ url_for('static', filename='js/profile.js') }}"></script>
</body>
</html>
```

### **3. Mood Selection Page (mood_selection.html)**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Select Your Mood - SavorMe</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/mood_selection.css') }}">
</head>
<body>
    <div class="mood-container">
        <div class="mood-header">
            <h1>How are you feeling today?</h1>
            <p>Select your current mood to get personalized recipe recommendations</p>
        </div>
        
        <div class="mood-grid">
            <div class="mood-card" data-mood="happy">
                <div class="mood-icon">😊</div>
                <span class="mood-name">Happy</span>
            </div>
            <div class="mood-card" data-mood="sad">
                <div class="mood-icon">😢</div>
                <span class="mood-name">Sad</span>
            </div>
            <div class="mood-card" data-mood="anxious">
                <div class="mood-icon">😰</div>
                <span class="mood-name">Anxious</span>
            </div>
            <div class="mood-card" data-mood="energetic">
                <div class="mood-icon">⚡</div>
                <span class="mood-name">Energetic</span>
            </div>
            <div class="mood-card" data-mood="fatigued">
                <div class="mood-icon">😴</div>
                <span class="mood-name">Fatigued</span>
            </div>
            <div class="mood-card" data-mood="stressed">
                <div class="mood-icon">😤</div>
                <span class="mood-name">Stressed</span>
            </div>
        </div>
        
        <div class="intensity-section">
            <h3>How intense is this feeling?</h3>
            <div class="intensity-buttons">
                <button class="intensity-btn" data-intensity="low">Low</button>
                <button class="intensity-btn" data-intensity="medium">Medium</button>
                <button class="intensity-btn" data-intensity="high">High</button>
                <button class="intensity-btn" data-intensity="very">Very</button>
            </div>
        </div>
        
        <button id="getRecommendation" class="recommendation-btn" disabled>
            Get My Recipe Recommendation
        </button>
        
        <div id="loadingSpinner" class="loading-spinner" style="display: none;">
            <div class="spinner"></div>
            <p>Finding the perfect recipe for your mood...</p>
        </div>
    </div>
    
    <script src="{{ url_for('static', filename='js/mood_selection.js') }}"></script>
</body>
</html>
```

### **4. Recipe Results Page (recipe_result.html)**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Your Recipe Recommendations - SavorMe</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/results.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/recipe_results.css') }}">
</head>
<body>
    <div class="app-container">
        <!-- Status Bar -->
        <div class="status-bar">
            <span>9:41</span>
            <span>SavorMe</span>
            <span>🔋 100%</span>
        </div>
        
        <div class="content-area">
            <div class="header">
                <h1 class="title">Your Recipe</h1>
                <p class="subtitle">Perfectly matched to your mood</p>
            </div>
            
            <!-- Loading Spinner -->
            <div id="loadingSpinner" class="loading-spinner">
                <div class="spinner"></div>
                <p>Preparing your personalized recipe...</p>
            </div>
            
            <!-- Results Content -->
            <div id="resultsContent" class="results-content">
                <!-- Recipe content will be populated by JavaScript -->
            </div>
            
            <!-- Action Buttons -->
            <div class="action-buttons">
                <button onclick="goBack()" class="btn-secondary">← Back</button>
                <button onclick="refreshResults()" class="btn-primary">New Suggestions</button>
            </div>
        </div>
    </div>
    
    <script src="{{ url_for('static', filename='js/recipe_result.js') }}"></script>
</body>
</html>
```

---

## 🔗 **Frontend-Backend Integration**

### **API Communication Flow**
```javascript
// 1. Profile Submission
function submitProfile(profileData) {
    sessionStorage.setItem('userProfile', JSON.stringify(profileData));
    window.location.href = '/mood-selection';
}

// 2. Mood Selection and Recommendation Request
function getRecommendation() {
    const selectedMoods = getSelectedMoods();
    const userProfile = JSON.parse(sessionStorage.getItem('userProfile') || '{}');
    
    const requestData = {
        mood_blend: {
            moods: selectedMoods.map(mood => ({
                mood: mood,
                intensity: selectedIntensity
            }))
        },
        user_profile: userProfile
    };
    
    // Show loading
    document.getElementById('loadingSpinner').style.display = 'block';
    
    // Make API call
    fetch('/api/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        // Store result and navigate
        sessionStorage.setItem('recipeResult', JSON.stringify(data));
        sessionStorage.setItem('selectedMoods', JSON.stringify(selectedMoods));
        sessionStorage.setItem('selectedIntensity', selectedIntensity);
        window.location.href = '/recipe-result';
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error
    });
}

// 3. Recipe Display
function displayRecipe(data) {
    const recipe = data.recipe;
    
    const recipeHTML = `
        <div class="recipe-card">
            <img src="${recipe.image_url}" alt="${recipe.name}" class="recipe-image">
            <h2 class="recipe-title">${recipe.name}</h2>
            
            <div class="recipe-section">
                <h3>Why This Recipe?</h3>
                <p class="emotional-rationale">${data.emotional_rationale}</p>
            </div>
            
            <div class="recipe-section">
                <h3>Ingredients</h3>
                <ul class="ingredients-list">
                    ${recipe.ingredients.map(ing => `<li>${ing.name}: ${ing.amount}</li>`).join('')}
                </ul>
            </div>
            
            <div class="recipe-section">
                <h3>Cooking Directions</h3>
                <ol class="directions-list">
                    ${recipe.cooking_directions.map(dir => `<li>${dir}</li>`).join('')}
                </ol>
            </div>
            
            <div class="recipe-section">
                <h3>Nutritional Benefits</h3>
                <p class="nutrition-info">${data.nutritional_analysis}</p>
            </div>
            
            <div class="recipe-section">
                <h3>Scientific Evidence</h3>
                <ul class="evidence-list">
                    ${data.evidence.map(evidence => `<li>${evidence}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;
    
    document.getElementById('resultsContent').innerHTML = recipeHTML;
    showResults();
}
```

### **Error Handling**
```javascript
function handleAPIError(error, response) {
    let errorMessage = 'Something went wrong. Please try again.';
    
    if (response && response.status === 404) {
        errorMessage = 'No recipes found for your mood. Try selecting different moods.';
    } else if (response && response.status === 500) {
        errorMessage = 'Server error. Please try again later.';
    } else if (error.name === 'TypeError') {
        errorMessage = 'Unable to connect to the server. Please check your connection.';
    }
    
    // Display error message to user
    showErrorMessage(errorMessage);
}
```

---

## 🍳 **Cooking Directions System**

### **AI-Powered Cooking Directions**
```python
class OpenRouterClient:
    def __init__(self):
        self.base_url = f"{settings.OPENROUTER_BASE_URL}/chat/completions"
        self.api_key = settings.OPENROUTER_API_KEY
        self.default_model = "meta-llama/llama-3.1-8b-instruct:free"
    
    async def generate_cooking_directions(self, recipe_name, ingredients, cuisine_type=None):
        """Generate step-by-step cooking directions using LLM"""
        
        if not self.api_key or self.api_key == "your_openrouter_api_key":
            # Use fallback directions
            return self._generate_fallback_directions(recipe_name, ingredients, cuisine_type)
        
        # AI-generated directions
        prompt = f"""
        Generate detailed, step-by-step cooking directions for this recipe:
        
        Recipe: {recipe_name}
        Ingredients: {', '.join([ing.name for ing in ingredients])}
        Cuisine: {cuisine_type[0] if cuisine_type else 'general'}
        
        Provide 5-6 clear, actionable cooking steps that are:
        1. Easy to follow for home cooks
        2. Include proper cooking temperatures and times
        3. Mention important techniques
        4. Include safety considerations
        5. Are culturally appropriate for the cuisine type
        
        Format as a numbered list of steps.
        """
        
        # Make API call to OpenRouter
        # Handle response and parse directions
        # Return list of cooking steps
        
    def _generate_fallback_directions(self, recipe_name, ingredients, cuisine_type=None):
        """Generate basic cooking directions when API is unavailable"""
        cuisine = cuisine_type[0] if cuisine_type else "general"
        
        # Analyze ingredients to determine cooking method
        ingredient_names = [ing.name.lower() for ing in ingredients]
        
        if any(meat in " ".join(ingredient_names) for meat in ["beef", "chicken", "pork", "lamb"]):
            return self._get_meat_cooking_directions()
        elif any(fish in " ".join(ingredient_names) for fish in ["salmon", "tuna", "cod", "halibut"]):
            return self._get_fish_cooking_directions()
        elif any(veg in " ".join(ingredient_names) for veg in ["bell pepper", "zucchini", "eggplant"]):
            return self._get_vegetable_cooking_directions()
        else:
            return self._get_general_cooking_directions()
    
    def _get_meat_cooking_directions(self):
        return [
            "Preheat oven to 375°F (190°C).",
            "Season the meat with salt, pepper, and herbs.",
            "Brown the meat in a large skillet over medium-high heat.",
            "Add vegetables and continue cooking until tender.",
            "Transfer to oven-safe dish and bake for 25-30 minutes.",
            "Let rest for 5 minutes before serving."
        ]
    
    def _get_fish_cooking_directions(self):
        return [
            "Preheat oven to 400°F (200°C).",
            "Season the fish with salt, pepper, and lemon.",
            "Heat oil in an oven-safe skillet over medium heat.",
            "Cook fish for 3-4 minutes per side until golden.",
            "Transfer to oven and bake for 8-10 minutes.",
            "Garnish with fresh herbs and serve immediately."
        ]
    
    def _get_vegetable_cooking_directions(self):
        return [
            "Preheat oven to 425°F (220°C).",
            "Wash and prepare all vegetables.",
            "Toss vegetables with olive oil, salt, and herbs.",
            "Arrange on baking sheet in single layer.",
            "Roast for 20-25 minutes until tender and golden.",
            "Season with additional herbs and serve warm."
        ]
    
    def _get_general_cooking_directions(self):
        return [
            "Prepare all ingredients according to recipe requirements.",
            "Heat cooking oil or butter in a large pan over medium heat.",
            "Add main ingredients and cook until tender.",
            "Season with salt, pepper, and herbs to taste.",
            "Simmer for 10-15 minutes to develop flavors.",
            "Garnish and serve hot."
        ]
```

### **Mood-to-Nutrition Mapping**
```python
class MoodNutritionEngine:
    def __init__(self):
        with open('app/data/mood_mapping.json', 'r') as f:
            self.mood_mapping = json.load(f)
    
    def get_nutrition_requirements(self, mood_blend):
        """Map mood to nutritional requirements"""
        requirements = {
            'calories_range': '2000-2500',
            'protein_range': '50-100',
            'carbs_range': '200-300',
            'fat_range': '50-80',
            'fiber_range': '25-35',
            'vitamins': [],
            'minerals': []
        }
        
        for mood_intensity in mood_blend.moods:
            mood = mood_intensity.mood
            intensity = mood_intensity.intensity
            
            if mood in self.mood_mapping:
                mood_data = self.mood_mapping[mood]
                
                # Adjust requirements based on mood and intensity
                if mood == 'fatigued' and intensity in ['high', 'very']:
                    requirements['protein_range'] = '60-80'
                    requirements['vitamins'].extend(['B12', 'Iron'])
                elif mood == 'anxious' and intensity in ['high', 'very']:
                    requirements['vitamins'].extend(['Magnesium', 'Omega-3'])
                elif mood == 'stressed' and intensity in ['high', 'very']:
                    requirements['vitamins'].extend(['Vitamin C', 'B-Complex'])
        
        return requirements
```

---

## 🚀 **Implementation Steps**

### **Phase 1: Backend Setup**
1. **Create FastAPI Application**
   ```bash
   pip install fastapi uvicorn python-dotenv requests
   ```

2. **Set up Project Structure**
   ```
   mkdir -p app/{api,core,models,services,data}
   touch app/__init__.py app/main.py
   ```

3. **Create Configuration**
   ```python
   # app/core/config.py
   from pydantic_settings import BaseSettings
   
   class Settings(BaseSettings):
       OPENROUTER_API_KEY: str = "your_openrouter_api_key"
       EDAMAM_APP_ID: str = "your_edamam_app_id"
       EDAMAM_APP_KEY: str = "your_edamam_app_key"
   
   settings = Settings()
   ```

4. **Implement API Endpoints**
   - Health check endpoint
   - Recipe recommendation endpoint
   - User profile management

### **Phase 2: Frontend Setup**
1. **Create Flask Application**
   ```bash
   pip install flask requests
   ```

2. **Set up Project Structure**
   ```
   mkdir -p demo_app/{templates,static/{css,js}}
   touch demo_app/app.py
   ```

3. **Create HTML Templates**
   - Landing page with mobile-first design
   - Profile setup page
   - Mood selection interface
   - Recipe results display

4. **Implement CSS Styling**
   - Mobile-first responsive design
   - Consistent color scheme
   - Glassmorphic effects
   - Smooth animations

### **Phase 3: Integration**
1. **Frontend-Backend Communication**
   - API proxy endpoints
   - Error handling
   - Loading states
   - Session management

2. **External API Integration**
   - Edamam recipe search
   - OpenRouter AI directions
   - Fallback systems

### **Phase 4: Testing & Quality Assurance**
1. **Unit Tests**
   - Backend API endpoints
   - Frontend JavaScript functions
   - Integration tests

2. **User Experience Testing**
   - Mobile responsiveness
   - Cross-browser compatibility
   - Performance optimization

---

## ✅ **Quality Assurance**

### **Testing Checklist**
- [ ] Backend API responds correctly
- [ ] Frontend pages load without errors
- [ ] Mood selection works properly
- [ ] Recipe recommendations generate
- [ ] Cooking directions appear
- [ ] "New Suggestions" button works
- [ ] Mobile design is responsive
- [ ] Error handling works
- [ ] Loading states display
- [ ] Session storage functions

### **Performance Requirements**
- **Page Load Time**: < 2 seconds
- **API Response Time**: < 5 seconds
- **Mobile Responsiveness**: Works on screens 320px+
- **Browser Compatibility**: Chrome, Firefox, Safari, Edge

### **Security Considerations**
- Input validation on all forms
- API key protection
- CORS configuration
- Error message sanitization

---

## 📚 **Additional Resources**

### **Documentation Files**
- `CUSTOMIZATIONS_PERSISTENT.md` - Design system documentation
- `AUTOMATED_APP_STARTUP_GUIDE.md` - Setup and deployment guide
- `PAGE_LAYOUTS_REFERENCE.md` - Page layout specifications

### **Startup Scripts**
- `savorme_professional_startup.bat` - Complete startup automation
- `setup_new_clone.bat` - Environment setup
- `start_savorme_auto.bat` - Quick start script

### **Configuration Files**
- `requirements.txt` - Python dependencies
- `.env` - Environment variables template
- `README.md` - Project overview

---

*This technical specification provides a complete blueprint for creating the SavorMe application from scratch, ensuring consistent quality and functionality across all components.*
