# 🚨 Backend Not Running - Start It Now!

## The Problem

Your frontend is trying to connect to the backend at `http://localhost:8000` but the backend server is not running.

Error: `ERR_CONNECTION_REFUSED` means the backend is not started.

## ✅ Solution: Start the Backend

### Step 1: Open a New Terminal/Command Prompt

Keep your frontend running in the current terminal and open a **NEW** terminal window.

### Step 2: Navigate to Backend Directory

```bash
cd backend
```

### Step 3: Install Dependencies (First Time Only)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Start the Backend

```bash
python start_backend.py
```

You should see:
```
============================================================
🚀 Cloud Monitoring System - Backend Server
============================================================

📦 Initializing database...
✅ Database initialized successfully!

🌐 Starting FastAPI server...
📍 API Documentation: http://localhost:8000/api/docs
📍 Alternative Docs: http://localhost:8000/api/redoc
📍 Health Check: http://localhost:8000/api/health

💡 Tip: Run 'python create_dummy_users.py' to create test users
============================================================

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 5: Create Dummy Users (In Another New Terminal)

Open **ANOTHER** new terminal (keep backend running):

```bash
cd backend
python create_dummy_users.py
```

This creates test users:
- Username: `admin`, Password: `admin123`
- Username: `user`, Password: `user123`
- Username: `demo`, Password: `demo123`

### Step 6: Refresh Your Frontend

Go back to your browser and refresh the page. The login should now work!

## 🎯 Quick Commands Summary

**Terminal 1 (Frontend):**
```bash
cd frontend
npm run dev
```

**Terminal 2 (Backend):**
```bash
cd backend
python start_backend.py
```

**Terminal 3 (Create Users - Run Once):**
```bash
cd backend
python create_dummy_users.py
```

## ✅ Verify Backend is Running

Open your browser and go to:
- http://localhost:8000/api/health

You should see:
```json
{
  "status": "healthy",
  "timestamp": "2024-...",
  "version": "1.0.0",
  "app": "Cloud Monitoring System"
}
```

## 🐛 Troubleshooting

### "python: command not found"
Try `python3` instead of `python`

### "pip: command not found"
Try `pip3` instead of `pip`

### "Port 8000 already in use"
Kill the process using port 8000:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### "Module not found" errors
Make sure you activated the virtual environment and installed dependencies:
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## 📱 After Backend Starts

1. ✅ Backend running at http://localhost:8000
2. ✅ Frontend running at http://localhost:5173
3. ✅ Login with: `admin` / `admin123`
4. ✅ Check API docs: http://localhost:8000/api/docs

## 🎉 Success!

Once the backend is running, your frontend will connect successfully and you can login!
