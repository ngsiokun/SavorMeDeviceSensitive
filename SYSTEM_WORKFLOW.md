# SavorMe System Workflow

## Complete User Journey: From Profile to Recipe Recommendation

This document describes the complete workflow of the SavorMe application, showing how user input flows through various systems to generate personalized, mood-based recipe recommendations.

## 📍 **Mapping Data Sources**

### **Primary Source: `app/data/mood_mapping.json`**

**File Path**: `C:\Users\HP\SavorMe\SavorMe-backend\app\data\mood_mapping.json`

This JSON file is the **single source of truth** for all mood-to-nutrient mappings and contains:
- Evidence-based mood definitions
- Nutrient targets and weights
- Scientific evidence levels
- Nutrient alias mappings
- Dietary patterns and contraindications

### **Key Components in mood_mapping.json**:
```json
{
  "version": "2.1.0",
  "moods": [
    {
      "id": "stressed",
      "display_name": "Stressed / Anxious", 
      "targets": {
        "nutrients": [
          {"name": "magnesium", "min_per_meal": 120, "weight": 1.0}
        ]
      },
      "evidence_level": "Moderate - Mixed but trending positive"
    }
    // ... 3 more evidence-based moods
  ],
  "nutrient_aliases": {
    "magnesium": ["MG", "Magnesium, Mg", "magnesium"],
    "iron": ["iron", "iron_fe", "Iron, Fe", "FE"]
    // ... complete alias mappings
  }
}
```

---

## 📊 Workflow Overview

```
User Input → Profile Processing → Mood Selection → Backend Processing → API Calls → Recipe Scoring → Response Display
```

## 🔄 **Detailed Technical Flow: Mood → Nutrients → Recipe**

### **Step 1: User Input Processing**
```json
{
  "mood_blend": {
    "moods": [
      {"mood": "stressed", "intensity": "very"}
    ]
  },
  "user_profile": {
    "age": 32,
    "gender": "female", 
    "height_cm": 165,
    "weight_kg": 60,
    "cuisine_preferences": ["Mediterranean"],
    "dietary_preference": "none"
  }
}
```

### **Step 2: Mood → Nutrient Targets** 
*[MoodNutritionEngine loads mood_mapping.json]*

For "stressed" mood, system extracts:
- Magnesium: ≥120mg (weight: 1.0)
- Omega-3 EPA/DHA: ≥0.3g (weight: 0.9) 
- Fiber: ≥8g (weight: 0.7)
- Added Sugar: ≤10g (weight: 0.6)

### **Step 3: User Nutrition Needs Calculation**
*[NutritionCalculator using Harris-Benedict]*

- BMR: 1,375 kcal/day
- TDEE: 2,131 kcal/day (moderate activity)
- Protein: 72g/day (1.2g/kg)
- Fiber: 25g/day

### **Step 4: Recipe Search & Nutrient Extraction**
*[EdamamClient searches recipes and extracts nutrients]*

- Searches Edamam API for Mediterranean recipes
- Extracts full nutrient data from `totalNutrients`
- Converts to per-serving values
- Canonicalizes nutrient names using aliases

### **Step 5: Recipe Scoring & Enhancement**
*[MoodNutritionEngine scores recipes and enhances with secondary nutrients]*

- Scores each recipe against mood nutrient targets
- Enhances recipes with secondary nutrients (magnesium, iron, B12, folate, vitamin D, omega-3, zinc, vitamin C)
- Applies variety rotation logic
- Selects best-scoring recipe

### **Step 6: Response Generation**
*[OpenRouterClient generates cooking directions and emotional rationale]*

- Generates detailed cooking instructions
- Creates emotional rationale explaining mood-nutrition connection
- Returns complete recipe recommendation with enhanced nutrition data

---

## 🔄 Detailed Step-by-Step Workflow

### **STEP 1: User Profile Collection**
**Component**: Frontend (Profile Page)  
**URL**: `http://localhost:5000/profile`  
**File**: `demo_app/templates/profile.html`

**User Inputs:**
```json
{
  "age": 32,
  "gender": "female",
  "height_cm": 165,
  "weight_kg": 60,
  "cuisine_preferences": ["Mediterranean"],
  "food_allergies": ["peanuts"],
  "dietary_preference": "vegetarian"
}
```

