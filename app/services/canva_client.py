"""
Canva API Client for SavorMe
Generates beautiful UI designs and branded content
"""
import httpx
import base64
from typing import Dict, List, Optional, Any
from app.core.config import settings


class CanvaClient:
    """Client for Canva API integration"""
    
    def __init__(self):
        self.client_id = settings.CANVA_CLIENT_ID
        self.client_secret = settings.CANVA_CLIENT_SECRET
        self.access_token = settings.CANVA_ACCESS_TOKEN
        self.base_url = "https://api.canva.com/rest/v1"
        
    async def create_recipe_card(self, recipe_data: Dict[str, Any]) -> Optional[str]:
        """
        Create a beautiful recipe card design using Canva API
        
        Args:
            recipe_data: Recipe information including name, ingredients, nutrition
            
        Returns:
            URL to the generated design or None if failed
        """
        try:
            # Template ID for recipe cards (you'll need to create this in Canva)
            template_id = "your_recipe_card_template_id"
            
            # Prepare design data
            design_data = {
                "template_id": template_id,
                "design_data": {
                    "recipe_name": recipe_data.get("name", "Delicious Recipe"),
                    "calories": recipe_data.get("nutrition", {}).get("calories", 0),
                    "protein": recipe_data.get("nutrition", {}).get("protein_g", 0),
                    "fiber": recipe_data.get("nutrition", {}).get("fiber_g", 0),
                    "ingredients": recipe_data.get("ingredients", [])[:5],  # Top 5 ingredients
                    "servings": recipe_data.get("servings", 1)
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/designs",
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": "application/json"
                    },
                    json=design_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("design_url")
                    
        except Exception as e:
            print(f"Error creating recipe card: {e}")
            
        return None
    
    async def create_mood_selection_card(self, mood_data: Dict[str, Any]) -> Optional[str]:
        """
        Create a mood selection card design
        
        Args:
            mood_data: Mood information including name, description, evidence level
            
        Returns:
            URL to the generated design
        """
        try:
            template_id = "your_mood_card_template_id"
            
            design_data = {
                "template_id": template_id,
                "design_data": {
                    "mood_name": mood_data.get("name", "Mood"),
                    "description": mood_data.get("description", ""),
                    "evidence_stars": "⭐" * mood_data.get("evidence_level", 3),
                    "nutrient_focus": mood_data.get("nutrient_focus", "")
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/designs",
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": "application/json"
                    },
                    json=design_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("design_url")
                    
        except Exception as e:
            print(f"Error creating mood card: {e}")
            
        return None
    
    async def create_nutrition_info_card(self, nutrition_data: Dict[str, Any]) -> Optional[str]:
        """
        Create a nutrition information card
        
        Args:
            nutrition_data: Nutrition information including targets and actual values
            
        Returns:
            URL to the generated design
        """
        try:
            template_id = "your_nutrition_card_template_id"
            
            design_data = {
                "template_id": template_id,
                "design_data": {
                    "calories": nutrition_data.get("calories", 0),
                    "protein": nutrition_data.get("protein_g", 0),
                    "fiber": nutrition_data.get("fiber_g", 0),
                    "target_calories": nutrition_data.get("target_calories", 0),
                    "target_protein": nutrition_data.get("target_protein", 0),
                    "target_fiber": nutrition_data.get("target_fiber", 0)
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/designs",
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": "application/json"
                    },
                    json=design_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("design_url")
                    
        except Exception as e:
            print(f"Error creating nutrition card: {e}")
            
        return None
    
    async def create_branded_header(self, title: str, subtitle: str = "") -> Optional[str]:
        """
        Create a branded header design
        
        Args:
            title: Main title text
            subtitle: Subtitle text
            
        Returns:
            URL to the generated design
        """
        try:
            template_id = "your_header_template_id"
            
            design_data = {
                "template_id": template_id,
                "design_data": {
                    "title": title,
                    "subtitle": subtitle,
                    "brand_color": "#2D5A27",  # SavorMe green
                    "accent_color": "#F4F1E8"  # Light accent
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/designs",
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": "application/json"
                    },
                    json=design_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("design_url")
                    
        except Exception as e:
            print(f"Error creating header: {e}")
            
        return None
    
    async def get_templates(self) -> List[Dict[str, Any]]:
        """
        Get available Canva templates
        
        Returns:
            List of available templates
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/templates",
                    headers={
                        "Authorization": f"Bearer {self.access_token}"
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("templates", [])
                    
        except Exception as e:
            print(f"Error getting templates: {e}")
            
        return []
    
    async def download_design(self, design_url: str) -> Optional[bytes]:
        """
        Download a design as image data
        
        Args:
            design_url: URL of the design to download
            
        Returns:
            Image data as bytes or None if failed
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    design_url,
                    headers={
                        "Authorization": f"Bearer {self.access_token}"
                    }
                )
                
                if response.status_code == 200:
                    return response.content
                    
        except Exception as e:
            print(f"Error downloading design: {e}")
            
        return None


# Global instance
canva_client = CanvaClient()
