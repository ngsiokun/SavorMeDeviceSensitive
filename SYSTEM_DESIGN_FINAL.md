# SavorMe Backend - Final System Design

## ✅ Approved Design (October 2025)

### **Core Architecture**

**Evidence-Based, Two-Phase Personalization System**

---

## 📊 Phase 1: MVP (Current Implementation)

### **1. Mood System**
- ✅ **4 Evidence-Based Moods** (not 12)
  - Stressed/Anxious (⭐⭐⭐ Moderate evidence)
  - Fatigued/Low Energy (⭐⭐⭐⭐ Strong evidence)
  - Low Mood/Blue (⭐⭐⭐⭐⭐ Strongest - SMILES trial)
  - Irritable/Angry (⭐⭐⭐ Moderate evidence)

- ✅ **User Selection**: 1-3 moods (not 4)
- ✅ **Intensity Levels**: "a little", "medium", "very"

### **2. Personalization Level**

#### **Fully Personalized** ✅
- **Daily Calorie Target**: Harris-Benedict equation (age, gender, height, weight)
- **Daily Protein Target**: Body weight × activity level
- **Daily Fiber Target**: Gender-based (male: 38g, female: 25g)
- **Recipe Portion Sizes**: Scaled to user's calorie needs

#### **Fixed Targets (Not Personalized)** ⚠️
- **Mood-Specific Nutrients**: Same for everyone
  - Magnesium: 120mg per meal (stressed)
  - Iron: 6mg per meal (fatigued)
  - Omega-3: 0.3g per meal (stressed/low mood)
  - Vitamin C: 30mg per meal (fatigued)

**Rationale**: 
- Research-based absolute dosages
- Simpler to implement and explain
- Conservative and safe
- Matches peer-reviewed study dosages

### **3. API Configuration**

#### **Recipe Search**
- ✅ **Edamam Recipe Search API v2** (Minimum Service - Free)
  - `app_id`: f96cea5d
  - `app_key`: afb66c232e1090ece34618db1acc1136
  - Endpoint: `https://api.edamam.com/api/recipes/v2`

#### **Nutrition Calculation**
- ✅ **Built-in Harris-Benedict Formulas** (No API needed)
  - Free, instant, scientifically validated
  - No rate limits or external dependencies

#### **Optional APIs**
- OpenRouter AI: Emotional rationale generation (optional)
- USDA FDC: Nutrient fallback (optional)
- Hugging Face: Image generation (optional)

### **4. Decision Flow**

```
User Input (Mood + Profile)
    ↓
Calculate Personal Daily Targets (age, gender, height, weight)
    ↓
Load Mood Nutrient Targets (fixed from JSON)
    ↓
Search Recipes (Edamam) - filtered by BOTH
    ↓
Score Recipes (Math-based nutrient matching)
    ↓
Select Best Recipe
    ↓
Generate Explanation (Optional: OpenRouter AI)
    ↓
Return Complete Recommendation
```

---

## 🚀 Phase 2: Future Enhancements (Not MVP)

### **Planned Improvements**

#### **1. Smart Nutrient Personalization**
```python
# Scale mood nutrients by body weight
magnesium_target = 120mg × (user_weight / 60kg)

# Gender multipliers
if male:
    magnesium_target × 1.3

# Age adjustments
if female and age >= 50:
    iron_target × 0.7  # Post-menopausal need less
```

#### **2. User Feedback Loop**
- Track which recipes users complete
- Adjust nutrient weights based on satisfaction
- Personalized mood-food preferences

#### **3. Advanced Features**
- Multi-day meal planning
- Grocery list generation
- Seasonal ingredient adjustments
- Restaurant recommendations

---

## 📋 Data Sources

### **Mapping Data**
- ✅ **File**: `app/data/mood_mapping.json`
- ✅ **Source**: Manual curation from scientific literature
- ✅ **Evidence**: 
  - SMILES trial (2017)
  - Cochrane reviews
  - WHO/NIH guidelines
  - PMC meta-analyses

