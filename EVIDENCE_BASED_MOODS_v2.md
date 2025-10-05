# Evidence-Based Moods v2.1.0 - Focus on Scientific Rigor

## 🎯 Major Change: 12 Moods → 4 Evidence-Based Moods

### Why This Change?

**Scientific Credibility**: The original 12 moods included states like "dreamy", "playful", and "charismatic" that lack scientific evidence linking them to specific nutrient needs. This reduced credibility and made medical/legal defensibility challenging.

**Solution**: Focus exclusively on 4 moods with the strongest scientific support.

---

## 📊 The 4 Evidence-Based Moods

### 1. 😰 **Stressed / Anxious**

**Evidence Level**: ⭐⭐⭐ Moderate - Mixed but trending positive

**Key Nutrients**:
- Magnesium (120mg+) - supports nervous system
- Omega-3 EPA/DHA (0.3g+) - anti-inflammatory
- Fiber (8g+) - gut-brain axis
- Low added sugar (<10g) - prevents spikes

**Scientific Basis**:
- Multiple meta-analyses show magnesium has small-to-moderate benefits for anxiety
- Omega-3 studies show mixed but trending positive results
- Mediterranean diet pattern consistently associated with lower stress

**Key Studies**:
- Magnesium and anxiety meta-analyses (PMC)
- Omega-3 for anxiety (Cochrane reviews)
- Mediterranean diet and mental health
- Caffeine and stress response

**User Aliases**: anxious, wired, restless, overwhelmed, tense

---

### 2. 😴 **Fatigued / Low Energy**

**Evidence Level**: ⭐⭐⭐⭐ Strong - Well-established clinical relationship

**Key Nutrients**:
- Iron (6mg+) - oxygen transport and energy
- Vitamin C (30mg+) - enhances iron absorption
- Complex carbs (30g+) - sustained energy
- Protein (20g+) - stable blood sugar
- Fiber (8g+) - prevents crashes

**Scientific Basis**:
- Iron deficiency (even without anemia) is a **well-established** cause of fatigue
- WHO and medical guidelines strongly support food-first iron intervention
- Glycemic stability through complex carbs prevents energy crashes

**Key Studies**:
- Iron deficiency and fatigue (Office of Dietary Supplements)
- WHO iron guidelines
- Glycemic index and energy (multiple RCTs)
- Vitamin C and iron absorption

**Contraindications**: ⚠️ Hemochromatosis, iron overload

**User Aliases**: tired, exhausted, brain fog, sluggish, drained

---

### 3. 😢 **Low Mood / Blue**

**Evidence Level**: ⭐⭐⭐⭐⭐ Strong - RCT support + meta-analyses (STRONGEST)

**Key Nutrients**:
- Fiber (10g+) - gut microbiome and gut-brain axis
- Omega-3 EPA/DHA (0.35g+) - neurotransmitter support
- Protein (20g+) - amino acids for serotonin
- Low added sugar (<12g) - prevents mood swings

**Scientific Basis**:
- **SMILES trial (2017)**: RCT showing Mediterranean diet significantly improved depression symptoms
- Multiple meta-analyses support omega-3 and fiber for mood
- Gut-brain axis research links microbiome to mental health
- Ultra-processed foods correlate with worse mental health

**Key Studies**:
- **SMILES trial (2017)** - Mediterranean diet for depression
- Mediterranean diet and depression meta-analyses
- Omega-3 and mood (Cochrane reviews)
- Gut-brain axis and mental health
- Ultra-processed foods and depression

**User Aliases**: sad, down, blue, melancholy, depressed, unhappy

---

### 4. 😠 **Irritable / Angry**

**Evidence Level**: ⭐⭐⭐ Moderate - Observational + physiological mechanisms

**Key Nutrients**:
- Protein (22g+) - blood sugar stability
- Fiber (9g+) - slows glucose absorption
- Very low added sugar (<8g) - prevents spikes
- Omega-3 (0.25g+) - anti-inflammatory

**Scientific Basis**:
- Ultra-processed foods correlate with mood disturbances
- Blood sugar variability linked to irritability
- Protein + fiber combination prevents glucose swings
- Physiological mechanism well-understood even if direct RCTs limited

**Key Studies**:
- Ultra-processed foods and mental health (PMC)
- Glycemic index and mood
- Protein and satiety research
- Blood sugar variability and mood

**User Aliases**: angry, snappy, cranky, short-tempered, agitated, annoyed

---

## 📉 Removed Moods (v1.0.0 → v2.0.0)

The following 8 moods were **removed** due to insufficient scientific evidence:

| Removed Mood | Reason |
|--------------|--------|
| Dreamy | No evidence linking poetic/imaginative states to specific nutrient needs |
| Focused | Lacks specific nutrient research beyond general cognitive health |
| Playful | Pattern-based only, no direct evidence |
| Craving | More about satiety than mood per se |
| Light | No specific nutrient-mood connection |
| Grounded | Vague emotional state, lacks research |
| Restorative | Overlaps with general health, not mood-specific |
| Charismatic | No scientific basis for nutrient-confidence link |

**Impact**: Users who previously selected these moods will need to map to one of the 4 evidence-based moods.

---

## 🔬 Evidence Level Definitions

### ⭐⭐⭐⭐⭐ Strong
- **Randomized Controlled Trials (RCTs)** support
- Multiple meta-analyses
- Clinically significant outcomes
- **Example**: Low Mood (SMILES trial)

