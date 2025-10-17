# Gemini Deployment Consultation - SavorMe App Issues

## 🎯 **Current Situation Summary**

### **Problem Statement**
We have a SavorMe mood-based recipe recommendation app with multiple critical issues preventing proper functionality:

1. **Backend Startup Failure**: Local backend won't start due to module import errors
2. **Image Mismatch**: Recipe images don't match the actual recipes (e.g., "Eggs with Avocado and Chard" showing rice/curry image)
3. **Missing Ingredient Units**: Recipe ingredients display quantities without units (e.g., "2.0 extra-virgin olive oil" instead of "2.0 tablespoons")
4. **Frontend-Backend Communication**: 500 Internal Server Error when frontend tries to communicate with backend

### **Current Architecture**
- **Frontend**: Flask app running on `localhost:5000` ✅ (Working)
- **Backend**: FastAPI app should run on `127.0.0.1:8000` ❌ (Failing)
- **Cloud Run**: Existing deployment at `https://savorme-router-662773309683.us-central1.run.app` ✅ (Available)

### **Technical Details**

#### **Backend Error**
```
ModuleNotFoundError: No module named 'app'
```
- Running from wrong directory
- Virtual environment issues
- Import path problems

#### **Image System Issues**
- Edamam returns 1800+ character AWS S3 signed URLs (rejected by 500-char filter)
- Frontend fallback selects wrong image categories
- "Eggs with Avocado and Chard" → "rice_egg" category → Wrong image

#### **Ingredient Units Missing**
- Backend parsing not including units
- Frontend display not showing units
- Data loss in API response

## 🤔 **Strategic Options**

### **Option 1: Fix Local Development**
**Pros:**
- Faster development cycle
- No cloud costs
- Full control over environment

**Cons:**
- Complex setup issues
- Environment inconsistencies
- Time-consuming debugging

### **Option 2: Deploy to Cloud Run (Recommended)**
**Pros:**
- Production-ready environment
- Consistent deployment
- Scalable infrastructure
- Already partially working

**Cons:**
- Cloud costs
- Deployment time
- Less local control

### **Option 3: Hybrid Approach**
**Pros:**
- Best of both worlds
- Local development + cloud testing

**Cons:**
- More complex setup
- Multiple environments to maintain

## 🚀 **Immediate Action Plan**

### **Phase 1: Quick Cloud Deployment**
1. Deploy current code to Cloud Run
2. Test full functionality in cloud environment
3. Fix image matching and ingredient units
4. Verify end-to-end workflow

### **Phase 2: Local Development Fix**
1. Fix local backend startup issues
2. Set up proper development environment
3. Create reliable local testing workflow

### **Phase 3: Image & Data Fixes**
1. Fix image category matching for egg/avocado recipes
2. Restore ingredient units in API responses
3. Improve image fallback logic

## 📋 **Specific Technical Questions for Gemini**

1. **Deployment Strategy**: Should we prioritize Cloud Run deployment or fix local development first?

2. **Image Matching**: How can we improve the frontend image selection algorithm to better match recipe names to appropriate image categories?

3. **Ingredient Units**: What's the best approach to preserve and display ingredient units throughout the API chain?

4. **Architecture**: Is the current microservices approach optimal, or should we simplify to a monolithic deployment?

5. **Development Workflow**: What's the most efficient way to set up a reliable local development environment for this FastAPI + Flask stack?

## 🔧 **Current File Structure**
```
SavorMeDeviceSensitive/
├── app/                    # FastAPI backend
├── demo_app/              # Flask frontend  
├── backend_app/           # Microservices
├── router/                # API Gateway
├── deploy-to-cloud-run.bat # Cloud deployment script
├── start.bat              # Local startup script
└── requirements.txt       # Dependencies
```

## 🎯 **Success Criteria**
- [ ] Backend API responding correctly
- [ ] Recipe images matching recipe names
- [ ] Ingredient units displaying properly
- [ ] End-to-end mood selection → recipe recommendation workflow
- [ ] Reliable local development environment

## 💡 **Key Files to Focus On**
- `app/services/edamam_client.py` - Recipe data parsing
- `demo_app/static/js/recipe_result.js` - Image selection logic
- `app/api/routes.py` - API endpoints
- `demo_app/app.py` - Frontend configuration

---

**Request for Gemini**: Please provide strategic advice on the best approach to resolve these issues, focusing on deployment strategy, image matching improvements, and ingredient unit preservation.
