# SavorMe Backend - Quick Start Guide

## What You Have Now

A **fully functional, evidence-based backend** that maps user moods to scientifically-backed nutrient targets and recommends recipes accordingly.

---

## 📋 Key Documents

### 1. **MAPPING_STRATEGY.md** ← **READ THIS FIRST**
Complete technical plan for the mood → nutrient → recipe mapping:
- Scientific foundation (SMILES trial, omega-3 studies, etc.)
- Three-tier architecture
- Scoring algorithm details
- Edge case handling
- Testing strategy

### 2. **IMPLEMENTATION_ROADMAP.md**
Current status and next steps:
- ✅ What's completed
- 🚧 What's remaining
- Priority levels
- Risk assessment
- Success criteria

### 3. **README.md**
Standard repository documentation:
- Installation instructions
- API documentation
- Configuration guide

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
cd SavorMe-backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
cp .env.example .env
# Edit .env with your API keys
```

Required keys:
- `EDAMAM_APP_ID` and `EDAMAM_APP_KEY` (get from https://developer.edamam.com/)
- Optional: `OPENROUTER_API_KEY`, `USDA_API_KEY`

### 3. Run the Server
```bash
uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`

### 4. Test the API
Visit: `http://localhost:8000/docs` for interactive API documentation

---

## 🧪 Test the Evidence-Based System

### Quick Test Request

```bash
curl -X POST "http://localhost:8000/api/v1/recipes/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "mood_blend": {
      "moods": [
        {"mood": "stress", "intensity": "very"},
        {"mood": "fatigue", "intensity": "medium"}
      ]
    },
    "user_profile": {
      "age": 30,
      "gender": "female",
      "height_cm": 165,
      "weight_kg": 60,
      "cuisine_preferences": ["Mediterranean", "Asian"],
      "food_allergies": [],
      "dietary_preference": "none"
    }
  }'
```

### Expected Response

```json
{
  "recipe": {
    "name": "Salmon with Spinach and Quinoa",
    "nutrition": {
      "calories": 520,
      "protein_g": 28,
      "fiber_g": 9,
      ...
    }
  },
  "flavor_alignment": {
    "nutrient_match_score": 87.5,
    "nutrient_reasons": [
      "Magnesium: 135mg (target ≥120mg) — supports stress response",
      "Iron: 4.5mg (target ≥3.6mg) — combats fatigue",
      "Omega-3: 0.45g (target ≥0.25g) — anti-inflammatory"
    ],
    "evidence_based": true
  },
  ...
}
```

---

## 🎯 How the System Works

### Step 1: User Selects Moods
```
User picks: "Stress (very)" + "Fatigue (medium)"
```

### Step 2: System Maps to Nutrient Targets
```
Stress → Magnesium (120mg+), Omega-3 (0.25g+), Fiber (8g+)
Fatigue → Iron (6mg+), Vitamin C (30mg+), Complex carbs (25g+)

Combined targets (weighted by intensity):
- Magnesium: ≥120mg (weight: 0.9)
- Iron: ≥3.6mg (weight: 0.6)  
- Omega-3: ≥0.25g (weight: 0.6)
- Fiber: ≥8g (weight: 0.65)
- Vitamin C: ≥18mg (weight: 0.36)
```

### Step 3: Searches & Scores Recipes
```
1. Search Edamam for Mediterranean recipes with fish/greens
2. Extract nutrients from each recipe
3. Score each recipe against targets
4. Rank by nutrient match score
```

### Step 4: Returns Best Match
```
Top recipe: Salmon with Spinach (87.5% match)
Why: High magnesium, good iron, excellent omega-3
Evidence: "Magnesium and omega-3 show positive results for stress in meta-analyses"
```

---

## 📊 Key Endpoints

### 1. Main Recommendation
`POST /api/v1/recipes/recommend`
- Input: Mood blend + user profile
- Output: Best recipe with nutrient scoring

### 2. Nutrient Scoring
`POST /api/v1/nutrition/score-recipe`
- Input: Recipe nutrients + mood IDs
- Output: Score and explanations

### 3. Mood Targets
`GET /api/v1/nutrition/mood-targets/{mood_id}`
- Input: Mood ID (e.g., "stress")
- Output: Scientific nutrient targets with evidence

### 4. Health Check
`GET /api/v1/health`
- Output: System status, available moods

---

## 🔬 Scientific Evidence

### Strong Evidence
- **Mediterranean Diet → Mood**: SMILES trial showed depression improvement
- **Iron → Fatigue**: Well-established link even without anemia
- **Protein/Fiber → Blood Sugar**: Reduces mood-disrupting swings

