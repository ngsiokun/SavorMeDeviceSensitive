"""
Mood models and enums for SavorMe
"""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class MoodType(str, Enum):
    """Available mood types - Evidence-based only (v2.0.0)"""
    STRESSED = "stressed"
    FATIGUED = "fatigued"
    LOW_MOOD = "low_mood"
    IRRITABLE = "irritable"


class IntensityLevel(str, Enum):
    """Mood intensity levels"""
    A_LITTLE = "a_little"
    MEDIUM = "medium"
    VERY = "very"


class MoodSelection(BaseModel):
    """Single mood with intensity"""
    mood: MoodType
    intensity: IntensityLevel
    
    class Config:
        use_enum_values = True


class MoodBlend(BaseModel):
    """User's mood blend (1-3 moods)"""
    moods: List[MoodSelection] = Field(..., min_length=1, max_length=3)
    
    @validator('moods')
    def validate_unique_moods(cls, v):
        """Ensure no duplicate mood types"""
        mood_types = [mood.mood for mood in v]
        if len(mood_types) != len(set(mood_types)):
            raise ValueError("Each mood can only be selected once")
        return v


class FlavorProfile(BaseModel):
    """Generated flavor profile from mood fusion"""
    flavor_bias: List[str]  # e.g., ["floral", "citrus", "umami"]
    texture_preference: List[str]  # e.g., ["silky", "creamy"]
    culinary_tone: List[str]  # e.g., ["poetic", "slow-paced"]
    search_keywords: List[str]  # Keywords for recipe API search
    
    
class MoodInterpretation(BaseModel):
    """Complete mood interpretation result"""
    mood_blend: MoodBlend
    flavor_profile: FlavorProfile
    interpretation_summary: str
    mood_description: str  # For image generation

