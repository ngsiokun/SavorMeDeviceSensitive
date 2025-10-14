"""
SavorMe API Gateway
Orchestrates communication between microservices
"""
import sys
from pathlib import Path
import httpx
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

# Add shared models to path
sys.path.append(str(Path(__file__).parent.parent / "backend_app" / "shared"))

from shared.models import (
    UserProfile,
    MoodBlend,
    RecipeRecommendation,
    Recipe,
    MoodInterpretation,
    NutritionTargets
)

app = FastAPI(
    title="SavorMe API Gateway",
    description="Orchestrates microservices for mood-based recipe recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs - Cloud Run microservices
USER_NUTRITION_SERVICE_URL = "https://savorme-user-nutrition-662773309683.us-central1.run.app"
RECIPE_SERVICE_URL = "https://savorme-recipe-662773309683.us-central1.run.app"
MOOD_AI_SERVICE_URL = "https://savorme-mood-ai-662773309683.us-central1.run.app"


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Check all services
    service_status = {}
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Check user-nutrition service
            response = await client.get(f"{USER_NUTRITION_SERVICE_URL}/health")
            service_status["user_nutrition"] = response.json()["status"]
    except:
        service_status["user_nutrition"] = "unhealthy"
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Check recipe service
            response = await client.get(f"{RECIPE_SERVICE_URL}/health")
            service_status["recipe"] = response.json()["status"]
    except:
        service_status["recipe"] = "unhealthy"
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Check mood-ai service
            response = await client.get(f"{MOOD_AI_SERVICE_URL}/health")
            service_status["mood_ai"] = response.json()["status"]
    except:
        service_status["mood_ai"] = "unhealthy"
    
    overall_status = "healthy" if all(status == "healthy" for status in service_status.values()) else "degraded"
    
    return {
        "status": overall_status,
        "service": "SavorMe API Gateway",
        "version": "1.0.0",
        "services": service_status
    }


@app.post("/nutrition/calculate", response_model=NutritionTargets)
async def calculate_nutrition_targets(profile: UserProfile):
    """Calculate daily nutrition targets"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{USER_NUTRITION_SERVICE_URL}/nutrition/calculate",
                json={"user_profile": profile.model_dump(mode='json')}
            )
            response.raise_for_status()
            data = response.json()
            return NutritionTargets(**data["nutrition_targets"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating nutrition: {str(e)}")


@app.post("/mood/interpret", response_model=MoodInterpretation)
async def interpret_mood(mood_blend: MoodBlend, cuisine_preference: str = None):
    """Interpret mood blend and generate flavor profile"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{MOOD_AI_SERVICE_URL}/mood/interpret",
                json={
                    "mood_blend": mood_blend.model_dump(mode='json'),
                    "cuisine_preference": cuisine_preference
                }
            )
            response.raise_for_status()
            data = response.json()
            return MoodInterpretation(**data["interpretation"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interpreting mood: {str(e)}")


@app.post("/recipes/search", response_model=List[Recipe])
async def search_recipes(
    mood_blend: MoodBlend,
    user_profile: UserProfile,
    nutrition_targets: Optional[NutritionTargets] = None
):
    """Search for recipes based on mood and profile"""
    try:
        # Calculate nutrition targets if not provided
        if not nutrition_targets:
            nutrition_targets = await calculate_nutrition_targets(user_profile)
        
        # Interpret mood
        mood_interpretation = await interpret_mood(mood_blend, user_profile.cuisine_preferences[0] if user_profile.cuisine_preferences else None)
        
        # Extract mood IDs
        mood_ids = [m.mood.value for m in mood_blend.moods]
        
        # Search recipes
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{RECIPE_SERVICE_URL}/recipes/search",
                json={
                    "search_keywords": mood_interpretation.flavor_profile.search_keywords,
                    "user_profile": user_profile.model_dump(mode='json'),
                    "nutrition_targets": nutrition_targets.model_dump(mode='json'),
                    "mood_ids": mood_ids
                }
            )
            response.raise_for_status()
            data = response.json()
            return [Recipe(**recipe) for recipe in data["recipes"]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching recipes: {str(e)}")


@app.post("/recipes/recommend", response_model=RecipeRecommendation)
async def get_recipe_recommendation(
    mood_blend: MoodBlend,
    user_profile: UserProfile,
    nutrition_targets: Optional[NutritionTargets] = None
):
    """Get complete recipe recommendation with emotional rationale"""
    try:
        # Step 1: Calculate nutrition targets
        if not nutrition_targets:
            nutrition_targets = await calculate_nutrition_targets(user_profile)
        
        # Step 2: Interpret mood
        mood_interpretation = await interpret_mood(mood_blend, user_profile.cuisine_preferences[0] if user_profile.cuisine_preferences else None)
        
        # Step 3: Search and score recipes
        mood_ids = [m.mood.value for m in mood_blend.moods]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            recipe_search_request = {
                "search_keywords": mood_interpretation.flavor_profile.search_keywords,
                "user_profile": user_profile.model_dump(mode='json'),
                "nutrition_targets": nutrition_targets.model_dump(mode='json'),
                "mood_ids": mood_ids
            }
            
            response = await client.post(
                f"{RECIPE_SERVICE_URL}/recipes/search",
                json=recipe_search_request
            )
            response.raise_for_status()
            data = response.json()
            
            best_recipe = Recipe(**data["best_recipe"])
            score = data["score"]
            reasons = data["reasons"]
        
        # Step 4: Generate AI content
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Generate emotional rationale
            response = await client.post(
                f"{MOOD_AI_SERVICE_URL}/ai/generate-content",
                json={
                    "recipe": best_recipe.model_dump(mode='json'),
                    "mood_interpretation": mood_interpretation.model_dump(mode='json'),
                    "task": "rationale"
                }
            )
            response.raise_for_status()
            rationale_data = response.json()
            emotional_rationale = rationale_data["content"]
            
            # Generate cooking directions if needed
            if not best_recipe.cooking_directions:
                response = await client.post(
                    f"{MOOD_AI_SERVICE_URL}/ai/generate-content",
                    json={
                        "recipe": best_recipe.model_dump(mode='json'),
                        "mood_interpretation": mood_interpretation.model_dump(mode='json'),
                        "task": "directions"
                    }
                )
                response.raise_for_status()
                directions_data = response.json()
                best_recipe.cooking_directions = directions_data["content"]
        
        # Step 5: Build response
        nutrition_comparison = {
            "recipe_calories": best_recipe.nutrition.calories,
            "target_calories": nutrition_targets.calories,
            "recipe_protein": best_recipe.nutrition.protein_g,
            "target_protein": nutrition_targets.protein_g,
            "recipe_fiber": best_recipe.nutrition.fiber_g,
            "target_fiber": nutrition_targets.fiber_g,
            "percentage_of_daily_calories": round((best_recipe.nutrition.calories / nutrition_targets.calories) * 100, 1),
            "percentage_of_daily_protein": round((best_recipe.nutrition.protein_g / nutrition_targets.protein_g) * 100, 1),
            "percentage_of_daily_fiber": round((best_recipe.nutrition.fiber_g / nutrition_targets.fiber_g) * 100, 1)
        }
        
        flavor_alignment = {
            "desired_flavors": mood_interpretation.flavor_profile.flavor_bias,
            "desired_textures": mood_interpretation.flavor_profile.texture_preference,
            "culinary_tone": mood_interpretation.flavor_profile.culinary_tone,
            "nutrient_match_score": round(min(score, 100), 1),
            "nutrient_reasons": reasons,
            "evidence_based": True
        }
        
        return RecipeRecommendation(
            recipe=best_recipe,
            emotional_rationale=emotional_rationale,
            flavor_alignment=flavor_alignment,
            nutrition_comparison=nutrition_comparison,
            mood_description=mood_interpretation.mood_description
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendation: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "SavorMe API Gateway", "version": "1.0.0", "docs": "/docs"}


# API v1 endpoints for frontend compatibility
@app.post("/api/v1/recipes/recommend", response_model=RecipeRecommendation)
async def api_v1_get_recipe_recommendation(
    mood_blend: MoodBlend,
    user_profile: UserProfile,
    nutrition_targets: Optional[NutritionTargets] = None,
    activity_level: str = "moderate"
):
    """API v1 endpoint for recipe recommendations"""
    return await get_recipe_recommendation(mood_blend, user_profile, nutrition_targets)


@app.get("/api/v1/health")
async def api_v1_health_check():
    """API v1 health check endpoint"""
    return await health_check()


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
