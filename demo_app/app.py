"""
SavorMe Functional Demo App
Beautiful web interface that connects to the backend API
"""
from flask import Flask, render_template, jsonify, request
import requests
import os
from pathlib import Path

app = Flask(__name__)

# Backend API URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')


@app.route('/profile')
def profile():
    """User profile input page"""
    return render_template('profile.html')

@app.route('/profile-enhanced')
def profile_enhanced():
    """Enhanced user profile input page with Canva-inspired design"""
    return render_template('profile_enhanced.html')


@app.route('/mood-selection')
def mood_selection():
    """Mood selection page"""
    return render_template('mood_selection.html')


@app.route('/recipe-result')
def recipe_result():
    """Recipe recommendation result page"""
    return render_template('recipe_result.html')


@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    """Proxy endpoint to backend API"""
    try:
        data = request.json
        print(f"Received request: {data}")
        
        # Use synchronous requests instead of async
        import requests
        response = requests.post(
            f"{BACKEND_URL}/api/v1/recipes/recommend",
            json=data,
            timeout=30.0
        )
        
        print(f"Backend status code: {response.status_code}")
        print(f"Backend response: {response.text[:500]}")
        
        if response.status_code == 404:
            # Try to get more details about why no recipes were found
            try:
                error_detail = response.json().get("detail", "Unknown error")
                print(f"404 Error detail: {error_detail}")
            except:
                print("Could not parse 404 error response")
        
        response.raise_for_status()
        return jsonify(response.json())
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text if e.response else 'No response'}")
        return jsonify({"error": str(e), "detail": e.response.text if e.response else None}), 500
    except Exception as e:
        print(f"General Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Check backend health"""
    try:
        import requests
        response = requests.get(f"{BACKEND_URL}/api/v1/health", timeout=10.0)
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

