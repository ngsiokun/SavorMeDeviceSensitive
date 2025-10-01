# Evidence-Based Mood-to-Nutrient-to-Recipe Mapping Strategy

## Overview
This document outlines the complete strategy for mapping user moods → nutrient targets → food recipes using evidence-based nutritional science.

---

## 1. Three-Tier Mapping Architecture

```
USER MOOD → NUTRIENT TARGETS → RECIPE SCORING → FINAL RECOMMENDATION
   (10 moods)   (Scientific)      (Algorithmic)      (Personalized)
```

### Tier 1: Mood → Nutrient Targets (Evidence-Based)
**Input**: User selects 1-3 moods with intensity (a little, medium, very)  
**Output**: Prioritized nutrient targets with min/max values per meal

### Tier 2: Nutrient Targets → Recipe Scoring
**Input**: Recipe nutrient data (from Edamam or FDC)  
**Output**: Numerical score (0-1.25) indicating mood-nutrient fit

### Tier 3: Recipe Scoring → Final Recommendation
**Input**: Top-scoring recipes + user preferences  
**Output**: Best-matched recipe with explanations

---

## 2. Scientific Foundation

### A. Mediterranean Diet Pattern (Baseline for All Moods)
**Evidence**: SMILES trial, meta-analyses  
**Application**: All moods start with Mediterranean base, then add specific nutrient targets

**Core Pattern**:
- ✅ Emphasize: vegetables, fruits, legumes, nuts, whole grains, olive oil, fish
- ❌ Limit: ultra-processed foods, refined sugars

### B. Mood-Specific Nutrient Science

| Mood State | Primary Issue | Key Nutrients | Evidence Level | Citations |
|------------|---------------|---------------|----------------|-----------|
| **Anger/Irritability** | Blood sugar swings, inflammation | Protein (20g+), Fiber (8g+), Low sugar (<10g), Omega-3 (0.25g) | Moderate | Ultra-processed ↔ mood swings |
| **Moodiness/Low** | Serotonin, gut health, inflammation | Fiber (10g+), Omega-3 (0.3g), Polyphenols (0.5g) | Strong | SMILES trial, Mediterranean diet RCTs |
| **Fatigue/Brain fog** | Iron deficiency, energy metabolism | Iron (6mg+), Vitamin C (30mg+), Complex carbs (25g+), Fiber (8g+) | Strong | Iron deficiency ↔ fatigue (even without anemia) |
| **Stress/Anxiety** | Cortisol, nervous system | Magnesium (120mg+), Omega-3 (0.25g), Fiber (8g+), Low caffeine | Mixed/Positive | Magnesium & omega-3 meta-analyses |
| **Dreamy** | Cognitive clarity, calm | Fiber (8g+), Omega-3 (0.2g), Polyphenols (0.3g) | Moderate | Mediterranean pattern |
| **Focused** | Sustained energy, mental performance | Protein (25g+), Iron (4mg+), Vitamin C (25mg+), Fiber (6g+) | Moderate | Glycemic stability, iron ↔ cognition |
| **Playful** | Energy, variety | Fiber (7g+), Vitamin C (40mg+), Colorful plants | Weak | Pattern-based |
| **Craving** | Satiety, prevent overeating | Protein (18g+), Fiber (6g+), Low added sugar (<15g) | Moderate | Protein/fiber ↔ satiety |
| **Light** | Fresh, low-calorie density | Fiber (9g+), Vitamin C (50mg+), Very low sugar (<8g) | Weak | Pattern-based |
| **Grounded** | Stability, calm energy | Fiber (10g+), Protein (20g+), Magnesium (100mg+) | Moderate | Whole foods, magnesium |
| **Restorative** | Healing, anti-inflammation | Protein (18g+), Fiber (8g+), Magnesium (110mg+), Omega-3 (0.2g) | Moderate | Anti-inflammatory diet |
| **Charismatic** | Energy, vitality | Protein (22g+), Iron (5mg+), Vitamin C (35mg+) | Weak | Nutrient density |

