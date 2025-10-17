# Edamam API Integration - Complete Technical Documentation

## 🎯 **Purpose**
This document provides comprehensive documentation for the Edamam Recipe Search API integration, ensuring proper input/output handling and reliable communication between SavorMe and Edamam's systems.

## 📊 **API Overview**

### **Service Details**
- **Provider**: Edamam
- **API Version**: v2
- **Base URL**: `https://api.edamam.com/api/recipes/v2`
- **Documentation**: https://developer.edamam.com/edamam-recipe-api
- **Plan**: Developer (Free Tier)
- **Rate Limit**: 10 calls/minute

### **Authentication**
```bash
# Required credentials (stored in .env)
EDAMAM_APP_ID=your_edamam_app_id
EDAMAM_APP_KEY=your_edamam_app_key
EDAMAM_BASE_URL=https://api.edamam.com/api/recipes/v2
```

## 🔗 **Input Format Specification**

### **1. Base Parameters**
```python
{
    "type": "public",           # Recipe type (required)
    "q": "salmon spinach",      # Search query (required)
    "app_id": "YOUR_APP_ID",    # Authentication (required)
    "app_key": "YOUR_APP_KEY"   # Authentication (required)
}
```

### **2. Advanced Filtering Parameters**
```python
{
    # Cuisine filters (multiple values supported)
    "cuisineType": ["Mediterranean", "Asian"],
    
    # Dietary preferences (multiple values supported)
    "diet": ["vegetarian", "vegan"],
    
    # Health restrictions (multiple values supported)
    "health": ["peanut-free", "gluten-free"],
    
    # Excluded ingredients (multiple values supported)
    "excluded": ["nuts", "dairy"],
    
    # Nutritional ranges
    "calories": "400-600",                    # Calorie range
    "nutrients[PROCNT]": "20-40",            # Protein range (grams)
    "nutrients[FIBTG]": "5-15",              # Fiber range (grams)
    
    # Response fields (optimize response size)
    "field": [
        "uri", "label", "image", "images", "source", "url", 
        "yield", "dietLabels", "healthLabels", "ingredients", 
        "calories", "totalNutrients", "totalDaily", "cuisineType",
        "mealType", "dishType"
    ]
}
```

### **3. SavorMe-Specific Query Building**
**File**: `app/services/edamam_client.py` (lines 748-906)

```python
def build_search_query_from_mood(
    self,
    keywords: List[str],                    # From fusion engine
    user_profile: UserProfile,              # User preferences
    nutrition_targets: NutritionTargets     # Calculated targets
) -> Dict[str, Any]:
    
    # Dynamic ingredient replacement for Edamam compatibility
    problematic_ingredients = {
        "rabbit": ["chicken", "turkey", "salmon"],
        "venison": ["beef", "lamb"],
        "bison": ["beef", "turkey"],
        "teff": ["quinoa", "brown rice", "barley"],
        "seitan": ["tofu", "tempeh"],
        # ... complete mapping
    }
    
    # Filter and replace keywords
    filtered_keywords = []
    for keyword in keywords:
        if keyword.lower() in problematic_ingredients:
            replacement = problematic_ingredients[keyword.lower()][0]
            print(f"DEBUG: Replacing '{keyword}' with '{replacement}' for better Edamam compatibility")
            filtered_keywords.append(replacement)
        else:
            filtered_keywords.append(keyword)
    
    # Build final query parameters
    return {
        "query": " ".join(filtered_keywords[:2]),
        "cuisine_types": self._map_cuisine_preference(user_profile.cuisine_preferences),
        "diet_labels": self._map_dietary_preference(user_profile.dietary_preference),
        "health_labels": self._map_allergies(user_profile.food_allergies),
        "calories_range": f"{int(nutrition_targets.calories * 0.15)}-{int(nutrition_targets.calories * 0.50)}",
        "protein_range": f"{int(nutrition_targets.protein_g * 0.10)}-{int(nutrition_targets.protein_g * 0.60)}"
    }
```

## 📤 **Output Format Specification**

