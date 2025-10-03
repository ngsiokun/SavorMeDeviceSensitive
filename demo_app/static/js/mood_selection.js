// SavorMe Mood Selection - Functional JavaScript

// State management
let selectedMoods = [];
let selectedIntensity = 'medium';
let userProfile = null;

// Load user profile from sessionStorage
window.addEventListener('DOMContentLoaded', () => {
    const savedProfile = sessionStorage.getItem('userProfile');
    if (savedProfile) {
        userProfile = JSON.parse(savedProfile);
    } else {
        // Redirect to profile page if no profile
        // For demo, use default profile
        userProfile = {
            age: 32,
            gender: 'female',
            height_cm: 165,
            weight_kg: 60,
            cuisine_preferences: ['Mediterranean', 'Italian'],
            food_allergies: [],
            dietary_preference: 'none'
        };
    }
});

// Select mood (called from HTML onclick)
function selectMood(mood) {
    const element = document.querySelector(`[data-mood="${mood}"]`);
    const isSelected = element.classList.contains('selected');
    
    if (isSelected) {
        // Deselect
        element.classList.remove('selected');
        selectedMoods = selectedMoods.filter(m => m !== mood);
    } else {
        // Select (max 3)
        if (selectedMoods.length < 3) {
            element.classList.add('selected');
            selectedMoods.push(mood);
        } else {
            showError('Maximum 3 moods can be selected');
        }
    }
    
    updateCounter();
    updateGenerateButton();
}

// Toggle mood selection (alternative function)
function toggleMood(element) {
    const mood = element.dataset.mood;
    selectMood(mood);
}

// Select intensity (called from HTML onclick)
function selectIntensity(intensity) {
    // Remove selected from all
    document.querySelectorAll('.intensity-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // Add selected to clicked
    const element = document.querySelector(`[data-intensity="${intensity}"]`);
    element.classList.add('selected');
    selectedIntensity = intensity;
}

// Update mood counter
function updateCounter() {
    const counter = document.getElementById('moodCounter');
    const count = selectedMoods.length;
    counter.textContent = `${count} mood${count !== 1 ? 's' : ''} selected (max 3)`;
}

// Update generate button state
function updateGenerateButton() {
    const btn = document.getElementById('generateBtn');
    btn.disabled = selectedMoods.length === 0;
}

// Show error message
function showError(message) {
    alert(message);  // Simple for now, could be a toast notification
}

// Generate recommendation
async function generateRecommendation() {
    if (selectedMoods.length === 0) {
        showError('Please select at least one mood');
        return;
    }
    
    // Show loading
    const loadingIndicator = document.getElementById('loadingIndicator');
    const generateBtn = document.getElementById('generateBtn');
    
    loadingIndicator.style.display = 'block';
    generateBtn.disabled = true;
    
    try {
        // Build request payload
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
        
        console.log('Sending request:', payload);
        
        // Call backend API
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to get recommendation');
        }
        
        const result = await response.json();
        console.log('Recommendation:', result);
        
        // Store result and navigate to results page
        sessionStorage.setItem('recipeResult', JSON.stringify(result));
        sessionStorage.setItem('selectedMoods', JSON.stringify(selectedMoods));
        sessionStorage.setItem('selectedIntensity', selectedIntensity);
        
        window.location.href = '/recipe-result';
        
    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}\n\nMake sure the backend is running at http://localhost:8000`);
    } finally {
        loadingIndicator.style.display = 'none';
        generateBtn.disabled = false;
    }
}

// Initialize
updateGenerateButton();

