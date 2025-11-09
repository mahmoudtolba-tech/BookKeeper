#!/bin/bash
# BookKeeper Pro Setup Script (Linux/Mac)
# This script sets up a virtual environment and installs dependencies

echo "========================================="
echo "  BookKeeper Pro - Setup Script"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

echo -e "${BLUE}Python version:${NC}"
python3 --version
echo ""

# Check Python version (must be 3.8+)
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Error: Python 3.8 or higher is required.${NC}"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Check if tkinter is available (required for GUI)
echo -e "${BLUE}Checking for tkinter...${NC}"
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}tkinter is not installed.${NC}"
    echo ""
    echo "tkinter is a system package required for the GUI."
    echo "This script can install it for you (requires sudo)."
    echo ""

    # Detect package manager
    if command -v apt-get &> /dev/null; then
        INSTALL_CMD="sudo apt-get install -y python3-tk"
        PKG_MANAGER="apt-get (Debian/Ubuntu)"
    elif command -v dnf &> /dev/null; then
        INSTALL_CMD="sudo dnf install -y python3-tkinter"
        PKG_MANAGER="dnf (Fedora)"
    elif command -v pacman &> /dev/null; then
        INSTALL_CMD="sudo pacman -S --noconfirm tk"
        PKG_MANAGER="pacman (Arch)"
    elif command -v zypper &> /dev/null; then
        INSTALL_CMD="sudo zypper install -y python3-tk"
        PKG_MANAGER="zypper (openSUSE)"
    else
        echo -e "${RED}Could not detect package manager.${NC}"
        echo "Please install tkinter manually and run this script again."
        exit 1
    fi

    echo "Detected package manager: ${PKG_MANAGER}"
    echo "Command to run: ${INSTALL_CMD}"
    echo ""
    read -p "Install tkinter now? [Y/n] " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        echo -e "${BLUE}Installing tkinter...${NC}"
        eval $INSTALL_CMD

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ tkinter installed successfully${NC}"
            echo ""

            # Verify installation
            python3 -c "import tkinter" 2>/dev/null
            if [ $? -ne 0 ]; then
                echo -e "${RED}Error: tkinter installation failed or Python can't find it.${NC}"
                echo "You may need to restart your terminal or install a different Python-tkinter package."
                exit 1
            fi
        else
            echo -e "${RED}Failed to install tkinter.${NC}"
            echo "Please install it manually using:"
            echo "  ${INSTALL_CMD}"
            exit 1
        fi
    else
        echo ""
        echo "Installation cancelled. Please install tkinter manually:"
        echo "  ${INSTALL_CMD}"
        echo ""
        echo "Then run this setup script again."
        exit 1
    fi
else
    echo -e "${GREEN}✓ tkinter is available${NC}"
fi
echo ""

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}Virtual environment already exists. Skipping creation.${NC}"
else
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Virtual environment created successfully${NC}"
    else
        echo -e "${RED}✗ Failed to create virtual environment${NC}"
        exit 1
    fi
fi
echo ""

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
else
    echo -e "${RED}✗ Failed to activate virtual environment${NC}"
    exit 1
fi
echo ""

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip
echo ""

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi
echo ""

# Create necessary directories
echo -e "${BLUE}Creating necessary directories...${NC}"
mkdir -p data exports backups assets/icons
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Success message
echo ""
echo "========================================="
echo -e "${GREEN}  Setup completed successfully!${NC}"
echo "========================================="
echo ""
echo "To run BookKeeper Pro:"
echo "  1. Activate the virtual environment:"
echo "     ${BLUE}source venv/bin/activate${NC}"
echo "  2. Run the application:"
echo "     ${BLUE}python main.py${NC}"
echo ""
echo "Or simply use the run script:"
echo "  ${BLUE}./run.sh${NC}"
echo ""
