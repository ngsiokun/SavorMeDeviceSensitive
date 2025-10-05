"""Service layer for external API integrations"""

from .edamam_client import EdamamClient
from .fusion_engine import FusionEngine
from .mood_nutrition_engine import MoodNutritionEngine
from .nutrition_calculator import NutritionCalculator
from .openrouter_client import OpenRouterClient

__all__ = [
    "EdamamClient",
    "FusionEngine", 
    "MoodNutritionEngine",
    "NutritionCalculator",
    "OpenRouterClient"
]

