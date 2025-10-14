# ☁️ Cloud Run Deployment Steps

## 🎯 **Pre-Deployment Checklist**

Before deploying, ensure:
- ✅ Local testing complete (see `LOCAL_TESTING_CHECKLIST.md`)
- ✅ All 4 cuisines tested and working
- ✅ All 4 moods tested and working
- ✅ "Nutrient Match Score" button working
- ✅ No errors in browser console

---

## 🚀 **Deployment Method 1: Automated (RECOMMENDED)**

### **Double-click:** `DEPLOY_TO_CLOUD_RUN.bat`

This will:
1. Navigate to project directory
2. Run `gcloud builds submit`
3. Deploy all 5 services:
   - Router (API Gateway)
   - User-Nutrition Service
   - Recipe Service
   - Mood-AI Service
   - Frontend

**Time:** ~10-15 minutes

---

## 🚀 **Deployment Method 2: Manual**

### **Open Command Prompt and run:**

```cmd
cd C:\Users\Samsung\savorme-cloud-run\SavorMeDeviceSensitive
"C:\Users\Samsung\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" builds submit --config cloudbuild.yaml . --substitutions=COMMIT_SHA="MANUAL_DEPLOY"
```

---

## 📦 **What Gets Deployed**

### **1. Router Service**
- **URL:** https://savorme-router-662773309683.us-central1.run.app
- **Purpose:** API Gateway that orchestrates all microservices
- **Recent fixes:**
  - Updated service URLs to Cloud Run endpoints
  - Fixed Pydantic serialization (`.model_dump(mode='json')`)
  - Added `/api/v1/recipes/recommend` endpoint

### **2. User-Nutrition Service**
- **URL:** https://savorme-user-nutrition-662773309683.us-central1.run.app
- **Purpose:** Calculates nutrition targets based on user profile
- **Recent fixes:**
  - Fixed port to 8080
  - Fixed import statements (`from shared_models import ...`)

### **3. Recipe Service**
- **URL:** https://savorme-recipe-662773309683.us-central1.run.app
- **Purpose:** Searches Edamam API for recipes
- **Recent fixes:**
  - Added cuisine mapping for Edamam API
  - Implemented fallback logic (retry without cuisine if no results)
  - Fixed case sensitivity for cuisine types

### **4. Mood-AI Service**
- **URL:** https://savorme-mood-ai-662773309683.us-central1.run.app
- **Purpose:** Interprets moods and generates AI content using OpenRouter
- **Recent fixes:**
  - Fixed port to 8080
  - Added `MoodInterpretation` to imports

### **5. Frontend Service**
- **URL:** https://savorme-frontend-662773309683.us-central1.run.app
- **Purpose:** User-facing web application
- **Recent fixes:**
  - Fixed "Nutrient Match Score" button (now uses `querySelectorAll`)
  - Updated cuisine dropdown to use Edamam's exact types
  - Set `BACKEND_URL` to router service URL

---

## ⏱️ **Deployment Timeline**

| Step | Duration | What Happens |
|------|----------|-------------|
| Build Images | 5-8 min | Builds Docker images for all 5 services |
| Push to Registry | 1-2 min | Uploads images to Google Container Registry |
| Deploy Services | 2-3 min | Deploys services to Cloud Run |
| Health Checks | 1-2 min | Verifies services are healthy |
| **Total** | **10-15 min** | **Complete deployment** |

---

## ✅ **Post-Deployment Verification**

### **Step 1: Check Build Status**
Watch the Cloud Build output for:
```
BUILD SUCCESS
```

### **Step 2: Verify All Services**
Open each URL and check status:

1. **Router:** https://savorme-router-662773309683.us-central1.run.app/docs
   - Should show FastAPI docs

2. **User-Nutrition:** https://savorme-user-nutrition-662773309683.us-central1.run.app/docs
   - Should show FastAPI docs

3. **Recipe:** https://savorme-recipe-662773309683.us-central1.run.app/docs
   - Should show FastAPI docs

