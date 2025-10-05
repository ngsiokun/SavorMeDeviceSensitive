# How to Run SavorMe Demo - Step by Step

## ⚠️ IMPORTANT: Use Command Prompt (cmd), NOT PowerShell

## 🎯 Complete Instructions

### **Step 1: Open Command Prompt**
- Press `Win + R`
- Type `cmd`
- Press Enter

### **Step 2: Navigate to Project**
```cmd
cd C:\Users\HP\SavorMe\SavorMe-backend
```

### **Step 3: Activate Virtual Environment**
```cmd
venv\Scripts\activate.bat
```

You should see `(venv)` appear in your prompt.

### **Step 4: Clear Python Cache** (Important!)
```cmd
del /s /q __pycache__
del /s /q *.pyc
```

### **Step 5: Start Backend (Terminal 1)**
```cmd
py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Wait until you see:
```
INFO:     Application startup complete.
```

### **Step 6: Open NEW Command Prompt (Terminal 2)**
- Press `Win + R` → type `cmd` → Enter
- Navigate and activate venv:

```cmd
cd C:\Users\HP\SavorMe\SavorMe-backend\demo_app
..\venv\Scripts\activate.bat
python app.py
```

Wait until you see:
```
* Running on http://127.0.0.1:5000
* Debugger is active!
```

### **Step 7: Open Browser**
Visit: `http://localhost:5000/mood-selection`

---

## 🐛 If Still Getting Errors

### **Clear ALL Python Cache**:
```cmd
cd C:\Users\HP\SavorMe\SavorMe-1
rmdir /s /q app\__pycache__
rmdir /s /q app\services\__pycache__
rmdir /s /q app\models\__pycache__
rmdir /s /q app\api\__pycache__
rmdir /s /q app\core\__pycache__
```

### **Then restart both servers** (Steps 5 & 6 above)

---

## ✅ Success Indicators

### **Backend Running Successfully**:
```
INFO:     Application startup complete.
(No AttributeError about DREAMY)
```

### **Demo App Running Successfully**:
```
🍽️  SavorMe Demo App
* Running on http://127.0.0.1:5000
* Debugger is active!
```

### **Browser Working**:
- See 4 mood cards
- Can click and select moods
- No "can't be reached" error

---

## 📝 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| `(venv)` not showing | Run `venv\Scripts\activate.bat` in cmd |
| "MoodType has no attribute DREAMY" | Clear __pycache__ folders |
| "localhost refused to connect" | Make sure both servers are running |
| "RuntimeError: async views" | This should be fixed, restart Flask app |

---

## 🎯 Expected Result

When everything works, you should be able to:
1. ✅ Select 1-3 moods
2. ✅ Choose intensity
3. ✅ Click "Get My Recipe Recommendation"
4. ✅ See a real recipe from Edamam!

---

**Key**: Use **cmd** not PowerShell, and **clear Python cache** before starting!

