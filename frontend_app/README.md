# SavorMe Functional Demo App

## 🎯 Overview

A **fully functional web demo** that connects to the SavorMe backend API and provides a complete user experience for mood-based recipe recommendations.

## ✨ Features

- ✅ **4 Evidence-Based Moods** with star ratings
- ✅ **Real Backend Integration** - connects to FastAPI backend
- ✅ **Interactive UI** - click to select moods and intensities
- ✅ **Live Recipe Recommendations** - real data from Edamam
- ✅ **Nutrient Match Scoring** - shows evidence-based scores
- ✅ **Beautiful Design** - Canva-quality styling
- ✅ **Responsive Layout** - optimized for mobile and desktop

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd demo_app
pip install -r requirements.txt
```

### 2. Start Backend (Separate Terminal)

```bash
# In project root directory
uvicorn app.main:app --reload
# Backend runs at http://localhost:8000
```

### 3. Start Demo App

```bash
# In demo_app directory
py app.py
# Demo runs at http://localhost:5000
```

### 4. Open in Browser

Visit: `http://localhost:5000/mood-selection`

## 📱 User Flow

1. **Select Moods** → Choose 1-3 moods from 4 options
2. **Set Intensity** → A little, Medium, or Very
3. **Get Recommendation** → Click button to call backend
4. **View Results** → See recipe with evidence-based explanation

## 🔧 Configuration

The demo automatically connects to:
- **Backend**: `http://localhost:8000` (default)

To change backend URL:
```bash
export BACKEND_URL=http://your-backend-url
py app.py
```

## 📊 What It Demonstrates

- Real mood selection with 4 evidence-based options
- Working API integration with FastAPI backend
- Nutrient match scoring display
- Evidence levels and scientific citations
- Complete recipe information
- Nutrition comparison tables

## 🎨 Design

- iPhone 14 Pro mockup (393×852px)
- Professional color scheme
- Smooth animations and transitions
- Evidence badges (⭐⭐⭐⭐⭐)
- Canva-quality styling

## 🧪 Testing

Make sure backend is running:
```bash
curl http://localhost:8000/api/v1/health
```

Should return:
```json
{
  "status": "healthy",
  "available_moods": ["stressed", "fatigued", "low_mood", "irritable"]
}
```

## 📝 Next Steps

This demo can be:
- Used for user testing
- Shown to investors/stakeholders
- Deployed as a web app
- Used as reference for iOS development
- Converted to React/Vue/Svelte

---

**A complete, working prototype of SavorMe!** 🎉