### **1. API Response Structure**
```json
{
  "from": 1,
  "to": 10,
  "count": 10000,
  "hits": [
    {
      "recipe": {
        "uri": "http://www.edamam.com/ontologies/edamam.owl#recipe_b79327d05b8e5b838ad6cfd9576b30b6",
        "label": "Mediterranean Salmon with Spinach",
        "image": "https://edamam-product-images.s3.amazonaws.com/...",
        "images": {
          "THUMBNAIL": {
            "url": "https://edamam-product-images.s3.amazonaws.com/...",
            "width": 100,
            "height": 100
          },
          "SMALL": {
            "url": "https://edamam-product-images.s3.amazonaws.com/...",
            "width": 200,
            "height": 200
          },
          "REGULAR": {
            "url": "https://edamam-product-images.s3.amazonaws.com/...",
            "width": 300,
            "height": 300
          },
          "LARGE": {
            "url": "https://edamam-product-images.s3.amazonaws.com/...",
            "width": 600,
            "height": 600
          }
        },
        "source": "Serious Eats",
        "url": "https://www.seriouseats.com/...",
        "shareAs": "http://www.edamam.com/recipe/...",
        "yield": 4,
        "dietLabels": ["Low-Carb"],
        "healthLabels": ["Sugar-Conscious", "Peanut-Free"],
        "cautions": [],
        "ingredientLines": [
          "4 salmon fillets (6 oz each)",
          "2 cups fresh spinach",
          "1/4 cup olive oil"
        ],
        "ingredients": [
          {
            "text": "4 salmon fillets (6 oz each)",
            "quantity": 4,
            "measure": "piece",
            "food": "salmon fillet",
            "weight": 680.38905,
            "foodCategory": "Seafood",
            "foodId": "food_bhncugnadgib5lal4j8dsa6s5oyw"
          }
        ],
        "calories": 1240.5,
        "totalWeight": 907.83,
        "totalTime": 45,
        "cuisineType": ["mediterranean"],
        "mealType": ["lunch/dinner"],
        "dishType": ["main course"],
        "totalNutrients": {
          "ENERC_KCAL": {
            "label": "Energy",
            "quantity": 1240.5,
            "unit": "kcal"
          },
          "PROCNT": {
            "label": "Protein",
            "quantity": 96.2,
            "unit": "g"
          },
          "FIBTG": {
            "label": "Fiber",
            "quantity": 28.4,
            "unit": "g"
          },
          "MG": {
            "label": "Magnesium",
            "quantity": 350.8,
            "unit": "mg"
          },
          "FE": {
            "label": "Iron",
            "quantity": 12.5,
            "unit": "mg"
          },
          "VITC": {
            "label": "Vitamin C",
            "quantity": 45.2,
            "unit": "mg"
          }
        },
        "totalDaily": {
          "ENERC_KCAL": {
            "label": "Energy",
            "quantity": 62.0,
            "unit": "%"
          }
        }
      }
    }
  ]
}
```

### **2. SavorMe Recipe Model Mapping**
**File**: `app/services/edamam_client.py` (lines 215-290)

