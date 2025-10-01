# Complete Flow: Mood → Nutrients → Recipe

## End-to-End Example: User Feeling Stressed

Let me walk you through exactly how the system works from a user selecting "Stressed" to getting a specific recipe recommendation.

---

## 🎯 Step-by-Step Flow

### **Step 1: User Input**

```json
{
  "mood_blend": {
    "moods": [
      {"mood": "stressed", "intensity": "very"}
    ]
  },
  "user_profile": {
    "age": 32,
    "gender": "female",
    "height_cm": 165,
    "weight_kg": 60,
    "cuisine_preferences": ["Mediterranean", "Asian"],
    "food_allergies": [],
    "dietary_preference": "none"
  }
}
```

**What happens**: User selects "Stressed / Anxious" at "very" intensity

---

### **Step 2: Mood → Nutrient Targets** 
*[MoodNutritionEngine]*

The system loads `mood_mapping.json` and looks up "stressed":

```python
# From mood_mapping.json
{
  "id": "stressed",
  "targets": {
    "nutrients": [
      {"name": "magnesium", "unit": "mg", "min_per_meal": 120, "weight": 1.0},
      {"name": "omega_3_epa_dha", "unit": "g", "min_per_meal": 0.3, "weight": 0.9},
      {"name": "fiber", "unit": "g", "min_per_meal": 8, "weight": 0.7},
      {"name": "added_sugar", "unit": "g", "max_per_meal": 10, "weight": 0.6}
    ]
  }
}
```

**Intensity Weighting** (since intensity = "very"):
```python
INTENSITY_WEIGHTS = {
    "a_little": 0.3,
    "medium": 0.6,
    "very": 1.0
}

# "very" = 1.0, so targets stay at full strength
```

**Output**: Nutrient targets for this meal
```
- Magnesium: ≥120mg (importance: 1.0)
- Omega-3 EPA/DHA: ≥0.3g (importance: 0.9)
- Fiber: ≥8g (importance: 0.7)
- Added Sugar: ≤10g (importance: 0.6)
```

---

### **Step 3: Calculate User's Daily Nutrition Needs**
*[NutritionCalculator]*

```python
# Harris-Benedict BMR for female
BMR = 447.593 + (9.247 × 60kg) + (3.098 × 165cm) - (4.330 × 32)
    = 447.593 + 554.82 + 511.17 - 138.56
    = 1,375 kcal (BMR)

# TDEE (moderate activity = BMR × 1.55)
TDEE = 1,375 × 1.55 = 2,131 kcal/day

# Protein needs (moderate activity = 1.2g/kg)
Protein = 60kg × 1.2 = 72g/day

# Fiber needs (female = 25g/day per WHO)
Fiber = 25g/day
```

**Output**: Daily targets
```
Calories: 2,131 kcal/day
Protein: 72g/day
Fiber: 25g/day
```

---

### **Step 4: Build Recipe Search Query**
*[EdamamClient.build_search_query_from_mood()]*

**A. Generate Search Keywords** (from old Fusion Engine for variety):
```python
# For "stressed" mood, generate flavorful search terms
keywords = ["salmon", "spinach", "quinoa"]  # Magnesium & omega-3 rich
```

**B. Build Edamam API Query**:
```python
query_params = {
    "q": "salmon spinach",  # Search term
    "app_id": "YOUR_EDAMAM_ID",
    "app_key": "YOUR_EDAMAM_KEY",
    
    # Nutrition ranges (for one meal = ~30% of daily)
    "calories": "500-700",      # ~30% of 2,131
    "protein": "20-40",         # ~30% of 72g
    
    # Dietary filters
    "cuisineType": ["Mediterranean", "Asian"],
    "health": [],  # No allergies
    "diet": []     # No restrictions
}
```

---

### **Step 5: Search Recipes**
*[EdamamClient.search_recipes()]*

**API Call**:
```
GET https://api.edamam.com/api/recipes/v2?
  q=salmon+spinach
  &calories=500-700
  &protein=20-40
  &cuisineType=Mediterranean
  &app_id=xxx
  &app_key=xxx
```

**Edamam Returns** (example recipes):
```json
{
  "hits": [
    {
      "recipe": {
        "label": "Baked Salmon with Spinach and Quinoa",
        "yield": 4,
        "totalNutrients": {
          "ENERC_KCAL": {"quantity": 2340},  // total for 4 servings
          "PROCNT": {"quantity": 136},        // protein
          "FIBTG": {"quantity": 32},          // fiber
          "FE": {"quantity": 28},             // iron (28mg total)
          "MG": {"quantity": 560},            // magnesium (560mg total)
          "VITC": {"quantity": 120},          // vitamin C
          "EPA": {"quantity": 800},           // EPA (mg)
          "DHA": {"quantity": 1200}           // DHA (mg)
        }
      }
    },
    // ... more recipes
  ]
}
```

