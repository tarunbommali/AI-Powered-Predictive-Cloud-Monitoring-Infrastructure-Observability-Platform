@echo off
echo ============================================================
echo   Installing Backend Dependencies
echo ============================================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)
echo.

echo Creating virtual environment...
if not exist "venv\" (
    python -m venv venv
    echo Virtual environment created successfully!
) else (
    echo Virtual environment already exists.
)
echo.

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Installing dependencies from requirements.txt...
echo This may take a few minutes...
echo.
pip install --upgrade pip
pip install -r requirements.txt
echo.

if errorlevel 1 (
    echo.
    echo ============================================================
    echo   ERROR: Installation failed!
    echo ============================================================
    echo.
    echo Please check the error messages above.
    echo Common issues:
    echo   - Internet connection required
    echo   - Some packages may need Visual C++ Build Tools
    echo   - Try running as Administrator
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ============================================================
    echo   SUCCESS: All dependencies installed!
    echo ============================================================
    echo.
    echo You can now start the backend with:
    echo   python start_backend.py
    echo.
    echo Or create dummy users with:
    echo   python create_dummy_users.py
    echo.
)

pause