```python
def _parse_recipe(self, recipe_data: Dict[str, Any]) -> Recipe:
    """Parse Edamam response into SavorMe Recipe model"""
    
    # Extract basic recipe info
    recipe_name = recipe_data.get("label", "Unknown Recipe")
    servings = float(recipe_data.get("yield", 1))
    
    # Parse ingredients
    ingredients = []
    for ing_data in recipe_data.get("ingredients", []):
        ingredient = Ingredient(
            name=ing_data.get("food", ""),
            amount=ing_data.get("text", ""),
            unit=ing_data.get("measure", "")
        )
        ingredients.append(ingredient)
    
    # Parse nutrition (convert total amounts to per-serving)
    nutrients = recipe_data.get("totalNutrients", {})
    nutrition = NutritionInfo(
        calories=nutrients.get("ENERC_KCAL", {}).get("quantity", 0) / servings,
        protein_g=nutrients.get("PROCNT", {}).get("quantity", 0) / servings,
        fiber_g=nutrients.get("FIBTG", {}).get("quantity", 0) / servings,
        carbs_g=nutrients.get("CHOCDF", {}).get("quantity", 0) / servings,
        fat_g=nutrients.get("FAT", {}).get("quantity", 0) / servings,
        sodium_mg=nutrients.get("NA", {}).get("quantity", 0) / servings,
        # Secondary nutrients (enhanced)
        iron_mg=nutrients.get("FE", {}).get("quantity", 0) / servings,
        magnesium_mg=nutrients.get("MG", {}).get("quantity", 0) / servings,
        vitamin_c_mg=nutrients.get("VITC", {}).get("quantity", 0) / servings,
        # ... complete nutrient mapping
    )
    
    return Recipe(
        recipe_id=recipe_data.get("uri", "").split("#")[-1],
        name=recipe_name,
        image_url=self._choose_recipe_image(recipe_data, recipe_name),
        ingredients=ingredients,
        cooking_directions=self._generate_cooking_directions(recipe_data),
        prep_time=None,  # Not provided by Edamam
        cook_time=recipe_data.get("totalTime"),
        servings=int(servings),
        nutrition=nutrition,
        source_url=recipe_data.get("url"),
        source_name=recipe_data.get("source"),
        cuisine_type=recipe_data.get("cuisineType", []),
        meal_type=recipe_data.get("mealType", []),
        dish_type=recipe_data.get("dishType", [])
    )
```

## 🔍 **Nutrient Code Mapping**

### **Complete Nutrient Constants**
**File**: `app/data/edamam_constants.py`

```python
# Macronutrients
ENERC_KCAL = "ENERC_KCAL"  # Energy (kcal)
PROCNT = "PROCNT"          # Protein (g)
FAT = "FAT"                # Total lipid (fat) (g)
CHOCDF = "CHOCDF"          # Carbohydrate, by difference (g)
FIBTG = "FIBTG"            # Fiber, total dietary (g)

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
FOLDFE = "FOLDFE"          # Folate, DFE (µg)

# Nutrient extraction for mood scoring
def extract_full_nutrients_per_serving(self, recipe_data: Dict[str, Any]) -> Dict[str, float]:
    """Extract comprehensive nutrients from Edamam recipe"""
    nutrients_raw = {}
    total_nutrients = recipe_data.get("totalNutrients", {})
    servings = float(recipe_data.get("yield", 1))
    
    # Map Edamam codes to canonical names
    nutrient_map = {
        ENERC_KCAL: "calories",
        PROCNT: "protein",
        CHOCDF: "carbohydrate_by_difference",
        FIBTG: "fiber",
        FAT: "total_fat",
        FE: "iron",
        MG: "magnesium",
        VITC: "vitamin_c",
        VITB12: "vitamin_b12",
        FOLDFE: "folate",
        ZN: "zinc",
        VITD: "vitamin_d"
    }
    
    for edamam_code, canonical_name in nutrient_map.items():
        if edamam_code in total_nutrients:
            quantity = total_nutrients[edamam_code].get("quantity", 0)
            nutrients_raw[canonical_name] = quantity / servings
    
    return nutrients_raw
```

## 🚨 **Error Handling & Fallbacks**

### **1. API Failure Handling**
```python
async def search_recipes(self, query: str, **params) -> List[Recipe]:
    """Search with automatic fallback strategies"""
    try:
        # Primary search with full parameters
        recipes = await self._execute_search(query, **params)
        
        if not recipes:
            # Fallback 1: Simplified search with just first keyword
            simple_query = query.split()[0] if query.split() else query
            recipes = await self._execute_search(simple_query, calories_range=None, protein_range=None)
            
        if not recipes:
            # Fallback 2: Generic healthy keywords
            generic_queries = ["healthy", "nutritious", "balanced", "protein", "vegetables"]
            for generic_query in generic_queries:
                recipes = await self._execute_search(generic_query)
                if recipes:
                    break
                    
        return recipes
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            print(f"RATE LIMIT: Waiting 60 seconds...")
            await asyncio.sleep(60)
            # Retry with simplified parameters
        raise
```

