# SavorMe – Mood-Based Recipe Companion

## Table of Contents
1. [App Overview](#app-overview)
2. [Core Concept](#core-concept)
3. [Architecture](#architecture)
4. [Data Sources & APIs](#data-sources--apis)
5. [User Flow](#user-flow)
6. [Technical Requirements](#technical-requirements)
7. [Example Output](#example-output)

## App Overview

SavorMe is an iOS app that curates recipes based on a user's emotional state, nutritional needs, and culinary preferences. It blends mood input, personality profile, and cultural context to deliver meals that comfort, excite, or indulge—each paired with poetic narration and sensory resonance.

The app empowers users to explore how they feel and what they crave through food that speaks to their emotions. It's not just about eating—it's about savoring emotion through flavor.

## Core Concept

### The Problem
Traditional recipe apps focus solely on ingredients and cooking techniques, ignoring the emotional and psychological aspects of food. People often eat based on their mood, but there's no intelligent system that understands this connection.

### The Solution
SavorMe creates a bridge between emotional state and culinary choice by:
- Capturing user mood through an intuitive interface
- Building comprehensive personality profiles
- Leveraging AI to generate emotionally resonant recipe descriptions
- Providing nutritional guidance that aligns with both health and emotional needs

## Mood System

### Emotional States & Intensity Mapping

SavorMe uses a sophisticated mood palette system that allows users to select up to 3 moods from 10 emotional states, each with 3 intensity levels:

| Mood         | Description                          | Intensity Levels       |
|--------------|--------------------------------------|------------------------|
| Dreamy       | Soft, poetic, imaginative            | A little, Medium, Very |
| Fiery        | Bold, intense, passionate            | A little, Medium, Very |
| Focused      | Sharp, minimal, driven               | A little, Medium, Very |
| Playful      | Light, curious, whimsical            | A little, Medium, Very |
| Craving      | Indulgent, sensory, longing          | A little, Medium, Very |
| Light        | Fresh, airy, gentle                  | A little, Medium, Very |
| Grounded     | Earthy, stable, calm                 | A little, Medium, Very |
| Restorative  | Healing, warm, nurturing             | A little, Medium, Very |
| Charismatic  | Flirty, radiant, magnetic            | A little, Medium, Very |
| Melancholy   | Tender, introspective, slow          | A little, Medium, Very |

### Mood Fusion Engine

The Fusion Engine interprets combinations of emotional states and intensity levels to generate:

- **Flavor Bias**: Primary taste directions (e.g., floral, citrus, umami, spicy, earthy)
- **Texture Preference**: Desired mouthfeel (e.g., silky, creamy, crisp, brothy, velvety)
- **Culinary Tone**: Cooking approach and presentation style (e.g., poetic, bold, nurturing, minimal)

#### Example Mood Combinations

| Mood Combination            | Interpretation Summary                                                                 | Flavor Bias         | Texture Preference | Culinary Tone        |
|-----------------------------|-----------------------------------------------------------------------------------------|----------------------|---------------------|-----------------------|
| Dreamy (Very) + Craving (Medium) + Grounded (A little) | Longing for softness and indulgence with gentle anchoring.                          | Floral, citrus, umami | Silky, creamy        | Poetic, slow-paced    |
| Fiery (Very) + Focused (Medium) + Light (A little)     | Intense drive with clarity and minimal distraction.                                | Spicy, sharp, herbal  | Crisp, lean          | Bold, minimal         |
| Melancholy (Medium) + Restorative (Very) + Craving (A little) | Emotional tenderness seeking warmth and quiet pleasure.                        | Earthy, warm, sweet   | Soft, brothy         | Healing, introspective|
| Playful (Very) + Charismatic (Medium) + Light (A little) | Radiant curiosity with a touch of elegance.                                      | Fruity, tangy, bright | Airy, crunchy        | Flirty, whimsical     |
| Grounded (Very) + Focused (Medium) + Restorative (A little) | Stability with purpose and gentle renewal.                                     | Nutty, savory, herbal | Dense, roasted       | Calm, intentional     |
| Craving (Very) + Fiery (Medium) + Dreamy (A little)     | Sensory hunger with emotional intensity and a hint of fantasy.                   | Rich, spicy, floral   | Velvety, bold        | Indulgent, dramatic   |
| Melancholy (Very) + Dreamy (Medium) + Grounded (A little) | Deep introspection with poetic longing and quiet grounding.                   | Bitter, floral, earthy| Soft, slow-cooked    | Tender, reflective    |
| Focused (Very) + Light (Medium) + Playful (A little)    | Precision with freshness and a spark of curiosity.                               | Herbal, citrus, clean | Crisp, minimal       | Bright, efficient     |
| Restorative (Very) + Grounded (Medium) + Craving (A little) | Healing nourishment with emotional depth and light indulgence.               | Warm, savory, sweet   | Brothy, creamy        | Nurturing, soulful    |
| Charismatic (Very) + Fiery (Medium) + Playful (A little) | Magnetic energy with boldness and charm.                                        | Spicy, fruity, tangy  | Juicy, vibrant        | Flirty, high-energy   |

### Fusion Engine Outputs

The Fusion Engine uses mood combinations to generate:
- **Flavor bias** (e.g., citrus, spicy, earthy)
- **Texture preference** (e.g., silky, crisp, brothy)
- **Culinary tone** (e.g., poetic, bold, nurturing)

These outputs guide the recipe query builder and LLM narration layer, with user feedback refining the mappings over time.

## Architecture

### Core Modules

| Module | Function |
|--------|----------|
| **Personality Profile Setup** | Captures age, gender, height, weight, ethnic background, food allergies, dietary preferences, and cuisine preferences. Calculates recommended calorie, protein, and fiber intake. |
| **Mood Input Layer** | User selects up to 3 moods from a palette of 10 (e.g., Dreamy, Fiery, Grounded), each with 3 intensity levels (a little, medium, very). |
| **Fusion Engine** | Blends mood, nutrition, and preferences to generate a recipe query. Maps emotional tone, sensory bias, and cultural flavor logic. |
| **Query Builder** | Converts fusion output into a structured API request to Edamam, filtering by nutrition, cuisine, mood tags, and allergy exclusions. |
| **Recipe Structuring Agent** | Wraps Edamam's raw recipe data into a unified schema including: ingredients with amounts, cooking directions, nutrition summary, and emotional alignment mapping. |
| **LLM Orchestration** | Receives structured recipe schema and generates: poetic recipe description, emotional fit summary, plating suggestion, journaling prompt, and a reflective rationale explaining how the dish supports the user's emotional state. |

### Workflow Summary

1. User inputs mood blend and completes personality profile  
2. Fusion Engine calculates nutrition targets and emotional tone  
3. Query Builder sends structured request to Edamam API  
4. Edamam returns recipe with nutrition data  
5. Recipe Structuring Agent parses and formats the recipe  
6. LLM generates emotionally resonant output with rationale

## Data Sources & APIs

### Primary APIs

| Source/API | Purpose | Documentation |
|------------|---------|---------------|
| **HHS Nutrition API** | Estimates recommended caloric, protein, and fiber intake based on age, gender, height, and weight | [USDA FoodData Central](https://fdc.nal.usda.gov/api-guide.html) |
| **Edamam Recipe Search API** | Retrieves recipes based on generated query, filtering for mood-aligned tags, nutrition fit, cuisine type, and exclusions | [Edamam Recipe API](https://developer.edamam.com/edamam-recipe-api) |
| **OpenRouter AI API** | Generates poetic narration, emotional alignment notes, plating suggestions, and reflective rationale explaining emotional fit | [OpenRouter API](https://openrouter.ai/docs) |

### API Requirements & Setup

#### 1. HHS Nutrition API
- **Endpoint**: `https://api.nal.usda.gov/fdc/v1/`
- **Authentication**: API Key required
- **Rate Limits**: 1,000 requests per hour
- **Use Case**: Calculate daily nutritional requirements based on user profile

#### 2. Edamam Recipe Search API
- **Endpoint**: `https://api.edamam.com/search`
- **Authentication**: App ID and App Key required
- **Rate Limits**: 10 requests per minute (free tier)
- **Use Case**: Search and retrieve recipes based on mood, nutrition, and preference filters

#### 3. OpenRouter AI API
- **Endpoint**: `https://openrouter.ai/api/v1/chat/completions`
- **Authentication**: API Key required
- **Rate Limits**: Varies by model and tier
- **Use Case**: Generate emotional descriptions, plating suggestions, and reflective content
- **Available Models**: Access to multiple LLM models (GPT-4, Claude, Llama, etc.)

**Example Usage**:
```python
import openai

# Configure for OpenRouter
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = "your_openrouter_api_key"

# Generate emotional rationale
response = openai.ChatCompletion.create(
    model="anthropic/claude-3.5-sonnet",  # or your preferred model
    messages=[
        {"role": "system", "content": "You are a poetic food writer who explains how recipes connect to emotions."},
        {"role": "user", "content": f"Explain why this recipe matches the user's mood: {mood_combination}"}
    ]
)
```

### Data Flow Architecture

```
User Input → Personality Profile → Mood Selection
     ↓
Fusion Engine → Query Builder → Edamam API
     ↓
Recipe Data → Structuring Agent → LLM Processing
     ↓
Final Recipe with Emotional Context
```

## User Flow

### 1. Onboarding
- Personal information collection (age, gender, height, weight)
- Ethnic background and cultural preferences
- Dietary restrictions and allergies
- Cuisine preferences
- Initial mood assessment

### 2. Daily Usage
- Quick mood input (1-3 moods with intensity levels)
- Recipe generation and display
- Emotional rationale presentation
- Cooking instructions and plating suggestions

### 3. Profile Management
- Update personal information
- Modify dietary preferences
- View nutrition history
- Adjust mood palette preferences

## Technical Requirements

### Backend Requirements
- **Language**: Python 3.8+
- **Framework**: FastAPI or Flask
- **Database**: PostgreSQL or MongoDB
- **Caching**: Redis for API response caching
- **Authentication**: JWT tokens

### Frontend Requirements
- **Platform**: iOS (Swift/SwiftUI)
- **State Management**: Combine framework
- **Networking**: URLSession with async/await
- **UI Components**: Custom mood selection interface

### Infrastructure
- **Hosting**: AWS/GCP/Azure
- **API Gateway**: For rate limiting and authentication
- **Monitoring**: Application performance monitoring
- **Analytics**: User behavior and recipe success tracking

## Example Output

### User Input
- **Age**: 34  
- **Gender**: Female  
- **Height**: 168 cm  
- **Weight**: 58 kg  
- **Ethnic Background**: Japanese  
- **Cuisine Preferences**: Italian, Japanese  
- **Allergies**: Peanuts  
- **Dietary Preference**: Vegetarian  
- **Mood Blend**:
  - Dreamy (Very)
  - Craving (Medium)
  - Grounded (A little)

### Recommended Dish
**Yuzu-Scented Risotto with Silken Tofu and Shiso Oil**

### Ingredients
| Ingredient         | Amount     |
|--------------------|------------|
| Arborio rice       | 150g       |
| Silken tofu        | 100g       |
| Vegetable broth    | 600ml      |
| Yuzu zest          | 1 tsp      |
| Olive oil          | 2 tbsp     |
| Shiso leaves       | 6 leaves   |
| White wine         | 50ml       |
| Garlic (minced)    | 1 clove    |
| Shallot (minced)   | 1 small    |
| Salt               | To taste   |
| Black pepper       | To taste   |

### Cooking Directions
1. Sauté garlic and shallot in olive oil until translucent.  
2. Add Arborio rice and toast gently.  
3. Deglaze with white wine and stir until absorbed.  
4. Gradually add vegetable broth, stirring until creamy.  
5. Fold in silken tofu and yuzu zest. Season to taste.  
6. Infuse shiso leaves in warm olive oil for 5 minutes.  
7. Plate risotto and drizzle with shiso oil. Garnish with fresh shiso.

### Nutrition Summary
- **Calories**: 520 kcal  
- **Protein**: 18g  
- **Fiber**: 7g

### Emotional Rationale
This dish was chosen to gently cradle your emotional state with softness, warmth, and quiet indulgence.

- **Dreamy**: The silky texture and floral brightness evoke a sense of floating—like mist over Kyoto.  
- **Craving**: The tofu's richness and citrus brightness satisfy your desire for indulgence.  
- **Grounded**: The slow, meditative preparation invites presence and calm.

Together, this recipe offers emotional nourishment: a sensory lullaby for your dreamy longing, a quiet indulgence for your craving, and a gentle anchor for your grounded self.

## Future Enhancements

### Phase 2 Features
- Social sharing of mood-inspired recipes
- Community mood boards
- Seasonal mood adjustments
- Integration with smart kitchen devices

### Phase 3 Features
- AI-powered meal planning
- Grocery list generation
- Restaurant recommendations based on mood
- Wellness tracking integration

---

*This documentation serves as the foundation for SavorMe development and will be updated as the project evolves.*
