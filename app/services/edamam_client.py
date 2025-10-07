"""
Edamam Recipe Search API Client
https://developer.edamam.com/edamam-recipe-api
"""
import httpx
from typing import List, Optional, Dict, Any
from app.core.config import settings
from app.models.recipe import Recipe, Ingredient, NutritionInfo
from app.models.user import UserProfile, NutritionTargets
from app.services.nutrient_web_lookup import nutrient_web_lookup
from app.data.edamam_constants import (
    PRIMARY_NUTRIENTS, SECONDARY_NUTRIENTS, ALL_NUTRIENTS,
    ENERC_KCAL, PROCNT, CHOCDF, FAT, FIBTG, FIBER, NA,
    FE, MG, VITB12, FOLDFE, VITD, ZN, VITC, CA, K, P,
    HIGH_FIBER_INGREDIENTS, is_high_fiber_ingredient,
    convert_vitamin_d_to_iu, get_nutrient_code
)
from app.services.web_image_search import web_image_search


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
            params.append((f"nutrients[{PROCNT}]", protein_range))
        
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
            recipe = await self._parse_recipe_with_image_fallback(recipe_data)
            
            # Enhance nutrition data with web lookup
            print(f"DEBUG: Recipe '{recipe.name}' has {len(recipe.ingredients) if recipe.ingredients else 0} ingredients")
            if recipe.ingredients:
                print(f"DEBUG: Ingredients: {[ing.name for ing in recipe.ingredients[:3]]}...")  # Show first 3 ingredients
                try:
                    web_nutrients = await nutrient_web_lookup.get_detailed_nutrients(
                        recipe.name, recipe.ingredients
                    )
                    
                    # Merge web nutrients with existing nutrition data
                    if web_nutrients:
                        recipe.nutrition = self._merge_nutrition_data(recipe.nutrition, web_nutrients)
                        print(f"Enhanced {recipe.name} with web nutrients: {list(web_nutrients.keys())}")
                        print(f"Web nutrient values: {web_nutrients}")
                    else:
                        print(f"No web nutrients found for {recipe.name}")
                        
                except Exception as e:
                    print(f"Error enhancing nutrients for {recipe.name}: {e}")
            
            recipes.append(recipe)
        
        print(f"Initial search for '{query}' found {len(recipes)} recipes")
        
        # If no results found, try a more flexible search
        if not recipes:
            print(f"No results found for '{query}', trying flexible search...")
            print(f"Original params - calories: {calories_range}, protein: {protein_range}, cuisine: {cuisine_types}")
            
            # Try with just the first keyword if query has multiple words
            simple_query = query.split()[0] if query.split() else query
            print(f"Trying simple query: '{simple_query}'")
            
            # Create a more flexible search with only basic parameters
            flexible_params = [
                ("type", "public"),
                ("q", simple_query),
                ("app_id", self.app_id),
                ("app_key", self.app_key),
            ]
            
            # Add only the most important fields
            for field in ["uri", "label", "image", "ingredients", "calories", "totalNutrients"]:
                flexible_params.append(("field", field))
            
            try:
                response = await client.get(self.base_url, params=flexible_params)
                response.raise_for_status()
                data = response.json()
                
                # Parse flexible results
                for hit in data.get("hits", [])[:max_results]:
                    recipe_data = hit.get("recipe", {})
                    recipe = await self._parse_recipe_with_image_fallback(recipe_data)
                    recipes.append(recipe)
                    
                print(f"Flexible search found {len(recipes)} recipes")
                
                # If still no results, try with generic healthy keywords
                if not recipes:
                    print("Trying generic healthy keywords...")
                    generic_queries = ["healthy", "nutritious", "balanced", "protein", "vegetables"]
                    
                    for generic_query in generic_queries:
                        if recipes:
                            break
                            
                        generic_params = [
                            ("type", "public"),
                            ("q", generic_query),
                            ("app_id", self.app_id),
                            ("app_key", self.app_key),
                        ]
                        
                        for field in ["uri", "label", "image", "ingredients", "calories", "totalNutrients"]:
                            generic_params.append(("field", field))
                        
                        try:
                            response = await client.get(self.base_url, params=generic_params)
                            response.raise_for_status()
                            data = response.json()
                            
                            for hit in data.get("hits", [])[:max_results]:
                                recipe_data = hit.get("recipe", {})
                                recipe = await self._parse_recipe_with_image_fallback(recipe_data)
                                recipes.append(recipe)
                                
                            print(f"Generic search '{generic_query}' found {len(recipes)} recipes")
                        except Exception as e:
                            print(f"Generic search '{generic_query}' failed: {e}")
                            continue
                            
            except Exception as e:
                print(f"Flexible search failed: {e}")
        
        return recipes
    
    def _parse_recipe(self, recipe_data: Dict[str, Any]) -> Recipe:
        """Parse Edamam recipe response into Recipe model"""
        
        recipe_name = recipe_data.get("label", "Unknown Recipe")
        print(f"DEBUG: Processing recipe '{recipe_name}'")
        
        # Choose best image with intelligent selection and validation
        image_url = self._choose_recipe_image(recipe_data, recipe_name)
        
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
        
        # Calculate per-serving values using constants
        fiber_from_api = nutrients.get(FIBTG, {}).get("quantity", 0) / servings or nutrients.get(FIBER, {}).get("quantity", 0) / servings
        
        # If fiber is 0, try to get it from nutrient lookup for high-fiber ingredients
        if fiber_from_api == 0:
            fiber_from_lookup = 0
            for ingredient in ingredients:
                if is_high_fiber_ingredient(ingredient.name):
                    # Use nutrient lookup to get fiber for high-fiber ingredients
                    try:
                        # Note: nutrient_web_lookup is async, but we can't await here in sync method
                        # This is a fallback - the main nutrition enhancement happens in async methods
                        pass
                    except:
                        pass
            
            fiber_from_api = fiber_from_lookup
        
        nutrition = NutritionInfo(
            calories=nutrients.get(ENERC_KCAL, {}).get("quantity", 0) / servings,
            protein_g=nutrients.get(PROCNT, {}).get("quantity", 0) / servings,
            fiber_g=fiber_from_api,
            carbs_g=nutrients.get(CHOCDF, {}).get("quantity", 0) / servings,
            fat_g=nutrients.get(FAT, {}).get("quantity", 0) / servings,
            sodium_mg=nutrients.get(NA, {}).get("quantity", 0) / servings
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
    
    async def _parse_recipe_with_image_fallback(self, recipe_data: Dict[str, Any]) -> Recipe:
        """
        Parse Edamam recipe response into Recipe model with image fallback
        
        Args:
            recipe_data: Raw recipe data from Edamam API
            
        Returns:
            Recipe object with enhanced image handling
        """
        # First, parse the recipe normally
        recipe = self._parse_recipe(recipe_data)
        
        # Only try fallback if no image was found AND the original was filtered out
        if not recipe.image_url:
            # Check if the original image was filtered out (not just missing)
            original_image_url = recipe_data.get("image")
            if original_image_url:
                recipe_name = recipe.name
                ingredients = recipe.ingredients
                
                print(f"DEBUG: Original image was filtered out for {recipe_name}, trying web search...")
                fallback_image = await self._get_fallback_image_url(recipe_name, ingredients)
                if fallback_image:
                    # Update the recipe with the fallback image
                    recipe = Recipe(
                        recipe_id=recipe.recipe_id,
                        name=recipe.name,
                        image_url=fallback_image,
                        ingredients=recipe.ingredients,
                        cooking_directions=recipe.cooking_directions,
                        prep_time=recipe.prep_time,
                        cook_time=recipe.cook_time,
                        servings=recipe.servings,
                        nutrition=recipe.nutrition,
                        source_url=recipe.source_url,
                        source_name=recipe.source_name,
                        cuisine_type=recipe.cuisine_type,
                        meal_type=recipe.meal_type,
                        dish_type=recipe.dish_type
                    )
                    print(f"DEBUG: Updated {recipe_name} with fallback image")
                else:
                    print(f"DEBUG: No fallback image found for {recipe_name}")
            else:
                print(f"DEBUG: No original image from Edamam for {recipe.name}")
        
        return recipe
    
    def _enhance_recipe_nutrition(self, recipe: Recipe, canonical_nutrients: Dict[str, float]) -> Recipe:
        """
        Enhance recipe nutrition data with secondary nutrients from canonical nutrients
        
        Args:
            recipe: Recipe object with basic nutrition
            canonical_nutrients: Dictionary of canonical nutrient names to values
            
        Returns:
            Enhanced recipe with secondary nutrients
        """
        # Create enhanced nutrition info with secondary nutrients
        enhanced_nutrition = NutritionInfo(
            calories=recipe.nutrition.calories,
            protein_g=recipe.nutrition.protein_g,
            fiber_g=recipe.nutrition.fiber_g,
            carbs_g=recipe.nutrition.carbs_g,
            fat_g=recipe.nutrition.fat_g,
            sodium_mg=recipe.nutrition.sodium_mg,
            
            # Secondary nutrients from canonical data
            iron_mg=canonical_nutrients.get("iron", 0),
            magnesium_mg=canonical_nutrients.get("magnesium", 0),
            vitamin_b12_mcg=canonical_nutrients.get("vitamin_b12", 0),
            folate_mcg=canonical_nutrients.get("folate", 0),
            vitamin_d_iu=convert_vitamin_d_to_iu(canonical_nutrients.get("vitamin_d", 0)),
            omega3_g=canonical_nutrients.get("omega_3_epa_dha", 0),
            zinc_mg=canonical_nutrients.get("zinc", 0),
            vitamin_c_mg=canonical_nutrients.get("vitamin_c", 0)
        )
        
        # Create new recipe with enhanced nutrition
        enhanced_recipe = Recipe(
            recipe_id=recipe.recipe_id,
            name=recipe.name,
            image_url=recipe.image_url,
            ingredients=recipe.ingredients,
            cooking_directions=recipe.cooking_directions,
            prep_time=recipe.prep_time,
            cook_time=recipe.cook_time,
            servings=recipe.servings,
            nutrition=enhanced_nutrition,
            source_url=recipe.source_url,
            source_name=recipe.source_name,
            cuisine_type=recipe.cuisine_type,
            meal_type=recipe.meal_type,
            dish_type=recipe.dish_type
        )
        
        print(f"DEBUG: Enhanced {recipe.name} nutrition with secondary nutrients:")
        print(f"  Iron: {enhanced_nutrition.iron_mg}mg")
        print(f"  Magnesium: {enhanced_nutrition.magnesium_mg}mg")
        print(f"  Vitamin B12: {enhanced_nutrition.vitamin_b12_mcg}mcg")
        print(f"  Folate: {enhanced_nutrition.folate_mcg}mcg")
        print(f"  Vitamin D: {enhanced_nutrition.vitamin_d_iu}IU")
        print(f"  Omega-3: {enhanced_nutrition.omega3_g}g")
        print(f"  Zinc: {enhanced_nutrition.zinc_mg}mg")
        print(f"  Vitamin C: {enhanced_nutrition.vitamin_c_mg}mg")
        
        return enhanced_recipe
    
    def _pick_best_edamam_image(self, images_dict: dict) -> str:
        """
        Select the best image variant from Edamam's images object
        Prefers larger images with aspect ratio close to 16:9
        
        Args:
            images_dict: Edamam's images object with THUMB/SMALL/REGULAR/LARGE variants
            
        Returns:
            Best image URL or None
        """
        if not images_dict:
            return None
            
        from math import inf
        
        PREFERRED_AR = 16 / 9  # Target aspect ratio for hero images
        best_url, best_score = None, -inf
        
        for variant_name, meta in images_dict.items():
            w = meta.get("width")
            h = meta.get("height")
            url = meta.get("url")
            
            if not w or not h or not url:
                continue
                
            # Score based on area and aspect ratio proximity
            area = w * h
            ar_penalty = abs((w / h) - PREFERRED_AR)
            score = area - 200_000 * ar_penalty  # Weight AR fairly strongly
            
            if score > best_score:
                best_score = score
                best_url = url
                print(f"DEBUG: Found better image variant '{variant_name}' ({w}x{h}, AR={(w/h):.2f}, score={score:.0f})")
        
        return best_url
    
    def _is_generic_path(self, url: str) -> bool:
        """Check if URL path contains generic/decorative image indicators"""
        try:
            from urllib.parse import urlsplit
            path = urlsplit(url).path.lower()
        except Exception:
            return True
            
        generic_parts = (
            "/logo", "/icon", "/sprite", "/placeholder", "/default",
            "/avatar", "/social", "/share", "/banner", "/header",
            "/footer", "/bg", "/background", "heart"
        )
        return any(p in path for p in generic_parts)
    
    def _looks_like_valid_image(self, url: str, timeout: int = 5) -> bool:
        """
        Lightweight HEAD request to validate image
        Checks content-type and minimum file size
        
        WARNING: This is a blocking network call. Only use for final selected recipe.
        """
        try:
            import httpx
            with httpx.Client(timeout=timeout) as client:
                response = client.head(url, follow_redirects=True)
                
                # Must be image/*
                content_type = response.headers.get("Content-Type", "").lower()
                if not content_type.startswith("image/"):
                    print(f"DEBUG: Invalid content-type '{content_type}' for {url}")
                    return False
                
                # Must be larger than 5KB (avoid tiny placeholders)
                content_length = response.headers.get("Content-Length")
                if content_length and content_length.isdigit():
                    size_bytes = int(content_length)
                    if size_bytes < 5_000:
                        print(f"DEBUG: Image too small ({size_bytes} bytes) for {url}")
                        return False
                
                return True
        except Exception as e:
            print(f"DEBUG: HEAD request failed for {url}: {e}")
            return False
    
    def validate_final_recipe_image(self, recipe: Recipe) -> Recipe:
        """
        Validate the image of the final selected recipe (only called once per recommendation)
        
        Args:
            recipe: The selected recipe to validate
            
        Returns:
            Recipe with validated image (or None if invalid)
        """
        if not recipe.image_url:
            return recipe
        
        print(f"DEBUG: Validating final recipe image for '{recipe.name}'")
        
        # Perform HEAD validation on the final image only
        if not self._looks_like_valid_image(recipe.image_url):
            print(f"DEBUG: Final recipe image failed validation, setting to None")
            # Create new recipe with image_url = None (frontend will use placeholder)
            recipe = Recipe(
                recipe_id=recipe.recipe_id,
                name=recipe.name,
                image_url=None,  # Clear invalid image
                ingredients=recipe.ingredients,
                cooking_directions=recipe.cooking_directions,
                prep_time=recipe.prep_time,
                cook_time=recipe.cook_time,
                servings=recipe.servings,
                nutrition=recipe.nutrition,
                source_url=recipe.source_url,
                source_name=recipe.source_name,
                cuisine_type=recipe.cuisine_type,
                meal_type=recipe.meal_type,
                dish_type=recipe.dish_type
            )
        else:
            print(f"DEBUG: Final recipe image validated successfully")
        
        return recipe
    
    def _choose_recipe_image(self, recipe_data: dict, recipe_name: str, validate: bool = False) -> str:
        """
        Choose the best image for a recipe with optional validation
        
        SIMPLIFIED: Just use the main 'image' field from Edamam (reliable and fast)
        
        Args:
            recipe_data: Raw recipe data from Edamam
            recipe_name: Recipe name for logging
            validate: If True, perform HEAD request validation (slow, only use for final recipe)
            
        Returns:
            Image URL or None
        """
        # Get the main image URL from Edamam (simple and reliable)
        image_url = recipe_data.get("image")
        
        if not image_url:
            print(f"DEBUG: No image URL in Edamam data for '{recipe_name}'")
            return None
        
        # Filter out generic/decorative images by path
        if self._is_generic_path(image_url):
            print(f"DEBUG: Image filtered as generic for '{recipe_name}'")
            return None
        
        # Optionally validate with HEAD request (only for final selected recipe)
        if validate and not self._looks_like_valid_image(image_url):
            print(f"DEBUG: Image failed HEAD validation for '{recipe_name}'")
            return None
        
        print(f"DEBUG: Using image for '{recipe_name}': {image_url[:80]}...")
        return image_url
    
    async def _get_fallback_image_url(self, recipe_name: str, ingredients: list = None) -> str:
        """
        Get a fallback food image URL when the original image is filtered out
        
        Args:
            recipe_name: Name of the recipe for context
            ingredients: List of ingredients for better search
            
        Returns:
            Fallback image URL or None
        """
        try:
            print(f"DEBUG: Starting fallback image search for '{recipe_name}'")
            
            # Try to find a food image from web sources
            image_url = await web_image_search.search_food_image(recipe_name, ingredients)
            if image_url:
                print(f"DEBUG: Found web image for recipe '{recipe_name}': {image_url}")
                return image_url
            else:
                print(f"DEBUG: No web image found for recipe '{recipe_name}'")
            
            # If no web image found, generate a simple placeholder
            placeholder_url = await web_image_search.generate_simple_food_placeholder(recipe_name)
            if placeholder_url:
                print(f"DEBUG: Generated placeholder for recipe '{recipe_name}': {placeholder_url}")
                return placeholder_url
            else:
                print(f"DEBUG: No placeholder generated for recipe '{recipe_name}'")
                
        except Exception as e:
            print(f"ERROR: Failed to get fallback image for {recipe_name}: {e}")
        
        print(f"DEBUG: No fallback image available for '{recipe_name}'")
        return None
    
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
        
        # Use constants for nutrient mapping - Complete micronutrient coverage
        nutrient_map = {
            # Macronutrients
            ENERC_KCAL: "calories",
            PROCNT: "protein",
            CHOCDF: "carbohydrate_by_difference",
            FIBTG: "fiber",
            FAT: "total_fat",
            "SUGAR": "sugars_total",
            "SUGAR.added": "added_sugars",
            
            # Minerals
            FE: "iron",
            MG: "magnesium",
            CA: "calcium",
            K: "potassium",
            NA: "sodium",
            ZN: "zinc",
            P: "phosphorus",
            "CU": "copper",
            "MN": "manganese",
            "SE": "selenium",
            
            # Vitamins
            VITC: "vitamin_c",
            VITD: "vitamin_d",
            "VITB6A": "vitamin_b6",
            VITB12: "vitamin_b12",
            FOLDFE: "folate",  # Folate (B9)
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
    
    def _merge_nutrition_data(self, existing_nutrition: NutritionInfo, web_nutrients: Dict[str, float]) -> NutritionInfo:
        """
        Merge web-based nutrient data with existing nutrition information
        
        Args:
            existing_nutrition: Existing nutrition data from Edamam
            web_nutrients: Additional nutrients from web lookup
            
        Returns:
            Enhanced nutrition info
        """
        # Create a copy of existing nutrition
        enhanced_nutrition = NutritionInfo(
            calories=existing_nutrition.calories,
            protein_g=existing_nutrition.protein_g,
            carbohydrate_g=existing_nutrition.carbohydrate_g,
            fat_g=existing_nutrition.fat_g,
            fiber_g=existing_nutrition.fiber_g,
            sugar_g=existing_nutrition.sugar_g,
            sodium_mg=existing_nutrition.sodium_mg,
            cholesterol_mg=existing_nutrition.cholesterol_mg,
            saturated_fat_g=existing_nutrition.saturated_fat_g,
            trans_fat_g=existing_nutrition.trans_fat_g,
            monounsaturated_fat_g=existing_nutrition.monounsaturated_fat_g,
            polyunsaturated_fat_g=existing_nutrition.polyunsaturated_fat_g,
            omega3_g=existing_nutrition.omega3_g,
            omega6_g=existing_nutrition.omega6_g,
            calcium_mg=existing_nutrition.calcium_mg,
            iron_mg=existing_nutrition.iron_mg,
            magnesium_mg=existing_nutrition.magnesium_mg,
            phosphorus_mg=existing_nutrition.phosphorus_mg,
            potassium_mg=existing_nutrition.potassium_mg,
            zinc_mg=existing_nutrition.zinc_mg,
            copper_mg=existing_nutrition.copper_mg,
            manganese_mg=existing_nutrition.manganese_mg,
            selenium_mcg=existing_nutrition.selenium_mcg,
            vitamin_a_iu=existing_nutrition.vitamin_a_iu,
            vitamin_c_mg=existing_nutrition.vitamin_c_mg,
            vitamin_d_iu=existing_nutrition.vitamin_d_iu,
            vitamin_e_mg=existing_nutrition.vitamin_e_mg,
            vitamin_k_mcg=existing_nutrition.vitamin_k_mcg,
            thiamin_mg=existing_nutrition.thiamin_mg,
            riboflavin_mg=existing_nutrition.riboflavin_mg,
            niacin_mg=existing_nutrition.niacin_mg,
            vitamin_b6_mg=existing_nutrition.vitamin_b6_mg,
            folate_mcg=existing_nutrition.folate_mcg,
            vitamin_b12_mcg=existing_nutrition.vitamin_b12_mcg,
            pantothenic_acid_mg=existing_nutrition.pantothenic_acid_mg,
            biotin_mcg=existing_nutrition.biotin_mcg,
            choline_mg=existing_nutrition.choline_mg
        )
        
        # Add web nutrients (prefer web data if available)
        for nutrient, value in web_nutrients.items():
            if hasattr(enhanced_nutrition, nutrient):
                setattr(enhanced_nutrition, nutrient, value)
        
        return enhanced_nutrition
    
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

