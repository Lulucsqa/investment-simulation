@echo off
REM Start the original Python simulation (No Docker needed)

echo 🚀 Investment Simulation System - Python Simulation
echo ==================================================
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

REM Create outputs directory
if not exist "outputs" mkdir outputs

echo [INFO] Running Investment Simulation...
echo [INFO] Results will be saved in the 'outputs' directory
echo [INFO] Charts will be generated as JPG files
echo.

REM Run the main simulation
python main.py

echo.
echo [INFO] Simulation completed! ✅
echo [INFO] Check the 'outputs' directory for generated charts
echo.
pause