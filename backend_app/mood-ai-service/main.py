"""
Mood & AI Service
Handles mood interpretation and AI content generation
"""
import sys
import os
from pathlib import Path
import httpx
import random
from typing import List, Dict, Any

# Add shared models to path
sys.path.append(str(Path(__file__).parent.parent / "shared"))

from fastapi import FastAPI, HTTPException
from shared.models import (
    MoodBlend,
    MoodInterpretationRequest,
    MoodInterpretationResponse,
    FlavorProfile,
    MoodType,
    IntensityLevel,
    Recipe,
    AIContentRequest,
    AIContentResponse
)

app = FastAPI(
    title="SavorMe Mood & AI Service",
    description="Handles mood interpretation and AI content generation",
    version="1.0.0"
)


class FusionEngine:
    """Converts mood combinations into recipe search parameters"""
    
    # Mood to search keywords mapping
    MOOD_SEARCH_KEYWORDS = {
        MoodType.STRESSED: [
            ["salmon", "spinach"],
            ["avocado", "quinoa"],
            ["dark chocolate", "almonds"],
            ["chickpeas", "sweet potato"],
            ["oats", "banana"],
            ["walnuts", "blueberries"],
            ["kale", "salmon"],
            ["miso", "tofu"],
            ["pumpkin seeds", "yogurt"],
            ["green tea", "matcha"]
        ],
        MoodType.FATIGUED: [
            ["lentils", "spinach"],
            ["quinoa", "beans"],
            ["eggs", "broccoli"],
            ["beef", "sweet potato"],
            ["chicken", "rice"],
            ["tofu", "vegetables"],
            ["beans", "rice"],
            ["salmon", "quinoa"],
            ["turkey", "sweet potato"],
            ["chickpeas", "spinach"]
        ],
        MoodType.LOW_MOOD: [
            ["salmon", "quinoa"],
            ["beans", "sweet potato"],
            ["oats", "berries"],
            ["walnuts", "dark chocolate"],
            ["avocado", "eggs"],
            ["lentils", "vegetables"],
            ["chickpeas", "rice"],
            ["tofu", "vegetables"],
            ["salmon", "vegetables"],
            ["quinoa", "nuts"]
        ],
        MoodType.IRRITABLE: [
            ["chicken", "rice"],
            ["tofu", "quinoa"],
            ["beans", "vegetables"],
            ["eggs", "avocado"],
            ["salmon", "sweet potato"],
            ["lentils", "rice"],
            ["turkey", "vegetables"],
            ["chickpeas", "quinoa"],
            ["beef", "vegetables"],
            ["fish", "rice"]
        ]
    }
    
    MOOD_FLAVOR_MAP = {
        MoodType.STRESSED: ["calming", "herbal", "omega-3-rich", "magnesium-rich", "gentle"],
        MoodType.FATIGUED: ["energizing", "iron-rich", "vitamin-c", "complex-carbs", "sustaining"],
        MoodType.LOW_MOOD: ["comforting", "omega-3", "fiber-rich", "wholesome", "nourishing"],
        MoodType.IRRITABLE: ["stabilizing", "protein-rich", "fiber", "low-sugar", "grounding"],
    }
    
    MOOD_TEXTURE_MAP = {
        MoodType.STRESSED: ["soft", "smooth", "gentle", "calming"],
        MoodType.FATIGUED: ["substantial", "energizing", "hearty", "sustaining"],
        MoodType.LOW_MOOD: ["comforting", "warm", "nourishing", "wholesome"],
        MoodType.IRRITABLE: ["balanced", "stable", "grounding", "satisfying"],
    }
    
    MOOD_TONE_MAP = {
        MoodType.STRESSED: ["calming", "gentle", "soothing", "peaceful"],
        MoodType.FATIGUED: ["energizing", "revitalizing", "sustaining", "strengthening"],
        MoodType.LOW_MOOD: ["nurturing", "comforting", "uplifting", "healing"],
        MoodType.IRRITABLE: ["balancing", "grounding", "stabilizing", "calming"],
    }
    
    def interpret_mood_blend(self, mood_blend: MoodBlend, cuisine_preference: str = None) -> MoodInterpretationResponse:
        """Interpret mood blend into flavor profile and search keywords"""
        # Combine flavors from all moods
        combined_flavors = []
        combined_textures = []
        combined_tones = []
        combined_keywords = []
        
        mood_descriptions = []
        
        for mood_selection in mood_blend.moods:
            mood_type = mood_selection.mood
            intensity = mood_selection.intensity
            
            # Add flavor characteristics
            flavors = self.MOOD_FLAVOR_MAP.get(mood_type, [])
            textures = self.MOOD_TEXTURE_MAP.get(mood_type, [])
            tones = self.MOOD_TONE_MAP.get(mood_type, [])
            
            combined_flavors.extend(flavors)
            combined_textures.extend(textures)
            combined_tones.extend(tones)
            
            # Get search keywords
            keywords = self.MOOD_SEARCH_KEYWORDS.get(mood_type, [["vegetables", "legumes"]])
            selected_keywords = random.choice(keywords)
            combined_keywords.extend(selected_keywords)
            
            # Create mood description
            intensity_desc = {
                IntensityLevel.A_LITTLE: "slightly",
                IntensityLevel.MEDIUM: "moderately",
                IntensityLevel.VERY: "very"
            }
            mood_descriptions.append(f"{intensity_desc.get(intensity, '')} {mood_type.value}")
        
        # Create overall description
        if len(mood_descriptions) == 1:
            overall_desc = f"You're feeling {mood_descriptions[0]}."
        elif len(mood_descriptions) == 2:
            overall_desc = f"You're feeling {mood_descriptions[0]} and {mood_descriptions[1]}."
        else:
            overall_desc = f"You're feeling {', '.join(mood_descriptions[:-1])}, and {mood_descriptions[-1]}."
        
        # Create flavor profile
        flavor_profile = FlavorProfile(
            flavor_bias=list(set(combined_flavors)),
            texture_preference=list(set(combined_textures)),
            culinary_tone=list(set(combined_tones)),
            search_keywords=list(set(combined_keywords))
        )
        
        return MoodInterpretationResponse(
            interpretation=MoodInterpretation(
                mood_description=overall_desc,
                flavor_profile=flavor_profile,
                emotional_context=f"Based on your mood, we're looking for foods that can help support your emotional well-being through evidence-based nutrition."
            )
        )


