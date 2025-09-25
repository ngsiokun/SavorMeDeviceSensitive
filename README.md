# SavorMe – Mood-Based Recipe Companion

SavorMe is an iOS app that curates recipes based on a user's emotional state, nutritional needs, and culinary preferences. It blends mood input, personality profile, and cultural context to deliver meals that comfort, excite, or indulge—each paired with poetic narration and sensory resonance.

## 🎯 Project Overview

SavorMe creates a bridge between emotional state and culinary choice by:
- Capturing user mood through an intuitive interface
- Building comprehensive personality profiles  
- Leveraging AI to generate emotionally resonant recipe descriptions
- Providing nutritional guidance that aligns with both health and emotional needs

## 📱 UI Mockups

This repository contains iPhone-optimized UI mockups for the SavorMe app, created with a green theme matching modern health-focused design aesthetics.

### Final Mockup Files
- `mood_selection_mockup.html` - Mood selection screen with 10 mood options and intensity levels
- `emotional_rationale_mockup.html` - Complete emotional rationale with nutrition comparison

### Mockup Generator
- `final_mockup_generator.py` - Python script to generate final UI mockups
- `view_final_mockups.py` - Script to open final mockups in browser

## 🛠️ Technical Stack

### APIs Used
- **HHS Nutrition API** - Calculate nutritional requirements and daily intake recommendations
- **Edamam Recipe Search API** - Retrieve recipes based on mood and preferences
- **OpenRouter AI API** - Generate emotional descriptions and rationale
- **Hugging Face Stable Diffusion API** - Generate simulated serving images
- **Mood Meals Journal** - Store user reflections for adaptive personalization

### Development Tools
- Python 3.8+ for mockup generation
- HTML/CSS for responsive iPhone mockups
- Canva Connect API for design integration

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**:
   Create a `.env` file with your API credentials (see `setup_guide.md`)

3. **Generate Final Mockups**:
   ```bash
   python final_mockup_generator.py
   ```

4. **View Final Mockups**:
   ```bash
   python view_final_mockups.py
   ```

## 📋 User Flow

1. **Onboarding** - Personal profile setup (age, gender, height, weight, dietary preferences)
2. **Nutrition Calculation** - HHS API calculates recommended daily intake for your profile
3. **Mood Selection** - 10 mood states with 3 intensity levels each
4. **Recipe Suggestion** - Ingredients, amounts, cooking directions, AI-generated serving image
5. **Emotional Rationale** - Detailed explanation of mood-recipe connection
6. **Nutrition Comparison** - Recipe nutrition vs. your recommended daily intake
7. **Mood Meals Journal** - Reflection and feedback for adaptive personalization

## 🎨 Design Features

- **iPhone-optimized** (393x852px dimensions)
- **Green theme** matching health-focused aesthetic
- **Compact layout** ensuring all content fits within screen height
- **Professional typography** with proper spacing and hierarchy
- **Interactive elements** with visual feedback

## 📚 Documentation

- `documentation.md` - Complete technical documentation
- `workflow.md` - End-to-end workflow and process flow
- `example_output.md` - Example recipe output with all features
- `setup_guide.md` - Setup and configuration instructions

## 🤝 Contributing

This project is part of the SavorMe mood-based recipe companion app development.

## 📄 License

This project is for development and demonstration purposes.
