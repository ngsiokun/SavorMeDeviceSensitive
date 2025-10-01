# SavorMe Canva Connect API Setup Guide

## Prerequisites

1. **Canva Developer Account**: You already have this set up with your SavorMe integration
2. **Python Environment**: Python 3.8 or higher
3. **Required Packages**: Install the dependencies

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in your project root with the following variables:
   ```
CANVA_CLIENT_ID=your_client_id_here
CANVA_CLIENT_SECRET=your_client_secret_here
CANVA_ACCESS_TOKEN=your_access_token_here

# OpenRouter AI API (for LLM functionality)
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet  # or your preferred model

# Hugging Face API (for image generation)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Edamam Recipe API
EDAMAM_APP_ID=your_edamam_app_id
EDAMAM_APP_KEY=your_edamam_app_key

# HHS Nutrition API
HHS_API_KEY=your_hhs_api_key
   REDIRECT_URI=http://127.0.0.1:3001/oauth/redirect
   RETURN_URL=http://127.0.0.1:3001/return-nav
   ```

3. **Get Your Credentials**:
   - Go to your Canva Developer Portal: https://canva.com/developers/integrations/connect-api/OC-AZI8LZejb8u/configuration
   - Copy your Client ID and Client Secret from the "Credentials" section
   - Set up OAuth flow to get your access token

## Usage

### Generate Final Mockups:
```bash
python final_mockup_generator.py
```

### View Final Mockups:
```bash
python view_final_mockups.py
```

This will create 2 final smartphone-optimized mockups:
1. **Mood Selection Screen** - The main mood input interface with 10 mood options
2. **Emotional Rationale Screen** - Complete recipe explanation with nutrition comparison

## Final Mockup Features

### Mood Selection Screen (v2.0 - Evidence-Based)
- **4 mood options** with scientific evidence badges (Stressed, Fatigued, Low Mood, Irritable)
- Evidence level indicators (⭐⭐⭐ to ⭐⭐⭐⭐⭐)
- Mood aliases for better identification (e.g., "Anxious, Wired, Overwhelmed")
- Intensity level selection (A little, Medium, Very)
- Generate button to trigger recipe creation
- iPhone-optimized dimensions (393x852px)
- Clean 2×2 grid layout (instead of 5×2)

### Emotional Rationale Screen
- Recipe summary with nutrition information
- Emotional rationale explanation
- Nutrition comparison table (recipe vs. daily intake)
- Mood breakdown with individual explanations
- Mood Meals journal for user reflection
- Action buttons (Back to Home, Share Recipe)
- iPhone-optimized dimensions with all content visible

## API Integration Notes

The mockup system uses the Canva Connect API to:
- Create new designs programmatically
- Add text and shape elements
- Apply styling and positioning
- Generate visual representations of the SavorMe UI

## Troubleshooting

1. **Authentication Issues**: Ensure your access token is valid and has the correct scopes
2. **API Limits**: Check your Canva API rate limits
3. **Element Positioning**: Adjust x,y coordinates in the elements array if needed
4. **Styling**: Modify colors, fonts, and sizes in the style objects

## Next Steps

1. Run the mockup generator to create initial designs
2. Review the generated designs in your Canva account
3. Refine the designs manually in Canva
4. Export high-quality images for development reference
5. Use the designs as templates for your iOS app development