### Mixed/Positive Evidence
- **Magnesium → Stress**: Meta-analyses show trending positive results
- **Omega-3 → Anxiety**: Variable results, small benefits observed

### Pattern-Based (Weaker Evidence)
- **Colorful plants → Playful mood**: Pattern-based, lacks direct RCTs
- **Nutrient density → Charisma**: Theoretical, not clinically tested

All recommendations include appropriate disclaimers based on evidence strength.

---

## ⚠️ Important Notes

### Medical Disclaimers
- **Always shown**: "Not a substitute for medical advice"
- **Contraindications checked**: Iron avoided if hemochromatosis
- **Conservative claims**: "May help" not "Will cure"

### Data Quality
- **Edamam**: Good for calories, protein, fiber, basic vitamins
- **FDC fallback**: Better micronutrient data when needed
- **Missing data**: Polyphenols often estimated or omitted

### Performance
- **Target**: <2 seconds per recommendation
- **Rate limits**: Edamam free tier = 10 requests/min
- **Caching**: Not yet implemented (add Redis)

---

## 🐛 Known Issues & Limitations

### Current Gaps
1. **No polyphenol data**: Edamam doesn't provide, needs estimation
2. **Added sugar tracking**: Often null in Edamam, using total sugars
3. **No automated tests**: Needs comprehensive test suite
4. **No caching**: Every request hits external APIs

See `IMPLEMENTATION_ROADMAP.md` for complete list and solutions.

---

## 📝 Next Steps (Priority Order)

### Immediate (This Week)
1. ✅ **Test manually** with 20 real recipes
2. 📝 **Write unit tests** for MoodNutritionEngine
3. 🔧 **Fix critical bugs** discovered during testing

### Short-term (Next 2 Weeks)
4. 🧪 **Build test suite** (80%+ coverage)
5. 💾 **Add caching layer** (Redis)
6. 📊 **Validate data quality** (nutrient extraction accuracy)

### Medium-term (Next Month)
7. 🚀 **Deploy to staging**
8. 👥 **User testing** (10-20 beta users)
9. 📈 **A/B test** evidence-based vs emotional-only

---

## 🎓 Learning Resources

### Understanding the Mapping
1. Read `MAPPING_STRATEGY.md` sections 1-3 for architecture
2. Review `app/data/mood_mapping.json` for actual targets
3. Study `app/services/mood_nutrition_engine.py` for scoring logic

### Scientific Background
- **SMILES Trial**: Mediterranean diet for depression
- **Iron & Fatigue**: Office of Dietary Supplements resources
- **Magnesium & Stress**: PMC meta-analyses
- **Omega-3 & Mood**: Cochrane reviews

Links in `MAPPING_STRATEGY.md` Section 2.

---

## 🤝 Contributing

### Code Structure
```
app/
├── api/routes.py          # API endpoints
├── services/
│   ├── mood_nutrition_engine.py  # ⭐ Core scoring logic
│   ├── edamam_client.py          # Recipe search
│   ├── fdc_client.py             # USDA nutrients
│   └── fusion_engine.py          # Legacy emotional mapping
├── models/                # Pydantic data models
└── data/
    └── mood_mapping.json  # ⭐ Evidence-based targets
```

### Making Changes
1. Update `mood_mapping.json` for new moods or nutrient targets
2. Modify `MoodNutritionEngine.score_recipe()` for algorithm changes
3. Add tests in `app/tests/`
4. Update documentation

---

## 📞 Support

- **Documentation**: Check this guide + `MAPPING_STRATEGY.md`
- **API Issues**: Check `/docs` endpoint for API specs
- **GitHub**: https://github.com/ngsiokun/SavorMe-backend

---

## ✅ Quick Validation Checklist

Test that everything works:

- [ ] Server starts without errors
- [ ] `/api/v1/health` returns available moods
- [ ] `/api/v1/nutrition/mood-targets/stress` returns scientific targets
- [ ] Recipe recommendation works with Edamam API key
- [ ] Nutrient match score appears in response
- [ ] Evidence-based explainers are included

---

**Congratulations!** 🎉 You now have an evidence-based, scientifically-grounded mood-to-recipe recommendation system.

The key innovation: **Emotional resonance (dreamy, grounded) + Nutritional science (magnesium for stress, iron for fatigue) = Truly personalized recommendations**

Start with the MAPPING_STRATEGY.md to understand the full system architecture!

