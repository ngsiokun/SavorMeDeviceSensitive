# Frontend Update Guide - COMPLETED ✅

## 🎯 Status: UPDATE COMPLETE

**The frontend has been successfully updated** to match the **v2.1.0 backend** with 4 evidence-based moods. This guide is now archived for reference.

---

## ✅ Changes Completed

### **Previous (v1.0)**: 10 Moods
```
Dreamy, Fiery, Focused, Playful, Craving, 
Light, Grounded, Restorative, Charismatic, Melancholy
```

### **Current (v2.1.0)**: 4 Evidence-Based Moods ✅
```
Stressed/Anxious, Fatigued, Low Mood, Irritable
```

**Status**: All frontend components have been updated and are working correctly.

---

## 📚 Historical Reference - Update Instructions (COMPLETED)

### **Note**: These instructions were used to update the frontend and are now archived for reference.

### **Option 1: Update Current Frontend Repository** ✅ COMPLETED

The frontend has been successfully updated in the current repository:

#### **Step 1: Navigate to Frontend Repo**
```bash
cd C:\Users\HP\SavorMe\SavorMe
# Or wherever your frontend is
```

#### **Step 2: Update Mood Selection Component**

Replace the 10-mood grid with 4-mood grid:

**Before** (10 moods in 2 columns):
```html
<div class="mood-grid">
    <div class="mood-button dreamy">Dreamy</div>
    <div class="mood-button fiery">Fiery</div>
    <div class="mood-button focused">Focused</div>
    <div class="mood-button playful">Playful</div>
    <div class="mood-button craving">Craving</div>
    <div class="mood-button light">Light</div>
    <div class="mood-button grounded">Grounded</div>
    <div class="mood-button restorative">Restorative</div>
    <div class="mood-button charismatic">Charismatic</div>
    <div class="mood-button melancholy">Melancholy</div>
</div>
```

**After** (4 moods in 2 columns):
```html
<div class="mood-grid">
    <div class="mood-button stressed">
        <div class="evidence-badge">⭐⭐⭐</div>
        <div class="mood-emoji">😰</div>
        <div class="mood-name">Stressed</div>
        <div class="mood-subtitle">Anxious, Wired</div>
    </div>
    
    <div class="mood-button fatigued">
        <div class="evidence-badge">⭐⭐⭐⭐</div>
        <div class="mood-emoji">😴</div>
        <div class="mood-name">Fatigued</div>
        <div class="mood-subtitle">Tired, Exhausted</div>
    </div>
    
    <div class="mood-button low-mood">
        <div class="evidence-badge">⭐⭐⭐⭐⭐</div>
        <div class="mood-emoji">😢</div>
        <div class="mood-name">Low Mood</div>
        <div class="mood-subtitle">Sad, Down, Blue</div>
    </div>
    
    <div class="mood-button irritable">
        <div class="evidence-badge">⭐⭐⭐</div>
        <div class="mood-emoji">😠</div>
        <div class="mood-name">Irritable</div>
        <div class="mood-subtitle">Angry, Cranky</div>
    </div>
</div>
```

#### **Step 3: Update Mood Values in Code**

**Old enum/constants**:
```javascript
const MOODS = [
  'dreamy', 'fiery', 'focused', 'playful', 'craving',
  'light', 'grounded', 'restorative', 'charismatic', 'melancholy'
];
```

**New enum/constants**:
```javascript
const MOODS = {
  STRESSED: 'stressed',
  FATIGUED: 'fatigued',
  LOW_MOOD: 'low_mood',
  IRRITABLE: 'irritable'
};

const MOOD_DISPLAY = {
  stressed: {
    emoji: '😰',
    name: 'Stressed / Anxious',
    subtitle: 'Anxious, Wired, Overwhelmed',
    evidence: '⭐⭐⭐',
    color: '#3B82F6'
  },
  fatigued: {
    emoji: '😴',
    name: 'Fatigued / Low Energy',
    subtitle: 'Tired, Exhausted, Brain Fog',
    evidence: '⭐⭐⭐⭐',
    color: '#EF4444'
  },
  low_mood: {
    emoji: '😢',
    name: 'Low Mood / Blue',
    subtitle: 'Sad, Down, Melancholy',
    evidence: '⭐⭐⭐⭐⭐',
    color: '#8B5CF6'
  },
  irritable: {
    emoji: '😠',
    name: 'Irritable / Angry',
    subtitle: 'Angry, Cranky, Snappy',
    evidence: '⭐⭐⭐',
    color: '#F59E0B'
  }
};
```

#### **Step 4: Update API Endpoint Call**

Make sure your API call sends the correct mood IDs:

```javascript
// API request payload
const requestBody = {
  mood_blend: {
    moods: [
      { mood: "stressed", intensity: "very" },      // ✅ New format
      { mood: "fatigued", intensity: "medium" }
    ]
  },
  user_profile: {
    age: 32,
    gender: "female",
    height_cm: 165,
    weight_kg: 60,
    cuisine_preferences: ["Mediterranean", "Italian"],
    food_allergies: [],
    dietary_preference: "none"
  }
};

// Call backend
const response = await fetch('http://your-backend/api/v1/recipes/recommend', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(requestBody)
});
```

