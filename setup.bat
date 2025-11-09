@echo off
REM BookKeeper Pro Setup Script (Windows)
REM This script sets up a virtual environment and installs dependencies

echo =========================================
echo   BookKeeper Pro - Setup Script
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher and try again.
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Check if tkinter is available
echo Checking for tkinter...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo Warning: tkinter is not available.
    echo.
    echo tkinter should come pre-installed with Python on Windows.
    echo If you're seeing this, you may have a minimal Python installation.
    echo.
    echo Please reinstall Python from python.org and make sure to:
    echo   1. Check "tcl/tk and IDLE" during installation
    echo   2. Or use the full installer instead of minimal
    echo.
    pause
    exit /b 1
)
echo tkinter is available
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Create necessary directories
echo Creating necessary directories...
if not exist "data" mkdir data
if not exist "exports" mkdir exports
if not exist "backups" mkdir backups
if not exist "assets\icons" mkdir assets\icons
echo Directories created
echo.

REM Success message
echo.
echo =========================================
echo   Setup completed successfully!
echo =========================================
echo.
echo To run BookKeeper Pro:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate.bat
echo   2. Run the application:
echo      python main.py
echo.
echo Or simply use the run script:
echo   run.bat
echo.
pause
