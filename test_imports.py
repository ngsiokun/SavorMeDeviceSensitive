#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""
import sys
import traceback

def test_imports():
    """Test all critical imports"""
    try:
        print("Testing imports...")
        
        # Test models
        from app.models import MoodBlend, MoodInterpretation, UserProfile, NutritionTargets
        print("✅ Models imported successfully")
        
        # Test API routes
        from app.api.routes import router
        print("✅ API routes imported successfully")
        
        # Test main app
        from app.main import app
        print("✅ Main app imported successfully")
        
        print("\n🎉 All imports successful! The app should start without errors.")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
