# SavorMe Microservices Deployment Guide

## 🎯 Architecture Overview

SavorMe has been successfully restructured into **3 microservices + API Gateway + Frontend**:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway    │    │  User & Nutr.   │
│   (Port 5000)   │◄──►│   (Port 8000)    │◄──►│   (Port 8001)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ├──► Recipe Service (Port 8002)
                              │
                              └──► Mood & AI Service (Port 8003)
```

## 🚀 Quick Start (Local Development)

### Option 1: Individual Services
```bash
# Start all services individually
start-microservices.bat
```

### Option 2: Docker Compose
```bash
# Start all services with Docker
docker-compose up --build
```

## 🌐 Cloud Deployment

### Deploy to Google Cloud Run
```bash
# Deploy all services
gcloud builds submit --config cloudbuild.yaml
```

## 📋 Service Details

### **Service 1: User & Nutrition Service** (Port 8001)
- **Purpose**: User profile management & nutrition calculations
- **Endpoints**: 
  - `POST /nutrition/calculate` - Calculate daily nutrition targets
  - `POST /user/profile/validate` - Validate user profile
- **Dependencies**: None (uses medical formulas)

### **Service 2: Recipe Service** (Port 8002)
- **Purpose**: Recipe search, scoring, and variety rotation
- **Endpoints**:
  - `POST /recipes/search` - Search and score recipes
- **Dependencies**: Edamam Recipe API

### **Service 3: Mood & AI Service** (Port 8003)
- **Purpose**: Mood interpretation and AI content generation
- **Endpoints**:
  - `POST /mood/interpret` - Interpret mood into search parameters
  - `POST /ai/generate-content` - Generate emotional rationale
- **Dependencies**: OpenRouter AI API

### **API Gateway** (Port 8000)
- **Purpose**: Orchestrates all services, maintains original API contract
- **Endpoints**: All original SavorMe endpoints
- **Dependencies**: All 3 microservices

### **Frontend** (Port 5000)
- **Purpose**: Beautiful web interface
- **Dependencies**: API Gateway

## 🔧 Environment Variables

Create `.env` file with:
```bash
# Edamam Recipe API
EDAMAM_APP_ID=your_app_id
EDAMAM_APP_KEY=your_app_key

# OpenRouter AI
OPENROUTER_API_KEY=your_api_key

# Backend URL for frontend
BACKEND_URL=http://localhost:8000
```

## 🧪 Testing the Architecture

### 1. Health Checks
```bash
curl http://localhost:8001/health  # User & Nutrition
curl http://localhost:8002/health  # Recipe Service  
curl http://localhost:8003/health  # Mood & AI
curl http://localhost:8000/health  # API Gateway
```

### 2. End-to-End Test
1. Open http://localhost:5000
2. Fill out profile
3. Select mood
4. Get recipe recommendation

## 📊 Benefits of Microservices Architecture

### ✅ **Scalability**
- Scale each service independently based on demand
- Recipe service can handle high search loads
- AI service can scale for content generation

### ✅ **Maintainability** 
- Each service has single responsibility
- Easier debugging and updates
- Independent deployments

### ✅ **Reliability**
- Service isolation prevents cascading failures
- Can implement circuit breakers
- Individual health monitoring

### ✅ **Technology Flexibility**
- Each service can use optimal technology stack
- Easy to replace services (e.g., different AI provider)

## 🔄 Migration from Monolithic

The API Gateway maintains **100% backward compatibility** with the original monolithic API:

- ✅ All original endpoints work unchanged
- ✅ Frontend requires no modifications  
- ✅ Same request/response formats
- ✅ Same authentication (if any)

## 🎯 Next Steps

1. **Test locally**: Run `start-microservices.bat`
2. **Deploy to Cloud Run**: Use `cloudbuild.yaml`
3. **Monitor services**: Check health endpoints
4. **Scale as needed**: Adjust Cloud Run instances

---

**🎉 SavorMe is now a modern, scalable microservices architecture!**
