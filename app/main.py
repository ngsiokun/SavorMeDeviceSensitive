 """
SavorMe Backend - Main FastAPI Application
Mood-Based Recipe Companion Backend

⚠️  IMPORTANT: This backend should be started via Command Prompt (cmd.exe), NOT PowerShell!
   Use: start.bat or run manually in Command Prompt for proper environment setup.
"""
import os
import sys
import subprocess
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .api.routes import router


def check_and_setup_environment():
    """
    Check if the environment is properly set up and run setup if needed
    """
    print("Checking SavorMe environment setup...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("WARNING: .env file not found. Running setup...")
        run_setup_script()
        return
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("WARNING: Virtual environment not detected. Please activate venv first.")
        print("HINT: Run: venv\\Scripts\\activate.bat (Windows) or source venv/bin/activate (Linux/Mac)")
        return
    
    # Check if required packages are installed
    try:
        import fastapi
        import uvicorn
        import requests
        print("Environment setup verified successfully!")
    except ImportError as e:
        print(f"WARNING: Missing required package: {e}")
        print("HINT: Run: pip install -r requirements.txt")
        return


def run_setup_script():
    """
    Run the automated setup script
    """
    print("Running automated setup...")
    
    setup_script = Path("setup_new_clone.bat")
    if setup_script.exists():
        try:
            # Run the setup script
            result = subprocess.run([str(setup_script)], 
                                  capture_output=True, 
                                  text=True, 
                                  shell=True,
                                  encoding='utf-8',
                                  errors='ignore')
            if result.returncode == 0:
                print("Setup completed successfully!")
                print("HINT: Please restart the application after setup.")
            else:
                print(f"ERROR: Setup failed: {result.stderr}")
        except Exception as e:
            print(f"ERROR: Error running setup: {e}")
    else:
        print("WARNING: Setup script not found. Please run setup manually:")
        print("1. Create virtual environment: py -m venv venv")
        print("2. Activate venv: venv\\Scripts\\activate.bat")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Create .env file with your API keys")


# Create FastAPI app
app = FastAPI(
    title="SavorMe Backend API",
    description="Mood-based recipe recommendation backend with emotional intelligence",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.on_event("startup")
async def startup_event():
    """
    Application startup event - environment should be pre-configured
    """
    print("SavorMe Backend API started successfully!")
    print("Backend URL: http://127.0.0.1:8000")
    print("API Docs: http://127.0.0.1:8000/docs")

# Add CORS middleware
cors_origins = settings.CORS_ORIGINS.split(",") if "," in settings.CORS_ORIGINS else [settings.CORS_ORIGINS]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["SavorMe API"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SavorMe Backend API",
        "version": "2.1.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

