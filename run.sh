#!/bin/bash
# BookKeeper Pro Run Script (Linux/Mac)

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting BookKeeper Pro...${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found.${NC}"
    echo "Please run setup.sh first:"
    echo "  ${BLUE}./setup.sh${NC}"
    exit 1
fi

# Use the venv's Python directly
VENV_PYTHON="./venv/bin/python"

# Check if tkinter is available (system dependency)
$VENV_PYTHON -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: tkinter is not installed.${NC}"
    echo ""
    echo "tkinter is a system package required for the GUI."
    echo "Please install it using your package manager:"
    echo ""
    echo "  ${BLUE}Ubuntu/Debian:${NC}"
    echo "    sudo apt-get install python3-tk"
    echo ""
    echo "  ${BLUE}Fedora:${NC}"
    echo "    sudo dnf install python3-tkinter"
    echo ""
    echo "  ${BLUE}Arch Linux:${NC}"
    echo "    sudo pacman -S tk"
    echo ""
    exit 1
fi

# Check if customtkinter is installed
$VENV_PYTHON -c "import customtkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Dependencies not installed.${NC}"
    echo "Please run setup.sh first:"
    echo "  ${BLUE}./setup.sh${NC}"
    exit 1
fi

# Run the application
echo -e "${GREEN}✓ Dependencies verified${NC}"
echo -e "${GREEN}Launching BookKeeper Pro...${NC}"
echo ""
$VENV_PYTHON main.py
