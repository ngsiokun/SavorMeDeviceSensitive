# ✅ SavorMe Local Testing Checklist - Tomorrow

## 🚀 **Quick Start**

1. **Double-click:** `LOCAL_TEST_TOMORROW.bat`
2. **Wait 10 seconds** for services to start
3. **Open browser:** http://localhost:5000

---

## 🧪 **Test 1: Mediterranean Cuisine + Stressed Mood**

### Steps:
1. Click "Start Your Journey"
2. **Profile:**
   - Age: 32
   - Gender: Female
   - Height: 165 cm
   - Weight: 60 kg
   - Diet: None
   - Cuisine: **Mediterranean** 🫒
   - Allergies: (leave blank)
3. Click "Continue to Mood Selection"
4. **Mood:** Select **Stressed** 😰
5. **Intensity:** Medium
6. Click "🍽 Get My Recipe Recommendation"

### Expected Result:
- ✅ Recipe displays with image
- ✅ Nutrition info shows (calories, protein, fiber)
- ✅ Ingredients list appears
- ✅ Directions appear
- ✅ "Nutrient Match Score" button works
- ✅ Modal shows detailed breakdown
- ✅ Match score ~70-100%

---

## 🧪 **Test 2: Asian Cuisine + Fatigued Mood**

### Steps:
1. Go back to home
2. **Profile:**
   - Age: 28
   - Gender: Male
   - Height: 175 cm
   - Weight: 70 kg
   - Diet: None
   - Cuisine: **South East Asian** 🍜
   - Allergies: (leave blank)
3. **Mood:** Select **Fatigued** 😴
4. **Intensity:** Very
5. Click "🍽 Get My Recipe Recommendation"

### Expected Result:
- ✅ Different recipe from Test 1
- ✅ High in iron, B12, folate (for energy)
- ✅ "Nutrient Match Score" modal works
- ✅ Shows energy-supporting nutrients

---

## 🧪 **Test 3: Italian Cuisine + Low Mood**

### Steps:
1. Go back to home
2. **Profile:**
   - Age: 35
   - Gender: Female
   - Height: 160 cm
   - Weight: 55 kg
   - Diet: Vegetarian
   - Cuisine: **Italian** 🍝
   - Allergies: (leave blank)
3. **Mood:** Select **Low Mood** 😢
4. **Intensity:** Medium
5. Click "🍽 Get My Recipe Recommendation"

### Expected Result:
- ✅ Vegetarian recipe
- ✅ High in omega-3, folate, vitamin D
- ✅ Pasta-based or Italian-style dish
- ✅ Nutrient highlights show mood-supporting nutrients

---

## 🧪 **Test 4: Mexican Cuisine + Irritable Mood**

### Steps:
1. Go back to home
2. **Profile:**
   - Age: 40
   - Gender: Male
   - Height: 180 cm
   - Weight: 85 kg
   - Diet: None
   - Cuisine: **Mexican** 🌮
   - Allergies: peanuts
3. **Mood:** Select **Irritable** 😠
4. **Intensity:** A little
5. Click "🍽 Get My Recipe Recommendation"

### Expected Result:
- ✅ Mexican-style recipe
- ✅ NO peanuts in ingredients
- ✅ High in magnesium, zinc (for mood stability)
- ✅ Recipe suitable for larger male profile

---

## 🧪 **Test 5: Multiple Moods**

### Steps:
1. Go back to home
2. **Profile:** Use any profile
3. **Moods:** Select **2-3 moods** (e.g., Stressed + Fatigued + Low Mood)
4. **Intensity:** Medium
5. Click "🍽 Get My Recipe Recommendation"

### Expected Result:
- ✅ Recipe addresses multiple mood needs
- ✅ "Why This Recipe?" explains how it helps each mood
- ✅ Nutrient highlights cover all selected moods

---

## 🧪 **Test 6: Nutrient Match Score Modal**

### For EVERY test above, check:
1. Click "📊 Nutrient Match Score" button
2. **Modal should show:**
   - ✅ Match score percentage (usually 60-100%)
   - ✅ "Why This Recipe?" with detailed explanation
   - ✅ Nutrition Breakdown table
   - ✅ Nutrient Highlights with targets and percentages
   - ✅ Scientific Evidence section
   - ✅ "Another Recipe Suggestion" button works
   - ✅ "← Go Back" button closes modal

---

## 🧪 **Test 7: Error Handling**

### Test with invalid data:
1. Try leaving profile fields empty
2. Try very high/low values (age: 200, weight: 5)
3. Try selecting no mood

### Expected Result:
- ✅ Validation prevents submission OR
- ✅ Clear error message appears OR
- ✅ Default values are used

---

## 🐛 **Known Issues to Watch For**

### ❌ Things that should NOT happen:
- Recipe image is a logo or brand image
- Recipe has no ingredients
- Recipe has no directions
- "Nutrient Match Score" button doesn't respond
- Modal doesn't open
- Error: "Failed to get recommendation"
- Error: "Backend not running"

### ✅ If these happen:
1. Check backend is running (http://127.0.0.1:8000/docs should work)
2. Check frontend logs in Command Prompt window
3. Check browser console (F12) for JavaScript errors

---

## 📊 **Testing Summary**

After completing all tests, confirm:

- [ ] All 4 cuisines work (Mediterranean, Asian, Italian, Mexican)
- [ ] All 4 moods work (Stressed, Fatigued, Low Mood, Irritable)
- [ ] Multiple moods work
- [ ] Dietary restrictions respected (vegetarian, allergies)
- [ ] "Nutrient Match Score" button works
- [ ] Modal displays correctly
- [ ] "Another Recipe Suggestion" generates new recipe
- [ ] "Go Back" navigation works

---

## ✅ **If All Tests Pass**

**YOU'RE READY FOR CLOUD RUN DEPLOYMENT!**

Run: `DEPLOY_TO_CLOUD_RUN.bat`

---

## ❌ **If Any Test Fails**

1. Note which test failed
2. Copy the error message
3. Check browser console (F12)
4. Paste into Cursor for debugging

---

**Estimated Testing Time:** 15-20 minutes  
**Last Updated:** October 14, 2025

