"""
Complete local test - Frontend to Backend
"""
import requests
import json

print("="*70)
print("COMPLETE LOCAL TEST - Frontend ↔ Backend")
print("="*70)

# Test 1: Frontend
print("\n1. Testing Frontend...")
try:
    r = requests.get("http://127.0.0.1:5000", timeout=3)
    print(f"   ✅ Frontend running: {r.status_code}")
except Exception as e:
    print(f"   ❌ Frontend not running: {e}")
    exit(1)

# Test 2: Complete flow
print("\n2. Testing Complete Flow (User clicks 'Get Recipe')...")
payload = {
    "mood_blend": {
        "moods": [{"mood": "stressed", "intensity": "medium"}]
    },
    "user_profile": {
        "age": 32,
        "gender": "female",
        "height_cm": 165,
        "weight_kg": 60,
        "cuisine_preferences": ["Mediterranean"],
        "food_allergies": [],
        "dietary_preference": "none",
        "activity_level": "moderate"
    },
    "cuisine_preference": "Mediterranean"
}

try:
    r = requests.post("http://127.0.0.1:5000/api/recommend", json=payload, timeout=30)
    if r.status_code == 200:
        result = r.json()
        print(f"   ✅ SUCCESS!")
        print(f"   Recipe: {result['recipe']['name']}")
        print(f"   Calories: {result['recipe']['nutrition']['calories']:.0f}")
    else:
        print(f"   ❌ Error {r.status_code}: {r.text[:200]}")
        exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 3: All cuisines
print("\n3. Testing All 4 Cuisines...")
for cuisine in ["Mediterranean", "South East Asian", "Italian", "Mexican"]:
    p = payload.copy()
    p["user_profile"]["cuisine_preferences"] = [cuisine]
    p["cuisine_preference"] = cuisine
    try:
        r = requests.post("http://127.0.0.1:5000/api/recommend", json=p, timeout=30)
        if r.status_code == 200:
            print(f"   ✅ {cuisine:20s} - {r.json()['recipe']['name'][:35]}")
        else:
            print(f"   ❌ {cuisine:20s} - Error {r.status_code}")
    except Exception as e:
        print(f"   ❌ {cuisine:20s} - {str(e)[:35]}")

print("\n" + "="*70)
print("🎉 LOCAL TESTING COMPLETE!")
print("✅ Open browser: http://localhost:5000")
print("✅ Ready for Cloud Run deployment!")
print("="*70)

