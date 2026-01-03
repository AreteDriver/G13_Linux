#!/bin/bash
# G13LogitechOPS Installation Script

set -e

echo "================================================================"
echo "G13LogitechOPS Installation"
echo "================================================================"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "Error: Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi
echo "✓ Python $PYTHON_VERSION found"

# Check for system dependencies
echo ""
echo "Checking system dependencies..."

MISSING_DEPS=()

if ! python3 -c "import hid" 2>/dev/null; then
    MISSING_DEPS+=("libhidapi (python hidapi)")
fi

if ! python3 -c "import evdev" 2>/dev/null; then
    MISSING_DEPS+=("python evdev")
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    echo "Missing dependencies: ${MISSING_DEPS[@]}"
    echo ""
    echo "Please install them using your package manager:"
    echo ""
    
    if [ -f /etc/debian_version ]; then
        echo "  sudo apt-get install python3-pip libhidapi-hidraw0 libhidapi-libusb0"
        echo "  pip3 install -r requirements.txt"
    elif [ -f /etc/redhat-release ]; then
        echo "  sudo dnf install python3-pip hidapi"
        echo "  pip3 install -r requirements.txt"
    elif [ -f /etc/arch-release ]; then
        echo "  sudo pacman -S python-pip hidapi"
        echo "  pip3 install -r requirements.txt"
    else
        echo "  pip3 install -r requirements.txt"
    fi
    echo ""
    
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists."
    read -p "Recreate it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .venv
        python3 -m venv .venv
        echo "✓ Virtual environment created"
    fi
else
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi

# Activate and install
echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing G13LogitechOPS..."
pip install --upgrade pip > /dev/null 2>&1
pip install -e .
echo "✓ G13LogitechOPS installed"

# Install udev rules
echo ""
echo "Installing udev rules..."
if [ -f "udev/99-logitech-g13.rules" ]; then
    read -p "Install udev rules for non-root access? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        sudo cp udev/99-logitech-g13.rules /etc/udev/rules.d/
        sudo udevadm control --reload-rules
        sudo udevadm trigger
        echo "✓ Udev rules installed"
        echo "  Please unplug and replug your G13 keyboard"
    fi
fi

echo ""
echo "================================================================"
echo "Installation Complete!"
echo "================================================================"
echo ""
echo "To use G13LogitechOPS:"
echo "  1. Activate the virtual environment: source .venv/bin/activate"
echo "  2. Run: g13-ops"
echo "  3. Or: python -m g13_ops.cli"
echo ""
echo "For more information, see README.md"
echo ""
