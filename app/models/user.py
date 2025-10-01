"""
User profile models
"""
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum


class Gender(str, Enum):
    """User gender options"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class DietaryPreference(str, Enum):
    """Dietary preferences"""
    NONE = "none"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    PESCATARIAN = "pescatarian"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"
    KETO = "keto"
    PALEO = "paleo"


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
    
    # Calculated nutrition targets (will be filled by backend)
    target_calories: Optional[float] = None
    target_protein_g: Optional[float] = None
    target_fiber_g: Optional[float] = None
    
    class Config:
        use_enum_values = True


class NutritionTargets(BaseModel):
    """Calculated daily nutrition targets"""
    calories: float
    protein_g: float
    fiber_g: float
    
    # Optional detailed breakdown
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    sodium_mg: Optional[float] = None

