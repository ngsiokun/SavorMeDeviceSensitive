"""
API Routes for SavorMe Backend
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
import httpx
import random

from app.models.user import UserProfile, NutritionTargets
from app.models.mood import MoodBlend, MoodInterpretation
from app.models.recipe import RecipeRecommendation, Recipe
from app.services.nutrition_calculator import nutrition_calculator
from app.services.fusion_engine import fusion_engine
from app.services.edamam_client import edamam_client
from app.services.openrouter_client import openrouter_client
from app.services.mood_nutrition_engine import get_mood_nutrition_engine
from app.services.canva_client import canva_client


router = APIRouter()

# Simple in-memory variety tracking (in production, use Redis or database)
recent_keywords = []
recent_ingredients = []  # Track individual ingredients for better variety


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
async def interpret_mood(mood_blend: MoodBlend, cuisine_preference: str = None):
    """
    Interpret mood blend and generate flavor profile with variety enhancement
    
    Args:
        mood_blend: User's selected moods with intensity levels
        cuisine_preference: Optional cuisine preference for better personalization
    
    Returns:
        Mood interpretation with flavor profile and search keywords
    """
    try:
        interpretation = fusion_engine.interpret_mood_blend(mood_blend, cuisine_preference)
        
        # Variety enhancement: avoid repeating recent keywords and ingredients
        global recent_keywords, recent_ingredients
        
        # Extract ingredients from keywords for ingredient-level tracking
        current_ingredients = []
        for keyword in interpretation.search_keywords:
            # Split compound keywords and extract individual ingredients
            if " " in keyword:
                current_ingredients.extend(keyword.split())
            else:
                current_ingredients.append(keyword)
        
        # Filter out recently used ingredients (more aggressive variety)
        if recent_ingredients:
            filtered_keywords = []
            for keyword in interpretation.search_keywords:
                keyword_ingredients = keyword.split() if " " in keyword else [keyword]
                # Skip if any ingredient in this keyword was recently used
                # Also temporarily ban salmon if it's been used recently
                if (not any(ingredient in recent_ingredients for ingredient in keyword_ingredients) and
                    "salmon" not in keyword.lower()):
                    filtered_keywords.append(keyword)
            
            # If we filtered out too many, allow some through but prioritize variety
            if filtered_keywords:
                interpretation.search_keywords = filtered_keywords
            else:
                # Fallback: allow keywords but prioritize those with fewer recent ingredients
                interpretation.search_keywords = sorted(
                    interpretation.search_keywords,
                    key=lambda kw: sum(1 for ing in kw.split() if ing in recent_ingredients)
                )
        
        # Track current keywords and ingredients for future requests
        recent_keywords.extend(interpretation.search_keywords)
        recent_keywords = recent_keywords[-10:]  # Keep only last 10 keywords
        
        recent_ingredients.extend(current_ingredients)
        recent_ingredients = recent_ingredients[-15:]  # Keep only last 15 ingredients
        
        return interpretation
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error interpreting mood: {str(e)}")


@router.post("/variety/reset")
async def reset_variety_tracking():
    """
    Reset variety tracking for testing purposes
    """
    global recent_keywords, recent_ingredients
    recent_keywords = []
    recent_ingredients = []
    return {"message": "Variety tracking reset successfully"}


@router.get("/variety/status")
async def get_variety_status():
    """
    Get current variety tracking status for debugging
    """
    global recent_keywords, recent_ingredients
    return {
        "recent_keywords": recent_keywords,
        "recent_ingredients": recent_ingredients,
        "keyword_count": len(recent_keywords),
        "ingredient_count": len(recent_ingredients)
    }


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
        
        # Interpret mood into flavor profile (with cuisine preference for better keyword selection)
        cuisine_pref = user_profile.cuisine_preferences[0] if user_profile.cuisine_preferences else None
        mood_interpretation = fusion_engine.interpret_mood_blend(mood_blend, cuisine_pref)
        
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
        mood_ids = [m.mood if isinstance(m.mood, str) else m.mood.value for m in mood_blend.moods]
        
        # Interpret mood with cuisine preference for better keyword selection
        cuisine_pref = user_profile.cuisine_preferences[0] if user_profile.cuisine_preferences else None
        mood_interpretation = fusion_engine.interpret_mood_blend(mood_blend, cuisine_pref)
        
        # Search recipes
        search_params = edamam_client.build_search_query_from_mood(
            mood_interpretation.flavor_profile.search_keywords,
            user_profile,
            nutrition_targets
        )
        
        # Debug logging
        print(f"Search keywords: {mood_interpretation.flavor_profile.search_keywords}")
        print(f"Search params: {search_params}")
        
        # Get raw recipe data to access full nutrients
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Build params as list of tuples to support multiple values per key
            params = [
                ("type", "public"),
                ("q", search_params["query"]),
                ("app_id", edamam_client.app_id),
                ("app_key", edamam_client.app_key),
            ]
            
            # Add cuisine types (multiple values)
            if search_params.get("cuisine_types"):
                for cuisine in search_params["cuisine_types"]:
                    params.append(("cuisineType", cuisine))
            
            # Add diet labels (multiple values)
            if search_params.get("diet_labels"):
                for diet in search_params["diet_labels"]:
                    params.append(("diet", diet))
            
            # Add health labels (multiple values)
            if search_params.get("health_labels"):
                for health in search_params["health_labels"]:
                    params.append(("health", health))
            
            # Add other filters
            if search_params.get("calories_range"):
                params.append(("calories", search_params["calories_range"]))
            if search_params.get("protein_range"):
                params.append(("nutrients[PROCNT]", search_params["protein_range"]))
            
            print(f"Edamam API request params: {params}")
            response = await client.get(edamam_client.base_url, params=params)
            response.raise_for_status()
            search_results = response.json()
            print(f"Edamam API response hits: {len(search_results.get('hits', []))}")
        
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
        
        # Generate cooking directions if not available or just a link
        if (not recipe.cooking_directions or 
            len(recipe.cooking_directions) == 0 or
            "Full instructions available" in recipe.cooking_directions[0]):
            
            cooking_directions = await openrouter_client.generate_cooking_directions(
                recipe_name=recipe.name,
                ingredients=recipe.ingredients,
                cuisine_type=recipe.cuisine_type
            )
            recipe.cooking_directions = cooking_directions
        
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


@router.post("/design/recipe-card")
async def create_recipe_card_design(recipe: Recipe):
    """
    Create a beautiful recipe card design using Canva
    
    Args:
        recipe: Recipe data to design
        
    Returns:
        Design URL and metadata
    """
    try:
        recipe_data = {
            "name": recipe.name,
            "ingredients": recipe.ingredients,
            "nutrition": {
                "calories": recipe.nutrition.calories,
                "protein_g": recipe.nutrition.protein_g,
                "fiber_g": recipe.nutrition.fiber_g
            },
            "servings": recipe.servings
        }
        
        design_url = await canva_client.create_recipe_card(recipe_data)
        
        if design_url:
            return {
                "success": True,
                "design_url": design_url,
                "recipe_name": recipe.name,
                "message": "Recipe card design created successfully"
            }
        else:
            return {
                "success": False,
                "message": "Failed to create recipe card design"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating recipe card: {str(e)}")


@router.post("/design/mood-card")
async def create_mood_card_design(mood_data: Dict[str, Any]):
    """
    Create a mood selection card design
    
    Args:
        mood_data: Mood information including name, description, evidence level
        
    Returns:
        Design URL and metadata
    """
    try:
        design_url = await canva_client.create_mood_selection_card(mood_data)
        
        if design_url:
            return {
                "success": True,
                "design_url": design_url,
                "mood_name": mood_data.get("name"),
                "message": "Mood card design created successfully"
            }
        else:
            return {
                "success": False,
                "message": "Failed to create mood card design"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating mood card: {str(e)}")


@router.post("/design/nutrition-card")
async def create_nutrition_card_design(nutrition_data: Dict[str, Any]):
    """
    Create a nutrition information card design
    
    Args:
        nutrition_data: Nutrition information including targets and actual values
        
    Returns:
        Design URL and metadata
    """
    try:
        design_url = await canva_client.create_nutrition_info_card(nutrition_data)
        
        if design_url:
            return {
                "success": True,
                "design_url": design_url,
                "message": "Nutrition card design created successfully"
            }
        else:
            return {
                "success": False,
                "message": "Failed to create nutrition card design"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating nutrition card: {str(e)}")


@router.get("/design/templates")
async def get_canva_templates():
    """
    Get available Canva templates
    
    Returns:
        List of available templates
    """
    try:
        templates = await canva_client.get_templates()
        return {
            "success": True,
            "templates": templates,
            "count": len(templates)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting templates: {str(e)}")


@router.post("/design/download")
async def download_design(design_url: str):
    """
    Download a design as image data
    
    Args:
        design_url: URL of the design to download
        
    Returns:
        Base64 encoded image data
    """
    try:
        image_data = await canva_client.download_design(design_url)
        
        if image_data:
            # Convert to base64 for JSON response
            base64_data = base64.b64encode(image_data).decode('utf-8')
            return {
                "success": True,
                "image_data": base64_data,
                "format": "base64",
                "size": len(image_data)
            }
        else:
            return {
                "success": False,
                "message": "Failed to download design"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading design: {str(e)}")

