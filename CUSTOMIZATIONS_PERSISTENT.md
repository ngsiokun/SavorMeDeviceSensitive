# SavorMe Customizations - Persistent Design System

## 🎯 **Purpose**
This document ensures that all customizations made to the SavorMe application persist through GitHub clones and maintain consistent quality, branding, evidence-based scientific accuracy, and comprehensive cooking instructions.

## 📁 **Files Modified/Created**

### 1. **Landing Page Customizations**
- **File**: `demo_app/templates/index.html`
- **CSS**: `demo_app/static/css/landing.css`
- **Changes**: 
  - Mobile-first vertical layout (hero section on top, 2x2 feature grid below)
  - Dark teal gradient background (#0F766E to #065F46)
  - Glassmorphic cards with backdrop blur effects
  - Proper responsive design for all screen sizes
  - Consistent typography and spacing

### 2. **Recipe Results Page Customizations**
- **File**: `demo_app/templates/recipe_result.html`
- **CSS**: `demo_app/static/css/recipe_results.css`
- **JavaScript**: `demo_app/static/js/recipe_result.js`
- **Changes**:
  - Mobile-first smartphone design with status bar
  - Pure JavaScript-driven page generation (no HTML templates needed)
  - Comprehensive nutrient analysis modal with detailed breakdown
  - Enhanced "Why This Recipe?" section with specific nutritional data
  - "Another Recipe Suggestion" button (replaces "Got it!" button)
  - Scientific evidence section with research backing
  - 8 key mood-supporting nutrients analysis
  - Proper loading states and error handling
  - Consistent color scheme and typography

### 3. **Evidence-Based Nutrient Analysis System (v2.2)**
- **File**: `demo_app/static/js/recipe_result.js`
- **Changes**:
  - Enhanced "Why This Recipe?" section with evidence-based nutritional rationale
  - EPA-focused omega-3 targeting (≥60% EPA of EPA+DHA)
  - Iron-supportive recipes with heme/non-heme + vitamin C pairing
  - Mediterranean pattern with anti-inflammatory herbs/spices
  - Medically safe claim wording based on evidence strength
  - Comprehensive nutrient highlights with evidence-based targets
  - Scientific evidence section with updated research backing
  - "Another Recipe Suggestion" button for seamless recipe exploration
  - Detailed nutritional breakdown with percentages and targets
  - Mood-specific nutrient benefits explanation
  - **Recipe Match Score Transparency System** with weighted scoring breakdown
  - **Nutrient contribution display** showing individual nutrient scores
  - **Evidence-based weighting** (1.0 = strongest evidence, 0.5 = emerging evidence)
  - **Data source transparency** (Edamam API + built-in nutrient database)

### 4. **Enhanced Cooking Directions System (v3.1.0)**
- **File**: `app/services/openrouter_client.py`
- **Changes**:
  - **Comprehensive AI-Generated Directions**: Increased token limit from 500 to 1200 for detailed instructions
  - **Professional Chef-Level Instructions**: Enhanced prompt requesting preparation, cooking steps, finishing, and tips
  - **Detailed Fallback Directions**: Complete rewrite with ingredient-specific cooking methods
  - **Sectioned Format**: PREPARATION, COOKING STEPS, FINISHING, and TIPS sections
  - **Specific Temperatures & Times**: 375°F for meat, 400°F for fish, 425°F for vegetables
  - **Professional Techniques**: Resting meat, reserving pasta water, proper browning methods
  - **Beginner-Friendly**: Clear enough for someone new to cooking to follow successfully
  - **Ingredient-Specific Methods**: Different detailed approaches for meat, fish, vegetables, pasta
  - **Pro Tips Included**: Common mistakes to avoid, cooking techniques, equipment guidance

### 5. **Evidence-Based Mood Mapping System (v2.2)**
- **File**: `app/data/mood_mapping.json`
- **Changes**:
  - Updated with latest scientific research and meta-analyses
  - EPA-focused omega-3 targeting (≥60% EPA of EPA+DHA)
  - Iron-supportive implementation with heme/non-heme + vitamin C
  - Mediterranean pattern with anti-inflammatory herbs/spices
  - Medically safe claim wording based on evidence strength
  - Evidence level transparency (Strong, Moderate, Low-Moderate)
  - Enhanced micronutrient support (Vitamin D, Zinc, Selenium)

### 6. **Professional Startup System**
- **File**: `savorme_professional_startup.bat`
- **File**: `AUTOMATED_APP_STARTUP_GUIDE.md`
- **Changes**:
  - Comprehensive diagnostic and startup system
  - Step-by-step validation process
  - Professional error handling and recovery
  - Complete user flow testing
  - Evidence-based nutrient targeting verification

## 🎨 **Design System**

### **Color Palette**
- **Primary**: #0F766E (Dark Teal)
- **Secondary**: #065F46 (Dark Green)
- **Accent**: #10B981 (Green)
- **Background**: #F0FDF4 (Light Green)
- **Text**: White (#FFFFFF) and Dark Gray (#374151)

### **Typography**
- **Font Family**: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
- **Hero Title**: 36px, font-weight 800
- **Subtitle**: 16px, font-weight 600
- **Body**: 14px, line-height 1.5
- **Feature Cards**: 14px titles, 11px descriptions

### **Layout Principles**
- **Mobile-First**: All designs start with mobile (414px width)
- **Vertical Stacking**: Hero section above feature grid
- **Glassmorphic Effects**: Semi-transparent cards with blur
- **Consistent Spacing**: 20px margins, 16px gaps
- **Responsive**: Scales appropriately for larger screens

## 🔬 **Evidence-Based Scientific Improvements (v2.2)**

### **EPA-Focused Omega-3 Targeting**
- **Target**: EPA ≥ 60% of EPA+DHA based on meta-analyses
- **Evidence**: Small-to-modest effects for mood support in meta-analyses
- **Implementation**: Prioritize salmon, mackerel, sardines over general omega-3 sources
- **Claim Wording**: "EPA-rich sources may support balanced mood when included regularly"

### **Iron-Supportive Implementation**
- **Target**: 6mg per meal with heme/non-heme distinction
- **Evidence**: Moderate-Strong evidence for fatigue when deficient
- **Implementation**: Combine heme (lean red meat) and non-heme (spinach, legumes) sources
- **Vitamin C Pairing**: 30mg per meal to enhance non-heme iron absorption
- **Claim Wording**: "iron-supportive foods help with energy when levels are adequate"

### **Mediterranean Anti-Inflammatory Pattern**
- **Target**: Whole foods with anti-inflammatory herbs/spices
- **Evidence**: Observational and some RCT support for mood improvement
- **Implementation**: Include turmeric, rosemary, oregano for neuroprotective potential
- **Focus**: Anti-oxidant, anti-inflammatory foods with neuroprotective herbs/spices

## 📊 **Recipe Match Score Transparency System (v2.2)**

### **Scoring Algorithm Overview**
- **Method**: Weighted average based on scientific evidence strength
- **Formula**: `Final Score = (Σ nutrient_score × weight) / Σ weight`
- **Range**: 0-100% (displayed as percentage)
- **Transparency**: Each nutrient's contribution is calculated and can be displayed

### **Weighting System by Evidence Strength**
- **Weight 1.0**: Strongest evidence (SMILES trial, clinical guidelines)
- **Weight 0.9**: Very strong evidence (meta-analyses, Cochrane reviews)
- **Weight 0.8**: Strong evidence (multiple RCTs)
- **Weight 0.7**: Good evidence (observational + some trials)
- **Weight 0.6**: Moderate evidence (correlational studies)
- **Weight 0.5**: Emerging evidence (limited but promising)

### **Mood-Specific Weight Examples**
**Stressed/Anxious Mood**:
- Magnesium: 1.0 (highest - strongest evidence)
- Omega-3 EPA/DHA: 0.9 (very high - meta-analyses)
- Fiber: 0.7 (high - gut-brain axis)
- Added Sugar (limit): 0.6 (medium-high - blood sugar stability)
- Vitamin D: 0.6 (medium-high - emerging evidence)
- Zinc: 0.5 (medium - limited studies)

**Fatigued/Low Energy Mood**:
- Iron: 1.0 (highest - clinical guidelines)
- Vitamin C: 0.8 (very high - absorption enhancement)
- Complex Carbs: 0.8 (very high - energy stability)
- Protein: 0.7 (high - satiety research)
- Fiber: 0.6 (medium-high - crash prevention)
- Vitamin B12: 0.5 (medium - deficiency correction)

### **Data Sources for Scoring**
**Primary Source**: Edamam API
- Comprehensive nutrition data (macronutrients, minerals, vitamins)
- Complete micronutrient coverage (iron, magnesium, omega-3, B-vitamins)
- Per-serving calculations from recipe ingredients

**Enhancement Source**: Built-in Nutrient Database
- Key mood-supporting ingredients (spinach, salmon, lentils, nuts)
- Detailed micronutrient data for common ingredients
- Fills gaps in Edamam's micronutrient coverage

### **Score Calculation Example**
```
Recipe: Mediterranean Salmon (per serving)
Magnesium: 90% × 1.0 = 90
Omega-3: 80% × 0.9 = 72
Fiber: 70% × 0.7 = 49
Added Sugar: 60% × 0.6 = 36
Vitamin D: 50% × 0.6 = 30
Zinc: 40% × 0.5 = 20

Total Weighted Sum: 90 + 72 + 49 + 36 + 30 + 20 = 297
Total Weight: 1.0 + 0.9 + 0.7 + 0.6 + 0.6 + 0.5 = 4.3
Final Score: 297 ÷ 4.3 = 69.1% ≈ 69%
```

### **Transparency Features**
- **Nutrient Breakdown**: Shows individual nutrient scores
- **Weight Display**: Shows why each nutrient matters more/less
- **Evidence Level**: Indicates scientific strength behind each target
- **Data Source**: Traces back to Edamam API + built-in database
- **Target Comparison**: Shows actual vs. target values

### **Medically Safe Claim Wording**
- **Approach**: Evidence-based wording that's clinically appropriate
- **Transparency**: Honest assessment of research strength
- **Safety**: All claims are medically safe and evidence-based
- **Disclaimers**: Appropriate medical disclaimers throughout

### **Evidence Level Classification**
- **Strong Evidence**: Iron deficiency → fatigue (clinical guidelines)
- **Moderate Evidence**: Mediterranean diet → mood improvement (observational + some RCTs)
- **Low-Moderate Evidence**: Omega-3 EPA, magnesium, B-vitamins (mixed RCT results)

## 🔧 **Technical Improvements**

### **Essential Code Snippets**

#### **1. Recipe Result Template (demo_app/templates/recipe_result.html)**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SavorMe - Your Recipe Recommendation</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/recipe_results.css') }}">
</head>
<body>
    <div id="app-container">
        <!-- Everything will be generated by JavaScript -->
    </div>
    <script src="{{ url_for('static', filename='js/recipe_result.js') }}"></script>
</body>
</html>
```

#### **2. Evidence-Based Nutrient Analysis Function (demo_app/static/js/recipe_result.js)**
```javascript
// Generate evidence-based rationale with nutritional information
function generateDetailedRationale(recipe, nutrition, rationale) {
    const calories = Math.round(recipe.nutrition?.calories || 0);
    const protein = Math.round(recipe.nutrition?.protein_g || 0);
    const fiber = Math.round(recipe.nutrition?.fiber_g || 0);
    const magnesium = Math.round(recipe.nutrition?.magnesium_mg || 0);
    const omega3 = Math.round((recipe.nutrition?.omega3_g || 0) * 10) / 10;
    const iron = Math.round(recipe.nutrition?.iron_mg || 0);
    const folate = Math.round(recipe.nutrition?.folate_mcg || 0);
    const b12 = Math.round(recipe.nutrition?.vitamin_b12_mcg || 0);
    const zinc = Math.round(recipe.nutrition?.zinc_mg || 0);
    const vitaminD = Math.round(recipe.nutrition?.vitamin_d_iu || 0);
    const vitaminC = Math.round(recipe.nutrition?.vitamin_c_mg || 0);
    
    const targetCalories = Math.round(nutrition?.target_calories || 0);
    const targetProtein = Math.round(nutrition?.target_protein || 0);
    const targetFiber = Math.round(nutrition?.target_fiber || 0);
    
    const caloriePercent = Math.round((calories / targetCalories) * 100);
    const proteinPercent = Math.round((protein / targetProtein) * 100);
    const fiberPercent = Math.round((fiber / targetFiber) * 100);
    
    let rationaleText = `This ${recipe.name} was carefully selected to provide optimal nutrition for your current needs. `;
    
    // Calorie information
    rationaleText += `With ${calories} calories (${caloriePercent}% of your daily target), `;
    
    // Protein information
    rationaleText += `it delivers ${protein}g of protein (${proteinPercent}% of daily needs) for sustained energy and muscle support. `;
    
    // Fiber information
    rationaleText += `The ${fiber}g of fiber (${fiberPercent}% of daily target) helps maintain stable blood sugar levels and supports digestive health. `;
    
    // Evidence-based nutrient benefits
    if (magnesium > 0) {
        rationaleText += `Rich in magnesium (${magnesium}mg), this recipe helps the body cope with stress. `;
    }
    
    if (omega3 > 0) {
        rationaleText += `The ${omega3}g of EPA-rich omega-3 fatty acids may support balanced mood when included regularly. `;
    }
    
    if (iron > 0) {
        rationaleText += `With ${iron}mg of iron, this iron-supportive recipe helps with energy when levels are adequate. `;
    }
    
    if (vitaminC > 0 && iron > 0) {
        rationaleText += `The ${vitaminC}mg of vitamin C enhances iron absorption from plant sources. `;
    }
    
    if (folate > 0) {
        rationaleText += `The ${folate}mcg of folate (B9) is important for brain function and emotional balance. `;
    }
    
    if (b12 > 0) {
        rationaleText += `Vitamin B12 (${b12}mcg) is important for brain function and emotional balance. `;
    }
    
    if (zinc > 0) {
        rationaleText += `Zinc (${zinc}mg) is an essential mineral for brain and nervous system support. `;
    }
    
    if (vitaminD > 0) {
        rationaleText += `Vitamin D (${vitaminD}IU) supports overall health and may play a role in mood balance. `;
    }
    
    // Mood-specific benefits
    rationaleText += `This combination of nutrients works synergistically to support your emotional well-being and provide the energy your body needs.`;
    
    return rationaleText;
}
```

#### **3. Evidence-Based Nutrient Highlights (Non-Zero Only)**
```javascript
// Generate evidence-based nutrient highlights for only non-zero nutrients
function generateNutrientHighlights(recipe) {
    const nutrients = [
        {
            name: 'Magnesium',
            value: Math.round(recipe.nutrition?.magnesium_mg || 0),
            unit: 'mg',
            target: 120,
            benefit: 'helps the body cope with stress',
            evidence: 'Low-Moderate evidence'
        },
        {
            name: 'EPA-Rich Omega-3',
            value: Math.round((recipe.nutrition?.omega3_g || 0) * 10) / 10,
            unit: 'g',
            target: 0.35,
            benefit: 'may support balanced mood when included regularly',
            evidence: 'Small-to-modest effects in meta-analyses'
        },
        {
            name: 'Iron',
            value: Math.round(recipe.nutrition?.iron_mg || 0),
            unit: 'mg',
            target: 6,
            benefit: 'iron-supportive foods help with energy when levels are adequate',
            evidence: 'Moderate-Strong evidence for fatigue when deficient'
        },
        {
            name: 'Folate (B9)',
            value: Math.round(recipe.nutrition?.folate_mcg || 0),
            unit: 'mcg',
            target: 100,
            benefit: 'important for brain function and emotional balance',
            evidence: 'Correlations with mood, supportive building blocks'
        },
        {
            name: 'Vitamin B12',
            value: Math.round(recipe.nutrition?.vitamin_b12_mcg || 0),
            unit: 'mcg',
            target: 1.5,
            benefit: 'important for brain function and emotional balance',
            evidence: 'Correlations with mood, supportive building blocks'
        },
        {
            name: 'Zinc',
            value: Math.round(recipe.nutrition?.zinc_mg || 0),
            unit: 'mg',
            target: 3,
            benefit: 'essential mineral for brain and nervous system support',
            evidence: 'Emerging evidence for cognitive/emotional regulation'
        },
        {
            name: 'Vitamin D',
            value: Math.round(recipe.nutrition?.vitamin_d_iu || 0),
            unit: 'IU',
            target: 400,
            benefit: 'supports overall health and may play a role in mood balance',
            evidence: 'Low evidence, associations with mood'
        },
        {
            name: 'Fiber',
            value: Math.round(recipe.nutrition?.fiber_g || 0),
            unit: 'g',
            target: 8,
            benefit: 'may support gut microbiome and gut-brain axis health',
            evidence: 'Gut-brain axis research'
        }
    ];
    
    // Filter to only show nutrients with non-zero values
    const nonZeroNutrients = nutrients.filter(nutrient => nutrient.value > 0);
    
    // If no nutrients have values, show a message
    if (nonZeroNutrients.length === 0) {
        return '<li><em>This recipe provides essential macronutrients (calories, protein, fiber) that support your mood and energy levels.</em></li>';
    }
    
    // Generate HTML for non-zero nutrients with evidence information
    return nonZeroNutrients.map(nutrient => 
        `<li><strong>${nutrient.name}:</strong> ${nutrient.value} ${nutrient.unit} (target: ${nutrient.target} ${nutrient.unit}) — ${nutrient.benefit}. <em>${nutrient.evidence}</em></li>`
    ).join('');
}
```

**HTML Usage:**
```html
<div class="nutrient-highlights">
    <h4>Nutrient Highlights:</h4>
    <ul>
        ${generateNutrientHighlights(recipe)}
    </ul>
</div>
```

#### **4. Another Recipe Suggestion Button**
```html
<div class="modal-footer">
    <button class="btn btn-primary" onclick="generateNewRecommendation()">Another Recipe Suggestion</button>
</div>
```

#### **5. Enhanced Modal CSS (demo_app/static/css/recipe_results.css)**
```css
/* Nutrient Match Score Button Styling */
.nutrient-match-btn {
    width: 100%;
    background: #065F46;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 16px 24px;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(6, 95, 70, 0.3);
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.nutrient-match-btn:hover {
    background: #0F766E;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(6, 95, 70, 0.4);
}

.nutrient-match-btn:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(6, 95, 70, 0.3);
}

.nutrient-match-icon {
    font-size: 18px;
}

.nutrient-match-text {
    font-size: 16px;
    font-weight: 700;
}

/* Disclaimer styling to blend in */
.disclaimer {
    padding: 12px;
    background: #F9FAFB;
    border-radius: 8px;
    border: 1px solid #E5E7EB;
}

.disclaimer small {
    font-size: 10px;
    color: #6B7280;
    line-height: 1.3;
}
```

### **Cooking Directions System**
```python
# Fallback cooking directions based on ingredient analysis
def _generate_fallback_directions(self, recipe_name, ingredients, cuisine_type):
    # Analyzes ingredients to determine cooking method
    # Generates appropriate steps for meat, fish, vegetables, or general dishes
    # Provides 5-6 practical cooking steps
```

### **New Suggestions Button Fix**
```javascript
// Properly retrieves mood and profile data from session storage
// Makes new API call for fresh recommendations
// Handles errors gracefully with fallback to mood selection
```

### **Professional Startup System**
- Comprehensive environment validation
- Automatic dependency installation
- Health checks for both backend and frontend
- Complete user flow testing
- Error recovery procedures

## 📋 **Verification Checklist**

After cloning from GitHub, verify these elements are present:

### **Landing Page**
- [ ] Mobile-first vertical layout
- [ ] Dark teal gradient background
- [ ] Hero section with SavorMe branding
- [ ] 2x2 feature grid below hero
- [ ] Glassmorphic card effects
- [ ] "Start Your Journey →" button works

### **Recipe Results Page**
- [ ] Mobile smartphone design with status bar
- [ ] Loading spinner appears during API calls
- [ ] Cooking directions show actual steps (not just links)
- [ ] "Nutrient Match Score" button opens detailed modal
- [ ] "Another Recipe Suggestion" button gets fresh recipes (replaces "Got it!")
- [ ] Comprehensive nutrient analysis with 8 key nutrients
- [ ] Enhanced "Why This Recipe?" section with specific nutritional data
- [ ] Scientific evidence section with research backing
- [ ] Proper error handling and user feedback

### **Backend Functionality**
- [ ] Cooking directions generate automatically
- [ ] Fallback system works when API keys missing
- [ ] Recipe recommendations include full data
- [ ] Error handling provides meaningful messages

### **Evidence-Based Nutrient Analysis (v2.2)**
- [ ] Evidence-based mood-supporting nutrients displayed:
  - [ ] Magnesium (120mg target) - helps the body cope with stress (Low-Moderate evidence)
  - [ ] EPA-Rich Omega-3 (0.35g target) - may support balanced mood when included regularly (Small-to-modest effects in meta-analyses)
  - [ ] Iron (6mg target) - iron-supportive foods help with energy when levels are adequate (Moderate-Strong evidence for fatigue when deficient)
  - [ ] Folate/B9 (100mcg target) - important for brain function and emotional balance (Correlations with mood, supportive building blocks)
  - [ ] Vitamin B12 (1.5mcg target) - important for brain function and emotional balance (Correlations with mood, supportive building blocks)
  - [ ] Zinc (3mg target) - essential mineral for brain and nervous system support (Emerging evidence for cognitive/emotional regulation)
  - [ ] Vitamin D (400 IU target) - supports overall health and may play a role in mood balance (Low evidence, associations with mood)
  - [ ] Fiber (8g target) - may support gut microbiome and gut-brain axis health (Gut-brain axis research)
- [ ] EPA-focused omega-3 targeting (≥60% EPA of EPA+DHA)
- [ ] Iron-supportive recipes with heme/non-heme + vitamin C pairing
- [ ] Mediterranean pattern with anti-inflammatory herbs/spices
- [ ] Medically safe claim wording throughout
- [ ] Evidence level transparency (Strong, Moderate, Low-Moderate)
- [ ] Detailed rationale with specific nutritional percentages
- [ ] Scientific evidence section with updated research backing
- [ ] "Another Recipe Suggestion" button functionality

### **Professional Startup**
- [ ] `savorme_professional_startup.bat` exists
- [ ] `AUTOMATED_APP_STARTUP_GUIDE.md` is present
- [ ] All CSS files are in place
- [ ] Environment setup works automatically

## 🚀 **Quick Setup After Clone**

1. **Run the professional startup script**:
   ```cmd
   savorme_professional_startup.bat
   ```

2. **Or follow the automated guide**:
   - Read `AUTOMATED_APP_STARTUP_GUIDE.md`
   - Follow the step-by-step process

3. **Verify customizations**:
   - Check landing page layout
   - Test recipe results page
   - Verify cooking directions appear
   - Test "New Suggestions" button

## 🔄 **Maintenance**

### **When Adding New Features**
- Follow the established design system
- Use the same color palette and typography
- Maintain mobile-first approach
- Update this documentation

### **When Updating Styles**
- Modify the dedicated CSS files, not inline styles
- Test across different screen sizes
- Ensure consistency with existing design
- Update this documentation

### **When Fixing Bugs**
- Document the fix in this file
- Ensure the fix persists through clones
- Update verification checklist if needed

## 🎯 **Key Features That Must Be Preserved**

### **Essential Files for GitHub Cloning:**
1. **`demo_app/templates/recipe_result.html`** - Minimal template for JavaScript-driven page
2. **`demo_app/static/js/recipe_result.js`** - Complete JavaScript functionality with:
   - Dynamic page generation
   - Comprehensive nutrient analysis
   - Enhanced rationale generation
   - Modal functionality
   - "Another Recipe Suggestion" button
3. **`demo_app/static/css/recipe_results.css`** - Complete styling with:
   - Mobile-first design
   - Modal styles
   - Button animations
   - Disclaimer styling
4. **`demo_app/templates/index.html`** - Landing page template
5. **`demo_app/static/css/landing.css`** - Landing page styling

### **Critical JavaScript Functions:**
- `generateDetailedRationale()` - Evidence-based nutritional analysis
- `showNutrientAnalysis()` - Modal display with comprehensive data
- `generateNewRecommendation()` - Seamless recipe exploration
- `generatePage()` - Dynamic page generation
- `addEventListeners()` - Button functionality

### **Evidence-Based Mood-Supporting Nutrients (v2.2):**
- **Primary**: Magnesium, EPA-Rich Omega-3, Iron, B-Vitamins (Folate, B6, B12), Fiber
- **Secondary**: Vitamin D, Zinc, Selenium, Vitamin C
- **Evidence Levels**: Strong (Iron), Moderate (Mediterranean), Low-Moderate (Omega-3, B-vitamins)
- **EPA Focus**: ≥60% EPA of EPA+DHA for optimal mood support
- **Iron Implementation**: Heme/non-heme sources with vitamin C pairing
- **Mediterranean Pattern**: Anti-inflammatory herbs/spices for neuroprotection
- **Medically Safe Claims**: Evidence-based wording throughout
- **Conditional Display**: Based on recipe content with evidence transparency

## 📝 **Notes**

- All customizations are now in dedicated files that will persist through GitHub clones
- The design system ensures consistent quality and branding
- Professional startup system provides reliable deployment
- Error handling and fallback systems ensure robust operation
- Mobile-first design provides optimal user experience across devices
- **Evidence-based nutrient analysis (v2.2) provides scientifically accurate recommendations**
- **EPA-focused omega-3 targeting (≥60% EPA of EPA+DHA) based on meta-analyses**
- **Iron-supportive recipes with heme/non-heme + vitamin C pairing**
- **Mediterranean pattern with anti-inflammatory herbs/spices for neuroprotection**
- **Medically safe claim wording based on evidence strength**
- **Evidence level transparency (Strong, Moderate, Low-Moderate)**
- **"Another Recipe Suggestion" button eliminates need to re-enter data**
- **Enhanced modal system provides detailed nutritional insights with scientific backing**

---

*This document ensures that the SavorMe application maintains its professional quality, evidence-based nutritional analysis, scientifically accurate recommendations, and consistent design across all deployments and GitHub clones.*
