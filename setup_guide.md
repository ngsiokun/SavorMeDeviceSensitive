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
   REDIRECT_URI=http://127.0.0.1:3001/oauth/redirect
   RETURN_URL=http://127.0.0.1:3001/return-nav
   ```

3. **Get Your Credentials**:
   - Go to your Canva Developer Portal: https://canva.com/developers/integrations/connect-api/OC-AZI8LZejb8u/configuration
   - Copy your Client ID and Client Secret from the "Credentials" section
   - Set up OAuth flow to get your access token

## Usage

Run the mockup generator:
```bash
python mockup.py
```

This will create 4 mockup designs in your Canva account:
1. **Mood Selection Screen** - The main mood input interface
2. **Personality Profile Setup** - User onboarding form
3. **Recipe Results Screen** - Display of generated recipes
4. **Main Dashboard** - Home screen with quick access

## Mockup Features

### Mood Selection Screen
- 10 mood options with color-coded themes
- Intensity level selection (A little, Medium, Very)
- Generate button to trigger recipe creation

### Personality Profile Setup
- Personal information fields (age, height, weight)
- Dietary preferences and allergies
- Cuisine preferences selection
- Continue button for onboarding flow

### Recipe Results Screen
- Recipe title and mood alignment
- Emotional rationale explanation
- Key ingredients list
- Nutrition information
- Action buttons (View Full Recipe, Save Recipe)

### Main Dashboard
- Welcome message
- Quick mood selection
- Recent recipes display
- Profile management options

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
