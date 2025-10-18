# Edamam API JSON Format Documentation

## 🎯 Purpose
This document provides the complete JSON format reference for the Edamam Recipe Search API used in SavorMe. This is essential for understanding API responses and debugging recipe data issues.

**Cross-References**:
- `MASTER_FILE_ORGANIZATION.md` - Lists this file in Technical Documentation
- `EDAMAM_API_INTEGRATION_GUIDE.md` - High-level API integration guide
- `app/services/edamam_client.py` - Implementation that parses these formats

---

## 📡 API Endpoint

```
GET https://api.edamam.com/api/recipes/v2
```

### Query Parameters
```python
params = {
    "type": "public",
    "q": "search_query",                    # e.g., "salmon omega-3 leafy"
    "app_id": "your_app_id",
    "app_key": "your_app_key",
    "cuisineType": "Mediterranean",         # Can be multiple
    "diet": "low-carb",                     # e.g., "vegetarian", "vegan"
    "health": "gluten-free",                # e.g., "peanut-free"
    "calories": "400-600",                  # Calorie range
    "nutrients[PROCNT]": "20-40"            # Protein range (g)
}
```

---

## 📋 Response Structure

### Top-Level Response
```json
{
    "from": 1,
    "to": 20,
    "count": 10000,
    "_links": {
        "self": { "href": "...", "title": "Self" },
        "next": { "href": "...", "title": "Next page" }
    },
    "hits": [
        {
            "recipe": { /* Recipe object (see below) */ },
            "_links": {
                "self": { "href": "...", "title": "Self" }
            }
        }
    ]
}
```

---

## 🍽️ Recipe Object Format