**Action**: User fills out profile form  
**Output**: Profile data stored in browser session  
**Next Step**: → Mood Selection Page

---

### **STEP 2: Mood State Selection**
**Component**: Frontend (Mood Selection Page)  
**URL**: `http://localhost:5000/mood-selection`  
**File**: `demo_app/templates/mood_selection.html`

**User Selects Moods:**
```json
{
  "moods": [
    {
      "mood": "stressed",
      "intensity": "medium"
    },
    {
      "mood": "fatigued",
      "intensity": "high"
    }
  ]
}
```

**Available Mood States:**
- `stressed` - Stressed/Anxious
- `fatigued` - Fatigued/Low Energy
- `low_mood` - Low Mood/Blue
- `irritable` - Irritable/Angry

**Intensity Levels:** `low`, `medium`, `high`

**Action**: User selects 1-3 moods with intensity  
**Output**: Mood blend object  
**Next Step**: → Submit to Backend API

---

### **STEP 3: Request Formation**
**Component**: Frontend (JavaScript)  
**File**: `demo_app/static/js/mood_selection.js`

**Combined Request JSON:**
```json
{
  "mood_blend": {
    "moods": [
      {"mood": "stressed", "intensity": "medium"},
      {"mood": "fatigued", "intensity": "high"}
    ]
  },
  "user_profile": {
    "age": 32,
    "gender": "female",
    "height_cm": 165,
    "weight_kg": 60,
    "cuisine_preferences": ["Mediterranean"],
    "food_allergies": ["peanuts"],
    "dietary_preference": "vegetarian"
  }
}
```

**Action**: Frontend combines profile + mood data  
**HTTP Method**: `POST`  
**Endpoint**: `http://localhost:8000/api/v1/recipes/recommend`  
**Next Step**: → Backend API Processing

---

### **STEP 4: Backend API Receives Request**
**Component**: FastAPI Backend  
**URL**: `http://localhost:8000/api/v1/recipes/recommend`  
**File**: `app/api/routes.py` (Line 104-240)

**API Endpoint Details:**
- **Method**: POST
- **Path**: `/api/v1/recipes/recommend`
- **Input**: `MoodBlend` + `UserProfile`
- **Output**: `RecipeRecommendation`

**Action**: Validates request and starts processing  
**Next Step**: → Nutrition Calculator

---

### **STEP 5: Nutrition Calculation**
**Component**: Nutrition Calculator Service  
**Data Source**: In-house calculation using medical formulas  
**File**: `app/services/nutrition_calculator.py`

**Formulas Used:**
- **BMR (Basal Metabolic Rate)**: Harris-Benedict Equation
  - Female: `655 + (9.6 × weight_kg) + (1.8 × height_cm) - (4.7 × age)`
  - Male: `66 + (13.7 × weight_kg) + (5 × height_cm) - (6.8 × age)`
- **TDEE (Total Daily Energy Expenditure)**: BMR × Activity Factor
- **Protein**: WHO guidelines (0.8-1.2g per kg body weight)
- **Fiber**: 25-38g per day based on gender

**Input:**
```json
{
  "age": 32,
  "gender": "female",
  "height_cm": 165,
  "weight_kg": 60
}
```

**Output (Nutrition Targets):**
```json
{
  "calories": 1845.0,
  "protein_g": 48.0,
  "fiber_g": 25.0,
  "carbs_g": 230.0,
  "fat_g": 61.0
}
```

**Action**: Calculates personalized daily nutritional needs  
**Next Step**: → Mood Interpretation

---

### **STEP 6: Mood-to-Nutrient Mapping**
**Component**: Mood Nutrition Engine  
**Data Source**: Evidence-based mood mapping (JSON config)  
**File**: `app/services/mood_nutrition_engine.py`  
**Config File**: `app/data/mood_mapping.json`

**Scientific Evidence Sources:**
- SMILES Trial (2017) - Mediterranean diet for depression
- Cochrane Reviews - Omega-3 for anxiety
- WHO Guidelines - Nutritional psychiatry

**Mood-Specific Nutrient Targets:**

