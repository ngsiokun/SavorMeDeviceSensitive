# 🎯 Test Your SavorMe App!

## 🌐 **Live URL**
https://savorme-frontend-662773309683.us-central1.run.app

---

## 🧪 **Test Scenarios**

### **Test 1: Mediterranean + Stressed**
1. Select cuisine: **Mediterranean**
2. Select mood: **Stressed**
3. Intensity: **Medium**
4. Expected: Greek/Mediterranean recipe with calming ingredients (salmon, spinach, etc.)

### **Test 2: Asian + Fatigued**
1. Select cuisine: **Asian** (now works!)
2. Select mood: **Fatigued**
3. Intensity: **Very**
4. Expected: Asian-inspired recipe with energizing ingredients (iron-rich, protein)

### **Test 3: Chinese + Low Mood**
1. Select cuisine: **Chinese**
2. Select mood: **Low Mood**
3. Intensity: **Medium**
4. Expected: Chinese recipe with mood-boosting nutrients (omega-3, fiber)

### **Test 4: Surprise Me + Irritable**
1. Select cuisine: **Surprise Me** (no filter)
2. Select mood: **Irritable**
3. Intensity: **A little**
4. Expected: Any cuisine with stabilizing ingredients (protein, fiber, low sugar)

### **Test 5: Multiple Moods**
1. Select cuisine: **Italian**
2. Select moods: **Stressed** + **Fatigued**
3. Intensity: **Medium**
4. Expected: Italian recipe balancing both mood needs

---

## ✅ **What to Check**

### **1. Profile Page**
- [ ] All form fields work
- [ ] Cuisine dropdown shows 17 options
- [ ] "Surprise Me" is at the top
- [ ] Emojis display correctly

### **2. Mood Selection**
- [ ] Can select up to 3 moods
- [ ] Intensity buttons work
- [ ] "Get My Recipe Recommendation" button enabled after selection

### **3. Recipe Results**
- [ ] Recipe image loads
- [ ] Recipe name displays
- [ ] Ingredients list shows
- [ ] Nutritional info displays
- [ ] Emotional rationale appears
- [ ] "Generate New Recipe" works

### **4. Error Handling**
- [ ] No more "Error: [object Object]"
- [ ] If error occurs, shows friendly message
- [ ] Can go back and try again

---

## 🐛 **If You See Issues**

### **"Failed to get recommendation"**
- Check if cuisine is valid
- Try "Surprise Me" (no cuisine filter)
- Check browser console for errors

### **"Backend service unavailable"**
- Services might be cold-starting (wait 10 seconds)
- Try refreshing the page

### **Recipe has no image**
- Normal - some recipes don't have images
- Recipe data is still valid

---

## 📊 **Expected Response Times**

- **First request:** 10-15 seconds (cold start)
- **Subsequent requests:** 3-5 seconds
- **Image loading:** 1-2 seconds

---

## 🎉 **Success Criteria**

✅ All cuisines work (especially "Asian"!)  
✅ All moods generate recipes  
✅ Nutritional info matches profile  
✅ No 500 errors  
✅ Beautiful UI on mobile and desktop  

---

**Happy Testing! 🚀**

