// Profile Form Handling

// Load saved profile if exists
window.addEventListener('DOMContentLoaded', () => {
    const savedProfile = sessionStorage.getItem('userProfile');
    if (savedProfile) {
        const profile = JSON.parse(savedProfile);
        loadProfileData(profile);
    }
});

function loadProfileData(profile) {
    document.getElementById('age').value = profile.age || 32;
    document.getElementById('gender').value = profile.gender || 'female';
    document.getElementById('height_cm').value = profile.height_cm || 165;
    document.getElementById('weight_kg').value = profile.weight_kg || 60;
    document.getElementById('dietary_preference').value = profile.dietary_preference || 'none';
    
    // Load cuisines
    if (profile.cuisine_preferences) {
        document.querySelectorAll('input[name="cuisines"]').forEach(checkbox => {
            checkbox.checked = profile.cuisine_preferences.includes(checkbox.value);
        });
    }
    
    // Load allergies
    if (profile.food_allergies && profile.food_allergies.length > 0) {
        document.getElementById('allergies').value = profile.food_allergies.join(', ');
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
    
    // Collect selected cuisines
    const cuisines = [];
    document.querySelectorAll('input[name="cuisines"]:checked').forEach(checkbox => {
        cuisines.push(checkbox.value);
    });
    
    // Parse allergies
    const allergiesText = document.getElementById('allergies').value.trim();
    const allergies = allergiesText ? 
        allergiesText.split(',').map(a => a.trim()).filter(a => a) : 
        [];
    
    // Build profile object
    const profile = {
        age,
        gender,
        height_cm,
        weight_kg,
        cuisine_preferences: cuisines,
        food_allergies: allergies,
        dietary_preference
    };
    
    // Save to sessionStorage
    sessionStorage.setItem('userProfile', JSON.stringify(profile));
    
    console.log('Profile saved:', profile);
    
    // Navigate to mood selection
    window.location.href = '/mood-selection';
}

