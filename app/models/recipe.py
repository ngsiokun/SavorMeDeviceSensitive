"""
Recipe models
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    """Recipe ingredient"""
    name: str
    amount: str
    unit: Optional[str] = None


class NutritionInfo(BaseModel):
    """Nutrition information for a recipe"""
    calories: float
    protein_g: float
    fiber_g: float
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    sodium_mg: Optional[float] = None


class Recipe(BaseModel):
    """Complete recipe structure"""
    recipe_id: Optional[str] = None
    name: str
    image_url: Optional[str] = None
    
    # Recipe details
    ingredients: List[Ingredient]
    cooking_directions: List[str]
    prep_time: Optional[int] = None  # minutes
    cook_time: Optional[int] = None  # minutes
    servings: Optional[int] = None
    
    # Nutrition
    nutrition: NutritionInfo
    
    # Source
    source_url: Optional[str] = None
    source_name: Optional[str] = None
    
    # Tags
    cuisine_type: List[str] = Field(default_factory=list)
    meal_type: List[str] = Field(default_factory=list)
    dish_type: List[str] = Field(default_factory=list)


class EmotionalRationale(BaseModel):
    """LLM-generated emotional explanation"""
    overall_rationale: str
    mood_breakdowns: List[Dict[str, str]]  # [{mood: "dreamy", explanation: "..."}]
    plating_suggestion: str
    journaling_prompt: str


class RecipeRecommendation(BaseModel):
    """Complete recipe recommendation with emotional context"""
    recipe: Recipe
    emotional_rationale: EmotionalRationale
    flavor_alignment: Dict[str, Any]  # How recipe aligns with mood
    nutrition_comparison: Dict[str, Any]  # Recipe vs user targets
    mood_description: str  # For image generation