### Complete Recipe Structure
```json
{
    "uri": "http://www.edamam.com/ontologies/edamam.owl#recipe_abc123",
    "label": "Grilled Salmon with Quinoa",
    "image": "https://edamam-product-images.s3.amazonaws.com/...",
    "images": {
        "THUMBNAIL": {
            "url": "https://...",
            "width": 100,
            "height": 100
        },
        "SMALL": {
            "url": "https://...",
            "width": 200,
            "height": 200
        },
        "REGULAR": {
            "url": "https://...",
            "width": 300,
            "height": 300
        },
        "LARGE": {
            "url": "https://...",
            "width": 600,
            "height": 600
        }
    },
    "source": "Serious Eats",
    "url": "https://www.seriouseats.com/...",
    "shareAs": "http://www.edamam.com/recipe/...",
    "yield": 4.0,
    "dietLabels": [
        "Low-Carb",
        "High-Protein"
    ],
    "healthLabels": [
        "Sugar-Conscious",
        "Peanut-Free",
        "Tree-Nut-Free",
        "Alcohol-Free"
    ],
    "cautions": [
        "Sulfites"
    ],
    "ingredientLines": [
        "2 salmon fillets (6 oz each)",
        "1 cup quinoa, uncooked",
        "2 cups baby spinach",
        "1 tablespoon olive oil",
        "Salt and pepper to taste"
    ],
    "ingredients": [
        {
            "text": "2 salmon fillets (6 oz each)",
            "quantity": 2.0,
            "measure": "fillet",
            "food": "salmon",
            "weight": 340.0,
            "foodCategory": "seafood",
            "foodId": "food_bhg...",
            "image": "https://www.edamam.com/food-img/..."
        }
    ],
    "calories": 564.32,
    "totalWeight": 815.5,
    "totalTime": 30.0,
    "cuisineType": [
        "mediterranean"
    ],
    "mealType": [
        "lunch/dinner"
    ],
    "dishType": [
        "main course"
    ],
    "totalNutrients": {
        "ENERC_KCAL": {
            "label": "Energy",
            "quantity": 564.32,
            "unit": "kcal"
        },
        "FAT": {
            "label": "Fat",
            "quantity": 18.45,
            "unit": "g"
        },
        "FASAT": {
            "label": "Saturated",
            "quantity": 3.12,
            "unit": "g"
        },
        "FATRN": {
            "label": "Trans",
            "quantity": 0.0,
            "unit": "g"
        },
        "FAMS": {
            "label": "Monounsaturated",
            "quantity": 7.89,
            "unit": "g"
        },
        "FAPU": {
            "label": "Polyunsaturated",
            "quantity": 5.67,
            "unit": "g"
        },
        "CHOCDF": {
            "label": "Carbs",
            "quantity": 62.45,
            "unit": "g"
        },
        "CHOCDF.net": {
            "label": "Carbohydrates (net)",
            "quantity": 55.12,
            "unit": "g"
        },
        "FIBTG": {
            "label": "Fiber",
            "quantity": 7.33,
            "unit": "g"
        },
        "SUGAR": {
            "label": "Sugars",
            "quantity": 2.45,
            "unit": "g"
        },
        "PROCNT": {
            "label": "Protein",
            "quantity": 38.67,
            "unit": "g"
        },
        "CHOLE": {
            "label": "Cholesterol",
            "quantity": 94.0,
            "unit": "mg"
        },
        "NA": {
            "label": "Sodium",
            "quantity": 167.0,
            "unit": "mg"
        },
        "CA": {
            "label": "Calcium",
            "quantity": 89.5,
            "unit": "mg"
        },
        "MG": {
            "label": "Magnesium",
            "quantity": 184.3,
            "unit": "mg"
        },
        "K": {
            "label": "Potassium",
            "quantity": 987.6,
            "unit": "mg"
        },
        "FE": {
            "label": "Iron",
            "quantity": 3.45,
            "unit": "mg"
        },
        "ZN": {
            "label": "Zinc",
            "quantity": 2.34,
            "unit": "mg"
        },
        "P": {
            "label": "Phosphorus",
            "quantity": 456.7,
            "unit": "mg"
        },
        "VITA_RAE": {
            "label": "Vitamin A",
            "quantity": 234.5,
            "unit": "µg"
        },
        "VITC": {
            "label": "Vitamin C",
            "quantity": 12.3,
            "unit": "mg"
        },
        "THIA": {
            "label": "Thiamin (B1)",
            "quantity": 0.34,
            "unit": "mg"
        },
        "RIBF": {
            "label": "Riboflavin (B2)",
            "quantity": 0.45,
            "unit": "mg"
        },
        "NIA": {
            "label": "Niacin (B3)",
            "quantity": 12.34,
            "unit": "mg"
        },
        "VITB6A": {
            "label": "Vitamin B6",
            "quantity": 0.89,
            "unit": "mg"
        },
        "FOLDFE": {
            "label": "Folate (equivalent)",
            "quantity": 145.6,
            "unit": "µg"
        },
        "FOLFD": {
            "label": "Folate (food)",
            "quantity": 145.6,
            "unit": "µg"
        },
        "FOLAC": {
            "label": "Folic Acid",
            "quantity": 0.0,
            "unit": "µg"
        },
        "VITB12": {
            "label": "Vitamin B12",
            "quantity": 4.56,
            "unit": "µg"
        },
        "VITD": {
            "label": "Vitamin D",
            "quantity": 14.5,
            "unit": "µg"
        },
        "TOCPHA": {
            "label": "Vitamin E",
            "quantity": 3.45,
            "unit": "mg"
        },
        "VITK1": {
            "label": "Vitamin K",
            "quantity": 78.9,
            "unit": "µg"
        }
    },
    "totalDaily": {
        "ENERC_KCAL": {
            "label": "Energy",
            "quantity": 28.22,
            "unit": "%"
        },
        "FAT": {
            "label": "Fat",
            "quantity": 28.38,
            "unit": "%"
        },
        "FASAT": {
            "label": "Saturated",
            "quantity": 15.6,
            "unit": "%"
        },
        "CHOCDF": {
            "label": "Carbs",
            "quantity": 20.82,
            "unit": "%"
        },
        "FIBTG": {
            "label": "Fiber",
            "quantity": 29.32,
            "unit": "%"
        },
        "PROCNT": {
            "label": "Protein",
            "quantity": 77.34,
            "unit": "%"
        },
        "CHOLE": {
            "label": "Cholesterol",
            "quantity": 31.33,
            "unit": "%"
        },
        "NA": {
            "label": "Sodium",
            "quantity": 6.96,
            "unit": "%"
        },
        "CA": {
            "label": "Calcium",
            "quantity": 8.95,
            "unit": "%"
        },
        "MG": {
            "label": "Magnesium",
            "quantity": 43.88,
            "unit": "%"
        },
        "K": {
            "label": "Potassium",
            "quantity": 21.01,
            "unit": "%"
        },
        "FE": {
            "label": "Iron",
            "quantity": 19.17,
            "unit": "%"
        },
        "ZN": {
            "label": "Zinc",
            "quantity": 21.27,
            "unit": "%"
        }
    },
    "digest": [
        {
            "label": "Fat",
            "tag": "FAT",
            "schemaOrgTag": "fatContent",
            "total": 18.45,
            "hasRDI": true,
            "daily": 28.38,
            "unit": "g",
            "sub": [
                {
                    "label": "Saturated",
                    "tag": "FASAT",
                    "schemaOrgTag": "saturatedFatContent",
                    "total": 3.12,
                    "hasRDI": true,
                    "daily": 15.6,
                    "unit": "g"
                }
            ]
        },
        {
            "label": "Carbs",
            "tag": "CHOCDF",
            "schemaOrgTag": "carbohydrateContent",
            "total": 62.45,
            "hasRDI": true,
            "daily": 20.82,
            "unit": "g",
            "sub": [
                {
                    "label": "Fiber",
                    "tag": "FIBTG",
                    "schemaOrgTag": "fiberContent",
                    "total": 7.33,
                    "hasRDI": true,
                    "daily": 29.32,
                    "unit": "g"
                },
                {
                    "label": "Sugars",
                    "tag": "SUGAR",
                    "schemaOrgTag": "sugarContent",
                    "total": 2.45,
                    "hasRDI": false,
                    "daily": 0.0,
                    "unit": "g"
                }
            ]
        },
        {
            "label": "Protein",
            "tag": "PROCNT",
            "schemaOrgTag": "proteinContent",
            "total": 38.67,
            "hasRDI": true,
            "daily": 77.34,
            "unit": "g"
        }
    ]
}
```

