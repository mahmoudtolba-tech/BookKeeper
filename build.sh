#!/bin/bash
# BookKeeper Pro Build Script (Linux/Mac)
# This script creates a standalone executable using PyInstaller

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "========================================="
echo "  BookKeeper Pro - Build Script"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found.${NC}"
    echo "Please run setup.sh first:"
    echo "  ${BLUE}./setup.sh${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if PyInstaller is installed
if ! pip show pyinstaller &> /dev/null; then
    echo -e "${YELLOW}PyInstaller not found. Installing...${NC}"
    pip install pyinstaller
fi

# Parse command line arguments
BUILD_TYPE="onefile"
OUTPUT_NAME="BookKeeperPro"

while [[ $# -gt 0 ]]; do
    case $1 in
        --onedir)
            BUILD_TYPE="onedir"
            shift
            ;;
        --onefile)
            BUILD_TYPE="onefile"
            shift
            ;;
        --name)
            OUTPUT_NAME="$2"
            shift 2
            ;;
        --help)
            echo "Usage: ./build.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --onefile    Create a single executable file (default)"
            echo "  --onedir     Create a directory with executable and dependencies"
            echo "  --name NAME  Set custom executable name (default: BookKeeperPro)"
            echo "  --help       Show this help message"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Create build directory if it doesn't exist
mkdir -p build dist

# Clean previous builds
echo -e "${BLUE}Cleaning previous builds...${NC}"
rm -rf build/* dist/*
echo ""

# Build the executable
echo -e "${BLUE}Building executable...${NC}"
echo "Build type: $BUILD_TYPE"
echo "Output name: $OUTPUT_NAME"
echo ""

if [ "$BUILD_TYPE" = "onefile" ]; then
    pyinstaller --onefile \
        --name="$OUTPUT_NAME" \
        --windowed \
        --add-data "src:src" \
        --hidden-import=customtkinter \
        --hidden-import=PIL \
        --hidden-import=PIL._imagingtk \
        --hidden-import=PIL._tkinter_finder \
        --collect-all=customtkinter \
        --noconfirm \
        main.py
else
    pyinstaller --onedir \
        --name="$OUTPUT_NAME" \
        --windowed \
        --add-data "src:src" \
        --hidden-import=customtkinter \
        --hidden-import=PIL \
        --hidden-import=PIL._imagingtk \
        --hidden-import=PIL._tkinter_finder \
        --collect-all=customtkinter \
        --noconfirm \
        main.py
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo -e "${GREEN}  Build completed successfully!${NC}"
    echo "========================================="
    echo ""
    echo "Executable location:"
    if [ "$BUILD_TYPE" = "onefile" ]; then
        echo "  ${GREEN}dist/$OUTPUT_NAME${NC}"
    else
        echo "  ${GREEN}dist/$OUTPUT_NAME/$OUTPUT_NAME${NC}"
    fi
    echo ""
    echo "To run the executable:"
    if [ "$BUILD_TYPE" = "onefile" ]; then
        echo "  ${BLUE}./dist/$OUTPUT_NAME${NC}"
    else
        echo "  ${BLUE}./dist/$OUTPUT_NAME/$OUTPUT_NAME${NC}"
    fi
    echo ""
else
    echo -e "${RED}Build failed!${NC}"
    exit 1
fi

# Deactivate virtual environment
deactivate
