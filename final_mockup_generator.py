"""
SavorMe Super Ultra-Compact Smartphone Mockup Generator
Creates mobile-first mockups that fit perfectly within iPhone screen height
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class SavorMeSuperUltraCompactMockup:
    def __init__(self):
        # iPhone 14 Pro dimensions: 393 x 852 points
        self.iphone_width = 393
        self.iphone_height = 852
        print("Creating super ultra-compact smartphone-optimized SavorMe mockups...")
    
    def create_super_ultra_compact_mood_selection_screen(self) -> str:
        """Create super ultra-compact smartphone-optimized mood selection screen"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SavorMe - Mood Selection</title>
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
            padding: 8px;
            box-shadow: 0 0 30px rgba(0,0,0,0.3);
            position: relative;
            display: flex;
            flex-direction: column;
        }}
        .status-bar {{
            height: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 10px;
            font-weight: 600;
            color: #000;
            margin-bottom: 8px;
        }}
        .content {{
            flex: 1;
            display: flex;
            flex-direction: column;
        }}
        .header {{
            text-align: center;
            margin-bottom: 8px;
        }}
        .title {{
            font-size: 16px;
            font-weight: bold;
            color: #065F46;
            margin-bottom: 2px;
        }}
        .subtitle {{
            font-size: 10px;
            color: #10B981;
            margin-bottom: 8px;
        }}
        .mood-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 4px;
            margin-bottom: 8px;
            flex: 1;
            overflow: hidden;
        }}
        .mood-button {{
            padding: 6px 4px;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            border: 2px solid;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 10px;
            min-height: 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 2px;
        }}
        .mood-button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .mood-button.selected {{
            transform: scale(1.01);
            box-shadow: 0 3px 12px rgba(0,0,0,0.15);
        }}
        .mood-emoji {{
            font-size: 14px;
        }}
        .mood-name {{
            font-size: 9px;
            line-height: 1.0;
        }}
        .dreamy {{ background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%); border-color: #10B981; color: #065F46; }}
        .fiery {{ background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%); border-color: #EF4444; color: #991B1B; }}
        .focused {{ background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border-color: #3B82F6; color: #1E40AF; }}
        .playful {{ background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); border-color: #F59E0B; color: #92400E; }}
        .craving {{ background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%); border-color: #8B5CF6; color: #6B21A8; }}
        .light {{ background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); border-color: #22C55E; color: #166534; }}
        .grounded {{ background: linear-gradient(135deg, #FAF5FF 0%, #F3E8FF 100%); border-color: #A855F7; color: #7C2D12; }}
        .restorative {{ background: linear-gradient(135deg, #FFF5F5 0%, #FED7D7 100%); border-color: #F56565; color: #C53030; }}
        .charismatic {{ background: linear-gradient(135deg, #FFFAF0 0%, #FED7AA 100%); border-color: #ED8936; color: #C05621; }}
        .melancholy {{ background: linear-gradient(135deg, #F7FAFC 0%, #EDF2F7 100%); border-color: #A0AEC0; color: #4A5568; }}
        .intensity-section {{
            background: #F0FDF4;
            border-radius: 8px;
            padding: 6px;
            margin-bottom: 8px;
            border: 2px solid #BBF7D0;
        }}
        .intensity-title {{
            font-size: 10px;
            font-weight: 600;
            color: #065F46;
            text-align: center;
            margin-bottom: 4px;
        }}
        .intensity-options {{
            display: flex;
            justify-content: space-around;
            gap: 4px;
        }}
        .intensity-option {{
            flex: 1;
            padding: 4px 6px;
            border-radius: 12px;
            text-align: center;
            font-size: 9px;
            font-weight: 500;
            background: white;
            border: 2px solid #10B981;
            color: #065F46;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .intensity-option.selected {{
            background: #10B981;
            color: white;
        }}
        .generate-button {{
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            color: white;
            border: none;
            border-radius: 15px;
            padding: 8px;
            font-size: 12px;
            font-weight: bold;
            width: 100%;
            cursor: pointer;
            box-shadow: 0 3px 10px rgba(16, 185, 129, 0.3);
            transition: all 0.3s ease;
        }}
        .generate-button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        }}
        .progress-indicator {{
            display: flex;
            justify-content: center;
            gap: 4px;
            margin-top: 6px;
        }}
        .progress-dot {{
            width: 4px;
            height: 4px;
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
                <div class="title">How are you feeling today?</div>
                <div class="subtitle">Select up to 3 moods that resonate with you</div>
            </div>
            
            <div class="mood-grid">
                <div class="mood-button dreamy selected">
                    <div class="mood-emoji">😌</div>
                    <div class="mood-name">Dreamy</div>
                </div>
                <div class="mood-button fiery">
                    <div class="mood-emoji">🔥</div>
                    <div class="mood-name">Fiery</div>
                </div>
                <div class="mood-button focused">
                    <div class="mood-emoji">🎯</div>
                    <div class="mood-name">Focused</div>
                </div>
                <div class="mood-button playful">
                    <div class="mood-emoji">🎨</div>
                    <div class="mood-name">Playful</div>
                </div>
                <div class="mood-button craving selected">
                    <div class="mood-emoji">🍯</div>
                    <div class="mood-name">Craving</div>
                </div>
                <div class="mood-button light">
                    <div class="mood-emoji">✨</div>
                    <div class="mood-name">Light</div>
                </div>
                <div class="mood-button grounded">
                    <div class="mood-emoji">🌱</div>
                    <div class="mood-name">Grounded</div>
                </div>
                <div class="mood-button restorative">
                    <div class="mood-emoji">💚</div>
                    <div class="mood-name">Restorative</div>
                </div>
                <div class="mood-button charismatic">
                    <div class="mood-emoji">💫</div>
                    <div class="mood-name">Charismatic</div>
                </div>
                <div class="mood-button melancholy">
                    <div class="mood-emoji">🌙</div>
                    <div class="mood-name">Melancholy</div>
                </div>
            </div>
            
            <div class="intensity-section">
                <div class="intensity-title">Intensity Level</div>
                <div class="intensity-options">
                    <div class="intensity-option">A little</div>
                    <div class="intensity-option selected">Medium</div>
                    <div class="intensity-option">Very</div>
                </div>
            </div>
            
            <button class="generate-button">🍽️ Generate My Recipe</button>
            
            <div class="progress-indicator">
                <div class="progress-dot"></div>
                <div class="progress-dot active"></div>
                <div class="progress-dot"></div>
                <div class="progress-dot"></div>
            </div>
        </div>
    </div>
</body>
</html>
        """
    
    def create_super_ultra_compact_emotional_rationale_screen(self) -> str:
        """Create super ultra-compact smartphone-optimized emotional rationale screen"""
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
            padding: 8px;
            box-shadow: 0 0 30px rgba(0,0,0,0.3);
            position: relative;
            display: flex;
            flex-direction: column;
        }}
        .status-bar {{
            height: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 10px;
            font-weight: 600;
            color: #000;
            margin-bottom: 8px;
        }}
        .content {{
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        .header {{
            text-align: center;
            margin-bottom: 8px;
        }}
        .title {{
            font-size: 16px;
            font-weight: bold;
            color: #065F46;
            margin-bottom: 2px;
        }}
        .subtitle {{
            font-size: 10px;
            color: #10B981;
            margin-bottom: 6px;
        }}
        .recipe-summary {{
            background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
            border-radius: 8px;
            padding: 6px;
            margin-bottom: 8px;
            border: 2px solid #10B981;
            text-align: center;
        }}
        .recipe-name {{
            font-size: 12px;
            font-weight: bold;
            color: #065F46;
            margin-bottom: 2px;
        }}
        .nutrition-info {{
            font-size: 9px;
            color: #10B981;
            font-weight: 600;
        }}
        .rationale-section {{
            margin-bottom: 8px;
        }}
        .section-title {{
            font-size: 10px;
            font-weight: 600;
            color: #10B981;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 2px;
        }}
        .rationale-content {{
            background: #F9FAFB;
            border-radius: 6px;
            padding: 6px;
            border-left: 2px solid #10B981;
            line-height: 1.2;
            font-size: 9px;
            color: #374151;
        }}
        .nutrition-comparison {{
            background: #F0FDF4;
            border-radius: 6px;
            padding: 6px;
            margin-bottom: 8px;
            border: 1px solid #BBF7D0;
        }}
        .nutrition-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 8px;
        }}
        .nutrition-table th {{
            background: #10B981;
            color: white;
            padding: 3px;
            text-align: left;
            font-weight: 600;
        }}
        .nutrition-table td {{
            padding: 3px;
            border-bottom: 1px solid #E5E7EB;
        }}
        .nutrition-table tr:last-child td {{
            border-bottom: none;
        }}
        .mood-breakdown {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            margin-bottom: 8px;
        }}
        .mood-item {{
            background: white;
            border-radius: 6px;
            padding: 4px;
            border: 1px solid #E5E7EB;
            transition: all 0.3s ease;
        }}
        .mood-item:hover {{
            border-color: #10B981;
            box-shadow: 0 2px 6px rgba(16, 185, 129, 0.1);
        }}
        .mood-header {{
            display: flex;
            align-items: center;
            gap: 3px;
            margin-bottom: 2px;
        }}
        .mood-emoji {{
            font-size: 10px;
        }}
        .mood-name {{
            font-size: 8px;
            font-weight: 600;
            color: #065F46;
            flex: 1;
        }}
        .mood-intensity {{
            font-size: 7px;
            color: #10B981;
            background: #F0FDF4;
            padding: 1px 3px;
            border-radius: 4px;
        }}
        .mood-explanation {{
            font-size: 7px;
            color: #374151;
            line-height: 1.1;
        }}
        .journal-section {{
            background: #FFFBEB;
            border-radius: 6px;
            padding: 6px;
            margin-bottom: 8px;
            border: 1px solid #FEF3C7;
        }}
        .journal-prompt {{
            font-size: 8px;
            color: #92400E;
            font-weight: 600;
            margin-bottom: 3px;
        }}
        .journal-input {{
            width: 100%;
            padding: 4px;
            border: 1px solid #F3E8FF;
            border-radius: 4px;
            font-size: 8px;
            resize: vertical;
            min-height: 20px;
        }}
        .action-buttons {{
            display: flex;
            gap: 4px;
            margin-top: auto;
            padding-top: 8px;
        }}
        .primary-button {{
            flex: 1;
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            color: white;
            border: none;
            border-radius: 15px;
            padding: 6px;
            font-size: 9px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 3px 10px rgba(16, 185, 129, 0.3);
            transition: all 0.3s ease;
        }}
        .secondary-button {{
            flex: 1;
            background: white;
            color: #10B981;
            border: 2px solid #10B981;
            border-radius: 15px;
            padding: 6px;
            font-size: 9px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .primary-button:hover, .secondary-button:hover {{
            transform: translateY(-1px);
        }}
        .progress-indicator {{
            display: flex;
            justify-content: center;
            gap: 4px;
            margin-top: 6px;
        }}
        .progress-dot {{
            width: 4px;
            height: 4px;
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
                <div class="recipe-name">🍜 Citrus Blossom Risotto</div>
                <div class="nutrition-info">540 kcal • 22g protein • 7g fiber</div>
            </div>
            
            <div class="rationale-section">
                <div class="section-title">
                    <span>💭</span>
                    <span>Emotional Rationale</span>
                </div>
                <div class="rationale-content">
                    This dish was chosen to evoke softness and indulgence, with gentle anchoring. The citrus and floral notes awaken longing, while creamy textures soothe and center.
                </div>
            </div>
            
            <div class="nutrition-comparison">
                <div class="section-title">
                    <span>🧪</span>
                    <span>Nutrition Comparison</span>
                </div>
                <table class="nutrition-table">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>This Dish</th>
                            <th>Your Daily</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Calories</td>
                            <td>540 kcal</td>
                            <td>1,860 kcal</td>
                        </tr>
                        <tr>
                            <td>Protein</td>
                            <td>22 g</td>
                            <td>84 g</td>
                        </tr>
                        <tr>
                            <td>Fiber</td>
                            <td>7 g</td>
                            <td>24 g</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="mood-breakdown">
                <div class="mood-item">
                    <div class="mood-header">
                        <div class="mood-emoji">😌</div>
                        <div class="mood-name">Dreamy (Very)</div>
                        <div class="mood-intensity">Very</div>
                    </div>
                    <div class="mood-explanation">The silky texture and floral brightness evoke a sense of floating—like mist over Kyoto.</div>
                </div>
                
                <div class="mood-item">
                    <div class="mood-header">
                        <div class="mood-emoji">🍯</div>
                        <div class="mood-name">Craving (Medium)</div>
                        <div class="mood-intensity">Medium</div>
                    </div>
                    <div class="mood-explanation">The coconut cream's richness and citrus brightness satisfy your desire for indulgence.</div>
                </div>
                
                <div class="mood-item">
                    <div class="mood-header">
                        <div class="mood-emoji">🌱</div>
                        <div class="mood-name">Grounded (A little)</div>
                        <div class="mood-intensity">A little</div>
                    </div>
                    <div class="mood-explanation">The slow, meditative preparation invites presence and calm.</div>
                </div>
            </div>
            
            <div class="journal-section">
                <div class="journal-prompt">📝 How did this dish make you feel?</div>
                <textarea class="journal-input" placeholder="Share your thoughts..."></textarea>
            </div>
            
            <div class="action-buttons">
                <button class="primary-button">🏠 Back to Home</button>
                <button class="secondary-button">📱 Share</button>
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
    
    def create_all_super_ultra_compact_mockups(self):
        """Create all super ultra-compact smartphone-optimized SavorMe mockups"""
        print("Creating super ultra-compact smartphone-optimized SavorMe mockups...")
        
        # Create HTML mockups
        mood_html = self.create_super_ultra_compact_mood_selection_screen()
        with open("mood_selection_mockup.html", "w", encoding="utf-8") as f:
            f.write(mood_html)
        
        rationale_html = self.create_super_ultra_compact_emotional_rationale_screen()
        with open("emotional_rationale_mockup.html", "w", encoding="utf-8") as f:
            f.write(rationale_html)
        
        print("Final smartphone-optimized HTML mockups created successfully!")
        print("Files created:")
        print("- mood_selection_mockup.html")
        print("- emotional_rationale_mockup.html")

def main():
    """Main function to create super ultra-compact smartphone mockups"""
    print("SavorMe Super Ultra-Compact Smartphone Mockup Generator")
    print("=" * 50)
    
    mockup_generator = SavorMeSuperUltraCompactMockup()
    mockup_generator.create_all_super_ultra_compact_mockups()

if __name__ == "__main__":
    main()
