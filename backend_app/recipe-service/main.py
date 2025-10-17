"""
Recipe Service
Handles recipe search, scoring, and rotation
"""
import sys
import os
from pathlib import Path
import httpx
import json
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from shared_models import (
    UserProfile, 
    NutritionTargets, 
    Recipe,
    RecipeSearchRequest,
    RecipeSearchResponse,
    Ingredient,
    Nutrition
)

app = FastAPI(
    title="SavorMe Recipe Service",
    description="Handles recipe search, scoring, and variety rotation",
    version="1.0.0"
)


class EdamamClient:
    """Client for Edamam Recipe Search API"""
    
    def __init__(self):
        self.base_url = "https://api.edamam.com/api/recipes/v2"
        self.app_id = os.getenv("EDAMAM_APP_ID")
        self.app_key = os.getenv("EDAMAM_APP_KEY")
    
    # Valid Edamam cuisine types (case-sensitive!)
    # Map lowercase input to Edamam's exact case requirements
    CUISINE_MAPPING = {
        "american": "American",
        "asian": "South East Asian",
        "british": "British",
        "caribbean": "Caribbean",
        "central europe": "Central Europe",
        "chinese": "Chinese",
        "eastern europe": "Eastern Europe",
        "french": "French",
        "greek": "Greek",
        "indian": "Indian",
        "italian": "Italian",
        "japanese": "Japanese",
        "korean": "Korean",
        "kosher": "Kosher",
        "mediterranean": "Mediterranean",
        "mexican": "Mexican",
        "middle eastern": "Middle Eastern",
        "nordic": "Nordic",
        "south american": "South American",
        "south east asian": "South East Asian",
        "thai": "South East Asian",  # Thai is part of South East Asian
        "vietnamese": "South East Asian",  # Vietnamese is part of South East Asian
        "world": "World"
    }
    
    def build_search_params(self, keywords: List[str], user_profile: UserProfile, nutrition_targets: NutritionTargets) -> Dict[str, Any]:
        """Build search parameters for Edamam API"""
        params = {
            "type": "public",
            "q": " ".join(keywords),
            "app_id": self.app_id,
            "app_key": self.app_key,
        }
        
        # Add cuisine filters with proper case mapping
        if user_profile.cuisine_preferences:
            cuisine_input = user_profile.cuisine_preferences[0].lower()
            # Map to Edamam's exact case
            cuisine = self.CUISINE_MAPPING.get(cuisine_input)
            if cuisine:
                params["cuisineType"] = cuisine
            # If invalid, skip cuisine filter rather than failing
        
        # Add dietary restrictions
        if user_profile.dietary_preference != "none":
            params["diet"] = user_profile.dietary_preference
        
        # Add health restrictions (allergies)
        if user_profile.food_allergies:
            for allergy in user_profile.food_allergies:
                params[f"health"] = f"{allergy}-free"
        
        # Add nutrition ranges (25-40% of daily targets for a meal)
        meal_calories = nutrition_targets.calories * 0.30  # 30% of daily
        params["calories"] = f"{meal_calories * 0.7}-{meal_calories * 1.3}"
        
        meal_protein = nutrition_targets.protein_g * 0.25  # 25% of daily
        params["nutrients[PROCNT]"] = f"{meal_protein * 0.7}-{meal_protein * 1.5}"
        
        return params
    
    async def search_recipes(self, keywords: List[str], user_profile: UserProfile, nutrition_targets: NutritionTargets) -> List[Dict]:
        """Search for recipes using Edamam API with fallback logic"""
        params = self.build_search_params(keywords, user_profile, nutrition_targets)
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Try with all filters first
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            hits = data.get("hits", [])
            
            # If no results and cuisine was specified, try without cuisine filter
            if not hits and "cuisineType" in params:
                print(f"No results with cuisine {params['cuisineType']}, retrying without cuisine filter...")
                params_no_cuisine = params.copy()
                del params_no_cuisine["cuisineType"]
                
                response = await client.get(self.base_url, params=params_no_cuisine)
                response.raise_for_status()
                data = response.json()
                hits = data.get("hits", [])
            
            return hits[:10]  # Return top 10 recipes
    
    def parse_recipe(self, recipe_data: Dict) -> Recipe:
        """Parse Edamam recipe data into our Recipe model"""
        # Extract basic info
        recipe_id = recipe_data.get("uri", "").split("_")[-1]
        name = recipe_data.get("label", "Unknown Recipe")
        
        # Get the best available image from Edamam's images object
        images = recipe_data.get("images", {})
        image_url = None
        
        # Try to get the best quality image available
        if images.get("LARGE", {}).get("url"):
            image_url = images["LARGE"]["url"]
        elif images.get("REGULAR", {}).get("url"):
            image_url = images["REGULAR"]["url"]
        elif images.get("SMALL", {}).get("url"):
            image_url = images["SMALL"]["url"]
        elif images.get("THUMBNAIL", {}).get("url"):
            image_url = images["THUMBNAIL"]["url"]
        else:
            # Fallback to the basic image field (often a placeholder)
            image_url = recipe_data.get("image")
        
        # Parse ingredients
        ingredients = []
        for ing in recipe_data.get("ingredients", []):
            ingredients.append(Ingredient(
                name=ing.get("food", ""),
                amount=str(ing.get("quantity", "")),
                unit=ing.get("measure", "")
            ))
        
        # Parse nutrition
        total_nutrients = recipe_data.get("totalNutrients", {})
        yield_count = recipe_data.get("yield", 1)
        
        # Calculate per-serving nutrition
        def get_nutrient_per_serving(nutrient_key: str) -> float:
            nutrient = total_nutrients.get(nutrient_key, {})
            return nutrient.get("quantity", 0.0) / yield_count
        
        nutrition = Nutrition(
            calories=get_nutrient_per_serving("ENERC_KCAL"),
            protein_g=get_nutrient_per_serving("PROCNT"),
            fiber_g=get_nutrient_per_serving("FIBTG"),
            carbs_g=get_nutrient_per_serving("CHOCDF"),
            fat_g=get_nutrient_per_serving("FAT"),
            sodium_mg=get_nutrient_per_serving("NA"),
            # Enhanced nutrients
            magnesium_mg=get_nutrient_per_serving("MG"),
            iron_mg=get_nutrient_per_serving("FE"),
            vitamin_b12_mcg=get_nutrient_per_serving("B12"),
            folate_mcg=get_nutrient_per_serving("FOLDFE"),
            vitamin_d_mcg=get_nutrient_per_serving("VITD"),
            omega_3_g=get_nutrient_per_serving("OMEGA3"),
            zinc_mg=get_nutrient_per_serving("ZN"),
            vitamin_c_mg=get_nutrient_per_serving("VITC")
        )
        
        return Recipe(
            recipe_id=recipe_id,
            name=name,
            image_url=image_url,
            ingredients=ingredients,
            prep_time=recipe_data.get("totalTime"),
            servings=yield_count,
            nutrition=nutrition,
            source_url=recipe_data.get("url"),
            source_name=recipe_data.get("source"),
            cuisine_type=recipe_data.get("cuisineType", []),
            meal_type=recipe_data.get("mealType", []),
            dish_type=recipe_data.get("dishType", [])
        )


