"""
User & Nutrition Service
Handles user profile management and nutrition calculations
"""
import sys
import os
from pathlib import Path

# Add shared models to path
sys.path.append(str(Path(__file__).parent.parent / "shared"))

from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from shared.models import (
    UserProfile, 
    NutritionTargets, 
    ActivityLevel,
    NutritionCalculationRequest,
    NutritionCalculationResponse
)

app = FastAPI(
    title="SavorMe User & Nutrition Service",
    description="Handles user profiles and nutrition calculations",
    version="1.0.0"
)


class NutritionCalculator:
    """Calculates nutrition targets using medical formulas"""
    
    @staticmethod
    def calculate_bmr(profile: UserProfile) -> float:
        """Calculate Basal Metabolic Rate using Harris-Benedict equation"""
        if profile.gender.lower() == "female":
            bmr = 655 + (9.6 * profile.weight_kg) + (1.8 * profile.height_cm) - (4.7 * profile.age)
        else:  # male
            bmr = 66 + (13.7 * profile.weight_kg) + (5 * profile.height_cm) - (6.8 * profile.age)
        return bmr
    
    @staticmethod
    def calculate_tdee(bmr: float, activity_level: ActivityLevel) -> float:
        """Calculate Total Daily Energy Expenditure"""
        activity_factors = {
            ActivityLevel.SEDENTARY: 1.2,
            ActivityLevel.LIGHT: 1.375,
            ActivityLevel.MODERATE: 1.55,
            ActivityLevel.ACTIVE: 1.725,
            ActivityLevel.VERY_ACTIVE: 1.9
        }
        return bmr * activity_factors.get(activity_level, 1.55)
    
    @staticmethod
    def calculate_nutrition_targets(profile: UserProfile) -> NutritionTargets:
        """Calculate complete nutrition targets"""
        bmr = NutritionCalculator.calculate_bmr(profile)
        tdee = NutritionCalculator.calculate_tdee(bmr, profile.activity_level)
        
        # WHO guidelines
        protein_g = profile.weight_kg * 1.2  # 1.2g per kg body weight
        
        # Fiber guidelines
        if profile.gender.lower() == "female":
            fiber_g = 25.0
        else:
            fiber_g = 38.0
        
        # Macronutrient distribution
        carbs_g = (tdee * 0.45) / 4  # 45% calories from carbs
        fat_g = (tdee * 0.25) / 9    # 25% calories from fat
        
        return NutritionTargets(
            calories=tdee,
            protein_g=protein_g,
            fiber_g=fiber_g,
            carbs_g=carbs_g,
            fat_g=fat_g,
            sodium_mg=2300.0  # Daily limit
        )


nutrition_calculator = NutritionCalculator()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "User & Nutrition Service",
        "version": "1.0.0"
    }


@app.post("/nutrition/calculate", response_model=NutritionCalculationResponse)
async def calculate_nutrition(request: NutritionCalculationRequest):
    """Calculate nutrition targets for user profile"""
    try:
        profile = request.user_profile
        nutrition_targets = nutrition_calculator.calculate_nutrition_targets(profile)
        bmr = nutrition_calculator.calculate_bmr(profile)
        tdee = nutrition_calculator.calculate_tdee(bmr, profile.activity_level)
        
        return NutritionCalculationResponse(
            nutrition_targets=nutrition_targets,
            bmr=bmr,
            tdee=tdee
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating nutrition: {str(e)}")


@app.post("/user/profile/validate")
async def validate_user_profile(profile: UserProfile):
    """Validate user profile data"""
    try:
        # Basic validation
        if profile.age < 1 or profile.age > 120:
            raise ValueError("Age must be between 1 and 120")
        
        if profile.height_cm < 50 or profile.height_cm > 300:
            raise ValueError("Height must be between 50 and 300 cm")
        
        if profile.weight_kg < 20 or profile.weight_kg > 500:
            raise ValueError("Weight must be between 20 and 500 kg")
        
        return {
            "valid": True,
            "message": "Profile is valid",
            "profile_summary": {
                "age": profile.age,
                "gender": profile.gender,
                "bmi": round(profile.weight_kg / ((profile.height_cm / 100) ** 2), 1)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid profile: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get('PORT', 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
