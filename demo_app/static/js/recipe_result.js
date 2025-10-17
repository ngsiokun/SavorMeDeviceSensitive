// SavorMe Recipe Result - Pure JavaScript Dynamic Page Generation
// Matching the beautiful design from the first screenshot

// Clear any cached images to prevent mismatches
function clearImageCache() {
    const images = document.querySelectorAll('img.recipe-image');
    images.forEach(img => {
        img.src = '';
        img.remove();
    });
}

// Main function to generate the entire page
function generatePage() {
    // Clear any existing images to prevent caching issues
    clearImageCache();
    const container = document.getElementById('app-container');
    
    // Get recipe data from session storage
    const resultData = sessionStorage.getItem('recipeResult');
    
    console.log('🔍 DEBUG: Loading recipe from sessionStorage');
    console.log('📦 Recipe data exists:', !!resultData);
    
    if (!resultData) {
        container.innerHTML = generateErrorPage();
        return;
    }
    
    try {
    const result = JSON.parse(resultData);
        console.log('🍽️ Recipe name:', result.recipe?.name);
        console.log('🖼️ Image URL:', result.recipe?.image_url);
        console.log('📸 Image URL length:', result.recipe?.image_url?.length || 0);
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
    
    // Generate image HTML with smart validation and contextual placeholders
    let imageHTML = '';
    
    // Trust Edamam images completely - they are reliable recipe image sources
    // Only validate that it's a real URL from Edamam
    const hasValidEdamamImage = recipe.image_url && 
                               recipe.image_url.includes('edamam-product-images.s3.amazonaws.com') &&
                               (recipe.image_url.startsWith('http') || recipe.image_url.startsWith('https'));
    
    // Use Edamam image if it's valid, otherwise use Unsplash
    const hasValidImage = hasValidEdamamImage;
    
    // Log what Edamam provided
    console.log('🔍 Edamam image analysis:');
    console.log('  - Image URL exists:', !!recipe.image_url);
    console.log('  - Image URL length:', recipe.image_url?.length || 0);
    console.log('  - Is SVG placeholder:', recipe.image_url?.includes('data:image/svg') || false);
    console.log('  - Is base64:', recipe.image_url?.includes('base64') || false);
    console.log('  - Starts with http:', recipe.image_url?.startsWith('http') || false);
    console.log('  - Valid Edamam image:', hasValidEdamamImage);
    
    if (!hasValidImage && !recipe.image_url) {
        console.log('🖼️ Image URL is null, using Unsplash fallback');
    } else if (!hasValidImage && recipe.image_url) {
        if (recipe.image_url.length > 2000) {
            console.log(`🖼️ Image URL too long (${recipe.image_url.length} chars), using Unsplash fallback`);
        } else if (recipe.image_url.includes('data:image/svg') || recipe.image_url.includes('base64')) {
            console.log('🖼️ Image URL is base64 SVG placeholder, using Unsplash fallback');
        } else if (!recipe.image_url.startsWith('http')) {
            console.log('🖼️ Image URL is not a valid HTTP URL, using Unsplash fallback');
        } else {
            console.log('🖼️ Image URL failed validation, using Unsplash fallback');
        }
    }
    
    if (hasValidImage) {
        imageHTML = `
            <img src="${recipe.image_url}" class="recipe-image" alt="${recipe.name}" 
                 onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                     <div class="recipe-image-placeholder" style="display: none;">
                         ${generateContextualPlaceholder(recipe)}
            </div>
        `;
    } else {
        // Use Unsplash fallback image - select based on recipe type
        const recipeName = recipe.name.toLowerCase();
        const ingredients = (recipe.ingredients || []).map(ing => ing.name.toLowerCase()).join(' ');
        
        let selectedImage;
        
        // Smart image selection based on recipe type - REFINED LOGIC
        const combined = recipeName + ' ' + ingredients;
        
        // DEBUG: Log the combined string for debugging
        console.log(`🔍 DEBUG: Combined string for image matching: "${combined}"`);
        
        // Define keywords with PRIORITY ORDER - most specific first
        // HIGH PRIORITY: Specific ingredients that should override generic matches
        const avocadoKeywords = ['avocado', 'avocados', 'guacamole'];
        const chardKeywords = ['chard', 'swiss chard', 'rainbow chard'];
        const leafyGreenKeywords = ['spinach', 'kale', 'arugula', 'lettuce', 'greens', 'chard', 'swiss chard'];
        const porkKeywords = ['pork', 'pork loin', 'pork roast', 'pork chop', 'pork tenderloin', 'pork shoulder', 'pork belly'];
        const cauliflowerKeywords = ['cauliflower', 'cauliflower rice', 'cauliflower mash', 'roasted cauliflower', 'cauliflower florets'];
        const tunaKeywords = ['tuna', 'tuna steak', 'tuna salad', 'tuna fish', 'albacore', 'yellowfin', 'bluefin'];
        const beansKeywords = ['beans', 'kidney beans', 'black beans', 'pinto beans', 'white beans', 'cannellini beans', 'navy beans'];
        
        // MEDIUM PRIORITY: Specific dish types
        const pizzaKeywords = ['pizza', 'calzone', 'flatbread'];
        const sandwichKeywords = ['sandwich', 'panini', 'wrap', 'sub', 'burger', 'grilled cheese', 'club sandwich'];
        const pastaKeywords = ['pasta', 'spaghetti', 'linguine', 'penne', 'noodles', 'fettuccine', 'ravioli', 'macaroni', 'lasagna'];
        const chiliKeywords = ['chili', 'poblano chili', 'con carne'];
        const soupKeywords = ['soup', 'chowder', 'broth', 'bisque', 'consommé'];
        const stewKeywords = ['stew', 'casserole', 'braised', 'goulash', 'curry'];
        const vegetarianKeywords = ['vegetarian', 'vegan', 'plant-based', 'salad', 'vegetables', 'falafel', 'lentil', 'chickpea', 'eggplant', 'squash', 'stuffed eggplant', 'baked eggplant'];
        const tofuKeywords = ['tofu', 'firm tofu', 'silken tofu', 'bean curd'];
        const fishSeafoodKeywords = ['fish', 'salmon', 'tuna', 'cod', 'shrimp', 'prawn', 'seafood', 'lobster', 'crab'];
        const salmonKeywords = ['salmon', 'grilled salmon', 'baked salmon', 'salmon fillet'];
        const grilledMeatKeywords = ['grilled', 'bbq', 'barbecue', 'kebab', 'skewer', 'chops'];
        const meatballKeywords = ['meatball', 'kofta'];
        const generalMeatKeywords = ['lamb', 'beef', 'pork', 'steak', 'burger', 'chicken', 'turkey', 'ribs', 'bacon', 'sausage'];
        
        const saladKeywords = ['salad', 'lettuce', 'greens', 'arugula', 'spinach salad', 'coleslaw', 'asian salad', 'turkey salad', 'pasta salad', 'quinoa salad', 'vegan salad'];
        const dessertKeywords = ['dessert', 'sweet', 'cake', 'pie', 'compote', 'jam', 'jelly', 'preserve', 'apricot', 'fruit', 'berries', 'chocolate', 'ice cream', 'pudding', 'tart', 'muffin', 'cookie', 'brownie', 'cheesecake'];
        
        // LOW PRIORITY: Generic ingredients (only match if no specific match found)
        const riceKeywords = ['rice', 'fried rice', 'brown rice', 'white rice', 'basmati', 'jasmine', 'wild rice', 'rice bowl', 'rice dish'];
        const eggKeywords = ['egg', 'eggs', 'fried egg', 'scrambled egg', 'poached egg', 'boiled egg', 'omelet', 'omelette'];
        const quinoaKeywords = ['quinoa', 'quinoa bowl', 'quinoa salad', 'quinoa dish'];
        const lentilKeywords = ['lentils', 'lentil soup', 'lentil curry', 'lentil stew', 'one-pot lentils'];
        
        let matchedCategory = 'default';
        
        // 1. HIGHEST PRIORITY: Specific ingredients (avocado, chard, leafy greens, pork, cauliflower)
        if (avocadoKeywords.some(keyword => combined.includes(keyword)) || chardKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1512621776951-a5739a2d21ae?w=1200&h=600&fit=crop&auto=format"; // Avocado/Chard dishes
            matchedCategory = 'avocado_chard';
        } else if (porkKeywords.some(keyword => combined.includes(keyword)) && cauliflowerKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=1200&h=600&fit=crop&auto=format"; // Pork with cauliflower dishes
            matchedCategory = 'pork_cauliflower';
        } else if (porkKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&h=600&fit=crop&auto=format"; // Pork dishes
            matchedCategory = 'pork_dishes';
        } else if (tunaKeywords.some(keyword => combined.includes(keyword)) && beansKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=1200&h=600&fit=crop&auto=format"; // Tuna and beans dishes
            matchedCategory = 'tuna_beans';
        } else if (tunaKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&h=600&fit=crop&auto=format"; // Tuna dishes
            matchedCategory = 'tuna_dishes';
        } else if (cauliflowerKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=1200&h=600&fit=crop&auto=format"; // Cauliflower dishes
            matchedCategory = 'cauliflower_dishes';
        } else if (leafyGreenKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=1200&h=600&fit=crop&auto=format"; // Leafy green dishes
            matchedCategory = 'leafy_greens';
        } else if (dessertKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=1200&h=600&fit=crop&auto=format"; // Dessert
            matchedCategory = 'dessert';
        } else if (lentilKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=1200&h=600&fit=crop&auto=format"; // Lentil dishes
            matchedCategory = 'lentil';
        } else if (quinoaKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1512621776951-a5739a2d21ae?w=1200&h=600&fit=crop&auto=format"; // Quinoa dishes
            matchedCategory = 'quinoa';
        } else if (riceKeywords.some(keyword => combined.includes(keyword)) && eggKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=1200&h=600&fit=crop&auto=format"; // Rice + Egg dishes
            matchedCategory = 'rice_egg';
        } else if (riceKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=1200&h=600&fit=crop&auto=format"; // Rice dishes
            matchedCategory = 'rice';
        } else if (eggKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1512621776951-a5739a2d21ae?w=1200&h=600&fit=crop&auto=format"; // Egg dishes
            matchedCategory = 'egg';
        } else if (beansKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=1200&h=600&fit=crop&auto=format"; // Bean dishes
            matchedCategory = 'beans';
        } else if (sandwichKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=1200&h=600&fit=crop&auto=format"; // Sandwich/Panini
            matchedCategory = 'sandwich';
        } else if (pizzaKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1593560704721-db25271a3615?w=1200&h=600&fit=crop&auto=format"; // Pizza
            matchedCategory = 'pizza';
        } else if (saladKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=1200&h=600&fit=crop&auto=format"; // Salad - Higher priority
            matchedCategory = 'salad';
        } else if (pastaKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1588726231922-26154562c55b?w=1200&h=600&fit=crop&auto=format"; // Pasta - New reliable URL
            matchedCategory = 'pasta';
        }
        // 2. Distinct liquid/sauced dishes (Chili, Soup, Stew)
        else if (chiliKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1550965020-03ee3ce56ad2?w=1200&h=600&fit=crop&auto=format"; // Chili
            matchedCategory = 'chili';
        } else if (soupKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=1200&h=600&fit=crop&auto=format"; // Soup
            matchedCategory = 'soup';
        } else if (stewKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1543353071-872f771f7679?w=1200&h=600&fit=crop&auto=format"; // Stew
            matchedCategory = 'stew';
        }
        // 3. Specific components/dietary categories
        else if (vegetarianKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1512621776951-a5739a2d21ae?w=1200&h=600&fit=crop&auto=format"; // Vegetarian - Working URL
            matchedCategory = 'vegetarian';
        } else if (tofuKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=1200&h=600&fit=crop&auto=format"; // Tofu
            matchedCategory = 'tofu';
        } else if (salmonKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=1200&h=600&fit=crop&auto=format"; // Salmon - Proper salmon dish image
            matchedCategory = 'salmon';
        } else if (fishSeafoodKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1574484284002-952d92456975?w=1200&h=600&fit=crop&auto=format"; // Fish - General fish image
            matchedCategory = 'fish_seafood';
        } else if (meatballKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1533038668700-1c056d61034f?w=1200&h=600&fit=crop&auto=format"; // Meatballs
            matchedCategory = 'meatball';
        } else if (grilledMeatKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=1200&h=600&fit=crop&auto=format"; // Grilled meat/BBQ
            matchedCategory = 'grilled_meat';
        }
        // 4. General fallback meat category
        else if (generalMeatKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&h=600&fit=crop&auto=format"; // General meat
            matchedCategory = 'general_meat';
        } else if (saladKeywords.some(keyword => combined.includes(keyword))) {
            selectedImage = "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=1200&h=600&fit=crop&auto=format"; // Salad
            matchedCategory = 'salad';
        } else {
            // Generic healthy bowl - Better default image for rice/egg dishes
            selectedImage = "https://images.unsplash.com/photo-1512621776951-a5739a2d21ae?w=1200&h=600&fit=crop&auto=format";
            matchedCategory = 'default';
        }
        
        console.log(`🔍 Recipe: "${recipe.name}"`);
        console.log(`🔍 Matched category: ${matchedCategory}`);
        console.log(`🔍 Keywords checked: ${combined.substring(0, 150)}...`);
        
        // Debug: Check if our new keywords are being matched
        console.log(`🔍 Debug - Rice keywords match:`, riceKeywords.some(keyword => combined.includes(keyword)));
        console.log(`🔍 Debug - Egg keywords match:`, eggKeywords.some(keyword => combined.includes(keyword)));
        console.log(`🔍 Debug - Beans keywords match:`, beansKeywords.some(keyword => combined.includes(keyword)));
        
        // Add aggressive cache busting to force fresh image load
        const cacheBuster = Date.now();
        const randomId = Math.random().toString(36).substring(7);
        const imageUrlWithCache = `${selectedImage}&t=${cacheBuster}&r=${randomId}&v=2`;
        
        // Reliable image URLs for each category (manually verified)
        const reliableImageUrls = {
            'egg': 'https://images.unsplash.com/photo-1512621776951-a5739a2d21ae?w=1200&h=600&fit=crop&auto=format',
            'rice_egg': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=1200&h=600&fit=crop&auto=format',
            'rice': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=1200&h=600&fit=crop&auto=format',
            'beans': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=1200&h=600&fit=crop&auto=format',
            'lentil': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=1200&h=600&fit=crop&auto=format',
            'quinoa': 'https://images.unsplash.com/photo-1512621776951-a5739a2d21ae?w=1200&h=600&fit=crop&auto=format',
            'salad': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=1200&h=600&fit=crop&auto=format',
            'fish_seafood': 'https://images.unsplash.com/photo-1574484284002-952d92456975?w=1200&h=600&fit=crop&auto=format',
            'default': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200&h=600&fit=crop&auto=format'
        };
        
        // Use reliable image for the matched category
        const reliableImage = reliableImageUrls[matchedCategory] || reliableImageUrls['default'];
        const finalImageUrl = reliableImage + `&t=${cacheBuster}&r=${randomId}&v=2`;
        
        console.log(`✅ Using reliable image for ${recipe.name}: ${finalImageUrl}`);
        console.log(`🔍 Category: ${matchedCategory} | Recipe: ${recipe.name}`);
        
        // Image loading with inline fallback logic
        
        imageHTML = `
            <img src="${finalImageUrl}" class="recipe-image" alt="${recipe.name}" style="width: 100%; height: auto; object-fit: cover;" loading="eager" 
                 onload="console.log('✅ Image loaded successfully:', this.src)" 
                 onerror="console.error('❌ Failed to load image:', this.src); this.style.display='none'; this.nextElementSibling.style.display='flex';">
            <div class="recipe-image-placeholder" style="display: none;">
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; background: #f0f9ff; color: #065f46; padding: 20px; text-align: center; border-radius: 8px;">
                    <div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">${recipe.name}</div>
                    <div style="font-size: 16px; color: #6b7280;">🍽️ Recipe Image</div>
                    <div style="font-size: 12px; color: #9ca3af;">Image from Web</div>
                </div>
            </div>
        `;
        
        console.log(`🖼️ Final image HTML:`, imageHTML);
    }
    
    return `
        <!-- Mobile/Tablet Layout (Phone Mockup) -->
        <div class="app-container">
            <div class="phone-mockup">
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
                
                <!-- Go Back Button -->
                <button class="back-btn" onclick="goBack()">
                    ← Go Back
                </button>
                </div>
            </div>
        </div>

        <!-- Desktop Layout (Full Web Layout) -->
        <div class="desktop-layout">
            <div class="desktop-content">
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
                
                <!-- Go Back Button -->
                <button class="back-btn" onclick="goBack()">
                    ← Go Back
                </button>
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
    // Nutrient Match Score buttons (both mobile and desktop)
    const nutrientMatchBtns = document.querySelectorAll('.nutrient-match-btn');
    console.log('Found', nutrientMatchBtns.length, 'nutrient match buttons');
    nutrientMatchBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            console.log('Nutrient Match Score button clicked!');
            // Show detailed nutrition analysis
            showNutrientAnalysis();
        });
    });
    
    // Retry button (for error state)
    const retryBtn = document.getElementById('retry-btn');
    if (retryBtn) {
        retryBtn.addEventListener('click', () => {
            window.location.href = '/mood-selection';
        });
    }
}

// Go back to mood selection page
function goBack() {
    window.location.href = '/mood-selection';
}

// Go back from modal (close modal first, stay on recipe page)
function goBackFromModal() {
    closeNutrientModal();
    // Stay on the current recipe page - don't navigate away
}

// Image validation logic to detect only OBVIOUS mismatched recipe images
function isImageMismatched(recipe) {
    if (!recipe.image_url) return true;
    
    const imageUrl = recipe.image_url.toLowerCase();
    
    // Only flag EXTREMELY obvious mismatches - be very conservative
    // Check for logo/brand images instead of food
    const logoKeywords = ['logo', 'brand', 'food network', 'allrecipes', 'tasteofhome'];
    const hasLogoKeywords = logoKeywords.some(keyword => 
        imageUrl.includes(keyword)
    );
    
    if (hasLogoKeywords) {
        console.log('🚨 Flagged logo image:', recipe.name);
        return true;
    }
    
    // Only flag if it's a single ingredient photo for a complex recipe
    const singleIngredientKeywords = ['garlic-cloves', 'rosemary-sprigs', 'single-carrot'];
    const hasSingleIngredient = singleIngredientKeywords.some(keyword => 
        imageUrl.includes(keyword)
    );
    
    // Only flag if it's clearly a single ingredient AND a complex multi-ingredient recipe
    if (hasSingleIngredient && recipe.ingredients && recipe.ingredients.length > 5) {
        console.log('🚨 Flagged single ingredient image for complex recipe:', recipe.name);
        return true;
    }
    
    // For now, let most images through - only catch the most obvious mismatches
    return false;
}

// Generate contextual placeholder based on recipe type
function generateContextualPlaceholder(recipe) {
    const recipeTitle = recipe.name.toLowerCase();
    const ingredients = (recipe.ingredients || []).map(ing => ing.name.toLowerCase()).join(' ');
    
    // Determine recipe category
    if (recipeTitle.includes('beef') || recipeTitle.includes('chicken') || 
        recipeTitle.includes('pork') || recipeTitle.includes('meat') ||
        ingredients.includes('beef') || ingredients.includes('chicken')) {
        return `
            <div class="placeholder-icon">🍖</div>
            <div class="placeholder-text">${recipe.name}</div>
            <div class="placeholder-subtitle">Meat Dish</div>
        `;
    } else if (recipeTitle.includes('dessert') || recipeTitle.includes('cake') || 
               recipeTitle.includes('cookie') || recipeTitle.includes('sweet') ||
               ingredients.includes('sugar') || ingredients.includes('chocolate')) {
        return `
            <div class="placeholder-icon">🍰</div>
            <div class="placeholder-text">${recipe.name}</div>
            <div class="placeholder-subtitle">Dessert</div>
        `;
    } else if (recipeTitle.includes('salad') || ingredients.includes('lettuce') || 
               ingredients.includes('vegetables')) {
        return `
            <div class="placeholder-icon">🥗</div>
            <div class="placeholder-text">${recipe.name}</div>
            <div class="placeholder-subtitle">Fresh Salad</div>
        `;
    } else if (recipeTitle.includes('soup') || recipeTitle.includes('stew') || 
               ingredients.includes('broth')) {
        return `
            <div class="placeholder-icon">🍲</div>
            <div class="placeholder-text">${recipe.name}</div>
            <div class="placeholder-subtitle">Hearty Soup</div>
        `;
    } else if (recipeTitle.includes('pasta') || ingredients.includes('pasta') || 
               ingredients.includes('noodles')) {
        return `
            <div class="placeholder-icon">🍝</div>
            <div class="placeholder-text">${recipe.name}</div>
            <div class="placeholder-subtitle">Pasta Dish</div>
        `;
    } else {
        // Generic fallback
        return `
            <div class="placeholder-icon">🥘</div>
            <div class="placeholder-text">${recipe.name}</div>
            <div class="placeholder-subtitle">Delicious Recipe</div>
        `;
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
                            <button class="back-btn" onclick="goBackFromModal()">← Go Back</button>
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

        // Generate nutrient highlights with target values for mood-supporting nutrients
        function generateNutrientHighlights(recipe) {
            const nutrients = [
                {
                    name: 'Magnesium',
                    value: Math.round(recipe.nutrition?.magnesium_mg || 0),
                    unit: 'mg',
                    target: 120,
                    benefit: 'supports nervous system and stress response',
                    moodImportance: 'Critical for stress management and muscle relaxation'
                },
                {
                    name: 'Omega 3 EPA DHA',
                    value: Math.round((recipe.nutrition?.omega3_g || 0) * 10) / 10,
                    unit: 'g',
                    target: 2.0,
                    benefit: 'anti-inflammatory, supports mood regulation',
                    moodImportance: 'Essential for brain health and depression prevention'
                },
                {
                    name: 'Iron',
                    value: Math.round(recipe.nutrition?.iron_mg || 0),
                    unit: 'mg',
                    target: 18,
                    benefit: 'prevents fatigue and supports cognitive function',
                    moodImportance: 'Prevents mood-related fatigue and brain fog'
                },
                {
                    name: 'Folate (B9)',
                    value: Math.round(recipe.nutrition?.folate_mcg || 0),
                    unit: 'mcg',
                    target: 400,
                    benefit: 'essential for neurotransmitter synthesis and mood stability',
                    moodImportance: 'Critical for serotonin and dopamine production'
                },
                {
                    name: 'Vitamin B12',
                    value: Math.round(recipe.nutrition?.vitamin_b12_mcg || 0),
                    unit: 'mcg',
                    target: 2.4,
                    benefit: 'supports brain function and prevents depression',
                    moodImportance: 'Essential for nerve function and mood regulation'
                },
                {
                    name: 'Zinc',
                    value: Math.round(recipe.nutrition?.zinc_mg || 0),
                    unit: 'mg',
                    target: 11,
                    benefit: 'regulates stress response and immune function',
                    moodImportance: 'Supports stress resilience and immune health'
                },
                {
                    name: 'Vitamin D',
                    value: Math.round(recipe.nutrition?.vitamin_d_iu || 0),
                    unit: 'IU',
                    target: 2000,
                    benefit: 'crucial for mood regulation and seasonal depression',
                    moodImportance: 'Prevents seasonal mood disorders and supports well-being'
                },
                {
                    name: 'Plant Protein',
                    value: Math.round(recipe.nutrition?.protein_g || 0),
                    unit: 'g',
                    target: 50,
                    benefit: 'provides amino acids for neurotransmitter synthesis and sustained energy',
                    moodImportance: 'Essential for mood-regulating neurotransmitters like serotonin and dopamine'
                }
            ];
            
            // Filter to only show nutrients with non-zero values
            const nonZeroNutrients = nutrients.filter(nutrient => nutrient.value > 0);
            
            // If we have micronutrient data, show it with targets
            if (nonZeroNutrients.length > 1) {
                return nonZeroNutrients.map(nutrient => {
                    const percentage = Math.round((nutrient.value / nutrient.target) * 100);
                    const statusIcon = percentage >= 50 ? '✅' : percentage >= 25 ? '🟡' : '🔴';
                    
                    return `<li><strong>${nutrient.name}:</strong> ${nutrient.value} ${nutrient.unit} of ${nutrient.target} ${nutrient.unit} target (${percentage}%) ${statusIcon}<br>
                            <em>${nutrient.moodImportance}</em></li>`;
                }).join('');
            }
            
            // Fallback: Show macronutrients with targets and ingredient-based analysis
            const highlights = [];
            
            // Always include macronutrient benefits with targets
            const calories = Math.round(recipe.nutrition?.calories || 0);
            const protein = Math.round(recipe.nutrition?.protein_g || 0);
            const fiber = Math.round(recipe.nutrition?.fiber_g || 0);
            
            if (calories > 0) {
                const calorieTarget = 2000; // Daily calorie target
                const caloriePercent = Math.round((calories / calorieTarget) * 100);
                highlights.push(`<li><strong>Energy:</strong> ${calories} calories (${caloriePercent}% of daily target) provide sustained energy for mood stability and focus.</li>`);
            }
            
            // Note: Plant Protein is now handled in the main nutrient highlights above
            
            // Fiber is already shown in the main nutrition table above, so we skip it here to avoid duplication
            // if (fiber > 0) {
            //     const fiberTarget = 25; // Daily fiber target
            //     const fiberPercent = Math.round((fiber / fiberTarget) * 100);
            //     highlights.push(`<li><strong>Fiber:</strong> ${fiber}g (${fiberPercent}% of daily target) stabilizes blood sugar and prevents energy crashes that can affect mood.</li>`);
            // }
            
            // Add ingredient-based nutrient benefits with estimated targets
            const ingredients = recipe.ingredients || [];
            const ingredientText = ingredients.map(ing => ing.name.toLowerCase()).join(' ');
            
            if (ingredientText.includes('leafy') || ingredientText.includes('spinach') || ingredientText.includes('kale')) {
                const folatePercent = folate > 0 ? Math.round((folate / 400) * 100) : 0;
                const ironPercent = iron > 0 ? Math.round((iron / 18) * 100) : 0;
                const magPercent = magnesium > 0 ? Math.round((magnesium / 120) * 100) : 0;
                highlights.push(`<li><strong>Leafy Greens:</strong> Rich in folate (${folate}mcg, ${folatePercent}% of 400mcg target), iron (${iron}mg, ${ironPercent}% of 18mg target), and magnesium (${magnesium}mg, ${magPercent}% of 120mg target) for mood support and stress reduction.</li>`);
            }
            
            if (ingredientText.includes('fish') || ingredientText.includes('salmon') || ingredientText.includes('tuna') || ingredientText.includes('mackerel')) {
                const omega3Percent = omega3 > 0 ? Math.round((omega3 / 2.0) * 100) : 0;
                highlights.push(`<li><strong>Omega-3 Fatty Acids:</strong> Provides ${omega3}g (${omega3Percent}% of 2g daily target) with anti-inflammatory properties that support brain health and mood regulation.</li>`);
            }
            
            if (ingredientText.includes('nuts') || ingredientText.includes('almond') || ingredientText.includes('walnut')) {
                const fatGrams = Math.round(recipe.nutrition?.fat_g || 0);
                const fatPercent = fatGrams > 0 ? Math.round((fatGrams / 50) * 100) : 0; // Assuming 50g daily fat target
                highlights.push(`<li><strong>Healthy Fats:</strong> Provides ${fatGrams}g (${fatPercent}% of daily target) to support brain function and maintain stable mood throughout the day.</li>`);
            }
            
            if (ingredientText.includes('legume') || ingredientText.includes('bean') || ingredientText.includes('lentil') || ingredientText.includes('chickpea')) {
                const proteinPercent = protein > 0 ? Math.round((protein / 50) * 100) : 0;
                highlights.push(`<li><strong>Plant Protein:</strong> Provides ${protein}g (${proteinPercent}% of 50g daily target) with amino acids for neurotransmitter synthesis and sustained energy.</li>`);
            }
            
            if (ingredientText.includes('whole grain') || ingredientText.includes('quinoa') || ingredientText.includes('brown rice') || ingredientText.includes('oats')) {
                const carbsGrams = Math.round(recipe.nutrition?.carbs_g || 0);
                const carbsPercent = carbsGrams > 0 ? Math.round((carbsGrams / 250) * 100) : 0; // Assuming 250g daily carbs target
                highlights.push(`<li><strong>Complex Carbohydrates:</strong> Provides ${carbsGrams}g (${carbsPercent}% of daily target) for steady glucose release that supports stable mood and energy levels.</li>`);
            }
            
            // Add mood-specific nutrient values and targets
            const selectedMoods = JSON.parse(sessionStorage.getItem('selectedMoods') || '[]');
            if (selectedMoods.includes('stressed')) {
                const magPercent = magnesium > 0 ? Math.round((magnesium / 120) * 100) : 0;
                const omega3Percent = omega3 > 0 ? Math.round((omega3 / 2.0) * 100) : 0;
                highlights.push(`<li><strong>Stress Support:</strong> This recipe provides ${magnesium}mg magnesium (${magPercent}% of 120mg target) and ${omega3}g omega-3 (${omega3Percent}% of 2g target) to help manage stress response.</li>`);
            }
            if (selectedMoods.includes('fatigued')) {
                const ironPercent = iron > 0 ? Math.round((iron / 18) * 100) : 0;
                const b12Percent = b12 > 0 ? Math.round((b12 / 2.4) * 100) : 0;
                const folatePercent = folate > 0 ? Math.round((folate / 400) * 100) : 0;
                highlights.push(`<li><strong>Energy Support:</strong> This recipe provides ${iron}mg iron (${ironPercent}% of 18mg target), ${b12}mcg B12 (${b12Percent}% of 2.4mcg target), and ${folate}mcg folate (${folatePercent}% of 400mcg target) to combat fatigue and boost energy.</li>`);
            }
            if (selectedMoods.includes('low_mood')) {
                const omega3Percent = omega3 > 0 ? Math.round((omega3 / 2.0) * 100) : 0;
                const folatePercent = folate > 0 ? Math.round((folate / 400) * 100) : 0;
                const vitDPercent = vitaminD > 0 ? Math.round((vitaminD / 2000) * 100) : 0;
                highlights.push(`<li><strong>Mood Support:</strong> This recipe provides ${omega3}g omega-3 (${omega3Percent}% of 2g target), ${folate}mcg folate (${folatePercent}% of 400mcg target), and ${vitaminD}IU vitamin D (${vitDPercent}% of 2000IU target) to support mood regulation.</li>`);
            }
            if (selectedMoods.includes('irritable')) {
                const magPercent = magnesium > 0 ? Math.round((magnesium / 120) * 100) : 0;
                const zincPercent = zinc > 0 ? Math.round((zinc / 11) * 100) : 0;
                highlights.push(`<li><strong>Mood Stability:</strong> This recipe provides ${magnesium}mg magnesium (${magPercent}% of 120mg target) and ${zinc}mg zinc (${zincPercent}% of 11mg target) to help regulate mood and reduce irritability.</li>`);
            }
            
            return highlights.join('');
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
    
    const targetCalories = Math.round(nutrition?.target_calories || 2000);
    const targetProtein = Math.round(nutrition?.target_protein || 50);
    const targetFiber = Math.round(nutrition?.target_fiber || 25);
    
    const caloriePercent = Math.round((calories / targetCalories) * 100);
    const proteinPercent = Math.round((protein / targetProtein) * 100);
    const fiberPercent = Math.round((fiber / targetFiber) * 100);
    
    let rationaleText = `This ${recipe.name} was carefully selected to provide optimal nutrition for your current mood needs. `;
    
    // Calorie information with target
    rationaleText += `With ${calories} calories (${caloriePercent}% of your daily target of ${targetCalories} calories), `;
    
    // Protein information with target
    rationaleText += `it delivers ${protein}g of protein (${proteinPercent}% of daily target of ${targetProtein}g) for sustained energy and muscle support. `;
    
    // Fiber information with target
    rationaleText += `The ${fiber}g of fiber (${fiberPercent}% of daily target of ${targetFiber}g) helps maintain stable blood sugar levels and supports digestive health. `;
    
    // Key mood-supporting nutrients with targets
    if (magnesium > 0) {
        const magPercent = Math.round((magnesium / 120) * 100);
        rationaleText += `Rich in magnesium (${magnesium}mg, ${magPercent}% of daily target of 120mg), this recipe supports nervous system function and stress response. `;
    }
    
    if (omega3 > 0) {
        const omegaPercent = Math.round((omega3 / 2.0) * 100);
        rationaleText += `The ${omega3}g of omega-3 fatty acids (${omegaPercent}% of daily target of 2g) provide anti-inflammatory benefits and support mood regulation. `;
    }
    
    if (iron > 0) {
        const ironPercent = Math.round((iron / 18) * 100);
        rationaleText += `With ${iron}mg of iron (${ironPercent}% of daily target of 18mg), it helps maintain energy levels and cognitive function. `;
    }
    
    if (folate > 0) {
        const folatePercent = Math.round((folate / 400) * 100);
        rationaleText += `The ${folate}mcg of folate (B9) (${folatePercent}% of daily target of 400mcg) is essential for neurotransmitter synthesis and mood stability. `;
    }
    
    if (b12 > 0) {
        const b12Percent = Math.round((b12 / 2.4) * 100);
        rationaleText += `Vitamin B12 (${b12}mcg, ${b12Percent}% of daily target of 2.4mcg) supports brain function and helps prevent depression. `;
    }
    
    if (zinc > 0) {
        const zincPercent = Math.round((zinc / 11) * 100);
        rationaleText += `Zinc (${zinc}mg, ${zincPercent}% of daily target of 11mg) regulates stress response and supports immune function. `;
    }
    
    if (vitaminD > 0) {
        const vitDPercent = Math.round((vitaminD / 2000) * 100);
        rationaleText += `Vitamin D (${vitaminD}IU, ${vitDPercent}% of daily target of 2000IU) is crucial for mood regulation and helps combat seasonal depression. `;
    }
    
    // Mood-specific benefits with actual recipe values and targets
    const selectedMoods = JSON.parse(sessionStorage.getItem('selectedMoods') || '[]');
    if (selectedMoods.includes('stressed')) {
        const magPercent = magnesium > 0 ? Math.round((magnesium / 120) * 100) : 0;
        const omega3Percent = omega3 > 0 ? Math.round((omega3 / 2.0) * 100) : 0;
        rationaleText += `For stress management, this recipe provides ${magnesium}mg magnesium (${magPercent}% of 120mg daily target) and ${omega3}g omega-3 (${omega3Percent}% of 2g daily target) to help regulate your stress response. `;
    }
    if (selectedMoods.includes('fatigued')) {
        const ironPercent = iron > 0 ? Math.round((iron / 18) * 100) : 0;
        const b12Percent = b12 > 0 ? Math.round((b12 / 2.4) * 100) : 0;
        const folatePercent = folate > 0 ? Math.round((folate / 400) * 100) : 0;
        rationaleText += `To combat fatigue, this recipe provides ${iron}mg iron (${ironPercent}% of 18mg daily target), ${b12}mcg B12 (${b12Percent}% of 2.4mcg daily target), and ${folate}mcg folate (${folatePercent}% of 400mcg daily target) to boost energy and cognitive function. `;
    }
    if (selectedMoods.includes('low_mood')) {
        const omega3Percent = omega3 > 0 ? Math.round((omega3 / 2.0) * 100) : 0;
        const folatePercent = folate > 0 ? Math.round((folate / 400) * 100) : 0;
        const vitDPercent = vitaminD > 0 ? Math.round((vitaminD / 2000) * 100) : 0;
        rationaleText += `For mood support, this recipe provides ${omega3}g omega-3 (${omega3Percent}% of 2g daily target), ${folate}mcg folate (${folatePercent}% of 400mcg daily target), and ${vitaminD}IU vitamin D (${vitDPercent}% of 2000IU daily target) to support mood regulation. `;
    }
    if (selectedMoods.includes('irritable')) {
        const magPercent = magnesium > 0 ? Math.round((magnesium / 120) * 100) : 0;
        const zincPercent = zinc > 0 ? Math.round((zinc / 11) * 100) : 0;
        rationaleText += `To reduce irritability, this recipe provides ${magnesium}mg magnesium (${magPercent}% of 120mg daily target) and ${zinc}mg zinc (${zincPercent}% of 11mg daily target) to help stabilize mood. `;
    }
    
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