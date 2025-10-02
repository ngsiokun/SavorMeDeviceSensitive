// Profile Form Handling

// Load saved profile if exists
window.addEventListener('DOMContentLoaded', () => {
    const savedProfile = sessionStorage.getItem('userProfile');
    if (savedProfile) {
        const profile = JSON.parse(savedProfile);
        loadProfileData(profile);
    }
    
    // Set up calorie preference event listeners
    setupCaloriePreferenceHandlers();
});

function setupCaloriePreferenceHandlers() {
    const calorieAuto = document.getElementById('calorie_auto');
    const calorieCustom = document.getElementById('calorie_custom');
    const customCalorieGroup = document.getElementById('customCalorieGroup');
    
    calorieAuto.addEventListener('change', () => {
        customCalorieGroup.style.display = 'none';
    });
    
    calorieCustom.addEventListener('change', () => {
        customCalorieGroup.style.display = 'block';
    });
    
    // Add validation for custom calories
    const customCaloriesInput = document.getElementById('custom_calories');
    customCaloriesInput.addEventListener('input', validateCalories);
}

function validateCalories() {
    const input = document.getElementById('custom_calories');
    const value = parseInt(input.value);
    
    // Remove existing warning
    const existingWarning = document.querySelector('.calorie-warning');
    if (existingWarning) {
        existingWarning.remove();
    }
    
    if (value && value < 800) {
        // Create warning message
        const warning = document.createElement('div');
        warning.className = 'calorie-warning';
        warning.innerHTML = '⚠️ Very low calorie targets should be discussed with a healthcare provider for safety.';
        warning.style.cssText = 'color: #F59E0B; font-size: 11px; margin-top: 4px; padding: 6px; background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 6px;';
        
        // Insert after the input field
        input.parentNode.insertBefore(warning, input.nextSibling);
    }
}

function loadProfileData(profile) {
    document.getElementById('age').value = profile.age || 32;
    document.getElementById('gender').value = profile.gender || 'female';
    document.getElementById('height_cm').value = profile.height_cm || 165;
    document.getElementById('weight_kg').value = profile.weight_kg || 60;
    document.getElementById('dietary_preference').value = profile.dietary_preference || 'none';
    
    // Load cuisine (single selection)
    if (profile.cuisine_preferences && profile.cuisine_preferences.length > 0) {
        document.getElementById('cuisine').value = profile.cuisine_preferences[0];
    }
    
    // Load allergies
    if (profile.food_allergies && profile.food_allergies.length > 0) {
        document.getElementById('allergies').value = profile.food_allergies.join(', ');
    }
    
    // Load calorie preferences
    if (profile.calorie_preference) {
        document.querySelector(`input[name="calorie_preference"][value="${profile.calorie_preference}"]`).checked = true;
        if (profile.calorie_preference === 'custom' && profile.custom_calories) {
            document.getElementById('custom_calories').value = profile.custom_calories;
            document.getElementById('customCalorieGroup').style.display = 'block';
        }
    }
}

function saveProfile(event) {
    event.preventDefault();
    
    // Collect form data
    const age = parseInt(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const height_cm = parseFloat(document.getElementById('height_cm').value);
    const weight_kg = parseFloat(document.getElementById('weight_kg').value);
    const dietary_preference = document.getElementById('dietary_preference').value;
    
    // Get selected cuisine (single selection)
    const cuisine = document.getElementById('cuisine').value;
    const cuisines = cuisine === "Surprise Me" ? [] : [cuisine];
    
    // Parse allergies
    const allergiesText = document.getElementById('allergies').value.trim();
    const allergies = allergiesText ? 
        allergiesText.split(',').map(a => a.trim()).filter(a => a) : 
        [];
    
    // Get calorie preference
    const caloriePreference = document.querySelector('input[name="calorie_preference"]:checked').value;
    const customCalories = caloriePreference === 'custom' ? 
        parseInt(document.getElementById('custom_calories').value) : null;
    
    // Build profile object
    const profile = {
        age,
        gender,
        height_cm,
        weight_kg,
        cuisine_preferences: cuisines,
        food_allergies: allergies,
        dietary_preference,
        calorie_preference: caloriePreference,
        custom_calories: customCalories
    };
    
    // Save to sessionStorage
    sessionStorage.setItem('userProfile', JSON.stringify(profile));
    
    console.log('Profile saved:', profile);
    
    // Navigate to mood selection
    window.location.href = '/mood-selection';
}