---

### **Step 6: Extract & Normalize Nutrients**
*[EdamamClient.extract_full_nutrients_per_serving()]*

**Raw Extraction** (total → per serving):
```python
servings = 4

nutrients_per_serving = {
    "calories": 2340 / 4 = 585 kcal,
    "protein": 136 / 4 = 34g,
    "fiber": 32 / 4 = 8g,
    "iron": 28 / 4 = 7mg,
    "magnesium": 560 / 4 = 140mg,
    "vitamin_c": 120 / 4 = 30mg,
    "omega_3_epa_dha": (800 + 1200) / 4 / 1000 = 0.5g  // Convert mg to g
}
```

**Canonicalize Nutrients** (using aliases):
```python
# MoodNutritionEngine.canonicalize_nutrients()
nutrient_aliases = {
    "magnesium": ["MG", "Magnesium, Mg", "magnesium"],
    "omega_3_epa_dha": ["EPA", "DHA", "epa", "dha"]
}

canonical_nutrients = {
    "calories": 585,
    "protein": 34,
    "fiber": 8,
    "iron": 7,
    "magnesium": 140,        # ← Matched from "MG"
    "vitamin_c": 30,
    "omega_3_epa_dha": 0.5   # ← Combined EPA+DHA
}
```

---

### **Step 7: Score Recipe Against Mood Targets**
*[MoodNutritionEngine.score_recipe()]*

**For each nutrient target**:

#### A. Magnesium (target: ≥120mg, weight: 1.0)
```python
value = 140mg
min_target = 120mg

# Recipe exceeds minimum
contribution = min(1.25, 140 / 120) = min(1.25, 1.167) = 1.167

weighted_score = 1.167 × 1.0 = 1.167
```

#### B. Omega-3 (target: ≥0.3g, weight: 0.9)
```python
value = 0.5g
min_target = 0.3g

# Recipe exceeds minimum
contribution = min(1.25, 0.5 / 0.3) = min(1.25, 1.667) = 1.25 (capped)

weighted_score = 1.25 × 0.9 = 1.125
```

#### C. Fiber (target: ≥8g, weight: 0.7)
```python
value = 8g
min_target = 8g

# Recipe meets exactly
contribution = min(1.25, 8 / 8) = 1.0

weighted_score = 1.0 × 0.7 = 0.7
```

#### D. Added Sugar (target: ≤10g, weight: 0.6)
```python
value = 5g (assume from recipe)
max_target = 10g

# Recipe is below maximum (good)
contribution = 1.0

weighted_score = 1.0 × 0.6 = 0.6
```

**Calculate Final Score**:
```python
total_weighted = 1.167 + 1.125 + 0.7 + 0.6 = 3.592
total_weight = 1.0 + 0.9 + 0.7 + 0.6 = 3.2

final_score = 3.592 / 3.2 = 1.1225
# On 0-1 scale: 112% (exceeds targets!)
```

**Generate Reasons**:
```python
reasons = [
    "Magnesium: 140mg (target ≥120mg) — supports nervous system and stress response",
    "Omega-3 EPA/DHA: 0.5g (target ≥0.3g) — anti-inflammatory, supports mood regulation",
    "Fiber: 8g (target ≥8g) — gut-brain axis support",
    "Added Sugar: 5g (target ≤10g) — avoids blood sugar spikes"
]
```

---

### **Step 8: Rank All Recipes**
*[routes.py]*

```python
# Score top 10 recipes from Edamam
scored_recipes = []
for recipe in edamam_results[:10]:
    nutrients = extract_nutrients(recipe)
    canonical = canonicalize_nutrients(nutrients)
    score, reasons, contributions = score_recipe(canonical, ["stressed"])
    
    scored_recipes.append({
        "recipe": recipe,
        "score": score,
        "reasons": reasons
    })

# Sort by score (highest first)
scored_recipes.sort(key=lambda x: x["score"], reverse=True)

best_recipe = scored_recipes[0]  # Score: 1.1225 (112%)
```

---

### **Step 9: Generate Emotional Rationale**
*[OpenRouterClient.generate_emotional_rationale()]*

**Prompt to AI**:
```
Create an emotional rationale for why this recipe matches the user's mood.

Recipe: Baked Salmon with Spinach and Quinoa
Ingredients: salmon, spinach, quinoa, olive oil, garlic, lemon

User's Mood: Stressed (very)
Desired Nutrients: Magnesium, Omega-3, Fiber
Interpretation: Seeking to calm nervous system and reduce stress

Please provide:
1. Overall rationale (2-3 sentences)
2. Mood breakdown explaining how specific elements support their stressed state
3. Plating suggestion
4. Journaling prompt
```

