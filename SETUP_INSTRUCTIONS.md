# 🚀 SavorMe Setup Instructions for New Computer

## 📋 **Step-by-Step Setup**

### **Step 1: Install Google Cloud SDK**
1. Download from: https://cloud.google.com/sdk/docs/install
2. Run the installer
3. Open Command Prompt and run:
   ```cmd
   gcloud init
   ```
4. Login with: `ngsiokun88@gmail.com`
5. Select project: `savorme-474712`

### **Step 2: Copy Environment File**
1. Copy your `.env` file to the project root directory
2. Make sure it contains:
   ```
   EDAMAM_APP_ID=your_edamam_app_id
   EDAMAM_APP_KEY=your_edamam_app_key
   OPENROUTER_API_KEY=your_openrouter_key
   ```

### **Step 3: Validate Setup**
```cmd
.\check-setup.bat
```
This will verify everything is ready.

### **Step 4: Deploy to Cloud Run**
```cmd
.\deploy-to-cloud-run.bat
```

## ⚡ **Quick Commands**
```cmd
# Check what's installed
.\check-setup.bat

# Deploy everything
.\deploy-to-cloud-run.bat

# Deploy frontend only (faster)
.\deploy-frontend-only.bat
```

## 🌐 **Expected Results**
After successful deployment, you'll have:
- **Frontend**: `https://savorme-frontend-savorme-474712-uc.a.run.app`
- **API Gateway**: `https://savorme-router-savorme-474712-uc.a.run.app`
- **All microservices** running on Google Cloud Run

## 🔧 **Troubleshooting**
- If `check-setup.bat` shows missing requirements, install them first
- If deployment fails, check the logs in the terminal
- All services use port 8080 (Cloud Run standard)
- Environment variables are automatically configured

## 📞 **Need Help?**
- Check `CLOUD_RUN_DEPLOYMENT.md` for detailed guide
- Run `.\check-setup.bat` to diagnose issues
- All documentation is included in the project

---

**Total setup time: ~10-15 minutes**  
**Everything is pre-configured and ready to deploy!** 🚀
