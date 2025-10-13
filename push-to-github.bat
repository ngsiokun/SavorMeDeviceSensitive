@echo off
echo ========================================
echo Pushing SavorMe to GitHub
echo ========================================
echo.

echo [INFO] Adding all files to git...
git add .

echo [INFO] Committing changes...
git commit -m "Fix Cloud Run deployment - All path issues resolved

- Fixed all Dockerfile ports (8080 for Cloud Run)
- Added PORT environment variables to all services
- Fixed invalid Docker COPY paths
- Updated cloudbuild.yaml with dynamic PROJECT_ID URLs
- Created deployment scripts and documentation
- Ready for production deployment"

echo [INFO] Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo GitHub Push Complete!
echo ========================================
echo.
echo Your fixed code is now on GitHub.
echo You can clone it on another computer with:
echo   git clone [YOUR_REPO_URL]
echo.
pause
