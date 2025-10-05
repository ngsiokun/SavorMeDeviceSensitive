"""
SavorMe Functional Demo App
Beautiful web interface that connects to the backend API
"""
from flask import Flask, render_template, jsonify, request
import requests
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info(f"Received recommendation request: {data}")
        
        # Use synchronous requests instead of async
        response = requests.post(
            f"{BACKEND_URL}/api/v1/recipes/recommend",
            json=data,
            timeout=30.0
        )
        
        logger.info(f"Backend status code: {response.status_code}")
        logger.info(f"Backend response: {response.text[:500]}")
        
        if response.status_code == 404:
            # Try to get more details about why no recipes were found
            try:
                error_detail = response.json().get("detail", "Unknown error")
                logger.warning(f"404 Error detail: {error_detail}")
            except:
                logger.warning("Could not parse 404 error response")
        
        response.raise_for_status()
        return jsonify(response.json())
    
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error: {e}")
        logger.error(f"Response: {e.response.text if e.response else 'No response'}")
        return jsonify({"error": str(e), "detail": e.response.text if e.response else None}), 500
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection Error: {e}")
        return jsonify({"error": "Backend service unavailable", "detail": str(e)}), 503
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout Error: {e}")
        return jsonify({"error": "Request timeout", "detail": str(e)}), 504
    except Exception as e:
        logger.error(f"General Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Check backend health"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/health", timeout=10.0)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Backend connection failed: {e}")
        return jsonify({
            "status": "unhealthy", 
            "error": "Backend service unavailable", 
            "backend_url": BACKEND_URL
        }), 503
    except requests.exceptions.Timeout as e:
        logger.error(f"Backend health check timeout: {e}")
        return jsonify({
            "status": "unhealthy", 
            "error": "Backend health check timeout", 
            "backend_url": BACKEND_URL
        }), 504
    except Exception as e:
        logger.error(f"Backend health check failed: {e}")
        return jsonify({
            "status": "unhealthy", 
            "error": str(e), 
            "backend_url": BACKEND_URL
        }), 503


@app.route('/api/version')
def version():
    """Get demo app version information"""
    return jsonify({
        "version": "2.1.0",
        "service": "SavorMe Demo App",
        "backend_url": BACKEND_URL,
        "status": "running"
    })


if __name__ == '__main__':
    print("🍽️  SavorMe Demo App v2.1.0")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Demo URL: http://localhost:5000")
    print(f"Health Check: http://localhost:5000/api/health")
    print(f"Version Info: http://localhost:5000/api/version")
    print("=" * 60)
    logger.info("Starting SavorMe Demo App")
    app.run(debug=True, port=5000)

