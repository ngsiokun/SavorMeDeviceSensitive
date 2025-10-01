"""
OpenRouter AI API Client for generating emotional rationale
https://openrouter.ai/docs
"""
import httpx
from typing import List, Dict, Any
from app.core.config import settings
from app.models.recipe import Recipe, EmotionalRationale
from app.models.mood import MoodInterpretation


class OpenRouterClient:
    """Client for OpenRouter AI API"""
    
    def __init__(self):
        self.base_url = f"{settings.OPENROUTER_BASE_URL}/chat/completions"
        self.api_key = settings.OPENROUTER_API_KEY
        self.default_model = "anthropic/claude-3.5-sonnet"
    
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