---

## 🔑 Key Nutrient Codes Used in SavorMe

### Primary Nutrients (Always Available)
```python
ENERC_KCAL = "ENERC_KCAL"  # Energy (calories)
PROCNT = "PROCNT"          # Protein
FAT = "FAT"                # Fat
CHOCDF = "CHOCDF"          # Carbohydrates
FIBTG = "FIBTG"            # Fiber
```

### Secondary Nutrients (Mood-Related)
```python
MG = "MG"           # Magnesium (stress, sleep)
FE = "FE"           # Iron (energy, fatigue)
ZN = "ZN"           # Zinc (immune, mood)
VITB12 = "VITB12"   # Vitamin B12 (energy, mood)
FOLDFE = "FOLDFE"   # Folate (mood, serotonin)
VITD = "VITD"       # Vitamin D (mood, seasonal depression)
VITC = "VITC"       # Vitamin C (antioxidant, stress)
CA = "CA"           # Calcium (nerve function)
K = "K"             # Potassium (muscle, nerve function)
P = "P"             # Phosphorus (energy metabolism)
```

See `app/data/edamam_constants.py` for complete list.

---

## 🛠️ SavorMe Usage

### Recipe Parsing
Location: `app/services/edamam_client.py`

```python
def _parse_recipe(self, recipe_data: Dict[str, Any]) -> Recipe:
    """Parse Edamam recipe JSON into SavorMe Recipe model"""
    
    # Extract basic info
    name = recipe_data.get("label", "Unknown Recipe")
    image_url = recipe_data.get("image", "")
    source = recipe_data.get("source", "")
    source_url = recipe_data.get("url", "")
    
    # Extract servings
    servings = int(recipe_data.get("yield", 4))
    
    # Parse ingredients
    ingredients = []
    for ing in recipe_data.get("ingredientLines", []):
        ingredients.append(Ingredient(
            name=ing,
            amount="",
            unit=""
        ))
    
    # Extract nutrition per serving
    total_nutrients = recipe_data.get("totalNutrients", {})
    calories = total_nutrients.get("ENERC_KCAL", {}).get("quantity", 0) / servings
    protein = total_nutrients.get("PROCNT", {}).get("quantity", 0) / servings
    carbs = total_nutrients.get("CHOCDF", {}).get("quantity", 0) / servings
    fat = total_nutrients.get("FAT", {}).get("quantity", 0) / servings
    fiber = total_nutrients.get("FIBTG", {}).get("quantity", 0) / servings
    
    # Extract cuisine and diet labels
    cuisine_types = recipe_data.get("cuisineType", [])
    cuisine_type = cuisine_types[0] if cuisine_types else "international"
    
    diet_labels = recipe_data.get("dietLabels", [])
    health_labels = recipe_data.get("healthLabels", [])
    
    return Recipe(...)
```

