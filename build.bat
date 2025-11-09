@echo off
REM BookKeeper Pro Build Script (Windows)
REM This script creates a standalone executable using PyInstaller

setlocal enabledelayedexpansion

echo =========================================
echo   BookKeeper Pro - Build Script
echo =========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Error: Virtual environment not found.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    echo.
)

REM Parse command line arguments
set BUILD_TYPE=onefile
set OUTPUT_NAME=BookKeeperPro

:parse_args
if "%~1"=="" goto end_parse_args
if /i "%~1"=="--onedir" (
    set BUILD_TYPE=onedir
    shift
    goto parse_args
)
if /i "%~1"=="--onefile" (
    set BUILD_TYPE=onefile
    shift
    goto parse_args
)
if /i "%~1"=="--name" (
    set OUTPUT_NAME=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--help" (
    echo Usage: build.bat [OPTIONS]
    echo.
    echo Options:
    echo   --onefile    Create a single executable file ^(default^)
    echo   --onedir     Create a directory with executable and dependencies
    echo   --name NAME  Set custom executable name ^(default: BookKeeperPro^)
    echo   --help       Show this help message
    echo.
    exit /b 0
)
echo Unknown option: %~1
echo Use --help for usage information
pause
exit /b 1

:end_parse_args

REM Create build directory if it doesn't exist
if not exist "build" mkdir build
if not exist "dist" mkdir dist

REM Clean previous builds
echo Cleaning previous builds...
if exist "build\*" del /Q build\*
if exist "dist\*" rmdir /S /Q dist
echo.

REM Build the executable
echo Building executable...
echo Build type: %BUILD_TYPE%
echo Output name: %OUTPUT_NAME%
echo.

if "%BUILD_TYPE%"=="onefile" (
    pyinstaller --onefile ^
        --name="%OUTPUT_NAME%" ^
        --windowed ^
        --add-data "src;src" ^
        --hidden-import=customtkinter ^
        --hidden-import=PIL ^
        --hidden-import=PIL._imagingtk ^
        --hidden-import=PIL._tkinter_finder ^
        --collect-all=customtkinter ^
        --noconfirm ^
        main.py
) else (
    pyinstaller --onedir ^
        --name="%OUTPUT_NAME%" ^
        --windowed ^
        --add-data "src;src" ^
        --hidden-import=customtkinter ^
        --hidden-import=PIL ^
        --hidden-import=PIL._imagingtk ^
        --hidden-import=PIL._tkinter_finder ^
        --collect-all=customtkinter ^
        --noconfirm ^
        main.py
)

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo =========================================
echo   Build completed successfully!
echo =========================================
echo.
echo Executable location:
if "%BUILD_TYPE%"=="onefile" (
    echo   dist\%OUTPUT_NAME%.exe
) else (
    echo   dist\%OUTPUT_NAME%\%OUTPUT_NAME%.exe
)
echo.
echo To run the executable:
if "%BUILD_TYPE%"=="onefile" (
    echo   dist\%OUTPUT_NAME%.exe
) else (
    echo   dist\%OUTPUT_NAME%\%OUTPUT_NAME%.exe
)
echo.

REM Deactivate virtual environment
deactivate
pause