### **Nutrition Formulas**
- ✅ Harris-Benedict Equation (1919, revised 1984)
- ✅ WHO dietary guidelines
- ✅ American College of Sports Medicine activity multipliers

---

## 🎯 Key Design Decisions

### **Decision 1: 4 Moods (Not 12)**
**Reason**: Focus on moods with strong scientific evidence only
- Removed: dreamy, focused, playful, craving, light, grounded, restorative, charismatic
- Kept: Only evidence-based moods with RCT or meta-analysis support

### **Decision 2: Fixed Mood Nutrient Targets**
**Reason**: Match research dosages, simpler MVP
- Phase 1: Use research-based fixed targets
- Phase 2: Add body weight/gender scaling

### **Decision 3: Built-in Nutrition Calculation**
**Reason**: No need for API
- Free, instant, accurate
- Scientifically validated formulas
- No external dependencies

### **Decision 4: Edamam Recipe Search (Not Other APIs)**
**Reason**: Best fit for our needs
- Not using: Nutrition Analysis, Food Database, Meal Planner APIs
- Using: Recipe Search API only

### **Decision 5: Science Picks Recipe, AI Explains It**
**Reason**: Trustworthy recommendations
- Backend uses math/science for selection
- LLM only for human-friendly explanations
- Not relying on AI for medical decisions

---

## 📊 Personalization Matrix

| Factor | Affects | Personalized? | Method |
|--------|---------|---------------|--------|
| **Age** | BMR, Calories | ✅ Yes | Harris-Benedict formula |
| **Gender** | BMR, Calories, Fiber | ✅ Yes | Harris-Benedict + WHO |
| **Height** | BMR, Calories | ✅ Yes | Harris-Benedict formula |
| **Weight** | BMR, Calories, Protein | ✅ Yes | Harris-Benedict + 1.2g/kg |
| **Activity Level** | TDEE, Protein | ✅ Yes | Activity multipliers |
| **Cuisine Preference** | Recipe pool | ✅ Yes | Edamam cuisineType filter |
| **Allergies** | Recipe filtering | ✅ Yes | Edamam health labels |
| **Dietary Preference** | Recipe filtering | ✅ Yes | Edamam diet labels |
| **Mood** | Recipe selection | ✅ Yes | Nutrient scoring algorithm |
| **Body Weight** | Mood nutrients | ❌ Phase 2 | Future enhancement |
| **Age** | Mood nutrients | ❌ Phase 2 | Future enhancement |
| **Gender** | Mood nutrients | ❌ Phase 2 | Future enhancement |

---

## 🔬 Evidence Levels

### **Mood Evidence Quality**

| Mood | Evidence Level | Key Studies |
|------|----------------|-------------|
| **Low Mood** | ⭐⭐⭐⭐⭐ Strong | SMILES trial (RCT), Multiple meta-analyses |
| **Fatigued** | ⭐⭐⭐⭐ Strong | Iron-fatigue link well-established (WHO/NIH) |
| **Stressed** | ⭐⭐⭐ Moderate | Magnesium/omega-3 meta-analyses (mixed) |
| **Irritable** | ⭐⭐⭐ Moderate | Glycemic stability research (observational) |

---

## 🎯 Success Metrics (MVP)

### **Technical**
- [ ] API response time < 2 seconds
- [ ] Recipe match rate > 80%
- [ ] Nutrient extraction accuracy > 90%

### **User Experience**
- [ ] User satisfaction > 4.0/5.0
- [ ] Recipe completion rate > 60%
- [ ] Weekly active retention > 40%

### **Business**
- [ ] 100+ active users in first month
- [ ] 3+ sessions per week average
- [ ] Positive user feedback on evidence-based approach

---

## 📝 Implementation Status

