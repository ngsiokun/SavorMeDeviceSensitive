#!/usr/bin/env python3
"""
SavorMe Startup Script with Automatic Setup
This script will automatically check and setup the environment before starting the application
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """
    Main startup function with automatic setup
    """
    print("=" * 50)
    print("🚀 SavorMe Application Startup with Auto-Setup")
    print("=" * 50)
    print()
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Error: Please run this script from the SavorMe-backend directory")
        print("💡 Expected structure: SavorMe-backend/app/main.py")
        return 1
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found. Running setup...")
        if run_setup_script():
            print("✅ Setup completed! Please restart the application.")
            return 0
        else:
            print("❌ Setup failed. Please check the errors above.")
            return 1
    
    # Check if virtual environment is activated
    if not is_venv_activated():
        print("⚠️  Virtual environment not detected.")
        print("💡 Please activate your virtual environment first:")
        print("   Windows: venv\\Scripts\\activate.bat")
        print("   Linux/Mac: source venv/bin/activate")
        return 1
    
    # Check if required packages are installed
    if not check_required_packages():
        print("⚠️  Missing required packages. Installing...")
        if install_requirements():
            print("✅ Dependencies installed successfully!")
        else:
            print("❌ Failed to install dependencies.")
            return 1
    
    # Start the application
    print("🎉 Environment verified! Starting SavorMe application...")
    print()
    start_application()
    return 0


def is_venv_activated():
    """Check if virtual environment is activated"""
    return (hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))


def check_required_packages():
    """Check if required packages are installed"""
    required_packages = ['fastapi', 'uvicorn', 'requests', 'pydantic']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed")
    return True


def install_requirements():
    """Install requirements from requirements.txt"""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            print(f"❌ pip install failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing requirements: {e}")
        return False


def run_setup_script():
    """Run the automated setup script"""
    setup_script = Path("setup_new_clone.bat")
    if not setup_script.exists():
        print("⚠️  setup_new_clone.bat not found. Running manual setup...")
        return run_manual_setup()
    
    try:
        print("🚀 Running automated setup script...")
        result = subprocess.run([str(setup_script)], 
                              capture_output=True, 
                              text=True, 
                              shell=True,
                              encoding='utf-8',
                              errors='ignore')
        
        if result.returncode == 0:
            print("✅ Setup script completed successfully!")
            return True
        else:
            print(f"❌ Setup script failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running setup script: {e}")
        return False


def run_manual_setup():
    """Run manual setup process"""
    print("🔧 Running manual setup...")
    
    # Create virtual environment
    print("1. Creating virtual environment...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "venv", "venv"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Failed to create virtual environment: {result.stderr}")
            return False
        
        print("✅ Virtual environment created")
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False
    
    # Install requirements
    print("2. Installing dependencies...")
    if not install_requirements():
        return False
    
    # Create .env template
    print("3. Creating .env template...")
    env_template = """# SavorMe Backend Environment Variables
# Copy this file and add your actual API keys

# Edamam Recipe API
EDAMAM_APP_ID=your_edamam_app_id
EDAMAM_APP_KEY=your_edamam_app_key

# OpenRouter AI API
OPENROUTER_API_KEY=your_openrouter_api_key

# Canva API (optional)
CANVA_CLIENT_ID=your_canva_client_id
CANVA_CLIENT_SECRET=your_canva_client_secret

# CORS Origins
CORS_ORIGINS=http://localhost:5000,http://127.0.0.1:5000
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_template)
        print("✅ .env template created")
        print("💡 Please edit .env file with your actual API keys")
    except Exception as e:
        print(f"❌ Error creating .env template: {e}")
        return False
    
    print("✅ Manual setup completed!")
    return True


def start_application():
    """Start the SavorMe application"""
    try:
        # Import and run the FastAPI app
        from app.main import app
        import uvicorn
        
        print("🌐 Starting SavorMe Backend API...")
        print("📍 Backend URL: http://127.0.0.1:8000")
        print("📚 API Docs: http://127.0.0.1:8000/docs")
        print("💡 Press Ctrl+C to stop the server")
        print()
        
        uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the correct directory and virtual environment is activated")
    except Exception as e:
        print(f"❌ Error starting application: {e}")


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
