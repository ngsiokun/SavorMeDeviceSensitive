# SavorMe – End-to-End Workflow

## 1. Personal Profile Input

- User enters gender, age, height, and weight via the UI
- Optional fields: ethnic background, dietary preferences, allergies, cuisine preferences

## 2. Nutrition Target Calculation

- Profile data is sent to the HHS Nutrition API (US NUS)
- API returns recommended daily intake for:
  - Calories
  - Protein
  - Fiber
- These values are stored and displayed as **recommended daily intake for your profile**

## 3. Mood Input

- User selects up to 3 moods from a curated palette of 10
- Each mood includes intensity: A little, Medium, Very
- Mood blend is mapped to emotional tone, sensory bias, and culinary style

## 4. Recipe Query Generation

- Fusion Engine combines:
  - Nutrition targets from HHS API
  - Mood blend and intensity
  - Dietary and cuisine preferences
- Structured query is sent to Edamam Recipe Search API
- Filters applied: nutrition range, cuisine type, exclusions

## 5. Recipe Retrieval & Structuring

- Edamam returns matching recipe(s)
- Supervisor agent wraps recipe data into structured schema:
  - Ingredients with amounts
  - Cooking directions
  - Nutrition summary (calories, protein, fiber)
- Prompt crafted for LLM orchestration

## 6. LLM Response Generation

- LLM receives structured recipe schema and prompt
- Generates emotionally resonant output including:
  - Recommended recipe with nutrition info
  - Cooking directions (step-by-step)
  - Emotional rationale: "Why this dish was chosen for you"
  - **Recommended daily intake for your profile** for comparison

## 7. Serving Image Generation

- LLM generates poetic prompt based on mood blend and plating suggestion
- Prompt sent to Hugging Face Inference API hosting Stable Diffusion
- API returns simulated serving image styled to reflect emotional tone
- Image embedded in recipe output and summary page
- Optional fallback: curated image library tagged by mood + cuisine

## 8. Summary & Reflection

- Summary page presented to user:
  - Emotional alignment explanation
  - Plating suggestion
  - Simulated serving image
  - Nutrition comparison: actual dish vs. recommended daily intake
  - Optional journaling prompt: "How did this dish make you feel?"
- Entry autosaved to Mood Meals journal
- Feedback loop informs future personalization

## 9. Agent Collaboration

- Supervisor agent coordinates:
  - HHS Nutrition API for intake targets
  - Edamam API for recipe sourcing
  - LLM for poetic narration and emotional rationale
  - Hugging Face Stable Diffusion API for serving image generation
- Ensures cohesive, emotionally intelligent response to user

## 10. Mood Meals Journal

- User reflections are stored for adaptive personalization
- Tracks emotional responses to recipes over time
- Informs future recipe recommendations
- Provides insights into mood-food connections
