"""
USDA FoodData Central API Client
https://fdc.nal.usda.gov/api-guide.html

Provides nutrient data for foods and ingredients
"""
import httpx
from typing import List, Dict, Optional, Any
from app.core.config import settings


class FDCClient:
    """Client for USDA FoodData Central API"""
    
    def __init__(self):
        self.base_url = settings.USDA_BASE_URL
        self.api_key = settings.USDA_API_KEY
    
    async def search_foods(
        self,
        query: str,
        page_size: int = 5,
        data_type: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for foods by name
        
        Args:
            query: Search term (e.g., "salmon raw")
            page_size: Number of results
            data_type: Filter by data type (e.g., ["SR Legacy", "Foundation"])
        
        Returns:
            List of food summaries with fdcId
        """
        if not self.api_key:
            return []
        
        url = f"{self.base_url}/foods/search"
        params = {
            "api_key": self.api_key,
            "query": query,
            "pageSize": page_size
        }
        
        if data_type:
            params["dataType"] = ",".join(data_type)
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                return data.get("foods", [])
        except Exception as e:
            print(f"FDC search error: {e}")
            return []
    
    async def get_food_detail(self, fdc_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed nutrient information for a food
        
        Args:
            fdc_id: FoodData Central ID
        
        Returns:
            Food detail with nutrients
        """
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/food/{fdc_id}"
        params = {"api_key": self.api_key}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"FDC detail error: {e}")
            return None
    
    def extract_nutrients_per_100g(self, food_detail: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract nutrients from FDC food detail
        
        Returns nutrients per 100g in raw format (will be canonicalized later)
        """
        nutrients = {}
        
        # Try foodNutrients array (SR Legacy, Foundation foods)
        if "foodNutrients" in food_detail:
            for nutrient_data in food_detail["foodNutrients"]:
                nutrient_info = nutrient_data.get("nutrient", {})
                name = nutrient_info.get("name", "")
                amount = nutrient_data.get("amount", 0)
                
                if name and amount:
                    nutrients[name] = amount
        
        # Try labelNutrients (Branded foods - usually per serving)
        elif "labelNutrients" in food_detail:
            label_nutrients = food_detail["labelNutrients"]
            
            # Map common label nutrients
            label_map = {
                "protein": "protein",
                "fat": "total_fat",
                "carbohydrates": "carbohydrate_by_difference",
                "fiber": "fiber",
                "iron": "iron",
                "calcium": "calcium",
                "vitaminC": "vitamin_c",
                "vitaminD": "vitamin_d"
            }
            
            for label_key, nutrient_name in label_map.items():
                if label_key in label_nutrients:
                    value = label_nutrients[label_key].get("value")
                    if value:
                        nutrients[nutrient_name] = value
        
        return nutrients
    
    def to_canonical_nutrients(
        self,
        raw_nutrients: Dict[str, float],
        aliases: Dict[str, List[str]]
    ) -> Dict[str, float]:
        """
        Convert FDC nutrient names to canonical names
        
        Args:
            raw_nutrients: Nutrients from FDC with their original names
            aliases: Nutrient alias mapping from mood_mapping.json
        
        Returns:
            Canonicalized nutrients
        """
        canonical = {}
        
        for canonical_name, alias_list in aliases.items():
            value = 0.0
            
            # Check all possible aliases
            for alias in alias_list + [canonical_name]:
                # Case-insensitive partial matching
                for raw_name, raw_value in raw_nutrients.items():
                    if alias.lower() in raw_name.lower():
                        value += raw_value
                        break
            
            if value > 0:
                canonical[canonical_name] = value
        
        return canonical
    
    async def get_ingredient_nutrients(
        self,
        ingredient_name: str,
        serving_size_g: float = 100.0
    ) -> Dict[str, float]:
        """
        Get canonicalized nutrients for an ingredient
        
        Args:
            ingredient_name: Name of ingredient (e.g., "salmon")
            serving_size_g: Serving size in grams
        
        Returns:
            Canonical nutrients per serving
        """
        # Search for the ingredient
        foods = await self.search_foods(ingredient_name, page_size=1)
        
        if not foods:
            return {}
        
        # Get detailed nutrients for first result
        fdc_id = foods[0].get("fdcId")
        if not fdc_id:
            return {}
        
        detail = await self.get_food_detail(fdc_id)
        if not detail:
            return {}
        
        # Extract nutrients per 100g
        nutrients_per_100g = self.extract_nutrients_per_100g(detail)
        
        # Scale to serving size
        multiplier = serving_size_g / 100.0
        nutrients_per_serving = {
            name: value * multiplier
            for name, value in nutrients_per_100g.items()
        }
        
        return nutrients_per_serving


# Singleton instance
fdc_client = FDCClient()

