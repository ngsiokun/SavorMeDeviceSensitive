# 🍽️ SavorMe - Mood-Based Recipe Recommendation App

## 🚀 **Quick Deployment (5 Minutes)**

### **Prerequisites**
1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Copy your `.env` file to project root (contains API keys)

### **Deployment Steps**
```cmd
# 1. Authenticate with Google Cloud
gcloud auth login

# 2. Set project (already configured)
gcloud config set project savorme-474712

# 3. Check setup
.\check-setup.bat

# 4. Deploy to Cloud Run
.\deploy-to-cloud-run.bat
```

## 🌐 **Live URLs After Deployment**
- **Frontend**: `https://savorme-frontend-savorme-474712-uc.a.run.app`
- **API Gateway**: `https://savorme-router-savorme-474712-uc.a.run.app`

## 🏗️ **Architecture**
- **Frontend**: Flask web app (mood selection & recipe display)
- **API Gateway**: FastAPI router (orchestrates microservices)
- **User Nutrition Service**: Profile management & nutrition calculations
- **Recipe Service**: Recipe search & scoring via Edamam API
- **Mood AI Service**: Mood interpretation & AI content generation

## ✅ **What's Fixed & Ready**
- ✅ All Dockerfiles configured for Cloud Run (port 8080)
- ✅ All environment variables properly set
- ✅ All path issues resolved
- ✅ Complete deployment scripts
- ✅ Google Cloud project configured (`savorme-474712`)
- ✅ Account authenticated (`ngsiokun88@gmail.com`)

## 📋 **Required Environment Variables (.env)**
```
EDAMAM_APP_ID=your_edamam_app_id
EDAMAM_APP_KEY=your_edamam_app_key
OPENROUTER_API_KEY=your_openrouter_key
```

## 🎯 **Features**
- Mood-based recipe recommendations
- AI-powered emotional rationale generation
- Nutritional analysis and scoring
- Beautiful responsive web interface
- Scalable microservices architecture

## 📚 **Documentation**
- `CLOUD_RUN_DEPLOYMENT.md` - Complete deployment guide
- `SETUP_REQUIREMENTS.md` - Prerequisites and troubleshooting
- `PROJECT_STATUS.md` - Current status and fixes applied

## 🚀 **Deployment Scripts**
- `deploy-to-cloud-run.bat` - Deploy all services
- `deploy-frontend-only.bat` - Deploy frontend only
- `test-docker-builds.bat` - Test builds locally
- `check-setup.bat` - Validate setup

---

**Status**: ✅ **Production Ready**  
**Deployment Time**: ~10-15 minutes  
**Last Updated**: December 2024