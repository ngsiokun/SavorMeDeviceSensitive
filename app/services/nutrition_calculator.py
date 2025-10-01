"""
Nutrition Calculator - Estimates daily nutritional needs
Based on Harris-Benedict Equation and WHO guidelines
"""
from app.models.user import UserProfile, Gender, NutritionTargets


class NutritionCalculator:
    """Calculate daily nutritional requirements based on user profile"""
    
    def calculate_bmr(self, profile: UserProfile) -> float:
        """
        Calculate Basal Metabolic Rate using Harris-Benedict Equation
        
        BMR (Male) = 88.362 + (13.397 × weight in kg) + (4.799 × height in cm) - (5.677 × age)
        BMR (Female) = 447.593 + (9.247 × weight in kg) + (3.098 × height in cm) - (4.330 × age)
        """
        if profile.gender == Gender.MALE:
            bmr = (88.362 + 
                   (13.397 * profile.weight_kg) + 
                   (4.799 * profile.height_cm) - 
                   (5.677 * profile.age))
        else:  # Female or Other
            bmr = (447.593 + 
                   (9.247 * profile.weight_kg) + 
                   (3.098 * profile.height_cm) - 
                   (4.330 * profile.age))
        
        return bmr
    
    def calculate_tdee(self, profile: UserProfile, activity_level: str = "moderate") -> float:
        """
        Calculate Total Daily Energy Expenditure
        
        Activity levels:
        - sedentary: BMR × 1.2 (little or no exercise)
        - light: BMR × 1.375 (light exercise 1-3 days/week)
        - moderate: BMR × 1.55 (moderate exercise 3-5 days/week)
        - active: BMR × 1.725 (hard exercise 6-7 days/week)
        - very_active: BMR × 1.9 (very hard exercise & physical job)
        """
        activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        
        bmr = self.calculate_bmr(profile)
        multiplier = activity_multipliers.get(activity_level, 1.55)
        
        return bmr * multiplier
    
    def calculate_protein_needs(self, profile: UserProfile, activity_level: str = "moderate") -> float:
        """
        Calculate daily protein needs
        
        General guidelines:
        - Sedentary: 0.8g per kg body weight
        - Moderately active: 1.2g per kg body weight
        - Very active: 1.6-2.0g per kg body weight
        """
        protein_multipliers = {
            "sedentary": 0.8,
            "light": 1.0,
            "moderate": 1.2,
            "active": 1.6,
            "very_active": 1.8
        }
        
        multiplier = protein_multipliers.get(activity_level, 1.2)
        return profile.weight_kg * multiplier
    
    def calculate_fiber_needs(self, profile: UserProfile) -> float:
        """
        Calculate daily fiber needs
        
        WHO recommendations:
        - Women: 25g per day
        - Men: 38g per day
        """
        if profile.gender == Gender.MALE:
            return 38.0
        else:
            return 25.0
    
    def calculate_nutrition_targets(
        self, 
        profile: UserProfile, 
        activity_level: str = "moderate"
    ) -> NutritionTargets:
        """
        Calculate complete nutrition targets for user
        """
        calories = self.calculate_tdee(profile, activity_level)
        protein_g = self.calculate_protein_needs(profile, activity_level)
        fiber_g = self.calculate_fiber_needs(profile)
        
        # Calculate macros based on balanced diet (if needed)
        # Protein: 4 cal/g, Carbs: 4 cal/g, Fat: 9 cal/g
        # Typical macro split: 30% protein, 40% carbs, 30% fat
        
        protein_calories = protein_g * 4
        fat_calories = calories * 0.30
        carb_calories = calories - protein_calories - fat_calories
        
        carbs_g = carb_calories / 4
        fat_g = fat_calories / 9
        
        # Sodium: WHO recommends < 2000mg per day
        sodium_mg = 2000.0
        
        return NutritionTargets(
            calories=round(calories, 1),
            protein_g=round(protein_g, 1),
            fiber_g=round(fiber_g, 1),
            carbs_g=round(carbs_g, 1),
            fat_g=round(fat_g, 1),
            sodium_mg=sodium_mg
        )


# Singleton instance
nutrition_calculator = NutritionCalculator()

