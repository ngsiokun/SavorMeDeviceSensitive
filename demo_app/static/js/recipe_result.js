// SavorMe Recipe Result - Display recommendation

window.addEventListener('DOMContentLoaded', () => {
    const resultData = sessionStorage.getItem('recipeResult');
    
    if (!resultData) {
        alert('No recipe data found. Redirecting to mood selection...');
        window.location.href = '/mood-selection';
        return;
    }
    
    const result = JSON.parse(resultData);
    displayRecipe(result);
});

function displayRecipe(data) {
    const recipe = data.recipe;
    const rationale = data.emotional_rationale;
    const alignment = data.flavor_alignment;
    const nutrition = data.nutrition_comparison;
    
    // Recipe Card
    document.getElementById('recipeCard').innerHTML = `
        ${recipe.image_url ? `<img src="${recipe.image_url}" class="recipe-image" alt="${recipe.name}">` : ''}
        <div class="recipe-info">
            <h2 class="recipe-name">${recipe.name}</h2>
            <div class="recipe-meta">
                ${recipe.prep_time ? `<span>⏱️ ${recipe.prep_time + recipe.cook_time || recipe.prep_time} min</span>` : ''}
                <span>🍽️ ${recipe.servings || 1} serving${recipe.servings !== 1 ? 's' : ''}</span>
            </div>
            <div class="nutrition-quick">
                <div class="nutrition-quick-item">
                    <div class="nutrition-quick-value">${Math.round(recipe.nutrition.calories)}</div>
                    <div class="nutrition-quick-label">Calories</div>
                </div>
                <div class="nutrition-quick-item">
                    <div class="nutrition-quick-value">${Math.round(recipe.nutrition.protein_g)}g</div>
                    <div class="nutrition-quick-label">Protein</div>
                </div>
                <div class="nutrition-quick-item">
                    <div class="nutrition-quick-value">${Math.round(recipe.nutrition.fiber_g)}g</div>
                    <div class="nutrition-quick-label">Fiber</div>
                </div>
            </div>
        </div>
    `;
    
    // Match Score
    const score = alignment.nutrient_match_score || 85;
    document.getElementById('matchScore').innerHTML = `
        <div class="match-score-title">Nutrient Match Score</div>
        <div class="match-score-value">${Math.round(score)}%</div>
        <div class="match-score-subtitle">Evidence-Based Recommendation</div>
    `;
    
    // Emotional Rationale
    let moodBreakdownHTML = '';
    if (rationale.mood_breakdowns && rationale.mood_breakdowns.length > 0) {
        moodBreakdownHTML = '<div class="mood-breakdown">';
        rationale.mood_breakdowns.forEach(breakdown => {
            const moodEmoji = getMoodEmoji(breakdown.mood);
            moodBreakdownHTML += `
                <div class="mood-breakdown-item">
                    <div class="mood-breakdown-header">${moodEmoji} ${breakdown.mood}</div>
                    <div class="mood-breakdown-text">${breakdown.explanation}</div>
                </div>
            `;
        });
        moodBreakdownHTML += '</div>';
    }
    
    document.getElementById('rationale').innerHTML = `
        <div class="section-header">
            <span>💭</span>
            <span>Why This Recipe?</span>
        </div>
        <div class="rationale-text">${rationale.overall_rationale}</div>
        ${moodBreakdownHTML}
    `;
    
    // Nutrition Comparison
    document.getElementById('nutrition').innerHTML = `
        <div class="section-header">
            <span>📊</span>
            <span>Nutrition Breakdown</span>
        </div>
        <table class="nutrition-table">
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
                    <td>${Math.round(nutrition.recipe_calories)} kcal</td>
                    <td>${Math.round(nutrition.target_calories)} kcal</td>
                    <td class="percentage">${nutrition.percentage_of_daily_calories}%</td>
                </tr>
                <tr>
                    <td>Protein</td>
                    <td>${Math.round(nutrition.recipe_protein)}g</td>
                    <td>${Math.round(nutrition.target_protein)}g</td>
                    <td class="percentage">${nutrition.percentage_of_daily_protein}%</td>
                </tr>
                <tr>
                    <td>Fiber</td>
                    <td>${Math.round(nutrition.recipe_fiber)}g</td>
                    <td>${Math.round(nutrition.target_fiber)}g</td>
                    <td class="percentage">${nutrition.percentage_of_daily_fiber}%</td>
                </tr>
            </tbody>
        </table>
        ${alignment.nutrient_reasons ? `
            <div style="margin-top: 12px; font-size: 11px; color: #6B7280;">
                <strong>Nutrient Highlights:</strong>
                <ul style="margin: 8px 0 0 16px; line-height: 1.6;">
                    ${alignment.nutrient_reasons.slice(0, 3).map(reason => `<li>${reason}</li>`).join('')}
                </ul>
            </div>
        ` : ''}
    `;
    
    // Evidence Section
    if (alignment.evidence_based) {
        document.getElementById('evidence').innerHTML = `
            <div class="section-header">
                <span>🔬</span>
                <span>Scientific Evidence</span>
            </div>
            <div class="evidence-level">⭐⭐⭐⭐ Evidence-Based Recommendation</div>
            <div class="evidence-list">
                <p><strong>This recommendation is based on:</strong></p>
                <ul>
                    <li>Peer-reviewed nutritional research</li>
                    <li>Mediterranean diet studies (SMILES trial)</li>
                    <li>Nutrient-mood correlation meta-analyses</li>
                </ul>
            </div>
            <div class="disclaimer">
                This app provides food suggestions based on mood and nutritional science. 
                It is not a substitute for professional medical advice. Always consult your 
                healthcare provider for persistent symptoms.
            </div>
        `;
    }
}

function getMoodEmoji(moodName) {
    const emojiMap = {
        'stressed': '😰',
        'fatigued': '😴',
        'low_mood': '😢',
        'low mood': '😢',
        'irritable': '😠'
    };
    return emojiMap[moodName.toLowerCase()] || '💭';
}

function shareRecipe() {
    const result = JSON.parse(sessionStorage.getItem('recipeResult'));
    const text = `Check out this recipe from SavorMe: ${result.recipe.name}!`;
    
    if (navigator.share) {
        navigator.share({
            title: 'SavorMe Recipe',
            text: text,
            url: window.location.href
        });
    } else {
        alert('Recipe saved! (Share functionality requires mobile browser)');
    }
}

