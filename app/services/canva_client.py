"""
Canva Connect API Client for Design Generation
https://www.canva.com/developers/docs/connect-api/
"""
import requests
from typing import Dict, List, Optional, Any
from app.core.config import settings


class CanvaClient:
    """Client for Canva Connect API to generate professional UI mockups"""
    
    def __init__(self):
        self.base_url = "https://api.canva.com/rest/v1"
        self.client_id = getattr(settings, 'CANVA_CLIENT_ID', None)
        self.client_secret = getattr(settings, 'CANVA_CLIENT_SECRET', None)
        self.access_token = getattr(settings, 'CANVA_ACCESS_TOKEN', None)
    
    def create_mood_selection_design_v2(self) -> Optional[str]:
        """
        Create v2.0 mood selection screen design with 4 evidence-based moods
        
        Returns:
            Design ID or None if error
        """
        if not self.access_token:
            print("Canva API not configured")
            return None
        
        # Design specification for 4-mood layout
        design_data = {
            "asset_type": "design",
            "title": "SavorMe Mood Selection v2.0 - Evidence-Based",
            "width": {"value": 393, "unit": "px"},
            "height": {"value": 852, "unit": "px"},
            "elements": self._build_mood_selection_elements_v2()
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/designs",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                },
                json=design_data
            )
            response.raise_for_status()
            
            design_id = response.json().get("design", {}).get("id")
            print(f"✅ Canva design created: {design_id}")
            return design_id
        
        except Exception as e:
            print(f"❌ Canva API error: {e}")
            return None
    
    def _build_mood_selection_elements_v2(self) -> List[Dict[str, Any]]:
        """Build UI elements for 4-mood selection screen"""
        
        moods = [
            {
                "id": "stressed",
                "name": "Stressed",
                "subtitle": "Anxious, Wired",
                "emoji": "😰",
                "evidence": "⭐⭐⭐",
                "color": "#3B82F6",
                "position": {"x": 20, "y": 200}
            },
            {
                "id": "fatigued",
                "name": "Fatigued",
                "subtitle": "Tired, Exhausted",
                "emoji": "😴",
                "evidence": "⭐⭐⭐⭐",
                "color": "#EF4444",
                "position": {"x": 210, "y": 200}
            },
            {
                "id": "low_mood",
                "name": "Low Mood",
                "subtitle": "Sad, Down, Blue",
                "emoji": "😢",
                "evidence": "⭐⭐⭐⭐⭐",
                "color": "#8B5CF6",
                "position": {"x": 20, "y": 380}
            },
            {
                "id": "irritable",
                "name": "Irritable",
                "subtitle": "Angry, Cranky",
                "emoji": "😠",
                "evidence": "⭐⭐⭐",
                "color": "#F59E0B",
                "position": {"x": 210, "y": 380}
            }
        ]
        
        elements = [
            # Header
            {
                "type": "text",
                "text": "How are you feeling?",
                "position": {"x": 196, "y": 60},
                "style": {
                    "font_size": 22,
                    "font_weight": "bold",
                    "color": "#065F46",
                    "alignment": "center"
                }
            },
            {
                "type": "text",
                "text": "Select 1-3 moods that resonate with you",
                "position": {"x": 196, "y": 90},
                "style": {
                    "font_size": 13,
                    "color": "#10B981",
                    "alignment": "center"
                }
            },
            # Evidence note
            {
                "type": "shape",
                "shape_type": "rectangle",
                "position": {"x": 20, "y": 120},
                "width": 353,
                "height": 50,
                "style": {
                    "fill_color": "#ECFDF5",
                    "border_color": "#A7F3D0",
                    "border_width": 1,
                    "corner_radius": 8
                }
            },
            {
                "type": "text",
                "text": "✨ All moods backed by scientific research",
                "position": {"x": 196, "y": 145},
                "style": {
                    "font_size": 11,
                    "color": "#059669",
                    "alignment": "center",
                    "italic": True
                }
            }
        ]
        
        # Add mood buttons
        for mood in moods:
            # Button background
            elements.append({
                "type": "shape",
                "shape_type": "rectangle",
                "position": mood["position"],
                "width": 170,
                "height": 160,
                "style": {
                    "fill_color": "#FFFFFF",
                    "border_color": mood["color"],
                    "border_width": 3,
                    "corner_radius": 16
                }
            })
            
            # Evidence badge
            elements.append({
                "type": "text",
                "text": mood["evidence"],
                "position": {
                    "x": mood["position"]["x"] + 130,
                    "y": mood["position"]["y"] + 10
                },
                "style": {
                    "font_size": 10,
                    "font_weight": "bold",
                    "color": mood["color"]
                }
            })
            
            # Emoji
            elements.append({
                "type": "text",
                "text": mood["emoji"],
                "position": {
                    "x": mood["position"]["x"] + 85,
                    "y": mood["position"]["y"] + 40
                },
                "style": {"font_size": 32, "alignment": "center"}
            })
            
            # Mood name
            elements.append({
                "type": "text",
                "text": mood["name"],
                "position": {
                    "x": mood["position"]["x"] + 85,
                    "y": mood["position"]["y"] + 90
                },
                "style": {
                    "font_size": 13,
                    "font_weight": "bold",
                    "color": mood["color"],
                    "alignment": "center"
                }
            })
            
            # Subtitle
            elements.append({
                "type": "text",
                "text": mood["subtitle"],
                "position": {
                    "x": mood["position"]["x"] + 85,
                    "y": mood["position"]["y"] + 115
                },
                "style": {
                    "font_size": 9,
                    "color": "#6B7280",
                    "alignment": "center"
                }
            })
        
        # Intensity section
        elements.extend([
            # Intensity background
            {
                "type": "shape",
                "shape_type": "rectangle",
                "position": {"x": 20, "y": 570},
                "width": 353,
                "height": 80,
                "style": {
                    "fill_color": "#F0FDF4",
                    "border_color": "#BBF7D0",
                    "border_width": 2,
                    "corner_radius": 12
                }
            },
            # Intensity title
            {
                "type": "text",
                "text": "How intense is this feeling?",
                "position": {"x": 196, "y": 585},
                "style": {
                    "font_size": 13,
                    "font_weight": "600",
                    "color": "#065F46",
                    "alignment": "center"
                }
            },
            # Generate button
            {
                "type": "shape",
                "shape_type": "rectangle",
                "position": {"x": 20, "y": 680},
                "width": 353,
                "height": 50,
                "style": {
                    "fill_color": "#10B981",
                    "corner_radius": 16,
                    "shadow": {"blur": 14, "color": "#10B981", "opacity": 0.4}
                }
            },
            {
                "type": "text",
                "text": "🍽️ Get My Recipe Recommendation",
                "position": {"x": 196, "y": 705},
                "style": {
                    "font_size": 15,
                    "font_weight": "bold",
                    "color": "#FFFFFF",
                    "alignment": "center"
                }
            },
            # Version badge
            {
                "type": "text",
                "text": "v2.0 • Evidence-Based Moods",
                "position": {"x": 196, "y": 760},
                "style": {
                    "font_size": 9,
                    "color": "#6B7280",
                    "alignment": "center"
                }
            }
        ])
        
        return elements
    
    def export_design(self, design_id: str, format: str = "png") -> Optional[str]:
        """
        Export Canva design to image
        
        Args:
            design_id: Canva design ID
            format: Export format (png, jpg, pdf)
        
        Returns:
            Export URL or None
        """
        if not self.access_token:
            return None
        
        try:
            response = requests.post(
                f"{self.base_url}/exports",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "design_id": design_id,
                    "format": {"type": format}
                }
            )
            response.raise_for_status()
            
            export_url = response.json().get("export", {}).get("url")
            return export_url
        
        except Exception as e:
            print(f"Export error: {e}")
            return None


# Singleton instance
canva_client = CanvaClient()