### C. Important Caveats
1. **Mixed Evidence**: Omega-3 and magnesium have "trending positive" but variable results
2. **Food-First**: Always prefer whole foods over supplements
3. **Individual Variation**: Effects vary by person, baseline status
4. **Pattern > Individual Nutrients**: Mediterranean pattern is stronger evidence than isolated nutrients

---

## 3. Mapping Implementation Strategy

### Phase 1: Mood Selection & Intensity Weighting

```python
# User selects moods
moods = [
    ("stress", "very"),      # weight = 1.0
    ("fatigue", "medium"),   # weight = 0.6
    ("grounded", "a_little") # weight = 0.3
]

# Intensity multipliers
INTENSITY_WEIGHTS = {
    "a_little": 0.3,
    "medium": 0.6,
    "very": 1.0
}
```

### Phase 2: Nutrient Target Aggregation

**Strategy**: When multiple moods are selected, combine their nutrient targets intelligently

```python
# For minimums: Take MAX (most restrictive)
iron_target = max(
    fatigue.iron_min * 0.6,    # 6mg * 0.6 = 3.6mg
    grounded.iron_min * 0.3     # 0mg * 0.3 = 0mg
) = 3.6mg

# For maximums: Take MIN (most restrictive)
sugar_target = min(
    stress.sugar_max * 1.0,     # 10g
    fatigue.sugar_max * 0.6     # No limit
) = 10g

# For weights: Average and cap at 1.0
nutrient_importance = min(1.0, 
    (stress.protein_weight + fatigue.protein_weight) / 2
)
```

### Phase 3: Recipe Nutrient Extraction

**Two Data Sources**:

#### A. Edamam Recipe API (Primary)
```
Edamam Nutrient Codes → Canonical Names
ENERC_KCAL → calories
PROCNT → protein
FIBTG → fiber
FE → iron
MG → magnesium
VITC → vitamin_c
SUGAR.added → added_sugar
EPA + DHA → omega_3_epa_dha
```

#### B. USDA FoodData Central (Supplementary)
- Use when Edamam data is incomplete
- Use for ingredient-level nutrient lookup
- More detailed micronutrient data

**Canonicalization Process**:
```python
# Raw from Edamam
raw = {
    "PROCNT": 27.5,
    "FIBTG": 9.2,
    "Iron, Fe": 7.8
}

# Canonicalize using aliases
canonical = {
    "protein": 27.5,
    "fiber": 9.2,
    "iron": 7.8
}
```

### Phase 4: Recipe Scoring Algorithm

**Formula**:
```
For each nutrient target:
  1. Calculate contribution (0 to 1.25)
  2. Multiply by nutrient weight (importance)
  3. Sum all weighted contributions
  4. Normalize by total weight

Final Score = Σ(contribution × weight) / Σ(weight)
```

**Contribution Calculation**:

```python
if min_target and max_target:  # Range target (e.g., 20-30g protein)
    if min ≤ value ≤ max:
        # Reward being in range, bonus for being centered
        mid = (min + max) / 2
        closeness = 1.0 - |value - mid| / mid
        contribution = 0.75 + 0.5 × closeness  # 0.75 to 1.25
    elif value > max:
        contribution = 0.6  # Mild penalty
    else:
        contribution = min(1.25, value / min)

elif min_target only:  # Minimum target (e.g., ≥8g fiber)
    contribution = min(1.25, value / min)

elif max_target only:  # Maximum target (e.g., ≤10g added sugar)
    if value ≤ max:
        contribution = 1.0
    else:
        contribution = max(0.3, max / value)  # Penalty
```

**Example**:
```
Mood: Stress (very)
Targets:
  - Magnesium: ≥120mg, weight=0.9
  - Omega-3: ≥0.25g, weight=0.6
  - Fiber: ≥8g, weight=0.5

Recipe A:
  - Magnesium: 135mg → contribution = 1.125 (exceeds by 12.5%)
  - Omega-3: 0.35g → contribution = 1.25 (exceeds by 40%, capped)
  - Fiber: 9.5g → contribution = 1.187

Score = (1.125×0.9 + 1.25×0.6 + 1.187×0.5) / (0.9+0.6+0.5)
      = (1.0125 + 0.75 + 0.5935) / 2.0
      = 1.178 / 2.0
      = 0.589 (58.9%)
```