---

### **Option 2: Use the Updated HTML Mockup**

I've created an updated mockup for you:

**File**: `mood_selection_v2.html`

**Features**:
- ✅ 4 moods in 2×2 grid
- ✅ Evidence badges (⭐⭐⭐)
- ✅ Larger buttons (better UX)
- ✅ Aliases shown (e.g., "Anxious, Wired")
- ✅ Interactive selection (1-3 moods)
- ✅ Visual feedback on selection
- ✅ Version badge (v2.0)

**To use**:
```bash
# Open in browser to preview
start mood_selection_v2.html
```

---

## 🎨 Visual Changes

### **Before (v1.0)**:
```
┌─────────────────────────────────────┐
│ 10 moods in 2 columns (5×2 grid)   │
│ Small buttons                       │
│ No evidence indicators              │
│ Vague mood names                    │
└─────────────────────────────────────┘
```

### **After (v2.0)**:
```
┌─────────────────────────────────────┐
│ 4 moods in 2 columns (2×2 grid)    │
│ Larger, more readable buttons       │
│ Evidence badges (⭐⭐⭐⭐⭐)         │
│ Clear aliases shown                 │
│ "Evidence-based" messaging          │
└─────────────────────────────────────┘
```

---

## 📱 iOS/Swift Changes (If Using Native App)

### **Update Mood Enum**

```swift
// OLD
enum Mood: String, CaseIterable {
    case dreamy, fiery, focused, playful, craving,
         light, grounded, restorative, charismatic, melancholy
}

// NEW
enum Mood: String, CaseIterable {
    case stressed = "stressed"
    case fatigued = "fatigued"
    case lowMood = "low_mood"
    case irritable = "irritable"
    
    var displayName: String {
        switch self {
        case .stressed: return "Stressed / Anxious"
        case .fatigued: return "Fatigued / Low Energy"
        case .lowMood: return "Low Mood / Blue"
        case .irritable: return "Irritable / Angry"
        }
    }
    
    var emoji: String {
        switch self {
        case .stressed: return "😰"
        case .fatigued: return "😴"
        case .lowMood: return "😢"
        case .irritable: return "😠"
        }
    }
    
    var evidenceStars: String {
        switch self {
        case .stressed: return "⭐⭐⭐"
        case .fatigued: return "⭐⭐⭐⭐"
        case .lowMood: return "⭐⭐⭐⭐⭐"
        case .irritable: return "⭐⭐⭐"
        }
    }
    
    var aliases: [String] {
        switch self {
        case .stressed: return ["Anxious", "Wired", "Overwhelmed", "Tense"]
        case .fatigued: return ["Tired", "Exhausted", "Brain Fog", "Drained"]
        case .lowMood: return ["Sad", "Down", "Blue", "Melancholy"]
        case .irritable: return ["Angry", "Cranky", "Snappy", "Agitated"]
        }
    }
}
```

### **Update Mood Selection View**

```swift
// OLD: Grid with 10 items
LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 16) {
    ForEach(Mood.allCases, id: \.self) { mood in
        MoodButton(mood: mood, isSelected: selectedMoods.contains(mood))
    }
}

// NEW: Grid with 4 items (same code works!)
// Just the enum changed from 10 to 4 cases
LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 16) {
    ForEach(Mood.allCases, id: \.self) { mood in
        MoodButton(
            mood: mood, 
            isSelected: selectedMoods.contains(mood),
            evidenceLevel: mood.evidenceStars  // ← Add evidence badge
        )
    }
}
```

---

## ✅ Complete Checklist

### **Frontend Repository Updates**

- [ ] **Update mood enum/constants** (10 → 4)
- [ ] **Update UI grid layout** (5×2 → 2×2)
- [ ] **Add evidence badges** (⭐⭐⭐⭐⭐)
- [ ] **Add mood aliases/subtitles** (help users identify)
- [ ] **Update color scheme** (4 distinct colors)
- [ ] **Update selection limit validation** (still max 3)
- [ ] **Test API integration** (ensure correct mood IDs sent)
- [ ] **Update any hardcoded mood references**
- [ ] **Update mockups/screenshots**
- [ ] **Update README**

### **Files to Update**

Common files that need changes:
```
frontend/
├── src/
│   ├── constants/moods.js (or .swift)     ← Update enum
│   ├── components/MoodSelector.jsx        ← Update UI
│   ├── services/api.js                    ← Verify payload
│   └── utils/moodMapping.js               ← Update mappings
├── assets/
│   └── mockups/                           ← Update screenshots
└── README.md                              ← Update documentation
```

---

## 🚀 Quick Commands for Frontend Repo

### **If Frontend is in Separate Repo**:

```bash
# Navigate to frontend repository
cd C:\Users\HP\SavorMe\SavorMe  # Or your frontend path

# Create new branch for mood update
git checkout -b update-to-4-moods

# Make your changes (use mood_selection_v2.html as reference)
# ... edit files ...

# Commit changes
git add .
git commit -m "Update to 4 evidence-based moods matching backend v2.0

- Reduce from 10 moods to 4 scientifically-backed moods
- Add evidence level badges (⭐⭐⭐⭐⭐)
- Show mood aliases for better user identification
- Update API calls to use new mood IDs
- Improve grid layout (2×2 instead of 5×2)

Breaking change: Old mood IDs (dreamy, fiery, etc.) no longer supported
Backend compatibility: v2.0+"

# Push to GitHub
git push origin update-to-4-moods

# Create pull request on GitHub
```

---

## 📦 Files I've Created for You

### **1. `mood_selection_v2.html`** (Just created)
- ✅ Updated 4-mood mockup
- ✅ Evidence badges included
- ✅ Interactive demo
- ✅ Modern styling
- ✅ Responsive design

**Preview it**:
```bash
start mood_selection_v2.html
```

### **2. Ready-to-Use Code Snippets**
- JavaScript constants for 4 moods
- Swift enum for iOS
- Display names and aliases
- Evidence level indicators

---

## 🎨 Design Recommendations

### **Mood Colors** (Updated for 4 moods)

```css
.stressed {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border-color: #3B82F6;  /* Blue - calming */
}

.fatigued {
    background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
    border-color: #EF4444;  /* Red - alerting */
}

.low-mood {
    background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%);
    border-color: #8B5CF6;  /* Purple - gentle */
}

.irritable {
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
    border-color: #F59E0B;  /* Orange - energetic */
}
```

### **Evidence Badge Styling**

```css
.evidence-badge {
    position: absolute;
    top: 8px;
    right: 8px;
    font-size: 10px;
    background: rgba(255,255,255,0.95);
    padding: 3px 6px;
    border-radius: 8px;
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

---

## 🔌 Backend API Compatibility

### **New API Request Format**

```json
POST /api/v1/recipes/recommend

{
  "mood_blend": {
    "moods": [
      {"mood": "stressed", "intensity": "very"},
      {"mood": "fatigued", "intensity": "medium"}
    ]
  },
  "user_profile": {
    "age": 32,
    "gender": "female",
    "height_cm": 165,
    "weight_kg": 60,
    "cuisine_preferences": ["Mediterranean", "Italian"],
    "food_allergies": [],
    "dietary_preference": "none"
  }
}
```

### **Valid Mood IDs** (Backend v2.0)
```
✅ "stressed"
✅ "fatigued"
✅ "low_mood"
✅ "irritable"

❌ "dreamy"  (will return 404)
❌ "fiery"   (will return 404)
❌ etc.
```

---

## 🧪 Testing Checklist

After updating frontend:

- [ ] All 4 moods render correctly
- [ ] Evidence badges display
- [ ] Can select 1-3 moods (not 4)
- [ ] Intensity selection works
- [ ] API request sends correct mood IDs
- [ ] Backend returns successful response
- [ ] Recipe displays with evidence
- [ ] No references to old moods remain
- [ ] Error handling for removed moods

---

## 📸 Before & After Preview

### **Before (v1.0)**
```
┌─────────────────────────────────┐
│  😌 Dreamy    🔥 Fiery         │
│  🎯 Focused   🎨 Playful        │
│  🍯 Craving   ✨ Light          │
│  🌱 Grounded  💚 Restorative    │
│  💫 Charismatic 🌙 Melancholy   │
└─────────────────────────────────┘
10 moods, cluttered, no evidence
```

### **After (v2.0)**
```
┌──────────────────────────────────┐
│  😰 Stressed      😴 Fatigued    │
│  ⭐⭐⭐ Moderate   ⭐⭐⭐⭐ Strong │
│  Anxious, Wired   Tired, Drained │
│                                  │
│  😢 Low Mood      😠 Irritable   │
│  ⭐⭐⭐⭐⭐ Best   ⭐⭐⭐ Moderate │
│  Sad, Down, Blue  Angry, Cranky  │
└──────────────────────────────────┘
4 moods, clear, evidence-based
```

---

## ✅ Summary - UPDATE COMPLETED

### **Completed Update Path**:

1. ✅ **Mood Selection Updated**: 4 evidence-based moods implemented
2. ✅ **UI Layout Updated**: 2×2 grid with colored borders
3. ✅ **Evidence Banner**: Green theme (not yellow)
4. ✅ **Button Functionality**: Working recipe generation
5. ✅ **API Integration**: Fully functional with v2.1.0 backend
6. ✅ **All Changes Committed**: Saved to git and GitHub

### **Current Status**:
- **Moods**: ✅ 4 evidence-based moods (Stressed, Fatigued, Low Mood, Irritable)
- **Layout**: ✅ 2×2 grid with specific colored borders
- **Evidence Banner**: ✅ Green theme matching design requirements
- **Backend**: ✅ Compatible with v2.1.0 API
- **Functionality**: ✅ All features working correctly

---

**🎉 The frontend update is complete and fully functional!**

**Current Application**: http://localhost:5000

