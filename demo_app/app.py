"""
SavorMe Functional Demo App
Beautiful web interface that connects to the backend API
"""
from flask import Flask, render_template, jsonify, request
import httpx
import os
from pathlib import Path

app = Flask(__name__)

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')


@app.route('/profile')
def profile():
    """User profile input page"""
    return render_template('profile.html')


@app.route('/mood-selection')
def mood_selection():
    """Mood selection page"""
    return render_template('mood_selection.html')


@app.route('/recipe-result')
def recipe_result():
    """Recipe recommendation result page"""
    return render_template('recipe_result.html')


@app.route('/api/recommend', methods=['POST'])
async def get_recommendation():
    """Proxy endpoint to backend API"""
    try:
        data = request.json
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{BACKEND_URL}/api/v1/recipes/recommend",
                json=data
            )
            response.raise_for_status()
            return jsonify(response.json())
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
async def health_check():
    """Check backend health"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BACKEND_URL}/api/v1/health")
            return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e), "backend_url": BACKEND_URL}), 503


if __name__ == '__main__':
    print("🍽️  SavorMe Demo App")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Demo URL: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)

