@echo off
echo ========================================
echo SavorMe GitHub Setup
echo ========================================
echo.

echo [INFO] This will push all your fixed code to GitHub
echo [INFO] The .env file will NOT be uploaded (for security)
echo.

echo [INFO] Initializing git repository...
git init

echo [INFO] Adding all files (except .env)...
git add .

echo [INFO] Creating initial commit...
git commit -m "SavorMe Cloud Run Deployment - All Issues Fixed

✅ FIXED:
- All Dockerfile ports (8080 for Cloud Run)
- All environment variables configured
- All invalid Docker COPY paths resolved
- Dynamic PROJECT_ID URLs in cloudbuild.yaml
- Complete deployment scripts created
- Comprehensive documentation added

🚀 READY FOR DEPLOYMENT:
- Google Cloud project: savorme-474712
- Account: ngsiokun88@gmail.com
- All microservices configured
- Frontend and API Gateway ready

📋 SETUP ON NEW COMPUTER:
1. Install Google Cloud SDK
2. Copy .env file to project root
3. Run: .\deploy-to-cloud-run.bat

🌐 EXPECTED URLS:
- Frontend: https://savorme-frontend-savorme-474712-uc.a.run.app
- API: https://savorme-router-savorme-474712-uc.a.run.app"

echo.
echo [INFO] Please set up your GitHub repository URL:
echo [INFO] Example: git remote add origin https://github.com/yourusername/savorme.git
echo.
echo [INFO] Then run: git push -u origin main
echo.
echo ========================================
echo GitHub Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Create a new repository on GitHub
echo 2. Copy the repository URL
echo 3. Run: git remote add origin [YOUR_REPO_URL]
echo 4. Run: git push -u origin main
echo 5. Clone on new computer and deploy!
echo.
pause
