"""
Edamam API Constants
====================

This module contains all the constants used for the Edamam Recipe API.
Based on the official API documentation: https://api.edamam.com/doc/open-api/recipe-search-v2.yaml

This centralizes all API-related constants to prevent bugs from hardcoded strings
and makes the code more maintainable.
"""

# =============================================================================
# NUTRIENT CODES (from Edamam API documentation)
# =============================================================================

# Basic Macronutrients
ENERC_KCAL = "ENERC_KCAL"  # Energy (kcal)
PROCNT = "PROCNT"          # Protein (g)
FAT = "FAT"                # Total lipid (fat) (g)
CHOCDF = "CHOCDF"          # Carbohydrate, by difference (g)
CHOCDF_NET = "CHOCDF.net"  # Carbohydrates (net) (g)
FIBTG = "FIBTG"            # Fiber, total dietary (g)
FIBER = "FIBER"            # Alternative fiber code (legacy)
SUGAR = "SUGAR"            # Sugars, total (g)
SUGAR_ADDED = "SUGAR.added" # Sugars, added (g)
SUGAR_ALCOHOL = "Sugar.alcohol" # Sugar alcohols (g)

# Fatty Acids
FAMS = "FAMS"              # Fatty acids, total monounsaturated (g)
FAPU = "FAPU"              # Fatty acids, total polyunsaturated (g)
FASAT = "FASAT"            # Fatty acids, total saturated (g)
FATRN = "FATRN"            # Fatty acids, total trans (g)

# Minerals
CA = "CA"                  # Calcium (mg)
FE = "FE"                  # Iron (mg)
MG = "MG"                  # Magnesium (mg)
P = "P"                    # Phosphorus (mg)
K = "K"                    # Potassium (mg)
NA = "NA"                  # Sodium (mg)
ZN = "ZN"                  # Zinc (mg)

# Vitamins
VITA_RAE = "VITA_RAE"      # Vitamin A, RAE (µg)
VITB6A = "VITB6A"          # Vitamin B6 (mg)
VITB12 = "VITB12"          # Vitamin B12 (µg)
VITC = "VITC"              # Vitamin C, total ascorbic acid (mg)
VITD = "VITD"              # Vitamin D (D2 + D3) (µg)
VITK1 = "VITK1"            # Vitamin K (phylloquinone) (µg)
TOCPHA = "TOCPHA"          # Vitamin E (alpha-tocopherol) (mg)
THIA = "THIA"              # Thiamin (mg)
RIBF = "RIBF"              # Riboflavin (mg)
NIA = "NIA"                # Niacin (mg)

# Folate (multiple forms)
FOLAC = "FOLAC"            # Folic acid (µg)
FOLDFE = "FOLDFE"          # Folate, DFE (µg)
FOLFD = "FOLFD"            # Folate (food) (µg)

# Other Nutrients
CHOLE = "CHOLE"            # Cholesterol (mg)
WATER = "WATER"            # Water (g)

# =============================================================================
# NUTRIENT MAPPING DICTIONARIES
# =============================================================================

# Primary nutrients used in basic nutrition info
PRIMARY_NUTRIENTS = {
    "calories": ENERC_KCAL,
    "protein_g": PROCNT,
    "carbs_g": CHOCDF,
    "fat_g": FAT,
    "fiber_g": FIBTG,
    "sodium_mg": NA
}

# Secondary nutrients for mood-based nutrition scoring
SECONDARY_NUTRIENTS = {
    "iron_mg": FE,
    "magnesium_mg": MG,
    "vitamin_b12_mcg": VITB12,
    "folate_mcg": FOLDFE,  # Using DFE (Dietary Folate Equivalents)
    "vitamin_d_iu": VITD,  # Note: API returns µg, we convert to IU
    "omega3_g": None,      # Not directly available in Edamam API
    "zinc_mg": ZN,
    "vitamin_c_mg": VITC
}