### Phase 5: Ranking & Selection

**Multi-Factor Ranking**:
```python
final_score = (
    nutrient_score × 0.6 +           # 60% weight
    pattern_bonus × 0.2 +             # 20% weight
    preference_match × 0.1 +          # 10% weight
    novelty_factor × 0.1              # 10% weight
) - penalties
```

**Pattern Bonus**:
- Mediterranean compliance: +0.1
- Low ultra-processed: +0.05
- Glycemic stability: +0.05

**Penalties**:
- Allergens present: -1.0 (exclude)
- Exceeds contraindication: -0.5
- High caffeine for stress: -0.2

---

## 4. Data Flow Pipeline

```
┌─────────────────┐
│ USER INPUT      │
│ - 1-3 moods     │
│ - Intensities   │
│ - Profile       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ MOOD FUSION     │
│ - Load targets  │
│ - Aggregate     │
│ - Weight        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ RECIPE SEARCH   │
│ - Edamam query  │
│ - Filters       │
│ - Get 10-20     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ NUTRIENT EXTRACT│
│ - Parse Edamam  │
│ - Canonicalize  │
│ - Per serving   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ SCORING ENGINE  │
│ - Score each    │
│ - Rank all      │
│ - Select best   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ EXPLANATION GEN │
│ - Why this fits │
│ - Nutrient match│
│ - Evidence      │
│ - Disclaimers   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ FINAL OUTPUT    │
│ - Recipe        │
│ - Rationale     │
│ - Score         │
│ - Safety notes  │
└─────────────────┘
```

---

## 5. Edge Cases & Handling

### A. Conflicting Nutrient Targets
**Scenario**: User selects "craving" (allows indulgence) + "focused" (strict glycemia)

**Resolution**:
1. Take most restrictive maximum (lower sugar cap)
2. Average weights to moderate strictness
3. Prioritize health over indulgence

### B. No Recipes Meet Targets
**Fallback Strategy**:
1. Relax strictest constraint by 20%
2. Search again
3. If still none, show closest match with warning
4. Suggest ingredient substitutions

### C. Missing Nutrient Data
**Handling**:
1. Use FDC API to supplement
2. Estimate from ingredient list
3. If critical nutrient missing, reduce weight
4. Note uncertainty in explanation

### D. Contraindications
**Iron Example**:
```python
if "hemochromatosis" in user.contraindications:
    if "fatigue" in selected_moods:
        # Remove iron target, add warning
        warning = "Iron targets removed due to contraindication"
        # Focus on other fatigue nutrients (B12, carbs, sleep)
```

---

## 6. User Experience Design

### A. Transparent Scoring
**Show users**:
- ✅ Nutrient match score: 87%
- ✅ Why: "High magnesium (135mg) supports your stressed state"
- ✅ Evidence: "Studies suggest magnesium may help with stress"
- ⚠️ Disclaimer: "Not a substitute for medical advice"

### B. Explainability
```json
{
  "score": 0.87,
  "reasons": [
    "Magnesium: 135mg (target ≥120mg) — supports stress response",
    "Omega-3: 0.35g (target ≥0.25g) — anti-inflammatory",
    "Fiber: 9.5g (target ≥8g) — gut-brain axis support"
  ],
  "evidence": [
    "Magnesium-rich foods linked to calmer mood (meta-analyses)",
    "Mediterranean pattern associated with reduced anxiety (SMILES trial)"
  ],
  "disclaimer": "Individual results vary. Consult healthcare provider for persistent symptoms."
}
```

### C. Progressive Disclosure
- **Simple view**: "87% match for your stress + fatigue"
- **Detailed view**: Show nutrient breakdown
- **Science view**: Link to evidence, citations

---

## 7. Testing & Validation Strategy

### A. Unit Tests
```python
def test_mood_aggregation():
    """Test that multiple moods combine correctly"""
    moods = [("stress", "very"), ("fatigue", "medium")]
    targets = engine.aggregate_targets(moods)
    
    # Stress wants magnesium ≥120mg (weight 0.9)
    # Fatigue wants iron ≥6mg (weight 1.0)
    assert "magnesium" in targets
    assert "iron" in targets
    assert targets["magnesium"]["min"] >= 120

def test_scoring_algorithm():
    """Test that scoring rewards good matches"""
    nutrients = {"magnesium": 135, "fiber": 10, "omega_3_epa_dha": 0.3}
    score = engine.score_recipe(nutrients, ["stress"])
    assert 0.5 <= score <= 1.0  # Should be high for stress
```

