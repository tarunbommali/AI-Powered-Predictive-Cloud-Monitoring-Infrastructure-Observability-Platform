# 🔧 Troubleshooting Guide

## ❌ Error: ERR_CONNECTION_REFUSED

### Problem
Frontend shows: `POST http://localhost:8000/api/auth/login net::ERR_CONNECTION_REFUSED`

### Cause
The backend server is not running.

### Solution

1. **Open a new terminal** (keep frontend running)
2. **Navigate to backend:**
   ```bash
   cd backend
   ```

3. **Install dependencies (first time only):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

4. **Start the backend:**
   ```bash
   python start_backend.py
   ```

5. **Create users (in another terminal):**
   ```bash
   cd backend
   python create_dummy_users.py
   ```

6. **Refresh your browser**

### Verify Backend is Running
Open: http://localhost:8000/api/health

Should see:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "version": "1.0.0"
}
```

---

## ⚠️ React Router Warnings

### Problem
Console shows React Router future flag warnings.

### Solution
✅ **Already Fixed!** The warnings are now resolved in `frontend/src/App.jsx` with:
```javascript
<BrowserRouter
  future={{
    v7_startTransition: true,
    v7_relativeSplatPath: true
  }}
>
```

---

## 🔐 Autocomplete Warnings

### Problem
Console shows: "Input elements should have autocomplete attributes"

### Solution
✅ **Already Fixed!** Login form now has proper autocomplete attributes:
- Username field: `autoComplete="username"`
- Password field: `autoComplete="current-password"`

---

## 🐍 Python/Pip Not Found

### Problem
`python: command not found` or `pip: command not found`

### Solution

**Try python3/pip3:**
```bash
python3 --version
pip3 --version
```

**Install Python:**
- Windows: Download from https://python.org
- Mac: `brew install python3`
- Linux: `sudo apt install python3 python3-pip`

---

## 📦 Module Not Found Errors

### Problem
`ModuleNotFoundError: No module named 'fastapi'` (or other modules)

### Solution

1. **Activate virtual environment:**
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python test_dependencies.py
   ```

---

## 🔌 Port Already in Use

### Problem
`Error: Address already in use` or `Port 8000 is already in use`

### Solution

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**Linux/Mac:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Or use a different port:**
Edit `backend/start_backend.py` and change:
```python
port=8000  # Change to 8001 or any available port
```

---

## 💾 Database Errors

### Problem
Database connection errors or SQLAlchemy errors

### Solution

1. **Delete old database:**
   ```bash
   cd backend
   rm monitoring.db  # Linux/Mac
   del monitoring.db  # Windows
   ```

2. **Restart backend:**
   ```bash
   python start_backend.py
   ```

3. **Recreate users:**
   ```bash
   python create_dummy_users.py
   ```

---

## 🔑 Login Fails with Correct Credentials

### Problem
Login fails even with correct username/password

### Possible Causes & Solutions

1. **Users not created:**
   ```bash
   cd backend
   python create_dummy_users.py
   ```

2. **Backend not running:**
   Check http://localhost:8000/api/health

3. **Wrong credentials:**
   Default credentials:
   - Username: `admin`, Password: `admin123`
   - Username: `user`, Password: `user123`
   - Username: `demo`, Password: `demo123`

4. **Database issue:**
   Delete `monitoring.db` and restart backend

---

## 🌐 CORS Errors

### Problem
`Access to XMLHttpRequest blocked by CORS policy`

### Solution

1. **Check .env file:**
   ```bash
   cd backend
   notepad .env  # Windows
   nano .env  # Linux/Mac
   ```

2. **Verify CORS_ORIGINS includes your frontend URL:**
   ```
   CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"]
   ```

3. **Restart backend** after changing .env

---

## 🤖 ML Model Errors

### Problem
`Model not trained` or ML endpoints return errors

### Cause
ML models need training data before they can make predictions.

### Solution

1. **Add instances to the system**
2. **Wait for metrics to be collected** (or add dummy metrics)
3. **Train models using training endpoints:**
   - POST `/api/ml/anomaly/train/{instance_id}`
   - POST `/api/ml/cpu/train/{instance_id}`
   - POST `/api/ml/memory/train/{instance_id}`

4. **Or use the ML features that don't require training:**
   - Health Score
   - Failure Prediction
   - Root Cause Analysis
   - Auto-Scaling Recommendations

---

## 📊 Prometheus Not Available

### Problem
Metrics endpoints return errors about Prometheus

### Solution

**Option 1: Install Prometheus (Recommended)**
1. Download from https://prometheus.io/download/
2. Configure to scrape your instances
3. Update `PROMETHEUS_URL` in `.env`

**Option 2: Use Without Prometheus (Testing)**
The system will work with dummy data for testing. ML features will still function.

---

## 🎨 Frontend Build Errors

### Problem
`npm run build` fails or frontend won't start

### Solution

1. **Clear node_modules:**
   ```bash
   cd frontend
   rm -rf node_modules  # Linux/Mac
   rmdir /s node_modules  # Windows
   ```

2. **Reinstall dependencies:**
   ```bash
   npm install
   ```

3. **Clear cache:**
   ```bash
   npm cache clean --force
   ```

4. **Restart dev server:**
   ```bash
   npm run dev
   ```

---

## 🔄 Hot Reload Not Working

### Problem
Changes not reflecting in browser

### Solution

1. **Hard refresh browser:**
   - Windows/Linux: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`

2. **Clear browser cache**

3. **Restart dev server:**
   ```bash
   # Frontend
   cd frontend
   npm run dev

   # Backend
   cd backend
   python start_backend.py
   ```

---

## 📝 Common Setup Mistakes

### ❌ Wrong Directory
Make sure you're in the correct directory:
```bash
# For backend commands
cd backend

# For frontend commands
cd frontend
```

### ❌ Virtual Environment Not Activated
You should see `(venv)` in your terminal prompt:
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### ❌ Running Backend from Wrong Location
Always run backend commands from the `backend/` directory:
```bash
cd backend
python start_backend.py  # ✅ Correct
```

Not from root:
```bash
python backend/start_backend.py  # ❌ Wrong
```

---

## 🆘 Still Having Issues?

### Check These:

1. **Backend is running:**
   - http://localhost:8000/api/health should work

2. **Frontend is running:**
   - http://localhost:5173 should show login page

3. **Users are created:**
   - Run `python create_dummy_users.py`

4. **Dependencies installed:**
   - Backend: `pip list` should show all packages
   - Frontend: `npm list` should show all packages

5. **Ports are correct:**
   - Backend: 8000
   - Frontend: 5173 (or 5174)

6. **Check logs:**
   - Backend terminal shows errors
   - Browser console (F12) shows errors

### Get Help:

1. **Check documentation:**
   - `START_BACKEND_NOW.md`
   - `backend/SETUP_GUIDE.md`
   - `backend/BACKEND_READY.md`

2. **Test dependencies:**
   ```bash
   cd backend
   python test_dependencies.py
   ```

3. **Check API docs:**
   - http://localhost:8000/api/docs

---

## ✅ Quick Health Check

Run these commands to verify everything:

```bash
# 1. Check Python
python --version

# 2. Check backend dependencies
cd backend
python test_dependencies.py

# 3. Check backend health
curl http://localhost:8000/api/health

# 4. Check frontend
cd frontend
npm run dev
```

If all pass, your system is working correctly! 🎉
