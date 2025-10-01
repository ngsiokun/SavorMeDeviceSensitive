# Canva API Setup for SavorMe v2.0

## 🎨 Overview

Use Canva Connect API to generate professional mockups for the 4 evidence-based mood system.

---

## 📋 Step 1: Get Canva API Credentials

### **A. Go to Canva Developers Portal**
https://www.canva.com/developers/

### **B. Create/Access Your App**
1. Click "Create an app" or access existing app
2. Your existing integration: https://canva.com/developers/integrations/connect-api/OC-AZI8LZejb8u/configuration

### **C. Get Credentials**
From your app's "Credentials" section, copy:
- **Client ID**: `your_client_id`
- **Client Secret**: `your_client_secret`

### **D. Get Access Token**
You'll need to complete OAuth flow or use a test token from Canva dashboard.

---

## 📝 Step 2: Configure Environment

Add to your `.env` file:

```bash
# Canva Connect API
CANVA_CLIENT_ID=your_client_id_here
CANVA_CLIENT_SECRET=your_client_secret_here
CANVA_ACCESS_TOKEN=your_access_token_here
```

---

## 🚀 Step 3: Generate v2.0 Mockups

### **Run the Generator**:

```bash
python generate_canva_mockups.py
```

### **What It Does**:

1. ✅ Creates a new Canva design (393×852px - iPhone size)
2. ✅ Adds 4 mood buttons with evidence badges
3. ✅ Positions all UI elements
4. ✅ Applies styling and colors
5. ✅ Returns design ID

### **Expected Output**:

```
============================================================
SavorMe v2.0 Canva Mockup Generator
4 Evidence-Based Moods
============================================================

🎨 Creating mood selection screen...
✅ Design created successfully!
   Design ID: ABC123XYZ
   View at: https://www.canva.com/design/ABC123XYZ

📦 Exporting design...
✅ Export ready!
   Download: https://export.canva.com/ABC123/image.png

============================================================
Next steps:
1. Review design in Canva
2. Refine colors, spacing, typography
3. Export high-resolution images
4. Use as reference for iOS/React development
============================================================
```

---

## 🎨 What Gets Created

### **Design Specifications**

**Canvas Size**: 393×852px (iPhone 14 Pro dimensions)

**4 Mood Buttons** (2×2 grid):

| Mood | Emoji | Evidence | Color | Position |
|------|-------|----------|-------|----------|
| Stressed | 😰 | ⭐⭐⭐ | Blue #3B82F6 | Top-left |
| Fatigued | 😴 | ⭐⭐⭐⭐ | Red #EF4444 | Top-right |
| Low Mood | 😢 | ⭐⭐⭐⭐⭐ | Purple #8B5CF6 | Bottom-left |
| Irritable | 😠 | ⭐⭐⭐ | Orange #F59E0B | Bottom-right |

**Additional Elements**:
- Header: "How are you feeling?"
- Subtitle: "Select 1-3 moods that resonate with you"
- Evidence note: "✨ All moods backed by scientific research"
- Intensity selector (A little, Medium, Very)
- Generate button
- Version badge (v2.0)

---

## 🔧 Customization

### **Edit the Design in Canva**

After generation:
1. Open design in Canva (use the URL from output)
2. Manually adjust:
   - Typography
   - Spacing
   - Colors
   - Add branding elements
   - Add imagery
3. Export final version

### **Modify Code**

Edit `app/services/canva_client.py` to change:
- Button positions
- Colors
- Font sizes
- Layout

---

## 📦 Export Options

### **PNG** (Recommended for mockups)
```python
export_url = canva_client.export_design(design_id, format="png")
```

### **JPG** (Smaller file size)
```python
export_url = canva_client.export_design(design_id, format="jpg")
```

### **PDF** (For print/documentation)
```python
export_url = canva_client.export_design(design_id, format="pdf")
```

---

## 🔄 Workflow

```
┌─────────────────────────────────────┐
│ 1. Run generate_canva_mockups.py   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 2. Canva API creates design         │
│    (4 moods, evidence badges)       │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 3. Open design in Canva             │
│    (Manual refinement)              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 4. Export high-res PNG/PDF         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 5. Use for iOS/React development    │
└─────────────────────────────────────┘
```

---

## ⚠️ Important Notes

### **Canva API Limitations**
- Requires paid Canva account for some features
- API calls may have rate limits
- OAuth flow needed for access token

### **Alternative: HTML Mockups**
If Canva API is not configured, the project includes:
- ✅ `mood_selection_v2.html` - Interactive HTML mockup
- ✅ Can be viewed directly in browser
- ✅ Can be used as design reference
- ✅ No API needed

---

## 🎯 Recommended Approach

### **For Quick Prototyping**:
Use **HTML mockups** (`mood_selection_v2.html`)
- Instant preview
- Easy to iterate
- No API setup needed

### **For Professional Designs**:
Use **Canva API** once you have credentials
- Professional polish
- Team collaboration in Canva
- High-quality exports
- Brand asset management

---

## 🔗 Resources

- **Canva Developers**: https://www.canva.com/developers/
- **Connect API Docs**: https://www.canva.com/developers/docs/connect-api/
- **OAuth Guide**: https://www.canva.com/developers/docs/connect-api/authentication/
- **Your Integration**: https://canva.com/developers/integrations/connect-api/OC-AZI8LZejb8u/

---

## ✅ Quick Start

```bash
# If you have Canva credentials
python generate_canva_mockups.py

# If not, just use HTML mockup
start mood_selection_v2.html
```

Both approaches give you professional 4-mood designs! 🎨

