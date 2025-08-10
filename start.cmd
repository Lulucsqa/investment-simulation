@echo off
REM Simple Windows deployment script for Investment Simulation System
REM This is the simplest way to deploy on Windows

echo 🚀 Investment Simulation System - Quick Start
echo ============================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker Desktop first.
    echo.
    echo 1. Open Docker Desktop
    echo 2. Wait for it to start completely
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo [INFO] Docker is running ✅
echo.

REM Create directories
if not exist "outputs" mkdir outputs
if not exist "backend" mkdir backend

echo [INFO] Starting Investment Simulation System...
echo.

REM Start services
docker-compose up -d

echo.
echo [INFO] Waiting for services to start...
timeout /t 15 /nobreak >nul

echo.
echo 🎉 Investment Simulation System is starting!
echo.
echo 📊 Access your application:
echo    Frontend: http://localhost
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
echo 📝 Useful commands:
echo    Check status: python status.py
echo    Health check: python health-check.py
echo    View logs: docker-compose logs -f
echo    Stop system: docker-compose down
echo.
echo Press any key to open the application in your browser...
pause >nul

REM Open browser
start http://localhost