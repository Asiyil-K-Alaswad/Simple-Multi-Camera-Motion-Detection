#!/bin/bash

echo "========================================"
echo "macOS Setup Script for Multi-Camera"
echo "Object Tracking System"
echo "========================================"
echo

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    echo "This will install the package manager for macOS."
    echo
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo
    echo "Homebrew installed successfully!"
    echo
else
    echo "Homebrew found. Updating..."
    brew update
    echo
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Installing Python3..."
    brew install python3
    echo
else
    echo "Python3 found: $(python3 --version)"
fi

# Check if pip3 is available
if ! command -v pip3 &> /dev/null; then
    echo "pip3 not found. Installing pip3..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
    echo
else
    echo "pip3 found: $(pip3 --version)"
fi

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created successfully!"
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment and install requirements
echo "Activating virtual environment and installing requirements..."
source venv/bin/activate

# Upgrade pip
pip3 install --upgrade pip

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
    echo "Dependencies installed successfully!"
else
    echo "Warning: requirements.txt not found. Installing common dependencies..."
    pip3 install opencv-python numpy torch torchvision
    echo "Basic dependencies installed."
fi

echo
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo
echo "Next steps:"
echo "1. Run './configure_cameras.sh' to configure your cameras"
echo "2. Run './run_application.sh' to start the main application"
echo "3. Or run './run_demo.sh' to test the demo mode"
echo
echo "Note: Make sure to run these scripts from the project root directory."
echo
read -p "Press Enter to continue..." 