**For "Stressed" Mood:**
```json
{
  "magnesium_mg": {"min": 350, "max": 400},
  "omega_3_epa_dha_g": {"min": 0.5, "max": null},
  "vitamin_b6_mg": {"min": 1.5, "max": null},
  "added_sugars_g": {"min": null, "max": 25},
  "caffeine_mg": {"min": null, "max": 200}
}
```

**For "Fatigued" Mood:**
```json
{
  "iron_mg": {"min": 10, "max": null},
  "vitamin_b12_mcg": {"min": 2.4, "max": null},
  "protein_g": {"min": 25, "max": null},
  "complex_carbs_g": {"min": 30, "max": null},
  "added_sugars_g": {"min": null, "max": 15}
}
```

**Action**: Maps moods to specific nutrient requirements  
**Output**: Combined nutrient targets for recipe scoring  
**Next Step**: → Recipe Search Keywords

---

### **STEP 7: Search Keyword Generation**
**Component**: Fusion Engine  
**File**: `app/services/fusion_engine.py`

**Mood-Based Keyword Database:**
```python
MOOD_SEARCH_KEYWORDS = {
    "stressed": [
        ["salmon", "spinach"],
        ["avocado", "quinoa"],
        ["dark chocolate", "almonds"],
        ["chickpeas", "sweet potato"],
        # ... 10 variations per mood
    ],
    "fatigued": [
        ["lentils", "spinach"],
        ["quinoa", "beans"],
        ["eggs", "broccoli"],
        # ...
    ]
}
```

**Keyword Filtering Rules:**
- ✅ Remove meat keywords if vegetarian/vegan
- ✅ Remove seafood keywords if vegan
- ✅ Remove allergen keywords
- ✅ Fallback to "vegetables legumes" if all filtered

**Input:** `stressed` + `fatigued` moods  
**Output:** `["salmon", "spinach"]` (randomly selected from variations)  
**Next Step**: → Edamam Recipe Search

---

### **STEP 8: Edamam Recipe Search API Call**
**Component**: Edamam API Client  
**Data Source**: Edamam Recipe Search API (External)  
**File**: `app/services/edamam_client.py`

**API Details:**
- **Provider**: Edamam
- **API URL**: `https://api.edamam.com/api/recipes/v2`
- **API Type**: Recipe Search API
- **Documentation**: https://developer.edamam.com/edamam-recipe-api
- **Plan**: Developer (Free Tier)
- **Rate Limit**: 10 calls/minute

**API Request Parameters:**
```http
GET https://api.edamam.com/api/recipes/v2
?type=public
&q=salmon+spinach
&app_id=YOUR_APP_ID
&app_key=YOUR_APP_KEY
&cuisineType=Mediterranean
&diet=vegetarian
&health=peanut-free
&calories=461-738
&nutrients[PROCNT]=12-19
```

**Parameter Mapping:**

| Parameter | Source | Example |
|-----------|--------|---------|
| `q` | Fusion Engine | `salmon spinach` |
| `cuisineType` | User Profile | `Mediterranean` |
| `diet` | User Profile | `vegetarian` |
| `health` | User Allergies | `peanut-free` |
| `calories` | Nutrition Calculator | `461-738` (25-40% of TDEE) |
| `nutrients[PROCNT]` | Nutrition Calculator | `12-19` (20-40% of daily protein) |

**Cuisine Mapping:**
```json
{
  "Mediterranean": ["Mediterranean"],
  "Asian": ["Asian", "Chinese", "Japanese", "South East Asian"],
  "Mexican": ["Mexican"],
  "Italian": ["Italian"],
  "American": ["American"],
  "Other Western": ["British", "French", "Nordic", "Central Europe"],
  "Surprise Me": null
}
```

**API Response (10 Recipes):**
```json
{
  "hits": [
    {
      "recipe": {
        "uri": "recipe_123abc...",
        "label": "Mediterranean Salmon with Spinach",
        "image": "https://edamam-product-images.s3.amazonaws.com/...",
        "source": "Serious Eats",
        "url": "https://www.seriouseats.com/...",
        "yield": 4,
        "calories": 1240.5,
        "totalTime": 45,
        "cuisineType": ["mediterranean"],
        "mealType": ["lunch/dinner"],
        "dishType": ["main course"],
        "ingredients": [...],
        "totalNutrients": {
          "ENERC_KCAL": {"quantity": 1240.5},
          "PROCNT": {"quantity": 96.2},
          "FIBTG": {"quantity": 28.4},
          "MG": {"quantity": 350.8},
          "FE": {"quantity": 12.5},
          // ... full nutrient data
        }
      }
    }
    // ... 9 more recipes
  ]
}
```

