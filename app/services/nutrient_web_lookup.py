"""
Web-based nutrient lookup service for detailed ingredient analysis
Uses web search to get comprehensive nutritional data for recipe ingredients
"""
import httpx
import re
from typing import List, Dict, Any, Optional
from app.models.recipe import Ingredient, NutritionInfo
import asyncio


class NutrientWebLookup:
    """Service to lookup detailed nutrient information for ingredients via web search"""
    
    def __init__(self):
        self.session = None
    
    async def get_detailed_nutrients(self, recipe_name: str, ingredients: List[Ingredient]) -> Dict[str, float]:
        """
        Get detailed nutrient information for recipe ingredients via web search
        
        Args:
            recipe_name: Name of the recipe
            ingredients: List of ingredients with amounts
            
        Returns:
            Dictionary of nutrients with values
        """
        if not ingredients:
            return {}
        
        # Initialize session if needed
        if not self.session:
            self.session = httpx.AsyncClient(timeout=30.0)
        
        nutrients = {}
        
        # Process each ingredient
        for ingredient in ingredients:
            try:
                ingredient_nutrients = await self._lookup_ingredient_nutrients(ingredient)
                
                # Add to total nutrients
                for nutrient, value in ingredient_nutrients.items():
                    if nutrient in nutrients:
                        nutrients[nutrient] += value
                    else:
                        nutrients[nutrient] = value
                        
            except Exception as e:
                print(f"Error looking up nutrients for {ingredient.name}: {e}")
                continue
        
        return nutrients
    
    async def _lookup_ingredient_nutrients(self, ingredient: Ingredient) -> Dict[str, float]:
        """
        Lookup nutrient information for a single ingredient
        
        Args:
            ingredient: Ingredient with amount and name
            
        Returns:
            Dictionary of nutrients for this ingredient
        """
        # Parse amount to get quantity
        amount = self._parse_amount(ingredient.amount or "1")
        ingredient_name = ingredient.name.lower()
        
        # Create search query
        search_query = f"{ingredient_name} nutrition facts per 100g micronutrients vitamins minerals"
        
        try:
            # Use a simple web search approach
            # In a real implementation, you might use a nutrition API like USDA
            nutrients = await self._search_nutrient_data(search_query, amount)
            return nutrients
            
        except Exception as e:
            print(f"Error in web search for {ingredient_name}: {e}")
            return {}
    
    def _parse_amount(self, amount_str: str) -> float:
        """
        Parse ingredient amount to get numeric value
        
        Args:
            amount_str: String like "2 cups", "1/2 tsp", "250g"
            
        Returns:
            Numeric amount
        """
        if not amount_str:
            return 1.0
        
        # Remove common units and extract numbers
        amount_str = amount_str.lower().strip()
        
        # Handle fractions
        if '/' in amount_str:
            parts = amount_str.split()
            for part in parts:
                if '/' in part:
                    try:
                        num, den = part.split('/')
                        return float(num) / float(den)
                    except:
                        continue
        
        # Extract numbers
        numbers = re.findall(r'\d+\.?\d*', amount_str)
        if numbers:
            return float(numbers[0])
        
        return 1.0
    
    async def _search_nutrient_data(self, query: str, amount: float) -> Dict[str, float]:
        """
        Search for nutrient data using web search
        
        Args:
            query: Search query
            amount: Amount multiplier
            
        Returns:
            Dictionary of nutrients
        """
        # For now, use a simplified approach with known nutrient databases
        # In a real implementation, you would use a proper nutrition API
        
        # Common nutrient values per 100g for typical ingredients
        nutrient_database = {
            # Leafy greens
            'spinach': {
                'magnesium_mg': 79,
                'iron_mg': 2.7,
                'folate_mcg': 194,
                'vitamin_c_mg': 28,
                'vitamin_k_mcg': 483,
                'calcium_mg': 99
            },
            'kale': {
                'magnesium_mg': 47,
                'iron_mg': 1.5,
                'folate_mcg': 62,
                'vitamin_c_mg': 120,
                'vitamin_k_mcg': 817,
                'calcium_mg': 150
            },
            'lettuce': {
                'magnesium_mg': 13,
                'iron_mg': 0.9,
                'folate_mcg': 38,
                'vitamin_c_mg': 9,
                'vitamin_k_mcg': 126,
                'calcium_mg': 36
            },
            
            # Fish and seafood
            'salmon': {
                'omega3_g': 2.3,
                'vitamin_d_iu': 988,
                'vitamin_b12_mcg': 3.2,
                'selenium_mcg': 36.5,
                'protein_g': 25.4
            },
            'tuna': {
                'omega3_g': 0.3,
                'vitamin_d_iu': 82,
                'vitamin_b12_mcg': 2.5,
                'selenium_mcg': 108.2,
                'protein_g': 30.0
            },
            'mackerel': {
                'omega3_g': 2.5,
                'vitamin_d_iu': 643,
                'vitamin_b12_mcg': 8.7,
                'selenium_mcg': 51.6,
                'protein_g': 19.0
            },
            'sardines': {
                'omega3_g': 1.5,
                'vitamin_d_iu': 272,
                'vitamin_b12_mcg': 8.9,
                'calcium_mg': 382,
                'protein_g': 25.0
            },
            
            # Legumes
            'lentils': {
                'folate_mcg': 479,
                'iron_mg': 6.5,
                'magnesium_mg': 47,
                'zinc_mg': 3.3,
                'protein_g': 25.0,
                'fiber_g': 10.7
            },
            'chickpeas': {
                'folate_mcg': 557,
                'iron_mg': 4.3,
                'magnesium_mg': 48,
                'zinc_mg': 2.8,
                'protein_g': 19.0,
                'fiber_g': 17.0
            },
            'beans': {
                'folate_mcg': 394,
                'iron_mg': 5.1,
                'magnesium_mg': 120,
                'zinc_mg': 2.8,
                'protein_g': 21.0,
                'fiber_g': 15.0
            },
            
            # Nuts and seeds
            'almonds': {
                'magnesium_mg': 270,
                'vitamin_e_mg': 25.6,
                'zinc_mg': 3.1,
                'calcium_mg': 264,
                'protein_g': 21.0
            },
            'walnuts': {
                'omega3_g': 9.1,
                'magnesium_mg': 158,
                'zinc_mg': 2.9,
                'folate_mcg': 98,
                'protein_g': 15.0
            },
            'chia': {
                'omega3_g': 17.8,
                'magnesium_mg': 335,
                'calcium_mg': 631,
                'iron_mg': 7.7,
                'fiber_g': 34.4
            },
            
            # Whole grains
            'quinoa': {
                'magnesium_mg': 197,
                'iron_mg': 4.6,
                'folate_mcg': 184,
                'zinc_mg': 3.1,
                'protein_g': 14.0,
                'fiber_g': 7.0
            },
            'oats': {
                'magnesium_mg': 177,
                'iron_mg': 4.7,
                'zinc_mg': 3.6,
                'folate_mcg': 56,
                'protein_g': 17.0,
                'fiber_g': 10.6
            },
            'brown rice': {
                'magnesium_mg': 43,
                'iron_mg': 0.8,
                'zinc_mg': 1.2,
                'folate_mcg': 20,
                'protein_g': 7.9,
                'fiber_g': 3.5
            },
            
            # Meat
            'chicken': {
                'protein_g': 27.0,
                'iron_mg': 1.0,
                'zinc_mg': 1.5,
                'vitamin_b12_mcg': 0.3,
                'selenium_mcg': 22.0
            },
            'lamb': {
                'protein_g': 25.0,
                'iron_mg': 2.3,
                'zinc_mg': 4.4,
                'vitamin_b12_mcg': 2.3,
                'selenium_mcg': 7.0
            },
            'beef': {
                'protein_g': 26.0,
                'iron_mg': 2.6,
                'zinc_mg': 6.3,
                'vitamin_b12_mcg': 2.4,
                'selenium_mcg': 19.0
            }
        }
        
        # Find matching ingredient
        query_lower = query.lower()
        nutrients = {}
        
        for ingredient_key, nutrient_data in nutrient_database.items():
            if ingredient_key in query_lower:
                # Scale by amount (assuming 100g base)
                for nutrient, value in nutrient_data.items():
                    nutrients[nutrient] = value * (amount / 100.0)
                break
        
        return nutrients
    
    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.aclose()


# Singleton instance
nutrient_web_lookup = NutrientWebLookup()
