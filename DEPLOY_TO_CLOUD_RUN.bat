@echo off
echo ============================================================
echo DEPLOY SAVORME TO GOOGLE CLOUD RUN
echo ============================================================
echo.
echo This will deploy ALL 5 microservices to Cloud Run
echo.
echo Services to deploy:
echo   1. Router (API Gateway)
echo   2. User-Nutrition Service
echo   3. Recipe Service
echo   4. Mood-AI Service
echo   5. Frontend
echo.
echo ============================================================
pause
echo.

cd /d C:\Users\Samsung\savorme-cloud-run\SavorMeDeviceSensitive

echo Starting deployment...
echo.

"C:\Users\Samsung\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" builds submit --config cloudbuild.yaml . --substitutions=COMMIT_SHA="MANUAL_DEPLOY"

echo.
echo ============================================================
echo DEPLOYMENT COMPLETE!
echo ============================================================
echo.
echo Your services should now be live at:
echo.
echo Frontend: https://savorme-frontend-662773309683.us-central1.run.app
echo Router: https://savorme-router-662773309683.us-central1.run.app
echo.
pause

