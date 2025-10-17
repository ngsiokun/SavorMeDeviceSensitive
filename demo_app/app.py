"""
SavorMe Functional Demo App
Beautiful web interface that connects to the backend API

⚠️  IMPORTANT: This app should be started via Command Prompt (cmd.exe), NOT PowerShell!
   Use: start.bat or run manually in Command Prompt for proper environment setup.
"""
from flask import Flask, render_template, jsonify, request, Response, g
import requests
import os
import logging
import time
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for better troubleshooting
logger = logging.getLogger(__name__)

app = Flask(__name__)

# FOR DEVELOPMENT ONLY - Disable static file caching
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Backend API URL - Use cloud backend (already deployed)
BACKEND_URL = os.getenv("BACKEND_URL", "https://savorme-backend-662773309683.asia-southeast1.run.app").strip().rstrip("/")


@app.before_request
def set_app_version():
    """Set cache-busting version for static assets"""
    if not hasattr(g, 'app_version'):
        # Use current timestamp for development cache busting
        g.app_version = int(time.time())


@app.route('/config')
def config():
    """Frontend config endpoint - provides backend URL to JavaScript"""
    return jsonify({"BACKEND_URL": BACKEND_URL})


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
    return render_template('mood_selection.html', backend_url=BACKEND_URL)


@app.route('/recipe-result')
def recipe_result():
    """Recipe recommendation result page"""
    return render_template('recipe_result.html')


@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    """Proxy endpoint to backend API - FIXED to handle FastAPI parameter structure"""
    target_backend_endpoint = f"{BACKEND_URL}/api/v1/recipes/recommend"
    
    try:
        # 1. Parse the incoming JSON data
        request_data = request.get_json()
        logger.debug(f"Flask proxy received data: {request_data}")
        
        # 2. Extract mood_blend and user_profile from the request
        mood_blend = request_data.get('mood_blend')
        user_profile = request_data.get('user_profile')
        
        if not mood_blend or not user_profile:
            return jsonify({"error": "Missing required fields: mood_blend and user_profile"}), 400
        
        # 3. Prepare headers for backend request
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # 4. Create the properly structured payload for FastAPI
        # FastAPI expects the data as a single JSON object with the parameters
        payload = {
            "mood_blend": mood_blend,
            "user_profile": user_profile
        }
        
        logger.debug(f"Flask proxy forwarding POST request to {target_backend_endpoint} with payload: {payload}")
        
        # 5. Send the request to the backend
        backend_response = requests.post(target_backend_endpoint, headers=headers, json=payload, timeout=30.0)
        
        logger.debug(f"Backend responded with status: {backend_response.status_code}")
        logger.debug(f"Backend response headers: {backend_response.headers}")
        logger.debug(f"Backend response content (first 500 chars): {backend_response.text[:500]}...")
        
        # 3. Construct Flask response from backend's response
        # Crucially, return the actual content, status, and content-type header
        response_from_flask = Response(
            backend_response.content,
            status=backend_response.status_code,
            mimetype=backend_response.headers.get('Content-Type', 'application/json')
        )
        
        # 4. Copy other relevant headers from the backend to the frontend response
        for header, value in backend_response.headers.items():
            if header.lower() not in ['content-encoding', 'transfer-encoding', 'content-length']:
                response_from_flask.headers[header] = value
        
        return response_from_flask
    
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Flask proxy: Connection to backend failed: {e}")
        return jsonify({"error": "Backend service is unreachable."}), 503
    except requests.exceptions.RequestException as e:
        logger.error(f"Flask proxy: Error during request to backend: {e}")
        return jsonify({"error": f"Error communicating with backend: {str(e)}"}), 500
    except Exception as e:
        logger.error(f"Flask proxy: An unexpected error occurred: {e}", exc_info=True)
        return jsonify({"error": f"An unexpected server error occurred: {str(e)}"}), 500


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
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") != "production"
    
    print("🍽️  SavorMe Demo App v2.1.0")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Demo URL: http://localhost:{port}")
    print(f"Health Check: http://localhost:{port}/api/health")
    print(f"Version Info: http://localhost:{port}/api/version")
    print("=" * 60)
    logger.info("Starting SavorMe Demo App")
    app.run(debug=debug, host="0.0.0.0", port=port)