**Action**: Fetches 10 recipes matching all criteria  
**Output**: Recipe data with full nutrition info  
**Next Step**: → Recipe Scoring

---

### **STEP 9: Evidence-Based Recipe Scoring**
**Component**: Mood Nutrition Engine  
**File**: `app/services/mood_nutrition_engine.py`

**Scoring Algorithm:**

For each recipe, calculate score based on mood-specific nutrient targets:

```python
score = 0

# For each nutrient target
for nutrient, target in mood_targets.items():
    recipe_amount = recipe.nutrients[nutrient]
    
    # Check if minimum met
    if target.min and recipe_amount >= target.min:
        score += 10
    
    # Check if within range
    if target.max and recipe_amount > target.max:
        score -= 5  # Penalty for exceeding max
    
    # Partial credit for approaching target
    if target.min and recipe_amount >= target.min * 0.7:
        score += 5

# Final score: 0-100
```

**Example Scoring:**

**Recipe: Mediterranean Salmon (per serving)**
```json
{
  "magnesium_mg": 87.7,     // ✅ Target: 350mg min → Partial +5
  "omega_3_epa_dha_g": 1.2, // ✅ Target: 0.5g min → Full +10
  "iron_mg": 3.1,           // ✅ Target: 10mg min → Partial +5
  "fiber_g": 7.1,           // ✅ Good amount +5
  "protein_g": 24.0,        // ✅ Target: 25g min → Close +8
  "added_sugars_g": 2.0     // ✅ Under 15g max → Full +10
}
// Total Score: 43/100
```

**Scoring Output (Top 3 Recipes):**
```json
[
  {
    "recipe_id": "recipe_123abc",
    "score": 87,
    "reasons": [
      "✅ High in magnesium (350mg) - Great for stress",
      "✅ Excellent omega-3 (1.2g EPA+DHA) - Reduces anxiety",
      "✅ Good iron (12mg) - Fights fatigue"
    ]
  },
  {
    "recipe_id": "recipe_456def",
    "score": 72,
    "reasons": [...]
  },
  {
    "recipe_id": "recipe_789ghi",
    "score": 65,
    "reasons": [...]
  }
]
```

**Action**: Scores all 10 recipes, sorts by score  
**Output**: Best matching recipe (highest score)  
**Next Step**: → AI Enhancement

---

### **STEP 10: AI-Generated Content**
**Component**: OpenRouter AI Client  
**Data Source**: OpenRouter API (External LLM Service)  
**File**: `app/services/openrouter_client.py`

**API Details:**
- **Provider**: OpenRouter
- **API URL**: `https://openrouter.ai/api/v1/chat/completions`
- **Model Used**: `anthropic/claude-3.5-sonnet`
- **Documentation**: https://openrouter.ai/docs

**Two AI Generation Tasks:**

#### **Task 1: Emotional Rationale**
**Purpose**: Explain why this recipe matches the user's mood

**API Request:**
```json
{
  "model": "anthropic/claude-3.5-sonnet",
  "messages": [
    {
      "role": "system",
      "content": "You are a nutritional psychiatry expert..."
    },
    {
      "role": "user",
      "content": "Recipe: Mediterranean Salmon\nMood: Stressed (medium), Fatigued (high)\nNutrients: High omega-3, magnesium, iron..."
    }
  ]
}
```

**AI Response:**
```
"This Mediterranean salmon dish is perfect for your current state. The high omega-3 content (1.2g EPA+DHA) helps reduce stress hormones and anxiety, while the iron (12mg) and B-vitamins combat fatigue and boost energy production. Spinach provides magnesium to calm your nervous system."
```

#### **Task 2: Cooking Directions**
**Purpose**: Generate step-by-step instructions if not provided by Edamam

