"""
API Routes for SavorMe Backend
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
import httpx

from app.models.user import UserProfile, NutritionTargets
from app.models.mood import MoodBlend, MoodInterpretation
from app.models.recipe import RecipeRecommendation, Recipe
from app.services.nutrition_calculator import nutrition_calculator
from app.services.fusion_engine import fusion_engine
from app.services.edamam_client import edamam_client
from app.services.openrouter_client import openrouter_client
from app.services.mood_nutrition_engine import get_mood_nutrition_engine
from app.services.fdc_client import fdc_client


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
    2. Interpret mood blend (both emotional AND scientific nutrient-based)
    3. Search for matching recipes
    4. Score recipes using evidence-based nutrient mapping
    5. Generate emotional rationale
    
    Args:
        mood_blend: User's mood selection
        user_profile: User profile
        nutrition_targets: Optional pre-calculated targets
        activity_level: Activity level
    
    Returns:
        Complete recipe recommendation with emotional context and nutrient scoring
    """
    try:
        # Calculate nutrition targets
        if not nutrition_targets:
            nutrition_targets = nutrition_calculator.calculate_nutrition_targets(
                user_profile, activity_level
            )
        
        # Get nutrition engine for evidence-based scoring
        nutrition_engine = get_mood_nutrition_engine()
        
        # Extract mood IDs for nutrient scoring
        mood_ids = [m.mood.value for m in mood_blend.moods]
        
        # Interpret mood (legacy emotional approach)
        mood_interpretation = fusion_engine.interpret_mood_blend(mood_blend)
        
        # Search recipes
        search_params = edamam_client.build_search_query_from_mood(
            mood_interpretation.flavor_profile.search_keywords,
            user_profile,
            nutrition_targets
        )
        
        # Get raw recipe data to access full nutrients
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {
                "type": "public",
                "q": search_params["query"],
                "app_id": edamam_client.app_id,
                "app_key": edamam_client.app_key,
            }
            if search_params.get("cuisine_types"):
                params["cuisineType"] = search_params["cuisine_types"]
            if search_params.get("diet_labels"):
                params["diet"] = search_params["diet_labels"]
            if search_params.get("health_labels"):
                params["health"] = search_params["health_labels"]
            
            response = await client.get(edamam_client.base_url, params=params)
            response.raise_for_status()
            search_results = response.json()
        
        if not search_results.get("hits"):
            raise HTTPException(status_code=404, detail="No recipes found matching criteria")
        
        # Score all recipes using evidence-based nutrition engine
        scored_recipes = []
        for hit in search_results.get("hits", [])[:10]:  # Score top 10
            recipe_data = hit.get("recipe", {})
            
            # Extract full nutrients
            nutrients_raw = edamam_client.extract_full_nutrients_per_serving(recipe_data)
            
            # Canonicalize nutrients
            nutrients_canonical = nutrition_engine.canonicalize_nutrients(nutrients_raw)
            
            # Score recipe
            score, reasons, contributions = nutrition_engine.score_recipe(
                nutrients_canonical,
                mood_ids
            )
            
            scored_recipes.append({
                "recipe_data": recipe_data,
                "score": score,
                "reasons": reasons,
                "contributions": contributions,
                "nutrients": nutrients_canonical
            })
        
        # Sort by score (highest first)
        scored_recipes.sort(key=lambda x: x["score"], reverse=True)
        
        if not scored_recipes:
            raise HTTPException(status_code=404, detail="No recipes found matching criteria")
        
        # Pick best recipe
        best = scored_recipes[0]
        recipe = edamam_client._parse_recipe(best["recipe_data"])
        
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
        
        # Build flavor alignment with evidence-based nutrient scoring
        flavor_alignment = {
            "desired_flavors": mood_interpretation.flavor_profile.flavor_bias,
            "desired_textures": mood_interpretation.flavor_profile.texture_preference,
            "culinary_tone": mood_interpretation.flavor_profile.culinary_tone,
            "nutrient_match_score": round(best["score"] * 100, 1),  # Convert to 0-100 scale
            "nutrient_reasons": best["reasons"],
            "evidence_based": True
        }
        
        # Add scientific explainers and disclaimers
        scientific_explainers = nutrition_engine.get_mood_explainers(mood_ids)
        contraindications = nutrition_engine.get_contraindications(mood_ids)
        disclaimer = nutrition_engine.get_disclaimer()
        
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


@router.post("/nutrition/score-recipe")
async def score_recipe_nutrients(
    recipe_nutrients: Dict[str, float],
    mood_ids: List[str]
):
    """
    Score a recipe's nutrients against mood-based targets (evidence-based)
    
    Args:
        recipe_nutrients: Dict of nutrient names to values (canonical format)
        mood_ids: List of mood IDs (e.g., ["stress", "fatigue"])
    
    Returns:
        Score, reasons, and contributions
    """
    try:
        nutrition_engine = get_mood_nutrition_engine()
        
        score, reasons, contributions = nutrition_engine.score_recipe(
            recipe_nutrients,
            mood_ids
        )
        
        return {
            "score": score,
            "score_percentage": round(score * 100, 1),
            "reasons": reasons,
            "contributions": contributions,
            "explainers": nutrition_engine.get_mood_explainers(mood_ids),
            "contraindications": nutrition_engine.get_contraindications(mood_ids),
            "disclaimer": nutrition_engine.get_disclaimer()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error scoring recipe: {str(e)}")


@router.get("/nutrition/mood-targets/{mood_id}")
async def get_mood_nutrient_targets(mood_id: str):
    """
    Get evidence-based nutrient targets for a specific mood
    
    Args:
        mood_id: Mood identifier (e.g., "stress", "fatigue")
    
    Returns:
        Nutrient targets, explainers, and scientific evidence
    """
    try:
        nutrition_engine = get_mood_nutrition_engine()
        
        if mood_id not in nutrition_engine.moods:
            raise HTTPException(status_code=404, detail=f"Mood '{mood_id}' not found")
        
        mood_def = nutrition_engine.moods[mood_id]
        
        return {
            "mood_id": mood_def.id,
            "aliases": mood_def.aliases,
            "nutrient_targets": [
                {
                    "name": t.name,
                    "unit": t.unit,
                    "min_per_meal": t.min_per_meal,
                    "max_per_meal": t.max_per_meal,
                    "weight": t.weight,
                    "note": t.note
                }
                for t in mood_def.nutrient_targets
            ],
            "patterns": mood_def.patterns,
            "explainers": mood_def.explainers,
            "evidence": mood_def.evidence,
            "contraindications": mood_def.contraindications,
            "disclaimer": nutrition_engine.get_disclaimer()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving mood targets: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    nutrition_engine = get_mood_nutrition_engine()
    return {
        "status": "healthy",
        "service": "SavorMe Backend",
        "version": "0.1.0",
        "mood_mapping_version": nutrition_engine.version,
        "available_moods": list(nutrition_engine.moods.keys())
    }

