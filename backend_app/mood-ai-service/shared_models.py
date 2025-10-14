"""
Shared Data Models for SavorMe Microservices
These models are used across all services for consistency
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


# ==================== User & Nutrition Models ====================

class ActivityLevel(str, Enum):
    """Activity level for TDEE calculation"""
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"


class UserProfile(BaseModel):
    """User profile with dietary preferences and restrictions"""
    age: int = Field(..., ge=1, le=120, description="Age in years")
    gender: str = Field(..., description="Gender (male/female)")
    height_cm: float = Field(..., ge=50, le=300, description="Height in cm")
    weight_kg: float = Field(..., ge=20, le=500, description="Weight in kg")
    cuisine_preferences: List[str] = Field(default=[], description="Preferred cuisines")
    food_allergies: List[str] = Field(default=[], description="Food allergies")
    dietary_preference: str = Field(default="none", description="Dietary restriction")
    activity_level: ActivityLevel = Field(default=ActivityLevel.MODERATE)


class NutritionTargets(BaseModel):
    """Daily nutrition targets"""
    calories: float = Field(..., description="Daily calorie target")
    protein_g: float = Field(..., description="Daily protein target (grams)")
    fiber_g: float = Field(..., description="Daily fiber target (grams)")
    carbs_g: float = Field(..., description="Daily carbs target (grams)")
    fat_g: float = Field(..., description="Daily fat target (grams)")
    sodium_mg: Optional[float] = Field(None, description="Daily sodium limit (mg)")


# ==================== Mood Models ====================

class MoodType(str, Enum):
    """Evidence-based mood types"""
    STRESSED = "stressed"
    FATIGUED = "fatigued"
    LOW_MOOD = "low_mood"
    IRRITABLE = "irritable"


class IntensityLevel(str, Enum):
    """Mood intensity levels"""
    A_LITTLE = "low"
    MEDIUM = "medium"
    VERY = "high"


class MoodSelection(BaseModel):
    """Single mood with intensity"""
    mood: MoodType
    intensity: IntensityLevel


class MoodBlend(BaseModel):
    """Combination of moods"""
    moods: List[MoodSelection] = Field(..., min_items=1, max_items=3)


class FlavorProfile(BaseModel):
    """Culinary flavor profile derived from mood"""
    flavor_bias: List[str] = Field(default=[])
    texture_preference: List[str] = Field(default=[])
    culinary_tone: List[str] = Field(default=[])
    search_keywords: List[str] = Field(default=[])


class MoodInterpretation(BaseModel):
    """Complete mood interpretation"""
    mood_description: str
    flavor_profile: FlavorProfile
    emotional_context: str


# ==================== Recipe Models ====================

class Ingredient(BaseModel):
    """Recipe ingredient"""
    name: str
    amount: str
    unit: Optional[str] = None


class Nutrition(BaseModel):
    """Nutritional information per serving"""
    calories: float
    protein_g: float
    fiber_g: float
    carbs_g: float
    fat_g: float
    sodium_mg: Optional[float] = None
    
    # Enhanced nutrients
    magnesium_mg: Optional[float] = None
    iron_mg: Optional[float] = None
    vitamin_b12_mcg: Optional[float] = None
    folate_mcg: Optional[float] = None
    vitamin_d_mcg: Optional[float] = None
    omega_3_g: Optional[float] = None
    zinc_mg: Optional[float] = None
    vitamin_c_mg: Optional[float] = None


class Recipe(BaseModel):
    """Complete recipe with metadata"""
    recipe_id: str
    name: str
    image_url: Optional[str] = None
    ingredients: List[Ingredient]
    cooking_directions: List[str] = Field(default=[])
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: int = Field(default=1)
    nutrition: Nutrition
    source_url: Optional[str] = None
    source_name: Optional[str] = None
    cuisine_type: List[str] = Field(default=[])
    meal_type: List[str] = Field(default=[])
    dish_type: List[str] = Field(default=[])


class RecipeRecommendation(BaseModel):
    """Complete recipe recommendation with context"""
    recipe: Recipe
    emotional_rationale: str
    flavor_alignment: Dict[str, Any]
    nutrition_comparison: Dict[str, Any]
    mood_description: str


# ==================== Service Communication Models ====================

class NutritionCalculationRequest(BaseModel):
    """Request for nutrition calculation"""
    user_profile: UserProfile


class NutritionCalculationResponse(BaseModel):
    """Response from nutrition service"""
    nutrition_targets: NutritionTargets
    bmr: float
    tdee: float


class MoodInterpretationRequest(BaseModel):
    """Request for mood interpretation"""
    mood_blend: MoodBlend
    cuisine_preference: Optional[str] = None


class MoodInterpretationResponse(BaseModel):
    """Response from mood service"""
    interpretation: MoodInterpretation


class RecipeSearchRequest(BaseModel):
    """Request for recipe search"""
    search_keywords: List[str]
    user_profile: UserProfile
    nutrition_targets: NutritionTargets
    mood_ids: List[str]


class RecipeSearchResponse(BaseModel):
    """Response from recipe service"""
    recipes: List[Recipe]
    best_recipe: Recipe
    score: float
    reasons: List[str]


class AIContentRequest(BaseModel):
    """Request for AI-generated content"""
    recipe: Recipe
    mood_interpretation: MoodInterpretation
    task: str  # "rationale" or "directions"


class AIContentResponse(BaseModel):
    """Response from AI service"""
    content: Any  # str for rationale, List[str] for directions

