"""
Recipe rotation service to ensure variety and avoid repeats
Tracks recent recipes and provides rotation logic
"""
from typing import List, Dict, Set, Optional
from app.models.recipe import Recipe
import random
from datetime import datetime, timedelta


class RecipeRotationService:
    """Service to manage recipe variety and avoid repeats"""
    
    def __init__(self):
        # In-memory storage for demo (in production, use Redis or database)
        self.recent_recipes: Dict[str, List[str]] = {}  # session_id -> list of recipe names
        self.recent_times: Dict[str, List[datetime]] = {}  # session_id -> list of timestamps
        self.max_recent_recipes = 10  # Keep track of last 10 recipes per session
        self.rotation_window_hours = 24  # Don't repeat within 24 hours
    
    def get_session_id(self, user_profile: Dict) -> str:
        """
        Generate a session ID based on user profile
        In a real app, this would be a proper session ID
        """
        # Use a combination of user preferences to create a session-like ID
        preferences = [
            user_profile.get('dietary_preferences', []),
            user_profile.get('allergies', []),
            user_profile.get('cuisine_preference', ''),
        ]
        return str(hash(str(preferences)))
    
    def filter_recent_recipes(self, recipes: List[Recipe], session_id: str) -> List[Recipe]:
        """
        Filter out recently recommended recipes to ensure variety
        
        Args:
            recipes: List of candidate recipes
            session_id: Session identifier
            
        Returns:
            Filtered list of recipes with recent ones removed
        """
        if not recipes:
            return recipes
        
        # Get recent recipe names for this session
        recent_names = self.recent_recipes.get(session_id, [])
        recent_times = self.recent_times.get(session_id, [])
        
        # Remove recipes that are too recent
        now = datetime.now()
        filtered_recipes = []
        
        for recipe in recipes:
            recipe_name = recipe.name.lower().strip()
            
            # Check if this recipe was recently recommended
            is_recent = False
            for i, recent_name in enumerate(recent_names):
                if recent_name.lower().strip() == recipe_name:
                    # Check if it's within the rotation window
                    if i < len(recent_times):
                        time_diff = now - recent_times[i]
                        if time_diff < timedelta(hours=self.rotation_window_hours):
                            is_recent = True
                            break
            
            if not is_recent:
                filtered_recipes.append(recipe)
        
        # If we filtered out too many, add some back (but prefer variety)
        if len(filtered_recipes) < 2 and len(recipes) > 2:
            # Add back some recipes, but prioritize those that haven't been used recently
            remaining_recipes = [r for r in recipes if r not in filtered_recipes]
            # Sort by how long ago they were used (oldest first)
            remaining_with_times = []
            for recipe in remaining_recipes:
                recipe_name = recipe.name.lower().strip()
                last_used = None
                for i, recent_name in enumerate(recent_names):
                    if recent_name.lower().strip() == recipe_name and i < len(recent_times):
                        last_used = recent_times[i]
                        break
                
                if last_used:
                    time_since_used = now - last_used
                    remaining_with_times.append((recipe, time_since_used))
                else:
                    remaining_with_times.append((recipe, timedelta(days=365)))  # Very old
            
            # Sort by time since last used (oldest first)
            remaining_with_times.sort(key=lambda x: x[1], reverse=True)
            
            # Add back up to 2 recipes
            for recipe, _ in remaining_with_times[:2]:
                filtered_recipes.append(recipe)
        
        return filtered_recipes
    
    def record_recipe_used(self, recipe: Recipe, session_id: str):
        """
        Record that a recipe was recommended to avoid future repeats
        
        Args:
            recipe: The recipe that was recommended
            session_id: Session identifier
        """
        recipe_name = recipe.name
        
        # Initialize session tracking if needed
        if session_id not in self.recent_recipes:
            self.recent_recipes[session_id] = []
            self.recent_times[session_id] = []
        
        # Add to recent recipes
        self.recent_recipes[session_id].append(recipe_name)
        self.recent_times[session_id].append(datetime.now())
        
        # Keep only the most recent recipes
        if len(self.recent_recipes[session_id]) > self.max_recent_recipes:
            self.recent_recipes[session_id] = self.recent_recipes[session_id][-self.max_recent_recipes:]
            self.recent_times[session_id] = self.recent_times[session_id][-self.max_recent_recipes:]
    
    def get_variety_boost(self, recipes: List[Recipe], session_id: str) -> List[Recipe]:
        """
        Apply variety boosting to recipe selection
        
        Args:
            recipes: List of recipes to boost variety for
            session_id: Session identifier
            
        Returns:
            Recipes with variety boosting applied
        """
        if len(recipes) <= 1:
            return recipes
        
        # Get recent recipe names to avoid
        recent_names = set(name.lower().strip() for name in self.recent_recipes.get(session_id, []))
        
        # Separate recipes into categories for variety
        protein_sources = {}
        cuisine_types = {}
        cooking_methods = {}
        
        for recipe in recipes:
            # Categorize by protein source
            protein_key = self._extract_protein_source(recipe)
            if protein_key not in protein_sources:
                protein_sources[protein_key] = []
            protein_sources[protein_key].append(recipe)
            
            # Categorize by cuisine type
            cuisine_key = self._extract_cuisine_type(recipe)
            if cuisine_key not in cuisine_types:
                cuisine_types[cuisine_key] = []
            cuisine_types[cuisine_key].append(recipe)
            
            # Categorize by cooking method
            method_key = self._extract_cooking_method(recipe)
            if method_key not in cooking_methods:
                cooking_methods[method_key] = []
            cooking_methods[method_key].append(recipe)
        
        # Prioritize recipes that provide variety
        variety_scores = {}
        for recipe in recipes:
            score = 0
            
            # Boost score for different protein sources
            protein_key = self._extract_protein_source(recipe)
            if len(protein_sources[protein_key]) < len(recipes) / 2:
                score += 2
            
            # Boost score for different cuisines
            cuisine_key = self._extract_cuisine_type(recipe)
            if len(cuisine_types[cuisine_key]) < len(recipes) / 2:
                score += 2
            
            # Boost score for different cooking methods
            method_key = self._extract_cooking_method(recipe)
            if len(cooking_methods[method_key]) < len(recipes) / 2:
                score += 1
            
            # Penalize recently used recipes
            if recipe.name.lower().strip() in recent_names:
                score -= 3
            
            variety_scores[recipe] = score
        
        # Sort by variety score (highest first)
        sorted_recipes = sorted(recipes, key=lambda r: variety_scores[r], reverse=True)
        
        return sorted_recipes
    
    def _extract_protein_source(self, recipe: Recipe) -> str:
        """Extract primary protein source from recipe"""
        if not recipe.ingredients:
            return "unknown"
        
        ingredients_text = " ".join([ing.name.lower() for ing in recipe.ingredients])
        
        if any(meat in ingredients_text for meat in ["chicken", "turkey", "duck"]):
            return "poultry"
        elif any(meat in ingredients_text for meat in ["beef", "lamb", "pork", "veal"]):
            return "red_meat"
        elif any(fish in ingredients_text for fish in ["salmon", "tuna", "mackerel", "cod", "halibut", "trout"]):
            return "fish"
        elif any(seafood in ingredients_text for seafood in ["shrimp", "crab", "lobster", "scallops"]):
            return "seafood"
        elif any(legume in ingredients_text for legume in ["beans", "lentils", "chickpeas", "peas"]):
            return "legumes"
        elif any(soy in ingredients_text for soy in ["tofu", "tempeh", "edamame"]):
            return "soy"
        elif "egg" in ingredients_text:
            return "eggs"
        elif any(nut in ingredients_text for nut in ["almonds", "walnuts", "cashews", "nuts"]):
            return "nuts"
        else:
            return "vegetarian"
    
    def _extract_cuisine_type(self, recipe: Recipe) -> str:
        """Extract cuisine type from recipe"""
        if not recipe.cuisine_type:
            return "general"
        
        cuisine = recipe.cuisine_type[0].lower() if recipe.cuisine_type else "general"
        
        # Group similar cuisines
        if cuisine in ["italian", "mediterranean", "greek"]:
            return "mediterranean"
        elif cuisine in ["chinese", "japanese", "korean", "thai", "vietnamese"]:
            return "asian"
        elif cuisine in ["mexican", "spanish", "latin"]:
            return "latin"
        elif cuisine in ["indian", "middle eastern"]:
            return "spiced"
        else:
            return cuisine
    
    def _extract_cooking_method(self, recipe: Recipe) -> str:
        """Extract cooking method from recipe"""
        if not recipe.cooking_directions:
            return "unknown"
        
        directions_text = " ".join(recipe.cooking_directions).lower()
        
        if any(method in directions_text for method in ["grill", "grilled", "barbecue"]):
            return "grilled"
        elif any(method in directions_text for method in ["roast", "roasted", "bake", "baked"]):
            return "roasted"
        elif any(method in directions_text for method in ["sauté", "sautéed", "pan-fry", "stir-fry"]):
            return "sautéed"
        elif any(method in directions_text for method in ["boil", "boiled", "simmer", "simmered"]):
            return "boiled"
        elif any(method in directions_text for method in ["steam", "steamed"]):
            return "steamed"
        elif any(method in directions_text for method in ["raw", "fresh", "no cook"]):
            return "raw"
        else:
            return "mixed"


# Singleton instance
recipe_rotation_service = RecipeRotationService()
