"""
OpenRouter AI API Client for generating emotional rationale and cooking directions
https://openrouter.ai/docs
"""
import httpx
import re
from typing import List, Dict, Any
from app.core.config import settings
from app.models.recipe import Recipe, EmotionalRationale
from app.models.mood import MoodInterpretation


class OpenRouterClient:
    """Client for OpenRouter AI API"""
    
    def __init__(self):
        self.base_url = f"{settings.OPENROUTER_BASE_URL}/chat/completions"
        self.api_key = settings.OPENROUTER_API_KEY
        self.default_model = "meta-llama/llama-3.1-8b-instruct:free"
    
    async def generate_cooking_directions(
        self,
        recipe_name: str,
        ingredients: List,
        cuisine_type: List[str] = None
    ) -> List[str]:
        """
        Generate step-by-step cooking directions using LLM
        
        Args:
            recipe_name: Name of the recipe
            ingredients: List of ingredients
            cuisine_type: Type of cuisine
        
        Returns:
            List of cooking direction steps
        """
        if not self.api_key or self.api_key == "your_openrouter_api_key":
            # Generate basic cooking directions without API
            return self._generate_fallback_directions(recipe_name, ingredients, cuisine_type)
        
        # Build ingredients list
        ingredients_text = "\n".join([f"- {ing.amount} {ing.name}" for ing in ingredients[:10]])
        cuisine = cuisine_type[0] if cuisine_type else "general"
        
        prompt = f"""Generate comprehensive, detailed cooking directions for this recipe:

Recipe: {recipe_name}
Cuisine: {cuisine}

Ingredients:
{ingredients_text}

Please provide detailed, step-by-step cooking instructions that include:
1. PREPARATION: Ingredient prep, equipment needed, timing estimates
2. COOKING STEPS: Detailed cooking process with specific temperatures, times, and techniques
3. FINISHING: Plating, garnishing, and serving suggestions
4. TIPS: Pro tips for best results, common mistakes to avoid, and variations

Make the directions thorough enough for someone to successfully recreate this dish. Include specific cooking times, temperatures, and techniques. Format as a clear numbered list with detailed explanations for each step."""

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.default_model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a professional chef and cooking instructor providing comprehensive, detailed cooking instructions. Be thorough, specific, and practical. Include cooking times, temperatures, techniques, and helpful tips. Make sure a beginner could follow your instructions successfully."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1200
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                # Parse numbered list from response
                content = data["choices"][0]["message"]["content"]
                steps = self._parse_cooking_steps(content)
                return steps
        
        except Exception as e:
            print(f"Error generating directions: {e}")
            # Use fallback directions instead of just a link
            return self._generate_fallback_directions(recipe_name, ingredients, cuisine_type)
    
    def _parse_cooking_steps(self, content: str) -> List[str]:
        """Parse LLM response into list of steps"""
        steps = []
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Skip section headers (PREPARATION:, COOKING STEPS:, etc.)
            if line.endswith(':') and line.isupper():
                steps.append(line)  # Keep section headers
                continue
            
            # Remove numbering if present (1., 2., etc.)
            import re
            cleaned = re.sub(r'^\d+[\.\)]\s*', '', line)
            
            # Remove bullet points but keep the content
            cleaned = re.sub(r'^[•\-\*]\s*', '', cleaned)
            
            if cleaned and len(cleaned) > 5:  # Include more lines, even shorter ones
                steps.append(cleaned)
        
        return steps if steps else [content]
    
    def _generate_fallback_directions(self, recipe_name: str, ingredients: List, cuisine_type: List[str] = None) -> List[str]:
        """Generate comprehensive cooking directions when API is not available"""
        cuisine = cuisine_type[0] if cuisine_type else "general"
        
        # Comprehensive cooking directions based on cuisine and ingredients
        directions = []
        
        # Analyze ingredients to determine cooking method
        ingredient_names = [ing.name.lower() for ing in ingredients]
        ingredient_text = " ".join(ingredient_names)
        
        # PREPARATION SECTION
        directions.extend([
            "PREPARATION:",
            "• Gather all ingredients and equipment needed",
            "• Wash and prepare all vegetables as required",
            "• Preheat oven to 375°F (190°C) if baking is needed",
            "• Have all seasonings and spices ready",
            ""
        ])
        
        # COOKING STEPS based on ingredients
        if any(meat in ingredient_text for meat in ["beef", "chicken", "pork", "lamb", "turkey"]):
            directions.extend([
                "COOKING STEPS:",
                "• Season the meat generously with salt, pepper, and your choice of herbs (rosemary, thyme, or oregano work well)",
                "• Heat 2 tablespoons of oil in a large oven-safe skillet over medium-high heat",
                "• Brown the meat on all sides for 3-4 minutes per side until golden brown",
                "• Remove meat and set aside. Add chopped vegetables to the same pan",
                "• Cook vegetables for 5-7 minutes until they begin to soften",
                "• Return meat to pan, add any liquid (broth, wine, or water) and bring to a simmer",
                "• Cover and transfer to preheated oven. Bake for 25-35 minutes until meat is tender",
                "• Remove from oven and let rest for 5-10 minutes before serving"
            ])
        elif any(fish in ingredient_text for fish in ["salmon", "tuna", "cod", "halibut", "mackerel"]):
            directions.extend([
                "COOKING STEPS:",
                "• Preheat oven to 400°F (200°C) and heat a large oven-safe skillet over medium heat",
                "• Pat fish dry and season both sides with salt, pepper, and lemon zest",
                "• Add 2 tablespoons of oil to the hot skillet",
                "• Place fish skin-side down (if applicable) and cook for 3-4 minutes without moving",
                "• Carefully flip fish and cook for another 2-3 minutes",
                "• Transfer skillet to oven and bake for 6-10 minutes until fish flakes easily",
                "• Remove from oven and let rest for 2-3 minutes before serving"
            ])
        elif any(veg in ingredient_text for veg in ["bell pepper", "zucchini", "eggplant", "tomato", "onion"]):
            directions.extend([
                "COOKING STEPS:",
                "• Preheat oven to 425°F (220°C) and line a baking sheet with parchment paper",
                "• Cut vegetables into uniform pieces (about 1-inch cubes for even cooking)",
                "• Toss vegetables with 3-4 tablespoons of olive oil, salt, pepper, and herbs",
                "• Arrange vegetables in a single layer on the prepared baking sheet",
                "• Roast for 20-25 minutes, stirring halfway through, until tender and golden",
                "• Check for doneness - vegetables should be easily pierced with a fork",
                "• Season with additional salt, pepper, or herbs to taste"
            ])
        elif any(pasta in ingredient_text for pasta in ["pasta", "noodles", "spaghetti", "penne"]):
            directions.extend([
                "COOKING STEPS:",
                "• Bring a large pot of salted water to a rolling boil",
                "• Add pasta and cook according to package directions, stirring occasionally",
                "• Meanwhile, heat oil in a large skillet over medium heat",
                "• Add aromatics (garlic, onions) and cook for 2-3 minutes until fragrant",
                "• Add other ingredients and cook until heated through",
                "• Reserve 1 cup of pasta water before draining pasta",
                "• Toss cooked pasta with sauce and ingredients, adding pasta water as needed",
                "• Cook for 1-2 minutes more until sauce coats pasta evenly"
            ])
        else:
            directions.extend([
                "COOKING STEPS:",
                "• Heat 2-3 tablespoons of oil or butter in a large pan over medium heat",
                "• Add aromatics (onions, garlic) and cook for 2-3 minutes until softened",
                "• Add main ingredients in order of cooking time (hardest vegetables first)",
                "• Season with salt, pepper, and herbs, stirring frequently",
                "• Cook for 10-15 minutes, adding small amounts of liquid if needed",
                "• Taste and adjust seasoning as needed",
                "• Continue cooking until all ingredients are tender and flavors are combined"
            ])
        
        # FINISHING SECTION
        directions.extend([
            "",
            "FINISHING:",
            "• Taste and adjust seasoning with salt, pepper, or additional herbs",
            "• Plate the dish attractively, considering color and texture contrast",
            "• Garnish with fresh herbs, citrus zest, or a drizzle of quality oil",
            "• Serve immediately while hot for best flavor and texture",
            "",
            "TIPS:",
            "• Don't overcrowd the pan - cook in batches if necessary",
            "• Let meat rest after cooking to redistribute juices",
            "• Taste as you cook and adjust seasoning gradually",
            "• Keep ingredients at room temperature for even cooking",
            "• Use a meat thermometer for perfect doneness (145°F for most meats)"
        ])
        
        return directions
    
    async def generate_emotional_rationale(
        self,
        recipe: Recipe,
        mood_interpretation: MoodInterpretation
    ) -> EmotionalRationale:
        """
        Generate emotional rationale explaining why recipe matches user's mood
        """
        if not self.api_key:
            # Return a basic rationale if no API key
            return self._generate_fallback_rationale(recipe, mood_interpretation)
        
        # Build prompt
        prompt = self._build_rationale_prompt(recipe, mood_interpretation)
        
        try:
            # Make API request
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.default_model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a poetic food writer who creates emotional connections between recipes and moods. Write in a warm, lyrical style that helps users understand why a dish resonates with their feelings."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.8,
                        "max_tokens": 800
                    }
                )
                response.raise_for_status()
                data = response.json()
            
            # Parse response
            content = data["choices"][0]["message"]["content"]
            return self._parse_rationale_response(content, mood_interpretation)
        
        except Exception as e:
            print(f"OpenRouter API error: {e}")
            return self._generate_fallback_rationale(recipe, mood_interpretation)
    
    def _build_rationale_prompt(self, recipe: Recipe, mood_interpretation: MoodInterpretation) -> str:
        """Build prompt for LLM"""
        mood_val = lambda x: x if isinstance(x, str) else x.value
        intensity_val = lambda x: x if isinstance(x, str) else x.value
        moods_str = ", ".join([
            f"{mood_val(m.mood)} ({intensity_val(m.intensity).replace('_', ' ')})" 
            for m in mood_interpretation.mood_blend.moods
        ])
        
        flavors = ", ".join(mood_interpretation.flavor_profile.flavor_bias)
        textures = ", ".join(mood_interpretation.flavor_profile.texture_preference)
        tones = ", ".join(mood_interpretation.flavor_profile.culinary_tone)
        
        prompt = f"""Create an emotional rationale for why this recipe matches the user's mood.

Recipe: {recipe.name}
Ingredients: {", ".join([ing.name for ing in recipe.ingredients[:5]])}

User's Mood Blend: {moods_str}
Desired Flavors: {flavors}
Desired Textures: {textures}
Culinary Tone: {tones}

Interpretation: {mood_interpretation.interpretation_summary}

Please provide:
1. OVERALL_RATIONALE: A poetic 2-3 sentence explanation of why this dish matches their emotional state
2. MOOD_BREAKDOWNS: For each mood, explain how specific elements of the dish support it (1 sentence each)
3. PLATING_SUGGESTION: A brief, artistic plating suggestion that enhances the emotional experience
4. JOURNALING_PROMPT: A reflective question to help them connect with their experience

Format your response as:
OVERALL_RATIONALE:
[your response]

MOOD_BREAKDOWNS:
{mood_val(mood_interpretation.mood_blend.moods[0].mood)}: [explanation]
{mood_val(mood_interpretation.mood_blend.moods[1].mood) if len(mood_interpretation.mood_blend.moods) > 1 else ""}: [explanation]

PLATING_SUGGESTION:
[your response]

JOURNALING_PROMPT:
[your response]
"""
        return prompt
    
    def _parse_rationale_response(self, content: str, mood_interpretation: MoodInterpretation) -> EmotionalRationale:
        """Parse LLM response into EmotionalRationale model"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split("\n"):
            line = line.strip()
            if not line:
                continue
            
            if line.startswith("OVERALL_RATIONALE:"):
                current_section = "overall"
                current_content = []
            elif line.startswith("MOOD_BREAKDOWNS:"):
                if current_section:
                    sections[current_section] = "\n".join(current_content)
                current_section = "moods"
                current_content = []
            elif line.startswith("PLATING_SUGGESTION:"):
                if current_section:
                    sections[current_section] = "\n".join(current_content)
                current_section = "plating"
                current_content = []
            elif line.startswith("JOURNALING_PROMPT:"):
                if current_section:
                    sections[current_section] = "\n".join(current_content)
                current_section = "journal"
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = "\n".join(current_content)
        
        # Parse mood breakdowns
        mood_breakdowns = []
        if "moods" in sections:
            for line in sections["moods"].split("\n"):
                if ":" in line:
                    mood, explanation = line.split(":", 1)
                    mood_breakdowns.append({
                        "mood": mood.strip(),
                        "explanation": explanation.strip()
                    })
        
        return EmotionalRationale(
            overall_rationale=sections.get("overall", "This dish complements your emotional state beautifully."),
            mood_breakdowns=mood_breakdowns,
            plating_suggestion=sections.get("plating", "Serve with care and attention to presentation."),
            journaling_prompt=sections.get("journal", "How does this meal make you feel?")
        )
    
    def _generate_fallback_rationale(self, recipe: Recipe, mood_interpretation: MoodInterpretation) -> EmotionalRationale:
        """Generate basic rationale when AI is unavailable"""
        mood_val = lambda x: x if isinstance(x, str) else x.value
        mood_breakdowns = []
        for mood_sel in mood_interpretation.mood_blend.moods:
            mood_str = mood_val(mood_sel.mood)
            mood_breakdowns.append({
                "mood": mood_str,
                "explanation": f"The {', '.join(mood_interpretation.flavor_profile.flavor_bias[:2])} flavors complement your {mood_str} mood."
            })
        
        return EmotionalRationale(
            overall_rationale=f"This {recipe.name} was chosen to match your {mood_interpretation.interpretation_summary.lower()}.",
            mood_breakdowns=mood_breakdowns,
            plating_suggestion="Plate thoughtfully with attention to color and texture contrast.",
            journaling_prompt="What emotions arise as you prepare and enjoy this meal?"
        )


# Singleton instance
openrouter_client = OpenRouterClient()

