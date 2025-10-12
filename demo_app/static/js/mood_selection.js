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
    console.log('Selecting intensity:', intensity); // Debug log
    
    // Remove selected from all intensity buttons
    const allIntensityButtons = document.querySelectorAll('.intensity-btn');
    console.log('Found intensity buttons:', allIntensityButtons.length);
    
    allIntensityButtons.forEach(btn => {
        btn.classList.remove('selected');
        console.log('Removed selected from:', btn.textContent.trim());
    });
    
    // Add selected to clicked button
    const element = document.querySelector(`[data-intensity="${intensity}"]`);
    console.log('Looking for element with data-intensity:', intensity, 'Found:', element);
    
    if (element) {
        element.classList.add('selected');
        selectedIntensity = intensity;
        console.log('✅ Intensity selected:', selectedIntensity);
        console.log('Element classes after selection:', element.className);
    } else {
        console.error('❌ Could not find intensity button for:', intensity);
        console.log('Available intensity buttons:');
        allIntensityButtons.forEach((btn, index) => {
            console.log(`  ${index}: ${btn.textContent.trim()} (data-intensity: ${btn.getAttribute('data-intensity')})`);
        });
    }
}

// Update mood counter
function updateCounter() {
    const counter = document.getElementById('moodCounter');
    const counterDesktop = document.getElementById('moodCounterDesktop');
    const count = selectedMoods.length;
    const counterText = `${count} mood${count !== 1 ? 's' : ''} selected (max 3)`;
    
    if (counter) {
        counter.textContent = counterText;
    }
    if (counterDesktop) {
        counterDesktop.textContent = counterText;
    }
}

// Update generate button state
function updateGenerateButton() {
    const btn = document.getElementById('generateBtn');
    const btnDesktop = document.getElementById('generateBtnDesktop');
    const isDisabled = selectedMoods.length === 0;
    
    if (btn) {
        btn.disabled = isDisabled;
    }
    if (btnDesktop) {
        btnDesktop.disabled = isDisabled;
    }
}

// Show error message
function showError(message) {
    const errorElement = document.getElementById('errorMessage');
    const errorElementDesktop = document.getElementById('errorMessageDesktop');
    
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.add('show');
        setTimeout(() => {
            errorElement.classList.remove('show');
        }, 3000);
    }
    if (errorElementDesktop) {
        errorElementDesktop.textContent = message;
        errorElementDesktop.classList.add('show');
        setTimeout(() => {
            errorElementDesktop.classList.remove('show');
        }, 3000);
    }
}

// Go back to profile page
function goBack() {
    window.location.href = '/profile';
}

// Generate recommendation
async function generateRecommendation() {
    if (selectedMoods.length === 0) {
        showError('Please select at least one mood');
        return;
    }
    
    // Show loading with cute animations
    const loadingIndicator = document.getElementById('loadingIndicator');
    const loadingIndicatorDesktop = document.getElementById('loadingIndicatorDesktop');
    const generateBtn = document.getElementById('generateBtn');
    const generateBtnDesktop = document.getElementById('generateBtnDesktop');
    
    const loadingElement = loadingIndicator || loadingIndicatorDesktop;
    const loadingText = loadingElement ? loadingElement.querySelector('div:last-child') : null;
    
    if (loadingIndicator) {
        loadingIndicator.style.display = 'block';
    }
    if (loadingIndicatorDesktop) {
        loadingIndicatorDesktop.style.display = 'block';
    }
    if (generateBtn) {
        generateBtn.disabled = true;
    }
    if (generateBtnDesktop) {
        generateBtnDesktop.disabled = true;
    }
    
    // Cute loading messages with extended timing
    const loadingMessages = [
        { text: "Finding your perfect recipe...", delay: 0 },
        { text: "Analyzing your mood... 🧠", delay: 3000 },
        { text: "Searching for the best ingredients... 🥬", delay: 6000 },
        { text: "Crafting your personalized recipe... 👨‍🍳", delay: 9000 },
        { text: "Adding a sprinkle of magic... ✨", delay: 12000 },
        { text: "Almost ready... just a moment! 🍽️", delay: 15000 }
    ];
    
    let messageIndex = 0;
    const messageInterval = setInterval(() => {
        if (messageIndex < loadingMessages.length) {
            loadingText.textContent = loadingMessages[messageIndex].text;
            messageIndex++;
        }
    }, 3000);
    
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
        console.log('✅ Recommendation received:', result);
        console.log('🍽️ Recipe name:', result.recipe?.name);
        console.log('🖼️ Image URL from backend:', result.recipe?.image_url);
        console.log('📏 Image URL length:', result.recipe?.image_url?.length || 0);
        console.log('🔗 Full image URL:', result.recipe?.image_url || 'NO IMAGE URL');
        
        // Store result and navigate to results page
        sessionStorage.setItem('recipeResult', JSON.stringify(result));
        sessionStorage.setItem('selectedMoods', JSON.stringify(selectedMoods));
        sessionStorage.setItem('selectedIntensity', selectedIntensity);
        
        window.location.href = '/recipe-result';
        
    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}\n\nMake sure the backend is running at http://127.0.0.1:8000`);
    } finally {
        clearInterval(messageInterval);
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
        if (loadingIndicatorDesktop) {
            loadingIndicatorDesktop.style.display = 'none';
        }
        if (generateBtn) {
            generateBtn.disabled = false;
        }
        if (generateBtnDesktop) {
            generateBtnDesktop.disabled = false;
        }
    }
}

// Initialize
updateGenerateButton();

// Test function availability
console.log('Mood selection JavaScript loaded');
console.log('selectIntensity function available:', typeof selectIntensity === 'function');
console.log('selectMood function available:', typeof selectMood === 'function');