**AI Response**:
```
OVERALL_RATIONALE:
This dish was chosen to gently ease your stressed state with nutrient-dense ingredients that support your nervous system. The salmon provides omega-3 fatty acids that help reduce inflammation and support mood regulation, while the magnesium-rich spinach and quinoa work to calm your body's stress response.

MOOD_BREAKDOWNS:
Stressed: The omega-3s in salmon act as natural anti-inflammatories, helping to counter the physical effects of stress on your body. Magnesium from spinach and quinoa helps regulate your nervous system, promoting a sense of calm.

PLATING_SUGGESTION:
Arrange the salmon fillet atop a bed of fluffy quinoa, nestle the wilted spinach alongside, and finish with a bright squeeze of lemon. The vibrant greens and golden fish create a visually calming plate.

JOURNALING_PROMPT:
As you eat this meal, what are three things that felt overwhelming today, and how might you approach them differently tomorrow?
```

---

### **Step 10: Build Final Response**

**Nutrition Comparison**:
```python
nutrition_comparison = {
    "recipe_calories": 585,
    "target_calories": 2131,
    "percentage_of_daily": round((585 / 2131) * 100, 1),  # 27.4%
    
    "recipe_protein": 34,
    "target_protein": 72,
    "percentage_of_daily_protein": round((34 / 72) * 100, 1),  # 47.2%
    
    "recipe_fiber": 8,
    "target_fiber": 25,
    "percentage_of_daily_fiber": round((8 / 25) * 100, 1)  # 32%
}
```

**Final JSON Response**:
```json
{
  "recipe": {
    "name": "Baked Salmon with Spinach and Quinoa",
    "image_url": "https://...",
    "ingredients": [
      {"name": "salmon fillet", "amount": "6 oz"},
      {"name": "fresh spinach", "amount": "2 cups"},
      {"name": "quinoa", "amount": "1 cup cooked"},
      {"name": "olive oil", "amount": "1 tbsp"},
      {"name": "garlic", "amount": "2 cloves"},
      {"name": "lemon", "amount": "1/2"}
    ],
    "cooking_directions": [
      "Preheat oven to 400°F",
      "Season salmon with salt, pepper, garlic",
      "Bake salmon for 12-15 minutes",
      "Sauté spinach in olive oil until wilted",
      "Serve salmon over quinoa with spinach, squeeze lemon"
    ],
    "nutrition": {
      "calories": 585,
      "protein_g": 34,
      "fiber_g": 8,
      "carbs_g": 45,
      "fat_g": 22
    },
    "prep_time": 10,
    "cook_time": 15,
    "servings": 1
  },
  
  "emotional_rationale": {
    "overall_rationale": "This dish was chosen to gently ease your stressed state with nutrient-dense ingredients...",
    "mood_breakdowns": [
      {
        "mood": "stressed",
        "explanation": "The omega-3s in salmon act as natural anti-inflammatories..."
      }
    ],
    "plating_suggestion": "Arrange the salmon fillet atop a bed of fluffy quinoa...",
    "journaling_prompt": "As you eat this meal, what are three things that felt overwhelming today..."
  },
  
  "flavor_alignment": {
    "nutrient_match_score": 112.3,  // Percentage
    "nutrient_reasons": [
      "Magnesium: 140mg (target ≥120mg) — supports nervous system",
      "Omega-3: 0.5g (target ≥0.3g) — anti-inflammatory",
      "Fiber: 8g (target ≥8g) — gut-brain axis support"
    ],
    "evidence_based": true
  },
  
  "nutrition_comparison": {
    "recipe_calories": 585,
    "target_calories": 2131,
    "percentage_of_daily_calories": 27.4,
    "recipe_protein": 34,
    "target_protein": 72,
    "percentage_of_daily_protein": 47.2
  },
  
  "evidence": {
    "level": "Moderate - Mixed but trending positive",
    "key_studies": [
      "Magnesium and anxiety meta-analyses (PMC)",
      "Omega-3 for anxiety (Cochrane reviews)"
    ],
    "explainers": [
      "Magnesium-rich foods are linked to calmer mood in several studies.",
      "Omega-3 fatty acids show mixed but trending positive results for anxiety."
    ],
    "disclaimer": "This app provides food suggestions based on mood and nutritional science. It is not a substitute for professional medical advice..."
  }
}
```

---