4. **Mood-AI:** https://savorme-mood-ai-662773309683.us-central1.run.app/docs
   - Should show FastAPI docs

5. **Frontend:** https://savorme-frontend-662773309683.us-central1.run.app
   - Should show SavorMe landing page

### **Step 3: Test Live App**
1. Open: https://savorme-frontend-662773309683.us-central1.run.app
2. Click "Start Your Journey"
3. Fill profile (Mediterranean, Stressed, Medium intensity)
4. Click "Get My Recipe Recommendation"
5. Verify recipe appears
6. Click "Nutrient Match Score" button
7. Verify modal opens

---

## 🐛 **Troubleshooting**

### **Problem: Build Fails**

**Symptoms:**
```
ERROR: build step 0 failed
```

**Solution:**
1. Check `cloudbuild.yaml` syntax
2. Verify all Dockerfiles exist
3. Check gcloud authentication: `gcloud auth list`

---

### **Problem: Service Shows "Unhealthy"**

**Symptoms:**
- Service deployed but shows "degraded" status
- 500 errors when accessing service

**Solution:**
1. Check Cloud Run logs:
   - Go to: https://console.cloud.google.com/run
   - Click on service
   - Click "LOGS" tab
2. Look for errors in startup logs
3. Common issues:
   - Missing environment variables
   - Port not set to 8080
   - Import errors

---

### **Problem: Frontend Can't Connect to Backend**

**Symptoms:**
- Frontend loads but shows "Failed to get recommendation"
- Alert: "Make sure the backend is running"

**Solution:**
1. Verify `BACKEND_URL` is set correctly in frontend deployment
2. Check router service is healthy
3. Check CORS settings in router
4. View browser console (F12) for error details

---

### **Problem: Recipe Service Returns Empty Results**

**Symptoms:**
- "No recipes found for your criteria"
- Empty recipe list

**Solution:**
1. Check Edamam API credentials are set:
   - `EDAMAM_APP_ID`
   - `EDAMAM_APP_KEY`
2. Verify cuisine mapping in `recipe-service/main.py`
3. Check Edamam API quota (free tier: 5 requests/min)

---

## 🔄 **Redeployment**

If you need to redeploy after making changes:

1. Make your code changes locally
2. Test locally first (`LOCAL_TEST_TOMORROW.bat`)
3. Run `DEPLOY_TO_CLOUD_RUN.bat` again
4. Services will be updated (not deleted and recreated)

---

## 💰 **Cost Considerations**

### **Cloud Run Pricing (Free Tier):**
- First 2 million requests/month: FREE
- 180,000 vCPU-seconds/month: FREE
- 360,000 GiB-seconds/month: FREE

### **Your Current Usage:**
- 5 services × minimal traffic = **Well within free tier**
- Estimated cost: **$0/month** for testing/demo

---

## 📊 **Environment Variables**

### **Frontend:**
```bash
BACKEND_URL=https://savorme-router-662773309683.us-central1.run.app
```

### **Router:**
```bash
USER_NUTRITION_SERVICE_URL=https://savorme-user-nutrition-662773309683.us-central1.run.app
RECIPE_SERVICE_URL=https://savorme-recipe-662773309683.us-central1.run.app
MOOD_AI_SERVICE_URL=https://savorme-mood-ai-662773309683.us-central1.run.app
```

### **Recipe Service:**
```bash
EDAMAM_APP_ID=<your-app-id>
EDAMAM_APP_KEY=<your-app-key>
```

### **Mood-AI Service:**
```bash
OPENROUTER_API_KEY=<your-api-key>
```

---

## 🎯 **Success Criteria**

Deployment is successful when:
- ✅ All 5 services show "Healthy" status in Cloud Run console
- ✅ Frontend loads at https://savorme-frontend-662773309683.us-central1.run.app
- ✅ Can complete full user journey (profile → mood → recipe)
- ✅ "Nutrient Match Score" modal works
- ✅ No errors in browser console

---

**Last Updated:** October 14, 2025  
**Next Deployment:** After local testing tomorrow

