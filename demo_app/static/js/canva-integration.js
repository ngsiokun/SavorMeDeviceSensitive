/**
 * Canva Integration for SavorMe
 * Generates beautiful designs using Canva API
 */

class CanvaIntegration {
    constructor() {
        this.backendUrl = window.location.origin.replace('5000', '8000');
    }

    /**
     * Generate a recipe card design using Canva
     * @param {Object} recipe - Recipe data
     * @returns {Promise<string>} - Design URL
     */
    async generateRecipeCard(recipe) {
        try {
            const response = await fetch(`${this.backendUrl}/api/v1/design/recipe-card`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(recipe)
            });

            const result = await response.json();
            
            if (result.success) {
                return result.design_url;
            } else {
                console.error('Failed to generate recipe card:', result.message);
                return null;
            }
        } catch (error) {
            console.error('Error generating recipe card:', error);
            return null;
        }
    }

    /**
     * Generate a mood card design using Canva
     * @param {Object} moodData - Mood information
     * @returns {Promise<string>} - Design URL
     */
    async generateMoodCard(moodData) {
        try {
            const response = await fetch(`${this.backendUrl}/api/v1/design/mood-card`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(moodData)
            });

            const result = await response.json();
            
            if (result.success) {
                return result.design_url;
            } else {
                console.error('Failed to generate mood card:', result.message);
                return null;
            }
        } catch (error) {
            console.error('Error generating mood card:', error);
            return null;
        }
    }

    /**
     * Generate a nutrition card design using Canva
     * @param {Object} nutritionData - Nutrition information
     * @returns {Promise<string>} - Design URL
     */
    async generateNutritionCard(nutritionData) {
        try {
            const response = await fetch(`${this.backendUrl}/api/v1/design/nutrition-card`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(nutritionData)
            });

            const result = await response.json();
            
            if (result.success) {
                return result.design_url;
            } else {
                console.error('Failed to generate nutrition card:', result.message);
                return null;
            }
        } catch (error) {
            console.error('Error generating nutrition card:', error);
            return null;
        }
    }

    /**
     * Download a design as an image
     * @param {string} designUrl - URL of the design to download
     * @returns {Promise<Blob>} - Image blob
     */
    async downloadDesign(designUrl) {
        try {
            const response = await fetch(`${this.backendUrl}/api/v1/design/download`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ design_url: designUrl })
            });

            const result = await response.json();
            
            if (result.success) {
                // Convert base64 to blob
                const byteCharacters = atob(result.image_data);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }
                const byteArray = new Uint8Array(byteNumbers);
                return new Blob([byteArray], { type: 'image/png' });
            } else {
                console.error('Failed to download design:', result.message);
                return null;
            }
        } catch (error) {
            console.error('Error downloading design:', error);
            return null;
        }
    }

    /**
     * Display a design in a modal
     * @param {string} designUrl - URL of the design to display
     * @param {string} title - Title for the modal
     */
    displayDesignModal(designUrl, title = 'Generated Design') {
        // Create modal
        const modal = document.createElement('div');
        modal.className = 'canva-modal';
        modal.innerHTML = `
            <div class="canva-modal-content">
                <div class="canva-modal-header">
                    <h3>${title}</h3>
                    <button class="canva-modal-close">&times;</button>
                </div>
                <div class="canva-modal-body">
                    <img src="${designUrl}" alt="${title}" style="max-width: 100%; height: auto;">
                </div>
                <div class="canva-modal-footer">
                    <button class="btn btn-primary" onclick="canvaIntegration.downloadDesignAsFile('${designUrl}', '${title}')">
                        Download Design
                    </button>
                    <button class="btn btn-secondary" onclick="canvaIntegration.closeModal()">
                        Close
                    </button>
                </div>
            </div>
        `;

        // Add modal styles
        const style = document.createElement('style');
        style.textContent = `
            .canva-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
            }
            .canva-modal-content {
                background: white;
                border-radius: 16px;
                max-width: 90%;
                max-height: 90%;
                overflow: auto;
            }
            .canva-modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px;
                border-bottom: 1px solid #E5E7EB;
            }
            .canva-modal-header h3 {
                margin: 0;
                color: #065F46;
            }
            .canva-modal-close {
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                color: #6B7280;
            }
            .canva-modal-body {
                padding: 20px;
                text-align: center;
            }
            .canva-modal-footer {
                padding: 20px;
                border-top: 1px solid #E5E7EB;
                display: flex;
                gap: 12px;
                justify-content: flex-end;
            }
            .btn-secondary {
                background: #6B7280;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(modal);

        // Close modal handlers
        modal.querySelector('.canva-modal-close').onclick = () => this.closeModal();
        modal.onclick = (e) => {
            if (e.target === modal) this.closeModal();
        };
    }

    /**
     * Close the design modal
     */
    closeModal() {
        const modal = document.querySelector('.canva-modal');
        if (modal) {
            modal.remove();
        }
    }

    /**
     * Download design as a file
     * @param {string} designUrl - URL of the design to download
     * @param {string} filename - Filename for the download
     */
    async downloadDesignAsFile(designUrl, filename = 'design') {
        try {
            const blob = await this.downloadDesign(designUrl);
            if (blob) {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${filename}.png`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }
        } catch (error) {
            console.error('Error downloading design as file:', error);
        }
    }
}

// Global instance
const canvaIntegration = new CanvaIntegration();
