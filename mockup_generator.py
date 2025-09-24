"""
SavorMe Final Compact Mockup Generator
Creates iPhone mockups with shorter, more concise text
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class SavorMeFinalCompactMockup:
    def __init__(self):
        # iPhone 13/14 dimensions: 390 x 844 points
        self.iphone_width = 390
        self.iphone_height = 844
        print("Creating final compact iPhone-optimized SavorMe mockups...")
    
    def create_recipe_suggestion_html(self) -> str:
        """Create compact recipe suggestion screen with shorter text"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SavorMe - Recipe Suggestion</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            width: {self.iphone_width}px;
            height: {self.iphone_height}px;
            background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%);
            overflow: hidden;
            position: relative;
        }}
        .phone-container {{
            width: 100%;
            height: 100%;
            background: white;
            border-radius: 40px;
            padding: 15px;
            box-shadow: 0 0 30px rgba(0,0,0,0.3);
            position: relative;
            display: flex;
            flex-direction: column;
        }}
        .status-bar {{
            height: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            font-weight: 600;
            color: #000;
            margin-bottom: 15px;
        }}
        .content {{
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }}
        .recipe-image {{
            width: 100%;
            height: 150px;
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 32px;
            margin-bottom: 12px;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        }}
        .recipe-title {{
            font-size: 16px;
            font-weight: bold;
            color: #065F46;
            text-align: center;
            margin-bottom: 6px;
            line-height: 1.2;
            padding: 0 5px;
        }}
        .mood-indicator {{
            font-size: 11px;
            color: #10B981;
            text-align: center;
            margin-bottom: 15px;
            background: #F0FDF4;
            padding: 6px 12px;
            border-radius: 12px;
            border: 1px solid #BBF7D0;
        }}
        .section {{
            margin-bottom: 15px;
        }}
        .section-title {{
            font-size: 14px;
            font-weight: 600;
            color: #10B981;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        .ingredients-list {{
            background: #F9FAFB;
            border-radius: 8px;
            padding: 10px;
            border-left: 3px solid #10B981;
        }}
        .ingredient-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 4px 0;
            border-bottom: 1px solid #E5E7EB;
            font-size: 12px;
        }}
        .ingredient-item:last-child {{
            border-bottom: none;
        }}
        .ingredient-name {{
            color: #374151;
            font-weight: 500;
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .ingredient-amount {{
            color: #10B981;
            font-weight: 600;
            margin-left: 6px;
        }}
        .cooking-directions {{
            background: #F0FDF4;
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #BBF7D0;
        }}
        .direction-step {{
            display: flex;
            gap: 8px;
            margin-bottom: 8px;
            font-size: 11px;
            line-height: 1.3;
        }}
        .step-number {{
            background: #10B981;
            color: white;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 9px;
            font-weight: bold;
            flex-shrink: 0;
        }}
        .step-text {{
            color: #374151;
            flex: 1;
        }}
        .action-buttons {{
            display: flex;
            gap: 6px;
            margin-top: auto;
            padding-top: 12px;
        }}
        .primary-button {{
            flex: 1;
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            color: white;
            border: none;
            border-radius: 20px;
            padding: 12px;
            font-size: 12px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
            transition: all 0.3s ease;
        }}
        .secondary-button {{
            flex: 1;
            background: white;
            color: #10B981;
            border: 2px solid #10B981;
            border-radius: 20px;
            padding: 12px;
            font-size: 12px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .primary-button:hover, .secondary-button:hover {{
            transform: translateY(-2px);
        }}
        .progress-indicator {{
            display: flex;
            justify-content: center;
            gap: 5px;
            margin-top: 10px;
        }}
        .progress-dot {{
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background-color: #D1FAE5;
        }}
        .progress-dot.active {{
            background-color: #10B981;
        }}
    </style>
</head>
<body>
    <div class="phone-container">
        <div class="status-bar">
            <span>9:41</span>
            <span>🔋 100%</span>
        </div>
        
        <div class="content">
            <div class="recipe-image">🍜</div>
            
            <div class="recipe-title">Yuzu Risotto with Tofu & Shiso</div>
            
            <div class="mood-indicator">Perfect for: Dreamy + Craving + Grounded</div>
            
            <div class="section">
                <div class="section-title">
                    <span>🥘</span>
                    <span>Ingredients</span>
                </div>
                <div class="ingredients-list">
                    <div class="ingredient-item">
                        <span class="ingredient-name">Arborio rice</span>
                        <span class="ingredient-amount">150g</span>
                    </div>
                    <div class="ingredient-item">
                        <span class="ingredient-name">Silken tofu</span>
                        <span class="ingredient-amount">100g</span>
                    </div>
                    <div class="ingredient-item">
                        <span class="ingredient-name">Vegetable broth</span>
                        <span class="ingredient-amount">600ml</span>
                    </div>
                    <div class="ingredient-item">
                        <span class="ingredient-name">Yuzu zest</span>
                        <span class="ingredient-amount">1 tsp</span>
                    </div>
                    <div class="ingredient-item">
                        <span class="ingredient-name">Shiso leaves</span>
                        <span class="ingredient-amount">6 leaves</span>
                    </div>
                    <div class="ingredient-item">
                        <span class="ingredient-name">Olive oil</span>
                        <span class="ingredient-amount">2 tbsp</span>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">
                    <span>👨‍🍳</span>
                    <span>Cooking Directions</span>
                </div>
                <div class="cooking-directions">
                    <div class="direction-step">
                        <div class="step-number">1</div>
                        <div class="step-text">Sauté garlic and shallot in olive oil</div>
                    </div>
                    <div class="direction-step">
                        <div class="step-number">2</div>
                        <div class="step-text">Add rice and toast for 2 minutes</div>
                    </div>
                    <div class="direction-step">
                        <div class="step-number">3</div>
                        <div class="step-text">Add wine and stir until absorbed</div>
                    </div>
                    <div class="direction-step">
                        <div class="step-number">4</div>
                        <div class="step-text">Add broth gradually, stirring until creamy</div>
                    </div>
                    <div class="direction-step">
                        <div class="step-number">5</div>
                        <div class="step-text">Fold in tofu and yuzu zest</div>
                    </div>
                    <div class="direction-step">
                        <div class="step-number">6</div>
                        <div class="step-text">Infuse shiso in warm oil for 5 min</div>
                    </div>
                    <div class="direction-step">
                        <div class="step-number">7</div>
                        <div class="step-text">Plate and drizzle with shiso oil</div>
                    </div>
                </div>
            </div>
            
            <div class="action-buttons">
                <button class="primary-button">💡 Why This Recipe?</button>
                <button class="secondary-button">💾 Save Recipe</button>
            </div>
            
            <div class="progress-indicator">
                <div class="progress-dot"></div>
                <div class="progress-dot"></div>
                <div class="progress-dot active"></div>
                <div class="progress-dot"></div>
            </div>
        </div>
    </div>
</body>
</html>
        """
    
    def create_emotional_rationale_html(self) -> str:
        """Create compact emotional rationale screen with shorter text"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SavorMe - Why This Recipe?</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            width: {self.iphone_width}px;
            height: {self.iphone_height}px;
            background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%);
            overflow: hidden;
            position: relative;
        }}
        .phone-container {{
            width: 100%;
            height: 100%;
            background: white;
            border-radius: 40px;
            padding: 15px;
            box-shadow: 0 0 30px rgba(0,0,0,0.3);
            position: relative;
            display: flex;
            flex-direction: column;
        }}
        .status-bar {{
            height: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            font-weight: 600;
            color: #000;
            margin-bottom: 15px;
        }}
        .content {{
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .title {{
            font-size: 20px;
            font-weight: bold;
            color: #065F46;
            margin-bottom: 6px;
        }}
        .subtitle {{
            font-size: 12px;
            color: #10B981;
            margin-bottom: 12px;
        }}
        .recipe-summary {{
            background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 15px;
            border: 2px solid #10B981;
            text-align: center;
        }}
        .recipe-name {{
            font-size: 14px;
            font-weight: bold;
            color: #065F46;
            margin-bottom: 6px;
            line-height: 1.2;
        }}
        .nutrition-info {{
            font-size: 11px;
            color: #10B981;
            font-weight: 600;
        }}
        .rationale-section {{
            margin-bottom: 15px;
        }}
        .section-title {{
            font-size: 14px;
            font-weight: 600;
            color: #10B981;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        .rationale-content {{
            background: #F9FAFB;
            border-radius: 8px;
            padding: 12px;
            border-left: 3px solid #10B981;
            line-height: 1.4;
            font-size: 12px;
            color: #374151;
        }}
        .mood-breakdown {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 15px;
        }}
        .mood-item {{
            background: white;
            border-radius: 8px;
            padding: 10px;
            border: 2px solid #E5E7EB;
            transition: all 0.3s ease;
        }}
        .mood-item:hover {{
            border-color: #10B981;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);
        }}
        .mood-header {{
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 6px;
        }}
        .mood-emoji {{
            font-size: 14px;
        }}
        .mood-name {{
            font-size: 12px;
            font-weight: 600;
            color: #065F46;
            flex: 1;
        }}
        .mood-intensity {{
            font-size: 9px;
            color: #10B981;
            background: #F0FDF4;
            padding: 2px 4px;
            border-radius: 6px;
        }}
        .mood-explanation {{
            font-size: 11px;
            color: #374151;
            line-height: 1.3;
        }}
        .action-buttons {{
            display: flex;
            gap: 6px;
            margin-top: auto;
            padding-top: 12px;
        }}
        .primary-button {{
            flex: 1;
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            color: white;
            border: none;
            border-radius: 20px;
            padding: 12px;
            font-size: 12px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
            transition: all 0.3s ease;
        }}
        .secondary-button {{
            flex: 1;
            background: white;
            color: #10B981;
            border: 2px solid #10B981;
            border-radius: 20px;
            padding: 12px;
            font-size: 12px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .primary-button:hover, .secondary-button:hover {{
            transform: translateY(-2px);
        }}
        .progress-indicator {{
            display: flex;
            justify-content: center;
            gap: 5px;
            margin-top: 10px;
        }}
        .progress-dot {{
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background-color: #D1FAE5;
        }}
        .progress-dot.active {{
            background-color: #10B981;
        }}
    </style>
</head>
<body>
    <div class="phone-container">
        <div class="status-bar">
            <span>9:41</span>
            <span>🔋 100%</span>
        </div>
        
        <div class="content">
            <div class="header">
                <div class="title">Why This Recipe?</div>
                <div class="subtitle">Understanding the emotional connection</div>
            </div>
            
            <div class="recipe-summary">
                <div class="recipe-name">🍜 Yuzu Risotto with Tofu & Shiso</div>
                <div class="nutrition-info">520 kcal • 18g protein • 7g fiber</div>
            </div>
            
            <div class="rationale-section">
                <div class="section-title">
                    <span>💭</span>
                    <span>Emotional Rationale</span>
                </div>
                <div class="rationale-content">
                    This dish gently cradles your emotional state with softness, warmth, and quiet indulgence. The silky texture and floral brightness evoke a sense of floating—like mist over Kyoto. Together, this recipe offers emotional nourishment: a sensory lullaby for your dreamy longing, a quiet indulgence for your craving, and a gentle anchor for your grounded self.
                </div>
            </div>
            
            <div class="mood-breakdown">
                <div class="mood-item">
                    <div class="mood-header">
                        <div class="mood-emoji">😌</div>
                        <div class="mood-name">Dreamy (Very)</div>
                        <div class="mood-intensity">Very</div>
                    </div>
                    <div class="mood-explanation">The silky texture and floral brightness evoke a sense of floating—like mist over Kyoto. The yuzu zest adds a dreamy, ethereal quality.</div>
                </div>
                
                <div class="mood-item">
                    <div class="mood-header">
                        <div class="mood-emoji">🍯</div>
                        <div class="mood-name">Craving (Medium)</div>
                        <div class="mood-intensity">Medium</div>
                    </div>
                    <div class="mood-explanation">The tofu's richness and citrus brightness satisfy your desire for indulgence. The creamy risotto provides sensory satisfaction.</div>
                </div>
                
                <div class="mood-item">
                    <div class="mood-header">
                        <div class="mood-emoji">🌱</div>
                        <div class="mood-name">Grounded (A little)</div>
                        <div class="mood-intensity">A little</div>
                    </div>
                    <div class="mood-explanation">The slow, meditative preparation invites presence and calm. The earthy shiso oil provides gentle grounding.</div>
                </div>
            </div>
            
            <div class="action-buttons">
                <button class="primary-button">🏠 Back to Home</button>
                <button class="secondary-button">📱 Share Recipe</button>
            </div>
            
            <div class="progress-indicator">
                <div class="progress-dot"></div>
                <div class="progress-dot"></div>
                <div class="progress-dot"></div>
                <div class="progress-dot active"></div>
            </div>
        </div>
    </div>
</body>
</html>
        """
    
    def create_all_final_mockups(self):
        """Create all final compact iPhone-optimized SavorMe mockups"""
        print("Creating final compact iPhone-optimized SavorMe mockups...")
        
        # Create HTML mockups
        recipe_html = self.create_recipe_suggestion_html()
        with open("final_recipe_suggestion_mockup.html", "w", encoding="utf-8") as f:
            f.write(recipe_html)
        
        rationale_html = self.create_emotional_rationale_html()
        with open("final_emotional_rationale_mockup.html", "w", encoding="utf-8") as f:
            f.write(rationale_html)
        
        print("Final compact iPhone-optimized HTML mockups created successfully!")
        print("Files created:")
        print("- final_recipe_suggestion_mockup.html")
        print("- final_emotional_rationale_mockup.html")

def main():
    """Main function to create final compact iPhone mockups"""
    print("SavorMe Final Compact iPhone Mockup Generator")
    print("=" * 50)
    
    mockup_generator = SavorMeFinalCompactMockup()
    mockup_generator.create_all_final_mockups()

if __name__ == "__main__":
    main()