### **✅ Completed**
- [x] 4-mood evidence-based system
- [x] mood_mapping.json with scientific citations
- [x] Harris-Benedict nutrition calculator
- [x] Edamam API integration
- [x] MoodNutritionEngine with scoring algorithm
- [x] FastAPI backend structure
- [x] Nutrient canonicalization
- [x] Medical disclaimers
- [x] API credentials configured (.env)
- [x] Complete documentation

### **🚧 Ready for Testing**
- [ ] Start backend server
- [ ] Test API with real requests
- [ ] Validate nutrient scoring
- [ ] Test with 20+ real recipes

### **📅 Phase 2 (Future)**
- [ ] Body weight-based nutrient scaling
- [ ] Gender-specific nutrient adjustments
- [ ] Age-based nutrient adjustments
- [ ] User feedback collection
- [ ] A/B testing framework
- [ ] Machine learning personalization

---

## 🎊 Final System Architecture

```
┌─────────────────────────────────────────────────────────┐
│ FRONTEND (iOS - To Be Built)                            │
│ - Mood selection (4 moods, 1-3 selection)              │
│ - Personal profile input                                │
│ - Recipe display with evidence                          │
└────────────────────────┬────────────────────────────────┘
                         │ REST API
                         ▼
┌─────────────────────────────────────────────────────────┐
│ BACKEND (Python FastAPI) ✅ COMPLETE                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Personal Profile → Nutrition Calculator          │  │
│  │ (age, gender, height, weight)                    │  │
│  │ → Daily Targets (calories, protein, fiber)       │  │
│  └──────────────────────────────────────────────────┘  │
│                          +                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Mood Selection → mood_mapping.json               │  │
│  │ (1-3 moods, intensity)                           │  │
│  │ → Nutrient Targets (Mg, Fe, Omega-3, etc.)      │  │
│  └──────────────────────────────────────────────────┘  │
│                          ↓                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Recipe Search (Edamam API)                       │  │
│  │ → Filters: cuisine, diet, health, nutrition      │  │
│  └──────────────────────────────────────────────────┘  │
│                          ↓                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Nutrient Scoring (Math Algorithm)                │  │
│  │ → Score each recipe against targets              │  │
│  │ → Rank by best match                             │  │
│  └──────────────────────────────────────────────────┘  │
│                          ↓                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │ AI Explanation (Optional: OpenRouter)            │  │
│  │ → Generate emotional rationale                   │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ OUTPUT                                                   │
│ - Recipe with complete nutrition                        │
│ - Evidence-based explanation                            │
│ - Nutrient match score                                  │
│ - Scientific references                                 │
└─────────────────────────────────────────────────────────┘
```

---

## 📚 Documentation

All documentation is available in the repository:

1. **QUICK_START_GUIDE.md** - How to run the backend
2. **MAPPING_STRATEGY.md** - Complete technical architecture
3. **MAPPING_DATA_SOURCES.md** - Where the data comes from
4. **EVIDENCE_BASED_MOODS_v2.md** - Why 4 moods, evidence levels
5. **MOOD_TO_RECIPE_FLOW.md** - End-to-end example walkthrough
6. **IMPLEMENTATION_ROADMAP.md** - Status, next steps, testing plan
7. **SYSTEM_DESIGN_FINAL.md** - This document

---

## 🎯 Key Takeaway

**SavorMe Backend combines:**
- ✅ **Scientific rigor** (evidence-based nutrient targets)
- ✅ **Personalization** (age, gender, height, weight)
- ✅ **Simplicity** (fixed mood targets for MVP)
- ✅ **Transparency** (show evidence, cite studies)
- ✅ **Safety** (conservative targets, disclaimers)

**Result**: A trustworthy, scientifically-grounded mood-to-recipe recommendation system that's ready for testing and user validation! 🎊

---

**Version**: 2.0.0  
**Date**: October 1, 2025  
**Status**: MVP Complete - Ready for Testing  
**GitHub**: https://github.com/ngsiokun/SavorMe-backend

