@echo off
echo ============================================================
echo   Cloud Monitoring System - Backend Setup and Start
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Test dependencies
echo Testing dependencies...
python test_dependencies.py
echo.

REM Start backend
echo.
echo ============================================================
echo   Starting Backend Server...
echo ============================================================
echo.
python start_backend.py

pause
