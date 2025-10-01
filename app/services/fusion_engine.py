"""
Mood Fusion Engine - Converts mood combinations into recipe search parameters
"""
from typing import Dict, List
import random
from app.models.mood import MoodBlend, MoodType, IntensityLevel, FlavorProfile, MoodInterpretation


class FusionEngine:
    """
    Translates emotional states into culinary parameters
    """
    
    # Mood to flavor mapping (Updated for 4 evidence-based moods)
    MOOD_FLAVOR_MAP: Dict[MoodType, List[str]] = {
        MoodType.STRESSED: ["calming", "herbal", "omega-3-rich", "magnesium-rich", "gentle"],
        MoodType.FATIGUED: ["energizing", "iron-rich", "vitamin-c", "complex-carbs", "sustaining"],
        MoodType.LOW_MOOD: ["comforting", "omega-3", "fiber-rich", "wholesome", "nourishing"],
        MoodType.IRRITABLE: ["stabilizing", "protein-rich", "fiber", "low-sugar", "grounding"],
    }
    
    # Mood to texture mapping
    MOOD_TEXTURE_MAP: Dict[MoodType, List[str]] = {
        MoodType.STRESSED: ["soft", "smooth", "gentle", "calming"],
        MoodType.FATIGUED: ["substantial", "energizing", "hearty", "sustaining"],
        MoodType.LOW_MOOD: ["comforting", "warm", "nourishing", "wholesome"],
        MoodType.IRRITABLE: ["balanced", "stable", "grounding", "satisfying"],
    }
    
    # Mood to culinary tone mapping
    MOOD_TONE_MAP: Dict[MoodType, List[str]] = {
        MoodType.STRESSED: ["calming", "gentle", "soothing", "peaceful"],
        MoodType.FATIGUED: ["energizing", "revitalizing", "sustaining", "strengthening"],
        MoodType.LOW_MOOD: ["nurturing", "comforting", "uplifting", "healing"],
        MoodType.IRRITABLE: ["balancing", "grounding", "stabilizing", "calming"],
    }
    
    # Intensity multipliers
    INTENSITY_WEIGHTS = {
        IntensityLevel.A_LITTLE: 0.3,
        IntensityLevel.MEDIUM: 0.6,
        IntensityLevel.VERY: 1.0,
    }
    
    # Mood to recipe search keywords (Updated for 4 evidence-based moods)
    # Using common, everyday ingredients from various cuisines
    # Randomized for variety while maintaining nutrient targets
    MOOD_SEARCH_KEYWORDS: Dict[MoodType, List[str]] = {
        MoodType.STRESSED: [
            # High magnesium + omega-3 options
            ["salmon", "spinach"],
            ["chicken", "broccoli"],
            ["beef", "kale"],
            ["pork", "bok choy"],
            ["tofu", "edamame"],
            ["shrimp", "asparagus"],
            ["turkey", "green beans"],
            ["eggs", "avocado"],
            ["almonds", "quinoa"],
            ["black beans", "brown rice"],
            ["mackerel", "kale"],
            ["walnuts", "spinach"],
            ["chia seeds", "banana"],
            ["pumpkin seeds", "oats"],
            ["sardines", "broccoli"]
        ],
        MoodType.FATIGUED: [
            # High iron + vitamin C options
            ["beef", "bell peppers"],
            ["chicken", "tomatoes"],
            ["pork", "orange"],
            ["lentils", "lemon"],
            ["spinach", "strawberries"],
            ["turkey", "broccoli"],
            ["eggs", "kale"],
            ["tofu", "citrus"],
            ["beans", "cabbage"],
            ["lean meat", "apple"],
            ["lamb", "bell peppers"],
            ["duck", "tomatoes"],
            ["venison", "orange"],
            ["bison", "lemon"],
            ["rabbit", "strawberries"]
        ],
        MoodType.LOW_MOOD: [
            # High fiber + omega-3 options  
            ["salmon", "quinoa"],
            ["chicken", "brown rice"],
            ["fish", "whole grains"],
            ["turkey", "oats"],
            ["beans", "vegetables"],
            ["lentils", "greens"],
            ["chickpeas", "spinach"],
            ["tofu", "broccoli"],
            ["eggs", "avocado"],
            ["tuna", "salad"],
            ["mackerel", "quinoa"],
            ["walnuts", "oats"],
            ["chia seeds", "berries"],
            ["hemp seeds", "banana"],
            ["sardines", "brown rice"]
        ],
        MoodType.IRRITABLE: [
            # High protein + fiber, low sugar options
            ["chicken breast", "vegetables"],
            ["turkey", "beans"],
            ["lean beef", "quinoa"],
            ["pork tenderloin", "broccoli"],
            ["fish", "lentils"],
            ["tofu", "brown rice"],
            ["eggs", "spinach"],
            ["shrimp", "zucchini"],
            ["chicken", "chickpeas"],
            ["lean meat", "green beans"],
            ["lamb", "vegetables"],
            ["duck", "beans"],
            ["venison", "quinoa"],
            ["bison", "broccoli"],
            ["rabbit", "lentils"]
        ],
    }
    
    def interpret_mood_blend(self, mood_blend: MoodBlend, cuisine_preference: str = None) -> MoodInterpretation:
        """
        Convert mood blend into flavor profile and search parameters
        Now with cuisine-aware keyword selection for better personalization!
        """
        flavors = []
        textures = []
        tones = []
        keywords = []
        
        # Aggregate weighted attributes from all moods
        for mood_selection in mood_blend.moods:
            mood = mood_selection.mood
            weight = self.INTENSITY_WEIGHTS[mood_selection.intensity]
            
            # Get top attributes for this mood (weighted by intensity)
            num_items = int(3 * weight) or 1
            
            flavors.extend(self.MOOD_FLAVOR_MAP[mood][:num_items])
            textures.extend(self.MOOD_TEXTURE_MAP[mood][:num_items])
            tones.extend(self.MOOD_TONE_MAP[mood][:num_items])
            
            # Cuisine-aware keyword selection for better personalization
            keyword_options = self.MOOD_SEARCH_KEYWORDS[mood]
            
            # Filter keywords by cuisine preference if provided
            if cuisine_preference:
                cuisine_filtered = self._filter_keywords_by_cuisine(keyword_options, cuisine_preference)
                if cuisine_filtered:  # Use filtered if we found matches
                    keyword_options = cuisine_filtered
            
            # Randomly select from (possibly filtered) keyword variations
            selected_keywords = random.choice(keyword_options) if isinstance(keyword_options[0], list) else keyword_options
            keywords.extend(selected_keywords[:num_items])
        
        # Remove duplicates while preserving order
        flavors = list(dict.fromkeys(flavors))
        textures = list(dict.fromkeys(textures))
        tones = list(dict.fromkeys(tones))
        keywords = list(dict.fromkeys(keywords))
        
        # Create flavor profile
        flavor_profile = FlavorProfile(
            flavor_bias=flavors[:5],  # Top 5 flavors
            texture_preference=textures[:3],  # Top 3 textures
            culinary_tone=tones[:3],  # Top 3 tones
            search_keywords=keywords[:4]  # Top 4 keywords for API search
        )
        
        # Generate interpretation summary
        mood_val = lambda x: x if isinstance(x, str) else x.value
        intensity_val = lambda x: x if isinstance(x, str) else x.value
        mood_names = [f"{mood_val(ms.mood)} ({intensity_val(ms.intensity).replace('_', ' ')})" 
                     for ms in mood_blend.moods]
        interpretation_summary = self._generate_interpretation_summary(mood_blend, flavor_profile)
        mood_description = self._generate_mood_description(mood_blend, flavor_profile)
        
        return MoodInterpretation(
            mood_blend=mood_blend,
            flavor_profile=flavor_profile,
            interpretation_summary=interpretation_summary,
            mood_description=mood_description
        )
    
    def _filter_keywords_by_cuisine(self, keyword_options: List[List[str]], cuisine: str) -> List[List[str]]:
        """
        Filter keyword options to prefer cuisine-appropriate ingredients
        Increases likelihood of culturally relevant recipes!
        """
        # Define cuisine-specific ingredient preferences
        cuisine_ingredients = {
            "Mediterranean": ["salmon", "olive", "chickpeas", "lentils", "lamb", "fish", "feta", "yogurt", "hummus"],
            "Asian": ["pork", "tofu", "bok choy", "edamame", "rice", "noodles", "soy", "ginger", "sesame"],
            "Mexican": ["beans", "corn", "peppers", "tomatoes", "avocado", "chicken", "beef", "cilantro", "lime"],
            "Italian": ["pasta", "tomatoes", "chicken", "cheese", "basil", "olive", "pine nuts", "fish", "risotto"],
            "American": ["beef", "chicken", "turkey", "bacon", "potatoes", "corn", "beans", "apple", "burger"],
            "Other Western": ["beef", "pork", "potatoes", "cheese", "cream", "butter", "chicken", "vegetables"],
        }
        
        # Get preferred ingredients for this cuisine
        preferred_ingredients = cuisine_ingredients.get(cuisine, [])
        if not preferred_ingredients:
            return []  # Return empty to use all keywords
        
        # Filter keyword pairs that contain at least one preferred ingredient
        filtered = []
        for keyword_pair in keyword_options:
            for keyword in keyword_pair:
                if any(pref in keyword.lower() for pref in preferred_ingredients):
                    filtered.append(keyword_pair)
                    break  # Found a match, add this pair
        
        return filtered if filtered else []  # Return empty if no matches (fallback to all)
    
    def _generate_interpretation_summary(self, mood_blend: MoodBlend, 
                                        flavor_profile: FlavorProfile) -> str:
        """Generate human-readable interpretation"""
        primary_mood = mood_blend.moods[0]
        
        summary_templates = {
            MoodType.STRESSED: "Seeking calm and stress relief",
            MoodType.FATIGUED: "Needing energy and vitality",
            MoodType.LOW_MOOD: "Looking for mood support and comfort",
            MoodType.IRRITABLE: "Wanting balance and emotional stability",
        }
        
        base = summary_templates.get(primary_mood.mood, "Seeking emotional nourishment")
        
        mood_val = lambda x: x if isinstance(x, str) else x.value
        if len(mood_blend.moods) > 1:
            base += f" with hints of {', '.join(mood_val(m.mood) for m in mood_blend.moods[1:])}"
        
        return base
    
    def _generate_mood_description(self, mood_blend: MoodBlend, 
                                  flavor_profile: FlavorProfile) -> str:
        """Generate description for image generation"""
        flavors = ", ".join(flavor_profile.flavor_bias[:3])
        tones = ", ".join(flavor_profile.culinary_tone[:2])
        
        return f"{tones} dish with {flavors} flavors"


# Singleton instance
fusion_engine = FusionEngine()

