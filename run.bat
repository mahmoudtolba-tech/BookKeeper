@echo off
REM BookKeeper Pro Run Script (Windows)

echo Starting BookKeeper Pro...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Error: Virtual environment not found.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Use the venv's Python directly
set VENV_PYTHON=venv\Scripts\python.exe

REM Check if dependencies are installed
%VENV_PYTHON% -c "import customtkinter" >nul 2>&1
if errorlevel 1 (
    echo Error: Dependencies not installed.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Run the application
echo Dependencies verified
echo Launching BookKeeper Pro...
echo.
%VENV_PYTHON% main.py

pause
