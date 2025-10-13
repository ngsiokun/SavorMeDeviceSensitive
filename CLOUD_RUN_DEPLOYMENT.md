# SavorMe Cloud Run Deployment Guide

## 🚀 Quick Start

### Option 1: Deploy Everything (Full Microservices)
```cmd
deploy-to-cloud-run.bat
```

### Option 2: Deploy Frontend Only (For Testing)
```cmd
deploy-frontend-only.bat
```

## 📋 Prerequisites

1. **Google Cloud SDK installed**
   - Download from: https://cloud.google.com/sdk/docs/install
   - Verify: `gcloud version`

2. **Google Cloud Project set up**
   - Create project in Google Cloud Console
   - Set project: `gcloud config set project YOUR_PROJECT_ID`
   - Enable billing

3. **Authenticated with Google Cloud**
   - Run: `gcloud auth login`

4. **Environment file (.env)**
   - Copy your `.env` file to project root
   - Required variables:
     - `EDAMAM_APP_ID`
     - `EDAMAM_APP_KEY`
     - `OPENROUTER_API_KEY`

## 🏗️ Architecture

The deployment creates 5 Cloud Run services:

1. **savorme-frontend** (Port 8080)
   - Flask web application
   - User interface for mood selection and recipe display

2. **savorme-router** (Port 8080)
   - API Gateway
   - Orchestrates communication between microservices

3. **savorme-user-nutrition** (Port 8080)
   - User profile management
   - Nutrition target calculations

4. **savorme-recipe** (Port 8080)
   - Recipe search and scoring
   - Integration with Edamam API

5. **savorme-mood-ai** (Port 8080)
   - Mood interpretation
   - AI content generation via OpenRouter

## 🔧 Configuration

### Environment Variables

Each service is configured with appropriate environment variables:

- **Frontend**: `BACKEND_URL` → Points to API Gateway
- **API Gateway**: Service URLs for all microservices
- **Services**: API keys from `.env` file

### Resource Allocation

- **Frontend**: 512Mi RAM, 1 CPU
- **API Gateway**: 1Gi RAM, 1 CPU  
- **Microservices**: 512Mi RAM, 1 CPU each

## 🌐 Service URLs

After deployment, your services will be available at:

```
Frontend: https://savorme-frontend-{PROJECT_ID}-uc.a.run.app
API Gateway: https://savorme-router-{PROJECT_ID}-uc.a.run.app
User Nutrition: https://savorme-user-nutrition-{PROJECT_ID}-uc.a.run.app
Recipe Service: https://savorme-recipe-{PROJECT_ID}-uc.a.run.app
Mood AI Service: https://savorme-mood-ai-{PROJECT_ID}-uc.a.run.app
```

## 🔍 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check `.env` file exists
   - Verify all dependencies in requirements.txt
   - Check Dockerfile syntax

2. **Service Communication Issues**
   - Verify service URLs in environment variables
   - Check Cloud Run service status
   - Review service logs in Google Cloud Console

3. **Port Issues**
   - All services use port 8080 (Cloud Run standard)
   - Frontend configured to use PORT environment variable

### Logs and Monitoring

- View logs: Google Cloud Console → Cloud Run → Select Service → Logs
- Monitor performance: Google Cloud Console → Cloud Run → Metrics

## 📝 Manual Deployment Steps

If automated scripts fail, you can deploy manually:

1. **Build individual services**:
   ```cmd
   gcloud builds submit --tag gcr.io/{PROJECT_ID}/savorme-frontend ./frontend_app
   ```

2. **Deploy to Cloud Run**:
   ```cmd
   gcloud run deploy savorme-frontend --image gcr.io/{PROJECT_ID}/savorme-frontend --region us-central1 --allow-unauthenticated
   ```

## 🎯 Next Steps

1. **Test the deployment** by visiting the frontend URL
2. **Update environment variables** if needed
3. **Configure custom domain** (optional)
4. **Set up monitoring and alerts**
5. **Implement CI/CD pipeline** for automated deployments

## 📞 Support

If you encounter issues:
1. Check the logs in Google Cloud Console
2. Verify all prerequisites are met
3. Test individual services locally first
4. Review the cloudbuild.yaml configuration

---

**Last Updated**: December 2024
**Version**: 1.0.0
