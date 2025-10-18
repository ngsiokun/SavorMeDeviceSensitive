# 📚 SavorMe API Schema Reference

## 🎯 Purpose
This document contains the complete API schemas for the SavorMe backend, serving as a reference for frontend-backend integration.

**API Documentation URL:** `http://127.0.0.1:8000/docs` (when backend is running)

---

## 📡 Recipe Recommendation Endpoint

### Endpoint Details
- **URL:** `POST /api/v1/recipes/recommend`
- **Description:** Get complete recipe recommendation with emotional rationale
- **Response Model:** `RecipeRecommendation`

### Request Body Schema

```json
{
  "mood_blend": {
    "moods": [
      {
        "mood": "stressed",
        "intensity": "a_little"
      }
    ]
  },
  "user_profile": {
    "user_id": "string",
    "age": 0,
    "gender": "male",
    "height_cm": 1,
    "weight_kg": 1,
    "ethnic_background": "string",
    "cuisine_preferences": [
      "string"
    ],
    "food_allergies": [
      "string"
    ],
    "dietary_preference": "none",
    "target_calories": 0,
    "target_protein_g": 0,
    "target_fiber_g": 0
  },
  "nutrition_targets": {
    "calories": 0,
    "protein_g": 0,
    "fiber_g": 0,
    "carbs_g": 0,
    "fat_g": 0,
    "sodium_mg": 0
  },
  "activity_level": "moderate"
}
```

### Mood Options (Enums)
**Valid mood values:**
- `"stressed"` - Stressed/Anxious state
- `"fatigued"` - Fatigued/Low Energy state
- `"low_mood"` - Low Mood/Sad state
- `"irritable"` - Irritable/Cranky state

**Valid intensity values:**
- `"a_little"` - A little intensity
- `"medium"` - Medium intensity
- `"very"` - Very intense

### Gender Options (Enums)
- `"male"`
- `"female"`
- `"other"`

### Dietary Preference Options (Enums)
- `"none"` - No dietary restrictions
- `"vegetarian"` - Vegetarian diet
- `"vegan"` - Vegan diet
- `"pescatarian"` - Pescatarian diet
- `"gluten_free"` - Gluten-free diet
- `"dairy_free"` - Dairy-free diet
- `"keto"` - Ketogenic diet
- `"paleo"` - Paleo diet

### Response Schema

```json
{
  "recipe": {
    "recipe_id": "string",
    "name": "string",
    "image_url": "string",
    "ingredients": [
      {
        "name": "string",
        "amount": "string",
        "unit": "string"
      }
    ],
    "cooking_directions": [
      "string"
    ],
    "prep_time": 0,
    "cook_time": 0,
    "servings": 0,
    "nutrition": {
      "calories": 0,
      "protein_g": 0,
      "fiber_g": 0,
      "carbs_g": 0,
      "fat_g": 0,
      "sodium_mg": 0,
      "iron_mg": 0,
      "magnesium_mg": 0,
      "vitamin_b12_mcg": 0,
      "folate_mcg": 0,
      "vitamin_d_iu": 0,
      "omega3_g": 0,
      "zinc_mg": 0,
      "vitamin_c_mg": 0
    },
    "source_url": "string",
    "source_name": "string",
    "cuisine_type": [
      "string"
    ],
    "meal_type": [
      "string"
    ],
    "dish_type": [
      "string"
    ]
  },
  "emotional_rationale": {
    "overall_rationale": "string",
    "mood_breakdowns": [
      {
        "mood": "string",
        "explanation": "string"
      }
    ],
    "plating_suggestion": "string",
    "journaling_prompt": "string"
  },
  "flavor_alignment": {
    "nutrient_match_score": 0,
    "nutrient_reasons": ["string"],
    "evidence_based": true
  },
  "nutrition_comparison": {
    "recipe_calories": 0,
    "target_calories": 0,
    "recipe_protein": 0,
    "target_protein": 0,
    "recipe_fiber": 0,
    "target_fiber": 0,
    "percentage_of_daily_calories": 0,
    "percentage_of_daily_protein": 0,
    "percentage_of_daily_fiber": 0
  },
  "mood_description": "string"
}
```

---

## 🧮 Nutrition Calculate Endpoint

### Endpoint Details
- **URL:** `POST /api/v1/nutrition/calculate`
- **Description:** Calculate daily nutrition targets based on user profile
- **Response Model:** `NutritionTargets`

### Request Body Schema

```json
{
  "age": 0,
  "gender": "male",
  "height_cm": 1,
  "weight_kg": 1,
  "cuisine_preferences": ["string"],
  "food_allergies": ["string"],
  "dietary_preference": "none",
  "activity_level": "moderate"
}
```

### Response Schema

```json
{
  "calories": 0,
  "protein_g": 0,
  "fiber_g": 0,
  "carbs_g": 0,
  "fat_g": 0,
  "sodium_mg": 0
}
```

