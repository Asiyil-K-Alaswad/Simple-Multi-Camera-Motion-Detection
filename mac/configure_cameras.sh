#!/bin/bash

echo "========================================"
echo "Camera Configuration Tool"
echo "========================================"
echo
echo "Starting camera configuration..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed or not in PATH"
    echo "Please install Python3 and try again."
    echo "You can install Python3 using Homebrew: brew install python3"
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if we're in the correct directory
if [ ! -f "launcher.py" ]; then
    echo "ERROR: launcher.py not found in current directory"
    echo "Please run this script from the project directory."
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if virtual environment exists and activate it if present
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Virtual environment activated."
    echo
else
    echo "Warning: No virtual environment found. Using system Python."
    echo
fi

# Run the camera configuration tool
echo "Starting camera configuration tool..."
python3 launcher.py

# Check if the script ran successfully
if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Camera configuration failed to start"
    echo "Please check the error messages above."
    echo
    read -p "Press Enter to continue..."
    exit 1
fi

echo
echo "Camera configuration completed."
echo "You can now run 'python3 main.py' to start the main application."
echo
read -p "Press Enter to continue..." 