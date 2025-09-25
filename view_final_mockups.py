"""
Script to open super ultra-compact smartphone-optimized SavorMe mockups in browser
"""

import webbrowser
import os
import time

def open_super_ultra_compact_mockups():
    """Open all super ultra-compact smartphone mockups in browser"""
    print("Opening super ultra-compact smartphone-optimized SavorMe mockups...")
    
    mockup_files = [
        "mood_selection_mockup.html",
        "emotional_rationale_mockup.html"
    ]
    
    for i, file in enumerate(mockup_files):
        if os.path.exists(file):
            print(f"Opening {file}...")
            webbrowser.open(f"file://{os.path.abspath(file)}")
            if i < len(mockup_files) - 1:  # Don't wait after the last file
                time.sleep(2)  # Wait 2 seconds between opening files
        else:
            print(f"Warning: {file} not found. Please run final_mockup_generator.py first.")
    
    print("\nAll super ultra-compact smartphone mockups opened in browser!")
    print("\n✅ Super ultra-optimizations made:")
    print("📱 Minimal padding (8px) for maximum space utilization")
    print("📏 Micro font sizes (7-16px) while maintaining readability")
    print("🎯 Ultra-compact spacing and margins (2-8px)")
    print("⚡ Streamlined layouts that fit perfectly in iPhone height")
    print("👆 Maintained touch targets for usability")
    print("🎨 Preserved visual hierarchy with super condensed design")
    print("📐 All content now fits within screen boundaries - no scrolling needed!")

if __name__ == "__main__":
    open_super_ultra_compact_mockups()