---

## 🎭 Mood Interpret Endpoint

### Endpoint Details
- **URL:** `POST /api/v1/mood/interpret`
- **Description:** Interpret mood blend into flavor profile
- **Response Model:** `MoodInterpretation`

### Request Body Schema

```json
{
  "moods": [
    {
      "mood": "stressed",
      "intensity": "medium"
    }
  ],
  "cuisine_preference": "italian"
}
```

### Response Schema

```json
{
  "mood_description": "string",
  "flavor_profile": {
    "flavor_bias": ["string"],
    "texture_preference": ["string"],
    "culinary_tone": ["string"],
    "search_keywords": ["string"]
  }
}
```

---

## 🔍 Health Endpoint

### Endpoint Details
- **URL:** `GET /api/v1/health`
- **Description:** Health check endpoint for monitoring
- **Response Model:** JSON object

### Response Schema

```json
{
  "status": "healthy",
  "version": "2.1.0",
  "service": "SavorMe Backend API",
  "timestamp": "2025-10-05T00:00:00Z"
}
```

---

## 📝 Model Definitions

### RecipeRecommendationRequest Model
**File:** `app/api/routes.py` (lines 196-201)

```python
class RecipeRecommendationRequest(BaseModel):
    """Request model for recipe recommendation"""
    mood_blend: MoodBlend
    user_profile: UserProfile
    nutrition_targets: Optional[NutritionTargets] = None
    activity_level: str = "moderate"
```

### MoodBlend Model
**File:** `app/models/mood.py` (lines 33-43)

```python
class MoodBlend(BaseModel):
    """User's mood blend (1-3 moods)"""
    moods: List[MoodSelection] = Field(..., min_length=1, max_length=3)
```

### MoodSelection Model
**File:** `app/models/mood.py` (lines 24-30)

```python
class MoodSelection(BaseModel):
    """Single mood with intensity"""
    mood: MoodType
    intensity: IntensityLevel
    
    class Config:
        use_enum_values = True
```

### UserProfile Model
**File:** `app/models/user.py` (lines 28-52)

```python
class UserProfile(BaseModel):
    """User personality profile"""
    user_id: Optional[str] = None
    
    # Basic info
    age: int = Field(..., gt=0, le=120)
    gender: Gender
    height_cm: float = Field(..., gt=0, le=300)
    weight_kg: float = Field(..., gt=0, le=500)
    
    # Cultural & preferences
    ethnic_background: Optional[str] = None
    cuisine_preferences: List[str] = Field(default_factory=list)
    
    # Dietary restrictions
    food_allergies: List[str] = Field(default_factory=list)
    dietary_preference: DietaryPreference = DietaryPreference.NONE
    
    # Calculated nutrition targets (optional)
    target_calories: Optional[float] = None
    target_protein_g: Optional[float] = None
    target_fiber_g: Optional[float] = None
    
    class Config:
        use_enum_values = True
```

---

## 🔗 Cross-References

See also:
- **MASTER_FILE_ORGANIZATION.md** - Overall file structure
- **CUSTOMIZATIONS_PERSISTENT.md** - Evidence-based system details
- **BACKEND_TROUBLESHOOTING_FOR_GEMINI.md** - Debugging guide
- **CHATGPT_HELP_REQUEST.md** - Current issue investigation

---

## 📊 Frontend Integration

### Desktop App Request Transform
**File:** `desktop_app/templates/desktop-results.html` (lines 159-197)

The frontend transforms its data into the backend format:

```javascript
function transformToBackendFormat(requestData) {
    const moods = requestData.mood_selections.map(mood => ({
        mood: moodMap[mood] || mood,
        intensity: intensityMap[requestData.mood_intensity] || requestData.mood_intensity
    }));
    
    return {
        mood_blend: {
            moods: moods
        },
        user_profile: {
            age: parseInt(requestData.age),
            gender: requestData.gender,
            height_cm: parseFloat(requestData.height_cm),
            weight_kg: parseFloat(requestData.weight_kg),
            cuisine_preferences: requestData.cuisine_preferences || [],
            food_allergies: requestData.food_allergies || [],
            dietary_preference: requestData.dietary_preference || 'none'
        },
        activity_level: 'moderate'
    };
}
```

---

## ⚠️ Important Notes

1. **Enum Values:** All enum fields accept string values due to `use_enum_values = True` config
2. **Required Fields:** 
   - `mood_blend.moods` - at least 1 mood, maximum 3
   - `user_profile.age`, `gender`, `height_cm`, `weight_kg` - all required
3. **Optional Fields:**
   - `nutrition_targets` - will be calculated if not provided
   - `activity_level` - defaults to "moderate"
   - `user_profile.user_id`, `ethnic_background` - optional

---

*Last Updated: 2025-10-18*
*Backend Version: 2.1.0*