class OpenRouterClient:
    """Client for OpenRouter AI API"""
    
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = "anthropic/claude-3.5-sonnet"
    
    async def generate_emotional_rationale(self, recipe: Recipe, mood_interpretation) -> str:
        """Generate emotional rationale for recipe selection"""
        prompt = f"""
        You are a nutritional psychiatry expert. Generate a brief, warm explanation (2-3 sentences) 
        of why this recipe is perfect for someone feeling: {mood_interpretation.mood_description}
        
        Recipe: {recipe.name}
        Key nutrients: Protein: {recipe.nutrition.protein_g:.1f}g, Fiber: {recipe.nutrition.fiber_g:.1f}g
        
        Focus on the emotional and nutritional benefits. Be encouraging and scientifically grounded.
        """
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 200
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
    
    async def generate_cooking_directions(self, recipe: Recipe) -> List[str]:
        """Generate detailed cooking directions"""
        ingredients_text = "\n".join([f"- {ing.amount} {ing.unit or ''} {ing.name}" for ing in recipe.ingredients])
        
        prompt = f"""
        Generate step-by-step cooking instructions for: {recipe.name}
        
        Ingredients:
        {ingredients_text}
        
        Provide 6-8 clear, detailed steps that a home cook can follow. Include cooking times, temperatures, and techniques.
        """
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 800
                }
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
            
            # Split into steps
            steps = [step.strip() for step in content.split('\n') if step.strip() and not step.strip().startswith('#')]
            return steps


fusion_engine = FusionEngine()
openrouter_client = OpenRouterClient()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Mood & AI Service",
        "version": "1.0.0"
    }


@app.post("/mood/interpret", response_model=MoodInterpretationResponse)
async def interpret_mood(request: MoodInterpretationRequest):
    """Interpret mood blend into flavor profile and search keywords"""
    try:
        return fusion_engine.interpret_mood_blend(
            request.mood_blend,
            request.cuisine_preference
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error interpreting mood: {str(e)}")


@app.post("/ai/generate-content", response_model=AIContentResponse)
async def generate_ai_content(request: AIContentRequest):
    """Generate AI content (rationale or directions)"""
    try:
        if request.task == "rationale":
            content = await openrouter_client.generate_emotional_rationale(
                request.recipe,
                request.mood_interpretation
            )
        elif request.task == "directions":
            content = await openrouter_client.generate_cooking_directions(request.recipe)
        else:
            raise ValueError("Task must be 'rationale' or 'directions'")
        
        return AIContentResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating AI content: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get('PORT', 8003))
    uvicorn.run(app, host="0.0.0.0", port=port)
