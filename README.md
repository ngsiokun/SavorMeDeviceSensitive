# SavorMe Backend - Mood-Based Recipe Companion

Backend API for SavorMe, an emotionally intelligent recipe recommendation system that curates recipes based on user's mood, nutritional needs, and culinary preferences.

## 🎯 Overview

SavorMe Backend provides a RESTful API that:
- Interprets user mood combinations into culinary parameters
- Calculates personalized nutrition targets
- Searches for recipes matching emotional and nutritional needs
- Generates poetic emotional rationales using AI
- Integrates with multiple food and AI APIs

## 🏗️ Architecture

### Core Components

```
app/
├── api/           # FastAPI routes and endpoints
├── core/          # Configuration and settings
├── models/        # Pydantic data models
├── services/      # Business logic and external API clients
│   ├── fusion_engine.py      # Mood → Recipe parameter conversion
│   ├── edamam_client.py      # Edamam Recipe Search API
│   ├── openrouter_client.py  # AI-powered emotional rationale
│   └── nutrition_calculator.py # Nutrition calculations
└── utils/         # Utility functions
```

### Key Services

1. **Fusion Engine** - Converts mood combinations into:
   - Flavor bias (floral, spicy, earthy, etc.)
   - Texture preferences (silky, crispy, creamy, etc.)
   - Culinary tone (poetic, bold, nurturing, etc.)
   - Recipe search keywords

2. **Nutrition Calculator** - Calculates daily targets using:
   - Harris-Benedict BMR equation
   - WHO nutrition guidelines
   - Activity level adjustments

3. **Edamam Client** - Searches recipes with filters:
   - Mood-derived keywords
   - Dietary restrictions (vegetarian, vegan, etc.)
   - Allergen exclusions
   - Nutrition ranges (calories, protein, fiber)
   - Cuisine preferences

4. **OpenRouter Client** - Generates emotional content:
   - Poetic recipe descriptions
   - Mood-specific rationales
   - Plating suggestions
   - Journaling prompts

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- API Keys for:
  - [Edamam Recipe API](https://developer.edamam.com/)
  - [OpenRouter AI](https://openrouter.ai/) (optional)
  - [USDA FoodData Central](https://fdc.nal.usda.gov/api-key-signup.html) (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ngsiokun/SavorMe-backend.git
cd SavorMe-backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Run the server**
```bash
# Development mode
uvicorn app.main:app --reload

# Production mode
python app/main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

#### `POST /api/v1/recipes/recommend`
Get complete recipe recommendation with emotional rationale

**Request:**
```json
{
  "mood_blend": {
    "moods": [
      {"mood": "dreamy", "intensity": "very"},
      {"mood": "craving", "intensity": "medium"},
      {"mood": "grounded", "intensity": "a_little"}
    ]
  },
  "user_profile": {
    "age": 34,
    "gender": "female",
    "height_cm": 168,
    "weight_kg": 58,
    "cuisine_preferences": ["Japanese", "Italian"],
    "food_allergies": ["peanuts"],
    "dietary_preference": "vegetarian"
  }
}
```

**Response:**
```json
{
  "recipe": {
    "name": "Yuzu-Scented Risotto with Silken Tofu",
    "ingredients": [...],
    "nutrition": {
      "calories": 520,
      "protein_g": 18,
      "fiber_g": 7
    }
  },
  "emotional_rationale": {
    "overall_rationale": "This dish was chosen to gently cradle your emotional state...",
    "mood_breakdowns": [...]
  },
  "nutrition_comparison": {...},
  "flavor_alignment": {...}
}
```

#### `POST /api/v1/nutrition/calculate`
Calculate daily nutrition targets

#### `POST /api/v1/mood/interpret`
Interpret mood blend into flavor profile

#### `POST /api/v1/recipes/search`
Search recipes based on mood and profile

## 🎨 Mood System

### Available Moods (10 total)

| Mood | Flavor Bias | Texture | Tone |
|------|-------------|---------|------|
| Dreamy | Floral, citrus, vanilla | Silky, smooth | Poetic, artistic |
| Fiery | Spicy, bold, smoky | Crispy, charred | Bold, dramatic |
| Focused | Clean, herbal, sharp | Lean, minimal | Precise, efficient |
| Playful | Fruity, tangy, bright | Bouncy, varied | Whimsical, fun |
| Craving | Rich, creamy, umami | Luscious, decadent | Indulgent, sensory |
| Light | Fresh, crisp, airy | Delicate, fluffy | Bright, elegant |
| Grounded | Earthy, nutty, roasted | Dense, hearty | Traditional, rustic |
| Restorative | Warm, comforting, gentle | Soft, brothy | Nurturing, healing |
| Charismatic | Vibrant, exotic, bold | Dynamic, complex | Sophisticated, magnetic |
| Melancholy | Tender, subtle, soft | Slow-cooked, tender | Introspective, gentle |

### Intensity Levels
- **A little**: 30% weight
- **Medium**: 60% weight  
- **Very**: 100% weight

Users can select 1-3 moods, each with an intensity level.

## 🔧 Configuration

### Environment Variables

See `.env.example` for all configuration options:

```bash
# Required
EDAMAM_APP_ID=your_app_id
EDAMAM_APP_KEY=your_app_key

# Optional (fallback implementations provided)
OPENROUTER_API_KEY=your_openrouter_key
USDA_API_KEY=your_usda_key
HUGGINGFACE_API_KEY=your_hf_key

# Database
DATABASE_URL=sqlite:///./savorme.db
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 📦 Project Structure

```
SavorMe-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Settings and configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── mood.py          # Mood-related models
│   │   ├── user.py          # User profile models
│   │   └── recipe.py        # Recipe models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── fusion_engine.py
│   │   ├── edamam_client.py
│   │   ├── openrouter_client.py
│   │   └── nutrition_calculator.py
│   └── utils/
│       └── __init__.py
├── documentation.md         # Detailed documentation
├── workflow.md             # End-to-end workflow
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔌 API Integration Details

### Edamam Recipe Search API
- **Endpoint**: `https://api.edamam.com/api/recipes/v2`
- **Rate Limit**: 10 requests/min (free tier)
- **Features**: Recipe search with nutrition, cuisine, dietary filters

### OpenRouter AI API
- **Endpoint**: `https://openrouter.ai/api/v1`
- **Models**: Claude 3.5 Sonnet, GPT-4, etc.
- **Usage**: Emotional rationale generation

### USDA FoodData Central
- **Endpoint**: `https://api.nal.usda.gov/fdc/v1/`
- **Rate Limit**: 1,000 requests/hour
- **Usage**: Nutritional data (future enhancement)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Edamam for recipe data API
- OpenRouter for AI API access
- USDA for nutritional guidelines
- FastAPI framework

---

**Built with ❤️ for emotional eaters everywhere**
