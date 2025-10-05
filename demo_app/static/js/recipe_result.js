// SavorMe Recipe Result - Pure JavaScript Dynamic Page Generation
// Matching the beautiful design from the first screenshot

// Main function to generate the entire page
function generatePage() {
    const container = document.getElementById('app-container');
    
    // Get recipe data from session storage
    const resultData = sessionStorage.getItem('recipeResult');
    
    if (!resultData) {
        container.innerHTML = generateErrorPage();
        return;
    }
    
    try {
    const result = JSON.parse(resultData);
        container.innerHTML = generateRecipePage(result);
        addEventListeners();
    } catch (error) {
        console.error('Error parsing recipe data:', error);
        container.innerHTML = generateErrorPage();
    }
}

// Generate the complete recipe page HTML matching the first screenshot
function generateRecipePage(data) {
    const recipe = data.recipe;
    const rationale = data.emotional_rationale;
    const alignment = data.flavor_alignment;
    const nutrition = data.nutrition_comparison;
    
    // Generate ingredients HTML
    let ingredientsHTML = '';
    if (recipe.ingredients && recipe.ingredients.length > 0) {
        ingredientsHTML = `
            <div class="ingredients-section">
                <h3 class="section-title">• Ingredients</h3>
                <ul class="ingredients-list">
                    ${recipe.ingredients.map(ing => `<li>${ing.amount || ''} ${ing.name}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Generate directions HTML
    let directionsHTML = '';
    if (recipe.cooking_directions && recipe.cooking_directions.length > 0) {
        directionsHTML = `
            <div class="directions-section">
                <h3 class="section-title">Directions</h3>
                <div class="directions-content">
                    ${recipe.cooking_directions.map(step => `<p>${step}</p>`).join('')}
                </div>
            </div>
        `;
    }
    
    // Generate image HTML with fallback
    let imageHTML = '';
    if (recipe.image_url) {
        imageHTML = `
            <img src="${recipe.image_url}" class="recipe-image" alt="${recipe.name}" 
                 onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                     <div class="recipe-image-placeholder" style="display: none;">
                         <div class="placeholder-icon">🥘</div>
                         <div class="placeholder-text">${recipe.name}</div>
                         <div class="placeholder-subtitle">Delicious Recipe</div>
            </div>
        `;
    } else {
        imageHTML = `
            <div class="recipe-image-placeholder">
                         <div class="placeholder-icon">🥘</div>
                         <div class="placeholder-text">${recipe.name}</div>
                         <div class="placeholder-subtitle">Delicious Recipe</div>
            </div>
        `;
    }
    
    return `
        <div class="app-container">
            <!-- Status Bar -->
            <div class="status-bar">
                <span>9:41</span>
                <span>🔋 100%</span>
            </div>
            
            <!-- Main Content -->
            <div class="content-area">
                <!-- Header -->
                <div class="page-header">
                    <h1 class="page-title">Your Perfect Recipe</h1>
                    <p class="page-subtitle">Based on your mood and profile</p>
                </div>

                <!-- Recipe Image -->
                <div class="recipe-image-container">
                    ${imageHTML}
                </div>

                <!-- Recipe Info -->
                <div class="recipe-info">
                    <h2 class="recipe-name">${recipe.name}</h2>
                    <div class="recipe-servings">${recipe.servings || 4} servings</div>
                </div>

                <!-- Nutrition Summary -->
                <div class="nutrition-summary">
                    <div class="nutrition-item">
                        <span class="nutrition-value">${Math.round(recipe.nutrition?.calories || 0)}</span>
                        <span class="nutrition-label">CALORIES</span>
                    </div>
                    <div class="nutrition-item">
                        <span class="nutrition-value">${Math.round(recipe.nutrition?.protein_g || 0)}g</span>
                        <span class="nutrition-label">PROTEIN</span>
                    </div>
                    <div class="nutrition-item">
                        <span class="nutrition-value">${Math.round(recipe.nutrition?.fiber_g || 0)}g</span>
                        <span class="nutrition-label">FIBER</span>
                    </div>
                </div>

                ${ingredientsHTML}
                ${directionsHTML}

                <!-- Nutrient Match Score Section -->
                <div class="nutrient-match-section">
                    <button class="nutrient-match-btn">
                        <span class="nutrient-match-icon">📊</span>
                        <span class="nutrient-match-text">Nutrient Match Score</span>
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Generate error page HTML
function generateErrorPage() {
    return `
        <div class="app-container">
            <!-- Status Bar -->
            <div class="status-bar">
                <span>9:41</span>
                <span>🔋 100%</span>
            </div>
            
            <!-- Main Content -->
            <div class="content-area">
                <!-- Header -->
                <div class="page-header">
                    <h1 class="page-title">Recipe Recommendation</h1>
                    <p class="page-subtitle">Something went wrong</p>
                </div>

                <!-- Error State -->
                <div class="error-container">
                    <div class="error-icon">😔</div>
                    <h3 class="error-title">Oops! Something went wrong</h3>
                    <p class="error-message">We couldn't find the perfect recipe for you right now.</p>
                    <button id="retry-btn" class="btn btn-primary">Try Again</button>
                </div>
            </div>
        </div>
    `;
}

// Add event listeners
function addEventListeners() {
    // Nutrient Match Score button
    const nutrientMatchBtn = document.querySelector('.nutrient-match-btn');
    if (nutrientMatchBtn) {
        nutrientMatchBtn.addEventListener('click', () => {
            // Show detailed nutrition analysis
            showNutrientAnalysis();
        });
    }
    
    // Retry button (for error state)
    const retryBtn = document.getElementById('retry-btn');
    if (retryBtn) {
        retryBtn.addEventListener('click', () => {
            window.location.href = '/mood-selection';
        });
    }
}

// Generate new recommendations
async function generateNewRecommendation() {
    try {
        // Close the modal first
        closeNutrientModal();
        
        // Get mood and profile data from session storage
        const selectedMoods = JSON.parse(sessionStorage.getItem('selectedMoods') || '[]');
        const selectedIntensity = sessionStorage.getItem('selectedIntensity') || 'medium';
        const userProfile = JSON.parse(sessionStorage.getItem('userProfile') || '{}');
        
        if (selectedMoods.length === 0) {
            window.location.href = '/mood-selection';
            return;
        }
        
        // Show loading state
        const container = document.getElementById('app-container');
        container.innerHTML = `
            <div class="app-container">
                <div class="status-bar">
                    <span>9:41</span>
                    <span>🔋 100%</span>
                </div>
                <div class="content-area">
                    <div class="page-header">
                        <h1 class="page-title">Finding New Recipe</h1>
                        <p class="page-subtitle">Please wait...</p>
                    </div>
                    <div class="loading-container">
                        <div class="loading-spinner"></div>
                        <p class="loading-text">Finding your perfect recipe...</p>
                    </div>
                </div>
                </div>
            `;
        
        const payload = {
            mood_blend: {
                moods: selectedMoods.map(mood => ({
                    mood: mood,
                    intensity: selectedIntensity
                }))
            },
            user_profile: userProfile,
            cuisine_preference: userProfile.cuisine_preference || null
        };
        
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error('Failed to get new recommendation');
        }
        
        const result = await response.json();
        sessionStorage.setItem('recipeResult', JSON.stringify(result));
        
        // Regenerate the page with new data
        generatePage();
        
    } catch (error) {
        console.error('Error getting new recommendation:', error);
        const container = document.getElementById('app-container');
        container.innerHTML = generateErrorPage();
        addEventListeners();
    }
}

// Show detailed nutrient analysis modal
function showNutrientAnalysis() {
    const resultData = sessionStorage.getItem('recipeResult');
    if (!resultData) return;
    
    const data = JSON.parse(resultData);
    const recipe = data.recipe;
    const rationale = data.emotional_rationale;
    const alignment = data.flavor_alignment;
    const nutrition = data.nutrition_comparison;
    
    // Create modal HTML
    const modalHTML = `
        <div class="nutrient-modal-overlay" onclick="closeNutrientModal()">
            <div class="nutrient-modal" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h2>Nutrient Match Score</h2>
                    <button class="close-btn" onclick="closeNutrientModal()">×</button>
                </div>
                
                <div class="modal-content">
                    <!-- Match Score -->
                    <div class="match-score-card">
                        <div class="match-score-value">${Math.round(alignment?.nutrient_match_score || 105)}%</div>
                        <div class="match-score-subtitle">Evidence-Based Recommendation</div>
                    </div>
                    
                    <!-- Why This Recipe -->
                    <div class="analysis-section">
        <div class="section-header">
                            <span class="section-icon">💭</span>
                            <h3>Why This Recipe?</h3>
                        </div>
                        <div class="rationale-text">${generateDetailedRationale(recipe, nutrition, rationale)}</div>
                        
                        ${rationale?.mood_breakdowns ? rationale.mood_breakdowns.map(breakdown => `
                            <div class="mood-breakdown-item">
                                <div class="mood-breakdown-header">
                                    <span class="mood-icon">${getMoodEmoji(breakdown.mood)}</span>
                                    <span class="mood-name">${breakdown.mood}</span>
                                </div>
                                <div class="mood-breakdown-text">${breakdown.explanation}</div>
                            </div>
                        `).join('') : ''}
        </div>
    
                    <!-- Nutrition Breakdown -->
                    <div class="analysis-section">
        <div class="section-header">
                            <span class="section-icon">📊</span>
                            <h3>Nutrition Breakdown</h3>
        </div>
                        <div class="nutrition-table">
                            <table>
            <thead>
                <tr>
                    <th>Nutrient</th>
                    <th>This Meal</th>
                    <th>Daily Target</th>
                    <th>% of Day</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Calories</td>
                                        <td>${Math.round(nutrition?.recipe_calories || 0)} kcal</td>
                                        <td>${Math.round(nutrition?.target_calories || 0)} kcal</td>
                                        <td class="percentage">${nutrition?.percentage_of_daily_calories || 0}%</td>
                </tr>
                <tr>
                    <td>Protein</td>
                                        <td>${Math.round(nutrition?.recipe_protein || 0)}g</td>
                                        <td>${Math.round(nutrition?.target_protein || 0)}g</td>
                                        <td class="percentage">${nutrition?.percentage_of_daily_protein || 0}%</td>
                </tr>
                <tr>
                    <td>Fiber</td>
                                        <td>${Math.round(nutrition?.recipe_fiber || 0)}g</td>
                                        <td>${Math.round(nutrition?.target_fiber || 0)}g</td>
                                        <td class="percentage">${nutrition?.percentage_of_daily_fiber || 0}%</td>
                </tr>
            </tbody>
        </table>
                        </div>
                        
                                <div class="nutrient-highlights">
                                    <h4>Nutrient Highlights:</h4>
                                    <ul>
                                        ${generateNutrientHighlights(recipe)}
                </ul>
            </div>
                    </div>
    
                    <!-- Scientific Evidence -->
                    <div class="analysis-section">
            <div class="section-header">
                            <span class="section-icon">🧪</span>
                            <h3>Scientific Evidence</h3>
                        </div>
                        <div class="evidence-rating">
                            <div class="stars">★★★★★</div>
                            <div class="evidence-text">Evidence-Based Recommendation</div>
            </div>
                        <div class="evidence-details">
                            <p>This recommendation is based on:</p>
                <ul>
                    <li>Peer-reviewed nutritional research</li>
                    <li>Mediterranean diet studies (SMILES trial)</li>
                    <li>Nutrient-mood correlation meta-analyses</li>
                </ul>
            </div>
            <div class="disclaimer">
                            <small>This app provides food suggestions based on science and is not a substitute for professional medical advice.</small>
                        </div>
                    </div>
                </div>
                
                        <div class="modal-footer">
                            <button class="btn btn-primary" onclick="generateNewRecommendation()">Another Recipe Suggestion</button>
                        </div>
            </div>
            </div>
        `;
    
    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

// Close nutrient modal
function closeNutrientModal() {
    const modal = document.querySelector('.nutrient-modal-overlay');
    if (modal) {
        modal.remove();
    }
}

        // Generate nutrient highlights with fallback for limited micronutrient data
        function generateNutrientHighlights(recipe) {
            const nutrients = [
                {
                    name: 'Magnesium',
                    value: Math.round(recipe.nutrition?.magnesium_mg || 0),
                    unit: 'mg',
                    target: 120,
                    benefit: 'supports nervous system and stress response'
                },
                {
                    name: 'Omega 3 EPA DHA',
                    value: Math.round((recipe.nutrition?.omega3_g || 0) * 10) / 10,
                    unit: 'g',
                    target: 2.0,
                    benefit: 'anti-inflammatory, supports mood regulation'
                },
                {
                    name: 'Iron',
                    value: Math.round(recipe.nutrition?.iron_mg || 0),
                    unit: 'mg',
                    target: 18,
                    benefit: 'prevents fatigue and supports cognitive function'
                },
                {
                    name: 'Folate (B9)',
                    value: Math.round(recipe.nutrition?.folate_mcg || 0),
                    unit: 'mcg',
                    target: 400,
                    benefit: 'essential for neurotransmitter synthesis and mood stability'
                },
                {
                    name: 'Vitamin B12',
                    value: Math.round(recipe.nutrition?.vitamin_b12_mcg || 0),
                    unit: 'mcg',
                    target: 2.4,
                    benefit: 'supports brain function and prevents depression'
                },
                {
                    name: 'Zinc',
                    value: Math.round(recipe.nutrition?.zinc_mg || 0),
                    unit: 'mg',
                    target: 11,
                    benefit: 'regulates stress response and immune function'
                },
                {
                    name: 'Vitamin D',
                    value: Math.round(recipe.nutrition?.vitamin_d_iu || 0),
                    unit: 'IU',
                    target: 2000,
                    benefit: 'crucial for mood regulation and seasonal depression'
                },
                {
                    name: 'Fiber',
                    value: Math.round(recipe.nutrition?.fiber_g || 0),
                    unit: 'g',
                    target: 28,
                    benefit: 'stabilizes blood sugar and prevents energy crashes'
                }
            ];
            
            // Filter to only show nutrients with non-zero values
            const nonZeroNutrients = nutrients.filter(nutrient => nutrient.value > 0);
            
            // If only fiber has values, provide more comprehensive highlights
            if (nonZeroNutrients.length <= 1) {
                const highlights = [];
                
                // Always include macronutrient benefits
                const calories = Math.round(recipe.nutrition?.calories || 0);
                const protein = Math.round(recipe.nutrition?.protein_g || 0);
                const fiber = Math.round(recipe.nutrition?.fiber_g || 0);
                
                if (calories > 0) {
                    highlights.push(`<li><strong>Energy:</strong> ${calories} calories provide sustained energy for mood stability and focus.</li>`);
                }
                
                if (protein > 0) {
                    highlights.push(`<li><strong>Protein:</strong> ${protein}g supports neurotransmitter production and helps regulate blood sugar levels.</li>`);
                }
                
                if (fiber > 0) {
                    highlights.push(`<li><strong>Fiber:</strong> ${fiber}g stabilizes blood sugar and prevents energy crashes that can affect mood.</li>`);
                }
                
                // Add ingredient-based nutrient benefits
                const ingredients = recipe.ingredients || [];
                const ingredientText = ingredients.map(ing => ing.name.toLowerCase()).join(' ');
                
                if (ingredientText.includes('leafy') || ingredientText.includes('spinach') || ingredientText.includes('kale')) {
                    highlights.push(`<li><strong>Leafy Greens:</strong> Rich in folate, iron, and magnesium for mood support and stress reduction.</li>`);
                }
                
                if (ingredientText.includes('fish') || ingredientText.includes('salmon') || ingredientText.includes('tuna') || ingredientText.includes('mackerel')) {
                    highlights.push(`<li><strong>Omega-3 Fatty Acids:</strong> Anti-inflammatory properties support brain health and mood regulation.</li>`);
                }
                
                if (ingredientText.includes('nuts') || ingredientText.includes('almond') || ingredientText.includes('walnut')) {
                    highlights.push(`<li><strong>Healthy Fats:</strong> Support brain function and help maintain stable mood throughout the day.</li>`);
                }
                
                if (ingredientText.includes('legume') || ingredientText.includes('bean') || ingredientText.includes('lentil') || ingredientText.includes('chickpea')) {
                    highlights.push(`<li><strong>Plant Protein:</strong> Provides amino acids for neurotransmitter synthesis and sustained energy.</li>`);
                }
                
                if (ingredientText.includes('whole grain') || ingredientText.includes('quinoa') || ingredientText.includes('brown rice') || ingredientText.includes('oats')) {
                    highlights.push(`<li><strong>Complex Carbohydrates:</strong> Steady glucose release supports stable mood and energy levels.</li>`);
                }
                
                return highlights.join('');
            }
            
            // Generate HTML for non-zero nutrients
            return nonZeroNutrients.map(nutrient => 
                `<li><strong>${nutrient.name}:</strong> ${nutrient.value} ${nutrient.unit} (target: ${nutrient.target} ${nutrient.unit}) — ${nutrient.benefit}.</li>`
            ).join('');
        }

// Generate detailed rationale with nutritional information
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
    
    // Key nutrients
    if (magnesium > 0) {
        rationaleText += `Rich in magnesium (${magnesium}mg), this recipe supports nervous system function and stress response. `;
    }
    
    if (omega3 > 0) {
        rationaleText += `The ${omega3}g of omega-3 fatty acids provide anti-inflammatory benefits and support mood regulation. `;
    }
    
    if (iron > 0) {
        rationaleText += `With ${iron}mg of iron, it helps maintain energy levels and cognitive function. `;
    }
    
    if (folate > 0) {
        rationaleText += `The ${folate}mcg of folate (B9) is essential for neurotransmitter synthesis and mood stability. `;
    }
    
    if (b12 > 0) {
        rationaleText += `Vitamin B12 (${b12}mcg) supports brain function and helps prevent depression. `;
    }
    
    if (zinc > 0) {
        rationaleText += `Zinc (${zinc}mg) regulates stress response and supports immune function. `;
    }
    
    if (vitaminD > 0) {
        rationaleText += `Vitamin D (${vitaminD}IU) is crucial for mood regulation and helps combat seasonal depression. `;
    }
    
    // Mood-specific benefits
    rationaleText += `This combination of nutrients works synergistically to support your emotional well-being and provide the energy your body needs.`;
    
    return rationaleText;
}

// Get mood emoji
function getMoodEmoji(mood) {
    const moodEmojis = {
        'stressed': '😰',
        'fatigued': '😴',
        'low_mood': '😢',
        'irritable': '😠'
    };
    return moodEmojis[mood.toLowerCase()] || '😊';
}

// Initialize the page when DOM is loaded
document.addEventListener('DOMContentLoaded', generatePage);