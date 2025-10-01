"""
API Routes for SavorMe Backend
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from app.models.user import UserProfile, NutritionTargets
from app.models.mood import MoodBlend, MoodInterpretation
from app.models.recipe import RecipeRecommendation, Recipe
from app.services.nutrition_calculator import nutrition_calculator
from app.services.fusion_engine import fusion_engine
from app.services.edamam_client import edamam_client
from app.services.openrouter_client import openrouter_client


router = APIRouter()


@router.post("/nutrition/calculate", response_model=NutritionTargets)
async def calculate_nutrition_targets(profile: UserProfile, activity_level: str = "moderate"):
    """
    Calculate daily nutrition targets based on user profile
    
    Args:
        profile: User profile with age, gender, height, weight
        activity_level: Activity level (sedentary, light, moderate, active, very_active)
    
    Returns:
        Nutrition targets including calories, protein, fiber
    """
    try:
        targets = nutrition_calculator.calculate_nutrition_targets(profile, activity_level)
        return targets
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating nutrition: {str(e)}")


@router.post("/mood/interpret", response_model=MoodInterpretation)
async def interpret_mood(mood_blend: MoodBlend):
    """
    Interpret mood blend and generate flavor profile
    
    Args:
        mood_blend: User's selected moods with intensity levels
    
    Returns:
        Mood interpretation with flavor profile and search keywords
    """
    try:
        interpretation = fusion_engine.interpret_mood_blend(mood_blend)
        return interpretation
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error interpreting mood: {str(e)}")


@router.post("/recipes/search", response_model=List[Recipe])
async def search_recipes(
    mood_blend: MoodBlend,
    user_profile: UserProfile,
    nutrition_targets: Optional[NutritionTargets] = None,
    activity_level: str = "moderate"
):
    """
    Search for recipes based on mood, user profile, and nutrition targets
    
    Args:
        mood_blend: User's mood selection
        user_profile: User profile with preferences and restrictions
        nutrition_targets: Optional pre-calculated nutrition targets
        activity_level: Activity level for nutrition calculation
    
    Returns:
        List of matching recipes
    """
    try:
        # Calculate nutrition targets if not provided
        if not nutrition_targets:
            nutrition_targets = nutrition_calculator.calculate_nutrition_targets(
                user_profile, activity_level
            )
        
        # Interpret mood into flavor profile
        mood_interpretation = fusion_engine.interpret_mood_blend(mood_blend)
        
        # Build search parameters
        search_params = edamam_client.build_search_query_from_mood(
            mood_interpretation.flavor_profile.search_keywords,
            user_profile,
            nutrition_targets
        )
        
        # Search recipes
        recipes = await edamam_client.search_recipes(**search_params)
        
        return recipes
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching recipes: {str(e)}")


@router.post("/recipes/recommend", response_model=RecipeRecommendation)
async def get_recipe_recommendation(
    mood_blend: MoodBlend,
    user_profile: UserProfile,
    nutrition_targets: Optional[NutritionTargets] = None,
    activity_level: str = "moderate"
):
    """
    Get complete recipe recommendation with emotional rationale
    
    This is the main endpoint that combines all services:
    1. Calculate nutrition targets
    2. Interpret mood blend
    3. Search for matching recipe
    4. Generate emotional rationale
    
    Args:
        mood_blend: User's mood selection
        user_profile: User profile
        nutrition_targets: Optional pre-calculated targets
        activity_level: Activity level
    
    Returns:
        Complete recipe recommendation with emotional context
    """
    try:
        # Calculate nutrition targets
        if not nutrition_targets:
            nutrition_targets = nutrition_calculator.calculate_nutrition_targets(
                user_profile, activity_level
            )
        
        # Interpret mood
        mood_interpretation = fusion_engine.interpret_mood_blend(mood_blend)
        
        # Search recipes
        search_params = edamam_client.build_search_query_from_mood(
            mood_interpretation.flavor_profile.search_keywords,
            user_profile,
            nutrition_targets
        )
        
        recipes = await edamam_client.search_recipes(**search_params)
        
        if not recipes:
            raise HTTPException(status_code=404, detail="No recipes found matching criteria")
        
        # Pick best recipe (first one for now)
        recipe = recipes[0]
        
        # Generate emotional rationale
        emotional_rationale = await openrouter_client.generate_emotional_rationale(
            recipe, mood_interpretation
        )
        
        # Build nutrition comparison
        nutrition_comparison = {
            "recipe_calories": recipe.nutrition.calories,
            "target_calories": nutrition_targets.calories,
            "recipe_protein": recipe.nutrition.protein_g,
            "target_protein": nutrition_targets.protein_g,
            "recipe_fiber": recipe.nutrition.fiber_g,
            "target_fiber": nutrition_targets.fiber_g,
            "percentage_of_daily_calories": round((recipe.nutrition.calories / nutrition_targets.calories) * 100, 1),
            "percentage_of_daily_protein": round((recipe.nutrition.protein_g / nutrition_targets.protein_g) * 100, 1),
            "percentage_of_daily_fiber": round((recipe.nutrition.fiber_g / nutrition_targets.fiber_g) * 100, 1)
        }
        
        # Build flavor alignment
        flavor_alignment = {
            "desired_flavors": mood_interpretation.flavor_profile.flavor_bias,
            "desired_textures": mood_interpretation.flavor_profile.texture_preference,
            "culinary_tone": mood_interpretation.flavor_profile.culinary_tone,
            "match_score": 85  # TODO: Implement actual matching algorithm
        }
        
        return RecipeRecommendation(
            recipe=recipe,
            emotional_rationale=emotional_rationale,
            flavor_alignment=flavor_alignment,
            nutrition_comparison=nutrition_comparison,
            mood_description=mood_interpretation.mood_description
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendation: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SavorMe Backend",
        "version": "0.1.0"
    }

