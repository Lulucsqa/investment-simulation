@echo off
REM Manual startup script for Investment Simulation System (No Docker)
REM This runs the system using Python directly

echo 🚀 Investment Simulation System - Manual Start
echo =============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [INFO] Python found ✅
echo.

REM Create necessary directories
if not exist "outputs" mkdir outputs
if not exist "backend" mkdir backend

echo [INFO] Starting Backend API Server...
echo.

REM Start the FastAPI backend server
echo [INFO] Backend API will be available at: http://localhost:8000
echo [INFO] API Documentation will be at: http://localhost:8000/docs
echo.
echo [INFO] Press Ctrl+C to stop the server
echo.

REM Start the server
python -m uvicorn backend.api:app --host 0.0.0.0 --port 8000 --reload