## 📊 Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. USER INPUT                                               │
│    Mood: Stressed (very)                                    │
│    Profile: Female, 32, 165cm, 60kg                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. MOOD → NUTRIENT TARGETS (mood_mapping.json)             │
│    Magnesium: ≥120mg (weight: 1.0)                         │
│    Omega-3: ≥0.3g (weight: 0.9)                            │
│    Fiber: ≥8g (weight: 0.7)                                │
│    Sugar: ≤10g (weight: 0.6)                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. CALCULATE DAILY NUTRITION NEEDS                          │
│    TDEE: 2,131 kcal/day                                    │
│    Protein: 72g/day                                        │
│    Fiber: 25g/day                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. BUILD RECIPE SEARCH (Edamam API)                        │
│    Query: "salmon spinach"                                  │
│    Calories: 500-700                                       │
│    Cuisine: Mediterranean, Asian                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. GET RECIPES FROM EDAMAM                                  │
│    10 recipes returned with full nutrient data              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. EXTRACT & CANONICALIZE NUTRIENTS                        │
│    Recipe A: Mg=140mg, Omega-3=0.5g, Fiber=8g             │
│    Recipe B: Mg=95mg, Omega-3=0.2g, Fiber=9g              │
│    Recipe C: Mg=130mg, Omega-3=0.4g, Fiber=7g             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. SCORE EACH RECIPE                                        │
│    Recipe A: Score = 1.12 (112%) ← BEST                    │
│    Recipe B: Score = 0.85 (85%)                            │
│    Recipe C: Score = 1.08 (108%)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. GENERATE EMOTIONAL RATIONALE (OpenRouter AI)            │
│    Why this dish matches your stressed state...             │
│    Plating suggestions, journaling prompts                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. RETURN COMPLETE RECOMMENDATION                           │
│    Recipe + Nutrition + Rationale + Evidence + Score        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Key Decision Points

### Why This Recipe Won

**Recipe A (Baked Salmon with Spinach)**: Score 112%
- ✅ **Magnesium**: 140mg (exceeds 120mg target by 17%)
- ✅ **Omega-3**: 0.5g (exceeds 0.3g target by 67%)
- ✅ **Fiber**: 8g (meets target exactly)
- ✅ **Sugar**: 5g (well below 10g limit)

**Recipe B (Chicken Salad)**: Score 85%
- ⚠️ **Magnesium**: 95mg (below 120mg target)
- ⚠️ **Omega-3**: 0.2g (below 0.3g target)
- ✅ **Fiber**: 9g (exceeds target)
- ✅ **Sugar**: 4g (well below limit)

Recipe A wins because it **exceeds all critical targets** (magnesium and omega-3) which have the highest importance weights for stress.

---

## 💡 Multi-Mood Example

What if user selects **2 moods**?

```json
{
  "moods": [
    {"mood": "stressed", "intensity": "very"},
    {"mood": "fatigued", "intensity": "medium"}
  ]
}
```

**Mood Aggregation**:
```python
# Stressed (very = 1.0) targets:
- Magnesium: ≥120mg (weight: 1.0)
- Omega-3: ≥0.3g (weight: 0.9)

# Fatigued (medium = 0.6) targets (scaled):
- Iron: ≥6mg × 0.6 = ≥3.6mg (weight: 1.0)
- Vitamin C: ≥30mg × 0.6 = ≥18mg (weight: 0.8)
- Complex carbs: ≥30g × 0.6 = ≥18g (weight: 0.8)

# COMBINED targets:
- Magnesium: ≥120mg (weight: 1.0) 
- Omega-3: ≥0.3g (weight: 0.9)
- Iron: ≥3.6mg (weight: 0.6)  // Scaled by intensity
- Vitamin C: ≥18mg (weight: 0.48)  // Scaled
- Complex carbs: ≥18g (weight: 0.48)  // Scaled
```

Now the system searches for recipes that meet **both** stress relief AND energy needs!

---

## 🎯 Summary: The Magic

1. **Mood** → Looked up in `mood_mapping.json`
2. **Nutrient Targets** → Scientific requirements (mg, grams)
3. **Recipe Search** → Edamam finds matching recipes
4. **Nutrient Extraction** → Parse API response per serving
5. **Scoring** → Math: How well does recipe match targets?
6. **Ranking** → Pick best match
7. **AI Explanation** → Make it human and poetic
8. **Evidence** → Show the science behind it

**Result**: User gets a recipe that's **scientifically optimized** for their emotional state, but explained in a **warm, human way**.

---

This is the power of combining **nutritional science** (magnesium for stress) with **emotional intelligence** (understanding what "stressed" means) and **AI storytelling** (making it relatable). 🎉

