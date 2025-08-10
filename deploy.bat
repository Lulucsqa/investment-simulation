@echo off
REM Investment Simulation System Deployment Script for Windows
REM This script handles the complete deployment of both backend and frontend
REM Usage: .\deploy.bat

echo.
echo ========================================================
echo 🚀 Investment Simulation System Deployment
echo ========================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist "outputs" mkdir outputs
if not exist "backend" mkdir backend

REM Set environment variables
set COMPOSE_PROJECT_NAME=investment-simulation

REM Build and start services
echo [INFO] Building and starting services...
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

REM Wait for services to be ready
echo [INFO] Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are running
echo [INFO] Checking service status...
curl -f http://localhost:8000/ >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] ✅ Backend API is running at http://localhost:8000
) else (
    echo [WARNING] ⚠️  Backend API might not be ready yet. Check logs with: docker-compose logs backend
)

curl -f http://localhost/ >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] ✅ Frontend is running at http://localhost
) else (
    echo [WARNING] ⚠️  Frontend might not be ready yet. Check logs with: docker-compose logs frontend
)

echo.
echo [INFO] 🎉 Deployment completed!
echo.
echo [INFO] 📊 Investment Simulation System is now running:
echo [INFO]    Frontend: http://localhost
echo [INFO]    Backend API: http://localhost:8000
echo [INFO]    API Documentation: http://localhost:8000/docs
echo.
echo [INFO] 📝 Useful commands:
echo [INFO]    View logs: docker-compose logs -f
echo [INFO]    Stop services: docker-compose down
echo [INFO]    Restart services: docker-compose restart
echo [INFO]    View running containers: docker-compose ps
echo.
pause