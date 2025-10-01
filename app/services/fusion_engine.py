"""
Mood Fusion Engine - Converts mood combinations into recipe search parameters
"""
from typing import Dict, List
from app.models.mood import MoodBlend, MoodType, IntensityLevel, FlavorProfile, MoodInterpretation


class FusionEngine:
    """
    Translates emotional states into culinary parameters
    """
    
    # Mood to flavor mapping
    MOOD_FLAVOR_MAP: Dict[MoodType, List[str]] = {
        MoodType.DREAMY: ["floral", "citrus", "vanilla", "aromatic", "delicate"],
        MoodType.FIERY: ["spicy", "bold", "peppery", "smoky", "intense"],
        MoodType.FOCUSED: ["clean", "herbal", "sharp", "citrus", "minimal"],
        MoodType.PLAYFUL: ["fruity", "tangy", "colorful", "bright", "sweet"],
        MoodType.CRAVING: ["rich", "creamy", "umami", "indulgent", "savory"],
        MoodType.LIGHT: ["fresh", "crisp", "airy", "light", "refreshing"],
        MoodType.GROUNDED: ["earthy", "nutty", "roasted", "wholesome", "hearty"],
        MoodType.RESTORATIVE: ["warm", "comforting", "healing", "nourishing", "gentle"],
        MoodType.CHARISMATIC: ["vibrant", "exotic", "magnetic", "sophisticated", "bold"],
        MoodType.MELANCHOLY: ["tender", "slow", "subtle", "contemplative", "soft"],
    }
    
    # Mood to texture mapping
    MOOD_TEXTURE_MAP: Dict[MoodType, List[str]] = {
        MoodType.DREAMY: ["silky", "smooth", "velvety", "cloud-like"],
        MoodType.FIERY: ["crispy", "crunchy", "charred", "bold"],
        MoodType.FOCUSED: ["lean", "precise", "clean", "minimal"],
        MoodType.PLAYFUL: ["bouncy", "varied", "fun", "layered"],
        MoodType.CRAVING: ["creamy", "rich", "luscious", "decadent"],
        MoodType.LIGHT: ["airy", "crisp", "delicate", "fluffy"],
        MoodType.GROUNDED: ["dense", "hearty", "substantial", "rustic"],
        MoodType.RESTORATIVE: ["soft", "brothy", "gentle", "warm"],
        MoodType.CHARISMATIC: ["dynamic", "textured", "complex", "layered"],
        MoodType.MELANCHOLY: ["slow-cooked", "tender", "soft", "melt-in-mouth"],
    }
    
    # Mood to culinary tone mapping
    MOOD_TONE_MAP: Dict[MoodType, List[str]] = {
        MoodType.DREAMY: ["poetic", "artistic", "slow-paced", "meditative"],
        MoodType.FIERY: ["bold", "dramatic", "intense", "passionate"],
        MoodType.FOCUSED: ["minimal", "efficient", "precise", "intentional"],
        MoodType.PLAYFUL: ["whimsical", "creative", "fun", "experimental"],
        MoodType.CRAVING: ["indulgent", "sensory", "luxurious", "satisfying"],
        MoodType.LIGHT: ["fresh", "bright", "elegant", "simple"],
        MoodType.GROUNDED: ["traditional", "honest", "comforting", "rustic"],
        MoodType.RESTORATIVE: ["nurturing", "healing", "gentle", "soothing"],
        MoodType.CHARISMATIC: ["flirty", "sophisticated", "impressive", "magnetic"],
        MoodType.MELANCHOLY: ["introspective", "gentle", "tender", "reflective"],
    }
    
    # Intensity multipliers
    INTENSITY_WEIGHTS = {
        IntensityLevel.A_LITTLE: 0.3,
        IntensityLevel.MEDIUM: 0.6,
        IntensityLevel.VERY: 1.0,
    }
    
    # Mood to recipe search keywords
    MOOD_SEARCH_KEYWORDS: Dict[MoodType, List[str]] = {
        MoodType.DREAMY: ["risotto", "soufflé", "mousse", "delicate pasta", "floral"],
        MoodType.FIERY: ["curry", "spicy", "grilled", "chili", "peppers"],
        MoodType.FOCUSED: ["bowl", "salad", "grain bowl", "simple", "clean"],
        MoodType.PLAYFUL: ["colorful", "fusion", "creative", "mixed"],
        MoodType.CRAVING: ["pasta", "creamy", "cheese", "chocolate", "comfort"],
        MoodType.LIGHT: ["salad", "steamed", "fresh", "raw", "light"],
        MoodType.GROUNDED: ["roasted", "stew", "beans", "root vegetables", "hearty soup"],
        MoodType.RESTORATIVE: ["soup", "broth", "porridge", "warm bowl", "healing"],
        MoodType.CHARISMATIC: ["plated", "elegant", "presentation", "gourmet"],
        MoodType.MELANCHOLY: ["slow-cooked", "braised", "comfort", "nostalgic"],
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
        mood_names = [f"{ms.mood.value} ({ms.intensity.value.replace('_', ' ')})" 
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
            MoodType.DREAMY: "Seeking softness and poetic indulgence",
            MoodType.FIERY: "Craving bold intensity and passion",
            MoodType.FOCUSED: "Desiring clarity and precision",
            MoodType.PLAYFUL: "Looking for whimsy and curiosity",
            MoodType.CRAVING: "Longing for sensory indulgence",
            MoodType.LIGHT: "Wanting freshness and airiness",
            MoodType.GROUNDED: "Needing stability and comfort",
            MoodType.RESTORATIVE: "Seeking healing and warmth",
            MoodType.CHARISMATIC: "Desiring radiance and magnetism",
            MoodType.MELANCHOLY: "Embracing tenderness and introspection",
        }
        
        base = summary_templates.get(primary_mood.mood, "Seeking emotional nourishment")
        
        if len(mood_blend.moods) > 1:
            base += f" with hints of {', '.join(m.mood.value for m in mood_blend.moods[1:])}"
        
        return base
    
    def _generate_mood_description(self, mood_blend: MoodBlend, 
                                  flavor_profile: FlavorProfile) -> str:
        """Generate description for image generation"""
        flavors = ", ".join(flavor_profile.flavor_bias[:3])
        tones = ", ".join(flavor_profile.culinary_tone[:2])
        
        return f"{tones} dish with {flavors} flavors"


# Singleton instance
fusion_engine = FusionEngine()