# All nutrients for comprehensive parsing
ALL_NUTRIENTS = {
    **PRIMARY_NUTRIENTS,
    **SECONDARY_NUTRIENTS,
    "calcium_mg": CA,
    "potassium_mg": K,
    "phosphorus_mg": P,
    "vitamin_a_mcg": VITA_RAE,
    "vitamin_b6_mg": VITB6A,
    "vitamin_e_mg": TOCPHA,
    "vitamin_k_mcg": VITK1,
    "thiamin_mg": THIA,
    "riboflavin_mg": RIBF,
    "niacin_mg": NIA,
    "cholesterol_mg": CHOLE,
    "sugar_g": SUGAR,
    "saturated_fat_g": FASAT,
    "monounsaturated_fat_g": FAMS,
    "polyunsaturated_fat_g": FAPU
}

# =============================================================================
# NUTRIENT CANONICALIZATION MAPPING
# =============================================================================

# Maps various nutrient names/aliases to canonical names
NUTRIENT_ALIASES = {
    # Energy
    "energy": "calories",
    "kcal": "calories",
    "calorie": "calories",
    
    # Protein
    "protein": "protein_g",
    "proteins": "protein_g",
    
    # Carbohydrates
    "carbohydrate": "carbs_g",
    "carbohydrates": "carbs_g",
    "carbs": "carbs_g",
    "carb": "carbs_g",
    
    # Fat
    "fat": "fat_g",
    "fats": "fat_g",
    "lipid": "fat_g",
    "lipids": "fat_g",
    "total_fat": "fat_g",
    
    # Fiber
    "fiber": "fiber_g",
    "fibre": "fiber_g",
    "dietary_fiber": "fiber_g",
    "total_fiber": "fiber_g",
    
    # Sodium
    "sodium": "sodium_mg",
    "salt": "sodium_mg",
    "na": "sodium_mg",
    
    # Iron
    "iron": "iron_mg",
    "fe": "iron_mg",
    
    # Magnesium
    "magnesium": "magnesium_mg",
    "mg": "magnesium_mg",
    
    # Vitamin B12
    "vitamin_b12": "vitamin_b12_mcg",
    "b12": "vitamin_b12_mcg",
    "cobalamin": "vitamin_b12_mcg",
    
    # Folate
    "folate": "folate_mcg",
    "folic_acid": "folate_mcg",
    "vitamin_b9": "folate_mcg",
    "b9": "folate_mcg",
    
    # Vitamin D
    "vitamin_d": "vitamin_d_iu",
    "vit_d": "vitamin_d_iu",
    "d3": "vitamin_d_iu",
    "d2": "vitamin_d_iu",
    
    # Omega-3
    "omega_3": "omega3_g",
    "omega3": "omega3_g",
    "omega-3": "omega3_g",
    "epa_dha": "omega3_g",
    "epa": "omega3_g",
    "dha": "omega3_g",
    
    # Zinc
    "zinc": "zinc_mg",
    "zn": "zinc_mg",
    
    # Vitamin C
    "vitamin_c": "vitamin_c_mg",
    "vit_c": "vitamin_c_mg",
    "ascorbic_acid": "vitamin_c_mg",
    "c": "vitamin_c_mg"
}

# =============================================================================
# API ENDPOINTS AND CONFIGURATION
# =============================================================================

# Base URL for Edamam Recipe API
BASE_URL = "https://api.edamam.com/api/recipes/v2"

# Required parameters for all API calls
REQUIRED_PARAMS = {
    "type": "public"  # Default to public recipes
}

# Field names to request from API (optimize response size)
DEFAULT_FIELDS = [
    "uri", "label", "image", "source", "url", "yield",
    "dietLabels", "healthLabels", "ingredientLines", "ingredients",
    "calories", "totalNutrients", "totalDaily", "cuisineType",
    "mealType", "dishType"
]

# =============================================================================
# RECIPE TYPE CONSTANTS
# =============================================================================

RECIPE_TYPES = ["public", "user", "edamam-generic"]

DIET_LABELS = [
    "balanced", "high-fiber", "high-protein", "low-carb", 
    "low-fat", "low-sodium"
]

