"""
Mood Fusion Engine - Converts mood combinations into recipe search parameters
"""
from typing import Dict, List
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
    MOOD_SEARCH_KEYWORDS: Dict[MoodType, List[str]] = {
        MoodType.STRESSED: ["salmon", "spinach", "nuts", "leafy greens", "whole grains"],
        MoodType.FATIGUED: ["lean meat", "lentils", "spinach", "citrus", "quinoa"],
        MoodType.LOW_MOOD: ["fish", "beans", "berries", "leafy greens", "whole grains"],
        MoodType.IRRITABLE: ["chicken", "beans", "vegetables", "whole grains", "lean protein"],
    }
    
    def interpret_mood_blend(self, mood_blend: MoodBlend) -> MoodInterpretation:
        """
        Convert mood blend into flavor profile and search parameters
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
            keywords.extend(self.MOOD_SEARCH_KEYWORDS[mood][:num_items])
        
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

