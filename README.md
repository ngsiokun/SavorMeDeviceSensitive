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

### Mockup Files
- `recipe_suggestion_mockup.html` - Recipe display with ingredients and cooking directions
- `emotional_rationale_mockup.html` - Emotional explanation of recipe choices

### Mockup Generator
- `mockup_generator.py` - Python script to generate UI mockups
- `view_mockups.py` - Script to open mockups in browser

## 🛠️ Technical Stack

### APIs Used
- **HHS Nutrition API** - Calculate nutritional requirements
- **Edamam Recipe Search API** - Retrieve recipes based on mood and preferences
- **OpenRouter AI API** - Generate emotional descriptions and rationale

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

3. **Generate Mockups**:
   ```bash
   python mockup_generator.py
   ```

4. **View Mockups**:
   ```bash
   python view_mockups.py
   ```

## 📋 User Flow

1. **Onboarding** - Personal profile setup (age, gender, height, weight, dietary preferences)
2. **Mood Selection** - 10 mood states with 3 intensity levels each
3. **Recipe Suggestion** - Ingredients, amounts, cooking directions, dish image
4. **Emotional Rationale** - Detailed explanation of mood-recipe connection

## 🎨 Design Features

- **iPhone-optimized** (390x844px dimensions)
- **Green theme** matching health-focused aesthetic
- **Compact layout** ensuring all content fits within screen height
- **Professional typography** with proper spacing and hierarchy
- **Interactive elements** with visual feedback

## 📚 Documentation

- `documentation.md` - Complete technical documentation
- `setup_guide.md` - Setup and configuration instructions

## 🤝 Contributing

This project is part of the SavorMe mood-based recipe companion app development.

## 📄 License

This project is for development and demonstration purposes.