**API Request:**
```json
{
  "model": "anthropic/claude-3.5-sonnet",
  "messages": [
    {
      "role": "user",
      "content": "Create cooking instructions for:\nRecipe: Mediterranean Salmon with Spinach\nIngredients: 4 salmon fillets, 2 cups spinach, ..."
    }
  ]
}
```

**AI Response:**
```json
[
  "Preheat oven to 400°F (200°C). Line a baking sheet with parchment paper.",
  "Season salmon fillets with salt, pepper, and oregano on both sides.",
  "Sauté garlic in olive oil for 1 minute, then add spinach until wilted.",
  "Place salmon on baking sheet, top with spinach mixture and lemon slices.",
  "Bake for 12-15 minutes until salmon flakes easily with a fork.",
  "Serve hot, garnished with fresh parsley and pine nuts."
]
```

**Action**: Generates personalized content using AI  
**Output**: Emotional rationale + cooking directions  
**Next Step**: → Response Formation

---

### **STEP 11: Final Response Creation**
**Component**: FastAPI Backend  
**File**: `app/api/routes.py`

**Complete Response JSON:**
```json
{
  "recipe": {
    "recipe_id": "recipe_8d385349bd071c964aa8dab8cc3c98b5",
    "name": "Mediterranean Salmon with Spinach and Pine Nuts",
    "image_url": "https://edamam-product-images.s3.amazonaws.com/...",
    "ingredients": [
      {
        "name": "salmon fillet",
        "amount": "4 fillets (6 oz each)",
        "unit": "piece"
      },
      {
        "name": "fresh spinach",
        "amount": "2 cups",
        "unit": "cup"
      },
      {
        "name": "pine nuts",
        "amount": "1/4 cup",
        "unit": "cup"
      },
      {
        "name": "olive oil",
        "amount": "2 tablespoons",
        "unit": "tablespoon"
      },
      {
        "name": "garlic",
        "amount": "3 cloves",
        "unit": "clove"
      },
      {
        "name": "lemon",
        "amount": "1",
        "unit": "whole"
      }
    ],
    "cooking_directions": [
      "Preheat oven to 400°F (200°C)...",
      "Season salmon fillets...",
      "Sauté garlic in olive oil...",
      "Place salmon on baking sheet...",
      "Bake for 12-15 minutes...",
      "Serve hot, garnished..."
    ],
    "prep_time": 15,
    "cook_time": 45,
    "servings": 4,
    "nutrition": {
      "calories": 310.1,
      "protein_g": 24.0,
      "fiber_g": 7.1,
      "carbs_g": 12.3,
      "fat_g": 18.5,
      "sodium_mg": 245.0
    },
    "source_url": "https://www.seriouseats.com/...",
    "source_name": "Serious Eats",
    "cuisine_type": ["mediterranean"],
    "meal_type": ["lunch/dinner"],
    "dish_type": ["main course"]
  },
  "emotional_rationale": "This Mediterranean salmon dish is perfect for your current state. The high omega-3 content helps reduce stress hormones and anxiety, while the iron and B-vitamins combat fatigue...",
  "mood_match_score": 87,
  "mood_match_reasons": [
    "✅ High in magnesium (350mg) - Great for stress relief",
    "✅ Excellent omega-3 (1.2g EPA+DHA) - Reduces anxiety",
    "✅ Good iron (12mg) - Fights fatigue and boosts energy"
  ],
  "nutritional_highlights": {
    "magnesium_mg": 350.0,
    "omega_3_epa_dha_g": 1.2,
    "iron_mg": 12.0,
    "vitamin_b12_mcg": 4.8
  }
}
```

**Action**: Combines all data into final response  
**HTTP Status**: `200 OK`  
**Next Step**: → Send to Frontend

---

### **STEP 12: Frontend Receives Response**
**Component**: Flask Demo App  
**File**: `demo_app/app.py`

**Action**: Proxies response from backend to frontend  
**Next Step**: → Display Recipe

---

### **STEP 13: Recipe Display**
**Component**: Frontend (Recipe Result Page)  
**URL**: `http://localhost:5000/recipe-result`  
**File**: `demo_app/templates/recipe_result.html`

**Displayed Information:**
- ✅ Recipe image
- ✅ Recipe name
- ✅ Prep and cook time
- ✅ Servings
- ✅ Nutrition summary (calories, protein, fiber)
- ✅ **100% Nutrient Match Score** badge
- ✅ Emotional rationale (why this recipe matches mood)
- ✅ Ingredients list
- ✅ Step-by-step cooking directions
- ✅ Link to original recipe source