### ⭐⭐⭐⭐ Strong - Well-established
- Clear clinical relationship
- Major health organizations (WHO, NIH) support
- Consistent observational data
- **Example**: Fatigued (Iron deficiency)

### ⭐⭐⭐ Moderate
- Meta-analyses with mixed but trending positive results
- Strong observational data
- Physiological mechanism understood
- **Examples**: Stressed, Irritable

---

## 💡 User Experience Improvements

### Clearer Choices
Before: "Should I pick dreamy or grounded or charismatic?"
After: "Am I stressed, fatigued, feeling low, or irritable?"

### More Confident Recommendations
Each recommendation now includes:
- ✅ Evidence level rating
- ✅ Key studies citations
- ✅ Mechanism explanation
- ✅ Appropriate disclaimers

### Better Medical Defensibility
- All recommendations backed by peer-reviewed research
- Clear disclaimers about evidence strength
- Contraindications properly flagged
- "Not medical advice" appropriately positioned

---

## 📱 Frontend Impact

### Required UI Changes

1. **Mood Selection Screen**
   - Update from 10-12 mood buttons to 4
   - Add display names (e.g., "Stressed / Anxious")
   - Show evidence level badges (⭐⭐⭐⭐)

2. **Mood Descriptions**
   - Show aliases to help users identify (e.g., "Also: wired, restless, overwhelmed")
   - Brief description per mood

3. **Results Screen**
   - Show evidence level
   - Link to key studies (expandable)
   - Display disclaimers based on mood contraindications

### Example Mood Button

```
┌─────────────────────────────────┐
│  😰 Stressed / Anxious          │
│  ⭐⭐⭐ Moderate Evidence        │
│                                 │
│  Also: wired, restless,         │
│  overwhelmed, tense             │
└─────────────────────────────────┘
```

---

## 🧪 Testing Recommendations

### Validation Tests Needed

1. **Load `mood_mapping.json` v2.0.0**
   - Verify 4 moods load correctly
   - Check all nutrient targets parse
   - Validate evidence levels present

2. **Test Each Mood**
   - stressed + fatigued combination
   - low_mood alone
   - irritable + stressed
   - All 4 moods together

3. **Verify Removed Moods**
   - Ensure old mood IDs return 404
   - Check health endpoint shows only 4 moods
   - Validate no legacy mood remnants

4. **Evidence Display**
   - Explainers render correctly
   - Key studies appear in response
   - Disclaimers show appropriately

### Sample Test Request

```json
{
  "mood_blend": {
    "moods": [
      {"mood": "stressed", "intensity": "very"},
      {"mood": "fatigued", "intensity": "medium"}
    ]
  },
  "user_profile": {
    "age": 32,
    "gender": "female",
    "height_cm": 165,
    "weight_kg": 58,
    "food_allergies": [],
    "dietary_preference": "none"
  }
}
```

**Expected**: Recipe high in magnesium, iron, omega-3, with vitamin C

---

## 📈 Benefits of This Change

### For Users
✅ Less confusion - 4 clear choices vs 12 vague ones
✅ More trust - see evidence levels and studies
✅ Better results - recommendations backed by science
✅ Safer - contraindications properly handled

### For Development
✅ Easier to test (4 moods vs 12)
✅ Clearer validation criteria
✅ Better documentation
✅ Faster iteration cycles

### For Business
✅ Medical/legal defensibility
✅ Marketing differentiator ("evidence-based")
✅ Potential for clinical partnerships
✅ Reduced liability risk

---

## 🚀 Migration Guide (v1 → v2)

### For Existing Users

If users have saved preferences with old moods, map them:

```python
MOOD_MIGRATION_MAP = {
    "dreamy": "low_mood",      # Soft emotions → address underlying mood
    "fiery": "irritable",       # Intense → irritable
    "focused": "stressed",      # Mental demand → stress
    "playful": "stressed",      # Need lightness → reduce stress
    "craving": "irritable",     # Hunger-driven → irritability
    "light": "stressed",        # Seeking lightness → stress relief
    "grounded": "low_mood",     # Seeking stability → lift mood
    "restorative": "fatigued",  # Need healing → address fatigue
    "charismatic": "stressed",  # Performance anxiety → stress
    "melancholy": "low_mood"    # Direct mapping
}
```

### Backend Changes Required

```python
# Old code
if mood_id in ["dreamy", "focused", ...]:  # Now invalid

# New code - will automatically fail with 404
# No changes needed, old moods simply don't exist
```

---

## 📝 Key Takeaways

1. **Quality over quantity**: 4 evidence-based moods > 12 speculative ones
2. **Trust through transparency**: Show evidence levels and studies
3. **Safety first**: Proper contraindications and disclaimers
4. **User-friendly**: Clearer choices, better explanations
5. **Scientifically defensible**: Every recommendation backed by research

---

## 🔗 References

- **SMILES Trial**: Jacka et al. (2017). "A randomised controlled trial of dietary improvement for adults with major depression"
- **Iron & Fatigue**: Office of Dietary Supplements, NIH
- **Magnesium & Anxiety**: Multiple meta-analyses (PMC)
- **Omega-3 & Mood**: Cochrane systematic reviews
- **Mediterranean Diet**: Multiple RCTs and meta-analyses

---

**Version**: 2.1.0  
**Date**: 2025-10-05  
**Status**: Production Ready  
**Breaking Change**: Yes - Old mood IDs no longer supported

