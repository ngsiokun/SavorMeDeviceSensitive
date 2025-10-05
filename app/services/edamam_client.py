"""
Edamam Recipe Search API Client
https://developer.edamam.com/edamam-recipe-api
"""
import httpx
from typing import List, Optional, Dict, Any
from app.core.config import settings
from app.models.recipe import Recipe, Ingredient, NutritionInfo
from app.models.user import UserProfile, NutritionTargets
from typing import Dict, Any


class EdamamClient:
    """Client for Edamam Recipe Search API"""
    
    def __init__(self):
        self.base_url = settings.EDAMAM_BASE_URL
        self.app_id = settings.EDAMAM_APP_ID
        self.app_key = settings.EDAMAM_APP_KEY
    
    async def search_recipes(
        self,
        query: str,
        cuisine_types: Optional[List[str]] = None,
        diet_labels: Optional[List[str]] = None,
        health_labels: Optional[List[str]] = None,
        excluded_ingredients: Optional[List[str]] = None,
        calories_range: Optional[str] = None,  # e.g., "400-600"
        protein_range: Optional[str] = None,   # e.g., "20-40"
        max_results: int = 10
    ) -> List[Recipe]:
        """
        Search for recipes using Edamam API
        
        Args:
            query: Search keywords (from fusion engine)
            cuisine_types: List of cuisine types (e.g., ["Japanese", "Italian"])
            diet_labels: Dietary preferences (e.g., ["vegetarian", "vegan"])
            health_labels: Health restrictions (e.g., ["peanut-free", "gluten-free"])
            excluded_ingredients: Ingredients to exclude
            calories_range: Calorie range filter
            protein_range: Protein range filter
            max_results: Maximum number of results
        
        Returns:
            List of Recipe objects
        """
        if not self.app_id or not self.app_key:
            raise ValueError("Edamam API credentials not configured")
        
        # Build query parameters as list of tuples to support multiple values
        params = [
            ("type", "public"),
            ("q", query),
            ("app_id", self.app_id),
            ("app_key", self.app_key),
        ]
        
        # Add cuisine types (multiple values supported)
        if cuisine_types:
            for cuisine in cuisine_types:
                params.append(("cuisineType", cuisine))
        
        # Add diet labels (multiple values supported)
        if diet_labels:
            for diet in diet_labels:
                params.append(("diet", diet))
        
        # Add health labels (multiple values supported)
        if health_labels:
            for health in health_labels:
                params.append(("health", health))
        
        # Add excluded ingredients (multiple values supported)
        if excluded_ingredients:
            for excluded in excluded_ingredients:
                params.append(("excluded", excluded))
        
        # Add calorie and protein ranges
        if calories_range:
            params.append(("calories", calories_range))
        
        if protein_range:
            params.append(("nutrients[PROCNT]", protein_range))
        
        # Ensure we get detailed nutritional data including micronutrients
        # The 'field' parameter specifies which fields to include in the response
        fields_to_include = [
            "uri", "label", "image", "images", "source", "url", "shareAs", 
            "yield", "dietLabels", "healthLabels", "cautions", 
            "ingredientLines", "ingredients", "calories", "totalNutrients", 
            "totalDaily", "totalWeight", "cuisineType", "mealType", "dishType"
        ]
        
        for field in fields_to_include:
            params.append(("field", field))
        
        # Make API request
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
        
        # Parse recipes
        recipes = []
        for hit in data.get("hits", [])[:max_results]:
            recipe_data = hit.get("recipe", {})
            recipe = self._parse_recipe(recipe_data)
            recipes.append(recipe)
        
        return recipes
    
    def _parse_recipe(self, recipe_data: Dict[str, Any]) -> Recipe:
        """Parse Edamam recipe response into Recipe model"""
        
        # Validate and potentially filter image URL
        image_url = self._validate_recipe_image(recipe_data.get("image"), recipe_data.get("label", ""))
        
        # Parse ingredients
        ingredients = []
        for ing_data in recipe_data.get("ingredients", []):
            ingredient = Ingredient(
                name=ing_data.get("food", ""),
                amount=ing_data.get("text", ""),
                unit=ing_data.get("measure", "")
            )
            ingredients.append(ingredient)
        
        # Parse nutrition (totalNutrients contains total amounts for entire recipe)
        nutrients = recipe_data.get("totalNutrients", {})
        servings = float(recipe_data.get("yield", 1))
        
        # Calculate per-serving values
        nutrition = NutritionInfo(
            calories=nutrients.get("ENERC_KCAL", {}).get("quantity", 0) / servings,
            protein_g=nutrients.get("PROCNT", {}).get("quantity", 0) / servings,
            fiber_g=nutrients.get("FIBTG", {}).get("quantity", 0) / servings,
            carbs_g=nutrients.get("CHOCDF", {}).get("quantity", 0) / servings,
            fat_g=nutrients.get("FAT", {}).get("quantity", 0) / servings,
            sodium_mg=nutrients.get("NA", {}).get("quantity", 0) / servings
        )
        
        # Note: Edamam doesn't always provide cooking directions
        # We'll use the source URL for full instructions
        cooking_directions = []
        if recipe_data.get("url"):
            cooking_directions = [
                f"Full instructions available at: {recipe_data.get('url')}"
            ]
        
        recipe = Recipe(
            recipe_id=recipe_data.get("uri", "").split("#")[-1],
            name=recipe_data.get("label", "Untitled Recipe"),
            image_url=image_url,
            ingredients=ingredients,
            cooking_directions=cooking_directions,
            prep_time=None,  # Not provided by Edamam
            cook_time=recipe_data.get("totalTime"),
            servings=int(recipe_data.get("yield", 1)),
            nutrition=nutrition,
            source_url=recipe_data.get("url"),
            source_name=recipe_data.get("source"),
            cuisine_type=recipe_data.get("cuisineType", []),
            meal_type=recipe_data.get("mealType", []),
            dish_type=recipe_data.get("dishType", [])
        )
        
        return recipe
    
    def _validate_recipe_image(self, image_url: str, recipe_name: str) -> str:
        """
        Validate recipe image URL and provide fallback if image appears generic/abstract
        
        Args:
            image_url: Original image URL from Edamam
            recipe_name: Recipe name for context
            
        Returns:
            Validated image URL or None if image appears generic
        """
        if not image_url:
            return None
        
        # Only filter out obvious non-food images
        generic_patterns = [
            "placeholder",
            "default",
            "abstract",
            "heart",  # Like the heart shape you saw
            "metallic",
            "decorative",
            "ornament",
            "artistic"
        ]
        
        # Check URL and recipe name for generic indicators
        image_url_lower = image_url.lower()
        recipe_name_lower = recipe_name.lower()
        
        # Skip if URL contains generic patterns
        for pattern in generic_patterns:
            if pattern in image_url_lower:
                return None
        
        # Skip if recipe name suggests the image might be generic
        # (This is a heuristic - in practice, you might want to be more specific)
        
        # Be more permissive with Edamam images - they usually have food photos
        # Only filter out the most obvious non-food patterns
        return image_url
    
    def extract_full_nutrients_per_serving(self, recipe_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract comprehensive nutrients from Edamam recipe for nutrition scoring
        
        Returns nutrients per serving in raw format (to be canonicalized by nutrition engine)
        """
        nutrients_raw = {}
        total_nutrients = recipe_data.get("totalNutrients", {})
        servings = float(recipe_data.get("yield", 1))
        
        # Debug: Log available nutrients from Edamam
        print(f"DEBUG: Available nutrients from Edamam: {list(total_nutrients.keys())}")
        print(f"DEBUG: Recipe yield: {servings}")
        
        # Edamam nutrient code mapping - Complete micronutrient coverage
        nutrient_map = {
            # Macronutrients
            "ENERC_KCAL": "calories",
            "PROCNT": "protein",
            "CHOCDF": "carbohydrate_by_difference",
            "FIBTG": "fiber",
            "FAT": "total_fat",
            "SUGAR": "sugars_total",
            "SUGAR.added": "added_sugars",
            
            # Minerals
            "FE": "iron",
            "MG": "magnesium",
            "CA": "calcium",
            "K": "potassium",
            "NA": "sodium",
            "ZN": "zinc",
            "P": "phosphorus",
            "CU": "copper",
            "MN": "manganese",
            "SE": "selenium",
            
            # Vitamins
            "VITC": "vitamin_c",
            "VITD": "vitamin_d",
            "VITB6A": "vitamin_b6",
            "VITB12": "vitamin_b12",
            "FOLDFE": "folate",  # Folate (B9)
            "THIA": "thiamin",   # B1
            "RIBF": "riboflavin", # B2
            "NIA": "niacin",     # B3
            "VITK1": "vitamin_k",
            "VITE": "vitamin_e",
            "VITA_RAE": "vitamin_a",
            
            # Omega-3 fatty acids
            "EPA": "epa",
            "DHA": "dha",
            "OMEGA3": "omega3_g"
        }
        
        for edamam_code, canonical_name in nutrient_map.items():
            if edamam_code in total_nutrients:
                quantity = total_nutrients[edamam_code].get("quantity", 0)
                nutrients_raw[canonical_name] = quantity / servings
                print(f"DEBUG: Found {canonical_name}: {quantity / servings:.2f} (from {edamam_code})")
        
        # Calculate EPA+DHA if available (convert mg to g)
        epa = total_nutrients.get("EPA", {}).get("quantity", 0) / servings
        dha = total_nutrients.get("DHA", {}).get("quantity", 0) / servings
        if epa > 0 or dha > 0:
            nutrients_raw["omega3_g"] = (epa + dha) / 1000.0  # Convert mg to g
        
        # Also check for direct omega-3 value
        if "OMEGA3" in total_nutrients:
            omega3_mg = total_nutrients["OMEGA3"].get("quantity", 0) / servings
            if omega3_mg > 0:
                nutrients_raw["omega3_g"] = omega3_mg / 1000.0  # Convert mg to g
        
        print(f"DEBUG: Final extracted nutrients: {nutrients_raw}")
        return nutrients_raw
    
    def build_search_query_from_mood(
        self,
        keywords: List[str],
        user_profile: UserProfile,
        nutrition_targets: NutritionTargets
    ) -> Dict[str, Any]:
        """
        Build Edamam search parameters from mood keywords and user profile
        """
        # Filter keywords based on dietary preferences and allergies
        meat_keywords = ["beef", "pork", "chicken", "turkey", "lamb", "veal", "duck", 
                        "meat", "bacon", "sausage", "ham", "lean meat", "lean beef"]
        seafood_keywords = ["fish", "salmon", "tuna", "shrimp", "seafood", "shellfish"]
        
        filtered_keywords = []
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # Skip meat for vegetarians/vegans
            if user_profile.dietary_preference in ["vegetarian", "vegan"]:
                if any(meat in keyword_lower for meat in meat_keywords):
                    continue
            
            # Skip seafood for vegans
            if user_profile.dietary_preference == "vegan":
                if any(seafood in keyword_lower for seafood in seafood_keywords):
                    continue
                # Skip eggs and dairy
                if any(item in keyword_lower for item in ["egg", "dairy", "milk", "cheese"]):
                    continue
            
            # Skip allergies
            skip_keyword = False
            for allergy in user_profile.food_allergies:
                if allergy.lower() in keyword_lower:
                    skip_keyword = True
                    break
            
            if not skip_keyword:
                filtered_keywords.append(keyword)
        
        # Fallback to generic vegetarian keywords if all filtered out
        if not filtered_keywords:
            if user_profile.dietary_preference in ["vegetarian", "vegan"]:
                filtered_keywords = ["vegetables", "legumes"]
            else:
                filtered_keywords = ["healthy", "nutritious"]
        
        # Combine keywords into search query
        query = " ".join(filtered_keywords[:2])  # Use top 2 keywords
        
        # Map user-friendly cuisine names to Edamam cuisine type filters
        cuisine_map = {
            "Mediterranean": ["Mediterranean"],
            "Asian": ["Asian", "Chinese", "Japanese", "South East Asian"],
            "Mexican": ["Mexican"],
            "Italian": ["Italian"],
            "American": ["American"],
            "Other Western": ["British", "French", "Nordic", "Central Europe", "Eastern Europe"],
            "Surprise Me": None  # No filter = all cuisines
        }
        
        # Get cuisine types from user preferences
        cuisine_types = None
        if user_profile.cuisine_preferences:
            user_cuisine = user_profile.cuisine_preferences[0]  # Take first preference
            cuisine_types = cuisine_map.get(user_cuisine, None)
        
        # Map dietary preferences to Edamam diet labels
        diet_label_map = {
            "vegetarian": "vegetarian",
            "vegan": "vegan",
            "pescatarian": "pescatarian",
            "paleo": "paleo-gluten-free",
            "keto": "low-carb"
        }
        
        diet_labels = []
        if user_profile.dietary_preference in diet_label_map:
            diet_labels.append(diet_label_map[user_profile.dietary_preference])
        
        # Map allergies to health labels
        health_labels = []
        allergy_map = {
            "peanuts": "peanut-free",
            "tree nuts": "tree-nut-free",
            "dairy": "dairy-free",
            "gluten": "gluten-free",
            "soy": "soy-free",
            "eggs": "egg-free",
            "fish": "fish-free",
            "shellfish": "shellfish-free"
        }
        
        for allergy in user_profile.food_allergies:
            allergy_lower = allergy.lower()
            for key, label in allergy_map.items():
                if key in allergy_lower:
                    health_labels.append(label)
                    break
        
        # Calculate calorie range (more flexible for better recipe matching)
        cal_min = int(nutrition_targets.calories * 0.15)  # About 15% for light meal
        cal_max = int(nutrition_targets.calories * 0.50)  # About 50% for hearty meal
        calories_range = f"{cal_min}-{cal_max}"
        
        # Protein range (more flexible for better recipe matching)
        protein_min = int(nutrition_targets.protein_g * 0.10)  # Minimum 10% of daily protein
        protein_max = int(nutrition_targets.protein_g * 0.60)  # Up to 60% of daily protein
        protein_range = f"{protein_min}-{protein_max}"
        
        return {
            "query": query,
            "cuisine_types": cuisine_types,
            "diet_labels": diet_labels if diet_labels else None,
            "health_labels": health_labels if health_labels else None,
            "excluded_ingredients": user_profile.food_allergies if user_profile.food_allergies else None,
            "calories_range": calories_range,
            "protein_range": protein_range,
            "max_results": 5
        }


# Singleton instance
edamam_client = EdamamClient()

