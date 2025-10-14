# 🧪 Complete Local Testing Guide

## 📋 **What We're Testing**
1. Backend health
2. Frontend health  
3. Frontend → Backend connection
4. All 4 cuisines working end-to-end
5. Browser UI functionality

---

## 🚀 **Step-by-Step Testing**

### **Step 1: Start Backend** ✅ (Already Running)

Backend is already running on **http://127.0.0.1:8000**

Verify:
```cmd
curl http://127.0.0.1:8000/api/v1/health
```

Expected: `{"status":"healthy"...}`

---

### **Step 2: Start Frontend**

**Open NEW Command Prompt:**
```cmd
cd C:\Users\Samsung\savorme-cloud-run\SavorMeDeviceSensitive
START_LOCAL_FRONTEND.bat
```

**Wait for:**
```
 * Running on http://127.0.0.1:5000
```

---

### **Step 3: Test Frontend → Backend Connection**

**Open ANOTHER Command Prompt:**
```cmd
cd C:\Users\Samsung\savorme-cloud-run\SavorMeDeviceSensitive
python test_frontend_to_backend.py
```

**Expected Output:**
```
✅ Frontend is running at http://127.0.0.1:5000
✅ SUCCESS! Frontend → Backend connection working!

Recipe Details:
   Name: [Recipe Name]
   Calories: [XXX]
   Protein: [XX]g
   Fiber: [XX]g

Testing All Cuisines Through Frontend
✅ Mediterranean        - [Recipe Name]
✅ South East Asian     - [Recipe Name]
✅ Italian              - [Recipe Name]
✅ Mexican              - [Recipe Name]

🎉 Frontend ↔ Backend connection fully working!
✅ Ready to test in browser: http://localhost:5000
✅ Ready for Cloud Run deployment!
```

---

### **Step 4: Test in Browser**

**Open Browser:**
```
http://localhost:5000
```

#### **Test Scenario 1: Mediterranean + Stressed**
1. Click "Start Your Journey"
2. Fill in profile:
   - Age: 32
   - Gender: Female
   - Height: 165 cm
   - Weight: 60 kg
   - Cuisine: **Mediterranean** ✓
3. Click "Continue to Mood Selection"
4. Select mood: **Stressed**
5. Choose intensity: **Medium**
6. Click "🍽 Get My Recipe Recommendation"

**Expected:** Recipe page with:
- Recipe name
- Image
- Ingredients list
- Nutritional info
- Emotional rationale
- "Generate New Recipe" button works

#### **Test Scenario 2: Asian + Fatigued**
1. Go back to profile
2. Change cuisine to: **Asian**
3. Continue to mood selection
4. Select mood: **Fatigued**
5. Intensity: **Very**
6. Get recommendation

**Expected:** Asian recipe (Thai, Vietnamese, etc.)

#### **Test Scenario 3: Multiple Moods**
1. Select moods: **Stressed** + **Low Mood**
2. Get recommendation

**Expected:** Recipe balancing both mood needs

---

## ✅ **Success Criteria**

### **Backend:**
- [ ] `/api/v1/health` returns 200
- [ ] All 4 cuisines return recipes
- [ ] Response time < 5 seconds

### **Frontend:**
- [ ] Landing page loads
- [ ] Profile form works
- [ ] Cuisine dropdown shows 4 options
- [ ] Mood selection works
- [ ] Recipe results display correctly

### **Frontend ↔ Backend:**
- [ ] `/api/recommend` endpoint works
- [ ] No CORS errors
- [ ] No "[object Object]" errors
- [ ] All cuisines work through frontend
- [ ] Nutritional data displays

### **Browser UI:**
- [ ] No console errors
- [ ] Images load
- [ ] Responsive on mobile size
- [ ] "Generate New Recipe" works
- [ ] "Go Back" navigation works

---

## 🐛 **Troubleshooting**

### Frontend Won't Start
```cmd
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill process if needed
taskkill /PID <PID> /F

# Restart
START_LOCAL_FRONTEND.bat
```

### "Backend service unavailable"
- Check backend is running: `curl http://127.0.0.1:8000/api/v1/health`
- Check `BACKEND_URL` is set to `http://127.0.0.1:8000`
- Restart backend

### Console Errors
- Open browser DevTools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for failed requests

---

## 📊 **Current Status**

### ✅ **Working:**
- Backend health check
- All 4 cuisines via backend API
- Cuisine validation
- Fallback logic

### 🔄 **To Test:**
- [ ] Frontend starts successfully
- [ ] Frontend → Backend proxy works
- [ ] Browser UI fully functional
- [ ] All cuisines through browser

---

## 🚀 **After All Tests Pass**

1. **Stop Local Services:**
   - Press Ctrl+C in both Command Prompts (backend & frontend)

2. **Deploy to Cloud Run:**
   ```cmd
   deploy-to-cloud-run.bat
   ```

3. **Test Live Application:**
   - https://savorme-frontend-662773309683.us-central1.run.app

---

**🎯 Current Step: Start Frontend and Run test_frontend_to_backend.py**

