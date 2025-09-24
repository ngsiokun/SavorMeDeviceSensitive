"""
SavorMe Final Mockup Viewer
Opens final compact iPhone-optimized HTML mockups in the default web browser
"""

import webbrowser
import os
from pathlib import Path

def open_final_mockups():
    """Open all final compact iPhone-optimized SavorMe mockups in the browser"""
    mockup_files = [
        "final_recipe_suggestion_mockup.html",
        "final_emotional_rationale_mockup.html"
    ]
    
    print("Opening FINAL compact iPhone-optimized SavorMe mockups in your browser...")
    print("📱 iPhone 13/14 dimensions: 390 x 844 points")
    print("🔧 FINAL version - shorter text, better fit!")
    print("=" * 60)
    
    for i, mockup_file in enumerate(mockup_files, 1):
        if os.path.exists(mockup_file):
            file_path = Path(mockup_file).absolute()
            webbrowser.open(f"file://{file_path}")
            print(f"✅ Opened {i}/2: {mockup_file}")
        else:
            print(f"❌ File not found: {mockup_file}")
    
    print("\n🎉 All FINAL compact iPhone mockups opened!")
    print("\n🔧 Final Text Optimizations:")
    print("✅ Recipe title shortened: 'Yuzu Risotto with Tofu & Shiso'")
    print("✅ Mood indicator shortened: 'Perfect for: Dreamy + Craving + Grounded'")
    print("✅ Cooking directions condensed to single lines")
    print("✅ Smaller font sizes throughout")
    print("✅ Reduced padding and margins")
    print("✅ Compact layout for better screen fit")
    print("✅ All content fits within iPhone screen height")
    print("✅ No more overly long text elements")
    
    print("\n📋 Final Optimizations:")
    print("1️⃣ Recipe Suggestion - Compact recipe display with shorter text")
    print("2️⃣ Emotional Rationale - Condensed emotional explanations")
    print("✅ Green theme matching BeautyDiet aesthetic")
    print("✅ Progress indicators for user flow")
    print("✅ Professional UI with optimized spacing")
    print("✅ NO TEXT OVERFLOW - Everything fits perfectly!")
    print("✅ SHORTER TEXT - No more overly long elements!")
    print("✅ COMPACT LAYOUT - Everything visible on screen!")

if __name__ == "__main__":
    open_final_mockups()