HEALTH_LABELS = [
    "alcohol-cocktail", "alcohol-free", "celery-free", "crustacean-free",
    "dairy-free", "DASH", "egg-free", "fish-free", "fodmap-free",
    "gluten-free", "immuno-supportive", "keto-friendly", "kidney-friendly",
    "kosher", "low-fat-abs", "low-potassium", "low-sugar", "lupine-free",
    "Mediterranean", "mollusk-free", "mustard-free", "no-oil-added",
    "paleo", "peanut-free", "pescatarian", "pork-free", "red-meat-free",
    "sesame-free", "shellfish-free", "soy-free", "sugar-conscious",
    "sulfite-free", "tree-nut-free", "vegan", "vegetarian", "wheat-free"
]

CUISINE_TYPES = [
    "American", "Asian", "British", "Caribbean", "Central Europe",
    "Chinese", "Eastern Europe", "French", "Greek", "Indian",
    "Italian", "Japanese", "Korean", "Kosher", "Mediterranean",
    "Mexican", "Middle Eastern", "Nordic", "South American",
    "South East Asian"
]

MEAL_TYPES = [
    "Breakfast", "Dinner", "Lunch", "Snack", "Teatime"
]

DISH_TYPES = [
    "Biscuits and cookies", "Bread", "Cereals", "Condiments and sauces",
    "Desserts", "Drinks", "Main course", "Pancake", "Preps", "Preserve",
    "Salad", "Sandwiches", "Side dish", "Soup", "Starter", "Sweets"
]

IMAGE_SIZES = ["LARGE", "REGULAR", "SMALL", "THUMBNAIL"]

# =============================================================================
# CONVERSION FACTORS
# =============================================================================

# Vitamin D conversion: 1 µg = 40 IU
VITAMIN_D_CONVERSION_FACTOR = 40.0

# =============================================================================
# HIGH-FIBER INGREDIENTS (for fallback fiber calculation)
# =============================================================================

HIGH_FIBER_INGREDIENTS = [
    'lentil', 'bean', 'chickpea', 'quinoa', 'oats', 'barley',
    'whole grain', 'brown rice', 'black bean', 'kidney bean',
    'navy bean', 'pinto bean', 'lima bean', 'garbanzo bean',
    'split pea', 'black-eyed pea', 'artichoke', 'avocado',
    'raspberry', 'blackberry', 'pear', 'apple', 'banana',
    'broccoli', 'brussels sprout', 'carrot', 'spinach'
]

# =============================================================================
# ERROR HANDLING
# =============================================================================

# Common error codes from Edamam API
ERROR_CODES = {
    "LIMIT_EXCEEDED": "API limit exceeded",
    "INVALID_APP_ID": "Invalid application ID",
    "INVALID_APP_KEY": "Invalid application key",
    "MALFORMED_REQUEST": "Malformed request parameters",
    "NO_RESULTS": "No recipes found for given criteria"
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_nutrient_code(nutrient_name: str) -> str:
    """
    Get the Edamam API nutrient code for a given nutrient name.
    
    Args:
        nutrient_name: The nutrient name (e.g., 'calories', 'protein_g')
        
    Returns:
        The Edamam API nutrient code (e.g., 'ENERC_KCAL', 'PROCNT')
    """
    return ALL_NUTRIENTS.get(nutrient_name, nutrient_name)

def get_canonical_name(nutrient_name: str) -> str:
    """
    Get the canonical nutrient name from various aliases.
    
    Args:
        nutrient_name: Any nutrient name or alias
        
    Returns:
        The canonical nutrient name
    """
    return NUTRIENT_ALIASES.get(nutrient_name.lower(), nutrient_name)

def is_high_fiber_ingredient(ingredient_name: str) -> bool:
    """
    Check if an ingredient is known to be high in fiber.
    
    Args:
        ingredient_name: The name of the ingredient
        
    Returns:
        True if the ingredient is high in fiber
    """
    ingredient_lower = ingredient_name.lower()
    return any(high_fiber in ingredient_lower for high_fiber in HIGH_FIBER_INGREDIENTS)

def convert_vitamin_d_to_iu(mcg: float) -> float:
    """
    Convert Vitamin D from micrograms to International Units.
    
    Args:
        mcg: Vitamin D amount in micrograms
        
    Returns:
        Vitamin D amount in International Units
    """
    return mcg * VITAMIN_D_CONVERSION_FACTOR