### B. Integration Tests
```python
async def test_end_to_end():
    """Test full pipeline from mood to recipe"""
    request = {
        "moods": [{"mood": "stress", "intensity": "very"}],
        "profile": sample_profile
    }
    
    response = await client.post("/api/v1/recipes/recommend", json=request)
    assert response.status_code == 200
    assert response.json()["flavor_alignment"]["nutrient_match_score"] > 50
```

### C. A/B Testing Plan
1. **Control**: Original emotional-only matching
2. **Treatment**: Evidence-based nutrient scoring
3. **Metrics**:
   - User satisfaction ratings
   - Recipe completion rate
   - Return usage rate
   - Self-reported mood improvement

---

## 8. Future Enhancements

### Phase 2 (Post-MVP)
1. **Personalized baselines**: Learn user's actual deficiencies from food logs
2. **Temporal patterns**: Adjust targets by time of day (morning energy vs evening calm)
3. **Combination effects**: Model synergies (iron + vitamin C absorption)
4. **Bioavailability**: Weight heme vs non-heme iron differently

### Phase 3 (Advanced)
1. **Machine learning**: Learn which nutrient combinations work for each user
2. **Genetic factors**: Integrate nutrigenomics (MTHFR, etc.)
3. **Microbiome**: Adjust fiber types based on gut health
4. **Clinical validation**: Partner with nutritionists for RCT

---

## 9. Implementation Checklist

### Backend
- [x] Create `mood_mapping.json` with evidence-based targets
- [x] Build `MoodNutritionEngine` for scoring
- [x] Create `FDCClient` for USDA data
- [x] Add nutrient extraction to `EdamamClient`
- [x] Integrate scoring into recommendation endpoint
- [ ] Add unit tests for scoring algorithm
- [ ] Add integration tests for full pipeline
- [ ] Add performance benchmarking

### Data Quality
- [ ] Validate all nutrient aliases with Edamam/FDC docs
- [ ] Ensure unit conversions are correct (mg/g/mcg)
- [ ] Test with 20+ real recipes to verify scoring
- [ ] Verify Mediterranean pattern detection
- [ ] Test contraindication filtering

### UX/Frontend
- [ ] Design score visualization (87% match)
- [ ] Create nutrient breakdown UI
- [ ] Add "Why this recipe?" explanation
- [ ] Show evidence links (expandable)
- [ ] Display medical disclaimers
- [ ] Add feedback mechanism ("Did this help?")

### Legal/Compliance
- [ ] Draft medical disclaimers with legal review
- [ ] Add "Not medical advice" warnings
- [ ] Implement contraindication checking
- [ ] Add opt-out for health claims
- [ ] Create privacy policy for health data

---

## 10. Success Metrics

### Technical Metrics
- Nutrient extraction accuracy: >90%
- Scoring algorithm correlation with expert ratings: >0.7
- API response time: <2 seconds
- Recipe match rate: >80% of requests find suitable recipe

### User Metrics
- User satisfaction: >4.0/5.0
- Recipe completion rate: >60%
- Weekly active users retention: >40%
- Self-reported mood improvement: >50%

### Business Metrics
- User engagement: 3+ sessions per week
- Premium conversion: 15%+ (for personalized features)
- Referral rate: 20%+

---

## Summary

This mapping strategy provides:
1. **Scientific rigor**: Evidence-based nutrient targets
2. **Transparency**: Clear explanations and disclaimers
3. **Flexibility**: Handles multiple moods, intensities, edge cases
4. **Scalability**: Extensible to new moods and nutrients
5. **Safety**: Contraindication handling and medical disclaimers

The key innovation is combining **emotional resonance** (dreamy, grounded) with **nutritional science** (magnesium for stress, iron for fatigue) to create a truly personalized, evidence-based recommendation system.