### Nutrient Enhancement
Location: `app/services/edamam_client.py`

```python
def extract_full_nutrients_per_serving(self, recipe_data: Dict[str, Any]) -> Dict[str, float]:
    """Extract ALL nutrients from Edamam response"""
    
    total_nutrients = recipe_data.get("totalNutrients", {})
    servings = recipe_data.get("yield", 4)
    
    nutrients = {}
    for nutrient_code, nutrient_data in total_nutrients.items():
        quantity = nutrient_data.get("quantity", 0)
        nutrients[nutrient_code] = quantity / servings
    
    return nutrients
```

---

## 🔍 Common Issues & Solutions

### Issue 1: Missing Images
**Problem**: Recipe has no image or broken image URL

**Solution**: SavorMe uses fallback system
```python
# 1. Try Edamam image
image_url = recipe_data.get("image", "")

# 2. Try images object
if not image_url:
    images = recipe_data.get("images", {})
    if "LARGE" in images:
        image_url = images["LARGE"]["url"]
    elif "REGULAR" in images:
        image_url = images["REGULAR"]["url"]

# 3. Fallback to web search
if not image_url:
    image_url = await web_image_search.search_food_image(recipe_name)
```

### Issue 2: Missing Nutrients
**Problem**: Secondary nutrients not in `totalNutrients`

**Solution**: Use nutrient web lookup service
```python
from app.services.nutrient_web_lookup import nutrient_web_lookup

# Estimate missing nutrients from ingredients
enhanced_nutrients = await nutrient_web_lookup.estimate_nutrients(
    ingredients,
    existing_nutrients
)
```

### Issue 3: Inconsistent Ingredient Format
**Problem**: `ingredientLines` vs `ingredients` array

**Solution**: Use `ingredientLines` for display
```python
# Display format (better for users)
ingredient_lines = recipe_data.get("ingredientLines", [])

# Structured format (for nutrition calculation)
ingredients_array = recipe_data.get("ingredients", [])
```

---

## 📚 References

- **Edamam API Docs**: https://developer.edamam.com/edamam-docs-recipe-api
- **SavorMe Implementation**: `app/services/edamam_client.py`
- **Constants**: `app/data/edamam_constants.py`
- **Integration Guide**: `EDAMAM_API_INTEGRATION_GUIDE.md`

---

**Last Updated**: October 2025  
**Maintained By**: SavorMe Development Team

