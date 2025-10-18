"""
SavorMe Desktop Version - Flask Application
Optimized for desktop screens (1024px+)
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
import httpx
import asyncio
import json
import os
from typing import Dict, Any

app = Flask(__name__)

# Configuration - use environment variable for Cloud Run compatibility
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
DESKTOP_PORT = int(os.getenv("PORT", 5001))

# Helper function to run async functions
def run_async(coro):
    """Run async function in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

@app.route('/')
def desktop_landing():
    """Desktop landing page with enhanced layout"""
    return render_template('desktop-index.html')

@app.route('/profile')
def desktop_profile():
    """Desktop profile page with two-column layout"""
    return render_template('desktop-profile.html')

@app.route('/mood')
def desktop_mood():
    """Desktop mood selection with 2x2 grid layout"""
    return render_template('desktop-mood.html')

@app.route('/results')
def desktop_results():
    """Desktop recipe results with side-by-side layout"""
    return render_template('desktop-results.html')

@app.route('/api/nutrition/calculate', methods=['POST'])
def calculate_nutrition():
    """Calculate nutrition targets for desktop"""
    async def _calculate():
        try:
            data = request.get_json()
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{BACKEND_URL}/api/v1/nutrition/calculate",
                    json=data
                )
                response.raise_for_status()
                return jsonify(response.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return run_async(_calculate())

@app.route('/api/mood/interpret', methods=['POST'])
def interpret_mood():
    """Interpret mood for desktop version"""
    async def _interpret():
        try:
            data = request.get_json()
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{BACKEND_URL}/api/v1/mood/interpret",
                    json=data
                )
                response.raise_for_status()
                return jsonify(response.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return run_async(_interpret())

@app.route('/api/recipes/recommend', methods=['POST'])
def get_recipe_recommendation():
    """Get recipe recommendation for desktop"""
    async def _recommend():
        try:
            data = request.get_json()
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{BACKEND_URL}/api/v1/recipes/recommend",
                    json=data
                )
                response.raise_for_status()
                return jsonify(response.json())
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return run_async(_recommend())

@app.route('/api/health')
def health_check():
    """Health check for desktop version"""
    async def _health():
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{BACKEND_URL}/api/v1/health")
                response.raise_for_status()
                return jsonify(response.json())
        except Exception as e:
            return jsonify({"error": "Backend not available", "details": str(e)}), 503
    return run_async(_health())

if __name__ == '__main__':
    print(f"Desktop: SavorMe Desktop Version starting on port {DESKTOP_PORT}")
    print(f"Desktop URL: http://localhost:{DESKTOP_PORT}")
    print(f"Mobile URL: http://localhost:5000")
    print(f"Backend URL: {BACKEND_URL}")
    app.run(host='0.0.0.0', port=DESKTOP_PORT, debug=True)