### **2. Image URL Handling**
```python
def _choose_recipe_image(self, recipe_data: dict, recipe_name: str) -> str:
    """Handle problematic Edamam image URLs"""
    image_url = recipe_data.get("image")
    
    if not image_url:
        return None
    
    # Filter out URLs that are too long (AWS S3 signed URLs)
    if len(image_url) > 500:
        print(f"DEBUG: Image URL too long ({len(image_url)} chars) for '{recipe_name}', will use fallback")
        return None
    
    # Filter out generic/decorative images
    if self._is_generic_path(image_url):
        print(f"DEBUG: Image filtered as generic for '{recipe_name}'")
        return None
    
    return image_url
```

### **3. AWS S3 Image URL Issue**
**Problem**: Edamam returns AWS S3 signed URLs that are 1800+ characters long and get rejected by validation.

**Solution**:
```python
def _looks_like_valid_image(self, url: str) -> bool:
    """Skip validation for Edamam S3 URLs - assume they're valid"""
    # Skip validation for Edamam S3 URLs (ChatGPT recommended)
    if "edamam-product-images.s3.amazonaws.com" in url:
        print(f"DEBUG: Trusting Edamam S3 URL: {url[:100]}...")
        return True
    
    # Normal validation for other URLs
    # ... validation logic
```

## 📈 **Performance Optimization**

### **1. Response Field Optimization**
```python
# Only request necessary fields to reduce response size
fields_to_include = [
    "uri", "label", "image", "source", "url", "yield",
    "ingredientLines", "ingredients", "calories", "totalNutrients",
    "cuisineType", "mealType", "dishType"
]

for field in fields_to_include:
    params.append(("field", field))
```

### **2. Nutrition Enhancement Pipeline**
```python
# Enhance nutrition data with web lookup for missing micronutrients
if recipe.ingredients:
    try:
        web_nutrients = await nutrient_web_lookup.get_detailed_nutrients(
            recipe.name, recipe.ingredients
        )
        if web_nutrients:
            recipe.nutrition = self._merge_nutrition_data(recipe.nutrition, web_nutrients)
    except Exception as e:
        print(f"Error enhancing nutrients: {e}")
```

## 🧪 **Testing & Validation**

### **1. API Health Check**
```bash
# Test basic connectivity
curl "https://api.edamam.com/api/recipes/v2?type=public&q=chicken&app_id=YOUR_ID&app_key=YOUR_KEY"
```

### **2. Parameter Validation**
```python
def validate_search_parameters(self, params: dict) -> bool:
    """Validate parameters before API call"""
    required = ["type", "q", "app_id", "app_key"]
    for param in required:
        if param not in params or not params[param]:
            raise ValueError(f"Missing required parameter: {param}")
    
    # Validate ranges
    if "calories" in params:
        calories = params["calories"]
        if not re.match(r'\d+-\d+', calories):
            raise ValueError(f"Invalid calorie range format: {calories}")
    
    return True
```

### **3. Response Parsing Validation**
```python
def validate_recipe_data(self, recipe_data: dict) -> bool:
    """Validate recipe data completeness"""
    required_fields = ["label", "yield", "totalNutrients"]
    for field in required_fields:
        if field not in recipe_data:
            print(f"WARNING: Missing field '{field}' in recipe data")
            return False
    
    # Validate nutrition data
    nutrients = recipe_data.get("totalNutrients", {})
    if not nutrients.get("ENERC_KCAL"):
        print("WARNING: No calorie data available")
        return False
    
    return True
```

## ⚠️ **Critical Issues & Solutions**

### **1. Dynamic Ingredient Replacement**
**Issue**: Exotic ingredients (rabbit, venison, bison, teff, seitan) cause 404 errors
**Solution**: Runtime replacement system in `build_search_query_from_mood()`

### **2. Long AWS S3 URLs**
**Issue**: Edamam returns 1800+ character signed URLs that exceed validation limits
**Solution**: Trust Edamam S3 URLs without HEAD validation

### **3. Rate Limiting**
**Issue**: 10 calls/minute limit can be exceeded during testing
**Solution**: Implement exponential backoff and retry logic

---

**Status**: ✅ PRODUCTION READY  
**Last Updated**: October 2025  
**Version**: 3.2.0