class RecipeScorer:
    """Scores recipes based on mood-nutrient targets"""
    
    def __init__(self):
        self.mood_targets = {
            "stressed": {
                "magnesium_mg": {"min": 350, "weight": 1.0},
                "omega_3_g": {"min": 0.5, "weight": 0.9},
                "fiber_g": {"min": 8, "weight": 0.7},
                "added_sugars_g": {"max": 10, "weight": 0.6}
            },
            "fatigued": {
                "iron_mg": {"min": 10, "weight": 1.0},
                "vitamin_b12_mcg": {"min": 2.4, "weight": 0.9},
                "protein_g": {"min": 25, "weight": 0.8},
                "complex_carbs_g": {"min": 30, "weight": 0.7}
            },
            "low_mood": {
                "omega_3_g": {"min": 0.8, "weight": 1.0},
                "fiber_g": {"min": 10, "weight": 0.8},
                "folate_mcg": {"min": 200, "weight": 0.7},
                "vitamin_d_mcg": {"min": 15, "weight": 0.6}
            },
            "irritable": {
                "protein_g": {"min": 30, "weight": 1.0},
                "fiber_g": {"min": 12, "weight": 0.9},
                "zinc_mg": {"min": 8, "weight": 0.7},
                "added_sugars_g": {"max": 8, "weight": 0.8}
            }
        }
    
    def score_recipe(self, recipe: Recipe, mood_ids: List[str]) -> tuple[float, List[str]]:
        """Score recipe against mood-based nutrient targets"""
        score = 0
        reasons = []
        
        for mood_id in mood_ids:
            if mood_id not in self.mood_targets:
                continue
                
            targets = self.mood_targets[mood_id]
            
            for nutrient, target in targets.items():
                recipe_value = getattr(recipe.nutrition, nutrient, 0)
                
                if target.get("min") and recipe_value >= target["min"]:
                    score += 10 * target["weight"]
                    reasons.append(f"✅ High in {nutrient} ({recipe_value:.1f}) - Great for {mood_id}")
                elif target.get("min") and recipe_value >= target["min"] * 0.7:
                    score += 5 * target["weight"]
                    reasons.append(f"⚠️ Moderate {nutrient} ({recipe_value:.1f}) - Good for {mood_id}")
                
                if target.get("max") and recipe_value > target["max"]:
                    score -= 5 * target["weight"]
                    reasons.append(f"❌ High {nutrient} ({recipe_value:.1f}) - May worsen {mood_id}")
        
        return min(score, 100), reasons


edamam_client = EdamamClient()
recipe_scorer = RecipeScorer()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Recipe Service",
        "version": "1.0.0"
    }


@app.post("/recipes/search", response_model=RecipeSearchResponse)
async def search_recipes(request: RecipeSearchRequest):
    """Search and score recipes based on mood and nutrition targets"""
    try:
        # Search for recipes
        recipe_hits = await edamam_client.search_recipes(
            request.search_keywords,
            request.user_profile,
            request.nutrition_targets
        )
        
        if not recipe_hits:
            raise HTTPException(status_code=404, detail="No recipes found")
        
        # Parse and score recipes
        recipes = []
        scored_recipes = []
        
        for hit in recipe_hits:
            recipe_data = hit.get("recipe", {})
            recipe = edamam_client.parse_recipe(recipe_data)
            recipes.append(recipe)
            
            # Score recipe
            score, reasons = recipe_scorer.score_recipe(recipe, request.mood_ids)
            scored_recipes.append((recipe, score, reasons))
        
        # Sort by score and get best recipe
        scored_recipes.sort(key=lambda x: x[1], reverse=True)
        best_recipe, best_score, best_reasons = scored_recipes[0]
        
        return RecipeSearchResponse(
            recipes=recipes,
            best_recipe=best_recipe,
            score=best_score,
            reasons=best_reasons
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching recipes: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get('PORT', 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
