"""
SavorMe Frontend Router v4.0.0
==================================
This router detects device type and forwards to the appropriate frontend:
- Desktop requests → desktop_app/ (port 5001)
- Mobile requests → demo_app/ (port 5000)

This keeps frontend and backend completely SEPARATE for easier debugging.

Architecture:
- app_router.py (this file) - Routes traffic based on device detection
- desktop_app/ - Desktop frontend (completely separate)
- demo_app/ - Mobile frontend (completely separate)  
- app/ - Backend (completely separate)

Cross-references:
- MASTER_FILE_ORGANIZATION.md - File organization
- AUTOMATED_APP_STARTUP_GUIDE.md - Startup guide
"""

from flask import Flask, request, redirect, jsonify
import os

app = Flask(__name__)

# Frontend URLs (use environment variables for Cloud Run)
DESKTOP_URL = os.getenv("DESKTOP_URL", "http://localhost:5001")
MOBILE_URL = os.getenv("MOBILE_URL", "http://localhost:5000")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

print("=" * 70)
print("SavorMe Frontend Router v4.0.0")
print("Automatic Device Detection & Routing")
print("=" * 70)
print(f"Desktop Frontend: {DESKTOP_URL}")
print(f"Mobile Frontend:  {MOBILE_URL}")
print(f"Backend API:      {BACKEND_URL}")
print("=" * 70)
print("This router keeps frontends SEPARATE for easier debugging!")
print("=" * 70)

def is_mobile_device(user_agent):
    """Detect if request is from mobile device"""
    mobile_keywords = [
        'mobile', 'android', 'iphone', 'ipad', 'ipod',
        'blackberry', 'windows phone', 'webos', 'opera mini',
        'tablet'
    ]
    user_agent_lower = user_agent.lower()
    is_mobile = any(keyword in user_agent_lower for keyword in mobile_keywords)
    
    # Log detection for debugging
    device_type = "MOBILE" if is_mobile else "DESKTOP"
    print(f"[{device_type}] User-Agent: {user_agent[:50]}...")
    
    return is_mobile

def get_target_url():
    """Determine which frontend to route to based on device"""
    user_agent = request.headers.get('User-Agent', '')
    
    if is_mobile_device(user_agent):
        return MOBILE_URL
    else:
        return DESKTOP_URL

@app.route('/')
@app.route('/<path:path>')
def route_request(path=''):
    """
    Route all requests to appropriate frontend based on device type
    This keeps desktop and mobile frontends completely separate
    """
    target_url = get_target_url()
    
    # Build full target URL with path and query string
    if path:
        full_url = f"{target_url}/{path}"
    else:
        full_url = target_url
    
    # Preserve query parameters
    if request.query_string:
        full_url += f"?{request.query_string.decode()}"
    
    device_type = "MOBILE" if target_url == MOBILE_URL else "DESKTOP"
    print(f"[ROUTER] → {device_type}: {full_url}")
    
    return redirect(full_url, code=302)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "version": "4.0.0",
        "mode": "router",
        "desktop_url": DESKTOP_URL,
        "mobile_url": MOBILE_URL,
        "backend_url": BACKEND_URL
    })

@app.route('/api/device-info')
def device_info():
    """Return detected device information (for debugging)"""
    user_agent = request.headers.get('User-Agent', '')
    is_mobile = is_mobile_device(user_agent)
    target = MOBILE_URL if is_mobile else DESKTOP_URL
    
    return jsonify({
        "device_type": "mobile" if is_mobile else "desktop",
        "user_agent": user_agent,
        "will_route_to": target
    })

if __name__ == '__main__':
    print("\n⚠️  IMPORTANT: This router requires both frontends to be running:")
    print(f"   Desktop: {DESKTOP_URL}")
    print(f"   Mobile:  {MOBILE_URL}")
    print("\n   Use START-ALL-SEPARATE.bat to start everything correctly!\n")
    
    # Router runs on port from environment (Cloud Run) or 8080 (local)
    port = int(os.getenv('PORT', 8080))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('ENV') != 'production'
    )