**User Actions:**
- View full recipe details
- Click "View Full Recipe" to visit source website
- Start over with new mood selection

---

## 📋 System Architecture Summary

### **Frontend (Flask)**
- `demo_app/app.py` - Flask server
- `demo_app/templates/` - HTML pages
- `demo_app/static/` - CSS & JavaScript
- **Port**: 5000

### **Backend (FastAPI)**
- `app/main.py` - FastAPI server
- `app/api/routes.py` - API endpoints
- `app/services/` - Business logic
- `app/models/` - Data models
- `app/data/` - Configuration files
- **Port**: 8000

### **External APIs**
1. **Edamam Recipe Search API**
   - URL: `https://api.edamam.com/api/recipes/v2`
   - Purpose: Recipe data with nutrition
   - Rate Limit: 10 calls/minute

2. **OpenRouter AI API**
   - URL: `https://openrouter.ai/api/v1/chat/completions`
   - Purpose: AI content generation
   - Model: Claude 3.5 Sonnet

### **Data Sources**
1. **User Input** - Profile & mood from frontend
2. **Medical Formulas** - Harris-Benedict, WHO guidelines
3. **Scientific Research** - SMILES trial, Cochrane reviews
4. **Edamam Database** - 2M+ recipes with nutrition data
5. **AI Model** - Claude 3.5 Sonnet via OpenRouter

---

## 🔐 Security & Configuration

### **Environment Variables (.env)**
```bash
# Edamam API
EDAMAM_APP_ID=your_app_id
EDAMAM_APP_KEY=your_app_key
EDAMAM_BASE_URL=https://api.edamam.com/api/recipes/v2

# OpenRouter AI
OPENROUTER_API_KEY=your_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Application
BACKEND_URL=http://localhost:8000
```

---

## 📊 Data Flow Summary

```
┌─────────────────┐
│   User Input    │
│  (Profile +     │
│  Mood State)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Nutrition      │──► Harris-Benedict Formula
│  Calculator     │──► WHO Guidelines
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Mood→Nutrient  │──► mood_mapping.json
│  Mapping Engine │──► SMILES Trial Evidence
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Search Keyword │──► Fusion Engine
│  Generation     │──► Keyword Filtering
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Edamam API     │──► Recipe Search
│  Recipe Search  │──► 10 Recipes Returned
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Recipe Scoring │──► Nutrient Matching
│  Algorithm      │──► Best Recipe Selected
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OpenRouter AI  │──► Emotional Rationale
│  Content Gen    │──► Cooking Directions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Final Response │──► Complete Recipe Data
│  to User        │──► Displayed on Screen
└─────────────────┘
```

---

## 🎯 Key Features Demonstrated

1. ✅ **Evidence-Based Nutrition** - SMILES trial, Cochrane reviews
2. ✅ **Personalized Calculations** - Age, gender, height, weight
3. ✅ **Multi-API Integration** - Edamam + OpenRouter
4. ✅ **Intelligent Filtering** - Dietary restrictions, allergies, cuisine
5. ✅ **AI Enhancement** - Personalized explanations & instructions
6. ✅ **Mood-Based Scoring** - Deterministic algorithm with scientific backing
7. ✅ **Real-Time Processing** - <5 seconds end-to-end response

---

## 📖 References

### Scientific Evidence
- SMILES Trial (2017): Mediterranean diet for depression
- Cochrane Reviews: Omega-3 fatty acids for anxiety
- WHO Guidelines: Protein and micronutrient requirements

### APIs & Tools
- Edamam Recipe Search API: https://developer.edamam.com
- OpenRouter AI: https://openrouter.ai
- FastAPI Framework: https://fastapi.tiangolo.com
- Flask Framework: https://flask.palletsprojects.com

### Medical Formulas
- Harris-Benedict Equation (BMR)
- WHO Protein Guidelines
- Dietary Reference Intakes (DRIs)

---

**Document Version**: 1.0  
**Last Updated**: October 5, 2025  
**Project**: SavorMe - Mood-Based Recipe Recommendation System

