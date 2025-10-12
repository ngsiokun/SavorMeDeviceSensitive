# 📋 Copy-Paste These Commands in Cloud Shell

## ⚠️ IMPORTANT: Run these commands ONE AT A TIME in Cloud Shell

### Command 1: Set Project
```bash
gcloud config set project savorme-474712
```
**Wait for**: `Updated property [core/project].`

---

### Command 2: Clone Your Repo (REPLACE with your GitHub URL)
```bash
git clone https://github.com/YOUR-USERNAME/SavorMe-backend.git
cd SavorMe-backend
```
**If you don't have it on GitHub yet, skip to the Alternative section below**

---

### Command 3: Fix IAM Permissions (Copy ALL of this)
```bash
PROJECT_ID="savorme-474712"
REGION="asia-southeast1"
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')
CB_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

echo "🔐 Fixing IAM permissions..."

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/run.admin" \
  --quiet

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/iam.serviceAccountUser" \
  --quiet

gcloud artifacts repositories add-iam-policy-binding "cloud-run-source-deploy" \
  --location="$REGION" \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/artifactregistry.writer" \
  --quiet

echo "✅ IAM permissions fixed!"
```
**Wait for**: `✅ IAM permissions fixed!`

---

### Command 4: Build Container (Copy ALL of this)
```bash
PROJECT_ID="savorme-474712"
REGION="asia-southeast1"

echo "🔨 Building container image (this takes 2-3 minutes)..."

gcloud builds submit \
  --region="$REGION" \
  --tag "asia-southeast1-docker.pkg.dev/${PROJECT_ID}/cloud-run-source-deploy/savorme-backend:latest" \
  --timeout=10m
```
**Wait for**: `SUCCESS` (this takes 2-3 minutes, you'll see lots of output)

---

### Command 5: Deploy to Cloud Run (Copy ALL of this)
```bash
echo "🚀 Deploying to Cloud Run..."

gcloud run deploy savorme-backend \
  --image "asia-southeast1-docker.pkg.dev/${PROJECT_ID}/cloud-run-source-deploy/savorme-backend:latest" \
  --region "$REGION" \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars ENVIRONMENT=production \
  --quiet

echo "✅ Deployment complete!"
```
**Wait for**: `✅ Deployment complete!` and you'll see a URL

---

### Command 6: Get Your Service URL
```bash
SERVICE_URL=$(gcloud run services describe savorme-backend \
  --region=asia-southeast1 \
  --project=savorme-474712 \
  --format='value(status.url)')

echo ""
echo "🎉 SUCCESS! YOUR SERVICE IS LIVE!"
echo "=================================="
echo "📍 Service URL: $SERVICE_URL"
echo "📚 API Docs: $SERVICE_URL/docs"
echo "=================================="
```

---

### Command 7: Test It
```bash
curl "$SERVICE_URL/api/v1/health"
```
**Expected**: Should return JSON with `"status": "healthy"`

---

## 🆘 ALTERNATIVE: If Code is NOT on GitHub Yet

### Option A: Upload Files Directly to Cloud Shell

1. In Cloud Shell, click the **three dots** (⋮) at the top-right
2. Click **"Upload"**
3. Select your entire SavorMe-backend folder
4. Wait for upload to complete
5. Then run: `cd SavorMe-backend`
6. Continue with Command 3 above

### Option B: Push to GitHub First (From Your Local Machine)

**Open a NEW Command Prompt on your local machine** (not Cloud Shell):

```cmd
cd C:\Users\HP\SavorMe\SavorMe-backend

REM Initialize git (if not already done)
git init

REM Add all files
git add .

REM Commit
git commit -m "Deploy to Cloud Run"

REM Create a repo on GitHub, then add it:
git remote add origin https://github.com/YOUR-USERNAME/SavorMe-backend.git

REM Push
git push -u origin main
```

Then go back to Cloud Shell and use Command 2 to clone it.

---

## ✅ Success Indicators

After Command 6, you should see something like:
```
🎉 SUCCESS! YOUR SERVICE IS LIVE!
==================================
📍 Service URL: https://savorme-backend-xyz123-uc.a.run.app
📚 API Docs: https://savorme-backend-xyz123-uc.a.run.app/docs
==================================
```

Copy that URL and open it in your browser! 🚀

---

## 🆘 If Something Goes Wrong

**Build fails?**
- Check the error message in red
- Common issue: Missing files (make sure you're in the SavorMe-backend directory)

**Deploy fails?**
- Re-run Command 3 (IAM permissions)
- Check Cloud Run logs: https://console.cloud.google.com/run?project=savorme-474712

**Still stuck?**
- Copy the error message
- Tell me what command failed
- I'll help you fix it!

---

## 📸 What Each Step Should Look Like

**After Command 1**: 
```
Updated property [core/project].
```

**After Command 3**: 
```
✅ IAM permissions fixed!
```

**After Command 4**: 
```
ID: abc-123-def
CREATE_TIME: ...
STATUS: SUCCESS
```

**After Command 5**: 
```
Service [savorme-backend] revision [savorme-backend-00001-xyz] has been deployed
✅ Deployment complete!
```

**After Command 6**: 
```
🎉 SUCCESS! YOUR SERVICE IS LIVE!
📍 Service URL: https://...
```

---

## 🎯 Total Time: 3-5 Minutes

- Command 1: 5 seconds
- Command 2: 10 seconds
- Command 3: 15 seconds
- Command 4: 2-3 minutes ⏳
- Command 5: 30 seconds
- Command 6: 5 seconds
- Command 7: 5 seconds

**Most of the time is just waiting for the build!**

