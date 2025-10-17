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
    // --- CRITICAL FIX START ---
    // Use the EXACT IDs found in your browser's DevTools "Elements" tab for the *rendered* HTML.
    // Based on your console and screenshot, these appear to be 'calorie_auto-desktop' and 'calorie_custom-desktop'.
    // Check for mobile first, then desktop
    const calorieAuto = document.getElementById('calorie_auto') || document.getElementById('calorie_auto-desktop');
    const calorieCustom = document.getElementById('calorie_custom') || document.getElementById('calorie_custom-desktop');
    // --- CRITICAL FIX END ---

    const customCalorieGroup = document.getElementById('customCalorieGroup') || document.getElementById('customCalorieGroupDesktop');
    
    if (!calorieAuto || !calorieCustom || !customCalorieGroup) {
        console.error('Calorie preference elements not found. Check IDs in HTML and JS (`profile.js`).');
        console.error('  Expected Auto ID (JS): calorie_auto-desktop, Found:', calorieAuto ? calorieAuto.id : 'Not Found');
        console.error('  Expected Custom ID (JS): calorie_custom-desktop, Found:', calorieCustom ? calorieCustom.id : 'Not Found');
        console.error('  Expected Custom Group ID (JS): customCalorieGroupDesktop, Found:', customCalorieGroup ? customCalorieGroup.id : 'Not Found');
        return;
    }

    // Add null checks and better debugging
    console.log('🔍 Found elements:');
    console.log('  calorieAuto:', calorieAuto ? calorieAuto.id : 'Not Found');
    console.log('  calorieCustom:', calorieCustom ? calorieCustom.id : 'Not Found');
    console.log('  customCalorieGroup:', customCalorieGroup ? customCalorieGroup.id : 'Not Found');

    // Simplified and more robust visibility control
    function updateCustomInputVisibility() {
        console.log('--- Debugging updateCustomInputVisibility ---');
        console.log('calorieAuto.checked:', calorieAuto ? calorieAuto.checked : 'N/A');
        console.log('calorieCustom.checked:', calorieCustom ? calorieCustom.checked : 'N/A');

        // Find the correct custom calorie group (mobile or desktop)
        const customCalorieGroupMobile = document.getElementById('customCalorieGroup');
        const customCalorieGroupDesktop = document.getElementById('customCalorieGroupDesktop');
        const targetGroup = customCalorieGroupMobile || customCalorieGroupDesktop;
        
        console.log('Found customCalorieGroupMobile:', !!customCalorieGroupMobile);
        console.log('Found customCalorieGroupDesktop:', !!customCalorieGroupDesktop);
        console.log('Using targetGroup:', targetGroup ? targetGroup.id : 'None');
        
        if (calorieCustom && calorieCustom.checked) {
            if (targetGroup) {
                targetGroup.classList.add('show');
                console.log('✅ Custom selected, showing custom input.');
            } else {
                console.error('❌ Custom calorie group not found!');
            }
        } else {
            if (targetGroup) {
                targetGroup.classList.remove('show');
                console.log('Auto selected or nothing selected, hiding custom input.');
            }
        }
        console.log('--- End Debugging updateCustomInputVisibility ---');
    }
    
    // Listen to both 'change' and 'click' events for maximum reliability
    calorieAuto.addEventListener('change', updateCustomInputVisibility);
    calorieCustom.addEventListener('change', updateCustomInputVisibility);
    calorieAuto.addEventListener('click', updateCustomInputVisibility);
    calorieCustom.addEventListener('click', updateCustomInputVisibility);
    
    // Set initial state on page load
    updateCustomInputVisibility();
    
    // Refine the click handler on parent divs:
    // Its primary role should be to click the radio button, and let the radio's 'change' event handle visibility.
    document.querySelectorAll('.calorie-option').forEach(optionDiv => {
        optionDiv.addEventListener('click', function(event) {
            const radio = this.querySelector('input[type="radio"]');
            console.log('Calorie option div clicked. Radio inside:', radio ? radio.id : 'None');
            if (radio && !radio.checked) {
                radio.checked = true; // Manually check the radio button
                // No need to call updateCustomInputVisibility() here directly.
                // The `change` event listener on `radio` (which is `calorieAuto` or `calorieCustom`)
                // will now fire and call `updateCustomInputVisibility()` asynchronously,
                // ensuring the DOM has updated and `radio.checked` is correct.
            }
        });
    });
    
    // Initialize visibility based on the default checked radio button
    updateCustomInputVisibility();
    
    // Add validation for custom calories (both mobile and desktop)
    const customCaloriesInput = document.getElementById('custom_calories');
    const customCaloriesInputDesktop = document.getElementById('custom_calories-desktop');
    
    if (customCaloriesInput) {
        customCaloriesInput.addEventListener('input', validateCalories);
    }
    if (customCaloriesInputDesktop) {
        customCaloriesInputDesktop.addEventListener('input', validateCalories);
    }
}

function validateCalories() {
    const input = document.getElementById('custom_calories') || document.getElementById('custom_calories-desktop');
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
    
    // Validate custom calories (800 kcal minimum warning)
    if (caloriePreference === 'custom' && customCalories < 800) {
        // Show warning but allow continuation
        const warningMessage = "Usually a meal of 800 kcal or more is recommended";
        alert(warningMessage + "\n\nYou can continue, but consider increasing your calorie target for better nutrition.");
        console.log('Custom calorie warning:', customCalories, 'kcal (< 800 recommended)');
    }
    
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

