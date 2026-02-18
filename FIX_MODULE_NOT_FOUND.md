# 🔧 Fix: Module NotFoundError

## Error Message
```
ModuleNotFoundError: No module named 'sqlalchemy'
```

## ✅ Quick Fix

The issue is that dependencies are not installed. SQLAlchemy **IS** in requirements.txt, but you need to install it.

### Solution (Choose One):

---

### Option 1: Automated Installation (Easiest)

**Windows:**
```bash
cd backend
install_dependencies.bat
```

**Linux/Mac:**
```bash
cd backend
chmod +x install_dependencies.sh
./install_dependencies.sh
```

---

### Option 2: Manual Installation

**Step 1: Navigate to backend directory**
```bash
cd backend
```

**Step 2: Create virtual environment**
```bash
python -m venv venv
```

**Step 3: Activate virtual environment**

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

**Step 4: Upgrade pip**
```bash
pip install --upgrade pip
```

**Step 5: Install all dependencies**
```bash
pip install -r requirements.txt
```

This will install all 30+ packages including:
- sqlalchemy
- fastapi
- uvicorn
- scikit-learn
- tensorflow
- prophet
- and all other dependencies

**Step 6: Verify installation**
```bash
python test_dependencies.py
```

---

### Option 3: Install Just SQLAlchemy (Not Recommended)

If you only want to install SQLAlchemy:
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install sqlalchemy==2.0.25
```

**But you'll need ALL dependencies eventually, so use Option 1 or 2 instead!**

---

## ⚠️ Common Mistakes

### ❌ Not Activating Virtual Environment
You MUST activate the virtual environment first:
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

Look for `(venv)` in your terminal prompt.

### ❌ Wrong Directory
Make sure you're in the `backend/` directory:
```bash
cd backend
pip install -r requirements.txt
```

### ❌ Using System Python
Don't install to system Python. Always use virtual environment:
```bash
# ❌ Wrong
pip install -r requirements.txt

# ✅ Correct
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📦 What Gets Installed

When you run `pip install -r requirements.txt`, it installs:

### Web Framework (5 packages)
- fastapi, uvicorn, pydantic, pydantic-settings, python-multipart

### Authentication (3 packages)
- python-jose, passlib, email-validator

### Database (4 packages)
- **sqlalchemy** ← This fixes your error!
- alembic, psycopg2-binary, asyncpg

### ML Libraries (10 packages)
- scikit-learn, numpy, pandas, scipy, prophet, statsmodels, tensorflow, joblib, matplotlib, seaborn

### Monitoring (5 packages)
- prometheus-client, requests, aiohttp, redis, celery

### Utilities (1 package)
- python-dotenv

**Total: 30+ packages**

---

## ✅ Verify Installation

After installing, verify everything works:

```bash
cd backend
python test_dependencies.py
```

You should see:
```
✅ SQLAlchemy                - OK
✅ FastAPI                   - OK
✅ Scikit-learn             - OK
... (all packages)

📊 Results: 24 passed, 0 failed
✅ All dependencies are installed correctly!
```

---

## 🚀 After Installation

Once dependencies are installed:

1. **Start the backend:**
   ```bash
   python start_backend.py
   ```

2. **Create users (in new terminal):**
   ```bash
   cd backend
   python create_dummy_users.py
   ```

3. **Access the API:**
   - http://localhost:8000/api/docs

---

## 🆘 Still Having Issues?

### Check Python Version
```bash
python --version
```
Should be Python 3.8 or higher.

### Check Pip Version
```bash
pip --version
```

### Try Python3/Pip3
If `python` doesn't work, try:
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Install Build Tools (If Needed)

Some packages need build tools:

**Windows:**
- Install Visual C++ Build Tools from Microsoft

**Linux:**
```bash
sudo apt-get install python3-dev build-essential
```

**Mac:**
```bash
xcode-select --install
```

---

## 💡 Pro Tip

Use the automated installation script to avoid all these issues:

**Windows:**
```bash
cd backend
install_dependencies.bat
```

This handles everything automatically! 🎉
