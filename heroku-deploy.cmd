@echo off
REM Heroku Deployment Script for Investment Simulation System

echo 🚀 Investment Simulation System - Heroku Deployment
echo ===================================================

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Heroku CLI is not installed
    echo.
    echo Please install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli
    echo.
    echo After installation:
    echo 1. Run: heroku login
    echo 2. Run this script again
    echo.
    pause
    exit /b 1
)

echo [INFO] Heroku CLI found ✅
echo.

REM Check if git is initialized
if not exist ".git" (
    echo [INFO] Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit for Investment Simulation System"
)

echo [INFO] Logging into Heroku...
heroku login

echo.
echo [INFO] Creating Heroku app...
set /p APP_NAME="Enter your app name (or press Enter for auto-generated): "

if "%APP_NAME%"=="" (
    heroku create
) else (
    heroku create %APP_NAME%
)

if %errorlevel% neq 0 (
    echo [ERROR] Failed to create Heroku app
    pause
    exit /b 1
)

echo.
echo [INFO] Setting environment variables...
heroku config:set ENVIRONMENT=production
heroku config:set DEBUG=false

echo.
echo [INFO] Deploying to Heroku...
git add .
git commit -m "Deploy Investment Simulation System to Heroku"
git push heroku main

if %errorlevel% neq 0 (
    echo [ERROR] Deployment failed
    echo.
    echo Common solutions:
    echo 1. Make sure you're on the 'main' branch
    echo 2. Try: git push heroku master
    echo 3. Check heroku logs: heroku logs --tail
    pause
    exit /b 1
)

echo.
echo 🎉 Deployment completed successfully!
echo.
echo 📊 Your Investment Simulation System is now live:
heroku open

echo.
echo 📝 Useful Heroku commands:
echo   View logs: heroku logs --tail
echo   Open app: heroku open
echo   App info: heroku apps:info
echo   Scale app: heroku ps:scale web=1
echo.
pause